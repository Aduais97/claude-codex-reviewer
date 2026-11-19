#!/usr/bin/env python3
"""
ASG Security | PB Tech Case Studies Addendum (editable Word).
Built at PB Tech's direct request for named clients and case studies
(Kenny feedback 24 Oct 2026 + Ahmad's brief). ETR round 5 hardened:
Codex gpt-5.6-terra + 4 Claude lenses (confidentiality, buyer-skeptic,
NZ privacy-law, anti-slop); ~70 findings applied.
HARD GATE: carries a red DO-NOT-SEND banner until per-client disclosure
consents are confirmed (HOTC, Woolworths NZ, Bunnings, Mitre 10, Viaduct/Tramco).
No em-dashes. No rates. No per-client dollar figures.
Output: ~/Desktop/ASG/Sales & Marketing/Proposals/PBTech_Client_Case_Studies_Addendum.docx
"""
import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.oxml import OxmlElement
from docx.shared import Mm, Pt, RGBColor

MIDNIGHT = RGBColor(0x05, 0x0A, 0x14)
SIGNAL = RGBColor(0x25, 0x63, 0xEB)
SLATE = RGBColor(0x33, 0x41, 0x55)
GRAY_500 = RGBColor(0x64, 0x74, 0x8B)
RED = RGBColor(0xDC, 0x26, 0x26)
BODY_FONT = 'Arial'

OUT = Path.home() / 'Desktop/ASG/Sales & Marketing/Proposals/PBTech_Client_Case_Studies_Addendum.docx'


def add_runs(p, text, base_color=SLATE, size=10, bold_color=MIDNIGHT):
    for chunk in re.split(r'(<b>.*?</b>)', text, flags=re.S):
        if not chunk:
            continue
        bold = chunk.startswith('<b>')
        seg = re.sub(r'</?b>', '', chunk)
        r = p.add_run(seg)
        r.bold = bold
        r.font.name = BODY_FONT
        r.font.size = Pt(size)
        r.font.color.rgb = bold_color if bold else base_color
    return p


def body(doc, text, size=10, space_after=5):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.12
    return add_runs(p, text, size=size)


