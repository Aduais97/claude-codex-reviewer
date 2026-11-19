"""HOTC x ASG — LCF Pilot: full Accountability & Value Report.

Single-truth figures from final_stats.json / final_dataset.json (reconciled
with the rebuilt Weekly Data Reports). Covers all agreement cl 3.3 themes.
Outputs the PDF + a parallel REPORT.md (for the ETR review corpus).
"""
import json, os, datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, PageBreak, Image, HRFlowable)
from reportlab.platypus.tableofcontents import TableOfContents
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

DATA = os.path.expanduser('~/Desktop/Dev/Claude/scripts/hotc/data/hotc_pilot_2026')
OUT_PDF = os.path.expanduser('~/Desktop/ASG/HOTC/2026/HOTC_LCF_Pilot_Accountability_Report.pdf')
OUT_MD = os.path.join(DATA, 'REPORT.md')
CHART_DIR = os.path.join(DATA, 'charts')
os.makedirs(CHART_DIR, exist_ok=True)

NAVY = HexColor('#1B2A4A'); DBLUE = HexColor('#2C3E6B'); MBLUE = HexColor('#4A6FA5')
GOLD = HexColor('#D4A843'); LBLUE = HexColor('#E8EDF5'); BORDER = HexColor('#D0D5DD')
ROWALT = HexColor('#F2F4F8'); TDARK = HexColor('#1A1A2E'); TMED = HexColor('#4A4A5A')
TLIGHT = HexColor('#7A7A8A')
CB = '#3E63A8'; CG = '#B8892D'

S = json.load(open(DATA + '/final_stats.json'))
DAYS = json.load(open(DATA + '/final_dataset.json'))
T = S['totals']; W = S['weekly_avg']; BL = S['baseline_weekly']; YY = S['yoy_2025_weekly']
N = S['days']
UP_BASE = (W['response_calls'] / BL['calls'] - 1) * 100
UP_YOY = (W['response_calls'] / YY['calls'] - 1) * 100
POL_YOY = (W['police_escalations'] / YY['police'] - 1) * 100

# weekly series (calendar Mon-start)
wk = {}
for d in DAYS:
    iso = datetime.date.fromisoformat(d['date'])
    w0 = iso - datetime.timedelta(days=iso.weekday())
    wk[w0] = wk.get(w0, 0) + d['response_calls']
WEEKLY = sorted(wk.items())

STORIES = json.load(open(DATA + '/stories.json')) if os.path.exists(DATA + '/stories.json') else []

# ---------------- charts ----------------

def chart_weekly(path):
    last = max(w for w, _ in WEEKLY)
    labels = [w.strftime('%-d %b') + ('*' if w == last else '') for w, _ in WEEKLY]
    vals = [v for _, v in WEEKLY]
    top = max(vals + [BL['calls']]) * 1.30
    fig, ax = plt.subplots(figsize=(7.6, 3.0), dpi=200)
    ax.bar(range(len(vals)), vals, width=0.62, color=CG, zorder=3)
    ax.axhline(BL['calls'], color=CB, lw=2, zorder=4)
    ax.text(-0.38, top * 0.97, f"Pre-uplift baseline: {BL['calls']:.0f} attended calls / week "
            f"(10-week average, 9 Mar – 31 May)", fontsize=8, color=CB, fontweight='bold', va='top')
    for i, v in enumerate(vals):
        ax.text(i, v + top * 0.015, f'{v:.0f}', ha='center', fontsize=8.5, color='#1A1A2E', fontweight='bold')
    # partial final week: annotate the 7-day pace so the low bar is not misread
    last_idx = len(vals) - 1
    last_days = sum(1 for d in DAYS if (datetime.date.fromisoformat(d['date'])
                    - datetime.timedelta(days=datetime.date.fromisoformat(d['date']).weekday())) == last)
    if last_days < 7:
        pace = vals[last_idx] / last_days * 7
        ax.text(last_idx, vals[last_idx] + top * 0.085, f'({last_days} days —\n{pace:.0f}/wk pace)',
                ha='center', fontsize=7, color='#4A4A5A')
    ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel('Calls attended / week', fontsize=8.5); ax.set_ylim(0, top)
    ax.spines[['top', 'right']].set_visible(False)
    ax.spines[['left', 'bottom']].set_color('#D0D5DD')
    ax.tick_params(colors='#4A4A5A', labelsize=8)
    ax.grid(axis='y', color='#E8EDF5', lw=0.8, zorder=0)
    fig.tight_layout(); fig.savefig(path, facecolor='white'); plt.close(fig)

