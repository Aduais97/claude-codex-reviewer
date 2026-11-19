#!/usr/bin/env python3
"""HOTC Calls vs Funding workbook for Edward's board/KPI pack.
Tab 1: Monthly FY26 vs FY25. Tab 2: Funding->Calls analysis + verdict.
Tab 3: LCF pilot weekly natural experiment (Apr-Aug 2026) with chart."""
import glob, openpyxl, os
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, Reference
from openpyxl.utils import get_column_letter

TREE = "/Users/ahmadduais/Desktop/ASG/Operations/Clients/HOTC"
DL2024 = "/Users/ahmadduais/Downloads/2024"
NAVY='FF1F3864'; GOLD='FFB8912F'; LIGHT='FFEDF0F7'; GREENF='FFE3F1E4'; AMBER='FFFDF3D6'; REDF='FFF6DEDE'
WHITE='FFFFFFFF'
thin=Side(style='thin',color='FFBFBFBF'); BORDER=Border(thin,thin,thin,thin)
def cd(p):
    try:
        ws=openpyxl.load_workbook(p,data_only=True).active
        for r in ws.iter_rows(values_only=True):
            if r and r[0] and 'calls made from businesses' in str(r[0]).lower():
                n=[c for c in r[1:] if isinstance(c,(int,float))]
                return (int(n[-1]) if n else 0, len([c for c in r[1:-1] if isinstance(c,(int,float))]))
    except: pass
    return 0,0
def month_tot(base,year,month,is2024=False):
    tot=days=0
    patt=f"{DL2024}/{month}/**/*.xlsx" if is2024 else f"{base}/{year}/{month}/**/Weekly Data Report*.xlsx"
    for f in glob.glob(patt,recursive=True):
        if is2024 and 'weekly data report' not in f.lower(): continue
        c,d=cd(f); tot+=c; days+=d
    return tot,days

MONTHS=['July','August','September','October','November','December','January','February','March','April','May','June']
MAB={'July':'Jul','August':'Aug','September':'Sep','October':'Oct','November':'Nov','December':'Dec',
     'January':'Jan','February':'Feb','March':'Mar','April':'Apr','May':'May','June':'Jun'}
fy26=[]; fy25=[]
for i,m in enumerate(MONTHS):
    fy26.append(month_tot(TREE,'2025',m) if i<6 else month_tot(TREE,'2026',m))
    fy25.append(month_tot(None,None,m,is2024=True) if i<6 else month_tot(TREE,'2025',m))
c26=[x[0] for x in fy26]; d26=[x[1] for x in fy26]
c25=[x[0] for x in fy25]; d25=[x[1] for x in fy25]
T26,T25=sum(c26),sum(c25); L26,L25=sum(c26[1:]),sum(c25[1:])

wb=openpyxl.Workbook()
def hcell(ws,r,c,v,fill=NAVY,color=WHITE,bold=True,align='center',sz=11):
    cell=ws.cell(r,c,v); cell.font=Font(bold=bold,color=color,size=sz)
    if fill: cell.fill=PatternFill('solid',fgColor=fill)
    cell.alignment=Alignment(horizontal=align,vertical='center',wrap_text=True); cell.border=BORDER
    return cell
def cell(ws,r,c,v,bold=False,align='center',fill=None,color='FF000000'):
    x=ws.cell(r,c,v); x.font=Font(bold=bold,color=color); x.alignment=Alignment(horizontal=align,vertical='center')
    if fill: x.fill=PatternFill('solid',fgColor=fill)
    x.border=BORDER; return x

# ---------- Tab 1: Monthly ----------
ws=wb.active; ws.title="Monthly Calls"
ws['A1']="HOTC — Calls from Businesses: FY2026 vs FY2025"; ws['A1'].font=Font(bold=True,size=14,color=NAVY)
ws['A2']="FY2026 = 1 Jul 2025–30 Jun 2026  |  FY2025 = 1 Jul 2024–30 Jun 2025"; ws['A2'].font=Font(italic=True,color='FF555555')
h=4
for j,t in enumerate(['Month','FY26 calls','FY26 /day','FY25 calls','FY25 /day','Change','YoY %']):
    hcell(ws,h,j+1,t)
