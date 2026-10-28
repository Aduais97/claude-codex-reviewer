#!/usr/bin/env python3
"""HNZ RFP 0018709 — Compliance & Requirements Matrix (xlsx).

Eight sheets: Key Dates, Compliance Checklist, Response Questions,
Officer Gates, District Sizing, Risk Register, Departure Register,
Clarification Questions. Navy/gold house style.

Usage: .venv/bin/python build_compliance_matrix.py <out.xlsx>
"""
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

NAVY = "1B2A4A"
GOLD = "D4A843"
ALT = "F2F4F8"
LIGHT = "E8EDF5"
BORDER = Side(style="thin", color="D0D5DD")

def sheet(wb, title, headers, rows, widths, status_col=None):
    ws = wb.create_sheet(title)
    ws.freeze_panes = "A2"
    for c, h in enumerate(headers, 1):
        cell = ws.cell(1, c, h)
        cell.font = Font(bold=True, color="FFFFFF", size=10)
        cell.fill = PatternFill("solid", fgColor=NAVY)
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        cell.border = Border(bottom=Side(style="medium", color=GOLD))
    for r, row in enumerate(rows, 2):
        for c, v in enumerate(row, 1):
            cell = ws.cell(r, c, v)
            cell.font = Font(size=9.5)
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = Border(left=BORDER, right=BORDER, top=BORDER, bottom=BORDER)
            if r % 2 == 0:
                cell.fill = PatternFill("solid", fgColor=ALT)
    for c, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(c)].width = w
    ws.row_dimensions[1].height = 28
    if status_col:
        for r in range(2, len(rows) + 2):
            ws.cell(r, status_col).fill = PatternFill("solid", fgColor=LIGHT)
    return ws

KEY_DATES = [
    ["Fri 30 Oct 2026, 5:00 PM", "Deadline for supplier questions on GETS", "Lodge clarification questions (see Clarifications sheet)", ""],
    ["Tue 3 Nov 2026, 5:00 PM", "HNZ answers final questions", "Reconcile answers into the draft response", ""],
    ["Fri 6 Nov 2026, 12:00 MIDDAY", "DEADLINE FOR PROPOSALS — GETS locks", "Submit via GETS no later than Wed 5 Nov", ""],
    ["~Late Nov 2026", "Respondents scoring 5+ on all non-price criteria invited to price", "Pricing Schedule + average district rates arrive by email", ""],
    ["Nov–Dec 2026", "Pricing submission window (HNZ-set deadline)", "Rates, rebate tiers, revised assumptions", ""],
    ["Feb 2027", "Final award decisions confirmed", "", ""],
    ["1 Apr 2027", "Contract/service start (most districts)", "One-month transition before start; HSO VRT after execution", ""],
    ["1 Apr – 1 Jul 2027", "Northland / MidCentral / Whanganui service start window", "", ""],
    ["~6 May 2027", "Offer validity expires (6 months from deadline)", "", ""],
]

