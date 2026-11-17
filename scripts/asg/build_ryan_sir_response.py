#!/usr/bin/env python3
"""Build SLS RTC's response to the lawyer on the Draft Statement in Reply.
Point-by-point answers to every highlighted query + corrections + exhibits.
Outputs: response doc + short cover email, into ~/Desktop/Ryan Webby/ and Downloads."""
import os, shutil
from docx import Document
from docx.shared import Pt, RGBColor, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

NAVY=RGBColor(0x1F,0x38,0x64); GOLD=RGBColor(0xB8,0x91,0x2F); GREY=RGBColor(0x55,0x55,0x55)
RED=RGBColor(0xB0,0x1E,0x1E); GREEN=RGBColor(0x2E,0x7D,0x32)
OUTDIR=os.path.expanduser("~/Desktop/Ryan Webby")
os.makedirs(OUTDIR,exist_ok=True)

def setfont(doc):
    st=doc.styles['Normal']; st.font.name='Calibri'; st.font.size=Pt(10.5)
    st.element.rPr.rFonts.set(qn('w:eastAsia'),'Calibri')

def H(doc,txt,size=13,color=NAVY,before=10,after=3,rule=False):
    p=doc.add_paragraph(); p.paragraph_format.space_before=Pt(before); p.paragraph_format.space_after=Pt(after)
    r=p.add_run(txt); r.bold=True; r.font.size=Pt(size); r.font.color.rgb=color
    if rule:
        pb=OxmlElement('w:pBdr'); bt=OxmlElement('w:bottom')
        bt.set(qn('w:val'),'single'); bt.set(qn('w:sz'),'6'); bt.set(qn('w:space'),'2'); bt.set(qn('w:color'),'B8912F')
        pb.append(bt); p._p.get_or_add_pPr().append(pb)
    return p

def body(doc,txt,before=0,after=6,size=10.5,color=None,italic=False,indent=0,bold=False):
    p=doc.add_paragraph(); pf=p.paragraph_format
    pf.space_before=Pt(before); pf.space_after=Pt(after); pf.left_indent=Mm(indent)
    r=p.add_run(txt); r.font.size=Pt(size); r.italic=italic; r.bold=bold
    if color: r.font.color.rgb=color
    return p

def runs(doc,parts,before=0,after=6,indent=0,size=10.5):
    """parts = list of (text, bold, color, italic)"""
    p=doc.add_paragraph(); pf=p.paragraph_format
    pf.space_before=Pt(before); pf.space_after=Pt(after); pf.left_indent=Mm(indent)
    for tup in parts:
        t=tup[0]; b=tup[1] if len(tup)>1 else False; c=tup[2] if len(tup)>2 else None; it=tup[3] if len(tup)>3 else False
        r=p.add_run(t); r.bold=b; r.italic=it; r.font.size=Pt(size)
        if c: r.font.color.rgb=c
    return p

def bullet(doc,txt,color=None,after=3,bold_lead=None):
    p=doc.add_paragraph(style='List Bullet'); p.paragraph_format.space_after=Pt(after)
    if bold_lead:
        r=p.add_run(bold_lead); r.bold=True; r.font.size=Pt(10.5)
        if color: r.font.color.rgb=color
    r=p.add_run(txt); r.font.size=Pt(10.5)
    if color and not bold_lead: r.font.color.rgb=color
    return p

def suggest(doc,txt):
    """indented suggested-wording block, italic, boxed feel"""
    p=doc.add_paragraph(); pf=p.paragraph_format
    pf.left_indent=Mm(8); pf.space_before=Pt(2); pf.space_after=Pt(8)
    r=p.add_run("Suggested wording:  "); r.bold=True; r.font.size=Pt(9.5); r.font.color.rgb=GOLD
    r2=p.add_run('“'+txt+'”'); r2.italic=True; r2.font.size=Pt(9.5); r2.font.color.rgb=GREY
    return p

# ============================================================ RESPONSE DOC
doc=Document(); setfont(doc)
for s in doc.sections:
    s.top_margin=Mm(16); s.bottom_margin=Mm(14); s.left_margin=Mm(18); s.right_margin=Mm(18)

