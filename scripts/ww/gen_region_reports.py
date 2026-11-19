#!/usr/bin/env python3
"""SLS RTC — Regional Team Performance Reports (INTERNAL, one branded PDF per region).
Auckland / Wellington / Canterbury / Waikato. Recognition-led + STORE-LEVEL ROI:
hours per store, ROI measured PRIMARILY by incidents-per-100-guard-hours (activity/detection),
with recovery-$ per hour secondary. Recovery split Product (in-store) vs Packaging.
No individual $/hr. Zac Shannon excluded from contributor recognition (per instruction)."""
import os, re, base64, datetime, sys
from collections import defaultdict
import openpyxl
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_master_v2 as bm

DL = os.path.expanduser("~/Downloads/")
GIR_FY = DL+"Woolworths _ Guard Incident Report_c825cc65-4f04-47bf-b60c-57e23f7026ea.xlsx"
PKG_FY = DL+"Woolworths _ Recovered Packaging_a42b0810-42bc-430e-83c4-02017db4c98b.xlsx"
DET_FY = DL+"Woolworths _ Guard Deterent  Report_a53b9b34-b6b2-45aa-ab48-04a7ada46008.xlsx"
GIR_W1 = DL+"Woolworths _ Guard Incident Report_3f88efe3-fcd2-46e8-b223-101972193adf.xlsx"
PKG_W1 = DL+"Woolworths _ Recovered Packaging_3641b511-7e80-4e7a-8b1f-d0e686b8dab8.xlsx"
SCHED  = DL+"Schedule-Export 2026-06-01 to 2026-07-05 (1).xlsx"
LOGO   = os.path.expanduser("~/Desktop/SLS-RTC/Operations/Analytics/assets/slsrtc_logo_hd.png")
OUTDIR = os.path.expanduser("~/Desktop/Woolworths /Regional Team Reports")
os.makedirs(OUTDIR, exist_ok=True)

EXCLUDE_CONTRIB = {"Zac Shannon"}                    # keep out of recognition tables (still counts to store totals)
MGMT = {"Ahmad Duais","Blake Zuill","Graham Zuill","Hasi Nabawi","Mark Clansey","Nikki Christian","Sydney Eady"}
WGTN_TEAM = {"levin","paraparaumu","flaxmere"}       # team-run even if source-tagged Manawatū/Kāpiti/HB
NEW_STARTERS = {"Levaula Vaea":"April 2026","George Tehe":"May 2026"}
DEPARTED = {"Greig Singer","Melvin Yamben","James Olsen"}
REGIONS = ["Auckland","Wellington","Canterbury","Waikato"]
SUBTITLE = {"Auckland":"Tāmaki Makaurau","Wellington":"Te Whanganui-a-Tara & Lower North Island",
            "Canterbury":"Waitaha","Waikato":"Waikato"}

FY0,FY1 = datetime.date(2025,7,1), datetime.date(2026,6,30)
WS,WE   = datetime.date(2026,6,1), datetime.date(2026,7,5)     # matched hours window

def m0(v): return f"${v:,.0f}"
def clean_full(s):
    s=" ".join(str(s).split()).strip()
    s=bm.STORE_NAME_FIXES.get(s.lower(), s)
    s=re.sub(r"\bMount\b","Mt",s); s=re.sub(r"\bPt Chevalier\b","Pt Chev",s)
    return s
def short(s): return re.sub(r"\s+"," ",re.sub(r"\bWoolworths\b","",clean_full(s),flags=re.I)).strip()
def to_f(v):
    try: return float(v) if isinstance(v,(int,float)) else float(str(v).replace("$","").replace(",","").strip() or 0)
    except: return 0.0
def pdate(v):
    if isinstance(v,datetime.datetime): return v.date()
    if isinstance(v,datetime.date): return v
    for f in ("%Y-%m-%d","%m/%d/%Y","%d/%m/%Y"):
        try: return datetime.datetime.strptime(str(v).split(" ")[0],f).date()
        except: pass
    return None
def cols(hdr,names):
    low=[str(h).strip().lower() if h else "" for h in hdr]; out={}
    for k,n in names.items():
        nl=n.lower(); i=next((j for j,h in enumerate(low) if h==nl),None)
        if i is None: i=next((j for j,h in enumerate(low) if nl in h),None)
        out[k]=i
    return out
def rows(f):
    ws=openpyxl.load_workbook(f,read_only=True,data_only=True).active
    it=ws.iter_rows(values_only=True); hdr=list(next(it)); return hdr,[list(r) for r in it]

