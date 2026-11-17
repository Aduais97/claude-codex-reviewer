#!/usr/bin/env python3
"""
Woolworths Master Data — v2 (region-grouped, self-reconciling), fresh from 01 Jun 2026.

Rebuilds the weekly master from the full-year source exports so every figure is
internally consistent (fixes the old file's silent packaging drift, corrupted
header dates, and broken YTD). Four sheets:

  1. National Summary   — weekly national rollup + YTD (headline = Total Loss)
  2. Region Summary     — same metrics, one block per region (grouped-by-region)
  3. Store Comparison   — every store, grouped under its region, + region subtotals
  4. Reconciliation     — asserts stores == regions == national, every week

Run:  python3 build_master_v2.py
"""
import os, re, sys
from datetime import datetime, timedelta
from collections import defaultdict
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L

D = os.path.expanduser("~/Downloads")

# Source exports per stream. Each entry: (path, incident-date lower bound, upper bound),
# bounds INCLUSIVE (None = open). Bounds split overlapping exports so each incident is
# counted exactly once. Columns are resolved by HEADER NAME (positions differ per export).
GIR_SOURCES = [
    (f"{D}/Woolworths _ Guard Incident Report_c825cc65-4f04-47bf-b60c-57e23f7026ea.xlsx", None, datetime(2026, 6, 30)),
    (f"{D}/Woolworths _ Guard Incident Report_3f88efe3-fcd2-46e8-b223-101972193adf.xlsx", datetime(2026, 7, 1), datetime(2026, 7, 5)),   # W1
    (f"{D}/Woolworths _ Guard Incident Report_4144a886-50ea-4ca9-a8e7-3bdc8fa738b8.xlsx", datetime(2026, 7, 6), datetime(2026, 7, 12)), # W2
    (f"{D}/Woolworths _ Guard Incident Report_8f7cb974-8f1f-41b7-9ee4-8321ce476506.xlsx", datetime(2026, 7, 13), datetime(2026, 7, 19)), # W3 (a late-submitted 3-Jul row id 11797 is bounded out — W1 stays as sent)
    (f"{D}/Woolworths _ Guard Incident Report_010e9b32-250a-4c1f-b4a8-5ea3092f8113.xlsx", datetime(2026, 7, 20), datetime(2026, 7, 26)), # W4
    (f"{D}/Woolworths _ Guard Incident Report_0e1a1fc6-0a76-4685-8310-8b43f8a1a501.xlsx", datetime(2026, 7, 27), datetime(2026, 8, 2)),  # W5 (27 Jul-2 Aug)
    (f"{D}/Woolworths _ Guard Incident Report_14caeadb-85bd-42fd-83d5-8adec9ed45e5.xlsx", datetime(2026, 8, 3), datetime(2026, 8, 9)),     # W6 (3-9 Aug; 30 Jul-9 Aug window bounded)
    (f"{D}/Woolworths _ Guard Incident Report_a3b71305-8dcf-472d-a624-5fe33e277437.xlsx", datetime(2026, 8, 10), datetime(2026, 8, 16)),  # W7 (10-16 Aug)
    (f"{D}/Woolworths _ Guard Incident Report_84187d88-d86e-49a5-9dd5-8e1b79252efb.xlsx", datetime(2026, 8, 17), datetime(2026, 8, 23)),   # W8 (17-23 Aug)
    (f"{D}/Woolworths _ Guard Incident Report_16fe7a18-4490-4908-ae24-0cbdb5a834b0.xlsx", datetime(2026, 8, 24), datetime(2026, 8, 30)),  # W9 (24-30 Aug)
    (f"{D}/Woolworths _ Guard Incident Report_082fe552-5fa4-447a-9064-72dcf13f5d1b.xlsx", datetime(2026, 8, 31), datetime(2026, 9, 6)),   # W10 (31 Aug-6 Sep) — capped
    (f"{D}/Woolworths _ Guard Incident Report_dfacf58c-2714-4fe4-81aa-62b5fcdbd0dc.xlsx", datetime(2026, 9, 7), datetime(2026, 9, 27)),  # W11-W13 (7-27 Sep broad re-export)
    (f"{D}/Woolworths _ Guard Incident Report_79e44d5c-a7d4-433c-844f-7cbd5266b0aa.xlsx", datetime(2026, 9, 28), datetime(2026, 10, 4)),  # W14 (28 Sep-4 Oct)
    (f"{D}/Woolworths _ Guard Incident Report_MANUAL-W14-Greenlane.xlsx", datetime(2026, 9, 28), datetime(2026, 10, 4)),  # W14 manual add (Greenlane report not logged in Connecteam)
    (f"{D}/Woolworths _ Guard Incident Report_6b892b4c-3a2d-46d4-9091-3057d04ea7ca.xlsx", datetime(2026, 10, 5), datetime(2026, 10, 11)),  # W15 (5-11 Oct)
    (f"{D}/Woolworths _ Guard Incident Report_06d38edb-75a8-455c-a97b-05ef9d165e1f.xlsx", datetime(2026, 10, 12), datetime(2026, 10, 18)),  # W16 (12-18 Oct)
    (f"{D}/Woolworths _ Guard Incident Report_ab3890f3-00bf-477f-b0dd-4a9fbfd13eee.xlsx", datetime(2026, 10, 19), datetime(2026, 10, 25)),  # W17 (19-25 Oct)
    (f"{D}/Woolworths _ Guard Incident Report_555db30a-2d25-4500-92cc-cb8566fa04f2.xlsx", datetime(2026, 10, 26), datetime(2026, 11, 1)),  # W18 (26 Oct-1 Nov)
    (f"{D}/Woolworths _ Guard Incident Report_2ff92e5e-b0c3-4e8a-b5b1-2dae4ecd039c.xlsx", datetime(2026, 11, 2), datetime(2026, 11, 8)),  # W19 (2-8 Nov)
    (f"{D}/Woolworths _ Guard Incident Report_b2928bc5-928c-4fee-afe7-e6bede09a32a.xlsx", datetime(2026, 11, 9), datetime(2026, 11, 15)),  # W20 (9-15 Nov)
]
PKG_SOURCES = [
    (f"{D}/Woolworths _ Recovered Packaging_a42b0810-42bc-430e-83c4-02017db4c98b.xlsx", None, datetime(2026, 6, 30)),
    (f"{D}/Woolworths _ Recovered Packaging_3641b511-7e80-4e7a-8b1f-d0e686b8dab8.xlsx", datetime(2026, 7, 1), datetime(2026, 7, 5)),    # W1
    (f"{D}/Woolworths _ Recovered Packaging_9fb11235-3870-44d5-a3c2-468d2e511093.xlsx", datetime(2026, 7, 6), datetime(2026, 7, 12)),   # W2
    (f"{D}/Woolworths _ Recovered Packaging_45c16d06-005b-46c6-a36b-4d92628792ce.xlsx", datetime(2026, 7, 13), datetime(2026, 7, 19)),  # W3
    (f"{D}/Woolworths _ Recovered Packaging_bba87fae-e74f-4b31-ba0e-ec4866fdbd21.xlsx", datetime(2026, 7, 20), datetime(2026, 7, 26)),  # W4
    (f"{D}/Woolworths _ Recovered Packaging_9cdb68af-be84-4e56-b4de-39d704599495.xlsx", datetime(2026, 7, 27), datetime(2026, 8, 2)),  # W5
    (f"{D}/Woolworths _ Recovered Packaging_c8cffc68-1f34-4338-8e2b-47dce3f2d207.xlsx", datetime(2026, 8, 3), datetime(2026, 8, 9)),     # W6 (3-9 Aug)
    (f"{D}/Woolworths _ Recovered Packaging_f6abbe5a-d591-45ca-9a6e-4071a3d70429.xlsx", datetime(2026, 8, 10), datetime(2026, 8, 16)),  # W7 (10-16 Aug)
    (f"{D}/Woolworths _ Recovered Packaging_7cab9913-6fcd-46c1-a3e0-927cd7bdf475.xlsx", datetime(2026, 8, 17), datetime(2026, 8, 23)),   # W8 (17-23 Aug)
    (f"{D}/Woolworths _ Recovered Packaging_a2d87d8d-128c-4eef-a7ea-459741904ea3.xlsx", datetime(2026, 8, 24), datetime(2026, 8, 30)),  # W9 (24-30 Aug)
    (f"{D}/Woolworths _ Recovered Packaging_fdac6322-49f3-4e20-8c33-0bfde99c3d56.xlsx", datetime(2026, 8, 31), datetime(2026, 9, 6)),   # W10 (31 Aug-6 Sep) — capped
    (f"{D}/Woolworths _ Recovered Packaging_ab3aac86-ed86-4d6d-8018-22641273833f.xlsx", datetime(2026, 9, 7), datetime(2026, 9, 27)),  # W11-W13 (7-27 Sep broad re-export)
    (f"{D}/Woolworths _ Recovered Packaging_c10d4659-b834-427c-b2ea-c8209c62b1a7.xlsx", datetime(2026, 9, 28), datetime(2026, 10, 4)),  # W14 (28 Sep-4 Oct)
    (f"{D}/Woolworths _ Recovered Packaging_e7fe588b-5e71-4574-bc9d-b9f4b3075869.xlsx", datetime(2026, 10, 5), datetime(2026, 10, 11)),  # W15 (5-11 Oct)
    (f"{D}/Woolworths _ Recovered Packaging_0e3c3e7d-7497-4b97-a62a-a74312cadbb0.xlsx", datetime(2026, 10, 12), datetime(2026, 10, 18)),  # W16 (12-18 Oct)
    (f"{D}/Woolworths _ Recovered Packaging_59285172-f61c-457c-aabb-42cf4398690f.xlsx", datetime(2026, 10, 19), datetime(2026, 10, 25)),  # W17 (19-25 Oct)
    (f"{D}/Woolworths _ Recovered Packaging_0cc0a2f2-2893-4984-bc60-933a252ea310.xlsx", datetime(2026, 10, 26), datetime(2026, 11, 1)),  # W18 (26 Oct-1 Nov)
    (f"{D}/Woolworths _ Recovered Packaging_100630be-7a6e-4d77-a479-221135b38910.xlsx", datetime(2026, 11, 2), datetime(2026, 11, 8)),  # W19 (2-8 Nov)
    (f"{D}/Woolworths _ Recovered Packaging_d4f5cc27-123c-40b2-8ae9-7ddc576f1999.xlsx", datetime(2026, 11, 9), datetime(2026, 11, 15)),  # W20 (9-15 Nov)
]
DET_SOURCES = [
    (f"{D}/Woolworths _ Guard Deterent  Report_a53b9b34-b6b2-45aa-ab48-04a7ada46008.xlsx", None, datetime(2026, 6, 30)),
    (f"{D}/Woolworths _ Guard Deterent  Report_e64171b5-9c89-42eb-b8b8-6148f5066b0e.xlsx", datetime(2026, 7, 1), datetime(2026, 7, 5)), # W1
    (f"{D}/Woolworths _ Guard Deterent  Report_a778f582-9ba3-4e59-8b36-dcc76c8bd094.xlsx", datetime(2026, 7, 6), datetime(2026, 7, 12)), # W2 (form only 6-9 Jul; sent as floor 13)
    (f"{D}/Woolworths _ Guard Deterent  Report_cc8568e2-cc01-4294-a4d6-deb965c251cd.xlsx", datetime(2026, 7, 13), datetime(2026, 7, 19)), # W3 (form lags: nothing after Fri 17 yet — FLOOR; late 30-Jun/6-7-Jul rows bounded out)
    (f"{D}/Woolworths _ Guard Deterent  Report_33f18380-9ee9-47a8-807e-bd75cd150075.xlsx", datetime(2026, 7, 20), datetime(2026, 7, 26)), # W4
    (f"{D}/Woolworths _ Guard Deterent  Report_83fb8471-dfc9-42a6-a9d4-046e1ab4d5cf.xlsx", datetime(2026, 7, 27), datetime(2026, 8, 2)),  # W5
    (f"{D}/Woolworths _ Guard Deterent  Report_dc0055e1-14db-4c6a-9c59-664969fab1f3.xlsx", datetime(2026, 8, 3), datetime(2026, 8, 9)),    # W6 (3-9 Aug)
    (f"{D}/Woolworths _ Guard Deterent  Report_74b9b795-d571-4856-bba3-9200e67b094a.xlsx", datetime(2026, 8, 10), datetime(2026, 8, 16)),  # W7 (10-16 Aug)
    (f"{D}/Woolworths _ Guard Deterent  Report_a8b3b97d-9b10-49ac-abde-8e5a7561d033.xlsx", datetime(2026, 8, 17), datetime(2026, 8, 23)),  # W8 (17-23 Aug)
    (f"{D}/Woolworths _ Guard Deterent  Report_f9ca5cd8-d0e6-4a32-84be-b495322c83f4.xlsx", datetime(2026, 8, 24), datetime(2026, 8, 30)), # W9 (24-30 Aug)
    (f"{D}/Woolworths _ Guard Deterent  Report_89b3efde-ca9a-4654-802e-8c0e908ad8c3.xlsx", datetime(2026, 8, 31), datetime(2026, 9, 6)),  # W10 (31 Aug-6 Sep) — capped
    (f"{D}/Woolworths _ Guard Deterent  Report_0efbfee7-63fe-4d83-a723-4443260b793a.xlsx", datetime(2026, 9, 7), datetime(2026, 9, 27)),  # W11-W13 (7-27 Sep broad re-export)
    (f"{D}/Woolworths _ Guard Deterent  Report_db300736-1e32-4573-a98c-73b359685be3.xlsx", datetime(2026, 9, 28), datetime(2026, 10, 4)), # W14 (28 Sep-4 Oct)
    (f"{D}/Woolworths _ Guard Deterent  Report_2f0d1c6e-1ea9-4476-bccf-c35e9cb03eff.xlsx", datetime(2026, 10, 5), datetime(2026, 10, 11)), # W15 (5-11 Oct)
    (f"{D}/Woolworths _ Guard Deterent  Report_6db99d07-6bdc-49fa-b0d9-b07c8ddcabd0.xlsx", datetime(2026, 10, 12), datetime(2026, 10, 18)), # W16 (12-18 Oct)
    (f"{D}/Woolworths _ Guard Deterent  Report_dade4315-1f21-4512-b052-ab9a4b0b0775.xlsx", datetime(2026, 10, 19), datetime(2026, 10, 25)), # W17 (19-25 Oct)
    (f"{D}/Woolworths _ Guard Deterent  Report_7ed9b0df-aa6b-4023-8c93-230bcbabf5ef.xlsx", datetime(2026, 10, 26), datetime(2026, 11, 1)), # W18 (26 Oct-1 Nov)
    (f"{D}/Woolworths _ Guard Deterent  Report_faf3b67d-b835-4ab5-a30a-f911f21c77e6.xlsx", datetime(2026, 11, 2), datetime(2026, 11, 8)), # W19 (2-8 Nov)
    (f"{D}/Woolworths _ Guard Deterent  Report_b4c4ca4d-530c-4bdf-8fca-2366a86c4544.xlsx", datetime(2026, 11, 9), datetime(2026, 11, 15)), # W20 (9-15 Nov)
]

