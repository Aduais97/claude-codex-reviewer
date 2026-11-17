#!/usr/bin/env python3
"""Assemble the complete 'Response to Statement in Reply' folder for the lawyer
(Matt McGoldrick): cover email + responses doc + file note + exhibit PDFs/emails.
Everything Ahmad needs to reply to Matt's draft, in one send-ready folder."""
import os, shutil, email
from email import policy
from xml.sax.saxutils import escape
from docx import Document
from docx.shared import Pt, RGBColor, Mm
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

NAVY=RGBColor(0x1F,0x38,0x64); GOLD=RGBColor(0xB8,0x91,0x2F); GREY=RGBColor(0x55,0x55,0x55); RED=RGBColor(0xB0,0x1E,0x1E); GREEN=RGBColor(0x2E,0x7D,0x32)
HOME=os.path.expanduser("~")
BASE=os.path.join(HOME,"Desktop/Ryan Webby")
FOLDER=os.path.join(BASE,"Response to Statement in Reply - for Matt McGoldrick")
EXH=os.path.join(FOLDER,"Exhibits (for the pleading)")
CONF=os.path.join(FOLDER,"CONFIDENTIAL - Mediation (NOT a pleading exhibit)")
for d in (FOLDER,EXH,CONF): os.makedirs(d,exist_ok=True)

# ---------- helpers ----------
def parse_eml(p):
    m=email.message_from_binary_file(open(p,'rb'),policy=policy.default)
    body=None
    if m.is_multipart():
        for part in m.walk():
            if part.get_content_type()=='text/plain': body=part.get_content(); break
        if not body:
            import re
            for part in m.walk():
                if part.get_content_type()=='text/html':
                    body=re.sub('<[^>]+>',' ',part.get_content()); break
    else: body=m.get_content()
    return dict(frm=m.get('From',''),to=m.get('To',''),cc=m.get('Cc',''),date=m.get('Date',''),subject=m.get('Subject',''),body=(body or '').strip())

def render_email_pdf(meta, outpath, title, confidential=False):
    ss=getSampleStyleSheet()
    def S(n,**k): return ParagraphStyle(n,parent=ss['Normal'],**k)
    NV=colors.HexColor('#1F3864'); GD=colors.HexColor('#B8912F'); GY=colors.HexColor('#555555'); RD=colors.HexColor('#B01E1E')
    el=[]
    el.append(Paragraph(f'<b>{escape(title)}</b>',S('t',fontSize=14,textColor=NV,leading=17)))
    if confidential:
        el.append(Paragraph('<b>IN CONFIDENCE — mediation communication, privileged (Employment Relations Act 2000, ss 148 &amp; 148A)</b>',
                            S('c',fontSize=8.5,textColor=RD,leading=11,spaceBefore=2)))
    el.append(Spacer(1,4))
    hdr=[['From:',escape(meta['frm'])],['To:',escape(meta['to'])]]
    if meta['cc']: hdr.append(['Cc:',escape(meta['cc'])])
    hdr+=[['Date:',escape(meta['date'])],['Subject:',escape(meta['subject'])]]
    t=Table(hdr,colWidths=[18*mm,158*mm])
    t.setStyle(TableStyle([('FONTSIZE',(0,0),(-1,-1),8.5),('TEXTCOLOR',(0,0),(0,-1),NV),('FONTNAME',(0,0),(0,-1),'Helvetica-Bold'),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1),('LINEBELOW',(0,-1),(-1,-1),0.5,GD)]))
    el.append(t); el.append(Spacer(1,6))
    body=S('b',fontSize=8.8,leading=12.5,spaceAfter=2)
    for line in meta['body'].split('\n'):
        ln=line.rstrip()
        if not ln: el.append(Spacer(1,4)); continue
        # visual cue for quoted lines
        q=ln.lstrip().startswith('>')
        st=S('q',fontSize=8.5,leading=11.5,textColor=GY,leftIndent=8) if q else body
        el.append(Paragraph(escape(ln) or '&nbsp;',st))
    SimpleDocTemplate(outpath,pagesize=A4,topMargin=14*mm,bottomMargin=14*mm,leftMargin=16*mm,rightMargin=16*mm).build(el)

