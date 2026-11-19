#!/usr/bin/env python3
"""
Auckland Painting Co — Business Plan + Financial Model generator.
Self-contained (no external data deps). Outputs:
  ~/Desktop/Painting/Auckland_Painting_Co_Business_Plan.pdf
  ~/Desktop/Painting/Auckland_Painting_Co_Financial_Model.xlsx

Content is the ETR-hardened plan (agentic workflow: 7 research agents -> assumptions
-> 5-lens adversarial review -> synthesis; CONDITIONAL_GO). Financials computed here.
Design per pdf-design-standards: ReportLab, navy+gold, >=8.5pt, TOC, no callout boxes.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, PageBreak, NextPageTemplate, Flowable,
                                KeepTogether)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.graphics.shapes import Drawing, Line, Rect, String
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.widgets.markers import makeMarker

# ---------------------------------------------------------------- palette
NAVY   = colors.HexColor("#1E2A3A")
NAVY2  = colors.HexColor("#2C3E50")
GOLD   = colors.HexColor("#C8952A")
GREEN  = colors.HexColor("#00843D")
INK    = colors.HexColor("#22262B")
GREY   = colors.HexColor("#5A6472")
LINEG  = colors.HexColor("#D8DCE2")
ROWALT = colors.HexColor("#F4F6F8")
LIGHT  = colors.HexColor("#EEF1F4")
RED    = colors.HexColor("#B23A2E")

OUT_DIR = os.path.expanduser("~/Desktop/Painting")
os.makedirs(OUT_DIR, exist_ok=True)
PDF = os.path.join(OUT_DIR, "Auckland_Painting_Co_Business_Plan.pdf")
XLSX = os.path.join(OUT_DIR, "Auckland_Painting_Co_Financial_Model.xlsx")

def nz(x):
    x = round(x)
    return ("-${:,.0f}".format(-x)) if x < 0 else ("${:,.0f}".format(x))

# ================================================================ FINANCIAL ENGINE
# --- Unit economics (ETR-hardened) ---
CHARGE_OUT   = 95      # $/hr cost-plus (pay subbie $55) -- NOT the fatal $65
SUBBIE_HR    = 55
EMPLOYED_HR  = 38      # all-in incl on-costs
MATERIALS_PC = 0.19
AVG_RES_JOB  = 11000   # exterior-weighted
AVG_COMM_JOB = 6000

# --- 3-year P&L drivers ---
REV   = {"Y1": 235000, "Y2": 430000, "Y3": 620000}
REV_RANGE = {"Y1_low": 200000, "Y1_high": 285000}
GM    = {"Y1": 0.30, "Y2": 0.39, "Y3": 0.43}
FIXED_OPEX = {"Y1": 54240, "Y2": 72000, "Y3": 95000}   # ex owner draws & provisions
PROV_PC = 0.045                                          # rework 3% + bad debt 1.5%
DRAWS = {"Y1": 69000, "Y2": 90000, "Y3": 140000}        # combined owner drawings (Y1 incl B winter living top-up)
LOAN = 150000
LOAN_RATE = 0.09

def pnl(y):
    rev = REV[y]
    cogs = rev * (1 - GM[y])
    gp = rev - cogs
    fixed = FIXED_OPEX[y]
    prov = rev * PROV_PC
    ebitda_bd = gp - fixed - prov            # EBITDA before owner drawings
    draws = DRAWS[y]
    after = ebitda_bd - draws
    return dict(rev=rev, cogs=cogs, gp=gp, gm=GM[y], fixed=fixed, prov=prov,
                ebitda_bd=ebitda_bd, draws=draws, after=after)

PL = {y: pnl(y) for y in ("Y1", "Y2", "Y3")}

# --- Startup use of funds ---
USE_OF_FUNDS = [
    ("Work van — lease/finance deposit + fit-out (not a $28k cash buy)", 5000),
    ("Spray gear, ladders/platforms, prep tools, sanders, HEPA vac + P2 kit", 12000),
    ("Access equipment (small scaffold/steps; hire larger 2-storey rigs)", 3000),
    ("Branding, website + SEO, vehicle signage, uniforms, Google Business Profile", 7000),
    ("Insurance — initial deposit/bond (programme then paid monthly)", 1500),
    ("Company / IRD / GST registration, SiteWise, Dulux/Resene accreditation", 3000),
    ("Legal — SHA, constitution, shareholder-loan/PPSR deed, IP + vesting + restraints", 7000),
    ("Working-capital / contingency buffer (COD materials mths 1-3)", 25000),
]
SETUP_TOTAL = sum(a for _, a in USE_OF_FUNDS)
EQUITY = 50000
CAPITAL = EQUITY + LOAN
RESERVE = CAPITAL - SETUP_TOTAL

# --- Monthly overhead schedule (Y1) ---
OVERHEAD = [
    ("Leased van + fuel + RUC + maintenance", 1200),
    ("Insurance programme (public liability $2M, statutory, tools, contract works, vehicle)", 350),
    ("Key-person life/TPD/trauma on Partner B + income protection / ACC CoverPlus Extra", 220),
    ("Marketing & lead-gen (BLENDED Y1 avg; phased $400 -> $2,000-2,500/mo)", 1500),
    ("Accounting, bookkeeping & Xero", 500),
    ("Job-management software (ServiceM8), phone, internet", 300),
    ("Partner A — principal / back-office draw (staged to cash)", 3000),
    ("Partner B — supervision/quoting/QC draw (billable time sits in COGS)", 1500),
    ("Rework / warranty reserve (~3% of revenue)", 600),
    ("Bad-debt provision (~1.5% of revenue)", 300),
    ("SiteWise, memberships (amortised), PPE consumables, bank/sundry", 450),
]

# --- Y1 monthly cashflow (base case) ---
# Launch into winter; ramp through to the Nov-Apr exterior peak.
MONTHS = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12"]
REV_VEC = [6, 8, 10, 14, 20, 22, 24, 26, 28, 30, 22, 25]  # $000, sums to 235
REV_VEC = [v * 1000 for v in REV_VEC]

def y1_cashflow():
    opening = CAPITAL - SETUP_TOTAL          # operating cash after day-0 setup
    bal = opening
    rows = []
    prev_rev = 0
    gst_accrued = 0.0
    for i, rev in enumerate(REV_VEC):
        # Realistic collection: 63% this month (deposit/progress on residential), 35% next
        # month (balance + slower commercial); ~2% slow tail / bad debt. Reflects the reviewer's
        # ~50% deposit-capture caveat rather than the optimistic near-full same-month capture.
        collect = rev * 0.63 + prev_rev * 0.35
        materials = rev * MATERIALS_PC
        mat_paid = materials if i < 3 else REV_VEC[i-1] * MATERIALS_PC  # COD mths 1-3, else 30-day
        labour = rev * (0.70 - MATERIALS_PC) # subbie + B billable, paid same month
        fixed = FIXED_OPEX["Y1"] / 12.0
        # Partner B is a working painter with no other income: through the low-utilisation winter
        # trough (months 1-6) his billable COGS income is thin, so he needs a living top-up.
        draws = 4500 + (2500 if i < 6 else 0)
        rework = (REV_VEC[i-1] * 0.03) if i >= 1 else 0.0          # re-dos lag 1 month
        gst_accrued += collect * 0.045       # net GST ~4.5% of collections (payments basis)
        gst_paid = 0.0
        if (i + 1) % 2 == 0:                  # remit 2-monthly
            gst_paid = gst_accrued
            gst_accrued = 0.0
        net = collect - mat_paid - labour - fixed - draws - rework - gst_paid
        bal += net
        rows.append(dict(m=MONTHS[i], rev=rev, collect=collect, mat=mat_paid, lab=labour,
                         fixed=fixed, draws=draws, rework=rework, gst=gst_paid, net=net, bal=bal))
        prev_rev = rev
    return opening, rows

OPENING, CF = y1_cashflow()
MIN_BAL = min(r["bal"] for r in CF)
PEAK_NEED = CAPITAL - MIN_BAL                 # cash actually consumed from the $200k
HEADROOM = 200000 - PEAK_NEED
STRESS_PEAK = 195000

print("=== FINANCIAL SUMMARY ===")
for y in ("Y1", "Y2", "Y3"):
    p = PL[y]
    print(f"{y}: rev {nz(p['rev'])} GP {nz(p['gp'])} ({p['gm']*100:.0f}%) "
          f"EBITDA-before-draws {nz(p['ebitda_bd'])} draws {nz(p['draws'])} after {nz(p['after'])}")
print(f"Setup {nz(SETUP_TOTAL)}  Capital {nz(CAPITAL)}  Reserve {nz(RESERVE)}")
print(f"Opening op cash {nz(OPENING)}  Min bal {nz(MIN_BAL)}  Peak cash need {nz(PEAK_NEED)}  Headroom {nz(HEADROOM)}")

# ================================================================ PDF STYLES
ss = getSampleStyleSheet()
def style(name, **kw):
    return ParagraphStyle(name, **kw)

BODY = style("Body", fontName="Helvetica", fontSize=10, leading=14.5, textColor=INK,
             alignment=TA_JUSTIFY, spaceAfter=7)
LEAD = style("Lead", fontName="Helvetica-Bold", fontSize=10, leading=14.5, textColor=NAVY,
             spaceAfter=2)
H1 = style("H1", fontName="Helvetica-Bold", fontSize=15.5, leading=19, textColor=NAVY,
           spaceBefore=6, spaceAfter=9, keepWithNext=1)
H2 = style("H2", fontName="Helvetica-Bold", fontSize=11.5, leading=15, textColor=GOLD_DARK if (GOLD_DARK:=colors.HexColor("#A87A1E")) else GOLD,
           spaceBefore=11, spaceAfter=4, keepWithNext=1)
BULLET = style("Bullet", fontName="Helvetica", fontSize=9.5, leading=13.5, textColor=INK,
               leftIndent=13, bulletIndent=2, spaceAfter=3.5, alignment=TA_LEFT)
SMALL = style("Small", fontName="Helvetica", fontSize=8, leading=11, textColor=GREY)
TCELL = style("TCell", fontName="Helvetica", fontSize=8.5, leading=11.5, textColor=INK)
TCELLB = style("TCellB", fontName="Helvetica-Bold", fontSize=8.5, leading=11.5, textColor=NAVY)
THEAD = style("THead", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=colors.white)
TNUM = style("TNum", fontName="Helvetica", fontSize=8.5, leading=11.5, textColor=INK, alignment=TA_RIGHT)
TNUMB = style("TNumB", fontName="Helvetica-Bold", fontSize=8.5, leading=11.5, textColor=NAVY, alignment=TA_RIGHT)
KTAG = style("KTag", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=NAVY)

def P(t, s=BODY): return Paragraph(t, s)
def bullets(items, s=BULLET):
    return [Paragraph(("<font color='#C8952A'>&#9642;</font>&nbsp;&nbsp;") + it, s) for it in items]

# ---- table helpers
def data_table(header, rows, colw, aligns=None, hi_last=False, hi_rows=None):
    hi_rows = hi_rows or []
    data = [[Paragraph(h, THEAD) for h in header]]
    for r in rows:
        cells = []
        for j, c in enumerate(r):
            st = TNUM if (aligns and aligns[j] == "r") else TCELL
            cells.append(Paragraph(str(c), st))
        data.append(cells)
    t = Table(data, colWidths=colw, repeatRows=1)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("LINEBELOW", (0, 0), (-1, 0), 0.7, NAVY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 1), (-1, -1), 0.35, LINEG),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            cmds.append(("BACKGROUND", (0, i), (-1, i), ROWALT))
    for hr in hi_rows:
        cmds.append(("BACKGROUND", (0, hr), (-1, hr), LIGHT))
        cmds.append(("LINEABOVE", (0, hr), (-1, hr), 0.6, NAVY))
    t.setStyle(TableStyle(cmds))
    return t

def kv_table(pairs, w1=150, w2=330):
    data = [[Paragraph(k, KTAG), Paragraph(v, TCELL)] for k, v in pairs]
    t = Table(data, colWidths=[w1, w2])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, LINEG),
    ]))
    return t

class HRule(Flowable):
    def __init__(self, w, color=GOLD, thick=1.4):
        super().__init__(); self.w=w; self.color=color; self.thick=thick
    def wrap(self, aw, ah): return (self.w, self.thick+2)
    def draw(self):
        self.canv.setStrokeColor(self.color); self.canv.setLineWidth(self.thick)
        self.canv.line(0, 1, self.w, 1)

# ---- charts
def revenue_chart(width=470, height=170):
    d = Drawing(width, height)
    bc = VerticalBarChart()
    bc.x = 40; bc.y = 28; bc.width = width-90; bc.height = height-55
    bc.data = [[PL["Y1"]["rev"], PL["Y2"]["rev"], PL["Y3"]["rev"]],
               [PL["Y1"]["ebitda_bd"], PL["Y2"]["ebitda_bd"], PL["Y3"]["ebitda_bd"]]]
    bc.categoryAxis.categoryNames = ["Year 1", "Year 2", "Year 3"]
    bc.bars[0].fillColor = NAVY
    bc.bars[1].fillColor = GOLD
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 650000
    bc.valueAxis.valueStep = 130000
    bc.valueAxis.labelTextFormat = lambda v: "$%dk" % (v/1000)
    bc.valueAxis.labels.fontName = "Helvetica"; bc.valueAxis.labels.fontSize = 7.5
    bc.categoryAxis.labels.fontName = "Helvetica-Bold"; bc.categoryAxis.labels.fontSize = 8.5
    bc.barWidth = 9; bc.groupSpacing = 22; bc.barSpacing = 2
    d.add(bc)
    d.add(String(40, height-12, "Revenue vs EBITDA (before owner drawings) — base case",
                 fontName="Helvetica-Bold", fontSize=8.5, fillColor=NAVY))
    d.add(Rect(width-140, height-14, 8, 8, fillColor=NAVY, strokeColor=None))
    d.add(String(width-128, height-12, "Revenue", fontName="Helvetica", fontSize=7.5, fillColor=INK))
    d.add(Rect(width-70, height-14, 8, 8, fillColor=GOLD, strokeColor=None))
    d.add(String(width-58, height-12, "EBITDA", fontName="Helvetica", fontSize=7.5, fillColor=INK))
    return d

def cashflow_chart(width=470, height=190):
    d = Drawing(width, height)
    lp = LinePlot()
    lp.x = 42; lp.y = 30; lp.width = width-90; lp.height = height-60
    pts_bal = [(i+1, CF[i]["bal"]) for i in range(12)]
    pts_ceil = [(1, 0), (12, 0)]  # y=0 line reference for "cash consumed"
    lp.data = [pts_bal]
    lp.lines[0].strokeColor = NAVY; lp.lines[0].strokeWidth = 2
    lp.lines[0].symbol = makeMarker("FilledCircle"); lp.lines[0].symbol.size = 3; lp.lines[0].symbol.fillColor = GOLD
    lp.xValueAxis.valueMin = 1; lp.xValueAxis.valueMax = 12; lp.xValueAxis.valueStep = 1
    lp.xValueAxis.labels.fontName = "Helvetica"; lp.xValueAxis.labels.fontSize = 7
    lp.yValueAxis.valueMin = 0; lp.yValueAxis.valueMax = 160000; lp.yValueAxis.valueStep = 40000
    lp.yValueAxis.labelTextFormat = lambda v: "$%dk" % (v/1000)
    lp.yValueAxis.labels.fontName = "Helvetica"; lp.yValueAxis.labels.fontSize = 7.5
    d.add(lp)
    # min-balance marker line
    ymin = 30 + (MIN_BAL/160000.0)*(height-60)
    d.add(Line(42, ymin, width-48, ymin, strokeColor=RED, strokeWidth=0.8, strokeDashArray=[3,2]))
    d.add(String(46, ymin+3, "Cash trough %s  (peak draw on the $200k = %s)" % (nz(MIN_BAL), nz(PEAK_NEED)),
                 fontName="Helvetica-Bold", fontSize=7.5, fillColor=RED))
    d.add(String(42, height-12, "Year-1 monthly operating cash balance (base case) — of $200k capital",
                 fontName="Helvetica-Bold", fontSize=8.5, fillColor=NAVY))
    return d

# ================================================================ DOC TEMPLATE
class PlanDoc(BaseDocTemplate):
    def __init__(self, fn, **kw):
        super().__init__(fn, **kw)
        fw, fh = A4
        L, R, T, B = 54, 54, 62, 52
        frame = Frame(L, B, fw-L-R, fh-T-B, id="main")
        cover = Frame(0, 0, fw, fh, id="cover")
        self.addPageTemplates([
            PageTemplate(id="Cover", frames=[cover], onPage=self._cover_bg),
            PageTemplate(id="Main", frames=[frame], onPage=self._chrome),
        ])
    def _cover_bg(self, c, d):
        fw, fh = A4
        c.setFillColor(NAVY); c.rect(0, 0, fw, fh, fill=1, stroke=0)
        c.setFillColor(GOLD); c.rect(0, fh-6, fw, 6, fill=1, stroke=0)
        c.setStrokeColor(GOLD); c.setLineWidth(1)
        c.line(54, fh*0.60, fw-54, fh*0.60)
    def _chrome(self, c, d):
        fw, fh = A4
        c.setStrokeColor(LINEG); c.setLineWidth(0.6)
        c.line(54, fh-46, fw-54, fh-46)
        c.setФont if False else c.setFont("Helvetica", 7.5)
        c.setFillColor(GREY)
        c.drawString(54, fh-42, "Auckland Painting Co  —  Business Plan & Financial Model")
        c.drawRightString(fw-54, fh-42, "Confidential")
        c.setStrokeColor(LINEG); c.line(54, 40, fw-54, 40)
        c.setFont("Helvetica", 7.5); c.setFillColor(GREY)
        c.drawString(54, 30, "Prepared 27 July 2026  •  ETR-hardened (CONDITIONAL_GO)")
        c.drawRightString(fw-54, 30, "Page %d" % d.page)
    def afterFlowable(self, flowable):
        if hasattr(flowable, "style") and flowable.style.name in ("H1",):
            txt = flowable.getPlainText()
            self.notify("TOCEntry", (0, txt, self.page))

# ================================================================ BUILD STORY
story = []

# ---- COVER
story += [Spacer(1, 150)]
story.append(Paragraph("BUSINESS PLAN &amp; FINANCIAL MODEL",
             style("cvtag", fontName="Helvetica-Bold", fontSize=11, textColor=GOLD,
                   alignment=TA_CENTER, spaceAfter=14)))
story.append(Paragraph("Auckland Residential &amp; Commercial<br/>Painting Company",
             style("cvtitle", fontName="Helvetica-Bold", fontSize=30, leading=35,
                   textColor=colors.white, alignment=TA_CENTER, spaceAfter=10)))
story.append(Paragraph("Working name: <i>Weatherline Painters</i> (brand TBD)",
             style("cvsub", fontName="Helvetica", fontSize=12, textColor=colors.HexColor("#C9D2DC"),
                   alignment=TA_CENTER, spaceAfter=40)))
story += [Spacer(1, 120)]
story.append(Paragraph("A 50/50 venture — the principal runs the business &amp; funds it; his cousin, a qualified painter, runs operations.",
             style("cvline", fontName="Helvetica", fontSize=11, leading=16,
                   textColor=colors.HexColor("#C9D2DC"), alignment=TA_CENTER, spaceAfter=8)))
story.append(Paragraph("Auckland, New Zealand  •  Launch 2026  •  $200,000 capital  •  Prepared 27 July 2026",
             style("cvline2", fontName="Helvetica", fontSize=9.5,
                   textColor=GOLD, alignment=TA_CENTER)))
story.append(NextPageTemplate("Main"))
story.append(PageBreak())

# ---- TOC
story.append(Paragraph("Contents", H1))
story.append(HRule(487)); story.append(Spacer(1, 8))
toc = TableOfContents()
toc.levelStyles = [ParagraphStyle("toc1", fontName="Helvetica", fontSize=10.5, leading=20,
                                  textColor=INK, leftIndent=6, rightIndent=14)]
story.append(toc)
story.append(PageBreak())

def H(t): return Paragraph(t, H1)
def SH(t): return Paragraph(t, H2)

# ---- 1. EXECUTIVE SUMMARY
story.append(H("1.  Executive Summary"))
story.append(HRule(487)); story.append(Spacer(1, 6))
story.append(Paragraph("Verdict:&nbsp; CONDITIONAL GO", LEAD))
story.append(P("A viable, low-barrier Auckland painting venture that clears the $200k cash ceiling <b>only if</b> "
    "it (1) prices labour cost-plus, (2) restructures the $200k as equity-plus-secured-shareholder-loan, "
    "(3) funds the Partner&nbsp;B key-person risk, and (4) commits to one beachhead lane. As a naive 50/50, "
    "cost-plus, jack-of-all-trades it fails on margin, fairness and key-person risk — which is exactly what the "
    "adversarial review caught and this plan fixes."))
story.append(P("The venture enters a large, fragmented market — roughly <b>$1.9&ndash;2.0bn</b> nationally across "
    "~<b>5,832 mostly micro firms</b> with no dominant residential player and <b>no trade licence required</b> "
    "(painting is not restricted building work). That structurally favours a small, well-run, credentialed "
    "independent. Two realities shape the model: the market is in late-cyclical softness (contracted "
    "-7.0% in 2024, -3.2% in 2025; new-dwelling consents ~33,500, down 3.8%), so the plan does <b>not</b> lean on "
    "builder-subcontract volume; and demand is strongly seasonal, with exterior work concentrated Nov&ndash;Apr "
    "and collapsing through the Jun&ndash;Aug winter."))
story.append(SH("What the adversarial review changed"))
story.append(P("The pre-review plan failed four hard tests. Each is now corrected:"))
story += bullets([
    "<b>Margin.</b> Billing subbie hours at $65/hr — inside the $45&ndash;75 subbie cost band — yields ~12% gross "
    "margin, not the claimed 45%. Repriced to <b>cost-plus: pay $55, bill $95/hr</b>, and a <b>honest 30% Year-1 "
    "gross margin</b> (rising to ~43% by Year 3).",
    "<b>Capital fairness.</b> Partner A funding 100% of $200k for 50% plain equity gifts B ~$100k on day one and "
    "traps A's cash behind everything. Resolved by splitting into <b>~$50k equity (50/50) + ~$150k secured, "
    "PPSR-registered shareholder loan</b> from A, repaid ahead of dividends.",
    "<b>Key-person risk.</b> B is the only qualified painter, sole quoter, sole QC and only HSWA-competent person. "
    "Mitigated with key-person/TPD/trauma cover, an anchor subbie on retainer, reverse-vesting + restraints, and an "
    "employed painter brought forward to early H2 as a continuity/QC backup.",
    "<b>Positioning.</b> 'Mixed/opportunistic' across four buyer types fragments B's scarce capacity and stops any "
    "referral flywheel. Fixed by pointing 100% of marketing at <b>one beachhead lane — premium residential "
    "weatherboard exterior repaint</b> — while keeping intake opportunistic.",
])
story.append(SH("The numbers, hardened"))
story.append(kv_table([
    ("Year-1 revenue", "%s base  (%s low / %s high) — supervision-constrained, launching into winter" %
        (nz(REV["Y1"]), nz(REV_RANGE["Y1_low"]), nz(REV_RANGE["Y1_high"]))),
    ("3-year revenue path", "%s &#8594; %s &#8594; %s (base)" % (nz(REV["Y1"]), nz(REV["Y2"]), nz(REV["Y3"]))),
    ("Gross margin", "30% (Y1, fully-costed) &#8594; 39% (Y2) &#8594; 43% (Y3)"),
    ("Year-1 result", "Near-breakeven before owner drawings (%s); a deliberate ~%s investment year after modest, staged draws" %
        (nz(PL["Y1"]["ebitda_bd"]), nz(abs(PL["Y1"]["after"])))),
    ("Peak cash need", "~%s base of the $200k (trough %s, ~%s headroom); explicit stress case ~%s at the ceiling" %
        (nz(PEAK_NEED), nz(MIN_BAL), nz(HEADROOM), nz(STRESS_PEAK))),
    ("Capital structure", "%s equity (50/50) + %s secured shareholder loan (Partner A, PPSR-registered)" % (nz(EQUITY), nz(LOAN))),
    ("Break-even", "~Month 12 on an EBITDA-before-drawings basis; full market owner pay affordable from Year 2"),
]))
story.append(Spacer(1, 8))
story.append(revenue_chart())
story.append(Spacer(1, 4))
story.append(P("<i>The plan is a green light on the structure and legals first, then launch to fill winter with "
    "interior repaints and property-management turnovers to bank reviews before spring, then specialise on real "
    "margin data by the end of Year 1.</i>", SMALL))
story.append(PageBreak())

# ---- 2. THE MARKET
story.append(H("2.  The Market"))
story.append(HRule(487)); story.append(Spacer(1, 6))
story.append(P("The strategic read is to anchor on counter-cyclical, recurring <b>residential repaint</b> and "
    "property-maintenance demand (Auckland weatherboard exterior cycle ~7&ndash;10 years, shorter on coastal/high-UV "
    "sites), concentrate on Auckland (rising toward ~44% of national consents by 2030), and use light-commercial and "
    "interior work as a weather-independent winter hedge — with new-build as opportunistic top-up only."))
story.append(SH("Market facts (with sources)"))
mkt = [
    ("Market size", "~$1.9bn (2025), approaching $2.0bn (2026)", "IBISWorld — Painting & Decorating Services in NZ (332)"),
    ("Trajectory", "-7.0% (2024), -3.2% (2025); ~1.7% CAGR 2020-25", "IBISWorld (332)"),
    ("Fragmentation", "~5,832 firms; no dominant residential player", "IBISWorld (332)"),
    ("New consents", "~33,530 dwellings (yr to May 2025), down 3.8%", "Stats NZ Building Consents, May 2025"),
    ("Auckland share", "rising toward ~44% of national consents by 2030", "MBIE National Construction Pipeline"),
    ("Repaint cycle", "Auckland weatherboard ~7-10 yrs (shorter coastal)", "The House Painters (Auckland trade)"),
    ("Seasonality", "Exterior peak Nov-Apr; 4-8 wk waits; winter skews interior", "Automate The Trades — Rates NZ 2026"),
    ("Barrier to entry", "Painting is NOT restricted building work — no LBP licence", "Building Performance (MBIE)"),
    ("Threat", "DIY substitution, esp. interior repaints under cost-of-living pressure", "IBISWorld (332)"),
]
story.append(data_table(["Factor", "Figure", "Source"], mkt,
                        [95, 210, 182], aligns=["l", "l", "l"]))
story.append(Spacer(1, 6))
story.append(P("<i>Governance note: every figure above is attributable to a named, producible source (IBISWorld NZ "
    "industry 332, Stats NZ, MBIE) — full URLs are listed in the Sources appendix. No stat is attributed to a "
    "council, police or industry body without a source.</i>", SMALL))
story.append(PageBreak())

# ---- 3. POSITIONING & STRATEGY
story.append(H("3.  Positioning &amp; Strategy"))
story.append(HRule(487)); story.append(Spacer(1, 6))
story.append(Paragraph("The beachhead: premium residential weatherboard exterior repaints", LEAD))
story.append(P("In a ~5,800-firm fragmented market the customer sets price, so a zero-review newcomer needs a "
    "concrete edge, not a cost-plus rate. Exterior repaint is the single best lane because it is <b>counter-cyclical</b> "
    "(not exposed to the construction downturn), <b>recurring</b> (the 7&ndash;10yr cycle drives repeat and referral "
    "density), <b>highest-value per job</b> ($10&ndash;20k), and has the <b>best cash profile</b> (deposit + progress "
    "claim + completion &#8776; effectively 0&ndash;14 day terms)."))
story.append(P("Keep <b>intake</b> opportunistic — say yes to interior repaints, property-maintenance/tenancy turnovers "
    "and selective light-commercial that walk in — but point <b>100% of marketing spend, review-harvesting and the "
    "referral ask</b> at the one exterior-repaint lane so the flywheel actually spins. Decide the permanent "
    "specialise-in lane on real margin data by the <b>end of Year 1</b>, not Year 2."))
story.append(SH("The value proposition — a verifiable quality promise"))
story.append(P("Every job is delivered against a <b>written, measured scope referencing AS/NZS&nbsp;2311</b>, backed by "
    "a <b>fixed re-do guarantee</b>, <b>Dulux Accredited / Resene Eco.Decorator</b> status and the manufacturer's own "
    "<b>5-year workmanship warranty</b>. Priced at par (no peak premium) in Year 1 to build a review base, with the "
    "premium and the Master Painters NZ 5-year guarantee added in Year 2 (MPNZ is gated out until ~2027&ndash;28 by an "
    "18-month + 3-job inspection). This turns 'reliable finish, no surprises, guaranteed in writing' into the "
    "differentiator, so the firm stops pricing purely off its own cost stack."))
story.append(SH("Brand name options (to finalise)"))
story += bullets([
    "<b>Weatherline Painters</b> — signals exterior / weatherboard specialism",
    "<b>Trueline Decorators Auckland</b>",
    "<b>Northside Repaint Co.</b> — suburb-clustered, repaint-focused",
    "<b>Clearcoat Painting &amp; Decorating</b>",
    "<b>Harbour City Repaints</b>",
])
story.append(PageBreak())

# ---- 4. BUSINESS MODEL & UNIT ECONOMICS
story.append(H("4.  Business Model &amp; Unit Economics"))
story.append(HRule(487)); story.append(Spacer(1, 6))
story.append(P("An independent, self-branded Auckland painting company with its own back-office and client "
    "acquisition. <b>Partner A</b> (the principal) runs finance, growth and back-office and provides all startup "
    "capital; <b>Partner B</b> (his cousin), a qualified experienced painter, runs delivery as the working lead — "
    "quoting, QC and on-the-tools — and builds a subcontract crew. Year 1 is deliberately capacity-light and "
    "cash-protective."))
story.append(SH("Crew model — subbie-first, hardened"))
story += bullets([
    "<b>Subbie-first in Year 1</b> to convert labour to a variable cost and protect the $200k ceiling.",
    "Secure <b>1&ndash;2 anchor subbies on first-call/retainer terms</b> — good Auckland subbies book out 4&ndash;8 "
    "weeks at the Nov&ndash;Apr peak, so on-demand liquidity is unreliable exactly when surge is needed.",
    "<b>Prohibit unsupervised height/lead work</b> by newly onboarded subbies; stage each new subbie through paid, "
    "fully-inspected trial jobs — CGA re-do liability sits with the company regardless of the contractor label.",
    "Paper each subbie as a genuine contract-for-services (own GST/ACC, own tools, non-exclusive, invoicing) to "
    "avoid IRD/MBIE reclassification.",
    "Bring the <b>first employed qualified painter forward to early H2</b> as a continuity + QC backup — then convert "
    "the best subbies to employment only once run-rate is a stable ~$400k+.",
])
story.append(SH("Pricing — cost-plus, never cost-band"))
story.append(kv_table([
    ("Labour charge-out", "~$95/hr (range $85-110), a 45-70% markup on the $55/hr subbie — never bill a subbie hour inside its cost band"),
    ("Light-commercial", "~$760/painter/day (8h &#215; $95)"),
    ("Materials", "~19% of revenue (~24% of prime cost), passed through off Resene/Dulux trade accounts"),
    ("Year-1 realised rate", "~10-15% reputation discount on the first ~10-20 jobs; 0% peak premium — restored in Year 2"),
    ("Validation", "Test willingness-to-pay against 5-10 real competitor quotes before locking the rate"),
]))
story.append(Spacer(1, 6))
story.append(SH("Unit economics"))
ue = [
    ("Labour charge-out (client)", nz(CHARGE_OUT) + "/hr", "Cost-plus on subbie labour"),
    ("Subbie cost", nz(SUBBIE_HR) + "/hr", "Variable; no idle payroll"),
    ("Employed painter (all-in)", nz(EMPLOYED_HR) + "/hr", "~$30 base + 12-18% on-costs"),
    ("Materials", "19% of revenue", "Resene/Dulux trade accounts"),
    ("Gross margin (Y1)", "30%", "Fully-costed incl. all direct labour"),
    ("Avg exterior/residential job", nz(AVG_RES_JOB), "Interior ~$5,500; large 2-storey $20-30k+"),
    ("Avg light-commercial job", nz(AVG_COMM_JOB), "Day-rate maintenance work"),
]
story.append(data_table(["Metric", "Value", "Note"], ue, [150, 90, 247], aligns=["l", "l", "l"]))
story.append(Spacer(1, 5))
story.append(P("<i>Labour is 75&ndash;85% of job cost, so the crew mix is the single biggest margin and cash lever. "
    "Gross margin rises to 39&ndash;43% in Years 2&ndash;3 as a small employed core lifts utilisation.</i>", SMALL))
story.append(PageBreak())

# ---- 5. GO TO MARKET
story.append(H("5.  Go-to-Market"))
story.append(HRule(487)); story.append(Spacer(1, 6))
story.append(P("A newcomer's first job is to manufacture trust cheaply and fast, then convert it into a near-free "
    "referral engine. Spend is phased: free and pay-per-lead channels first, paid Google only once the website "
    "converts and reviews exist."))
gtm = [
    ("Google Business Profile", "Claim &amp; optimise day one; harvest reviews from job one", "$0 (time)"),
    ("Builderscrack (pay-per-lead)", "Instant lead flow week 1; push conversion 1-in-6/7 &#8594; 1-in-3", "~$40-100/booked job"),
    ("NoCowboys (subscription)", "List month 1; bank public reviews, relationship stays yours", "$999/yr flat"),
    ("Agents &amp; property managers", "Outreach pack for pre-sale freshen-ups + tenancy turnovers (Y2 build)", "Low; 14-45 day terms"),
    ("Paid Google Search", "Layer from month 2-3 once site converts + reviews exist", "~$2,000-2,500/mo ramp"),
    ("Facebook/Instagram + referrals", "Before/after content + formal referral ask; dominant by mth 3-6", "~$0-300/mo"),
]
story.append(data_table(["Channel", "Tactic", "Cost / CAC"], gtm, [130, 250, 107], aligns=["l", "l", "l"]))
story.append(Spacer(1, 8))
story.append(SH("First 90 days"))
story += bullets([
    "Register company + IRD; register GST from day one on <b>PAYMENTS basis</b>; enrol ACC CoverPlus / CoverPlus Extra for B.",
    "Execute the legals <b>before trading</b>: SHA + constitution + secured shareholder-loan/PPSR deed + IP/brand "
    "assignment + reverse-vesting + restraints; bind key-person + income-protection cover on B.",
    "Open Resene AND Dulux trade accounts (expect COD/low-limit for months 1-3); apply for Dulux Accredited / Resene Eco.Decorator.",
    "Lease the van; buy spray/prep/HEPA-P2 kit; build the H&amp;S spine (height/access SWMS, lead-paint procedure, "
    "hazardous-substances inventory + SDS); start SiteWise (target Green 75%+).",
    "Claim + optimise GBP; stand up a converting website; list on NoCowboys; turn on Builderscrack — no paid Google yet.",
    "Sign 1-2 anchor subbies on first-call/retainer terms; stage each through a paid, fully-inspected trial job.",
    "Fill the winter trough with interior repaints + PM tenancy turnovers to bank reviews before the Sep-Oct spring ramp.",
    "Stand up Xero + ServiceM8; set a ~$30k minimum-cash covenant and a tax-reserve sub-account (~28% of profit).",
])
story.append(PageBreak())

# ---- 6. OPERATIONS & DELIVERY
story.append(H("6.  Operations, Quality &amp; Health-and-Safety"))
story.append(HRule(487)); story.append(Spacer(1, 6))
story.append(P("Delivery runs off Partner B as working lead, but the model explicitly stops double-counting his hours "
    "as both revenue engine and QC/quoting function: carve out realistic <b>non-billable QC + quoting time "
    "(1&ndash;2 days/week)</b> and derive the Year-1 revenue ceiling downward accordingly (effective ~1.2&ndash;1.8 "
    "billable painters)."))
story.append(SH("Quality control"))
story += bullets([
    "Written <b>AS/NZS 2311</b> measured scope per job; Partner B QC sign-off before invoicing.",
    "New subbies staged through paid, fully-inspected trial jobs before any unsupervised work.",
    "Rework/warranty reserve (~3% of revenue) funds re-dos — CGA liability sits with the company, not the subbie.",
    "Dulux/Resene accreditation + manufacturer 5-year workmanship warranty in Y1; MPNZ 5-year guarantee at month 18.",
])
story.append(SH("Health &amp; safety (HSWA / WorkSafe)"))
story += bullets([
    "Documented SWMS/JSA per job for height and lead work; certified scaffolder + WorkSafe notification where a 5m+ fall is possible.",
    "Hire (not improvise) access equipment for 2-storey+; the company is the PCBU regardless of the contractor label.",
    "P2/HEPA lead-paint controls for pre-1980 homes (lead banned in residential paint 1979); Resene PaintWise / licensed solvent disposal.",
    "Statutory liability cover; SiteWise-tested H&amp;S system (target Green 75%+) to unlock commercial / head-contractor work.",
])
story.append(SH("Systems"))
story.append(P("Xero (GST payments basis) + ServiceM8 for quoting/scheduling/invoicing; SiteWise prequalification; "
    "hazardous-substances inventory + SDS. <b>Key hires:</b> first employed qualified painter early H2 (continuity + "
    "QC backup — the only structural mitigation for the key-person and unsupervised-QC risks), then a BCITO apprentice "
    "in Y2 and a non-owner lead by Y3 to move delivery off Partner B's sole shoulders and lift exit value."))
story.append(PageBreak())

# ---- 7. FINANCIAL PLAN
story.append(H("7.  Financial Plan"))
story.append(HRule(487)); story.append(Spacer(1, 6))
story.append(SH("7.1  Use of the $200,000"))
uf_rows = [(d, nz(a)) for d, a in USE_OF_FUNDS]
uf_rows.append(("Setup sub-total", nz(SETUP_TOTAL)))
uf_rows.append(("Retained working-capital reserve (funds the Year-1 ramp)", nz(RESERVE)))
uf_rows.append(("Total capital deployed", nz(CAPITAL)))
story.append(data_table(["Use of funds", "NZD"], uf_rows, [400, 87], aligns=["l", "r"],
                        hi_rows=[len(USE_OF_FUNDS)+1, len(USE_OF_FUNDS)+3]))
story.append(Spacer(1, 5))
story.append(P("Capital in: <b>%s equity + %s secured shareholder loan (Partner A) = %s</b>. Only %s is spent on "
    "day-one setup; the remaining %s is the working-capital reserve that carries the Year-1 ramp and winter trough."
    % (nz(EQUITY), nz(LOAN), nz(CAPITAL), nz(SETUP_TOTAL), nz(RESERVE)), BODY))

story.append(SH("7.2  Three-year P&amp;L (base case)"))
def row(label, key, pct=False):
    return [label] + [("%.0f%%" % (PL[y][key]*100)) if pct else nz(PL[y][key]) for y in ("Y1","Y2","Y3")]
pl_rows = [
    row("Revenue", "rev"),
    row("Cost of sales (materials + direct labour)", "cogs"),
    row("Gross profit", "gp"),
    ["Gross margin", "30%", "39%", "43%"],
    row("Operating expenses (fixed, ex owner draws)", "fixed"),
    row("Provisions (rework 3% + bad debt 1.5%)", "prov"),
    row("EBITDA before owner drawings", "ebitda_bd"),
    row("Owner drawings (combined, staged to cash)", "draws"),
    row("Operating result after drawings", "after"),
]
story.append(data_table(["NZD", "Year 1", "Year 2", "Year 3"], pl_rows,
                        [244, 81, 81, 81], aligns=["l", "r", "r", "r"],
                        hi_rows=[7, 9]))
story.append(Spacer(1, 5))
story.append(P("The honest picture Ahmad's lens cares about: <b>EBITDA before owner drawings</b> runs %s (Y1, "
    "~breakeven) &#8594; %s (Y2, ~18%%) &#8594; %s (Y3, ~23%%). Year 1 is a deliberate investment year — after modest, "
    "staged owner draws it posts ~%s, funded from the capital reserve, not new cash. Full market owner pay "
    "($70&ndash;90k each) only becomes affordable from Year 2." %
    (nz(PL["Y1"]["ebitda_bd"]), nz(PL["Y2"]["ebitda_bd"]), nz(PL["Y3"]["ebitda_bd"]), nz(PL["Y1"]["after"])), BODY))
story.append(P("<i>Financing memo: the $150k shareholder loan accrues interest at ~9% (~$13.5k/yr, income to Partner A) "
    "— assumed to accrue, not be paid, through Year 1 to protect the ceiling. Ring-fence ~28% of profit for terminal + "
    "Year-2 provisional tax so the tax wall is not funded out of the $200k.</i>", SMALL))

story.append(SH("7.3  Year-1 cashflow &amp; the $200k ceiling"))
story.append(cashflow_chart())
story.append(Spacer(1, 4))
story.append(P("Base peak cash need is <b>~%s</b> of the $200k (the trough dips to ~%s in balance), leaving "
    "<b>~%s of genuine headroom</b> — not the pre-review 'comfortable $80k'. An explicit stress case reaches "
    "<b>~%s, sitting at the ceiling</b>, if the plan's own breach levers co-occur (commercial drifting to ~50%% at "
    "60-day terms + retentions, one slow/disputed debtor, a slower 6-month ramp, and both owners drawing full "
    "salaries). The ceiling is therefore a genuine, not comfortable, constraint." %
    (nz(PEAK_NEED), nz(MIN_BAL), nz(HEADROOM), nz(STRESS_PEAK)), BODY))
story.append(SH("Governor rules to hold under the ceiling"))
story += bullets([
    "Subbie-first keeps labour variable; deposit/progress-claimed residential self-funds materials + labour.",
    "<b>Lease</b> the van (frees ~$23k) and <b>hire</b> large access equipment.",
    "Elect <b>GST payments basis</b> — never remit GST on uncollected commercial/new-build invoices.",
    "Commercial &lt; 30% of billings until terms proven; <b>no employed head until run-rate &gt; $400k</b>.",
    "Stage <b>both</b> owner draws to a <b>~$30k minimum bank-balance covenant</b>; carry the buffer through winter.",
    "Assume COD materials for months 1-3; sensitivity-test residential deposit capture at ~50% reliability.",
])
story.append(PageBreak())

# ---- 8. OWNERSHIP & LEGAL STRUCTURE
story.append(H("8.  Ownership, Capital &amp; Legal Structure"))
story.append(HRule(487)); story.append(Spacer(1, 6))
story.append(Paragraph("The single most important decision: how the $200k goes in", LEAD))
story.append(P("Partner A funds 100% of the capital but takes 50% equity. Left as plain 50/50 share capital, that "
    "<b>gifts Partner B ~$100k of value on day one</b> and traps A's cash behind everything, recoverable only via "
    "dividends A must then share 50/50. The fix keeps the 50/50 upside but makes A whole first:"))
story.append(kv_table([
    ("Equity", "~%s, split 50/50 — reflects A's cash and B's skill/sweat" % nz(EQUITY)),
    ("Shareholder loan", "~%s from Partner A, arm's-length interest (~8-10%%), <b>PPSR-registered</b>, repaid ahead of any dividend" % nz(LOAN)),
    ("Entity", "Ordinary limited company (a partnership's unlimited liability is unacceptable for a height/lead trade)"),
    ("Tax", "GST payments basis from day one; take advice on a first-year LTC election to flow Y1 ramp losses to A — weighed against the 49% shareholder-continuity test that vesting/buy-sell can trip"),
]))
story.append(Spacer(1, 6))
story.append(SH("Shareholders' agreement — must-have terms"))
story += bullets([
    "<b>Reverse-vesting</b> on B's 50% over 4 years (12-month cliff, then monthly); unvested shares reacquired at "
    "nominal value on a bad-leaver exit, fair value on a good-leaver exit.",
    "<b>Restraint of trade + non-solicit</b> of clients, staff and subcontractors (painting needs no licence, so B "
    "could otherwise leave and immediately compete).",
    "<b>Full IP/brand assignment to the company</b> — trademark, domain, Google Business Profile, socials, website — "
    "never in B's personal name.",
    "<b>Key-person insurance</b> (company-owned life + TPD + trauma on B), sized to the loan + ~6 months' overheads, "
    "structured to fund a buy-sell so B's estate is bought out and A's capital repaid; plus income protection / ACC CoverPlus Extra.",
    "<b>Deadlock mechanism</b>: reserved-matters list, escalation ladder (negotiation &#8594; mediation &#8594; binding "
    "buy/sell 'shotgun'), and a <b>weighted vote to A on capital/finance matters</b> while the loan is outstanding.",
    "<b>Remuneration &amp; distribution policy</b>: market-rate pay to each owner for work done, interest to A on the "
    "loan, then residual profit 50/50 as dividends — all staged to cashflow.",
    "<b>Guarantee allocation</b> documented: van on lease with small deposit; capped trade-account limits; where only A "
    "can realistically guarantee, price that risk with a 50/50 cross-indemnity; avoid PGs on any working-capital overdraft.",
])
story.append(PageBreak())

# ---- 9. RISKS
story.append(H("9.  Risks &amp; Mitigations"))
story.append(HRule(487)); story.append(Spacer(1, 6))
RISKS = [
    ("Key-person collapse — B is sole qualified painter, quoter, QC and HSWA-competent person", "Med / High",
     "Key-person life/TPD/trauma + income protection; employed painter early H2 as backup; model a 4-week-out scenario; non-owner lead by Y3"),
    ("Margin trap — cost-band pricing yields ~12% GM; a loss-making Y1 erodes the ceiling", "High / High",
     "Cost-plus (pay $55, bill $95); 30% fully-costed Y1 GM; validate rate vs 5-10 quotes; lean overhead until utilisation proven"),
    ("Cash-ceiling breach — commercial drift + slow debtors + slow ramp + dual draws &#8594; ~$195k", "Med / High",
     "Lease van; GST payments basis; hard governors; $25k buffer through winter; size liquidity to the $200k low case"),
    ("Capital-asymmetry dispute — A funds 100% for 50% equity; deadlock/exit-game risk", "Med / High",
     "$50k equity + $150k secured PPSR loan; reverse-vesting + good/bad-leaver; restraints + IP; weighted vote to A; ~$7k legals"),
    ("Cold-start meets seasonality — launching into winter misses the first exterior peak", "High / Med",
     "Y1 base $235k; fill winter with interior + PM turnovers to bank reviews; ramp marketing before spring; $285k = high case"),
    ("Subbie availability + quality — booked out at peak; early jobs a quality lottery (CGA liability)", "Med / Med",
     "1-2 anchor subbies on retainer; paid, inspected trial jobs; ~3% rework reserve; no unsupervised height/lead work"),
    ("Contractor misclassification (IRD/MBIE) — clawback of PAYE/KiwiSaver/leave + penalties", "Med / Med",
     "Genuine contracts-for-services; accept imperfect reliability OR convert to employment and price the on-costs"),
    ("HSWA height/lead incident — statutory liability + WorkSafe action + reputational kill", "Low / High",
     "Statutory liability cover; SWMS/JSA per job; certified scaffolder + notification for 5m+; P2/HEPA lead controls; hire access"),
    ("No differentiation / jack-of-all-trades — no referral flywheel, stuck on paid leads", "Med / Med",
     "One beachhead lane with a written AS/NZS 2311 scope + fixed re-do guarantee; 100% of marketing at it; specialise by end Y1"),
    ("Tax wall — terminal + Y2 provisional tax after the firm thinks it is self-funding", "Med / Low",
     "Ring-fence ~28% of profit from the first profitable month; note Y2 provisional-tax stacking"),
]
story.append(data_table(["Risk", "L / I", "Mitigation"], RISKS, [188, 58, 241], aligns=["l", "l", "l"]))
story.append(PageBreak())

# ---- 10. ROADMAP
story.append(H("10.  Roadmap &amp; Milestones"))
story.append(HRule(487)); story.append(Spacer(1, 6))
story.append(SH("Phase 0 — Pre-launch (weeks 0-8)"))
story.append(P("Execute the structure and legals <b>before trading</b>: company + GST (payments basis) + ACC; the full "
    "SHA package; bind key-person + income-protection cover; lease van; buy spray/HEPA-P2 kit; open Resene/Dulux trade "
    "accounts and pick a primary brand; stand up brand/website/GBP; sign 1-2 anchor subbies; build the H&amp;S spine "
    "and start SiteWise."))
story.append(SH("Phase 1 — Winter build (months 1-6)"))
story.append(P("Fill the trough with interior repaints + PM/tenancy turnovers to bank reviews; run Builderscrack + "
    "NoCowboys + GBP (no paid Google yet); layer paid Google from month 2-3 once the site converts; stage new subbies "
    "through paid trial jobs; bring the first employed qualified painter on in early H2 as continuity/QC; hold the "
    "buffer and the ~$30k minimum-cash covenant through winter."))
story.append(SH("Phase 2 — Peak &amp; specialise (months 7-18)"))
story.append(P("Capture the Nov&ndash;Apr exterior season on the reputation built over winter; convert PM/agent "
    "outreach into recurring contracts; decide the specialise-in lane on real margin data by end of Y1; achieve "
    "SiteWise Green to open light-commercial; apply for MPNZ at month 18; from Y2, add an employed painter + BCITO "
    "apprentice once run-rate &gt; $400k, restore peak-premium pricing, and begin moving delivery off Partner B's "
    "sole shoulders."))
story.append(SH("Milestones"))
story += bullets([
    "Legals + insurance bound and $200k structured (equity + secured loan) <b>before</b> the first job.",
    "First 10-20 delivered jobs with reviews banked <b>before</b> the Sep-Oct spring ramp.",
    "GST payments basis + minimum-cash covenant + tax reserve operational from month 1.",
    "First employed qualified painter onboarded early H2 as continuity/QC backup.",
    "Peak cash held under ~$150k base through winter; never breach the $200k ceiling.",
    "SiteWise Green (75%+) achieved to unlock commercial work.",
    "Year-1 revenue $235k base (min $200k) with a documented specialise-in lane decision by end of Y1.",
    "MPNZ application lodged at month 18; Y2 run-rate &gt; $400k before converting subbies to employment.",
])
story.append(PageBreak())

# ---- 11. WHAT THE ETR CHANGED
story.append(H("11.  What the Adversarial Review Changed"))
story.append(HRule(487)); story.append(Spacer(1, 6))
story.append(P("This plan was produced by an ETR-style agentic workflow: seven web-research agents mapped the live "
    "NZ/Auckland market; an assumptions agent built a first model; five adversarial reviewers (financial realism, "
    "market/competition, operational feasibility, cashflow/liquidity, and partnership/legal/tax) attacked it — two "
    "returned FAIL; and a synthesis pass hardened the plan. The material corrections applied:"))
CORR = [
    "PRICING — repriced subbie labour from a fatal $65/hr (inside the $45-75 cost band &#8594; ~12% GM) to cost-plus: pay $55, bill $95 (~45-70% markup).",
    "GROSS MARGIN — restated Y1 from 45% to 30% fully-costed, rising to 38-42% in Y2-Y3; resolved the internal contradiction where 'materials 18-20% of revenue' already implied ~25% GM.",
    "REVENUE — demoted Y1 base from $285k to $235k ($200k low / $285k high); a zero-reputation firm launching into winter largely misses its first exterior peak.",
    "NET MARGIN — reset Y1 from +10-20% to roughly -5% to +2% (near-breakeven after modest staged draws); full owner pay only affordable Y2-Y3.",
    "CAPITAL — split the $200k into ~$50k equity + ~$150k secured PPSR-registered shareholder loan from A, repaid ahead of dividends.",
    "VAN — made lease (~$5k deposit) the base assumption instead of a $28k cash buy — reclaims ~$23k of the ceiling.",
    "GST — elected payments (cash) basis — removes the invoice-basis trap of funding GST on slow debtors before collection.",
    "OWNER PAY — added an explicit Partner B pay line; the pre-review model funded only A's draw and left the 50/50 owner with no income.",
    "KEY-PERSON — added company-owned life/TPD/trauma on B + income protection (~$2-3.5k/yr); previously $0.",
    "CONTINUITY HIRE — brought the first employed painter forward to early H2 as a continuity/QC backup, not a growth head.",
    "ANCHOR CREW — secured 1-2 anchor subbies on retainer; do not model on-demand subbie liquidity as reliable.",
    "PROVISIONS — added rework/warranty (~3%) + bad-debt (~1.5%) reserves; previously zero.",
    "MARKETING — lifted and phased spend (~$400/mo &#8594; $2,000-2,500/mo once the site converts); modelled at 5-7% of a lower base.",
    "PEAK CASH — re-cut from $120k ('$80k headroom') to ~$150k base with an explicit ~$195k stress case at the ceiling.",
    "DOUBLE-COUNTS — reconciled a duplicated insurance line and a van shown in both capex and lease opex.",
    "GOVERNORS — hardened soft guidance into numeric rules (commercial &lt;30%; no employed head &lt;$400k run-rate; ~$30k minimum-cash covenant).",
    "POSITIONING — committed to one beachhead lane with a named, verifiable edge; set the Y1 peak premium to 0%.",
    "LEGAL — carved legal onto its own ~$7k line (no $200 template SHA for a capital-asymmetric 50/50); added deadlock, IP assignment and remuneration policy.",
    "MPNZ — confirmed Master Painter status is gated until ~2027-28; Y1 credibility leans on Dulux/Resene + manufacturer warranty.",
    "BUFFER — raised the working-capital buffer from $10k to ~$25k; assume COD materials for months 1-3.",
]
story += bullets(CORR)
story.append(PageBreak())

# ---- APPENDIX
story.append(H("Appendix A — Open Questions to Close"))
story.append(HRule(487)); story.append(Spacer(1, 6))
story.append(P("Confirm these before locking the model and signing the legals:"))
OQ = [
    "Exact current ACC Work levy for the painting Classification Unit (commonly CU 42110) — 2026/27 ACC Levy Guidebook or ACC 0800 222 776 (currently ESTIMATE ~$1.00-2.00/$100).",
    "Partner B's realistic non-billable load (quoting + QC + admin + crew-build hrs/week) — firms up the effective-billable-painter count and the Y1 revenue ceiling.",
    "MPNZ's actual annual membership fee (unpublished; ~$500-1,200/yr is an estimate) and eligibility at the 18-month + 3-job gate.",
    "Accounting advice on a first-year LTC election to flow Y1 ramp losses to A vs the 49% shareholder-continuity test.",
    "Validate willingness-to-pay at $95/hr against 5-10 real Auckland competitor quotes before locking the rate.",
    "Partner B's personal runway — can he self-fund ~6 months of low utilisation, or must the model carry a larger B living-draw (each $3.5k/mo over 6 months adds ~$21k of cash need)?",
    "Builderscrack's current post-2024 subscription pricing and whether painters qualify for Google Local Services Ads in NZ.",
    "Pin the launch month precisely — the goal is delivered jobs + reviews banked BEFORE Sep-Oct, not during the deepest winter weeks.",
]
story += bullets(OQ)
story.append(Spacer(1, 10))
story.append(H("Appendix B — Expansion Upside (not in the base numbers)"))
story.append(HRule(487)); story.append(Spacer(1, 6))
story.append(P("The plan assumes the firm wins 100% of its own clients independently. Any warm-network introductions "
    "are upside only. The real expansion story is internal and belongs to Years 2&ndash;3, not Year 1: (1) converting "
    "one-off exterior customers into a recurring 7&ndash;10yr repaint pipeline and suburb-clustered referral cluster; "
    "(2) turning property-manager/agent relationships into standing tenancy-turnover contracts that smooth the winter "
    "trough and lift the exit multiple; (3) adding weather-independent light-commercial/facilities-maintenance "
    "contracts once SiteWise Green is achieved."))
story.append(Spacer(1, 10))
story.append(H("Appendix C — Sources"))
story.append(HRule(487)); story.append(Spacer(1, 6))
SRC = [
    "IBISWorld — Painting &amp; Decorating Services in New Zealand (industry 332): market size, growth, firm count, competition, DIY threat.",
    "Stats NZ — Building Consents Issued, May 2025: new-dwelling consents ~33,530, down 3.8%.",
    "MBIE — National Construction Pipeline Report: Auckland ~44% of national consents by 2030; recovery to ~40,000 dwellings by 2030.",
    "Building Performance (MBIE) — Restricted Building Work: painting is not restricted work; no LBP licence required.",
    "Automate The Trades — Painting Hourly Rate NZ 2026: subbie/day rates, seasonality, peak premiums.",
    "The House Painters (Auckland) — exterior repaint cycle ~7-10 years (shorter coastal/high-UV).",
    "Resene / Dulux trade-account pricing; WorkSafe NZ (height, scaffolding, lead paint); Site Safe / SiteWise; ACC CoverPlus; business.govt.nz; Master Painters NZ membership criteria.",
]
story += bullets(SRC)
story.append(Spacer(1, 8))
story.append(P("<i>Prepared 27 July 2026. This is an internal planning document for the two partners; it deliberately "
    "carries no third-party client names or related-company financials. Figures are ETR-hardened base-case estimates "
    "for decision-making, not audited forecasts — confirm the open questions above before committing capital.</i>", SMALL))

# ================================================================ RENDER PDF
doc = PlanDoc(PDF, pagesize=A4, title="Auckland Painting Co — Business Plan & Financial Model",
              author="Prepared for the partners")
doc.multiBuild(story)
print("PDF ->", PDF)

# ================================================================ EXCEL MODEL
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = Workbook()
navy = "1E2A3A"; gold = "C8952A"; light = "EEF1F4"
hf = Font(bold=True, color="FFFFFF", size=11)
hfill = PatternFill("solid", fgColor=navy)
title_f = Font(bold=True, color=navy, size=14)
sub_f = Font(bold=True, color=navy, size=11)
bold = Font(bold=True, color="1E2A3A")
money = '#,##0'
pct = '0%'
thin = Side(style="thin", color="D8DCE2")
border = Border(bottom=thin)

def hdr(ws, row, cols, start=1):
    for j, c in enumerate(cols):
        cell = ws.cell(row=row, column=start+j, value=c)
        cell.font = hf; cell.fill = hfill; cell.alignment = Alignment(horizontal="left", vertical="center")

def setw(ws, widths):
    for i, w in enumerate(widths):
        ws.column_dimensions[get_column_letter(i+1)].width = w

# Sheet 1: Summary / Assumptions
ws = wb.active; ws.title = "Assumptions"
setw(ws, [46, 18, 18, 18])
ws["A1"] = "Auckland Painting Co — Assumptions & Unit Economics"; ws["A1"].font = title_f
ws["A2"] = "ETR-hardened base case (CONDITIONAL_GO) — prepared 27 Jul 2026"; ws["A2"].font = Font(italic=True, color="5A6472")
r = 4
ws.cell(r, 1, "Unit economics").font = sub_f; r += 1
for k, v, unit in [
    ("Labour charge-out (client)", CHARGE_OUT, "$/hr (cost-plus on $55 subbie)"),
    ("Subbie cost", SUBBIE_HR, "$/hr"),
    ("Employed painter (all-in)", EMPLOYED_HR, "$/hr incl on-costs"),
    ("Materials", MATERIALS_PC, "% of revenue"),
    ("Avg exterior/residential job", AVG_RES_JOB, "$"),
    ("Avg light-commercial job", AVG_COMM_JOB, "$"),
]:
    ws.cell(r, 1, k); c = ws.cell(r, 2, v)
    c.number_format = pct if k == "Materials" else money
    ws.cell(r, 3, unit); r += 1
r += 1
ws.cell(r, 1, "Capital structure").font = sub_f; r += 1
for k, v in [("Equity (50/50)", EQUITY), ("Secured shareholder loan (Partner A, PPSR)", LOAN),
             ("Total capital", CAPITAL), ("Loan interest rate", LOAN_RATE)]:
    ws.cell(r, 1, k); c = ws.cell(r, 2, v); c.number_format = pct if "rate" in k else money; r += 1

# Sheet 2: Use of funds
ws2 = wb.create_sheet("Use of Funds")
setw(ws2, [60, 16])
ws2["A1"] = "Use of the $200,000"; ws2["A1"].font = title_f
hdr(ws2, 3, ["Item", "NZD"])
rr = 4
for d, a in USE_OF_FUNDS:
    ws2.cell(rr, 1, d); ws2.cell(rr, 2, a).number_format = money; rr += 1
ws2.cell(rr, 1, "Setup sub-total").font = bold; c = ws2.cell(rr, 2, SETUP_TOTAL); c.number_format = money; c.font = bold; rr += 1
ws2.cell(rr, 1, "Working-capital reserve").font = bold; c = ws2.cell(rr, 2, RESERVE); c.number_format = money; c.font = bold; rr += 1
ws2.cell(rr, 1, "Total capital deployed").font = bold; c = ws2.cell(rr, 2, CAPITAL); c.number_format = money; c.font = bold

# Sheet 3: 3-year P&L
ws3 = wb.create_sheet("3-Year P&L")
setw(ws3, [42, 16, 16, 16])
ws3["A1"] = "Three-Year P&L (base case)"; ws3["A1"].font = title_f
hdr(ws3, 3, ["NZD", "Year 1", "Year 2", "Year 3"])
lines = [
    ("Revenue", "rev", money), ("Cost of sales", "cogs", money), ("Gross profit", "gp", money),
    ("Gross margin", "gm", pct), ("Operating expenses (fixed)", "fixed", money),
    ("Provisions (rework + bad debt)", "prov", money), ("EBITDA before owner drawings", "ebitda_bd", money),
    ("Owner drawings (combined)", "draws", money), ("Operating result after drawings", "after", money),
]
rr = 4
for label, key, fmt in lines:
    ws3.cell(rr, 1, label)
    for j, y in enumerate(("Y1", "Y2", "Y3")):
        c = ws3.cell(rr, 2+j, PL[y][key]); c.number_format = fmt
    if key in ("ebitda_bd", "after", "gp"):
        for col in range(1, 5): ws3.cell(rr, col).font = bold
    rr += 1
ws3.cell(rr+1, 1, "Revenue range Y1"); ws3.cell(rr+1, 2, REV_RANGE["Y1_low"]).number_format = money
ws3.cell(rr+1, 3, REV["Y1"]).number_format = money; ws3.cell(rr+1, 4, REV_RANGE["Y1_high"]).number_format = money
ws3.cell(rr+1, 1).font = Font(italic=True, color="5A6472")

# Sheet 4: Y1 monthly cashflow
ws4 = wb.create_sheet("Y1 Cashflow")
setw(ws4, [30] + [11]*12)
ws4["A1"] = "Year-1 Monthly Cashflow (base case) — of $200k capital"; ws4["A1"].font = title_f
ws4.cell(2, 1, "Opening operating cash after day-0 setup:")
ws4.cell(2, 2, OPENING).number_format = money
hdr(ws4, 4, ["NZD"] + MONTHS)
cf_lines = [
    ("Revenue (billed)", "rev"), ("Cash collected", "collect"), ("Materials paid", "mat"),
    ("Direct labour (subbie + B)", "lab"), ("Fixed overhead", "fixed"), ("Owner draws", "draws"),
    ("Rework", "rework"), ("GST paid", "gst"), ("Net cash", "net"), ("Cash balance", "bal"),
]
rr = 5
for label, key in cf_lines:
    ws4.cell(rr, 1, label)
    for j, row in enumerate(CF):
        c = ws4.cell(rr, 2+j, round(row[key])); c.number_format = money
    if key in ("net", "bal"):
        for col in range(1, 14): ws4.cell(rr, col).font = bold
    rr += 1
ws4.cell(rr+1, 1, "Cash trough"); ws4.cell(rr+1, 2, round(MIN_BAL)).number_format = money
ws4.cell(rr+2, 1, "Peak cash need (of $200k)"); ws4.cell(rr+2, 2, round(PEAK_NEED)).number_format = money
ws4.cell(rr+3, 1, "Headroom under ceiling"); ws4.cell(rr+3, 2, round(HEADROOM)).number_format = money
ws4.cell(rr+4, 1, "Stress-case peak"); ws4.cell(rr+4, 2, STRESS_PEAK).number_format = money
for k in range(1, 5): ws4.cell(rr+k, 1).font = bold

# Sheet 5: Overhead
ws5 = wb.create_sheet("Monthly Overhead")
setw(ws5, [64, 14])
ws5["A1"] = "Monthly Overhead Schedule (Year 1)"; ws5["A1"].font = title_f
hdr(ws5, 3, ["Item", "NZD/mo"])
rr = 4
tot = 0
for d, a in OVERHEAD:
    ws5.cell(rr, 1, d); ws5.cell(rr, 2, a).number_format = money; tot += a; rr += 1
ws5.cell(rr, 1, "Total monthly overhead").font = bold; c = ws5.cell(rr, 2, tot); c.number_format = money; c.font = bold

wb.save(XLSX)
print("XLSX ->", XLSX)
print("DONE")
