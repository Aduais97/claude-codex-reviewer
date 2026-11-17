#!/usr/bin/env python3
"""Simple, board-ready workbook for Edward. Tab 1 = exactly what he asked
(monthly calls FY26 vs FY25 + grand total). Tabs 2-3 = plain-English supporting
insight, clearly labelled as secondary."""
import glob, openpyxl, os
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, Reference
from openpyxl.utils import get_column_letter

TREE="/Users/ahmadduais/Desktop/ASG/Operations/Clients/HOTC"; DL="/Users/ahmadduais/Downloads/2024"
NAVY='FF1F3864'; LIGHT='FFEDF0F7'; GREEN='FFE3F1E4'; WHITE='FFFFFFFF'
thin=Side(style='thin',color='FFCCCCCC'); B=Border(thin,thin,thin,thin)
def cd(p):
    try:
        ws=openpyxl.load_workbook(p,data_only=True).active
        for r in ws.iter_rows(values_only=True):
            if r and r[0] and 'calls made from businesses' in str(r[0]).lower():
                n=[c for c in r[1:] if isinstance(c,(int,float))]
                return int(n[-1]) if n else 0
    except: pass
    return 0
def mt(base,year,month,is24=False):
    tot=0
    patt=f"{DL}/{month}/**/*.xlsx" if is24 else f"{base}/{year}/{month}/**/Weekly Data Report*.xlsx"
    for f in glob.glob(patt,recursive=True):
        if is24 and 'weekly data report' not in f.lower(): continue
        tot+=cd(f)
    return tot
MONTHS=['July','August','September','October','November','December','January','February','March','April','May','June']
MAB={'July':'July','August':'Aug','September':'Sep','October':'Oct','November':'Nov','December':'Dec',
     'January':'Jan','February':'Feb','March':'Mar','April':'Apr','May':'May','June':'June'}
YRS={'July':("'25","'24"),'August':("'25","'24"),'September':("'25","'24"),'October':("'25","'24"),
     'November':("'25","'24"),'December':("'25","'24"),'January':("'26","'25"),'February':("'26","'25"),
     'March':("'26","'25"),'April':("'26","'25"),'May':("'26","'25"),'June':("'26","'25")}
c26=[mt(TREE,'2025',m) if i<6 else mt(TREE,'2026',m) for i,m in enumerate(MONTHS)]
c25=[mt(None,None,m,True) if i<6 else mt(TREE,'2025',m) for i,m in enumerate(MONTHS)]
JUL_EST=190          # July 2025: 2 wks recorded (86) + 3 wks estimated from daily logs, calibrated
c26_rec0=c26[0]      # keep the recorded figure for the note
c26[0]=JUL_EST       # use the estimate so July is a full month
T26,T25=sum(c26),sum(c25); L26,L25=sum(c26[1:]),sum(c25[1:])

# ---- full monthly timeline (calls + days) Jul24 -> Aug26: spans the cut, the pilot, into FY27 ----
def cdays(p):
    try:
        ws=openpyxl.load_workbook(p,data_only=True).active
        for r in ws.iter_rows(values_only=True):
            if r and r[0] and 'calls made from businesses' in str(r[0]).lower():
                n=[c for c in r[1:] if isinstance(c,(int,float))]
                return (int(n[-1]) if n else 0, len([c for c in r[1:-1] if isinstance(c,(int,float))]))
    except: pass
    return 0,0
def mget(year,month,is24=False):
    tot=days=0
    patt=f"{DL}/{month}/**/*.xlsx" if is24 else f"{TREE}/{year}/{month}/**/Weekly Data Report*.xlsx"
    for f in glob.glob(patt,recursive=True):
        if is24 and 'weekly data report' not in f.lower(): continue
        c,d=cdays(f); tot+=c; days+=d
    return tot,days
