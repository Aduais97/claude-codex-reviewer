# PRE-LAWYER HARDENING REVIEW
## Agreement for Sale and Purchase of Shares — Nikki Wairau Christian (Vendor) to Ahmad Duais (Purchaser)
### Absolute Security Group Limited and SLS RTC Limited — NZ$260,000

---

# A1. Executive Summary

**Verdict: the draft is structurally sound, materially stronger than either precedent it was built from, and is NOT yet ready to send to the solicitors for settlement — four BLOCKER findings must be resolved first, and one of them (the Lockhart trustee question) determines what is actually being sold.**

This review tested `SPA_DRAFT.md` against the agreed deal terms in `deal_facts.txt`, against both precedents (`PRECEDENT_ProHost_2023.pdf`, drafted by Franklin Law, and `PRECEDENT_Gwin_2025.pdf`), and against the enforceability standards a New Zealand commercial solicitor would apply. The output is **25 numbered findings: 4 BLOCKER, 18 RECOMMENDED, 3 OPTIONAL**, each with exact suggested wording, plus a schedule of 14 placeholders and unresolved facts that must be completed before signing.

**The four blockers, in plain language:**

1. **The subject matter of the sale is unresolved (F1).** The Companies Register at 30 June 2026 shows the Vendor registered for only 1 share (0.01%) in each company, with Lockhart Trustee Services No.222 Limited holding 1,524 shares (15.24%) in each. A $260,000 price for 2 registered shares is inconsistent with the register. Until it is confirmed whether the Lockhart parcel is the Vendor's beneficial stake — and, if so, the trustee is joined as a party and the `[●]` share numbers completed — the agreement cannot be signed. The draft anticipates this correctly (clause 1.2, Drafting Note 1) but cannot resolve it on paper.

2. **Three clauses could be read as restricting communications with the regulator (F2).** Clause 11.1(c) restrains "interference" with the Companies' relationships with *regulators*; clause 12.1(a) permits disclosure only "as required by" a regulator (not voluntary disclosure); and clause 13.1's non-disparagement has no regulator carve-out. With an open PSPLA → CIPU process, any wording capable of being portrayed as restraining or discouraging the Vendor from speaking to the regulator is unacceptable — both as a matter of enforceability and, more importantly, because the parties' deliberate design (clause 14.2) is that nothing is concealed and personal regulatory responsibility is preserved. An express regulator-communications carve-out fixes all three clauses at once.

3. **No survival clause (F14).** If the agreement is cancelled after a dispute, the restraints, confidentiality and non-disparagement obligations — the very things Background E says the Purchaser is paying for — are at risk of falling away with the cancellation. An express survival clause, with a sensible exception where the Shares are re-transferred to the Vendor, is essential in a deferred-consideration deal.

4. **Exercising the set-off could hand the Vendor a cancellation right (F23).** If the Purchaser withholds an instalment under clause 15 in good faith, the Vendor could characterise the withholding as a payment default, serve a 14-day notice under clause 6, and cancel — demanding the shares back — before any arbitration resolves whether the set-off was proper. Clause 15 must expressly provide that a withholding in accordance with it is not a "default" for the purposes of clauses 5 and 6 until an arbitrator rules and the Purchaser fails to pay.

**Deal-term accuracy is otherwise clean.** Every number, date, party name, company number, NZBN, registered office and payment in the draft exactly matches `deal_facts.txt` (the full diff table is at §D1). The three instalments sum correctly to $260,000. The draft did **not** inherit either of the Gwin precedent's recital errors (the NZBN-quoted-as-company-number, or the 1,690 share count), and it did not inherit ProHost's numbering artifacts or its inverted "receipt by the Purchaser" settlement condition. The 1,690 (Gwin 2025) versus 10,000 (deal_facts 2026) issued-share discrepancy is logged as an unresolved fact to confirm from a current register extract — it is consistent with a share restructure between March 2025 and June 2026, but must be positively confirmed, not assumed.

**Regulatory integrity — explicit confirmation.** The draft *as designed* preserves personal regulatory responsibility and conceals nothing: clause 14.1 secures cooperation, clause 14.2 expressly provides that no personal regulatory liability is transferred or released, clause 12.2 permits disclosure to the PSPLA and other regulators, and clause 8.2(c) carves personal regulatory liability out of the mutual release. The three defects identified in F2 are drafting leaks against that design, not departures from it — and every suggested wording in this report has been checked against the same constraint. Nothing recommended in this report limits, transfers, or conceals personal regulatory liability, and this report does not recommend reinstating either of the Gwin precedent's known defective clauses (its clause 2(a) sole-discretion compensation wording and its clause 14.1 forfeiture clause).

**The purchaser's three stated requirements are substantially met but need hardening.** The sector restraint (clause 10) is the strongest clause in the document — cascading periods and areas, a severance formula, and a reasonableness acknowledgement — but the carve-out in clause 10.4(b) partially reopens the door it closes (F3), the Restrained Business definition misses several sector activities (F4), and "client" is never defined (F5). The set-off (clause 15) and settlement-deliverables (clause 3) machinery works but has the gaps identified in F7, F10, F11, F17 and F23. The most valuable additions a solicitor would make are the pre-settlement conduct covenant and no-prior-diversion warranty (F24) — the Vendor works in the business today, with full access to clients, rosters and pricing, and knows this template from the other side of the table.

**Findings by severity:**

| Severity | Count | Findings |
|---|---|---|
| BLOCKER | 4 | F1, F2, F14, F23 |
| RECOMMENDED | 18 | F3–F13, F15–F20, F24 |
| OPTIONAL | 3 | F21, F22, F25 |

**Fix-before-solicitors list (shortest path to a settlement-ready draft):** resolve the Lockhart question and complete the share numbers (F1); insert the regulator-communications carve-out and amend clauses 11.1(c) and 12.1(a) (F2); add the survival clause (F14); add the set-off/default firewall (F23); then apply the 18 RECOMMENDED amendments, all of which are drafted ready to paste in §A4.

---

# A2. Context

## A2.1 Scope resolution — why this is a legal-draft review, not an acquisition analysis

The engagement template contemplates a generic acquisition analysis (financials, organisational benchmarking, valuation). The job-specific brief states — correctly — that this is a **legal-draft review, not an acquisition analysis**, and the corpus confirms it: the source documents are one draft agreement, two precedents, and one deal-facts sheet. They contain **no** profit-and-loss data, no balance sheet, no headcount or organisational data, no client list and no market data, and the price is already agreed at $260,000. Accordingly:

| Mandated generic section | Disposition in this report |
|---|---|
| Executive summary | Delivered above as a sign-readiness verdict with blocker count in place of investment thesis |
| Business overview | Reduced to the party/company/register context below — the only corpus facts |
| Organisational analysis | **Not performable.** The corpus contains zero organisational data — no employee list, no functions, no revenue to divide by FTE. The only staffing fact in any source document is the Vendor's own weekly pay of ~$1,923 (`deal_facts.txt`), which is relevant to the employment release (§D4.3), not to organisational benchmarking. Producing headcount maps, revenue-per-FTE ratios, industry benchmarks or restructuring scenarios from this corpus would require inventing every input, and this report will not do that. If organisational analysis is required, it needs a payroll export, an org chart and management accounts — none are in the corpus. |
| Financial analysis | **Not performable.** The only financial facts are the price ($260,000), the instalment profile ($100k/$80k/$80k) and the 12% default interest rate. These are reviewed as deal terms (§D1) and purchaser protections (§D6). There is no reported EBITDA to normalise and no add-backs to validate. |
| Valuation analysis | **Out of scope.** The price is agreed. This report notes only where the price interacts with legal risk: the restraint-consideration recital (Background E), and the register anomaly that makes $260,000 for 2 registered shares inconsistent (F1). |
| Strategic fit | **N/A.** The Purchaser already co-owns and runs both companies; this is a partner buyout, not a market entry. |
| Risk assessment | Delivered as §D4 (enforceability risk) and §D6 (purchaser protection), plus the regulatory-integrity checks throughout. |
| Deal structure | Delivered as §D6: deferred-consideration mechanics, set-off, default and security posture. |

## A2.2 Parties, companies and register position

**Vendor:** Nikki Wairau Christian — current business partner of the Purchaser. She was herself a **purchaser** under the 2023 Pro Host precedent (one of four purchasers, alongside Ahmad Duais, Hasibullah Nabawi and Shannon Gwin, buying Pro Host Security Limited from Sharon Rose Tahere under the Franklin Law draft). She therefore knows this template line by line, from the buyer's side. Every change the draft makes to that template is negotiation-visible to her; §D5 arms the Purchaser's solicitor with the justification for each.

**Purchaser:** Ahmad Duais — currently the largest registered shareholder of both companies (44.59% each).

**The Companies (identical registers as at 30 June 2026):**

| | Absolute Security Group Limited | SLS RTC Limited |
|---|---|---|
| Company number | 8517467 | 9325956 |
| NZBN | 9429050952960 | 9429052674921 |
| Registered office | 7/220 Queen Street, Auckland Central 1010 | Office 2, Level 7, 220 Queen Street, Auckland Central 1010 |
| Issued ordinary shares | 10,000 | 10,000 |

**Register position, both companies (30 June 2026):**

| Shareholder | Shares | % |
|---|---|---|
| Ahmad Duais | 4,459 | 44.59% |
| Hasibullah Nabawi | 4,016 | 40.16% |
| Lockhart Trustee Services No.222 Limited | 1,524 | 15.24% |
| Nikki Wairau Christian | 1 | 0.01% |

The unresolved question at the centre of F1: `deal_facts.txt` states the subject of the sale is **all** of the Vendor's shares in both companies, but the Vendor's registered holding is 1 share per company. If the Lockhart trustee parcel (1,524 per company) is the Vendor's beneficial stake, the deal is for 1,525 shares per company (15.25%) and the trustee must be joined; if it is not, what $260,000 buys must be re-established before anything is signed.

**Deal terms (agreed, per `deal_facts.txt`):** NZ$260,000 total — $100,000 at settlement on 1 August 2026; $80,000 on 1 September 2026; $80,000 on 1 October 2026.

**Regulatory context:** both Companies and their directors are subject to an open PSPLA → CIPU process. The draft's clause 14 (regulatory cooperation; no transfer or release of personal regulatory liability) is a deliberate design feature, and this report treats "nothing may conceal, transfer or release personal regulatory liability" as a hard constraint on every finding.

**Employment context:** the Vendor works in the business (weekly pay ~$1,923). Her employment must end at settlement with a proper release — a contractual release does not bar a personal grievance; only a record of settlement certified under s 149 of the Employment Relations Act 2000 does (§D4.3, F15).

---

# A3. Methodology and Sources

**Sources:** (i) `SPA_DRAFT.md` (the document under review); (ii) `deal_facts.txt` (agreed terms and Companies Register position, 20–21 July 2026); (iii) `PRECEDENT_ProHost_2023.pdf` (Franklin Law); (iv) `PRECEDENT_Gwin_2025.pdf`. Every finding cites the draft clause and the corpus document it is tested against. Statutory and case-law references (Contract and Commercial Law Act 2017, Employment Relations Act 2000, Arbitration Act 1996, *127 Hobson Street Ltd v Honey Bees Preschool Ltd* [2020] NZSC 53) are legal context, not corpus evidence — this is a hardening pass, not a legal opinion.

**Severity rubric:**

