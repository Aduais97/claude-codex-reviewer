#!/usr/bin/env python3
"""
1st Call Recruitment — maintainable EBITDA vs revenue, $12.0m -> $13.4m.
Two lines: ex-KiwiSaver basis ($441k at FY26) and KiwiSaver-normalised (-$65k).

EBITDA(R) = 0.2005*R - 2,093,288   (ex-KiwiSaver; $441k at FY26 $12.64m)
Deliverables -> ~/Desktop/Acquisitions/1st-Call-Recruitment/Working Files/
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.expanduser("~/Desktop/Acquisitions/1st-Call-Recruitment/Working Files")
PNG = os.path.join(OUT, "1CR_EBITDA_vs_Revenue_Chart.png")
PDF = os.path.join(OUT, "1CR_EBITDA_vs_Revenue_Chart.pdf")

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
OPEX = 2.093288          # $m, ex-KiwiSaver basis
KS = 0.065              # $m KiwiSaver-normalisation haircut

def eb(R):   return GP * R - OPEX
def ebks(R): return GP * R - OPEX - KS

R = np.linspace(12.0, 13.4, 240)

fig, ax = plt.subplots(figsize=(11.6, 7.4))
fig.subplots_adjust(left=0.09, right=0.86, top=0.8, bottom=0.115)

# shade between the two bases
ax.fill_between(R, ebks(R) * 1000, eb(R) * 1000, color=TEAL, alpha=0.10, zorder=1)

ax.plot(R, eb(R) * 1000,  color=NAVY, lw=2.8, zorder=5)
ax.plot(R, ebks(R) * 1000, color=TEAL, lw=2.2, ls=(0, (5, 3)), zorder=5)

# end labels
ax.text(13.43, eb(13.4) * 1000, "Maintainable\n(ex-KiwiSaver)", color=NAVY,
        fontsize=9, fontweight="bold", va="center")
ax.text(13.43, ebks(13.4) * 1000, "KiwiSaver-\nnormalised", color=TEAL,
        fontsize=9, fontweight="bold", va="center")

# key revenue markers
def vmark(x, label):
    ax.axvline(x, color="#C9D3DC", lw=1.0, ls=(0, (2, 3)), zorder=1)
    ax.text(x, 250, label, rotation=90, va="bottom", ha="right",
            fontsize=8.2, color="#7A8794")
vmark(12.10, "Run-rate  ~$12.1m")
vmark(12.64, "FY26  $12.64m")
vmark(13.40, "Recovery  $13.4m")

# anchor points on the main line
for x in (12.0, 12.64, 13.0, 13.4):
    y = eb(x) * 1000
    ax.scatter([x], [y], s=42, color=NAVY, zorder=6, edgecolor="white", linewidth=1.1)
    ax.annotate(f"${y:,.0f}k", xy=(x, y), xytext=(x, y + 26),
                ha="center", fontsize=9, fontweight="bold", color=NAVY, zorder=7)

ax.set_xlim(12.0, 13.4)
ax.set_ylim(200, 650)
ax.set_xlabel("Annual revenue ($m)", fontsize=10.5)
ax.set_ylabel("Maintainable EBITDA ($000s)", fontsize=10.5)
ax.xaxis.set_major_locator(plt.MultipleLocator(0.2))
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:.1f}m"))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"${y:,.0f}k"))
ax.grid(axis="y", color="#EEF2F5", lw=0.9, zorder=0)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)

fig.suptitle("1st Call Recruitment — Maintainable EBITDA vs Revenue",
             x=0.09, y=0.95, ha="left", fontsize=16.5, fontweight="bold",
             color=NAVY)
fig.text(0.09, 0.862,
         "Normalised earnings across $12.0m–$13.4m of revenue at a 20.0% gross margin with fixed overhead.\n"
         "Each extra $1.0m of revenue adds ~$200k of EBITDA — the business is high-drop-through but starts from a thin base.",
         ha="left", fontsize=9.8, color="#5A6B7B", linespacing=1.4)
fig.text(0.09, 0.028,
         "Maintainable basis: FY26 normalised EBITDA $441k (owner, IT, FBT, disposal gain & three accrual releases adjusted; $50k sublease retained). "
         "KiwiSaver-normalised line restates the FY26 1.18% rate toward 1.89%. Source: FY26 Xero P&L (year ended 31 Mar 2026).",
         ha="left", fontsize=7.5, color="#8895A2")

fig.savefig(PNG, dpi=300, facecolor="white"); print("Wrote", PNG)
fig.savefig(PDF, facecolor="white"); print("Wrote", PDF)

print("\nEBITDA by revenue:")
for r in (12.0, 12.2, 12.4, 12.6, 12.64, 12.8, 13.0, 13.2, 13.4):
    print(f"  ${r:5.2f}m  ->  ex-KS ${eb(r)*1000:6,.0f}k   |   KS-norm ${ebks(r)*1000:6,.0f}k")
