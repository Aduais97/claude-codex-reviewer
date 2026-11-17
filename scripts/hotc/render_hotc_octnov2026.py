#!/usr/bin/env python3
"""
Central HOTC renderer — reads per-day JSON (produced by extraction agents) and
renders BOTH the locked-format Daily Patrol Report (docx) and the Weekly Data
Report (xlsx), dual-saving into the canonical Operations tree + Downloads.

Day JSON schema (staged at data/hotc_octnov2026/<weekkey>/<ops_day>.json):
{
  "date_iso": "2026-07-20",
  "date": "Monday, 20 July 2026",
  "fname": "HOTC Daily Report - Monday 20 July 2026.docx",
  "ops_day": "Monday 20th July",
  "month": "July",
  "week": "Week 4 20th July - 26th July",
  "col": "Mon 20th",
  "coverage": "Morning (Team 1) · Day (Team 2) · Afternoon/Evening · Night",
  "sections": [ {"title": "...", "items": [ ["sub","Alpha Route"], ["e","06:47","..."],
                 ["ei","08:36","..."], ["er","07:46","..."], ["b",["S1","S2"]], ["n","All clear."] ]} ],
  "metrics": {"calls":6,"police":0,"aggressive":2,"drinking":0,"assist":1,"serious":0,
              "arrests":0,"injuries":0,"vagrants":3,"theft":1,"intoxicated":0,"medical":0}
}
"""
import os, json, glob, sys
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

HOME = os.path.expanduser('~')
TREE = os.path.join(HOME, 'Desktop/ASG/Operations/Clients/HOTC/2026')
STAGE = os.path.join(HOME, 'Desktop/Dev/Claude/scripts/hotc/data/hotc_octnov2026')

NAVY = RGBColor(0x1F, 0x38, 0x64); RED = RGBColor(0xB0, 0x1E, 0x1E)
GREY = RGBColor(0x55, 0x55, 0x55); SUBNAVY = RGBColor(0x2E, 0x4A, 0x7A)

# ---- metric label order (exact, matches existing weeklies) ----
METRICS = [
    ('calls', 'Calls Made From Businesses'), ('police', 'Police Calls'),
    ('aggressive', 'Aggressive Behaviour'), ('drinking', 'Public Drinking/Cannabis'),
    ('assist', 'Assistance Provided'), ('serious', 'Serious Incidents'),
    ('arrests', 'Arrests'), ('injuries', 'Injuries Reported'),
    ('vagrants', 'Vagrants Moved On'), ('theft', 'Shoplifting/Theft'),
    ('intoxicated', 'Intoxicated Persons'), ('medical', 'Medical Responses'),
]
ROUTES = [('Alpha', 3), ('Bravo/Beta', 2), ('Charlie', 2), ('Delta', 3)]

def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement('w:shd'); sh.set(qn('w:fill'), hexcolor); tcPr.append(sh)

def bottom_border(p, color="1F3864", sz="12"):
    pPr = p._p.get_or_add_pPr(); pbdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single'); bottom.set(qn('w:sz'), sz)
    bottom.set(qn('w:space'), '2'); bottom.set(qn('w:color'), color)
    pbdr.append(bottom); pPr.append(pbdr)

