#!/usr/bin/env python3
"""SLS RTC pay run — Connecteam unified timesheet -> PayHero CSV import.
Implements the /adjust-paycycle-timesheet skill with all edge-case handling:
  - employee name carry-forward (grouped cells), title-case + whitespace-collapse
  - permanent exclusions (Faiez Idais, Zac Shannon); drop leave/public-holiday rows
  - data-fault resolution: phantom zero-duration drop; cross-day auto-clock-out -> co-guard mode;
    missing-out -> own next shift's start (else co-guard mode); abort on anything unresolved
  - overlap resolution: trim roving edge-overlaps to the next shift's start; FLAG (abort) on a
    fully-contained overlap that needs a human call
  - two-pass 30-min break logic (>=6h/day, gap-aware; deduct shortfall on the longest shift)
  - HARD GATE: every row has parseable In/Out, End>Start, same-day, before writing

Usage: python3 adjust_paycycle_timesheet.py "<unified_time_sheet_report_YYYY-MM-DD_YYYY-MM-DD.xlsx>"
Out:   ~/Downloads/PayHero_-_Timesheet_Import_Template_<period>.csv
"""
import openpyxl, csv, datetime, sys, re, os, glob, shutil
from collections import defaultdict, Counter

if len(sys.argv) > 1:
    SRC = os.path.expanduser(sys.argv[1])
else:  # convenience: newest unified timesheet-format export in Downloads
    cands = sorted(glob.glob(os.path.expanduser("~/Downloads/unified_time_sheet_report_*.xlsx")), key=os.path.getmtime)
    if not cands: sys.exit("usage: adjust_paycycle_timesheet.py <unified_time_sheet_report_*.xlsx>")
    SRC = cands[-1]
_m = re.search(r'(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})', os.path.basename(SRC))
PERIOD = f"{_m.group(1)}_{_m.group(2)}" if _m else "period"
# File into ~/Desktop/SLS-RTC/Finance/Pay Runs/<DD:MM:YY>/ where the folder date = period-end + 1 day
# (matches the established convention). Folder holds the source export + a base-named PayHero CSV.
if _m:
    _end = datetime.datetime.strptime(_m.group(2), "%Y-%m-%d").date()
    OUTDIR = os.path.expanduser("~/Desktop/SLS-RTC/Finance/Pay Runs/" + (_end + datetime.timedelta(days=1)).strftime("%d:%m:%y"))
    os.makedirs(OUTDIR, exist_ok=True)
    OUT = os.path.join(OUTDIR, "PayHero_-_Timesheet_Import_Template.csv")
    try: shutil.copy2(SRC, os.path.join(OUTDIR, os.path.basename(SRC)))  # keep the source export with the run
    except Exception: pass
else:
    OUT = os.path.expanduser("~/Downloads/PayHero_-_Timesheet_Import_Template.csv")
EXCLUDE = {"faiez idais", "zac shannon"}
FN, LN, TYPE, SD, IN, ED, OUT_ = 0, 1, 2, 4, 5, 7, 8   # unified timesheet column indices

def norm(fn, ln): return " ".join(f"{str(fn or '').strip()} {str(ln or '').strip()}".split()).title()
def t2m(v):
    if v is None: return None
    if isinstance(v, datetime.time): return v.hour*60+v.minute
    if isinstance(v, (int, float)): return round(v*1440) if 0 <= v <= 1 else None
    s = str(v).strip()
    if not s: return None
    try: p = s.split(":"); return int(p[0])*60+int(p[1])
    except Exception: return None
def m2t(m): return f"{m//60}:{m%60:02d}"

ws = openpyxl.load_workbook(SRC, data_only=True).active
rows = list(ws.iter_rows(values_only=True))
hdr = [str(h or "").strip().lower() for h in rows[0]]
if not all(c in hdr for c in ("type", "in", "out", "start date")):
    sys.exit(f"ERROR: {os.path.basename(SRC)} is not a timesheet-format export (needs Type/In/Out/Start Date)")

# ---- Pass 0: parse + carry-forward name; drop excluded / leave / PH / no-punch ----
recs = []; name = ""; excl_ct = Counter(); leave_log = defaultdict(list); ph_ct = 0; nopunch = []
for ri, r in enumerate(rows[1:], 2):
    if (r[FN] and str(r[FN]).strip()) or (r[LN] and str(r[LN]).strip()): name = norm(r[FN], r[LN])
    typ = str(r[TYPE] or "").strip(); tl = typ.lower()
    if name.lower() in EXCLUDE: excl_ct[name] += 1; continue
    if "leave" in tl or "holiday" in tl:
        (leave_log[name].append(typ) if "public holiday" not in tl else None)
        if "public holiday" in tl: ph_ct += 1
        continue
    im, om = t2m(r[IN]), t2m(r[OUT_])
    if im is not None: im = round(im/15)*15   # round punches to nearest quarter-hour (Ahmad, 12 Aug 2026)
    if om is not None: om = round(om/15)*15
    sd = str(r[SD])[:10] if r[SD] else None; ed = str(r[ED])[:10] if r[ED] else None
    if im is None and om is None: nopunch.append((ri, name)); continue
    recs.append({"row": ri, "name": name, "type": typ, "sd": sd, "ed": ed, "in": im, "out": om, "break": ""})

