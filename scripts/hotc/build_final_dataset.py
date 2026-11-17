"""HOTC LCF pilot — single-truth final dataset.

Folds the reconstructed second-team activity for the 9 Sun-Thu June days
(team operated, log not returned) into per-day figures: each core metric on
those days is floored at the rounded fully-logged Sun-Thu daily average.
Fri/Sat ran as one combined group — logs complete, never adjusted.

Also derives the soft weekly-report metrics per day from the verified
notable/flag text (conservative, same spirit as build_weekly_from_daily.py).

Outputs (repo data dir): final_dataset.json (per-day) + final_stats.json.
"""
import json, glob, os, re, datetime

DATA = os.path.expanduser('~/Desktop/Dev/Claude/scripts/hotc/data/hotc_pilot_2026')
CORE = ['response_calls', 'move_ons', 'welfare_person_checks', 'police_escalations',
        'thefts', 'aggression_incidents', 'trespass_events', 'auror_mentions',
        'store_checks_named', 'store_sweep_mentions']

days = []
for f in sorted(glob.glob(DATA + '/parsed/*.json')):
    days.extend(json.load(open(f)))
days.sort(key=lambda d: d['date'])
missing = set(json.load(open(DATA + '/missing_team2.json'))['dates'])

def dclass(iso):
    return 'FRI_SAT' if datetime.date.fromisoformat(iso).weekday() in (4, 5) else 'SUN_THU'

# fully-logged Sun-Thu averages — FROZEN to the original window (<=18 Jul) so the
# unusually-detailed final-week (19-24 Jul) logs don't retroactively inflate the 9
# reconstructed June-day estimates. The reconstruction stays identical to the validated report.
full_st = [d for d in days if dclass(d['date']) == 'SUN_THU' and d['date'] not in missing and d['date'] <= '2026-07-18']
floors = {k: round(sum(d.get(k) or 0 for d in full_st) / len(full_st)) for k in CORE}
# never floor sweeps/auror upward aggressively: keep floor but cap at observed+floor? Keep simple max().

def text_blob(d):
    return ' '.join(d.get('notable', []) + d.get('flags', [])).lower()

final = []
for d in days:
    blob = text_blob(d)
    row = {'date': d['date'],
           'day': datetime.date.fromisoformat(d['date']).strftime('%a'),
           'two_teams': bool(d.get('simultaneous_teams_daytime')),
           'reconstructed': d['date'] in missing}
    for k in CORE:
        obs = d.get(k) or 0
        row[k] = max(obs, floors[k]) if d['date'] in missing else obs
    # derived soft metrics (for the weekly 12-metric table).
    # If a day provides 'soft_verified' (the 19-24 Jul final week, hand-verified from the raw
    # logs), use those exact counts — the keyword-regex is tuned to the original readers' notable
    # style and mis-fires on the final-week logs (e.g. "refusing to leave until arrested" = a
    # demand, not an arrest; "citymed medical care" = a business name, not a medical event).
    sv = d.get('soft_verified')
    if sv:
        for k in ('arrests', 'public_drinking', 'intoxicated', 'medical', 'serious', 'injuries'):
            row[k] = sv[k]
    else:
        row['arrests'] = min(len(re.findall(r'arrest', blob)), max(row['police_escalations'], 0))
        row['public_drinking'] = len(re.findall(r'alcohol (?:removed|confiscat)|liquor-ban|drinking(?:/| in)', blob))
        row['intoxicated'] = len(re.findall(r'intoxicated', blob))
        row['medical'] = len(re.findall(r'ambulance|seizure|unresponsive|medical', blob))
        row['serious'] = len(re.findall(r'assault|knife|switchblade|brawl|fire\b|break-in', blob))
        row['injuries'] = 1 if re.search(r'guard was assaulted|assaulting a guard|assaulted a guard', blob) else 0
    row['assistance'] = 1  # original builder rule: 1 per active day
    final.append(row)

totals = {k: sum(r[k] for r in final) for k in CORE + ['arrests', 'public_drinking', 'intoxicated',
                                                       'medical', 'serious', 'injuries', 'assistance']}
n = len(final)
stats = {
    'days': n, 'window': '1 June – 24 July 2026 (full pilot period; commenced 2 June, incl. 1 June mobilisation day)',
    'reconstructed_days': sorted(missing),
    'floors_used': floors,
    'totals': totals,
    'weekly_avg': {k: round(v / n * 7, 1) for k, v in totals.items()},
    'baseline_weekly': {'calls': 40.7, 'move_ons': 17.9, 'aggression': 10.8, 'theft': 8.3, 'police': 4.4,
                        'arrests': 1.2, 'arrests_total_10wk': 12,
                        'window': '9 Mar – 31 May 2026, 10 clean Mon–Sun weeks', 'fri_sat_share_pct': 35},
    'yoy_2025_weekly': {'calls': 46.2, 'police': 6.5, 'aggression': 8.7,
                        'window': 'Jun–Jul 2025, 6 weeks, older 5-metric format'},
    'capacity': {'pre_pilot': '211 missed interventions = 29% of calls; 51 busy instances (ASG analysis Jan–Apr 2026)',
                 'pilot_instances': [
                     {'date': '2026-06-01', 'what': 'Coffee Club caller queued behind another incident (pilot day zero)'},
                     {'date': '2026-06-06', 'what': 'Cafe call unattended while guards managed an active altercation'},
                     {'date': '2026-07-02', 'what': 'Night: second concurrent call queued minutes behind the first — both attended'}],
                 'statement': 'Three capacity-affected responses in 54 days (~1%); none in the two-team daytime window after the first week.'}
}
json.dump(final, open(DATA + '/final_dataset.json', 'w'), indent=1)
json.dump(stats, open(DATA + '/final_stats.json', 'w'), indent=1)
print('days:', n, '| reconstructed:', len(missing))
print('floors:', floors)
for k in CORE:
    print(f'  {k:22s} {totals[k]:6d}   ({stats["weekly_avg"][k]:.1f}/wk)')
print('soft:', {k: totals[k] for k in ['arrests', 'public_drinking', 'intoxicated', 'medical', 'serious', 'injuries']})
