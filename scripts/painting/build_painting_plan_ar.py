#!/usr/bin/env python3
"""
Auckland Painting Co — Business Plan (ARABIC / RTL edition).
Outputs: ~/Desktop/Painting/Auckland_Painting_Co_Business_Plan_AR.pdf
Same ETR-hardened numbers as the English plan; Modern Standard Arabic, right-to-left.
Rendering: arabic_reshaper + python-bidi + Arial Unicode (Arabic+Latin+digits), custom
per-line RTL flowable so wrapped lines keep correct bidi order.
"""
import os
import arabic_reshaper
try:
    from bidi.algorithm import get_display
except Exception:
    from bidi import get_display
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Spacer, Table,
                                TableStyle, PageBreak, NextPageTemplate, Flowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Line, Rect, String
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.widgets.markers import makeMarker

# ---- fonts (Arial Unicode covers Arabic + Latin + digits) ----
AR_PATH = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
pdfmetrics.registerFont(TTFont("ARU", AR_PATH))
FONT = "ARU"

import re
_CTRL = re.compile("[‎‏‪-‮⁦-⁩]")  # LRM/RLM/embeds/isolates
def ar(t):
    return get_display(arabic_reshaper.reshape(_CTRL.sub("", str(t))))

# ---- palette ----
NAVY = colors.HexColor("#1E2A3A"); GOLD = colors.HexColor("#C8952A")
GOLDD = colors.HexColor("#A87A1E"); GREEN = colors.HexColor("#00843D")
INK = colors.HexColor("#22262B"); GREY = colors.HexColor("#5A6472")
LINEG = colors.HexColor("#D8DCE2"); ROWALT = colors.HexColor("#F4F6F8")
LIGHT = colors.HexColor("#EEF1F4"); RED = colors.HexColor("#B23A2E"); WHITE = colors.white

OUT_DIR = os.path.expanduser("~/Desktop/Painting")
os.makedirs(OUT_DIR, exist_ok=True)
PDF = os.path.join(OUT_DIR, "Auckland_Painting_Co_Business_Plan_AR.pdf")

def nz(x):
    x = round(x)
    return ("-${:,.0f}".format(-x)) if x < 0 else ("${:,.0f}".format(x))

# ================================================================ FINANCIAL ENGINE (identical to EN)
REV = {"Y1": 235000, "Y2": 430000, "Y3": 620000}
REV_RANGE = {"Y1_low": 200000, "Y1_high": 285000}
GM = {"Y1": 0.30, "Y2": 0.39, "Y3": 0.43}
FIXED_OPEX = {"Y1": 54240, "Y2": 72000, "Y3": 95000}
PROV_PC = 0.045
DRAWS = {"Y1": 69000, "Y2": 90000, "Y3": 140000}
LOAN = 150000; EQUITY = 50000; CAPITAL = EQUITY + LOAN
CHARGE_OUT = 95; SUBBIE_HR = 55; EMPLOYED_HR = 38; MATERIALS_PC = 0.19
AVG_RES_JOB = 11000; AVG_COMM_JOB = 6000

def pnl(y):
    rev = REV[y]; cogs = rev * (1 - GM[y]); gp = rev - cogs
    prov = rev * PROV_PC; ebd = gp - FIXED_OPEX[y] - prov
    return dict(rev=rev, cogs=cogs, gp=gp, gm=GM[y], fixed=FIXED_OPEX[y], prov=prov,
                ebitda_bd=ebd, draws=DRAWS[y], after=ebd - DRAWS[y])
PL = {y: pnl(y) for y in ("Y1", "Y2", "Y3")}

USE_OF_FUNDS = [
    ("عربة عمل — دفعة إيجار/تمويل + تجهيز (بدلاً من شراء نقدي بـ‎$28,000‎)", 5000),
    ("معدات رش وسلالم ومنصات وأدوات تحضير وصنفرة ومكنسة HEPA + كمامات P2", 12000),
    ("معدات وصول (سقالة صغيرة/درجات؛ تأجير سقالات الطابقين)", 3000),
    ("علامة تجارية وموقع + SEO ولافتات العربة والزي وملف Google Business", 7000),
    ("تأمين — دفعة/كفالة أولية (ثم يُدفع شهرياً)", 1500),
    ("تسجيل الشركة/الضريبة/GST وSiteWise واعتماد Dulux/Resene", 3000),
    ("قانوني — اتفاق المساهمين والنظام وسند قرض المساهم/PPSR وتنازل الملكية الفكرية والاستحقاق والقيود", 7000),
    ("رأس مال عامل / احتياطي طوارئ (مواد نقداً في الأشهر 1–3)", 25000),
]
SETUP_TOTAL = sum(a for _, a in USE_OF_FUNDS)
RESERVE = CAPITAL - SETUP_TOTAL

MONTHS = list(range(1, 13))
REV_VEC = [v * 1000 for v in [6, 8, 10, 14, 20, 22, 24, 26, 28, 30, 22, 25]]

def y1_cashflow():
    opening = CAPITAL - SETUP_TOTAL; bal = opening; rows = []; prev = 0; gst = 0.0
    for i, rev in enumerate(REV_VEC):
        collect = rev * 0.63 + prev * 0.35
        mat_paid = rev * MATERIALS_PC if i < 3 else REV_VEC[i-1] * MATERIALS_PC
        labour = rev * (0.70 - MATERIALS_PC)
        fixed = FIXED_OPEX["Y1"] / 12.0
        draws = 4500 + (2500 if i < 6 else 0)
        rework = (REV_VEC[i-1] * 0.03) if i >= 1 else 0.0
        gst += collect * 0.045; gst_paid = 0.0
        if (i + 1) % 2 == 0:
            gst_paid = gst; gst = 0.0
        net = collect - mat_paid - labour - fixed - draws - rework - gst_paid
        bal += net; rows.append(bal); prev = rev
    return opening, rows
OPENING, CF_BAL = y1_cashflow()
MIN_BAL = min(CF_BAL); PEAK_NEED = CAPITAL - MIN_BAL; HEADROOM = 200000 - PEAK_NEED
STRESS_PEAK = 195000

# ================================================================ RTL FLOWABLES
class ArText(Flowable):
    """Right-to-left paragraph: wraps in logical order, applies bidi per visual line."""
    def __init__(self, text, size=10, leading=14.5, color=INK, space_after=7,
                 bullet=False, indent=0, gap_before=0):
        super().__init__()
        self.text = text; self.size = size; self.leading = leading; self.color = color
        self.space_after = space_after; self.bullet = bullet; self.indent = indent
        self.gap_before = gap_before; self.lines = []
    def wrap(self, availW, availH):
        self.width = availW
        usable = availW - self.indent - (14 if self.bullet else 0)
        words = self.text.split(" "); lines = []; cur = []
        for w in words:
            trial = " ".join(cur + [w])
            if pdfmetrics.stringWidth(ar(trial), FONT, self.size) <= usable or not cur:
                cur.append(w)
            else:
                lines.append(" ".join(cur)); cur = [w]
        if cur:
            lines.append(" ".join(cur))
        self.lines = lines or [""]
        self.height = self.gap_before + len(self.lines) * self.leading + self.space_after
        return (availW, self.height)
    def draw(self):
        c = self.canv; c.setFont(FONT, self.size); c.setFillColor(self.color)
        right = self.width - self.indent
        y = self.height - self.space_after - self.size - self.gap_before + (self.leading - self.size)
        if self.bullet:
            c.setFillColor(GOLD)
            c.rect(right - 7, y + 1.2, 4.2, 4.2, fill=1, stroke=0)
            c.setFillColor(self.color)
            right -= 14
        for ln in self.lines:
            c.setFont(FONT, self.size); c.setFillColor(self.color)
            c.drawRightString(right, y, ar(ln)); y -= self.leading

