#!/usr/bin/env python3
"""Mitre 10 MEGA New Lynn — First-Week Covert LP Report + Store Assessment (clean white)."""
import asyncio, base64, fitz, re
from pathlib import Path
GIR=Path.home()/"Downloads/Mitre 10 _ Guard Incident Report_June_14_2026_to_June_20_2026.pdf"
ASSESS=Path.home()/"Downloads/Mitre 10 _ Store Assessment Report.pdf"
LOGO=Path.home()/"Desktop/SLS-RTC/Operations/Analytics/assets/slsrtc_logo_hd.png"
OUT1=Path.home()/"Desktop/Mitre10/Mitre10_New_Lynn_First_Week_LP_Report.pdf"
OUT2=Path.home()/"Desktop/Mitre10/Mitre10_New_Lynn_Store_Assessment.pdf"
ACC="#1f3a5f"; SUB="#5b6472"; LINE="#dfe3e8"; RED="#b23a3a"; GREEN="#1d7a4d"; CARD="#f6f8fa"; AMBER="#c98a1a"
RECOVERIES=[17.18,141.32,93.82,39.98,13.45,130.19,29.78,50.56,4.99,369.98,51.96,470.00]
TOTAL_REC=sum(RECOVERIES)
# ---- parse incidents ----
full="\n".join(p.get_text() for p in fitz.open(GIR))
blocks=re.split(r'Date and Time of Incident:\s*',full)[1:]
inc=[]
for b in blocks:
    dt=re.match(r'([0-9/]+),\s*([0-9:]+)',b)
    date,time=(dt.group(1),dt.group(2)) if dt else ('?','')
    cat=re.search(r'Incident Category:\s*(\w+)',b); cat=cat.group(1) if cat else '?'
    cause=re.search(r'Cause/Reason for Intervention:\s*([^\n]+)',b); cause=cause.group(1).strip() if cause else ('—' if cat=='Deterrent' else '')
    sev=re.search(r'Severity:\s*\n?\s*(\d)',b); sev=int(sev.group(1)) if sev else None
    vt=re.search(r'Verbal Trespass\s*:\s*(\w+)',b); vt=vt.group(1) if vt else 'No'
    inc.append(dict(date=date,time=time,cat=cat,cause=cause,sev=sev,vt=vt))
N=len(inc); interv=sum(1 for i in inc if i['cat']=='Intervention'); deter=sum(1 for i in inc if i['cat']=='Deterrent')
vt=sum(1 for i in inc if i['vt']=='Yes'); store="Mitre 10 MEGA New Lynn"
dmin="15 Jun"; dmax="20 Jun 2026"
def m(v): return f"${v:,.2f}"
def kpi(l,v,col="#1f2933",s=""):
    return f'<div style="flex:1"><div style="font-size:8.5px;color:{SUB};text-transform:uppercase;letter-spacing:.6px">{l}</div><div style="font-size:21px;font-weight:700;color:{col};margin-top:2px">{v}</div>{f"<div style=\"font-size:8.5px;color:{SUB}\">{s}</div>" if s else ""}</div>'
TH=f'background:{CARD};color:{SUB};font-size:8.5px;text-transform:uppercase;letter-spacing:.5px;padding:6px 8px'
SEV={1:'1 — Low',2:'2 — Medium',3:'3 — High',None:'—'}
def inc_rows():
    o=""
    for i in inc:
        catc=GREEN if i['cat']=='Intervention' else ACC
        d=f"{i['date'][:5]}, {i['time']}"
        o+=f'<tr><td style="padding:4px 8px">{d}</td><td style="text-align:center;color:{catc};font-weight:700">{i["cat"]}</td><td style="padding:4px 8px;color:{SUB}">{i["cause"]}</td><td style="text-align:center;color:{SUB}">{i["vt"]}</td></tr>'
    return o
