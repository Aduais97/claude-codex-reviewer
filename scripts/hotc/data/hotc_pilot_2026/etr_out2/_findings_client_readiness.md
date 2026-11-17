# Client-Readiness Review — REPORT.md (LCF Pilot Accountability & Value Report)

Reviewed line by line against `internal_sensitivity_brief.txt`. Verified figures untouched — every
replacement below preserves all numbers exactly. Findings are ordered most severe first.
Scope note: the review corpus contains only REPORT.md and the sensitivity brief; the acquisition-framework
boilerplate in the tasking prompt does not match this corpus and was set aside.

---

## FINDINGS

### F1 — BLOCKER — §13 Data Sources: provenance statement over-discloses internal reporting mechanics

The brief (category 3) requires §13 to keep an honest compilation-method statement but phrased neutrally —
explicitly: missing team logs must not be framed as a failure. The current paragraph does three things it
doesn't need to: "carried-over entries" signals stale copy-pasted log content; "was not returned" frames
the missing logs as a submission failure by staff; and "concentrated in the first three pilot weeks" is an
internal detail that invites the question "what was going wrong in weeks 1–3?" from a Council reader.

**Current text (§13):**
> Figures are compiled from every daily patrol log for 1 June – 18 July 2026 (48 days), reviewed line by
> line, with duplicate and carried-over entries removed and cross-team double-counts consolidated; where a
> team's written log was not returned for a shift that operated (nine of the 48 days, concentrated in the
> first three pilot weeks), its activity is included at the verified average level for equivalent
> fully-logged two-team days, rounded to whole events — the effect on headline totals is under one per cent.

**Replacement:**
> Figures are compiled from the daily patrol logs for 1 June – 18 July 2026 (48 days), reviewed line by
> line, with duplicate entries removed and incidents attended by both teams counted once. Where an
> individual team log is not available for a shift that operated (nine of the 48 days), that team's
> activity is included at the verified average level for equivalent fully-logged two-team days, rounded to
> whole events; the effect on headline totals is under one per cent.

This keeps every honest element — line-by-line review, deduplication, the estimation method, its scale
(nine of 48 days) and its materiality (under one per cent) — and keeps the "reconcile exactly with the
HOTC Weekly Data Reports" sentence that follows unchanged. What changes is only the framing: "not
available" (neutral, archival) instead of "not returned" (someone failed to hand it in), and the removal
of the two internal-mechanics tells. No figure changes.

---

### F2 — RECOMMENDED — §7: Viaduct reference goes beyond coordination context

The brief (category 5) allows Viaduct static-guard references only as coordination context, not as ASG
servicing another client. "Holding the Viaduct overnight" reads as the LCF-funded team providing sustained
cover of another operator's site outside the core precinct — it invites the funder question "whose hours
paid for that night?" and, for anyone who knows ASG's client base, hints at whose guard it was. §9 already
uses the right model ("venue static guard"); §7 should match it.

**Current text (§7):**
> **Venue and static security** — coordinated interventions with nightclub, hotel and site guards,
> including holding the Viaduct overnight after an assault on a static guard (14 July).

**Replacement:**
> **Venue and static security** — coordinated interventions with nightclub, hotel and site guards,
> including supporting venue security at the Viaduct after an assault on a venue guard (14 July).

---

### F3 — RECOMMENDED — §4 and §7: Auror-meeting references tie funded patrol hours to an ASG commercial meeting

Deepening the Auror integration is a legitimate partnership positive and should stay in §7. But two
phrasings make the funded team's involvement in ASG's own commercial meeting explicit, and one of them is
defensive — it answers a question ("did you pull guards off the street for it?") that the reader hadn't
asked, thereby planting it. This is exactly the kind of question ASG would rather field in person.

**Current text (§4):**
> the team splitting to hold live response cover during the Auror meeting (17 July)

**Replacement:**
> the team splitting to hold live response cover during partner engagements (17 July)

**Current text (§7):**
> ASG met with Auror's global headquarters on 17 July to deepen the integration, while keeping live
> response cover on the street.

**Replacement:**
> ASG met with Auror on 17 July to deepen the integration.

The §7 replacement also fixes the awkward "met with Auror's global headquarters" (one meets people, not a
building) and drops the defensive tail. Shorter is stronger here.

---

### F4 — RECOMMENDED — §8: survey gap framed as a lapse rather than a design choice

"No survey wave has yet been completed" is a bald admission that invites "why didn't you run it during the
pilot?" The honest facts support a better ordering: present post-pilot timing as the methodological
rationale (which the current text already contains) and let the absence of results follow from it.
The replacement remains fully honest — it still states plainly that no results are in the report.

**Current text (§8):**
> The programme's perceptions survey instrument (business, landlord and public-intercept forms) was
> prepared at pilot commencement. No survey wave has yet been completed, so no survey results are reported
> here. ASG recommends running the survey immediately post-pilot so that measured perceptions are
> referenced to the deployment period.

**Replacement:**
> The programme's perceptions survey instrument (business, landlord and public-intercept forms) was
> prepared at pilot commencement. ASG recommends running the first survey wave immediately post-pilot, so
> that measured perceptions are referenced to the full deployment period; survey results are therefore not
> included in this report.

---

### F5 — OPTIONAL — §6: "passive victims" labels precinct businesses unflatteringly

No store is named, so this passes the brief's letter; it is a tone item only. "Converting passive victims
into active reporters" mildly disparages the very businesses the report is meant to celebrate.

