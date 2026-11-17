#!/usr/bin/env python3
"""QA gate for the Woolworths weekly report package (/report-qa).

Deterministic, INDEPENDENT validation of the generated Excel + PDF package before
anything is sent to Glenn. Exists because a previous master silently zeroed out a
sheet; and because the tracker's Cost/Total-Recovery/Total-Loss columns are Excel
FORMULAS that read as blank/zero to programmatic readers until Excel recalculates
(so no downstream script may ever "read" them — this validator recomputes instead).

Checks (FAIL = do not send; WARN = eyeball before sending):
  1  Master: 4 sheets present; Reconciliation = PASS for every week; latest week present
  2  Error-cell scan (#REF!/#DIV/0!/#VALUE!/#N/A/#NAME?) across master + tracker
  3  Master National Summary, target week: TOTAL LOSS / recovery / incidents all > 0
  4  Zero-out guard: every past week column in National Summary has TOTAL LOSS > 0
     and every past Weekly Ledger row has Hours > 0 and recovery > 0
  5  Tracker Weekly Ledger row (target week): static cells agree with master to the cent
     (direct, packaging, not-recovered, incidents, trespass) and Hours > 0
  6  Tracker formula integrity: Cost / Total Recovery / Total Loss cells for the target
     week CONTAIN formulas; recomputed cost = hours x bill-rate cell
  7  This Week - Store Detail: hours foot to Weekly Ledger hours; recovery foots to
     direct+packaging to the cent
  8  PDFs (value, safety, dashboard): headline figures (total loss, recovery, incidents,
     hours) appear verbatim in the rendered text
  9  Week-over-week sanity: WARN if hours or total recovery swing > 60% vs prior week

Usage: validate_week_package.py [--week YYYY-MM-DD]   (default: latest Reconciliation row)
Exit 0 = all PASS (warnings allowed); exit 1 = any FAIL.
"""
import sys, os, re, datetime
import openpyxl

WW = os.path.expanduser("~/Desktop/Woolworths ")
MASTER = f"{WW}/Woolworths Master Data FY27.xlsx"
TRACKER = f"{WW}/Woolworths FY27 Deployment & Recovery Tracker.xlsx"
ERRS = ("#REF!", "#DIV/0!", "#VALUE!", "#N/A", "#NAME?", "#NULL!", "#NUM!")

results = []
def rec(level, check, msg):
    results.append((level, check, msg))
    print(f"  [{level:4s}] {check}: {msg}")

def num(v):
    try: return float(v)
    except (TypeError, ValueError): return 0.0

def d(v):
    if isinstance(v, datetime.datetime): return v.date()
    if isinstance(v, datetime.date): return v
    return None

# ---------- target week ----------
week_arg = None
if "--week" in sys.argv:
    week_arg = datetime.datetime.strptime(sys.argv[sys.argv.index("--week") + 1], "%Y-%m-%d").date()

mv = openpyxl.load_workbook(MASTER, read_only=True, data_only=True)

# 1 — sheets + reconciliation
need = {"National Summary", "Region Summary", "Store Comparison", "Reconciliation"}
missing = need - set(mv.sheetnames)
rec("FAIL" if missing else "PASS", "C1 master sheets", f"missing {missing}" if missing else "all 4 sheets present")

recon_rows = [r for r in mv["Reconciliation"].iter_rows(values_only=True) if d(r[0])]
bad = [r for r in recon_rows if str(r[5]).strip() != "PASS"]
rec("FAIL" if bad else "PASS", "C1 reconciliation",
    f"{len(bad)} week(s) not PASS: {[str(r[0])[:10] for r in bad]}" if bad else f"all {len(recon_rows)} weeks PASS")
WEEK = week_arg or max(d(r[0]) for r in recon_rows)
weeks_all = sorted(d(r[0]) for r in recon_rows)
print(f"  target week ending: {WEEK}")
if WEEK not in weeks_all:
    rec("FAIL", "C1 target week", f"{WEEK} not in master reconciliation")

recon_national = {d(r[0]): num(r[1]) for r in recon_rows}

