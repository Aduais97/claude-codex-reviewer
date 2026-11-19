#!/usr/bin/env python3
"""Woolworths Primary Connect DC Security tender (Ref 523941) - fill Document 2
pricing workbook from a bottom-up charge build-up.

Takes the client's original template, populates the Charge Breakdown input cells
(base wage, statutory holiday loading, on-cost %s, operating %s, margin) for both
Standard and Supervisor guards, links every roster line in the Profile tab live to
the computed billing rate, flags the PRDC night-shift anomaly in the Comments
column, and records the Auckland-3 fallback total.

DRAFT: rates are ASG's recommended build-up for Ahmad to confirm. Yellow input
cells are the only ones to change. Figures may shift once Woolworths answers the
clarification questions (PRDC night shift, indexation, committed volumes).

Usage: .venv/bin/python build_pricing_workbook.py <original_template.xlsx> <out.xlsx>
"""
import sys
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.comments import Comment

YELLOW = PatternFill("solid", fgColor="FFF2CC")
NOTE_FILL = PatternFill("solid", fgColor="FDE9D9")
BOLD = Font(bold=True)

CB = "2. Pricing Proposal - Charge Br"   # exact (31-char truncated) sheet name
PROF = "3. Pricing Proposal - Profile"

# ---- Build-up inputs (COMPETITIVE scenario) ----------------------------------
# Base wages per Ahmad 19 Nov; lean 14% operating load; 5% margin to beat FIRST and
# sit at Allied's upper edge while staying above water.
# (Premium scenario was base 27.50/31.00, operating 17.5%, margin 11% -> $43.33/$48.85.)
# Standard Guard
STD = dict(base=25.50, stat=1.53,                       # $ base, $ stat-holiday loading (~6% of base)
           al=0.08, sick=0.035, bereav=0.003, acc=0.009, kiwi=0.035, other_leave=0.002,
           training=0.03, uniform=0.012, opsmgmt=0.045, equip=0.012, admin=0.021, other=0.02,
           margin=0.05)
# Supervisor Guard
SUP = dict(base=27.25, stat=1.64,
           al=0.08, sick=0.035, bereav=0.003, acc=0.009, kiwi=0.035, other_leave=0.002,
           training=0.03, uniform=0.012, opsmgmt=0.045, equip=0.012, admin=0.021, other=0.02,
           margin=0.05)


def fill_charge_breakdown(ws):
    ws["C3"] = "ASG Limited"
    ws["H3"] = "ASG Limited"
    # Standard Guard -> C (percent/base) and D7 (stat $)
    pct = "0.0%"
    dol = "#,##0.00"
    def put(cell, val, fmt):
        ws[cell] = val
        ws[cell].number_format = fmt
        ws[cell].fill = YELLOW
    put("C6", STD["base"], dol)
    put("D7", STD["stat"], dol)
    for cell, key in [("C10","al"),("C11","sick"),("C12","bereav"),("C13","acc"),
                      ("C14","kiwi"),("C15","other_leave"),("C19","training"),
                      ("C20","uniform"),("C21","opsmgmt"),("C22","equip"),
                      ("C23","admin"),("C24","other"),("C27","margin")]:
        put(cell, STD[key], pct)
    # Supervisor Guard -> H (percent/base) and I7 (stat $)
    put("H6", SUP["base"], dol)
    put("I7", SUP["stat"], dol)
    for cell, key in [("H10","al"),("H11","sick"),("H12","bereav"),("H13","acc"),
                      ("H14","kiwi"),("H15","other_leave"),("H19","training"),
                      ("H20","uniform"),("H21","opsmgmt"),("H22","equip"),
                      ("H23","admin"),("H24","other"),("H27","margin")]:
        put(cell, SUP[key], pct)
    # annotate the build-up
    ws["D7"].comment = Comment(
        "Statutory holiday loading built up for a 24/7 roster (worked public holidays at time-and-a-half "
        "plus alternative-day accrual, blended across productive hours). Approx 6% of base. Confirm per region "
        "anniversary days.", "ASG")
    ws["C6"].comment = Comment(
        "Base wage above the April 2026 minimum ($23.95), below living wage ($29.90): competitive positioning "
        "that still supports the stability/turnover answer. Confirm before submission.", "ASG")
    ws["C27"].comment = Comment(
        "Margin 5% markup to win on price against FIRST while staying above water. This is a thin, strategic "
        "number: net retained margin after unmodelled costs is near-breakeven (see cost analysis). "
        "Operating rows already trimmed to a lean 14%.", "ASG")


