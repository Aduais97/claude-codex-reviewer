#!/usr/bin/env python3
"""Land-bank pack: cover + 11 per-property PDF profiles (ETR-corrected ranking).

Design per ~/.claude/commands/references/generate-pdf.md (ReportLab, navy/gold,
no callout boxes, tables >=8.5pt, em-dash-free client copy, macrons ASCII-ised).
Images: ./images/. Output: ~/Desktop/Property/Landbank12/.
ETR review applied: 25 findings, corrected ranking, 2 cuts, 92 Adams promoted.
"""
import re
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle, HRFlowable, Image)

NAVY = HexColor("#1B2A4A"); DBLUE = HexColor("#2C3E6B"); MBLUE = HexColor("#4A6FA5")
GOLD = HexColor("#D4A843"); LBLUE = HexColor("#E8EDF5"); BORDER = HexColor("#D0D5DD")
ALT = HexColor("#F2F4F8"); TDARK = HexColor("#1A1A2E"); TMED = HexColor("#4A4A5A")
TLIGHT = HexColor("#7A7A8A")

SRC = Path(__file__).parent
IMG = SRC / "images"
OUT = Path.home() / "Desktop" / "Property" / "Landbank12"
OUT.mkdir(parents=True, exist_ok=True)
W = A4[0] - 108

body = ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=14.5,
                      textColor=TDARK, alignment=TA_JUSTIFY, spaceAfter=7)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=18, bulletIndent=6, spaceAfter=4)
h3s = ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=11.5, leading=15,
                     textColor=DBLUE, spaceBefore=10, spaceAfter=3)
cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=9, leading=12, textColor=TDARK)
cellw = ParagraphStyle("cellw", fontName="Helvetica-Bold", fontSize=8.5, leading=11,
                       textColor=HexColor("#FFFFFF"), alignment=TA_CENTER)
small = ParagraphStyle("small", parent=body, fontSize=8.5, leading=11.5, textColor=TMED)

STANDARD_BLOCK = ("**Standard conditions applying to every option in this pack:** re-verify the "
                  "listing is active on the day any offer is drafted and again before going "
                  "unconditional; every cap is GST-settled, never plus GST; the accountant's land-taint "
                  "(ss CB 9-11) and CB 6 intent opinion must be in hand before ANY offer; ownership "
                  "vehicle settled before contract; parcel-level LIM (zone, flood, SEA, grid) before "
                  "unconditional; this pack funds ONE purchase unless the family explicitly decides "
                  "otherwise. Profiles are stale after 1 December 2026.")


def clean(t):
    for a, b in (("ā", "a"), ("ē", "e"), ("ī", "i"), ("ō", "o"), ("ū", "u"),
                 ("Ā", "A"), ("Ē", "E"), ("Ī", "I"), ("Ō", "O"), ("Ū", "U")):
        t = t.replace(a, b)
    return t.replace(" — ", " - ").replace("—", "-").replace("≈", "~").replace("≤", "max ")


def mi(t):
    t = clean(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)


def fitted_image(path, max_w, max_h):
    r = ImageReader(str(path)); iw, ih = r.getSize()
    s = min(max_w / iw, max_h / ih)
    return Image(str(path), width=iw * s, height=ih * s)


def doc_shell(path, title):
    doc = BaseDocTemplate(str(path), pagesize=A4, leftMargin=54, rightMargin=54,
                          topMargin=62, bottomMargin=54, title=clean(title))
    frame = Frame(54, 54, W, A4[1] - 116, id="main")

    def decorate(canv, _doc):
        canv.saveState()
        canv.setStrokeColor(BORDER); canv.setLineWidth(0.5)
        canv.line(54, A4[1] - 40, A4[0] - 54, A4[1] - 40)
        canv.setFont("Helvetica", 7); canv.setFillColor(TLIGHT)
        canv.drawString(54, A4[1] - 36, "Duais Family | Land Bank Options $1.3M-$1.8M")
        canv.drawRightString(A4[0] - 54, A4[1] - 36, "CONFIDENTIAL")
        canv.line(54, 40, A4[0] - 54, 40)
        canv.setFont("Helvetica", 7.5)
        canv.drawString(54, 30, "1 November 2026 | stale after 1 Dec 2026")
        canv.drawCentredString(A4[0] / 2, 30, f"Page {canv.getPageNumber()}")
        canv.drawRightString(A4[0] - 54, 30, "ETR-reviewed (25 findings applied)")
        canv.restoreState()

    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=decorate)])
    return doc


def navy_bar(text, size=14):
    bar = Table([[Paragraph(mi(text), ParagraphStyle(
        "hb", fontName="Helvetica-Bold", fontSize=size, leading=size + 4,
        textColor=HexColor("#FFFFFF"), leftIndent=6))]], colWidths=[W])
    bar.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY),
                             ("LINEBEFORE", (0, 0), (0, -1), 4, GOLD),
                             ("TOPPADDING", (0, 0), (-1, -1), 7),
                             ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                             ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
    return bar


