#!/usr/bin/env python3
"""Woolworths Primary Connect DC Security (523941) - full cost showcase + true-margin
reconciliation. Shows every cost line in $/hr for Standard and Supervisor guards, then
reconciles the quoted markup down to realistic net margin after costs not in the per-hour
rate (corporate overhead, working-capital financing, slippage/unbilled, penalty/bad-debt).

Usage: .venv/bin/python build_cost_analysis.py <out.xlsx>
"""
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

NAVY="1B2A4A"; GOLD="D4A843"; ALT="F2F4F8"; LIGHT="E8EDF5"; YELLOW="FFF2CC"; TOTAL="DCE6F1"
BORDER=Side(style="thin",color="D0D5DD")
WHITE=Font(color="FFFFFF",bold=True,size=10)

def compute(base, stat_pct, margin_pct, op):
    stat = base*stat_pct
    d8 = base+stat
    al=0.08*d8; sick=0.035*d8; bereav=0.003*d8
    acc=0.009*(d8+al+sick+bereav); kiwi=0.035*(d8+al+sick+bereav)
    other_lv=0.002*d8
    direct=al+sick+bereav+acc+kiwi+other_lv
    training=op["training"]*d8; uniform=op["uniform"]*d8; opsmgmt=op["opsmgmt"]*d8
    equip=op["equip"]*d8; admin=op["admin"]*d8; other=op["other"]*d8
    operating=training+uniform+opsmgmt+equip+admin+other
    cost=d8+direct+operating
    margin=margin_pct*cost
    rate=cost+margin
    return dict(base=base,stat=stat,al=al,sick=sick,bereav=bereav,acc=acc,kiwi=kiwi,
                other_lv=other_lv,training=training,uniform=uniform,opsmgmt=opsmgmt,
                equip=equip,admin=admin,other=other,cost=cost,margin=margin,rate=rate)

OP=dict(training=0.035,uniform=0.015,opsmgmt=0.06,equip=0.015,admin=0.025,other=0.02)
STD=compute(27.50,0.06,0.11,OP)
SUP=compute(31.00,0.06,0.11,OP)

