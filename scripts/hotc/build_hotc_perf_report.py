#!/usr/bin/env python3
"""Render the HOTC Quarterly Performance Report (Jul-Sep 2026) from /tmp/hotc_perf_report.json.
Reference-report structure + our trend charts; CONFIDENTIAL board doc. Re-run after editing the JSON."""
import json, os, re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, ListFlowable, ListItem)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

R=json.load(open("/tmp/hotc_perf_report.json"))
NAVY=colors.HexColor('#1F3864'); GOLD=colors.HexColor('#B8912F'); LIGHT=colors.HexColor('#EDF0F7')
GREY=colors.HexColor('#555555')
CH="/Users/ahmadduais/Desktop/ASG/HOTC/2026/_charts_quarterly"
OUT="/Users/ahmadduais/Desktop/ASG/HOTC/2026/HOTC_Performance_Report_JulSep2026.pdf"
ss=getSampleStyleSheet()
def S(n,**k): return ParagraphStyle(n,parent=ss['Normal'],**k)
H1=S('h1',textColor=NAVY,fontSize=22,leading=26,fontName='Helvetica-Bold',alignment=TA_CENTER)
H2=S('h2',textColor=NAVY,fontSize=14,leading=17,spaceBefore=13,spaceAfter=6,fontName='Helvetica-Bold')
H3=S('h3',textColor=GOLD,fontSize=10.5,leading=13,spaceBefore=9,spaceAfter=3,fontName='Helvetica-Bold')
BODY=S('body',fontSize=10,leading=14.5,spaceAfter=7,alignment=TA_JUSTIFY)
BUL=S('bul',fontSize=9.6,leading=13.5,spaceAfter=3)
NOTE=S('note',fontSize=8,leading=10.5,textColor=GREY,spaceAfter=2)
CAP=S('cap',fontSize=8.3,leading=11,textColor=GREY,spaceBefore=2,spaceAfter=10)
el=[]
_cH=S('cH',fontSize=8.6,textColor=colors.white,leading=10.5,fontName='Helvetica-Bold')
_cB=S('cB',fontSize=8.5,textColor=colors.black,leading=11)
_cN=S('cN',fontSize=8.5,textColor=NAVY,leading=11,fontName='Helvetica-Bold')
def _esc(s):
    return re.sub(r'&(?!amp;|rsquo;|lsquo;|lt;|gt;|#|nbsp;|mdash;|ndash;)','&amp;',str(s))
def tbl(rows,widths,hdr=True,boldlast=False):
    # EVERY cell is a Paragraph so long text WRAPS within the column (no overflow)
    data=[]
    for ri,row in enumerate(rows):
        cells=[]
        for ci,c in enumerate(row):
            sty=_cH if (hdr and ri==0) else (_cN if (boldlast and ci==len(row)-1) else _cB)
            cells.append(Paragraph(_esc(c),sty))
        data.append(cells)
    t=Table(data,colWidths=widths,repeatRows=1 if hdr else 0)
    st=[('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#CCCCCC')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F6F8FC')])]
    if hdr: st+=[('BACKGROUND',(0,0),(-1,0),NAVY)]
    t.setStyle(TableStyle(st)); return t
def bullets(items,sty=BUL):
    return ListFlowable([ListItem(Paragraph(x,sty),leftIndent=6,value='•') for x in items],
                        bulletType='bullet',start='•',leftIndent=12)

el.append(Spacer(1,55*mm))
el.append(Paragraph('ABSOLUTE SECURITY GROUP',S('m',textColor=GOLD,fontSize=11,alignment=TA_CENTER,spaceAfter=20,fontName='Helvetica-Bold')))
el.append(Paragraph('Heart of the City',S('ht',textColor=NAVY,fontSize=15,alignment=TA_CENTER,spaceAfter=4)))
el.append(Paragraph('Quarterly Performance Report',H1))
el.append(Spacer(1,8)); el.append(Paragraph(R['period'],S('pd',textColor=GREY,fontSize=13,alignment=TA_CENTER,spaceAfter=30)))
meta=Table([[Paragraph('<b>Prepared For</b>',S('x',alignment=TA_CENTER,fontSize=9.5)),Paragraph('<b>Prepared By</b>',S('x',alignment=TA_CENTER,fontSize=9.5)),Paragraph('<b>Classification</b>',S('x',alignment=TA_CENTER,fontSize=9.5))],
            [Paragraph('Heart of the City Board',S('x',alignment=TA_CENTER,fontSize=9.5)),Paragraph('Absolute Security Group Ltd',S('x',alignment=TA_CENTER,fontSize=9.5)),Paragraph('CONFIDENTIAL',S('x',alignment=TA_CENTER,fontSize=9.5,textColor=colors.HexColor('#B01E1E')))]],
           colWidths=[58*mm,58*mm,58*mm])
meta.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.5,LIGHT),('INNERGRID',(0,0),(-1,-1),0.5,LIGHT),('BACKGROUND',(0,0),(-1,0),LIGHT),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
el.append(meta); el.append(Spacer(1,14))
el.append(Paragraph('This report is prepared for Heart of the City and contains confidential operational data.',S('d',fontSize=8.5,textColor=GREY,alignment=TA_CENTER)))
el.append(PageBreak())

