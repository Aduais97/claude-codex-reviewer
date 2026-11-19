#!/usr/bin/env python3
"""
ASG weekly BILLING SUMMARY — turns a verified 'Timesheet - Weekending - DD-MM-YYYY.xlsx'
(Site Summary sheet) into an invoice-ready, per-site billing worksheet with live formulas.

- Hours are read straight from the verified timesheet (no re-parsing) so they tie out exactly.
- Charge rate defaults to $38.50 ex-GST (ASG rate from 1 Jul 2026) — EDITABLE per row.
- Amount ex GST = Total hrs x rate; GST = 15%; Amount inc GST = ex x 1.15. All live formulas.
- 'Admin' / internal rows default to rate 0 (not billable) and are flagged.
- HD venues (star) flagged so a premium HD rate can be set per row if the contract differs.

Usage:
  ~/Desktop/Dev/Claude/.venv/bin/python generate_asg_billing_summary.py \
      "/Users/ahmadduais/Desktop/ASG - Timesheets/Timesheet - Weekending - 26-07-2026.xlsx"
"""
import sys, os, re
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

DEFAULT_RATE = 38.50          # ex-GST, ASG charge-out from 1 Jul 2026
GST = 0.15
INTERNAL = {"admin", "office", "training", "induction", "meeting", "hq"}  # rate 0, not billable

TS_PATH = sys.argv[1] if len(sys.argv) > 1 else \
    "/Users/ahmadduais/Desktop/ASG - Timesheets/Timesheet - Weekending - 26-07-2026.xlsx"

# ---- derive week-ending label from filename ----
m = re.search(r"(\d{2})-(\d{2})-(\d{4})", os.path.basename(TS_PATH))
we_label = f"{m.group(1)}/{m.group(2)}/{m.group(3)}" if m else "[week ending]"
we_file = m.group(0) if m else "unknown"

# ---- read verified Site Summary ----
wb = load_workbook(TS_PATH, data_only=True)
ss = wb["Site Summary"]
# find header row (contains 'CLIENT / SITE')
hdr = next(r for r in range(1, ss.max_row + 1)
           if str(ss.cell(r, 1).value or "").strip().upper().startswith("CLIENT"))
sites = []
for r in range(hdr + 1, ss.max_row + 1):
    name = ss.cell(r, 1).value
    if name is None:
        continue
    name = str(name).strip()
    if name.upper() == "TOTAL":
        break
    if name.startswith("★HD venue") or name.startswith("Pay week"):
        continue
    hd = ss.cell(r, 2).value or 0
    guard = ss.cell(r, 3).value or 0
    phhd = ss.cell(r, 4).value or 0
    phg = ss.cell(r, 5).value or 0
    total = ss.cell(r, 6).value or 0
    is_hd = name.startswith("★")
    clean = name.lstrip("★↳ ").strip()
    sites.append((clean, is_hd, float(hd or 0), float(guard or 0),
                  float(phhd or 0), float(phg or 0), float(total or 0)))

# ---- build billing workbook ----
out = Workbook()
ws = out.active
ws.title = "Billing Summary"

NAVY = "1F3B63"; LIGHT = "E8EEF5"; YELLOW = "FFF2CC"; GREY = "777777"; REDF = "C00000"
thin = Side(style="thin", color="CCCCCC")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

def style_cell(c, bold=False, fill=None, color=None, align=None, money=False, num=False, size=None):
    if bold: c.font = Font(bold=True, color=color or "000000", size=size or 11)
    elif color or size: c.font = Font(color=color or "000000", size=size or 11)
    if fill: c.fill = PatternFill("solid", fgColor=fill)
    if align: c.alignment = Alignment(horizontal=align, vertical="center", wrap_text=(align == "center"))
    if money: c.number_format = '"$"#,##0.00'
    if num: c.number_format = '0.00'
    c.border = border

# Title block
ws.merge_cells("A1:H1")
ws["A1"] = "ASG — WEEKLY BILLING SUMMARY"
ws["A1"].font = Font(bold=True, size=16, color=NAVY)
ws.merge_cells("A2:H2")
ws["A2"] = (f"Week ending {we_label}  ·  hours from verified timesheet  ·  "
            f"rates shown EX-GST  ·  default charge-out $38.50/hr (from 1 Jul 2026) — EDIT per row where a client rate differs")
ws["A2"].font = Font(italic=True, size=9.5, color=GREY)

HDRS = ["Client / Site", "HD hrs", "Guard hrs", "Total hrs",
        "Rate $/hr (ex GST)", "Amount (ex GST)", "GST 15%", "Amount (inc GST)"]
