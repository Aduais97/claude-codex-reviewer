#!/usr/bin/env python3
"""Bunnings National Risk Overview — data + metrics layer (windowed).
Reads the persisted master GIR (already merged to latest), optionally merges a fresh GIR window,
filters incidents AND deployed hours to a reporting window, and emits nro_metrics_<tag>.json.
Hours: truth.db timeclock_shifts (Bunnings) to 23 Jun 2026 + SLS Payrun unified timesheets from
24 Jun on — combined per-shift so any window gets its own hours. Client-safe (no recovery-per-hour).

Usage: python3 nro_metrics.py <WINDOW> [fresh_GIR_window.xlsx]
  WINDOW = FULL | FY26 | JUL2026
"""
import openpyxl, os, sys, re, json, glob, sqlite3, datetime
from datetime import date, timedelta
from collections import defaultdict, Counter

MASTER=os.path.expanduser("~/Desktop/SLS-RTC/Operations/Analytics/data/latest/gir-bunnings.xlsx")
TRUTHDB=os.path.expanduser("~/Desktop/Dev/asg-ops-hub/data/truth.db")
HERE=os.path.dirname(os.path.abspath(__file__))
ID,AUROR,IDATE,ITIME,REGION,SITE,SEV,RECTYPE,REC,STOLEN,NOTIFY=0,5,6,7,8,9,11,13,14,15,16
CO_SIG,SUP_SIG,DM_SIG,SM_SIG,GUARD_SIG=18,20,22,24,25
REGION_CANON={"hamilton":"Waikato","te rapa":"Waikato","dunedin":"Otago"}

WINDOWS={
 "FULL":   (None,None,"FULL","BUNNINGS NEW ZEALAND","Full programme history",
            "the full programme","full"),
 "FY26":   (date(2025,7,1),date(2026,6,30),"FY26","FY26 · FULL-YEAR REVIEW","1 July 2025 – 30 June 2026",
            "FY26 (1 Jul 2025 – 30 Jun 2026)","FY26"),
 "JUL2026":(date(2026,7,1),date(2026,7,31),"JUL2026","MONTH IN REVIEW","1 – 31 July 2026",
            "July 2026","Jul2026"),
}
WKEY=sys.argv[1].upper() if len(sys.argv)>1 else "FULL"
FROM,TO,TAG,KICKER,PERIOD_LABEL,PHRASE,FOOT=WINDOWS[WKEY]
FRESH=sys.argv[2] if len(sys.argv)>2 else None

def num(v):
    if v in (None,""): return 0.0
    try: return float(str(v).replace(",","").replace("$","").strip())
    except: return 0.0
def pdate(v):
    if isinstance(v,datetime.datetime): return v.date()
    if v in (None,""): return None
    s=str(v).strip()[:10]
    for f in ("%Y-%m-%d","%d/%m/%Y","%m/%d/%Y","%d/%m/%y"):
        try: return datetime.datetime.strptime(s,f).date()
        except: pass
    return None
def sev(v):
    m=re.search(r"[1-5]",str(v or "")); return int(m.group()) if m else None
def canon_region(v):
    s=str(v or "").strip(); return REGION_CANON.get(s.lower(), s or "Unspecified")
def hastext(v): return 1 if str(v or "").strip() else 0
def load(path):
    wb=openpyxl.load_workbook(path, read_only=True, data_only=True); ws=wb.active
    rows=list(ws.iter_rows(values_only=True)); wb.close()
    out={}
    for r in rows[1:]:
        if isinstance(r[ID],(int,float)): out[int(r[ID])]=r
    return rows[0],out

hdr,master=load(MASTER)
if FRESH:
    _,win=load(os.path.expanduser(FRESH)); master.update(win)
    wb=openpyxl.Workbook(); ws=wb.active; ws.append(list(hdr))
    for k in sorted(master): ws.append(list(master[k]))
    wb.save(MASTER); print(f"merged fresh window -> master now {len(master)} rows")