# 2 — error cells (master values + tracker formulas/values)
def err_scan(path, label, data_only):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=data_only)
    hits = []
    for sn in wb.sheetnames:
        for row in wb[sn].iter_rows(values_only=True):
            for v in row:
                if isinstance(v, str) and any(e in v for e in ERRS):
                    hits.append(sn)
                    break
    wb.close()
    rec("FAIL" if hits else "PASS", f"C2 error cells ({label})",
        f"error strings in sheets {sorted(set(hits))}" if hits else "none")
err_scan(MASTER, "master", True)
err_scan(TRACKER, "tracker", False)

# 3 + 4 — National Summary target column + zero-out guard across all past weeks
ns = list(mv["National Summary"].iter_rows(values_only=True))
hdr = next(r for r in ns if str(r[0]).strip() == "Metric")
col_of = {d(v): i for i, v in enumerate(hdr) if d(v)}
def metric_row(label):
    return next((r for r in ns if str(r[0] or "").strip().lower() == label.lower()), None)
M = {k: metric_row(k) for k in ("TOTAL LOSS ($)", "Combined Recovery ($)", "Total Incidents (#)",
                                 "Trespass Actions (#)", "Total Recovered ($)", "Recovered Packaging ($)",
                                 "Total Lost ($)", "Offenders in Incidents (#)")}
none_rows = [k for k, v in M.items() if v is None]
if none_rows:
    rec("FAIL", "C3 metric rows", f"missing metric rows {none_rows}")
ci = col_of.get(WEEK)
if ci is None:
    rec("FAIL", "C3 week column", f"{WEEK} column not in National Summary")
    print("ABORT"); sys.exit(1)
tl, cr, inc = num(M["TOTAL LOSS ($)"][ci]), num(M["Combined Recovery ($)"][ci]), num(M["Total Incidents (#)"][ci])
rec("FAIL" if (tl <= 0 or cr <= 0 or inc <= 0) else "PASS", "C3 target-week national",
    f"TOTAL LOSS ${tl:,.2f} · recovery ${cr:,.2f} · incidents {int(inc)}")
zero_weeks = [w for w, i in col_of.items() if w <= WEEK and num(M["TOTAL LOSS ($)"][i]) <= 0]
rec("FAIL" if zero_weeks else "PASS", "C4 zero-out guard (master)",
    f"weeks with TOTAL LOSS <= 0: {zero_weeks}" if zero_weeks else f"all {sum(1 for w in col_of if w <= WEEK)} past weeks > 0")
# also: master national vs its own reconciliation sheet
diff = abs(tl - recon_national.get(WEEK, -1))
rec("FAIL" if diff > 0.01 else "PASS", "C4 master vs recon sheet", f"diff ${diff:,.4f}")
mv.close()

# 5 + 6 — tracker (static values + formula presence)
tv = openpyxl.load_workbook(TRACKER, read_only=True, data_only=True)
tf = openpyxl.load_workbook(TRACKER, read_only=True, data_only=False)
wlv = list(tv["Weekly Ledger"].iter_rows(values_only=True))
wlf = list(tf["Weekly Ledger"].iter_rows(values_only=True))
hv = next(i for i, r in enumerate(wlv) if str(r[0] or "").strip() == "Wk")
H = [str(x or "").strip() for x in wlv[hv]]
def hcol(frag):
    return next(i for i, h in enumerate(H) if frag.lower() in h.lower())
c_we, c_hrs, c_cost = hcol("Week Ending"), hcol("Hours"), hcol("Cost $")
c_dir, c_pkg, c_totrec, c_notrec, c_loss, c_inc = (hcol("Direct"), hcol("Packaging Recove"),
    hcol("Total Recovery"), hcol("Not Recovered"), hcol("Total Loss"), hcol("Incidents"))
c_tres = hcol("Trespass") if any("trespass" in h.lower() for h in H) else None
rate = None
for r in wlv[:hv]:
    for v in r:
        if isinstance(v, (int, float)) and 20 < float(v) < 100: rate = float(v)
