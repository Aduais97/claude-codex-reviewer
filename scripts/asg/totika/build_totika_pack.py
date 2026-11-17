#!/usr/bin/env python3
"""ASG Totika Prequalification Pack — Evidence Register XLSX + Briefing PDF.

ETR agentic workflow run wf_2edef0ec-0a4 (17 Nov 2026): 4 web research agents +
1 local inventory agent -> synthesis -> 3-lens adversarial verify (fact-check,
category-correctness, completeness). All verifier corrections applied here.

Navy+gold house style per ~/.claude/commands/references/generate-pdf.md.
Outputs: ~/Desktop/ASG/Totika/ASG_Totika_Evidence_Register.xlsx
         ~/Desktop/ASG/Totika/ASG_Totika_PreQual_Briefing_Nov2026.pdf
"""
import os, json, re
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak, KeepTogether,
                                Flowable, HRFlowable)

NAVY = HexColor('#1B2A4A'); DARKBLUE = HexColor('#2C3E6B'); MIDBLUE = HexColor('#4A6FA5')
GOLD = HexColor('#D4A843'); LIGHTBLUE = HexColor('#E8EDF5'); BGGREY = HexColor('#F7F8FA')
BORDER = HexColor('#D0D5DD'); ROWALT = HexColor('#F2F4F8')
TEXTD = HexColor('#1A1A2E'); TEXTM = HexColor('#4A4A5A'); TEXTL = HexColor('#7A7A8A')
RED = HexColor('#C0392B'); AMBER = HexColor('#E67E22'); GREEN = HexColor('#27AE60')

PAGE_W, PAGE_H = A4
ML, MR, MT, MB = 54, 54, 62, 54
CW = PAGE_W - ML - MR

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.expanduser('~/Desktop/ASG/Totika')
os.makedirs(OUTDIR, exist_ok=True)
PDF_OUT = os.path.join(OUTDIR, 'ASG_Totika_PreQual_Briefing_Nov2026.pdf')
XLSX_OUT = os.path.join(OUTDIR, 'ASG_Totika_Evidence_Register.xlsx')

REGISTER = json.load(open(os.path.join(HERE, 'totika_register.json')))

S = {}
S['body'] = ParagraphStyle('body', fontName='Helvetica', fontSize=10, leading=14.5,
                           textColor=TEXTD, alignment=TA_JUSTIFY, spaceAfter=7)
S['bodyL'] = ParagraphStyle('bodyL', parent=S['body'], alignment=TA_LEFT)
S['lead'] = ParagraphStyle('lead', parent=S['bodyL'], fontName='Helvetica-Bold')
S['small'] = ParagraphStyle('small', parent=S['body'], fontSize=8.5, leading=12,
                            textColor=TEXTM, alignment=TA_LEFT)
S['bullet'] = ParagraphStyle('bullet', parent=S['body'], leftIndent=18, bulletIndent=6,
                             spaceAfter=5, alignment=TA_LEFT)
S['h3'] = ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=11.5, leading=14,
                         textColor=DARKBLUE, spaceBefore=12, spaceAfter=4)
S['cap'] = ParagraphStyle('cap', fontName='Helvetica-Oblique', fontSize=8.5, leading=11.5,
                          textColor=TEXTM, spaceBefore=4, spaceAfter=8)
S['cell'] = ParagraphStyle('cell', fontName='Helvetica', fontSize=8.5, leading=11,
                           textColor=TEXTD, alignment=TA_LEFT)
S['cellC'] = ParagraphStyle('cellC', parent=S['cell'], alignment=TA_CENTER)
S['cellH'] = ParagraphStyle('cellH', fontName='Helvetica-Bold', fontSize=8.5, leading=11,
                            textColor=white, alignment=TA_CENTER)
S['toc1'] = ParagraphStyle('toc1', fontName='Helvetica', fontSize=10.5, leading=19,
                           textColor=TEXTD)

STATUS_COLOR = {'HAVE': GREEN, 'PARTIAL': AMBER, 'MISSING': RED, 'UNKNOWN': TEXTM}


class SectionBar(Flowable):
    def __init__(self, number, title):
        super().__init__()
        self.number = number; self.title = title; self.height = 24

    def wrap(self, aw, ah):
        self.width = aw
        return aw, self.height + 10

    def draw(self):
        c = self.canv
        c.setFillColor(NAVY)
        c.rect(0, 0, self.width, self.height, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(0, 0, 4, self.height, stroke=0, fill=1)
        c.setFillColor(white)
        c.setFont('Helvetica-Bold', 13)
        label = f"{self.number}.  {self.title}" if self.number else self.title
        c.drawString(12, 7, label)


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(BORDER); canvas.setLineWidth(0.5)
    canvas.line(ML, PAGE_H - 40, PAGE_W - MR, PAGE_H - 40)
    canvas.setFont('Helvetica', 7); canvas.setFillColor(TEXTL)
    canvas.drawString(ML, PAGE_H - 36, 'Absolute Security Group  |  Totika Prequalification Briefing')
    canvas.drawRightString(PAGE_W - MR, PAGE_H - 36, 'CONFIDENTIAL')
    canvas.line(ML, 40, PAGE_W - MR, 40)
    canvas.setFont('Helvetica', 7.5)
    canvas.drawString(ML, 30, '17 November 2026')
    canvas.drawCentredString(PAGE_W / 2, 30, f'Page {doc.page}')
    canvas.drawRightString(PAGE_W - MR, 30, 'ETR run wf_2edef0ec-0a4')
    canvas.restoreState()


def esc(text):
    """Escape raw ampersands while leaving intentional entities intact."""
    return re.sub(r'&(?!amp;|bull;|lt;|gt;|nbsp;|#)', '&amp;', text)


def datatable(headers, rows, widths, bold_rows=(), status_col=None):
    hdr = [Paragraph(h, S['cellH']) for h in headers]
    body = []
    for r in rows:
        line = []
        for ci, cell in enumerate(r):
            cell = esc(cell) if isinstance(cell, str) else cell
            if ci == status_col:
                col = STATUS_COLOR.get(cell, TEXTD)
                st = ParagraphStyle(f'st{cell}', parent=S['cellC'],
                                    fontName='Helvetica-Bold', textColor=col)
                line.append(Paragraph(cell, st))
            else:
                st = S['cell'] if ci == 0 or ci >= 2 else S['cellC']
                line.append(Paragraph(cell, st))
        body.append(line)
    t = Table([hdr] + body, colWidths=widths, repeatRows=1)
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('GRID', (0, 0), (-1, -1), 0.4, BORDER),
        ('LINEBELOW', (0, 0), (-1, 0), 1.2, NAVY),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]
    for i in range(len(body)):
        if i % 2 == 1:
            style.append(('BACKGROUND', (0, i + 1), (-1, i + 1), ROWALT))
    for i in bold_rows:
        style.append(('BACKGROUND', (0, i + 1), (-1, i + 1), LIGHTBLUE))
    t.setStyle(TableStyle(style))
    return t


