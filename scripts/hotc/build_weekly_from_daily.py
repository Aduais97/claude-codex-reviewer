#!/usr/bin/env python3
"""
Build HOTC Weekly Data Report.xlsx files from daily patrol reports.

Source: ~/Desktop/hotc reports/extracted/<Month>/<Week ...>/<Day>/HOTC Daily*.docx
Dest:   ~/Desktop/ASG/Operations/Clients/HOTC/2026/<Month>/<Week ...>/Weekly Data Report.xlsx

Mapping (validated against existing May Week 1 weekly report — 5 core metrics exact):
  Calls Made From Businesses  <- "Total Response Calls"        (structured)
  Police Calls                <- "Police Involvement"          (structured)
  Aggressive Behaviour        <- "Disorderly Behaviour"        (structured)
  Vagrants Moved On           <- "Vagrancy" (by type)          (structured)
  Shoplifting/Theft           <- "Theft" (by type)             (structured)
  Public Drinking/Cannabis    <- narrative keyword scan        (interpretive)
  Arrests                     <- narrative keyword 'arrest'    (interpretive)
  Serious Incidents           <- narrative assault/weapon/etc  (interpretive)
  Injuries Reported           <- narrative injury/wound        (interpretive)
  Intoxicated Persons         <- narrative intoxicated/drunk   (interpretive)
  Medical Responses           <- narrative medical/ambulance   (interpretive)
  Assistance Provided         <- 1 if any assistance/welfare provided that day
Routes: standard daily deployment template Alpha 3 / Bravo-Beta 2 / Charlie 2 / Delta 3
"""
import glob, os, re, datetime
from docx import Document
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

SRC = os.path.expanduser('~/Desktop/hotc reports/extracted')
DEST = os.path.expanduser('~/Desktop/ASG/Operations/Clients/HOTC/2026')

METRICS = [
    'Calls Made From Businesses','Police Calls','Aggressive Behaviour',
    'Public Drinking/Cannabis','Assistance Provided','Serious Incidents',
    'Arrests','Injuries Reported','Vagrants Moved On','Shoplifting/Theft',
    'Intoxicated Persons','Medical Responses',
]
ROUTES = [('Alpha',3),('Bravo/Beta',2),('Charlie',2),('Delta',3)]

# Manual overrides for summary-only "Security Report" days that lack a structured
# Incident Metrics block (June Wk2). Hand-classified from the full narrative,
# consolidating ALL teams (10 June includes the Team-2 incidents the daily summary
# omitted) and excluding the stale 06/03/26 Tsujiri copy-paste artifact.
def _m(calls,police,aggr,drink,assist,serious,arrests,inj,vagr,theft,intox,med):
    keys=['Calls Made From Businesses','Police Calls','Aggressive Behaviour',
          'Public Drinking/Cannabis','Assistance Provided','Serious Incidents','Arrests',
          'Injuries Reported','Vagrants Moved On','Shoplifting/Theft','Intoxicated Persons','Medical Responses']
    return dict(zip(keys,[calls,police,aggr,drink,assist,serious,arrests,inj,vagr,theft,intox,med]))
MANUAL = {
    datetime.date(2026,6,8):  _m(10,1,4,1,1,1,0,0,3,0,1,0),
    datetime.date(2026,6,9):  _m(8, 2,2,0,1,2,1,0,5,0,0,0),
    datetime.date(2026,6,10): _m(7, 0,1,1,1,0,0,0,4,1,0,0),  # 4 summary + 3 Team-2
}
DAYNAMES = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
ORD = {1:'st',2:'nd',3:'rd'}

def ordn(d):
    return f"{d}{ORD.get(d if d<20 else d%10,'th')}"

def all_text(doc):
    out=[]
    for p in doc.paragraphs:
        if p.text.strip():
            out.append(p.text.strip())
    return out

