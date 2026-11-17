#!/usr/bin/env python3
"""FY27 weekly Loss-Prevention report (client-facing) — region-grouped, branded, A4 PDF.
Reads structured data straight from build_master_v2.aggregate() so it ties to the master."""
import os, base64
from collections import defaultdict
from datetime import datetime
from playwright.sync_api import sync_playwright
import build_master_v2 as bm

LOGO = os.path.expanduser("~/Desktop/SLS-RTC/Operations/Analytics/assets/slsrtc_logo_hd.png")
WEEK_END = bm.CURRENT_WEEK
WSTART = bm.week_start(WEEK_END); WNUM = bm.week_num(WEEK_END)
WEEK_LABEL = f"Week Ending {bm.week_label(WEEK_END)}"
FY_LABEL = f"FY27 · Week {WNUM} ({WSTART.day}–{WEEK_END.day} {WEEK_END.strftime('%B %Y')})"
OUTDIR = os.path.expanduser(f"~/Desktop/Woolworths /{WEEK_LABEL}")
OUT = f"{OUTDIR}/Woolworths National LP Dashboard - {WEEK_LABEL}.pdf"

DET_PENDING = False  # deterrent export received

agg, store_region, regions = bm.aggregate()
week = WEEK_END


def money(v):
    return f"${v:,.2f}"


def num(v):
    return f"{int(round(v)):,}"


nat = bm.rollup([a for (w, s), a in agg.items() if w == week])
reg_roll = {r: bm.rollup([a for (w, s), a in agg.items() if w == week and store_region.get(s) == r]) for r in regions}
stores_by_region = defaultdict(list)
for (w, s), a in agg.items():
    if w == week:
        stores_by_region[store_region.get(s)].append((s, a))

logo_b64 = base64.b64encode(open(LOGO, "rb").read()).decode()
det_cell = '<span class="pend">pending*</span>' if DET_PENDING else num(nat["det"])
det_ind_cell = '<span class="pend">pending*</span>' if DET_PENDING else num(nat["det_ind"])


# ---- headline tiles ---- (Total Loss = single $ headline; recovery shown as a rate)
REC_PCT = (nat["rec"] + nat["pkg"]) / nat["total_loss"] * 100 if nat["total_loss"] else 0
tiles = [
    ("TOTAL LOSS", money(nat["total_loss"]), "loss"),
    ("Recovered", f"{REC_PCT:.1f}%", ""),
    ("Recovered Packaging", money(nat["pkg"]), ""),
    ("Incidents", num(nat["inc"]), ""),
    ("Offenders", num(nat["off"]), ""),
    ("Deterrents", det_cell, "pendtile" if DET_PENDING else ""),
    ("Trespass Actions", num(nat["tres"]), ""),
]
tile_html = "".join(
    f'<div class="tile {cls}"><div class="big">{val}</div><div class="lab">{lab}</div></div>'
    for lab, val, cls in tiles)


# ---- region performance table ----
reg_rows = ""
for r in regions:
    d = reg_roll[r]
    det = '<span class="pend">—*</span>' if DET_PENDING else num(d["det"])
    reg_rows += (f'<tr><td class="rgn">{r}</td>'
                 f'<td class="num">{money(d["rec"] + d["lost"])}</td>'
                 f'<td class="num">{money(d["pkg"])}</td>'
                 f'<td class="num tl">{money(d["total_loss"])}</td>'
                 f'<td class="num">{num(d["inc"])}</td>'
                 f'<td class="num">{det}</td>'
                 f'<td class="num">{num(d["tres"])}</td></tr>')
det_net = '<span class="pend">pending*</span>' if DET_PENDING else num(nat["det"])
reg_rows += (f'<tr class="network"><td>NETWORK (all regions)</td>'
             f'<td class="num">{money(nat["rec"] + nat["lost"])}</td>'
             f'<td class="num">{money(nat["pkg"])}</td>'
             f'<td class="num">{money(nat["total_loss"])}</td>'
             f'<td class="num">{num(nat["inc"])}</td>'
             f'<td class="num">{det_net}</td>'
             f'<td class="num">{num(nat["tres"])}</td></tr>')


# ---- store detail, grouped by region ----
store_blocks = ""
for r in regions:
    rows = ""
    for s, a in sorted(stores_by_region[r], key=lambda x: -(x[1]["rec"] + x[1]["lost"] + x[1]["pkg"])):
        tl = a["rec"] + a["lost"] + a["pkg"]
        rows += (f'<tr><td>{s}</td>'
                 f'<td class="num">{money(a["rec"] + a["lost"])}</td>'
                 f'<td class="num">{money(a["pkg"])}</td>'
                 f'<td class="num tl">{money(tl)}</td>'
                 f'<td class="num">{num(a["inc"])}</td></tr>')
    d = reg_roll[r]
    store_blocks += (
        f'<tr class="rgnhdr"><td colspan="5">{r} &nbsp;·&nbsp; {len(stores_by_region[r])} stores '
        f'&nbsp;·&nbsp; {money(d["total_loss"])} total loss</td></tr>{rows}')