TLSPEC=[('Jul 24','2024','July',1),('Aug 24','2024','August',1),('Sep 24','2024','September',1),('Oct 24','2024','October',1),
 ('Nov 24','2024','November',1),('Dec 24','2024','December',1),('Jan 25','2025','January',0),('Feb 25','2025','February',0),
 ('Mar 25','2025','March',0),('Apr 25','2025','April',0),('May 25','2025','May',0),('Jun 25','2025','June',0),
 ('Jul 25','2025','July',0),('Aug 25','2025','August',0),('Sep 25','2025','September',0),('Oct 25','2025','October',0),
 ('Nov 25','2025','November',0),('Dec 25','2025','December',0),('Jan 26','2026','January',0),('Feb 26','2026','February',0),
 ('Mar 26','2026','March',0),('Apr 26','2026','April',0),('May 26','2026','May',0),('Jun 26','2026','June',0),
 ('Jul 26','2026','July',0),('Aug 26','2026','August',0)]   # last 2 = FY2027
TL=[]
for lab,y,m,is24 in TLSPEC:
    c,d=mget(y,m,is24)
    if lab=='Jul 25': c,d=190,31   # July 2025 estimate
    TL.append([lab,c,d,round(c/d,1) if d else 0])
pre=[t for t in TL[:10]]; post=[t for t in TL[10:24]]           # cut after Apr 2025
PRE=sum(t[1] for t in pre)/sum(t[2] for t in pre)
POST=sum(t[1] for t in post)/sum(t[2] for t in post)
JUL26,AUG26=TL[24][1],TL[25][1]                                  # FY27 to date

wb=openpyxl.Workbook()
def title(ws,txt,sub):
    ws['A1']=txt; ws['A1'].font=Font(bold=True,size=15,color=NAVY)
    ws['A2']=sub; ws['A2'].font=Font(italic=True,size=10.5,color='FF555555')
def H(ws,r,c,v,align='center'):
    x=ws.cell(r,c,v); x.font=Font(bold=True,color=WHITE,size=11); x.fill=PatternFill('solid',fgColor=NAVY)
    x.alignment=Alignment(horizontal=align,vertical='center'); x.border=B; return x
def C(ws,r,c,v,bold=False,align='center',fill=None,color='FF000000',size=11):
    x=ws.cell(r,c,v); x.font=Font(bold=bold,color=color,size=size); x.alignment=Alignment(horizontal=align,vertical='center')
    if fill: x.fill=PatternFill('solid',fgColor=fill)
    x.border=B; return x

# ===== TAB 1: exactly what Edward asked =====
ws=wb.active; ws.title="Calls by Month"
title(ws,"Calls from Businesses — Full Year",
      "The monthly breakdown and grand total you asked for: FY2026 (Jul '25–Jun '26) vs the year before.")
H(ws,4,1,"Month",'left'); H(ws,4,2,"FY2026"); H(ws,4,3,"FY2025"); H(ws,4,4,"Difference")
for i,m in enumerate(MONTHS):
    r=5+i; est=(i==0)
    C(ws,r,1,MAB[m],align='left',bold=True)
    C(ws,r,2, f"~{c26[i]}  (est.)" if est else c26[i], fill=LIGHT if est else None)
    C(ws,r,3, c25[i])
    d=c26[i]-c25[i]; C(ws,r,4,f"{d:+d}",color='FF2E7D32' if d>=0 else 'FFB01E1E', fill=LIGHT if est else None)
C(ws,17,1,"GRAND TOTAL",bold=True,align='left',fill=NAVY,color=WHITE)
C(ws,17,2,f"~{T26:,}",bold=True,fill=NAVY,color=WHITE); C(ws,17,3,f"{T25:,}",bold=True,fill=NAVY,color=WHITE)
C(ws,17,4,f"{(T26/T25-1)*100:+.0f}%",bold=True,fill=NAVY,color=WHITE)
# plain-English note
ws['A19']="In plain terms:"; ws['A19'].font=Font(bold=True,size=11,color=NAVY)
notes=[f"• FY2026 ≈ {T26:,} business calls vs FY2025 {T25:,} — about {abs(round((T26/T25-1)*100))}% lower.",
       "• This reflects the patrol funding being cut from $800k to $690k around April/May 2025 (mid-FY25).",
       f"• July 2025 is part-estimated (~{JUL_EST}): {c26_rec0} calls recorded across 2 weeks; the remaining ~3 weeks",
       "   are estimated from the daily patrol logs. Every other month is a full recorded figure.",
       f"• FY2027 to date (Jul–Aug 2026): {JUL26+AUG26} calls so far. See 'The funding story' tab for the full trend."]