p=doc.add_paragraph(); p.add_run('SLS RTC LIMITED — INSTRUCTIONS & RESPONSES ON DRAFT STATEMENT IN REPLY').bold=True
p.runs[0].font.size=Pt(14); p.runs[0].font.color.rgb=NAVY
body(doc,'ERA File 3480826  ·  Ryan Andrew Webby v SLS RTC Limited (Second Respondent)',after=1,size=10,color=GREY)
body(doc,'Prepared by Ahmad Duais, Director, SLS RTC Limited  ·  For: M J McGoldrick, Wynn Williams  ·  Re: Draft Statement in Reply dated 21 August 2026',after=2,size=10,color=GREY)
# rule
pr=doc.add_paragraph(); pb=OxmlElement('w:pBdr'); bt=OxmlElement('w:bottom')
bt.set(qn('w:val'),'single'); bt.set(qn('w:sz'),'8'); bt.set(qn('w:space'),'1'); bt.set(qn('w:color'),'B8912F')
pb.append(bt); pr._p.get_or_add_pPr().append(pb)

body(doc,'Matt — thank you for the draft. Below are responses to every highlighted query and the further information requested, in the order they appear in the draft. Items I can confirm from documents are marked ✓ (with the supporting email provided). Items needing my factual confirmation are marked [TO CONFIRM] with draft wording ready to drop in. There are also three corrections to make before filing, and two substantive points you should be aware of.',before=4,after=8)

# ---------- PART A
H(doc,'A.  Corrections to make before filing',13,NAVY,rule=True)
runs(doc,[('1.  ',True),('Background section',True,NAVY),('  — “On 11 March 2025, ',),('SLC RTC Limited',True,RED),(' completed its purchase…” should read ',),('SLS',True,GREEN),(' RTC Limited.',)],after=3)
runs(doc,[('2.  ',True),('Further-information section',True,NAVY),('  — “Mr Webby’s employment with SLS RTC Limited began on 12 March ',),('2026',True,RED),('” — the year is wrong; it should be ',),('12 March 2025',True,GREEN),(' (consistent with the Background and Calculation sections). ',),('Important',True,RED),(' — the entire defence turns on the 12 March 2025 date, so this typo must be fixed.',)],after=3)
runs(doc,[('3.  ',True),('Footer table',True,NAVY),('  — the solicitor email shows “matt.mcgoldrick@',),('wynn williams',True,RED),('.co.nz” (with a space); it should be ',),('wynnwilliams.co.nz',True,GREEN),(' (the address-for-service paragraph is already correct).',)],after=4)

# ---------- PART B
H(doc,'B.  Responses to the highlighted queries',13,NAVY,rule=True)

H(doc,'Calculation of Entitlements',11.5,NAVY,before=6,after=2)

runs(doc,[('Query — the pay-breakdown email (“we do not appear to have a copy of this”)   ',True,NAVY),('✓ LOCATED',True,GREEN)],after=2)
body(doc,'It is Mr Duais’ email to Mr Webby of 24 June 2026, 7:19pm, in the “Leave calculation review request” thread — provided as Exhibit A. It:',after=3)
bullet(doc,'explains that for the week ending 23 June, 44.25 hours on site − 0.50h unpaid meal break = 43.75 paid hours;')
bullet(doc,'identifies the two days where the gap between shifts was only 15 minutes and was topped up to a 30-minute unpaid break — Wed 17 June (Belfast 09:30–15:15 + Northlands 15:30–19:00) and Mon 22 June (New Brighton 09:00–13:45 + Ferrymead 14:00–18:15);')
bullet(doc,'attaches Mr Webby’s earning summary; and')
bullet(doc,'confirms the payslip figure is correct.')
suggest(doc,'On 24 June 2026, Mr Duais emailed Mr Webby explaining how his pay for the week ending 23 June 2026 was calculated: 44.25 hours on site, less a 30-minute unpaid meal break, produced 43.75 paid hours. Mr Duais identified the two days on which the gap between Mr Webby’s consecutive shifts was only 15 minutes and had been topped up to a 30-minute unpaid meal break. He attached Mr Webby’s earning summary and confirmed the payslip figure was correct.')

