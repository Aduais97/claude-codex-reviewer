#!/usr/bin/env python3
"""Compile the Truecoat FB Marketplace kit into one PDF proof sheet (review + share)."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas as rlcanvas

KD = os.path.expanduser("~/Desktop/Painting/Truecoat - Facebook Marketplace Kit")
OUT = os.path.join(KD, "Truecoat FB Kit - Proof.pdf")
NAVY = colors.HexColor("#0D1632"); BLUE = colors.HexColor("#1E3EB4")
GOLD = colors.HexColor("#C8962E"); INK = colors.HexColor("#161A21"); MUT = colors.HexColor("#7E828A")

ASSETS = [
    ("01_profile_avatar_1080.png", "Profile picture", "Facebook page + Marketplace seller pic (crops to a circle)"),
    ("05_facebook_cover_1640x624.png", "Cover banner", "Facebook Page cover photo"),
    ("02_logo_on-white_2400.png", "Logo — on white", "Quotes, invoices, email signature"),
    ("03_logo_on-blue_2400.png", "Logo — on navy", "Dark backgrounds"),
    ("06_tile_hero_1080.png", "Listing 1 — Hero", "The scroll-stopper — first image in the carousel"),
    ("09_tile_beforeafter_1080.png", "Listing 2 — Before / After", "Swap in a real completed job photo"),
    ("07_tile_services_1080.png", "Listing 3 — What we paint", "Interior + exterior services"),
    ("08_tile_whyus_1080.png", "Listing 4 — Why Truecoat", "Trust points / the prep story"),
    ("10_tile_offer_1080.png", "Listing 5 — Foundation offer", "Launch offer"),
    ("11_tile_contact_1080.png", "Listing 6 — Contact", "How to reach you"),
]

c = rlcanvas.Canvas(OUT, pagesize=A4)
W, H = A4

# cover page
c.setFillColor(NAVY); c.rect(0, 0, W, H, fill=1, stroke=0)
c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 30); c.drawCentredString(W/2, H-150, "TRUECOAT")
c.setFillColor(GOLD); c.setFont("Helvetica-Bold", 12); c.drawCentredString(W/2, H-172, "A U C K L A N D   P A I N T E R S")
c.setStrokeColor(GOLD); c.setLineWidth(1); c.line(W/2-30, H-186, W/2+30, H-186)
c.setFillColor(colors.HexColor("#AEB9D0")); c.setFont("Helvetica", 13)
c.drawCentredString(W/2, H/2+20, "Facebook Marketplace Launch Kit")
c.drawCentredString(W/2, H/2-4, "Brand assets, listing copy & posting guide")
c.setFillColor(colors.HexColor("#7C88A8")); c.setFont("Helvetica", 10)
c.drawCentredString(W/2, 90, "Interior & exterior painting  ·  Auckland-wide")
c.drawCentredString(W/2, 74, "021 819 947   ·   Mohammaddud99@gmail.com")
c.showPage()

for i, (fn, title, note) in enumerate(ASSETS):
    p = os.path.join(KD, fn)
    if not os.path.exists(p): continue
    ir = ImageReader(p); iw, ih = ir.getSize(); ar = iw/ih
    # header
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 15); c.drawString(24*mm, H-26*mm, title)
    c.setFillColor(MUT); c.setFont("Helvetica", 10); c.drawString(24*mm, H-31*mm, note)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold", 9); c.drawRightString(W-24*mm, H-26*mm, fn)
    c.setStrokeColor(colors.HexColor("#E1DED7")); c.setLineWidth(0.6); c.line(24*mm, H-34*mm, W-24*mm, H-34*mm)
    # image, fit within frame
    maxw = W-48*mm; maxh = H-34*mm-30*mm
    dw = maxw; dh = dw/ar
    if dh > maxh: dh = maxh; dw = dh*ar
    x = (W-dw)/2; y = (H-34*mm-30*mm)-dh + 12*mm
    # subtle frame for the square/light tiles
    c.setStrokeColor(colors.HexColor("#D9D6CE")); c.setLineWidth(0.5); c.rect(x-1, y-1, dw+2, dh+2, fill=0, stroke=1)
    c.drawImage(ir, x, y, width=dw, height=dh, mask='auto')
    c.setFillColor(MUT); c.setFont("Helvetica", 8); c.drawCentredString(W/2, 16*mm, f"Truecoat — Auckland Painters   ·   page {i+2}")
    c.showPage()

c.save()
print("wrote", OUT)
