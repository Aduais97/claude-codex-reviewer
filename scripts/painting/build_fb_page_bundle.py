#!/usr/bin/env python3
"""Bundle the Truecoat Facebook business-page assets into one email-ready folder."""
import os, shutil
KD = os.path.expanduser("~/Desktop/Painting/Truecoat - Facebook Marketplace Kit")
B  = os.path.join(KD, "Facebook Page Assets (email these)")
if os.path.exists(B): shutil.rmtree(B)
os.makedirs(B)

FILES = [
    ("01_profile_avatar_1080.png",        "1 — Profile Picture (1080x1080).png"),
    ("05_facebook_cover_1640x624.png",    "2 — Cover Photo (1640x624).png"),
    ("06_tile_hero_1080.png",             "3 — Post - Hero.png"),
    ("09_tile_beforeafter_1080.png",      "4 — Post - Before & After.png"),
    ("07_tile_services_1080.png",         "5 — Post - What We Paint.png"),
    ("08_tile_whyus_1080.png",            "6 — Post - Why Truecoat.png"),
    ("10_tile_offer_1080.png",            "7 — Post - Foundation Offer.png"),
    ("11_tile_contact_1080.png",          "8 — Post - Contact.png"),
]
for src, dst in FILES:
    sp = os.path.join(KD, src)
    if os.path.exists(sp): shutil.copy2(sp, os.path.join(B, dst)); print("→", dst)

readme = """TRUECOAT — FACEBOOK BUSINESS PAGE ASSETS
=========================================
Everything to set up the Truecoat Facebook business page. Upload in this order.

PAGE NAME:     Truecoat
CATEGORY:      Painter  (or House Painting / Home Improvement)
USERNAME:      @truecoatnz  (or nearest available)

--------------------------------------------------------------------
1 — PROFILE PICTURE  → "1 — Profile Picture (1080x1080).png"
    Upload as the page profile photo. It crops to a circle (already safe).

2 — COVER PHOTO      → "2 — Cover Photo (1640x624).png"
    Upload as the page cover. Keep the name/phone lower-left visible.

3-8 — FIRST POSTS    → the "Post - ..." images
    Publish these as the first few posts so the page looks established.
    Suggested order: Hero, Before & After, What We Paint, Why Truecoat,
    Foundation Offer, Contact. Post 1-2 per day, not all at once.
--------------------------------------------------------------------

ABOUT / INTRO (paste into the page's About section):
Truecoat is a local Auckland painting crew - interior and exterior. Repaints,
new builds, renovations and light-commercial work. Proper prep, quality trade
paints, a tidy respectful crew, and free no-obligation quotes. Servicing
Auckland-wide. Message us your suburb and a photo of the job to book a free quote.

CONTACT (add to the page):
  Phone / text:  021 819 947
  Email:         Mohammaddud99@gmail.com
  Service area:  Auckland-wide
  Button:        Set the page's main button to "Send Message" (or "Call Now").

NOTE ON PHOTOS:
  The Before & After post is a real completed Truecoat job - great trust-builder.
  As you finish more jobs, take before/after photos and post them - that is what
  wins painting work on Facebook.
"""
open(os.path.join(B, "READ ME - Facebook Page Setup.txt"), "w").write(readme)
print("wrote READ ME - Facebook Page Setup.txt")
print("bundle ->", B)
