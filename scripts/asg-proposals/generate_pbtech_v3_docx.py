#!/usr/bin/env python3
"""
ASG Security | PB Tech 3.0: Integrated Security Partnership (editable Word).
Blends the v1 proposal context (owner-liked) with the 2.0 services-showcase
format, whole-group framing, and the owner-requested FRT + LPR + AI section
(in place of the covert operating-model section the owner removed from 2.0).
ETR round 4 hardened (Codex + privacy-vision + buyer-antislop + GSD lenses).
No em-dashes. No rates. Verified claims + owner-approved overrides only.
Output: ~/Desktop/ASG/Sales & Marketing/Proposals/PBTech_Integrated_Security_Partnership_3.0.docx
"""
import re
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Mm, Pt, RGBColor

MIDNIGHT = RGBColor(0x05, 0x0A, 0x14)
SIGNAL = RGBColor(0x25, 0x63, 0xEB)
SLATE = RGBColor(0x33, 0x41, 0x55)
GRAY_400 = RGBColor(0x94, 0xA3, 0xB8)
GRAY_500 = RGBColor(0x64, 0x74, 0x8B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BODY_FONT = 'Arial'
MONO_FONT = 'Consolas'

OUT = Path.home() / 'Desktop/ASG/Sales & Marketing/Proposals/PBTech_Integrated_Security_Partnership_3.0.docx'
TEAM_PHOTO = Path(__file__).parent / 'assets/asg_leadership_team.png'


def shade(cell, hexfill):
    cell._tc.get_or_add_tcPr().append(
        parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:fill="{hexfill}"/>'))


def set_borders(table, edges, size=4, color='E2E8F0'):
    tbl_pr = table._tbl.tblPr
    borders = OxmlElement('w:tblBorders')
    for edge in edges:
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), str(size))
        el.set(qn('w:color'), color)
        borders.append(el)
    tbl_pr.append(borders)


def add_runs(p, text, base_color=SLATE, size=10, font=BODY_FONT):
    text = text.replace('&amp;', '&')
    for chunk in re.split(r'(<b>.*?</b>)', text, flags=re.S):
        if not chunk:
            continue
        bold = chunk.startswith('<b>')
        seg = re.sub(r'</?b>', '', chunk)
        r = p.add_run(seg)
        r.bold = bold
        r.font.name = font
        r.font.size = Pt(size)
        r.font.color.rgb = MIDNIGHT if bold else base_color
    return p


def body(doc, text, size=10):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.12
    return add_runs(p, text, size=size)


