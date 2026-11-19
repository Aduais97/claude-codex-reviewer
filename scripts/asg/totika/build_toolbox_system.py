#!/usr/bin/env python3
"""ASG Toolbox Meeting System — compliant templates + programme + prepared packs.

Aligns with the SafetySeek Migration Manifest (18 Nov 2026) honest position:
no backdated records; a documented system with records accruing from 19 Nov 2026.
Compliance anchors: HSWA 2015 ss58-61 (worker engagement/participation),
Totika MB28 (regular meetings + frequency rationale + records), MB2 (policy
communicated with sign-off), MB26 (open communication), MB30 (controls communicated).

Outputs -> ~/Desktop/ASG/Operations/Toolbox Meetings/
Copies of template + programme -> ~/Desktop/ASG/Totika/Evidence/F-Engagement-Toolbox/
"""
import os, shutil
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

NAVY = RGBColor(0x1B, 0x2A, 0x4A)
GREY = RGBColor(0x4A, 0x4A, 0x5A)

OUTDIR = os.path.expanduser('~/Desktop/ASG/Operations/Toolbox Meetings')
EVID = os.path.expanduser('~/Desktop/ASG/Totika/Evidence/F-Engagement-Toolbox')
os.makedirs(OUTDIR, exist_ok=True)
os.makedirs(EVID, exist_ok=True)


def new_doc():
    doc = Document()
    import datetime as _dt
    cp = doc.core_properties
    cp.author = 'Absolute Security Group Ltd'
    cp.created = _dt.datetime.now(); cp.modified = _dt.datetime.now()
    for s in doc.sections:
        s.top_margin = Cm(1.8); s.bottom_margin = Cm(1.8)
        s.left_margin = Cm(2.0); s.right_margin = Cm(2.0)
    st = doc.styles['Normal']
    st.font.name = 'Calibri'; st.font.size = Pt(10.5)
    return doc


def title(doc, text, sub=None):
    t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run(text); r.bold = True; r.font.size = Pt(17); r.font.color.rgb = NAVY
    if sub:
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(sub); r.font.size = Pt(9.5); r.font.color.rgb = GREY


def heading(doc, text, size=12):
    h = doc.add_paragraph()
    r = h.add_run(text); r.bold = True; r.font.size = Pt(size); r.font.color.rgb = NAVY


def kv_table(doc, pairs, label_w=4.2, val_w=12.4):
    tb = doc.add_table(rows=0, cols=2)
    tb.style = 'Table Grid'
    for k, v in pairs:
        row = tb.add_row().cells
        row[0].width = Cm(label_w); row[1].width = Cm(val_w)
        p = row[0].paragraphs[0]; r = p.add_run(k); r.bold = True; r.font.size = Pt(9.5)
        p = row[1].paragraphs[0]; r = p.add_run(v); r.font.size = Pt(9.5)
    doc.add_paragraph()
    return tb


def attendance_table(doc, rows=10):
    heading(doc, 'Attendance (each attendee signs to confirm attendance and understanding)')
    tb = doc.add_table(rows=1, cols=3)
    tb.style = 'Table Grid'
    widths = [6.0, 5.4, 5.2]
    for i, h in enumerate(['Name (print)', 'Role / Site', 'Signature']):
        c = tb.rows[0].cells[i]; c.width = Cm(widths[i])
        p = c.paragraphs[0]; r = p.add_run(h); r.bold = True; r.font.size = Pt(9.5)
    for _ in range(rows):
        cells = tb.add_row().cells
        for i in range(3):
            cells[i].width = Cm(widths[i])
            cells[i].paragraphs[0].add_run(' ').font.size = Pt(12)
    doc.add_paragraph()


def actions_table(doc, rows=4):
    heading(doc, 'Actions arising')
    tb = doc.add_table(rows=1, cols=4)
    tb.style = 'Table Grid'
    widths = [7.0, 3.4, 2.8, 3.4]
    for i, h in enumerate(['Action', 'Owner', 'Due date', 'Closed (date / initials)']):
        c = tb.rows[0].cells[i]; c.width = Cm(widths[i])
        p = c.paragraphs[0]; r = p.add_run(h); r.bold = True; r.font.size = Pt(9.5)
    for _ in range(rows):
        cells = tb.add_row().cells
        for i in range(4):
            cells[i].width = Cm(widths[i])
            cells[i].paragraphs[0].add_run(' ').font.size = Pt(12)
    doc.add_paragraph()


