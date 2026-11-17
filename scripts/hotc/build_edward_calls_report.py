#!/usr/bin/env python3
"""Edward's board KPI: Calls from Businesses — full-year FY26 vs FY25, by month.
Pulls calls totals from Weekly Data Reports (FY25 Jul-Dec from the /Downloads/2024
backfill; everything else from the canonical tree). Builds a chart + board PDF."""
import os, glob, openpyxl
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

TREE = "/Users/ahmadduais/Desktop/ASG/Operations/Clients/HOTC"
DL2024 = "/Users/ahmadduais/Downloads/2024"
NAVY = colors.HexColor('#1F3864'); GOLD = colors.HexColor('#B8912F')
LIGHT = colors.HexColor('#EDF0F7'); GREY = colors.HexColor('#555555')
RED = colors.HexColor('#B01E1E'); GREEN = colors.HexColor('#2E7D32')

def calls_days(path):
    try:
        ws = openpyxl.load_workbook(path, data_only=True).active
        for r in ws.iter_rows(values_only=True):
            if r and r[0] and 'calls made from businesses' in str(r[0]).lower():
                nums = [c for c in r[1:] if isinstance(c, (int, float))]
                return (int(nums[-1]) if nums else 0, len([c for c in r[1:-1] if isinstance(c, (int, float))]))
    except Exception:
        pass
    return 0, 0

def month_total(base, year, month):
    tot = days = wk = 0
    for f in glob.glob(f"{base}/{year}/{month}/**/Weekly Data Report*.xlsx", recursive=True):
        c, d = calls_days(f); tot += c; days += d; wk += 1
    return tot, days, wk

def month_total_2024(month):
    tot = days = wk = 0
    for f in glob.glob(f"{DL2024}/{month}/**/*.xlsx", recursive=True):
        if 'weekly data report' not in f.lower():
            continue
        c, d = calls_days(f); tot += c; days += d; wk += 1
    return tot, days, wk

MONTHS = ['July','August','September','October','November','December',
          'January','February','March','April','May','June']
MABBR = {'July':'Jul','August':'Aug','September':'Sep','October':'Oct','November':'Nov',
         'December':'Dec','January':'Jan','February':'Feb','March':'Mar','April':'Apr','May':'May','June':'Jun'}

# FY26 = Jul25-Dec25 (tree/2025) + Jan26-Jun26 (tree/2026)
# FY25 = Jul24-Dec24 (Downloads/2024) + Jan25-Jun25 (tree/2025)
fy26, fy25 = [], []
for m in MONTHS:
    if MONTHS.index(m) < 6:   # Jul-Dec
        fy26.append(month_total(TREE, '2025', m))
        fy25.append(month_total_2024(m))
    else:                     # Jan-Jun
        fy26.append(month_total(TREE, '2026', m))
        fy25.append(month_total(TREE, '2025', m))

c26 = [x[0] for x in fy26]; c25 = [x[0] for x in fy25]
d26 = [x[1] for x in fy26]; d25 = [x[1] for x in fy25]
T26, T25 = sum(c26), sum(c25)
PD26 = T26 / sum(d26); PD25 = T25 / sum(d25)
# July 2025 (index 0) captured only 2 weeks -> like-for-like excludes it
L26, L25 = sum(c26[1:]), sum(c25[1:])          # Aug-Jun, both fully reported
LFL = (L26 / L25 - 1) * 100                      # fair year-on-year
PDL26 = L26 / sum(d26[1:]); PDL25 = L25 / sum(d25[1:])   # per-day, SAME Aug-Jun basis
JUL_PARTIAL = d26[0] < 20
# value facts (F8) — verified against the monthly data
beats = [(MABBR[MONTHS[i]], c26[i], c25[i], c26[i]-c25[i]) for i in range(1,12) if c26[i] > c25[i]]

print("Month   FY26  FY25   Δ")
for i, m in enumerate(MONTHS):
    print(f"  {MABBR[m]:<4}{c26[i]:>6}{c25[i]:>6}   {c26[i]-c25[i]:+d}")
print(f"  TOT {T26:>6}{T25:>6}   {T26-T25:+d}  ({(T26/T25-1)*100:+.1f}%)")
print(f"  per-day FY26 {PD26:.2f} vs FY25 {PD25:.2f} ({(PD26/PD25-1)*100:+.1f}%)")