OUT = os.path.expanduser("~/Desktop/Woolworths /Woolworths Master Data FY27.xlsx")

# FY27 = from 01 Jul 2026. Weeks are explicit (start, end) INCLUSIVE incident-date ranges,
# keyed/headed by the week-ENDING date. W1 is a partial (Wed 1 Jul -> Sun 5 Jul) matching
# WW's historical pattern (FY W1 runs 1 Jul -> first Sunday); thereafter Mon-Sun.
# Append one tuple per week going forward.
WEEK_DEFS = [
    (datetime(2026, 7, 1), datetime(2026, 7, 5)),    # W1  (1-5 Jul, partial first FY week)
    (datetime(2026, 7, 6), datetime(2026, 7, 12)),   # W2  (6-12 Jul, first full week)
    (datetime(2026, 7, 13), datetime(2026, 7, 19)),  # W3  (13-19 Jul)
    (datetime(2026, 7, 20), datetime(2026, 7, 26)),  # W4  (20-26 Jul)
    (datetime(2026, 7, 27), datetime(2026, 8, 2)),   # W5  (27 Jul-2 Aug)
    (datetime(2026, 8, 3), datetime(2026, 8, 9)),    # W6  (3-9 Aug)
    (datetime(2026, 8, 10), datetime(2026, 8, 16)),  # W7  (10-16 Aug)
    (datetime(2026, 8, 17), datetime(2026, 8, 23)),  # W8  (17-23 Aug)
    (datetime(2026, 8, 24), datetime(2026, 8, 30)),  # W9  (24-30 Aug)
    (datetime(2026, 8, 31), datetime(2026, 9, 6)),   # W10 (31 Aug-6 Sep)
    (datetime(2026, 9, 7), datetime(2026, 9, 13)),   # W11 (7-13 Sep)
    (datetime(2026, 9, 14), datetime(2026, 9, 20)),  # W12 (14-20 Sep)
    (datetime(2026, 9, 21), datetime(2026, 9, 27)),  # W13 (21-27 Sep)
    (datetime(2026, 9, 28), datetime(2026, 10, 4)),  # W14 (28 Sep-4 Oct)
    (datetime(2026, 10, 5), datetime(2026, 10, 11)), # W15 (5-11 Oct)
    (datetime(2026, 10, 12), datetime(2026, 10, 18)), # W16 (12-18 Oct)
    (datetime(2026, 10, 19), datetime(2026, 10, 25)), # W17 (19-25 Oct)
    (datetime(2026, 10, 26), datetime(2026, 11, 1)),  # W18 (26 Oct-1 Nov; incl. Labour Day Mon 26 Oct)
    (datetime(2026, 11, 2), datetime(2026, 11, 8)),   # W19 (2-8 Nov)
    (datetime(2026, 11, 9), datetime(2026, 11, 15)),  # W20 (9-15 Nov)
]
WEEKS = [end for (start, end) in WEEK_DEFS]           # column key + header = week-ending date

