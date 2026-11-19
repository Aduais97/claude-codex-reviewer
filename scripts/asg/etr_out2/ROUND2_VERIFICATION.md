# VERIFICATION REVIEW — ROUND 2 (FINAL AUTOMATED GATE)
## Agreement for Sale and Purchase of Shares — Nikki Wairau Christian (Vendor) to Ahmad Duais (Purchaser)
### Absolute Security Group Limited and SLS RTC Limited — NZ$260,000 — `SPA_DRAFT_V2.md` verified against `ROUND1_FINDINGS.md`

---

# B1. Executive Summary

**Verdict: PASS — the v2 draft is cleared to go to Franklin Law.** Every applicable round-1 finding (F2–F25) has been applied, and a full line-by-line diff of v1 against v2 confirms there are **no silent or unauthorised edits anywhere in the document** — every changed line maps to a numbered finding. All internal cross-references resolve correctly after the renumbering. Deal terms remain an exact match to `deal_facts.txt`. The regulatory-integrity constraint holds everywhere, and clause 14.4 now expressly reaches clauses 4.3 and 4.4 as intended.

**Application scorecard for the 25 round-1 findings:**

| Classification | Count | Findings |
|---|---|---|
| APPLIED CORRECTLY (character-exact to the round-1 suggested wording) | 21 | F3, F4, F6, F7, F8, F9, F10, F11, F12, F13, F14, F15, F16, F17, F18, F19, F20, F21, F22, F23, F24 |
| APPLIED WITH DIVERGENCE — beneficial, pre-authorised by round 1 | 1 | F2 (clause 14.4's parenthetical extended to include clauses 4.3 and 4.4 — the exact improvement round 1's regulatory-integrity backstop invited) |
| APPLIED WITH DIVERGENCE — immaterial, consequential tidy | 1 | F5 (clause 11.1(a): "any client of either Company" / "any such client" simplified to "any client" — consistent with the new defined term, though round 1 said "no further change needed") |
| APPLIED CORRECTLY (no change was required) | 1 | F25 (12-month staff lookback deliberately retained — confirmed intentional) |
| CORRECTLY HELD OPEN (factual gate — placeholders retained by design) | 1 | F1 (share numbers `[●]`, price apportionment `$[●]`, conditional Lockhart execution block — all still open, as they must be) |
| NOT APPLIED | **0** | — |

**The new-defect sweep found no blockers.** It found **three RECOMMENDED and two OPTIONAL new findings (N1–N5)**, all of which are *composition* defects — places where two round-1 amendments, each faithfully applied, interact imperfectly. The most significant (N1): **the survival clause (16.5) lists 15.2 but omits 15.3** — the set-off/default firewall that resolved BLOCKER F23. On a purported cancellation, the clause that makes the Purchaser pay (15.2) expressly survives while the clause that protects him from default characterisation (15.3) arguably does not, and the express listing of 15.2 invites the inference that 15.3's exclusion was deliberate. This partially re-opens, in the post-cancellation window only, the exposure F23 closed. It is a one-line fix (drafted at §B5) and should be applied before the draft is transmitted. N2 and N3 similarly complete the intended reach of the clause 4.3/4.4 protections (set-off trigger and "client" definition); N4 and N5 are precision polish.

**Sign-readiness in one paragraph:** the document is drafting-complete. Nothing NOT APPLIED, no unauthorised edits, no broken cross-references, no deal-term error, no regulatory-integrity leak. What remains falls into two categories: (i) five cheap text edits from this round's sweep (N1 strongly recommended before transmission; N2–N5 may be left to the settling solicitors with this report); and (ii) the factual and external matters that were never drafting matters — the F1/Lockhart gate, the placeholder schedule, and the round-1 §A5 reserved matters — all of which travel *with* the draft to the solicitors and gate **signing**, not transmission.

> **⚠ PROCESS WARNING — corpus integrity (must be fixed before any further automated round).** The compiled corpus supplied for this round (`_analysis_corpus.txt`) was truncated at its 100,000-character limit and **omitted the two central documents entirely — `SPA_DRAFT_V2.md` and `deal_facts.txt` — and cut `ROUND1_FINDINGS.md` off mid-section (§D6)**, leaving only the ProHost precedent and roughly 80% of the round-1 report. The supplied framework file (`_analysis_framework.txt`) contained only an API connection error. This verification was therefore performed against the canonical source files in `etr_corpus2/` (and `etr_corpus/SPA_DRAFT.md` for the v1↔v2 diff), which is the correct evidence base — but a future automated pass that trusted the compiled corpus alone would have "verified" a draft it had never read. Fix the corpus builder (raise the limit or corpus the documents in priority order, draft first) before round 3, if any.

---

# B2. Scope, Sources and Method

**Scope.** This is the verification round of a legal draft — not an acquisition analysis. The engagement template's generic requirements (organisational benchmarking, revenue per FTE, EBITDA normalisation, valuation multiples) remain non-performable against this corpus for the reasons established at §A2.1 of the round-1 report, which is adopted here without repetition: the corpus contains one draft agreement, one findings report, one precedent and one deal-facts sheet, and no financial, organisational or market data of any kind. The price is agreed. The deliverable, per the round-2 brief, is: (1) finding-by-finding verification of F1–F25; (2) the post-renumbering cross-reference audit; (3) a new-defect sweep over the amendments themselves; (4) a deal-term re-check; (5) regulatory-integrity confirmation; then the sign-readiness verdict.

