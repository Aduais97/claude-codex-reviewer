#!/usr/bin/env python3
"""
ASG x Liberty Security | Security Services Supply and Restraint Agreement (editable Word).
Converts the ETR-hardened agreement markdown into a lawyer-editable .docx.
Traditional legal layout: numbered clause headings, justified body, rates table,
signature blocks. No em-dashes anywhere (Ahmad's client-doc rule).

Usage:
    python3 build_liberty_agreement_docx.py <agreement.md> <output.docx>
"""
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor

BLACK = RGBColor(0x00, 0x00, 0x00)
DARK = RGBColor(0x11, 0x18, 0x27)
FONT = 'Georgia'
HEAD_FONT = 'Arial'


def runs(p, text, size=10, bold_all=False, color=DARK, font=FONT):
    for chunk in re.split(r'(\*\*.*?\*\*)', text, flags=re.S):
        if not chunk:
            continue
        bold = chunk.startswith('**')
        seg = chunk[2:-2] if bold else chunk
        r = p.add_run(seg)
        r.bold = bold or bold_all
        r.font.name = font
        r.font.size = Pt(size)
        r.font.color.rgb = color
    return p


def body(doc, text, size=10, space_after=6, indent=0, justify=True):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.18
    if indent:
        pf.left_indent = Mm(indent)
    if justify:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    return runs(p, text, size=size)


def heading(doc, text, size=12, space_before=12, space_after=6):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.keep_with_next = True
    runs(p, text, size=size, bold_all=True, color=BLACK, font=HEAD_FONT)
    return p


def hrule(doc):
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:color'), '94A3B8')
    pBdr.append(bottom)
    pPr.append(pBdr)
    p.paragraph_format.space_after = Pt(8)


def add_table(doc, rows):
    table = doc.add_table(rows=0, cols=len(rows[0]))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(rows):
        cells = table.add_row().cells
        for j, cell_text in enumerate(row):
            cell = cells[j]
            cell.text = ''
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            runs(p, cell_text, size=9.5, bold_all=(i == 0),
                 font=HEAD_FONT if i == 0 else FONT)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


def build(md_path: Path, out_path: Path):
    text = md_path.read_text()
    assert '—' not in text and '–' not in text, 'em/en dash found in source markdown'

    doc = Document()
    for section in doc.sections:
        section.page_width, section.page_height = Mm(210), Mm(297)
        section.left_margin = section.right_margin = Mm(22)
        section.top_margin, section.bottom_margin = Mm(20), Mm(20)

    lines = text.split('\n')
    i, table_buf = 0, []

    def flush_table():
        nonlocal table_buf
        if table_buf:
            add_table(doc, table_buf)
            table_buf = []

    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()

        if stripped.startswith('|') and stripped.endswith('|'):
            cells = [c.strip() for c in stripped.strip('|').split('|')]
            if not all(re.fullmatch(r':?-+:?', c) for c in cells):
                table_buf.append(cells)
            i += 1
            continue
        flush_table()

        if not stripped:
            i += 1
            continue
        if stripped == '---':
            doc.add_page_break()
        elif stripped.startswith('# '):
            p = heading(doc, stripped[2:], size=15, space_before=0, space_after=2)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            hrule(doc)
        elif stripped.startswith('### '):
            heading(doc, stripped[4:], size=10.5, space_before=10)
        elif stripped.startswith('## '):
            heading(doc, stripped[3:], size=11.5, space_before=14)
        elif re.match(r'^\d+\.\d+ ', stripped) or re.match(r'^[A-Z]\. ', stripped):
            body(doc, stripped, indent=0)
        elif re.match(r'^\([a-z]\)', stripped) or re.match(r'^\([ivx]+\)', stripped):
            body(doc, stripped, indent=8)
        elif re.match(r'^\d+\. ', stripped) and 'SCHEDULE' in '\n'.join(lines[max(0, i - 30):i]).upper():
            body(doc, stripped, indent=5, justify=False)
        elif stripped.startswith('Signature:'):
            body(doc, stripped, space_after=14, justify=False)
        else:
            body(doc, stripped)
        i += 1
    flush_table()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out_path)
    print(f'Saved: {out_path}')


if __name__ == '__main__':
    build(Path(sys.argv[1]), Path(sys.argv[2]))
