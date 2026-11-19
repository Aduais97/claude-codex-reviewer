from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

NAVY = RGBColor(0x0B, 0x1F, 0x3A)
GOLD = RGBColor(0xB8, 0x8A, 0x2E)
GREY = RGBColor(0x55, 0x55, 0x55)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LBLUE = "DCE3EC"

doc = Document()
for sec in doc.sections:
    sec.top_margin = Inches(0.8); sec.bottom_margin = Inches(0.8)
    sec.left_margin = Inches(0.9); sec.right_margin = Inches(0.9)
s = doc.styles['Normal']; s.font.name='Calibri'; s.font.size=Pt(10.5)

def shade(cell, hexcol):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement('w:shd'); sh.set(qn('w:val'),'clear'); sh.set(qn('w:fill'),hexcol)
    tcPr.append(sh)

def h1(text, n=None):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(12); p.paragraph_format.space_after = Pt(4)
    r = p.add_run((f"{n}.  " if n else "") + text); r.bold=True; r.font.size=Pt(13); r.font.color.rgb=NAVY
    return p

def body(text, after=4, bullet=False, indent=0):
    p = doc.add_paragraph(style='List Bullet' if bullet else None)
    p.paragraph_format.space_after = Pt(after)
    if indent: p.paragraph_format.left_indent = Inches(indent)
    p.add_run(text); return p

def kv(label, value):
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(1)
    r=p.add_run(label+'  '); r.bold=True; r.font.size=Pt(10); r.font.color.rgb=GREY
    p.add_run(value).font.size=Pt(10)

# ---------- Header band ----------
t = doc.add_table(rows=1, cols=1); t.style=None
cell = t.rows[0].cells[0]; shade(cell, "0B1F3A")
p = cell.paragraphs[0]; p.paragraph_format.space_after=Pt(2)
r = p.add_run('ABSOLUTE SECURITY GROUP'); r.bold=True; r.font.size=Pt(18); r.font.color.rgb=WHITE
p2 = cell.add_paragraph(); r2=p2.add_run('Scope of Works & Proposal'); r2.font.size=Pt(12); r2.font.color.rgb=RGBColor(0xD9,0xB8,0x6B)
cell.paragraphs[0].paragraph_format.space_before=Pt(6)
p2.paragraph_format.space_after=Pt(6)

doc.add_paragraph().paragraph_format.space_after=Pt(2)
kv('Prepared for:', 'Colliers — Property Management (Attn: Tom Ogg, Sam McGowan)')
kv('Site:', 'Chancery Carpark & associated managed property, Auckland CBD')
kv('Prepared by:', 'Ahmad Duais, CEO — Absolute Security Group Limited')
kv('Date:', '10 June 2026')
kv('Reference:', 'Safety Information & Other Actions — post-walkthrough')

# ---------- 1 Background ----------
h1('Background', 1)
body('Following our introduction via Heart of the City and the on-site walkthrough of the Chancery Carpark, this '
     'document sets out the proposed scope of works to address current safety issues and prevent repeat offending. '
     'It covers the immediate (core) works plus optional ongoing scope, to be confirmed at the building-owner '
     'meeting on Thursday. Absolute Security Group is New Zealand’s only distributor of the Mosquito anti-loitering system.')

# ---------- 2 Site & risk ----------
h1('Site & Risk Summary', 2)
body('Repeat anti-social behaviour and unauthorised access at the carpark, concentrated in peak-risk periods.', bullet=True)
body('One of the currently installed Mosquito anti-loitering units is damaged and not operating effectively; '
     'original supplier unknown.', bullet=True)
body('Complex manager requires a direct, immediate line to a responsive security team.', bullet=True)

# ---------- 3 Core scope ----------
h1('Scope of Works — Core (Immediate)', 3)
body('3.1  Mosquito system service & recalibration — on-site diagnostic of the damaged unit, repair or '
     'replacement, and frequency calibration / placement optimisation of all units (as NZ’s only distributor).')
body('3.2  One-week deterrence operation — a dedicated security officer stationed on-site over a continuous '
     'seven-day period to deter repeat offending, coordinated alongside the HOTC safety team, with body-worn '
     'cameras and full incident reporting.')
body('3.3  Trespass enforcement — issuing and managing trespass notices end-to-end under delegated authority '
     '(subject to written authorisation from Colliers / the building owners).')
body('3.4  24/7 rapid-response line — direct 09 number for the complex manager (already provided), with the '
     'team personally introduced for immediate assistance.')

# ---------- 4 Additional scope ----------
h1('Additional / Ongoing Scope (to confirm Thursday)', 4)
body('Scheduled patrol coverage across the wider Colliers-managed portfolio, frequency configurable to risk.', bullet=True)
body('Ongoing dedicated / static guarding where a continuous presence is warranted.', bullet=True)
body('Mosquito maintenance plan — scheduled servicing, recalibration and unit replacement as required.', bullet=True)
body('Extension of trespass-enforcement and rapid-response coverage to additional properties.', bullet=True)

# ---------- 5 Pricing ----------
h1('Pricing Summary', 5)
body('All figures exclude GST (15%). Core works priced below; additional scope is indicative pending Thursday.', after=6)

