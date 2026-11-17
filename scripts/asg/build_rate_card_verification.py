#!/usr/bin/env python3
"""Build the ASG invoice rate card verification workbook for admin sign-off.
Data: asg_invoices_fy27.json (Xero pull, FY27 to 16 Nov) + Timesheet w/e 08-11-2026."""
import json, re, datetime, os
from collections import Counter, defaultdict
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

SCRATCH = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.expanduser("~/Desktop/ASG/Finance/ASG Invoice Rate Card - Admin Verification.xlsx")

NAVY = "1F3864"; GOLD = "C9A227"; LIGHT = "EEF2F8"; YELLOW = "FFF4CC"; GREEN = "E7F4E4"; RED = "FDE8E8"
thin = Side(style="thin", color="B8C2D0")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

inv = [i for i in json.load(open(f"{SCRATCH}/asg_invoices_fy27.json")) if i["Status"] in ("PAID", "AUTHORISED", "DRAFT")]
by_contact = defaultdict(list)
for i in inv:
    by_contact[i["Contact"]["Name"]].append(i)
for c in by_contact:
    by_contact[c].sort(key=lambda i: i["DateString"])

def classify(desc):
    d = (desc or "").lower()
    ph = "public holiday" in d
    if "mileage" in d: return "CCTV_MILEAGE"
    if "cctv" in d: return "CCTV_WORK"
    if "head doorman" in d: return "PH_HD" if ph else "HD"
    if "professional host" in d or "host" in d: return "PH_HOST" if ph else "HOST"
    if "guard" in d: return "PH_GUARD" if ph else "GUARD"
    return "OTHER"

