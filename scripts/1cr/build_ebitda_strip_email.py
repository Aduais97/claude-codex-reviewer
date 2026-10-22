#!/usr/bin/env python3
"""
1st Call Recruitment (JCR 2006 Ltd) — FY26 Normalisation deliverables.
Builds:
  1) A two-panel strip-out waterfall chart (GP + EBITDA)  -> PNG
  2) A broker-facing email to Greg Dunn with the chart embedded -> DOCX

All figures sourced line-by-line from Xero_Profit_and_Loss_FY26_Draft.pdf
(JCR 2006 Limited, year ended 31 March 2026).

Deliverables -> ~/Desktop/Acquisitions/1st-Call-Recruitment/Working Files/
Script lives in the repo per the 'no local working files' rule.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

OUT = os.path.expanduser("~/Desktop/Acquisitions/1st-Call-Recruitment/Working Files")
PNG = os.path.join(OUT, "1CR_EBITDA_GP_Stripout_Chart.png")
PDF = os.path.join(OUT, "1CR_EBITDA_GP_Stripout_Chart.pdf")
DOCX = os.path.join(OUT, "1CR_EBITDA_Normalisation_Email_Greg.docx")

# ---- palette -------------------------------------------------------------
NAVY  = "#13314F"   # totals / brand
TEAL  = "#1C8C8C"   # maintainable totals
GREEN = "#2E8B57"   # add-backs
RED   = "#C0392B"   # strip-outs
GREY  = "#9AA6B2"
INK   = "#1A1A1A"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.edgecolor": "#D5DCE3",
    "axes.linewidth": 0.8,
    "text.color": INK,
    "axes.labelcolor": INK,
    "xtick.color": INK,
    "ytick.color": "#5A6B7B",
})


def money_k(v):
    s = f"${abs(v):,.0f}k"
    if v < 0:
        return "−" + s
    return s


def delta_k(v):
    s = f"${abs(v):,.0f}k"
    return ("+" if v > 0 else "−") + s


def waterfall(ax, labels, values, kinds, title, subtitle, inside_labels=None):
    inside_labels = inside_labels or {}
    running = 0.0
    tops = []          # (x, top_of_bar) for connectors
    for i, (v, k) in enumerate(zip(values, kinds)):
        if k == "total":
            bottom, height, running = 0.0, v, v
            color = NAVY if i == 0 else TEAL
        else:
            start, end = running, running + v
            bottom, height = min(start, end), abs(v)
            running = end
            color = GREEN if v > 0 else RED
        ax.bar(i, height, bottom=bottom, width=0.62, color=color,
               edgecolor="white", linewidth=0.6, zorder=3)
        top = bottom + height
        tops.append(top if k == "total" else max(start, end))
        # value label
        if k == "total":
            ax.text(i, top, money_k(v), ha="center", va="bottom",
                    fontsize=10.5, fontweight="bold", color=color, zorder=5)
        else:
            ax.text(i, top + (ax_ymax(values) * 0.012), delta_k(v),
                    ha="center", va="bottom", fontsize=9, fontweight="bold",
                    color=color, zorder=5)
        # optional in-bar label (e.g. GP %)
        if i in inside_labels:
            ax.text(i, bottom + height * 0.90, inside_labels[i], ha="center",
                    va="center", fontsize=10.5, fontweight="bold",
                    color="white", zorder=6)
    # connectors
    for i in range(len(values) - 1):
        if kinds[i] == "total":
            y = values[i] if i == 0 else tops[i]
        else:
            y = tops[i]
        # connect from running level after bar i to start of bar i+1
        run_after = sum_running(values, kinds, i)
        ax.plot([i + 0.31, i + 1 - 0.31], [run_after, run_after],
                color=GREY, lw=0.9, ls=(0, (4, 3)), zorder=2)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, fontsize=8.6)
    ax.set_ylim(0, ax_ymax(values) * 1.16)
    ax.set_title(title, fontsize=13.5, fontweight="bold", color=NAVY,
                 loc="left", pad=26)
    ax.text(0, 1.045, subtitle, transform=ax.transAxes, fontsize=9.3,
            color="#5A6B7B")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}k"))
    ax.grid(axis="y", color="#EEF2F5", lw=0.9, zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def sum_running(values, kinds, idx):
    r = 0.0
    for j in range(idx + 1):
        if kinds[j] == "total":
            r = values[j]
        else:
            r += values[j]
    return r


def ax_ymax(values):
    # peak running total for scaling
    r, peak = 0.0, 0.0
    return max(abs(v) for v in values) if max(values) < 0 else _peak(values)


def _peak(values):
    return 720.0  # set per-panel below


# ---- data (all $000s, from FY26 P&L) -------------------------------------
gp_labels = ["Reported\nGross Profit", "Holiday Pay\nAccrual release",
             "Temping Pays\nAccrual reversal", "Maintainable\nGross Profit"]
gp_values = [2729.49, -154.91, -40.28, 2534.30]
gp_kinds  = ["total", "neg", "neg", "total"]

eb_labels = ["Reported\nEBITDA", "+ Owner\nsalary", "+ IT\nwages", "+ FBT",
             "− Disposal\ngain", "− Holiday Pay\naccrual",
             "− Temping Pays\naccrual", "− Wages Holiday\naccrual",
             "Maintainable\nEBITDA"]
eb_values = [186.73, 385.0, 116.61, 30.0, -22.15, -154.91, -40.28, -59.96, 441.04]
eb_kinds  = ["total", "pos", "pos", "pos", "neg", "neg", "neg", "neg", "total"]

# override per-panel y scaling
def make():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11.2, 12.4))
    fig.subplots_adjust(left=0.085, right=0.965, top=0.83, bottom=0.07, hspace=0.6)

    fig.suptitle("1st Call Recruitment (JCR 2006 Ltd) — FY26 Normalisation",
                 x=0.085, y=0.978, ha="left", fontsize=16.5, fontweight="bold",
                 color=NAVY)
    fig.text(0.085, 0.918,
             "Reported gross profit and earnings are lifted by non-cash provision releases.\n"
             "Removing them — with owner and non-operating items — gives the maintainable earnings a buyer underwrites.",
             ha="left", fontsize=9.6, color="#5A6B7B", linespacing=1.4)

    # patch peak scaling
    global _peak
    _peak = lambda v: 2730.0
    waterfall(ax1, gp_labels, gp_values, gp_kinds,
              "Gross Profit  —  20.0%, not the reported 21.6%",
              "Two accrual releases sit inside Cost of Sales (−$195k), flattering the margin.",
              inside_labels={0: "21.6%", 3: "20.0%"})

    _peak = lambda v: 720.0
    waterfall(ax2, eb_labels, eb_values, eb_kinds,
              "Maintainable EBITDA  —  approximately $441k",
              "Add back owner & non-recurring costs; remove the disposal gain and the three accrual releases.")
    # KiwiSaver conservative annotation
    ax2.annotate("≈ $376k after normalised KiwiSaver",
                 xy=(8, 441.0), xytext=(6.4, 290),
                 fontsize=8.7, color="#7A4B00", ha="center",
                 arrowprops=dict(arrowstyle="-|>", color="#B5762B", lw=1.0))

    fig.text(0.085, 0.022,
             "Source: Xero Profit & Loss, JCR 2006 Limited, year ended 31 March 2026 (draft). "
             "Reported EBITDA = net profit $146k + interest $29k + depreciation $12k. "
             "Figures in $000s. Temping Sales accrual (~$451k) and FY25-vs-FY26 revenue mix excluded pending KPMG detail.",
             ha="left", fontsize=7.6, color="#8895A2")
    fig.savefig(PNG, dpi=300, facecolor="white")
    print("Wrote", PNG)
    fig.savefig(PDF, facecolor="white")          # vector, for email attachment
    print("Wrote", PDF)


make()

# ---- email docx ----------------------------------------------------------
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
st = doc.styles["Normal"]
st.font.name = "Calibri"
st.font.size = Pt(11)
st.font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)


def p(text="", bold=False, size=11, color=None, space_after=6, align=None):
    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(space_after)
    if align:
        par.alignment = align
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
        r = par.add_run(bold_lead)
        r.bold = True
        par.add_run(text)
    else:
        par.add_run(text)
    return par


NAVY_T = (0x13, 0x31, 0x4F)

# header block
hdr = doc.add_paragraph()
hdr.paragraph_format.space_after = Pt(2)
for lbl, val in [("To:  ", "Greg Dunn — gregd@abcbusiness.co.nz"),
                 ("Cc:  ", "Tony Begbie — tonyb@abcbusiness.co.nz")]:
    rr = hdr.add_run(lbl); rr.bold = True
    hdr.add_run(val + "\n")
subj = doc.add_paragraph()
subj.paragraph_format.space_after = Pt(10)
sr = subj.add_run("Subject:  1st Call Recruitment (JCR 2006) — normalised EBITDA & gross profit findings")
sr.bold = True
sr.font.color.rgb = RGBColor(*NAVY_T)

p("Hi Greg,")
p("Thanks for coming back to me, and for being straight on where Phill sits at $1.6m. "
  "Before we either find a way through or draw a line, I want to share — transparently "
  "— what our review of the FY26 accounts produced, because the maintainable earnings "
  "are the whole basis on which we, and any funder behind us, can value the business.")
p("We’ve gone through the FY26 profit and loss line by line. The short version: the "
  "reported gross profit and headline earnings are materially flattered by one-off, "
  "non-cash accounting movements. Once those are normalised, maintainable earnings are a "
  "good deal lower than the reported accounts suggest. The attached one-page chart lays "
  "the adjustments out; the detail is below.")

p("Gross profit — 20.0%, not 21.6%", bold=True, size=12, color=NAVY_T, space_after=4)
p("Reported FY26 gross profit is $2,729,490 (21.6% of trading income). Sitting inside cost "
  "of sales, however, are two provision movements that reduce reported cost and lift the margin:")
bullet("−$154,914 (a credit)", bold_lead="Holiday Pay Accrual:  ")
bullet("−$40,277 (a reversal)", bold_lead="Temping Pays Accrual:  ")
p("These aren’t trading margin — they’re previously-booked provisions unwinding "
  "as the temp workforce contracted (headcount down roughly 29% year-on-year). They’re "
  "non-cash, they don’t recur, and a buyer doesn’t earn them. Strip them out and "
  "maintainable gross profit is $2,534,299 — a true margin of 20.0%.")

p("EBITDA — approximately $440,000 maintainable", bold=True, size=12, color=NAVY_T, space_after=4)
p("Starting from reported EBITDA of about $187,000 (net profit $146,262 + interest + "
  "depreciation), we add back what genuinely won’t carry to a buyer and remove what "
  "isn’t recurring operating earnings:")
bullet("$385,000 — owner is non-operational; the management team’s pay already sits separately in the accounts", bold_lead="+ Shareholder salary  ")
bullet("$116,614 — the in-house developers, which relate to the separate IT venture, not the recruitment business", bold_lead="+ IT wages  ")
bullet("~$30,000 — owner vehicle-related", bold_lead="+ FBT  ")
bullet("$22,152 — gain on asset disposal", bold_lead="− Non-operating other income  ")
bullet("$154,914 + $40,277 in cost of sales, plus a further $59,959 in operating costs", bold_lead="− The three provision releases  ")
p("That nets to a maintainable EBITDA of approximately $440,000. Applying a normalised "
  "employer KiwiSaver rate (FY26 ran at 1.18% vs 1.89% the prior year) takes it closer to "
  "$375,000, and we’ve set the ~$451,000 “Temping Sales” accrual movement to one "
  "side pending KPMG’s detail, as it could move the number either way.")

# embedded chart
doc.add_picture(PNG, width=Inches(6.3))
cap = doc.paragraphs[-1]
cap.alignment = WD_ALIGN_PARAGRAPH.CENTER

p("What this means for value", bold=True, size=12, color=NAVY_T, space_after=4)
p("I’ll be straight because I respect the process. At ~$440,000 of maintainable EBITDA, "
  "$1.6m implies a multiple of around 3.6x. Even a stable, growing recruitment business "
  "rarely trades above ~3–3.5x, and 1st Call’s revenue fell ~29% from FY25 to FY26. "
  "Our read of the monthly numbers through April 2026 doesn’t yet show a recovery — "
  "it shows the usual seasonal peak. A declining-revenue, thin-margin labour-hire book "
  "doesn’t support a 4x multiple.")
p("So I can’t see a credible path to $1.6m on price alone, and I don’t want to waste "
  "Phill’s time pretending otherwise. What I can do:")
bullet("If Phill genuinely believes the recovery is real, I’m open to an earn-out that pays him the upside if and when the revenue actually returns — that bridges the gap and puts the risk where the conviction is.", bold_lead="An earn-out.  ")
bullet("The one thing that could move our number up today is the FY25 monthly P&L (or at least April–May 2025), so we can test the recovery like-for-like rather than against the seasonal peak. If you can get that from KPMG, send it through and we’ll re-run our numbers immediately.", bold_lead="The FY25 monthly data.  ")
p("None of this is a walk — we like the business and the strategic fit — but it has "
  "to be priced off what it actually earns. Happy to jump on a call and take Phill or KPMG "
  "through the attached and the line-by-line if that helps.")

p("Kind regards,", space_after=2)
p("Ahmad Duais", bold=True, space_after=0)
p("Absolute Security Group", space_after=0, size=10, color=(0x5A, 0x6B, 0x7B))

doc.save(DOCX)
print("Wrote", DOCX)
