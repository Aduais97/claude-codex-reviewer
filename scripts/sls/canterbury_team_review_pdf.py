#!/usr/bin/env python3
"""Canterbury Covert LP Team Review FY26 — internal manager-facing PDF.

Source: output/Canterbury_Team_Review_FY26.md (workflow-synthesized, adversarially
verified). Style: /generate-pdf skill standard. INTERNAL document — guard names
included by design; not for client distribution.
"""
import os, re, json, datetime, collections
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak)
from reportlab.lib.styles import ParagraphStyle
from reportlab.graphics.shapes import Drawing, Rect, String, Line

NAVY = HexColor("#1B2A4A"); DBLUE = HexColor("#2C3E6B"); MBLUE = HexColor("#4A6FA5")
GOLD = HexColor("#D4A843"); LBLUE = HexColor("#E8EDF5"); BORDER = HexColor("#D0D5DD")
ROWALT = HexColor("#F2F4F8"); TDARK = HexColor("#1A1A2E"); TMED = HexColor("#4A4A5A")
TLIGHT = HexColor("#7A7A8A")

SRC = os.path.expanduser("~/Desktop/SLS-RTC/Operations/Analytics/output/Canterbury_Team_Review_FY26.md")
BASE = "/private/tmp/claude-501/-Users-ahmadduais/39b97e60-84b8-4374-9bae-ef503507aa75/scratchpad/chch/team_baseline.json"
OUT = os.path.expanduser("~/Desktop/SLS-RTC/Operations/Analytics/output/Canterbury_Team_Review_FY26.pdf")
TODAY = datetime.date(2026, 7, 13)

M_L = M_R = 54; M_T = 62; M_B = 54
PAGE_W, PAGE_H = A4
CW = PAGE_W - M_L - M_R

# ---------- text sanitisation (WinAnsi-safe) ----------
SUB = {"≥": ">=", "≤": "<=", "✓": "(y)", "✗": "(x)",
       "ā": "a", "ē": "e", "ī": "i", "ō": "o", "ū": "u",
       "Ā": "A", "Ē": "E", "Ī": "I", "Ō": "O", "Ū": "U"}
def clean(s):
    for k, v in SUB.items(): s = s.replace(k, v)
    return s

def inline(s):
    """markdown inline -> reportlab markup. Escape first, then re-inject tags."""
    s = clean(s)
    # protect entities already present in source (&lt; &amp; &gt;)
    s = s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+?)\*(?![\w*])", r"<i>\1</i>", s)
    s = re.sub(r"`([^`]+)`", r"<font face='Courier' size='8.5'>\1</font>", s)
    return s

styles = {
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=14.5,
                           alignment=TA_JUSTIFY, textColor=TDARK, spaceAfter=7),
    "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=10, leading=14,
                             leftIndent=18, textColor=TDARK, spaceAfter=4),
    "h3": ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=11.5, leading=15,
                         textColor=DBLUE, spaceBefore=13, spaceAfter=4),
    "h4": ParagraphStyle("h4", fontName="Helvetica-Bold", fontSize=10.5, leading=14,
                         textColor=MBLUE, spaceBefore=8, spaceAfter=3),
    "small": ParagraphStyle("small", fontName="Helvetica-Oblique", fontSize=8.5,
                            leading=11.5, textColor=TMED, spaceAfter=6),
    "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=8.5, leading=10.5,
                           textColor=TDARK),
    "cellh": ParagraphStyle("cellh", fontName="Helvetica-Bold", fontSize=8.5,
                            leading=10.5, textColor=white),
    "toc": ParagraphStyle("toc", fontName="Helvetica", fontSize=10.5, leading=20, textColor=TDARK),
}

def header_footer(cv, doc):
    cv.saveState()
    cv.setStrokeColor(BORDER); cv.setLineWidth(0.5)
    cv.line(M_L, PAGE_H - 40, PAGE_W - M_R, PAGE_H - 40)
    cv.setFont("Helvetica", 7); cv.setFillColor(TLIGHT)
    cv.drawString(M_L, PAGE_H - 36, "SLS RTC  |  Canterbury Team Review FY26")
    cv.drawRightString(PAGE_W - M_R, PAGE_H - 36, "INTERNAL - CONFIDENTIAL")
    cv.line(M_L, 40, PAGE_W - M_R, 40)
    cv.setFont("Helvetica", 7.5)
    cv.drawString(M_L, 30, TODAY.strftime("%d %B %Y"))
    cv.drawCentredString(PAGE_W / 2, 30, f"Page {doc.page}")
    cv.drawRightString(PAGE_W - M_R, 30, "Ops Manager distribution only")
    cv.restoreState()

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=M_L, rightMargin=M_R,
                      topMargin=M_T, bottomMargin=M_B)
