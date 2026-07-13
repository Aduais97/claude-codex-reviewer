#!/usr/bin/env python3
"""v3 — built off the FULL Xero FY26 P&L (not just the COGS image). Adds the THIRD accrual
credit that was previously invisible: Wages - Holiday Pay Accrual (OpEx) FY26 -$59,959 /
FY25 -$58,080 — a second provision release flattering EBITDA. Confirms all add-backs to the
dollar from the statement. Corrected FY26 normalised EBITDA = ~$371K (incl KiwiSaver) /
~$436K (ex-KiwiSaver). GP unchanged ~20.0% (the new strip is below GP). Idempotent over v2."""
import openpyxl
from copy import copy
from openpyxl.utils.cell import coordinate_to_tuple

SRC = "/Users/ahmadduais/Desktop/Acquisitions/1st-Call-Recruitment/1CR_Acquisition_Model.xlsx"
MIRROR = "/Users/ahmadduais/Desktop/Acquisitions/1st-Call-Recruitment/FINAL Acquisition Pack/1CR_Acquisition_Model.xlsx"
wb = openpyxl.load_workbook(SRC)

def sset(ws, coord, val):
    tr, tc = coordinate_to_tuple(coord)
    for mr in list(ws.merged_cells.ranges):
        if mr.min_row <= tr <= mr.max_row and mr.min_col <= tc <= mr.max_col:
            ws.unmerge_cells(str(mr)); break
    ws[coord] = val

REV26, REV25, REV27 = 12640040, 17890076, 12100000
ws = wb["Normalisation & FY25"]

# v2 layout: 16 holiday-COGS, 17 temping, 18 KiwiSaver, 19 EBITDA, 20 margin, 23 hdr, 24-25 bullets...
# Insert one strip row at 18 (OpEx holiday) -> KiwiSaver 19, EBITDA 20, margin 21, bullets shift +1
ws.insert_rows(18, 1)
for c in range(1, 7):
    ws.cell(18, c)._style = copy(ws.cell(17, c)._style)
ws["B18"] = "− Wages Holiday Pay Accrual release (OpEx provision release on salaried staff)"
ws["C18"], ws["D18"] = -58080, -59959
ws["F18"] = "Second provision release (perm/admin staff) — non-cash credit cutting OpEx; FY26 -$59,959 / FY25 -$58,080"

# IT add-back to the exact GL figure less ~$30k maintainable
ws["D10"] = 86614
ws["F10"] = "GL Wages-IT $116,614 (eliminated dev); keep ~$30K forward IT → add ~$86.6K"

def col_sum(letter):
    return sum((ws[f"{letter}{r}"].value or 0) for r in range(8, 20))  # 8..19 inclusive
fy25, fy26 = col_sum("C"), col_sum("D")
fy26_exks = fy26 + 65000
ws["C20"], ws["D20"] = fy25, fy26          # EBITDA total now row 20
ws["E20"] = 380000                          # FY27 flat-declining on the lower basis
ws["F20"] = f"FY26 ~${fy26/1000:.0f}K (~${fy26_exks/1000:.0f}K ex-KiwiSaver) — three accrual releases stripped. NOT $783K."
ws["C21"] = round(fy25/REV25, 4); ws["D21"] = round(fy26/REV26, 4); ws["E21"] = round(380000/REV27, 4)

sset(ws, "C24", f"• FY25 normalised EBITDA ~${fy25/1e6:.2f}M at $17.9M revenue = earnings power AT SCALE, NOT the basis. Revenue has since fallen 29%.")
sset(ws, "B25", f"• FY26 buyer-normalised EBITDA ~${fy26/1000:.0f}K (≈${fy26_exks/1000:.0f}K ex-KiwiSaver). Built straight off the full Xero P&L: add-backs confirmed to the dollar (owner $385K, IT $116.6K, interest $28.7K, depr $11.8K, FBT $42.98K, rent $369.2K, other income $72.2K). Three non-cash accrual releases stripped: holiday-pay COGS -$154.9K, temping-pays -$40.3K, holiday-pay OpEx -$60.0K. GP ~20.0%. The old $783K embedded all three credits + over-stated add-backs.")
sset(ws, "B26", "• FY27 modelled FLAT-to-DECLINING ~$380K. FY26 revenue -29.3% YoY; trailing ~$12.1M ~4% below FY26; no pipeline. Underwrite the declining FY26 base, not a recovery.")

