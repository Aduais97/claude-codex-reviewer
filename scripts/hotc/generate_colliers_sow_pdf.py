from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                ListFlowable, ListItem)
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
import os

NAVY = colors.HexColor('#0B1F3A')
GOLD = colors.HexColor('#B88A2E')
GOLDL = colors.HexColor('#D9B86B')
GREY = colors.HexColor('#555555')
LBLUE = colors.HexColor('#DCE3EC')

out = os.path.expanduser('~/Desktop/ASG/Colliers/2026/Colliers_Scope_of_Works_Proposal.pdf')
os.makedirs(os.path.dirname(out), exist_ok=True)

doc = SimpleDocTemplate(out, pagesize=A4, topMargin=16*mm, bottomMargin=16*mm,
                        leftMargin=18*mm, rightMargin=18*mm, title='ASG Scope of Works — Colliers')
ss = getSampleStyleSheet()
body = ParagraphStyle('body', parent=ss['Normal'], fontName='Helvetica', fontSize=9.5, leading=13, spaceAfter=4)
bullet = ParagraphStyle('bul', parent=body, leftIndent=8)
h1 = ParagraphStyle('h1', parent=ss['Normal'], fontName='Helvetica-Bold', fontSize=12.5,
                    textColor=NAVY, spaceBefore=10, spaceAfter=4)
