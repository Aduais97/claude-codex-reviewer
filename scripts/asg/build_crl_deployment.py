#!/usr/bin/env python3
"""CRL Grand Opening — Guard Deployment Layout (xlsx).
One tab per station (posts, security layer, officer count, role) + a Deployment Summary tab.
Data is lifted verbatim from the sent proposal (Section 3 station plans + Section 2 six-layer
model + Section 5 programme hours). Officer counts and totals are NOT invented — they match the
proposal to the officer. Rebuild if the proposal deployment changes.

Out: ~/Desktop/ASG/Operations/Clients/CRL/CRL_Grand_Opening_Guard_Deployment.xlsx
"""
import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L

OUT = os.path.expanduser("~/Desktop/ASG/Operations/Clients/CRL/CRL_Grand_Opening_Guard_Deployment.xlsx")

# ---- ASG brand ----
NAVY="1E2A3A"; GOLD="C8952A"; LIGHT="EEF2F6"; BAND="D9E1EA"; WHITE="FFFFFF"; INK="1F2733"; SUB="5A6675"
thin=Side(style="thin", color="C9D2DC"); B=Border(left=thin,right=thin,top=thin,bottom=thin)
CEN=Alignment(horizontal="center", vertical="center")
LEFT=Alignment(horizontal="left", vertical="center", wrap_text=True)
LEFTT=Alignment(horizontal="left", vertical="center", indent=1)

# Layer labels (Section 2 six-layer model) + a reserve/relief tier
L1="1 · Outer perimeter & portals"; L2="2 · Entry & access control"; L3="3 · Screening / bag-check"
L4="4 · Concourse & platform"; L5="5 · Command & control"; L6="6 · Emergency egress"
RES="Relief & surge reserve"

# group key used for the summary cross-tab
GRP_ORDER=["Command & supervision","Entry / access control","Screening / bag-check",
           "Platform & concourse","Perimeter / portals / frontage","Egress / emergency","Relief & reserve"]

# Each station: (post, layer, group, officers, role)
STATIONS = {
 "Karanga-a-Hape (K Rd)": {
   "peak":3500, "total":44,
   "zones":"Mercury Lane + Beresford Square portals · Mercury Lane platform · Beresford platform · ground floor · upstairs concourse",
   "posts":[
     ("Station Event Manager + Supervisors", L5, "Command & supervision", 4, "Command point, radio net; live liaison with AT, NZ Police, FENZ & first-aid; incident logging & escalation"),
     ("Mercury Lane entry / access control", L2, "Entry / access control", 6, "Ticket / access verification & lane management at the main portal"),
     ("Bag-check / screening", L3, "Screening / bag-check", 6, "Consent-based bag & property inspection; same-gender screening on request; refusal = no entry"),
     ("Beresford Square portal & egress", L1, "Perimeter / portals / frontage", 3, "Secondary portal control + marked emergency egress route"),
     ("Platform ends (both caverns)", L4, "Platform & concourse", 5, "Platform-end posts across both caverns; capacity monitoring"),
     ("Concourse & upstairs roving", L4, "Platform & concourse", 6, "Roving ground-floor & upstairs concourse; behavioural assessment & de-escalation"),
     ("Protest watch / frontage team (dedicated)", L1, "Perimeter / portals / frontage", 5, "Mercury Lane frontage; observe-and-document, non-engagement; NZ Police liaison"),
     ("Roving floaters / capacity reserve", RES, "Relief & reserve", 9, "Scheduled break / relief cover + surge capacity so no critical post is left unmanned"),
   ]},
 "Te Waihorotiu (Aotea)": {
   "peak":4000, "total":50,
   "zones":"Bledisloe Lane entry · ground & upstairs concourse · deep platform · emergency-service access point",
   "posts":[
     ("Station Event Manager + Supervisors", L5, "Command & supervision", 4, "Command point, radio net; multi-agency liaison; incident logging & escalation"),
     ("Bledisloe Lane entry / access control", L2, "Entry / access control", 7, "Ticket / access verification & lane management"),
     ("Bag-check / screening", L3, "Screening / bag-check", 7, "Consent-based screening at designated check points; same-gender on request"),
     ("Platform ends & mid-platform", L4, "Platform & concourse", 6, "Deep-platform ends + mid-platform posts; capacity monitoring"),
     ("Concourse (ground + upstairs) roving", L4, "Platform & concourse", 7, "Roving concourse coverage; behavioural assessment & de-escalation"),
     ("Emergency-service access warden", L6, "Egress / emergency", 1, "Keeps the FENZ / ambulance access lane clear and re-openable throughout"),
     ("Egress / evacuation wardens", L6, "Egress / emergency", 3, "Marked emergency routes under the station's FENZ-approved evacuation scheme"),
     ("Roving floaters / capacity reserve", RES, "Relief & reserve", 15, "Scheduled break / relief cover + surge capacity"),
   ]},
 "Maungawhau (Mt Eden)": {
   "peak":3500, "total":44,
   "zones":"Ground-floor entry · long island platform (c0–c4+) · upstairs nerve centre · vent-building / plant side",
   "posts":[
     ("Station Event Manager + Supervisors", L5, "Command & supervision", 4, "Nerve-centre control, radio net; multi-agency liaison; incident logging"),
     ("Ground-floor entry / access control", L2, "Entry / access control", 6, "Ticket / access verification at the ground-floor entry"),
     ("Bag-check / screening", L3, "Screening / bag-check", 6, "Consent-based bag & property inspection; same-gender on request"),
     ("Platform — ends + mid-platform egress", L4, "Platform & concourse", 6, "Long island platform (c0–c4+) ends + mid-platform egress; capacity monitoring"),
     ("Vent-building / plant-side posts", L1, "Perimeter / portals / frontage", 2, "Plant-side perimeter posts"),
     ("Nerve-centre / control + concourse", L5, "Command & supervision", 3, "Upstairs nerve-centre + concourse coverage"),
     ("Egress / evacuation wardens", L6, "Egress / emergency", 3, "Marked emergency routes under the FENZ-approved evacuation scheme"),
     ("Roving floaters / capacity reserve", RES, "Relief & reserve", 14, "Scheduled break / relief cover + surge capacity"),
   ]},
}
SHIFT_H = 11  # event-day operational shift

