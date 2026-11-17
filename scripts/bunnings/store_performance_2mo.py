#!/usr/bin/env python3
"""
Bunnings Store Performance — last 2 months (April + May 2026) for Mark (GM SLS).
Dark SLS-RTC dashboard theme, A4 landscape, rendered HTML -> PDF via Playwright.
Data source: asg-ops-hub truth store (bunnings_incidents + timeclock_shifts).
"""
import asyncio, base64, sqlite3
from collections import defaultdict
from pathlib import Path

DB   = Path.home()/ "Desktop/Dev/asg-ops-hub/data/truth.db"
LOGO = Path.home()/ "Desktop/SLS-RTC/Operations/Analytics/assets/slsrtc_logo_hd.png"
OUT  = Path.home()/ "Desktop/SLS-RTC/Operations/Bunnings/Bunnings_Store_Performance_Apr-May_2026.pdf"
A    = ("2026-04-01", "2026-05-31")
RATE = 43.0   # $/hr blended Bunnings guard cost (ROI rule)

GOLD="#d4a72c"; GREEN="#56c271"; RED="#e8625f"; BG="#0a0d16"; CARD="#11151f"
HEAD="#1c2230"; SUB="#8a93a6"; LINE="#232a3a"

def norm(s):
    s=(s or "").lower().strip()
    if s.startswith("bunnings"): s=s[8:].strip()
    return {"hamilton south":"south hamilton"}.get(s,s)

def load():
    c=sqlite3.connect(DB)
    rows=c.execute("SELECT region,store,recovery_type,COALESCE(recovered_value,0),COALESCE(stolen_value,0) "
                   "FROM bunnings_incidents WHERE incident_date>=? AND incident_date<=?",A).fetchall()
    n2reg={norm(s):r for r,s in c.execute("SELECT region,store FROM bunnings_incidents")}
    hrs=defaultdict(float); reghrs=defaultdict(float); tot_h=0
    for store,h in c.execute("SELECT store,COALESCE(hours,0) FROM timeclock_shifts "
                             "WHERE LOWER(client)='bunnings' AND shift_date>=? AND shift_date<=?",A):
        hrs[norm(store)]+=h; reghrs[n2reg.get(norm(store),"Unknown")]+=h; tot_h+=h
    isrec=lambda rt:str(rt).lower() in("full","partial")
    reg=defaultdict(lambda:{"ev":0,"rec":0.,"sto":0.,"rc":0})
    st =defaultdict(lambda:{"reg":"","ev":0,"rec":0.,"sto":0.,"rc":0})
    for region,store,rt,rec,sto in rows:
        for d in (reg[region],st[store]):
            d["ev"]+=1; d["rec"]+=rec; d["sto"]+=sto; d["rc"]+=1 if isrec(rt) else 0
        st[store]["reg"]=region
    return reg,st,hrs,reghrs,tot_h

MONTHS=["2026-02","2026-03","2026-04","2026-05"]
MLABEL={"2026-02":"Feb","2026-03":"Mar","2026-04":"Apr","2026-05":"May"}
def load_monthly():
    c=sqlite3.connect(DB); isrec=lambda rt:str(rt).lower() in("full","partial")
    mon=defaultdict(lambda:{"ev":0,"rec":0.,"sto":0.,"rc":0}); hbym=defaultdict(float)
    smat=defaultdict(lambda:defaultdict(float))
    for d,store,rt,rec,sto in c.execute("SELECT substr(incident_date,1,7),store,recovery_type,"
            "COALESCE(recovered_value,0),COALESCE(stolen_value,0) FROM bunnings_incidents "
            "WHERE incident_date>='2026-02-01' AND incident_date<='2026-05-31'"):
        m=mon[d]; m["ev"]+=1; m["rec"]+=rec; m["sto"]+=sto; m["rc"]+=1 if isrec(rt) else 0
        smat[store][d]+=rec
    for hm,h in c.execute("SELECT substr(shift_date,1,7),COALESCE(hours,0) FROM timeclock_shifts "
            "WHERE LOWER(client)='bunnings' AND shift_date>='2026-02-01' AND shift_date<='2026-05-31'"):
        hbym[hm]+=h
    return mon,hbym,smat

def money(v): return f"${v:,.0f}"

