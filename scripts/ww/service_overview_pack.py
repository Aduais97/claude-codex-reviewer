#!/usr/bin/env python3
"""
Woolworths NZ — Covert LP Service Overview pack for Glenn (SLS RTC Limited).
Answers all 5: Store Profiles & Hours, Spend, Commercials, Allocation Matrix, Notice.
Dark SLS-RTC theme, A4 portrait, HTML->PDF (Playwright).
"""
import asyncio, base64, openpyxl, sqlite3
from collections import defaultdict
from pathlib import Path

ALLOC = Path.home()/"Downloads/Progressive-StoreAllocation.xlsx"
SPEND = Path.home()/"Downloads/Progressive-Spend.xlsx"
DB    = Path.home()/"Desktop/Dev/asg-ops-hub/data/truth.db"
LOGO  = Path.home()/"Desktop/SLS-RTC/Operations/Analytics/assets/slsrtc_logo_hd.png"
OUT   = Path.home()/"Desktop/SLS-RTC/Operations/Woolworths/Woolworths_NZ_Service_Overview_for_Glenn.pdf"

# Clean light/white theme (ACCENT replaces the old "GOLD" var name throughout)
GOLD="#1f3a5f"; GREEN="#1d7a4d"; RED="#b23a3a"; BG="#ffffff"; CARD="#f6f8fa"
HEAD="#eef1f5"; SUB="#5b6472"; LINE="#dfe3e8"; MED="#2a6db0"
def norm(s): return str(s or "").replace(" Woolworths","").strip()

# ---- hours per store + region ----
def load_hours():
    ws=openpyxl.load_workbook(ALLOC,data_only=True)["All Jobs"]
    hrs=defaultdict(float); hpm=defaultdict(float)
    for row in ws.iter_rows(min_row=2,values_only=True):
        if row[0]:
            try: hrs[norm(row[0])]+=float(row[8])
            except: pass
        else:  # detail row: col2=Start Date, col6=Shift hours → hours by WORK month
            d=row[2]; h=row[6]
            if hasattr(d,'strftime') and isinstance(h,(int,float)): hpm[d.strftime('%Y-%m')]+=h
    return hrs, hpm

# ---- spend ----
def load_spend():
    ws=openpyxl.load_workbook(SPEND,data_only=True)["Progressive"]
    months=[]; region={}; monthly={}
    for r in range(1,ws.max_row+1):
        a=ws.cell(r,1).value
        if a=="Contact":
            months=[ws.cell(r,c).value for c in range(2,14)]
        elif a and "Progressive Foods" in str(a):
            reg=str(a).split("Woolworths")[-1].strip()
            region[reg]=ws.cell(r,14).value
        elif a=="Total":
            for i,m in enumerate(months):
                monthly[m]=ws.cell(r,2+i).value
            total=ws.cell(r,14).value
    return months, region, monthly, total

# ---- incidents/recovery ----
def load_inc():
    c=sqlite3.connect(DB); inc=defaultdict(int); rec=defaultdict(int); regm={}
    for region,store,rt in c.execute("SELECT region,store,recovery_type FROM ww_incidents WHERE incident_date>='2025-07-01'"):
        k=norm(store).lower(); inc[k]+=1; rec[k]+=(1 if str(rt) in('full','partial') else 0); regm[k]=region.split(' -')[0]
    return inc,rec,regm

HRS,HPM=load_hours(); MONTHS,REGION_SPEND,MONTHLY,TOTAL_SPEND=load_spend(); INC,REC,REGM=load_inc()

# Blended rate — invoices LAG work by 1 month (a June invoice = May's work), so align
# each invoice to the prior work-month's hours before dividing. Rate must be <= $45 (senior cap).
LBL2YM={'Jul 2025':'2025-07','Aug 2025':'2025-08','Sept 2025':'2025-09','Oct 2025':'2025-10',
        'Nov 2025':'2025-11','Dec 2025':'2025-12','Jan 2026':'2026-01','Feb 2026':'2026-02',
        'Mar 2026':'2026-03','Apr 2026':'2026-04','May 2026':'2026-05','Jun 2026':'2026-06'}
def _prev(ym):
    y,m=map(int,ym.split('-')); m-=1
    if m==0: y-=1; m=12
    return f'{y}-{m:02d}'
_ah=_ai=0
for lbl,val in MONTHLY.items():
    ym=LBL2YM.get(lbl);
    if not ym or not val: continue
    wm=_prev(ym); h=HPM.get(wm,0)
    if h: _ah+=h; _ai+=val