small = ParagraphStyle('small', parent=body, fontSize=8.5, textColor=GREY)
sub = ParagraphStyle('sub', parent=ss['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=GOLD, spaceBefore=4, spaceAfter=2)
cellL = ParagraphStyle('cellL', parent=body, fontSize=9, spaceAfter=0)
cellR = ParagraphStyle('cellR', parent=body, fontSize=9, alignment=TA_RIGHT, spaceAfter=0)
cellH = ParagraphStyle('cellH', parent=body, fontSize=9, fontName='Helvetica-Bold', textColor=colors.white, spaceAfter=0)
cellHR = ParagraphStyle('cellHR', parent=cellH, alignment=TA_RIGHT)

E = []

# Header band
hdr = Table([[Paragraph('<font color="white"><b>ABSOLUTE SECURITY GROUP</b></font>',
                ParagraphStyle('x', fontSize=18, leading=22))],
             [Paragraph('<font color="#D9B86B">Scope of Works &amp; Proposal</font>',
                ParagraphStyle('y', fontSize=12, leading=15))]],
            colWidths=[174*mm])
hdr.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),NAVY),
                         ('TOPPADDING',(0,0),(-1,0),8),('BOTTOMPADDING',(0,-1),(-1,-1),8),
                         ('LEFTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,1),(-1,1),0)]))
E += [hdr, Spacer(1,8)]

# Meta
def meta(label,val): return [Paragraph(f'<b><font color="#555555">{label}</font></b>', body),
                             Paragraph(val, body)]
m = Table([meta('Prepared for:','Colliers — Property Management (Attn: Tom Ogg, Sam McGowan)'),
           meta('Site:','Chancery Carpark &amp; associated managed property, Auckland CBD'),
           meta('Prepared by:','Ahmad Duais, CEO — Absolute Security Group Limited'),
           meta('Date:','12 June 2026'),
           meta('Reference:','Safety Information &amp; Other Actions — post-walkthrough')],
          colWidths=[32*mm, 142*mm])
m.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
E += [m]

# 1 Background
E += [Paragraph('1.&nbsp;&nbsp;Background', h1),
      Paragraph('Following our introduction via Heart of the City and the on-site walkthrough of the Chancery '
        'Carpark, this document sets out the proposed scope of works to address current safety issues and prevent '
        'repeat offending. It covers the immediate (core) works plus optional ongoing scope, to be confirmed at the '
        'building-owner meeting on Thursday. Absolute Security Group is New Zealand’s only distributor of the '
        'Mosquito anti-loitering system.', body)]

# 2 Site & risk
E += [Paragraph('2.&nbsp;&nbsp;Site &amp; Risk Summary', h1)]
E += [ListFlowable([ListItem(Paragraph(t, bullet)) for t in [
        'Repeat anti-social behaviour and unauthorised access at the carpark, concentrated in peak-risk periods.',
        'One of the currently installed Mosquito anti-loitering units is damaged and not operating effectively; original supplier unknown.',
        'Complex manager requires a direct, immediate line to a responsive security team.']],
        bulletType='bullet', bulletColor=GOLD, leftIndent=10)]

# 3 Core scope
E += [Paragraph('3.&nbsp;&nbsp;Scope of Works — Core (Immediate)', h1),
  Paragraph('<b>3.1  Mosquito system service &amp; recalibration</b> — on-site diagnostic of the damaged unit, repair or '
     'replacement, and frequency calibration / placement optimisation of all units (as NZ’s only distributor).', body),
  Paragraph('<b>3.2  One-week deterrence operation</b> — a dedicated security officer stationed on-site over a continuous '
     'seven-day period to deter repeat offending, coordinated alongside the HOTC safety team, with body-worn cameras and full incident reporting.', body),
  Paragraph('<b>3.3  Trespass enforcement</b> — issuing and managing trespass notices end-to-end under delegated authority '
     '(subject to written authorisation from Colliers / the building owners).', body),
  Paragraph('<b>3.4  24/7 rapid-response line</b> — direct 09 number for the complex manager (already provided), with the '
     'team personally introduced for immediate assistance.', body)]

# 4 Additional
E += [Paragraph('4.&nbsp;&nbsp;Additional / Ongoing Scope (to confirm Thursday)', h1)]
E += [ListFlowable([ListItem(Paragraph(t, bullet)) for t in [
        'Scheduled patrol coverage across the wider Colliers-managed portfolio, frequency configurable to risk.',
        'Ongoing dedicated / static guarding where a continuous presence is warranted.',
        'Mosquito maintenance plan — scheduled servicing, recalibration and unit replacement as required.',
        'Extension of trespass-enforcement and rapid-response coverage to additional properties.']],
        bulletType='bullet', bulletColor=GOLD, leftIndent=10)]

# 5 Pricing
E += [Paragraph('5.&nbsp;&nbsp;Pricing Summary', h1),
      Paragraph('All figures exclude GST (15%). Core works priced below; additional scope is indicative pending Thursday.', body)]

def tbl(data, widths, header=True, total_row=None):
    t = Table(data, colWidths=widths)
    sty = [('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#BBBBBB')),
           ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
           ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
           ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6)]
    if header:
        sty += [('BACKGROUND',(0,0),(-1,0),NAVY)]
    if total_row is not None:
        sty += [('BACKGROUND',(0,total_row),(-1,total_row),LBLUE)]
    t.setStyle(TableStyle(sty))
    return t

E += [Spacer(1,3), Paragraph('Core works', sub)]
core = [[Paragraph('Item',cellH), Paragraph('Basis',cellH), Paragraph('Total (excl GST)',cellHR)],
        [Paragraph('Mosquito service &amp; recalibration (all units)',cellL), Paragraph('1 on-site visit',cellL), Paragraph('$450.00',cellR)],
        [Paragraph('Replacement Mosquito unit (if required)',cellL), Paragraph('Per unit, supply &amp; install',cellL), Paragraph('from $2,250.00 *',cellR)],
        [Paragraph('One-week deterrence operation — dedicated officer',cellL), Paragraph('12 hrs/day × 7 days = 84 hrs @ $40.00/hr',cellL), Paragraph('$3,360.00',cellR)],
        [Paragraph('Trespass delegation setup &amp; enforcement',cellL), Paragraph('Under delegated authority',cellL), Paragraph('Included',cellR)],
        [Paragraph('24/7 rapid-response line',cellL), Paragraph('Direct 09 line + introduction',cellL), Paragraph('Included',cellR)]]