runs(doc,[('Query — “When were records provided?”   ',True,NAVY),('✓',True,GREEN)],after=2)
body(doc,'The earning summary was attached to the 24 June 2026 email (Exhibit A). Mr Webby also had continuous self-service access to his SLS RTC-period wage, time and leave records via the PayHero portal at all material times (referred to in the 25 May and 24 June emails). Consistent with SLS RTC’s position, the records related to the period from 12 March 2025 — SLS RTC could not provide the previous employer’s pre-2025 records.',after=3)
runs(doc,[('Candour point:  ',True,RED),('Mr Webby chased on 14 June 2026 (“I have still not received any records”); the consolidated earning summary followed on 24 June. I would not describe the provision as immediate — the honest position is that the SLS-period records were always available in PayHero and the earning summary was supplied on 24 June.',)],after=3)
suggest(doc,'Mr Webby’s earning summary was provided with Mr Duais’ email of 24 June 2026. Mr Webby also had access to his wage, time and leave records for his employment with SLS RTC Limited through the PayHero payroll portal at all material times.')

runs(doc,[('Query — “Mr Duais investigated and concluded paid correctly. No monies are owing.”   ',True,NAVY),('✓ CHECKED — SUPPORTABLE',True,GREEN)],after=2)
body(doc,'I have reviewed Mr Webby’s Earnings Summary, Holiday Leave History and Other Leave History (12 March 2025 – 20 August 2026). The records do NOT support the underpayment claim — his leave and public holidays are paid on his average earnings, which are above the 8-hour-day basis he alleges:',after=3)
bullet(doc,'Rate confirmed at $26.50/hour throughout.')
bullet(doc,'Annual holidays are valued at the greater of ordinary weekly pay or average weekly earnings (the Holidays Act 2003 test). His average weekly earnings are ~$1,125/week — about 42.5 hours — well above both his 35-hour contractual minimum and a 40-hour week. Annual leave is therefore paid generously, not on an 8-hour day.')
bullet(doc,'Public holidays, sick and bereavement days are paid at Average Daily Pay of ~$231/day — about 8.7 hours — which is above his actual average paid day of ~8.55 hours. Again, not an 8-hour-day calculation.')
body(doc,'Honest caveat: this verifies the method from the summary reports (which is compliant). The only theoretical gap is relevant-daily-pay vs average-daily-pay on individual public holidays — worth at most ~$100–250 across 17 months, and itself arguable because Mr Webby’s daily hours vary. There is no sign of systematic underpayment. On this basis “no monies owing” is supportable:',before=2,after=3)
suggest(doc,'Mr Duais reviewed Mr Webby’s wage, holiday and leave records and concluded that Mr Webby has been paid correctly. Mr Webby’s leave and public-holiday entitlements have been calculated on his average earnings in accordance with the Holidays Act 2003, which exceed his ordinary contracted hours, and no monies are owing. To the extent any minor discrepancy were ever identified, SLS RTC Limited’s practice is to correct it and credit Mr Webby’s leave balance, as Mr Duais advised on 29 April and 25 May 2026.')

H(doc,'Management Conduct and Workplace Treatment',11.5,NAVY,before=8,after=2)

runs(doc,[('Query — 2 March 2026 Bunnings Riccarton: were concerns about Mr Webby’s work discussed with other staff before being raised with him?   ',True,NAVY),('✓ CONFIRMED',True,GREEN)],after=2)
body(doc,'Confirmed by Mr Duais: any discussion of Mr Webby’s performance took place only at the appropriate management level — with his direct manager — as occurs for all staff in the ordinary course of ensuring the quality of service delivered to clients. It was NOT discussed with his colleagues or the wider team, and none of his private or personal information was disclosed. Any concerns about the 2 March observation task were raised directly with Mr Webby.',after=3)
suggest(doc,'Any concerns regarding Mr Webby’s observation task on 2 March 2026 were raised directly with Mr Webby. To the extent Mr Webby’s performance was discussed internally, it was discussed only at the appropriate management level (with his direct manager), as occurs for all employees in the ordinary course of ensuring the quality of service provided to clients. Mr Webby’s performance was not discussed with his colleagues or the wider team, and none of his personal or private information was disclosed.')
runs(doc,[('This also answers the privacy allegation:  ',True,GREEN),('Mr Webby alleges his performance/personal matters were discussed with colleagues before being raised with him. The distinction to draw is that manager-to-manager performance discussion is ordinary management practice for all staff — not disclosure to peers — and it supports the existing denial that any of Mr Webby’s personal or private information was disclosed (Privacy Act 2020 / confidentiality).',)],after=4)
runs(doc,[('Privacy / family information — additional confirmation (reinforces the “personal information” paragraph):  ',True,NAVY),('Mr Duais confirms SLS does not hold or maintain information about Mr Webby’s family circumstances, does not discuss employees’ private or family matters, and is not aware of any of Mr Webby’s family, personal or medical information being disclosed to or discussed with staff — you cannot disclose what you do not hold. NB the underlying allegation is directed at the Christchurch manager, so the pleading is best kept to “SLS is not aware of / does not hold” (which the draft already does) rather than an absolute Mr Duais cannot personally guarantee for others.',)],after=3)
suggest(doc,'SLS RTC Limited does not hold or maintain any information about Mr Webby’s family circumstances, and does not discuss its employees’ private or family matters. It is not aware of any of Mr Webby’s personal, medical, or family information being disclosed to, or discussed with, any staff member. Mr Webby has provided no dates or particulars of the alleged disclosures, and SLS RTC Limited denies any breach of the Privacy Act 2020 or its obligations of confidentiality.')

