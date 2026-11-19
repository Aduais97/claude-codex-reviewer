#!/usr/bin/env python3
"""HOTC CBD Dynamics — August 2026 update (2 pages). Positive & negative changes
vs July 2026 and vs August 2025, plus recent-weeks trend."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT

NAVY=colors.HexColor('#1F3864'); GOLD=colors.HexColor('#B8912F'); LIGHT=colors.HexColor('#EDF0F7')
GREY=colors.HexColor('#555555'); RED=colors.HexColor('#B01E1E'); GREEN=colors.HexColor('#2E7D32')
GREENBG=colors.HexColor('#EAF3EA'); REDBG=colors.HexColor('#F7E9E9'); AMBERBG=colors.HexColor('#FBF3DD')
CH="/Users/ahmadduais/Desktop/ASG/HOTC/2026/_charts_quarterly"
OUT="/Users/ahmadduais/Desktop/ASG/HOTC/2026/HOTC_CBD_Dynamics_August_2026.pdf"
ss=getSampleStyleSheet()
def S(n,**k): return ParagraphStyle(n,parent=ss['Normal'],**k)
MAST=S('m',textColor=GOLD,fontSize=9,leading=11); H1=S('h1',textColor=NAVY,fontSize=18,leading=21,fontName='Helvetica-Bold')
SUB=S('s',textColor=GREY,fontSize=10,leading=13); H2=S('h2',textColor=NAVY,fontSize=12.5,leading=15,fontName='Helvetica-Bold',spaceBefore=10,spaceAfter=4)
BODY=S('b',fontSize=9.5,leading=13.5,spaceAfter=6); SMALL=S('sm',fontSize=8.5,leading=11.5,textColor=GREY)
PH=S('ph',fontSize=9.5,leading=13,spaceAfter=3); CAP=S('cap',fontSize=8,leading=10.5,textColor=GREY,spaceBefore=2)
el=[]
def rule():
    t=Table([['']],colWidths=[178*mm]); t.setStyle(TableStyle([('LINEBELOW',(0,0),(-1,-1),1,GOLD)])); return t

el.append(Paragraph('ABSOLUTE SECURITY GROUP',MAST))
el.append(Paragraph('CBD Dynamics — August 2026 Update',H1))
el.append(Paragraph('How the city centre is tracking · August 2026 vs July 2026 and vs August 2025 · to 11 August',SUB))
el.append(Spacer(1,4)); el.append(rule()); el.append(Spacer(1,8))

el.append(Paragraph('<b>Read this first.</b> August is 11 days in and <b>post-pilot</b> — the LCF-funded extra team ended 24 July, so this is the core team only. Figures are shown as <b>per-day rates</b> for fair comparison, and lower August counts partly reflect <b>reduced coverage, not only less activity</b>. The detailed incident measures (theft, vagrancy, serious incidents) have only been tracked since 2026, so the year-on-year comparison uses the five long-run core measures.',SMALL))
el.append(Spacer(1,8))

el.append(Paragraph('At a glance — per-day rates',H2))
rows=[['Measure (events/day)','Aug 2026','Jul 2026','Aug 2025','Movement'],
 ['Business calls','6.9','7.4','8.1','↓ vs both — coverage-driven'],
 ['Aggressive behaviour','1.7','2.3','1.7','↓ from Jul spike; flat YoY'],
 ['Public drinking / drugs','0.7','0.5','1.6','↓↓ vs last year (good)'],
 ['Police involvement','0.8','0.6','1.3','↓ vs last year'],
 ['Assistance provided','0.4','0.7','0.8','↓'],
 ['Vagrancy move-ons','2.0','2.9','— *','↓ from July'],
 ['Retail theft','1.3','1.1','— *','↑ from July'],
 ['Serious incidents','0.2','0.5','— *','↓ count, but see caveat'],]
t=Table(rows,colWidths=[46*mm,22*mm,22*mm,22*mm,66*mm])
st=[('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
 ('FONTSIZE',(0,0),(-1,-1),8.5),('ALIGN',(1,0),(3,-1),'CENTER'),('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#CCCCCC')),
 ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F6F8FC')]),('TOPPADDING',(0,0),(-1,-1),3.5),('BOTTOMPADDING',(0,0),(-1,-1),3.5),
 ('LINEABOVE',(0,6),(-1,6),0.8,GOLD)]
t.setStyle(TableStyle(st)); el.append(t)
el.append(Paragraph('* Detailed incident measures were not tracked in 2025, so no year-on-year figure. The gold line separates the five long-run core measures (top) from the 2026-only detailed measures (below).',SMALL))
el.append(Spacer(1,8))

# Positive / negative panels
pos=[('<b>Public drinking &amp; drug use down sharply</b> — ~0.7/day vs 1.6/day last August (−58%). A real, visible-disorder improvement on the street.',),
     ('<b>Aggression, vagrancy &amp; serious-incident counts have eased</b> from July’s peak — the acute spike of late July has not (yet) carried into August.',),
     ('<b>Fewer escalations to Police</b> year-on-year (0.8 vs 1.3/day) — consistent with more matters resolved by the team without Police call-out.',),
     ('<b>Intelligence-led enforcement is landing</b> — evidenced Auror + formal trespass cases built on repeat offenders (Vape Haven harasser; Hollywood Cafe thief; Desiree/Brenda/Gordon, 10 Aug with Police &amp; Council Wardens).',)]
neg=[('<b>Retail theft is up on July</b> (~1.3 vs 1.1/day) — and now includes <b>organised crime</b>: 6 masked males on bikes robbed two Victoria St West stores (8 Aug).',),
     ('<b>The character of incidents is harder</b> — a stabbing (7 Aug), a street assault (“Gordon”, 10 Aug), weapons and mental-health crises in the same 11 days. Severity has not fallen with the counts.',),
     ('<b>Coverage is stretched</b> — one team, one ops phone (which repeatedly dies mid-patrol), no cover for simultaneous calls; the same offenders keep returning (displacement, not resolution).',),
     ('<b>Call volume is below last August</b> (6.9 vs 8.1/day) — reduced saturation/deterrence following the budget cut and the pilot ending.',)]
def panel(title,items,bg,fg):
    cells=[[Paragraph(f'<b>{title}</b>',S('pt',fontSize=10.5,textColor=fg))]]
    for it in items: cells.append([Paragraph('•&nbsp; '+it[0],PH)])
    tt=Table(cells,colWidths=[87*mm])
    tt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,0),6),('BOTTOMPADDING',(0,0),(-1,-1),5),('VALIGN',(0,0),(-1,-1),'TOP')]))
    return tt
el.append(Table([[panel('▲ Positive — improving / easing',pos,GREENBG,GREEN),panel('▼ Negative — worsening / new risk',neg,REDBG,RED)]],
    colWidths=[89*mm,89*mm],style=TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(0,0),4)])))

# ---------- Page 2 ----------
el.append(PageBreak())
el.append(Paragraph('Trends over the last few weeks',H2))
p=os.path.join(CH,'fig_weekly_trend.png')
if os.path.exists(p): el.append(Image(p,width=170*mm,height=170*mm*3.6/9)); el.append(Paragraph('Weekly business calls per day, June–August 2026. June ran hot on the funded pilot; activity tapered through July as the pilot wound down (ended 24 July) and settled to the post-cut baseline in early August. (The 10–11 Aug point is a 2-day sample only.)',CAP))
el.append(Spacer(1,6))
el.append(Paragraph('<b>The shape of it:</b> a clear <b>surge → taper → normalise</b> arc. The June funded-pilot weeks peaked near 9–11 calls/day; July stepped down as the extra team wound down; early August sits at ~5–6/day — the core-team baseline. <b>Severity ran opposite to volume:</b> July carried the quarter’s worst serious-incident load (16), and early August, though quieter by count, has already logged a stabbing, an assault and an organised robbery.',BODY))

el.append(Paragraph('What the patrol logs show on the ground (20 Jul – 11 Aug)',H2))
for b in [
 '<b>Hotspots:</b> McDonald’s (Queen St &amp; Britomart) is the dominant 24/7 flashpoint by a wide margin; the <b>77 Convenience cluster on Victoria St West</b> is where the serious incidents landed; Lovisa, Glassons and the Queen St retail spine drive the daytime theft load.',
 '<b>Escalating:</b> organised retail crime (masked bike-gang robberies), weekend late-night violence (a suspected gang brawl converged on Britomart, 1 Aug), and recurring weapons / mental-health presentations.',
 '<b>Repeat offenders</b> are being worked into evidenced cases (Auror photos, formal trespass) rather than just moved along — a shift toward intelligence-led enforcement.',
 '<b>Post-pilot reality:</b> the team holds 24/7 coverage but leans more on Police and Council Wardens as the force multiplier; concurrency gaps and the ops-phone bottleneck point to reduced saturation versus the funded weeks.',
]:
    el.append(Paragraph('•&nbsp; '+b,PH))
el.append(Spacer(1,6))

el.append(Table([[Paragraph('<b>Bottom line for the meeting:</b> volume has normalised as the pilot ended, and some disorder measures (public drinking especially) are genuinely improving year-on-year. But the <b>city centre is getting harder, not busier</b> — theft, organised crime and serious violence are rising in character even as call counts ease, and the single core team is visibly stretched. Read the lower August counts with care: with reduced coverage, part of the fall is less detection, not only less crime.',
    S('bl',fontSize=9.5,leading=13.5,textColor=NAVY))]],colWidths=[178*mm],
    style=TableStyle([('BACKGROUND',(0,0),(-1,-1),AMBERBG),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)])))
el.append(Spacer(1,6)); el.append(rule())
el.append(Paragraph('Prepared by Absolute Security Group for Heart of the City · Source: weekly data reports + daily patrol logs, to 11 August 2026 · per-day rates approximate; detailed incident measures tracked from 2026.',SMALL))

SimpleDocTemplate(OUT,pagesize=A4,topMargin=14*mm,bottomMargin=12*mm,leftMargin=16*mm,rightMargin=16*mm).build(el)
print("SAVED:",OUT)
import shutil; shutil.copy2(OUT,os.path.expanduser("~/Downloads/"+os.path.basename(OUT)))
