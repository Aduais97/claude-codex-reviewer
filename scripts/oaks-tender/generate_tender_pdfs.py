#!/usr/bin/env python3
"""Generate Oaks Wellington tender PDFs for ASG Group.

Produces three deliverables in ~/Desktop/Oaks Wellington Tender/:
  1. Oaks_Wellington_Cover_Letter.pdf
  2. ASG_HOTC_Case_Study_1Pager.pdf
  3. ASG_Capability_Statement.pdf

Design system (per ASG PDF standards):
  - ReportLab, A4, Helvetica
  - Navy + gold palette
  - 54pt side margins, 62pt top
  - Min 10pt body, 8.5pt tables
"""

import sys
sys.path.insert(0, '/Users/ahmadduais/Desktop/Claude/.venv/lib/python3.14/site-packages')

import os
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable, ListFlowable, ListItem,
)

# ── Palette ─────────────────────────────────────────────────────────────────
NAVY      = HexColor('#1B2A4A')
DARK_BLUE = HexColor('#2C3E6B')
MID_BLUE  = HexColor('#4A6FA5')
LIGHT_BLUE = HexColor('#E8EDF5')
GOLD      = HexColor('#D4A843')
BG_GREY   = HexColor('#F7F8FA')
BORDER    = HexColor('#D0D5DD')
TEXT_DARK = HexColor('#1A1A2E')
TEXT_MED  = HexColor('#4A4A5A')
TEXT_LIGHT = HexColor('#7A7A8A')

W, H = A4
ML, MR, MT, MB = 54, 54, 62, 54
CW = W - ML - MR

OUT_DIR = '/Users/ahmadduais/Desktop/Oaks Wellington Tender'
os.makedirs(OUT_DIR, exist_ok=True)


# ── Styles ──────────────────────────────────────────────────────────────────
def styles():
    s = {}
    s['body'] = ParagraphStyle(
        'body', fontName='Helvetica', fontSize=10.5, leading=15,
        textColor=TEXT_DARK, alignment=TA_LEFT, spaceAfter=7,
    )
    s['body_just'] = ParagraphStyle(
        'body_just', parent=s['body'], alignment=TA_JUSTIFY,
    )
    s['body_bold'] = ParagraphStyle(
        'body_bold', parent=s['body'], fontName='Helvetica-Bold',
    )
    s['bullet'] = ParagraphStyle(
        'bullet', parent=s['body'], leftIndent=16, bulletIndent=4,
        spaceAfter=4, leading=14,
    )
    s['h1'] = ParagraphStyle(
        'h1', fontName='Helvetica-Bold', fontSize=22, leading=26,
        textColor=NAVY, spaceBefore=0, spaceAfter=4,
    )
    s['h1_center'] = ParagraphStyle(
        'h1_center', parent=s['h1'], alignment=TA_CENTER,
    )
    s['h2'] = ParagraphStyle(
        'h2', fontName='Helvetica-Bold', fontSize=13, leading=17,
        textColor=NAVY, spaceBefore=12, spaceAfter=5,
    )
    s['h3'] = ParagraphStyle(
        'h3', fontName='Helvetica-Bold', fontSize=11, leading=14,
        textColor=DARK_BLUE, spaceBefore=9, spaceAfter=3,
    )
    s['subtitle'] = ParagraphStyle(
        'subtitle', fontName='Helvetica-Oblique', fontSize=11, leading=14,
        textColor=TEXT_MED, alignment=TA_CENTER, spaceAfter=12,
    )
    s['small'] = ParagraphStyle(
        'small', fontName='Helvetica', fontSize=9, leading=12,
        textColor=TEXT_MED, spaceAfter=4,
    )
    s['small_center'] = ParagraphStyle(
        'small_center', parent=s['small'], alignment=TA_CENTER,
    )
    s['footer'] = ParagraphStyle(
        'footer', fontName='Helvetica', fontSize=8, leading=10,
        textColor=TEXT_LIGHT, alignment=TA_CENTER,
    )
    s['tag'] = ParagraphStyle(
        'tag', fontName='Helvetica-Bold', fontSize=9, leading=12,
        textColor=GOLD, alignment=TA_LEFT, spaceAfter=2,
    )
    return s


