#!/usr/bin/env python3
"""Convert a Connecteam 'timeclock-tag-sheet <range>.xlsx' (hours AGGREGATED by job/store for the
week, no per-shift dates) into the Schedule-Export shape the FY27 WW pipeline reads.

Some weeks the hours arrive as a tag-sheet (All Jobs sheet: Job | Sub item | Performed by | Num of
shifts | Hours | Pay) rather than the per-shift timeclock-timesheet_overview. This has hours per
STORE (the store-header rows carry the weekly total) but no dates or In/Out — so we emit one row
per WW store, dated to a date INSIDE the pay week, with End = the store's total hours. The pipeline
sums by store, so per-store & network totals reconcile to the tag-sheet. NOTE: the >11h/shift cap
does NOT apply here (these are weekly store aggregates, not individual shifts).

WW scope: keep '<store> Woolworths'; drop Flaxmere/Hastings, leave, and generic 'Travel ...' jobs
(the tag-sheet carries no Team/Zone, so Wellington-team travel can't be isolated — it is tiny anyway).

Usage: python3 convert_tagsheet_schedule.py "<tag-sheet.xlsx>" "<out Schedule-Export.xlsx>" <MM/DD/YYYY in-week>
"""
import sys, openpyxl

def classify(job):
    jl = job.lower()
    if 'flaxmere' in jl or 'hastings' in jl or 'leave' in jl: return None
    if 'travel' in jl: return None
    return job if 'woolworth' in jl else None

def hm(h):
    m = round(float(h) * 60)
    return f"{m // 60}:{m % 60:02d}"

def convert(src, out, date):
    ws = openpyxl.load_workbook(src, data_only=True).active
    rows = list(ws.iter_rows(values_only=True))
    H = [str(c or '').strip().lower() for c in rows[0]]
    ji, hi = H.index('job'), H.index('hours')
    ob = openpyxl.Workbook(); o = ob.active; o.title = "Schedule"
    o.append(["Date", "Start", "End", "Job", "Users"])
    n = 0; tot = 0.0
    for r in rows[1:]:
        job = r[ji]
        if job in (None, ''):     # guard sub-row — skip; the store-header row carries the weekly total
            continue
        try: h = float(r[hi])
        except (TypeError, ValueError): continue
        if h <= 0: continue
        j = classify(str(job).strip())
        if j is None: continue
        o.append([date, "0:00", hm(h), j, ""]); n += 1; tot += h
    ob.save(out)
    print(f"wrote {n} WW store rows, {tot:.2f}h (dated {date}) -> {out}")

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "08/13/2026")