def valid(x): return x["in"] is not None and x["out"] is not None and x["ed"] == x["sd"] and x["out"] > x["in"]
outmap = defaultdict(list); ins_empday = defaultdict(list)
for x in recs:
    if valid(x): outmap[(x["type"], x["sd"])].append(x["out"])
    if x["in"] is not None and x["sd"]: ins_empday[(x["name"], x["sd"])].append(x["in"])

# ---- resolve data faults ----
resolutions = []; drops = []; keep = []; unresolved = []
for x in recs:
    if valid(x): keep.append(x); continue
    if x["in"] is not None and x["out"] is not None and x["ed"] == x["sd"] and x["out"] <= x["in"]:
        sib = [y for y in recs if y is not x and y["name"] == x["name"] and y["type"] == x["type"] and y["sd"] == x["sd"] and valid(y)]
        if sib: drops.append((x, "zero/dup phantom — real shift already present")); continue
        unresolved.append((x, "zero-duration, no sibling")); continue
    if x["in"] is not None and x["ed"] and x["sd"] and x["ed"] != x["sd"]:      # cross-day auto-clock-out
        peers = outmap.get((x["type"], x["sd"]), [])
        if peers:
            mode = Counter(peers).most_common(1)[0][0]; x["out"], x["ed"] = mode, x["sd"]
            resolutions.append((x, f"cross-day -> {m2t(mode)} (co-guard mode)")); keep.append(x); continue
        unresolved.append((x, "cross-day, no co-guard")); continue
    if x["in"] is not None and x["out"] is None:                                # missing out
        nexts = [i for i in ins_empday[(x["name"], x["sd"])] if i > x["in"]]
        if nexts:
            x["out"], x["ed"] = min(nexts), x["sd"]
            resolutions.append((x, f"missing-out -> {m2t(min(nexts))} (own next shift)")); keep.append(x); continue
        peers = outmap.get((x["type"], x["sd"]), [])
        if peers:
            mode = Counter(peers).most_common(1)[0][0]; x["out"], x["ed"] = mode, x["sd"]
            resolutions.append((x, f"missing-out -> {m2t(mode)} (co-guard mode)")); keep.append(x); continue
        unresolved.append((x, "missing-out, no anchor")); continue
    unresolved.append((x, "missing-in / other"))
if unresolved:
    print("ABORT — unresolved rows (need manual finish time):")
    for x, why in unresolved: print(f"  row {x['row']} {x['name']} @ {x['type']} {x['sd']} In={x['in'] and m2t(x['in'])} Out={x['out'] and m2t(x['out'])} :: {why}")
    sys.exit(1)

# ---- overlap resolution (trim roving edges; flag containment) ----
# INTERNAL_CONTAINED: internal / non-billable blocks that AUTO-DROP when found fully inside a real
# client-site shift (guard can't be in two places at once; the site shift is the paid time — the
# internal hour would double-count). Ahmad, 19 Aug 2026: e.g. a "HEAD OFFICE SLSRTC" 13:00-14:00
# sitting inside a Kilbirnie Woolworths 10:00-19:00 -> drop the internal hour, pay the 9h site shift.
# ONLY the internal-inside-a-site pattern auto-resolves; every OTHER containment still aborts for a human.
INTERNAL_CONTAINED = ("head office",)
byday = defaultdict(list)
for x in keep: byday[(x["name"], x["sd"])].append(x)
ov_trim = []; ov_flag = []
for (nm, d), sh in byday.items():
    sh.sort(key=lambda s: (s["in"], s["out"]))       # tie-break on end so a shorter same-start block sorts first
    for k in range(len(sh)-1):
        a, b = sh[k], sh[k+1]
        if b["in"] < a["out"]:                        # a and b overlap
            at = str(a["type"]).lower(); bt = str(b["type"]).lower()
            a_int = any(kw in at for kw in INTERNAL_CONTAINED)
            b_int = any(kw in bt for kw in INTERNAL_CONTAINED)
            a_in_b = b["in"] <= a["in"] and a["out"] <= b["out"]   # a's span sits inside b's
            b_in_a = a["in"] <= b["in"] and b["out"] <= a["out"]   # b's span sits inside a's
            if b_in_a and b_int and not a_int:        # internal block inside a real site shift -> auto-drop
                b["_drop_contained"] = True
                drops.append((b, f"internal block inside {a['type']} {m2t(a['in'])}-{m2t(a['out'])} — auto-dropped (site shift is the paid time)"))
            elif a_in_b and a_int and not b_int:      # same, but the internal block sorted first (equal start time)
                a["_drop_contained"] = True
                drops.append((a, f"internal block inside {b['type']} {m2t(b['in'])}-{m2t(b['out'])} — auto-dropped (site shift is the paid time)"))
            elif b["out"] <= a["out"]:                # a non-internal fully-contained overlap -> human decision
                ov_flag.append((nm, d, a["type"], a["row"], b["type"], b["row"]))
            else:                                     # partial edge overlap -> trim earlier out to next start
                old = a["out"]; a["out"] = b["in"]
                ov_trim.append((nm, d, a["type"], a["row"], m2t(old), m2t(a["out"]), b["type"], b["row"]))
