#!/usr/bin/env python3
"""Write LISTING_COPY.md + INFO_NEEDED.md for the Truecoat FB Marketplace kit.
GENERAL painting business (interior + exterior). Copy kept legal-safe per the ETR Fair Trading Act audit."""
import os
KD = os.path.expanduser("~/Desktop/Painting/Truecoat - Facebook Marketplace Kit")
FENCE = "```"

profile_name = "Truecoat — Auckland Painters"
page_bio = ("Truecoat is a local Auckland painting crew — interior and exterior. Repaints, new builds, "
            "renovations and light-commercial work. Written prep + paint scope to the AS/NZS 2311 standard, "
            "quality trade paints, a workmanship re-do guarantee in writing, a tidy crew, and free no-obligation "
            "quotes. Servicing [SUBURBS]. Message us your suburb + a photo of the job to book a free quote.")
listing_title = "House Painters Auckland | Interior & Exterior | Free Quotes"
listing_description = """🏠 AUCKLAND PAINTERS — INTERIOR & EXTERIOR

Freshening up inside, repainting the exterior, or finishing a new build or reno? 🎨 Truecoat is a local Auckland crew that does it properly, start to finish — walls and ceilings through to weatherboards and roofs.

✅ WHAT WE PAINT
🖌️ Interior repaints — walls, ceilings, doors & trim
🏡 Exterior & weatherboard repaints
🧱 Plaster, fibre-cement & brick exteriors
🪟 Fascia, soffits, gutters & trims
🚪 Fences, decks & doors
🏗️ New builds & renovations
🏢 Light-commercial & rental turnovers

🔧 THE TRUECOAT WAY
📋 A written prep + paint scope to the AS/NZS 2311 painting standard — so you know exactly what you're getting
🧼 Proper prep first: fill, sand, wash & prime (prep is what makes paint last)
🪣 Quality trade paints, backed by the paint manufacturer's product warranty
🤝 Our own workmanship re-do guarantee — if something's not right, we come back and put it right
🧹 Tidy, respectful crew — we protect your furniture & floors and clean up every day

💬 FREE, no-obligation quotes. No pressure, no surprises.

📩 Message us your suburb and what you'd like painted — inside, outside, or both — and we'll book you in for a free on-site quote. ☀️

Truecoat — Auckland painters. Get it done right the first time."""
short_description = ("Local Auckland painters — interior & exterior. Repaints, new builds & renos, done with proper "
                     "prep, quality trade paint, a written workmanship re-do guarantee & free no-obligation quotes. "
                     "Message us your suburb for a free on-site look.")
first_reply_template = """Hi 👋 thanks for reaching out to Truecoat! Happy to sort you a free, no-obligation quote.

To point you in the right direction, could you let me know:
1️⃣ What suburb are you in?
2️⃣ Is it interior, exterior, or both?
3️⃣ Roughly what's involved? (e.g. a few rooms / whole house / weatherboards / fence & deck)
4️⃣ Roughly when are you hoping to get it done?

A couple of photos of the job help heaps if it's easy 📷. From there I'll pop out for a quick free on-site look and give you a written quote — no pressure at all. 😊

Cheers,
Truecoat — Auckland Painters"""
offer_headline = "TRUECOAT FOUNDATION CUSTOMERS — our first Auckland jobs, interior & exterior"
offer_terms = """We're a new Auckland painting business and we're upfront about it. To build our name the right way, we're taking on a limited number of "Foundation Customer" jobs — interior or exterior. Foundation customers pay a fair, standard price — no discount gimmicks — and get looked after as one of our very first jobs.

FOUNDATION CUSTOMER GETS (genuine add-ons, not price cuts):
• A free colour consultation to help you choose the right palette
• Priority booking
• Your written quote locked in — no price rise before we start (as long as the agreed scope doesn't change)
• A full written AS/NZS 2311 prep + paint scope, so you know exactly what's being done
• Our written workmanship re-do guarantee (term stated in your written quote)
• Named as one of our founding Auckland customers

ALL WE ASK IN RETURN:
• Written consent to take before-and-after photos of the work for our portfolio (you can decline photos)
• An honest review once the job's done — a request, never a requirement

HONEST FINE PRINT:
• The Foundation intake is a genuine limit — once those spots are booked, the offer closes.
• Applies to interior or exterior painting within our Auckland service area.
• The perks are for booking early — they do NOT depend on you leaving a review, and never on the review being positive.
• Free quote means exactly that — no cost, no obligation.
• We don't claim reviews, ratings, memberships or accreditations we haven't earned yet.

[GATE BEFORE PUBLISHING: confirm the real capacity number, confirm the workmanship guarantee term and put it in writing, and define the Auckland service-area boundary. No dollar figures anywhere in public copy.]"""

