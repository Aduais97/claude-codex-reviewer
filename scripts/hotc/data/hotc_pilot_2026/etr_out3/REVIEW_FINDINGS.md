# LCF Pilot Accountability Package — Final Cross-Consistency Review

**Reviewed:** REPORT.md · DATA_SUMMARY.pdf · DATA_SUMMARY.xlsx · weekly_reports_totals.txt (client-held) — against final_stats.txt, daily_data.csv, baseline_and_yoy.txt, lcf_contract_facts.txt.
**Prepared for:** send to Edward Caughey (Heart of the City) 27 July 2026; onward to the joint LCF funding administrators, Auckland Council, by 31 July 2026.
**Date of review:** 20 July 2026.

---

**Cross-consistency review complete. The package is one story with one set of numbers — every shared figure reconciles — but there are 2 blockers (both one-line fixes), 3 recommended fixes, and 3 optional polish items before the 27 July send.**

A note first: the tasking's "YOUR TASK" section contained boilerplate for an acquisition-analysis report, which does not match this corpus (there is no acquisition target in it). The ANALYSIS REQUIREMENTS section, the working directory, and the corpus contents all define the real job — the final cross-consistency review of the LCF Pilot accountability package — and the approved framework confirms that scope. That is what is delivered here. Findings only; nothing has been rewritten.

**Verification performed:** every figure was checked mechanically, not by eye. `daily_data.csv` was parsed and all 17 metric totals recomputed; all weekly averages recomputed (÷ 48 × 7, rounded to one decimal); all seven week-by-week rows re-summed; all 48 rows of the xlsx Daily Data sheet compared field-by-field against the csv (11 fields per row plus the two-team flag); all 96 metric cells of the eight client-held HOTC Weekly Data Reports (including the 29–30 Jun / 1–5 Jul split) reconciled against the csv date ranges; and every published percentage recomputed from the displayed one-decimal weekly rates. **Zero numeric mismatches anywhere.**

---

## Findings

### BLOCKER

**B1 — Residual plural "additional teams" framing.**
- **Artifact/location:** REPORT.md, §11 CPTED Alignment table, "Territoriality & access" row.
- **Current text:** "Additional uniformed **teams** providing visible guardianship across the precinct in peak-risk windows, seven days."
- **Problem:** Plural "additional … teams" is the outdated two-additional-teams framing. It contradicts §1 ("ASG deployed **one** additional LCF-funded Safety Team") and overstates what the fund paid for — exactly what the administrators will check. A full-corpus scan confirms this is the only such instance in any deliverable (the other plural "teams" uses — §3 "two teams on the ground", §6, §7, §10 "both teams" — correctly mean core + uplift on the ground and are fine).
- **Correction:** "An additional uniformed team, alongside the core patrol, providing visible guardianship across the precinct in peak-risk windows, seven days."

**B2 — The 48-day count is not reconcilable on the face of the PDF or xlsx.**
- **Artifact/location:** DATA_SUMMARY.pdf page 1 header + §1 title; DATA_SUMMARY.xlsx Summary sheet header row 2. Secondary instance: PDF §4 and xlsx Summary capacity table, pilot-period row.
- **Current text:** "Accountability Data Summary · 2 June – 24 July 2026 (activity data to 18 July)" followed by "Pilot Activity Totals — 48 days"; capacity row labelled "1 Jun – 18 Jul 2026 (pilot)".
- **Problem:** 2 June – 18 July inclusive is 47 days. The 48th day (the 1 June mobilisation day) is disclosed only in REPORT.md §1 — but the PDF and xlsx are standalone handouts, and their own week-by-week table visibly starts "w/c 01 Jun", so a reviewer who counts will find a date/day-count contradiction with no explanation on the page. The capacity row compounds it by labelling the 1 June start "(pilot)" when the pilot commenced 2 June.
- **Correction:** Add one footnote to both artifacts: "Data window 1 June – 18 July 2026 (48 days), including the 1 June mobilisation day; pilot commenced 2 June and runs to 24 July." Relabel the capacity row "1 Jun – 18 Jul 2026 (pilot data window)".

