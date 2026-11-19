#!/usr/bin/env python3
"""Woolworths FY27 CLIENT-FACING 'Weekly Security Performance & Value Report' (2-page PDF).
Per the ETR display review: value-led, NO net / NO recovery:cost ratio / NO per-store cost;
cost (page 2) and recovery (page 1) on separate pages; legally-safe language; deterred-loss = placeholder.
Internal 'Spend & Recovery Tracker.xlsx' (with Net/ROI) is NOT this — this is the safe client view."""
import os, sys, re, base64
from datetime import datetime
from collections import defaultdict
import openpyxl
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_master_v2 as bm
from ww_incidents import INCIDENTS
from ww_hs import hs_metrics

LOGO = os.path.expanduser("~/Desktop/SLS-RTC/Operations/Analytics/assets/slsrtc_logo_hd.png")
WK = bm.CURRENT_WEEK
WNUM = bm.week_num(WK); WLABEL = bm.week_label(WK); WSTART = bm.week_start(WK); PARTIAL = bm.is_partial(WK)
WNOTE = bm.week_note(WK)
SUBT = ' · partial first FY week' if PARTIAL else (f' · {WNOTE}' if WNOTE else '')
OUTDIR = os.path.expanduser(f"~/Desktop/Woolworths /Week Ending {WLABEL}")
OUT = f"{OUTDIR}/Woolworths Weekly Security Performance & Value Report - Week Ending {WLABEL}.pdf"

def mn(s):
    s=str(s).lower().replace("woolworths","").replace("countdown","")
    s=s.replace("mount","mt").replace("point","pt").replace("pt chevalier","pt chev")
    return re.sub(r"\s+"," ",re.sub(r"[^a-z0-9 ]"," ",s)).strip()
def pdd(s):
    for fm in ("%m/%d/%Y","%d/%m/%Y","%Y-%m-%d"):
        try: return datetime.strptime(str(s).split(" ")[0],fm)
        except: pass
    return None
def hh(a,b):
    try:
        ah,am=map(int,str(a).split(":")); bh,bm2=map(int,str(b).split(":")); d=(bh*60+bm2)-(ah*60+am); return d/60 if d>0 else 0
    except: return 0

# hours per store for the reporting week
f=bm.schedule_for(WK)
wb=openpyxl.load_workbook(f,read_only=True); ws=wb.active; it=ws.iter_rows(values_only=True); hd=list(next(it))
di,si,ei,ji=hd.index("Date"),hd.index("Start"),hd.index("End"),hd.index("Job")
H=defaultdict(float)
for r in it:
    d=pdd(r[di]); job=r[ji]
    if not d or not(WSTART<=d<=WK) or not job or "woolworth" not in str(job).lower() or "travel" in str(job).lower(): continue
    H[mn(job)]+=hh(r[si],r[ei])
wb.close()

agg,sreg,regs=bm.aggregate(); wk=WK
active=[(s,a) for (w,s),a in agg.items() if w==wk]
nat=bm.rollup([a for s,a in active])
deployed=sum(1 for h in H.values() if h>0)   # all stores with guard-hours this week (deployed)
TOTAL_H=round(sum(H.values()))
# Region hours cover ALL deployed stores so the column foots to the network total (state the
# larger sum). Stores deployed with no incidents this week are absent from the incident-derived
# sreg, so also map via STORE_REGION_OVERRIDE / normalised keys.
nreg={mn(s):r for s,r in sreg.items()}
nreg.update({mn(k):v for k,v in bm.STORE_REGION_OVERRIDE.items()})
reg_h=defaultdict(float)
for k,h in H.items(): reg_h[nreg.get(k)]+=h
_unmapped=sum(h for k,h in H.items() if nreg.get(k) not in regs)
if _unmapped: print(f"WARN: {_unmapped:.2f}h of deployment did not map to a region", file=sys.stderr)
reg_roll={r:bm.rollup([a for s,a in active if sreg.get(s)==r]) for r in regs}
top=sorted(active,key=lambda x:-(x[1]['rec']+x[1]['lost']))[:5]   # incident loss (excl recovered packaging)
top_inc=sorted(active,key=lambda x:(-x[1]['inc'], -(x[1]['rec']+x[1]['lost']+x[1]['pkg'])))[:5]
SCOPE=len(active); NREG=len(regs)   # derived from the master so counts can't drift/hardcode-stale
# Report on ONE headline number (Total Loss, WW's metric) with recovery as a rate — avoids the
# "$11k vs $10.5k" confusion of showing two competing dollar totals across documents.
def rpct(a):
    tl=a['rec']+a['lost']+a['pkg']; return (a['rec']+a['pkg'])/tl*100 if tl else 0
