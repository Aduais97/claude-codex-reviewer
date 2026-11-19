#!/usr/bin/env python3
"""Project Beacon: internal platform strategy + external development brief (two PDFs).
Built 28 Oct 2026 via ETR workflow: 3 research agents (gap/competitors, market sizing,
build economics) -> draft -> Codex gpt-5.6-terra + 3 lenses (CTO/dev-partner, strategy
skeptic, external-safety/anti-slop), ~90 findings applied. Key engineering: document FORKED
(internal strategy never leaves ASG; external RFP carries no pricing bands, market map,
funding dollars or strategy); pull-through split retention-vs-acquisition-hypothesis;
payback base case added; pilot gate restated on provable metrics; s21(3) position corrected
(commissioner owns by default); scope cuts (per-message ACLs, geo-targeting, AI triage out);
audit taxonomy + WORM; residency stated honestly (ping-then-fetch); "many multiples" and
pilot-approvals confidentiality leaks removed. No em-dashes. No client names.
Outputs: ~/Desktop/ASG/Beacon Platform/Beacon_Platform_Strategy_INTERNAL.pdf
         ~/Desktop/ASG/Beacon Platform/Beacon_Development_Brief_RFP.pdf
"""
from pathlib import Path
from fpdf import FPDF

NAVY = (16, 34, 62)
GOLD = (176, 141, 60)
INK = (40, 45, 55)
GRAY = (110, 118, 130)
RED = (176, 30, 30)

OUTDIR = Path.home() / 'Desktop/ASG/Beacon Platform'


class Doc(FPDF):
    def __init__(self, header_line):
        super().__init__(format='A4')
        self.header_line = header_line
        self.set_auto_page_break(auto=True, margin=16)
        self.set_margins(17, 15, 17)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('Helvetica', '', 7.8)
        self.set_text_color(*GRAY)
        self.cell(0, 5, self.header_line, new_x='LMARGIN', new_y='NEXT')
        self.ln(2)

    def footer(self):
        self.set_y(-12)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(*GRAY)
        self.cell(0, 5, f'{self.page_no()}', align='C')

    def h1(self, num, title):
        if self.get_y() > 240:
            self.add_page()
        self.ln(3.5)
        self.set_font('Helvetica', 'B', 13.5)
        self.set_text_color(*GOLD)
        self.cell(9, 7, num)
        self.set_text_color(*NAVY)
        self.cell(0, 7, title, new_x='LMARGIN', new_y='NEXT')
        self.set_draw_color(*GOLD)
        self.set_line_width(0.4)
        self.line(self.l_margin, self.get_y() + 0.5, self.l_margin + 50, self.get_y() + 0.5)
        self.ln(2.8)

    def h2(self, title):
        self.ln(1)
        self.set_font('Helvetica', 'B', 10.5)
        self.set_text_color(*NAVY)
        self.multi_cell(0, 5, title, new_x='LMARGIN', new_y='NEXT')
        self.ln(0.6)

    def p(self, text, size=9.4, after=2.2):
        self.set_font('Helvetica', '', size)
        self.set_text_color(*INK)
        self.multi_cell(0, 4.6, text, new_x='LMARGIN', new_y='NEXT')
        self.ln(after)

    def b(self, lead, text, size=9.2):
        self.set_font('Helvetica', 'B', size)
        self.set_text_color(*NAVY)
        self.cell(4, 4.5, '-')
        if lead:
            self.cell(self.get_string_width(lead + ' ') + 1, 4.5, lead)
        self.set_font('Helvetica', '', size)
        self.set_text_color(*INK)
        self.multi_cell(0, 4.5, text, new_x='LMARGIN', new_y='NEXT')
        self.ln(1)

    def table(self, headers, rows, widths, size=8.4):
        self.set_font('Helvetica', 'B', size)
        self.set_fill_color(*NAVY)
        self.set_text_color(255, 255, 255)
        for w, h in zip(widths, headers):
            self.cell(w, 6, h, fill=True, border=1)
        self.ln()
        self.set_text_color(*INK)
        for row in rows:
            self.set_font('Helvetica', '', size)
            x0, y0 = self.get_x(), self.get_y()
            heights = []
            for w, cell in zip(widths, row):
                lines = self.multi_cell(w, 4.1, cell, dry_run=True, output='LINES')
                heights.append(len(lines) * 4.1 + 2)
            rh = max(heights + [8])
            if y0 + rh > 275:
                self.add_page()
                x0, y0 = self.get_x(), self.get_y()
            cx = x0
            for i, (w, cell) in enumerate(zip(widths, row)):
                self.set_font('Helvetica', 'B' if i == 0 else '', size)
                self.set_xy(cx, y0)
                self.multi_cell(w, 4.1, cell)
                self.rect(cx, y0, w, rh)
                cx += w
            self.set_xy(x0, y0 + rh)
        self.ln(2.5)

    def cover(self, title, subtitle, lines, note):
        self.add_page()
        self.ln(26)
        self.set_font('Helvetica', 'B', 27)
        self.set_text_color(*NAVY)
        self.multi_cell(0, 12, title, new_x='LMARGIN', new_y='NEXT')
        self.set_font('Helvetica', '', 14)
        self.set_text_color(*GOLD)
        self.multi_cell(0, 8, subtitle, new_x='LMARGIN', new_y='NEXT')
        self.ln(5)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(*GRAY)
        for ln in lines:
            self.cell(0, 6, ln, new_x='LMARGIN', new_y='NEXT')
        self.ln(8)
        self.p(note, size=10.5)