def setfont(doc):
    st=doc.styles['Normal']; st.font.name='Calibri'; st.font.size=Pt(10.5)
    st.element.rPr.rFonts.set(qn('w:eastAsia'),'Calibri')
def B(doc,txt,after=6,size=10.5,color=None,bold=False,italic=False,before=0):
    p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(after); p.paragraph_format.space_before=Pt(before)
    r=p.add_run(txt); r.font.size=Pt(size); r.bold=bold; r.italic=italic
    if color: r.font.color.rgb=color
    return p
def BL(doc,txt,lead=None,after=3):
    p=doc.add_paragraph(style='List Bullet'); p.paragraph_format.space_after=Pt(after)
    if lead:
        r=p.add_run(lead); r.bold=True; r.font.size=Pt(10.5)
    r=p.add_run(txt); r.font.size=Pt(10.5); return p
def rule(doc,color='B8912F'):
    p=doc.add_paragraph(); pb=OxmlElement('w:pBdr'); bt=OxmlElement('w:bottom')
    bt.set(qn('w:val'),'single'); bt.set(qn('w:sz'),'8'); bt.set(qn('w:space'),'1'); bt.set(qn('w:color'),color)
    pb.append(bt); p._p.get_or_add_pPr().append(pb)

# ---------- 1. copy the built docs in ----------
shutil.copy2(os.path.join(BASE,"Response to Lawyer - Draft Statement in Reply.docx"),
             os.path.join(FOLDER,"01 - Responses to Draft Statement in Reply.docx"))
shutil.copy2(os.path.join(BASE,"File Note - 14 July 2026 Christchurch Meeting.docx"),
             os.path.join(FOLDER,"02 - File Note 14 July (Exhibit C) - REVIEW & SIGN.docx"))

# ---------- 2. exhibit emails -> PDF + original .eml ----------
EA=os.path.join(HOME,"Downloads/Leave calculation review request.eml")
EB=os.path.join(BASE,"FORMAL COMPLAINT REGARDING MANAGEMENT CONDUCT, WORKPLACE PRACTICES, AND PROCEDURAL CONCERNS.eml")
EM=os.path.join(HOME,"Downloads/File 2162011, Ryan Andrew Webby AND SLS RETAIL THEFT CONTROL LTD IN-CONFIDENCE.eml")
render_email_pdf(parse_eml(EA),os.path.join(EXH,"Exhibit A - Pay & Records emails (29 Apr-24 Jun 2026).pdf"),
                 "Exhibit A — Pay & records email chain (29 April – 24 June 2026)")
shutil.copy2(EA,os.path.join(EXH,"Exhibit A - Pay & Records emails (original).eml"))
render_email_pdf(parse_eml(EB),os.path.join(EXH,"Exhibit B - Complaint & same-day acknowledgement (14 Jun 2026).pdf"),
                 "Exhibit B — Complaint of 14 June 2026 & same-day acknowledgement")
shutil.copy2(EB,os.path.join(EXH,"Exhibit B - Complaint & same-day acknowledgement (original).eml"))
render_email_pdf(parse_eml(EM),os.path.join(CONF,"MBIE Mediation File 2162011 - CONFIDENTIAL.pdf"),
                 "MBIE Mediation — File 2162011 (25 June – 16 July 2026)",confidential=True)
shutil.copy2(EM,os.path.join(CONF,"MBIE Mediation File 2162011 - CONFIDENTIAL (original).eml"))

# ---------- 3. pay records ----------
for src,dst in [("Earnings Summary - Ryan Webby - 2025-03-12 - 2026-08-20.pdf","Pay records - Earnings Summary.pdf"),
                ("Holiday Leave History - Ryan Webby (4).pdf","Pay records - Holiday Leave History.pdf"),
                ("Other Leave History - Ryan Webby (3).pdf","Pay records - Other Leave History.pdf")]:
    s=os.path.join(HOME,"Downloads",src)
    if os.path.exists(s): shutil.copy2(s,os.path.join(EXH,dst))

