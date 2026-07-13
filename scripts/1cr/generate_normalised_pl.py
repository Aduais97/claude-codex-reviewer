#!/usr/bin/env python3
"""Exact 1:1 recreation of the vendor's Xero FY26 Profit and Loss (same title, every line in
Xero's order incl. 0.00 lines, 2026 + 2025), in Xero's plain look. Lines marked * are the
normalisation adjustments, reconciled to Normalised EBITDA in the notes block at the end."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

OUT = "/Users/ahmadduais/Desktop/Acquisitions/1st-Call-Recruitment/1CR_Normalised_PL_FY26.pdf"
NAVY = HexColor("#13294B"); GREY = HexColor("#5A6470"); FAINT = HexColor("#E4E7EC"); RULE = HexColor("#9AA3AF")
S = getSampleStyleSheet()
TITLE = ParagraphStyle("T", parent=S["Normal"], fontName="Helvetica-Bold", fontSize=15, leading=18)
SUB = ParagraphStyle("Sub", parent=S["Normal"], fontName="Helvetica", fontSize=9, leading=12)
NOTE = ParagraphStyle("N", parent=S["Normal"], fontName="Helvetica", fontSize=7.8, textColor=GREY, leading=10.2)
NH = ParagraphStyle("NH", parent=S["Normal"], fontName="Helvetica-Bold", fontSize=9.5, textColor=NAVY, spaceBefore=8, spaceAfter=3)

def m(x):
    if abs(x) < 0.005: return "0.00"
    return f"({abs(x):,.2f})" if x < 0 else f"{x:,.2f}"

SECTIONS = [
 ("Trading Income", [
  ("Consulting Income",323053.77,498335.87),("Sales - Safety Gear",0.00,-140.26),
  ("Temping Income",12443358.76,17500154.75),("Temping Sales Accrual",-126372.34,-108274.20)],
  ("Total Trading Income",12640040.19,17890076.16)),
 ("Cost of Sales", [
  ("ACC 1st Week paid",2887.44,7349.93),("Allowance - non taxable",233.55,2905.03),
  ("Closing stock - safety gear",-20000.00,-20000.00),("Closing stock - stock to oncharge",0.00,0.00),
  ("COGs - safety Gear",0.00,-192.87),("Consulting expense",31.29,0.00),
  ("Holiday Pay Accrual *",-154913.79,-268156.29),("Internationals - cash advances",0.00,0.00),
  ("Internationals - domestic travel",160.72,0.00),("Internationals - overseas travel",2319.68,4627.00),
  ("Internationals - tools + setup expenses",-2955.00,-742.00),("Leave pays",637145.69,1068899.10),
  ("Medical / Drug Testing - tempin",7321.56,23042.63),("Miscellaneous payment",-3320.85,-1170.30),
  ("Opening stock - Safety gear",20000.00,27746.46),("Opening stock to oncharge",0.00,0.00),
  ("Personal Protection Safety Gear",-8694.50,-17237.01),("PPE Gear - closing stock",-45795.50,-45970.17),
  ("PPE Gear - opening stock",45970.17,51728.12),("Rebate - Downers",0.00,0.00),
  ("Staff Testing/Courses:Training",413.26,-208.64),("Stat Day pays",225120.12,344646.59),
  ("Stock to oncharge - purchase",0.00,0.00),("Temp pays - Covid 19",0.00,0.00),
  ("Temping Pays",9137425.57,12527372.15),("Temping Pays Accrual *",-40276.54,40276.54),
  ("Temps Kiwisaver Employer Contribution",107477.68,237384.01)],
  ("Total Cost of Sales",9910550.55,13982300.28)),
 ("Other Income", [
  ("Construct safe course",0.00,860.87),("Covid 19 wage subsidy - perm",0.00,0.00),
  ("Covid 19 wage subsidy - temps",0.00,0.00),("Depreciation recovered on disposal of fixed assets *",22151.76,18535.31),
  ("Interest received - current account",0.00,0.00),("Interest received - TMNZ *",0.00,15150.00),
  ("Interest received - Van Syp Investments Limited *",0.00,7319.75),("Interest received - Van Syp Trust *",0.00,99466.92),
  ("Loss on disposal of fixed assets *",0.00,-29442.09),("Rent Received *",50000.04,12681.17),
  ("Resurgence support payment",0.00,0.00)],
  ("Total Other Income",72151.80,124571.93)),
 ("Operating Expenses", [
  ("ACC Levies",112374.33,245995.67),("Acc Levies: Doctor ACC Surcharge",191.30,47.83),
  ("Advertising",0.00,305.00),("Advertising:Marketing",714.08,7681.26),("Advertising:Online",78443.56,92219.49),
  ("Bad Debts Written Off",0.00,0.00),("Bank: Interest Expense *",28655.11,17.49),
  ("Bank: Interest expense - TMNZ",0.00,0.00),("Bank: Service Charges",16903.46,8230.28),
  ("Computer:Computer Hardware",3408.63,503.75),("Computer:Computer Repairs",0.00,152.50),
  ("Computer:Computer Software",68751.58,88689.49),("Computer:IT Development",0.00,0.00),
  ("Contract settlement paid",0.00,1000.00),("Customer Relations - 50% deductible",884.96,1150.82),
  ("Customer Relations:Gifts & Donations",0.00,0.00),("Customer Relations:Non-deductible",0.00,0.00),
  ("Depreciation *",11815.35,151153.24),("Dues and Subscriptions",2695.11,3588.12),
  ("Entertainment:Entertainment Non-Deductible",0.00,4120.53),("FBT *",42975.11,82835.09),
  ("Income Tax Expense",0.00,0.00),("Insurance",53640.33,62331.23),("Insurance - Employee medical",0.00,8765.41),
  ("IT Services",0.00,186.98),("Lease - corporate",0.00,0.00),("Low value assets",0.00,0.00),
  ("Marac Finance - Vehicle Lease:UDC Finance - Vehicle Lease",0.00,0.00),("Motor Expense",-5796.15,7529.48),
  ("Motor Expense:Parking Fines - Non-deductible",95.65,150.00),("Motor Expense:Petrol/Diesel",14237.17,27625.25),
  ("Motor Expense:Registration",1779.77,2059.80),("Motor Expense:Road User",37.04,623.30),
  ("Motor Expense:Tyres",430.43,1897.23),("Motor Expense:WOF/Service",5943.29,4569.40),
  ("Office Expense",31501.41,60668.88),("Office Expense:Cafeteria expense",1059.20,1330.57),
  ("Office Expense:Cleaning",7421.28,17504.46),("Office Expense:Lease's - Phone & Computer",0.00,0.00),
  ("Office Expense:Lease's - Phone & Computer:Photocopier Lease",12742.23,21354.46),
  ("Office Expense:Repairs and maintenance",5642.52,8545.30),("Office Expense:Rubbish Disposal",3888.74,9052.19),
  ("Office Expense:Security",0.00,526.74),("Office Expense:Stationery",621.34,2246.60),
  ("Postage and Delivery",613.17,1571.52),("Professional Fees",405.14,2840.13),
  ("Professional Fees:Accounting",51213.02,29458.20),("Professional Fees:Legal Fees",9309.73,14392.71),
  ("Professional Fees:Working In Fees",0.00,0.00),("R & D tax credit incentive",0.00,0.00),
  ("Rent *",369238.96,527315.52),("Rubbish",0.00,0.00),("Salary staff - leave",35976.13,248259.13),
  ("Shareholder bonus",0.00,0.00),("Shareholder Salaries PAYE *",385000.00,705000.83),
  ("Staff Amenities",0.00,0.00),("Staff Conference",0.00,0.00),("Staff Entertainment",0.00,1506.30),
  ("Staff entertainment - 50% deductible",2939.29,1449.45),("Staff Entertainment:Staff Event",0.00,0.00),
  ("Staff Entertainment:Staff Gifts",843.41,173.92),("Staff Entertainment:Staff Meals",83.85,738.29),
  ("Staff Testing & Courses",-108.70,0.00),("Telephone",23762.80,53921.36),("Telephone:Mobile",17644.70,27774.32),
  ("Travel",5553.60,344.10),("Travel:Accomodation",12726.23,6287.25),("Travel:Meals",1182.11,1092.93),
  ("Travel:Overseas - 100% Deductible",0.00,1691.20),("Travel:Overseas Travel",3835.75,2014.61),
  ("Travel:Travel",308.98,6637.34),("Uniforms",0.00,0.00),("Utilities:Power",24012.24,39435.69),
  ("Utilities:Water",89.09,746.40),("Wages",506220.55,924869.43),("Wages - Covid 19",0.00,0.00),
  ("Wages - Holiday Pay Accrual *",-59958.76,-58080.45),("Wages:Contractors",7156.61,20853.36),
  ("Wages:Kiwisaver Employer Contribution",19679.86,50210.06),("Wages:Non tax payout",0.00,0.00),
  ("Wages:Staff Bonus",1279.80,22156.25),("Wages:Wages - Administration",133652.87,300859.32),
  ("Wages:Wages - IT *",116614.47,248134.70),("Wages:Wages - Management",485047.77,489206.85)],
  ("Total Operating Expenses",2655379.50,4595518.56)),
]

def build_section(title, rows, total):
    data = [[title, "2026", "2025"]] + [[l, m(a), m(b)] for l, a, b in rows] + [[total[0], m(total[1]), m(total[2])]]
    n = len(data) - 1
    t = Table(data, colWidths=[110*mm, 31*mm, 31*mm], repeatRows=1)
    t.setStyle(TableStyle([
        ("FONT",(0,0),(-1,-1),"Helvetica",7.7),("ALIGN",(1,0),(2,-1),"RIGHT"),
        ("TOPPADDING",(0,0),(-1,-1),1.4),("BOTTOMPADDING",(0,0),(-1,-1),1.6),
        ("FONT",(0,0),(-1,0),"Helvetica-Bold",8.6),("LINEBELOW",(0,0),(-1,0),0.7,colors.black),
        ("LINEBELOW",(0,1),(-1,n-1),0.25,FAINT),
        ("FONT",(0,n),(-1,n),"Helvetica-Bold",8),("LINEABOVE",(0,n),(-1,n),0.5,colors.black),
        ("LINEBELOW",(0,n),(-1,n),0.5,colors.black),("TOPPADDING",(0,n),(-1,n),3),("BOTTOMPADDING",(0,n),(-1,n),3),
    ]))
    return t

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=15*mm, bottomMargin=13*mm)
E = [Paragraph("Profit and Loss", TITLE),
     Paragraph("JCR 2006 Limited trading as 1st Call Recruitment", SUB),
     Paragraph("For the year ended 31 March 2026 &nbsp;—&nbsp; Normalised (buyer / maintainable-earnings basis)", SUB),
     Paragraph("Lines marked <b>*</b> are removed or adjusted to reach maintainable earnings — reconciled in the Normalisation block below.", NOTE),
     Spacer(1, 7)]
for title, rows, total in SECTIONS:
    E.append(build_section(title, rows, total)); E.append(Spacer(1, 5))
    if title == "Cost of Sales":
        gp = Table([["Gross Profit", m(2729489.64), m(3907775.88)]], colWidths=[110*mm,31*mm,31*mm])
        gp.setStyle(TableStyle([("FONT",(0,0),(-1,0),"Helvetica-Bold",9),("ALIGN",(1,0),(2,0),"RIGHT"),
            ("LINEABOVE",(0,0),(-1,0),0.8,colors.black),("LINEBELOW",(0,0),(-1,0),0.8,colors.black),
            ("TOPPADDING",(0,0),(-1,0),3.5),("BOTTOMPADDING",(0,0),(-1,0),3.5)]))
        E.append(gp); E.append(Spacer(1, 5))
nprof = Table([["Net Profit", m(146261.94), m(-563170.75)]], colWidths=[110*mm,31*mm,31*mm])
nprof.setStyle(TableStyle([("FONT",(0,0),(-1,0),"Helvetica-Bold",9.5),("ALIGN",(1,0),(2,0),"RIGHT"),
    ("LINEABOVE",(0,0),(-1,0),1,colors.black),("LINEBELOW",(0,0),(-1,0),1,colors.black),
    ("TOPPADDING",(0,0),(-1,0),4),("BOTTOMPADDING",(0,0),(-1,0),4)]))
E.append(nprof)

# ---- Normalisation block ----
E.append(Spacer(1, 10))
E.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=5))
E.append(Paragraph("Normalisation — FY26 (maintainable earnings)", NH))
bridge = [
 ("Net Profit (reported)", 146261.94, ""),
 ("Add back — owner & non-continuing:", None, ""),
 ("   Shareholder Salaries PAYE (absentee owner)", 385000.00, ""),
 ("   Wages - IT (not required post-acquisition)", 116614.47, ""),
 ("   Rent - non-continuing portion (of $369,239; ~$294K continues)", 75000.00, ""),
 ("   FBT - owner-vehicle portion (of $42,975)", 30000.00, ""),
 ("Add back — below EBITDA:", None, ""),
 ("   Bank Interest Expense (debt stays with vendor)", 28655.11, ""),
 ("   Depreciation", 11815.35, ""),
 ("Remove — non-operating income:", None, ""),
 ("   Total Other Income", -72151.80, ""),
 ("Remove — non-cash accrual releases (balance-sheet provision unwinds):", None, ""),
 ("   Holiday Pay Accrual (Cost of Sales)", -154913.79, ""),
 ("   Temping Pays Accrual (Cost of Sales)", -40276.54, ""),
 ("   Wages - Holiday Pay Accrual (Operating Expenses)", -59958.76, ""),
 ("Normalised EBITDA", 466044.08, "3.69%"),
 ("   less KiwiSaver under-accrual (1.18% vs 1.89% — DD-contingent)", -65000.00, ""),
 ("Normalised EBITDA - fully loaded", 401044.08, "3.17%"),
]
bd = [[l, m(v) if v is not None else "", p] for l, v, p in bridge]
bt = Table(bd, colWidths=[122*mm, 28*mm, 14*mm])
stt = [("FONT",(0,0),(-1,-1),"Helvetica",8),("ALIGN",(1,0),(2,-1),"RIGHT"),
       ("TOPPADDING",(0,0),(-1,-1),1.7),("BOTTOMPADDING",(0,0),(-1,-1),1.7)]
for i,(l,v,p) in enumerate(bridge):
    if v is None: stt += [("FONT",(0,i),(-1,i),"Helvetica-Bold",7.8),("TEXTCOLOR",(0,i),(-1,i),GREY)]
    if l.startswith("Normalised EBITDA"):
        stt += [("FONT",(0,i),(-1,i),"Helvetica-Bold",8.5),("LINEABOVE",(0,i),(-1,i),0.5,RULE),("TEXTCOLOR",(0,i),(-1,i),NAVY)]
    if l == "Normalised EBITDA - fully loaded":
        stt += [("BACKGROUND",(0,i),(-1,i),NAVY),("TEXTCOLOR",(0,i),(-1,i),colors.white),
                ("FONT",(0,i),(-1,i),"Helvetica-Bold",9.5),("TOPPADDING",(0,i),(-1,i),4),("BOTTOMPADDING",(0,i),(-1,i),4)]
bt.setStyle(TableStyle(stt))
E.append(bt)
E.append(Spacer(1, 5))
E.append(Paragraph("<b>Maintainable Gross Profit</b> (gross profit less the two Cost-of-Sales accrual releases) = <b>$2,534,299 = 20.05%</b>. Reported GP 21.59% is flattered by those releases.", NOTE))
E.append(Paragraph("<b>Reviewed and KEPT</b> (correctly not adjusted): Temping Sales Accrual (recurring revenue contra); inventory opening/closing stock (safety gear net $0, PPE gear net ~$175); bank service charges; immaterial COGS credits (Internationals tools/setup, staff-testing). FY25 Other Income included $121,937 of related-party interest (Van Syp) — an owner-extraction tell.", NOTE))

doc.build(E)
print("Wrote", OUT)
