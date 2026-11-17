#!/usr/bin/env python3
"""QA gate for the Bunnings MONTHLY report package (/report-qa, Bunnings edition).

Independent validation of the month-end artefacts before anything is sent:
  - master GIR  ~/Desktop/SLS-RTC/Operations/Analytics/data/latest/gir-bunnings.xlsx
  - metrics     scripts/bunnings/nro_metrics_<TAG>.json   (client basis, may be
                adopt-Auror-greater UNION >= GIR basis)
  - client PDF  ~/Desktop/Bunnings/Bunnings_<Month>_Value_Report.pdf
  - dashboards  Analytics/output/bunnings/Bunnings_Operative_Performance_<YYYY-MM>[_recovered].pdf
  - tag-sheet   data/latest/timeclock-tag-sheet YYYY-MM-*.xlsx  (hours = invoice basis)
  - XERO_INVOICED entry inside generate_bunnings_monthly_report.py

Checks:
  C1  master opens, target-month rows exist, no error cells (#REF! etc.)
  C2  independent GIR-basis recompute (events / recovered / identified / severity / sites)
  C3  metrics JSON internal consistency: regional foots to incidents + recovered to the
      cent; recovery_pct, inc_per_100h, top6 shares recompute; severity sum == GIR events;
      union incidents >= GIR events; union recovered >= GIR recovered
  C4  zero-out guard: every FY month (Aug 2026 -> target) has events > 0 and recovered > 0
  C5  billable-hours leave check: every tag-sheet job row is a Bunnings store (the monthly
      leave check, automated); tag-sheet total == metrics hours_window
  C6  invoice recompute: hours x $43/$45 split (6 named $45 guards, name variants collapsed)
      == XERO_INVOICED["<month>"] in the dashboard generator, to the cent
  C7  PDF probes: value report carries the JSON headline figures; dashboard(s) carry the
      GIR-basis recovered for the month
  C8  month-over-month sanity: WARN on >60% swings in events or recovered
  C9  name hygiene: WARN on reporter names w/ double spaces or unknown lowercase variants

Usage: validate_month_package.py [--month YYYY-MM]   (default: latest month in master)
Exit 0 = all PASS (warnings allowed); exit 1 = any FAIL.
"""
import sys, os, re, json, glob, datetime
import openpyxl

DL = os.path.expanduser("~/Desktop/SLS-RTC/Operations/Analytics/data/latest")
GEN = os.path.expanduser("~/Desktop/SLS-RTC/Operations/Analytics/generators/generate_bunnings_monthly_report.py")
OUTB = os.path.expanduser("~/Desktop/SLS-RTC/Operations/Analytics/output/bunnings")
HERE = os.path.dirname(os.path.abspath(__file__))
ERRS = ("#REF!", "#DIV/0!", "#VALUE!", "#N/A", "#NAME?", "#NULL!", "#NUM!")
FY_DETAIL_START = "2026-08"
RATE45 = {"farshid hakimi", "pene tuiketei", "simmerjit singh brar", "nirajkumar katwala",
          "eru nehana", "siositeni maka"}
NAME_FIX = {"benn conner": "ben conner", "fashid hakimi": "farshid hakimi",
            "don tehe": "don tamasese", "simmerjit singh": "simmerjit singh brar",
            "nirajkumar": "nirajkumar katwala", "pat manu": "patrick manu"}

results = []
def rec(level, check, msg):
    results.append((level, check, msg))
    print(f"  [{level:4s}] {check}: {msg}")

def num(v):
    try: return float(str(v or 0).replace(",", "").replace("$", "") or 0)
    except ValueError: return 0.0

def canon(name):
    s = re.sub(r"\s+", " ", str(name or "").strip()).lower()
    return NAME_FIX.get(s, s)

# ---------- C1: master + target month ----------
MASTER = f"{DL}/gir-bunnings.xlsx"
wb = openpyxl.load_workbook(MASTER, read_only=True, data_only=True)
ws = wb.active
rows = list(ws.iter_rows(values_only=True))
H = [str(h or "").strip().lower() for h in rows[0]]
def col(frag): return next(i for i, h in enumerate(H) if frag in h)
c_d, c_site = col("date and time of incident - date"), col("bunnings site")
c_rec, c_stol, c_sev, c_fn = col("recovered reciept value"), col("estimated stolen value"), col("incident severity"), col("full name")
err_hits = sum(1 for r in rows for v in r if isinstance(v, str) and any(e in v for e in ERRS))
rec("FAIL" if err_hits else "PASS", "C1 error cells (master)", f"{err_hits} error strings" if err_hits else "none")

by_month = {}
for r in rows[1:]:
    dt = r[c_d]
    if not isinstance(dt, datetime.datetime): continue
    by_month.setdefault(dt.strftime("%Y-%m"), []).append(r)
wb.close()

