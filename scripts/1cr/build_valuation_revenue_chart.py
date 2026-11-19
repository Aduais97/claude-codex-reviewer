#!/usr/bin/env python3
"""
1st Call Recruitment — Revenue vs implied value ($12.1m -> $13.7m).
Shows maintainable EBITDA and implied valuation at 1.5x / 2.0x / 3.0x across
the revenue range, against the $1.6m vendor ask.

Model (from the FY26 normalised bridge):
  maintainable GP  = 20.05% of revenue
  fixed OpEx       = $2,143,259  (gives EBITDA $391k at FY26 revenue $12.64m)
  EBITDA(R)        = 0.2005*R - 2,143,259   (overhead fixed -> ~20% drop-through)

Deliverables -> ~/Desktop/Acquisitions/1st-Call-Recruitment/Working Files/
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.expanduser("~/Desktop/Acquisitions/1st-Call-Recruitment/Working Files")
PNG = os.path.join(OUT, "1CR_Revenue_vs_Value_Chart.png")
PDF = os.path.join(OUT, "1CR_Revenue_vs_Value_Chart.pdf")

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
OPEX = 2.093259           # $m, ex-KiwiSaver basis; net of $50k retained sublease rent
                          # (EBITDA $441k at FY26 revenue $12.64m)

def ebitda(R):            # R in $m -> EBITDA in $m
    return GP * R - OPEX

R = np.linspace(12.1, 13.7, 200)
eb = ebitda(R)

fig, ax = plt.subplots(figsize=(11.6, 7.6))
fig.subplots_adjust(left=0.085, right=0.845, top=0.82, bottom=0.115)

# valuation fan
ax.plot(R, 3.0 * eb, color=GREEN, lw=2.2, zorder=4)
ax.plot(R, 2.0 * eb, color=TEAL,  lw=2.2, zorder=4)
ax.plot(R, 1.5 * eb, color=GREY,  lw=2.2, zorder=4)
ax.plot(R, eb,       color=NAVY,  lw=2.8, zorder=5)

# vendor ask
ax.axhline(1.6, color=RED, lw=1.8, ls=(0, (5, 3)), zorder=3)
ax.text(12.12, 1.63, "Vendor ask  $1.6m", color=RED, fontsize=10,
        fontweight="bold", va="bottom")

# right-edge labels
def endlab(y, txt, color):
    ax.text(13.74, y, txt, color=color, fontsize=10, fontweight="bold", va="center")
endlab(3.0 * eb[-1], "3.0×", GREEN)
endlab(2.0 * eb[-1], "2.0×", TEAL)
endlab(1.5 * eb[-1], "1.5×", GREY)
endlab(eb[-1],       "EBITDA", NAVY)

# crossing: 3x = 1.6m  ->  EBITDA 0.5333 -> R
R_cross = (1.6 / 3.0 + OPEX) / GP
ax.scatter([R_cross], [1.6], s=70, color=RED, zorder=6, edgecolor="white", linewidth=1.2)
ax.annotate(f"3× reaches $1.6m only at\n~${R_cross:.2f}m revenue  (+4% vs FY26)",
            xy=(R_cross, 1.6), xytext=(R_cross - 0.02, 1.20),
            fontsize=9.3, color=RED, ha="center", fontweight="bold",
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.1))

# key revenue markers
def vline(x, label, ytxt):
    ax.axvline(x, color="#C9D3DC", lw=1.0, ls=(0, (2, 3)), zorder=1)
    ax.text(x, ytxt, label, rotation=90, va="bottom", ha="right",
            fontsize=8.2, color="#7A8794")
vline(12.10, "Run-rate  ~$12.1m", 0.15)
vline(12.64, "FY26  $12.64m", 0.15)

# anchor points on EBITDA line
for x in (12.10, 12.64, 13.7):
    ax.scatter([x], [ebitda(x)], s=34, color=NAVY, zorder=6,
               edgecolor="white", linewidth=1)
ax.annotate("FY26: EBITDA ~$441k", xy=(12.64, ebitda(12.64)),
            xytext=(12.64, 0.74), fontsize=8.6, color=NAVY, ha="center",
            arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.8))

# shortfall callout box
ax.text(12.16, 1.40,
        "At realistic multiples for a declining,\n"
        "20%-margin labour-hire book:\n"
        "•  2.0× tops out at ~$1.31m\n"
        "•  1.5× tops out at ~$0.98m\n"
        "…even at $13.7m revenue — neither\n"
        "reaches $1.6m.",
        fontsize=8.8, color="#33454F", va="top",
        bbox=dict(boxstyle="round,pad=0.6", fc="#F4F7F9", ec="#D5DCE3", lw=1))

ax.set_xlim(12.1, 13.7)
ax.set_ylim(0, 2.0)
ax.set_xlabel("Annual revenue ($m)", fontsize=10.5)
ax.xaxis.set_major_locator(plt.MultipleLocator(0.2))
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:.1f}m"))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"${y:.1f}m"))
ax.grid(axis="y", color="#EEF2F5", lw=0.9, zorder=0)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)

fig.suptitle("1st Call Recruitment — Revenue vs Implied Value",
             x=0.085, y=0.95, ha="left", fontsize=16.5, fontweight="bold",
             color=NAVY)
fig.text(0.085, 0.885,
         "Maintainable EBITDA at 20.0% GP with fixed overhead, and the value it implies at 1.5× / 2.0× / 3.0×, "
         "across $12.1m–$13.7m of revenue.",
         ha="left", fontsize=9.8, color="#5A6B7B")
fig.text(0.085, 0.028,
         "EBITDA on the pre-KiwiSaver-normalisation basis ($441k at FY26), net of $50k retained sublease rent. Normalising KiwiSaver "
         "lowers it ~$65k and pushes the 3× crossing right to ~$13.4m. Source: FY26 Xero P&L (year ended 31 Mar 2026).",
         ha="left", fontsize=7.6, color="#8895A2")

fig.savefig(PNG, dpi=300, facecolor="white"); print("Wrote", PNG)
fig.savefig(PDF, facecolor="white"); print("Wrote", PDF)
