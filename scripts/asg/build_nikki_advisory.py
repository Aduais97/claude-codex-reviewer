"""Advisory & Consulting Agreement — Absolute Security Group Ltd x Nikki Wairau Christian.
Companion to the Share Sale Agreement (SPA cl 9.4). Built on the Graham Zuill V2 template.
v2 — all package-review findings applied (cross-doc B1/B2/R1-R7, compliance A1/B1/D1/E1/E2,
research recommendations 1-6). DRAFT — to be settled by solicitors alongside the SPA.
"""
import os
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

OUTDIR = os.path.expanduser('~/Desktop/ASG/Legal/Nikki Share Purchase')
os.makedirs(OUTDIR, exist_ok=True)
OUT_DOCX = os.path.join(OUTDIR, 'Advisory and Consulting Agreement - N W Christian - DRAFT v2.docx')
OUT_MD = os.path.expanduser('~/Desktop/Dev/Claude/scripts/asg/ADVISORY_DRAFT.md')

NAVY = RGBColor(0x1B, 0x2A, 0x4A)
doc = Document()
for s in doc.sections:
    s.top_margin = s.bottom_margin = Cm(2.2)
    s.left_margin = s.right_margin = Cm(2.4)
normal = doc.styles['Normal']
normal.font.name = 'Calibri'
normal.font.size = Pt(11)
md = []

def title(text, size=16, bold=True, center=True):
    p = doc.add_paragraph()
    if center: p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text); r.bold = bold; r.font.size = Pt(size); r.font.color.rgb = NAVY

def head(text):
    p = doc.add_paragraph()
    r = p.add_run(text); r.bold = True; r.font.size = Pt(12); r.font.color.rgb = NAVY
    p.paragraph_format.space_before = Pt(12); p.paragraph_format.space_after = Pt(4)
    md.append('\n## ' + text + '\n')

def para(text, indent=0, bold=False):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(indent)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text); r.bold = bold
    md.append(('  ' if indent else '') + text + '\n')

title('ADVISORY AND CONSULTING AGREEMENT', 16)
doc.add_paragraph()
para('This Advisory and Consulting Agreement (the Agreement) is made as of [        ] 2026 between:')
para('ABSOLUTE SECURITY GROUP LIMITED, company number 8517467, of 7/220 Queen Street, Auckland '
     'CBD 1010, New Zealand (the Company); and')
para('NIKKI WAIRAU CHRISTIAN, an individual (the Advisor).')
md.insert(0, '# ADVISORY AND CONSULTING AGREEMENT\n\nABSOLUTE SECURITY GROUP LIMITED (Company) x NIKKI WAIRAU CHRISTIAN (Advisor)\n')

head('Background')
para('A.  The Company and the Advisor are parties to matters contemplated by clause 9.4 of the '
     'Agreement for Sale and Purchase of Shares between the Advisor, Ahmad Duais and Lockhart '
     'Trustee Services No.222 Limited (the Share Sale Agreement). This Agreement is a separate '
     'advisory agreement contemplated by that clause.')
para('B.  The restraints, confidentiality and other obligations in the Share Sale Agreement continue '
     'to apply in accordance with their terms. Services performed under this Agreement are services '
     'provided directly to the Company within clause 10.4(d) of the Share Sale Agreement, and client '
     'contact in the course of services requested in writing under this Agreement is contact '
     'permitted by clause 11.5 of the Share Sale Agreement. Nothing in this Agreement varies the '
     'Share Sale Agreement.')

head('1.  Engagement and Services')
para('1.1  The Company engages the Advisor, and the Advisor agrees, to provide advisory and '
     'consulting services to the Company (the Services), being:')
para('(a)  quality-control operations and compliance checking of the Company’s teams — the core '
     'monthly focus of the engagement;', indent=1)
para('(b)  maintaining and building the Company’s client relationships, and attending meetings with '
     'clients as a consultant where required by the Company;', indent=1)
para('(c)  business development — identifying, introducing and assisting to secure new clients for '
     'the Company (clause 4 provides for commission); and', indent=1)
para('(d)  such training and other consulting tasks as are agreed in writing under clause 3.2.', indent=1)
para('1.2  Services are to be requested or agreed in writing by Ahmad Duais on behalf of the '
     'Company. Subject to any agreed scheduling, site-access and health-and-safety requirements, '
     'the Advisor determines the manner and method of performing the Services. The Advisor shall not '
     'contact clients of the Company except in the course of Services requested in writing by the '
     'Company (or, where clause 1.3 applies, SLS RTC Limited), or with the prior written '
     'confirmation of Ahmad Duais as Purchaser under the Share Sale Agreement, consistent with '
     'clause 11.5 of the Share Sale Agreement.')
