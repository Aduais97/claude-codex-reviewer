#!/usr/bin/env python3
"""FY27 Woolworths Deployment & Recovery Tracker (Weekly / Period / YTD + per-store).
Per Glenn (8 Jul): ACTUAL COST PER WEEK added (hours × agreed bill rate, ex-GST) so WW can
roll it into periods and track against budget. Cost + hours + recovery + full activity stats.
NO net / recovery:cost ratio (cost is tracked vs BUDGET, never divided by recovery).
Per-store cost is deliberately NOT shown (weekly/period cost only — Glenn's ask)."""
import os, sys, re, glob
from datetime import datetime, timedelta
from collections import defaultdict
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L

OUT = os.path.expanduser("~/Desktop/Woolworths /Woolworths FY27 Deployment & Recovery Tracker.xlsx")
NAVY="1E2A3A"; GREEN="00843D"; GOLD="C8952A"; LIGHT="EEF2F6"; REG="D9E1EA"; INPUT="FFF3CD"; WHITE="FFFFFF"; INK="1F2733"
thin=Side(style="thin", color="C9D2DC"); B=Border(left=thin,right=thin,top=thin,bottom=thin)
MON='#,##0.00'; INT='#,##0'; DT='dd mmm yyyy'
BILL_RATE=43.50   # agreed WW bill rate, ex-GST (~$43.50/hr) — cost = hours × this (adjustable in the C3 input cell)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_master_v2 as bm
def _mn(s):
    s=str(s).lower().replace("woolworths","").replace("countdown","")
    s=s.replace("mount","mt").replace("point","pt").replace("pt chevalier","pt chev")
    return re.sub(r"\s+"," ",re.sub(r"[^a-z0-9 ]"," ",s)).strip()
def _sched_pd(s):
    for fm in ("%m/%d/%Y","%d/%m/%Y","%Y-%m-%d"):
        try: return datetime.strptime(str(s).split(" ")[0],fm)
        except: pass
    return None
def _sched_hh(a,b):
    try:
        ah,am=map(int,str(a).split(":")); bh,bm2=map(int,str(b).split(":"))
        d=(bh*60+bm2)-(ah*60+am); return d/60 if d>0 else 0
    except: return 0
def _sched_rows():
    """Yield (date, job, hours) for every WW deployment shift across ALL weekly ACTUAL schedule
    files (each week may point to a different file — e.g. W1-W5 in one export, W6 in the next).
    Keeps the relabelled Wellington transit ('...Transit Woolworths') and drops any 'travel' job."""
    seen=set()
    for wk in bm.WEEKS:
        f=bm.schedule_for(wk)
        if f in seen: continue
        seen.add(f)
        wb=openpyxl.load_workbook(f, read_only=True); ws=wb.active
        it=ws.iter_rows(values_only=True); hd=list(next(it))
        di,si,ei,ji=hd.index("Date"),hd.index("Start"),hd.index("End"),hd.index("Job")
        for r in it:
            d=_sched_pd(r[di]); job=r[ji]
            if not d or not job: continue
            # A file only contributes rows for the FY week(s) IT serves. A shift whose clock-in
            # lands just outside the export window (e.g. a Sun-night shift stamped the next Mon)
            # otherwise leaks into the NEXT week's file window and double-counts.
            wof=bm.week_of(d)
            if wof is None or bm.schedule_for(wof)!=f: continue
            j=str(job).lower()
            if "woolworth" not in j or "travel" in j: continue
            yield d, job, _sched_hh(r[si],r[ei])
        wb.close()
def _store_hours(week):
    ws0=bm.week_start(week); H=defaultdict(float); disp={}
    for d,job,h in _sched_rows():
        if ws0<=d<=week:
            mn=_mn(job); H[mn]+=h; disp.setdefault(mn,str(job).strip())
    return H, disp
