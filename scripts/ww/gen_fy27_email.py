#!/usr/bin/env python3
"""FY27 W1 cover email (docx) — region-grouped weekly results, mirrors the weekly template."""
import os
from datetime import datetime
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import build_master_v2 as bm

agg, store_region, regions = bm.aggregate()
week = bm.CURRENT_WEEK
WNUM = bm.week_num(week); WLABEL = bm.week_label(week); PARTIAL = bm.is_partial(week)
prev = bm.WEEKS[bm.WEEKS.index(week) - 1] if WNUM > 1 else None
nat = bm.rollup([a for (w, s), a in agg.items() if w == week])
prev_nat = bm.rollup([a for (w, s), a in agg.items() if w == prev]) if prev else None
reg_roll = {r: bm.rollup([a for (w, s), a in agg.items() if w == week and store_region.get(s) == r]) for r in regions}
stores_by_region = {r: len([1 for (w, s), a in agg.items() if w == week and store_region.get(s) == r]) for r in regions}

WNOTE = bm.week_note(week)
def rpct(a):
    tl = a['rec'] + a['lost'] + a['pkg']; return (a['rec'] + a['pkg']) / tl * 100 if tl else 0
REC_PCT = rpct(nat)
OUTDIR = os.path.expanduser(f"~/Desktop/Woolworths /Week Ending {WLABEL}")
OUT = f"{OUTDIR}/Weekly Results - Email to Glenn - Week Ending {WLABEL}.docx"
NAVY = RGBColor(0x1E, 0x2A, 0x3A)


def money(v):
    return f"${v:,.2f}"


doc = Document()
st = doc.styles["Normal"]
st.font.name = "Calibri"; st.font.size = Pt(11)

# header block (To/Cc/Subject)
for lab, val in [("To:", "Glenn Sinclair <glenn.sinclair@woolworths.co.nz>"),
                 ("Cc:", "Mark Clansey <mark@slsrtc.co.nz>"),
                 ("Subject:", f"Weekly Results — Week Ending {WLABEL} (FY27, Week {WNUM})")]:
    p = doc.add_paragraph()
    r = p.add_run(lab + " "); r.bold = True; r.font.color.rgb = NAVY
    p.add_run(val)
    p.paragraph_format.space_after = Pt(2)
doc.add_paragraph().paragraph_format.space_after = Pt(4)

wow = ""
if prev_nat and prev_nat["total_loss"]:
    delta = nat["total_loss"] - prev_nat["total_loss"]; pct = delta / prev_nat["total_loss"] * 100
    # attach the prior week's context note (e.g. a public-holiday short week) so a big WoW
    # swing is never presented without its explanation
    pnote = bm.week_note(prev)
    ctx = ""
    if pnote:
        parts = pnote.split(" — ")
        base = parts[0][0].lower() + parts[0][1:]
        reason = f" ({parts[1].split(',')[0].split(' (')[0]})" if len(parts) > 1 else ""
        ctx = f" — noting last week was a {base}{reason}"
    wow = f" That is {'up' if delta >= 0 else 'down'} {abs(pct):.0f}% on last week ({money(prev_nat['total_loss'])}{ctx})."
intro = f"Please find attached this week's National Loss Prevention & Safety Report and Deployment & Recovery Tracker for the Week Ending {WLABEL}, across the full national network grouped by region."
if PARTIAL:
    intro += " This is the first week of the new financial year (FY27)."
elif WNOTE:
    intro += f" Note this was a {WNOTE}."
body = [
    "Hi Glenn,",
    "I hope you had a great weekend.",
    intro,
    f"This week the covert team identified {money(nat['total_loss'])} in total loss across the network and recovered {REC_PCT:.1f}% of it, from {nat['inc']} incidents involving {nat['off']} offenders, alongside {nat['det']} documented deterrents (a conservative floor as weekend logging settles).{wow} Performance by region:",
]
for i, t in enumerate(body):
    p = doc.add_paragraph(t)
    p.paragraph_format.space_after = Pt(8)

# region table
hdr = ["Region", "Total Loss", "Recovered %", "Incidents", "Deterrents"]
tbl = doc.add_table(rows=1, cols=len(hdr))
tbl.style = "Light Grid Accent 1"
for j, h in enumerate(hdr):
    c = tbl.rows[0].cells[j].paragraphs[0]
    run = c.add_run(h); run.bold = True; run.font.size = Pt(10)
    c.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 else WD_ALIGN_PARAGRAPH.RIGHT
order = sorted(regions, key=lambda r: -reg_roll[r]["total_loss"])
for r in order:
    d = reg_roll[r]
    row = tbl.add_row().cells
    vals = [r, money(d["total_loss"]), f"{rpct(d):.1f}%", str(d["inc"]), str(d["det"])]
    for j, v in enumerate(vals):
        pr = row[j].paragraphs[0]; run = pr.add_run(v); run.font.size = Pt(10)
        pr.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 else WD_ALIGN_PARAGRAPH.RIGHT
# network total row
row = tbl.add_row().cells
netvals = ["NETWORK", money(nat["total_loss"]), f"{REC_PCT:.1f}%", str(nat["inc"]), str(nat["det"])]
for j, v in enumerate(netvals):
    pr = row[j].paragraphs[0]; run = pr.add_run(v); run.bold = True; run.font.size = Pt(10)
    pr.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 else WD_ALIGN_PARAGRAPH.RIGHT

note = doc.add_paragraph()
nr = note.add_run("Total Loss = recovered product + estimated stolen + recovered packaging; Recovered % = value recovered and returned as a share of total loss. Deterrent counts are submissions to date (a conservative floor)." + (" First week of FY27, so week-on-week comparison begins next week." if PARTIAL else " WoW = week-on-week change vs the prior week."))
nr.italic = True; nr.font.size = Pt(9); nr.font.color.rgb = RGBColor(0x8a, 0x95, 0xa3)
note.paragraph_format.space_before = Pt(4)

top = order[0]
close = [
    f"{top} led the network this week on total value returned. Wellington and the lower North Island continued to carry the deterrence and packaging load, while Auckland drove incident volume and direct recovery.",
    "Have a good day ahead.",
    "Many thanks,",
]
for t in close:
    p = doc.add_paragraph(t); p.paragraph_format.space_after = Pt(8)
sig = doc.add_paragraph()
s1 = sig.add_run("Ahmad Duais\n"); s1.bold = True
sig.add_run("Absolute Security Group | SLS RTC\nahmad@absolutesecuritygroup.co.nz")

os.makedirs(OUTDIR, exist_ok=True)
doc.save(OUT)
print("wrote", OUT)