**Sources.** (i) `SPA_DRAFT_V2.md` (document under verification); (ii) `ROUND1_FINDINGS.md` (the 25-finding round-1 report whose suggested wordings are the verification baseline); (iii) `deal_facts.txt` (agreed terms; Companies Register position 30 June 2026); (iv) `PRECEDENT_ProHost_2023.pdf` (base template, context only this round); (v) `SPA_DRAFT.md` (the v1 draft, retrieved from the round-1 corpus directory to enable a full-document diff — see the process warning above for why the compiled corpus could not be used).

**Method — five passes:**

- **V1 (application check):** each of F2–F25's exact suggested wordings compared character-by-character against the v2 text at its expected location; every divergence quoted and assessed for materiality.
- **V2 (diff audit):** full line diff of v1 → v2; every changed, added or deleted line attributed to a specific finding. Any hunk not attributable to a finding would have been an unauthorised edit — none was found. This pass is what converts "the findings I checked were applied" into "nothing else was touched."
- **V3 (cross-reference audit):** every internal clause reference in v2 resolved against the renumbered structure, with specific attention to the nine danger points listed in the round-1 renumbering note.
- **V4 (new-defect sweep):** the amendments read *against each other* — contradictions between new clauses, definitions used out of scope, survival-list omissions, double obligations, and the enforcement-path traces re-walked with the new clauses in place.
- **V5 (deal-term and integrity re-check):** the round-1 §D1 diff re-run field-by-field against `deal_facts.txt`; the regulatory-integrity constraint re-tested clause-by-clause on the final text.

**Severity rubric for new findings** (unchanged from round 1): BLOCKER / RECOMMENDED / OPTIONAL. Every new finding carries exact fix wording and has been checked against the regulatory-integrity constraint ("nothing may conceal, transfer or release personal regulatory liability or fetter dealings with the PSPLA/CIPU").

---

# B3. Part 1 — Verification of Findings F1–F25

## B3.1 Verification table

Verdicts: **AC** = APPLIED CORRECTLY (character-exact unless noted); **AD** = APPLIED WITH DIVERGENCE (divergence quoted at §B3.2 and assessed); F1 is the standing factual gate and is assessed for whether it was correctly *held open*, not applied.

| # | Sev. | Round-1 requirement (compressed) | v2 location | Verdict | Note |
|---|---|---|---|---|---|
| F1 | BLOCKER | Factual gate: keep share-number and apportionment placeholders; do not resolve on paper; Lockhart execution block stays conditional | Background D; cl 2.1; execution block | **CORRECTLY HELD OPEN** | Background D retains `[●]` ×2; cl 2.1 retains `$[●]` ×2; execution block retains "[LOCKHART TRUSTEE SERVICES NO.222 LIMITED — if joined under clause 1.2]". No one has guessed numbers into the draft. Gate unchanged — signing remains blocked until resolved (§B8). |
| F2 | BLOCKER | (1) strike "or regulators" from 11.1(c); (2) recast 12.1(a) to the required-or-permitted + regulator formula; (3) insert regulator-communications carve-out as new 14.4 | cl 11.1(c); cl 12.1(a); cl 14.4 | **AD (beneficial)** | Parts (1) and (2) character-exact. Part (3) exact except the parenthetical: "(including clauses **4.3, 4.4 and** 10 to 13)" vs round 1's "(including clauses 10 to 13)" — the precise improvement round 1's regulatory-integrity backstop invited. See §B3.2(a). |
| F3 | REC | Replace 10.4(b) with the role-activity carve-out | cl 10.4(b) | **AC** | Character-exact. |
| F4 | REC | Replace the Restrained Business service list in 10.1(a) with the full-sector list | cl 10.1(a) | **AC** | Character-exact, including the deliberate omission of any licence-status restraint. |
| F5 | REC | Insert client definition as new 11.2; simplify 10.1(b) to "any client"; 11.1(a) to rely on the defined term | cl 11.2; cl 10.1(b); cl 11.1(a) | **AD (immaterial)** | 11.2 and 10.1(b) character-exact. In 11.1(a) the drafter also deleted "of either Company" and changed "any such client" to "any client" — round 1 said "no further change needed" there. Benign and definition-consistent; see §B3.2(b). |
| F6 | REC | Insert non-solicit cascade as new 11.3 | cl 11.3 | **AC** | Character-exact. (But see new finding N5 on its "any period" phrasing — a round-1 wording residual, not an application error.) |
| F7 | REC | Replace 3.1(f) (vehicles, MFA transfer); add (g) share certificates and (h) bank/payroll de-authorisation forms | cl 3.1(f)–(h) | **AC** | (f) is round 1's F7 text with F21's insertion composed at exactly the instructed position; (g) and (h) character-exact. Lettering runs (a)–(j) as F7's implementation note required. |
| F8 | REC | Replace 16.3 with addressed notices + deemed-receipt rules | cl 16.3 | **AC** | Character-exact, including the four `[●]` address fields (expected — completion is §A6 item 10, a signing item, not a drafting item). |
| F9 | REC | Insert definitions of "working day" and "material" as new 1.3 | cl 1.3 | **AC** | Character-exact. Clause 1 heading updated to "Sale and purchase; interpretation" — consequential, appropriate. |
| F10 | REC | Limit set-off in 15.1 to "clauses 2.2(b) and 2.2(c)" | cl 15.1 | **AC** | Exact. Contradiction with cl 2.3 eliminated. |
| F11 | REC | Insert contemporaneous-completion mechanic as new 3.3 | cl 3.3 | **AC** | Character-exact. Gwin's defective 24-hour/sole-discretion mechanic confirmed **not** reinstated. |
| F12 | REC | Background E and cl 1.2: "clauses 10 to 14" → "clauses 10 to 13"; add the individual-obligation carve-out in 1.2 | Background E; cl 1.2 | **AC** | Both exact. Grep of the full v2 text confirms **no instance of "clauses 10 to 14" survives anywhere**. |
| F13 | REC | Delete the three bracketed "[Execution block: …]" annotations and the entire Drafting Notes section; retain the draft banner | Execution section; end of document | **AC** | Diff confirms all three annotations and Drafting Notes 1–7 removed in full; no note content leaked into any clause. "DRAFT FOR LEGAL REVIEW — NOT FOR EXECUTION" banner retained, correctly. |
| F14 | BLOCKER | Insert survival clause as new 16.5 with the 6.1(b) re-transfer exception | cl 16.5 | **AC** | Character-exact to round 1's wording. (The wording itself has a composition gap round 1 authored — the omission of 15.3 from the survival list — raised as new finding N1, not as an application failure.) |
| F15 | REC | Replace 9.2 (obligation, not intention; sign by settlement; employment-only content); add record as deliverable 3.1(i) | cl 9.2; cl 3.1(i) | **AC** | Both character-exact, including the no-restatement-of-restraints sentence F16 depends on. |
| F16 | REC | Add vendor-capacity anchor to end of 10.5 | cl 10.5 | **AC** | Character-exact. |
| F17 | REC | 15.1: add irremediable-breach immediate path + stated estimation basis | cl 15.1 | **AC** | Both insertions exact and at the instructed positions. |
| F18 | REC | Add pre-emption waiver/confirmation deliverable as 3.1(j) | cl 3.1(j) | **AC** | Character-exact. |
| F19 | REC | Add covenantor-style joinder mechanics to end of 1.2 (instrument, scope, title warranty) | cl 1.2 | **AC** | Character-exact, including the 4.1(a)/4.1(b) warranty pass-through and the body-corporate capability limit. |
| F20 | REC | Insert mutual prompt-and-accurate notification covenant as new 14.3 | cl 14.3 | **AC** | Character-exact. Clause 14 heading updated to "Regulatory cooperation and communications" — consequential, appropriate. |
| F21 | OPT | In 3.1(f), name IP and domain/registrar/hosting accounts after "banking and social media accounts of the Companies" | cl 3.1(f) | **AC** | Inserted verbatim at exactly the instructed anchor point. |
| F22 | OPT | Optional unpaid, questions-only, no-attendance handover as new 9.3 — "only if instructed" | cl 9.3 | **AC** | Included, character-exact. Its inclusion is an election the round-1 wording contemplated; the clause is the *maximum* round 1 recommended (no payment, no site attendance, 10 working days) and imports none of the precedents' remuneration mechanics. No concern. |
| F23 | BLOCKER | Insert set-off/default firewall as new 15.3 | cl 15.3 | **AC** | Character-exact, including the five-working-day post-determination cure and the bar on clause 6.1 notices and cancellation. |
| F24 | REC | Insert pre-settlement conduct covenant and no-prior-diversion warranty as new 4.3 and 4.4 | cl 4.3; cl 4.4 | **AC** | Both character-exact. Clause 4 heading updated to "Warranties and pre-settlement conduct" — consequential, appropriate. |
| F25 | OPT | No change: retain the 12-month staff lookback in 11.1(b) as a recorded intentional asymmetry | cl 11.1(b) | **AC (no change required)** | "twelve (12) months" retained. The asymmetry stands as a decision, not drift. |

