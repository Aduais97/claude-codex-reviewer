#!/usr/bin/env python3
"""34 Follies Way, Dairy Flat - ETR Valuation PDF.

Navy+gold house style per ~/.claude/commands/references/generate-pdf.md.
Output: ~/Desktop/Property/34_Follies_Way_ETR_Valuation_Nov2026.pdf
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak, KeepTogether,
                                Flowable, HRFlowable)
from reportlab.graphics.shapes import Drawing, Polygon, Line, Rect, String, Group
from reportlab.graphics import renderPDF

NAVY = HexColor('#1B2A4A'); DARKBLUE = HexColor('#2C3E6B'); MIDBLUE = HexColor('#4A6FA5')
GOLD = HexColor('#D4A843'); LIGHTBLUE = HexColor('#E8EDF5'); BGGREY = HexColor('#F7F8FA')
BORDER = HexColor('#D0D5DD'); ROWALT = HexColor('#F2F4F8')
TEXTD = HexColor('#1A1A2E'); TEXTM = HexColor('#4A4A5A'); TEXTL = HexColor('#7A7A8A')
RED = HexColor('#C0392B'); AMBER = HexColor('#E67E22'); GREEN = HexColor('#27AE60')
GRIDBLUE = HexColor('#2A78D6')

PAGE_W, PAGE_H = A4
ML, MR, MT, MB = 54, 54, 62, 54
CW = PAGE_W - ML - MR

OUT = os.path.expanduser('~/Desktop/Property/34_Follies_Way_ETR_Valuation_Nov2026.pdf')

S = {}
S['body'] = ParagraphStyle('body', fontName='Helvetica', fontSize=10, leading=14.5,
                           textColor=TEXTD, alignment=TA_JUSTIFY, spaceAfter=7)
S['bodyL'] = ParagraphStyle('bodyL', parent=S['body'], alignment=TA_LEFT)
S['small'] = ParagraphStyle('small', parent=S['body'], fontSize=8.5, leading=12,
                            textColor=TEXTM, alignment=TA_LEFT)
S['bullet'] = ParagraphStyle('bullet', parent=S['body'], leftIndent=18, bulletIndent=6,
                             spaceAfter=5, alignment=TA_LEFT)
S['h2'] = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=13, leading=16,
                         textColor=white, spaceBefore=0, spaceAfter=0)
S['h3'] = ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=11.5, leading=14,
                         textColor=DARKBLUE, spaceBefore=12, spaceAfter=4)
S['cap'] = ParagraphStyle('cap', fontName='Helvetica-Oblique', fontSize=8.5, leading=11.5,
                          textColor=TEXTM, spaceBefore=4, spaceAfter=8)
S['cell'] = ParagraphStyle('cell', fontName='Helvetica', fontSize=8.5, leading=11,
                           textColor=TEXTD, alignment=TA_LEFT)
S['cellC'] = ParagraphStyle('cellC', parent=S['cell'], alignment=TA_CENTER)
S['cellH'] = ParagraphStyle('cellH', fontName='Helvetica-Bold', fontSize=8.5, leading=11,
                            textColor=white, alignment=TA_CENTER)
S['toc1'] = ParagraphStyle('toc1', fontName='Helvetica', fontSize=10.5, leading=19,
                           textColor=TEXTD)


class SectionBar(Flowable):
    """Navy bar with 4pt gold left accent and white bold title."""
    def __init__(self, number, title):
        super().__init__()
        self.number = number; self.title = title; self.height = 24

    def wrap(self, aw, ah):
        self.width = aw
        return aw, self.height + 10

    def draw(self):
        c = self.canv
        c.setFillColor(NAVY)
        c.rect(0, 0, self.width, self.height, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(0, 0, 4, self.height, stroke=0, fill=1)
        c.setFillColor(white)
        c.setFont('Helvetica-Bold', 13)
        label = f"{self.number}.  {self.title}" if self.number else self.title
        c.drawString(12, 7, label)


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(BORDER); canvas.setLineWidth(0.5)
    canvas.line(ML, PAGE_H - 40, PAGE_W - MR, PAGE_H - 40)
    canvas.setFont('Helvetica', 7); canvas.setFillColor(TEXTL)
    canvas.drawString(ML, PAGE_H - 36, 'Duais Family Land Bank  |  34 Follies Way ETR Valuation')
    canvas.drawRightString(PAGE_W - MR, PAGE_H - 36, 'CONFIDENTIAL')
    canvas.line(ML, 40, PAGE_W - MR, 40)
    canvas.setFont('Helvetica', 7.5)
    canvas.drawString(ML, 30, '15 November 2026')
    canvas.drawCentredString(PAGE_W / 2, 30, f'Page {doc.page}')
    canvas.drawRightString(PAGE_W - MR, 30, 'ETR run wf_290129c0-25e')
    canvas.restoreState()


def datatable(headers, rows, widths, align_first_left=True, bold_rows=(), status_cols=()):
    hdr = [Paragraph(h, S['cellH']) for h in headers]
    body = []
    for r in rows:
        line = []
        for ci, cell in enumerate(r):
            st = S['cell'] if (ci == 0 and align_first_left) else S['cellC']
            line.append(Paragraph(cell, st))
        body.append(line)
    t = Table([hdr] + body, colWidths=widths, repeatRows=1)
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('GRID', (0, 0), (-1, -1), 0.4, BORDER),
        ('LINEBELOW', (0, 0), (-1, 0), 1.2, NAVY),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]
    for i in range(len(body)):
        if i % 2 == 1:
            style.append(('BACKGROUND', (0, i + 1), (-1, i + 1), ROWALT))
    for i in bold_rows:
        style.append(('BACKGROUND', (0, i + 1), (-1, i + 1), LIGHTBLUE))
    t.setStyle(TableStyle(style))
    return t


def corridor_drawing():
    """Plan-view schematic, simplified from the GIS geometry. Not to survey."""
    W, H = CW, 250
    d = Drawing(W, H)
    scale = W / 860.0

    def sx(x): return x * scale
    def sy(y): return H - y * (H / 440.0)

    wash = HexColor('#F7E8C8')
    # corridor band
    d.add(Polygon([sx(748.9), sy(17.8), sx(588.9), sy(457.8), sx(491.1), sy(422.2),
                   sx(651.1), sy(-17.8)], fillColor=wash, strokeColor=None))
    for xoff in (-48.9, 48.9):
        d.add(Line(sx(700 + xoff), sy(0 + (17.8 if xoff > 0 else -17.8)),
                   sx(540 + xoff), sy(440 + (17.8 if xoff > 0 else -17.8)),
                   strokeColor=AMBER, strokeWidth=0.6, strokeDashArray=[3, 2]))
    d.add(Line(sx(700), sy(0), sx(540), sy(440), strokeColor=AMBER, strokeWidth=1.8))
    # towers
    for tx, ty in ((663, 71), (593, 265)):
        d.add(Rect(sx(tx), sy(ty + 16), 11, 11, fillColor=AMBER, strokeColor=white, strokeWidth=1.2))
    # parcel
    d.add(Polygon([sx(120), sy(100), sx(430), sy(68), sx(500), sy(210), sx(420), sy(368),
                   sx(150), sy(350)], fillColor=HexColor('#EAF0EA'), strokeColor=NAVY, strokeWidth=1.6))
    def txt(x, y, s_, size=8.5, color=TEXTD, bold=False, anchor='start'):
        d.add(String(sx(x), sy(y), s_, fontName='Helvetica-Bold' if bold else 'Helvetica',
                     fontSize=size, fillColor=color, textAnchor=anchor))
    txt(190, 185, '34 Follies Way', 12, NAVY, True)
    txt(190, 207, 'Lot 7 DP 512543  -  20,090 m2', 8.5, TEXTM)
    txt(190, 227, '0.00% corridor overlap - no tower on parcel', 9, GREEN, True)
    txt(432, 26, '20 Follies Way', 9, TEXTD, True)
    txt(432, 42, 'crossed 117.8 m, tower on parcel', 8, AMBER)
    txt(648, 396, '22 Follies Way', 9, TEXTD, True)
    txt(648, 412, 'crossed 55 m', 8, AMBER)
    txt(655, 82, '61.6 m to tower A0019', 8.5, TEXTD, False, 'end')
    txt(618, 128, '36.8 m to centreline', 8.5, TEXTD, False, 'end')
    txt(524, 266, '23.2 m to corridor edge', 8.5, TEXTD, False, 'end')
    d.add(Line(sx(622), sy(132), sx(645), sy(152), strokeColor=TEXTL, strokeWidth=0.6))
    d.add(Line(sx(528), sy(258), sx(567), sy(214), strokeColor=TEXTL, strokeWidth=0.6))
    txt(594, 300, 'A0018', 7.5, TEXTM)
    txt(48, 396, 'Follies Way (private) to Bawden Rd', 8, TEXTL)
    d.add(Line(sx(40), sy(406), sx(300), sy(424), strokeColor=TEXTL, strokeWidth=2.5))
    return d


def comps_drawing():
    comps = [
        ('13 Bobs Way', 40.1, 'unk', 'sold'),
        ('63 Follies (crossed)', 47.2, 'crossed', 'sold'),
        ('233 Bawden Rd', 51.7, 'clear', 'sold'),
        ('53 Follies', 59.5, 'unk', 'sold'),
        ('164 Top Rd', 73.9, 'unk', 'sold'),
        ('5 Bobs Way', 74.9, 'unk', 'sold'),
        ('166H Postman Rd', 87.0, 'unk', 'sold'),
        ('79 Follies', 92.4, 'clear', 'sold'),
        ('71 Follies', 95.2, 'clear', 'sold'),
        ('34 Follies - SUBJECT ask', 59.7, 'clear', 'ask'),
        ('20 Follies ask (crossed)', 63.9, 'crossed', 'ask'),
        ('79 Follies ask', 92.4, 'clear', 'ask'),
    ]
    rowh, barh, padl, padr, padt, padb = 19, 11, 150, 40, 18, 34
    W = CW
    H = padt + rowh * len(comps) + padb
    d = Drawing(W, H)
    maxv = 100.0
    plot_w = W - padl - padr

    def x(v): return padl + v / maxv * plot_w

    for g in range(0, 101, 20):
        d.add(Line(x(g), padb, x(g), H - padt + 6, strokeColor=HexColor('#E3E5EA'), strokeWidth=0.5))
        d.add(String(x(g), padb - 11, f'${g}', fontName='Helvetica', fontSize=7.5,
                     fillColor=TEXTL, textAnchor='middle'))
    for v, lab, anch in ((47.3, 'OPEN $47.3', 'end'), (52.3, 'CAP $52.3', 'start')):
        d.add(Line(x(v), padb, x(v), H - padt + 10, strokeColor=GREEN, strokeWidth=0.9,
                   strokeDashArray=[3, 2]))
        d.add(String(x(v) + (3 if anch == 'start' else -3), H - padt + 12, lab,
                     fontName='Helvetica-Bold', fontSize=7.5, fillColor=GREEN, textAnchor=anch))
    for i, (name, v, grid, kind) in enumerate(comps):
        yc = H - padt - i * rowh - rowh / 2
        fill = {'clear': GRIDBLUE, 'crossed': AMBER, 'unk': HexColor('#9A998E')}[grid]
        if kind == 'ask':
            fill = HexColor({'clear': '#BBD5F3', 'crossed': '#F2D9A8', 'unk': '#D8D7CF'}[grid])
        bold = 'SUBJECT' in name
        d.add(String(padl - 6, yc - 3, name, fontName='Helvetica-Bold' if bold else 'Helvetica',
                     fontSize=8, fillColor=TEXTD, textAnchor='end'))
        d.add(Rect(padl, yc - barh / 2, x(v) - padl, barh, fillColor=fill, strokeColor=None))
        d.add(String(x(v) + 4, yc - 3, f'{v:.1f}', fontName='Helvetica', fontSize=7.5,
                     fillColor=TEXTM))
    legend = [(GRIDBLUE, 'Grid-clear (verified)'), (AMBER, 'Corridor-crossed'),
              (HexColor('#9A998E'), 'Status unverified'), (HexColor('#BBD5F3'), 'Tinted = current ask')]
    lx = padl
    for col, lab in legend:
        d.add(Rect(lx, 1, 8, 8, fillColor=col, strokeColor=None))
        d.add(String(lx + 12, 2.5, lab, fontName='Helvetica', fontSize=7.5, fillColor=TEXTM))
        lx += 12 + len(lab) * 3.8 + 16
    return d


def build():
    doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=ML, rightMargin=MR,
                          topMargin=MT, bottomMargin=MB,
                          title='34 Follies Way ETR Valuation',
                          author='Duais Family Land Bank')
    frame = Frame(ML, MB, CW, PAGE_H - MT - MB, id='main')
    doc.addPageTemplates([PageTemplate(id='all', frames=[frame], onPage=header_footer)])
    E = []

    # ---------------- title page ----------------
    E.append(Spacer(1, 90))
    E.append(HRFlowable(width='40%', thickness=1.4, color=GOLD, hAlign='CENTER'))
    E.append(Spacer(1, 26))
    E.append(Paragraph('34 Follies Way, Dairy Flat',
                       ParagraphStyle('t', fontName='Helvetica-Bold', fontSize=32, leading=38,
                                      textColor=NAVY, alignment=TA_CENTER)))
    E.append(Spacer(1, 12))
    E.append(Paragraph('Grid-Corridor Review and Price Valuation',
                       ParagraphStyle('st', fontName='Helvetica', fontSize=16, leading=20,
                                      textColor=DARKBLUE, alignment=TA_CENTER)))
    E.append(Spacer(1, 8))
    E.append(Paragraph('ETR agentic workflow: 5 research agents, valuation synthesis, 3-lens adversarial verification',
                       ParagraphStyle('tag', fontName='Helvetica-Oblique', fontSize=12, leading=16,
                                      textColor=MIDBLUE, alignment=TA_CENTER)))
    E.append(Spacer(1, 26))
    E.append(HRFlowable(width='40%', thickness=1.4, color=GOLD, hAlign='CENTER'))
    E.append(Spacer(1, 44))
    info = [['Legal description', 'Lot 7 DP 512543', 'Record of title', 'CT 801783'],
            ['Area', '20,090 m2 (2.009 ha)', 'Zone', 'Future Urban (100%)'],
            ['Capital value (May 2024)', '$1,700,000 (all land)', 'Live asking price', '$1,199,995 incl GST'],
            ['Report date', '15 November 2026', 'Stale after', '15 Dec 2026 or any street sale']]
    it = Table(info, colWidths=[CW * 0.22, CW * 0.28, CW * 0.22, CW * 0.28])
    it.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), LIGHTBLUE), ('BACKGROUND', (2, 0), (2, -1), LIGHTBLUE),
        ('GRID', (0, 0), (-1, -1), 0.4, BORDER),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'), ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'), ('FONTNAME', (3, 0), (3, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5), ('TEXTCOLOR', (0, 0), (-1, -1), TEXTD),
        ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
    ]))
    E.append(it)
    E.append(Spacer(1, 26))
    km = [['Market value (base)', 'Vendor ask', 'Opening offer', 'Hard cap'],
          ['$1.05M', '$1,199,995', '$950,000', '$1,050,000'],
          ['range $1.00M-$1.20M', '$59.7/m2, 70.6% of CV', '$47.3/m2, 56% of CV', 'stretch $1.10M conditional']]
    kt = Table(km, colWidths=[CW / 4.0] * 4)
    kt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), LIGHTBLUE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, 0), 8.5),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'), ('FONTSIZE', (0, 1), (-1, 1), 15),
        ('TEXTCOLOR', (0, 1), (-1, 1), NAVY),
        ('FONTNAME', (0, 2), (-1, 2), 'Helvetica'), ('FONTSIZE', (0, 2), (-1, 2), 8),
        ('TEXTCOLOR', (0, 2), (-1, 2), TEXTM),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('GRID', (0, 0), (-1, -1), 0.4, BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    E.append(kt)
    E.append(Spacer(1, 60))
    E.append(Paragraph('Prepared for the Duais family land-bank mandate. Internal decision support only; '
                       'not a registered valuation. All figures NZD. Evidence verified 15 November 2026 '
                       'against Auckland Council ArcGIS, Transpower open geospatial data, and live listing portals.',
                       ParagraphStyle('disc', fontName='Helvetica-Oblique', fontSize=8, leading=11,
                                      textColor=TEXTM, alignment=TA_CENTER)))
    E.append(PageBreak())

    # ---------------- table of contents ----------------
    E.append(SectionBar('', 'Contents'))
    E.append(Spacer(1, 14))
    toc = ['1.  Verdict and the correction: this is not the pylon lot',
           '2.  Where the cable goes: the Albany-Silverdale 220 kV line',
           '3.  How sales near transmission lines actually price',
           '4.  Comparable evidence',
           '5.  Valuation build-up',
           '6.  Vendor position and negotiation',
           '7.  Title instruments reviewed',
           '8.  Conditions before any offer, and kill criteria',
           '9.  Hold economics and planning odds']
    for line in toc:
        E.append(Paragraph(line, S['toc1']))
    E.append(Spacer(1, 24))
    E.append(Paragraph('<b>Provenance.</b> ETR agentic workflow run wf_290129c0-25e, 15 November 2026: '
                       'five parallel research agents (listing and identity, GIS and grid geometry, comparable sales, '
                       'transmission-impact literature, planning and sequencing), one valuation synthesis, and three '
                       'adversarial verification lenses. Verify verdicts: grid-geometry SOUND; comparable-evidence '
                       'ADJUST (applied); thesis-liquidity ADJUST (applied). The figures in this report are the '
                       'post-adjustment numbers.', S['bodyL']))
    E.append(PageBreak())

    # ---------------- 1 verdict ----------------
    E.append(SectionBar('1', 'Verdict and the correction: this is not the pylon lot'))
    E.append(Spacer(1, 10))
    E.append(Paragraph('<b>Verdict: grid-clear, over-asked.</b> The parcel has 0.00% National Grid corridor overlap, '
                       'no tower on the land, and the conductor passes 36.8 m outside the boundary. Fair value is '
                       'around $1.05M against a $1,199,995 ask from a vendor 14.5 months into failed, dual-agency '
                       'marketing. Open at $950,000 with a hard cap of $1,050,000.', S['body']))
    E.append(Paragraph('The 1 November land-bank review eliminated a 20,100 m2 Follies Way lot ("the twin") because '
                       'transmission pylons appeared in its listing photos. This review establishes two things at '
                       'parcel level:', S['body']))
    E.append(Paragraph('<bullet>&bull;</bullet><b>The twin is 34 Follies Way itself.</b> The Harcourts PBN campaign '
                       '(Trade Me 5886963422, "PRICE DROPPED!", listed 16 Apr 2026) resolves to street address '
                       '34 Follies Way in the agency\'s own structured data, and its aerial photos match the parcel '
                       'outline. The property is dual-listed with two agencies at once.', S['bullet']))
    E.append(Paragraph('<bullet>&bull;</bullet><b>34 Follies Way is grid-clear.</b> A polygon intersect of the '
                       'council parcel against the Auckland Unitary Plan National Grid Corridor Overlay returns zero '
                       'features, cross-checked against Transpower\'s own line and tower data. A positive control on '
                       '20 Follies Way returned its two known corridor features, proving the method detects what is '
                       'there. The pylons in the photos stand on the neighbours.', S['bullet']))
    E.append(Paragraph('The family rule for corridor-crossed lots (only ever at or below $1.0M with a 70%-plus-clean '
                       'survey) therefore <b>does not bind this parcel</b>. What applies instead is an adjacency '
                       'stigma on an otherwise clean lot, plus ordinary distressed-street pricing.', S['body']))

    # ---------------- 2 cable ----------------
    E.append(Spacer(1, 8))
    E.append(SectionBar('2', 'Where the cable goes: the Albany-Silverdale 220 kV line'))
    E.append(Spacer(1, 10))
    E.append(Paragraph('The line crossing the Follies block is Transpower\'s <b>ALB-SVL-A "Albany-Silverdale A"</b>: '
                       'a 220 kV-design, double-circuit steel-tower line, 14.35 km long, running from Albany '
                       'substation (Rosedale) north to Silverdale substation. It is the radial grid feed to the '
                       'Hibiscus Coast, tying into Auckland\'s 220 kV backbone at Albany. It is commissioned, '
                       'permanent infrastructure: undergrounding costs $5-15M per km and Transpower only relocates '
                       'lines when the beneficiary pays. Plan on it being there for the life of any hold.', S['body']))
    E.append(Spacer(1, 4))
    E.append(corridor_drawing())
    E.append(Paragraph('Plan-view schematic from council parcel polygons and Transpower centreline and tower data. '
                       'Not to survey. Distances boundary-to-feature in NZTM: Subdivision Corridor edge 23.2 m, '
                       'National Grid Yard edge 24.8 m, conductor centreline 36.8 m, tower ALB-SVL-A0019 61.6 m '
                       '(standing on 20 Follies Way), tower A0018 110.4 m.', S['cap']))
    E.append(Paragraph('The street\'s corridor register', S['h3']))
    reg = [['16 Follies Way', 'Crossed 269 m', '34 Follies Way (subject)', 'CLEAR, 0.00% overlap'],
           ['20 Follies Way', 'Crossed 117.8 m + tower; 14-18% of area in corridor', '40 Follies Way', 'Clear'],
           ['22 Follies Way', 'Crossed 55 m', '44 Follies Way', 'Clear'],
           ['63 Follies Way', 'Crossed 119 m', '58 Follies Way', 'Clear'],
           ['67 Follies Way', 'Crossed 136 m', '79 Follies Way', 'Clear (250.7 m away)'],
           ['304 Bawden Rd', 'Crossed 105 m', '', '']]
    E.append(datatable(['Crossed lot', 'Extent', 'Clear lot', 'Status'], reg,
                       [CW * 0.2, CW * 0.34, CW * 0.26, CW * 0.2]))
    E.append(Paragraph('The "two overlay features" seen on 1 November are the National Grid Yard and Subdivision '
                       'Corridor bands of this one line, not two lines.', S['cap']))
    E.append(PageBreak())

    # ---------------- 3 impact ----------------
    E.append(SectionBar('3', 'How sales near transmission lines actually price'))
    E.append(Spacer(1, 10))
    E.append(Paragraph('The evidence splits into two very different effects, and the whole valuation turns on which '
                       'one applies:', S['body']))
    E.append(Paragraph('<bullet>&bull;</bullet><b>Crossing with a structure is severe.</b> NZ hedonic studies measure '
                       'minus 27% at 10 m from a pylon, minus 5% at 50 m, roughly nil beyond 100 m; a line crossing '
                       'without a structure prices at under minus 1% and is statistically insignificant. For vacant '
                       'and development land the hit is larger and leaks across the whole parcel: US studies find '
                       'minus 44.9% for adjacent vacant lots and minus 17.9% within about 300 m, because the corridor '
                       'permanently caps future subdivision yield.', S['bullet']))
    E.append(Paragraph('<bullet>&bull;</bullet><b>Adjacency-only is a single-digit stigma.</b> Two visible towers at '
                       '62 m and 110 m from a boundary justify roughly 5-10% off a bare lot. A future dwelling '
                       'platform on a 2 ha parcel sits 150 m-plus from the towers, where measured effects vanish.',
                       S['bullet']))
    E.append(Paragraph('<b>This street ran its own controlled experiment.</b> Corridor-crossed 63 Follies sold at '
                       '$47.2/m2 in Feb 2021 while clean 71 Follies sold at $95.2/m2 weeks later: a measured 50% '
                       'crossing discount that fully vindicates the family rule for crossed lots. The 2015 subdivider '
                       'sell-down shows corridor-abutting at about minus 8.6% (67 vs 75 Follies).', S['body']))
    E.append(Paragraph('At urbanisation, masterplans recycle corridor strips into roads, reserves and stormwater '
                       '(Flat Bush does this by policy), so crossed land recovers only infrastructure value, never '
                       'urban-lot value. No compensation is ever paid for existing lines. Crossed lots also sit on '
                       'market far longer: bank-pressured 20 Follies is at 291-plus days. All of that burden falls on '
                       'the neighbours here, not on 34.', S['body']))

    # ---------------- 4 comps ----------------
    E.append(Spacer(1, 8))
    E.append(SectionBar('4', 'Comparable evidence'))
    E.append(Spacer(1, 10))
    E.append(Paragraph('Sold evidence, not asking prices, sets value. The street\'s asks have demonstrably failed to '
                       'clear: 79 Follies has sat about 6 months at $92.4/m2 (its own 2020 cost), and 20 Follies is '
                       'at 291-plus days. The clean 2 ha-class benchmark, time-adjusted for a market falling about '
                       '7% a year, lands at <b>$56-58/m2</b>.', S['body']))
    E.append(comps_drawing())
    E.append(Paragraph('Dairy Flat bare-land evidence in dollars per square metre. Solid bars are sales; tinted bars '
                       'are current unsold asks. Dashed lines mark the recommended open and cap.', S['cap']))
    comps_rows = [
        ['13 Bobs Way', '34,410', 'Sold, 52% of CV', '$1,380,000', '40.1', 'Feb 2023', 'Unverified'],
        ['63 Follies Way', '21,511', 'Sold', '$1,015,000', '47.2', 'Feb 2021', '<b>Crossed 119 m</b>'],
        ['233 Bawden Rd', '20,015', 'Sold, 47% of CV', '$1,035,000', '51.7', 'Jun 2025', 'Clear'],
        ['53 Follies Way', '18,492', 'Sold', '$1,100,000', '59.5', 'Feb 2018', 'Unverified'],
        ['164 Top Rd', '37,020', 'Sold, 100% of CV, near-bare', '$2,735,761', '73.9', 'Aug 2026', 'Unverified'],
        ['5 Bobs Way', '22,692', 'Sold, 68% of CV', '$1,700,000', '74.9', 'Aug 2025', 'Unverified'],
        ['166H Postman Rd', '20,001', 'Sold, 95% of CV', '$1,740,000', '87.0', 'May 2025', 'Unverified'],
        ['79 Follies Way', '17,202', 'Sold', '$1,590,000', '92.4', 'Oct 2020', 'Clear'],
        ['71 Follies Way', '13,873', 'Sold', '$1,320,000', '95.2', 'Mar 2021', 'Clear'],
        ['<b>34 Follies Way (subject)</b>', '20,090', 'Ask, cut from ~$1.295M, 150 days', '$1,199,995', '59.7',
         'Live Nov 2026', 'Clear'],
        ['20 Follies Way', '20,024', 'Ask, 291+ days, bank-pressured', '$1,280,000', '63.9', 'Live Nov 2026',
         '<b>Crossed 117.8 m</b>'],
        ['79 Follies Way', '17,202', 'Ask, ~6 months at its 2020 cost', '$1,590,000', '92.4', 'Live Nov 2026',
         'Clear'],
    ]
    E.append(datatable(['Property', 'Size m2', 'Event', 'Price', '$/m2', 'Date', 'Grid'],
                       comps_rows,
                       [CW * 0.21, CW * 0.09, CW * 0.26, CW * 0.12, CW * 0.07, CW * 0.12, CW * 0.13],
                       bold_rows=(9,)))
    E.append(Paragraph('The paired sales 63 vs 71 Follies (same street, same month, Feb/Mar 2021) are the measured '
                       'crossing discount: minus 50%. No sale has ever been recorded for 34 Follies Way itself; '
                       'the vendor is almost certainly the original subdivider.', S['cap']))
    E.append(PageBreak())

    # ---------------- 5 build-up ----------------
    E.append(SectionBar('5', 'Valuation build-up'))
    E.append(Spacer(1, 10))
    bu = [['Clean 2 ha benchmark, time-adjusted',
           '233 Bawden $51.7 (Jun 25), 5 Bobs $74.9 (Aug 25), 13 Bobs $40.1 (Feb 23); trimmed for ~7%/yr market decline',
           '56-58', '$1.13-1.17M'],
          ['Tower-visibility stigma',
           'Minus 7.5% (band 5-10%): two visible double-circuit towers 62 m and 110 m off the NE boundary; '
           'vacant-land adjacency band 0-10%', '-4.3', '-$86k'],
          ['Private-way and covenant friction',
           'Minus 2%: mandatory management-company share, $2,000+GST/yr levy, covenant text unseen', '-1.1', '-$22k'],
          ['<b>Market value, base</b>', '<b>Adversarially adjusted (comps and thesis lenses applied)</b>',
           '<b>~52</b>', '<b>~$1.05M</b>'],
          ['Bracket', 'Low = clearance-grade $50/m2; high capped at the ask, never above it', '50-60', '$1.00-1.20M']]
    E.append(datatable(['Step', 'Basis', '$/m2', 'Value'], bu,
                       [CW * 0.22, CW * 0.5, CW * 0.12, CW * 0.16], bold_rows=(3,)))
    E.append(Paragraph('Cross-checks: 2 ha-plus bare land clears at 47-68% of CV ($800k-$1.16M on the $1.70M CV); '
                       'the ask itself is 70.6% of CV; the homes.co.nz estimate of $1.41M is above anything the '
                       'street has cleared since 2021. CV history runs $2.0M (2017) to $2.3M (2021) to $1.7M '
                       '(2024, minus 26%).', S['cap']))

    # ---------------- 6 vendor ----------------
    E.append(Spacer(1, 8))
    E.append(SectionBar('6', 'Vendor position and negotiation'))
    E.append(Spacer(1, 10))
    E.append(Paragraph('Every signal says time favours the buyer:', S['body']))
    E.append(Paragraph('<bullet>&bull;</bullet><b>No sale has ever been recorded on this title</b> since issue in '
                       'Nov 2017. The vendor is almost certainly the original subdivider (Campbell/Li or an '
                       'associate) with a 2015-era cost basis. Confirm from the title PDF already in hand.',
                       S['bullet']))
    E.append(Paragraph('<bullet>&bull;</bullet><b>Dual-listed with two competing agencies:</b> Harcourts PBN since '
                       '16 Apr 2026 ("PRICE DROPPED!") and Ray White since 18-19 Jun 2026 (failed tender, then an '
                       'advertised $1,199,995 from about 23 Oct). About 14.5 months of marketing across three '
                       'campaigns since Sep 2025, possibly 2.4 years since a 2023 campaign.', S['bullet']))
    E.append(Paragraph('<bullet>&bull;</bullet>The Harcourts listing states the vendor <b>"has purchased other '
                       'property"</b> and is <b>not GST-registered</b> (price inclusive of GST, if any). The agency '
                       'is now emailing full title packs to cold enquiries.', S['bullet']))
    E.append(Paragraph('<bullet>&bull;</bullet>Market context: Auckland volumes minus 30% year on year, about 14 '
                       'unsold Dairy Flat sections against 3-4 land sales in 18 months, zero competing-bidder '
                       'evidence anywhere on this street since 2021.', S['bullet']))
    E.append(Paragraph('The play', S['h3']))
    E.append(Paragraph('<b>Open at $950,000</b> ($47.3/m2, 56% of CV), justified line by line from sold evidence '
                       'only. <b>Hard cap $1,050,000.</b> A stretch to $1.10M is permitted only with the option '
                       'character of the hold accepted in writing. Before offering: confirm with the Harcourts agent '
                       'that his PBN listing is number 34 (one verifier could not replicate the address match), and '
                       'ask what happened to 20 Follies\' indexed Dec-2025 "sold" event: a fallen-over contract '
                       'strengthens the distress read.', S['body']))
    E.append(Paragraph('<b>Comparative rule before any offer:</b> capital goes to the cheapest clean dollar-per-'
                       'square-metre in the corridor. Check 7 Bobs Way\'s status (grid-clear, no private way, prior '
                       '"cheapest FUZ" pick), and consider a sub-$1.0M surveyor-conditional lowball at bank-pressured '
                       '20 Follies as price discovery: at 82-86% clean it actually passes the family rule, and if it '
                       'bites below $1.0M the whole street reprices.', S['body']))
    E.append(PageBreak())

    # ---------------- 7 instruments ----------------
    E.append(SectionBar('7', 'Title instruments reviewed'))
    E.append(Spacer(1, 10))
    inst = [['10959985.6', 'Right-of-way easement creating "Follies Way" (private road, 19 users)',
             '1/19th base cost share. Clauses 11-12: the road converts to a <b>public road by simple majority '
             '(10 of 19 shares)</b>. Genuinely helpful at urbanisation; no single holdout can block it.'],
            ['10959985.9 / 10780754.8', 'Residents\'-association encumbrances (Stage 2 / Stage 1)',
             'Mandatory share in Follies Way Management Ltd; levy the greater of <b>$2,000 + GST/yr</b> or 2x cost '
             'share; fines to $10,000; interest at overdraft +3%. Budget ~$2,300+/yr on top of rates.'],
            ['10959985.8', 'Amenity planting encumbrance over Lots 7, 10-13',
             '<b>Applies to this lot.</b> Perpetual obligation to preserve, stock-fence and weed planting area "AF" '
             'per a 2016 plan. Part of the 2.009 ha is sterilised for use and carries active maintenance.'],
            ['10959985.7', 'Land covenant: <b>a shell</b>',
             'The real restrictions are incorporated from <b>10780745.5 as varied by 10824937.1, which was not '
             'supplied</b>. A build-by-date or no-subdivision clause in there survives rezoning and impairs the '
             'thesis. Request both before anything else.']]
    E.append(datatable(['Instrument', 'What it is', 'What it means for the hold'], inst,
                       [CW * 0.16, CW * 0.3, CW * 0.54]))
    E.append(Paragraph('The Certificate of Title and LIM named in the agent\'s email did not arrive in the forward '
                       'reviewed here; only the five instruments did. Other overlays at the parcel: North Shore '
                       'Airport approach surface (height limits only) and six minor overland flow paths. Both '
                       'negligible for a grazing land bank.', S['cap']))

    # ---------------- 8 gates & kills ----------------
    E.append(Spacer(1, 8))
    E.append(SectionBar('8', 'Conditions before any offer, and kill criteria'))
    E.append(Spacer(1, 10))
    E.append(Paragraph('Gates: all before an offer is lodged', S['h3']))
    gates = ['Covenant text 10780745.5 + 10824937.1 read in full: no build obligations, no restrictions '
             'incompatible with a passive 7-15 yr hold.',
             'Licensed surveyor corridor map certifying the zero-overlap finding to survey grade (desktop GIS is '
             'not a survey).',
             'Title PDF read: registered owner reconciled with the marketing vendor; no caveats.',
             'LIM reviewed in full (flow paths, consents, any Crown/NZTA corridor interest).',
             'Follies Way Management Ltd pack: arrears, special levies, insurance, transfer mechanics.',
             'Written GST-inclusive warranty from the vendor.',
             'The land-taint / CB 6 accountant\'s opinion: still outstanding, still blocks every offer.']
    for i, g in enumerate(gates, 1):
        E.append(Paragraph(f'<bullet><b>{i}.</b></bullet>{g}', S['bullet']))
    E.append(Paragraph('Kills: walk immediately', S['h3']))
    kills = ['Survey shows any corridor overlap or structure on the parcel: crossed rulebook applies; default is walk.',
             'Covenants prohibit future subdivision by successors or impose a compulsory build timeframe.',
             'Deal becomes plus-GST, or the GST warranty is refused.',
             'All-in cost (price + arrears + share transfer) exceeds the cap.',
             'Management company shows arrears, litigation or uncapped special levies.',
             '20 Follies clears below about $45-50/m2 before going unconditional: re-anchor or walk.']
    for i, k in enumerate(kills, 1):
        E.append(Paragraph(f'<bullet><b><font color="#C0392B">{i}.</font></b></bullet>{k}', S['bullet']))
    E.append(PageBreak())

    # ---------------- 9 hold economics ----------------
    E.append(SectionBar('9', 'Hold economics and planning odds'))
    E.append(Spacer(1, 10))
    E.append(Paragraph('<b>The honest caveat the adversarial pass forced:</b> at $1.05M entry, a 10-year 6% p.a. '
                       'return (net of $6-7k/yr rates and levy) requires an exit near $98/m2. This street cannot '
                       'clear $92/m2 today. Market drift alone does not pay for this trade; the return comes only '
                       'from Dairy Flat entering a committed urbanisation sequence, against the ~$127/m2 historical '
                       'englobo reference once a developer bid exists.', S['body']))
    odds = [['Live urban zoning by 2033', '~10-15%'],
            ['Live urban zoning by 2041', '~35-45%'],
            ['Inside a committed, documented pre-2045 sequence by 2041 (what a land-bank exit actually prices)',
             '~60-70%']]
    E.append(datatable(['Scenario', 'Probability'], odds, [CW * 0.76, CW * 0.24]))
    E.append(Spacer(1, 6))
    E.append(Paragraph('<bullet>&bull;</bullet><b>The decisive event is Auckland\'s Regional Spatial Plan, about '
                       '2028</b>, under the new Planning Act (assent 30 Sep 2026) and the pro-growth national '
                       'direction: 30 years of live-zoned capacity required, rural-urban boundaries abolished.',
                       S['bullet']))
    E.append(Paragraph('<bullet>&bull;</bullet>Precedents cut both ways: PC103 queue-jumped 107 ha of Silverdale '
                       'West FUZ to live zoning in about 2 years; Milldale is being urbanised through fast-track '
                       'consents with private wastewater plants that bypass Watercare entirely. But every active '
                       'front is 6-8 km north, and private plan changes are barred from 1 Jan 2028.', S['bullet']))
    E.append(Paragraph('<bullet>&bull;</bullet>Watercare: Hibiscus Coast connection freeze since Nov 2024; Army Bay '
                       'upgrade about 2031; Dairy Flat servicing described as 20-plus years away.', S['bullet']))
    E.append(Spacer(1, 6))
    E.append(Paragraph('Priced at $950k-$1.05M ($47-52/m2), the parcel is a cheap, clean option on that 2028 '
                       'decision. Priced at the ask, the buyer pays today for optionality the market has already '
                       'stopped paying for.', S['body']))

    doc.build(E)
    print('WROTE', OUT)


if __name__ == '__main__':
    build()