# ---------------------------------------------------------------- content data
ACTION_PLAN = [
    ("1. [RESOLVED 17 Nov] Gate check: Totika IS required in the PC tender", "Done (verified from tender docs)", "-",
     "PC 523941 question 8.1 / RFX-22 literally asks: 'Do you maintain an OHS Management System certified to "
     "ISO 45001:2018 or recognized under Totika / ACC WSMP? Please attach certificate.' Totika is the accepted "
     "route (ACC WSMP is retired; ISO 45001 not held). Site 360 in the PC docs is the DC visitor sign-in kiosk "
     "guards operate, not a supplier prequal portal. HNZ is PARKED per Ahmad 17 Nov — Woolworths drives timing."),
    ("2. [RESOLVED 17 Nov] Entity: ASG Limited", "Done (verified from tender docs)", "-",
     "The group structure statement names ASG Limited as 'the contracting entity for new business, including the "
     "distribution centre tender currently in progress', and the drafted PSPLA answer bids as ASG Limited (NZBN "
     "9429050952960). Register ASG Ltd only; SLS RTC is not needed for this tender."),
    ("3. Sign the H&S policy", "Ahmad + Hasibullah", "TODAY",
     "Verify Hasibullah is a current registered ASG Ltd director, then both sign and date "
     "ASG_Health_and_Safety_Policy_SMS_Nov2026 and regenerate the PDF. P1: the drafted PC Q8.1 answer claims the "
     "SMS is 'issued and signed November 2026' and uploads it in place of a certificate — it must actually be "
     "signed before submission."),
    ("4. Free Totika supplier registration + PAY RapidCert", "Shannon or Ahmad", "by 21 Nov (before PC submission)",
     "Register ASG at app.totika.org (free), then purchase the TOTIKA Category 2 assessment at "
     "app.rapidcert.co.nz/signup/totika ($949+GST = $1,091.35). Paying BEFORE 25 Nov makes 'Category 2 assessment "
     "in progress with SHE Pre-Qual' literally true in the Q8.1/Q4.5 answers — far stronger than a bare "
     "commitment. Urgent fee (+$250) NOT needed: no track delivers a certificate by 25 Nov, and the real deadline "
     "is mobilisation (1 Mar 2027)."),
    ("5. Pre-payment email to SHE Prequal", "Claude drafts, Ahmad sends", "17-18 Nov",
     "One email to support@sheprequal.co.nz (06 833 7227): (a) is the $20M Category 2 contract cap per annum or "
     "whole-of-term — the PC contract term is stated nowhere in the RFx (clarification Q1 lodged); if WW answers "
     "5 years at $4.5-5M/yr, whole-of-term exceeds $20M and Category 3 recategorisation applies within one month "
     "of award; (b) are clarification rounds included in the fee (unverified; fees non-refundable); "
     "(c) Christmas assessor cutoff date; (d) current member-scheme roster."),
    ("6. Live records that cannot be backfilled", "Ahmad / Shannon / ops", "BEFORE 24 Nov (~3 hrs total)",
     "Do these before PC submission week swallows the calendar: management meeting with H&S as agenda item 1 + "
     "3-5 FY27 H&S KPIs, minuted (MB5/12); first recorded H&S committee meeting (MB27); toolbox talk covering the "
     "signed policy with signed attendance (MB2/28); induction sign-offs at the 19 Nov Thursday session — only "
     "19 and 26 Nov sessions exist this month, so confirm real inductees or export history from Deputy (MB16). "
     "These cadences also underwrite claims already made in the PC draft answers."),
    ("7. Ahmad confirmations", "Ahmad", "by 21 Nov",
     "R&P notifiability CLEARED 17 Nov: Ahmad confirms the Reign & Pour incident did not meet the HSWA s23 "
     "notifiable threshold, so the nil WorkSafe declaration in PC Q8.5 stands and R&P can be used as an "
     "investigation example. Remaining: (a) Nil WorkSafe/court return for ASG Ltd and directors (assessor runs "
     "a court search). (b) SafetySeek genuinely in use — the PC Q8.1 answer asserts the SMS 'is administered "
     "through the SafetySeek platform'; confirm or strip before submission. (c) Deputy training/CoA register "
     "real and exportable. (d) PSPLA Responsible Employee named + licence certificates downloaded. (e) BizCover "
     "schedule (due 21 Nov) -> standalone certificates; decide the $3M PI quote."),
    ("8. Build/collate sprint (Claude-buildable; post-sweep this is mostly COLLATION)", "Claude + Shannon", "26-28 Nov (after PC submission)",
     "TOP ACTION: export Connecteam 'H&S Toolbox Meeting' form submissions + any digital policy acknowledgements "
     "(may close MB28/MB2 outright). Then: re-date and restructure the EXISTING hazard register so "
     "violence/aggression leads + 2 site risk assessments (MB29); complete the EXISTING Onboarding pack.xlsx into "
     "the training matrix (MB15); lone-worker procedure wrapped around the 980-log welfare-check record + staged "
     "extracts; HOTC site safety plan (MB10); finish/sign the WW ethical self-audit then run the internal HSMS "
     "self-audit (MB14); locate or write the completed Reign & Pour investigation report; redact + stage the "
     "Cotton On and 19 Mar 26 investigations; RTW procedure around Torrin's live plan; no-subcontracting policy "
     "(MB39-42); PPE register from the daily-log equipment blocks + PPE.docx; vehicle/journey policy (true gap); "
     "BWC/CCTV privacy one-pager; doc-control + SOP dedupe (library in 10+ locations); officer due-diligence plan; "
     "HSR statement; notifiable-event register; fatigue limit reconciliation (MB36); emergency assault procedure "
     "(MB24); improvement write-ups; budget statement."),
    ("9. Resolve the PC tender placeholders", "Claude drafts, Ahmad approves", "before 25 Nov 4pm",
     "Swap the two Totika placeholders in PC_523941_Draft_Answers_v1.docx (Q8.1 '[VERIFY: current Totika "
     "registration status]' + '[AHMAD: confirm target Totika tier]'; Q4.5 '[VERIFY: Totika status]') for the "
     "live position: supplier registration completed, Category 2 assessment in progress with SHE Pre-Qual, "
     "listing expected December 2026, ahead of the 1 March 2027 commencement. Only submit this wording if "
     "payment (step 4) actually happened."),
    ("10. Evidence upload and submission timing", "Shannon (employee submission satisfies the rule)", "early Dec",
     "With HNZ parked, 'Performing' pressure is off: RFX-22 asks for recognition under Totika, and a listed "
     "supplier is recognised whether graded Performing or Developing. So submit as soon as the evidence set is "
     "coherent (early Dec after the 26-28 Nov build sprint), accept a Developing first pass if that is the "
     "outcome, and re-mark at a later review once 3-6 months of cadence records exist. Realistic listing: late "
     "Dec 2026 (or mid-Jan 2027 across the Christmas shutdown) — months ahead of 1 Mar 2027 mobilisation."),
    ("11. After approval", "Shannon", "on listing",
     "Download certificate (category, score %, Performing/Developing, valid-until) + full report; upload proof to "
     "the Totika dashboard at app.totika.org so buyers can see the listing. Diarise annual renewal AND the "
     "one-month recategorisation rule: if the business changes (e.g. 5-yr PC award pushes whole-of-term value "
     "past $20M -> Category 3; Liberty Security subcontracting goes live -> MB39-42 flips from NA to a real "
     "procedure), a new assessment is required within ONE MONTH or the listing expires."),
]

