#!/usr/bin/env python3
"""CRL Grand Opening — EVENT guard-hours roster (xlsx). One tab per station.
Officers down the rows (one row per deployed post slot), the activation days across the columns
(Fri pack-in · Fri test run · Sat EVENT DAY · Sun pack-out), planned hours in the cells, blank
Guard-name column to assign real people. Totals reconcile to the sent proposal:
event day 1,518 gh · Friday test run 207 gh · pack-in/out 132 gh · programme 1,857 gh.

Out: ~/Desktop/ASG/Operations/Clients/CRL/CRL_Grand_Opening_Event_Roster.xlsx
"""
import os, math
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L

OUT = os.path.expanduser("~/Desktop/ASG/Operations/Clients/CRL/CRL_Grand_Opening_Event_Roster.xlsx")

NAVY="1E2A3A"; GOLD="C8952A"; LIGHT="EEF2F6"; INPUT="FFF3CD"; EVENT="EAF3ED"; WHITE="FFFFFF"; INK="1F2733"; SUB="5A6675"
thin=Side(style="thin", color="C9D2DC"); B=Border(left=thin,right=thin,top=thin,bottom=thin)
CEN=Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT=Alignment(horizontal="left", vertical="center", indent=1)

# planned hours per activation phase
H_PACKIN=8; H_TEST=3; H_EVENT=11; H_PACKOUT=6
PACKIN_N=4; PACKOUT_N=2   # officers on pack-in / pack-out (supervisors)

# Station: peak, event-day total, ordered post groups (post, officer count)
STATIONS = {
 "Karanga-a-Hape (K Rd)": {"peak":3500, "posts":[
     ("Station Event Manager + Supervisor", 4),
     ("Mercury Lane entry / access control", 6),
     ("Bag-check / screening", 6),
     ("Beresford Square portal & egress", 3),
     ("Platform ends (both caverns)", 5),
     ("Concourse & upstairs roving", 6),
     ("Protest watch / frontage team", 5),
     ("Roving floater / capacity reserve", 9)]},
 "Te Waihorotiu (Aotea)": {"peak":4000, "posts":[
     ("Station Event Manager + Supervisor", 4),
     ("Bledisloe Lane entry / access control", 7),
     ("Bag-check / screening", 7),
     ("Platform ends & mid-platform", 6),
     ("Concourse (ground + upstairs) roving", 7),
     ("Emergency-service access warden", 1),
     ("Egress / evacuation warden", 3),
     ("Roving floater / capacity reserve", 15)]},
 "Maungawhau (Mt Eden)": {"peak":3500, "posts":[
     ("Station Event Manager + Supervisor", 4),
     ("Ground-floor entry / access control", 6),
     ("Bag-check / screening", 6),
     ("Platform — ends + mid-platform egress", 6),
     ("Vent-building / plant-side post", 2),
     ("Nerve-centre / control + concourse", 3),
     ("Egress / evacuation warden", 3),
     ("Roving floater / capacity reserve", 14)]},
}
# day columns: (header, planned hours, fill)
DAYS = [("Fri\nPack-in\n(8h)", H_PACKIN, LIGHT),
        ("Fri\nTest Run\n(3h)", H_TEST, LIGHT),
        ("Sat\nEVENT DAY\n(11h)", H_EVENT, EVENT),
        ("Sun\nPack-out\n(6h)", H_PACKOUT, LIGHT)]