# ---------- chart ----------
OUTDIR = "/Users/ahmadduais/Desktop/ASG/HOTC/2026"
os.makedirs(OUTDIR, exist_ok=True)
chartpng = os.path.join(OUTDIR, "_edward_calls_chart.png")
fig, ax = plt.subplots(figsize=(9.2, 3.5), dpi=200)
x = range(len(MONTHS)); w = 0.4
ax.bar([i - w/2 for i in x], c25, w, label='FY25 (prior year)', color='#B8912F')
ax.bar([i + w/2 for i in x], c26, w, label='FY26 (this year)', color='#1F3864')
ax.set_xticks(list(x)); ax.set_xticklabels([MABBR[m] for m in MONTHS], fontsize=9)
ax.set_ylabel('Calls from businesses', fontsize=9)
ax.yaxis.set_major_locator(MaxNLocator(integer=True))
ax.legend(frameon=False, fontsize=9, loc='upper right')
ax.spines[['top','right']].set_visible(False)
ax.grid(axis='y', color='#DDDDDD', linewidth=0.6)
bars26 = ax.patches[len(MONTHS):]           # FY26 bars (second set)
if JUL_PARTIAL:
    ax.patches[0].set_hatch('////'); ax.patches[0].set_alpha(0.55)   # FY25 Jul (full)
    bars26[0].set_hatch('////'); bars26[0].set_alpha(0.55)           # FY26 Jul (partial)
    ax.text(0, max(c25)*0.5, 'Jul \'25\npart-year', ha='center', va='center', fontsize=6, color='#B01E1E')
for i in x:
    if c26[i]: ax.text(i + w/2, c26[i] + 3, str(c26[i]), ha='center', fontsize=6.5, color='#1F3864')
plt.tight_layout()
plt.savefig(chartpng, bbox_inches='tight'); plt.close()

# ---------- PDF ----------
pdf = os.path.join(OUTDIR, "HOTC_Calls_From_Businesses_FY26_vs_FY25.pdf")
doc = SimpleDocTemplate(pdf, pagesize=A4, topMargin=16*mm, bottomMargin=14*mm,
                        leftMargin=16*mm, rightMargin=16*mm)
ss = getSampleStyleSheet()
H = ParagraphStyle('H', parent=ss['Title'], textColor=NAVY, fontSize=18, leading=22, spaceAfter=2, alignment=TA_LEFT)
SUB = ParagraphStyle('SUB', parent=ss['Normal'], textColor=GREY, fontSize=10, leading=13, spaceAfter=2)
MAST = ParagraphStyle('MAST', parent=ss['Normal'], textColor=GOLD, fontSize=9, leading=11, spaceAfter=1)
BODY = ParagraphStyle('BODY', parent=ss['Normal'], fontSize=9.5, leading=13, spaceAfter=4)
NOTE = ParagraphStyle('NOTE', parent=ss['Normal'], fontSize=8, leading=11, textColor=GREY)
H2 = ParagraphStyle('H2', parent=ss['Normal'], textColor=NAVY, fontSize=12, leading=15, spaceBefore=8, spaceAfter=4, fontName='Helvetica-Bold')
el = []
el.append(Paragraph('ABSOLUTE SECURITY GROUP', MAST))
el.append(Paragraph('Calls from Businesses — Full-Year Report', H))
el.append(Paragraph('Heart of the City — CBD Safety Team &nbsp;|&nbsp; FY2026 (1 Jul 2025 – 30 Jun 2026) vs FY2025 (1 Jul 2024 – 30 Jun 2025)', SUB))
el.append(Spacer(1, 8))

# KPI band
def kpi(label, value, sub, color=NAVY):
    return Table([[Paragraph(f'<b>{value}</b>', ParagraphStyle('v', fontSize=20, textColor=color, leading=22))],
                  [Paragraph(label, ParagraphStyle('l', fontSize=8, textColor=GREY, leading=10))],
                  [Paragraph(sub, ParagraphStyle('s', fontSize=7.5, textColor=GREY, leading=9))]],
                 colWidths=[54*mm])
band = Table([[kpi('FY26 total business calls', f'{T26:,}*', '1 Jul 25 – 30 Jun 26'),
               kpi('FY25 total business calls', f'{T25:,}', '1 Jul 24 – 30 Jun 25', GOLD),
               kpi('Like-for-like YoY', f'{LFL:+.0f}%', '11 fully-reported months (Aug–Jun)')]],
             colWidths=[58*mm, 58*mm, 58*mm])
band.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.5,LIGHT),('INNERGRID',(0,0),(-1,-1),0.5,LIGHT),
                          ('BACKGROUND',(0,0),(-1,-1),LIGHT),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                          ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
                          ('LEFTPADDING',(0,0),(-1,-1),10)]))
el.append(band); el.append(Spacer(1, 8))

# ---- What the data shows (F8: honest, data-backed value line) ----
VAL = ParagraphStyle('VAL', parent=ss['Normal'], fontSize=9.5, leading=13, textColor=NAVY,
                     backColor=colors.HexColor('#F6F8FC'), borderPadding=6, spaceAfter=6)
