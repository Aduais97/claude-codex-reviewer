#!/usr/bin/env python3
"""QA gate for the Oct-Nov 2026 HOTC catch-up package.

Checks:
 1. Every day in every _daymap.json has a day JSON (+ raw.txt for newly extracted days).
 2. Day JSON schema: required keys, metadata matches the day map verbatim,
    12 integer metrics, non-empty sections, items well-formed.
 3. Cross-day duplicate-section detection (template-copy trap, e.g. Sat 8 Aug).
 4. Metrics sanity: calls >= count of 'er' items is NOT required (calls can be
    relayed/merged) but flag days where |calls - er_count| > 3 for review.
 5. Rendered outputs exist and are fresh: Daily Report.docx per day,
    Weekly Data Report.xlsx per week; weekly totals re-derived from day JSONs
    match what openpyxl reads back from the xlsx.
 6. Aggregate flags report (CAPACITY / SENSITIVE / DUPLICATE? / etc.).

Exit 0 = pass (warnings allowed), exit 1 = hard failure.
"""
import os, json, glob, hashlib, sys
import openpyxl

HOME = os.path.expanduser('~')
TREE = os.path.join(HOME, 'Desktop/ASG/Operations/Clients/HOTC/2026')
STAGE = os.path.join(HOME, 'Desktop/Dev/Claude/scripts/hotc/data/hotc_octnov2026')

METRIC_KEYS = ['calls','police','aggressive','drinking','assist','serious',
               'arrests','injuries','vagrants','theft','intoxicated','medical']
METRIC_LABELS = {
    'calls':'Calls Made From Businesses','police':'Police Calls',
    'aggressive':'Aggressive Behaviour','drinking':'Public Drinking/Cannabis',
    'assist':'Assistance Provided','serious':'Serious Incidents','arrests':'Arrests',
    'injuries':'Injuries Reported','vagrants':'Vagrants Moved On',
    'theft':'Shoplifting/Theft','intoxicated':'Intoxicated Persons','medical':'Medical Responses'}
META_KEYS = ['date_iso','date','fname','ops_day','col','month','week']

errors, warnings = [], []
def err(m): errors.append(m)
def warn(m): warnings.append(m)

def section_fingerprint(sec):
    ent = [it for it in sec.get('items', []) if it and it[0] in ('e','ei','er')]
    if len(ent) < 5:
        return None  # too small to be meaningful
    return hashlib.sha1(json.dumps(ent, sort_keys=True).encode()).hexdigest()

