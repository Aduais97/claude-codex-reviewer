# HOTC Daily Report Extraction Guide (Oct–Nov 2026 catch-up)

You are converting raw HOTC CBD Safety Team guard patrol logs (messy free-text docx) into
clean per-day JSON for the locked-format renderer. This is an operational + client-facing
record: clean the prose, never change the facts.

## Inputs
Your week folder contains `_daymap.json` — a list of day dicts with `src` = absolute path
to that day's raw log (`Untitled document.docx`). Read each with python-docx
(venv: `~/Desktop/Dev/Claude/.venv/bin/python`). Dump paragraphs AND any tables.

## Output — one file per day
Write `<ops_day>.json` (e.g. `Thursday 1st October.json`) into your week folder.
Schema (see worked example
`~/Desktop/Dev/Claude/scripts/hotc/data/hotc_sep2/sepwk5/Tuesday 29th September.json` —
READ IT FIRST, it is the style gold standard):

```json
{
 "date_iso": "...", "date": "...", "fname": "...", "ops_day": "...", "col": "...",
 "month": "...", "week": "...",            // copy ALL of these verbatim from _daymap.json
 "coverage": "Morning (Team 1) · Afternoon/Evening · Night",   // build from shifts present
 "sections": [ {"title": "Morning Shift — Team 1 (06:30 – 14:30)", "items": [...]} ],
 "metrics": { ...12 keys... },
 "flags": [ ... ]                           // QA notes, renderer ignores
}
```

Also write `<ops_day>.raw.txt` — the raw paragraph dump (one para per line) for audit.