# ---- weekly scope: contact -> timesheet site substrings (lowercase, apostrophes stripped) ----
SITE_MAP = {
    "ACE KTV": ["ace ktv"],
    "AKA Rooftop": ["aka rooftop"],
    "Abbeville Estate": ["abbeville"],
    "Bar101": ["bar101", "darby street"],
    "Brew on Quay - Slattery and Sons": ["slattery"],
    "Citizen Park": ["citizen park"],
    "Danny Doolans": ["danny doolan"],
    "Doolan Brothers Ellerslie - O'Dowds": ["odowds"],
    "Elliott Management Limited": ["elliott stables"],
    "Farro Fresh": ["farro"],
    "Good George North Wharf": ["good george"],
    "Grand Central": ["grand central"],
    "Ground Zero": ["ground zero"],
    "Jungle 8": ["jungle 8"],
    "Kemuri": ["kemuri"],
    "Lime Bar": ["lime"],
    "Mcdonalds": ["mcdonald"],
    "Neck of the Woods": ["neck of the woods"],
    "Oceania Harmony": ["oceania"],
    "Parasol and Swing Company": ["parasol"],
    "Reign and Pour": ["reign"],
    "Sapphire - SALASAR BALAJI": ["sapphire"],
    "Shadows": ["shadows"],
    "Space On Crummer": ["space on crummer"],
    "Star Hospitality Group - Foxglove Wellington": ["fox glove", "foxglove"],
    "Star Hospitality Group - Goldie's Bar and Yard": ["goldies"],
    "Star Hospitality Group - Harbourside Function": ["harbourside"],
    "Star Hospitality Group - Hotel Bristol": ["hotel bristol"],
    "Star Hospitality Group - Southern Cross": ["southern cross"],
    "Star Hospitality Group Limited - Empire": ["empire"],
    "Star Hospitality Group Limited - Flying Moa": ["flying moa"],
    "Star Hospitality Group Limited - Garrison Public House": ["garrison"],
    "Star Hospitality Group Limited - Loosies Wellington": ["loosies"],
    "Star Hospitality Group Limited - Moretons": ["moretons"],
    "Star Hospitality Group Limited - Regatta": ["regatta"],
    "Star Hospitality Group Limited - Rosie's Viaduct": ["rosies viaduct"],
    "Star Hospitality Group Limited - Rosies Takapuna": ["rosies takapuna"],
    "Star Hospitality Group Limited - Sweat Shop Brew Kitchen": ["sweatshop", "sweat shop"],
    "Star Hospitality Group Limited - The Lula Inn": ["lula"],
    "Star Hospitality Group Limited - The Merchant Pub Co.": ["merchant"],
    "Star Hospitality Group Limited - The Postmans Leg": ["postman"],
    "The Broken Lantern": ["broken lantern"],
    "The Cav": ["the cav"],
    "The Celler Bar": ["cellar bar"],
    "The Earl - Basalt": ["basalt"],
    "The Fox": ["fox, a london pub", "the fox a london"],
    "VYC": ["vyc"],
    "Zookeepers Son New": ["zookeeper"],
    "Star Hospitality Group - The Green Man Pub Wellington": ["greenman", "green man"],
    "Star Hospitality Group Limited - Goode Brothers Botany": ["goode brothers"],
    "Hospo Night": ["ostend", "morra"],
    "Mudbrick": ["mudbrick", "rooftop bar", "wedding venue"],
    "Tantalus": ["tantalus"],
    "Stonyridge": ["stonyridge"],
    "Onetangi Hall": ["onetangi"],
}
FREQ = {
    "Brew on Quay - Slattery and Sons": "Ad-hoc - confirm",
    "The Cav": "Ad-hoc when worked",
    "Star Hospitality Group Limited - Goode Brothers Botany": "Per visit (CCTV)",
    "Hospo Night": "Per event",
    "Mudbrick": "Per event",
    "Tantalus": "Per event",
    "Stonyridge": "Per event",
    "Onetangi Hall": "Per event",
}
RATE_OVERRIDES = {
    "Brew on Quay - Slattery and Sons": {"HD": 42.00},
    "Mudbrick": {"GUARD": 55.00},
    "Onetangi Hall": {"GUARD": 55.00},
}
MINIMUMS = {
    "Elliott Management Limited": "6h per night minimum (fixed)",
    "Jungle 8": "6h per night minimum (fixed)",
    "Star Hospitality Group Limited - The Lula Inn": "3h minimum charge (per INV-5207)",
    "The Cav": "3h minimum charge (per INV-4625)",
}
NOTES = {
    "Mcdonalds": "One invoice covers all 3 sites (Queen St, Britomart, Balmoral), a line per site",
    "Bar101": "Invoice includes Darby Street Station hours as separate lines",
    "The Celler Bar": "Xero contact name is misspelt (Celler); site is The Cellar Bar",
    "The Fox": "Do not confuse with Foxglove Wellington (separate SHG contact)",
    "Elliott Management Limited": "RATE UNSTABLE: FY27 invoices alternate $39/$40 (12 straight at $40 Jul-Oct, latest 2 at $39). CONFIRM which is contractual",
    "Kemuri": "One service; Xero line alternates HEAD DOORMAN vs Security Host at same $38.50. Pick one canonical label",
    "Brew on Quay - Slattery and Sons": "$42 inferred from single catch-up INV-5370 (covers Aug+Nov). Confirm rate, terms (10d observed) and cadence",
    "Good George North Wharf": "Terms vary 14/17/7 across its 3 invoices (latest 7). Confirm",
    "Oceania Harmony": "Terms vary 14/18/11; last 2 invoices both due the 20th (date-of-month?). Client NEVER appears on the timesheet workbook - hours sourced elsewhere, manual-only for automation",
    "Farro Fresh": "Epsom weekly; Newmarket + Grey Lynn ad-hoc on same invoice at $36.50. Night-check/patrol jobs billed per-DAY ($250/$315), not hourly",
    "Star Hospitality Group - The Green Man Pub Wellington": "w/e 15-11 has 6h NOT YET INVOICED - raise invoice",
    "Star Hospitality Group Limited - Goode Brothers Botany": "Standalone CCTV-only client: 2h CCTV @ $45 + $19 mileage per visit, no guard hours",
    "Hospo Night": "Ad-hoc Waiheke events (Ostend War Memorial Hall, Morra Hall): Guard $55 + ferry $28.64. INV-5323 underbilled 0.5h (10.0 vs 10.5) - review",
    "Mudbrick": "Waiheke event venue, Guard $55 + disbursements (ferry/RT hireage). Rooftop Bar + Wedding Venue sites",
    "Tantalus": "Waiheke event venue, Guard $55 + disbursements",
    "Stonyridge": "Waiheke event venue, Guard $55 + disbursements",
    "Onetangi Hall": "Waiheke hall, Guard $55 + disbursements",
    "The Cav": "Ad-hoc: dormant Aug-Oct 2026, billed only when worked",
}