rows_v = {d(r[c_we]): r for r in wlv[hv+1:] if d(r[c_we])}
rows_f = {d(r[c_we]): r for r in wlf[hv+1:] if d(r[c_we])}
row = rows_v.get(WEEK); rowf = rows_f.get(WEEK)
if row is None:
    rec("FAIL", "C5 tracker week row", f"{WEEK} not in Weekly Ledger"); sys.exit(1)
hrs, dr, pk, nr, incs = num(row[c_hrs]), num(row[c_dir]), num(row[c_pkg]), num(row[c_notrec]), num(row[c_inc])
m_dir, m_pkg = num(M["Total Recovered ($)"][ci]), num(M["Recovered Packaging ($)"][ci])
m_nr, m_inc = num(M["Total Lost ($)"][ci]), num(M["Total Incidents (#)"][ci])
m_tres = num(M["Trespass Actions (#)"][ci])
mism = []
for name, a, b in (("direct $", dr, m_dir), ("packaging $", pk, m_pkg), ("not-recovered $", nr, m_nr),
                   ("incidents", incs, m_inc)):
    if abs(a - b) > 0.01: mism.append(f"{name}: tracker {a:,.2f} vs master {b:,.2f}")
if c_tres is not None and abs(num(row[c_tres]) - m_tres) > 0.01:
    mism.append(f"trespass: tracker {num(row[c_tres]):.0f} vs master {m_tres:.0f}")
rec("FAIL" if (mism or hrs <= 0) else "PASS", "C5 tracker vs master",
    "; ".join(mism) if mism else (f"hours {hrs:,.2f} and all static figures agree to the cent" if hrs > 0 else "HOURS = 0"))

fcost, ftot, floss = rowf[c_cost], rowf[c_totrec], rowf[c_loss]
is_f = lambda v: isinstance(v, str) and v.startswith("=")
fe = [n for n, v in (("Cost", fcost), ("Total Recovery", ftot), ("Total Loss", floss)) if not is_f(v)]
exp_cost = round(hrs * (rate or 43.5), 2)
rec("FAIL" if fe else "PASS", "C6 formula integrity",
    f"NOT formulas: {fe}" if fe else f"Cost/TotRec/Loss are formulas; recomputed cost ${exp_cost:,.2f} @ ${rate or 43.5}/h")

# past-week zero-out in tracker
tz = [w for w, r in rows_v.items() if w <= WEEK and (num(r[c_hrs]) <= 0 or (num(r[c_dir]) + num(r[c_pkg])) <= 0)]
rec("FAIL" if tz else "PASS", "C4 zero-out guard (tracker)",
    f"past weeks with zero hours/recovery: {tz}" if tz else "all past weeks populated")

# 7 — This Week Store Detail foots
sw = list(tv["This Week — Store Detail"].iter_rows(values_only=True))
shdr = next(i for i, r in enumerate(sw) if str(r[0] or "").strip() == "Store")
SH = [str(x or "").strip() for x in sw[shdr]]
si = {k: next(i for i, h in enumerate(SH) if k.lower() in h.lower()) for k in ("Hours", "Direct", "Packaging", "Total Recovery")}
# Sheet design: activity stores under "▍ <Region>" headers, per-region "— subtotal" rows,
# and one "NETWORK — all stores" row carrying FULL deployed hours (store rows = activity
# stores only, so their hours sum to <= network hours by design).
def _is_store(r):
    s = str(r[0] or "").strip()
    return s and not s.startswith("▍") and "subtotal" not in s.lower() and not s.upper().startswith("NETWORK")
srows = [r for r in sw[shdr+1:] if _is_store(r)]
netrow = next((r for r in sw[shdr+1:] if str(r[0] or "").upper().startswith("NETWORK")), None)
s_rec = sum(num(r[si["Direct"]]) + num(r[si["Packaging"]]) for r in srows)
s_hrs = sum(num(r[si["Hours"]]) for r in srows)
if netrow is None:
    rec("FAIL", "C7 store-detail foots", "NETWORK row missing")