MONTH = sys.argv[sys.argv.index("--month") + 1] if "--month" in sys.argv else max(by_month)
print(f"  target month: {MONTH}")
mrows = by_month.get(MONTH, [])
rec("FAIL" if not mrows else "PASS", "C1 target month", f"{len(mrows)} GIR rows in master for {MONTH}")
if not mrows: sys.exit(1)

# ---------- C2: independent GIR-basis recompute ----------
g_n = len(mrows)
g_rec = round(sum(num(r[c_rec]) for r in mrows), 2)
g_ident = round(sum(num(r[c_rec]) + num(r[c_stol]) for r in mrows), 2)
g_sev = {}
for r in mrows:
    m = re.search(r"[1-5]", str(r[c_sev] or ""))
    if m: g_sev[int(m.group())] = g_sev.get(int(m.group()), 0) + 1
g_sites = {str(r[c_site] or "").strip() for r in mrows if str(r[c_site] or "").strip()}
rec("PASS", "C2 GIR-basis recompute",
    f"{g_n} ev · ${g_rec:,.2f} rec · ${g_ident:,.2f} ident · {len(g_sites)} sites · sev {dict(sorted(g_sev.items()))}")

# ---------- C3: metrics JSON consistency ----------
mdate = datetime.datetime.strptime(MONTH, "%Y-%m")
TAG = mdate.strftime("%b%Y").upper()
jpath = f"{HERE}/nro_metrics_{TAG}.json"
if not os.path.exists(jpath):
    rec("FAIL", "C3 metrics json", f"{os.path.basename(jpath)} missing")
    J = None
else:
    J = json.load(open(jpath))
    probs = []
    if not (str(J["date_lo"]).startswith(MONTH) and str(J["date_hi"]).startswith(MONTH)):
        probs.append(f"date range {J['date_lo']}..{J['date_hi']} outside {MONTH}")
    reg_inc = sum(r["incidents"] for r in J["regional"]); reg_rec = sum(r["recovered"] for r in J["regional"])
    if reg_inc != J["incidents"]: probs.append(f"regional incidents foot {reg_inc} != {J['incidents']}")
    if abs(reg_rec - J["recovered"]) > 0.01: probs.append(f"regional recovered foot ${reg_rec:,.2f} != ${J['recovered']:,.2f}")
    if abs(J["recovery_pct"] - 100 * J["recovered"] / J["identified"]) > 0.06:
        probs.append("recovery_pct does not recompute")
    if J.get("hours_window", 0) <= 0: probs.append("hours_window <= 0")
    elif abs(J["inc_per_100h"] - 100 * J["incidents"] / J["hours_window"]) > 0.02:
        probs.append("inc_per_100h does not recompute")
    sev_sum = sum(int(v) for v in J["severity"].values())
    if sev_sum != g_n: probs.append(f"severity sum {sev_sum} != GIR events {g_n}")
    if J["incidents"] < g_n: probs.append(f"union incidents {J['incidents']} < GIR events {g_n}")
    if J["recovered"] + 0.01 < g_rec: probs.append(f"union recovered ${J['recovered']:,.2f} < GIR ${g_rec:,.2f}")
    for s in J["top6"]:
        if abs(s["share"] - 100 * s["recovered"] / J["recovered"]) > 0.06:
            probs.append(f"top6 share off for {s['store']}"); break
    rec("FAIL" if probs else "PASS", "C3 metrics json",
        "; ".join(probs) if probs else
        f"{J['incidents']} ev · ${J['recovered']:,.2f} ({J['recovery_pct']}%) — foots, recomputes, union >= GIR")

# ---------- C4: zero-out guard across FY months ----------
fy_months = sorted(k for k in by_month if FY_DETAIL_START <= k <= MONTH)
zero = [k for k in fy_months if not by_month[k] or sum(num(r[c_rec]) for r in by_month[k]) <= 0]
rec("FAIL" if zero else "PASS", "C4 zero-out guard",
    f"months with zero events/recovery: {zero}" if zero else
    f"all {len(fy_months)} FY months populated ({', '.join(str(len(by_month[k])) + ' ev' for k in fy_months)})")

# ---------- C5 + C6: tag-sheet leave check, hours, invoice recompute ----------
tags = glob.glob(f"{DL}/timeclock-tag-sheet {MONTH}-01*.xlsx")
if not tags:
    rec("FAIL", "C5 tag-sheet", f"no tag-sheet for {MONTH} in data/latest")
