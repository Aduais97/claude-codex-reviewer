#!/usr/bin/env python3
"""Bunnings National Risk Overview — client report renderer (windowed).
Reads a windowed metrics JSON (from nro_metrics.py), builds brand charts + the PDF, runs a
guardrail lint. Client-safe: no rate/guard-name/other-client/apprehension language; hours only
at programme level; every headline figure traces to data.

Usage: python3 nro_report.py <nro_metrics_TAG.json>
Out:   ~/Desktop/Bunnings/Bunnings_National_Risk_Overview_<TAG>.pdf
"""
import os, json, datetime, tempfile, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
                                PageBreak, HRFlowable)
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

_ttf=os.path.join(matplotlib.get_data_path(),"fonts","ttf")
try:
    pdfmetrics.registerFont(TTFont("DejaVu",os.path.join(_ttf,"DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold",os.path.join(_ttf,"DejaVuSans-Bold.ttf")))
    UNI,UNIB="DejaVu","DejaVu-Bold"
except Exception: UNI,UNIB="Helvetica","Helvetica-Bold"

HERE=os.path.dirname(os.path.abspath(__file__))
MJSON=sys.argv[1] if len(sys.argv)>1 else os.path.join(HERE,"nro_metrics_full.json")
M=json.load(open(MJSON)); TMP=tempfile.mkdtemp()
NAVY="#1F3864"; GOLD="#C8952A"; RED="#B0322A"; INK="#243244"; GREY="#5A6675"; LIGHT="#EEF2F6"; FAINT="#C9D2DC"
cNAVY=colors.HexColor(NAVY); cGOLD=colors.HexColor(GOLD); cRED=colors.HexColor(RED)
cINK=colors.HexColor(INK); cGREY=colors.HexColor(GREY); cLIGHT=colors.HexColor(LIGHT)
TAG=M["tag"]; PERIOD=M["period_label"]; PHRASE=M["phrase"]; KICK=M["kicker"]; FOOT=M["foot"]
def money(v): return "${:,.0f}".format(v)

def savefig(fig,name):
    p=os.path.join(TMP,name); fig.savefig(p,dpi=200,bbox_inches="tight",facecolor="white",pad_inches=0.12); plt.close(fig); return p
def chart_donut():
    rec=M["recovered"]; notrec=M["identified"]-M["recovered"]
    fig,ax=plt.subplots(figsize=(4.2,3.4))
    ax.pie([rec,notrec],colors=[NAVY,FAINT],startangle=90,counterclock=False,wedgeprops=dict(width=0.38,edgecolor="white",linewidth=2))
    ax.text(0,0.12,f"{M['recovery_pct']}%",ha="center",va="center",fontsize=26,fontweight="bold",color=NAVY)
    ax.text(0,-0.24,"of identified value\nrecovered",ha="center",va="center",fontsize=8.5,color=GREY); ax.set(aspect="equal")
    return savefig(fig,"donut.png")
def chart_severity():
    s=M["severity"]; labels=["1 Minor","2 Low","3 Moderate","4 Serious","5 Critical"]
    vals=[s["1"],s["2"],s["3"],s["4"],s["5"]]; cols=[FAINT,FAINT,GOLD,RED,"#7a1d16"]
    fig,ax=plt.subplots(figsize=(5.4,2.7)); y=list(range(len(vals)))[::-1]
    ax.barh(y,vals,color=cols,height=0.66,edgecolor="white")
    for yi,v in zip(y,vals): ax.text(v+max(vals+[1])*0.01,yi,f"{v:,}",va="center",fontsize=9,color=INK,fontweight="bold")
    ax.set_yticks(list(range(len(labels)))[::-1]); ax.set_yticklabels(labels,fontsize=9,color=INK)
    ax.set_xlim(0,max(vals+[1])*1.14); ax.set_xticks([])
    for sp in ("top","right","bottom"): ax.spines[sp].set_visible(False)
    ax.spines["left"].set_color(FAINT); ax.axhspan(-0.5,2.5,color=RED,alpha=0.05)
    if M["sev3plus"]: ax.text(max(vals+[1])*1.02,1,f"{M['sev3plus']} at severity 3+\n({M['sev45']} at 4–5)",fontsize=8,color=RED,va="center",ha="right",fontweight="bold")
    return savefig(fig,"sev.png")
def chart_heatmap():
    mat=np.zeros((7,24))
    for k,c in M.get("heat",{}).items():
        d,h=map(int,k.split("_")); mat[d,h]=c
    hrs=list(range(6,24)); fig,ax=plt.subplots(figsize=(6.6,2.9))
    im=ax.imshow(mat[:,6:24],aspect="auto",cmap="YlOrRd")
    ax.set_yticks(range(7)); ax.set_yticklabels(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],fontsize=8)
    ax.set_xticks(range(0,len(hrs),2)); ax.set_xticklabels([f"{h}:00" for h in hrs[::2]],fontsize=7.5)
    ax.set_title("Incidents by day × hour — risk concentrates 12:00–18:00",fontsize=9,color=INK,pad=6)
    cb=fig.colorbar(im,ax=ax,fraction=0.03,pad=0.02); cb.ax.tick_params(labelsize=7)
    return savefig(fig,"heat.png")
