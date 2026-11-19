#!/usr/bin/env python3
"""Bunnings MONTHLY NRO metrics from a raw Connecteam GIR (our-staff DB; resolves columns by
HEADER NAME because raw-export order differs from the consolidated master) + tag-sheet hours.
Emits nro_metrics_<TAG>.json in the exact shape nro_report.py consumes.

Usage: python3 monthly_metrics.py <GIR.xlsx> <tagsheet.xlsx> <YYYY-MM> <TAG> "<period label>" "<phrase>"
"""
import openpyxl, sys, re, json, os, datetime
from datetime import timedelta
from collections import defaultdict, Counter
from itertools import combinations

GIR, TAG_XLSX, MONTH, TAG, PLABEL, PHRASE = sys.argv[1:7]
SHIFT_XLSX = sys.argv[7] if len(sys.argv) > 7 else None   # per-shift timesheet → co-worked hours for pairings
AUROR_CSV = sys.argv[8] if len(sys.argv) > 8 else None     # Auror Events.csv → reconciliation stat (truthful coverage)
YY, MM = int(MONTH[:4]), int(MONTH[5:7])
HERE = os.path.dirname(os.path.abspath(__file__))
REGION_CANON = {"hamilton": "Waikato", "te rapa": "Waikato", "dunedin": "Otago"}

def num(v):
    try: return float(str(v or 0).replace(",", "").replace("$", "") or 0)
    except: return 0.0
def pdate(v):
    if isinstance(v, datetime.datetime): return v.date()
    if isinstance(v, datetime.date): return v
    return None
def sev(v):
    m = re.search(r"[1-5]", str(v or "")); return int(m.group()) if m else None
def canon(v):
    s = str(v or "").strip(); return REGION_CANON.get(s.lower(), s or "Unspecified")
def htx(v): return 1 if str(v or "").strip() else 0
def thr(v):
    m = re.match(r"\s*(\d{1,2}):(\d{2})", str(v or "")); return int(m.group(1)) if m else None

# ---- GIR (our staff), resolve by header ----
ws = openpyxl.load_workbook(GIR, read_only=True, data_only=True).active
rows = list(ws.iter_rows(values_only=True)); H = [str(h or "").strip().lower() for h in rows[0]]
def col(name): return next(i for i, h in enumerate(H) if name in h)
c_au, c_d, c_t = col("auror report number"), col("date and time of incident - date"), col("date and time of incident - time")
c_reg, c_site, c_sev = col("region of site"), col("bunnings site"), col("incident severity")
c_rec, c_stol = col("recovered reciept value"), col("estimated stolen value")
c_co, c_sup, c_dm, c_sm, c_g = (col("checkout operator signature"), col("supervisor signature"),
    col("duty manager signature"), col("store manager signature"), col("guard signature"))

R = [r for r in rows[1:] if (lambda d: d and d.year == YY and d.month == MM)(pdate(r[c_d]))]

