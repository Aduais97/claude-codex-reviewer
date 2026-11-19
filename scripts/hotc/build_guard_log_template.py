#!/usr/bin/env python3
"""Guard-facing HOTC daily patrol log template (v2) — adds the formal Response Call
Log + end-of-shift Capacity Summary fields committed to the HOTC board for the
Oct-Dec 2026 quarter. Locked visual style (navy #1F3864 / red #B01E1E)."""
import os
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

NAVY = RGBColor(0x1F, 0x38, 0x64); RED = RGBColor(0xB0, 0x1E, 0x1E)
GREY = RGBColor(0x55, 0x55, 0x55); SUBNAVY = RGBColor(0x2E, 0x4A, 0x7A)

def bottom_border(p, color='1F3864', sz='12'):
    pPr = p._p.get_or_add_pPr(); pbdr = OxmlElement('w:pBdr')
    b = OxmlElement('w:bottom'); b.set(qn('w:val'), 'single'); b.set(qn('w:sz'), sz)
    b.set(qn('w:space'), '2'); b.set(qn('w:color'), color)
    pbdr.append(b); pPr.append(pbdr)

doc = Document()
for s in doc.sections:
    s.top_margin = s.bottom_margin = Cm(1.8); s.left_margin = s.right_margin = Cm(2.0)
doc.styles['Normal'].font.name = 'Calibri'; doc.styles['Normal'].font.size = Pt(10.5)

t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run('HEART OF THE CITY — CBD SAFETY TEAM'); r.bold = True; r.font.size = Pt(17); r.font.color.rgb = NAVY
st = doc.add_paragraph(); st.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = st.add_run('Daily Patrol Log — Guard Template (v2)'); r.font.size = Pt(12); r.font.color.rgb = GREY
sub = doc.add_paragraph(); sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub.add_run('Absolute Security Group  |  Auckland CBD  |  Effective 1 October 2026'); r.font.size = Pt(9); r.font.color.rgb = GREY
bottom_border(sub)

def heading(text):
    p = doc.add_paragraph(); r = p.add_run(text); r.bold = True; r.font.size = Pt(12.5); r.font.color.rgb = NAVY
    bottom_border(p); p.paragraph_format.space_after = Pt(6); p.paragraph_format.space_before = Pt(12)

def para(text, bold=False, color=None, size=10.5, italic=False):
    p = doc.add_paragraph(); r = p.add_run(text); r.bold = bold; r.italic = italic
    r.font.size = Pt(size)
    if color: r.font.color.rgb = color
    return p

def bullet(text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet'); p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.left_indent = Cm(1.0)
    if bold_prefix:
        r = p.add_run(bold_prefix); r.bold = True; r.font.size = Pt(10)
    r = p.add_run(text); r.font.size = Pt(10)

heading('Why this template')
para('Nothing about how you log your shift changes — same shift headers, equipment list and '
     'timestamped entries as now. This version adds TWO new mandatory items, reported to the '
     'Heart of the City board every quarter: logging every response call with the time you were '
     'called AND the time you arrived, and a short Capacity Summary at the end of each shift.',
     size=10)

heading('Shift structure (unchanged)')
bullet('[Morning Shift Deployed] / [Afternoon Shift Deployed] / [Night Shift Deployed] header.')
bullet('Equipment received: list every item (swipe cards, keys, vests, Ops Phone, bodycams, radios).')
bullet('Timestamped entries in 24-hour time (e.g. 06:31, 14:07, 23:45 — not 2:30 or 11pm).')
bullet('Note: All photos and videos will be sent at the end of the shift report.')

heading('NEW — Response Call Log (every response call, no exceptions)')
para('For EVERY response call or request you receive, your entries must show all four of these:', size=10)
bullet('the time the call was received — e.g. "14:07 — Received a response call from …"', bold_prefix='1. ')
bullet('who called and the location.', bold_prefix='2. ')
bullet('the time you arrived on scene — e.g. "14:15 — Arrived at …"', bold_prefix='3. ')
bullet('the outcome (moved on / items recovered / gone on arrival / Police attended, etc.).', bold_prefix='4. ')
p = para('If you cannot go straight away, say so in the entry:', size=10)
bullet('DELAYED — and why (e.g. "DELAYED — engaged on a call at Commercial Bay").', bold_prefix='• ')
bullet('UNABLE TO ATTEND — and why (e.g. "UNABLE TO ATTEND — two simultaneous calls, no second team").', bold_prefix='• ')
para('Never leave a call with no arrival time and no reason — a call with no outcome recorded '
     'counts against the team.', bold=True, color=RED, size=10)

heading('NEW — End-of-Shift Capacity Summary (last entry before handover)')
para('Fill in these five lines at the end of every shift:', size=10)
for line in ['Response calls received:  ____',
             'Attended:  ____',
             'Delayed (attended late):  ____',
             'Unable to attend:  ____',
             'Longest response time:  ____ minutes']:
    p = doc.add_paragraph(); p.paragraph_format.left_indent = Cm(1.0)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(line); r.font.size = Pt(10.5); r.font.color.rgb = SUBNAVY; r.bold = True

heading('Worked example')
for line in ['14:07 — Received a response call from Cotton On regarding a male concealing items; '
             'DELAYED — engaged on a vagrant move-on at Aotea Square.',
             '14:21 — Arrived at Cotton On. Individual had left; staff provided a photo. (Photo on file.)',
             '…',
             '22:25 — Capacity Summary: calls received 6 / attended 6 / delayed 1 / unable 0 / '
             'longest response 14 minutes.',
             '22:30 — Changeover to the Night Shift.']:
    p = doc.add_paragraph(); p.paragraph_format.left_indent = Cm(0.6); p.paragraph_format.space_after = Pt(2)
    r = p.add_run(line); r.font.size = Pt(9.5); r.italic = True; r.font.color.rgb = GREY

out1 = os.path.expanduser('~/Desktop/ASG/HOTC/2026/HOTC_Guard_Daily_Log_Template.docx')
doc.save(out1)
out2 = os.path.expanduser('~/Downloads/HOTC_Guard_Daily_Log_Template.docx')
doc.save(out2)
print(out1); print(out2)