lc = f"""# Truecoat — Facebook Marketplace Listing Copy

General Auckland painting business (interior + exterior). Copy-paste ready and legal-safe under the NZ Fair Trading Act **provided** you first confirm the gated items in `INFO_NEEDED.md` (insurance, guarantee terms, name clearance). Fill every `[BRACKET]` before posting.

---

## Facebook Page — profile name
> {profile_name}

## Facebook Page — About / bio
> {page_bio}

---

## Marketplace listing — TITLE
> {listing_title}

## Marketplace listing — DESCRIPTION (paste as-is)
{FENCE}
{listing_description}
{FENCE}

## Short description (for community groups / one-liner)
> {short_description}

---

## First-reply / DM script (send the moment someone messages)
{FENCE}
{first_reply_template}
{FENCE}

> **Speed wins.** Marketplace shoppers message several painters at once — reply within minutes, qualify with the script, then book the free on-site look and grab their mobile.

---

## Launch offer

**{offer_headline}**

{offer_terms}
"""
open(os.path.join(KD, "LISTING_COPY.md"), "w").write(lc)
print("wrote LISTING_COPY.md (general)")

must_have = [
 "Business mobile number [MOBILE] — the exact line that goes in every listing and will be answered during quoting hours (Marketplace leads die in minutes; decide who owns the phone)",
 "Business email [EMAIL] — dedicated address (e.g. quotes@ / hello@), not a personal Gmail if possible",
 "Public liability insurance — CONFIRMED ACTIVE with insurer, policy number, cover amount and Certificate of Currency on file (and, for exterior/two-storey work, that it covers working at heights). Until bound, the word 'insured' and any near-synonym is deleted from ALL copy",
 "Workmanship re-do guarantee — exact written terms: duration (e.g. 12/24 months), what's covered (application/workmanship defects) vs excluded (substrate failure, moisture ingress, pre-existing rot, customer-caused damage), what 're-do' means. Do not publish any 'guarantee' wording until terms exist in writing and can be honoured",
 "AS/NZS 2311 — confirm the crew genuinely writes and works to this standard so the headline claim is defensible",
 "Exact service-area suburbs [SUBURBS] — the precise Auckland zones you'll travel to and quote in, and the outer boundary of free quotes",
 "Company/trading structure — is Truecoat registered (Ltd) or sole trader/partnership? No 'Truecoat Ltd' in copy unless it exists",
 "'Truecoat' name clearance — Companies Register + IPONZ trade-mark search (note: 'TrueCoat' is an existing Graco sprayer product line — different class, but check for friction), plus the logo mark",
 "Interim photo policy — do ANY real before/after jobs exist (interior or exterior)? If none: NO stock, AI-generated results, or competitors' photos passed off as Truecoat work. Use clearly-generic brand/process imagery not captioned as 'our work' until job #1 is shot",
 "Facebook Business Page live and populated — logo profile image, cover, About, service area, hours, Message button — before the first listing goes up",
 "Reviews — confirm there are genuinely NONE yet; ship with zero review/star/'trusted by X'/company-experience claims. Reviews from any other business/trade cannot be reworded as Truecoat testimonials",
 "Launch-offer specifics — the real Foundation-customer capacity number, and confirm the free no-obligation quote has no hidden call-out fee",
]
nice = [
 "Confirm which trade paint(s) you'll actually buy and apply (e.g. Dulux / Resene trade-line) — only then may brand names go into copy; and verify the exact manufacturer product-warranty terms so you don't imply a warranty you can't pass on",
 "Logo files — final mark (T + paint-drop) in transparent PNG + SVG, with True Blue #1E3EB4 locked as the hex",
 "Google Business Profile — set up as a service-area business; for a tradie, Google reviews matter more long-term than FB",
 "NZBN + GST registration status — for quotes/invoices (not public copy)",
 "0800 vanity number — only if a provider-confirmed, diallable number is secured; do not print any mnemonic until confirmed",
 "Van signage / uniform / branded-gear photos — strong 'tidy professional crew' proof once kitted out",
 "Simple one-page landing site as a stronger quote-request link target",
 "Stated quote turnaround ('we'll come look within X days') once a realistic promise is set",
 "Payment methods accepted — for the close stage, not the public listing",
 "Decide the marketing lead: even as a general painter, pick ONE hook per listing (e.g. interior repaints in one, exterior in another) so each ad has a clear message — 'we do everything' converts worse than a specific hook",
]
safe = [
 "Free, no-obligation quote (as long as it is genuinely free — no call-out fee, no obligation to sign)",
 "Auckland-based / locally owned and operated (if true)",
 "Interior & exterior painting — repaints, new builds, renovations, light-commercial (scope language)",
 "We work to / follow a written AS/NZS 2311 prep-and-paint scope (method claim — NOT 'certified to AS/NZS 2311')",
 "Written workmanship re-do guarantee — if our work fails we come back and put it right (only once terms are in writing and can be honoured; framed as EXTRA to the customer's Consumer Guarantees Act rights, never as granting a right they already have)",
 "Quality trade-line paints, backed by the manufacturer's own product warranty subject to their terms (no year figure; Truecoat does not back it)",
 "Careful, tidy treatment of your property — drop sheets, furniture & floor protection, daily clean-up (a conduct promise you control; NOT 'insured')",
 "Booking now for the coming season (factual scheduling)",
 "Ordinary puffery — 'we take pride in a sharp finish', 'your place, done right', 'get it done right the first time'",
]
avoid = [
 "'Insured' / 'fully insured' / any insurance reference — until a policy is bound and in force",
 "'Dulux Accredited' / 'Resene Eco.Decorator' and any manufacturer badge or logo — protected memberships not yet held",
 "'Master Painters' / 'MPNZ member' / the MP logo / the Master Painters Guarantee — not a member yet",
 "Any reviews, star ratings, testimonials, 'trusted by X homeowners', 'our happy customers' — none genuine exist yet; none borrowed, bought or invented",
 "'20 years experience' / 'established' / 'reputable' / 'trusted' as a company track-record — the business is brand new",
 "'Specialists' / 'experts' as an earned credential — use scope language ('we do / what we paint') instead",
 "'Licensed painters' / 'licensed and qualified' — painting is not a licensed trade in NZ",
 "Specific manufacturer-warranty years ('15-year guarantee') or 'guaranteed to last X years' — until confirmed for the exact product/system",
 "Superlatives/comparatives — 'best', 'cheapest', '#1', 'unbeatable'",
 "Any price, rate, or 'from $X' in public copy",
 "Any mention of a parent/group/other company — Truecoat is fully independent",
 "Any photo passed off as 'our work' when it isn't (imagery is a representation under FTA s9); AI-generated results and competitors' shots are out",
 "Fake scarcity / countdowns from a business with no bookings — only a real, honoured Foundation cap is allowed",
 "Weathertightness / structural / leak / rot-repair claims — painting is a coating, not a repair",
]