para('1.3  Where SLS RTC Limited executes a joinder to this Agreement, the Services may extend to '
     'SLS RTC Limited on the terms of this Agreement, and references to the Company then include SLS '
     'RTC Limited in respect of those Services.')

head('2.  Hours and availability')
para('2.1  The Advisor shall perform a minimum of six (6) hours of Services each calendar month, '
     'spread across a minimum of two (2) days in that month, at times agreed with the Company.')
para('2.2  If the Company does not request, or does not require, Services in a month, the Advisor '
     'remains entitled to the monthly fee under clause 3.1 — the fee is a retainer for availability '
     'as much as for work performed.')
para('2.3  If the Company has requested Services and the Advisor fails to perform the minimum hours '
     'under clause 2.1 in a month, the Company may withhold the monthly fee for that month. The '
     'Company shall give the Advisor written notice of the shortfall and, where practicable, a '
     'reasonable opportunity to make the hours up within the following ten (10) working days before '
     'withholding.')

head('3.  Fees')
para('3.1  The Company shall pay the Advisor a fee of NZ$1,500.00 plus GST (if any) per calendar '
     'month, payable monthly on invoice to Accounts@absolutesecuritygroup.co.nz, for the Services '
     'described in clause 1.1 up to the minimum hours in clause 2.1.')
para('3.2  Time beyond the minimum hours is chargeable only where the additional hours and the task '
     'are agreed in writing in advance, at NZ$100.00 plus GST per hour, for any of the Services '
     '(including training and other consulting tasks under clause 1.1(d)).')
para('3.3  The Company will reimburse reasonable out-of-pocket expenses incurred in providing the '
     'Services where approved in writing in advance and supported by receipts.')

head('4.  New-client commission')
para('4.1  A Qualifying New Client is a client which: (a) is first introduced to the Company by the '
     'Advisor during the term of this Agreement and is not, and has not in the twenty-four (24) '
     'months before introduction been, a client of the Company or of SLS RTC Limited; (b) enters '
     'into a written services agreement with the Company with a minimum contractual term of six (6) '
     'months; (c) engages the Company for recurring contracted services — one-off events, casual or '
     'ad hoc bookings do not qualify; and (d) is engaged at the Company’s standard charge-out rates '
     'current at the date of the client’s services agreement, or at other rates the Company '
     'confirms in writing as commissionable.')
para('4.2  For each Qualifying New Client, the Company shall pay the Advisor commission equal to '
     'thirteen percent (13%) of the Net Revenue received by the Company from that client in respect '
     'of services performed in the client’s first three (3) months of services (the Commission '
     'Quarter). Net Revenue means fees actually received by the Company, excluding GST, '
     'disbursements and pass-through costs. The Company retains sole discretion whether to accept, '
     'and on what terms to contract with, any introduced prospective client, and no commission is '
     'payable in respect of services charged at rates below the Company’s standard rates unless '
     'confirmed in writing under clause 4.1(d). Once Net Revenue qualifies, commission on it is '
     'payable at 13% without discretion.')
para('4.3  Commission is paid in monthly instalments over the Commission Quarter: within fourteen '
     '(14) days after the end of each month of the Commission Quarter, the Company shall pay 13% of '
     'the Net Revenue received in that month, with a final wash-up within fourteen (14) days after '
     'the end of the second month following the Commission Quarter; and any Net Revenue for services '
     'performed in the Commission Quarter that is received after that date shall be included in a '
     'supplementary payment within fourteen (14) days of receipt.')
para('4.4  If the Qualifying New Client validly terminates within its minimum term for reasons '
     'attributable to the Advisor’s conduct, unpaid commission for that client ceases to accrue. '
     'If this Agreement expires or is terminated other than by the Company under clause 5.3, '
     'commission continues to accrue and be payable under clauses 4.2 and 4.3 for the remainder of '
     'the Commission Quarter of each then-existing Qualifying New Client as if this Agreement had '
     'continued. Entitlements accrued before termination survive termination in all cases.')
para('4.5  The Advisor shall register each proposed introduction with the Company in writing, naming '
     'the prospective client and the date of first contact, before or promptly after first '
     'substantive contact. Within ten (10) working days the Company shall confirm in writing whether '
     'the prospective client is capable of being a Qualifying New Client (including under clauses '
     '4.1(a) and 4.1(d)). Only registered introductions confirmed under this clause attract '
     'commission.')
