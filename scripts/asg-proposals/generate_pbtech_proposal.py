#!/usr/bin/env python3
"""
ASG Security — PB Tech Integrated Security Proposal (3-4pp A4, ReportLab).
Brand: ASG Security Brand Guidelines V1.0 (Midnight/Signal Blue, Helvetica fallbacks).
Output: ~/Desktop/ASG/Sales & Marketing/Proposals/PBTech_Integrated_Security_Proposal.pdf
"""
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether,
)

# ---- Brand palette -----------------------------------------------------------
MIDNIGHT = HexColor('#050A14')
DEEP = HexColor('#0B1221')
NAVY = HexColor('#111B2E')
STEEL = HexColor('#1A2744')
SIGNAL = HexColor('#2563EB')
WHITE = HexColor('#FFFFFF')
GRAY_100 = HexColor('#F1F5F9')
GRAY_200 = HexColor('#E2E8F0')
GRAY_400 = HexColor('#94A3B8')
GRAY_500 = HexColor('#64748B')
SLATE = HexColor('#334155')

PAGE_W, PAGE_H = A4
M_SIDE, M_TOP, M_BOT = 54, 62, 52
COVER_H = 218  # cover band height on page 1

OUT = Path.home() / 'Desktop/ASG/Sales & Marketing/Proposals/PBTech_Integrated_Security_Proposal.pdf'

# ---- Styles ------------------------------------------------------------------
def st(name, **kw):
    base = dict(fontName='Helvetica', fontSize=10, leading=14.2, textColor=SLATE,
                spaceAfter=7)
    base.update(kw)
    return ParagraphStyle(name, **base)

S = {
    'body': st('body'),
    'lead': st('lead', fontSize=10.5, leading=15, textColor=NAVY),
    'h2': st('h2', fontName='Helvetica-Bold', fontSize=13.5, leading=16.5,
             textColor=MIDNIGHT, spaceBefore=13, spaceAfter=5),
    'h3': st('h3', fontName='Helvetica-Bold', fontSize=10.5, leading=14,
             textColor=MIDNIGHT, spaceBefore=7, spaceAfter=3),
    'overline': st('overline', fontName='Helvetica-Bold', fontSize=8,
                   textColor=SIGNAL, spaceAfter=2, leading=10),
    'bullet': st('bullet', leftIndent=12, bulletIndent=2, spaceAfter=4),
    'statnum': st('statnum', fontName='Courier-Bold', fontSize=16, leading=18,
                  textColor=MIDNIGHT, alignment=1, spaceAfter=1),
    'statlab': st('statlab', fontSize=8, leading=10, textColor=GRAY_500,
                  alignment=1, spaceAfter=0),
    'tcell': st('tcell', fontSize=8.5, leading=11.5, spaceAfter=0),
    'tcellb': st('tcellb', fontName='Helvetica-Bold', fontSize=8.5, leading=11.5,
                 textColor=MIDNIGHT, spaceAfter=0),
}

def B(text):  # body paragraph
    return Paragraph(text, S['body'])

def BUL(text):
    return Paragraph(text, S['bullet'], bulletText='•')

def H2(num, text):
    return KeepTogether([
        Paragraph(f'<font color="#2563EB">{num}</font>&nbsp;&nbsp;{text}', S['h2']),
    ])

def H3(text):
    return Paragraph(text, S['h3'])

