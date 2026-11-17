#!/usr/bin/env python3
"""Truecoat FB kit — v2 editorial system (print-quality, not templatey).
Off-white 'paper' content tiles, flat navy hero, left-aligned hierarchy, hairline rules,
letter-spaced small-caps eyebrows, a considered paint-chip monogram (no cartoon drip),
photo-ready frames. Supersampled Pillow. Reads content from _content.json."""
import os, json, math
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.expanduser("~/Desktop/Painting/Truecoat - Facebook Marketplace Kit")
SS = 3

INK=(22,26,33); PAPER=(247,245,240); PAPER2=(238,235,227); CARD=(241,238,231)
BLUE=(30,62,180); NAVY=(13,22,50); NAVY2=(20,32,70)
GOLD=(200,150,46); LINE=(223,219,210); LINE_D=(52,64,102); MUT=(126,130,138); MUT_L=(150,162,196); WHITE=(255,255,255)
HN="/System/Library/Fonts/HelveticaNeue.ttc"
IDX={"bold":1,"med":10,"reg":0,"light":7,"black":9,"cbold":4}
_fc={}
def font(w,s):
    k=(w,s)
    if k not in _fc: _fc[k]=ImageFont.truetype(HN,int(s*SS),index=IDX[w])
    return _fc[k]