def band(ws, r, c1, c2, text, fill, color=WHITE, size=10, bold=True, italic=False, h=None, align=None):
    ws.merge_cells(start_row=r, start_column=c1, end_row=r, end_column=c2)
    cell=ws.cell(r,c1,text)
    cell.font=Font(name="Arial", size=size, bold=bold, italic=italic, color=color)
    cell.fill=PatternFill("solid", fgColor=fill)
    cell.alignment=align or Alignment(horizontal="left", vertical="center", indent=1, wrap_text=True)
    if h: ws.row_dimensions[r].height=h

def hdr(ws, r, labels, widths=None):
    for i,t in enumerate(labels,1):
        c=ws.cell(r,i,t); c.font=Font(name="Arial", size=9.5, bold=True, color=WHITE)
        c.fill=PatternFill("solid", fgColor=NAVY); c.border=B
        c.alignment=Alignment(horizontal="center" if i!=1 else "left", vertical="center", indent=0 if i!=1 else 1, wrap_text=True)
    ws.row_dimensions[r].height=24

wb=openpyxl.Workbook()

# ============ TAB 1: Deployment Summary ============
ss=wb.active; ss.title="Deployment Summary"
for i,w in enumerate([34,15,15,16,15],1): ss.column_dimensions[L(i)].width=w
band(ss,1,1,5,"CITY RAIL LINK — Grand Opening Event Security Deployment", NAVY, size=14, h=26)
band(ss,2,1,5,"Three-station activation · one event day per station (Saturdays, 2nd half Q3 2026) · 11-hour event day · heightened 1 officer : 80 patrons", LIGHT, color=SUB, size=9, bold=False, italic=True, h=18)

r=4
band(ss,r,1,5,"Event-day deployment by station", GOLD, color=NAVY, size=10.5, h=18); r+=1
hdr(ss,r,["Station","Peak capacity","Officers (event day)","Guard-hours (×11h)","Coverage"]); r+=1
sub_off=0; sub_gh=0
for name,d in STATIONS.items():
    off=d["total"]; gh=off*SHIFT_H; sub_off+=off; sub_gh+=gh
    vals=[name, d["peak"], off, gh, "1 : 80"]
    for i,v in enumerate(vals,1):
        c=ss.cell(r,i,v); c.border=B; c.font=Font(name="Arial", size=10, color=INK)
        c.alignment=LEFTT if i==1 else CEN
        if i in (2,4): c.number_format='#,##0'
    r+=1