def kpi(label,val,color="#fff",sub=""):
    s=f'<div style="font-size:9px;color:{SUB};text-transform:uppercase;letter-spacing:.6px">{label}</div>'
    s+=f'<div style="font-size:23px;font-weight:700;color:{color};margin-top:2px">{val}</div>'
    if sub: s+=f'<div style="font-size:9px;color:{SUB}">{sub}</div>'
    return f'<div style="flex:1">{s}</div>'

def region_card(name,d,h):
    rep=d["rec"]+d["sto"]; rate=d["rc"]/d["ev"]*100 if d["ev"] else 0
    roi=rep/(h*RATE) if h else 0
    rate_c=GREEN if rate>=85 else (GOLD if rate>=60 else RED)
    flag = d["ev"]==0 and h>0
    border = RED if flag else LINE
    name_c = RED if flag else GOLD
    foot = (f'<div style="margin-top:7px;border-top:1px solid {LINE};padding-top:6px;color:{RED};font-size:9px;font-weight:700">'
            f'&#9888; {h:,.0f} guard hrs &middot; 0 incidents logged</div>') if flag else (
            f'<div style="display:flex;gap:10px;margin-top:8px;border-top:1px solid {LINE};padding-top:7px">'
            f'<div><span style="font-size:8px;color:{SUB}">ROI </span><span style="color:{GOLD};font-weight:700">{roi:.2f}x</span></div>'
            f'<div><span style="font-size:8px;color:{SUB}">RATE </span><span style="color:{rate_c};font-weight:700">{rate:.0f}%</span></div>'
            f'<div><span style="font-size:8px;color:{SUB}">REPORTED </span><span style="font-weight:700">{money(rep)}</span></div></div>')
    return f"""
    <div style="flex:1;background:{CARD};border:1px solid {border};border-radius:8px;padding:11px 13px;min-width:150px">
      <div style="color:{name_c};font-weight:700;font-size:13px;letter-spacing:.5px">{name.upper()}</div>
      <div style="display:flex;gap:10px;margin-top:8px">
        <div><div style="font-size:8px;color:{SUB}">EVENTS</div><div style="font-size:15px;font-weight:700">{d['ev']}</div></div>
        <div><div style="font-size:8px;color:{SUB}">RECOVERED</div><div style="font-size:15px;font-weight:700;color:{GREEN}">{money(d['rec'])}</div></div>
        <div><div style="font-size:8px;color:{SUB}">STOLEN</div><div style="font-size:15px;font-weight:700;color:{RED}">{money(d['sto'])}</div></div>
      </div>
      {foot}
    </div>"""

def rows_recovery(st):
    out=""
    for s,d in sorted(st.items(),key=lambda kv:-kv[1]["rec"]):
        rate=d["rc"]/d["ev"]*100 if d["ev"] else 0; avg=d["rec"]/d["ev"] if d["ev"] else 0
        rc=GREEN if rate>=85 else (GOLD if rate>=60 else RED)
        out+=f"""<tr>
          <td style="padding:6px 8px;font-weight:600">{s}</td>
          <td style="text-align:center;color:{SUB}">{d['ev']}</td>
          <td style="text-align:right;color:{GREEN};font-weight:700">{money(d['rec'])}</td>
          <td style="text-align:right;color:{RED}">{money(d['sto'])}</td>
          <td style="text-align:center;color:{rc};font-weight:700">{rate:.0f}%</td>
          <td style="text-align:right;color:{SUB}">${avg:,.0f}</td></tr>"""
    return out

def rows_loss(st):
    out=""
    for s,d in sorted(st.items(),key=lambda kv:-kv[1]["sto"]):
        if d["sto"]<=0: continue
        rate=d["rc"]/d["ev"]*100 if d["ev"] else 0
        rc=GREEN if rate>=85 else (GOLD if rate>=60 else RED)
        out+=f"""<tr>
          <td style="padding:6px 8px;font-weight:600">{s}</td>
          <td style="text-align:center;color:{SUB}">{d['ev']}</td>
          <td style="text-align:right;color:{RED};font-weight:700">{money(d['sto'])}</td>
          <td style="text-align:right;color:{GREEN}">{money(d['rec'])}</td>
          <td style="text-align:center;color:{rc};font-weight:700">{rate:.0f}%</td></tr>"""
    return out

