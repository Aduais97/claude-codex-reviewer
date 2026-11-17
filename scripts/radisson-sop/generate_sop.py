#!/usr/bin/env python3
"""Radisson RED Auckland — Host & Concierge Standard Operating Procedure.

Client deliverable for ASG Group. Produces:
  ~/Desktop/Radisson RED Auckland/ASG_Radisson_RED_Host_Concierge_SOP.pdf

Source material: client correspondence with Parijata Moeava (People & Culture
Manager) and Nileshni Chand (Financial Controller), Radisson RED Auckland —
trespass authority, drug-use process, reporting standards, conduct, access
control, and waste/delivery handling.

Design system (ASG PDF standards): ReportLab, A4, Helvetica, navy + gold,
54pt sides / 62pt top margins, min 10pt body / 8.5pt tables, ToC, clean cards.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable,
)

# ── Palette ──────────────────────────────────────────────────────────────────
NAVY       = HexColor('#1B2A4A')
DARK_BLUE  = HexColor('#2C3E6B')
MID_BLUE   = HexColor('#4A6FA5')
LIGHT_BLUE = HexColor('#E8EDF5')
GOLD       = HexColor('#D4A843')
RED_ACCENT = HexColor('#B3242B')   # Radisson RED nod, used sparingly for ALERT
BG_GREY    = HexColor('#F7F8FA')
BORDER     = HexColor('#D0D5DD')
TEXT_DARK  = HexColor('#1A1A2E')
TEXT_MED   = HexColor('#4A4A5A')
TEXT_LIGHT = HexColor('#7A7A8A')

W, H = A4
ML, MR, MT, MB = 54, 54, 62, 56
CW = W - ML - MR

OUT_DIR = os.path.expanduser('~/Desktop/Radisson RED Auckland')
os.makedirs(OUT_DIR, exist_ok=True)
OUT = os.path.join(OUT_DIR, 'ASG_Radisson_RED_Host_Concierge_SOP.pdf')

DOC_NO   = 'ASG-SOP-RR-001'
VERSION  = 'v1.0 (Draft)'
ISSUED   = '9 June 2026'


# ── Styles ───────────────────────────────────────────────────────────────────
def styles():
    s = {}
    s['body'] = ParagraphStyle('body', fontName='Helvetica', fontSize=10,
        leading=14.5, textColor=TEXT_DARK, alignment=TA_LEFT, spaceAfter=7)
    s['body_just'] = ParagraphStyle('body_just', parent=s['body'], alignment=TA_JUSTIFY)
    s['bullet'] = ParagraphStyle('bullet', parent=s['body'], leftIndent=15,
        bulletIndent=3, spaceAfter=4, leading=14)
    s['bullet_tight'] = ParagraphStyle('bullet_tight', parent=s['bullet'], spaceAfter=2)
    s['num'] = ParagraphStyle('num', parent=s['body'], leftIndent=20,
        bulletIndent=2, spaceAfter=5, leading=14)
    s['h1'] = ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=20,
        leading=24, textColor=NAVY, spaceBefore=0, spaceAfter=4)
    s['h2'] = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=13.5,
        leading=17, textColor=NAVY, spaceBefore=4, spaceAfter=6)
    s['h3'] = ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=11,
        leading=14, textColor=DARK_BLUE, spaceBefore=9, spaceAfter=3)
    s['subtitle'] = ParagraphStyle('subtitle', fontName='Helvetica-Oblique',
        fontSize=11, leading=15, textColor=TEXT_MED, alignment=TA_CENTER, spaceAfter=10)
    s['small'] = ParagraphStyle('small', fontName='Helvetica', fontSize=9,
        leading=12, textColor=TEXT_MED, spaceAfter=3)
    s['small_c'] = ParagraphStyle('small_c', parent=s['small'], alignment=TA_CENTER)
    s['tag'] = ParagraphStyle('tag', fontName='Helvetica-Bold', fontSize=9.5,
        leading=12, textColor=GOLD, alignment=TA_LEFT, spaceAfter=3)
    s['toc'] = ParagraphStyle('toc', fontName='Helvetica', fontSize=10.5,
        leading=18, textColor=TEXT_DARK)
    s['cover_t'] = ParagraphStyle('cover_t', fontName='Helvetica-Bold', fontSize=30,
        leading=34, textColor=white, alignment=TA_LEFT)
    s['cover_s'] = ParagraphStyle('cover_s', fontName='Helvetica', fontSize=13,
        leading=18, textColor=HexColor('#D7DEEC'), alignment=TA_LEFT)
    s['cell'] = ParagraphStyle('cell', fontName='Helvetica', fontSize=8.7,
        leading=11.5, textColor=TEXT_DARK)
    s['cell_b'] = ParagraphStyle('cell_b', parent=s['cell'], fontName='Helvetica-Bold')
    s['cell_w'] = ParagraphStyle('cell_w', parent=s['cell'], textColor=white,
        fontName='Helvetica-Bold', fontSize=9)
    return s


S = styles()


# ── Components ───────────────────────────────────────────────────────────────
def letterhead():
    tbl = Table([[
        Paragraph('<font color="#1B2A4A"><b>ASG</b></font>'
                  '<font color="#D4A843"><b> GROUP</b></font>',
                  ParagraphStyle('lh', fontName='Helvetica-Bold', fontSize=15,
                                 textColor=NAVY, leading=17)),
        Paragraph('<font color="#4A4A5A">Absolute Security Group Limited</font><br/>'
                  '<font color="#7A7A8A">Host &amp; Concierge Services &nbsp;|&nbsp; Auckland</font>',
            ParagraphStyle('lhr', fontName='Helvetica', fontSize=8.5, leading=11,
                           alignment=2, textColor=TEXT_MED)),
    ]], colWidths=[CW * 0.4, CW * 0.6])
    tbl.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBELOW', (0, 0), (-1, -1), 1.4, GOLD),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (0, 0), 0),
        ('RIGHTPADDING', (-1, 0), (-1, 0), 0),
    ]))
    return tbl


def h2(num, title):
    return Paragraph(f'<font color="#D4A843">{num}</font>&nbsp;&nbsp;{title}', S['h2'])


def bullets(items, key='bullet'):
    return [Paragraph(f'•&nbsp;&nbsp;{it}', S[key]) for it in items]


def numbered(items):
    return [Paragraph(f'<b><font color="#2C3E6B">{i}.</font></b>&nbsp;&nbsp;{it}', S['num'])
            for i, it in enumerate(items, 1)]


def info_card(rows, c0=0.26):
    data = [[Paragraph(f'<b>{k}</b>', S['small']), Paragraph(v, S['small'])] for k, v in rows]
    tbl = Table(data, colWidths=[CW * c0, CW * (1 - c0)])
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


def callout(title, body, accent=None, bg=None):
    """Clean, non-boxed emphasis block: bold navy lead-in + plain body text.
    `accent`/`bg` are accepted for backwards compatibility but no longer drawn."""
    flows = [Paragraph(title, ParagraphStyle('co_t', fontName='Helvetica-BoldOblique',
                fontSize=10, leading=14, textColor=NAVY, spaceBefore=4, spaceAfter=2))]
    if isinstance(body, str):
        body = [body]
    for b in body:
        flows.append(Paragraph(b, ParagraphStyle('co_b', fontName='Helvetica-Oblique',
                fontSize=10, leading=14, textColor=TEXT_MED, spaceAfter=4)))
    flows.append(Spacer(1, 2))
    return KeepTogether(flows)


def table(header, rows, col_widths, header_bg=NAVY, zebra=True):
    data = [[Paragraph(h, S['cell_w']) for h in header]]
    for r in rows:
        data.append([Paragraph(str(c), S['cell']) for c in r])
    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    st = [
        ('BACKGROUND', (0, 0), (-1, 0), header_bg),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]
    if zebra:
        for i in range(1, len(data)):
            if i % 2 == 0:
                st.append(('BACKGROUND', (0, i), (-1, i), BG_GREY))
    tbl.setStyle(TableStyle(st))
    return tbl


# ── Page furniture ───────────────────────────────────────────────────────────
def _footer(canv, doc):
    canv.saveState()
    if doc.page > 1:
        canv.setFont('Helvetica', 8)
        canv.setFillColor(TEXT_LIGHT)
        canv.drawString(ML, 32, f'{DOC_NO}  ·  {VERSION}')
        canv.drawCentredString(W / 2, 32,
            'ASG Group  |  Radisson RED Auckland — Host & Concierge SOP')
        canv.drawRightString(W - MR, 32, f'Page {doc.page}')
        canv.setStrokeColor(BORDER)
        canv.setLineWidth(0.5)
        canv.line(ML, 44, W - MR, 44)
    canv.restoreState()


def _cover(canv, doc):
    canv.saveState()
    canv.setFillColor(NAVY)
    canv.rect(0, H - 430, W, 430, fill=1, stroke=0)
    canv.setFillColor(GOLD)
    canv.rect(0, H - 438, W, 8, fill=1, stroke=0)
    # bottom band
    canv.setFillColor(NAVY)
    canv.rect(0, 0, W, 86, fill=1, stroke=0)
    canv.setFillColor(GOLD)
    canv.rect(0, 86, W, 4, fill=1, stroke=0)
    canv.restoreState()


# ══════════════════════════════════════════════════════════════════════════
def build():
    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=ML, rightMargin=MR,
        topMargin=MT, bottomMargin=MB,
        title='Radisson RED Auckland — Host & Concierge SOP', author='ASG Group')
    story = []

    # ── COVER ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 70))
    story.append(Paragraph('STANDARD OPERATING PROCEDURE', ParagraphStyle(
        'ct', fontName='Helvetica-Bold', fontSize=11, leading=14,
        textColor=GOLD, alignment=TA_LEFT)))
    story.append(Spacer(1, 10))
    story.append(Paragraph('Host &amp; Concierge<br/>Services', S['cover_t']))
    story.append(Spacer(1, 12))
    story.append(Paragraph('Radisson RED Auckland &nbsp;·&nbsp; 33 Lorne Street, Auckland 1010',
        S['cover_s']))
    story.append(Spacer(1, 8))
    story.append(Paragraph('Prepared by Absolute Security Group Limited '
        'for the People &amp; Culture and Operations teams, Radisson RED Auckland',
        ParagraphStyle('cx', fontName='Helvetica', fontSize=10.5, leading=15,
                       textColor=HexColor('#C7D0E2'), alignment=TA_LEFT)))
    story.append(Spacer(1, 150))
    story.append(info_card([
        ('Document', f'{DOC_NO} &nbsp;—&nbsp; Host &amp; Concierge Standard Operating Procedure'),
        ('Version', f'{VERSION}'),
        ('Issued', f'{ISSUED}'),
        ('Prepared by', 'Ahmad Duais, CEO — Absolute Security Group Limited'),
        ('Prepared for', 'Parijata Moeava, People &amp; Culture Manager — Radisson RED Auckland'),
        ('Classification', 'Operational — for ASG officers and Radisson RED management'),
    ], c0=0.22))
    story.append(PageBreak())

    # ── DOCUMENT CONTROL + ToC ────────────────────────────────────────────────
    story.append(letterhead())
    story.append(Spacer(1, 14))
    story.append(Paragraph('Document Control', S['h2']))
    story.append(table(
        ['Field', 'Detail'],
        [
            ['Title', 'Host &amp; Concierge Standard Operating Procedure — Radisson RED Auckland'],
            ['Document number', DOC_NO],
            ['Version', VERSION],
            ['Issued', ISSUED],
            ['Owner', 'Absolute Security Group Limited (ASG Group)'],
            ['Client sponsor', 'Parijata Moeava — People &amp; Culture Manager, Radisson RED Auckland'],
            ['Applies to', 'All ASG Host &amp; Concierge officers deployed at Radisson RED Auckland'],
            ['Review cycle', 'Annual, or after any significant incident — whichever is sooner'],
            ['Related documents', 'ASG Trespass Register; ASG Incident Report; Radisson RED House Rules &amp; Guest Terms of Stay'],
        ],
        [CW * 0.24, CW * 0.76]))
    story.append(Spacer(1, 16))

    story.append(Paragraph('Contents', S['h2']))
    toc = [
        ('1', 'Purpose &amp; Scope'),
        ('2', 'Site Overview &amp; Key Contacts'),
        ('3', 'The Host &amp; Concierge Role'),
        ('4', 'Presentation, Conduct &amp; Standards'),
        ('5', 'Shift Routine &amp; Patrols'),
        ('6', 'Access Control, Deliveries &amp; Waste Collection'),
        ('7', 'Reporting &amp; the Shared Drive'),
        ('8', 'Trespass Authority &amp; Process'),
        ('9', 'Drug Use — Response Procedure'),
        ('10', 'Incident Management &amp; Escalation'),
        ('11', 'Legislative &amp; Compliance Framework'),
        ('12', 'Emergency &amp; Escalation Contacts'),
        ('A', 'Appendix A — Nightly Shift Report Template'),
        ('B', 'Appendix B — Trespass Register &amp; Notice Checklist'),
    ]
    for n, t in toc:
        story.append(Paragraph(
            f'<font color="#D4A843"><b>{n}</b></font>&nbsp;&nbsp;&nbsp;{t}', S['toc']))
    story.append(PageBreak())

    # ── 1. PURPOSE & SCOPE ────────────────────────────────────────────────────
    story.append(letterhead()); story.append(Spacer(1, 14))
    story.append(Paragraph('SECTION 1', S['tag']))
    story.append(h2('1', 'Purpose &amp; Scope'))
    story.append(Paragraph(
        'This Standard Operating Procedure (SOP) sets out how Absolute Security Group '
        '(ASG) delivers its <b>Host &amp; Concierge</b> service at Radisson RED Auckland. '
        'It defines the standards of presentation and conduct expected of every officer, '
        'the nightly operating routine, and the procedures the team will follow for access '
        'control, reporting, trespass, and incident management.', S['body_just']))
    story.append(Paragraph(
        'The Host &amp; Concierge role at Radisson RED is deliberately blended: the officer '
        'is the calm, professional first point of contact for guests after hours, while also '
        'holding clear responsibility for the safety and security of the property, its '
        'people, and its assets. This document gives the team a single reference for "how '
        'this is to be facilitated", and gives Radisson RED management confidence that every '
        'shift is run to a consistent, documented standard.', S['body_just']))
    story.append(Paragraph('This SOP covers:', S['body']))
    story.extend(bullets([
        'The conduct, presentation and positioning of ASG officers on site;',
        'The nightly patrol and walk-about routine, and what is observed and recorded;',
        'Access control for guests, suppliers, early-morning deliveries and waste collection;',
        'Reporting via the shared drive, including brief walk-about notes and full incident reports;',
        'The <b>Trespass Authority</b> and the step-by-step trespass process;',
        'The response to suspected drug use on the premises;',
        'Escalation to the Duty Manager, ASG management, NZ Police and Heart of the City support.',
    ]))
    story.append(Spacer(1, 4))
    story.append(callout('Guiding principle',
        'ASG officers protect the Radisson RED experience. We are warm and helpful to guests, '
        'firm and procedural on safety, and we document everything. When in doubt, observe, '
        'record, notify the Duty Manager, and escalate — never improvise on safety.'))
    story.append(PageBreak())

    # ── 2. SITE & CONTACTS ────────────────────────────────────────────────────
    story.append(letterhead()); story.append(Spacer(1, 14))
    story.append(Paragraph('SECTION 2', S['tag']))
    story.append(h2('2', 'Site Overview &amp; Key Contacts'))
    story.append(info_card([
        ('Property', 'Radisson RED Auckland'),
        ('Address', '33 Lorne Street, Auckland 1010, New Zealand'),
        ('Service', 'Overnight Host &amp; Concierge / security presence'),
        ('Shift', '11:00pm – 7:00am, Monday to Sunday (7 nights per week)'),
        ('Primary zones', 'Lobby &amp; Queen Street / Lorne Street entrances, all external doors, '
                          'loading dock, Level 3 car park, winter garden, bar &amp; guest floors'),
        ('Reporting to', 'Radisson RED Duty Manager (on shift); Parijata Moeava, P&amp;C Manager'),
    ], c0=0.22))
    story.append(Spacer(1, 12))
    story.append(Paragraph('Key contacts', S['h3']))
    story.append(table(
        ['Name', 'Role', 'Contact'],
        [
            ['Radisson RED Duty Manager', 'On-shift escalation — first point of contact', 'Via hotel front desk / radio'],
            ['Parijata Moeava', 'People &amp; Culture Manager, Radisson RED', '+64 290 400 4504'],
            ['Nileshni Chand (Nila)', 'Financial Controller, Radisson RED', '+64 290 400 4505'],
            ['Reinout Engel', 'Radisson RED management', 'Via hotel'],
            ['Hasi Nabawi', 'ASG — primary contact / operations', '020 4007 9904'],
            ['Ahmad Duais', 'CEO, ASG Group — account owner', '09 950 4640 / 021 0850 0009'],
            ['ASG Operations', 'On-call ASG support (24/7)', 'Via ASG control room'],
            ['Heart of the City (HOTC)', 'CBD safety support line', '09 961 6161'],
            ['NZ Police / Emergency', 'Immediate threat to life or safety', '111'],
        ],
        [CW * 0.27, CW * 0.45, CW * 0.28]))
    story.append(Spacer(1, 8))
    story.append(callout('Contact note',
        'Confirm the on-shift Duty Manager&#39;s name and the current internal radio / phone '
        'protocol at the start of every shift. Contact numbers above are to be verified and '
        'kept current by the ASG site supervisor.', accent=MID_BLUE))
    story.append(PageBreak())

    # ── 3. THE ROLE ───────────────────────────────────────────────────────────
    story.append(letterhead()); story.append(Spacer(1, 14))
    story.append(Paragraph('SECTION 3', S['tag']))
    story.append(h2('3', 'The Host &amp; Concierge Role'))
    story.append(Paragraph(
        'The Host &amp; Concierge officer is a hospitality-first security professional. The '
        'role carries two responsibilities at once, and both matter equally:', S['body_just']))
    story.append(Paragraph('Host &amp; Concierge (guest-facing)', S['h3']))
    story.extend(bullets([
        'Provide a warm, professional, brand-appropriate welcome and presence after hours;',
        'Assist guests with directions, access, taxis/ride-share, and general queries, or '
        'refer them to the Duty Manager where appropriate;',
        'Be visible and approachable at the lobby and main entrances during peak movement;',
        'Set the tone of a calm, well-run, safe property — presence is prevention.',
    ]))
    story.append(Paragraph('Security &amp; safety (protective)', S['h3']))
    story.extend(bullets([
        'Control access at all external doors, the loading dock and the Level 3 car park;',
        'Conduct regular patrols / walk-abouts of the property and record observations;',
        'Identify, de-escalate and document antisocial behaviour, intoxication, drug use, '
        'and trespass;',
        'Protect guests, staff and assets, and uphold the hotel&#39;s House Rules and Guest '
        'Terms of Stay;',
        'Escalate correctly and maintain accurate, timely records of everything observed.',
    ]))
    story.append(Spacer(1, 4))
    story.append(callout('Balance',
        'A great Radisson RED officer is hard to distinguish from a host until the moment '
        'they are needed — then they are decisive, procedural and calm. Hospitality is the '
        'default posture; security is always ready underneath it.', accent=GOLD))
    story.append(PageBreak())

    # ── 4. CONDUCT & STANDARDS ────────────────────────────────────────────────
    story.append(letterhead()); story.append(Spacer(1, 14))
    story.append(Paragraph('SECTION 4', S['tag']))
    story.append(h2('4', 'Presentation, Conduct &amp; Standards'))
    story.append(Paragraph('Presentation', S['h3']))
    story.extend(bullets([
        'Full ASG uniform, clean and pressed, worn correctly for the entire shift; ASG ID / '
        'COA licence carried at all times and produced on request;',
        'Professional grooming and demeanour consistent with the Radisson RED brand;',
        'Phone use limited to operational purposes only — never while engaging a guest.',
    ]))
    story.append(Paragraph('Conduct on site — non-negotiables', S['h3']))
    story.append(Paragraph('The following are house rules for ASG officers, set by Radisson RED '
        'management:', S['body']))
    story.extend(bullets([
        '<b>Do not sit in guest areas.</b> Officers are <b>not</b> to be seated at the bar, '
        'in guest areas, or in the winter garden at any point during the shift.',
        '<b>Off-duty is different.</b> Enjoying the bar or guest services is only acceptable '
        '<i>after</i> the shift has finished, as a paying guest — never while on duty or in uniform on shift.',
        '<b>Smoking / vaping is restricted to the Level 3 car park staff area only.</b> No other '
        'area of the property is permitted for smoking or vaping, with the sole exception of the '
        'designated spot directly opposite the entrance.',
    ]))
    story.append(Spacer(1, 4))
    story.append(Paragraph('General standards', S['h3']))
    story.extend(bullets([
        'Remain alert and on task for the full shift — no sleeping, and no extended absences from post;',
        'Stay in assigned zones; complete patrols on schedule rather than settling in one comfortable spot;',
        'Be courteous and impartial with guests, staff and the public at all times;',
        'Maintain strict confidentiality — never discuss guests, incidents, or hotel/ASG security '
        'arrangements with anyone outside the authorised chain;',
        'Zero tolerance for being unfit for duty (alcohol/drugs) — report fit and stay fit for work.',
    ]))
    story.append(PageBreak())

    # ── 5. SHIFT ROUTINE & PATROLS ────────────────────────────────────────────
    story.append(letterhead()); story.append(Spacer(1, 14))
    story.append(Paragraph('SECTION 5', S['tag']))
    story.append(h2('5', 'Shift Routine &amp; Patrols'))
    story.append(Paragraph(
        'The Host &amp; Concierge shift runs <b>11:00pm to 7:00am, Monday to Sunday</b> — a '
        'seven-night-per-week overnight presence. Officers cover the property through the '
        'quietest and highest-risk hours, when most access control, patrols, deliveries and '
        'waste collection take place.', S['body_just']))
    story.append(Paragraph('Start of shift (from 11:00pm)', S['h3']))
    story.extend(numbered([
        'Arrive before 11:00pm, in full uniform, and sign on. Confirm the on-shift Duty Manager.',
        'Take a handover: review the previous shift report and any flagged guests, '
        'trespass notices, or ongoing issues.',
        'Confirm radio / phone, keys, access fobs and torch are working.',
        'Walk the property once to establish a baseline — note anything already out of place.',
    ]))
    story.append(Paragraph('Patrols / walk-abouts', S['h3']))
    story.append(Paragraph(
        'Conduct regular walk-abouts across the shift (and additional patrols whenever '
        'movement or risk increases). Cover, as a minimum:', S['body']))
    story.extend(bullets([
        'All external doors and the <b>Queen Street / Lorne Street entrances</b> — record entries and exits;',
        'The <b>Level 3 car park</b> — a known spot for loiterers, rough sleepers, and people '
        'using the area to smoke illegal substances. Check on each patrol and after every '
        'after-hours opening;',
        'Loading dock / rubbish area, lobby, lifts, stairwells, winter garden and guest-floor landings;',
        'Any area flagged at handover or by the Duty Manager.',
    ]))
    story.append(callout('What to record on every walk-about',
        'Brief notes are enough — full detail only for incidents. Capture: time of patrol, '
        'doors checked (and any found unsecured), entries/exits observed, the number of times '
        'the car park is opened after hours, anyone loitering or behaving unusually, and any '
        'safety hazard. See Section 7 and Appendix A.', accent=MID_BLUE))
    story.append(Paragraph('End of shift (to 7:00am)', S['h3']))
    story.extend(numbered([
        'Complete and submit the nightly shift report to the shared drive before sign-off.',
        'Hand over outstanding issues, flagged guests and any open incidents to the next officer / Duty Manager.',
        'Return keys, fobs and equipment; confirm all doors are in their correct secured state.',
    ]))
    story.append(PageBreak())

    # ── 6. ACCESS CONTROL / DELIVERIES / WASTE ────────────────────────────────
    story.append(letterhead()); story.append(Spacer(1, 14))
    story.append(Paragraph('SECTION 6', S['tag']))
    story.append(h2('6', 'Access Control, Deliveries &amp; Waste Collection'))
    story.append(Paragraph(
        'Controlling who and what moves in and out of the property after hours is a core '
        'duty. The officer opens and secures access points, supervises deliveries and '
        'collections, and records the times — these records are relied on by hotel '
        'management (including Finance) and must be accurate.', S['body_just']))
    story.append(Paragraph('Doors &amp; entrances', S['h3']))
    story.extend(bullets([
        'Keep external doors secured outside their permitted open hours; never prop a door and leave it;',
        'Log entry and exit activity at all doors and the Queen Street / Lorne Street entrances;',
        'Challenge politely but firmly anyone without a clear, legitimate reason to be on site.',
    ]))
    story.append(Paragraph('Car park (Level 3) — after hours', S['h3']))
    story.extend(bullets([
        'Only open the car park after hours for a legitimate, authorised reason;',
        '<b>Record every after-hours opening</b> — time, reason, and who requested it;',
        'Re-secure immediately after use and check for loiterers or anyone using the area to smoke / use substances.',
    ]))
    story.append(Paragraph('Early-morning deliveries &amp; suppliers', S['h3']))
    story.extend(bullets([
        'Assist suppliers with opening and closing doors / the loading area for early-morning deliveries;',
        'Record the supplier and the <b>time of delivery</b>; remain present while access is open;',
        'Re-secure the loading area and doors immediately once the delivery is complete.',
    ]))
    story.append(Paragraph('Waste Management collection', S['h3']))
    story.extend(bullets([
        'Open the loading area for Waste Management to collect rubbish, and re-secure afterwards;',
        '<b>Record the date and time of every waste collection</b> — Finance has requested an '
        'ongoing log of collection times (initially a two-month history), so this must be '
        'captured consistently on every occasion.',
    ]))
    story.append(callout('Why the times matter',
        'Delivery, waste-collection and car-park-opening times feed directly into hotel '
        'operational and financial records. Treat each as a logged event — a missed time is a '
        'gap in the hotel&#39;s records, not just ours.', accent=GOLD))
    story.append(PageBreak())

    # ── 7. REPORTING ──────────────────────────────────────────────────────────
    story.append(letterhead()); story.append(Spacer(1, 14))
    story.append(Paragraph('SECTION 7', S['tag']))
    story.append(h2('7', 'Reporting &amp; the Shared Drive'))
    story.append(Paragraph(
        'Every shift produces a written report, submitted to the agreed <b>shared drive</b> so '
        'that Radisson RED management has timely visibility. Reports stick to operational and '
        'safety matters relevant to the hotel; ASG internal security tactics are not detailed '
        'in the client-facing report.', S['body_just']))
    story.append(Paragraph('Two levels of reporting', S['h3']))
    story.append(table(
        ['Type', 'When', 'Detail level'],
        [
            ['Brief walk-about notes', 'Every patrol, every shift',
             'Short notes — times, doors checked, entries/exits, car-park openings, '
             'deliveries, waste collection, anything observed of relevance'],
            ['Full incident report', 'Any security or behavioural incident',
             'Detailed: date, time, exact location, who was involved, what was observed, '
             'actions taken, who was notified, and the outcome'],
        ],
        [CW * 0.22, CW * 0.24, CW * 0.54]))
    story.append(Spacer(1, 8))
    story.append(Paragraph('Each nightly report should capture, at minimum', S['h3']))
    story.extend(bullets([
        'Officer name, date and shift times;',
        'Patrol times and a brief note for each walk-about;',
        'Door / entrance activity, including the Queen Street / Lorne Street entrances;',
        'Number of times the car park was opened after hours (with times and reasons);',
        'Early-morning deliveries — supplier and time;',
        'Waste Management collection — date and time;',
        'Any loitering, antisocial behaviour, intoxication or drug-related observation;',
        'Any incident (cross-reference the full incident report);',
        'Anything handed over to the next shift.',
    ], key='bullet_tight'))
    story.append(callout('Standards (per ASG recommendations to Radisson RED)',
        'A formal incident-reporting process means every security or behavioural incident is '
        'logged with date, time, personnel involved, actions taken and outcome. Consistent '
        'records demonstrate the hotel&#39;s compliance with its Health and Safety at Work Act '
        '2015 duty to provide a safe environment for workers and guests.', accent=MID_BLUE))
    story.append(PageBreak())

    # ── 8. TRESPASS ───────────────────────────────────────────────────────────
    story.append(letterhead()); story.append(Spacer(1, 14))
    story.append(Paragraph('SECTION 8  ·  HEADLINE PROCEDURE', S['tag']))
    story.append(h2('8', 'Trespass Authority &amp; Process'))
    story.append(Paragraph(
        'Radisson RED management has asked ASG to facilitate the hotel&#39;s <b>Trespass '
        'Authority</b> — the lawful removal and exclusion of individuals who threaten the '
        'safety, security or good order of the property. ASG officers act as the hotel&#39;s '
        'authorised agents in issuing and enforcing trespass notices, under the '
        '<b>Trespass Act 1980</b>.', S['body_just']))
    story.append(Paragraph('When trespass applies', S['h3']))
    story.extend(bullets([
        'A person has no lawful reason to be on the property and refuses to leave when asked;',
        'A guest or visitor breaches the House Rules or Guest Terms of Stay (e.g. illegal '
        'drug use, antisocial behaviour, property damage, threats);',
        'A previously trespassed individual returns to the property.',
    ]))
    story.append(Paragraph('The process — step by step', S['h3']))
    story.extend(numbered([
        'Notify the <b>Duty Manager</b> and obtain authority to act on the hotel&#39;s behalf '
        '(ASG officers issue trespass as the hotel&#39;s agent).',
        'Where safe, ask the person to leave the property. Stay calm, professional and '
        'non-confrontational; do not use force beyond reasonable lawful authority.',
        'Issue a <b>formal Trespass Notice</b> under the Trespass Act 1980. A notice may be '
        'verbal, but a <b>written notice is strongly recommended for evidential purposes</b> '
        '(see Appendix B).',
        'If there is any immediate threat to safety, or the person refuses to leave, call '
        '<b>NZ Police on 111</b>. For CBD support, the Heart of the City line is <b>09 961 6161</b>.',
        'Record the trespass in the <b>internal trespass register</b>: full name (if known), '
        'photo (if available from CCTV), date of incident, and the reason for trespass.',
        'Flag the individual in the hotel&#39;s <b>property management system (PMS)</b> to '
        'prevent future bookings.',
        'Complete a full incident report and submit it to the shared drive.',
    ]))
    story.append(callout('Once a person is trespassed',
        'If a trespassed individual returns to the property they are <b>committing an offence</b>, '
        'and Police can be called to remove them. Keep the written notice and register entry on '
        'file as evidence.', accent=RED_ACCENT, bg=HexColor('#FBEEEE')))
    story.append(Spacer(1, 4))
    story.append(Paragraph('Register, privacy &amp; multi-site sharing', S['h3']))
    story.extend(bullets([
        'ASG maintains the trespass register on the hotel&#39;s behalf and can assist with '
        'serving notices;',
        'Where ASG covers multiple properties, the register may be shared across sites <b>strictly '
        'for safety and security purposes only</b>, in compliance with the <b>Privacy Act 2020</b>;',
        'Trespass information must never be used for any purpose other than safety and security.',
    ]))
    story.append(PageBreak())

    # ── 9. DRUG USE ───────────────────────────────────────────────────────────
    story.append(letterhead()); story.append(Spacer(1, 14))
    story.append(Paragraph('SECTION 9', S['tag']))
    story.append(h2('9', 'Drug Use — Response Procedure'))
    story.append(Paragraph(
        'Under New Zealand law, hotels are <b>not required to actively search for or police '
        'drug use</b>. However, where staff become aware of drug use, or find drug '
        'paraphernalia, ASG officers follow a clear, lawful procedure.', S['body_just']))
    story.append(Paragraph('If drug use or paraphernalia is observed', S['h3']))
    story.extend(numbered([
        '<b>Do not confront the guest directly.</b> Notify the Duty Manager and ASG / security immediately.',
        'Document the incident in detail — time, location, what was observed, and by whom.',
        'If there is an <b>immediate safety risk</b> to staff or other guests, call <b>Police '
        'on 111</b> without hesitation, and call the <b>HOTC support line 09 961 6161</b> for '
        'immediate CBD support.',
        'Under the <b>Misuse of Drugs Act 1975</b>, the hotel is within its rights to ask a '
        'guest to leave if their behaviour breaches the House Rules or Terms of Stay — where '
        'eviction is required, follow the trespass process in Section 8.',
        'Do <b>not</b> handle any drugs or paraphernalia found in a vacated room — contact '
        'Police to collect.',
    ]))
    story.append(callout('Contractual basis',
        'Radisson RED&#39;s Guest Terms &amp; Conditions should explicitly prohibit illegal drug '
        'use on the premises. This gives a clear contractual basis for eviction if required, '
        'and supports the officer&#39;s actions on the night.', accent=GOLD))
    story.append(Spacer(1, 4))
    story.append(Paragraph('Key reminders', S['h3']))
    story.extend(bullets([
        'Safety first — officer and guest safety always takes priority over confrontation;',
        'Observe and record, escalate to the Duty Manager, and let Police handle anything seized or unlawful;',
        'Never search a person or a room beyond your lawful authority.',
    ]))
    story.append(PageBreak())

    # ── 10. INCIDENT / ESCALATION ─────────────────────────────────────────────
    story.append(letterhead()); story.append(Spacer(1, 14))
    story.append(Paragraph('SECTION 10', S['tag']))
    story.append(h2('10', 'Incident Management &amp; Escalation'))
    story.append(Paragraph('The escalation chain', S['h3']))
    story.append(Paragraph(
        'All staff are trained on a single, consistent escalation path. Move up the chain as '
        'the situation requires — and move straight to Police for any immediate threat to '
        'life or safety.', S['body']))
    story.append(table(
        ['Step', 'Who', 'When'],
        [
            ['1', 'Officer on shift', 'First response — observe, de-escalate, make safe, begin recording'],
            ['2', 'Radisson RED Duty Manager', 'Notify immediately for any guest, trespass, drug or safety matter'],
            ['3', 'ASG security / site supervisor &amp; ASG Operations', 'For security response, backup, and trespass enforcement'],
            ['4', 'NZ Police — 111', 'Immediate threat to safety, refusal to leave, unlawful behaviour, seizure of drugs'],
            ['—', 'Heart of the City — 09 961 6161', 'CBD safety support, in parallel with the above'],
        ],
        [CW * 0.08, CW * 0.42, CW * 0.50]))
    story.append(Spacer(1, 10))
    story.append(Paragraph('Every incident', S['h3']))
    story.extend(bullets([
        'Is logged with date, time, personnel involved, actions taken and outcome;',
        'Is written up as a full incident report and submitted to the shared drive;',
        'Is handed over to the next shift and the Duty Manager if still open;',
        'Feeds a <b>quarterly review</b> between ASG and Radisson RED to spot trends and adjust '
        'coverage or procedures.',
    ]))
    story.append(callout('Decision rule',
        'If a situation involves an immediate risk to anyone&#39;s safety, call 111 first, then '
        'notify the Duty Manager and ASG. Documentation always follows — but it never delays '
        'protecting people.', accent=RED_ACCENT, bg=HexColor('#FBEEEE')))
    story.append(PageBreak())

    # ── 11. COMPLIANCE ────────────────────────────────────────────────────────
    story.append(letterhead()); story.append(Spacer(1, 14))
    story.append(Paragraph('SECTION 11', S['tag']))
    story.append(h2('11', 'Legislative &amp; Compliance Framework'))
    story.append(Paragraph(
        'ASG officers operate within New Zealand law at all times. The following framework '
        'underpins this SOP:', S['body']))
    story.append(table(
        ['Instrument', 'Relevance to this SOP'],
        [
            ['Trespass Act 1980', 'Authority to issue trespass notices and exclude individuals; offence to return once trespassed'],
            ['Misuse of Drugs Act 1975', 'Basis for asking guests to leave where behaviour breaches the Terms of Stay; Police handle any drugs found'],
            ['Privacy Act 2020', 'Trespass register and any cross-site sharing used solely for safety and security purposes'],
            ['Health and Safety at Work Act 2015', 'Hotel&#39;s duty to provide a safe environment for workers and guests; documented processes evidence compliance'],
            ['Private Security Personnel &amp; Private Investigators Act 2010',
             'ASG and its officers hold current COA licences; officers carry and produce ID on request'],
            ['Radisson RED House Rules &amp; Guest Terms of Stay',
             'Contractual basis for conduct standards and eviction; reviewed annually to cover current risks'],
        ],
        [CW * 0.34, CW * 0.66]))
    story.append(Spacer(1, 10))
    story.append(callout('Annual review',
        'Radisson RED&#39;s House Rules and Guest Terms of Stay should be reviewed at least '
        'annually to ensure they cover current risks — drugs, antisocial behaviour and '
        'property damage. ASG is available to support that review and to refresh team training.',
        accent=MID_BLUE))
    story.append(PageBreak())

    # ── 12. CONTACTS QUICK REF ────────────────────────────────────────────────
    story.append(letterhead()); story.append(Spacer(1, 14))
    story.append(Paragraph('SECTION 12  ·  QUICK REFERENCE', S['tag']))
    story.append(h2('12', 'Emergency &amp; Escalation Contacts'))
    story.append(table(
        ['Situation', 'Call', 'Number'],
        [
            ['Immediate threat to life or safety', 'NZ Police / Emergency', '111'],
            ['CBD safety support', 'Heart of the City (HOTC)', '09 961 6161'],
            ['On-shift escalation', 'Radisson RED Duty Manager', 'Front desk / radio'],
            ['People &amp; Culture matters', 'Parijata Moeava', '+64 290 400 4504'],
            ['Finance / reporting queries', 'Nileshni Chand (Nila)', '+64 290 400 4505'],
            ['ASG — primary contact', 'Hasi Nabawi — ASG', '020 4007 9904'],
            ['ASG account owner', 'Ahmad Duais, CEO — ASG', '09 950 4640 / 021 0850 0009'],
            ['ASG operational support', 'ASG Operations (24/7)', 'ASG control room'],
        ],
        [CW * 0.42, CW * 0.34, CW * 0.24]))
    story.append(Spacer(1, 14))
    story.append(callout('Print &amp; post',
        'This quick-reference table should be printed and kept at the ASG post for fast access. '
        'Verify all numbers with the ASG site supervisor and update if they change.', accent=GOLD))
    story.append(PageBreak())

    # ── APPENDIX A ────────────────────────────────────────────────────────────
    story.append(letterhead()); story.append(Spacer(1, 14))
    story.append(Paragraph('APPENDIX A', S['tag']))
    story.append(h2('A', 'Nightly Shift Report Template'))
    story.append(Paragraph('Officers complete and submit to the shared drive before sign-off.', S['body']))
    story.append(table(
        ['Field', 'Entry'],
        [
            ['Officer name', ''],
            ['Date', ''],
            ['Shift start / finish', ''],
            ['Duty Manager on shift', ''],
            ['Handover received (flags / open issues)', ''],
            ['Patrol 1 — time &amp; notes', ''],
            ['Patrol 2 — time &amp; notes', ''],
            ['Patrol 3 — time &amp; notes', ''],
            ['Additional patrols', ''],
            ['Door / entrance activity (incl. Queen St)', ''],
            ['Car park opened after hours? (times / reasons)', ''],
            ['Early-morning deliveries (supplier &amp; time)', ''],
            ['Waste Management collection (date &amp; time)', ''],
            ['Loitering / antisocial / drug observations', ''],
            ['Incidents (cross-ref incident report no.)', ''],
            ['Trespass notices issued', ''],
            ['Handover to next shift', ''],
        ],
        [CW * 0.42, CW * 0.58]))
    story.append(PageBreak())

    # ── APPENDIX B ────────────────────────────────────────────────────────────
    story.append(letterhead()); story.append(Spacer(1, 14))
    story.append(Paragraph('APPENDIX B', S['tag']))
    story.append(h2('B', 'Trespass Register &amp; Notice Checklist'))
    story.append(Paragraph('Trespass register — fields captured for each entry', S['h3']))
    story.append(table(
        ['Field', 'Detail'],
        [
            ['Full name of individual', '(if known)'],
            ['Photo', '(if available from CCTV)'],
            ['Date of incident', ''],
            ['Location on property', ''],
            ['Reason for trespass', ''],
            ['Notice type', 'Verbal / Written (written strongly recommended)'],
            ['Issued by (officer)', ''],
            ['Duty Manager authorising', ''],
            ['Police involved? (event / ref no.)', ''],
            ['Flagged in PMS?', 'Yes / No'],
            ['Incident report reference', ''],
        ],
        [CW * 0.40, CW * 0.60]))
    story.append(Spacer(1, 12))
    story.append(Paragraph('Issuing a Trespass Notice — checklist', S['h3']))
    story.extend(numbered([
        'Duty Manager notified and authority to act confirmed;',
        'Person asked to leave (where safe to do so);',
        'Written Trespass Notice completed and served (verbal recorded if written not possible);',
        'Police called if immediate threat or refusal to leave (111);',
        'Register entry completed with all fields above;',
        'Individual flagged in PMS to block future bookings;',
        'Full incident report written and uploaded to the shared drive.',
    ]))
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width='100%', thickness=0.6, color=BORDER))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        '<i>Prepared by Absolute Security Group Limited. This is a draft SOP for review and '
        'sign-off by Radisson RED Auckland management. Once approved, it will be issued to all '
        'ASG officers deployed on site and reviewed annually or after any significant incident.</i>',
        S['small']))

    doc.build(story, onFirstPage=_cover, onLaterPages=_footer)
    print('Wrote', OUT)


if __name__ == '__main__':
    build()
