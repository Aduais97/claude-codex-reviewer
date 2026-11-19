#!/usr/bin/env python3
"""
Build the AT-facing CRL First Looks Event Security Incident Report PDF.

Usage:
    python3 build_crl_first_looks_incident_report.py <spec.json> <out.pdf>

Consumes the hardened report spec produced by the ETR agentic workflow
(crl_first_looks_wf.js -> finalReport). Design per Ahmad's PDF standards:
navy + gold, ReportLab, no decorative tinted call-out boxes, clean data
tables, min 8pt / 10pt body, generous margins.
"""
import json
import re
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table,
    TableStyle, KeepTogether, HRFlowable,
)

# ---- palette -------------------------------------------------------------
NAVY = colors.HexColor(0x14284B)
NAVY_SOFT = colors.HexColor(0x2A3E63)
GOLD = colors.HexColor(0xB8860B)
INK = colors.HexColor(0x1F2733)
GREY = colors.HexColor(0x5B6472)
HAIR = colors.HexColor(0xD8DCE3)
ROW = colors.HexColor(0xF4F6F9)
WHITE = colors.white

PAGE_W, PAGE_H = A4
LM = RM = 46
TM = 54
BM = 46


def styles():
    ss = getSampleStyleSheet()
    s = {}
    s['kicker'] = ParagraphStyle('kicker', parent=ss['Normal'], fontName='Helvetica-Bold',
                                 fontSize=9, textColor=GOLD, spaceAfter=4, leading=11,
                                 tracking=1)
    s['title'] = ParagraphStyle('title', parent=ss['Normal'], fontName='Helvetica-Bold',
                                fontSize=21, textColor=NAVY, leading=25, spaceAfter=4)
    s['subtitle'] = ParagraphStyle('subtitle', parent=ss['Normal'], fontName='Helvetica',
                                   fontSize=11, textColor=GREY, leading=15, spaceAfter=10)
    s['h2'] = ParagraphStyle('h2', parent=ss['Normal'], fontName='Helvetica-Bold',
                            fontSize=13, textColor=NAVY, leading=16, spaceBefore=14, spaceAfter=6)
    s['h3'] = ParagraphStyle('h3', parent=ss['Normal'], fontName='Helvetica-Bold',
                            fontSize=10.5, textColor=NAVY_SOFT, leading=13, spaceBefore=8, spaceAfter=3)
    s['body'] = ParagraphStyle('body', parent=ss['Normal'], fontName='Helvetica',
                              fontSize=10, textColor=INK, leading=14.5, spaceAfter=7, alignment=TA_LEFT)
    s['lead'] = ParagraphStyle('lead', parent=s['body'], fontName='Helvetica-Bold', textColor=NAVY,
                             spaceAfter=2)
    s['cell'] = ParagraphStyle('cell', parent=ss['Normal'], fontName='Helvetica',
                             fontSize=9, textColor=INK, leading=12.5)
    s['cellb'] = ParagraphStyle('cellb', parent=s['cell'], fontName='Helvetica-Bold', textColor=NAVY_SOFT)
    s['cellh'] = ParagraphStyle('cellh', parent=s['cell'], fontName='Helvetica-Bold', textColor=WHITE)
    s['kv_k'] = ParagraphStyle('kv_k', parent=s['cell'], fontName='Helvetica-Bold', textColor=GREY, fontSize=8.5)
    s['kv_v'] = ParagraphStyle('kv_v', parent=s['cell'], fontName='Helvetica', textColor=INK, fontSize=9)
    s['note'] = ParagraphStyle('note', parent=s['body'], fontSize=9, textColor=GREY, leading=12.5)
    s['sign'] = ParagraphStyle('sign', parent=s['body'], fontSize=9.5, leading=13.5)
    return s


S = styles()


_AMP = re.compile(r'&(?!amp;|lt;|gt;|quot;|apos;|#\d+;|#x[0-9A-Fa-f]+;)')


def para(txt, st):
    txt = _AMP.sub('&amp;', (txt or ''))
    return Paragraph(txt.replace('\n', '<br/>'), st)


def rule(color=HAIR, w=0.8, space_before=2, space_after=8):
    return HRFlowable(width='100%', thickness=w, color=color,
                      spaceBefore=space_before, spaceAfter=space_after)


def meta_table(spec):
    rows = [
        ('Prepared for', spec.get('preparedFor', 'Auckland Transport')),
        ('Prepared by', spec.get('preparedBy', 'Absolute Security Group (ASG)')),
        ('Report reference', spec.get('reportRef', '')),
        ('Issue date', spec.get('issueDate', '')),
        ('Classification', spec.get('classificationLine', '')),
        ('Contact', spec.get('contactLine', '')),
    ]
    data = [[para(k, S['kv_k']), para(v, S['kv_v'])] for k, v in rows if v]
    t = Table(data, colWidths=[95, PAGE_W - LM - RM - 95])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('LINEBELOW', (0, 0), (-1, -2), 0.4, HAIR),
    ]))
    return t


def glance_table(spec):
    header = ['Date', 'Location', 'Main incidents']
    data = [[para(h, S['cellh']) for h in header]]
    for r in spec.get('eventsAtAGlance', []):
        data.append([para(r.get('date', ''), S['cell']),
                     para(r.get('location', ''), S['cell']),
                     para(r.get('mainIncidents', ''), S['cell'])])
    t = Table(data, colWidths=[95, 175, PAGE_W - LM - RM - 270], repeatRows=1)
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, -1), 0.4, HAIR),
        ('LINEAFTER', (0, 0), (-2, -1), 0.4, colors.HexColor(0xE9EDF2)),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(('BACKGROUND', (0, i), (-1, i), ROW))
    t.setStyle(TableStyle(style))
    return t