def rows_full(st,hrs):
    out=""
    for s,d in sorted(st.items(),key=lambda kv:-(kv[1]["rec"]+kv[1]["sto"])):
        rep=d["rec"]+d["sto"]; h=hrs.get(norm(s),0); roi=rep/(h*RATE) if h else 0
        rph=d["rec"]/h if h else 0; rate=d["rc"]/d["ev"]*100 if d["ev"] else 0
        roic=GREEN if roi>=0.5 else (GOLD if roi>=0.3 else RED)
        out+=f"""<tr>
          <td style="padding:5px 8px;font-weight:600">{s}</td>
          <td style="color:{SUB}">{d['reg']}</td>
          <td style="text-align:center">{d['ev']}</td>
          <td style="text-align:right;color:{GREEN}">{money(d['rec'])}</td>
          <td style="text-align:right;color:{RED}">{money(d['sto'])}</td>
          <td style="text-align:right;font-weight:600">{money(rep)}</td>
          <td style="text-align:center">{rate:.0f}%</td>
          <td style="text-align:right;color:{SUB}">{h:,.0f}</td>
          <td style="text-align:right;color:{roic};font-weight:700">{roi:.2f}x</td>
          <td style="text-align:right">${rph:,.0f}</td></tr>"""
    return out

def month_overall(mon,hbym):
    th='style="background:%s;color:%s;font-size:9px;text-transform:uppercase;letter-spacing:.5px;padding:7px 9px;text-align:right"'%(HEAD,SUB)
    th0=th.replace("text-align:right","text-align:left")
    hdr="".join(f"<th {th}>{MLABEL[m]}</th>" for m in MONTHS)
    def row(label,fn,bold=False):
        cells=""
        vals=[fn(m) for m in MONTHS]
        for m,(disp,raw) in zip(MONTHS,vals):
            peak=raw==max(v[1] for v in vals) and raw>0
            cells+=f'<td style="text-align:right;padding:6px 9px;{"color:%s;font-weight:700"%GOLD if peak else ""}">{disp}</td>'
        return f'<tr><td style="padding:6px 9px;{"font-weight:700" if bold else ""}">{label}</td>{cells}</tr>'
    def rate(m): d=mon[m]; return (f'{d["rc"]/d["ev"]*100:.0f}%' if d["ev"] else "0%", d["rc"]/d["ev"]*100 if d["ev"] else 0)
    def roi(m):
        d=mon[m]; rep=d["rec"]+d["sto"]; h=hbym[m]; v=rep/(h*RATE) if h else 0; return (f"{v:.2f}x",v)
    body=(row("Events",lambda m:(str(mon[m]["ev"]),mon[m]["ev"]))
        + row("Recovered",lambda m:(money(mon[m]["rec"]),mon[m]["rec"]),True)
        + row("Stolen (loss)",lambda m:(money(mon[m]["sto"]),mon[m]["sto"]))
        + row("Total Reported",lambda m:(money(mon[m]["rec"]+mon[m]["sto"]),mon[m]["rec"]+mon[m]["sto"]))
        + row("Recovery Rate",rate)
        + row("Guard Hours",lambda m:(f"{hbym[m]:,.0f}",hbym[m]))
        + row("ROI",roi))
    return f'<table><thead><tr><th {th0}>Metric</th>{hdr}</tr></thead><tbody>{body}</tbody></table>'

def store_matrix(smat,st):
    th='style="background:%s;color:%s;font-size:9px;text-transform:uppercase;letter-spacing:.5px;padding:7px 9px;text-align:right"'%(HEAD,SUB)
    th0=th.replace("text-align:right","text-align:left")
    hdr="".join(f"<th {th}>{MLABEL[m]}</th>" for m in MONTHS)+f"<th {th}>Apr&rarr;May</th>"
    rows=""
    for s in sorted(st.keys(),key=lambda x:-sum(smat[x].get(m,0) for m in MONTHS)):
        vals=[smat[s].get(m,0) for m in MONTHS]
        peak=max(vals) if vals else 0
        cells=""
        for m,v in zip(MONTHS,vals):
            cells+=f'<td style="text-align:right;padding:5px 9px;{"color:%s;font-weight:700"%GOLD if v==peak and v>0 else ("color:%s"%SUB if v==0 else "")}">{money(v) if v else "&mdash;"}</td>'
        delta=vals[3]-vals[2]; arr="&#9650;" if delta>50 else ("&#9660;" if delta<-50 else "&ndash;")
        ac=GREEN if delta>50 else (RED if delta<-50 else SUB)
        cells+=f'<td style="text-align:right;padding:5px 9px;color:{ac};font-weight:700">{arr} {money(abs(delta)) if abs(delta)>50 else ""}</td>'
        rows+=f'<tr><td style="padding:5px 9px;font-weight:600">{s}</td>{cells}</tr>'
    return f'<table><thead><tr><th {th0}>Store (recovered $/mo)</th>{hdr}</tr></thead><tbody>{rows}</tbody></table>'