hr = 4
for j, h in enumerate(HDRS, start=1):
    c = ws.cell(hr, j, h)
    style_cell(c, bold=True, fill=NAVY, color="FFFFFF",
               align="center" if j > 1 else "left")

row = hr + 1
first = row
for (name, is_hd, hd, guard, phhd, phg, total) in sites:
    internal = name.lower() in INTERNAL
    rate = 0 if internal else DEFAULT_RATE
    disp = ("★ " if is_hd else "") + name + ("   (internal — not billable)" if internal else "")
    ws.cell(row, 1, disp)
    style_cell(ws.cell(row, 1))
    if internal:
        ws.cell(row, 1).font = Font(color=GREY, italic=True)
    ws.cell(row, 2, round(hd + phhd, 2)); style_cell(ws.cell(row, 2), num=True, align="center")
    ws.cell(row, 3, round(guard + phg, 2)); style_cell(ws.cell(row, 3), num=True, align="center")
    ws.cell(row, 4, round(total, 2)); style_cell(ws.cell(row, 4), num=True, align="center")
    rc = ws.cell(row, 5, rate); style_cell(rc, money=True, align="center", fill=YELLOW)
    L = get_column_letter
    ws.cell(row, 6, f"=D{row}*E{row}"); style_cell(ws.cell(row, 6), money=True)
    ws.cell(row, 7, f"=F{row}*{GST}"); style_cell(ws.cell(row, 7), money=True)
    ws.cell(row, 8, f"=F{row}+G{row}"); style_cell(ws.cell(row, 8), money=True, bold=True)
    row += 1

last = row - 1
# TOTAL row
ws.cell(row, 1, "TOTAL"); style_cell(ws.cell(row, 1), bold=True, fill=LIGHT)
for col in (2, 3, 4):
    ws.cell(row, col, f"=SUM({get_column_letter(col)}{first}:{get_column_letter(col)}{last})")
    style_cell(ws.cell(row, col), bold=True, num=True, align="center", fill=LIGHT)
ws.cell(row, 5, ""); style_cell(ws.cell(row, 5), fill=LIGHT)
for col in (6, 7, 8):
    ws.cell(row, col, f"=SUM({get_column_letter(col)}{first}:{get_column_letter(col)}{last})")
    style_cell(ws.cell(row, col), bold=True, money=True, fill=LIGHT)
total_row = row

# widths
widths = [34, 9, 9, 9, 16, 15, 12, 16]
for j, w in enumerate(widths, start=1):
    ws.column_dimensions[get_column_letter(j)].width = w

# notes
nr = total_row + 2
notes = [
    ("CONFIRM BEFORE INVOICING:", REDF, True),
    ("• Default rate = $38.50/hr ex-GST (ASG rate letter, effective 1 Jul 2026). Overwrite any yellow Rate cell with the client's actual negotiated rate — totals recalculate.", GREY, False),
    ("• ★ = HD (door) venue. If your contract charges a PREMIUM for Head Doorman hours, add a separate line or lift that row's rate — the HD column here is a mix of true HD hours and single-rate hours at non-HD venues.", GREY, False),
    ("• 'Admin' and any internal rows are set to $0 (not billable) — confirm.", GREY, False),
    ("• Billing shown PER SITE. If several venues belong to one client group and invoice together, consolidate those rows.", GREY, False),
    ("• No public holiday this week, so no PH loading. AT train stations + HOTC are billed separately and are NOT in this sheet.", GREY, False),
    ("• Hours tie exactly to 'Timesheet - Weekending - " + we_file + ".xlsx' (Site Summary).", GREY, False),
]
for text, color, bold in notes:
    ws.cell(nr, 1, text)
    ws.cell(nr, 1).font = Font(color=color, bold=bold, size=10 if bold else 9)
    nr += 1

ws.freeze_panes = "A5"

OUT = os.path.join(os.path.dirname(TS_PATH), f"Billing Summary - Weekending - {we_file}.xlsx")
out.save(OUT)
print("Saved:", OUT)
print(f"Sites billed: {len(sites)} | default rate ${DEFAULT_RATE}/hr ex-GST")
print(f"Internal (rate 0): {[s[0] for s in sites if s[0].lower() in INTERNAL]}")
billable = sum(s[6] for s in sites if s[0].lower() not in INTERNAL)
print(f"Billable hours: {billable:.2f}  ->  ex-GST ${billable*DEFAULT_RATE:,.2f}  |  inc-GST ${billable*DEFAULT_RATE*1.15:,.2f}  (at flat ${DEFAULT_RATE})")