def record_form(doc, meeting_no='', date='', time='', location='', facilitator='', topic='',
                talking_points=None, discussion_prompts=None):
    kv_table(doc, [
        ('Meeting number', meeting_no),
        ('Date / time / duration', f'{date}    {time}'),
        ('Location / site', location),
        ('Facilitator', facilitator),
        ('Topic(s)', topic),
        ('Reference material', 'ASG toolbox topic sheet / SOP / policy section used (attach or name)'),
    ])
    if talking_points:
        heading(doc, 'Key points covered')
        for tp in talking_points:
            doc.add_paragraph(tp, style='List Bullet')
        doc.add_paragraph()
    heading(doc, 'Hazards, issues and feedback raised by workers (two-way: record even if nil)')
    for prompt in (discussion_prompts or ['', '', '']):
        p = doc.add_paragraph(style='List Bullet')
        r = p.add_run(prompt if prompt else '                                                            ')
        r.font.size = Pt(10)
    doc.add_paragraph()
    actions_table(doc)
    attendance_table(doc)
    heading(doc, 'Record keeping')
    p = doc.add_paragraph()
    r = p.add_run('Facilitator: complete the Connecteam Health and Safety Toolbox Meeting APP FORM for this meeting, '
                  'file this signed sheet in the Toolbox Delivery Register folder, and upload a copy to SafetySeek. '
                  'Add one line to the Toolbox Delivery Register (xlsx).')
    r.font.size = Pt(9.5); r.font.color.rgb = GREY
    sig = doc.add_paragraph()
    sig.add_run('\nFacilitator signature: ______________________________    Date: ________________').bold = True


# ---------------------------------------------------------------- 1. blank template
doc = new_doc()
title(doc, 'ASG Toolbox Meeting Record',
      'Absolute Security Group Ltd  |  Health and Safety Toolbox Meeting  |  Version 1.0, issued 18 November 2026')
doc.add_paragraph()
record_form(doc)
tpl = os.path.join(OUTDIR, 'ASG_Toolbox_Meeting_Record_TEMPLATE_v1.0.docx')
doc.save(tpl)

# ---------------------------------------------------------------- 2. programme
doc = new_doc()
title(doc, 'ASG Toolbox Meeting Programme FY27',
      'Absolute Security Group Ltd  |  Version 1.0, issued 18 November 2026  |  Owner: H&S Administrator (Gina), advisor Simon Glasgow ProfNZISM (VINCI)')
doc.add_paragraph()
heading(doc, '1. Purpose and compliance basis', 13)
p = doc.add_paragraph()
p.add_run('This programme gives effect to ASG\'s duties to engage with workers and enable worker participation in '
          'health and safety matters (Health and Safety at Work Act 2015, sections 58 to 61) and to the worker '
          'engagement commitments in the ASG Health and Safety Policy and Safety Management System (November 2026). '
          'It defines the meeting rhythm, topics, records and responsibilities so that delivery is demonstrable to '
          'clients and prequalification assessors. Records accrue from 19 November 2026; no earlier delivery '
          'records exist and none are to be created retrospectively.')
heading(doc, '2. Meeting rhythm and frequency rationale', 13)
for b in ['Per shift: a brief safety check-in delivered through the Connecteam Health and Safety Toolbox Meeting '
          'APP FORM task that is already mandatory on every rostered shift. The completed form becomes the delivery '
          'record; completion rates are monitored monthly from 19 November 2026.',
          'Weekly (Thursday induction and refresher session, Queen Street office): a 10 to 15 minute toolbox talk '
          'using the topic schedule below, recorded on the ASG Toolbox Meeting Record with signed attendance. '
          'Weekly talks may deliver scheduled topics early where operational risk warrants it.',
          'Monthly: one formal toolbox meeting per site group covering the scheduled monthly topic, plus review of '
          'incidents, hazards raised and open actions. Recorded on the ASG Toolbox Meeting Record.',
          'Rationale: ASG guards work dispersed, often alone and at night across hospitality, retail and patrol '
          'sites, so a high-frequency light rhythm (per shift and weekly) is used rather than a single monthly '
          'gathering, with the monthly formal meeting providing depth and action tracking.']:
    doc.add_paragraph(b, style='List Bullet')
heading(doc, '2a. Worker representation', 12)
p = doc.add_paragraph()
p.add_run('In addition to these meetings, any worker may raise a health and safety matter directly with the H&S '
          'Administrator or any manager at any time, and workers may at any time request the election of one or '
          'more Health and Safety Representatives under Part 3 of the Health and Safety at Work Act 2015 and the '
          'Health and Safety at Work (Worker Engagement, Participation and Representation) Regulations 2016. Any '
          'such request will be facilitated in accordance with the Regulations.')
