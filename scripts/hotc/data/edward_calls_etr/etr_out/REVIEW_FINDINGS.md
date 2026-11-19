# REPORT.md — Verification & Value Review

**Reviewer:** Strategy/assurance review for Absolute Security Group
**Audience of the report:** Edward Caughey, Head of Customer Experience, Heart of the City — for his board report / KPI tracker
**Sources:** `REPORT.md`, `SOURCE_DATA.txt` (both in `_analysis_corpus.txt`)
**Recompute basis:** every monthly total re-summed from the weekly figures; grand totals, like-for-like, and per-day recomputed independently.

---

## 1. Number verification — result: **every figure reproduces exactly**

| Check | Report says | Recomputed from weekly data | Verdict |
|---|---|---|---|
| All 24 monthly totals (12 × FY26, 12 × FY25) | as tabled | identical, month for month | ✅ PASS |
| FY26 grand total | 2,505 | 2,505 | ✅ PASS |
| FY25 grand total | 3,042 | 3,042 | ✅ PASS |
| Like-for-like Aug–Jun | 2,419 vs 2,707 | 2,419 vs 2,707 | ✅ PASS |
| Like-for-like YoY | −11% | −10.64% (rounds to −11%) | ✅ PASS (see F5) |
| Per recorded day | 6.7 vs 8.1 | 6.698 vs 8.090 | ✅ PASS |
| All 11 monthly "Change" values (Aug–Jun) | as tabled | identical | ✅ PASS |

**The arithmetic is clean.** No monthly total, grand total, subtotal, or change value is mis-added. This is the strongest possible answer to the prior HOTC query about a mis-attributed statistic: the *numbers* are fully defensible. The remaining findings are about **basis, attribution, and framing**, not arithmetic errors.

---

## 2. Findings list (severity-ranked)

### F1 — Patrol-coverage attribution is UNSUPPORTED by the corpus — **CRITICAL**
**Current text (Notes):**
> "FY25 operated a larger patrol-coverage programme than FY26; the year-on-year movement primarily reflects the reduced coverage footprint, not reduced business engagement per patrol delivered."

**Why this is the highest-risk line in the report:**
- There is **no coverage, patrol-count, roster, hours, or budget figure anywhere in `SOURCE_DATA.txt` or `REPORT.md`.** The claim "FY25 operated a larger patrol-coverage programme" is stated as fact but has no supporting datum in the corpus.
- "business engagement **per patrol delivered**" is **not computable** from this data — there is no patrol count. This is precisely the class of unsupported, recomputation-inviting statistic HOTC queried before.
- The one coverage-*like* proxy that *is* in the data — recorded days — is essentially **equal** (FY26 = 374 days, FY25 = 376 days). On the only footprint measure present, the two years are the same size, which **runs against** an unqualified "larger programme" claim. If challenged, ASG cannot defend this line from the report's own data.

**Replacement — Option A (preferred, if ASG holds the figure):**
> "FY25 was resourced at **[X patrol hours / N patrols per week / \$Y coverage budget]** versus **[X′ / N′ / \$Y′]** in FY26 (a reduction of **[Z%]**). The year-on-year movement in call volume should be read against this reduced coverage footprint."

**Replacement — Option B (if no figure can be cited — do this rather than assert):**
> "FY26 was delivered under a changed patrol-coverage footprint relative to FY25. ASG can provide the underlying deployment/coverage figures to support like-for-like interpretation on request."

**Delete outright** unless a patrol count is supplied: *"not reduced business engagement per patrol delivered."* It asserts a per-patrol efficiency conclusion the data cannot support.

---

### F2 — Per-day metric uses a different period basis than the headline, unlabelled — **MAJOR**
**Current text (Headline):**
> "Per recorded day: 6.7 (FY26) vs 8.1 (FY25)"

**Issue:** the headline −11% is the **Aug–Jun** like-for-like (July excluded). The per-day figure is the **full year including the part-reported July**. Two headline stats on two different periods, neither labelled. A board reader reconciling them will find the full-year per-day implies a ~17% drop and wonder why the headline says −11%.

**Replacement — Option A (preferred: match the headline period):**
> "Per recorded day (Aug–Jun, like-for-like): **6.8 (FY26) vs 7.9 (FY25)**"
*(recomputed: 2,419/358 = 6.76; 2,707/341 = 7.94)*

**Replacement — Option B (keep full year, but label it):**
> "Per recorded day (full year, all recorded days incl. part-reported July): 6.7 (FY26) vs 8.1 (FY25)"

Either is honest; the defect is the **unlabelled basis-mix**, not the value.

---

### F3 — TOTAL row places a like-for-like % next to full-year totals — **MAJOR**
**Current text (table TOTAL row):**
> `| **TOTAL** | **2,505 *** | **3,042** | **−11% l-f-l** |`

