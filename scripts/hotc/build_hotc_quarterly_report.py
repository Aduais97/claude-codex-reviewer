#!/usr/bin/env python3
"""HOTC Safety Team — Quarterly Report & Value/ROI Review (Q ending 31 Jul 2026).
Board-presentable. Quarter May-Jul 2026 highlighted; full-history trend appendix."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

NAVY=colors.HexColor('#1F3864'); GOLD=colors.HexColor('#B8912F'); LIGHT=colors.HexColor('#EDF0F7')
GREY=colors.HexColor('#555555'); RED=colors.HexColor('#B01E1E'); GREEN=colors.HexColor('#2E7D32')
CH="/Users/ahmadduais/Desktop/ASG/HOTC/2026/_charts_quarterly"
OUT="/Users/ahmadduais/Desktop/ASG/HOTC/2026/HOTC_Safety_Team_Quarterly_Value_Review_Jul2026.pdf"

ss=getSampleStyleSheet()
def S(name,**kw): return ParagraphStyle(name,parent=ss['Normal'],**kw)
MAST=S('mast',textColor=GOLD,fontSize=9,leading=11,spaceAfter=1)
H1=S('h1',textColor=NAVY,fontSize=20,leading=23,spaceAfter=2,alignment=TA_LEFT,fontName='Helvetica-Bold')
SUB=S('sub',textColor=GREY,fontSize=10.5,leading=13,spaceAfter=2)
H2=S('h2',textColor=NAVY,fontSize=13.5,leading=16,spaceBefore=12,spaceAfter=5,fontName='Helvetica-Bold')
BODY=S('body',fontSize=10,leading=14.5,spaceAfter=7)
BULL=S('bull',fontSize=10,leading=14,spaceAfter=3,leftIndent=10,bulletIndent=0)
NOTE=S('note',fontSize=8.5,leading=11,textColor=GREY)
CAP=S('cap',fontSize=8.5,leading=11,textColor=GREY,spaceBefore=2,spaceAfter=10)

el=[]
def rule():
    t=Table([['']],colWidths=[178*mm]); t.setStyle(TableStyle([('LINEBELOW',(0,0),(-1,-1),1,GOLD)])); return t

# ---------- Cover / header ----------
el.append(Paragraph('ABSOLUTE SECURITY GROUP',MAST))
el.append(Paragraph('HOTC Safety Team — Quarterly Report &amp; Value Review',H1))
el.append(Paragraph('Heart of the City · Auckland CBD Safety Team &nbsp;|&nbsp; Quarter ending 31 July 2026 (May–Jun–Jul 2026)',SUB))
el.append(Spacer(1,4)); el.append(rule()); el.append(Spacer(1,10))

# ---------- KPI band ----------
def kpi(v,l,c=NAVY):
    return Table([[Paragraph(f'<b>{v}</b>',S('k',fontSize=19,textColor=c,leading=21))],
                  [Paragraph(l,S('kl',fontSize=8,textColor=GREY,leading=10))]],colWidths=[42*mm])
band=Table([[kpi('673','Business calls responded to<br/>(the quarter)'),
             kpi('667','Incidents handled<br/>(the quarter)'),
             kpi('+47%','June calls vs May<br/>(265 vs 180)',GREEN),
             kpi('$690k','Annual funding<br/>(was $800k)',GOLD)]],
            colWidths=[45*mm,45*mm,45*mm,45*mm])
band.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LIGHT),('BOX',(0,0),(-1,-1),0.5,LIGHT),
    ('INNERGRID',(0,0),(-1,-1),0.5,colors.white),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LEFTPADDING',(0,0),(-1,-1),9)]))
el.append(band); el.append(Spacer(1,12))

# ---------- Executive summary ----------
el.append(Paragraph('Executive summary',H2))
el.append(Paragraph('Over the May–July 2026 quarter the CBD Safety Team responded to <b>673 calls from businesses</b> and handled <b>667 recorded incidents</b> across the city centre — vagrancy move-ons, theft, aggression, and serious events — while maintaining continuous patrol coverage.',BODY))
el.append(Paragraph('The clear story in the data is that <b>frontline output tracks funding</b>. The programme has run on a reduced budget (<b>$690k</b>, down from $800k) since a cut in <b>April/May 2025</b>; activity stepped down about <b>21%</b> at that point and has held at the lower level since, apart from seasonal peaks. The Council-funded <b>LCF pilot</b> (one additional team, 2 June – 24 July 2026) then lifted <b>June calls ~47%</b> versus May (265 vs 180) and drove a <b>~60% rise in incidents</b> (271 vs 169) — the two largest categories, aggression and theft, roughly doubling — before output fell back when the pilot ended. Funding and safety output move firmly in the same direction.',BODY))
el.append(Paragraph('<b>Implication for the board:</b> added coverage capacity translates into materially higher recorded safety activity, so restoring or increasing funding can be expected to increase the safety output delivered to the city centre — recognising that the 2025 step-down also coincided with the programme’s natural post-launch normalisation, so funding is a major but not the sole driver.',BODY))

# ---------- The quarter ----------
el.append(Paragraph('The quarter in focus — May to July 2026',H2))
qrows=[['Month','Business calls','Incidents handled','Note'],
 ['May 2026','180','169','Post-cut baseline'],
 ['June 2026','265','271','LCF pilot peak — +47% calls, +60% incidents vs May'],
 ['July 2026','228','227','Pilot ran to 24 Jul; serious incidents highest of the quarter (16)'],
 ['Quarter total','673','667','']]
t=Table(qrows,colWidths=[26*mm,30*mm,32*mm,90*mm])
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),colors.white),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),9),('ALIGN',(1,0),(2,-1),'CENTER'),
    ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#CCCCCC')),('ROWBACKGROUNDS',(0,1),(-1,-2),[colors.white,colors.HexColor('#F6F8FC')]),
    ('BACKGROUND',(0,-1),(-1,-1),LIGHT),('FONTNAME',(0,-1),(-1,-1),'Helvetica-Bold'),
    ('BACKGROUND',(0,2),(-1,2),colors.HexColor('#EAF2EA')),
    ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
el.append(t); el.append(Spacer(1,4))
el.append(Paragraph('The quarter captured the LCF pilot’s peak impact: June recorded the highest monthly incident count (271) since detailed incident categories began being tracked in March 2026, and July stayed elevated (227) while the pilot ran to the 24th before tapering. Serious incidents also climbed across the quarter (4 → 10 → 16, May → June → July) — a severity signal worth watching. This is the trend to read the quarter against; see the appendix.',BODY))

# ---------- The trend ----------
el.append(Paragraph('The trend — how it has flowed',H2))
for b in [
 'Launch &amp; ramp (2024): from March 2024 the service scaled quickly, peaking near 395 business calls a month in mid-2024 on the larger programme.',
 'Budget cut (April/May 2025): when funding was reduced from $800k to $690k, business calls dropped about 21% (from ~8.5 to ~6.7 per day) and settled at that lower band — where they have stayed since, apart from the pre-Christmas seasonal peaks (Oct &amp; Dec).',
 'LCF pilot (June–July 2026): the Council-funded extra team produced a sharp, temporary surge — the clearest single proof that added funding lifts output — then activity returned to the post-cut level once it ended.',
]:
    el.append(Paragraph('•&nbsp; '+b,BULL))
el.append(Spacer(1,3))
el.append(Paragraph('Two independent events — the 2025 cut and the 2026 pilot — move output in the same direction as funding (down with the cut, up with the pilot), alongside a natural easing from the 2024 launch peak. The full 29-month picture is in the appendix.',BODY))

el.append(PageBreak())

# ---------- Value & ROI ----------
el.append(Paragraph('Value &amp; return on funding',H2))
el.append(Paragraph('<b>What the current $690k delivers:</b> on the order of ~2,500 business calls responded to a year, thousands of incidents managed, and continuous CBD patrol presence — at roughly <b>$276 per business call</b> (allocating total funding to calls as the headline output measure).',BODY))
el.append(Paragraph('<b>The funding-to-output relationship (the return case):</b>',BODY))
roi=[['Funding event','Change in funding','Change in output'],
 ['Budget cut (Apr/May 2025)','−$110k (−14%)','Business calls −21%; sustained lower'],
 ['LCF pilot (2 Jun–24 Jul 2026)','+$41,150 (one team, ~8 wks)','+136 calls &amp; +136 incidents vs baseline'],]
t=Table(roi,colWidths=[52*mm,45*mm,81*mm])
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),colors.white),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),9),
    ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#CCCCCC')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F6F8FC')]),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
el.append(t); el.append(Spacer(1,6))
el.append(Paragraph('The pilot delivered additional output at about <b>$300 per unit of its primary output</b> — a marginal rate close to, and about 9% above, the core programme’s ~$276 average cost per call. Read with the post-cut step-down, this shows <b>funding and safety output move firmly in the same direction</b>, with extra funding buying extra output at a broadly comparable unit cost — slightly higher at the margin, consistent with mild diminishing returns rather than a fixed linear rate. The pilot’s output was additional and served, consistent with unmet demand at the current funding level.',BODY))
el.append(Paragraph('<b>Value beyond the counts:</b> visible deterrence, business confidence, and keeping low-level disorder from escalating to Police all sit behind these figures. (Note: this review measures business calls and recorded incidents; it is not a measure of every outcome the team delivers.)',BODY))
el.append(Paragraph('<b>Bottom line:</b> the HOTC Safety Team is a predictable, good-value safety investment for the city centre. The evidence — a cut that reduced output and a pilot that restored it — makes a clear, data-backed case for protecting and, ideally, growing the programme’s funding.',S('bl',fontSize=10.5,leading=15,textColor=NAVY,spaceBefore=4,backColor=colors.HexColor('#F6F8FC'),borderPadding=8)))

# ---------- Appendix ----------
el.append(PageBreak())
el.append(Paragraph('Appendix — full-history trend graphs',H2))
el.append(Paragraph('All data the team has tracked, from the March 2024 launch to end of July 2026. The quarter (May–Jul 2026) is shaded gold in each chart. A note on terminology: the five core measures (calls, aggression, police involvement, public drinking, assistance) have been recorded throughout; the more detailed incident breakdown (vagrancy, theft, serious incidents, intoxication, arrests) has been tracked since March 2026, so its history is shorter.',NOTE))
el.append(Spacer(1,8))
figs=[('fig1_calls.png',4.4/11,'Figure 1 — Business calls per month, full history, with a 3-month moving average. The 2024 highs, the step-down after the Apr/May-2025 budget cut, and the June-2026 pilot are all visible. July 2025 is partly estimated (two weeks recorded, remainder from daily logs).'),
 ('fig2_funding_vs_calls.png',4.6/11,'Figure 2 — Funding vs output: business calls (3-month average, left axis) against the programme funding level (right axis). Calls step down with the 2025 cut and lift during the LCF pilot.'),
 ('fig3_antisocial.png',4.4/11,'Figure 3 — Antisocial behaviour (aggression + public drinking/cannabis combined) per month, full history, with a 3-month moving average.'),
 ('fig4_detail_incidents.png',4.4/9,'Figure 4 — Detailed incidents handled each month since tracking began (Mar 2026). June’s pilot spike (271) is the highest since detailed tracking began.'),
 ('fig5_total_activity.png',4.6/11,'Figure 5 — Total recorded activity per month, all measures combined. The navy line (business calls + aggression + police + drinking/drugs + assistance) runs the full history; the gold line adds the detailed incident types tracked since March 2026, so its step-up reflects broader recording rather than a real jump.')]
for i,(f,ar,cap) in enumerate(figs):
    p=os.path.join(CH,f)
    if os.path.exists(p):
        w=178*mm
        el.append(KeepTogether([Image(p,width=w,height=w*ar),Paragraph(cap,CAP)]))
        if i in (1,3): el.append(PageBreak())

el.append(Spacer(1,6)); el.append(rule())
el.append(Paragraph('Prepared by Absolute Security Group for Heart of the City · Data: weekly patrol reports, Mar 2024 – Jul 2026 · July 2025 partly estimated from daily logs.',NOTE))

doc=SimpleDocTemplate(OUT,pagesize=A4,topMargin=15*mm,bottomMargin=13*mm,leftMargin=16*mm,rightMargin=16*mm)
doc.build(el)
print("SAVED:",OUT)
import shutil; shutil.copy2(OUT, os.path.expanduser("~/Downloads/"+os.path.basename(OUT)))