def make_table(headers, rows, widths):
    tbl = doc.add_table(rows=1, cols=len(headers)); tbl.alignment=WD_TABLE_ALIGNMENT.LEFT
    tbl.style='Table Grid'
    hdr=tbl.rows[0].cells
    for i,htext in enumerate(headers):
        shade(hdr[i],"0B1F3A")
        pr=hdr[i].paragraphs[0]; rr=pr.add_run(htext); rr.bold=True; rr.font.size=Pt(9.5); rr.font.color.rgb=WHITE
    for row in rows:
        cells=tbl.add_row().cells
        for i,val in enumerate(row):
            pr=cells[i].paragraphs[0]; rr=pr.add_run(val); rr.font.size=Pt(9.5)
            if i==len(row)-1: pr.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    for i,w in enumerate(widths):
        for r_ in tbl.rows: r_.cells[i].width=Inches(w)
    return tbl

# Core table
sub = doc.add_paragraph(); sub.paragraph_format.space_before=Pt(2); sub.paragraph_format.space_after=Pt(2)
sr=sub.add_run('Core works'); sr.bold=True; sr.font.size=Pt(10.5); sr.font.color.rgb=GOLD
make_table(
    ['Item','Basis','Total (excl GST)'],
    [
     ['Mosquito service & recalibration (all units)','1 on-site visit','$450.00'],
     ['Replacement Mosquito unit (if required)','Per unit, supply & install','from $2,250.00 *'],
     ['One-week deterrence operation — dedicated officer','12 hrs/day × 7 days = 84 hrs @ $45.00/hr','$3,780.00'],
     ['Trespass delegation setup & enforcement','Under delegated authority','Included'],
     ['24/7 rapid-response line','Direct 09 line + introduction','Included'],
    ],
    [3.4,2.2,1.4]
)
# Totals
tt = make_table(
    ['', 'Core subtotal (excl GST)','$4,230.00'][0:0] + ['Summary','','Amount'],
    [
     ['Core subtotal (excl replacement unit)','','$4,230.00'],
     ['GST (15%)','','$634.50'],
     ['Core total (incl GST)','','$4,864.50'],
    ],
    [3.4,2.2,1.4]
)
# bold the total row
for cell in tt.rows[-1].cells:
    for p in cell.paragraphs:
        for r in p.runs: r.bold=True; r.font.color.rgb=NAVY

body('* Replacement unit quoted following on-site diagnostic; repair preferred where viable.', after=6)

# Indicative ongoing
sub2 = doc.add_paragraph(); sub2.paragraph_format.space_before=Pt(4); sub2.paragraph_format.space_after=Pt(2)
sr2=sub2.add_run('Additional / ongoing (indicative — confirm Thursday)'); sr2.bold=True; sr2.font.size=Pt(10.5); sr2.font.color.rgb=GOLD
make_table(
    ['Item','Basis','Rate (excl GST)'],
    [
     ['Scheduled patrol coverage','Per officer hour','from $45.00/hr'],
     ['Dedicated / static guarding','Per officer hour','from $45.00/hr'],
     ['Mosquito maintenance plan','Annual programme','from $1,200.00/yr'],
    ],
    [3.4,2.2,1.4]
)

# ---------- 6 Assumptions ----------
h1('Pricing Basis, Assumptions & Exclusions', 6)
abox = doc.add_table(rows=1, cols=1); cell=abox.rows[0].cells[0]; shade(cell,LBLUE)
items = [
 'Officer rate: $45.00/hr + GST (standard commercial rate; the HOTC subsidised contract rate does not apply outside HOTC scope).',
 'One-week operation assumes 12 hrs/day coverage of the peak-risk window over 7 consecutive days (84 hrs) — adjustable on confirmation.',
 'Mosquito service fee is for diagnostic and recalibration; parts/replacement units quoted after inspection.',
 'Trespass enforcement is subject to written authorisation/delegation from Colliers or the building owners.',
 'Pricing valid for 30 days. Public-holiday and overnight loadings may apply if the operation window changes.',
]
first=True
for it in items:
    p = cell.paragraphs[0] if first else cell.add_paragraph()
    first=False
    p.paragraph_format.space_after=Pt(2)
    p.add_run('•  '+it).font.size=Pt(9.5)

# ---------- 7 Next steps ----------
h1('Next Steps', 7)
body('Colliers to provide written authorisation/delegation for trespass enforcement.', bullet=True)
body('Confirm preferred start date and operation window for the one-week deterrence operation.', bullet=True)
body('Building-owner meeting Thursday to define any additional ongoing scope; final pricing to follow.', bullet=True)
body('On approval, ASG mobilises within 24 hours (guards demonstrated 5-minute on-site response during the walkthrough).', bullet=True)

# Footer contact
doc.add_paragraph().paragraph_format.space_before=Pt(6)
fp = doc.add_paragraph(); fp.alignment=WD_ALIGN_PARAGRAPH.CENTER
fr=fp.add_run('Absolute Security Group Limited  ·  7/220 Queen St, Auckland CBD 1010  ·  09 950 4640  ·  ahmad@absolutesecuritygroup.co.nz')
fr.font.size=Pt(8.5); fr.font.color.rgb=GREY

out = os.path.expanduser('~/Desktop/ASG/Colliers/2026/Colliers_Scope_of_Works_Proposal.docx')
os.makedirs(os.path.dirname(out), exist_ok=True)
doc.save(out)
print(out)
