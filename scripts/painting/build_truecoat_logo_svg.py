#!/usr/bin/env python3
"""Truecoat logo — pure SVG, rendered crisp via fitz. Open-C + T monogram (round caps),
width-matched TRUE/COAT wordmark, tagline. TWO COLOURS: white + True Blue. No gold, no illustration."""
import os, fitz
from PIL import Image
OUT = os.path.expanduser("~/Desktop/Painting/Truecoat - Facebook Marketplace Kit")
BLUE="#1E3EB4"; WHITE="#FFFFFF"

def mark_svg(fg, sw=7.5):
    # Variant A: T crossbar flows INTO the C's top terminal — connected TC monogram.
    return (f'<g fill="none" stroke="{fg}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M 86 46 A 42 42 0 1 0 86 84"/>'   # C (opens lower-right)
            '<path d="M 30 46 H 86"/>'                    # T crossbar -> meets C top terminal
            '<path d="M 58 46 V 90"/>'                    # T stem
            '</g>')

def horizontal_svg(fg, bg=None):
    # FONT ONLY — no symbol. Two-line width-matched TRUE / COAT + tagline, centred.
    W,H=920,470; cx=W/2; wlen=560
    bgrect=f'<rect width="{W}" height="{H}" fill="{bg}"/>' if bg else ''
    word=(
      f'<text x="{cx}" y="176" font-family="Helvetica" font-weight="bold" font-size="150" text-anchor="middle" '
      f'fill="{fg}" textLength="{wlen}" lengthAdjust="spacingAndGlyphs">TRUE</text>'
      f'<text x="{cx}" y="322" font-family="Helvetica" font-weight="bold" font-size="150" text-anchor="middle" '
      f'fill="{fg}" textLength="{wlen}" lengthAdjust="spacingAndGlyphs">COAT</text>'
      f'<text x="{cx}" y="378" font-family="Helvetica" font-weight="500" font-size="31" text-anchor="middle" '
      f'fill="{fg}" textLength="{wlen}" lengthAdjust="spacingAndGlyphs" opacity="0.82">YOUR TRUSTED AUCKLAND PAINTERS</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">{bgrect}{word}</svg>'

def avatar_svg(fg, bg):
    # FONT ONLY — two-line TRUE / COAT + tagline, centred (circle-safe).
    S=1080; cx=540; wlen=620
    word=(
      f'<text x="{cx}" y="470" font-family="Helvetica" font-weight="bold" font-size="176" text-anchor="middle" '
      f'fill="{fg}" textLength="{wlen}" lengthAdjust="spacingAndGlyphs">TRUE</text>'
      f'<text x="{cx}" y="640" font-family="Helvetica" font-weight="bold" font-size="176" text-anchor="middle" '
      f'fill="{fg}" textLength="{wlen}" lengthAdjust="spacingAndGlyphs">COAT</text>'
      f'<text x="{cx}" y="706" font-family="Helvetica" font-weight="500" font-size="37" text-anchor="middle" '
      f'fill="{fg}" textLength="{wlen}" lengthAdjust="spacingAndGlyphs" opacity="0.9">AUCKLAND PAINTERS</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}"><rect width="{S}" height="{S}" fill="{bg}"/>{word}</svg>'

def compact_svg(fg):
    """FONT ONLY — single-line TRUECOAT for tile corners. transparent."""
    W,H=760,150
    word=(f'<text x="6" y="116" font-family="Helvetica" font-weight="bold" font-size="112" '
          f'fill="{fg}" letter-spacing="1.5">TRUECOAT</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">{word}</svg>'

def render(svg, name, scale=4, alpha=False):
    p="/tmp/_tc.svg"; open(p,"w").write(svg)
    doc=fitz.open(p); pix=doc[0].get_pixmap(matrix=fitz.Matrix(scale,scale), alpha=alpha)
    out=os.path.join(OUT,name); pix.save(out); print("wrote",name, (pix.width,pix.height))

if __name__=="__main__":
    render(horizontal_svg(WHITE, BLUE),  "logo_primary_on-blue_2400.png")
    render(horizontal_svg(BLUE,  WHITE), "logo_on-white_2400.png")
    render(horizontal_svg(WHITE),        "logo_transparent_white_2400.png", alpha=True)
    render(horizontal_svg(BLUE),         "logo_transparent_blue_2400.png", alpha=True)
    render(avatar_svg(WHITE, BLUE),      "logo_avatar_on-blue_1080.png")
    render(avatar_svg(BLUE, WHITE),      "logo_mark_on-white_1080.png")
    render(compact_svg(WHITE),           "logo_compact_white.png", alpha=True)
    render(compact_svg(BLUE),            "logo_compact_blue.png", alpha=True)
    print("SVG logo set ->", OUT)
