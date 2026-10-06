#!/usr/bin/env python3
"""Beaded-dress brand growth blueprint — markdown -> 3-page PDF per the
generate-pdf standards (ReportLab, A4, 54/62pt margins, 10pt body min 8pt,
navy+gold, clean tables, no tinted callout boxes). 3-page budget: compact
masthead on page 1 instead of a title page + ToC.

Usage: .venv/bin/python generate_blueprint_pdf.py <blueprint.md> <out.pdf>
"""

import re, sys, datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,
                                Paragraph, Spacer, Table, TableStyle,
                                PageBreak, HRFlowable)

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

S_BODY = ParagraphStyle("body", fontName="Helvetica", fontSize=9.5,
                        leading=13.0, textColor=TEXT_D, alignment=4,
                        spaceAfter=4)
S_BULLET = ParagraphStyle("bullet", parent=S_BODY, leftIndent=16,
                          bulletIndent=5, spaceAfter=2.5)
S_H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=12.5,
                      textColor=white, backColor=NAVY,
                      borderPadding=(4, 7, 4, 7), leading=16,
                      spaceBefore=9, spaceAfter=6)
S_H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.8,
                      textColor=DBLUE, spaceBefore=6, spaceAfter=3)
S_H3 = ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=10,
                      textColor=MBLUE, spaceBefore=6, spaceAfter=3)


def inline(md):
    md = (md.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    md = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", md)
    md = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", md)
    return md


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(BORDER); canvas.setLineWidth(0.5)
    canvas.line(ML, H - 40, W - MR, H - 40)
    canvas.setFont("Helvetica", 7); canvas.setFillColor(TEXT_L)
    canvas.drawString(ML, H - 36, "ONLINE GROWTH BLUEPRINT  |  Beaded Occasion Dresses — NZ")
    canvas.drawRightString(W - MR, H - 36, "CONFIDENTIAL")
    canvas.line(ML, 40, W - MR, 40)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(ML, 30, datetime.date.today().strftime("%d %B %Y"))
    canvas.drawCentredString(W / 2, 30, f"Page {doc.page} of 3")
    canvas.drawRightString(W - MR, 30, "Prepared by Ahmad Duais")
    canvas.restoreState()


def make_table(rows):
    n = len(rows[0])
    data = [[Paragraph(f"<b>{inline(c)}</b>", ParagraphStyle(
        "th", fontName="Helvetica-Bold", fontSize=8.5, textColor=white,
        leading=10.5)) for c in rows[0]]]
    for r in rows[1:]:
        r = (r + [""] * n)[:n]
        data.append([Paragraph(inline(c), ParagraphStyle(
            "td", fontName="Helvetica", fontSize=8.5, leading=11,
            textColor=TEXT_D)) for c in r])
    avail = W - ML - MR
    first = avail * (0.30 if n <= 3 else 0.26)
    widths = [first] + [(avail - first) / (n - 1)] * (n - 1)
    t = Table(data, colWidths=widths, repeatRows=1)
    style = [("BACKGROUND", (0, 0), (-1, 0), NAVY),
             ("LINEBELOW", (0, 0), (-1, 0), 1.2, GOLD),
             ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
             ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("TOPPADDING", (0, 0), (-1, -1), 4),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
             ("LEFTPADDING", (0, 0), (-1, -1), 6),
             ("RIGHTPADDING", (0, 0), (-1, -1), 6)]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
    t.setStyle(TableStyle(style))
    return t


def masthead(story):
    story.append(Paragraph("ONLINE GROWTH BLUEPRINT", ParagraphStyle(
        "t", fontName="Helvetica-Bold", fontSize=20, leading=24,
        textColor=NAVY)))
    story.append(Paragraph(
        "Beaded occasion dresses · NZ-based · built on the Hormozi "
        "frameworks · hardened by ETR multi-agent review", ParagraphStyle(
            "st", fontName="Helvetica-Oblique", fontSize=9.5, leading=13,
            textColor=TEXT_M, spaceBefore=3)))
    story.append(Spacer(1, 5))
    story.append(HRFlowable(width="100%", thickness=1.4, color=GOLD))
    story.append(Spacer(1, 6))


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
                          title="Online Growth Blueprint — Beaded Dress Brand")
    doc.addPageTemplates([PageTemplate(
        id="main", frames=[Frame(ML, MB, W - ML - MR, H - MT - MB)],
        onPage=header_footer)])

    story = []
    masthead(story)
    i = 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if ln.startswith("# ") or not ln.strip():
            i += 1
            continue
        if ln == "---PAGE---":
            story.append(PageBreak())
        elif ln == "---":
            i += 1
            continue
        elif ln.startswith("## "):
            story.append(Paragraph(inline(ln[3:]), S_H1))
        elif ln.startswith("### "):
            story.append(Paragraph(inline(ln[4:]), S_H2))
        elif ln.startswith("#### "):
            story.append(Paragraph(inline(ln[5:]), S_H3))
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
                story.append(Spacer(1, 6))
            continue
        elif re.match(r"^\d+\.\s", ln):
            num, rest = ln.split(".", 1)
            para = collect_wrapped(lines, i, rest.strip())
            story.append(Paragraph(inline(para[0]), S_BULLET,
                                   bulletText=f"{num}."))
            i = para[1]
            continue
        elif ln.startswith("- "):
            para = collect_wrapped(lines, i, ln[2:])
            story.append(Paragraph(inline(para[0]), S_BULLET, bulletText="•"))
            i = para[1]
            continue
        else:
            para = collect_wrapped(lines, i, ln)
            story.append(Paragraph(inline(para[0]), S_BODY))
            i = para[1]
            continue
        i += 1

    doc.build(story)
    import fitz
    n = fitz.open(out_path).page_count
    print(f"PDF written: {out_path} ({n} pages)")
    if n > 3:
        print("WARNING: over the 3-page budget — trim content.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    build(sys.argv[1], sys.argv[2])