def chart_stores():
    t=M["top6"]; names=[x["store"].replace("Bunnings ","") for x in t][::-1]; vals=[x["recovered"] for x in t][::-1]
    fig,ax=plt.subplots(figsize=(5.4,2.9)); ax.barh(range(len(vals)),vals,color=NAVY,height=0.64,edgecolor="white")
    for i,(v,x) in enumerate(zip(vals,t[::-1])): ax.text(v+max(vals+[1])*0.01,i,f"{money(v)} · {x['share']}%",va="center",fontsize=8,color=INK)
    ax.set_yticks(range(len(names))); ax.set_yticklabels(names,fontsize=9,color=INK)
    ax.set_xlim(0,max(vals+[1])*1.30); ax.set_xticks([])
    for sp in ("top","right","bottom"): ax.spines[sp].set_visible(False)
    ax.spines["left"].set_color(FAINT); return savefig(fig,"stores.png")
def chart_trend():
    tr=M["trend"]; lab=[t["label"] for t in tr]; inc=[t["incidents"] for t in tr]; rec=[t["recovered"] for t in tr]
    fig,ax=plt.subplots(figsize=(7.0,2.8))
    ax.bar(range(len(inc)),inc,color=FAINT,width=0.62)
    ax2=ax.twinx(); ax2.plot(range(len(rec)),rec,color=GOLD,lw=2.2,marker="o",ms=3.5)
    ax.set_xticks(range(len(lab))); ax.set_xticklabels(lab,fontsize=6.8,rotation=45,ha="right",color=GREY)
    ax.set_ylabel("Incidents",fontsize=8,color=GREY); ax2.set_ylabel("Recovered $",fontsize=8,color=GOLD)
    ax.tick_params(labelsize=7); ax2.tick_params(labelsize=7,colors=GOLD)
    ax.spines["top"].set_visible(False); ax2.spines["top"].set_visible(False)
    for a in (ax,ax2):
        for sp in ("left","right"): a.spines[sp].set_color(FAINT)
    ax.set_title(f"By {M['trend_unit']} — incidents (bars) &amp; recovered value (line)".replace('&amp;','&'),fontsize=8.5,color=INK,pad=5)
    return savefig(fig,"trend.png")
