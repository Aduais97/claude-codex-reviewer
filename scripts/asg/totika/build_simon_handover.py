#!/usr/bin/env python3
"""Simon handover deliverables: cover note PDF + trimmed register + pre-flight zip.

Run modes:
  python3 build_simon_handover.py          -> builds cover note + trimmed register
  python3 build_simon_handover.py zip      -> runs pre-flight checks, then builds the zip
Client-facing copy is written dash-free per ASG house rule.
"""
import os, sys, re, zipfile
from openpyxl import load_workbook

T = os.path.expanduser('~/Desktop/ASG/Totika')
COVER = os.path.join(T, '00_Cover_Note_for_Simon.pdf')
REG_SIMON = os.path.join(T, 'ASG_Totika_Evidence_Register_SIMON.xlsx')
ZIP = os.path.join(T, 'ASG_Totika_Evidence_Pack_Nov2026.zip')

ZIP_CONTENTS = ['00_Cover_Note_for_Simon.pdf', 'Evidence',
                'ASG_Totika_Evidence_Register_SIMON.xlsx',
                'ASG_SafetySeek_Migration_Manifest_Nov2026.docx',
                'ASG_Team_Meeting_Evidence_Extract_FOR_SIMON.xlsx']


def build_cover():
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.colors import HexColor
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    NAVY = HexColor('#1B2A4A'); GREY = HexColor('#4A4A5A')
    doc = SimpleDocTemplate(COVER, pagesize=A4, leftMargin=54, rightMargin=54, topMargin=56, bottomMargin=50)
    B = ParagraphStyle('b', fontName='Helvetica', fontSize=9.8, leading=13.6, alignment=TA_LEFT, spaceAfter=6)
    H = ParagraphStyle('h', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=NAVY, spaceBefore=8, spaceAfter=3)
    TT = ParagraphStyle('t', fontName='Helvetica-Bold', fontSize=15, leading=19, textColor=NAVY, alignment=TA_CENTER)
    E = [Paragraph('ASG Totika Category 2 Evidence Pack: Cover Note for Simon Glasgow (VINCI)', TT),
         Paragraph('Absolute Security Group Ltd (NZBN 9429050952960)  |  18 November 2026  |  Contact: Ahmad Duais (decisions), Gina (uploads and records)',
                   ParagraphStyle('s', fontName='Helvetica-Oblique', fontSize=8.5, leading=11, textColor=GREY, alignment=TA_CENTER, spaceAfter=10))]
    sections = [
        ('What this is', 'The complete evidence staging for ASG\'s Totika Category 2 prequalification (Core Criteria v3.4, questions MB1 to MB54, scored 0 to 4; Performing requires a 3 on every applicable question). This pack is for you and Gina to run the SafetySeek submission.'),
        ('What is attached', 'The Evidence folder (10 themed subfolders, redacted upload versions only); the register workbook with the question by question Upload Map (statuses READY, READY-AFTER-FIX, PENDING-RECORD, NA-JUSTIFIED); the migration manifest you confirmed on 18 November; and the full team meeting extract as a named migration source under our engagement confidentiality (it is not a SafetySeek upload file).'),
        ('Ground rule', 'Only files inside the Evidence folder ever go to SafetySeek. On insurance specifically: upload only the four NZI certificates in Evidence/Insurance (Broadform Liability 10 million, Statutory Liability 1 million, Employers Liability 1 million, Professional Indemnity 500 thousand; both group entities named insureds; period 18 Nov 2026 to 18 Nov 2027). Older BizCover and AIG certificates exist in legacy folders and are superseded. Premium payment confirmation and a possible PI limit increase are in hand.'),
        ('Honest status', 'Operating evidence is deep: incident management at scale, welfare and lone worker logs over 2.7 years, training and licensing records, client coordination. The governance cadence (toolbox series, management meetings, inspections, drills) goes live 19 November with meeting TBX-2026-001. Nothing is backdated, and signed records will flow to you and Gina as they are created.'),
        ('Your five deliverables', '1. Your engagement letter, please stating your ProfNZISM and HASANZ member body status (the MB8 anchor wants that wording). 2. Your gap review written up as the HSMS audit report for MB14. 3. Written confirmation of the member scheme and your HASANZ standing before 25 November (we need it for tender wording). 4. SafetySeek historical exports and Connecteam form submission exports per the manifest. 5. Your entity scope ruling (ASG Ltd versus SLS RTC sourced evidence) this week; it gates which monitoring and induction records we upload.'),
        ('Timing proposal for your agreement', 'Upload evidence early December; hold the marking to mid January 2027 so roughly eight weeks of live cadence makes a 3 defensible on the governance lines. The alternative is accepting a Developing grade in a December marking and re-marking later. Our analysis of the published Simply Security scorecard (81 percent Performing) suggests a mid January Performing in the low 80s is realistic; we would value your view.'),
        ('Platform numbering warning', 'If the submission platform numbering runs one higher than the standard criteria after MB33, map prepared answers by question text, not number, and cross check the first three questions at upload.'),
        ('Confidentiality', 'The scheme requires redaction of personal information; redacted versions are what is staged. Client named material (the COA register, the meeting extract, HOTC and Woolworths documents) is shared with you under engagement confidentiality and is not for upload in unredacted form. Nothing from outside the Evidence folder is uploaded anywhere.'),
    ]
    for h, b in sections:
        E.append(Paragraph(h, H)); E.append(Paragraph(b, B))
    doc.build(E)
    print('cover note ->', COVER)