def H1(t):
    return ArText(t, size=15.5, leading=19, color=NAVY, space_after=4, gap_before=4)
def H2(t):
    return ArText(t, size=11.5, leading=15, color=GOLDD, space_after=3, gap_before=8)
def LEAD(t):
    return ArText(t, size=10.5, leading=14.5, color=NAVY, space_after=3)
def B(t):
    return ArText(t, size=10, leading=14.5, color=INK, space_after=7)
def LI(t):
    return ArText(t, size=9.5, leading=13.5, color=INK, space_after=3.5, bullet=True)
def SMALL(t):
    return ArText(t, size=8, leading=11, color=GREY, space_after=5)

class HRule(Flowable):
    def __init__(self, w, color=GOLD, thick=1.4):
        super().__init__(); self.w = w; self.color = color; self.thick = thick
    def wrap(self, aw, ah): return (self.w, self.thick + 3)
    def draw(self):
        self.canv.setStrokeColor(self.color); self.canv.setLineWidth(self.thick)
        self.canv.line(0, 2, self.w, 2)

def ar_table(headers, rows, widths, hi_rows=None):
    """Logical columns [c0, c1, ...] with c0 the row label; displayed RTL (label on right)."""
    hi_rows = hi_rows or []
    def cell(txt, color, size=8.5):
        return ArText(str(txt), size=size, leading=11.5, color=color, space_after=0)
    data = []
    data.append([cell(h, WHITE) for h in reversed(headers)])
    for r in rows:
        data.append([cell(v, INK) for v in reversed(list(r))])
    t = Table(data, colWidths=list(reversed(widths)), repeatRows=1)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 1), (-1, -1), 0.35, LINEG),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            cmds.append(("BACKGROUND", (0, i), (-1, i), ROWALT))
    for hr in hi_rows:
        cmds.append(("BACKGROUND", (0, hr), (-1, hr), LIGHT))
        cmds.append(("LINEABOVE", (0, hr), (-1, hr), 0.6, NAVY))
    t.setStyle(TableStyle(cmds))
    return t

def kv(pairs, w1=150, w2=337):
    # key on the right, value on the left (RTL): logical [key, val] -> display [val, key]
    data = [[ArText(v, size=9, leading=12.5, color=INK, space_after=0),
             ArText(k, size=9.5, leading=12.5, color=NAVY, space_after=0)] for k, v in pairs]
    t = Table(data, colWidths=[w2, w1])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, LINEG),
    ]))
    return t

# ---- charts (Arabic titles) ----
def revenue_chart(width=470, height=175):
    d = Drawing(width, height)
    bc = VerticalBarChart(); bc.x = 40; bc.y = 28; bc.width = width - 90; bc.height = height - 58
    bc.data = [[PL[y]["rev"] for y in ("Y1", "Y2", "Y3")],
               [PL[y]["ebitda_bd"] for y in ("Y1", "Y2", "Y3")]]
    bc.categoryAxis.categoryNames = [ar("السنة 1"), ar("السنة 2"), ar("السنة 3")]
    bc.bars[0].fillColor = NAVY; bc.bars[1].fillColor = GOLD
    bc.valueAxis.valueMin = 0; bc.valueAxis.valueMax = 650000; bc.valueAxis.valueStep = 130000
    bc.valueAxis.labelTextFormat = lambda v: "$%dk" % (v / 1000)
    bc.valueAxis.labels.fontName = FONT; bc.valueAxis.labels.fontSize = 7.5
    bc.categoryAxis.labels.fontName = FONT; bc.categoryAxis.labels.fontSize = 8.5
    bc.barWidth = 9; bc.groupSpacing = 22; bc.barSpacing = 2
    d.add(bc)
    d.add(String(width - 40, height - 12, ar("الإيرادات مقابل EBITDA (قبل مسحوبات الملاك)"),
                 fontName=FONT, fontSize=8.5, fillColor=NAVY, textAnchor="end"))
    d.add(Rect(40, height - 14, 8, 8, fillColor=NAVY, strokeColor=None))
    d.add(String(52, height - 12, ar("الإيرادات"), fontName=FONT, fontSize=7.5, fillColor=INK))
    d.add(Rect(120, height - 14, 8, 8, fillColor=GOLD, strokeColor=None))
    d.add(String(132, height - 12, ar("EBITDA"), fontName=FONT, fontSize=7.5, fillColor=INK))
    return d

def cashflow_chart(width=470, height=190):
    d = Drawing(width, height)
    lp = LinePlot(); lp.x = 42; lp.y = 30; lp.width = width - 90; lp.height = height - 60
    lp.data = [[(i + 1, CF_BAL[i]) for i in range(12)]]
    lp.lines[0].strokeColor = NAVY; lp.lines[0].strokeWidth = 2
    lp.lines[0].symbol = makeMarker("FilledCircle"); lp.lines[0].symbol.size = 3
    lp.lines[0].symbol.fillColor = GOLD
    lp.xValueAxis.valueMin = 1; lp.xValueAxis.valueMax = 12; lp.xValueAxis.valueStep = 1
    lp.xValueAxis.labels.fontName = FONT; lp.xValueAxis.labels.fontSize = 7
    lp.yValueAxis.valueMin = 0; lp.yValueAxis.valueMax = 160000; lp.yValueAxis.valueStep = 40000
    lp.yValueAxis.labelTextFormat = lambda v: "$%dk" % (v / 1000)
    lp.yValueAxis.labels.fontName = FONT; lp.yValueAxis.labels.fontSize = 7.5
    d.add(lp)
    ymin = 30 + (MIN_BAL / 160000.0) * (height - 60)
    d.add(Line(42, ymin, width - 48, ymin, strokeColor=RED, strokeWidth=0.8, strokeDashArray=[3, 2]))
    d.add(String(width - 48, ymin + 3, ar("أدنى رصيد %s (السحب الأقصى من الـ‎$200k‎ = %s)" % (nz(MIN_BAL), nz(PEAK_NEED))),
                 fontName=FONT, fontSize=7.5, fillColor=RED, textAnchor="end"))
    d.add(String(width - 42, height - 12, ar("رصيد النقد الشهري في السنة الأولى (الحالة الأساسية) — من رأسمال ‎$200k‎"),
                 fontName=FONT, fontSize=8.5, fillColor=NAVY, textAnchor="end"))
    return d

# ================================================================ DOC
class Doc(BaseDocTemplate):
    def __init__(self, fn, **kw):
        super().__init__(fn, **kw)
        fw, fh = A4; L = R = 54; T = 62; Bm = 52
        self.addPageTemplates([
            PageTemplate(id="Cover", frames=[Frame(0, 0, fw, fh, id="c")], onPage=self._cover),
            PageTemplate(id="Main", frames=[Frame(L, Bm, fw - L - R, fh - T - Bm, id="m")], onPage=self._chrome),
        ])
    def _cover(self, c, d):
        fw, fh = A4
        c.setFillColor(NAVY); c.rect(0, 0, fw, fh, fill=1, stroke=0)
        c.setFillColor(GOLD); c.rect(0, fh - 6, fw, 6, fill=1, stroke=0)
        c.setStrokeColor(GOLD); c.setLineWidth(1); c.line(54, fh * 0.60, fw - 54, fh * 0.60)
    def _chrome(self, c, d):
        fw, fh = A4
        c.setStrokeColor(LINEG); c.setLineWidth(0.6); c.line(54, fh - 46, fw - 54, fh - 46)
        c.setFont(FONT, 7.5); c.setFillColor(GREY)
        c.drawRightString(fw - 54, fh - 42, ar("شركة دهانات أوكلاند — خطة العمل والنموذج المالي"))
        c.drawString(54, fh - 42, ar("سرّي"))
        c.setStrokeColor(LINEG); c.line(54, 40, fw - 54, 40)
        c.drawRightString(fw - 54, 30, ar("أُعدّت في 27 يوليو 2026 — مُحصّنة بمراجعة ETR (موافقة مشروطة)"))
        c.drawString(54, 30, ar("صفحة %d" % d.page))

