#!/usr/bin/env python3
"""
Generate the SLS RTC / Ryan Webby disciplinary + employment-process pack.

Produces editable Word (.docx) deliverables:
  00 - Process Guide (NZ-compliant) — master reference
  01 - File Note & Letter - Radio Incident (send today)
  02 - Investigation Meeting - Invitation Letter
  03 - Disciplinary Meeting - Notice & Allegations
  04 - Verbal Warning - Confirmation Letter
  05 - Written / Final Written Warning
  06 - Performance Improvement Plan (PIP)
  07 - Disciplinary Outcome - Dismissal Letter
  08 - Meeting Record (Minutes) Template

Fill-in fields are shown as [LIKE THIS] with yellow highlight.
Guidance notes are grey italic and should be deleted before sending.

Run:  ~/Desktop/Dev/Claude/.venv/bin/python \
        ~/Desktop/Dev/Claude/scripts/asg/generate_ryan_webby_disciplinary_pack.py
"""

import os
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.text import WD_COLOR_INDEX

OUT_DIR = os.path.expanduser("~/Desktop/ASG/HR/Ryan Webby - Disciplinary Pack")
os.makedirs(OUT_DIR, exist_ok=True)

EMPLOYER = "SLS RTC Limited"
EMP_ADDR = "7/220 Queen Street, Auckland | +64 9 921 5710 | sales@slsrtc.co.nz"
EMPLOYEE = "Ryan Webby"
EMP_HOME = "11 Humboldt Street, Sydenham, Christchurch"
ROLE = "Retail Security Officer (Covert Loss Prevention)"

GREY = RGBColor(0x77, 0x77, 0x77)
NAVY = RGBColor(0x1F, 0x3B, 0x63)
RED = RGBColor(0xB0, 0x00, 0x00)


# ---------- helpers ----------
def new_doc():
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(11)
    for section in doc.sections:
        section.top_margin = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
    return doc


def letterhead(doc):
    p = doc.add_paragraph()
    r = p.add_run(EMPLOYER)
    r.bold = True
    r.font.size = Pt(15)
    r.font.color.rgb = NAVY
    sub = doc.add_paragraph()
    rs = sub.add_run(EMP_ADDR)
    rs.font.size = Pt(8.5)
    rs.font.color.rgb = GREY
    doc.add_paragraph()


def title(doc, text, color=NAVY, size=16):
    p = doc.add_paragraph()
    p.space_after = Pt(6)
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(size)
    r.font.color.rgb = color
    return p


def h(doc, text, size=12.5):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(size)
    r.font.color.rgb = NAVY
    return p