REC_PCT=rpct(nat)
def rpct_inc(a):
    il=a['rec']+a['lost']; return a['rec']/il*100 if il else 0
HS=hs_metrics(bm, WK)
# Severity-aware H&S clause: the blanket "without physical intervention" claim is only true
# when the week has no severity-5 (physical altercation) incident — W17 proved it can lie
# right next to the "Sev 5: 1" spread. Keep the sentence honest either way.
_S5 = HS['sev'].get('5', 0)
if _S5 == 0:
    PHYS_CLAUSE = "each managed without physical intervention"
elif _S5 == 1:
    PHYS_CLAUSE = ("managed with de-escalation first; one incident reached severity 5, where an "
                   "offender became physically aggressive toward the team &mdash; the team "
                   "de-escalated and the matter was escalated to Police")
else:
    PHYS_CLAUSE = (f"managed with de-escalation first; {_S5} incidents reached severity 5, where "
                   "offenders became physically aggressive toward the team &mdash; each was "
                   "escalated to Police")

def money(v): return f"${v:,.2f}"
def m0(v): return f"${v:,.0f}"
logo=base64.b64encode(open(LOGO,'rb').read()).decode()

# ---- value scorecard tiles (incidents-led, mirroring the FY26 Impact Report: the incident
# count is the anchor, offenders "engaged across N incidents") ----
tres_sub=f"{nat['vtres']} verbal + {nat['ftres']} formal notice" + ("s" if nat['ftres']!=1 else "")
tiles=[(f"{nat['inc']:,}","Incidents managed","on your floor this week"),
       (f"{nat['off']:,}","Offenders engaged",f"across {nat['inc']:,} incidents · handed to Police where warranted"),
       (f"{nat['tres']:,}","Trespass actions",tres_sub),
       (f"{nat['det']:,}","Deterrents",f"{nat['det_ind']} individuals turned away")]
tile_html="".join(f'<div class="vt{" hero" if i==0 else ""}"><div class="vb">{b}</div><div class="vl">{l}</div><div class="vs">{s}</div></div>' for i,(b,l,s) in enumerate(tiles))

reg_rows=""
order=sorted(regs,key=lambda r:-reg_roll[r]['total_loss'])
for r in order:
    d=reg_roll[r]
    reg_rows+=(f'<tr><td class="rg">{r}</td><td class="n">{reg_h[r]:.0f}</td><td class="n">{d["inc"]}</td>'
               f'<td class="n">{d["det"]}</td><td class="n">{d["tres"]}</td>'
               f'<td class="n">{money(d["total_loss"])}</td><td class="n">{rpct(d):.1f}%</td></tr>')
reg_rows+=(f'<tr class="net"><td>Network</td><td class="n">{TOTAL_H:.0f}</td><td class="n">{nat["inc"]}</td>'
           f'<td class="n">{nat["det"]}</td><td class="n">{nat["tres"]}</td>'
           f'<td class="n">{money(nat["total_loss"])}</td><td class="n">{REC_PCT:.1f}%</td></tr>')
top_rows="".join(f'<tr><td>{i}</td><td class="s">{s}</td><td class="n">{money(a["rec"]+a["lost"])}</td><td class="n">{rpct_inc(a):.1f}%</td></tr>'
                 for i,(s,a) in enumerate(top,1))
topinc_rows="".join(f'<tr><td>{i}</td><td class="s">{s}</td><td class="n">{a["inc"]}</td><td class="n">{money(a["rec"]+a["lost"]+a["pkg"])}</td></tr>'
                 for i,(s,a) in enumerate(top_inc,1))