def resolve_contact(prefix):
    return prefix if prefix in by_contact else None

def contact_profile(full):
    invs = by_contact[full]
    last = invs[-1]
    rates = defaultdict(list)
    offs = []
    for i in invs[-6:]:
        for li in i.get("LineItems", []):
            cl = classify(li.get("Description"))
            ua = li.get("UnitAmount")
            if ua and ua > 0 and cl != "OTHER":
                rates[cl].append(ua)
        if i.get("DueDateString"):
            offs.append((datetime.date.fromisoformat(i["DueDateString"][:10])
                         - datetime.date.fromisoformat(i["DateString"][:10])).days)
    cur = {cl: Counter(v).most_common(1)[0][0] for cl, v in rates.items()}
    descs = [li.get("Description") or "" for i in invs[-4:] for li in i.get("LineItems", [])]
    if any(re.match(r"Professional Host \d", d) for d in descs):
        style = "One line per night (Professional Host DD/MM/YY)"
    elif any(re.match(r"(\d+/\d+/\d+\s+Security Guard|SECURITY GUARD \d)", d) for d in descs):
        style = "One line per night (Security Guard + date)"
    elif any(d.startswith("HEAD DOORMAN") for d in descs):
        style = "Aggregated weekly lines (HEAD DOORMAN / SECURITY GUARDS)"
    elif any(" from " in d.lower() and "-" in d for d in descs):
        style = "Single line, week date range"
    else:
        style = "Aggregated weekly line(s)"
    terms = Counter(offs).most_common(1)[0][0] if offs else ""
    return {
        "rates": cur, "style": style, "terms": terms, "n": len(invs),
        "last_no": last["InvoiceNumber"], "last_date": last["DateString"][:10],
    }

contacts = {}
for prefix in SITE_MAP:
    full = resolve_contact(prefix)
    if full:
        contacts[full] = contact_profile(full)
        contacts[full]["rates"].update(RATE_OVERRIDES.get(prefix, {}))
        if FREQ.get(prefix, "Weekly") != "Weekly":
            rr = contacts[full]["rates"]
            if rr.get("HOST") and rr.get("HOST") == rr.get("GUARD"):
                del rr["HOST"]
        contacts[full]["sites"] = SITE_MAP[prefix]
        contacts[full]["freq"] = FREQ.get(prefix, "Weekly")
        contacts[full]["min"] = MINIMUMS.get(prefix, "")
        contacts[full]["note"] = NOTES.get(prefix, "")

# ---- timesheet sites (w/e 08-11) loaded early so Sheet 1 can show real site names ----
tswb = openpyxl.load_workbook(os.path.expanduser("/Users/ahmadduais/Desktop/ASG - Timesheets/Timesheet - Weekending - 08-11-2026.xlsx"), data_only=True)
tsws = tswb["Site Summary"]
sites = {}
for row in tsws.iter_rows(values_only=True):
    if row and row[0] and isinstance(row[0], str) and row[0].strip() not in ("CLIENT / SITE", "TOTAL", "GRAND TOTAL") \
            and any(isinstance(x, (int, float)) for x in row[1:6] if x is not None):
        tot = row[5] if isinstance(row[5], (int, float)) else 0
        sites[row[0].strip()] = tot

def norm_site(s):
    s = s.replace("★", "").replace("↳", "").replace("'", "").replace("’", "").lower()
    return " ".join(s.replace("hd", " ").split()) if s.endswith("hd") else " ".join(s.split())

def pretty_site(s):
    return s.replace("★HD", "").replace("↳", "").strip()