# ---- ADOPT AUROR AS TRUTH (Ahmad, 30 Oct 2026): per matched event take the GREATER of the two
# systems' values; append covert-team Auror events missing from the GIR (union count).
# Cross-check the ID list against reconcile_auror_gir.py each month. ----
if AUROR_CSV and os.path.exists(os.path.expanduser(AUROR_CSV)):
    import csv as _csv2
    _ar = list(_csv2.reader(open(os.path.expanduser(AUROR_CSV), newline='', encoding='utf-8-sig')))
    _ah = [x.strip().upper() for x in _ar[0]]
    _ai = {k: _ah.index(k) for k in ("EVENTID", "OCCURREDAT", "STORENAME", "RECOVEREDVALUE",
                                     "TOTALVALUE", "EVENTREPORTEDBY", "EVENTREPORTEDBYJOBTITLE")}
    def _anum(v):
        try: return float(str(v or 0).replace(",", "") or 0)
        except: return 0.0
    def _adate(v):
        s = str(v or "").strip()
        m = re.match(r"(\d{4})-(\d{2})-(\d{2})", s)      # ISO — Auror exports from Oct 2026
        if m: return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)  # d/m/yyyy — earlier exports
        return datetime.date(int(m.group(3)), int(m.group(2)), int(m.group(1))) if m else None
    _norm = lambda v: re.sub(r"[^0-9]", "", str(v or ""))
    _am = {}
    for _r in _ar[1:]:
        if len(_r) > max(_ai.values()):
            _am[_r[_ai["EVENTID"]].strip()] = _r
    R = [list(r) for r in R]
    _gids = set()
    for r in R:
        k = _norm(r[c_au]); _gids.add(k)
        a = _am.get(k)
        if a:
            arec, atot = _anum(a[_ai["RECOVEREDVALUE"]]), _anum(a[_ai["TOTALVALUE"]])
            grec, gidf = num(r[c_rec]), num(r[c_rec]) + num(r[c_stol])
            nrec = max(grec, arec)
            nidf = max(gidf, atot, nrec)
            r[c_rec], r[c_stol] = nrec, nidf - nrec
    _gnames = {str(r[1] or "").strip().lower().split()[0] for r in R if str(r[1] or "").strip()}
    _store_region = {str(r[c_site]).strip().lower(): r[c_reg] for r in R}
    for _k, _a in _am.items():
        _d = _adate(_a[_ai["OCCURREDAT"]])
        if not _d or _d.year != YY or _d.month != MM or _k in _gids:
            continue
        # OUR team = 'covert' in name/title only (a first-name fallback once swept in a
        # Bunnings Operations Manager named Patrick — never match on first name alone)
        _who = (str(_a[_ai["EVENTREPORTEDBY"]]) + " " + str(_a[_ai["EVENTREPORTEDBYJOBTITLE"]])).lower()
        if ("covert" in _who or "cover security" in _who):
            _store = str(_a[_ai["STORENAME"]]).strip()   # GIR keeps the "Bunnings " prefix
            if "hamilton south" in _store.lower(): _store = "Bunnings South Hamilton"
            _row = [None] * len(H)
            _row[c_au] = _k; _row[c_d] = datetime.datetime(_d.year, _d.month, _d.day)
            _row[c_site] = _store
            _row[c_reg] = _store_region.get(_store.lower(), "")
            _row[c_rec] = _anum(_a[_ai["RECOVEREDVALUE"]])
            _row[c_stol] = max(_anum(_a[_ai["TOTALVALUE"]]) - _anum(_a[_ai["RECOVEREDVALUE"]]), 0)
            _row[1] = str(_a[_ai["EVENTREPORTEDBY"]] or "").strip()
            R.append(_row)
    print(f"  [adopt-auror] union events: {len(R)}; greater-value adoption applied")
n = len(R)
dts = sorted(pdate(r[c_d]) for r in R); lo, hi = dts[0], dts[-1]
rec = sum(num(r[c_rec]) for r in R); stolen = sum(num(r[c_stol]) for r in R); ident = rec + stolen
sites = sorted({str(r[c_site]).strip() for r in R if str(r[c_site] or "").strip()})
regions = sorted({canon(r[c_reg]) for r in R})
sevc = Counter(s for s in (sev(r[c_sev]) for r in R) if s)
sev3plus = sum(v for k, v in sevc.items() if k >= 3); sev45 = sum(v for k, v in sevc.items() if k >= 4)
auror = sum(htx(r[c_au]) for r in R)
timed = [(pdate(r[c_d]), thr(r[c_t])) for r in R]; timed = [(d, h) for d, h in timed if d and h is not None]
in_win = sum(1 for d, h in timed if 12 <= h < 18)
dow = Counter(d.strftime("%A") for d, h in timed); cell = Counter((d.strftime("%A"), h) for d, h in timed)
hot = cell.most_common(1)[0] if cell else None
store_rec = defaultdict(float); store_inc = Counter(); store_sev3 = Counter(); heat = defaultdict(int)
for r in R:
    s = str(r[c_site] or "").strip(); d = pdate(r[c_d]); h = thr(r[c_t])
    if s: store_rec[s] += num(r[c_rec]); store_inc[s] += 1
    if s and (sev(r[c_sev]) or 0) >= 3: store_sev3[s] += 1
    if d and h is not None: heat[(d.weekday(), h)] += 1