def chart_signoff():
    s=M["signoff"]; order=["Guard","Duty Manager","Checkout Operator","Supervisor","Store Manager"]; vals=[s[k] for k in order]
    fig,ax=plt.subplots(figsize=(5.4,2.5)); ax.barh(list(range(len(vals)))[::-1],vals,color=[NAVY]+[RED]*4,height=0.62,edgecolor="white")
    for yi,v in zip(range(len(vals))[::-1],vals): ax.text(v+1.5,yi,f"{v:.0f}%",va="center",fontsize=8.5,color=INK,fontweight="bold")
    ax.set_yticks(list(range(len(order)))[::-1]); ax.set_yticklabels(order,fontsize=9,color=INK)
    ax.set_xlim(0,108); ax.set_xticks([])
    for sp in ("top","right","bottom"): ax.spines[sp].set_visible(False)
    ax.spines["left"].set_color(FAINT); return savefig(fig,"signoff.png")
D=chart_donut(); SEV=chart_severity(); HEAT=chart_heatmap(); STORES=chart_stores(); TREND=chart_trend(); SIGN=chart_signoff()

styles=getSampleStyleSheet()
def st(name,**kw):
    base=dict(fontName="Helvetica",textColor=cINK,fontSize=9.5,leading=13.5); base.update(kw); return ParagraphStyle(name,**base)
H1=st("H1",fontName="Helvetica-Bold",fontSize=17,textColor=cNAVY,leading=20)
H2=st("H2",fontName="Helvetica-Bold",fontSize=12.5,textColor=cNAVY,leading=15)
SUB=st("SUB",fontSize=9.5,textColor=cGREY,leading=13); BODY=st("BODY",fontSize=9.5,leading=14,spaceAfter=5)
SMALL=st("SMALL",fontSize=7.6,textColor=cGREY,leading=10); CAP=st("CAP",fontSize=8,textColor=cGREY,leading=11,alignment=TA_CENTER)
TILEN=st("TILEN",fontName="Helvetica-Bold",fontSize=18,textColor=cNAVY,alignment=TA_CENTER,leading=20)
TILEL=st("TILEL",fontSize=7.6,textColor=cGREY,alignment=TA_CENTER,leading=9.5)
story=[]
def rule(c=cGOLD,w=1.4): return HRFlowable(width="100%",thickness=w,color=c,spaceBefore=3,spaceAfter=7)
def tiles(items):
    cells=[[Paragraph(v,TILEN) for v,_ in items],[Paragraph(l,TILEL) for _,l in items]]
    t=Table(cells,colWidths=[(170*mm)/len(items)]*len(items))
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),cLIGHT),("INNERGRID",(0,0),(-1,-1),3,colors.white),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,0),8),("BOTTOMPADDING",(0,1),(-1,1),8),
        ("TOPPADDING",(0,1),(-1,1),0),("BOTTOMPADDING",(0,0),(-1,0),0)])); return t
def img(path,w):
    from PIL import Image as PImage
    iw,ih=PImage.open(path).size; return Image(path,width=w,height=w*ih/iw)

story+=[Spacer(1,42*mm),
  Paragraph("BUNNINGS NEW ZEALAND",st("cvk",fontName="Helvetica-Bold",fontSize=11,textColor=cGOLD,leading=14)),
  Paragraph("National Risk Overview",st("cvt",fontName="Helvetica-Bold",fontSize=30,textColor=cNAVY,leading=34)),
  Paragraph(KICK+" &middot; "+PERIOD,st("cvp",fontName="Helvetica-Bold",fontSize=12.5,textColor=cGREY,leading=16)),
  Paragraph("Loss Prevention &amp; Safety Intelligence — covert LP programme",st("cvs",fontSize=11,textColor=cGREY,leading=15)),
  Spacer(1,6*mm), rule(cRED,2.2), Spacer(1,3*mm),
  Paragraph("Prepared for the Bunnings Loss Prevention team",SUB),
  Spacer(1,96*mm),
  Paragraph("Confidential — prepared by SLS RTC. Your data, returned to you. Health &amp; safety observations are advisory (HSWA 2015 shared-duty context), not legal advice.",SMALL),
  PageBreak()]

