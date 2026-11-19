#!/usr/bin/env python3
"""Generate the Oaks Wellington cover letter as a .docx (editable)."""

import sys
sys.path.insert(0, '/Users/ahmadduais/Desktop/Claude/.venv/lib/python3.14/site-packages')

import os
from datetime import datetime

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = '/Users/ahmadduais/Desktop/Oaks Wellington Tender/Oaks_Wellington_Cover_Letter.docx'

NAVY = RGBColor(0x1B, 0x2A, 0x4A)
GOLD = RGBColor(0xD4, 0xA8, 0x43)
TEXT_DARK = RGBColor(0x1A, 0x1A, 0x2E)
TEXT_MED  = RGBColor(0x4A, 0x4A, 0x5A)


def set_margins(doc, top=2.2, bottom=2.0, left=2.0, right=2.0):
    for s in doc.sections:
        s.top_margin = Cm(top)
        s.bottom_margin = Cm(bottom)
        s.left_margin = Cm(left)
        s.right_margin = Cm(right)


def add_run(p, text, *, bold=False, italic=False, size=11, color=TEXT_DARK,
            font='Calibri'):
    r = p.add_run(text)
    r.bold = bold
    r.italic = italic
    r.font.size = Pt(size)
    r.font.color.rgb = color
    r.font.name = font
    return r


def add_paragraph(doc, *runs, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6,
                  space_before=0):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.line_spacing = 1.25
    for run in runs:
        add_run(p, **run)
    return p


def add_bullet(doc, runs):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.2
    for run in runs:
        add_run(p, **run)
    return p


def add_heading_band(doc):
    """ASG-style header band: navy bold name + gold underline."""
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    add_run(p, 'ASG GROUP', bold=True, size=18, color=NAVY)
    p2 = doc.add_paragraph()
    p2.paragraph_format.space_after = Pt(10)
    add_run(p2, 'Absolute Security Group Limited  ·  Auckland, New Zealand',
            size=9, color=TEXT_MED, italic=True)
    # Gold horizontal rule
    p3 = doc.add_paragraph()
    p3.paragraph_format.space_after = Pt(14)
    pPr = p3._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '12')  # eighths of a point — 12 = 1.5pt
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), 'D4A843')
    pBdr.append(bottom)
    pPr.append(pBdr)