S = styles()


# ── Reusable components ────────────────────────────────────────────────────
def letterhead():
    """Top-of-page ASG letterhead band."""
    tbl = Table(
        [[
            Paragraph('<font color="#1B2A4A"><b>ASG GROUP</b></font>', ParagraphStyle(
                'lh', fontName='Helvetica-Bold', fontSize=16, textColor=NAVY, leading=18)),
            Paragraph(
                '<font color="#4A4A5A">Absolute Security Group Limited</font><br/>'
                '<font color="#7A7A8A">Auckland, New Zealand</font>',
                ParagraphStyle('lhr', fontName='Helvetica', fontSize=9, leading=11,
                               alignment=TA_LEFT, textColor=TEXT_MED)),
        ]],
        colWidths=[CW * 0.45, CW * 0.55],
    )
    tbl.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBELOW', (0, 0), (-1, -1), 1.5, GOLD),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    return tbl


def footer_band(text='ASG Group | Absolute Security Group Ltd  |  asgsecurity.co.nz'):
    return Paragraph(text, S['footer'])


def bullets(items, style_key='bullet'):
    flows = []
    for it in items:
        flows.append(Paragraph(f'• {it}', S[style_key]))
    return flows


def info_card(rows, col_widths=None):
    """Two-column key/value card with subtle background."""
    if col_widths is None:
        col_widths = [CW * 0.28, CW * 0.72]
    data = []
    for k, v in rows:
        data.append([
            Paragraph(f'<b>{k}</b>', S['small']),
            Paragraph(v, S['small']),
        ])
    tbl = Table(data, colWidths=col_widths)
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_GREY),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, BORDER),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return tbl