for full, p in contacts.items():
    names = [pretty_site(sname) for sname in sites
             if any(sub in norm_site(sname) for sub in p["sites"])]
    p["display_sites"] = " + ".join(names) if names else " / ".join(w.title() for w in p["sites"])

wb = openpyxl.Workbook()

def style_header(ws, row, cols, fill=NAVY):
    for c in range(1, cols + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = Font(bold=True, color="FFFFFF", size=10)
        cell.fill = PatternFill("solid", fgColor=fill)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER

def title_block(ws, title, subtitle, cols):
    ws.cell(row=1, column=1, value=title).font = Font(bold=True, size=15, color=NAVY)
    ws.cell(row=2, column=1, value=subtitle).font = Font(size=10, color="5A6B82")
    ws.cell(row=3, column=1, value="Prepared 17 Nov 2026 from 873 Xero invoices (1 Jul - 16 Nov 2026). Please review each row, mark Confirm Y/N and note any corrections.").font = Font(italic=True, size=9, color="8A6D00")

# ================= Sheet 1: Rate Card =================
ws = wb.active
ws.title = "1. Rate Card"
HDRS = ["Xero Contact", "Timesheet Site(s)", "Freq", "Terms (days)", "Invoice Style",
        "HD $/hr", "Guard $/hr", "Host $/hr", "CCTV $/hr", "Mileage $",
        "Public Holiday $/hr (x1.5)", "Minimum / Fixed", "FY27 Inv #", "Last Invoice", "Notes",
        "CONFIRM (Y/N)", "Corrections"]
title_block(ws, "ASG Invoice Rate Card - Admin Verification", "All rates ex GST. Weekly hospitality clients only; monthly clients excluded for now.", len(HDRS))
hr = 5
for c, h in enumerate(HDRS, 1):
    ws.cell(row=hr, column=c, value=h)
style_header(ws, hr, len(HDRS))
r = hr + 1
for full, p in sorted(contacts.items()):
    rr = p["rates"]
    ph_parts = []
    for base, lab in (("HD", "HD"), ("GUARD", "Gd"), ("HOST", "Host")):
        if base in rr:
            ph_parts.append(f"{lab} {rr[base] * 1.5:.2f}")
    stale = (datetime.date(2026, 11, 17) - datetime.date.fromisoformat(p["last_date"])).days >= 21 \
        and p["freq"] == "Weekly"
    vals = [full, p["display_sites"], p["freq"], p["terms"], p["style"],
            rr.get("HD", ""), rr.get("GUARD", ""), rr.get("HOST", ""),
            rr.get("CCTV_WORK", ""), rr.get("CCTV_MILEAGE", ""),
            ", ".join(ph_parts), p["min"], p["n"],
            f'{p["last_no"]} on {datetime.date.fromisoformat(p["last_date"]).strftime("%d %b")}'
            + (" (CHECK: not billed in 3+ weeks)" if stale else ""),
            p["note"], "", ""]
    for c, v in enumerate(vals, 1):
        cell = ws.cell(row=r, column=c, value=v)
        cell.border = BORDER
        cell.font = Font(size=9)
        cell.alignment = Alignment(vertical="center", wrap_text=(c in (1, 2, 5, 11, 12, 14, 15, 17)))
        if c in (6, 7, 8, 9, 10):
            cell.number_format = "0.00"
            cell.alignment = Alignment(horizontal="center")
        if r % 2 == 0:
            cell.fill = PatternFill("solid", fgColor=LIGHT)
        if c >= len(HDRS) - 1:
            cell.fill = PatternFill("solid", fgColor=YELLOW)
    r += 1
widths = [34, 26, 7, 7, 34, 8, 8, 8, 8, 8, 20, 22, 7, 20, 30, 9, 24]
for c, w in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(c)].width = w
ws.freeze_panes = "A6"

# ================= Sheet 2: Week check =================