def main(out):
    wb=Workbook(); wb.remove(wb.active)
    # ---------------- Sheet 1: per-hour build ----------------
    ws=wb.create_sheet("Per-Hour Cost Build")
    ws.sheet_view.showGridLines=False
    ws["B2"]="Full Charge-Rate Cost Breakdown - every dollar in the rate"
    ws["B2"].font=Font(bold=True,size=14,color=NAVY)
    ws["B3"]="Standard and Supervisor guard, per hour. ASG recommended draft build (base $27.50 / $31.00)."
    ws["B3"].font=Font(italic=True,size=9,color="4A4A5A")
    hdr=["Cost component","Standard $/hr","% of rate","Supervisor $/hr","% of rate"]
    for i,h in enumerate(hdr):
        c=ws.cell(5,2+i,h); c.font=WHITE; c.fill=PatternFill("solid",fgColor=NAVY)
        c.alignment=Alignment(horizontal="center" if i else "left",vertical="center",wrap_text=True)
        c.border=Border(bottom=Side(style="medium",color=GOLD))
    rows=[
        ("1. Base wage paid to the guard","base",False),
        ("2. Statutory holidays (12 days, built for 24/7)","stat",False),
        ("3. Annual leave","al",False),
        ("   Sick leave","sick",False),
        ("   Bereavement leave","bereav",False),
        ("   ACC levy","acc",False),
        ("   KiwiSaver (employer)","kiwi",False),
        ("   Other leave","other_lv",False),
        ("4. Training (40-hr induction, first aid, refreshers)","training",False),
        ("   Uniform & PPE (hi-vis, AS/NZS boots, wet-weather)","uniform",False),
        ("   Operational management (account mgr, ops, dispatch)","opsmgmt",False),
        ("   Equipment (radios, phones, torches, panic, GTMS)","equip",False),
        ("   Admin (payroll, licensing, COA renewals, back office)","admin",False),
        ("   Other (relief-pool carry, SEDEX/SMETA audits)","other",False),
        ("TOTAL COST (what it costs ASG to deliver)","cost",True),
        ("Margin / markup (11% on cost)","margin",True),
        ("BILLING RATE TO WOOLWORTHS","rate",True),
    ]
    r=6
    for label,key,strong in rows:
        ws.cell(r,2,label)
        ws.cell(r,3,round(STD[key],2)).number_format='"$"#,##0.00'
        ws.cell(r,4,STD[key]/STD["rate"]).number_format='0.0%'
        ws.cell(r,5,round(SUP[key],2)).number_format='"$"#,##0.00'
        ws.cell(r,6,SUP[key]/SUP["rate"]).number_format='0.0%'
        fill = TOTAL if strong else (ALT if r%2==0 else "FFFFFF")
        for col in range(2,7):
            cell=ws.cell(r,col)
            cell.border=Border(left=BORDER,right=BORDER,top=BORDER,bottom=BORDER)
            if fill!="FFFFFF": cell.fill=PatternFill("solid",fgColor=fill)
            if strong: cell.font=Font(bold=True,size=10)
            else: cell.font=Font(size=9.5)
        r+=1
    ws.column_dimensions["B"].width=52
    for col in "CDEF": ws.column_dimensions[col].width=15
    note=ws.cell(r+1,2,"Note: the 11% margin is a MARK-UP ON COST. As a share of the billing rate it is 9.9% "
                 "of revenue - not 11%. And 9.9% is GROSS: see the 'True Margin' tab for what ASG actually keeps.")
    note.font=Font(italic=True,size=9,color="B42318"); note.alignment=Alignment(wrap_text=True)
    ws.merge_cells(start_row=r+1,start_column=2,end_row=r+2,end_column=6)

    # ---------------- Sheet 2: true margin ----------------
    ws2=wb.create_sheet("True Margin Reconciliation")
    ws2.sheet_view.showGridLines=False
    ws2["B2"]="What the margin actually nets to"
    ws2["B2"].font=Font(bold=True,size=14,color=NAVY)
    ws2["B3"]=("The 9.9% gross margin funds real costs that are NOT in the per-hour rate. "
               "After those, the retained net margin is far thinner. Yellow cells are editable assumptions.")
    ws2["B3"].font=Font(italic=True,size=9,color="4A4A5A")

    # national revenue & gross margin (from the build)
    sup_hrs=436*52; std_hrs=1620*52
    revenue=sup_hrs*SUP["rate"]+std_hrs*STD["rate"]
    gross=sup_hrs*SUP["margin"]+std_hrs*STD["margin"]

    def block(ws2, start, title, revenue, gross):
        r=start
        c=ws2.cell(r,2,title); c.font=Font(bold=True,size=11,color="2C3E6B"); r+=1
        hdr=["Line","% of revenue","$ per year"]
        for i,h in enumerate(hdr):
            cell=ws2.cell(r,2+i,h); cell.font=WHITE; cell.fill=PatternFill("solid",fgColor=NAVY)
            cell.alignment=Alignment(horizontal="left" if i==0 else "right")
            cell.border=Border(bottom=Side(style="medium",color=GOLD))
        r+=1
        def line(lbl,pct,amt,strong=False,yellow=False,red=False):
            nonlocal r
            ws2.cell(r,2,lbl)
            if pct is not None:
                ws2.cell(r,3,pct).number_format='0.0%'
            ws2.cell(r,4,round(amt)).number_format='"$"#,##0'
            for col in range(2,5):
                cell=ws2.cell(r,col); cell.border=Border(left=BORDER,right=BORDER,top=BORDER,bottom=BORDER)
                cell.font=Font(bold=strong,size=9.5, color=("B42318" if red else "1A1A2E"))
                if strong: cell.fill=PatternFill("solid",fgColor=TOTAL)
                elif yellow: cell.fill=PatternFill("solid",fgColor=YELLOW)
            r+=1
        line("Contract revenue",1.0,revenue,strong=True)
        line("Gross margin quoted (markup on cost)",gross/revenue,gross,strong=True)
        # below-the-line costs
        oh=0.020*revenue; fin=0.013*revenue; slip=0.020*revenue; cont=0.015*revenue
        line("Less: corporate/group overhead not in rate (exec, office, group IT, group insurance)",0.020,-oh,yellow=True)
        line("Less: working-capital financing (~$600k cash gap funded)",0.013,-fin,yellow=True)
        line("Less: slippage / unbilled hours / roster inefficiency",0.020,-slip,yellow=True)
        line("Less: KPI penalties + bad debt + training-attrition contingency",0.015,-cont,yellow=True)
        net=gross-oh-fin-slip-cont
        line("NET MARGIN ASG actually keeps",net/revenue,net,strong=True,red=(net/revenue<0.05))
        return r

    nr=block(ws2,5,"NATIONAL - all 6 DCs (2,056 hrs/wk)",revenue,gross)
    # Auckland-3
    a_sup=184*52; a_std=864*52
    a_rev=a_sup*SUP["rate"]+a_std*STD["rate"]
    a_gross=a_sup*SUP["margin"]+a_std*STD["margin"]
    block(ws2,nr+2,"AUCKLAND-3 fallback (ARDC+ANDC+AFDC, 1,048 hrs/wk)",a_rev,a_gross)

    ws2.column_dimensions["B"].width=62
    ws2.column_dimensions["C"].width=15
    ws2.column_dimensions["D"].width=16

    foot=ws2.cell(nr+11,2,"Bottom line: a quoted 11% markup (9.9% of revenue) realistically nets ~3% after the "
                  "real costs above. If you want a genuine double-digit NET margin, the rate has to go UP, not "
                  "down - or these below-the-line costs have to be driven out of the business. The below-the-line "
                  "% assumptions are editable; tell me your real numbers and I will re-fit.")
    foot.font=Font(italic=True,size=9,color="B42318"); foot.alignment=Alignment(wrap_text=True)
    ws2.merge_cells(start_row=nr+11,start_column=2,end_row=nr+13,end_column=4)

    wb.save(out)
    print(f"Written: {out}")
    print(f"Std cost ${STD['cost']:.2f} margin ${STD['margin']:.2f} rate ${STD['rate']:.2f}")
    print(f"National revenue ${revenue:,.0f} gross margin ${gross:,.0f} ({gross/revenue:.1%})")
    net=gross-0.068*revenue
    print(f"Net after ~6.8% below-line ≈ ${net:,.0f} ({net/revenue:.1%})")

if __name__=="__main__":
    main(sys.argv[1])
