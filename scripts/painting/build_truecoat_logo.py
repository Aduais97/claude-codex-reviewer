#!/usr/bin/env python3
"""Truecoat logo — Sensation-style system (ref: circular line-monogram + two-line width-matched
wordmark + small tagline). TWO COLOURS ONLY: white + True Blue. No gold, no illustration."""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.expanduser("~/Desktop/Painting/Truecoat - Facebook Marketplace Kit")
SS = 4
BLUE = (30, 62, 180); WHITE = (255, 255, 255)
HN = "/System/Library/Fonts/HelveticaNeue.ttc"; IDX = {"bold":1,"med":10,"reg":0,"light":7}
_fc = {}
def font(w, s):
    k=(w,s)
    if k not in _fc: _fc[k]=ImageFont.truetype(HN,int(s*SS),index=IDX[w])
    return _fc[k]
def cw(d,ch,f): b=d.textbbox((0,0),ch,font=f,anchor="la"); return (b[2]-b[0])/SS
def ltext(d,t,f,x,ytop,fill,tr):
    """left, tracking tr, y=ascender-top (anchor la). returns width."""
    cx=x
    for ch in t:
        d.text((cx*SS,ytop*SS),ch,font=f,fill=fill,anchor="la"); cx+=cw(d,ch,f)+tr
    return cx-x-tr
def ltext_w(d,t,f,tr): return sum(cw(d,ch,f)+tr for ch in t)-tr
def track_to(d,t,f,target):
    base=ltext_w(d,t,f,0); return (target-base)/(len(t)-1) if len(t)>1 else 0

def monogram(d, cx, cy, D, color, w=None):
    """Thin outer ring + interlocked 'TC' (C = open arc on the right, T over it)."""
    w=w or D*0.05; s=SS; R=D/2
    def bb(r): return [(cx-r)*s,(cy-r)*s,(cx+r)*s,(cy+r)*s]
    d.ellipse(bb(R), outline=color, width=int(w*s))
    d.arc(bb(R*0.63), 50, 310, fill=color, width=int(w*s))            # C
    barw=D*0.34; ty=cy-D*0.16; stemh=D*0.42
    d.line([(cx-barw/2)*s, ty*s, (cx+barw/2)*s, ty*s], fill=color, width=int(w*s))   # T bar
    d.line([cx*s, ty*s, cx*s, (ty+stemh)*s], fill=color, width=int(w*s))            # T stem

def wordmark(d, x, cy, color, sub, big):
    """TRUE over COAT (width-matched) + tagline, vertically centred on cy. Returns block width."""
    fb=font("bold",big)
    w1=ltext_w(d,"TRUE",fb,0)
    fc=font("bold",big); ctrk=track_to(d,"COAT",fc,w1)
    tag="YOUR TRUSTED AUCKLAND PAINTERS"; ft=font("med",big*0.15); ttrk=track_to(d,tag,ft,w1)
    l1=big*0.80; gap_tag=big*0.42                       # line-to-line, and gap before tagline
    total=l1 + l1 + gap_tag + big*0.15                  # TRUE + COAT + gap + tagline height
    y=cy-total/2
    ltext(d,"TRUE",fb,x,y,color,0)
    ltext(d,"COAT",fc,x,y+l1,color,ctrk)
    ltext(d,tag,ft,x,y+2*l1+gap_tag,sub,ttrk)
    return w1

def build(bg, fg, sub, name, transparent=False):
    W,H=2400,900
    img=Image.new("RGBA",(W*SS,H*SS),(0,0,0,0)) if transparent else Image.new("RGB",(W*SS,H*SS),bg)
    d=ImageDraw.Draw(img)
    D=430; mx=250; cy=H/2
    monogram(d, mx, cy, D, fg)
    wordmark(d, mx+D/2+150, cy, fg, sub, 150)
    img=img.resize((W,H),Image.LANCZOS); img.save(os.path.join(OUT,name)); print("wrote",name)

def build_mark(bg, fg, name, wordmark_too=True):
    S=1080
    img=Image.new("RGB",(S*SS,S*SS),bg); d=ImageDraw.Draw(img)
    if wordmark_too:
        monogram(d, S/2, S/2-70, 470, fg)
        big=132; fb=font("bold",big); w1=ltext_w(d,"TRUECOAT",fb,0)
        ltext(d,"TRUECOAT",fb,S/2-w1/2,S/2+250,fg,0)
        tag="AUCKLAND PAINTERS"; ft=font("med",big*0.30); ttrk=track_to(d,tag,ft,w1)
        ltext(d,tag,ft,S/2-w1/2,S/2+250+big*0.92,fg,ttrk)
    else:
        monogram(d, S/2, S/2, 620, fg)
    img=img.resize((S,S),Image.LANCZOS); img.save(os.path.join(OUT,name)); print("wrote",name)

if __name__=="__main__":
    build(BLUE, WHITE, (200,210,240), "logo_primary_on-blue_2400.png")
    build(WHITE, BLUE, (95,110,190), "logo_on-white_2400.png")
    build(None, WHITE, (200,210,240), "logo_transparent_white_2400.png", transparent=True)
    build(None, BLUE, (95,110,190), "logo_transparent_blue_2400.png", transparent=True)
    build_mark(BLUE, WHITE, "logo_avatar_on-blue_1080.png")
    build_mark(WHITE, BLUE, "logo_mark_on-white_1080.png")
    print("logo set ->", OUT)
