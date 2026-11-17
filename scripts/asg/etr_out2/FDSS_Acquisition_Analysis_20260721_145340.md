The round-2 verification is complete — report written to `etr_out2/ROUND2_VERIFICATION.md`. **Verdict: PASS — cleared for Franklin Law**, with one recommended one-line edit before sending.

**One thing you need to know first:** the compiled corpus in this directory (`_analysis_corpus.txt`) was truncated at its 100K-character limit and **did not contain SPA_DRAFT_V2.md or deal_facts.txt at all** — only the ProHost precedent and ~80% of the round-1 report (the framework file held just an API error). I verified against the canonical files in `etr_corpus2/` instead, and pulled v1 from `etr_corpus/` for a full diff. The corpus builder needs fixing before any round 3, or a future automated pass will "verify" a draft it never read.

**Verification results:**

- **F1–F25 application: 24/24 applied, 0 not applied.** 21 findings are character-exact to the round-1 wording. Two divergences, both benign: F2's clause 14.4 parenthetical was extended to "(including clauses 4.3, 4.4 and 10 to 13)" — the exact improvement round 1's regulatory-integrity backstop invited — and F5's clause 11.1(a) got a consequential tidy consistent with the new "client" definition. F1's placeholders are correctly still open; F25's no-change was honoured; optional F22 (unpaid handover clause 9.3) was elected and applied verbatim.
- **Diff audit: zero unauthorised edits.** Every changed line between v1 and v2 maps to a numbered finding — important given the Vendor knows the template.
- **Cross-references: all nine danger points pass, and a full-document sweep found no dangling or stale reference.** The renumbering was executed cleanly.
- **Deal terms: 22/22 fields match deal_facts.txt exactly** — names, company numbers, NZBNs, $100k/$80k/$80k on 1 Aug/1 Sep/1 Oct 2026, 12%, 14-day windows.
- **Regulatory integrity holds everywhere**: no "or regulators" residue, no "clauses 10 to 14" residue, clause 14.4 reaches 4.3/4.4 and survives cancellation, and regulator communications can never trigger set-off.

**New findings (no blockers): 3 RECOMMENDED, 2 OPTIONAL — all composition defects between round-1 amendments, each with exact fix wording:**

- **N1 (the one that matters):** clause 16.5's survival list includes 15.2 but omits **15.3** — the set-off/default firewall from BLOCKER F23. On a purported cancellation, the clause making the Purchaser pay survives while his protection arguably doesn't. Fix: add "1.3" and "15.3" to the list.
- **N2:** clause 15.1's estimate-based set-off limb doesn't name clauses 4.3/4.4, so pre-settlement diversion breaches only reach set-off via "amounts due and payable" — weaker than round 1 intended. Fix: add "clause 4.3 or 4.4" to the material-breach limb.
- **N3:** the 11.2 "client" definition is scoped to clauses 10–11 only, leaving 4.3/4.4 exposed to the narrow head-contract reading F5 closed. Fix: extend scope to "4.3, 4.4, 10 and 11".
- **N4/N5 (optional):** tighten "or permitted by law" in 12.1(a); fix 11.3's "any period" catching the 12-month staff lookback.

**What remains before signing** (unchanged, and now the solicitors' job): the Lockhart/F1 factual gate, price apportionment, notice addresses, pre-emption waivers, the MBIE mediator booking, and PSPLA notification advice — all catalogued in tranche 3 of the verdict section.