else:
    tw = openpyxl.load_workbook(tags[0], read_only=True, data_only=True).active
    tr = list(tw.iter_rows(values_only=True))
    TH = [str(x or "").strip().lower() for x in tr[0]]
    ij, ip, ih = TH.index("job"), TH.index("performed by"), TH.index("hours")
    nonb, tot = [], 0.0
    guard_h = {}
    for r in tr[1:]:
        j = str(r[ij] or "").strip()
        if j:
            tot += num(r[ih])
            if "bunning" not in j.lower(): nonb.append(j)
        else:
            nm = canon(r[ip])
            if nm: guard_h[nm] = guard_h.get(nm, 0) + num(r[ih])
    rec("FAIL" if nonb else "PASS", "C5 leave check",
        f"NON-Bunnings job rows: {nonb}" if nonb else f"all {tot:,.2f}h are Bunnings store jobs — fully billable")
    if J:
        dh = abs(tot - J["hours_window"])
        rec("FAIL" if dh > 0.01 else "PASS", "C5 hours vs metrics",
            f"tag-sheet {tot:,.2f}h vs json {J['hours_window']:,.2f}h (diff {dh:,.2f})")
    h45 = sum(h for g, h in guard_h.items() if g in RATE45)
    h43 = sum(guard_h.values()) - h45
    inv = round(h43 * 43 + h45 * 45, 2)
    gsrc = open(GEN).read()
    m = re.search(rf'"{MONTH}":\s*([0-9_]+(?:\.[0-9]+)?)', gsrc)
    if not m:
        rec("FAIL", "C6 invoice", f'XERO_INVOICED has no "{MONTH}" entry in the dashboard generator')
    else:
        booked = float(m.group(1).replace("_", ""))
        di = abs(inv - booked)
        rec("FAIL" if di > 0.01 else "PASS", "C6 invoice recompute",
            f"recomputed ${inv:,.2f} ({h43:,.2f}h@$43 + {h45:,.2f}h@$45) vs XERO_INVOICED ${booked:,.2f} (diff ${di:,.2f})")

# ---------- C7: PDF probes ----------
try:
    import fitz
    month_name = mdate.strftime("%B")
    vr = os.path.expanduser(f"~/Desktop/Bunnings/Bunnings_{month_name}_Value_Report.pdf")
    if not os.path.exists(vr):
        rec("FAIL", "C7 value report", "pdf missing")
    elif J:
        t = "".join(p.get_text() for p in fitz.open(vr))
        miss = [k for k, s in (("incidents", str(J["incidents"])), ("recovered", f"${J['recovered']:,.2f}"),
                               ("recovery%", f"{J['recovery_pct']:.1f}%"), ("sites", str(J["sites"]))) if s not in t]
        rec("FAIL" if miss else "PASS", "C7 value report", f"figures NOT found: {miss}" if miss else "headline figures present")
    for suffix in ("", "_recovered"):
        dp = f"{OUTB}/Bunnings_Operative_Performance_{MONTH}{suffix}.pdf"
        if not os.path.exists(dp):
            if suffix == "": rec("FAIL", "C7 dashboard", "pdf missing")
            continue
        t = "".join(p.get_text() for p in fitz.open(dp))
        probe = f"${g_rec:,.0f}"
        rec("PASS" if probe in t else "FAIL", f"C7 dashboard{suffix or ''}",
            f"GIR recovered {probe} {'present' if probe in t else 'NOT FOUND'}")
except ImportError:
    rec("WARN", "C7 pdfs", "pymupdf unavailable — PDF probes skipped")

# ---------- C8: month-over-month sanity ----------
prev = max((k for k in by_month if k < MONTH and k >= FY_DETAIL_START), default=None)
if prev:
    p_n, p_rec = len(by_month[prev]), sum(num(r[c_rec]) for r in by_month[prev])
    warned = False
    for name, cur, pv in (("events", g_n, p_n), ("recovered", g_rec, p_rec)):
        if pv > 0 and abs(cur - pv) / pv > 0.60:
            rec("WARN", "C8 MoM swing", f"{name} moved {100*(cur-pv)/pv:+.0f}% vs {prev}"); warned = True
    if not warned:
        rec("PASS", "C8 MoM sanity", f"{prev}: {p_n} ev/${p_rec:,.0f} -> {MONTH}: {g_n} ev/${g_rec:,.0f} within band")

# ---------- C9: name hygiene ----------
odd = sorted({str(r[c_fn]) for r in mrows
              if str(r[c_fn] or "").strip() and
              (re.search(r"\s{2,}", str(r[c_fn])) or str(r[c_fn]).strip()[0].islower())})
rec("WARN" if odd else "PASS", "C9 name hygiene",
    f"variant-looking reporter names (check maps): {odd}" if odd else "no suspicious reporter-name variants")

fails = [r for r in results if r[0] == "FAIL"]
warns = [r for r in results if r[0] == "WARN"]
print(f"\n{'='*60}\nBUNNINGS MONTH QA — {MONTH}: "
      f"{'FAIL — DO NOT SEND' if fails else 'PASS — PACKAGE OK TO SEND'}"
      f"  ({len(results)-len(fails)-len(warns)} pass / {len(warns)} warn / {len(fails)} fail)")
sys.exit(1 if fails else 0)
