#!/usr/bin/env python3
"""Pre-fill the Woolworths Ethical Sourcing Self Assessment for the Primary Connect
DC Security tender (Ref 523941). Marks every numbered clause Compliant (X),
fills supplier identity fields, leaves Date blank for Ahmad to sign on review.
"""
import re
import openpyxl

SRC = "/Users/ahmadduais/Downloads/NZ_Primary_Connect_Security_Services/Attachments/Woolworths Ethical Self Audit.xlsx"
OUT = ("/Users/ahmadduais/Desktop/ASG/Tenders/NZ Primary Connect Security Services 523941/"
       "ASG_Woolworths_Ethical_Self_Audit_COMPLETED_DRAFT.xlsx")

wb = openpyxl.load_workbook(SRC)
ws = wb["Sheet1"]

ws["C1"] = None  # Date — Ahmad signs on review
ws["C2"] = "ASG Limited (Absolute Security Group)"
ws["C3"] = "Ahmad Duais, Chief Executive"
ws["C4"] = "Level 7, 220 Queen Street, Auckland CBD 1010"

clause = re.compile(r"^\d+\.\d+$")  # e.g. 1.1, 2.3 — numbered clauses only, not section headers
marked = 0
for row in ws.iter_rows(min_row=8):
    a = row[0].value
    if a is None:
        continue
    text = str(a).strip()
    # openpyxl may give floats like 1.1 for numeric cells
    if isinstance(a, float):
        text = f"{a:.1f}"
    if clause.match(text) and not text.endswith(".0"):  # X.0 rows are section headers
        ws.cell(row=row[0].row, column=3, value="X")
        marked += 1

wb.save(OUT)
print(f"Marked {marked} clauses compliant -> {OUT}")
