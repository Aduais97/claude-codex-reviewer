# LCF Pilot Accountability & Value Report — Verification & Hardening Findings

**Document reviewed:** REPORT.md (Enhanced CBD Safety Team — LCF Pilot: Accountability & Value Report)
**Sources verified against:** daily_data.csv (48 days), final_stats.txt, weekly_reports_totals.txt, baseline_and_yoy.txt, lcf_contract_facts.txt
**Review date:** 20 July 2026
**Audience for the report:** Heart of the City (Edward Caughey) → joint LCF funding administrators, Auckland Council, by 31 July 2026

---

## Verification method

Every number, percentage and date in REPORT.md was recomputed independently from daily_data.csv (not taken from final_stats.txt), then cross-checked against the rebuilt HOTC Weekly Data Reports and the funding-agreement facts. All 17 metric totals, all weekly averages, and all 12 metrics × 8 weeks of the weekly reports were reconciled cell by cell.

**Bottom line:** the arithmetic core of the report is sound. All 406/48-day totals reproduce exactly from the daily data; the weekly data reports reconcile with the report **96 out of 96 cells**; every ratio in the Section 3 table reproduces from the displayed weekly rates. No survey results are cited anywhere (constraint met). The defects that remain are of exactly the class flagged as highest-risk: window/date inconsistency on the face of the report, one internally contradicted claim, one missing contractual framing element, and several attribution claims not supported by the supplied corpus.

**Findings: 1 CRITICAL · 5 MAJOR · 11 MINOR.** All are correctable without restructuring the report.

---

## CRITICAL findings

### F-1 (CRITICAL) — Reporting window does not reconcile with the data window; totals include a pre-commencement day

**Locations:** §1 opening paragraph; §1 fourth bullet; §4 table, second row. (§13 states the window correctly.)

**Current text (§1):**
> Between 2 June and 24 July 2026, ASG deployed the Enhanced CBD Safety Team across the Heart of the City precinct under the Local Crime Fund allocation…

**Current text (§4 table):**
> | 2 Jun – 18 Jul 2026 (pilot) | Two teams Sun–Thu; enlarged team Fri–Sat | Three capacity-affected responses across 48 days (≈1% of demand) — all in the first pilot week or on single-team night cover |

**Problem.** Three windows are in circulation and they do not reconcile:

1. The Executive Summary frames results "Between 2 June and 24 July 2026" (53 days), but the headline figures cover 48 logged days.
2. The §4 table labels the pilot row "2 Jun – 18 Jul 2026 … across 48 days" — 2 June to 18 July inclusive is **47 days**, not 48. An administrator counting on a calendar finds an impossible number in under a minute.
3. The 48 days actually run **1 June – 18 July** (as §13 correctly states), i.e. the totals include 1 June — a day **before** the funded pilot commenced (agreement: pilot period 2 June – 24 July), and one of the three capacity-affected responses in the §4 list is dated 1 June, outside the window the table itself declares.

This is the same defect class (a statistic attached to the wrong frame) that drew the previous HOTC query. Note also that 1 June is one of the nine reconstructed-log days (see F-13), which compounds the exposure if discovered rather than disclosed.

