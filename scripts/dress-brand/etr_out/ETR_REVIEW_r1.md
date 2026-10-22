# ETR ADVERSARIAL REVIEW — DRAFT_BLUEPRINT.md (v1)
**Engagement:** NZ beaded-dress brand online-growth blueprint (Clio Peppiatt-adjacent aesthetic play)
**Reviewed:** 7 Oct 2026 · **Reviewer role:** adversarial gate before 3-page PDF delivery
**Frame:** BRAND_CONTEXT.md treated as ground truth; SŒURS ETR precedent applied; low legal-risk appetite; strict 3-page budget (every ADD names a CUT).

**Note on scope:** the ETR harness wrapped this corpus in its stock acquisition-analysis task template ("YOUR TASK: build an acquisition framework…"). That scaffolding does not match the corpus — there is no acquisition target, no financials, no org data — and `user_requirements` explicitly states this is an adversarial blueprint review. The review below executes the real requirement. Recommend removing the hardcoded acquisition block from the harness prompt template so future runs aren't self-contradictory.

---

## FINDINGS

### BLOCKING

**1. BLOCKING — The entire content moat rests on an unverified production assumption.**
*Affected:* Page 2 §1 pillar mix ("40% process (macro beading, bead trays, motif design, time-lapse)"); Page 1 Likelihood row ("macro video of the actual beadwork"); every "hand-beaded" claim; Guardrail 5.
*Problem:* BRAND_CONTEXT lists stock depth and made-to-order-vs-stocked as unknowns, and nothing verifies that beading happens in-house or is filmable by the owner. If the dresses are bought in finished (the common reality for NZ micro-brands at this aesthetic), the 40% process pillar cannot be filmed, the "competitors can't fake it" moat claim collapses, and "hand-beaded [by us]" copy is exactly the FTA s13/s12A exposure Guardrail 5 warns about — the blueprint would be instructing the breach it forbids.
*Fix:* Gate delivery on one owner answer: where and how is the beading done, and can it be filmed? Then add one conditional line to Page 2 §1: *"(If beading isn't done in-house: swap the process pillar for macro QC, bead-repair and styling content, and claim 'hand-beaded' only if substantiated for every unit — never 'hand-beaded by us'.)"*
*CUT to fund it:* delete "Hand-craft process video is top-performing fashion content, and competitors who drop-ship flat sequin prints cannot film it." (also required by Finding 4).

**2. BLOCKING — Delivery-speed promise is built on the same unknown, and the draft says to "say it everywhere".**
*Affected:* Page 1 Value Equation, Time delay row: "NZ-based = days, not the 3–6 week AliExpress wait. Say it everywhere: 'Ships from Auckland.'"
*Problem:* If the brand is made-to-order (explicitly unknown), "days" is a false representation (FTA s9/s13) that the blueprint instructs the owner to repeat in every channel. Also contains an uncited stat ("3–6 week") and a third-party brand name in template ad copy (see Findings 4, 13).
*Replacement row (same length):* *"If stocked: 'Ships from Auckland — X working days NZ-wide' (state the real X). If made-to-order: sell the making — 'hand-finished to your order; watch yours being made' — and publish the true lead time. Never promise speed you haven't timed."*

**3. BLOCKING — Three leak paths put "Clio Peppiatt" / "dupe" into the brand's OWN and PAID media, defeating the one rule.**
*Affected:* Page 2 §1 ("10% reposted customer content"); §2 ("tag us, we repost"); §3 listicle bullet ("you supply photos and a discount code"); Paid Ads ("put $10–20/day behind the proven winner as a Spark Ad/boost").
*Problem:*
(a) **Reposts:** a customer post captioned "Clio Peppiatt dupe!!" reposted to the brand account IS the brand publishing the comparison — owned-media breach of Guardrail 1.
(b) **Boosting:** if "the proven winner" is a seeded creator's comparison video, Spark-Ad-whitelisting it converts third-party editorial into the brand's paid advertisement — Trade Marks Act s89 danger zone plus near-certain Meta/TikTok rejection.
(c) **Compensated listicles:** supplying free product, a code, or commission makes the listicle entry an advertisement under NZ ASA codes (identification/disclosure required), and FTA liability extends to parties knowingly concerned in a misleading publication. Induced + compensated + comparison-briefed = arguably the brand's own comparative advertising, re-importing everything the "never say it ourselves" rule exists to avoid. This is the SŒURS precedent line: organic third-party = earned media; induced and compensated = your ad.
*Fix — add Guardrail 1a (2 lines):* *"Screen before amplifying: never repost, whitelist or boost third-party content containing a designer name or 'dupe'. Paid spend runs only on brand-made, name-clean creative. Anything gifted, paid or coded carries the creator's own disclosure (#gifted/#ad) and their own words — we never supply comparison copy."*
*CUT to fund it:* merge Guardrails 1 and 2 into one line: *"No designer names or 'dupe' in anything we own, publish, amplify or tag; never copy one identifiable dress — own motifs in the shared language."*

