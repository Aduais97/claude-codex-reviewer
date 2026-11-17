#!/usr/bin/env python3
"""HOTC Safety Team — Quarterly Report & Value Review (Q ending 30 Sep 2026, Jul–Aug–Sep).
Board-presentable. First FULL quarter after the LCF pilot. Verified (ETR) data. Mirrors the
Jul-2026 review template; full-history trend appendix."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT

NAVY=colors.HexColor('#1F3864'); GOLD=colors.HexColor('#B8912F'); LIGHT=colors.HexColor('#EDF0F7')
GREY=colors.HexColor('#555555'); RED=colors.HexColor('#B01E1E'); GREEN=colors.HexColor('#2E7D32')
CH="/Users/ahmadduais/Desktop/ASG/HOTC/2026/_charts_quarterly"
OUT="/Users/ahmadduais/Desktop/ASG/HOTC/2026/HOTC_Safety_Team_Quarterly_Value_Review_Sep2026.pdf"

ss=getSampleStyleSheet()
def S(name,**kw): return ParagraphStyle(name,parent=ss['Normal'],**kw)
MAST=S('mast',textColor=GOLD,fontSize=9,leading=11,spaceAfter=1)
H1=S('h1',textColor=NAVY,fontSize=20,leading=23,spaceAfter=2,alignment=TA_LEFT,fontName='Helvetica-Bold')
SUB=S('sub',textColor=GREY,fontSize=10.5,leading=13,spaceAfter=2)
H2=S('h2',textColor=NAVY,fontSize=13.5,leading=16,spaceBefore=12,spaceAfter=5,fontName='Helvetica-Bold')
BODY=S('body',fontSize=10,leading=14.5,spaceAfter=7)
NOTE=S('note',fontSize=8.5,leading=11,textColor=GREY)
CAP=S('cap',fontSize=8.5,leading=11,textColor=GREY,spaceBefore=2,spaceAfter=10)

el=[]
def rule():
    t=Table([['']],colWidths=[178*mm]); t.setStyle(TableStyle([('LINEBELOW',(0,0),(-1,-1),1,GOLD)])); return t

# ---------- Header ----------
el.append(Paragraph('ABSOLUTE SECURITY GROUP',MAST))
el.append(Paragraph('HOTC Safety Team — Quarterly Report &amp; Value Review',H1))
el.append(Paragraph('Heart of the City · Auckland CBD Safety Team &nbsp;|&nbsp; Quarter ending 30 September 2026 (Jul–Aug–Sep 2026)',SUB))
el.append(Spacer(1,4)); el.append(rule()); el.append(Spacer(1,10))

# ---------- KPI band ----------
def kpi(v,l,c=NAVY):
    return Table([[Paragraph(f'<b>{v}</b>',S('k',fontSize=19,textColor=c,leading=21))],
                  [Paragraph(l,S('kl',fontSize=8,textColor=GREY,leading=10))]],colWidths=[42*mm])
band=Table([[kpi('607','Business calls responded to<br/>(the quarter)'),
             kpi('667','Incidents handled<br/>(the quarter)'),
             kpi('+16%','Sept calls vs Aug<br/>(223 vs 193)',GREEN),
             kpi('$690k','Annual funding<br/>(core programme)',GOLD)]],
            colWidths=[45*mm,45*mm,45*mm,45*mm])
band.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LIGHT),('BOX',(0,0),(-1,-1),0.5,LIGHT),
    ('INNERGRID',(0,0),(-1,-1),0.5,colors.white),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LEFTPADDING',(0,0),(-1,-1),9)]))
el.append(band); el.append(Spacer(1,12))

# ---------- Executive summary ----------
el.append(Paragraph('Executive summary',H2))
el.append(Paragraph('Over the July–September 2026 quarter — the first full quarter since the Council-funded LCF pilot ended on 24 July — the CBD Safety Team responded to <b>607 calls from businesses</b> and handled <b>667 recorded incidents</b> across the city centre: vagrancy move-ons, theft, aggression, intoxication and serious events, alongside continuous patrol coverage.',BODY))
el.append(Paragraph('The quarter&rsquo;s clear signal is that <b>demand is rising on a flat budget</b>. Running on the reduced <b>$690k</b> core programme with no additional team, monthly business calls climbed through the quarter — <b>191 → 193 → 223</b> — making <b>September the busiest month</b> of the quarter (+16% on August). Serious incidents also stepped up over the three months (13 → 8 → <b>15</b> in September), and vagrancy remained the single largest load at <b>302 move-ons</b>. The team absorbed this growing demand without additional resource — the clearest indication yet of unmet need at the current funding level.',BODY))
el.append(Paragraph('<i>Figures in this review are drawn from the team&rsquo;s weekly patrol reports and have been independently data-verified.</i>',NOTE))

# ---------- Quarter in focus ----------
el.append(Paragraph('The quarter in focus — July to September 2026',H2))
rows=[['Measure','Jul','Aug','Sep','Quarter'],
 ['Business calls responded to','191','193','223','607'],
 ['Vagrancy move-ons','120','76','106','302'],
 ['Aggression','53','50','65','168'],
 ['Shoplifting / theft','33','36','38','107'],
 ['Public drinking / cannabis','25','23','32','80'],
 ['Serious incidents','13','8','15','36'],
 ['Intoxicated persons','13','10','16','39'],
 ['Police coordinations','23','22','29','74'],
 ['Arrests assisted','7','3','5','15']]
t=Table(rows,colWidths=[66*mm,24*mm,24*mm,24*mm,28*mm])
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),colors.white),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(-1,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),9),
    ('ALIGN',(1,0),(-1,-1),'CENTER'),('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#CCCCCC')),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F6F8FC')]),('BACKGROUND',(-1,1),(-1,-1),LIGHT),
    ('TOPPADDING',(0,0),(-1,-1),4.5),('BOTTOMPADDING',(0,0),(-1,-1),4.5)]))
el.append(t); el.append(Spacer(1,7))
el.append(Paragraph('<b>September was the quarter&rsquo;s peak.</b> As the city centre warmed into spring, business calls (223), aggression (65), serious incidents (15), intoxication (16) and public drinking (32) all reached their quarterly highs in September — on the same core team that ran the whole period. July carried the tail of the LCF pilot (which ran to the 24th) and a vagrancy spike (120 move-ons); August settled to the core baseline; September then rose above both. The direction of travel into Q2 is upward.',BODY))

el.append(PageBreak())
# ---------- Trend ----------
el.append(Paragraph('The trend — how it has flowed',H2))
for b in ['<b>Launch &amp; ramp (2024):</b> from March 2024 the service scaled quickly, peaking near 395 business calls a month in mid-2024 on the larger programme.',
          '<b>The 2025 cut:</b> after the budget was reduced from $800k to $690k in April/May 2025, monthly output stepped down and has held at the lower level since, apart from seasonal peaks.',
          '<b>The 2026 pilot:</b> the Council-funded LCF team (one additional crew, 2 June – 24 July 2026) lifted output while it ran, then output returned to the core level once it ended.',
          '<b>This quarter (Jul–Sep 2026):</b> the first full post-pilot quarter — the core programme holding ~190–220 business calls a month and <b>rising into September</b>, the busiest month of the quarter.']:
    el.append(Paragraph(b,S('bull',fontSize=10,leading=14.5,spaceAfter=4,leftIndent=10)))
el.append(Paragraph('Read together, the history shows output moving with funding — down with the 2025 cut, up with the 2026 pilot — and now a core programme carrying a rising workload at a flat budget. The full 31-month picture is in the appendix.',BODY))

# ---------- Value & ROI ----------
el.append(Paragraph('Value &amp; return on funding',H2))
el.append(Paragraph('<b>What the current $690k delivers:</b> on the order of <b>~2,400 business calls responded to a year</b> and <b>~2,700 incidents handled</b>, plus continuous CBD patrol presence — at roughly <b>$284 per business call</b> (allocating total funding to calls as the headline output measure).',BODY))
roi=[['Funding event','Change in funding','Effect on output'],
 ['Budget cut (Apr/May 2025)','−$110k (−14%)','Monthly output stepped down and held lower'],
 ['LCF pilot (2 Jun–24 Jul 2026)','+$41,150 (one team, ~8 wks)','Lifted Jun–Jul output; returned to core after 24 Jul'],
 ['Post-pilot core (this quarter)','flat at $690k','Demand rising — Sep the busiest month on no extra team']]
t=Table(roi,colWidths=[55*mm,44*mm,79*mm])
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),colors.white),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),9),
    ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#CCCCCC')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F6F8FC')]),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
el.append(t); el.append(Spacer(1,6))
el.append(Paragraph('<b>Value beyond the counts:</b> visible deterrence, business confidence, and keeping low-level disorder from escalating to Police all sit behind these figures. (This review measures business calls and recorded incidents; it is not a measure of every outcome the team delivers.)',BODY))
el.append(Paragraph('<b>Bottom line:</b> the HOTC Safety Team is a predictable, good-value safety investment for the city centre. With demand climbing through the quarter on a flat budget — September the busiest month on the core team alone — the data makes a clear case for protecting and, ideally, growing the programme&rsquo;s funding ahead of the summer peak.',S('bl',fontSize=10.5,leading=15,textColor=NAVY,spaceBefore=4,backColor=colors.HexColor('#F6F8FC'),borderPadding=8)))

# ---------- Appendix ----------
el.append(PageBreak())
el.append(Paragraph('Appendix — full-history trend graphs',H2))
el.append(Paragraph('All data the team has tracked, from the March 2024 launch to end of September 2026. The quarter (Jul–Sep 2026) is shaded gold in each chart. A note on terminology: the five core measures (calls, aggression, police involvement, public drinking, assistance) have been recorded throughout; the more detailed incident breakdown (vagrancy, theft, serious incidents, intoxication, arrests) has been tracked since March 2026, so its history is shorter.',NOTE))
el.append(Spacer(1,8))
figs=[('fig1_calls.png',4.4/11,'Figure 1 — Business calls per month, full history, with a 3-month moving average. The 2024 highs, the step-down after the Apr/May-2025 budget cut, the June-2026 pilot, and the rise into September 2026 are all visible.'),
 ('fig2_funding_vs_calls.png',4.6/11,'Figure 2 — Funding vs output: business calls (3-month average, left axis) against the programme funding level (right axis). Calls step down with the 2025 cut and lift during the LCF pilot.'),
 ('fig3_antisocial.png',4.4/11,'Figure 3 — Antisocial behaviour (aggression + public drinking/cannabis combined) per month, full history, with a 3-month moving average.'),
 ('fig4_detail_incidents.png',4.4/9,'Figure 4 — Detailed incidents handled each month since tracking began (Mar 2026). The Jul–Sep 2026 quarter is shaded; September is the highest post-pilot month.'),
 ('fig5_total_activity.png',4.6/11,'Figure 5 — Total recorded activity per month, all measures combined. The navy line (business calls + aggression + police + drinking/drugs + assistance) runs the full history; the gold line adds the detailed incident types tracked since March 2026.')]
for i,(f,ar,cap) in enumerate(figs):
    p=os.path.join(CH,f)
    if os.path.exists(p):
        w=178*mm
        el.append(KeepTogether([Image(p,width=w,height=w*ar),Paragraph(cap,CAP)]))
        if i in (1,3): el.append(PageBreak())

el.append(Spacer(1,6)); el.append(rule())
el.append(Paragraph('Prepared by Absolute Security Group for Heart of the City · Data: weekly patrol reports, Mar 2024 – Sep 2026 · Jun–Sep 2026 independently data-verified.',NOTE))

doc=SimpleDocTemplate(OUT,pagesize=A4,topMargin=15*mm,bottomMargin=13*mm,leftMargin=16*mm,rightMargin=16*mm)
doc.build(el)
print("SAVED:",OUT)
import shutil; shutil.copy2(OUT, os.path.expanduser("~/Downloads/"+os.path.basename(OUT)))
