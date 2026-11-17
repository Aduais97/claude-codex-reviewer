#!/usr/bin/env python3
"""Render the HOTC Reporting App feasibility assessment (markdown) into a
client/board-grade PDF in ASG house style (navy + gold, ReportLab, clean tables,
no tinted callout boxes, TOC, title page). Per Ahmad's PDF design standards."""
import os, re, sys, html, datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, PageBreak, HRFlowable, KeepTogether,
                                NextPageTemplate)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib

SRC = sys.argv[1] if len(sys.argv) > 1 else \
    "/Users/ahmadduais/Desktop/ASG/HOTC-Reporting-App/ETR-Output/HOTC_Reporting_App_Feasibility_Assessment.md"
OUT = sys.argv[2] if len(sys.argv) > 2 else \
    "/Users/ahmadduais/Desktop/ASG/HOTC-Reporting-App/HOTC_Reporting_App_Feasibility_BMAD_GSD.pdf"
SUBTITLE = os.environ.get("DOC_SUBTITLE", "Feasibility · BMAD Strategy · GSD Execution Plan")
DOC_TITLE = os.environ.get("DOC_TITLE", "HOTC Reporting App")
DOC_VERDICT = os.environ.get("DOC_VERDICT", "CONDITIONAL_GO")
_default_blurb = ("A crime / incident / feedback reporting app for Heart of the City — digitising the\n"
                  "existing safety operation (report → live dispatch to ASG's floor team → escalation to\n"
                  "Police), with a path to commercialise the platform to other BIDs and precincts.\n"
                  "\n"
                  "Three ventures, three risk profiles:  A) HOTC MVP — strategically GO;\n"
                  "B) shared offender-intelligence layer — CONDITIONAL, legally gated;\n"
                  "C) SaaS commercialisation — CONDITIONAL, IP- and market-gated.")
DOC_BLURB = os.environ.get("DOC_BLURB", _default_blurb)
_ds = os.environ.get("DOC_DATE", "2026-09-04").split("-")
DOC_DATE = datetime.date(int(_ds[0]), int(_ds[1]), int(_ds[2]))

