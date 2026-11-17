#!/usr/bin/env python3
"""Woolworths NZ — National LP Performance (recovery INCL packaging; per-region top stores)."""
import asyncio, base64, sqlite3
from collections import defaultdict
from pathlib import Path
DB=Path.home()/"Desktop/Dev/asg-ops-hub/data/truth.db"
LOGO=Path.home()/"Desktop/SLS-RTC/Operations/Analytics/assets/slsrtc_logo_hd.png"
OUT=Path.home()/"Desktop/SLS-RTC/Operations/Woolworths/Woolworths_NZ_National_LP_Performance.pdf"
GREEN="#1d7a4d"; RED="#b23a3a"; ACC="#1f3a5f"; SUB="#5b6472"; HEAD="#eef1f5"; LINE="#dfe3e8"
c=sqlite3.connect(DB)
# per-store from saved truth table (recovery incl packaging)
rows=[dict(store=s,region=r,events=e,direct=d,pkg=p,total=t,stolen=st,rate=rr)
      for s,r,e,d,p,t,st,rr in c.execute("SELECT store,region,events,direct_recovery,packaging,total_recovery,stolen,recovery_rate FROM ww_store_performance_fy")]
det=c.execute("SELECT COUNT(*) FROM ww_deterrents WHERE event_date BETWEEN '2025-07-01' AND '2026-06-30'").fetchone()[0]
# region recovery rate from incidents
regrate={}
for region,ev,rc in c.execute("SELECT region,COUNT(*),SUM(CASE WHEN recovery_type IN ('full','partial') THEN 1 ELSE 0 END) FROM ww_incidents WHERE incident_date BETWEEN '2025-07-01' AND '2026-06-30' GROUP BY region"):
    regrate[region]=round(100*rc/ev) if ev else 0
REAL=lambda r: r!="Other - Unmapped"
NAT=dict(ev=sum(r['events'] for r in rows),rec=sum(r['total'] for r in rows),dir=sum(r['direct'] for r in rows),
         pkg=sum(r['pkg'] for r in rows),sto=sum(r['stolen'] for r in rows),stores=sum(1 for r in rows if r['events']))
natrate=c.execute("SELECT SUM(CASE WHEN recovery_type IN ('full','partial') THEN 1 ELSE 0 END),COUNT(*) FROM ww_incidents WHERE incident_date BETWEEN '2025-07-01' AND '2026-06-30'").fetchone()
NAT['rate']=round(100*natrate[0]/natrate[1])
reg=defaultdict(lambda:defaultdict(float))
for r in rows:
    if not REAL(r['region']): continue
    R=reg[r['region']]; R['ev']+=r['events']; R['rec']+=r['total']; R['sto']+=r['stolen']
def m(v): return f"${v:,.0f}"
def kpi(l,v,col="#1f2933",s=""):
    return f'<div style="flex:1"><div style="font-size:8.5px;color:{SUB};text-transform:uppercase;letter-spacing:.6px">{l}</div><div style="font-size:20px;font-weight:700;color:{col};margin-top:2px">{v}</div>{f"<div style=\"font-size:8.5px;color:{SUB}\">{s}</div>" if s else ""}</div>'
TH=f'background:{HEAD};color:{SUB};font-size:8.5px;text-transform:uppercase;letter-spacing:.5px;padding:6px 8px'
def regrows():
    o=""
    for region,v in sorted(reg.items(),key=lambda x:-x[1]['rec']):
        rate=regrate.get(region,0); rc=GREEN if rate>=85 else(ACC if rate>=70 else RED)
        o+=f'<tr><td style="padding:6px 8px;font-weight:600">{region.split(" -")[0]}</td><td style="text-align:center;color:{SUB}">{int(v["ev"])}</td><td style="text-align:right;color:{GREEN};font-weight:600">{m(v["rec"])}</td><td style="text-align:right;color:{RED}">{m(v["sto"])}</td><td style="text-align:center;color:{rc};font-weight:700">{rate}%</td></tr>'
    o+=f'<tr style="border-top:2px solid {ACC}"><td style="padding:7px 8px;font-weight:700">TOTAL</td><td style="text-align:center;font-weight:700">{NAT["ev"]}</td><td style="text-align:right;font-weight:700;color:{GREEN}">{m(NAT["rec"])}</td><td style="text-align:right;font-weight:700;color:{RED}">{m(NAT["sto"])}</td><td style="text-align:center;font-weight:700">{NAT["rate"]}%</td></tr>'
    return o