def main():
    weeks = sorted(glob.glob(os.path.join(STAGE, '*', '_daymap.json')))
    all_days, fps = [], {}
    for mapf in weeks:
        wdir = os.path.dirname(mapf)
        for md in json.load(open(mapf)):
            jf = os.path.join(wdir, md['ops_day'] + '.json')
            if not os.path.exists(jf):
                err(f"MISSING JSON: {jf}"); continue
            if not os.path.exists(os.path.join(wdir, md['ops_day'] + '.raw.txt')):
                warn(f"missing raw.txt: {md['ops_day']}")
            try:
                d = json.load(open(jf))
            except Exception as e:
                err(f"BAD JSON {jf}: {e}"); continue
            for k in META_KEYS:
                if d.get(k) != md[k]:
                    err(f"{md['ops_day']}: metadata '{k}' = {d.get(k)!r}, map says {md[k]!r}")
            m = d.get('metrics', {})
            for k in METRIC_KEYS:
                if not isinstance(m.get(k), int):
                    err(f"{md['ops_day']}: metric '{k}' not int: {m.get(k)!r}")
            extra = set(m) - set(METRIC_KEYS)
            if extra: warn(f"{md['ops_day']}: extra metric keys {extra}")
            if not d.get('sections'):
                err(f"{md['ops_day']}: no sections")
            er_count = 0
            for sec in d.get('sections', []):
                if not sec.get('title'): err(f"{md['ops_day']}: section missing title")
                for it in sec.get('items', []):
                    k = it[0] if it else None
                    if k in ('e','ei','er'):
                        if len(it) != 3 or ':' not in str(it[1]):
                            err(f"{md['ops_day']}: malformed entry {str(it)[:70]}")
                        if k == 'er': er_count += 1
                    elif k == 'b':
                        if len(it) != 2 or not isinstance(it[1], list):
                            err(f"{md['ops_day']}: malformed bullets")
                    elif k in ('sub','n'):
                        if len(it) != 2: err(f"{md['ops_day']}: malformed {k}")
                    else:
                        err(f"{md['ops_day']}: unknown item kind {k!r}")
                fp = section_fingerprint(sec)
                if fp:
                    if fp in fps and fps[fp][0] != md['ops_day']:
                        err(f"TEMPLATE-COPY: {md['ops_day']} '{sec['title']}' identical to "
                            f"{fps[fp][0]} '{fps[fp][1]}'")
                    fps.setdefault(fp, (md['ops_day'], sec.get('title','')))
            if abs(m.get('calls', 0) - er_count) > 3:
                warn(f"{md['ops_day']}: calls={m.get('calls')} vs {er_count} 'er' entries — review")
            if 'capacity' not in d or not isinstance(d['capacity'], list):
                err(f"{md['ops_day']}: missing/invalid 'capacity' key (mandatory from 1 Oct 2026)")
            else:
                for c in d['capacity']:
                    if not (isinstance(c, dict) and ':' in str(c.get('received'))
                            and c.get('call') and c.get('status') in
                            ('Queued', 'Delayed', 'Unable to attend', 'Not completed')
                            and (c.get('attended') is None or ':' in str(c.get('attended')))):
                        err(f"{md['ops_day']}: malformed capacity entry {str(c)[:80]}")
            all_days.append(d)

    # rendered outputs + weekly reconciliation
    bywk = {}
    for d in all_days:
        bywk.setdefault((d['month'], d['week']), []).append(d)
    # fold in the pre-existing sepwk5 Mon-Wed copies already staged (they're in maps? no)
    for jf in glob.glob(os.path.join(STAGE, 'sepwk5', '*.json')):
        if os.path.basename(jf).startswith('_'): continue
        d = json.load(open(jf))
        key = (d['month'], d['week'])
        if d['ops_day'] not in [x['ops_day'] for x in bywk.get(key, [])]:
            bywk.setdefault(key, []).append(d)

    for (month, week), days in sorted(bywk.items()):
        days.sort(key=lambda x: x['date_iso'])
        for d in days:
            rp = os.path.join(TREE, month, week, d['ops_day'], 'Report', 'Daily Report.docx')
            if not os.path.exists(rp): err(f"MISSING RENDER: {rp}")
            if not os.path.exists(os.path.join(TREE, month, week, d['ops_day'], 'Raw Guard Log.docx')):
                warn(f"no Raw Guard Log.docx filed for {d['ops_day']}")
        wx = os.path.join(TREE, month, week, 'Weekly Data Report.xlsx')
        if not os.path.exists(wx):
            err(f"MISSING WEEKLY: {wx}"); continue
        ws = openpyxl.load_workbook(wx).active
        ncol = len(days)
        hdr = [ws.cell(2, 2 + j).value for j in range(ncol)]
        want_hdr = [d['col'] for d in days]
        if hdr != want_hdr:
            err(f"{week}: weekly day columns {hdr} != {want_hdr}")
        for ri, key in enumerate(METRIC_KEYS, start=3):
            label = ws.cell(ri, 1).value
            if label != METRIC_LABELS[key]:
                err(f"{week}: row {ri} label {label!r} != {METRIC_LABELS[key]!r}"); continue
            want = sum(int(d['metrics'].get(key) or 0) for d in days)
            got = ws.cell(ri, 2 + ncol).value or 0
            if int(got) != want:
                err(f"{week}: {label} total {got} != derived {want}")
            for j, d in enumerate(days):
                cv = ws.cell(ri, 2 + j).value or 0
                dv = int(d['metrics'].get(key) or 0)
                if int(cv) != dv:
                    err(f"{week}: {label} {d['col']} cell {cv} != {dv}")
        if any('capacity' in d for d in days):
            cap_ri = 3 + len(METRIC_KEYS)
            if ws.cell(cap_ri, 1).value != 'Capacity-Affected Responses':
                err(f"{week}: capacity row missing at {cap_ri} (got {ws.cell(cap_ri,1).value!r})")
            else:
                want_tot = 0
                for j, d in enumerate(days):
                    want = len(d['capacity']) if 'capacity' in d else 0
                    want_tot += want
                    got = int(ws.cell(cap_ri, 2 + j).value or 0)
                    if got != want:
                        err(f"{week}: capacity {d['col']} cell {got} != {want}")
                if int(ws.cell(cap_ri, 2 + ncol).value or 0) != want_tot:
                    err(f"{week}: capacity total != {want_tot}")

        tot = {k: sum(int(d['metrics'].get(k) or 0) for d in days) for k in METRIC_KEYS}
        print(f"  {month:<9} {week:<40} days={len(days)} "
              f"calls={tot['calls']} police={tot['police']} vagrants={tot['vagrants']} "
              f"theft={tot['theft']} serious={tot['serious']} arrests={tot['arrests']}")

    print('\n--- FLAGS ---')
    nf = 0
    for d in sorted(all_days, key=lambda x: x['date_iso']):
        for f in d.get('flags', []) or []:
            print(f"  {d['ops_day']:<26} {f}"); nf += 1
    if not nf: print('  (none)')

    print(f'\n{len(all_days)} newly extracted days checked.')
    for w in warnings: print('WARN:', w)
    for e in errors: print('FAIL:', e)
    print(f'\n{len(errors)} failures, {len(warnings)} warnings.')
    sys.exit(1 if errors else 0)

if __name__ == '__main__':
    main()