# ============================================================ INTERNAL STRATEGY
A = Doc('Project Beacon | Platform Strategy | ASG Group INTERNAL')
A.cover('Project Beacon', 'The city safety coordination platform: strategy',
        ['ASG Group | Strictly internal. Not for external distribution in any form.',
         'October 2026 | Working name only; trademark clearance is a Phase 0 task'],
        'This is the internal strategy. The companion Development Brief (separate document) '
        'is the only artefact shown to development partners; it carries the build scope and '
        'terms, and none of the market, pricing or strategy content in this document. '
        'Figures marked (est.) are analyst estimates; assumptions available on request.')
A.set_font('Helvetica', 'B', 9)
A.set_text_color(*RED)
A.multi_cell(0, 4.6, 'Do not send this document outside ASG. The external artefact is '
                     'Beacon_Development_Brief_RFP.pdf only.', new_x='LMARGIN', new_y='NEXT')

A.add_page()
A.h1('1', 'Summary')
A.p('Every city centre is kept safe by organisations that cannot talk to each other. In '
    'September 2026, Auckland Council\'s newest business-safety initiative launched with a '
    'WhatsApp group as its coordination channel. The city centre\'s longest-running '
    'retailer-and-Police network describes its own information sharing as text and email. '
    'The central city\'s safety guidance routes businesses to four separate phone numbers '
    'for four organisations. New Zealand has strong evidence platforms moving footage and '
    'number plates from businesses to Police, and it has phone trees. We have not '
    'identified any NZ product that connects councils, business associations, Police '
    'liaison and private security in one governed operational channel; that assessment is '
    'current as at October 2026 and is tested in Phase 0.')
A.p('Beacon is that channel: a multi-tenant platform where each organisation owns its own '
    'data, reports and alerts flow to the people they affect, and the organisations that '
    'keep a city centre safe coordinate in one governed place. The tenancy model follows '
    'the pattern proven in retail: the operator owns the platform; every client owns its '
    'own data. The governance design is deliberate: every access logged against a lawful '
    'basis, per-tenant data silos, no biometrics. That discipline is what councils and '
    'Police can politically afford to join.')
A.p('The economics are a niche, and the strategy says so plainly: see sections 4 and 5. '
    'The conclusion is a lean, gated build: a roughly $20k Phase 0 demand test before any '
    'build spend, a thin MVP if the test passes, and a documented fallback if it fails.')