## Sections
One section per shift, chronological. Titles follow the convention:
- `"Morning Shift — Team 1 (06:30 – 14:30)"`
- `"Day Shift — Team 2 (09:00 – 18:00)"` (when a second day team appears)
- `"Afternoon/Evening Shift (14:30 – 22:30)"`
- `"Night Shift (22:30 – 06:30)"`
Use the actual start/end times stated in the log when they differ (e.g. afternoon ending
21:30 → `(14:30 – 21:30)`). Route subheadings (`["sub","Alpha Route"]`) whenever the log
declares a route (Alpha / Beta / Bravo / Charlie / Delta / Echo — use the guard's name).

## Item kinds
- `["n", text]` — notes: ALWAYS first item of each shift = equipment, inline form:
  `"Equipment received: 2 x Swipe Cards, 5 sets of keys, 2 x Vests, Ops Phone, 1 x Bodycam, 2 x Radio."`
- `["e", "HH:MM", text]` — normal timestamped entry
- `["er", "HH:MM", text]` — response call RECEIVED (from a business, management, police, public)
- `["ei", "HH:MM", text]` — notable incident (fight, trespass issued, forcible removal,
  arrest, weapon, assault, serious disturbance). First report entry = er, escalation = ei.
- `["b", [list]]` — bulleted store list. When a welfare check names ~7+ stores, convert to
  `["e","HH:MM","Welfare check, all clear:"]` followed by a `b` list. Short lists (≤6)
  stay inline in the entry text.

## Rewrite rules (LOCKED — from prior ETR'd batches)
1. Normalise ALL times to 24-hour `HH:MM` (`0631`→`06:31`, `6:32`→`06:32`, `1 pm`→`13:00`).
2. Re-sequence entries chronologically WITHIN each shift; handle midnight wrap in Night
   shift (22:30→06:30 order, do not naively sort). Lines with multiple embedded times
   (`"0230 responded... 0240 arrived... 0318 ..."`) → split into separate entries.
3. Clean the prose to professional operational English: fix spelling/grammar
   (`recieved`→`received`, `welfarecheck`→`welfare check`, `loaction`→`location`),
   expand slang (`maccas`→`McDonald's`, `cops`→`Police`, `hq`→`HQ`), full sentences.
4. PRESERVE business names as the guard spelled them (title-case only) — operational
   record. `Woolsworths` stays recognisable as `Woolworths` only for the obvious
   typo-level fixes of KNOWN chains; unknown/local shops keep guard spelling.
5. Keep every timestamp and every fact. NEVER invent, NEVER drop an incident, NEVER
   soften (don't delete e.g. "racially profiling us" — rephrase factually:
   "directed racial abuse at the team before leaving").
6. Break out incidents embedded inside store-check lists into their own entry.
7. Photos/video references: keep as `(Photo on file.)` / `(Footage on file.)`.
8. Equipment lists at shift start → single inline `n` note (see above).
9. Phone-charging / break / standby entries are kept (they evidence coverage) but merge
   consecutive identical "Charging." / "Break." spam lines into one entry spanning the
   period, e.g. `16:10 — Standing by at HQ charging the Ops Phone (16:10–17:00).`

## Metrics (12 keys, integers; count each applicable category per incident)
- `calls` — distinct response calls/requests received requiring attendance (business,
  management-relayed, police request, public). Self-initiated observations do NOT count.
- `police` — incidents with Police presence/involvement the team interacted with/observed on patrol.
- `aggressive` — aggressive/disorderly behaviour incidents.
- `drinking` — public drinking / cannabis incidents.
- `assist` — general public assistance/wayfinding (directions, escorts, helping public,
  assisting management with non-security tasks). NOT response calls.
- `serious` — serious incidents: fights, assaults, weapons, threats of violence.
- `arrests` — arrest events (incident-level, conservative).
- `injuries` — injuries reported/observed/treated.
- `vagrants` — vagrants moved on (individuals, conservative estimate).
- `theft` — shoplifting/theft incidents or theft response calls.
- `intoxicated` — persons under the influence (alcohol/drugs) dealt with.
- `medical` — medical responses.
A multi-attribute incident ticks EVERY applicable category (e.g. intoxicated vagrant moved
on after a business call = calls+1, vagrants+1, intoxicated+1). This is the Wk4/AugWk1
rule — do NOT use one-primary-category counting.

## Capacity (MANDATORY key from 1 Oct 2026 — board reporting commitment)
Every day JSON carries a `"capacity"` array ([] when none) of capacity-affected
responses — calls queued, delayed, or unable to be attended due to concurrent demand
or team availability. Staffing/battery patrol-pause windows with NO affected call stay
in flags/entries only. Entry shape:
```json
{"received":"HH:MM","attended":"HH:MM"|null,"call":"<caller/location — nature>",
 "status":"Queued"|"Delayed"|"Unable to attend"|"Not completed","note":"<reason/outcome>"}
```
The renderer prints this as the daily "Response Capacity Log" section (and a
"Capacity-Affected Responses" row in the weekly). Guards' log template v2
(`~/Desktop/ASG/HOTC/2026/HOTC_Guard_Daily_Log_Template.docx`) instructs them to log
received/arrived times, DELAYED/UNABLE markers, and an end-of-shift Capacity Summary —
parse those fields natively when present; otherwise derive events the way the flags do.

## Flags (QA — populate honestly, [] if none)
- Any call the team could NOT attend, or attended late because they were engaged
  elsewhere ("unable to attend", queued, "will head there after") → flag as
  `"CAPACITY: <HH:MM> <desc>"`. This feeds a board commitment — do not miss these.
- Sections that look byte-identical to another day (template-copy suspicion) →
  `"DUPLICATE?: <desc>"`.
- Missing shifts (no morning/afternoon/night section in the raw) → `"MISSING SHIFT: <which>"`.
- Dates inside the log contradicting the folder date → `"DATE MISMATCH: <desc>"`.
- Anything client-sensitive (use of force, serious violence, complaints about ASG) →
  `"SENSITIVE: <desc>"`.
- Stale/copy-paste content from another date → `"STALE: <desc>"`.

## Checklist before finishing
Every day in `_daymap.json` has a `.json` + `.raw.txt`; metadata copied verbatim from the
map; valid JSON (load it back); metrics are integers; every shift in the raw appears as a
section; counts justified by entries actually present in your sections.
