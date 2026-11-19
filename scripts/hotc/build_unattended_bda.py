#!/usr/bin/env python3
"""Unattended demand / missed interventions — Before, During and After the pilot.
Edward Caughey's 9 Oct 2026 ask: the Pilot report's 'Capacity' section format, extended
before-during-after and plotted by month/quarter, as a standing quarterly section.
Outputs: chart PNG (_charts_quarterly/unattended_bda.png), note PDF (+ ~/Downloads copy),
reply-email draft DOCX. Honesty rules per memory/projects/asg/hotc-shift-reports.md."""
import os, re, shutil
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

HOTC = "/Users/ahmadduais/Desktop/ASG/HOTC/2026"
CH = os.path.join(HOTC, "_charts_quarterly")
PNG = os.path.join(CH, "unattended_bda.png")
PDF = os.path.join(HOTC, "HOTC_Unattended_Demand_Before_During_After.pdf")
DOCX = os.path.join(HOTC, "Reply to Edward - Missed Interventions (DRAFT).docx")
NAVY = '#1F3864'; GOLD = '#B8912F'; RED = '#B01E1E'; GREY = '#555555'

# ---------------------------------------------------------------- chart
plt.rcParams.update({'font.size': 10, 'axes.edgecolor': '#CCCCCC', 'axes.linewidth': 0.8})
fig, ax = plt.subplots(figsize=(11.2, 5.6))
# x layout: before-bar | dashed method divider | monthly bars Jun..Sep
bx = 0.0
months = ['Jun 26', 'Jul 26', 'Aug 26', 'Sep 26']
mx = [1.6, 2.6, 3.6, 4.6]
mv = [2, 1, 0, 1]
mnote = ['1 attended after a delay;\n1 unattended (6 Jun)', '1 queued minutes,\nattended (2 Jul)', '0 recorded',
         '1 delayed response\n(21 Sep) — attended']
ax.bar([bx], [211], width=0.95, color=RED, zorder=3)
ax.bar(mx, mv, width=0.62, color=GOLD, zorder=3)
# pilot window shading (pilot ran 1 Jun – 24 Jul; Jul bar is mostly in-pilot)
ax.axvspan(mx[0] - 0.45, mx[1] + 0.45, color=NAVY, alpha=0.07, zorder=0)
ax.text((mx[0] + mx[1]) / 2, 196, 'LCF pilot\n1 Jun – 24 Jul', ha='center', va='top',
        fontsize=8.5, color=NAVY, fontweight='bold')
ax.axvline(0.8, color='#999999', linestyle='--', linewidth=1)
# method labels — clear of the bars/labels (the old chart overlapped these)
ax.text(bx, 242, 'One-off dedicated\ncapacity analysis', ha='center', va='top',
        fontsize=8.5, color=RED, style='italic')
ax.text(3.1, 242, 'Counts recorded in the daily patrol logs (lighter-touch measure)',
        ha='center', va='top', fontsize=8.5, color=GREY, style='italic')
# value label inside the bar so it cannot collide with the method label above
ax.text(bx, 202, '211', ha='center', va='top', fontsize=16, color='white', fontweight='bold')
ax.text(bx, 186, 'unable to attend\n(≈29% of demand)', ha='center', va='top',
        fontsize=8.5, color='white', fontweight='bold')
for x, v, n in zip(mx, mv, mnote):
    ax.text(x, v + 4, str(v), ha='center', va='bottom', fontsize=11, color=NAVY, fontweight='bold')
    ax.text(x, v + 16, n, ha='center', va='bottom', fontsize=7.6, color=GREY)
ax.set_xticks([bx] + mx)
ax.set_xticklabels(['Before uplift\n(Jan–Apr 2026)'] + months, fontsize=9.5, color=NAVY,
                   fontweight='bold')
ax.set_ylabel('Capacity-affected responses (count)', fontsize=10, color='#333')
ax.set_ylim(0, 245); ax.set_xlim(-0.7, 5.3)
ax.grid(axis='y', color='#EAEAEA', linewidth=0.7, zorder=0)
ax.spines[['top', 'right']].set_visible(False)
ax.set_title('Capacity-Affected Demand — Before, During and After the Pilot',
             fontsize=13.5, color=NAVY, fontweight='bold', pad=12)
# no embedded footer caption — the PDF supplies its own caption under the image
fig.tight_layout()
fig.savefig(PNG, dpi=150)
plt.close(fig)
print("CHART:", PNG)

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