A.h1('2', 'The gap, with evidence')
A.p('What exists today is a two-rail system. Evidence rails: Auror moves retail crime '
    'evidence to Police (85,000+ stores on the vendor\'s own published count; reportedly '
    'around 10% of revenue now from NZ) and is entangled in governance controversy: a 2025 '
    'Police review found access controls inadequate, warrantless-use litigation has reached '
    'the appellate courts with a further appeal reported likely, the Privacy Commissioner '
    'has engaged formally, and a UK force has reportedly drawn regulatory action over '
    'ungoverned accounts. SaferCities vGRID moves live camera feeds and plates to Police; '
    'it is a camera pipe, not a coordination tool. Human rails: co-located safety hubs, '
    'monthly meetings, phone trees, text, email and WhatsApp groups. Scale figures below '
    'are the vendors\' own published counts as at October 2026.')
A.table(['Product', 'What it is', 'Why the gap stays open'],
        [['Auror (NZ)', 'Retail evidence and ORC intelligence to Police',
          'Retailer-to-Police only; no council, BID or security tenancy; governance baggage'],
         ['vGRID (NZ)', 'Live camera and plate sharing to Police',
          'One-way pipe; no messaging, tasking or coordination'],
         ['DISC (UK)', 'BID crime reporting and alerts; 100+ BIDs, 550+ schemes',
          'Intelligence sharing, not live coordination; no NZ presence today'],
         ['Safer Places (AU)', 'Camera registry and incident reports, ~A$10/business/month',
          'Business and Police only; no multi-agency operations; minimal NZ traction'],
         ['Snap Send Solve, Antenno (NZ)', 'Public-to-council fault reporting; 50+ councils',
          'One-way civic reporting; proves councils buy this category as SaaS']],
        [34, 68, 74])
A.p('The gap is durable for us specifically: platform vendors do not run street operations, '
    'security firms do not build platforms, councils do not productise. ASG does all three '
    'jobs today in the same city centre. And coordination networks compound: each '
    'organisation that joins makes the channel more valuable to the rest, subject to the '
    'tenancy policy tension addressed in section 6.')

A.h1('3', 'The product')
A.b('Report and respond.', 'A frontline worker reports an incident in under 30 seconds. It '
    'reaches the right responder with a structured, human-reviewed handoff toward Police '
    'where needed, and the reporter sees it was received and what happened.')
A.b('Alert and coordinate.', 'Verified, targeted alerts: incident advisories, planned event '
    'and disruption notices drawn from public feeds. Shared incident channels let a council '
    'warden, a BID safety team and a security firm work one incident in one thread.')
A.b('Insight.', 'Per-tenant analytics: incidents, hotspots, response performance, the '
    'evidence base for levy and funding cases. Across tenants, only anonymised aggregates.')
A.p('What it is not: not a camera platform, not facial recognition, not number plate '
    'recognition, not an offender database, not a replacement for 111, and no monitoring '
    'or reporting of lawful assembly. These boundaries are deliberate product decisions; '
    'they are what make the platform joinable by councils and Police.')

A.h1('4', 'Model and market (est.)')
A.p('Tenancy: the platform entity owns the platform; every tenant owns its own data: '
    'branded workspace (logo and name at MVP), its own users, its own data partition, full '
    'export rights, the right to leave. Cross-tenant sharing only in channels both sides '
    'opt into, every access logged against a recorded lawful basis, a per-tenant '
    'disclosure register generated from the audit log itself.')
A.p('Pricing bands (est., from comparables: DISC schemes at low thousands of pounds plus '
    'about 100 to 150 pounds per member business; Safer Places about A$10 per business per '
    'month; Snap Send Solve council deals around NZ$8k to $15k): small BIDs $1k to $3k, '
    'mid $3k to $8k, large associations $8k to $25k, councils $20k to $60k. The council '
    'premium over the Snap Send Solve comparable is the argument we must win: multi-agency '
    'coordination and auditable governance versus one-way fault reporting. If councils '
    'only pay fault-reporting money, the capture range below drops materially; roughly '
    'half the upside case is council-dependent.')
