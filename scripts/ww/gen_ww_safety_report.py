#!/usr/bin/env python3
"""Woolworths National LP — consolidated H&S-led weekly report (ONE PDF).
Replaces the separate Value Report + National LP Dashboard for the client send.
Focus: worker/customer SAFETY first, a simple loss overview (recovered goods /
recovered packaging / not recovered / total loss), top-5 stores per region
(Total Loss / Recovered / Incidents), and an anonymised incidents showcase.
The Deployment & Recovery Tracker xlsx carries the full detail — this PDF stays lean.

Weekly curation: update INCIDENTS below from the week's notable GIR rows (anonymised,
legally-safe verbs only: observed / intercepted / recovered / deterred / de-escalated /
issued trespass / handed to Police — NEVER apprehended/arrested/detained; no names).
"""
import os, re, openpyxl
from datetime import datetime
from collections import Counter, defaultdict
import build_master_v2 as bm
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    Table, TableStyle, HRFlowable, KeepTogether)

WK = bm.CURRENT_WEEK; WLABEL = bm.week_label(WK); WNUM = bm.week_num(WK)
NAVY=HexColor("#1E2A3A"); NAVY2=HexColor("#2C3E52"); GREEN=HexColor("#00843D"); GOLD=HexColor("#C8952A")
RED=HexColor("#C0392B"); BORDER=HexColor("#C9D2DC"); ROWALT=HexColor("#F3F6F9"); LABELBG=HexColor("#EAEEF3")
TDARK=HexColor("#1A1A2E"); TMED=HexColor("#4A5568"); TLIGHT=HexColor("#8A97A6"); WHITE=HexColor("#FFFFFF")
CW=487.0
OUTDIR=os.path.expanduser(f"~/Desktop/Woolworths /Week Ending {WLABEL}")
OUT=f"{OUTDIR}/Woolworths National LP & Safety Report - Week Ending {WLABEL}.pdf"

# ---------- data: loss overview + top-5 per region (from reconciled master) ----------
agg,sreg,regs=bm.aggregate()
active=[(s,a) for (w,s),a in agg.items() if w==WK]
nat=bm.rollup([a for s,a in active])
REC=nat['rec']; PKG=nat['pkg']; LOST=nat['lost']; TL=REC+PKG+LOST
TOTREC=REC+PKG; RECPCT=100*TOTREC/TL if TL else 0

# ---------- data: H&S metrics from the week's GIR ----------
def num(v):
    if v is None: return 0.0
    x=re.sub(r'[^0-9.]','',str(v)); return float(x) if x else 0.0
def yes(v): return str(v).strip().lower() in ('yes','y','true')
T={"date":"Date and Time of Incident - Date","sev":"Incident Severity","off":"Number of offenders/POI",
   "beh":"Type of non-compliant behaviour","pol":"Were the police informed?","vt":"Verbal Trespass",
   "ft":"Formal Trespass Notice Served","cat":"Incident Category",
   "site":"Select Woolworths Site","rec":"Recovered Reciept Value","desc":"Incident Description"}
sev=Counter(); off_tot=0; inc=0; pol=vt=ft=0; confront=0; beh_tally=Counter()
AGG={"aggressive behaviour","threatening language/behaviour","violent behaviour","verbal abuse"}
gir_seen={}
for path,lo,hi in bm.GIR_SOURCES:
    ws=openpyxl.load_workbook(path,read_only=True).active; it=ws.iter_rows(values_only=True)
    low=[str(h).strip().lower() if h else "" for h in next(it)]
    col={k:next((i for i,h in enumerate(low) if h==v.lower()),
               next((i for i,h in enumerate(low) if v.lower() in h),None)) for k,v in T.items()}
    def g(r,k):
        i=col.get(k); return r[i] if i is not None and i<len(r) else None
    for r in it:
        d=bm.pdate(g(r,"date"))
        if not d or bm.week_of(d)!=WK: continue
        if not(lo is None or d>=lo) or not(hi is None or d<=hi): continue
        if bm.dup_seen(gir_seen, str(g(r,"site") or "").strip(), d, num(g(r,"rec")), int(num(g(r,"off")) or 1), g(r,"desc")): continue
        inc+=1
        if g(r,"sev"): sev[str(g(r,"sev")).strip()]+=1
        off_tot+=int(num(g(r,"off")) or 0)
        if yes(g(r,"pol")): pol+=1
        if yes(g(r,"vt")): vt+=1
        if yes(g(r,"ft")): ft+=1
        tags=[t.strip().lower() for t in re.split(r'[;,]',str(g(r,"beh") or ""))]
        if any(t in AGG for t in tags): confront+=1
        for t in tags:
            if t in AGG: beh_tally[t.title()]+=1