# ---- filter incidents to window ----
def inwin(d): return d is not None and (FROM is None or d>=FROM) and (TO is None or d<=TO)
R=[r for r in master.values() if inwin(pdate(r[IDATE]))]
if not R: sys.exit(f"no incidents in window {WKEY}")

# ---- combined per-shift Bunnings hours (truth.db <=23 Jun + payrun >=24 Jun) ----
def t2m(v):
    if v is None: return None
    if isinstance(v,datetime.time): return v.hour*60+v.minute
    s=str(v).strip()
    try: p=s.split(":"); return int(p[0])*60+int(p[1])
    except: return None
shift_hours=[]  # (date, hours)
try:
    con=sqlite3.connect(TRUTHDB); cur=con.cursor()
    cur.execute("SELECT shift_date,hours FROM timeclock_shifts WHERE lower(coalesce(store,client,'')) LIKE '%unning%'")
    for sd,hh in cur.fetchall():
        d=pdate(sd)
        if d and d<=date(2026,6,23) and hh: shift_hours.append((d,float(hh)))
    con.close()
except Exception as e: print("truth.db hours err:",e)
_seen={}   # dedup payrun files by period (avoids (1)/(2) variants counting twice)
for f in glob.glob(os.path.expanduser("~/Downloads/unified_time_sheet_report_2026-0*.xlsx")):
    m=re.search(r'(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})',os.path.basename(f))
    if not m or m.group(1)<"2026-06-24": continue
    _seen.setdefault(m.group(0),(f,pdate(m.group(1)),pdate(m.group(2))))
for per,(f,ps,pe) in _seen.items():
    wb=openpyxl.load_workbook(f, read_only=True, data_only=True); ws=wb.active
    rows=list(ws.iter_rows(values_only=True)); h=[str(x or "").strip().lower() for x in rows[0]]
    if not all(c in h for c in ("type","in","out","start date")): wb.close(); continue
    ti,ii,oi,sdi=h.index("type"),h.index("in"),h.index("out"),h.index("start date")
    for rr in rows[1:]:
        if "bunning" not in str(rr[ti] or "").lower(): continue
        d=pdate(rr[sdi]); im,om=t2m(rr[ii]),t2m(rr[oi])
        if not (d and ps<=d<=pe): continue          # count each shift only in its own week's file
        if im is not None and om is not None and om>im: shift_hours.append((d,(om-im)/60))
    wb.close()
win_hours=round(sum(hh for d,hh in shift_hours if inwin(d)),1)

# ---- metrics ----
dts=[pdate(r[IDATE]) for r in R]; dts=[d for d in dts if d]; lo,hi=min(dts),max(dts)
n=len(R)
sites=sorted({str(r[SITE]).strip() for r in R if str(r[SITE] or '').strip()})
regions=sorted({canon_region(r[REGION]) for r in R})
rec=sum(num(r[REC]) for r in R); stolen=sum(num(r[STOLEN]) for r in R); identified=rec+stolen
sevc=Counter(s for s in (sev(r[SEV]) for r in R) if s)
sev3plus=sum(v for k,v in sevc.items() if k>=3); sev45=sum(v for k,v in sevc.items() if k>=4)
auror=sum(hastext(r[AUROR]) for r in R)
def thour(v):
    m=re.match(r"\s*(\d{1,2}):(\d{2})",str(v or "")); return int(m.group(1)) if m else None
timed=[(pdate(r[IDATE]),thour(r[ITIME])) for r in R]; timed=[(d,h) for d,h in timed if d and h is not None]
in_window=sum(1 for d,h in timed if 12<=h<18)
dow=Counter(d.strftime("%A") for d,h in timed); cell=Counter((d.strftime("%A"),h) for d,h in timed)
hot=cell.most_common(1)[0] if cell else None
store_rec=defaultdict(float); store_inc=Counter(); store_sev3=Counter(); heat=defaultdict(int)
for r in R:
    s=str(r[SITE] or '').strip(); d=pdate(r[IDATE]); h=thour(r[ITIME])
    if s: store_rec[s]+=num(r[REC]); store_inc[s]+=1
    if s and (sev(r[SEV]) or 0)>=3: store_sev3[s]+=1
    if d and h is not None: heat[(d.weekday(),h)]+=1