OPEN_QUESTIONS = [
    ("WW contract term", "When Woolworths answers clarification Q1 (initial term from 1 Mar 2027 + renewals): does term x ~$4.5-5M/yr exceed $20M whole-of-term? If yes, Category 3 recategorisation applies within one month of award ($1,459+GST/yr, larger question set)."),
    ("WorkSafe / court history", "Confirm nil enforcement/prosecution/investigation (5 years) for ASG Ltd, SLS RTC Ltd and all directors — the assessor verifies via court search."),
    ("Policy signatures", "Sign the H&S policy (Ahmad + Hasibullah) — nothing can be submitted until done. First verify Hasibullah's current registered directorship."),
    ("SafetySeek", "Is SafetySeek genuinely in use as the SMS platform? If not, the claim must be dropped before it reaches an assessor."),
    ("Deputy training register", "Does the Deputy-linked training/CoA register with expiry alerts (claimed in both tenders) actually exist and export? If not it must be stood up now."),
    ("Insurance", "Chase BizCover schedule (due 21 Nov) for standalone certificates; decide the $3M PI quote; is any cover held in SLS RTC's name?"),
    ("PSPLA", "Who is the Responsible Employee ('[to confirm]' in the structure doc)? Download both PSPLA licence certificates."),
    ("Fatigue limits", "Do 12h max shift / 10h min rest / 60h per 7 days match the issued Fatigue Policy? Reconcile before asserting to Totika."),
    ("Submitter", "Who submits in RapidCert — must be an ASG employee (Shannon as H&S Administrator is natural) or a HASANZ-registered consultant."),
    ("Liberty go-live", "Expected go-live date for the Fernando+Jason/Liberty B2B restructure? If invoicing starts before submission, the 'no subcontracting' NA answer is false on day one."),
    ("Inductees", "Do 3 genuine new inductees exist across the 19/26 Nov Thursday sessions, or should induction records be exported from Deputy history?"),
]