# Hours source per week, keyed by week-ending date.
# ★ From 3 Aug 2026: ACTUAL worked hours from the Connecteam timeclock supersede the planned
# roster/schedule (Ahmad: "these are the actual timesheets, make sure everything up to this amount").
# ONE timeclock-derived Schedule-Export covers the whole FY-to-date; each week filters to its own
# dates. Built via convert_timeclock_schedule.py (exact 'Shift hours'; Flaxmere/Hastings removed;
# travel counted for the Wellington team only). Rebuild that file when a fresh timeclock export lands.
_ACTUAL = "Schedule-Export ACTUAL 2026-07-01 to 2026-08-02.xlsx"
WEEK_SCHEDULE = {
    datetime(2026, 7, 5):  _ACTUAL,
    datetime(2026, 7, 12): _ACTUAL,
    datetime(2026, 7, 19): _ACTUAL,
    datetime(2026, 7, 26): _ACTUAL,
    datetime(2026, 8, 2):  _ACTUAL,
    datetime(2026, 8, 9):  "Schedule-Export ACTUAL 2026-08-03 to 2026-08-09.xlsx",  # W6 (capped >11h→9h)
    datetime(2026, 8, 16): "Schedule-Export ACTUAL 2026-08-10 to 2026-08-16.xlsx",  # W7 (tag-sheet: weekly store aggregates, no >11h cap)
    datetime(2026, 8, 23): "Schedule-Export ACTUAL 2026-08-17 to 2026-08-23.xlsx",  # W8 (tag-sheet: weekly store aggregates)
    datetime(2026, 8, 30): "Schedule-Export ACTUAL 2026-08-24 to 2026-08-30.xlsx",  # W9 (timeclock: leave excluded, >11h→9h)
    datetime(2026, 9, 6):  "Schedule-Export ACTUAL 2026-08-31 to 2026-09-06.xlsx",  # W10 (timeclock: leave excluded)
    datetime(2026, 9, 13): "Schedule-Export ACTUAL 2026-08-31 to 2026-09-27.xlsx",  # W11 (broad timeclock 31 Aug-27 Sep, week-filtered; >11h→9h)
    datetime(2026, 9, 20): "Schedule-Export ACTUAL 2026-08-31 to 2026-09-27.xlsx",  # W12 (same broad export)
    datetime(2026, 9, 27): "Schedule-Export ACTUAL 2026-08-31 to 2026-09-27.xlsx",  # W13 (same broad export)
    datetime(2026, 10, 4): "Schedule-Export ACTUAL 2026-09-28 to 2026-10-04.xlsx",  # W14 (timeclock actual hours)
    datetime(2026, 10, 11): "Schedule-Export ACTUAL 2026-10-05 to 2026-10-11.xlsx",  # W15 (timeclock actual hours)
    datetime(2026, 10, 18): "Schedule-Export ACTUAL 2026-10-12 to 2026-10-18.xlsx",  # W16 (timeclock actual hours)
    datetime(2026, 10, 25): "Schedule-Export ACTUAL 2026-10-19 to 2026-10-25.xlsx",  # W17 (timeclock actual hours)
    datetime(2026, 11, 1): "Schedule-Export ACTUAL 2026-10-26 to 2026-11-01.xlsx",  # W18 (timeclock actual hours; Labour Day week)
    datetime(2026, 11, 8): "Schedule-Export ACTUAL 2026-11-02 to 2026-11-08.xlsx",  # W19 (timeclock actual hours)
    datetime(2026, 11, 15): "Schedule-Export ACTUAL 2026-11-09 to 2026-11-15.xlsx",  # W20 (timeclock actual hours)
}
CURRENT_WEEK = WEEKS[-1]                               # the week the client package reports on
def week_start(week):  return next(s for (s, e) in WEEK_DEFS if e == week)
def week_num(week):    return WEEKS.index(week) + 1
def week_label(week):  return f"{week.day} {week.strftime('%B %Y')}"   # e.g. "12 July 2026"
def is_partial(week):  return week == WEEKS[0]         # only W1 (1 Jul start) is a partial week
def schedule_for(week=None):
    return os.path.expanduser(f"~/Downloads/{WEEK_SCHEDULE[week or CURRENT_WEEK]}")

