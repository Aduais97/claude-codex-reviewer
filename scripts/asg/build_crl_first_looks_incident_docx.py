#!/usr/bin/env python3
"""
Word (.docx) build of the AT-facing CRL First Looks incident report.
Consumes the same hardened spec as the PDF generator so content is identical.

Usage:
    python3 build_crl_first_looks_incident_docx.py <spec.json> <out.docx>
"""
import json
import sys

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Mm

NAVY = RGBColor(0x14, 0x28, 0x4B)
NAVY_SOFT = RGBColor(0x2A, 0x3E, 0x63)
GOLD = RGBColor(0xB8, 0x86, 0x0B)
INK = RGBColor(0x1F, 0x27, 0x33)
GREY = RGBColor(0x5B, 0x64, 0x72)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
NAVY_HEX = '14284B'
ROW_HEX = 'F4F6F9'
LABEL_HEX = 'FBFBF8'


def shade(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_fill)
    tcPr.append(shd)


def set_cell_margins(cell, top=60, bottom=60, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    m = OxmlElement('w:tcMar')
    for tag, val in (('top', top), ('bottom', bottom), ('start', left), ('end', right)):
        e = OxmlElement(f'w:{tag}')
        e.set(qn('w:w'), str(val))
        e.set(qn('w:type'), 'dxa')
        m.append(e)
    tcPr.append(m)


def _set_borders(tbl, color='D8DCE3', sz=4, which=('top', 'bottom', 'insideH')):
    tblPr = tbl._tbl.tblPr
    borders = OxmlElement('w:tblBorders')
    for edge in which:
        e = OxmlElement(f'w:{edge}')
        e.set(qn('w:val'), 'single')
        e.set(qn('w:sz'), str(sz))
        e.set(qn('w:space'), '0')
        e.set(qn('w:color'), color)
        borders.append(e)
    tblPr.append(borders)


def run(p, text, *, size=10, color=INK, bold=False, font='Calibri'):
    r = p.add_run((text or ''))
    r.font.name = font
    r.font.size = Pt(size)
    r.font.color.rgb = color
    r.bold = bold
    return r


def cell_text(cell, text, *, size=9, color=INK, bold=False):
    cell.paragraphs[0].text = ''
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    run(p, text, size=size, color=color, bold=bold)
    return p


def heading(doc, text, *, size=13, color=NAVY, before=14, after=5, bold=True):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.keep_with_next = True
    run(p, text, size=size, color=color, bold=bold)
    return p


def body(doc, text, *, size=10, color=INK, after=8):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 1.18
    run(p, text, size=size, color=color)
    return p


def build(spec, out_path):
    doc = Document()
    # base style
    normal = doc.styles['Normal']
    normal.font.name = 'Calibri'
    normal.font.size = Pt(10)
    normal.font.color.rgb = INK
    sec = doc.sections[0]
    sec.top_margin = Mm(18)
    sec.bottom_margin = Mm(18)
    sec.left_margin = Mm(18)
    sec.right_margin = Mm(18)
    content_w = sec.page_width - sec.left_margin - sec.right_margin

    # ---- kicker + title
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    run(p, 'ASG SECURITY  ·  EVENT OPERATIONS', size=9, color=GOLD, bold=True)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    run(p, spec.get('reportTitle', ''), size=19, color=NAVY, bold=True)
    if spec.get('reportSubtitle'):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(8)
        run(p, spec['reportSubtitle'], size=11, color=GREY)

    # ---- metadata table (borderless key/value)
    meta = [
        ('Prepared for', spec.get('preparedFor', '')),
        ('Prepared by', spec.get('preparedBy', '')),
        ('Report reference', spec.get('reportRef', '')),
        ('Issue date', spec.get('issueDate', '')),
        ('Classification', spec.get('classificationLine', '')),
        ('Contact', spec.get('contactLine', '')),
    ]
    meta = [(k, v) for k, v in meta if v]
    t = doc.add_table(rows=len(meta), cols=2)
    t.allow_autofit = False
    t.columns[0].width = Mm(38)
    t.columns[1].width = content_w - Mm(38)
    for i, (k, v) in enumerate(meta):
        t.rows[i].cells[0].width = Mm(38)
        t.rows[i].cells[1].width = content_w - Mm(38)
        cell_text(t.rows[i].cells[0], k, size=8.5, color=GREY, bold=True)
        cell_text(t.rows[i].cells[1], v, size=9, color=INK)
        for c in t.rows[i].cells:
            set_cell_margins(c, top=40, bottom=40, left=0, right=80)
    _set_borders(t, which=('insideH',))

    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    body(doc, spec.get('introParagraph', ''))

    # ---- events at a glance
    heading(doc, 'Events at a glance')
    rows = spec.get('eventsAtAGlance', [])
    t = doc.add_table(rows=len(rows) + 1, cols=3)
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.allow_autofit = False
    widths = [Mm(28), Mm(52), content_w - Mm(80)]
    hdr = t.rows[0].cells
    for j, htxt in enumerate(['Date', 'Location', 'Main incidents']):
        cell_text(hdr[j], htxt, size=9, color=WHITE, bold=True)
        shade(hdr[j], NAVY_HEX)
    for i, r in enumerate(rows, start=1):
        vals = [r.get('date', ''), r.get('location', ''), r.get('mainIncidents', '')]
        for j, v in enumerate(vals):
            cell_text(t.rows[i].cells[j], v, size=9)
            if i % 2 == 0:
                shade(t.rows[i].cells[j], ROW_HEX)
    for r_ in t.rows:
        for j, c in enumerate(r_.cells):
            c.width = widths[j]
            set_cell_margins(c)
    _set_borders(t, which=('top', 'bottom', 'insideH'))

    # ---- notifiable statement
    if spec.get('notifiableStatement'):
        heading(doc, 'Notifiable-event determination (HSWA 2015)')
        body(doc, spec['notifiableStatement'])

    # ---- incident detail
    heading(doc, 'Incident detail by event')
    field_order = [
        ('Classification', 'classification'),
        ('Time', 'time'),
        ('Person affected', 'personAffected'),
        ('What happened', 'description'),
        ('Immediate response', 'immediateResponse'),
        ('Notifications / attendance', 'notifications'),
        ('Outcome', 'outcome'),
        ('Harm outcome', 'harmOutcome'),
    ]
    for ev in spec.get('events', []):
        heading(doc, ev.get('heading', ''), size=11, color=NAVY_SOFT, before=10, after=3)
        for inc in ev.get('incidents', []):
            ref = inc.get('ref', '')
            ttl = inc.get('title', '')
            heading(doc, f"Incident {ref} — {ttl}" if ref else f"Incident — {ttl}",
                    size=10.5, color=NAVY, before=8, after=3)
            fields = []
            for label, key in field_order:
                val = inc.get(key)
                if key == 'time' and not val:
                    val = 'Not recorded (available from radio/incident log on request)'
                if val:
                    fields.append((label, val, None))
            nf = inc.get('notifiableUnderHswa')
            if nf is not None:
                nf_word = 'No' if nf is False else 'Yes'
                fields.append(('Notifiable event (HSWA 2015)', inc.get('notifiableRationale', ''), nf_word))

            it = doc.add_table(rows=len(fields), cols=2)
            it.allow_autofit = False
            lw = Mm(46)
            for i, (label, val, nf_word) in enumerate(fields):
                lc, vc = it.rows[i].cells
                lc.width = lw
                vc.width = content_w - lw
                cell_text(lc, label, size=9, color=NAVY_SOFT, bold=True)
                shade(lc, LABEL_HEX)
                vc.paragraphs[0].text = ''
                vp = vc.paragraphs[0]
                vp.paragraph_format.space_after = Pt(0)
                vp.paragraph_format.line_spacing = 1.12
                if nf_word:
                    run(vp, nf_word + '. ', size=9, color=NAVY, bold=True)
                run(vp, val, size=9, color=INK)
                for c in (lc, vc):
                    set_cell_margins(c)
            _set_borders(it, which=('top', 'bottom', 'insideH'))
            doc.add_paragraph().paragraph_format.space_after = Pt(3)

    # ---- closing sections
    if spec.get('proactiveMonitoringNote'):
        heading(doc, 'Proactive monitoring')
        body(doc, spec['proactiveMonitoringNote'])
    if spec.get('overallSummary'):
        heading(doc, 'Overall operational summary')
        body(doc, spec['overallSummary'])
    if spec.get('workerWelfareNote'):
        heading(doc, 'Worker health, safety & welfare')
        body(doc, spec['workerWelfareNote'])
    if spec.get('sharedDutiesNote'):
        heading(doc, 'Overlapping duties (ASG & Auckland Transport)')
        body(doc, spec['sharedDutiesNote'])

    # ---- sign-off
    so = spec.get('signOff', {})
    if so:
        doc.add_paragraph().paragraph_format.space_after = Pt(6)
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        run(p, so.get('name', ''), size=10, color=NAVY, bold=True)
        for line in [so.get('title'), so.get('org'), so.get('contact')]:
            if line:
                pp = doc.add_paragraph()
                pp.paragraph_format.space_after = Pt(0)
                run(pp, line, size=9.5, color=INK)

    # ---- footer
    footer = sec.footer
    fp = footer.paragraphs[0]
    fp.text = ''
    fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run(fp, f"Absolute Security Group  ·  {spec.get('classificationLine','')}",
        size=7.5, color=GREY)

    doc.save(out_path)
    print(f"Wrote {out_path}")


if __name__ == '__main__':
    spec_path, out_path = sys.argv[1], sys.argv[2]
    with open(spec_path) as f:
        spec = json.load(f)
    build(spec, out_path)