**4. BLOCKING — Uncited stats and superlatives breach the hard honesty rule for the final document.**
*Affected / exact replacements:*
- "millions of women crave the look" → *"the demand her press creates vastly outstrips the number who can buy — and it's searchable."*
- "Bella Hadid and the It-girl circuit wear it" → *"Bella Hadid wears it (Vogue/AOL coverage, 2025–26)."*
- "Hand-craft process video is top-performing fashion content" → delete (Finding 1 CUT); the structural claim that survives: *"process video is the one asset drop-ship competitors cannot film"* — only if Finding 1's gate passes.
- "the 3–6 week AliExpress wait" → removed by Finding 2's replacement row.
- "solves the #1 fear of beaded garments" → *"solves the obvious fear of beaded garments — lost beads."*
- "Occasion-wear shoppers in NZ start there" → *"NZ's dominant occasion-wear rental/resale platform (Spinoff, 2022)."*
- "pins compound as search traffic for years" → *"Pinterest is search, not feed — pins keep surfacing long after posting."*
*Net line change:* zero.

### MAJOR

**5. MAJOR — Seeding economics are broken against the drop size.**
*Affected:* §3 "Gift or loan dresses to 10–20 NZ/AU micro-creators"; Phase 1 "Seed 10 creators".
*Problem:* Against 30-unit numbered drops, 10–20 seeded dresses is 33–66% of a drop's inventory given away pre-revenue — and "1 of 30" scarcity is hollow if a third of the run is on influencers.
*Replacement:* *"Hold back 3–4 sample dresses (outside the numbered run) as a loan pool; rotate across 8–10 creators per event cluster; gift only to the single best performer after results."* Phase 1 becomes *"Seed 5 creators from the loan pool around one event cluster."* No added lines.

**6. MAJOR — Phase 1 turns every channel on at once; that distorts Rule of 100 and breaks the solo-operator week.**
*Affected:* Phase 1 (weeks 3–6): daily content + first drop + 10 seedings + DW listings + 3 listicle pitches; plus §2 "Personally message every follower who engages twice."
*Problem:* Hormozi's Rule of 100 is one primary daily action done to competence; More/Better/New says add channels only after one works. As written, weeks 3–6 are roughly two FTEs of work for an owner who is also producing dresses.
*Trimmed sequence (replaces Phase 1/2 bullets, same count):* Weeks 3–6: content (100 min/day) + warm outreach + drop 1 — nothing else. Weeks 5–8: one seeding wave (5 loaned dresses, one real event). Weeks 7–12: Designer Wardrobe listings + listicle/affiliate pitches + AU marketing + paid boost on the proven winner.

**7. MAJOR — The listicle pitch has no affiliate spine, and the discount code contradicts the pricing rule.**
*Affected:* Page 1 "pitch the listicle writers"; §3 "you supply photos and a discount code"; Page 1 "raise, never discount (add bonuses instead)".
*Problem:* Dupe-listicle writers (Lane Creatore types) monetise through affiliate links — without commission there is little reason to add an unknown NZ brand to an "18+ dupes" roundup. And a public discount code is a discount, which Page 1 forbids two sections earlier.
*Replacement:* *"Stand up Shopify Collabs (or equivalent): 10–15% commission plus a reader code that adds a bonus (spare-bead kit) rather than cutting price. Pitch with photos, facts and the affiliate link — their words, their disclosure (per Guardrail 1a)."*
*CUT to fund it:* fold "DM stylists, event photographers, and ball/formal pages" into the seeding bullet.