def bullet(doc, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.12
    return add_runs(p, text)


def overline(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(' '.join(text.upper()))
    r.bold = True
    r.font.name = BODY_FONT
    r.font.size = Pt(8)
    r.font.color.rgb = SIGNAL
    return p


def heading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True
    r.font.name = BODY_FONT
    r.font.size = Pt(15)
    r.font.color.rgb = MIDNIGHT
    return p


def cell_text(cell, runs, align=None):
    p = cell.paragraphs[0]
    if align:
        p.alignment = align
    for text, kw in runs:
        r = p.add_run(text)
        r.bold = kw.get('bold', False)
        r.font.name = kw.get('font', BODY_FONT)
        r.font.size = Pt(kw.get('size', 9))
        r.font.color.rgb = kw.get('color', SLATE)
    return p


def dark_block(doc, paras):
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    cell = t.cell(0, 0)
    cell.width = Mm(172)
    shade(cell, '050A14')
    set_borders(t, ['top', 'left', 'bottom', 'right'], size=4, color='050A14')
    first = True
    for runs, kw in paras:
        p = cell.paragraphs[0] if first else cell.add_paragraph()
        first = False
        p.paragraph_format.space_before = Pt(kw.get('before', 0))
        p.paragraph_format.space_after = Pt(kw.get('after', 4))
        if kw.get('tab'):
            p.paragraph_format.tab_stops.add_tab_stop(Mm(165), WD_TAB_ALIGNMENT.RIGHT)
        for text, rkw in runs:
            r = p.add_run(text)
            r.bold = rkw.get('bold', False)
            r.font.name = BODY_FONT
            r.font.size = Pt(rkw.get('size', 10))
            r.font.color.rgb = rkw.get('color', GRAY_400)
    return t


def stat_strip(doc):
    stats = [
        ('350+', 'security professionals group-wide'),
        ('$1M+', 'verified recoveries since Jul 2025'),
        ('100+', 'retail sites under covert LP'),
        ('Since 2006', 'SLS RTC protecting NZ retail'),
    ]
    t = doc.add_table(rows=2, cols=4)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for row in t.rows:
        for c in row.cells:
            c.width = Mm(43)
    set_borders(t, ['top', 'bottom'], size=6, color='E2E8F0')
    for i, (num, label) in enumerate(stats):
        pn = t.cell(0, i).paragraphs[0]
        pn.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pn.paragraph_format.space_before = Pt(6)
        r = pn.add_run(num)
        r.bold = True; r.font.name = MONO_FONT; r.font.size = Pt(14); r.font.color.rgb = MIDNIGHT
        pl = t.cell(1, i).paragraphs[0]
        pl.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pl.paragraph_format.space_after = Pt(6)
        r = pl.add_run(label)
        r.font.name = BODY_FONT; r.font.size = Pt(8); r.font.color.rgb = GRAY_500


def tile_grid(doc, tiles, cols=2):
    rows = (len(tiles) + cols - 1) // cols
    t = doc.add_table(rows=rows, cols=cols)
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_borders(t, ['top', 'left', 'bottom', 'right', 'insideH', 'insideV'], size=4, color='E2E8F0')
    for idx, (title, text) in enumerate(tiles):
        cell = t.cell(idx // cols, idx % cols)
        cell.width = Mm(86)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(3)
        r = p.add_run(title)
        r.bold = True; r.font.name = BODY_FONT; r.font.size = Pt(9.5); r.font.color.rgb = MIDNIGHT
        p2 = cell.add_paragraph()
        p2.paragraph_format.space_after = Pt(3)
        r = p2.add_run(text)
        r.font.name = BODY_FONT; r.font.size = Pt(8.5); r.font.color.rgb = SLATE
    return t


def layer_card(doc, code, title, text, chips):
    t = doc.add_table(rows=1, cols=2)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    set_borders(t, ['top', 'left', 'bottom', 'right'], size=4, color='E2E8F0')
    badge, main = t.cell(0, 0), t.cell(0, 1)
    badge.width = Mm(14)
    main.width = Mm(158)
    shade(badge, '050A14')
    cell_text(badge, [(code, dict(bold=True, size=10, color=WHITE))], align=WD_ALIGN_PARAGRAPH.CENTER)
    p = main.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    r = p.add_run(title)
    r.bold = True; r.font.name = BODY_FONT; r.font.size = Pt(10.5); r.font.color.rgb = MIDNIGHT
    p2 = main.add_paragraph()
    add_runs(p2, text, size=9)
    p3 = main.add_paragraph()
    p3.paragraph_format.space_after = Pt(2)
    r = p3.add_run('  ·  '.join(chips))
    r.font.name = BODY_FONT; r.font.size = Pt(8); r.font.color.rgb = GRAY_500
    doc.add_paragraph().paragraph_format.space_after = Pt(1)


def main():
    doc = Document()
    doc.core_properties.title = 'PB Tech: Integrated Security Partnership 3.0'
    doc.core_properties.author = 'ASG Security'
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(19)
    sec.top_margin, sec.bottom_margin = Mm(20), Mm(18)
    style = doc.styles['Normal']
    style.font.name = BODY_FONT
    style.font.size = Pt(10)
    style.font.color.rgb = SLATE

    # Cover
    dark_block(doc, [
        ([('ASG', dict(bold=True, size=14, color=WHITE)), ('  |  ', dict(size=12, color=GRAY_500)),
          ('S E C U R I T Y', dict(size=10)), ('\t', dict()), ('Complete Security. One Partner.', dict(size=8.5))],
         dict(before=14, after=16, tab=True)),
        ([('I N T E G R A T E D   S E C U R I T Y   P A R T N E R S H I P', dict(bold=True, size=8.5, color=SIGNAL))], dict(after=4)),
        ([('Security, Loss Prevention and Intelligence', dict(bold=True, size=22, color=WHITE))], dict(after=6)),
        ([('Covert loss prevention, uniformed guarding, electronic security, monitoring, vision systems '
           'and intelligence-led reporting for one of New Zealand’s largest technology retailers.',
           dict(size=10.5))], dict(after=10)),
        ([('Prepared for PB Technologies Ltd    ·    Issued 22 October 2026    ·    Commercial in confidence',
           dict(size=9.5))], dict(after=2)),
        ([('Absolute Security Group  &  SLS Retail Theft Control', dict(size=9.5))], dict(after=14)),
    ])
    doc.add_paragraph().paragraph_format.space_after = Pt(1)
    stat_strip(doc)

    # 1 — One partner
    overline(doc, 'The partnership')
    heading(doc, 'One partner, every store')
    body(doc, 'Security for a nationwide retail network is usually bought as three separate services: '
              'guarding from one vendor, alarm monitoring from another, loss prevention from a third, none '
              'of which share data. The gaps between vendors are where loss happens. ASG Group runs all of '
              'it as one partnership: <b>one vendor, one SLA, one weekly report, every store.</b> Absolute '
              'Security Group Ltd contracts as head contractor, with SLS Retail Theft Control delivering '
              'covert LP under it: one counterparty, one invoice.')
    body(doc, '<b>Who we are.</b> ASG Group is New Zealand-owned. Its covert loss-prevention arm, '
              '<b>SLS Retail Theft Control</b>, has protected NZ retail continuously since 2006 and joined '
              'the group in 2025, alongside <b>Absolute Security Group Ltd</b>, which delivers uniformed '
              'guarding, precinct patrol, CCTV monitoring and electronic security. 350+ security '
              'professionals on active rosters group-wide, with offices in Auckland, Waikato, Wellington '
              'and Christchurch, working every day inside national retail networks across grocery, '
              'hardware and general merchandise, alongside precinct, education, hospitality, property and '
              'corporate work. Client data is strictly siloed, never cross-shared, and a dedicated PB Tech '
              'team with contractual information barriers is part of this offer.')

    # 2 — The challenge
    overline(doc, 'The challenge')
    heading(doc, 'Technology retail faces unique risks')
    body(doc, 'Laptops, phones, components and accessories are compact, high-value and quick to resell. '
              'That stock profile shapes four risks every technology retailer manages daily:')
    tile_grid(doc, [
        ('Organised retail crime', 'Repeat offenders working across branches, with the same group appearing '
         'at different stores in the same week.'),
        ('Aggression at counters', 'Staff face anti-social behaviour, verbal abuse and physical threats, '
         'raising duty-of-care obligations as well as morale costs.'),
        ('After-hours attack', 'Stores and warehouses holding resaleable stock carry a standing burglary '
         'and ram-raid exposure outside trading hours.'),
        ('Fraud channels', 'Refund and warranty fraud, click-and-collect abuse and internal loss patterns '
         'that pure door security never sees.'),
    ])
    body(doc, 'Compact, serialised, high-resale stock is consistently among the most targeted categories '
              'across our own covert portfolio. The pilot in Section 8 puts the economics to the test on '
              'your own stores.')

    # 3 — Service lines
    overline(doc, 'Our service lines')
    heading(doc, 'Five capabilities, one provider')
    body(doc, 'Covert operatives recover stock before it leaves the store. Uniformed officers hold the '
              'entry and the counter. Electronic systems and monitoring cover the hours nobody is on the '
              'floor. And one weekly dataset decides where all of it sits (Section 6). The companion '
              'proposal configures these capabilities specifically for PB Tech.')
    layer_card(doc, 'LP', 'Covert Loss Prevention',
               'Plain-clothes operatives blend with customers in minimum two-person teams, giving a '
               'corroborating witness at every event. They identify, monitor and engage offenders where it '
               'is safe and lawful, recovering stock before it leaves the store. Our staff claim no '
               'detention powers beyond any citizen’s, and trespass action is taken only as PB Tech’s '
               'authorised agent under SOPs agreed before day one.',
               ['Floor-walking', '2-person teams', 'Crime-intelligence trained', 'Real-time reporting'])
    layer_card(doc, 'UG', 'Uniformed Guarding and Precinct Operations',
               'Visible, professional officers for stores, service centres, distribution sites and '
               'corporate offices. They deter opportunistic theft, de-escalate counter aggression, serve '
               'trespass notices as PB Tech’s authorised agent, and respond to duress activations under '
               'the agreed protocol.',
               ['Visible deterrent', 'Entry control', 'Duress response', 'De-escalation'])
    layer_card(doc, 'ES', 'Electronic Security Systems',
               'EAS theft-detection gates (RF and AM) calibrated for high-traffic retail; product '
               'protection tagging (hard tags, cable locks, spider wraps) for laptops, phones and '
               'high-risk lines; alarmed display protection that keeps demonstration devices open to '
               'customers; bollards, secure fixtures and access control for stock and service-centre '
               'custody areas. We integrate with your existing camera estate first and specify new '
               'hardware only where coverage gaps create risk; supply, installation and servicing are '
               'in-house, and the Mosquito anti-loitering system is available where exterior congregation '
               'is a problem.',
               ['EAS gates', 'Product tagging', 'Display alarms', 'CCTV', 'Anti-theft infrastructure'])
    layer_card(doc, 'MN', 'Monitoring and Alarm Response',
               'Around-the-clock monitoring of alarm activations with AI video verification: automated '
               'detection flags and ranks events, and trained operators review footage and confirm before '
               'any dispatch. An agreed response protocol sits behind every event, backed by patrol or '
               'keyholder attendance.',
               ['24/7 monitoring', 'Operator-confirmed verification', 'Alarm response', 'Camera health'])
    body(doc, '<b>Specialist support.</b> Investigations and Intelligence (internal investigations, '
              'serialised-stock tracing, refund and warranty fraud, click-and-collect fraud screening) '
              'and Surge and Event Support (launch-day crowd management, promotional peaks, multi-store '
              'simultaneous activation across regions).')

    # 4 — Vision systems
    overline(doc, 'Vision systems')
    heading(doc, 'Facial recognition, licence plate recognition and AI capability')
    body(doc, 'PB Tech already owns most of the hardware this needs: LPR can run on existing cameras '
              'where image quality allows, and facial recognition is lawful in New Zealand retail only '
              'inside the Biometric Processing Privacy Code 2025. Our position on both is the same: '
              'staged, governed and human-verified.')
    body(doc, '<b>Facial recognition (gated).</b> The payoff is early warning: your highest-harm repeat '
              'offenders identified at the door, before staff are exposed, not after the event on review '
              'footage. Watchlist alerting is limited to serious, formally trespassed repeat offenders '
              'under a written watchlist policy: eligibility evidence, person-by-person PB Tech approval, '
              'no minors or vulnerable persons, scheduled review, a challenge and correction process, and '
              'entries lapsing automatically with the two-year trespass warning. The system is specified '
              'so that non-matches are discarded at the point of comparison and never stored; both '
              'controls are contractual, verified at commissioning and auditable. Every alert is verified '
              'by a human operator before any floor response; no action is ever taken on an automated '
              'match alone. Clear signage at every FRT-enabled entrance and published customer information '
              'go live before the first camera does, as the Code’s notice rules require. FRT is biometric '
              'processing under the Code, so a documented necessity and proportionality assessment comes '
              'first, any trial runs against pre-agreed accuracy, fairness, deletion and stop criteria, '
              'and PB Tech holds the go, scale or stop decision throughout. If the assessment does not '
              'support it, we do not run it.')
    body(doc, '<b>Licence plate recognition (carpark and perimeter).</b> Offenders arrive by vehicle, and '
              'a plate is often readable before a face. LPR on carpark entries can give the on-site team '
              'and the monitoring centre earlier notice when a vehicle on the watchlist arrives, where '
              'camera placement and plate readability support it; compatibility with your existing '
              'cameras is confirmed in the Phase 0 survey. <b>A plate identifies a vehicle, not a '
              'person:</b> an LPR alert triggers observation and monitoring review only, and no approach, '
              'trespass action or Police call is made on a plate match alone. Watchlist entries are '
              'approved by PB Tech against a documented evidential threshold, carry a fixed expiry, and '
              'are removed on sale, error or staleness, with an accuracy check recorded before any entry '
              'is acted on. Number plates are not biometric information, so LPR sits under the Privacy '
              'Act 2020 rather than the Biometric Code, and we run it with the same discipline: carpark '
              'signage and an updated privacy statement before the first read is collected; retention '
              'fixed and documented in the Phase 0 privacy scoping, with non-match reads purged on a '
              'cycle measured in days, not months; role-based access with audit logs; no standing Police '
              'access, with each disclosure assessed and recorded by an authorised decision-maker in a '
              'disclosure register.')
    body(doc, '<b>AI capability: today and next.</b> Today: automated detection flags and ranks alarm '
              'events, trained operators review footage and confirm before any dispatch, and camera-health '
              'monitoring treats a dead camera as an event to fix, not background noise. No automated '
              'action is ever taken on an AI output alone, today or in anything we roll out later. Next, '
              'staged: detection models extended to more event types on the same flag-and-confirm rule, '
              'and LPR alerts, incident records, severity grading and recovery data feeding one picture '
              'per store. All vision alerts route to our 24/7 monitoring centre; after hours, a confirmed '
              'LPR or video alert triggers the same response protocol as an alarm activation (patrol '
              'dispatch, keyholder contact or Police) and is logged against the same SLA.')
    body(doc, '<b>Governance spine.</b> Every vision capability ships with the same controls: defined '
              'purpose, signage and published customer information before go-live, privacy assessment '
              'where required, human verification before any response, a correction pathway for anyone '
              'misidentified, audit logging, and PB Tech sign-off. Where existing cameras do not meet LPR '
              'image requirements, replacements are specified in the Phase 0 survey and quoted before any '
              'commitment; LPR and FRT licensing appears as its own line on the indicative rate card.')

    # 5 — Reporting (merged with data-led coverage)
    overline(doc, 'Intelligence')
    heading(doc, 'Intelligence-led reporting and data-led coverage')
    tile_grid(doc, [
        ('Deployment & Recovery Tracker', 'Hours, recoveries, incidents, offenders, deterrents and '
         'trespasses per store, with cost tracked against budget.'),
        ('National summary', 'Store, region and national totals with week-on-week movements explained, '
         'not just reported.'),
        ('Safety report', 'Severity spread on our 1 to 5 scale, with serious incidents narrated and '
         'Police referrals tracked.'),
        ('Verified attendance', 'Every hour billed reconciles to timeclock records. No guesswork, no '
         'ghost shifts.'),
    ])
    body(doc, '<b>Crime-intelligence integration.</b> Operatives are trained on retail crime-intelligence '
              'platforms such as Auror. Where authorised by you and consistent with your privacy policy, '
              'incidents are recorded in agreed systems and structured evidence packs prepared for Police '
              'consideration, subject always to Police evidential requirements and discretion.')
    body(doc, '<b>Data-led coverage.</b> Weeks 1 to 8 build a per-store baseline: incidents, recoveries, '
              'offender counts, trespass register, alarm activations and severity spread. Covert days and '
              'depth per store are then set from the data, weighing recovery value, incident severity, '
              'loss trend, stock profile and safety risk, with a breadth rule guaranteeing no store is '
              'ever left uncovered. The weighting is recalculated weekly, so when offenders shift to a '
              'quieter branch, the hours follow them within a week.')
    body(doc, '<b>Reporting cycle.</b> Real-time incident logging, a weekly pack every Tuesday, a monthly '
              'review of trends and recommendations, and a quarterly strategy session where coverage is '
              're-tiered from the data.')

    # 6 — Compliance
    overline(doc, 'Compliance')
    heading(doc, 'Licensed, trained and compliant')
    tile_grid(doc, [
        ('Personnel standards', '✓ Required current licence or Certificate of Approval under the Private '
         'Security Personnel and Private Investigators Act 2010, in the classes each role requires\n'
         '✓ Conflict resolution and de-escalation training\n✓ First aid\n✓ Site-specific SOP training '
         'before any shift\n✓ Pre-employment vetting including Police checks'),
        ('Operational quality', '✓ Timeclock-verified attendance at every shift\n✓ Digital, time-stamped '
         'incident logging\n✓ Weekly performance reporting\n✓ Monthly trend analysis and KPIs\n'
         '✓ Regular rotation to prevent complacency'),
        ('Insurance and liability', '✓ Public liability cover held by both entities\n✓ Statutory '
         'liability cover held by both entities\n✓ Certificates of currency and limits available on '
         'request'),
        ('Health and safety', '✓ We meet our PCBU duties under the Health and Safety at Work Act and '
         'consult, cooperate and coordinate with PB Tech on overlapping duties\n✓ Incident and near-miss '
         'reporting\n✓ De-escalation first; physical contact a last resort\n✓ 24/7 operations support '
         'line'),
    ])

    # 7 — Results
    overline(doc, 'Proven results')
    heading(doc, 'Proven in national retail')
    bullet(doc, '<b>Covert loss prevention:</b> more than $1 million in verified recoveries since July '
                '2025, reported to clients weekly, across 100+ retail sites.')
    bullet(doc, '<b>Precinct and urban security:</b> a flagship multi-year city-centre precinct contract '
                'has recorded zero use of force across every aggression incident in its life, with '
                'thousands of patrol routes and assistance calls completed.')
    body(doc, 'Reference conversations with comparable national retail clients are available on request, '
              'with those clients’ consent.')

    # 8 — The offer
    overline(doc, 'The offer')
    heading(doc, 'The Peak-Season Start: free audit, guaranteed pilot')
    body(doc, '<b>Start free: the Loss-Map Audit.</b> A walkthrough of three representative sites and a '
              'loss-data workshop under NDA, no cost, no obligation. We are on site within five working '
              'days of your confirmation and NDA execution, and return a store-by-store coverage plan, '
              'risk tiering and an indicative return scenario (assumptions stated) within ten working '
              'days of the workshop and receipt of your loss data. An indicative rate card per service '
              'line is available on request, independent of the audit. Everything the audit produces is '
              'yours to keep, whatever you decide.')
    body(doc, '<b>Pilot without risk.</b> A four-week covert LP pilot in your highest-loss stores, live '
              'within 48 hours of pilot-scope sign-off and store-access confirmation in our four covert '
              'base regions (other regions within five working days). Our pilot guarantee: if the '
              'verified recovery value recorded on the weekly tracker both parties sign off does not '
              'exceed the pilot’s invoiced cost across the four weeks, you do not pay. Interventions, '
              'deterrents and trespasses are reported alongside, but the guarantee is measured on '
              'recovery value alone; full terms sit in the pilot schedule.')
    body(doc, '<b>Timing.</b> The pilot runs as its own track under the 48-hour start commitment and '
              'does not wait for Phase 0, so covert teams can be in stores ahead of Black Friday on a '
              'prompt decision. On a Phase 0 start by Friday 13 November 2026, guarding is live at '
              'priority stores by early December and runs through the peak, with monitoring transitioning '
              'in parallel as incumbent notice periods allow, and the full national rotation completes by '
              'late January. The commercial terms in this document remain open until 21 December 2026; '
              'the pre-Christmas timeline holds only for a Phase 0 start by 13 November.')
    rows = [
        ['Phase', 'Timing', 'Scope'],
        ['0  Survey & design', 'Weeks 1–2',
         'Site surveys; risk tiering from PB Tech loss data (under NDA); burglary and ram-raid hardening '
         'assessment; SOPs and duress protocol; privacy scoping across CCTV, LPR, crime-intelligence and FRT'],
        ['1  Static & monitoring', 'Weeks 3–6',
         'Guarding live at priority stores; monitoring transition aligned to incumbent notice periods, '
         'with parallel running; reporting live from first shift'],
        ['2  Covert LP', 'Weeks 5–10',
         'Full national covert rotation from the four regional bases; pilot stores, data and weeks roll '
         'straight in without a restart; first tier re-weighting at week 8'],
        ['3  Vision systems (gated)', 'Week 8 on',
         'LPR pilot on carpark entries at selected sites under the Privacy Act controls in Section 4; '
         'FRT only after the necessity and proportionality assessment and PB Tech go or no-go, in 2–3 '
         'stores with pre-agreed accuracy, fairness, deletion and stop criteria'],
    ]
    t = doc.add_table(rows=len(rows), cols=3)
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths = [Mm(40), Mm(24), Mm(111)]
    for row in t.rows:
        for c, w in zip(row.cells, widths):
            c.width = w
    for j, cell in enumerate(t.rows[0].cells):
        shade(cell, '050A14')
        p = cell.paragraphs[0]
        r = p.add_run(rows[0][j])
        r.bold = True; r.font.name = BODY_FONT; r.font.size = Pt(8.5); r.font.color.rgb = WHITE
    for i, row in enumerate(rows[1:], start=1):
        if i % 2 == 0:
            for cell in t.rows[i].cells:
                shade(cell, 'F1F5F9')
        for j, val in enumerate(row):
            p = t.rows[i].cells[j].paragraphs[0]
            r = p.add_run(val)
            r.bold = (j == 0)
            r.font.name = BODY_FONT
            r.font.size = Pt(8.5)
            r.font.color.rgb = MIDNIGHT if j == 0 else SLATE

    # 9 — People
    overline(doc, 'Our people')
    heading(doc, 'Leadership team')
    if TEAM_PHOTO.exists():
        doc.add_picture(str(TEAM_PHOTO), width=Mm(120))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    body(doc, 'Our leadership experience is anchored by SLS Retail Theft Control’s continuous retail '
              'loss-prevention operation since 2006. The group is led by <b>Ahmad Duais</b> (Chief '
              'Executive), with <b>Mark Clansey</b> (General Manager) and <b>Hasi Nabawi</b> (Operations '
              'Manager) running national operations.')
    bullet(doc, '<b>Dedicated account manager</b> named at engagement: a single point of contact.')
    bullet(doc, '<b>Regional operations coverage</b> from our Auckland, Waikato, Wellington and '
                'Christchurch bases.')
    bullet(doc, '<b>24/7 operations support line</b> for urgent escalations.')
    bullet(doc, '<b>In-house training academy;</b> turnover across our permanent security workforce ran '
                'under 5% in the last 12 months.')
    bullet(doc, '<b>No subcontracting outside the group:</b> every officer is directly employed by an ASG '
                'Group company.')

    # Contact
    dark_block(doc, [
        ([('Ready when you are.', dict(bold=True, size=13, color=WHITE))], dict(before=10)),
        ([('Ahmad Duais  ·  Chief Executive, Absolute Security Group', dict(size=10))], dict()),
        ([('ahmad@absolutesecuritygroup.co.nz  ·  absolutesecuritygroup.co.nz  ·  slsrtc.co.nz',
           dict(size=10))], dict()),
        ([('Reply to this document to arrange the Loss-Map Audit.', dict(size=9, color=GRAY_500))],
         dict(after=10)),
    ])

    # Footer
    fp = sec.footer.paragraphs[0]
    fp.paragraph_format.tab_stops.add_tab_stop(Mm(170), WD_TAB_ALIGNMENT.RIGHT)
    r = fp.add_run('ASG Security  ·  Commercial in confidence\t')
    r.font.name = BODY_FONT; r.font.size = Pt(7.5); r.font.color.rgb = GRAY_500
    rp = fp.add_run('Page ')
    rp.font.name = BODY_FONT; rp.font.size = Pt(7.5); rp.font.color.rgb = GRAY_500
    fld = OxmlElement('w:fldSimple')
    fld.set(qn('w:instr'), 'PAGE')
    fp._p.append(fld)

    doc.save(str(OUT))
    print(f'OK {OUT}')


if __name__ == '__main__':
    main()