top6 = sorted(store_rec.items(), key=lambda x: -x[1])[:6]
top6_share = sum(v for _, v in top6) / rec * 100 if rec else 0
reg_rec = defaultdict(float); reg_inc = Counter()
for r in R: rg = canon(r[c_reg]); reg_rec[rg] += num(r[c_rec]); reg_inc[rg] += 1
signoff = {"Guard": sum(htx(r[c_g]) for r in R) / n * 100, "Duty Manager": sum(htx(r[c_dm]) for r in R) / n * 100,
    "Checkout Operator": sum(htx(r[c_co]) for r in R) / n * 100, "Supervisor": sum(htx(r[c_sup]) for r in R) / n * 100,
    "Store Manager": sum(htx(r[c_sm]) for r in R) / n * 100}
# weekly trend (month span < 75 days)
keyf = lambda d: (d - timedelta(days=d.weekday())).strftime("%Y-%m-%d")
labf = lambda k: datetime.datetime.strptime(k, "%Y-%m-%d").strftime("%d %b")
tinc = Counter(); trec = defaultdict(float)
for r in R:
    d = pdate(r[c_d]); k = keyf(d); tinc[k] += 1; trec[k] += num(r[c_rec])
trend = [{"key": k, "label": labf(k), "incidents": tinc[k], "recovered": round(trec[k], 2)} for k in sorted(tinc)]

# ---- teamwork: who works best together (Full name + Witness on each incident) ----
c_fn, c_wit = col("full name"), col("witness")
_NF = {"nirajkumar katwala": "NirajKumar Katwala", "niraj": "NirajKumar Katwala",
       "nirajkumar": "NirajKumar Katwala",
       "simmerjit singh brar": "Simmerjit Singh Brar", "simmer": "Simmerjit Singh Brar",
       "simmerjit singh": "Simmerjit Singh Brar",
       "pat manu": "Patrick Manu", "patrick manu": "Patrick Manu", "pene tuiketei": "Pene Tuiketei",
       "farshid hakimi": "Farshid Hakimi", "fashid hakimi": "Farshid Hakimi", "charlie maka": "Charlie Maka",
       "siositeni maka": "Siositeni Maka", "viliami fangaiuiha": "Viliami Fangaiuiha", "james taylor": "James Taylor",
       "jordan martin": "Jordan Martin", "jake webby": "Jake Webby", "ben conner": "Ben Conner",
       "benn conner": "Ben Conner", "eru nehana": "Eru Nehana",
       "don tehe": "Don Tamasese"}  # witness misnaming; George Tehe is a different person
def _op(s):
    s = re.sub(r"\s+", " ", str(s or "").strip()); return _NF.get(s.lower(), s.title() if s else "")
op_inc = Counter(); op_rec = defaultdict(float); team_inc = Counter(); team_rec = defaultdict(float)
for r in R:
    O = set()
    for i in (c_fn, c_wit):
        for part in str(r[i] or "").split(","):
            nm = _op(part)
            if nm: O.add(nm)
    rc = num(r[c_rec])
    for o in O: op_inc[o] += 1; op_rec[o] += rc
    for a, b in combinations(sorted(O), 2): team_inc[(a, b)] += 1; team_rec[(a, b)] += rc