runs(doc,[('Query — 11 March 2026 meeting: purpose + why no support person   ',True,NAVY),('✓ CONFIRMED — NO RECORD',True,GREEN)],after=2)
body(doc,'Confirmed by Mr Duais: SLS RTC Limited has no record of any meeting with Mr Webby on 11 March 2026, and Mr Duais was not party to any such meeting. Two consequences for the pleading:',after=3)
bullet(doc,'The draft currently asserts “On 11 March 2026, SLS RTC Limited invited Mr Webby to a meeting.” Because there is no record and the meeting cannot be confirmed, we should NOT assert it occurred — better to put Mr Webby to proof (a non-admission) than to plead a fact we cannot support or explain.')
bullet(doc,'Mr Webby’s complaint alleges a support person was appointed for him (i.e. imposed) — not that one was withheld. So the query “why a support person was not required” may misframe his allegation; worth checking against his Statement of Problem before finalising.')
body(doc,'If a meeting did occur it would have been at Christchurch site level. This matter is in any event outside the 90-day timeframe and is caught by the existing time-bar defence.',before=2,after=3)
suggest(doc,'SLS RTC Limited has no record of a meeting with Mr Webby on 11 March 2026. Mr Webby has not provided any details of the meeting he asserts took place, including its purpose, who attended, or what was discussed. SLS RTC Limited is unable to respond further and does not admit the assertions made about it. In any event, this matter is raised outside the 90-day statutory timeframe, and SLS RTC Limited does not consent to it being raised out of time.')