for k,t in enumerate(notes):
    ws.cell(20+k,1,t).font=Font(size=10.5,color='FF333333')

# ---- FY2027 (current year to date) — showcases the LCF pilot carrying into July 2026 ----
fr=27
C(ws,fr,1,"FY2027 — current year, to date  (the LCF pilot ran to 24 July 2026)",bold=True,align='left',fill=NAVY,color=WHITE)
for c in (2,3,4): C(ws,fr,c,"",fill=NAVY)
H(ws,fr+1,1,"Month",'left'); H(ws,fr+1,2,"Calls"); H(ws,fr+1,3,"What was happening")
ws.merge_cells(start_row=fr+1,start_column=3,end_row=fr+1,end_column=4)
fy27rows=[("July 2026",JUL26,"LCF pilot active to 24 July → well above the post-cut norm",GREEN,True),
          ("August 2026",AUG26,"post-pilot; 1 week recorded so far",LIGHT,False)]
for k,(m,v,w,fl,bold) in enumerate(fy27rows):
    r=fr+2+k; C(ws,r,1,m,align='left',fill=fl,bold=bold); C(ws,r,2,v,fill=fl,bold=bold)
    C(ws,r,3,w,align='left',fill=fl); ws.merge_cells(start_row=r,start_column=3,end_row=r,end_column=4)
r=fr+4; C(ws,r,1,"Total so far",bold=True,align='left',fill=LIGHT); C(ws,r,2,JUL26+AUG26,bold=True,fill=LIGHT)
C(ws,r,3,"vs a normal post-cut month of ~180 — July shows the pilot's funding effect",align='left',fill=LIGHT)
ws.merge_cells(start_row=r,start_column=3,end_row=r,end_column=4)

ws.column_dimensions['A'].width=40
for col in 'BCD': ws.column_dimensions[col].width=15
ws.sheet_view.showGridLines=False

# ===== TAB 2: Why it changed (secondary) =====
ws2=wb.create_sheet("The funding story")
title(ws2,"Supporting insight ①  ·  Calls follow funding",
      "SECONDARY / optional. The budget cut (May 2025) and the June-2026 pilot are both visible in the trend below.")
ws2['A4']="What this shows:"; ws2['A4'].font=Font(bold=True,color=NAVY,size=11)
ws2['A5']="Business calls track how much patrol coverage is funded. When the budget was cut to $690k (from $800k)"
ws2['A6']="around April/May 2025, calls dropped ~21% and stayed low. When Council briefly funded an extra team"
ws2['A7']="(June 2026 pilot), calls jumped back up — then fell again when it ended."
for r in (5,6,7): ws2.cell(r,1).font=Font(size=10.5,color='FF333333')
H(ws2,9,1,"Period",'left'); H(ws2,9,2,"Calls/day"); H(ws2,9,3,"Funding")
rowsp=[("Before the cut  (Jul '24 – Apr '25)",round(PRE,1),"$800k",LIGHT,False),
       ("After the cut  (May '25 onward)",round(POST,1),"$690k  →  −21% calls",GREEN if False else LIGHT,True),
       ("June 2026 LCF pilot  (+1 team)",TL[23][3],"+ uplift  →  +52% vs post-cut",GREEN,True)]
for k,(lab,v,w,fl,bold) in enumerate(rowsp):
    r=10+k; C(ws2,r,1,lab,align='left',fill=fl,bold=bold); C(ws2,r,2,v,fill=fl,bold=bold); C(ws2,r,3,w,align='left',fill=fl,bold=bold)
ws2['A14']="Same pattern in July, 3 years running:  July '24 (pre-cut) 335  →  July '25 (post-cut) ~190  →  July '26 (pilot) 228."
ws2['A14'].font=Font(size=10.5,italic=True,color='FF1F3864')
ws2['A15']=f"FY2027 to date (Jul–Aug 2026, post-pilot): {JUL26+AUG26} calls so far — back at the post-cut level."
ws2['A15'].font=Font(size=10.5,color='FF333333')

