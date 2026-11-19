#!/usr/bin/env python3
"""
Generate the HOTC x ASG LCF pilot SERVICE AGREEMENT as an editable .docx.

Mirrors HOTC's own "Independent Supplier Agreement" template (Specific Terms schedule),
and incorporates by reference the General Terms & Appendices of the executed agreement
dated 1 July 2025 — so nothing is renegotiated and Edward/Viv recognise the instrument.

Integrates the LCF Scope of Works (services / deliverables / KPIs) into the schedule, plus
an LCF Funding Compliance appendix (CPTED purpose + accountability reporting obligations).

Output: ~/Desktop/ASG/HOTC/2026/LCF_Independent_Supplier_Agreement.docx
Script lives in the Dev/Claude repo (no working files left in data folders).
"""

import os
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = os.path.expanduser("~/Desktop/ASG/HOTC/2026/LCF_Independent_Supplier_Agreement.docx")
NAVY = RGBColor(0x1B, 0x2A, 0x4A)
RATE = "$36.90"          # per LCF proposal agreed with Edward (master agreement shows $36.50 — confirm)
TOTAL = "$41,150"
TOTAL_INCL = "$47,322.50"
HALF = "$20,575"
HOURS = "approximately 1,115"

doc = Document()

# base style
normal = doc.styles['Normal']
normal.font.name = 'Calibri'
normal.font.size = Pt(10.5)

def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement('w:shd')
    sh.set(qn('w:val'), 'clear'); sh.set(qn('w:color'), 'auto'); sh.set(qn('w:fill'), hexcolor)
    tcPr.append(sh)

def set_widths(table, widths_cm):
    table.autofit = False
    for row in table.rows:
        for i, w in enumerate(widths_cm):
            row.cells[i].width = Cm(w)

def h(text, size=13, space_before=12, space_after=4, color=NAVY):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    r = p.add_run(text); r.bold = True; r.font.size = Pt(size); r.font.color.rgb = color
    return p

def body(text, bold=False, size=10.5, space_after=4, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    r = p.add_run(text); r.bold = bold; r.italic = italic; r.font.size = Pt(size)
    return p

def bullet(text, size=10.5):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text); r.font.size = Pt(size)
    return p

def schedule(rows, label_w=4.8, val_w=11.7):
    t = doc.add_table(rows=0, cols=2)
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for label, value in rows:
        cells = t.add_row().cells
        shade(cells[0], 'E8EDF5')
        lp = cells[0].paragraphs[0]; lr = lp.add_run(label); lr.bold = True; lr.font.size = Pt(10)
        # value may be list (multi-line) or string
        vp = cells[1].paragraphs[0]
        if isinstance(value, list):
            for j, line in enumerate(value):
                if j > 0:
                    vp = cells[1].add_paragraph()
                vp.paragraph_format.space_after = Pt(1)
                vr = vp.add_run(line); vr.font.size = Pt(10)
        else:
            vr = vp.add_run(value); vr.font.size = Pt(10)
    set_widths(t, [label_w, val_w])
    return t

# ════════════════════════════════════════════════════════════════════════════
# TITLE
# ════════════════════════════════════════════════════════════════════════════
title = doc.add_paragraph(); title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = title.add_run("INDEPENDENT SUPPLIER AGREEMENT"); r.bold = True; r.font.size = Pt(18); r.font.color.rgb = NAVY
sub = doc.add_paragraph(); sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub.add_run("Contract name: CBD Safety Uplift Pilot (Local Crime Fund)"); r.bold = True; r.font.size = Pt(12)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("between\nHeart of the City Incorporated\nand\nAbsolute Security Group Limited").font.size = Pt(11)

body("This agreement comprises these Specific Terms and the General Terms, Appendices and "
     "definitions of the Independent Supplier Agreement between the parties dated 1 July 2025 "
     "(the “Master Agreement”), which are incorporated by reference and apply to this "
     "agreement (see clause A). To the extent of any inconsistency, these Specific Terms prevail.",
     italic=True, size=9.5, space_after=8)