focus_html="".join(f'<div class="fi"><div class="fih">{it["h"]}</div>'
                   f'<div class="fib"><b>What happened.</b> {it["occ"]}</div>'
                   f'<div class="fib"><b>How the team handled it.</b> {it["hand"]}</div>'
                   f'<div class="fib"><b>Outcome.</b> {it["out"]}</div></div>' for it in INCIDENTS)

# ---- This week's standout interceptions ("what we did"), from the incident detail ----
INC=bm.week_incidents(WK)
N_FULL=sum(1 for x in INC if 'full' in x['type'].lower())
N_GROUP=sum(1 for x in INC if x['off']>1)
def _prod(p):
    parts=[x.strip().rstrip(',').strip() for x in str(p or '').split(',')]
    parts=[x for x in parts if x and x.lower()!='other'][:2]
    return ' & '.join(parts) if parts else 'stock'
def _hl(x):
    act='recovered in full' if 'full' in x['type'].lower() else ('partial recovery' if 'partial' in x['type'].lower() else 'intercepted')
    tags=[]
    if x['police']: tags.append('Police notified')
    if x['ft']: tags.append('formal trespass served')
    elif x['vt']: tags.append('trespass issued')
    if x['off']>1: tags.append(f"{x['off']}-offender group")
    return f"{_prod(x['product'])} concealment intercepted — {act}" + (f" · {' · '.join(tags)}" if tags else "")
_full=[x for x in INC if 'full' in x['type'].lower() and x['rec']>0]
_part=[x for x in INC if 'full' not in x['type'].lower() and x['rec']>0]
HL=(_full+_part)[:4]
hl_html="".join(f'<div class="hc"><div class="hh"><span class="hs">{x["store"].replace("Mount ","Mt ")}</span><span class="hv">{money(x["rec"])}</span></div>'
                f'<div class="hd">{_hl(x)}</div></div>' for x in HL)
WKNUM=(f"<b>{nat['inc']}</b> incidents managed &nbsp;·&nbsp; <b>{N_FULL} recovered in full</b> &nbsp;·&nbsp; "
       f"<b>{N_GROUP}</b> group / multi-offender incidents &nbsp;·&nbsp; <b>{REC_PCT:.1f}%</b> of identified loss recovered &amp; returned")