def _month_hours():
    """Deployed hours per CALENDAR MONTH (actual shift date), gated to dates inside a defined FY
    week so the monthly YTD ties to the Weekly Ledger. A month-straddling week is split by day."""
    M=defaultdict(float)
    for d,job,h in _sched_rows():
        if bm.week_of(d) is not None: M[d.strftime("%b %Y")]+=h
    return M

def _cumulative_tagsheet_hours():
    """FY-to-date hours per store from the authoritative full-period Connecteam tag-sheet.
    Some exports arrive as a single 1-Jul→week-end 'timeclock-tag-sheet' — hours AGGREGATED by
    store across the whole period, no per-shift dates. That can't drive the (dated) weekly ledger,
    but it IS the source of truth for FY-to-date CUMULATIVE store totals. Ahmad, 17 Aug 2026:
    weekly rows keep their dated per-week actuals; the cumulative Store Detail ties to this file.
    Reads the NEWEST '~/Downloads/timeclock-tag-sheet 2026-07-01 *.xlsx' (FY start). WW scope only
    (drops travel / Flaxmere / Hastings / leave). Returns {canonical_store: hours, '__total__': tot}
    or None if no such export is present (→ cumulative falls back to summed weekly hours)."""
    cands=sorted(glob.glob(os.path.expanduser("~/Downloads/timeclock-tag-sheet 2026-07-01 *.xlsx")))
    if not cands: return None
    ws=openpyxl.load_workbook(cands[-1], data_only=True).active
    H=defaultdict(float); tot=0.0; travel=0.0; disp={}
    for r in ws.iter_rows(min_row=2, values_only=True):
        job=r[0]
        if job in (None,""): continue          # guard sub-row — the store-header row carries the total
        jl=str(job).lower(); h=float(r[4] or 0)
        if "travel" in jl:                     # WW team transit (to/from WW sites) shown as its own line;
            if "sls" not in jl: travel+=h      # 'Travel (SLSRTC)' is SLS RTC's own travel — not WW-billable
            continue
        if "flaxmere" in jl or "hastings" in jl or "leave" in jl or "woolworth" not in jl: continue
        H[_mn(job)]+=h; tot+=h; disp.setdefault(_mn(job),str(job).strip())
    H["__total__"]=tot; H["__travel__"]=travel; H["__disp__"]=disp
    return dict(H)

_agg,_sreg,_regs=bm.aggregate()
def _weekdata(week):
    hrs,disp=_store_hours(week)
    active=[(s,a) for (w,s),a in _agg.items() if w==week]
    natw=bm.rollup([a for s,a in active])
    srows=defaultdict(list); matched=0.0; active_mn=set()
    for s,a in active:
        h=hrs.get(_mn(s),0.0); matched+=h; active_mn.add(_mn(s))
        srows[_sreg.get(s,"Other")].append({"store":s,"h":h,"dir":a["rec"],"pkg":a["pkg"],"lost":a["lost"],"inc":a["inc"],
            "off":a["off"],"det":a["det"],"det_ind":a["det_ind"],"tres":a["vtres"]+a["ftres"],"pkgc":a["pkgc"]})
    # Deployed stores with hours but NO incident/recovery logged → their own "covered, no incidents"
    # rows (not a mystery residual). Team transit → its own travel line.
    transit=0.0
    for mn,h in hrs.items():
        if mn in active_mn: continue
        if "transit" in mn or "travel" in mn: transit+=h; continue
        name=disp.get(mn,mn); reg=bm.STORE_REGION_OVERRIDE.get(name.lower(),"Other")
        srows[reg].append({"store":name,"h":h,"dir":0.0,"pkg":0.0,"lost":0.0,"inc":0,
            "off":0,"det":0,"det_ind":0,"tres":0,"pkgc":0}); matched+=h
    total=sum(hrs.values())
    return {"hours":total,"direct":natw["rec"],"pkg":natw["pkg"],"lost":natw["lost"],"inc":natw["inc"],"off":natw["off"],
            "det":natw["det"],"det_ind":natw["det_ind"],"tres":natw["tres"],"pkgc":natw["pkgc"],
            "store_rows":srows,"resid":total-matched-transit,"transit":transit}