def profile_flow(p):
    f = [navy_bar(f"#{p['rank']}  -  {p['address']}")]
    f.append(Spacer(1, 4))
    f.append(Paragraph(mi(f"**{p['tier']}**  |  {p['headline']}"), ParagraphStyle(
        "sub", parent=body, fontSize=10.5, textColor=MBLUE, spaceAfter=8)))
    if p.get("valid_until"):
        f.append(Paragraph(mi(f"**VALID UNTIL {p['valid_until']}** - after that date this "
                              "profile's tactic lapses and must be re-cut."), ParagraphStyle(
            "vu", parent=body, fontName="Helvetica-Bold", textColor=DBLUE, spaceAfter=6)))
    if p.get("img1") and (IMG / p["img1"]).exists():
        f.append(fitted_image(IMG / p["img1"], W, 290))
        f.append(Paragraph(mi(p.get("img1cap", "Listing photo (verified active 1 Nov 2026)")),
                           ParagraphStyle("cap", fontName="Helvetica-Oblique", fontSize=8,
                                          leading=10, textColor=TMED, spaceBefore=3,
                                          spaceAfter=8, alignment=TA_CENTER)))
    rows = [[Paragraph(f"<b>{mi(k)}</b>", cell), Paragraph(mi(v), cell)] for k, v in p["facts"]]
    t = Table(rows, colWidths=[W * 0.26, W * 0.74])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, BORDER),
                           ("BACKGROUND", (0, 0), (0, -1), LBLUE),
                           ("TOPPADDING", (0, 0), (-1, -1), 5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                           ("LEFTPADDING", (0, 0), (-1, -1), 6),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    f += [t, Spacer(1, 6)]
    f.append(Paragraph("Why it is on the list", h3s))
    f.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=5))
    f.append(Paragraph(mi(p["thesis"]), body))
    f.append(Paragraph("Risks and conditions before any offer", h3s))
    f.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=5))
    for r in p["risks"]:
        f.append(Paragraph(mi(r), bullet, bulletText="•"))
    f.append(Spacer(1, 4))
    f.append(Paragraph(mi(f"**Offer tactics:** {p['tactics']}"), body))
    if p.get("img2") and (IMG / p["img2"]).exists():
        f.append(Spacer(1, 6))
        f.append(fitted_image(IMG / p["img2"], W, 240))
    f.append(Spacer(1, 8))
    f.append(Paragraph(mi(STANDARD_BLOCK), small))
    f.append(Paragraph(mi(f"Listing: {p['url']}"), ParagraphStyle(
        "url", parent=body, fontSize=8, leading=10, textColor=TMED)))
    return f


def build(p):
    safe = re.sub(r"[^A-Za-z0-9]+", "_", clean(p["address"])).strip("_")
    path = OUT / f"{p['rank']:02d}_{safe}.pdf"
    doc_shell(path, f"Land Bank Option {p['rank']} - {p['address']}").build(profile_flow(p))
    return path


PROPERTIES = []


def P(**kw):
    PROPERTIES.append(kw)


# ============ CORRECTED RANKING (ETR deliverable b) ============
P(rank=1, address="2 Rope Road, Whenuapai",
  tier="TIER A | Future Urban Zone, GIS-confirmed",
  headline="The only anchored multiple in the pack: 55-60 percent of a transacted corridor rate",
  img1="rope1.jpg", img2="rope2.jpg",
  img1cap="Listing aerial with indicative boundary; bare paddock, no pylons (verified 1 Nov 2026)",
  facts=[("Land", "11,684 m2 bare (L-shaped paddock)"),
         ("Price / method", "By negotiation, no guide. On market since Oct 2024 (~25 months as listed; confirm the full listing history with the agent: a relist can mask even longer)"),
         ("Agent", "Barfoot and Thompson Meadowlands (Jing Li / Helen Han)"),
         ("Zone", "FUTURE URBAN ZONE, confirmed by council GIS point query 1 Nov 2026; flood, flood-prone, grid and SEA overlays clear at point"),
         ("Price rate", "$128-150/m2 at $1.50-1.75M vs the corridor's own TRANSACTED rate of $245-257/m2 (80 Trig Rd sold $11.0M / 4.28ha, 2025)"),
         ("Carry estimate", "Bare land, zero income: ~$60-75k per year all-in at 60 percent LVR (estimate; actual rates assessment required before modelling)"),
         ("Catalysts", "PC107 operative; PC109 + PC122 plan changes in process; Watercare wastewater ~2028; Brigham Creek busway station design-funded ~2km; Westgate station open")],
  thesis="Whenuapai is the one Auckland greenfield front where urbanisation inside 10 years is the base case rather than the hope. Land in this corridor has actually sold at $245-257/m2; at $1.5-1.75M this parcel costs roughly 55-60 percent of that transacted rate. The exit arithmetic is evidenced, not extrapolated: at the corridor's own sale rate the parcel maps to about $2.9M. The open question a 25-month-stale listing must answer is WHY it has not sold at a discount this visible: the first due diligence spend on this entire pack should be the airbase noise-contour check on this parcel, because contours are the one defect that would explain the staleness and void the thesis.",
  risks=["FIRST DD SPEND OF THE PACK: parcel-level airbase noise-contour check. If contours touch the parcel, the profile is void.",
         "Ask the agent directly for the full listing and offer history: 25 months unsold at an apparent discount demands an explanation before your money arrives.",
         "Smallest Tier A quantum; rezoning of small parcels relies on neighbours aggregating; council will not run the rezoning itself.",
         "Carry as tabled; obtain the actual rates assessment."],
  tactics="Open $1.40M. Target $1.55-1.65M. Cap $1.75M, GST-settled in writing.",
  url="realestate.co.nz/42656003")

