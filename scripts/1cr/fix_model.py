#!/usr/bin/env python3
"""Correct the 1st Call (JCR 2006) acquisition model to the de-inverted, adversarially-
verified numbers. Strips the holiday-pay accrual RELEASE (it flatters GP, not drags it),
fixes the over-stated IT & rent add-backs, books the KiwiSaver under-accrual and the
temping-pays timing reversal, deletes the phantom ~$148K interest note and the +5%
recovery story. Corrected FY26 normalised EBITDA ~= $525,748 (NOT the model's $783K, and
NOT the workflow's $498K which double-counted the existing -$30K GP buffer)."""
import openpyxl
from copy import copy

SRC = "/Users/ahmadduais/Desktop/Acquisitions/1st-Call-Recruitment/1CR_Acquisition_Model.xlsx"
MIRROR = "/Users/ahmadduais/Desktop/Acquisitions/1st-Call-Recruitment/FINAL Acquisition Pack/1CR_Acquisition_Model.xlsx"

wb = openpyxl.load_workbook(SRC)

def sset(ws, coord, val):
    """Set a cell value even if it sits inside a merged range (unmerge first)."""
    from openpyxl.utils.cell import coordinate_to_tuple
    tr, tc = coordinate_to_tuple(coord)
    for mr in list(ws.merged_cells.ranges):
        if mr.min_row <= tr <= mr.max_row and mr.min_col <= tc <= mr.max_col:
            ws.unmerge_cells(str(mr))
            break
    ws[coord] = val

# ---------- 1) Normalisation & FY25 bridge (THE source of truth) ----------
ws = wb["Normalisation & FY25"]

# Revenue / GP / GP% re-base (C=FY25, D=FY26, E=FY27)
ws["E5"] = 12100000                                   # FY27 revenue: flat, no +5%
ws["F5"] = "FY25 KPMG · FY26 KPMG · FY27 FLAT (no recovery)"
ws["C6"], ws["D6"], ws["E6"] = 3639017, 2574776, 2468400      # GP$ at maintainable %
ws["F6"] = "~20.4% maintainable (reported 21.6% overstated by non-cash provision releases)"
ws["C7"], ws["D7"], ws["E7"] = 0.2034, 0.2037, 0.204          # GP%
ws["F7"] = "maintainable ~20.4% — headline 21.6% FLATTERED by holiday-pay accrual RELEASES (credit in COGS: FY26 -$154,914, FY25 -$268,156), not real margin"

# Over-stated add-backs
ws["D10"] = 86000                                     # IT/SaaS: GL Wages-IT $116,614, keep ~$30K maintainable
ws["F10"] = "FY25 2 staff · FY26 GL $116,614, ~$30K forward IT maintainable → add ~$86K"
ws["D11"] = 75000                                     # Rent: add back only non-continuing net of replacement
ws["F11"] = "Manukau related-party $110K terminates → ~$50K market replacement; Fiji KEPT. Net non-continuing ~$75K (not $165K)"

# Interest: delete the phantom ~$148K note (value unchanged)
ws["F13"] = "Xero year-end interest $28,655; total finance incl charges $45,558 (0.4% of rev). New CARL interest ~$114K/yr is a NewCo cost BELOW EBITDA."

# GP re-base replaces the mis-purposed prudence buffer (counted ONCE)
ws["B16"] = "− GP re-base to maintainable 20.4% (strip holiday-pay accrual release)"
ws["C16"], ws["D16"] = -269620, -79832
ws["F16"] = "Holidays Act s28 historic exposure handled SEPARATELY via indemnity/holdback, NOT in EBITDA"

# Insert two explicit correction lines before the EBITDA total (row 17)
ws.insert_rows(17, 2)
style_src = ws[16]  # copy look of a bridge data row
for newr in (17, 18):
    for c in range(1, 7):
        ws.cell(newr, c)._style = copy(ws.cell(16, c)._style)
ws["B17"] = "− KiwiSaver under-accrual (hold at FY25 effective 1.89%, not 1.18%)"
ws["D17"] = -65000
ws["F17"] = "Every wage-on-cost ratio fell in FY26; KiwiSaver 1.18% vs FY25 1.89% = under-accrual flattering GP"
ws["B18"] = "− Temping Pays Accrual timing reversal (FY25 +$40,277 → FY26 credit)"
ws["D18"] = -20000
ws["F18"] = "Year-end wage-cutoff timing; conservative half-strip pending KPMG-final P&L (nets to ~0 over two years)"

# Recompute the EBITDA total (now row 19) as the honest sum of the bridge rows 8..18
def col_sum(letter):
    return sum((ws[f"{letter}{r}"].value or 0) for r in range(8, 19))
fy25, fy26 = col_sum("C"), col_sum("D")
ws["C19"], ws["D19"] = fy25, fy26
ws["E19"] = 500000                                    # FY27 built directly, flat basis
ws["F19"] = "FY26 ~$526K is the buyer-normalised basis; FY27 flat ~$500K"
# margins now on row 20
ws["C20"] = round(fy25 / 17890937, 4)
ws["D20"] = round(fy26 / 12640040, 4)
ws["E20"] = round(500000 / 12100000, 4)

