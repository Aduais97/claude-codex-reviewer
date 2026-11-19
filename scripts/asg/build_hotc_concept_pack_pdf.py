#!/usr/bin/env python3
"""HOTC Business App Concept Pack (joint HOTC + ASG document).
Built from Edward Caughey's 27 Oct 2026 brainstorm notes via the ETR workflow
(Codex gpt-5.6-terra + 4 Claude lenses: client-reader, strategy/IP, privacy/honesty,
anti-slop; ~88 findings applied). Master copy: session scratchpad hotc_concept_pack_FINAL_v2.md.
Key engineered positions: platform licence = RECOMMENDED structure, decision deferred to the
written agreement; dispatch = operating service "different in kind" from data feeds; s11 AGENT
(not "processor") wording with own-records carve-out; purposes closed-list with
aggregated/de-identified qualifier; disavowals scoped to "this app"; governance = HOTC publish
authority. No em-dashes.
Output: ~/Desktop/ASG/HOTC-Reporting-App/HOTC_Business_App_Concept_Pack.pdf
"""
from pathlib import Path
from fpdf import FPDF

NAVY = (31, 56, 100)      # HOTC house navy #1F3864
GOLD = (176, 141, 60)
INK = (40, 45, 55)
GRAY = (110, 118, 130)
LIGHT = (243, 245, 248)

OUT = Path.home() / 'Desktop/ASG/HOTC-Reporting-App/HOTC_Business_App_Concept_Pack.pdf'


class Pack(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('Helvetica', '', 8)
        self.set_text_color(*GRAY)
        self.cell(0, 5, 'HOTC Business App | Concept Pack | Heart of the City with ASG Security',
                  new_x='LMARGIN', new_y='NEXT')
        self.ln(3)

    def footer(self):
        self.set_y(-13)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(*GRAY)
        self.cell(0, 5, f'{self.page_no()}', align='C')

    def section(self, num, title):
        if self.get_y() > 235:
            self.add_page()
        self.ln(4)
        self.set_font('Helvetica', 'B', 15)
        self.set_text_color(*GOLD)
        self.cell(10, 8, num)
        self.set_text_color(*NAVY)
        self.cell(0, 8, title, new_x='LMARGIN', new_y='NEXT')
        self.set_draw_color(*GOLD)
        self.set_line_width(0.5)
        self.line(self.l_margin, self.get_y() + 0.5, self.l_margin + 55, self.get_y() + 0.5)
        self.ln(3.5)

    def body(self, text, size=10, after=2.5):
        self.set_font('Helvetica', '', size)
        self.set_text_color(*INK)
        self.multi_cell(0, 4.9, text, new_x='LMARGIN', new_y='NEXT')
        self.ln(after)

    def kicker(self, text):
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(*GRAY)
        self.multi_cell(0, 4.6, text, new_x='LMARGIN', new_y='NEXT')
        self.ln(0.5)

    def quote(self, text):
        x = self.get_x()
        self.set_fill_color(*LIGHT)
        self.set_font('Helvetica', 'I', 11)
        self.set_text_color(*NAVY)
        self.set_x(x + 3)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 6, 5.6, text, fill=True,
                        new_x='LMARGIN', new_y='NEXT')
        self.set_x(x)
        self.ln(2.5)

    def bullet(self, lead, text, size=9.6):
        self.set_font('Helvetica', 'B', size)
        self.set_text_color(*NAVY)
        self.cell(4, 4.8, '-')
        if lead:
            w = self.get_string_width(lead + ' ') + 1
            self.cell(w, 4.8, lead)
        self.set_font('Helvetica', '', size)
        self.set_text_color(*INK)
        self.multi_cell(0, 4.8, text, new_x='LMARGIN', new_y='NEXT')
        self.ln(1.2)


pdf = Pack(format='A4')
pdf.set_auto_page_break(auto=True, margin=18)
pdf.set_margins(18, 16, 18)
pdf.add_page()

# Cover block
pdf.ln(28)
pdf.set_font('Helvetica', 'B', 30)
pdf.set_text_color(*NAVY)
pdf.cell(0, 13, 'HOTC Business App', new_x='LMARGIN', new_y='NEXT')
pdf.set_font('Helvetica', '', 15)
pdf.set_text_color(*GOLD)
pdf.cell(0, 9, 'Concept pack: vision, users, proposition and first use cases',
         new_x='LMARGIN', new_y='NEXT')