A.p('Market (est.): 51 Auckland BIDs (Auckland Council BID Policy requires $120k minimum '
    'income by 2028, so the small tier is consolidating), roughly 15 to 25 more formal '
    'BIDs and mainstreet organisations nationally, and a provincial tail: 70 to 90 '
    'plausible tenant organisations plus 10 to 20 realistic council buyers. NZ potential '
    'roughly $0.4m to $1.4m a year; credible capture $300k to $700k at maturity. '
    'Australia roughly triples the tenant universe (Victorian special-rate schemes, '
    'Brisbane mall levies, the NSW CID pilot creating new BIDs now). Funding tailwind: '
    'publicly announced Proceeds of Crime allocations already flow through Auckland BIDs '
    'for safety work with reporting obligations attached; Beacon positions as the '
    'accountability layer that money demands.')
A.p('The value stack, argued honestly in three parts: (1) subscription revenue, a solid '
    'niche; (2) services retention: the platform makes our precinct contracts stickier and '
    'harder to displace, which is defensible today, while winning NEW precinct work '
    'through the platform is a hypothesis until a tender names it as a factor or a '
    'non-ASG-guarded organisation signs as a paying tenant; (3) the Australian option. '
    'Tenant analytics and funding-case packs are retention features inside (2), not a '
    'separate asset line. This stack justifies a lean, gated build inside the group. It '
    'does not justify a venture-scale raise, and nothing in this plan depends on one.')

A.h1('5', 'Base case and payback (est.)')
A.table(['Year', 'Tenants (end)', 'ARR', 'Cash out (build, run, sell)', 'Cumulative net'],
        [['1', '1 to 2', '$10k to $30k', '$220k to $320k', 'negative $200k to $300k'],
         ['2', '4 to 8', '$40k to $110k', '$90k to $140k', 'negative $250k to $360k'],
         ['3', '8 to 15', '$90k to $220k', '$100k to $160k', 'negative $200k to $340k'],
         ['4', '12 to 25', '$150k to $350k', '$110k to $180k', 'approaching breakeven high case']],
        [16, 28, 32, 52, 48])
A.p('Read plainly: subscriptions alone pay back in year 4 at the earliest, later with '
    'churn, and BIDs are manager-dependent organisations where churn is real. What makes '
    'the investment rational on a shorter horizon is the retention value on precinct '
    'services work plus the option value. If that sentence stops being believed, stop at '
    'the fallback: a $60k to $100k internal operations and client-retention tool for our '
    'own contracts, which is a perfectly good outcome at a third of the spend.')

A.h1('6', 'Risks, honestly ranked')
A.b('Willingness to pay is undemonstrated (the biggest risk).', 'Every piece of our gap '
    'evidence also shows this market currently pays zero for coordination. The Phase 0 '
    'test in section 7 exists to answer this for about $20k before any build dollar.')
A.b('Closed tenancy versus network effect.', 'Phases 1 and 2 are ASG-plus-clients, so the '
    'phase 1 to 2 addressable market is our footprint plus councils, not 70 to 90 '
    'organisations. The openness decision is scheduled, not vague: reviewed at Phase 4 or '
    'when two non-client organisations ask to join, whichever is first; the end state '
    'likely requires independent governance over the aggregate layer for competitor '
    'tenants to trust it.')
A.b('Nearer competitors than Auror.', 'vGRID adding comms is the most dangerous sideways '
    'move (it owns council and Police relationships); DISC entering NZ arrives with ten '
    'years of product; a council could tender its own; and the real incumbent in every '
    'sales meeting is free: the WhatsApp group. Mitigation for all four: speed to a '
    'signed second tenant, and a product whose responder loop WhatsApp cannot copy.')
A.b('Pilot evidence is pre-commercial.', 'Concept use cases and success measures are '
    'agreed and the frontline concept test is designed, not yet run; there is no signed '
    'commercial commitment. Gate: a signed paid pilot agreement, even $5k to $10k '
    'conditional, before Phase 1 spend.')
A.b('Operational accountability.', 'A reporting app creates response expectations. '
    'Pilot-launch gate: per-tenant acknowledgement SLA, auto-escalation on timeout, and '
    'in-app wording that is explicit about what the platform does and does not promise, '
    'with 111 first for anything happening now.')
A.b('Privacy execution.', 'Incident reports contain third-party personal information and '
    'the audit log is itself a personal-information system (append-only, retention '
    'defined, discoverable). PIA commissioned separately from the build; penetration test '
    'with cross-tenant leakage as an explicit objective before pilot launch.')