WD={w:_weekdata(w) for w in bm.WEEKS}          # per-week data, keyed by week-ending datetime
CUR=bm.CURRENT_WEEK
store_rows=WD[CUR]["store_rows"]; _resid_h=WD[CUR]["resid"]; _total_h=WD[CUR]["hours"]  # Store Detail = current week

weeks=[(1, datetime(2026,7,1), datetime(2026,7,5))]
end=datetime(2026,7,12); n=2
while end <= datetime(2027,6,29):
    weeks.append((n, end-timedelta(days=6), end)); end+=timedelta(days=7); n+=1
def period(d): return d.strftime("%b %Y")
periods=[]
for _,_,e in weeks:
    p=period(e)
    if p not in periods: periods.append(p)

def style_hdr(ws, row, labels):
    for i,h in enumerate(labels,1):
        c=ws.cell(row,i,h); c.font=Font(name="Arial",size=9,bold=True,color=WHITE)
        c.fill=PatternFill("solid",fgColor=NAVY); c.border=B
        c.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True)

wb=openpyxl.Workbook()
RATE="$C$3"

# ============ SHEET 1: Weekly Ledger ============
ws=wb.active; ws.title="Weekly Ledger"; NC=16
ws.merge_cells(start_row=1,start_column=1,end_row=1,end_column=NC)
t=ws.cell(1,1,"Woolworths New Zealand — FY27 Deployment & Recovery Tracker")
t.font=Font(name="Arial",size=14,bold=True,color=WHITE); t.fill=PatternFill("solid",fgColor=NAVY)
t.alignment=Alignment(horizontal="left",vertical="center",indent=1); ws.row_dimensions[1].height=26
ws.merge_cells(start_row=2,start_column=1,end_row=2,end_column=NC)
s=ws.cell(2,1,"FY27 = 1 Jul 2026 – 30 Jun 2027 · Cost = deployed hours × agreed bill rate (ex-GST) · Recovery = direct + packaging · Total Loss (Reported) = recovery + not recovered · SLS RTC covert LP")
s.font=Font(name="Arial",size=9,italic=True,color="5A6675"); s.alignment=Alignment(indent=1)
ws.cell(3,1,"Bill rate ($/hr, ex-GST):").font=Font(name="Arial",size=10,bold=True,color=INK)
rc=ws.cell(3,3,BILL_RATE); rc.number_format=MON; rc.fill=PatternFill("solid",fgColor=INPUT)
rc.font=Font(name="Arial",size=10,bold=True,color=INK); rc.border=B; rc.alignment=Alignment(horizontal="center")
ws.cell(3,4,"← agreed WW rate (input); Cost column = Hours × this. Reconciles to the SLS RTC invoice.").font=Font(name="Arial",size=9,italic=True,color=GOLD)
hdr=["Wk","Week Ending","Period","Hours","Cost $ (ex-GST)","Direct Recovery $","Packaging Recovery $","Total Recovery $",
     "Not Recovered $","Total Loss $ (Reported)",
     "Incidents","Offenders","Deterrents","Deterred Individuals","Trespass Actions","Packaging Events"]
HR=4; style_hdr(ws,HR,hdr); ws.row_dimensions[HR].height=30
STAT_COLS={"inc":11,"off":12,"det":13,"det_ind":14,"tres":15,"pkgc":16}
r=HR+1
for wk,ws0,we in weeks:
    wd=WD.get(we); filled=wd is not None
    ws.cell(r,1,wk); d=ws.cell(r,2,we); d.number_format=DT; ws.cell(r,3,period(we))
    if filled:
        ws.cell(r,4,wd["hours"]); ws.cell(r,6,wd["direct"]); ws.cell(r,7,wd["pkg"]); ws.cell(r,9,wd["lost"])
        for k,col in STAT_COLS.items(): ws.cell(r,col,wd[k])
    ws.cell(r,5,f"=D{r}*{RATE}").number_format=MON      # Cost = hours × rate
    ws.cell(r,8,f"=F{r}+G{r}").number_format=MON         # Total Recovery
    ws.cell(r,10,f"=H{r}+I{r}").number_format=MON        # Total Loss (Reported) = recovery + not recovered
    for c in range(1,NC+1):
        cell=ws.cell(r,c); cell.border=B; cell.font=Font(name="Arial",size=9.5,color=INK)
        cell.alignment=Alignment(horizontal="left" if c in (1,2,3) else "right")
        if c==4: cell.number_format='#,##0.0'
        if c in (5,6,7,8,9,10): cell.number_format=MON
        if c>=11: cell.number_format=INT
        if filled: cell.fill=PatternFill("solid",fgColor="F4FAF6")
    r+=1