html = f"""<!doctype html><html><head><meta charset=utf-8><style>
@page {{ size:A4; margin:0; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:'Helvetica Neue',Arial,sans-serif; color:#1f2733; -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
.mast {{ background:#1E2A3A; color:#fff; padding:20px 30px; display:flex; align-items:center; justify-content:space-between; }}
.mast .l {{ display:flex; align-items:center; gap:16px; }}
.pill {{ background:#fff; border-radius:8px; padding:7px 11px; display:flex; }}
.pill img {{ height:30px; display:block; }}
.mast .title {{ font-size:19px; font-weight:800; letter-spacing:.2px; }}
.mast .subt {{ font-size:11px; color:#aeb9c6; margin-top:2px; }}
.mast .r {{ text-align:right; }}
.mast .r .fy {{ font-size:13px; font-weight:700; color:#C8952A; }}
.mast .r .we {{ font-size:11px; color:#aeb9c6; margin-top:2px; }}
.wrap {{ padding:20px 30px 14px; }}
.lead {{ font-size:11px; color:#5A6675; margin-bottom:16px; }}
.band {{ display:flex; gap:9px; margin-bottom:22px; }}
.tile {{ flex:1; border:1px solid #e6eaef; border-radius:8px; padding:11px 8px; text-align:center; }}
.tile .big {{ font-size:19px; font-weight:800; color:#1E2A3A; font-variant-numeric:tabular-nums; }}
.tile.loss {{ background:#f4faf6; border-color:#bfe3cd; }}
.tile.loss .big {{ color:#00843d; }}
.tile.pendtile {{ background:#fbf7ee; border-color:#e7d6ab; }}
.tile .lab {{ font-size:8.5px; color:#5A6675; text-transform:uppercase; letter-spacing:.6px; margin-top:4px; font-weight:700; }}
.pend {{ color:#C8952A; font-style:italic; font-weight:700; }}
h2 {{ color:#00843d; font-size:13.5px; margin:6px 0 9px; padding-bottom:5px; border-bottom:2px solid #1E2A3A; }}
table {{ width:100%; border-collapse:collapse; font-size:10.5px; margin-bottom:20px; }}
th {{ background:#1E2A3A; color:#fff; text-align:left; padding:7px 10px; font-size:9.5px; text-transform:uppercase; letter-spacing:.4px; }}
th.num, td.num {{ text-align:right; }}
td {{ padding:5.5px 10px; border-bottom:1px solid #eef1f5; }}
td.num {{ font-variant-numeric:tabular-nums; }}
td.rgn {{ font-weight:700; color:#1E2A3A; }}
td.tl {{ font-weight:700; color:#1E2A3A; }}
tr.network td {{ background:#C8952A; color:#1E2A3A; font-weight:800; border:none; }}
tr.rgnhdr td {{ background:#D9E1EA; color:#1E2A3A; font-weight:700; font-size:11px; padding:6px 10px; }}
.foot {{ font-size:9px; color:#8a95a3; border-top:1px solid #e6eaef; padding:9px 30px 16px; line-height:1.5; }}
.foot b {{ color:#5A6675; }}
</style></head><body>
<div class="mast">
  <div class="l">
    <div class="pill"><img src="data:image/png;base64,{logo_b64}"></div>
    <div><div class="title">Woolworths New Zealand</div><div class="subt">Weekly Loss-Prevention Report · National · all stores</div></div>
  </div>
  <div class="r"><div class="fy">{FY_LABEL}</div><div class="we">{WEEK_LABEL} · Prepared by SLS RTC</div></div>
</div>
<div class="wrap">
  <div class="lead">{"The first week of FY27. " if WNUM==1 else ""}Covert loss-prevention performance across the national network, grouped by region.
  <b>Total Loss = direct recovery + reported stolen value + recovered packaging.</b></div>
  <div class="band">{tile_html}</div>

  <h2>Performance by Region</h2>
  <table>
    <thead><tr><th>Region</th><th class="num">Recovered</th><th class="num">Packaging</th>
    <th class="num">Total Loss</th><th class="num">Incidents</th><th class="num">Deterrents</th><th class="num">Trespass</th></tr></thead>
    <tbody>{reg_rows}</tbody>
  </table>

  <h2>Store Detail</h2>
  <table>
    <thead><tr><th>Store</th><th class="num">Recovered</th><th class="num">Packaging</th>
    <th class="num">Total Loss</th><th class="num">Incidents</th></tr></thead>
    <tbody>{store_blocks}</tbody>
  </table>
</div>
<div class="foot">
  <b>SLS RTC — Confidential.</b> Prepared for Woolworths New Zealand. Figures from the Guard Incident Report and Recovered
  Packaging exports for {WSTART.day}–{WEEK_END.day} {WEEK_END.strftime('%B %Y')}, reconciled at store / region / national level.
  {"<b>*Deterrent data for 1–5 July is pending its export</b> and will be added on receipt — the figures above exclude it." if DET_PENDING else ""}
  Trespass Actions = {num(nat["vtres"])} verbal + {num(nat["ftres"])} formal notices served — a compounding barrier of banned offenders.
  Week-on-week comparison begins next week (this is the first week of FY27).
</div>
</body></html>"""

os.makedirs(OUTDIR, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.set_content(html, wait_until="networkidle")
    pg.pdf(path=OUT, prefer_css_page_size=True, print_background=True)
    b.close()
print("wrote", OUT)
print(f"National Total Loss (W{WNUM}, {WEEK_LABEL}): {money(nat['total_loss'])} | {len(store_region)} stores | {len(regions)} regions")