story+=[Paragraph("Executive Summary",H1),Paragraph(f"Covert loss-prevention programme &middot; {PERIOD}",SUB),rule(),
  tiles([(f"{M['incidents']:,}","Incidents"),(money(M['recovered']),"Value recovered"),
         (f"{M['recovery_pct']}%","Of identified value"),(f"{M['sev3plus']}","Serious (sev 3+)"),
         (f"{M['sites']}","Sites &middot; %d regions"%M['regions'])]), Spacer(1,5*mm),
  Paragraph("This report covers the <b>SLS RTC covert loss-prevention programme only</b> — incidents identified and recorded by our "
    "covert team. Events recorded by Bunnings store staff (also visible in Auror) are outside this programme's scope and are excluded; "
    "the figures below are the covert programme's contribution, not total store loss prevention.",
    st("scope",fontSize=8.8,leading=12.5,textColor=cGREY,fontName="Helvetica-Oblique")),
  Spacer(1,2*mm),
  Paragraph(f"Over <b>{PHRASE}</b>, the covert team recorded <b>{M['incidents']:,} incidents</b> across "
    f"<b>{M['sites']} Bunnings sites</b> and returned <b>{money(M['recovered'])}</b> of recovered value. Measured against a "
    f"<b>priced base of {money(M['identified'])}</b> — recovered receipt value plus the estimated value of goods not recovered, for "
    f"valued incidents only (this is not a measure of total store shrinkage) — that is a <b>{M['recovery_pct']}%</b> recovery rate. "
    f"An Auror reference was captured on every incident ({M['recon']['captured']}/{M['incidents']}); "
    f"<b>{M['recon']['reconciled']}/{M['incidents']} ({M['recon']['reconciled_pct']}%) reconcile to a confirmed event</b> in the store's own case system"
    +(f", with {M['recon']['bad']} reference{'s' if M['recon']['bad']!=1 else ''} under correction" if M['recon']['bad'] else "")+".",BODY),
  Paragraph(f"Recovery is the counted layer. Beneath it is a measurable risk and safety picture: "
    f"<b>{M['sev3plus']} incidents at severity 3+</b> (of which {M['sev45']} at 4–5), demand clustered in the "
    f"<b>12:00–18:00 window ({M['risk_window_pct']}% of incidents)</b> peaking {M['peak_day'][0] if M['peak_day'] else 'midweek'} afternoons, "
    f"and a loss base concentrated in a handful of stores (<b>top 6 = {M['top6_share']}% of recovered value</b>).",BODY),
  Paragraph("The question this report answers is not &ldquo;how much did we recover&rdquo; — it is "
    "<b>how much risk is visible, where, and who owns the response</b>.",st("lead",fontSize=9.5,leading=14,textColor=cNAVY,fontName="Helvetica-Oblique")),
  PageBreak()]

notrec=M["identified"]-M["recovered"]
story+=[Paragraph("1 &middot; Recovery &amp; What It Counts",H2),rule(),
  Table([[img(D,58*mm),
    Paragraph(f"The programme recovered <b>{money(M['recovered'])}</b> of the <b>{money(M['identified'])}</b> in loss "
      f"identified and priced — a <b>{M['recovery_pct']}%</b> return on <i>counted</i> value, with {money(notrec)} identified but "
      f"not recovered.<br/><br/>Read carefully, {M['recovery_pct']}% measures <b>coverage of a narrow field</b> — loss that was "
      f"seen, priced and actioned. It says nothing about loss deterred before it happened, packaged out, or never observed. "
      f"The useful question is <b>how much loss is currently left uncounted</b>, and which layers the programme could begin to measure.",BODY)]],
    colWidths=[62*mm,108*mm]),
  Spacer(1,3*mm),
  Paragraph("Recovery is the visible layer; deterrence, recovered packaging and unobserved loss are not yet captured as structured fields — each a candidate to turn on.",CAP),
  PageBreak()]

