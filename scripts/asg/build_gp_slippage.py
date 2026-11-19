#!/usr/bin/env python3
"""
ASG weekly GP / slippage-per-hour builder.

Combines the /asg-timesheets output with real payroll rates to produce a
true-cost, gross-profit and slippage-per-hour workbook, per site and per person.

INPUTS
------
1. Timesheet workbook (`Timesheet - Weekending - DD-MM-YYYY.xlsx`, from /asg-timesheets):
   - `Site Summary` sheet: Ahmad enters CHARGE-OUT rates INTO cols B/C
     (col B = HD/single-role charge rate, col C = guard charge rate at HD venues),
     overwriting the HD/Guard *hour* columns. Col F (Total) stays = hours.
     Where a charge rate is 0/blank, --charge-default (39) is used.
   - `Detail by Site & Date` sheet (SITE|DATE|GUARD|ROLE|HOURS): the true HD-vs-Guard
     hour split survives here and is the basis for both revenue and cost.
2. Payroll export CSV (e.g. `~/Downloads/New_Report*.csv`): columns
   `Contractor` (true/false), `Name`, `Normal Rate (SUM)`.
   Contractor=false  => EMPLOYEE  -> base rate + EMP_LOAD (default 8%, holiday pay only).
   Contractor=true   => contractor -> no loading.

RULES
-----
- Exclude `Admin` + `ASG Guards` site rows (internal, non-client).
- Unmatched staff (no rate on file) fall back to --base ($30) as a contractor.
- SLIPPAGE/hr = charge - real labour cost per billed hour = GROSS margin,
  BEFORE overhead (management, insurance, vehicles, ACC, non-billable, bad debt).
- 8% covers holiday pay only; a fully-compliant NZ on-cost (KiwiSaver/ACC/leave)
  would be higher if those become payable.

USAGE
-----
    python3 build_gp_slippage.py                       # auto: latest timesheet + latest New_Report csv
    python3 build_gp_slippage.py --timesheet PATH --rates PATH --out PATH
    python3 build_gp_slippage.py --emp-load 0.08 --base 30 --charge-default 39

Baseline (wk ending 30-08-2026): 1,381.75 h | rev $53,754.50 (avg $38.90/h)
    | labour $37,713.85 (avg $27.29/h) | GP $16,040.65 (29.8%) | slippage $11.61/h.
"""
import argparse, csv, glob, os, re, sys, difflib
from collections import defaultdict

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

TS_DIR = os.path.expanduser('~/Desktop/ASG - Timesheets')
DL_DIR = os.path.expanduser('~/Downloads')
DEFAULT_EXCLUDE = {'admin', 'asg guards'}
UNM = '(unmatched)'