### RECOMMENDED

**R1 — Saturday 4 July flagged as a two-team *day*.**
- **Artifact/location:** daily_data.csv row `2026-07-04` (`two_teams=True`) and DATA_SUMMARY.xlsx Daily Data sheet, 2026-07-04 ("Y" in "Two teams (day)").
- **Problem:** The csv and xlsx agree with each other (all 48 rows match), but under the stated model the Fri–Sat uplift runs the **night** window — 4 July is the only Friday or Saturday in the 48 days carrying the day flag; every other one is correctly blank. A "Y" in the day column on a Saturday contradicts the deployment story on the face of the workbook. No published total, and not the "none in the two-team daytime window after week one" claim (the three capacity instances are 1 Jun, 6 Jun, 2 Jul), depends on it, so the fix is safe.
- **Correction:** Verify the 4 July daily log. If the uplift ran the night window, set `two_teams` to False in daily_data.csv and clear the "Y" in the xlsx together (they must stay in lockstep); if a genuine one-off daytime redeployment occurred, footnote it.

**R2 — Reconstruction methodology worded differently (and slightly inaccurately) in REPORT vs PDF.**
- **Artifact/location:** REPORT.md §13 vs DATA_SUMMARY.pdf page 2 footnote.
- **Current text:** REPORT §13: "included at the verified average level for equivalent fully-logged **two-team** days"; PDF: "included at the verified average level for equivalent fully-logged days".
- **Problem:** Two of the nine affected days (1 June and 7 June) are single-team days in the source data, so the REPORT's "two-team days" claim is not strictly accurate, and the two client-facing artifacts describe the same method in different words.
- **Correction:** In REPORT §13 delete "two-team" so both artifacts read "equivalent fully-logged days".

**R3 — Footnote doesn't explain the arrests "n/a" columns.**
- **Artifact/location:** DATA_SUMMARY.pdf §2 footnote and DATA_SUMMARY.xlsx Weekly Averages sheet footnote.
- **Current text:** "Feb 2026 and Jun–Jul 2025 reports used the older 5-metric format — move-ons and theft were not captured then (n/a)."
- **Problem:** Arrests are also shown n/a for Feb 2026 and Jun–Jul 2025 but the footnote explains only move-ons and theft. Since 1.2 → 1.9 arrests/week (+58%) is a headline claim, an administrator may ask why a baseline arrest rate exists for Mar–May but not for last year. (The source confirms the old 5-metric format did not capture arrests.)
- **Correction:** "…— move-ons, theft and arrests were not captured then (n/a)." in both artifacts.

### OPTIONAL

**O1 — "café" vs "cafe".** REPORT.md §4 bullets: "a **café** caller" (1 June) vs "one **cafe** call" (6 June). Pick one form. (Both correctly unnamed — see clean categories below.)

**O2 — "Afternoon, 09:00–17:00" label.** REPORT.md §2 coverage table gives the Sun–Thu uplift window as "Afternoon, 09:00–17:00" — a 09:00 start isn't an afternoon window, and every other artifact says "afternoons Sun–Thu" without clock hours. Either drop the hours from the table row or confirm the rostered hours and label the window accordingly.

**O3 — Final weekly report title spans to 19 July.** The client-held "Week 3 13th July – 19th July" report covers one day past the package's 18 July cutoff. Its totals reconcile exactly with the package's 6-day "13 Jul *" row (34 calls / 12 move-ons / 14 aggression / 5 thefts / 2 police, 1 arrest, 1 injury), so there is no numeric issue, but a reviewer matching titles could ask whether 19 July is missing. No package change required; optionally add to REPORT §13 that the final weekly report is reconciled to 18 July.

---

## Categories confirmed fully consistent

