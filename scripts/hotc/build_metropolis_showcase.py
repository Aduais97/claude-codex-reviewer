#!/usr/bin/env python3
"""Metropolis September 2026 — Security Service Showcase (2-3pp) for incoming building management.
Reads the ETR-synthesized JSON and renders in the ASG/HOTC house style. Re-run after editing the JSON."""
import json, os, re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, ListFlowable, ListItem)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

R=json.load(open("/private/tmp/claude-501/-Users-ahmadduais/d7b18d45-5633-4a8e-9750-512554c7f60c/scratchpad/metro_sep/showcase.json"))
NAVY=colors.HexColor('#1F3864'); GOLD=colors.HexColor('#B8912F'); LIGHT=colors.HexColor('#EDF0F7')
GREY=colors.HexColor('#555555'); SOFT=colors.HexColor('#F6F8FC')
OUT="/Users/ahmadduais/Desktop/ASG/Metropolis/Metropolis_Security_Showcase_September2026.pdf"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
ss=getSampleStyleSheet()
def S(n,**k): return ParagraphStyle(n,parent=ss['Normal'],**k)
H1=S('h1',textColor=NAVY,fontSize=21,leading=25,fontName='Helvetica-Bold',alignment=TA_CENTER)
H2=S('h2',textColor=NAVY,fontSize=13.5,leading=16,spaceBefore=12,spaceAfter=5,fontName='Helvetica-Bold')
H3=S('h3',textColor=GOLD,fontSize=10.5,leading=13,spaceBefore=7,spaceAfter=3,fontName='Helvetica-Bold')
BODY=S('body',fontSize=10,leading=14.5,spaceAfter=7,alignment=TA_JUSTIFY)
BUL=S('bul',fontSize=9.5,leading=13.2,spaceAfter=3)
NOTE=S('note',fontSize=8,leading=10.5,textColor=GREY,spaceAfter=2)
def _esc(s): return re.sub(r'&(?!amp;|rsquo;|lsquo;|lt;|gt;|#|nbsp;)','&amp;',str(s))
el=[]

# ---- header band ----
el.append(Spacer(1,4))
el.append(Paragraph('ABSOLUTE SECURITY GROUP',S('m',textColor=GOLD,fontSize=10.5,alignment=TA_CENTER,spaceAfter=10,fontName='Helvetica-Bold')))
el.append(Paragraph('The Metropolis',S('ht',textColor=NAVY,fontSize=15,alignment=TA_CENTER,spaceAfter=3)))
el.append(Paragraph('Security Service Showcase',H1))
el.append(Spacer(1,6)); el.append(Paragraph('September 2026  ·  On-Site Security Service',S('pd',textColor=GREY,fontSize=12,alignment=TA_CENTER,spaceAfter=12)))

# ---- at-a-glance metric strip ----
t=R['september_totals']
def card(n,l):
    return [Paragraph(f'<b>{n}</b>',S('cn',fontSize=17,textColor=NAVY,alignment=TA_CENTER,leading=19)),
            Paragraph(l,S('cl',fontSize=7.6,textColor=GREY,alignment=TA_CENTER,leading=9))]
cells=[card(f"{t['days_covered']}", "Days with security presence"),
       card(f"{t['total_actions']:,}", "Logged security actions"),
       card(f"{t['proactive_patrols_monitoring']:,}", "Proactive patrols & CCTV"),
       card(f"{t['resident_access_service']}", "Resident-service actions"),
       card(f"{t['incidents_interventions']}", "Incidents handled")]
gt=Table([[c[0] for c in cells],[c[1] for c in cells]],colWidths=[36*mm]*5)
gt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),SOFT),('BOX',(0,0),(-1,-1),0.5,LIGHT),
    ('INNERGRID',(0,0),(-1,-1),0.5,colors.white),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('TOPPADDING',(0,0),(-1,0),7),('BOTTOMPADDING',(0,1),(-1,1),7)]))
el.append(gt); el.append(Spacer(1,12))

# ---- headline value statements ----
el.append(Paragraph('Why residents and management are well served', H2))
el.append(ListFlowable([ListItem(Paragraph(_esc(x),BUL),leftIndent=6,value='•') for x in R['headline_values']],
                       bulletType='bullet',start='•',leftIndent=12))
