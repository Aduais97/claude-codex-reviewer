#!/usr/bin/env python3
"""SŒURS launch strategy — markdown -> PDF per the generate-pdf standards
(ReportLab, A4, 54/62pt margins, TOC, 10pt body min 8pt, clean tables, no
tinted callout boxes), with the brand palette in place of ASG navy/gold:
espresso headers, rose-gold accents on cream.

Usage: .venv/bin/python generate_strategy_pdf.py <strategy.md> <out.pdf>
"""

import re, sys, datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,
                                Paragraph, Spacer, Table, TableStyle,
                                PageBreak, HRFlowable)
from reportlab.platypus.tableofcontents import TableOfContents

ESPRESSO = HexColor("#2A1206")
COCOA = HexColor("#33251C")
ROSE = HexColor("#C89A76")
BRONZE = HexColor("#7A4E2C")
CREAM = HexColor("#F6EFE4")
ROW_ALT = HexColor("#F4EEE6")
BORDER = HexColor("#D8CFC2")
TEXT_D = HexColor("#1F1710")
TEXT_M = HexColor("#5A4A3A")
TEXT_L = HexColor("#8A7A6A")

W, H = A4
ML, MR, MT, MB = 54, 54, 62, 54

S_BODY = ParagraphStyle("body", fontName="Helvetica", fontSize=10,
                        leading=14.5, textColor=TEXT_D, alignment=4,
                        spaceAfter=6)
S_BULLET = ParagraphStyle("bullet", parent=S_BODY, leftIndent=18,
                          bulletIndent=6, spaceAfter=3)
S_H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=13,
                      textColor=white, backColor=ESPRESSO,
                      borderPadding=(5, 8, 5, 8), leading=17,
                      spaceBefore=16, spaceAfter=10)
S_H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11.5,
                      textColor=BRONZE, spaceBefore=12, spaceAfter=6)
S_META = ParagraphStyle("meta", parent=S_BODY, fontSize=9, textColor=TEXT_M,
                        alignment=1)
S_TOC1 = ParagraphStyle("toc1", fontName="Helvetica", fontSize=10,
                        leading=16, textColor=TEXT_D)


def inline(md):
    md = (md.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    md = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", md)
    md = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", md)
    md = re.sub(r"`([^`]+?)`", r"<font face='Courier' size='9'>\1</font>", md)
    return md


class Doc(BaseDocTemplate):
    def afterFlowable(self, fl):
        if isinstance(fl, Paragraph) and fl.style.name == "h1":
            text = re.sub(r"<[^>]+>", "", fl.getPlainText())
            self.notify("TOCEntry", (0, text, self.page))


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(BORDER); canvas.setLineWidth(0.5)
    canvas.line(ML, H - 40, W - MR, H - 40)
    canvas.setFont("Helvetica", 7); canvas.setFillColor(TEXT_L)
    canvas.drawString(ML, H - 36, "SŒURS FRAGRANCES  |  Launch Marketing Strategy")
    canvas.drawRightString(W - MR, H - 36, "CONFIDENTIAL")
    canvas.line(ML, 40, W - MR, 40)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(ML, 30, datetime.date.today().strftime("%d %B %Y"))
    canvas.drawCentredString(W / 2, 30, f"Page {doc.page}")
    canvas.drawRightString(W - MR, 30, "Prepared by Ahmad Duais")
    canvas.restoreState()


def make_table(rows):
    n = len(rows[0])
    data = [[Paragraph(f"<b>{inline(c)}</b>", ParagraphStyle(
        "th", fontName="Helvetica-Bold", fontSize=8.5, textColor=white,
        leading=11)) for c in rows[0]]]
    for r in rows[1:]:
        r = (r + [""] * n)[:n]
        data.append([Paragraph(inline(c), ParagraphStyle(
            "td", fontName="Helvetica", fontSize=8.5, leading=11.5,
            textColor=TEXT_D)) for c in r])
    avail = W - ML - MR
    first = avail * (0.34 if n <= 3 else 0.28)
    widths = [first] + [(avail - first) / (n - 1)] * (n - 1)
    t = Table(data, colWidths=widths, repeatRows=1)
    style = [("BACKGROUND", (0, 0), (-1, 0), ESPRESSO),
             ("LINEBELOW", (0, 0), (-1, 0), 1.2, ROSE),
             ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
             ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("TOPPADDING", (0, 0), (-1, -1), 5),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
             ("LEFTPADDING", (0, 0), (-1, -1), 6),
             ("RIGHTPADDING", (0, 0), (-1, -1), 6)]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
    t.setStyle(TableStyle(style))
    return t


def title_page(story, title, subtitle, meta_lines):
    story.append(Spacer(1, 150))
    story.append(HRFlowable(width="40%", thickness=1.2, color=ROSE,
                            hAlign="CENTER"))
    story.append(Spacer(1, 22))
    story.append(Paragraph(title, ParagraphStyle(
        "t", fontName="Helvetica-Bold", fontSize=30, leading=36,
        textColor=ESPRESSO, alignment=1)))
    story.append(Spacer(1, 10))
    story.append(Paragraph(subtitle, ParagraphStyle(
        "st", fontName="Helvetica", fontSize=15, textColor=BRONZE,
        alignment=1)))
    story.append(Spacer(1, 22))
    story.append(HRFlowable(width="40%", thickness=1.2, color=ROSE,
                            hAlign="CENTER"))
    story.append(Spacer(1, 46))
    for m in meta_lines:
        story.append(Paragraph(m, S_META))
    story.append(Spacer(1, 90))
    story.append(Paragraph(
        "<i>Advisory document. Market figures carry their stated attribution; "
        "assumptions are flagged. Nothing herein is legal advice — NZ counsel "
        "signs off before launch.</i>",
        ParagraphStyle("disc", parent=S_META, fontSize=8, textColor=TEXT_L)))
    story.append(PageBreak())


def build(md_path, out_path):
    lines = open(md_path, encoding="utf-8").read().split("\n")
    doc = Doc(out_path, pagesize=A4, leftMargin=ML, rightMargin=MR,
              topMargin=MT, bottomMargin=MB, title="SŒURS Launch Strategy")
    doc.addPageTemplates([PageTemplate(
        id="main", frames=[Frame(ML, MB, W - ML - MR, H - MT - MB)],
        onPage=header_footer)])

    story = []
    title_page(story, "SŒURS FRAGRANCES", "Launch Marketing Strategy",
               [datetime.date.today().strftime("%d %B %Y"),
                "Internal — founders only",
                "Adversarially reviewed (ETR multi-agent panel)"])

    toc = TableOfContents(); toc.levelStyles = [S_TOC1]
    story.append(Paragraph("Contents", S_H1))
    story.append(toc)
    story.append(PageBreak())

    i = 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if ln.startswith("# ") or ln == "---" or not ln.strip():
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
                story.append(Spacer(1, 4))
                story.append(make_table(rows))
                story.append(Spacer(1, 8))
            continue
        elif re.match(r"^\d+\.\s", ln):
            num, rest = ln.split(".", 1)
            para = collect_wrapped(lines, i, rest.strip())
            story.append(Paragraph(inline(para[0]),
                                   S_BULLET, bulletText=f"{num}."))
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

    doc.multiBuild(story)
    print(f"PDF written: {out_path}")


def collect_wrapped(lines, i, first):
    """Merge markdown soft-wrapped continuation lines into one paragraph."""
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


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    build(sys.argv[1], sys.argv[2])