vals=["Event days — subtotal (3 stations)","",sub_off,sub_gh,""]
for i,v in enumerate(vals,1):
    c=ss.cell(r,i,v); c.border=B; c.fill=PatternFill("solid", fgColor=LIGHT)
    c.font=Font(name="Arial", size=10, bold=True, color=NAVY); c.alignment=LEFTT if i==1 else CEN
    if i in (2,4): c.number_format='#,##0'
r+=2

# Programme hours (Section 5)
band(ss,r,1,5,"Full programme — guard-hours", GOLD, color=NAVY, size=10.5, h=18); r+=1
hdr(ss,r,["Programme component","Officers","Basis","Guard-hours",""]); ss.merge_cells(start_row=r,start_column=4,end_row=r,end_column=5); r+=1
prog=[
  ("Event days (3 stations)", "138", "3 × 11-hour event day", sub_gh),
  ("Friday test run (dress rehearsal)", "69", "50% deployment 22 / 25 / 22 · 4:30–7:30pm (3h)", 207),
  ("Pack-in & pack-out support", "—", "Fri 4×8h + Sun 2×6h, ×3 stations", 132),
]
ptot=0
for comp,offs,basis,gh in prog:
    ptot+=gh
    ss.cell(r,1,comp).alignment=LEFTT; ss.cell(r,2,offs).alignment=CEN
    ss.cell(r,3,basis).alignment=LEFT
    ss.merge_cells(start_row=r,start_column=4,end_row=r,end_column=5)
    gc=ss.cell(r,4,gh); gc.alignment=CEN; gc.number_format='#,##0'
    for i in range(1,6):
        c=ss.cell(r,i); c.border=B
        if not c.font or not c.font.bold: c.font=Font(name="Arial", size=10, color=INK)
    r+=1
ss.cell(r,1,"Indicative programme total").alignment=LEFTT
ss.merge_cells(start_row=r,start_column=2,end_row=r,end_column=3)
ss.merge_cells(start_row=r,start_column=4,end_row=r,end_column=5)
tc=ss.cell(r,4,ptot); tc.number_format='#,##0'; tc.alignment=CEN
for i in range(1,6):
    c=ss.cell(r,i); c.border=B; c.fill=PatternFill("solid", fgColor=GOLD)
    c.font=Font(name="Arial", size=10, bold=True, color=NAVY)
    if i==1: c.alignment=LEFTT
    elif i==4: c.alignment=CEN
r+=2

# Function cross-tab
band(ss,r,1,5,"Officers by function — across stations", GOLD, color=NAVY, size=10.5, h=18); r+=1
hdr(ss,r,["Function","Karanga-a-Hape","Te Waihorotiu","Maungawhau","Total"]); r+=1
names=list(STATIONS.keys())
for grp in GRP_ORDER:
    row=[grp]; tot=0
    for name in names:
        n=sum(p[3] for p in STATIONS[name]["posts"] if p[2]==grp); row.append(n); tot+=n
    row.append(tot)
    for i,v in enumerate(row,1):
        c=ss.cell(r,i,v); c.border=B; c.font=Font(name="Arial", size=10, color=INK)
        c.alignment=LEFTT if i==1 else CEN
    r+=1
row=["TOTAL — event-day officers"]+[STATIONS[n]["total"] for n in names]+[sub_off]
for i,v in enumerate(row,1):
    c=ss.cell(r,i,v); c.border=B; c.fill=PatternFill("solid", fgColor=LIGHT)
    c.font=Font(name="Arial", size=10, bold=True, color=NAVY); c.alignment=LEFTT if i==1 else CEN
r+=2
ss.cell(r,1,"Overnight infrastructure security (Fri & Sat nights) is covered under ASG's existing 24-hour static contract at these stations — no additional charge. Roving reserve doubles as the break/relief tier; final post counts confirm at the joint per-station walk-through against issued site plans & run sheet.").font=Font(name="Arial", size=8.5, italic=True, color=SUB)
ss.merge_cells(start_row=r,start_column=1,end_row=r+2,end_column=5)
ss.cell(r,1).alignment=Alignment(horizontal="left", vertical="top", wrap_text=True, indent=1)
ss.sheet_view.showGridLines=False
ss.freeze_panes="A3"

