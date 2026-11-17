export const meta = {
  name: 'etr-34-follies-valuation',
  description: 'ETR agentic valuation of 34 Follies Way, Dairy Flat — grid-corridor land-bank lot',
  phases: [
    { title: 'Research', detail: '5 parallel finders: listing/identity, GIS+grid, comps, transmission-impact, planning' },
    { title: 'Value', detail: 'valuation synthesis from all research' },
    { title: 'Verify', detail: '3-lens adversarial review of the valuation' },
  ],
}

const CTX = `
CONTEXT (established facts — do not re-derive, but DO verify anything marked unverified):
- Subject: 34 Follies Way, Dairy Flat, Auckland, NZ. ~2.009 ha (20,090 m²) bare freehold land. One of Lots 5-18 DP 512543 (Stage 2 of the Follies Way subdivision by Kim Valerie Campbell & Sanmei Li, titles issued Nov 2017; Stage 1 = Lots 1-4 DP 504817, May 2017; parent CT 688152). Follies Way is a PRIVATE right-of-way off Bawden Road, Dairy Flat, managed by Follies Way Management Ltd (mandatory share, minimum levy $2,000+GST/yr, registered encumbrances). Land covenants from instrument 10780745.5 (as varied by 10824937.1) bind all lots (text not yet obtained). Currently marketed by Ray White Carpenter Realty (agent Steven Fang, assistant Rossy Qiang 027 888 8656), property-info email sent 13 Nov 2026 with title + LIM.
- Zone: Future Urban Zone (FUZ), Auckland Unitary Plan. Dairy Flat urbanisation is DEFERRED long-term (Future Development Strategy ~2050+; Watercare servicing 20+ years out). Swing factors: mid-2027 national planning direction under the new planning legislation; Albany-Milldale rapid transit corridor geography; PC103 private-plan-change precedent.
- Grid: A Transpower transmission line + pylon crosses the Follies Way block mid-block. Auckland Council GIS showed 2 National_Grid_Corridor_Overlay features across the block (verified 1 Nov 2026). 20 Follies Way (20,024 m²) and a second ~20,100 m² "twin" lot were ELIMINATED from a prior shortlist because pylons/lines cross those parcels (photo-evidenced). 79 Follies Way (17,202 m², asking $1,590,000 = $92/m², ~6 months listed) is grid-clear. 34 Follies Way at 20,090 m² may BE the previously seen 20,100 m² twin (old Trade Me listing 5886963422, "PRICE DROPPED", PBN) — confirm or refute.
- Street/area price intel (1 Nov 2026): 20 Follies Way PBN "bank says MUST SELL" ~278 days on market (Harcourts, Trade Me 5753048100); 44 Follies Way 1.01 ha CV $1.275M reportedly sold (status was conflicted); 7 Bobs Way Dairy Flat cheapest FUZ ~$60/m²; historical Dairy Flat englobo benchmark ~$127/m²; current Dairy Flat FUZ asks $60-92/m².
- Buyer mandate: pure LAND BANK, budget <=$1.5M, 7-15 yr hold, NO development, value = rezoning/urbanisation option. Standing family rule (1 Nov 2026): a pylon-crossed Follies lot may be revisited ONLY at <=$1.0M AND with a surveyor corridor map showing >=70% of the parcel clean of the National Grid corridor.
Today is 15 Nov 2026. Return RAW findings as instructed — your final text is data for an orchestrator, not a human-facing message. Cite a source URL for every externally-sourced claim. Use ToolSearch to load WebSearch/WebFetch; use Bash curl for ArcGIS REST queries if needed.`

const FINDER_SCHEMA = {
  type: 'object',
  required: ['summary', 'facts', 'gaps'],
  properties: {
    summary: { type: 'string', description: '5-10 sentence synthesis of what was found' },
    facts: { type: 'array', items: { type: 'object', required: ['claim', 'source', 'confidence'], properties: {
      claim: { type: 'string' }, source: { type: 'string', description: 'URL or method' },
      confidence: { type: 'string', enum: ['verified', 'probable', 'unverified'] } } } },
    gaps: { type: 'array', items: { type: 'string' }, description: 'what could not be established and why' },
  },
}