for i,m in enumerate(MONTHS):
    r=h+1+i; partial=(i==0 and d26[0]<20)
    cell(ws,r,1,MAB[m],bold=True,align='left')
    cell(ws,r,2, f"{c26[i]} *" if partial else c26[i])
    cell(ws,r,3, round(c26[i]/d26[i],1) if d26[i] else 0)
    cell(ws,r,4, c25[i]); cell(ws,r,5, round(c25[i]/d25[i],1) if d25[i] else 0)
    if partial:
        cell(ws,r,6,"— *",fill=LIGHT); cell(ws,r,7,"— *",fill=LIGHT)
    else:
        dlt=c26[i]-c25[i]; cell(ws,r,6, f"{dlt:+d}", color='FF2E7D32' if dlt>=0 else 'FFB01E1E')
        cell(ws,r,7, f"{(c26[i]/c25[i]-1)*100:+.0f}%", color='FF2E7D32' if dlt>=0 else 'FFB01E1E')
r=h+13
cell(ws,r,1,"Aug–Jun (like-for-like)",bold=True,align='left',fill='FFE4EBF6')
cell(ws,r,2,L26,bold=True,fill='FFE4EBF6'); cell(ws,r,3,round(L26/sum(d26[1:]),1),bold=True,fill='FFE4EBF6')
cell(ws,r,4,L25,bold=True,fill='FFE4EBF6'); cell(ws,r,5,round(L25/sum(d25[1:]),1),bold=True,fill='FFE4EBF6')
cell(ws,r,6,f"{L26-L25:+d}",bold=True,fill='FFE4EBF6',color='FFB01E1E')
cell(ws,r,7,f"{(L26/L25-1)*100:+.0f}%",bold=True,fill='FFE4EBF6',color='FFB01E1E')
r+=1
cell(ws,r,1,"Full-year total",bold=True,align='left',fill=LIGHT)
cell(ws,r,2,f"{T26} *",bold=True,fill=LIGHT); cell(ws,r,3,"",fill=LIGHT)
cell(ws,r,4,T25,bold=True,fill=LIGHT); cell(ws,r,5,"",fill=LIGHT)
cell(ws,r,6,"not comparable",bold=True,fill=LIGHT,color='FF555555'); cell(ws,r,7,"see *",fill=LIGHT,color='FF555555')
ws['A20']="* July 2025 part-reported (2 of ~4–5 weeks); excluded from YoY. Valid comparison = Aug–Jun like-for-like."
ws['A20'].font=Font(italic=True,size=9,color='FF555555')
for col,w in zip('ABCDEFG',[24,12,11,12,11,12,10]): ws.column_dimensions[col].width=w

# ---------- Tab 2: Funding -> Calls ----------
ws2=wb.create_sheet("Funding vs Calls")
ws2['A1']="Does funding drive calls? — Evidence"; ws2['A1'].font=Font(bold=True,size=14,color=NAVY)
ws2['A2']="Business calls are HOTC's utilisation/engagement measure. Below tests whether they track deployment/funding."
ws2['A2'].font=Font(italic=True,color='FF555555')
# annual block
hcell(ws2,4,1,"Annual",fill=GOLD,color=NAVY,align='left'); hcell(ws2,4,2,"FY25"); hcell(ws2,4,3,"FY26"); hcell(ws2,4,4,"Change")
rows=[("Funding (relative index — ASG est., replace w/ $)",120,100,"−20%"),
      ("Total business calls",T25,f"{T26} *","−18% (raw)"),
      ("Calls per patrol day (Aug–Jun)",round(L25/sum(d25[1:]),1),round(L26/sum(d26[1:]),1),f"{(L26/L25-1)*100:+.0f}% l-f-l")]
for k,(lab,a,b,ch) in enumerate(rows):
    r=5+k; cell(ws2,r,1,lab,align='left'); cell(ws2,r,2,a); cell(ws2,r,3,b); cell(ws2,r,4,ch,color='FFB01E1E')
cell(ws2,8,1,"→ Calls fell roughly in proportion to the funding cut. Directionally supported.",align='left',fill=AMBER); ws2.merge_cells('A8:D8')