# ---- Cover band + footer -----------------------------------------------------
def draw_cover(cv, doc):
    cv.saveState()
    cv.setFillColor(MIDNIGHT)
    cv.rect(0, PAGE_H - COVER_H, PAGE_W, COVER_H, stroke=0, fill=1)
    # thin signal-blue rule along band base
    cv.setFillColor(SIGNAL)
    cv.rect(0, PAGE_H - COVER_H, PAGE_W, 2.2, stroke=0, fill=1)
    x = M_SIDE
    # wordmark
    y = PAGE_H - 46
    cv.setFillColor(WHITE)
    cv.setFont('Helvetica-Bold', 15)
    cv.drawString(x, y, 'ASG')
    w_asg = cv.stringWidth('ASG', 'Helvetica-Bold', 15)
    cv.setStrokeColor(GRAY_500)
    cv.setLineWidth(0.8)
    cv.line(x + w_asg + 8, y - 2.5, x + w_asg + 8, y + 12)
    cv.setFont('Helvetica', 10.5)
    cv.setFillColor(GRAY_400)
    _tracked(cv, x + w_asg + 15, y + 0.5, 'SECURITY', 3.0)
    cv.setFont('Helvetica', 8.5)
    cv.setFillColor(GRAY_400)
    cv.drawRightString(PAGE_W - M_SIDE, y + 0.5, 'Complete Security. One Partner.')
    # overline
    cv.setFillColor(SIGNAL)
    cv.setFont('Helvetica-Bold', 8.5)
    _tracked(cv, x, PAGE_H - 96, 'INTEGRATED SECURITY PROPOSAL', 1.8)
    # title
    cv.setFillColor(WHITE)
    cv.setFont('Helvetica-Bold', 25)
    cv.drawString(x, PAGE_H - 126, 'PB Tech — nationwide security')
    cv.drawString(x, PAGE_H - 156, 'operations, one partner')
    # meta line
    cv.setFont('Helvetica', 9.5)
    cv.setFillColor(GRAY_400)
    cv.drawString(x, PAGE_H - 182,
                  'Prepared for PB Technologies Ltd   ·   October 2026   ·   Commercial in confidence')
    cv.drawString(x, PAGE_H - 196,
                  'Absolute Security Group Ltd  &  SLS RTC Ltd')
    cv.restoreState()
    draw_footer(cv, doc)

def _tracked(cv, x, y, text, tracking):
    for ch in text:
        cv.drawString(x, y, ch)
        x += cv.stringWidth(ch, cv._fontname, cv._fontsize) + tracking

def draw_footer(cv, doc):
    cv.saveState()
    cv.setStrokeColor(GRAY_200)
    cv.setLineWidth(0.6)
    cv.line(M_SIDE, 40, PAGE_W - M_SIDE, 40)
    cv.setFont('Helvetica', 7.5)
    cv.setFillColor(GRAY_500)
    cv.drawString(M_SIDE, 29, 'ASG Security  ·  Commercial in confidence')
    cv.drawRightString(PAGE_W - M_SIDE, 29, f'Page {doc.page}')
    cv.restoreState()

# ---- Stat strip --------------------------------------------------------------
def stat_strip():
    stats = [
        ('300+', 'security professionals'),
        ('4', 'regional covert bases'),
        ('35+', 'retail stores worked weekly'),
        ('1,200+', 'covert LP hours weekly'),
    ]
    cells = [[Table([[Paragraph(n, S['statnum'])], [Paragraph(l, S['statlab'])]],
                    colWidths=[(PAGE_W - 2 * M_SIDE) / 4 - 8])
              for n, l in stats]]
    t = Table(cells, colWidths=[(PAGE_W - 2 * M_SIDE) / 4] * 4)
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEABOVE', (0, 0), (-1, 0), 0.7, GRAY_200),
        ('LINEBELOW', (0, 0), (-1, 0), 0.7, GRAY_200),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t