def field(paras, label):
    # matches 'Label: N' and 'Label / Extra Words: N' (newer June format), but NOT
    # a different field that merely starts with the same word (e.g. 'Theft Outcomes')
    pat = re.compile(re.escape(label)+r'(?:\s*/[^:\n]*)?\s*:\s*([0-9]+)', re.I)
    for t in paras:
        for ln in t.split('\n'):
            m = pat.search(ln)
            if m: return int(m.group(1))
    return 0

def count_kw(text, pattern):
    return len(re.findall(pattern, text, re.I))

def parse_day(path):
    doc = Document(path)
    paras = all_text(doc)
    full = '\n'.join(paras)
    low = full.lower()
    # response section only (incident/business/summary lines) — excludes welfare-check spam
    ri = next((i for i,t in enumerate(paras) if 'Response Calls' in t or t=='Summary'), 0)
    mi = next((i for i,t in enumerate(paras) if 'Incident Metrics' in t), len(paras))
    resp = '\n'.join(paras[ri:mi]).lower()
    # ---- structured fields (authoritative; validated exact on May Wk1) ----
    calls   = field(paras, 'Total Response Calls')
    police  = field(paras, 'Police Involvement')
    aggr    = field(paras, 'Disorderly Behaviour')
    vagr    = field(paras, 'Vagrancy')          # 'Vagrancy' & 'Vagrancy / Loitering'
    theft   = field(paras, 'Theft')             # 'Theft' by type
    serious = field(paras, 'Assault')           # 'Assault / Fight' / '... Potential Brawl'
    alcohol = field(paras, 'Alcohol-Related')   # newer reports only
    # ---- interpretive (conservative; response-section keyword scan) ----
    inc_lines = [l for l in resp.split('\n') if re.match(r'\d{1,2}:\d{2}', l.strip())]
    drink_scan = sum(1 for l in inc_lines if re.search(r'weed|cannabis|marijuana|\bdrinking\b|consuming alcohol|public drinking|smoking', l))
    drink   = max(alcohol, drink_scan)
    arrests = count_kw(resp, r'\barrest')
    injury  = sum(1 for l in inc_lines if re.search(r'injur|laceration|bleeding|stabbed', l))
    intox   = sum(1 for l in inc_lines if re.search(r'intoxicat|under the influence|drunk', l) and re.search(r'police|restrain|handed|removed|ambulance', l))
    medical = sum(1 for l in inc_lines if re.search(r'st john|paramedic|\bcpr\b|first aid administered', l))  # excl. bare 'ambulance involved' per house style
    assist  = 1 if calls>0 else 0             # house style: nominal 1/active day (matches May Wk1)
    return {
        'Calls Made From Businesses':calls,'Police Calls':police,
        'Aggressive Behaviour':aggr,'Public Drinking/Cannabis':drink,
        'Assistance Provided':assist,'Serious Incidents':serious,'Arrests':arrests,
        'Injuries Reported':injury,'Vagrants Moved On':vagr,'Shoplifting/Theft':theft,
        'Intoxicated Persons':intox,'Medical Responses':medical,
    }

def date_from_name(path):
    m = re.search(r'(\d{1,2})[_](\d{1,2})[_](\d{2,4})', os.path.basename(path))
    if not m: return None
    d,mo,y = map(int, m.groups())
    if y<100: y+=2000
    return datetime.date(y,mo,d)

# ---- gather weeks ----
weeks = {}  # (month, weekfolder) -> list of (date, path)
for path in glob.glob(SRC+'/**/HOTC Daily*.docx', recursive=True):
    rel = os.path.relpath(path, SRC).split(os.sep)
    month, weekfolder = rel[0], rel[1]
    dt = date_from_name(path)
    if dt is None: continue
    weeks.setdefault((month,weekfolder), []).append((dt,path))

THIN = Side(style='thin', color='BBBBBB')
BORDER = Border(left=THIN,right=THIN,top=THIN,bottom=THIN)
HEADFILL = PatternFill('solid', fgColor='1F3864')
SUBFILL  = PatternFill('solid', fgColor='D9E1F2')
TOTFILL  = PatternFill('solid', fgColor='FCE4D6')