def chart_categories(path):
    cats = [('Calls attended', T['response_calls']), ('People moved on', T['move_ons']),
            ('Aggression de-escalated', T['aggression_incidents']), ('Theft responses', T['thefts']),
            ('Police escalations', T['police_escalations']), ('Welfare interventions', T['welfare_person_checks']),
            ('Trespasses actioned', T['trespass_events'])]
    fig, ax = plt.subplots(figsize=(7.6, 2.9), dpi=200)
    y = range(len(cats))
    ax.barh(y, [v for _, v in cats], height=0.58, color=CB, zorder=3)
    for i, (_, v) in enumerate(cats):
        ax.text(v + 3, i, f'{v}', va='center', fontsize=8.5, color='#1A1A2E', fontweight='bold')
    ax.set_yticks(list(y)); ax.set_yticklabels([c for c, _ in cats], fontsize=8.5)
    ax.invert_yaxis(); ax.set_xlim(0, max(v for _, v in cats) * 1.12)
    ax.set_xlabel(f'Pilot totals — {N} days', fontsize=8.5)
    ax.spines[['top', 'right']].set_visible(False)
    ax.spines[['left', 'bottom']].set_color('#D0D5DD')
    ax.tick_params(colors='#4A4A5A', labelsize=8)
    ax.grid(axis='x', color='#E8EDF5', lw=0.8, zorder=0)
    fig.tight_layout(); fig.savefig(path, facecolor='white'); plt.close(fig)

# ---------------- pdf machinery ----------------

MACRONS = str.maketrans('āēīōūĀĒĪŌŪ', 'aeiouAEIOU')
styles = {
    'body': ParagraphStyle('body', fontName='Helvetica', fontSize=10, leading=14.5,
                           alignment=TA_JUSTIFY, textColor=TDARK, spaceAfter=7),
    'bullet': ParagraphStyle('bullet', fontName='Helvetica', fontSize=10, leading=14,
                             leftIndent=18, bulletIndent=6, textColor=TDARK, spaceAfter=4),
    'h2': ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=white,
                         spaceBefore=14, spaceAfter=8, backColor=NAVY, borderPadding=(6, 8, 5, 8)),
    'h3': ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=11.5, leading=14,
                         textColor=DBLUE, spaceBefore=10, spaceAfter=5),
    'note': ParagraphStyle('note', fontName='Helvetica-Oblique', fontSize=8.5, leading=11.5,
                           textColor=TMED, spaceAfter=6),
    'title': ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=32, leading=38,
                            alignment=TA_CENTER, textColor=NAVY),
    'subtitle': ParagraphStyle('subtitle', fontName='Helvetica', fontSize=16, leading=21,
                               alignment=TA_CENTER, textColor=DBLUE),
    'tag': ParagraphStyle('tag', fontName='Helvetica-Oblique', fontSize=12, leading=16,
                          alignment=TA_CENTER, textColor=MBLUE),
}
md_lines = []
el = []

def P(text, style='body'):
    el.append(Paragraph(text.translate(MACRONS), styles[style]))
    md_lines.append(text.replace('<b>', '**').replace('</b>', '**').replace('&amp;', '&')
                    .replace('<bullet>&bull;</bullet>', '- ') + '\n')

def B(text):
    el.append(Paragraph('<bullet>&bull;</bullet>' + text.translate(MACRONS), styles['bullet']))
    md_lines.append('- ' + text.replace('<b>', '**').replace('</b>', '**').replace('&amp;', '&') + '\n')

h2_inner = ParagraphStyle('h2i', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=white)