# ════════════════════════════════════════════════════════════════════════════
# SPECIFIC TERMS
# ════════════════════════════════════════════════════════════════════════════
h("Specific Terms", size=14)

schedule([
    ("Dated:", "2 June 2026"),
    ("Parties:", ["The Heart of the City Incorporated (“HOTC”)",
                  "Absolute Security Group Limited (“the Supplier” / “ASG”)"]),
    ("Type of Supplier:", "Supplier is a limited liability company."),
    ("Funding source:", ["Local Crime Fund (LCF), provided under the Proceeds of Crime Fund (PoCF) "
                         "objective and jointly administered (the “Funding”).",
                         "Total Funding available for this initiative: " + TOTAL + " + GST."]),
])

schedule([
    ("Services:", [
        "Enhanced CBD Safety Team – an additional, LCF-funded uplift to the existing safety "
        "patrol, deployed across the Auckland City Centre precinct during peak-risk periods.",
        "• Additional Safety Team deployed seven days, covering peak trading hours "
        "(09:00–17:00 weekdays) with weekend daytime support (09:00–18:00).",
        "• A targeted peak-risk uplift pool deployed flexibly to documented hotspots "
        "(Queen Street, Aotea Square, Hobson/Victoria corner), concentrated on the highest-risk "
        "evening windows (Thursday–Saturday).",
        "Deployment is reviewed weekly and flexed to live hotspot intelligence; the indicative "
        "pattern is ~149 hours per week, equating to " + HOURS + " service hours across the pilot.",
        "ASG provides at no cost to the Funding: all uniforms for the additional team; operational "
        "management oversight and supervision; and camera/surveillance support."]),
    ("Service Fees:", [
        "Contracted rate of " + RATE + " per hour per guard, excl. GST (existing contract rate).",
        "Total contract price is agreed at a maximum of " + TOTAL + " excl. GST (" + TOTAL_INCL +
        " incl. GST) for the pilot period.",
        "This equates to " + HOURS + " service hours at the contracted rate.",
        "Invoicing: two equal instalments of " + HALF + " + GST each, both issued before 30 June "
        "2026, consistent with the Funding requirement that funds be committed and invoiced before "
        "end of June. Invoice 1 on execution (early June); Invoice 2 mid–late June."]),
    ("Supplier will report to the following HOTC person(s):", "Edward Caughey, Head of Customer Experience"),
    ("Manager to provide Services:", "Ahmad Duais, CEO"),
    ("Supplier's Contact Details:", ["Head office: 220 Queen Street, Auckland CBD 1010",
                                     "Phone: 021 0850 0009 / 09 950 4640",
                                     "Email: ahmad@absolutesecuritygroup.co.nz  —  Attn: Ahmad Duais"]),
    ("HOTC's Contact Details:", ["Heart of the City, PO Box 105 331, Auckland 1143",
                                 "Email: edward.caughey@hotcity.co.nz  —  Attn: Edward Caughey"]),
    ("HOTC's address for delivery:", "Heart of the City, Level 23, 151 Queen Street, Auckland 1010"),
    ("Deliverables:", [
        "A defined, evidence-generating CPTED pilot: “This pilot delivers a targeted "
        "CPTED-based intervention, increasing visible guardianship, improving natural surveillance, "
        "and strengthening business-community safety networks during peak risk periods.”",
        "Increased visible guardianship and natural surveillance of identified hotspots during "
        "peak-risk windows.",
        "Business Engagement Programme: two to three ASG operational managers (including the CEO) "
        "conducting face-to-face visits with precinct businesses to introduce the initiative, "
        "understand store-level safety concerns, and reinforce HOTC's commitment to safety and "
        "wellbeing.",
        "A comprehensive end-of-pilot accountability report (see Appendix B and clause A) "
        "demonstrating how the Funding achieved its Purpose."]),
    ("KPIs:", "Outlined at Appendix B. Reviewed against the period of activity 2 June – 24 July 2026."),
    ("Commencement Date:", "2 June 2026"),
    ("Term:", "Fixed term – the Expiry Date is 24 July 2026 (period of activity 2 June – 24 July 2026)."),
    ("Termination / Suspension:", "Per the General Terms of the Master Agreement. Three (3) weeks' "
                                  "written notice; HOTC may suspend at any time, in which case HOTC "
                                  "pays only for Services actually delivered."),
    ("Insurance:", "Supplier to maintain Public Liability Insurance to a minimum of $1 million and "
                   "Statutory Liability Insurance of $250,000 (as per Master Agreement)."),
    ("Additional specific terms:", [
        "(a) The Funding must be used solely for Crime Prevention through Environmental Design "
        "(CPTED) based interventions for the Purpose set out in Appendix A.",
        "(b) ASG will capture activity and engagement data from commencement (2 June) and provide "
        "HOTC the accountability report by 27 July 2026 to enable HOTC's report to the joint "
        "funding administrators by 31 July 2026.",
        "(c) The pilot period may run to 24 July 2026 (beyond the original funding-agreement period) "
        "as approved by Auckland Council; all Funding is committed before 30 June 2026."]),
])