wb=openpyxl.Workbook(); wb.remove(wb.active)
prog=0
for name,d in STATIONS.items():
    posts=d["posts"]; total=sum(n for _,n in posts); test_n=round(total*0.5)
    ws=wb.create_sheet(name[:31]); ws.sheet_view.showGridLines=False
    NC=3+len(DAYS)+1   # Post | Officer | Guard | 4 days | Total
    # title + subtitle
    ws.merge_cells(start_row=1,start_column=1,end_row=1,end_column=NC)
    t=ws.cell(1,1,f"{name.upper()} — Grand Opening Event Roster")
    t.font=Font(name="Arial",size=13,bold=True,color=WHITE); t.fill=PatternFill("solid",fgColor=NAVY)
    t.alignment=Alignment(indent=1,vertical="center"); ws.row_dimensions[1].height=24
    ws.merge_cells(start_row=2,start_column=1,end_row=2,end_column=NC)
    ws.cell(2,1,f"Event Saturday: ____________ (2nd half Q3 2026) · peak {d['peak']:,} patrons · event-day total {total} officers · 1:80 · 11-hour shift · fill the Guard column with the rostered officer").font=Font(name="Arial",size=9,italic=True,color=SUB)
    ws.cell(2,1).alignment=Alignment(indent=1,vertical="center")
    # header
    heads=["Post / Role","#","Guard (assign)"]+[h for h,_,_ in DAYS]+["Total h"]
    for i,h in enumerate(heads,1):
        c=ws.cell(3,i,h); c.font=Font(name="Arial",size=9,bold=True,color=WHITE)
        c.fill=PatternFill("solid",fgColor=NAVY); c.border=B
        c.alignment=Alignment(horizontal="left" if i==1 else "center",vertical="center",wrap_text=True,indent=1 if i==1 else 0)
    ws.row_dimensions[3].height=34
    r=4; slot=0; col_tot=[0]*len(DAYS)
    for post,n in posts:
        for k in range(1,n+1):
            slot+=1
            ws.cell(r,1,post).alignment=LEFT; ws.cell(r,1).font=Font(name="Arial",size=9.5,color=INK)
            ws.cell(r,2,k).alignment=CEN; ws.cell(r,2).font=Font(name="Arial",size=9,color=SUB)
            gn=ws.cell(r,3,""); gn.fill=PatternFill("solid",fgColor=INPUT); gn.alignment=LEFT
            row_tot=0
            for j,(hh,hrs,fill) in enumerate(DAYS):
                col=4+j; val=0
                if j==0 and slot<=PACKIN_N: val=hrs           # pack-in: first N
                elif j==1 and slot<=test_n: val=hrs            # test run: first 50%
                elif j==2: val=hrs                             # event day: everyone
                elif j==3 and slot<=PACKOUT_N: val=hrs         # pack-out: first N
                cell=ws.cell(r,col)
                if val: cell.value=val; cell.font=Font(name="Arial",size=9.5,bold=(j==2),color=INK); row_tot+=val; col_tot[j]+=val
                cell.alignment=CEN; cell.border=B; cell.fill=PatternFill("solid",fgColor=fill if val else WHITE)
            tc=ws.cell(r,NC,row_tot); tc.number_format='0.##'; tc.font=Font(name="Arial",size=9.5,bold=True,color=NAVY)
            tc.alignment=CEN; tc.border=B; tc.fill=PatternFill("solid",fgColor=LIGHT)
            for i in (1,2,3): ws.cell(r,i).border=B
            r+=1
    # totals
    ws.cell(r,1,"STATION TOTAL — guard-hours").font=Font(name="Arial",size=10,bold=True,color=NAVY)
    ws.merge_cells(start_row=r,start_column=1,end_row=r,end_column=3); ws.cell(r,1).alignment=LEFT
    for j in range(len(DAYS)):
        c=ws.cell(r,4+j,col_tot[j]); c.number_format='0.##'; c.font=Font(name="Arial",size=10,bold=True,color=NAVY); c.alignment=CEN
    st_tot=sum(col_tot)
    gt=ws.cell(r,NC,st_tot); gt.number_format='0.##'; gt.font=Font(name="Arial",size=10,bold=True,color=NAVY); gt.alignment=CEN
    for i in range(1,NC+1): ws.cell(r,i).border=B; ws.cell(r,i).fill=PatternFill("solid",fgColor=GOLD)
    r+=1
    # officers-per-day
    ws.cell(r,1,"Officers on shift").font=Font(name="Arial",size=9,bold=True,color=SUB)
    ws.merge_cells(start_row=r,start_column=1,end_row=r,end_column=3); ws.cell(r,1).alignment=LEFT
    heads_n=[PACKIN_N,test_n,total,PACKOUT_N]
    for j,nn in enumerate(heads_n):
        c=ws.cell(r,4+j,nn); c.font=Font(name="Arial",size=9,bold=True,color=SUB); c.alignment=CEN
    for i in range(1,NC+1): ws.cell(r,i).border=B; ws.cell(r,i).fill=PatternFill("solid",fgColor=LIGHT)
    # widths
    ws.column_dimensions["A"].width=34; ws.column_dimensions["B"].width=4; ws.column_dimensions["C"].width=22
    for j in range(len(DAYS)): ws.column_dimensions[L(4+j)].width=10
    ws.column_dimensions[L(NC)].width=9
    ws.freeze_panes="D4"
    prog+=st_tot
    print(f"  {name}: {total} officers · station {st_tot:g} gh  (event {total*H_EVENT}, test {test_n*H_TEST}, pack {PACKIN_N*H_PACKIN+PACKOUT_N*H_PACKOUT})")

wb.save(OUT)
print(f"wrote {OUT}")
print(f"  programme total: {prog:g} guard-hours  (proposal = 1,857)")
