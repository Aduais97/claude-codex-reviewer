# FINAL READ-THROUGH — ROUND 3 (PRE-TRANSMISSION PASS)
## Agreement for Sale and Purchase of Shares — Nikki Wairau Christian (Vendor) to Ahmad Duais (Purchaser)
### Absolute Security Group Limited and SLS RTC Limited — NZ$260,000 — `SPA_DRAFT_V4.md` verified against `deal_facts.txt` (v2) and `ROUND2_VERIFICATION.md`

---

# C1. Executive Summary

**Verdict: CLEARED FOR TRANSMISSION TO FRANKLIN LAW — no BLOCKER.** Both v4 material changes are implemented correctly and, in substance, completely:

1. **The Lockhart trustee resolution is in.** Background D now states the definite holding — 1 personal share plus 1,524 shares held through Lockhart Trustee Services No.222 Limited, totalling 1,525 ordinary shares in each Company — the arithmetic is right (1 + 1,524 = 1,525; 1,525 of 10,000 issued = 15.25%), clause 1.2 treats the Trustee as a definite party, the execution block is active and unconditional, and the former `[●]` share-count placeholders and "if joined" conditional annotation are gone. Four residues of the old conditional structure survive in the surrounding text (the PARTIES block, the clause 1.2 joinder formula, and hedged wording in clauses 4.1(a) and 4.1(b)) — all RECOMMENDED fixes, none affecting validity, wording supplied below.