wk_inv_hours = {}
for i in inv:
    if "2026-11-09" <= i["DateString"][:10] <= "2026-11-16":
        h = sum((li.get("Quantity") or 0) for li in i.get("LineItems", [])
                if (li.get("UnitAmount") or 0) > 10 and "mileage" not in (li.get("Description") or "").lower()
                and (li.get("Quantity") or 0) > 0)
        # SUM across multiple invoices in the window (catch-up invoices must not be hidden)
        prev_h, prev_nos = wk_inv_hours.get(i["Contact"]["Name"], (0.0, []))
        wk_inv_hours[i["Contact"]["Name"]] = (prev_h + h, prev_nos + [i["InvoiceNumber"]])

ws2 = wb.create_sheet("2. Week Check (w-e 08 Nov)")
H2 = ["Xero Contact", "Timesheet Site(s) incl CCTV", "Timesheet hrs", "Invoiced hrs", "Diff", "Status", "Explanation", "CONFIRM (Y/N)", "Corrections"]
title_block(ws2, "Sample Week Reconciliation - week ending Sun 08 Nov 2026",
            "Hours on the timesheet workbook vs hours on the Xero invoice raised 9-16 Nov. CCTV hours and multi-site clients are folded per billing practice.", len(H2))
hr = 5
for c, h in enumerate(H2, 1):
    ws2.cell(row=hr, column=c, value=h)
style_header(ws2, hr, len(H2))
r = hr + 1
EXPLAIN = {
    "Brew on Quay - Slattery and Sons": "Invoice was a manual catch-up (included August hours), not a mismatch",
    "Star Hospitality Group Limited - Loosies Wellington": "Timesheet 8.42h billed as 8.50h - quarter hour rounding",
    "Oceania Harmony": "Client never appears on the timesheet workbook; hours sourced elsewhere (manual-only)",
}
matched_sites = set()
for full, p in sorted(contacts.items()):
    subs = p["sites"]
    wbh = 0.0; names = []
    for sname, tot in sites.items():
        ns = norm_site(sname)
        if any(sub in ns for sub in subs):
            wbh += tot; names.append(sname); matched_sites.add(sname)
    if full not in wk_inv_hours and wbh == 0:
        continue
    ivh, invnos = wk_inv_hours.get(full, (None, []))
    invno = " + ".join(invnos) if invnos else "no invoice found"
    multi = len(invnos) > 1
    diff = (ivh - wbh) if ivh is not None else None
    if ivh is None:
        status, fillc = "NO INVOICE", RED
        expl = "No invoice found dated 9-16 Nov; confirm whether billed late or missed"
    elif abs(diff) < 0.005:
        status, fillc = "TIES", GREEN
        expl = EXPLAIN.get(full, "")
    elif abs(diff) <= 0.13:
        status, fillc = "TIES (rounding)", GREEN
        expl = EXPLAIN.get(full, "Quarter hour rounding")
    elif p["freq"] != "Weekly":
        status, fillc = "PER EVENT", YELLOW
        expl = EXPLAIN.get(full, "Not week-aligned: client invoices per event/visit, so this week's timesheet and invoice cover different events")
    else:
        status, fillc = f"DIFF {diff:+.2f}", RED
        expl = EXPLAIN.get(full, "Please review")
        if full in EXPLAIN:
            status, fillc = "EXPLAINED", YELLOW
    if multi:
        expl = ("MULTI-INVOICE week (incl. catch-up). " + expl).strip()
    vals = [full, " + ".join(names) if names else "(no row this week)", round(wbh, 2),
            ivh if ivh is not None else "", round(diff, 2) if diff is not None else "",
            status, expl + (f"  [{invno}]" if ivh is not None else ""), "", ""]
    for c, v in enumerate(vals, 1):
        cell = ws2.cell(row=r, column=c, value=v)
        cell.border = BORDER; cell.font = Font(size=9)
        cell.alignment = Alignment(vertical="center", wrap_text=(c in (1, 2, 7, 9)))
        if c == 6:
            cell.fill = PatternFill("solid", fgColor=fillc)
            cell.font = Font(size=9, bold=True)
        elif c >= 8:
            cell.fill = PatternFill("solid", fgColor=YELLOW)
        elif r % 2 == 0:
            cell.fill = PatternFill("solid", fgColor=LIGHT)
    r += 1
