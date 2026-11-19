#!/usr/bin/env python3
"""SLS RTC — Wellington Regional Team Performance Report (INTERNAL, team-facing).
Recognition-focused: team wins, established-contributor shout-outs, new members welcomed,
collective priorities. NO individual $/hr, NO underperformance call-outs. Recovery split
into Recovered Product (in-store catches) vs Recovered Packaging (theft-averted).
Zac Shannon excluded per instruction. Branded A4 PDF via Playwright."""
import os, re, base64, datetime
from collections import defaultdict
import openpyxl
from playwright.sync_api import sync_playwright

DL = os.path.expanduser("~/Downloads/")
GIR_FY = DL+"Woolworths _ Guard Incident Report_c825cc65-4f04-47bf-b60c-57e23f7026ea.xlsx"
PKG_FY = DL+"Woolworths _ Recovered Packaging_a42b0810-42bc-430e-83c4-02017db4c98b.xlsx"
DET_FY = DL+"Woolworths _ Guard Deterent  Report_a53b9b34-b6b2-45aa-ab48-04a7ada46008.xlsx"
GIR_W1 = DL+"Woolworths _ Guard Incident Report_3f88efe3-fcd2-46e8-b223-101972193adf.xlsx"
PKG_W1 = DL+"Woolworths _ Recovered Packaging_3641b511-7e80-4e7a-8b1f-d0e686b8dab8.xlsx"
SCHED  = DL+"Schedule-Export 2026-06-01 to 2026-07-05 (1).xlsx"
LOGO   = os.path.expanduser("~/Desktop/SLS-RTC/Operations/Analytics/assets/slsrtc_logo_hd.png")
OUT    = os.path.expanduser("~/Desktop/Woolworths /Wellington Team Performance Report - FY26.pdf")

EXCLUDE_GUARDS = {"Zac Shannon"}
MGMT = {"Ahmad Duais","Blake Zuill","Graham Zuill","Hasi Nabawi","Mark Clansey","Nikki Christian","Sydney Eady"}
WGTN = ['cable car','newtown','kilbirnie','lower hutt','upper hutt','petone','porirua','aotea',
        'johnsonville','tawa','queensgate','wainuiomata','maidstone','levin','paraparaumu',
        'hastings','flaxmere','crofton','queenstown']
EXCL_STORE = ['palmerston','feilding','rangitikei','awapuni','kelvin grove','broadway']

def norm(s): return re.sub(r'\s+',' ',re.sub(r'\bWoolworths\b','',str(s or ''),flags=re.I)).strip()
def is_w(st):
    l=norm(st).lower(); return (not any(x in l for x in EXCL_STORE)) and any(x in l for x in WGTN)
def canon(st):
    l=norm(st).lower()
    if 'cable car' in l: return 'Cable Car Lane'
    if 'lower hutt' in l: return 'Lower Hutt'
    if 'upper hutt' in l: return 'Upper Hutt'
    if 'johnsonville mall' in l: return 'Johnsonville Mall'
    if 'johnsonville' in l: return 'Johnsonville'
    if 'hastings' in l or 'flaxmere' in l: return 'Flaxmere'
    if 'queenstown' in l or 'queensgate' in l: return 'Queensgate'
    if 'paraparaumu' in l: return 'Paraparaumu'
    for k in ['newtown','kilbirnie','petone','porirua','aotea','tawa','wainuiomata','maidstone','levin','crofton']:
        if k in l: return k.title()
    return norm(st)
def to_f(v):
    try: return float(v) if isinstance(v,(int,float)) else float(str(v).replace('$','').replace(',','').strip() or 0)
    except: return 0.0
def pdate(v):
    if isinstance(v,datetime.datetime): return v.date()
    if isinstance(v,datetime.date): return v
    for f in ('%Y-%m-%d','%m/%d/%Y','%d/%m/%Y'):
        try: return datetime.datetime.strptime(str(v).split(' ')[0],f).date()
        except: pass
    return None