story = []
FW = A4[0] - 108  # usable width 487

# COVER
story += [Spacer(1, 150)]
story.append(ArText(ar_kw := "خطة العمل والنموذج المالي", size=11, leading=16, color=GOLD, space_after=14) if False else ArText("خطة العمل والنموذج المالي", size=11, leading=16, color=GOLD, space_after=14))
def cvcenter(t, size, color, sa=10, lead=None):
    f = ArText(t, size=size, leading=lead or size + 5, color=color, space_after=sa)
    f._center = True
    return f
# center helper: override draw by using a centered ArText subclass
class ArCenter(ArText):
    def draw(self):
        c = self.canv; y = self.height - self.space_after - self.size + (self.leading - self.size)
        for ln in self.lines:
            c.setFont(FONT, self.size); c.setFillColor(self.color)
            c.drawCentredString(self.width / 2.0, y, ar(ln)); y -= self.leading
story = [Spacer(1, 150)]
story.append(ArCenter("خطة العمل والنموذج المالي", size=12, leading=17, color=GOLD, space_after=16))
story.append(ArCenter("شركة دهانات سكنية وتجارية خفيفة في أوكلاند", size=23, leading=30, color=WHITE, space_after=8))
story.append(ArCenter("الاسم المبدئي: Weatherline Painters (العلامة قيد التحديد)", size=12, leading=16, color=colors.HexColor("#C9D2DC"), space_after=40))
story += [Spacer(1, 120)]
story.append(ArCenter("مشروع مناصفة 50/50 — الشريك الأول يدير العمل ويموّله، وابن عمّه، وهو دهّان مؤهّل، يدير العمليات.", size=11, leading=16, color=colors.HexColor("#C9D2DC"), space_after=8))
story.append(ArCenter("أوكلاند، نيوزيلندا • الإطلاق 2026 • رأس مال ‎$200,000‎ • أُعدّت في 27 يوليو 2026", size=9.5, leading=14, color=GOLD, space_after=0))
story.append(NextPageTemplate("Main")); story.append(PageBreak())

def sec(title):
    story.append(H1(title)); story.append(HRule(FW)); story.append(Spacer(1, 5))

# 1. EXEC SUMMARY
sec("1.  الملخص التنفيذي")
story.append(LEAD("القرار: موافقة مشروطة (Conditional Go)"))
story.append(B("مشروع دهانات قابل للتطبيق في أوكلاند بحاجز دخول منخفض، ويبقى ضمن سقف النقد البالغ ‎$200,000‎ فقط إذا: (1) سُعّرت العمالة بمبدأ التكلفة‑زائد، (2) أُعيدت هيكلة الـ‎$200,000‎ إلى حقوق ملكية + قرض مساهم مضمون، (3) مُوّل خطر الشخص المحوري (الشريك ب)، و(4) التزم المشروع بمسار سوقي واحد. أمّا كمشروع مناصفة ساذج يسعّر بالتكلفة ويقبل كل شيء، فإنه يفشل في الهامش والعدالة وخطر الشخص المحوري — وهو ما التقطته المراجعة الخصمية بالضبط وتُصلحه هذه الخطة."))
story.append(B("يدخل المشروع سوقاً كبيراً ومجزّأً — نحو ‎$1.9–2.0‎ مليار وطنياً عبر ~5,832 شركة صغيرة الحجم، دون لاعب سكني مهيمن، ودون اشتراط رخصة مهنية (الدهان ليس عملاً إنشائياً مقيّداً). هذا يفضّل بنيوياً شركة مستقلة صغيرة ومُدارة جيداً وموثّقة الاعتمادات. لكن حقيقتين تحكمان النموذج: السوق في تباطؤ دوري متأخر (انكماش ‎-7.0%‎ في 2024 و‎-3.2%‎ في 2025)، فلا نعتمد على حجم أعمال البناء الجديد؛ والطلب موسمي بقوة، إذ تتركّز الأعمال الخارجية بين نوفمبر وأبريل وتنهار في شتاء يونيو–أغسطس."))
story.append(H2("ما الذي غيّرته المراجعة الخصمية"))
story.append(B("فشلت الخطة قبل المراجعة في أربعة اختبارات صارمة، وقد صُحّح كلٌّ منها:"))
story.append(LI("الهامش: تسعير ساعة المقاول الباطن بـ‎$65‎ — داخل نطاق تكلفته ‎$45–75‎ — يعطي هامشاً إجمالياً ~12% لا 45%. أُعيد التسعير بمبدأ التكلفة‑زائد: ادفع ‎$55‎ وحاسب العميل ‎$95‎/ساعة، وهامش إجمالي واقعي 30% في السنة الأولى (يرتفع إلى ~43% في السنة الثالثة)."))
story.append(LI("عدالة رأس المال: تمويل الشريك أ لكامل الـ‎$200,000‎ مقابل 50% ملكية عادية يمنح الشريك ب ~‎$100,000‎ في اليوم الأول. الحل: ~‎$50,000‎ حقوق ملكية (50/50) + ~‎$150,000‎ قرض مساهم مضمون ومسجّل على PPSR، يُسدَّد قبل أي أرباح موزّعة."))
story.append(LI("خطر الشخص المحوري: الشريك ب هو الدهّان المؤهّل الوحيد ومقدّر العروض والمراقب الوحيد للجودة والوحيد المؤهّل للسلامة. يُخفَّف بتأمين شخص محوري/عجز/مرض، ومقاول باطن مرتبط بعقد أولوية، واستحقاق عكسي وقيود، وتقديم توظيف دهّان مؤهّل مبكّراً كاحتياطي استمرارية وجودة."))
story.append(LI("التموضع: نهج «مختلط/انتهازي» عبر أربعة أنواع مشترين يشتّت طاقة الشريك ب النادرة ويوقف دولاب الإحالات. الحل: توجيه 100% من التسويق نحو مسار واحد — إعادة دهان الواجهات الخشبية السكنية الفاخرة — مع إبقاء استقبال الأعمال انتهازياً."))
story.append(H2("الأرقام بعد التحصين"))
story.append(kv([
    ("إيراد السنة الأولى", "%s أساسي (%s حد أدنى / %s حد أعلى) — مقيّد بطاقة الإشراف، مع إطلاق في الشتاء" % (nz(REV["Y1"]), nz(REV_RANGE["Y1_low"]), nz(REV_RANGE["Y1_high"]))),
    ("مسار الإيراد ثلاث سنوات", "%s ← %s ← %s (أساسي)" % (nz(REV["Y1"]), nz(REV["Y2"]), nz(REV["Y3"]))),
    ("الهامش الإجمالي", "30% (س1، مُحمّل بالكامل) ← 39% (س2) ← 43% (س3)"),
    ("نتيجة السنة الأولى", "قرب التعادل قبل مسحوبات الملاك (%s)؛ سنة استثمار متعمّدة بنحو %s بعد مسحوبات متواضعة ومرحلية" % (nz(PL["Y1"]["ebitda_bd"]), nz(PL["Y1"]["after"]))),
    ("ذروة الحاجة النقدية", "~%s من الـ‎$200,000‎ (أدنى رصيد %s، هامش أمان ~%s)؛ حالة ضغط صريحة ~%s عند السقف" % (nz(PEAK_NEED), nz(MIN_BAL), nz(HEADROOM), nz(STRESS_PEAK))),
    ("هيكل رأس المال", "%s حقوق ملكية (50/50) + %s قرض مساهم مضمون (الشريك أ، مسجّل PPSR)" % (nz(EQUITY), nz(LOAN))),
    ("نقطة التعادل", "~الشهر 12 على أساس EBITDA قبل المسحوبات؛ رواتب سوقية كاملة للملاك تصبح ممكنة من السنة الثانية"),
]))
story.append(Spacer(1, 8)); story.append(revenue_chart())
story.append(SMALL("الخطة إشارة خضراء على الهيكل والقانونيات أولاً، ثم الإطلاق لملء الشتاء بإعادة الدهانات الداخلية وأعمال إدارة الأملاك لتجميع التقييمات قبل الربيع، ثم التخصّص وفق بيانات الهامش الحقيقية بنهاية السنة الأولى."))
story.append(PageBreak())