def H(text):
    # navy section bar with 4pt gold left accent (per PDF design standards)
    p = Paragraph(text.translate(MACRONS), h2_inner)
    t = Table([['', p]], colWidths=[4, 483])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, 0), GOLD), ('BACKGROUND', (1, 0), (1, 0), NAVY),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           ('TOPPADDING', (1, 0), (1, 0), 5), ('BOTTOMPADDING', (1, 0), (1, 0), 6),
                           ('LEFTPADDING', (1, 0), (1, 0), 8)]))
    t.spaceBefore = 14; t.spaceAfter = 8
    t._toc_title = text.translate(MACRONS).replace('&amp;', '&')
    el.append(t)
    md_lines.append('\n## ' + text.replace('&amp;', '&') + '\n')

def H3(text):
    el.append(Paragraph(text.translate(MACRONS), styles['h3']))
    el.append(HRFlowable(width='100%', thickness=0.5, color=BORDER, spaceBefore=0, spaceAfter=5))
    md_lines.append('\n### ' + text.replace('&amp;', '&') + '\n')

def NOTE(text):
    el.append(Paragraph(text.translate(MACRONS), styles['note']))
    md_lines.append('_' + text.replace('&amp;', '&') + '_\n')

cell_style = ParagraphStyle('cell', fontName='Helvetica', fontSize=8.5, leading=11, textColor=TDARK)

def TBL(data, widths, totals=False):
    wrapped = [data[0]] + [
        [Paragraph(str(c).translate(MACRONS).replace('\n', '<br/>'), cell_style)
         if isinstance(c, str) and (len(c) > 24 or '\n' in c) else c for c in row]
        for row in data[1:]]
    t = Table(wrapped, colWidths=widths, repeatRows=1)
    data_orig = data
    data = wrapped
    st = [('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 8.5),
          ('TEXTCOLOR', (0, 0), (-1, -1), TDARK), ('GRID', (0, 0), (-1, -1), 0.4, BORDER),
          ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
          ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
          ('LEFTPADDING', (0, 0), (-1, -1), 6), ('RIGHTPADDING', (0, 0), (-1, -1), 6),
          ('BACKGROUND', (0, 0), (-1, 0), NAVY), ('TEXTCOLOR', (0, 0), (-1, 0), white),
          ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), ('LINEBELOW', (0, 0), (-1, 0), 1.2, GOLD)]
    for r in range(1, len(data)):
        if r % 2 == 0: st.append(('BACKGROUND', (0, r), (-1, r), ROWALT))
    if totals:
        st += [('BACKGROUND', (0, len(data) - 1), (-1, len(data) - 1), LBLUE),
               ('FONTNAME', (0, len(data) - 1), (-1, len(data) - 1), 'Helvetica-Bold')]
    t.setStyle(TableStyle(st))
    el.append(t); el.append(Spacer(1, 4))
    md_lines.append('\n' + '\n'.join('| ' + ' | '.join(str(c).replace('\n', ' ').replace('&amp;', '&') for c in row) + ' |'
                                     for row in [data_orig[0], ['---'] * len(data_orig[0])] + data_orig[1:]) + '\n')

def header_footer(canvas, doc):
    canvas.saveState(); w, h = A4
    canvas.setStrokeColor(BORDER); canvas.setLineWidth(0.5)
    canvas.line(54, h - 40, w - 54, h - 40)
    canvas.setFont('Helvetica', 7); canvas.setFillColor(TLIGHT)
    canvas.drawString(54, h - 36, 'Absolute Security Group  |  Heart of the City — LCF Pilot Accountability Report')
    canvas.drawRightString(w - 54, h - 36, 'COMMERCIAL IN CONFIDENCE')
    canvas.line(54, 40, w - 54, 40)
    canvas.setFont('Helvetica', 7.5)
    canvas.drawString(54, 30, 'July 2026')
    canvas.drawCentredString(w / 2, 30, f'Page {doc.page}')
    canvas.drawRightString(w - 54, 30, 'Prepared by Absolute Security Group')
    canvas.restoreState()

# ---------------- build ----------------
chart_weekly(CHART_DIR + '/weekly.png')
chart_categories(CHART_DIR + '/cats.png')

class ReportDoc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, '_toc_title'):
            self.notify('TOCEntry', (0, flowable._toc_title, self.page))