- **BLOCKER** — factually wrong against `deal_facts.txt`, legally defective, self-contradictory, or would fail or backfire if signed as-is (including anything that could be read as concealing regulatory matters).
- **RECOMMENDED** — a careful NZ commercial solicitor would add or amend it; the agreement functions without it but the Purchaser is materially less protected.
- **OPTIONAL** — polish, clarity, or belt-and-braces.

**Finding format:** sequential number → severity → clause reference → issue with a concrete failure scenario → **exact suggested wording** (insert/replace text ready to paste; for deletions, the words to strike). Findings are ordered most-severe-first within each dimension; the consolidated list in §A4.7 re-orders them most-severe-first overall.

**Verification passes, in order:** (P1) field-by-field deal-term diff; (P2) clause-by-clause completeness walk against the Purchaser's three stated requirements; (P3) cross-reference and defined-terms audit; (P4) enforceability tests; (P5) three-way precedent comparison; (P6) adversarial pass — the draft read as the Vendor's solicitor would attack it, given her inside knowledge and familiarity with the template; (P7) placeholder sweep.

**Wording discipline:** suggested wording adapts the corpus's existing drafting style (the ProHost/Franklin Law register and the draft's own house style) rather than inventing a new one, so the settling solicitors receive a consistent document. No whole-agreement redraft is offered. Matters requiring legal advice, external searches or third parties are routed to §A5, not presented as drafting findings.

---

# A4. Findings

## D1. Deal-Term Accuracy (Pass P1)

**Method:** field-by-field diff of every fact in `deal_facts.txt` against the draft. Matches are shown as well as mismatches — the solicitors need positive confirmation, not just exceptions.

| # | Fact | deal_facts.txt value | Draft location | Draft value | Match? |
|---|---|---|---|---|---|
| 1 | Vendor name | Nikki Wairau Christian | Parties 1; Background A–D; execution block | Nikki Wairau Christian | ✔ |
| 2 | Purchaser name | Ahmad Duais | Parties 2; execution block | Ahmad Duais | ✔ |
| 3 | ASG company number | 8517467 | Background A | 8517467 | ✔ |
| 4 | ASG NZBN | 9429050952960 | Background A | 9429050952960 (correctly labelled NZBN) | ✔ |
| 5 | ASG registered office | 7/220 Queen Street, Auckland Central 1010 | Background A | 7/220 Queen Street, Auckland Central, Auckland 1010 | ✔ |
| 6 | ASG issued shares | 10,000 ordinary | Background A | 10,000 ordinary | ✔ |
| 7 | SLS company number | 9325956 | Background B | 9325956 | ✔ |
| 8 | SLS NZBN | 9429052674921 | Background B | 9429052674921 | ✔ |
| 9 | SLS registered office | Office 2, Level 7, 220 Queen Street, Auckland Central 1010 | Background B | Office 2, Level 7, 220 Queen Street, Auckland Central, Auckland 1010 | ✔ |
| 10 | SLS issued shares | 10,000 ordinary | Background B | 10,000 ordinary | ✔ |
| 11 | Subject: ALL Vendor's shares in BOTH companies incl. trustee/nominee holdings | Yes | Background D; cl 1.2 | "all of the shares … held by the Vendor, or held by any trustee or nominee on the Vendor's behalf" | ✔ in words; share counts are `[●]` — **F1** |
| 12 | Price | NZ$260,000 total | cl 2.1 | NZ$260,000.00 | ✔ |
| 13 | Instalment 1 | $100,000 at settlement 1 Aug 2026 | cl 2.2(a) + cl 1.1 | $100,000.00 on the Settlement Date (1 Aug 2026) | ✔ |
| 14 | Instalment 2 | $80,000 on 1 Sep 2026 | cl 2.2(b) | $80,000.00 on 1 September 2026 | ✔ |
| 15 | Instalment 3 | $80,000 on 1 Oct 2026 | cl 2.2(c) | $80,000.00 on 1 October 2026 | ✔ |
| 16 | Instalments sum to price | $100k+$80k+$80k = $260k | cl 2.1–2.2 | $260,000.00 | ✔ |
| 17 | Settlement Date | 1 August 2026 | cl 1.1 | 1 August 2026 "or such other date agreed in writing" | ✔ |
| 18 | Register position 30 Jun 2026 | Duais 4,459; Nabawi 4,016; Lockhart 1,524; Christian 1 (both companies) | Drafting Note 1 | Recites Vendor 1 share (0.01%) and Lockhart 1,524 (15.24%) in each | ✔ consistent |
| 19 | 12% p.a. default interest (both precedents) | Yes | cl 5.1 | 12% per annum | ✔ carried |
| 20 | 14-day default/remedy windows (both precedents) | Yes | cl 6.1, cl 7.1 | 14 days each | ✔ carried |
| 21 | 2-year client non-solicit (both precedents) | Yes | cl 11.1 | 24 months | ✔ carried |
| 22 | Negotiation → arbitration, Arbitration Act 1996, single arbitrator, NZLS appointment | Yes | cl 17.1 | Identical structure | ✔ carried |

**Inherited-error check (Gwin and ProHost):** the Gwin precedent's Background B recites ASG as "incorporated under number 9429050952960" — that is the **NZBN**, not the company number — and recites **1,690** issued shares. The draft inherited **neither** error: it states the company number (8517467) and NZBN separately and correctly, and recites 10,000 shares, matching `deal_facts.txt`. The 1,690 (2025) vs 10,000 (2026) discrepancy is consistent with a share restructure between March 2025 and June 2026 but must be confirmed from a current register extract before signing — logged at §A6 item 9. The draft also did not inherit ProHost's revision artifacts (its "15.14/16.15/17.16/18.17/19.18" double numbering) or ProHost clause 3's inverted condition ("Subject to receipt by the **Purchaser** of the payments…", which also mis-cites "clause 2.1(a) and (b)" when the payments sit in clause 2(a)–(d)) — the draft's clause 3.1 correctly reads "Subject to receipt by the **Vendor** of the payment under clause 2.2(a)".

**Conclusion on accuracy:** no numeric, date, party or company-identifier mismatch exists between the draft and `deal_facts.txt`. The single accuracy blocker is the unresolved subject-matter quantum:

---

### F1 — [BLOCKER] — Background D, cl 1.2, cl 2.1, execution block — the number of shares being sold is unresolved and the register contradicts the price

**Issue.** `deal_facts.txt` (register position, 30 June 2026) shows the Vendor registered for 1 share (0.01%) in each Company and Lockhart Trustee Services No.222 Limited for 1,524 shares (15.24%) in each. Background D leaves the share counts as `[●]`, clause 2.1 leaves the price apportionment as `[●]`, and the Lockhart execution block is conditional. If the Lockhart parcel is not the Vendor's beneficial stake, the Purchaser would be paying $260,000 for 2 registered shares — inconsistent with the register and the price, as the draft's own Drafting Note 1 warns. Concrete failure scenario: the agreement is signed with the Vendor alone; at settlement Lockhart declines to transfer its 1,524 shares in each company; the Purchaser has paid (or is committed to pay) $260,000 for 0.02% of the group and has no contractual claim against the trustee, which is not a party. Clause 1.2's "the Vendor shall procure" obligation gives a damages claim against the Vendor only — an unsecured claim against the person he has just paid.

**Fix (exact steps and wording).** Before signing: (i) confirm from the trust records and the Companies Register whether the Lockhart holding is the Vendor's beneficial stake; (ii) if yes, complete Background D as: "…being **1,525** ordinary shares in ASG and **1,525** ordinary shares in SLS (together the **Shares**), together with all rights attaching to them."; join Lockhart as a party under clause 1.2 (see F19 for the joinder mechanics) and activate its execution block; (iii) if no, do not sign — the subject matter and price must be re-established and the agreement re-papered. In either case, complete the clause 2.1 apportionment per the accountant's advice (§A5 item 4). This finding cannot be cleared by drafting alone; it is a factual gate.

---

## D2. Completeness Against the Purchaser's Stated Requirements (Pass P2)

The Purchaser's three requirements, in his own words (`deal_facts.txt`): (i) the Vendor must **"not go and work within the security guarding sector"**; (ii) **"restraints around customers"**; (iii) **"ensuring we put good protections"**. Each requirement is mapped to its implementing clause(s) and stress-tested; every gap is a finding with drafted wording.

### Requirement (i) — sector restraint → clause 10

Clause 10 is the strongest clause in the draft and has no counterpart in either precedent (Gwin clause 10 restrains only client diversion; ProHost clause 12 the same). It restrains carrying on or being engaged in a Restrained Business (10.1(a)), servicing 24-month lookback clients (10.1(b)), with cascading periods 24→18→12→6 months (10.2), cascading areas NZ→North Island→Auckland (10.3), carve-outs (10.4), and a severance-and-reasonableness clause (10.5) that correctly references both 10.2 and 10.3. The cascade produces 12 severable period×area combinations — the formula wording in 10.5 is effective and should be kept rather than enumerating them. Two gaps:

---

### F3 — [RECOMMENDED] — cl 10.4(b) — the "role outside the Restrained Business" carve-out reopens the door clause 10.1(a) closes

**Issue.** Clause 10.1(a) restrains the Vendor from being "engaged in… any business which provides" the listed security services. Clause 10.4(b) then carves out "working in a role outside the Restrained Business". Because "Restrained Business" is defined by reference to what the *business* provides, not what the *role* involves, the carve-out is ambiguous in both directions: (a) the Vendor could take an in-house security role — e.g. loss-prevention officer employed directly by a retail chain — and argue her employer is a retailer, not a "business which provides… retail loss prevention" services to others, so the role is "outside the Restrained Business"; and (b) conversely, she could take a nominally administrative role at a direct competitor and argue the same. Either reading defeats the Purchaser's stated requirement that she "not go and work within the security guarding sector". Tested against `deal_facts.txt` (purchaser requirement (i)) and the Gwin/ProHost precedents (neither of which has a sector restraint at all, so there is no precedent wording to fall back on).

**Fix (replace clause 10.4(b) in full):**

> (b) working in a role which does not involve performing, managing, supervising, selling or soliciting any of the services described in clause 10.1(a), and which is not with or for a business that provides any of those services in competition with either Company; or

This preserves her genuine freedom to work outside the sector (the enforceability safety valve) while closing both the in-house-security and the admin-role-at-a-competitor readings.

---

### F4 — [RECOMMENDED] — cl 10.1(a) — the Restrained Business definition does not cover the whole security sector

**Issue.** Clause 10.1(a) lists "security guarding, crowd control or host security, event security, mobile patrol, static guarding, retail loss prevention, or security consultancy services". Measured against the Purchaser's requirement that the Vendor not work "within the security guarding sector", the list omits several activities a licensed security operator can pivot to with the same client book and staff: personal/close protection, alarm or CCTV monitoring and response, cash-in-transit and valuables escort, concierge/corporate reception security, the supply of security personnel by labour-hire or subcontract (the most likely leakage route for a guarding business — supplying guards to a head contractor rather than to the end client), and security training. Failure scenario: the Vendor establishes a "security staffing agency" supplying licensed guards to competitors servicing the Companies' former clients, and argues staffing supply is not "security guarding… services". Deliberately **not** added: any restraint on the Vendor holding or applying for a PSPLA licence or certificate of approval — her licensing status is a matter between her and the regulator, and touching it would collide with the regulatory-integrity constraint (deal_facts: the agreement must not interfere with or conceal anything in the PSPLA/CIPU process).

**Fix (replace the service list in clause 10.1(a)):**