const FINDERS = [
  { key: 'listing', prompt: `${CTX}
TASK — LISTING & IDENTITY. Establish: (1) The live listing for 34 Follies Way, Dairy Flat — search Ray White (rwcarpenterrealty.co.nz, raywhite.co.nz), Trade Me Property, OneRoof, realestate.co.nz, homes.co.nz. Is it active, what method (PBN/asking/auction/tender), what price indication, days on market, which agency, listing ID. Check whether old Trade Me listing 5886963422 (the 20,100 m² "twin") is the same property. (2) Identity: which Lot number on DP 512543 is 34 Follies Way, and its title/CT identifier (candidates 801781-801794) — try homes.co.nz / OneRoof / propertyvalue.co.nz / Auckland Council property-rates lookup (aucklandcouncil.govt.nz rates search shows legal description). (3) Rating valuation: current CV/RV (land value, improvements, capital value) and valuation date. (4) Sale history of 34 Follies Way: what did it last sell for and when (the subdivider sold lots ~2017-2019). (5) Listing history: prior campaigns, price drops, agency changes — a lot relisted across agencies for a year+ is distress evidence. Report every price signal with its date.` },
  { key: 'gis', prompt: `${CTX}
TASK — GIS, GRID GEOMETRY & WHERE THE CABLE GOES. Establish: (1) Exact location/geometry of 34 Follies Way parcel — use Auckland Council GeoMaps / ArcGIS REST services (try https://services1.arcgis.com/n4yPwebTjJCmXB6W/arcgis/rest/services — Unitary Plan Base Zone + overlays incl. National_Grid_Corridor_Overlay; also mapservices.aucklandcouncil.govt.nz) and LINZ data (DP 512543 lots). Confirm FUZ at the parcel. (2) The transmission line: identify WHICH Transpower line crosses the Follies Way block — line name/code, voltage, circuits, and its route (which substations it connects, i.e. where the cable is coming from and going to — likely between Albany and Silverdale substations feeding north; verify via Transpower network maps gis.transpower.co.nz or openinframap.org / OpenStreetMap power layer). (3) Geometry vs the subject: does the line / National Grid Corridor Overlay CROSS 34 Follies Way, clip a corner, or only pass nearby ("not far away")? Estimate distance from parcel boundary to the nearest conductor centreline and whether any pylon stands on the parcel. State coordinates you queried and what returned. Compare with neighbours (20 Follies crossed, 79 clear). (4) Rules: Auckland Unitary Plan National Grid Corridor Overlay provisions (D26) + NES Electricity Transmission Activities — National Grid Yard widths (e.g. 12 m either side of centreline for 110kV+, 12 m around support structures), what is prohibited/restricted under it (dwellings, sensitive activities, subdivision controls in the corridor), and what remains permitted (grazing, pasture). (5) Any other overlay hits at the parcel: flood plain, flood prone, SEA, airfield (Dairy Flat airfield is nearby — check its protection surfaces), quarry buffer (Stevenson? no — check), stormwater. Output a clear verdict: CROSSED / CLIPPED / ADJACENT-ONLY with estimated % of parcel inside the corridor.` },
  { key: 'comps', prompt: `${CTX}
TASK — COMPARABLE SALES & STREET EVIDENCE. Establish with dates and sources: (1) Follies Way transaction history: every lot sale you can find 2017-2026 (homes.co.nz / OneRoof / propertyvalue / qv.co.nz show sold prices) — especially 44 Follies Way (did it sell, when, how much vs CV $1.275M), 20 Follies Way (sold or still listed? price), 79 Follies Way (still asking $1.59M?), and the original 2017-2019 subdivider sell-down prices of Lots 5-18 (what did buyers pay Campbell/Li per lot — this anchors what TODAY's vendors paid). (2) 34 Follies Way specifically: its last sale price and date, and current CV. (3) Dairy Flat / Bawden Rd / Bobs Way / Postman Rd / Green Rd FUZ land sales 2024-2026, $/m², distinguishing: bare lifestyle lot in FUZ vs englobo farmland; note any pylon/line-affected sale and its discount vs clean neighbours (Follies Way itself is a natural experiment: pylon lots vs clear lots, same street, same zone). (4) Market state: Dairy Flat / Rodney lifestyle-land clearance 2026 — are things selling, at what % of CV? Any mortgagee/bank-forced sales on the street ("bank says must sell" was live Nov 2026). (5) CVs of several Follies Way lots for a CV-ratio cross-check (homes.co.nz estimates included but labelled as estimates). Build a small table in your summary: address | size | event (sold/ask/CV) | $ | $/m² | date | grid status.` },
  { key: 'impact', prompt: `${CTX}
TASK — HOW TRANSMISSION-LINE PROXIMITY PRICES INTO LAND SALES. Research and synthesize, NZ-first then international: (1) Valuation practice & empirical studies on high-voltage transmission lines and land value: typical % diminution for (a) line CROSSING a parcel with a pylon on it, (b) line crossing without a structure, (c) line adjacent/visible only (within ~100-300 m), for rural-residential/lifestyle land and for development land. Look for NZ sources: Transpower-commissioned valuation studies, NZ Institute of Valuers / Property Institute papers, Land Valuation Tribunal decisions, academic (e.g. studies on pylon proximity Auckland/Waikato), and credible AU/US/UK meta-analyses. Give ranges, not a single number, and separate perception/amenity discount from the hard yield loss. (2) The FUTURE-URBAN twist: for land banked for urbanisation, the National Grid Corridor is a permanent yield haircut — buildings for sensitive activities can't go in the National Grid Yard and subdivision inside the corridor is restricted, so the sterilised strip earns rural value forever while the rest earns urban value. Explain how developers price corridor strips in masterplans (roads/reserves/stormwater placed under lines = partial value recovery — find examples e.g. Hobsonville, Flat Bush, Milldale where transmission corridors became linear parks/roads). (3) Transpower relationship: for an EXISTING line there is no ongoing compensation to the owner (verify), landowner rights (injurious affection historic only), Transpower access rights to spans/towers, undergrounding possibility (who pays — effectively never for 220kV). (4) Liquidity effect: evidence that line-crossed lots sit on market far longer / sell to a thinner buyer pool (bank-forced sale on this exact street after 278+ days is one datum). (5) Practical pricing heuristic used by valuers for partially-affected parcels (e.g. affected area at 20-50% of clean value + 0-10% blanket stigma on remainder) — find support for or against such decomposition.` },
  { key: 'planning', prompt: `${CTX}
TASK — PLANNING & SEQUENCING REFRESH (light but current). Establish as of Nov 2026: (1) Dairy Flat FUZ status: Auckland Future Development Strategy timing for Dairy Flat/Silverdale West, any change since mid-2026; Watercare servicing position. (2) The new resource-management/planning legislation: status of the mid-2027 national direction work, anything announced that changes live-zoning obligations for future-urban land. (3) Albany-Milldale / North rapid transit corridor: current designation/route protection status near Dairy Flat, any 2026 announcements (Supporting Growth / NZTA). (4) PC103 or other private plan changes near Dairy Flat: outcomes and what they imply for queue-jumping probability. (5) Dairy Flat structure plan work: has Auckland Council started any structure planning for this FUZ area; Silverdale West Dairy Flat Industrial area status. (6) Milldale/Milldale-south expansion and Pine Valley/Wainui progression — how fast is urbanisation actually marching toward Bawden Rd. Conclude: probability-weighted view of rezoning inside 7-15 yrs (the buyer's hold window) and what event would move it.` },
]

