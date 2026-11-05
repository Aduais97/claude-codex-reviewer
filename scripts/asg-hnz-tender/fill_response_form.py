#!/usr/bin/env python3
"""Fill HNZ Response Form V3 with ASG answers from the master markdown.

Preserves all human-entered values (profile, PoC, pre-condition, finances
rows 2-5, claims, Response Locations). Fills: financial status, insurance,
the 21 Part A answers, Assumptions & KPIs, referees scaffold, declaration,
dates, Proposed Contract option 2. Deletes instruction pages and all
RESPONDENT TIP boxes and purple instruction paragraphs. [Brackets] are
yellow-highlighted for the owner's final pass.

Usage: .venv/bin/python fill_response_form.py <master.md> <form.docx> <out.docx>
"""
import re, sys
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_COLOR_INDEX

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PURPLES = {'603F99', '7030A0', 'EC008C'}


# ---------- master markdown parsing ----------

def load_sections(md_path):
    txt = open(md_path, encoding='utf-8').read()
    secs = {}
    for m in re.finditer(r'^## ([A-Z]\d+|Assumptions|KPIs)[.\s]', txt, re.M):
        key = m.group(1)
        start = m.end()
        nxt = re.search(r'^#{1,2} ', txt[start:], re.M)
        end = start + nxt.start() if nxt else len(txt)
        # drop the rest of the heading line
        body = txt[start:end]
        body = body[body.find('\n') + 1:]
        secs[key] = body.strip()
    # financial status paragraph
    m = re.search(r'Current financial status: (.+?)\n', txt)
    secs['FINSTATUS'] = m.group(1).strip() if m else ''
    return secs


def clean_lines(body):
    """Strip internal NOTE lines; yield structured lines."""
    out = []
    for ln in body.split('\n'):
        if ln.strip().startswith('NOTE:'):
            continue
        out.append(ln.rstrip())
    return out


# ---------- docx writing ----------

def add_runs(p, text, bold_all=False):
    bold = False
    for tok in text.split('**'):
        if tok:
            for seg in re.split(r'(\[[^\]]+\])', tok):
                if not seg:
                    continue
                run = p.add_run(seg)
                run.font.size = Pt(10)
                if seg.startswith('['):
                    run.font.highlight_color = WD_COLOR_INDEX.YELLOW
                    run.bold = True
                else:
                    run.bold = bold or bold_all
        bold = not bold


def fill_cell(cell, body):
    """Replace cell content with rendered markdown body."""
    # clear existing paragraphs except first
    for p in list(cell.paragraphs[1:]):
        p._element.getparent().remove(p._element)
    first = cell.paragraphs[0]
    for r in list(first.runs):
        r._element.getparent().remove(r._element)

    lines = clean_lines(body)
    i, used_first = 0, False

    def new_para():
        nonlocal used_first
        if not used_first:
            used_first = True
            return first
        return cell.add_paragraph()

    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        if ln.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells_ = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-{2,}:?', c) for c in cells_):
                    rows.append(cells_)
                i += 1
            if rows:
                n = max(len(r) for r in rows)
                t = cell.add_table(rows=len(rows), cols=n)
                t.style = 'Table Grid'
                for ri, row in enumerate(rows):
                    for ci in range(n):
                        tc = t.cell(ri, ci)
                        for r in list(tc.paragraphs[0].runs):
                            r._element.getparent().remove(r._element)
                        add_runs(tc.paragraphs[0],
                                 row[ci] if ci < len(row) else '',
                                 bold_all=(ri == 0))
                cell.add_paragraph()
            continue
        p = new_para()
        p.paragraph_format.space_after = Pt(6)
        if ln.startswith('### '):
            add_runs(p, ln[4:], bold_all=True)
        elif re.match(r'^\d+\.\s', ln):
            num, rest = ln.split('.', 1)
            p.paragraph_format.space_after = Pt(3)
            add_runs(p, f'{num}. {rest.strip()}')
        elif ln.startswith('- '):
            p.paragraph_format.space_after = Pt(3)
            add_runs(p, '• ' + ln[2:])
        else:
            add_runs(p, ln)
        i += 1


def set_cell_text(cell, text):
    for p in list(cell.paragraphs[1:]):
        p._element.getparent().remove(p._element)
    for r in list(cell.paragraphs[0].runs):
        r._element.getparent().remove(r._element)
    add_runs(cell.paragraphs[0], text)


def delete_el(el):
    el.getparent().remove(el)