SCHEME_FACTS = [
    ("Official domain", "totika.org (totika.org.nz does not resolve). Free supplier registration: app.totika.org"),
    ("Governance", "CHASNZ board of trustees (not-for-profit). Cross-recognition: one assessment with any member scheme, listed on the central register, accepted by every buyer member"),
    ("Buyers", "40+ buyer organisations displayed on totika.org incl. Te Whatu Ora - Health NZ, Auckland Council, Auckland Transport, Eke Panuku, Watercare, SkyCity, Auckland Airport, St John, NZTA, Fonterra, IAG. Woolworths / Primary Connect is NOT displayed (they use Site360)"),
    ("Member schemes", "totika.org references 'our three member schemes'; SHE Pre-Qual confirmed current. Roster uncertainty (Avetta exit likely; PREQUAL issued Simply Security's 2026 report) — confirm by email"),
    ("Categories", "S sole trader $280/2yr; Cat 1 $450/2yr (<=20 people AND <=$2.5M contracts AND no high-risk primary); Cat 2 $949/1yr (<=200 people, <=$20M, no very-high-risk primary); Cat 3 $1,459/1yr (>200 people or >$20M or VHR primary). All +GST, SHE Prequal pricing"),
    ("ASG category", "Category 2, primary activity 'Security Services' (never 'Labour Hire' or 'Facilities Management' — both High-Risk list items). Security/guarding/crowd control/patrol absent from both risk lists (Scheme Rules v3.4.2 + High-Risk Definitions v1.2, verified twice independently)"),
    ("Category risk", "The $20M cap reads as whole-of-term ('does not take on contracts with value in excess of NZ$20M'); 'take on' is present practice, so Cat 2 is correct today, but a 5-yr PC award (~$22.5-25M) likely forces Cat 3 within the one-month recategorisation window"),
    ("Question set", "Cat 2 = MB1-MB54 (Core Criteria v3.4). Scoring 0-4 per question; 'Performing' = 3 on every applicable question, else 'Developing'. Expected NA set for a guarding firm: MB18, MB25, MB34, MB46-49 (Simply Security precedent)"),
    ("Process", "app.rapidcert.co.nz/signup/totika -> pay -> upload evidence per question -> first decision ~6 working days (urgent ~1 day, +$250+GST) -> clarification round(s) -> certificate + report -> upload proof to Totika dashboard. Fees non-refundable; clarification-fee treatment unverified"),
    ("Rules that bite", "Submission only by an employee or HASANZ-registered consultant. Personal info in evidence must be redacted. Insurance is outside Totika scoring but collected on the profile (buyers see it). Category change -> new assessment within 1 month or listing expires"),
    ("Precedent", "Simply Security Ltd: 179 staff, Category 2, 'Security Services', Performing at 81%, valid Jun 2026-Jun 2027, PL $10M / PI $1M / MV $10M — assessed by PREQUAL. The template outcome for ASG"),
    ("Provider contact", "SHE Pre-Qual (RJ Safety Consulting Ltd) — support@sheprequal.co.nz, 06 833 7227. Buy the TOTIKA product, not SHE's generic prequal"),
]


def p1_rows():
    out = []
    for r in REGISTER:
        if r['priority'] == 'P1-blocker':
            sec = r['section'].split(' NEW')[0]
            req = r['requirement']
            req = req if len(req) < 110 else req[:107] + '...'
            act = r['action']
            act = act if len(act) < 220 else act[:217] + '...'
            out.append([f"{sec}: {req}", r['status'], act])
    return out