# Per-week context notes (e.g. public-holiday short weeks) shown on the client report so a
# reduced-day week doesn't read as underperformance. Keyed by week-ending date.
WEEK_NOTES = {
    datetime(2026, 7, 12): "6-day operating week — Matariki public holiday (Fri 10 Jul), no covert deployment",
}
def week_note(week=None): return WEEK_NOTES.get(week or CURRENT_WEEK, "")

def _norm_desc(s):
    return " ".join(str(s or "").lower().split())


def dup_seen(seen, site, d, rec, off, desc):
    """Permanent GIR de-duplication. Returns True if this incident row duplicates one already
    counted — same store + date + recovered-$ + offender-count AND >=0.90 description similarity
    (a double-submission of the same report). Distinct incidents that merely share a $ amount are
    KEPT (their descriptions differ). Added 4 Oct 2026 (Ahmad: 'keep all de-dupe as truth going forward')."""
    import difflib
    key = (site, str(d), round(rec, 2), off)
    nd = _norm_desc(desc)
    for prev in seen.get(key, []):
        if difflib.SequenceMatcher(None, nd, prev).ratio() >= 0.90:
            return True
    seen.setdefault(key, []).append(nd)
    return False


def week_incidents(week=None):
    """Incident-level rows for a week (client highlights). Non-deterrent GIR rows with
    store, recovered $, recovery type, product, offender count, police/trespass flags."""
    week = week or CURRENT_WEEK
    T = {"date": "Date and Time of Incident - Date", "site": "Select Woolworths Site",
         "cat": "Incident Category", "rec": "Recovered Reciept Value", "type": "Type of recovery",
         "prod": "General Product Categories Targeted", "off": "Number of offenders/POI",
         "police": "Were the police informed?", "vt": "Verbal Trespass", "ft": "Formal Trespass Notice Served",
         "desc": "Incident Description"}
    def cl(s): return " ".join(str(s).split()).strip() if s else ""
    out = []; wi_seen = {}
    for path, lo, hi in GIR_SOURCES:
        wb = openpyxl.load_workbook(path, read_only=True); ws = wb.active
        it = ws.iter_rows(values_only=True); header = list(next(it))
        low = [str(h).strip().lower() if h else "" for h in header]
        col = {}
        for k, name in T.items():
            nl = name.strip().lower()
            col[k] = next((i for i, h in enumerate(low) if h == nl),
                          next((i for i, h in enumerate(low) if nl in h), None))
        def g(row, k):
            i = col.get(k); return row[i] if i is not None and i < len(row) else None
        for row in it:
            d = pdate(g(row, "date"))
            if not d or week_of(d) != week: continue
            if not (lo is None or d >= lo) or not (hi is None or d <= hi): continue
            site = g(row, "site")
            if not site: continue
            if "deterrent" in cl(g(row, "cat")).lower(): continue
            off = g(row, "off"); off = int(off) if isinstance(off, (int, float)) and off else 1
            if dup_seen(wi_seen, site, d, num(g(row, "rec")), off, g(row, "desc")): continue
            out.append({
                "store": re.sub(r"\bWoolworths\b", "", cl(site), flags=re.I).strip(),
                "rec": num(g(row, "rec")), "type": cl(g(row, "type")), "product": cl(g(row, "prod")),
                "off": off, "police": "yes" in cl(g(row, "police")).lower(),
                "vt": "yes" in cl(g(row, "vt")).lower(), "ft": "yes" in cl(g(row, "ft")).lower()})
        wb.close()
    out.sort(key=lambda x: -x["rec"])
    return out


