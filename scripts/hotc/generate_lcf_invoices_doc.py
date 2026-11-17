from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
import os

NAVY = RGBColor(0x0B, 0x1F, 0x3A)
GOLD = RGBColor(0xB8, 0x8A, 0x2E)
GREY = RGBColor(0x55, 0x55, 0x55)

doc = Document()
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(10.5)

def heading(text, size=15, color=NAVY, space_before=10, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(size)
    r.font.color.rgb = color
    return p

def sub(text, size=12, color=GOLD, space_before=8):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(size)
    r.font.color.rgb = color
    return p

def kv_table(rows):
    t = doc.add_table(rows=0, cols=2)
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.style = 'Light Grid Accent 1'
    for k, v in rows:
        cells = t.add_row().cells
        rk = cells[0].paragraphs[0].add_run(k)
        rk.bold = True
        rk.font.size = Pt(10)
        cells[1].paragraphs[0].add_run(v).font.size = Pt(10)
    t.columns[0].width = Inches(1.9)
    t.columns[1].width = Inches(4.4)
    return t

# ---- Title block ----
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(0)
r = p.add_run('ABSOLUTE SECURITY GROUP LIMITED')
r.bold = True; r.font.size = Pt(16); r.font.color.rgb = NAVY

p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(2)
r = p.add_run('LCF Invoicing Instructions — Heart of the City')
r.bold = True; r.font.size = Pt(12); r.font.color.rgb = GOLD

p = doc.add_paragraph()
r = p.add_run('Enhanced CBD Safety Team (June–July 2026 Uplift) · Independent Supplier Agreement dated 1 June 2026 · Activity period 2 June – 24 July 2026')
r.font.size = Pt(9.5); r.font.color.rgb = GREY; r.italic = True

# ---- Overview ----
heading('Overview')
doc.add_paragraph(
    'Total programme price is a maximum of $41,150 + GST ($47,322.50 incl GST), invoiced as two equal '
    'instalments of $20,575 + GST. Both invoices must be DATED BEFORE 30 JUNE 2026 (LCF funding-commitment rule), '
    'even though delivery runs to 24 July. Descriptions below satisfy clause 6.4 (calculation method, hours, dates). '
    'Under clause 6.5, HOTC pays on the 20th of the month following a valid invoice, so cash from June invoices lands ~20 July.'
)

# ---- Invoice 1 ----
heading('Invoice 1 — INV-4332 (issue now)')
kv_table([
    ('Contact', 'Heart of the City Incorporated'),
    ('Issue date', '9 June 2026'),
    ('Due date', '20 July 2026 (cl 6.5 — 20th of month following valid invoice)'),
    ('Invoice number', 'INV-4332'),
    ('Reference', 'Safety & Security – June–July 2026 Uplift (LCF/CPTED)'),
    ('Amounts are', 'Tax exclusive'),
])
sub('Line item')
kv_table([
    ('Qty', '1'),
    ('Unit price', '20,575.00'),
    ('Account', '200 – Sales'),
    ('Tax rate', '15% GST on Income'),
])
sub('Description (paste into the line)')
d = doc.add_paragraph()
d.paragraph_format.left_indent = Inches(0.15)
d.add_run(
    'Enhanced CBD Safety Team — additional LCF-funded safety patrol uplift, Auckland City Centre precinct. '
    'Per executed Independent Supplier Agreement "Safety and Security – June–July 2026 Uplift" (dated 1 Jun 2026), '
    'activity period 2 Jun – 24 Jul 2026.\n'
    'Instalment 1 of 2 of the agreed fixed programme price.\n'
    'Basis: ~1,115 service hours @ $36.90/hr per guard (excl GST), deployed ~149 hrs/week across the pilot. '
    'Total programme $41,150 + GST, payable in two equal instalments of $20,575 + GST.'
).font.size = Pt(9.5)
sub('Totals', color=NAVY)
kv_table([
    ('Subtotal', '$20,575.00'),
    ('GST (15%)', '$3,086.25'),
    ('Total incl GST', '$23,661.25'),
])

# ---- Invoice 2 ----
heading('Invoice 2 — INV-4333 (issue ~23 June, must be dated before 30 June)')
kv_table([
    ('Contact', 'Heart of the City Incorporated'),
    ('Issue date', '23 June 2026 (any date before 30 June)'),
    ('Due date', '20 July 2026'),
    ('Invoice number', 'INV-4333 (next sequential)'),
    ('Reference', 'Safety & Security – June–July 2026 Uplift (LCF/CPTED)'),
    ('Amounts are', 'Tax exclusive'),
])
sub('Line item')
kv_table([
    ('Qty', '1'),
    ('Unit price', '20,575.00'),
    ('Account', '200 – Sales'),
    ('Tax rate', '15% GST on Income'),
])
sub('Description (paste into the line)')
d = doc.add_paragraph()
d.paragraph_format.left_indent = Inches(0.15)
d.add_run(
    'Enhanced CBD Safety Team — additional LCF-funded safety patrol uplift, Auckland City Centre precinct. '
    'Per executed Independent Supplier Agreement "Safety and Security – June–July 2026 Uplift" (dated 1 Jun 2026), '
    'activity period 2 Jun – 24 Jul 2026.\n'
    'Instalment 2 of 2 of the agreed fixed programme price.\n'
    'Basis: ~1,115 service hours @ $36.90/hr per guard (excl GST). '
    'Total programme $41,150 + GST, payable in two equal instalments of $20,575 + GST.'
).font.size = Pt(9.5)
sub('Totals', color=NAVY)
kv_table([
    ('Subtotal', '$20,575.00'),
    ('GST (15%)', '$3,086.25'),
    ('Total incl GST', '$23,661.25'),
])

# ---- Reconciliation ----
heading('Reconciliation')
t = doc.add_table(rows=1, cols=4)
t.style = 'Light Grid Accent 1'
hdr = t.rows[0].cells
for i, h in enumerate(['', 'Net', 'GST', 'Incl GST']):
    rr = hdr[i].paragraphs[0].add_run(h); rr.bold = True; rr.font.size = Pt(10)
for label, net, gst, incl in [
    ('Invoice 1', '$20,575.00', '$3,086.25', '$23,661.25'),
    ('Invoice 2', '$20,575.00', '$3,086.25', '$23,661.25'),
    ('TOTAL', '$41,150.00', '$6,172.50', '$47,322.50'),
]:
    cells = t.add_row().cells
    rr = cells[0].paragraphs[0].add_run(label); rr.font.size = Pt(10)
    if label == 'TOTAL': rr.bold = True
    for i, val in enumerate([net, gst, incl], start=1):
        vr = cells[i].paragraphs[0].add_run(val); vr.font.size = Pt(10)
        if label == 'TOTAL': vr.bold = True

# ---- Reminders ----
heading('Reminders')
for rem in [
    'Both invoices must be DATED BEFORE 30 JUNE 2026 (funding-commitment rule), even though Invoice 2 covers the July tail of delivery.',
    'Cash from both invoices lands ~20 JULY under clause 6.5, not in June — plan GST/payroll cashflow accordingly.',
    'Keep the daily activity/hours log watertight: it is both the delivery evidence (cl 2.6 repayment protection) and the source for the accountability report (due Edward 27 Jul, HOTC to administrators 31 Jul).',
    'Do not exceed ~1,115 hours without HOTC prior written approval (cl 6.2) — over-delivery is unpaid otherwise.',
]:
    b = doc.add_paragraph(style='List Bullet')
    b.add_run(rem).font.size = Pt(10)

out = os.path.expanduser('~/Desktop/ASG/HOTC/2026/LCF_Invoicing_Instructions.docx')
os.makedirs(os.path.dirname(out), exist_ok=True)
doc.save(out)
print(out)