# ---------- 4. cover email ----------
d=Document(); setfont(d)
for s in d.sections: s.top_margin=Mm(18); s.bottom_margin=Mm(16); s.left_margin=Mm(20); s.right_margin=Mm(20)
B(d,'To:  matt.mcgoldrick@wynnwilliams.co.nz',after=1)
B(d,'Subject:  Webby v SLS RTC Limited (ERA 3480826) — responses to Draft Statement in Reply',after=8,bold=True)
B(d,'Hi Matt,',after=6)
def EH(t): B(d,t,bold=True,color=NAVY,before=9,after=2,size=11)
B(d,'Thank you for the draft. Below is everything you need to finalise and file the Statement in Reply, grouped by the highlighted queries and the corrections. The attached responses document sets out the same answers with suggested wording for each, plus the exhibits.',after=4)

EH('Corrections to make before filing')
BL(d,'“SLC RTC Limited” → “SLS RTC Limited” (Background).')
BL(d,'“began on 12 March 2026” → “12 March 2025” (further-information section). This one matters — the defence turns on the 12 March 2025 date.')
BL(d,'Footer email “wynn williams” (with a space) → “wynnwilliams”.')

EH('Calculation of entitlements')
BL(d,'Pay-breakdown email (the one you did not have a copy of): it is my email of 24 June 2026 (Exhibit A). It explains 44.25 hours on site − 0.5h unpaid meal break = 43.75 paid hours, identifies the two days where a 15-minute shift gap was topped up to a 30-minute break, and attaches the earning summary.')
BL(d,'When records were provided: the earning summary was attached to that 24 June email, and Ryan had ongoing PayHero access throughout. SLS RTC can only provide records from 12 March 2025 (pre-2025 is the previous employer’s).')
BL(d,'No monies owing: I have reviewed his full earnings and leave records. His leave and public holidays are calculated on his average earnings (annual leave ~$1,125/week ≈ 42.5 hours; public holidays/sick ~$231/day ≈ 8.7 hours) — above an 8-hour day. His underpayment claim is not borne out, so “no monies owing” is supportable.')

EH('Management conduct')
BL(d,'2 March (Bunnings): any discussion of Ryan’s performance was only ever with his direct manager — as we do for all staff to ensure good client service — never with his colleagues or the wider team. Concerns were raised directly with him.')
BL(d,'Privacy / family: we do not hold or maintain any information about Ryan’s family circumstances, and we do not discuss employees’ private or family matters. We are not aware of any of his personal, medical or family information being disclosed to or discussed with staff — you cannot disclose what you don’t hold. (He has given no dates or particulars.)')
BL(d,'11 March meeting: I have no record of any such meeting and was not party to one. I suggest we not assert it occurred — put Ryan to proof (a non-admission); it is also time-barred. Note Ryan’s complaint says a support person (Carly) was appointed/imposed on him, not withheld — so “why a support person was not required” may be answering the wrong point.')

EH('Complaint of 14 June 2026')
BL(d,'Acknowledged the same day by Mark Clansey (Exhibit B): “thank you for sharing your concerns … we will review and get back to you soon.”')
BL(d,'On 24 June I told Ryan in writing I would address his concerns on a Christchurch trip (Exhibit A).')
BL(d,'On 14 July I travelled to Christchurch and met Ryan in person — I alone attended for SLS; no other person was present. He declined to discuss the substance and said he wanted to raise the matters through mediation. I have checked my sent mail and confirm there was NO email of 14 July — Ryan has mischaracterised the in-person meeting as an email. My file note of the meeting is attached (Exhibit C).')

EH('Mediation — important, and confidential')
BL(d,'Ryan elected mediation: MBIE mediation File 2162011 was opened around 25 June, we both had a call with the mediator on 29 June, Ryan confirmed on/by 15 July it would proceed, and it was scheduled for 4 August 2026. This objectively confirms he chose mediation and answers the failure-to-investigate allegation.')
BL(d,'The 4 August mediation did NOT proceed.')
BL(d,'So the draft’s flat “No” to “have you tried MBIE mediation?” is not accurate — the correct answer is that MBIE mediation was arranged and scheduled for 4 August 2026 but did not go ahead. Please correct the mediation section.')
BL(d,'Mediation communications are privileged (ERA ss 148/148A), so the MBIE email is in a separate “Confidential” subfolder for your assessment of what may be referred to — please don’t file it as an exhibit without your advice. It names SLS Retail Theft Control Ltd (the First Respondent), not SLS RTC Limited — a possible entity point.')