CHECKLIST = [
    ["Form", "Use Response Form V3 (addendum 35288733 version with per-district Northern rows)", "Addendum / Slide Notes", "", ""],
    ["Form", "Keep section headings and sequence unchanged", "Form instructions", "", ""],
    ["Form", "Delete ALL purple Supplier Tips and purple instructions", "Form instructions", "", ""],
    ["Form", "Un-shade all blue answer areas after completing", "Form instructions", "", ""],
    ["Form", "Response Locations: answer Yes/No for ALL 17 district rows (No for districts not bid)", "Form instructions", "", ""],
    ["Form", "Label every Capability/Capacity answer with the district name(s) it covers", "GETS Q&A #18; Slide Notes", "", ""],
    ["Form", "Reference attachment file names inside the Response Form", "RFP s1.5(k)", "", ""],
    ["Pre-condition", "PSPLA Company Licence current — category Property Guard / class Guarding; evidence ready", "RFP s3.1; district schedules s9.2", "", ""],
    ["Pre-condition", "Confirm full green COA (Property Guard) + NZQA US 27364/27360/27361 pathway for all nominated staff", "RFP s3.1; district schedules s9.2", "", ""],
    ["Pre-condition", "H&S policy (HSWA 2015-compliant) — COPY ATTACHED to response; answer Yes in pre-condition table", "RFP s3.1; Form s2.1", "", ""],
    ["Due diligence", "Last 3 years statutory accounts attached (state audit/review/compilation basis plainly)", "Form s2.2", "", ""],
    ["Due diligence", "Insurance table per policy: insurer, type, cover, limitations, 3-year claims history + certificates", "Form s2.2; RFP s5.3", "", ""],
    ["Due diligence", "Claims & disputes: all legal/civil proceedings last 5 years + in progress + pending — truthful and complete", "Form s2.2; declaration", "", ""],
    ["Due diligence", "Merger/sale/restructure question answered truthfully (advice on wording if needed)", "Form s2.2", "", ""],
    ["Content", "All 21 scored questions answered, per district, with evidence", "Form Part A", "", ""],
    ["Content", "Assumptions & KPIs section completed NOW (not left for pricing stage)", "GETS Q&A #24", "", ""],
    ["Content", "Proposed Contract position completed — departure register attached if used", "GETS Q&A #30; RFP s5.1", "", ""],
    ["Content", "Two referees with consent confirmed; 'contact me first' box considered", "Form Referees", "", ""],
    ["Content", "Declaration: every row answered agree/disagree; signed + dated by authorised signatory (CEO)", "Form Declaration", "", ""],
    ["Hygiene", "NO pricing information anywhere in the response", "RFP s1.6", "", ""],
    ["Hygiene", "Commercially sensitive content marked; no third-party confidential data", "Form tips; ASG policy", "", ""],
    ["Hygiene", "Every factual claim evidenced or verifiable by reference call", "Scoring bands s3.4", "", ""],
    ["Submission", "Total package <50MB; videos (if any) <50MB", "RFP s1.5(j)", "", ""],
    ["Submission", "Submit via GETS 'Tender A Response' by Wed 5 Nov (buffer day); save confirmation", "RFP s1.6", "", ""],
    ["Probity", "No tender contact with any HNZ personnel outside GETS", "Slide 12; Slide Notes", "", ""],
]

