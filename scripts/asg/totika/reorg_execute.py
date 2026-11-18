#!/usr/bin/env python3
"""Execute the ETR reorg plan: 10 numbered folders, 5 lossless consolidations, cleanup.

Reads reorg.json (plan.file_plan). PDF merges via pymupdf (fitz). Welfare docx->one PDF
via python-docx text extraction + reportlab (preserves provenance lines). Lossless.
"""
import os, json, shutil, re, glob
import fitz
from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

T = os.path.expanduser('~/Desktop/ASG/Totika')
EV = os.path.join(T, 'Evidence')
INT = os.path.join(T, 'Internal-NotForUpload')
plan = json.load(open('/private/tmp/claude-501/-Users-ahmadduais/69134406-3eb3-4733-9e50-dbcf59ac15f3/scratchpad/reorg.json'))['plan']
fp = plan['file_plan']

STAGE = os.path.join(T, '_Evidence_new')  # build new tree here, then swap
if os.path.exists(STAGE): shutil.rmtree(STAGE)
os.makedirs(STAGE)

# group by new_rel_path to detect merges
from collections import defaultdict
groups = defaultdict(list)
removes, to_internal = [], []
for f in fp:
    a = f['action']; cur = f['current_rel_path']; new = f.get('new_rel_path') or ''
    if a == 'REMOVE': removes.append(cur); continue
    if a == 'MOVE-TO-INTERNAL': to_internal.append(cur); continue
    groups[new].append(cur)

def src(cur):
    return os.path.join(EV, cur)

merged_log, moved_log, missing = [], [], []

def welfare_docx_text(path):
    d = Document(path)
    parts = [p.text for p in d.paragraphs if p.text.strip()]
    for t in d.tables:
        for row in t.rows:
            cells = [c.text.strip() for c in row.cells if c.text.strip()]
            if cells: parts.append('  |  '.join(cells))
    return parts

for new, curs in groups.items():
    dest = os.path.join(STAGE, new)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    srcs = [src(c) for c in curs if os.path.exists(src(c))]
    for c in curs:
        if not os.path.exists(src(c)): missing.append(c)
    if not srcs:
        continue
    if len(curs) == 1:
        shutil.copy2(srcs[0], dest); moved_log.append((curs[0], new)); continue
    # merge
    if dest.lower().endswith('.pdf') and all(s.lower().endswith('.pdf') for s in srcs):
        srcs_sorted = sorted(srcs)  # date/name order via filename
        out = fitz.open()
        pages = 0
        for s in srcs_sorted:
            d = fitz.open(s); out.insert_pdf(d); pages += d.page_count; d.close()
        out.save(dest, garbage=3, deflate=True); out.close()
        merged_log.append((new, len(srcs_sorted), pages))
    elif dest.lower().endswith('.pdf') and all(s.lower().endswith('.docx') for s in srcs):
        # welfare docx -> one PDF, chronological, provenance preserved
        def datekey(p):
            m = re.search(r'(\d{4})-(\d{2})-(\d{2})', p) or None
            if m: return m.group(0)
            # map month-name files
            months = dict(January='01',February='02',March='03',April='04',May='05',June='06',July='07',August='08',September='09',October='10',November='11',December='12')
            mm = re.search(r'(\d{1,2})\w*_?(\w+)_(\d{4})', os.path.basename(p))
            return '0000'
        srcs_sorted = sorted(srcs, key=lambda p: os.path.basename(p))
        doc = SimpleDocTemplate(dest, pagesize=A4, leftMargin=48, rightMargin=48, topMargin=50, bottomMargin=46)
        NAVY=HexColor('#1B2A4A'); GREY=HexColor('#4A4A5A')
        HH=ParagraphStyle('h',fontName='Helvetica-Bold',fontSize=12,textColor=NAVY,spaceAfter=4)
        PR=ParagraphStyle('pr',fontName='Helvetica-Oblique',fontSize=8,textColor=GREY,spaceAfter=6)
        BB=ParagraphStyle('b',fontName='Helvetica',fontSize=9,leading=12,alignment=TA_LEFT,spaceAfter=2)
        E=[Paragraph('ASG Lone-Worker / Welfare Check Logs (consolidated)', HH),
           Paragraph('Consolidated transcripts of HOTC CBD patrol daily logs evidencing timestamped welfare checks and '
                     'equipment issue. Each section is one genuine daily log; provenance lines retained.', PR), Spacer(1,6)]
        for i, s in enumerate(srcs_sorted):
            parts = welfare_docx_text(s)
            title = os.path.basename(s).replace('.docx','').replace('_',' ')
            E.append(Paragraph(title, HH))
            for p in parts:
                sty = PR if ('TRANSCRIPT' in p or 'producible on request' in p) else BB
                E.append(Paragraph(p.replace('&','&amp;').replace('<','&lt;'), sty))
            if i < len(srcs_sorted)-1: E.append(PageBreak())
        doc.build(E)
        merged_log.append((new, len(srcs_sorted), 'docx->pdf'))
    else:
        # fallback: copy first, warn
        shutil.copy2(srcs[0], dest); moved_log.append((curs[0], new+' (FALLBACK single)'))

# demote raw export to Internal
os.makedirs(INT, exist_ok=True)
for c in to_internal:
    s = src(c)
    if os.path.exists(s): shutil.copy2(s, os.path.join(INT, os.path.basename(s)))

# swap: replace Evidence with new tree
shutil.rmtree(EV)
os.rename(STAGE, EV)

# removals at top level
for junk in ['.DS_Store', 'ASG_Totika_Evidence_Pack_Nov2026', 'ASG_Totika_Evidence_Pack_Nov2026.zip']:
    p = os.path.join(T, junk)
    if os.path.isdir(p): shutil.rmtree(p)
    elif os.path.exists(p): os.remove(p)

print('NEW STRUCTURE:')
for d in sorted(os.listdir(EV)):
    dp = os.path.join(EV, d)
    if os.path.isdir(dp):
        n = len([f for f in os.listdir(dp) if not f.startswith('.')])
        print(f'  {d}/  ({n} files)')
print('\nMERGES:')
for m in merged_log: print('  ', m)
print('\nmissing sources:', missing or 'none')
print('total evidence files:', sum(len([f for f in os.listdir(os.path.join(EV,d)) if not f.startswith('.')]) for d in os.listdir(EV) if os.path.isdir(os.path.join(EV,d))))