last=r-1
ws.cell(r,1,"FY27"); ws.cell(r,3,"YTD TOTAL")
ws.cell(r,4,f"=SUM(D{HR+1}:D{last})").number_format='#,##0.0'
for col in (5,6,7,8,9,10): ws.cell(r,col,f"=SUM({L(col)}{HR+1}:{L(col)}{last})").number_format=MON
for col in range(11,NC+1): ws.cell(r,col,f"=SUM({L(col)}{HR+1}:{L(col)}{last})").number_format=INT
for c in range(1,NC+1):
    cell=ws.cell(r,c); cell.border=B; cell.fill=PatternFill("solid",fgColor=GOLD)
    cell.font=Font(name="Arial",size=10,bold=True,color=NAVY)
    cell.alignment=Alignment(horizontal="left" if c in (1,2,3) else "right")
for i,w in enumerate([5,14,10,8,15,15,16,14,14,16,10,10,11,13,13,13],1): ws.column_dimensions[L(i)].width=w
ws.freeze_panes="D5"

# ============ SHEET 2: Period & YTD Summary ============
ps=wb.create_sheet("Period & YTD Summary")
PNC=10
ps.merge_cells(start_row=1,start_column=1,end_row=1,end_column=PNC)
t=ps.cell(1,1,"FY27 — Period & YTD Summary (calendar-month accurate · roll into WW periods vs budget)")
t.font=Font(name="Arial",size=13,bold=True,color=WHITE); t.fill=PatternFill("solid",fgColor=NAVY)
t.alignment=Alignment(indent=1,vertical="center"); ps.row_dimensions[1].height=24
style_hdr(ps,3,["Period","Hours","Cost $ (ex-GST)","Total Recovery $","Total Loss $ (Reported)","Incidents","Offenders","Deterrents","Trespass","Weeks"])
WL="'Weekly Ledger'"
# Calendar-month accurate: re-bucket the SAME dated events (bm.month_of) and shift hours by the
# month they actually occurred, so a reporting week straddling a month-end (e.g. W5, 27 Jul-2 Aug)
# is split by day — August shows only 1-2 Aug work, not a full late-July week. Values are written
# directly (a SUMIF against the weekly rows would misplace a split week); YTD still ties exactly.
_magg,_,_=bm.aggregate(bm.month_of)
_mh=_month_hours()
def _mroll(p): return bm.rollup([a for (mm,s),a in _magg.items() if mm==p])
rr=4
for p in periods:
    mr=_mroll(p); h=_mh.get(p,0.0)
    ps.cell(rr,1,p)
    ps.cell(rr,2,round(h,1)).number_format='#,##0.0'
    ps.cell(rr,3,f"=B{rr}*{WL}!$C$3").number_format=MON       # Cost = hours × rate (rate lives on Weekly Ledger C3)
    ps.cell(rr,4,round(mr["rec"]+mr["pkg"],2)).number_format=MON   # Total Recovery = direct + packaging
    ps.cell(rr,5,round(mr["total_loss"],2)).number_format=MON      # Total Loss (Reported) = rec + lost + pkg
    ps.cell(rr,6,mr["inc"]).number_format=INT
    ps.cell(rr,7,mr["off"]).number_format=INT
    ps.cell(rr,8,mr["det"]).number_format=INT
    ps.cell(rr,9,mr["tres"]).number_format=INT
    ps.cell(rr,10,f"=COUNTIF({WL}!$C:$C,A{rr})").number_format=INT  # scheduled weeks in the period (budget basis)
    for c in range(1,PNC+1):
        cell=ps.cell(rr,c); cell.border=B; cell.font=Font(name="Arial",size=10,color=INK)
        cell.alignment=Alignment(horizontal="left" if c==1 else "right")
    rr+=1
