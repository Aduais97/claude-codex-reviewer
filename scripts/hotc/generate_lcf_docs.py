#!/usr/bin/env python3
"""
Generate the two HOTC x ASG LCF pilot deliverables:
  1. LCF_Scope_of_Works.pdf          -- engagement schedule / scope of works (the "paperwork to lock down")
  2. LCF_Data_Capture_Tracker.xlsx   -- daily activity + business-engagement + KPI tracker, live from 2 June

House style: ReportLab, navy (#1B2A4A) + gold (#D4A843), Helvetica, A4.
Outputs to ~/Desktop/ASG/HOTC/2026/. Script lives in the Dev/Claude repo (no working files left in data folders).
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable, Frame, PageTemplate,
)

OUT_DIR = os.path.expanduser("~/Desktop/ASG/HOTC/2026")

# ── Palette ───────────────────────────────────────────────────────────────
NAVY      = HexColor('#1B2A4A')
DARK_BLUE = HexColor('#2C3E6B')
MID_BLUE  = HexColor('#4A6FA5')
LIGHT_BLUE= HexColor('#E8EDF5')
ACCENT    = HexColor('#D4A843')
BG_GREY   = HexColor('#F7F8FA')
BORDER    = HexColor('#D0D5DD')
TEXT_DARK = HexColor('#1A1A2E')
TEXT_MED  = HexColor('#4A4A5A')
TEXT_LIGHT= HexColor('#7A7A8A')
ROW_ALT   = HexColor('#F2F4F8')

W, H = A4
ML, MR, MT, MB = 54, 54, 64, 56
CONTENT_W = W - ML - MR

def san(t):
    if not t:
        return ""
    reps = {'—': '–', '‘': '’', '’': '’',
            '“': '”', '…': '...'}
    for k, v in reps.items():
        t = t.replace(k, v)
    return t

# ── Styles ────────────────────────────────────────────────────────────────
def styles():
    s = {}
    s['body'] = ParagraphStyle('body', fontName='Helvetica', fontSize=10, leading=14.5,
                               textColor=TEXT_DARK, alignment=TA_JUSTIFY, spaceAfter=6, spaceBefore=2)
    s['body_l'] = ParagraphStyle('body_l', parent=s['body'], alignment=TA_LEFT)
    s['bold'] = ParagraphStyle('bold', parent=s['body'], fontName='Helvetica-Bold')
    s['bullet'] = ParagraphStyle('bullet', parent=s['body'], leftIndent=16, bulletIndent=4,
                                 alignment=TA_LEFT, spaceAfter=3, spaceBefore=1)
    s['h1'] = ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=20, leading=24,
                             textColor=NAVY, spaceBefore=0, spaceAfter=4)
    s['h2'] = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=13.5, leading=17,
                             textColor=NAVY, spaceBefore=15, spaceAfter=6)
    s['h3'] = ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=11, leading=14,
                             textColor=DARK_BLUE, spaceBefore=10, spaceAfter=4)
    s['cell'] = ParagraphStyle('cell', fontName='Helvetica', fontSize=8.8, leading=11.5, textColor=TEXT_DARK)
    s['cell_b'] = ParagraphStyle('cell_b', parent=s['cell'], fontName='Helvetica-Bold')
    s['cell_w'] = ParagraphStyle('cell_w', parent=s['cell'], textColor=white, fontName='Helvetica-Bold')
    s['quote'] = ParagraphStyle('quote', fontName='Helvetica-Oblique', fontSize=10.5, leading=15,
                                textColor=NAVY, leftIndent=14, rightIndent=14, spaceBefore=4, spaceAfter=8)
    s['small'] = ParagraphStyle('small', fontName='Helvetica', fontSize=8, leading=10.5, textColor=TEXT_MED)
    s['footer'] = ParagraphStyle('footer', fontName='Helvetica', fontSize=7.5, leading=9,
                                 textColor=TEXT_LIGHT, alignment=TA_CENTER)
    return s

S = styles()

def P(t, st='body'):
    return Paragraph(san(t), S[st])

def bullets(items, st='bullet'):
    return [Paragraph(san('•&nbsp;&nbsp;' + i), S[st]) for i in items]

def section_rule():
    return HRFlowable(width='100%', thickness=1.2, color=ACCENT, spaceBefore=2, spaceAfter=10)

def kv_table(rows, col_w):
    data = [[P(r[0], 'cell_b'), P(r[1], 'cell')] for r in rows]
    t = Table(data, colWidths=col_w)
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (0, -1), LIGHT_BLUE),
        ('ROWBACKGROUNDS', (1, 0), (1, -1), [ROW_WHITE := white, ROW_ALT]),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
    ]))
    return t

def grid_table(header, rows, col_w, aligns=None):
    data = [[P(h, 'cell_w') for h in header]]
    for r in rows:
        data.append([P(str(c), 'cell') for c in r])
    t = Table(data, colWidths=col_w, repeatRows=1)
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, ROW_ALT]),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('LINEBELOW', (0, 0), (-1, 0), 1.2, ACCENT),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]
    t.setStyle(TableStyle(style))
    return t

# ── Page furniture ──────────────────────────────────────────────────────────
def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(ML, MB - 14, W - MR, MB - 14)
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(TEXT_LIGHT)
    canvas.drawString(ML, MB - 26, "ASG Security  ·  Heart of the City  ·  LCF Pilot – Scope of Works  ·  Commercial in Confidence")
    canvas.drawRightString(W - MR, MB - 26, "Page %d" % doc.page)
    canvas.restoreState()

def build_pdf(path, flows):
    doc = BaseDocTemplate(path, pagesize=A4, leftMargin=ML, rightMargin=MR,
                          topMargin=MT, bottomMargin=MB, title="LCF Pilot – Scope of Works",
                          author="ASG Security")
    frame = Frame(ML, MB, CONTENT_W, H - MT - MB, id='main')
    doc.addPageTemplates([PageTemplate(id='main', frames=[frame], onPage=footer)])
    doc.build(flows)

# ── Cover band ────────────────────────────────────────────────────────────
def cover_band():
    band = Table([[Paragraph(
        '<font color="#FFFFFF"><b>ASG SECURITY</b></font>', S['body'])]],
        colWidths=[CONTENT_W], rowHeights=[26])
    band.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NAVY),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('LINEBELOW', (0, 0), (-1, -1), 2, ACCENT),
    ]))
    return band

# ════════════════════════════════════════════════════════════════════════════
#  SCOPE OF WORKS PDF
# ════════════════════════════════════════════════════════════════════════════
def scope_pdf():
    f = []
    f.append(cover_band())
    f.append(Spacer(1, 16))
    f.append(P("Enhanced CBD Safety Team", 'h1'))
    f.append(P("Local Crime Fund (LCF) Pilot – Scope of Works &amp; Engagement Schedule", 'h3'))
    f.append(section_rule())
    f.append(kv_table([
        ("Provider", "Absolute Security Group Ltd (ASG Security), 220 Queen Street, Auckland CBD"),
        ("Funding holder", "Heart of the City Incorporated (HOTC), Level 23, 151 Queen Street, Auckland"),
        ("Funding source", "Local Crime Fund (LCF) – Proceeds of Crime Fund (PoCF) objective, joint-administered"),
        ("Initiative", "Targeted CPTED-based safety pilot across the Auckland City Centre precinct"),
        ("Pilot period", "2 June 2026 – 24 July 2026"),
        ("Total funding", "$41,150 + GST  ($47,322.50 incl. GST)"),
        ("Prepared", "June 2026  ·  Commercial in Confidence"),
    ], [120, CONTENT_W - 120]))

    # 1. Purpose
    f.append(P("1.&nbsp;&nbsp;Purpose &amp; Background", 'h2'))
    f.append(P("Since March 2024, ASG Security has delivered 24/7 safety patrols across the Heart of the City "
               "precinct, building trusted relationships with businesses, the public and Auckland's vulnerable "
               "community – a welfare-first approach delivering measurable results (a 41% reduction in police "
               "callouts and a 29% reduction in public-drinking incidents year-on-year)."))
    f.append(P("Under this LCF allocation, ASG will deploy an additional CBD Safety Team during peak-risk periods. "
               "The initiative is framed as a defined, evidence-generating pilot:"))
    f.append(Paragraph(san('“This pilot delivers a targeted CPTED-based intervention, increasing visible '
                           'guardianship, improving natural surveillance, and strengthening business-community '
                           'safety networks during peak risk periods.”'), S['quote']))
    f.append(P("The pilot is designed to identify peak-risk windows, test visible-deterrence impact, and build a "
               "scalable safety model for the post-City Rail Link (CRL) environment.", 'small'))

    # 2. Scope of services
    f.append(P("2.&nbsp;&nbsp;Scope of Services", 'h2'))
    f.append(P("Enhanced Safety Team deployment", 'h3'))
    f.extend(bullets([
        "A dedicated additional Safety Team deployed seven days, covering peak trading hours "
        "(09:00–17:00 weekdays) with weekend daytime support (09:00–18:00).",
        "A targeted peak-risk uplift pool deployed flexibly to documented hotspots – Queen Street, "
        "Aotea Square, and the Hobson/Victoria corner – concentrated on the highest-risk evening windows "
        "(Thursday–Saturday).",
    ]))
    f.append(P("Business Engagement Programme", 'h3'))
    f.append(P("Two to three ASG operational managers, including the CEO, will conduct face-to-face visits with "
               "businesses across the precinct to introduce the initiative and its objectives, understand "
               "store-level safety concerns, and reinforce Heart of the City's commitment to the safety and "
               "wellbeing of staff and customers."))
    f.append(P("Provided by ASG at no cost to the fund", 'h3'))
    f.extend(bullets([
        "All uniforms for the additional team – available and ready for deployment.",
        "Operational management oversight and supervision.",
        "Camera / surveillance support.",
    ]))

    # 3. Deployment schedule
    f.append(P("3.&nbsp;&nbsp;Indicative Deployment Schedule", 'h2'))
    f.append(P("The funded pool equates to approximately <b>1,115 service hours</b> at the contracted rate, "
               "deployed across the pilot. Exact rostering is set by ASG operations and flexed to live hotspot "
               "intelligence; the indicative weekly pattern is:", 'body'))
    f.append(grid_table(
        ["Coverage line", "Days", "Window", "Hrs/day", "Hrs/wk"],
        [
            ["Safety Officer 1", "Mon–Fri", "09:00–17:00", "8.0", "40"],
            ["Safety Officer 1", "Sat–Sun", "09:00–18:00", "9.0", "18"],
            ["Safety Officer 2", "Mon–Fri", "09:00–17:00", "8.0", "40"],
            ["Safety Officer 2", "Sat–Sun", "09:00–18:00", "9.0", "18"],
            ["Peak-risk uplift (hotspots)", "Thu–Sat", "evening, flexed", "~", "~33"],
            ["Indicative weekly total", "", "", "", "~149"],
        ],
        [150, 70, 95, 50, CONTENT_W - 415]))
    f.append(Spacer(1, 4))
    f.append(P("~149 hrs/week × ~7.5 weeks (2 Jun – 24 Jul) ≈ 1,115 hrs = $41,150 + GST, fully "
               "committed within the pilot period.", 'small'))

    # 4. Commercial terms
    f.append(P("4.&nbsp;&nbsp;Commercial Terms &amp; Invoicing", 'h2'))
    f.append(kv_table([
        ("Contracted rate", "$36.90 + GST per hour (existing HOTC contract rate)"),
        ("Funded hours", "~1,115 hours across the pilot period"),
        ("Total value", "$41,150 + GST  =  $47,322.50 incl. GST"),
    ], [120, CONTENT_W - 120]))
    f.append(Spacer(1, 6))
    f.append(P("Funds are committed and invoiced in full before 30 June 2026, in two equal instalments, "
               "consistent with the funding requirements:", 'body'))
    f.append(grid_table(
        ["Invoice", "Timing", "Ex-GST", "Incl. GST"],
        [
            ["Invoice 1 (50%)", "On execution – early June 2026", "$20,575.00", "$23,661.25"],
            ["Invoice 2 (50%)", "Mid–late June 2026 (before 30 Jun)", "$20,575.00", "$23,661.25"],
            ["Total", "", "$41,150.00", "$47,322.50"],
        ],
        [120, 175, 90, CONTENT_W - 385]))

    # 5. Funding compliance / CPTED
    f.append(P("5.&nbsp;&nbsp;Funding Compliance – CPTED Alignment", 'h2'))
    f.append(P("Funds must be used for Crime Prevention through Environmental Design (CPTED) interventions that "
               "address crime-related harm and improve community wellbeing. The pilot maps as follows:", 'body'))
    f.append(grid_table(
        ["LCF / CPTED category", "How the pilot delivers"],
        [
            ["Territoriality &amp; access – patrols / wardens / ambassadors",
             "Additional uniformed Safety Team providing visible guardianship across the precinct in peak-risk windows."],
            ["Natural surveillance",
             "Increased patrol density improves natural surveillance of identified hotspots."],
            ["Cultural cohesion / sense of community",
             "Business Engagement Programme building business-community safety networks and collaborative approaches."],
            ["Reduction in crime / improved safety in the BID area",
             "Targeted, welfare-first deterrence in documented hotspots during peak-risk periods."],
        ],
        [165, CONTENT_W - 165]))

    # 6. KPIs
    f.append(P("6.&nbsp;&nbsp;Measurement &amp; KPIs", 'h2'))
    f.append(P("Prevention / Impact KPIs", 'h3'))
    f.extend(bullets([
        "Reduction in repeat incidents in identified hotspots.",
        "Change in time-of-day incident patterns.",
        "Reduction in calls for service / security escalation.",
    ]))
    f.append(P("Engagement KPIs", 'h3'))
    f.extend(bullets([
        "Number of businesses engaged face-to-face.",
        "Number of perceptions surveys completed (baseline and follow-up).",
        "Qualitative feedback and quotes captured (positive stories).",
    ]))
    f.append(P("Perceptions Survey KPIs", 'h3'))
    f.append(P("A short face-to-face perceptions survey is the programme's measurement instrument, run "
               "in two waves – baseline (early June) and follow-up (mid–late July) – so change is "
               "attributable to the uplift. Captured digitally; reported in the accountability report.", 'small'))
    f.extend(bullets([
        "Perceived safety – day and night/evening (1–5): baseline vs follow-up uplift.",
        "Operating confidence (1–5): baseline vs follow-up uplift.",
        "% of businesses reporting improved safety since the uplift (attribution).",
        "Customer sentiment (1–5); % that would support a continued / expanded presence.",
    ]))

    # 7. Reporting
    f.append(P("7.&nbsp;&nbsp;Reporting &amp; Accountability", 'h2'))
    f.append(P("ASG will capture activity and engagement data from day one (2 June) against the measures below, "
               "and will provide HOTC a comprehensive accountability report covering the period 2 June – "
               "24 July. The report will demonstrate how the funding achieved its purpose, addressing the required "
               "reporting themes:", 'body'))
    f.extend(bullets([
        "Effectiveness metrics (asset / surveillance / engagement).",
        "Partnership &amp; collaboration with administrators and relevant stakeholders.",
        "Improved perceptions of safety.",
        "Reduction in harm and improved wellbeing, inclusive of the wider community.",
        "Positive stories and outcomes from the initiative.",
    ]))
    f.append(grid_table(
        ["Milestone", "Date", "Owner"],
        [
            ["Pilot activity commences", "2 June 2026", "ASG"],
            ["Both invoices issued (funds committed)", "Before 30 June 2026", "ASG → HOTC"],
            ["Pilot activity concludes", "24 July 2026", "ASG"],
            ["ASG accountability report to HOTC", "27 July 2026", "ASG"],
            ["HOTC report to joint funding administrators", "31 July 2026", "HOTC"],
        ],
        [240, 130, CONTENT_W - 370]))

    # 8. Acceptance
    accept = []
    accept.append(P("8.&nbsp;&nbsp;Acceptance", 'h2'))
    accept.append(P("Agreed on behalf of the parties:", 'body'))
    sig = Table([
        [P("For ASG Security", 'cell_b'), P("For Heart of the City", 'cell_b')],
        [P("<br/><br/>______________________________", 'cell'),
         P("<br/><br/>______________________________", 'cell')],
        [P("Ahmad Duais – CEO, Absolute Security Group", 'cell'),
         P("Edward Caughey – Head of Customer Experience", 'cell')],
        [P("Date:", 'cell'), P("Date:", 'cell')],
    ], colWidths=[CONTENT_W / 2, CONTENT_W / 2])
    sig.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    accept.append(sig)
    f.append(KeepTogether(accept))

    build_pdf(os.path.join(OUT_DIR, "LCF_Scope_of_Works.pdf"), f)
    print("PDF  ->", os.path.join(OUT_DIR, "LCF_Scope_of_Works.pdf"))


# ════════════════════════════════════════════════════════════════════════════
#  DATA-CAPTURE TRACKER XLSX
# ════════════════════════════════════════════════════════════════════════════
def tracker_xlsx():
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    NAVY_X = "1B2A4A"
    GOLD_X = "D4A843"
    LIGHT_X = "E8EDF5"
    GREY_X = "F2F4F8"

    hfont = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
    hfill = PatternFill("solid", fgColor=NAVY_X)
    title_font = Font(name="Calibri", bold=True, color=NAVY_X, size=15)
    sub_font = Font(name="Calibri", bold=True, color=NAVY_X, size=11)
    note_font = Font(name="Calibri", italic=True, color="4A4A5A", size=10)
    thin = Side(style="thin", color="D0D5DD")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    wrap = Alignment(wrap_text=True, vertical="top")
    center = Alignment(horizontal="center", vertical="center")

    wb = Workbook()

    def style_header(ws, row, ncols):
        for c in range(1, ncols + 1):
            cell = ws.cell(row=row, column=c)
            cell.font = hfont
            cell.fill = hfill
            cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
            cell.border = border

    def set_widths(ws, widths):
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w

    # ---- Sheet 1: Instructions ----
    ws = wb.active
    ws.title = "Instructions"
    ws["A1"] = "HOTC × ASG – LCF Pilot · Data-Capture Tracker"
    ws["A1"].font = title_font
    ws["A3"] = "Purpose"
    ws["A3"].font = sub_font
    ws["A4"] = ("Capture every shift and every business visit from 2 June so the 27/31 July accountability "
                "report writes itself. The funding requires evidence that the money achieved its purpose – "
                "this tracker is that evidence.")
    ws["A4"].alignment = wrap
    instr = [
        ("Daily Activity Log", "ONE row per shift, every day. Hours feed the budget tracker; incidents/move-ons/"
                               "calls feed the Prevention KPIs."),
        ("Business Engagement", "ONE row per business visited. Record confidence 1–5 before AND after, and a "
                                "short qualitative note. Feeds the Engagement KPIs."),
        ("Hotspot Incidents", "ONE row per notable incident at Queen St / Aotea / Hobson-Victoria. Used to show "
                              "reduction in repeat incidents and time-of-day shift."),
        ("KPI Dashboard", "Auto-calculates from the logs. This is the report's evidence base – do not edit "
                          "the formula cells."),
    ]
    r = 6
    ws.cell(r, 1, "Tab").font = sub_font
    ws.cell(r, 2, "How to use").font = sub_font
    for c in (1, 2):
        ws.cell(r, c).fill = PatternFill("solid", fgColor=LIGHT_X)
        ws.cell(r, c).border = border
    r += 1
    for name, how in instr:
        ws.cell(r, 1, name).font = Font(bold=True, color=NAVY_X)
        ws.cell(r, 1).border = border
        ws.cell(r, 1).alignment = wrap
        ws.cell(r, 2, how).alignment = wrap
        ws.cell(r, 2).border = border
        r += 1
    ws.cell(r + 1, 1, "Funded pool: $41,150 + GST  ·  Rate $36.90 + GST/hr  ·  ~1,115 hrs  ·  "
                      "Pilot 2 Jun – 24 Jul 2026").font = note_font
    set_widths(ws, [26, 95])

    # ---- Sheet 2: Daily Activity Log ----
    ws = wb.create_sheet("Daily Activity Log")
    cols = ["Date", "Day", "Shift window", "Officers on shift", "Hours billed",
            "Route / area", "Incidents attended", "Move-ons", "Welfare interventions",
            "Calls for service", "Police escalations", "Notes / positive stories"]
    ws.append(cols)
    style_header(ws, 1, len(cols))
    # pre-fill 60 blank rows
    for _ in range(60):
        ws.append([None] * len(cols))
    for row in ws.iter_rows(min_row=2, max_row=61, max_col=len(cols)):
        for cell in row:
            cell.border = border
            cell.alignment = wrap
    set_widths(ws, [12, 8, 16, 22, 11, 16, 13, 9, 13, 12, 12, 34])
    ws.freeze_panes = "A2"

    # ---- Sheet 3: Business Engagement ----
    ws = wb.create_sheet("Business Engagement")
    cols = ["Date", "Business name", "Contact / role", "ASG manager", "Key safety concerns raised",
            "Confidence BEFORE (1-5)", "Confidence AFTER (1-5)", "Confidence uplift",
            "Qualitative feedback", "Follow-up required"]
    ws.append(cols)
    style_header(ws, 1, len(cols))
    for i in range(60):
        rr = i + 2
        ws.append([None] * len(cols))
        # uplift formula = after - before
        ws.cell(rr, 8).value = f"=IF(AND(ISNUMBER(F{rr}),ISNUMBER(G{rr})),G{rr}-F{rr},\"\")"
    for row in ws.iter_rows(min_row=2, max_row=61, max_col=len(cols)):
        for cell in row:
            cell.border = border
            cell.alignment = wrap
    set_widths(ws, [12, 24, 20, 16, 30, 12, 12, 11, 30, 14])
    ws.freeze_panes = "A2"

    # ---- Sheet 4: Hotspot Incidents ----
    ws = wb.create_sheet("Hotspot Incidents")
    cols = ["Date", "Time", "Time band", "Hotspot", "Incident type", "Repeat? (Y/N)",
            "Action taken", "Outcome", "Reported to Police? (Y/N)", "Auror logged? (Y/N)"]
    ws.append(cols)
    style_header(ws, 1, len(cols))
    for _ in range(60):
        ws.append([None] * len(cols))
    for row in ws.iter_rows(min_row=2, max_row=61, max_col=len(cols)):
        for cell in row:
            cell.border = border
            cell.alignment = wrap
    set_widths(ws, [12, 8, 14, 20, 18, 12, 24, 22, 14, 14])
    ws.freeze_panes = "A2"

    # ---- Sheet 5: Perceptions Survey ----
    ws = wb.create_sheet("Perceptions Survey")
    cols = ["Date", "Wave (Baseline/Follow-up)", "Business name / ID", "Type", "Location",
            "Safety – DAY (1-5)", "Safety – NIGHT (1-5)", "vs 6-12 mo ago",
            "Operating confidence (1-5)", "Noticed safety team? (Y/N)",
            "Team made a difference? (Significant/Some/None/Negative)",
            "Customer sentiment (1-5)", "Support continued/expanded presence? (Y/N)",
            "Quote (positive story)", "Follow-up consent (Y + contact)"]
    ws.append(cols)
    style_header(ws, 1, len(cols))
    for _ in range(120):
        ws.append([None] * len(cols))
    for row in ws.iter_rows(min_row=2, max_row=121, max_col=len(cols)):
        for cell in row:
            cell.border = border
            cell.alignment = wrap
    set_widths(ws, [11, 16, 20, 12, 14, 11, 11, 12, 13, 12, 20, 12, 16, 30, 18])
    ws.freeze_panes = "A2"

    # ---- Sheet 6: KPI Dashboard ----
    ws = wb.create_sheet("KPI Dashboard")
    ws["A1"] = "LCF Pilot – KPI Dashboard (auto)"
    ws["A1"].font = title_font
    ws["A2"] = "Live evidence base for the 27/31 July accountability report. Figures update from the logs."
    ws["A2"].font = note_font

    def block(ws, start, title, rows):
        ws.cell(start, 1, title).font = sub_font
        ws.cell(start, 1).fill = PatternFill("solid", fgColor=LIGHT_X)
        ws.cell(start, 2).fill = PatternFill("solid", fgColor=LIGHT_X)
        ws.cell(start, 1).border = border
        ws.cell(start, 2).border = border
        rr = start + 1
        for label, formula in rows:
            ws.cell(rr, 1, label).border = border
            ws.cell(rr, 1).alignment = wrap
            c = ws.cell(rr, 2, formula)
            c.border = border
            c.alignment = center
            c.font = Font(bold=True, color=NAVY_X)
            rr += 1
        return rr + 1

    DAL = "'Daily Activity Log'"
    BE = "'Business Engagement'"
    HS = "'Hotspot Incidents'"
    PS = "'Perceptions Survey'"

    r = 4
    r = block(ws, r, "Budget & Delivery", [
        ("Total hours billed", f"=SUM({DAL}!E2:E61)"),
        ("Funded hours (target)", "=1115"),
        ("Hours remaining", "=B6-B5"),
        ("Value delivered ($ ex-GST)", "=B5*36.9"),
        ("% of funded pool delivered", "=IF(B6=0,0,B5/B6)"),
    ])
    ws["B5"].number_format = '#,##0.0'
    ws["B7"].number_format = '#,##0.0'
    ws["B8"].number_format = '$#,##0'
    ws["B9"].number_format = '0.0%'

    r = block(ws, r, "Prevention / Impact KPIs", [
        ("Total incidents attended", f"=SUM({DAL}!G2:G61)"),
        ("Total move-ons", f"=SUM({DAL}!H2:H61)"),
        ("Total welfare interventions", f"=SUM({DAL}!I2:I61)"),
        ("Total calls for service", f"=SUM({DAL}!J2:J61)"),
        ("Police escalations", f"=SUM({DAL}!K2:K61)"),
        ("Hotspot incidents logged", f"=COUNTA({HS}!A2:A61)"),
        ("Repeat incidents in hotspots", f"=COUNTIF({HS}!F2:F61,\"Y\")"),
    ])

    r = block(ws, r, "Engagement KPIs", [
        ("Businesses engaged (face-to-face)", f"=COUNTA({BE}!B2:B61)"),
        ("Avg confidence BEFORE", f"=IFERROR(AVERAGE({BE}!F2:F61),0)"),
        ("Avg confidence AFTER", f"=IFERROR(AVERAGE({BE}!G2:G61),0)"),
        ("Avg confidence uplift", f"=IFERROR(AVERAGE({BE}!H2:H61),0)"),
        ("Businesses reporting increased confidence", f"=COUNTIF({BE}!H2:H61,\">0\")"),
        ("% reporting increased confidence", f"=IFERROR(COUNTIF({BE}!H2:H61,\">0\")/COUNTA({BE}!B2:B61),0)"),
    ])

    base = r + 1  # first data row of the survey block (title sits on row r)
    day_b, day_f = base + 3, base + 4          # safety day baseline / follow-up
    night_b, night_f = base + 6, base + 7      # safety night baseline / follow-up
    conf_b, conf_f = base + 9, base + 10       # operating confidence baseline / follow-up
    r = block(ws, r, "Perceptions Survey KPIs (baseline vs follow-up)", [
        ("Surveys completed (total)", f"=COUNTA({PS}!C2:C121)"),
        ("  – Baseline wave", f"=COUNTIF({PS}!B2:B121,\"Baseline\")"),
        ("  – Follow-up wave", f"=COUNTIF({PS}!B2:B121,\"Follow-up\")"),
        ("Safety DAY – baseline avg", f"=IFERROR(AVERAGEIFS({PS}!F2:F121,{PS}!B2:B121,\"Baseline\"),0)"),
        ("Safety DAY – follow-up avg", f"=IFERROR(AVERAGEIFS({PS}!F2:F121,{PS}!B2:B121,\"Follow-up\"),0)"),
        ("Safety DAY – uplift", f"=B{day_f}-B{day_b}"),
        ("Safety NIGHT – baseline avg", f"=IFERROR(AVERAGEIFS({PS}!G2:G121,{PS}!B2:B121,\"Baseline\"),0)"),
        ("Safety NIGHT – follow-up avg", f"=IFERROR(AVERAGEIFS({PS}!G2:G121,{PS}!B2:B121,\"Follow-up\"),0)"),
        ("Safety NIGHT – uplift", f"=B{night_f}-B{night_b}"),
        ("Operating confidence – baseline avg", f"=IFERROR(AVERAGEIFS({PS}!I2:I121,{PS}!B2:B121,\"Baseline\"),0)"),
        ("Operating confidence – follow-up avg", f"=IFERROR(AVERAGEIFS({PS}!I2:I121,{PS}!B2:B121,\"Follow-up\"),0)"),
        ("Operating confidence – uplift", f"=B{conf_f}-B{conf_b}"),
        ("% reporting improved safety (attribution)",
         f"=IFERROR((COUNTIF({PS}!K2:K121,\"Significant\")+COUNTIF({PS}!K2:K121,\"Some\"))/COUNTIF({PS}!J2:J121,\"Y\"),0)"),
        ("% would support continued/expanded presence",
         f"=IFERROR(COUNTIF({PS}!M2:M121,\"Y\")/COUNTA({PS}!C2:C121),0)"),
    ])
    # number formats: averages/uplifts as 0.00, the two trailing %s as 0.0%
    for rr in range(base + 3, base + 12):
        ws[f"B{rr}"].number_format = '0.00'
    ws[f"B{base + 12}"].number_format = '0.0%'
    ws[f"B{base + 13}"].number_format = '0.0%'
    set_widths(ws, [42, 18])

    wb.save(os.path.join(OUT_DIR, "LCF_Data_Capture_Tracker.xlsx"))
    print("XLSX ->", os.path.join(OUT_DIR, "LCF_Data_Capture_Tracker.xlsx"))


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    scope_pdf()
    tracker_xlsx()