html=f"""<!doctype html><html><head><meta charset=utf-8><style>
@page {{ size:A4; margin:0; }} *{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Helvetica Neue',Arial,sans-serif;color:#1f2733;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.mast{{background:#1E2A3A;color:#fff;padding:20px 30px;display:flex;align-items:center;justify-content:space-between}}
.mast .l{{display:flex;align-items:center;gap:15px}} .pill{{background:#fff;border-radius:8px;padding:7px 11px}} .pill img{{height:30px;display:block}}
.mast .title{{font-size:17px;font-weight:800}} .mast .subt{{font-size:10.5px;color:#aeb9c6;margin-top:2px}}
.mast .r{{text-align:right}} .mast .fy{{font-size:12.5px;font-weight:700;color:#C8952A}} .mast .we{{font-size:10px;color:#aeb9c6;margin-top:2px}}
.wrap{{padding:20px 30px}} .frame{{background:#f4faf6;border:1px solid #bfe3cd;border-radius:8px;padding:12px 15px;margin-bottom:14px}}
.howto{{font-size:10px;color:#444;line-height:1.55;margin:2px 0 15px}} .howto b{{color:#00843d}}
.frame b{{color:#00843d}} .frame p{{font-size:10.5px;color:#31404f;line-height:1.5}}
.scope{{font-size:10px;color:#5A6675;margin:2px 0 16px;font-weight:600;letter-spacing:.3px}}
h2{{color:#00843d;font-size:14px;margin:4px 0 11px;padding-bottom:5px;border-bottom:2px solid #1E2A3A}}
.vband{{display:flex;gap:9px;margin-bottom:16px}} .vt{{flex:1;border:1px solid #e6eaef;border-radius:8px;padding:12px 8px;text-align:center;background:#fbfdfc}}
.vt .vb{{font-size:24px;font-weight:800;color:#1E2A3A}} .vt .vl{{font-size:9.5px;color:#1E2A3A;font-weight:700;margin-top:3px}} .vt .vs{{font-size:8px;color:#8a95a3;margin-top:3px;line-height:1.3}}
.vt.hero{{background:#1E2A3A;border-color:#1E2A3A}} .vt.hero .vb{{color:#C8952A;font-size:27px}} .vt.hero .vl{{color:#fff}} .vt.hero .vs{{color:#aeb9c6}}
.rec{{background:#1E2A3A;color:#fff;border-radius:8px;padding:14px 18px;margin-bottom:18px;display:flex;justify-content:space-between;align-items:center}}
.rec .lbl{{font-size:10px;color:#aeb9c6;text-transform:uppercase;letter-spacing:.5px}} .rec .big{{font-size:22px;font-weight:800;color:#fff}}
.rec .split{{font-size:10px;color:#c8d2dc;margin-top:3px}} .rec .cav{{font-size:9px;color:#8a95a3;font-style:italic;max-width:230px;text-align:right}}
table{{width:100%;border-collapse:collapse;font-size:10.5px;margin-bottom:16px}}
th{{background:#1E2A3A;color:#fff;text-align:left;padding:7px 10px;font-size:9.5px;text-transform:uppercase}} th.n,td.n{{text-align:right}}
td{{padding:6px 10px;border-bottom:1px solid #eef1f5}} td.rg,td.s{{font-weight:600;color:#1E2A3A}} tr.net td{{background:#C8952A;color:#1E2A3A;font-weight:800}}
.inv{{display:flex;gap:10px;margin-bottom:18px}} .iv{{flex:1;border:1px solid #e6eaef;border-radius:8px;padding:14px;text-align:center}}
.iv .b{{font-size:20px;font-weight:800;color:#1E2A3A}} .iv .l{{font-size:9px;color:#5A6675;text-transform:uppercase;letter-spacing:.4px;margin-top:4px;font-weight:700}}
.hl{{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-bottom:14px}}
.hc{{border:1px solid #e6eaef;border-left:3px solid #00843d;border-radius:6px;padding:10px 13px;background:#fbfdfc}}
.hc .hh{{display:flex;justify-content:space-between;align-items:baseline}}
.hc .hs{{font-weight:800;color:#1E2A3A;font-size:11px}} .hc .hv{{font-weight:800;color:#00843d;font-size:12px}}
.hc .hd{{font-size:9px;color:#5A6675;margin-top:4px;line-height:1.4}}
.wknum{{background:#1E2A3A;color:#fff;border-radius:8px;padding:11px 15px;font-size:10px;margin-bottom:16px;text-align:center;line-height:1.5}} .wknum b{{color:#C8952A}}
.side{{background:#fbf7ee;border:1px solid #e7d6ab;border-radius:8px;padding:13px 16px;margin-bottom:16px}}
.side .t{{font-size:11px;font-weight:800;color:#8a6d1f;margin-bottom:5px}} .side p{{font-size:10px;color:#6b5a2f;line-height:1.5}}
.foot{{font-size:8.5px;color:#8a95a3;line-height:1.5;border-top:1px solid #e6eaef;padding-top:9px;margin-top:6px}}
.fisub{{font-size:8.8px;color:#5A6675;margin:2px 0 2px}}
.fi{{margin-top:9px;break-inside:avoid}} .fih{{font-size:10px;font-weight:700;color:#C8952A}}
.fib{{font-size:9px;color:#3a3a4a;margin-top:2px;line-height:1.45}}
.hsband{{display:flex;gap:7px;margin-top:8px}}
.hst{{flex:1;background:#EEF1F5;border:1px solid #dfe4ea;border-radius:4px;padding:9px 5px;text-align:center}}
.hst .hn{{font-size:19px;font-weight:800;color:#1E2A3A}} .hst .hn.gold{{color:#C8952A}} .hst .hn.red{{color:#C0392B}}
.hst .hcap{{font-size:7.6px;color:#5A6675;font-weight:700;margin-top:3px;line-height:1.25}}
.hsp{{font-size:9px;color:#3a3a4a;line-height:1.5;margin-top:7px}}
.pagebreak{{page-break-before:always}}
</style></head><body>

<div class="mast"><div class="l"><div class="pill"><img src="data:image/png;base64,{logo}"></div>
<div><div class="title">Woolworths New Zealand — Weekly Security Performance &amp; Value Report</div>
<div class="subt">SLS RTC covert loss-prevention · national</div></div></div>
<div class="r"><div class="fy">FY27 · Week {WNUM}</div><div class="we">Week Ending {WLABEL}{SUBT}</div></div></div>

<div class="wrap">
  <p class="howto"><b>How to read this report.</b> Recovered value is one visible component of the return. The larger value of covert loss-prevention — deterrence, the trespass wall, offender intelligence and staff safety — is protective and is not monetised here.</p>
  <div class="scope">{deployed} STORES DEPLOYED THIS WEEK · {NREG} REGIONS</div>

  <h2>Value Delivered This Week</h2>
  <div class="vband">{tile_html}</div>
  <div class="rec"><div><div class="lbl">Total loss identified this week</div>
    <div class="big">{money(nat['total_loss'])}</div>
    <div class="split"><b>{REC_PCT:.1f}% recovered &amp; returned to Woolworths</b> &nbsp;·&nbsp; {money(nat['lost'])} ({100-REC_PCT:.1f}%) not recovered</div></div>
    <div class="cav">Recovery rate on identified loss — alongside {nat['off']:,} offenders engaged across {nat['inc']:,} incidents, {nat['tres']:,} trespass actions and {nat['det']:,} deterrents.</div></div>

  <h2>Health &amp; Safety This Week</h2>
  <div class="hsband">
    <div class="hst"><div class="hn">{nat['inc']}</div><div class="hcap">Incidents managed</div></div>
    <div class="hst"><div class="hn">{nat['off']}</div><div class="hcap">Offenders engaged</div></div>
    <div class="hst"><div class="hn gold">{HS['SERIOUS']}</div><div class="hcap">Serious (severity 3+)</div></div>
    <div class="hst"><div class="hn red">{HS['confront']}</div><div class="hcap">Involving aggression / threats</div></div>
    <div class="hst"><div class="hn">{nat['tres']:,}</div><div class="hcap">Trespass actions</div></div>
    <div class="hst"><div class="hn">{HS['pol']}</div><div class="hcap">Escalated to Police</div></div>
  </div>
  <p class="hsp">The team managed <b>{nat['inc']} incidents</b> involving <b>{nat['off']} offenders</b> this week. <b>{HS['SERIOUS']}</b> reached severity 3 or above (<b>{HS['SEVERE']}</b> at the severe end, severity 4&ndash;5), and <b>{HS['confront']}</b> involved aggression, threats or violence toward the team or others &mdash; {PHYS_CLAUSE}. Severity spread: {HS['sevline']}. <b>{nat['tres']:,} trespass actions</b> were issued and <b>{HS['pol']}</b> incidents escalated to Police. Our team is covert and observation-only; the priority throughout is the safety of staff and customers.</p>
  <p style="font-size:8.6pt;color:#555;margin:6px 0 0;line-height:1.45"><b>Severity grading (1&ndash;5).</b> Each incident is graded by the difficulty, cooperation and, above all, the risk to staff and customers during the intervention &mdash; <b>Level 3 and above is graded &lsquo;serious&rsquo;.</b> &nbsp;<b>1</b> Compliant &mdash; no issues, items recovered / returned. &nbsp;<b>2</b> Low-level difficulty &mdash; unhelpful or evasive, or items lost. &nbsp;<b>3</b> Mild aggression &mdash; managed without escalation. &nbsp;<b>4</b> Verbal &amp; aggressive abuse &mdash; threatening language, no physical contact. &nbsp;<b>5</b> Physical altercation or weapon &mdash; escalated to Police where warranted.</p>

  <h2>Performance by Region</h2>
  <table><thead><tr><th>Region</th><th class="n">Hours</th><th class="n">Incidents</th><th class="n">Deterrents</th><th class="n">Trespass</th><th class="n">Total Loss</th><th class="n">Recovered %</th></tr></thead>
  <tbody>{reg_rows}</tbody></table>

  <h2>Top Stores by Total Loss (Incidents)</h2>
  <table><thead><tr><th>#</th><th>Store</th><th class="n">Incident Loss</th><th class="n">Recovered %</th></tr></thead><tbody>{top_rows}</tbody></table>
</div>

<div class="pagebreak"></div>
<div class="mast"><div class="l"><div class="pill"><img src="data:image/png;base64,{logo}"></div>
<div><div class="title">Your Week in Action</div><div class="subt">What the covert team did on your floor this week</div></div></div>
<div class="r"><div class="fy">FY27 · Week {WNUM}</div><div class="we">Week Ending {WLABEL}</div></div></div>
<div class="wrap">
  <h2>This Week's Standout Interceptions</h2>
  <div class="hl">{hl_html}</div>
  <div class="wknum">{WKNUM}</div>

  <h2>Deployment — FY27 Week {WNUM}</h2>
  <div class="inv">
    <div class="iv"><div class="b">{TOTAL_H:,}</div><div class="l">Guard-hours deployed</div></div>
    <div class="iv"><div class="b">{deployed}</div><div class="l">Stores deployed</div></div>
    <div class="iv"><div class="b">{NREG}</div><div class="l">Regions covered</div></div>
  </div>

  <div class="side"><div class="t">Deterrence — theft turned away at the door</div>
  <p>{nat['det']} deterrent events this week turned <b>{nat['det_ind']} individuals</b> away before entry — theft stopped before it happened. Reported in activity terms; the prevented loss is real but not monetised here (a dollar value will be added once a Woolworths-sourced shrink basis is agreed).</p></div>

  <h2>What your security delivers</h2>
  <table><thead><tr><th>Protective outcome</th><th class="n">This week</th></tr></thead><tbody>
  <tr><td class="s">Deterrence — theft stopped before it happened</td><td class="n">{nat['det']} events · {nat['det_ind']} turned away</td></tr>
  <tr><td class="s">Trespass wall — banned-offender barrier</td><td class="n">{nat['tres']} actions ({nat['vtres']} verbal + {nat['ftres']} formal)</td></tr>
  <tr><td class="s">Offender intelligence — repeat/ORC identification</td><td class="n">{nat['off']} offenders engaged</td></tr>
  <tr><td class="s">Incidents managed on your floor</td><td class="n">{nat['inc']}</td></tr>
  <tr><td class="s">Total loss identified · recovered &amp; returned</td><td class="n">{money(nat['total_loss'])} · {REC_PCT:.1f}% recovered</td></tr>
  </tbody></table>

  <h2>Top Stores by Total Incidents</h2>
  <table><thead><tr><th>#</th><th>Store</th><th class="n">Incidents</th><th class="n">Total Loss</th></tr></thead><tbody>{topinc_rows}</tbody></table>

  <div class="pagebreak"></div>
  <h2>Incidents in Focus</h2>
  <div class="fisub">A sample of what the team dealt with this week and the results. Individuals are not identified; the team intervenes without physical force.</div>
  {focus_html}

  <div class="foot">
  <b>SLS RTC — Confidential.</b> Prepared for Woolworths New Zealand.
  </div>
</div>
</body></html>"""