top6=sorted(store_rec.items(),key=lambda x:-x[1])[:6]; top6_share=sum(v for _,v in top6)/rec*100 if rec else 0
reg_rec=defaultdict(float); reg_inc=Counter()
for r in R: rg=canon_region(r[REGION]); reg_rec[rg]+=num(r[REC]); reg_inc[rg]+=1
signoff={"Guard":sum(hastext(r[GUARD_SIG]) for r in R)/n*100,"Duty Manager":sum(hastext(r[DM_SIG]) for r in R)/n*100,
 "Checkout Operator":sum(hastext(r[CO_SIG]) for r in R)/n*100,"Supervisor":sum(hastext(r[SUP_SIG]) for r in R)/n*100,
 "Store Manager":sum(hastext(r[SM_SIG]) for r in R)/n*100}
# adaptive trend
span=(hi-lo).days
if span>75:
    tunit="month"; keyf=lambda d:d.strftime("%Y-%m"); labf=lambda k:datetime.datetime.strptime(k,"%Y-%m").strftime("%b %y")
else:
    tunit="week"; keyf=lambda d:(d-timedelta(days=d.weekday())).strftime("%Y-%m-%d"); labf=lambda k:datetime.datetime.strptime(k,"%Y-%m-%d").strftime("%d %b")
tinc=Counter(); trec=defaultdict(float)
for r in R:
    d=pdate(r[IDATE])
    if d: k=keyf(d); tinc[k]+=1; trec[k]+=num(r[REC])
trend=[{"key":k,"label":labf(k),"incidents":tinc[k],"recovered":round(trec[k],2)} for k in sorted(tinc)]

M={"tag":TAG,"kicker":KICKER,"period_label":PERIOD_LABEL,"phrase":PHRASE,"foot":FOOT,
 "date_lo":str(lo),"date_hi":str(hi),"incidents":n,"sites":len(sites),"regions":len(regions),
 "recovered":round(rec,2),"stolen":round(stolen,2),"identified":round(identified,2),
 "recovery_pct":round(rec/identified*100,1) if identified else 0,"auror_pct":round(auror/n*100,1),
 "severity":{str(k):sevc.get(k,0) for k in range(1,6)},"sev3plus":sev3plus,"sev45":sev45,
 "risk_window_pct":round(in_window/len(timed)*100,1) if timed else 0,
 "peak_day":dow.most_common(1)[0] if dow else None,
 "hottest_cell":{"day":hot[0][0],"hour":hot[0][1],"count":hot[1]} if hot else None,
 "heat":{f"{d}_{h}":c for (d,h),c in heat.items()},
 "top6":[{"store":s,"recovered":round(v,2),"share":round(v/rec*100,1),"incidents":store_inc[s],"sev3":store_sev3[s]} for s,v in top6],
 "top6_share":round(top6_share,1),
 "regional":sorted([{"region":k,"recovered":round(v,2),"incidents":reg_inc[k]} for k,v in reg_rec.items()],key=lambda x:-x["recovered"]),
 "signoff":{k:round(v,1) for k,v in signoff.items()},
 "serious_hotspots":sorted([{"store":s,"sev3":c} for s,c in store_sev3.items()],key=lambda x:-x["sev3"])[:5],
 "trend":trend,"trend_unit":tunit,
 "hours_window":win_hours,"inc_per_100h":round(n/win_hours*100,2) if win_hours else 0,
 "hours_per_inc":round(win_hours/n,1) if n else 0,
}
outp=os.path.join(HERE,f"nro_metrics_{TAG}.json"); json.dump(M,open(outp,"w"),indent=1,default=str)
print(f"[{WKEY}] {PERIOD_LABEL}: {n} inc | ${rec:,.0f} rec / {M['recovery_pct']}% | sev3+ {sev3plus} | top6 {top6_share:.1f}% "
      f"| hours {win_hours:,.0f}h -> {M['inc_per_100h']} inc/100h | {lo}..{hi}")
print(f"  wrote {outp}")
