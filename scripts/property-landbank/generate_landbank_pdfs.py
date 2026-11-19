#!/usr/bin/env python3
"""Render FINAL_RECOMMENDATION.md and TAINTING_BRIEF.md to client-grade PDFs.

Design per ~/.claude/commands/references/generate-pdf.md (navy/gold, ReportLab,
no shaded callout boxes, min 8.5pt tables). Em-dashes stripped per standing rule.
Outputs land in ~/Desktop/Property/.
"""
import re
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle, HRFlowable, PageBreak)

NAVY = HexColor("#1B2A4A"); DBLUE = HexColor("#2C3E6B"); MBLUE = HexColor("#4A6FA5")
GOLD = HexColor("#D4A843"); LBLUE = HexColor("#E8EDF5"); BORDER = HexColor("#D0D5DD")
ALT = HexColor("#F2F4F8"); TDARK = HexColor("#1A1A2E"); TMED = HexColor("#4A4A5A")
TLIGHT = HexColor("#7A7A8A")

SRC = Path(__file__).parent
OUT = Path.home() / "Desktop" / "Property"
OUT.mkdir(parents=True, exist_ok=True)

body = ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=14.5,
                      textColor=TDARK, alignment=TA_JUSTIFY, spaceAfter=7)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=18, bulletIndent=6, spaceAfter=4)
h2s = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=13, leading=17,
                     textColor=HexColor("#FFFFFF"), spaceBefore=0, spaceAfter=0,
                     leftIndent=6)
h3s = ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=11.5, leading=15,
                     textColor=DBLUE, spaceBefore=10, spaceAfter=3)
cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.5, leading=11, textColor=TDARK)
cellb = ParagraphStyle("cellb", parent=cell, fontName="Helvetica-Bold")
cellw = ParagraphStyle("cellw", parent=cellb, textColor=HexColor("#FFFFFF"), alignment=TA_CENTER)


def md_inline(t):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", t)
    return t


def clean(t):
    # standing rule: no em-dashes in client copy; Helvetica lacks macrons
    for a, b in (("ā", "a"), ("ē", "e"), ("ī", "i"), ("ō", "o"), ("ū", "u"),
                 ("Ā", "A"), ("Ē", "E"), ("Ī", "I"), ("Ō", "O"), ("Ū", "U")):
        t = t.replace(a, b)
    return (t.replace(" — ", " - ").replace("—", "-")
             .replace("≈", "~").replace("·", "|").replace("✔", "")
             .replace("➕", "+").replace("🚫", "").replace("⚠️", "").replace("🎯", ""))


def section_bar(text, width):
    p = Paragraph(md_inline(text), h2s)
    t = Table([[p]], colWidths=[width], rowHeights=None)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LINEBEFORE", (0, 0), (0, -1), 4, GOLD),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return [Spacer(1, 12), t, Spacer(1, 7)]


def md_table(rows, width):
    ncols = len(rows[0])
    first_w = width * (0.38 if ncols <= 3 else 0.28)
    other_w = (width - first_w) / (ncols - 1) if ncols > 1 else width
    data = []
    for ri, row in enumerate(rows):
        out = []
        for ci in range(ncols):
            txt = md_inline(row[ci] if ci < len(row) else "")
            st = cellw if ri == 0 else (cell if ci == 0 else ParagraphStyle(
                "c", parent=cell, alignment=TA_CENTER))
            out.append(Paragraph(txt, st))
        data.append(out)
    t = Table(data, colWidths=[first_w] + [other_w] * (ncols - 1), repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("LINEBELOW", (0, 0), (-1, 0), 1.2, NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]
    for ri in range(1, len(data)):
        if ri % 2 == 0:
            style.append(("BACKGROUND", (0, ri), (-1, ri), ALT))
    t.setStyle(TableStyle(style))
    return [Spacer(1, 4), t, Spacer(1, 8)]


def parse_md(path, width):
    flow, lines = [], clean(path.read_text()).splitlines()
    i, first_h1 = 0, True
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            i += 1; continue
        if ln.startswith("# "):
            if not first_h1:
                flow.append(Paragraph(md_inline(ln[2:]), h3s))
            first_h1 = False
        elif ln.startswith("## "):
            flow += section_bar(ln[3:], width)
        elif ln.startswith("### "):
            flow.append(Paragraph(md_inline(ln[4:]), h3s))
            flow.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=5))
        elif ln.strip().startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in clean(lines[i]).strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            if rows:
                flow += md_table(rows, width)
            continue
        elif re.match(r"^\s*[-*] ", ln):
            flow.append(Paragraph(md_inline(re.sub(r"^\s*[-*] ", "", ln)), bullet,
                                  bulletText="•"))
        elif re.match(r"^\s*\d+\. ", ln):
            num = re.match(r"^\s*(\d+)\. ", ln).group(1)
            flow.append(Paragraph(md_inline(re.sub(r"^\s*\d+\. ", "", ln)), bullet,
                                  bulletText=f"{num}."))
        elif ln.startswith("---"):
            flow.append(HRFlowable(width="100%", thickness=0.5, color=BORDER,
                                   spaceBefore=6, spaceAfter=6))
        else:
            flow.append(Paragraph(md_inline(ln), body))
        i += 1
    return flow