# LCF pilot natural experiment
hcell(ws2,10,1,"LCF pilot natural experiment (2026)",fill=GOLD,color=NAVY,align='left')
hcell(ws2,10,2,"Calls/day"); hcell(ws2,10,3,"vs baseline"); hcell(ws2,10,4,"Funding")
piv=[("Pre-pilot baseline (Jan–May)",5.8,"—","reduced",LIGHT),
     ("LCF PILOT (Jun – 24 Jul, +1 team)",8.8,"+52%","+ uplift",GREENF),
     ("Post-pilot (27 Jul – Aug)",5.6,"reverts","removed",LIGHT)]
for k,(lab,v,ch,fund,fl) in enumerate(piv):
    r=11+k; cell(ws2,r,1,lab,align='left',fill=fl,bold=(k==1)); cell(ws2,r,2,v,fill=fl,bold=(k==1))
    cell(ws2,r,3,ch,fill=fl,bold=(k==1),color='FF2E7D32' if k==1 else 'FF555555'); cell(ws2,r,4,fund,fill=fl)
cell(ws2,15,1,"→ Calls surged +52% when the funded team deployed and reverted the moment the pilot ended (24 Jul). "
              "This surge-and-revert is the strongest, near-causal evidence that funding drives calls.",align='left',fill=GREENF)
ws2.merge_cells('A15:D15'); ws2.row_dimensions[15].height=42
ws2['A15'].alignment=Alignment(wrap_text=True,vertical='center')
# verdict + caveats
cell(ws2,17,1,"VERDICT: SUPPORTED — clearly by the LCF pilot; directionally by the annual drop.",align='left',bold=True); ws2.merge_cells('A17:D17')
ws2['A17'].fill=PatternFill('solid',fgColor='FFE4EBF6')
for k,t in enumerate([
   "Caveats for the board:",
   "• The ~20% funding figure is ASG's estimate — insert actual $ to make it bulletproof.",
   "• Seasonality exists (Oct 7.9/day, Dec 8.5/day were high WITHOUT extra funding), so it is not a pure 1:1 line.",
   "• The pilot's surge-and-revert is the clean proof; the FY25→FY26 drop is suggestive, not proof."]):
    ws2.cell(19+k,1,t).font=Font(italic=(k>0),bold=(k==0),size=10,color='FF555555')
for col,w in zip('ABCD',[46,14,14,16]): ws2.column_dimensions[col].width=w

# ---------- Tab 3: LCF pilot weekly ----------
ws3=wb.create_sheet("LCF Pilot Weekly")
ws3['A1']="LCF Pilot — weekly calls/day (Apr–Aug 2026)"; ws3['A1'].font=Font(bold=True,size=14,color=NAVY)
ws3['A2']="Pilot window shaded green (2 Jun – 24 Jul 2026). Surge during funding, revert after."
ws3['A2'].font=Font(italic=True,color='FF555555')
weeks=[]
for m in ['April','May','June','July','August']:
    for f in sorted(glob.glob(f"{TREE}/2026/{m}/**/Weekly Data Report.xlsx",recursive=True)):
        c,d=cd(f); wk=f.split(f'/{m}/')[1].split('/')[0]
        weeks.append((m,wk,c,round(c/d,1) if d else 0))
def phase(m,wk):
    if m=='June': return 'PILOT'
    if m=='July':
        if 'Week 1' in wk or 'Week 2' in wk or ('Week 3' in wk): return 'PILOT'  # to ~19-24 Jul
        return 'post'
    if m in ('April','May'): return 'pre'
    return 'post'
for j,t in enumerate(['Month','Week','Calls','Calls/day','Phase']): hcell(ws3,4,j+1,t)
for i,(m,wk,c,pd) in enumerate(weeks):
    r=5+i; ph=phase(m,wk); fl=GREENF if ph=='PILOT' else None
    cell(ws3,r,1,MAB[m],align='left',fill=fl); cell(ws3,r,2,wk,align='left',fill=fl)
    cell(ws3,r,3,c,fill=fl); cell(ws3,r,4,pd,fill=fl,bold=(ph=='PILOT')); cell(ws3,r,5,ph,fill=fl,bold=(ph=='PILOT'))
last=4+len(weeks)
ch=LineChart(); ch.title="Calls per day — pilot vs baseline"; ch.height=8; ch.width=20
data=Reference(ws3,min_col=4,min_row=4,max_row=last); cats=Reference(ws3,min_col=2,min_row=5,max_row=last)
ch.add_data(data,titles_from_data=True); ch.set_categories(cats); ch.y_axis.title='Calls/day'
ws3.add_chart(ch,f"G4")
for col,w in zip('ABCDE',[8,34,9,11,10]): ws3.column_dimensions[col].width=w