SERIOUS=sum(sev.get(k,0) for k in ('3','4','5')); SEVERE=sev.get('4',0)+sev.get('5',0)
# Severity-aware clause (mirrors gen_value_report.py): the blanket "without physical
# intervention" claim must not appear in a week with a severity-5 (physical) incident.
_S5 = sev.get('5', 0)
if _S5 == 0:
    PHYS_CLAUSE = "each managed without physical intervention"
elif _S5 == 1:
    PHYS_CLAUSE = ("managed with de-escalation first; one incident reached severity 5, where an "
                   "offender became physically aggressive toward the team — the team de-escalated "
                   "and the matter was escalated to Police")
else:
    PHYS_CLAUSE = (f"managed with de-escalation first; {_S5} incidents reached severity 5, where "
                   "offenders became physically aggressive toward the team — each was escalated "
                   "to Police")

# ---------- curated incidents (shared module — anonymised, legally-safe) ----------
from ww_incidents import INCIDENTS

# ---------- styles ----------
body=ParagraphStyle("body",fontName="Helvetica",fontSize=9.5,leading=13.5,textColor=TDARK,alignment=TA_JUSTIFY,spaceAfter=6)
lead=ParagraphStyle("lead",parent=body,fontSize=10,leading=14,textColor=NAVY2,spaceAfter=8)
cell=ParagraphStyle("cell",fontName="Helvetica",fontSize=8.7,leading=11.5,textColor=TDARK)
cellb=ParagraphStyle("cellb",parent=cell,fontName="Helvetica-Bold",textColor=WHITE)
cellr=ParagraphStyle("cellr",parent=cell,alignment=2)
tval=ParagraphStyle("tv",fontName="Helvetica-Bold",fontSize=15,leading=17,textColor=NAVY,alignment=TA_CENTER)
tlab=ParagraphStyle("tl",fontName="Helvetica-Bold",fontSize=7.5,leading=9.5,textColor=NAVY2,alignment=TA_CENTER)
fbh=ParagraphStyle("fbh",fontName="Helvetica-Bold",fontSize=9.5,leading=12,textColor=GOLD,spaceBefore=5,spaceAfter=2)
fbl=ParagraphStyle("fbl",fontName="Helvetica",fontSize=8.8,leading=11.5,textColor=TDARK,leftIndent=6,spaceAfter=1)
def esc(t): return str(t).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def sbar(title,color=GREEN):
    t=Table([[Paragraph(f'<font color="#1E2A3A"><b>{esc(title)}</b></font>',ParagraphStyle("h",fontSize=12,leading=15,leftIndent=8))]],colWidths=[CW],rowHeights=[22])
    t.setStyle(TableStyle([("LINEBELOW",(0,0),(-1,-1),1.5,color),("LEFTPADDING",(0,0),(-1,-1),0),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    return t

def tiles(items,per,valcolors=None):
    out=[]
    for i in range(0,len(items),per):
        row=items[i:i+per]; cells=[]
        for j,(val,lab) in enumerate(row):
            vc=(valcolors[i+j] if valcolors else NAVY)
            vs=ParagraphStyle("v",parent=tval,textColor=vc)
            inner=Table([[Paragraph(esc(val),vs)],[Paragraph(esc(lab),tlab)]],colWidths=[(CW-(per-1)*7)/per])
            inner.setStyle(TableStyle([("TOPPADDING",(0,0),(-1,0),7),("BOTTOMPADDING",(0,0),(-1,0),1),
                ("TOPPADDING",(0,1),(-1,1),1),("BOTTOMPADDING",(0,1),(-1,1),7),
                ("BACKGROUND",(0,0),(-1,-1),LABELBG),("BOX",(0,0),(-1,-1),0.5,BORDER),
                ("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4)]))
            cells.append(inner)
        while len(cells)<per: cells.append("")
        gt=Table([cells],colWidths=[CW/per]*per,hAlign="LEFT")
        gt.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),4),("VALIGN",(0,0),(-1,-1),"TOP")]))
        out.append(gt); out.append(Spacer(1,7))
    return out

# ---------- page furniture ----------
def masthead(canvas,doc):
    canvas.saveState(); w,h=A4
    canvas.setFillColor(NAVY); canvas.rect(0,h-92,w,92,fill=1,stroke=0)
    canvas.setFillColor(GREEN); canvas.rect(0,h-92,w,4,fill=1,stroke=0)
    canvas.setFillColor(GOLD); canvas.setFont("Helvetica-Bold",9.5)
    canvas.drawRightString(w-54,h-42,f"FY27 · Week {WNUM}")
    canvas.setFillColor(WHITE); canvas.setFont("Helvetica",8.5)
    canvas.drawRightString(w-54,h-56,f"Week Ending {WLABEL}")
    canvas.setFillColor(WHITE); canvas.setFont("Helvetica-Bold",14)
    canvas.drawString(54,h-45,"Woolworths NZ — Loss Prevention & Safety Report")
    canvas.setFillColor(HexColor("#B9C4D0")); canvas.setFont("Helvetica",9.5)
    canvas.drawString(54,h-64,"SLS RTC covert loss-prevention · national · people-safety first")
    _footer(canvas,doc); canvas.restoreState()
def plain(canvas,doc):
    canvas.saveState(); w,h=A4
    canvas.setStrokeColor(BORDER); canvas.setLineWidth(0.5); canvas.line(54,h-40,w-54,h-40)
    canvas.setFont("Helvetica",7); canvas.setFillColor(TLIGHT)
    canvas.drawString(54,h-36,"Woolworths National LP & Safety Report")
    canvas.drawRightString(w-54,h-36,f"Week Ending {WLABEL}")
    _footer(canvas,doc); canvas.restoreState()
def _footer(canvas,doc):
    w,h=A4; canvas.setStrokeColor(BORDER); canvas.setLineWidth(0.5); canvas.line(54,40,w-54,40)
    canvas.setFont("Helvetica",7.5); canvas.setFillColor(TLIGHT)
    canvas.drawString(54,30,"SLS RTC — Confidential")
    canvas.drawCentredString(w/2,30,f"Page {doc.page}")
    canvas.drawRightString(w-54,30,"Prepared by SLS RTC (Absolute Security Group)")

doc=BaseDocTemplate(OUT,pagesize=A4,leftMargin=54,rightMargin=54,topMargin=112,bottomMargin=50,title="Woolworths National LP & Safety Report")
from reportlab.platypus import NextPageTemplate
doc.addPageTemplates([
    PageTemplate(id="first",frames=[Frame(54,50,A4[0]-108,A4[1]-162)],onPage=masthead),
    PageTemplate(id="rest",frames=[Frame(54,50,A4[0]-108,A4[1]-100)],onPage=plain)])

E=[NextPageTemplate("rest")]
E.append(Paragraph("Our covert team's first priority is the safety of your people and customers. This report leads with the week's safety picture, then the value recovered and the incidents the team managed on your floor. The Deployment &amp; Recovery Tracker (attached) carries the full store-by-store detail.",lead))

E.append(sbar("Loss Overview — Week Ending "+WLABEL))
E+=tiles([(f"${REC:,.0f}","Recovered goods"),(f"${PKG:,.0f}","Recovered packaging"),
          (f"${TOTREC:,.0f}","Total recovered"),(f"${LOST:,.0f}","Not recovered"),(f"${TL:,.0f}","Total loss")],5,
          valcolors=[GREEN,GREEN,GREEN,RED,NAVY])
E.append(Paragraph(f"Of <b>${TL:,.0f}</b> in total loss identified this week, <b>${TOTREC:,.0f} ({RECPCT:.1f}%)</b> was recovered and returned to Woolworths — <b>${REC:,.0f}</b> in recovered goods and <b>${PKG:,.0f}</b> in recovered packaging — with <b>${LOST:,.0f}</b> not recovered. Total loss = recovered goods + recovered packaging + estimated stolen.",body))

E.append(Spacer(1,6)); E.append(sbar("Health & Safety This Week"))
E+=tiles([(str(inc),"Incidents managed"),(str(off_tot),"Offenders engaged"),
          (str(SERIOUS),"Serious (severity 3+)"),(str(confront),"Involving aggression / threats"),
          (str(nat['tres']),"Trespass actions"),(str(pol),"Escalated to Police")],6,
          valcolors=[NAVY,NAVY,GOLD,RED,NAVY,NAVY])
sevline=" · ".join(f"Sev {k}: {sev.get(k,0)}" for k in ('1','2','3','4','5'))
E.append(Paragraph(f"The team managed <b>{inc} incidents</b> involving <b>{off_tot} offenders</b> this week. <b>{SERIOUS}</b> reached severity 3 or above (<b>{SEVERE}</b> at the severe end, severity 4–5), and <b>{confront}</b> involved aggression, threats or violence toward the team or others — {PHYS_CLAUSE}. Severity spread: {sevline}. <b>{nat['tres']} trespass actions</b> were issued and <b>{pol}</b> incidents escalated to Police. Our team is covert and observation-only; the priority throughout is the safety of staff and customers.",body))
E.append(Paragraph("<b>Severity grading (1&ndash;5).</b> Each incident is graded by the difficulty, cooperation and, above all, the risk to staff and customers during the intervention &mdash; <b>Level 3 and above is graded &lsquo;serious&rsquo;.</b> &nbsp;<b>1</b> Compliant &mdash; no issues, items recovered / returned. &nbsp;<b>2</b> Low-level difficulty &mdash; unhelpful or evasive, or items lost. &nbsp;<b>3</b> Mild aggression &mdash; managed without escalation. &nbsp;<b>4</b> Verbal &amp; aggressive abuse &mdash; threatening language, no physical contact. &nbsp;<b>5</b> Physical altercation or weapon &mdash; escalated to Police where warranted.",ParagraphStyle("sevkey",parent=body,fontSize=8.3,textColor=TMED,spaceBefore=3,spaceAfter=3)))
E.append(Paragraph("<i>Deterrent counts and weekend logging settle after the week closes; safety figures reflect submissions received to date.</i>",ParagraphStyle("note",parent=body,fontName="Helvetica-Oblique",fontSize=8.3,textColor=TMED)))

E.append(Spacer(1,8)); E.append(sbar("Incidents in Focus"))
E.append(Paragraph("A sample of what the team dealt with this week and the results. Individuals are not identified; the team intervenes without physical force.",ParagraphStyle("if",parent=body,fontSize=8.8,textColor=TMED,spaceAfter=4)))
for it in INCIDENTS:
    blk=[Paragraph(esc(it["h"]),fbh),
         Paragraph(f"<b>What happened.</b> {esc(it['occ'])}",fbl),
         Paragraph(f"<b>How the team handled it.</b> {esc(it['hand'])}",fbl),
         Paragraph(f"<b>Outcome.</b> {esc(it['out'])}",fbl)]
    E.append(KeepTogether(blk)); E.append(Spacer(1,4))

doc.build(E)
print("wrote",OUT)
print(f"Loss: recovered goods ${REC:,.0f} | pkg ${PKG:,.0f} | total rec ${TOTREC:,.0f} ({RECPCT:.1f}%) | not rec ${LOST:,.0f} | TOTAL LOSS ${TL:,.0f}")
print(f"H&S: {inc} inc | {off_tot} off | serious(3+) {SERIOUS} | severe(4-5) {SEVERE} | confrontation {confront} | trespass {nat['tres']} (GIR-only {vt+ft}) | police {pol}")
