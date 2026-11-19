#!/usr/bin/env python3
"""One-page board summary of the HOTC Data-Intelligence & AI strategy. ASG house
style (navy + gold), single A4 page, circulate-ready. No tinted callout boxes."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, HRFlowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib

OUT = "/Users/ahmadduais/Desktop/ASG/HOTC-Reporting-App/HOTC_DataIntelligence_Board_OnePager.pdf"

_ttf = os.path.join(matplotlib.get_data_path(), "fonts", "ttf")
try:
    pdfmetrics.registerFont(TTFont("DejaVu", os.path.join(_ttf, "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", os.path.join(_ttf, "DejaVuSans-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVu-Oblique", os.path.join(_ttf, "DejaVuSans-Oblique.ttf")))
    pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold", italic="DejaVu-Oblique")
    F, FB, FI = "DejaVu", "DejaVu-Bold", "DejaVu-Oblique"
except Exception:
    F, FB, FI = "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"

NAVY = colors.HexColor("#1F3864"); GOLD = colors.HexColor("#C8952A")
INK = colors.HexColor("#243244"); GREY = colors.HexColor("#5A6675")
LIGHT = colors.HexColor("#EEF2F6"); FAINT = colors.HexColor("#C9D2DC"); WHITE = colors.white

PAGE_W, PAGE_H = A4
LM = RM = 40; BM = 34
HEADER_H = 96  # navy band height from top

def S(name, **kw):
    base = dict(fontName=F, textColor=INK, fontSize=8.9, leading=11.4); base.update(kw)
    return ParagraphStyle(name, **base)

LEAD = S("LEAD", fontSize=9.2, leading=12.6, alignment=TA_JUSTIFY, spaceAfter=2)
BODY = S("BODY", fontSize=8.8, leading=11.3, alignment=TA_JUSTIFY)
H = S("H", fontName=FB, fontSize=9.4, textColor=NAVY, leading=11.5, spaceBefore=2, spaceAfter=1)
CELL = S("CELL", fontSize=8.3, leading=10.3)
CELLB = S("CELLB", fontName=FB, fontSize=8.3, leading=10.3, textColor=NAVY)
CELLH = S("CELLH", fontName=FB, fontSize=8.3, leading=10.3, textColor=WHITE)
BUL = S("BUL", fontSize=8.5, leading=10.7, leftIndent=9, bulletIndent=1, spaceAfter=1.5)
SMALL = S("SMALL", fontSize=7.3, textColor=GREY, leading=9)

FRAME_W = PAGE_W - LM - RM

def bullets(items, style=BUL):
    return [Paragraph(t, style, bulletText="•") for t in items]

def para(t, style=BODY): return Paragraph(t, style)

story = []

# Lead / recommendation
story.append(Paragraph(
    "<b>Recommendation:</b> build <b>data intelligence</b> as the core of the platform — it is the "
    "<b>moat and the monetiser</b>, not a feature. Proceed <b>conditionally</b>: the enabling decisions "
    "cost almost nothing today and are near-impossible to retrofit, so lock them before the next contract.",
    LEAD))
story.append(Spacer(1, 4))

# THE OPPORTUNITY
story.append(Paragraph("THE OPPORTUNITY — “Auror for precincts”", H))
story.append(Paragraph(
    "BIDs today buy footfall analytics and log incidents <b>separately</b>; nobody fuses them into "
    "deployment, roster and funding intelligence. ASG uniquely owns <b>both inputs</b> — the incident data "
    "<i>and</i> the patrol/deployment data. <b>The moat is the dataset + models, not the app</b> — a "
    "services→SaaS re-rating (~4–6× EBITDA → ~4–10× revenue). The category is proven and fundable (Auror: NZ$82M raised).",
    BODY))
story.append(Spacer(1, 5))

# THREE-TIER ARCHITECTURE
story.append(Paragraph("HOW IT FITS — a three-tier data architecture (keeps ASG a compliant processor; HOTC owns its data)", H))
tier_rows = [
    [Paragraph("Tier", CELLH), Paragraph("What", CELLH), Paragraph("Basis / status", CELLH)],
    [Paragraph("<b>A</b> · Per-client analytics", CELLB), Paragraph("Each client gets AI reports on <i>their own</i> data", CELL), Paragraph("Processor; within purpose — <b>ships now</b>", CELL)],
    [Paragraph("<b>B</b> · Cross-client benchmarking", CELLB), Paragraph("“Your precinct vs national average”", CELL), Paragraph("De-identified + confidentialised; <b>opt-in</b>", CELL)],
    [Paragraph("<b>C</b> · ASG owns software+models", CELLB), Paragraph("Engine, models & anonymised layer = the asset", CELL), Paragraph("<b>The moat</b> — no identifiable data pooled", CELL)],
]
t = Table(tier_rows, colWidths=[FRAME_W*0.24, FRAME_W*0.40, FRAME_W*0.36])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), NAVY), ("LINEBELOW", (0,0), (-1,0), 0.8, GOLD),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT]), ("GRID", (0,1), (-1,-1), 0.35, FAINT),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4),
    ("TOPPADDING",(0,0),(-1,-1),2.6),("BOTTOMPADDING",(0,0),(-1,-1),2.6),
]))
story.append(t)
story.append(Spacer(1, 6))

# SHIP -> MONETISE -> MOAT
smm = [[Paragraph("SHIP FIRST", CELLH), Paragraph("MONETISE", CELLH), Paragraph("THE MOAT", CELLH)],
       [Paragraph("Impact Report · hotspot · roster optimisation — <i>data we already hold</i>", CELL),
        Paragraph("The <b>levy/funding business-case pack</b> — a BID can’t get it elsewhere & needs it to survive its re-ballot", CELL),
        Paragraph("Opt-in anonymised cross-precinct <b>benchmarking network</b> (needs a 2nd BID)", CELL)]]
t2 = Table(smm, colWidths=[FRAME_W/3.0]*3)
t2.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), NAVY), ("LINEBELOW", (0,0), (-1,0), 0.8, GOLD),
    ("BACKGROUND", (0,1), (-1,1), WHITE), ("GRID", (0,0), (-1,-1), 0.35, FAINT),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4),
    ("TOPPADDING",(0,0),(-1,-1),2.6),("BOTTOMPADDING",(0,0),(-1,-1),2.6),
]))
story.append(t2)
story.append(Spacer(1, 7))

# TWO-COLUMN: AI + red line  |  what it needs
ai_col = [Paragraph("THE AI POWERHOUSE", H)]
ai_col += bullets([
    "<b>LLM data-grounded reports</b> over a governed <b>semantic layer</b> (fails <i>loudly</i>, not silently) — auto-drafts the funding pack, human-signed",
    "Anomaly/trend detection; <b>roster optimisation</b> = our existing OR solver (mature, not hype)",
])
ai_col.append(Paragraph(
    "<b>THE RED LINE — predict places &amp; times, never people.</b> No person scores, no demographics, no profiling "
    "(EU AI Act Art 5; PredPol matched crime &lt;1%). It’s also the <i>more effective</i> use.", BODY))

need_col = [Paragraph("WHAT IT NEEDS", H)]
need_col += bullets([
    "<b>Capability, not cost:</b> ~2–3 net FTE (data engineer, fractional product owner, analytics/ML contractor, fractional privacy counsel) before Phase 2",
    "A <b>2nd BID</b> signed & opted into benchmarking before the moat is real",
    "NZ privacy-lawyer sign-off on the data-rights model",
    "Phase-gate capital — release on milestones",
])
two = Table([[ai_col, need_col]], colWidths=[FRAME_W*0.54, FRAME_W*0.46])
two.setStyle(TableStyle([
    ("VALIGN",(0,0),(-1,-1),"TOP"),
    ("LEFTPADDING",(0,0),(0,0),0),("RIGHTPADDING",(0,0),(0,0),10),
    ("LEFTPADDING",(1,0),(1,0),10),("RIGHTPADDING",(1,0),(1,0),0),
    ("LINEBEFORE",(1,0),(1,0),0.5,FAINT),
    ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),
]))
story.append(two)
story.append(Spacer(1, 7))

# LOCK NOW
story.append(Paragraph("LOCK NOW — before the HOTC MVP contract (near-free today, un-retrofittable later)", H))
lock = [[Paragraph("1", CELLH), Paragraph("Draft the <b>IPP 1 purpose</b> to include “analytics, reporting &amp; benchmarking”", CELL)],
        [Paragraph("2", CELLH), Paragraph("Build the MVP on a <b>clean semantic / metrics data model</b> from day one (so AI reports can be grounded)", CELL)],
        [Paragraph("3", CELLH), Paragraph("Put the <b>anonymised-aggregated-data licence + AI-training clauses</b> in the Phase-0 contract", CELL)]]
t3 = Table(lock, colWidths=[16, FRAME_W-16])
t3.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(0,-1),NAVY), ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("ROWBACKGROUNDS",(1,0),(1,-1),[WHITE,LIGHT]), ("LINEBELOW",(1,0),(1,-1),0.35,FAINT),
    ("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4),
    ("TOPPADDING",(0,0),(-1,-1),2.8),("BOTTOMPADDING",(0,0),(-1,-1),2.8),
]))
story.append(t3)
story.append(Spacer(1, 7))

# THE ASK
story.append(HRFlowable(width="100%", thickness=1.1, color=GOLD, spaceBefore=1, spaceAfter=4))
story.append(Paragraph(
    "<b>THE DECISION:</b> approve <b>(a)</b> the three now-locks and <b>(b)</b> the three-tier architecture as policy — "
    "near-zero cost, preserves the entire upside — and commit the phased build <b>in tranches</b> as milestones clear "
    "(PIA → funding pack used in a real re-ballot → 2nd BID). One red line, enforced from day one: <b>places and times, never people.</b>",
    S("ASK", fontSize=8.9, leading=11.6, alignment=TA_JUSTIFY)))
story.append(Spacer(1, 3))
story.append(Paragraph(
    "Board-confidential · Verdict: CONDITIONAL GO · Full 10-page strategy &amp; ETR cross-model analysis available on request · "
    "Privacy/legal points are analyst readings to be confirmed by a NZ privacy lawyer before external use.", SMALL))


def header(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY); canvas.rect(0, PAGE_H-HEADER_H, PAGE_W, HEADER_H, fill=1, stroke=0)
    canvas.setFillColor(GOLD); canvas.rect(0, PAGE_H-HEADER_H-5, PAGE_W, 5, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#AEBAD0")); canvas.setFont(FB, 8.5)
    canvas.drawString(LM, PAGE_H-26, "ABSOLUTE SECURITY GROUP  ·  BOARD SUMMARY")
    canvas.setFillColor(WHITE); canvas.setFont(FB, 19)
    canvas.drawString(LM, PAGE_H-52, "Data Intelligence & AI")
    canvas.setFillColor(colors.HexColor("#E7D6AE")); canvas.setFont(FB, 10.5)
    canvas.drawString(LM, PAGE_H-70, "Strategy for the HOTC Reporting Platform")
    canvas.setFillColor(colors.HexColor("#AEBAD0")); canvas.setFont(F, 8)
    canvas.drawString(LM, PAGE_H-86, "8 September 2026")
    # verdict pill (right)
    pw, ph = 150, 30; px = PAGE_W - RM - pw; py = PAGE_H - 58
    canvas.setStrokeColor(GOLD); canvas.setLineWidth(1.2); canvas.setFillColor(NAVY)
    canvas.roundRect(px, py, pw, ph, 5, stroke=1, fill=1)
    canvas.setFillColor(colors.HexColor("#AEBAD0")); canvas.setFont(F, 7)
    canvas.drawCentredString(px+pw/2, py+18, "VERDICT")
    canvas.setFillColor(WHITE); canvas.setFont(FB, 12.5)
    canvas.drawCentredString(px+pw/2, py+5, "CONDITIONAL GO")
    canvas.restoreState()

frame = Frame(LM, BM, FRAME_W, PAGE_H - HEADER_H - 12 - BM, id="m",
              leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=LM, rightMargin=RM, topMargin=HEADER_H+12, bottomMargin=BM,
                      title="Data Intelligence & AI — Board Summary", author="Absolute Security Group")
doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=header)])
doc.build(story)
print("WROTE", OUT)