def topstores(region,n):
    sel=sorted([r for r in rows if r['region']==region and r['total']>0],key=lambda x:-x['total'])[:n]
    body=""
    for r in sel:
        body+=f'<tr><td style="padding:4px 8px;font-weight:600">{r["store"]}</td><td style="text-align:center;color:{SUB}">{r["events"]}</td><td style="text-align:right;color:{GREEN};font-weight:700">{m(r["total"])}</td><td style="text-align:center;color:{SUB}">{(str(r["rate"])+"%") if r["rate"] is not None else "—"}</td></tr>'
    return (f'<div style="margin-top:9px"><div style="color:{ACC};font-weight:700;font-size:11px">{region.split(" -")[0]} — Top {len(sel)}</div>'
            f'<table style="width:100%;border-collapse:collapse;font-size:10px;margin-top:3px"><thead><tr>'
            f'<th style="{TH};text-align:left">Store</th><th style="{TH};text-align:center">Ev</th><th style="{TH};text-align:right">Recovered</th><th style="{TH};text-align:center">Rate</th></tr></thead><tbody>{body}</tbody></table></div>')
order=sorted([r for r in reg],key=lambda x:-reg[x]['rec'])
logo=f"data:image/png;base64,{base64.b64encode(LOGO.read_bytes()).decode()}"
# Auckland full width; others in 2 columns
others=[r for r in order if 'Auckland' not in r]
col1=others[0::2]; col2=others[1::2]
HTML=f"""<html><head><meta charset='utf-8'><style>*{{margin:0;box-sizing:border-box;font-family:-apple-system,Segoe UI,Arial,sans-serif}}
body{{background:#fff;color:#1f2933}} .page{{padding:24px 28px;page-break-after:always}} .page:last-child{{page-break-after:auto}}
table{{width:100%;border-collapse:collapse;font-size:11px}} tbody tr{{border-bottom:1px solid {LINE}}} h2{{color:{ACC};font-size:13px;letter-spacing:.6px;margin:0 0 6px}}</style></head><body>
<div class="page">
<div style="display:flex;justify-content:space-between;align-items:flex-start;border-bottom:2px solid {ACC};padding-bottom:10px">
  <div><div style="font-size:22px;font-weight:800">WOOLWORTHS NZ — NATIONAL LP PERFORMANCE</div>
  <div style="color:{SUB};font-size:12px;margin-top:2px">SLS RTC Limited · Covert Loss Prevention · FY Jul 2025 – Jun 2026</div></div>
  <img src="{logo}" style="height:34px;opacity:.9"/></div>
<div style="display:flex;gap:6px;background:#f6f8fa;border:1px solid {LINE};border-radius:8px;padding:12px 16px;margin:14px 0">
  {kpi("Stores",str(NAT['stores']))}{kpi("Events",f"{NAT['ev']:,}")}{kpi("Recovered",m(NAT['rec']),GREEN,"incl. packaging")}{kpi("Stolen (loss)",m(NAT['sto']),RED)}{kpi("Recovery Rate",f"{NAT['rate']}%",GREEN)}{kpi("Deterrents",f"{det:,}",ACC,"prevented")}</div>
<h2>REGIONAL PERFORMANCE</h2>
<table><thead><tr><th style="{TH};text-align:left">Region</th><th style="{TH};text-align:center">Events</th><th style="{TH};text-align:right">Recovered (incl. pkg)</th><th style="{TH};text-align:right">Stolen</th><th style="{TH};text-align:center">Recovery</th></tr></thead><tbody>{regrows()}</tbody></table>
<p style="font-size:9px;color:{SUB};margin-top:6px">Recovered = direct product recovery + recovered packaging (Woolworths convention). National split: direct {m(NAT['dir'])} + packaging {m(NAT['pkg'])}.</p>
<h2 style="margin-top:16px">TOP PERFORMING STORES — AUCKLAND</h2>
{topstores([r for r in order if 'Auckland' in r][0],10)}
</div>
<div class="page">
<h2>TOP PERFORMING STORES — BY REGION</h2>
<div style="display:flex;gap:18px"><div style="flex:1">{''.join(topstores(r,5) for r in col1)}</div><div style="flex:1">{''.join(topstores(r,5) for r in col2)}</div></div>
<div style="margin-top:16px;background:#f6f8fa;border-left:3px solid {ACC};border-radius:4px;padding:9px 13px;font-size:9.5px;color:{SUB};line-height:1.5">
  <b style="color:{ACC}">Recovery</b> includes direct product recovery + recovered packaging. <b style="color:{ACC}">Recovery rate</b> = full + partial recoveries ÷ events. <b style="color:{ACC}">Deterrents</b> ({det:,}) are interventions that prevented theft before it occurred — tracked separately and not in recovery figures; they represent the larger share of LP value. Period FY 1 Jul 2025 – 30 Jun 2026. Source: SLS RTC truth store (Auror-linked incidents + master packaging).</div>
</div></body></html>"""
async def render():
    from playwright.async_api import async_playwright
    OUT.parent.mkdir(parents=True,exist_ok=True)
    async with async_playwright() as pw:
        b=await pw.chromium.launch(); p=await b.new_page(); await p.set_content(HTML,wait_until="networkidle")
        await p.pdf(path=str(OUT),format="A4",print_background=True,margin={"top":"0","bottom":"0","left":"0","right":"0"}); await b.close()
if __name__=="__main__":
    print(f"national recovered (incl pkg)=${NAT['rec']:,.0f}  rate={NAT['rate']}%")
    asyncio.run(render()); print("WROTE:",OUT)
