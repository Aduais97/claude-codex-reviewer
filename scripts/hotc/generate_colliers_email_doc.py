from docx import Document
from docx.shared import Pt, RGBColor, Inches
import os

NAVY = RGBColor(0x0B, 0x1F, 0x3A)
GOLD = RGBColor(0xB8, 0x8A, 0x2E)
GREY = RGBColor(0x55, 0x55, 0x55)

doc = Document()
s = doc.styles['Normal']; s.font.name='Calibri'; s.font.size=Pt(11)

def field(label, value):
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(1)
    r = p.add_run(label + '  '); r.bold = True; r.font.size = Pt(10); r.font.color.rgb = GREY
    r2 = p.add_run(value); r2.font.size = Pt(10)

def head(text):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(10); p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text); r.bold = True; r.font.size = Pt(11); r.font.color.rgb = NAVY

def body(text, space_after=4):
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(space_after)
    p.add_run(text)
    return p

# Header block
field('To:', 'Tom Ogg (Thomas.Ogg@colliers.com)')
field('Cc:', 'Sam McGowan (Sam.McGowan@colliers.com); Edward Caughey (edward.caughey@hotcity.co.nz)')
field('Subject:', 'Re: Safety Information & Other actions')

p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(4)
r = p.add_run('_'*78); r.font.color.rgb = GREY

body('Hi Tom,', space_after=6)
body('Great to meet you today — thanks for walking me through the site. As discussed:', space_after=6)

head('Mosquito system')
body('One of your currently installed Mosquito units is damaged. We can assist with getting it set up '
     'correctly and adjusting the frequencies as needed. We’re not sure who originally supplied the units, '
     'but as New Zealand’s only distributor we’re well placed to service and support them.')

head('Recommended one-week operation')
body('To prevent repeat offending, we recommend initiating a one-week operation at the site. During this '
     'period we would station a dedicated security officer and coordinate alongside the HOTC safety team for '
     'additional support.')

head('Team contact')
body('Your complex manager has been given the 09 number to reach the team directly and has been personally '
     'introduced to them, so they have immediate support available.')

head('Next steps / actions')
for t in [
    ('Tom', ' — to provide an authorisation letter or email confirming we have trespass authority / delegation from the building owners/management.'),
    ('Ahmad', ' — to send a proposal for any further assistance outside the current scope. This will be finalised based on our meeting on Thursday.'),
]:
    b = doc.add_paragraph(style='List Bullet'); b.paragraph_format.space_after = Pt(3)
    rb = b.add_run(t[0]); rb.bold = True
    b.add_run(t[1])

body('Happy to answer any questions in the meantime.', space_after=10)
body('Many thanks,', space_after=10)

# Signature
for line, opts in [
    ('Ahmad Duais', dict(bold=True)),
    ('CEO, Absolute Security Group', dict(bold=False)),
    ('09 950 4640  |  021 0850 0009', dict(bold=False)),
    ('ahmad@absolutesecuritygroup.co.nz', dict(bold=False)),
]:
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(0)
    r = p.add_run(line); r.font.size = Pt(10); r.bold = opts['bold']
    if opts['bold']: r.font.color.rgb = NAVY

out = os.path.expanduser('~/Desktop/ASG/HOTC/2026/Colliers_Tom_Followup_Email.docx')
os.makedirs(os.path.dirname(out), exist_ok=True)
doc.save(out)
print(out)
