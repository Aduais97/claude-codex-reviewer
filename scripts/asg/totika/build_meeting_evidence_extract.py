#!/usr/bin/env python3
"""SLS head-office Admin-hours meeting evidence extract.

Payroll-derived attendance evidence that staff meetings occurred (Totika MB28
supporting evidence). Honest classification only: timesheets prove WHO was at
head office WHEN; they do not record topics. No toolbox minutes are created.

Source: ~/Desktop/SLS-RTC/Finance/Pay Runs/**/unified_time_sheet_report_*.xlsx
Output: ~/Desktop/ASG/Operations/Toolbox Meetings/ASG_SLS_Team_Meeting_Evidence_Extract_2026.xlsx
        (copy staged to ~/Desktop/ASG/Totika/Evidence/F-Engagement-Toolbox/)
"""
import os, glob, re, shutil
from collections import defaultdict
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ADMIN = re.compile(r'HEAD OFFICE|ADMIN|OFFICE|TRAINING|MEETING', re.I)
OUT = os.path.expanduser('~/Desktop/ASG/Operations/Toolbox Meetings/ASG_SLS_Team_Meeting_Evidence_Extract_2026.xlsx')
EVID = os.path.expanduser('~/Desktop/ASG/Totika/Evidence/F-Engagement-Toolbox')

# classification of multi-staff dates, reviewed 18 Nov 2026
CLASSIFY = {
    '2026-04-08': ('TEAM MEETING (evidenced)', "3 staff overlapping midday; Hardik Patel note: 'Meeting at head office'"),
    '2026-04-20': ('TEAM MEETING (evidenced)', "5 staff all 11:30-12:30 (identical hour); Farshid Hakimi note: 'Meeting forgot to sign in'"),
    '2026-08-17': ('TEAM MEETING (evidenced)', "3 staff 13:00-14:00 identical hour; corroborated by same-day field timesheet notes from Manukau guards referencing 'the meeting'"),
    '2026-06-02': ('DISCIPLINARY MEETING', "2 staff 12:00-13:30; both notes name a disciplinary meeting (also corroborates ASG's minuted disciplinary process)"),
    '2026-04-25': ('CONFIRM PURPOSE', 'ANZAC Day: 8 staff logged 09:00-17:00 identically; may be a training/team day or a public-holiday payroll artifact. Confirm with Ahmad before presenting.'),
    '2026-04-15': ('ADMIN / ONE-ON-ONES', 'Two staff in sequential 1-hour slots (13:30-14:30, 14:30-15:30); pattern suggests interviews/one-on-ones, not a group meeting'),
    '2026-04-16': ('ADMIN / OTHER', "Notes: 'Staff search' and a pay-adjustment note; not a group meeting"),
    '2026-03-25': ('ADMIN / OTHER', 'Non-overlapping times; client-meeting and welfare-check notes'),
    '2026-04-05': ('ADMIN / OTHER', 'Non-overlapping times; hours-correction and admin-work notes'),
    '2026-05-25': ('ADMIN / OTHER', "Non-overlapping; notes 'Interview' and 'Admin work'"),
}

seen, entries = set(), []
for p in glob.glob(os.path.expanduser('~/Desktop/SLS-RTC/Finance/Pay Runs/**/*.xlsx'), recursive=True):
    if os.path.basename(p).startswith('~$'):
        continue
    try:
        wb = load_workbook(p, read_only=True, data_only=True)
        ws = wb['All Employees'] if 'All Employees' in wb.sheetnames else wb.active
        for row in list(ws.iter_rows(values_only=True))[1:]:
            if len(row) < 14:
                continue
            typ = row[2]
            if not (isinstance(typ, str) and ADMIN.search(typ)):
                continue
            name = f"{row[0] or ''} {row[1] or ''}".strip()
            if not name:
                continue
            date = str(row[4])[:10] if row[4] else '?'
            tin, tout = str(row[5] or ''), str(row[8] or '')
            key = (name, date, tin, tout, typ)
            if key in seen:
                continue
            seen.add(key)
            entries.append([name, date, tin, tout, str(row[13] or ''), typ,
                            str(row[11] or '').strip(), str(row[12] or '').strip()])
        wb.close()
    except Exception:
        pass

by_date = defaultdict(list)
for e in entries:
    by_date[e[1]].append(e)

