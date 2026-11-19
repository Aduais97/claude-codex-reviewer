#!/usr/bin/env python3
"""Cold outreach email to Brent Fleet (Kmart) — Hormozi grand-slam offer, ETR-synthesised.
Primary email + alt subject + short follow-up. Saved for Ahmad to schedule Monday."""
import os, shutil
from docx import Document
from docx.shared import Pt, RGBColor, Mm
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

NAVY=RGBColor(0x1F,0x38,0x64); GOLD=RGBColor(0xB8,0x91,0x2F); GREY=RGBColor(0x55,0x55,0x55)
OUT=os.path.expanduser("~/Desktop/ASG/Sales")
os.makedirs(OUT,exist_ok=True)
doc=Document()
st=doc.styles['Normal']; st.font.name='Calibri'; st.font.size=Pt(11)
st.element.rPr.rFonts.set(qn('w:eastAsia'),'Calibri')
for s in doc.sections: s.top_margin=Mm(18); s.bottom_margin=Mm(16); s.left_margin=Mm(20); s.right_margin=Mm(20)

def H(t,size=13,color=NAVY,before=10,after=3):
    p=doc.add_paragraph(); p.paragraph_format.space_before=Pt(before); p.paragraph_format.space_after=Pt(after)
    r=p.add_run(t); r.bold=True; r.font.size=Pt(size); r.font.color.rgb=color; return p
def B(t,after=6,size=11,color=None,bold=False,italic=False,before=0,indent=0):
    p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(after); p.paragraph_format.space_before=Pt(before); p.paragraph_format.left_indent=Mm(indent)
    r=p.add_run(t); r.font.size=Pt(size); r.bold=bold; r.italic=italic
    if color: r.font.color.rgb=color
    return p
def BUL(t,after=3):
    p=doc.add_paragraph(style='List Bullet'); p.paragraph_format.space_after=Pt(after)
    r=p.add_run(t); r.font.size=Pt(11); return p
def rule():
    p=doc.add_paragraph(); pb=OxmlElement('w:pBdr'); bt=OxmlElement('w:bottom')
    bt.set(qn('w:val'),'single'); bt.set(qn('w:sz'),'8'); bt.set(qn('w:space'),'1'); bt.set(qn('w:color'),'B8912F')
    pb.append(bt); p._p.get_or_add_pPr().append(pb)

p=doc.add_paragraph(); r=p.add_run('KMART OUTREACH — BRENT FLEET'); r.bold=True; r.font.size=Pt(14); r.font.color.rgb=NAVY
B('Cold email · Absolute Security Group · to schedule for Monday',after=2,size=9.5,color=GREY)
rule()

H('Subject line',12,before=6)
B('The same crews hitting Bunnings are walking into Kmart',bold=True,after=2)
B('Alternate (value-forward):  “Free Kmart store audit — the team behind Bunnings & Woolworths LP”',size=10,color=GREY,after=2)

H('Email body',12)
B('Brent,',after=6)
B('The organised retail-crime crews working Bunnings right now are very often the same ones walking into Kmart — same faces, same shopping-centre run. I know, because our teams run loss prevention for Bunnings and Woolworths, and we watch them move.',after=6)
B('Here’s the pattern we keep proving: uniformed-only deters the opportunist, but the organised crews read a lone guard in seconds and route around him. Covert-only catches them, but does nothing to slow the aggression your floor staff wear. Most of your shrinkage — and most of your risk to staff — lives in the gap between those two models. We close it with cross-deterrence: uniformed and covert working as one team, so the visible layer pushes offenders into the covert layer instead of out the door.',after=6)
B('Let me show you exactly where that gap sits in one of your stores — free:',after=3)
BUL('We walk one Kmart store you pick;')
BUL('We benchmark it against how we protect Bunnings and Woolworths; and')
BUL('You get a short written report — your ranked shrinkage exposure, the cross-deterrence gaps, and a few quick wins you can action with or without us.')
B('No obligation, no pitch — the report’s yours to keep either way. Worst case, you get an outside read on one store from the team already guarding the business next door.',after=6,before=3)
B('Coffee and 20 minutes to compare notes? Tell me the store and a time that suits — I’ll come to you.',after=8)
B('Ahmad Duais',after=0,bold=True)
B('CEO & Founder, Absolute Security Group',after=0,size=10,color=GREY)
B('ahmad@absolutesecuritygroup.co.nz · 09 950 4640 · www.absolutesecuritygroup.co.nz',after=2,size=10,color=GREY)

rule()
H('Short follow-up (if no reply after ~5–7 days)',12)
B('Subject:  re: The same crews hitting Bunnings are walking into Kmart',bold=True,after=4,size=10.5)
B('Brent — still happy to walk one store and hand you the report, free. Even if we never work together, you’ll get an outside read on your shrinkage exposure from the team guarding Bunnings next door. Worth a coffee? Just name the store.',after=8)

rule()
H('Why this works (Hormozi)',12)
BUL('Grand Slam Offer — a free, concrete deliverable (walk + benchmark + written report), risk fully reversed (“yours to keep either way”), so a no costs him more than a yes.')
BUL('Value Equation — big dream outcome (less shrinkage, safer staff), high believability (we already do this for Bunnings/Woolworths — his own Wesfarmers sibling), near-zero time/effort (we do the work; he just picks a store).')
BUL('Leads with HIS problem, not our pitch — the insight opening earns the read from a hard-to-reach expert; the ask is a single, low-friction yes.')

rule()
H('Scheduling for Monday',12)
BUL('Use “Schedule send” in Gmail/Outlook. For a hard-to-reach exec, aim for ~7:30am Monday (top of his inbox before the week buries it) — or ~1:30pm if you’d rather miss the Monday-morning flood.')
BUL('Note on client names: you asked to name Bunnings & Woolworths (strong proof, and Bunnings shares Wesfarmers with Kmart). If you’d rather not name them in a cold email, say the word and I’ll swap to “national hardware and grocery retailers”.')

path=os.path.join(OUT,"Kmart - Brent Fleet Outreach Email.docx")
doc.save(path); shutil.copy2(path,os.path.expanduser("~/Downloads/"+os.path.basename(path)))
print("SAVED:",path)