def _esc(s):
    return re.sub(r'&(?!amp;|rsquo;|lsquo;|rdquo;|ldquo;|rarr;|lt;|gt;|#|nbsp;|mdash;|ndash;)', '&amp;', str(s))

def tbl(rows, widths):
    data = [[Paragraph(_esc(c), _cH if ri == 0 else _cB) for c in row] for ri, row in enumerate(rows)]
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
    # pilot-report-style navy section bar with gold left accent (the format Edward referenced)
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
el.append(Paragraph('Unattended Demand — Before, During and After the Pilot',
                    S('t', textColor=colors.HexColor(NAVY), fontSize=19, leading=23,
                      fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=4)))
el.append(Paragraph('Standing section of the Quarterly Performance Report · Prepared October 2026 · CONFIDENTIAL',
                    S('st', textColor=colors.HexColor(GREY), fontSize=9.5, alignment=TA_CENTER, spaceAfter=14)))
el.append(Paragraph(
    'This restores the pilot report&rsquo;s capacity measure — <b>missed interventions</b>: business calls the '
    'Safety Team could not attend, or could only attend after a queue or delay, because it was already committed '
    'to another incident — and extends it before, during and after the pilot, plotted by month. It will appear '
    'in this format in every quarterly report from October–December 2026 onward.', BODY))
el.append(Spacer(1, 4))
el.append(secbar('Capacity — Unattended Demand: Before, During and After'))
el.append(Spacer(1, 6))
el.append(tbl([
    ['Period', 'Coverage model', 'Unattended / capacity-affected demand'],
    ['Jan – Apr 2026 (pre-uplift)', 'Single patrol team',
     '211 missed interventions — 29% of all calls; 51 instances with the team already committed to another call; '
     '20 simultaneous-incident clashes  (one-off dedicated ASG analysis)'],
    ['1 Jun – 24 Jul 2026 (full pilot)', 'Core patrol + LCF uplift team (afternoons Sun–Thu; nights Fri–Sat)',
     'Three capacity-affected responses across 54 days (~1% of demand) — all in the first week or on single-team '
     'night cover; one of the three went unattended'],
    ['25 Jul – 30 Sep 2026 (after pilot)', 'Core patrol model (single team on shift)',
     'Zero unattended recorded — every business call that reached the team was attended '
     '(607 across Jul–Sep); one delayed response recorded (21 Sep)'],
], [34 * mm, 48 * mm, 96 * mm]))
el.append(Spacer(1, 8))
el.append(Paragraph('The instances behind the in-log counts', H3))
el.append(bullets([
    '<b>1 June</b> — a cafe caller was queued behind another incident on the morning the uplift was still mobilising; responded to after a delay.',
    '<b>6 June</b> — one cafe call could not be attended while guards managed an active four-person altercation (the only outright miss recorded since the uplift began).',
    '<b>2 July, 01:34</b> — the night team took two near-simultaneous calls and attended them back-to-back; the second caller waited minutes, and both were resolved.',
    '<b>21 September</b> — a second caller (an aggressive male in a hotel lobby) was advised of a short delay while the team was committed to the McDonald&rsquo;s Britomart incident; attended and resolved. The only capacity-affected response recorded after the pilot.',
]))
el.append(PageBreak())
el.append(KeepTogether([Image(PNG, width=178 * mm, height=178 * mm * 5.6 / 11.2),
                        Paragraph('Capacity-affected responses by period. The pre-uplift figure comes from a dedicated '
                                  'one-off analysis of the Jan–Apr call record; the monthly figures are counts recorded in the '
                                  'daily patrol logs — a lighter-touch measure — so the two sides of the dashed line are not '
                                  'like-for-like and no recommendation rests on the comparison.', CAP)]))
el.append(Paragraph('Did unattended demand rise once the pilot resource ended?', H2))
el.append(Paragraph(
    'A reasonable expectation — the uplift team stood down on 24 July and cover returned to the core model. '
    'Three things are true at once:', BODY))