QUESTIONS = [
    ["Admin", "-", "Profile: legal name, trading name, addresses, website, entity type, NZBN, tax residence, GST", "No", "Company records", ""],
    ["Admin", "-", "Point of Contact (name, position, phone, mobile, email)", "No", "CEO", ""],
    ["Admin", "-", "Response Locations table — Yes/No all 17 districts", "Yes", "Bid decision", ""],
    ["Capability 25%", "C1", "Healthcare (or similarly intensive) experience — sites, years, services; translation case if no healthcare", "Yes", "HOTC precinct, events, licensed premises, de-escalation volumes", ""],
    ["Capability 25%", "C2", "Screening process + standards incl. physical fitness and English (SMC standard) assurance", "No", "Recruitment SOP, COA/MoJ/reference checks, English evidence method", ""],
    ["Capability 25%", "C3", "Induction, onboarding, site-specific training (ASG's own processes)", "No", "Guard training manual 2026, buddy shifts, site SOPs", ""],
    ["Capability 25%", "C4", "Ongoing training + frequency + frontline-to-senior pipeline", "No", "Refresher calendar, named progression examples", ""],
    ["Capability 25%", "C5", "Compliance processes (legislation, licences, certifications, HNZ policies, site rules)", "No", "Licence/COA register, compliance calendar", ""],
    ["Capability 25%", "C6", "Subcontractor QA — or explicit statement of non-use", "No", "State: no subcontracting of service delivery; FM-only rule acknowledged", ""],
    ["Capability 25%", "C7", "Q1.g: approach to other services (district schedule ss3-8) outside Scheduled/On-Demand", "Yes", "Alarm response, patrols, CCTV, [SOC for Northland]; vehicle approach", ""],
    ["Capacity 25%", "P1", "Current staffing per district + healthcare-relevant staff + current clients per district", "Yes", "Headcounts by home area, COA status; mark client names sensitive", ""],
    ["Capacity 25%", "P2", "Recruitment strategy per district + community-reflective workforce", "Yes", "Pipeline sources, time-to-deploy, links to EB answers", ""],
    ["Capacity 25%", "P3", "Backfill + surge processes, contacts, operating hours", "No", "24/7 ops desk, escalation tree, response-time data", ""],
    ["Capacity 25%", "P4", "Turnover rates per district (healthcare/similar) + improvement actions", "Yes", "Real % with basis; retention actions", ""],
    ["Capacity 25%", "P5", "Account management structure + HALF-PAGE BIOS national + district contacts", "Yes", "CEO + ops manager bios, QBR owner", ""],
    ["Capacity 25%", "P6", "Transition plan + ERA 2000 obligations + capacity beyond transferred staff", "Yes", "Mobilisation Gantt; careful Part 6A wording (guards not Sch 1A)", ""],
    ["H&S 10%", "H1", "H&S management practices incl. duty of care to patients/staff/public", "No", "H&S system, worker participation, HSWA overlapping duties", ""],
    ["H&S 10%", "H2", "Fatigue management incl. rest periods AND secondary-employment detection/mitigation", "No", "Deputy rostering rules, max hours, declarations", ""],
    ["H&S 10%", "H3", "Incident logging (standard + notifiable) + reporting out of system", "No", "Incident platform, exports, 24/48-hr KPI alignment", ""],
    ["H&S 10%", "H4", "Force majeure response, BCP, emergency/risk management", "No", "BCP + annual test evidence", ""],
    ["H&S 10%", "H5", "Measuring + continuously improving H&S performance", "No", "Leading/lagging indicators, reviews", ""],
    ["Econ Benefits 10%", "E1", "Engagement BY DISTRICT with iwi, Pacific Hauora, community networks", "Yes", "Named counterparts + dates + owner — build before drafting", ""],
    ["Econ Benefits 10%", "E2", "Diverse/inclusive workforce reflective of local communities + partnerships", "Yes", "Actual workforce diversity data, quantified", ""],
    ["Econ Benefits 10%", "E3", "Strengthening NZ healthcare-security capability/capacity", "No", "Training investment, career pathway, NZ ownership", ""],
    ["Part B", "-", "Assumptions register (complete NOW; revisable at pricing)", "Yes", "See pack Part 7.3 list of 8", ""],
    ["Part B", "-", "KPIs to negotiate / propose", "No", "98.5% fill measurement basis; response clock start", ""],
    ["Contract", "-", "Accept Attachment B OR departure register (shortlisting factor)", "No", "6 HIGH departures (see Departures sheet)", ""],
    ["Referees", "-", "Two work-related referees, full details", "No", "Confirm consent first", ""],
    ["Declaration", "-", "All rows agree/disagree + signed by authorised signatory", "No", "CEO signature", ""],
]

