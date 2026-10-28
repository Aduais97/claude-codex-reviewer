#!/usr/bin/env python3
"""HNZ RFP 0018709 Tender Review Pack — markdown -> PDF.

Per ASG generate-pdf standards: ReportLab, A4, 54/62pt margins, navy+gold,
10pt body / 8.5pt tables (min 8pt), title page + ToC, PART divider pages,
no tinted callout boxes. Two-pass build for page totals.

Usage: .venv/bin/python build_tender_pack_pdf.py <master.md> <out.pdf>
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
LIGHT_BLUE = HexColor("#E8EDF5")
ROW_ALT = HexColor("#F2F4F8")
BORDER = HexColor("#D0D5DD")
TEXT_D = HexColor("#1A1A2E")
TEXT_M = HexColor("#4A4A5A")
TEXT_L = HexColor("#7A7A8A")

W, H = A4
ML, MR, MT, MB = 54, 54, 62, 54
AVAIL = W - ML - MR

S_BODY = ParagraphStyle("body", fontName="Helvetica", fontSize=10,
                        leading=14.2, textColor=TEXT_D, alignment=4,
                        spaceAfter=5)
S_BULLET = ParagraphStyle("bullet", parent=S_BODY, leftIndent=18,
                          bulletIndent=6, spaceAfter=3)
S_QUOTE = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9,
                         leading=12.5, textColor=TEXT_M, leftIndent=18,
                         spaceAfter=3)
S_H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=13,
                      textColor=white, backColor=NAVY,
                      borderPadding=(4, 8, 4, 8), leading=17,
                      spaceBefore=12, spaceAfter=7)
S_H3 = ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=11.5,
                      textColor=DBLUE, spaceBefore=9, spaceAfter=4)
S_H4 = ParagraphStyle("h4", fontName="Helvetica-Bold", fontSize=10.5,
                      textColor=MBLUE, spaceBefore=7, spaceAfter=3)

DOC = {"total": "?", "header": "ASG  |  Health NZ Security Officer Services RFP 0018709 — Tender Review Pack"}
TOC = []  # (level, text, page) collected on pass 1


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
    canvas.drawString(ML, 30, "28 October 2026")
    canvas.drawCentredString(W / 2, 30, f"Page {doc.page} of {DOC['total']}")
    canvas.drawRightString(W - MR, 30, "Prepared for Ahmad Duais, CEO")
    canvas.restoreState()


class TocPara(Paragraph):
    """Paragraph that records its page number for the ToC on pass 1."""
    def __init__(self, text, style, level, raw):
        super().__init__(text, style)
        self._lvl, self._raw = level, raw

    def draw(self):
        TOC.append((self._lvl, self._raw, self.canv.getPageNumber()))
        super().draw()


def make_table(rows):
    n = max(len(r) for r in rows)
    th = ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=8.5,
                        textColor=white, leading=10.5)
    td = ParagraphStyle("td", fontName="Helvetica", fontSize=8.5,
                        leading=10.8, textColor=TEXT_D)
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
        txt = rows[i][0].lower() if rows[i] else ""
        if "total" in txt and "**" in rows[i][0].lower():
            style.append(("BACKGROUND", (0, i), (-1, i), LIGHT_BLUE))
        elif i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
    t.setStyle(TableStyle(style))
    return t


def title_page(story):
    story.append(Spacer(1, 150))
    story.append(HRFlowable(width="40%", thickness=1.6, color=GOLD, hAlign="CENTER"))
    story.append(Spacer(1, 22))
    story.append(Paragraph("SECURITY OFFICER SERVICES", ParagraphStyle(
        "t1", fontName="Helvetica-Bold", fontSize=30, leading=36,
        textColor=NAVY, alignment=1)))
    story.append(Paragraph("RFP 0018709 — Health New Zealand | Te Whatu Ora", ParagraphStyle(
        "t2", fontName="Helvetica-Bold", fontSize=15, leading=20,
        textColor=DBLUE, alignment=1, spaceBefore=12)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Full Tender Review & Response Requirements Pack", ParagraphStyle(
        "t3", fontName="Helvetica-Oblique", fontSize=12, leading=16,
        textColor=MBLUE, alignment=1)))
    story.append(Spacer(1, 22))
    story.append(HRFlowable(width="40%", thickness=1.6, color=GOLD, hAlign="CENTER"))
    story.append(Spacer(1, 60))
    info = [["Prepared for", "Ahmad Duais, CEO — Absolute Security Group"],
            ["Prepared", "28 October 2026 (ETR multi-agent review applied)"],
            ["Proposal deadline", "Friday 6 November 2026, 12:00 PM midday (GETS locks)"],
            ["Question deadline", "Friday 30 October 2026, 5:00 PM"],
            ["Recommendation", "BID — Northern Panel: Auckland + Counties Manukau + Waitemata; Northland = decision point"],
            ["Sources", "RFP V2, Response Form V3, Attachments B–X (32 documents), supplier briefings, 30 GETS Q&A items"]]
    t = Table([[Paragraph(f"<b>{a}</b>", ParagraphStyle("ia", fontName="Helvetica-Bold", fontSize=9, textColor=NAVY, leading=12)),
                Paragraph(b, ParagraphStyle("ib", fontName="Helvetica", fontSize=9, textColor=TEXT_D, leading=12))]
               for a, b in info], colWidths=[AVAIL * 0.24, AVAIL * 0.66])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), HexColor("#F7F8FA")),
                           ("BOX", (0, 0), (-1, -1), 0.4, BORDER),
                           ("INNERGRID", (0, 0), (-1, -1), 0.4, BORDER),
                           ("TOPPADDING", (0, 0), (-1, -1), 6),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
    t.hAlign = "CENTER"
    story.append(t)
    story.append(Spacer(1, 60))
    story.append(Paragraph(
        "Commercial in confidence. Prepared for internal bid decision-making. Hour and revenue figures are "
        "indicative sizing from Health NZ historical data; no hours are guaranteed under this RFP.",
        ParagraphStyle("disc", fontName="Helvetica-Oblique", fontSize=8,
                       textColor=TEXT_M, alignment=1, leading=11)))
    story.append(PageBreak())


def toc_page(story, toc):
    story.append(Paragraph("Contents", ParagraphStyle(
        "toct", fontName="Helvetica-Bold", fontSize=18, textColor=NAVY,
        spaceAfter=14)))
    if not toc:
        story.append(Paragraph("(generated on second pass)", S_BODY))
    else:
        rows = []
        for lvl, text, page in toc:
            if lvl == 1:
                rows.append([Paragraph(f"<b>{inline(text)}</b>", ParagraphStyle(
                    "tc1", fontName="Helvetica-Bold", fontSize=10, textColor=NAVY, leading=15)),
                    Paragraph(f"<b>{page}</b>", ParagraphStyle("tp1", fontName="Helvetica-Bold", fontSize=10, textColor=NAVY, alignment=2))])
            else:
                rows.append([Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;" + inline(text), ParagraphStyle(
                    "tc2", fontName="Helvetica", fontSize=9, textColor=TEXT_M, leading=13)),
                    Paragraph(str(page), ParagraphStyle("tp2", fontName="Helvetica", fontSize=9, textColor=TEXT_M, alignment=2))])
        t = Table(rows, colWidths=[AVAIL - 40, 40])
        t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                               ("TOPPADDING", (0, 0), (-1, -1), 1.5),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]))
        story.append(t)
    story.append(PageBreak())


def part_divider(story, text):
    story.append(Spacer(1, 230))
    story.append(HRFlowable(width="55%", thickness=1.4, color=GOLD, hAlign="CENTER"))
    story.append(Spacer(1, 20))
    story.append(TocPara(inline(text), ParagraphStyle(
        "part", fontName="Helvetica-Bold", fontSize=22, leading=28,
        textColor=NAVY, alignment=1), 1, re.sub(r"\*\*", "", text)))
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="55%", thickness=1.4, color=GOLD, hAlign="CENTER"))
    story.append(PageBreak())


def collect_wrapped(lines, i, first):
    parts = [first]
    j = i + 1
    while j < len(lines):
        nxt = lines[j].rstrip()
        if (not nxt.strip() or nxt.startswith(("#", "|", "- ", "---", "> "))
                or re.match(r"^\d+\.\s", nxt)):
            break
        parts.append(nxt.strip())
        j += 1
    return " ".join(parts), j


def build(md_path, out_path, toc_data):
    lines = open(md_path, encoding="utf-8").read().split("\n")
    doc = BaseDocTemplate(out_path, pagesize=A4, leftMargin=ML,
                          rightMargin=MR, topMargin=MT, bottomMargin=MB,
                          title="HNZ Security Officer Services RFP 0018709 — Tender Review Pack",
                          author="ASG")
    doc.addPageTemplates([PageTemplate(
        id="main", frames=[Frame(ML, MB, AVAIL, H - MT - MB)],
        onPage=header_footer)])

    story = []
    title_page(story)
    toc_page(story, toc_data)

    # skip preamble (duplicated on the title page) — start at the first PART
    first_part = next((k for k, l in enumerate(lines) if l.startswith("# PART")), 0)
    lines = lines[first_part:]

    i = 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip() or ln == "---":
            i += 1
            continue
        if ln.startswith("# PART"):
            part_divider(story, ln[2:])
        elif ln.startswith("# "):
            i += 1
            continue  # doc title block handled by title page
        elif ln.startswith("## "):
            # subtitle lines directly under the doc title are skipped
            if ln[3:].startswith("Full Tender Review"):
                i += 1
                continue
            story.append(TocPara(inline(ln[3:]), S_H2, 2, re.sub(r"\*\*", "", ln[3:])))
        elif ln.startswith("### "):
            story.append(Paragraph(inline(ln[4:]), S_H3))
        elif ln.startswith("#### "):
            story.append(Paragraph(inline(ln[5:]), S_H4))
        elif ln.startswith("> "):
            story.append(Paragraph(inline(ln[2:]), S_QUOTE))
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
    # pass 1: collect ToC + page count
    TOC.clear()
    n = build(sys.argv[1], sys.argv[2], None)
    DOC["total"] = str(n)
    toc_snapshot = list(TOC)
    # pass 2: real ToC + totals (page numbers shift only if ToC grows pages;
    # run a third pass with refreshed numbers to settle)
    TOC.clear()
    n2 = build(sys.argv[1], sys.argv[2], toc_snapshot)
    if n2 != n:
        DOC["total"] = str(n2)
        toc_snapshot = list(TOC)
        TOC.clear()
        n2 = build(sys.argv[1], sys.argv[2], toc_snapshot)
    print(f"PDF written: {sys.argv[2]} ({n2} pages)")