## B3.2 Divergence detail

**(a) F2 — clause 14.4's parenthetical (beneficial, pre-authorised).** Round 1's suggested wording opened: *"Nothing in this agreement (including clauses 10 to 13) prevents…"*. The v2 text reads: *"Nothing in this agreement (including clauses 4.3, 4.4 and 10 to 13) prevents…"*. Every other word of the clause — the full regulator list, "whether or not the communication is required by law", and the closing "or grounds for set-off under clause 15" — is character-identical. This divergence is not merely acceptable; it is the specific improvement round 1's regulatory-integrity backstop described: *"adding '(including clauses 4.3, 4.4 and 10 to 13)' to F2's wording is a one-word-cost improvement the settling solicitors may make."* Its effect is that the pre-settlement conduct covenant (4.3) and the no-prior-diversion warranty (4.4) — the two new clauses that restrain the Vendor's conduct *before* settlement — are expressly subordinated to the regulator-communications carve-out. **Verdict: divergence is correct and materially strengthens the regulatory-integrity posture. No action.**

**(b) F5 — clause 11.1(a)'s consequential tidy (immaterial).** Round 1 instructed the 11.2 definition and the 10.1(b) simplification, and said of 11.1(a): "rely on the defined term (no further change needed)." The drafter nonetheless made two micro-edits in 11.1(a): v1's *"the diversion of any client of either Company"* became *"the diversion of any client"*, and v1's *"accept the custom of any such client"* became *"accept the custom of any client"*. Both edits are consistent with — indeed required for clean drafting under — the new defined term, which already embeds "either Company" and the 24-month lookback; retaining the old words alongside the definition would have been redundant and arguably created a narrower parallel meaning. One substantive consequence checked: v1's "any *such* client" tied the acceptance limb back to the diversion limb's client; v2's "any client" ties it to the 11.2 definition directly — same class, cleaner. **Verdict: divergence is immaterial and mildly beneficial. No action.**

**(c) Consequential heading edits (immaterial).** Four headings changed without instruction: cl 1 "Sale and purchase; **interpretation**" (for new 1.3); cl 4 "Warranties **and pre-settlement conduct**" (for new 4.3–4.4); cl 14 "Regulatory cooperation **and communications**" (for new 14.4); cl 16 "~~Further assurances; general~~ **General**". All four accurately describe the amended contents; none has operative effect. **No action.**

## B3.3 Diff audit — confirmation of no unauthorised edits