def canvas(w,h,bg): return Image.new("RGB",(w*SS,h*SS),bg)
def save(img,name):
    w,h=img.size; img=img.resize((w//SS,h//SS),Image.LANCZOS); img.save(os.path.join(OUT,name)); print("wrote",name)
def tw(d,t,f): b=d.textbbox((0,0),t,font=f); return b[2]-b[0]
def th(d,t,f): b=d.textbbox((0,0),t,font=f); return b[3]-b[1]
def text(d,t,f,x,y,fill): d.text((x*SS,y*SS),t,font=f,fill=fill)
def ltext(d,t,f,x,y,fill,tr):
    """left text with letter tracking tr (px pre-SS)."""
    cx=x*SS
    for ch in t:
        d.text((cx,y*SS),ch,font=f,fill=fill); cx+=tw(d,ch,f)+tr*SS
def ltext_w(d,t,f,tr): return sum(tw(d,ch,f)+tr*SS for ch in t)/SS - tr
def rule(d,x0,y,x1,color=LINE,w=1.4): d.line([(x0*SS,y*SS),(x1*SS,y*SS)],fill=color,width=int(w*SS))
def rrect(d,box,r,fill=None,outline=None,width=1):
    d.rounded_rectangle([v*SS for v in box],radius=r*SS,fill=fill,outline=outline,width=int(width*SS))
def wrap(d,t,f,maxw):
    words=t.split(); lines=[]; cur=""
    for w in words:
        s=(cur+" "+w).strip()
        if tw(d,s,f)<=maxw*SS: cur=s
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

def arrow(d,x,y,length,color,w=3.2):
    """Clean right-arrow, drawn (Helvetica has no → glyph). x,y = left end, mid-height baseline."""
    x0=x*SS; x1=(x+length)*SS; yy=y*SS; hw=length*0.34*SS
    d.line([(x0,yy),(x1,yy)],fill=color,width=int(w*SS))
    d.line([(x1-hw,yy-hw),(x1,yy)],fill=color,width=int(w*SS))
    d.line([(x1-hw,yy+hw),(x1,yy)],fill=color,width=int(w*SS))
def cta_line(d,x,y,txt,f,color):
    text(d,txt,f,x,y,color); w=tw(d,txt,f)/SS
    arrow(d,x+w+22,y+th(d,txt,f)/SS/2+4,26,color); return w
def chip(d,x,y,size,fg=BLUE,letter=WHITE,r=None):
    """Paint-chip monogram: rounded-square swatch + white T. x,y top-left, size px."""
    r=r if r else size*0.24
    rrect(d,(x,y,x+size,y+size),r,fill=fg)
    # subtle lighter swatch band at bottom (paint-chip cue)
    band=size*0.16
    d.rounded_rectangle([(x+size*0.16)*SS,(y+size-band-size*0.13)*SS,(x+size*0.84)*SS,(y+size-size*0.13)*SS],
                        radius=band*0.4*SS, fill=(255,255,255,40) if False else _tint(fg,0.20))
    # T
    f=font("bold",int(size*0.60)); t="T"; wt=tw(d,t,f); ht=th(d,t,f)
    d.text((x*SS+size*SS/2-wt/2, y*SS+size*SS*0.16), t, font=f, fill=letter)
def _tint(c,f): return tuple(int(c[i]+(255-c[i])*f) for i in range(3))

def lockup(d,x,y,mark=BLUE,word=INK,sub=MUT,size=64,letter=WHITE):
    chip(d,x,y,size,fg=mark,letter=letter)
    wx=x+size+size*0.34
    f=font("bold",int(size*0.52))
    ltext(d,"TRUECOAT",f,wx,y+size*0.12,word,size*0.02)
    f2=font("med",int(size*0.20))
    ltext(d,"AUCKLAND PAINTERS",f2,wx+2,y+size*0.66,sub,size*0.09)

C=json.load(open(os.path.join(OUT,"_content.json")))
def T(k): return C["tiles"][k]

# ---------------- LOGO ----------------
def a_logo(bg,mark,word,sub,name,transparent=False,letter=WHITE):
    W,H=2400,820
    img=Image.new("RGBA",(W*SS,H*SS),(0,0,0,0)) if transparent else canvas(W,H,bg)
    d=ImageDraw.Draw(img)
    size=340; x=150; y=(H-size)//2-40
    chip(d,x,y,size,fg=mark,letter=letter)
    wx=x+size+120
    f=font("bold",210); ltext(d,"TRUECOAT",f,wx,y+40,word,4)
    rule(d,wx+4,y+300,wx+ltext_w(d,"TRUECOAT",f,4),GOLD,4)
    f2=font("med",64); ltext(d,"AUCKLAND PAINTERS",f2,wx+6,y+330,sub,18)
    if transparent:
        img=img.resize((W,H),Image.LANCZOS); img.save(os.path.join(OUT,name)); print("wrote",name); return
    save(img,name)

# ---------------- HERO ----------------
def a_hero():
    W=1080; img=canvas(W,W,NAVY); d=ImageDraw.Draw(img); t=T("hero")
    M=96
    ltext(d,t["eyebrow"].upper(),font("bold",26),M,146,GOLD,6)
    rule(d,M,192,M+ltext_w(d,t["eyebrow"].upper(),font("bold",26),6),LINE_D,1.2)
    hf=font("bold",92); lines=[]
    for part in t["headline"].split("\n"): lines+=wrap(d,part,hf,W-2*M)
    y=286
    for ln in lines: text(d,ln,hf,M,y,WHITE); y+=108
    rule(d,M,y+10,M+120,GOLD,5); y+=64
    sf=font("light",37)
    for ln in wrap(d,t["sub"],sf,820): text(d,ln,sf,M,y,MUT_L); y+=50
    y+=44
    cta_line(d,M,y,t["cta"],font("bold",34),GOLD)
    lockup(d,M,W-140,mark=WHITE,word=WHITE,sub=MUT_L,size=72,letter=NAVY)
    save(img,"06_tile_hero_1080.png")

# ---------------- AVATAR (square, circle-safe) ----------------
def a_avatar():
    W=1080; img=canvas(W,W,NAVY); d=ImageDraw.Draw(img)
    size=300; cx=W//2
    chip(d,cx-size//2,300,size,fg=WHITE,letter=NAVY)
    f=font("bold",108); w=ltext_w(d,"TRUECOAT",f,6); ltext(d,"TRUECOAT",f,cx-w/2,650,WHITE,6)
    f2=font("med",34); w2=ltext_w(d,"AUCKLAND PAINTERS",f2,14); ltext(d,"AUCKLAND PAINTERS",f2,cx-w2/2,772,MUT_L,14)
    save(img,"01_profile_avatar_1080.png")

# ---------------- COVER (1640x624) ----------------
def a_cover():
    W,H=1640,624; img=canvas(W,H,NAVY); d=ImageDraw.Draw(img); t=T("hero")
    M=90
    ltext(d,"AUCKLAND · INTERIOR & EXTERIOR",font("bold",24),M,120,GOLD,5)
    rule(d,M,164,M+ltext_w(d,"AUCKLAND · INTERIOR & EXTERIOR",font("bold",24),5),LINE_D,1.2)
    f=font("bold",92); ltext(d,"TRUECOAT",f,M,210,WHITE,4)
    rule(d,M+4,326,M+ltext_w(d,"TRUECOAT",f,4),GOLD,4)
    ltext(d,C["tagline"],font("light",40),M,360,MUT_L,0)
    cta_line(d,M,470,"Free quotes across Auckland",font("bold",32),GOLD)
    chip(d,W-330,H//2-150,300,fg=NAVY2,letter=NAVY2)   # subtle brand texture
    save(img,"05_facebook_cover_1640x624.png")

# ---------------- CONTENT (paper) helpers ----------------
def _paper_header(d,W):
    lockup(d,96,84,mark=BLUE,word=INK,sub=MUT,size=58,letter=WHITE)
    rule(d,96,196,W-96,LINE,1.4)
def _paper_footer(d,W,cta,color=BLUE):
    rule(d,96,948,W-96,LINE,1.4)
    cta_line(d,96,982,cta,font("bold",30),color)
def _eyebrow_head(d,eb,h1,h2=None,y=258):
    ltext(d,eb.upper(),font("bold",26),96,y,GOLD,6)
    text(d,h1,font("bold",62),96,y+40,INK)
    if h2: text(d,h2,font("bold",62),96,y+110,INK)

def a_whyus():
    W=1080; img=canvas(W,W,PAPER); d=ImageDraw.Draw(img); t=T("whyus")
    _paper_header(d,W)
    _eyebrow_head(d,"WHY TRUECOAT","The difference","is in the prep.")
    items=t["items"]; top=480; bottom=930; n=len(items); step=(bottom-top)/n
    itf=font("med",38); y=top
    for i,it in enumerate(items):
        cy=y+step/2
        # small gold tick
        d.line([(100)*SS,(cy)*SS,(112)*SS,(cy+12)*SS],fill=GOLD,width=int(3.4*SS))
        d.line([(112)*SS,(cy+12)*SS,(134)*SS,(cy-14)*SS],fill=GOLD,width=int(3.4*SS))
        text(d,it,itf,164,cy-26,INK)
        if i<n-1: rule(d,164,y+step,W-96,LINE,1.1)
        y+=step
    _paper_footer(d,W,t["cta"])
    save(img,"08_tile_whyus_1080.png")

def a_beforeafter():
    W=1080; img=canvas(W,W,PAPER); d=ImageDraw.Draw(img); t=T("beforeafter")
    _paper_header(d,W)
    _eyebrow_head(d,"OUR WORK","See the finish.",None)
    ltext(d,t["sub"],font("light",34),96,368,MUT,0)
    for lab,x in [("BEFORE",96),("AFTER",572)]:
        rrect(d,(x,440,x+412,852),16,fill=CARD,outline=LINE,width=2)
        # simple house-line placeholder
        d.line([(x+70)*SS,(700)*SS,(x+206)*SS,(560)*SS],fill=LINE,width=int(3*SS))
        d.line([(x+206)*SS,(560)*SS,(x+342)*SS,(700)*SS],fill=LINE,width=int(3*SS))
        d.rectangle([(x+96)*SS,(700)*SS,(x+316)*SS,(800)*SS],outline=LINE,width=int(3*SS))
        ltext(d,lab,font("bold",24),x+24,466,GOLD,4)
    text(d,t["note"],font("light",26),96,884,MUT)
    save(img,"09_tile_beforeafter_1080.png")

def a_offer():
    W=1080; img=canvas(W,W,NAVY); d=ImageDraw.Draw(img); t=T("offer")
    M=96
    ltext(d,t["eyebrow"].upper(),font("bold",26),M,150,GOLD,6)
    rule(d,M,196,M+ltext_w(d,t["eyebrow"].upper(),font("bold",26),6),LINE_D,1.2)
    hf=font("bold",78); y=300
    for ln in wrap(d,t["headline"],hf,W-2*M): text(d,ln,hf,M,y,WHITE); y+=94
    rule(d,M,y+10,M+120,GOLD,5); y+=64
    sf=font("light",38)
    for ln in wrap(d,t["sub"],sf,860): text(d,ln,sf,M,y,MUT_L); y+=52
    y+=44; cta_line(d,M,y,t["cta"],font("bold",34),GOLD)
    lockup(d,M,W-140,mark=WHITE,word=WHITE,sub=MUT_L,size=72,letter=NAVY)
    save(img,"10_tile_offer_1080.png")

def _fit(d,txt,weight,start,maxw,minsz=26):
    s=start
    while s>minsz and tw(d,txt,font(weight,s))>maxw*SS: s-=1
    return font(weight,s)
def a_contact():
    W=1080; img=canvas(W,W,PAPER); d=ImageDraw.Draw(img); t=T("contact")
    _paper_header(d,W)
    _eyebrow_head(d,"GET IN TOUCH","Get your free quote.",None)
    sy=368
    for ln in wrap(d,t["sub"],font("light",34),W-192): text(d,ln,font("light",34),96,sy,MUT); sy+=46
    rows=[("SERVICE AREAS",t["areas"]),("CALL / TEXT",t["phone"]),("EMAIL",t["email"])]
    y=470; step=150
    for i,(lab,val) in enumerate(rows):
        ltext(d,lab,font("bold",22),96,y,GOLD,4)
        text(d,val,_fit(d,val,"med",40,W-192),96,y+34,INK)
        if i<len(rows)-1: rule(d,96,y+step-24,W-96,LINE,1.1)
        y+=step
    _paper_footer(d,W,t["cta"])
    save(img,"11_tile_contact_1080.png")

def a_logo_transparent():
    a_logo(WHITE,BLUE,INK,MUT,"04_logo_transparent_2400.png",transparent=True)

# ---------------- SERVICES (paper, numbered) ----------------
def a_services():
    W=1080; img=canvas(W,W,PAPER); d=ImageDraw.Draw(img); t=T("services")
    _paper_header(d,W)
    _eyebrow_head(d,"WHAT WE PAINT","Inside and out,","done properly.")
    items=t["items"]; top=480; bottom=930; n=len(items); step=(bottom-top)/n
    itf=font("med",40); y=top
    for i,it in enumerate(items):
        cy=y+step/2
        ltext(d,f"0{i+1}",font("bold",26),96,cy-38,GOLD,2)
        text(d,it,itf,176,cy-28,INK)
        if i<n-1: rule(d,176,y+step,W-96,LINE,1.1)
        y+=step
    _paper_footer(d,W,t["cta"])
    save(img,"07_tile_services_1080.png")

if __name__=="__main__":
    a_avatar()
    a_logo(WHITE,BLUE,INK,MUT,"02_logo_on-white_2400.png",letter=WHITE)
    a_logo(NAVY,WHITE,WHITE,MUT_L,"03_logo_on-blue_2400.png",letter=NAVY)
    a_logo_transparent()
    a_cover()
    a_hero()
    a_services()
    a_whyus()
    a_beforeafter()
    a_offer()
    a_contact()
    print("v2 full kit ->",OUT)