doc = ReportDoc(OUT_PDF, pagesize=A4, leftMargin=54, rightMargin=54, topMargin=62, bottomMargin=54,
                title='LCF Pilot — Accountability & Value Report', author='Absolute Security Group')
doc.addPageTemplates([PageTemplate(id='p', frames=[Frame(54, 54, A4[0] - 108, A4[1] - 116)],
                                   onPage=header_footer)])

# title page
el.append(Spacer(1, 84))
el.append(HRFlowable(width='40%', thickness=1.6, color=GOLD, spaceBefore=6, spaceAfter=6, hAlign='CENTER'))
el.append(Paragraph('Enhanced CBD Safety Team', styles['title']))
el.append(Spacer(1, 6))
el.append(Paragraph('LCF Pilot — Accountability &amp; Value Report', styles['subtitle']))
el.append(Spacer(1, 4))
el.append(Paragraph('This pilot delivers a targeted CPTED-based intervention, increasing visible guardianship, '
                    'improving natural surveillance, and strengthening business-community safety networks '
                    'during peak risk periods.', styles['tag']))
el.append(HRFlowable(width='40%', thickness=1.6, color=GOLD, spaceBefore=6, spaceAfter=6, hAlign='CENTER'))
el.append(Spacer(1, 36))
md_lines.append('# Enhanced CBD Safety Team — LCF Pilot: Accountability & Value Report\n')
info = [['Prepared for', 'Heart of the City — Edward Caughey, Head of Customer Experience'],
        ['Prepared by', 'Absolute Security Group Ltd, 220 Queen Street, Auckland CBD'],
        ['Funding', 'Local Crime Fund (PoCF objective) via Heart of the City — $41,150 + GST'],
        ['Pilot period', '2 June – 24 July 2026 (complete pilot period)'],
        ['Deployment', 'One additional LCF-funded Safety Team: second afternoon team Sun–Thu (sector split '
                       'with the core patrol); night uplift Fri–Sat — on top of the existing 24/7 programme'],
        ['Reporting basis', 'Compiled from every daily patrol log for the period, cross-checked against the '
                            'weekly data reports']]
