#!/usr/bin/env python3
"""Memecoin ETR Technical Review PDF — verdict document from the 29 Sep 2026
22-agent ETR workflow (5 research lenses, 15 adversarially verified claims,
ruleset stress-test of the Grok 'The Floor' trading desk app).

Output: ~/Desktop/Personal/Memecoin_ETR_Review_29Sep2026.pdf
Design: /generate-pdf standards — navy/gold, no callout boxes, TOC, A4.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
    TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.platypus.tableofcontents import TableOfContents

# ---------------------------------------------------------------- palette
NAVY = colors.HexColor("#1B2A4A")
DARKBLUE = colors.HexColor("#2C3E6B")
MIDBLUE = colors.HexColor("#4A6FA5")
GOLD = colors.HexColor("#D4A843")
LIGHTBLUE = colors.HexColor("#E8EDF5")
BGGREY = colors.HexColor("#F7F8FA")
BORDER = colors.HexColor("#D0D5DD")
ROWALT = colors.HexColor("#F2F4F8")
TEXTDARK = colors.HexColor("#1A1A2E")
TEXTMED = colors.HexColor("#4A4A5A")
TEXTLIGHT = colors.HexColor("#7A7A8A")
RED = colors.HexColor("#C0392B")
AMBER = colors.HexColor("#E67E22")
GREEN = colors.HexColor("#27AE60")

PAGE_W, PAGE_H = A4
M_SIDE, M_TOP, M_BOT = 54, 62, 54
CW = PAGE_W - 2 * M_SIDE  # ~487pt

OUT = os.path.expanduser("~/Desktop/Personal/Memecoin_ETR_Review_29Sep2026.pdf")

# ---------------------------------------------------------------- styles
body = ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=14.5,
                      alignment=TA_JUSTIFY, textColor=TEXTDARK, spaceAfter=7)
lead = ParagraphStyle("lead", parent=body, fontName="Helvetica-Bold",
                      textColor=NAVY, spaceBefore=4)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=18, bulletIndent=6,
                        spaceAfter=4, alignment=TA_LEFT)
small_it = ParagraphStyle("small_it", fontName="Helvetica-Oblique", fontSize=8.5,
                          leading=11.5, textColor=TEXTMED, spaceAfter=6)
h2_txt = ParagraphStyle("h2_txt", fontName="Helvetica-Bold", fontSize=13,
                        leading=16, textColor=colors.white)
h3 = ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=11.5, leading=14,
                    textColor=DARKBLUE, spaceBefore=12, spaceAfter=2)
cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.5, leading=11,
                      textColor=TEXTDARK)
cellb = ParagraphStyle("cellb", parent=cell, fontName="Helvetica-Bold")
cellc = ParagraphStyle("cellc", parent=cell, alignment=TA_CENTER)
hcell = ParagraphStyle("hcell", fontName="Helvetica-Bold", fontSize=8.5,
                       leading=11, textColor=colors.white, alignment=TA_CENTER)
hcell_l = ParagraphStyle("hcell_l", parent=hcell, alignment=TA_LEFT)

toc_h = ParagraphStyle("toc_h", fontName="Helvetica-Bold", fontSize=16,
                       textColor=NAVY, spaceAfter=14)


def sect_header(num, title):
    """Navy bar with gold left accent — standard section header."""
    t = Table([[Paragraph(f"{num}&nbsp;&nbsp;{title}", h2_txt)]],
              colWidths=[CW], rowHeights=[24])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LINEBEFORE", (0, 0), (0, -1), 4, GOLD),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def verdict_para(text, colour):
    return Paragraph(f'<font color="{colour.hexval()[2:] if hasattr(colour, "hexval") else colour}"><b>{text}</b></font>', cellc)


def vcell(text, colour):
    hexs = "#%02X%02X%02X" % (int(colour.red * 255), int(colour.green * 255), int(colour.blue * 255))
    return Paragraph(f'<font color="{hexs}"><b>{text}</b></font>', cellc)


def data_table(headers, rows, widths, align_first_left=True, header_left_first=True):
    hdr = [Paragraph(h, hcell_l if (header_left_first and i == 0) else hcell)
           for i, h in enumerate(headers)]
    tbl_rows = [hdr]
    for r in rows:
        line = []
        for i, c in enumerate(r):
            if isinstance(c, Paragraph):
                line.append(c)
            else:
                st = cell if (i == 0 and align_first_left) else cellc
                line.append(Paragraph(str(c), st))
        tbl_rows.append(line)
    t = Table(tbl_rows, colWidths=widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("LINEBELOW", (0, 0), (-1, 0), 1.2, NAVY),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]
    for i in range(1, len(tbl_rows)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), ROWALT))
    t.setStyle(TableStyle(style))
    return t


# ---------------------------------------------------------------- doc template
class ETRDoc(BaseDocTemplate):
    def __init__(self, path, **kw):
        super().__init__(path, pagesize=A4, leftMargin=M_SIDE, rightMargin=M_SIDE,
                         topMargin=M_TOP, bottomMargin=M_BOT, **kw)
        frame = Frame(M_SIDE, M_BOT, CW, PAGE_H - M_TOP - M_BOT, id="main")
        self.addPageTemplates([
            PageTemplate(id="title", frames=[frame], onPage=self._title_page),
            PageTemplate(id="body", frames=[frame], onPage=self._body_page),
        ])

    def _title_page(self, canv, doc):
        pass  # clean title page, no header/footer

    def _body_page(self, canv, doc):
        canv.saveState()
        # header
        canv.setStrokeColor(BORDER)
        canv.setLineWidth(0.5)
        canv.line(M_SIDE, PAGE_H - 40, PAGE_W - M_SIDE, PAGE_H - 40)
        canv.setFont("Helvetica", 7)
        canv.setFillColor(TEXTLIGHT)
        canv.drawString(M_SIDE, PAGE_H - 36, "Ahmad Duais  |  New-Memecoin Investment: ETR Technical Review")
        canv.drawRightString(PAGE_W - M_SIDE, PAGE_H - 36, "CONFIDENTIAL")
        # footer
        canv.line(M_SIDE, 40, PAGE_W - M_SIDE, 40)
        canv.setFont("Helvetica", 7.5)
        canv.drawString(M_SIDE, 30, "29 September 2026")
        canv.drawCentredString(PAGE_W / 2, 30, f"Page {doc.page}")
        canv.drawRightString(PAGE_W - M_SIDE, 30, "ETR Agentic Workflow (22 agents)")
        canv.restoreState()

    def afterFlowable(self, flowable):
        if hasattr(flowable, "_toc_entry"):
            level, text = flowable._toc_entry
            self.notify("TOCEntry", (level, text, self.page))


class TocHook(Spacer):
    """Invisible marker that registers a TOC entry at its render position."""
    def __init__(self, level, text):
        super().__init__(0, 0)
        self._toc_entry = (level, text)


# ---------------------------------------------------------------- content
story = []

# ---- title page
story.append(Spacer(1, 120))
story.append(HRFlowable(width="40%", thickness=1.5, color=GOLD, hAlign="CENTER"))
story.append(Spacer(1, 26))
story.append(Paragraph("New-Memecoin Investment",
             ParagraphStyle("t1", fontName="Helvetica-Bold", fontSize=32,
                            leading=38, textColor=NAVY, alignment=TA_CENTER)))
story.append(Spacer(1, 8))
story.append(Paragraph("ETR Technical Review &amp; Verdict",
             ParagraphStyle("t2", fontName="Helvetica-Bold", fontSize=16,
                            leading=20, textColor=DARKBLUE, alignment=TA_CENTER)))
story.append(Spacer(1, 12))
story.append(Paragraph("Market assessment  ·  Entry-age analysis  ·  Ruleset stress-test",
             ParagraphStyle("t3", fontName="Helvetica-Oblique", fontSize=12,
                            leading=15, textColor=MIDBLUE, alignment=TA_CENTER)))
story.append(Spacer(1, 26))
story.append(HRFlowable(width="40%", thickness=1.5, color=GOLD, hAlign="CENTER"))
story.append(Spacer(1, 56))

info = Table([
    [Paragraph("Prepared for", cellb), Paragraph("Ahmad Duais", cell),
     Paragraph("Date", cellb), Paragraph("29 September 2026", cell)],
    [Paragraph("Method", cellb), Paragraph("ETR agentic workflow — 22 agents, 216 web-research calls", cell),
     Paragraph("Verification", cellb), Paragraph("15 load-bearing claims: 11 CONFIRMED / 4 PARTLY / 0 REFUTED", cell)],
    [Paragraph("Subject", cellb), Paragraph('New-memecoin entry logic incl. the Grok "The Floor" desk app', cell),
     Paragraph("Classification", cellb), Paragraph("INTERNAL", cell)],
], colWidths=[70, 175, 72, 170])
info.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), LIGHTBLUE),
    ("BACKGROUND", (2, 0), (2, -1), LIGHTBLUE),
    ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LEFTPADDING", (0, 0), (-1, -1), 7),
]))
story.append(info)
story.append(Spacer(1, 34))

verdict_row = Table([
    [Paragraph("VERDICT", hcell), Paragraph("ENTRY-AGE WINDOW", hcell),
     Paragraph("HOLDING PERIOD", hcell), Paragraph("EV / TRADE", hcell)],
    [vcell("NO_GO", RED), vcell("NONE", RED), vcell("NONE", RED),
     vcell("-20% to -30%", RED)],
], colWidths=[CW / 4] * 4, rowHeights=[20, 26])
verdict_row.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(verdict_row)
story.append(Spacer(1, 90))
story.append(Paragraph(
    "Internal decision analysis prepared with AI research agents against publicly available data as at 29 September 2026. "
    "Not financial advice. All statistics carry named producible sources (Appendix B); figures are point-in-time and market conditions change.",
    ParagraphStyle("disc", fontName="Helvetica-Oblique", fontSize=8, leading=10.5,
                   textColor=TEXTMED, alignment=TA_CENTER)))
from reportlab.platypus import NextPageTemplate
story.insert(0, NextPageTemplate("title"))
story.append(NextPageTemplate("body"))
story.append(PageBreak())

# ---- table of contents
story.append(Paragraph("Contents", toc_h))
toc = TableOfContents()
toc.levelStyles = [
    ParagraphStyle("toc1", fontName="Helvetica-Bold", fontSize=10.5, leading=18,
                   textColor=NAVY, leftIndent=6),
]
story.append(toc)
story.append(PageBreak())


def section(num, title):
    story.append(TocHook(0, f"{num}   {title}"))
    story.append(sect_header(num, title))
    story.append(Spacer(1, 10))


# ================================================================ 1. executive
section("1", "Executive Summary & Verdict")
story.append(Paragraph(
    "<b>Verdict: NO_GO. There is no token-age entry window with defensible positive expectancy for a "
    "non-insider buyer of new memecoins in the late-2026 market, and the reviewed trading-desk ruleset is "
    "unviable as designed.</b>", lead))
story.append(Paragraph(
    "This review was commissioned to answer two questions: (a) what is the current state of the crypto and "
    "memecoin market, and (b) is there a logic to investing in new memecoins up to a certain number of days "
    "after launch — and if so, what entry window and holding timeframe is optimal. A 22-agent ETR workflow "
    "researched five independent lenses from current web sources, adversarially verified every load-bearing "
    "claim (11 CONFIRMED, 4 PARTLY-corrected, 0 REFUTED), then stress-tested the ruleset of the Grok-built "
    "\"The Floor\" desk app against the verified evidence.", body))
story.append(Paragraph("Three independent failure classes, each disqualifying on its own:", body))
story.append(Paragraph(
    "<b>1. No age window works.</b> The only systematically profitable entry is the creation block itself, "
    "captured by deployer-funded insider bots retail cannot replicate. Every later window is negative: "
    "minutes-old entries lose 10-28% by minute five at realistic latency; 80% of tokens are dead within one "
    "day; the \"least-bad\" 2-14-day survivor window still sees 61.5% mortality within a month and has no "
    "demonstrated positive net returns; buy-and-hold on mature memecoins returned -78.7% over 13 months.", bullet, bulletText="•"))
story.append(Paragraph(
    "<b>2. The exit math is broken.</b> The app's +10% take-profit against a -60% stop needs an 85.7% win "
    "rate before costs and 90-97% after verified round-trip costs of 3-8% — versus 33-73% ever observed in "
    "wallet studies. Expected value is roughly -20% to -30% per trade.", bullet, bulletText="•"))
story.append(Paragraph(
    "<b>3. The confirmation signals are adverse selection.</b> Whale inflow is substantially manufactured "
    "(98.7% of migrated tokens had a same-transaction dev buy; 21.4% of pre-migration transactions are wash "
    "trades) and visible KOL shilling predicts -70% within one week for 80% of promoted coins. The desk's "
    "WHALE + SHILL gate selects precisely the tokens engineered to dump on the buyer.", bullet, bulletText="•"))
story.append(Paragraph(
    "The app's NZ$500,000 target from a 10 SOL (~NZ$3-4k) book requires 130-165x compounding through "
    "negative per-trade expectancy: probability of reaching the target is effectively zero, while probability "
    "of full book loss is near certain. Standing actions: allocate no real capital to new-memecoin trading; "
    "never connect a wallet to the app (its control layer is self-contradictory on whether auto-buy is live, "
    "and \"Sign while I sleep\" delegated signing is a drain scenario); if kept at all, keep it paper-only "
    "and rebuilt per Section 7.", body))
story.append(Spacer(1, 4))

# ================================================================ 2. methodology
section("2", "Methodology & Evidence Integrity")
story.append(Paragraph(
    "The ETR (Execute Technical Review) agentic workflow ran 22 agents in three phases on 29 September 2026, "
    "making 216 tool calls against live web sources:", body))
story.append(data_table(
    ["Phase", "Agents", "Function"],
    [
        ["Research", "5", "Independent lenses: market state · token survival · entry-age returns · exit math &amp; costs · adversarial landscape"],
        ["Verify", "15", "One adversarial verifier per load-bearing claim, instructed to refute first via independent sources"],
        ["Assess", "2", "High-effort ruleset stress-test (rule-by-rule) and timeframe analysis (instructed: do not invent a window to be helpful)"],
    ], [90, 55, CW - 145]))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "Verification outcome: <b>11 claims CONFIRMED, 4 PARTLY (corrected in place — none changed the verdict), "
    "0 REFUTED.</b> The full ledger is at Appendix A; primary sources at Appendix B include an 832,941-launch "
    "academic survival study (arXiv), an 18.67M-token CoinGecko population study, Solidus Labs' rug-pull "
    "forensics, Chainalysis pump-and-dump analysis, Messari's State of Solana, 21Shares' H1-2026 report and "
    "Pine Analytics' sniper-wallet forensics.", body))

# ================================================================ 3. market state
section("3", "Market State — Late September 2026")
story.append(data_table(
    ["Metric", "Reading", "Context"],
    [
        ["Bitcoin", "~US$83k · 60% dominance", "-34% from Oct-25 ATH ($126k); 2026 spot-ETF flows net negative"],
        ["Solana (SOL)", "~US$122", "Jan $149 &rarr; Jun $60 &rarr; Sep rally on SEC tokenized-stock exemption (17 Sep)"],
        ["Memecoin sector mcap", "~US$31B", "-80% vs &gt;$150B late-2024 peak"],
        ["Memecoin share of Solana volume", "16%", "Was 40% in H1-2025"],
        ["Solana network revenue", "-87% YoY", "US$1.09B &rarr; $141M (H1); memecoin fee demand evaporated"],
        ["pump.fun 24h graduation rate", "~0.2% (May-Jun 26)", "Was 0.63% Sep-Oct 25 — 3.2x worse; brief ~2.7% window Aug-Sep 26"],
        ["Launch supply", "~2.8M tokens Q1-26; ~42k/day peak", "Record supply chasing far less capital"],
        ["Graduate exit valuations", "Rarely &gt; US$10M", "Was $30-100M in 2024-25 — payoff compression 5-10x"],
        ["Legal / structural", "RICO claims proceeding vs pump.fun operator (31 Aug 26)", "CLARITY Act stalled; Solana pivoting to stablecoins/RWAs"],
    ], [128, 128, CW - 256]))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "The one live pocket of activity — the tokenized-equity \"stonks\" wave (StonkFun on Solana, Pons on "
    "Robinhood Chain) — briefly out-earned pump.fun in early September and pushed Solana to 208M weekly "
    "trades. It is narrow, venue-fragmenting and partly off-Solana; it does not rehabilitate the base rates. "
    "Net read: expected value per launch is materially worse than the 2024-25 era this style of trading was "
    "designed in — roughly 3x lower graduation odds and 5-10x lower exit valuations.", body))

# ================================================================ 4. age curve
section("4", "The Entry-Age Analysis — Returns by Token Age")
story.append(Paragraph(
    "This is the core question of the review: is there an age window, in days, at which buying a new memecoin "
    "has positive expectancy? The verified evidence, window by window:", body))
story.append(data_table(
    ["Entry age", "Verified evidence", "Outcome for outside buyer"],
    [
        ["Block 0 (creation)",
         "Only profitable cohort: deployer-funded insider snipers — 87% win rate, 55% exit within 1 min, 85% within 5; pre-signed transactions, off-chain coordination",
         Paragraph('<font color="#C0392B"><b>Unreachable</b></font> — retail on a public frontend is the exit liquidity by construction', cell)],
        ["Minutes-hours",
         "Median -10.5% to -27.6% by 5 minutes post-signal (770-call study); insiders front-run public signals by ~100 seconds",
         Paragraph('<font color="#C0392B"><b>Negative</b></font>', cell)],
        ["0-2 days",
         "68.7% of 18.67M pump.fun tokens record their last trade on launch day; 80.4% within one day; median rug lifecycle ~15 minutes; 95.7% of rug transactions on day 1",
         Paragraph('<font color="#C0392B"><b>Death zone</b></font>', cell)],
        ["2-14 days (survivors)",
         "Surviving to day 2 lifts 90-day survival ~5x (4.55% &rarr; 23.2%) and outlives the hard-rug window — but 61.5% of 2-day survivors die within a month; 93% of 388k Raydium pools eventually lose &ge;90% liquidity (soft rug)",
         Paragraph('<font color="#E67E22"><b>Least-bad</b></font> — no study shows positive net buyer returns; a heuristic, not an edge', cell)],
        ["Post-graduation",
         "60% of 41,470 graduates collapse below 20% of migration price almost immediately; 84% classified high-risk; 36.5% of supply in bundled wallets",
         Paragraph('<font color="#C0392B"><b>Negative</b></font>', cell)],
        ["Weeks-months (hold)",
         "Top-10 CEX-listed memecoins returned -78.7% Jan-25 to Feb-26 (BTC -30.7%); 82.7% max drawdown",
         Paragraph('<font color="#C0392B"><b>Strongly negative</b></font>', cell)],
    ], [88, CW - 88 - 140, 140]))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "<b>Conclusion — the answer to \"up to how many days\": there is no day count at which the hazard drops to "
    "an acceptable level.</b> The death rate declines smoothly with age and stays elevated for months; the "
    "dominant kill mechanism merely shifts from fast hard-rugs (day 0-1) to abandonment and soft-rug liquidity "
    "decay (day 2+). A 2-day minimum age is a real but partial de-risking filter — necessary if trading at all, "
    "nowhere near sufficient to produce positive expectancy. Recommended entry window: <b>NONE</b>.", body))

# ================================================================ 5. exit math
section("5", "The Exit Math — Costs, Win Rates, Expectancy")
story.append(data_table(
    ["Round-trip cost", "Break-even win rate (+10% TP / -60% SL)"],
    [
        ["0% (theoretical)", "85.7%   (p* = 0.60 / 0.70)"],
        ["3%", "90.0%"],
        ["5% (typical 0.5-2 SOL clip)", "92.9%   ·   net reward:risk &asymp; 0.08 : 1"],
        ["8% (fresh, low-liquidity token)", "97.1%"],
    ], [190, CW - 190]))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "Verified cost components: pump.fun bonding-curve fee 1.25%/side; Jupiter Ultra 10 bps/side (50 bps on "
    "tokens under 24h old); priority + Jito fees ~0.002-0.01 SOL per transaction (charged even on failed "
    "sends); realized slippage 1-3%/side on low-liquidity pairs; plus MEV. Against the required 90-97% win "
    "rate, observed reality: only <b>33.4%</b> of 771,939 pump.fun wallets were net-profitable (average "
    "profit 3.8%); the best month ever recorded was <b>73.3%</b> (April 2026 — realized-PnL-only, "
    "bot-contaminated, on a shrunken 1.8M-wallet base, ~89% of winners making US$1-500); only <b>0.41%</b> "
    "of 13.55M wallets ever realized more than US$10k. At a generous 50% win rate, expected value is "
    "approximately <b>-30% per trade</b>.", body))
story.append(Paragraph(
    "The -60% stop cannot be relied on to fill: Solana DEXs have no native guaranteed stops, and with 98.6% "
    "of launches showing rug/pump-and-dump characteristics, losses gap through the stop toward -90/-100%. "
    "Every documented profitable playbook uses the inverse structure — cut losers at -20/-30%, sell half at "
    "+100% to take out initials, ladder or trail the remainder — i.e. reward:risk well above 1, never a "
    "capped-winner/wide-stop regime.", body))

# ================================================================ 6. adversarial
section("6", "The Adversarial Landscape — Who Is on the Other Side")
story.append(data_table(
    ["Signal the desk trusts", "What the data shows", "Correct treatment"],
    [
        ["Whale inflow (WHALE seat)",
         "98.7% of 41,470 migrated tokens included a same-transaction dev buy; 36.5% of supply in bundled wallets; 21.4% of pre-migration transactions are wash trades; a documented single-funder op ran 200 bots faking US$532k volume in 12h to trigger trackers; ~94% of pump-and-dump pools rugged by their own creator",
         Paragraph('<font color="#C0392B"><b>VETO signal</b></font> — concentrated inflow = the operator', cell)],
        ["Visible shilling (SHILL seat)",
         "Across 1,567 promoted coins / 377 KOLs: 80% lost ~70% within ONE WEEK of promotion; 86% down 90%+ at 3 months; big accounts (200k+) worst at -89%; ~3% ever 10x; influencers paid ~US$399/tweet regardless of outcome",
         Paragraph('<font color="#C0392B"><b>VETO signal</b></font> — marks the exit-distribution phase', cell)],
        ["Mint/freeze authority check (RISK seat)",
         "Of 76,469 verified rugs (H1-2025): 78.9% insider-supply dumps, 20.4% LP withdrawals, only 0.6% freeze-authority abuse — 99.4% pass the check; Token-2022 permanent-delegate / transfer-hook honeypots pass with both authorities revoked",
         Paragraph('<font color="#E67E22"><b>Insufficient</b></font> — add holder-concentration, LP-lock, deployer-history, Token-2022 scans', cell)],
    ], [95, CW - 95 - 135, 135]))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "The combination the desk requires before buying — whale inflow plus visible shilling, gated only by a "
    "mint/freeze check — is the designed victim profile of the dominant extraction playbook: bundle supply at "
    "launch, wash-trade to trigger trending feeds and whale trackers, pay KOLs to broadcast, dump within "
    "minutes to hours.", body))

# ================================================================ 7. ruleset
section("7", 'Ruleset Stress-Test — "The Floor" Desk App')
story.append(data_table(
    ["Rule", "Verdict", "Finding"],
    [
        ['Universe "fresh SOL pairs" vs entry "2 days or older"', vcell("CONTRADICTORY", RED),
         "The sourcing layer feeds only tokens the entry rule must reject. Fix: universe = 2-14-day survivors from survivor/graduation feeds; delete \"fresh\"."],
        ["2-day minimum age gate", vcell("FLAWED", AMBER),
         "Best rule on the desk — outlives the hard-rug window, ~5x survival lift — but necessary-not-sufficient (61.5% of survivors still die in a month)."],
        ["WHALE seat: whale inflow confirms entry", vcell("FATAL", RED),
         "Whale flow is substantially manufactured (Section 6). Fix: invert to a veto on bundled supply / wash-trade / deployer-funding detection."],
        ["SHILL seat: visible promotion required", vcell("FATAL", RED),
         "KOL promotion predicts -70% in one week for 80% of coins. Fix: invert — large-account promotion in the last 7 days = do-not-buy."],
        ["Mint/freeze checks, fail-closed", vcell("FLAWED", AMBER),
         "Fail-closed is correct; the check catches 0.6% of rugs. Fix: add holder concentration (&gt;30-40% reject), LP lock/burn, deployer history, Token-2022 extension scan."],
        ['Manual APPROVE vs "Auto buy is on"', vcell("CONTRADICTORY", RED),
         "The control layer contradicts itself — if auto-buy is live the approval gate is decorative. Fix: manual approve for entries, one stated mode, alarms on unapproved routing."],
        ['"Sell a 3x" vs "+10% take-profit" + moon bag', vcell("CONTRADICTORY", RED),
         "+10% always fires first, so the 3x rule and moon bag are dead code. Fix: delete +10%; sell 50% at +100%, ladder/trail the rest."],
        ["+10% TP / -60% SL exit regime", vcell("FATAL", RED),
         "Needs 90-97% win rate after costs vs 33-73% ever observed (Section 5). Not patchable by tuning — the structure must invert."],
        ["0.015 SOL sell-gas reserve", vcell("FLAWED", AMBER),
         "Right instinct, ~3x undersized for a rug exit (fees charged on failed sends). Fix: 0.05 SOL global + ~0.02 SOL per open position; breach = trading halt."],
    ], [130, 78, CW - 208]))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "<b>Overall: UNVIABLE AS DESIGNED — three FATAL, three CONTRADICTORY, three FLAWED. Fixable only by "
    "rebuild, and even a rebuilt version has no demonstrated retail edge in this market.</b> The app also "
    "presents live-execution plumbing (Connect Trust Wallet, \"Sign while I sleep\" delegated signing, gas "
    "reserves) on a nominally paper-only book; given the self-contradictory control layer, connecting a "
    "funded wallet — even a \"separate desk key\" — is a drain scenario and must not happen.", body))

# ================================================================ 8. recommendation
section("8", "Recommendation & Conditions to Revisit")
story.append(Paragraph("<b>Strict recommendations:</b>", body))
for i, r in enumerate([
    "<b>Allocate no real capital to new-memecoin trading — at any token age, in this regime.</b> This is structural, not timing: the only profitable window is insider infrastructure, and every public window is negative-EV after costs.",
    "<b>Never connect a wallet to the app.</b> No Trust Wallet connection, no \"Sign while I sleep\" delegated key, funded or not.",
    "<b>If kept as a paper toy, rebuild it:</b> universe = 2-14-day survivors; WHALE/SHILL inverted to vetoes; add the checks that catch the real 99.4% of rugs (holder concentration, LP lock/burn, deployer history, Token-2022 hooks); exits = sell 50% at +100%, ladder/trail remainder, hard stop -25%; delete the +10% TP; reset the profit target to something the book can arithmetically support.",
    "<b>If the aim is crypto exposure at all,</b> BTC/SOL beta is a separate question — but it strictly dominates memecoin speculation on every verified number in this review. Capital currently has better-diligenced homes in the live deal pipeline (1st Call, Focus Digital, property).",
], 1):
    story.append(Paragraph(r, bullet, bulletText=f"{i}."))
story.append(Spacer(1, 6))
story.append(Paragraph("<b>All six of these would need to become true before this verdict is revisited:</b>", body))
for c in [
    "A verified out-of-sample track record (not a backtest) showing a specific entry-age/exit rule with net-of-cost positive expectancy in the post-2025 regime.",
    "Round-trip execution cost compressed below ~1.5% (current reality 3-6%, up to 8-10% on tokens under 24h).",
    "An exit structure with reward:risk well above 1 (laddered scaling) — never a capped-winner/wide-stop structure.",
    "Memecoin sector capital recovery (sector mcap and graduate exit valuations back toward 2024-25 levels).",
    "Resolution of the pump.fun RICO exposure and CLARITY Act status if the strategy depends on that venue.",
    "Hard risk caps regardless: &le;0.5-1% of speculative capital per position; speculative capital itself a small single-digit % of investable assets; acceptance that stops do not gap-protect (rugs realize -90 to -100%).",
]:
    story.append(Paragraph(c, bullet, bulletText="•"))

# ================================================================ appendix A
story.append(PageBreak())
section("Appendix A", "Adversarial Verification Ledger")
story.append(Paragraph(
    "Each load-bearing claim was independently re-researched by a verifier instructed to refute it first. "
    "PARTLY = directionally right, figure corrected in place (corrections applied throughout this document).", small_it))
story.append(data_table(
    ["Lens", "Claim (abridged)", "Verdict"],
    [
        ["Market", "Late-2026 regime is bear/risk-off: BTC ~$83k (-34% from ATH), 60% dominance, ETF flows net negative", vcell("CONFIRMED", GREEN)],
        ["Market", "Memecoin sector structurally collapsed: ~$31B mcap (-80%), Solana volume share 40% &rarr; 16%, network revenue -87%", vcell("CONFIRMED", GREEN)],
        ["Market", "Per-launch odds deteriorated: record supply, graduation 0.63% &rarr; ~0.2%, graduate valuations compressed", vcell("PARTLY", AMBER)],
        ["Survival", "68.7% of pump.fun tokens last trade on launch day; 80.4% within one day (18.67M-token population)", vcell("CONFIRMED", GREEN)],
        ["Survival", "Rugs execute in the first hours: median lifecycle ~15 min; 95.7% of rug transactions on creation day", vcell("CONFIRMED", GREEN)],
        ["Survival", "2-day age filter lifts survival ~5x (4.55% &rarr; 23.2% at 90d) but 61.5% still die within a month", vcell("CONFIRMED", GREEN)],
        ["Age-entry", "Block-0 is the only profitable window and is insider-captured (corrected: ~1.7% coordinated insider snipes; most same-block sniping is unprofitable wide-net bots)", vcell("PARTLY", AMBER)],
        ["Age-entry", "Minutes-after-launch entries have zero-to-negative median returns at realistic latency; insiders front-run by ~100s", vcell("CONFIRMED", GREEN)],
        ["Age-entry", "Hours-to-2-day entries are a near-lottery on the survival curve", vcell("CONFIRMED", GREEN)],
        ["Exit-math", "Round-trip cost ~3-6% (8-10% fresh): pump.fun 1.25%/side + Jupiter + priority/Jito + slippage", vcell("CONFIRMED", GREEN)],
        ["Exit-math", "Most wallets lose: 33.4% profitable (771,939 wallets); best month ever 73.3% (corrected: $1-500 winners = 65.1% of ALL active wallets, ~89% of winners)", vcell("PARTLY", AMBER)],
        ["Exit-math", "+10%/-60% needs 85.7% win rate pre-cost, 90-97% after — unreachable vs observed performance", vcell("CONFIRMED", GREEN)],
        ["Adversarial", "Deployer-linked wallets control large launch supply: 98.7% same-tx dev buys; 36.5% bundled supply", vcell("CONFIRMED", GREEN)],
        ["Adversarial", "Whale inflow largely manufactured (corrected wording: substantially contaminated — 21.4% wash trades, documented bot-fleet fakes)", vcell("PARTLY", AMBER)],
        ["Adversarial", "KOL shilling predicts negative forward returns: 80% of promoted coins -70% within a week", vcell("CONFIRMED", GREEN)],
    ], [62, CW - 62 - 82, 82]))

# ================================================================ appendix B
story.append(Spacer(1, 14))
section("Appendix B", "Primary Sources")
for s in [
    "arXiv 2607.02823 — 832,941-launch pump.fun survival analysis (May-Jun 2026 window; graduation 0.198% pooled)",
    "CoinGecko — 18.67M-token pump.fun population study (Jan 2024-Jun 2026 last-trade/survival distributions)",
    "Solidus Labs, 2025 Rug Pull Report — 98.6% of launches with rug/P&amp;D traits; 93% of 388k Raydium pools soft-rugged",
    "Chainalysis — ~94% of suspected pump-and-dump pools rugged by their own creator",
    "Academic H1-2025 rug-typology study — 100,063 new tokens / 76,469 rugs: 78.9% insider dumps, 20.4% LP pulls, 0.6% freeze",
    "Migrated-token study — 41,470 pump.fun graduates: 98.7% same-tx dev buys, 36.5% bundled supply, 60% immediate collapse",
    "Pine Analytics — deployer-funded sniper-wallet forensics (87% win rate, sub-5-minute exits)",
    "KOL study — 377 influencers / 1,567 promoted memecoins: 80% down ~70% in one week; corroborated by peer-reviewed -19%/3mo",
    "CoinWire/Dune — 771,939-wallet PnL study (33.4% profitable); 13.55M-wallet realized-profit distribution (0.41% &gt; $10k)",
    "Messari State of Solana Q1 2026; 21Shares H1 2026 report; CoinGecko launchpad-wars analysis (8 Sep 2026); Yahoo Finance / Coinbase market data (28 Sep 2026)",
]:
    story.append(Paragraph(s, bullet, bulletText="•"))

# ---------------------------------------------------------------- build
doc = ETRDoc(OUT)
doc.multiBuild(story)
print(f"OK {OUT}")
