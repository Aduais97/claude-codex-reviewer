"""HOTC x ASG — LCF Pilot: Accountability Data Summary (meeting handout).
Single-truth figures from final_stats.json / final_dataset.json — reconciled with
the Weekly Data Reports and the full Accountability & Value Report.
"""
import json, os, datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Table, TableStyle, HRFlowable)

DATA = os.path.expanduser('~/Desktop/Dev/Claude/scripts/hotc/data/hotc_pilot_2026')
OUT = os.path.expanduser('~/Desktop/ASG/HOTC/2026/HOTC_LCF_Pilot_Data_Summary.pdf')
NAVY = HexColor('#1B2A4A'); GOLD = HexColor('#D4A843'); LBLUE = HexColor('#E8EDF5')
BORDER = HexColor('#D0D5DD'); ROWALT = HexColor('#F2F4F8'); TDARK = HexColor('#1A1A2E')
TMED = HexColor('#4A4A5A'); TLIGHT = HexColor('#7A7A8A'); DBLUE = HexColor('#2C3E6B')

S = json.load(open(DATA + '/final_stats.json'))
DAYS = json.load(open(DATA + '/final_dataset.json'))
T = S['totals']; W = S['weekly_avg']; BL = S['baseline_weekly']; YY = S['yoy_2025_weekly']
N = S['days']

styles = {
    't': ParagraphStyle('t', fontName='Helvetica-Bold', fontSize=17, leading=21, textColor=NAVY, alignment=TA_CENTER),
    'st': ParagraphStyle('st', fontName='Helvetica', fontSize=10.5, leading=14, textColor=DBLUE, alignment=TA_CENTER),
    'h': ParagraphStyle('h', fontName='Helvetica-Bold', fontSize=11.5, leading=14, textColor=white,
                        backColor=NAVY, borderPadding=(5, 7, 4, 7), spaceBefore=12, spaceAfter=6),
    'n': ParagraphStyle('n', fontName='Helvetica-Oblique', fontSize=8, leading=10.5, textColor=TMED, spaceBefore=3),
    'cell': ParagraphStyle('cell', fontName='Helvetica', fontSize=8.5, leading=11, textColor=TDARK),
}

def T_(data, widths, totals_row=None):
    wrapped = [data[0]] + [[Paragraph(str(c).replace('\n', '<br/>'), styles['cell'])
                            if isinstance(c, str) and (len(c) > 42 or '\n' in c) else c for c in row]
                           for row in data[1:]]
    t = Table(wrapped, colWidths=widths, repeatRows=1)
    st = [('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 8.5),
          ('TEXTCOLOR', (0, 0), (-1, -1), TDARK), ('GRID', (0, 0), (-1, -1), 0.4, BORDER),
          ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
          ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
          ('BACKGROUND', (0, 0), (-1, 0), NAVY), ('TEXTCOLOR', (0, 0), (-1, 0), white),
          ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), ('LINEBELOW', (0, 0), (-1, 0), 1.1, GOLD)]
    for r in range(1, len(data)):
        if r % 2 == 0: st.append(('BACKGROUND', (0, r), (-1, r), ROWALT))
    if totals_row is not None:
        st += [('BACKGROUND', (0, totals_row), (-1, totals_row), LBLUE),
               ('FONTNAME', (0, totals_row), (-1, totals_row), 'Helvetica-Bold')]
    t.setStyle(TableStyle(st))
    return t

def hf(canvas, doc):
    canvas.saveState(); w, h = A4
    canvas.setFont('Helvetica', 7); canvas.setFillColor(TLIGHT)
    canvas.drawString(50, h - 30, 'Absolute Security Group x Heart of the City — LCF Pilot Data Summary')
    canvas.drawRightString(w - 50, h - 30, 'COMMERCIAL IN CONFIDENCE')
    canvas.drawCentredString(w / 2, 26, f'Page {doc.page}  ·  Prepared 20 July 2026 — compiled from daily patrol logs')
    canvas.restoreState()

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=50, rightMargin=50, topMargin=48, bottomMargin=44,
                      title='LCF Pilot — Accountability Data Summary', author='Absolute Security Group')
doc.addPageTemplates([PageTemplate(id='p', frames=[Frame(50, 44, A4[0] - 100, A4[1] - 92)], onPage=hf)])
el = []
el.append(Paragraph('Enhanced CBD Safety Team — LCF Pilot', styles['t']))
el.append(Paragraph('Accountability Data Summary  ·  2 June – 24 July 2026 (complete pilot period)', styles['st']))
el.append(HRFlowable(width='38%', thickness=1.4, color=GOLD, spaceBefore=6, spaceAfter=4, hAlign='CENTER'))
el.append(Paragraph('Data window 1 June – 24 July 2026 (54 days), including the 1 June mobilisation day; pilot commenced 2 June and concluded 24 July.', styles['n']))

# 1 totals
el.append(Paragraph('1.  Pilot Activity Totals — 54 days', styles['h']))
rows = [['Measure', 'Pilot total', 'Per week']]
for label, k in [('Calls / incidents attended', 'response_calls'), ('Named business welfare check-ins', 'store_checks_named'),
                 ('People moved on', 'move_ons'), ('Aggression / disorder de-escalated', 'aggression_incidents'),
                 ('Theft / shoplifting responses', 'thefts'), ('Welfare interventions (people)', 'welfare_person_checks'),
                 ('Police escalations', 'police_escalations'), ('Trespasses actioned', 'trespass_events'),
                 ('Arrests directly supported', 'arrests'), ('Auror evidence reports referenced', 'auror_mentions')]:
    rows.append([label, f'{T[k]:,}', f'{W[k]:.1f}'])