el.append(Paragraph('Executive Summary',H2))
el.append(Paragraph('Absolute Security Group has delivered 24/7 Safety Team patrol services to Heart of the City since March 2024. This report covers the July–September 2026 quarter — the city centre’s first full quarter after the LCF pilot — with performance verified from the team’s weekly patrol reports.',BODY))
el.append(bullets(R['exec_summary']))
for sec in R['sections']:
    el.append(Paragraph(sec['title'],H2))
    for p in sec['paras']: el.append(Paragraph(p,BODY))

el.append(PageBreak()); el.append(Paragraph('Year-on-Year Performance',H2))
el.append(tbl(R['yoy'],[46*mm,27*mm,27*mm,30*mm,48*mm]))
el.append(Spacer(1,10)); el.append(Paragraph('Demonstrated Value',H3))
el.append(tbl(R['demonstrated_value'],[40*mm,74*mm,64*mm]))

# optional hotspots section (added if present in JSON)
if R.get('hotspots'):
    el.append(PageBreak()); el.append(Paragraph('Operational Hotspots & Areas',H2))
    for p in R['hotspots'].get('intro',[]): el.append(Paragraph(p,BODY))
    for blk in R['hotspots'].get('tables',[]):
        el.append(Paragraph(blk['title'],H3)); el.append(tbl(blk['rows'],blk.get('widths',[70*mm,30*mm,78*mm])))
        el.append(Spacer(1,6))

el.append(PageBreak()); el.append(Paragraph('Operational Highlights',H2))
el.append(Paragraph('Selected incidents from the quarter, drawn from the daily patrol reports.',NOTE)); el.append(Spacer(1,4))
for g in R['highlights']:
    el.append(Paragraph(g['group'],H3)); el.append(bullets(g['items']))

el.append(PageBreak()); el.append(Paragraph('Appendix — Monthly Data Breakdown',H2))
el.append(tbl(R['monthly'],[56*mm,22*mm,22*mm,22*mm,26*mm],boldlast=True)); el.append(Spacer(1,14))
el.append(Paragraph('Notes on the data',H3))
for c in R['caveats']: el.append(Paragraph('• '+c,NOTE))

el.append(PageBreak()); el.append(Paragraph('Appendix — Trend Graphs (full history to Sep 2026)',H2))
figs=[('fig1_calls.png',4.4/11,'Business calls per month — full history, 3-month moving average. The Jul–Sep 2026 quarter is shaded.'),
 ('fig2_funding_vs_calls.png',4.6/11,'Output over time — business calls (3-month average). The 2025 service change and the 2026 LCF pilot are marked.'),
 ('fig3_antisocial.png',4.4/11,'Antisocial behaviour (aggression + public drinking/cannabis combined) per month, full history.'),
 ('fig4_detail_incidents.png',4.4/9,'Detailed incidents handled each month since tracking began (Mar 2026). Jul–Sep 2026 shaded.'),
 ('fig5_total_activity.png',4.6/11,'Total recorded activity per month, all measures combined.')]
for i,(f,ar,cap) in enumerate(figs):
    p=os.path.join(CH,f)
    if os.path.exists(p):
        el.append(KeepTogether([Image(p,width=178*mm,height=178*mm*ar),Paragraph(cap,CAP)]))
        if i in (1,3): el.append(PageBreak())

def deco(cv,doc):
    if doc.page==1: return
    cv.saveState(); cv.setFont('Helvetica',7.5); cv.setFillColor(GREY)
    cv.drawString(16*mm, A4[1]-10*mm, 'Absolute Security Group  |  HOTC Performance Report')
    cv.drawRightString(A4[0]-16*mm, A4[1]-10*mm, 'CONFIDENTIAL')
    cv.setStrokeColor(LIGHT); cv.line(16*mm,A4[1]-12*mm,A4[0]-16*mm,A4[1]-12*mm)
    cv.drawCentredString(A4[0]/2, 8*mm, f'Page {doc.page}  ·  July – September 2026')
    cv.restoreState()
doc=SimpleDocTemplate(OUT,pagesize=A4,topMargin=18*mm,bottomMargin=14*mm,leftMargin=16*mm,rightMargin=16*mm)
doc.build(el,onFirstPage=deco,onLaterPages=deco)
print("SAVED:",OUT)
import shutil; shutil.copy2(OUT, os.path.expanduser("~/Downloads/"+os.path.basename(OUT)))