P(rank=2, address="106 Pukekohe East Road, Pukekohe",
  tier="TIER A | Future Urban Zone, GIS-confirmed",
  headline="Highest rezone-in-window probability at this budget, with the pack's only real income",
  img1="pukekohe106.jpg",
  facts=[("Land", "8,200 m2 with two dwellings plus barn"),
         ("Price / method", "By negotiation; HomesEstimate $1.6-1.8M. Listed ~52 days"),
         ("Zone", "FUTURE URBAN ZONE, stated in listing AND confirmed by council GIS point query; hazard overlays clear"),
         ("Price rate", "AT CAP THIS IS $213/m2 - THE HIGHEST RATE IN THE PACK. It is justified only by the income and the corridor's rezoning cadence; it is not cheap land"),
         ("Income", "Two dwellings: the only strong carry-offset in the pack (rental appraisals required before counting it)"),
         ("Catalysts", "Inside the Pukekohe-Paerata structure plan, where private plan changes go operative roughly yearly (PC95, PC98, PC110, PC124 queued); 3 minutes to town and rail; CRL frequency south")],
  thesis="The Pukekohe-Paerata corridor has the highest documented probability of actual rezoning within the hold window at this budget: the structure plan was adopted in 2019 and landowner plan changes keep converting Future Urban to live zoning year on year. This parcel is Future Urban on both the listing and the council's GIS, and its two dwellings mean the hold largely pays for itself. The discipline is the rate: you are paying the pack's highest price per square metre for the smallest Tier A parcel, which only works because the probability and the income are also the pack's highest.",
  risks=["HARD WALK RULE: not one dollar above $1.75M. At $213/m2 the margin of safety is already the thinnest in the pack.",
         "Smallest Tier A quantum: uplift multiplies a smaller base.",
         "Dwelling condition, insurance and Healthy Homes checks before counting rent; written rental appraisals, not the agent's verbal.",
         "Elite-soil overlay formality check (FUZ identification normally carves it out)."],
  tactics="Open $1.50M. Cap $1.75M, GST-settled. Walk above it without exception.",
  url="trademe.co.nz listing 6125148747")

P(rank=3, address="79 Follies Way, Dairy Flat",
  tier="TIER A | Future Urban Zone, GIS-confirmed; grid corridor CLEAR (point + 300m envelope)",
  headline="The clean Follies Way lot, in a street whose other sellers are stranded by pylons",
  img1="follies79.jpg",
  img1cap="Listing aerial with boundary overlay; no transmission structures on this parcel (verified 1 Nov 2026)",
  facts=[("Land", "17,202 m2 bare"),
         ("Price / method", "ASKING $1,590,000 ($92/m2). Listed ~5.5 months"),
         ("Zone", "FUTURE URBAN ZONE, stated and GIS-confirmed; National Grid corridor CLEAR at point AND within a 300m envelope - the strongest grid evidence in the pack. Two nearby lots (20 Follies Way, Lot 2 Bawden Rd) failed exactly this test and were excluded"),
         ("Carry estimate", "Zero income; $50-86k per year all-in depending on the rates assessment (Dairy Flat FUZ rates run as high as ~$27,500); over a 10-15 year hold that compounds to roughly $700k-$1.2M of carry"),
         ("Catalysts", "Dairy Flat FUZ core; designated Albany-Milldale rapid transit geography; Penlink 2029; Milldale advancing from the north")],
  thesis="Dairy Flat is the only corridor where confirmed Future Urban land clears inside the band, and Follies Way is its distress street: pylon-stranded neighbours are dragging every comp down. This lot is GIS-verified clear of the grid corridor at both point and envelope, so it buys the street's depressed pricing without the street's defect. THE DEEP-TIME BLOCK, stated plainly: council sequencing says residential urbanisation here is 2050-plus and Watercare calls servicing 20-plus years away. This purchase is therefore a priced OPTION on the mid-2027 national policy direction and on private plan changes jumping the queue (as PC103 already did at Silverdale West). If neither happens, the exit inside 15 years is to another land-banker, not a developer.",
  risks=["Deep-time risk as stated in the thesis: this is the central risk, not a footnote.",
         "Zero income; carry as tabled; actual rates assessment first.",
         "Flood and geotech desktop (Waitemata soils, Zone 3) at parcel level.",
         "Never pay the ask in a street where stranded neighbours depress all comps."],
  tactics="Open $1.35M. Cap $1.50M, GST-settled.",
  url="realestate.co.nz/43048427")