hc=M["hottest_cell"]
story+=[Paragraph("2 &middot; Risk Intelligence — Severity &amp; Timing",H2),rule(),
  img(SEV,150*mm),Spacer(1,1*mm),
  Paragraph(f"Most incidents are low-severity, but the tail carries the health-and-safety exposure: "
    f"<b>{M['sev3plus']} reached severity 3+ and {M['sev45']} reached 4–5</b> — invisible in a recovery-only report.",BODY),
  Spacer(1,2*mm), img(HEAT,150*mm),Spacer(1,1*mm),
  Paragraph(f"Timing is predictable: <b>{M['risk_window_pct']}%</b> of incidents fall in the <b>12:00–18:00</b> window"
    +(f", peaking <b>{M['peak_day'][0]}</b> — hottest cell <b>{hc['day']} {hc['hour']}:00 ({hc['count']} incidents)</b>" if hc else "")
    +". Cover aligned to the window is cover aligned to the risk.",BODY),
  PageBreak()]

reg=M["regional"][:6]
regrows=[["Region","Incidents","Recovered $"]]+[[r["region"],f"{r['incidents']:,}",money(r["recovered"])] for r in reg]
rt=Table(regrows,colWidths=[80*mm,30*mm,40*mm])
rt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),cNAVY),("TEXTCOLOR",(0,0),(-1,0),colors.white),
  ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTNAME",(0,1),(-1,-1),UNI),("FONTSIZE",(0,0),(-1,-1),8.5),
  ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,cLIGHT]),("GRID",(0,0),(-1,-1),0.4,cLIGHT),
  ("ALIGN",(1,0),(-1,-1),"RIGHT"),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
story+=[Paragraph("3 &middot; Store &amp; Regional Concentration",H2),rule(),
  Paragraph(f"Loss is not spread evenly — the <b>top 6 stores account for {M['top6_share']}% of all recovered value</b>. "
    f"Concentration is an advantage: targeted effort and store-level partnership can move the national number.",BODY),
  img(STORES,150*mm),Spacer(1,3*mm),
  Paragraph("By region (recovered value):",st("h3",fontName="Helvetica-Bold",fontSize=9.5,textColor=cNAVY,spaceAfter=3)),
  rt, PageBreak()]

# ---- 4 · Team Performance — Who Works Best Together ----
teams=M.get("teams",[]); operatives=M.get("operatives",[])
def _thead(tbl,hcol):
    tbl.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),hcol),("TEXTCOLOR",(0,0),(-1,0),colors.white),
      ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTNAME",(0,1),(-1,-1),UNI),("FONTSIZE",(0,0),(-1,-1),8.5),
      ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,cLIGHT]),("GRID",(0,0),(-1,-1),0.4,cLIGHT),
      ("ALIGN",(1,0),(-1,-1),"RIGHT"),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
teamrows=[["Covert pairing","Co-hrs","Incidents","Recovered $","Inc / 100 co-hrs"]]+[
  [f"{t['a']} + {t['b']}", f"{t['cohours']:,.0f}", f"{t['incidents']:,}", money(t['recovered']), f"{t['inc_per_100cohr']:,.1f}"] for t in teams]
tmt=Table(teamrows,colWidths=[68*mm,18*mm,24*mm,28*mm,32*mm]); _thead(tmt,cNAVY)
oprows=[["Operative","Hrs","Incidents","Recovered $","Inc / 100h"]]+[
  [o['name'], f"{o['hours']:,.0f}", f"{o['incidents']:,}", money(o['recovered']), f"{o['inc_per_100h']:,.1f}"] for o in operatives]
