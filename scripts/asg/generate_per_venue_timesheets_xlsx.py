#!/usr/bin/env python3
"""
One EXCEL timesheet per venue from a verified weekly ASG timesheet — hours only, no charge/rate.

Reads 'Detail by Site & Date' and writes one .xlsx per venue:
  header (venue + week ending) · table (Date | Officer | Role | Hours) · total.

Usage:
  ~/Desktop/Dev/Claude/.venv/bin/python generate_per_venue_timesheets_xlsx.py \
      "/Users/ahmadduais/Desktop/ASG - Timesheets/Timesheet - Weekending - 26-07-2026.xlsx" \
      "/Users/ahmadduais/Desktop/timesheets for week ending 26-07-2026"
"""
import sys, os, re
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

INTERNAL = {"admin", "office", "training", "induction", "meeting", "hq"}

TS_PATH = sys.argv[1] if len(sys.argv) > 1 else \
    "/Users/ahmadduais/Desktop/ASG - Timesheets/Timesheet - Weekending - 26-07-2026.xlsx"
m = re.search(r"(\d{2})-(\d{2})-(\d{4})", os.path.basename(TS_PATH))
we_file = m.group(0) if m else "unknown"
we_human = f"Sunday {int(m.group(1))} {['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][int(m.group(2))]} {m.group(3)}" if m else "[week ending]"
OUT_DIR = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser(f"~/Desktop/timesheets for week ending {we_file}")
os.makedirs(OUT_DIR, exist_ok=True)

wb = load_workbook(TS_PATH, data_only=True)
d = wb["Detail by Site & Date"]
by_site = {}
for r in range(2, d.max_row + 1):
    site = d.cell(r, 1).value
    if not site or not str(site).strip():
        continue
    site = str(site).lstrip("★↳ ").strip()
    date = str(d.cell(r, 2).value or "").strip()
    guard = str(d.cell(r, 3).value or "").strip()
    role = str(d.cell(r, 4).value or "").strip()
    try:
        hours = float(d.cell(r, 5).value or 0)
    except (TypeError, ValueError):
        continue
    by_site.setdefault(site, []).append((date, guard, role, hours))

def day_key(s):
    mm = re.search(r"(\d+)", s)
    return int(mm.group(1)) if mm else 99

def safe_name(v):
    return re.sub(r"[\\/:*?\"<>|]", "-", v).strip()

NAVY = "1F3B63"; LIGHT = "E8EEF5"; GREY = "777777"
thin = Side(style="thin", color="D0D0D0")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

def hdr(c, align="left"):
    c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor=NAVY)
    c.alignment = Alignment(horizontal=align, vertical="center"); c.border = border

def cel(c, align="left", num=False, bold=False, fill=None):
    c.font = Font(bold=bold); c.alignment = Alignment(horizontal=align, vertical="center"); c.border = border
    if num: c.number_format = "0.00"
    if fill: c.fill = PatternFill("solid", fgColor=fill)

count = 0; skipped = []
for venue in sorted(by_site):
    if venue.lower() in INTERNAL:
        skipped.append(venue); continue
    out = Workbook(); ws = out.active; ws.title = "Timesheet"
    ws["A1"] = "ABSOLUTE SECURITY GROUP"; ws["A1"].font = Font(bold=True, size=14, color=NAVY)
    ws["A2"] = venue; ws["A2"].font = Font(bold=True, size=12)
    ws["A3"] = f"Weekly Security Timesheet  ·  Week ending {we_human}"
    ws["A3"].font = Font(italic=True, size=9.5, color=GREY)
    hr = 5
    for j, h in enumerate(("Date", "Officer", "Role", "Hours"), start=1):
        hdr(ws.cell(hr, j, h), "center" if j in (3, 4) else "left")
    rr = hr + 1
    for (date, guard, role, hours) in sorted(by_site[venue], key=lambda x: (day_key(x[0]), x[1])):
        cel(ws.cell(rr, 1, date)); cel(ws.cell(rr, 2, guard))
        cel(ws.cell(rr, 3, role), "center"); cel(ws.cell(rr, 4, round(hours, 2)), "center", num=True)
        rr += 1
    cel(ws.cell(rr, 1, "TOTAL"), bold=True, fill=LIGHT)
    cel(ws.cell(rr, 2, ""), fill=LIGHT); cel(ws.cell(rr, 3, ""), fill=LIGHT)
    cel(ws.cell(rr, 4, round(sum(h for *_, h in by_site[venue]), 2)), "center", num=True, bold=True, fill=LIGHT)
    for col, w in zip("ABCD", (14, 30, 10, 10)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A6"
    out.save(os.path.join(OUT_DIR, f"Timesheet - {safe_name(venue)} - WE {we_file}.xlsx"))
    count += 1

print(f"Output folder: {OUT_DIR}")
print(f"Per-venue Excel timesheets written: {count}")
print(f"Skipped (internal): {skipped}")