def build_week(month, weekfolder, days):
    days = sorted(days)
    dates = [d for d,_ in days]
    data = {d: (MANUAL[d] if d in MANUAL else parse_day(p)) for d,p in days}
    wb = openpyxl.Workbook(); ws = wb.active; ws.title='Weekly Data Report'
    cols = [d for d in dates]
    ncol = len(cols)
    # date-range label
    lo,hi = dates[0],dates[-1]
    rng = f"{ordn(lo.day)} {lo.strftime('%B')}".replace(f" {hi.strftime('%B')}","")
    label = f"HOTC Weekly Data Report — {weekfolder}"
    ws.cell(1,1,label).font = Font(bold=True, size=13, color='1F3864')
    # header row 3
    hdr = ['Metric'] + [f"{DAYNAMES[d.weekday()]} {ordn(d.day)}" for d in cols] + ['Total']
    for j,h in enumerate(hdr,1):
        c=ws.cell(3,j,h); c.font=Font(bold=True,color='FFFFFF'); c.fill=HEADFILL
        c.alignment=Alignment(horizontal='center'); c.border=BORDER
    # metric rows
    r=4
    for met in METRICS:
        ws.cell(r,1,met).font=Font(bold=False); ws.cell(r,1).border=BORDER
        tot=0
        for j,d in enumerate(cols,2):
            v=data[d][met]; tot+=v
            cell=ws.cell(r,j, v if v else None); cell.alignment=Alignment(horizontal='center'); cell.border=BORDER
        tc=ws.cell(r, 2+ncol, tot); tc.font=Font(bold=True); tc.alignment=Alignment(horizontal='center')
        tc.fill=TOTFILL; tc.border=BORDER
        r+=1
    # routes section
    r+=1
    ws.cell(r,1,'Patrol Route Coverage').font=Font(bold=True,size=12,color='1F3864'); r+=1
    for j,h in enumerate(['Route']+[f"{DAYNAMES[d.weekday()]} {ordn(d.day)}" for d in cols]+['Total'],1):
        c=ws.cell(r,j,h); c.font=Font(bold=True,color='FFFFFF'); c.fill=HEADFILL
        c.alignment=Alignment(horizontal='center'); c.border=BORDER
    r+=1
    for name,per in ROUTES:
        ws.cell(r,1,name).border=BORDER
        for j,d in enumerate(cols,2):
            c=ws.cell(r,j,per); c.alignment=Alignment(horizontal='center'); c.border=BORDER
        tc=ws.cell(r,2+ncol, per*ncol); tc.font=Font(bold=True); tc.alignment=Alignment(horizontal='center')
        tc.fill=TOTFILL; tc.border=BORDER
        r+=1
    # widths
    ws.column_dimensions['A'].width=28
    for j in range(2, 3+ncol):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width=10
    # write
    outdir = os.path.join(DEST, month, weekfolder)
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, 'Weekly Data Report.xlsx')
    wb.save(outpath)
    # also drop a copy alongside the daily reports in the source drop-folder
    srcdir = os.path.join(SRC, month, weekfolder)
    if os.path.isdir(srcdir):
        wb.save(os.path.join(srcdir, 'Weekly Data Report.xlsx'))
    # return weekly totals for reporting
    totals={met:sum(data[d][met] for d in cols) for met in METRICS}
    return outpath, dates, data, totals

print(f"Found {sum(len(v) for v in weeks.values())} daily reports across {len(weeks)} weeks\n")
for (month,weekfolder), days in sorted(weeks.items()):
    outpath,dates,data,totals = build_week(month,weekfolder,days)
    print(f"### {month} / {weekfolder}  ({len(dates)} days: {dates[0]}..{dates[-1]})")
    print(f"    -> {outpath}")
    print("    " + " | ".join(f"{m.split('/')[0][:14]}={totals[m]}" for m in METRICS if totals[m]))
    print()
