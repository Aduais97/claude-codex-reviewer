I've completed the review. One scope call to state up front: the "Deloitte M&A acquisition analysis" framing in the tasking prompt cannot be executed — the corpus contains no financials, org chart, IM, or valuation documents. It contains exactly two documents: **REPORT.md** (the LCF Pilot Accountability & Value Report) and **internal_sensitivity_brief.txt**. The operative, corpus-specific instruction is the ANALYSIS REQUIREMENTS block — a client-readiness review producing a findings list only — and that is what follows. I performed my own independent line-by-line sweep of all 13 sections against every named incident in the sensitivity brief; the result confirms the seven findings already saved in `_findings_client_readiness.md` (a prior run's output), with nothing additional at BLOCKER or RECOMMENDED level. No verified figure is altered by any replacement below.

---

# Client-Readiness Review — REPORT.md (LCF Pilot Accountability & Value Report)

**TLDR: One BLOCKER (§13 over-discloses internal reporting mechanics), three RECOMMENDED edits (§7 Viaduct framing, §4+§7 Auror-meeting phrasing, §8 survey reframe), three OPTIONAL polish items. All known internal incidents from the sensitivity brief — the 18 July no-show, 6 June gear delay, 7 June absence, 19/20 June late arrivals, and 19/26 June and 3 July early endings — are fully absent from the report. Apply F1 and the report is safe to send; apply F2–F4 as well and it is polished for the HOTC/Council audience.**

## Findings (most severe first)

### F1 — BLOCKER — §13 Data Sources: provenance statement airs internal reporting failures

The brief (category 3) requires §13 to keep an honest compilation-method statement phrased neutrally, and explicitly says missing team logs must not be framed as a failure. Three phrases go further than needed: **"carried-over entries"** signals stale copy-pasted log content; **"was not returned"** frames the missing logs as a staff submission failure; **"concentrated in the first three pilot weeks"** is internal detail that invites a Council reader to ask what was going wrong in weeks 1–3.

**Current:**
> Figures are compiled from every daily patrol log for 1 June – 18 July 2026 (48 days), reviewed line by line, with duplicate and carried-over entries removed and cross-team double-counts consolidated; where a team's written log was not returned for a shift that operated (nine of the 48 days, concentrated in the first three pilot weeks), its activity is included at the verified average level for equivalent fully-logged two-team days, rounded to whole events — the effect on headline totals is under one per cent.

**Replacement:**
> Figures are compiled from the daily patrol logs for 1 June – 18 July 2026 (48 days), reviewed line by line, with duplicate entries removed and incidents attended by both teams counted once. Where an individual team log is not available for a shift that operated (nine of the 48 days), that team's activity is included at the verified average level for equivalent fully-logged two-team days, rounded to whole events; the effect on headline totals is under one per cent.

This keeps every honest element — line-by-line review, deduplication, the estimation method, its scale (nine of 48 days) and materiality (under 1%) — and leaves the following "Totals reconcile exactly with the HOTC Weekly Data Reports" sentence untouched. Only the framing changes: "not available" is neutral and archival where "not returned" implies someone failed to hand it in.

### F2 — RECOMMENDED — §7: Viaduct reference exceeds coordination context

The brief (category 5) allows Viaduct static-guard references only as coordination context, not as ASG servicing another client. "Holding the Viaduct overnight" reads as the LCF-funded team providing sustained cover of another operator's site — inviting the funder question "whose hours paid for that night?" — and "a static guard" leaves whose guard it was ambiguous. §9 already uses the right model ("venue static guard"); §7 should match it.

**Current:** "��including holding the Viaduct overnight after an assault on a static guard (14 July)."
**Replacement:** "…including supporting venue security at the Viaduct after an assault on a venue guard (14 July)."

### F3 — RECOMMENDED — §4 and §7: Auror-meeting phrasing ties funded patrol hours to an ASG commercial meeting

The Auror partnership is a legitimate positive and belongs in §7. But §4 makes the funded team's involvement in ASG's own meeting explicit, and §7's tail clause is defensive — it answers "did you pull guards off the street?" before anyone asked, thereby planting the question. This is exactly the kind of question ASG would rather field in person.

**§4 current:** "the team splitting to hold live response cover during the Auror meeting (17 July)"
**§4 replacement:** "the team splitting to hold live response cover during partner engagements (17 July)"

**§7 current:** "ASG met with Auror's global headquarters on 17 July to deepen the integration, while keeping live response cover on the street."
**§7 replacement:** "ASG met with Auror on 17 July to deepen the integration."

The §7 edit also fixes the awkward "met with Auror's global headquarters" — one meets people, not a building.

### F4 — RECOMMENDED — §8: survey gap framed as a lapse rather than a design choice

"No survey wave has yet been completed" is a bald admission inviting "why not during the pilot?" The honest facts support a better ordering: lead with the methodological rationale the text already contains and let the absence of results follow from it. The replacement still states plainly that no results are included.