heading(doc, '3. Topic schedule (mapped to ASG principal risks)', 13)
tb = doc.add_table(rows=1, cols=3); tb.style = 'Table Grid'
for i, h in enumerate(['Month', 'Topic', 'Linked material']):
    c = tb.rows[0].cells[i]
    r = c.paragraphs[0].add_run(h); r.bold = True; r.font.size = Pt(9.5)
SCHEDULE = [
    ('Nov 2026', 'H&S policy launch, incident reporting and notifiable events', 'Signed H&S Policy and SMS Nov 2026; incident reporting procedure'),
    ('Dec 2026', 'Violence and aggression: de-escalation and use of force expectations', 'Guard Field Manual modules; recent investigation learnings'),
    ('Jan 2027', 'Lone working and welfare checks', 'Welfare check procedure; HOTC daily log practice'),
    ('Feb 2027', 'Fatigue and night work', 'Fatigue Policy (numeric limits); rostering rules'),
    ('Mar 2027', 'Body worn cameras and privacy', 'BWC SOP; footage retention statement'),
    ('Apr 2027', 'Emergency response including assault, fire and earthquake', 'SMS emergency section; assault response procedure'),
    ('May 2027', 'Alcohol, drugs and fitness for work', 'D&A policy and enforcement SOP'),
    ('Jun 2027', 'PPE and equipment: issue, checks and faults', 'PPE register; equipment issue log practice'),
    ('Jul 2027', 'Manual handling, slips, trips and falls', 'Toolbox topic library'),
    ('Aug 2027', 'Driving and journey safety for patrols', 'Driving and journey management policy'),
    ('Sep 2027', 'Mental wellbeing and stress', 'Wellbeing and EAP information'),
    ('Oct 2027', 'Hazard reporting and annual risk register review', 'Hazard and Risk Register (current version)'),
]
for m, t_, l in SCHEDULE:
    cells = tb.add_row().cells
    for i, v in enumerate([m, t_, l]):
        r = cells[i].paragraphs[0].add_run(v); r.font.size = Pt(9)
doc.add_paragraph()
heading(doc, '4. Records and retention', 13)
for b in ['Every meeting is recorded on the ASG Toolbox Meeting Record (template v1.0) with signed attendance.',
          'The facilitator completes the Connecteam APP FORM for the same meeting.',
          'Signed records are filed in the Toolbox Delivery Register folder and uploaded to SafetySeek; one index '
          'line is added to the Toolbox Delivery Register spreadsheet.',
          'Records are retained for a minimum of 5 years and are producible to clients and assessors on request.',
          'The H&S Administrator reports delivery rates and themes raised by workers at the monthly management '
          'meeting; the programme is reviewed annually.']:
    doc.add_paragraph(b, style='List Bullet')
prog = os.path.join(OUTDIR, 'ASG_Toolbox_Programme_FY27_v1.0.docx')
doc.save(prog)