# ---- pass 1: region votes per store (from GIR region-of-site field) ----
votes=defaultdict(lambda:defaultdict(int))
def vote(f):
    hdr,rs=rows(f); c=cols(hdr,{'site':'Select Woolworths Site','reg':'Region of site'})
    for r in rs:
        st=r[c['site']] if c['site'] is not None else None
        if not st: continue
        raw=str(r[c['reg']] or '').strip() if c['reg'] is not None else ''
        votes[short(st)][raw]+=1
vote(GIR_FY); vote(DET_FY); vote(GIR_W1)
def region_of(sh):
    if sh.lower() in WGTN_TEAM: return "Wellington"
    if not votes[sh]: return "Other"
    raw=max(votes[sh].items(), key=lambda x:x[1])[0]
    return bm.STORE_REGION_OVERRIDE.get((sh+" woolworths").lower(), bm.REGION_SHORT.get(raw,"Other"))

# ---- pass 2: FY26 per store + per guard ----
store=defaultdict(lambda:dict(inc=0,off=0,prod=0.0,pkg=0.0,det=0,tres=0,reg=None))
guard=defaultdict(lambda:dict(inc=0,prod=0.0,pkg=0.0,det=0,regcnt=defaultdict(int)))
def acc_store(sh,**kw):
    d=store[sh]; d['reg']=region_of(sh)
    for k,v in kw.items(): d[k]+=v
def gir(f,s,e):
    hdr,rs=rows(f); c=cols(hdr,{'d':'Date and Time of Incident - Date','site':'Select Woolworths Site',
        'rec':'Recovered Reciept Value','cat':'Incident Category','name':'Full name','off':'Number of offenders/POI',
        'vt':'Verbal Trespass','ft':'Formal Trespass Notice Served'})
    for r in rs:
        st=r[c['site']] if c['site'] is not None else None
        if not st: continue
        d=pdate(r[c['d']])
        if not d or d<s or d>e: continue
        sh=short(st); nm=str(r[c['name']] or '').strip(); cat=str(r[c['cat']] or '')
        vt=1 if str(r[c['vt']] or '').strip().lower()=='yes' else 0
        ft=1 if str(r[c['ft']] or '').strip().lower()=='yes' else 0
        rec=to_f(r[c['rec']])
        if 'Deterrent' in cat:
            acc_store(sh,det=1,prod=rec,tres=vt+ft); guard[nm]['det']+=1
        else:
            o=r[c['off']]; off=int(o) if isinstance(o,(int,float)) and o else 1
            acc_store(sh,inc=1,off=off,prod=rec,tres=vt+ft); guard[nm]['inc']+=1
        guard[nm]['prod']+=rec; guard[nm]['regcnt'][region_of(sh)]+=1
def pkg(f,s,e):
    hdr,rs=rows(f); c=cols(hdr,{'d':'Date and Time - Date','site':'Select Woolworths Site','val':'Receipt Value','name':'Full name'})
    for r in rs:
        st=r[c['site']] if c['site'] is not None else None
        if not st: continue
        d=pdate(r[c['d']])
        if not d or d<s or d>e: continue
        sh=short(st); nm=str(r[c['name']] or '').strip(); v=to_f(r[c['val']])
        acc_store(sh,pkg=v); guard[nm]['pkg']+=v; guard[nm]['regcnt'][region_of(sh)]+=1
def det(f,s,e):
    hdr,rs=rows(f); c=cols(hdr,{'d':'Date and Time of Incident - Date','site':'Select Woolworths Site',
        'name':'Full name','vt':'Verbal Trespass','ft':'Formal Trespass Notice Served'})
    for r in rs:
        st=r[c['site']] if c['site'] is not None else None
        if not st: continue
        d=pdate(r[c['d']]) or pdate(r[2])
        if not d or d<s or d>e: continue
        sh=short(st); nm=str(r[c['name']] or '').strip()
        vt=1 if str(r[c['vt']] or '').strip().lower()=='yes' else 0
        ft=1 if str(r[c['ft']] or '').strip().lower()=='yes' else 0
        acc_store(sh,det=1,tres=vt+ft); guard[nm]['det']+=1; guard[nm]['regcnt'][region_of(sh)]+=1
gir(GIR_FY,FY0,FY1); pkg(PKG_FY,FY0,FY1); det(DET_FY,FY0,FY1)