P(rank=4, address="7 Bobs Way, Dairy Flat",
  tier="TIER A | Future Urban Zone, GIS-confirmed",
  headline="The cheapest confirmed-FUZ dollars on the board, marketed below its own CV",
  img1="bobs7.jpg",
  facts=[("Land", "20,100 m2 bare"),
         ("Price / method", "By negotiation, listing says 'priced well below CV'; CV (May 2024) $1,255,500. Listed ~4.5 months"),
         ("Zone", "FUTURE URBAN ZONE, stated and GIS-confirmed; grid corridor CLEAR at point and 300m envelope; flood and SEA clear"),
         ("Identity check", "An eliminated Follies Way lot shares this parcel's 20,100 m2 area. Resolved on geography 1 Nov: 7 Bobs Way geocodes 1,043m from 20 Follies Way on a different named road, with its own clean grid result; the area match is the subdivision's standard 2ha lot size. Title/DP search remains a pre-offer formality"),
         ("Price rate", "~$60/m2 if secured near CV: the cheapest confirmed-FUZ rate found anywhere in this search"),
         ("Carry estimate", "Zero income; $50-86k per year all-in pending the rates assessment; 10-15yr cumulative roughly $700k-$1.2M")],
  thesis="Two hectares of GIS-confirmed Future Urban land at roughly sixty dollars a square metre is less than half the historical Dairy Flat englobo benchmark and a fraction of the same zoning in Whenuapai, from a vendor advertising a below-CV sale. THE DEEP-TIME BLOCK applies in full: Dairy Flat residential sequencing is officially 2050-plus; this is a priced option on the mid-2027 policy direction, and at this entry price the option premium is the smallest on the list. If the policy bet fails, the 15-year exit is to another land-banker.",
  risks=["Title/DP search before offer: confirms identity beyond the geographic resolution and surfaces the covenants.",
         "Land covenants apply per the listing: condition one is confirming they do not bind future development or resale.",
         "Deep-time risk identical to number 3.",
         "Zero income; carry as tabled; rates assessment first."],
  tactics="Open $1.10M. Cap $1.30M, GST-settled.",
  url="realestate.co.nz/43065925")

P(rank=5, address="197 Charles Road, Karaka",
  tier="TIER C | No zoning: value, scale and execution probability",
  headline="Entry at 61-66 percent of RV, below even forced-sale clearing levels, from a vendor begging for offers",
  img1="charles_aerial.jpg", img2="charles_ground.jpg",
  img1cap="The honest aerial with boundary (other campaign photos are stylised; rely on this one)",
  facts=[("Land", "6.96 ha, FLAT, earthworks completed, building consents granted. Title 695594"),
         ("Price / method", "Fresh relist 21 Oct 2026 (Boulgaris Realty): 'PRESENT A CHEEKY OFFER'. Prior campaign asked $1.95M from Jun 2024 and failed for ~2.4 years"),
         ("Value markers", "RV May 2024 $2.725M (land $2.7M); last sold May 2020 at $1.25M. At $1.65-1.8M you enter at 61-66 percent of RV - deeper than Auckland forced-sale clearing levels"),
         ("Zone", "Rural Production, GIS-confirmed; flood, grid and SEA clear at point"),
         ("Carry estimate", "Minimal income (grazing at best): ~$55-70k per year all-in at 60 percent LVR; rates assessment required"),
         ("Catalysts", "Between Karaka and the Drury West growth front; F&P/hospital precinct and the new rail stations to the east")],
  thesis="Promoted over four Tier A and B entries by the review because probability-weighted return is not just about zoning: this is the pack's best downside protection and its highest execution probability. Seven flat, earthworked hectares at $24-26/m2 - a tenth of zoned Drury rates - from a vendor who failed at $1.95M for over two years and is now openly inviting low offers. It holds no Future Urban status and Karaka sits behind Drury West in sequencing, so it is honestly a value-and-optionality purchase: you are buying more usable land per dollar than anywhere else on this list, at a price that already assumes nothing good ever happens.",
  risks=["No FUZ status and no sequencing signal: patience capital, labelled as such.",
         "Trust only the boundary aerial; several campaign photos are heavily stylised.",
         "Verify what the granted building consents cover and when they lapse.",
         "GST position early: at this size a plus-GST surprise is large."],
  tactics="As invited: open $1.50M. Cap $1.75M, GST-settled.",
  url="realestate.co.nz/42587325")

