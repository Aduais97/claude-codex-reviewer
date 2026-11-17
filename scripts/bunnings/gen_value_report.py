#!/usr/bin/env python3
"""Bunnings NZ CLIENT-FACING 'Monthly Security Performance & Value Report' (3-page PDF).
Mirrors the Woolworths value-PDF design (gen_value_report.py in scripts/ww): value-led,
client-safe: NO rates / cost / margin / per-hour, NO apprehension language, NO other client
names. Driven by the reconciled, client-safe August metrics (nro_metrics_AUG2026.json).
Bunnings-red accent; SLS RTC navy+gold masthead."""
import os, sys, re, json, base64
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.expanduser("~/Desktop/SLS-RTC/Operations/Analytics/assets/slsrtc_logo_hd.png")
METRICS = os.path.join(HERE, "nro_metrics_OCT2026.json")
OUTDIR = os.path.expanduser("~/Desktop/Bunnings")
OUT = f"{OUTDIR}/Bunnings_October_Value_Report.pdf"
FY_LABEL = "FY26/27 · October"
PERIOD = "1 – 31 October 2026"

d = json.load(open(METRICS))
INC   = d["incidents"]
SITES = d["sites"]
NREG  = d["regions"]
RECOV = d["recovered"]          # 23,126.39 recovered receipt value
STOLEN= d["stolen"]             # 1,200.06 unrecovered on valued incidents
IDENT = d["identified"]         # 24,326.45 total identified loss (valued incidents)
RPCT  = d["recovery_pct"]       # 95.1
SEV   = {int(k): v for k, v in d["severity"].items()}
SEV3P = d["sev3plus"]           # 4
SEV45 = d["sev45"]              # 0
RWIN  = d["risk_window_pct"]    # 65.3
PEAKD, PEAKN = d["peak_day"]    # Friday, 39
HRS   = d["hours_window"]       # 1360.0
INC100= d["inc_per_100h"]       # 8.9
HPI   = d["hours_per_inc"]      # 11.2
TOP6  = d["top6"]
REGL  = d["regional"]
RECON = "all 97 covert-team events reconciled; where the two systems differed, the higher value is reported"   # Oct: full union with Auror, greater-value adoption

# store -> region (for page-3 spotlights)
SREG = {"New Lynn": "Auckland", "Mt Roskill": "Auckland", "Mt Wellington": "Auckland", "Manukau": "Auckland",
        "Takanini": "Auckland", "Botany": "Auckland", "Westgate": "Auckland", "Grey Lynn": "Auckland",
        "Riccarton": "Canterbury", "Shirley": "Canterbury", "Christchurch Airport": "Canterbury",
        "Te Rapa": "Waikato", "Hamilton South": "Waikato", "South Hamilton": "Waikato", "Petone": "Wellington"}

def money(v): return f"${v:,.2f}"
def m0(v): return f"${v:,.0f}"
def short(name): return name.replace("Bunnings ", "")
def region_short(r): return r.split(" - ")[0].split(" – ")[0].strip()

logo = base64.b64encode(open(LOGO, "rb").read()).decode()

# ---- page 1 value tiles ----
tiles = [
    (f"{INC:,}", "Incidents managed", "on your floor in October"),
    (f"${RECOV/1000:,.1f}K", "Value recovered", "returned to Bunnings stock"),
    (f"{RPCT:.1f}%", "Recovery rate", "of identified loss returned to Bunnings"),
    (f"{SITES}", "Stores covered", f"across {NREG} regions"),
]
tile_html = "".join(
    f'<div class="vt{" hero" if i==0 else ""}"><div class="vb">{b}</div>'
    f'<div class="vl">{l}</div><div class="vs">{s}</div></div>'
    for i, (b, l, s) in enumerate(tiles))

# ---- severity spread line ----
sevline = " · ".join(f"Sev {k}: {SEV.get(k,0)}" for k in range(1, 6))

# ---- performance by region (recovered value + share) ----
regl = sorted(REGL, key=lambda r: -r["recovered"])
reg_rows = ""
for r in regl:
    share = (r["recovered"] / RECOV * 100) if RECOV else 0
    reg_rows += (f'<tr><td class="rg">{region_short(r["region"])}</td>'
                 f'<td class="n">{r["incidents"]}</td>'
                 f'<td class="n">{money(r["recovered"])}</td>'
                 f'<td class="n">{share:.1f}%</td></tr>')