> (a) carry on, be engaged in, or be concerned or interested in any business which provides security guarding, crowd control or host security, event security, mobile patrol, static guarding, retail loss prevention, personal or close protection, alarm or CCTV monitoring or response, cash-in-transit or valuables escort, concierge or corporate security, security training, the supply of security personnel (whether by employment agency, labour hire or subcontract), or security consultancy services (**Restrained Business**); or

---

### Requirement (ii) — customer restraints → clauses 10.1(b) and 11.1(a)

The two customer restraints are complementary by design — clause 10.1(b) stops the Vendor *servicing* former clients (riding on the cascading Restraint Period and Restraint Area), while clause 11.1(a) stops her *soliciting or accepting* their custom for a flat 24 months. Both carry the 2-year client-restraint concept from Gwin clause 10 and ProHost clause 12, substantially strengthened (the precedents restrain only being "instrumental in the diversion" of clients; the draft adds acceptance of custom and servicing). Three defects:

---

### F5 — [RECOMMENDED] — cl 10.1(b), cl 11.1(a) — "client" is undefined, and clause 11.1(a) has no lookback at all

**Issue.** Clause 10.1(b) restrains servicing "any person who was a client of either Company at any time in the twenty-four (24) months before the Settlement Date" — a lookback, but no definition of "client". Clause 11.1(a) restrains diversion of "any client of either Company" — no lookback and no definition, so it is ambiguous whether it captures clients as at settlement, at the time of breach, or ever. For a guarding business that staffs bars and venues, often under another party's head contract (the ProHost precedent's whole conditional structure — its clause 7 client-consent condition naming Star Hospitality Group, Lime Investments, Florrie McGreals and Bar101 — shows this group's client relationships run through hospitality operators), "client" must capture the venue/site relationships, not only direct contract counterparties. An undefined term invites the narrowest reading at exactly the moment it matters — in front of an arbitrator, argued by the Vendor, who knows precisely how the client relationships are structured.

**Fix (insert as new clause 11.2, and simplify the two uses):**

> 11.2 In clauses 10 and 11, **client** means any person to whom either Company provided services, or who engaged either Company to provide services (whether directly or through an agent, head contractor, facilities manager or venue operator, and including the operator or occupier of any site or venue at which either Company provided services), at any time in the twenty-four (24) months before the Settlement Date.

Then in clause 10.1(b) replace "any person who was a client of either Company at any time in the twenty-four (24) months before the Settlement Date" with "any client", and in clause 11.1(a) rely on the defined term (no further change needed). Renumber the existing clause 11 body as 11.1 if not already.

---

### F6 — [RECOMMENDED] — cl 11.1 — the non-solicit has no cascade and no reasonableness acknowledgement; if 24 months falls, everything falls

**Issue.** Clause 10's restraints degrade gracefully (24→18→12→6 months; NZ→North Island→Auckland; clause 10.5 severance). Clause 11's restraints are a flat 24 months with no cascade and no acknowledgement of reasonableness. If the Purchaser's protection is read down — and the customer restraints are the ones the Vendor is most likely to test, because the client relationships are where her inside knowledge is worth money — clause 10.1(b) survives at a shorter period via the cascade, but clause 11.1(a)'s no-solicitation/no-acceptance line is all-or-nothing. Under s 83 of the Contract and Commercial Law Act 2017 a court *may* modify an unreasonable restraint rather than strike it, but the cascading structure removes the gamble; there is no reason clause 11 should gamble when clause 10 does not.

**Fix (insert as new clause 11.3):**

> 11.3 If any period in clause 11.1 is held unenforceable, it shall be reduced to eighteen (18) months; if that period is held unenforceable, to twelve (12) months; and if that period is held unenforceable, to six (6) months. Each resulting restraint is separate and severable, and clause 10.5 applies to the restraints in this clause 11 as it applies to those in clause 10.

---

### F25 — [OPTIONAL] — cl 11.1(b) — the 12-month staff lookback is shorter than the 24-month client lookback: record the intent

**Issue.** Clause 11.1(b) protects staff with a 12-month pre-settlement lookback; the client protection (10.1(b), and F5's definition) uses 24 months. The asymmetry is defensible — courts scrutinise employee-solicitation restraints more closely than client restraints, and staff turnover in guarding is high, so a 12-month lookback tracks the realistically protectable connection — but it should be a decision, not drift. No change is recommended; if the Purchaser prefers symmetry, change "twelve (12) months" to "twenty-four (24) months" in clause 11.1(b), accepting some incremental enforceability risk on that limb (severable in any event under F6's clause 11.3).

---

### Requirement (iii) — "good protections" → clauses 3, 12, 13, 15, and the missing machinery

Clause 12 (confidentiality, unlimited in time — appropriate for a business sale), clause 13 (non-disparagement and controlled announcements) and clause 15 (set-off) all exceed both precedents, which contain none of them. The regulator-facing defects in clauses 11.1(c), 12.1(a) and 13.1 are consolidated into F2 below because they share one fix. The settlement-deliverables walk (clause 3.1(a)–(f)) and the missing general machinery produce F7–F9.

---

### F2 — [BLOCKER] — cl 11.1(c), cl 12.1(a), cl 13.1 — three clauses are capable of being read as restraining communications with the regulator during an open PSPLA/CIPU process

**Issue.** Three separate provisions leak against the draft's own regulatory-integrity design (clause 14.2; deal_facts: "the agreement must NOT purport to release or conceal personal regulatory liability"):

1. **Clause 11.1(c)** restrains the Vendor from "interfer[ing] with the relationship between either Company and any of its clients, suppliers, landlords, licensors **or regulators**". A complaint, disclosure or adverse submission by the Vendor to the PSPLA or CIPU about the Companies is literally an act that affects "the relationship between either Company and… regulators". A restraint that could be invoked — or even portrayed — as penalising the Vendor for speaking to the regulator is unacceptable in an open regulatory process, and would hand the Vendor (or the regulator) a narrative that the Purchaser paid to control regulatory communications.
2. **Clause 12.1(a)** permits disclosure of confidential information only "as **required** by law or a regulator". Voluntary, unprompted disclosure to a regulator is not "required" — so on its face the confidentiality clause forbids the Vendor volunteering information to the PSPLA/CIPU. Same vice.
3. **Clause 13.1** (non-disparagement) has no regulator carve-out at all: a truthful, critical statement to the PSPLA plainly "disparages… the Companies" within the clause's words.

Failure scenario: during the CIPU process the Vendor makes a disclosure adverse to the Companies; the Purchaser's solicitor (or the Vendor's, pre-emptively) is asked whether the agreement restrained it; clauses 11.1(c), 12.1 and 13.1 are put in front of the regulator as evidence the parties contracted to manage regulatory communications. Even if never enforced, the words alone are the harm. This is a BLOCKER under the review's regulatory-integrity rule: signed as-is, the draft can be read as concealing.

**Fix (three coordinated amendments — all must be made):**

1. In clause 11.1(c), strike the words "**or regulators**", so it reads: "…interfere with the relationship between either Company and any of its clients, suppliers, landlords or licensors."
2. In clause 12.1, replace limb (a) "as required by law or a regulator" with: "**(a) as required or permitted by law, or as made to any regulator in accordance with clause 14.4**".
3. Insert a new clause 14.4 (after the notification covenant added by F20; renumber accordingly):

> 14.4 Nothing in this agreement (including clauses 10 to 13) prevents, restricts, penalises or discourages any party from making any report, complaint, disclosure or submission to, cooperating with, or otherwise communicating with, any regulator or government agency (including the Private Security Personnel Licensing Authority, its Complaints, Investigation and Prosecution Unit, the New Zealand Police, the Companies Office, Inland Revenue, WorkSafe New Zealand, or the Ministry of Business, Innovation and Employment), whether or not the communication is required by law, and no such communication is a breach of this agreement or grounds for set-off under clause 15.

The closing words "or grounds for set-off under clause 15" matter: clause 15.1 triggers on material breach of clauses 10–13, so without them the set-off could itself be portrayed as a financial penalty held over regulatory communications.

---

### F7 — [RECOMMENDED] — cl 3.1 — settlement-deliverables gaps: share certificates, bank signatories, multi-factor authentication, vehicles and physical property

**Issue.** Clause 3.1(a)–(f) carries and improves both precedents' settlement machinery (ProHost cl 3.1–3.5; Gwin cl 3.1–3.4): share transfers, board resolutions, charge releases, resignation from office, a no-claims acknowledgement extended to current account and dividends, and a property/credentials/logins catch-all. Four gaps a solicitor would close, each with a concrete failure mode in this deal: (i) **share certificates** — if either Company has issued certificates, transfers may not be registrable without them; if none were issued, the Purchaser should hold written confirmation of that; (ii) **bank and payroll signatory removal** — clause 3.1(f) delivers "logins" but does not oblige the Vendor to sign the bank's own mandate-change forms, which banks require; a departing signatory who never signs the forms retains authority on paper; (iii) **multi-factor authentication** — "logins and administrative rights" are useless if 2FA still routes to the Vendor's personal phone (a live issue for banking, Xero, social media and email admin); (iv) **vehicles and physical property** — the Gwin deal (its clause 4, vehicle QEF939) shows vehicles are live issues in this group; clause 3.1(f)'s list ("keys, access cards…") does not clearly reach vehicles or other chattels in the Vendor's possession.

**Fix (replace clause 3.1(f) and add new (g) and (h)):**

> (f) all property of each Company in the Vendor's possession or control, including any vehicles, equipment and other physical property, keys, access cards and credentials, uniforms, identification, devices, documents and records, client information, and all logins and administrative rights to email, software, banking and social media accounts of the Companies, together with the transfer or re-registration of any device, phone number or authentication method used for multi-factor access to any of those accounts;
>
> (g) the share certificates (if any) for the Shares or, if none have been issued, written confirmation by each Company's board to that effect; and
>
> (h) all forms and authorities required by each Company's bank, accounting-software provider and payroll provider to remove the Vendor as a signatory or authorised user, duly executed by the Vendor.

(F15 adds a further deliverable (i) — the signed record of settlement — and F18 adds (j) — pre-emption waivers; the final lettering should run (a)–(j).)

---

### F8 — [RECOMMENDED] — cl 16.3 — notice mechanics are incomplete: no addresses, no deemed receipt

**Issue.** Every enforcement path in the agreement begins with a written notice — clause 6.1 (Vendor's default notice), 7.1 (Purchaser's default notice), 15.1 (set-off notice), 17.1(a) (dispute particulars) — yet clause 16.3 says only that notices "may be given by hand, post or email to the addresses notified by each party in writing", and no address is notified anywhere in the document. There are no deemed-receipt rules, so every notice invites a dispute about whether and when it was received — fatal in a document whose remedy windows (7 and 14 days) run from notice. Failure scenario: the Purchaser emails a clause 15.1 set-off notice; the Vendor asserts non-receipt; the arbitrator must decide a service question before reaching the merits, while the clause 6 default clock (F23) allegedly runs against the Purchaser.

**Fix (replace clause 16.3 in full; addresses go to the §A6 completion checklist):**

> 16.3 Notices under this agreement must be in writing and given by hand, by post or by email to the relevant party at the address stated below, or at any other address that party notifies in writing:
>
> Vendor: [●] (post) / [●] (email)
> Purchaser: [●] (post) / [●] (email)
>
> A notice is deemed received: (a) if given by hand, when delivered; (b) if posted, on the third working day after posting; and (c) if emailed, at the time shown on the sender's system as the time of sending, unless that time is after 5.00 pm on a working day or on a non-working day, in which case at 9.00 am on the next working day.

---

### F9 — [RECOMMENDED] — cl 2.2, cl 15.1, cl 16.3 — undefined terms: "working day" and "material breach"