P(rank=6, address="130 Helvetia Road, Pukekohe",
  tier="TIER A | Future Urban Zone, GIS point-confirmed | ONE-SHOT",
  headline="The scale lottery: 4.45ha of structure-plan FUZ, lowest execution probability in the pack",
  img1="helvetia1.jpg", img2="helvetia2.jpg",
  facts=[("Land", "4.45 ha with 3-bed house (renovate or demolish) plus sheds"),
         ("Price / method", "By negotiation, no guide. Listed 8 Jul 2021: ~5.3 YEARS, the longest staleness found anywhere in this search"),
         ("Agent", "Barfoot and Thompson Highland Park (Willie Kao / Kitty Long)"),
         ("Zone", "FUTURE URBAN ZONE, stated and confirmed at the GIS point; overlays clear; abuts the Pukekohe residential edge at Birdwood Rd"),
         ("Price rate", "At or under $1.8M this is $40/m2 or less: the largest FUZ quantum conceivably reachable in the band"),
         ("Carry estimate", "House near-worthless, income nil in practice: ~$60-75k per year all-in at 60 percent LVR on a $1.55-1.8M hold")],
  thesis="Ranked below the high-probability plays for one honest reason: a vendor who has refused the market for 5.3 years will probably refuse you too, making this the pack's lowest execution probability. It stays on the list because the prize is the largest - 4.45 structure-plan hectares is genuine development quantum, the kind an aggregator actually buys - and because a single written offer costs nothing but paper. Treat it as the lottery ticket it is: one disciplined number, no negotiation campaign, no emotional investment.",
  risks=["Execution probability is the defining risk: one written offer, then close the file on refusal.",
         "Price as bare land only; the house is a liability.",
         "Parcel-level LIM plus elite-soil/LUC formality check.",
         "Carry on a failed-exit scenario is material; rates assessment first."],
  tactics="One written offer at $1.55M. Absolute cap $1.80M, GST-settled. No chasing, no second call.",
  url="realestate.co.nz/4041906")

P(rank=7, address="18 Riverlea Road, Whenuapai",
  tier="TIER A | Future Urban Zone, GIS-confirmed | BAND-RISK",
  headline="A disciplined lowball that probably loses, entered anyway because losing costs nothing",
  valid_until="2 DECEMBER 2026 (tender close)",
  img1="riverlea18.jpg",
  facts=[("Land", "14,538 m2 with 215 m2 4-bed house"),
         ("Price / method", "TENDER closes 2 Dec 2026 (Colliers). Listed 30 Oct 2026, fresh"),
         ("Zone", "FUTURE URBAN ZONE, stated and GIS-confirmed; flood, grid, SEA clear"),
         ("Band reality", "A livable 4-bed on 1.45ha of confirmed Whenuapai FUZ will probably clear WELL above our $1.8M ceiling at tender - possibly around twice it. Our bid is a disciplined lowball with a real but minority chance in a soft market"),
         ("Income", "Livable house: genuine carry offset if secured"),
         ("Catalysts", "Same Whenuapai certainty stack as rank 1")],
  thesis="The same corridor logic as 2 Rope Road with more land and a house that pays part of the hold. The honest frame, per the adversarial review: our ceiling probably loses this tender. It ships anyway because tender entries cost nothing, spring tenders in a 0-of-7-clearance market sometimes attract no competing bids at all, and if $1.65-1.75M wins it is arguably the best risk-adjusted purchase on this list. Set the number before tender day; do not move it on the day.",
  risks=["Band risk IS the risk: the number is set in advance and never moves.",
         "Airbase noise contour parcel check, as for all Whenuapai.",
         "House condition, insurance, rental appraisal before counting income.",
         "Greenhouses adjacent: check consent history and reverse-sensitivity next door."],
  tactics="Tender $1.65-1.75M, GST-settled. Walk above $1.8M without hesitation. Expect to lose; be positioned to win.",
  url="realestate.co.nz/43160578")

P(rank=8, address="60 Harry Dodd Road, Drury (Bombay side)",
  tier="TIER B | Zone CONDITIONAL: GIS point says Future Urban, unconfirmed at parcel level",
  headline="A possible information edge that is worth exactly nothing until the parcel check lands",
  img1="harrydodd60.jpg",
  img1cap="Listing aerial with boundary; active subdivision earthworks visible beyond the rear boundary",
  facts=[("Land", "1.15 ha with house 'needing significant TLC'"),
         ("Price / method", "By negotiation; CV $1,875,000 (NOTE: above the band); HomesEstimate $1.69-1.9M. Listed 261 days"),
         ("Zone", "UNCONFIRMED. A council GIS point query returns Future Urban, but the listing itself never claims it and rural-road geocoding is imprecise. Until a parcel-level check confirms, this property is priced and ranked as rural adjacency - nothing more"),
         ("Catalysts", "Hero aerial shows active subdivision earthworks directly behind the rear boundary; Drury growth front edging over the hill"),
         ("Carry estimate", "House condition poor; income uncertain: budget ~$55-70k per year all-in until a rental appraisal says otherwise")],
  thesis="The only property where the council's data might say more than the marketing does: the agent sells 'development edging closer' while a GIS point query suggests the zone has already arrived. If - and only if - a parcel-level check confirms Future Urban, this is mispriced information worth acting on quickly. Until then it is a rural lifestyle block whose CV sits above our band, and the plain fact is the deal only works below CV, which 261 days of silence supports.",
  risks=["THE PARCEL-LEVEL ZONE CHECK COMES FIRST: no offer of any kind before it. Confirmation re-prices the deal; failure re-tiers it to adjacency value (around $1.4-1.5M, or walk).",
         "Cap is below CV by design: $1.78M against a $1.875M CV. Do not drift.",
         "Tree line on the western boundary may conceal a watercourse: walk it, flood-viewer it.",
         "House is a liability: land-value negotiation only."],
  tactics="Zone check first. If FUZ confirms: open $1.55M, cap $1.78M GST-settled. If not: re-price to adjacency or walk.",
  url="trademe.co.nz listing 5781944077")

