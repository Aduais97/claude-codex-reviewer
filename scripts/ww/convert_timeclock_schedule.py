#!/usr/bin/env python3
"""Convert a Connecteam 'timeclock-timesheet_overview_*.xlsx' (ACTUAL worked hours) into the
Schedule-Export shape the FY27 WW pipeline reads (Date, Start, End, Job, Users).

Actual timesheet hours SUPERSEDE the planned roster/schedule as the authoritative deployment
hours (Ahmad, 2 Aug 2026 — "these are the actual timesheets, make sure everything up to this
amount"). Each WW deployment shift is emitted so that End-Start == the timesheet 'Shift hours'
value EXACTLY (Start '0:00', End = the shift-hours duration), so the pipeline's per-store hours
total reconciles to the timeclock to the minute.

WW scope (Ahmad, 3 Aug 2026): every '<store> Woolworths' Type. EXCLUDE leave (Sick/Annual),
Flaxmere/Hastings ("remove flaxmere"; Hastings = same store mis-tagged). Travel is EXCLUDED
except for the WELLINGTON team ("include travel for wellington team only") — Wellington guards
travel between spread-out stores, so that time is deployment. Team/Zone (col 4) gives the region.
Wellington travel is relabelled 'Wellington Team Transit Woolworths' so it passes the pipeline's
store filter (has 'woolworth', no 'travel' word) and counts in the hours total.

Usage: python3 convert_timeclock_schedule.py "<timeclock.xlsx>" "<out Schedule-Export.xlsx>"
"""
import sys, openpyxl
from datetime import datetime

def classify(t, tz):
    """Return the Job to emit for this shift, or None to drop it."""
    tl = t.lower()
    if 'leave' in tl or 'flaxmere' in tl or 'hastings' in tl:
        return None
    if 'travel' in tl:
        # Wellington-team travel between spread-out WW stores is deployment and counts.
        # EXCLUDE: non-Wellington travel, and any non-Woolworths contract trip (e.g. SLS RTC)
        # that must not inflate the Woolworths client's hours (keep client data siloed).
        if 'slsrtc' in tl or 'sls rtc' in tl:
            return None
        # startswith (not ==) so a long region form like "Wellington Region" still matches.
        return "Wellington Team Transit Woolworths" if tz.strip().lower().startswith('wellington') else None
    return t if 'woolworth' in tl else None

def hm(h):
    m = round(h * 60)
    return f"{m // 60}:{m % 60:02d}"

def convert(src, out):
    ws = openpyxl.load_workbook(src, read_only=True)['All Employees']
    rows = list(ws.iter_rows(values_only=True))
    H = [str(h or '') for h in rows[0]]
    c_type, c_sd, c_sh = H.index('Type'), H.index('Start Date'), H.index('Shift hours')
    # name + team/zone are grouped (only on the first row of each employee block) — carry them forward
    c_fn, c_ln, c_tz = H.index('First name'), H.index('Last name'), H.index('Team / Zone')
    ob = openpyxl.Workbook(); o = ob.active; o.title = "Schedule"
    o.append(["Date", "Start", "End", "Job", "Users"])
    name = ""; tz = ""; n = 0
    for r in rows[1:]:
        fn = str(r[c_fn] or '').strip(); ln = str(r[c_ln] or '').strip()
        if fn or ln:
            name = f"{fn} {ln}".strip(); tz = str(r[c_tz] or '').strip()
        t = str(r[c_type] or '').strip(); d = r[c_sd]
        try:
            h = float(r[c_sh])
        except (TypeError, ValueError):
            h = 0.0
        if h > 11:            # >11h in a day = missed clock-out; cap to 9h (Ahmad, W6, 10 Aug 2026)
            h = 9.0
        if not t or not isinstance(d, datetime) or h <= 0:
            continue
        job = classify(t, tz)
        if job is None:
            continue
        o.append([d.strftime("%m/%d/%Y"), "0:00", hm(h), job, name])
        n += 1
    ob.save(out)
    print(f"wrote {n} WW shift rows -> {out}")

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
