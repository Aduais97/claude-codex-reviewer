#!/usr/bin/env python3
"""Woolworths Primary Connect DC Security tender (Ref 523941) — Compliance Matrix (xlsx).

Sheets: Key Dates, Site Sizing, SOW Requirements, RFx Requirements,
Findings (verified), Clarifications (due 12 Nov), Answer Open Items.
Reads the ETR workflow result JSON. Navy/gold house style.

Usage: .venv/bin/python build_compliance_matrix.py <etr_result.json> <out.xlsx>
"""
import json
import re
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

NAVY = "1B2A4A"
GOLD = "D4A843"
ALT = "F2F4F8"
LIGHT = "E8EDF5"
BORDER = Side(style="thin", color="D0D5DD")

SEV_FILL = {"CRITICAL": "F8D7DA", "HIGH": "FDE9D9", "MEDIUM": "FFF6DD", "LOW": "EAF3EA"}


def sheet(wb, title, headers, rows, widths, status_col=None, sev_col=None):
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
        if sev_col:
            sev = str(row[sev_col - 1]).upper()
            if sev in SEV_FILL:
                ws.cell(r, sev_col).fill = PatternFill("solid", fgColor=SEV_FILL[sev])
                ws.cell(r, sev_col).font = Font(size=9.5, bold=True)
    for c, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(c)].width = w
    ws.row_dimensions[1].height = 28
    if status_col:
        for r in range(2, len(rows) + 2):
            ws.cell(r, status_col).fill = PatternFill("solid", fgColor=LIGHT)
    return ws


KEY_DATES = [
    ["Thu 12 Nov 2026", "Key clarification questions due to Sandhya Reshmi (portal conversation tool)", "Lodge questions from the Clarifications sheet", ""],
    ["Next ~2 weeks", "DC site visits for ARDC and AFDC with the operational team", "Accept immediately; attend with ops lead; collect site intel for answers", ""],
    ["Coming days", "MSA issued for review", "Review; departures via tracked changes with comments", ""],
    ["Wed 25 Nov 2026, 4:00 PM NZT", "PROPOSAL DUE (portal)", "Upload answers, pricing workbook, ethical audit, policies, insurance, licences", ""],
    ["1 Mar 2027", "Contract effective date (pricing effective date)", "Mobilisation must complete: recruit, licence, 40-hr site inductions", ""],
    ["2 Mar 2027", "'Need by' date stated in RFx", "", ""],
]

# Computed from Document 2 'Pricing Proposal - Profile' roster rows.
SIZING = [
    ["ARDC", "Auckland Regional DC, 80 Favona Rd, Mangere", "4 on duty (1 sup + 1 std days; 2 std nights), 24/7", 336, 17472],
    ["ANDC", "Auckland National DC, 60 Kerrs Rd, Wiri", "Days: 1 std 7d + 1 sup 5d + 1 std w/e; nights 2 std, 24/7", 336, 17472],
    ["AFDC", "Auckland Fresh DC, 13 Puaki Dr, Wiri", "1 sup 8h Mon-Fri + 2 std days + 2 std nights, 24/7", 376, 19552],
    ["CRDC", "Christchurch Regional DC, 146 Shands Rd, Hornby", "4 on duty (1 sup + 1 std days; 2 std nights), 24/7", 336, 17472],
    ["CFDC", "Christchurch Fresh DC, 60 Hynds Dr, Hornby", "4 on duty (1 sup + 1 std days; 2 std nights), 24/7", 336, 17472],
    ["PRDC", "Palmerston North DC, 1-35 Alderson Dr, Milson", "4 on duty (1 sup + 1 std days; 2 std nights), 24/7", 336, 17472],
]


def main(result_path, out):
    data = json.load(open(result_path))

    wb = Workbook()
    wb.remove(wb.active)

    sheet(wb, "Key Dates", ["Date", "Event", "ASG action", "Status"], KEY_DATES, [24, 54, 50, 12], status_col=4)

    ws = sheet(wb, "Site Sizing", ["Site", "Address", "Roster pattern (client profile)", "Hours/week", "Hours/year"],
               SIZING, [8, 40, 52, 12, 12])
    tr = len(SIZING) + 2
    ws.cell(tr, 1, "TOTAL").font = Font(bold=True)
    ws.cell(tr, 4, sum(r[3] for r in SIZING)).font = Font(bold=True)
    ws.cell(tr, 5, sum(r[4] for r in SIZING)).font = Font(bold=True)
    ws.cell(tr + 1, 1, "Auckland-only (ARDC+ANDC+AFDC): 1,048 hrs/wk / 54,496 hrs/yr. "
                       "Hours from the client's own roster profile in Document 2; indicative only.").font = Font(italic=True, size=9)

    for key, title in (("sow", "SOW Requirements"), ("rfx", "RFx Requirements")):
        reqs = data["matrix"].get(key, [])
        rows = [[r["id"], r["category"], r["requirement"], r["asg_status"], r["evidence_or_action"], ""] for r in reqs]
        sheet(wb, title, ["ID", "Category", "Requirement", "ASG status", "Evidence / action", "Done"],
              rows, [9, 16, 62, 11, 48, 8], status_col=6)

    # Findings with verification verdicts merged by title
    verdicts = {v["title"]: v for v in data.get("verification", [])}
    frows = []
    for lens in data.get("lenses", []):
        for f in lens["findings"]:
            v = verdicts.get(f["title"], {})
            frows.append([lens["lens"], f["severity"], f["title"], f["detail"], f["action"],
                          v.get("verdict", ""), v.get("note", "")])
    sev_rank = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    frows.sort(key=lambda r: sev_rank.get(r[1], 9))
    frows = [r for r in frows if r[5] != "REFUTED"] + [r for r in frows if r[5] == "REFUTED"]
    sheet(wb, "Findings", ["Lens", "Severity", "Finding", "Detail", "Action", "Verify", "Verifier note"],
          frows, [18, 11, 30, 56, 44, 12, 30], sev_col=2)

    crows = [[q["priority"], q["question"], q["rationale"], ""] for q in data["clarifications"]["questions"]]
    crows.sort(key=lambda r: {"HIGH": 0, "MEDIUM": 1, "LOW": 2}.get(r[0], 9))
    sheet(wb, "Clarifications — by 12 Nov", ["Priority", "Question (portal-ready)", "Rationale", "Lodged?"],
          crows, [10, 72, 44, 10], status_col=4)

    orows = []
    for sec in data.get("sections", []):
        for a in sec["answers"]:
            for m in re.findall(r"\[(?:AHMAD|VERIFY)[^\]]*\]", a["answer"]):
                orows.append([sec["section"], a["q"], m, ""])
    sheet(wb, "Answer Open Items", ["Section", "Q", "Bracketed item needing Ahmad / verification", "Done"],
          orows, [20, 8, 92, 8], status_col=4)

    wb.save(out)
    print(f"Written: {out} ({len(frows)} findings, {len(orows)} open answer items)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
