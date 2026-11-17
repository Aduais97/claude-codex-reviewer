"""HOTC x ASG — LCF Pilot data summary workbook (single-truth figures + native charts).
Sheets: Summary · Weekly Averages · Week by Week · Daily Data. Reconciles with the
Weekly Data Reports and the Accountability & Value Report.
"""
import json, os, datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference, Series
from openpyxl.utils import get_column_letter

DATA = os.path.expanduser('~/Desktop/Dev/Claude/scripts/hotc/data/hotc_pilot_2026')
OUT = os.path.expanduser('~/Desktop/ASG/HOTC/2026/HOTC_LCF_Pilot_Data_Summary.xlsx')
NAVY = '1B2A4A'; BLUE = '3E63A8'; GOLD = 'B8892D'; LGREY = 'F2F4F8'; LBLUE = 'E8EDF5'

S = json.load(open(DATA + '/final_stats.json'))
DAYS = json.load(open(DATA + '/final_dataset.json'))
T = S['totals']; W = S['weekly_avg']; BL = S['baseline_weekly']; YY = S['yoy_2025_weekly']
N = S['days']
FEB = {'calls': 41.8, 'police': 3.2, 'agg': 12.2}

hdr_font = Font(name='Calibri', bold=True, color='FFFFFF', size=10)
hdr_fill = PatternFill('solid', fgColor=NAVY)
title_font = Font(name='Calibri', bold=True, size=14, color=NAVY)
sub_font = Font(name='Calibri', italic=True, size=9, color='4A4A5A')
tot_fill = PatternFill('solid', fgColor=LBLUE)
alt_fill = PatternFill('solid', fgColor=LGREY)
thin = Border(*[Side(style='thin', color='D0D5DD')] * 4)

def style_table(ws, top, left, n_rows, n_cols, totals=False):
    for c in range(left, left + n_cols):
        cell = ws.cell(row=top, column=c)
        cell.font = hdr_font; cell.fill = hdr_fill; cell.border = thin
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    for r in range(top + 1, top + n_rows):
        for c in range(left, left + n_cols):
            cell = ws.cell(row=r, column=c); cell.border = thin
            if (r - top) % 2 == 0: cell.fill = alt_fill
            if c > left: cell.alignment = Alignment(horizontal='center')
    if totals:
        for c in range(left, left + n_cols):
            cell = ws.cell(row=top + n_rows - 1, column=c)
            cell.fill = tot_fill; cell.font = Font(bold=True)

wb = Workbook()

# ---- Summary ----
ws = wb.active; ws.title = 'Summary'
ws['A1'] = 'Enhanced CBD Safety Team — LCF Pilot · Accountability Data Summary'; ws['A1'].font = title_font
ws['A2'] = ('Data window 1 June – 24 July 2026 (54 days, incl. the 1 June mobilisation day; pilot commenced 2 June and concluded 24 July, '
            'runs to 24 July) · compiled from daily patrol logs, reconciled with the Weekly Data Reports · Commercial in Confidence')
ws['A2'].font = sub_font
MEASURES = [('Calls / incidents attended', 'response_calls'), ('People moved on', 'move_ons'),
            ('Aggression / disorder de-escalated', 'aggression_incidents'),
            ('Theft / shoplifting responses', 'thefts'), ('Welfare interventions (people)', 'welfare_person_checks'),
            ('Police escalations', 'police_escalations'), ('Trespasses actioned', 'trespass_events'),
            ('Arrests directly supported', 'arrests'), ('Auror evidence reports referenced', 'auror_mentions'),
            ('Named business welfare check-ins', 'store_checks_named')]
ws.append([]); ws.append(['Measure', 'Pilot total', 'Per week'])
top = ws.max_row
for label, k in MEASURES:
    ws.append([label, T[k], W[k]])
style_table(ws, top, 1, len(MEASURES) + 1, 3)
ws.column_dimensions['A'].width = 36; ws.column_dimensions['B'].width = 13; ws.column_dimensions['C'].width = 11

cap_top = ws.max_row + 2
ws.cell(row=cap_top, column=1, value='Unattended demand — before vs during').font = Font(bold=True, size=11, color=NAVY)
ws.append(['Period', 'Coverage model', 'Unattended / capacity-affected demand'])
style_top = ws.max_row
ws.append(['Jan – Apr 2026 (pre-uplift)', 'Single patrol team', '211 missed interventions — 29% of calls; 51 instances with the team already committed to another call'])
ws.append(['1 Jun – 24 Jul 2026 (full pilot period)', 'Core patrol + LCF uplift team (afternoons Sun–Thu; nights Fri–Sat)',
           'Three capacity-affected responses in 54 days (~1%) — none in the two-team daytime window after week one'])
