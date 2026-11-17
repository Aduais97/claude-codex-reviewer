#!/usr/bin/env python3
"""Truecoat — Facebook Marketplace launch kit (brand assets).
Supersampled Pillow renderer. Brand: True Blue #1E3EB4, warm amber accent, charcoal ink.
Mark = ruled level line + loaded-brush drip forming a T. Beachhead = Auckland exterior repaints.
All copy lives in CONTENT (swap in ETR-verified copy, re-run). Outputs PNGs to the kit folder.
Run: ~/Desktop/Dev/Claude/.venv/bin/python3 build_truecoat_fb_kit.py
"""
import os, json, math
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.expanduser("~/Desktop/Painting/Truecoat - Facebook Marketplace Kit")
os.makedirs(OUT, exist_ok=True)
SS = 2  # supersample

# ---------- brand ----------
BLUE   = (30, 62, 180)      # True Blue #1E3EB4
BLUE_D = (16, 34, 104)      # deep navy
BLUE_L = (234, 240, 255)    # tint panel
AMBER  = (245, 166, 35)     # warm accent (loaded brush / wet paint)
INK    = (23, 30, 51)       # charcoal
GREY   = (110, 122, 140)
WHITE  = (255, 255, 255)
FA = "/System/Library/Fonts/Avenir Next.ttc"
IDX = {"heavy":8, "bold":0, "demi":2, "medium":5, "regular":7}
_fc = {}
def font(weight, size):
    k = (weight, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FA, int(size*SS), index=IDX[weight])
    return _fc[k]

# ---------- helpers ----------
def canvas(w, h, bg=WHITE):
    return Image.new("RGB", (w*SS, h*SS), bg)