phase('Research')
log('Fanning out 5 research agents on 34 Follies Way')
const research = await parallel(FINDERS.map(f => () =>
  agent(f.prompt, { label: `research:${f.key}`, phase: 'Research', schema: FINDER_SCHEMA })
    .then(r => ({ key: f.key, ...r }))
))
const got = research.filter(Boolean)
log(`Research complete: ${got.length}/5 agents returned`)

phase('Value')
const SYNTH_SCHEMA = {
  type: 'object',
  required: ['market_value_low', 'market_value_base', 'market_value_high', 'mandate_open_offer', 'mandate_cap', 'per_m2_logic', 'adjustments', 'conditions', 'kill_criteria', 'narrative'],
  properties: {
    market_value_low: { type: 'number' }, market_value_base: { type: 'number' }, market_value_high: { type: 'number' },
    mandate_open_offer: { type: 'number', description: 'opening offer for the land-bank buyer' },
    mandate_cap: { type: 'number', description: 'walk-away cap for the land-bank buyer' },
    per_m2_logic: { type: 'string', description: 'the $/m2 build-up: clean benchmark, affected-area treatment, stigma' },
    adjustments: { type: 'array', items: { type: 'object', required: ['factor', 'direction', 'magnitude', 'basis'], properties: { factor: { type: 'string' }, direction: { type: 'string', enum: ['up', 'down'] }, magnitude: { type: 'string' }, basis: { type: 'string' } } } },
    conditions: { type: 'array', items: { type: 'string' }, description: 'DD conditions before any offer' },
    kill_criteria: { type: 'array', items: { type: 'string' } },
    narrative: { type: 'string', description: '1-2 paragraphs: the valuation story a valuer would sign' },
  },
}
const synthesis = await agent(`${CTX}
TASK — VALUATION SYNTHESIS for 34 Follies Way, Dairy Flat (2.009 ha bare FUZ, private-way lot, possible National Grid corridor exposure).
You are given the full research JSON from 5 specialist agents below. Build a defensible valuation:
1. Establish the CLEAN comparable benchmark $/m² for a ~2 ha bare FUZ lifestyle lot on this street/area today (use street evidence first: 79 Follies ask $92/m² unsold ~6 months = ceiling, actual SOLD prices = floor; CV ratios; wider Dairy Flat sales).
2. Apply the grid-corridor treatment per the GIS agent's CROSSED/CLIPPED/ADJACENT verdict and the impact agent's diminution ranges — affected strip valued at its sterilised value + stigma on remainder. Show the arithmetic. If geometry is uncertain, run the valuation at 2-3 geometry scenarios and say which the evidence favours.
3. Sanity-check against: what the vendor likely paid (2017-19 sell-down), CV, the street's distress signals, and the fact the agent is now emailing cold leads full title packs (motivated vendor behaviour).
4. Produce: market value low/base/high, then the LAND-BANK buyer's open offer and hard cap honouring the standing family rule (pylon-crossed => only <=$1.0M with >=70% clean survey; adjacency-only => price against 79 Follies minus a relative-value margin). The buyer should never be the highest-conviction bidder on a corridor lot in a street with distressed clean alternatives.
5. Conditions precedent (title/covenant 10780745.5 text, surveyor corridor map, LIM review, Follies Way Mgmt levies/arrears, GST status) and kill criteria.
RESEARCH INPUT:
${JSON.stringify(got, null, 1).slice(0, 60000)}
`, { label: 'valuation-synthesis', phase: 'Value', schema: SYNTH_SCHEMA, effort: 'high' })

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object',
  required: ['verdict', 'findings'],
  properties: {
    verdict: { type: 'string', enum: ['SOUND', 'ADJUST', 'REJECT'] },
    findings: { type: 'array', items: { type: 'object', required: ['severity', 'title', 'detail', 'fix'], properties: { severity: { type: 'string', enum: ['BLOCKING', 'MAJOR', 'MINOR'] }, title: { type: 'string' }, detail: { type: 'string' }, fix: { type: 'string' } } } },
  },
}
const LENSES = [
  { key: 'comps-anchoring', brief: 'Attack the comparable-evidence chain: are "comps" actually asks not sales? Is the clean benchmark anchored on unsold asking prices? Is the vendor-cost anchor right? Is any listing assumed active without verification (hard rule: never cite an unverified listing as active)? Does the arithmetic foot? Would a registered valuer sign the per-m2 build-up?' },
  { key: 'grid-geometry', brief: 'Attack the grid/geometry claims: is the CROSSED/CLIPPED/ADJACENT verdict actually evidenced at parcel level or inferred from street-level data? Are the National Grid Yard widths and AUP D26 rules stated correctly? Is the % -affected estimate honest about uncertainty? Is the discount double-counted (yield haircut AND stigma on the same strip)? Does the valuation change sign under the worst plausible geometry?' },
  { key: 'thesis-liquidity', brief: 'Attack the investment thesis: with Dairy Flat sequencing ~2050+ and the buyer hold 7-15 yrs, is ANY price defensible vs the grid-clear alternative at 79 Follies or cheaper Dairy Flat FUZ (7 Bobs ~$60/m2)? Is the opportunity-cost comparison priced in? Exit liquidity for a corridor lot? Does the recommendation violate the standing family rule or the <=$1.5M mandate? Is the buyer being nudged to pay for optionality the corridor permanently impairs?' },
]
const verifications = await parallel(LENSES.map(l => () =>
  agent(`${CTX}
TASK — ADVERSARIAL VERIFICATION (${l.key} lens). Try hard to REFUTE or force adjustment of the valuation below. ${l.brief}
Default to ADJUST if any material weakness survives scrutiny. Be specific: every finding needs a concrete fix.
VALUATION UNDER REVIEW:
${JSON.stringify(synthesis, null, 1).slice(0, 30000)}
SUPPORTING RESEARCH SUMMARIES:
${JSON.stringify(got.map(g => ({ key: g.key, summary: g.summary, gaps: g.gaps })), null, 1).slice(0, 20000)}
`, { label: `verify:${l.key}`, phase: 'Verify', schema: VERDICT_SCHEMA, effort: 'high' })
    .then(v => ({ lens: l.key, ...v }))
))

return { research: got, synthesis, verifications: verifications.filter(Boolean) }