# ---- hours: total (tag-sheet store headers) + per-operative (tag-sheet guard rows) ----
trows = list(openpyxl.load_workbook(TAG_XLSX, read_only=True, data_only=True).active.iter_rows(values_only=True))
TH = [str(x or "").strip().lower() for x in trows[0]]
ti_job, ti_perf, ti_h = TH.index("job"), TH.index("performed by"), TH.index("hours")
win_hours = round(sum(num(r[ti_h]) for r in trows[1:] if str(r[ti_job] or "").strip()), 1)  # store headers only
op_hours = defaultdict(float)
for r in trows[1:]:
    if str(r[ti_job] or "").strip(): continue          # skip store-header row
    nm = _op(r[ti_perf])
    if nm: op_hours[nm] += num(r[ti_h])

# ---- co-worked hours per pair (per-shift timesheet: overlap of shifts at same store+day) ----
co_hours = defaultdict(float)
if SHIFT_XLSX and os.path.exists(os.path.expanduser(SHIFT_XLSX)):
    sr = list(openpyxl.load_workbook(os.path.expanduser(SHIFT_XLSX), read_only=True, data_only=True)['All Employees'].iter_rows(values_only=True))
    SH = [str(x or "").strip() for x in sr[0]]
    ifn, iln, ityp, isd, iin, iout = (SH.index('First name'), SH.index('Last name'), SH.index('Type'),
        SH.index('Start Date'), SH.index('In'), SH.index('Out'))
    def _t2m(v):
        if isinstance(v, datetime.time): return v.hour * 60 + v.minute
        try: p = str(v).split(":"); return int(p[0]) * 60 + int(p[1])
        except: return None
    sh = defaultdict(list); cur = ""
    for r in sr[1:]:
        f = str(r[ifn] or '').strip(); l = str(r[iln] or '').strip()
        if f or l: cur = _op(f"{f} {l}")
        typ = str(r[ityp] or ""); d = r[isd]
        if "bunning" not in typ.lower() or not isinstance(d, (datetime.datetime, datetime.date)): continue
        a, b = _t2m(r[iin]), _t2m(r[iout])
        if a is None or b is None or b <= a: continue
        sh[(re.sub(r"\s+", " ", typ).strip(), d.date() if isinstance(d, datetime.datetime) else d)].append((cur, a, b))
    for lst in sh.values():
        for (n1, a1, b1), (n2, a2, b2) in combinations(lst, 2):
            if n1 == n2: continue
            ov = max(0, min(b1, b2) - max(a1, a2))
            if ov > 0: co_hours[tuple(sorted((n1, n2)))] += ov / 60

# ---- per-hour ROI: operatives ranked by $/hr, pairs by $/co-hour (min hours to rank first) ----
MIN_OP_H, MIN_CO_H = 20, 15
def _pdiv(a, b): return round(a / b, 2) if b else 0.0
# NB: rec_per_hr / rec_per_cohr are INTERNAL only (client guardrail bans recovery÷hours). The
# CLIENT report ranks + shows the $-free efficiency measure (incidents per 100 hours worked).
operatives = sorted(
    [{"name": o, "incidents": op_inc[o], "recovered": round(op_rec[o], 2), "hours": round(op_hours.get(o, 0), 1),
      "rec_per_hr": _pdiv(op_rec[o], op_hours.get(o, 0)),
      "inc_per_100h": round(op_inc[o] / op_hours[o] * 100, 1) if op_hours.get(o, 0) else 0} for o in op_inc],
    key=lambda x: (x["hours"] >= MIN_OP_H, x["inc_per_100h"]), reverse=True)[:10]
teams = sorted(
    [{"a": a, "b": b, "incidents": team_inc[(a, b)], "recovered": round(team_rec[(a, b)], 2),
      "cohours": round(co_hours.get((a, b), 0), 1), "rec_per_hr": _pdiv(team_rec[(a, b)], co_hours.get((a, b), 0)),
      "inc_per_100cohr": round(team_inc[(a, b)] / co_hours[(a, b)] * 100, 1) if co_hours.get((a, b), 0) else 0}
     for (a, b) in team_inc],
    key=lambda x: (x["cohours"] >= MIN_CO_H, x["inc_per_100cohr"]), reverse=True)[:8]