def incident_block(inc):
    """Clean two-column data table per incident (allowed: data/key-value tables)."""
    ref = inc.get('ref', '')
    title = inc.get('title', '')
    head = f"Incident {ref} — {title}" if ref else f"Incident — {title}"
    fields = [
        ('Classification', inc.get('classification')),
        ('Time', inc.get('time') or 'Not recorded (available from radio/incident log on request)'),
        ('Person affected', inc.get('personAffected')),
        ('What happened', inc.get('description')),
        ('Immediate response', inc.get('immediateResponse')),
        ('Notifications / attendance', inc.get('notifications')),
        ('Outcome', inc.get('outcome')),
        ('Harm outcome', inc.get('harmOutcome')),
    ]
    nf = inc.get('notifiableUnderHswa')
    nf_txt = ('No' if nf is False else ('Yes' if nf is True else ''))
    rationale = inc.get('notifiableRationale', '')
    if nf_txt:
        fields.append(('Notifiable event (HSWA 2015)', f"<b>{nf_txt}.</b> {rationale}"))

    data = [[para(k, S['cellb']), para(v, S['cell'])] for k, v in fields if v]
    t = Table(data, colWidths=[130, PAGE_W - LM - RM - 130])
    style = [
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, -2), 0.4, HAIR),
        ('LINEBEFORE', (0, 0), (0, -1), 2, GOLD),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor(0xFBFBF8)),
    ]
    t.setStyle(TableStyle(style))
    return KeepTogether([para(head, S['h3']), Spacer(1, 2), t, Spacer(1, 6)])


def build(spec, out_path):
    def on_page(canvas, doc):
        canvas.saveState()
        # top gold hairline
        canvas.setStrokeColor(GOLD)
        canvas.setLineWidth(1.4)
        canvas.line(LM, PAGE_H - 34, PAGE_W - RM, PAGE_H - 34)
        # footer
        canvas.setFont('Helvetica', 7.5)
        canvas.setFillColor(GREY)
        foot = spec.get('classificationLine') or 'In confidence — Auckland Transport'
        canvas.drawString(LM, 26, f"Absolute Security Group  ·  {foot}")
        canvas.drawRightString(PAGE_W - RM, 26, f"Page {doc.page}")
        canvas.setStrokeColor(HAIR)
        canvas.setLineWidth(0.4)
        canvas.line(LM, 36, PAGE_W - RM, 36)
        canvas.restoreState()

    frame = Frame(LM, BM, PAGE_W - LM - RM, PAGE_H - TM - BM, id='main',
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc = BaseDocTemplate(out_path, pagesize=A4, leftMargin=LM, rightMargin=RM,
                          topMargin=TM, bottomMargin=BM, title=spec.get('reportTitle', ''),
                          author='Absolute Security Group')
    doc.addPageTemplates([PageTemplate(id='all', frames=[frame], onPage=on_page)])

    E = []
    E.append(para('ASG SECURITY  ·  EVENT OPERATIONS', S['kicker']))
    E.append(para(spec.get('reportTitle', 'CRL First Looks — Event Security Incident Report'), S['title']))
    if spec.get('reportSubtitle'):
        E.append(para(spec['reportSubtitle'], S['subtitle']))
    E.append(rule(GOLD, 1.0, 2, 10))
    E.append(meta_table(spec))
    E.append(Spacer(1, 12))
    E.append(para(spec.get('introParagraph', ''), S['body']))

    # events at a glance
    E.append(para('Events at a glance', S['h2']))
    E.append(glance_table(spec))
    E.append(Spacer(1, 6))

    # notifiable-event statement (bold lead-in + plain text; NOT a tinted box)
    if spec.get('notifiableStatement'):
        E.append(para('Notifiable-event determination (HSWA 2015)', S['h2']))
        E.append(para(spec['notifiableStatement'], S['body']))

    # per-event detail
    E.append(para('Incident detail by event', S['h2']))
    for ev in spec.get('events', []):
        E.append(para(ev.get('heading', ''), S['h3']))
        E.append(rule(HAIR, 0.6, 1, 5))
        for inc in ev.get('incidents', []):
            E.append(incident_block(inc))

    # proactive monitoring
    if spec.get('proactiveMonitoringNote'):
        E.append(para('Proactive monitoring', S['h2']))
        E.append(para(spec['proactiveMonitoringNote'], S['body']))

    # overall summary
    if spec.get('overallSummary'):
        E.append(para('Overall operational summary', S['h2']))
        E.append(para(spec['overallSummary'], S['body']))

    if spec.get('workerWelfareNote'):
        E.append(para('Worker health, safety &amp; welfare', S['h2']))
        E.append(para(spec['workerWelfareNote'], S['body']))

    if spec.get('sharedDutiesNote'):
        E.append(para('Overlapping duties (ASG &amp; Auckland Transport)', S['h2']))
        E.append(para(spec['sharedDutiesNote'], S['body']))

    # sign-off
    so = spec.get('signOff', {})
    if so:
        E.append(Spacer(1, 10))
        E.append(rule(HAIR, 0.6, 2, 8))
        block = "<b>%s</b>" % so.get('name', '')
        if so.get('title'):
            block += "<br/>%s" % so['title']
        block += "<br/>%s" % so.get('org', 'Absolute Security Group')
        if so.get('contact'):
            block += "<br/>%s" % so['contact']
        E.append(para(block, S['sign']))

    doc.build(E)
    print(f"Wrote {out_path}")


if __name__ == '__main__':
    spec_path, out_path = sys.argv[1], sys.argv[2]
    with open(spec_path) as f:
        spec = json.load(f)
    build(spec, out_path)