ps.cell(rr,1,"FY27 YTD")
for c in range(2,PNC+1):
    ps.cell(rr,c,f"=SUM({L(c)}4:{L(c)}{rr-1})")
    ps.cell(rr,c).number_format='#,##0.0' if c==2 else (MON if c in (3,4,5) else INT)
for c in range(1,PNC+1):
    cell=ps.cell(rr,c); cell.border=B; cell.fill=PatternFill("solid",fgColor=GOLD)
    cell.font=Font(name="Arial",size=10,bold=True,color=NAVY); cell.alignment=Alignment(horizontal="left" if c==1 else "right")
for i,w in enumerate([13,9,15,16,17,10,10,11,10,8],1): ps.column_dimensions[L(i)].width=w
ps.cell(rr+2,1,"Hours, recovery, incidents & deterrents are allocated to the CALENDAR MONTH each was worked / occurred — a reporting week that spans a month-end is split by day, so a period here won't equal a plain sum of that week's Weekly Ledger row (the Weekly Ledger stays whole-week). Cost = hours × agreed bill rate (ex-GST), reconciles to the SLS RTC invoice. Weeks = scheduled weeks in the period (budget basis). Roll against the FY27 security budget.").font=Font(name="Arial",size=8.5,italic=True,color="8a95a3")

# ============ SHEETS 3 & 4: Store Detail — CUMULATIVE (FY-to-date) + This Week ============
# Glenn Sinclair (WW, 30 Jul 2026): "keep a cumulative track of the individual stores on this
# tab after each week." => Tab 3 = CUMULATIVE running totals per store across the FY to date;
# Tab 4 = the This-Week snapshot (preserved). Both grouped by region.
SNC=12
# cumulative per store across all weeks W1..CUR
_cum={}; _cum_resid=0.0; _cum_total=0.0; _cum_travel_wk=0.0
for _w in bm.WEEKS:
    _d=WD[_w]; _cum_resid+=_d["resid"]; _cum_total+=_d["hours"]; _cum_travel_wk+=_d.get("transit",0.0)
    for _reg,_lst in _d["store_rows"].items():
        for _x in _lst:
            _c=_cum.setdefault(_x["store"],{"store":_x["store"],"region":_reg,"h":0.0,"dir":0.0,"pkg":0.0,"lost":0.0,
                                            "inc":0,"off":0,"det":0,"det_ind":0,"tres":0,"pkgc":0})
            for _k in ("h","dir","pkg","lost","inc","off","det","det_ind","tres","pkgc"): _c[_k]+=_x[_k]