pdf.ln(6)
pdf.set_font('Helvetica', '', 10.5)
pdf.set_text_color(*GRAY)
pdf.cell(0, 6, 'Heart of the City, with ASG Security', new_x='LMARGIN', new_y='NEXT')
pdf.cell(0, 6, 'Prepared for Edward Caughey and Jessie Vlasich  |  October 2026',
         new_x='LMARGIN', new_y='NEXT')
pdf.ln(10)
pdf.body('This pack turns the brainstorm notes of 27 October into a testable concept. It is '
         'deliberately not a technical specification or a feature list. It is the vision, the '
         'target user, the core proposition and the priority use cases, ready to put in front '
         'of frontline staff.', size=11)

pdf.add_page()
pdf.section('1', 'The vision')
pdf.kicker("Edward's wording from the brainstorm, kept as the anchor:")
pdf.quote('"Create a trusted, direct connection with businesses and their people working '
          'across the city centre, helping them feel safer, better informed and more connected '
          'to what is happening around them."')
pdf.body('The opportunity is bigger than a member app. It is a direct relationship with the '
         'frontline people who experience the city every day: store managers, hotel staff, '
         'hospitality workers, receptionists, security staff and office workers, whether or '
         'not their business is a formal member. Safety is the way in, because it is the thing '
         'every frontline worker relates to on day one.')
pdf.body('The end state is worth naming: year one targets 1,000 to 2,000 users, and the '
         "ambition beyond it is Heart of the City's direct relationship with 5,000 to 10,000 "
         'city centre workers. An owned, CRM-grade audience no email list can match, and a '
         'chance to lead: every city centre faces this same frontline problem, and HOTC can '
         'set the standard with the first and best answer to it.')

pdf.section('2', 'Who it is for')
pdf.body('Primary user: anyone working in a business in the city centre. Not tied to formal '
         'member representatives: open to any city centre worker, simple to join, with '
         "approval at HOTC's discretion so the audience grows deliberately.")
pdf.kicker('Five faces of that user, and the moment the app serves them:')
pdf.bullet('The store manager on Queen Street:', 'something is happening outside the shop right now.')
pdf.bullet('The hotel duty manager:', 'a protest will close the street to the lobby on Saturday.')
pdf.bullet('The hospitality worker closing at 1am:', 'wants one tap to the right help, not a phone tree.')
pdf.bullet('The receptionist or office worker:', 'wants to know what the disruption is before the questions start.')
pdf.bullet('The security officer or building manager:', 'wants one channel where city information is verified, not rumour.')
pdf.body('How joining works (draft, for testing): apply with name, employer, role and a work '
         'contact; HOTC approves against one simple rule (works in a city centre business), '
         'with a target turnaround of one working day; periodic re-confirmation keeps the '
         'audience current, and access ends when someone leaves their city role.')

pdf.section('3', 'The proposition, and how adoption builds')
pdf.kicker('The answer to the key question in the brainstorm (what would make a frontline '
           'worker download it, keep it and trust it), in one sentence:')
pdf.quote('"Know what\'s happening in the city, what affects you, and get help fast when '
          'something is wrong, from the city\'s own safety team on the street."')
pdf.kicker('The adoption ladder, from the brainstorm, is the organising logic:')
pdf.bullet('1. GET IT DOWNLOADED:', 'safety. One-tap incident reporting and real help.')
pdf.bullet('2. KEEP IT INSTALLED:', 'everyday utility. Report a public-realm issue, see what '
           'affects your street today.')
pdf.bullet('3. BUILD TRUST:', 'relevant, reliable, verified information, appropriately targeted.')
pdf.bullet('4. GROW ENGAGEMENT:', 'connection, communications and services: the city centre '
           'community layer. Recognition will matter more than points here: reporters who see '
           'what their reports led to, and businesses recognised in the HOTC channel for '
           'looking out for their street. The concept test probes which forms of '
           'recognition workers value.')

if pdf.get_y() > 150:
    pdf.add_page()
pdf.section('4', 'The top five use cases')
pdf.body('Framed by the three moments from the brainstorm. Each use case is described as it '
         'will work once built; the source and dispatch connections are established in the build.')

