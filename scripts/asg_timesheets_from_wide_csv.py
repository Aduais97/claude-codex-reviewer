import csv,datetime,sys,re
from collections import defaultdict
import openpyxl
from openpyxl.styles import Font,PatternFill,Alignment,Border,Side
# Wide/pivoted CSV adapter of asg_timesheets_by_site.py — same rules/output, source = a Deputy
# "Timesheets by employee, pivoted by day" export (one row per employee x area; per-day hour
# columns + Total). No shift times, so hours are taken AS Deputy reports them per calendar day
# (Deputy splits overnight shifts at midnight, so post-midnight Sunday hours sit under the Mon col).
CSVPATH=sys.argv[1]
OUTDIR="/Users/ahmadduais/Desktop/ASG - Timesheets"

NZ_HOLIDAYS={"2026-01-01","2026-01-02","2026-01-26","2026-02-06","2026-04-03","2026-04-06",
 "2026-04-27","2026-06-01","2026-07-10","2026-10-26","2026-12-25","2026-12-28",
 "2027-01-01","2027-01-04","2027-02-06","2027-03-26","2027-03-29","2027-04-26",
 "2027-06-07","2027-06-25","2027-10-25","2027-12-27","2027-12-28"}

EXCLUDE={"Auckland Harbour Suites","Viaduct Harbour","Metropolis","Maungawhau Station Mt Eden",
         "Mercury Lane - Karanagahape Station","Te Waihorotiu Station - Aotea","HOTC"}
HD_VENUES=["danny doolan","union post","the fox","the cav","the cellar","cellar bar","slattery",
           "brew on quay","o'dowds","odowds","doolan brothers","parasol","broken lantern"]
ALWAYS_HD={"danny doolan":["peniamina","peniama"]}
CCTV_PARENT={"CCTV Flying Moa":"The Flying Moa","CCTV Garrisons":"Garrison Public House",
 "CCTV Lulas Inn":"The Lula Inn","CCTV Moretons":"Moretons Bar & Restaurant",
 "CCTV Postmans Leg":"The Postman's Leg","CCTV Regatta":"Regatta Bar And Eatery",
 "CCTV Rosies Takapuna":"Rosies Takapuna ","CCTV Rosies Viaduct":"Rosies Viaduct",
 "CCTV Sweatshop Brew Kitchen":"Sweatshop Brew Kitchen","CCTV Merchant Bar":"The Merchant",
 "CCTV Zoo Keepers Son":"The Zookeeper's Son","CCTV Goode Brothers Botany":"Goode Brothers Botany",
 "CCTV Goode Brothers New Lynn":"Goode Brothers New Lynn","CCTV Goode Brothers North West":"Goode Brothers North West",
 "CCTV Elephant Wrestler":"Elephant Wrestler","CCTV Basalt":"Basalt"}

def hk(site):
    s=site.lower()
    for h in HD_VENUES:
        if h in s:return h
    return None

# ── load wide CSV: detect day columns (header cells ending in DD-MM-YYYY) ──
with open(CSVPATH,newline='',encoding='utf-8-sig') as fh:
    rdr=csv.DictReader(fh);raw=list(rdr);cols=rdr.fieldnames
daymap={}  # column header -> ISO date
for c in cols:
    m=re.search(r'(\d{2})-(\d{2})-(\d{4})',c)
    if m:daymap[c]=f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
if not daymap:sys.exit("No day columns (DD-MM-YYYY) found in header: "+str(cols))

def fnum(x):
    try:return float(str(x).strip())
    except:return 0.0