# lint: none of these tokens may reach the client doc (check visible text only, not the base64 logo blob)
_lint = re.sub(r'data:image/[^"\']+', '', html).lower()
for bad in ["apprehension","arrest","net $","recov:cost","% offset","/hr","bill rate","$c$3","per hour"]:
    assert bad not in _lint, f"LINT FAIL: '{bad}' in output"
# stricter gate on the Incidents in Focus narratives only (spares the negated 'physically detain' disclaimer)
_inc_text=" ".join(f"{it['occ']} {it['hand']} {it['out']}" for it in INCIDENTS).lower()
for bad in ["apprehend","arrest","detain","restrain","handcuff","tackle","grabbed","wrestled","chased"," took the ","physically stop","searched"]:
    assert bad not in _inc_text, f"INCIDENT LINT FAIL: '{bad}' in Incidents in Focus"

os.makedirs(OUTDIR, exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.set_content(html, wait_until="networkidle")
    pg.pdf(path=OUT, prefer_css_page_size=True, print_background=True); b.close()
print("wrote", OUT)
print(f"scope {SCOPE} / deployed {deployed} / hours {TOTAL_H} / recovery {money(nat['rec']+nat['pkg'])}")
print("lint: no net, no ratio, no per-store cost, no apprehension/arrest — PASS")