def compute_rate(p):
    d8 = p["base"] + p["stat"]
    al = p["al"] * d8
    sick = p["sick"] * d8
    bereav = p["bereav"] * d8
    acc = p["acc"] * (d8 + al + sick + bereav)
    kiwi = p["kiwi"] * (d8 + al + sick + bereav)
    other_leave = p["other_leave"] * d8
    d16 = al + sick + bereav + acc + kiwi + other_leave
    d17 = d16 + d8
    d25 = sum(p[k] for k in ("training","uniform","opsmgmt","equip","admin","other")) * d8
    d26 = d25 + d17
    margin = p["margin"] * d26
    return d26 + margin


def fill_profile(ws):
    std_ref = f"='{CB}'!$D$30"
    sup_ref = f"='{CB}'!$I$30"
    for row in range(5, 29):
        role = ws.cell(row, 6).value   # F = Guard Type
        if not role:
            continue
        r = role.strip().lower()
        if r.startswith("supervisor"):
            ws.cell(row, 13).value = sup_ref        # M
        elif r.startswith("standard"):
            ws.cell(row, 13).value = std_ref
        else:
            continue
        ws.cell(row, 13).number_format = "#,##0.00"
    # PRDC anomaly flag (rows 18-20) in Comments column P
    for row in (18, 19, 20):
        c = ws.cell(row, 16)   # P
        c.value = ("Priced as issued (all shifts 6:00AM-6:00PM). The 2-guard line reads days, not the "
                   "6:00PM-6:00AM night shift seen at every other site, so PRDC shows no night cover at a "
                   "24/7 site. Clarification lodged; rate holds, hours may rise if a night line is confirmed.")
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.fill = NOTE_FILL
    ws.column_dimensions["P"].width = 46
    # single-national-structure note on row 5
    ws.cell(5, 16).value = ("Single national pricing structure (Woolworths' stated preference): the same per-role "
                            "rates apply at every DC. ASG will also accept a selected-sites award for the Auckland "
                            "cluster (ARDC + ANDC + AFDC) at these same rates.")
    ws.cell(5, 16).alignment = Alignment(wrap_text=True, vertical="top")
    ws.cell(5, 16).fill = NOTE_FILL


def add_summary(ws):
    """Write an Auckland-3 fallback + draft banner below the grand total."""
    std = compute_rate(STD)
    sup = compute_rate(SUP)
    # weekly hours by role (from the issued profile)
    sup_wk = 84 + 60 + 84 + 84 + 40 + 84      # CRDC ANDC ARDC PRDC AFDC CFDC
    std_wk = 2056 - sup_wk
    akl_sup_wk = 84 + 60 + 40                  # ARDC + ANDC + AFDC
    akl_std_wk = (336 + 336 + 376) - akl_sup_wk
    national = (sup_wk * 52 * sup) + (std_wk * 52 * std)
    akl = (akl_sup_wk * 52 * sup) + (akl_std_wk * 52 * std)

    r = 33
    def line(txt, bold=False, fill=False):
        nonlocal r
        c = ws.cell(r, 2, txt)
        if bold:
            c.font = BOLD
        if fill:
            c.fill = NOTE_FILL
        r += 1

    line("DRAFT v1 - ASG recommended build-up. Confirm/adjust the yellow input cells before submission. "
         "Figures may change once the clarification answers arrive (PRDC night shift, indexation, volumes).",
         bold=True, fill=True)
    r += 1
    line(f"Standard Guard billing rate: ${std:,.2f}/hr   |   Supervisor Guard billing rate: ${sup:,.2f}/hr", bold=True)
    line(f"National (all 6 DCs): {2056:,} hrs/wk -> approx ${national:,.0f}/yr")
    line(f"Auckland-3 fallback (ARDC+ANDC+AFDC): {336+336+376:,} hrs/wk -> approx ${akl:,.0f}/yr")
    r += 1
    line("Base wage above market for workforce stability; statutory holiday built bottom-up for 24/7; "
         "margin stated plainly at 11%; all premiums blended into the flat rate. Rates subject to agreement "
         "of the MSA including an annual indexation mechanism.")
    for rr in range(33, r):
        ws.cell(rr, 2).alignment = Alignment(wrap_text=True, vertical="top")


def main(src, out):
    wb = openpyxl.load_workbook(src)
    fill_charge_breakdown(wb[CB])
    prof = wb[PROF]
    fill_profile(prof)
    add_summary(prof)
    wb.save(out)
    std, sup = compute_rate(STD), compute_rate(SUP)
    print(f"Written: {out}")
    print(f"Standard ${std:.2f}/hr  Supervisor ${sup:.2f}/hr")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