def main():
    doc = Document()
    set_margins(doc)

    # Default font
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(11)

    add_heading_band(doc)

    # Date
    today = datetime.now().strftime('%-d %B %Y')
    add_paragraph(doc, {'text': today, 'size': 10, 'color': TEXT_MED})

    # Recipient
    add_paragraph(doc, {'text': 'Zafer', 'size': 10, 'bold': True, 'color': TEXT_DARK})
    add_paragraph(doc, {'text': 'Oaks Wellington, Auckland CBD', 'size': 10, 'color': TEXT_DARK},
                  space_after=2)
    add_paragraph(doc, {'text': 'Auckland, New Zealand', 'size': 10, 'color': TEXT_DARK},
                  space_after=14)

    # Subject line
    add_paragraph(doc,
        {'text': 'Re: Senior Security Cover — Oaks Wellington',
         'bold': True, 'size': 12, 'color': NAVY},
        space_after=10)

    # Body
    add_paragraph(doc, {'text': 'Hi Zafer,'})

    add_paragraph(doc, {
        'text': "Pleasure meeting with you today, and thank you for walking me "
                "through what you're dealing with at the property."
    })

    add_paragraph(doc, {
        'text': "From our discussion, it's clear the issue isn't a shortage of "
                "security presence — it's the "
    }, {
        'text': 'type', 'italic': True
    }, {
        'text': " of presence. What you need is a senior security officer: someone "
                "with the judgment, command presence, and reporting discipline to "
                "reset the atmosphere outside the hotel, not just stand at the door. "
                "Phasing out the incumbent provider will create a short period of "
                "disruption as our team takes control of the environment — a necessary "
                "step to reset the baseline, and we'll manage it tightly so it doesn't "
                "touch the guest experience."
    })

    add_paragraph(doc, {
        'text': "From day one, here's what we put in place:", 'bold': True
    })
    for b_runs in [
        [{'text': 'Senior-grade officers only', 'bold': True},
         {'text': ', uniformed to your standard, briefed on your guest profile and escalation thresholds.'}],
        [{'text': 'Centralised incident database', 'bold': True},
         {'text': ' — every breach, trespass, and intervention logged, timestamped, and shared with NZ Police liaison. Weekly and monthly reports delivered directly to you.'}],
        [{'text': 'Direct line to ASG operations', 'bold': True},
         {'text': ' — Hasi or Nikki on call, not an answering service.'}],
        [{'text': 'A clean phase-out plan', 'bold': True},
         {'text': ' for the incumbent provider to minimise handover risk.'}],
    ]:
        add_bullet(doc, b_runs)

    add_paragraph(doc,
        {'text': 'On pricing', 'bold': True},
        {'text': " — I'm pleased to offer an introductory rate of "},
        {'text': '$36.90 + GST per hour', 'bold': True},
        {'text': ', a meaningful discount on our standard commercial rate. The rate is fixed with a maximum annual increase of '},
        {'text': '2.5% or OCR, whichever is lower', 'bold': True},
        {'text': ' — so you have full cost certainty year on year.'},
        space_before=4,
    )

    add_paragraph(doc, {'text': 'Why ASG Group:', 'bold': True})
    for b_runs in [
        [{'text': 'We hold the '},
         {'text': 'Heart of the City', 'bold': True},
         {'text': " contract — Auckland's CBD business association — providing precinct-wide safety and security patrol across Queen Street, Quay Street, Aotea Square, and the Hobson/Victoria corridor. Your hotel sits inside the precinct we already secure."}],
        [{'text': 'The only covert security provider in New Zealand holding national contracts with '},
         {'text': 'Woolworths, Bunnings, and The Warehouse Group', 'bold': True},
         {'text': " — our officers are trained to de-escalate, document, and operate to a standard most hospitality guards aren't built for."}],
        [{'text': 'Already trusted across your sister properties: '},
         {'text': 'Auckland Harbour Suites, Avani Auckland (Metropolis Residences), and Radisson Auckland', 'bold': True},
         {'text': ' — all of whom referred us to you. Happy to arrange a direct reference call.'}],
        [{'text': 'Locally owned and operated with an '},
         {'text': 'Auckland-based management team', 'bold': True},
         {'text': ' — no call centres, no offshore support.'}],
        [{'text': 'Fully licensed, insured, and COA-compliant — documentation available on request.'}],
    ]:
        add_bullet(doc, b_runs)

    add_paragraph(doc, {
        'text': "I've attached our capability statement and a one-page Heart of "
                "the City case study for your records. If it's useful, I'm happy "
                "to walk you and your team through a site plan this week, and we "
                "can have officers on deck "
    }, {
        'text': 'within 7 days of sign-off', 'bold': True
    }, {
        'text': '.'
    }, space_before=4)

    add_paragraph(doc, {
        'text': "We'd genuinely value the opportunity to work alongside the Oaks "
                "brand and grow our footprint in the precinct with you."
    })

    add_paragraph(doc, {'text': 'Kind regards,'}, space_before=8, space_after=18)

    add_paragraph(doc, {'text': 'Ahmad Duais', 'bold': True, 'color': NAVY},
                  space_after=2)
    add_paragraph(doc, {'text': 'Chief Executive Officer', 'size': 10, 'color': TEXT_MED},
                  space_after=2)
    add_paragraph(doc,
                  {'text': 'ASG Group | Absolute Security Group Ltd', 'size': 10, 'color': TEXT_MED},
                  space_after=2)
    add_paragraph(doc,
                  {'text': 'M: [your number]   ·   E: [your email]   ·   W: asgsecurity.co.nz',
                   'size': 10, 'color': TEXT_MED})

    doc.save(OUT)
    print(f'[OK] {os.path.basename(OUT)}  ({os.path.getsize(OUT):,} bytes)')
    print(f'Saved to: {OUT}')


if __name__ == '__main__':
    main()