reg_rows += (f'<tr class="net"><td>Network</td><td class="n">{INC}</td>'
             f'<td class="n">{money(RECOV)}</td><td class="n">100.0%</td></tr>')

# ---- top stores by value ----
top_val = sorted(TOP6, key=lambda s: -s["recovered"])[:5]
topv_rows = "".join(
    f'<tr><td>{i}</td><td class="s">{short(s["store"])}</td>'
    f'<td class="n">{money(s["recovered"])}</td><td class="n">{s["share"]:.1f}%</td></tr>'
    for i, s in enumerate(top_val, 1))

# ---- top stores by incidents ----
top_inc = sorted(TOP6, key=lambda s: (-s["incidents"], -s["recovered"]))[:5]
topi_rows = "".join(
    f'<tr><td>{i}</td><td class="s">{short(s["store"])}</td>'
    f'<td class="n">{s["incidents"]}</td><td class="n">{money(s["recovered"])}</td></tr>'
    for i, s in enumerate(top_inc, 1))

# ---- page-2 standout store cards ----
def _card_line(s):
    reg = SREG.get(short(s["store"]), "")
    bits = [f'{s["incidents"]} incidents managed']
    if s["recovered"] > 0:
        bits.append("recovered and returned to stock")
    if s.get("sev3"):
        bits.append(f'{s["sev3"]} graded serious · managed without escalation')
    return f'{reg} · ' + " · ".join(bits)
hl_html = "".join(
    f'<div class="hc"><div class="hh"><span class="hs">{short(s["store"])}</span>'
    f'<span class="hv">{money(s["recovered"])}</span></div>'
    f'<div class="hd">{_card_line(s)}</div></div>' for s in top_val[:4])

WKNUM = (f"<b>{INC}</b> incidents managed &nbsp;·&nbsp; <b>{RPCT:.1f}%</b> of identified loss recovered "
         f"&nbsp;·&nbsp; <b>{SITES}</b> stores &nbsp;·&nbsp; <b>{NREG}</b> regions covered")

# ⚠ MONTH-NAME LITERALS below ("October"): update together with PERIOD each month
# ---- page-3 store spotlights (aggregate, truthful: no fabricated incident scenes) ----
def _spot(s):
    reg = SREG.get(short(s["store"]), "")
    head = f'{short(s["store"])} ({reg}) · about {m0(s["recovered"])} recovered · {s["share"]:.1f}% of network value'
    covered = "Sustained covert observation across the trading week, concentrated on the aisles where loss recurs."
    found = (f'{s["incidents"]} incidents managed in October'
             + (': the network\'s highest concentration of recoverable loss.' if s is top_val[0]
                else '.'))
    ser = (f' {s["sev3"]} incident{"s" if s["sev3"]!=1 else ""} graded serious (severity 3+), managed through observation without escalation.'
           if s.get("sev3") else '')
    result = f'About {m0(s["recovered"])} of identified loss recovered and returned to stock.' + ser
    return (f'<div class="fi"><div class="fih">{head}</div>'
            f'<div class="fib"><b>What we covered.</b> {covered}</div>'
            f'<div class="fib"><b>What we found.</b> {found}</div>'
            f'<div class="fib"><b>Result.</b> {result}</div></div>')
spot_html = "".join(_spot(s) for s in top_val[:5])

