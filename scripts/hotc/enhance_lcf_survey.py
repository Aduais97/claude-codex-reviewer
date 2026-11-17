#!/usr/bin/env python3
"""
Enhance HOTC's actual perceptions survey (Edward's 'Safety Survey - Surge Jun July.docx').
Edward's structure and wording are preserved; ASG additions are inserted in place and tagged
[ASG suggested]. Two new instruments are appended: a 30-second Public/Pedestrian Intercept
(feeds Council's own day/night safety metric) and a Methodology & Sampling page.

Source: ~/Downloads/Safety Survey - Surge Jun July.docx
Output: ~/Desktop/ASG/HOTC/2026/Safety Survey - Surge Jun July (ASG enhanced).docx
"""

import os
from docx import Document
from docx.shared import Pt, RGBColor
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC = os.path.expanduser("~/Downloads/Safety Survey - Surge Jun July.docx")
OUT = os.path.expanduser("~/Desktop/ASG/HOTC/2026/Safety Survey - Surge Jun July (ASG enhanced).docx")
NAVY = RGBColor(0x1B, 0x2A, 0x4A)
GOLD = RGBColor(0xB8, 0x86, 0x1B)

doc = Document(SRC)


def find(substr, start=0):
    for i, p in enumerate(doc.paragraphs):
        if i >= start and substr.lower() in p.text.lower():
            return p
    raise ValueError("anchor not found: " + substr)


def next_para(p):
    nxt = p._p.getnext()
    return Paragraph(nxt, p._parent) if nxt is not None else p


def _fill(para, line):
    if line.startswith("##"):
        r = para.add_run(line[2:].strip()); r.bold = True; r.font.size = Pt(10.5); r.font.color.rgb = NAVY
    elif line == "":
        pass
    else:
        tag = para.add_run("[ASG suggested]  "); tag.bold = True; tag.font.size = Pt(8.5); tag.font.color.rgb = NAVY
        b = para.add_run(line); b.font.size = Pt(10.5)


def insert_after(anchor, lines):
    cur = anchor._p
    for line in lines:
        new_p = OxmlElement('w:p'); cur.addnext(new_p); cur = new_p
        para = Paragraph(new_p, anchor._parent); para.paragraph_format.space_after = Pt(3)
        _fill(para, line)


# ── helpers for the appended new instruments (plain, not tagged — whole section is labelled) ──
def heading(text, size=14, color=NAVY, before=14):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(before); p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text); r.bold = True; r.font.size = Pt(size); r.font.color.rgb = color
    return p

def line(text, bold=False, size=10.5, italic=False, color=None, after=3):
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(after)
    r = p.add_run(text); r.bold = bold; r.italic = italic; r.font.size = Pt(size)
    if color: r.font.color.rgb = color
    return p


# ════════════════════════════════════════════════════════════════════════════
# BUSINESS SURVEY — inserts
# ════════════════════════════════════════════════════════════════════════════

# Response header (before/after matching)
insert_after(find("gathering quick feedback"), [
    "## Response details (for before/after tracking):",
    "Business name / ID: __________________________   Date: __________   Surveyor: __________",
    "Wave:   ☐ Baseline (June)    ☐ Follow-up (July)",
])

# A. Snapshot — context that sharpens targeting
insert_after(find("Daytime"), [
    "Years at this location: ______      Number of staff: ______",
    "Typical opening / closing time:   Open ________   Close ________",
])

# B. Current Sentiment — day/night split + recommend score
insert_after(find("Very unsafe"), [
    "1a. Safety here during the DAY (1–5):   ☐ 1  ☐ 2  ☐ 3  ☐ 4  ☐ 5",
    "1b. Safety here at NIGHT / evening (1–5):   ☐ 1  ☐ 2  ☐ 3  ☐ 4  ☐ 5",
])
insert_after(find("operating your business day-to-day"), [
    "3a. How safe do your STAFF feel, particularly opening and closing? (1–5):   ☐ 1  ☐ 2  ☐ 3  ☐ 4  ☐ 5",
    "3b. How likely are you to recommend the city centre as a place to do business or visit? (0–10):  ______",
])