style_table(ws, style_top, 1, 3, 3)
for r in (style_top + 1, style_top + 2):
    ws.cell(row=r, column=3).alignment = Alignment(wrap_text=True)
    ws.cell(row=r, column=2).alignment = Alignment(horizontal='center', wrap_text=True)
key_r = ws.max_row + 2
ws.cell(row=key_r, column=1, value='KEY RESULT — Fewer Police callouts, more arrests: police 5.7/wk vs 6.5 last year (−12%), '
        'while arrests rose 1.2 → 1.9/wk (+58%); ~1 in 3 Police engagements ended in arrest vs ~1 in 4 pre-uplift.'
        ).font = Font(bold=True, size=10, color=NAVY)

ch = BarChart(); ch.type = 'bar'; ch.style = 10; ch.title = 'Pilot totals (excl. store check-ins)'
ch.height = 9.5; ch.width = 16.5; ch.gapWidth = 55; ch.legend = None
data = Reference(ws, min_col=2, min_row=top + 1, max_row=top + len(MEASURES) - 1)
cats = Reference(ws, min_col=1, min_row=top + 1, max_row=top + len(MEASURES) - 1)
ch.add_data(data, titles_from_data=False); ch.set_categories(cats)
ch.series[0].graphicalProperties.solidFill = BLUE
ws.add_chart(ch, 'E4')

# ---- Weekly Averages ----
ws2 = wb.create_sheet('Weekly Averages')
ws2['A1'] = 'Weekly averages — Feb 2026 onward, vs last year'; ws2['A1'].font = title_font
ws2.append([])
ws2.append(['Metric (per week)', 'Feb 2026', 'Mar–May 2026 (baseline)', 'PILOT Jun–Jul 2026',
            'Jun–Jul 2025 (last year)', 'vs baseline', 'vs last year'])
top2 = ws2.max_row
for label, bk, pk, yk, fk in [
        ('Calls / incidents attended', 'calls', 'response_calls', 'calls', 'calls'),
        ('Police calls / escalations', 'police', 'police_escalations', 'police', 'police'),
        ('Aggressive behaviour', 'aggression', 'aggression_incidents', 'aggression', 'agg'),
        ('People moved on', 'move_ons', 'move_ons', None, None),
        ('Theft / shoplifting', 'theft', 'thefts', None, None),
        ('Arrests directly supported', 'arrests', 'arrests', None, None)]:
    b = BL[bk]; p = W[pk]; y = YY.get(yk) if yk else None; f = FEB.get(fk) if fk else None
    ws2.append([label, f, b, p, y, f'{(p / b - 1) * 100:+.0f}%', f'{(p / y - 1) * 100:+.0f}%' if y else 'n/a'])
style_table(ws2, top2, 1, 7, 7)
ws2.column_dimensions['A'].width = 30
for col in 'BCDEFG': ws2.column_dimensions[col].width = 15
ws2.cell(row=ws2.max_row + 1, column=1, value='Feb 2026 and 2025 used the older 5-metric format — move-ons, theft and arrests '
         'not captured (blank). Baseline = ten clean Mon–Sun weeks, 9 Mar – 31 May 2026.').font = sub_font

ch3 = BarChart(); ch3.type = 'col'; ch3.style = 10; ch3.title = 'Attended calls per week — Feb 26 → pilot, vs last year'
ch3.height = 8.5; ch3.width = 16; ch3.legend = None; ch3.gapWidth = 55
ch3.add_data(Reference(ws2, min_col=2, max_col=5, min_row=top2 + 1, max_row=top2 + 1), titles_from_data=False, from_rows=True)
ch3.set_categories(Reference(ws2, min_col=2, max_col=5, min_row=top2))
ch3.series[0].graphicalProperties.solidFill = GOLD
ws2.add_chart(ch3, 'A11')

