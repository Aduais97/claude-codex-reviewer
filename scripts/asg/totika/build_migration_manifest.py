#!/usr/bin/env python3
"""SafetySeek migration manifest for Simon Glasgow (VINCI) — what ASG can migrate.

Sources = verified findings of the 17 Nov 2026 ETR filesystem sweep (wf_bbd8ef14-408).
Output: ~/Desktop/ASG/Totika/ASG_SafetySeek_Migration_Manifest_Nov2026.docx
"""
import os
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

NAVY = RGBColor(0x1B, 0x2A, 0x4A)
GOLD = RGBColor(0xD4, 0xA8, 0x43)
GREY = RGBColor(0x4A, 0x4A, 0x5A)

OUT = os.path.expanduser('~/Desktop/ASG/Totika/ASG_SafetySeek_Migration_Manifest_Nov2026.docx')

doc = Document()
for s in doc.sections:
    s.top_margin = Cm(2.0); s.bottom_margin = Cm(2.0)
    s.left_margin = Cm(2.2); s.right_margin = Cm(2.2)

st = doc.styles['Normal']
st.font.name = 'Calibri'; st.font.size = Pt(10.5)

t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run('ASG - SafetySeek Migration Manifest'); r.bold = True; r.font.size = Pt(20); r.font.color.rgb = NAVY
sub = doc.add_paragraph(); sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub.add_run('Incident and operating records available for migration  |  Prepared for Simon Glasgow, VINCI  |  18 November 2026')
r.font.size = Pt(10); r.font.color.rgb = GREY

doc.add_paragraph()
p = doc.add_paragraph()
p.add_run('Following your confirmation that internal incident records can be migrated into SafetySeek, this manifest lists '
          'every records source ASG holds, verified file by file on 17 November 2026. Items marked with a folder path are '
          'already staged in the Totika evidence pack at ')
r = p.add_run('~/Desktop/ASG/Totika/Evidence/'); r.font.name = 'Consolas'; r.font.size = Pt(9.5)
p.add_run(' and can be provided in any format needed.')


def heading(text):
    h = doc.add_paragraph()
    r = h.add_run(text); r.bold = True; r.font.size = Pt(13); r.font.color.rgb = NAVY
    h.space_before = Pt(14); h.space_after = Pt(4)


def table(headers, rows, widths):
    tb = doc.add_table(rows=1, cols=len(headers))
    tb.style = 'Table Grid'
    for i, (h, w) in enumerate(zip(headers, widths)):
        cell = tb.rows[0].cells[i]
        cell.width = Cm(w)
        para = cell.paragraphs[0]; para.text = ''
        r = para.add_run(h); r.bold = True; r.font.size = Pt(9.5)
    for row in rows:
        cells = tb.add_row().cells
        for i, (v, w) in enumerate(zip(row, widths)):
            cells[i].width = Cm(w)
            para = cells[i].paragraphs[0]; para.text = ''
            r = para.add_run(v); r.font.size = Pt(9)
    doc.add_paragraph()


heading('1.  Incident records (migrate — the big win)')
table(['Source', 'Volume and dates', 'Format'], widths=[5.0, 8.6, 3.0], rows=[
    ['Bunnings Guard Incident Reports (GIR) register', '1,740 named entries, 2 Jul 2025 - 31 Oct 2026, dual timestamps, severity, Auror refs. Guard-signature marker every row; actual signature images sit in the source form platform and should be exported with the data.', 'Excel (weekly exports; consolidated file held)'],
    ['Woolworths GIR register', '4,971 named entries covering full FY26, plus approximately 1,020 deterrent-event records and Mitre 10 / Warehouse weekly export sets', 'Excel'],
    ['Woolworths FRT severe incident register', '151 entries, 14 Mar - 14 Oct 2026', 'Excel'],
    ['HOTC CBD patrol incident data', '~980 daily shift logs Mar 2024 - 15 Nov 2026 (incidents with time/location/resolution, police interactions) + continuous weekly data registers with per-category counts', 'Word daily logs + Excel weeklies'],
    ['Completed investigations', 'Cotton On (incident 6 Sep 26, officer statement, video review, findings, corrective actions) + Investigation Summary 19 Mar 26 + CRL First Looks report (issued 25 Aug 26, HSWA s23-25 notifiable-event determinations)', 'PDF/Word'],
])