# ══════════════════════════════════════════════════════════════════════════
# 1. COVER LETTER
# ══════════════════════════════════════════════════════════════════════════
def build_cover_letter(path):
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=ML, rightMargin=MR,
        topMargin=MT, bottomMargin=MB,
        title='Oaks Wellington — Senior Security Proposal',
        author='ASG Group',
    )
    story = []

    story.append(letterhead())
    story.append(Spacer(1, 18))

    today = datetime.now().strftime('%-d %B %Y')
    story.append(Paragraph(today, S['small']))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        '<b>Zafer</b><br/>'
        'Oaks Wellington, Auckland CBD<br/>'
        'Auckland, New Zealand',
        S['small']))
    story.append(Spacer(1, 14))

    story.append(Paragraph(
        '<b>Re: Senior Security Cover — Oaks Wellington</b>', S['h3']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('Hi Zafer,', S['body']))

    story.append(Paragraph(
        'Pleasure meeting with you today, and thank you for walking me through '
        'what you&#39;re dealing with at the property.',
        S['body_just']))

    story.append(Paragraph(
        'From our discussion, it&#39;s clear the issue isn&#39;t a shortage of security '
        'presence — it&#39;s the <b>type</b> of presence. What you need is a senior '
        'security officer: someone with the judgment, command presence, and reporting '
        'discipline to reset the atmosphere outside the hotel, not just stand at the door. '
        'Phasing out the incumbent provider will create a short period of disruption as our '
        'team takes control of the environment — a necessary step to reset the baseline, '
        'and we&#39;ll manage it tightly so it doesn&#39;t touch the guest experience.',
        S['body_just']))

    story.append(Paragraph('<b>From day one, here&#39;s what we put in place:</b>', S['body']))
    for b in [
        'Senior-grade officers only, uniformed to your standard, briefed on your '
        'guest profile and escalation thresholds',
        'Centralised incident database — every breach, trespass, and intervention '
        'logged, timestamped, and shared with NZ Police liaison. Weekly and monthly '
        'reports delivered directly to you',
        'Direct line to ASG operations — Hasi or Nikki on call, not an answering service',
        'A clean phase-out plan for the incumbent provider to minimise handover risk',
    ]:
        story.append(Paragraph(f'• {b}', S['bullet']))

    story.append(Spacer(1, 4))
    story.append(Paragraph(
        '<b>On pricing</b> — I&#39;m pleased to offer an introductory rate of '
        '<b>$36.90 + GST per hour</b>, a meaningful discount on our standard '
        'commercial rate. The rate is fixed with a maximum annual increase of '
        '<b>2.5% or OCR, whichever is lower</b> — so you have full cost certainty '
        'year on year.',
        S['body_just']))

    story.append(Paragraph('<b>Why ASG Group:</b>', S['body']))
    for b in [
        'We hold the <b>Heart of the City</b> contract — Auckland&#39;s CBD business '
        'association — providing precinct-wide safety and security patrol across '
        'Queen Street, Quay Street, Aotea Square, and the Hobson/Victoria corridor. '
        'Your hotel sits inside the precinct we already secure.',
        'The only covert security provider in New Zealand holding national contracts '
        'with <b>Woolworths, Bunnings, and The Warehouse Group</b> — our officers are '
        'trained to de-escalate, document, and operate to a standard most hospitality '
        'guards aren&#39;t built for',
        'Already trusted across your sister properties: <b>Auckland Harbour Suites, '
        'Avani Auckland (Metropolis Residences), and Radisson Auckland</b> — all of '
        'whom referred us to you. Happy to arrange a direct reference call.',
        'Locally owned and operated with an <b>Auckland-based management team</b> — '
        'no call centres, no offshore support',
        'Fully licensed, insured, and COA-compliant — documentation available on request',
    ]:
        story.append(Paragraph(f'• {b}', S['bullet']))

    story.append(Spacer(1, 4))
    story.append(Paragraph(
        'I&#39;ve attached our capability statement and a one-page Heart of the City '
        'case study for your records. If it&#39;s useful, I&#39;m happy to walk you and '
        'your team through a site plan this week, and we can have officers on deck '
        '<b>within 7 days of sign-off</b>.',
        S['body_just']))

    story.append(Paragraph(
        'We&#39;d genuinely value the opportunity to work alongside the Oaks brand '
        'and grow our footprint in the precinct with you.',
        S['body_just']))

    story.append(Spacer(1, 10))
    story.append(Paragraph('Kind regards,', S['body']))
    story.append(Spacer(1, 16))
    story.append(Paragraph('<b>Ahmad Duais</b>', S['body']))
    story.append(Paragraph(
        'Chief Executive Officer<br/>'
        'ASG Group | Absolute Security Group Ltd<br/>'
        'M: [your number]  |  E: [your email]  |  W: asgsecurity.co.nz',
        S['small']))

    doc.build(story, onFirstPage=_page_footer, onLaterPages=_page_footer)


def _page_footer(canv, doc):
    canv.saveState()
    canv.setFont('Helvetica', 8)
    canv.setFillColor(TEXT_LIGHT)
    canv.drawCentredString(
        W / 2, 30,
        'ASG Group  |  Absolute Security Group Ltd  |  asgsecurity.co.nz')
    canv.restoreState()


# ══════════════════════════════════════════════════════════════════════════
# 2. HOTC CASE STUDY — 1 PAGER
# ══════════════════════════════════════════════════════════════════════════
def build_case_study(path):
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=ML, rightMargin=MR,
        topMargin=MT, bottomMargin=MB,
        title='Heart of the City — ASG Case Study',
        author='ASG Group',
    )
    story = []

    story.append(letterhead())
    story.append(Spacer(1, 14))

    story.append(Paragraph('CASE STUDY', S['tag']))
    story.append(Paragraph(
        'Heart of the City — Auckland CBD Precinct Safety &amp; Security',
        S['h1']))
    story.append(Paragraph(
        'Two years securing Auckland&#39;s city centre for its business association',
        S['subtitle']))

    story.append(info_card([
        ('Client', 'Heart of the City Incorporated (HOTC) — Auckland CBD business association'),
        ('Service', 'Safety &amp; security patrol, Auckland City Centre (precinct-wide)'),
        ('Scope', '4 patrol routes across Queen St, Quay St, Aotea Square, Hobson/Victoria corridor'),
        ('Status', 'Active, multi-year contract — operational since March 2024'),
    ]))
    story.append(Spacer(1, 10))

    story.append(Paragraph('The Challenge', S['h3']))
    story.append(Paragraph(
        'Auckland&#39;s city centre — one of the densest, highest-footfall precincts in '
        'New Zealand — facing the full spectrum of CBD pressure: public drinking, '
        'aggression, anti-social behaviour, rough sleeping, and spillover between '
        'venues and streets. All of it threatening the experience of every business, '
        'resident, and guest inside the precinct.',
        S['body_just']))

    story.append(Paragraph('What ASG Did', S['h3']))
    for b in [
        'Deployed senior-grade officers across four coordinated patrol routes '
        '(Alpha, Bravo, Charlie, Delta/Echo) covering the full CBD precinct',
        'Built a centralised incident reporting system with formal NZ Police liaison',
        'Delivered daily logs, weekly performance reports, and monthly trend analysis '
        'to HOTC and precinct stakeholders',
        'Integrated with retail, hospitality, and corporate tenants for real-time '
        'communication and rapid handoffs',
        'Supplemented foot patrols with two eco-friendly vehicle patrols covering '
        'evening and overnight high-risk windows',
    ]:
        story.append(Paragraph(f'• {b}', S['bullet']))

    story.append(Paragraph('Measured Results (2024 → 2025)', S['h3']))

    # Results table
    results_data = [
        ['Metric', '2024', '2025', 'Change'],
        ['Business calls responded', '2,305', '2,833', '+2.4% / month'],
        ['Police escalations', '460', '437', '−21% / month'],
        ['Public drinking incidents', '411', '418', '−15% / month'],
        ['Aggression incidents', '466', '558', 'Flat (~46/mo)'],
        ['Patrol routes completed', '4,244', '5,002', '9,700+ total'],
    ]
    tbl = Table(results_data, colWidths=[CW*0.42, CW*0.17, CW*0.17, CW*0.24])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, BG_GREY]),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, BORDER),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        'Across 23 months of operations, ASG teams responded to <b>5,300+ business '
        'calls</b>, managed <b>950 police interactions</b>, and completed <b>9,700+ '
        'patrol routes</b> across Auckland CBD. Police escalations fell 21% year on '
        'year — ASG resolving more incidents without escalation — while business '
        'trust increased (business-assist calls up 2.4%).',
        S['body_just']))

    story.append(Paragraph('Why This Matters for a Hotel', S['h3']))
    story.append(Paragraph(
        'Hospitality security isn&#39;t about standing at a door. It&#39;s about '
        'controlling the environment guests experience the moment they arrive — '
        'and protecting the brand between the street and the lobby. HOTC is proof '
        'that ASG does exactly that across the most demanding precinct in New Zealand. '
        'If your hotel sits inside Auckland CBD, we are already patrolling the streets '
        'around it.',
        S['body_just']))

    doc.build(story, onFirstPage=_page_footer, onLaterPages=_page_footer)


