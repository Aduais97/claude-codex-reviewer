"""Proportional layout + auto-fit (SPEC §4.1, M10, M12; §8 step 3).

All positions are fractions of the frame — never absolute pixels. The safe
rectangle is a conservative UNION of third-party creator guides (both
platforms move their chrome): UNVERIFIED until checked on a live device.
Default right margin is the flat 13% (M12) — the 5% relaxation is opt-in and
needs a live-device screenshot first.
"""

from . import typeset

# TYPE_SAFE (SPEC §4.1): x in [7%, 87%], y in [14%, 73%]
TYPE_SAFE = {"x0": 0.07, "x1": 0.87, "y0": 0.14, "y1": 0.73}
ACTION_SAFE_INSET = 0.05
PRODUCT_OPTICAL_CENTER_Y = 0.42

AUTO_FIT_FLOOR = 0.55   # shrink no further than 55% of the role size (M10)


def type_safe_px(W, H):
    return (int(W * TYPE_SAFE["x0"]), int(H * TYPE_SAFE["y0"]),
            int(W * TYPE_SAFE["x1"]), int(H * TYPE_SAFE["y1"]))


def fit_role(text, role, W):
    """M10 auto-fit: measure tracked width; shrink toward the floor, else wrap
    to two lines. Returns (lines, scale). Raises if it still cannot fit."""
    max_w = (TYPE_SAFE["x1"] - TYPE_SAFE["x0"]) * W
    if typeset.measure(text, role, W) <= max_w:
        return [text], 1.0
    # shrink
    scale = 1.0
    while scale > AUTO_FIT_FLOOR:
        scale -= 0.05
        if typeset.measure(text, role, W, scale) <= max_w:
            return [text], scale
    # wrap to two lines at the most balanced space
    words = text.split()
    if len(words) > 1:
        best = min(range(1, len(words)),
                   key=lambda i: abs(typeset.measure(" ".join(words[:i]), role, W)
                                     - typeset.measure(" ".join(words[i:]), role, W)))
        l1, l2 = " ".join(words[:best]), " ".join(words[best:])
        for scale in (1.0, 0.9, 0.8, 0.7, 0.6):
            if (typeset.measure(l1, role, W, scale) <= max_w
                    and typeset.measure(l2, role, W, scale) <= max_w):
                return [l1, l2], scale
    raise SystemExit(f"LAYOUT: {role} text cannot fit TYPE_SAFE even wrapped: {text!r}")


def place_centered(line_img, W, y_frac):
    """Top-left paste position for a line image horizontally centred at cx."""
    return ((W - line_img.width) // 2, int(y_frac * 1920) - line_img.height // 2)


def assert_inside_type_safe(y_frac, role=""):
    if not (TYPE_SAFE["y0"] <= y_frac <= TYPE_SAFE["y1"]):
        raise SystemExit(
            f"LAYOUT: {role} at y={y_frac:.0%} is outside TYPE_SAFE "
            f"[{TYPE_SAFE['y0']:.0%}, {TYPE_SAFE['y1']:.0%}] — chrome will cover it.")