def week_of(d):
    for start, end in WEEK_DEFS:
        if start <= d <= end:
            return end
    return None


def resolve(header, targets):
    """Map canonical keys -> column index by header name (exact, then substring)."""
    low = [str(h).strip().lower() if h is not None else "" for h in header]
    out = {}
    for key, name in targets.items():
        nl = name.strip().lower()
        idx = next((i for i, h in enumerate(low) if h == nl), None)
        if idx is None:
            idx = next((i for i, h in enumerate(low) if nl in h), None)
        if idx is None:
            raise ValueError(f"column '{name}' not found in header")
        out[key] = idx
    return out

REGION_SHORT = {
    "Auckland - Tāmaki Makaurau": "Auckland",
    "Wellington - Te Whanganui-a-Tara": "Wellington",
    "Canterbury - Waitaha": "Canterbury",
    "Waikato": "Waikato",
    "Bay of Plenty - Te Moana-a-Toi": "Waikato",   # new WW deployment from W11 (Tauranga/Rotorua) — folded into Waikato to match the client's 4-region report (as W12); revert to its own region if Glenn wants BoP broken out
    "Manawatū-Whanganui": "Manawatū-Whanganui",
    "Hawke's Bay - Heretaunga": "Wellington",   # Hawke's Bay folded into Wellington (lower North Island)
}
REGION_ORDER = ["Auckland", "Wellington", "Canterbury", "Waikato", "Manawatū-Whanganui", "Other"]

# Store-name corrections applied AT INGEST (in clean()) so mis-typed / renamed sites merge
# into one canonical row and land in the right region. Keyed by lowercased cleaned name.
# These are documented guard data-entry faults, not renames of real distinct stores.
STORE_NAME_FIXES = {
    "queenstown woolworths": "Queensgate Woolworths",   # guard typo — the store is Queensgate (Lower Hutt), NOT Queenstown/Otago
    "hastings woolworths":   "Flaxmere Woolworths",       # persistent mis-tag — the covered store is Flaxmere (Hawke's Bay)
}

# Manual store->region corrections for stores whose source region field is blank or a
# variant that doesn't map (caught via the "Other" warning). Keyed by lowercased store name
# (AFTER STORE_NAME_FIXES has been applied).
STORE_REGION_OVERRIDE = {
    "moorhouse ave woolworths": "Canterbury",   # Christchurch store, region field blank in source
    "flaxmere woolworths":      "Wellington",   # Hawke's Bay store folded into Wellington; force despite mixed HB/Waikato/Manawatū source tags
    "northwest woolworths":     "Auckland",      # NorthWest (Massey/Westgate) — deployed some weeks with no incidents, so absent from the incident-derived region map
    "amberley woolworths":      "Canterbury",    # North Canterbury (Hurunui) — deployed some weeks with no incidents, so absent from the incident-derived region map
    "mairangi bay woolworths":  "Auckland",      # North Shore — deployed some weeks with no incidents, so absent from the incident-derived region map
    "dinsdale woolworths":      "Waikato",       # Hamilton — covered with no incidents; present in the cumulative tag-sheet only
    "belfast woolworths":       "Canterbury",    # Christchurch — covered with no incidents; present in the cumulative tag-sheet only
    "waiata shores woolworths": "Auckland",      # South Auckland (Takanini) — covered with no incidents; present in the cumulative tag-sheet only
    "fraser cove woolworths":   "Waikato",  # BoP deployment from W11 (Tauranga) — folded into Waikato (see REGION_SHORT note)
    "rotorua woolworths":       "Waikato",
    "tauranga woolworths":      "Waikato",
    "bureta park woolworths":   "Waikato",  # Tauranga
    "fairy springs woolworths": "Waikato",  # Rotorua — mixed BoP/Waikato source tags
}

# ---- brand ----
NAVY = "1E2A3A"; GREEN = "00843D"; GOLD = "C8952A"; LIGHT = "EEF2F6"; REGFILL = "D9E1EA"
WHITE = "FFFFFF"; INK = "1F2733"
thin = Side(style="thin", color="C9D2DC")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
MONEY = '#,##0.00'; INT = '#,##0'


def pdate(v):
    # Normalise to date-level (strip time) so week-start/end and source-bound comparisons
    # are inclusive of the whole day — otherwise a Sunday incident timestamped 14:49 fails
    # "d <= week_end(00:00)" and gets silently dropped.
    if isinstance(v, datetime):
        return v.replace(hour=0, minute=0, second=0, microsecond=0)
    if v is None:
        return None
    s = str(v).strip().split(" ")[0]
    for f in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(s, f)
        except Exception:
            pass
    return None