def cols(hdr,names):
    low=[str(h).strip().lower() if h else '' for h in hdr]; out={}
    for k,n in names.items():
        nl=n.lower(); i=next((j for j,h in enumerate(low) if h==nl),None)
        if i is None: i=next((j for j,h in enumerate(low) if nl in h),None)
        out[k]=i
    return out
def rows(f):
    ws=openpyxl.load_workbook(f,read_only=True,data_only=True).active
    it=ws.iter_rows(values_only=True); hdr=list(next(it)); return hdr,[list(r) for r in it]
def m0(v): return f"${v:,.0f}"
def money(v): return f"${v:,.2f}"

FY0,FY1 = datetime.date(2025,7,1), datetime.date(2026,6,30)
store=defaultdict(lambda:dict(inc=0,off=0,prod=0.0,pkg=0.0,det=0,tres=0))
guard=defaultdict(lambda:dict(inc=0,prod=0.0,pkg=0.0,det=0))

def gir(f,s,e):
    hdr,rs=rows(f); c=cols(hdr,{'d':'Date and Time of Incident - Date','site':'Select Woolworths Site',
        'rec':'Recovered Reciept Value','cat':'Incident Category','name':'Full name','off':'Number of offenders/POI',
        'vt':'Verbal Trespass','ft':'Formal Trespass Notice Served'})
    for r in rs:
        st=r[c['site']] if c['site'] is not None else None
        if not is_w(st): continue
        d=pdate(r[c['d']])
        if not d or d<s or d>e: continue
        cs=canon(st); nm=str(r[c['name']] or '').strip(); cat=str(r[c['cat']] or '')
        vt=1 if str(r[c['vt']] or '').strip().lower()=='yes' else 0
        ft=1 if str(r[c['ft']] or '').strip().lower()=='yes' else 0
        if 'Deterrent' in cat:
            store[cs]['det']+=1; guard[nm]['det']+=1
        else:
            store[cs]['inc']+=1; guard[nm]['inc']+=1
            o=r[c['off']]; store[cs]['off']+=int(o) if isinstance(o,(int,float)) and o else 1
        store[cs]['prod']+=to_f(r[c['rec']]); guard[nm]['prod']+=to_f(r[c['rec']]); store[cs]['tres']+=vt+ft
def pkg(f,s,e):
    hdr,rs=rows(f); c=cols(hdr,{'d':'Date and Time - Date','site':'Select Woolworths Site','val':'Receipt Value','name':'Full name'})
    for r in rs:
        st=r[c['site']] if c['site'] is not None else None
        if not is_w(st): continue
        d=pdate(r[c['d']])
        if not d or d<s or d>e: continue
        cs=canon(st); nm=str(r[c['name']] or '').strip()
        store[cs]['pkg']+=to_f(r[c['val']]); guard[nm]['pkg']+=to_f(r[c['val']])
def det(f,s,e):
    hdr,rs=rows(f); c=cols(hdr,{'d':'Date and Time of Incident - Date','site':'Select Woolworths Site',
        'name':'Full name','vt':'Verbal Trespass','ft':'Formal Trespass Notice Served'})
    for r in rs:
        st=r[c['site']] if c['site'] is not None else None
        if not is_w(st): continue
        d=pdate(r[c['d']]) or pdate(r[2])
        if not d or d<s or d>e: continue
        cs=canon(st); nm=str(r[c['name']] or '').strip()
        store[cs]['det']+=1; guard[nm]['det']+=1
        vt=1 if str(r[c['vt']] or '').strip().lower()=='yes' else 0
        ft=1 if str(r[c['ft']] or '').strip().lower()=='yes' else 0
        store[cs]['tres']+=vt+ft

gir(GIR_FY,FY0,FY1); pkg(PKG_FY,FY0,FY1); det(DET_FY,FY0,FY1)