EH('Pay rates')
BL(d,'No formal written pay-review correspondence (the agreement has no pay-review process). Pay was discussed in person on 14 July in the context of the business budget position; I explained reviews would follow once budgets were finalised and that there was no issue with the current rate.')

EH('Bunnings Riccarton (radio)')
BL(d,'Ryan was paid. One fix: the shift was 23 July — the draft says “paid … for his shift on 24 July”, which should read 23 July (24 July is the confirmation-email date).')

B(d,'The attached responses document has all of this with suggested wording, and the Exhibits folder has Exhibits A–C and the pay records. The MBIE mediation email is in the separate Confidential subfolder.',before=8,after=6)
B(d,'Kind regards,',after=1)
B(d,'Ahmad Duais',after=0,bold=True); B(d,'Director, SLS RTC Limited',after=0,size=10,color=GREY)
d.save(os.path.join(FOLDER,"00 - Cover Email to Matt.docx"))

# ---------- 5. README / index ----------
r=Document(); setfont(r)
for s in r.sections: s.top_margin=Mm(18); s.bottom_margin=Mm(16); s.left_margin=Mm(20); s.right_margin=Mm(20)
p=r.add_paragraph(); rr=p.add_run('RESPONSE TO STATEMENT IN REPLY — FOLDER CONTENTS'); rr.bold=True; rr.font.size=Pt(13); rr.font.color.rgb=NAVY
B(r,'Ryan Andrew Webby v SLS RTC Limited · ERA File 3480826 · for M J McGoldrick, Wynn Williams',after=2,size=9.5,color=GREY)
rule(r)
B(r,'What is in this folder',after=3,bold=True,color=NAVY,before=4)
BL(r,'the email to send to Matt.',lead='00 – Cover Email to Matt.docx — ')
BL(r,'the main document — point-by-point responses to every highlighted query, all corrections, and suggested wording.',lead='01 – Responses to Draft Statement in Reply.docx — ')
BL(r,'the reconstructed record of the 14 July Christchurch meeting (you and Ryan only). REVIEW and SIGN before sending.',lead='02 – File Note 14 July (Exhibit C) – REVIEW & SIGN.docx — ')
B(r,'Exhibits (for the pleading)',after=3,bold=True,color=NAVY,before=6)
BL(r,'the pay-breakdown email + records provision + the written Christchurch commitment (PDF + original .eml).',lead='Exhibit A – Pay & Records emails — ')
BL(r,'Ryan’s complaint and Mark Clansey’s same-day acknowledgement (PDF + original .eml).',lead='Exhibit B – Complaint & acknowledgement — ')
BL(r,'Earnings Summary, Holiday Leave History, Other Leave History — the basis for “no monies owing”.',lead='Pay records (3 PDFs) — ')
B(r,'CONFIDENTIAL – Mediation (NOT a pleading exhibit)',after=3,bold=True,color=RED,before=6)
BL(r,'the MBIE mediation email (File 2162011). Mediation-privileged (ERA ss 148/148A) — for Matt’s assessment only; do NOT file it as an exhibit without his advice.',lead='MBIE Mediation File 2162011 — ')
rule(r)
B(r,'Your action list before sending',after=3,bold=True,color=NAVY,before=4)
BL(r,'Review and SIGN the 14 July file note (item 02). Confirmed: you and Ryan only were present.')
BL(r,'Send items 00–02 + the Exhibits folder to Matt; hand him the Confidential mediation email separately, flagged as privileged.')
BL(r,'Confirmed for Matt (in the email): the 4 August mediation did not proceed, and there is no 14 July email.')
r.save(os.path.join(FOLDER,"README - contents & action list.docx"))

print("FOLDER BUILT:",FOLDER)
for root,dirs,files in os.walk(FOLDER):
    lvl=root.replace(FOLDER,'').count(os.sep)
    print('  '*lvl+os.path.basename(root)+'/')
    for f in sorted(files): print('  '*(lvl+1)+f)