# ★ CUMULATIVE HOURS := authoritative full-period tag-sheet (Ahmad, 17 Aug 2026). The weekly ledger,
#   This-Week snapshot and Period tab keep their dated per-week actuals; only the FY-to-date cumulative
#   store hours (+ network total + residual) are re-based to the single 1-Jul→week-end export so the
#   cumulative ties to the source-of-truth timeclock. Recovery/incident columns stay weekly-summed.
_TAG=_cumulative_tagsheet_hours()
_CUM_SRC="summed weekly actuals"; _cum_travel=_cum_travel_wk   # default to summed weekly transit; overridden only by a complete tag-sheet
_weekly_total=sum(WD[w]['hours'] for w in bm.WEEKS)
# Only re-base cumulative store hours to a tag-sheet if it is a (near-)COMPLETE FY-to-date export.
# A partial/wrong tag-sheet would zero every store it omits (whole regions); in that case keep the
# summed weekly actuals, which are authoritative (each week's hours came from that week's timeclock).
if _TAG:
    _missing=[_c for _c in _cum.values() if _c["h"]>0.05 and _TAG.get(_mn(_c["store"])) is None]
    _tag_total=_TAG.get("__total__",0.0)
    if len(_missing)<=2 and _tag_total>=0.80*_weekly_total:
        _matched=0.0; _have={_mn(_c["store"]) for _c in _cum.values()}
        for _c in _cum.values():
            _h=_TAG.get(_mn(_c["store"])); _c["h"]=_h if _h is not None else 0.0; _matched+=_c["h"]
        # tag-sheet stores with NO weekly-derived row (covered, no incidents, missed by the weekly
        # exports) → add them so every FY-to-date deployed store appears and rows sum to the NETWORK total.
        _disp=_TAG.get("__disp__",{})
        for _k,_hh in list(_TAG.items()):
            if _k.startswith("__") or _k in _have or not isinstance(_hh,(int,float)) or _hh<=0.05: continue
            _nm=_disp.get(_k,_k.title()+" Woolworths"); _rg=bm.STORE_REGION_OVERRIDE.get(_nm.lower(),"Other")
            _cum[_nm]={"store":_nm,"region":_rg,"h":_hh,"dir":0.0,"pkg":0.0,"lost":0.0,
                       "inc":0,"off":0,"det":0,"det_ind":0,"tres":0,"pkgc":0}; _matched+=_hh
        _cum_total=_tag_total
        _cum_resid=max(0.0,_cum_total-_matched)
        _cum_travel=_TAG.get("__travel__",0.0)
        _CUM_SRC="authoritative full-period tag-sheet"
        print(f"  cumulative Store Detail := {_CUM_SRC}: {_cum_total:,.2f}h stores + {_cum_travel:,.2f}h transit "
              f"= {_cum_total+_cum_travel:,.2f}h (weekly ledger stays {_weekly_total:,.2f}h)")
    else:
        print(f"  ⚠ cumulative tag-sheet incomplete ({len(_missing)} stores missing, {_tag_total:,.0f}h vs "
              f"weekly {_weekly_total:,.0f}h) — using SUMMED WEEKLY ACTUALS for Store Detail hours", file=sys.stderr)
        _cum_total=_weekly_total
_cum_rows=defaultdict(list)
for _c in _cum.values(): _cum_rows[_c["region"]].append(_c)