el.append(T_(rows, [245, 125, 125]))

# 2 weekly averages
el.append(Paragraph('2.  Weekly Averages — Pilot vs 2026 Months and Last Year', styles['h']))
rows = [['Metric (per week)', 'Feb 2026', 'Mar–May 26 (baseline)', 'PILOT Jun–Jul 26', 'Jun–Jul 25 (last year)', 'vs baseline', 'vs last year']]
FEB = {'calls': 41.8, 'police': 3.2, 'agg': 12.2}
for label, bk, pk, yk, fk in [
        ('Calls / incidents attended', 'calls', 'response_calls', 'calls', 'calls'),
        ('Police calls / escalations', 'police', 'police_escalations', 'police', 'police'),
        ('Aggressive behaviour', 'aggression', 'aggression_incidents', 'aggression', 'agg'),
        ('People moved on', 'move_ons', 'move_ons', None, None),
        ('Theft / shoplifting', 'theft', 'thefts', None, None),
        ('Arrests directly supported', 'arrests', 'arrests', None, None)]:
    b = BL[bk]; p = W[pk]; y = YY.get(yk) if yk else None; f = FEB.get(fk) if fk else None
    rows.append([label, f'{f:.1f}' if f else 'n/a', f'{b:.1f}', f'{p:.1f}', f'{y:.1f}' if y else 'n/a',
                 f'{(p / b - 1) * 100:+.0f}%', f'{(p / y - 1) * 100:+.0f}%' if y else 'n/a'])
el.append(T_(rows, [122, 52, 78, 72, 78, 47, 46]))
el.append(Paragraph('Feb 2026 and Jun–Jul 2025 reports used the older 5-metric format — move-ons, theft and arrests were not '
                    'captured then (n/a). Baseline = the ten clean Mon–Sun weeks, 9 Mar – 31 May 2026.', styles['n']))

# 3 week by week
el.append(Paragraph('3.  Pilot Week-by-Week', styles['h']))
wk = {}
for d in DAYS:
    iso = datetime.date.fromisoformat(d['date'])
    w0 = iso - datetime.timedelta(days=iso.weekday())
    g = wk.setdefault(w0, {'days': 0, 'c': 0, 'm': 0, 'a': 0, 't': 0, 'p': 0, 's': 0})
    g['days'] += 1; g['c'] += d['response_calls']; g['m'] += d['move_ons']
    g['a'] += d['aggression_incidents']; g['t'] += d['thefts']; g['p'] += d['police_escalations']
    g['s'] += d['store_checks_named']
rows = [['Week commencing', 'Days', 'Calls attended', 'Move-ons', 'Aggression', 'Thefts', 'Police', 'Store checks']]
for w0 in sorted(wk):
    g = wk[w0]
    rows.append([w0.strftime('%d %b') + (' *' if g['days'] < 7 else ''), g['days'], g['c'], g['m'], g['a'], g['t'], g['p'], f"{g['s']:,}"])
rows.append(['TOTAL', N, T['response_calls'], T['move_ons'], T['aggression_incidents'], T['thefts'],
             T['police_escalations'], f"{T['store_checks_named']:,}"])
el.append(T_(rows, [88, 40, 68, 54, 62, 48, 44, 64], totals_row=len(rows) - 1))
el.append(Paragraph('* Partial weeks: w/c 29 June spans June–July; the final week w/c 20 July covers five days '
                    '(Mon 20 – Fri 24), the pilot having concluded Friday 24 July.', styles['n']))

# 4 capacity
el.append(Paragraph('4.  Unattended Demand — Before vs During', styles['h']))
el.append(T_([['Period', 'Coverage model', 'Unattended / capacity-affected demand'],
              ['Jan – Apr 2026 (pre-uplift)', 'Single patrol team',
               '211 missed interventions — 29% of all calls; 51 instances with the team already committed to another call'],
              ['1 Jun – 24 Jul 2026 (full pilot period)', 'Core patrol + LCF uplift team (afternoons Sun–Thu; nights Fri–Sat)',
               'Three capacity-affected responses in 54 days (≈1%) — none in the two-team daytime window after week one']],
             [108, 138, 241]))

# 5 reading
el.append(Paragraph('5.  Reading the Numbers', styles['h']))
for txt in [
    '<b>Attended demand rose immediately and stayed up</b> — pilot weeks ran well above the 40.7/week baseline through the core of the deployment (peak 68/week); businesses call when a team reliably arrives.',
    f'<b>Fewer Police callouts, more arrests</b> — {W["police_escalations"]:.1f}/week vs {YY["police"]:.1f} in the same weeks last year ({(W["police_escalations"]/YY["police"]-1)*100:.0f}%): with two teams able to call each other, matters that once required Police were resolved between the teams. Arrests rose from 1.2 to {W["arrests"]:.1f}/week (+{(W["arrests"]/BL["arrests"]-1)*100:.0f}%), and roughly one Police engagement in three ended in an arrest vs one in four pre-uplift — Police attendance shifted to targeted enforcement.',
    '<b>Capacity effect:</b> missed demand collapsed from 29% of calls (Jan–Apr) to ≈1% during the pilot.',
    'Figures compiled from every daily patrol record for the period and reconciled with the HOTC Weekly Data Reports.']:
    p = ParagraphStyle('b', fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=TDARK,
                       leftIndent=16, bulletIndent=5, spaceAfter=4)
    el.append(Paragraph('<bullet>&bull;</bullet>' + txt, p))

doc.build(el)
print('SAVED:', OUT)