def bl(items, n=False):
    return "\n".join(f"{i}. {x}" if n else f"- {x}" for i, x in enumerate(items, 1))

inf = f"""# Truecoat — Info Needed Before You Go Live

General Auckland painting business (interior + exterior). This is the gate: settle the **Must-have** items before the first listing goes up; the compliance audit tells you exactly which wording is safe vs off-limits for a brand-new business.

## 🔴 MUST-HAVE before going live
{bl(must_have, n=True)}

## 🟡 Nice-to-have (do soon, not blocking)
{bl(nice, n=True)}

---

## ✅ SAFE to say now (legal-safe for a brand-new painter)
{bl(safe)}

## ⛔ DO NOT say until verified (NZ Fair Trading Act risk)
{bl(avoid)}

---

## ⚠️ Design tiles that carry a gated claim
- **Why-us tile** lists *"Written workmanship re-do guarantee"* — only publish once the guarantee term is written down and you can honour it (Must-have #4). If it's not ready, tell me and I'll drop that line and re-render.
- No tile says *"insured"* — that stays out until your policy is bound (Must-have #3).
- **Before/After tile** is a TEMPLATE — never publish it with stock or another painter's photos; swap in a real completed Truecoat job (interior or exterior).
- The **offer** copy has a `[GATE BEFORE PUBLISHING]` note — confirm the real Foundation number, the guarantee term, and the service-area boundary before it goes live.
"""
open(os.path.join(KD, "INFO_NEEDED.md"), "w").write(inf)
print("wrote INFO_NEEDED.md (general)")