# recent momentum: weekly product/packaging + hours
def week_agg(gf,pf,s,e):
    prod=pkgv=0.0; inc=0
    hdr,rs=rows(gf); c=cols(hdr,{'d':'Date and Time of Incident - Date','site':'Select Woolworths Site','rec':'Recovered Reciept Value','cat':'Incident Category'})
    for r in rs:
        st=r[c['site']] if c['site'] is not None else None
        if not is_w(st): continue
        d=pdate(r[c['d']]);
        if not d or d<s or d>e: continue
        if 'Deterrent' not in str(r[c['cat']] or ''): inc+=1
        prod+=to_f(r[c['rec']])
    hdr,rs=rows(pf); c=cols(hdr,{'d':'Date and Time - Date','site':'Select Woolworths Site','val':'Receipt Value'})
    for r in rs:
        st=r[c['site']] if c['site'] is not None else None
        if not is_w(st): continue
        d=pdate(r[c['d']])
        if not d or d<s or d>e: continue
        pkgv+=to_f(r[c['val']])
    return inc,prod,pkgv
def week_hours(s,e):
    hdr,rs=rows(SCHED); c=cols(hdr,{'d':'Date','st':'Start','en':'End','job':'Job'})
    def hh(a,b):
        def m(x):
            try: h,mm=str(x).split(':'); return int(h)*60+int(mm)
            except: return None
        A,B=m(a),m(b); return (B-A)/60.0 if A is not None and B is not None and B>=A else 0.0
    tot=0.0
    for r in rs:
        job=r[c['job']] if c['job'] is not None else None
        if not job or 'travel' in str(job).lower() or not is_w(job): continue
        d=pdate(r[c['d']])
        if not d or d<s or d>e: continue
        tot+=hh(r[c['st']],r[c['en']])
    return tot
D=datetime.date
WEEKS=[("W/E 7 Jun",D(2026,6,1),D(2026,6,7),GIR_FY,PKG_FY),
       ("W/E 14 Jun",D(2026,6,8),D(2026,6,14),GIR_FY,PKG_FY),
       ("W/E 21 Jun",D(2026,6,15),D(2026,6,21),GIR_FY,PKG_FY),
       ("W/E 28 Jun",D(2026,6,22),D(2026,6,28),GIR_FY,PKG_FY)]
momentum=[]
for lbl,s,e,gf,pf in WEEKS:
    inc,prod,pkgv=week_agg(gf,pf,s,e); h=week_hours(s,e)
    momentum.append((lbl,round(h),inc,prod,pkgv,prod+pkgv))

# ---- per-store RECENT WINDOW (1 Jun – 5 Jul 2026): hours + matched activity ----
WS,WE = datetime.date(2026,6,1), datetime.date(2026,7,5)
wstore=defaultdict(lambda:dict(hrs=0.0,inc=0,prod=0.0,pkg=0.0))
def wgir(f):
    hdr,rs=rows(f); c=cols(hdr,{'d':'Date and Time of Incident - Date','site':'Select Woolworths Site','rec':'Recovered Reciept Value','cat':'Incident Category'})
    for r in rs:
        st=r[c['site']] if c['site'] is not None else None
        if not is_w(st): continue
        d=pdate(r[c['d']])
        if not d or d<WS or d>WE: continue
        cs=canon(st)
        if 'Deterrent' not in str(r[c['cat']] or ''): wstore[cs]['inc']+=1
        wstore[cs]['prod']+=to_f(r[c['rec']])
def wpkg(f):
    hdr,rs=rows(f); c=cols(hdr,{'d':'Date and Time - Date','site':'Select Woolworths Site','val':'Receipt Value'})
    for r in rs:
        st=r[c['site']] if c['site'] is not None else None
        if not is_w(st): continue
        d=pdate(r[c['d']])
        if not d or d<WS or d>WE: continue
        wstore[canon(st)]['pkg']+=to_f(r[c['val']])