H(doc,'Complaint of 14 June 2026',11.5,NAVY,before=8,after=2)
runs(doc,[('Query — the correct account of events + supporting emails   ',True,NAVY),('✓ FULL ACCOUNT BELOW',True,GREEN)],after=2)
runs(doc,[('⚠️ Correcting the draft:  ',True,RED),('the draft (and Mr Webby) refer to a “14 July email” in which Mr Duais supposedly said he assumed another manager had dealt with the complaint. Mr Duais has checked his sent mail and confirms there was NO 14 July email — on 14 July Mr Duais ',),('visited Mr Webby in person',True,NAVY),(' in Christchurch (Mr Duais alone attended for SLS; no other person was present). Mr Webby has mischaracterised the in-person meeting as an email. The record of that day is the file note (Exhibit C), not an email.',)],after=4)
body(doc,'The correct sequence (supporting documents: Exhibit B = 14 June complaint + same-day acknowledgement; Exhibit A = 24 June written commitment; Exhibit C = file note of the 14 July in-person meeting):',after=3)
bullet(doc,'14 June 2026 — Mr Webby emailed his complaint (addressed to GM Mark Clansey, cc Mr Duais). Mr Clansey acknowledged it the same day (2:00pm): “thank you for sharing your concerns with us. We will review and get back to you soon.” (Exhibit B).',bold_lead='')
bullet(doc,'24 June 2026 — in his pay email, Mr Duais told Mr Webby in writing he was planning a trip to Christchurch and would be “addressing the concerns in your previous email” (Exhibit A). Contemporaneous evidence the complaint was being actioned, a month before the visit.')
bullet(doc,'Mr Clansey (the GM to whom the complaint was addressed) was on approximately one month’s leave during this period.')
bullet(doc,'14 July 2026 — Mr Duais travelled to Christchurch and met Mr Webby IN PERSON (a visit, not an email) to discuss his concerns. Mr Webby declined to discuss the substance and said he wished to raise the matters through mediation. At the same meeting he said he was looking for other work.')
bullet(doc,'Mr Duais understood, given Mr Clansey’s acknowledgement and leave and Mr Webby’s election of mediation, that the matter was being progressed on that basis. Any understanding that another manager was handling it was formed in that context — it was not conveyed by any email of 14 July.')
suggest(doc,'On receiving Mr Webby’s complaint of 14 June 2026, SLS RTC Limited escalated it to its most senior level. It was acknowledged the same day. In his email of 24 June 2026, Mr Duais advised Mr Webby that he was planning to travel to Christchurch and would address the concerns Mr Webby had raised. The general manager to whom the complaint had been addressed, Mark Clansey, was on extended leave during this period. On 14 July 2026, Mr Duais travelled to Christchurch and met with Mr Webby in person to discuss his concerns. At that meeting Mr Webby declined to discuss the substance of his complaint and stated that he wished to raise his concerns through mediation. SLS RTC Limited respected that election, did not compel an internal process Mr Webby had declined, and remains willing to participate in mediation to resolve the matter. For the avoidance of doubt, Mr Duais did not email Mr Webby on 14 July 2026 as alleged; the contact on that date was the in-person meeting described above.')
runs(doc,[('Note:  ',True,GREEN),('the 24 June “addressing the concerns in your previous email” line is the strongest single piece of evidence in the file — it shows the complaint was being dealt with in writing before the visit. Attach the 24 June email (Exhibit A), Mr Clansey’s 14 June acknowledgement (Exhibit B), and the 14 July file note (Exhibit C). There is no 14 July email to attach.',)],after=4)
runs(doc,[('★ Strong corroboration that Mr Webby elected mediation — but CONFIDENTIAL (your call):  ',True,RED)],after=1)
body(doc,'Mr Webby’s election of mediation is backed by an active MBIE mediation — File 2162011 (coordinator Mel Tuineau, MBIE Employment Services). The timeline objectively confirms the complaint was dealt with:',after=3)
bullet(doc,'14 June — complaint; ~25 June — MBIE mediation file opened (11 days later);')
bullet(doc,'29 June — Mr Duais AND Mr Webby had a call with the mediator;')
bullet(doc,'15 July — the mediator wrote: “Thank you Ryan for your email informing that mediation is to proceed”;')
bullet(doc,'Mediation booked for 4 August 2026 (Graham, a director of SLS Retail Theft Control Ltd, brought in to assist) — but the mediation did NOT proceed.')
body(doc,'This is independent, government evidence that Mr Webby chose mediation and that SLS engaged with it — it substantially answers the “failure to investigate the complaint” grievance (the complaint was referred to statutory mediation within ~11 days, with Mr Webby participating).',after=3)
runs(doc,[('⚠️ Confidentiality:  ',True,RED),('mediation communications are privileged under sections 148 and 148A of the Employment Relations Act 2000. I have NOT put any mediation content into the pleading. The MBIE email is provided to you separately, in confidence, for your assessment of what (if anything) may properly be referred to — the fact that mediation was arranged and that Mr Webby elected it is likely referable, but the content is protected and this is your call.',)],after=3)
runs(doc,[('⚠️ It also contradicts the draft’s mediation answers — see Part C.',True,RED)],after=4)

H(doc,'Pay Rates',11.5,NAVY,before=8,after=2)
runs(doc,[('Query — “What correspondence occurred?” + the date pay reviews were discussed   ',True,NAVY),('✓ CONFIRMED',True,GREEN)],after=2)
body(doc,'Confirmed by Mr Duais: there was no formal written pay-review correspondence (the agreement has no pay-review process). Pay reviews were discussed in person at the 14 July 2026 Christchurch meeting, in the context of the wider business and economic position. Suggested wording for the Pay Rates section:',after=3)
suggest(doc,'Mr Webby’s employment agreement does not provide any formal process or requirement for pay reviews, and there has been no formal written correspondence concerning pay reviews. On 14 July 2026, Mr Duais met with Mr Webby in Christchurch and discussed the general business environment, including the significant reductions in client budgets that had reduced the volume of work available across SLS RTC Limited and the wider economic conditions affecting the availability of security work. Mr Duais explained that, in that context, a review of the business’s budget remained in progress, that pay reviews would be considered once budgets had been finalised, and that SLS RTC Limited did not consider there was any issue with Mr Webby’s current rate of pay.')
body(doc,'This lets the two bracketed pay-review sentences merge into the 14 July account — no separate earlier date is needed unless you recall discussing pay reviews before 14 July.',before=0,after=3)
runs(doc,[('⚠️ One caution on how we shape this:  ',True,RED),('the 14 July meeting also touched on staff performance and how hard work is to come by. I have deliberately kept that OUT of the pleading. In a meeting with an employee who had just filed a protected complaint, a “you need to improve / jobs are scarce” message can be recast by the applicant as pressure or intimidation — the victimisation risk the analysis flagged as the single most dangerous point. Keep the pleading to the legitimate purpose (the budget/economic context that explains the pay-review position) and leave the performance element out.',)],after=4)