# 2. MARKET
sec("2.  السوق")
story.append(B("القراءة الاستراتيجية: التركيز على طلب إعادة الدهان السكني المتكرّر والمضاد للدورة (دورة الواجهات الخشبية في أوكلاند ~7–10 سنوات، أقصر على السواحل والأشعة العالية)، والتركّز في أوكلاند (نحو ~44% من تصاريح البناء الوطنية بحلول 2030)، واستخدام الأعمال التجارية الخفيفة والداخلية كتحوّط شتوي مستقل عن الطقس — مع البناء الجديد كإضافة انتهازية فقط."))
story.append(H2("حقائق السوق (بمصادرها)"))
story.append(ar_table(
    ["العامل", "الرقم", "المصدر"],
    [
        ("حجم السوق", "~‎$1.9‎ مليار (2025)، نحو ‎$2.0‎ مليار (2026)", "IBISWorld — قطاع 332"),
        ("المسار", "‎-7.0%‎ (2024)، ‎-3.2%‎ (2025)", "IBISWorld — قطاع 332"),
        ("التجزّؤ", "~5,832 شركة؛ لا لاعب سكني مهيمن", "IBISWorld — قطاع 332"),
        ("تصاريح جديدة", "~33,530 مسكن (حتى مايو 2025)، ‎-3.8%‎", "Stats NZ، مايو 2025"),
        ("حصة أوكلاند", "نحو ~44% من التصاريح الوطنية بحلول 2030", "MBIE — خط أنابيب الإنشاء"),
        ("دورة إعادة الدهان", "الواجهات الخشبية ~7–10 سنوات", "The House Painters (أوكلاند)"),
        ("الموسمية", "ذروة خارجية نوفمبر–أبريل؛ انتظار 4–8 أسابيع", "Automate The Trades 2026"),
        ("حاجز الدخول", "الدهان ليس عملاً مقيّداً — لا رخصة LBP", "Building Performance (MBIE)"),
        ("التهديد", "الاستبدال بالعمل الذاتي، خاصة داخلياً", "IBISWorld — قطاع 332"),
    ],
    [95, 210, 182]))
story.append(Spacer(1, 5))
story.append(SMALL("ملاحظة حوكمة: كل رقم أعلاه منسوب إلى مصدر مُنتَج قابل للإثبات (IBISWorld قطاع 332، Stats NZ، MBIE) — الروابط الكاملة في ملحق المصادر. لا يُنسب أي إحصاء لمجلس أو شرطة أو جهة دون مصدر."))
story.append(PageBreak())

# 3. POSITIONING
sec("3.  التموضع والاستراتيجية")
story.append(LEAD("رأس الحربة: إعادة دهان الواجهات الخشبية السكنية الفاخرة"))
story.append(B("في سوق مجزّأ بنحو 5,800 شركة يحدّد العميل السعر، لذا يحتاج الوافد الجديد بلا تقييمات إلى ميزة ملموسة لا إلى سعر تكلفة‑زائد. إعادة الدهان الخارجي هي أفضل مسار لأنها مضادة للدورة (غير معرّضة لتراجع البناء)، ومتكرّرة (دورة 7–10 سنوات تولّد التكرار وكثافة الإحالات)، والأعلى قيمة للوظيفة (‎$10,000–20,000‎)، وأفضل ملف نقدي (دفعة مقدّمة + مطالبة مرحلية + إتمام ≈ شروط 0–14 يوماً)."))
story.append(B("أبقِ الاستقبال انتهازياً — اقبل الدهانات الداخلية وأعمال الصيانة/تسليم الإيجارات والتجاري الخفيف الذي يأتي — لكن وجّه 100% من إنفاق التسويق وجمع التقييمات وطلب الإحالة نحو مسار الواجهات الخارجية الواحد كي يدور الدولاب. احسم مسار التخصّص الدائم وفق بيانات الهامش الحقيقية بنهاية السنة الأولى لا الثانية."))
story.append(H2("عرض القيمة — وعد جودة قابل للتحقّق"))
story.append(B("كل عمل يُنفَّذ وفق نطاق مكتوب ومُقاس يستند إلى معيار AS/NZS 2311، مدعوماً بضمان إعادة عمل ثابت، واعتماد Dulux Accredited / Resene Eco.Decorator، وضمان الصنعة من المصنّع لخمس سنوات. يُسعّر بالتكافؤ (دون علاوة ذروة) في السنة الأولى لبناء قاعدة تقييمات، مع إضافة العلاوة وضمان Master Painters NZ لخمس سنوات في السنة الثانية (عضوية MPNZ محجوبة حتى ~2027–28: 18 شهراً + 3 وظائف مُعاينة)."))
story.append(H2("خيارات اسم العلامة (للحسم)"))
for n in ["Weatherline Painters — يشير إلى تخصّص الواجهات الخارجية",
          "Trueline Decorators Auckland",
          "Northside Repaint Co. — مركّز على الأحياء وإعادة الدهان",
          "Clearcoat Painting & Decorating",
          "Harbour City Repaints"]:
    story.append(LI(n))
story.append(PageBreak())

# 4. BUSINESS MODEL
sec("4.  نموذج العمل واقتصاديات الوحدة")
story.append(B("شركة دهانات مستقلة بعلامتها الخاصة في أوكلاند، بإدارة خلفية واستقطاب عملاء ذاتيين. الشريك أ يدير المال والنمو والإدارة الخلفية ويوفّر كامل رأس المال؛ الشريك ب، دهّان مؤهّل ذو خبرة، يدير التنفيذ كقائد عامل — التسعير والجودة والعمل الميداني — ويبني طاقم مقاولين باطنيين. السنة الأولى خفيفة الطاقة عمداً وحامية للنقد."))
story.append(H2("نموذج الطاقم — المقاول الباطن أولاً، مُحصّن"))
story.append(LI("المقاول الباطن أولاً في السنة الأولى لتحويل العمالة إلى تكلفة متغيّرة وحماية سقف الـ‎$200,000‎."))
story.append(LI("تأمين 1–2 مقاول باطن «مرساة» بعقود أولوية/استبقاء — الجيّدون في أوكلاند محجوزون 4–8 أسابيع في ذروة نوفمبر–أبريل، فالسيولة عند الطلب غير موثوقة وقت الحاجة."))
story.append(LI("منع أعمال الارتفاع/الرصاص دون إشراف للمقاولين الجدد؛ تمرير كل مقاول عبر وظائف تجريبية مدفوعة ومُعاينة بالكامل — مسؤولية إعادة العمل بموجب قانون ضمانات المستهلك تقع على الشركة بغضّ النظر عن صفة المقاول."))
story.append(LI("توثيق كل مقاول كعقد خدمات حقيقي (ضريبته وACC وأدواته، غير حصري، بفواتير) لتجنّب إعادة التصنيف من IRD/MBIE."))
story.append(LI("تقديم توظيف أول دهّان مؤهّل إلى بداية النصف الثاني كاحتياطي استمرارية وجودة — ثم تحويل الأفضل إلى توظيف عند استقرار معدّل الدوران فوق ~‎$400,000‎."))
story.append(H2("اقتصاديات الوحدة"))
story.append(ar_table(
    ["المقياس", "القيمة", "ملاحظة"],
    [
        ("سعر العمالة للعميل", nz(CHARGE_OUT) + "/ساعة", "تكلفة‑زائد على أجر المقاول"),
        ("تكلفة المقاول الباطن", nz(SUBBIE_HR) + "/ساعة", "متغيّرة؛ دون أجور تعطّل"),
        ("الدهّان الموظّف (شامل)", nz(EMPLOYED_HR) + "/ساعة", "~‎$30‎ + 12–18% أعباء"),
        ("المواد", "19% من الإيراد", "حسابات Resene/Dulux التجارية"),
        ("الهامش الإجمالي (س1)", "30%", "مُحمّل بالكامل مع كل العمالة المباشرة"),
        ("متوسط وظيفة خارجية/سكنية", nz(AVG_RES_JOB), "داخلي ~‎$5,500‎؛ طابقان ‎$20–30k+‎"),
        ("متوسط وظيفة تجارية خفيفة", nz(AVG_COMM_JOB), "أعمال صيانة بأجر يومي"),
    ],
    [150, 90, 247]))