para('4.6  With each commission payment (and with any nil return) the Company shall provide a '
     'statement showing, for each Qualifying New Client, invoices issued, Net Revenue received in '
     'the period, the exclusions applied (GST, disbursements, pass-through costs) and the commission '
     'calculated. Not more than once per Commission Quarter per client, the Advisor may, on ten (10) '
     'working days’ written notice, have an independent chartered accountant (bound by '
     'confidentiality and acting solely for this purpose) inspect the Company’s records to the '
     'extent necessary to verify the calculation. The Advisor bears the cost of the review unless it '
     'identifies an underpayment exceeding five percent (5%), in which case the Company shall pay '
     'the underpayment plus the reasonable cost of the review.')

head('5.  Term, renewal and termination')
para('5.1  This Agreement commences on the Settlement Date under the Share Sale Agreement and '
     'continues for an initial term of three (3) months, and then renews automatically for '
     'successive three (3) month terms unless either party gives the other written notice of '
     'non-renewal at least twenty (20) working days before the end of the then-current term.')
para('5.2  In addition, either party may terminate this Agreement at any time by ninety (90) days’ '
     'written notice to the other. If the notice period extends beyond the end of the then-current '
     'term, this Agreement continues on its then-current terms until the notice expires, and no '
     'further renewal occurs under clause 5.1 after the notice is given.')
para('5.3  The Company may terminate immediately by written notice if the Advisor materially '
     'breaches this Agreement or the Share Sale Agreement, or engages in conduct detrimental to the '
     'interests or reputation of the Company or SLS RTC Limited (subject to clause 6.2).')
para('5.4  On termination the Advisor shall return all materials, credentials and confidential '
     'information of the Company, and clauses 4.4 to 4.6 (commission), 6, 7, 8, 9 and 10 survive '
     'termination.')

head('6.  Confidentiality and regulator communications')
para('6.1  The Advisor shall keep confidential all confidential and proprietary information of the '
     'Company and SLS RTC Limited received in the course of the Services, shall use it solely to '
     'perform the Services, and shall not disclose it to any third party except as required by law. '
     'This clause supplements, and does not limit or replace, clause 12 of the Share Sale Agreement '
     '(which is unlimited in time).')
para('6.2  Nothing in this Agreement (including clauses 1.2, 2.3, 5.3 and 6.1) prevents, restricts, '
     'penalises or discourages the Advisor or the Company from making any report, complaint, '
     'disclosure or submission to, cooperating with, or otherwise communicating with, any regulator '
     'or government agency (including the Private Security Personnel Licensing Authority and its '
     'Complaints, Investigation and Prosecution Unit, the New Zealand Police, WorkSafe New Zealand, '
     'Inland Revenue, the Companies Office and the Ministry of Business, Innovation and Employment), '
     'whether or not the communication is required by law. No such communication is a breach of this '
     'Agreement, grounds for termination under clause 5.3, grounds for withholding any fee or '
     'commission, or conduct detrimental to the interests or reputation of any person for the '
     'purposes of clause 5.3.')

head('7.  Independent contractor; regulatory approvals; conflicts')
para('7.1  The Advisor is an independent contractor and not an employee of the Company. The Advisor '
     'has no authority to bind the Company or to represent the Company other than as an advisor '
     'acting within the Services. Nothing in this Agreement creates a partnership, joint venture or '
     'employment relationship. The Advisor is responsible for the Advisor’s own tax and ACC '
     'obligations.')
para('7.2  The Advisor shall promptly disclose to the Company any conflict of interest and work with '
     'the Company to resolve it. The restraints and related obligations in clauses 10, 11, 12 and '
     '12A of the Share Sale Agreement continue to apply and are not varied by this Agreement.')
para('7.3  During the term of this Agreement and for twelve (12) months after its termination or '
     'expiry, the Advisor shall not, directly or indirectly, solicit, canvass or accept the custom '
     'of, or be instrumental in the diversion away from the Company or SLS RTC Limited of, any '
     'client of the Company or of SLS RTC Limited with whom the Advisor dealt, or whom the Advisor '
     'introduced, in the course of the Services (including any Qualifying New Client), for services '
     'of a kind provided by the Company or SLS RTC Limited.')
para('7.4  The Advisor shall, at the Advisor’s cost, obtain before commencing the relevant Services, '
     'and hold, maintain and comply with for so long as this Agreement continues, every licence, '
     'certificate of approval, class endorsement and other approval under the Private Security '
     'Personnel and Private Investigators Act 2010 or any other law that is required for the Advisor '
     'to perform each of the Services, and shall provide evidence of them to the Company on request.')
