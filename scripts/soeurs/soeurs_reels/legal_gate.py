"""Legal gates (SPEC §3, §6.2 gates 2-6; M1/M2/M3/M9; §8 step 5).

ADVISORY, NOT LEGAL ADVICE. A variant failing any gate is REFUSED, not
rendered. The composite (gate 5) and comment policy are HUMAN sign-offs the
code can only record, never grant.
"""

import re
from datetime import date

# SPEC §3.2 prohibited phrasing — on-screen text, captions, hashtags, replies.
# Substring match, case-insensitive. House names are checked from the movie
# definition's own list so future scents extend it without a code change.
PROHIBITED_SUBSTRINGS = [
    "dupe of", "dupe for", "#perfumedupe",
    "smells exactly like", "identical to", "an exact match", "same as",
    "your designer scent",
    "lasts 12 hours", "12-hour", "12 hour", "10-hour", "10 hour",
    "lasts all day", "all-day wear", "24 hours", "24-hour",
    "lasts longer than", "outlasts", "stronger than", "more concentrated than",
    "hypoallergenic", "clinically", "dermatologist", "gentle on sensitive skin",
    "guess which designer", "which designer",
    "was $",  # fake strike-through pricing
]
PROHIBITED_PATTERNS = [
    re.compile(r"#\w*dupe", re.I),           # any *dupe hashtag
    re.compile(r"\bnew\b|\bjust launched\b", re.I),  # only with valid_until (M9)
]
TIME_DECAY_PATTERN = PROHIBITED_PATTERNS[1]


class LegalRefusal(SystemExit):
    pass


def scan_text(text, house_names=()):
    """Return list of violations in a text token (empty = clean)."""
    hits = []
    low = text.lower()
    for s in PROHIBITED_SUBSTRINGS:
        if s in low:
            hits.append(f"prohibited phrase: {s!r}")
    if PROHIBITED_PATTERNS[0].search(text):
        hits.append("prohibited *dupe hashtag")
    for name in house_names:
        if name and name.lower() in low:
            hits.append(f"house name present: {name!r}")
    return hits


def check_token(token, registry, publish_target, today=None):
    """Gates 2 and 4 for one text token dict:
    {text, claim_key?, valid_until?}."""
    today = today or date.today()
    violations = scan_text(token["text"], registry.get("_house_names", ()))

    # M9 expiry gate: time-decaying words need a future valid_until
    if TIME_DECAY_PATTERN.search(token["text"]):
        vu = token.get("valid_until")
        if not vu:
            violations.append("time-decaying word without valid_until (M9)")
        elif date.fromisoformat(vu) < today:
            violations.append(f"valid_until {vu} has passed (M9)")

    # M1: CLAIM-tier tokens need all three orthogonal gates
    key = token.get("claim_key")
    if key:
        entry = registry.get(key)
        if not entry:
            violations.append(f"claim_key {key!r} not in substantiation registry")
        elif entry.get("tier") == "claim":
            if not entry.get("substantiation_ref"):
                violations.append(f"{key}: no dated substantiation_ref (s12A)")
            if entry.get("misleading_review") != "signed":
                violations.append(f"{key}: misleading_review not signed (s9/s13)")
            if (publish_target == "paid"
                    and entry.get("platform_ad_status") != "paid_eligible"):
                violations.append(f"{key}: not paid_eligible on platform")
        elif not entry.get("usable", False):
            violations.append(f"{key}: registry marks it unusable")
    return violations


def check_scent(scent):
    """Gate 3 (M3): every scent name needs a dated tm_clearance_ref."""
    if not scent.get("tm_clearance_ref"):
        return [f"scent {scent['name']!r}: no tm_clearance_ref "
                "(IPONZ check + free-riding screen, SPEC M3)"]
    return []


def check_variant(tokens, scent, registry, publish_target, allow_draft=False):
    """Run gates 2-4 + 6. Returns [] or raises LegalRefusal.
    allow_draft: tm-clearance pends may pass for DRAFT-watermarked internal
    renders only — everything else still refuses."""
    violations = []
    for t in tokens:
        violations += check_token(t, registry, publish_target)
    scent_v = check_scent(scent)
    if not allow_draft:
        violations += scent_v
    if publish_target == "paid":
        violations += [v for v in scent_v if v not in violations]
    if violations:
        raise LegalRefusal("LEGAL GATE REFUSED:\n  - " + "\n  - ".join(violations))
    return scent_v  # pending items the draft must surface


def composite_signed(reel_def):
    """Gate 5 (M2): human whole-reel sign-off. Code records, never grants."""
    return reel_def.get("composite_claim_review") == "signed"