story.append(SMALL("العمالة 75–85% من تكلفة الوظيفة، فمزيج الطاقم هو أكبر رافعة للهامش والنقد. يرتفع الهامش إلى 39–43% في السنتين الثانية والثالثة مع رفع نواة موظّفة لمعدّل الاستغلال."))
story.append(PageBreak())

# 5. GO TO MARKET
sec("5.  الذهاب إلى السوق")
story.append(B("مهمة الوافد الجديد الأولى صناعة الثقة بسرعة ورخص، ثم تحويلها إلى محرّك إحالات شبه مجاني. الإنفاق مرحلي: قنوات مجانية وبالدفع‑لكل‑عميل أولاً، وإعلانات Google المدفوعة فقط بعد أن يحوّل الموقع الزوار وتوجد تقييمات."))
story.append(ar_table(
    ["القناة", "التكتيك", "التكلفة/CAC"],
    [
        ("Google Business Profile", "المطالبة والتحسين يوم واحد؛ جمع التقييمات من أول وظيفة", "‎$0‎ (وقت)"),
        ("Builderscrack (دفع لكل عميل)", "تدفّق فوري الأسبوع الأول؛ رفع التحويل 1‑من‑7 ← 1‑من‑3", "~‎$40–100‎/وظيفة"),
        ("NoCowboys (اشتراك)", "الإدراج الشهر الأول؛ تجميع تقييمات علنية، والعلاقة تبقى لك", "‎$999‎/سنة"),
        ("الوكلاء ومديرو الأملاك", "حزمة تواصل لتجديدات ما قبل البيع وتسليم الإيجارات (بناء س2)", "منخفضة؛ شروط 14–45 يوماً"),
        ("بحث Google المدفوع", "يُضاف من الشهر 2–3 بعد أن يحوّل الموقع وتوجد تقييمات", "~‎$2,000–2,500‎/شهر"),
        ("فيسبوك/إنستغرام + الإحالات", "محتوى قبل/بعد + طلب إحالة رسمي؛ يهيمن بحلول الشهر 3–6", "~‎$0–300‎/شهر"),
    ],
    [130, 250, 107]))
story.append(Spacer(1, 6)); story.append(H2("أول 90 يوماً"))
for t in [
    "تسجيل الشركة وIRD؛ التسجيل في GST من اليوم الأول على أساس نقدي (Payments)؛ تسجيل الشريك ب في ACC CoverPlus.",
    "تنفيذ القانونيات قبل بدء العمل: اتفاق المساهمين + النظام + سند قرض المساهم/PPSR + تنازل الملكية الفكرية + الاستحقاق العكسي + القيود؛ وربط تأمين الشخص المحوري وحماية الدخل على الشريك ب.",
    "فتح حسابي Resene وDulux التجاريين (توقّع الدفع نقداً في الأشهر 1–3)؛ والتقدّم لاعتماد Dulux Accredited / Resene Eco.Decorator.",
    "استئجار العربة؛ شراء معدات الرش والتحضير وطقم HEPA-P2؛ بناء منظومة السلامة (إجراءات الارتفاع/الوصول، إجراء الرصاص، جرد المواد الخطرة)؛ وبدء SiteWise (هدف أخضر 75%+).",
    "المطالبة بملف GBP وتحسينه؛ إطلاق موقع يحوّل الزوار؛ الإدراج في NoCowboys؛ تشغيل Builderscrack — دون إنفاق Google مدفوع بعد.",
    "توقيع 1–2 مقاول باطن مرساة بعقود أولوية؛ وتمرير كلٍّ عبر وظيفة تجريبية مدفوعة ومُعاينة بالكامل.",
    "ملء ركود الشتاء بالدهانات الداخلية وتسليم الإيجارات لتجميع التقييمات قبل نهضة الربيع (سبتمبر–أكتوبر).",
    "تشغيل Xero وServiceM8؛ ضبط تعهّد بحد أدنى نقدي ~‎$30,000‎ وحساب فرعي لاحتياطي الضريبة (~28% من الربح).",
]:
    story.append(LI(t))
story.append(PageBreak())

# 6. OPERATIONS
sec("6.  العمليات والجودة والصحة والسلامة")
story.append(B("يقود التنفيذ الشريك ب كقائد عامل، لكن النموذج يتوقّف صراحةً عن احتساب ساعاته مرّتين (محرّك إيراد + وظيفة جودة/تسعير): نخصّص وقتاً حقيقياً غير قابل للفوترة للجودة والتسعير (1–2 يوم أسبوعياً) ونخفض سقف إيراد السنة الأولى تبعاً لذلك (فعلياً ~1.2–1.8 دهّان قابل للفوترة)."))
story.append(H2("ضبط الجودة"))
story.append(LI("نطاق مكتوب ومُقاس بمعيار AS/NZS 2311 لكل وظيفة؛ واعتماد جودة من الشريك ب قبل إصدار الفاتورة."))
story.append(LI("تمرير المقاولين الجدد عبر وظائف تجريبية مدفوعة ومُعاينة بالكامل قبل أي عمل دون إشراف."))
story.append(LI("احتياطي إعادة عمل/ضمان (~3% من الإيراد) يموّل الإصلاحات — المسؤولية بموجب قانون ضمانات المستهلك على الشركة لا المقاول."))
story.append(LI("اعتماد Dulux/Resene + ضمان صنعة المصنّع 5 سنوات في السنة الأولى؛ وضمان MPNZ 5 سنوات في الشهر 18."))
story.append(H2("الصحة والسلامة (HSWA / WorkSafe)"))
story.append(LI("وثيقة SWMS/JSA لكل وظيفة للارتفاع والرصاص؛ سقّال معتمد وإخطار WorkSafe حيث يُحتمل سقوط 5 أمتار+."))
story.append(LI("تأجير (لا ارتجال) معدات الوصول للطابقين+؛ الشركة هي الجهة المسؤولة (PCBU) بغضّ النظر عن صفة المقاول."))
story.append(LI("ضوابط رصاص P2/HEPA لمنازل ما قبل 1980 (حُظر الرصاص في الدهان السكني 1979)؛ تخلّص مرخّص عبر Resene PaintWise."))
story.append(LI("تغطية المسؤولية القانونية؛ منظومة سلامة مُختبرة بـSiteWise (هدف أخضر 75%+) لفتح الأعمال التجارية."))
story.append(H2("الأنظمة والتوظيف"))
story.append(B("Xero (أساس GST نقدي) + ServiceM8 للتسعير والجدولة والفوترة؛ تأهيل مسبق SiteWise؛ جرد مواد خطرة + SDS. التوظيف المحوري: أول دهّان مؤهّل في بداية النصف الثاني كاحتياطي استمرارية وجودة (التخفيف الهيكلي الوحيد لخطر الشخص المحوري)، ثم متدرّب BCITO في السنة الثانية وقائد غير مالك بحلول السنة الثالثة لنقل التنفيذ عن كاهل الشريك ب ورفع قيمة الخروج."))
story.append(PageBreak())