# ============ TABS 2-4: one per station ============
SAFE={"Karanga-a-Hape (K Rd)":"K Rd — Karanga-a-Hape",
      "Te Waihorotiu (Aotea)":"Te Waihorotiu — Aotea",
      "Maungawhau (Mt Eden)":"Maungawhau — Mt Eden"}
for name,d in STATIONS.items():
    ws=wb.create_sheet(SAFE[name][:31])
    for i,w in enumerate([42,26,10,54],1): ws.column_dimensions[L(i)].width=w
    band(ws,1,1,4,f"{name.upper()} — Event-Day Deployment", NAVY, size=13, h=25)
    band(ws,2,1,4,f"Peak capacity {d['peak']:,} patrons  ·  event-day total {d['total']} officers  ·  1 officer : 80  ·  11-hour operational shift  ·  Saturday (2nd half Q3 2026)", LIGHT, color=SUB, size=9, bold=False, italic=True, h=18)
    band(ws,3,1,4,f"Zones covered:  {d['zones']}", WHITE, color=INK, size=9, bold=False, italic=True, h=16, align=Alignment(horizontal="left", vertical="center", indent=1, wrap_text=True))
    hdr(ws,5,["Post / Function","Security layer","Officers","Role / coverage"])
    r=6
    for post,layer,grp,off,role in d["posts"]:
        ws.cell(r,1,post).alignment=LEFTT; ws.cell(r,1).font=Font(name="Arial", size=10, bold=True, color=INK)
        ws.cell(r,2,layer).alignment=Alignment(horizontal="left", vertical="center", indent=1, wrap_text=True)
        oc=ws.cell(r,3,off); oc.alignment=CEN; oc.font=Font(name="Arial", size=11, bold=True, color=NAVY)
        ws.cell(r,4,role).alignment=LEFT
        for i in range(1,5):
            c=ws.cell(r,i); c.border=B
            if not c.font.bold: c.font=Font(name="Arial", size=9.5, color=INK)
        ws.row_dimensions[r].height=30
        r+=1
    # total row
    ws.cell(r,1,"EVENT-DAY TOTAL").alignment=LEFTT
    ws.merge_cells(start_row=r,start_column=1,end_row=r,end_column=2)
    tc=ws.cell(r,3,d["total"]); tc.alignment=CEN
    ws.cell(r,4,f"= {d['total']} officers × 11h = {d['total']*SHIFT_H:,} guard-hours").alignment=LEFTT
    for i in range(1,5):
        c=ws.cell(r,i); c.border=B; c.fill=PatternFill("solid", fgColor=GOLD)
        c.font=Font(name="Arial", size=10.5, bold=True, color=NAVY)
        if i==3: c.alignment=CEN
    ws.row_dimensions[r].height=22
    r+=2
    ws.cell(r,1,"Post counts are the planned event-day baseline; final allocations confirm at the joint walk-through against the issued site plans & run sheet. The roving reserve provides scheduled break/relief cover as well as surge capacity, so no critical post (screening lane, portal, platform end, egress warden) is left unmanned across the 11-hour shift.").font=Font(name="Arial", size=8.5, italic=True, color=SUB)
    ws.merge_cells(start_row=r,start_column=1,end_row=r+2,end_column=4)
    ws.cell(r,1).alignment=Alignment(horizontal="left", vertical="top", wrap_text=True, indent=1)
    ws.sheet_view.showGridLines=False
    ws.freeze_panes="A6"

wb.save(OUT)
print(f"wrote {OUT}")
tot=sum(d["total"] for d in STATIONS.values())
print(f"  tabs: Deployment Summary + {len(STATIONS)} stations")
for name,d in STATIONS.items():
    chk=sum(p[3] for p in d["posts"])
    print(f"    {name}: {chk} officers  ({'OK' if chk==d['total'] else 'MISMATCH vs '+str(d['total'])})")
print(f"  event-day officers total: {tot}  |  event-day guard-hours: {tot*SHIFT_H:,}  |  programme gh: {tot*SHIFT_H+207+132:,}")