**Current:**
> The programme's perceptions survey instrument (business, landlord and public-intercept forms) was prepared at pilot commencement. No survey wave has yet been completed, so no survey results are reported here. ASG recommends running the survey immediately post-pilot so that measured perceptions are referenced to the deployment period.

**Replacement:**
> The programme's perceptions survey instrument (business, landlord and public-intercept forms) was prepared at pilot commencement. ASG recommends running the first survey wave immediately post-pilot, so that measured perceptions are referenced to the full deployment period; survey results are therefore not included in this report.

### F5 — OPTIONAL — §6: "passive victims" mildly disparages precinct businesses

No store is named, so this passes the brief's letter; it is tone only — but it labels the very businesses the report celebrates.

**Current:** "…walked staff through contacting HOTC immediately, converting passive victims into active reporters."
**Replacement:** "…walked staff through contacting HOTC immediately, so more incidents are reported and actioned."

### F6 — OPTIONAL — §4: polish on the first approved capacity instance (not removal)

All three CEO-approved instances stay, and their framing is verified capacity-focused. Two polish points on the 1 June entry: naming Coffee Club associates one specific business with the queued call (the 6 June entry is already generic — "one cafe call"), and "standing up" is ops jargon for a funder audience.

**Current:** "1 June — a Coffee Club caller was queued behind another incident on the morning the uplift was still standing up."
**Replacement:** "1 June — a café caller was queued behind another incident on the morning the uplift was still mobilising."

### F7 — OPTIONAL — §4 table: internal log vocabulary surfacing

"Team busy" is internal log shorthand appearing verbatim, in quotes, in a funder document. Same figure, plain wording.

**Current:** "51 'team busy' instances; 20 simultaneous-incident clashes"
**Replacement:** "51 instances with the team already committed to another call; 20 simultaneous-incident clashes"

---

## Category sweep — explicit clearance per sensitivity-brief category

1. **Staffing failures — CLEAN.** Each known incident individually checked and absent: the 18 July second-guard no-show/solo SOP-restricted morning (no trace; §4's "none in the two-team daytime window after the first week" is scoped to the Sun–Thu two-team window and 18 July was a Saturday, so the claim does not expose it); the 6 June ~45-minute gear-locked delay (the report's only 6 June entry is the approved altercation instance); the 7 June B-team absence; the 19/20 June night-guard late arrivals; the 19/26 June and 3 July early shift endings (the report's 3 July content is night-time welfare work only). Nothing reads as an ASG-caused delay or absence.
2. **Equipment/admin failures — CLEAN.** No body-camera chargers, keys, phone or radio battery, standby periods, or WhatsApp artifacts anywhere.
3. **Internal reporting-quality mechanics — ONE LEAK: §13 (F1).** Otherwise clean; the §3 footnote explaining the 2025 five-metric format is a neutral, necessary explanation of the n/a cells and should stay.
4. **Internal management matters — CLEAN.** No manager names, standby orders, HR or rostering language; "flexed" reads as service design, not internal rostering.
5. **Third-party exposure — ONE FLAG: §7 Viaduct (F2).** No ASG staff named anywhere (all references are "guards", "the team", "a guard"); no other ASG client or site identifiable.
6. **Blame/embarrassment of precinct businesses, Police, or Council — CLEAN** (bar the optional F5 tone item). All store namings are victim/beneficiary framed; Police are framed favourably ("orderly handover, not emergency callout", falling escalation share); Council appears only in positive joint-working contexts; the FENZ bin-fire line is neutral.
7. **§4 approved capacity instances — PRESENT AND CORRECTLY FRAMED.** All three (1 Jun queued caller, 6 Jun cafe call during the altercation, 2 Jul night concurrent calls) are framed as capacity findings, not staff failures, and the section correctly channels the residual gap toward the night-cover business case. Only optional polish flagged (F6, F7).

## Section-by-section professional read

**§1 Executive Summary, §2 Delivery, §5 Capacity Use, §9 Harm Reduction, §10 Stories, §11 CPTED, §12 Beyond the Pilot — clean and strong** for a funder audience. Specifically: §2's invoicing and reconciliation sentences are the right accountability posture; §1's police-escalation bullet leads with the favourable year-on-year figure, which is defensible because §3's table shows both comparators and the share-of-attended-demand analysis (9.6% vs 10.8% baseline vs 14.1% last year) falls against both; §9's disclosure of the two third-party-caused injuries is honest and correctly scoped ("neither involving force used by the Safety Team"); §12's extension recommendation is evidence-grounded without overreaching. §3 is clean — its interpretive paragraph on rising attended-call counts is necessary pre-emption, not defensiveness; without it, "+92% aggressive behaviour" invites a worse reading. The flagged sections are §4 (F3, F6, F7), §6 (F5), §7 (F2, F3), §8 (F4), and §13 (F1).

**Bottom line:** with F1 applied the report is safe to send to Heart of the City and onward to Auckland Council; with F2–F4 also applied it is polished for that audience. All replacements preserve every verified figure exactly. The full findings are on disk at `_findings_client_readiness.md`, which this independent pass re-verified line by line — no corrections to it were needed, and no additional leaks were found.