# Fonts (DejaVu covers arrows/math/× ≈ ≥ used heavily in the doc)
_ttf = os.path.join(matplotlib.get_data_path(), "fonts", "ttf")
try:
    pdfmetrics.registerFont(TTFont("DejaVu", os.path.join(_ttf, "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", os.path.join(_ttf, "DejaVuSans-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVu-Oblique", os.path.join(_ttf, "DejaVuSans-Oblique.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVu-BoldOblique", os.path.join(_ttf, "DejaVuSans-BoldOblique.ttf")))
    pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold",
                                  italic="DejaVu-Oblique", boldItalic="DejaVu-BoldOblique")
    F, FB, FI = "DejaVu", "DejaVu-Bold", "DejaVu-Oblique"
except Exception:
    F, FB, FI = "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"

NAVY = colors.HexColor("#1F3864"); GOLD = colors.HexColor("#C8952A")
INK = colors.HexColor("#243244"); GREY = colors.HexColor("#5A6675")
LIGHT = colors.HexColor("#EEF2F6"); FAINT = colors.HexColor("#C9D2DC")
WHITE = colors.white

def sty(name, **kw):
    base = dict(fontName=F, textColor=INK, fontSize=9.6, leading=13.8)
    base.update(kw); return ParagraphStyle(name, **base)

H1 = sty("H1", fontName=FB, fontSize=15, textColor=NAVY, leading=18, spaceBefore=16, spaceAfter=7)
H2 = sty("H2", fontName=FB, fontSize=12, textColor=NAVY, leading=15, spaceBefore=13, spaceAfter=5)
H3 = sty("H3", fontName=FB, fontSize=10.4, textColor=INK, leading=13.5, spaceBefore=9, spaceAfter=3)
H4 = sty("H4", fontName=FB, fontSize=9.6, textColor=GREY, leading=12.5, spaceBefore=6, spaceAfter=2)
BODY = sty("BODY", fontSize=9.6, leading=13.8, spaceAfter=5, alignment=TA_JUSTIFY)
QUOTE = sty("QUOTE", fontName=FI, fontSize=9.2, textColor=GREY, leading=13, spaceAfter=5,
            leftIndent=12, alignment=TA_LEFT)
BULLET = sty("BULLET", fontSize=9.6, leading=13.4, spaceAfter=2, leftIndent=14, bulletIndent=3)
TCELL = sty("TCELL", fontSize=8.3, leading=10.8, textColor=INK)
TCELLC = sty("TCELLC", fontSize=8.3, leading=10.8, textColor=INK, alignment=TA_CENTER)
TCELLR = sty("TCELLR", fontSize=8.3, leading=10.8, textColor=INK, alignment=TA_RIGHT)
THEAD = sty("THEAD", fontName=FB, fontSize=8.3, leading=10.8, textColor=WHITE)
THEADC = sty("THEADC", fontName=FB, fontSize=8.3, leading=10.8, textColor=WHITE, alignment=TA_CENTER)
SMALL = sty("SMALL", fontSize=7.8, textColor=GREY, leading=10.5)
TOCH = sty("TOCH", fontName=FB, fontSize=12, textColor=NAVY, leading=15, spaceAfter=6)

PAGE_W, PAGE_H = A4
LM = RM = 52; TM = 60; BM = 46
FRAME_W = PAGE_W - LM - RM

def esc(t):
    return html.escape(t, quote=False)

_link = re.compile(r"\[([^\]]+)\]\((?:[^)]+)\)")
_bolditalic = re.compile(r"\*\*\*(.+?)\*\*\*")
_bold = re.compile(r"\*\*(.+?)\*\*")
_ital = re.compile(r"(?<![\*A-Za-z0-9])\*(?!\s)(.+?)(?<!\s)\*(?![\*A-Za-z0-9])")
_code = re.compile(r"`([^`]+)`")

def inline(t):
    """markdown inline -> reportlab mini-html."""
    t = esc(t)
    # links -> muted source-cue text (drop url)
    t = _link.sub(lambda m: f'<font color="#5A6675">{m.group(1)}</font>', t)
    t = _bolditalic.sub(lambda m: f"<b><i>{m.group(1)}</i></b>", t)
    t = _bold.sub(lambda m: f"<b>{m.group(1)}</b>", t)
    t = _ital.sub(lambda m: f"<i>{m.group(1)}</i>", t)
    t = _code.sub(lambda m: f'<font face="Courier">{m.group(1)}</font>', t)
    return t

def is_table_row(l): return l.strip().startswith("|") and l.strip().endswith("|") and "|" in l.strip()[1:-1] + "|"
def is_sep_row(l):
    cells = [c.strip() for c in l.strip().strip("|").split("|")]
    return all(re.fullmatch(r":?-{2,}:?", c or "") for c in cells) and len(cells) > 0

def split_row(l):
    return [c.strip() for c in l.strip().strip("|").split("|")]

def col_align(sep_cells):
    al = []
    for c in sep_cells:
        c = c.strip()
        if c.startswith(":") and c.endswith(":"): al.append("c")
        elif c.endswith(":"): al.append("r")
        else: al.append("l")
    return al

def make_table(rows):
    header = split_row(rows[0])
    aligns = col_align(split_row(rows[1]))
    body = [split_row(r) for r in rows[2:]]
    ncol = len(header)
    aligns = (aligns + ["l"]*ncol)[:ncol]

    # column widths proportional to content, but never narrower than the longest
    # single word (prevents ugly mid-word header breaks like "timelin e")
    def longest_word(s):
        return max([len(w) for w in re.split(r"\s+", re.sub(r"[*`]", "", s))] or [1])
    weights, floors = [], []
    for i in range(ncol):
        mx = len(header[i]); lw = longest_word(header[i])
        for r in body:
            if i < len(r):
                mx = max(mx, min(len(r[i]), 55))
        weights.append(max(mx, lw + 1))
        # hard floor from the HEADER's longest word only — headers must never
        # break mid-word; long cell words (e.g. "misidentification") may wrap.
        floors.append(lw)
    # ~5.7pt per character at 8.3pt DejaVu; reserve each col's longest-word width
    # FIRST, then distribute the leftover by content weight — so narrow columns
    # keep enough room and never break a word.
    min_w = [max(30, f * 7.5 + 10) for f in floors]  # generous: no mid-word header breaks
    base = sum(min_w)
    if base <= FRAME_W:
        rem = FRAME_W - base; wtot = sum(weights) or 1
        widths = [min_w[i] + rem * weights[i] / wtot for i in range(ncol)]
    else:  # genuinely over-constrained: scale the floors down to fit
        k = FRAME_W / base; widths = [w * k for w in min_w]

    def cellpara(txt, align, hdr=False):
        if hdr:
            st = THEADC if align == "c" else THEAD
        else:
            st = {"c": TCELLC, "r": TCELLR}.get(align, TCELL)
        return Paragraph(inline(txt), st)

    data = [[cellpara(header[i], aligns[i], hdr=True) for i in range(ncol)]]
    for r in body:
        r = (r + [""]*ncol)[:ncol]
        data.append([cellpara(r[i], aligns[i]) for i in range(ncol)])

    t = Table(data, colWidths=widths, repeatRows=1)
    ts = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, GOLD),
        ("GRID", (0, 1), (-1, -1), 0.4, FAINT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT]),
    ]
    t.setStyle(TableStyle(ts))
    return t