def build_html(reg,st,hrs,reghrs,tot_h,mon,hbym,smat):
    logo=f"data:image/png;base64,{base64.b64encode(LOGO.read_bytes()).decode()}"
    TE=sum(d["ev"] for d in reg.values()); TR=sum(d["rec"] for d in reg.values())
    TS=sum(d["sto"] for d in reg.values()); TRC=sum(d["rc"] for d in reg.values())
    rep=TR+TS; rate=TRC/TE*100 if TE else 0; roi=rep/(tot_h*RATE) if tot_h else 0
    # include regions that have guard hours but logged zero incidents (e.g. Wellington) so the gap is visible
    allreg=set(reg)|({k for k in reghrs if k!="Unknown"})
    zero={"ev":0,"rec":0.,"sto":0.,"rc":0}
    cards="".join(region_card(r,reg.get(r,zero),reghrs.get(r,0))
                  for r in sorted(allreg,key=lambda r:-(reg.get(r,zero)["rec"], )[0]))
    th='style="background:%s;color:%s;font-size:9px;text-transform:uppercase;letter-spacing:.5px;padding:7px 8px;text-align:left"'%(HEAD,SUB)
    return f"""<html><head><meta charset="utf-8"><style>
    *{{margin:0;box-sizing:border-box;font-family:-apple-system,Segoe UI,Arial,sans-serif}}
    body{{background:{BG};color:#eef1f6;padding:22px 26px}}
    table{{width:100%;border-collapse:collapse;font-size:11px}}
    tbody tr{{border-bottom:1px solid {LINE}}}
    h2{{color:{GOLD};font-size:13px;letter-spacing:.8px;margin:0 0 8px}}
    </style></head><body>
    <div style="display:flex;justify-content:space-between;align-items:flex-start;border-bottom:2px solid {GOLD};padding-bottom:10px">
      <div>
        <div style="font-size:24px;font-weight:800;letter-spacing:1px">STORE PERFORMANCE &amp; ANALYSIS</div>
        <div style="color:{SUB};font-size:12px;margin-top:2px">Bunnings Covert LP &nbsp;|&nbsp; Last 2 Months &mdash; April &amp; May 2026</div>
      </div>
      <img src="{logo}" style="height:42px;background:#fff;padding:4px 9px;border-radius:6px"/>
    </div>

    <div style="display:flex;gap:6px;background:{CARD};border:1px solid {LINE};border-radius:8px;padding:12px 16px;margin:14px 0">
      {kpi("Stores Covered",str(len(st)))}
      {kpi("Total Events",str(TE))}
      {kpi("Recovered",money(TR),GREEN)}
      {kpi("Stolen (Loss)",money(TS),RED)}
      {kpi("Total Reported",money(rep))}
      {kpi("Recovery Rate",f"{rate:.0f}%",GREEN if rate>=85 else GOLD)}
      {kpi("ROI",f"{roi:.2f}x",GOLD,f"{tot_h:,.0f} hrs &times; ${RATE:.0f}")}
    </div>

    <h2>REGIONAL BREAKDOWN</h2>
    <div style="display:flex;gap:9px;margin-bottom:16px">{cards}</div>

    <div style="display:flex;gap:18px;margin-bottom:16px">
      <div style="flex:1">
        <h2 style="color:{GREEN}">TOP STORES &mdash; RECOVERY</h2>
        <table><thead><tr><th {th}>Store</th><th {th} style="text-align:center">Ev</th>
          <th {th} style="text-align:right">Recovered</th><th {th} style="text-align:right">Stolen</th>
          <th {th} style="text-align:center">Rate</th><th {th} style="text-align:right">Avg/Ev</th></tr></thead>
          <tbody>{rows_recovery(st)}</tbody></table>
      </div>
      <div style="flex:1">
        <h2 style="color:{RED}">LOSS HOTSPOTS &mdash; HIGHEST STOLEN</h2>
        <table><thead><tr><th {th}>Store</th><th {th} style="text-align:center">Ev</th>
          <th {th} style="text-align:right">Stolen</th><th {th} style="text-align:right">Recovered</th>
          <th {th} style="text-align:center">Rate</th></tr></thead>
          <tbody>{rows_loss(st)}</tbody></table>
      </div>
    </div>

    <div style="break-before:page;padding-top:4px">
      <div style="display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid {LINE};margin-bottom:10px">
        <div style="font-size:18px;font-weight:800;letter-spacing:.6px;color:{GOLD}">MONTHLY TREND &mdash; FEB &rarr; MAY 2026</div>
        <div style="color:{SUB};font-size:11px">Bunnings Covert LP &middot; recovery trajectory</div>
      </div>
      <div style="display:flex;gap:18px">
        <div style="flex:1.05">
          <h2>PROGRAMME &mdash; MONTH BY MONTH</h2>
          {month_overall(mon,hbym)}
          <div style="margin-top:9px;background:{CARD};border-left:3px solid {RED};border-radius:4px;padding:8px 12px;font-size:9.5px;color:{SUB};line-height:1.5">
            <b style="color:{RED}">&#9888; Wellington coverage gap</b> &mdash; Wellington Bunnings stores (Lyall Bay,
            Wellington Central, Petone, Porirua) were staffed ~233 guard hours across Apr&ndash;May but logged
            <b>zero incidents</b> (last activity Mar). Either a reporting gap (Auror not filed) or stores not being
            worked &mdash; ~$10k labour at 0.00x return. Needs review.
          </div>
        </div>
        <div style="flex:1.25">
          <h2>RECOVERY BY STORE &mdash; MONTH BY MONTH</h2>
          {store_matrix(smat,st)}
        </div>
      </div>
    </div>

    <div style="break-before:page;padding-top:4px">
    <div style="display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid {LINE};margin-bottom:10px">
      <div style="font-size:18px;font-weight:800;letter-spacing:.6px;color:{GOLD}">FULL STORE TABLE &mdash; DEPLOYMENT VIEW</div>
      <div style="color:{SUB};font-size:11px">All Bunnings stores &middot; April &amp; May 2026 &middot; sorted by total reported</div>
    </div>
    <table><thead><tr>
      <th {th}>Store</th><th {th}>Region</th><th {th} style="text-align:center">Events</th>
      <th {th} style="text-align:right">Recovered</th><th {th} style="text-align:right">Stolen</th>
      <th {th} style="text-align:right">Reported</th><th {th} style="text-align:center">Rate</th>
      <th {th} style="text-align:right">Hours</th><th {th} style="text-align:right">ROI</th>
      <th {th} style="text-align:right">Rec/Hr</th></tr></thead>
      <tbody>{rows_full(st,hrs)}</tbody></table>

    <div style="margin-top:14px;background:{CARD};border-left:3px solid {GOLD};border-radius:4px;padding:9px 13px;font-size:9.5px;color:{SUB};line-height:1.5">
      <b style="color:{GOLD}">ROI methodology</b> — Total Reported (recovered + estimated stolen) &divide; guard labour cost
      (hours &times; ${RATE:.0f}/hr blended). <b style="color:{GOLD}">Recovery rate</b> = full + partial recoveries &divide; events.
      Period 1 Apr &ndash; 31 May 2026. Source: SLS RTC truth store (Auror-linked incidents + timeclock hours).
      Auckland region hours include a small unmapped remainder.
    </div>
    </div>
    </body></html>"""

async def render(html):
    from playwright.async_api import async_playwright
    OUT.parent.mkdir(parents=True,exist_ok=True)
    async with async_playwright() as pw:
        b=await pw.chromium.launch(); p=await b.new_page()
        await p.set_content(html,wait_until="networkidle")
        await p.pdf(path=str(OUT),format="A4",landscape=True,print_background=True,
                    margin={"top":"0","bottom":"0","left":"0","right":"0"})
        await b.close()

if __name__=="__main__":
    reg,st,hrs,reghrs,tot_h=load()
    mon,hbym,smat=load_monthly()
    asyncio.run(render(build_html(reg,st,hrs,reghrs,tot_h,mon,hbym,smat)))
    print("WROTE:",OUT)