2. **The advisory carve-out is in and correctly shaped.** New clause 9.4 acknowledges the future advisory role (QC operations and compliance checking) without incorporating its terms, obliges no one to enter into it, and expressly coordinates with clauses 9.1 and 9.2. New clause 10.4(c) carves services to the Companies out of the restraint — and out of clause 10.1 *only*: clauses 11 (non-solicitation), 12 (confidentiality) and 13 (non-disparagement) continue to bind the Vendor in full while he performs the advisory role, so the carve-out cannot swallow the client restraints. The stress-test found one narrow seam (an indirect "services to a Company" argument via a third-party engagement — N9), one *expressio unius* gap (9.4's coordination sentence names 9.1 and 9.2 but not 9.3 — N10), and one technical-breach tension (clause 12 literally prohibits the *use* of confidential information the advisory role requires — N11). Each is a one-edit RECOMMENDED fix, drafted below.

**All five round-2 findings (N1–N5) are confirmed applied in v4** — the survival list includes 1.3 and 15.3; the set-off trigger reaches 4.3/4.4; the client definition covers 4.3, 4.4, 10 and 11; 12.1(a) uses the tightened three-limb formula; the 11.3 cascade names the 24-month period. Deal terms re-checked field-by-field against `deal_facts.txt` v2: **no drift**. The pronoun sweep found **zero** instances of she/her/he/him/his — the draft uses "the Vendor" throughout, as required. The regulatory-integrity constraint **holds** on the final text, including for the Trustee (clause 14.4 protects "any party", which the Trustee now is).

**Findings this round: 0 BLOCKER, 8 RECOMMENDED (N6–N13), 2 OPTIONAL (N14–N15).** All are minutes-of-work edits with exact wording supplied at §C6. Apply the RECOMMENDED set before transmission; N14–N15 may travel to the solicitors with this report.

**Process note:** the round-2 corpus-builder defect is fixed — this round's compiled corpus contained all four source documents in full, including the draft under review and the deal-facts sheet.

*Scope note: the engagement template's generic acquisition-analysis requirements (organisational benchmarking, EBITDA normalisation, valuation multiples) remain non-performable against this corpus and out of scope, per §A2.1 of round 1 and §B2 of round 2, adopted here without repetition. This is a legal-draft read-through; the price is agreed.*

---

# C2. Scope, Sources and Method

**Sources.** (i) `SPA_DRAFT_V4.md` (document under review); (ii) `deal_facts.txt` v2, updated 22 July 2026 (read first, as instructed — records the ownership resolution, the Vendor's gender, the restraint intent in the Purchaser's own words, and the advisory carve-out requirements); (iii) `ROUND2_VERIFICATION.md` (the previously verified v2 state and the N1–N5 fix wordings); (iv) `PRECEDENT_ProHost_2023.pdf` (context only — including its clause 8–10 advisory-services mechanics, used as a negative reference: v4 correctly imports none of them).

**Method — six passes:**

- **P1 (Change 1 verification):** every location that previously assumed a conditional trustee read against the definite-party facts: Background D, clauses 1.2, 3.1(a), 4.1(a)–(b), the execution blocks, and a grep sweep for residual `[●]` share counts, "if joined", "if applicable" and hedged trust language. Arithmetic checked.
- **P2 (Change 2 verification and stress-test):** clauses 9.4 and 10.4(c) verified against the three deal-facts requirements (not prohibit; acknowledge without incorporating; restraints intact for everything else), then stress-tested against 9.1, 9.2, 9.3, 3.1(f), 4.3, 12, and the indirect-competitor argument.
- **P3 (restraint-intent confirmation):** the Purchaser's stated intent traced limb-by-limb through 10.1, 10.4, 11.1 and 11.2, including whether the carve-out can swallow either limb.
- **P4 (carry-forward check):** N1–N5 verified present in v4; every wording round 2 quoted spot-checked against the v4 text. (Caveat: no v3 text was supplied, so no exhaustive v2→v4 line diff was possible; every checked location matched, and the only structural deltas found are the two authorised changes.)
- **P5 (language and cross-reference sweep):** full read-through; grep sweeps for gendered pronouns (zero hits), placeholder census, two-party idioms now imperfect in a three-party instrument, and resolution of every cross-reference touched by the 9.4 and 10.4(c) insertions.
- **P6 (regulatory-integrity re-confirmation):** the round-2 §B7 table re-run on the v4 deltas and on every proposed fix.

**Severity rubric** (unchanged): BLOCKER / RECOMMENDED / OPTIONAL. Findings continue the engagement's numbering from N5, as N6–N15.

---

# C3. Part 1 — Verification of Change 1: the Lockhart Trustee Resolution

## C3.1 Arithmetic

| Check | Expected | v4 | Result |
|---|---|---|---|
| Personal + trustee parcels | 1 + 1,524 = 1,525 | Background D: "1 ordinary share… personally, and 1,524 ordinary shares… through Lockhart Trustee Services No.222 Limited… being 1,525 ordinary shares in ASG and 1,525 ordinary shares in SLS" | **PASS** |
| Proportion of issued capital | 1,525 / 10,000 = 15.25% per company | Background A and B each state 10,000 issued ordinary shares (matches deal_facts and the Companies Register position) | **PASS** — consistent; the draft correctly does not state the percentage |
| Entity name | Lockhart Trustee Services No.222 Limited | Identical spelling in Background D and the execution block | **PASS** |

## C3.2 Location-by-location verification

| Location | Previous (v2, conditional) state | v4 state | Verdict |
|---|---|---|---|
| Background D | `[●]` share counts ×2; trustee/nominee contingency wording | Definite holdings; "(the Trustee)" defined; "The Trustee joins this agreement under clause 1.2" | **PASS** (style residue → N6) |
| cl 1.2 | Conditional joinder mechanics (F19) | "The Trustee joins this agreement as a party by executing it" + transfer obligation + (a) sale/transfer covenant, (b) 4.1(a)–(b) warranty pass-through, (c) clauses 10–13 covenant with body-corporate and individual-obligation limits | **PASS in substance** — the joinder *formula* is now the wrong idiom for a definite party (→ N6) |
| cl 3.1(a) | "duly executed by the Vendor" lineage | "duly executed by the registered holder in registrable form" — correctly accommodates two registered holders (Vendor: 1 share each; Trustee: 1,524 each) | **PASS** (micro-polish → N14) |
| cl 4.1(a) | Hedged ownership warranty | "the Vendor is, **or** through the registered holder referred to in clause 1.2 is, the sole legal and beneficial owner" — the disjunctive "or" is the conditional-era hedge; both limbs are now simultaneously true for different parcels | **PASS in substance**, residual hedge → N7 |
| cl 4.1(b) | "where Shares are held on trust" | Unchanged — but the condition is now a known fact, not a contingency | **PASS in substance**, residual hedge → N8 |
| Execution block | "[LOCKHART TRUSTEE SERVICES NO.222 LIMITED — if joined under clause 1.2]" (conditional) | Active, unconditional: "SIGNED by LOCKHART TRUSTEE SERVICES NO.222 LIMITED (as Trustee) as Registered holder" | **PASS** — activation correct; corporate execution formality and double-"as" phrasing → N12 |
| PARTIES block | Vendor and Purchaser only (correct while the Trustee was conditional) | Unchanged — the Trustee, now a definite executing party, is absent from the list | Residue → **N6** |
| Residual conditionals sweep | — | grep: zero hits for "if joined" / "if applicable" / `[●]` share counts; the only "where/or" hedges are 4.1(a) and 4.1(b) above | **PASS** |

**Conclusion:** Change 1 is implemented correctly and consistently at every operative location. What remains is style archaeology — four places where the drafting still *sounds* conditional even though it now *operates* definitely. None affects enforceability (the Trustee executes and clause 1.2 binds it), but this is the draft's last automated pass, so they are raised as N6–N8 with exact wording.

## C3.3 Trustee coherence checks (all cleared)

- **Default routing:** if the Trustee fails to deliver transfers, the Vendor is in default under clause 3.1 ("deliver, **or procure delivery**"), so clause 7.1 and the notice machinery operate against the Vendor without needing a separate Trustee-default regime. Coherent.
- **Restraint pass-through:** clause 1.2(c) binds the Trustee to clauses 10–13 "as if named as the Vendor", subject to the body-corporate capability limit; clause 10.4's carve-outs therefore read for the Trustee equally. Coherent.
- **Regulator protection:** clause 14.4 protects "any party" — which now includes the Trustee. The Trustee's new clause 12–13 obligations cannot fetter its regulator communications. Holds.
- **Two-party idioms:** clauses 8.2 ("each party releases the other"), 13.1 and 16.2 ("signed by both parties") use two-party grammar in what is now a three-party instrument. The variation clause is the one with operative bite → N13; the rest are tidies within it.

---

# C4. Part 2 — Verification of Change 2: the Advisory Carve-Out

## C4.1 Against the deal-facts requirements

| Requirement (deal_facts v2) | v4 implementation | Verdict |
|---|---|---|
| (a) The SPA must not prohibit the advisory role | cl 10.4(c): clause 10.1 does not prevent "providing services to either Company (including advisory, quality-control or compliance services under any separate written agreement with either Company as contemplated by clause 9.4)". Necessary and sufficient — ASG and SLS are themselves Restrained Businesses under 10.1(a), so without this carve-out the advisory role would literally breach the restraint | **PASS** (tightening → N9) |
| (b) Acknowledge without incorporating terms | cl 9.4: "under a separate written advisory agreement…"; "nothing in this agreement obliges either party to enter into that agreement, and its terms (including remuneration and termination) are recorded separately" | **PASS** (polish → N15) |
| (c) Restraints intact for everything outside services to the Companies | The carve-out disapplies **clause 10.1 only**. Clauses 11, 12 and 13 are untouched by it, and 10.4(c)'s own words limit it to services "to either Company" | **PASS** (see stress-test) |
| New engagement, not continuation of employment | cl 9.4 final sentence expressly preserves 9.1 (employment ends) and 9.2 (s149 record); cl 10.5 already anchors the restraints to the vendor capacity, not the employment | **PASS** (9.3 omission → N10) |

**Numbering and cross-references after the insertions:** 9.4 was appended after 9.3 — no renumbering ripple; clauses 10–17 are unchanged. 10.4's former consent limb (c) is now (d); no other provision cites 10.4's sub-letters, so nothing breaks. 10.4(c)'s reference to 9.4 resolves. All references to "clause 9" (3.1(e), 3.1(i), 3.2, 10.5) still land correctly — and 10.5's closing words ("independent of, and survive the ending of, the employment and **any engagement referred to in clause 9**") now do useful extra work: the restraints expressly survive the end of the advisory engagement too. **All PASS.**

## C4.2 Stress-test results

**(a) Could a role with a competitor be dressed up as "services to a Company"?** The operative words of 10.4(c) are "providing services to either Company"; the written-agreement condition sits only inside an "including" parenthetical, i.e. it is illustrative, not operative. The seam: the Vendor takes an engagement with a third party (a competitor, labour-hire firm or head contractor) and argues that his *activity* — say, QC-checking guards on a site where ASG is subcontractor, or a secondment onto ASG work — is "providing services to either Company". The argument should fail (his engagement is *with* the third party, and being an employee or contractor *of* a Restrained Business breaches 10.1(a) regardless of where he is deployed; and any genuine secondment into ASG requires ASG — Purchaser-controlled — to accept him), but the carve-out as drafted gives it a foothold. One edit makes the written agreement with the Company the operative condition and kills every indirect route → **N9 (RECOMMENDED)**.

**(b) cl 9.1 (employment ends).** No conflict — 9.4 expressly provides that the ending of employment is "not affected by, and do[es] not affect" the advisory agreement, and the advisory engagement begins "from settlement", after employment ends. **Cleared.**

**(c) cl 9.2 (s149 record, employment-only).** No conflict — the record "shall relate to employment matters only"; the advisory agreement is a new engagement, not a continuation, and 9.4 expressly insulates the record. The 9.2 design (no restatement of restraints) is undisturbed. **Cleared.**

**(d) cl 9.3 (10-day unpaid handover) — redundant or contradictory next to a paid advisory role?** Neither, on the correct reading: 9.3 is the *backstop* — it is an SPA obligation that exists whether or not the advisory agreement is ever signed (9.4: "nothing in this agreement obliges either party to enter into that agreement"), and it is expressly *not* services ("does not require the Vendor to attend any workplace or perform any services"), so it does not overlap the paid scope. But 9.4's coordination sentence names only 9.1 and 9.2 as "not affected" — the same *expressio unius* pattern round 2 caught in the survival list (N1). The omission of 9.3 invites the argument that the paid advisory agreement subsumes or supersedes the free handover. One-line fix → **N10 (RECOMMENDED)**.

**(e) cl 3.1(f) (return of ALL credentials and logins at settlement) vs an ongoing QC advisor's access needs.** No contradiction — and the sequence as drafted is the *correct* security posture: complete surrender and MFA re-registration at settlement, then fresh, minimal access re-granted by the Companies under (and governed by) the advisory agreement, on the Companies' terms and revocable with it. The same logic applies to the 4.4 deletion certificate: any records the advisory role needs are re-provided afresh. Nothing in 3.1(f) or 4.4 prevents a re-grant. **Cleared — no SPA edit needed**; the instruction letter should tell Franklin Law to put the access-grant, access-revocation and return-on-termination provisions *in the advisory agreement* (§C9, package note 3).

**(f) cl 4.3 (pre-settlement discussion ban).** No conflict — the advisory agreement is negotiated with the Purchaser and the Companies' boards, none of whom is a "client, supplier or staff member"; and any pre-settlement announcement of the Vendor's ongoing QC role to staff or clients is exactly what 4.3(a)'s carve-out to the clause 13.2 agreed-form channel is for. The ban is doing its intended job here, not obstructing the carve-out. **Cleared.**

**(g) cl 12 (confidentiality) — an advisor necessarily receives and uses confidential information.** Here there is a real technical tension: 12.1 prohibits the Vendor *using* confidential information (rosters, staffing arrangements, operational methods — the exact enumerated categories QC work runs on), and after the N4 tightening the exceptions are "required by law", "expressly permitted by this agreement", and regulator communications. The advisory agreement is *not* "this agreement", and 9.4 acknowledges the role but does not expressly permit the use. Use on behalf of, and at the request of, the protected party would almost certainly be read as impliedly consented (round 2 cleared the 9.3/12.1 interaction on that basis) — but the advisory role makes this a recurring exposure rather than a 10-day one, and the Vendor's side could use the tension to demand a broader confidentiality rewrite later. One inserted limb forecloses it → **N11 (RECOMMENDED)**.

---

# C5. Part 3 — Restraint-Intent Confirmation

The Purchaser's stated intent (deal_facts v2, verbatim): *"Nikki restraint is to go and work for a guarding business and take clients from ASG to other businesses which is where the restraint must be put."*

| Intent limb | Where it lives in v4 | Intact? |
|---|---|---|
| (1) No working for / operating a guarding business | 10.1(a): full-sector Restrained Business list (guarding, crowd control/host, event, patrol, static, loss prevention, close protection, monitoring, CIT, concierge, training, personnel supply, consultancy), in every capacity (employee → adviser → financier); 10.2/10.3 cascades; 10.4(b) permits out-of-sector roles only if not "with or for" a competing provider | **YES** |
| (2) No taking ASG/SLS clients elsewhere | 10.1(b) (no services of the Companies' kind to any client) + 11.1(a) (no solicitation or diversion, no accepting custom in a Restrained Business) + 11.2's wide client definition (head-contractor, facilities-manager and venue-inclusive, 24-month lookback, extended to 4.3/4.4 by N3) + 4.3/4.4 pre-settlement protections with the 15.1 set-off trigger (N2) | **YES** |
| Carve-out cannot swallow either limb | 10.4(c) (i) disapplies **only clause 10.1** — while advising the Companies the Vendor remains fully bound by 11 (non-solicitation), 12 (confidentiality) and 13 (non-disparagement), so client contact in the QC role cannot lawfully become client diversion; (ii) is limited to services *to the Companies* — with N9 applied, only under a written agreement with the relevant Company, and not through or on behalf of anyone else; (iii) is inherently self-limiting in the direct case, because the Companies (Purchaser-controlled) choose whether, and on what scope, to engage him | **YES** (N9 closes the one indirect seam) |

**Confirmation: the restraint still matches the stated intent, and the carve-out is a door only the Purchaser's own companies can open.**

---

# C6. Part 4 — Findings N6–N15

No BLOCKER. Eight RECOMMENDED, two OPTIONAL. Each carries exact fix wording and a regulatory-integrity check.

---

### N6 — [RECOMMENDED] — PARTIES block, cl 1.2, Background D — the Trustee is a definite executing party but is missing from the PARTIES list, and 1.2 keeps the conditional-era joinder formula

**Issue.** The PARTIES block still lists only the Vendor and the Purchaser — correct while the Trustee was conditional, wrong now that it is a definite party which executes the agreement and gives covenants and warranties. Clause 1.2's opening ("The Trustee **joins** this agreement as a party **by executing it**") and Background D's echo ("The Trustee joins this agreement under clause 1.2") are joinder mechanics for a party that might arrive later; the Trustee is here from day one. Not a validity problem — execution plus 1.2 binds the Trustee — but it is the most visible residue of the resolved contingency, and the first thing Franklin Law will notice.

**Fix (three edits).**
1. In PARTIES, add:
   > 3.  LOCKHART TRUSTEE SERVICES NO.222 LIMITED (Trustee)
2. In clause 1.2, replace the first sentence:
   > The Trustee joins this agreement as a party by executing it. The Trustee shall transfer the Shares registered in its name…
   with:
   > The Trustee is a party to this agreement as the registered holder of the Shares described in Background D. The Trustee shall transfer the Shares registered in its name…
   and in the same clause replace "and by executing it: (a) agrees" with "and: (a) agrees".
3. In Background D, replace the final sentence "The Trustee joins this agreement under clause 1.2." with:
   > The Trustee is a party to this agreement (clause 1.2).

**Regulatory-integrity check:** party mechanics only; no regulator-facing effect. Clear.

---

### N7 — [RECOMMENDED] — cl 4.1(a) — the ownership warranty keeps the conditional-era disjunctive "is, or through the registered holder… is"

**Issue.** "the Vendor is, **or** through the registered holder referred to in clause 1.2 is, the sole legal and beneficial owner of the Shares" was drafted when the trustee holding was unconfirmed. The facts are now known and *both* limbs are simultaneously true for different parcels (1 share direct; 1,524 via the Trustee) — so the connective should be conjunctive. As drafted, a disjunctive warranty is literally satisfied if *either* limb holds, which is weaker than the Purchaser needs and weaker than the facts support. The Trustee's parallel warranty under 1.2(b) mitigates but does not cure the hedge in the Vendor's own warranty.

**Fix (one edit in clause 4.1(a)).** Replace:
> the Vendor is, or through the registered holder referred to in clause 1.2 is, the sole legal and beneficial owner of the Shares, free of all encumbrances,

with:
> the Vendor is, directly and through the Trustee as registered holder under clause 1.2, the sole legal and beneficial owner of the Shares, free of all encumbrances,

(Minimal-diff form deliberately chosen so that 1.2(b)'s pass-through — the Trustee warranting "the matters in clauses 4.1(a) and 4.1(b) in respect of its Shares" — continues to read exactly as before.)

**Regulatory-integrity check:** none implicated. Clear.

---

### N8 — [RECOMMENDED] — cl 4.1(b) — "where Shares are held on trust" is a contingency that is now a known fact

**Issue.** "and where Shares are held on trust, all trustee authorisations required for the sale have been obtained" hedges on whether a trust holding exists. It does: 1,524 shares per company are registered to the Trustee on the Vendor's behalf. The warranty should assert the authorisations for *those* Shares definitely.

**Fix (one edit in clause 4.1(b)).** Replace:
> and where Shares are held on trust, all trustee authorisations required for the sale have been obtained;

with:
> and, in respect of the Shares registered in the name of the Trustee, all trustee resolutions and authorisations required for the sale and transfer of those Shares have been obtained;

**Regulatory-integrity check:** none implicated. Clear.

---

### N9 — [RECOMMENDED] — cl 10.4(c) — make the written agreement with the Company the operative condition of the carve-out, closing the indirect-"services to a Company" argument

**Issue.** As drafted, the operative words are "providing services to either Company", and the written-agreement condition appears only inside an illustrative "including" parenthetical. That leaves the Vendor room to argue that activity performed in the course of an engagement with a *third party* — a labour-hire placement onto ASG work, QC-checking ASG's guards on behalf of a head contractor, a "secondment" from a competitor — is "providing services to either Company" and therefore outside the restraint. The argument should lose (the engagement with the third party independently breaches 10.1(a)), but this Vendor knows the template, and the carve-out is the newest and least-tested clause in the document. Conditioning the carve-out on a written agreement between the Vendor and the Company makes the Companies' consent — the whole safety theory of the carve-out — explicit and unavoidable, and matches deal_facts ("under a SEPARATE agreement").

**Fix (one edit in clause 10.4(c)).** Replace:
> (c) providing services to either Company (including advisory, quality-control or compliance services under any separate written agreement with either Company as contemplated by clause 9.4); or

with:
> (c) providing services directly to either Company under a written agreement between the Vendor and that Company (including the advisory, quality-control and compliance services contemplated by clause 9.4), and not on behalf of, through, or in the course of any employment or engagement with, any other person or entity; or

**Regulatory-integrity check:** this narrows a carve-out from the restraint, not any regulator gateway; clause 14.4 overrides clauses 10 to 13 in any event. Clear.

---

### N10 — [RECOMMENDED] — cl 9.4 — the coordination sentence names 9.1 and 9.2 but not 9.3, inviting the argument that the paid advisory role displaces the free handover

**Issue.** 9.4's final sentence expressly insulates the ending of employment (9.1) and the record of settlement (9.2) from the advisory agreement — but not the 10-day unpaid handover (9.3). Same *expressio unius* pattern as round 2's N1: by enumerating two of the three neighbouring provisions, the drafting implies the third *is* affected. The Vendor's argument writes itself: "the parties agreed I would be paid for advisory services from settlement; the free handover was superseded." 9.3 is precisely the backstop the Purchaser needs if the advisory agreement is never signed or collapses early, and it should be expressly preserved.

**Fix (one edit in clause 9.4, final sentence).** Replace:
> The ending of employment under clause 9.1, and the record of settlement under clause 9.2, are not affected by, and do not affect, any such advisory agreement.

with:
> The ending of employment under clause 9.1, the record of settlement under clause 9.2, and the handover obligation under clause 9.3 are not affected by, and do not affect, any such advisory agreement, and clause 9.3 applies whether or not that agreement is entered into.

**Regulatory-integrity check:** none implicated. Clear.

---

### N11 — [RECOMMENDED] — cl 12.1 — the confidentiality clause literally prohibits the use of the very information the advisory role requires

**Issue.** 12.1 forbids the Vendor to "use or disclose" confidential information — expressly including rosters, staffing arrangements and operational methods, the raw material of QC and compliance checking — and, after the round-2 N4 tightening, excepts only disclosure required by law, "expressly permitted by this agreement", and regulator communications. The advisory agreement is not "this agreement", and 9.4 acknowledges the role without expressly permitting the use. Use *for* the Companies at their request would almost certainly be read as consented (the round-2 clearance of 9.3 vs 12.1 rests on the same logic), but the advisory role converts a 10-day theoretical tension into a standing one, and leaving it open hands the Vendor's solicitors a reason to reopen clause 12. One inserted limb resolves it in the Purchaser's favour: use is permitted only in the course of, and to the extent necessary for, services the Companies themselves have requested.

**Fix (one edit in clause 12.1).** Replace:
> except (a) as required by law, as expressly permitted by this agreement, or as made to any regulator in accordance with clause 14.4, or (b) information which is or becomes public other than through a breach of this clause.

with:
> except (a) as required by law, as expressly permitted by this agreement, or as made to any regulator in accordance with clause 14.4, (b) use or disclosure solely in the course of, and to the extent necessary for, providing services to either Company at that Company's request (including under the advisory agreement contemplated by clause 9.4), or (c) information which is or becomes public other than through a breach of this clause.

(No other provision cites 12.1's sub-letters, so the relettering ripples nowhere.)

**Regulatory-integrity check:** this *adds* a permission running to the protected party's benefit and leaves the regulator limb untouched. Clear.

---

### N12 — [RECOMMENDED] — Execution block — a company cannot sign like an individual, and "(as Trustee) as Registered holder" reads twice

**Issue.** The now-active Lockhart block uses the individual-style attestation (single unlabelled signature line plus witness) and the double formula "SIGNED by LOCKHART TRUSTEE SERVICES NO.222 LIMITED (as Trustee) as Registered holder". A body corporate signs by its director(s) or authorised signatory (Companies Act 1993, s 180); the signatory's name and capacity should be captured, and the "as… as…" stutter should go.

**Fix (replace the Lockhart execution block).**
> SIGNED for and on behalf of LOCKHART TRUSTEE SERVICES NO.222 LIMITED as Trustee and registered holder by:
>
> Signature:  ______________________________
>
> Name: ______________________    Position (director / authorised signatory): ______________________

(Franklin Law to settle final execution formalities for all three parties; this brings the block to the conventional starting point.)

**Regulatory-integrity check:** none implicated. Clear.

---

### N13 — [RECOMMENDED] — cl 16.2 (with tidies in 8.2 and 16.3) — two-party grammar in a three-party instrument, sharpest in the variation clause

**Issue.** 16.2 permits variation "only in writing signed by **both** parties" — in a three-party agreement that literally suggests two signatures suffice, including for a variation touching the Trustee's transfer obligation or its clause 10–13 covenants. General contract law would protect the non-signing party, but the variation clause should not point the wrong way. Two softer instances travel with it: 8.2 ("each party releases the other") and the absence of a Trustee line in the 16.3 notice addresses.

**Fix.**
1. In clause 16.2, replace "signed by both parties" with "signed by each party".
2. In clause 8.2, replace "each party releases the other from" with "each party releases each other party from".
3. In clause 16.3, add below the Purchaser line:
   > Trustee:  [●] (post)  /  [●] (email)
   (Per deal_facts the Trustee sits under the Vendor's ownership, so these may simply duplicate the Vendor's details — but the party should have a notice address.)

**Regulatory-integrity check:** none implicated. Clear.

---

### N14 — [OPTIONAL] — cl 3.1(a) — "the registered holder" → "the relevant registered holder"

**Issue.** With two registered holders (Vendor and Trustee), "duly executed by the registered holder" is grammatically serviceable (each transfer is executed by its own holder) but a one-word tighten removes any doubt about which holder executes which transfer.

**Fix.** In clause 3.1(a), replace "duly executed by the registered holder in registrable form" with "duly executed by the relevant registered holder in registrable form".

**Regulatory-integrity check:** none implicated. Clear.

---

### N15 — [OPTIONAL] — cl 9.4 — three tense/precision polishes in the acknowledgement

**Issue.** (i) "Any such services **are provided** to the Companies alone" and "its terms… **are recorded** separately" use the present tense for an agreement that does not yet exist and may never be entered into (as 9.4 itself says); (ii) "nothing in this agreement obliges **either party**" — the advisory agreement's counterparties are the Vendor and the *Companies*, who are not SPA parties, so the persons not obliged are better named.

**Fix (one edit in clause 9.4, second sentence).** Replace:
> Any such services are provided to the Companies alone; nothing in this agreement obliges either party to enter into that agreement, and its terms (including remuneration and termination) are recorded separately.

with:
> Any such services will be provided to the Companies alone; nothing in this agreement obliges the Vendor, the Purchaser or either Company to enter into that agreement, and its terms (including remuneration and termination) will be recorded in that agreement and not in this one.

**Regulatory-integrity check:** none implicated. Clear.

---

## C6.1 Interactions considered and cleared this round

| Interaction | Assessment |
|---|---|
| cl 9.3 vs the paid advisory role | **Cleared as backstop** (see §C4.2(d)); N10 forecloses the supersession argument. |
| cl 3.1(f)/4.4 credential surrender vs advisor access | **Cleared** — surrender-then-regrant is the correct posture; access terms belong in the advisory agreement (§C9 note 3). |
| cl 4.3 discussion ban vs advisory negotiation and announcement | **Cleared** — negotiation is with the Purchaser/boards; announcements route through 13.2 as designed. |
| cl 10.5 "any engagement referred to in clause 9" now capturing the advisory engagement | **Cleared — beneficial**: the restraints expressly survive the advisory engagement's end. |
| cl 11.1(c) ("interfere with… clients") vs QC site visits | **Cleared** — acting for a Company at its request is not interference; and 10.4(c) does not disapply clause 11, so solicitation on site remains a breach. |
| Trustee bound by 12–13 vs regulator communications | **Cleared** — 14.4 protects "any party", now including the Trustee. |
| 10.4(c) "with either Company" vs 9.4 "between the Vendor and the Companies" | **Cleared** — "either" comprehends both; no conflict. |
| 16.5 survival list not naming clause 9 | **Cleared** — 9.2/9.3/9.4 operate post-settlement by their own express terms; the 16.5 list was settled by rounds 1–2 (N1) and the pattern is unchanged by v4. |
| Advisory role vs open PSPLA→CIPU process | **No SPA defect** — but see §C9 note 4: whether the QC/compliance role itself has PSPLA licensing implications for the Vendor is a question for Franklin Law and the advisory agreement, not this document. |

---

# C7. Part 5 — Language Sweep Results

- **Gendered pronouns: ZERO hits.** A whole-document grep for she/her/hers/he/him/his/himself/herself found no instance in any form. The draft uses "the Vendor", "the Purchaser", "the Trustee" (its) throughout, exactly as deal_facts v2 requires. (Round 2's report text used "she" in a hypothetical — the *draft* never did in v2 and does not now.)
- **Residual hedged/conditional wording:** confined to the four locations raised as N6–N8 (PARTIES/1.2/Background D joinder formula; 4.1(a) disjunctive; 4.1(b) "where… held on trust"). The remaining "if" clauses — 3.1(d) (if a director), 3.1(g) (if certificates issued), 3.1(j) (if no pre-emptive rights) — are genuine factual conditionals and correctly conditional.
- **Numbering:** clause 9 now runs 9.1–9.4; clause 10.4 runs (a)–(d); no other structural change; clauses 10–17 unchanged; no renumbering ripple; no reference anywhere to a superseded sub-letter. "Clauses 10 to 13" is used consistently (Background E, 1.2, 9.2, 14.4, 17.1(c)); grep confirms no "10 to 14" anywhere.
- **N1–N5 carry-forward confirmed in v4:** 16.5 lists "1.3, 4, 5, 8, 12, 13, 14, 15.2, 15.3, 16 and 17" (N1); 15.1 opens "If the Vendor is in material breach of clause 4.3 or 4.4 or of clauses 10, 11, 12 or 13" (N2); 11.2 opens "In clauses 4.3, 4.4, 10 and 11" (N3); 12.1(a) reads "as required by law, as expressly permitted by this agreement, or as made to any regulator in accordance with clause 14.4" (N4); 11.3 opens "If the twenty-four (24) month period in clause 11.1" (N5). All five applied exactly.
- **Deal-term re-check:** all round-2 §B6 fields re-verified against v4 — parties, company numbers, NZBNs, registered offices, 10,000 issued shares each, $260,000 = $100,000 (1 Aug 2026) + $80,000 (1 Sep 2026) + $80,000 (1 Oct 2026), Settlement Date 1 August 2026, Lockhart spelling, 12% default interest, 14-day windows, 24-month restraints, arbitration structure. **No drift**, and item 11 (share counts) has moved from "gate" to **match** (1,525 + 1,525).
- **Reading quality:** the document reads cleanly end to end; the only awkward constructions found are those already itemised (the double-"as" in the Lockhart block (N12), the 9.4 tense slips (N15), and the 4.1(a) disjunctive (N7)).

---

# C8. Part 6 — Regulatory-Integrity Re-Confirmation

The round-2 §B7 table was re-run on the v4 text with specific attention to the two changes and every proposed fix. Constraint: nothing may conceal, transfer or release personal regulatory liability, and nothing may restrain, penalise or discourage communications with the regulator during the open PSPLA → CIPU process.

| Check | v4 position | Result |
|---|---|---|
| cl 9.4 (advisory acknowledgement) | Imposes no obligation capable of touching regulator communications; conceals nothing (the advisory arrangement is recorded on the face of the SPA, not hidden) | **HOLDS** |
| cl 10.4(c) (carve-out) | Widens the Vendor's permitted activity; cannot fetter any communication | **HOLDS** |
| Trustee as definite party under clauses 12–13 | 14.4 protects "**any party**" — now including the Trustee — for any communication with any regulator, required or voluntary, and no such communication is a breach or set-off ground | **HOLDS** |
| 14.4 parenthetical | "(including clauses 4.3, 4.4 and 10 to 13)" — unchanged from the verified v2 state | **HOLDS** |
| No transfer/release of personal regulatory liability | 14.2 and 8.2(c) unchanged | **HOLDS** |
| Consideration not expressed to buy regulatory cooperation | Background E and 1.2 still "clauses 10 to 13"; cl 14 still excluded from the 17.1(c) injunction carve-out | **HOLDS** |
| Employment record cannot touch PSPLA processes | 9.2 unchanged ("employment matters only"); 9.4 expressly leaves 9.2 undisturbed | **HOLDS** |
| Notification duties | 14.3 unchanged — the change in shareholding (now including the Trustee's transfer) must be notified promptly and accurately | **HOLDS** |
| Findings N6–N15 tested against the constraint | Each checked individually at §C6 — none narrows any regulator gateway; N11 adds a Company-facing permission and leaves the regulator limb untouched; N9 narrows only a restraint carve-out, which 14.4 overrides in any event | **HOLDS** |

**Confirmation: the agreement as it stands — and as it would stand with N6–N15 applied — conceals nothing, fetters no regulator communication, and preserves personal regulatory responsibility in both directions, for all three parties.**

---

# C9. Sign-Readiness Verdict

**VERDICT: CLEARED FOR TRANSMISSION TO FRANKLIN LAW — apply N6–N13 first (minutes of work, all wording at §C6); N14–N15 at the Purchaser's option.** Both v4 material changes are correctly and consistently implemented; the arithmetic is right; all prior-round findings (F1–F25, N1–N5) are confirmed in place; deal terms match `deal_facts.txt` v2 exactly; the pronoun requirement is met with zero exceptions; the regulatory-integrity constraint holds for all three parties. No BLOCKER exists. **The F1/Lockhart gate — the single blocker to signing since round 1 — is resolved**: the trustee parcels are confirmed as the Vendor's beneficial stake and the draft now reflects it.

## Remaining placeholder list (all expected; none may survive to execution)

| # | Placeholder | Location | Owner / trigger |
|---|---|---|---|
| 1 | Agreement date "[        ] 2026" | Front page | Complete at signing |
| 2 | `$[●]` — ASG price apportionment | cl 2.1 | Accountant (per deal_facts, still open) |
| 3 | `$[●]` — SLS price apportionment | cl 2.1 | Accountant |
| 4–5 | `[●]` Vendor notice addresses (post / email) | cl 16.3 | Parties, before signing |
| 6–7 | `[●]` Purchaser notice addresses (post / email) | cl 16.3 | Parties, before signing |
| — | (+2 if N13.3 adopted: Trustee notice addresses) | cl 16.3 | Parties, before signing |
| — | "DRAFT FOR LEGAL REVIEW — NOT FOR EXECUTION" banner | Front page | Remove only at execution |

## What travels with the draft (package notes for the instruction letter)

1. **This report plus `ROUND1_FINDINGS.md` and `ROUND2_VERIFICATION.md`** — the complete audit trail; the change-set Franklin Law must defend to the Vendor's side is exactly the findings lists.
2. **The advisory agreement is now a live drafting task.** It is deliberately not part of the SPA; Franklin Law should prepare it concurrently so both documents can complete together. Deal points from deal_facts: QC operations and compliance checking; between the Vendor and the Companies; new engagement, not continuation; remuneration and termination in that document. (Precedent context: the Gwin 2025 deal used an appendix; here it stays a separate document by design.)
3. **Advisory-agreement contents to request:** its own confidentiality and IP clauses; access-grant, access-control and return-on-termination provisions (mirroring the SPA's 3.1(f) surrender — access under the advisory role is a fresh, revocable grant, not a carve-back); an express acknowledgement that the SPA restraints (clauses 10–13) are unaffected and survive its termination (matching SPA 10.5 and 9.4).
4. **PSPLA point for advice, not drafting:** whether the Vendor's post-settlement QC/compliance role has any licensing or certificate-of-approval implication given the open PSPLA→CIPU process, and whether the advisory arrangement should feature in the 14.3 notifications. The SPA conceals nothing; this is a compliance question for the solicitors.
5. **Trust-records evidence:** the beneficial-ownership resolution was made on the deal facts (22 July 2026); Franklin Law should verify it from the trust's records before signing, alongside the standing round-1 §A6 items — constitutions/shareholders'-agreement review and pre-emption waivers (Nabawi 40.16%; the 3.1(j) deliverable covers the mechanics), current register extract, MBIE mediator booking against 1 August 2026, Vendor's bank-account nomination by 30 July 2026.

**Bottom line for the Purchaser:** make the eight recommended edits — every one is a supplied one- or two-line change — and transmit. The draft now says what the deal is: a definite three-party sale of 1,525 shares in each company, a clean exit from employment, a door held open for the Vendor to keep serving *your* companies on *your* terms, and a restraint that closes every other door.

---

*This report is the round-3 pre-transmission pass of a pre-lawyer hardening review. It is not legal advice. The final documents (SPA and advisory agreement) are to be settled by the parties' solicitors, who should receive all three rounds' reports and the source documents.*