A.h1('7', 'Phase 0: the $20k de-risk plan (before any build spend)')
A.b('1.', 'Convert the pilot relationship into a signed, conditional paid pilot (any real '
    'dollars).')
A.b('2.', 'Clickable prototype (design-tool grade, $5k to $15k, no code) plus a one-page '
    'price card at the section 4 bands.')
A.b('3.', 'Take it cold to 8 to 10 non-pilot BIDs, including publicly safety-funded ones, '
    'asking for signed non-binding letters of intent at stated prices.')
A.b('Pass gate:', '3 or more LOIs, at least one from an organisation whose security '
    'provider is not ASG. That single criterion tests demand, the open-network question '
    'and the pull-through direction at once. Zero non-ASG interest means build the '
    'fallback tool instead.')
A.b('In parallel:', 'form the platform entity and start app-store organisation '
    'registration (weeks of lead time); IPONZ and AU trademark search on the working name '
    '(expect to rename); commission the PIA scoping; design the incident data model and '
    'alert taxonomy as our deliverable to any builder.')

A.h1('8', 'Build path')
A.p('Internal team and agency cost roughly the same for the MVP (approximately $200k to '
    '$350k first year all-in; expect good agencies to argue the build alone toward $260k '
    'to $320k unless the scope cuts hold: per-message channel ACLs, street-level alert '
    'targeting and any AI features are out of MVP). The difference is what you hold '
    'afterwards: internal keeps the team and knowledge; an agency compresses time and '
    'transfers delivery risk.')
A.p('Recommendation: build-operate-transfer with a continuity vessel. A partner builds '
    'Phase 1 against the external brief\'s terms (IP assigned on payment, code in our '
    'repositories and cloud accounts from day one, architecture records and runbooks as '
    'acceptance-gated deliverables, defined transition-out package instead of a priced '
    'exit option), and one ASG-side technical owner is embedded in the partner\'s team '
    'from day one: design reviews, standups, the lot. That person is the Phase 2 '
    'internalisation seed and the named product owner the build needs. ASG Group '
    'guarantees the platform entity\'s contract obligations until the entity stands '
    'alone. Decision point to internalise: Phase 2, with pilot evidence in hand.')
A.p('Gate restated on what the pilot can prove: weekly active reporters per member '
    'business, reporter return rate, time to acknowledge, and share of reports closed '
    'with an outcome, instrumented in the MVP itself. The independent inter-organisation '
    'channel becomes the Phase 2 to 3 gate, when a counterparty that is not us exists.')
A.p('Next steps: run Phase 0 now; shortlist three development partners against the '
    'external brief in parallel; decision meeting when the LOI results and the bids are '
    'both on the table.')
A.ln(2)
A.set_font('Helvetica', '', 8.5)
A.set_text_color(*GRAY)
A.multi_cell(0, 4.4, 'ASG Group | Ahmad Duais | ahmad@absolutesecuritygroup.co.nz | '
                     'Strictly internal', new_x='LMARGIN', new_y='NEXT')

# ============================================================ EXTERNAL RFP
B = Doc('Beacon | Development Brief | Commercial in confidence')
B.cover('Beacon', 'Development brief: multi-tenant incident coordination platform',
        ['ASG Group | Commercial in confidence | Shared under NDA',
         'October 2026 | Beacon is a working name, pre-clearance'],
        'ASG Group is commissioning the MVP of a multi-tenant incident reporting and '
        'coordination SaaS for precinct safety organisations: business associations, '
        'councils and security operators. A pilot business association partner has '
        'participated in early discovery, subject to its own approvals. This brief asks '
        'development partners to propose an approach, team and price for Phase 1, or to '
        'help us compare that against an internal build. Commercial strategy, market '
        'detail and budgets are retained internally.')

B.add_page()
B.h1('1', 'What the MVP is')
B.p('Two tenants at launch (a business association and a security operator), one reporting '
    'loop, one alert loop, one shared incident channel. Deliberately thin.')
B.h2('Mobile app (iOS and Android, one codebase)')
B.b('', 'Register and join a tenant: name, employer, role, work contact; admin approval '
    'queue. Tenant provisioning is manual, by us.')