# ---- reconciliation to Auror (client system of record): truthful coverage, not "100%" ----
recon = {"captured": n, "reconciled": n, "reconciled_pct": 100.0, "bad": 0}
if AUROR_CSV and os.path.exists(os.path.expanduser(AUROR_CSV)):
    import csv as _csv
    arows = list(_csv.reader(open(os.path.expanduser(AUROR_CSV), newline='', encoding='utf-8-sig')))
    eidx = arows[0].index("EVENTID"); auror_ids = {str(r[eidx]).strip() for r in arows[1:] if len(r) > eidx}
    def _akey(v):
        m = re.search(r"e?\s*(\d{5,})", str(v or "").lower()); return m.group(1) if m else None
    caps = sum(1 for r in R if str(r[c_au] or "").strip()); ok = 0; bad = 0
    for r in R:
        k = _akey(r[c_au])
        if k and k in auror_ids: ok += 1
        else: bad += 1
    recon = {"captured": caps, "reconciled": ok, "reconciled_pct": round(ok / n * 100, 1) if n else 0, "bad": bad}

M = {"tag": TAG, "kicker": "MONTH IN REVIEW", "period_label": PLABEL, "phrase": PHRASE, "foot": TAG, "recon": recon,
    "date_lo": str(lo), "date_hi": str(hi), "incidents": n, "sites": len(sites), "regions": len(regions),
    "recovered": round(rec, 2), "stolen": round(stolen, 2), "identified": round(ident, 2),
    "recovery_pct": round(rec / ident * 100, 1) if ident else 0, "auror_pct": round(auror / n * 100, 1),
    "severity": {str(k): sevc.get(k, 0) for k in range(1, 6)}, "sev3plus": sev3plus, "sev45": sev45,
    "risk_window_pct": round(in_win / len(timed) * 100, 1) if timed else 0,
    "peak_day": dow.most_common(1)[0] if dow else None,
    "hottest_cell": {"day": hot[0][0], "hour": hot[0][1], "count": hot[1]} if hot else None,
    "heat": {f"{d}_{h}": c for (d, h), c in heat.items()},
    "top6": [{"store": s, "recovered": round(v, 2), "share": round(v / rec * 100, 1) if rec else 0,
              "incidents": store_inc[s], "sev3": store_sev3[s]} for s, v in top6],
    "top6_share": round(top6_share, 1),
    "regional": sorted([{"region": k, "recovered": round(v, 2), "incidents": reg_inc[k]} for k, v in reg_rec.items()], key=lambda x: -x["recovered"]),
    "signoff": {k: round(v, 1) for k, v in signoff.items()},
    "serious_hotspots": sorted([{"store": s, "sev3": c} for s, c in store_sev3.items()], key=lambda x: -x["sev3"])[:5],
    "trend": trend, "trend_unit": "week",
    "operatives": operatives, "teams": teams, "operatives_active": len(op_inc),
    "hours_window": win_hours, "inc_per_100h": round(n / win_hours * 100, 2) if win_hours else 0,
    "hours_per_inc": round(win_hours / n, 1) if n else 0}
outp = os.path.join(HERE, f"nro_metrics_{TAG}.json"); json.dump(M, open(outp, "w"), indent=1, default=str)
print(f"[{TAG}] {PLABEL}: {n} inc | ${rec:,.0f} rec / {M['recovery_pct']}% | sev3+ {sev3plus} | top6 {top6_share:.1f}% "
      f"| {len(sites)} sites / {len(regions)} regions | hours {win_hours:,.0f}h -> {M['inc_per_100h']} inc/100h | {lo}..{hi}")
print(f"  wrote {outp}")