# ════════════════════════════════════════════════════════════════════════════
# CLAUSE A — incorporation
# ════════════════════════════════════════════════════════════════════════════
h("A.  Incorporation of General Terms", size=13)
body("The General Terms and Conditions, Appendices and definitions of the Master Agreement "
     "(Independent Supplier Agreement between the parties dated 1 July 2025) are incorporated into "
     "and form part of this agreement and apply to the Services, Deliverables and Funding described "
     "in these Specific Terms, including without limitation the clauses governing:")
for c in ["Agreement and order of precedence", "Commencement date and term",
          "Services and Deliverables to be provided", "Payment", "Independent contractor",
          "Assignment and subcontracting", "Notices", "Liabilities of Supplier", "Audit",
          "HOTC Data and Privacy", "Confidentiality / conflicts of interest",
          "Intellectual Property", "Dispute resolution"]:
    bullet(c)
body("Where this agreement is to operate as a standalone instrument, the parties may instead annex "
     "the full General Terms; the parties confirm the General Terms already executed between them "
     "apply unamended.", italic=True, size=9.5)

# ════════════════════════════════════════════════════════════════════════════
# APPENDIX A — LCF Funding Compliance
# ════════════════════════════════════════════════════════════════════════════
doc.add_page_break()
h("Appendix A — LCF Funding Compliance (Purpose & CPTED Alignment)", size=13)
body("Purpose of the Funding: to undertake community safety initiatives ‘to address crime-related "
     "harm to communities and improve community wellbeing’ as per the PoCF objective. The Funding "
     "must be used for Crime Prevention through Environmental Design (CPTED) based interventions. "
     "The pilot maps to the eligible categories as follows:")

t = doc.add_table(rows=1, cols=2); t.style = 'Table Grid'; t.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr = t.rows[0].cells
for i, txt in enumerate(["LCF / CPTED category", "How the pilot delivers"]):
    shade(hdr[i], '1B2A4A')
    rp = hdr[i].paragraphs[0]; rr = rp.add_run(txt); rr.bold = True; rr.font.color.rgb = RGBColor(0xFF,0xFF,0xFF); rr.font.size = Pt(10)
rows = [
    ("Territoriality & access — patrols / wardens / ambassadors",
     "Additional uniformed Safety Team providing visible guardianship across the precinct in peak-risk windows."),
    ("Natural surveillance",
     "Increased patrol density improves natural surveillance of identified hotspots."),
    ("Cultural cohesion / sense of community",
     "Business Engagement Programme building business-community safety networks and collaborative approaches to safety."),
    ("Reduction in crime / improved safety in the BID area",
     "Targeted, welfare-first deterrence in documented hotspots during peak-risk periods."),
]
for a, b in rows:
    cells = t.add_row().cells
    cells[0].paragraphs[0].add_run(a).font.size = Pt(10)
    cells[1].paragraphs[0].add_run(b).font.size = Pt(10)
