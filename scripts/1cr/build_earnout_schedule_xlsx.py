#!/usr/bin/env python3
"""
1st Call Recruitment — earn-out schedule, $11.5m -> $13.5m revenue.

Structure (Ahmad's math):
  Maintainable EBITDA = GP% * Revenue - Fixed OpEx
  TOTAL (raw)         = Multiple (2.69x) * EBITDA
  Settlement          = $750,000 fixed
  12-month earn-out   = TOTAL - Settlement
Bounded variant: earn-out floored at $0, total capped at $1.6m.
The extended range exposes the two edge cases:
  - below ~$11.83m revenue, raw earn-out < 0 (settlement > formula)
  - above $13.4m revenue, raw total > $1.6m (no cap)

Deliverable -> ~/Desktop/Acquisitions/1st-Call-Recruitment/Working Files/
"""
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

OUT = os.path.expanduser("~/Desktop/Acquisitions/1st-Call-Recruitment/Working Files")
XLSX = os.path.join(OUT, "1CR_Earnout_Schedule.xlsx")

NAVY = "13314F"; TEAL = "1C8C8C"; GREEN = "2E8B57"; RED = "C0392B"; AMBER = "B5762B"
LIGHT = "EEF3F6"; BAND = "F4F7F9"; INK = "1A1A1A"; GREY = "5A6B7B"

wb = Workbook(); ws = wb.active
ws.title = "Earn-out Schedule"
ws.sheet_view.showGridLines = False
thin = Side(style="thin", color="D5DCE3")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

def cell(r, c, val=None, bold=False, size=11, color=INK, fill=None,
         align="left", fmt=None, bd=False, italic=False):
    cl = ws.cell(row=r, column=c)
    if val is not None: cl.value = val
    cl.font = Font(name="Calibri", bold=bold, size=size, color=color, italic=italic)
    cl.alignment = Alignment(horizontal=align, vertical="center")
    if fill: cl.fill = PatternFill("solid", fgColor=fill)
    if fmt: cl.number_format = fmt
    if bd: cl.border = border
    return cl

# ---- title -------------------------------------------------------------
cell(1, 1, "1st Call Recruitment (JCR 2006 Ltd)", bold=True, size=15, color=NAVY)
cell(2, 1, "Earn-out schedule  $11.5m–$13.5m  —  $750k settlement + balance to ~2.69× EBITDA", size=11, color=GREY)

# ---- assumptions -------------------------------------------------------
cell(4, 1, "Assumptions", bold=True, size=11, color=NAVY)
ass = [("Maintainable gross margin", 0.2005, "0.00%"),
       ("Fixed operating costs (below GP)", 2093288, "#,##0"),
       ("Settlement (fixed, at completion)", 750000, "$#,##0"),
       ("Total consideration multiple (× EBITDA)", 2.69, '0.00"×"'),
       ("Total cap", 1600000, "$#,##0")]
for i, (lab, val, fmt) in enumerate(ass):
    r = 5 + i
    cell(r, 1, lab, color=INK)
    cell(r, 2, val, align="right", fmt=fmt, fill=LIGHT, bd=True)
GP, OPEX, SETT, MULT, CAP = "$B$5", "$B$6", "$B$7", "$B$8", "$B$9"

# ---- table -------------------------------------------------------------
H = 12
hdrs = ["Revenue", "EBITDA\n(maintainable)", "Settlement",
        "12-mo earn-out\n(raw)", "Total\n(raw, 2.69×)",
        "12-mo earn-out\n(floored $0)", "Total\n(floor $750k / cap $1.6m)", "Note"]
for i, h in enumerate(hdrs, start=1):
    c = cell(H, i, h, bold=True, size=10, color="FFFFFF", fill=NAVY, align="center", bd=True)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
ws.row_dimensions[H].height = 34

GPv, OPEXv, SETTv, MULTv, CAPv = 0.2005, 2093288, 750000, 2.69, 1600000
def eb(R): return GPv * R - OPEXv