def build_trimmed_register():
    src = os.path.join(T, 'ASG_Totika_Evidence_Register.xlsx')
    wb = load_workbook(src)
    for name in list(wb.sheetnames):
        if name not in ('Evidence Register', 'Upload Map'):
            del wb[name]
    SOFTEN = [
        (re.compile(r'\$690k[^.;)]*', re.I), 'client commercial terms (on file)'),
        (re.compile(r'fake[- ]2013[^.;)]*', re.I), 'file metadata corrected'),
        (re.compile(r'[Nn]o retrofitted addendum optics[^.;)]*'), 'present honestly as formalised in the Nov 2026 reissue'),
        (re.compile(r'\$800k[^.;)]*', re.I), 'client commercial terms (on file)'),
    ]
    n = 0
    for ws in wb:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str):
                    v = c.value
                    for pat, rep in SOFTEN:
                        v = pat.sub(rep, v)
                    if v != c.value:
                        c.value = v; n += 1
    wb.save(REG_SIMON)
    print(f'trimmed register -> {REG_SIMON} ({n} notes softened)')


def preflight():
    ok = True
    # 1. all upload-map citations exist
    import json
    um = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'totika_upload_map.json')))
    for u in um:
        for f in u.get('files', []):
            if not os.path.exists(f):
                print('FAIL broken citation:', u['mb'], f); ok = False
    # 2. no placeholder strings in Evidence text-extractable files
    import fitz
    from docx import Document
    PLACEHOLDER = re.compile(r'\[to confirm|\[VERIFY|\bTBC\b|\[AHMAD|\[time\]|\[Facilitator', re.I)
    for root, _, files in os.walk(os.path.join(T, 'Evidence')):
        for fn in files:
            p = os.path.join(root, fn)
            try:
                if fn.endswith('.pdf'):
                    txt = ''.join(pg.get_text() for pg in fitz.open(p))
                elif fn.endswith('.docx'):
                    d = Document(p)
                    txt = '\n'.join(par.text for par in d.paragraphs)
                else:
                    continue
            except Exception:
                continue
            m = PLACEHOLDER.search(txt)
            if m:
                print(f'FAIL placeholder "{m.group(0)}" in {p}'); ok = False
    # 3. signed SMS freshness heuristic
    sms = os.path.join(T, 'Evidence/A-Leadership-Policy/ASG_Health_and_Safety_Policy_SMS_Nov2026.pdf')
    import datetime
    age = (datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(sms))).days
    if age > 0:
        print(f'WARN: staged SMS PDF is {age} day(s) old. Confirm it is the SIGNED regeneration before sending.')
    # 4. zip inputs present
    for item in ZIP_CONTENTS:
        if not os.path.exists(os.path.join(T, item)):
            print('FAIL missing zip input:', item); ok = False
    return ok


def build_zip():
    if not preflight():
        print('\nPRE-FLIGHT FAILED. Fix the items above; zip NOT built.')
        sys.exit(1)
    if os.path.exists(ZIP):
        os.remove(ZIP)
    with zipfile.ZipFile(ZIP, 'w', zipfile.ZIP_DEFLATED) as z:
        for item in ZIP_CONTENTS:
            p = os.path.join(T, item)
            if os.path.isdir(p):
                for root, _, files in os.walk(p):
                    for fn in files:
                        if fn.startswith('.'):
                            continue
                        fp = os.path.join(root, fn)
                        z.write(fp, os.path.relpath(fp, T))
            else:
                z.write(p, item)
    print(f'ZIP -> {ZIP} ({os.path.getsize(ZIP)//1024//1024} MB)')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'zip':
        build_zip()
    else:
        build_cover()
        build_trimmed_register()
        print('\nPre-flight preview:')
        preflight()