B.b('', 'Report an incident: category, location (auto plus adjust), description, up to 3 '
    'photos; under 30 seconds end to end. The reporting screen leads with: emergency '
    'happening now, call 111.')
B.b('', 'Receive push alerts, tenant-wide with a category filter; acknowledge. No '
    'street-level geo-targeting at MVP.')
B.b('', 'See my reports and their status: received, responded, outcome summary (status '
    'only, no personal details of third parties).')
B.h2('Responder and dispatch console (web)')
B.b('', 'Live incident queue per tenant; assign, update status, close with outcome '
    'category.')
B.b('', 'Compose and send alerts: tenant audience and category targeting, per-tenant '
    'approval step, templates.')
B.b('', 'Shared incident channel: a timeline two tenants both opted into, where every '
    'participant sees everything in that channel, with tasking. No per-message visibility '
    'rules at MVP.')
B.b('', 'Minimal metrics view: weekly active reporters, reports per week, time to '
    'acknowledge, closure rate.')
B.h2('Admin and governance (web)')
B.b('', 'Tenant admin: user approval, roles, templates, alert approval policy, content '
    'flag-and-remove.')
B.b('', 'Audit and export: auditable events logged (see NFR 2), per-tenant disclosure '
    'register generated from the audit log, full tenant data export.')
B.h2('Explicitly out of MVP scope')
B.p('Cameras or video ingestion, facial recognition, number plate recognition, offender '
    'databases or watchlists, cross-tenant identity sharing, public (unapproved) users, '
    'AI features of any kind, per-message visibility rules, street-level alert targeting, '
    'per-tenant theming beyond logo and name, third-party system integrations. Police '
    'handoff at MVP means a tenant-authorised, human-reviewed export in a documented '
    'format (budget as a templated PDF and email export; format confirmed with us during '
    'design). It is not a Police integration and implies no Police endorsement.')

B.h1('2', 'Planning assumptions (price against these)')
B.table(['Assumption', 'Value'],
        [['Users per tenant at pilot', '30 to 60; design headroom to 500'],
         ['Reports', 'Up to 40 per day across the network at pilot'],
         ['Alerts', 'Up to 20 per week per tenant'],
         ['Photos', 'Up to 3 per report, 10 MB each; EXIF and GPS stripped on upload; '
          'malware scanned'],
         ['Environments', 'Dev, staging, production; infrastructure in our cloud accounts, '
          'run cost ours'],
         ['Design', 'Partner provides product design within our brand guide; we approve'],
         ['Support', 'Business hours, with a severity-1 response path, hours stated in '
          'your proposal'],
         ['App stores', 'Accounts owned by us (entity registration underway); evaluate '
          'closed-membership distribution options with us'],
         ['Moderation', 'Tenant-admin flag and remove, plus a published contact, per '
          'store policies for user-generated content'],
         ['Privacy assessment', 'PIA commissioned separately by us; your obligation is to '
          'implement its findings']],
        [52, 124])

B.h1('3', 'Non-functional requirements')
B.b('1. Tenant isolation, stated as outcomes:', 'tenant-scoped access enforced at the '
    'data layer and provable in audit; zero cross-tenant leakage is an explicit '
    'penetration-test objective; per-tenant export and deletion; data for opted-in shared '
    'channels held as a named, separately governed exception. Propose your mechanism '
    '(row-level security, schema, or hybrid) and defend it.')
B.b('2. Audit:', 'defined event taxonomy: viewing a record in detail, exporting, and any '
    'cross-tenant disclosure are logged with actor, time and a recorded basis; list '
    'renders are logged without a basis prompt. The log is append-only (object-lock or '
    'equivalent), has a stated retention period, and the disclosure register is generated '
    'from it.')
B.b('3. Security:', 'encryption in transit and at rest; role-based least privilege; MFA '
    'for console users; OIDC-based auth from day one (enterprise IdP federation later); '
    'upload malware scanning; vulnerability remediation and incident-response procedures; '
    'independent penetration test before pilot launch with criticals and highs remediated '
    'or formally risk-accepted.')
