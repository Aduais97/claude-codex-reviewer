#!/usr/bin/env python3
"""HNZ RFP 0018709 — markdown -> submission-draft DOCX.

Markup: # H1, ## H2, ### H3; - bullets; 1. numbered; | tables |;
**bold**; [PLACEHOLDER] -> yellow highlight; lines starting 'NOTE:' ->
red italic internal drafting notes; '>' quote -> indented italic.

Usage: .venv/bin/python build_submission_docx.py <content.md> <out.docx>
"""
import re, sys
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_COLOR_INDEX

NAVY = RGBColor(0x1B, 0x2A, 0x4A)
RED = RGBColor(0xC0, 0x39, 0x2B)
GREY = RGBColor(0x4A, 0x4A, 0x5A)


def add_runs(p, text, size=10.5, italic=False, color=None):
    # split out [placeholders] and **bold**
    for seg in re.split(r"(\[[^\]]+\])", text):
        if not seg:
            continue
        if seg.startswith("["):
            run = p.add_run(seg)
            run.font.size = Pt(size)
            run.font.highlight_color = WD_COLOR_INDEX.YELLOW
            run.bold = True
            continue
        for part in re.split(r"(\*\*[^*]+\*\*)", seg):
            if not part:
                continue
            bold = part.startswith("**")
            run = p.add_run(part.strip("*") if bold else part)
            run.font.size = Pt(size)
            run.bold = bold
            run.italic = italic
            if color is not None:
                run.font.color.rgb = color


def build(md_path, out_path):
    doc = Document()
    # tighten default style
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10.5)

    lines = open(md_path, encoding="utf-8").read().split("\n")
    i = 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            i += 1
            continue
        if ln.startswith("### "):
            h = doc.add_heading(ln[4:], level=3)
            for r in h.runs: r.font.color.rgb = NAVY
        elif ln.startswith("## "):
            h = doc.add_heading(ln[3:], level=2)
            for r in h.runs: r.font.color.rgb = NAVY
        elif ln.startswith("# "):
            h = doc.add_heading(ln[2:], level=1)
            for r in h.runs: r.font.color.rgb = NAVY
        elif ln.startswith("NOTE:"):
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(8)
            run = p.add_run("DRAFTING NOTE (delete before submission): " + ln[5:].strip())
            run.italic = True
            run.font.size = Pt(9)
            run.font.color.rgb = RED
        elif ln.startswith("> "):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.7)
            p.paragraph_format.space_after = Pt(4)
            add_runs(p, ln[2:], size=9.5, italic=True, color=GREY)
        elif ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            if rows:
                n = max(len(r) for r in rows)
                t = doc.add_table(rows=len(rows), cols=n)
                t.style = "Table Grid"
                for ri, row in enumerate(rows):
                    for ci in range(n):
                        cell = t.cell(ri, ci)
                        cell.paragraphs[0].text = ""
                        add_runs(cell.paragraphs[0],
                                 row[ci] if ci < len(row) else "",
                                 size=9.5)
                        if ri == 0:
                            for r in cell.paragraphs[0].runs:
                                r.bold = True
                doc.add_paragraph()
            continue
        elif re.match(r"^\d+\.\s", ln):
            num, rest = ln.split(".", 1)
            p = doc.add_paragraph(style="List Number")
            p.paragraph_format.space_after = Pt(3)
            add_runs(p, rest.strip())
        elif ln.startswith("- "):
            p = doc.add_paragraph(style="List Bullet")
            p.paragraph_format.space_after = Pt(3)
            add_runs(p, ln[2:])
        else:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(6)
            add_runs(p, ln)
        i += 1

    doc.save(out_path)
    print("Written:", out_path)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    build(sys.argv[1], sys.argv[2])