**Issue.** "Working days" is used in clause 2.2 (bank-account nomination "at least two (2) working days before the relevant payment date") and in F8's and F23's suggested wording, but is defined nowhere. "Material breach" is the trigger for the entire set-off regime (clause 15.1) and is likewise undefined — the Vendor's first answer to any set-off notice will be "the breach, if any, was not material". The other quasi-defined terms audited (§D3(b)) are acceptable as drafted: "confidential information" in clause 12.1 is lower-case but immediately particularised by the inclusive list (client lists, pricing, rosters, financial information, operational methods), and "Purchaser's nominee" needs no definition.

**Fix (insert as new clause 1.3):**

> 1.3 In this agreement: **working day** means a day other than a Saturday, a Sunday, or a public holiday observed in Auckland, New Zealand; and a breach is **material** if its effect on either Company, its business or the value of the Shares is more than trivial.

---

## D3. Internal Consistency (Pass P3)

**Method:** (a) cross-reference audit, (b) defined-terms audit, (c) structural audit. Results tabulated with pass/fail; failures become findings F10–F13.

### (a) Cross-reference audit

| # | Cross-reference | Result |
|---|---|---|
| 1 | cl 2.3 → cl 15 (set-off limited to instalments 2.2(b), (c)) | **FAIL** — cl 15.1 says "the instalments in clause 2.2" without limitation, contradicting cl 2.3 → **F10** |
| 2 | cl 3.1 opening ↔ cl 2.2(a) (payment and delivery both due on Settlement Date, each conditional on the other) | **FAIL** — no simultaneous-exchange mechanic → **F11** |
| 3 | cl 3.1(e) ↔ cl 9 ↔ cl 3.2 (no-claims acknowledgement carve-outs) | PASS — 3.1(e) and 3.2 both except only the unpaid Purchase Price balance and the clause 9 final pay; cl 9.1's "normal pay cycle" timing is consistent with those carve-outs |
| 4 | cl 1.2 (trustee joinder) ↔ Background D ↔ conditional execution block ↔ Drafting Note 1 | PASS structurally, but the joinder mechanics are undercooked → **F19** (D4.7) |
| 5 | Background E "clauses 10 to 14" ↔ cl 1.2 "clauses 10 to 14" | **FAIL** — both should reference 10 to 13 → **F12** |
| 6 | cl 15.1 triggers → cl 4, cl 5, "clauses 10, 11, 12 or 13"; 7-day remedy window vs cl 6/7 14-day windows | Partial — references resolve; "material breach" undefined (**F9**); 7-day window unworkable for irremediable breaches (**F17**); the 7 vs 14-day difference itself is acceptable (a set-off notice and a default notice do different jobs) |
| 7 | cl 17.1(c) injunction carve-out "clauses 10 to 13" — cl 14 excluded | PASS — intentional and correct: regulatory cooperation should not be enforced by injunction, and an injunction touching clause 14 would sit badly with the regulatory-integrity constraint. Confirmed the carve-out covers clauses 11, 12 and 13 by number |
| 8 | cl 8.2 mutual release: "Subject to settlement occurring and to clause 4"; carve-outs (a)–(c) ↔ cl 14.2 | PASS — warranty claims survive via the "subject to clause 4" words; carve-out (c) ("any personal liability of a party to a regulator or other third party") aligns with cl 14.2; carve-out (b) (fraud or dishonesty) adequately protects against concealed pre-settlement misconduct, which answers the deferred-consideration concern without a further known-matters carve-out |
| 9 | cl 9.2 s 149 record — obligation, condition or intention? | **FAIL** — drafted as an intention ("The parties intend…") and the record is not a cl 3.1 deliverable → **F15** (D4.3) |
| 10 | cl 6.1(b) cancellation ↔ survival of cl 10–14 | **FAIL** — no survival clause anywhere → **F14** (D4.6) |

### (b) Defined-terms audit

Defined and used consistently: **ASG**, **SLS** (Background A/B); **Companies/Company** (Background C); **Shares** (Background D); **Settlement Date** (cl 1.1); **Purchase Price** (cl 2.1); **Restrained Business** (cl 10.1(a)); **Restraint Period** (cl 10.2); **Restraint Area** (cl 10.3). Restraint Period and Restraint Area are used in clause 10.1 a few lines before their definitions in 10.2/10.3 — within the same clause, this creates no ambiguity and needs no change. Undefined terms requiring definition: **working day**, **material** (F9); **client** (F5). Acceptable without definition: "confidential information" (particularised in situ), "Purchaser's nominee".

### (c) Structural audit

Clause numbering 1–17 is continuous with consistent sub-numbering; Background lettering A–E is clean; no ProHost-style double-numbering artifacts. Two structural items require action before the draft leaves the Purchaser's side (F13), and the "DRAFT FOR LEGAL REVIEW — NOT FOR EXECUTION" banner must be removed only at execution (§A6 item 14).

---

### F10 — [RECOMMENDED] — cl 15.1 — the set-off clause contradicts cl 2.3 by reaching the settlement-day payment

**Issue.** Clause 2.3 provides that "the instalments under clauses 2.2(b) and 2.2(c) are subject to the Purchaser's right of set-off in clause 15" — deliberately excluding the $100,000 settlement payment, which must flow unconditionally for settlement to occur (clause 3.1 is conditional on it). But clause 15.1 permits withholding "against the instalments in clause 2.2" — all three. The contradiction gives the Vendor's solicitor an argument that the set-off regime is incoherent, and in the worst reading lets a pre-settlement dispute stall the settlement payment itself, collapsing the deal mechanics.

**Fix.** In clause 15.1, replace "withhold and set off against the instalments in clause 2.2" with "withhold and set off against the instalments in clauses 2.2(b) and 2.2(c)".

---

### F11 — [RECOMMENDED] — cl 3.1 / cl 2.2(a) — no simultaneous-exchange mechanic for settlement day

**Issue.** Clause 2.2(a) obliges the Purchaser to pay $100,000 on the Settlement Date; clause 3.1 obliges the Vendor to deliver "subject to receipt" of that payment, also on the Settlement Date. Each party's obligation is conditioned on or simultaneous with the other's, with no mechanism saying who moves first — the classic exchange problem. The Gwin precedent's clause 2(a) tried to solve exactly this with its botched 24-hour transfer-or-refund mechanic backed by "compensation to be decided solely by the purchasers" — a known defect this draft rightly dropped and which must **not** be reinstated. The legitimate underlying concern (the Purchaser must not part with $100,000 and then chase the documents) is solved the orthodox way: contemporaneous completion, through solicitors if either party wants it.

**Fix (insert as new clause 3.3):**

> 3.3 Payment under clause 2.2(a) and delivery under clause 3.1 shall take place contemporaneously on the Settlement Date and, if either party so requires, shall be effected through the parties' solicitors against their undertakings. Neither party is obliged to complete unless the other completes at the same time, and neither party is in default under clauses 5, 6 or 7 by reason only of withholding its own performance while the other party's contemporaneous performance remains outstanding.

---

### F12 — [RECOMMENDED] — Background E, cl 1.2 — "clauses 10 to 14" should be "clauses 10 to 13" in both places

**Issue.** Background E recites that the consideration reflects the value of "the restraints and protections given by the Vendor in clauses 10 to 14", and clause 1.2 binds a joining trustee to "clauses 10 to 14 as if named as the Vendor". Clause 14 is the *regulatory cooperation* clause. Two problems: (i) **optics in an open PSPLA/CIPU process** — a recital that part of $260,000 was paid for the Vendor's cooperation in regulatory matters is exactly the reading the regulatory-integrity constraint exists to prevent; cooperation under clause 14.1 is already supported by the mutual obligations and paid expenses, and must not look bought; (ii) **capacity** — a corporate trustee cannot meaningfully give clause 14's personal regulatory cooperation, and binding it to clause 14.2 (which concerns personal liability of the Vendor) is incoherent.

**Fix.** In Background E, replace "clauses 10 to 14" with "clauses 10 to 13". In clause 1.2, replace "is bound by clauses 10 to 14 as if named as the Vendor" with "is bound by clauses 10 to 13 (other than any obligation which by its nature can only be performed by an individual) as if named as the Vendor".

---

### F13 — [RECOMMENDED] — Drafting Notes section and bracketed execution annotations — remove before the draft leaves the Purchaser's side

**Issue.** The draft contains (i) three bracketed duplicate execution-block annotations ("[Execution block: NIKKI WAIRAU CHRISTIAN as Vendor + witness]" and equivalents for the Purchaser and Lockhart), and (ii) the "DRAFTING NOTES — FOR THE PARTIES' SOLICITORS (REMOVE BEFORE CIRCULATION)" section. The drafting notes disclose the Purchaser's negotiation-sensitive reasoning — the restraint-consideration strategy (Note 3), the security-for-instalments fallback thinking (Note 7), and the register anomaly analysis (Note 1). Sent to the Vendor — who knows the base template and will read every departure from it — the notes are a gift to her solicitor. Their substance belongs in the instruction letter to the Purchaser's own solicitors (§A5 item 9), not in the circulated draft.

**Fix (words to strike).** Before circulation to the Vendor or her advisers: delete the three bracketed "[Execution block: …]" annotation lines, and delete the entire "DRAFTING NOTES — FOR THE PARTIES' SOLICITORS (REMOVE BEFORE CIRCULATION)" section (items 1–7), first transplanting its content into the solicitor instruction letter. Retain the "DRAFT FOR LEGAL REVIEW — NOT FOR EXECUTION" banner until execution versions are prepared.

---

## D4. Enforceability Risk Under NZ Law (Pass P4)

**Method:** each legal test applied to the identified clause; findings state the risk, the likely treatment, and drafted mitigation. Authorities are context, not corpus evidence. Anything turning on unresolved facts is routed to §A5.

### D4.1 Restraint of trade — clause 10