blended = _ai/_ah if _ah else 0  # lag-aligned blended charge-out rate
ALIAS={'hobsonville':'Auckland','amberley':'Canterbury','bureta park':'Bay of Plenty'}
SKIP={'travel to a site','travel from a ww site','head office slsrtc','sls rtc head office'}
DELIV={'Auckland':'Auckland','Canterbury':'Canterbury / South Island','Waikato':'Waikato',
       'Wellington':'Wellington','Manawatū-Whanganui':'Manawatū','Northland':'Northland','Bay of Plenty':'Bay of Plenty'}
# region hours (delivery) + core store rows
reghrs=defaultdict(float); overhead=0.0; core=defaultdict(list); total_hrs=0
for k,h in HRS.items():
    total_hrs+=h
    kl=k.lower()
    if kl in SKIP: overhead+=h; continue
    r=REGM.get(kl) or ALIAS.get(kl)
    rk=DELIV.get(r,'Other')
    reghrs[rk]+=h
    if h>=250:
        i=INC.get(kl,0); rt=round(100*REC.get(kl,0)/i) if i else None
        core[rk].append((k,h,i,rt))
def tier(h): return 'Critical' if h>=1500 else 'High' if h>=800 else 'Medium' if h>=350 else 'Standard'
ncore=sum(len(v) for v in core.values())

def money(v): return f"${v:,.0f}"
def kpi(label,val,color="#1f2933",sub=""):
    s=f'<div style="font-size:8.5px;color:{SUB};text-transform:uppercase;letter-spacing:.6px">{label}</div>'
    s+=f'<div style="font-size:21px;font-weight:700;color:{color};margin-top:2px">{val}</div>'
    if sub: s+=f'<div style="font-size:8.5px;color:{SUB}">{sub}</div>'
    return f'<div style="flex:1">{s}</div>'
TH=f'style="background:{HEAD};color:{SUB};font-size:8.5px;text-transform:uppercase;letter-spacing:.5px;padding:6px 8px;text-align:left"'
def th(extra=""): return TH if not extra else TH.replace('text-align:left',extra)

# ---- Section: regional hours+spend table ----
BILL={'Auckland':['Auckland','Northland'],'Wellington':['Wellington','Manawatū'],
      'Christchurch':['Canterbury / South Island'],'Waikato':['Waikato','Bay of Plenty']}
SPENDMAP={'Auckland':'Auckland','Wellington':'Wellington','Christchurch':'Christchurch','Waikato':'Waikato'}
reg_rows=""
for bill,delivs in BILL.items():
    h=sum(reghrs.get(d,0) for d in delivs)
    sp=REGION_SPEND.get(SPENDMAP[bill],0)
    reg_rows+=f'<tr><td style="padding:6px 8px;font-weight:600">{bill}</td><td style="text-align:right">{h:,.0f}</td><td style="text-align:right;color:{GREEN}">{money(sp)}</td></tr>'
_shown=sum(sum(reghrs.get(d,0) for d in dl) for dl in BILL.values())
_other=total_hrs-_shown
if _other>1:
    reg_rows+=f'<tr><td style="padding:6px 8px;color:{SUB}">Ad-hoc / roving + travel &amp; HQ</td><td style="text-align:right;color:{SUB}">{_other:,.0f}</td><td style="text-align:right;color:{SUB}">—</td></tr>'

# ---- Section: monthly spend table ----
mlab={'Jul 2025':'Jul','Aug 2025':'Aug','Sept 2025':'Sep','Oct 2025':'Oct','Nov 2025':'Nov','Dec 2025':'Dec','Jan 2026':'Jan','Feb 2026':'Feb','Mar 2026':'Mar','Apr 2026':'Apr','May 2026':'May','Jun 2026':'Jun'}
order=['Jul 2025','Aug 2025','Sept 2025','Oct 2025','Nov 2025','Dec 2025','Jan 2026','Feb 2026','Mar 2026','Apr 2026','May 2026','Jun 2026']
max_m=max(MONTHLY.get(m,0) for m in order)
mon_rows=""
for m in order:
    v=MONTHLY.get(m,0); bar=int(120*v/max_m)
    mon_rows+=f'<tr><td style="padding:4px 8px">{mlab.get(m,m)} </td><td style="text-align:right">{money(v)}</td><td style="width:140px"><div style="background:{GOLD};height:9px;width:{bar}px;border-radius:2px"></div></td></tr>'

