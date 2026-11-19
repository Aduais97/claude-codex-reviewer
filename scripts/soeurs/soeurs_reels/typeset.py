"""Per-glyph tracked typesetter (SPEC §4.3, M6/M7, §8 step 2).

Pillow has no letter-spacing (`spacing` is line leading) and libraqm is
absent on this host, so tracking is hand-rolled: loop font.getlength(ch),
add track = pct * fontsize between glyphs, bake to RGBA. Latin/upper only.

The wordmark is NEVER typeset here — it is a serif carrying brand equity and
appears only as the supplied logo asset (SPEC M6). Satoshi containing Œ is
irrelevant to that rule.
"""

import os
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = os.path.expanduser("~/Library/Fonts")

# SPEC §4.3 type scale. size_frac = glyph size as fraction of canvas WIDTH.
# tracking = fraction of an em added between glyphs.
ROLES = {
    "display_hook_editorial": ("Satoshi-Light.otf",  0.100, -0.005, "sentence"),
    "display_hook_punch":     ("Satoshi-Black.otf",  0.089,  0.000, "upper"),
    "scent_name":             ("Satoshi-Medium.otf", 0.119,  0.060, "upper"),
    "eyebrow_label":          ("Nexa-Bold.ttf",      0.030,  0.220, "upper"),
    "claim_line":             ("Satoshi-Bold.otf",   0.078,  0.010, "upper"),
    "note_word":              ("Satoshi-Light.otf",  0.056,  0.040, "sentence"),
    "cta_line":               ("Satoshi-Medium.otf", 0.048,  0.020, "sentence"),
    "price_format":           ("Satoshi-Medium.otf", 0.033,  0.040, "upper"),
    "handle":                 ("Satoshi-Regular.otf", 0.028, 0.060, "lower"),
    "legal_micro":            ("Satoshi-Regular.otf", 0.024, 0.020, "sentence"),
}


def _apply_case(text, case):
    return {"upper": text.upper(), "lower": text.lower()}.get(case, text)


def load_role_font(role, canvas_w, scale=1.0):
    fname, size_frac, tracking, case = ROLES[role]
    size = max(8, int(canvas_w * size_frac * scale))
    return ImageFont.truetype(os.path.join(FONT_DIR, fname), size), tracking, case


def tracked_width(text, font, track_px):
    if not text:
        return 0.0
    return sum(font.getlength(ch) for ch in text) + track_px * (len(text) - 1)


def measure(text, role, canvas_w, scale=1.0):
    font, tracking, case = load_role_font(role, canvas_w, scale)
    text = _apply_case(text, case)
    return tracked_width(text, font, tracking * font.size)


def set_line(text, role, canvas_w, color_rgb, scale=1.0, pad=0.25):
    """Render one tracked line to a tight RGBA image. Returns (Image, ascent)."""
    font, tracking, case = load_role_font(role, canvas_w, scale)
    text = _apply_case(text, case)
    track_px = tracking * font.size
    w = int(tracked_width(text, font, track_px)) + int(font.size * pad * 2)
    ascent, descent = font.getmetrics()
    h = ascent + descent + int(font.size * pad)
    img = Image.new("RGBA", (max(w, 1), h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = float(int(font.size * pad))
    y = int(font.size * pad / 2)
    for ch in text:
        d.text((x, y), ch, font=font, fill=(*color_rgb, 255))
        x += font.getlength(ch) + track_px
    return img, y + ascent