def wk(d):
    return (d - timedelta(days=d.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)


def num(v):
    try:
        return float(str(v).replace(",", "").replace("$", "")) if v not in (None, "") else 0.0
    except Exception:
        return 0.0


def month_of(d):
    """Calendar-month bucket key ('Jul 2026') for a date inside a defined FY week; None otherwise.
    Lets aggregate() re-bucket the SAME events by calendar month, so a reporting week that
    straddles a month-end is split by the day each event actually occurred."""
    return d.strftime("%b %Y") if week_of(d) is not None else None


def aggregate(bucket=week_of):
    """Return (data, store_region, regions_present).
    data[(bucket_key, store)] = dict of metrics; store keyed by cleaned display name.
    `bucket` maps an incident date -> a bucket key (default week_of = week-ending date; pass
    month_of for calendar-month buckets). Only dates inside a defined FY week are counted, so
    any bucketing sums to the same YTD — a straddling week's events split by calendar month.
    Unions multiple exports per stream, splitting by the per-source incident-date bounds."""
    region_votes = defaultdict(lambda: defaultdict(int))
    agg = defaultdict(lambda: {"rec": 0.0, "lost": 0.0, "off": 0, "inc": 0,
                               "pkg": 0.0, "pkgc": 0, "det": 0, "det_ind": 0,
                               "vtres": 0, "ftres": 0})

    def clean(s):
        # collapse whitespace, then apply documented store-name fixes + light spelling
        # hygiene (Mount->Mt, Pt Chevalier->Pt Chev) so variant labels don't split into
        # duplicate store rows or strand a typo'd site as a phantom store.
        s = " ".join(str(s).split()).strip()
        fixed = STORE_NAME_FIXES.get(s.lower())
        if fixed is not None:
            return fixed
        s = re.sub(r"\bMount\b", "Mt", s)
        s = re.sub(r"\bPt Chevalier\b", "Pt Chev", s)
        return s

    def within(d, lo, hi):
        return (lo is None or d >= lo) and (hi is None or d <= hi)

    def rows_of(path, targets):
        wb = openpyxl.load_workbook(path, read_only=True); ws = wb.active
        it = ws.iter_rows(values_only=True)
        header = list(next(it))
        col = resolve(header, targets)
        for row in it:
            yield row, col
        wb.close()

    GIR_T = {"date": "Date and Time of Incident - Date", "region": "Region of site",
             "site": "Select Woolworths Site", "off": "Number of offenders/POI",
             "rec": "Recovered Reciept Value", "stol": "Estimated Stolen Value",
             "desc": "Incident Description",
             "vt": "Verbal Trespass", "ft": "Formal Trespass Notice Served"}
    PKG_T = {"date": "Date and Time - Date", "region": "Region",
             "site": "Select Woolworths Site", "val": "Receipt Value"}
    DET_T = {"date": "Date and Time of Incident - Date", "region": "Region of site",
             "site": "Select Woolworths Site", "off": "Number of offenders/POI",
             "vt": "Verbal Trespass", "ft": "Formal Trespass Notice Served"}

    def is_yes(v):
        return str(v).strip().lower() == "yes"

    # GIR (permanent exact-duplicate removal — same store/date/$/offenders AND ~identical
    # description is a double-submission, counted once; distinct same-$ incidents kept)
    gir_seen = {}
    for path, lo, hi in GIR_SOURCES:
        for row, c in rows_of(path, GIR_T):
            d = pdate(row[c["date"]])
            if not d or bucket(d) is None or not within(d, lo, hi) or not row[c["site"]]:
                continue
            site = clean(row[c["site"]]); w = bucket(d)
            off = row[c["off"]]; off = int(off) if isinstance(off, (int, float)) and off else 1
            rec = num(row[c["rec"]])
            desc = row[c["desc"]] if c.get("desc") is not None else ""
            if dup_seen(gir_seen, site, d, rec, off, desc):
                continue
            region_votes[site][clean(row[c["region"]]) if row[c["region"]] else "Other"] += 1
            a = agg[(w, site)]
            a["rec"] += rec; a["lost"] += num(row[c["stol"]])
            a["off"] += off
            a["inc"] += 1
            if is_yes(row[c["vt"]]): a["vtres"] += 1
            if is_yes(row[c["ft"]]): a["ftres"] += 1
    # PKG
    for path, lo, hi in PKG_SOURCES:
        for row, c in rows_of(path, PKG_T):
            d = pdate(row[c["date"]])
            if not d or bucket(d) is None or not within(d, lo, hi) or not row[c["site"]]:
                continue
            site = clean(row[c["site"]]); w = bucket(d)
            region_votes[site][clean(row[c["region"]]) if row[c["region"]] else "Other"] += 1
            a = agg[(w, site)]; a["pkg"] += num(row[c["val"]]); a["pkgc"] += 1
    # DET
    for path, lo, hi in DET_SOURCES:
        for row, c in rows_of(path, DET_T):
            d = pdate(row[c["date"]])
            if not d or bucket(d) is None or not within(d, lo, hi) or not row[c["site"]]:
                continue
            site = clean(row[c["site"]]); w = bucket(d)
            region_votes[site][clean(row[c["region"]]) if row[c["region"]] else "Other"] += 1
            a = agg[(w, site)]; a["det"] += 1
            o = row[c["off"]]; a["det_ind"] += int(o) if isinstance(o, (int, float)) and o else 1
            if is_yes(row[c["vt"]]): a["vtres"] += 1
            if is_yes(row[c["ft"]]): a["ftres"] += 1

    store_region = {}
    for s, votes in region_votes.items():
        raw = max(votes.items(), key=lambda x: x[1])[0]
        store_region[s] = STORE_REGION_OVERRIDE.get(s.strip().lower(), REGION_SHORT.get(raw, "Other"))
    unmapped = [s for s, r in store_region.items() if r == "Other"]
    if unmapped:
        print("[WARN] stores mapped to 'Other' (region field blank/unmapped — add to "
              "STORE_REGION_OVERRIDE):", unmapped, file=sys.stderr)
    regions = sorted({r for r in store_region.values()},
                     key=lambda r: REGION_ORDER.index(r) if r in REGION_ORDER else 99)
    return dict(agg), store_region, regions


# ---- metric helpers (money rows vs count rows) ----
def store_metrics(a):
    # "Total Recovered" carries recovered + reported stolen (historical convention so
    # the store grand total ties to National Total Loss). Packaging + Deterrents separate.
    return {
        "Total Recovered": (a["rec"] + a["lost"], True),
        "Recovered Packaging": (a["pkg"], True),
        "Deterents": (a["det"], False),
    }


NATIONAL_ROWS = [
    ("Total Recovered ($)", "rec", True),
    ("Total Lost ($)", "lost", True),
    ("Combined Recovery ($)", "combined", True),
    ("Recovered Packaging ($)", "pkg", True),
    ("TOTAL LOSS ($)", "total_loss", True),
    ("", None, None),
    ("Total Incidents (#)", "inc", False),
    ("Offenders in Incidents (#)", "off", False),
    ("Deterrents (#)", "det", False),
    ("Deterred Individuals (#)", "det_ind", False),
    ("Trespass Actions (#)", "tres", False),
    ("  — Verbal (#)", "vtres", False),
    ("  — Formal (#)", "ftres", False),
    ("Packaging Events (#)", "pkgc", False),
]


def rollup(rows):
    """rows = list of metric dicts -> national/region totals dict."""
    rec = sum(a["rec"] for a in rows); lost = sum(a["lost"] for a in rows)
    pkg = sum(a["pkg"] for a in rows)
    return {
        "rec": rec, "lost": lost, "rec_lost": rec + lost, "combined": rec + lost,
        "pkg": pkg, "total_loss": rec + lost + pkg,
        "inc": sum(a["inc"] for a in rows), "det": sum(a["det"] for a in rows),
        "pkgc": sum(a["pkgc"] for a in rows), "off": sum(a["off"] for a in rows),
        "det_ind": sum(a["det_ind"] for a in rows),
        "vtres": sum(a["vtres"] for a in rows), "ftres": sum(a["ftres"] for a in rows),
        "tres": sum(a["vtres"] + a["ftres"] for a in rows),
    }


def style_title(ws, ncols, text, sub):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=ncols)
    c = ws.cell(1, 1, text)
    c.font = Font(name="Arial", size=14, bold=True, color=WHITE)
    c.fill = PatternFill("solid", fgColor=NAVY)
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[1].height = 26
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=ncols)
    c2 = ws.cell(2, 1, sub)
    c2.font = Font(name="Arial", size=9, italic=True, color="5A6675")
    c2.alignment = Alignment(horizontal="left", indent=1)