def title_page(flow, title, subtitle, tagline, info_rows, width):
    flow.append(Spacer(1, 150))
    flow.append(HRFlowable(width="40%", thickness=1.2, color=GOLD, hAlign="CENTER"))
    flow.append(Spacer(1, 18))
    flow.append(Paragraph(title, ParagraphStyle("t", fontName="Helvetica-Bold",
                fontSize=27, leading=33, textColor=NAVY, alignment=TA_CENTER)))
    flow.append(Spacer(1, 10))
    flow.append(Paragraph(subtitle, ParagraphStyle("s", fontName="Helvetica",
                fontSize=15, leading=20, textColor=DBLUE, alignment=TA_CENTER)))
    flow.append(Spacer(1, 8))
    flow.append(Paragraph(tagline, ParagraphStyle("g", fontName="Helvetica-Oblique",
                fontSize=11.5, leading=16, textColor=MBLUE, alignment=TA_CENTER)))
    flow.append(Spacer(1, 18))
    flow.append(HRFlowable(width="40%", thickness=1.2, color=GOLD, hAlign="CENTER"))
    flow.append(Spacer(1, 50))
    rows = [[Paragraph(f"<b>{k}</b>", cell), Paragraph(md_inline(v), cell)]
            for k, v in info_rows]
    t = Table(rows, colWidths=[width * 0.3, width * 0.5], hAlign="CENTER")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LBLUE),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    flow.append(t)
    flow.append(Spacer(1, 60))
    flow.append(Paragraph(
        "Private and confidential. Prepared for the Duais family. Figures rely on listings "
        "verified 1 November 2026 and are stale after 1 December 2026 or upon any trigger "
        "event named inside. Not financial, legal, or tax advice.",
        ParagraphStyle("d", fontName="Helvetica-Oblique", fontSize=8, leading=11,
                       textColor=TMED, alignment=TA_CENTER)))
    flow.append(PageBreak())


def build(outname, header_title, flow_fn):
    path = OUT / outname
    doc = BaseDocTemplate(str(path), pagesize=A4, leftMargin=54, rightMargin=54,
                          topMargin=62, bottomMargin=54, title=header_title)
    width = A4[0] - 108
    frame = Frame(54, 54, width, A4[1] - 116, id="main")

    def decorate(canv, _doc):
        canv.saveState()
        canv.setStrokeColor(BORDER); canv.setLineWidth(0.5)
        canv.line(54, A4[1] - 40, A4[0] - 54, A4[1] - 40)
        canv.setFont("Helvetica", 7); canv.setFillColor(TLIGHT)
        canv.drawString(54, A4[1] - 36, f"Duais Family | {header_title}")
        canv.drawRightString(A4[0] - 54, A4[1] - 36, "CONFIDENTIAL")
        canv.line(54, 40, A4[0] - 54, 40)
        canv.setFont("Helvetica", 7.5)
        canv.drawString(54, 30, "1 November 2026")
        canv.drawCentredString(A4[0] / 2, 30, f"Page {canv.getPageNumber()}")
        canv.drawRightString(A4[0] - 54, 30, "Prepared with ETR review")
        canv.restoreState()

    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=decorate)])
    doc.build(flow_fn(width))
    return path


def rec_flow(width):
    flow = []
    title_page(flow, "Auckland Land Purchase", "Buy and Hold Recommendation",
               "Pure land, budget $1.8M, hold 7 to 15 years",
               [("Prepared", "1 November 2026 (rev 3, budget raised to $1.8M)"),
                ("Primary target", "2 Rope Rd, Whenuapai (CONDITIONAL GO)"),
                ("Alternative", "12 Cheriton Lane, Drury: beside new rail station"),
                ("Scale option", "130 Helvetia Rd, Pukekohe: 4.45ha, one hard offer"),
                ("Fallbacks", "Lot 2 Bawden Rd, Dairy Flat | 220 Kern Rd, Ramarama"),
                ("Eliminated", "Upper Orewa ($3.1M vendor) | Follies (pylon) | Hobson (lifestyle only)"),
                ("Review", "ETR adversarial review, 34 findings + family vetting applied")], width)
    flow += parse_md(SRC / "FINAL_RECOMMENDATION.md", width)
    return flow


def brief_flow(width):
    flow = []
    title_page(flow, "Tax Opinion Brief", "Land Taint and Purchase Structuring",
               "Six questions ahead of two intended property purchases",
               [("Prepared", "1 November 2026"),
                ("For", "Accountant to Ahmad Duais"),
                ("Deliverable", "Short written opinion, 2 to 4 pages"),
                ("Timing", "Offers planned within 2 to 4 weeks")], width)
    flow += parse_md(SRC / "TAINTING_BRIEF.md", width)
    return flow


if __name__ == "__main__":
    for p in (build("Landbank_Recommendation_Nov2026.pdf",
                    "Land Purchase Recommendation", rec_flow),
              build("Tax_Opinion_Brief_Land_Taint.pdf",
                    "Tax Opinion Brief", brief_flow)):
        print("OK", p, p.stat().st_size, "bytes")