def para(doc, text="", bold=False, italic=False, size=11, color=None, after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    if text:
        r = p.add_run(text)
        r.bold = bold
        r.italic = italic
        r.font.size = Pt(size)
        if color:
            r.font.color.rgb = color
    return p


def note(doc, text):
    """Grey italic guidance note — delete before sending."""
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("» " + text)
    r.italic = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = GREY
    return p


def bullet(doc, text, bold_lead=None):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(2)
    if bold_lead:
        r = p.add_run(bold_lead)
        r.bold = True
    p.add_run(text)
    return p


def numbered(doc, text, bold_lead=None):
    p = doc.add_paragraph(style="List Number")
    p.paragraph_format.space_after = Pt(3)
    if bold_lead:
        r = p.add_run(bold_lead)
        r.bold = True
    p.add_run(text)
    return p


def rich(doc, segments, after=6):
    """segments = list of (text, dict-of-attrs). attrs: bold, italic, fill(bool), color."""
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    for text, attrs in segments:
        r = p.add_run(text)
        r.bold = attrs.get("bold", False)
        r.italic = attrs.get("italic", False)
        if attrs.get("size"):
            r.font.size = Pt(attrs["size"])
        if attrs.get("color"):
            r.font.color.rgb = attrs["color"]
        if attrs.get("fill"):
            r.font.highlight_color = WD_COLOR_INDEX.YELLOW
    return p


def field(text):
    """A fill-in field tuple (yellow highlight)."""
    return (text, {"fill": True})


def line(doc):
    p = doc.add_paragraph()
    r = p.add_run("_" * 92)
    r.font.color.rgb = GREY
    return p


def sign_block(doc, who_label="Signed on behalf of SLS RTC Limited"):
    doc.add_paragraph()
    rich(doc, [(who_label, {"bold": True})], after=14)
    rich(doc, [("Name: ", {}), field("[NAME]"), ("     Position: ", {}), field("[Director / GM / Regional Manager]")])
    rich(doc, [("Signature: ", {}), ("______________________________", {}), ("     Date: ", {}), field("[DD/MM/YYYY]")])


def save(doc, name):
    path = os.path.join(OUT_DIR, name)
    doc.save(path)
    print("  wrote:", name)
    return path


def addressee_block(doc):
    para(doc, "PRIVATE & CONFIDENTIAL", bold=True, size=10, color=RED, after=8)
    rich(doc, [("Date: ", {"bold": True}), field("[DD/MM/YYYY]")], after=2)
    para(doc, EMPLOYEE, bold=True, after=0)
    para(doc, EMP_HOME, after=0)
    rich(doc, [("Delivery: ", {"bold": True}), ("hand-delivered / email to ", {}), ("Mrrawebby@gmail.com", {}), (" / post (tick one)", {})], after=8)
    rich(doc, [("Dear ", {}), ("Ryan,", {"bold": True})])


# =====================================================================
# 00 — PROCESS GUIDE
# =====================================================================
def doc_00_guide():
    doc = new_doc()
    letterhead(doc)
    title(doc, "Managing Ryan Webby — Disciplinary & Employment Process Guide")
    para(doc, "New Zealand-compliant. Internal management reference — NOT to be given to the employee.",
         italic=True, color=GREY, size=9.5)
    para(doc, "Prepared for: SLS RTC Limited (Directors / Christchurch Regional Manager / General Manager)",
         size=9.5, color=GREY)

    h(doc, "0.  Read this first — the two rules that keep you safe")
    numbered(doc, "An investigation meeting is fact-finding ONLY. No warning, sanction or decision can be issued at it. A disciplinary meeting is a separate, later step that must be preceded by written notice. Never blur the two.", bold_lead="Investigation ≠ discipline.  ")
    numbered(doc, "A warning, an unpaid stand-down, a pay dock, a demotion or a dismissal are all sanctions. None may be imposed without a proper process (written notice → meeting → chance to respond → adjournment → written outcome). This is the exact mistake made in the James Sison matter (Apr 2026) — do not repeat it.", bold_lead="No sanction without process.  ")

    h(doc, "1.  Ryan's status — know where you stand")
    bullet(doc, "Full-time employee, SLS RTC Limited, $26.50/hr, commenced 2025.", bold_lead="Employment: ")
    bullet(doc, "He is well past the 90-day probation/trial in his contract. He has FULL unjustified-dismissal protection. Every step must pass the s103A justification test (below).", bold_lead="Protection: ")
    rich(doc, [("Trial period — moot for Ryan, but know the current rule: ", {"bold": True}),
               ("since 23 December 2023 a 90-day trial period is available to employers of ANY size (the old 'fewer than 20 employees' limit was repealed). To be valid it must be signed BEFORE the employee starts and only bars an unjustified-DISMISSAL claim. It cannot apply to Ryan regardless — he is ~10–16 months in, long past 90 days. Note: clause 3 muddles 'probation' and 'trial period' wording; worth tidying in your template, but it gives you no protection with Ryan.", {})])

    h(doc, "2.  The radio incident (sent home [DATE]) — pay decision")
    rich(doc, [("Pay him for the shift. Do not dock his pay. ", {"bold": True, "color": RED}),
               ("Treat the uncharged radio as a separate conduct matter.", {})])
    bullet(doc, "Your contract gives NO right to an unpaid stand-down. The only suspension clause (13(e)) is suspension ON PAY. Sending him home unpaid is an unjustified disadvantage risk.")
    bullet(doc, "Withholding the pay = a wage deduction. Even with the clause 6(g) 'default' wording, the Wages Protection Act 1983 requires you to consult him first and act reasonably. An on-the-spot dock fails that.")
    bullet(doc, "The disputed amount is ~$130–240. An unjustified-disadvantage grievance can cost tens of thousands. The maths is not close — pay it.")
    bullet(doc, "Pay any time already worked regardless. If he had signed on, been briefed, or done any work before being sent home, that time must be paid at least the minimum wage — sending him home does not erase time already worked (Minimum Wage Act 1983).")
    bullet(doc, "Docking pay is NOT a disciplinary tool in NZ. The lawful responses are a warning, a PIP, or dismissal via fair process — never a fine on wages. A deduction may only ever reflect a real, measurable, proportionate loss, not a punishment.")
    bullet(doc, "Proportionality is your weak point if challenged. Sending him home for the WHOLE day, when a radio can usually be charged in under an hour or a spare issued, is likely disproportionate under the s103A test. Fix it operationally: keep spare charged radios and a shift-start equipment-check routine.")
    bullet(doc, "The radio IS a real breach — just deal with it correctly. The Woolworths SOP expressly requires 'RT's must be charged, working and used at all times'; without it he cannot make the mandatory two-person approach, so it is a safety-critical SOP breach (good grounds for the conduct process), even though the pay is still due.")
    bullet(doc, "Handle the radio through the conduct process (Template 01 today; then 02/03 as needed). Whether it is infringement #1 (→ verbal warning) or an escalation depends on what is already on his file — confirm that before deciding the level.")
    note(doc, "Only-if-you-must exception: non-payment is arguable ONLY if the SOP clearly makes charging the radio his duty, no spare was available, he could do no useful work, AND you consult him first. Even then it is contestable and not worth it for a repeat-issues employee whose record you want spotless.")

    h(doc, "3.  The correct process — step by step")
    para(doc, "Use this sequence for the radio issue and for consolidating his repeated issues.", size=10, color=GREY, italic=True)
    numbered(doc, "Gather the facts. Roster, who sent him home & what was said, whether a spare radio/battery existed, the SOP requiring a charged radio, and his prior history. If facts are already clear, a formal investigation meeting may not be needed — but if in doubt, hold one (Template 02).", bold_lead="Establish the facts.  ")
    numbered(doc, "Decide whether the facts, if true, could justify disciplinary action. If yes, proceed. If it is a performance (capability) issue rather than conduct, consider a PIP (Template 06) instead of / alongside warnings.", bold_lead="Decide if it is disciplinary.  ")
    numbered(doc, "Written notice of a disciplinary meeting (Template 03). Must set out: the specific allegation(s); the evidence (attach it); that the outcome could be [a warning / dismissal]; his right to bring a support person or representative; enough time to prepare (at least 24–48h); and that no decision will be made until he has responded.", bold_lead="Issue the notice.  ")
    numbered(doc, "Hold the meeting. Put each allegation, hear his explanation in full, take minutes (Template 08). Do NOT announce an outcome in the room.", bold_lead="Meet.  ")
    numbered(doc, "Adjourn and genuinely consider his response with an open mind. If new issues surface, put them to him before deciding.", bold_lead="Adjourn & consider.  ")
    numbered(doc, "Written outcome letter (Template 04/05/07). State the finding, the decision and reasons, the standard expected, the review period, the consequence of repetition, and his personal-grievance rights (90 days).", bold_lead="Decide & confirm in writing.  ")

    h(doc, "4.  The warning ladder (contract clause 13(e))")
    para(doc, "SLS RTC's normal practice, per Ryan's own agreement:")
    bullet(doc, "1st infringement → verbal warning (confirm in writing — Template 04)")
    bullet(doc, "2nd infringement → final written warning (Template 05)")
    bullet(doc, "3rd infringement → dismissal (Template 07)")
    rich(doc, [("Caveat: ", {"bold": True}),
               ("the contract says each situation is 'considered on its merits'. Serious misconduct (clause 13(d) — e.g. intentional SOP breach, refusing a lawful instruction) can justify summary dismissal without prior warnings, but only after a fair process. A one-off uncharged radio is very unlikely to be serious misconduct.", {})])

    h(doc, "5.  Building the 'repeated issues' case")
    bullet(doc, "List every prior issue with dates, what was said/done, and whether anything is in writing. Undocumented verbal tellings-off carry little weight — you can rely on a documented pattern, not memory.")
    bullet(doc, "If little is documented, treat the current incident as the point you start a clean, well-recorded trail. Do not back-date or inflate history.")
    bullet(doc, "Keep conduct issues (radio, lateness, SOP breaches) and any performance/capability issues on separate tracks — the fair process differs slightly.")

    h(doc, "6.  Legal guardrails (keep these in mind at every step)")
    bullet(doc, "Was the action one a fair and reasonable employer could have taken in all the circumstances, at the time? Did you investigate fairly, raise concerns, give a genuine chance to respond, and keep an open mind? If any of these is 'no', the action is unjustified.", bold_lead="s103A justification test: ")
    bullet(doc, "Be active, communicative, and don't mislead. Give him information relevant to decisions about his job and a real chance to comment before deciding.", bold_lead="Good faith (s4): ")
    bullet(doc, "He may bring a support person or representative to any investigation or disciplinary meeting. Offer this in writing every time.", bold_lead="Representation: ")
    bullet(doc, "He has 90 days from the action (or from when he knew of it) to raise a personal grievance (s114 ERA 2000). Your outcome letters must state this.", bold_lead="PG window: ")
    bullet(doc, "No deductions from wages without written authority AND, even under a general clause, prior consultation on the specific deduction (s5A); the deduction must be reasonable and reflect a real, proportionate loss — never a punishment.", bold_lead="Wages Protection Act 1983: ")

    h(doc, "7.  Common mistakes to avoid")
    bullet(doc, "Issuing a 'verbal warning' at the end of a meeting that was only ever an investigation (the Sison error).")
    bullet(doc, "Announcing the outcome in the meeting instead of adjourning to consider.")
    bullet(doc, "Pre-writing the warning/dismissal letter before hearing his side (shows a closed mind).")
    bullet(doc, "Docking pay or standing him down unpaid as an on-the-spot penalty.")
    bullet(doc, "Vague allegations ('attitude problem') instead of specific, dated facts.")

    h(doc, "8.  Which template to use when")
    bullet(doc, "01 — File note + short neutral letter. Use today for the radio incident.", bold_lead="")
    bullet(doc, "02 — Investigation meeting invite. Use when facts need establishing first.", bold_lead="")
    bullet(doc, "03 — Disciplinary meeting notice. Use once you decide the matter is disciplinary.", bold_lead="")
    bullet(doc, "04 — Verbal warning confirmation. First infringement outcome.", bold_lead="")
    bullet(doc, "05 — Written / final written warning. Second infringement outcome.", bold_lead="")
    bullet(doc, "06 — PIP. For performance/capability rather than conduct.", bold_lead="")
    bullet(doc, "07 — Dismissal outcome letter. Final step, after fair process.", bold_lead="")
    bullet(doc, "08 — Meeting record. Take minutes at EVERY meeting.", bold_lead="")
    bullet(doc, "09 — Case Summary & Allegation Matrix (CONFIDENTIAL). Ryan-specific: maps his issues to clauses, pre-drafts the allegations, lists the evidence to gather. Read this before running the process.", bold_lead="")

    para(doc, "")
    para(doc, "This guide summarises how to apply the process correctly. It is not a substitute for advice from your employment lawyer on any contested or high-value matter.",
         italic=True, size=9, color=GREY)
    save(doc, "00 - Process Guide - Managing Ryan Webby (NZ-compliant).docx")


# =====================================================================
# 01 — FILE NOTE + RADIO LETTER
# =====================================================================
def doc_01_filenote():
    doc = new_doc()
    letterhead(doc)
    title(doc, "Part A — Internal File Note (Radio Incident)", size=14)
    para(doc, "For the employee's confidential HR file. Do NOT send this part to the employee.", italic=True, color=GREY, size=9.5)
    rich(doc, [("Employee: ", {"bold": True}), (EMPLOYEE + " — " + ROLE, {})], after=2)
    rich(doc, [("Date/time of incident: ", {"bold": True}), field("[DD/MM/YYYY, time]")], after=2)
    rich(doc, [("Recorded by: ", {"bold": True}), field("[Name / position]")], after=8)
    h(doc, "What happened (facts only)", 11.5)
    rich(doc, [("Ryan presented for his rostered shift at ", {}), field("[site]"), (" at approximately ", {}),
               field("[time]"), (". His two-way radio was not charged. A charged radio is a mandatory client-SOP requirement — the Woolworths (NZ) Covert LP SOP v1 (06.03.2024) states “RT’s (Radio telephones) must be charged, working and used at all times” — and without it he could not verify a concealment with a colleague or make the mandatory two-person approach. He was therefore unable to be deployed and was sent home by ", {}),
               field("[manager name]"), (".", {})])
    h(doc, "Key facts to record now (while fresh)", 11.5)
    bullet(doc, "Was a spare radio / battery available on site? " )
    rich(doc, [("   → ", {}), field("[Yes / No — detail]")], after=2)
    bullet(doc, "Was he offered the chance to charge it / return later?")
    rich(doc, [("   → ", {}), field("[Yes / No — detail]")], after=2)
    bullet(doc, "Exact words used when he was sent home:")
    rich(doc, [("   → ", {}), field("[quote]")], after=2)
    bullet(doc, "Whose radio is it (SLS-issued to Ryan / client / site pool)?")
    rich(doc, [("   → ", {}), field("[detail]")], after=2)
    bullet(doc, "Prior related issues on file (dates):")
    rich(doc, [("   → ", {}), field("[list, or 'none documented']")], after=6)
    rich(doc, [("Pay decision: ", {"bold": True, "color": RED}),
               ("shift to be PAID as normal. Radio issue to be addressed as a conduct matter (see Part B and the Process Guide). No pay deduction.", {})])

    doc.add_page_break()
    letterhead(doc)
    title(doc, "Part B — Letter to Ryan (send today)", size=14)
    note(doc, "Neutral and factual. This is NOT a warning and uses no warning language. It records the incident and flags that it will be discussed. Send by email and/or hand.")
    addressee_block(doc)
    para(doc, "")
    rich(doc, [("I am writing to record that on ", {}), field("[date]"), (" you attended your rostered shift at ", {}),
               field("[site]"), (" but your two-way radio was not charged. As a charged radio is required to carry out the role safely, you were unable to be deployed and were sent home for the day. You will be paid for this shift as normal.", {})])
    para(doc, "Being ready to work with functioning, charged equipment is an important part of the role. I would like to discuss this with you so I understand what happened and we can make sure it does not happen again.")
    rich(doc, [("I will be in touch shortly to arrange a time to talk. You are welcome to bring a support person or representative to that discussion. This letter is not a warning; it is a record of what occurred and a note that we will discuss it.", {})])
    para(doc, "If you would like to add anything in the meantime, please let me know.")
    para(doc, "")
    para(doc, "Kind regards,")
    sign_block(doc)
    save(doc, "01 - File Note & Letter - Radio Incident (send today).docx")


# =====================================================================
# 02 — INVESTIGATION MEETING INVITATION
# =====================================================================
def doc_02_investigation():
    doc = new_doc()
    letterhead(doc)
    title(doc, "Invitation to an Investigation Meeting", size=15)
    note(doc, "Fact-finding only. No decision or sanction will result from this meeting. Use when you need to establish the facts before deciding whether the matter is disciplinary.")
    addressee_block(doc)
    para(doc, "")
    para(doc, "I am writing to invite you to a meeting to discuss and establish the facts about the following matter(s):")
    rich(doc, [field("[Describe the matter, e.g. 'On [date] you attended your rostered shift without a charged radio and were unable to be deployed.']")], after=8)
    h(doc, "Purpose of this meeting")
    para(doc, "The purpose is fact-finding only. This is an investigation meeting, not a disciplinary meeting. No decision, warning or other action will be made or taken at or as a result of this meeting. Its purpose is to gather information.")
    h(doc, "Meeting details")
    rich(doc, [("Date: ", {"bold": True}), field("[DD/MM/YYYY]"), ("    Time: ", {"bold": True}), field("[time]")], after=2)
    rich(doc, [("Location: ", {"bold": True}), field("[venue / video link]")], after=2)
    rich(doc, [("Will be conducted by: ", {"bold": True}), field("[name / position]")], after=8)
    h(doc, "Your rights")
    bullet(doc, "You may bring a support person or representative (for example a friend, family member, lawyer or union representative).")
    bullet(doc, "You may ask questions and give your account of events.")
    bullet(doc, "If you need any information or documents to prepare, please tell me and I will provide them where I can.")
    para(doc, "")
    para(doc, "Please confirm you can attend, and let me know if the time does not suit or if you need any assistance to take part.")
    para(doc, "")
    para(doc, "Kind regards,")
    sign_block(doc)
    save(doc, "02 - Investigation Meeting - Invitation Letter.docx")


# =====================================================================
# 03 — DISCIPLINARY MEETING NOTICE
# =====================================================================
def doc_03_disciplinary_notice():
    doc = new_doc()
    letterhead(doc)
    title(doc, "Notice of Disciplinary Meeting", size=15)
    note(doc, "Issue this only after you have the facts and have decided the matter could justify disciplinary action. It must reach the employee with enough time to prepare (24–48h minimum) and must attach the evidence.")
    addressee_block(doc)
    para(doc, "")
    para(doc, "I am writing to invite you to a disciplinary meeting to discuss the following allegation(s), which if substantiated may amount to misconduct / poor performance under your employment agreement and the SLS RTC Code of Conduct (clause 13):")
    h(doc, "Allegation(s)")
    numbered(doc, "", bold_lead="")
    rich(doc, [field("[Allegation 1 — specific and dated, e.g. 'That on [date] you attended your rostered shift at [site] without a charged radio, contrary to [SOP ref], and were unable to perform your duties.']")], after=4)
    rich(doc, [field("[Allegation 2 — if any]")], after=8)
    h(doc, "The evidence")
    para(doc, "The information I will be relying on is set out in the documents enclosed with this letter:")
    bullet(doc, field("[list enclosures — e.g. file note dated [x], roster, SOP extract, prior warning letters]")[0])
    h(doc, "Possible outcomes")
    rich(doc, [("If the allegation(s) are substantiated, the possible outcomes include ", {}),
               field("[a first/verbal warning / a final written warning / dismissal]"),
               (". No decision has been made and none will be made until you have had a full opportunity to respond and I have genuinely considered what you say.", {})])
    h(doc, "Meeting details")
    rich(doc, [("Date: ", {"bold": True}), field("[DD/MM/YYYY]"), ("    Time: ", {"bold": True}), field("[time]")], after=2)
    rich(doc, [("Location: ", {"bold": True}), field("[venue / video link]")], after=2)
    rich(doc, [("Chaired by: ", {"bold": True}), field("[name / position]")], after=8)
    h(doc, "Your rights")
    bullet(doc, "You are entitled to bring a support person or representative. I strongly encourage you to do so.")
    bullet(doc, "You will have a full and genuine opportunity to respond to each allegation and to raise anything you wish me to take into account.")
    bullet(doc, "You may request further information or an adjournment if you need more time to prepare or respond.")
    para(doc, "")
    para(doc, "Please confirm your attendance and let me know who (if anyone) will accompany you. If the time or format does not work for you, contact me and I will try to accommodate a reasonable alternative.")
    para(doc, "")
    para(doc, "Kind regards,")
    sign_block(doc)
    save(doc, "03 - Disciplinary Meeting - Notice & Allegations.docx")


# =====================================================================
# 04 — VERBAL WARNING CONFIRMATION
# =====================================================================
def doc_04_verbal():
    doc = new_doc()
    letterhead(doc)
    title(doc, "Confirmation of Verbal Warning", size=15)
    note(doc, "Send only AFTER a disciplinary meeting where, having considered his response, you decided a first (verbal) warning is warranted. Confirming a verbal warning in writing is good practice and creates the record.")
    addressee_block(doc)
    para(doc, "")
    rich(doc, [("Following our disciplinary meeting on ", {}), field("[date]"),
               (", and having considered your response, I am writing to confirm that you have been given a ", {}),
               ("verbal warning", {"bold": True}), (".", {})])
    h(doc, "The concern")
    rich(doc, [field("[State the finding, e.g. 'On [date] you attended your rostered shift without a charged radio and were unable to be deployed. This breached [SOP/policy].']")], after=6)
    para(doc, "I took into account what you told me at the meeting, including " )
    rich(doc, [field("[summarise his explanation and how it was weighed]")], after=8)
    h(doc, "The standard expected")
    para(doc, "You must attend every rostered shift ready to work, with all required equipment (including a charged radio) in working order, and comply with all SLS RTC and client SOPs and policies.")
    h(doc, "What happens next")
    rich(doc, [("This warning will remain on your file for ", {}), field("[e.g. 6 / 12] months"),
               (". If there is a further infringement during this period, it may lead to a final written warning and, ultimately, to dismissal.", {})])
    h(doc, "Support")
    para(doc, "If anything is making it difficult for you to meet these expectations, please tell me so we can look at how to help.")
    h(doc, "Your rights")
    para(doc, "If you disagree with this warning you may raise a personal grievance. Any personal grievance must be raised with SLS RTC within 90 days of the action you are aggrieved by.")
    para(doc, "")
    para(doc, "Kind regards,")
    sign_block(doc)
    save(doc, "04 - Verbal Warning - Confirmation Letter.docx")


# =====================================================================
# 05 — WRITTEN / FINAL WRITTEN WARNING
# =====================================================================
def doc_05_written():
    doc = new_doc()
    letterhead(doc)
    title(doc, "Written Warning", size=15)
    note(doc, "Choose the heading: 'Written Warning' or 'Final Written Warning'. Send only after a disciplinary meeting and genuine consideration of his response.")
    addressee_block(doc)
    para(doc, "")
    rich(doc, [("Following our disciplinary meeting on ", {}), field("[date]"),
               (", and having carefully considered your response, I am writing to issue you with a ", {}),
               field("[written / FINAL written]"), (" warning.", {})])
    h(doc, "The finding")
    rich(doc, [field("[State the substantiated allegation and the facts found, with dates.]")], after=6)
    para(doc, "In reaching this decision I considered your explanation, namely ")
    rich(doc, [field("[summarise his response and why it did / did not change the outcome]")], after=8)
    h(doc, "The standard expected")
    rich(doc, [field("[State clearly what must change and by when — e.g. attend all shifts ready to work with a charged radio; full SOP compliance.]")], after=6)
    h(doc, "Consequence of any further issue")
    rich(doc, [("This ", {}), field("[written / final written]"),
               (" warning will remain on your file for ", {}), field("[e.g. 12] months"),
               (". Any further misconduct or failure to meet the required standard during this period may result in ", {}),
               field("[a final written warning / the termination of your employment]"), (".", {})])
    h(doc, "Support")
    para(doc, "We want you to succeed in your role. If there is anything affecting your ability to meet these expectations, please raise it with me.")
    h(doc, "Your rights")
    para(doc, "You may seek advice on this decision and, if you disagree with it, you may raise a personal grievance. Any personal grievance must be raised with SLS RTC within 90 days of the action complained of.")
    para(doc, "")
    para(doc, "Please sign below to acknowledge receipt (acknowledging receipt does not mean you agree with the warning).")
    doc.add_paragraph()
    rich(doc, [("Employee acknowledgement of receipt: ", {"bold": True})], after=14)
    rich(doc, [("Signature: ", {}), ("______________________________", {}), ("     Date: ", {}), field("[DD/MM/YYYY]")])
    sign_block(doc)
    save(doc, "05 - Written or Final Written Warning.docx")


# =====================================================================
# 06 — PIP
# =====================================================================
def doc_06_pip():
    doc = new_doc()
    letterhead(doc)
    title(doc, "Performance Improvement Plan (PIP)", size=15)
    note(doc, "Use for capability / performance issues (things he cannot yet do to standard) rather than conduct (things he chose to do or not do). A PIP is supportive, not punitive — but a failed PIP can support a fair dismissal for performance.")
    rich(doc, [("Employee: ", {"bold": True}), (EMPLOYEE + " — " + ROLE, {})], after=2)
    rich(doc, [("Manager: ", {"bold": True}), field("[name / position]")], after=2)
    rich(doc, [("Plan start: ", {"bold": True}), field("[DD/MM/YYYY]"), ("     Review period: ", {"bold": True}), field("[e.g. 4–8 weeks]")], after=2)
    rich(doc, [("Review dates: ", {"bold": True}), field("[week 2 date] · [week 4 date] · [final review date]")], after=8)

    h(doc, "1.  Areas of concern")
    rich(doc, [field("[Describe the performance gaps specifically and factually, with examples and dates.]")], after=6)
    h(doc, "2.  Required standard & objectives")
    para(doc, "The following must be achieved and maintained:")
    bullet(doc, field("[Objective 1 — specific, measurable, with the standard defined]")[0])
    bullet(doc, field("[Objective 2]")[0])
    bullet(doc, field("[Objective 3]")[0])
    h(doc, "3.  Support SLS RTC will provide")
    bullet(doc, field("[e.g. re-training on SOPs, buddy shift, equipment check-in routine, weekly 1:1s]")[0])
    h(doc, "4.  How progress will be measured")
    rich(doc, [field("[Define the evidence — e.g. shift readiness checks, incident reports, client feedback, ROI metrics.]")], after=6)
    h(doc, "5.  Consequences")
    para(doc, "This plan is intended to help you succeed. If the required standard is not achieved and maintained by the end of the review period, this may lead to further action under your employment agreement, up to and including termination of employment for reasons of performance, following a fair process.")
    h(doc, "6.  Review log")
    tbl = doc.add_table(rows=1, cols=3)
    tbl.style = "Light Grid Accent 1"
    hdr = tbl.rows[0].cells
    hdr[0].text = "Review date"
    hdr[1].text = "Progress / evidence"
    hdr[2].text = "Actions & agreed next steps"
    for _ in range(3):
        tbl.add_row()
    doc.add_paragraph()
    rich(doc, [("Employee signature: ", {}), ("__________________", {}), ("  Date: ", {}), field("[  ]"),
               ("      Manager signature: ", {}), ("__________________", {}), ("  Date: ", {}), field("[  ]")])
    save(doc, "06 - Performance Improvement Plan (PIP).docx")


# =====================================================================
# 07 — DISMISSAL OUTCOME LETTER
# =====================================================================
def doc_07_dismissal():
    doc = new_doc()
    letterhead(doc)
    title(doc, "Outcome of Disciplinary Process — Termination of Employment", size=14)
    note(doc, "Use ONLY after a full and fair process, genuine consideration of his response, and where dismissal is a decision a fair and reasonable employer could reach. If relying on serious misconduct for summary (no-notice) dismissal, adjust the notice section and be certain the conduct qualifies.")
    addressee_block(doc)
    para(doc, "")
    rich(doc, [("I am writing to confirm the outcome of the disciplinary meeting held on ", {}), field("[date]"),
               (", concerning ", {}), field("[the allegation(s)]"), (".", {})])
    h(doc, "The findings")
    rich(doc, [field("[Set out each allegation and the finding, with the facts relied on and dates.]")], after=6)
    h(doc, "Your response and how it was considered")
    rich(doc, [field("[Summarise what he told you at the meeting and genuinely explain why it did not alter the outcome. This section is critical to a defensible dismissal.]")], after=6)
    h(doc, "Decision")
    rich(doc, [("Having considered all of the above, including your response and your disciplinary history (", {}),
               field("[reference prior warnings and dates]"),
               ("), I have decided to terminate your employment with SLS RTC Limited.", {})])
    h(doc, "Notice and final pay")
    rich(doc, [("Your employment will end on ", {}), field("[date]"), (". ", {}),
               ("In accordance with clause 11 of your agreement you will ", {}),
               field("[be given one month's notice / be paid one month's salary in lieu of notice]"),
               (". ", {})])
    para(doc, "Your final pay, including any outstanding wages and holiday pay owed under the Holidays Act 2003, will be paid on the next pay run.")
    note(doc, "If this is a summary dismissal for SERIOUS misconduct (clause 13(d)), replace the notice sentence with: 'As this is a summary dismissal for serious misconduct, your employment ends immediately and no notice or payment in lieu of notice is payable.' Only use this if the conduct genuinely qualifies as serious misconduct.")
    h(doc, "Company property")
    para(doc, "Please return all SLS RTC and client property in your possession by [date], including any radio, ID, uniform, keys, access cards and documents.")
    h(doc, "Your rights")
    para(doc, "If you believe this decision is unjustified you may raise a personal grievance. Any personal grievance must be raised with SLS RTC within 90 days of the date of this decision. You may also seek to resolve the matter through mediation.")
    para(doc, "")
    para(doc, "Kind regards,")
    sign_block(doc)
    save(doc, "07 - Disciplinary Outcome - Dismissal Letter.docx")


# =====================================================================
# 08 — MEETING RECORD
# =====================================================================
def doc_08_minutes():
    doc = new_doc()
    letterhead(doc)
    title(doc, "Meeting Record / Minutes", size=15)
    note(doc, "Complete for EVERY investigation and disciplinary meeting. Offer the employee a copy and the chance to correct the record. Contemporaneous notes are your best protection.")
    rich(doc, [("Meeting type: ", {"bold": True}), field("[Investigation / Disciplinary]")], after=2)
    rich(doc, [("Date: ", {"bold": True}), field("[DD/MM/YYYY]"), ("   Time (start/end): ", {"bold": True}), field("[  ]")], after=2)
    rich(doc, [("Location: ", {"bold": True}), field("[venue / video]")], after=2)
    rich(doc, [("Present: ", {"bold": True}), field("[chair, note-taker, employee, support person/representative]")], after=8)

    h(doc, "1.  Matters / allegations discussed")
    rich(doc, [field("[List each matter put to the employee.]")], after=6)
    h(doc, "2.  Employee's response (record as fully as possible)")
    rich(doc, [field("[Capture his explanation for each matter, in his words where you can.]")], after=6)
    h(doc, "3.  Questions asked & answers")
    rich(doc, [field("[Key Q&A.]")], after=6)
    h(doc, "4.  Adjournment")
    rich(doc, [field("[Note the adjournment to consider — e.g. 'Meeting adjourned at [time]; no decision made in the meeting.']")], after=6)
    h(doc, "5.  Outcome / next steps")
    rich(doc, [field("[Record what was decided or that a decision will follow in writing.]")], after=8)
    line(doc)
    rich(doc, [("Employee: I confirm this is an accurate record ", {}), ("(or note corrections):", {"italic": True})], after=10)
    rich(doc, [("Signature: ", {}), ("__________________", {}), ("  Date: ", {}), field("[  ]")], after=6)
    rich(doc, [("Chair signature: ", {}), ("__________________", {}), ("  Date: ", {}), field("[  ]")])
    save(doc, "08 - Meeting Record (Minutes) Template.docx")


def doc_09_case_summary():
    doc = new_doc()
    letterhead(doc)
    title(doc, "Case Summary & Allegation Matrix — Ryan Webby", size=15)
    para(doc, "PRIVATE & CONFIDENTIAL — internal management document. Do NOT give this to the employee.",
         bold=True, size=10, color=RED)
    para(doc, "Maps Ryan's known issues to the contract clauses they engage, the severity, and the evidence you need. "
              "Use it to prioritise, to fill Templates 02 and 03, and to decide the level of any outcome.", size=10, color=GREY, italic=True)

    h(doc, "A.  The issues on the table")
    numbered(doc, "Set up / operates his own security business while employed as a covert LP officer.", bold_lead="PRIORITY — potential SERIOUS misconduct: ")
    numbered(doc, "Bad attitude to work; staff complain of constant complaining and swearing.", bold_lead="Conduct: ")
    numbered(doc, "Caught multiple times wearing a hoodie on duty (contrary to instruction / appearance SOP).", bold_lead="Conduct / SOP: ")
    numbered(doc, "Attended his rostered shift without a charged radio; unable to be deployed.", bold_lead="Conduct (the trigger): ")

    h(doc, "B.  Allegation matrix — issue → contract clause → severity")
    rows = [
        ("Issue", "Clause(s) engaged", "Level", "Evidence you need"),
        ("Own security business (no written Director authorisation)",
         "SLS 15(b) conflict / not to work for another security company; 13(f) fidelity; 13(d) 'failure to honour conflict/confidentiality conditions' & 'conduct damaging to interests'; 15(a)/(c) confidentiality & IP. PLUS Woolworths SOP: AUROR-use & confidentiality rules; 'resources/assets not to be used for personal gain' — breach 'may lead to termination or legal action'. Client-SOP breach = SLS clause 2 + 13(d) 'intentionally breaching SOPs'.",
         "Serious (potentially)",
         "Companies/NZBN + PSPLA licence check; what it does (competes?); clients approached; use of work time / equipment / AUROR / Woolworths info; any written authorisation"),
        ("Complaining & swearing at staff / bad attitude",
         "13(c) 'discourteous to other workers' / 'aggressive or argumentative'; 13(d) 'verbal abuse' (if severe). Also breaches the Woolworths SOP Acknowledgment he signed (core values: Integrity, Respect, Teamwork).",
         "Conduct (serious if severe/persistent)",
         "Written, dated statements from the staff who complained; specific incidents & words used"),
        ("Wearing a hoodie on duty",
         "Clause 2 'high standard of personal grooming' & 'work to SOPs'; 13(c) 'failure to abide by policies'; 13(d) 'disobeying reasonable instructions' if told to stop and continued",
         "Conduct (escalates if defiant)",
         "The appearance/covert SOP; record of prior instructions to stop; dates seen"),
        ("Uncharged radio",
         "SLS 13(c) 'reporting to work in such a condition that duties are not performed properly or safely' & 'failure to abide by SOPs'; SLS 13(d) 'intentionally breaching SOPs' (if repeated/deliberate). Woolworths SOP (safety-critical): 'RT's must be charged, working and used at all times.'",
         "Conduct",
         "Roster; Woolworths SOP p.4 (charged-RT rule); file note (Template 01); whether a spare was available"),
    ]
    tbl = doc.add_table(rows=0, cols=4)
    tbl.style = "Light Grid Accent 1"
    for i, (a, b, c, d) in enumerate(rows):
        cells = tbl.add_row().cells
        for cell, val in zip(cells, (a, b, c, d)):
            cell.text = ""
            rr = cell.paragraphs[0].add_run(val)
            rr.font.size = Pt(8.5)
            if i == 0:
                rr.bold = True

    h(doc, "C.  Pre-drafted allegations (paste into Template 03; fill the [brackets])")
    para(doc, "Allegation 1 — conflict of interest / competing business", bold=True, size=10.5)
    rich(doc, [("“That, while employed by SLS RTC Limited as a Covert Loss Prevention Officer, you have established and/or operate a security business ", {}),
               field("[name / NZBN]"),
               (" without the written authorisation of a Director, contrary to clauses 15(b) and 13(f) of your employment agreement; and/or that in doing so you have used, or placed at risk, SLS RTC's or its client's confidential information, methods, systems (including AUROR) or client relationships, contrary to clause 15(a) of your agreement and the Woolworths Covert LP SOP you acknowledged.”", {})], after=6)
    note(doc, "Second allegation only if the facts support it — do not allege AUROR/confidential-info misuse unless you can evidence it. Keep the bare conflict-of-interest allegation separate so it stands even if the misuse point is not made out.")
    para(doc, "Allegation 2 — conduct toward staff", bold=True, size=10.5)
    rich(doc, [("“That on ", {}), field("[dates]"),
               (" you behaved discourteously and/or aggressively toward colleagues, including persistent complaining and the use of offensive/abusive language, contrary to clause 13(c) and the standards of conduct expected under your agreement.”", {})], after=8)
    para(doc, "Allegation 3 — appearance / SOP (hoodie)", bold=True, size=10.5)
    rich(doc, [("“That on ", {}), field("[dates]"),
               (", despite ", {}), field("[prior instruction / SLS appearance standard]"),
               (", you wore a hooded top while on duty, contrary to clause 2 of your agreement (SOP compliance and grooming standard)", {}),
               (" and compromising your covert role (the need to blend in as an ordinary shopper, remain identifiable to the duty manager, and work under CCTV).”", {})], after=6)
    note(doc, "Evidence gap: the Woolworths Covert LP SOP has NO dress code and does not mention hoodies. To run this allegation you need either an SLS appearance/uniform standard, or a documented prior instruction telling Ryan not to wear a hood on duty. Without one of those, anchor it in clause 2 + the covert-role rationale above — and expect it to carry less weight than the radio and conflict issues.")
    para(doc, "Allegation 4 — uncharged radio", bold=True, size=10.5)
    rich(doc, [("“That on ", {}), field("[date]"),
               (" you attended your rostered shift without a charged radio and were unable to be deployed, contrary to the Woolworths Covert LP SOP ('RT's must be charged, working and used at all times') and clause 13(c) of your agreement, thereby preventing the mandatory two-person approach and compromising safety.”", {})], after=8)

    h(doc, "D.  The business issue — facts to establish BEFORE any decision")
    bullet(doc, "Is a company/business registered? Check the Companies Register (companies-register.companiesoffice.govt.nz) and NZBN register (nzbn.govt.nz) — get the name, NZBN, incorporation date and directors/shareholders.")
    bullet(doc, "Does it hold (or has it applied for) a PSPLA Company Licence + does he hold a Certificate of Approval? A security business legally needs these — check the licence register.")
    bullet(doc, "What does it actually do — does it compete with SLS RTC (retail LP / security guarding)?")
    bullet(doc, "Is it operating? Any clients? Has he approached or solicited ANY SLS RTC clients?")
    bullet(doc, "Is he running it during SLS work hours, or using SLS equipment, SOPs, confidential info or client lists?")
    bullet(doc, "CLIENT DATA: has he accessed or used AUROR, Woolworths store intel, LP methods or any client's confidential information for the business? (This breaches the Woolworths SOP directly and is the most serious factual line — pull his AUROR access log if you can.)")
    bullet(doc, "Did he obtain written Director authorisation (clause 15(b))? Did he disclose the business to you, or did you find out independently? (His candour matters to the outcome.)")

    h(doc, "E.  Severity & likely outcome")
    bullet(doc, "If the business genuinely competes and/or he solicited clients or used confidential information, with no written authorisation → this can support serious misconduct and, after a fair process, potentially summary dismissal (clause 13(d)).", bold_lead="Strong case: ")
    bullet(doc, "If it is dormant, non-competing and he disclosed it → likely a serious conduct issue, not summary dismissal; require him in writing to cease or to seek authorisation, plus a warning.", bold_lead="Weaker case: ")
    bullet(doc, "The conduct issues (attitude, swearing, hoodie, radio) support the overall pattern and, combined and documented, justify moving up the warning ladder — but each needs specific, dated evidence, not general impressions.", bold_lead="The pattern: ")

    h(doc, "F.  Recommended sequence")
    numbered(doc, "Today: pay the radio shift; send Template 01.")
    numbered(doc, "Collect evidence: written, dated staff complaints; the radio and appearance SOPs; the Companies/NZBN/PSPLA checks on the business.")
    numbered(doc, "Hold ONE investigation meeting (Template 02) covering all issues, with the business as the priority — fact-find only, no decision.")
    numbered(doc, "If warranted, a disciplinary meeting (Template 03) with the substantiated allegations from Section C, evidence attached, right to a representative.")
    numbered(doc, "Genuinely consider his response, then confirm the outcome in writing (Template 04/05/07).")
    note(doc, "Do NOT summarily dismiss for the business before investigating and hearing him — even strong conflict-of-interest cases are lost at the ERA when the employer skipped process or had a closed mind.")

    h(doc, "G.  Three things to watch")
    rich(doc, [("Client risk — Woolworths. ", {"bold": True, "color": RED}),
               ("Ryan is a covert operative on your biggest client's sites with AUROR access. An operative running his own security business is a serious client-trust issue. Manage the Woolworths relationship carefully, and consider restricting his AUROR / system access now as a protective measure. NOTE: limiting system access is fine, but if you stand him down from work entirely it must be ON PAY and justified (see the pay rules in the Process Guide).", {})])
    rich(doc, [("No post-employment restraint. ", {"bold": True}),
               ("This contract has confidentiality (15a), a during-employment conflict/no-competing-work clause (15b) and IP assignment (15c), but NO restraint-of-trade / non-compete for AFTER he leaves. So your leverage over the competing business is strongest WHILE he is employed (duty of fidelity) and via ongoing confidentiality — not a non-compete once employment ends. Factor this into whether you manage him out carefully or hold the line now.", {})])
    rich(doc, [("Protect confidential information now. ", {"bold": True}),
               ("Whatever the outcome, remind him in writing of his continuing confidentiality and IP obligations (clauses 15(a) and 15(c)) and consider what client/method information he can access while this runs.", {})])
    save(doc, "09 - Case Summary & Allegation Matrix (CONFIDENTIAL).docx")


def main():
    print("Generating Ryan Webby disciplinary pack →", OUT_DIR)
    doc_00_guide()
    doc_01_filenote()
    doc_02_investigation()
    doc_03_disciplinary_notice()
    doc_04_verbal()
    doc_05_written()
    doc_06_pip()
    doc_07_dismissal()
    doc_08_minutes()
    doc_09_case_summary()
    print("Done. 10 files.")


if __name__ == "__main__":
    main()