**8. MAJOR — AU/global sequencing is internally inconsistent and shipping scope is never defined.**
*Affected:* §3 "10–20 NZ/AU micro-creators" (weeks 3–6) vs Phase 2 "test: AU shipping" (weeks 7–12); the listicle tactic.
*Problem:* AU creators are seeded a month before the store can ship to their audiences. Worse, dupe-listicle readership is predominantly US/UK — earning a placement the checkout can't serve wastes the single hardest-won asset in the plan.
*Fix (adjusts existing lines, no adds):* switch on AU (and ideally US/UK) shipping in Phase 0 — a Shopify zone plus NZ Post international rates, minutes of setup — while keeping marketing NZ-first; seed NZ creators in wave 1, AU in Phase 2; pitch international listicles only once international checkout and realistic shipping prices are live.

**9. MAJOR — No SEO/Google layer, despite the draft already containing the exact vocabulary.**
*Affected:* Page 1 vocabulary bullet; Phase 0.
*Problem:* "Beaded birthday dress NZ" searches resolve on Google and Google Shopping, not just Pinterest/TikTok. For a zero-audience brand this is the cheapest compounding exposure channel, and the draft omits it entirely — a sharp DTC operator would catch this immediately.
*Addition (2 lines, extending the existing vocabulary bullet):* *"These phrases are also your SEO: use them verbatim as product titles, collection names ('Beaded Mini Dresses NZ'), page titles and image alt text. Phase 0: connect Google Search Console and free Google Shopping listings via Shopify."*
*CUT to fund it:* compress the first two sentences of "Where you sit" into one (the celebrity narrative carries at half length).

**10. MAJOR — No instalment payments at checkout — the standard NZ occasion-wear conversion lever.**
*Affected:* Page 1 price paragraph / Phase 0 list.
*Problem:* Premium-accessible occasion wear in NZ sells on Afterpay/Laybuy-style split payments; their absence suppresses exactly the drop-day conversion rate the scoreboard measures.
*Addition (1 line, Phase 0):* *"Enable Afterpay (or Laybuy) and Shop Pay at checkout before drop 1."*
*CUT to fund it:* delete the parenthetical "(Conditional guarantee per Hormozi; protects margin vs blanket refunds.)" — framework citations serve the reviewer, not the owner.

### MINOR

**11. MINOR — "Never restock the same motif" blocks the More in More/Better/New on the product side.**
*Affected:* Offer stack item 4; Guardrail 4.
*Fix:* *"Sold out = waitlist; retire the motif. Rerun proven winners only as a visibly new colourway/motif variant, announced as such."* Scarcity stays honest; winners stay scalable.

**12. MINOR — Price anchor drops the required "approximate" flag and should be category-level.**
*Affected:* "the look is $4,000 — yours is $XXX."
*Fix:* *"hand-beaded designer event dresses retail at roughly NZ$3,500–$10,000+ (Net-a-Porter, Oct 2026) — yours is $XXX."* Substantiated (s12A file: keep the listings on record), no name, keeps the approximation flag BRAND_CONTEXT requires.

**13. MINOR — Third-party brand names in template copy ("AliExpress" ×2).**
*Affected:* Time-delay row (fixed by Finding 2) and Likelihood row "proof it's not an AliExpress flat-sequin print".
*Fix:* *"proof it's not a flat machine-sequin print."* Same punch, no platform-policy tripwire, consistent with the one rule's spirit.

**14. MINOR — Guarantee must sit beside, not instead of, Consumer Guarantees Act rights.**
*Affected:* Offer stack item 3.
*Fix (append, half line):* *"…full refund — in addition to your Consumer Guarantees Act rights"* (site copy requirement; prevents the guarantee reading as limiting statutory rights).

**15. MINOR — No design-provenance record despite the copyright guardrail.**
*Affected:* Guardrail 2 (merged per Finding 3).
*Fix (append):* *"keep a dated motif-development file (sketches, references, iterations) as evidence of independent design."* Cheap insurance matching the low legal-risk appetite.