# ---------- PART C
H(doc,'C.  Two substantive points you should know (not highlighted)',13,NAVY,rule=True)
runs(doc,[('1.  Radio-shift — PAID (✓ confirmed).  ',True,GREEN),('Mr Webby was paid for the radio shift. One date fix: the shift was 23 July (9.30am–2.00pm); the draft says “paid Mr Webby for his shift on ',),('24 July',True,RED),('” — this should read ',),('23 July',True,GREEN),(' (the shift he was sent home from; 24 July is the confirmation-email date). Please correct so there is no date inconsistency for the applicant to pick at.',)],after=3)
runs(doc,[('2.  Leave / public-holiday calculation — CHECKED.  ',True,GREEN),('I have now reviewed the Earnings Summary + Holiday/Other Leave histories: leave and public holidays are paid on average earnings that exceed an 8-hour-day basis, so Mr Webby’s underpayment claim is not borne out and “no monies owing” is supportable (see the Calculation of Entitlements response above for the detail and wording).',)],after=4)
runs(doc,[('3.  The mediation answers need correcting (the “Have you tried mediation?” questions).  ',True,RED),('The draft answers a flat “No” to using MBIE mediation. That is not accurate: MBIE mediation — File 2162011 — was arranged and scheduled for 4 August 2026 (Mr Duais took part in a call with the mediator on 29 June; Mr Webby confirmed it would proceed on/by 15 July), ',),('but the mediation did not proceed',True,NAVY),('. So the accurate answer is not “No” and not “held” — it is that MBIE mediation was arranged and scheduled for 4 August 2026 but did not go ahead. Two related points: (a) the mediation names ',),('SLS Retail Theft Control Ltd (the First Respondent)',True,NAVY),(', not SLS RTC Limited — a possible entity mismatch; and (b) handle it consistently with the confidentiality point above.',)],after=4)

# ---------- PART D
H(doc,'D.  Exhibits',13,NAVY,rule=True)
bullet(doc,'Email chain “Leave calculation review request”, 29 April – 24 June 2026 — the pay breakdown, the records provision, and the written Christchurch commitment. (Transcript at Appendix A; original email to be forwarded.)',bold_lead='Exhibit A — ')
bullet(doc,'Mr Webby’s formal complaint of 14 June 2026 and Mr Clansey’s same-day acknowledgement (“thank you for sharing your concerns … we will review and get back to you soon”) — confirms the complaint was acknowledged immediately.',bold_lead='Exhibit B — ')
bullet(doc,'File note of the 14 July 2026 Christchurch meeting (Mr Duais’ reconstructed record of the in-person visit) — prepared and attached. This is the record of 14 July; there is no “14 July email”.',bold_lead='Exhibit C — ')
bullet(doc,'MBIE mediation email, File 2162011 (25 June – 16 July 2026) — CONFIDENTIAL / mediation-privileged (ERA ss 148, 148A). Provided to you separately for assessment; NOT proposed as a pleading exhibit.',bold_lead='For your eyes only (confidential) — ')
bullet(doc,'Documentary Response folder already prepared: pay records, 14 May 2026 performance review, complaint acknowledgement, and the 11 March fact-gathering note.',bold_lead='Also available — ')