# ---- Content -----------------------------------------------------------------
def build_story():
    s = []
    s.append(Paragraph('1&nbsp;&nbsp;Executive summary',
                       ParagraphStyle('h2first', parent=S['h2'], spaceBefore=0)))
    s.append(Paragraph(
        'Security for a nationwide retail network is usually bought as three separate services \u2014 '
        'guarding from one vendor, alarm monitoring from another, loss prevention from a third \u2014 none of '
        'which share data. The gaps between vendors are where loss happens. ASG Group proposes to run all of '
        'it for PB Tech as one partnership: <b>one vendor, one SLA, one weekly report, every store.</b>', S['lead']))
    s.append(B('The risk profile justifies it. PB Tech\u2019s superstores and service centres carry dense '
               'concentrations of high-value, high-resale, serialised stock \u2014 a profile that draws organised '
               'repeat offenders working across branches, distraction theft at counters, refund and warranty '
               'fraud, and targeted after-hours attack on stores and warehouses. The partnership is built on '
               'five layers:'))
    s.append(BUL('<b>Risk-tiered static guarding</b> at the stores where measured loss justifies a visible presence.'))
    s.append(BUL('<b>Covert loss prevention</b> \u2014 plain-clothes operatives who engage offenders where it is '
                 'safe and lawful, recover stock, and document everything.'))
    s.append(BUL('<b>CCTV and alarm monitoring</b>, 24/7, with video-verified response wherever live footage '
                 'is available.'))
    s.append(BUL('<b>Facial recognition (optional, privacy-gated)</b> \u2014 watchlist alerting for serious repeat '
                 'offenders, taken forward only if a joint assessment under the Biometric Processing Privacy '
                 'Code 2025 supports it.'))
    s.append(BUL('<b>Data-led coverage</b> \u2014 guard-hours re-weighted every week from your own incident and '
                 'recovery data, so cover sits where loss is occurring.'))
    s.append(B('<b>Who we are.</b> ASG Group is New Zealand-owned: <b>Absolute Security Group Ltd</b> '
               '(uniformed guarding, precinct patrol, CCTV monitoring and electronic security) and '
               '<b>SLS RTC Ltd</b> (specialist covert retail loss prevention), operating as one group with '
               'covert teams based in Auckland, Hamilton, Wellington and Christchurch. Our covert operatives '
               'work every week inside national retail networks across grocery, hardware and general '
               'merchandise. Client data is strictly siloed \u2014 each client\u2019s incident, offender and loss data '
               'lives in its own store and is never cross-shared \u2014 and a dedicated PB Tech team with '
               'contractual information barriers is part of this offer.'))
    s.append(stat_strip())

    s.append(H2('2', 'Current operations \u2014 what we run today'))
    s.append(B('<b>Covert retail loss prevention (SLS RTC).</b> Two-operative minimum teams \u2014 we never roster '
               'solo covert staff \u2014 rotating across client store networks. Operatives engage and recover under '
               'a documented use-of-force and citizen\u2019s-arrest policy: de-escalate, recover, document, refer. '
               'Trespass warnings are administered as the client\u2019s authorised agents under the Trespass Act '
               '1980. Every incident is graded on our 1\u20135 severity scale (1 = compliant through 5 = '
               'physical/weapons), so you see the safety picture your staff face, not just the recovery number. '
               'Structured evidence packs support Police decision-making \u2014 individual incidents rarely cross '
               'the charging threshold, but a documented cross-store pattern gives Police something to assess.'))
    s.append(B('<b>Static and uniformed guarding (ASG).</b> Retail, corporate, venue and precinct work, '
               'including a multi-year city-centre precinct safety patrol contract run to contracted '
               'response-time service levels.'))
    s.append(B('<b>CCTV, monitoring and electronic security (ASG).</b> We operate on the Nx Witness video '
               'management platform, run remote CCTV monitoring, and engineer our own alert-triage tooling so '
               'operators work a ranked, verified queue rather than a raw alarm flood. Camera-health monitoring '
               'is standing practice \u2014 a dead camera is a blind spot, and we treat it as an incident.'))
    s.append(B('<b>Systems and integrations.</b> GPS-verified patrols, digital incident reporting from the '
               'floor, timeclock-verified billing, and \u2014 where authorised by the client and consistent with its '
               'privacy policy \u2014 integration with retail crime-intelligence platforms such as Auror.'))

    s.append(H2('3', 'Proposed configuration for PB Tech'))
    s.append(B('<b>3.1&nbsp; Static guarding \u2014 risk-tiered, not blanket.</b> We do not propose a guard in '
               'every store. Phase 0 tiering, built from your loss data and our site surveys, sets which sites '
               'carry trading-hour presence, which carry peak-window presence (weekends, launch days, '
               'promotional periods), and which are covered by covert rotation and monitoring. The protocol for '
               'when your staff face aggression \u2014 including duress-alarm response \u2014 is agreed in Phase 0, '
               'alongside the overlapping-duties consultation the Health and Safety at Work Act requires '
               'between both PCBUs. Electronics-specific training modules (distraction theft, grab-and-run on '
               'display stock, refund and warranty fraud, service-centre custody of customer devices) are '
               'built with your input in Phase 0.'))
    s.append(B('<b>3.2&nbsp; Covert loss prevention \u2014 intercept and recover.</b> Rotating covert teams '
               'concentrate on the highest-loss stores, with depth set by measured return (Section 4). '
               'Operatives engage and recover where it is safe and lawful \u2014 our staff hold no detention powers '
               'beyond any citizen\u2019s, and are trained to de-escalate, preserve evidence and refer to Police '
               'rather than confront \u2014 administer trespass warnings under written delegation, and build '
               'offender files. Because one team works many branches, cross-store patterns \u2014 the same group '
               'hitting your Albany branch on Tuesday and St Lukes on Thursday \u2014 surface in days, not months. '
               'Where loss patterns point inside, the same team runs covert investigations and serialised-stock '
               'tracing.'))
    s.append(B('<b>3.3&nbsp; CCTV and alarm monitoring \u2014 verified response.</b> 24/7 monitoring of alarm '
               'activations. Events are video-verified where live footage is available; otherwise the agreed '
               'alarm-response protocol applies \u2014 verification never delays response. Patrol or keyholder '
               'response to verified events. We integrate with your existing camera estate where it is fit for '
               'purpose and specify upgrades only where coverage gaps create risk. Because after-hours attack '
               'is a defining risk for stores and warehouses full of resaleable stock, Phase 0 includes a '
               'site-by-site burglary and ram-raid hardening assessment, and after-hours response targets are '
               'set per location class in the SLA.'))
    s.append(B('<b>3.4&nbsp; Facial recognition \u2014 staged, honest, gated.</b> FRT in New Zealand retail is '
               'governed by the Biometric Processing Privacy Code 2025; done wrong it is a regulatory and '
               'reputational liability, and the evidence from New Zealand\u2019s only large retail trial is '
               'qualified \u2014 which is why we pilot and measure rather than promise. How it works, stated '
               'plainly: every entering face is checked against a watchlist; non-matches are deleted '
               'immediately; only enrolled individuals are retained. Enrolment is limited to serious repeat '
               'offenders \u2014 formally trespassed, identity verified, approved person-by-person by PB Tech, no '
               'minors or vulnerable persons, entries expiring with the two-year trespass warning and reviewed '
               'on a set cycle. Every alert is verified by a human operator before any floor response; no '
               'action is ever taken on an automated match alone. Controls include purpose limitation, defined '
               'retention, role-based access with audit logs, accuracy testing before go-live, clear entry '
               'signage, and incident and breach procedures. PB Tech owns the necessity-and-proportionality '
               'assessment and the go/no-go decision \u2014 we prepare it with you and supply the operational '
               'evidence. If the assessment does not support FRT, we do not run it; the rest of this proposal '
               'stands on its own.'))

    s.append(H2('4', 'Data-led coverage \u2014 hours follow the loss'))
    s.append(B('Most guarding contracts fix hours at tender and never move them. Ours re-weights cover every '
               'week from your own incident and recovery data.'))
    s.append(B('<b>Baseline and tiering.</b> Weeks 1\u20138 build a per-store baseline: incidents, recoveries, '
               'offender counts, trespass register, alarm activations and severity spread. Stores are tiered '
               'from the data, not by intuition.'))
    s.append(B('<b>Return-weighted coverage.</b> Covert days and depth per store follow the data. For '
               'illustration: a store returning around $15k of quarterly recoveries might warrant four covert '
               'visit-days a week; one returning under $1k, a single day \u2014 with a breadth rule guaranteeing no '
               'store is ever left uncovered. Recovery value is one input alongside incident severity, loss '
               'trend and stock profile \u2014 it informs cover, it does not cap it. The weighting is recalculated '
               'weekly, so when offenders shift to a quieter branch, the hours follow them within a week.'))
    s.append(B('<b>Evidence pipeline.</b> Every documented incident feeds offender profiles and structured '
               'evidence packs for Police \u2014 subject always to Police evidential requirements and discretion. '
               'The trespass register feeds the FRT watchlist only under the enrolment standard in 3.4.'))
    s.append(H3('Weekly reporting package \u2014 one pack, every Tuesday'))
    s.append(BUL('<b>Deployment &amp; Recovery Tracker (Excel)</b> \u2014 hours, recoveries, incidents, offenders, '
                 'deterrents and trespasses per store; cost against budget, week / period / year-to-date.'))
    s.append(BUL('<b>National summary</b> \u2014 store, region and national totals with week-on-week movements '
                 'explained, not just reported. Billed hours reconcile to timeclock records, recoveries are '
                 'valued at verified retail value, and totals reconcile exactly across every level of the pack.'))
    s.append(BUL('<b>Safety report</b> \u2014 severity spread on the 1\u20135 scale, serious (3+) incidents narrated, '
                 'Police referrals tracked.'))
    s.append(B('<b>Governance cadence.</b> Weekly report \u2192 monthly operations review with your LP lead \u2192 '
               'quarterly strategy review where tiering, static placement and the FRT gate are re-set from '
               'the data.'))

    s.append(H2('5', 'Implementation'))
    rows = [
        ['Phase', 'Timing', 'Scope'],
        ['0 \u2014 Survey & design', 'Weeks 1\u20132',
         'Site surveys; risk tiering from PB Tech loss data (under NDA); burglary/ram-raid hardening '
         'assessment; SOPs and duress protocol; privacy scoping across CCTV, crime-intelligence and FRT'],
        ['1 \u2014 Static & monitoring', 'Weeks 3\u20136',
         'Guarding live at priority stores; monitoring transition aligned to incumbent notice periods, with '
         'parallel running; reporting live from first shift'],
        ['2 \u2014 Covert LP', 'Weeks 5\u201310',
         'Covert rotation live nationally from the four regional bases; baseline accumulating; first tier '
         're-weighting at week 8'],
        ['3 \u2014 FRT (gated)', 'Week 8 on',
         'Necessity-and-proportionality assessment completed with PB Tech; pilot proceeds only on PB Tech '
         'go/no-go, in 2\u20133 stores with a measured false-positive gate'],
    ]
    data = [[Paragraph(f'<font color="#FFFFFF"><b>{c}</b></font>', S['tcell']) if r == 0
             else Paragraph(c, S['tcellb'] if i == 0 else S['tcell'])
             for i, c in enumerate(row)] for r, row in enumerate(rows)]
    tw = PAGE_W - 2 * M_SIDE
    t = Table(data, colWidths=[tw * 0.23, tw * 0.14, tw * 0.63], repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), MIDNIGHT),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, GRAY_100]),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY_200),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
    ]))
    s.append(t)
    s.append(Spacer(0, 4))

    s.append(H2('6', 'Accountability, compliance and commercial approach'))
    s.append(B('<b>SLA.</b> Weekly report every Tuesday; monthly operations review; quarterly business '
               'reviews with the data on the table. Shift-fill guarantee and monitored-event response targets '
               'by location class, backed by service credits \u2014 the numbers are tabled with the priced plan.'))
    s.append(B('<b>Contracting.</b> Absolute Security Group Ltd contracts as head contractor; SLS RTC Ltd '
               'delivers covert LP under it as a disclosed subcontractor with flow-down obligations \u2014 one '
               'counterparty, one invoice.'))
    s.append(B('<b>Licensing, vetting and insurance.</b> Both entities are licensed under the Private '
               'Security Personnel and Private Investigators Act 2010 in the classes each service requires; '
               'every operative holds the required current licence or Certificate of Approval, verified at '
               'induction and re-checked during the term. Pre-employment vetting includes Police checks. '
               'Public liability and statutory liability cover is held by both entities \u2014 certificates of '
               'currency and limits are provided with the priced plan.'))
    s.append(B('<b>Your data.</b> PB Tech\u2019s incident, offender and loss data lives in an access-controlled '
               'store siloed from every other client, with role-based access, return or destruction on exit, '
               'and breach notification agreed in the SLA.'))
    s.append(B('<b>Commercial.</b> A single national agreement, one consolidated monthly invoice, and '
               'cost-versus-budget visible in every weekly tracker \u2014 you should never have to ask what you '
               'spent or what it returned. Rates adjust annually through a transparent mechanism tied to '
               'published wage movements, not mid-term renegotiation.'))

    s.append(H2('7', 'Next steps'))
    s.append(BUL('Mutual NDA, then a 90-minute loss-data workshop and a walkthrough of three representative '
                 'sites (one superstore, one service centre, one distribution point). We can be on site within '
                 'five working days of your reply.'))
    s.append(BUL('We return a priced, store-by-store coverage plan \u2014 with the indicative rate card per '
                 'service line \u2014 within ten working days of the workshop.'))
    s.append(Spacer(0, 6))
    s.append(B('<b>Ahmad Duais</b> \u2014 Chief Executive, Absolute Security Group<br/>'
               'ahmad@absolutesecuritygroup.co.nz &nbsp;\u00b7&nbsp; absolutesecuritygroup.co.nz'))
    return s

# ---- Document ----------------------------------------------------------------
def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=M_SIDE, rightMargin=M_SIDE,
                          topMargin=M_TOP, bottomMargin=M_BOT,
                          title='PB Tech — Integrated Security Proposal',
                          author='ASG Security')
    frame_cover = Frame(M_SIDE, M_BOT, PAGE_W - 2 * M_SIDE,
                        PAGE_H - COVER_H - M_BOT - 18, id='cover')
    frame_norm = Frame(M_SIDE, M_BOT, PAGE_W - 2 * M_SIDE,
                       PAGE_H - M_TOP - M_BOT, id='norm')
    doc.addPageTemplates([
        PageTemplate(id='first', frames=[frame_cover], onPage=draw_cover),
        PageTemplate(id='later', frames=[frame_norm], onPage=draw_footer),
    ])
    story = build_story()
    from reportlab.platypus import NextPageTemplate
    story.insert(0, NextPageTemplate('later'))
    doc.build(story)
    print(f'OK {OUT}')

if __name__ == '__main__':
    main()