# Read-across narrative (shifted +2 → rows 23/24/25)
sset(ws, "C23", "• FY25 normalised EBITDA ~$1.21M at $17.9M revenue shows earnings power AT SCALE — it is NOT the acquisition basis (FY26 ~$526K is).")
sset(ws, "B24", "• FY26 buyer-normalised EBITDA ~$526K after re-basing GP to maintainable 20.4% (stripping non-cash holiday-pay accrual releases) and correcting the over-stated IT & rent add-backs and the KiwiSaver under-accrual. The earlier $783K rested on a backwards provision-build story and over-stated add-backs.")
sset(ws, "B25", "• FY27 modelled FLAT-to-DECLINING at ~$500K. No +5% recovery: FY26 fell -29.3% YoY, trailing-12mo ~$12.1M is ~4% below FY26, no contracted pipeline. The Feb-Apr peak is seasonal, not recovery.")

print(f"Normalisation bridge recomputed: FY25={fy25:,.0f}  FY26={fy26:,.0f}  FY27=500,000")

# ---------- 2) Mgmt Accounts Reconciliation (the most-inverted tab) ----------
ws = wb["Mgmt Accounts Reconciliation"]
ws["C6"], ws["E6"] = "~20.4% (maintainable)", "⚠ FLATTERED"
ws["F6"] = "Reported 20.8% (11-mo) is INFLATED by holiday-pay accrual RELEASES — a CREDIT in COGS (FY26 -$154,914, FY25 -$268,156) that cuts cost and lifts GP. Provision is RELEASING as the business contracts ~29%, NOT building. Maintainable GP ~20.4%."
ws["C8"] = "~$86K (GL Wages-IT $116,614)"
ws["F8"] = "~$30K forward systems support is maintainable for a $12M BOSS+Crystal+Xero+CRM op"
ws["C9"], ws["D9"], ws["E9"] = "$28,655 used", "Xero $28,655 / total finance $45,558", "✓ CONFIRMED (no upside)"
ws["F9"] = "The ~$148K is a phantom (~3x the entire finance category) — DELETED. New CARL interest ~$114K/yr is a NewCo cost below EBITDA."
ws["C11"], ws["D11"], ws["E11"] = "~$526K (buyer-normalised, corrected)", "~$450–520K (trailing run-rate)", "⚠ CORRECTED DOWN"
ws["F11"] = "Re-based GP to 20.4% + corrected IT/rent/KiwiSaver/temping add-backs = ~$526K, not $783K. Trailing ~$12.1M is ~4% below FY26 = slight decline, growth UNPROVEN."
ws["B14"] = ("Net: revenue stabilised at a slight decline; GP is NOT ~21% — reported 20.8% is FLATTERED by holiday-pay accrual releases (a CREDIT in COGS), so maintainable GP is ~20.4%. The 'GP up to 21%' was an accounting artifact of a contracting business releasing provisions, not operating performance. Buyer-normalised EBITDA ~$526K, not $783K. The '~$148K interest upside' is a phantom and is deleted.")

# ---------- 3) Group Consolidated ----------
ws = wb["Group Consolidated"]
ws["D9"], ws["E9"], ws["F9"], ws["G9"] = 2574776, 0.2037, fy26, round(fy26/12640040, 4)
ws["D10"] = 1621420 + 2574776
ws["F10"] = 1436680 + fy26
ws["E10"] = round((1621420 + 2574776) / 20191220, 4)
ws["G10"] = round((1436680 + fy26) / 20191220, 4)
ws["B11"] = f"1st Call at FY26 buyer-normalised ~${fy26/1000:,.0f}K (corrected: GP re-based to 20.4%, over-stated IT/rent add-backs and KiwiSaver under-accrual fixed). Revenue declining ~4% — growth unproven."
# FY27 group
ws["D18"], ws["E18"], ws["F18"], ws["G18"] = 2468400, 0.204, 500000, round(500000/12100000, 4)
ws["D19"] = 1815990 + 2468400
ws["F19"] = 1609082 + 500000
ws["G19"] = round((1609082 + 500000) / 20557322, 4)
ws["B20"] = "Existing group +12% (CSFpace growth assumption); 1st Call FLAT (no recovery — revenue declining)."
ws["C24"] = f"$1.44M → ${(1436680+fy26)/1e6:.2f}M"
ws["F24"] = f"+{round((fy26)/1436680*100):.0f}%"
ws["C26"] = "19.0% → 9.7%"

# ---------- 4) Summary ----------
ws = wb["Summary"]
ws["C5"] = "~$850K target (open $700K · walk-away $950K)"
ws["C6"] = "$850,000 target — offered $1.1M (REJECTED); vendor seeks $1.6M (≈2.9x corrected EBITDA — not supportable)"
ws["C11"], ws["D11"] = 12640040, 12100000
ws["C12"], ws["D12"] = fy26, 500000
ws["C13"], ws["D13"] = 650000, 650000           # proven-floor / upside case (if rent+KiwiSaver DD-benign)
ws["B13"] = "Proven floor if rent + KiwiSaver DD-benign (GP+IT only)"
ws["C14"], ws["D14"] = round(fy26/12640040, 4), round(500000/12100000, 4)
ws["B16"] = "RETURNS (corrected EBITDA ~$526K)"
ws["C17"] = f"{1100000/fy26:.2f}x at $1.1M · {850000/fy26:.2f}x at $850K target"
ws["D17"] = f"{850000/500000:.2f}x (FY27)"
ws["C18"] = "~20 months at $850K target"
ws["C19"] = fy25
ws["B12"] = "Normalised EBITDA (corrected, buyer basis)"

wb.save(SRC)
wb.save(MIRROR)
print(f"Saved corrected model. Headline FY26 normalised EBITDA = ${fy26:,.0f}")
print(f"Multiple at $1.1M = {1100000/fy26:.2f}x ; at $850K target = {850000/fy26:.2f}x")