html = f"""<!doctype html><html><head><meta charset=utf-8><style>
@page {{ size:A4; margin:0; }} *{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Helvetica Neue',Arial,sans-serif;color:#1f2733;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.mast{{background:#1E2A3A;color:#fff;padding:20px 30px;display:flex;align-items:center;justify-content:space-between}}
.mast .l{{display:flex;align-items:center;gap:15px}} .pill{{background:#fff;border-radius:8px;padding:7px 11px}} .pill img{{height:30px;display:block}}
.mast .title{{font-size:17px;font-weight:800}} .mast .subt{{font-size:10.5px;color:#aeb9c6;margin-top:2px}}
.mast .r{{text-align:right}} .mast .fy{{font-size:12.5px;font-weight:700;color:#C8952A}} .mast .we{{font-size:10px;color:#aeb9c6;margin-top:2px}}
.wrap{{padding:20px 30px}} .frame{{background:#fdf3f4;border:1px solid #f0c4c9;border-radius:8px;padding:12px 15px;margin-bottom:14px}}
.frame b{{color:#C8102E}} .frame p{{font-size:10.5px;color:#31404f;line-height:1.5}}
.scope{{font-size:10px;color:#5A6675;margin:2px 0 16px;font-weight:600;letter-spacing:.3px}}
h2{{color:#C8102E;font-size:14px;margin:4px 0 11px;padding-bottom:5px;border-bottom:2px solid #1E2A3A}}
.vband{{display:flex;gap:9px;margin-bottom:16px}} .vt{{flex:1;border:1px solid #e6eaef;border-radius:8px;padding:12px 8px;text-align:center;background:#fbfdfc}}
.vt .vb{{font-size:24px;font-weight:800;color:#1E2A3A}} .vt .vl{{font-size:9.5px;color:#1E2A3A;font-weight:700;margin-top:3px}} .vt .vs{{font-size:8px;color:#8a95a3;margin-top:3px;line-height:1.3}}
.vt.hero{{background:#1E2A3A;border-color:#1E2A3A}} .vt.hero .vb{{color:#C8952A;font-size:27px}} .vt.hero .vl{{color:#fff}} .vt.hero .vs{{color:#aeb9c6}}
.rec{{background:#1E2A3A;color:#fff;border-radius:8px;padding:14px 18px;margin-bottom:18px;display:flex;justify-content:space-between;align-items:center}}
.rec .lbl{{font-size:10px;color:#aeb9c6;text-transform:uppercase;letter-spacing:.5px}} .rec .big{{font-size:22px;font-weight:800;color:#fff}}
.rec .split{{font-size:10px;color:#c8d2dc;margin-top:3px}} .rec .cav{{font-size:9px;color:#8a95a3;font-style:italic;max-width:240px;text-align:right}}
table{{width:100%;border-collapse:collapse;font-size:10.5px;margin-bottom:16px}}
th{{background:#1E2A3A;color:#fff;text-align:left;padding:7px 10px;font-size:9.5px;text-transform:uppercase}} th.n,td.n{{text-align:right}}
td{{padding:6px 10px;border-bottom:1px solid #eef1f5}} td.rg,td.s{{font-weight:600;color:#1E2A3A}} tr.net td{{background:#C8952A;color:#1E2A3A;font-weight:800}}
.inv{{display:flex;gap:10px;margin-bottom:18px}} .iv{{flex:1;border:1px solid #e6eaef;border-radius:8px;padding:14px;text-align:center}}
.iv .b{{font-size:20px;font-weight:800;color:#1E2A3A}} .iv .l{{font-size:9px;color:#5A6675;text-transform:uppercase;letter-spacing:.4px;margin-top:4px;font-weight:700}}
.hl{{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-bottom:14px}}
.hc{{border:1px solid #e6eaef;border-left:3px solid #C8102E;border-radius:6px;padding:10px 13px;background:#fbfdfc}}
.hc .hh{{display:flex;justify-content:space-between;align-items:baseline}}
.hc .hs{{font-weight:800;color:#1E2A3A;font-size:11px}} .hc .hv{{font-weight:800;color:#1E7A46;font-size:12px}}
.hc .hd{{font-size:9px;color:#5A6675;margin-top:4px;line-height:1.4}}
.wknum{{background:#1E2A3A;color:#fff;border-radius:8px;padding:11px 15px;font-size:10px;margin-bottom:16px;text-align:center;line-height:1.5}} .wknum b{{color:#C8952A}}
.side{{background:#fbf7ee;border:1px solid #e7d6ab;border-radius:8px;padding:13px 16px;margin-bottom:16px}}
.side .t{{font-size:11px;font-weight:800;color:#8a6d1f;margin-bottom:5px}} .side p{{font-size:10px;color:#6b5a2f;line-height:1.5}}
.foot{{font-size:8.5px;color:#8a95a3;line-height:1.5;border-top:1px solid #e6eaef;padding-top:9px;margin-top:6px}}
.fisub{{font-size:8.8px;color:#5A6675;margin:2px 0 2px}}
.fi{{margin-top:9px;break-inside:avoid}} .fih{{font-size:10px;font-weight:700;color:#C8102E}}
.fib{{font-size:9px;color:#3a3a4a;margin-top:2px;line-height:1.45}}
.hsband{{display:flex;gap:7px;margin-top:8px}}
.hst{{flex:1;background:#EEF1F5;border:1px solid #dfe4ea;border-radius:4px;padding:9px 5px;text-align:center}}
.hst .hn{{font-size:19px;font-weight:800;color:#1E2A3A}} .hst .hn.gold{{color:#C8952A}} .hst .hn.small{{font-size:14px}}
.hst .hcap{{font-size:7.6px;color:#5A6675;font-weight:700;margin-top:3px;line-height:1.25}}
.hsp{{font-size:9px;color:#3a3a4a;line-height:1.5;margin-top:7px}}
.pagebreak{{page-break-before:always}}
</style></head><body>

<div class="mast"><div class="l"><div class="pill"><img src="data:image/png;base64,{logo}"></div>
<div><div class="title">Bunnings New Zealand | Monthly Security Performance &amp; Value Report</div>
<div class="subt">SLS RTC covert loss-prevention · national</div></div></div>
<div class="r"><div class="fy">{FY_LABEL}</div><div class="we">{PERIOD}</div></div></div>

<div class="wrap">
  <div class="frame"><p><b>How to read this report.</b> Recovered value is one visible component of the return. The larger value of covert loss-prevention (deterrence, repeat-offender intelligence and staff safety) is protective and is not monetised here. All figures are reconciled against Bunnings' Auror database.</p></div>
  <div class="scope">{SITES} STORES COVERED IN OCTOBER · {NREG} REGIONS</div>

  <h2>Value Delivered This Month</h2>
  <div class="vband">{tile_html}</div>
  <div class="rec"><div><div class="lbl">Value recovered &amp; returned in October</div>
    <div class="big">{money(RECOV)}</div>
    <div class="split"><b>{RPCT:.1f}% of the {money(IDENT)} identified</b> &nbsp;·&nbsp; {money(STOLEN)} ({100-RPCT:.1f}%) not recovered</div></div>
    <div class="cav">Recovery rate on identified loss. Reconciled against Bunnings' Auror system: {RECON}.</div></div>

  <h2>Health &amp; Safety This Month</h2>
  <div class="hsband">
    <div class="hst"><div class="hn">{INC}</div><div class="hcap">Incidents managed</div></div>
    <div class="hst"><div class="hn gold">{SEV3P}</div><div class="hcap">Serious (severity 3+)</div></div>
    <div class="hst"><div class="hn">{SEV45}</div><div class="hcap">Severe (severity 4–5)</div></div>
    <div class="hst"><div class="hn small">{PEAKD}</div><div class="hcap">Peak activity day ({PEAKN} incidents)</div></div>
    <div class="hst"><div class="hn">{RWIN:.0f}%</div><div class="hcap">Loss in peak risk window</div></div>
    <div class="hst"><div class="hn">{HRS:,.0f}</div><div class="hcap">Guard-hours deployed</div></div>
  </div>
  <p class="hsp">The team managed <b>{INC} incidents</b> across {SITES} stores in October. <b>{SEV3P}</b> reached severity 3 or above (<b>{SEV45}</b> at the severe end, severity 4&ndash;5), each managed through covert observation without physical intervention. Severity spread: {sevline}. Activity concentrated on <b>{PEAKD}s</b> ({PEAKN} incidents) and within the peak risk window (<b>{RWIN:.0f}%</b> of identified loss). Our team is covert and observation-only; the priority throughout is the safety of staff and customers.</p>
  <p style="font-size:8.6pt;color:#555;margin:6px 0 0;line-height:1.45"><b>Severity grading (1&ndash;5).</b> Each incident is graded by the difficulty, cooperation and, above all, the risk to staff and customers during the intervention. <b>Level 3 and above is graded &lsquo;serious&rsquo;.</b> &nbsp;<b>1</b> Compliant: no issues, items recovered / returned. &nbsp;<b>2</b> Low-level difficulty: unhelpful or evasive, or items lost. &nbsp;<b>3</b> Mild aggression: managed without escalation. &nbsp;<b>4</b> Verbal &amp; aggressive abuse: threatening language, no physical contact. &nbsp;<b>5</b> Physical altercation or weapon: escalated to Police where warranted.</p>

  <h2>Performance by Region</h2>
  <table><thead><tr><th>Region</th><th class="n">Incidents</th><th class="n">Value Recovered</th><th class="n">Share of Value</th></tr></thead>
  <tbody>{reg_rows}</tbody></table>

  <h2>Top Stores by Value Recovered</h2>
  <table><thead><tr><th>#</th><th>Store</th><th class="n">Value Recovered</th><th class="n">Share of Network</th></tr></thead><tbody>{topv_rows}</tbody></table>
</div>

<div class="pagebreak"></div>
<div class="mast"><div class="l"><div class="pill"><img src="data:image/png;base64,{logo}"></div>
<div><div class="title">Your Month in Action</div><div class="subt">What the covert team delivered on your floor in October</div></div></div>
<div class="r"><div class="fy">{FY_LABEL}</div><div class="we">{PERIOD}</div></div></div>
<div class="wrap">
  <h2>This Month's Standout Stores</h2>
  <div class="hl">{hl_html}</div>
  <div class="wknum">{WKNUM}</div>

  <h2>Deployment · {FY_LABEL}</h2>
  <div class="inv">
    <div class="iv"><div class="b">{HRS:,.0f}</div><div class="l">Guard-hours deployed</div></div>
    <div class="iv"><div class="b">{SITES}</div><div class="l">Stores deployed</div></div>
    <div class="iv"><div class="b">{NREG}</div><div class="l">Regions covered</div></div>
  </div>

  <div class="side"><div class="t">Coverage intensity: where the cover went</div>
  <p>Across roughly {HRS:,.0f} guard-hours the team managed {INC} incidents: about <b>{INC100:.1f} incidents per 100 guard-hours</b> (around one every {HPI:.0f} hours of cover). Coverage is concentrated on the highest-loss stores and the {PEAKD} peak, so effort tracks where the risk actually sits.</p></div>

  <h2>What Your Security Delivers</h2>
  <table><thead><tr><th>Protective outcome</th><th class="n">This month</th></tr></thead><tbody>
  <tr><td class="s">Value recovered &amp; returned to stock</td><td class="n">{money(RECOV)} · {RPCT:.1f}% of identified loss</td></tr>
  <tr><td class="s">Stores under covert coverage</td><td class="n">{SITES} across {NREG} regions</td></tr>
  <tr><td class="s">Incidents managed on your floor</td><td class="n">{INC}</td></tr>
  <tr><td class="s">Serious incidents managed (severity 3+)</td><td class="n">{SEV3P} · {SEV45} severe</td></tr>
  <tr><td class="s">Reconciled to Auror</td><td class="n">{RECON}</td></tr>
  </tbody></table>

  <h2>Top Stores by Total Incidents</h2>
  <table><thead><tr><th>#</th><th>Store</th><th class="n">Incidents</th><th class="n">Value Recovered</th></tr></thead><tbody>{topi_rows}</tbody></table>

  <div class="pagebreak"></div>
  <h2>Where the Value Came From</h2>
  <div class="fisub">The stores that drove October's recovered value, and what our covert team delivered at each. Figures are aggregate; individuals are not identified and the team operates by observation, without physical force.</div>
  {spot_html}

  <div class="foot">
  <b>SLS RTC | Confidential.</b> Prepared for Bunnings New Zealand. All figures reconciled against Bunnings' Auror database ({RECON}). Value = recovered receipt value plus estimated unrecovered on valued incidents; deterrence and repeat-offender intelligence are protective and not monetised here.
  </div>
</div>
</body></html>"""