def build_pdf():
    doc = BaseDocTemplate(PDF_OUT, pagesize=A4, leftMargin=ML, rightMargin=MR,
                          topMargin=MT, bottomMargin=MB, title='ASG Totika Prequalification Briefing')
    frame = Frame(ML, MB, CW, PAGE_H - MT - MB, id='main')
    doc.addPageTemplates([PageTemplate(id='all', frames=[frame], onPage=header_footer)])
    E = []

    # ---- title page
    E.append(Spacer(1, 110))
    E.append(HRFlowable(width='40%', thickness=1.2, color=GOLD, hAlign='CENTER'))
    E.append(Spacer(1, 22))
    E.append(Paragraph('Totika Prequalification',
                       ParagraphStyle('t1', fontName='Helvetica-Bold', fontSize=32, leading=38,
                                      textColor=NAVY, alignment=TA_CENTER)))
    E.append(Spacer(1, 10))
    E.append(Paragraph('Category 2 Readiness Briefing &amp; Evidence Compilation Plan',
                       ParagraphStyle('t2', fontName='Helvetica', fontSize=16, leading=21,
                                      textColor=DARKBLUE, alignment=TA_CENTER)))
    E.append(Spacer(1, 8))
    E.append(Paragraph('ETR agentic workflow: 9 agents, 3-lens adversarial verification',
                       ParagraphStyle('t3', fontName='Helvetica-Oblique', fontSize=12, leading=16,
                                      textColor=MIDBLUE, alignment=TA_CENTER)))
    E.append(Spacer(1, 22))
    E.append(HRFlowable(width='40%', thickness=1.2, color=GOLD, hAlign='CENTER'))
    E.append(Spacer(1, 46))
    info = [['Entity', 'Absolute Security Group Ltd (NZBN 9429050952960)'],
            ['Provider', 'SHE Pre-Qual via RapidCert (Totika member scheme)'],
            ['Category', "2 — primary activity 'Security Services'"],
            ['Cost', '$949 + GST per year ($1,091.35); urgent option +$250 + GST'],
            ['First decision', '~6 working days standard; ~1 working day urgent'],
            ['Companion file', 'ASG_Totika_Evidence_Register.xlsx (55 evidence lines)'],
            ['Prepared', '17 November 2026 — ETR run wf_2edef0ec-0a4']]
    it = Table([[Paragraph(f'<b>{a}</b>', S['cell']), Paragraph(b, S['cell'])] for a, b in info],
               colWidths=[CW * 0.22, CW * 0.58], hAlign='CENTER')
    it.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), LIGHTBLUE),
        ('BACKGROUND', (1, 0), (1, -1), BGGREY),
        ('GRID', (0, 0), (-1, -1), 0.4, BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    E.append(it)
    E.append(Spacer(1, 60))
    E.append(Paragraph('Internal working document. Facts verified against totika.org and sheprequal.co.nz '
                       'on 17 November 2026 by an adversarial fact-check pass; items marked unverified must be '
                       'confirmed with SHE Prequal before reliance.',
                       ParagraphStyle('disc', fontName='Helvetica-Oblique', fontSize=8, leading=11,
                                      textColor=TEXTM, alignment=TA_CENTER)))
    E.append(PageBreak())

    # ---- TOC
    E.append(SectionBar('', 'Contents'))
    toc = ['1.  Verdict', '2.  The Scheme — What Totika Is', '3.  Why ASG Needs It',
           '4.  The Category Decision', '5.  Cost, Process and Scoring',
           '6.  Where ASG Stands — Readiness', '7.  P1 Blockers',
           '8.  The Plan', '9.  Risks and Gates', '10.  Open Questions for Ahmad',
           '11.  Scheme Fact Sheet']
    for t in toc:
        E.append(Paragraph(t, S['toc1']))
    E.append(PageBreak())

    # ---- 1 verdict
    E.append(SectionBar(1, 'Verdict'))
    E.append(Paragraph('<b>GO — register ASG Ltd as Totika Category 2 via SHE Prequal, but run the evidence '
                       'sprint first and time the submission deliberately.</b>', S['bodyL']))
    E.append(Paragraph('The scheme fit is confirmed: security guarding sits on neither risk list, ASG lands in '
                       'Category 2 by size and contract value, and the direct precedent — Simply Security Ltd, '
                       '179 staff, Category 2 "Security Services", Performing at 81% — is the template outcome. '
                       'Cost is modest ($949 + GST per year) and Te Whatu Ora, a live ASG bid target, is a '
                       'displayed Totika buyer.', S['body']))
    E.append(Paragraph('The readiness picture (revised after the 17 Nov full-filesystem sweep, 8 agents, '
                       '2 adversarial verifiers): ASG is far better evidenced than first believed, but lopsidedly. '
                       'The OPERATING layer is deep — ~980 dated daily patrol logs with timestamped welfare checks '
                       '(Mar 2024 to 15 Nov 2026), incident registers at scale (1,740 Bunnings + 4,971 Woolworths '
                       'entries), two complete investigations with corrective actions, a filled hazard register, '
                       'DocuSign-executed induction packs, current COA registers and a live graduated '
                       'return-to-work plan. The GOVERNANCE layer is what is absent: zero management or committee '
                       'minutes, zero toolbox delivery/attendance records, zero completed H&amp;S inspections, '
                       'zero drills, zero vehicle records, no completed internal audit. The single biggest unlock '
                       'is not on the filesystem: Connecteam makes a "Health &amp; Safety Toolbox Meeting (APP '
                       'FORM)" a mandatory task on every rostered shift — exporting those form submissions may '
                       'flip toolbox evidence to HAVE in one move. The plan splits into live records that must '
                       'actually happen (about 3 hours, before PC submission week) and build/collation work '
                       '(26-28 Nov).', S['body']))
    E.append(Spacer(1, 4))
    counts = {}
    for r in REGISTER:
        counts[r['status']] = counts.get(r['status'], 0) + 1
    E.append(datatable(['Evidence lines', 'HAVE', 'PARTIAL', 'MISSING', 'UNKNOWN', 'P1 blockers'],
                       [[str(len(REGISTER)), str(counts.get('HAVE', 0)), str(counts.get('PARTIAL', 0)),
                         str(counts.get('MISSING', 0)), str(counts.get('UNKNOWN', 0)),
                         str(sum(1 for r in REGISTER if r['priority'] == 'P1-blocker'))]],
                       [CW/6.0]*6))
    E.append(PageBreak())

    # ---- 2 scheme
    E.append(SectionBar(2, 'The Scheme — What Totika Is'))
    E.append(Paragraph('Totika is New Zealand\'s national cross-recognition framework for health and safety '
                       'prequalification, governed by the CHASNZ board of trustees (not-for-profit). A supplier '
                       'completes one assessment with any approved member scheme and is listed on the central '
                       'register (app.totika.org); every buyer member accepts that listing. Prequalify once, not '
                       'once per client. Supplier registration on the portal is free — the fee is paid to the '
                       'member scheme for the assessment itself. The official domain is totika.org; totika.org.nz '
                       'does not resolve.', S['body']))
    E.append(Paragraph('A registered-but-unassessed supplier is not visible to buyers, so registration alone '
                       'proves nothing. Assessments are answered against a published question set (Core Criteria '
                       'v3.4, questions MB1-MB54 at Category 2) and scored 0-4 per question by a qualified '
                       'assessor.', S['body']))
    E.append(Paragraph('Member schemes', S['h3']))
    E.append(Paragraph('totika.org currently references "our three member schemes". SHE Pre-Qual (RJ Safety '
                       'Consulting Ltd, Napier — assessments on the RapidCert platform) is confirmed current. '
                       'The wider roster is genuinely uncertain: older material listed four schemes including '
                       'Avetta, and Simply Security\'s June 2026 report was issued by PREQUAL. All member schemes '
                       'assess the identical national standard, so output is equivalent; SHE\'s published pricing '
                       'and ~6-working-day turnaround plus NZ phone support make it a sound choice. One email '
                       'confirms the roster (step 5 of the plan).', S['body']))
    E.append(PageBreak())

    # ---- 3 why
    E.append(SectionBar(3, 'Why ASG Needs It'))
    E.append(Paragraph('Confirmed buyers', S['h3']))
    E.append(Paragraph('Over forty buyer organisations are displayed on totika.org, including: '
                       '<b>Te Whatu Ora - Health New Zealand</b> (ASG\'s submitted RFP 0018709), Auckland '
                       'Council, Auckland Transport, Eke Panuku, Watercare, SkyCity, Auckland Airport, St John, '
                       'NZTA, Fonterra and IAG — essentially ASG\'s target client list for CBD, precinct and '
                       'corporate work.', S['body']))
    E.append(Paragraph('The Woolworths correction', S['h3']))
    E.append(Paragraph('<b>Woolworths / Primary Connect is not a Totika buyer.</b> Woolworths runs its own '
                       'prequalification through the Site360 (WOW Contractor) portal. For DC tender 523941, '
                       'Totika is supporting H&amp;S evidence inside the response, not the binding prequal — '
                       'verify in the tender documents (by 20 Nov) before paying for urgency, and plan for '
                       'Site360 onboarding if awarded.', S['body']))
    E.append(Paragraph('Competitor parity', S['h3']))
    E.append(Paragraph('<b>Simply Security Ltd</b> — 179 staff, near-identical scale — holds Category 2, primary '
                       'activity "Security Services", Performing at 81%, insurances PL $10M / PI $1M / MV $10M '
                       '(fully confirmed from its published report). Claims that FIRST Security, Armourguard and '
                       'P4G hold Totika/PREQUAL/SiteWise could not be verified from public sources — the supplier '
                       'register needs a buyer login — and are treated as plausible only.', S['body']))
    E.append(PageBreak())

    # ---- 4 category
    E.append(SectionBar(4, 'The Category Decision'))
    E.append(Paragraph('<b>Category 2, primary work activity "Security Services" — independently verified '
                       'twice.</b>', S['bodyL']))
    E.append(Paragraph('Security guarding, crowd control and patrol appear on neither the 35-item High-Risk list '
                       'nor the 25-item Very-High-Risk list (full-text extraction of Scheme Rules v3.4.2 and the '
                       'High-Risk Work Activity List Definitions v1.2; zero occurrences of "security", "crowd", '
                       '"guard" or "patrol"; re-verified by the adversarial category lens). Category therefore '
                       'follows size and contract value. Category 1 is excluded on two independent legs: ASG '
                       'exceeds 20 people, and tendering $4.5-5M/yr contracts alone disqualifies it. No entity '
                       'approaches 200 people, so Category 3\'s headcount trigger is clear.', S['body']))
    E.append(datatable(['Category', 'Thresholds', 'Price (+GST)', 'Validity'],
                       [['S Sole trader', 'Individual working alone', '$280', '2 years'],
                        ['1', '<=20 people AND <=$2.5M contracts AND no high-risk primary activity', '$450', '2 years'],
                        ['2  (ASG)', '<=200 people, <=$20M contracts, no very-high-risk primary activity', '$949', '1 year'],
                        ['3', '>200 people, or >$20M contracts, or very-high-risk primary activity', '$1,459', '1 year']],
                       [CW*0.16, CW*0.48, CW*0.17, CW*0.19], bold_rows=(2,)))
    E.append(Paragraph('Three live caveats', S['h3']))
    E.append(Paragraph('<bullet>&bull;</bullet><b>The $20M cap reads whole-of-term.</b> The rules say a Category 2 supplier '
                       '"does not take on contracts with value in excess of NZ$20 million" — the natural reading '
                       'is total contract value, not per annum. "Take on" is present practice, so Category 2 is '
                       'correct today; but a 5-year PC DC award at $4.5-5M/yr (~$22.5-25M) would likely force '
                       'Category 3. Confirm the measurement basis with SHE Prequal before paying.', S['bullet']))
    E.append(Paragraph('<bullet>&bull;</bullet><b>The one-month rule.</b> If the business changes such that the category '
                       'changes, a new assessment must be completed within one month or the listing expires. A PC '
                       'award or the Liberty subcontracting flip are award-day obligations, not renewal items.', S['bullet']))
    E.append(Paragraph('<bullet>&bull;</bullet><b>Per-entity listing.</b> The rules count only the supplier\'s own people with '
                       'no group consolidation; listings are per legal entity (per the registration flow — '
                       'confirm with SHE). SLS RTC Ltd would need its own $949+GST assessment if a buyer requires '
                       'it listed. Buyers have no mechanism inside the scheme to dictate a supplier\'s category.', S['bullet']))
    E.append(Paragraph('Declare "Security Services" as primary activity — never "Labour Hire" or "Facilities '
                       'Management", both of which sit on the High-Risk list. Even a worst-case mislabel lands '
                       'Category 2, not 3; only a very-high-risk primary activity forces Category 3.', S['body']))
    E.append(PageBreak())

    # ---- 5 cost/process
    E.append(SectionBar(5, 'Cost, Process and Scoring'))
    E.append(datatable(['Item', 'Detail'],
                       [['Assessment fee', 'Category 2: $949 + GST = $1,091.35 per year, paid to SHE Prequal. Non-refundable (T&amp;Cs verbatim)'],
                        ['Urgent option', '+$250 + GST — first decision ~1 working day instead of ~6'],
                        ['Totika portal', 'Free supplier registration at app.totika.org'],
                        ['Second entity', 'SLS RTC Ltd if ever needed: another $949 + GST per year'],
                        ['Year-one budget', '~$1,100 incl GST (ASG only, standard track); ~$2,500 if urgent + both entities'],
                        ['Clarifications', 'Assessor may request further information; whether rounds are included in the fee is UNVERIFIED — ask before paying'],
                        ['Signup', 'app.rapidcert.co.nz/signup/totika — buy the TOTIKA product, not SHE\'s generic prequal'],
                        ['Submitter', 'Must be an ASG employee or a HASANZ-registered consultant'],
                        ['Redaction', 'Personal identifying information in uploaded evidence must be redacted (scheme rule)']],
                       [CW*0.24, CW*0.76]))
    E.append(Paragraph('Scoring', S['h3']))
    E.append(Paragraph('Each applicable question (MB1-MB54) is scored 0-4 against published anchors. '
                       '<b>"Performing" requires a 3 on every applicable question</b> — a single 2 grades the '
                       'whole assessment "Developing" (still listed, lower standing). Construction-only sections '
                       'are answered NA with justification; the expected NA set for a guarding firm is MB18 '
                       '(hazardous-work licences), MB25 (site emergency plans), MB34 (health monitoring) and '
                       'MB46-49 (hazardous substances), exactly as in the Simply Security report. Insurance is '
                       'outside Totika scoring but is collected on the supplier profile and visible to buyers — '
                       'ASG already matches the PL $10M benchmark; the open PI decision closes the gap.', S['body']))
    E.append(PageBreak())

    # ---- 6 readiness
    E.append(SectionBar(6, 'Where ASG Stands — Readiness (post-sweep, 17 Nov)'))
    E.append(Paragraph('Operating layer — deep, verified by adversarial re-read', S['h3']))
    for s in ['~980 dated HOTC daily patrol logs Mar 2024 - 15 Nov 2026: timestamped welfare checks + an equipment-issue block every shift (lone-worker + PPE evidence; typed, unsigned)',
              'Incident registers at scale: Bunnings GIR 1,740 named dual-timestamped entries (signature images live in the form platform, not the xlsx) + Woolworths GIR 4,971 FY26 entries + 151 severe-incident entries',
              'Two complete investigations: Cotton On (incident 6 Sep 26 -> statement -> video review -> substantiated finding -> corrective actions) + Investigation Summary 19 Mar 26 (minuted disciplinary process, legal review)',
              'CRL First Looks incident report (issued 25 Aug 26) with explicit HSWA s23-25 notifiable-event determinations',
              'Filled company Hazard &amp; Risk Register (needs re-dating: two lapsed review dates; restructure so violence/aggression leads)',
              'Training/competency: 31-name PSPLA-verified COA register (10 Nov 26) + 22-name CoA return + 29 ServeWise certs + Onboarding pack.xlsx (39 officers x 9 document types, partially populated — the matrix to complete, not build)',
              'Induction: 5 DocuSign-executed witnessed Mitre 10 packs + ~24 onboarding packs + 65 CRL induction attendance entries',
              'Live graduated return-to-work plan (occupational therapist, 9 Nov - 21 Dec 2026) — injury-management evidence',
              'Performance reporting: quarterly value reviews 2024-26 + 28 consecutive weekly WW LP &amp; Safety reports + LCF accountability report',
              'Signed policy-acknowledgement mechanism proven (James Olsen WW SOP ack; witness block incomplete)']:
        E.append(Paragraph(f'<bullet>&bull;</bullet>{s}', S['bullet']))
    E.append(Paragraph('Governance layer — the true gap (sweep-confirmed absent everywhere)', S['h3']))
    E.append(Paragraph('Zero across all slices: management meeting minutes + KPI setting (MB5); H&amp;S committee '
                       'minutes (MB27); toolbox DELIVERY/attendance records (MB28 — content library exists in 10+ '
                       'locations; Connecteam export is the unlock); completed H&amp;S inspections (MB37-38); '
                       'completed internal audit (MB14 — the WW ethical self-audit is 30 minutes from usable); '
                       'drills; vehicle records; sign-offs against ASG\'s OWN policy/induction (client-doc '
                       'acknowledgements exist instead). The completed Reign &amp; Pour investigation report '
                       'promised to the client by 27 Oct is also not on disk — locate or write it. Tender texts '
                       'commit to several of these as recurring cadences (weekly inspections, monthly toolbox with '
                       'recorded attendance, monthly hazard-register reviews), so claims hygiene remains a P1 '
                       'line: stand the cadences up or soften the wording. Assessors want systems in use over 3-6 '
                       'months; the operating layer proves that richly — the governance layer must start now so '
                       'at least a few weeks of cadence exist by submission.', S['body']))
    E.append(PageBreak())

    # ---- 7 P1 table
    E.append(SectionBar(7, 'P1 Blockers'))
    E.append(Paragraph('The 19 lines the assessment fails without. Full 55-line register with file paths and '
                       'owners: ASG_Totika_Evidence_Register.xlsx.', S['body']))
    E.append(datatable(['Requirement', 'Status', 'Action'], p1_rows(),
                       [CW*0.34, CW*0.11, CW*0.55], status_col=1))
    E.append(PageBreak())

    # ---- 8 plan
    E.append(SectionBar(8, 'The Plan'))
    for step, owner, when, detail in ACTION_PLAN:
        E.append(KeepTogether([
            Paragraph(f'<b>{esc(step)}</b> &nbsp;&nbsp;<font color="#4A6FA5">{esc(owner)} - {esc(when)}</font>', S['h3']),
            Paragraph(esc(detail), S['body'])]))
    E.append(PageBreak())

    # ---- 9 risks
    E.append(SectionBar(9, 'Risks and Gates'))
    risks = [
        ('Reign &amp; Pour notifiability — CLEARED 17 Nov',
         'Ahmad confirms the Oct 2026 incident did not meet the HSWA s23 notifiable-event threshold (no injury '
         'requiring notification), so no WorkSafe notification was required. The nil declaration in PC Q8.5 '
         'stands on that confirmation and the incident can be used as a root-cause investigation example.'),
        ('Claims hygiene',
         'SafetySeek, the Deputy-linked training register, weekly inspections and monthly toolboxes are tender '
         'claims not yet evidenced on disk. Verify or drop each before it is repeated to an assessor; the 24 '
         'bracketed placeholders in the PC draft answers are the not-yet-real list.'),
        ('Entity mis-targeting',
         'The Woolworths relationship sits with SLS RTC Ltd. If SLS RTC is the named bidder in PC 523941, an '
         'ASG-only listing misses the biggest driver — and SLS RTC\'s lagging Companies Register (Nikki still a '
         'recorded director) contaminates its director declarations until fixed.'),
        ('Timing honesty',
         'Standard track with one clarification round lands late Dec 2026 — or mid-Jan 2027 across the Christmas '
         'shutdown (SHE\'s cutoff unverified; ask in the step-5 email). Survivable: the only confirmed buyer '
         'deadline is HNZ award ~Feb 2027. A listing is NOT achievable before the 25 Nov PC submission on the '
         'standard track; the tender wording in step 4 covers it truthfully.'),
        ('Developing vs Performing',
         'One sub-3 score anywhere grades Developing. Freshly minted records make 2s plausible on the '
         'engagement/leadership questions (MB5, MB27, MB28, MB37). Mitigation: run the cadence for 4+ weeks '
         'before submitting, or accept Developing first and re-mark at clarification/renewal.'),
        ('Liberty flip',
         'If the Fernando+Jason/Liberty B2B restructure goes live, the "no subcontracting" NA (MB39-42) dies and '
         'a real subcontractor-management procedure + prequal examples become mandatory — within one month, per '
         'the recategorisation rule, not at renewal.')]
    for t, d in risks:
        E.append(KeepTogether([Paragraph(t, S['h3']), Paragraph(d, S['body'])]))
    E.append(PageBreak())

    # ---- 10 open questions
    E.append(SectionBar(10, 'Open Questions for Ahmad'))
    E.append(datatable(['#', 'Topic', 'Question'],
                       [[str(i + 1), t, q] for i, (t, q) in enumerate(OPEN_QUESTIONS)],
                       [CW*0.05, CW*0.20, CW*0.75]))
    E.append(PageBreak())

    # ---- 11 fact sheet
    E.append(SectionBar(11, 'Scheme Fact Sheet'))
    E.append(datatable(['Item', 'Fact'], [[a, b] for a, b in SCHEME_FACTS], [CW*0.2, CW*0.8]))
    E.append(Spacer(1, 10))
    E.append(Paragraph('Verification note: every pricing, category, risk-list, scoring and process fact above '
                       'survived an adversarial fact-check against totika.org and sheprequal.co.nz on 17 Nov 2026 '
                       '(Scheme Rules v3.4.2, High-Risk Definitions v1.2, Core Criteria v3.4, SHE T&amp;Cs). '
                       'Flagged as unverified: clarification-round fee treatment, current member-scheme roster, '
                       'per-NZBN listing mechanics, SHE\'s Christmas cutoff — all resolved by the step-5 email.',
                       S['small']))
    doc.build(E)
    print('PDF ->', PDF_OUT)


def build_xlsx():
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    NAVY_F = PatternFill('solid', fgColor='1B2A4A')
    ALT_F = PatternFill('solid', fgColor='F2F4F8')
    GOLD_F = PatternFill('solid', fgColor='F7EEDB')
    HDR = Font(name='Calibri', size=10, bold=True, color='FFFFFF')
    B = Font(name='Calibri', size=10)
    BB = Font(name='Calibri', size=10, bold=True)
    WRAP = Alignment(wrap_text=True, vertical='top')
    CTR = Alignment(horizontal='center', vertical='top')
    THIN = Border(*[Side(style='thin', color='D0D5DD')] * 4)
    STAT_FONT = {'HAVE': Font(name='Calibri', size=10, bold=True, color='27AE60'),
                 'PARTIAL': Font(name='Calibri', size=10, bold=True, color='E67E22'),
                 'MISSING': Font(name='Calibri', size=10, bold=True, color='C0392B'),
                 'UNKNOWN': Font(name='Calibri', size=10, bold=True, color='4A4A5A')}

    wb = Workbook()

    def sheet(ws, headers, widths):
        for c, (h, w) in enumerate(zip(headers, widths), 1):
            cell = ws.cell(1, c, h)
            cell.font = HDR; cell.fill = NAVY_F; cell.alignment = WRAP; cell.border = THIN
            ws.column_dimensions[get_column_letter(c)].width = w
        ws.freeze_panes = 'A2'

    ws = wb.active; ws.title = 'Evidence Register'
    sheet(ws, ['Section', 'Requirement', 'Evidence needed', 'Status', 'Priority',
               'Existing source on disk', 'Action to close'], [16, 36, 42, 11, 12, 44, 60])
    for i, r in enumerate(REGISTER, 2):
        vals = [r['section'], r['requirement'], r['evidence_needed'], r['status'],
                r['priority'], r.get('existing_source') or '-', r['action']]
        for c, v in enumerate(vals, 1):
            cell = ws.cell(i, c, v)
            cell.font = STAT_FONT[r['status']] if c == 4 else B
            cell.alignment = CTR if c in (4, 5) else WRAP
            cell.border = THIN
            if r['priority'] == 'P1-blocker' and c == 5:
                cell.font = Font(name='Calibri', size=10, bold=True, color='C0392B')
            if i % 2 == 0:
                cell.fill = ALT_F
    ws.auto_filter.ref = f'A1:G{len(REGISTER) + 1}'

    ws = wb.create_sheet('Action Plan')
    sheet(ws, ['Step', 'Owner', 'When', 'Detail'], [34, 24, 22, 110])
    for i, (step, owner, when, detail) in enumerate(ACTION_PLAN, 2):
        for c, v in enumerate([step, owner, when, detail], 1):
            cell = ws.cell(i, c, v)
            cell.font = BB if c == 1 else B
            cell.alignment = WRAP; cell.border = THIN
            if i % 2 == 0:
                cell.fill = ALT_F

    ws = wb.create_sheet('Open Questions (Ahmad)')
    sheet(ws, ['#', 'Topic', 'Question', 'Answer'], [5, 22, 90, 40])
    for i, (t, q) in enumerate(OPEN_QUESTIONS, 2):
        for c, v in enumerate([i - 1, t, q, ''], 1):
            cell = ws.cell(i, c, v)
            cell.font = BB if c == 2 else B
            cell.alignment = WRAP; cell.border = THIN
            if c == 4:
                cell.fill = GOLD_F
    ws.cell(1, 4).comment = None

    ws = wb.create_sheet('Scheme Facts')
    sheet(ws, ['Item', 'Fact (verified 17 Nov 2026 unless flagged)'], [22, 130])
    for i, (a, b) in enumerate(SCHEME_FACTS, 2):
        ws.cell(i, 1, a).font = BB; ws.cell(i, 1).alignment = WRAP; ws.cell(i, 1).border = THIN
        ws.cell(i, 2, b).font = B; ws.cell(i, 2).alignment = WRAP; ws.cell(i, 2).border = THIN
        if i % 2 == 0:
            ws.cell(i, 1).fill = ALT_F; ws.cell(i, 2).fill = ALT_F

    wb.save(XLSX_OUT)
    print('XLSX ->', XLSX_OUT)


if __name__ == '__main__':
    build_xlsx()
    build_pdf()