ch4 = BarChart(); ch4.type = 'col'; ch4.style = 10; ch4.title = 'Police calls per week — Feb 26 → pilot, vs last year'
ch4.height = 8.5; ch4.width = 16; ch4.legend = None; ch4.gapWidth = 55
s = Series(Reference(ws2, min_col=2, max_col=5, min_row=top2 + 2, max_row=top2 + 2), title='Police calls/wk')
ch4.append(s)
ch4.set_categories(Reference(ws2, min_col=2, max_col=5, min_row=top2))
ch4.series[0].graphicalProperties.solidFill = BLUE
ws2.add_chart(ch4, 'J11')

# ---- Week by Week ----
ws3 = wb.create_sheet('Week by Week')
ws3['A1'] = 'Pilot week-by-week'; ws3['A1'].font = title_font
ws3.append([])
ws3.append(['Week commencing', 'Days', 'Calls attended', 'Move-ons', 'Aggression handled',
            'Theft responses', 'Police', 'Store check-ins', 'Baseline calls/wk'])
top3 = ws3.max_row
wk = {}
for d in DAYS:
    iso = datetime.date.fromisoformat(d['date'])
    w0 = iso - datetime.timedelta(days=iso.weekday())
    g = wk.setdefault(w0, {'days': 0, 'c': 0, 'm': 0, 'a': 0, 't': 0, 'p': 0, 's': 0})
    g['days'] += 1; g['c'] += d['response_calls']; g['m'] += d['move_ons']
    g['a'] += d['aggression_incidents']; g['t'] += d['thefts']; g['p'] += d['police_escalations']
    g['s'] += d['store_checks_named']
for w0 in sorted(wk):
    g = wk[w0]
    ws3.append([w0.strftime('%d %b') + (' *' if g['days'] < 7 else ''), g['days'], g['c'], g['m'],
                g['a'], g['t'], g['p'], g['s'], BL['calls']])
ws3.append(['TOTAL', N, T['response_calls'], T['move_ons'], T['aggression_incidents'], T['thefts'],
            T['police_escalations'], T['store_checks_named'], ''])
style_table(ws3, top3, 1, len(wk) + 2, 9, totals=True)
ws3.column_dimensions['A'].width = 18
for col in 'BCDEFGHI': ws3.column_dimensions[col].width = 14
ws3.cell(row=ws3.max_row + 1, column=1, value='* Partial weeks. Baseline = 40.7 attended calls/wk '
         '(10 clean Mon–Sun weeks, 9 Mar – 31 May 2026).').font = sub_font

ch5 = BarChart(); ch5.type = 'col'; ch5.style = 10; ch5.title = 'Attended calls per pilot week vs baseline'
ch5.height = 9; ch5.width = 18; ch5.gapWidth = 50
ch5.add_data(Reference(ws3, min_col=3, min_row=top3, max_row=top3 + len(wk)), titles_from_data=True)
ch5.set_categories(Reference(ws3, min_col=1, min_row=top3 + 1, max_row=top3 + len(wk)))
ch5.series[0].graphicalProperties.solidFill = GOLD
line = LineChart()
line.add_data(Reference(ws3, min_col=9, min_row=top3, max_row=top3 + len(wk)), titles_from_data=True)
line.series[0].graphicalProperties.line.solidFill = BLUE
line.series[0].graphicalProperties.line.width = 22000
line.series[0].smooth = False
ch5 += line
ws3.add_chart(ch5, 'K3')

# ---- Daily Data ----
ws4 = wb.create_sheet('Daily Data')
ws4.append(['Date', 'Day', 'Two teams (day)', 'Calls attended', 'Move-ons', 'Welfare (people)',
            'Aggression', 'Thefts', 'Police', 'Trespass', 'Auror', 'Arrests', 'Store check-ins'])
for d in DAYS:
    ws4.append([d['date'], d['day'], 'Y' if d.get('two_teams') else '', d['response_calls'], d['move_ons'],
                d['welfare_person_checks'], d['aggression_incidents'], d['thefts'], d['police_escalations'],
                d['trespass_events'], d['auror_mentions'], d['arrests'], d['store_checks_named']])
style_table(ws4, 1, 1, len(DAYS) + 1, 13)
ws4.column_dimensions['A'].width = 12
for i in range(2, 14): ws4.column_dimensions[get_column_letter(i)].width = 12
note4 = ws4.max_row + 2
ws4.cell(row=note4, column=1, value='4 Jul: two teams overlapped in the day window while guards completed Police statements on the Britomart switchblade incident — incident-driven overlap, not scheduled uplift cover.').font = sub_font
ws4.freeze_panes = 'A2'

wb.save(OUT)
print('SAVED:', OUT)