# 7. FINANCIAL PLAN
sec("7.  الخطة المالية")
story.append(H2("7.1  استخدام الـ‎$200,000‎"))
uf = [(d, nz(a)) for d, a in USE_OF_FUNDS]
uf.append(("إجمالي فرعي للتأسيس", nz(SETUP_TOTAL)))
uf.append(("احتياطي رأس المال العامل (يموّل تصاعد السنة الأولى)", nz(RESERVE)))
uf.append(("إجمالي رأس المال المُوظَّف", nz(CAPITAL)))
story.append(ar_table(["استخدام الأموال", "دولار"], uf, [400, 87],
                      hi_rows=[len(USE_OF_FUNDS) + 1, len(USE_OF_FUNDS) + 3]))
story.append(SMALL("رأس المال الداخل: %s حقوق ملكية + %s قرض مساهم مضمون (الشريك أ) = %s. يُنفق %s فقط على التأسيس في اليوم الأول؛ ويبقى %s احتياطي رأس مال عامل يحمل تصاعد السنة الأولى وركود الشتاء." % (nz(EQUITY), nz(LOAN), nz(CAPITAL), nz(SETUP_TOTAL), nz(RESERVE))))
story.append(H2("7.2  قائمة الدخل لثلاث سنوات (أساسي)"))
def prow(label, key, pct=False):
    return [label] + [("%.0f%%" % (PL[y][key] * 100)) if pct else nz(PL[y][key]) for y in ("Y1", "Y2", "Y3")]
plr = [
    prow("الإيراد", "rev"),
    prow("تكلفة المبيعات (مواد + عمالة مباشرة)", "cogs"),
    prow("الربح الإجمالي", "gp"),
    ["الهامش الإجمالي", "30%", "39%", "43%"],
    prow("مصروفات تشغيل ثابتة (بلا مسحوبات)", "fixed"),
    prow("مخصّصات (إعادة عمل 3% + ديون 1.5%)", "prov"),
    prow("EBITDA قبل مسحوبات الملاك", "ebitda_bd"),
    prow("مسحوبات الملاك (مجمّعة، مرحلية)", "draws"),
    prow("النتيجة التشغيلية بعد المسحوبات", "after"),
]
story.append(ar_table(["دولار", "السنة 1", "السنة 2", "السنة 3"], plr, [244, 81, 81, 81], hi_rows=[7, 9]))
story.append(B("الصورة الصادقة: EBITDA قبل مسحوبات الملاك يسير %s (س1، قرب التعادل) ← %s (س2، ~18%%) ← %s (س3، ~23%%). السنة الأولى سنة استثمار متعمّدة — بعد مسحوبات متواضعة ومرحلية تسجّل ~%s تُموَّل من الاحتياطي لا من نقد جديد. الرواتب السوقية الكاملة (‎$70–90k‎ لكلٍّ) تصبح ممكنة من السنة الثانية." % (nz(PL["Y1"]["ebitda_bd"]), nz(PL["Y2"]["ebitda_bd"]), nz(PL["Y3"]["ebitda_bd"]), nz(PL["Y1"]["after"]))))
story.append(SMALL("مذكّرة تمويل: قرض المساهم ‎$150k‎ يستحق فائدة ~9% (~‎$13.5k‎/سنة، دخل للشريك أ) — يُفترض تراكمه لا دفعه خلال السنة الأولى لحماية السقف. احجز ~28% من الربح لضريبة الختام والضريبة المؤقتة للسنة الثانية."))
story.append(H2("7.3  التدفّق النقدي للسنة الأولى وسقف الـ‎$200k‎"))
story.append(cashflow_chart())
story.append(B("ذروة الحاجة النقدية الأساسية ~%s من الـ‎$200k‎ (يهبط أدنى رصيد إلى ~%s)، بهامش أمان حقيقي ~%s — لا «‎$80k‎ مريح» كما قبل المراجعة. وتبلغ حالة الضغط الصريحة ~%s عند السقف إن تزامنت روافع الاختراق (انجراف التجاري نحو ~50%% بشروط 60 يوماً واحتجازات، ومدين بطيء/متنازع، وتصاعد أبطأ 6 أشهر، وسحب الشريكين رواتب كاملة). فالسقف قيد حقيقي لا مريح." % (nz(PEAK_NEED), nz(MIN_BAL), nz(HEADROOM), nz(STRESS_PEAK))))
story.append(H2("قواعد الضبط للبقاء تحت السقف"))
for t in [
    "المقاول الباطن أولاً يبقي العمالة متغيّرة؛ والأعمال السكنية المموّلة بدفعات مقدّمة/مرحلية تموّل موادها وعمالتها.",
    "استئجار العربة (يوفّر ~‎$23k‎) وتأجير معدات الوصول الكبيرة.",
    "اختيار أساس GST النقدي — لا تسدّد ضريبة على فواتير تجارية غير محصّلة.",
    "التجاري أقل من 30% من الفوترة حتى تثبت الشروط؛ ولا توظيف حتى يتجاوز معدّل الدوران ‎$400k‎.",
    "ربط مسحوبات الشريكين بتعهّد حد أدنى نقدي ~‎$30k‎؛ وحمل الاحتياطي عبر الشتاء.",
    "افتراض شراء المواد نقداً في الأشهر 1–3؛ واختبار حساسية لالتقاط الدفعات المقدّمة عند ~50% موثوقية.",
]:
    story.append(LI(t))
story.append(PageBreak())