el.append(Spacer(1,4))

# ---- sections ----
for sec in R['sections']:
    el.append(Paragraph(_esc(sec['title']),H2))
    el.append(Paragraph(_esc(sec['narrative']),BODY))
    # keep only short, stat-style metric values (long descriptive ones already live in the narrative)
    m=[x for x in sec.get('metrics',[]) if len(str(x['value']))<=22]
    if m:
        rows=[[Paragraph(f"<b>{_esc(x['value'])}</b>",S('mv',fontSize=10.5,textColor=NAVY)),
               Paragraph(_esc(x['label']),S('ml',fontSize=9,textColor=colors.black))] for x in m]
        mt=Table(rows,colWidths=[26*mm,146*mm])
        mt.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),2),
            ('BOTTOMPADDING',(0,0),(-1,-1),2),('LEFTPADDING',(0,0),(0,-1),2)]))
        el.append(mt); el.append(Spacer(1,6))

# ---- highlights ----
el.append(Paragraph('Operational highlights — September', H2))
el.append(Paragraph('Selected from the daily security logs.',NOTE)); el.append(Spacer(1,3))
hrows=[[Paragraph('<b>Date</b>',S('hh',fontSize=8.6,textColor=colors.white,fontName='Helvetica-Bold')),
        Paragraph('<b>What happened</b>',S('hh',fontSize=8.6,textColor=colors.white,fontName='Helvetica-Bold'))]]
for h in R['curated_highlights']:
    txt=f"<b>{_esc(h['title'])}.</b> {_esc(h['description'])}"
    hrows.append([Paragraph(_esc(h['date']),S('hd',fontSize=8.5,leading=10.5)),
                  Paragraph(txt,S('ht2',fontSize=8.5,leading=11))])
ht=Table(hrows,colWidths=[24*mm,148*mm],repeatRows=1)
ht.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#CCCCCC')),('VALIGN',(0,0),(-1,-1),'TOP'),
    ('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,SOFT]),
    ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6)]))
el.append(ht)

if R.get('closing'):
    el.append(Spacer(1,8))
    cb=Table([[Paragraph(_esc(R['closing']),S('cl',fontSize=9.6,leading=13.5,textColor=NAVY))]],colWidths=[172*mm])
    cb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LIGHT),('BOX',(0,0),(-1,-1),0.5,GOLD),
        ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    el.append(cb)

el.append(Spacer(1,8)); el.append(Paragraph('Note on the data',H3))
el.append(Paragraph(_esc(
  "Figures are drawn from ASG’s daily on-site security logs for September 2026 (30 days). Category "
  "totals are normalised across weeks where logging terminology varied; “building faults” counts fault "
  "events, several of which recurred during the month. ASG provides the building’s after-hours cover — "
  "overnight on weeknights and full 24-hour weekend cover; weekday daytime hours are covered by building management."),NOTE))
if R.get('confidentiality'):
    el.append(Spacer(1,5))
    el.append(Paragraph(_esc(R['confidentiality']),S('conf',fontSize=7.5,leading=9.5,textColor=GREY,fontName='Helvetica-Oblique')))

def deco(cv,doc):
    cv.saveState(); cv.setFont('Helvetica',7.5); cv.setFillColor(GREY)
    cv.drawString(16*mm, 9*mm, 'Absolute Security Group  ·  The Metropolis — September 2026')
    cv.drawRightString(A4[0]-16*mm, 9*mm, f'Page {doc.page}')
    cv.setStrokeColor(LIGHT); cv.line(16*mm,12*mm,A4[0]-16*mm,12*mm)
    cv.restoreState()
doc=SimpleDocTemplate(OUT,pagesize=A4,topMargin=14*mm,bottomMargin=15*mm,leftMargin=18*mm,rightMargin=18*mm,
                      title="Metropolis Security Showcase — September 2026", author="Absolute Security Group")
doc.build(el,onFirstPage=deco,onLaterPages=deco)
print("SAVED:",OUT)
import shutil; shutil.copy2(OUT, os.path.expanduser("~/Downloads/"+os.path.basename(OUT)))
print("pages:", __import__('fitz').open(OUT).page_count)