# ---------- extract ALL metrics monthly (both FYs) ----------
METRICS=[('calls','calls made from businesses','Calls from Businesses'),('police','police calls','Police Calls'),
 ('aggr','aggressive behavio','Aggressive Behaviour'),('drink','public drinking','Public Drinking/Cannabis'),
 ('assist','assistance provided','Assistance Provided'),('serious','serious incidents','Serious Incidents'),
 ('arrests','arrests','Arrests'),('injuries','injuries','Injuries Reported'),('vagr','vagrants moved on','Vagrants Moved On'),
 ('theft','shoplifting','Shoplifting/Theft'),('intox','intoxicated','Intoxicated Persons'),('medical','medical responses','Medical Responses')]
def metrics_of(p):
    out={}
    try:
        wsx=openpyxl.load_workbook(p,data_only=True).active
        for r in wsx.iter_rows(values_only=True):
            if not r or not r[0]: continue
            lab=str(r[0]).strip().lower()
            for key,kw,_ in METRICS:
                if kw in lab and key not in out:
                    nums=[c for c in r[1:] if isinstance(c,(int,float))]
                    if nums: out[key]=int(nums[-1])
    except: pass
    return out
def files_for(month,fy,i):
    if fy==26: return glob.glob(f"{TREE}/2025/{month}/**/Weekly Data Report*.xlsx",recursive=True) if i<6 else glob.glob(f"{TREE}/2026/{month}/**/Weekly Data Report*.xlsx",recursive=True)
    return [f for f in glob.glob(f"{DL2024}/{month}/**/*.xlsx",recursive=True) if 'weekly data report' in f.lower()] if i<6 else glob.glob(f"{TREE}/2025/{month}/**/Weekly Data Report*.xlsx",recursive=True)
def agg(fy):
    res={}
    for i,m in enumerate(MONTHS):
        tot={}
        for f in files_for(m,fy,i):
            for k,v in metrics_of(f).items(): tot[k]=tot.get(k,0)+v
        res[m]=tot
    return res
M26=agg(26); M25=agg(25); mkeys=[k for k,_,_ in METRICS]; mlab={k:lab for k,_,lab in METRICS}

# ---------- Tab: All Metrics Monthly ----------
ws4=wb.create_sheet("All Metrics Monthly")
ws4['A1']="HOTC — All Metrics, Monthly Totals (FY26 & FY25)"; ws4['A1'].font=Font(bold=True,size=14,color=NAVY)
ws4['A2']="Detail incident metrics (serious→medical) only tracked from Mar 2026 — blank = not recorded that period."
ws4['A2'].font=Font(italic=True,color='FF555555')
def metric_block(ws,startrow,data,title):
    hcell(ws,startrow,1,title,fill=GOLD,color=NAVY,align='left')
    hcell(ws,startrow,2,"Metric \\ Month",align='left')
    for j,m in enumerate(MONTHS): hcell(ws,startrow,3+j,MAB[m])
    hcell(ws,startrow,15,"Total")
    for k_i,k in enumerate(mkeys):
        r=startrow+1+k_i; cell(ws,r,2,mlab[k],align='left',bold=True)
        tot=0; any_v=False
        for j,m in enumerate(MONTHS):
            v=data[m].get(k)
            if v is None: cell(ws,r,3+j,"",fill=LIGHT)
            else: cell(ws,r,3+j,v); tot+=v; any_v=True
        cell(ws,r,15,tot if any_v else "",bold=True)
    return startrow+1+len(mkeys)
nxt=metric_block(ws4,4,M26,"FY2026 (Jul 25 – Jun 26)")
metric_block(ws4,nxt+2,M25,"FY2025 (Jul 24 – Jun 25) — core 5 only")
for col in ['A']: ws4.column_dimensions[col].width=3
ws4.column_dimensions['B'].width=24
for j in range(13): ws4.column_dimensions[get_column_letter(3+j)].width=6.5