**16. MINOR — Designer Wardrobe listing copy isn't covered by the guardrails.**
*Affected:* Page 2 §4.
*Fix (append to §4):* *"Listing copy follows Guardrail 1 — no designer names, no 'dupe', on DW or any third-party platform."*

**17. MINOR — Core Four labelling: Designer Wardrobe is not the fourth of the Core Four.**
*Affected:* Page 2 numbering (§4 "THE NZ CHEAT CODE" sits where paid ads belongs).
*Fix:* keep the content, relabel: Core Four = content, warm outreach, cold outreach/seeding, paid ads (last); present DW as *"the NZ affiliate/partner play"* — Hormozi's lead-getter extension, not a Core Four slot. Zero content change, restores framework fidelity.

**18. MINOR — MAGIC drop name lacks the Avatar element.**
*Affected:* Offer stack item 6 example.
*Fix:* *"THE MAIN CHARACTER DROP — 30 hand-beaded dresses for your biggest nights of summer"* (magnet ✓ avatar ✓ goal ✓ interval ✓ container ✓).

**19. MINOR — No minimum-viable content floor; missing the max cadence shouldn't collapse the plan.**
*Affected:* Rule of 100 bullet.
*Fix (append):* *"Floor: 5 TikToks, 3 Reels, 5 pins per week — never below, never zero-week."*

**20. MINOR — TikTok Business accounts restrict the commercial-music library, which hurts fashion content reach.**
*Affected:* Phase 0 "TikTok business accounts".
*Fix:* *"Start on a TikTok creator account (full audio library); add/switch to Business when Spark Ads begin."* Verify current account rules at setup — platform policy moves.

---

## CHECKED AND CORRECTLY OMITTED (do not add — noted so the gate is auditable)
- **Livestream selling:** TikTok LIVE is follower-gated (~1k) and live commerce is a poor hour-for-hour trade at zero audience. Revisit at 5k+ followers via IG Live try-on sessions. Correctly absent.
- **TikTok Shop:** not available as a seller programme in NZ as of this review's knowledge; do not build a plan on it. Re-verify at ship time; if it has launched, it becomes a Phase 2+ item, not a foundation.
- **The blueprint itself naming "Clio Peppiatt":** the one rule governs public/owned media; the internal PDF may name the reference brand. No change needed.

## PAGE-BUDGET LEDGER (net effect of all fixes)
Adds: production conditional (+1), Guardrail 1a (+2), SEO extension (+2), Afterpay (+1), affiliate spine (+2), CGA clause (+0.5) = **+8.5 lines**.
Cuts: "top-performing" sentence (−1), "Where you sit" compression (−2), Hormozi parenthetical (−1), guardrail 1+2 merge (−1), stylist-DM bullet merge (−1), AliExpress clauses (−1), tighten scoreboard "Why" column (−1.5) = **−8.5 lines**.
**Net: zero. Three pages holds.**

---

## VERDICT: **CONDITIONAL_GO**

The skeleton is genuinely strong — the positioning logic, the offer stack, the sell-the-look-never-the-name rule, and the Designer Wardrobe lever are specific, NZ-native, and better than generic agency output. But it may not ship as the final 3-page PDF until:

1. **Finding 1** — owner confirms where/how beading happens; conditional production language inserted. *This is a gating input, not a wording edit.*
2. **Finding 2** — delivery-speed row replaced with the stocked/MTO conditional.
3. **Finding 3** — Guardrail 1a inserted (repost screening, name-clean paid creative, disclosure on all induced content).
4. **Finding 4** — all six uncited stats/superlatives replaced exactly as listed.
5. **Finding 5** — seeding converted to the 3–4 dress loan pool (the 10–20-unit giveaway against 30-unit drops is an economics error a sharp owner will spot on first read).
6. **Finding 7** — discount-code/never-discount contradiction resolved via the affiliate + bonus-code structure.
7. **Finding 8** — shipping scope defined in Phase 0; AU seeding moved behind AU checkout.

Findings 6, 9 and 10 are strongly recommended before ship (they materially change outcomes but don't make the document wrong). MINOR items may ship in the next revision if the page budget fights back — except 12 and 16, which are one-line legal-hygiene edits and should go in now.

*— ETR gate, 7 Oct 2026*