uc = [
    ('1', 'Something is\nhappening now', 'Report an incident,\nget a response',
     'Report in under 30 seconds. It reaches the Safety Team on the street in real time, and '
     'the reporter sees it was received and what happened next. The reporting screen leads '
     'with: emergency now, call 111.'),
    ('2', 'Something is\nhappening now', 'Verified safety alert',
     'A verified alert about an incident nearby, sent only to the people it affects, only '
     'when it matters.'),
    ('3', 'It will affect me', 'Disruption notices',
     'Protests, closures, works, major events: what, where, when and what to do, drawing on '
     'agreed sources across Council, AT, Police, CRL and event organisers.'),
    ('4', 'Normal day', 'Report a city issue',
     'Graffiti, broken lighting, dumped rubbish: photograph, tap, done, routed to the right '
     'owner, with HOTC tracking that it lands.'),
    ('5', 'Normal day', 'The city channel',
     "What's on this week, HOTC news and member offers, opportunities to get involved. The "
     'reason to open the app on a quiet Tuesday.'),
]
cw = [8, 32, 40, 94]
pdf.set_font('Helvetica', 'B', 9)
pdf.set_fill_color(*NAVY)
pdf.set_text_color(255, 255, 255)
for w, h in zip(cw, ['#', 'Moment', 'Use case', 'What the app will do']):
    pdf.cell(w, 6.5, h, fill=True, border=1)
pdf.ln()
pdf.set_text_color(*INK)
for n, m, u, d in uc:
    pdf.set_font('Helvetica', '', 8.8)
    x0, y0 = pdf.get_x(), pdf.get_y()
    lines = pdf.multi_cell(cw[3], 4.4, d, split_only=True)
    rh = max(len(lines) * 4.4 + 2.4, 11)
    if y0 + rh > 270:
        pdf.add_page(); x0, y0 = pdf.get_x(), pdf.get_y()
    pdf.set_font('Helvetica', 'B', 9); pdf.set_xy(x0, y0); pdf.cell(cw[0], rh, n, border=1)
    pdf.set_font('Helvetica', '', 8.8)
    pdf.set_xy(x0 + cw[0], y0); pdf.multi_cell(cw[1], 4.4, m, border=1)
    pdf.set_font('Helvetica', 'B', 8.8)
    pdf.set_xy(x0 + cw[0] + cw[1], y0); pdf.multi_cell(cw[2], 4.4, u, border=1)
    pdf.set_font('Helvetica', '', 8.8)
    pdf.set_xy(x0 + cw[0] + cw[1] + cw[2], y0); pdf.multi_cell(cw[3], 4.4, d, border=1)
    # square off shorter cells
    for cx, w in zip([x0, x0 + cw[0], x0 + cw[0] + cw[1], x0 + cw[0] + cw[1] + cw[2]], cw):
        pdf.rect(cx, y0, w, rh)
    pdf.set_xy(x0, y0 + rh)
pdf.ln(3)

pdf.body('Use case 1 is the differentiator. Reporting apps are common; a reporting app wired '
         'directly into the dispatch of a response team already walking the street is not. '
         'The Safety Team (the street patrol ASG operates for Heart of the City) attended '
         'every one of the 607 business calls it received in the three months to September, '
         'and that record comes from the patrol, the dispatch workflow and the escalation '
         'pathways operating as one system. The app puts that existing, proven response '
         'within one tap of thousands of workers who today have no direct way to raise it. '
         'Where an incident needs Police, the report is structured so the handover is '
         'complete first time, with nothing to re-collect.')
pdf.body("Use case 5 is the comms team's channel, and it works only if it costs that team "
         'nothing extra: HOTC comms owns the editorial, the channel reuses the content '
         'streams HOTC already publishes, and a simple publishing tool for the comms team is '
         'part of the first build. The launch-week seeding plan is a named output of the '
         'design sprint.')

pdf.section('5', 'What earns trust')
pdf.kicker('Rung three of the ladder is trust. Five things earn it:')
pdf.bullet('Verified before sent.', 'Each alert shows its source and follows an agreed '
           'publishing and approval process.')