def parse(md):
    lines = md.split("\n")
    blocks = []
    i = 0
    while i < len(lines):
        l = lines[i]
        s = l.strip()
        if not s:
            i += 1; continue
        # tables
        if is_table_row(l) and i+1 < len(lines) and is_sep_row(lines[i+1]):
            tbl = [l]; j = i+1
            while j < len(lines) and is_table_row(lines[j]):
                tbl.append(lines[j]); j += 1
            blocks.append(("table", tbl)); i = j; continue
        if s.startswith("#### "): blocks.append(("h4", s[5:])); i += 1; continue
        if s.startswith("### "): blocks.append(("h3", s[4:])); i += 1; continue
        if s.startswith("## "): blocks.append(("h2", s[3:])); i += 1; continue
        if s.startswith("# "): blocks.append(("h1", s[2:])); i += 1; continue
        if re.fullmatch(r"-{3,}", s): blocks.append(("hr", None)); i += 1; continue
        if s.startswith(">"):
            q = [s.lstrip(">").strip()]; j = i+1
            while j < len(lines) and lines[j].strip().startswith(">"):
                q.append(lines[j].strip().lstrip(">").strip()); j += 1
            blocks.append(("quote", " ".join(q))); i = j; continue
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)", l)
        if m:
            items = []; j = i
            while j < len(lines):
                mm = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)", lines[j])
                if mm:
                    marker = mm.group(2)
                    ordered = bool(re.match(r"\d+\.", marker))
                    items.append((ordered, marker, mm.group(3))); j += 1
                elif lines[j].strip() == "":
                    break
                else:
                    # continuation line
                    if items: items[-1] = (items[-1][0], items[-1][1], items[-1][2] + " " + lines[j].strip()); j += 1
                    else: break
            blocks.append(("list", items)); i = j; continue
        # paragraph (gather until blank / structural)
        para = [s]; j = i+1
        while j < len(lines):
            nx = lines[j]; ns = nx.strip()
            if ns == "" or ns.startswith("#") or ns.startswith(">") or is_table_row(nx) \
               or re.match(r"^(\s*)([-*]|\d+\.)\s+", nx) or re.fullmatch(r"-{3,}", ns):
                break
            para.append(ns); j += 1
        blocks.append(("p", " ".join(para))); i = j
    return blocks

# ---- read + strip the top metadata block into a subtitle for the title page ----
raw = open(SRC, encoding="utf-8").read()
blocks = parse(raw)

story = []
# TOC
toc = TableOfContents()
toc.levelStyles = [
    ParagraphStyle("toc1", fontName=FB, fontSize=9.6, textColor=INK, leading=15, leftIndent=6),
    ParagraphStyle("toc2", fontName=F, fontSize=8.8, textColor=GREY, leading=12.5, leftIndent=20),
]

first_h1_seen = False
for kind, payload in blocks:
    if kind == "h1":
        if not first_h1_seen:
            # place TOC before the first H1 (after title page)
            story.append(Paragraph("Contents", TOCH))
            story.append(HRFlowable(width="100%", thickness=1.2, color=GOLD, spaceAfter=8))
            story.append(toc)
            story.append(PageBreak())
            first_h1_seen = True
        p = Paragraph(inline(payload), H1)
        story.append(HRFlowable(width="100%", thickness=0.7, color=FAINT, spaceBefore=2, spaceAfter=4))
        story.append(p)
    elif kind == "h2":
        story.append(Paragraph(inline(payload), H2))
    elif kind == "h3":
        story.append(Paragraph(inline(payload), H3))
    elif kind == "h4":
        story.append(Paragraph(inline(payload), H4))
    elif kind == "p":
        story.append(Paragraph(inline(payload), BODY))
    elif kind == "quote":
        story.append(Paragraph(inline(payload), QUOTE))
    elif kind == "hr":
        story.append(Spacer(1, 2))
    elif kind == "list":
        for ordered, marker, txt in payload:
            bullet = marker if ordered else "•"
            story.append(Paragraph(inline(txt), BULLET, bulletText=bullet))
    elif kind == "table":
        story.append(Spacer(1, 2))
        story.append(make_table(payload))
        story.append(Spacer(1, 5))