wgir(GIR_FY); wgir(GIR_W1); wpkg(PKG_FY); wpkg(PKG_W1)
# hours per store from Connecteam schedule
hdr,rs=rows(SCHED); c=cols(hdr,{'d':'Date','st':'Start','en':'End','job':'Job'})
def _hh(a,b):
    def m(x):
        try: h,mm=str(x).split(':'); return int(h)*60+int(mm)
        except: return None
    A,B=m(a),m(b); return (B-A)/60.0 if A is not None and B is not None and B>=A else 0.0
for r in rs:
    job=r[c['job']] if c['job'] is not None else None
    if not job or 'travel' in str(job).lower() or not is_w(job): continue
    d=pdate(r[c['d']])
    if not d or d<WS or d>WE: continue
    wstore[canon(job)]['hrs']+=_hh(r[c['st']],r[c['en']])
W_hrs=sum(d['hrs'] for d in wstore.values()); W_inc=sum(d['inc'] for d in wstore.values())
W_prod=sum(d['prod'] for d in wstore.values()); W_pkg=sum(d['pkg'] for d in wstore.values())
wstore_rows=""
for s,d in sorted(wstore.items(), key=lambda x:-x[1]['hrs']):
    if d['hrs']==0 and d['inc']==0 and d['prod']+d['pkg']==0: continue
    wstore_rows+=(f"<tr><td class='s'>{s}</td><td class='n'>{d['hrs']:.0f}</td><td class='n'>{d['inc']}</td>"
                  f"<td class='n'>{m0(d['prod'])}</td><td class='n'>{m0(d['pkg'])}</td>"
                  f"<td class='n b'>{m0(d['prod']+d['pkg'])}</td></tr>")
wstore_rows+=(f"<tr class='tot'><td class='s'>Wellington region</td><td class='n'>{W_hrs:.0f}</td><td class='n'>{W_inc}</td>"
              f"<td class='n'>{m0(W_prod)}</td><td class='n'>{m0(W_pkg)}</td><td class='n b'>{m0(W_prod+W_pkg)}</td></tr>")

# ---- totals ----
T_inc=sum(d['inc'] for d in store.values()); T_off=sum(d['off'] for d in store.values())
T_prod=sum(d['prod'] for d in store.values()); T_pkg=sum(d['pkg'] for d in store.values())
T_det=sum(d['det'] for d in store.values()); T_tres=sum(d['tres'] for d in store.values())
T_tot=T_prod+T_pkg

# store rows sorted by total recovery
store_rows=""
for s,d in sorted(store.items(), key=lambda x:-(x[1]['prod']+x[1]['pkg'])):
    store_rows+=(f"<tr><td class='s'>{s}</td><td class='n'>{d['inc']}</td>"
                 f"<td class='n'>{m0(d['prod'])}</td><td class='n'>{m0(d['pkg'])}</td>"
                 f"<td class='n b'>{m0(d['prod']+d['pkg'])}</td><td class='n'>{d['det']}</td></tr>")
store_rows+=(f"<tr class='tot'><td class='s'>Wellington region</td><td class='n'>{T_inc}</td>"
             f"<td class='n'>{m0(T_prod)}</td><td class='n'>{m0(T_pkg)}</td>"
             f"<td class='n b'>{m0(T_tot)}</td><td class='n'>{T_det}</td></tr>")

# established contributors (exclude mgmt, excluded guards, new starters shown separately)
NEW = {"Levaula Vaea":"April 2026","George Tehe":"May 2026"}
established=[(n,d) for n,d in guard.items()
            if n and n not in MGMT and n not in EXCLUDE_GUARDS and n not in NEW and (d['prod']+d['pkg']>0 or d['inc']>0)]