el.append(bullets([
    '<b>The logs show no return of outright misses.</b> From 25 July to 30 September, zero unattended business calls '
    'were recorded; the one capacity-affected response was the 21 September delay. All 607 business calls across the '
    'quarter were attended.',
    '<b>But the recorded figures are the visible minimum, not proof of zero.</b> The pre-uplift 211 came from a dedicated '
    'analysis that went looking for misses; day-to-day, a miss or delay only enters the record if a guard notes it, and '
    'response times are not yet captured. A late response that nobody logged would not appear above.',
    '<b>What has visibly risen is pressure, concentrated into September.</b> Total response demand grew 280 &rarr; 301 &rarr; 380 '
    'across the quarter (+36%); September ran high-load (10+ response calls) on 21 of its 30 days; the team absorbed '
    'concurrent calls by splitting (9 Jul, 28 Jul, 26 Sep) and sequencing (seven calls across ~3 hours on 29 Sep). '
    'Concurrency is currently being absorbed rather than surfacing as misses — and the structural no-backup gap on '
    'single-team night cover, where the pilot capacity used to sit, remains.',
]))
el.append(Paragraph(
    'So the honest reading is: the record does not show unattended demand returning, but the measurement is not yet '
    'strong enough to rule it out — and the pressure trend says the question will keep getting harder.', BODY))
el.append(Paragraph('Making this a reliable trend from next quarter', H2))
el.append(Paragraph(
    'From the October–December 2026 quarter the daily patrol log gains two formal fields: an <b>unable-to-attend / '
    'delayed</b> line recorded at the time for every call the team cannot reach immediately, and a <b>response-time</b> '
    'field (call received &rarr; team on scene). That makes this section a true like-for-like trend going forward — '
    'and will show directly whether capacity-affected demand grows as overall demand does.', BODY))
el.append(Spacer(1, 4))
el.append(KeepTogether([Paragraph('Demand pressure by month (context)', H3), tbl([
    ['Measure', 'Jul', 'Aug', 'Sep', 'Quarter'],
    ['Business calls', '191', '193', '223', '607'],
    ['All response calls &amp; requests logged', '280', '301', '380', '961'],
    ['High-load days (10+ response calls)', '14', '13', '21', '48'],
    ['Avg response calls per day', '9.0', '9.7', '12.7', '10.4'],
], [86 * mm, 22 * mm, 22 * mm, 22 * mm, 26 * mm])]))
el.append(Spacer(1, 10))
el.append(Paragraph('Note on the data', H3))
for c in [
    'The pre-pilot figure (211 / 29%) is a one-off dedicated analysis used only to frame the scale of the problem before '
    'the uplift; it is not like-for-like with the log-based counts and no recommendation rests on it.',
    '&ldquo;Capacity-affected&rdquo; covers unable-to-attend, queued and delayed responses. Of the four in-log instances since '
    '1 June, one went unattended (6 Jun); three were attended after a delay (1 Jun, 2 Jul, 21 Sep).',
    'The &ldquo;attended everything&rdquo; finding applies to the 607 business calls; the pressure measures use the broader '
    '961 logged requests (business plus Police, Council, public and other callers) — the two bases differ.',
    'These figures record whether a call was attended, not how quickly — response times are not yet captured, so the '
    'recorded delays are the visible minimum.',
]:
    el.append(Paragraph('• ' + c, NOTE))

def deco(cv, doc):
    cv.saveState(); cv.setFont('Helvetica', 7.5); cv.setFillColor(colors.HexColor(GREY))
    cv.drawString(16 * mm, A4[1] - 10 * mm, 'Absolute Security Group  ·  Heart of the City')
    cv.drawRightString(A4[0] - 16 * mm, A4[1] - 10 * mm, 'CONFIDENTIAL')
    cv.setStrokeColor(colors.HexColor('#EDF0F7'))
    cv.line(16 * mm, A4[1] - 12 * mm, A4[0] - 16 * mm, A4[1] - 12 * mm)
    cv.drawCentredString(A4[0] / 2, 8 * mm, f'Page {doc.page}  ·  Unattended Demand — Before, During and After')
    cv.restoreState()

doc = SimpleDocTemplate(PDF, pagesize=A4, topMargin=18 * mm, bottomMargin=14 * mm,
                        leftMargin=16 * mm, rightMargin=16 * mm)
doc.build(el, onFirstPage=deco, onLaterPages=deco)
shutil.copy2(PDF, os.path.expanduser('~/Downloads/' + os.path.basename(PDF)))
print("PDF:", PDF)