# 8. OWNERSHIP
sec("8.  الملكية ورأس المال والهيكل القانوني")
story.append(LEAD("أهم قرار: كيف تدخل الـ‎$200,000‎"))
story.append(B("يموّل الشريك أ 100% من رأس المال لكنه يأخذ 50% ملكية. لو تُركت كحقوق ملكية عادية مناصفة، فإنها تمنح الشريك ب ~‎$100,000‎ في اليوم الأول وتحبس نقد أ خلف كل شيء، لا يُسترد إلا عبر أرباح يتقاسمها مناصفة. الحل يبقي مكاسب المناصفة لكن يجعل أ يسترد أولاً:"))
story.append(kv([
    ("حقوق الملكية", "~%s مناصفة — تعكس نقد أ ومهارة/جهد ب" % nz(EQUITY)),
    ("قرض المساهم", "~%s من الشريك أ، بفائدة سوقية (~8–10%%)، مسجّل على PPSR، يُسدَّد قبل أي أرباح" % nz(LOAN)),
    ("الكيان", "شركة محدودة عادية (المسؤولية غير المحدودة للشراكة غير مقبولة لمهنة ارتفاع/رصاص)"),
    ("الضريبة", "أساس GST نقدي من اليوم الأول؛ استشر بشأن اختيار LTC للسنة الأولى لتمرير خسائر التصاعد للشريك أ مقابل اختبار استمرارية المساهمة 49%"),
]))
story.append(H2("اتفاق المساهمين — بنود لا غنى عنها"))
for t in [
    "استحقاق عكسي لحصة ب البالغة 50% على 4 سنوات (سنة جرف ثم شهرياً)؛ إعادة شراء غير المستحق بقيمة اسمية عند خروج «المغادر السيّئ» وبالقيمة العادلة عند «المغادر الحسن».",
    "قيد عدم منافسة + عدم استقطاب للعملاء والموظفين والمقاولين (الدهان لا يحتاج رخصة، فقد يغادر ب وينافس فوراً).",
    "تنازل كامل عن الملكية الفكرية/العلامة للشركة — العلامة التجارية والنطاق وملف Google والحسابات والموقع — لا باسم ب شخصياً.",
    "تأمين شخص محوري (حياة + عجز كلي دائم + مرض على ب) بحجم القرض + ~6 أشهر مصروفات، مُهيكل لتمويل بيع/شراء يُخرج ورثة ب ويعيد رأسمال أ؛ + حماية دخل / ACC CoverPlus Extra.",
    "آلية فض التعثّر: قائمة مسائل محفوظة، سلّم تصعيد (تفاوض ← وساطة ← بيع/شراء إجباري «شوت‑غن»)، وصوت مرجّح لأ في مسائل المال ما دام القرض قائماً.",
    "سياسة أجور وتوزيع موثّقة: أجر سوقي لكل مالك مقابل العمل المؤدَّى، فائدة لأ على القرض، ثم الربح المتبقّي مناصفة كأرباح — كلها مرحلية حسب النقد.",
    "توزيع الكفالات موثّق: العربة بإيجار بدفعة صغيرة؛ سقوف حسابات تجارية محدودة؛ حيث لا يكفل إلا أ، سعّر ذلك الخطر بتعويض متبادل مناصفة؛ وتجنّب الكفالات على أي سحب على المكشوف.",
]:
    story.append(LI(t))
story.append(PageBreak())

# 9. RISKS
sec("9.  المخاطر وتخفيفها")
story.append(ar_table(
    ["الخطر", "الاحتمال/الأثر", "التخفيف"],
    [
        ("انهيار الشخص المحوري — ب هو الدهّان/المقدّر/المراقب/المؤهّل الوحيد", "متوسط / مرتفع", "تأمين شخص محوري + حماية دخل؛ دهّان موظّف مبكّراً كاحتياطي؛ نمذجة سيناريو غياب 4 أسابيع؛ قائد غير مالك بحلول س3"),
        ("فخّ الهامش — تسعير بنطاق التكلفة يعطي ~12% هامش", "مرتفع / مرتفع", "تكلفة‑زائد (ادفع ‎$55‎ حاسب ‎$95‎)؛ هامش س1 30% مُحمّل؛ تحقّق من السعر مقابل 5–10 عروض"),
        ("اختراق سقف النقد — انجراف تجاري + مدينون بطيئون → ~‎$195k‎", "متوسط / مرتفع", "استئجار العربة؛ GST نقدي؛ ضوابط صارمة؛ احتياطي ‎$25k‎ عبر الشتاء؛ حجم السيولة للحالة الدنيا"),
        ("نزاع تباين رأس المال — أ يموّل 100% مقابل 50% ملكية", "متوسط / مرتفع", "‎$50k‎ ملكية + ‎$150k‎ قرض مضمون PPSR؛ استحقاق عكسي؛ قيود + ملكية فكرية؛ صوت مرجّح لأ"),
        ("البداية الباردة والموسمية — الإطلاق شتاءً يفوّت أول ذروة", "مرتفع / متوسط", "أساس س1 ‎$235k‎؛ ملء الشتاء بالداخلي والتسليمات لتجميع التقييمات؛ ‎$285k‎ حالة عليا"),
        ("توفّر وجودة المقاولين — محجوزون في الذروة؛ الأعمال المبكّرة يانصيب جودة", "متوسط / متوسط", "1–2 مقاول مرساة؛ وظائف تجريبية مُعاينة؛ احتياطي إعادة عمل ~3%؛ منع أعمال ارتفاع دون إشراف"),
        ("إعادة تصنيف المقاول (IRD/MBIE) — استرداد PAYE/كيويسيفر + غرامات", "متوسط / متوسط", "عقود خدمات حقيقية؛ تقبّل عدم الموثوقية أو التحويل للتوظيف وتسعير الأعباء"),
        ("حادث ارتفاع/رصاص (HSWA) — مسؤولية قانونية + إجراء WorkSafe", "منخفض / مرتفع", "تغطية مسؤولية قانونية؛ SWMS/JSA لكل وظيفة؛ سقّال معتمد للـ5م+؛ ضوابط P2/HEPA؛ تأجير الوصول"),
        ("غياب التمايز — تشتيت طاقة ب يوقف دولاب الإحالات", "متوسط / متوسط", "مسار واحد بنطاق AS/NZS 2311 + ضمان إعادة عمل ثابت؛ 100% تسويق عليه؛ تخصّص بنهاية س1"),
        ("جدار الضريبة — ضريبة ختام + مؤقتة للسنة الثانية", "متوسط / منخفض", "حجز ~28% من الربح من أول شهر مربح؛ ملاحظة تراكم الضريبة المؤقتة"),
    ],
    [186, 66, 235]))
story.append(PageBreak())

# 10. ROADMAP
sec("10.  خارطة الطريق والمراحل")
story.append(H2("المرحلة 0 — ما قبل الإطلاق (الأسابيع 0–8)"))
story.append(B("تنفيذ الهيكل والقانونيات قبل بدء العمل: الشركة + GST (نقدي) + ACC؛ حزمة اتفاق المساهمين الكاملة؛ ربط تأمين الشخص المحوري وحماية الدخل؛ استئجار العربة؛ شراء طقم الرش وHEPA-P2؛ فتح حسابي Resene/Dulux واختيار علامة أساسية؛ بناء العلامة/الموقع/GBP؛ توقيع 1–2 مقاول مرساة؛ بناء منظومة السلامة وبدء SiteWise."))
story.append(H2("المرحلة 1 — بناء الشتاء (الأشهر 1–6)"))
story.append(B("ملء الركود بالدهانات الداخلية والتسليمات لتجميع التقييمات؛ تشغيل Builderscrack وNoCowboys وGBP (دون Google مدفوع)؛ إضافة Google المدفوع من الشهر 2–3 بعد أن يحوّل الموقع؛ تمرير المقاولين الجدد عبر وظائف تجريبية؛ توظيف أول دهّان مؤهّل في بداية النصف الثاني كاحتياطي استمرارية/جودة؛ حمل الاحتياطي وتعهّد الحد الأدنى النقدي ~‎$30k‎ عبر الشتاء."))
story.append(H2("المرحلة 2 — الذروة والتخصّص (الأشهر 7–18)"))
story.append(B("اقتناص موسم الواجهات نوفمبر–أبريل بناءً على سمعة بُنيت شتاءً؛ تحويل تواصل مديري الأملاك/الوكلاء إلى عقود متكرّرة؛ حسم مسار التخصّص وفق بيانات الهامش بنهاية س1؛ بلوغ SiteWise الأخضر لفتح التجاري الخفيف؛ التقدّم لعضوية MPNZ في الشهر 18؛ من س2 إضافة دهّان موظّف + متدرّب BCITO عند تجاوز الدوران ‎$400k‎، واستعادة تسعير علاوة الذروة، وبدء نقل التنفيذ عن كاهل ب."))
story.append(H2("المراحل الرئيسية"))
for t in [
    "ربط القانونيات والتأمين وهيكلة الـ‎$200k‎ (ملكية + قرض مضمون) قبل أول وظيفة.",
    "أول 10–20 وظيفة منجزة بتقييمات مُجمّعة قبل نهضة الربيع (سبتمبر–أكتوبر).",
    "أساس GST نقدي + تعهّد حد أدنى نقدي + احتياطي ضريبة فعّال من الشهر الأول.",
    "توظيف أول دهّان مؤهّل في بداية النصف الثاني كاحتياطي استمرارية/جودة.",
    "إبقاء ذروة النقد تحت ~‎$150k‎ أساسي عبر الشتاء؛ وعدم اختراق سقف الـ‎$200k‎ أبداً.",
    "بلوغ SiteWise الأخضر (75%+) لفتح الأعمال التجارية.",
    "إيراد س1 ‎$235k‎ أساسي (حد أدنى ‎$200k‎) مع قرار مسار تخصّص موثّق بنهاية س1.",
    "تقديم طلب MPNZ في الشهر 18؛ ومعدّل دوران س2 فوق ‎$400k‎ قبل تحويل المقاولين للتوظيف.",
]:
    story.append(LI(t))
