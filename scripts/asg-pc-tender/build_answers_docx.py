#!/usr/bin/env python3
"""Woolworths Primary Connect DC Security tender (Ref 523941) — Draft Answers DOCX.

Reads the ETR workflow result JSON (sections[].answers[]) and renders a
portal-ready draft answer document. [AHMAD: ...] and [VERIFY: ...] brackets
are rendered in red bold so nothing slips through to the portal unresolved.

Usage: .venv/bin/python build_answers_docx.py <etr_result.json> <out.docx>
"""
import json
import re
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor

NAVY = RGBColor(0x1B, 0x2A, 0x4A)
DBLUE = RGBColor(0x2C, 0x3E, 0x6B)
RED = RGBColor(0xB4, 0x23, 0x18)
GREY = RGBColor(0x4A, 0x4A, 0x5A)

SECTION_TITLES = {
    "S1-Governance": "Section 1 — Governance, Licensing and Compliance",
    "S2-DCOperations": "Section 2 — Distribution Centre Operations",
    "S3-Training": "Section 3 — Training, Capability and Onboarding",
    "S4-QualitySLA": "Section 4 — Quality Management and SLA Assurance",
    "S5-Workforce": "Section 5 — Workforce Management and Guard Welfare",
    "S6-Ethical": "Section 6 — Ethical Compliance Audit",
    "S7-Technology": "Section 7 — Technology, Reporting and Systems",
    "S8-Statutory": "Section 8 — Statutory Compliance and Operations",
    "S9-Experience": "Section 9 — Experience and Reference",
    "S10-PriorToSubmission": "Section 10 — Prior to Submission (Uploads)",
}

QUESTION_TEXT = {}  # filled from main_extract if provided


def add_runs(par, text):
    """Write text, rendering [AHMAD: ...] / [VERIFY: ...] brackets red-bold."""
    pos = 0
    for m in re.finditer(r"\[(?:AHMAD|VERIFY)[^\]]*\]", text):
        if m.start() > pos:
            par.add_run(text[pos:m.start()])
        r = par.add_run(m.group(0))
        r.bold = True
        r.font.color.rgb = RED
        pos = m.end()
    if pos < len(text):
        par.add_run(text[pos:])


def main(result_path, out_path):
    data = json.load(open(result_path))
    sections = data["sections"]

    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10.5)

    # Title block
    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run("NZ PRIMARY CONNECT SECURITY SERVICES")
    r.bold = True
    r.font.size = Pt(20)
    r.font.color.rgb = NAVY
    s = doc.add_paragraph()
    s.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = s.add_run("Woolworths NZ Ref 523941 — ASG Draft Portal Answers v1")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = DBLUE
    m = doc.add_paragraph()
    m.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = m.add_run(
        "DRAFT — internal working document. Red bracketed items require Ahmad's "
        "input/verification before any text is pasted into the portal. "
        "Submission due Wednesday 25 November 2026, 4:00 PM NZT."
    )
    r.italic = True
    r.font.size = Pt(9)
    r.font.color.rgb = GREY

    bracket_total = 0
    for sec in sections:
        key = sec["section"]
        h = doc.add_heading(SECTION_TITLES.get(key, key), level=1)
        for run in h.runs:
            run.font.color.rgb = NAVY
        for a in sec["answers"]:
            q = doc.add_paragraph()
            r = q.add_run(f"Question {a['q']}")
            r.bold = True
            r.font.size = Pt(11)
            r.font.color.rgb = DBLUE
            qt = QUESTION_TEXT.get(a["q"])
            if qt:
                r = q.add_run(f" — {qt}")
                r.italic = True
                r.font.size = Pt(9.5)
                r.font.color.rgb = GREY
            for para in a["answer"].split("\n\n"):
                para = para.strip()
                if not para:
                    continue
                lines = para.split("\n")
                # bullet blocks
                if all(l.strip().startswith(("-", "•")) for l in lines):
                    for l in lines:
                        p = doc.add_paragraph(style="List Bullet")
                        add_runs(p, l.strip().lstrip("-•").strip())
                else:
                    p = doc.add_paragraph()
                    add_runs(p, para.replace("\n", " "))
            bracket_total += len(re.findall(r"\[(?:AHMAD|VERIFY)", a["answer"]))

    doc.add_page_break()
    h = doc.add_heading("Open items register", level=1)
    for run in h.runs:
        run.font.color.rgb = NAVY
    doc.add_paragraph(
        f"{bracket_total} bracketed [AHMAD]/[VERIFY] items remain across the answer set. "
        "Search the document for '[' to clear each one before upload."
    )

    doc.save(out_path)
    n_answers = sum(len(s["answers"]) for s in sections)
    print(f"Written: {out_path} ({len(sections)} sections, {n_answers} answers, {bracket_total} open brackets)")


def load_question_text(main_extract):
    txt = open(main_extract).read()
    for m in re.finditer(r"^(\d{1,2}\.\d{1,2})\s+(.+)$", txt, re.M):
        QUESTION_TEXT.setdefault(m.group(1), m.group(2).strip())


if __name__ == "__main__":
    if len(sys.argv) >= 4:
        load_question_text(sys.argv[3])
    main(sys.argv[1], sys.argv[2])