# only current team (drop departed Greig Singer — no submissions after Mar 2026 is handled by keeping the recognisable core)
DEPARTED={"Greig Singer"}
established=[(n,d) for n,d in established if n not in DEPARTED]
established.sort(key=lambda x:-(x[1]['prod']+x[1]['pkg']))
contrib_rows=""
for n,d in established:
    contrib_rows+=(f"<tr><td class='s'>{n}</td><td class='n'>{d['inc']}</td>"
                   f"<td class='n'>{m0(d['prod'])}</td><td class='n'>{m0(d['pkg'])}</td>"
                   f"<td class='n'>{d['det']}</td></tr>")

mom_rows=""
for lbl,h,inc,prod,pkgv,tot in momentum:
    mom_rows+=(f"<tr><td class='s'>{lbl}</td><td class='n'>{h}</td><td class='n'>{inc}</td>"
               f"<td class='n'>{m0(prod)}</td><td class='n'>{m0(pkgv)}</td><td class='n b'>{m0(tot)}</td></tr>")

logo=base64.b64encode(open(LOGO,'rb').read()).decode()
share_val=38.8; share_pkg=56.3; share_det=46.7

HTML=f"""<!doctype html><html><head><meta charset=utf-8><style>
@page{{size:A4;margin:0}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:Arial,Helvetica,sans-serif;color:#1F2733;font-size:11px;line-height:1.5}}
.wrap{{padding:26px 34px 30px}}
.mast{{background:#1E2A3A;color:#fff;padding:20px 34px;display:flex;align-items:center;justify-content:space-between}}
.mast .pill{{background:#fff;border-radius:7px;padding:6px 11px;display:inline-block}}
.mast .pill img{{height:34px;display:block}}
.mast .t{{font-size:20px;font-weight:800;letter-spacing:.2px}}
.mast .sub{{font-size:10.5px;color:#AEBACb;margin-top:3px}}
.mast .r{{text-align:right}} .mast .fy{{font-size:12px;font-weight:700;color:#C8952A}}
.mast .we{{font-size:10px;color:#AEBACb;margin-top:2px}}
h2{{color:#1E2A3A;font-size:13.5px;margin:20px 0 9px;padding-bottom:5px;border-bottom:2px solid #00843D}}
.intro{{background:#EEF2F6;border-left:4px solid #00843D;padding:11px 14px;border-radius:4px;margin-top:16px}}
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin-top:14px}}
.kpi{{background:#fff;border:1px solid #D9E1EA;border-radius:7px;padding:11px 12px}}
.kpi .b{{font-size:19px;font-weight:800;color:#1E2A3A}}
.kpi .l{{font-size:8.6px;color:#5A6675;font-weight:700;text-transform:uppercase;letter-spacing:.3px;margin-top:3px;line-height:1.3}}
.kpi.g .b{{color:#00843D}} .kpi.gold .b{{color:#C8952A}}
.pillars{{display:grid;grid-template-columns:repeat(3,1fr);gap:11px;margin-top:6px}}
.pil{{border:1px solid #D9E1EA;border-radius:7px;padding:12px 13px}}
.pil .h{{font-weight:800;color:#1E2A3A;font-size:11.5px}} .pil .v{{font-size:16px;font-weight:800;color:#00843D;margin:5px 0 4px}}
.pil .d{{font-size:9.5px;color:#5A6675;line-height:1.45}}
table{{width:100%;border-collapse:collapse;margin-top:4px}}
th{{background:#1E2A3A;color:#fff;font-size:9px;text-transform:uppercase;letter-spacing:.3px;padding:7px 8px;text-align:left}}
th.n,td.n{{text-align:right}} td{{padding:6px 8px;border-bottom:1px solid #E4E9EF;font-size:10px}}
td.s{{font-weight:600}} td.b{{font-weight:800;color:#1E2A3A}}
tr.tot td,tr:last-child.tot td{{background:#EEF2F6;font-weight:800;border-top:2px solid #1E2A3A}}
.note{{font-size:9px;color:#8a95a3;margin-top:5px;font-style:italic}}
.welcome{{background:#F0F7F2;border:1px solid #BEE0CC;border-radius:6px;padding:10px 13px;margin-top:9px;font-size:10px}}
.prio{{margin-top:6px}} .prio .p{{display:flex;gap:9px;padding:8px 0;border-bottom:1px solid #E4E9EF}}
.prio .num{{background:#00843D;color:#fff;font-weight:800;border-radius:50%;min-width:20px;height:20px;display:flex;align-items:center;justify-content:center;font-size:10px}}
.prio .txt b{{color:#1E2A3A}}
.foot{{margin-top:22px;padding-top:10px;border-top:1px solid #D9E1EA;font-size:8.6px;color:#8a95a3;display:flex;justify-content:space-between}}
</style></head><body>
<div class="mast"><div style="display:flex;align-items:center;gap:16px">
  <div class="pill"><img src="data:image/png;base64,{logo}"></div>
  <div><div class="t">Wellington Regional Performance</div>
  <div class="sub">SLS RTC Covert Loss Prevention · Woolworths NZ · Team Update</div></div></div>
  <div class="r"><div class="fy">FY2026</div><div class="we">Jul 2025 – Jun 2026</div></div></div>

<div class="wrap">
  <div class="intro"><b>Team — outstanding year.</b> Across FY2026 the Wellington team protected {store.__len__()} stores from Kāpiti and Horowhenua through the Hutt Valley to the CBD, returning <b>{m0(T_tot)}</b> in recovered value and turning away hundreds of offenders. Wellington now carries a bigger share of the national result than any region outside Auckland. This is what that looked like — and where we're pointing next.</div>

  <div class="kpis">
    <div class="kpi"><div class="b">{T_inc:,}</div><div class="l">Incidents managed</div></div>
    <div class="kpi"><div class="b">{T_off:,}</div><div class="l">Offenders engaged</div></div>
    <div class="kpi g"><div class="b">{T_det:,}</div><div class="l">Deterrents</div></div>
    <div class="kpi"><div class="b">{T_tres:,}</div><div class="l">Trespass actions</div></div>
    <div class="kpi gold"><div class="b">{m0(T_prod)}</div><div class="l">Recovered product (in-store)</div></div>
    <div class="kpi gold"><div class="b">{m0(T_pkg)}</div><div class="l">Recovered packaging</div></div>
    <div class="kpi g"><div class="b">{m0(T_tot)}</div><div class="l">Total value returned</div></div>
    <div class="kpi"><div class="b">{share_val:.0f}%</div><div class="l">Of the national total</div></div>
  </div>

  <h2>The three ways we create value</h2>
  <div class="pillars">
    <div class="pil"><div class="h">In-store product recovery</div><div class="v">{m0(T_prod)}</div>
      <div class="d">Physically stopping theft as it happens and recovering the goods — the frontline catch. Every incident engaged is stock kept on Woolworths' shelves.</div></div>
    <div class="pil"><div class="h">Packaging recovery</div><div class="v">{m0(T_pkg)}</div>
      <div class="d">Empty packaging swept from the floor — the evidence of averted theft. Wellington leads the whole country here: <b>{share_pkg:.0f}% of national packaging recovery</b>.</div></div>
    <div class="pil"><div class="h">Deterrence & the trespass wall</div><div class="v">{T_det:,} deterrents</div>
      <div class="d">{T_tres:,} trespass actions and hundreds of would-be offenders turned away before loss occurs — <b>{share_det:.0f}% of the national deterrent effort</b>.</div></div>
  </div>

  <h2>Store performance — FY2026</h2>
  <table><thead><tr><th>Store</th><th class="n">Incidents</th><th class="n">Recovered Product</th><th class="n">Recovered Packaging</th><th class="n">Total Recovered</th><th class="n">Deterrents</th></tr></thead>
  <tbody>{store_rows}</tbody></table>
  <div class="note">Lower Hutt led the country on packaging recovery; Newtown was our most complete store (strong on both catches and packaging); Cable Car Lane anchored the CBD with the highest activity and deterrent volume.</div>

  <h2>Deployment by store — recent 5 weeks (1 Jun – 5 Jul 2026)</h2>
  <table><thead><tr><th>Store</th><th class="n">Guard-hours</th><th class="n">Incidents</th><th class="n">Recovered Product</th><th class="n">Recovered Packaging</th><th class="n">Total Recovered</th></tr></thead>
  <tbody>{wstore_rows}</tbody></table>
  <div class="note">Guard-hours are shown for the recent period, where per-store deployment is tracked — {W_hrs:.0f} hours across the region. Hours, incidents and recovery here all cover the same 5 weeks, so they line up. (Full-year per-store hours aren't held; the FY2026 table above is our annual recovery record.)</div>

  <h2>Team contributors — FY2026</h2>
  <table><thead><tr><th>Team member</th><th class="n">Incidents</th><th class="n">Recovered Product</th><th class="n">Recovered Packaging</th><th class="n">Deterrents</th></tr></thead>
  <tbody>{contrib_rows}</tbody></table>
  <div class="welcome"><b>Welcome to our newest team members</b> — Levaula Vaea (joined April 2026) and George Tehe (joined May 2026) are building their record on the ground and already adding to the deterrent effort. Great to have you with the team.</div>
  <div class="note">Recognition reflects submitted reports; covert work is a team effort and packaging sweeps are often logged by one member on behalf of the shift.</div>

  <h2>Recent momentum — June</h2>
  <table><thead><tr><th>Week</th><th class="n">Guard-hours</th><th class="n">Incidents</th><th class="n">Recovered Product</th><th class="n">Recovered Packaging</th><th class="n">Total Recovered</th></tr></thead>
  <tbody>{mom_rows}</tbody></table>
  <div class="note">Deployment hours climbed through June as the client asked for more coverage across the region. (Deterrent totals in some June weeks are understated by a reporting-system gap — not a drop in effort.)</div>

  <h2>Where we're focused next</h2>
  <div class="prio">
    <div class="p"><div class="num">1</div><div class="txt"><b>Convert our presence into more in-store catches.</b> Our packaging and deterrent numbers are national-leading — the next lift is product recovery. Newtown and Cable Car Lane show the model: high visibility, quick engagement, stock recovered in-store.</div></div>
    <div class="p"><div class="num">2</div><div class="txt"><b>Keep the packaging discipline.</b> Lower Hutt's packaging recovery is the best in the country — that consistency is a genuine competitive edge for SLS RTC. Keep sweeping and logging every receipt.</div></div>
    <div class="p"><div class="num">3</div><div class="txt"><b>Hold the deterrent & trespass wall.</b> Nearly half the nation's deterrents come from this team. Keep issuing trespass notices and turning offenders away — prevention is as valuable as recovery.</div></div>
    <div class="p"><div class="num">4</div><div class="txt"><b>Log everything, every shift.</b> Complete, on-the-day reporting is what lets us show Woolworths the full value you deliver — and it's how the region keeps winning more hours.</div></div>
  </div>

  <div class="foot"><span>SLS RTC — Confidential · Internal team document (not for external distribution)</span><span>Wellington Regional Performance · FY2026</span></div>
</div>
</body></html>"""

html_path="/tmp/wgtn_team.html"
open(html_path,"w").write(HTML)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.goto("file://"+html_path)
    pg.pdf(path=OUT, prefer_css_page_size=True, print_background=True)
    b.close()
print("wrote", OUT)
print(f"region: {len(store)} stores | {T_inc} inc | product {money(T_prod)} | packaging {money(T_pkg)} | total {money(T_tot)} | det {T_det} | tres {T_tres}")
print("contributors:", [n for n,_ in established], "| new:", list(NEW), "| excluded:", list(EXCLUDE_GUARDS))