GATES = [
    ["PSPLA full green COA — category Property Guard", "Every person on site incl. managers/support; no temporary COAs (emergency written approval only)", "Before any site entry", "COA application 4-8 wks if new", "District schedules s9.2"],
    ["NZQA US 27364 / 27360 / 27361", "All deployed personnel", "Before deployment", "Part of COA training", "District schedules s9.2"],
    ["English evidence — INZ Skilled Migrant Category standard", "All assigned officers; documented proof (IELTS one option)", "At assignment", "Varies; collect early", "Schedules s11; Q&A #28"],
    ["HNZ inductions ×3 (site, security, contractor H&S)", "All personnel", "Before deployment", "Transition month", "Schedules s9.1"],
    ["HSO Violence Reduction Training (CPI SI + HNZ tradecraft)", "All regularly assigned officers; level 5/7/9 days set by District Security Manager; annual revalidation; HNZ-funded course + hourly rate; ASG pays travel/accom (+ backfill in Northland)", "After contract execution, in transition month", "5-9 days + scheduling", "Schedules s9; Q&A #9/#19/#25"],
    ["SPEC (4-day) — Mental Health assignment", "Officers permanently assigned to MH facilities; annual revalidation; HNZ-funded", "Before MH assignment", "4 days + scheduling", "Auckland/Waitematā s9.3"],
    ["Infectious disease screening + vaccination (Category A)", "Hep B course + serology, MMR ×2, varicella, Tdap 10-yr, TB form (+IGRA/CXR if flagged); ASG pays ~$550/officer blended (worst case $1,100-1,500); strict evidence standard; HIPC-compliant register", "Screening complete BEFORE first shift; Hep B dose 1 pre-start", "2-6 weeks per officer", "Attachments W/X"],
    ["Children's Act safety checks (if Children's Workers)", "Identity + Police vet + referees + interview + risk assessment; 3-yearly rechecks; child-protection policy + 2-yearly training", "BEFORE Start Date + compliance declaration", "Police vetting ~2-4 wks", "Contract cl 24; Clarification Q5"],
    ["MoJ criminal record check (data access)", "Staff accessing HNZ data; ASG cost", "Before data access", "1-2 wks", "Contract cl 50.1(e)"],
    ["Physical capability + cultural awareness + computer literacy", "Assessment method documented; HNZ may interview and decline any officer (free replacement)", "At assignment", "-", "Schedules s11/s16"],
]

SIZING = [
    ["Auckland", "NORTHERN (bid)", 84531, 40.6, "Supplementary on-demand; scheduled OUT of scope", "2-hr urgent response; 6-site patrols; 24/7 alarm response 15+ sites; HNZ supplies shirts+covert vests (may change)"],
    ["Counties Manukau", "NORTHERN (bid)", 23120, 11.1, "Supplementary on-demand only", "1-24 hr response set per request; ASG supplies vests; cash transport possible"],
    ["Waitematā", "NORTHERN (bid)", 15492, 7.4, "Supplementary on-demand only", "HNZ supplies vests + patrol vehicle (Restricted licence+); fortnightly meetings"],
    ["Northland", "NORTHERN (decision)", 67942, 32.7, "FULLY OUTSOURCED: ~1,232 sched hrs/wk + SOC", "45-min response district-wide; 4 hospitals incl. Kaitāia/Dargaville/Kawakawa; OC post 16h may go 24h; ASG pays training backfill"],
    ["Canterbury", "No bid", 217861, 104.7, "Fully outsourced; 3,357.5 hrs/wk", "1-hr response; patient watch 25-60 hrs/day"],
    ["Waikato", "No bid", 95597, 46.0, "Fully outsourced roster ~1,680 hrs/wk", "Secondary-employment ban"],
    ["MidCentral", "No bid", 60196, 28.9, "Fully outsourced + control room", "2-min Level A response"],
    ["Southern", "No bid", 52445, 25.2, "Mixed; 784 sched hrs/wk", "Queenstown labour market"],
    ["Taranaki", "No bid", 50725, 24.4, "Mixed; large 24/7 roster (V2 increased)", "Supplier radio network"],
    ["West Coast", "No bid", 11728, 5.6, "Fully outsourced; 196 hrs/wk all nights", "Two towns 100km apart"],
    ["Bay of Plenty", "No bid", 10140, 4.9, "On-Demand only (MH sites)", "1-hr notice capability"],
    ["Wairoa", "No bid", 8823, 4.2, "Fully outsourced; 168 hrs/wk lone post", "Lone worker"],
    ["Whanganui", "No bid", 5993, 2.9, "Fully outsourced; ~100→243 hrs/wk", "Sunday overlap ambiguity"],
    ["South Canterbury", "No bid", 4951, 2.4, "Fully outsourced; 77 hrs/wk nights", "Talbot patrol contradiction"],
    ["Hawkes Bay", "No bid", 4400, 2.1, "Supplementary on-demand", "2-hr urgent response"],
    ["Lakes", "No bid", 3600, 1.7, "Supplementary on-demand", "230km MH transfers"],
    ["Nelson Marlborough", "No bid", 519, 0.2, "Supplementary ad hoc only", "3-hr response, towns 115km apart"],
]