def hdr_row(ws, r, labels, first_label="Metric"):
    cells = [first_label] + labels
    for i, v in enumerate(cells, 1):
        c = ws.cell(r, i, v)
        c.font = Font(name="Arial", size=10, bold=True, color=WHITE)
        c.fill = PatternFill("solid", fgColor=NAVY)
        c.alignment = Alignment(horizontal="center" if i > 1 else "left",
                                vertical="center", indent=0 if i > 1 else 1)
        c.border = BORDER
        if i > 1 and isinstance(v, datetime):
            c.number_format = 'dd mmm'
    ws.row_dimensions[r].height = 20


def write_metric_row(ws, r, label, per_week_vals, ytd, is_money, bold=False, fill=None, indent=1):
    lc = ws.cell(r, 1, label)
    lc.font = Font(name="Arial", size=10, bold=bold, color=INK)
    lc.alignment = Alignment(horizontal="left", indent=indent)
    lc.border = BORDER
    if fill:
        lc.fill = PatternFill("solid", fgColor=fill)
    for i, v in enumerate(per_week_vals, 2):
        c = ws.cell(r, i, round(v, 2) if is_money else int(v))
        c.number_format = MONEY if is_money else INT
        c.font = Font(name="Arial", size=10, bold=bold, color=INK)
        c.alignment = Alignment(horizontal="right")
        c.border = BORDER
        if fill:
            c.fill = PatternFill("solid", fgColor=fill)
    yc = ws.cell(r, 2 + len(per_week_vals), round(ytd, 2) if is_money else int(ytd))
    yc.number_format = MONEY if is_money else INT
    yc.font = Font(name="Arial", size=10, bold=True, color=INK)
    yc.alignment = Alignment(horizontal="right")
    yc.border = BORDER
    yc.fill = PatternFill("solid", fgColor=LIGHT if not fill else fill)


