#!/usr/bin/env python3
"""Structure REAL Connecteam H&S Toolbox Meeting submissions into readable records.

Input: the actual Connecteam form export (one row per genuine submission).
Output: one properly-structured meeting-record PDF per REAL submission, carrying
that submission's genuine date, + a clean register sheet. NOTHING is invented or
date-propagated; each record maps 1:1 to a real Connecteam submission.
"""
import os, glob
from openpyxl import load_workbook
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

NAVY = HexColor('#1B2A4A'); GREY = HexColor('#4A4A5A'); BORDER = HexColor('#D0D5DD'); LB = HexColor('#E8EDF5')
SRC = glob.glob(os.path.expanduser('~/Downloads/H&S Toolbox Meeting_*.xlsx'))
OUTDIR = os.path.expanduser('~/Desktop/ASG/Operations/Toolbox Meetings/Connecteam Records')
EVID = os.path.expanduser('~/Desktop/ASG/Totika/Evidence/F-Engagement-Toolbox')
os.makedirs(OUTDIR, exist_ok=True)

wb = load_workbook(SRC[0], data_only=True); ws = wb.active
hdr = [ws.cell(1, c).value for c in range(1, ws.max_column + 1)]

def rows():
    for r in range(2, ws.max_row + 1):
        d = {hdr[c-1]: ws.cell(r, c).value for c in range(1, ws.max_column + 1)}
        if d.get('Submission Date'):
            yield d

B = ParagraphStyle('b', fontName='Helvetica', fontSize=9.5, leading=13, alignment=TA_LEFT)
H = ParagraphStyle('h', fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=NAVY, alignment=TA_CENTER)
SUB = ParagraphStyle('s', fontName='Helvetica-Oblique', fontSize=8.5, leading=11, textColor=GREY, alignment=TA_CENTER)
SH = ParagraphStyle('sh', fontName='Helvetica-Bold', fontSize=10.5, leading=13, textColor=NAVY, spaceBefore=8, spaceAfter=3)

def kv(pairs):
    t = Table([[Paragraph(f'<b>{k}</b>', B), Paragraph(str(v), B)] for k, v in pairs], colWidths=[210, 277])
    t.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.4, BORDER), ('BACKGROUND', (0,0), (0,-1), LB),
                           ('VALIGN', (0,0), (-1,-1), 'TOP'), ('TOPPADDING', (0,0), (-1,-1), 4),
                           ('BOTTOMPADDING', (0,0), (-1,-1), 4), ('LEFTPADDING', (0,0), (-1,-1), 6)]))
    return t