RISKS = [
    ["1", "No guaranteed hours; panel allocation discretionary (direct sourcing + location); realistic share 10-25% of historical volume", "HIGH", "Price standby into rates; no fixed-cost build until volume flows; panel seat = option value"],
    ["2", "No price indexation over up to 4 years; all-inclusive rates; downward-only ratchets; no ASG termination right", "HIGH", "Departure #1 (indexation clause); rate-floor model + stage-2 walk-away red lines"],
    ["3", "Uncapped liability; negligence carve-out; failure-to-supply indemnity incl. patient-care costs", "HIGH", "Departures #2-4; broker alignment with contract definitions"],
    ["4", "1 Apr 2027 minimum wage rise lands between pricing and start", "HIGH", "Clarification Q4; price forward; assumption register"],
    ["5", "Mobilisation gates compress the 1-month transition (COA/screening/Children's Act/HSO VRT)", "HIGH", "Pre-vetted bench; screening starts at preferred-supplier stage"],
    ["6", "Training repayment (<3-month leavers) + annual revalidations + travel/accom (+ Northland backfill)", "MED", "Retention measures; training-attrition allowance"],
    ["7", "Metro on-demand model = revenue volatility; patrol schedules changeable at will; demand decays as HNZ in-house staffs up", "MED", "Multi-district seats; minimum-callout assumption; declining-volume model; flexible workforce"],
    ["8", "Northland = takeover vs sitting incumbent (remote 24/7 posts, 45-min response, SOC, Pool KPI) + cross-default contagion to metro seats", "HIGH if bid", "Only with incumbent intel + named SOC lead + local recruitment partner + dated plan + priced assumptions"],
    ["9", "Due diligence disclosure (claims/disputes/restructures/live Reign & Pour Police investigation) - omission = elimination/termination", "HIGH", "Legal advice THIS WEEK on materiality; truthful wording + remediation narrative"],
    ["10", "Economic Benefits criterion scores <5 and gates the whole bid (no existing iwi/Pacific partnerships)", "HIGH", "Verifiable first contact with named orgs before Friday; honest-evidence-only rule; 3 Nov go/no-go gate"],
    ["11", "Capability Q1 translation argument scores 3-4 with district SMEs (adjacent, not healthcare, evidence)", "HIGH", "Quantified HOTC dataset + verifying referee; dated uplift plan; healthcare-experienced hire in bios"],
    ["12", "Capacity double-count: HOTC/CRL bench = proposed surge pool; hospitality COAs may be Crowd Control class not Property Guard", "HIGH", "29 Oct COA-class audit gate; count net spare headcount per time band; honest surge-priority rules"],
    ["13", "Cashflow: invoice by 2nd business day (late = no contractual payment date); payment 20th following; set-off routes; no-PO-no-pay", "MED", "Billing process + PO capture discipline from day one"],
    ["14", "Data/cyber: NZ residency vs Deputy AU hosting; encryption-key handover; pen tests; Annexure E/G breach = DEEMED material breach = immediate termination", "HIGH", "Written hosting confirmations pre-submission; offshore-consent + deemed-breach departures; cyber owner + calendar"],
    ["15", "Time of the essence (cl 60.1) + self-report any breach (cl 21.1(o)) feed PIP/termination machinery", "MED", "Departure #15; escalation protocol satisfying 21.1(o) without over-disclosing"],
    ["16", "Pool KPI = standing overstaffing commitment (leave cover contractualised), esp. Northland thin markets", "MED", "Assumption #11; Pool-resize-on-volume-change KPI proposal; cost into rate floor"],
    ["17", "Uniform direction (non-militaristic, not all-black/navy) vs ASG rebrand", "LOW", "HNZ uniform variant at mobilisation"],
    ["18", "Change-of-control consent required mid-term (>50% deemed; in-flight ASG share transactions)", "MED", "Factor into ASG equity/restructure planning; DD restructure answer with advice"],
    ["19", "Probity breach = exclusion", "HIGH", "All comms via GETS only; brief the team"],
]

