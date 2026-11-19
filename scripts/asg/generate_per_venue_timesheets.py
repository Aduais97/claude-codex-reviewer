#!/usr/bin/env python3
"""
Split a verified weekly ASG timesheet into ONE PDF per venue — invoice-backup docs for Xero.

Reads the 'Detail by Site & Date' sheet of a
'Timesheet - Weekending - DD-MM-YYYY.xlsx' and writes one PDF per venue:
  header · venue · week-ending · shift table (Date | Officer | Role | Hours) · total · charge summary.

Usage:
  ~/Desktop/Dev/Claude/.venv/bin/python generate_per_venue_timesheets.py \
      "/Users/ahmadduais/Desktop/ASG - Timesheets/Timesheet - Weekending - 26-07-2026.xlsx" \
      "/Users/ahmadduais/Desktop/timesheets for week ending 26-07-2026"
"""
import sys, os, re
from openpyxl import load_workbook
from fpdf import FPDF
from fpdf.fonts import FontFace

RATE = 38.50   # ex-GST default charge-out (ASG, from 1 Jul 2026)
GST = 0.15
INTERNAL = {"admin", "office", "training", "induction", "meeting", "hq"}

TS_PATH = sys.argv[1] if len(sys.argv) > 1 else \
    "/Users/ahmadduais/Desktop/ASG - Timesheets/Timesheet - Weekending - 26-07-2026.xlsx"

m = re.search(r"(\d{2})-(\d{2})-(\d{4})", os.path.basename(TS_PATH))
we_file = m.group(0) if m else "unknown"
we_human = f"Sunday {int(m.group(1))} {['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][int(m.group(2))]} {m.group(3)}" if m else "[week ending]"

OUT_DIR = sys.argv[2] if len(sys.argv) > 2 else \
    os.path.expanduser(f"~/Desktop/timesheets for week ending {we_file}")
os.makedirs(OUT_DIR, exist_ok=True)

# ---- read Detail sheet ----
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
    hours = d.cell(r, 5).value or 0
    try:
        hours = float(hours)
    except (TypeError, ValueError):
        continue
    by_site.setdefault(site, []).append((date, guard, role, hours))

def day_key(s):
    mm = re.search(r"(\d+)", s)
    return int(mm.group(1)) if mm else 99

NAVY = (31, 59, 99)
GREY = (120, 120, 120)

def safe_name(v):
    return re.sub(r"[\\/:*?\"<>|]", "-", v).strip()

def venue_pdf(venue, shifts, path):
    shifts = sorted(shifts, key=lambda x: (day_key(x[0]), x[1]))
    total = round(sum(s[3] for s in shifts), 2)
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(True, margin=16)
    pdf.add_page()
    # header
    pdf.set_text_color(*NAVY); pdf.set_font("Helvetica", "B", 17)
    pdf.cell(0, 9, "ABSOLUTE SECURITY GROUP", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*GREY); pdf.set_font("Helvetica", "", 8.5)
    pdf.cell(0, 5, "7/220 Queen Street, Auckland   -   +64 9 921 5710   -   sales@slsrtc.co.nz",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_draw_color(200, 200, 200); pdf.line(pdf.l_margin, pdf.get_y(), 210 - pdf.r_margin, pdf.get_y())
    pdf.ln(3)
    pdf.set_text_color(0, 0, 0); pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Weekly Security Timesheet", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, f"Venue:  {venue}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Week ending:  {we_human}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    # table
    pdf.set_font("Helvetica", "", 10)
    head_style = FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=NAVY)
    bold = FontFace(emphasis="BOLD")
    with pdf.table(col_widths=(26, 78, 18, 18),
                   text_align=("LEFT", "LEFT", "CENTER", "RIGHT"),
                   headings_style=head_style, line_height=6.5, width=140) as table:
        hrow = table.row()
        for h in ("Date", "Officer", "Role", "Hours"):
            hrow.cell(h)
        for (date, guard, role, hours) in shifts:
            row = table.row()
            row.cell(date); row.cell(guard); row.cell(role); row.cell(f"{hours:.2f}")
        trow = table.row(style=bold)
        trow.cell("TOTAL"); trow.cell(""); trow.cell(""); trow.cell(f"{total:.2f}")
    # charge summary
    ex = total * RATE; gst = ex * GST; inc = ex + gst
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 6, f"Total billable hours:  {total:.2f}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 5.5, f"Charges ex-GST  (@ $38.50/hr):   ${ex:,.2f}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5.5, f"GST (15%):   ${gst:,.2f}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 6, f"Total inc-GST:   ${inc:,.2f}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_text_color(*GREY); pdf.set_font("Helvetica", "I", 8)
    pdf.cell(0, 4.5, "Charge shown at default rate $38.50/hr ex-GST (from 1 Jul 2026); adjust to this client's contracted rate before invoicing.",
             new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 4.5, "Supporting document for tax invoice. Hours reconcile to the master weekly timesheet.",
             new_x="LMARGIN", new_y="NEXT")
    pdf.output(path)
    return total

count = 0; grand = 0.0; skipped = []
for venue in sorted(by_site):
    if venue.lower() in INTERNAL:
        skipped.append(venue); continue
    path = os.path.join(OUT_DIR, f"Timesheet - {safe_name(venue)} - WE {we_file}.pdf")
    grand += venue_pdf(venue, by_site[venue], path)
    count += 1

print(f"Output folder: {OUT_DIR}")
print(f"Per-venue PDFs written: {count}")
print(f"Skipped (internal): {skipped}")
print(f"Sum of billable hours across venue PDFs: {grand:.2f}")