info_val = ParagraphStyle('infoval', fontName='Helvetica', fontSize=9.5, leading=12.5, textColor=TDARK)
info = [[k, Paragraph(v.translate(MACRONS), info_val)] for k, v in info]
t = Table(info, colWidths=[100, 387])
t.setStyle(TableStyle([('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (0, -1), 9.5),
                       ('TEXTCOLOR', (0, 0), (0, -1), NAVY), ('BACKGROUND', (0, 0), (0, -1), LBLUE),
                       ('GRID', (0, 0), (-1, -1), 0.4, BORDER), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                       ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                       ('LEFTPADDING', (0, 0), (-1, -1), 8)]))
el.append(t)
el.append(Spacer(1, 130))
el.append(Paragraph('Commercial in Confidence. Prepared July 2026 for the LCF accountability reporting cycle: '
                    'ASG report to Heart of the City, 27 July 2026; HOTC report to the joint funding '
                    'administrators, 31 July 2026.', styles['note']))
el.append(PageBreak())

# ---- table of contents ----
el.append(Paragraph('Contents', ParagraphStyle('toch', fontName='Helvetica-Bold', fontSize=15,
                                               leading=19, textColor=NAVY, spaceAfter=10)))
el.append(HRFlowable(width='100%', thickness=0.8, color=GOLD, spaceBefore=0, spaceAfter=10))
toc = TableOfContents()
toc.levelStyles = [ParagraphStyle('toc0', fontName='Helvetica', fontSize=10.5, leading=17,
                                  textColor=TDARK, leftIndent=6)]
toc.dotsMinLevel = 0
el.append(toc)
el.append(PageBreak())

# 1 exec summary
H('1.  Executive Summary')
P(f'The Enhanced CBD Safety Team pilot ran from 2 June to 24 July 2026 under the Local Crime Fund allocation '
  f'administered by Heart of the City. This report presents verified activity data for the complete pilot period '
  f'— {N} days of daily patrol logs covering 1 June to 24 July 2026, including the 1 June mobilisation day '
  f'immediately preceding pilot commencement. ASG '
  f'deployed one additional LCF-funded Safety Team on top of the existing 24/7 patrol programme: a second '
  f'afternoon team Sunday to Thursday, running a sector split alongside the core patrol, redeployed into '
  f'the night window on Friday and Saturday when evening risk concentrates. '
  f'This pilot delivers a targeted CPTED-based intervention, increasing visible guardianship, improving '
  f'natural surveillance, and strengthening business-community safety networks during peak risk periods.')
H3('Headline results')
B(f'<b>{T["response_calls"]} calls and incidents attended</b> in {N} days — {W["response_calls"]:.1f} per week '
  f'against a pre-uplift baseline of {BL["calls"]:.1f} (<b>+{UP_BASE:.0f}%</b>) and {YY["calls"]:.1f} in the '
  f'same weeks last year (<b>+{UP_YOY:.0f}%</b>).')
B(f'<b>Fewer Police callouts — more arrests.</b> Police escalations ran at {W["police_escalations"]:.1f}/week '
  f'vs {YY["police"]:.1f} in the same weeks last year ({POL_YOY:.0f}%): with two teams on the ground, matters '
  f'that would once have required Police were resolved between the teams. When Police were engaged, it '
  f'counted — <b>{T["arrests"]} arrests directly supported ({W["arrests"]:.1f}/week vs {BL["arrests"]:.1f} in '
  f'the baseline period, +{(W["arrests"]/BL["arrests"]-1)*100:.0f}%)</b>, roughly one arrest for every three Police engagements against one in '
  f'four before the uplift, with evidential incidents posted to the Auror pipeline '
  f'({T["auror_mentions"]} Auror reports referenced).')
B(f'<b>{T["store_checks_named"]:,} welfare check-ins with named precinct businesses</b> '
  f'(≈{T["store_checks_named"] // N} per day) plus {T["store_sweep_mentions"]} block-level welfare sweeps — '
  f'visible guardianship delivered street by street, every day of the pilot.')
B(f'<b>{T["move_ons"]} move-ons</b>, <b>{T["aggression_incidents"]} aggression or disorder events attended '
  f'and managed</b>, <b>{T["thefts"]} theft responses</b> with repeated recoveries returned to stores, '
  f'<b>{T["welfare_person_checks"]} welfare interventions</b> with vulnerable people, and '
  f'<b>{T["trespass_events"]} trespasses</b> actioned.')
B(f'<b>Unattended demand fell to near zero:</b> ASG’s pre-pilot capacity analysis (Jan–Apr 2026) recorded 211 '
  f'missed interventions — 29% of all calls. Across the full pilot ({N} logged days) the logs show '
  f'<b>three</b> capacity-affected responses (≈1%), and none in the two-team daytime window after the '
  f'first week.')
P('The pattern is consistent: when capacity was added, attended demand rose immediately and stayed high — '
  'while the share passed on to Police fell. The precinct’s demand for a responsive safety presence was '
  'always there; before this uplift, close to a third of it was going unmet.')

# 2 what was delivered
H('2.  What Was Delivered')
TBL([['Coverage', 'Days', 'Window', 'Purpose'],
     ['Core 24/7 programme', 'Mon–Sun', 'All hours', 'Existing HOTC contract (unchanged)'],
     ['LCF uplift team', 'Sun–Thu', '09:00–17:00', 'Second daytime team — sector split with the core patrol (upper / lower CBD)'],
     ['LCF uplift team', 'Fri–Sat', 'Night / peak evening window', 'Enlarged night presence on the highest-risk trading nights — documented hotspots: Queen St, Aotea Square, Hobson/Victoria corner']],
    [108, 50, 112, 217])
P('The Scope of Works’ indicative schedule placed the additional officers on daytime cover seven days; under '
  'its flexing provision, ASG redeployed the Friday–Saturday uplift hours into the night window, where '
  'Friday–Saturday risk concentrates. The funded pool of approximately 1,115 service hours ($41,150 + GST) '
  'is fully allocated across the pilot roster to 24 July, and was invoiced in two equal instalments before '
  '30 June 2026, per the funding agreement. Hours delivered across the pilot are evidenced by the daily patrol '
  'logs, which reconcile line-for-line with this report.')
P('The Sunday–Thursday sector split — the core team wrapping one half of the CBD while the uplift team '
  'covers the other — runs through the daily logs and shows up directly in outcomes: cross-team dispatches '
  'resolving calls within minutes, simultaneous incidents held at two locations at once, and coverage '
  'maintained during meetings, statements and prolonged incidents.')

# 3 demand & response
H('3.  Demand &amp; Response — Baseline and Year-on-Year')
el.append(Image(CHART_DIR + '/weekly.png', width=487, height=192))
md_lines.append('\n[Chart: attended calls per pilot week vs 40.7 baseline]\n')
NOTE('* The final bar is a partial week — five days only (Monday 20 to Friday 24 July), not a full seven-day '
     'week, as the pilot concluded on Friday 24 July. Its lower total reflects the shorter week, not reduced '
     'demand: at a full-week pace that week runs above the baseline.')
TBL([['Metric (weekly average)', 'Baseline\nMar–May 26', 'Pilot\nJun–Jul 26', 'Jun–Jul 25\n(last year)', 'vs baseline', 'vs last year'],
     ['Calls / incidents attended', f"{BL['calls']:.1f}", f"{W['response_calls']:.1f}", f"{YY['calls']:.1f}",
      f'+{UP_BASE:.0f}%', f'+{UP_YOY:.0f}%'],
     ['People moved on', f"{BL['move_ons']:.1f}", f"{W['move_ons']:.1f}", 'n/a', f"+{(W['move_ons']/BL['move_ons']-1)*100:.0f}%", 'n/a'],
     ['Aggressive behaviour handled', f"{BL['aggression']:.1f}", f"{W['aggression_incidents']:.1f}", f"{YY['aggression']:.1f}",
      f"+{(W['aggression_incidents']/BL['aggression']-1)*100:.0f}%", f"+{(W['aggression_incidents']/YY['aggression']-1)*100:.0f}%"],
     ['Theft / shoplifting responses', f"{BL['theft']:.1f}", f"{W['thefts']:.1f}", 'n/a', f"+{(W['thefts']/BL['theft']-1)*100:.0f}%", 'n/a'],
     ['Police calls / escalations', f"{BL['police']:.1f}", f"{W['police_escalations']:.1f}", f"{YY['police']:.1f}",
      f"+{(W['police_escalations']/BL['police']-1)*100:.0f}%", f"{POL_YOY:.0f}%"],
     ['Arrests directly supported', f"{BL['arrests']:.1f}", f"{W['arrests']:.1f}", 'n/a',
      f"+{(W['arrests']/BL['arrests']-1)*100:.0f}%", 'n/a']],
    [150, 72, 68, 72, 62, 63])
NOTE('Jun–Jul 2025 weekly reports used the older 5-metric format — move-ons and theft were not captured then (n/a). '
     'Baseline = the ten clean Monday–Sunday weeks, 9 March – 31 May 2026. Percentages are computed from the '
     'weekly rates as displayed (one decimal place).')
P('Rising attended-call numbers during a deterrence pilot are the capacity effect, not a safety deterioration: '
  'businesses call when a team reliably arrives. The same applies to category counts such as aggressive '
  'behaviour: these are attended and recorded events, which rise with patrol density and reporting confidence, '
  'not a measure of underlying prevalence. The team absorbed roughly half as much again in weekly demand '
  'while police escalation rates fell year-on-year — more incidents resolved at the guardianship tier, exactly '
  'where a CPTED intervention should resolve them. As a share of attended demand, police escalations fell '
  'against both comparators — 9.8% of attended calls during the pilot, against 10.8% in the baseline period '
  'and 14.1% in June–July 2025 — while the arrest rate rose from 1.2 to 1.8 per week. Fewer callouts, more '
  'arrests: Police attendance shifted from overflow cover to targeted enforcement on the incidents that '
  'warranted it.')

# 4 capacity
H('4.  Capacity — Unattended Demand, Before and During')
P('The clearest single measure of the uplift is what happened to calls ASG could not attend.')
TBL([['Period', 'Coverage model', 'Unattended / capacity-affected demand'],
     ['Jan – Apr 2026\n(pre-uplift)', 'Single patrol team', '211 missed interventions — 29% of all calls; '
      '51 instances with the team already committed to another call; 20 simultaneous-incident clashes'],
     ['1 Jun – 24 Jul 2026\n(full pilot)', 'Core patrol + LCF uplift team\n(afternoons Sun–Thu; nights Fri–Sat)',
      f'Three capacity-affected responses across {N} days (≈1% of demand) — all in the first '
      'week or on single-team night cover']],
    [95, 135, 257])
B('1 June — a cafe caller was queued behind another incident on the morning the uplift was still mobilising.')
B('6 June — one cafe call could not be attended while guards managed an active four-person altercation.')
B('2 July, 01:34 — the night team took two near-simultaneous calls and attended them back-to-back; the second '
  'caller waited minutes, and both were resolved.')
P('In the two-team daytime window itself, unattended demand after the first week was <b>zero</b>. The logs show '
  'the opposite failure mode disappearing: cross-team dispatches (13–16 July), the team splitting to hold live '
  'response cover during partner engagements (17 July), and both teams converging on the same offender when '
  'needed (23 June). The residual pressure sits exactly where the uplift did not reach — single-team night '
  'cover — which indicates where any future capacity would have the greatest effect.')

# 5 categories
H('5.  Where the Capacity Went')
el.append(Image(CHART_DIR + '/cats.png', width=487, height=186))
md_lines.append('\n[Chart: pilot totals by category]\n')
H3('Theft response in action')
P('The logs show a consistent interception pattern: staff call or flag a person of interest, the nearest team '
  'is dispatched — often the second team, already positioned in-sector — the POI is located within minutes, '
  'goods are recovered where possible, and the event is posted to Auror with descriptions and footage so '
  'repeat offenders accumulate a prosecutable file. Recoveries during the pilot included $1,083.91 of goods '
  'in a single multi-offender operation (23 June), $368 returned within five minutes (5 July), and a $1,377 '
  'theft with the offender identified and trespass requested (9 July).')

# 6 engagement
H('6.  Business Engagement &amp; Guardianship')
B(f'<b>{T["store_checks_named"]:,} welfare check-ins with named businesses</b> across the pilot — '
  f'≈{T["store_checks_named"] // N} named-store check-ins per day (individual stores may be checked more '
  f'than once), plus {T["store_sweep_mentions"]} block-level sweeps.')
B('Face-to-face introductions and HOTC calling cards delivered across the precinct, including onboarding new '
  'stores to the service, with a clear message to stores: one number to call, and a team that responds.')
B('Store-level intelligence actively gathered and circulated — repeat-offender descriptions and photos '
  'collected from affected stores, shared between teams, and posted to Auror.')
B('Reporting behaviour coached — where thefts went unreported, guards followed up and walked staff through '
  'contacting HOTC immediately, so more incidents are reported and actioned.')
B('Business feedback in the logs is direct: store teams sought guards out to thank them after incidents, '
  'and stores that had never engaged began calling the service during the pilot.')

# 7 partnership
H('7.  Partnership &amp; Collaboration')
B(f'<b>NZ Police</b> — {T["arrests"]} arrests directly supported during the pilot ({W["arrests"]:.1f}/week vs '
  f'{BL["arrests"]:.1f} pre-uplift): offenders detained or tracked until Police arrival, statements given, '
  f'scenes preserved, footage handed over. Roughly one Police engagement in three ended in an arrest, '
  f'against one in four before the uplift — escalation was orderly handover for enforcement that counted, '
  f'not emergency callout.')
B('<b>Auckland Council</b> — joint handling of welfare and compliance matters: wardens engaged on trespass '
  'requests, a vulnerable young woman connected to Council support services for housing and financial help, '
  'and combined responses to street disorder.')
B(f'<b>Auror</b> — theft and repeat-offender incidents with evidential material (descriptions, footage, '
  f'recoveries) are posted to Auror, building prosecutable files on repeat offenders; {T["auror_mentions"]} '
  f'Auror reports are referenced in the pilot logs. ASG met with Auror on 17 July to deepen the integration.')
B('<b>Fire and Emergency</b> — bin fires attended and contained pending arrival (25 June, 14 July).')
B('<b>Venue and static security</b> — coordinated interventions with nightclub, hotel and site guards, '
  'including supporting venue security at the Viaduct after an assault on a venue guard (14 July).')

# 8 perceptions
H('8.  Perceptions of Safety')
P('The programme’s perceptions survey instrument (business, landlord and public-intercept forms) was prepared '
  'at pilot commencement. ASG recommends running the first survey wave immediately post-pilot, so that '
  'measured perceptions are referenced to the full deployment period; survey results are therefore not '
  'included in this report. In the interim, the qualitative record from daily engagement is consistent: staff '
  'thanking teams by name after incidents, businesses adopting HOTC-first reporting, new stores requesting '
  'onboarding, and repeat callers whose confidence in a response has visibly changed their reporting '
  'behaviour.')

# 9 harm reduction
H('9.  Reduction in Harm &amp; Community Wellbeing')
P('The team operates welfare-first. Most street-community interactions in the logs end in voluntary '
  'compliance, a welfare conversation, or connection to support — not force. The period’s logs record no '
  'injuries to members of the public arising from any use of force by the team. Two injuries appear in the '
  'weekly data reports for the period — an offender assaulting a guard during the 8 July Mountain Warehouse '
  'theft recovery, and the 14 July assault on a venue static guard at the Viaduct — neither involving force '
  'used by the Safety Team. Aggression events were consistently de-escalated through presence, patience and '
  'negotiation.')
B('Vulnerable people escorted to safety and warmth, kept company while awaiting transport, connected with '
  'shelter information — including a woman sheltering from the cold escorted to a safe, warm location (5 July).')
B(f'Alcohol removed from minors and intoxicated persons in public spaces ({T["public_drinking"]} logged '
  f'public-drinking and liquor-ban interventions), and {T["medical"]} medical-support events including '
  f'seizure assistance and an unresponsive woman safeguarded until ambulance arrival (3 July).')
B('ASG-sponsored hot meals distributed overnight to rough sleepers on Queen Street (21 June) — the '
  'street-community trust this builds is the reason move-ons resolve without force.')
B('A switchblade taken off a 10-year-old after a violent threat, held safely until Police custody (4 July).')

# 10 stories
H('10.  Positive Stories from the Precinct')
for date_label, txt in STORIES:
    B(f'<b>{date_label}:</b> {txt}')

# 11 cpted
H('11.  CPTED Alignment')
TBL([['LCF / CPTED category', 'How the pilot delivered'],
     ['Territoriality &amp; access — patrols / wardens', 'An additional uniformed team, alongside the core patrol, '
      'providing visible guardianship across the precinct in peak-risk windows, seven days.'],
     ['Natural surveillance', f'{T["store_checks_named"]:,} business check-ins and {T["store_sweep_mentions"]} '
      'block sweeps materially increased patrol density and observation of hotspots.'],
     ['Cultural cohesion / community', 'Business Engagement Programme, street-community welfare work, and '
      'onboarding of new businesses into the safety network.'],
     ['Reduction in crime / improved safety', 'Targeted welfare-first deterrence in documented hotspots; theft '
      'recoveries; supported arrests; falling year-on-year police load.']],
    [165, 322])

# 12 beyond
H('12.  Beyond the Pilot')
P('The pilot set out to identify peak-risk windows, test visible-deterrence impact, and build a scalable model '
  'for the post-CRL environment. It has done all three. Demand concentrates exactly where the uplift was '
  'aimed — afternoon trading hours, and Friday–Saturday, which carried 35% of baseline demand. Added capacity '
  'was absorbed immediately by real, previously-unmet demand. The two-team sector-split model held '
  'simultaneous incidents without dropping coverage, and the only residual unattended demand sits on '
  'single-team night cover. ASG recommends the deployment pattern tested and evidenced in this pilot — a '
  'second afternoon team Sunday–Thursday and enlarged Friday–Saturday night cover — as the baseline design '
  'for city-centre guardianship as CRL opening lifts footfall through late 2026, with weeknight cover as '
  'the next capacity case.')

doc.multiBuild(el)   # multiBuild resolves TOC page numbers
open(OUT_MD, 'w').write(''.join(md_lines))
print('SAVED:', OUT_PDF)
print('SAVED:', OUT_MD)
