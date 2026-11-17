#!/usr/bin/env python3
"""Generate the 1st Call Recruitment Investor DD Briefing PDF (house style).

Reads the briefing markdown from the Investor DD Pack folder and renders it
with the standard navy/gold ReportLab layout used across the 1CR deliverables.
"""

import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, Image
)

NAVY = HexColor('#1B2A4A')
GOLD = HexColor('#C4A35A')
LIGHT_GREY = HexColor('#F5F5F5')
MID_GREY = HexColor('#E0E0E0')
DARK_GREY = HexColor('#333333')
RED_ACCENT = HexColor('#C0392B')

PAGE_W, PAGE_H = A4
MARGIN_LEFT = 54
MARGIN_RIGHT = 54
MARGIN_TOP = 62
MARGIN_BOTTOM = 54
CONTENT_W = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT

BASE = '/Users/ahmadduais/Desktop/Acquisitions/1st-Call-Recruitment/Investor DD Pack'
INPUT_MD = f'{BASE}/1CR_Investor_DD_Briefing.md'
OUTPUT_PDF = f'{BASE}/1CR_Investor_DD_Briefing.pdf'

PROJECT = '1st Call Recruitment — DD Briefing'
FOOTER_L = 'STRICTLY CONFIDENTIAL — Investor Due-Diligence Briefing'
FOOTER_DATE = 'July 2026 — Deal Team Only'

TOC_ITEMS = [
    '1. Purpose &amp; Contents of This Pack',
    '2. The Target &amp; The Parties',
    '3. Deal Timeline &amp; Communications Log',
    '4. Where the Deal Stands (9 July 2026)',
    '5. The Business — What We Know',
    '6. Financial Findings',
    '7. Vendor IM — Credibility Findings',
    '8. Proposed Acquisition Structure &amp; Conditions',
    '9. Key Risks (ranked)',
    '10. Open DD Items — Suggested Workplan',
    '11. Confidentiality &amp; Basis of Preparation',
]


def create_styles():
    styles = {}
    styles['body'] = ParagraphStyle('Body', fontName='Helvetica', fontSize=10, leading=14,
                                    textColor=DARK_GREY, alignment=TA_JUSTIFY, spaceAfter=6)
    styles['h1'] = ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=18, leading=22,
                                  textColor=NAVY, spaceBefore=24, spaceAfter=12)
    styles['h2'] = ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=14, leading=18,
                                  textColor=NAVY, spaceBefore=18, spaceAfter=8)
    styles['h3'] = ParagraphStyle('H3', fontName='Helvetica-Bold', fontSize=11, leading=15,
                                  textColor=NAVY, spaceBefore=12, spaceAfter=6)
    styles['bullet'] = ParagraphStyle('Bullet', fontName='Helvetica', fontSize=10, leading=14,
                                      textColor=DARK_GREY, leftIndent=18, bulletIndent=6,
                                      spaceAfter=3, alignment=TA_LEFT)
    styles['numbered'] = ParagraphStyle('Numbered', fontName='Helvetica', fontSize=10, leading=14,
                                        textColor=DARK_GREY, leftIndent=18, bulletIndent=0,
                                        spaceAfter=3, alignment=TA_LEFT)
    styles['blockquote'] = ParagraphStyle('BlockQuote', fontName='Helvetica-Oblique', fontSize=9.5,
                                          leading=13, textColor=HexColor('#555555'), leftIndent=18,
                                          rightIndent=18, spaceBefore=6, spaceAfter=6)
    styles['toc_entry'] = ParagraphStyle('TOCEntry', fontName='Helvetica', fontSize=11, leading=16,
                                         textColor=NAVY, leftIndent=12, spaceAfter=4)
    styles['table_header'] = ParagraphStyle('TableHeader', fontName='Helvetica-Bold', fontSize=8.5,
                                            leading=11, textColor=white, alignment=TA_LEFT)
    styles['table_cell'] = ParagraphStyle('TableCell', fontName='Helvetica', fontSize=8.5,
                                          leading=11, textColor=DARK_GREY, alignment=TA_LEFT)
    styles['table_cell_bold'] = ParagraphStyle('TableCellBold', fontName='Helvetica-Bold',
                                               fontSize=8.5, leading=11, textColor=DARK_GREY,
                                               alignment=TA_LEFT)
    return styles