def build_store_sheet(name,title,sub,rows_by_region,resid,total,resid_label,transit=0.0,
                      transit_label="Team Transit / Travel (to & from WW sites)"):
    sd=wb.create_sheet(name)
    sd.merge_cells(start_row=1,start_column=1,end_row=1,end_column=SNC)
    t=sd.cell(1,1,title); t.font=Font(name="Arial",size=13,bold=True,color=WHITE); t.fill=PatternFill("solid",fgColor=NAVY)
    t.alignment=Alignment(indent=1,vertical="center"); sd.row_dimensions[1].height=24
    sd.merge_cells(start_row=2,start_column=1,end_row=2,end_column=SNC)
    sd.cell(2,1,sub).font=Font(name="Arial",size=9,italic=True,color="5A6675")
    style_hdr(sd,3,["Store","Hours","Direct Recovery $","Packaging $","Total Recovery $","Not Recovered $","Total Loss $ (Reported)","Incidents","Offenders","Deterrents","Trespass","Pkg Events"])
    sd.row_dimensions[3].height=28
    def row(r,label,d,kind="store"):
        sd.cell(r,1,label); sd.cell(r,2,round(d["h"],1)).number_format='#,##0.0'
        sd.cell(r,3,round(d["dir"],2)).number_format=MON; sd.cell(r,4,round(d["pkg"],2)).number_format=MON
        sd.cell(r,5,round(d["dir"]+d["pkg"],2)).number_format=MON; sd.cell(r,6,round(d["lost"],2)).number_format=MON
        sd.cell(r,7,round(d["dir"]+d["pkg"]+d["lost"],2)).number_format=MON
        for col,k in [(8,"inc"),(9,"off"),(10,"det"),(11,"tres"),(12,"pkgc")]: sd.cell(r,col,d[k]).number_format=INT
        for c in range(1,SNC+1):
            cell=sd.cell(r,c); cell.border=B; cell.alignment=Alignment(horizontal="left" if c==1 else "right")
            if kind=="store": cell.font=Font(name="Arial",size=9.5,color=INK)
            elif kind=="sub": cell.font=Font(name="Arial",size=9.5,bold=True,color=NAVY); cell.fill=PatternFill("solid",fgColor=LIGHT)
            else: cell.font=Font(name="Arial",size=10,bold=True,color=NAVY); cell.fill=PatternFill("solid",fgColor=GOLD)
    def agg(lst): return {k:sum(x[k] for x in lst) for k in ("h","dir","pkg","lost","inc","off","det","tres","pkgc")}
    r=4
    for reg in _regs:
        if reg not in rows_by_region: continue
        sd.merge_cells(start_row=r,start_column=1,end_row=r,end_column=SNC)
        hc=sd.cell(r,1,f"▍ {reg}"); hc.font=Font(name="Arial",size=10,bold=True,color=NAVY)
        hc.fill=PatternFill("solid",fgColor=REG); hc.alignment=Alignment(indent=1); r+=1
        lst=sorted(rows_by_region[reg],key=lambda x:-(x["dir"]+x["pkg"]+x["lost"]))
        for st in lst: row(r,st["store"],st,"store"); r+=1
        row(r,f"{reg} — subtotal",agg(lst),"sub"); r+=1
    if resid>0.05:
        row(r,resid_label,{"h":resid,"dir":0,"pkg":0,"lost":0,"inc":0,"off":0,"det":0,"tres":0,"pkgc":0},"sub"); r+=1
    if transit>0.05:
        row(r,transit_label,{"h":transit,"dir":0,"pkg":0,"lost":0,"inc":0,"off":0,"det":0,"tres":0,"pkgc":0},"sub"); r+=1
    _all=[x for lst in rows_by_region.values() for x in lst]
    net=agg(_all); net["h"]=total+transit; row(r,"NETWORK — all stores",net,"net")
    for i,w in enumerate([34,8,15,12,15,14,16,10,10,10,9,9],1): sd.column_dimensions[L(i)].width=w
    sd.freeze_panes="B4"

_cum_sub=("Running totals per store across the FY to date · grouped by region · accumulates each week"
          if not _TAG else
          "FY-to-date per store · HOURS tie to the authoritative Connecteam timeclock (1 Jul → week-end), "
          "incl. team transit as its own line; recovery & activity accumulate each week · grouped by region")
build_store_sheet("Store Detail",
    f"Woolworths NZ — FY27 Store Detail · CUMULATIVE to Week {bm.week_num(CUR)} ({CUR.strftime('%d %b %Y')})",
    _cum_sub,
    _cum_rows,_cum_resid,_cum_total,"Covered stores — no incidents logged to date",transit=_cum_travel)
build_store_sheet("This Week — Store Detail",
    f"Woolworths NZ — FY27 Store Detail · This Week (Week {bm.week_num(CUR)}, {bm.week_start(CUR).day}–{CUR.day} {CUR.strftime('%b %Y')})",
    "Hours + recovery + activity by store · THIS WEEK only · grouped by region",
    store_rows,_resid_h,_total_h,"Covered stores — no incidents logged this week")

wb.save(OUT)
print(f"wrote {OUT}")
for w in bm.WEEKS:
    d=WD[w]; print(f"  W{bm.week_num(w)} ({bm.week_label(w)}): {d['hours']:.0f}h × ${BILL_RATE} = ${d['hours']*BILL_RATE:,.2f} cost | recovery ${d['direct']+d['pkg']:,.2f}")
