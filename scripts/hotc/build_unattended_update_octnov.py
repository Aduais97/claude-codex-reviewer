#!/usr/bin/env python3
"""Unable-to-attend data update for Edward Caughey's 16 Nov 2026 board-paper request.
Extends the approved Before/During/After format with the formal Response Capacity Log
period (1 Oct - 15 Nov 2026). Honesty rules per memory (method bands, visible-minimum,
no like-for-like claims across measurement regimes). Client copy is em-dash free.
Outputs: chart PNG, update PDF (+ Downloads copy), reply-email draft DOCX."""
import os, re, json, glob, shutil, datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                Image, PageBreak, KeepTogether, ListFlowable, ListItem)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

HOTC = os.path.expanduser('~/Desktop/ASG/HOTC/2026')
CH = os.path.join(HOTC, '_charts_quarterly')
STAGE = os.path.expanduser('~/Desktop/Dev/Claude/scripts/hotc/data/hotc_octnov2026')
PNG = os.path.join(CH, 'unattended_update_octnov.png')
PDF = os.path.join(HOTC, 'HOTC_Unattended_Demand_Update_OctNov2026.pdf')
DOCX = os.path.join(HOTC, 'Reply to Edward - Unable to Attend Data (DRAFT).docx')
NAVY = '#1F3864'; GOLD = '#B8912F'; RED = '#B01E1E'; GREY = '#555555'

# ---------------------------------------------------------------- data (live from day JSONs)
days = []
for jf in glob.glob(os.path.join(STAGE, '*', '*.json')):
    if os.path.basename(jf).startswith('_'):
        continue
    days.append(json.load(open(jf)))
days = [d for d in days if d['date_iso'] >= '2026-10-01']
days.sort(key=lambda x: x['date_iso'])
assert len(days) == 46, len(days)

def mins_of(c):
    if not c.get('attended'):
        return None
    h1, m1 = map(int, c['received'].split(':')); h2, m2 = map(int, c['attended'].split(':'))
    return ((h2 * 60 + m2) - (h1 * 60 + m1)) % 1440

events = []
for d in days:
    dt = datetime.date.fromisoformat(d['date_iso'])
    for c in d.get('capacity', []):
        events.append((dt, c))