# lint: none of these tokens may reach the client doc: check VISIBLE TEXT only
# (strip the <style> block + all tags + base64 logo so CSS keywords like 'margin' don't false-trip)
_vis = re.sub(r'<style[^>]*>.*?</style>', ' ', html, flags=re.S)
_vis = re.sub(r'<[^>]+>', ' ', _vis)
_vis = re.sub(r'data:image/[^"\']+', '', _vis).lower()
BANNED = ["apprehen", "arrest", "detain", "restrain", "handcuff", "tackle", "grabbed",
          "wrestled", "chased", "searched", "physically stop", "per hour", "/hr", "bill rate",
          "net $", "margin", "rate card", "cost-plus", "woolworth", "countdown", "mitre",
          "the warehouse"]
for bad in BANNED:
    assert bad not in _vis, f"LINT FAIL: '{bad}' in visible text"

os.makedirs(OUTDIR, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.set_content(html, wait_until="networkidle")
    pg.pdf(path=OUT, prefer_css_page_size=True, print_background=True); b.close()
print("wrote", OUT)
print(f"scope {SITES} stores / {NREG} regions / {HRS:,.0f}h / {INC} incidents / recovered {money(RECOV)} ({RPCT:.1f}%)")
print("lint: no rates/cost/margin, no apprehension language, no other-client names: PASS")