E += [tbl(core, [78*mm, 62*mm, 34*mm])]

summ = [[Paragraph('Summary',cellH), Paragraph('',cellH), Paragraph('Amount',cellHR)],
        [Paragraph('Core subtotal (excl replacement unit)',cellL), Paragraph('',cellL), Paragraph('$3,810.00',cellR)],
        [Paragraph('GST (15%)',cellL), Paragraph('',cellL), Paragraph('$571.50',cellR)],
        [Paragraph('<b>Core total (incl GST)</b>',cellL), Paragraph('',cellL), Paragraph('<b>$4,381.50</b>',cellR)]]
E += [Spacer(1,2), tbl(summ, [78*mm, 62*mm, 34*mm], total_row=3)]
E += [Paragraph('* Replacement unit quoted following on-site diagnostic; repair preferred where viable.', small)]

E += [Spacer(1,4), Paragraph('Additional / ongoing (indicative — confirm Thursday)', sub)]
ong = [[Paragraph('Item',cellH), Paragraph('Basis',cellH), Paragraph('Rate (excl GST)',cellHR)],
       [Paragraph('Scheduled patrol coverage',cellL), Paragraph('Per officer hour',cellL), Paragraph('from $40.00/hr',cellR)],
       [Paragraph('Dedicated / static guarding',cellL), Paragraph('Per officer hour',cellL), Paragraph('from $40.00/hr',cellR)],
       [Paragraph('Mosquito maintenance plan',cellL), Paragraph('Annual programme',cellL), Paragraph('from $1,200.00/yr',cellR)]]
E += [tbl(ong, [78*mm, 62*mm, 34*mm])]

# 6 Assumptions
E += [Paragraph('6.&nbsp;&nbsp;Pricing Basis, Assumptions &amp; Exclusions', h1)]
abullets = [
 'Officer rate: $40.00/hr + GST (standard commercial rate; the HOTC subsidised contract rate does not apply outside HOTC scope).',
 'One-week operation assumes 12 hrs/day coverage of the peak-risk window over 7 consecutive days (84 hrs) — adjustable on confirmation.',
 'Mosquito service fee is for diagnostic and recalibration; parts / replacement units quoted after inspection.',
 'Trespass enforcement is subject to written authorisation / delegation from Colliers or the building owners.',
 'Pricing valid for 30 days. Public-holiday and overnight loadings may apply if the operation window changes.']
abox = Table([[ListFlowable([ListItem(Paragraph(t, bullet)) for t in abullets],
              bulletType='bullet', bulletColor=NAVY, leftIndent=10)]], colWidths=[174*mm])
abox.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LBLUE),
              ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
              ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8)]))
E += [abox]

# 7 Next steps
E += [Paragraph('7.&nbsp;&nbsp;Next Steps', h1)]
E += [ListFlowable([ListItem(Paragraph(t, bullet)) for t in [
        'Colliers to provide written authorisation / delegation for trespass enforcement.',
        'Confirm preferred start date and operation window for the one-week deterrence operation.',
        'Building-owner meeting Thursday to define any additional ongoing scope; final pricing to follow.',
        'On approval, ASG mobilises within 24 hours (guards demonstrated 5-minute on-site response during the walkthrough).']],
        bulletType='bullet', bulletColor=GOLD, leftIndent=10)]

E += [Spacer(1,8),
      Paragraph('<font color="#555555">Absolute Security Group Limited&nbsp;&nbsp;·&nbsp;&nbsp;7/220 Queen St, Auckland CBD 1010'
        '&nbsp;&nbsp;·&nbsp;&nbsp;09 950 4640&nbsp;&nbsp;·&nbsp;&nbsp;ahmad@absolutesecuritygroup.co.nz</font>',
        ParagraphStyle('foot', parent=small, alignment=TA_CENTER))]

doc.build(E)
print(out)
