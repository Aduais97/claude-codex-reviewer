Verification complete. The report's arithmetic is solid — every headline figure reproduces from the raw daily data, and the weekly-report reconciliation is exact (96 of 96 cells) — but I found **1 CRITICAL, 5 MAJOR and 11 MINOR** defects, almost all in the highest-risk class you flagged: window/date inconsistency, attribution, and universal claims. Full findings report saved to `REPORT_findings.md` in this directory.

One process note first: the prompt's M&A/valuation/org-analysis sections are stale template boilerplate — the corpus contains no financials, org chart or valuations, only REPORT.md and its five LCF source files, so I executed the operative instruction (the verification-and-hardening review). Also, `_analysis_framework.txt` contains only the string "Timed out after 722s…" — the upstream framework-generation step failed and wrote its error into the file; worth fixing in the pipeline.

## The one CRITICAL finding

**F-1 — The reporting window doesn't reconcile, and the totals include a pre-commencement day.** The Executive Summary frames results "Between 2 June and 24 July 2026"; the §4 table says "2 Jun – 18 Jul 2026 … across 48 days" — but 2 June to 18 July is **47 days**. The 48 logged days actually run **1 June – 18 July** (§13 gets this right), meaning the totals include 1 June, a day *before* the funded pilot commenced — and one of the three capacity-affected responses listed in §4 is dated 1 June, outside the window that table declares. Worse, 1 June is also one of the nine reconstructed-log days. An administrator with a calendar finds this in a minute, and it's exactly the mis-attribution class that drew the last HOTC query.

**Fix by disclosure, not deletion**: don't drop 1 June — the HOTC Weekly Data Report for 1–7 June already includes it, so excluding it would break the exact weekly reconciliation (the report's strongest audit feature) and flip police YoY from −12% to −13%. Corrected §1 opening: state that the pilot runs 2 June–24 July, that this report covers verified data for **1 June – 18 July (48 days, including the 1 June mobilisation day)**, with 19–24 July to be appended. Relabel the §4 row "1 Jun – 18 Jul 2026 (pilot to date)".

## The five MAJOR findings

- **F-2 — "Every attended incident fed the Auror evidence pipeline (48 Auror reports referenced)"** (§1, repeated in §7) is contradicted by its own parenthesis: 406 incidents, 48 reports. Correct to "evidential incidents were posted to the Auror pipeline — 48 Auror reports are referenced in the pilot logs."
- **F-3 — The contractually required CPTED framing sentence appears nowhere.** The report is CPTED-aligned in substance, but the agreement's required Council-facing sentence ("This pilot delivers a targeted CPTED-based intervention, increasing visible guardianship…") must be inserted verbatim — close of the §1 opening paragraph.
- **F-4 — "No use-of-force injuries" (§9) is unreconciled with the 2 "Injuries Reported"** sitting in the weekly reports the administrators hold. Technically compatible, but it will be challenged. Add a reconciling clause identifying both injuries (verify from the daily logs — likely including the 14 July assault on the static guard) and stating neither involved ASG force.
- **F-5 — §2 delivery table conflicts with the Scope of Works on Sunday hours.** The agreement funds 09:00–18:00 on weekends; the table shows Sun–Thu 09:00–17:00, and Fri–Sat shows no hours at all ("Peak windows"). Either correct to the SoW windows or disclose the variance — silence reads as a delivery shortfall.
- **F-6 — "prepared *with Heart of the City*" (§8 survey instrument) is not supported by the corpus** — an attribution about the funder itself. Drop it unless documented. Also add an explicit "No survey wave has yet been completed, so no survey results are reported here" — §8 currently complies with the no-survey-results rule (PASS) but invites the "where's the baseline wave?" question.

## The eleven MINOR findings (condensed)

- **F-7** Exec bullet's rounded inputs don't reproduce its own percentage (59÷41 = +44%, not +45%) — display 59.2 / 40.7 / 46.2 as the §3 table does.
- **F-8** Add a footnote stating percentages are computed from displayed one-decimal rates; and pre-empt the inevitable "+30% police vs baseline" challenge with the corpus-supported share stat: escalations were **9.6% of attended calls vs 10.8% baseline and 14.1% in 2025**.
- **F-9** "142 aggression events **de-escalated**" overstates (two §10 stories end in arrest) — use "attended and managed"; extend the capacity-effect note to cover the +92%/+138% aggression rises.
- **F-10** "≈90 individually named stores visited per day" → "≈90 named-store check-ins per day" (metric counts events, not distinct premises).
- **F-11** "10 liquor-ban interventions" relabels the "Public Drinking/**Cannabis**" metric — soften or verify all 10 were alcohol.
- **F-12** "Hours **were fully committed**" is past-tense about a pilot that runs 6 more days — change to "fully allocated across the pilot roster to 24 July".
- **F-13** Quantify the reconstruction disclosure: 9 of 48 days. (The method itself verifies — imputed values equal rounded averages of equivalent fully-logged two-team days, effect on totals under 1%.)
- **F-14** `&amp;` HTML entity in the §11 table.
- **F-15** Render both chart placeholders; on the §3 weekly chart, annotate the two partial weeks (22 over 2 days, 34 over 6 days) or they'll plot below baseline and read as a late-pilot collapse.
- **F-16** A named pre-submission checklist of log-level claims not verifiable from the corpus (Auror HQ meeting 17 July, FENZ fires, Council referral, calling cards, all 13 positive stories, the §12 objectives sentence, the Queen St/Aotea Square hotspot naming) — none contradict the numeric record; all dollar amounts, the arrest count and the capacity instances ARE corroborated by the contract facts.
- **F-17** Four tone fixes: "Missed demand collapsed" → "Unattended demand fell to near zero"; "unambiguous" → "consistent"; "one number, and a team that comes" → "one number to call, and a team that responds"; "proven here" → "tested and evidenced in this pilot". Otherwise tone passes for a funder audience — adverse numbers are disclosed, and no tender/showcasing language remains after these edits.

## What verified clean

All 17 metric totals (406, 4,354, 678, 156, 142, 79, 39, 35, 30, 13, 48, …), every weekly average and every ratio in the §3 table (+45%, +28%, +27%, +92%, +138%, +39%, +30%, −12%), the baseline and 2025 comparators (recomputed from the raw weekly values), the 10-week baseline window (9 Mar is a Monday, 31 May a Sunday), the Fri–Sat 35% share, all dollar recoveries and capacity instances against the agreement facts, the invoicing statement, and the claim "totals reconcile exactly with the HOTC Weekly Data Reports" — which is literally true, 96/96 cells. The full PASS appendix (29 line items) is in the findings file.

Nothing requires restructuring or restating any headline result. The priority order: F-1 first (five-minute edit, highest challenge risk), then F-2/F-3 (compliance), then F-4/F-5/F-6 (each needs a quick log/roster/correspondence check before final wording), then the mechanical edits.