# ---------------- name matching ----------------
def norm(s):
    s = str(s or '').lower().replace('★hd', '')
    s = re.sub(r'\s*-\s*waiheke( island)?', '', s)
    s = re.sub(r'[().]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    t = s.split()
    if len(t) >= 2 and len(t) % 2 == 0 and t[:len(t) // 2] == t[len(t) // 2:]:
        t = t[:len(t) // 2]  # collapse doubled full name ("Stanley laulu Stanley laulu")
    return ' '.join(t)


def load_rates(path):
    """Return (raw_lookup, norm_lookup). Records = (is_contractor, rate, raw_name)."""
    raw, nl = {}, defaultdict(list)
    with open(path, newline='', encoding='utf-8-sig') as f:
        for r in csv.reader(f):
            if not r or r[0].strip().lower() in ('contractor', ''):
                continue
            try:
                rate = float(r[2])
            except (ValueError, IndexError):
                continue
            rec = (r[0].strip().lower() == 'true', rate, r[1].strip())
            raw[r[1].strip().lower()] = rec
            nl[norm(r[1])].append(rec)
    return raw, nl


def make_lookup(raw, nl):
    names = list(nl.keys())

    def resolve(recs):
        con = [x for x in recs if x[0]]
        return con[0] if (len(recs) > 1 and con) else recs[0]

    def lookup(g):
        lg = str(g).strip().lower()
        if lg in raw:
            return raw[lg], 'raw'
        n = norm(g)
        if n in nl:
            return resolve(nl[n]), 'norm'
        m = difflib.get_close_matches(n, names, n=1, cutoff=0.90)
        if m:
            return resolve(nl[m[0]]), 'fuzzy'
        ns = set(n.split())
        cand = [a for a in names if ns and (ns <= set(a.split()) or set(a.split()) <= ns)
                and len(ns & set(a.split())) == min(len(ns), len(a.split()))]
        if len(cand) == 1:
            return resolve(nl[cand[0]]), 'subset'
        return None, 'none'
    return lookup


# ---------------- core compute ----------------
def compute(ts_path, rates_path, base, emp_load, charge_default, exclude):
    raw, nl = load_rates(rates_path)
    lookup = make_lookup(raw, nl)

    wb = openpyxl.load_workbook(ts_path, data_only=True)
    det = wb['Detail by Site & Date']
    detail = list(det.iter_rows(values_only=True))[1:]

    # per-person loaded rate
    workers = {str(g).strip() for s, d, g, r, h in detail
               if g and h is not None and str(s).strip().lower() not in exclude}
    prate, people = {}, []
    for g in workers:
        rec, how = lookup(g)
        if rec:
            is_con, b, raw_n = rec
            loaded = b * (1 if is_con else 1 + emp_load)
        else:
            is_con, b, raw_n, loaded = (True, base, UNM, base)
        prate[g] = loaded
        people.append((g, is_con, b, loaded, raw_n, how))

    # charge rates per site (Site Summary cols B/C)
    ss = wb['Site Summary']
    crate, disp = {}, {}
    for r in range(4, ss.max_row + 1):
        nm = ss.cell(row=r, column=1).value
        if not nm or str(nm).strip() == 'TOTAL' or str(nm).startswith('★'):
            continue
        crate[norm(nm)] = (ss.cell(row=r, column=2).value, ss.cell(row=r, column=3).value)
        disp[norm(nm)] = str(nm).replace('★HD', '').strip()

    def rr(x):
        return charge_default if (x is None or float(x) == 0) else float(x)

    site_hd = defaultdict(float); site_gu = defaultdict(float)
    site_cost = defaultdict(float); site_hrs = defaultdict(float); phrs = defaultdict(float)
    for s, d, g, role, h in detail:
        if h is None or g is None:
            continue
        k = norm(s)
        if k in exclude:
            continue
        h = float(h)
        (site_hd if str(role).strip() == 'HD' else site_gu)[k] += h
        site_hrs[k] += h
        site_cost[k] += h * prate.get(str(g).strip(), base)
        phrs[str(g).strip()] += h

    rows = []
    for k in site_hrs:
        b, c = crate.get(k, (None, None))
        rev = site_hd[k] * rr(b) + site_gu[k] * (rr(c) if (c and float(c) != 0) else rr(b))
        cost, t = site_cost[k], site_hrs[k]
        rows.append([disp.get(k, k), round(site_hd[k], 2), round(site_gu[k], 2), round(t, 2),
                     round(rev, 2), round(cost, 2), round(rev - cost, 2),
                     round((rev - cost) / t, 2), round((rev - cost) / rev * 100, 1) if rev else 0])
    rows.sort(key=lambda x: -x[7])
    return rows, people, phrs


# ---------------- workbook writer ----------------
NAVY, LIGHT, ALT, GREEN, RED = '1B2A4A', 'E8EDF5', 'F2F4F8', '27AE60', 'C0392B'
_thin = Side(style='thin', color='D0D5DD')
BD = Border(_thin, _thin, _thin, _thin)


def write_workbook(out, rows, people, phrs, week_label, base, emp_load, exclude):
    TH = sum(x[3] for x in rows); TR = sum(x[4] for x in rows)
    TC = sum(x[5] for x in rows); TG = TR - TC
    n_unm = sum(1 for p in people if p[4] == UNM)
    emp_h = sum(phrs.get(p[0], 0) for p in people if (not p[1]) and p[4] != UNM)
    unm_h = sum(phrs.get(p[0], 0) for p in people if p[4] == UNM)
    con_h = TH - emp_h - unm_h

    wb = openpyxl.Workbook()
    ws = wb.active; ws.title = 'GP by Site'
    ws.merge_cells('A1:I1')
    ws['A1'] = f'ASG — True Cost & Slippage (real pay rates) — {week_label} · Admin + ASG Guards excluded'
    ws['A1'].font = Font(bold=True, size=12, color=NAVY)
    for c, x in enumerate(['Client / Site', 'HD hrs', 'Guard hrs', 'Total hrs', 'Revenue $',
                           'Labour Cost $', 'GP $', 'Slippage $/hr', 'Margin %'], 1):
        cc = ws.cell(row=3, column=c, value=x)
        cc.font = Font(bold=True, color='FFFFFF', size=9); cc.fill = PatternFill('solid', fgColor=NAVY)
        cc.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True); cc.border = BD
    r = 4
    for row in rows:
        for c, v in enumerate(row, 1):
            cc = ws.cell(row=r, column=c, value=v); cc.border = BD; cc.font = Font(size=9)
            if r % 2 == 0:
                cc.fill = PatternFill('solid', fgColor=ALT)
            if c in (5, 6, 7, 8):
                cc.number_format = '$#,##0.00'
            if c == 8:
                cc.font = Font(size=9, bold=True, color=GREEN if v >= 10 else (RED if v < 7 else '000000'))
            if c == 9:
                cc.number_format = '0.0"%"'
        r += 1
    T = ['TOTAL', round(sum(x[1] for x in rows), 2), round(sum(x[2] for x in rows), 2), round(TH, 2),
         round(TR, 2), round(TC, 2), round(TG, 2), round(TG / TH, 2) if TH else 0,
         round(TG / TR * 100, 1) if TR else 0]
    for c, v in enumerate(T, 1):
        cc = ws.cell(row=r, column=c, value=v); cc.fill = PatternFill('solid', fgColor=LIGHT)
        cc.border = BD; cc.font = Font(bold=True, size=9)
        if c in (5, 6, 7, 8):
            cc.number_format = '$#,##0.00'
        if c == 9:
            cc.number_format = '0.0"%"'
    for col, w in zip('ABCDEFGHI', [30, 8, 9, 9, 12, 13, 12, 13, 10]):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = 'A4'

    # cost by person
    wsp = wb.create_sheet('Cost by Person')
    for c, x in enumerate(['Staff (timesheet)', 'Hours', 'Type', 'Base $/hr', 'Loaded $/hr',
                           'Cost $', 'Matched to', 'Match'], 1):
        cc = wsp.cell(row=1, column=c, value=x)
        cc.font = Font(bold=True, color='FFFFFF', size=9); cc.fill = PatternFill('solid', fgColor=NAVY); cc.border = BD
    pr = 2
    for g, is_con, b, loaded, raw_n, how in sorted(people, key=lambda x: -phrs.get(x[0], 0)):
        h = phrs.get(g, 0)
        typ = 'Unmatched' if raw_n == UNM else ('Contractor' if is_con else 'Employee')
        for c, v in enumerate([g, round(h, 2), typ, round(b, 2), round(loaded, 2),
                               round(h * loaded, 2), raw_n, how], 1):
            cc = wsp.cell(row=pr, column=c, value=v); cc.border = BD; cc.font = Font(size=9)
            if pr % 2 == 0:
                cc.fill = PatternFill('solid', fgColor=ALT)
            if c in (4, 5, 6):
                cc.number_format = '$#,##0.00'
            if c == 3 and v == 'Employee':
                cc.font = Font(size=9, bold=True, color='2C3E6B')
            if c == 3 and v == 'Unmatched':
                cc.font = Font(size=9, bold=True, color=RED)
        pr += 1
    for col, w in zip('ABCDEFGH', [30, 8, 11, 10, 11, 11, 28, 8]):
        wsp.column_dimensions[col].width = w
    wsp.freeze_panes = 'A2'

    # assumptions
    a = wb.create_sheet('Assumptions')
    L = [
        (f'ASG True-Cost / Slippage — {week_label} — assumptions & data quality', 1),
        ('', 0),
        (f'Pay rates from payroll export. Contractor=false => EMPLOYEE, +{emp_load*100:.0f}% '
         f'(holiday pay only). Contractor=true => no loading. Unmatched => ${base:.0f} fallback (contractor).', 0),
        (f'Match quality: {len(people)-n_unm}/{len(people)} staff matched; {n_unm} unmatched ({unm_h:.1f}h).', 0),
        (f'Hours split: contractor {con_h:.0f}h | employee {emp_h:.0f}h | unmatched {unm_h:.0f}h.', 0),
        (f'Excluded site rows: {", ".join(sorted(exclude))}. '
         f'Revenue = charge rates (Site Summary B/C) x actual HD/Guard hours.', 0),
        ('SLIPPAGE = charge - real labour cost per billed hour = GROSS margin, BEFORE overhead '
         '(management, insurance, vehicles, ACC, non-billable/travel, bad debt).', 0),
        (f'NOTE: {emp_load*100:.0f}% covers holiday pay only; a fully-compliant NZ on-cost '
         '(KiwiSaver 3% + ACC + sick/public-holiday leave) would add several % more if payable.', 0),
        ('', 0),
        (f'WEEK TOTAL: {TH:,.2f} billable hrs | revenue ${TR:,.2f} (avg ${TR/TH:.2f}/hr) | '
         f'labour ${TC:,.2f} (avg ${TC/TH:.2f}/hr) | GP ${TG:,.2f} ({TG/TR*100:.1f}%) | '
         f'slippage ${TR/TH-TC/TH:.2f}/hr', 1),
    ]
    for i, (t, b) in enumerate(L, 1):
        a.cell(row=i, column=1, value=t).font = Font(bold=bool(b), size=11 if b else 9,
                                                     color=NAVY if b else '000000')
    a.column_dimensions['A'].width = 125
    wb.save(out)
    return TH, TR, TC, TG, len(people) - n_unm, len(people), n_unm, emp_h, con_h, unm_h


# ---------------- file resolution ----------------
def latest(pattern):
    files = glob.glob(pattern)
    return max(files, key=os.path.getmtime) if files else None


def week_label_from(ts_path):
    m = re.search(r'(\d{2}-\d{2}-\d{4})', os.path.basename(ts_path))
    return f'Week ending {m.group(1)}' if m else os.path.basename(ts_path)


def main():
    ap = argparse.ArgumentParser(description='ASG weekly GP / slippage builder')
    ap.add_argument('--timesheet', help='Timesheet xlsx (default: latest in ~/Desktop/ASG - Timesheets)')
    ap.add_argument('--rates', help='Payroll rates CSV (default: latest New_Report*.csv in ~/Downloads)')
    ap.add_argument('--out', help='Output xlsx (default: "ASG GP - <week>.xlsx" beside the timesheet)')
    ap.add_argument('--base', type=float, default=30.0, help='Fallback pay rate for unmatched staff (default 30)')
    ap.add_argument('--emp-load', type=float, default=0.08, help='Employee on-cost loading (default 0.08)')
    ap.add_argument('--charge-default', type=float, default=39.0, help='Charge rate where B/C is 0/blank (default 39)')
    ap.add_argument('--exclude', default='admin,asg guards', help='Comma-separated site rows to exclude')
    args = ap.parse_args()

    ts = args.timesheet or latest(os.path.join(TS_DIR, 'Timesheet - Weekending - *.xlsx'))
    rates = args.rates or latest(os.path.join(DL_DIR, 'New_Report*.csv'))
    if not ts or not os.path.exists(ts):
        sys.exit('ERROR: no timesheet found. Pass --timesheet PATH.')
    if not rates or not os.path.exists(rates):
        sys.exit('ERROR: no rates CSV found. Pass --rates PATH.')
    exclude = {s.strip().lower() for s in args.exclude.split(',') if s.strip()}
    week = week_label_from(ts)
    out = args.out or os.path.join(os.path.dirname(ts), f'ASG GP - {week.replace("Week ending ", "Weekending ")}.xlsx')

    print(f'Timesheet : {ts}')
    print(f'Rates     : {rates}')
    rows, people, phrs = compute(ts, rates, args.base, args.emp_load, args.charge_default, exclude)
    TH, TR, TC, TG, nm, ntot, nunm, emp_h, con_h, unm_h = write_workbook(
        out, rows, people, phrs, week, args.base, args.emp_load, exclude)

    print(f'Matched   : {nm}/{ntot} staff ({nunm} unmatched -> ${args.base:.0f})')
    print(f'Hours     : {TH:,.2f}  (contractor {con_h:.0f}h | employee {emp_h:.0f}h | unmatched {unm_h:.0f}h)')
    print(f'Revenue   : ${TR:,.2f}   (avg charge ${TR/TH:.2f}/hr)')
    print(f'Labour    : ${TC:,.2f}   (avg cost   ${TC/TH:.2f}/hr)')
    print(f'GP        : ${TG:,.2f}   ({TG/TR*100:.1f}%)   |   SLIPPAGE ${TR/TH-TC/TH:.2f}/hr')
    print(f'WROTE     : {out}')


if __name__ == '__main__':
    main()