NAVY_F = PatternFill('solid', fgColor='1B2A4A')
GREEN_F = Font(name='Calibri', size=10, bold=True, color='27AE60')
AMBER_F = Font(name='Calibri', size=10, bold=True, color='E67E22')
GREY_F = Font(name='Calibri', size=10, bold=True, color='4A4A5A')
B = Font(name='Calibri', size=10)
HDR = Font(name='Calibri', size=10, bold=True, color='FFFFFF')
WRAP = Alignment(wrap_text=True, vertical='top')
THIN = Border(*[Side(style='thin', color='D0D5DD')] * 4)

wb = Workbook()

def sheet(ws, headers, widths):
    for c, (h, w) in enumerate(zip(headers, widths), 1):
        cell = ws.cell(1, c, h)
        cell.font = HDR; cell.fill = NAVY_F; cell.alignment = WRAP; cell.border = THIN
        ws.column_dimensions[get_column_letter(c)].width = w
    ws.freeze_panes = 'A2'

ws = wb.active; ws.title = 'Basis and Limitations'
sheet(ws, ['Statement'], [130])
for i, s in enumerate([
    'WHAT THIS IS: an extract of SLS RTC unified timesheet (payroll) records of hours worked at HEAD OFFICE SLSRTC, '
    'March to November 2026, compiled 18 November 2026. Where two or more staff were paid for overlapping time at '
    'head office, the records evidence a staff gathering with attendance derivable from payroll.',
    'WHAT THIS IS NOT: topic-level meeting records. Timesheets prove who was present and when; they do not record '
    'what was discussed. No minutes or toolbox records were kept at the time and none have been created retrospectively.',
    'MANAGEMENT STATEMENT: these head-office sessions were ASG/SLS staff get-togethers under Admin hours at which '
    'operational and health and safety matters were discussed (per Ahmad Duais, CEO, 18 November 2026). This attestation '
    'is management recollection, not a contemporaneous topic record.',
    'USE: supporting evidence for Totika MB28 (regular worker meetings occurred, payroll-evidenced) alongside the '
    'documented Toolbox Programme FY27. Formal recorded toolbox delivery (template + signed attendance + Connecteam '
    'form) begins 19 November 2026.',
    'SOURCE: ~/Desktop/SLS-RTC/Finance/Pay Runs/ unified_time_sheet_report_*.xlsx, All Employees sheets, deduplicated. '
    f'{len(entries)} unique head-office entries across {len(by_date)} dates.'], start=2):
    cell = ws.cell(i, 1, s); cell.font = B; cell.alignment = WRAP; cell.border = THIN
    ws.row_dimensions[i].height = 48

ws = wb.create_sheet('Meeting Cohorts')
sheet(ws, ['Date', 'Classification', 'Staff (count)', 'Attendees', 'Times', 'Basis / notes (verbatim where quoted)'],
      [12, 26, 10, 42, 26, 60])
r = 2
for d in sorted(by_date):
    es = by_date[d]
    names = sorted(set(e[0] for e in es))
    if len(names) < 2:
        continue
    cls, basis = CLASSIFY.get(d, ('UNCLASSIFIED', ''))
    times = '; '.join(f"{e[0].split()[0]} {e[2]}-{e[3]}" for e in es)
    vals = [d, cls, len(names), ', '.join(names), times, basis]
    for c, v in enumerate(vals, 1):
        cell = ws.cell(r, c, v)
        cell.font = GREEN_F if (c == 2 and 'TEAM MEETING' in str(cls)) else AMBER_F if (c == 2 and 'CONFIRM' in str(cls)) else GREY_F if c == 2 else B
        cell.alignment = WRAP; cell.border = THIN
    r += 1

ws = wb.create_sheet('All Admin Entries (raw)')
sheet(ws, ['Name', 'Date', 'In', 'Out', 'Hours', 'Type', 'Employee note', 'Manager note'],
      [20, 12, 8, 8, 8, 20, 50, 30])
for i, e in enumerate(sorted(entries, key=lambda x: (x[1], x[0])), 2):
    for c, v in enumerate(e, 1):
        cell = ws.cell(i, c, v); cell.font = B; cell.alignment = WRAP; cell.border = THIN

wb.save(OUT)
shutil.copy(OUT, EVID)
print('XLSX ->', OUT)
print('staged ->', EVID)
