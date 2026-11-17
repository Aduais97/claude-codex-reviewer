#!/usr/bin/env python3
"""Render the reply-to-Edward email (survey recommendations inline) as an editable .docx."""
import os
from docx import Document
from docx.shared import Pt, RGBColor

OUT = os.path.expanduser("~/Desktop/ASG/HOTC/2026/Reply to Edward - LCF Survey.docx")
NAVY = RGBColor(0x1B, 0x2A, 0x4A)

doc = Document()
doc.styles['Normal'].font.name = 'Calibri'
doc.styles['Normal'].font.size = Pt(11)

def meta(label, value):
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(2)
    r = p.add_run(label + "  "); r.bold = True; r.font.size = Pt(10.5); r.font.color.rgb = NAVY
    r2 = p.add_run(value); r2.font.size = Pt(10.5)

def para(text="", after=8, bold=False):
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(after)
    if text:
        r = p.add_run(text); r.bold = bold
    return p

def lead(label, text):
    """Bold lead-in sentence followed by normal text, same paragraph."""
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(8)
    r = p.add_run(label); r.bold = True
    p.add_run(text)

def bullet(text):
    p = doc.add_paragraph(); p.paragraph_format.left_indent = Pt(18); p.paragraph_format.space_after = Pt(3)
    p.add_run("•  " + text)

meta("To:", "Edward Caughey <edward.caughey@hotcity.co.nz>")
meta("Subject:", "Re: Fw: LCF activities")
doc.add_paragraph()

para("Hi Edward,")
para("Good first day — the team's been out across the precinct and it's gone well. I'll keep you "
     "posted through the week.")
para("The survey's great. A few questions I'd suggest adding, and one structural thing that I think "
     "makes the whole exercise much stronger:")

lead("The key one — run it in two waves.  ",
     "If we add a short header to each form (business name, date, surveyor, and a “Baseline / "
     "Follow-up” tickbox) we can capture each business now and again in July and match them up. That "
     "lets us show the actual shift per business, rather than just an average — which is exactly what "
     "your accountability report needs.")

para("Suggested extra questions for the business survey:", bold=True, after=4)
for b in [
    "Split the safety score into day and night/evening (1–5) — this lines up with Council's own "
    "perceptions tracking (their baseline is 58% feel safe by day, 15% at night), so our data speaks "
    "to their numbers.",
    "How safe do staff feel, particularly opening and closing?",
    "Has the safety team specifically changed how safe you feel? (Significant / Some / None) — the "
    "attribution that ties the presence to the result.",
    "How quickly do you think help would arrive if you called? (1–5)",
    "When something happens, do you report it — and to whom?",
    "Would you support a continued or expanded safety presence? (useful for the post-pilot funding case)",
    "One sentence we can quote on what the team's meant for you (captures the “positive stories” the "
    "funding asks for), plus whether you're happy for us to check back in July.",
]:
    bullet(b)

para("", after=4)
lead("One bigger idea:  ",
     "alongside the business survey, we could run a 30-second public intercept — stopping a sample of "
     "people on the street: “how safe do you feel here right now, day and night?” That's the "
     "public-perception measure Council actually tracks, so it would let us demonstrate movement "
     "against their own metric. The team can run these during patrols.")

para("I've also put all of this into a marked-up version of your doc (additions tagged so they're "
     "easy to keep or cut) — attached if useful, but happy to leave the survey as yours and just feed "
     "in whichever of the above you like.")

para("Plan would be a baseline wave over the next fortnight while the team's visibly out there, then "
     "a follow-up mid-July for your report. I'll also have the service agreement and first invoice "
     "across to you shortly.")

para("Cheers,", after=2)
para("Ahmad")

doc.save(OUT)
print("DOCX ->", OUT)