# ---- pass 3: recent-window per store (hours + matched activity) ----
wstore=defaultdict(lambda:dict(hrs=0.0,inc=0,prod=0.0,pkg=0.0,reg=None))
def wgir(f):
    hdr,rs=rows(f); c=cols(hdr,{'d':'Date and Time of Incident - Date','site':'Select Woolworths Site','rec':'Recovered Reciept Value','cat':'Incident Category'})
    for r in rs:
        st=r[c['site']] if c['site'] is not None else None
        if not st: continue
        d=pdate(r[c['d']])
        if not d or d<WS or d>WE: continue
        sh=short(st); wstore[sh]['reg']=region_of(sh)
        if 'Deterrent' not in str(r[c['cat']] or ''): wstore[sh]['inc']+=1
        wstore[sh]['prod']+=to_f(r[c['rec']])
def wpkg(f):
    hdr,rs=rows(f); c=cols(hdr,{'d':'Date and Time - Date','site':'Select Woolworths Site','val':'Receipt Value'})
    for r in rs:
        st=r[c['site']] if c['site'] is not None else None
        if not st: continue
        d=pdate(r[c['d']])
        if not d or d<WS or d>WE: continue
        sh=short(st); wstore[sh]['reg']=region_of(sh); wstore[sh]['pkg']+=to_f(r[c['val']])
wgir(GIR_FY); wgir(GIR_W1); wpkg(PKG_FY); wpkg(PKG_W1)
# hours per store
hdr,rs=rows(SCHED); c=cols(hdr,{'d':'Date','st':'Start','en':'End','job':'Job'})
def _hh(a,b):
    def m(x):
        try: h,mm=str(x).split(':'); return int(h)*60+int(mm)
        except: return None
    A,B=m(a),m(b); return (B-A)/60.0 if A is not None and B is not None and B>=A else 0.0
for r in rs:
    job=r[c['job']] if c['job'] is not None else None
    if not job or 'travel' in str(job).lower() or 'head office' in str(job).lower(): continue
    d=pdate(r[c['d']])
    if not d or d<WS or d>WE: continue
    sh=short(job)
    if not votes.get(sh): continue                       # only real WW stores
    wstore[sh]['reg']=region_of(sh); wstore[sh]['hrs']+=_hh(r[c['st']],r[c['en']])

# per-week momentum per region
D=datetime.date
WEEKS=[("W/E 7 Jun",D(2026,6,1),D(2026,6,7)),("W/E 14 Jun",D(2026,6,8),D(2026,6,14)),
       ("W/E 21 Jun",D(2026,6,15),D(2026,6,21)),("W/E 28 Jun",D(2026,6,22),D(2026,6,28))]
def week_region(reg,s,e):
    inc=0;prod=0.0;pkgv=0.0;hrs=0.0
    hdr,rs=rows(GIR_FY); c=cols(hdr,{'d':'Date and Time of Incident - Date','site':'Select Woolworths Site','rec':'Recovered Reciept Value','cat':'Incident Category'})
    for r in rs:
        st=r[c['site']] if c['site'] is not None else None
        if not st or region_of(short(st))!=reg: continue
        d=pdate(r[c['d']])
        if not d or d<s or d>e: continue
        if 'Deterrent' not in str(r[c['cat']] or ''): inc+=1
        prod+=to_f(r[c['rec']])
    hdr,rs=rows(PKG_FY); c=cols(hdr,{'d':'Date and Time - Date','site':'Select Woolworths Site','val':'Receipt Value'})
    for r in rs:
        st=r[c['site']] if c['site'] is not None else None
        if not st or region_of(short(st))!=reg: continue
        d=pdate(r[c['d']])
        if not d or d<s or d>e: continue
        pkgv+=to_f(r[c['val']])
    hdr,rs=rows(SCHED); c=cols(hdr,{'d':'Date','st':'Start','en':'End','job':'Job'})
    for r in rs:
        job=r[c['job']] if c['job'] is not None else None
        if not job or 'travel' in str(job).lower() or 'head office' in str(job).lower() or not votes.get(short(job)): continue
        if region_of(short(job))!=reg: continue
        d=pdate(r[c['d']])
        if not d or d<s or d>e: continue
        hrs+=_hh(r[c['st']],r[c['en']])
    return round(hrs),inc,prod,pkgv

