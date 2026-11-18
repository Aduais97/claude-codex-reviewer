#!/usr/bin/env python3
"""Build redacted H&S incident registers (Woolworths + Bunnings) for folder 04.

Keeps only H&S-relevant structured fields; strips ALL offender PII, staff names/
signatures, recovery $ values, Auror refs, free-text and images. Guard -> initials.
Full unredacted registers remain with the client/SLS under engagement confidentiality.
"""
import os
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

OUT = os.path.expanduser('~/Desktop/ASG/Totika/Evidence/04_Incidents_and_Investigations')
SOURCES = {
    'Woolworths': os.path.expanduser('~/Downloads/Woolworths _ Guard Incident Report_c825cc65-4f04-47bf-b60c-57e23f7026ea.xlsx'),
    'Bunnings':   os.path.expanduser('~/Downloads/Bunnings _ Guard Incident Report _93467dba-f520-495a-858d-6e18a669e4c6.xlsx'),
}
# header substrings to KEEP (safe, H&S-relevant, no PII/commercial)
KEEP = ['submission date', 'date and time of incident - date', 'date and time of incident - time',
        'region of site', 'bunnings site', 'select woolworths site', 'incident severity',
        'incident category', 'type of non-compliant', 'was the suspect', 'were the police informed',
        'did the police attend', 'who did you notify']
NAVY = PatternFill('solid', fgColor='1B2A4A'); THIN = Border(*[Side(style='thin', color='D0D5DD')]*4)

def initials(n):
    if not n: return ''
    return '.'.join(w[0].upper() for w in str(n).split() if w) + '.'

for client, src in SOURCES.items():
    if not os.path.exists(src):
        print('MISSING source:', client); continue
    wb = load_workbook(src, read_only=True, data_only=True)
    ws = wb.active
    rowsit = ws.iter_rows(values_only=True)
    hdr = list(next(rowsit))
    # column indices to keep + the guard name col
    keep_idx = [i for i, h in enumerate(hdr) if h and any(k in str(h).lower() for k in KEEP)]
    name_idx = next((i for i, h in enumerate(hdr) if h and str(h).lower().strip() == 'full name'), None)
    out_hdr = ['#'] + [hdr[i] for i in keep_idx] + ['Guard (initials)']

    owb = Workbook(); ows = owb.active; ows.title = f'{client} Incident Register'
    # note row
    note = (f'{client} Guard Incident Register - REDACTED for Totika H&S evidence. '
            'Offender/customer/staff names, DOB, addresses, vehicles, signatures, recovery values, Auror refs, '
            'images and free-text removed; guard names shown as initials. Full register held under engagement confidentiality.')
    ows.cell(1, 1, note).font = Font(italic=True, size=9, color='4A4A5A')
    ows.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(out_hdr))
    for c, h in enumerate(out_hdr, 1):
        cell = ows.cell(2, c, h); cell.font = Font(bold=True, color='FFFFFF', size=9); cell.fill = NAVY
        cell.alignment = Alignment(wrap_text=True, vertical='top'); cell.border = THIN
    ows.freeze_panes = 'A3'
    n = 0
    for r in rowsit:
        if all(v is None for v in r): continue
        n += 1
        vals = [n] + [r[i] if i < len(r) else '' for i in keep_idx] + [initials(r[name_idx]) if name_idx is not None and name_idx < len(r) else '']
        for c, v in enumerate(vals, 1):
            cell = ows.cell(n + 2, c, v); cell.font = Font(size=9); cell.border = THIN
            cell.alignment = Alignment(vertical='top')
    for c in range(1, len(out_hdr) + 1):
        ows.column_dimensions[chr(64 + c) if c <= 26 else 'A'].width = 16
    wb.close()
    dest = os.path.join(OUT, f'Incident_Register_{client}_REDACTED.xlsx')
    owb.save(dest)
    print(f'{client}: {n} entries, {len(out_hdr)} safe cols -> {os.path.basename(dest)}')