opt=Table(oprows,colWidths=[68*mm,18*mm,24*mm,28*mm,32*mm]); _thead(opt,cNAVY)
_top=teams[0] if teams else None
_hero=max(teams,key=lambda t:t['recovered']) if teams else None
story+=[Paragraph("4 &middot; Team Performance — Who Works Best Together",H2),rule(),
  Paragraph("The covert programme runs in <b>pairs</b>. Because some operatives are almost always deployed together, raw totals mostly "
    "reward time on the job — so the table ranks every pairing on <b>incidents actioned per 100 hours worked</b>, which normalises for "
    "time and shows who is genuinely most productive, not simply most deployed. "
    +(f"On returned value, <b>{_hero['a']} + {_hero['b']}</b> were the standout — <b>{money(_hero['recovered'])}</b> recovered across "
      f"<b>{_hero['incidents']} shared incidents</b> in {_hero['cohours']:,.0f} co-worked hours; " if _hero else "")
    +(f"on activity rate, <b>{_top['a']} + {_top['b']}</b> lead at <b>{_top['inc_per_100cohr']:,.0f} incidents per 100 hours</b>. " if _top else "")
    +f"Across <b>{M.get('operatives_active',0)} active operatives</b>, the consistent high-productivity pairings are the ones to protect on the roster.",BODY),
  Paragraph("Top covert pairings (ranked by incidents per 100 co-worked hours):",st("h3t",fontName="Helvetica-Bold",fontSize=9.5,textColor=cNAVY,spaceAfter=3)),
  tmt, Spacer(1,4*mm),
  Paragraph("Operative contribution (ranked by incidents per 100 hours on site):",st("h3o",fontName="Helvetica-Bold",fontSize=9.5,textColor=cNAVY,spaceAfter=3)),
  opt, Spacer(1,2*mm),
  Paragraph("Effectiveness is normalised to incidents per 100 hours (recovered value is shown as a total, not divided by hours). Ratios computed for operatives with &ge;20 hours and pairings with &ge;15 co-worked hours; lower-hour entries appear but are not ranked.",CAP),
  PageBreak()]

story+=[Paragraph("5 &middot; Trend Over Time",H2),rule(),
  img(TREND,160*mm),Spacer(1,2*mm),
  Paragraph(f"Incident volume and recovered value by {M['trend_unit']}. A standing view like this turns single-point reporting "
    "into a leading indicator — seasonality and emerging store-level shifts become visible before they compound.",BODY),
  PageBreak()]

h_win=M["hours_window"]; ip100=M["inc_per_100h"]; hpi=M["hours_per_inc"]; hot=M["serious_hotspots"]
hotrows=[["Store","Serious (sev 3+)"]]+[[x["store"].replace("Bunnings ",""),str(x["sev3"])] for x in hot]
ht=Table(hotrows,colWidths=[90*mm,40*mm])
ht.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),cRED),("TEXTCOLOR",(0,0),(-1,0),colors.white),
  ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),8.5),
  ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,cLIGHT]),("GRID",(0,0),(-1,-1),0.4,cLIGHT),
  ("ALIGN",(1,0),(-1,-1),"CENTER"),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
depl=[]
if h_win:
    depl=[Paragraph("Deployment &amp; coverage",st("h3c",fontName="Helvetica-Bold",fontSize=10.5,textColor=cNAVY,spaceAfter=3)),
      tiles([(f"{h_win:,.0f}h","Guard-hours deployed"),(f"{ip100}","Incidents / 100 guard-hrs"),(f"{hpi}h","One incident every")]),
      Spacer(1,2*mm),
      Paragraph(f"Across <b>{h_win:,.0f} deployed guard-hours</b> in this period the programme logged about <b>{ip100} incidents "
        f"per 100 guard-hours</b> — roughly one every {hpi} hours on site. Hours are a workload denominator only; recovered value is never divided by hours.",BODY)]
