#!/usr/bin/env python3
"""Shared Health & Safety metrics for the WW weekly reports, computed from the reconciled GIR
sources in build_master_v2 — so the National LP & Safety Report and the Weekly Value Report show
identical H&S figures. Returns the reporting week's severity spread, serious/severe counts,
aggression/confrontation count, trespass actions, offenders and Police escalations.
"""
import re, openpyxl
from collections import Counter

def _num(v):
    if v is None: return 0.0
    x = re.sub(r'[^0-9.]', '', str(v)); return float(x) if x else 0.0
def _yes(v): return str(v).strip().lower() in ('yes', 'y', 'true')

_T = {"date": "Date and Time of Incident - Date", "sev": "Incident Severity",
      "off": "Number of offenders/POI", "beh": "Type of non-compliant behaviour",
      "pol": "Were the police informed?", "vt": "Verbal Trespass",
      "ft": "Formal Trespass Notice Served"}
_AGG = {"aggressive behaviour", "threatening language/behaviour", "violent behaviour", "verbal abuse"}

def hs_metrics(bm, WK):
    sev = Counter(); off_tot = 0; inc = 0; pol = vt = ft = 0; confront = 0
    for path, lo, hi in bm.GIR_SOURCES:
        ws = openpyxl.load_workbook(path, read_only=True).active; it = ws.iter_rows(values_only=True)
        low = [str(h).strip().lower() if h else "" for h in next(it)]
        col = {k: next((i for i, h in enumerate(low) if h == v.lower()),
                       next((i for i, h in enumerate(low) if v.lower() in h), None)) for k, v in _T.items()}
        def g(r, k):
            i = col.get(k); return r[i] if i is not None and i < len(r) else None
        for r in it:
            d = bm.pdate(g(r, "date"))
            if not d or bm.week_of(d) != WK: continue
            if not (lo is None or d >= lo) or not (hi is None or d <= hi): continue
            inc += 1
            if g(r, "sev"): sev[str(g(r, "sev")).strip()] += 1
            off_tot += int(_num(g(r, "off")) or 0)
            if _yes(g(r, "pol")): pol += 1
            if _yes(g(r, "vt")): vt += 1
            if _yes(g(r, "ft")): ft += 1
            tags = [t.strip().lower() for t in re.split(r'[;,]', str(g(r, "beh") or ""))]
            if any(t in _AGG for t in tags): confront += 1
    SERIOUS = sum(sev.get(k, 0) for k in ('3', '4', '5')); SEVERE = sev.get('4', 0) + sev.get('5', 0)
    sevline = " · ".join(f"Sev {k}: {sev.get(str(k), 0)}" for k in (1, 2, 3, 4, 5))
    return {"inc": inc, "off": off_tot, "sev": sev, "pol": pol, "vt": vt, "ft": ft,
            "confront": confront, "SERIOUS": SERIOUS, "SEVERE": SEVERE, "sevline": sevline}