def rec_rows():
    o=""
    for n,v in enumerate(sorted(RECOVERIES,reverse=True),1):
        o+=f'<tr><td style="padding:4px 8px;color:{SUB}">Recovery {n}</td><td style="text-align:right;color:{GREEN};font-weight:600">{m(v)}</td></tr>'
    return o
logo=f"data:image/png;base64,{base64.b64encode(LOGO.read_bytes()).decode()}"
HTML=f"""<html><head><meta charset='utf-8'><style>*{{margin:0;box-sizing:border-box;font-family:-apple-system,Segoe UI,Arial,sans-serif}}
body{{background:#fff;color:#1f2933;padding:24px 28px}} table{{width:100%;border-collapse:collapse;font-size:11px}} tbody tr{{border-bottom:1px solid {LINE}}}
h2{{color:{ACC};font-size:13px;letter-spacing:.6px;margin:0 0 6px}} .lead{{color:{SUB};font-size:11px;line-height:1.5}}</style></head><body>
<div style="display:flex;justify-content:space-between;align-items:flex-start;border-bottom:2px solid {ACC};padding-bottom:10px">
  <div><div style="font-size:21px;font-weight:800">MITRE 10 — FIRST-WEEK COVERT LP REPORT</div>
  <div style="color:{SUB};font-size:12px;margin-top:2px">{store} · SLS RTC Limited · {dmin} – {dmax}</div></div>
  <img src="{logo}" style="height:34px;opacity:.9"/></div>
<div style="display:flex;gap:6px;background:{CARD};border:1px solid {LINE};border-radius:8px;padding:12px 16px;margin:14px 0">
  {kpi("Store","1",ACC,"launch")}{kpi("Incidents",str(N))}{kpi("Interventions",str(interv),GREEN)}{kpi("Deterrents",str(deter),ACC)}{kpi("Recovered",m(TOTAL_REC),GREEN,f"{len(RECOVERIES)} recoveries")}{kpi("Verbal Trespasses",str(vt))}</div>
<p class="lead">SLS RTC commenced covert loss-prevention at <b>{store}</b> on 15 June 2026. In the first week the team actioned <b>{N} incidents</b> ({interv} active interventions, {deter} deterrents), recovered <b>{m(TOTAL_REC)}</b> of product across <b>{len(RECOVERIES)} recoveries</b>, and issued <b>{vt} verbal trespass notices</b> — strong, measurable results from launch. A parallel store security assessment was completed (see separate report).</p>
<div style="display:flex;gap:18px;margin-top:14px">
  <div style="flex:1.7"><h2>INCIDENT LOG</h2>
  <table><thead><tr><th style="{TH};text-align:left">Date/Time</th><th style="{TH};text-align:center">Category</th><th style="{TH};text-align:left">Cause</th><th style="{TH};text-align:center">Verbal Trespass</th></tr></thead><tbody>{inc_rows()}</tbody></table></div>
  <div style="flex:1"><h2 style="color:{GREEN}">RECOVERIES — {m(TOTAL_REC)}</h2>
  <table><thead><tr><th style="{TH};text-align:left">Item</th><th style="{TH};text-align:right">Value</th></tr></thead><tbody>{rec_rows()}
  <tr style="border-top:2px solid {GREEN}"><td style="padding:6px 8px;font-weight:700">TOTAL</td><td style="text-align:right;font-weight:700;color:{GREEN}">{m(TOTAL_REC)}</td></tr></tbody></table></div></div>
<div style="margin-top:16px;background:{CARD};border-left:3px solid {ACC};border-radius:4px;padding:10px 13px;font-size:9.5px;color:{SUB};line-height:1.55">
  <b style="color:{ACC}">Launch week.</b> Covert deployment at the pilot store. {m(TOTAL_REC)} of product recovered across {len(RECOVERIES)} recoveries; recoveries shown ranked by value. As the engagement scales, reporting will mirror our established multi-store LP reporting (recovery value incl. packaging, recovery rate, deterrents, and per-store performance). Source: SLS RTC covert LP reporting (Auror-linked incidents).</div>
</body></html>"""
# ---- assessment report ----
at="\n".join(p.get_text() for p in fitz.open(ASSESS))
ablocks=re.split(r'Mitre 10 \| Store Assessment',at)
obs=[]
for b in ablocks:
    desc=re.search(r'Description of observation:\s*(.+?)\nImages',b,re.S)
    rec=re.search(r'next steps for the store to action:\s*(.+?)\n(?:Signature|$)',b,re.S)
    if desc: obs.append((re.sub(r'\s+',' ',desc.group(1)).strip(), re.sub(r'\s+',' ',rec.group(1)).strip() if rec else ''))