**Do not fix this by dropping 1 June from the totals.** The HOTC Weekly Data Report "Week 1, 1st June – 7th June" already includes 1 June; excluding it would break the exact weekly reconciliation (the report's strongest audit feature) and would nudge the police YoY figure from −12% to −13%. The correct fix is disclosure and consistent labelling:

**Corrected text (§1, opening):**
> The Enhanced CBD Safety Team pilot runs from 2 June to 24 July 2026 under the Local Crime Fund allocation administered by Heart of the City. This report presents verified activity data for 1 June – 18 July 2026 — 48 days of daily patrol logs, including the 1 June mobilisation day immediately preceding pilot commencement; the final pilot days (19–24 July) will be appended for the administrators' report. ASG deployed two additional afternoon teams Sunday to Thursday, one enlarged combined team on Friday and Saturday, and a flexed evening uplift on peak nights — alongside the existing 24/7 patrol programme.

**Corrected text (§4 table row):**
> | 1 Jun – 18 Jul 2026 (pilot to date) | Two teams Sun–Thu; enlarged team Fri–Sat | Three capacity-affected responses across 48 logged days (≈1% of demand) — all in the mobilisation/first week or on single-team night cover |

**Corrected text (§1, fourth bullet):** replace "Across the entire pilot the logs show" with "Across the pilot to date (48 logged days) the logs show" — the pilot is not complete at the reporting date.

---

## MAJOR findings

### F-2 (MAJOR) — "Every attended incident fed the Auror evidence pipeline" is contradicted by the report's own numbers

**Locations:** §1 fifth bullet; §7 Auror bullet.

**Current text (§1):**
> …while 13 arrests were directly supported and every attended incident fed the Auror evidence pipeline (48 Auror reports referenced).

**Current text (§7):**
> **Auror** — every attended incident feeds the evidence pipeline; ASG met with Auror's global headquarters on 17 July to deepen the integration…

**Problem.** The report attends 406 incidents and references 48 Auror reports — in the same sentence. "Every attended incident" is falsified by the adjacent parenthesis. This is a gift to a line-by-line reviewer: a universal claim disproved without leaving the bullet.

**Corrected text (§1):**
> …while 13 arrests were directly supported and evidential incidents were posted to the Auror pipeline — 48 Auror reports are referenced in the pilot logs.

**Corrected text (§7):**
> **Auror** — theft and repeat-offender incidents with evidential material (descriptions, footage, recoveries) are posted to Auror, building prosecutable files on repeat offenders; 48 Auror reports are referenced in the pilot logs. ASG met with Auror's global headquarters on 17 July to deepen the integration…

### F-3 (MAJOR) — The contractually required CPTED framing sentence does not appear in the report

**Location:** absent; should anchor §1 (and may be echoed in §11).

**Problem.** The funding agreement requires the Council-facing framing: *"This pilot delivers a targeted CPTED-based intervention, increasing visible guardianship, improving natural surveillance, and strengthening business-community safety networks during peak risk periods."* The report is CPTED-aligned in substance (§11 table; §3 narrative references the guardianship tier), but the required sentence appears nowhere. Since HOTC forwards this to Council, the framing should be present verbatim, positioned where the administrators read first.

**Corrected text:** insert as the closing sentence of the §1 opening paragraph (immediately before "### Headline results"):
> This pilot delivers a targeted CPTED-based intervention, increasing visible guardianship, improving natural surveillance, and strengthening business-community safety networks during peak risk periods.

### F-4 (MAJOR) — "No use-of-force injuries" is unreconciled with the two injuries recorded in the weekly data reports

**Location:** §9, first paragraph.

**Current text:**
> The period's logs record no use-of-force injuries to members of the public, while aggression events were consistently de-escalated through presence, patience and negotiation.

**Problem.** The weekly data reports the administrators hold show **Injuries Reported: 1** in each of the weeks 6–12 July and 13–19 July (total 2). The report's claim is technically compatible (it is scoped to *use-of-force* injuries to *the public*), but it reads as "no injuries" and will be challenged the moment someone cross-references the weekly reports. Unprompted reconciliation is far stronger than a scoped denial.

**Corrected text (pending log verification of what the two injury entries were — see F-16):**
> The period's logs record no injuries to members of the public arising from any use of force by the team. Two injuries appear in the weekly data reports for the period — [insert one-line description of each from the daily logs, e.g. the 14 July assault on a venue static guard] — neither involving force used by the Safety Team. Aggression events were consistently de-escalated through presence, patience and negotiation.

Do not submit until the bracketed description is verified against the daily logs.

### F-5 (MAJOR) — §2 coverage table conflicts with the Scope of Works on Sunday hours (and is vague on Fri–Sat)

**Location:** §2 coverage table, rows 1, 2 and 3.

**Current text:**
> | Afternoon Team 1 (uplift) | Sun–Thu | 09:00–17:00 | Upper CBD sector — welfare checks, response |
> | Afternoon Team 2 (uplift) | Sun–Thu | 09:00–17:00 | Lower CBD sector — welfare checks, response |
> | Enlarged combined team | Fri–Sat | Peak windows | Single larger group on the highest-demand trading days |

**Problem.** The executed agreement specifies the two additional Safety Officers at **09:00–17:00 weekdays, 09:00–18:00 weekends**. Sunday is a weekend: the table's "Sun–Thu 09:00–17:00" understates the funded Sunday window by an hour per team. "Peak windows" for Fri–Sat states no hours at all. In a funding-accountability report, the delivery table will be checked against the Scope of Works line by line; any variance between funded hours and displayed hours needs to be either corrected or explicitly disclosed — silence reads as a shortfall.

**Corrected text (if delivery matched the SoW):**
> | Afternoon Team 1 (uplift) | Sun–Thu | Sun 09:00–18:00; Mon–Thu 09:00–17:00 | Upper CBD sector — welfare checks, response |
> | Afternoon Team 2 (uplift) | Sun–Thu | Sun 09:00–18:00; Mon–Thu 09:00–17:00 | Lower CBD sector — welfare checks, response |
> | Enlarged combined team | Fri–Sat | Fri 09:00–17:00; Sat 09:00–18:00 | Single larger group on the highest-demand trading days |

If rostered delivery differed from the SoW windows, state the actual windows and add one sentence noting the variance and where the hours were redeployed. Verify against rosters/timesheets before submission.

### F-6 (MAJOR) — Survey-instrument attribution to Heart of the City is not supported by the corpus

**Location:** §8, first sentence.

**Current text:**
> The programme's perceptions survey instrument (business, landlord and public-intercept forms) was prepared with Heart of the City at pilot commencement.

**Problem.** The agreement facts record only that the instrument *was prepared* (business/landlord/public-intercept) and that a follow-up wave is recommended post-pilot. Joint preparation "with Heart of the City" is not evidenced. This is an attribution about the funder itself, in a report the funder reviews — precisely the defect class that triggered the previous query. Separately, §8 never states explicitly that **no survey wave has been completed**; "follow-up wave" plus "so the perception shift is measured" invites the question "where are the baseline wave results?" Pre-empt it.

**Corrected text:**
> The programme's perceptions survey instrument (business, landlord and public-intercept forms) was prepared at pilot commencement. No survey wave has yet been completed, so no survey results are reported here. ASG recommends running the survey immediately post-pilot so that measured perceptions are referenced to the deployment period. In the interim, the qualitative record from daily engagement is consistent: …

(Reinstate "with Heart of the City" only if joint preparation is documented — e.g. email trail — and retain that evidence.)

---

## MINOR findings

### F-7 (MINOR) — Executive Summary rounding does not reproduce the headline percentages

**Location:** §1, first bullet.

**Current text:**
> **406 calls and incidents attended** in 48 days — 59 per week against a pre-uplift baseline of 41 (**+45%**) and 46 in the same weeks last year (**+28%**).

**Problem.** A reviewer recomputing from the displayed figures gets 59 ÷ 41 = +43.9%, not +45%. The percentages are correct (they derive from 59.2 ÷ 40.7 = +45.5% and 59.2 ÷ 46.2 = +28.2%) but the bullet displays over-rounded inputs. Show the same one-decimal figures the §3 table uses.

**Corrected text:**
> **406 calls and incidents attended** in 48 days — 59.2 per week against a pre-uplift baseline of 40.7 (**+45%**) and 46.2 in the same weeks last year (**+28%**).

### F-8 (MINOR) — Percentage convention should be stated; police comparisons need one pre-emptive sentence

**Locations:** §3 table and footnote; §1 fifth bullet; §3 closing narrative.

**Problem (a) — convention.** All eight ratios in the §3 table reproduce exactly from the *displayed* one-decimal weekly rates (e.g. 5.7/4.4 → +30%; 5.7/6.5 → −12%). From unrounded rates, police would be +29.3% and −12.5% — an administrator using either convention should not be left to guess. One footnote closes the gap.

**Problem (b) — the +30% challenge.** The table honestly discloses police escalations up +30% vs baseline while the Executive Summary leads with −12% YoY. Expect the question: "you say police load fell, but your own table shows +30% against baseline." The strongest, fully corpus-supported answer is the escalation *share*: police escalations were **9.6% of attended calls during the pilot, vs 10.8% in the baseline and 14.1% in June–July 2025** — the share fell against both comparators even as attended demand rose 45%.

**Corrected text (add to §3 table footnote):**
> Percentages are computed from the weekly rates as displayed (one decimal place).

**Corrected text (append to §3 closing paragraph):**
> As a share of attended demand, police escalations fell against both comparators — 9.6% of attended calls during the pilot, against 10.8% in the baseline period and 14.1% in June–July 2025.

### F-9 (MINOR) — "142 aggression or disorder events de-escalated" overstates; the large aggression rises need the capacity-effect note extended

**Location:** §1, third bullet; §3 narrative.

**Current text:**
> **156 move-ons**, **142 aggression or disorder events de-escalated**, …

**Problem.** Not all 142 ended in de-escalation — the report's own §10 records aggression events ending in physical removal and arrest (9 June, 16 July). The §3 table's own label ("Aggressive behaviour handled") is accurate; the bullet should match it. Separately, aggression +92% vs baseline / +138% YoY are the largest movements in the table; §3 explains rising *calls* as the capacity effect but never explicitly extends that logic to aggression counts — a one-clause addition ("attended and recorded events, not prevalence") closes the "did the precinct get more violent?" reading.

**Corrected text (§1 bullet):**
> **156 move-ons**, **142 aggression or disorder events attended and managed**, **79 theft responses** …

**Corrected text (§3, append to the capacity-effect sentence):**
> The same applies to category counts such as aggressive behaviour: these are attended and recorded events, which rise with patrol density and reporting confidence, not a measure of underlying prevalence.

### F-10 (MINOR) — "≈90 individually named stores visited per day" implies distinct stores; the metric counts check-ins

**Location:** §6, first bullet.

**Current text:**
> **4,354 welfare check-ins with named businesses** across the pilot — ≈90 individually named stores visited per day, plus 678 block-level sweeps.

**Problem.** 4,354 ÷ 48 = 90.7 *check-ins* per day. The metric counts named-store check-in events; the same store checked twice in a day counts twice. "90 individually named stores visited per day" will be read as 90 distinct premises — a claim the data does not establish.

**Corrected text:**
> **4,354 welfare check-ins with named businesses** across the pilot — ≈90 named-store check-ins per day (individual stores may be checked more than once), plus 678 block-level sweeps.

### F-11 (MINOR) — "10 logged liquor-ban interventions" relabels the Public Drinking/Cannabis metric

**Location:** §9, second bullet.

**Current text:**
> Alcohol removed from minors and intoxicated persons in public spaces (10 logged liquor-ban interventions), and 5 medical-support events…

**Problem.** The 10 reconciles to the weekly reports' **"Public Drinking/Cannabis"** metric, which by its name may include cannabis events that are neither "alcohol removed" nor "liquor-ban" matters. If any of the 10 were cannabis-related, the sentence mis-describes them.

**Corrected text (unless the logs confirm all 10 were alcohol):**
> Alcohol removed from minors and intoxicated persons in public spaces (10 logged public-drinking and liquor-ban interventions), and 5 medical-support events…

### F-12 (MINOR) — "Fully committed within the pilot window" is a forward-looking delivery claim in a report dated mid-pilot

**Location:** §2, paragraph after the coverage table.

**Current text:**
> The funded pool of approximately 1,115 service hours was fully committed within the pilot window and invoiced in two equal instalments before 30 June 2026, per the funding agreement.

**Problem.** The report's data runs to 18 July; the pilot (and the hours) run to 24 July. "Was fully committed within the pilot window" asserts, in the past tense, something not yet complete at the reporting date, and hour-level delivery is not evidenced in the corpus. The invoicing statement is correct per the agreement.

**Corrected text:**
> The funded pool of approximately 1,115 service hours is fully allocated across the pilot roster to 24 July, and was invoiced in two equal instalments before 30 June 2026, per the funding agreement. Hours delivered to 18 July are evidenced by the daily patrol logs and the weekly data reports, which reconcile line-for-line with this report.

(Optional hardening for an accountability audience: state the contract value — $41,150 + GST — alongside the hours, so the money and the delivery sit in the same paragraph.)

### F-13 (MINOR) — Reconstructed-day disclosure should be quantified

**Location:** §13.

**Current text:**
> …where a team's written log was not returned for a shift that operated, its activity is included at the verified average level for equivalent fully-logged days.

**Problem.** The method itself verifies cleanly: the imputed values equal the averages of fully-logged two-team Sun–Thu days rounded to whole events (e.g. attended calls 8.9 → 9; named check-ins 94.6 → 95), and the effect on headline totals is under ~1%. But the disclosure does not say **how many** days were reconstructed. Nine of 48 days (19%) — 1, 2, 3, 7, 8, 9, 10, 14 and 21 June — carry reconstructed activity. If an administrator asks and the answer is "nine, including 1 June," it is far better that the report said so first. Note the interaction with F-1: 1 June is both pre-commencement and reconstructed.

**Corrected text:**
> …where a team's written log was not returned for a shift that operated (nine of the 48 days, concentrated in the first three pilot weeks), its activity is included at the verified average level for equivalent fully-logged two-team days, rounded to whole events; the effect on headline totals is under one per cent. Totals reconcile exactly with the HOTC Weekly Data Reports for the period.

### F-14 (MINOR) — HTML entity in the §11 table

**Location:** §11 table, first row.

**Current text:**
> | Territoriality &amp; access — patrols / wardens | …

**Corrected text:**
> | Territoriality & access — patrols / wardens | …

### F-15 (MINOR) — Chart placeholders; partial-week bars will plot below baseline and invite misreading

**Locations:** §3 "[Chart: attended calls per pilot week vs 40.7 baseline]"; §5 "[Chart: pilot totals by category]".

**Problem.** Both placeholders must be rendered before submission. For the §3 chart specifically: two of the eight HOTC weekly-report periods are partial (29–30 June = 2 days, total 22; 13–18 July = 6 days, total 34). Plotted raw against the 40.7 weekly baseline, both bars fall *below* baseline and a reviewer will read them as demand collapsing late in the pilot. Either plot full 7-day weeks only, annotate the partial periods on the chart itself, or plot the daily rate × 7 for partial periods with a clear label.

**Corrected text:** n/a — production instruction; ensure the §3 footnote's partial-week note is mirrored on the chart.

### F-16 (MINOR) — Log-level narrative claims not verifiable from the supplied corpus: run a named pre-submission checklist

**Locations:** §§2, 4, 5, 6, 7, 9, 10, 12.

**Problem.** The corpus corroborates every dollar figure ($1,083.91 / 23 June; $368 / 5 July; $1,377 / 9 July), the arrest count (13), the Auror report count (48), and all three capacity instances. The following are consistent with the daily numeric data but rest on the underlying written logs, which are not in the verification corpus. Given the prior mis-attribution query, each should be checked against the specific log entry (and initialled) before submission:

| Claim | Location | Numeric cross-check |
| --- | --- | --- |
| Auror global HQ meeting, 17 July, with live cover maintained | §4, §7 | — (date only) |
| FENZ bin fires attended, 25 June and 14 July | §7 | Serious-incident entries exist both days |
| Viaduct held overnight after assault on static guard, 14 July | §7 | 14 July: 3 serious, 1 injury logged |
| Council referral of vulnerable young woman (housing/financial) | §7 | — |
| HOTC calling cards delivered; new stores onboarded | §6 | — |
| All 13 positive stories and their dates | §10 | Each date's theft/arrest/medical counts are consistent (e.g. 23 June: 5 thefts, 1 arrest; 3 July: 4 medical) |
| Cross-team dispatch examples (13–16 July, 17 July, 23 June) | §4 | Two-team days confirmed in daily data |
| Hotspots named as "Queen St, Aotea Square" | §2 | Not in agreement facts — confirm against SoW wording |
| Pilot objectives sentence ("set out to identify peak-risk windows…") | §12 | Not in agreement facts — confirm against SoW/proposal wording |
| The two injury entries (F-4) and the composition of the 10 public-drinking events (F-11) | §9 | Totals confirmed; descriptions need logs |

No claim in this list contradicts the numeric record; the exposure is attribution, not arithmetic.

### F-17 (MINOR) — Tone: four phrases exceed the accountability register

**Problem.** Overall tone is appropriate — evidence-led, direct, with adverse numbers (police +30% vs baseline) disclosed rather than buried. No "showcasing" or tender vocabulary appears; §12's recommendation is legitimate report content under the agreement's forward-looking theme, provided it stays findings-based. Four phrases tip toward promotional and are cheap to fix:

| Location | Current text | Corrected text |
| --- | --- | --- |
| §1 bullet 4 | "**Missed demand collapsed:**" | "**Unattended demand fell to near zero:**" |
| §1 closing | "The pattern is unambiguous:" | "The pattern is consistent:" |
| §6 bullet 2 | "with a clear message: one number, and a team that comes." | "with a clear message to stores: one number to call, and a team that responds." |
| §12 | "ASG recommends the deployment pattern proven here" | "ASG recommends the deployment pattern tested and evidenced in this pilot" |

Also §4: "which is the design case for extending the model" — acceptable, but consider "which indicates where any future capacity would have the greatest effect," keeping the explicit recommendation in §12 only, so the report pitches once, with evidence, rather than throughout.

---

## Verification appendix — figures checked and PASSED

Every figure below was recomputed from daily_data.csv and/or the agreement facts and reproduces as stated.

| # | Report claim | Recomputed | Status |
| --- | --- | --- | --- |
| 1 | 406 calls/incidents attended, 48 days | Σ response_calls = 406; 1 Jun–18 Jul = 48 days | PASS (window label: see F-1) |
| 2 | 59.2 attended per week | 406÷48×7 = 59.21 | PASS |
| 3 | +45% vs baseline 40.7 | 59.2÷40.7 = +45.5% | PASS |
| 4 | +28% vs 2025 (46.2) | 59.2÷46.2 = +28.1% | PASS |
| 5 | 2025 comparators: calls 46.2, police 6.5, aggression 8.7 (6 weeks) | 277÷6=46.17; 39÷6=6.50; 52÷6=8.67 | PASS |
| 6 | 4,354 named-store check-ins; ≈90/day | Σ = 4,354; ÷48 = 90.7 | PASS (wording: F-10) |
| 7 | 678 block-level sweeps | Σ = 678 | PASS |
| 8 | 156 move-ons; 22.8/wk; +27% vs 17.9 | Σ=156; 22.75; +27.4% | PASS |
| 9 | 142 aggression; 20.7/wk; +92% vs 10.8; +138% vs 8.7 | Σ=142; 20.71; +91.7%; +137.9% | PASS (wording: F-9) |
| 10 | 79 theft responses; 11.5/wk; +39% vs 8.3 | Σ=79; 11.52; +38.6% | PASS |
| 11 | 35 welfare interventions | Σ welfare_person_checks = 35 | PASS |
| 12 | 30 trespasses | Σ = 30 | PASS |
| 13 | 39 police escalations; 5.7/wk; +30% vs 4.4; −12% vs 6.5 | Σ=39; 5.69; +29.5% / −12.3% from displayed rates | PASS (convention footnote: F-8) |
| 14 | 13 arrests directly supported | Σ arrests = 13; agreement facts = 13 | PASS |
| 15 | 48 Auror reports referenced | Σ auror_mentions = 48; agreement facts = 48 | PASS (universal claim: F-2) |
| 16 | 211 missed interventions = 29% of calls; 51 busy; 20 clashes (Jan–Apr 26) | Agreement facts verbatim | PASS |
| 17 | 3 capacity-affected responses ≈1%; none in two-team daytime after week 1 | 3÷406 = 0.74%; instances 1 Jun / 6 Jun (Sat, week 1) / 2 Jul night | PASS (1 Jun window: F-1) |
| 18 | Capacity instance details (Coffee Club 1 Jun; cafe 6 Jun; 2 Jul 01:34) | Agreement facts verbatim | PASS |
| 19 | ~1,115 funded hours; two equal instalments before 30 Jun 2026 | Agreement facts | PASS (tense: F-12) |
| 20 | Recoveries $1,083.91 (23 Jun), $368 in 5 min (5 Jul), $1,377 (9 Jul) | Agreement facts verbatim | PASS |
| 21 | 10 liquor/public-drinking; 5 medical; 2 injuries; 22 serious; 7 intoxicated; 48 assistance | Σ = 10, 5, 2, 22, 7, 48 | PASS (labels: F-11, F-4) |
| 22 | Baseline: 10 clean Mon–Sun weeks, 9 Mar – 31 May 2026; values 40.7/17.9/10.8/8.3/4.4 | Source verbatim; 9 Mar = Monday, 31 May = Sunday | PASS |
| 23 | 2025 reports were 5-metric; move-ons and theft n/a | Source confirms 5-metric format | PASS |
| 24 | Fri–Sat carried 35% of baseline demand | Source: fri_sat_call_share_pct = 35 | PASS |
| 25 | Final week partial — six days, Mon 13 – Sat 18 July | 13 Jul 2026 = Monday; 6 days | PASS |
| 26 | "Totals reconcile exactly with the HOTC Weekly Data Reports" | 12 metrics × 8 weeks = 96/96 cells match | PASS |
| 27 | Reconstruction method (§13 description) | Imputed values = rounded averages of equivalent fully-logged two-team days | PASS (quantify: F-13) |
| 28 | No survey results cited anywhere | Confirmed — §8 is qualitative and log-sourced only | PASS (add explicit statement: F-6) |
| 29 | Deployment model (2 teams Sun–Thu; enlarged Fri–Sat; Thu–Sat evening pool) | Agreement facts verbatim | PASS (hours detail: F-5) |

---

## Tone assessment (requirement 4)

For a funder-accountability audience the report is fundamentally well-pitched: it leads with delivery against objectives, discloses the unflattering comparator (+30% police vs baseline) in plain sight, explains its own methodology limitations (§13), and confines advocacy to a single forward-looking section that the agreement's reporting themes accommodate. The welfare-first material (§9) is the right register for a Proceeds of Crime Fund audience. The residual risk is concentrated in the four phrases listed in F-17 and in universal quantifiers ("every attended incident", "every day of the pilot", "no use-of-force injuries") — accountability reviewers hunt universals because a single counter-instance defeats them. After F-2, F-4 and F-17, no tender or showcasing language remains.

## Priority order for correction

1. **F-1** — fix the window framing in §1 and §4 (CRITICAL; five-minute edit, highest challenge risk).
2. **F-2, F-3** — Auror claim and required CPTED sentence (compliance-facing).
3. **F-4, F-5, F-6** — reconcile injuries, align the delivery table with the SoW, fix the survey attribution (each needs a quick verification against logs/rosters/correspondence before final wording).
4. **F-7 through F-15** — mechanical edits; under an hour in total.
5. **F-16** — run the attribution checklist against the daily logs with sign-off per item.
6. **F-17** — tone edits.

Nothing in the findings requires restructuring the report or restating any headline result. The numbers hold; the hardening is in framing, attribution and disclosure.
