#!/usr/bin/env python3
"""HNZ RFP 0018709 — Owner's Briefing: markdown -> compact working PDF.

Masthead style (no title page/ToC — it is a working brief), ASG design
standards: ReportLab, A4, 54/62pt margins, navy+gold, min 8.5pt tables.
Two-pass build for page totals.

Usage: .venv/bin/python build_owners_briefing_pdf.py <brief.md> <out.pdf>
"""
import re, sys

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,
                                Paragraph, Spacer, Table, TableStyle,
                                HRFlowable)

NAVY = HexColor("#1B2A4A")
DBLUE = HexColor("#2C3E6B")
MBLUE = HexColor("#4A6FA5")
GOLD = HexColor("#D4A843")
ROW_ALT = HexColor("#F2F4F8")
BORDER = HexColor("#D0D5DD")
TEXT_D = HexColor("#1A1A2E")
TEXT_M = HexColor("#4A4A5A")
TEXT_L = HexColor("#7A7A8A")

W, H = A4
ML, MR, MT, MB = 54, 54, 62, 54
AVAIL = W - ML - MR

S_BODY = ParagraphStyle("body", fontName="Helvetica", fontSize=10,
                        leading=14, textColor=TEXT_D, alignment=4,
                        spaceAfter=5)
S_BULLET = ParagraphStyle("bullet", parent=S_BODY, leftIndent=18,
                          bulletIndent=6, spaceAfter=3.5)
S_H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=13,
                      textColor=white, backColor=NAVY,
                      borderPadding=(4, 8, 4, 8), leading=17,
                      spaceBefore=13, spaceAfter=7)
S_H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11,
                      textColor=DBLUE, spaceBefore=8, spaceAfter=4)

DOC = {"total": "?",
       "header": "ASG  |  HNZ Security Officer Services RFP 0018709 — Owner's Briefing"}

MACRONS = str.maketrans("āēīōūĀĒĪŌŪ’‘“”–—", "aeiouAEIOU''\"\"--")


def inline(md):
    md = md.translate(MACRONS)
    md = md.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    md = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", md)
    md = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", md)
    return md


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(BORDER); canvas.setLineWidth(0.5)
    canvas.line(ML, H - 40, W - MR, H - 40)
    canvas.setFont("Helvetica", 7); canvas.setFillColor(TEXT_L)
    canvas.drawString(ML, H - 36, DOC["header"])
    canvas.drawRightString(W - MR, H - 36, "COMMERCIAL IN CONFIDENCE")
    canvas.line(ML, 40, W - MR, 40)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(ML, 30, "31 October 2026")
    canvas.drawCentredString(W / 2, 30, f"Page {doc.page} of {DOC['total']}")
    canvas.drawRightString(W - MR, 30, "Prepared for Ahmad Duais, CEO")
    canvas.restoreState()


def make_table(rows):
    n = max(len(r) for r in rows)
    th = ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=8.5,
                        textColor=white, leading=10.5)
    td = ParagraphStyle("td", fontName="Helvetica", fontSize=8.5,
                        leading=11, textColor=TEXT_D)
    data = [[Paragraph(inline(c), th) for c in (rows[0] + [""] * n)[:n]]]
    for r in rows[1:]:
        data.append([Paragraph(inline(c), td) for c in (r + [""] * n)[:n]])
    first = AVAIL * (0.30 if n <= 3 else 0.22 if n <= 5 else 0.16)
    widths = [first] + [(AVAIL - first) / (n - 1)] * (n - 1) if n > 1 else [AVAIL]
    t = Table(data, colWidths=widths, repeatRows=1)
    style = [("BACKGROUND", (0, 0), (-1, 0), NAVY),
             ("LINEBELOW", (0, 0), (-1, 0), 1.2, GOLD),
             ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
             ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("TOPPADDING", (0, 0), (-1, -1), 4.5),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
             ("LEFTPADDING", (0, 0), (-1, -1), 6),
             ("RIGHTPADDING", (0, 0), (-1, -1), 6)]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
    t.setStyle(TableStyle(style))
    return t


def masthead(story):
    story.append(Paragraph("HNZ SECURITY OFFICER SERVICES — RFP 0018709",
                           ParagraphStyle("t", fontName="Helvetica-Bold",
                                          fontSize=19, leading=23,
                                          textColor=NAVY)))
    story.append(Paragraph("Owner's Briefing: what to read, what to know, what to prepare, what gets submitted",
                           ParagraphStyle("st", fontName="Helvetica-Oblique",
                                          fontSize=10, leading=13.5,
                                          textColor=TEXT_M, spaceBefore=3)))
    story.append(Paragraph("Absolute Security Group Limited  ·  Bidding: Auckland, Counties Manukau, Waitemata, Northland  ·  Submission locks Friday 6 November, 12:00 midday",
                           ParagraphStyle("st2", fontName="Helvetica-Bold",
                                          fontSize=9.5, leading=13,
                                          textColor=DBLUE, spaceBefore=4)))
    story.append(Spacer(1, 5))
    story.append(HRFlowable(width="100%", thickness=1.4, color=GOLD))
    story.append(Spacer(1, 4))


def collect_wrapped(lines, i, first):
    parts = [first]
    j = i + 1
    while j < len(lines):
        nxt = lines[j].rstrip()
        if (not nxt.strip() or nxt.startswith(("#", "|", "- ", "---"))
                or re.match(r"^\d+\.\s", nxt)):
            break
        parts.append(nxt.strip())
        j += 1
    return " ".join(parts), j


def build(md_path, out_path):
    lines = open(md_path, encoding="utf-8").read().split("\n")
    doc = BaseDocTemplate(out_path, pagesize=A4, leftMargin=ML,
                          rightMargin=MR, topMargin=MT, bottomMargin=MB,
                          title="HNZ RFP 0018709 — Owner's Briefing",
                          author="ASG")
    doc.addPageTemplates([PageTemplate(
        id="main", frames=[Frame(ML, MB, AVAIL, H - MT - MB)],
        onPage=header_footer)])

    story = []
    masthead(story)
    i = 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip() or ln == "---" or ln.startswith("# "):
            i += 1
            continue
        if ln.startswith("## "):
            story.append(Paragraph(inline(ln[3:]), S_H1))
        elif ln.startswith("### "):
            story.append(Paragraph(inline(ln[4:]), S_H2))
        elif ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            if rows:
                story.append(Spacer(1, 3))
                story.append(make_table(rows))
                story.append(Spacer(1, 7))
            continue
        elif re.match(r"^\d+\.\s", ln):
            num, rest = ln.split(".", 1)
            para, j = collect_wrapped(lines, i, rest.strip())
            story.append(Paragraph(inline(para), S_BULLET, bulletText=f"{num}."))
            i = j
            continue
        elif ln.startswith("- "):
            para, j = collect_wrapped(lines, i, ln[2:])
            story.append(Paragraph(inline(para), S_BULLET, bulletText="•"))
            i = j
            continue
        else:
            para, j = collect_wrapped(lines, i, ln)
            story.append(Paragraph(inline(para), S_BODY))
            i = j
            continue
        i += 1

    doc.build(story)
    import fitz
    return fitz.open(out_path).page_count


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    n = build(sys.argv[1], sys.argv[2])
    DOC["total"] = str(n)
    n = build(sys.argv[1], sys.argv[2])
    print(f"PDF written: {sys.argv[2]} ({n} pages)")