def render_day(day):
    doc = Document()
    for s in doc.sections:
        s.top_margin = s.bottom_margin = Cm(1.8); s.left_margin = s.right_margin = Cm(2.0)
    normal = doc.styles['Normal']; normal.font.name = 'Calibri'; normal.font.size = Pt(10.5)

    t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run('HEART OF THE CITY — CBD SAFETY TEAM'); r.bold = True; r.font.size = Pt(17); r.font.color.rgb = NAVY
    st = doc.add_paragraph(); st.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = st.add_run('Daily Patrol Report'); r.font.size = Pt(12); r.font.color.rgb = GREY
    sub = doc.add_paragraph(); sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = sub.add_run('Absolute Security Group  |  Auckland CBD'); r.font.size = Pt(9); r.font.color.rgb = GREY
    bottom_border(sub); doc.add_paragraph()

    meta = [('Date', day['date']), ('Operating Area', 'Auckland CBD (Heart of the City)'),
            ('Shift Coverage', day['coverage']), ('Prepared By', '______________________')]
    tbl = doc.add_table(rows=0, cols=2); tbl.style = 'Table Grid'
    for k, v in meta:
        row = tbl.add_row().cells
        p = row[0].paragraphs[0]; run = p.add_run(k); run.bold = True; run.font.size = Pt(9.5); run.font.color.rgb = NAVY
        shade(row[0], 'EDF0F7')
        p = row[1].paragraphs[0]; run = p.add_run(v); run.font.size = Pt(9.5)
    tbl.columns[0].width = Cm(4.5); tbl.columns[1].width = Cm(12); doc.add_paragraph()

    def heading(text):
        p = doc.add_paragraph(); r = p.add_run(text); r.bold = True; r.font.size = Pt(12.5); r.font.color.rgb = NAVY
        bottom_border(p); p.paragraph_format.space_after = Pt(6); p.paragraph_format.space_before = Pt(12)
    def subhead(text):
        p = doc.add_paragraph(); r = p.add_run(text); r.bold = True; r.font.size = Pt(11); r.font.color.rgb = SUBNAVY
        p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(3)
    def entry(time, text, tag=None):
        p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(3)
        rt = p.add_run(time + '  '); rt.bold = True; rt.font.color.rgb = NAVY; p.add_run('—  ')
        if tag:
            rtag = p.add_run('[' + tag + '] '); rtag.bold = True; rtag.font.color.rgb = RED
        p.add_run(text)
    def bullets(items):
        for it in items:
            p = doc.add_paragraph(style='List Bullet'); p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.left_indent = Cm(1.4); run = p.add_run(it); run.font.size = Pt(10)
    def note(text):
        p = doc.add_paragraph(); r = p.add_run(text); r.italic = True; r.font.size = Pt(9.5); r.font.color.rgb = GREY

    for section in day['sections']:
        heading(section['title'])
        for item in section['items']:
            kind = item[0]
            if kind == 'sub': subhead(item[1])
            elif kind == 'e': entry(item[1], item[2])
            elif kind == 'ei': entry(item[1], item[2], tag='INCIDENT')
            elif kind == 'er': entry(item[1], item[2], tag='RESPONSE')
            elif kind == 'b': bullets(item[1])
            elif kind == 'n': note(item[1])

    if 'capacity' in day:
        heading('Response Capacity Log')
        cap = day['capacity']
        if not cap:
            note('No capacity-affected responses recorded this day — all response calls were attended as received.')
        else:
            ct = doc.add_table(rows=1, cols=5); ct.style = 'Table Grid'
            for i, h in enumerate(['Received', 'Attended', 'Response', 'Call & Outcome', 'Status']):
                p = ct.rows[0].cells[i].paragraphs[0]
                r = p.add_run(h); r.bold = True; r.font.size = Pt(9); r.font.color.rgb = NAVY
                shade(ct.rows[0].cells[i], 'EDF0F7')
            for c in cap:
                mins = None
                if c.get('attended'):
                    h1, m1 = map(int, c['received'].split(':')); h2, m2 = map(int, c['attended'].split(':'))
                    mins = ((h2 * 60 + m2) - (h1 * 60 + m1)) % (24 * 60)
                vals = [c['received'], c.get('attended') or '—',
                        f'{mins} min' if mins is not None else '—',
                        c['call'] + ('. ' + c['note'] if c.get('note') else ''), c['status']]
                row = ct.add_row().cells
                for i, v in enumerate(vals):
                    p = row[i].paragraphs[0]; r = p.add_run(v); r.font.size = Pt(9)
                    if i == 4: r.bold = True; r.font.color.rgb = RED if c['status'] != 'Queued' else SUBNAVY
            for i, w in enumerate([2.0, 2.0, 2.0, 8.0, 2.8]):
                for cell in ct.columns[i].cells: cell.width = Cm(w)
            doc.add_paragraph()
        note('Capacity-affected responses: calls queued, delayed, or unable to be attended due to '
             'concurrent demand or team availability. Formal tracking in effect from 1 October 2026.')

    doc.add_paragraph()
    np_ = doc.add_paragraph(); bottom_border(np_, color="CCCCCC", sz="6")
    note('Note: All photos and videos will be provided at the end of the shift report.')

    dl = os.path.join(HOME, 'Downloads', day['fname']); doc.save(dl)
    ops_dir = os.path.join(TREE, day['month'], day['week'], day['ops_day'], 'Report')
    os.makedirs(ops_dir, exist_ok=True)
    ops = os.path.join(ops_dir, 'Daily Report.docx'); doc.save(ops)
    return ops