P(rank=9, address="145A Runciman Road, Runciman (Pukekohe)",
  tier="TIER B | Zone CONDITIONAL: Future Urban stated by listing, parcel GIS check pending",
  headline="The weakest evidence stack in the pack, carried by position and eleven stale months",
  img1="runciman145a.jpg",
  facts=[("Land", "1.25 ha bare, rolling pasture"),
         ("Price / method", "By negotiation, no CV or estimate published. Listed ~11 months"),
         ("Zone", "Listing claims 'Future Urban zoning'; the GIS point landed on road reserve so the claim is UNVERIFIED. Parcel-level confirmation is condition one and the price is conditional on it"),
         ("Physical flag", "Photographs show a damp gully / drain line through the middle of the property: walk it and run the council flood viewer before any number is discussed"),
         ("Catalysts", "Pukekohe-Paerata structure plan edge; between the new Paerata station and the Drury South employment front"),
         ("Carry estimate", "Bare land, zero income: ~$45-60k per year all-in at 60 percent LVR, pending the rating valuation")],
  thesis="Ranked last of the zone-conditional pair because everything about it is unverified: the zone claim failed its first GIS attempt on a road-reserve technicality, there is no published CV to anchor against, and the photos show a damp gully that likely explains some of the eleven quiet months. What it has is position - structure-plan edge between a day-one rail station and an employment front - and a vendor whose silence is your leverage. Verify first; the discount only matters if the land is what the listing says it is.",
  risks=["Zone claim unverified: offer strictly conditional on parcel-level FUZ confirmation.",
         "Damp gully / drain line: walk the land, flood-viewer check, price the finding.",
         "No CV published: obtain the rating valuation before anchoring any number.",
         "Zero income; standard bare-land carry."],
  tactics="Open $1.05M. Cap $1.35M, strictly conditional on zone confirmation and flood check.",
  url="trademe.co.nz listing 5656695951")

P(rank=10, address="540 Runciman Road, Runciman (Drury)",
  tier="TIER C | Countryside Living | AUCTION 25 NOV: attend, do not bid",
  headline="A double-contingency play: needs the auction to fail AND the vendor to accept 12.5 percent under CV",
  valid_until="25 NOVEMBER 2026 (auction day; the tactic begins at the pass-in)",
  img1="runciman540.jpg",
  facts=[("Land", "2.16 ha with house; small pond lower on the land"),
         ("Price / method", "AUCTION 25 Nov 2026; CV $2.0M; HomesEstimate $1.71-1.92M. Fresh listing, 28 watchers"),
         ("Zone", "Countryside Living, GIS-confirmed; flood, grid, SEA clear at point. Pond corner needs a flood-viewer look"),
         ("Execution reality", "This profile requires TWO things to go your way: the auction fails (likely in a 0-of-7 market, but 28 watchers is real interest), and the vendor then accepts roughly 12.5 percent below a fresh CV. State both odds honestly"),
         ("Catalysts", "Runciman corridor between Drury South Crossing / Ramarama interchange and Paerata"),
         ("Carry estimate", "House rentable subject to checks: net carry ~$25-45k per year at 60 percent LVR")],
  thesis="The most land the Drury postcode offers inside the band, squeezed between two advancing fronts. The standing rule holds: never bid at auction in this market. The play only exists if the hammer falls on silence - then a motivated post-auction vendor meets a prepared buyer. Countryside Living means the uplift path is the Auckland Deal re-opening southern sequencing rather than existing zoning, and the price must keep reflecting that.",
  risks=["Attend, observe, DO NOT BID. The strategy is the pass-in negotiation or nothing.",
         "Not FUZ: uplift depends on future strategy extension.",
         "Pond and lower land: flood-viewer the wet corner.",
         "Anchor on land value; do not pay for the house."],
  tactics="Post-pass-in offer $1.60-1.75M, GST-settled. If it sells under the hammer, it was never ours.",
  url="trademe.co.nz listing 6203073146")