# ---------- PART E
H(doc,'E.  Summary — what I still need to confirm for you',13,NAVY,rule=True)
bullet(doc,'the three corrections in Part A;',bold_lead='You to amend: ')
bullet(doc,'the three corrections in Part A, plus the radio-shift date (24 July → 23 July) and softening the 11 March assertion to a non-admission.',bold_lead='You to amend in the draft: ')
bullet(doc,'all highlighted factual queries are now answered — 2 March, 11 March, the 14 June complaint, records provision, the pay-breakdown email, pay reviews, and the radio shift.',bold_lead='✓ All confirmed: ')
bullet(doc,'the 14 July file note is prepared (Exhibit C). There is no “14 July email” to retrieve — 14 July was an in-person visit — so the pack is complete once you review/sign the file note and forward the exhibits.  [Leave/PH check — DONE: “no monies owing” is supportable.]',bold_lead='Final step: ')

# ---------- APPENDIX A: exhibit transcript
doc.add_page_break()
H(doc,'Appendix A — Exhibit A transcript',13,NAVY,after=2)
body(doc,'Email chain “Re: Leave calculation review request” (oldest first). Mr Duais = Director, SLS RTC Limited; R A Webby = Ryan Webby.',after=6,size=9.5,color=GREY,italic=True)

emails=[
 ('Ryan Webby → Ahmad Duais','29 April 2026, 3:55pm',
  'I am requesting a review of how my leave and public holiday payments have been calculated since I started on 20 November 2024. My usual roster is a 5-on / 2-off pattern, with shifts generally around 9 hours per day and 43–45 hours per week, aside from a short initial period of reduced hours. On reviewing my payslips, leave and public holiday payments appear to have been calculated using an 8-hour day. Could you please confirm whether this aligns with my employment agreement and normal roster, and whether any adjustments are required. Please also confirm the correct method that will be used going forward.'),
 ('Ahmad Duais → Ryan Webby','29 April 2026, 5:37pm',
  'I will only be able to assist from the 12th March 2025 as this is when you were employed with SLS RTC Limited. I will look into this for you — if there are any errors PayHero will automatically adjust them and add them to the balance. I will get back to you once I hear from them.'),
 ('Ryan Webby → Ahmad Duais','25 May 2026, 4:53pm',
  'I’m following up on my email from 19 days ago regarding my leave calculations and the 8-hour vs 9-hour discrepancy. As it has been nearly a month, I would now like to formally request a copy of my Wage and Time Records and my Holidays and Leave Records from the start of my employment in 2024 to the present. Under Section 130 of the Employment Relations Act, I am entitled to access these. Please provide them by 29th May 2026.'),
 ('Ahmad Duais → Ryan Webby','25 May 2026, 5:06pm',
  'Hi Ryan, this record will need to be reviewed by your previous employer — I can only provide from when you joined SLS RTC Limited, which you have access to from PayHero, and any difference in hours from PayHero will be added to your entitlements. For your concern around 9 vs 8 hrs, your shifts include a .5hr unpaid break and shifts roughly come to 8hrs; any discrepancy gets added to your leave balance — i.e. if you take 4hrs or 1 day annual leave you don’t lose the rest of the hours, that’s not how the system works.'),
 ('Ahmad Duais → Ryan Webby','25 May 2026, 6:30pm',
  'Thanks Ryan, I’ll send this to PayHero — I’m not sure why it’s showing that many hours. Much appreciated.'),
 ('Ryan Webby → Ahmad Duais','14 June 2026, 9:31am',
  'I have still not received any records. Also Graham’s email does not work.'),
 ('Ryan Webby → Ahmad Duais','24 June 2026, 6:55pm',
  'Hello Ahmad, my timesheet doesn’t seem to match my payslip. Thanks.'),
 ('Ahmad Duais → Ryan Webby  [THE PAY-BREAKDOWN EMAIL]','24 June 2026, 7:19pm',
  'Hi Ryan, thanks for checking in about your hours for the week ending 23 June. I wanted to explain how the 43.75 hours on your payslip is worked out, as the meal-break deduction can look confusing at first. Your total time on site for the week (clock-in to clock-out) added up to 44.25 hours. From that, a 30-minute unpaid meal break applies, which brings your paid total to 43.75 hours. The important point is that the result is identical either way. Here is exactly where the 30 minutes (0.5h) came from — on two days your morning and afternoon shifts were only 15 minutes apart, so the system topped that gap up to a full 30-minute unpaid break: Wed 17 June – Belfast 09:30–15:15 + Northlands 15:30–19:00 (15-minute gap) → 15 minutes added; Mon 22 June – New Brighton 09:00–13:45 + Ferrymead 14:00–18:15 (15-minute gap) → 15 minutes added. On your other days the gap was already 30 minutes or more. So in short: 44.25 hours on site − 0.50 hours unpaid meal break = 43.75 hours paid. That is the figure on your payslip, and it is correct. The half hour is simply the standard unpaid meal break, not missing pay. I have also attached your earning summary in case you have not been able to see this for yourself in PayHero. I am currently planning a trip to Christchurch. During this time I will be addressing the concerns in your previous email and also overlooking the results of individuals. Have a great rest of your week and let me know if you have any other questions.'),
 ('Ryan Webby → Ahmad Duais','24 June 2026, 7:28pm',
  'The roster showed only 15 minutes travel between sites, so I worked those 15 minutes understanding that was the travel time allowed.'),
 ('Ahmad Duais → Ryan Webby','24 June 2026, 7:34pm',
  'Yes that is correct and the same math gives you the same answer — for example Wed 17 June, Belfast 09:30–15:15 + Northlands 15:30–19:00 (15-minute gap) 9.25hrs → 15 minutes removed to compensate for break time is a total of 9hrs; 9:30am–7pm is 9.5hrs − 30m meal break = 9hrs. This is the same calculation regardless of whether the distance was 15m or 30m.'),
]
for who,when,txt in emails:
    hilite = 'PAY-BREAKDOWN' in who
    p=doc.add_paragraph(); p.paragraph_format.space_before=Pt(6); p.paragraph_format.space_after=Pt(1)
    r=p.add_run(who); r.bold=True; r.font.size=Pt(9.5); r.font.color.rgb=(GREEN if hilite else NAVY)
    r2=p.add_run('   '+when); r2.font.size=Pt(9); r2.font.color.rgb=GREY; r2.italic=True
    b=body(doc,txt,after=4,size=9.5,indent=4)
    if hilite:
        for rr in b.runs: rr.font.color.rgb=RGBColor(0x1a,0x1a,0x1a)