def main(md_path, form_path, out_path):
    secs = load_sections(md_path)
    doc = Document(form_path)
    T = doc.tables

    # ----- Part A answers (table 11) -----
    amap = {2: 'C1', 4: 'C2', 6: 'C3', 8: 'C4', 10: 'C5', 12: 'C6', 14: 'C7',
            18: 'P1', 20: 'P2', 22: 'P3', 24: 'P4', 26: 'P5', 28: 'P6',
            31: 'H1', 33: 'H2', 35: 'H3', 37: 'H4', 39: 'H5',
            42: 'E1', 44: 'E2', 46: 'E3'}
    t11 = T[11]
    for ri, key in amap.items():
        fill_cell(t11.rows[ri].cells[0], secs[key])

    # ----- financial status (T5 R1 answer cell) -----
    set_cell_text(T[5].rows[1].cells[-1], secs['FINSTATUS'])

    # ----- insurance (T7) -----
    ins = {
        1: ('Policy #1:', 'Public liability  /  Policy #2: Professional indemnity'),
        2: ('Name of insurers:', '[INSURER NAME(S)]'),
        3: ('Type of insurance:', 'Policy 1: Public liability. Policy 2: Professional indemnity. Statutory liability cover is also held.'),
        4: ('$ amount of insurance cover:', 'Policy 1: [$ PL COVER]. Policy 2: [$ PI COVER]. Our broker has confirmed in writing our capacity to bind cover at the tier corresponding to the districts and FTE awarded under RFP section 5.3, effective at contract commencement [BROKER LETTER FILE NAME].'),
        5: ('Limitations:', '[PER POLICY SCHEDULES]'),
        6: ('History:', '[CLAIMS HISTORY LAST 3 YEARS - e.g. No claims]'),
    }
    for ri, (_, val) in ins.items():
        set_cell_text(T[7].rows[ri].cells[-1], val)

    # ----- referees (T17/T18) -----
    ref1 = {1: '[REFEREE 1 NAME]', 2: '[CITY CENTRE BUSINESS ASSOCIATION - confirm naming]',
            3: '24/7 precinct security patrol programme: public-facing patrols, de-escalation, welfare-first engagement, Police liaison, incident reporting',
            4: 'March 2024 to present', 5: '[ADDRESS]', 6: '[PHONE]', 7: '[EMAIL]',
            8: '[Contract owner / manager]'}
    ref2 = {1: '[REFEREE 2 NAME]', 2: '[SECOND CLIENT ORGANISATION]',
            3: '[Services provided - 24/7 guarding / events / property security]',
            4: '[DATES]', 5: '[ADDRESS]', 6: '[PHONE]', 7: '[EMAIL]', 8: '[ROLE]'}
    for ri, val in ref1.items():
        set_cell_text(T[17].rows[ri].cells[-1], val)
    for ri, val in ref2.items():
        set_cell_text(T[18].rows[ri].cells[-1], val)
    set_cell_text(T[19].rows[0].cells[-1], 'Yes')

    # ----- assumptions & KPIs (T14) -----
    fill_cell(T[14].rows[2].cells[0], secs['Assumptions'])
    fill_cell(T[14].rows[5].cells[0], secs['KPIs'])

    # ----- declaration (T21) -----
    for ri in range(2, 9):
        set_cell_text(T[21].rows[ri].cells[-1], 'Agree')
    set_cell_text(T[21].rows[9].cells[-1], 'Not applicable')

    # ----- paragraphs: date, cover, proposed contract, signature -----
    opt1_del = []
    for p in doc.paragraphs:
        t = p.text.strip()
        if t.startswith('Date of this Proposal'):
            for r in list(p.runs):
                delete_el(r._element)
            add_runs(p, 'Date of this Proposal: 5 November 2026')
        elif t.startswith('[insert your (Respondent'):
            for r in list(p.runs):
                delete_el(r._element)
            add_runs(p, 'Absolute Security Group Limited   [INSERT ASG LOGO]')
        elif t == 'Choose one and delete the other:' or t == 'OR':
            opt1_del.append(p)
        elif t.startswith('Having read and understood the Proposed Contract') and 'confirm that these terms and conditions are acceptable' in t:
            opt1_del.append(p)  # option 1 removed; option 2 kept
        elif t.startswith('Having read and understood the Proposed Contract') and 'suggestions in Attachment B' in t:
            # append register reference after option 2
            add_runs(p, '  The Contract Departure Register is attached as ASG_Contract_Departure_Register.docx. We also note, per RFP sections 5.2 and 5.3: our positions on the proposed KPIs are set out in the Assumptions and KPIs section above, and we ask that the insurance tier applying at commencement reflect the districts and FTE actually awarded, evidenced by the attached broker confirmation of capacity to bind the corresponding cover.')
        elif t.startswith('Full name:'):
            set_para(p, 'Full name: Ahmad Duais')
        elif t.startswith('Title/position:'):
            set_para(p, 'Title/position: Chief Executive')
        elif t.startswith('Name of organisation:') and 'Date' not in t:
            set_para(p, 'Name of organisation: Absolute Security Group Limited')
        elif t == 'Date:':
            set_para(p, 'Date: 5 November 2026')
    for p in opt1_del:
        delete_el(p._element)

    # ----- delete instruction pages: everything before the cover line -----
    body = doc.element.body
    stop_texts = ('Absolute Security Group Limited   [INSERT ASG LOGO]',)
    to_delete = []
    for child in body.iterchildren():
        if child.tag == W + 'p':
            texts = ''.join(child.itertext())
            if any(s in texts for s in stop_texts):
                break
            to_delete.append(child)
        elif child.tag == W + 'tbl':
            to_delete.append(child)
        else:
            continue
    for el in to_delete:
        delete_el(el)

    # ----- delete all remaining RESPONDENT TIP tables -----
    for tbl in list(doc.tables):
        if 'RESPONDENT TIP' in tbl.rows[0].cells[0].text or (
                len(tbl.rows) == 1 and 'RESPONDENT TIP' in ''.join(
                    c.text for c in tbl.rows[0].cells)):
            delete_el(tbl._element)

    # ----- delete purple instruction paragraphs anywhere -----
    for p in list(doc.paragraphs):
        runs = p.runs
        if not runs or not p.text.strip():
            continue
        purple = [r for r in runs if r.font.color and r.font.color.rgb is not None
                  and str(r.font.color.rgb) in PURPLES]
        if purple and len(''.join(r.text for r in purple)) >= 0.7 * len(p.text):
            delete_el(p._element)

    doc.save(out_path)
    print('Saved:', out_path)


def set_para(p, text):
    for r in list(p.runs):
        r._element.getparent().remove(r._element)
    add_runs(p, text)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