def build_weekly(month, week, days):
    """days = list of day dicts (sorted by date_iso)."""
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'Weekly Data Report'
    navy = 'FF1F3864'; lightblue = 'FFEDF0F7'
    thin = Side(style='thin', color='FFBFBFBF'); border = Border(thin, thin, thin, thin)
    cols = [d['col'] for d in days]; ncol = len(cols)

    # Title
    ws.cell(1, 1, f'HOTC Weekly Data Report — {week}')
    ws.cell(1, 1).font = Font(bold=True, size=13, color='FF1F3864')
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=ncol + 2)

    def hdr_row(rowi, first):
        ws.cell(rowi, 1, first)
        for j, c in enumerate(cols): ws.cell(rowi, 2 + j, c)
        ws.cell(rowi, 2 + ncol, 'Total')
        for j in range(ncol + 2):
            cc = ws.cell(rowi, 1 + j)
            cc.font = Font(bold=True, color='FFFFFFFF'); cc.fill = PatternFill('solid', fgColor=navy)
            cc.alignment = Alignment(horizontal='center' if j else 'left'); cc.border = border

    # Metric table
    hdr_row(2, 'Metric')
    ri = 3
    for key, label in METRICS:
        ws.cell(ri, 1, label).font = Font(bold=False)
        ws.cell(ri, 1).border = border
        tot = 0
        for j, d in enumerate(days):
            v = int(d['metrics'].get(key, 0) or 0); tot += v
            cc = ws.cell(ri, 2 + j, v if v else None)
            cc.alignment = Alignment(horizontal='center'); cc.border = border
        tc = ws.cell(ri, 2 + ncol, tot); tc.font = Font(bold=True)
        tc.alignment = Alignment(horizontal='center'); tc.border = border
        ri += 1

    if any('capacity' in d for d in days):
        ws.cell(ri, 1, 'Capacity-Affected Responses').font = Font(bold=False)
        ws.cell(ri, 1).border = border
        ctot = 0
        for j, d in enumerate(days):
            v = len(d['capacity']) if 'capacity' in d else None
            ctot += v or 0
            cc = ws.cell(ri, 2 + j, v if v else None)
            cc.alignment = Alignment(horizontal='center'); cc.border = border
        tc = ws.cell(ri, 2 + ncol, ctot); tc.font = Font(bold=True)
        tc.alignment = Alignment(horizontal='center'); tc.border = border
        ri += 1

    ri += 1
    ws.cell(ri, 1, 'Patrol Route Coverage').font = Font(bold=True, size=12, color='FF1F3864'); ri += 1
    hdr_row(ri, 'Route'); ri += 1
    for name, per in ROUTES:
        ws.cell(ri, 1, name).border = border
        for j in range(ncol):
            cc = ws.cell(ri, 2 + j, per); cc.alignment = Alignment(horizontal='center'); cc.border = border
        tc = ws.cell(ri, 2 + ncol, per * ncol); tc.font = Font(bold=True)
        tc.alignment = Alignment(horizontal='center'); tc.border = border
        ri += 1

    ws.column_dimensions['A'].width = 30
    for j in range(ncol + 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(2 + j)].width = 11

    outdir = os.path.join(TREE, month, week); os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, 'Weekly Data Report.xlsx'); wb.save(outpath)
    totals = {label: sum(int(d['metrics'].get(key, 0) or 0) for d in days) for key, label in METRICS}
    return outpath, totals

def main():
    weekfiles = {}
    for jf in glob.glob(os.path.join(STAGE, '*', '*.json')):
        if os.path.basename(jf).startswith('_'): continue
        d = json.load(open(jf))
        weekfiles.setdefault((d['month'], d['week']), []).append(d)
    if not weekfiles:
        print('No day JSONs found in', STAGE); return
    grand = 0
    for (month, week), days in sorted(weekfiles.items()):
        days.sort(key=lambda x: x['date_iso'])
        for d in days:
            ops = render_day(d); print('  daily :', ops)
        outpath, totals = build_weekly(month, week, days)
        wk_total = totals['Calls Made From Businesses']
        print(f'WEEKLY: {outpath}')
        print('        ', ' | '.join(f"{lab.split()[0]}={v}" for lab, v in totals.items() if v))
        grand += len(days)
    print(f'\nRendered {grand} daily reports across {len(weekfiles)} weeks.')

if __name__ == '__main__':
    main()