DEPARTURES = [
    ["1", "cl 29.2/29.8 — no indexation", "No CPI/LCI or statutory pass-through over up to 4 years", "Annual adjustment = greater of CPI/LCI + statutory labour cost pass-through (HNZ invited via Q&A #7)", "HIGH"],
    ["2", "cl 47.1/47.2(b) — uncapped liability", "Negligence carve-out removes any practical cap", "Aggregate cap (2× annual fees or insurance); carve-outs only fraud/wilful default/death-injury", "HIGH"],
    ["3", "cl 48.3 — failure-to-supply indemnity", "Covers patient-care costs; HNZ judges FM; one shift triggers", "Limit to direct cover cost; materiality threshold; objective FM test", "HIGH"],
    ["4", "cl 44.5 — liquidated damages", "Rate unseen; LDs not sole remedy; unworkable safe harbour", "LDs sole financial remedy short of termination; annual cap; same-day absence grace mechanism", "HIGH"],
    ["5", "cl 46.4 — convenience termination", "3 months' notice; cl 46.4(b)(ii) reimburses only pre-agreed unavoidable expenses", "Extend 46.4(b)(ii) to unamortised mobilisation + unavoidable redundancy whether or not pre-agreed; 6 months' notice; HNZ to facilitate staff introductions to replacement supplier", "HIGH"],
    ["6", "FM definition / cl 42.2", "No FM relief; obligations intensify in emergencies", "Mutual FM suspension; pre-agreed emergency rate uplift", "HIGH"],
    ["7", "cl 46.1(b)", "Termination for ANY unremedied breach after 10 business days", "Materiality threshold; 20-day cure for non-urgent breaches", "MED"],
    ["8", "cl 32.2/32.3 — MFC + benchmarking", "Retroactive price-match; 1-month ultimatum; savings pass-through", "Confine to same spec/risk/volume/term; adjustments by agreement", "MED"],
    ["9", "Annex F1.8 — reversed onus", "ASG must prove breach NOT its fault; uncapped", "Delete reversed onus; cyber sub-cap; Privacy Act threshold definition", "MED"],
    ["10", "cl 69 — change of control", "Consent withholdable at HNZ's absolute discretion", "Not unreasonably withheld; intra-group carve-out", "MED"],
    ["11", "cl 23.1(d)/56.2 — ISO 9001 + accreditation", "ASG likely cannot truthfully warrant at signing", "'ISO 9001 or equivalent QMS appropriate to security services'; 12-month certification runway", "HIGH"],
    ["12", "cl 59.3 — one-way non-solicit", "ASG cannot even employ HNZ staff; HNZ free to hire ASG's HNZ-trained guards", "Mutual restraint (term + 6 months or recruitment fee); delete bare 'employ or engage'", "HIGH"],
    ["13", "cl 50.1(k) — offshore hosting", "No offshore hosting of HNZ data without consent — Deputy hosts in Australia", "Written consent for named subprocessors with hosting locations disclosed", "HIGH"],
    ["14", "Annex E2.5/G2.22/E1.11 — deemed material breach", "ANY Annexure E/G breach = immediate termination, no cure period", "Confine to material non-compliance unremedied after 20 BD; proportionality carve-out for minor lapses", "MED"],
    ["15", "cl 60.1 + 21.1(o)", "Time of essence for ALL obligations; duty to self-report ANY breach", "60.1 confined to expressly time-critical obligations; 21.1(o) limited to material breaches", "MED"],
    ["16", "cl 24.8(a) — Children's Act costs", "Intervention cost recovery by set-off", "Reasonable evidenced direct costs, where risk arose from ASG non-compliance", "MED"],
    ["17", "cl 31.2 recovery routes", "Notice-based set-off, but 24.8(a)/38.1(e)(iii) route recovery through it", "Withholding limited to reasonable loss estimate with particulars; disputes to cl 39", "MED"],
    ["18", "cl 30.1/14.4 — invoicing/PO windows", "Invoice by 2nd business day (late = no contractual payment date); PO deemed accepted 3 days", "5th-7th business day, late invoices payable next cycle; 5-day PO window", "LOW"],
]

