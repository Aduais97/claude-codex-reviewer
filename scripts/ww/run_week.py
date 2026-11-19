#!/usr/bin/env python3
"""FY27 Woolworths weekly runner — ONE command builds the whole package for the latest week.

Weekly process:
  1. Drop the 4 exports for the new week in ~/Downloads (GIR, Recovered Packaging,
     Guard Deterrent, Connecteam Schedule-Export).
  2. In build_master_v2.py append the new week to WEEK_DEFS, add the 3 source files
     (bounded to the new week) to *_SOURCES, and add the schedule file to WEEK_SCHEDULE.
  3. Run:  python3 run_week.py

This rebuilds the self-reconciling master and regenerates every artefact for CURRENT_WEEK,
then assembles the send-ready 'Client (to send)' folder (Value Report + Tracker).
Internal-only artefacts (Master, National Dashboard, email draft) stay in the week folder.
"""
import subprocess, sys, os, shutil
from datetime import datetime
HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
sys.path.insert(0, HERE)

# Pre-flight: warn loudly if the wired pipeline is behind the calendar (the silent failure
# that let W11/W12 slip — the script had reverted to W10 and nobody noticed).
import build_master_v2 as _bm
_behind = (datetime.now() - _bm.CURRENT_WEEK).days
if _behind > 10:
    print(f"\n⚠  PIPELINE MAY BE BEHIND: latest wired week ends {_bm.CURRENT_WEEK.date()} "
          f"({_behind} days ago).\n   Did you append the new week to WEEK_DEFS / *_SOURCES / WEEK_SCHEDULE "
          f"in build_master_v2.py?\n   Continuing with the weeks currently wired.\n")

def run(script):
    print(f"\n=== {script} ===")
    r = subprocess.run([PY, os.path.join(HERE, script)], capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    print("\n".join(out.strip().splitlines()[-8:]))
    if r.returncode != 0:
        print(f"\n*** {script} FAILED ***\n{r.stderr[-2000:]}"); sys.exit(1)

# master FIRST (its reconciliation gate is the success signal); then all generators
for s in ["build_master_v2.py", "gen_value_report.py", "build_spend_tracker.py",
          "gen_ww_safety_report.py", "gen_fy27_report.py", "gen_fy27_email.py"]:
    run(s)

import build_master_v2 as bm
label = bm.week_label(bm.CURRENT_WEEK)
wkdir = os.path.expanduser(f"~/Desktop/Woolworths /Week Ending {label}")
client = os.path.join(wkdir, "Client (to send)"); os.makedirs(client, exist_ok=True)
deliverables = [
    os.path.join(wkdir, f"Woolworths National LP & Safety Report - Week Ending {label}.pdf"),
    os.path.expanduser("~/Desktop/Woolworths /Woolworths FY27 Deployment & Recovery Tracker.xlsx"),
]
for src in deliverables:
    if os.path.exists(src): shutil.copy2(src, client)

# Permanent source-data backlog — copy every raw export + the master + a pipeline-script
# snapshot into ~/Desktop/Woolworths /_Source Archive so this week can always be rebuilt,
# even after ~/Downloads is cleaned. Flags any missing source (a data-leak alarm).
run("archive_sources.py")

print(f"\n{'='*60}\n✅ FY27 Week {bm.week_num(bm.CURRENT_WEEK)} — Week Ending {label} package built.")
print(f"   CLIENT (send to Glenn):  {client}")
print(f"     • National LP & Safety Report (PDF)")
print(f"     • FY27 Deployment & Recovery Tracker (xlsx)")
print(f"   INTERNAL (do not send):  Value Report + National LP Dashboard, Master Data, email draft — in the week folder.")