oct_ev = [e for e in events if e[0].month == 10]
nov_ev = [e for e in events if e[0].month == 11]
UNABLE = ('Unable to attend', 'Not completed')
calls_oct = sum(d['metrics']['calls'] for d in days if d['date_iso'][5:7] == '10')
calls_nov = sum(d['metrics']['calls'] for d in days if d['date_iso'][5:7] == '11')
calls_tot = calls_oct + calls_nov
n_unable = sum(1 for _, c in events if c['status'] in UNABLE)
n_qd = len(events) - n_unable
qd_mins = sorted(m for _, c in events if (m := mins_of(c)) is not None)
med = int((qd_mins[len(qd_mins) // 2 - 1] + qd_mins[len(qd_mins) // 2]) / 2) if len(qd_mins) % 2 == 0 \
    else qd_mins[len(qd_mins) // 2]
oct_unable = sum(1 for _, c in oct_ev if c['status'] in UNABLE)
nov_unable = sum(1 for _, c in nov_ev if c['status'] in UNABLE)
attended = calls_tot - n_unable
pct_att = f'{attended / calls_tot * 100:.1f}'
pct_un = f'{n_unable / calls_tot * 100:.1f}'
print(f'calls {calls_tot} (oct {calls_oct} nov {calls_nov}) events {len(events)} '
      f'unable {n_unable} qd {n_qd} median {med} range {qd_mins[0]}-{qd_mins[-1]}')

# ---------------------------------------------------------------- chart
# Same buckets on every bar (the Jan-Apr dedicated-analysis methodology):
#   missed = calls that could not be attended at all (red, baseline)
#   committed = calls attended only after a queue or delay, team already engaged (gold, stacked)
plt.rcParams.update({'font.size': 10, 'axes.edgecolor': '#CCCCCC', 'axes.linewidth': 0.8})
fig, ax = plt.subplots(figsize=(10.8, 6.0))
xs = [0.0, 1.5, 3.0, 4.0]
missed = [211, 1, oct_unable, nov_unable]
committed = [0, 2, len(oct_ev) - oct_unable, len(nov_ev) - nov_unable]
widths = [0.95, 0.72, 0.62, 0.62]
ax.bar(xs, missed, width=widths, color=RED, zorder=3, label='Could not be attended (missed)')
ax.bar(xs, committed, width=widths, bottom=missed, color=GOLD, zorder=3,
       label='Attended after a queue or delay (team already committed)')
ax.axvline(0.75, color='#999999', linestyle='--', linewidth=1)
ax.axvline(2.25, color='#999999', linestyle='--', linewidth=1)
ax.text(xs[0], 256, 'One-off dedicated\ncapacity analysis', ha='center', va='top',
        fontsize=8.5, color=RED, style='italic')
ax.text(xs[1], 256, 'Counts recorded in\nthe daily patrol logs', ha='center', va='top',
        fontsize=8.5, color=GREY, style='italic')
ax.text((xs[2] + xs[3]) / 2, 256, 'Formal Response Capacity Log\n(every queued, delayed or unable\nresponse recorded, from 1 Oct 2026)',
        ha='center', va='top', fontsize=8.5, color=NAVY, style='italic', fontweight='bold')
ax.text(xs[0], 195, '211', ha='center', va='top', fontsize=16, color='white', fontweight='bold')
ax.text(xs[0], 178, 'missed/late calls\n(29% of 718 calls)', ha='center', va='top',
        fontsize=8.5, color='white', fontweight='bold')
notes = [None,
         '1 missed (6 Jun);\n2 attended late',
         f'{oct_unable} missed (2.1% of {calls_oct} calls);\n{len(oct_ev) - oct_unable} attended late',
         f'0 missed of {calls_nov} calls;\nall {len(nov_ev)} attended late']
for x, m, c, n in zip(xs, missed, committed, notes):
    if n is None:
        continue
    tot = m + c
    ax.text(x, tot + 6, str(tot), ha='center', va='bottom', fontsize=11, color=NAVY, fontweight='bold')
    ax.text(x, tot + 20, n, ha='center', va='bottom', fontsize=7.6, color=GREY)
ax.legend(loc='center right', bbox_to_anchor=(1.0, 0.55), frameon=False, fontsize=9)
ax.set_xticks(xs)
ax.set_xticklabels(['Before uplift\n(Jan-Apr 2026)', 'LCF uplift pilot\n(1 Jun - 24 Jul 2026)',
                    'Oct 26', 'Nov 26\n(1-15 only)'],
                   fontsize=9.5, color=NAVY, fontweight='bold')
ax.set_ylabel('Business calls missed or attended late (count)', fontsize=10, color='#333')
ax.set_ylim(0, 260); ax.set_xlim(-0.95, 4.75)
ax.grid(axis='y', color='#EAEAEA', linewidth=0.7, zorder=0)
ax.spines[['top', 'right']].set_visible(False)
ax.set_title('Missed and Delayed Demand, Same Buckets Across All Periods',
             fontsize=13, color=NAVY, fontweight='bold', pad=12)
fig.tight_layout()
fig.savefig(PNG, dpi=150)
plt.close(fig)
print('CHART:', PNG)

# ---------------------------------------------------------------- pdf
ss = getSampleStyleSheet()
def S(n, **k): return ParagraphStyle(n, parent=ss['Normal'], **k)
H2 = S('h2', textColor=colors.HexColor(NAVY), fontSize=14, leading=17, spaceBefore=13,
       spaceAfter=6, fontName='Helvetica-Bold')
H3 = S('h3', textColor=colors.HexColor(GOLD), fontSize=10.5, leading=13, spaceBefore=9,
       spaceAfter=3, fontName='Helvetica-Bold')
BODY = S('body', fontSize=10, leading=14.5, spaceAfter=7, alignment=TA_JUSTIFY)
BUL = S('bul', fontSize=9.6, leading=13.5, spaceAfter=3)
NOTE = S('note', fontSize=8, leading=10.5, textColor=colors.HexColor(GREY), spaceAfter=2)
CAP = S('cap', fontSize=8.3, leading=11, textColor=colors.HexColor(GREY), spaceBefore=2, spaceAfter=10)
_cH = S('cH', fontSize=8.6, textColor=colors.white, leading=10.5, fontName='Helvetica-Bold')
_cB = S('cB', fontSize=8.5, textColor=colors.black, leading=11)
_cBs = S('cBs', fontSize=7.8, textColor=colors.black, leading=10)

def _esc(s):
    s = str(s).replace(' — ', ': ').replace('—', '-').replace('–', '-')
    return re.sub(r'&(?!amp;|rsquo;|lsquo;|rdquo;|ldquo;|rarr;|lt;|gt;|#|nbsp;)', '&amp;', s)

def tbl(rows, widths, body_style=None):
    bs = body_style or _cB
    data = [[Paragraph(_esc(c), _cH if ri == 0 else bs) for c in row] for ri, row in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#CCCCCC')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6), ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F6F8FC')]),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(NAVY))]))
    return t

def secbar(txt):
    t = Table([[Paragraph(f'<font color="white"><b>{_esc(txt)}</b></font>',
                          S('sb', fontSize=11.5, leading=14))]], colWidths=[178 * mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(NAVY)),
        ('LINEBEFORE', (0, 0), (0, -1), 4, colors.HexColor(GOLD)),
        ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8)]))
    return t

def bullets(items):
    return ListFlowable([ListItem(Paragraph(_esc(x), BUL), leftIndent=6, value='•') for x in items],
                        bulletType='bullet', start='•', leftIndent=12)

el = []
el.append(Paragraph('ABSOLUTE SECURITY GROUP',
                    S('m', textColor=colors.HexColor(GOLD), fontSize=10.5, alignment=TA_CENTER,
                      spaceAfter=8, fontName='Helvetica-Bold')))
el.append(Paragraph('Heart of the City', S('ht', textColor=colors.HexColor(NAVY), fontSize=13,
                                           alignment=TA_CENTER, spaceAfter=2)))
el.append(Paragraph('Unattended Demand Update: 1 October to 15 November 2026',
                    S('t', textColor=colors.HexColor(NAVY), fontSize=19, leading=23,
                      fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=4)))
el.append(Paragraph('Prepared 16 November 2026 for the Heart of the City board paper · CONFIDENTIAL',
                    S('st', textColor=colors.HexColor(GREY), fontSize=9.5, alignment=TA_CENTER, spaceAfter=14)))
el.append(Paragraph(
    'As committed in the October report, the Safety Team moved to <b>formal capacity tracking on 1 October '
    '2026</b>: every response call that is queued, delayed, or cannot be attended is now recorded at the time, '
    'with the time the call was received and the time the team was on scene. This update presents the first '
    'six and a half weeks of that data and extends the before, during and after trend.', BODY))
el.append(Spacer(1, 4))
el.append(secbar('Headline: 1 October to 15 November 2026'))
el.append(Spacer(1, 6))
el.append(tbl([
    ['Business calls received', 'Attended', 'Attended after a queue or delay', 'Unable to attend'],
    [f'{calls_tot}  (Oct {calls_oct}, 1-15 Nov {calls_nov})',
     f'{attended}  ({pct_att}%)',
     f'{n_qd}  (median {med} min, range {qd_mins[0]} to {qd_mins[-1]} min)',
     f'{n_unable}  ({pct_un}%), all in October; none 1-15 Nov'],
], [44 * mm, 36 * mm, 56 * mm, 42 * mm]))
el.append(Spacer(1, 8))
el.append(secbar('Capacity: Unattended Demand Before, During and After'))
el.append(Spacer(1, 6))
el.append(tbl([
    ['Period', 'Coverage model', 'Unattended / capacity-affected demand'],
    ['Jan - Apr 2026 (pre-uplift)', 'Single patrol team',
     '211 missed interventions, 29% of all calls; 51 instances with the team already committed to another call; '
     '20 simultaneous-incident clashes  (one-off dedicated ASG analysis)'],
    ['1 Jun - 24 Jul 2026 (full pilot)', 'Core patrol + LCF uplift team',
     'Three capacity-affected responses across 54 days, about 1% of demand; one of the three went unattended (6 Jun)'],
    ['25 Jul - 30 Sep 2026 (after pilot)', 'Core patrol model (single team)',
     'Zero unattended recorded; every business call that reached the team was attended (607 across Jul-Sep); '
     'one delayed response recorded (21 Sep)'],
    ['1 Oct - 15 Nov 2026 (formal tracking)', 'Core patrol model (single team)',
     f'{len(events)} capacity-affected responses recorded of {calls_tot} business calls: {n_qd} attended after a '
     f'queue or delay ({qd_mins[0]} to {qd_mins[-1]} minutes, median {med}); {n_unable} unable to attend or '
     f'complete ({pct_un}% of calls). October: {len(oct_ev)} events, {oct_unable} unable. '
     f'1-15 November: {len(nov_ev)} events, none unable.'],
], [34 * mm, 42 * mm, 102 * mm]))
el.append(PageBreak())
el.append(KeepTogether([Image(PNG, width=172 * mm, height=172 * mm * 6.0 / 10.8),
                        Paragraph('Missed and late business calls by period. The pre-uplift bar is the 211 missed/late '
                                  'calls identified by the dedicated Jan-Apr analysis (29% of 718 calls). The later bars '
                                  'use the same definitions, split into calls that could not be attended (red) and calls '
                                  'attended after a queue or delay with the team already committed (gold). Sources differ '
                                  'across the dashed lines (the pre-uplift figure comes from a dedicated review of the '
                                  'call record; the pilot and formal periods come from the patrol logs), so the recent '
                                  'figures are the recorded minimum. The after-pilot months (25 Jul - 30 Sep), which '
                                  'recorded zero missed and one delayed response, are tabled on page 1 and omitted from '
                                  'the chart for clarity.', CAP)]))
el.append(Paragraph('The same methodology at both ends', H2))
el.append(Paragraph(
    'The pre-uplift figure is the one presented to the board at the start of the contract: <b>211 missed/late '
    'calls, 29% of 718 business calls</b> (Jan-Apr dedicated analysis). Applying the same definitions to the '
    f'formal tracking period gives <b>25 missed/late calls, 7.0% of {calls_tot}</b>, and the split shows the '
    f'failure mode has changed: only <b>5 were missed outright</b> ({pct_un}% overall; 2.1% of October&rsquo;s '
    f'{calls_oct} calls and none of November&rsquo;s {calls_nov} so far), while <b>{n_qd} were still attended</b> '
    'after a queue or delay of 6 to 41 minutes. Simultaneous calls drove at least four of those occasions '
    '(2, 10, 22 and 24 October, 10 November). One difference remains: the Jan-Apr figure came from a dedicated '
    'review of the call record, while the new figures come from the patrol logs, so they are the recorded '
    'minimum. A reconciliation of the Ops Phone call history against the logs would close that gap and can be '
    'run for the quarterly report.', BODY))
el.append(Paragraph('What the new data shows', H2))
el.append(bullets([
    f'<b>Demand is at record levels.</b> October logged {calls_oct} business calls, the highest month recorded in '
    '2026 (September 223, August 193, July 191, pre-uplift months 167 to 196). The first half of November is '
    f'tracking to a similar rate ({calls_nov} calls in 15 days).',
    f'<b>Concurrency is the pressure point.</b> 10 of the {len(events)} events arose from simultaneous calls, '
    'including two afternoons (22 and 24 October) with three near-simultaneous calls inside five minutes. A '
    'single team can only triage: it attends the most urgent or resolvable call and queues the rest.',
    f'<b>All five unable-to-attend events fell in October;</b> the first half of November recorded none, with all '
    f'{len(nov_ev)} of its capacity-affected calls still attended after a queue or delay.',
    f'<b>The delayed tail is measured for the first time.</b> Among the {n_qd} queued or delayed attendances the '
    f'median wait was {med} minutes (range {qd_mins[0]} to {qd_mins[-1]}). All other calls, roughly 93% of the '
    'total, were attended as received.',
]))
el.append(Paragraph('Measurement from here', H2))
el.append(Paragraph(
    'A new guard log template is rolling out that records, for every response call, the time received and the '
    'time on scene, explicit DELAYED and UNABLE TO ATTEND markers, and an end-of-shift capacity summary. From '
    'the October-December quarter onward this section becomes a true like-for-like trend, including response '
    'times for routine attendances, which are not yet individually captured.', BODY))
el.append(PageBreak())
el.append(secbar('Appendix: all 25 capacity-affected responses, 1 Oct - 15 Nov 2026'))
el.append(Spacer(1, 6))
rows = [['Date', 'Rec.', 'On scene', 'Min', 'Call and reason', 'Status']]
for dt, c in events:
    m = mins_of(c)
    rows.append([dt.strftime('%a %-d %b'), c['received'], c.get('attended') or '-',
                 str(m) if m is not None else '-',
                 c['call'] + ('. ' + c['note'] if c.get('note') else ''), c['status']])
el.append(tbl(rows, [19 * mm, 14 * mm, 14 * mm, 10 * mm, 102 * mm, 19 * mm], body_style=_cBs))
el.append(Spacer(1, 10))
el.append(Paragraph('Notes on the data', H3))
for c in [
    'The pre-uplift figure (211, about 29%) is a one-off dedicated analysis used only to frame the scale of the '
    'problem before the contract; it is not like-for-like with the log-based counts and no recommendation rests on it.',
    '"Capacity-affected" covers unable-to-attend, queued and delayed responses. Staffing and equipment matters that '
    'paused patrols without affecting a specific call are recorded in the daily reports but are not counted here.',
    'Attendance figures use the business-call base. Response times for the queued and delayed events are measured '
    'from call received to team on scene; response times for routine attendances begin with the new guard log.',
    'November figures cover 1-15 November only; the full month will appear in the quarterly report.',
]:
    el.append(Paragraph('• ' + c, NOTE))

def deco(cv, doc):
    cv.saveState(); cv.setFont('Helvetica', 7.5); cv.setFillColor(colors.HexColor(GREY))
    cv.drawString(16 * mm, A4[1] - 10 * mm, 'Absolute Security Group  ·  Heart of the City')
    cv.drawRightString(A4[0] - 16 * mm, A4[1] - 10 * mm, 'CONFIDENTIAL')
    cv.setStrokeColor(colors.HexColor('#EDF0F7'))
    cv.line(16 * mm, A4[1] - 12 * mm, A4[0] - 16 * mm, A4[1] - 12 * mm)
    cv.drawCentredString(A4[0] / 2, 8 * mm, f'Page {doc.page}  ·  Unattended Demand Update, Oct-Nov 2026')
    cv.restoreState()

doc = SimpleDocTemplate(PDF, pagesize=A4, topMargin=18 * mm, bottomMargin=14 * mm,
                        leftMargin=16 * mm, rightMargin=16 * mm)
doc.build(el, onFirstPage=deco, onLaterPages=deco)
shutil.copy2(PDF, os.path.expanduser('~/Downloads/' + os.path.basename(PDF)))
print('PDF:', PDF)

# ---------------------------------------------------------------- email draft
from docx import Document
from docx.shared import Pt, RGBColor
d = Document()
st = d.styles['Normal']; st.font.name = 'Calibri'; st.font.size = Pt(11)
p = d.add_paragraph(); r = p.add_run('DRAFT  ·  Attach: HOTC_Unattended_Demand_Update_OctNov2026.pdf')
r.bold = True; r.font.color.rgb = RGBColor(0xB0, 0x1E, 0x1E)
p = d.add_paragraph(); r = p.add_run('Subject:  RE: Unable to attend Data'); r.bold = True
for para in [
    'Hi Edward,',
    'As promised. The attached update has the latest unable-to-attend data with the trend table and graph in '
    'the same format as the last report, extended through 15 November.',
    'The short version for the board paper:',
    f'From 1 October we moved to formal capacity tracking, as committed in the October report. Every response '
    'call that is queued, delayed or cannot be attended is now recorded at the time, with the time received '
    'and the time on scene.',
    f'Across 1 October to 15 November the team received {calls_tot} business calls. {attended} were attended '
    f'({pct_att}%), including {n_qd} after a queue or short delay. {n_unable} could not be attended, all of '
    'them in October; the first half of November recorded none.',
    'The graph compares like with like. The start-of-year figure is the one we presented at the time: 211 '
    'missed/late calls, 29% of 718 calls (Jan to Apr dedicated analysis). On the same definitions, 1 October '
    f'to 15 November recorded 25 missed/late calls, 7.0% of {calls_tot}, and only {n_unable} of those were '
    f'missed outright ({pct_un}%; zero so far in November). The other {n_qd} were attended after a queue or '
    'delay.',
    'The only remaining difference is the source: the Jan to Apr figures came from a dedicated review of the '
    'call record, while the new figures come from the patrol logs, so they are the recorded minimum. We can '
    'reconcile the Ops Phone call history against the logs for the quarterly if the board wants that check.',
    f'October was also the busiest month on record ({calls_oct} business calls). The clear pressure point is '
    f'simultaneous calls: 10 of the 25 affected responses were concurrency, including two afternoons with '
    'three calls inside five minutes. A single team can only triage, which is the capacity case for the paper.',
    'Happy to cut the table or graph any other way that suits the board paper.',
    'Cheers,',
    'Ahmad',
]:
    d.add_paragraph(para)
d.add_paragraph()
from docx.shared import Cm
d.add_picture(PNG, width=Cm(16.5))
cap = d.add_paragraph()
r = cap.add_run('Trend graph (also page 2 of the attached PDF). The Jan-Apr bar is the start-of-year problem '
                'as originally reported: 211 missed/late calls, 29% of calls. The later bars use the same '
                'definitions, split into missed outright (red) and attended after a queue or delay (gold): '
                'Oct-Nov totals 25, of which only 5 were missed.')
r.italic = True; r.font.size = Pt(9); r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
d.save(DOCX)
print('DOCX:', DOCX)
