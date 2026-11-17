#!/usr/bin/env python3
"""CRL guard-hours matrix — guards in rows, days of the month in columns, hours worked in cells.
Pivots a CRL monthly invoice (per-guard/per-day/per-station timesheet) into a roster-style grid.
Tabs: All CRL (combined across stations) + one per station. Row totals = guard's monthly hours;
column totals = daily hours + headcount. Reconciles to the invoice station totals.

Usage: python3 build_crl_hours_matrix.py ["<invoice.xlsx>"]   (default = amended June 2026 invoice)
Out:   ~/Desktop/ASG/Operations/Clients/CRL/CRL Guard Hours Matrix - <Mon Year>.xlsx
"""
import os, sys, calendar
from datetime import datetime
from collections import defaultdict
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L

SRC = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1
                         else "~/Downloads/June Invoice Amended - CRL.xlsx")

# invoice sheet name -> station display name
STATION = {"Aotea": "Te Waihorotiu (Aotea)", "K Road": "Karanga-a-Hape (K Rd)", "Mt Eden": "Maungawhau (Mt Eden)"}
LABELS = {"total", "standard rate", "public holiday", "ph", "holiday", "subtotal"}

NAVY="1E2A3A"; GOLD="C8952A"; LIGHT="EEF2F6"; WKND="FBF1D9"; WHITE="FFFFFF"; INK="1F2733"; SUB="5A6675"
thin=Side(style="thin", color="D3DAE3"); B=Border(left=thin,right=thin,top=thin,bottom=thin)
CEN=Alignment(horizontal="center", vertical="center")
LEFT=Alignment(horizontal="left", vertical="center", indent=1)

def norm(n):
    return " ".join(str(n).split()).strip().title()

# ---- parse invoice: hours[station][guard][day] = summed hours ----
wb_in = openpyxl.load_workbook(SRC, data_only=True)
hours = {STATION[s]: defaultdict(lambda: defaultdict(float)) for s in wb_in.sheetnames if s in STATION}
combined = defaultdict(lambda: defaultdict(float))
year = month = None
for sh in wb_in.sheetnames:
    if sh not in STATION: continue
    st = STATION[sh]
    for r in list(wb_in[sh].iter_rows(values_only=True))[1:]:
        name, date, start, end, hrs = r[0], r[1], r[2], r[3], r[4]
        lab = " ".join(str(x).lower() for x in r if x is not None)
        if any(k in lab for k in LABELS): continue          # skip embedded total/label rows
        if not name or not isinstance(date, datetime) or start is None or end is None: continue
        try: h = float(hrs)
        except (TypeError, ValueError): continue
        if h <= 0 or h > 20: continue
        g = norm(name); d = date.day
        hours[st][g][d] += h
        combined[g][d] += h
        year, month = date.year, date.month

NDAYS = calendar.monthrange(year, month)[1]
MON = calendar.month_abbr[month]
WK = ["M", "T", "W", "T", "F", "S", "S"]