CLARIFICATIONS = [
    ["Q1", "Auckland — vehicles (narrow)", "Building on the Q&A response re supplier vehicles for offsite alarm response: confirm 'Vehicle for Mobile Patrols — Not Applicable' means no Health NZ vehicle is supplied for the s4.1 patrol run or s3.1 Alarm Response in Auckland", "Attachment F s15; Q&A #15", ""],
    ["Q2", "Northland — SOC pricing", "Should the Operations Controller post be priced as a distinct role/rate? Would a 16-to-24-hr extension be a variation at the tendered OC rate?", "Attachment H s2.1 footnote", ""],
    ["Q3", "Children's Act", "Are Security Officers under this contract Children's Workers (core/non-core) requiring Safety Checks before the Start Date? (Expect clause-24 deflection per Q&A #23 — Assumption 12 carries the lead time regardless)", "Attachment B cl 24", ""],
    ["Q4", "Pricing mechanics", "Confirm pricing-stage rates should be those applying from contract commencement 1 Apr 2027 (i.e. inclusive of the 1 Apr 2027 minimum wage adjustment)", "Pricing ~Nov-Dec 2026; start Apr 2027", ""],
    ["Q5", "Auckland — alarm response time", "Required response time for the 24/7 Alarm Response service, or agreed in SOPs?", "Attachment F s3.1 silent", ""],
    ["—", "DO NOT ASK", "Minimum callout duration (use Assumption 1 — a published 'no minimum' would foreclose it); vest spec (Q&A #8 answered); indexation willingness (Q&A #7 names the channel — propose the clause); current SOC gap staffing (HNZ refuses operational detail, Q&A #5/#22); incumbent workforce data (refused, Q&A #6/#20)", "Pruned after checking all 30 published Q&A items", "n/a"],
]

def main(out):
    wb = Workbook()
    wb.remove(wb.active)
    sheet(wb, "Key Dates", ["Date", "Event", "ASG action", "Status"], KEY_DATES, [26, 52, 52, 14], status_col=4)
    sheet(wb, "Compliance Checklist", ["Area", "Requirement", "Source", "Owner", "Status"], CHECKLIST, [13, 72, 26, 14, 12], status_col=5)
    sheet(wb, "Response Questions", ["Criterion", "#", "Question / requirement", "Per-district?", "Evidence / approach", "Status"], QUESTIONS, [16, 6, 62, 11, 46, 12], status_col=6)
    sheet(wb, "Officer Gates", ["Gate", "Who / what", "When", "Lead time", "Source"], GATES, [34, 62, 30, 18, 24])
    ws = sheet(wb, "District Sizing", ["District", "Position", "FY26 hours", "~FTE", "Delivery model", "Key notes"], SIZING, [18, 17, 12, 8, 42, 52])
    ws.cell(len(SIZING) + 2, 1, "TOTAL").font = Font(bold=True)
    ws.cell(len(SIZING) + 2, 3, sum(r[2] for r in SIZING)).font = Font(bold=True)
    ws.cell(len(SIZING) + 3, 1, "Hours are FY Jul 2025–Jun 2026 historical (Attachment D) — indication only, NO guaranteed hours. FTE = hours/2080.").font = Font(italic=True, size=9)
    sheet(wb, "Risk Register", ["#", "Risk", "Severity", "Treatment"], RISKS, [5, 62, 11, 62])
    sheet(wb, "Departure Register", ["#", "Clause", "Issue", "Proposed position", "Priority"], DEPARTURES, [5, 26, 44, 52, 10])
    sheet(wb, "Clarifications — by 30 Oct", ["#", "Topic", "Question", "Context", "Lodged?"], CLARIFICATIONS, [5, 24, 62, 34, 10], status_col=5)
    wb.save(out)
    print("Written:", out)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "HNZ_RFP_0018709_Compliance_Matrix.xlsx")
