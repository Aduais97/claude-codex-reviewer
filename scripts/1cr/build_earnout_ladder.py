#!/usr/bin/env python3
"""
1st Call Recruitment — revenue-linked price ladder (earn-out bridge).
Base $1.1m at ~$12.6m revenue, scaling linearly to a $1.6m cap at $13.4m.

Builds:
  1) Ladder chart (PNG + PDF)
  2) Proposal email to Greg Dunn (DOCX, chart embedded)

EBITDA model from the FY26 normalised bridge:
  EBITDA(R) = 0.2005*R - 2,093,288   (R in $;  $441k at FY26 $12.64m)
Price(R):  flat $1.1m below $12.6m; linear to $1.6m at $13.4m; capped $1.6m above.

Deliverables -> ~/Desktop/Acquisitions/1st-Call-Recruitment/Working Files/
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.expanduser("~/Desktop/Acquisitions/1st-Call-Recruitment/Working Files")
PNG = os.path.join(OUT, "1CR_Earnout_Ladder_Chart.png")
PDF = os.path.join(OUT, "1CR_Earnout_Ladder_Chart.pdf")
DOCX = os.path.join(OUT, "1CR_Earnout_Proposal_Email_Greg.docx")

NAVY  = "#13314F"
TEAL  = "#1C8C8C"
GREEN = "#2E8B57"
GREY  = "#9AA6B2"
RED   = "#C0392B"
AMBER = "#B5762B"
INK   = "#1A1A1A"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.edgecolor": "#D5DCE3",
    "text.color": INK, "axes.labelcolor": INK,
    "xtick.color": "#5A6B7B", "ytick.color": "#5A6B7B",
})

GP = 0.2005
OPEX = 2.093288           # $m, ex-KiwiSaver basis (EBITDA $441k at FY26 $12.64m)
R_LO, R_HI = 12.6, 13.4   # earn-out band ($m)
P_LO, P_HI = 0.75, 1.6    # settlement floor -> cap ($m); earn-out pool $0.85m
SLOPE = (P_HI - P_LO) / (R_HI - R_LO)   # 1.0625 price$ per revenue$


def ebitda(R):
    return GP * R - OPEX


def price(R):
    return np.clip(P_LO + (R - R_LO) * SLOPE, P_LO, P_HI)


# ---- chart ---------------------------------------------------------------
R = np.linspace(12.4, 13.6, 240)
P = price(R)

fig, ax = plt.subplots(figsize=(11.6, 7.6))
fig.subplots_adjust(left=0.085, right=0.965, top=0.78, bottom=0.135)

# base vs earn-out shading
ax.fill_between(R, 0, P_LO, color=NAVY, alpha=0.10, zorder=1)
ax.fill_between(R, P_LO, P, color=GREEN, alpha=0.16, zorder=1)

ax.plot(R, P, color=NAVY, lw=2.8, zorder=5)

# band guide lines
ax.axhline(P_LO, color=NAVY, lw=1.0, ls=(0, (3, 3)), zorder=2)
ax.axhline(P_HI, color=RED, lw=1.4, ls=(0, (5, 3)), zorder=2)
ax.text(12.42, P_HI + 0.014, "Vendor ask  $1.6m  (cap)", color=RED,
        fontsize=9.5, fontweight="bold", va="bottom")
ax.text(12.42, P_LO + 0.014, "Settlement  $750k  (floor, paid at completion)",
        color=NAVY, fontsize=9.5, fontweight="bold", va="bottom")

# anchor points + callouts
def pt(R0, label, dy, color=NAVY):
    p0, e0 = price(R0), ebitda(R0) * 1000
    m = (p0 * 1000) / e0
    ax.scatter([R0], [p0], s=70, color=color, zorder=6,
               edgecolor="white", linewidth=1.3)
    ax.annotate(f"{label}\n${p0:.2f}m  ≈ {m:.1f}× EBITDA ${e0:,.0f}k",
                xy=(R0, p0), xytext=(R0, p0 + dy), fontsize=8.8,
                color=color, ha="center", fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=color, lw=0.8))

pt(12.6, "Today  (~$12.6m run-rate)", -0.16, NAVY)
pt(13.0, "Half-way  ($13.0m)", 0.18, GREEN)
pt(13.4, "Full recovery  ($13.4m)", -0.18, RED)

# earn-out band label
ax.annotate("Earn-out pool\n+ up to $0.85m, paid only as\nrevenue actually recovers",
            xy=(12.9, (P_LO + price(12.9)) / 2), xytext=(13.12, 0.92),
            fontsize=8.8, color=GREEN, ha="center", fontweight="bold",
            arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.0))

ax.set_xlim(12.4, 13.6)
ax.set_ylim(0.6, 1.75)
ax.set_xlabel("Trailing-12-month revenue at measurement ($m)", fontsize=10.5)
ax.xaxis.set_major_locator(plt.MultipleLocator(0.2))
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:.1f}m"))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"${y:.2f}m"))
ax.grid(axis="y", color="#EEF2F5", lw=0.9, zorder=0)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)

fig.suptitle("1st Call Recruitment — Revenue-Linked Price Bridge",
             x=0.085, y=0.955, ha="left", fontsize=16.5, fontweight="bold",
             color=NAVY)
fig.text(0.085, 0.862,
         "$750k at settlement (fair value today, ~1.7× maintainable earnings), rising to the full $1.6m ask only if revenue recovers to $13.4m.\n"
         "The remaining $0.85m is paid purely out of the recovery — fair value if it stays flat, a growth premium only if it delivers.",
         ha="left", fontsize=9.8, color="#5A6B7B", linespacing=1.4)
fig.text(0.085, 0.028,
         "Earn-out = (achieved revenue − $12.6m) × 1.0625, capped at $0.85m. EBITDA on the maintainable basis "
         "(20.0% GP, fixed overhead; $441k at FY26). Measured on trailing-12-month revenue post-completion.",
         ha="left", fontsize=7.6, color="#8895A2")

fig.savefig(PNG, dpi=300, facecolor="white"); print("Wrote", PNG)
fig.savefig(PDF, facecolor="white"); print("Wrote", PDF)

# ---- email docx ----------------------------------------------------------
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
st = doc.styles["Normal"]
st.font.name = "Calibri"
st.font.size = Pt(11)
st.font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)
NAVY_T = (0x13, 0x31, 0x4F)


def p(text="", bold=False, size=11, color=None, space_after=6):
    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(space_after)
    r = par.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    if color:
        r.font.color.rgb = RGBColor(*color)
    return par


def bullet(text, bold_lead=None):
    par = doc.add_paragraph(style="List Bullet")
    par.paragraph_format.space_after = Pt(3)
    if bold_lead:
        r = par.add_run(bold_lead); r.bold = True
        par.add_run(text)
    else:
        par.add_run(text)
    return par


hdr = doc.add_paragraph(); hdr.paragraph_format.space_after = Pt(2)
for lbl, val in [("To:  ", "Greg Dunn — gregd@abcbusiness.co.nz"),
                 ("Cc:  ", "Tony Begbie — tonyb@abcbusiness.co.nz")]:
    rr = hdr.add_run(lbl); rr.bold = True
    hdr.add_run(val + "\n")
subj = doc.add_paragraph(); subj.paragraph_format.space_after = Pt(10)
sr = subj.add_run("Subject:  1st Call Recruitment — a way to bridge to $1.6m")
sr.bold = True; sr.font.color.rgb = RGBColor(*NAVY_T)

p("Hi Greg,")
p("Following my note on the normalised earnings, I’ve been thinking about how we close the "
  "gap between where our numbers land and where Phill wants to be. Rather than argue a single "
  "price across a difference we both know exists, I’d like to put a structure on the table "
  "that lets Phill reach his full $1.6m — paid out of the recovery he believes is coming.")

p("The proposal — cash at settlement plus a revenue-linked earn-out", bold=True, size=12, color=NAVY_T, space_after=4)
bullet("paid at completion. This reflects the business at its current ~$12.6m run-rate — fair value on the maintainable earnings, around 1.7× — and is Phill’s regardless of what happens next.", bold_lead="$750,000 at settlement:  ")
bullet("a further amount of up to $850,000, taking the total to the full $1.6m, earned as revenue recovers from $12.6m toward $13.4m.", bold_lead="Earn-out:  ")
bullet("the additional consideration scales straight-line with revenue — every $1.0m of revenue above $12.6m releases $1.0625m of earn-out, to the $1.6m cap. At $13.0m the total is about $1.18m; reach $13.4m and Phill receives the full $1.6m.", bold_lead="How it scales:  ")
bullet("to reward a genuine recovery rather than a single strong season, we’d measure it in two equal annual tranches (up to $425,000 each) on trailing-12-month revenue at the first and second anniversaries of completion.", bold_lead="Paid in two tranches:  ")

doc.add_picture(PNG, width=Inches(6.3))
cap = doc.paragraphs[-1]; cap.alignment = WD_ALIGN_PARAGRAPH.CENTER

p("Why this should work for Phill", bold=True, size=12, color=NAVY_T, space_after=4)
p("Phill’s case for $1.6m rests on the business recovering. This structure pays him exactly "
  "that — in full — if it does. He takes $750,000 in cash on day one, and the balance is "
  "funded by the very growth it’s priced on rather than out of our pocket up front. If the "
  "recovery is as real as he believes, he is no worse off than a $1.6m sale today; he simply "
  "collects the upside over the first 12–24 months, as it’s proven.")
p("From our side it lets us commit, because we’re paying for performance we can see rather "
  "than a forecast we can’t yet verify — which is also what our funder needs to get "
  "comfortable. It puts the risk where the conviction is.")

p("What I’d need to finalise it", bold=True, size=12, color=NAVY_T, space_after=4)
bullet("The FY25 monthly P&L (or at least April–May 2025), so we set the $12.6m baseline like-for-like against the seasonal pattern rather than the peak.", bold_lead="Baseline data:  ")
bullet("Agreement that revenue is measured on the transferred client book over the two annual windows, and on how new business won post-completion is treated.", bold_lead="Mechanics:  ")
p("Happy to walk Phill or KPMG through the structure and the earnings work behind it on a "
  "call. I think this is the most honest way to bridge the gap — it gives Phill his number "
  "if the business delivers, and gives us a deal we can stand behind either way.")

p("Kind regards,", space_after=2)
p("Ahmad Duais", bold=True, space_after=0)
p("Absolute Security Group", space_after=0, size=10, color=(0x5A, 0x6B, 0x7B))

doc.save(DOCX)
print("Wrote", DOCX)

# ---- console table -------------------------------------------------------
print("\nLadder:")
for r in (12.6, 12.8, 13.0, 13.2, 13.4):
    e = ebitda(r) * 1000
    pr = price(r)
    print(f"  ${r:.1f}m rev -> price ${pr*1000:,.0f}k  | EBITDA ${e:,.0f}k  | {pr*1000/e:.2f}x")