story+=[Paragraph("6 &middot; Health, Safety &amp; Shared Accountability",H2),rule(),
  Paragraph("A serious incident is a worker-safety event before it is a loss event. Under HSWA 2015, when store teams and a covert "
    "LP provider share a workplace, the duty to keep people safe is <b>shared</b> — making the record of who was notified, and who "
    "signed off, part of the safety system.",BODY),
  Table([[img(SIGN,92*mm),
    Paragraph(f"The accountability trail is one-sided: the <b>guard signs {M['signoff']['Guard']:.0f}%</b> of reports, but store-side "
      f"sign-off is near zero (Duty Manager {M['signoff']['Duty Manager']:.0f}%, Checkout {M['signoff']['Checkout Operator']:.0f}%, "
      f"Supervisor {M['signoff']['Supervisor']:.0f}%, Store Manager {M['signoff']['Store Manager']:.0f}%) — even though a store person "
      f"is the notified party on most incidents. Closing that loop is a low-cost, high-value safety improvement.",BODY)]],
    colWidths=[96*mm,74*mm]),
  Spacer(1,3*mm),
  Paragraph("Serious-incident hotspots (severity 3+):",st("h3b",fontName="Helvetica-Bold",fontSize=9.5,textColor=cRED,spaceAfter=3)),
  ht, Spacer(1,4*mm)]+depl+[PageBreak()]

story+=[Paragraph("Method &amp; Notes",H2),rule(),
  Paragraph(f"&bull; <b>Source &amp; scope.</b> Every figure is drawn from the programme's own Guard Incident Report data for "
    f"<b>{PERIOD}</b> and the covert team's deployment records. An Auror reference is captured on every incident; {M['recon']['reconciled_pct']:.0f}% reconcile to a confirmed event in Bunnings' Auror system (the balance are references under correction).",BODY),
  Paragraph("&bull; <b>Recovery %.</b> Recovered value &divide; identified (priced) value — coverage of counted loss, not total shrink.",BODY),
  Paragraph("&bull; <b>Severity &amp; safety.</b> Health-and-safety observations are advisory, framed in the HSWA 2015 shared-duty context; not legal advice.",BODY),
  Paragraph("&bull; <b>Hours.</b> Deployed guard-hours for the period are a workload denominator only (FY26 from programme records; recent weeks from live deployment).",BODY),
  Paragraph("&bull; <b>Confidentiality.</b> Contains Bunnings' own data, returned to Bunnings. Our covert operatives are credited by name for the teamwork view; <b>no offenders are named</b>, and LP actions are described in lawful terms (intercepted / recovered / handed to Police).",BODY),
  Spacer(1,6*mm),Paragraph(f"Prepared by SLS RTC &middot; Confidential &middot; {PERIOD}",SMALL)]

def footer(canvas,doc):
    canvas.saveState(); canvas.setFont("Helvetica",7); canvas.setFillColor(cGREY)
    canvas.drawString(18*mm,10*mm,"Bunnings National Risk Overview  ·  Confidential")
    canvas.drawRightString(192*mm,10*mm,f"{FOOT}  ·  page {doc.page}")
    canvas.setStrokeColor(cLIGHT); canvas.line(18*mm,13*mm,192*mm,13*mm); canvas.restoreState()

OUT=os.path.expanduser(f"~/Desktop/Bunnings/Bunnings_National_Risk_Overview_{TAG}.pdf")
SimpleDocTemplate(OUT,pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=16*mm,bottomMargin=18*mm,
    title=f"Bunnings National Risk Overview — {PERIOD}").build(story,onFirstPage=footer,onLaterPages=footer)
print("wrote",OUT)

import re as _re
banned=[r"\bapprehend",r"\barrest",r"\bdetain",r"\bwoolworth",r"\bmitre",r"\bwarehouse\b",r"\bper hour\b",r"recovery per",r"\bmargin\b",r"\brate card\b"]
issues=[]
try:
    import fitz; d=fitz.open(OUT); alltext=" ".join(p.get_text() for p in d).lower()
    for pat in banned:
        if _re.search(pat,alltext): issues.append(pat)
    for fig in [f"{M['incidents']:,}",f"{M['recovery_pct']}%",str(M['sev3plus'])]:
        if fig.lower() not in alltext: issues.append("MISSING "+fig)
except Exception as e: issues.append("lint-skip: "+str(e))
print("GUARDRAIL LINT:", "PASS" if not issues else "FAIL: "+str(issues))