# derive week (Monday on/before earliest day column)
alldates=sorted(daymap.values())
d0d=datetime.datetime.strptime(alldates[0],"%Y-%m-%d").date()
mon=d0d-datetime.timedelta(days=d0d.weekday())
WK_START=mon.strftime("%Y-%m-%d")
days=[(mon+datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(8)]
PH_DATES={(mon+datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)}&NZ_HOLIDAYS

def lbl(ds):
    dt=datetime.datetime.strptime(ds,"%Y-%m-%d");x=dt.strftime("%a %d %b")
    return x+" (PH)" if ds in PH_DATES else x

# ── build shift list: one entry per (employee x area x non-zero day cell) ──
# hours taken as reported (per calendar day); whole-day value sits on that day (no sub-day split).
shifts=[]
for r in raw:
    site=(r.get("Area") or r.get("Area Name") or "").strip()
    if not site or site in EXCLUDE:continue
    name=(r.get("Employee Name") or f"{r.get('Employee First Name','')} {r.get('Employee Last Name','')}").strip()
    for col,ds in daymap.items():
        h=fnum(r.get(col))
        if h<=0:continue
        shifts.append({"site":site,"emp":name,"night":ds,"tot":h,"portions":{ds:round(h,4)}})

# HD per (site,night) — employee with most hours that day = HD (proxy for longest shift); always-HD overrides
night_emp=defaultdict(lambda:defaultdict(float))
for sh in shifts:
    if hk(sh["site"]):night_emp[(sh["site"],sh["night"])][sh["emp"]]+=sh["tot"]
hd_of=defaultdict(set)
for (site,night),ppl in night_emp.items():
    hd_of[(site,night)].add(max(ppl,key=ppl.get))
    for sk in ALWAYS_HD.get(hk(site),[]):
        for nm in ppl:
            if sk in nm.lower():hd_of[(site,night)].add(nm)

summary=defaultdict(lambda:{"HD":0.0,"Guard":0.0,"PH HD":0.0,"PH Guard":0.0})
detail=defaultdict(list)
for sh in shifts:
    split=hk(sh["site"]) is not None
    ishd = sh["emp"] in hd_of[(sh["site"],sh["night"])] if split else False
    role="HD" if ishd else "Guard"
    for ds,h in sh["portions"].items():
        if h<=0:continue
        ph=ds in PH_DATES;S=summary[sh["site"]]
        if split:
            S[("PH HD" if ph else "HD") if ishd else ("PH Guard" if ph else "Guard")]+=h
        else:
            S["PH HD" if ph else "HD"]+=h
        detail[(sh["site"],ds)].append((sh["emp"],role if split else "Guard",round(h,2)))

FIXED={"Elliott Stables":6.0,"Jungle 8":6.0}
for venue,hh in FIXED.items():
    guards=sorted({sh["emp"] for sh in shifts if sh["site"]==venue})
    dates=sorted({d for (s,d) in detail if s==venue})
    name=" / ".join(guards) if guards else "ProHost (split)"
    when=dates[0] if dates else days[6]
    for k in [k for k in list(detail) if k[0]==venue]:del detail[k]
    summary[venue]={"HD":hh,"Guard":0.0,"PH HD":0.0,"PH Guard":0.0}
    detail[(venue,when)]=[(name,"Guard",hh)]

present=set(summary)
def parent_of(site):
    p=CCTV_PARENT.get(site, site[5:]).strip();return p if p in present else None
nested={s for s in summary if s.startswith("CCTV") and parent_of(s)}
def grp(site):
    if site in nested:return (parent_of(site).lower(),1,site.lower())
    return (site.lower(),0,site.lower())
ordered=sorted(summary,key=grp)

daysum=defaultdict(lambda:defaultdict(float))
for (site,ds),entries in detail.items():
    for nm,role,h in entries:daysum[site][ds]+=h
active_days=[d for d in days if any(daysum[s].get(d,0) for s in summary)]
DAYCOL0=8

weekending=datetime.datetime.strptime(days[6],"%Y-%m-%d").strftime("%d-%m-%Y")
OUT=f"{OUTDIR}/Timesheet - Weekending - {weekending}.xlsx"
wb=openpyxl.Workbook()
HDR=PatternFill("solid",fgColor="1F3864");HF=Font(color="FFFFFF",bold=True);BF=Font(bold=True)
PHF=PatternFill("solid",fgColor="FCE4D6");HDF=PatternFill("solid",fgColor="E2EFDA")
CCF=PatternFill("solid",fgColor="EDEDED")
tn=Side(style="thin",color="BFBFBF");BD=Border(tn,tn,tn,tn);CN=Alignment(horizontal="center")
ws=wb.active;ws.title="Site Summary"
ws.append([f"Pay week {days[0]} to {days[6]}   (Public holiday: {' + '.join(sorted(PH_DATES)) or 'none'})   — Deputy pivoted CSV, hours as reported per calendar day (no shift times; Deputy splits overnight shifts at midnight, so post-midnight Sun hours sit under Mon {datetime.datetime.strptime(days[7],'%Y-%m-%d').strftime('%d %b')})"])
ws['A1'].font=Font(bold=True,size=12);ws.append([])
ws.append(["CLIENT / SITE","HD","Guard","PH HD","PH Guard","Total"])
for c in range(1,7):
    x=ws.cell(3,c);x.fill=HDR;x.font=HF;x.alignment=CN;x.border=BD
for i,ds in enumerate(active_days):
    x=ws.cell(3,DAYCOL0+i,lbl(ds));x.fill=(PHF if ds in PH_DATES else HDR)
    x.font=(Font(bold=True) if ds in PH_DATES else HF);x.alignment=CN;x.border=BD
tot={"HD":0,"Guard":0,"PH HD":0,"PH Guard":0,"T":0}
dtot=defaultdict(float)
for site in ordered:
    S=summary[site];t=sum(S.values())
    label=("   ↳ "+site) if site in nested else site+(" ★HD" if hk(site) else "")
    ws.append([label,round(S["HD"],2)or"",round(S["Guard"],2)or"",round(S["PH HD"],2)or"",round(S["PH Guard"],2)or"",round(t,2)])
    r=ws.max_row
    for i,ds in enumerate(active_days):
        v=daysum[site].get(ds,0);c=DAYCOL0+i
        cell=ws.cell(r,c,round(v,2) if v else "");cell.alignment=CN;dtot[ds]+=v
        if ds in PH_DATES and v:cell.fill=PHF
    if site.startswith("CCTV"):
        for c in range(1,7):ws.cell(r,c).fill=CCF
    for k in("HD","Guard","PH HD","PH Guard"):tot[k]+=S[k]
    tot["T"]+=t
    for c in list(range(1,7))+[DAYCOL0+i for i in range(len(active_days))]:ws.cell(r,c).border=BD
rr=ws.max_row+1
ws.append(["TOTAL",round(tot["HD"],2),round(tot["Guard"],2),round(tot["PH HD"],2),round(tot["PH Guard"],2),round(tot["T"],2)])
for i,ds in enumerate(active_days):
    ws.cell(rr,DAYCOL0+i,round(dtot[ds],2)).alignment=CN
for c in list(range(1,7))+[DAYCOL0+i for i in range(len(active_days))]:ws.cell(rr,c).font=BF;ws.cell(rr,c).border=BD
ws.column_dimensions['A'].width=44
for col in 'BCDEF':ws.column_dimensions[col].width=11
for i in range(len(active_days)):ws.column_dimensions[openpyxl.utils.get_column_letter(DAYCOL0+i)].width=13
ws.append([]);ws.append(["★HD venue. HD = longest shift that night (most hours, whole shift) — can change nightly. Peniama always HD at Danny's. PH = hours before midnight on the public holiday. CCTV shown under parent venue."])

ws2=wb.create_sheet("Detail by Site & Date")
ws2.append(["SITE","DATE","GUARD","ROLE","HOURS"])
for c in range(1,6):
    x=ws2.cell(1,c);x.fill=HDR;x.font=HF;x.alignment=CN;x.border=BD
for site in ordered:
    for ds in days:
        if (site,ds) not in detail:continue
        for nm,role,h in sorted(detail[(site,ds)],key=lambda x:(x[1]!="HD",x[0])):
            ws2.append([site,lbl(ds),nm,role,h]);r2=ws2.max_row
            if role=="HD":
                for c in range(1,6):ws2.cell(r2,c).fill=HDF
            if ds in PH_DATES:ws2.cell(r2,2).fill=PHF
            for c in range(1,6):ws2.cell(r2,c).border=BD
ws2.column_dimensions['A'].width=34;ws2.column_dimensions['B'].width=16;ws2.column_dimensions['C'].width=30
ws2.column_dimensions['D'].width=8;ws2.column_dimensions['E'].width=8;ws2.freeze_panes="A2"
wb.save(OUT)
print("Saved:",OUT)
print(f"Week {days[0]} to {days[6]} | PH: {sorted(PH_DATES) or 'none'}")
print(f"Sites {len(summary)} | total {tot['T']:.2f} | HD={tot['HD']:.2f} Guard={tot['Guard']:.2f} PH-HD={tot['PH HD']:.2f} PH-Guard={tot['PH Guard']:.2f}")
print(f"Shift-cells: {len(shifts)} | excluded-site rows dropped | day cols: {len(active_days)}")
print("HD venues:")
for site in ordered:
    if hk(site):
        S=summary[site];print(f"  {site:<24} HD={S['HD']:.2f} Guard={S['Guard']:.2f} PH-HD={S['PH HD']:.2f} PH-Guard={S['PH Guard']:.2f}")
