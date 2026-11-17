#!/usr/bin/env python3
"""Truecoat FB kit — v3 FINAL. Photo-led tiles + SVG logo overlay. TWO COLOURS: True Blue + white.
NO gold. Real job photos (before/after) + painting-action shots. Builds the numbered kit + assembles."""
import os, shutil
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter

KD = os.path.expanduser("~/Desktop/Painting/Truecoat - Facebook Marketplace Kit")
P  = os.path.join(KD, "photos")
BLUE=(30,62,180); NAVY=(16,26,58); NAVY2=(11,19,44); INK=(22,26,33)
PAPER=(245,244,240); WHITE=(255,255,255); MUT_L=(200,208,228); MUT=(120,124,132); LINE=(224,221,213)
HN="/System/Library/Fonts/HelveticaNeue.ttc"; IDX={"bold":1,"med":10,"reg":0,"light":7}
_fc={}
def font(w,s):
    k=(w,s)
    if k not in _fc: _fc[k]=ImageFont.truetype(HN,int(s),index=IDX[w])
    return _fc[k]
def tw(d,t,f): b=d.textbbox((0,0),t,font=f); return b[2]-b[0]
def th(d,t,f): b=d.textbbox((0,0),t,font=f); return b[3]-b[1]
def text(d,t,f,x,y,fill): d.text((x,y),t,font=f,fill=fill)
def ltext(d,t,f,x,y,fill,tr):
    cx=x
    for ch in t: d.text((cx,y),ch,font=f,fill=fill); cx+=tw(d,ch,f)+tr
def rule(d,x0,y,x1,c,w=2): d.line([(x0,y),(x1,y)],fill=c,width=w)
def wrap(d,t,f,mw):
    out=[]
    for para in t.split("\n"):
        cur=""
        for w in para.split():
            s=(cur+" "+w).strip()
            if tw(d,s,f)<=mw: cur=s
            else: out.append(cur); cur=w
        out.append(cur)
    return out
def arrow(d,x,y,L,c,w=4):
    x1=x+L; hw=L*0.34
    d.line([(x,y),(x1,y)],fill=c,width=w); d.line([(x1-hw,y-hw),(x1,y)],fill=c,width=w); d.line([(x1-hw,y+hw),(x1,y)],fill=c,width=w)

def cover(path,tw_,th_,fx=0.5,fy=0.5):
    im=ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    iw,ih=im.size; s=max(tw_/iw,th_/ih); nw,nh=int(iw*s+.5),int(ih*s+.5)
    im=im.resize((nw,nh),Image.LANCZOS); x=int((nw-tw_)*fx); y=int((nh-th_)*fy)
    return im.crop((x,y,x+tw_,y+th_))
def scrim(img,mode="bottom",frac=0.62,amax=236,color=(9,15,38)):
    w,h=img.size; ov=Image.new("RGBA",(w,h),(0,0,0,0)); d=ImageDraw.Draw(ov)
    if mode in("bottom","both"):
        y0=int(h*(1-frac))
        for y in range(y0,h):
            t=(y-y0)/max(1,h-y0); d.line([(0,y),(w,y)],fill=color+(int(amax*t*t),))
    if mode in("top","both"):
        y1=int(h*0.22)
        for y in range(0,y1):
            t=1-(y/max(1,y1)); d.line([(0,y),(w,y)],fill=color+(int(150*t),))
    if mode=="full":
        d.rectangle([0,0,w,h],fill=color+(amax,))
    return Image.alpha_composite(img.convert("RGBA"),ov).convert("RGB")

_lc={}
def logo(kind):  # 'white','blue' compact ; 'avatar'
    f={"white":"logo_compact_white.png","blue":"logo_compact_blue.png"}[kind]
    if kind not in _lc:
        p=os.path.join(KD,f); _lc[kind]=Image.open(p).convert("RGBA") if os.path.exists(p) else None
    return _lc[kind]