B.b('4. Data residency:', 'personal information, backups and logs at rest in New Zealand '
    '(AWS Auckland region or Azure NZ North); transient notification triggers are data '
    'minimised through platform push services (ping then fetch; no personal information '
    'in push payloads). Provide a subprocessor and data-flow register before build: every '
    'external service, location, fields, purpose, retention.')
B.b('5. Alerts and offline:', 'target 95% of alerts delivered to online devices within 60 '
    'seconds, with delivery and acknowledgement tracked; email or SMS mirror for '
    'high-severity alerts; offline reporting is store-and-forward (queued locally with '
    'photos, idempotent submit on reconnect, location and time captured at creation). No '
    'offline-first sync.')
B.b('6. Quality:', 'WCAG AA across both surfaces; the incident data model (categories, '
    'locations, outcomes, severity) is supplied by us as a design input and is a '
    'deliverable of design.')

B.h1('4', 'Phases')
B.b('Phase 0 (ours, underway):', 'frontline concept test; data model and alert taxonomy; '
    'PIA scoping; entity and app-store registration; this procurement.')
B.b('Phase 1 (the engagement, 4 to 6 months):', 'the MVP above, to pilot launch with two '
    'tenants, including the pre-launch penetration test and remediation.')
B.b('Phase 2 (optional extension):', 'additional tenants, a council channel, public '
    'disruption-notice feeds, per-message channel controls, reporting packs. Scoped and '
    'priced separately after pilot evidence.')

B.h1('5', 'What to propose')
B.b('1.', 'Approach and architecture for the Section 1 to 3 scope, including your '
    'multi-tenancy and audit design.')
B.b('2.', 'A fixed-price discovery phase as the first deliverable, then build as fixed '
    'scope or capped time-and-materials, plus a monthly run and support price. For '
    'calibration, we assess the build at roughly 1,200 to 1,700 hours; if your view '
    'differs materially, show your breakdown.')
B.b('3.', 'Team: named technical lead and key people, with substitution consent not to '
    'be unreasonably withheld, equivalent-seniority replacement and no-charge overlap '
    'handover.')
B.b('4.', 'Evidence: two comparable builds we can reference, at least one multi-tenant.')
B.b('5.', 'Privacy and security: how you build to Privacy Act 2020 requirements, your '
    'penetration test regime, and your residency approach per NFR 4.')

B.h1('6', 'Terms we weight heavily')
B.b('', 'Express present assignment of all new IP in the deliverables to our nominated '
    'platform entity on payment, with a narrow, listed carve-out licence for your '
    'pre-existing tools. We will not rely on statutory defaults in either direction, and '
    'ASG Group guarantees the platform entity\'s obligations under the contract.')
B.b('', 'Code in our repositories and our cloud accounts from day one.')
B.b('', 'Architecture decision records, runbooks and deployment documentation as '
    'acceptance-gated Phase 1 deliverables; on any transition, a defined handover package '
    'with named-lead support at stated day rates and no exit fee.')
B.b('', '60 to 90 day defect warranty after acceptance; severity-tiered support SLA; '
    'changes capped at 10% of build price without a re-baselined agreement; written '
    'residency and audit-log-retention commitments per NFR 2 and 4.')

B.h1('7', 'Process')
B.p('Questions by [date]. Proposals by [date, two weeks later]. Shortlist interviews the '
    'following week; decision within one month of proposals. Evaluation weighting: team '
    '30, approach 30, price 25, references 15. Contact: Ahmad Duais, '
    'ahmad@absolutesecuritygroup.co.nz.')
B.ln(2)
B.set_font('Helvetica', '', 8.5)
B.set_text_color(*GRAY)
B.multi_cell(0, 4.4, 'ASG Group | Commercial in confidence | Shared under NDA | October '
                     '2026', new_x='LMARGIN', new_y='NEXT')

OUTDIR.mkdir(parents=True, exist_ok=True)
A.output(str(OUTDIR / 'Beacon_Platform_Strategy_INTERNAL.pdf'))
B.output(str(OUTDIR / 'Beacon_Development_Brief_RFP.pdf'))
print('Saved both PDFs to', OUTDIR)