P(rank=11, address="92 Adams Road, Wainui",
  tier="TIER C | Rural Production | PROMOTED RESERVE: maximum optionality per dollar",
  headline="44.5 hectares at four dollars a square metre in the corridor where rezoning is happening now",
  img1="adams92.jpg",
  facts=[("Land", "44.50 ha rolling-to-steep pasture"),
         ("Price / method", "ASKING $1,800,000 (~$40,000/ha, ~$4/m2). Listed 4 Aug 2022: ~4.3 YEARS on market"),
         ("Zone", "Rural Production, GIS-confirmed 1 Nov 2026; flood, flood-prone, grid (point AND 300m envelope) and SEA all CLEAR - the documented screen that qualified this promotion"),
         ("Catalysts", "Wainui/Milldale expansion direction - the corridor where greenfield rezoning-to-titles is happening NOW (Milldale fast-track 2026, ~9,000-home programme); adjacent the new Wainui golf course"),
         ("Carry estimate", "Grazing lease realistic at this scale: net carry ~$40-60k per year at 60 percent LVR; rates assessment required"),
         ("The honest label", "No zoning, no sequencing signal, steep contour sterilises an unknown fraction: this is a pure optionality purchase, priced accordingly")],
  thesis="Promoted into the vacated slot by the adversarial review on one argument: optionality per dollar. Forty-four hectares at four dollars a square metre, in the only corridor where Auckland greenfield rezoning is converting to titles right now, from a vendor 4.3 years on market. Even if contour sterilises most of it, the effective rate on the usable balance still beats every non-FUZ alternative several times over. It is a 15-year lottery ticket with a grazing income and the pack's largest land quantum by a factor of six - the deliberate opposite of rank 1's small, certain, expensive metres.",
  risks=["Contour is the defect: commission a desktop slope/usable-area assessment before offering; the usable fraction sets the price.",
         "Rural Production with no FUZ and no sequencing: pure policy-and-direction option.",
         "4.3 years stale demands the same why-unsold interrogation as every stale listing here.",
         "Confirm grazing income assumptions and GST status (farmland is commonly plus GST / zero-rated)."],
  tactics="Open $1.45M. Cap $1.70M, GST-settled - the ask has waited four years; it can wait for your number.",
  url="realestate.co.nz/42208670")