para('7.5  The Advisor shall not perform, and the Company shall not require or permit the Advisor to '
     'perform, any Service which the Advisor is not lawfully entitled to perform. If the Advisor '
     'does not hold, or ceases to hold, an approval required for any of the Services (including on '
     'suspension, cancellation, refusal, surrender or expiry), the Advisor shall notify the Company '
     'immediately and: (a) clauses 2.1 to 2.3 and 3.1 are suspended in respect of the affected '
     'Services for so long as the approval is not held, no fee accruing under clause 3.1 where all '
     'Services are affected and the fee abating proportionately where part is affected; and (b) the '
     'Company may terminate this Agreement immediately by written notice if the position is not '
     'remedied within twenty (20) working days.')
para('7.6  The Advisor warrants that as at the date of this Agreement the Advisor has disclosed to '
     'the Company in writing the status of every licence and certificate of approval held or '
     'previously held by the Advisor under that Act, and every current or pending application, '
     'complaint, investigation or proceeding relating to the Advisor under that Act.')
para('7.7  The parties acknowledge and intend, having each had the opportunity to take independent '
     'advice, that this is a contract for services and that the real nature of the relationship is '
     'one of independent contractor: the Advisor conducts an independent advisory business, is free '
     '(subject to clauses 10 to 12A of the Share Sale Agreement) to provide services to other '
     'persons, is not subject to the Company’s employment policies (other than site health-and-'
     'safety and compliance requirements), and is not entitled to holidays, leave, KiwiSaver '
     'contributions or any other employee entitlement. The fees in clause 3 are set on that basis '
     'and are inclusive of all entitlements; if a court or authority nevertheless determines the '
     'Advisor is an employee, all amounts paid under this Agreement shall, to the maximum extent '
     'permitted by law, be credited against any minimum entitlements found to be owing.')

head('8.  Intellectual property')
para('8.1  All work product and intellectual property created by the Advisor in the course of the '
     'Services is the sole property of the Company, and the Advisor assigns to the Company all '
     'rights in it. This clause is in addition to clause 12A of the Share Sale Agreement (existing '
     'Company intellectual property), which continues to apply.')

head('9.  Indemnity')
para('9.1  The Company shall indemnify the Advisor against claims arising out of the Advisor’s good '
     'faith performance of the Services, except in cases of gross negligence, wilful misconduct or '
     'breach of this Agreement or the Share Sale Agreement.')

head('10.  Governing law and disputes')
para('10.1  This Agreement is governed by New Zealand law. Any dispute shall first be the subject of '
     'good faith negotiation between the parties, then mediation in Auckland, and failing resolution '
     'shall be referred to arbitration on the terms of clause 17 of the Share Sale Agreement, which '
     'applies to this Agreement with all necessary modifications as if set out in full. Despite the '
     'foregoing, any dispute solely concerning the calculation of commission or Net Revenue under '
     'clause 4 shall, at either party’s request, be referred to an independent chartered accountant '
     'agreed by the parties or, failing agreement within ten (10) working days, appointed by the '
     'President for the time being of Chartered Accountants Australia and New Zealand, acting as an '
     'expert and not as an arbitrator. The expert’s determination is final and binding absent '
     'manifest error, and the expert’s costs are borne as the expert directs.')

doc.add_paragraph()
head('EXECUTION')
para('EXECUTED as an agreement.', bold=True)
doc.add_paragraph()
para('SIGNED for and on behalf of ABSOLUTE SECURITY GROUP LIMITED by:', bold=True)
para('Signature:  ______________________________')
para('Name: Ahmad Duais        Title: Chief Executive Officer        Date: ________________')
doc.add_paragraph()
para('SIGNED by NIKKI WAIRAU CHRISTIAN as Advisor:', bold=True)
para('Signature:  ______________________________')
para('Date: ________________')
doc.add_paragraph()
para('[SLS RTC LIMITED joinder — complete if the Services extend to SLS RTC Limited (clause 1.3)]', bold=True)
para('SIGNED for and on behalf of SLS RTC LIMITED by:')
para('Signature:  ______________________________')
para('Name: ______________________    Position (director / authorised signatory): ______________________')

doc.save(OUT_DOCX)
open(OUT_MD, 'w').write('\n'.join(md))
print('SAVED:', OUT_DOCX)
print('SAVED:', OUT_MD)