# ---------------------------------------------------------------- 3. prepared packs
PACKS = [
    dict(no='TBX-2026-001', date='Thursday 19 November 2026', time='[time]  (10 to 15 minutes)',
         loc='ASG Office, 7/220 Queen Street, Auckland (Thursday induction and refresher session)',
         fac='[Facilitator name]',
         topic='H&S policy launch, incident reporting and notifiable events',
         prereq='PREREQUISITE: deliver this meeting only after both directors have signed the H&S Policy/SMS. If not '
                'yet signed at delivery, amend the first talking point verbally to "is being signed this week" and do '
                'NOT use this attendance sheet as the policy acknowledgement record.',
         points=['The ASG Health and Safety Policy and Safety Management System (November 2026) has been signed by '
                 'the directors: what it commits ASG and every guard to.',
                 'Everyone\'s duty to take reasonable care and report: what counts as an incident, a near miss and '
                 'a hazard, and how to report each one on shift.',
                 'Notifiable events: what must reach management immediately so WorkSafe notification can be assessed.',
                 'How to raise any H&S issue at any time, and what happens after you raise one.',
                 'Attendees sign below to confirm the policy was presented and understood (this sheet doubles as '
                 'the policy acknowledgement record).'],
         prompts=['Questions or concerns raised about the policy:', 'Hazards or issues raised from current sites:', 'Other feedback:']),
    dict(no='TBX-2026-002', date='Thursday 26 November 2026', time='[time]  (10 to 15 minutes)',
         loc='ASG Office, 7/220 Queen Street, Auckland (Thursday induction and refresher session)',
         fac='[Facilitator name]',
         topic='Lone working and welfare checks',
         points=['Why welfare checks exist: dispersed, solo and night work is ASG\'s highest-exposure arrangement.',
                 'The check-in rhythm: scheduled welfare checks, what to do on a missed check, escalation steps.',
                 'Duress options on shift: phones, radios, body worn cameras and safe havens.',
                 'What gets logged and why the daily log matters as a safety record.'],
         prompts=['Sites or shifts where checking in is hard in practice:', 'Suggestions to improve the welfare check routine:', 'Other feedback:']),
    dict(no='TBX-2026-003', date='[Date, December 2026]', time='[time]  (15 minutes)',
         loc='[Site / office]',
         fac='[Facilitator name]',
         topic='Violence and aggression: de-escalation and use of force expectations',
         points=['Learnings from recent incidents: early de-escalation, creating distance, calling for backup.',
                 'The lawful use of force ladder and ASG\'s expectations: minimum force, last resort, report everything.',
                 'Body worn camera activation expectations during conflict.',
                 'Post-incident: welfare support, reporting and investigation process.'],
         prompts=['Venues or situations currently of concern to guards:', 'Training needs raised:', 'Other feedback:']),
]
pack_paths = []
for pk in PACKS:
    doc = new_doc()
    title(doc, 'ASG Toolbox Meeting Record',
          f"Absolute Security Group Ltd  |  Prepared meeting pack {pk['no']}  |  Record is complete only when attendance is signed")
    doc.add_paragraph()
    if pk.get('prereq'):
        w = doc.add_paragraph()
        r = w.add_run(pk['prereq']); r.bold = True; r.font.size = Pt(9.5); r.font.color.rgb = RGBColor(0xC0, 0x39, 0x2B)
    record_form(doc, meeting_no=pk['no'], date=pk['date'], time=pk['time'], location=pk['loc'],
                facilitator=pk['fac'], topic=pk['topic'], talking_points=pk['points'],
                discussion_prompts=pk['prompts'])
    out = os.path.join(OUTDIR, f"Toolbox_{pk['no']}_{pk['topic'].split(',')[0].split(':')[0].replace(' ', '_')}.docx")
    doc.save(out); pack_paths.append(out)

# ---------------------------------------------------------------- 4. delivery register
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
wb = Workbook(); ws = wb.active; ws.title = 'Toolbox Delivery Register'
hdrs = ['Meeting no', 'Date', 'Type (per-shift / weekly / monthly)', 'Topic', 'Site / location',
        'Facilitator', 'Attendees (count)', 'Signed sheet filed (Y/N)', 'Connecteam form done (Y/N)',
        'Uploaded to SafetySeek (Y/N)', 'Actions raised', 'Notes']
widths = [12, 12, 16, 34, 20, 16, 10, 12, 14, 14, 24, 28]
NAVY_F = PatternFill('solid', fgColor='1B2A4A')
for c, (h, w) in enumerate(zip(hdrs, widths), 1):
    cell = ws.cell(1, c, h)
    cell.font = Font(name='Calibri', size=10, bold=True, color='FFFFFF')
    cell.fill = NAVY_F
    cell.alignment = Alignment(wrap_text=True, vertical='top')
    cell.border = Border(*[Side(style='thin', color='D0D5DD')] * 4)
    ws.column_dimensions[get_column_letter(c)].width = w
ws.freeze_panes = 'A2'
PLANNED = [
    ('TBX-2026-001', '19/11/2026', 'weekly', 'H&S policy launch, incident reporting and notifiable events'),
    ('TBX-2026-002', '26/11/2026', 'weekly', 'Lone working and welfare checks'),
    ('TBX-2026-003', 'Dec 2026', 'monthly', 'Violence and aggression: de-escalation and use of force expectations'),
]
for i, (no, dt, typ, topic) in enumerate(PLANNED, 2):
    ws.cell(i, 1, no); ws.cell(i, 2, dt); ws.cell(i, 3, typ); ws.cell(i, 4, topic)
    ws.cell(i, 5, 'ASG Office, Queen St'); ws.cell(i, 12, 'PLANNED - complete this row only AFTER delivery')
reg = os.path.join(OUTDIR, 'ASG_Toolbox_Delivery_Register.xlsx')
wb.save(reg)

# ---------------------------------------------------------------- stage copies
for p in [tpl, prog]:
    shutil.copy(p, EVID)
print('Built in', OUTDIR, ':')
for p in [tpl, prog, reg] + pack_paths:
    print('  -', os.path.basename(p))
print('Template + programme copied to', EVID)