Every hunk in the v1 → v2 diff was attributed to a finding: Background E (F12); cl 1 heading and 1.2–1.3 (F9, F12, F19); 3.1(e) punctuation (consequential relettering under F7/F15/F18); 3.1(f)–(j) (F7, F21, F15, F18); 3.3 (F11); cl 4 heading, 4.3–4.4 (F24); 9.2 (F15); 9.3 (F22); 10.1(a) (F4); 10.1(b) (F5); 10.4(b) (F3); 10.5 (F16); 11.1(a) (F5 consequential); 11.1(c) (F2); 11.2–11.3 (F5, F6); 12.1 (F2); cl 14 heading, 14.3–14.4 (F20, F2); 15.1 (F10, F17); 15.3 (F23); cl 16 heading, 16.3 (F8); 16.5 (F14); execution annotations and Drafting Notes deleted (F13). **Residue: zero.** No number, date, party, warranty, remedy or restraint was altered other than as a finding instructed. In a deal where the Vendor knows the template and will read every departure, this matters: the change-set the Purchaser's solicitor must justify is exactly the round-1 findings list, nothing more.

---

# B4. Part 2 — Cross-Reference Audit After Renumbering

## B4.1 The nine danger points from the round-1 renumbering note

| # | Reference | v2 text | Resolves to | Result |
|---|---|---|---|---|
| 1 | cl 2.3 → cl 15 | "subject to the Purchaser's right of set-off in clause 15" | cl 15 Set-off | **PASS** — and 2.3's limitation to 2.2(b)/(c) now agrees with 15.1 (F10) |
| 2 | cl 3.1(e) → cl 9 | "any final pay referred to in clause 9" | cl 9 Employment and engagement (final pay in 9.1) | **PASS** (same reference in cl 3.2 also passes) |
| 3 | cl 12.1(a) → cl 14.4 | "as made to any regulator in accordance with clause 14.4" | cl 14.4 regulator-communications carve-out | **PASS** |
| 4 | cl 15.3 → cl 17 | "an arbitrator appointed under clause 17" | cl 17 Dispute resolution (appointment mechanics in 17.1(c)) | **PASS** |
| 5 | cl 16.5's clause list | "Clauses 4, 5, 8, 12, 13, 14, 15.2, 16 and 17… Clauses 10 and 11… clause 6.1(b)" | All exist and are the intended provisions | **PASS as references** — but the list has a content omission (15.3) → new finding **N1** |
| 6 | cl 10.5's references | "periods in clause 10.2 and areas in clause 10.3"; "clauses 10 and 11"; "clause 9" | 10.2 Restraint Period cascade; 10.3 Restraint Area cascade; cl 9 employment | **PASS** |
| 7 | cl 11.2–11.3 | 11.2: "In clauses 10 and 11"; 11.3: "clause 11.1", "clause 10.5" | All resolve; 11.3's severance import of 10.5 lands on the right clause | **PASS** |
| 8 | cl 14.4's clause list | "(including clauses 4.3, 4.4 and 10 to 13)"; "set-off under clause 15" | 4.3 conduct covenant; 4.4 no-prior-diversion warranty; 10–13 restraint/non-solicit/confidentiality/non-disparagement; 15 set-off | **PASS** — the carve-out reaches every clause capable of touching regulator communications |
| 9 | cl 17.1(c) | "an injunction to enforce clauses 10 to 13" | The four protective clauses; cl 14 deliberately excluded | **PASS** — exclusion of 14 remains intentional and correct |

## B4.2 Full-document sweep (every other internal reference)

