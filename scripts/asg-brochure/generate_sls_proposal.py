#!/usr/bin/env python3
"""
SLS RTC — EAS Product Proposal for Ngahuia Group / Outlet Stores
Uses Century branding guidelines with SLS RTC as distributor
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, Image, Flowable
)
from reportlab.pdfgen import canvas
import os

# ── Century Brand Colours (from catalog) ───────────────────────
CENTURY_NAVY = HexColor('#1B3A6B')       # Primary dark blue
CENTURY_BLUE = HexColor('#4A7FC5')       # Secondary/swoosh blue
CENTURY_LIGHT_BLUE = HexColor('#6EA8D7') # Lighter accent
CENTURY_DARK = HexColor('#1A1A2E')       # Near-black text
WHITE = HexColor('#FFFFFF')
GRAY_50 = HexColor('#F9FAFB')
GRAY_100 = HexColor('#F3F4F6')
GRAY_200 = HexColor('#E5E7EB')
GRAY_400 = HexColor('#9CA3AF')
GRAY_500 = HexColor('#6B7280')
GRAY_600 = HexColor('#4B5563')
GRAY_700 = HexColor('#374151')
TEXT_DARK = HexColor('#1F2937')

# ── SLS RTC Brand ──────────────────────────────────────────────
SLS_RED = HexColor('#C8102E')    # From logo
SLS_BLUE = HexColor('#0072CE')   # From logo
SLS_YELLOW = HexColor('#FFC72C') # From logo

# ── Page Setup ─────────────────────────────────────────────────
PAGE_W, PAGE_H = A4
MARGIN_SIDE = 50
MARGIN_TOP = 56
MARGIN_BOTTOM = 50
CONTENT_W = PAGE_W - 2 * MARGIN_SIDE

OUTPUT_PATH = os.path.expanduser(
    '~/Desktop/Clients/ASG/brochures/SLS_RTC_EAS_Proposal_Ngahuia_2026.pdf'
)

# ── Image paths ────────────────────────────────────────────────
IMG_DIR = '/tmp/century_products/crops'
SLS_LOGO = '/tmp/century_logo.png'

PRODUCT_IMAGES = {
    't001b': os.path.join(IMG_DIR, 't001b_mini_square.png'),
    't213': os.path.join(IMG_DIR, 't213_lanyard.png'),
    't511': os.path.join(IMG_DIR, 't511_multi_grip.png'),
    't504': os.path.join(IMG_DIR, 't504_baby_multi_grip.png'),
    'd104': os.path.join(IMG_DIR, 'd104_detacher.png'),
    'd204': os.path.join(IMG_DIR, 'd204_detacher.png'),
    'gf4040h': os.path.join(IMG_DIR, 'gf4040h_label.png'),
}


# ── Styles ─────────────────────────────────────────────────────
def make_styles():
    s = {}

    s['title_main'] = ParagraphStyle(
        'title_main', fontName='Helvetica-Bold', fontSize=30,
        leading=36, textColor=CENTURY_NAVY, alignment=TA_LEFT,
        spaceAfter=6
    )
    s['title_sub'] = ParagraphStyle(
        'title_sub', fontName='Helvetica', fontSize=14,
        leading=20, textColor=GRAY_500, alignment=TA_LEFT,
        spaceAfter=0
    )
    s['h1'] = ParagraphStyle(
        'h1', fontName='Helvetica-Bold', fontSize=22,
        leading=27, textColor=CENTURY_NAVY, alignment=TA_LEFT,
        spaceBefore=0, spaceAfter=10
    )
    s['h2'] = ParagraphStyle(
        'h2', fontName='Helvetica-Bold', fontSize=15,
        leading=20, textColor=CENTURY_NAVY, alignment=TA_LEFT,
        spaceBefore=14, spaceAfter=6
    )
    s['h3'] = ParagraphStyle(
        'h3', fontName='Helvetica-Bold', fontSize=12,
        leading=16, textColor=CENTURY_NAVY, alignment=TA_LEFT,
        spaceBefore=8, spaceAfter=4
    )
    s['overline'] = ParagraphStyle(
        'overline', fontName='Helvetica-Bold', fontSize=9,
        leading=12, textColor=CENTURY_BLUE, alignment=TA_LEFT,
        spaceBefore=0, spaceAfter=4
    )
    s['body'] = ParagraphStyle(
        'body', fontName='Helvetica', fontSize=10,
        leading=15, textColor=TEXT_DARK, alignment=TA_JUSTIFY,
        spaceBefore=0, spaceAfter=8
    )
    s['body_small'] = ParagraphStyle(
        'body_small', fontName='Helvetica', fontSize=9,
        leading=13, textColor=GRAY_600, alignment=TA_LEFT,
        spaceBefore=0, spaceAfter=4
    )
    s['product_name'] = ParagraphStyle(
        'product_name', fontName='Helvetica-Bold', fontSize=13,
        leading=17, textColor=CENTURY_NAVY, alignment=TA_LEFT,
        spaceBefore=0, spaceAfter=2
    )
    s['product_code'] = ParagraphStyle(
        'product_code', fontName='Helvetica-Bold', fontSize=9,
        leading=12, textColor=CENTURY_BLUE, alignment=TA_LEFT,
        spaceBefore=0, spaceAfter=6
    )
    s['spec_label'] = ParagraphStyle(
        'spec_label', fontName='Helvetica-Bold', fontSize=8.5,
        leading=11, textColor=GRAY_500, alignment=TA_LEFT,
    )
    s['spec_value'] = ParagraphStyle(
        'spec_value', fontName='Helvetica', fontSize=9,
        leading=12, textColor=TEXT_DARK, alignment=TA_LEFT,
    )
    s['bullet'] = ParagraphStyle(
        'bullet', fontName='Helvetica', fontSize=9.5,
        leading=14, textColor=TEXT_DARK, alignment=TA_LEFT,
        leftIndent=12, spaceBefore=0, spaceAfter=3, bulletIndent=0,
    )
    s['footer'] = ParagraphStyle(
        'footer', fontName='Helvetica', fontSize=7.5,
        leading=10, textColor=GRAY_400, alignment=TA_CENTER,
    )
    s['stat_number'] = ParagraphStyle(
        'stat_number', fontName='Helvetica-Bold', fontSize=28,
        leading=32, textColor=CENTURY_NAVY, alignment=TA_CENTER,
        spaceBefore=0, spaceAfter=2
    )
    s['stat_label'] = ParagraphStyle(
        'stat_label', fontName='Helvetica', fontSize=8.5,
        leading=12, textColor=GRAY_500, alignment=TA_CENTER,
    )
    s['toc_item'] = ParagraphStyle(
        'toc_item', fontName='Helvetica', fontSize=11,
        leading=22, textColor=TEXT_DARK, alignment=TA_LEFT,
    )
    return s


# ── Custom Flowable: Century-style dotted separator ────────────
class DottedSeparator(Flowable):
    def __init__(self, width=None, color=GRAY_200):
        super().__init__()
        self.width = width or CONTENT_W
        self.height = 8
        self.color = color

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineCap(1)  # round cap
        self.canv.setDash(1, 4)
        self.canv.setLineWidth(1)
        self.canv.line(0, 4, self.width, 4)


# ── Custom Flowable: Blue accent bar ──────────────────────────
class AccentBar(Flowable):
    def __init__(self, width=60, height=4, color=CENTURY_BLUE):
        super().__init__()
        self.width = width
        self.height = height + 8
        self._color = color

    def draw(self):
        self.canv.setFillColor(self._color)
        self.canv.roundRect(0, 4, self.width, self.height - 8, 2, fill=1, stroke=0)


# ── Page Templates ─────────────────────────────────────────────
def draw_cover(c, doc):
    """Century-style cover page."""
    w, h = PAGE_W, PAGE_H

    # White background (default)
    # Top blue swoosh bar
    c.setFillColor(CENTURY_NAVY)
    c.rect(0, h - 6, w, 6, fill=1, stroke=0)

    # Century-style blue accent swoosh (simplified as a gradient bar)
    c.setFillColor(CENTURY_BLUE)
    c.rect(0, h - 10, w * 0.6, 4, fill=1, stroke=0)

    # SLS RTC logo top right
    if os.path.exists(SLS_LOGO):
        c.drawImage(SLS_LOGO, w - MARGIN_SIDE - 120, h - 70, width=120,
                     height=30, preserveAspectRatio=True, mask='auto')

    # Century branding note bottom
    c.setFillColor(GRAY_400)
    c.setFont('Helvetica', 7.5)
    c.drawString(MARGIN_SIDE, 35, 'Century EAS products distributed by SLS Retail Theft Control Ltd')
    c.drawRightString(w - MARGIN_SIDE, 35, 'www.slsrtc.co.nz')

    # Bottom bar
    c.setStrokeColor(CENTURY_BLUE)
    c.setLineWidth(0.75)
    c.line(MARGIN_SIDE, 50, w - MARGIN_SIDE, 50)


def draw_content_page(c, doc):
    """Standard content page."""
    w, h = PAGE_W, PAGE_H

    # Top accent bar
    c.setFillColor(CENTURY_NAVY)
    c.rect(0, h - 4, w, 4, fill=1, stroke=0)
    c.setFillColor(CENTURY_BLUE)
    c.rect(0, h - 5.5, w * 0.3, 1.5, fill=1, stroke=0)

    # Header text
    c.setFillColor(GRAY_400)
    c.setFont('Helvetica', 7.5)
    c.drawString(MARGIN_SIDE, h - 20, 'SLS RTC  |  EAS Product Proposal  |  Ngahuia Group')

    # SLS logo small in header
    if os.path.exists(SLS_LOGO):
        c.drawImage(SLS_LOGO, w - MARGIN_SIDE - 60, h - 23, width=60,
                     height=15, preserveAspectRatio=True, mask='auto')

    # Footer
    c.setStrokeColor(GRAY_200)
    c.setLineWidth(0.5)
    c.line(MARGIN_SIDE, 36, w - MARGIN_SIDE, 36)

    # Page number
    c.setFillColor(GRAY_500)
    c.setFont('Helvetica', 8)
    c.drawCentredString(w / 2, 22, str(doc.page))

    # Century attribution
    c.setFillColor(GRAY_400)
    c.setFont('Helvetica', 6.5)
    c.drawRightString(w - MARGIN_SIDE, 22, 'Products by Century  |  century-cn.com')


# ── Product Card Builder ──────────────────────────────────────
def make_product_section(styles, name, code, description, specs, features, img_path=None, price=None, unit=None):
    """Build a product section with image and specs side by side."""
    elements = []

    # Product header with price
    elements.append(Paragraph(code.upper(), styles['product_code']))
    if price and unit:
        name_price = Table(
            [[Paragraph(name, styles['product_name']),
              Paragraph(f'<b>${price}</b> <font size="8" color="#{GRAY_500.hexval()[2:]}">{unit} excl. GST</font>',
                        ParagraphStyle('price', fontName='Helvetica-Bold', fontSize=13,
                                       leading=17, textColor=CENTURY_NAVY, alignment=TA_RIGHT))]],
            colWidths=[CONTENT_W * 0.6, CONTENT_W * 0.4]
        )
        name_price.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        elements.append(name_price)
    else:
        elements.append(Paragraph(name, styles['product_name']))
    elements.append(AccentBar(40, 3))
    elements.append(Spacer(1, 4))

    # Image + description side by side
    if img_path and os.path.exists(img_path):
        img = Image(img_path, width=140, height=110)
        img.hAlign = 'LEFT'

        desc_para = Paragraph(description, styles['body'])

        img_table = Table(
            [[img, desc_para]],
            colWidths=[155, CONTENT_W - 170]
        )
        img_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (0, 0), 0),
            ('LEFTPADDING', (1, 0), (1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        elements.append(img_table)
    else:
        elements.append(Paragraph(description, styles['body']))

    # Specs table
    if specs:
        elements.append(Spacer(1, 6))
        spec_data = []
        for label, value in specs:
            spec_data.append([
                Paragraph(f'<b>{label}</b>', styles['spec_label']),
                Paragraph(value, styles['spec_value']),
            ])
        t = Table(spec_data, colWidths=[120, CONTENT_W - 135])
        t.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('LEFTPADDING', (0, 0), (0, -1), 0),
            ('LEFTPADDING', (1, 0), (1, -1), 8),
            ('LINEBELOW', (0, 0), (-1, -2), 0.25, GRAY_200),
        ]))
        elements.append(t)

    # Features
    if features:
        elements.append(Spacer(1, 4))
        for f in features:
            elements.append(Paragraph(f'<bullet>&bull;</bullet> {f}', styles['bullet']))

    elements.append(Spacer(1, 6))
    elements.append(DottedSeparator())
    elements.append(Spacer(1, 10))

    return elements


# ── Build Document ─────────────────────────────────────────────
def build():
    styles = make_styles()

    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=MARGIN_SIDE,
        rightMargin=MARGIN_SIDE,
        topMargin=MARGIN_TOP + 20,
        bottomMargin=MARGIN_BOTTOM,
    )

    story = []

    # ══════════════════════════════════════════════════════════
    # COVER PAGE
    # ══════════════════════════════════════════════════════════
    story.append(Spacer(1, 80))

    # SLS RTC heading area
    story.append(Paragraph('EAS PRODUCT PROPOSAL', styles['overline']))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        'Electronic Article<br/>Surveillance',
        styles['title_main']
    ))
    story.append(Paragraph(
        'Tags, Labels, Detachers &amp; Detection Systems',
        styles['title_sub']
    ))
    story.append(Spacer(1, 8))
    story.append(AccentBar(80, 4, CENTURY_BLUE))

    story.append(Spacer(1, 30))

    # Cover product grid — show key product images
    cover_images = []
    for key in ['t001b', 't511', 'd104', 'gf4040h']:
        path = PRODUCT_IMAGES.get(key)
        if path and os.path.exists(path):
            cover_images.append(Image(path, width=110, height=85))
        else:
            cover_images.append(Paragraph('', styles['body']))

    if cover_images:
        cover_grid = Table(
            [cover_images],
            colWidths=[CONTENT_W / 4] * 4,
        )
        cover_grid.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(cover_grid)

    story.append(Spacer(1, 40))

    # Prepared for
    story.append(DottedSeparator())
    story.append(Spacer(1, 12))

    prep_data = [
        [
            Paragraph('<b>Prepared for</b>', styles['body_small']),
            Paragraph('<b>Prepared by</b>', styles['body_small']),
        ],
        [
            Paragraph('Ngahuia Group<br/>Outlet Stores', styles['body']),
            Paragraph('SLS Retail Theft Control Ltd<br/>Mark Clansey, General Manager', styles['body']),
        ],
        [
            Paragraph('', styles['body']),
            Paragraph('mark@slsrtc.co.nz  |  021 879 664', styles['body_small']),
        ],
    ]
    prep_table = Table(prep_data, colWidths=[CONTENT_W / 2] * 2)
    prep_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(prep_table)

    story.append(Spacer(1, 16))
    story.append(Paragraph(
        'April 2026',
        ParagraphStyle('date_cover', fontName='Helvetica', fontSize=11,
                       textColor=GRAY_500, spaceAfter=0)
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # PAGE 2: CONTENTS / INTRO
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('CONTENTS', styles['overline']))
    story.append(Paragraph('Product Overview', styles['h1']))
    story.append(AccentBar(50, 3))
    story.append(Spacer(1, 16))

    toc_items = [
        ('1.', 'Hard Tags', 'Reusable security tags for apparel'),
        ('2.', 'RF Labels', 'Disposable barcode labels for source tagging'),
        ('3.', 'Multi-Alarm Spider Tags', 'High-security alarming wraps'),
        ('4.', 'Detachers', 'Magnetic detachers for point of sale'),
        ('5.', 'Detection Antennas', 'EAS pedestals for store entry/exit'),
        ('6.', 'Guarding Services', 'Uniformed retail security'),
        ('7.', 'Pricing Summary', 'Product pricing schedule (NZD excl. GST)'),
    ]

    for num, title, desc in toc_items:
        toc_row = Table(
            [[
                Paragraph(f'<b>{num}</b>', ParagraphStyle(
                    'toc_num', fontName='Helvetica-Bold', fontSize=12,
                    textColor=CENTURY_BLUE)),
                Paragraph(f'<b>{title}</b><br/><font size="9" color="#{GRAY_500.hexval()[2:]}">{desc}</font>',
                          styles['toc_item']),
            ]],
            colWidths=[30, CONTENT_W - 40],
        )
        toc_row.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LINEBELOW', (0, 0), (-1, -1), 0.25, GRAY_200),
        ]))
        story.append(toc_row)

    story.append(Spacer(1, 24))
    story.append(Paragraph('ABOUT SLS RTC', styles['overline']))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        'SLS Retail Theft Control is a specialist retail loss prevention company operating '
        'across New Zealand. We supply and support a full range of EAS (Electronic Article '
        'Surveillance) products from Century \u2014 one of the world\u2019s largest publicly listed '
        'EAS manufacturers (Shenzhen Stock Exchange, 300078.SZ).',
        styles['body']
    ))
    story.append(Paragraph(
        'From disposable RF labels through to multi-alarm spider wraps and detection antennas, '
        'we provide the hardware, installation, and ongoing support to protect your merchandise. '
        'Combined with our uniformed guarding capability, we deliver a complete retail security '
        'package under one contract.',
        styles['body']
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # SECTION 1: HARD TAGS
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('1. HARD TAGS', styles['overline']))
    story.append(Paragraph('Reusable security tags', styles['h1']))
    story.append(AccentBar(50, 3))
    story.append(Spacer(1, 12))

    # T001B + P01
    story.extend(make_product_section(
        styles,
        name='Mini Square Hard Tag + Flat Steel Pin',
        code='T001B + P01',
        description=(
            'Compact, low-profile hard tag paired with a flat steel pin. One of the most '
            'widely deployed EAS tags in retail, suitable for apparel and soft goods. '
            'Multiple lock options provide flexibility across risk levels.'
        ),
        specs=[
            ('Frequency', '8.2 MHz'),
            ('Dimension', '51.5 mm \u00d7 42 mm'),
            ('Lock Options', 'Standard / Super / Super S / Hyper'),
            ('Colour', 'Black, White, or customised'),
            ('Pin (P01)', 'Flat steel, 16/19/21 mm, groove or smooth'),
        ],
        features=[
            'Low-profile design for minimal merchandise impact',
            'Multiple lock strengths for tiered security',
            'Compatible with standard and super magnetic detachers',
        ],
        img_path=PRODUCT_IMAGES['t001b'],
        price='0.10', unit='/set'
    ))

    story.append(PageBreak())

    # T213 on its own page to avoid blank page overflow
    story.append(Paragraph('1. HARD TAGS (CONTINUED)', styles['overline']))
    story.append(Spacer(1, 8))
    story.extend(make_product_section(
        styles,
        name='Milli Lanyard Tag',
        code='T213',
        description=(
            'Slim lanyard tag for items where pin attachment is not suitable. The '
            'integrated loop secures to merchandise without puncturing fabric \u2014 ideal '
            'for accessories, knitwear, and delicate garments.'
        ),
        specs=[
            ('Frequency', '8.2 MHz / 58 KHz'),
            ('Dimension', '48 mm \u00d7 13.5 mm'),
            ('Pin', '14 mm'),
            ('Lanyard', '90 mm'),
            ('Lock Options', 'Standard / Super'),
        ],
        features=[
            'Non-piercing \u2014 no marks left on merchandise',
            'Slim profile for small or delicate items',
            'Dual-frequency options available',
        ],
        img_path=PRODUCT_IMAGES['t213'],
        price='0.32', unit='/pcs'
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # SECTION 2: RF LABELS
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('2. RF LABELS', styles['overline']))
    story.append(Paragraph('Disposable barcode labels', styles['h1']))
    story.append(AccentBar(50, 3))
    story.append(Spacer(1, 12))

    story.extend(make_product_section(
        styles,
        name='GF4040H Barcode RF Label',
        code='GF4040H',
        description=(
            '40 mm \u00d7 40 mm RF barcode label for high-volume retail. Century\u2019s optimised '
            'circuit design delivers superior detection range, and the unique dimpling '
            'deactivation process minimises reactivation. Available in multiple variants.'
        ),
        specs=[
            ('Frequency', '8.2 MHz (\u00b15%)'),
            ('Label Size', '40 mm \u00d7 40 mm'),
            ('Liner Width', '42 mm'),
            ('Packing', '1,000 pcs/roll, 20,000 pcs/carton'),
            ('Face Sheets', 'Thermal, transparent, barcode-printable'),
        ],
        features=[
            'Optimised circuit for extended detection range',
            'Unique dimpling process limits reactivation',
            'Compatible with standard RF deactivation pads',
            'Frozen-grade variant (GF4040H_FZ) available',
        ],
        img_path=PRODUCT_IMAGES['gf4040h'],
        price='0.02', unit='/pcs'
    ))

    # Variants table
    story.append(Paragraph('Available Variants', styles['h3']))
    v_data = [
        [Paragraph('<b>Code</b>', styles['spec_label']),
         Paragraph('<b>Type</b>', styles['spec_label']),
         Paragraph('<b>Application</b>', styles['spec_label'])],
        [Paragraph('GF4040H', styles['spec_value']),
         Paragraph('Standard barcode', styles['spec_value']),
         Paragraph('General retail, packaged goods', styles['spec_value'])],
        [Paragraph('GF4040H_NA', styles['spec_value']),
         Paragraph('Non-adhesive insertable', styles['spec_value']),
         Paragraph('Packaging inserts, hang tags', styles['spec_value'])],
        [Paragraph('GF4040H_CO', styles['spec_value']),
         Paragraph('Transparent', styles['spec_value']),
         Paragraph('Cosmetics, clear packaging', styles['spec_value'])],
        [Paragraph('GF4040H_FZ', styles['spec_value']),
         Paragraph('Frozen-grade', styles['spec_value']),
         Paragraph('Chilled and frozen products', styles['spec_value'])],
        [Paragraph('GF4040M', styles['spec_value']),
         Paragraph('Microwaveable', styles['spec_value']),
         Paragraph('Microwave-safe frozen food', styles['spec_value'])],
    ]
    vt = Table(v_data, colWidths=[95, 135, CONTENT_W - 250])
    vt.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 0), (-1, 0), CENTURY_NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, GRAY_50]),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, GRAY_200),
        ('BOX', (0, 0), (-1, -1), 0.5, GRAY_200),
    ]))
    story.append(vt)

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # SECTION 3: MULTI-ALARM SPIDER TAGS
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('3. MULTI-ALARM TAGS', styles['overline']))
    story.append(Paragraph('High-security alarming spider wraps', styles['h1']))
    story.append(AccentBar(50, 3))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        'Century\u2019s multi-alarm spider tags provide layered protection for high-value '
        'boxed merchandise. The expandable cables cinch tightly around products, with '
        'built-in alarms that trigger on tamper, removal, and store exit.',
        styles['body']
    ))

    # Alarm levels
    alarm_data = [
        [Paragraph('<b>Level</b>', styles['spec_label']),
         Paragraph('<b>Trigger</b>', styles['spec_label'])],
        [Paragraph('Self-alarm', styles['spec_value']),
         Paragraph('Merchandise taken outside the store', styles['spec_value'])],
        [Paragraph('System alarm', styles['spec_value']),
         Paragraph('Tag removed from merchandise while in store', styles['spec_value'])],
        [Paragraph('Tamper alarm', styles['spec_value']),
         Paragraph('Lanyard cut or tag physically tampered with', styles['spec_value'])],
    ]
    at = Table(alarm_data, colWidths=[100, CONTENT_W - 115])
    at.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 0), (-1, 0), CENTURY_NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, GRAY_50]),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, GRAY_200),
        ('BOX', (0, 0), (-1, -1), 0.5, GRAY_200),
    ]))
    story.append(at)
    story.append(Spacer(1, 14))

    # T504
    story.extend(make_product_section(
        styles,
        name='Baby Multi Grip \u2014 Small Spider',
        code='T504',
        description=(
            'Compact alarming spider wrap for small to medium boxed merchandise. '
            'Suited to electronics accessories, cosmetics, and smaller retail items.'
        ),
        specs=[
            ('Frequency', '8.2 MHz, 58 KHz, or dual'),
            ('Dimension', '\u00d850 mm \u00d7 47 mm'),
            ('Lock', 'Standard / Super'),
            ('Lanyard', '1.2 mm dia, 640 mm length'),
            ('Alarm', '\u226590 dB, \u22653 year battery'),
        ],
        features=[
            'Flashing LED visual deterrent',
            'Reusable one-piece design',
            'Easy to apply and remove at POS',
        ],
        img_path=PRODUCT_IMAGES['t504'],
        price='5.35', unit='/pcs'
    ))

    # T511
    story.extend(make_product_section(
        styles,
        name='Multi Grip \u2014 Large Spider',
        code='T511',
        description=(
            'Full-size alarming spider wrap for medium to large boxed merchandise. '
            'Designed for electronics, small appliances, and premium retail products.'
        ),
        specs=[
            ('Frequency', '8.2 MHz, 58 KHz, or dual'),
            ('Dimension', '\u00d873 mm \u00d7 50 mm'),
            ('Lock', 'Standard / Super'),
            ('Lanyard', '1.2 mm dia, 900/1,200 mm length'),
            ('Alarm', '\u226595 dB, \u22653 year battery'),
        ],
        features=[
            'Higher alarm volume (95 dB) for active deterrence',
            'Longer lanyard options for large-format boxes',
            'Excellent for open merchandising displays',
        ],
        img_path=PRODUCT_IMAGES['t511'],
        price='6.50', unit='/pcs'
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # SECTION 4: DETACHERS
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('4. DETACHERS', styles['overline']))
    story.append(Paragraph('Magnetic detachers for point of sale', styles['h1']))
    story.append(AccentBar(50, 3))
    story.append(Spacer(1, 12))

    # D104
    story.extend(make_product_section(
        styles,
        name='Slim Standard Detacher',
        code='D104',
        description=(
            'Compact countertop detacher for standard-lock tags. Slim profile '
            'minimises counter space. Compatible with all Century standard-lock tags.'
        ),
        specs=[
            ('Magnetic Force', '\u22654,500 GS'),
            ('Dimension', '\u00d853 mm \u00d7 37 mm'),
            ('Weight', '250 g'),
            ('Compatibility', 'All standard-lock tags'),
        ],
        features=[
            'Slim design for clean checkout counters',
            'Durable for high-volume retail',
            'Lockable with K09 key for overnight security',
        ],
        img_path=PRODUCT_IMAGES['d104'],
        price='18.50', unit='/pcs'
    ))

    # D204
    story.extend(make_product_section(
        styles,
        name='Slim Super Detacher',
        code='D204',
        description=(
            'High-strength magnetic detacher for super-lock tags. Same slim form '
            'factor as D104 with more than double the magnetic force.'
        ),
        specs=[
            ('Magnetic Force', '\u22659,500 GS'),
            ('Dimension', '\u00d853 mm \u00d7 37 mm'),
            ('Weight', '290 g'),
            ('Compatibility', 'All standard and super-lock tags'),
        ],
        features=[
            'Same slim profile as D104 \u2014 easy upgrade path',
            'Handles both standard and super-lock tags',
            'Lockable with K02 key for overnight security',
        ],
        img_path=PRODUCT_IMAGES['d204'],
        price='41.95', unit='/pcs'
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # SECTION 5: DETECTION ANTENNAS
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('5. DETECTION ANTENNAS', styles['overline']))
    story.append(Paragraph('EAS antenna pedestals', styles['h1']))
    story.append(AccentBar(50, 3))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        'EAS detection antennas are installed at store entry and exit points to detect '
        'active security tags and labels. These pedestal systems provide a visible '
        'deterrent and reliable alarm activation when tagged items leave without deactivation.',
        styles['body']
    ))
    story.append(Spacer(1, 8))

    # CA36L-G09
    story.extend(make_product_section(
        styles,
        name='EAS Detection Antenna \u2014 Wide Aisle',
        code='CA36L-G09',
        description=(
            'Extended-range antenna pedestal for wider store entrances and high-traffic '
            'environments. Broader coverage for wide door configurations or multi-lane '
            'entry points.'
        ),
        specs=[
            ('Type', 'RF antenna pedestal (extended range)'),
            ('Detection', '8.2 MHz RF tags and labels'),
            ('Installation', 'Floor-mounted, single or paired'),
            ('Finish', 'Slim acrylic, customisable branding panel'),
        ],
        features=[
            'Extended range for wider entrances',
            'Enhanced sensitivity for small-format labels',
            'Professional installation available through SLS RTC',
        ],
        price='930', unit='/unit'
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # SECTION 6: GUARDING
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('6. GUARDING SERVICES', styles['overline']))
    story.append(Paragraph('Uniformed retail security', styles['h1']))
    story.append(AccentBar(50, 3))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        'EAS hardware reduces opportunistic theft. But organised retail crime, staff '
        'safety, and customer experience require a physical presence. SLS RTC provides '
        'trained, uniformed security professionals who understand the retail environment.',
        styles['body']
    ))

    story.append(Spacer(1, 6))

    guard_features = [
        '<b>Trained retail security professionals</b> \u2014 customer service, de-escalation, '
        'and the balance between security presence and shopping experience',
        '<b>Consistent rostering</b> \u2014 the same team at your store, with GPS-verified '
        'attendance and digital check-ins',
        '<b>Incident reporting</b> \u2014 digital reports with photos, timestamps, and '
        'follow-up actions delivered to your inbox',
        '<b>Flexible scaling</b> \u2014 additional coverage for peak trading and holiday '
        'periods without weeks of lead time',
        '<b>Technology-enabled</b> \u2014 GPS-verified patrols, real-time dashboards, and '
        'workforce management systems',
    ]
    for f in guard_features:
        story.append(Paragraph(f'<bullet>&bull;</bullet> {f}', styles['bullet']))

    story.append(Spacer(1, 20))

    # Integration pitch
    story.append(Paragraph('THE COMPLETE PACKAGE', styles['overline']))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        'When the same company supplies the EAS tags on your merchandise, the detection '
        'system at your doors, and the security professional standing beside them \u2014 '
        'the gaps disappear. One team, one standard, one point of contact.',
        styles['body']
    ))

    # Integration flow
    int_cells = [
        Paragraph('<b>EAS Tags<br/>&amp; Labels</b>', ParagraphStyle(
            'ic1', fontName='Helvetica-Bold', fontSize=9, leading=13,
            textColor=WHITE, alignment=TA_CENTER)),
        Paragraph('\u2192', ParagraphStyle(
            'arr1', fontSize=16, alignment=TA_CENTER, textColor=CENTURY_BLUE)),
        Paragraph('<b>Detection<br/>Systems</b>', ParagraphStyle(
            'ic2', fontName='Helvetica-Bold', fontSize=9, leading=13,
            textColor=WHITE, alignment=TA_CENTER)),
        Paragraph('\u2192', ParagraphStyle(
            'arr2', fontSize=16, alignment=TA_CENTER, textColor=CENTURY_BLUE)),
        Paragraph('<b>Uniformed<br/>Guards</b>', ParagraphStyle(
            'ic3', fontName='Helvetica-Bold', fontSize=9, leading=13,
            textColor=WHITE, alignment=TA_CENTER)),
    ]

    int_table = Table([int_cells], colWidths=[120, 30, 120, 30, 120])
    int_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (0, 0), CENTURY_NAVY),
        ('BACKGROUND', (2, 0), (2, 0), CENTURY_BLUE),
        ('BACKGROUND', (4, 0), (4, 0), CENTURY_NAVY),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
    ]))
    story.append(Spacer(1, 12))
    story.append(int_table)

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # PRICING SUMMARY
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('PRICING SUMMARY', styles['overline']))
    story.append(Paragraph('Product pricing schedule', styles['h1']))
    story.append(AccentBar(50, 3))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        'All prices are in New Zealand Dollars (NZD), exclusive of GST. '
        'Pricing is subject to foreign exchange fluctuations and may be '
        'adjusted at time of order confirmation.',
        styles['body']
    ))
    story.append(Spacer(1, 8))

    price_header_style = ParagraphStyle(
        'ph', fontName='Helvetica-Bold', fontSize=8.5,
        leading=11, textColor=WHITE, alignment=TA_LEFT)
    price_val_style = ParagraphStyle(
        'pv', fontName='Helvetica', fontSize=9.5,
        leading=14, textColor=TEXT_DARK, alignment=TA_LEFT)
    price_num_style = ParagraphStyle(
        'pn', fontName='Helvetica-Bold', fontSize=10,
        leading=14, textColor=CENTURY_NAVY, alignment=TA_RIGHT)

    price_data = [
        [Paragraph('<b>Code</b>', price_header_style),
         Paragraph('<b>Product</b>', price_header_style),
         Paragraph('<b>Unit</b>', price_header_style),
         Paragraph('<b>NZD excl. GST</b>', ParagraphStyle(
             'phr', parent=price_header_style, alignment=TA_RIGHT))],
        [Paragraph('T001B + P01', price_val_style),
         Paragraph('Mini Square Tag + Flat Steel Pin', price_val_style),
         Paragraph('per set', price_val_style),
         Paragraph('$0.10', price_num_style)],
        [Paragraph('T213', price_val_style),
         Paragraph('Milli Lanyard Tag', price_val_style),
         Paragraph('per piece', price_val_style),
         Paragraph('$0.32', price_num_style)],
        [Paragraph('GF4040H', price_val_style),
         Paragraph('RF Barcode Label', price_val_style),
         Paragraph('per piece', price_val_style),
         Paragraph('$0.02', price_num_style)],
        [Paragraph('T504', price_val_style),
         Paragraph('Baby Multi Grip (Small Spider)', price_val_style),
         Paragraph('per piece', price_val_style),
         Paragraph('$5.35', price_num_style)],
        [Paragraph('T511', price_val_style),
         Paragraph('Multi Grip (Large Spider)', price_val_style),
         Paragraph('per piece', price_val_style),
         Paragraph('$6.50', price_num_style)],
        [Paragraph('D104', price_val_style),
         Paragraph('Slim Standard Detacher', price_val_style),
         Paragraph('per piece', price_val_style),
         Paragraph('$18.50', price_num_style)],
        [Paragraph('D204', price_val_style),
         Paragraph('Slim Super Detacher', price_val_style),
         Paragraph('per piece', price_val_style),
         Paragraph('$41.95', price_num_style)],
        [Paragraph('CA36L-G09', price_val_style),
         Paragraph('EAS Antenna \u2014 Wide Aisle', price_val_style),
         Paragraph('per unit', price_val_style),
         Paragraph('$930.00', price_num_style)],
    ]

    pt = Table(price_data, colWidths=[80, 190, 65, CONTENT_W - 355])
    pt.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (-1, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, 0), CENTURY_NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, GRAY_50]),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, GRAY_200),
        ('BOX', (0, 0), (-1, -1), 0.75, GRAY_200),
        ('LINEAFTER', (0, 0), (-2, -1), 0.25, GRAY_200),
    ]))
    story.append(pt)

    story.append(Spacer(1, 16))
    story.append(Paragraph(
        '<b>Notes:</b>',
        ParagraphStyle('notes_h', fontName='Helvetica-Bold', fontSize=9,
                       textColor=GRAY_600, spaceAfter=4)
    ))
    notes = [
        'All prices are in NZD and exclude GST (15%)',
        'Pricing is based on current exchange rates and subject to adjustment at order confirmation',
        'Volume discounts may apply \u2014 contact us for quantities above 10,000 units',
        'Freight and installation charges quoted separately',
        'Minimum order quantities may apply for certain products',
    ]
    for n in notes:
        story.append(Paragraph(
            f'<bullet>&bull;</bullet> {n}',
            ParagraphStyle('note', fontName='Helvetica', fontSize=8.5,
                           leading=13, textColor=GRAY_600, leftIndent=12,
                           bulletIndent=0, spaceBefore=0, spaceAfter=2)
        ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # BACK COVER
    # ══════════════════════════════════════════════════════════
    # Dark background via flowable
    class DarkBackground(Flowable):
        def __init__(self):
            super().__init__()
            self.width = 0
            self.height = 0
        def draw(self):
            c = self.canv
            c.saveState()
            c.setFillColor(CENTURY_NAVY)
            c.rect(-MARGIN_SIDE, -MARGIN_BOTTOM, PAGE_W, PAGE_H, fill=1, stroke=0)
            # Accent bar
            c.setFillColor(CENTURY_BLUE)
            c.rect(-MARGIN_SIDE, PAGE_H - MARGIN_BOTTOM - 6, PAGE_W, 6, fill=1, stroke=0)
            c.restoreState()

    story.append(DarkBackground())
    story.append(Spacer(1, 140))

    # SLS RTC logo on dark
    if os.path.exists(SLS_LOGO):
        logo = Image(SLS_LOGO, width=180, height=45)
        logo.hAlign = 'CENTER'
        story.append(logo)
        story.append(Spacer(1, 24))

    story.append(Paragraph(
        'Your EAS &amp; Retail Security Partner',
        ParagraphStyle('back_tag', fontName='Helvetica', fontSize=14,
                       leading=20, textColor=CENTURY_LIGHT_BLUE, alignment=TA_CENTER,
                       spaceAfter=40)
    ))

    # Divider
    story.append(HRFlowable(width='30%', thickness=0.5, color=HexColor('#2A4A7B'),
                             spaceBefore=0, spaceAfter=30, hAlign='CENTER'))

    # Contact
    contact_s = ParagraphStyle(
        'back_contact', fontName='Helvetica', fontSize=11,
        leading=18, textColor=HexColor('#8BA4C8'), alignment=TA_CENTER, spaceAfter=4
    )
    story.append(Paragraph('Mark Clansey  |  General Manager', contact_s))
    story.append(Paragraph('021 879 664  |  mark@slsrtc.co.nz',
                           ParagraphStyle('bc2', parent=contact_s, fontSize=10)))
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        'www.slsrtc.co.nz',
        ParagraphStyle('back_url', fontName='Helvetica-Bold', fontSize=13,
                       leading=18, textColor=WHITE, alignment=TA_CENTER)
    ))

    # ── Build ──────────────────────────────────────────────────
    doc.build(story, onFirstPage=draw_cover, onLaterPages=draw_content_page)
    print(f'Proposal generated: {OUTPUT_PATH}')


if __name__ == '__main__':
    build()