# ---------------------------------------------------------------- email draft
from docx import Document
from docx.shared import Pt, RGBColor
d = Document()
st = d.styles['Normal']; st.font.name = 'Calibri'; st.font.size = Pt(11)
p = d.add_paragraph(); r = p.add_run('DRAFT  ·  Attach: HOTC_Unattended_Demand_Before_During_After.pdf')
r.bold = True; r.font.color.rgb = RGBColor(0xB0, 0x1E, 0x1E)
p = d.add_paragraph(); r = p.add_run('Subject:  RE: A few more questions re quarterly'); r.bold = True
for para in [
    'Hi Edward,',
    'We’ve made a slight change to our response strategy: guards are now dispatched individually when the team is '
    'tied up awaiting Police attendance for an arrest, or when simultaneous calls come in. This has been made '
    'possible by a recent hire — AJ, our CBD-focused Operations Manager — and for high-risk situations he and/or '
    'Hasi attend the call with the team.',
    'The main reason for the change is to make sure we don’t see that high number of unattended calls again.',
    'Please see the report below.',
    'Cheers,',
    'Ahmad',
]:
    d.add_paragraph(para)
d.save(DOCX)
print("DOCX:", DOCX)

# ---------------------------------------------------------------- one-page summary
PDF1 = os.path.join(HOTC, "HOTC_Unattended_Demand_OnePager.pdf")
BODY_S = S('bodyS', fontSize=9.3, leading=13, spaceAfter=5, alignment=TA_JUSTIFY)
BUL_S = S('bulS', fontSize=9.0, leading=12.5, spaceAfter=2.5)
one = []
one.append(Paragraph('ABSOLUTE SECURITY GROUP',
                     S('m1', textColor=colors.HexColor(GOLD), fontSize=9.5, alignment=TA_CENTER,
                       spaceAfter=4, fontName='Helvetica-Bold')))
one.append(Paragraph('Unattended Demand — Before, During and After the Pilot',
                     S('t1', textColor=colors.HexColor(NAVY), fontSize=16, leading=19,
                       fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=2)))
one.append(Paragraph('One-page summary · Heart of the City · Prepared October 2026 · CONFIDENTIAL',
                     S('s1', textColor=colors.HexColor(GREY), fontSize=8.5, alignment=TA_CENTER, spaceAfter=8)))
one.append(Paragraph(
    '<b>Missed interventions</b> — business calls the Safety Team could not attend, or attended only after a queue '
    'or delay, because it was already committed — tracked before, during and after the LCF pilot. A standing section '
    'of every quarterly report from Oct–Dec 2026.', BODY_S))
one.append(tbl([
    ['Period', 'Coverage model', 'Unattended / capacity-affected demand'],
    ['Jan – Apr 2026 (pre-uplift)', 'Single patrol team',
     '211 missed interventions — 29% of all calls; 51 instances team already committed; '
     '20 simultaneous-incident clashes  (one-off dedicated ASG analysis)'],
    ['1 Jun – 24 Jul 2026 (full pilot)', 'Core patrol + LCF uplift team',
     'Three capacity-affected responses in 54 days (~1% of demand); one outright miss (6 Jun)'],
    ['25 Jul – 30 Sep 2026 (after pilot)', 'Core patrol model (single team)',
     'Zero unattended recorded — all 607 business calls attended; one delayed response (21 Sep)'],
], [36 * mm, 44 * mm, 98 * mm]))
one.append(Spacer(1, 6))
one.append(Image(PNG, width=174 * mm, height=174 * mm * 5.6 / 11.2))

def deco1(cv, doc):
    cv.saveState(); cv.setFont('Helvetica', 7.5); cv.setFillColor(colors.HexColor(GREY))
    cv.drawString(16 * mm, A4[1] - 10 * mm, 'Absolute Security Group  ·  Heart of the City')
    cv.drawRightString(A4[0] - 16 * mm, A4[1] - 10 * mm, 'CONFIDENTIAL')
    cv.setStrokeColor(colors.HexColor('#EDF0F7'))
    cv.line(16 * mm, A4[1] - 12 * mm, A4[0] - 16 * mm, A4[1] - 12 * mm)
    cv.restoreState()

doc1 = SimpleDocTemplate(PDF1, pagesize=A4, topMargin=16 * mm, bottomMargin=11 * mm,
                         leftMargin=16 * mm, rightMargin=16 * mm)
doc1.build(one, onFirstPage=deco1, onLaterPages=deco1)
shutil.copy2(PDF1, os.path.expanduser('~/Downloads/' + os.path.basename(PDF1)))
print("ONEPAGER:", PDF1)