def finish(img, name):
    w, h = img.size
    img = img.resize((w//SS, h//SS), Image.LANCZOS)
    p = os.path.join(OUT, name); img.save(p); print("wrote", name, img.size)
def vgrad(img, box, top, bottom):
    x0,y0,x1,y1 = [v*SS for v in box]; d=ImageDraw.Draw(img); h=y1-y0
    for i in range(h):
        t=i/max(1,h-1)
        c=tuple(int(top[j]+(bottom[j]-top[j])*t) for j in range(3))
        d.line([(x0,y0+i),(x1,y0+i)], fill=c)
def tw(d, text, f):
    b=d.textbbox((0,0),text,font=f); return b[2]-b[0], b[3]-b[1]
def center(d, text, f, cx, y, fill):
    w,h=tw(d,text,f); d.text((cx*SS-w/2, y*SS), text, font=f, fill=fill)
def left(d, text, f, x, y, fill):
    d.text((x*SS, y*SS), text, font=f, fill=fill)
def wrap(d, text, f, maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if tw(d,t,f)[0] <= maxw*SS: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines
def para_center(d, text, f, cx, y, fill, maxw, lh):
    for ln in wrap(d,text,f,maxw):
        center(d, ln, f, cx, y, fill); y+=lh
    return y
def rrect(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle([v*SS for v in box], radius=r*SS, fill=fill, outline=outline, width=int(width*SS))
def fit_lines(d, lines, weight, start, maxw, minsz=40):
    """Largest font size <= start where every line fits within maxw."""
    sz=start
    while sz>minsz:
        f=font(weight,sz)
        if all(tw(d,ln,f)[0] <= maxw*SS for ln in lines): return f
        sz-=2
    return font(weight,minsz)
def checkcircle(d, cx, cy, r, circ=None, tick=WHITE):
    circ=circ or BLUE
    d.ellipse([(cx-r)*SS,(cy-r)*SS,(cx+r)*SS,(cy+r)*SS], fill=circ)
    d.line([((cx-r*0.42))*SS,(cy)*SS,(cx-r*0.08)*SS,(cy+r*0.42)*SS], fill=tick, width=int(r*0.22*SS))
    d.line([((cx-r*0.08))*SS,(cy+r*0.42)*SS,(cx+r*0.48)*SS,(cy-r*0.38)*SS], fill=tick, width=int(r*0.22*SS))
def pill(d, cx, cy, text, f, fg, bg, padx=26, padh=22):
    w,h=tw(d,text,f); bw=w/SS+padx*2; bh=h/SS+padh
    box=[cx-bw/2, cy-bh/2, cx+bw/2, cy+bh/2]
    rrect(d, box, bh/2, fill=bg)
    d.text((cx*SS-w/2, cy*SS-h/2- (h*0.12)), text, font=f, fill=fg)

def teardrop(d, cx, apex_y, bulb_cy, r, color):
    """Clean paint-drop: pointed apex at top, round bulb at bottom (smooth tangent neck)."""
    H=bulb_cy-apex_y
    if H < r*1.15: H=r*1.15
    phi=math.acos(max(-1,min(1,r/H)))
    base=math.radians(-90)                 # center->apex points up
    aR=base+phi; aL=base-phi
    poly=[(cx,apex_y)]
    steps=28; end=aL+2*math.pi
    for i in range(steps+1):
        a=aR+(end-aR)*i/steps
        poly.append((cx+r*math.cos(a), bulb_cy+r*math.sin(a)))
    d.polygon([(x*SS,y*SS) for x,y in poly], fill=color)

def tmark(d, cx, top, h, color, drip=AMBER):
    """Simple, confident T (rounded terminals) + one neat amber paint-drop from the crossbar.
    cx=center x, top=top y, h=mark height (px, pre-SS)."""
    s=SS
    barw=h*0.78; bart=h*0.205; stemw=h*0.205
    x0=(cx-barw/2)*s; x1=(cx+barw/2)*s; y0=top*s; y1=(top+bart)*s
    d.rounded_rectangle([x0,y0,x1,y1], radius=bart*0.5*s, fill=color)        # crossbar
    sx0=(cx-stemw/2)*s; sx1=(cx+stemw/2)*s; sy1=(top+h)*s
    d.rounded_rectangle([sx0,y0,sx1,sy1], radius=stemw*0.5*s, fill=color)    # stem
    # one neat paint-drop hanging from the crossbar, between stem and right end
    dcx=cx+barw*0.26; bulbr=h*0.105
    apex=top+bart*0.62; bulb_cy=top+bart+h*0.20
    teardrop(d, dcx, apex, bulb_cy, bulbr, drip)

def load_content():
    p=os.path.join(OUT,"_content.json")
    if os.path.exists(p): return json.load(open(p))
    return DEFAULT

# ---------- default copy (replaced by ETR-verified _content.json when present) ----------
DEFAULT = {
 "brandline":"AUCKLAND EXTERIOR PAINTERS",
 "tagline":"Weatherboard repaints done right — the first time.",
 "tiles":{
  "hero":{"eyebrow":"AUCKLAND · EXTERIOR REPAINTS","headline":"Tired weatherboards?\nWe bring them back to life.","sub":"Premium exterior repaints for Auckland homes. Free, no-obligation quotes.","cta":"Message us for a free quote"},
  "services":{"headline":"What we paint","items":["Exterior weatherboard repaints","Roofs, fences & decks","Interior repaints & new builds","Light-commercial & rentals"],"cta":"Ask us — if it needs painting, we do it"},
  "whyus":{"headline":"Why Truecoat","items":["Written prep + paint scope (AS/NZS 2311)","Fixed workmanship guarantee","Quality trade paints","Tidy, respectful crew","Free, no-obligation quotes"],"cta":"Painted right, or we make it right"},
  "beforeafter":{"headline":"Before  →  After","sub":"Real Auckland weatherboard repaints","note":"[ add your before/after photos here ]"},
  "offer":{"eyebrow":"FOUNDING CUSTOMERS","headline":"Foundation repaint spots","sub":"A limited number of exterior repaints this season — a fair price for honest before/after photos & a review.","cta":"Message “FOUNDATION” to enquire"},
  "contact":{"headline":"Free quotes across Auckland","sub":"Weatherboard, villa & bungalow repaints.","areas":"[SUBURBS: North Shore · Central · West · East]","phone":"[MOBILE]","email":"[EMAIL]","cta":"Message us today"},
 }
}
C = load_content()
def T(k): return C["tiles"][k]

# =================== ASSETS ===================
def a_avatar():
    img=canvas(1080,1080,BLUE); d=ImageDraw.Draw(img)
    vgrad(img,(0,0,1080,1080),BLUE,BLUE_D)
    # keep within circle-safe center
    tmark(d,540,300,300,WHITE,AMBER)
    center(d,"TRUECOAT",font("heavy",96),540,660,WHITE)
    center(d,C["brandline"],font("demi",30),540,780,(180,198,235))
    finish(img,"01_profile_avatar_1080.png")

def _logo(bg, fg, sub_c, name, transparent=False):
    W,H=2400,760
    if transparent:
        img=Image.new("RGBA",(W*SS,H*SS),(0,0,0,0))
    else:
        img=canvas(W,H,bg)
    d=ImageDraw.Draw(img)
    tmark(d,360,190,380,fg,AMBER)
    left(d,"TRUECOAT",font("heavy",190),690,250,fg)
    left(d,C["brandline"],font("demi",58),700,470,sub_c)
    if transparent:
        img=img.resize((W,H),Image.LANCZOS); img.save(os.path.join(OUT,name)); print("wrote",name,img.size); return
    finish(img,name)

def a_logos():
    _logo(WHITE,BLUE,GREY,"02_logo_on-white_2400.png")
    _logo(BLUE,WHITE,(190,206,240),"03_logo_on-blue_2400.png")
    _logo(None,BLUE,GREY,"04_logo_transparent_2400.png",transparent=True)

def a_cover():
    W,H=1640,624
    img=canvas(W,H,BLUE); d=ImageDraw.Draw(img); vgrad(img,(0,0,W,H),BLUE,BLUE_D)
    # right-side big mark watermark
    tmark(d,1330,150,330,(255,255,255),AMBER)
    left(d,"TRUECOAT",font("heavy",150),90,150,WHITE)
    left(d,C["brandline"],font("demi",46),96,320,(190,206,240))
    left(d,C["tagline"],font("medium",40),96,400,WHITE)
    pill(d,300,520,"Free quotes across Auckland",font("demi",34),BLUE_D,AMBER)
    finish(img,"05_facebook_cover_1640x624.png")

def _tile_base(accent_top=True):
    img=canvas(1080,1080,WHITE); d=ImageDraw.Draw(img)
    # header band
    vgrad(img,(0,0,1080,150),BLUE,BLUE_D) if accent_top else None
    if accent_top:
        tmark(d,90,38,74,WHITE,AMBER)
        left(d,"TRUECOAT",font("heavy",44),150,52,WHITE)
        left(d,C["brandline"],font("demi",20),153,108,(190,206,240))
    return img,d

def a_hero():
    img=canvas(1080,1080,BLUE); d=ImageDraw.Draw(img); vgrad(img,(0,0,1080,1080),BLUE,BLUE_D)
    t=T("hero")
    pill(d,540,150,t["eyebrow"],font("demi",30),BLUE_D,AMBER)
    hlines=t["headline"].split("\n")
    hf=fit_lines(d,hlines,"heavy",78,940)
    lh=hf.size/SS*1.22
    y=330-((len(hlines)-1)*lh)/2
    for ln in hlines:
        center(d,ln,hf,540,y,WHITE); y+=lh
    y+=30
    y=para_center(d,t["sub"],font("medium",40),540,y,(206,218,245),820,54)
    tmark(d,540,y+40,150,WHITE,AMBER)
    pill(d,540,980,t["cta"],font("demi",38),BLUE_D,AMBER)
    finish(img,"06_tile_hero_1080.png")

def a_services():
    img,d=_tile_base(); t=T("services")
    left(d,t["headline"],font("heavy",72),90,215,INK)
    items=t["items"]; top=350; bottom=930          # band above the pinned CTA
    n=len(items); gap=18
    rowh=min(122,(bottom-top-gap*(n-1))/n); step=rowh+gap
    itf=fit_lines(d,items,"demi",38,760,30)
    y=top
    for it in items:
        rrect(d,(90,y,990,y+rowh),22,fill=BLUE_L)
        checkcircle(d,150,y+rowh/2,22)
        _,th=tw(d,it,itf); left(d,it,itf,200,y+rowh/2-(th/SS)/2-2,INK)
        y+=step
    pill(d,540,1012,t["cta"],font("demi",34),WHITE,BLUE)
    finish(img,"07_tile_services_1080.png")

def a_whyus():
    img,d=_tile_base(); t=T("whyus")
    left(d,t["headline"],font("heavy",72),90,215,INK)
    items=t["items"]; top=345; bottom=915
    n=len(items); f=fit_lines(d,items,"demi",38,800,28)
    step=(bottom-top)/n
    y=top
    for it in items:
        cy=y+step/2
        d.ellipse([(96)*SS,(cy-13)*SS,(96+26)*SS,(cy+13)*SS],fill=AMBER)
        _,th=tw(d,it,f); left(d,it,f,146,cy-(th/SS)/2-2,INK)
        y+=step
    pill(d,540,1012,t["cta"],font("demi",34),BLUE_D,AMBER)
    finish(img,"08_tile_whyus_1080.png")

def a_beforeafter():
    img,d=_tile_base(); t=T("beforeafter")
    left(d,t["headline"],font("heavy",64),90,210,INK)
    left(d,t["sub"],font("medium",34),90,300,GREY)
    # two placeholder frames
    for i,(lab,x) in enumerate([("BEFORE",70),("AFTER",560)]):
        rrect(d,(x,380,x+450,900),24,fill=BLUE_L,outline=BLUE,width=3)
        center(d,lab,font("heavy",40),x+225,410,BLUE)
        center(d,"◻",font("regular",120),x+225,600,(180,196,230))
    center(d,t["note"],font("medium",30),540,930,GREY)
    finish(img,"09_tile_beforeafter_1080.png")

def a_offer():
    img=canvas(1080,1080,BLUE_D); d=ImageDraw.Draw(img); vgrad(img,(0,0,1080,1080),BLUE,BLUE_D)
    t=T("offer")
    pill(d,540,170,t["eyebrow"],font("demi",30),BLUE_D,AMBER)
    y=para_center(d,t["headline"],font("heavy",84),540,300,WHITE,900,100)
    y+=30
    y=para_center(d,t["sub"],font("medium",40),540,y,(206,218,245),840,56)
    tmark(d,540,y+40,140,WHITE,AMBER)
    pill(d,540,980,t["cta"],font("demi",38),BLUE_D,AMBER)
    finish(img,"10_tile_offer_1080.png")

def a_contact():
    img,d=_tile_base(); t=T("contact")
    left(d,t["headline"],font("heavy",64),90,215,INK)
    y=para_center(d,t["sub"],font("medium",38),540,340,GREY,900,50)+20
    for lab,val in [("Areas",t["areas"]),("Call / text",t["phone"]),("Email",t["email"])]:
        rrect(d,(90,y,990,y+110),20,fill=BLUE_L)
        left(d,lab.upper(),font("demi",26),120,y+22,BLUE)
        left(d,val,font("demi",40),120,y+55,INK)
        y+=132
    pill(d,540,1005,t["cta"],font("demi",38),WHITE,BLUE)
    finish(img,"11_tile_contact_1080.png")

if __name__=="__main__":
    a_avatar(); a_logos(); a_cover()
    a_hero(); a_services(); a_whyus(); a_beforeafter(); a_offer(); a_contact()
    print("\nAll assets ->", OUT)