1. **Headline totals** — 406 / 4,354 / 156 / 142 / 79 / 39 / 35 / 30 / 13 / 48 are identical across PDF §1, xlsx Summary, REPORT.md, final_stats.txt, the csv column sums, and the summed HOTC weekly reports. Arrests notably reconcile three ways: 13 in the deliverables = 13 in the csv = 13 summed across the client's own weekly reports (0+3+0+4+0+3+2+1).
2. **Weekly averages and comparators** — every per-week figure recomputes exactly from totals ÷ 48 × 7 (59.2 / 635.0 / 22.8 / 20.7 / 11.5 / 5.7 / 5.1 / 4.4 / 1.9 / 7.0); baseline (40.7 / 17.9 / 10.8 / 8.3 / 4.4 / 1.2), Feb 2026 (41.8 / 3.2 / 12.2) and Jun–Jul 2025 (46.2 / 6.5 / 8.7) match baseline_and_yoy.txt everywhere, and the 2025 averages recompute exactly from the six 2025 weekly reports; all percentages recompute from the displayed rates (+45, +28, +27, +92, +138, +39, +30, −12, +58); the police-share sequence 9.6% / 10.8% / 14.1% (REPORT §3), ≈90 check-ins/day (4,354 ÷ 48 = 90.7), peak week 68, 35% Fri–Sat baseline share, and 678 block sweeps all verify.
3. **Arrest story** — 1.9 vs 1.2/wk (+58%) and ~1-in-3 vs ~1-in-4 Police engagements (13/39 = 0.33; 12/44 = 0.27) are stated identically in PDF §5, xlsx Summary KEY RESULT, REPORT §1, §3 and §7.
4. **Week-by-week rows** — all seven rows and the TOTAL row are identical in the PDF and xlsx and sum exactly from the csv; the split weeks reconcile exactly with the client-held weeklies (22+46 calls = 68, 8+27 move-ons = 35, etc.). The claim "totals reconcile exactly with the HOTC Weekly Data Reports" is true on every metric — all 96 weekly-report cells match the csv date ranges — including the metrics not surfaced in the package (assistance 48, serious 22, intoxicated 7, medical 5, public drinking 10, injuries 2).
5. **Capacity figures** — 211 / 29% / 51 identical everywhere (with the 20 simultaneous-incident clashes appearing only as additional detail in REPORT §4 — consistent, not contradictory); three instances ≈1% with matching dates (1 Jun, 6 Jun, 2 Jul) and the "none in the two-team daytime window after week one" caveat identical across artifacts. **No named cafe** appears in any deliverable — "Coffee Club" survives only in the internal source files (final_stats.txt, lcf_contract_facts.txt), which do not ship. **No "team busy" jargon** in any deliverable (only in the internal contract-facts file).
6. **Framing** — apart from B1, the one-additional-uplift-team model (afternoons Sun–Thu sector split; nights Fri–Sat; core 24/7 unchanged) is stated consistently in REPORT §1/§2/§12, PDF §4, and xlsx Summary; "enlarged" appears only in the permitted night sense (never "enlarged combined team" in a daytime sense); **no instance of "normalised"**; **no instance of "ASG Security"** in any deliverable (PDF header correctly reads "Absolute Security Group"; REPORT uses plain "ASG"; the xlsx names no preparing entity); the required Council-facing CPTED sentence appears verbatim in REPORT §1; §8 correctly cites no survey results; no showcasing/tender language; the financial/hours facts ($41,150 + GST, ~1,115 hours, 2 × $20,575 instalments before 30 June) match the contract facts, and 41,150 ÷ 36.90 ≈ 1,115 checks out.
7. **Internal operational leakage** — none found. No staffing gaps, equipment issues, or internally-framed failures appear in any deliverable; the missing-log reconstruction is disclosed in the agreed neutral wording in both the PDF and REPORT (subject only to R2), and the `reconstructed` column, floor values, and reconstructed-day list exist only in the internal source files.
8. **xlsx vs daily_data.csv** — all 48 Daily Data rows match the csv field-for-field (calls, move-ons, welfare, aggression, thefts, police, trespass, Auror, arrests, store check-ins, and the two-team flags), and every sheet total sums exactly from the csv.

**Bottom line:** fix B1 and B2 (two one-line edits), resolve R1 against the 4 July log, and apply R2/R3, and the package is internally airtight for Edward Caughey on 27 July and the Council administrators on 31 July.
