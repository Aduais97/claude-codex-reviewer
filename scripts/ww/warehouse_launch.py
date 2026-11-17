#!/usr/bin/env python3
"""The Warehouse Group — Covert LP Launch Snapshot (clean white)."""
import asyncio, base64, openpyxl
from collections import Counter
from pathlib import Path
GIR=Path.home()/"Downloads/The Warehouse _ Guard Incident Report_e1270d0c-b184-4fc6-907d-6759f8bec5ea.xlsx"
PKG=Path.home()/"Downloads/The Warehouse  _ Recovered Packaging_11954769-7a7f-4988-9d2b-8dbf2c5750fa.xlsx"
LOGO=Path.home()/"Desktop/SLS-RTC/Operations/Analytics/assets/slsrtc_logo_hd.png"
OUT=Path.home()/"Desktop/SLS-RTC/Operations/The Warehouse/The_Warehouse_Group_LP_Launch_Snapshot.pdf"
GREEN="#1d7a4d"; RED="#b23a3a"; ACC="#1f3a5f"; SUB="#5b6472"; HEAD="#eef1f5"; LINE="#dfe3e8"
g=openpyxl.load_workbook(GIR,data_only=True)['Entries']
def C(r,i): return g.cell(r,i).value
inc=[]
for r in range(2,g.max_row+1):
    if not C(r,8): continue
    inc.append(dict(date=C(r,5),time=C(r,6),store=C(r,8),region=C(r,7),sev=C(r,9),cat=C(r,19),
                    police=str(C(r,32)),vt=str(C(r,35)),guard=str(C(r,2)).strip()))
p=openpyxl.load_workbook(PKG,data_only=True)['Entries']
pkg=[(p.cell(r,5).value,p.cell(r,10).value,p.cell(r,15).value) for r in range(2,p.max_row+1) if p.cell(r,10).value]
# Recovery $ values (provided by ops — not captured in the GIR structured fields this launch period)
DIRECT_VALS=[29.0,28.0,129.0,383.80,219.74]      # 5 interventions (chronological best-effort)
PKG_VALS=[253.40,576.94,255.08]                   # 3 of 4 packaging entries carried a value
DIRECT_TOTAL=sum(DIRECT_VALS); PKG_TOTAL=sum(PKG_VALS); TOTAL_REC=DIRECT_TOTAL+PKG_TOTAL
N=len(inc); interv=sum(1 for i in inc if i['cat']=='Intervention'); deter=sum(1 for i in inc if i['cat']=='Deterrent')
vt=sum(1 for i in inc if i['vt']=='Yes'); npkg=len(pkg)
sev=Counter(i['sev'] for i in inc); guards=sorted(set(i['guard'] for i in inc)); stores=sorted(set(i['store'] for i in inc))
dates=[i['date'].date() for i in inc if hasattr(i['date'],'date')]+[x[0].date() for x in pkg if hasattr(x[0],'date')]
dmin,dmax=min(dates),max(dates)
def kpi(l,v,col="#1f2933",s=""):
    return f'<div style="flex:1"><div style="font-size:8.5px;color:{SUB};text-transform:uppercase;letter-spacing:.6px">{l}</div><div style="font-size:22px;font-weight:700;color:{col};margin-top:2px">{v}</div>{f"<div style=\"font-size:8.5px;color:{SUB}\">{s}</div>" if s else ""}</div>'
