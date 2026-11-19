#!/usr/bin/env python3
"""
ASG Security — Retail EAS Product Brochure
For Ngahuia Group / Outlet Stores meeting (10 April 2026)
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
import os

# ── Brand Colours ──────────────────────────────────────────────
MIDNIGHT = HexColor('#050A14')
DEEP = HexColor('#0B1221')
NAVY = HexColor('#111B2E')
STEEL = HexColor('#1A2744')
SIGNAL_BLUE = HexColor('#2563EB')
WHITE = HexColor('#FFFFFF')
GRAY_100 = HexColor('#F1F5F9')
GRAY_200 = HexColor('#E2E8F0')
GRAY_400 = HexColor('#94A3B8')
GRAY_500 = HexColor('#64748B')
EMERALD = HexColor('#10B981')
AMBER = HexColor('#F59E0B')

# ── Page Setup ─────────────────────────────────────────────────
PAGE_W, PAGE_H = A4
MARGIN_SIDE = 54
MARGIN_TOP = 62
MARGIN_BOTTOM = 54
CONTENT_W = PAGE_W - 2 * MARGIN_SIDE

OUTPUT_PATH = os.path.expanduser('~/Desktop/Clients/ASG/brochures/ASG_EAS_Product_Brochure_2026.pdf')


# ── Styles ─────────────────────────────────────────────────────
def make_styles():
    s = {}
    s['title_hero'] = ParagraphStyle(
        'title_hero', fontName='Helvetica-Bold', fontSize=36,
        leading=40, textColor=WHITE, alignment=TA_LEFT,
        spaceAfter=8
    )
    s['subtitle_hero'] = ParagraphStyle(
        'subtitle_hero', fontName='Helvetica', fontSize=14,
        leading=20, textColor=GRAY_400, alignment=TA_LEFT,
        spaceAfter=0
    )
    s['tagline'] = ParagraphStyle(
        'tagline', fontName='Helvetica', fontSize=11,
        leading=16, textColor=SIGNAL_BLUE, alignment=TA_LEFT,
        spaceBefore=16, spaceAfter=0, tracking=0.3
    )
    s['h1'] = ParagraphStyle(
        'h1', fontName='Helvetica-Bold', fontSize=24,
        leading=29, textColor=MIDNIGHT, alignment=TA_LEFT,
        spaceBefore=0, spaceAfter=12
    )
    s['h2'] = ParagraphStyle(
        'h2', fontName='Helvetica-Bold', fontSize=16,
        leading=21, textColor=MIDNIGHT, alignment=TA_LEFT,
        spaceBefore=18, spaceAfter=8
    )
    s['h2_white'] = ParagraphStyle(
        'h2_white', fontName='Helvetica-Bold', fontSize=16,
        leading=21, textColor=WHITE, alignment=TA_LEFT,
        spaceBefore=18, spaceAfter=8
    )
    s['h3'] = ParagraphStyle(
        'h3', fontName='Helvetica-Bold', fontSize=13,
        leading=17, textColor=MIDNIGHT, alignment=TA_LEFT,
        spaceBefore=12, spaceAfter=4
    )
    s['overline'] = ParagraphStyle(
        'overline', fontName='Helvetica-Bold', fontSize=9,
        leading=12, textColor=SIGNAL_BLUE, alignment=TA_LEFT,
        spaceBefore=0, spaceAfter=4
    )
    s['body'] = ParagraphStyle(
        'body', fontName='Helvetica', fontSize=10,
        leading=16, textColor=HexColor('#333333'), alignment=TA_JUSTIFY,
        spaceBefore=0, spaceAfter=8
    )
    s['body_white'] = ParagraphStyle(
        'body_white', fontName='Helvetica', fontSize=10,
        leading=16, textColor=GRAY_200, alignment=TA_JUSTIFY,
        spaceBefore=0, spaceAfter=8
    )
    s['body_small'] = ParagraphStyle(
        'body_small', fontName='Helvetica', fontSize=9,
        leading=13, textColor=GRAY_500, alignment=TA_LEFT,
        spaceBefore=0, spaceAfter=4
    )
    s['spec_label'] = ParagraphStyle(
        'spec_label', fontName='Helvetica-Bold', fontSize=8.5,
        leading=11, textColor=GRAY_500, alignment=TA_LEFT,
    )
    s['spec_value'] = ParagraphStyle(
        'spec_value', fontName='Helvetica', fontSize=9,
        leading=12, textColor=MIDNIGHT, alignment=TA_LEFT,
    )
    s['stat_number'] = ParagraphStyle(
        'stat_number', fontName='Helvetica-Bold', fontSize=32,
        leading=36, textColor=SIGNAL_BLUE, alignment=TA_CENTER,
        spaceBefore=0, spaceAfter=2
    )
    s['stat_label'] = ParagraphStyle(
        'stat_label', fontName='Helvetica', fontSize=9,
        leading=12, textColor=GRAY_500, alignment=TA_CENTER,
        spaceBefore=0, spaceAfter=0
    )
    s['footer'] = ParagraphStyle(
        'footer', fontName='Helvetica', fontSize=7.5,
        leading=10, textColor=GRAY_400, alignment=TA_CENTER,
    )
    s['product_name'] = ParagraphStyle(
        'product_name', fontName='Helvetica-Bold', fontSize=12,
        leading=15, textColor=MIDNIGHT, alignment=TA_LEFT,
        spaceBefore=0, spaceAfter=2
    )
    s['product_code'] = ParagraphStyle(
        'product_code', fontName='Helvetica', fontSize=9,
        leading=12, textColor=SIGNAL_BLUE, alignment=TA_LEFT,
        spaceBefore=0, spaceAfter=6
    )
    s['bullet'] = ParagraphStyle(
        'bullet', fontName='Helvetica', fontSize=9.5,
        leading=14, textColor=HexColor('#333333'), alignment=TA_LEFT,
        leftIndent=12, spaceBefore=0, spaceAfter=3, bulletIndent=0,
    )
    return s


# ── Custom Page Templates ──────────────────────────────────────
class BrochureDocTemplate(SimpleDocTemplate):
    def __init__(self, *args, **kwargs):
        self.page_type = 'normal'
        super().__init__(*args, **kwargs)


def draw_cover_page(c, doc):
    """Full midnight cover with brand elements."""
    w, h = PAGE_W, PAGE_H
    # Full midnight background
    c.setFillColor(MIDNIGHT)
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # Subtle gradient accent bar at top
    c.setFillColor(SIGNAL_BLUE)
    c.rect(0, h - 4, w, 4, fill=1, stroke=0)

    # Decorative line elements
    c.setStrokeColor(HexColor('#1A2744'))
    c.setLineWidth(0.5)
    c.line(MARGIN_SIDE, h - 120, w - MARGIN_SIDE, h - 120)

    # Logo area: ASG | SECURITY
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 42)
    c.drawString(MARGIN_SIDE, h - 100, 'ASG')
    # Separator
    c.setStrokeColor(HexColor('#FFFFFF40'))
    c.setLineWidth(1)
    c.line(MARGIN_SIDE + 108, h - 108, MARGIN_SIDE + 108, h - 78)
    # SECURITY text
    c.setFont('Helvetica', 16)
    c.setFillColor(GRAY_400)
    x_sec = MARGIN_SIDE + 118
    security_text = 'S E C U R I T Y'
    c.drawString(x_sec, h - 96, security_text)

    # Footer
    c.setFillColor(GRAY_500)
    c.setFont('Helvetica', 8)
    c.drawString(MARGIN_SIDE, 40, 'asgsecurity.co.nz')
    c.drawRightString(w - MARGIN_SIDE, 40, 'Confidential')

    # Bottom accent line
    c.setStrokeColor(SIGNAL_BLUE)
    c.setLineWidth(0.75)
    c.line(MARGIN_SIDE, 55, w - MARGIN_SIDE, 55)


def draw_normal_page(c, doc):
    """Standard content page with header and footer."""
    w, h = PAGE_W, PAGE_H

    # Top bar
    c.setFillColor(MIDNIGHT)
    c.rect(0, h - 28, w, 28, fill=1, stroke=0)
    c.setFillColor(GRAY_400)
    c.setFont('Helvetica', 7.5)
    c.drawString(MARGIN_SIDE, h - 19, 'ASG Security  |  Retail Loss Prevention & EAS Product Catalogue')
    c.setFillColor(SIGNAL_BLUE)
    c.drawRightString(w - MARGIN_SIDE, h - 19, 'asgsecurity.co.nz')

    # Footer line
    c.setStrokeColor(GRAY_200)
    c.setLineWidth(0.5)
    c.line(MARGIN_SIDE, 38, w - MARGIN_SIDE, 38)

    # Page number
    c.setFillColor(GRAY_500)
    c.setFont('Helvetica', 8)
    c.drawCentredString(w / 2, 25, str(doc.page))


def draw_dark_page(c, doc):
    """Dark background page."""
    w, h = PAGE_W, PAGE_H
    c.setFillColor(MIDNIGHT)
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # Accent bar
    c.setFillColor(SIGNAL_BLUE)
    c.rect(0, h - 3, w, 3, fill=1, stroke=0)

    # Footer
    c.setStrokeColor(STEEL)
    c.setLineWidth(0.5)
    c.line(MARGIN_SIDE, 38, w - MARGIN_SIDE, 38)
    c.setFillColor(GRAY_500)
    c.setFont('Helvetica', 8)
    c.drawCentredString(w / 2, 25, str(doc.page))


# ── Helper: Product Card ──────────────────────────────────────
def make_product_card(styles, name, code, description, specs, features):
    """Build a product card as a list of flowables."""
    elements = []

    # Overline
    elements.append(Paragraph(code.upper(), styles['overline']))
    # Product name
    elements.append(Paragraph(name, styles['product_name']))
    # Description
    elements.append(Paragraph(description, styles['body']))

    # Specs table
    if specs:
        spec_data = []
        for label, value in specs:
            spec_data.append([
                Paragraph(f'<b>{label}</b>', styles['spec_label']),
                Paragraph(value, styles['spec_value']),
            ])
        t = Table(spec_data, colWidths=[120, CONTENT_W - 140])
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
        elements.append(Spacer(1, 6))
        for f in features:
            elements.append(Paragraph(f'<bullet>&bull;</bullet> {f}', styles['bullet']))

    # Bottom divider
    elements.append(Spacer(1, 8))
    elements.append(HRFlowable(width='100%', thickness=0.5, color=GRAY_200,
                               spaceBefore=0, spaceAfter=16))

    return elements


# ── Build Document ─────────────────────────────────────────────
def build():
    styles = make_styles()

    doc = BrochureDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=MARGIN_SIDE,
        rightMargin=MARGIN_SIDE,
        topMargin=MARGIN_TOP + 28,  # account for header bar
        bottomMargin=MARGIN_BOTTOM,
    )

    story = []

    # ══════════════════════════════════════════════════════════
    # PAGE 1: COVER
    # ══════════════════════════════════════════════════════════
    # We'll use a custom approach: add spacers to position text on the cover
    story.append(Spacer(1, 160))
    story.append(Paragraph(
        'RETAIL LOSS PREVENTION',
        ParagraphStyle('cover_overline', fontName='Helvetica-Bold', fontSize=11,
                       leading=14, textColor=SIGNAL_BLUE, spaceAfter=8,
                       tracking=0.15)
    ))
    story.append(Paragraph(
        'EAS Product<br/>Catalogue',
        styles['title_hero']
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        'Electronic Article Surveillance tags, labels, detachers,<br/>'
        'and detection systems for retail environments.',
        styles['subtitle_hero']
    ))
    story.append(Spacer(1, 24))
    story.append(Paragraph(
        'Complete Security. One Partner.',
        styles['tagline']
    ))

    # Prepared for line
    story.append(Spacer(1, 80))
    story.append(Paragraph(
        'Prepared for Ngahuia Group  |  Outlet Stores',
        ParagraphStyle('prep', fontName='Helvetica', fontSize=10,
                       leading=14, textColor=GRAY_500, spaceAfter=4)
    ))
    story.append(Paragraph(
        'April 2026',
        ParagraphStyle('date', fontName='Helvetica', fontSize=10,
                       leading=14, textColor=GRAY_500)
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # PAGE 2: ABOUT ASG SECURITY
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('ABOUT ASG SECURITY', styles['overline']))
    story.append(Paragraph('One company. Four service lines.<br/>Zero gaps.', styles['h1']))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        'ASG Security is a New Zealand-owned security services company operating across '
        '9 regions with 300+ security professionals. We deliver four integrated service lines '
        'under one brand: uniformed guarding for hospitality, venues, and commercial clients; '
        'covert retail loss prevention for national retail chains; remote CCTV monitoring and '
        'CBD safety patrols; and integrated electronic security systems.',
        styles['body']
    ))
    story.append(Paragraph(
        'One contract, one standard, one point of accountability. Headquartered in Auckland.',
        ParagraphStyle('body_bold', fontName='Helvetica-Bold', fontSize=10,
                       leading=16, textColor=HexColor('#333333'), spaceAfter=16)
    ))

    # Stats row
    stats = [
        ('300+', 'Security\nProfessionals'),
        ('9', 'Regions\nNationally'),
        ('4', 'Integrated\nService Lines'),
        ('24/7', 'Operations\nCoverage'),
    ]
    stat_cells = []
    for num, label in stats:
        cell = [
            Paragraph(num, styles['stat_number']),
            Paragraph(label.replace('\n', '<br/>'), styles['stat_label']),
        ]
        stat_cells.append(cell)

    col_w = CONTENT_W / 4
    stat_table = Table(
        [stat_cells],
        colWidths=[col_w] * 4,
        rowHeights=[80],
    )
    stat_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOX', (0, 0), (-1, -1), 0.5, GRAY_200),
        ('LINEBEFORE', (1, 0), (-1, -1), 0.5, GRAY_200),
        ('BACKGROUND', (0, 0), (-1, -1), GRAY_100),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
    ]))
    story.append(stat_table)
    story.append(Spacer(1, 20))

    # Key clients
    story.append(Paragraph('TRUSTED BY', styles['overline']))
    story.append(Paragraph(
        'Woolworths NZ  &nbsp;&nbsp;|&nbsp;&nbsp;  Bunnings  &nbsp;&nbsp;|&nbsp;&nbsp;  '
        'The Warehouse  &nbsp;&nbsp;|&nbsp;&nbsp;  Noel Leeming',
        ParagraphStyle('clients', fontName='Helvetica-Bold', fontSize=11,
                       leading=16, textColor=MIDNIGHT, spaceAfter=16)
    ))

    story.append(Spacer(1, 12))
    story.append(Paragraph('THE PROBLEM', styles['overline']))
    story.append(Paragraph(
        'Most retailers manage security across multiple vendors. One company handles '
        'the guards, another supplies the EAS tags, a third maintains the detection systems. '
        'Nobody owns the full picture. When shrinkage persists, the finger-pointing begins.',
        styles['body']
    ))
    story.append(Paragraph(
        'ASG Security eliminates that fragmentation. We supply and support the EAS hardware, '
        'deploy the covert loss prevention operatives, and provide the uniformed guarding \u2014 '
        'all under a single contract with a single point of accountability.',
        styles['body']
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # PAGE 3: EAS OVERVIEW
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('EAS PRODUCT RANGE', styles['overline']))
    story.append(Paragraph('Electronic Article Surveillance', styles['h1']))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        'We supply a complete range of Century EAS products \u2014 from disposable RF labels and '
        'reusable hard tags through to multi-alarm spider wraps and detection antennas. '
        'Century (Hangzhou Century Co., Ltd) is a publicly listed manufacturer '
        '(Shenzhen Stock Exchange, 300078.SZ) and one of the world\u2019s largest EAS producers, '
        'serving major retailers globally.',
        styles['body']
    ))
    story.append(Spacer(1, 4))

    # Category overview table
    cat_data = [
        [
            Paragraph('<b>Category</b>', styles['spec_label']),
            Paragraph('<b>Products</b>', styles['spec_label']),
            Paragraph('<b>Application</b>', styles['spec_label']),
        ],
        [
            Paragraph('Hard Tags', styles['spec_value']),
            Paragraph('Mini Square (T001B), Milli Lanyard (T213)', styles['spec_value']),
            Paragraph('Apparel, soft goods, accessories', styles['spec_value']),
        ],
        [
            Paragraph('RF Labels', styles['spec_value']),
            Paragraph('GF4040H Barcode Label', styles['spec_value']),
            Paragraph('Packaged goods, cosmetics, electronics', styles['spec_value']),
        ],
        [
            Paragraph('Multi-Alarm Tags', styles['spec_value']),
            Paragraph('Baby Spider (T504), Spider (T511)', styles['spec_value']),
            Paragraph('High-value boxed merchandise', styles['spec_value']),
        ],
        [
            Paragraph('Detachers', styles['spec_value']),
            Paragraph('Standard (D104), Super (D204)', styles['spec_value']),
            Paragraph('Point-of-sale tag removal', styles['spec_value']),
        ],
        [
            Paragraph('Detection Systems', styles['spec_value']),
            Paragraph('Antenna Pedestals (CA35L, CA36L)', styles['spec_value']),
            Paragraph('Store entry/exit monitoring', styles['spec_value']),
        ],
    ]
    cat_table = Table(cat_data, colWidths=[110, 180, CONTENT_W - 310])
    cat_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 0), (-1, 0), MIDNIGHT),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, GRAY_100]),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, GRAY_200),
        ('BOX', (0, 0), (-1, -1), 0.5, GRAY_200),
    ]))
    story.append(cat_table)

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # PAGE 4-5: PRODUCT DETAILS — HARD TAGS
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('HARD TAGS', styles['overline']))
    story.append(Paragraph('Reusable security tags for apparel and soft goods', styles['h1']))
    story.append(Spacer(1, 8))

    # T001B + P01
    story.extend(make_product_card(
        styles,
        name='Mini Square Hard Tag + Flat Steel Pin',
        code='T001B + P01',
        description=(
            'Compact, low-profile hard tag paired with a flat steel pin. The Mini Square is '
            'one of the most widely deployed EAS tags in retail, suitable for a broad range of '
            'apparel and soft goods. Standard or super lock options provide flexibility across '
            'risk profiles.'
        ),
        specs=[
            ('Frequency', '8.2 MHz'),
            ('Dimension', '51.5 mm \u00d7 42 mm'),
            ('Lock Options', 'Standard / Super / Super S / Hyper'),
            ('Colour', 'Black, White, or customised'),
            ('Pin (P01)', 'Flat steel, 16/19/21 mm length, groove or smooth'),
        ],
        features=[
            'Low-profile design minimises impact on merchandise display',
            'Multiple lock strengths for tiered security',
            'Compatible with standard and super magnetic detachers',
            'Sold as a set \u2014 tag and pin supplied together',
        ]
    ))

    # T213
    story.extend(make_product_card(
        styles,
        name='Milli Lanyard Tag',
        code='T213',
        description=(
            'A slim, compact lanyard tag designed for items where pin attachment is not suitable. '
            'The integrated lanyard loop secures to merchandise without puncturing fabric, making '
            'it ideal for accessories, knitwear, and delicate garments.'
        ),
        specs=[
            ('Frequency', '8.2 MHz / 58 KHz'),
            ('Dimension', '48 mm \u00d7 13.5 mm'),
            ('Pin', '14 mm'),
            ('Lanyard', '90 mm'),
            ('Lock Options', 'Standard / Super'),
            ('Colour', 'Grey, Beige, or customised'),
        ],
        features=[
            'Non-piercing attachment \u2014 no marks left on merchandise',
            'Slim profile suits small or delicate items',
            'Dual-frequency options available',
            'Supplied with lanyard attached',
        ]
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # PAGE 5: RF LABELS
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('RF LABELS', styles['overline']))
    story.append(Paragraph('Disposable barcode labels for source tagging', styles['h1']))
    story.append(Spacer(1, 8))

    story.extend(make_product_card(
        styles,
        name='GF4040H Barcode RF Label',
        code='GF4040H',
        description=(
            'A 40 mm \u00d7 40 mm RF barcode label designed for high-volume retail environments. '
            'Century\u2019s optimised circuit design delivers superior detection range through a '
            'higher Q factor, while the unique dimpling deactivation process minimises '
            'reactivation. Available in multiple face sheet options including thermal '
            'printable, transparent, and frozen-grade variants.'
        ),
        specs=[
            ('Frequency', '8.2 MHz (\u00b15%)'),
            ('Label Size', '40 mm \u00d7 40 mm'),
            ('Liner Width', '42 mm'),
            ('Packing', '1,000 pcs/roll, 20,000 pcs/carton'),
            ('Face Sheet Options', 'Thermal, transparent, barcode-printable'),
        ],
        features=[
            'Optimised circuit design for extended detection range',
            'Unique dimpling process limits reactivation after deactivation',
            'Compatible with standard RF deactivation pads at checkout',
            'Available in frozen-grade (GF4040H_FZ) for chilled/frozen merchandise',
            'Auto-applied variant (GF4040H/PS) available for production-line integration',
        ]
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph('AVAILABLE VARIANTS', styles['overline']))

    variant_data = [
        [
            Paragraph('<b>Code</b>', styles['spec_label']),
            Paragraph('<b>Variant</b>', styles['spec_label']),
            Paragraph('<b>Application</b>', styles['spec_label']),
        ],
        [
            Paragraph('GF4040H', styles['spec_value']),
            Paragraph('Standard barcode', styles['spec_value']),
            Paragraph('General retail, packaged goods', styles['spec_value']),
        ],
        [
            Paragraph('GF4040H_NA', styles['spec_value']),
            Paragraph('Non-adhesive insertable', styles['spec_value']),
            Paragraph('Insert into packaging or hang tags', styles['spec_value']),
        ],
        [
            Paragraph('GF4040H_CO', styles['spec_value']),
            Paragraph('Transparent', styles['spec_value']),
            Paragraph('Cosmetics, clear packaging', styles['spec_value']),
        ],
        [
            Paragraph('GF4040H_FZ', styles['spec_value']),
            Paragraph('Frozen-grade', styles['spec_value']),
            Paragraph('Chilled and frozen products', styles['spec_value']),
        ],
        [
            Paragraph('GF4040M', styles['spec_value']),
            Paragraph('Microwaveable frozen', styles['spec_value']),
            Paragraph('Microwave-safe frozen food', styles['spec_value']),
        ],
    ]
    v_table = Table(variant_data, colWidths=[100, 150, CONTENT_W - 270])
    v_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 0), (-1, 0), MIDNIGHT),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, GRAY_100]),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, GRAY_200),
        ('BOX', (0, 0), (-1, -1), 0.5, GRAY_200),
    ]))
    story.append(v_table)

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # PAGE 6: MULTI-ALARM SPIDER TAGS
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('MULTI-ALARM TAGS', styles['overline']))
    story.append(Paragraph('High-security alarming spider wraps', styles['h1']))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        'Century\u2019s multi-alarm spider tags provide layered protection for high-value boxed '
        'merchandise. The expandable cable wraps cinch tightly around products, and the '
        'built-in alarm system triggers on tamper, tag removal, and store exit \u2014 providing '
        'up to 4 levels of alarm protection.',
        styles['body']
    ))

    # 4-alarm explanation
    alarm_data = [
        [
            Paragraph('<b>Alarm Level</b>', styles['spec_label']),
            Paragraph('<b>Trigger</b>', styles['spec_label']),
        ],
        [
            Paragraph('1. Self-alarm', styles['spec_value']),
            Paragraph('Merchandise taken outside the store', styles['spec_value']),
        ],
        [
            Paragraph('2. System alarm', styles['spec_value']),
            Paragraph('Tag removed from merchandise while still in store', styles['spec_value']),
        ],
        [
            Paragraph('3. Tamper alarm', styles['spec_value']),
            Paragraph('Lanyard cut or tag physically tampered with', styles['spec_value']),
        ],
        [
            Paragraph('4. Deactivation alarm', styles['spec_value']),
            Paragraph('Tag released before deactivation by authorised decoder', styles['spec_value']),
        ],
    ]
    alarm_table = Table(alarm_data, colWidths=[120, CONTENT_W - 140])
    alarm_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 0), (-1, 0), MIDNIGHT),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, GRAY_100]),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, GRAY_200),
        ('BOX', (0, 0), (-1, -1), 0.5, GRAY_200),
    ]))
    story.append(alarm_table)
    story.append(Spacer(1, 16))

    # T504
    story.extend(make_product_card(
        styles,
        name='Baby Multi Grip \u2014 Small Spider',
        code='T504',
        description=(
            'Compact alarming spider wrap for small to medium boxed merchandise. The smaller '
            'form factor suits electronics accessories, cosmetics boxes, and smaller retail items '
            'while providing the same multi-alarm protection as the full-size spider.'
        ),
        specs=[
            ('Frequency', '8.2 MHz, 58 KHz, or dual (8.2 MHz + 58 KHz)'),
            ('Dimension', '\u00d850 mm \u00d7 47 mm'),
            ('Lock Options', 'Standard / Super'),
            ('Lanyard Diameter', '1.2 mm'),
            ('Lanyard Length', '640 mm'),
            ('Alarm Volume', '\u226590 dB'),
            ('Battery Life', '\u22653 years'),
            ('Colour', 'Black, Grey, or customised'),
        ],
        features=[
            'Century 2-alarm technology (self-alarm + system alarm)',
            'Flashing LED creates a strong visual deterrent',
            'Auto-retractable lanyard for easy application',
            'Reusable one-piece design',
        ]
    ))

    # T511
    story.extend(make_product_card(
        styles,
        name='Multi Grip \u2014 Large Spider',
        code='T511',
        description=(
            'Full-size alarming spider wrap for medium to large boxed merchandise. Designed for '
            'high-value items such as electronics, small appliances, and premium retail products. '
            'The expanded lanyard reach secures larger box formats securely.'
        ),
        specs=[
            ('Frequency', '8.2 MHz, 58 KHz, or dual (8.2 MHz + 58 KHz)'),
            ('Dimension', '\u00d873 mm \u00d7 50 mm'),
            ('Lock Options', 'Standard / Super'),
            ('Lanyard Diameter', '1.2 mm'),
            ('Lanyard Length', '900 mm or 1,200 mm'),
            ('Alarm Volume', '\u226595 dB'),
            ('Battery Life', '\u22653 years'),
            ('Colour', 'Black, Grey, or customised'),
        ],
        features=[
            'Century multi-alarm technology (up to 2A protection)',
            'Higher alarm volume (95 dB) for active deterrence',
            'Longer lanyard options for large-format merchandise',
            'Easy to apply and remove at point of sale',
            'Excellent for open merchandising displays',
        ]
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # PAGE 7: DETACHERS
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('DETACHERS', styles['overline']))
    story.append(Paragraph('Magnetic detachers for point-of-sale operations', styles['h1']))
    story.append(Spacer(1, 8))

    # D104
    story.extend(make_product_card(
        styles,
        name='Slim Standard Detacher',
        code='D104',
        description=(
            'Compact countertop detacher for standard-lock hard tags. The slim profile '
            'minimises counter space usage while providing reliable tag removal at the '
            'point of sale. Compatible with all Century standard-lock tags.'
        ),
        specs=[
            ('Magnetic Force', '\u22654,500 GS'),
            ('Dimension', '\u00d853 mm \u00d7 37 mm'),
            ('Weight', '250 g'),
            ('Compatibility', 'All standard-lock tags (T001B, T213, and more)'),
        ],
        features=[
            'Slim, low-profile design for clean checkout counters',
            'Suitable for standard-lock security across all tag types',
            'Durable construction for high-volume retail use',
            'Lockable with K09 key for overnight security',
        ]
    ))

    # D204
    story.extend(make_product_card(
        styles,
        name='Slim Super Detacher',
        code='D204',
        description=(
            'High-strength magnetic detacher for super-lock tags. Same slim form factor as the '
            'D104 but with more than double the magnetic force, enabling removal of high-security '
            'super-lock tags used on premium merchandise.'
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
            'Higher magnetic force for premium security tag ranges',
            'Lockable with K02 key for overnight security',
        ]
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # PAGE 8: EAS ANTENNAS
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('DETECTION SYSTEMS', styles['overline']))
    story.append(Paragraph('EAS antenna pedestals for store protection', styles['h1']))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        'EAS detection antennas are installed at store entry and exit points to detect '
        'active security tags and labels as merchandise passes through. These pedestal-style '
        'systems provide a visible deterrent and reliable alarm activation when tagged items '
        'leave the store without deactivation.',
        styles['body']
    ))
    story.append(Spacer(1, 8))

    # CA35L-G09
    story.extend(make_product_card(
        styles,
        name='EAS Detection Antenna \u2014 Standard',
        code='CA35L-G09',
        description=(
            'Slim-profile EAS antenna pedestal for standard retail store configurations. '
            'Designed for single or dual-aisle deployment at entry/exit points. Detects both '
            'RF (8.2 MHz) hard tags and labels with reliable range across standard door widths.'
        ),
        specs=[
            ('Type', 'RF detection antenna pedestal'),
            ('Detection', '8.2 MHz RF tags and labels'),
            ('Installation', 'Floor-mounted, single or paired configuration'),
            ('Finish', 'Slim acrylic pedestal, customisable branding panel'),
        ],
        features=[
            'Reliable detection across standard retail door widths',
            'Slim pedestal design suits modern store aesthetics',
            'Compatible with all Century RF hard tags and labels',
            'Visual and audible alarm on detection',
        ]
    ))

    # CA36L-G09
    story.extend(make_product_card(
        styles,
        name='EAS Detection Antenna \u2014 Wide Aisle',
        code='CA36L-G09',
        description=(
            'Extended-range EAS antenna pedestal for wider store entrances and high-traffic '
            'retail environments. Delivers broader detection coverage for stores with wider '
            'door configurations or multi-lane entry points.'
        ),
        specs=[
            ('Type', 'RF detection antenna pedestal (extended range)'),
            ('Detection', '8.2 MHz RF tags and labels'),
            ('Installation', 'Floor-mounted, single or paired configuration'),
            ('Finish', 'Slim acrylic pedestal, customisable branding panel'),
        ],
        features=[
            'Extended detection range for wider store entrances',
            'Suitable for high-traffic, multi-lane entry points',
            'Enhanced sensitivity for small-format labels (GF4040H)',
            'Professional installation and commissioning available through ASG',
        ]
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # PAGE 9: GUARDING CAPABILITY
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('UNIFORMED GUARDING', styles['overline']))
    story.append(Paragraph('Retail security presence that represents your brand', styles['h1']))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        'EAS hardware reduces opportunistic theft. But organised retail crime, staff safety, '
        'and customer experience require a physical presence. ASG Security provides trained, '
        'uniformed security professionals who understand the retail environment \u2014 not a '
        'staffing agency sending warm bodies to fill a roster.',
        styles['body']
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph('What we deliver', styles['h2']))

    guard_features = [
        ('<b>Trained retail security professionals</b> \u2014 our people understand customer '
         'service, de-escalation, and the balance between security presence and shopping '
         'experience'),
        ('<b>Consistent rostering</b> \u2014 the same faces at your store, not a revolving door '
         'of strangers. GPS-verified attendance so you know who showed up and when'),
        ('<b>Incident reporting before you ask</b> \u2014 digital incident reports with photos, '
         'timestamps, and follow-up actions. Delivered to your inbox, not filed in a folder '
         'nobody reads'),
        ('<b>Flexible scaling</b> \u2014 additional coverage for peak trading, holiday periods, '
         'or specific risk events without weeks of lead time'),
        ('<b>Technology-enabled verification</b> \u2014 GuardForce WFM platform provides '
         'GPS-verified patrols, digital check-ins, and real-time dashboards'),
    ]
    for f in guard_features:
        story.append(Paragraph(f'<bullet>&bull;</bullet> {f}', styles['bullet']))

    story.append(Spacer(1, 16))
    story.append(Paragraph('THE INTEGRATED ADVANTAGE', styles['overline']))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        'When the same company supplies the EAS tags on your merchandise, the detection system '
        'at your doors, and the security professional standing beside them \u2014 the gaps disappear. '
        'Your guard knows which products are tagged, how the alarm system works, and what the '
        'escalation protocol is. That\u2019s not three vendors coordinating by email. That\u2019s one '
        'team, one standard.',
        styles['body']
    ))

    # Integration diagram as a simple table
    int_data = [
        [
            Paragraph('<b>EAS Tags &amp; Labels</b><br/>Product protection', styles['body_small']),
            Paragraph('\u2192', ParagraphStyle('arrow', fontSize=18, alignment=TA_CENTER,
                                               textColor=SIGNAL_BLUE)),
            Paragraph('<b>Detection Systems</b><br/>Alarm at exit', styles['body_small']),
            Paragraph('\u2192', ParagraphStyle('arrow', fontSize=18, alignment=TA_CENTER,
                                               textColor=SIGNAL_BLUE)),
            Paragraph('<b>Uniformed Guards</b><br/>Response &amp; deterrence', styles['body_small']),
        ]
    ]
    int_table = Table(int_data, colWidths=[130, 30, 130, 30, 130])
    int_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (0, 0), GRAY_100),
        ('BACKGROUND', (2, 0), (2, 0), GRAY_100),
        ('BACKGROUND', (4, 0), (4, 0), GRAY_100),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BOX', (0, 0), (0, 0), 0.5, GRAY_200),
        ('BOX', (2, 0), (2, 0), 0.5, GRAY_200),
        ('BOX', (4, 0), (4, 0), 0.5, GRAY_200),
    ]))
    story.append(Spacer(1, 8))
    story.append(int_table)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        'All under ASG Security. One contract. One standard. One point of accountability.',
        ParagraphStyle('integrated_cta', fontName='Helvetica-Bold', fontSize=11,
                       leading=16, textColor=SIGNAL_BLUE, alignment=TA_CENTER,
                       spaceBefore=8, spaceAfter=0)
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # PAGE 10: BACK COVER (drawn via custom flowable)
    # ══════════════════════════════════════════════════════════
    from reportlab.platypus import Flowable

    class DarkPageBackground(Flowable):
        """Draws a full-page dark background, overwriting the normal header."""
        def __init__(self):
            super().__init__()
            self.width = 0
            self.height = 0
        def draw(self):
            c = self.canv
            w, h = PAGE_W, PAGE_H
            # Full midnight background (covers the normal header)
            c.saveState()
            # Draw relative to absolute page coordinates
            # Current position is at top of frame, need to cover whole page
            frame_x = -MARGIN_SIDE
            frame_y = -MARGIN_BOTTOM
            c.setFillColor(MIDNIGHT)
            c.rect(frame_x, frame_y, w, h, fill=1, stroke=0)
            # Accent bar at top
            c.setFillColor(SIGNAL_BLUE)
            c.rect(frame_x, frame_y + h - 3, w, 3, fill=1, stroke=0)
            # Footer line
            c.setStrokeColor(STEEL)
            c.setLineWidth(0.5)
            c.line(0, frame_y + 38, w - 2 * MARGIN_SIDE, frame_y + 38)
            c.restoreState()

    story.append(DarkPageBackground())
    story.append(Spacer(1, 120))

    story.append(Paragraph(
        'ASG',
        ParagraphStyle('back_logo', fontName='Helvetica-Bold', fontSize=48,
                       leading=52, textColor=WHITE, alignment=TA_CENTER, spaceAfter=4)
    ))
    story.append(Paragraph(
        'S E C U R I T Y',
        ParagraphStyle('back_security', fontName='Helvetica', fontSize=18,
                       leading=22, textColor=GRAY_400, alignment=TA_CENTER, spaceAfter=24)
    ))
    story.append(Paragraph(
        'Complete Security. One Partner.',
        ParagraphStyle('back_tagline', fontName='Helvetica', fontSize=13,
                       leading=18, textColor=SIGNAL_BLUE, alignment=TA_CENTER, spaceAfter=40)
    ))

    # Divider
    story.append(HRFlowable(width='40%', thickness=0.5, color=STEEL,
                             spaceBefore=0, spaceAfter=40, hAlign='CENTER'))

    # Contact details
    contact_style = ParagraphStyle(
        'contact', fontName='Helvetica', fontSize=11,
        leading=18, textColor=GRAY_400, alignment=TA_CENTER, spaceAfter=4
    )
    story.append(Paragraph('Mark Clansey  |  General Manager', contact_style))
    story.append(Paragraph('mark@slsrtc.co.nz  |  021 879 664',
                           ParagraphStyle('contact2', parent=contact_style, fontSize=10)))

    story.append(Spacer(1, 24))

    story.append(Paragraph('Ahmad Duais  |  CEO',
                           ParagraphStyle('contact3', parent=contact_style)))
    story.append(Paragraph('ahmad@absolutesecuritygroup.co.nz',
                           ParagraphStyle('contact4', parent=contact_style, fontSize=10)))

    story.append(Spacer(1, 40))
    story.append(Paragraph(
        'asgsecurity.co.nz',
        ParagraphStyle('back_url', fontName='Helvetica-Bold', fontSize=12,
                       leading=16, textColor=WHITE, alignment=TA_CENTER)
    ))

    # ── Build ──────────────────────────────────────────────────
    def on_first_page(c, d):
        draw_cover_page(c, d)

    def on_later_pages(c, d):
        # Back cover draws its own background via DarkPageBackground flowable
        draw_normal_page(c, d)

    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    print(f'Brochure generated: {OUTPUT_PATH}')


if __name__ == '__main__':
    build()