# ============ COVER PDF ============
def cover_flow():
    f = []
    f.append(Spacer(1, 6))
    f.append(navy_bar("Auckland Land Bank Options - $1.3M to $1.8M", 17))
    f.append(Spacer(1, 6))
    f.append(Paragraph(mi("**11 verified options | 1 November 2026 | ETR adversarial review applied "
                          "(25 findings; 2 candidates cut; ranking corrected; 1 reserve promoted)**"), body))
    f.append(Paragraph(mi("Method: three parallel market sweeps across the North, Northwest and South "
                          "growth corridors on 1 Nov 2026, explicitly bounded to the $1.3M-$1.8M band, "
                          "evaluated 21+ live candidates; every listing verified active by loading its "
                          "live page; every survivor GIS-checked against Auckland Council's operative "
                          "Unitary Plan services (zone, flood plains, flood-prone areas, National Grid "
                          "corridor, SEA); every listing photo screened for transmission structures. "
                          "The ranking below is the ETR-corrected order, ranked on probability-weighted "
                          "uplift per dollar with execution probability as an input."), body))
    rows = [[Paragraph("<b>#</b>", cellw), Paragraph("<b>Property</b>", cellw),
             Paragraph("<b>Tier / evidence</b>", cellw), Paragraph("<b>Tactic</b>", cellw)]]
    data = [
        ("1", "2 Rope Rd, Whenuapai", "A: FUZ GIS-confirmed", "Open $1.40M, cap $1.75M"),
        ("2", "106 Pukekohe East Rd", "A: FUZ GIS-confirmed", "Open $1.50M, cap $1.75M, hard walk"),
        ("3", "79 Follies Way, Dairy Flat", "A: FUZ + best grid evidence", "Open $1.35M, cap $1.50M"),
        ("4", "7 Bobs Way, Dairy Flat", "A: FUZ GIS-confirmed", "Open $1.10M, cap $1.30M"),
        ("5", "197 Charles Rd, Karaka", "C: no zoning, 61-66% of RV", "Open $1.50M, cap $1.75M"),
        ("6", "130 Helvetia Rd, Pukekohe", "A: FUZ, one-shot lottery", "One offer $1.55M, cap $1.80M"),
        ("7", "18 Riverlea Rd, Whenuapai", "A: FUZ, band-risk tender", "Tender $1.65-1.75M, to 2 Dec"),
        ("8", "60 Harry Dodd Rd, Drury", "B: zone conditional", "Zone check, then $1.55-1.78M"),
        ("9", "145A Runciman Rd", "B: zone conditional", "Conditional $1.05-1.35M"),
        ("10", "540 Runciman Rd", "C: CSL, post-pass-in only", "After 25 Nov auction: $1.60-1.75M"),
        ("11", "92 Adams Rd, Wainui (44.5ha)", "C: promoted reserve", "Open $1.45M, cap $1.70M"),
    ]
    for r in data:
        rows.append([Paragraph(mi(c), cell) for c in r])
    t = Table(rows, colWidths=[W * 0.06, W * 0.32, W * 0.31, W * 0.31], repeatRows=1)
    style = [("BACKGROUND", (0, 0), (-1, 0), NAVY),
             ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
             ("LINEBELOW", (0, 0), (-1, 0), 1.2, NAVY),
             ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
             ("LEFTPADDING", (0, 0), (-1, -1), 6), ("VALIGN", (0, 0), (-1, -1), "TOP")]
    for ri in range(1, len(rows)):
        if ri % 2 == 0:
            style.append(("BACKGROUND", (0, ri), (-1, ri), ALT))
    t.setStyle(TableStyle(style))
    f += [Spacer(1, 4), t, Spacer(1, 10)]

    f.append(Paragraph("Time-critical dates", h3s))
    f.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=5))
    for line in ["18 Nov: 98A Hobson Rd deadline (see annex below) - let it pass unless lifestyle terms are met",
                 "25 Nov: 540 Runciman Rd auction - attend, do not bid; the tactic begins at the pass-in",
                 "2 Dec: 18 Riverlea Rd tender closes - number set in advance, never moved on the day",
                 "By ~7 Nov: accountant's land-taint + CB 6 opinion commissioned, or the November dates are formally let pass"]:
        f.append(Paragraph(mi(line), bullet, bulletText="•"))

    f.append(Paragraph("Excluded during this search (the register, so nothing resurfaces)", h3s))
    f.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=5))
    for line in [
        "**20 Follies Way + the second Follies Way lot (20,100m2) + Lot 2 Bawden Rd DP 466779, Dairy Flat** - Transpower pylons / transmission spans cross those parcels (photo plus GIS-overlay evidenced). Any future candidate with lines over the land is disqualified on sight.",
        "**100 Upper Orewa Rd, Wainui** - vendor purchased Aug 2021 at $3,100,000; anchored roughly double the band.",
        "**12 Cheriton Lane, Drury** - verified over-band (estimate $2.02-2.27M); its Ray White 'sold' flag was the historic 2020 sale.",
        "**68 Potter Rd, Dairy Flat** - fresh campaign against a $2.751M CV, heavily treed; an unverified Feb 2026 $1.85M sale record needs a title check before any engagement.",
        "**175 Oraha Rd, Kumeu** - CUT by review: its 18 Nov deadline lands before the late-2026 flood maps its own condition requires, and its Future Urban suggestion failed GIS (Countryside Living at point). Watch-list: re-engage after the flood maps publish, if still unsold, at adjacency pricing.",
        "**28 Durey Rd, Dairy Flat** - CUT by review: at $73-85/m2 of Countryside Living it is dominated by 7 Bobs Way's $60/m2 of confirmed FUZ in the same corridor.",
        "**1549E Great South Rd, 0 Woodlyn Dr, 44 Belmont Rd, 187 Cameron Town Rd, 65 Haigh Access Rd** - house-dominant value, wet ground, or no catalyst."]:
        f.append(Paragraph(mi(line), bullet, bulletText="•"))

    f.append(Paragraph("Annex: why 98A Hobson Road, Albany is not in this pack", h3s))
    f.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=5))
    f.append(Paragraph(mi(
        "The family's Albany block (2.15ha bare, CV $1.325M, deadline 18 Nov) was examined to the deepest "
        "evidence standard of any property in this engagement, and it fails the land-bank test on the "
        "council's own records: it is zoned Rural - Countryside Living, sits OUTSIDE the Rural Urban "
        "Boundary, and appears in no growth strategy (the council is currently removing future-urban land, "
        "not adding it). The listing's 'further subdivision' potential does not survive the operative rules: "
        "a standalone split of 2.15ha is a NON-COMPLYING activity under chapter E39 (2ha minimum); the only "
        "path is purchasing a transferable rural title for at most ONE extra lot, with thin economics and a "
        "20m esplanade reserve along Paremoremo Creek. It is the residual lot of the vendor's own recent "
        "two-lot subdivision, priced about 14 percent above the only recent bare-land comparable "
        "($1.10M, March 2025, 100 Paremoremo Rd). Its one upside channel - the mid-2027 policy direction "
        "someday opening non-FUZ fringe land - is carried in strictly stronger form by every Future Urban "
        "property in this pack at equal or lower rates per square metre. Whatever 2027 delivers reaches "
        "Future Urban zoned land before it reaches Paremoremo. **If the family wants it as a lifestyle "
        "block, that is a legitimate, separate, separately funded decision: offer $1.10-1.15M, hard ceiling "
        "$1.25M. The 18 November deadline is the vendor's clock, not evidence of demand - in a market "
        "clearing zero of seven auctions, an unsold deadline weakens the vendor, not the buyer.**"), body))
    f.append(Spacer(1, 8))
    f.append(Paragraph(mi(STANDARD_BLOCK), small))
    return f


if __name__ == "__main__":
    cover = OUT / "00_COVER_Ranking_Exclusions_Hobson_Annex.pdf"
    doc_shell(cover, "Land Bank Options - Cover").build(cover_flow())
    print("OK", cover)
    for p in PROPERTIES:
        print("OK", build(p))