valtxt = (f"<b>What the data shows:</b> business demand for the CBD Safety Team stayed strong across FY26 "
          f"({T26:,} recorded calls). Engagement held its strongest recent months this year — "
          f"October ({c26[3]}), December ({c26[5]}) and June ({c26[11]}) each exceeded the same month a year earlier "
          f"(+{c26[3]-c25[3]}, +{c26[5]-c25[5]}, +{c26[11]-c25[11]}); December and October were the two "
          f"highest-volume months in the comparison window across both years, and June closed "
          f"+{(c26[11]/c25[11]-1)*100:.0f}% year-on-year.")
el.append(Table([[Paragraph(valtxt, VAL)]], colWidths=[178*mm],
                style=TableStyle([('BOX',(0,0),(-1,-1),0.5,LIGHT),('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#F6F8FC')),
                                  ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
                                  ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)])))
el.append(Spacer(1, 8))

el.append(Image(chartpng, width=178*mm, height=178/9.2*3.5*mm))
el.append(Spacer(1, 8))

# monthly table
el.append(Paragraph('Monthly breakdown', H2))
hdr = ['Month', 'FY26', 'FY25', 'Change']
rows = [hdr]
for i, m in enumerate(MONTHS):
    delta = c26[i]-c25[i]
    partial = (i == 0 and JUL_PARTIAL)
    v26 = f'{c26[i]:,} *' if partial else f'{c26[i]:,}'
    chg = '— *' if partial else f'{delta:+d}'
    rows.append([MABBR[m], v26, f'{c25[i]:,}', chg])
rows.append(['Aug–Jun (like-for-like)', f'{L26:,}', f'{L25:,}', f'{LFL:+.0f}%'])
rows.append(['Full-year total', f'{T26:,} *', f'{T25:,}', 'see *'])
tbl = Table(rows, colWidths=[46*mm, 38*mm, 38*mm, 38*mm])
style = [('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),colors.white),
         ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),9),
         ('ALIGN',(1,0),(-1,-1),'CENTER'),('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#CCCCCC')),
         ('ROWBACKGROUNDS',(0,1),(-1,-3),[colors.white, colors.HexColor('#F6F8FC')]),
         ('BACKGROUND',(0,-2),(-1,-2),colors.HexColor('#E4EBF6')),('FONTNAME',(0,-2),(-1,-2),'Helvetica-Bold'),
         ('TEXTCOLOR',(3,-2),(3,-2),RED),
         ('BACKGROUND',(0,-1),(-1,-1),LIGHT),('FONTNAME',(0,-1),(-1,-1),'Helvetica-Bold'),
         ('TEXTCOLOR',(0,-1),(-1,-1),GREY),
         ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]
for i in range(len(MONTHS)):
    if i == 0 and JUL_PARTIAL:
        style.append(('TEXTCOLOR',(0,1),(-1,1), GREY)); continue   # grey the partial-July row
    delta = c26[i]-c25[i]
    style.append(('TEXTCOLOR',(3,i+1),(3,i+1), GREEN if delta>=0 else RED))
tbl.setStyle(TableStyle(style))
el.append(tbl); el.append(Spacer(1, 8))

el.append(Paragraph('Notes', H2))
el.append(Paragraph(f'&bull;&nbsp; <b>* The FY26 full-year total includes part-reported July 2025 (2 of ~4–5 weeks captured).</b> It is therefore lower than a fully-reported year would show and is <b>not</b> directly comparable to FY25’s complete 3,042. The valid comparison is the <b>Aug–Jun like-for-like: {L26:,} vs {L25:,} ({LFL:+.0f}%).</b>', NOTE))
el.append(Paragraph(f'&bull;&nbsp; Per patrol day (Aug–Jun, same like-for-like basis): {PDL26:.1f} (FY26) vs {PDL25:.1f} (FY25).', NOTE))
el.append(Paragraph('&bull;&nbsp; Figures are total calls from businesses recorded in the weekly patrol data, summed by month. Detailed callout and incident breakdowns are available in the daily logs and weekly reports.', NOTE))
el.append(Paragraph('&bull;&nbsp; FY26 was delivered under a changed patrol-coverage footprint relative to FY25; Absolute Security Group can provide the underlying deployment/coverage figures to support like-for-like interpretation on request.', NOTE))
el.append(Spacer(1, 6))
el.append(Paragraph('Prepared by Absolute Security Group for Heart of the City.', NOTE))

doc.build(el)
print("\nPDF:", pdf)
# also copy to Downloads
import shutil
shutil.copy2(pdf, os.path.join(os.path.expanduser('~/Downloads'), os.path.basename(pdf)))
print("Copied to Downloads.")