def main():
    agg, store_region, regions = aggregate()
    nweeks = len(WEEKS)
    ncols = 1 + nweeks + 1  # label + weeks + YTD
    week_labels = list(WEEKS)

    def rows_for(pred):
        return [a for (w, s), a in agg.items() if pred(w, s)]

    # national per week
    nat = {w: rollup([a for (ww, s), a in agg.items() if ww == w]) for w in WEEKS}
    nat_ytd = rollup(list(agg.values()))

    wb = openpyxl.Workbook()

    # ============ 1. NATIONAL SUMMARY ============
    ws = wb.active; ws.title = "National Summary"
    style_title(ws, ncols, "Woolworths NZ — National Loss-Prevention Summary",
                "SLS RTC covert LP · FY27 (from 01 Jul 2026) · Total Loss = Recovered + Lost + Recovered Packaging · self-reconciling")
    hdr_row(ws, 3, week_labels + ["YTD"])
    r = 4
    for label, key, is_money in NATIONAL_ROWS:
        if key is None:
            r += 1; continue
        pw = [nat[w][key] for w in WEEKS]
        headline = label.startswith("TOTAL LOSS")
        write_metric_row(ws, r, label, pw, nat_ytd[key], is_money,
                         bold=headline, fill=(GOLD if headline else None))
        if headline:
            for c in range(1, ncols + 1):
                ws.cell(r, c).font = Font(name="Arial", size=10, bold=True, color=NAVY)
        r += 1
    ws.column_dimensions["A"].width = 24
    for c in range(2, ncols + 1):
        ws.column_dimensions[L(c)].width = 13
    ws.freeze_panes = "B4"

    # ============ 2. REGION SUMMARY ============
    ws = wb.create_sheet("Region Summary")
    style_title(ws, ncols, "Woolworths NZ — Performance by Region",
                "Every region, every week · Total Loss and activity · region blocks sum to National")
    hdr_row(ws, 3, week_labels + ["YTD"], first_label="Region / Metric")
    r = 4
    reg_metric_rows = [("Recovered ($)", "rec_lost", True), ("Packaging ($)", "pkg", True),
                       ("Total Loss ($)", "total_loss", True), ("Incidents (#)", "inc", False),
                       ("Deterrents (#)", "det", False), ("Trespass Actions (#)", "tres", False)]
    for reg in regions:
        # region header
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=ncols)
        hc = ws.cell(r, 1, f"▍ {reg}")
        hc.font = Font(name="Arial", size=11, bold=True, color=NAVY)
        hc.fill = PatternFill("solid", fgColor=REGFILL)
        hc.alignment = Alignment(horizontal="left", indent=1)
        ws.row_dimensions[r].height = 18
        r += 1
        reg_week = {w: rollup([a for (ww, s), a in agg.items() if ww == w and store_region.get(s) == reg]) for w in WEEKS}
        reg_ytd = rollup([a for (ww, s), a in agg.items() if store_region.get(s) == reg])
        for label, key, is_money in reg_metric_rows:
            write_metric_row(ws, r, label, [reg_week[w][key] for w in WEEKS], reg_ytd[key], is_money, indent=2)
            r += 1
    # NETWORK total (ties to National Summary)
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=ncols)
    hc = ws.cell(r, 1, "▍ NETWORK (all regions)"); hc.font = Font(name="Arial", size=11, bold=True, color=WHITE)
    hc.fill = PatternFill("solid", fgColor=NAVY); hc.alignment = Alignment(horizontal="left", indent=1)
    r += 1
    for label, key, is_money in reg_metric_rows:
        write_metric_row(ws, r, label, [nat[w][key] for w in WEEKS], nat_ytd[key], is_money, bold=True, indent=2)
        r += 1
    ws.column_dimensions["A"].width = 24
    for c in range(2, ncols + 1):
        ws.column_dimensions[L(c)].width = 13
    ws.freeze_panes = "B4"

    # ============ 3. STORE COMPARISON (grouped by region) ============
    ws = wb.create_sheet("Store Comparison")
    style_title(ws, ncols, "Woolworths NZ — Store Comparison (grouped by region)",
                "Every store · Total Recovered (incl. reported stolen) / Recovered Packaging / Deterrents · region subtotals + GRAND TOTAL tie to National")
    hdr_row(ws, 3, week_labels + ["YTD"], first_label="Store / Metric")
    r = 4
    # store list per region
    stores_by_region = defaultdict(set)
    for (w, s), a in agg.items():
        stores_by_region[store_region.get(s, "Other")].add(s)
    METRIC_KEYS = [("Total Recovered", True), ("Recovered Packaging", True), ("Deterents", False)]
    for reg in regions:
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=ncols)
        hc = ws.cell(r, 1, f"▍ {reg}"); hc.font = Font(name="Arial", size=11, bold=True, color=NAVY)
        hc.fill = PatternFill("solid", fgColor=REGFILL); hc.alignment = Alignment(horizontal="left", indent=1)
        r += 1
        for s in sorted(stores_by_region[reg]):
            for metric, is_money in METRIC_KEYS:
                pw = []
                for w in WEEKS:
                    a = agg.get((w, s))
                    pw.append(store_metrics(a)[metric][0] if a else 0)
                ytd = sum(pw)
                write_metric_row(ws, r, f"{s} — {metric}", pw, ytd, is_money, indent=2)
                r += 1
        # region subtotal
        sub_week = {w: rollup([a for (ww, ss), a in agg.items() if ww == w and store_region.get(ss) == reg]) for w in WEEKS}
        sub_ytd = rollup([a for (ww, ss), a in agg.items() if store_region.get(ss) == reg])
        write_metric_row(ws, r, f"{reg} — SUBTOTAL Total Loss", [sub_week[w]["total_loss"] for w in WEEKS],
                         sub_ytd["total_loss"], True, bold=True, fill=LIGHT, indent=1)
        r += 1
    # GRAND TOTAL
    write_metric_row(ws, r, "GRAND TOTAL — Total Loss (ties to National)",
                     [nat[w]["total_loss"] for w in WEEKS], nat_ytd["total_loss"], True, bold=True, fill=GOLD, indent=1)
    for c in range(1, ncols + 1):
        ws.cell(r, c).font = Font(name="Arial", size=10, bold=True, color=NAVY)
    ws.column_dimensions["A"].width = 40
    for c in range(2, ncols + 1):
        ws.column_dimensions[L(c)].width = 13
    ws.freeze_panes = "B4"

    # ============ 4. RECONCILIATION ============
    ws = wb.create_sheet("Reconciliation")
    style_title(ws, 6, "Reconciliation — self-check (must be $0.00 every week)",
                "National Total Loss vs sum of Region blocks vs sum of Store rows. Any non-zero = a processing fault.")
    heads = ["Week", "National", "Σ Regions", "Σ Stores", "Max Diff", "Status"]
    for i, h in enumerate(heads, 1):
        c = ws.cell(3, i, h); c.font = Font(name="Arial", size=10, bold=True, color=WHITE)
        c.fill = PatternFill("solid", fgColor=NAVY); c.alignment = Alignment(horizontal="center"); c.border = BORDER
    r = 4
    all_ok = True
    for w in WEEKS:
        national = nat[w]["total_loss"]
        reg_sum = sum(rollup([a for (ww, s), a in agg.items() if ww == w and store_region.get(s) == reg])["total_loss"] for reg in regions)
        store_sum = sum(store_metrics(a)["Total Recovered"][0] + store_metrics(a)["Recovered Packaging"][0]
                        for (ww, s), a in agg.items() if ww == w)
        diff = max(abs(national - reg_sum), abs(national - store_sum))
        ok = diff < 0.01
        all_ok &= ok
        vals = [w, national, reg_sum, store_sum, diff, "PASS" if ok else "FAIL"]
        for i, v in enumerate(vals, 1):
            c = ws.cell(r, i, v); c.border = BORDER; c.alignment = Alignment(horizontal="right" if i > 1 else "left")
            if i == 1:
                c.number_format = 'dd mmm yyyy'
            elif i in (2, 3, 4, 5):
                c.number_format = MONEY
            if i == 6:
                c.font = Font(name="Arial", size=10, bold=True, color=("00843D" if ok else "A32318"))
                c.alignment = Alignment(horizontal="center")
        r += 1
    for i, wd in enumerate([16, 14, 14, 14, 12, 10], 1):
        ws.column_dimensions[L(i)].width = wd

    wb.save(OUT)

    # ---- console reconciliation ----
    print("=== NEW MASTER v2 built ===")
    print(f"  file: {OUT}")
    print(f"  weeks seeded: {[str(w.date()) for w in WEEKS]}")
    print(f"  regions: {regions}")
    print(f"  stores: {len(store_region)}")
    print(f"\n  FY27 YTD Total Loss (from 01 Jul): ${nat_ytd['total_loss']:,.2f}")
    print(f"\n  Per-week reconciliation:")
    for w in WEEKS:
        national = nat[w]["total_loss"]
        reg_sum = sum(rollup([a for (ww, s), a in agg.items() if ww == w and store_region.get(s) == reg])["total_loss"] for reg in regions)
        store_sum = sum(store_metrics(a)["Total Recovered"][0] + store_metrics(a)["Recovered Packaging"][0]
                        for (ww, s), a in agg.items() if ww == w)
        print(f"    {w.date()}  national=${national:>11,.2f}  regions=${reg_sum:>11,.2f}  stores=${store_sum:>11,.2f}  "
              f"{'PASS' if max(abs(national-reg_sum),abs(national-store_sum))<0.01 else 'FAIL'}")
    if not all_ok:
        print("\n  *** RECONCILIATION FAILED ***"); sys.exit(1)
    print("\n  ALL WEEKS RECONCILE ✓")


if __name__ == "__main__":
    main()