def build_tab(wb, title, subtitle, data):
    ws = wb.create_sheet(title[:31])
    ws.sheet_view.showGridLines = False
    ncol = 1 + NDAYS + 1
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=ncol)
    t = ws.cell(1, 1, subtitle); t.font = Font(name="Arial", size=12, bold=True, color=WHITE)
    t.fill = PatternFill("solid", fgColor=NAVY); t.alignment = Alignment(indent=1, vertical="center")
    ws.row_dimensions[1].height = 24
    # header (row 3): Guard | 1..NDAYS | Total
    hc = ws.cell(3, 1, "Guard"); hc.font = Font(name="Arial", size=9.5, bold=True, color=WHITE)
    hc.fill = PatternFill("solid", fgColor=NAVY); hc.alignment = LEFT; hc.border = B
    wknd_cols = []
    for d in range(1, NDAYS + 1):
        wd = datetime(year, month, d).weekday()
        c = ws.cell(3, 1 + d, f"{d}\n{WK[wd]}")
        c.font = Font(name="Arial", size=8, bold=True, color=WHITE)
        c.fill = PatternFill("solid", fgColor=NAVY); c.border = B
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        if wd >= 5: wknd_cols.append(1 + d)
    tc = ws.cell(3, ncol, "Total h"); tc.font = Font(name="Arial", size=9.5, bold=True, color=WHITE)
    tc.fill = PatternFill("solid", fgColor=GOLD); tc.alignment = CEN; tc.border = B
    ws.row_dimensions[3].height = 26

    guards = sorted(data.keys())
    r = 4
    col_tot = defaultdict(float); col_head = defaultdict(int)
    for g in guards:
        gc = ws.cell(r, 1, g); gc.font = Font(name="Arial", size=9.5, color=INK); gc.alignment = LEFT; gc.border = B
        row_tot = 0.0
        for d in range(1, NDAYS + 1):
            h = data[g].get(d, 0.0)
            cell = ws.cell(r, 1 + d)
            if h > 0:
                cell.value = round(h, 2); cell.number_format = '0.##'
                row_tot += h; col_tot[d] += h; col_head[d] += 1
                cell.font = Font(name="Arial", size=9, color=INK)
            cell.alignment = CEN; cell.border = B
            if (1 + d) in wknd_cols and h == 0:
                cell.fill = PatternFill("solid", fgColor=WKND)
            elif (1 + d) in wknd_cols:
                cell.fill = PatternFill("solid", fgColor=WKND)
        rt = ws.cell(r, ncol, round(row_tot, 2)); rt.number_format = '0.##'
        rt.font = Font(name="Arial", size=9.5, bold=True, color=NAVY); rt.alignment = CEN; rt.border = B
        rt.fill = PatternFill("solid", fgColor=LIGHT)
        r += 1
    # daily total + headcount rows
    for label, src, fmt in [("Daily hours", col_tot, '0.##'), ("Guards on shift", col_head, '0')]:
        lc = ws.cell(r, 1, label); lc.font = Font(name="Arial", size=9.5, bold=True, color=NAVY)
        lc.fill = PatternFill("solid", fgColor=LIGHT); lc.alignment = LEFT; lc.border = B
        tot = 0
        for d in range(1, NDAYS + 1):
            v = src.get(d, 0); tot += v
            c = ws.cell(r, 1 + d, round(v, 2) if v else None)
            c.number_format = fmt; c.font = Font(name="Arial", size=8.5, bold=True, color=NAVY)
            c.alignment = CEN; c.border = B; c.fill = PatternFill("solid", fgColor=LIGHT)
        gt = ws.cell(r, ncol, round(tot, 2)); gt.number_format = fmt
        gt.font = Font(name="Arial", size=10, bold=True, color=NAVY); gt.alignment = CEN; gt.border = B
        gt.fill = PatternFill("solid", fgColor=GOLD)
        r += 1
    # widths / freeze
    ws.column_dimensions["A"].width = 24
    for d in range(1, NDAYS + 1): ws.column_dimensions[L(1 + d)].width = 5.2
    ws.column_dimensions[L(ncol)].width = 9
    ws.freeze_panes = "B4"
    return sum(sum(v.values()) for v in data.values()), len(guards)

wb = openpyxl.Workbook(); wb.remove(wb.active)
gh = round(sum(sum(v.values()) for v in combined.values()), 2)
uniq = len(combined)
build_tab(wb, "All CRL — Combined",
          f"CITY RAIL LINK — Guard Hours by Day · {MON} {year} · ALL STATIONS combined · {gh:,.2f} h · {uniq} guards",
          combined)
recon = {}
for st, data in hours.items():
    st_h = round(sum(sum(v.values()) for v in data.values()), 2)
    tot, ng = build_tab(wb, st, f"{st.upper()} — Guard Hours by Day · {MON} {year} · {st_h:,.2f} h · {len(data)} guards", data)
    recon[st] = (tot, ng)

OUT = os.path.expanduser(f"~/Desktop/ASG/Operations/Clients/CRL/CRL Guard Hours Matrix - {MON} {year}.xlsx")
wb.save(OUT)
print(f"wrote {OUT}")
print(f"  period: {MON} {year} ({NDAYS} days)  |  combined: {gh:,.2f} h across {uniq} unique guards")
for st, (tot, ng) in recon.items():
    print(f"    {st:<26} {tot:>9,.2f} h  ({ng} guards)")
print(f"    {'STATION SUM':<26} {sum(t for t,_ in recon.values()):>9,.2f} h  (should tie to the invoice)")