**Current text (§6):**
> **Reporting behaviour coached** — where thefts went unreported, guards followed up and walked staff
> through contacting HOTC immediately, converting passive victims into active reporters.

**Replacement:**
> **Reporting behaviour coached** — where thefts went unreported, guards followed up and walked staff
> through contacting HOTC immediately, so more incidents are reported and actioned.

---

### F6 — OPTIONAL — §4: first approved capacity instance — polish only (not removal)

The three §4 instances are CEO-approved and their framing is verified capacity-focused — no removal is
flagged. Two optional polish points on the 1 June entry: naming Coffee Club associates a specific business
with the one queued call (the 6 June entry is already generic — "one cafe call"), and "standing up" is
ops jargon for a funder audience.

**Current text (§4):**
> 1 June — a Coffee Club caller was queued behind another incident on the morning the uplift was still
> standing up.

**Replacement:**
> 1 June — a café caller was queued behind another incident on the morning the uplift was still mobilising.

---

### F7 — OPTIONAL — §4 table: internal log vocabulary surfacing

The quoted term "team busy" in the pre-uplift row is internal log shorthand appearing verbatim in a funder
document. Same figure, plain wording:

**Current text (§4 table):**
> 211 missed interventions — 29% of all calls; 51 "team busy" instances; 20 simultaneous-incident clashes

**Replacement:**
> 211 missed interventions — 29% of all calls; 51 instances with the team already committed to another
> call; 20 simultaneous-incident clashes

---

## CATEGORY SWEEP — explicit clearance per sensitivity-brief category

1. **Staffing failures — CLEAN.** Each known internal incident was individually checked and is absent:
   the 18 July second-guard no-show / solo SOP-restricted morning (no trace; the report's "none in the
   two-team daytime window after the first week" claim is scoped to the two-team window and does not
   expose it); the 6 June ~45-minute gear-locked deployment delay (the report's 6 June entry is only the
   approved altercation instance); the 7 June B-team absence; the 19/20 June night-guard late arrivals;
   and the 19/26 June and 3 July early shift endings. Nothing in the report reads as an ASG-caused
   deployment delay or absence.
2. **Equipment/admin failures — CLEAN.** No body-camera chargers, keys, phone or radio battery, standby
   periods, or WhatsApp artifacts anywhere in the report.
3. **Internal reporting-quality mechanics — ONE LEAK: §13 (Finding F1).** Elsewhere clean; the §3
   footnote explaining the 2025 five-metric format is a neutral, necessary explanation of the n/a cells
   and should stay.
4. **Internal management matters — CLEAN.** No manager names, no standby orders, no HR or rostering
   language; "flexed" reads as service design, not internal rostering.
5. **Third-party exposure — ONE FLAG: §7 Viaduct (Finding F2).** No ASG staff are named anywhere (all
   references are "guards", "the team", "a guard"); no other ASG client or site is identifiable.
6. **Blame/embarrassment of precinct businesses, Police, or Council — CLEAN** (with the optional §6 tone
   item, F5). All store namings are positive-framed (goods recovered, staff thanked, escorts provided).
   Police are framed favourably throughout ("orderly handover, not emergency callout"; falling escalation
   share). Council appears only in positive joint-working contexts. The FENZ bin-fire line is neutral.
7. **§4 approved capacity instances — PRESENT AND CORRECTLY FRAMED.** All three (1 Jun queued caller,
   6 Jun cafe call during the altercation, 2 Jul night concurrent calls) are framed as capacity findings,
   not staff failures, and the section correctly channels the residual gap toward the night-cover
   business case. Only optional polish flagged (F6, F7).

## SECTION-BY-SECTION PROFESSIONAL READ

- **§1 Executive Summary — clean.** Strong and well-paced. The police-escalation bullet leads with the
  favourable year-on-year comparison; defensible because §3 shows both comparators and explains the
  share-of-attended-demand view.
- **§2 What Was Delivered — clean.** The invoicing and reconciliation sentences are exactly the right
  accountability posture for a funder.
- **§3 Demand & Response — clean.** The interpretive paragraph on rising attended-call counts is
  necessary pre-emption, not defensiveness — without it, "+92% aggressive behaviour" invites a worse
  reading. Keep it.
- **§4 Capacity — framing sound**; see F3, F6, F7.
- **§5 Where the Capacity Went — clean.**
- **§6 Business Engagement — clean** apart from F5.
- **§7 Partnership — two flags** (F2, F3); otherwise reads well.
- **§8 Perceptions of Safety — see F4.**
- **§9 Harm Reduction — clean.** The disclosure of the two third-party-caused injuries is honest,
  correctly scoped ("neither involving force used by the Safety Team"), and the guard-assault mention is
  appropriate transparency about the risk environment, not an internal failure.
- **§10 Positive Stories — clean.** Vivid but controlled; all store namings are victim/beneficiary
  framed.
- **§11 CPTED Alignment — clean.**
- **§12 Beyond the Pilot — clean.** The extension recommendation is well-grounded in the evidence and
  positions the night-cover case without overreaching.
- **§13 Data Sources — F1 (blocker)**; with the replacement paragraph it becomes a strength.

**Bottom line:** one blocker (§13 rewording), three recommended edits (§7 Viaduct, §4+§7 Auror-meeting
phrasing, §8 survey reframe), three optional polish items. No verified figure changes in any replacement.
With F1 applied, the report is safe to send; with F2–F4 also applied, it is polished for the Council
audience.