story.append(PageBreak())

# 11. WHAT ETR CHANGED (condensed)
sec("11.  ما الذي غيّرته المراجعة الخصمية (ETR)")
story.append(B("أُنتجت هذه الخطة بمنظومة عمل وكيلة على نمط ETR: سبعة وكلاء بحث ويب رسموا السوق النيوزيلندي الحيّ؛ ووكيل افتراضات بنى نموذجاً أولياً؛ وخمسة مراجعين خصميين (الواقعية المالية، السوق/المنافسة، الجدوى التشغيلية، النقد/السيولة، الشراكة/القانون/الضريبة) هاجموه — اثنان أعادا حكم «فشل»؛ ثم حصّنت خطوة تركيب الخطة. أبرز التصحيحات:"))
for t in [
    "التسعير — من ‎$65‎ قاتلة (داخل نطاق ‎$45–75‎ → ~12% هامش) إلى تكلفة‑زائد: ادفع ‎$55‎ حاسب ‎$95‎.",
    "الهامش الإجمالي — من 45% إلى 30% مُحمّل في س1، يرتفع إلى 38–42% في س2–س3.",
    "الإيراد — خفض أساس س1 من ‎$285k‎ إلى ‎$235k‎ (وافد بلا سمعة يطلق في الشتاء يفوّت أول ذروة).",
    "هيكل رأس المال — تقسيم الـ‎$200k‎ إلى ‎$50k‎ ملكية + ‎$150k‎ قرض مساهم مضمون PPSR يُسدَّد أولاً.",
    "العربة — الإيجار (~‎$5k‎ دفعة) أساساً بدل شراء نقدي ‎$28k‎ — يستعيد ~‎$23k‎ من السقف.",
    "GST — اختيار الأساس النقدي لإزالة فخ سداد الضريبة على مدينين بطيئين قبل التحصيل.",
    "أجر الملاك — إضافة خط أجر صريح للشريك ب؛ النموذج السابق موّل مسحوب أ فقط.",
    "الشخص المحوري — إضافة تأمين حياة/عجز/مرض على ب + حماية دخل (~‎$2–3.5k‎/سنة)؛ كان صفراً.",
    "المخصّصات — إضافة احتياطي إعادة عمل (~3%) وديون معدومة (~1.5%)؛ كانت صفراً.",
    "ذروة النقد — من ‎$120k‎ («‎$80k‎ هامش») إلى ~‎$150k‎ أساسي مع حالة ضغط صريحة ~‎$195k‎ عند السقف.",
    "التموضع — الالتزام بمسار واحد بميزة قابلة للتحقّق؛ وضبط علاوة الذروة على 0% في س1.",
    "القانوني — إفراد بند قانوني بـ~‎$7k‎؛ وإضافة آلية تعثّر وتنازل ملكية فكرية وسياسة أجور.",
]:
    story.append(LI(t))
story.append(PageBreak())

# APPENDIX
sec("ملحق أ — أسئلة مفتوحة يجب حسمها")
story.append(B("أكّد ما يلي قبل رصد رأس المال وتوقيع القانونيات:"))
for t in [
    "الرسم الدقيق لحساب عمل ACC لوحدة تصنيف الدهان (غالباً CU 42110) في دليل رسوم ACC 2026/27 (حالياً تقدير ~‎$1–2‎ لكل ‎$100‎).",
    "الحِمل الفعلي غير القابل للفوترة للشريك ب (تسعير + جودة + إدارة/أسبوع) — لتثبيت عدد الدهّانين الفعّالين وسقف إيراد س1.",
    "رسم عضوية MPNZ السنوي الفعلي (غير منشور؛ ~‎$500–1,200‎ تقدير) وأهلية بوابة 18 شهراً + 3 وظائف.",
    "استشارة محاسبية حول اختيار LTC للسنة الأولى لتمرير خسائر التصاعد للشريك أ مقابل اختبار الاستمرارية 49%.",
    "التحقّق من الرغبة في الدفع عند ‎$95‎/ساعة مقابل 5–10 عروض منافسين حقيقية في أوكلاند قبل تثبيت السعر.",
    "مدى قدرة الشريك ب على تمويل ~6 أشهر من الاستغلال المنخفض ذاتياً، أو حاجة النموذج لمسحوب معيشة أكبر له.",
    "تسعير Builderscrack الحالي بعد 2024 وأهلية الدهّانين لإعلانات Google Local Services في نيوزيلندا.",
    "تحديد شهر الإطلاق بدقّة — الهدف إنجاز وظائف وتجميع تقييمات قبل سبتمبر–أكتوبر لا في عمق الشتاء.",
]:
    story.append(LI(t))
story.append(Spacer(1, 8))
story.append(H1("ملحق ب — المصادر"))
story.append(HRule(FW)); story.append(Spacer(1, 5))
for t in [
    "IBISWorld — خدمات الدهان والديكور في نيوزيلندا (قطاع 332): حجم السوق والنمو وعدد الشركات والمنافسة.",
    "Stats NZ — تصاريح البناء الصادرة، مايو 2025: ~33,530 مسكن، ‎-3.8%‎.",
    "MBIE — تقرير خط أنابيب الإنشاء الوطني: أوكلاند ~44% من التصاريح الوطنية بحلول 2030.",
    "Building Performance (MBIE) — العمل الإنشائي المقيّد: الدهان ليس عملاً مقيّداً؛ لا رخصة LBP.",
    "Automate The Trades — أجر الدهان بالساعة NZ 2026: أجور المقاولين والموسمية وعلاوات الذروة.",
    "The House Painters (أوكلاند) — دورة إعادة الدهان الخارجي ~7–10 سنوات.",
    "أسعار حسابات Resene/Dulux التجارية؛ WorkSafe NZ (الارتفاع، السقالات، الرصاص)؛ Site Safe/SiteWise؛ ACC؛ Master Painters NZ.",
]:
    story.append(LI(t))
story.append(Spacer(1, 8))
story.append(SMALL("أُعدّت في 27 يوليو 2026. هذه وثيقة تخطيط داخلية للشريكين؛ لا تحمل عمداً أسماء عملاء لأطراف ثالثة ولا بيانات مالية لشركات ذات صلة. الأرقام تقديرات أساسية مُحصّنة بمراجعة ETR لأغراض القرار، لا توقّعات مدقّقة — أكّد الأسئلة المفتوحة أعلاه قبل رصد رأس المال."))

# ================================================================ RENDER
doc = Doc(PDF, pagesize=A4, title="Auckland Painting Co — Business Plan (Arabic)")
doc.build(story)
print("PDF ->", PDF)
print("Peak cash need", nz(PEAK_NEED), " Min bal", nz(MIN_BAL), " Headroom", nz(HEADROOM))
print("DONE")
