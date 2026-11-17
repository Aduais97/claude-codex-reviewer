#!/usr/bin/env python3
"""
Per-GUARD hours workbook from a verified weekly ASG timesheet.

One Excel workbook:
  - 'Summary' tab: Guard | Total Hours (+ grand total)
  - one tab per guard: Date | Venue | Hours (+ total)
No rates / no charges — hours only.

Usage:
  ~/Desktop/Dev/Claude/.venv/bin/python generate_per_guard_hours.py \
      "/Users/ahmadduais/Desktop/ASG - Timesheets/Timesheet - Weekending - 26-07-2026.xlsx" \
      "/Users/ahmadduais/Desktop/timesheets for week ending 26-07-2026/Guard Hours - Week Ending 26-07-2026.xlsx"
"""
import sys, os, re
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

TS_PATH = sys.argv[1] if len(sys.argv) > 1 else \
    "/Users/ahmadduais/Desktop/ASG - Timesheets/Timesheet - Weekending - 26-07-2026.xlsx"
m = re.search(r"(\d{2})-(\d{2})-(\d{4})", os.path.basename(TS_PATH))
we_file = m.group(0) if m else "unknown"
we_human = f"{int(m.group(1))} {['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][int(m.group(2))]} {m.group(3)}" if m else "[week ending]"
OUT = sys.argv[2] if len(sys.argv) > 2 else \
    os.path.expanduser(f"~/Desktop/timesheets for week ending {we_file}/Guard Hours - Week Ending {we_file}.xlsx")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

# ---- read Detail (SITE | DATE | GUARD | ROLE | HOURS) ----
wb = load_workbook(TS_PATH, data_only=True)
d = wb["Detail by Site & Date"]
by_guard = {}
for r in range(2, d.max_row + 1):
    site = d.cell(r, 1).value
    guard = d.cell(r, 3).value
    if not guard or not str(guard).strip() or not site:
        continue
    site = str(site).lstrip("★↳ ").strip()
    date = str(d.cell(r, 2).value or "").strip()
    try:
        hours = float(d.cell(r, 5).value or 0)
    except (TypeError, ValueError):
        continue
    by_guard.setdefault(str(guard).strip(), []).append((date, site, hours))

def day_key(s):
    mm = re.search(r"(\d+)", s)
    return int(mm.group(1)) if mm else 99

NAVY = "1F3B63"; LIGHT = "E8EEF5"; GREY = "777777"
thin = Side(style="thin", color="D0D0D0")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

def hdr_cell(c, align="left"):
    c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor=NAVY)
    c.alignment = Alignment(horizontal=align, vertical="center"); c.border = border

def cell(c, align="left", num=False, bold=False, fill=None):
    c.font = Font(bold=bold)
    c.alignment = Alignment(horizontal=align, vertical="center")
    c.border = border
    if num: c.number_format = "0.00"
    if fill: c.fill = PatternFill("solid", fgColor=fill)

def sane_tab(name, used):
    t = re.sub(r"[:\\/?*\[\]]", " ", name).strip()[:31] or "Guard"
    base = t; i = 2
    while t.lower() in used:
        suf = f" {i}"; t = base[:31 - len(suf)] + suf; i += 1
    used.add(t.lower()); return t

out = Workbook()
# ---- Summary sheet ----
sm = out.active; sm.title = "Summary"
sm["A1"] = "ASG — Guard Hours"; sm["A1"].font = Font(bold=True, size=15, color=NAVY)
sm["A2"] = f"Week ending {we_human}  ·  hours worked (clock-in to clock-out), per guard"
sm["A2"].font = Font(italic=True, size=9.5, color=GREY)
hdr_cell(sm.cell(4, 1, "Guard")); hdr_cell(sm.cell(4, 2, "Total Hours"), "center")
r = 5; grand = 0.0
tab_of = {}
for g in sorted(by_guard, key=lambda x: x.lower()):
    tot = round(sum(h for _, _, h in by_guard[g]), 2); grand += tot
    cell(sm.cell(r, 1, g)); cell(sm.cell(r, 2, tot), "center", num=True)
    r += 1
cell(sm.cell(r, 1, "TOTAL"), bold=True, fill=LIGHT)
cell(sm.cell(r, 2, round(grand, 2)), "center", num=True, bold=True, fill=LIGHT)
sm.column_dimensions["A"].width = 30; sm.column_dimensions["B"].width = 14
sm.freeze_panes = "A5"

# ---- per-guard tabs ----
used = set()
for g in sorted(by_guard, key=lambda x: x.lower()):
    ws = out.create_sheet(sane_tab(g, used))
    ws["A1"] = g; ws["A1"].font = Font(bold=True, size=13, color=NAVY)
    ws["A2"] = f"Week ending {we_human}"; ws["A2"].font = Font(italic=True, size=9.5, color=GREY)
    hdr_cell(ws.cell(4, 1, "Date")); hdr_cell(ws.cell(4, 2, "Venue")); hdr_cell(ws.cell(4, 3, "Hours"), "center")
    rr = 5
    for (date, venue, hours) in sorted(by_guard[g], key=lambda x: (day_key(x[0]), x[1])):
        cell(ws.cell(rr, 1, date)); cell(ws.cell(rr, 2, venue)); cell(ws.cell(rr, 3, round(hours, 2)), "center", num=True)
        rr += 1
    cell(ws.cell(rr, 1, "TOTAL"), bold=True, fill=LIGHT); cell(ws.cell(rr, 2, ""), fill=LIGHT)
    cell(ws.cell(rr, 3, round(sum(h for _, _, h in by_guard[g]), 2)), "center", num=True, bold=True, fill=LIGHT)
    ws.column_dimensions["A"].width = 14; ws.column_dimensions["B"].width = 34; ws.column_dimensions["C"].width = 10
    ws.freeze_panes = "A5"

out.save(OUT)
print("Saved:", OUT)
print(f"Guards: {len(by_guard)} | tabs: {len(out.sheetnames)} (incl Summary) | grand total hours: {grand:.2f}")