built = []
for d in rows():
    mdate = str(d.get('Date - Date') or d.get('Submission Date'))[:10]
    fname = f"Toolbox_Record_{mdate}_{str(d.get('Select Client') or 'site').split()[0]}.pdf"
    out = os.path.join(OUTDIR, fname)
    doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=48)
    E = [Paragraph('ASG Health &amp; Safety Toolbox Meeting Record', H),
         Paragraph(f"Connecteam submission #{d.get('#')} &mdash; structured from the original app form submission "
                   f"(submitted {d.get('Submission Date')}). Captured signatures held in Connecteam.", SUB),
         Spacer(1, 10)]
    E.append(kv([
        ('Meeting date', mdate),
        ('Submitted (Connecteam)', d.get('Submission Date')),
        ('Facilitator (Team Leader/Manager)', d.get('Full name')),
        ('Client', d.get('Select Client')),
        ('Number of attendees', d.get('Number of attendees at this meeting')),
    ]))
    E.append(Paragraph('Pre-shift safety confirmations', SH))
    E.append(kv([
        ('Aware of store Standard Operating Procedures', d.get('Are you aware of this stores Standard Operating Procedures?')),
        ('All staff have working radios and ear-pieces', d.get('Do all staff have working Radio Telephones and ear-pieces?')),
        ('Team understands the 100% rule', d.get('Does everyone understand the 100% rule?')),
        ('Authorises approach to a suspect', d.get('Who on the team is responsible for authorising staff to approach a suspect?')),
        ('Follow a suspect into the car park?', d.get('Are you allowed to follow a suspect into the car park at this store?')),
    ]))
    E.append(Paragraph('Risk assessment for the shift', SH))
    E.append(kv([
        ('Main risks faced in this store today', d.get('What are the main risks faced working in this store today? ')),
        ('Major risks identified on site', d.get('List any major risks that you could see happening on this site')),
        ('Exit strategy if threatened or attacked', d.get('If a Covert staff member is threatened or attacked what is the exit strategy?')),
    ]))
    E.append(Paragraph('Four-step apprehension process (confirmed)', SH))
    E.append(kv([
        ('Exit the suspect from store', d.get('Exit the suspect from store')),
        ('Monitor store entry for aggressive return', d.get('Monitor store entry for aggressive return by suspect')),
        ('Value merchandise and obtain docket', d.get('Value merchandise and obtain docket')),
        ('Complete report with photo of suspect', d.get('Complete Report with photo of suspect.')),
        ('Team confidence naming the four steps (1-4)', d.get('How confident is your team to name and list the four steps? ')),
    ]))
    E.append(Paragraph('Emergency and site awareness', SH))
    E.append(kv([
        ('Store exit point', d.get('Where do you exit the store?')),
        ('Aware of fire exit plan and doors', d.get('Are you aware of the stores fire exit plan and fire exit doors.')),
        ('Fire extinguisher locations', d.get('Where are the fire extinguishers located?')),
        ('Duty Manager notified team on site', d.get('Duty Manager Notified that the team is on site')),
        ('Store Manager notified team on site', d.get('Store Manager Notified that the team is on site')),
    ]))
    E.append(Spacer(1, 8))
    E.append(Paragraph('Attendance confirmed by captured signatures in Connecteam at submission. '
                       'This record is a structured rendering of a single genuine app-form submission; '
                       'no data has been added or altered.', SUB))
    doc.build(E)
    built.append((mdate, out))

# clean register sheet of the real submissions
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
reg = Workbook(); r = reg.active; r.title = 'Toolbox Delivery (Connecteam)'
cols = ['Submission #', 'Meeting date', 'Submitted', 'Facilitator', 'Client', 'Attendees', 'Main risks', 'SOP aware', 'Radios', '100% rule', 'Fire plan aware']
for i, h in enumerate(cols, 1):
    c = r.cell(1, i, h); c.font = Font(bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor='1B2A4A')
    c.alignment = Alignment(wrap_text=True, vertical='top'); c.border = Border(*[Side(style='thin', color='D0D5DD')]*4)
r.freeze_panes = 'A2'
for i, d in enumerate(rows(), 2):
    vals = [d.get('#'), str(d.get('Date - Date'))[:10], str(d.get('Submission Date')), d.get('Full name'),
            d.get('Select Client'), d.get('Number of attendees at this meeting'),
            d.get('What are the main risks faced working in this store today? '),
            d.get('Are you aware of this stores Standard Operating Procedures?'),
            d.get('Do all staff have working Radio Telephones and ear-pieces?'),
            d.get('Does everyone understand the 100% rule?'),
            d.get('Are you aware of the stores fire exit plan and fire exit doors.')]
    for j, v in enumerate(vals, 1):
        cc = r.cell(i, j, v); cc.alignment = Alignment(wrap_text=True, vertical='top'); cc.border = Border(*[Side(style='thin', color='D0D5DD')]*4)
for w, L in zip([10,12,18,16,12,9,28,10,9,9,10], 'ABCDEFGHIJK'):
    r.column_dimensions[L].width = w
regpath = os.path.join(EVID, 'ASG_Toolbox_Delivery_Register_Connecteam.xlsx')
reg.save(regpath)

# stage the record PDFs into Evidence too
import shutil
for _, o in built:
    shutil.copy(o, EVID)
print(f'built {len(built)} structured records from REAL submissions:')
for md, o in built: print('  ', md, '->', os.path.basename(o))
print('register ->', regpath)