# ---------------- Title page + doc template ----------------
def title_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - 200, PAGE_W, 200, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, PAGE_H - 206, PAGE_W, 6, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont(FB, 11)
    canvas.drawString(LM, PAGE_H - 60, "ABSOLUTE SECURITY GROUP")
    canvas.setFont(F, 9)
    canvas.setFillColor(colors.HexColor("#AEBAD0"))
    canvas.drawString(LM, PAGE_H - 76, "Corporate Advisory  ·  New-Venture Feasibility")
    canvas.setFillColor(WHITE)
    canvas.setFont(FB, 22)
    canvas.drawString(LM, PAGE_H - 128, DOC_TITLE)
    canvas.setFont(FB, 15)
    canvas.setFillColor(colors.HexColor("#E7D6AE"))
    canvas.drawString(LM, PAGE_H - 152, SUBTITLE)
    # verdict band
    canvas.setFillColor(INK); canvas.setFont(FB, 12)
    canvas.drawString(LM, PAGE_H - 250, "Verdict:  " + DOC_VERDICT)
    canvas.setFillColor(GREY); canvas.setFont(F, 9.6)
    txt = DOC_BLURB.split("\n")
    y = PAGE_H - 274
    for line in txt:
        canvas.drawString(LM, y, line); y -= 14
    # meta
    canvas.setStrokeColor(FAINT); canvas.setLineWidth(0.6)
    canvas.line(LM, 150, PAGE_W - RM, 150)
    canvas.setFillColor(INK); canvas.setFont(FB, 9)
    canvas.drawString(LM, 132, "Prepared for")
    canvas.setFont(F, 9); canvas.setFillColor(GREY)
    canvas.drawString(LM + 90, 132, "Ahmad Duais, CEO — Absolute Security Group Ltd")
    canvas.setFillColor(INK); canvas.setFont(FB, 9)
    canvas.drawString(LM, 116, "Method")
    canvas.setFont(F, 9); canvas.setFillColor(GREY)
    canvas.drawString(LM + 90, 116, "ETR cross-model analysis (Claude ⇄ Codex) over a 3-stream cited research base")
    canvas.setFillColor(INK); canvas.setFont(FB, 9)
    canvas.drawString(LM, 100, "Date")
    canvas.setFont(F, 9); canvas.setFillColor(GREY)
    canvas.drawString(LM + 90, 100, DOC_DATE.strftime("%d %B %Y"))
    canvas.setFillColor(colors.HexColor("#9AA6B6")); canvas.setFont(FI, 8)
    canvas.drawString(LM, 66, "Board-confidential — decision-grade. Items flagged [UNVERIFIED] / [ANALYST ESTIMATE] "
                              "must be confirmed before external circulation.")
    canvas.restoreState()

def later_pages(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(FAINT); canvas.setLineWidth(0.5)
    canvas.line(LM, BM - 12, PAGE_W - RM, BM - 12)
    canvas.setFont(F, 7.6); canvas.setFillColor(GREY)
    canvas.drawString(LM, BM - 22, os.environ.get("DOC_FOOTER", "HOTC Reporting App — Feasibility, BMAD & GSD"))
    canvas.drawRightString(PAGE_W - RM, BM - 22, "Absolute Security Group  ·  Board-confidential")
    canvas.setFont(FB, 7.6); canvas.setFillColor(NAVY)
    canvas.drawCentredString(PAGE_W / 2, BM - 22, str(doc.page))
    canvas.restoreState()

class Doc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            sn = flowable.style.name
            if sn == "H1":
                self.notify("TOCEntry", (0, flowable.getPlainText(), self.page))
            elif sn == "H2":
                self.notify("TOCEntry", (1, flowable.getPlainText(), self.page))

frame = Frame(LM, BM, FRAME_W, PAGE_H - TM - BM, id="main")
doc = Doc(OUT, pagesize=A4, leftMargin=LM, rightMargin=RM, topMargin=TM, bottomMargin=BM,
          title="HOTC Reporting App — Feasibility, BMAD & GSD", author="Absolute Security Group")
doc.addPageTemplates([
    PageTemplate(id="title", frames=[Frame(LM, BM, FRAME_W, PAGE_H - TM - BM)], onPage=title_page),
    PageTemplate(id="body", frames=[frame], onPage=later_pages),
])

flow = [Spacer(1, 1), NextPageTemplate("body"), PageBreak()]  # page 1 = title (canvas), then body
flow += story
doc.multiBuild(flow)
print("WROTE", OUT)