def header_footer(canvas, doc):
    canvas.saveState()
    page_num = doc.page
    if page_num > 1:
        canvas.setStrokeColor(GOLD)
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN_LEFT, PAGE_H - 42, PAGE_W - MARGIN_RIGHT, PAGE_H - 42)
        canvas.setFont('Helvetica', 7.5)
        canvas.setFillColor(HexColor('#999999'))
        canvas.drawString(MARGIN_LEFT, PAGE_H - 38, FOOTER_L)
        canvas.drawRightString(PAGE_W - MARGIN_RIGHT, PAGE_H - 38, PROJECT)
        canvas.setStrokeColor(MID_GREY)
        canvas.setLineWidth(0.3)
        canvas.line(MARGIN_LEFT, 36, PAGE_W - MARGIN_RIGHT, 36)
        canvas.setFont('Helvetica', 7.5)
        canvas.setFillColor(HexColor('#999999'))
        canvas.drawString(MARGIN_LEFT, 24, FOOTER_DATE)
        canvas.drawRightString(PAGE_W - MARGIN_RIGHT, 24, f'Page {page_num}')
    canvas.restoreState()


def build_title_page(styles):
    e = []
    e.append(Spacer(1, 110))
    e.append(Paragraph('STRICTLY CONFIDENTIAL', ParagraphStyle(
        'ConfBanner', fontName='Helvetica-Bold', fontSize=10, leading=12,
        textColor=RED_ACCENT, alignment=TA_CENTER, spaceAfter=38)))
    e.append(Paragraph('1st Call Recruitment', ParagraphStyle(
        'Title', fontName='Helvetica-Bold', fontSize=30, leading=36,
        textColor=NAVY, alignment=TA_CENTER, spaceAfter=8)))
    e.append(Paragraph('Investor Due-Diligence Briefing &amp; Deal File', ParagraphStyle(
        'Subtitle', fontName='Helvetica-Bold', fontSize=20, leading=26,
        textColor=GOLD, alignment=TA_CENTER, spaceAfter=6)))
    e.append(Paragraph('JCR 2006 Limited — going-concern business &amp; asset acquisition', ParagraphStyle(
        'SubSub', fontName='Helvetica', fontSize=13, leading=18,
        textColor=HexColor('#666666'), alignment=TA_CENTER, spaceAfter=28)))
    e.append(HRFlowable(width='40%', thickness=2, color=GOLD, spaceAfter=28, hAlign='CENTER'))
    e.append(Paragraph('The complete deal record — communications, source documents and findings —<br/>'
                       'prepared so an incoming JV investor can conduct independent due diligence.',
                       ParagraphStyle('DetailTitle', fontName='Helvetica', fontSize=12, leading=17,
                                      textColor=DARK_GREY, alignment=TA_CENTER, spaceAfter=40)))
    for label, value in [
        ('Prepared for', 'Prospective joint-venture investor'),
        ('Prepared by', 'Ahmad Duais (Sponsor)'),
        ('Date', 'July 2026'),
        ('Classification', 'Strictly Confidential — deal team and advisers only'),
    ]:
        e.append(Paragraph(f'<b>{label}:</b>  {value}', ParagraphStyle(
            'Detail', fontName='Helvetica', fontSize=11, leading=16,
            textColor=DARK_GREY, alignment=TA_CENTER, spaceAfter=4)))
    e.append(Spacer(1, 30))
    e.append(Paragraph(
        'Vendor-sourced material in this pack was supplied unaudited under ABC Business Sales’ '
        '“passing over information” terms. The Sponsor’s analysis is provided in good faith '
        'without warranty. Please do not contact the vendor, broker, staff, clients or banks directly.',
        ParagraphStyle('Foot', fontName='Helvetica-Oblique', fontSize=8.5, leading=12,
                       textColor=HexColor('#888888'), alignment=TA_CENTER)))
    e.append(PageBreak())
    return e


def build_toc(styles):
    e = []
    e.append(Paragraph('CONTENTS', styles['h1']))
    e.append(HRFlowable(width='100%', thickness=1, color=GOLD, spaceAfter=16))
    for item in TOC_ITEMS:
        e.append(Paragraph(item, styles['toc_entry']))
    return e


def format_inline(text):
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'(?<!\w)\*([^*]+?)\*(?!\w)', r'<i>\1</i>', text)
    text = re.sub(r'`(.+?)`', r'<font face="Courier" size="9">\1</font>', text)
    return text