r += 1
ws2.cell(row=r, column=1, value="UNBILLED WORK FOUND (out-of-sample checks of other weeks) - ACTION REQUIRED:").font = Font(bold=True, size=10, color="9C1C1C")
r += 1
UNBILLED = [
    ("Reign and Pour", "w/e 01 Nov: 15.0h worked Fri 30 + Sat 31 Oct (Asela Usufono 3.75 + Simi Palu 4.75 + 6.5) has NO invoice anywhere in the Xero pull. At $38.50 = $577.50 ex GST. BACK-BILL.", 15.0),
    ("Star Hospitality Group - The Green Man Pub Wellington", "w/e 15-11: 6.0h on the timesheet, no invoice yet (last Green Man invoice INV-5206, 20 Oct). ~$234.00 ex GST. RAISE.", 6.0),
    ("Star Hospitality Group Limited - Goode Brothers Botany", "w/e 15-11: CCTV 2.0h on the timesheet, no invoice yet (last was INV-5287, 2 Nov). $109.00 ex GST incl mileage. RAISE.", 2.0),
    ("Hospo Night", "INV-5323 (9 Nov) billed 10.0h but guards worked 7:00pm-12:15am x2 = 10.5h. 0.5h / $27.50 ex GST under-billed. REVIEW.", 0.5),
]
for cname, detail, hrs in UNBILLED:
    for c, v in enumerate([cname, "", hrs, "", "", "UNBILLED", detail, "", ""], 1):
        cell = ws2.cell(row=r, column=c, value=v)
        cell.border = BORDER; cell.font = Font(size=9, bold=(c in (1, 6)))
        cell.alignment = Alignment(vertical="center", wrap_text=(c in (1, 7)))
        if c in (6, 7):
            cell.fill = PatternFill("solid", fgColor=RED)
        if c >= 8:
            cell.fill = PatternFill("solid", fgColor=YELLOW)
    r += 1
r += 1
ws2.cell(row=r, column=1, value="Timesheet sites NOT billed weekly (monthly / separate / to review):").font = Font(bold=True, size=10, color=NAVY)
r += 1
MONTHLY_KNOWN = {"oak hotel": "Monthly - parked for now", "waiheke marina": "Monthly - parked",
                 "raddison": "Monthly - parked", "radisson": "Monthly - parked",
                 "take 10": "Monthly - parked", "darby": "Billed inside Bar101 weekly invoice"}
for sname, tot in sorted(sites.items()):
    if sname in matched_sites:
        continue
    ns = norm_site(sname)
    note = next((v for k, v in MONTHLY_KNOWN.items() if k in ns), "REVIEW: how is this billed?")
    for c, v in enumerate([sname, "", round(tot, 2), "", "", "", note, "", ""], 1):
        cell = ws2.cell(row=r, column=c, value=v)
        cell.border = BORDER; cell.font = Font(size=9, italic=True)
        if "REVIEW" in note and c == 7:
            cell.fill = PatternFill("solid", fgColor=RED)
    r += 1
w2 = [34, 30, 11, 11, 8, 14, 52, 9, 20]
for c, w in enumerate(w2, 1):
    ws2.column_dimensions[get_column_letter(c)].width = w
ws2.freeze_panes = "A6"

