#!/usr/bin/env python3
"""Build HOTC Weekly Data Reports for June Wk2 (8-14) and Wk3 (15-20) from hand-classified
narrative daily reports (no structured Incident Metrics block). Dual-saves to canonical + source."""
import openpyxl, datetime, os
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
METRICS=['Calls Made From Businesses','Police Calls','Aggressive Behaviour','Public Drinking/Cannabis',
 'Assistance Provided','Serious Incidents','Arrests','Injuries Reported','Vagrants Moved On',
 'Shoplifting/Theft','Intoxicated Persons','Medical Responses']
ROUTES=[('Alpha',3),('Bravo/Beta',2),('Charlie',2),('Delta',3)]
def m(*v): return dict(zip(METRICS,v))
# (calls,police,aggr,drink,assist,serious,arrests,inj,vagr,theft,intox,med)
DATA={
 # Week 2 (8-10 = previously validated; 11-14 = new hand-classification)
 datetime.date(2026,6,8):  m(10,1,4,1,1,1,0,0,3,0,1,0),
 datetime.date(2026,6,9):  m(8, 2,2,0,1,2,1,0,5,0,0,0),
 datetime.date(2026,6,10): m(7, 0,1,1,1,0,0,0,4,1,0,0),
 datetime.date(2026,6,11): m(8, 2,2,0,1,0,1,0,4,2,2,0),
 datetime.date(2026,6,12): m(12,1,2,1,1,1,0,0,6,2,1,1),
 datetime.date(2026,6,13): m(5, 1,3,0,1,1,0,0,1,0,1,0),
 datetime.date(2026,6,14): m(4, 1,2,0,1,0,0,0,1,2,0,0),
 # Week 3 (15-20; no Sunday 21 report supplied)
 datetime.date(2026,6,15): m(12,1,3,0,1,0,0,0,6,4,0,0),
 datetime.date(2026,6,16): m(8, 1,2,0,1,1,0,0,1,5,0,0),
 datetime.date(2026,6,17): m(8, 1,3,1,1,1,0,0,3,0,2,0),
 datetime.date(2026,6,18): m(12,1,3,0,1,0,0,0,3,3,0,0),
 datetime.date(2026,6,19): m(4, 0,1,0,1,0,0,0,1,1,0,0),
 datetime.date(2026,6,20): m(5, 0,2,0,1,0,0,0,1,1,2,0),
}
WEEKS={'Week 2 8th June - 14th June':[datetime.date(2026,6,d) for d in range(8,15)],
       'Week 3 15th June - 21st June':[datetime.date(2026,6,d) for d in range(15,21)]}
DAYN=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']; ORD={1:'st',2:'nd',3:'rd'}
def ordn(d): return f"{d}{ORD.get(d if d<20 else d%10,'th')}"
THIN=Side(style='thin',color='BBBBBB'); BORDER=Border(left=THIN,right=THIN,top=THIN,bottom=THIN)
HEADFILL=PatternFill('solid',fgColor='1F3864'); TOTFILL=PatternFill('solid',fgColor='FCE4D6')
DESTS=['/Users/ahmadduais/Desktop/ASG/Operations/Clients/HOTC/2026/June',
       '/Users/ahmadduais/Desktop/hotc reports/extracted/June']
def build(weekfolder,dates):
    wb=openpyxl.Workbook(); ws=wb.active; ws.title='Weekly Data Report'
    ws.cell(1,1,f"HOTC Weekly Data Report — {weekfolder}").font=Font(bold=True,size=13,color='1F3864')
    hdr=['Metric']+[f"{DAYN[d.weekday()]} {ordn(d.day)}" for d in dates]+['Total']
    for j,h in enumerate(hdr,1):
        c=ws.cell(3,j,h); c.font=Font(bold=True,color='FFFFFF'); c.fill=HEADFILL; c.alignment=Alignment(horizontal='center'); c.border=BORDER
    r=4
    for met in METRICS:
        ws.cell(r,1,met).border=BORDER; tot=0
        for j,d in enumerate(dates,2):
            v=DATA[d][met]; tot+=v
            cc=ws.cell(r,j, v if v else None); cc.alignment=Alignment(horizontal='center'); cc.border=BORDER
        tc=ws.cell(r,2+len(dates),tot); tc.font=Font(bold=True); tc.alignment=Alignment(horizontal='center'); tc.fill=TOTFILL; tc.border=BORDER
        r+=1
    r+=1; ws.cell(r,1,'Patrol Route Coverage').font=Font(bold=True,size=12,color='1F3864'); r+=1
    for j,h in enumerate(['Route']+[f"{DAYN[d.weekday()]} {ordn(d.day)}" for d in dates]+['Total'],1):
        c=ws.cell(r,j,h); c.font=Font(bold=True,color='FFFFFF'); c.fill=HEADFILL; c.alignment=Alignment(horizontal='center'); c.border=BORDER
    r+=1
    for name,per in ROUTES:
        ws.cell(r,1,name).border=BORDER
        for j,d in enumerate(dates,2):
            c=ws.cell(r,j,per); c.alignment=Alignment(horizontal='center'); c.border=BORDER
        tc=ws.cell(r,2+len(dates),per*len(dates)); tc.font=Font(bold=True); tc.alignment=Alignment(horizontal='center'); tc.fill=TOTFILL; tc.border=BORDER
        r+=1
    ws.column_dimensions['A'].width=28
    for j in range(2,3+len(dates)): ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width=9
    for base in DESTS:
        outdir=os.path.join(base,weekfolder); os.makedirs(outdir,exist_ok=True)
        wb.save(os.path.join(outdir,'Weekly Data Report.xlsx'))
    return {met:sum(DATA[d][met] for d in dates) for met in METRICS}
for wf,dates in WEEKS.items():
    t=build(wf,dates)
    print(f"### {wf} ({len(dates)} days)")
    print("   "+" | ".join(f"{k.split('/')[0][:12]}={t[k]}" for k in METRICS if t[k]))