pdf.bullet('Targeted.', 'Street-level relevance and user-selected settings, not city-wide blasts.')
pdf.bullet('Two-way.', 'Reports are acknowledged, and reporters learn the outcome: status '
           'updates that confirm what happened, not personal details.')
pdf.bullet('Careful with alerts.', 'Alerts describe behaviour, risk and what to do. They '
           'never identify individuals, name locations only as precisely as safety requires, '
           'and if an alert turns out to be wrong, a correction goes to the same audience.')
pdf.bullet('Private by design.', 'Built under the Privacy Act 2020 from day one. Personal '
           'information is collected only for stated purposes: service delivery, safety '
           "response, and HOTC's analytics, reporting and benchmarking in aggregated or "
           'de-identified form. No facial recognition in this app, and no sharing of '
           "individuals' information between businesses in anything proposed here; if HOTC "
           'ever considered capability of that kind, it would be a separate decision, taken '
           'only after a privacy impact assessment and with clear notice to users. Incident '
           'reports will often contain information about third parties; the privacy review '
           'sets the rules for photographing people, who can see reports, how long they are '
           'kept, and what outcome updates contain.')

pdf.section('6', 'What the first version is, and is not')
pdf.body('The MVP is the thin slice of use cases 1 and 2: report an incident, reach the team, '
         'receive verified alerts. Two use cases is enough to learn the only thing that '
         'matters: will frontline workers report through it, and do they act on the alerts. '
         'Use cases 3 to 5 layer on in planned releases once the safety core has earned its '
         'place on the phone.')
pdf.body('The MVP is deliberately not: a social feed, an offender database, a camera or '
         'facial recognition system, or a replacement for 111 (any emergency happening now '
         'goes to Police first, and the app says so at the point of reporting). It is also '
         "not a replacement for HOTC's existing member CRM; over time it becomes something "
         "the CRM cannot be, HOTC's relationship system for a new audience: the workers "
         'themselves.')
pdf.body('Sequenced, not dropped: community and connection features (rung four) are explored '
         'once the safety core is established, informed by the concept test, and later '
         'releases explore live two-way service, ask the city a question and get a human answer.')

pdf.section('7', 'What success looks like in year one')
pdf.kicker('Measures from the brainstorm, each with how it is evidenced:')
pdf.bullet('', '1,000 to 2,000 verified frontline users, with representation across retail, '
           'hospitality, hotels, offices and services (measured in the app, by sector).')
pdf.bullet('', 'The leading business alert channel for the city centre: alert delivery and '
           "acknowledgement rates measured against the current email channel's reach and "
           'engagement (baseline from HOTC comms).')
pdf.bullet('', 'Reporting that works: report volumes, acknowledgement times, and the '
           'proportion of users retained after 90 days. Response times become formally '
           'trackable through the app, which the current phone-and-email channel cannot '
           'offer, with a response-time target set once the first-quarter baseline exists.')
pdf.bullet('', 'Growing engagement with HOTC: opens, member-content engagement, and user '
           'trust and usefulness scores from in-app pulse questions.')
pdf.bullet('', "A direct, owned communications channel that complements HOTC's email, web "
           'and social channels rather than duplicating them.')

pdf.section('8', 'Ownership, architecture and governance')
pdf.kicker('Reflecting the principles in the brainstorm, stated plainly so the build can be '
           'structured correctly from day one:')
pdf.bullet('HOTC owns the app:', 'the brand, the user relationships, the communications '
           'channel, and the reports and personal information collected through it. These '
           "are HOTC's asset, held in HOTC's own secure partition and exportable in full at "
           'any time, with HOTC the responsible agency for them under the Privacy Act.')
pdf.bullet('ASG acts as HOTC\'s agent', 'under section 11 of the Privacy Act 2020: personal '
           "information in the app is used only on HOTC's instructions to deliver the "
           "service, never for ASG's separate commercial purposes. Where ASG must keep its "
           'own records of a response (for example staff health and safety or legal '
           'obligations), ASG holds those as its own responsibility under the Act, and the '
           'written agreement below records exactly where that line sits.')
pdf.bullet('Information sources plug in.', 'Council, AT, Police and event feeds connect '
           'through documented interfaces, and new sources can be added over time without '
           'rework. The live response behind use case 1 is different in kind: a report lands '
           "inside the Safety Team's dispatch operation, is actioned by officers already on "
           'the street, and the outcome flows back to the reporter. That loop is an '
           'operating service, not a data feed.')