def column_widths(rows, num_cols):
    """Proportional widths from the longest cell text per column, clamped."""
    maxima = []
    for c in range(num_cols):
        longest = max((len(re.sub(r'\*\*', '', r[c])) for r in rows if c < len(r)), default=1)
        maxima.append(max(longest, 4))
    capped = [min(m, 160) for m in maxima]
    total = sum(capped)
    fracs = [m / total for m in capped]
    floor = 0.42 / num_cols  # no column narrower than ~42% of an even share
    fracs = [max(f, floor) for f in fracs]
    scale = sum(fracs)
    return [CONTENT_W * f / scale for f in fracs]


def parse_table(lines, styles):
    if len(lines) < 2:
        return None
    rows = []
    for line in lines:
        line = line.strip().strip('|')
        rows.append([c.strip() for c in line.split('|')])
    rows = [r for r in rows if not all(re.match(r'^[-:]+$', c) for c in r)]
    if not rows:
        return None
    header, data_rows = rows[0], rows[1:]
    num_cols = len(header)
    table_data = [[Paragraph(format_inline(c), styles['table_header']) for c in header]]
    for row in data_rows:
        cells = []
        for cell in row[:num_cols]:
            t = format_inline(cell)
            is_bold = t.startswith('<b>') or cell.strip().startswith('**')
            cells.append(Paragraph(t, styles['table_cell_bold'] if is_bold else styles['table_cell']))
        while len(cells) < num_cols:
            cells.append(Paragraph('', styles['table_cell']))
        table_data.append(cells)
    col_widths = column_widths(rows, num_cols)
    table = Table(table_data, colWidths=col_widths, repeatRows=1)
    cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.3, MID_GREY),
        ('LINEBELOW', (0, 0), (-1, 0), 1, GOLD),
    ]
    for idx in range(1, len(table_data)):
        if idx % 2 == 0:
            cmds.append(('BACKGROUND', (0, idx), (-1, idx), LIGHT_GREY))
    table.setStyle(TableStyle(cmds))
    return table


def parse_markdown(md_text, styles):
    elements = []
    lines = md_text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped == '---' or not stripped:
            i += 1
            continue
        if re.match(r'^# ', stripped):
            elements.append(PageBreak())
            elements.append(Paragraph(format_inline(stripped[2:]), styles['h1']))
            elements.append(HRFlowable(width='100%', thickness=1, color=GOLD, spaceAfter=12))
            i += 1
            continue
        if stripped.startswith('## '):
            elements.append(Spacer(1, 8))
            elements.append(Paragraph(format_inline(stripped[3:]), styles['h2']))
            i += 1
            continue
        if stripped.startswith('### '):
            elements.append(Paragraph(format_inline(stripped[4:]), styles['h3']))
            i += 1
            continue
        if stripped.startswith('> '):
            elements.append(Paragraph(format_inline(stripped[2:]), styles['blockquote']))
            i += 1
            continue
        if '|' in stripped and i + 1 < len(lines) and '|' in lines[i + 1].strip():
            tlines = []
            while i < len(lines) and '|' in lines[i].strip():
                tlines.append(lines[i]); i += 1
            tbl = parse_table(tlines, styles)
            if tbl:
                elements.append(Spacer(1, 4)); elements.append(tbl); elements.append(Spacer(1, 6))
            continue
        m = re.match(r'^(\d+)\.\s+(.+)', stripped)
        if m:
            elements.append(Paragraph(f'<b>{m.group(1)}.</b>  {format_inline(m.group(2))}', styles['numbered']))
            i += 1
            continue
        if stripped.startswith('- '):
            elements.append(Paragraph(f'•  {format_inline(stripped[2:])}', styles['bullet']))
            i += 1
            continue
        if stripped.startswith('*') and stripped.endswith('*') and len(stripped) > 2 and not stripped.startswith('**'):
            elements.append(Paragraph(format_inline(stripped), styles['blockquote']))
            i += 1
            continue
        elements.append(Paragraph(format_inline(stripped), styles['body']))
        i += 1
    return elements


def main():
    with open(INPUT_MD) as f:
        md_text = f.read()
    styles = create_styles()
    doc = SimpleDocTemplate(
        OUTPUT_PDF, pagesize=A4,
        leftMargin=MARGIN_LEFT, rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM,
        title='1st Call Recruitment — Investor DD Briefing', author='Confidential',
    )
    elements = []
    elements.extend(build_title_page(styles))
    elements.extend(build_toc(styles))
    elements.extend(parse_markdown(md_text, styles))
    doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f'PDF generated: {OUTPUT_PDF}')


if __name__ == '__main__':
    main()