doc.addPageTemplates([PageTemplate(id="std",
    frames=[Frame(M_L, M_B, CW, PAGE_H - M_T - M_B, id="f")], onPage=header_footer)])
story = []

def section_bar(title):
    t = Table([[Paragraph(f"<font color='white'><b>{clean(title)}</b></font>",
                ParagraphStyle("s", fontName="Helvetica-Bold", fontSize=13, textColor=white))]],
              colWidths=[CW], rowHeights=[24])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY),
                           ("LINEBEFORE", (0, 0), (0, -1), 4, GOLD),
                           ("LEFTPADDING", (0, 0), (-1, -1), 10),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story.extend([Spacer(1, 14), t, Spacer(1, 9)])

def md_table(lines):
    rows = []
    for ln in lines:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) >= 2 and set(rows[1][0]) <= set("-: "):
        rows.pop(1)
    ncol = len(rows[0])
    HDR_SHORT = {"Bunnings n": "Bun", "WW n": "WW", "Sev2+ n†": "Sev2+†",
                 "Snapshot week (15–21 Jun)": "Snapshot wk (15–21 Jun)"}
    rows[0] = [HDR_SHORT.get(c, c) for c in rows[0]]
    body = []
    for i, r in enumerate(rows):
        r = (r + [""] * ncol)[:ncol]
        sty = styles["cellh"] if i == 0 else styles["cell"]
        body.append([Paragraph(inline(c), sty) for c in r])
    if ncol >= 7:      # team-at-a-glance wide table
        widths = [58, 30, 30, 56, 72, 32, 76, CW - 354]
        widths = widths[:ncol] + [max(30, CW - sum(widths[:ncol]))] * max(0, ncol - 8)
    else:
        first = 0.30 * CW
        widths = [first] + [(CW - first) / (ncol - 1)] * (ncol - 1)
    t = Table(body, colWidths=widths, repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), NAVY),
          ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
          ("LINEBELOW", (0, 0), (-1, 0), 1.2, NAVY),
          ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
          ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5)]
    for i in range(1, len(body)):
        if i % 2 == 0: st.append(("BACKGROUND", (0, i), (-1, i), ROWALT))
    t.setStyle(TableStyle(st))
    story.extend([Spacer(1, 4), t, Spacer(1, 8)])

def guard_chart():
    """Horizontal grouped bars: Bunnings vs WW incident counts per guard."""
    base = json.load(open(BASE))
    order = sorted(base, key=lambda g: -(base[g]["bunnings"]["n"] + base[g]["ww"]["n"]))
    rowh, gap, lblw = 11, 10, 96
    h = len(order) * (2 * rowh + gap) + 44
    d = Drawing(CW, h)
    maxv = max(max(base[g]["bunnings"]["n"], base[g]["ww"]["n"]) for g in order)
    barmax = CW - lblw - 60
    d.add(String(0, h - 12, "FY26 incident volume by guard and client (deployment-confounded — context, not ranking)",
                 fontName="Helvetica-Bold", fontSize=9, fillColor=NAVY))
    # legend
    d.add(Rect(0, h - 28, 8, 8, fillColor=NAVY, strokeColor=None))
    d.add(String(12, h - 27, "Bunnings", fontName="Helvetica", fontSize=8, fillColor=TMED))
    d.add(Rect(66, h - 28, 8, 8, fillColor=MBLUE, strokeColor=None))
    d.add(String(78, h - 27, "Woolworths", fontName="Helvetica", fontSize=8, fillColor=TMED))
    y = h - 44 - rowh
    for g in order:
        b, w = base[g]["bunnings"]["n"], base[g]["ww"]["n"]
        d.add(String(lblw - 6, y - rowh / 2 + 2, g.split()[0] + " " + g.split()[-1][0] + ".",
                     fontName="Helvetica", fontSize=8.5, fillColor=TDARK, textAnchor="end"))
        for val, col, yy in ((b, NAVY, y), (w, MBLUE, y - rowh)):
            bw = max(1.5, barmax * val / maxv)
            d.add(Rect(lblw, yy, bw, rowh - 1.5, fillColor=col, strokeColor=None, rx=1.5, ry=1.5))
            d.add(String(lblw + bw + 4, yy + 1.5, str(val), fontName="Helvetica",
                         fontSize=7.5, fillColor=TMED))
        y -= 2 * rowh + gap
    story.extend([Spacer(1, 4), d, Spacer(1, 6)])

