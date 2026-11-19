#!/usr/bin/env python3
"""File note — 14 July 2026 Christchurch meeting with Ryan Webby (reconstructed
from recollection, prepared 20 Aug 2026 for the ERA matter). Honest, not backdated."""
import os, shutil
from docx import Document
from docx.shared import Pt, RGBColor, Mm
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

NAVY=RGBColor(0x1F,0x38,0x64); GOLD=RGBColor(0xB8,0x91,0x2F); GREY=RGBColor(0x55,0x55,0x55)
OUTDIR=os.path.expanduser("~/Desktop/Ryan Webby")

doc=Document()
st=doc.styles['Normal']; st.font.name='Calibri'; st.font.size=Pt(11)
st.element.rPr.rFonts.set(qn('w:eastAsia'),'Calibri')
for s in doc.sections:
    s.top_margin=Mm(20); s.bottom_margin=Mm(18); s.left_margin=Mm(22); s.right_margin=Mm(22)

def H(txt,size=14,color=NAVY,before=8,after=4):
    p=doc.add_paragraph(); p.paragraph_format.space_before=Pt(before); p.paragraph_format.space_after=Pt(after)
    r=p.add_run(txt); r.bold=True; r.font.size=Pt(size); r.font.color.rgb=color; return p
def body(txt,after=8,size=11,color=None,italic=False,bold=False,before=0):
    p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(after); p.paragraph_format.space_before=Pt(before)
    r=p.add_run(txt); r.font.size=Pt(size); r.italic=italic; r.bold=bold
    if color: r.font.color.rgb=color
    return p
def kv(k,v):
    p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(2)
    r=p.add_run(k+'  '); r.bold=True; r.font.size=Pt(11); r.font.color.rgb=NAVY
    r2=p.add_run(v); r2.font.size=Pt(11); return p
def num(n,txt):
    p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(6); p.paragraph_format.left_indent=Mm(8)
    r=p.add_run(n+'  '); r.bold=True; r.font.size=Pt(11)
    r2=p.add_run(txt); r2.font.size=Pt(11); return p
def rule():
    p=doc.add_paragraph(); pb=OxmlElement('w:pBdr'); bt=OxmlElement('w:bottom')
    bt.set(qn('w:val'),'single'); bt.set(qn('w:sz'),'8'); bt.set(qn('w:space'),'1'); bt.set(qn('w:color'),'B8912F')
    pb.append(bt); p._p.get_or_add_pPr().append(pb)

p=doc.add_paragraph(); r=p.add_run('FILE NOTE — CONFIDENTIAL'); r.bold=True; r.font.size=Pt(15); r.font.color.rgb=NAVY
body('Meeting with Ryan Webby — Christchurch — 14 July 2026',after=2,size=11.5,color=GREY,bold=True)
rule()

kv('Prepared by:','Ahmad Duais, Director, SLS RTC Limited')
kv('Date prepared:','20 August 2026')
kv('Re:','Ryan Webby — complaint of 14 June 2026 / ERA File 3480826')
doc.add_paragraph()

body('This note is my record of a meeting I held with Ryan Webby in Christchurch on 14 July 2026. '
     'It has been prepared from my recollection on the date shown above, in connection with the current '
     'Employment Relations Authority matter. It is not a verbatim transcript and no contemporaneous notes '
     'were taken at the meeting.', italic=True, color=GREY)

H('Background',13)
body('Mr Webby sent a formal written complaint about his manager on 14 June 2026, which was acknowledged the '
     'same day. In my email to Mr Webby of 24 June 2026 I told him that I was planning to travel to Christchurch '
     'and that during that visit I would be addressing the concerns he had raised. Mark Clansey, our General '
     'Manager and the person to whom the complaint had been addressed, was on extended leave (approximately one '
     'month) during this period. I travelled to Christchurch and met with Mr Webby on 14 July 2026 as I had said I would.')

H('Present',13)
kv('•','Ahmad Duais (Director, SLS RTC Limited)')
kv('•','Ryan Webby')
body('No other person attended. The meeting was between Mr Duais and Mr Webby only.', size=10, color=GREY, italic=True, before=2)

H('What was discussed',13)
num('1.','I met with Mr Webby to follow up in person, as I had undertaken to do in my 24 June email, and to '
        'discuss the concerns he had raised in his complaint.')
num('2.','When I sought to discuss the substance of his complaint, Mr Webby did not wish to talk the points '
        'through with me. He told me he would prefer to raise his concerns through mediation rather than an '
        'internal process. I respected that and did not press him to go through the matters against his wishes.')
num('3.','Mr Webby told me during the meeting that he was looking for other work.')
num('4.','We also discussed the general position of the business — the significant reductions in client budgets '
        'that had reduced the volume of work available across the company, the wider economic conditions, and the '
        'importance of strong performance across the team in a difficult market. This was a general discussion '
        'about the business environment, not a disciplinary step directed at Mr Webby.')
num('5.','On pay, I explained that a review of the business budget was still in progress and that pay reviews '
        'would be considered once budgets had been finalised. I confirmed we did not consider there was any issue '
        'with Mr Webby’s current rate of pay.')

H('My understanding after the meeting',13)
body('Because our General Manager, Mark Clansey, had received and acknowledged the complaint and was the point of '
     'contact for it, and because Mr Webby had told me he wanted to deal with his concerns through mediation rather '
     'than internally, I understood that the matter would be progressed on that basis. I did not take further internal '
     'steps to investigate the complaint against Mr Webby’s stated wish to use mediation.')

doc.add_paragraph(); rule()
kv('Signed:','...........................................................')
kv('Name:','Ahmad Duais, Director, SLS RTC Limited')
kv('Date:','.......................................')

OUT=os.path.join(OUTDIR,'File Note - 14 July 2026 Christchurch Meeting.docx')
doc.save(OUT); shutil.copy2(OUT,os.path.expanduser('~/Downloads/'+os.path.basename(OUT)))
print('SAVED:',OUT)