# C. Business Impacts — quantify frequency, severity, cost, timing
insert_after(find("Rarely"), [
    "5a. When issues occur, how serious are they?   ☐ Minor  ☐ Moderate  ☐ Serious  ☐ Critical",
    "5b. In the last 30 days, roughly how many incidents affected your business? ______",
    "5c. Worst time of day for issues:   ☐ Morning  ☐ Midday  ☐ Afternoon  ☐ Evening  ☐ Late night",
    "5d. Rough impact on trade (lost sales / extra costs) per week:  $ ________   ☐ Don’t know",
])

# D. Safety Presence — visibility, attribution, response, reporting, interaction
insert_after(find("Have you noticed safety team"), [
    "6a. Roughly how often do you see the safety team?   ☐ Several times a day  ☐ Daily  ☐ Weekly  ☐ Rarely",
])
insert_after(find("Negative impact"), [
    "7a. Has the increased safety-team presence specifically changed how safe you feel?",
    "      ☐ Significant improvement   ☐ Some improvement   ☐ No change   ☐ Negative",
    "7b. If you called for help, how quickly do you think it would arrive? (1–5):   ☐ 1  ☐ 2  ☐ 3  ☐ 4  ☐ 5",
    "7c. When something happens, do you report it — and to whom?   ☐ Police   ☐ Safety team   ☐ Don’t report",
    "7d. Have you interacted directly with the team?   ☐ No   ☐ Yes — how was it?  ☐ Excellent  ☐ Good  ☐ Poor",
])

# E. Customer Experience — foot traffic + customer mentions
insert_after(find("How do your customers feel"), [
    "8a. Compared with a month ago, customer foot traffic is:   ☐ Down   ☐ About the same   ☐ Up",
])
insert_after(find("Are customers raising concerns"), [
    "9a. Do customers comment on the safety team?   ☐ Positively   ☐ Neutral   ☐ Negatively   ☐ Not mentioned",
])

# F. Future / Risks — CRL readiness
insert_after(find("No major concerns"), [
    "10a. How prepared do you feel for the City Rail Link opening and the change it brings? (1–5):   ☐ 1  ☐ 2  ☐ 3  ☐ 4  ☐ 5",
])

# H. Looking ahead (advocacy, quote, consent, funding support, permissions)
insert_after(find("Anything else"), [
    "## H. Looking ahead (ASG)",
    "13. Would you support a continued or expanded safety presence?   ☐ Yes   ☐ No   ☐ Unsure",
    "14. Would you support HOTC / Council continuing to fund a safety presence beyond this pilot?   ☐ Yes   ☐ No   ☐ Unsure",
    "15. In one sentence, what has the safety team meant for you? (a quote we may use)",
    "_______________________________________________________________________",
    "16. May we use your business name with the quote in reporting?   ☐ Yes, name + quote   ☐ Quote only (anonymous)   ☐ No",
    "17. Happy for us to check back in July?   ☐ Yes — name / contact: ____________________",
])

# ════════════════════════════════════════════════════════════════════════════
# LANDLORD / PROPERTY SURVEY — inserts
# ════════════════════════════════════════════════════════════════════════════
insert_after(find("Property Owner / Manager Check-In"), [
    "## Response details:  Property / address: ____________   Date: ________   Surveyor: ________   Wave: ☐ Baseline  ☐ Follow-up",
])
insert_after(find("Vacancy level"), [
    "Vacancy rate now: ______%      12 months ago: ______%",
    "Leasing enquiry levels vs 12 months ago:   ☐ Down   ☐ About the same   ☐ Up",
])
insert_after(find("Much stronger"), [
    "2a. Are you offering incentives (rent-free / fit-out) to secure tenants?   ☐ No   ☐ Yes — trend:  ☐ More  ☐ Same  ☐ Less",
])
insert_after(find("Attractiveness of this area"), [
    "4a. Has street-level safety / perception affected a leasing deal in the last 12 months?   ☐ Yes   ☐ No",
    "      If yes, briefly: ________________________________________________",
    "4b. If safety improved measurably, how much would it lift your confidence to invest / lease? (1–5):   ☐ 1  ☐ 2  ☐ 3  ☐ 4  ☐ 5",
])
insert_after(find("What would improve your confidence most"), [
    "8. Would you support landlords co-funding an ongoing safety presence?   ☐ Yes   ☐ No   ☐ Unsure",
    "9. A sentence we may quote: ________________________________________________",
])

