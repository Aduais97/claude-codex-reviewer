"""Palette tokens + contrast checker (SPEC §4.2, M8).

All hexes are DIRECTIONAL approximations sampled from AI-degraded frames.
PROVISIONAL stays True until resample_from_still() runs on the real 12MP
still — hero/paid renders are blocked while it is True.
"""

PROVISIONAL = True   # M8: flips only after resampling from the real still

TOKENS = {
    "carton_cream":        "#ECE0D0",
    "paper_warm_white":    "#F6EFE4",
    "rose_gold":           "#C89A76",   # accent only — NEVER body type on cream
    "rose_gold_highlight": "#F3D9C4",
    "bronze":              "#7A4E2C",
    "firelight_amber":     "#C07A34",   # type only on ember, large, with glow
    "ember_espresso":      "#2A1206",   # dark anchor
    "cocoa":               "#33251C",   # primary text on light
    "text_on_dark":        "#F1E7D8",   # primary text on ember
    "text_muted":          "#8A7A6A",
    "marshmallow_pink":    "#E8CBD0",   # LOW confidence — confirm from real still
}


def rgb(token):
    h = TOKENS[token].lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _lum(c):
    def chan(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (chan(v) for v in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(token_a, token_b):
    la, lb = sorted((_lum(rgb(token_a)), _lum(rgb(token_b))), reverse=True)
    return (la + 0.05) / (lb + 0.05)


# The codified legibility pairs (SPEC §4.2). rose_gold-as-type on cream is the
# known failure (~1.9:1) and is asserted BANNED, not asserted passing.
LEGIBLE_PAIRS = [("cocoa", "carton_cream"), ("text_on_dark", "ember_espresso")]
BANNED_TYPE_PAIRS = [("rose_gold", "carton_cream")]


def check_legibility():
    problems = []
    for fg, bg in LEGIBLE_PAIRS:
        if contrast(fg, bg) < 4.5:
            problems.append(f"{fg} on {bg} = {contrast(fg, bg):.1f}:1 (<4.5)")
    for fg, bg in BANNED_TYPE_PAIRS:
        if contrast(fg, bg) >= 4.5:
            problems.append(f"{fg} on {bg} unexpectedly passes — recheck palette")
    return problems


def assert_not_hero(purpose):
    """M8: AI-frame colours are for internal drafts only."""
    if PROVISIONAL and purpose in ("hero", "paid"):
        raise SystemExit(
            "PALETTE GATE: palette is provisional (sampled from AI-degraded "
            "frames). Resample from the real 12MP still before hero/paid renders "
            "(SPEC M8).")


def resample_from_still(path):
    raise NotImplementedError(
        "M8 resample: implement against the real 12MP still when it lands; "
        "then set PROVISIONAL=False and re-run check_legibility().")