rows = [
    (11_500_000, "below floor — settlement overpays"),
    (11_831_962, "break-even: earn-out = $0"),
    (12_000_000, ""),
    (12_100_000, "run-rate"),
    (12_400_000, ""),
    (12_600_000, ""),
    (12_640_040, "FY26 actual"),
    (12_800_000, ""),
    (13_000_000, ""),
    (13_200_000, ""),
    (13_400_000, "recovery → ~$1.6m"),
    (13_500_000, "above cap — total exceeds $1.6m"),
]
r = H + 1
for rev, note in rows:
    e = eb(rev); tot = MULTv * e; eo = tot - SETTv
    band = BAND if note == "FY26 actual" else None
    bold = note == "FY26 actual"
    eo_color = RED if eo < 0 else GREEN
    tot_color = AMBER if tot > CAPv else NAVY
    cell(r, 1, rev, align="right", fmt='$#,##0', fill=band, bd=True, bold=bold)
    cell(r, 2, f"={GP}*A{r}-{OPEX}", align="right", fmt='$#,##0', fill=band, bd=True, bold=bold, color=NAVY)
    cell(r, 3, f"={SETT}", align="right", fmt='$#,##0', fill=band, bd=True)
    cell(r, 4, f"={MULT}*B{r}-{SETT}", align="right", fmt='$#,##0;[Red]-$#,##0', fill=band, bd=True, color=eo_color)
    cell(r, 5, f"={MULT}*B{r}", align="right", fmt='$#,##0', fill=band, bd=True, color=tot_color)
    cell(r, 6, f"=MIN(MAX({MULT}*B{r}-{SETT},0),{CAP}-{SETT})", align="right", fmt='$#,##0', fill=band, bd=True, color=GREEN)
    cell(r, 7, f"=MIN(MAX({MULT}*B{r},{SETT}),{CAP})", align="right", fmt='$#,##0', fill=band, bd=True, bold=bold, color=NAVY)
    cell(r, 8, note, italic=True, color=(RED if "overpay" in note or "above cap" in note else GREY), fill=band)
    r += 1

# ---- notes -------------------------------------------------------------
cell(r + 1, 1, "Raw columns = the pure 2.69× formula. Floored/capped columns bound it: earn-out never below $0, total never above $1.6m.",
     size=8.5, color=GREY)
cell(r + 2, 1, "Below ~$11.83m revenue the $750k settlement exceeds 2.69× EBITDA (overpay, no clawback). Above $13.4m the raw total runs past $1.6m.",
     size=8.5, color=GREY)
cell(r + 3, 1, "Basis: FY26 normalised EBITDA $441k (owner, IT, FBT, disposal gain & 3 accrual releases adjusted; $50k sublease retained).",
     size=8.5, color=GREY)
cell(r + 4, 1, "Source: FY26 Xero Profit & Loss, JCR 2006 Limited, year ended 31 March 2026 (draft).",
     size=8.5, color=GREY)

for col, w in zip("ABCDEFG", (15, 17, 13, 16, 16, 16, 18)):
    ws.column_dimensions[col].width = w
ws.column_dimensions["H"].width = 30
ws.freeze_panes = f"A{H+1}"

wb.save(XLSX)
print("Wrote", XLSX)

# ---- console verification ----------------------------------------------
print("\nVerification ($11.5m–$13.5m):")
for rev, _ in rows:
    e = eb(rev); tot = MULTv * e; eo = tot - SETTv
    eo_b = min(max(eo, 0), CAPv - SETTv); tot_b = min(max(tot, SETTv), CAPv)
    print(f"  ${rev:>11,.0f}  EBITDA ${e:>8,.0f}  raw EO ${eo:>11,.2f}  raw tot ${tot:>12,.2f}   | capped EO ${eo_b:>9,.0f}  tot ${tot_b:>10,.0f}")
