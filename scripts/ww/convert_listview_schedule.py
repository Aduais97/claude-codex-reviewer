#!/usr/bin/env python3
"""Convert a Connecteam 'list-view' roster export into the Schedule-Export shape the
FY27 WW pipeline expects (columns: Date, Start, End, Job, Users).

The list-view export groups the Job (store) column (only populated on the first row of
each store block) and carries times as a single 'Set times' cell like '09:00 > 12:30 (...)'.
This forward-fills Job, splits Set times into Start/End, drops unfilled 'Open shift' rows
(no guard deployed => no deployment hours), and writes a clean Schedule-Export xlsx.

Usage: python3 convert_listview_schedule.py "<list-view.xlsx>" "<out Schedule-Export.xlsx>"
"""
import sys, re, openpyxl

def convert(src, out):
    wb = openpyxl.load_workbook(src, read_only=True)
    rows = list(wb["Sheet 1"].iter_rows(values_only=True))
    hdr = [str(h or "") for h in rows[0]]
    ci = {name: i for i, name in enumerate(hdr)}
    JOB, USERS, DATE, SET = ci["Job"], ci["Users"], ci["Date"], ci["Set times"]

    ob = openpyxl.Workbook(); ws = ob.active; ws.title = "Schedule"
    ws.append(["Date", "Start", "End", "Job", "Users"])
    job = None; n = 0; skipped_open = 0
    for r in rows[1:]:
        if r[JOB] and str(r[JOB]).strip():
            job = str(r[JOB]).strip()
        user = str(r[USERS] or "").strip()
        st = str(r[SET] or "").strip()
        date = str(r[DATE] or "").strip()
        m = re.match(r"(\d{1,2}:\d{2})\s*>\s*(\d{1,2}:\d{2})", st)
        if not (job and date and m):
            continue
        if not user or user.lower() == "open shift":   # unfilled shift => not deployed
            skipped_open += 1
            continue
        ws.append([date, m.group(1), m.group(2), job, user]); n += 1
    ob.save(out)
    print(f"wrote {n} shift rows -> {out}  (skipped {skipped_open} unfilled 'Open shift' rows)")

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