set_widths(t, [5.5, 11.0])

body("", space_after=2)
body("Accountability reporting (per Master Agreement Audit clause and Funding terms):", bold=True)
for x in [
    "ASG provides a detailed, accurate and complete accountability report covering the period "
    "2 June – 24 July 2026, demonstrating how the Funding achieved its Purpose.",
    "ASG report to HOTC by 27 July 2026; HOTC report to the joint funding administrators by 31 July 2026.",
    "Reporting themes: effectiveness metrics (asset / surveillance / engagement); partnership & "
    "collaboration with administrators and stakeholders; improved perceptions of safety; reduction "
    "in harm and improved wellbeing inclusive of the wider community; positive stories and outcomes.",
]:
    bullet(x)

# ════════════════════════════════════════════════════════════════════════════
# APPENDIX B — KPIs
# ════════════════════════════════════════════════════════════════════════════
h("Appendix B — KPIs", size=13)
body("Prevention / Impact KPIs", bold=True)
for x in ["Reduction in repeat incidents in identified hotspots.",
          "Change in time-of-day incident patterns.",
          "Reduction in calls for service / security escalation."]:
    bullet(x)
body("Engagement KPIs", bold=True)
for x in ["Number of businesses engaged face-to-face.",
          "Number of perceptions surveys completed (baseline and follow-up).",
          "Qualitative feedback and quotes captured (positive stories)."]:
    bullet(x)
body("Perceptions Survey KPIs", bold=True)
body("A short face-to-face perceptions survey is run as the programme's measurement instrument, "
     "delivered during the Business Engagement visits. Two waves are conducted — a baseline (early "
     "June, at commencement) and a follow-up (mid–late July) — so change can be attributed to the "
     "uplift. Responses are captured digitally and reported in the accountability report. Measured:",
     size=10)
for x in ["Perceived safety score by day and by night/evening (1–5) — baseline vs follow-up uplift.",
          "Operating confidence score (1–5) — baseline vs follow-up uplift.",
          "% of businesses reporting improved safety since the uplift (attribution).",
          "% of businesses reporting increased confidence (baseline vs follow-up).",
          "Customer sentiment score (1–5).",
          "% of businesses that would support a continued / expanded safety presence."]:
    bullet(x)
body("A short Landlord / Property Owner survey (leasing conditions, impact of safety perception on "
     "leasing, 12–24 month confidence) supplements the business survey where practicable.",
     size=9.5, italic=True)

# ════════════════════════════════════════════════════════════════════════════
# EXECUTION
# ════════════════════════════════════════════════════════════════════════════
h("Executed as an agreement", size=13)
sig = doc.add_table(rows=4, cols=2); sig.style = 'Table Grid'; sig.alignment = WD_TABLE_ALIGNMENT.CENTER
labels = [
    ("Signed for and on behalf of\nHeart of the City Incorporated", "Signed for and on behalf of\nAbsolute Security Group Limited"),
    ("\n\nSignature: ______________________", "\n\nSignature: ______________________"),
    ("Name: Edward Caughey\nTitle: Head of Customer Experience", "Name: Ahmad Duais\nTitle: CEO / Director"),
    ("Date: ______________________", "Date: ______________________"),
]
for ri, (l, rt) in enumerate(labels):
    for ci, txt in enumerate((l, rt)):
        cell = sig.rows[ri].cells[ci]
        run = cell.paragraphs[0].add_run(txt); run.font.size = Pt(10)
        if ri == 0: run.bold = True
set_widths(sig, [8.25, 8.25])

doc.save(OUT)
print("DOCX ->", OUT)