# ════════════════════════════════════════════════════════════════════════════
# NEW INSTRUMENT 1 — Public / Pedestrian Intercept (appended)
# ════════════════════════════════════════════════════════════════════════════
doc.add_page_break()
heading("PUBLIC / PEDESTRIAN INTERCEPT SURVEY  (30 seconds)", size=14)
line("Added by ASG. A very short on-street survey of people in the precinct — workers, shoppers, "
     "visitors. This captures the public's perception of safety, which is the measure Auckland Council "
     "tracks (their baseline: 58% feel safe by day, 15% at night). Running this lets the pilot show "
     "movement against Council's own metric, day and night.", italic=True, size=9.5, color=NAVY)
line("Approach: “Hi — quick 30-second question for Heart of the City: how safe do you feel here right now?”",
     italic=True, size=9.5)
line("Date: ________   Time: ________   Location: ____________   Surveyor: ________   Wave: ☐ Baseline  ☐ Follow-up",
     bold=True)
for q in [
    "1. You’re here mainly to:   ☐ Work   ☐ Shop / dine   ☐ Pass through   ☐ Live here",
    "2. How safe do you feel here right now? (1–5):   ☐ 1  ☐ 2  ☐ 3  ☐ 4  ☐ 5",
    "3. How safe would you feel here at night? (1–5):   ☐ 1  ☐ 2  ☐ 3  ☐ 4  ☐ 5",
    "4. Compared with a few months ago, it feels:   ☐ Worse   ☐ About the same   ☐ Better",
    "5. Have you noticed the safety team?   ☐ No   ☐ Yes — do they make you feel safer?  ☐ Yes  ☐ Somewhat  ☐ No",
    "6. One word for how the area feels today: ____________________",
]:
    line(q)

# ════════════════════════════════════════════════════════════════════════════
# NEW INSTRUMENT 2 — Methodology & Sampling (appended)
# ════════════════════════════════════════════════════════════════════════════
heading("METHODOLOGY & SAMPLING  (for the accountability report)", size=14)
line("Added by ASG. How the data is collected so the July report stands up.", italic=True, size=9.5, color=NAVY)
for b, t in [
    ("Two waves:", "Baseline 2–15 June (while the uplift is fresh); Follow-up 14–24 July."),
    ("Targets per wave:", "≥40 business surveys, ≥10 landlord surveys, ≥100 public intercepts."),
    ("Coverage:", "Spread across Queen St, Wellesley St, Federal St and the documented hotspots; "
                  "mix of daytime and evening so day/night perceptions are both captured."),
    ("Matching:", "Use the Business / Property ID to pair each baseline response with its follow-up "
                  "— this proves the shift, not just an average."),
    ("Scoring:", "Report mean scores and % improvement; segment by location and by day/night; pair "
                 "headline numbers with verbatim quotes."),
    ("Capture:", "Enter responses same-day into the Perceptions Survey tab of "
                 "LCF_Data_Capture_Tracker.xlsx; the KPI dashboard computes baseline→follow-up uplift."),
]:
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(3)
    rb = p.add_run("•  " + b + " "); rb.bold = True; rb.font.size = Pt(10.5)
    rt = p.add_run(t); rt.font.size = Pt(10.5)

doc.save(OUT)
print("DOCX ->", OUT)