# ---------- Mgmt Accounts Reconciliation ----------
ws = wb["Mgmt Accounts Reconciliation"]
ws["C11"], ws["D11"], ws["E11"] = "~$371K (full strip, FY26 basis)", "~$370–440K", "⚠ CORRECTED DOWN"
ws["F11"] = "Off the full Xero P&L: THREE accrual releases stripped (holiday COGS -$154.9K, temping -$40.3K, holiday OpEx -$60.0K) + corrected IT/rent + KiwiSaver = ~$371K (~$436K ex-KiwiSaver), NOT $783K."
ws["F6"] = "Reported GP flattered by accrual credits in COGS (holiday -$154.9K, temping -$40.3K). A THIRD release sits in OpEx (Wages-Holiday Pay -$60.0K), below GP. Maintainable GP ~20.0%, EBITDA ~$371-436K."
ws["B14"] = ("Net: built off the full Xero FY26 P&L — add-backs confirmed to the dollar; THREE non-cash accrual releases flatter earnings (holiday-pay COGS -$154.9K, temping-pays -$40.3K, holiday-pay OpEx -$60.0K). Maintainable GP ~20.0%; buyer-normalised FY26 EBITDA ~$371K (~$436K ex-KiwiSaver), NOT $783K. The '~$148K interest upside' is a phantom — real interest $28,655.")

# ---------- Group Consolidated ----------
ws = wb["Group Consolidated"]
ws["F9"], ws["G9"] = fy26, round(fy26/REV26, 4)        # GP cells already at 20.05% from v2
ws["F10"] = 1436680 + fy26
ws["G10"] = round((1436680 + fy26)/20191220, 4)
ws["B11"] = f"1st Call at FY26 buyer-normalised ~${fy26/1000:.0f}K (full P&L, three accrual releases stripped, GP ~20.0%, declining revenue)."
ws["F18"], ws["G18"] = 380000, round(380000/REV27, 4)
ws["F19"] = 1609082 + 380000
ws["G19"] = round((1609082 + 380000)/20557322, 4)
ws["C24"] = f"$1.44M → ${(1436680+fy26)/1e6:.2f}M"
ws["F24"] = f"+{round(fy26/1436680*100)}%"
ws["C26"] = f"19.0% → {round((1436680+fy26)/20191220*100,1)}%"

# ---------- Summary ----------
ws = wb["Summary"]
ws["C5"] = "~$600K target (open $500K · walk-away $700K)"
ws["C6"] = "Offered $1.1M (REJECTED); vendor seeks $1.6M (≈4.0x corrected EBITDA — not supportable)"
ws["C12"], ws["D12"] = fy26, 380000
ws["B12"] = "Normalised EBITDA (FY26 basis, full P&L, 3 accrual strips)"
ws["C13"], ws["D13"] = fy26_exks, 440000
ws["C14"], ws["D14"] = round(fy26/REV26, 4), round(380000/REV27, 4)
ws["B16"] = f"RETURNS (corrected EBITDA ~${fy26/1000:.0f}K)"
ws["C17"] = f"{1100000/fy26:.2f}x @ $1.1M · {600000/fy26:.2f}x @ $600K target · {1600000/fy26:.2f}x @ his $1.6M"
ws["C18"] = "at his $1.6M, after-tax payback >6yrs — uninvestable"
ws["C19"] = fy25

wb.save(SRC); wb.save(MIRROR)
print(f"FY25={fy25:,.0f}  FY26={fy26:,.0f} (ex-KiwiSaver {fy26_exks:,.0f})  FY27=380,000")
print(f"Multiple: {1100000/fy26:.2f}x @$1.1M | {600000/fy26:.2f}x @$600K | {1600000/fy26:.2f}x @$1.6M")