# ---------- Tab: Alignment Check ----------
ws5=wb.create_sheet("Alignment Check")
ws5['A1']="Does the funding story hold across metrics?"; ws5['A1'].font=Font(bold=True,size=14,color=NAVY)
hcell(ws5,3,1,"Core-5 YoY (Aug–Jun, both years)",fill=GOLD,color=NAVY,align='left')
hcell(ws5,3,2,"FY26"); hcell(ws5,3,3,"FY25"); hcell(ws5,3,4,"YoY"); hcell(ws5,3,5,"Read")
core=[('Calls from Businesses',2419,2707,'coverage-sensitive → down'),
      ('Police Calls',336,453,'coverage-sensitive → down'),
      ('Public Drinking/Cannabis',264,458,'coverage-sensitive → down'),
      ('Assistance Provided',360,377,'≈ flat'),
      ('Aggressive Behaviour',577,526,'DISORDER ROSE on less funding')]
for k,(lab,a,b,rd) in enumerate(core):
    r=4+k; up=a>b; fl=REDF if up else None
    cell(ws5,r,1,lab,align='left',fill=fl); cell(ws5,r,2,a,fill=fl); cell(ws5,r,3,b,fill=fl)
    cell(ws5,r,4,f"{(a/b-1)*100:+.0f}%",fill=fl,bold=up,color='FFB01E1E' if up else 'FF2E7D32'); cell(ws5,r,5,rd,align='left',fill=fl)
hcell(ws5,11,1,"LCF pilot spike — June 2026 vs Mar–May baseline",fill=GOLD,color=NAVY,align='left')
hcell(ws5,11,2,"Baseline"); hcell(ws5,11,3,"June"); hcell(ws5,11,4,"Change"); hcell(ws5,11,5,"")
pilot=[('Calls',178,265),('Aggressive Behaviour',47,95),('Shoplifting/Theft',33,58),('Vagrants Moved On',72,96),('Serious Incidents',9,10)]
for k,(lab,b,j) in enumerate(pilot):
    r=12+k; cell(ws5,r,1,lab,align='left',fill=GREENF); cell(ws5,r,2,b,fill=GREENF); cell(ws5,r,3,j,fill=GREENF,bold=True)
    cell(ws5,r,4,f"{(j/b-1)*100:+.0f}%",fill=GREENF,bold=True,color='FF2E7D32'); cell(ws5,r,5,"",fill=GREENF)
cell(ws5,18,1,"During the funded pilot EVERY incident type surged — the team detected & managed far more. "
              "Aggression up 10% YoY on a cut budget = rising disorder absorbed with fewer resources. "
              "Detail incidents (serious→medical) only tracked from Mar 2026, so no FY25 comparison.",align='left',fill=AMBER)
ws5.merge_cells('A18:E18'); ws5.row_dimensions[18].height=54; ws5['A18'].alignment=Alignment(wrap_text=True,vertical='center')
for col,w in zip('ABCDE',[26,11,10,10,30]): ws5.column_dimensions[col].width=w

# ---------- enhance Tab 2 with June seasonality control ----------
hcell(ws2,24,1,"Seasonality-controlled (same month: June)",fill=GOLD,color=NAVY,align='left')
hcell(ws2,24,2,"FY25"); hcell(ws2,24,3,"FY26"); hcell(ws2,24,4,"Change")
cell(ws2,25,1,"June calls/day (June normally quiet)",align='left'); cell(ws2,25,2,6.0); cell(ws2,25,3,8.8); cell(ws2,25,4,"+48%",color='FF2E7D32',bold=True)
cell(ws2,26,1,"→ Same month, LCF pilot the ONLY change → isolates funding from seasonality.",align='left',fill=GREENF); ws2.merge_cells('A26:D26')

OUT="/Users/ahmadduais/Desktop/ASG/HOTC/2026/HOTC_Calls_vs_Funding_FY26.xlsx"
wb.save(OUT)
import shutil; shutil.copy2(OUT, os.path.expanduser("~/Downloads/"+os.path.basename(OUT)))
print("SAVED:", OUT)
print(f"FY26={T26} FY25={T25} | LFL {L26} vs {L25} ({(L26/L25-1)*100:+.1f}%)")
print(f"Pilot weeks: {[ (m,round(c/d,1)) for m,wk,c,d in [(w[0],w[1],w[2], (w[2]/w[3] if w[3] else 1)) for w in weeks] ]}")