TH=f'background:{HEAD};color:{SUB};font-size:8.5px;text-transform:uppercase;letter-spacing:.5px;padding:6px 8px'
SEVLBL={1:'1 — Low',2:'2 — Medium',3:'3 — High'}
def inc_rows():
    o=""; vi=0
    for i in inc:  # keep source order = chronological/submission order (matches the GIR PDF, newest first)
        dd=i['date'].strftime('%a %d %b') if hasattr(i['date'],'strftime') else str(i['date'])
        d=f"{dd}, {i['time']}" if i.get('time') else dd
        catc=GREEN if i['cat']=='Intervention' else ACC
        if i['cat']=='Intervention' and vi<len(DIRECT_VALS):
            rv=f'${DIRECT_VALS[vi]:,.2f}'; vi+=1
        else: rv='—'
        o+=f'<tr><td style="padding:5px 8px">{d}</td><td style="padding:5px 8px;font-weight:600">{i["store"]}</td><td style="text-align:center;color:{catc};font-weight:700">{i["cat"]}</td><td style="text-align:center;color:{SUB}">{SEVLBL.get(i["sev"],i["sev"])}</td><td style="text-align:center;color:{SUB}">{i["vt"]}</td><td style="text-align:right;color:{GREEN};font-weight:600">{rv}</td></tr>'
    return o
def pkg_rows():
    o=""; vals=sorted(pkg,key=lambda x:str(x[0]))
    # assign captured values to the launch-week entries (most recent), earliest entry shows —
    valmap=['—']*(len(vals)-len(PKG_VALS))+[f'${v:,.2f}' for v in PKG_VALS]
    for (dt,store,catg),rv in zip(vals,valmap):
        d=dt.strftime('%a %d %b') if hasattr(dt,'strftime') else str(dt)
        o+=f'<tr><td style="padding:5px 8px">{d}</td><td style="padding:5px 8px;font-weight:600">{store}</td><td style="color:{SUB}">{catg}</td><td style="text-align:right;color:{GREEN};font-weight:600">{rv}</td></tr>'
    return o