RESP=os.path.join(OUTDIR,'Response to Lawyer - Draft Statement in Reply.docx')
doc.save(RESP); shutil.copy2(RESP,os.path.expanduser('~/Downloads/'+os.path.basename(RESP)))
print('SAVED:',RESP)

# ============================================================ COVER EMAIL
d2=Document(); setfont(d2)
for s in d2.sections:
    s.top_margin=Mm(18); s.bottom_margin=Mm(16); s.left_margin=Mm(20); s.right_margin=Mm(20)
body(d2,'To:  matt.mcgoldrick@wynnwilliams.co.nz',after=1,size=10.5)
body(d2,'Subject:  Webby v SLS RTC Limited (ERA 3480826) — responses to Draft Statement in Reply',after=8,size=10.5,bold=True)
body(d2,'Hi Matt,',after=6)
body(d2,'Thank you for the draft Statement in Reply. I’ve gone through it and attached a document setting out responses to each highlighted query, in the order they appear in the draft.',after=6)
body(d2,'In summary:',after=3)
for t in [
 'The pay-breakdown email you couldn’t locate is found — it’s my 24 June 2026 email, attached as Exhibit A (with the full chain from 29 April).',
 'That same email answers when records were provided (24 June, plus ongoing PayHero access), and it contains the line where I told Ryan I was travelling to Christchurch to address his complaint — a month before the 14 July meeting.',
 'The correct account of the 14 June complaint is set out in full, with the supporting emails.',
 'There are three small corrections to make before filing (including a “12 March 2026” that should read 2025).',
 'Two things I’m confirming before we finalise: the leave/public-holiday calculation (the real substance of Ryan’s pay concern), and a couple of dates/details on the 2 March and 11 March matters and pay reviews.',
]:
    bullet(d2,t)
body(d2,'The remaining items I need to confirm are listed at the end of the attached document. I’ll get you the 14 July email and a file note of that meeting shortly.',before=4,after=6)
body(d2,'Kind regards,',after=1)
body(d2,'Ahmad Duais',after=0,bold=True)
body(d2,'Director, SLS RTC Limited',after=0,size=10,color=GREY)
COVER=os.path.join(OUTDIR,'Cover Email to Lawyer - Statement in Reply (DRAFT).docx')
d2.save(COVER); shutil.copy2(COVER,os.path.expanduser('~/Downloads/'+os.path.basename(COVER)))
print('SAVED:',COVER)