# ---- Section: allocation matrix per region ----
def matrix_block(rk):
    rows=sorted(core.get(rk,[]),key=lambda x:-x[1])
    if not rows: return ""
    body=""
    for k,h,i,rt in rows:
        tc={'Critical':RED,'High':GOLD,'Medium':MED,'Standard':SUB}[tier(h)]
        body+=f'<tr><td style="padding:4px 8px;color:{tc};font-weight:700">{tier(h)}</td><td style="padding:4px 8px;font-weight:600">{k}</td><td style="text-align:right">{h:,.0f}</td><td style="text-align:center;color:{SUB}">{i}</td><td style="text-align:center;color:{SUB}">{(str(rt)+"%") if rt is not None else "—"}</td></tr>'
    return (f'<div style="margin-top:10px"><div style="color:{GOLD};font-weight:700;font-size:11px">{rk} — {len(rows)} stores · {sum(r[1] for r in rows):,.0f} hrs/yr</div>'
            f'<table style="width:100%;border-collapse:collapse;font-size:10px;margin-top:4px">'
            f'<thead><tr><th {th()}>Tier</th><th {th()}>Store</th><th {th("text-align:right")}>Hrs/yr</th><th {th("text-align:center")}>Inc</th><th {th("text-align:center")}>Rec</th></tr></thead><tbody>{body}</tbody></table></div>')
morder=['Auckland','Wellington','Canterbury / South Island','Waikato','Manawatū']
matrices="".join(matrix_block(r) for r in morder)