def paste_logo(img,kind,x,y,h):
    lg=logo(kind)
    if lg is None: return
    r=h/lg.height; lg=lg.resize((int(lg.width*r),h),Image.LANCZOS); img.paste(lg,(int(x),int(y)),lg)

import json
C=json.load(open(os.path.join(KD,"_content.json")))
def save(img,name): img.save(os.path.join(KD,name)); print("wrote",name)

# ---- photo tile (headline overlay) ----
def photo_tile(name, photo, headline, sub, cta, eyebrow, focus=(0.5,0.4)):
    W=1080; img=cover(os.path.join(P,photo),W,W,*focus)
    img=scrim(img,"both",0.66,240); d=ImageDraw.Draw(img); M=70
    paste_logo(img,"white",M,58,56)
    y=W-70
    if cta:
        cf=font("bold",30); y-=42; text(d,cta,cf,M,y,WHITE); arrow(d,M+tw(d,cta,cf)+20,y+th(d,cta,cf)//2+2,24,WHITE)
    if sub:
        sf=font("light",34); subs=wrap(d,sub,sf,W-2*M); y-=len(subs)*46+16
        yy=y
        for ln in subs: text(d,ln,sf,M,yy,MUT_L); yy+=46
    hf=font("bold",74); hs=wrap(d,headline,hf,W-2*M); y-=len(hs)*84+8
    rule(d,M,y-20,M+92,WHITE,5); yy=y
    for ln in hs: text(d,ln,hf,M,yy,WHITE); yy+=84
    if eyebrow: ltext(d,eyebrow.upper(),font("bold",23),M,y-64,WHITE,4)
    save(img,name)

# ---- photo tile with a list (services/why-us) ----
def photo_list_tile(name, photo, eyebrow, headline, items, cta, focus=(0.5,0.4)):
    W=1080; img=cover(os.path.join(P,photo),W,W,*focus)
    img=scrim(img,"full",amax=205); img=scrim(img,"both",0.5,150); d=ImageDraw.Draw(img); M=70
    paste_logo(img,"white",M,58,56)
    ltext(d,eyebrow.upper(),font("bold",23),M,182,MUT_L,4)
    text(d,headline,font("bold",64),M,220,WHITE)
    y=350; step=min(96,(900-350)/len(items))
    itf=font("med",37)
    for i,it in enumerate(items):
        cy=y+step/2
        d.ellipse([M,cy-5,M+10,cy+5],fill=WHITE)   # small dot
        text(d,it,itf,M+34,cy-24,WHITE)
        y+=step
    cf=font("bold",30); text(d,cta,cf,M,952,WHITE); arrow(d,M+tw(d,cta,cf)+20,952+th(d,cta,cf)//2+2,24,WHITE)
    save(img,name)

# ---- before/after ----
def before_after(name):
    W=1080; img=Image.new("RGB",(W,W),NAVY); d=ImageDraw.Draw(img); M=70
    paste_logo(img,"white",M,58,56)
    ltext(d,"REAL AUCKLAND JOB",font("bold",23),M,168,MUT_L,4)
    text(d,"See the difference.",font("bold",62),M,206,WHITE)
    ph=548; pw=(W-M*2-24)//2; top=316
    for lab,fn,x in [("BEFORE","before.jpg",M),("AFTER","after.jpg",M+pw+24)]:
        img.paste(cover(os.path.join(P,fn),pw,ph,0.5,0.4),(x,top))
        d.rectangle([x,top,x+150,top+42],fill=NAVY2); ltext(d,lab,font("bold",22),x+16,top+11,WHITE,3)
    text(d,"Tired & peeling weatherboards — fully repainted.",font("light",30),M,896,MUT_L)
    cf=font("bold",30); text(d,C["tiles"]["hero"]["cta"],cf,M,950,WHITE); arrow(d,M+tw(d,C["tiles"]["hero"]["cta"],cf)+20,950+th(d,C["tiles"]["hero"]["cta"],cf)//2+2,24,WHITE)
    save(img,name)

# ---- navy solid (offer / contact) ----
def navy_tile(name, eyebrow, headline, body_lines, cta, contact=None):
    W=1080; img=Image.new("RGB",(W,W),NAVY); d=ImageDraw.Draw(img); M=70
    paste_logo(img,"white",M,58,56)
    ltext(d,eyebrow.upper(),font("bold",23),M,200,MUT_L,4)
    y=244
    for ln in wrap(d,headline,font("bold",70),W-2*M): text(d,ln,font("bold",70),M,y,WHITE); y+=84
    rule(d,M,y+16,M+92,WHITE,5); y+=60
    if body_lines:
        for ln in body_lines: text(d,ln,font("light",34),M,y,MUT_L); y+=46
        y+=10
    if contact:
        for lab,val in contact:
            ltext(d,lab,font("bold",21),M,y,MUT_L,3); text(d,val,font("med",40),M,y+30,WHITE); y+=118
    cf=font("bold",30); text(d,cta,cf,M,952,WHITE); arrow(d,M+tw(d,cta,cf)+20,952+th(d,cta,cf)//2+2,24,WHITE)
    save(img,name)

# ---- cover banner (FB page cover: name + tagline + phone) ----
def cover_banner(name):
    W,H=1640,624; img=cover(os.path.join(P,"after.jpg"),W,H,0.5,0.42)
    img=scrim(img,"full",amax=120); img=scrim(img,"bottom",0.75,215)
    d=ImageDraw.Draw(img); M=96
    paste_logo(img,"white",M,H-250,100)     # "TRUECOAT" wordmark
    text(d,"Interior & exterior painters · Auckland-wide",font("light",38),M+4,H-132,WHITE)
    cf=font("bold",38); ph="021 819 947   ·   Free no-obligation quotes"
    text(d,ph,cf,M+4,H-80,WHITE)
    save(img,name)

def assemble():
    # numbered kit from the SVG logo + tiles
    m={"logo_avatar_on-blue_1080.png":"01_profile_avatar_1080.png",
       "logo_on-white_2400.png":"02_logo_on-white_2400.png",
       "logo_primary_on-blue_2400.png":"03_logo_on-blue_2400.png",
       "logo_transparent_blue_2400.png":"04_logo_transparent_2400.png"}
    for s,dst in m.items():
        sp=os.path.join(KD,s)
        if os.path.exists(sp): shutil.copy2(sp,os.path.join(KD,dst)); print("→",dst)

if __name__=="__main__":
    t=C["tiles"]
    cover_banner("05_facebook_cover_1640x624.png")
    photo_tile("06_tile_hero_1080.png","after.jpg","Fresh paint,\ndone right the first time.",
               t["hero"]["sub"], t["hero"]["cta"], t["hero"]["eyebrow"], (0.5,0.34))
    photo_list_tile("07_tile_services_1080.png","paint_exterior.jpg","WHAT WE PAINT","Inside and out.",
               [i for i in t["services"]["items"]], t["services"]["cta"], (0.5,0.4))
    photo_list_tile("08_tile_whyus_1080.png","paint_interior.jpg","WHY TRUECOAT","The difference is the prep.",
               ["Written prep + paint scope","Quality trade paints","Tidy, respectful crew","Workmanship re-do guarantee","Free, no-obligation quotes"],
               t["whyus"]["cta"], (0.5,0.3))
    before_after("09_tile_beforeafter_1080.png")
    navy_tile("10_tile_offer_1080.png", t["offer"]["eyebrow"], "Now booking — interior & exterior.",
              wrap(ImageDraw.Draw(Image.new("RGB",(1,1))), t["offer"]["sub"], font("light",34), 900), t["offer"]["cta"])
    navy_tile("11_tile_contact_1080.png","GET IN TOUCH","Get your free quote.", None, "Message us or call today",
              contact=[("SERVICE AREA",t["contact"]["areas"]),("CALL / TEXT",t["contact"]["phone"]),("EMAIL",t["contact"]["email"])])
    assemble()
    print("v3 pack ->",KD)