pdf.bullet('The recommended structure:', 'the app runs on an underlying city-safety platform '
           'that ASG develops, maintains and continuously improves, licensed to HOTC. That '
           'is what keeps the build fast, the cost sensible and the product alive, rather '
           'than a one-off bespoke build that starts ageing the day it ships. HOTC is '
           'protected either way: full data portability, documented interfaces and agreed '
           'continuity protections, so HOTC is never locked in. The final ownership and '
           'licensing structure is a decision for the written agreement below, with '
           "HOTC's requirements stated up front.")
pdf.bullet('The data is structured once, correctly.', 'Incidents, locations, categories and '
           'outcomes are recorded against a consistent city centre data model from day one, '
           'so every report is comparable month on month and year on year, and HOTC\'s '
           'reporting, funding cases and future integrations never require rebuilding the data.')
pdf.bullet('Insight by design.', 'Alongside individual reports, the platform maintains '
           'anonymised, aggregated safety insights: trends, hotspots and response patterns '
           'that can never identify a person or a business. These power HOTC\'s reporting '
           'and funding cases, and continuously improve how the platform triages, targets '
           'and routes, so the service gets smarter the more the city uses it. The privacy '
           'purposes in section 5 are written into the collection statement from day one, so '
           'none of this ever needs retrofitting.')
pdf.bullet('Governance from day one.', 'HOTC holds the publish authority for the channel. A '
           'pre-agreed alert protocol delegates narrow, defined safety alerts out of hours, '
           'using approved templates with immediate HOTC notification, and a joint review '
           "cadence keeps the protocol honest. Nothing goes out under HOTC's brand without "
           "HOTC's standing approval behind it.")
pdf.bullet('A short written agreement', 'records the IP, data, hosting and portability '
           'positions before build starts, so neither party is relying on defaults.')

pdf.section('9', 'Testing the concept, and next steps')
pdf.body('The next step the brainstorm asked for: put this concept in front of the people it '
         'is for, before anything is built.')
pdf.bullet('Who:', '12 to 15 frontline workers across member and non-member businesses, '
           'sectors, shifts and levels of prior contact with the Safety Team, no more than a '
           'third of whom have called the team before. HOTC leads recruitment through the '
           'member network; interviews are run by HOTC, with ASG observing.')
pdf.bullet('How:', "20-minute structured conversations, in their workplace, using this pack's "
           'use cases as stimulus. Name and brand reactions captured informally along the way.')
pdf.bullet('The seven questions:', 'Would you download this, and what would make you? Which '
           'of the five use cases would you actually use? What information would you want '
           'that is missing? What would make you delete it? Who else in your business should '
           'have it? What would make you tell a workmate to get it? What would you want from '
           'HOTC in here each week?')
pdf.bullet('Output:', 'a short findings note and a ranked, evidence-based use-case list, '
           'treated as qualitative direction for design rather than market validation.')
pdf.ln(1)
pdf.kicker('Steps:')
for s in ['1.  HOTC and ASG review this pack and agree the concept frame (November).',
          '2.  Run the concept test above (November).',
          '3.  Findings and a one-day design sprint: first screens, name and brand '
          '(HOTC-owned), alert taxonomy, access model (early December).',
          '4.  The written agreement per section 8, alongside a privacy review covering '
          'collection notices, third-party information and alert content (December).',
          '5.  MVP build decision: scope, pilot plan and the investment model, including '
          "ASG's contribution to the platform build, so HOTC's investment goes into HOTC's "
          'app and pilot rather than the underlying engine (December into the new year).']:
    pdf.body(s, size=9.8, after=0.8)

pdf.ln(4)
pdf.set_font('Helvetica', '', 8.5)
pdf.set_text_color(*GRAY)
pdf.multi_cell(0, 4.4, 'Heart of the City (Edward Caughey, edward.caughey@hotcity.co.nz) with '
                       'ASG Security (Ahmad Duais, ahmad@absolutesecuritygroup.co.nz)  |  '
                       'October 2026', new_x='LMARGIN', new_y='NEXT')

OUT.parent.mkdir(parents=True, exist_ok=True)
pdf.output(str(OUT))
print(f'Saved: {OUT}')