def bullet(doc, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.12
    return add_runs(p, text)


def section_head(doc, number, title, space_before=14):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(f'{number}  ')
    r.bold = True
    r.font.name = BODY_FONT
    r.font.size = Pt(15)
    r.font.color.rgb = SIGNAL
    r2 = p.add_run(title)
    r2.bold = True
    r2.font.name = BODY_FONT
    r2.font.size = Pt(15)
    r2.font.color.rgb = MIDNIGHT


def label(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text)
    r.bold = True
    r.font.name = BODY_FONT
    r.font.size = Pt(10.5)
    r.font.color.rgb = MIDNIGHT


def main():
    doc = Document()
    for sec in doc.sections:
        sec.page_width, sec.page_height = Mm(210), Mm(297)
        sec.top_margin = sec.bottom_margin = Mm(16)
        sec.left_margin = sec.right_margin = Mm(18)

    # Red internal gate banner (delete before sending)
    p = doc.add_paragraph()
    r = p.add_run('INTERNAL DRAFT. DELETE THIS LINE BEFORE SENDING. Do not release '
                  'until disclosure consent is confirmed for every named client: '
                  'Heart of the City, Woolworths NZ, Bunnings, Mitre 10, Viaduct Harbour.')
    r.bold = True
    r.font.name = BODY_FONT
    r.font.size = Pt(9)
    r.font.color.rgb = RED
    p.paragraph_format.space_after = Pt(10)

    # Title block
    p = doc.add_paragraph()
    r = p.add_run('THE WORK BEHIND THE PROPOSAL')
    r.bold = True
    r.font.name = BODY_FONT
    r.font.size = Pt(24)
    r.font.color.rgb = MIDNIGHT
    p.paragraph_format.space_after = Pt(2)
    p = doc.add_paragraph()
    r = p.add_run('Client case studies  |  ASG Security for PB Technologies  |  '
                  'Addendum to the Integrated Security Partnership proposal  |  October 2026')
    r.font.name = BODY_FONT
    r.font.size = Pt(10)
    r.font.color.rgb = GRAY_500
    p.paragraph_format.space_after = Pt(10)

    body(doc, 'PB Tech asked to see the work behind the capability claims. Below are three '
              'named engagements and one confidential programme. Where results are quoted they '
              'come from client-run surveys or from the reconciled weekly reporting those clients '
              'receive. One rule applies throughout: <b>we describe no client’s security '
              'posture in detail, in this document or any other. PB Tech’s would be treated '
              'the same.</b>')

    # 01 HOTC
    section_head(doc, '01', 'Heart of the City, Auckland')
    body(doc, 'Auckland’s city centre business association, representing around 15,000 '
              'businesses and property owners.', size=9.5)
    label(doc, 'The challenge')
    body(doc, 'City centre businesses deal with daily anti-social behaviour, aggression toward '
              'staff and theft, in an environment shaped by forces far beyond any one patrol. '
              'The association invests around $1.3 million a year in city centre security '
              'patrols, and the programme was topped up with central government Proceeds of '
              'Crime funding in 2025.')
    label(doc, 'What we deliver')
    body(doc, 'ASG operates the Heart of the City Safety Team: a 24/7 foot patrol across the '
              'Queen Street Valley that responds to business calls, de-escalates aggression, '
              'attends vagrancy-related callouts and works alongside Police, St John and '
              'Auckland Council’s compliance wardens. The programme has run continuously '
              'since early 2024.')
    label(doc, 'The results')
    bullet(doc, 'The association’s September 2026 member survey: <b>95.1% of businesses rate '
                'the Safety Team very or extremely valuable</b>, up from 76.9% a year earlier. '
                '<b>80.5% feel very or extremely well supported</b>, up from 69.2%. The share who '
                'did not know how to contact the team fell from 56.4% to 25.0%, with survey '
                'participation more than doubling.')
    bullet(doc, 'July to September 2026 workload: <b>607 business calls responded</b>, 168 '
                'aggressive-behaviour incidents managed, 107 theft incidents and 302 '
                'vagrancy-related responses.')
    bullet(doc, 'Our patrol logs record <b>zero use of force across every aggression incident</b> '
                'in the life of the contract. The logs are open to client audit.')
    body(doc, '<b>For PB Tech:</b> aggression management and staff duty of care, measured by the '
              'client’s own survey.')

    # 02 Covert LP
    section_head(doc, '02', 'National covert loss prevention: Woolworths NZ and Bunnings')
    label(doc, 'The challenge')
    body(doc, 'Organised retail crime: repeat offenders working across branches and regions, '
              'aggression when confronted, and losses concentrated in compact, high-resale stock.')
    label(doc, 'What we deliver')
    body(doc, 'SLS Retail Theft Control, ASG Group’s specialist covert loss prevention '
              'company, runs covert programmes across more than 100 retail sites nationally for '
              'Woolworths NZ and Bunnings, with a store-level programme for Mitre 10. '
              'Plainclothes teams, never deployed solo, identify and document offending: no '
              'detention beyond citizen’s arrest powers, trespass served under each '
              'client’s authority as occupier, and structured evidence packs prepared for '
              'Police consideration. Operatives are trained on the retail crime intelligence '
              'platforms our clients use and contribute structured intelligence under each '
              'client’s own procedures. For repeat-offender hotspots we run coordinated '
              'covert deployments, including in support of Police operations: our team detects '
              'concealment, theft and aggression in store and passes real-time information to '
              'Police, who make all apprehension decisions.')
    body(doc, 'For PB Tech the model gets stronger, not weaker: serialised stock means recovered '
              'product is traceable and evidence packs tie offender to item, and the same covert '
              'methodology extends to click-and-collect abuse and refund and warranty fraud.')
    label(doc, 'The results')
    body(doc, '<b>More than $1 million in verified recoveries since July 2025</b> across the '
              'covert portfolio: recovered product itemised in the weekly report each client '
              'receives, with every billed hour reconciled to timeclock records. Per-client '
              'detail is available in reference calls with each client’s consent, and a '
              'redacted sample weekly report is available on request.')
    body(doc, '<b>For PB Tech:</b> the organised-crime, high-value-stock problem set in the main '
              'proposal, already handled at national scale.')

    # 03 FRT/LPR
    section_head(doc, '03', 'Inside client FRT and LPR programmes (clients not named)')
    body(doc, 'Client facial recognition and licence plate recognition programmes are '
              'commercially confidential and the clients control all disclosure, so we do not '
              'name them here, and no connection should be inferred to any client named '
              'elsewhere in this document. That is the same discipline PB Tech’s systems '
              'would receive.', size=9.5)
    label(doc, 'The challenge')
    body(doc, 'Acting on FRT alerts lawfully takes a trained floor team operating under the '
              'Biometric Processing Privacy Code 2025, fully in force since August 2026. The '
              'camera is the easy part.')
    label(doc, 'What we deliver')
    body(doc, 'ASG teams work inside retail clients’ FRT and LPR standard operating '
              'procedures, acting as each client’s agent under section 11 of the Privacy '
              'Act 2020: the client remains the responsible agency, owns the system, the '
              'watchlist and the privacy impact assessment, and we provide the trained human '
              'layer its safeguards depend on. The client’s own match-verification '
              'procedure runs first; our officer independently confirms the person and the '
              'observed behaviour on the floor before any approach. Alerts are observation '
              'triggers, never grounds for immediate action, consistent with the safeguards the '
              'Privacy Commissioner relied on when the 2025 supermarket FRT inquiry found that '
              'trial compliant. We prepare verified, narrative-supported incident documentation '
              'for the client to assess against its own enrolment criteria: enrolment decisions '
              'stay with the client, and we never enrol individuals, alter watchlists or retain '
              'images. LPR sits outside the Biometric Code, since a plate identifies a vehicle '
              'rather than a person, but remains personal information under the Privacy Act '
              '2020, so alerts run under each client’s CCTV procedures: signage, retention '
              'limits and logged access.')
    body(doc, '<b>Verification:</b> the client’s privacy office can confirm the arrangement '
              'in a reference call under NDA.')
    body(doc, '<b>For PB Tech:</b> Section 4 of the main proposal offers a gated FRT and LPR '
              'capability. For our teams it is current practice, not a roadmap.')

    # 04 Viaduct
    section_head(doc, '04', 'Viaduct Harbour, Auckland: AI monitoring plus human response')
    label(doc, 'The challenge')
    body(doc, 'A 70-berth marina taking vessels up to 60 metres, in a precinct whose value rests '
              'on feeling safe and open. The brief is round-the-clock protection without a '
              'visible security presence.')
    label(doc, 'What we deliver')
    body(doc, 'ASG protects the berth and vessel portfolio at Auckland’s Viaduct Harbour '
              'with continuous AI-assisted camera monitoring (intrusion detection, not facial '
              'recognition), real-time alerting, and an on-site patrol team that verifies and '
              'attends immediately. Coverage is continuous and deliberately discreet, matched '
              'to the precinct’s brand.')
    body(doc, '<b>Verification:</b> engagement tenure and response-time performance are '
              'contractual and available in the reference call.')
    body(doc, '<b>For PB Tech:</b> after-hours intrusion at a marina is the same problem as '
              'after-hours intrusion at a store full of portable, high-value stock. This is the '
              'proposed monitoring stack, AI detection, human verification and immediate '
              'physical response, running as one system today.')

    # Verification table
    section_head(doc, '05', 'How to verify each claim')
    table = doc.add_table(rows=5, cols=3)
    table.style = 'Table Grid'
    headers = ['Case study', 'Proves', 'How PB Tech verifies it']
    rows = [
        ('Heart of the City', 'Aggression management, duty of care',
         'Client’s own member survey; reference call'),
        ('Covert loss prevention', 'ORC response, verified recoveries',
         'Reference calls; redacted sample weekly report'),
        ('FRT and LPR operations', 'The gated vision-systems path is current practice',
         'Reference call under NDA with the client’s privacy office'),
        ('Viaduct Harbour', 'AI monitoring integrated with physical response',
         'Reference call; contractual response-time data'),
    ]
    for j, h in enumerate(headers):
        cell = table.rows[0].cells[j]
        cell._tc.get_or_add_tcPr().append(
            parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:fill="050A14"/>'))
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = BODY_FONT
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    for i, row in enumerate(rows, start=1):
        for j, val in enumerate(row):
            p = table.rows[i].cells[j].paragraphs[0]
            r = p.add_run(val)
            r.bold = (j == 0)
            r.font.name = BODY_FONT
            r.font.size = Pt(9.5)
            r.font.color.rgb = MIDNIGHT if j == 0 else SLATE

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    add_runs(p, '<b>The fastest verification is the Section 8 pilot:</b> the weekly report '
                'PB Tech receives in week one is the same artefact these clients receive today. '
                'Client references are available on request, with each client’s consent.')

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    r = p.add_run('ASG Security  |  Ahmad Duais, Chief Executive  |  '
                  'ahmad@absolutesecuritygroup.co.nz  |  absolutesecuritygroup.co.nz  |  slsrtc.co.nz')
    r.font.name = BODY_FONT
    r.font.size = Pt(8.5)
    r.font.color.rgb = GRAY_500

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    main()