**Issue:** 2,505 vs 3,042 is **−17.7%**, not −11%. Printing "−11% l-f-l" immediately beside those two numbers invites the reader to believe it was derived from them. The asterisk mitigates but does not resolve the visual arithmetic mismatch — and this is exactly the kind of "the numbers don't tie" observation that triggered the prior query.

**Replacement — split the row so each % sits on its own basis:**
> `| **Aug–Jun subtotal (like-for-like)** | **2,419** | **2,707** | **−11%** |`
> `| **Full-year total** | **2,505 \*** | **3,042** | *(not comparable — see \*)* |`

This makes the −11% verifiably tie to the 2,419 / 2,707 pair, and stops the full-year totals from implying a headline number they don't produce.

---

### F4 — Asterisk on the 2,505 total is undefined — **MINOR**
**Current text:** "FY26 total business calls: **2,505\***" and TOTAL "**2,505 \***" — the note only explains July's asterisk, not the total's.

**Replacement footnote:**
> "\*The FY26 total includes part-reported July 2025 (2 of ~4–5 weeks). The full-year figure is therefore *lower* than a fully-reported year would show and is **not** directly comparable to FY25's complete 3,042 — use the Aug–Jun like-for-like comparison."

Note this actually **helps ASG**: it explains why the raw total gap looks larger than the real −11%.

---

### F5 — "−11%" is rounded from −10.6% — **MINOR / PASS**
−10.64% rounds correctly to −11%, and it rounds *conservatively* (shows a slightly **larger** decline than actual — i.e. not spin in ASG's favour). Acceptable as-is. Optional precision for a KPI tracker: **"−10.6% (≈ −11%)"**.

---

### F6 — July 2025 partial-data handling — **PASS (keep as-is)**
July FY26 (86 calls / 16 days / 2 weeks) is excluded from the YoY, marked "—" in the Change column (not a negative), and explained in the notes. Recorded FY26 July = 16 days vs FY25 July = 35 days, confirming the "2 of ~4–5 weeks" description. **This is honest, correctly flagged, and does not present July as a real decline.** No change needed.

---

### F7 — The engagement "index" is correctly NOT invented — **PASS (keep as-is)**
The report deals only in raw monthly counts and makes **no reference** to the baseline-100 / ~280 utilisation index Edward maintains. That is correct — ASG does not hold the index definition and must not restate or reverse-engineer it. **Continue supplying raw monthly figures + basis and let HOTC map them to the index.** Do not add an index value in a future version.

---

### F8 — No honest value framing is present; the only editorial line is the unsupported one — **MAJOR (value/tone)**
For a board/KPI audience the report is factual but bare, and its single interpretive sentence is F1 (the unsupported patrol line). The legitimate value story is currently missing. Add a short, **fully data-backed** value note. Every clause below reproduces from the source:

**Suggested addition (Notes or a short "What the data shows" line):**
> "Business demand for the CBD Safety Team stayed strong across FY26 at **2,505 recorded calls**. Engagement **strengthened through the year**: October (302), December (305) and June (265) each **exceeded** the same month in FY25 (**+61, +41, +74**). Two of the three highest-volume months in the Aug–Jun comparison window across both years — **December (305) and October (302)** — fell in FY26, and **June closed +39% year-on-year**, the largest positive monthly swing of the year."

**Verified:** Dec 305 = #1 and Oct 302 = #3 of all Aug–Jun months across both years (FY25 Jan 303 is #2); June 265 vs 191 = +38.7% ≈ +39%.

**Important honesty guardrails on the value framing (correcting the brief's suggested angles):**
- ❌ **Do NOT use "calls per patrol" / per-patrol efficiency.** Not computable — no patrol count exists in the corpus (same defect as F1).
- ❌ **Do NOT frame per-recorded-day as an efficiency win.** It is **down** (6.7 vs 8.1, −17%). Presenting it as value-positive would be spin.
- ✅ The defensible value angle rests on **(a) sustained absolute demand, (b) FY26 holding the strongest recent months, and (c) an improving second-half trajectory** — all directly in the data.

---

## 3. Tone assessment (board/KPI audience)
Factual and restrained overall; tables and notes are appropriate. Two adjustments needed:
1. **Remove the one defensive+unsupported sentence** (F1) — it currently reads as an unbacked justification for the decline, which is the weakest possible posture in front of a board that has already queried a statistic.
2. **Add the confident, data-backed value line** (F8) so the report *shows* value rather than *explaining away* a number. Net effect: honest about the −11%, confident about sustained engagement and the strong close — neither defensive nor over-promotional.

---

## 4. One-line bottom line
The numbers are fully defensible; the report's exposure is **one CRITICAL unsupported attribution (F1)** plus **two MAJOR basis/labelling issues (F2, F3)** and a **missing but easily-supported value line (F8)**. Fix those four and the report is board-ready and query-proof.