heading('2.  Other operating records worth loading')
table(['Source', 'Detail'], widths=[4.6, 12.0], rows=[
    ['Welfare / lone-worker checks', 'Timestamped welfare checks in every HOTC daily log (2.7 years) + supervisor "welfare / site checks on our guards" shifts in timesheets + 5,975 logged check-ins in LCF pilot data'],
    ['Hazard & Risk Register', 'Populated SafetySeek-era register (PDF) - needs re-review/re-date (review dates lapsed) and re-ordering so violence/aggression, lone work and fatigue lead'],
    ['Training & competency', 'Onboarding pack export: 39 officers x 9 document types (COA, driver licence, first aid, WW training, inductions; partially populated) + PSPLA-verified COA register (31 staff, 10 Nov 26) + 22-name CoA return + 29 ServeWise certificates'],
    ['Induction acknowledgements', '5 DocuSign-executed witnessed Mitre 10 packs (7 May 26) + ~24 onboarding packs + 65 CRL station induction attendance entries (19-28 Feb 26)'],
    ['Injury management / RTW', 'Occupational-therapist graduated return-to-work plan in effect 9 Nov - 21 Dec 2026'],
    ['Equipment / PPE issue', 'Equipment-issued block (vests, bodycams, radios, keys) opening every HOTC daily log'],
])

heading('3.  Team meetings — payroll-evidenced position')
p = doc.add_paragraph()
p.add_run('Staff meetings are evidenced by payroll: SLS unified timesheets record 80 head-office Admin-hours entries '
          '(Mar - Nov 2026), including two cohorts with fully overlapping paid attendance (20 Apr: 5 staff, identical '
          '11:30-12:30 hour; 17 Aug: 3 staff, corroborated by same-day field notes), plus 8 Apr with two staff '
          'overlapping (note "Meeting at head office") and a third sequential, and a payroll-evidenced disciplinary '
          'meeting (2 Jun; a separately minuted disciplinary process is on file in the 19 Mar 2026 Investigation '
          'Summary). The extract with attendee names, times and verbatim notes is attached '
          '(ASG_SLS_Team_Meeting_Evidence_Extract_2026.xlsx) and can be migrated as meeting attendance evidence. '
          'What the timesheets do not record is topics: no minutes or toolbox sign-offs were kept, and none have '
          'been created retrospectively. Two possible existing sources for topic-level records before anything is '
          'backfilled: ').bold = False
doc.add_paragraph('Connecteam: a "Health & Safety Toolbox Meeting (APP FORM)" task is mandatory on every rostered shift - '
                  'if guards have been completing the form, the submissions export IS the delivery record. Please export.', style='List Bullet')
doc.add_paragraph('SafetySeek history: any pre-2025 records from when the system was last active (acknowledgements, '
                  'hazard register versions, incidents) - please export before rebuilding.', style='List Bullet')
p = doc.add_paragraph()
r = p.add_run('If both come back empty, the recorded meeting cadence starts this week (Thursday induction 19 Nov is the first '
              'opportunity) rather than being backfilled.')
r.italic = True

heading('4.  Access')
p = doc.add_paragraph()
p.add_run('All source files are on hand and can be shared with you and Gina directly (originals or the staged evidence pack). '
          'Client-named registers (Bunnings / Woolworths) are provided for the H&S system only and contain guard and customer '
          'names - handle under the engagement confidentiality.')

doc.save(OUT)
print('DOCX ->', OUT)