# ================= title page =================
report = open(SRC).read()
story.append(Spacer(1, 120))
d = Drawing(CW, 6); d.add(Line(CW * 0.3, 3, CW * 0.7, 3, strokeColor=GOLD, strokeWidth=1.6))
story.append(d); story.append(Spacer(1, 16))
story.append(Paragraph("Canterbury Covert LP Team<br/>FY26 Performance Review",
             ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=30, leading=36,
                            alignment=TA_CENTER, textColor=NAVY)))
story.append(Spacer(1, 10))
story.append(Paragraph("<para align=center><font size=15 color='#2C3E6B'>Operational intelligence — deployment, coaching and recognition</font></para>", styles["body"]))
story.append(Spacer(1, 6))
story.append(Paragraph("<para align=center><font size=11.5 color='#4A6FA5'><i>Eight guards · 1,095 incidents · adversarially verified (25-agent review, 106 defects raised and resolved)</i></font></para>", styles["body"]))
story.append(Spacer(1, 16))
d = Drawing(CW, 6); d.add(Line(CW * 0.3, 3, CW * 0.7, 3, strokeColor=GOLD, strokeWidth=1.6))
story.append(d); story.append(Spacer(1, 40))
info = Table([["Scope", "Bunnings (3 Canterbury sites) + Woolworths (8 Christchurch sites)"],
              ["Data", "FY26 guard incident reports, 1 Jul 2025 - 30 Jun 2026"],
              ["Method", "Per-guard analysis, fairness + data-recompute critics, synthesis"],
              ["Status", "INTERNAL - ops manager distribution only. NOT disciplinary evidence."],
              ["Date", TODAY.strftime("%d %B %Y")]], colWidths=[80, 330])
info.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, -1), LBLUE),
                          ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                          ("FONTSIZE", (0, 0), (-1, -1), 9),
                          ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
                          ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                          ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
story.append(Table([[info]], colWidths=[CW], style=TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")])))
story.append(Spacer(1, 80))
story.append(Paragraph("<para align=center><font size=8 color='#4A4A5A'><i>Under NZ employment practice, any concern in this report requires its own fair investigative process — with the guard's side heard first — before any employment action is considered.</i></font></para>", styles["body"]))
story.append(PageBreak())

# ================= TOC =================
story.append(Paragraph("<font size=18 color='#1B2A4A'><b>Contents</b></font>", styles["body"]))
story.append(Spacer(1, 8))
for m in re.finditer(r"^## (.+)$", report, re.M):
    story.append(Paragraph(clean(m.group(1)), styles["toc"]))
story.append(PageBreak())

# ================= body =================
lines = report.split("\n")
i = 0
first_section = True
in_glance = False
while i < len(lines):
    ln = lines[i]
    if ln.startswith("# ") or ln.startswith("**SLS RTC |") or ln.startswith("*Prepared for the ops manager"):
        i += 1; continue          # title-page content already rendered
    if ln.startswith("## "):
        section_bar(ln[3:])
        in_glance = "TEAM AT A GLANCE" in ln
        first_section = False
        i += 1; continue
    if ln.startswith("### "):
        story.append(Paragraph(inline(ln[4:]), styles["h3"])); i += 1; continue
    if ln.startswith("#### "):
        story.append(Paragraph(inline(ln[5:]), styles["h4"])); i += 1; continue
    if ln.strip().startswith("|"):
        tbl = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            tbl.append(lines[i]); i += 1
        md_table(tbl)
        if in_glance:
            guard_chart(); in_glance = False
        continue
    if ln.strip().startswith(("- ", "* ")):
        story.append(Paragraph("•  " + inline(ln.strip()[2:]), styles["bullet"])); i += 1; continue
    if ln.strip() == "---":
        i += 1; continue
    if ln.strip().startswith("\\*") or ln.strip().startswith("†"):
        story.append(Paragraph(inline(ln.strip().lstrip("\\")), styles["small"])); i += 1; continue
    if ln.strip():
        story.append(Paragraph(inline(ln.strip()), styles["body"]))
    i += 1

doc.build(story)
print("written:", OUT, f"({os.path.getsize(OUT):,} bytes)")