# ══════════════════════════════════════════════════════════════════════════
# 3. CAPABILITY STATEMENT
# ══════════════════════════════════════════════════════════════════════════
def build_capability(path):
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=ML, rightMargin=MR,
        topMargin=MT, bottomMargin=MB,
        title='ASG Group — Capability Statement',
        author='ASG Group',
    )
    story = []

    story.append(letterhead())
    story.append(Spacer(1, 14))

    story.append(Paragraph('CAPABILITY STATEMENT', S['tag']))
    story.append(Paragraph('ASG Group', S['h1']))
    story.append(Paragraph(
        'Senior-grade guarding, covert loss prevention, monitoring, and electronic '
        'security — New Zealand owned, Auckland based.',
        S['subtitle']))

    story.append(Paragraph(
        'Absolute Security Group Limited is a New Zealand-owned and operated security '
        'services provider headquartered in Auckland. We deliver senior-grade guarding, '
        'covert loss prevention, monitoring, and electronic security across four service '
        'lines — backed by a locally based management team and a reporting standard most '
        'providers can&#39;t match.',
        S['body_just']))

    story.append(Paragraph('Who We Are', S['h2']))
    story.append(info_card([
        ('CEO', 'Ahmad Duais'),
        ('General Manager', 'Mark Clansey'),
        ('Operations Managers', 'Hasi Nabawi, Nikki Christian'),
        ('Headquarters', 'Auckland, New Zealand'),
        ('Group Revenue (FY26)', '$6.8M+'),
        ('Licensing', 'Fully COA-licensed, fully insured'),
    ]))

    story.append(Paragraph('Service Lines', S['h2']))

    story.append(Paragraph('1. Hospitality &amp; Venue Guarding', S['h3']))
    story.append(Paragraph(
        'Senior-grade officers for hotels, bars, restaurants, events, and multi-venue '
        'precincts. Our flagship precinct contract is with <b>Heart of the City</b> '
        '(HOTC) — Auckland CBD&#39;s business association — covering the full city '
        'centre across four coordinated patrol routes.',
        S['body_just']))

    story.append(Paragraph('2. Retail Loss Prevention (Covert)', S['h3']))
    story.append(Paragraph(
        'The only covert loss-prevention provider in New Zealand holding national '
        'contracts with <b>Woolworths, Bunnings, and The Warehouse Group</b>. '
        'Nationwide operative network, discreet surveillance, and apprehension.',
        S['body_just']))

    story.append(Paragraph('3. Monitoring &amp; Patrol', S['h3']))
    story.append(Paragraph(
        'Mobile patrol, alarm response, and site monitoring for commercial and '
        'residential clients. Eco-friendly vehicle fleet.',
        S['body_just']))

    story.append(Paragraph('4. Electronic Security', S['h3']))
    story.append(Paragraph(
        'CCTV, access control, and integrated electronic security systems — '
        'specification, installation, and ongoing support.',
        S['body_just']))

    story.append(Paragraph('Selected Clients', S['h2']))
    client_data = [
        ['Retail (National)', 'Woolworths New Zealand  ·  Bunnings  ·  The Warehouse Group (The Warehouse, Noel Leeming)'],
        ['Precinct', 'Heart of the City Incorporated (Auckland CBD)'],
        ['Hospitality', 'Auckland Harbour Suites  ·  Avani Auckland (Metropolis Residences)  ·  Radisson Auckland'],
    ]
    ctbl = Table(client_data, colWidths=[CW*0.22, CW*0.78])
    ctbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), NAVY),
        ('TEXTCOLOR', (0, 0), (0, -1), white),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (1, 0), (1, -1), BG_GREY),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, BORDER),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(ctbl)

    story.append(Paragraph('Why ASG', S['h2']))
    for b in [
        '<b>Senior-grade officers only</b> — we don&#39;t send juniors to sensitive sites',
        '<b>Centralised incident database</b> with NZ Police liaison integration',
        '<b>Full reporting suite</b> — daily, weekly, and monthly reports on every contract',
        '<b>Auckland-based management</b> — always reachable. No call centres, no offshore support',
        '<b>Cost certainty</b> — annual rate increases capped at 2.5% or OCR, whichever is lower',
        '<b>Proven at scale</b> — 9,700+ patrol routes and 5,300+ business calls handled '
        'across the Heart of the City contract alone',
    ]:
        story.append(Paragraph(f'• {b}', S['bullet']))

    story.append(Spacer(1, 6))
    story.append(HRFlowable(width=CW, thickness=0.8, color=GOLD, spaceBefore=4, spaceAfter=8))
    story.append(Paragraph('Contact', S['h3']))
    story.append(Paragraph(
        '<b>Ahmad Duais</b> — Chief Executive Officer<br/>'
        'ASG Group | Absolute Security Group Ltd<br/>'
        'Auckland, New Zealand  |  W: asgsecurity.co.nz',
        S['small']))

    doc.build(story, onFirstPage=_page_footer, onLaterPages=_page_footer)


# ══════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════
def main():
    outputs = [
        (os.path.join(OUT_DIR, 'Oaks_Wellington_Cover_Letter.pdf'), build_cover_letter),
        (os.path.join(OUT_DIR, 'ASG_HOTC_Case_Study_1Pager.pdf'), build_case_study),
        (os.path.join(OUT_DIR, 'ASG_Capability_Statement.pdf'), build_capability),
    ]
    for path, builder in outputs:
        builder(path)
        size = os.path.getsize(path)
        print(f'  [OK] {os.path.basename(path)}  ({size:,} bytes)')
    print(f'\nAll PDFs written to: {OUT_DIR}')


if __name__ == '__main__':
    main()