| Location | References | Result |
|---|---|---|
| cl 1.2 | clauses 10 to 13 (×2); clause 3; clauses 4.1(a), 4.1(b) | PASS — 4.1(a)/(b) are the title and authority warranties, exactly what a trustee joinder must pass through |
| cl 2.2 | "working day" | PASS — defined in 1.3, which precedes it |
| cl 3.1 opening | clause 2.2(a) | PASS — the $100,000 settlement payment ("receipt by the **Vendor**" — ProHost's inverted-condition defect confirmed still absent) |
| cl 3.1(i) | clause 9.2 | PASS |
| cl 3.3 | clauses 2.2(a), 3.1, 5, 6, 7 | PASS — the no-default protection names the right remedy clauses |
| cl 4.3 | clause 13.2; clause 3.1(f) | PASS — announcement coordination and systems-freeze both land correctly |
| cl 4.4 | clause 4.3(b) (×2); clause 3.1 | PASS |
| cl 6.1 | clause 5 | PASS |
| cl 8.2 | "subject to… clause 4" | PASS — warranty claims survive the mutual release |
| cl 9.2 | s 149 ERA 2000; clauses 10 to 13 | PASS — restraints excluded from the employment record, as F16 requires |
| cl 10.1 | Restraint Period (10.2); Restraint Area (10.3) | PASS — in-clause forward use, cleared in round 1 |
| cl 10.4 | clause 10.1(a) (×2) | PASS |
| cl 11.1(a) | "Restrained Business" | PASS — defined in 10.1(a) |
| cl 15.1 | clauses 10, 11, 12, 13; clause 4; clause 5; clauses 2.2(b), 2.2(c) | PASS as references (see N2 on the clause-4 limb's content) |
| cl 15.2 | clause 5 | PASS |
| cl 15.3 | clause 15.1 (×3); clause 17; clauses 5 and 6; clause 15.2; clause 6.1 | PASS |
| cl 16.5 | clause 6.1(b) | PASS — the re-transfer exception cites the Vendor's cancellation limb, correctly |
| Execution | clause 1.2 | PASS — the conditional Lockhart block cites the joinder clause |

**Conclusion: 100% of internal references resolve to the intended provisions. No dangling, transposed or stale reference exists in v2.** The renumbering was executed cleanly.

---

# B5. Part 3 — New-Defect Sweep (defects introduced by the amendments themselves)

The sweep read the twelve new or substantially rewritten provisions (1.3, 3.1(f)–(j), 3.3, 4.3–4.4, 9.2–9.3, 11.2–11.3, 14.3–14.4, 15.1, 15.3, 16.3, 16.5) against each other and re-walked the round-1 enforcement-path traces with the new clauses in place. Five findings, none BLOCKER. All are composition defects — each round-1 wording is faithfully applied; the defects live in the joints between them. Numbering continues from round 1 as N1–N5.

---

### N1 — [RECOMMENDED] — cl 16.5 ↔ cl 15.3 — the survival clause preserves the true-up (15.2) but not the firewall (15.3), partially re-opening BLOCKER F23 in the post-cancellation window

**Issue.** Clause 16.5 (from F14) lists "Clauses 4, 5, 8, 12, 13, 14, **15.2**, 16 and 17" as surviving cancellation. Clause 15.3 (from F23) — the provision that makes a withheld amount *not due* and the Purchaser *not in default* pending arbitral determination, and that bars the Vendor from cancelling over a withheld amount — is not in the list. F14's wording was drafted in round 1 before F23's 15.3 existed as a clause number, and the list was never updated: a pure composition artifact. The vice is *expressio unius*: because 16.5 reaches into clause 15 and expressly selects 15.2, an arbitrator can infer that 15.3's omission was deliberate. Failure scenario: the Purchaser withholds the 1 October instalment under 15.1; the Vendor identifies (or manufactures) a separate Purchaser default, serves a clause 6.1 notice on it, and purports to cancel under 6.1(b); she then argues that cancellation discharged 15.3 prospectively — while clause 5 (interest) and 15.2 (repayment with interest) *expressly* survive — so the withheld amount was due all along, interest runs against the Purchaser, and her cancellation-over-the-withheld-amount bar has evaporated. The bootstrap is circular (15.3 forbids the very cancellation she relies on to escape 15.3), and the accrued-rights sentence of 16.5 gives the Purchaser a counter-argument — but F23 was rated BLOCKER precisely because this Vendor knows the pressure points, and the fix costs one line. The asymmetry as drafted is exactly backwards for the paying party: the clauses that make the Purchaser pay survive; the clause that protects him while he lawfully withholds does not.

**Fix (one edit in clause 16.5).** Replace:

> Clauses 4, 5, 8, 12, 13, 14, 15.2, 16 and 17 survive settlement and any cancellation of this agreement.

with:

> Clauses 1.3, 4, 5, 8, 12, 13, 14, 15.2, 15.3, 16 and 17 survive settlement and any cancellation of this agreement.

(Adding **1.3** is the same-edit tidy: "working day" and "material" are used inside surviving clauses 15.3, 16.3 and 15.1. Definitions are not obligations and would almost certainly be read as informing surviving clauses anyway, but listing 1.3 forecloses the argument at zero cost.)

**Regulatory-integrity check:** clause 14 (including 14.4) already survives; this fix touches nothing regulator-facing. Clear.

---

### N2 — [RECOMMENDED] — cl 15.1 ↔ cl 4.3/4.4 — the set-off trigger does not cleanly reach the new pre-settlement conduct protections

**Issue.** Round 1's design intent (stated in §D6, F24) was that the 4.4 warranty "convert[s] suspicion into a clean set-off trigger under clause 15.1's reference to amounts due under clause 4". Walked against the final text, that path is weaker than intended. Clause 15.1 has two limbs: (i) "material breach of clauses **10, 11, 12 or 13**" — which lets the Purchaser withhold his own *reasonable estimate* of loss; and (ii) "any amount **due and payable** by the Vendor to the Purchaser under clause 4 or clause 5". A breach of the 4.3 conduct covenant or a false 4.4 warranty sounds in unliquidated damages — and unliquidated damages are not "due and payable" until quantified by agreement or award. So for exactly the breaches most likely to occur *first* (pre-settlement diversion and data-taking, discovered after settlement), the Vendor's answer to a set-off notice is: "no amount is yet *due and payable* under clause 4, and clause 4 is not in the material-breach limb — you had no right to withhold." The estimate-based limb should name the two new clauses. Failure scenario: in late August 2026 the Purchaser discovers the Vendor exported the client list in July (breaching 4.3(b) and falsifying the 4.4 certificate); he withholds part of the 1 September instalment; the Vendor invokes the gap, characterises the withholding as outside 15.1, and — but for 15.3 — a default; the Purchaser's strongest evidence-backed protection turns on a pleading point.

**Fix (one edit in clause 15.1).** Replace:

> If the Vendor is in material breach of clauses 10, 11, 12 or 13,

with:

> If the Vendor is in material breach of clause 4.3 or 4.4 or of clauses 10, 11, 12 or 13,

(The "amounts due under clause 4 or clause 5" limb remains for liquidated amounts; the materiality threshold in 1.3 applies to the new limb, keeping trivial breaches out of the set-off.)

**Regulatory-integrity check:** clause 14.4 expressly provides that no regulator communication "is a breach of this agreement or grounds for set-off under clause 15", and expressly covers clauses 4.3 and 4.4 — so extending the set-off trigger to 4.3/4.4 cannot reach any regulator-facing conduct. Clear.

---

### N3 — [RECOMMENDED] — cl 11.2 ↔ cl 4.3/4.4 — the "client" definition does not extend to the pre-settlement protections, leaving them exposed to the exact narrow reading F5 closed elsewhere

**Issue.** Clause 11.2 opens "In clauses **10 and 11**, client means…", so its wide, venue-and-head-contractor-inclusive definition does not apply to clauses 4.3(a) ("discuss the sale… with any client") or 4.4(a) ("has not solicited… any client"). F5 (the definition) and F24 (clauses 4.3/4.4) were drafted in parallel in round 1 and never coordinated — another composition artifact. Consequence: in the pre-settlement window, "client" reverts to its natural meaning, and the Vendor can run the argument F5 was written to kill — that a venue or site operator serviced under a hospitality operator's head contract is not a "client of either Company". For this group that is not hypothetical: the ProHost precedent's entire conditional structure (its clause 7 consent condition naming Star Hospitality Group, Lime Investments, Florrie McGreals and Bar101) shows the client relationships run through hospitality operators. The 4.4 warranty is a designed set-off trigger (and becomes a cleaner one under N2); its protected class should not be narrower than clause 10's and 11's.

**Fix (one edit in clause 11.2).** Replace:

> In clauses 10 and 11, client means

with:

> In clauses 4.3, 4.4, 10 and 11, client means

(The definition's 24-months-before-Settlement-Date lookback reads naturally in the pre-settlement clauses: at signing it captures the current and recent client base, which is the correct protected class for both.)

**Regulatory-integrity check:** definitional only; no regulator-facing effect. Clear.

---

### N4 — [OPTIONAL] — cl 12.1(a) — "as required **or permitted** by law" is broader than its purpose now requires and invites a swallow-the-rule argument

**Issue.** Round 1's F2 wording — applied verbatim — recast 12.1(a) as "as required or permitted by law, or as made to any regulator in accordance with clause 14.4". The "or permitted by law" limb was doing regulator work in the original conception (voluntary disclosure is not "required"), but the third limb now covers *all* regulator communications comprehensively, so "permitted by law" is redundant for its purpose — and in a perpetual confidentiality clause it is the widest words in the document: a determined counterparty can argue that any disclosure not positively prohibited by law is "permitted by law". A tribunal would very likely read it contextually (as meaning disclosure under a specific legal gateway, e.g. the Protected Disclosures Act 2022), and the argument is weak — hence OPTIONAL — but the words cost more than they buy, and the two disclosure gateways the agreement itself creates (the 9.3 handover and 13.2 agreed communications) are better anchors.

**Fix (one edit in clause 12.1).** Replace:

> (a) as required or permitted by law, or as made to any regulator in accordance with clause 14.4,

with:

> (a) as required by law, as expressly permitted by this agreement, or as made to any regulator in accordance with clause 14.4,

**Regulatory-integrity check — critical for this one:** the amendment narrows a disclosure exception, so it must not narrow regulator communications. It does not: the third limb ("as made to any regulator in accordance with clause 14.4") is untouched and is itself unlimited ("whether or not the communication is required by law"). The Vendor's path to the PSPLA/CIPU is exactly as wide after this fix as before. Clear.

---

### N5 — [OPTIONAL] — cl 11.3 — "any period in clause 11.1" literally captures the 12-month staff lookback, producing an incoherent "reduction" to 18 months

**Issue.** Clause 11.3 (F6, applied verbatim) begins: "If **any period in clause 11.1** is held unenforceable, it shall be reduced to eighteen (18) months…". Clause 11.1 contains two periods: the 24-month restraint period (the cascade's intended subject) and the **12-month** staff lookback in 11.1(b) (F25's recorded asymmetry). Read literally, if the 12-month lookback were ever held unenforceable it would be "reduced" to 18 months — an *enlargement*, which is incoherent and would simply render the cascade inapplicable to that limb. No tribunal would apply it that way, and the practical risk is negligible — hence OPTIONAL — but the round-1 wording pre-dated its own coexistence with the lookback and one word fixes it.

**Fix (one edit in clause 11.3).** Replace:

> If any period in clause 11.1 is held unenforceable, it shall be reduced to eighteen (18) months;

with:

> If the twenty-four (24) month period in clause 11.1 is held unenforceable, it shall be reduced to eighteen (18) months;

**Regulatory-integrity check:** none implicated. Clear.

---

## B5.1 Interactions considered and cleared

For completeness — the candidate defects the sweep tested and rejected, so the settling solicitors do not re-plough them:

| Interaction | Assessment |
|---|---|
| cl 9.3 handover (disclose rosters, client contacts) vs cl 12.1 confidentiality | **Cleared.** Disclosure is to the Purchaser/Companies — the persons the obligation protects — at their request, under an obligation "recorded in this agreement" (cl 8.2(a)'s language). No sensible breach reading; N4's "expressly permitted by this agreement" wording removes even the pedantic one. |
| cl 4.3(a) discussion ban vs cl 13.2 agreed communications | **Cleared.** F24 built the coordination in: 4.3's opening excepts communications "in a form agreed under clause 13.2". No conflict. |
| cl 4.2 ("warranties in clause 4.1 survive settlement") vs cl 16.5 ("Clauses 4… survive settlement and any cancellation") | **Cleared.** Overlap, not contradiction; 16.5 subsumes 4.2. The solicitors may delete 4.2 as redundant if they wish; retaining it is harmless. |
| cl 2.3 "Time is otherwise of the essence" vs cl 15.3 firewall | **Cleared.** "Otherwise" already carves the set-off out of the essential-time stipulation. |
| cl 6.1 (14-day) vs cl 15.1 (7-day/immediate) notice regimes | **Cleared** in round 1 (different jobs); unchanged by the amendments, and 15.3 now governs the interface. |
| "client" used in cl 10.1(b) before its definition in cl 11.2 | **Cleared.** The definition is expressly scoped "In clauses 10 and 11" (and under N3, "4.3, 4.4, 10 and 11"), so placement does not create ambiguity — same treatment round 1 gave Restraint Period/Area. |
| cl 4.4 deletion certificate vs cl 3.1(f) delivery obligation | **Cleared.** 4.4 expressly excepts "records delivered under clause 3.1" — no double or contradictory obligation. |
| cl 14.3 mandatory filings vs cl 12.2 terms-confidentiality | **Cleared.** 12.2 expressly excepts disclosure to the Companies Office, IRD, PSPLA "or any other regulator". |
| Conditional Lockhart execution block retained | **Cleared.** This is §A6 item 5 (activate or delete at signing, per F1's resolution), not one of F13's deleted annotations. Correctly retained. |
| Defined terms audit on the new clauses | **Cleared.** "working day" (2.2, 15.3, 16.3) and "material" (15.1) → 1.3; "Restrained Business" (11.1(a)) → 10.1(a); "Shares", "Settlement Date", "Purchase Price", "Companies/Company" all defined before first use. No term is used without a definition except "client" in 4.3/4.4 (→ N3) — and no definition is used before it exists in a way that creates ambiguity. |

---

# B6. Part 4 — Deal-Term Re-Check Against `deal_facts.txt`

Field-by-field re-run of the round-1 §D1 diff against the v2 text. **Result: 22/22 match; zero drift introduced by the amendments.**

| # | Fact | deal_facts.txt | v2 location | v2 value | Match |
|---|---|---|---|---|---|
| 1 | Vendor | Nikki Wairau Christian | Parties 1; Background; execution | Nikki Wairau Christian | ✔ |
| 2 | Purchaser | Ahmad Duais | Parties 2; execution | Ahmad Duais | ✔ |
| 3 | ASG company number | 8517467 | Background A | 8517467 | ✔ |
| 4 | ASG NZBN | 9429050952960 | Background A | 9429050952960, correctly labelled NZBN | ✔ |
| 5 | ASG registered office | 7/220 Queen Street, Auckland Central 1010 | Background A | Same (+ "New Zealand" — formatting only) | ✔ |
| 6 | ASG issued shares | 10,000 ordinary | Background A | 10,000 ordinary | ✔ |
| 7 | SLS company number | 9325956 | Background B | 9325956 | ✔ |
| 8 | SLS NZBN | 9429052674921 | Background B | 9429052674921 | ✔ |
| 9 | SLS registered office | Office 2, Level 7, 220 Queen Street, Auckland Central 1010 | Background B | Same (+ "New Zealand") | ✔ |
| 10 | SLS issued shares | 10,000 ordinary | Background B | 10,000 ordinary | ✔ |
| 11 | Subject: all Vendor's shares, both companies, incl. trustee/nominee | Yes | Background D; cl 1.2 | Same words; counts still `[●]` per F1 gate | ✔ (gate) |
| 12 | Price | NZ$260,000 | cl 2.1 | NZ$260,000.00 | ✔ |
| 13 | Instalment 1 | $100,000 at settlement 1 Aug 2026 | cl 2.2(a); cl 1.1 | $100,000.00 on Settlement Date; Settlement Date = 1 August 2026 | ✔ |
| 14 | Instalment 2 | $80,000 on 1 Sep 2026 | cl 2.2(b) | $80,000.00 on 1 September 2026 | ✔ |
| 15 | Instalment 3 | $80,000 on 1 Oct 2026 | cl 2.2(c) | $80,000.00 on 1 October 2026 | ✔ |
| 16 | Sum check | $100k+$80k+$80k = $260k | cl 2.1–2.2 | $260,000.00 | ✔ |
| 17 | Settlement Date | 1 August 2026 | cl 1.1 | 1 August 2026 "or such other date agreed in writing" | ✔ |
| 18 | Lockhart entity name | Lockhart Trustee Services No.222 Limited | cl 1.2; execution block | Identical spelling both places | ✔ |
| 19 | 12% p.a. default interest | Both precedents | cl 5.1 | 12% per annum | ✔ |
| 20 | 14-day default/remedy windows | Both precedents | cl 6.1; cl 7.1 | 14 days each | ✔ |
| 21 | 2-year client restraints | Both precedents | cl 11.1 (and 10.2 top step) | 24 months | ✔ |
| 22 | Negotiation → arbitration, Arbitration Act 1996, single arbitrator, NZLS appointment | Both precedents | cl 17.1 | Identical structure, President or Vice-President appointment | ✔ |

**Placeholder census (v2) — all expected, none unexpected, none prematurely filled:** agreement date "[        ] 2026" (front page); `[●]` share counts ×2 (Background D); `$[●]` apportionment ×2 (cl 2.1); `[●]` notice addresses ×4 (cl 16.3 — new, introduced by F8 exactly as drafted; completion is §A6 item 10); conditional Lockhart execution block. The "DRAFT FOR LEGAL REVIEW — NOT FOR EXECUTION" banner is retained, correctly. The round-1 §A6 schedule of 15 completion items remains the operative checklist and is unchanged by this round except that items 6 and 7 (annotation and drafting-note deletion) are now **done**.

---

# B7. Part 5 — Regulatory-Integrity Confirmation

Re-tested clause-by-clause on the final text against the hard constraint: nothing may conceal, transfer or release personal regulatory liability, and nothing may restrain, penalise or discourage communications with the regulator during the open PSPLA → CIPU process.

| Check | v2 position | Result |
|---|---|---|
| No restraint on regulator relationships | 11.1(c): "clients, suppliers, landlords or licensors" — "or regulators" struck (F2) | **HOLDS** |
| Confidentiality permits voluntary regulator disclosure | 12.1(a) routes to 14.4; 12.2 expressly permits disclosure to Companies Office, IRD, PSPLA, any regulator | **HOLDS** |
| Non-disparagement cannot reach regulator statements | 13.1 has no internal carve-out, by design — 14.4 overrides it ("Nothing in this agreement (including clauses… 10 to 13)…") | **HOLDS** |
| Pre-settlement conduct covenant and warranty cannot reach regulator communications | 14.4's parenthetical expressly includes **4.3 and 4.4** — the round-1-invited extension, applied | **HOLDS — as intended** |
| Regulator communication can never trigger the set-off | 14.4 closing words: "…no such communication is a breach of this agreement or grounds for set-off under clause 15" | **HOLDS** (and N2's proposed extension of the set-off trigger remains subject to it) |
| No transfer or release of personal regulatory liability | 14.2 (both directions); 8.2(c) carves "personal liability of a party to a regulator or other third party" out of the mutual release | **HOLDS** |
| Consideration not expressed to buy regulatory cooperation | Background E and 1.2 now say "clauses 10 to 13"; no "10 to 14" survives anywhere in the document | **HOLDS** |
| Regulatory cooperation not enforceable by injunction | 17.1(c) carve-out remains "clauses 10 to 13" — clause 14 deliberately excluded | **HOLDS** |
| Notifications made promptly and accurately, nothing concealed | 14.3 mutual covenant (F20) — filings must not misstate or omit any material fact | **HOLDS** |
| Employment record cannot touch PSPLA processes | 9.2: record of settlement "shall relate to employment matters only" and shall not restate the restraints | **HOLDS** |
| No restraint on the Vendor's licence or certificate of approval | 10.1(a)'s list deliberately omits licence status; 10.4(b) preserves out-of-sector work | **HOLDS** |
| Carve-out survives cancellation | Clause 14 (including 14.4) is in the 16.5 survival list | **HOLDS** |
| New findings N1–N5 tested against the constraint | Each checked individually at §B5 — none narrows any regulator gateway; N4 explicitly leaves the 14.4 limb untouched | **HOLDS** |

**Confirmation: the agreement as amended conceals nothing, fetters no regulator communication, and preserves personal regulatory responsibility in both directions. Clause 14.4 reaches clauses 4.3 and 4.4 as intended.**

---

# B8. Sign-Readiness Verdict

**VERDICT: CLEARED FOR TRANSMISSION TO FRANKLIN LAW.** The v2 draft passes the final automated gate: 24/24 applicable findings applied (none NOT APPLIED), a clean diff with zero unauthorised edits, a fully-resolving cross-reference structure, exact deal-term fidelity, and an intact regulatory-integrity posture. No new BLOCKER exists. The document the solicitors receive is materially stronger than either precedent it descends from, and the change-set they must defend to the Vendor's side corresponds exactly to the round-1 findings list.

**What remains — exactly, in three tranches:**

**Tranche 1 — before transmission (drafting; minutes of work, all wording supplied at §B5):**

1. **Apply N1** (cl 16.5: add "1.3" and "15.3" to the survival list). One line. This is the only new finding whose omission hands the Vendor an argument against a BLOCKER-level protection (the F23 firewall), and it should not travel unfixed.
2. **Apply N2 and N3** (cl 15.1: add "clause 4.3 or 4.4" to the material-breach limb; cl 11.2: extend the client definition to "4.3, 4.4, 10 and 11"). Recommended; alternatively flag both in the instruction letter for the solicitors to apply — but since each is a one-edit change with wording supplied, applying now is cheaper than explaining.
3. **N4 and N5 at the Purchaser's option** (12.1(a) tightening; 11.3 cascade precision). Genuinely optional; safe to leave to the solicitors with this report.

**Tranche 2 — with transmission (the package):** this report; `ROUND1_FINDINGS.md`; the instruction-letter material per round-1 §A5 item 9 (the transplanted Drafting Notes 1–7, the §D5.3 additions-justification table, and the negotiation posture on vendor security — resist guarantee and share charge; escrow of the final $80,000 as fallback); and the source documents.

**Tranche 3 — before signing (factual and external; gates signing, not transmission — unchanged from round 1):**

4. **The F1/Lockhart gate — still the single blocker to signing.** Confirm from trust records whether the 1,524-share parcels are the Vendor's beneficial stake; if yes, complete Background D at 1,525 shares per company, join the trustee under the cl 1.2 mechanics and activate its execution block; if no, do not sign — subject matter and price must be re-established. Nothing in v2 has, or could have, resolved this on paper.
5. The remaining round-1 §A6 items: agreement date; cl 2.1 price apportionment (accountant); notice addresses in 16.3; constitutions/shareholders'-agreement review and pre-emption waivers (Nabawi 40.16%, Lockhart 15.24%); current register extract confirming 10,000 issued shares; MBIE mediator booked against 1 August 2026 for the s 149 record; PSPLA notification advice (14.3 then operates); vehicle/chattels factual check; Vendor's bank-account nomination by 30 July 2026; banner removed only at execution.
6. **Process item for the deal team:** repair the corpus builder before any further automated round — this round's compiled corpus omitted the draft under review and the deal-facts sheet entirely (see §B1 warning). Automated verification is only as good as what it is allowed to read.

**Bottom line for the Purchaser:** make the one-line N1 edit (and preferably N2/N3), and send the package. The draft is done as a drafting exercise; from here the open risks are factual (Lockhart), external (waivers, mediator, regulatory advice) and negotiational (the Vendor knows this template and will probe clauses 10 and 15 hardest) — all of which now sit exactly where they should: in front of the solicitors, with the reasoning attached.

---

*This report is the round-2 verification pass of a pre-lawyer hardening review. It is not legal advice. The final document is to be settled by the parties' solicitors, who should receive both rounds' reports, the instruction-letter material identified in round-1 §A5.9, and the source documents.*