# ================= Sheet 3: Conventions =================
ws3 = wb.create_sheet("3. Billing Conventions")
title_block(ws3, "Invoicing Conventions (as practised, from FY27 invoices)", "These rules will be baked into the automated draft invoice generator.", 3)
RULES = [
    ("GST", "All rates entered ex GST; Xero tax type OUTPUT2 (15% on income). Account code 200 on every line."),
    ("Item codes", "1 = SECURITY GUARDS, 2 = HEAD DOORMAN, 4 = Professional Host, 5 = CCTV Work, 6 = CCTV Mileage."),
    ("Timing", "Weekly invoices raised Monday or Tuesday for the prior Monday-Sunday week, after the timesheet workbook is approved."),
    ("Public holidays", "PH hours billed at exactly 1.5x the client base rate, as a separate line marked (Public Holiday)."),
    ("Rounding", "Hours billed rounded to the NEAREST quarter hour (0.25). Confirmed 17 Nov 2026."),
    ("Elliott Stables and Jungle 8", "Fixed 6h per night each. Last invoices (INV-5336 / INV-5337, 10 Nov) at $39.00/hr, BUT Elliott's FY27 history alternates $39/$40 (12 straight at $40 Jul-Oct). ADMIN TO CONFIRM the contractual rate before automation. Jungle 8 is cleanly $39 since 29 Sep."),
    ("Minimum charges", "Known minimums: Elliott Stables and Jungle 8 = 6h/night; The Lula Inn = 3h (INV-5207); The Cav = 3h (INV-4625). Admin to confirm whether other venues carry minimums."),
    ("CCTV", "CCTV hours billed on the parent venue invoice at $45/hr plus one CCTV Mileage line at $19. CCTV stays flat $45 on public holidays (no 1.5x). Goode Brothers Botany is CCTV-ONLY on its own standalone invoice (2h + mileage per visit)."),
    ("McDonald's", "Single weekly invoice, separate HEAD DOORMAN line per site: Queen St, Britomart, Balmoral."),
    ("Bar101", "Weekly invoice includes Darby Street Station lines."),
    ("Farro Fresh", "Epsom weekly at $36.50/hr; Newmarket and Grey Lynn appear ad-hoc on the same invoice. Night-check / patrol jobs are billed per-DAY ($250 / $315), never as hours."),
    ("Waiheke event venues", "Mudbrick, Tantalus, Stonyridge, Onetangi Hall, Hospo Night (and one-offs like Island Sound): Guard $55/hr billed per event, plus disbursements (ferry/boat tickets ~$28.64, RT hireage ~$20). Not part of weekly automation; keep manual."),
    ("Payment terms", "Most clients: 7 or 14 days from invoice date. Known exceptions: Slattery 10d (single observation), Good George varies (14/17/7), Oceania Harmony possibly due-on-the-20th. See Rate Card sheet per client."),
    ("Excluded from weekly automation", "Oak Hotel Wellington, Waiheke Marina, Radisson RED, Take 10, Auckland Harbour Suites, Viaduct Harbour, Metropolis, HOTC, AT stations - these stay manual / monthly for now."),
    ("Drafts only", "The automation will create DRAFT invoices in Xero only. Admin reviews and approves in Xero; nothing is sent automatically."),
]
hr = 5
ws3.cell(row=hr, column=1, value="Rule"); ws3.cell(row=hr, column=2, value="Detail")
style_header(ws3, hr, 2)
r = hr + 1
for name, detail in RULES:
    a = ws3.cell(row=r, column=1, value=name); b = ws3.cell(row=r, column=2, value=detail)
    a.font = Font(bold=True, size=9, color=NAVY); b.font = Font(size=9)
    a.border = BORDER; b.border = BORDER
    a.alignment = Alignment(vertical="top"); b.alignment = Alignment(vertical="top", wrap_text=True)
    if r % 2 == 0:
        a.fill = PatternFill("solid", fgColor=LIGHT); b.fill = PatternFill("solid", fgColor=LIGHT)
    for c in (3, 4):
        cell = ws3.cell(row=r, column=c, value="")
        cell.border = BORDER
        cell.fill = PatternFill("solid", fgColor=YELLOW)
    r += 1
ws3.cell(row=5, column=3, value="CONFIRM (Y/N)")
ws3.cell(row=5, column=4, value="Corrections")
style_header(ws3, 5, 4)
ws3.column_dimensions["A"].width = 30; ws3.column_dimensions["B"].width = 100
ws3.column_dimensions["C"].width = 12; ws3.column_dimensions["D"].width = 28
ws3.freeze_panes = "A6"

os.makedirs(os.path.dirname(OUT), exist_ok=True)
wb.save(OUT)
print("SAVED:", OUT)
print("rate card rows:", len(contacts))