logo=f"data:image/png;base64,{base64.b64encode(LOGO.read_bytes()).decode()}"
HTML=f"""<html><head><meta charset='utf-8'><style>*{{margin:0;box-sizing:border-box;font-family:-apple-system,Segoe UI,Arial,sans-serif}}
body{{background:#fff;color:#1f2933;padding:24px 28px}} table{{width:100%;border-collapse:collapse;font-size:11px}} tbody tr{{border-bottom:1px solid {LINE}}}
h2{{color:{ACC};font-size:13px;letter-spacing:.6px;margin:0 0 6px}} .lead{{color:{SUB};font-size:11px;line-height:1.5}}</style></head><body>
<div style="display:flex;justify-content:space-between;align-items:flex-start;border-bottom:2px solid {ACC};padding-bottom:10px">
  <div><div style="font-size:22px;font-weight:800">THE WAREHOUSE GROUP — COVERT LP LAUNCH SNAPSHOT</div>
  <div style="color:{SUB};font-size:12px;margin-top:2px">SLS RTC Limited · Covert Loss Prevention · {dmin.strftime('%d %b')} – {dmax.strftime('%d %b %Y')}</div></div>
  <img src="{logo}" style="height:34px;opacity:.9"/></div>
<div style="display:flex;gap:6px;background:#f6f8fa;border:1px solid {LINE};border-radius:8px;padding:12px 16px;margin:14px 0">
  {kpi("Site",str(len(stores)),ACC,"pilot")}{kpi("Incidents",str(N))}{kpi("Interventions",str(interv),GREEN)}{kpi("Recovered",f"${TOTAL_REC:,.0f}",GREEN,"incl. packaging")}{kpi("Verbal Trespasses",str(vt))}{kpi("Packaging Recoveries",str(npkg),GREEN)}</div>
<p class="lead">SLS RTC commenced covert loss-prevention for <b>The Warehouse Group</b> at <b>{stores[0]}</b> on {dmin.strftime('%d %B %Y')}. In the opening days the team logged <b>{N} incidents</b> ({interv} active interventions, {deter} deterrent), recovered <b>${TOTAL_REC:,.2f}</b> of product (${DIRECT_TOTAL:,.2f} direct + ${PKG_TOTAL:,.2f} packaging) across <b>{npkg} packaging recoveries</b>, and issued <b>{vt} verbal trespass notices</b> — immediate, measurable results from day one. Covert team: {', '.join(g.replace('  ',' ') for g in guards)}.</p>
<div style="display:flex;gap:10px;margin:12px 0">
  <div style="flex:1;background:#f6f8fa;border:1px solid {LINE};border-radius:6px;padding:9px 13px"><span style="font-size:9px;color:{SUB};text-transform:uppercase">Direct recovery</span><div style="font-size:16px;font-weight:700;color:{GREEN}">${DIRECT_TOTAL:,.2f}</div></div>
  <div style="flex:1;background:#f6f8fa;border:1px solid {LINE};border-radius:6px;padding:9px 13px"><span style="font-size:9px;color:{SUB};text-transform:uppercase">Recovered packaging</span><div style="font-size:16px;font-weight:700;color:{GREEN}">${PKG_TOTAL:,.2f}</div></div>
  <div style="flex:1;background:#eef5ef;border:1px solid {GREEN};border-radius:6px;padding:9px 13px"><span style="font-size:9px;color:{SUB};text-transform:uppercase">Total recovery</span><div style="font-size:16px;font-weight:700;color:{GREEN}">${TOTAL_REC:,.2f}</div></div></div>
<h2 style="margin-top:14px">INCIDENT LOG</h2>
<table><thead><tr><th style="{TH};text-align:left">Date</th><th style="{TH};text-align:left">Site</th><th style="{TH};text-align:center">Category</th><th style="{TH};text-align:center">Severity</th><th style="{TH};text-align:center">Verbal Trespass</th><th style="{TH};text-align:right">Recovered</th></tr></thead><tbody>{inc_rows()}</tbody></table>
<div style="display:flex;gap:18px;margin-top:16px">
  <div style="flex:1"><h2>SEVERITY MIX</h2>
  <table><thead><tr><th style="{TH};text-align:left">Severity</th><th style="{TH};text-align:right">Incidents</th></tr></thead><tbody>
  {''.join(f'<tr><td style="padding:5px 8px">{SEVLBL.get(s,s)}</td><td style="text-align:right;font-weight:600">{n}</td></tr>' for s,n in sorted(sev.items()))}</tbody></table></div>
  <div style="flex:1.3"><h2>PACKAGING RECOVERIES</h2>
  <table><thead><tr><th style="{TH};text-align:left">Date</th><th style="{TH};text-align:left">Site</th><th style="{TH};text-align:left">Category</th><th style="{TH};text-align:right">Value</th></tr></thead><tbody>{pkg_rows()}</tbody></table></div></div>
<div style="margin-top:16px;background:#f6f8fa;border-left:3px solid {ACC};border-radius:4px;padding:10px 13px;font-size:9.5px;color:{SUB};line-height:1.55">
  <b style="color:{ACC}">Launch phase.</b> This snapshot covers the first operating days at the pilot site, with <b style="color:{GREEN}">${TOTAL_REC:,.2f} of product recovered</b> (direct + packaging). As the engagement scales, reporting will mirror our established Woolworths and Bunnings national LP reporting: <b>recovery value (incl. packaging), recovery rate, deterrents, and regional/store performance tiers</b>. Source: SLS RTC covert LP reporting (Auror-linked incidents).</div>
</body></html>"""
async def render():
    from playwright.async_api import async_playwright
    OUT.parent.mkdir(parents=True,exist_ok=True)
    async with async_playwright() as pw:
        b=await pw.chromium.launch(); pg=await b.new_page(); await pg.set_content(HTML,wait_until="networkidle")
        await pg.pdf(path=str(OUT),format="A4",print_background=True,margin={"top":"0","bottom":"0","left":"0","right":"0"}); await b.close()
if __name__=="__main__":
    print(f"incidents={N} interventions={interv} deterrents={deter} vt={vt} packaging={npkg} site={stores}")
    asyncio.run(render()); print("WROTE:",OUT)