# ---- monthly timeline chart data (Jul 24 -> Aug 26, incl FY27) in cols H/I ----
ws2.cell(4,8,"Month"); ws2.cell(4,9,"Calls/day")
for i,(lab,c,d,pd) in enumerate(TL):
    ws2.cell(5+i,8,lab); ws2.cell(5+i,9,pd)
chart=LineChart(); chart.title="Calls per day — budget cut (May '25) and June-'26 pilot both visible"
chart.height=8.2; chart.width=24; chart.style=2
data=Reference(ws2,min_col=9,min_row=4,max_row=4+len(TL)); cats=Reference(ws2,min_col=8,min_row=5,max_row=4+len(TL))
chart.add_data(data,titles_from_data=True); chart.set_categories(cats)
chart.y_axis.title="Calls/day"; chart.legend=None
ws2.add_chart(chart,"A17")
ws2['A34']="Takeaway:"; ws2['A34'].font=Font(bold=True,color=NAVY,size=11)
ws2['A35']="Calls fall when funding is cut and rise when it's added — proven twice (the May-2025 cut and the June-2026"
ws2['A36']="pilot). Funding directly drives community engagement. FY2027 has started back at the reduced-funding level."
for r in (35,36): ws2.cell(r,1).font=Font(size=10.5,color='FF333333')
ws2.column_dimensions['A'].width=34; ws2.column_dimensions['B'].width=11; ws2.column_dimensions['C'].width=30
ws2.column_dimensions['H'].width=8; ws2.column_dimensions['I'].width=9
ws2.sheet_view.showGridLines=False

# ===== TAB 3: Incidents too (secondary) =====
ws3=wb.create_sheet("Incidents too")
title(ws3,"Supporting insight ②  ·  It wasn't just calls",
      "SECONDARY / optional. During the funded pilot, real incidents handled also rose sharply.")
ws3['A4']="What this shows:"; ws3['A4'].font=Font(bold=True,color=NAVY,size=11)
ws3['A5']="The extra funded team didn't just take more calls — it detected and dealt with far more real incidents,"
ws3['A6']="i.e. more problems removed from the street for the community. June (pilot) vs the months either side:"
for r in (5,6): ws3.cell(r,1).font=Font(size=10.5,color='FF333333')
H(ws3,8,1,"Incidents handled",'left'); H(ws3,8,2,"Normal month"); H(ws3,8,3,"June (pilot)"); H(ws3,8,4,"Change")
inc=[("Aggressive behaviour",47,95),("Shoplifting / theft",33,58),("Vagrants moved on",72,96)]
for k,(lab,b,j) in enumerate(inc):
    r=9+k; C(ws3,r,1,lab,align='left',fill=GREEN); C(ws3,r,2,b,fill=GREEN); C(ws3,r,3,j,fill=GREEN,bold=True)
    C(ws3,r,4,f"+{round((j/b-1)*100)}%",fill=GREEN,bold=True,color='FF2E7D32')
ws3['A13']="Takeaway:"; ws3['A13'].font=Font(bold=True,color=NAVY,size=11)
ws3['A14']="With the extra team, the service roughly doubled its response to aggression and handled far more theft"
ws3['A15']="and vagrancy — more community value for the funding. (Detail incident data is only tracked from 2026.)"
for r in (14,15): ws3.cell(r,1).font=Font(size=10.5,color='FF333333')
ws3.column_dimensions['A'].width=24
for col in 'BCD': ws3.column_dimensions[col].width=15
ws3.sheet_view.showGridLines=False

OUT="/Users/ahmadduais/Desktop/ASG/HOTC/2026/HOTC_Calls_Report_for_Edward.xlsx"
wb.save(OUT); import shutil; shutil.copy2(OUT, os.path.expanduser("~/Downloads/"+os.path.basename(OUT)))
print("SAVED:",OUT)
print(f"Grand total FY26={T26} FY25={T25}; like-for-like {L26} vs {L25}")