if ov_flag:
    print("FLAG — full-containment overlaps need a decision (CSV NOT written):")
    for nm, d, ta, ra, tb, rb in ov_flag: print(f"  {nm} {d}: {ta} row{ra}  vs  {tb} row{rb} (inside it)")
    sys.exit(2)
# remove auto-dropped internal-contained blocks and rebuild the per-day map (so break/total logic is correct)
if any(x.get("_drop_contained") for x in keep):
    keep = [x for x in keep if not x.get("_drop_contained")]
    byday = defaultdict(list)
    for x in keep: byday[(x["name"], x["sd"])].append(x)

# ---- two-pass break logic (+ >11h/day confirmation flag: possible missed clock-out) ----
over14 = []; over11 = []
for (nm, d), sh in byday.items():
    sh.sort(key=lambda s: s["in"])
    for s in sh:
        if (s["out"]-s["in"]) > 14*60: over14.append((s["row"], nm, d, (s["out"]-s["in"])/60))
    total = sum(s["out"]-s["in"] for s in sh)/60
    if total > 11:
        over11.append((nm, d, round(total, 2), [(m2t(s["in"]), m2t(s["out"]), s["type"]) for s in sh]))
    if total >= 6:
        gap = sum(max(0, sh[k+1]["in"]-sh[k]["out"]) for k in range(len(sh)-1))
        if gap < 30:
            max(sh, key=lambda s: s["out"]-s["in"])["break"] = round((30-gap)/60, 2)

# ---- HARD GATE ----
for x in keep:
    assert x["in"] is not None and x["out"] is not None and x["ed"] == x["sd"] and x["out"] > x["in"], f"gate fail row {x['row']}"

# ---- sort (name asc, date desc) + write ----
keep.sort(key=lambda x: (x["name"], -datetime.datetime.strptime(x["sd"], "%Y-%m-%d").timestamp()))
with open(OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Employee", "Work Name", "Date", "Start Time", "End Time", "Employee Email", "Notes", "Duration", "Break Duration", "Units"])
    for x in keep:
        dt = datetime.datetime.strptime(x["sd"], "%Y-%m-%d").strftime("%d/%m/%y")
        w.writerow([x["name"], "Default Work", dt, m2t(x["in"]), m2t(x["out"]), "", "", "", x["break"] if x["break"] else "", ""])

# ---- summary ----
emps = sorted(set(x["name"] for x in keep)); gross = sum((x["out"]-x["in"])/60 for x in keep)
brk_rows = [x for x in keep if x["break"]]; brk = sum(x["break"] for x in brk_rows)
print("=== DATA RESOLUTIONS ===")
for x, why in resolutions: print(f"  ✓ row {x['row']} {x['name']} @ {x['type']} {x['sd']}: {why}")
for x, why in drops: print(f"  ✗ drop row {x['row']} {x['name']} @ {x['type']} {x['sd']}: {why}")
for t in ov_trim: print(f"  ✂ overlap {t[0]} {t[1]}: {t[2]} row{t[3]} out {t[4]}->{t[5]} (moved to {t[6]} row{t[7]})")
print(f"\n=== SUMMARY — SLS pay run {PERIOD} ===")
print(f"  rows written : {len(keep)}")
print(f"  employees    : {len(emps)}")
print(f"  gross hours  : {gross:.2f}  (net after {brk:.2f}h breaks = {gross-brk:.2f})")
print(f"  breaks       : {len(brk_rows)} rows, {brk:.2f}h deducted")
print(f"  excluded     : " + (", ".join(f"{k} x{v}" for k, v in excl_ct.items()) or "none"))
print(f"  leave dropped: {sum(len(v) for v in leave_log.values())} (" + "; ".join(f"{k}:{len(v)}" for k, v in leave_log.items()) + f")   PH rows: {ph_ct}")
print(f"  no-punch drop: {len(nopunch)}")
print(f"  >14h shifts  : {over14 or 'none'}")
print(f"  overlaps     : {len(ov_trim)} edge-trims applied, {len(ov_flag)} flagged")
print(f"  wrote        : {OUT}")
if over11:
    print(f"\n  ⚠️  CONFIRM — {len(over11)} guard-day(s) OVER 11h (possible missed clock-out — confirm genuine, or say cap):")
    for nm, d, tot, shifts in sorted(over11, key=lambda z: -z[2]):
        print(f"     {nm} — {d} — {tot}h:  " + "  ·  ".join(f"{i}-{o} {t[:16]}" for i, o, t in shifts))
else:
    print("\n  ✓ no guard over 11h in a day")
