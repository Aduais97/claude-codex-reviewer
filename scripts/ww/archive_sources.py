#!/usr/bin/env python3
"""Permanent SOURCE-DATA BACKLOG for the Woolworths FY27 weekly pipeline.

Why: raw Connecteam exports live transiently in ~/Downloads (which gets cleaned), the
master is overwritten each run, and scripts/ww is untracked in git — so a week's source
data (and the pipeline state that produced it) can be lost, exactly as W11/W12 were. This
tool copies every referenced raw export + the built master + a snapshot of the pipeline
scripts into a permanent, hashed archive with a manifest and a capture ledger, and reports
any MISSING source (a data-leak alarm) plus a per-week coverage table.

Run standalone:  python3 archive_sources.py
Wired as the final step of run_week.py so every weekly build auto-captures its inputs.
"""
import os, sys, shutil, hashlib, json, csv
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_master_v2 as bm

ARCHIVE = os.path.expanduser("~/Desktop/Woolworths /_Source Archive")
RAW     = os.path.join(ARCHIVE, "raw")               # every raw export, deduped by content
SNAP    = os.path.join(ARCHIVE, "pipeline_snapshots")# master + scripts, dated per capture
os.makedirs(RAW, exist_ok=True); os.makedirs(SNAP, exist_ok=True)

SCRIPTS = ["build_master_v2.py", "build_spend_tracker.py", "gen_value_report.py",
           "gen_ww_safety_report.py", "gen_fy27_report.py", "gen_fy27_email.py",
           "convert_timeclock_schedule.py", "convert_tagsheet_schedule.py",
           "run_week.py", "ww_incidents.py", "ww_hs.py", "archive_sources.py"]

def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def copy_if_new(src, dst_dir):
    """Copy src into dst_dir unless an identical (same-hash) copy is already there."""
    if not os.path.exists(src):
        return "MISSING"
    dst = os.path.join(dst_dir, os.path.basename(src))
    if os.path.exists(dst) and sha(dst) == sha(src):
        return "already"
    shutil.copy2(src, dst)
    return "copied"

def within(lo, hi, ws, we):
    return (lo is None or lo <= we) and (hi is None or hi >= ws)

def master_week_totals():
    """Read per-week TOTAL LOSS from the built master (light — no re-aggregation)."""
    try:
        import openpyxl
        wb = openpyxl.load_workbook(bm.OUT, read_only=True, data_only=True)
        ws = wb["National Summary"]
        hdr = list(next(ws.iter_rows(min_row=3, max_row=3, values_only=True)))
        weeks = [h for h in hdr if hasattr(h, "year")]
        for row in ws.iter_rows(min_row=4, max_row=25, values_only=True):
            if row[0] and "TOTAL LOSS" in str(row[0]):
                return {weeks[i]: row[1 + i] for i in range(len(weeks))}
    except Exception:
        pass
    return {}

def main():
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    manifest = {"captured_at": stamp, "raw": [], "missing": [], "snapshot": stamp}

    # 1) archive every referenced raw export (deduped by content hash)
    src_files = [p for (p, _, _) in (bm.GIR_SOURCES + bm.PKG_SOURCES + bm.DET_SOURCES)]
    src_files += [bm.schedule_for(w) for w in bm.WEEKS]
    src_files = list(dict.fromkeys(src_files))          # unique, order-preserving
    for s in src_files:
        status = copy_if_new(s, RAW)
        rec = {"name": os.path.basename(s), "status": status}
        if status == "MISSING":
            manifest["missing"].append(os.path.basename(s))
        else:
            rec["sha256"] = sha(os.path.join(RAW, os.path.basename(s)))[:16]
            rec["bytes"] = os.path.getsize(os.path.join(RAW, os.path.basename(s)))
            manifest["raw"].append(rec)

    # 2) snapshot the built master + pipeline scripts (dated)
    snapdir = os.path.join(SNAP, stamp); os.makedirs(snapdir, exist_ok=True)
    copy_if_new(bm.OUT, snapdir)
    HERE = os.path.dirname(os.path.abspath(__file__))
    for scr in SCRIPTS:
        copy_if_new(os.path.join(HERE, scr), snapdir)

    # 3) per-week coverage — is each stream's source (and the schedule) archived?
    totals = master_week_totals()
    archived = set(os.listdir(RAW))
    def covered(sources, ws, we):
        for (p, lo, hi) in sources:
            if within(lo, hi, ws, we) and os.path.basename(p) in archived:
                return True
        return False
    coverage = []
    for (ws, we) in bm.WEEK_DEFS:
        sched = os.path.basename(bm.schedule_for(we))
        coverage.append({
            "week": bm.week_num(we), "ending": we.strftime("%d %b %Y"),
            "GIR": covered(bm.GIR_SOURCES, ws, we), "PKG": covered(bm.PKG_SOURCES, ws, we),
            "DET": covered(bm.DET_SOURCES, ws, we), "SCHED": sched in archived,
            "total_loss": round(totals.get(we, 0) or 0, 2),
        })
    manifest["coverage"] = coverage

    # 4) write manifest + append the capture ledger
    json.dump(manifest, open(os.path.join(ARCHIVE, "MANIFEST.json"), "w"), indent=2)
    ledger = os.path.join(ARCHIVE, "CAPTURE_LEDGER.csv")
    new = not os.path.exists(ledger)
    with open(ledger, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["captured_at", "week", "ending", "GIR", "PKG", "DET", "SCHED", "total_loss"])
        for c in coverage:
            w.writerow([stamp, c["week"], c["ending"], c["GIR"], c["PKG"], c["DET"], c["SCHED"], c["total_loss"]])

    # 5) report — loud on any gap
    print(f"=== SOURCE ARCHIVE updated @ {stamp} ===")
    print(f"  archive: {ARCHIVE}")
    print(f"  raw exports archived: {len(manifest['raw'])}  | pipeline snapshot: {snapdir}")
    print(f"\n  Per-week source coverage (raw exports still recoverable):")
    print(f"    {'Wk':>3} {'ending':>12}  GIR PKG DET SCHED   total_loss")
    gaps = 0
    for c in coverage:
        flags = "".join(" ✓ " if c[k] else " ✗ " for k in ("GIR", "PKG", "DET"))
        sch = " ✓  " if c["SCHED"] else " ✗  "
        miss = not (c["GIR"] and c["PKG"] and c["DET"] and c["SCHED"])
        gaps += miss
        print(f"    W{c['week']:<2} {c['ending']:>12} {flags}{sch}  ${c['total_loss']:>11,.2f}  {'← RAW GAP (in master snapshot only)' if miss else ''}")
    if manifest["missing"]:
        print(f"\n  ⚠ {len(manifest['missing'])} referenced source(s) NOT on disk (already only in the master snapshot):")
        for m in manifest["missing"]:
            print(f"      - {m}")
    print(f"\n  {'⚠ ' if gaps else '✓ '}{gaps} week(s) missing a raw export on disk "
          f"({'those weeks survive in the master snapshot but cannot be re-derived from raw' if gaps else 'every week fully backed up from raw'}).")
    print(f"  Ledger: {ledger}")

if __name__ == "__main__":
    main()