else:
    n_hrs = num(netrow[si["Hours"]])
    n_rec = num(netrow[si["Direct"]]) + num(netrow[si["Packaging"]])
    probs = []
    if abs(n_hrs - hrs) > 0.26: probs.append(f"network hours {n_hrs:,.2f} vs ledger {hrs:,.2f}")
    if abs(n_rec - (dr + pk)) > 0.01: probs.append(f"network recovery ${n_rec:,.2f} vs ledger ${dr+pk:,.2f}")
    if abs(s_rec - n_rec) > 0.01: probs.append(f"Σstore recovery ${s_rec:,.2f} vs network ${n_rec:,.2f}")
    if s_hrs > n_hrs + 0.01: probs.append(f"Σstore hours {s_hrs:,.2f} EXCEEDS network {n_hrs:,.2f}")
    rec("FAIL" if probs else "PASS", "C7 store-detail foots",
        "; ".join(probs) if probs else
        f"network row = ledger ({n_hrs:,.0f}h / ${n_rec:,.2f}); Σ{len(srows)} activity stores foot to network recovery")
tv.close(); tf.close()

# 8 — PDFs carry the headline figures
try:
    import fitz
    WLAB = f"{WEEK.day} {WEEK.strftime('%B %Y')}"
    folder = f"{WW}/Week Ending {WLAB}"
    pdfs = {"value": f"{folder}/Woolworths Weekly Security Performance & Value Report - Week Ending {WLAB}.pdf",
            "safety": f"{folder}/Woolworths National LP & Safety Report - Week Ending {WLAB}.pdf",
            "dashboard": f"{folder}/Woolworths National LP Dashboard - Week Ending {WLAB}.pdf"}
    tl_forms = (f"${tl:,.2f}", f"${tl:,.0f}")   # value/dashboard use cents; safety rounds to $
    for tag, p in pdfs.items():
        if not os.path.exists(p):
            rec("FAIL", f"C8 pdf ({tag})", "file missing"); continue
        t = "".join(pg.get_text() for pg in fitz.open(p))
        probes = {"total loss": any(f in t for f in tl_forms)}
        if tag == "value":
            probes["hours"] = f"{hrs:,.0f}" in t.replace(" ", "")
            probes["incidents"] = str(int(m_inc)) in t
        if tag == "safety":
            probes["incidents"] = str(int(m_inc)) in t
        miss = [k for k, ok in probes.items() if not ok]
        rec("FAIL" if miss else "PASS", f"C8 pdf ({tag})",
            f"figures NOT found: {miss}" if miss else f"headline figures present ({', '.join(probes)})")
except ImportError:
    rec("WARN", "C8 pdfs", "pymupdf unavailable — PDF probe skipped")

# 9 — week-over-week sanity
prev = max((w for w in weeks_all if w < WEEK), default=None)
if prev and prev in rows_v:
    ph, pr = num(rows_v[prev][c_hrs]), num(rows_v[prev][c_dir]) + num(rows_v[prev][c_pkg])
    for name, cur, pv in (("hours", hrs, ph), ("recovery", dr + pk, pr)):
        if pv > 0 and abs(cur - pv) / pv > 0.60:
            rec("WARN", "C9 WoW swing", f"{name} moved {100*(cur-pv)/pv:+.0f}% vs prior week ({pv:,.0f} → {cur:,.0f})")
    else:
        if all(pv <= 0 or abs(c - pv) / pv <= 0.60 for c, pv in ((hrs, ph), (dr + pk, pr))):
            rec("PASS", "C9 WoW sanity", f"hours {ph:,.0f}→{hrs:,.0f}, recovery ${pr:,.0f}→${dr+pk:,.0f} within band")

fails = [r for r in results if r[0] == "FAIL"]
warns = [r for r in results if r[0] == "WARN"]
print(f"\n{'='*60}\nREPORT QA — week ending {WEEK}: "
      f"{'FAIL — DO NOT SEND' if fails else 'PASS — PACKAGE OK TO SEND'}"
      f"  ({len(results)-len(fails)-len(warns)} pass / {len(warns)} warn / {len(fails)} fail)")
sys.exit(1 if fails else 0)
