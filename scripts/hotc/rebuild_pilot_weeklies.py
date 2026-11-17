"""Rebuild the HOTC Weekly Data Reports for the LCF pilot period (Jun Wk1 - Jul Wk3)
from the single-truth final dataset, in the locked 12-metric format, so weekly
totals reconcile exactly with the LCF pilot report.

Originals are backed up to scripts/hotc/data/hotc_pilot_2026/weekly_backups/.
"""
import json, os, shutil, datetime
from openpyxl import Workbook
from openpyxl.styles import Font

DATA = os.path.expanduser('~/Desktop/Dev/Claude/scripts/hotc/data/hotc_pilot_2026')
BASE = os.path.expanduser('~/Desktop/ASG/Operations/Clients/HOTC/2026')
BACKUP = os.path.join(DATA, 'weekly_backups')
os.makedirs(BACKUP, exist_ok=True)

final = {r['date']: r for r in json.load(open(DATA + '/final_dataset.json'))}

WEEKS = [
    ('June/Week 1 1st June - 7th June',    '2026-06-01', '2026-06-07', 'Week 1 1st June - 7th June'),
    ('June/Week 2 8th June - 14th June',   '2026-06-08', '2026-06-14', 'Week 2 8th June - 14th June'),
    ('June/Week 3 15th June - 21st June',  '2026-06-15', '2026-06-21', 'Week 3 15th June - 21st June'),
    ('June/Week 4 22nd June - 28th June',  '2026-06-22', '2026-06-28', 'Week 4 22nd June - 28th June'),
    ('June/Week 5 29th June - 30th June',  '2026-06-29', '2026-06-30', 'Week 5 29th June - 30th June'),
    ('July/Week 1 1st July - 5th July',    '2026-07-01', '2026-07-05', 'Week 1 1st July - 5th July'),
    ('July/Week 2 6th July - 12th July',   '2026-07-06', '2026-07-12', 'Week 2 6th July - 12th July'),
    ('July/Week 3 13th July - 19th July',  '2026-07-13', '2026-07-18', 'Week 3 13th July - 19th July'),
]

METRICS = [('Calls Made From Businesses', 'response_calls'),
           ('Police Calls', 'police_escalations'),
           ('Aggressive Behaviour', 'aggression_incidents'),
           ('Public Drinking/Cannabis', 'public_drinking'),
           ('Assistance Provided', 'assistance'),
           ('Serious Incidents', 'serious'),
           ('Arrests', 'arrests'),
           ('Injuries Reported', 'injuries'),
           ('Vagrants Moved On', 'move_ons'),
           ('Shoplifting/Theft', 'thefts'),
           ('Intoxicated Persons', 'intoxicated'),
           ('Medical Responses', 'medical')]
ROUTES = [('Alpha', 3), ('Bravo/Beta', 2), ('Charlie', 2), ('Delta', 3)]

def ordinal(n):
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"

grand = {label: 0 for label, _ in METRICS}
for folder, start, end, label in WEEKS:
    d0 = datetime.date.fromisoformat(start)
    d1 = datetime.date.fromisoformat(end)
    dates = []
    d = d0
    while d <= d1:
        dates.append(d)
        d += datetime.timedelta(days=1)
    hdrs = [f"{d.strftime('%a')} {ordinal(d.day)}" for d in dates]

    wb = Workbook(); ws = wb.active; ws.title = 'Weekly Data Report'
    ws['A1'] = f'HOTC Weekly Data Report — {label}'
    ws['A1'].font = Font(bold=True, size=13)
    ws.append([])
    ws.append(['Metric'] + hdrs + ['Total'])
    for c in ws[3]:
        c.font = Font(bold=True)
    for mlabel, key in METRICS:
        vals = [final.get(d.isoformat(), {}).get(key, 0) for d in dates]
        row = [mlabel] + [(v if v else None) for v in vals] + [sum(vals)]
        ws.append(row)
        grand[mlabel] += sum(vals)
    ws.append([])
    ws.append(['Patrol Route Coverage'])
    ws.cell(row=ws.max_row, column=1).font = Font(bold=True)
    ws.append(['Route'] + hdrs + ['Total'])
    for c in ws[ws.max_row]:
        c.font = Font(bold=True)
    for rname, per_day in ROUTES:
        ws.append([rname] + [per_day] * len(dates) + [per_day * len(dates)])
    ws.column_dimensions['A'].width = 28
    for i in range(2, len(dates) + 3):
        ws.column_dimensions[chr(64 + i) if i <= 26 else 'A'].width = 10

    out = os.path.join(BASE, folder, 'Weekly Data Report.xlsx')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if os.path.exists(out):
        shutil.copy2(out, os.path.join(BACKUP, folder.replace('/', '__') + '.orig.xlsx'))
    wb.save(out)
    calls = sum(final.get(d.isoformat(), {}).get('response_calls', 0) for d in dates)
    print(f'{label:38s} calls={calls:3d}  -> {out.split("HOTC/")[-1]}')

print('\nGRAND TOTALS across the 8 weekly reports:')
for k, v in grand.items():
    print(f'  {k:28s} {v}')