The restraint is properly framed as a **vendor** restraint, which attracts materially greater judicial latitude than an employee restraint: goodwill is being purchased, and the buyer of goodwill is entitled to protect it (the *Nordenfelt* line, applied in NZ; and under s 83 of the Contract and Commercial Law Act 2017 the court may modify rather than void an unreasonable restraint). The draft does the three things that make vendor restraints stick: consideration is expressly anchored ("In consideration of the Purchase Price", cl 10.1, reinforced by Background E's acknowledgement that the Purchaser would not enter the agreement without the restraints); the cascade (10.2, 10.3) with clause 10.5's severance formula gives the court a ladder rather than a cliff — 4 periods × 3 areas = 12 severable combinations, and the formula wording is effective without enumerating them; and clause 10.5 recites the right reasonableness factors (the price, and the Vendor's knowledge of clients, staff, pricing and operations). Is 24 months × all of New Zealand supportable where the consideration is $260,000 and the Purchaser already co-owns and runs the business? At the top step it will be contested — the goodwill acquired is partial (a 15.25% stake, if F1 resolves as expected) — but that is exactly what the cascade is for: the Purchaser loses nothing by asking for 24 months × NZ when 12 months × Auckland is the defensible floor. One genuine vulnerability remains:

---

### F16 — [RECOMMENDED] — cl 10.5, cl 9 — the Vendor's dual status as employee invites recharacterisation of the restraint; anchor it expressly to the share sale

**Issue.** The Vendor is both selling shareholder and employee (weekly pay ~$1,923, `deal_facts.txt`). Her solicitor's best enforceability attack is recharacterisation: "this is in substance an employment restraint taken on termination, and employment restraints of 24 months × New Zealand are unenforceable." The draft's defences (Background E; "In consideration of the Purchase Price" in cl 10.1) are good but can be completed in two ways: an express capacity acknowledgement in clause 10.5, and — critically — keeping the restraint **out of the s 149 record of settlement** (F15). If the restraint is restated in the employment record of settlement, the Vendor acquires the argument that it is an employment term subject to employment-law scrutiny, and the Employment Relations Authority becomes a plausible forum.

**Fix (add to the end of clause 10.5):**

> The restraints in clauses 10 and 11 are given by the Vendor in the Vendor's capacity as vendor of the Shares and in consideration of the Purchase Price, and not in the Vendor's capacity as an employee of either Company; they are independent of, and survive the ending of, the employment and any engagement referred to in clause 9.

And (implementing note, carried into F15's wording): the record of settlement under clause 9.2 must settle employment matters only and must not restate the restraints.

### D4.2 Penalty doctrine — clauses 5, 6 and 15

Tested against the legitimate-interest/proportionality standard in *127 Hobson Street Ltd v Honey Bees Preschool Ltd* [2020] NZSC 53. **Clause 5** (12% p.a.): within the market range both precedents used (each at 12%), and it applies to "the amount in default" — sums actually due, not accelerated future instalments — so it is compensatory in structure. **Clause 6.1(a)** lets the Vendor sue for "the unpaid balance of the Purchase Price": to the extent this accelerates unmatured instalments, it is recovery of the agreed price for property already transferred — a debt claim, not a penalty — and is unobjectionable. **Clause 6.1(b)** (cancellation, re-transfer of the Shares against repayment less reasonable costs and damages) is compensatory and is the correct replacement for the Gwin precedent's clause 14.1, under which *all moneys paid were forfeited to the Vendor as liquidated damages* — a clause with obvious penalty exposure that the draft wisely dropped; confirmed nothing forfeiture-like survives anywhere in the draft. **Clause 15** (set-off of "the loss reasonably estimated by the Purchaser") is self-assessed and therefore the most attackable — but clause 15.2's true-up (repay immediately with interest from the original due date if an arbitrator disagrees) substantially de-risks it. Two hardening items: the estimate should carry a stated basis (F17), and the withholding must not itself constitute default (F23, §D6).

---

### F17 — [RECOMMENDED] — cl 15.1 — the set-off notice needs a stated basis, and the 7-day remedy window needs an irremediable-breach path

**Issue.** Two mechanical defects in the trigger. (i) The Purchaser may withhold "the amount of the loss reasonably estimated by the Purchaser" after notice "with full particulars" — but nothing requires the notice to show *how* the amount was estimated, which is the first thing an arbitrator applying clause 15.2 will ask and the easiest ground on which to paint the set-off as arbitrary (feeding the penalty argument, §D4.2). (ii) The notice must give "seven (7) days to remedy the breach (where capable of remedy)" — but the paradigm set-off trigger, a diverted client, cannot be remedied; the parenthetical implies no remedy period applies, but does not say when the withholding right then arises, leaving the sequence contestable.

**Fix (two insertions in clause 15.1).** After "seven (7) days to remedy the breach (where capable of remedy)" insert: "or, where the breach is not capable of remedy, immediately upon giving that notice". At the end of clause 15.1 add: "The notice must set out in reasonable detail the basis on which the Purchaser has estimated the loss."

### D4.3 Employment release — clause 9.2 and s 149 Employment Relations Act 2000

---

### F15 — [RECOMMENDED] — cl 9.2, cl 3.1 — the s 149 record of settlement is drafted as an intention; make it an obligation and a settlement deliverable

**Issue.** Clause 9.2 says the parties "intend" to record settlement of employment matters in a record certified under s 149 of the Employment Relations Act 2000. An intention binds no one. The legal position (correctly identified in the draft's own Drafting Note 4) is that a contractual release — including clause 3.1(e)'s no-claims acknowledgement and clause 8.2's mutual release — does **not** bar a personal grievance; only a certified record of settlement does. Failure scenario: settlement completes on the contractual documents alone; within 90 days the Vendor raises an unjustified-dismissal or disadvantage grievance; the Purchaser holds a $260,000 agreement and no employment release, and the grievance becomes leverage against the unpaid instalments. The record must be signed at or before settlement, with certification obtained as soon as an MBIE mediator is available (certification timing is not fully in the parties' control, so the *signing* is the deliverable and certification a best-endeavours obligation). Two content constraints: the record must not restate the restraints (F16), and — regulatory-integrity check — a s 149 settlement resolves employment claims only and cannot oust or touch PSPLA processes; the suggested wording stays clear of them.

**Fix (replace clause 9.2, and add a deliverable).** Replace clause 9.2 with:

> 9.2 All employment-related matters between the Vendor and each Company shall be fully and finally settled by a record of settlement signed by the Vendor and the relevant Company and certified by a mediator under section 149 of the Employment Relations Act 2000. The parties shall sign the record of settlement on or before the Settlement Date and shall each use best endeavours to obtain certification at the earliest date a Ministry of Business, Innovation and Employment mediator is available, whether before or promptly after the Settlement Date. The record of settlement shall relate to employment matters only and shall not restate or replace the restraints in clauses 10 to 13, which are given under this agreement in consideration of the Purchase Price.

And insert as new clause 3.1(i): "the record of settlement referred to in clause 9.2, signed by the Vendor;". Booking the mediator is an external step — §A5 item 5, timed against 1 August 2026.

### D4.4 Pre-emptive rights — constitutions and any shareholders' agreement

---

### F18 — [RECOMMENDED] — cl 3.1, cl 4.1(a) — pre-emption on transfer is unchecked; add a waiver deliverable (obtaining the waivers is reserved to §A5)

**Issue.** Neither constitution has been reviewed (Drafting Note 6), and any pre-emptive rights on share transfer would let the continuing shareholders — Hasibullah Nabawi (40.16%) and Lockhart (15.24%) — claim the Shares ahead of the Purchaser, or at minimum void or delay the transfers. Hasibullah is **not a party** to this agreement and cannot be bound by it; the draft can only (i) warrant the position and (ii) make waivers a deliverable. Clause 4.1(a) already warrants that "no person has any option, right of first refusal or other right to acquire any of the Shares" — which covers pre-emption as a warranty — but a warranty pays damages after the fact; a deliverable stops settlement occurring into a voidable transfer. There is also a structural wrinkle only the solicitors can resolve: if the Lockhart parcel is the Vendor's beneficial stake, its transfer may itself trigger pre-emption in favour of *both* continuing shareholders pro rata — i.e. Hasibullah could claim a share of the very parcel the Purchaser is buying. Both the constitution review and the waiver-gathering are reserved matters (§A5 items 3 and 6).

**Fix (insert as new clause 3.1(j)):**

> (j) waivers or consents, duly executed by every person entitled to them, in respect of any pre-emptive right, right of first refusal or other transfer restriction applying to the transfer of the Shares under either Company's constitution or any shareholders' agreement or, if no such rights or restrictions apply, written confirmation from each Company's board to that effect.

### D4.5 Regulatory — PSPLA / Private Security Personnel and Private Investigators Act 2010

The draft's regulatory architecture is confirmed sound as designed: clause 14.1 (cooperation at the Purchaser's request, expenses met) is compellable and fair; clause 14.2 implements the deliberate no-transfer/no-release design from `deal_facts.txt`; clause 12.2 expressly contemplates disclosure to the PSPLA; clause 8.2(c) carves regulatory liability out of the release; and clause 17.1(c)'s injunction carve-out deliberately excludes clause 14. The three leaks against that design are consolidated in F2 (BLOCKER, §D2). One addition:

---

### F20 — [RECOMMENDED] — cl 14 — add a mutual covenant to make post-settlement notifications to the PSPLA and Companies Office promptly and accurately

**Issue.** Settlement changes the shareholding and (via clause 3.1(d)) potentially the officers of two licensed security businesses. Whether the PSPLA requires notification of the change is a legal question reserved to the regulatory lawyer (§A5 item 7; Drafting Note 5), but the *contractual* gap is drafting: nothing obliges either party to make whatever notifications are required, promptly and accurately. In an open PSPLA/CIPU process, a late or inaccurate licence-record update — however innocent — reads as concealment. A mutual covenant closes the gap regardless of what the regulatory advice concludes, and affirmatively evidences the parties' no-concealment posture.

**Fix (insert as new clause 14.3; F2's carve-out then becomes 14.4):**

> 14.3 Each party shall promptly make, and shall cooperate with the other in making, every notification, update or filing to the Private Security Personnel Licensing Authority, the Companies Office or any other regulator that is required as a result of the change in shareholding or officers of either Company effected by this agreement, and shall ensure that nothing in any such notification misstates or omits any material fact.

### D4.6 Cancellation and survival

---

### F14 — [BLOCKER] — whole agreement (insert in cl 16) — no survival clause: cancellation after a dispute could discharge the restraints and confidentiality obligations the price was paid for

**Issue.** Under the Contract and Commercial Law Act 2017 cancellation regime, cancellation discharges the parties from unperformed future obligations. The draft has express cancellation rights in clauses 6.1(b) and 7.1(b) and no survival clause anywhere. Failure scenarios: (i) the Purchaser pays $100,000 and takes the Shares; a dispute erupts; the Vendor cancels under clause 6.1(b) for an alleged payment default — on cancellation the restraints (cl 10–11), confidentiality (cl 12) and non-disparagement (cl 13) are all arguably discharged prospectively, while the dispute over re-transfer and repayment grinds on with the Vendor free to compete; (ii) the Purchaser cancels under clause 7 for Vendor default — same result: the Vendor's own cancellation-triggering breach frees her from the restraints. Background E records that the Purchaser "would not enter into this agreement without" clauses 10–13; a structure in which those clauses evaporate on cancellation would backfire precisely when they matter most. One nuance must be preserved: if cancellation under clause 6.1(b) actually results in the Shares going back to the Vendor, restraining her from the business she has re-acquired would be wrong — the survival clause must except that completed re-transfer case for clauses 10 and 11 (but not for clauses 12 and 13, which should hold in every case).

**Fix (insert as new clause 16.5):**

> 16.5 Clauses 4, 5, 8, 12, 13, 14, 15.2, 16 and 17 survive settlement and any cancellation of this agreement. Clauses 10 and 11 survive settlement and any cancellation of this agreement, except that if this agreement is cancelled under clause 6.1(b) and the Shares are re-transferred to the Vendor, clauses 10 and 11 cease to apply from the date the re-transfer is registered. Cancellation does not affect any right or obligation which has accrued before cancellation.

### D4.7 Trustee capacity — clause 1.2 and Lockhart

---

### F19 — [RECOMMENDED] — cl 1.2 — the trustee joinder needs covenantor-style mechanics: a defined instrument, a title warranty, and obligations a company can actually perform

**Issue.** Clause 1.2 obliges the Vendor to "procure that the registered holder joins this agreement as a party" — but specifies no instrument, no scope of joinder, and no warranty from the trustee about its own parcel. As drafted, the trustee would be "bound by clauses 10 to 14 as if named as the Vendor", which a company cannot sensibly perform in full (it cannot "work" in a role, and clause 14's personal regulatory cooperation is an individual's obligation — partially addressed by F12). Meanwhile the warranties that matter most for the trustee parcel — title and authority, clause 4.1(a)–(b) — are given only by the Vendor, so the Purchaser has no direct claim against the registered holder of 15.24% of each company if the trust's authorisations prove defective. The corpus contains the model: ProHost clause 19.18 joined Jamin Tahere as **covenantor** "in relation to the provisions contained in Clauses 8, 9, 10 and 12" with his own execution block — a scoped joinder, which is what clause 1.2 should require. Trust-deed review and any limited-recourse wording the trustee requests are legal-advice matters reserved to §A5 item 3.

**Fix (add to the end of clause 1.2):**

> The joinder shall be effected by the registered holder executing this agreement, or a deed of covenant in a form reasonably required by the Purchaser, under which the registered holder: (a) agrees to sell and transfer its Shares in accordance with this agreement and to perform clause 3 in respect of them; (b) warrants the matters in clauses 4.1(a) and 4.1(b) in respect of its Shares; and (c) covenants to comply with clauses 10 to 13 to the extent they are capable of applying to a body corporate.

---

## D5. Precedent Delta (Pass P5)

**Method:** three-way clause mapping — every operative concept in either precedent, its treatment in the draft, and a disposition: KEPT / MODIFIED / DROPPED (restore?) / DROPPED (wisely). Every DROPPED row is classified with reasons; restorations become findings.

### D5.1 ProHost 2023 (Franklin Law) → Draft

| ProHost concept (clause) | Draft treatment | Disposition and assessment |
|---|---|---|
| Deposit + conditional structure (cl 2(a); cl 7 client-consent condition naming Star Hospitality, Lime Investments, Florrie McGreals, Bar101) | Absent | **DROPPED — wisely.** ProHost was an arm's-length entry into a business the purchasers didn't control; client consent and a deposit protected them. Here the Purchaser already co-owns and runs both Companies — client-consent conditions would advertise the buyout to clients prematurely (contrary to cl 13.2's controlled-communications design) and a deposit is meaningless when the first payment is the settlement payment. |
| Contingent instalment tied to contract renewal (cl 2(d): $30,000 payable only if the Star Hospitality agreement renewed) | Absent | **DROPPED — correctly, but its logic is instructive.** The price-protection-against-client-loss concept survives in better form as the set-off (cl 15) against restraint breach. No client-contingent instalment was agreed in `deal_facts.txt`, so none is drafted. Feeds §D6 scenario analysis. |
| Directors' resolutions deliverable (cl 3.2) | cl 3.1(b) | **KEPT — equivalent.** Same board-approval and register-entry mechanics. |
| Shareholders' resolutions appointing purchaser's nominee directors (cl 3.3) | Absent | **DROPPED — acceptable.** The Purchaser and Hasibullah already control the boards; no new appointments are needed for control. No finding. |
| Director resignations + no-claims acknowledgement (cl 3.5) | cl 3.1(d)+(e) | **KEPT — strengthened.** The draft's acknowledgement adds "current account" and "dividend" to ProHost's fees/salary/expenses/compensation list — important here because a shareholder-employee's current account is the likeliest residual claim. |
| Xero/accounting records: vendor retains account, purchaser starts fresh, audit access warranted (cl 4; cl 9 tail) | Absent; cl 3.1(f) covers logins | **DROPPED — correctly, because the situation is reversed.** In ProHost the *vendor* kept the accounts and the purchaser needed access. Here the *Companies* keep their accounts and the exiting Vendor's access must END — which cl 3.1(f) (logins and administrative rights) achieves, completed by F7's bank/software signatory-removal deliverable. Nothing to restore. |
| Invoice apportionment on trust pre/post settlement (cl 5); expense apportionment + Holidays Act payout (cl 6) | Absent; cl 3.2 and cl 9.1 instead | **DROPPED — wisely.** Those clauses fit a business handover where the vendor owned the whole trading operation. In a share sale where the Companies keep trading and a 15.25% holder exits, revenue and expenses stay inside the Companies; the correct simpler machinery is exactly what the draft has — cl 3.2 (no post-settlement dividends/drawings) and cl 3.1(e) (current-account acknowledgement). ProHost cl 6's Holidays Act payout obligation survives in correct form as cl 9.1 (final pay including Holidays Act 2003 entitlements). |
| Advisory/transition services, unpaid, 80-hour cap, chaperone requirement (cl 8–10) | Absent | **DROPPED — deliberate clean exit.** See F22 (OPTIONAL) for the minimal alternative. Do not import remuneration mechanics without instruction. |
| Purchaser reverse non-solicit (cl 13: purchasers restrained for 2 years from diverting clients) | Absent | **DROPPED — wisely.** A reverse restraint on the Purchaser made sense when the ProHost vendor was staying in the industry's orbit; here it would restrain the Purchaser from his own clients. Confirmed no residue anywhere in the draft — the only mutual obligations are cl 13.1 (non-disparagement) and cl 12.2 (terms confidentiality), both appropriate. |
| Guarantee release + indemnity (cl 14) | cl 8.1 | **KEPT — modified in the Purchaser's favour.** The draft adds a carve-out: the Purchaser's indemnity does not cover liability arising from "the Vendor's own act, omission or default prior to the Settlement Date". The carve-out is broad — arguably most of what a hands-on manager did pre-settlement is her "act" — and the Vendor's solicitor will push back, likely seeking to narrow it to breach/fault-based liability. From the Purchaser's side the wording is favourable and should be held as the opening position; concede narrowing (e.g. "act, omission or default *constituting a breach of the Vendor's duties*") only if pressed. No drafting change recommended. |
| Undertaking to sign all documents / exercise voting rights (cl 15.14) | cl 16.1 | **KEPT — equivalent.** |
| 12% default interest (cl 11); purchaser-default remedies (cl 16.15); vendor-default remedies (cl 17.16); dispute resolution (cl 18.17) | cl 5, 6, 7, 17 | **KEPT — improved.** The draft's cl 6 adds a written-notice precondition to the Vendor's default remedies (ProHost required only 14 days' continuing default, no notice) — a purchaser-favourable improvement since the Purchaser is the paying party. Cl 6 also **drops ProHost cl 16.1's forfeiture remedy** ("all moneys paid… forfeited to the Vendor as liquidated damages") in favour of compensatory cancellation — see §D4.2. The inverted "receipt by the Purchaser" defect in ProHost cl 3 and its mis-cited "clause 2.1" reference are both corrected in draft cl 3.1. |
| Covenantor joinder (cl 19.18: Jamin Tahere joins "in relation to… Clauses 8, 9, 10 and 12" with own execution block) | cl 1.2 + conditional Lockhart block | **Model adopted, mechanics incomplete** → F19 hardens cl 1.2 to the ProHost covenantor standard. |
| Numbering artifacts (15.14/16.15/17.16/18.17/19.18 double numbering) | Clean 1–17 | **Not inherited** — confirmed §D3(c). |

### D5.2 Gwin 2025 → Draft

| Gwin concept (clause) | Draft treatment | Disposition and assessment |
|---|---|---|
| Cl 2(a): 24-hour transfer-or-refund + "any type of compensation to be decided solely by the purchasers" | Absent | **KNOWN DEFECT — DROPPED — wisely; do not reinstate.** Uncertain trigger, no mechanism, and a sole-discretion compensation right that is unenforceable for uncertainty and reads as a penalty. The *legitimate* concern underneath it — payment/transfer simultaneity — is addressed properly by F11's contemporaneous-completion clause. |
| Cl 14.1: cancellation with forfeiture of **all** moneys paid as liquidated damages | Absent; cl 6.1(b) compensatory instead | **KNOWN DEFECT — DROPPED — wisely; do not reinstate.** Forfeiting up to $180,000 of instalments on a late final payment would fail the *Honey Bees* proportionality test outright. Confirmed the draft's cl 6 replacement is compensatory (§D4.2) and nothing forfeiture-like survives. |
| Cl 3.4: release of social media accounts, company property, intellectual property | cl 3.1(f) | **KEPT — improved, one term to restore** → F21 (Gwin names "intellectual property" expressly; the draft's list should too, plus domain/registrar accounts). |
| Cl 4: vehicle QEF939 (fines, finance, transfer out of company) | Absent | **N/A — deal-specific to Gwin.** But it proves vehicles are live issues in this group; F7's cl 3.1(f) wording adds "vehicles, equipment and other physical property" so the question is answered structurally. Whether this Vendor actually holds any company vehicle or chattels is a factual check — §A6 item 13. |
| Cl 5–6: invoice/expense apportionment | Absent | **DROPPED — wisely**, same reasoning as ProHost cl 5–6 above. |
| Cl 7–8 + Appendix 1: paid advisory agreement ($1,500/wk + GST, 3 months, defined availability) | Absent | **DROPPED — deliberate clean exit.** Context note: the Gwin advisory named Nikki Christian as part of the management team receiving the handover — she already holds the operational knowledge, which cuts against needing her transitional services and *for* the pre-settlement conduct protections in F24. See F22 for the minimal unpaid alternative. |
| Cl 10: restraint — 2-year client-diversion only, binding "the Vendor and Spouse" | cl 10–11 | **MODIFIED — substantially strengthened.** The draft adds the sector restraint, servicing restraint, staff non-solicit, non-interference, cascade and severance. On the Gwin "Spouse" concept: Gwin purported to bind a spouse who never signed — defective. The draft needs no spouse joinder absent specific facts; cl 10.1's "directly or indirectly, whether on the Vendor's own account or as an employee, contractor, consultant, director, shareholder, partner, agent, financier or adviser of any other person or entity" already catches the Vendor operating through a partner or associated entity. If specific facts emerge (e.g. a partner active in the industry), a scoped covenantor joinder on the ProHost cl 19.18 model is the correct instrument — noted for §A5, no drafting now. |
| Cl 11: guarantee release with pre-settlement debt carve-out | cl 8.1 | **KEPT — comparable.** Gwin excepted "any debt or liability in anyway occurred before the settlement date"; the draft's carve-out ("the Vendor's own act, omission or default prior to the Settlement Date") is tighter-drafted and more defensible. |
| Cl 9 (12% interest), cl 14/15 (14-day windows), cl 16 (negotiation→arbitration, Arbitration Act 1996, single arbitrator, NZLS appointment) | cl 5, 6, 7, 17 | **KEPT** — confirmed in the §D1 diff (rows 19–22). |

### D5.3 What the draft added that neither precedent has — with the one-line justification the Vendor's solicitor will ask for

The Vendor bought Pro Host under this template in 2023; every addition is negotiation-visible to her. The Purchaser's solicitor should hold these justifications (this table feeds the instruction letter, §A5 item 9):

| Addition | One-line justification |
|---|---|
| Background E (restraints as substantial consideration) | Standard vendor-restraint anchor; protects enforceability of the very clauses the price was paid for (§D4.1). |
| Cl 4 warranties | The precedents had none; deferred consideration and a two-company sale need title, authority and conduct warranties. |
| Cl 8.2 mutual release | Clean-break protection for both sides — the Vendor benefits equally. |
| Cl 9 employment end + s 149 record | The Vendor is an employee; both parties need a grievance-proof exit (her certainty as much as his). |
| Cl 10 sector restraint + cascade | The Purchaser's stated requirement; cascading structure is the enforceable way to draft what both parties already agreed commercially. |
| Cl 11 expanded non-solicit (staff, interference) | Protects what the price was paid for; mirrors what any buyer's solicitor adds in a people-business sale. |
| Cl 12 confidentiality | She holds client lists, pricing and rosters; unlimited-in-time confidentiality is standard in a business sale. |
| Cl 13 non-disparagement + agreed communications | Mutual — protects her exit narrative as much as the Companies' client base. |
| Cl 14 regulatory cooperation / no-release | Deliberate joint protection: preserves both parties' personal regulatory responsibility in the open PSPLA/CIPU process; conceals nothing. |
| Cl 15 set-off | The counterpart of the Purchaser paying 62% of the price after losing the shares' leverage; cl 15.2's true-up with interest makes it fair. |
| Cl 16 boilerplate (entire agreement, severance, counterparts, notices) | Absent from both precedents; standard machinery the settling solicitors would add anyway. |
| Cl 17.1(c) injunction carve-out | Restraints are only worth what an urgent injunction can protect; arbitration-only enforcement is too slow for a client walking out the door. |

---

## D6. Protection of the Purchaser — Deferred Consideration and the Vendor's Inside Knowledge (Pass P6)

**Method:** adversarial walk-through of three scenarios, testing whether the draft's remedies actually function in each — the draft read as the Vendor's solicitor would attack it.

### Scenario 1 — Vendor breaches a restraint early (before 1 October 2026)

The set-off (cl 15) is live against up to $160,000 of unpaid instalments — the Purchaser's strongest position. Walking the sequence exposed three defects: the 7-day remedy window has no stated path for irremediable breaches like a diverted client, and the loss estimate needs a stated basis (both fixed by F17); the set-off reaches the wrong instalments as drafted (fixed by F10); and — the most dangerous discovery of this review — exercising the set-off could hand the Vendor a cancellation right:

---

### F23 — [BLOCKER] — cl 15 ↔ cl 6 — a good-faith set-off can be characterised as a payment default, giving the Vendor a path to cancel and demand the Shares back before arbitration resolves anything

**Issue.** Clause 15.1 lets the Purchaser withhold an instalment; clause 15.2 provides the true-up if an arbitrator later disagrees. But nothing says the withheld amount is not "due" in the meantime. Sequence: (1) 15 September 2026 — the Purchaser learns the Vendor has diverted a client, serves a clause 15.1 notice and withholds the 1 October instalment; (2) the Vendor disputes the breach and serves a clause 6.1 notice asserting payment default; (3) fourteen days later — long before any arbitrator is even appointed under clause 17.1(c)'s escalation timeline — the Vendor purports to cancel under clause 6.1(b), demands re-transfer of the Shares, and clause 5 interest allegedly runs against the Purchaser throughout. The Purchaser's protection mechanism becomes the Vendor's cancellation trigger. Clause 15.2's "immediately, together with interest" language even lends her argument colour: it implies the amount was due all along. Nothing in clause 6 is subordinated to clause 15 or to the clause 17 dispute process, so the self-help remedies collide head-on. In a deal where the Vendor knows the template and the pressure points, this is the single most exploitable defect in the document.

**Fix (insert as new clause 15.3):**

> 15.3 If the Purchaser withholds an amount in accordance with clause 15.1, that amount is not due, and the Purchaser is not in default, for the purposes of clauses 5 and 6 unless and until: (a) an arbitrator appointed under clause 17 (or a court) determines that the amount, or part of it, was not properly set off; and (b) the Purchaser fails to pay the amount so determined, together with interest under clause 15.2, within five (5) working days after that determination. The Vendor may not give a notice under clause 6.1, and may not cancel this agreement, in respect of an amount withheld in accordance with clause 15.1 except following a failure to pay under paragraph (b).

### Scenario 2 — Vendor breaches a restraint late (after 1 October 2026)

All instalments are paid; the set-off is dead; the restraint tail runs to 1 August 2028 (at the top of the cascade) backed only by damages and injunction. Findings of the walk-through: **(i)** this exposure is inherent in the agreed payment structure — a longer instalment tail was not the deal `deal_facts.txt` records, so the report flags the risk rather than redrafting the commercial terms: after 1 October 2026, 100% of the price is paid and roughly 22 months of restraint protection depends on enforcement, against a counterparty with deep client relationships. **(ii)** The injunction route — the fast remedy that matters for a client walking out the door — is properly drafted: clause 17.1(c)'s carve-out covers "clauses 10 to 13" by number, so interim relief is available for the restraint, non-solicit, confidentiality and non-disparagement clauses without waiting out the 14-day negotiation period. F14's survival clause ensures those clauses still exist to enforce if the relationship has already collapsed into cancellation claims. F5's client definition and F17's notice mechanics make the damages claim provable rather than arguable. **(iii)** A liquidated-damages formula (e.g. a fixed sum per diverted client referenced to trailing-12-month revenue) was considered and is **not** recommended for unilateral insertion: without financial data in the corpus to calibrate it, a mis-set figure invites the *Honey Bees* penalty attack (§D4.2) and gives the Vendor a ceiling on her exposure. If wanted, it is a calibration exercise for the solicitors with the accountant's revenue data — §A5 item 8.

### Scenario 3 — Vendor uses inside knowledge between signing and settlement

The gap: the Vendor works in the business today with full access to clients, rosters and pricing, and will hold that access until 1 August 2026. Clause 4.1(c) restrains binding the Companies and moving assets, but says nothing about client or staff contact, and nothing warrants that diversion has not already begun pre-signing. She has also seen this template as a purchaser — she knows the restraints bite only from the Settlement Date.

---

### F24 — [RECOMMENDED] — cl 4 — add a signing-to-settlement conduct covenant, a no-prior-diversion warranty, and a settlement-day certification of deletion

**Issue.** Concrete failure scenario: between signing and 1 August 2026 the Vendor quietly tells key clients and guards she is leaving and where she will be, and exports the client contact list and pricing schedules — all before any restraint operates. At settlement she hands over "all… client information" under clause 3.1(f) while retaining copies, and the restraint war starts with the Purchaser unable to prove what was taken or when. The three protections that close this: a conduct covenant for the pre-settlement window, a warranty that diversion and copying have not already occurred (converting suspicion into a clean set-off trigger under clause 15.1's reference to amounts due under clause 4), and a certification at settlement that copies are deleted (making retention a documented, litigable act rather than a shrug).

**Fix (insert as new clauses 4.3 and 4.4):**

> 4.3 From the date of this agreement until the Settlement Date, the Vendor shall not, except with the Purchaser's prior written consent or in a form agreed under clause 13.2: (a) discuss the sale, or the future ownership or management of either Company, with any client, supplier or staff member of either Company; (b) copy, download, transmit or remove any client list or contact information, contract, pricing information, roster, or other record of either Company, other than as strictly required to perform the Vendor's current duties; or (c) alter, delete, or change the access rights to, any account, system or record referred to in clause 3.1(f).
>
> 4.4 The Vendor warrants that as at the date of this agreement the Vendor has not: (a) solicited, diverted or encouraged away, or attempted to solicit, divert or encourage away, any client or staff member of either Company; or (b) copied, downloaded, transmitted or removed any record of the kind described in clause 4.3(b), except as required to perform the Vendor's duties. On the Settlement Date the Vendor shall certify in writing that the Vendor has returned or permanently deleted all copies of all records of the kind described in clause 4.3(b) in the Vendor's possession or control, other than records delivered under clause 3.1.

### Cross-cutting checks

**Enforcement-path trace.** Each protection was traced through notice → remedy window → set-off or arbitration → interim injunction: **cl 10 (restraint)** — notice under 16.3 (F8 completes it) → 7-day/immediate window (F17) → set-off (cl 15, firewalled by F23) or arbitration (cl 17) → interim injunction (17.1(c) ✔). **cl 11 (non-solicit)** — same path ✔ (within 17.1(c)'s "10 to 13"). **cl 12 (confidentiality)** — same path ✔; unlimited duration confirmed; survives cancellation once F14 is inserted. **cl 13 (non-disparagement)** — same path ✔; F2's carve-out prevents regulatory misuse. The only dead ends found were the notice-address vacuum (F8) and the cl 6 collision (F23), both now closed.

**The Vendor knows the template.** Every departure from the 2023 ProHost document she signed is catalogued with its justification at §D5.3 — the Purchaser's solicitor should expect her to probe the set-off (cl 15) and the sector restraint (cl 10) hardest, because those are the two provisions with no counterpart in anything she has signed before, and both are the provisions this review has hardened most.

**Security for the deferred instalments (Drafting Note 7) — negotiation posture only, no drafting.** If the Vendor's solicitor asks for security for the $160,000 tail: **resist a personal guarantee** (it outlives the set-off and undermines the whole deferred structure); resist any charge over the Shares (it recreates the leverage the buyout removes). If pressure must be met, the least-bad concession is a solicitor-held escrow of the final $80,000 instalment released on 1 October 2026 absent a clause 15.1 notice — it gives her payment certainty while preserving the set-off in full. Concede nothing on the first two instalments; the settlement payment is already unconditional and the 1 September instalment is only 31 days deferred.

**Regulatory-integrity backstop (mandatory check).** Every suggested wording in F1–F25 has been re-read against the constraint that nothing may conceal, transfer, or release personal regulatory liability or fetter the Vendor's dealings with the PSPLA/CIPU. Confirmations: F2's carve-out affirmatively protects regulator communications, including against set-off; F20 mandates accurate notifications; F15's record of settlement covers employment matters only; F16's restraint anchor does not touch regulatory conduct; F24's conduct covenant restrains client/staff/records conduct only and is subject to F2's clause 14.4 override ("Nothing in this agreement (including clauses 10 to 13)…" — clause 4.3 should be understood, and if the solicitors prefer, expressly stated, as equally subject to it; adding "(including clauses 4.3, 4.4 and 10 to 13)" to F2's wording is a one-word-cost improvement the settling solicitors may make). No finding in this report purchases silence, restrains a complaint, or touches the Vendor's licence status.

### Findings arising from the precedent delta (§D5)

---

### F21 — [OPTIONAL] — cl 3.1(f) — name intellectual property and domain/registrar accounts expressly

**Issue.** Gwin clause 3.4 expressly required release of "any intellectual property of the company"; the draft's clause 3.1(f), though otherwise a superset, does not use the words, and does not reach domain-name registrar or website-hosting accounts — the one category of "login" most often registered in a founder's personal name. In a share sale the Companies' IP stays with the Companies regardless, so this is belt-and-braces about *possession and control*, not title.

**Fix.** In clause 3.1(f) (as replaced by F7), after "banking and social media accounts of the Companies" insert: ", domain name registrar, website and hosting accounts, and any records of intellectual property of either Company".

---

### F22 — [OPTIONAL] — cl 9 — a minimal, unpaid, remote handover obligation, if the Purchaser wants one

**Issue.** Both precedents contained transition-services machinery (ProHost cl 8–10: unpaid, 80-hour cap, chaperoned; Gwin cl 7–8 and Appendix 1: paid at $1,500/week). The draft has none — a deliberate clean exit, which this review supports given the relationship context and the fact that the operational knowledge largely already sits with the Purchaser's side (the Gwin advisory named this Vendor among the management team receiving Shannon Gwin's handover in 2025). The residual risk is narrow: passwords, supplier quirks, roster details that surface in the weeks after 1 August 2026. If the Purchaser wants cover, the clause below is the maximum this review recommends — unpaid, questions-only, no site attendance, no imported remuneration mechanics.

**Fix (only if instructed; insert as new clause 9.3):**

> 9.3 For ten (10) working days after the Settlement Date, the Vendor shall, at the Purchaser's reasonable request and without further payment, answer questions and provide information reasonably necessary to transfer the Vendor's operational knowledge of the Companies (including in relation to rosters, client contacts, supplier arrangements and systems access). This clause does not require the Vendor to attend any workplace or perform any services.

---

## A4.7 Consolidated Findings List (severity order)

Full issue analysis and exact wording for each finding appears in §D1–§D6 above at the section noted.

| # | Severity | Clause(s) | Issue (one line) | Section |
|---|---|---|---|---|
| F1 | **BLOCKER** | Background D, cl 1.2, cl 2.1, execution | Share numbers unresolved; register (Vendor 1 share; Lockhart 1,524) contradicts $260,000 price unless trustee joined — factual gate before signing | D1 |
| F2 | **BLOCKER** | cl 11.1(c), 12.1(a), 13.1 | Three clauses readable as restraining regulator communications during open PSPLA/CIPU — strike "or regulators", widen cl 12.1(a), add regulator-communications carve-out (new cl 14.4) | D2 |
| F14 | **BLOCKER** | cl 16 (new 16.5) | No survival clause — cancellation could discharge restraints/confidentiality the price was paid for; add survival with re-transfer exception | D4.6 |
| F23 | **BLOCKER** | cl 15 ↔ cl 6 (new 15.3) | Good-faith set-off can be cast as payment default → Vendor cancellation path; firewall withheld amounts from cl 5/6 until arbitral determination | D6 |
| F3 | RECOMMENDED | cl 10.4(b) | Carve-out circular with 10.1(a); permits in-house security roles and admin roles at competitors — redefine by role activities | D2 |
| F4 | RECOMMENDED | cl 10.1(a) | Restrained Business list misses close protection, monitoring, cash-in-transit, concierge, labour-hire supply, training | D2 |
| F5 | RECOMMENDED | cl 10.1(b), 11.1(a) | "Client" undefined; cl 11.1(a) has no lookback — add 24-month definition capturing venue/head-contract relationships | D2 |
| F6 | RECOMMENDED | cl 11 (new 11.3) | Non-solicit has no cascade or reasonableness acknowledgement — all-or-nothing at 24 months | D2 |
| F7 | RECOMMENDED | cl 3.1(f)–(h) | Deliverables gaps: share certificates, bank/payroll signatory forms, MFA transfer, vehicles and physical property | D2 |
| F8 | RECOMMENDED | cl 16.3 | Notices: no addresses stated, no deemed-receipt rules — every remedy window runs from notice | D2 |
| F9 | RECOMMENDED | new cl 1.3 | Define "working day" and "material" (breach) — the set-off trigger currently turns on an undefined term | D2 |
| F10 | RECOMMENDED | cl 15.1 | Set-off says "instalments in clause 2.2", contradicting cl 2.3's limit to 2.2(b) and (c) | D3 |
| F11 | RECOMMENDED | cl 3 (new 3.3) | No simultaneous-exchange mechanic for the $100,000/documents swap (solve properly — not via Gwin's defective cl 2(a)) | D3 |
| F12 | RECOMMENDED | Background E, cl 1.2 | "Clauses 10 to 14" → "10 to 13": consideration must not appear to buy regulatory cooperation; trustee cannot perform cl 14 | D3 |
| F13 | RECOMMENDED | Drafting notes, annotations | Remove drafting notes and bracketed execution annotations before circulation — negotiation-sensitive reasoning exposed | D3 |
| F15 | RECOMMENDED | cl 9.2, cl 3.1(i) | s 149 record is a mere intention; make signing a settlement deliverable, certification best-endeavours, employment-only content | D4.3 |
| F16 | RECOMMENDED | cl 10.5 | Anchor restraints to vendor capacity against employment-restraint recharacterisation; keep restraints out of the s 149 record | D4.1 |
| F17 | RECOMMENDED | cl 15.1 | Set-off notice needs a stated estimation basis and an immediate path for irremediable breaches | D4.2 |
| F18 | RECOMMENDED | cl 3.1(j) | Pre-emption unchecked; add waiver/confirmation deliverable (constitutions and waiver-gathering reserved to §A5) | D4.4 |
| F19 | RECOMMENDED | cl 1.2 | Trustee joinder lacks instrument, scope and title warranty — adopt ProHost cl 19.18 covenantor mechanics | D4.7 |
| F20 | RECOMMENDED | cl 14 (new 14.3) | Add mutual covenant for prompt, accurate PSPLA/Companies Office notifications on change of shareholding/officers | D4.5 |
| F24 | RECOMMENDED | cl 4 (new 4.3, 4.4) | Signing-to-settlement conduct covenant, no-prior-diversion warranty, settlement-day deletion certification | D6 |
| F21 | OPTIONAL | cl 3.1(f) | Name IP and domain/registrar/hosting accounts expressly (Gwin cl 3.4 parity) | D5 |
| F22 | OPTIONAL | cl 9 (new 9.3) | Minimal unpaid remote handover obligation, only if instructed | D5 |
| F25 | OPTIONAL | cl 11.1(b) | 12-month staff vs 24-month client lookback asymmetry — defensible; record as intentional (no change recommended) | D2 |

**Renumbering note for the settling solicitors.** Applying all findings produces: new cl 1.3 (F9); new cl 3.1(g)–(j) (F7, F15, F18) and cl 3.3 (F11); new cl 4.3–4.4 (F24); revised cl 9.2 and optional 9.3 (F15, F22); revised cl 10.1, 10.4(b), 10.5 (F4, F3, F16); new cl 11.2–11.3 with the existing clause body as 11.1 (F5, F6); revised cl 12.1(a) (F2); new cl 14.3–14.4 (F20, F2); revised cl 15.1 and new 15.3 (F10, F17, F23); new cl 16.5 (F14); revised cl 16.3 (F8); revised Background E and cl 1.2 (F12, F19). Cross-references to check after renumbering: cl 2.3 → 15; cl 3.1(e) → 9; cl 12.1(a) → 14.4; cl 15.3 → 17; cl 16.5's clause list.

---

# A5. Matters Reserved to the Instructing Solicitors

These require legal advice, external searches or third parties — not drafting — and are deliberately **not** presented as findings:

1. **The Lockhart question (with F1).** Confirm from the trust records whether the 1,524-share parcels are held for the Vendor; review the trust deed for the trustee's power of sale and any limited-recourse wording the trustee will require; advise on the joinder instrument (F19 provides the contractual mechanics).
2. **Structure check on the trustee transfer.** If the Lockhart parcel transfers, advise whether that transfer itself triggers pre-emptive rights in favour of *both* continuing shareholders pro rata — i.e. whether Hasibullah Nabawi could claim part of the parcel the Purchaser is buying.
3. **Constitutions and any shareholders' agreement.** Obtain and review both Companies' constitutions (and any shareholders' agreement) for pre-emption and transfer restrictions; obtain executed waivers from Hasibullah Nabawi (40.16%) and Lockhart (15.24%) if required — neither is a party and neither can be bound by drafting (F18 adds the deliverable that stops settlement without them).
4. **Tax apportionment.** Accountant to confirm the clause 2.1 ASG/SLS price split (Drafting Note 2) — relevant to each party's tax position; report does not advise on tax.
5. **MBIE mediator.** Book certification of the s 149 record of settlement against the 1 August 2026 settlement date (F15's wording tolerates certification promptly after settlement if a mediator is unavailable before).
6. **PSPLA notification advice.** Regulatory lawyer to confirm what the change of shareholding/officers of two licensed security businesses requires by way of PSPLA notification or licence-record updates (F20's covenant obliges the parties to do whatever is advised, promptly and accurately).
7. **Regulatory-integrity read-through.** Have the regulatory lawyer confirm the final document against the open PSPLA → CIPU process — specifically that clauses 12–14 as amended by F2 and F20 cannot be portrayed as managing regulatory communications.
8. **Liquidated damages (optional).** If the Purchaser wants a per-client liquidated-damages formula for restraint breach, calibrate it from actual client revenue data with the accountant, and test it against *Honey Bees* proportionality before inclusion (§D6 scenario 2 explains why this review does not draft it blind).
9. **Instruction letter.** Transplant the draft's Drafting Notes 1–7 (removed under F13) and the §D5.3 additions-justification table into the letter of instruction, including the negotiation posture on vendor security (resist guarantee and share charge; escrow of the final $80,000 as the fallback concession — §D6).
10. **Execution formalities.** Witnessing arrangements for all signatories; if Lockhart joins, confirm its signing authority (two directors / director + authorised signatory per its constitution).

---

# A6. Schedule of Placeholders and Unresolved Facts (Pass P7)

Every `[●]`, blank and open question that must be completed before signing (**S**) or before settlement (**C**):

| # | Item | Draft location | Owner | Deadline |
|---|---|---|---|---|
| 1 | Agreement date — "AGREEMENT dated [        ] 2026" | Front page | Both parties | S |
| 2 | `[●]` ordinary shares in ASG; `[●]` ordinary shares in SLS | Background D | Purchaser + register search (with item 4) | S — gates F1 |
| 3 | `$[●]` / `$[●]` price apportionment between ASG and SLS shares | cl 2.1 | Accountant (§A5.4) | S |
| 4 | **The Lockhart question**: is the trustee's 1,524-share parcel (each company) the Vendor's beneficial stake? If yes — join trustee, complete Background D at 1,525 per company, activate its execution block, review trust deed. If no — do not sign; subject matter and price inconsistent (F1) | Drafting Note 1; deal_facts "UNRESOLVED" | Vendor to evidence; Purchaser's solicitor to verify (§A5.1) | S — **BLOCKER until resolved** |
| 5 | Conditional execution block "[LOCKHART TRUSTEE SERVICES NO.222 LIMITED — if joined under clause 1.2]" — activate or delete | Execution section | Purchaser's solicitor | S |
| 6 | Three bracketed "[Execution block: …]" duplicate annotations — delete (F13) | Execution section | Purchaser | S — before circulation |
| 7 | "DRAFTING NOTES — REMOVE BEFORE CIRCULATION" section — delete after transplanting to instruction letter (F13, §A5.9) | End of draft | Purchaser | S — before circulation |
| 8 | Vendor's nominated bank account (cl 2.2 requires nomination ≥ 2 working days before each payment; none stated) | cl 2.2 | Vendor | C — first nomination by 30 July 2026 |
| 9 | 1,690 issued shares (Gwin 2025 recital) vs 10,000 (deal_facts 2026) — confirm current register extract; establishes no share-count error carries into Background A/B | Background A/B | Purchaser's solicitor (register search) | S |
| 10 | Notice addresses and emails for both parties (F8 wording contains `[●]` fields) | cl 16.3 | Both parties | S |
| 11 | Constitutions / shareholders' agreement obtained and checked; pre-emption waivers from Hasibullah Nabawi and Lockhart executed if required (F18, §A5.3) | cl 3.1(j) | Purchaser's solicitor | S (review) / C (waivers) |
| 12 | MBIE mediator booked for s 149 certification (F15, §A5.5) | cl 9.2 | Both parties | C — timed against 1 Aug 2026 |
| 13 | Factual check: any company vehicles, equipment or chattels in the Vendor's possession (Gwin cl 4 shows vehicles are live issues in this group; F7's cl 3.1(f) covers them if so) | cl 3.1(f) | Purchaser | S |
| 14 | "DRAFT FOR LEGAL REVIEW — NOT FOR EXECUTION" banner — remove only when execution versions are prepared | Front page | Purchaser's solicitor | C |
| 15 | PSPLA notification requirements confirmed (§A5.6; F20 covenant then operates) | cl 14 | Regulatory lawyer | S (advice) / C (filings) |

---

*This report is a pre-lawyer hardening review of a draft agreement prepared from the parties' own precedents and agreed deal terms. It is not legal advice. The final document is to be settled by the parties' solicitors, who should receive this report, the instruction-letter material identified in §A5.9, and the source documents reviewed.*