SEVMAP=['High','High','Medium','High']  # assigned by exposure: machete key + walk-out = High
def acard(i,o,r,sv):
    c={'High':RED,'Medium':AMBER}[sv]
    return f"""<div style="background:{CARD};border:1px solid {LINE};border-left:4px solid {c};border-radius:6px;padding:12px 15px;margin-bottom:10px">
      <div style="display:flex;justify-content:space-between"><div style="font-size:12px;font-weight:700;color:{ACC}">Finding {i}</div><div style="font-size:9px;font-weight:700;color:{c};text-transform:uppercase">{sv} risk</div></div>
      <div style="margin-top:6px;font-size:10.5px;color:{SUB}"><b style="color:#1f2933">Observation:</b> {o}</div>
      <div style="margin-top:4px;font-size:10.5px;color:{SUB}"><b style="color:{GREEN}">Recommended action:</b> {r}</div></div>"""
HTML2=f"""<html><head><meta charset='utf-8'><style>*{{margin:0;box-sizing:border-box;font-family:-apple-system,Segoe UI,Arial,sans-serif}}
body{{background:#fff;color:#1f2933;padding:26px 30px}}</style></head><body>
<div style="display:flex;justify-content:space-between;align-items:flex-start;border-bottom:2px solid {ACC};padding-bottom:10px">
  <div><div style="font-size:21px;font-weight:800">STORE SECURITY ASSESSMENT</div>
  <div style="color:{SUB};font-size:12px;margin-top:2px">{store} · SLS RTC Limited · June 2026</div></div>
  <img src="{logo}" style="height:34px;opacity:.9"/></div>
<p style="color:{SUB};font-size:11px;line-height:1.5;margin:14px 0">During our first-week deployment our team conducted a covert security assessment of the store, identifying the following vulnerabilities and recommended actions. Several were demonstrated live — including accessing secured stock and walking out undetected — highlighting immediate, addressable loss exposure.</p>
{''.join(acard(i+1,o,r,SEVMAP[i] if i<len(SEVMAP) else 'Medium') for i,(o,r) in enumerate(obs))}
<div style="margin-top:8px;background:{CARD};border-left:3px solid {ACC};border-radius:4px;padding:10px 13px;font-size:9.5px;color:{SUB};line-height:1.55">
  Prepared by SLS RTC Limited from on-floor observations during the launch week. We're happy to help implement these controls and re-assess after changes. Source: SLS RTC Mitre 10 store assessment submissions.</div>
</body></html>"""
async def render():
    from playwright.async_api import async_playwright
    OUT1.parent.mkdir(parents=True,exist_ok=True)
    async with async_playwright() as pw:
        b=await pw.chromium.launch(); p=await b.new_page()
        await p.set_content(HTML,wait_until="networkidle"); await p.pdf(path=str(OUT1),format="A4",print_background=True,margin={"top":"0","bottom":"0","left":"0","right":"0"})
        await p.set_content(HTML2,wait_until="networkidle"); await p.pdf(path=str(OUT2),format="A4",print_background=True,margin={"top":"0","bottom":"0","left":"0","right":"0"})
        await b.close()
if __name__=="__main__":
    print(f"incidents={N} interv={interv} deter={deter} vt={vt} recovered=${TOTAL_REC:.2f} obs={len(obs)}")
    asyncio.run(render()); print("WROTE:",OUT1,"+",OUT2)