logo=f"data:image/png;base64,{base64.b64encode(LOGO.read_bytes()).decode()}"
HTML=f"""<html><head><meta charset='utf-8'><style>
*{{margin:0;box-sizing:border-box;font-family:-apple-system,Segoe UI,Arial,sans-serif}}
body{{background:{BG};color:#1f2933}}
.page{{width:210mm;min-height:297mm;padding:22px 26px;page-break-after:always;position:relative}}
.page:last-child{{page-break-after:auto}}
table{{width:100%;border-collapse:collapse;font-size:11px}} tbody tr{{border-bottom:1px solid {LINE}}}
h2{{color:{GOLD};font-size:14px;letter-spacing:.6px;margin:0 0 8px}}
.lead{{color:{SUB};font-size:11px;line-height:1.5}}
</style></head><body>

<div class="page">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;border-bottom:2px solid {GOLD};padding-bottom:10px">
    <div><div style="font-size:23px;font-weight:800">WOOLWORTHS NZ — COVERT LP SERVICE OVERVIEW</div>
    <div style="color:{SUB};font-size:12px;margin-top:2px">Prepared by SLS RTC Limited &nbsp;|&nbsp; FY Jul 2025 – Jun 2026 &nbsp;|&nbsp; Confidential</div></div>
    <img src="{logo}" style="height:34px;opacity:0.9"/>
  </div>
  <div style="display:flex;gap:6px;background:{CARD};border:1px solid {LINE};border-radius:8px;padding:12px 16px;margin:14px 0">
    {kpi("Core Stores",str(ncore))}{kpi("Regions","5")}
    {kpi("Delivered Hours",f"{total_hrs:,.0f}")}{kpi("12-mo Spend",money(TOTAL_SPEND),GREEN)}
    {kpi("Avg / Month",money(TOTAL_SPEND/12),GOLD,"ex-GST")}
  </div>
  <h2>1 · STORE PROFILES &amp; HOURS</h2>
  <p class="lead">Covert loss-prevention delivered nationally across <b>{ncore} core stores in 5 regions</b>, plus ad-hoc / roving coverage on request. <b>{total_hrs:,.0f} guard-hours</b> delivered in the 12 months to Jun 2026 (incl. ~{overhead:,.0f} h travel/HQ). Per-store annual hours by region:</p>
  <table style="margin-top:8px"><thead><tr><th {th()}>Region (billing)</th><th {th("text-align:right")}>Delivered hrs/yr</th><th {th("text-align:right")}>12-mo spend (ex-GST)</th></tr></thead>
  <tbody>{reg_rows}<tr style="border-top:2px solid {GOLD}"><td style="padding:7px 8px;font-weight:700">TOTAL</td><td style="text-align:right;font-weight:700">{total_hrs:,.0f}</td><td style="text-align:right;font-weight:700;color:{GREEN}">{money(TOTAL_SPEND)}</td></tr></tbody></table>
  <p class="lead" style="margin-top:8px">Auckland additionally operates to a documented deployment model: <b>608 guard-hrs/week, 18 operatives, 5 proximity clusters</b>. Full per-store tiering in Section 4. <i>(Billing regions group delivery regions — Wellington billing includes Manawatū; Christchurch covers South Island.)</i></p>

  <h2 style="margin-top:18px">2 · INVOICES &amp; SPEND — 12 MONTHS</h2>
  <p class="lead">Total <b>{money(TOTAL_SPEND)} ex-GST</b> invoiced (avg ~${TOTAL_SPEND/12:,.0f}/mo). Invoices are raised <b>one month in arrears</b> (e.g. a June invoice covers May's work). Invoiced spend covers guard hours (at $42.10 standard / $45.00 senior) <b>plus travel time, fuel and parking</b> where applicable, so it is not a flat hourly figure.</p>
  <table style="margin-top:8px"><thead><tr><th {th()}>Month</th><th {th("text-align:right")}>Spend (ex-GST)</th><th {th()}></th></tr></thead><tbody>{mon_rows}</tbody></table>
</div>

<div class="page">
  <h2>3 · COMMERCIALS &amp; CONTRACT</h2>
  <table style="margin-top:6px;font-size:11.5px">
    <tr><td style="padding:7px 8px;color:{SUB};width:38%">Provider</td><td style="padding:7px 8px;font-weight:600">SLS RTC Limited</td></tr>
    <tr><td style="padding:7px 8px;color:{SUB}">Service</td><td style="padding:7px 8px">Covert store loss-prevention personnel, Woolworths NZ (national)</td></tr>
    <tr><td style="padding:7px 8px;color:{SUB}">Agreement commenced</td><td style="padding:7px 8px">4 October 2016 &nbsp;·&nbsp; cost centre 620040</td></tr>
    <tr><td style="padding:7px 8px;color:{SUB}">Standard rate</td><td style="padding:7px 8px;font-weight:700">$42.10 / hour (ex-GST)</td></tr>
    <tr><td style="padding:7px 8px;color:{SUB}">Senior rate</td><td style="padding:7px 8px;font-weight:700">$45.00 / hour (ex-GST)</td></tr>
    <tr><td style="padding:7px 8px;color:{SUB}">Service standards (SLA)</td><td style="padding:7px 8px">Delivered to the Woolworths NZ Covert LP Standard Operating Procedures (v1, 06.03.2024) — incl. min 2 / max 5 officers per store per shift, no solo working, every event reported via the RTC App + Auror.</td></tr>
  </table>

  <h2 style="margin-top:18px">5 · SUPPLIER NOTIFICATION — NOTICE PERIODS</h2>
  <table style="margin-top:6px;font-size:11.5px">
    <tr><td style="padding:7px 8px;color:{SUB};width:38%">Contract termination</td><td style="padding:7px 8px;font-weight:600">90 days' written notice (either party)</td></tr>
    <tr><td style="padding:7px 8px;color:{SUB}">Permanent service change / additional guard request</td><td style="padding:7px 8px;font-weight:600">10 working days</td></tr>
    <tr><td style="padding:7px 8px;color:{SUB}">Urgent / temporary cover</td><td style="padding:7px 8px;font-weight:600">Within the hour (where staffing allows)</td></tr>
  </table>
  <p class="lead" style="margin-top:8px">Coverage changes are subject to NZ employment law (Employment Relations Act) and our covert officers' employment agreements; permanent reductions or relocations require reasonable notice to redeploy staff compliantly.</p>

  <h2 style="margin-top:18px">4 · ALLOCATION DECISION MATRIX (NATIONAL)</h2>
  <p class="lead">Guards are allocated by a combined priority model: <b>recorded offending (Auror-aligned) volume × recovery performance → store tier → allocated hours</b>, with WW's min-2/max-5 per-shift rule, proximity clustering + split-shift rotation (offender-migration control), and hours calibrated to each store's incident peak; re-tiered continuously on fresh data.
  &nbsp;Tier bands (allocated hrs/yr): <b style="color:{RED}">Critical ≥1,500</b> · <b style="color:{GOLD}">High 800–1,499</b> · <b style="color:{MED}">Medium 350–799</b> · <b style="color:{SUB}">Standard 250–349</b>.</p>
  {matrices}
  <p class="lead" style="margin-top:10px"><i>Demand input nationally uses our recorded incident volume (Auror-aligned); WW regional Auror data would refine tiering further. Inc = FY incidents; Rec = recovery rate.</i></p>
</div>
</body></html>"""

async def render():
    from playwright.async_api import async_playwright
    OUT.parent.mkdir(parents=True,exist_ok=True)
    async with async_playwright() as pw:
        b=await pw.chromium.launch(); p=await b.new_page()
        await p.set_content(HTML,wait_until="networkidle")
        await p.pdf(path=str(OUT),format="A4",print_background=True,margin={"top":"0","bottom":"0","left":"0","right":"0"})
        await b.close()

if __name__=="__main__":
    print(f"stores={ncore} hours={total_hrs:.0f} spend={TOTAL_SPEND:.0f} blended=${blended:.2f}")
    asyncio.run(render()); print("WROTE:",OUT)