# national totals for share
NAT=dict(prod=sum(d['prod'] for d in store.values()), pkg=sum(d['pkg'] for d in store.values()),
         det=sum(d['det'] for d in store.values()), inc=sum(d['inc'] for d in store.values()))
NAT['tot']=NAT['prod']+NAT['pkg']

logo=base64.b64encode(open(LOGO,'rb').read()).decode()

def region_report(reg):
    sstores={s:d for s,d in store.items() if d['reg']==reg}
    if not sstores: return None
    T=dict(inc=sum(d['inc'] for d in sstores.values()),off=sum(d['off'] for d in sstores.values()),
           prod=sum(d['prod'] for d in sstores.values()),pkg=sum(d['pkg'] for d in sstores.values()),
           det=sum(d['det'] for d in sstores.values()),tres=sum(d['tres'] for d in sstores.values()))
    T['tot']=T['prod']+T['pkg']
    sh_val=100*T['tot']/NAT['tot'] if NAT['tot'] else 0
    sh_det=100*T['det']/NAT['det'] if NAT['det'] else 0
    # FY26 store rows
    srows=""
    for s,d in sorted(sstores.items(), key=lambda x:-(x[1]['prod']+x[1]['pkg'])):
        srows+=(f"<tr><td class='s'>{s}</td><td class='n'>{d['inc']}</td><td class='n'>{m0(d['prod'])}</td>"
                f"<td class='n'>{m0(d['pkg'])}</td><td class='n b'>{m0(d['prod']+d['pkg'])}</td><td class='n'>{d['det']}</td></tr>")
    srows+=(f"<tr class='tot'><td class='s'>{reg} total</td><td class='n'>{T['inc']}</td><td class='n'>{m0(T['prod'])}</td>"
            f"<td class='n'>{m0(T['pkg'])}</td><td class='n b'>{m0(T['tot'])}</td><td class='n'>{T['det']}</td></tr>")
    # ROI table (recent window): hours, incidents, incidents/100h (PRIMARY ROI), product, packaging, $/hr
    wst={s:d for s,d in wstore.items() if d['reg']==reg and (d['hrs']>0 or d['inc']>0 or d['prod']+d['pkg']>0)}
    Wh=sum(d['hrs'] for d in wst.values()); Wi=sum(d['inc'] for d in wst.values())
    Wp=sum(d['prod'] for d in wst.values()); Wk=sum(d['pkg'] for d in wst.values())
    rrows=""
    for s,d in sorted(wst.items(), key=lambda x:-(x[1]['inc']/x[1]['hrs'] if x[1]['hrs'] else 0)):
        hr=d['hrs']; i100=(d['inc']/hr*100) if hr else 0; dph=((d['prod']+d['pkg'])/hr) if hr else 0
        rrows+=(f"<tr><td class='s'>{s}</td><td class='n'>{hr:.0f}</td><td class='n'>{d['inc']}</td>"
                f"<td class='n roi'>{i100:.1f}</td><td class='n'>{m0(d['prod'])}</td><td class='n'>{m0(d['pkg'])}</td>"
                f"<td class='n'>${dph:.0f}</td></tr>")
    Ri100=(Wi/Wh*100) if Wh else 0; Rdph=((Wp+Wk)/Wh) if Wh else 0
    rrows+=(f"<tr class='tot'><td class='s'>{reg} total</td><td class='n'>{Wh:.0f}</td><td class='n'>{Wi}</td>"
            f"<td class='n roi'>{Ri100:.1f}</td><td class='n'>{m0(Wp)}</td><td class='n'>{m0(Wk)}</td><td class='n'>${Rdph:.0f}</td></tr>")
    # contributors: guards whose majority events are in this region
    conts=[]
    for n,d in guard.items():
        if n in MGMT or n in EXCLUDE_CONTRIB or n in DEPARTED or n in NEW_STARTERS or not n: continue
        if not d['regcnt']: continue
        home=max(d['regcnt'].items(),key=lambda x:x[1])[0]
        if home!=reg: continue
        if d['prod']+d['pkg']==0 and d['inc']==0: continue
        conts.append((n,d))
    conts.sort(key=lambda x:-(x[1]['prod']+x[1]['pkg']))
    crows=""
    for n,d in conts[:12]:
        crows+=(f"<tr><td class='s'>{n}</td><td class='n'>{d['inc']}</td><td class='n'>{m0(d['prod'])}</td>"
                f"<td class='n'>{m0(d['pkg'])}</td><td class='n'>{d['det']}</td></tr>")
    new_here=[nm for nm in NEW_STARTERS if guard.get(nm) and guard[nm]['regcnt'] and max(guard[nm]['regcnt'].items(),key=lambda x:x[1])[0]==reg]
    welcome = (f"<div class='welcome'><b>Welcome to our newest team members</b> — "
               + " and ".join(f"{nm} (joined {NEW_STARTERS[nm]})" for nm in new_here)
               + " are building their record on the ground. Great to have you with the team.</div>") if new_here else ""
    # momentum
    mrows=""
    for lbl,s,e in WEEKS:
        h,i,p,k=week_region(reg,s,e)
        mrows+=(f"<tr><td class='s'>{lbl}</td><td class='n'>{h}</td><td class='n'>{i}</td>"
                f"<td class='n'>{m0(p)}</td><td class='n'>{m0(k)}</td><td class='n b'>{m0(p+k)}</td></tr>")

    HTML=f"""<!doctype html><html><head><meta charset=utf-8><style>
@page{{size:A4;margin:0}} *{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:Arial,Helvetica,sans-serif;color:#1F2733;font-size:10.5px;line-height:1.5}}
.wrap{{padding:24px 34px 30px}}
.mast{{background:#1E2A3A;color:#fff;padding:18px 34px;display:flex;align-items:center;justify-content:space-between}}
.mast .pill{{background:#fff;border-radius:7px;padding:6px 11px}} .mast .pill img{{height:32px;display:block}}
.mast .t{{font-size:19px;font-weight:800}} .mast .sub{{font-size:10px;color:#AEBACb;margin-top:3px}}
.mast .fy{{font-size:12px;font-weight:700;color:#C8952A;text-align:right}} .mast .we{{font-size:9.5px;color:#AEBACb;text-align:right;margin-top:2px}}
h2{{color:#1E2A3A;font-size:13px;margin:18px 0 8px;padding-bottom:5px;border-bottom:2px solid #00843D}}
.intro{{background:#EEF2F6;border-left:4px solid #00843D;padding:11px 14px;border-radius:4px;margin-top:14px}}
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:13px}}
.kpi{{background:#fff;border:1px solid #D9E1EA;border-radius:7px;padding:10px 11px}}
.kpi .b{{font-size:18px;font-weight:800;color:#1E2A3A}} .kpi.g .b{{color:#00843D}} .kpi.gold .b{{color:#C8952A}}
.kpi .l{{font-size:8.4px;color:#5A6675;font-weight:700;text-transform:uppercase;letter-spacing:.3px;margin-top:3px;line-height:1.3}}
table{{width:100%;border-collapse:collapse;margin-top:4px}}
th{{background:#1E2A3A;color:#fff;font-size:8.6px;text-transform:uppercase;letter-spacing:.2px;padding:7px 7px;text-align:left}}
th.n,td.n{{text-align:right}} td{{padding:5.5px 7px;border-bottom:1px solid #E4E9EF;font-size:9.6px}}
td.s{{font-weight:600}} td.b{{font-weight:800;color:#1E2A3A}} td.roi{{font-weight:800;color:#00843D}}
th.roi{{color:#C8952A}} tr.tot td{{background:#EEF2F6;font-weight:800;border-top:2px solid #1E2A3A}}
.note{{font-size:8.6px;color:#8a95a3;margin-top:5px;font-style:italic}}
.welcome{{background:#F0F7F2;border:1px solid #BEE0CC;border-radius:6px;padding:9px 13px;margin-top:9px;font-size:9.6px}}
.foot{{margin-top:20px;padding-top:9px;border-top:1px solid #D9E1EA;font-size:8.4px;color:#8a95a3;display:flex;justify-content:space-between}}
</style></head><body>
<div class="mast"><div style="display:flex;align-items:center;gap:15px">
 <div class="pill"><img src="data:image/png;base64,{logo}"></div>
 <div><div class="t">{reg} Regional Performance</div><div class="sub">SLS RTC Covert Loss Prevention · Woolworths NZ · {SUBTITLE.get(reg,'')} · Team Update</div></div></div>
 <div><div class="fy">FY2026</div><div class="we">Jul 2025 – Jun 2026</div></div></div>
<div class="wrap">
 <div class="intro"><b>{reg} team — FY2026 in review.</b> Across the year the {reg} team worked {len(sstores)} stores, managing <b>{T['inc']:,} incidents</b> and returning <b>{m0(T['tot'])}</b> in recovered value ({sh_val:.0f}% of the national result), on top of {T['det']:,} deterrents and {T['tres']:,} trespass actions. Here's the store-by-store picture — and, crucially, the <b>return on our deployment hours</b>.</div>
 <div class="kpis">
  <div class="kpi"><div class="b">{T['inc']:,}</div><div class="l">Incidents managed</div></div>
  <div class="kpi"><div class="b">{T['off']:,}</div><div class="l">Offenders engaged</div></div>
  <div class="kpi g"><div class="b">{T['det']:,}</div><div class="l">Deterrents</div></div>
  <div class="kpi"><div class="b">{T['tres']:,}</div><div class="l">Trespass actions</div></div>
  <div class="kpi gold"><div class="b">{m0(T['prod'])}</div><div class="l">Recovered product (in-store)</div></div>
  <div class="kpi gold"><div class="b">{m0(T['pkg'])}</div><div class="l">Recovered packaging</div></div>
  <div class="kpi g"><div class="b">{m0(T['tot'])}</div><div class="l">Total value returned</div></div>
  <div class="kpi"><div class="b">{sh_val:.0f}%</div><div class="l">Of national recovery</div></div>
 </div>

 <h2>Store performance — FY2026</h2>
 <table><thead><tr><th>Store</th><th class="n">Incidents</th><th class="n">Recovered Product</th><th class="n">Recovered Packaging</th><th class="n">Total Recovered</th><th class="n">Deterrents</th></tr></thead><tbody>{srows}</tbody></table>

 <h2>Return on deployment — hours & ROI by store (recent 5 weeks, 1 Jun – 5 Jul 2026)</h2>
 <table><thead><tr><th>Store</th><th class="n">Guard-hours</th><th class="n">Incidents</th><th class="n roi">Incidents / 100h</th><th class="n">Recovered Product</th><th class="n">Recovered Packaging</th><th class="n">$ / hour</th></tr></thead><tbody>{rrows}</tbody></table>
 <div class="note">ROI is led by <b>incidents per 100 guard-hours</b> — the detection return on our deployment, not just dollars (recovery is lumpy and packaging-weighted). Hours, incidents and recovery all cover the same 5 weeks, so they line up. Full-year per-store hours aren't held; the FY2026 table above is the annual recovery record.</div>

 <h2>Team contributors — FY2026</h2>
 <table><thead><tr><th>Team member</th><th class="n">Incidents</th><th class="n">Recovered Product</th><th class="n">Recovered Packaging</th><th class="n">Deterrents</th></tr></thead><tbody>{crows}</tbody></table>
 {welcome}
 <div class="note">Recognition reflects submitted reports; covert work is a team effort and packaging sweeps are often logged by one member on behalf of the shift.</div>

 <h2>Recent momentum — June</h2>
 <table><thead><tr><th>Week</th><th class="n">Guard-hours</th><th class="n">Incidents</th><th class="n">Recovered Product</th><th class="n">Recovered Packaging</th><th class="n">Total Recovered</th></tr></thead><tbody>{mrows}</tbody></table>
 <div class="note">(Deterrent totals in some June weeks are understated by a reporting-system gap — not a drop in effort.)</div>

 <div class="foot"><span>SLS RTC — Confidential · Internal team document (not for external distribution)</span><span>{reg} Regional Performance · FY2026</span></div>
</div></body></html>"""
    hp=f"/tmp/region_{reg}.html"; open(hp,"w").write(HTML)
    out=f"{OUTDIR}/{reg} Team Performance Report - FY26.pdf"
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(); pg.goto("file://"+hp)
        pg.pdf(path=out, prefer_css_page_size=True, print_background=True); b.close()
    print(f"[{reg}] {len(sstores)} stores | {T['inc']} inc | prod {m0(T['prod'])} | pkg {m0(T['pkg'])} | tot {m0(T['tot'])} | {sh_val:.0f}% nat | window {Wh:.0f}h {Wi}inc ROI {Ri100:.1f}/100h | contrib {len(conts)} -> {out}")

for reg in REGIONS:
    region_report(reg)
print("national tot:", m0(NAT['tot']), "| stores mapped:", len(store))
# show any material stores landing in 'Other'
oth=[(s,round(d['prod']+d['pkg'])) for s,d in store.items() if d['reg']=='Other' and d['prod']+d['pkg']>500]
if oth: print("Other-region stores >$500 (not in any regional report):", sorted(oth,key=lambda x:-x[1])[:12])
