#!/usr/bin/env python3
"""Woolworths Primary Connect DC Security tender (Ref 523941) — Clarification
Questions DOCX, portal-ready, due Thursday 12 November 2026.

Usage: .venv/bin/python build_clarifications_docx.py <etr_result.json> <out.docx>
"""
import json
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor

NAVY = RGBColor(0x1B, 0x2A, 0x4A)
DBLUE = RGBColor(0x2C, 0x3E, 0x6B)
GREY = RGBColor(0x4A, 0x4A, 0x5A)


def main(result_path, out_path):
    data = json.load(open(result_path))
    qs = data["clarifications"]["questions"]
    qs.sort(key=lambda q: {"HIGH": 0, "MEDIUM": 1, "LOW": 2}.get(q["priority"], 9))

    doc = Document()
    doc.styles["Normal"].font.name = "Calibri"
    doc.styles["Normal"].font.size = Pt(10.5)

    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run("CLARIFICATION QUESTIONS — NZ PRIMARY CONNECT SECURITY SERVICES (REF 523941)")
    r.bold = True
    r.font.size = Pt(15)
    r.font.color.rgb = NAVY
    s = doc.add_paragraph()
    s.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = s.add_run("For lodgement via the portal conversation tool (Sandhya Reshmi) by Thursday 12 November 2026. "
                  "Internal priority tags are for Ahmad only; strip before sending.")
    r.italic = True
    r.font.size = Pt(9)
    r.font.color.rgb = GREY

    for i, q in enumerate(qs, 1):
        h = doc.add_paragraph()
        r = h.add_run(f"Q{i}  [{q['priority']}]")
        r.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = DBLUE
        doc.add_paragraph(q["question"])
        w = doc.add_paragraph()
        r = w.add_run(f"Why we are asking (internal, do not send): {q['rationale']}")
        r.italic = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = GREY

    doc.save(out_path)
    print(f"Written: {out_path} ({len(qs)} questions)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
