"""
ECHS Fraud Analytics Report 2 — Procedure-Level Upcoding & IPD Revenue Shift Analysis
Generates a professional 6-page PDF report using ReportLab.

Architecture:
  - Page 1 (cover) drawn directly with canvas, saved to a temp file.
  - Pages 2-6 (content) built with Platypus story, saved to a temp file.
  - Both files merged into final output using PdfReader/PdfWriter.
"""

import os
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib import colors

# ─── Colour palette ────────────────────────────────────────────────────────────
NAVY       = HexColor('#1B2744')
GOLD       = HexColor('#C9A020')
LIGHT_BLUE = HexColor('#EEF1F8')
WHITE      = white
DARK_GREY  = HexColor('#333333')
RED_ALERT  = HexColor('#8B0000')
LIGHT_NAVY = HexColor('#243358')
MID_GREY   = HexColor('#888888')

PAGE_W, PAGE_H = A4   # 595.27 x 841.89 pts

OUTPUT_PATH = '/home/abhishekpathak/Downloads/ECHS/ECHS_Fraud_Analytics_Report_2.pdf'
COVER_TMP   = '/tmp/echs_cover_tmp.pdf'
CONTENT_TMP = '/tmp/echs_content_tmp.pdf'

# ─── Paragraph styles ──────────────────────────────────────────────────────────
BODY = ParagraphStyle(
    'Body', fontName='Helvetica', fontSize=9, leading=13,
    textColor=DARK_GREY, alignment=TA_JUSTIFY, spaceAfter=6
)
BODY_LEFT = ParagraphStyle(
    'BodyLeft', fontName='Helvetica', fontSize=9, leading=13,
    textColor=DARK_GREY, alignment=TA_LEFT, spaceAfter=4
)
HEADING1 = ParagraphStyle(
    'H1', fontName='Helvetica-Bold', fontSize=13, leading=17,
    textColor=NAVY, spaceAfter=4, spaceBefore=4
)
HEADING2 = ParagraphStyle(
    'H2', fontName='Helvetica-Bold', fontSize=10, leading=13,
    textColor=NAVY, spaceAfter=4, spaceBefore=6
)
GOLD_HEADING = ParagraphStyle(
    'GoldH', fontName='Helvetica-Bold', fontSize=10, leading=13,
    textColor=GOLD, spaceAfter=4, spaceBefore=8
)
BULLET = ParagraphStyle(
    'Bullet', fontName='Helvetica', fontSize=8.5, leading=12,
    textColor=DARK_GREY, leftIndent=14, firstLineIndent=-14,
    spaceAfter=4, alignment=TA_JUSTIFY
)
SMALL_GREY = ParagraphStyle(
    'SmGrey', fontName='Helvetica', fontSize=7, leading=10,
    textColor=MID_GREY, alignment=TA_LEFT
)


# ─── Helper: standard table style ──────────────────────────────────────────────
def std_table_style(n_rows):
    cmds = [
        ('BACKGROUND',    (0, 0), (-1, 0),  NAVY),
        ('TEXTCOLOR',     (0, 0), (-1, 0),  WHITE),
        ('FONTNAME',      (0, 0), (-1, 0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, 0),  8),
        ('ALIGN',         (0, 0), (-1, 0),  'CENTER'),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING',    (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING',   (0, 0), (-1, -1), 4),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 4),
        ('GRID',          (0, 0), (-1, -1), 0.5, HexColor('#BBBBBB')),
        ('LINEBELOW',     (0, 0), (-1, 0),  1,   NAVY),
        ('FONTSIZE',      (0, 1), (-1, -1), 7.5),
    ]
    for i in range(1, n_rows):
        bg = WHITE if i % 2 == 1 else LIGHT_BLUE
        cmds.append(('BACKGROUND', (0, i), (-1, i), bg))
    return TableStyle(cmds)


# ─── Custom flowables ───────────────────────────────────────────────────────────
class PatternHeader(Flowable):
    """Gold left-border section header."""
    HEIGHT = 52

    def __init__(self, pattern_num, title, subtitle):
        super().__init__()
        self.pattern_num = pattern_num
        self.title = title
        self.subtitle = subtitle
        self._width = 0

    def wrap(self, availW, availH):
        self._width = availW
        return (availW, self.HEIGHT)

    def draw(self):
        c = self.canv
        w, h = self._width, self.HEIGHT
        c.setFillColor(HexColor('#F8F8F8'))
        c.rect(0, 0, w, h, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.rect(0, 0, 4, h, fill=1, stroke=0)
        c.setStrokeColor(HexColor('#DDDDDD'))
        c.setLineWidth(0.5)
        c.rect(0, 0, w, h, fill=0, stroke=1)
        c.setFillColor(GOLD)
        c.setFont('Helvetica-Bold', 7.5)
        c.drawString(12, h - 14, f'PATTERN {self.pattern_num}')
        c.setFillColor(NAVY)
        c.setFont('Helvetica-Bold', 13)
        c.drawString(12, h - 30, self.title)
        c.setFillColor(MID_GREY)
        c.setFont('Helvetica', 8)
        c.drawRightString(w - 8, 8, self.subtitle)


class MetricBoxRow(Flowable):
    """Row of metric boxes."""
    HEIGHT = 60

    def __init__(self, metrics):
        super().__init__()
        self.metrics = metrics
        self._width = 0

    def wrap(self, availW, availH):
        self._width = availW
        return (availW, self.HEIGHT)

    def draw(self):
        c = self.canv
        n = len(self.metrics)
        box_w = self._width / n
        h = self.HEIGHT
        for i, (label, value, sub) in enumerate(self.metrics):
            x = i * box_w
            c.setFillColor(HexColor('#F0F3FA'))
            c.roundRect(x + 3, 3, box_w - 6, h - 6, 4, fill=1, stroke=0)
            c.setStrokeColor(NAVY)
            c.setLineWidth(0.5)
            c.roundRect(x + 3, 3, box_w - 6, h - 6, 4, fill=0, stroke=1)
            # Gold top bar
            c.setFillColor(GOLD)
            c.rect(x + 3, h - 7, box_w - 6, 4, fill=1, stroke=0)
            cx = x + box_w / 2
            c.setFillColor(MID_GREY)
            c.setFont('Helvetica', 6.5)
            c.drawCentredString(cx, h - 20, label.upper())
            c.setFillColor(NAVY)
            c.setFont('Helvetica-Bold', 10.5)
            c.drawCentredString(cx, h - 36, value)
            c.setFillColor(DARK_GREY)
            c.setFont('Helvetica', 7)
            c.drawCentredString(cx, 10, sub)


class AlertBox(Flowable):
    """Red-bordered alert box with fixed height."""
    HEIGHT = 68

    def __init__(self, text):
        super().__init__()
        self.text = text
        self._width = 0

    def wrap(self, availW, availH):
        self._width = availW
        return (availW, self.HEIGHT)

    def draw(self):
        from reportlab.pdfbase.pdfmetrics import stringWidth
        c = self.canv
        w, h = self._width, self.HEIGHT
        c.setFillColor(HexColor('#FFF5F5'))
        c.rect(0, 0, w, h, fill=1, stroke=0)
        c.setStrokeColor(RED_ALERT)
        c.setLineWidth(1.5)
        c.rect(0, 0, w, h, fill=0, stroke=1)
        c.setFillColor(RED_ALERT)
        c.rect(0, 0, 5, h, fill=1, stroke=0)
        c.setFont('Helvetica-Bold', 8.5)
        c.setFillColor(RED_ALERT)
        c.drawString(14, h - 16, 'IMMEDIATE ESCALATION REQUIRED')
        # Word-wrap body text
        c.setFillColor(DARK_GREY)
        c.setFont('Helvetica', 7.5)
        words = self.text.split()
        lines, current = [], ''
        max_w = w - 22
        for word in words:
            test = (current + ' ' + word).strip()
            if stringWidth(test, 'Helvetica', 7.5) <= max_w:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        y = h - 30
        for line in lines:
            if y < 8:
                break
            c.drawString(14, y, line)
            y -= 11


# ─── Cover page (canvas-drawn, saved to temp PDF) ──────────────────────────────
def draw_cover_page():
    c = pdfcanvas.Canvas(COVER_TMP, pagesize=A4)

    # Full navy background
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Gold bars
    c.setFillColor(GOLD)
    c.rect(0, PAGE_H - 8, PAGE_W, 8, fill=1, stroke=0)
    c.rect(0, 0, PAGE_W, 8, fill=1, stroke=0)

    # Main title
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 36)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 162, 'ECHS FRAUD ANALYTICS')

    # Gold underline
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(PAGE_W / 2 - 170, PAGE_H - 172, PAGE_W / 2 + 170, PAGE_H - 172)

    # Subtitle
    c.setFillColor(WHITE)
    c.setFont('Helvetica', 14)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 196,
                        'Procedure-Level Upcoding & IPD Revenue Shift Analysis')

    # Module label
    c.setFillColor(GOLD)
    c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 220,
                        'SUPPLEMENTARY REPORT — MODULE 2')

    # ── Metadata table ──────────────────────────────────────────────────────────
    bx  = PAGE_W / 2 - 215
    bw  = 430
    bh  = 82
    by  = PAGE_H - 340

    # Outer border
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.rect(bx, by, bw, bh, fill=0, stroke=1)

    header_h = 28
    col_w = bw / 4
    headers_txt = ['CLASSIFICATION', 'PERIOD', 'HOSPITALS ANALYSED', 'QUERIES']
    values_txt  = ['RESTRICTED',     'FY 2023–2026', '~250 Active', '4 Query Sets (Q7–Q10)']

    for i in range(4):
        cx = bx + i * col_w + col_w / 2
        # Header cell background
        c.setFillColor(NAVY)
        c.rect(bx + i * col_w, by + bh - header_h, col_w, header_h, fill=1, stroke=0)
        # Data cell background
        c.setFillColor(LIGHT_NAVY)
        c.rect(bx + i * col_w, by, col_w, bh - header_h, fill=1, stroke=0)
        # Vertical divider
        if i > 0:
            c.setStrokeColor(HexColor('#3A4F7A'))
            c.setLineWidth(0.5)
            c.line(bx + i * col_w, by, bx + i * col_w, by + bh)
        # Header label
        c.setFillColor(GOLD)
        c.setFont('Helvetica-Bold', 7)
        c.drawCentredString(cx, by + bh - 13, headers_txt[i])
        # Value
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 8.5)
        c.drawCentredString(cx, by + (bh - header_h) / 2 - 4, values_txt[i])

    # Outer gold border on top of everything
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.rect(bx, by, bw, bh, fill=0, stroke=1)

    # IIT Kanpur line
    c.setFillColor(GOLD)
    c.setFont('Helvetica-Bold', 11)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 372,
                        'IIT KANPUR — Data Analytics & Fraud Intelligence Division')

    # Report date
    c.setFillColor(WHITE)
    c.setFont('Helvetica', 8.5)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 393,
                        'Report Date: May 2026  |  Ex-Servicemen Contributory Health Scheme (ECHS)')

    c.save()


# ─── Content page template callback ────────────────────────────────────────────
def content_page_template(canvas_obj, doc):
    c = canvas_obj
    c.saveState()
    pn = doc.page  # page number within the content doc (starts at 1)
    actual_page = pn + 1  # page 1 of content = page 2 of final doc

    bar_h    = 24
    footer_h = 22

    # Top bar
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - bar_h, PAGE_W, bar_h, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 7.5)
    c.drawString(20, PAGE_H - bar_h + 8, 'ECHS FRAUD ANALYTICS REPORT — CONFIDENTIAL')
    c.setFont('Helvetica', 7.5)
    c.drawRightString(PAGE_W - 20, PAGE_H - bar_h + 8, f'IIT Kanpur  |  Page {actual_page}')

    # Bottom bar
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, footer_h, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('Helvetica', 6.5)
    c.drawString(20, 7, 'RESTRICTED — For internal audit and investigative use only. Do not distribute without authorisation.')
    c.drawRightString(PAGE_W - 20, 7, 'Generated: 14 May 2026')

    c.restoreState()


# ─── Content pages (Platypus) ───────────────────────────────────────────────────
def build_executive_summary(story):
    story.append(Spacer(1, 4))
    story.append(Paragraph('EXECUTIVE SUMMARY', HEADING1))
    story.append(HRFlowable(width='100%', thickness=1, color=GOLD, spaceAfter=6))

    intro = (
        "This supplementary report extends the Module 1 fraud analytics exercise with four additional "
        "analytical queries targeting procedure-level upcoding, IPD revenue shift patterns, and "
        "empanelment irregularities. Two new fraud categories are identified: phantom procedure billing "
        "(billing at or below CGHS rates with 100% rejection) and systematic IPD revenue inflation "
        "across newly empanelled hospitals. A critical empanelment irregularity is flagged — a hospital "
        "located in Pokhara, Nepal (outside Indian territory) processing ECHS claims at scale."
    )
    story.append(Paragraph(intro, BODY))
    story.append(Spacer(1, 6))

    story.append(MetricBoxRow([
        ('Total Hospitals in Q10', '236 flagged',    'IPD growth > 100%'),
        ('New P1 Hospitals',       '6 identified',   'Not in Module 1'),
        ('Phantom Procedure Fraud','₹83.37L',        'Largest single category'),
        ('Critical Flag',          'MEDIPLUS NEPAL', 'Foreign hospital — Pokhara'),
    ]))
    story.append(Spacer(1, 10))

    story.append(Paragraph('New Fraud Patterns Identified — Module 2', HEADING2))
    headers = [['#', 'Pattern', 'Key Signal', 'Risk']]
    rows = [
        ['7',  'Phantom Procedure Billing',
               '170 uncoded procedure claims, ₹83.37L, 100% deducted',     'HIGH'],
        ['8',  'IPD Revenue Shift (Predictive)',
               '236 hospitals with >100% IPD growth, 3730: +395,411%',     'HIGH'],
        ['9',  'Pure-IPD Hospital Anomaly',
               '8 hospitals with zero OPD across 3 years',                 'HIGH'],
        ['10', 'Foreign Hospital / Empanelment',
               'MEDIPLUS, Pokhara Nepal, Tier 70, ₹1,693L IPD',            'CRITICAL'],
    ]
    data = headers + rows
    col_w = [20, 132, 272, 58]
    t = Table(data, colWidths=col_w, repeatRows=1)
    ts = std_table_style(len(data))
    for r_i, row in enumerate(rows, 1):
        if row[3] == 'CRITICAL':
            ts.add('BACKGROUND', (3, r_i), (3, r_i), HexColor('#FFE0E0'))
            ts.add('TEXTCOLOR',  (3, r_i), (3, r_i), RED_ALERT)
            ts.add('FONTNAME',   (3, r_i), (3, r_i), 'Helvetica-Bold')
        elif row[3] == 'HIGH':
            ts.add('BACKGROUND', (3, r_i), (3, r_i), HexColor('#FFF3CD'))
            ts.add('TEXTCOLOR',  (3, r_i), (3, r_i), HexColor('#856404'))
            ts.add('FONTNAME',   (3, r_i), (3, r_i), 'Helvetica-Bold')
    ts.add('ALIGN', (0, 0), (0, -1), 'CENTER')
    ts.add('ALIGN', (3, 0), (3, -1), 'CENTER')
    t.setStyle(ts)
    story.append(t)
    story.append(Spacer(1, 8))

    story.append(Paragraph('Immediate Actions', GOLD_HEADING))
    actions = [
        ("1.", "Escalate <b>MEDIPLUS HOSPITAL &amp; TRAUMA CENTER (3613, Pokhara, Nepal)</b> to ECHS HQ — "
               "foreign hospital with Tier 70 non-standard tier processing ₹1,693L in IPD claims and "
               "1,413 emergency admissions in 6 months."),
        ("2.", "Initiate empanelment review for <b>YATHARTH SUPER SPECIALITY HOSPITAL (3625, Greater Noida)</b> "
               "— IPD grew from ₹4L to ₹3,045L (+75,663%) in 2 years."),
        ("3.", "Verify admission records for all <b>PURE-IPD hospitals</b> (JMC MEDICITY, LIFELINE, MAXWELL, "
               "KRUSH DIVINE, OSCAR) — zero OPD across 3 years is clinically impossible for genuine hospitals."),
        ("4.", "Conduct phantom procedure audit — 54 claims filed with invalid CAT_ID=−1 and 170 with "
               "CAT_ID=0 (uncoded), totalling ₹88.54L with 100% deduction, indicating bulk auto-submission "
               "of unverifiable claims."),
    ]
    for num, text in actions:
        story.append(Paragraph(f'<b>{num}</b>  {text}', BULLET))

    story.append(PageBreak())


def build_pattern7(story):
    story.append(Spacer(1, 4))
    story.append(PatternHeader(7, 'PHANTOM PROCEDURE BILLING',
                               'Procedure-Level Upcoding Detection'))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "Unlike conventional rate inflation fraud where hospitals bill above CGHS entitlement rates, "
        "the historical procedure claims (his_hosp_exp_det) reveal a more sophisticated pattern: "
        "hospitals billing at or below the CGHS entitled rate yet having 100% of the claim amount "
        "deducted. This indicates the fraud lies not in rate manipulation but in clinical justification "
        "— procedures are claimed for conditions that do not warrant them, or for treatments that were "
        "never performed. Auditors reject these in their entirety.", BODY))
    story.append(Spacer(1, 6))

    story.append(Paragraph('Table 3.1 — Procedure Package Categories with 100% Deduction', HEADING2))
    headers = [['CAT_ID', 'Specialty', 'Claims', 'Avg Billed\n(₹)', 'Avg Entitled\n(₹)',
                 'Inflation', 'Claimed\n(L)', 'Deducted\n(L)']]
    rows = [
        ['0 (Uncoded)',    'Unknown',             '170', '290',       '306',       '−16',    '83.37', '83.37'],
        ['NU122',          'Neurology',            '25',  '1,610',    '2,500',     '−890',   '8.45',  '8.45'],
        ['NU123',          'Neurology',            '25',  '2,375',    '3,000',     '−625',   '7.72',  '7.72'],
        ['−1 (Invalid)',   'Unknown',              '54',  '0',        '0',         '—',      '5.17',  '5.17'],
        ['CP002',          'Cardiac Surgery',      '2',   '67,593',   '67,608',    '−15',    '1.35',  '1.35'],
        ['OR089',          'Orthopaedics',         '1',   '1,29,200', '1,29,200',  '0',      '1.29',  '1.29'],
        ['CI016',          'Cardiac Intervention', '2',   '5,410',    '10,821',    '−5,411', '0.11',  '0.11'],
    ]
    data = headers + rows
    col_w = [58, 92, 36, 66, 68, 50, 52, 56]
    t = Table(data, colWidths=col_w, repeatRows=1)
    ts = std_table_style(len(data))
    ts.add('ALIGN', (2, 1), (-1, -1), 'CENTER')
    ts.add('TEXTCOLOR', (0, 1), (0, 1), RED_ALERT)
    ts.add('FONTNAME',  (0, 1), (0, 1), 'Helvetica-Bold')
    ts.add('TEXTCOLOR', (0, 4), (0, 4), RED_ALERT)
    ts.add('FONTNAME',  (0, 4), (0, 4), 'Helvetica-Bold')
    t.setStyle(ts)
    story.append(t)
    story.append(Spacer(1, 8))

    story.append(Paragraph('Key Findings', GOLD_HEADING))
    for f in [
        "<b>CAT_ID=0 (Uncoded Procedures):</b> 170 claims worth ₹83.37L submitted without a valid "
        "CGHS package code. These are auto-rejected but continue to be filed, generating fraudulent "
        "claim volume. This is systematic bulk auto-submission, not isolated errors.",
        "<b>CAT_ID=−1 (Invalid Code):</b> 54 claims filed with a programmatically invalid category ID. "
        "No legitimate billing system generates negative category codes — this indicates direct database "
        "manipulation or API bypass of the submission system.",
        "<b>Negative Inflation = Phantom Admissions:</b> All NU (Neurology) and CP (Cardiac Surgery) "
        "categories show hospitals billing below the CGHS entitlement rate. The rejection is not due "
        "to over-pricing; auditors are rejecting the clinical basis entirely — the procedures were "
        "either not performed or not medically justified.",
        "<b>High-value specialties targeted:</b> OR089 (Orthopaedic package at ₹1,29,200), CP002 "
        "(Cardiac surgery at ₹67,593), CI016 (Cardiac intervention) — chosen precisely because they "
        "are complex, hard to verify without physical record inspection, and have high CGHS entitlement rates.",
    ]:
        story.append(Paragraph(f'• {f}', BULLET))

    story.append(PageBreak())


def build_pattern8(story):
    story.append(Spacer(1, 4))
    story.append(PatternHeader(8, 'IPD REVENUE SHIFT ANALYSIS',
                               'Predictive Upcoding Detection via settlement_stat'))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "Q10 analysed 3 years of settlement_stat data (3M pre-aggregated records) to identify hospitals "
        "where IPD revenue is growing disproportionately faster than OPD. An organic hospital grows both "
        "IPD and OPD in proportion to its patient load. Hospitals where IPD revenue grows by hundreds or "
        "thousands of percent while OPD remains flat are reclassifying OPD patients as IPD (upcoding) "
        "or generating phantom inpatient admissions.", BODY))
    story.append(Spacer(1, 6))

    story.append(Paragraph('Table 4.1 — Top 15 Hospitals by IPD Growth (FY 2023–2025)', HEADING2))
    headers = [['Office\nID', 'Hospital', '2023\nIPD (L)', '2025\nIPD (L)', 'Growth %',
                 '2025\nOPD (L)', 'Flag']]
    rows = [
        ['3730', 'MEDANTA ABDUR RAZZAQUE, Ranchi',        '0.0',     '104.6',    '395,411%', '5.8',   'NEW-ENTRANT'],
        ['3651', 'MEHAR HOSPITAL, Zirakpur',               '0.2',     '427.2',    '216,146%', '9.2',   'NEW-ENTRANT'],
        ['3625', 'YATHARTH SUPER SPECIALITY, Gr Noida',   '4.0',     '3,045.1',  '75,663%',  '85.4',  'CRITICAL'],
        ['3706', 'GRAPHIC ERA INST OF MED SCI, Dehradun', '1.8',     '1,323.5',  '73,126%',  '146.6', 'CRITICAL'],
        ['3583', 'JMC MEDICITY, Meerut',                  '2.7',     '1,277.2',  '47,526%',  '0.0',   'PURE-IPD'],
        ['3541', 'PACE HOSPITAL, Hyderabad',              '1.9',     '555.5',    '29,734%',  '13.3',  'NEW-ENTRANT'],
        ['3613', 'MEDIPLUS HOSPITAL, POKHARA NEPAL',      '6.6',     '1,692.8',  '25,374%',  '937.9', 'FOREIGN'],
        ['2694', 'STAR HOSPITAL',                         '42.3',    '8,537.7',  '20,097%',  '1.5',   'PURE-IPD'],
        ['3544', 'KRUSH DIVINE HOSPITAL, GB Nagar',      '15.6',    '1,817.4',  '11,547%',  '1.2',   'PURE-IPD'],
        ['3657', 'OSCAR SUPERSPECIALITY, Ch Dadri',       '14.1',    '1,132.6',  '7,954%',   '4.7',   'PURE-IPD'],
        ['2844', 'SINGHANIA UNIVERSITY HOSP',             '83.4',    '3,305.9',  '3,865%',   '3.3',   'PURE-IPD'],
        ['1042', 'METRO HOSPITAL, Noida',                 '2,706.6', '10,005.9', '270%',     '67.8',  'P1-CONFIRMED'],
        ['3149', 'VIJAY HOSPITAL',                        '2,142.4', '21,691.8', '913%',     '8.6',   'P1-CONFIRMED'],
        ['2856', 'VIRAT HOSPITAL',                        '1,196.1', '7,401.6',  '519%',     '4.7',   'P1-CONFIRMED'],
        ['1065', 'PRAYAG HOSPITAL',                       '144.9',   '928.6',    '541%',     '1.1',   'PURE-IPD'],
    ]
    data = headers + rows
    col_w = [36, 162, 46, 46, 52, 46, 74]
    t = Table(data, colWidths=col_w, repeatRows=1)
    ts = std_table_style(len(data))
    ts.add('ALIGN', (0, 0), (0, -1), 'CENTER')
    ts.add('ALIGN', (2, 1), (5, -1), 'CENTER')
    ts.add('ALIGN', (6, 0), (6, -1), 'CENTER')
    flag_style = {
        'CRITICAL':     (HexColor('#FFE0E0'), RED_ALERT),
        'FOREIGN':      (HexColor('#FFE0E0'), RED_ALERT),
        'PURE-IPD':     (HexColor('#FFF8E1'), HexColor('#7B5E00')),
        'NEW-ENTRANT':  (HexColor('#E8F5E9'), HexColor('#1B5E20')),
        'P1-CONFIRMED': (LIGHT_BLUE, NAVY),
    }
    for r_i, row in enumerate(rows, 1):
        flag = row[6]
        if flag in flag_style:
            bg, fg = flag_style[flag]
            ts.add('BACKGROUND', (6, r_i), (6, r_i), bg)
            ts.add('TEXTCOLOR',  (6, r_i), (6, r_i), fg)
            ts.add('FONTNAME',   (6, r_i), (6, r_i), 'Helvetica-Bold')
    t.setStyle(ts)
    story.append(t)
    story.append(Spacer(1, 8))

    story.append(Paragraph('Key Findings', GOLD_HEADING))
    for f in [
        "236 hospitals show >100% IPD growth with >₹100L 2025 IPD volume — this is the full predictive watchlist.",
        "<b>P1 hospitals confirmed:</b> VIJAY (3149), METRO NOIDA (1042), VIRAT (2856), PRAYAG (1065), "
        "RLKC (1069), STAR (2694) all appear in Q10, cross-validating the Module 1 findings with IPD shift data.",
        "<b>YATHARTH SUPER SPECIALITY (3625, Greater Noida, Tier 60):</b> IPD grew from ₹4L to ₹3,045L — "
        "a ₹30 Crore IPD revenue base built in 2 years from near-zero. This hospital had zero presence in "
        "Module 1 analysis (below volume threshold), making Q10 the discovery mechanism.",
        "<b>GRAPHIC ERA INSTITUTE (3706, Dehradun):</b> Educational/research institute with ₹13Cr IPD in "
        "2025 up from ₹2L base. Medical college hospitals have complex billing structures that may mask "
        "procedure upcoding.",
    ]:
        story.append(Paragraph(f'• {f}', BULLET))

    story.append(PageBreak())


def build_pattern9_10(story):
    story.append(Spacer(1, 4))
    story.append(PatternHeader(9, 'PURE-IPD HOSPITAL ANOMALY',
                               'Zero OPD Across 3 Years'))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "A legitimate hospital, regardless of specialty, generates some outpatient activity — follow-up "
        "consultations, pre-admission workups, post-discharge reviews. Eight hospitals in Q10 show zero "
        "or near-zero OPD (&lt;₹5L) across all three years while simultaneously running large IPD "
        "operations. This clinical impossibility indicates either: (a) all outpatient activity is being "
        "mis-categorised as IPD to claim higher reimbursements, or (b) the hospital exists primarily as "
        "a claims processing entity with minimal genuine patient care.", BODY))
    story.append(Spacer(1, 6))

    story.append(Paragraph('Table 5.1 — Pure-IPD Hospitals (OPD < ₹5L across FY 2023–2025)', HEADING2))
    headers = [['Hospital', 'City', 'Tier', '2025 IPD (L)', '2025 OPD (L)', 'IPD Growth']]
    rows = [
        ['JMC MEDICITY (3583)',        'Meerut',        '61', '1,277.2', '0.0',  '+47,526%'],
        ['STAR HOSPITAL (2694)',        '—',             '62', '8,537.7', '1.5',  '+20,097%'],
        ['KRUSH DIVINE HOSP (3544)',    'GB Nagar',      '62', '1,817.4', '1.2',  '+11,547%'],
        ['OSCAR SUPERSPECIALITY (3657)','Charkhi Dadri', '62', '1,132.6', '4.7',  '+7,954%'],
        ['SINGHANIA UNIV HOSP (2844)', '—',             '62', '3,305.9', '3.3',  '+3,865%'],
        ['LIFELINE MULTISPEC (3560)',   'Bhiwani',       '62', '920.5',   '0.4',  '+3,073%'],
        ['MAXWELL MULTISPEC (3563)',    'Varanasi',      '61', '691.9',   '0.1',  '+2,514%'],
        ['PRAYAG HOSPITAL (1065)',      'Noida',         '—',  '928.6',   '1.1',  '+541%'],
    ]
    data = headers + rows
    col_w = [152, 72, 34, 72, 72, 74]
    t = Table(data, colWidths=col_w, repeatRows=1)
    ts = std_table_style(len(data))
    ts.add('ALIGN', (2, 0), (5, -1), 'CENTER')
    t.setStyle(ts)
    story.append(t)
    story.append(Spacer(1, 12))

    # Pattern 10
    story.append(PatternHeader(10, 'FOREIGN HOSPITAL / EMPANELMENT IRREGULARITY',
                               'Critical Escalation Required'))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "MEDIPLUS HOSPITAL &amp; TRAUMA CENTER PVT LTD (Office ID: 3613) is registered in the ECHS "
        "office_master with city = POKHARA and OM_TIER_ID = 70. Pokhara is Nepal's second-largest city. "
        "Tier 70 is not a valid ECHS tier code (valid tiers: 60, 61, 62). This hospital appeared in Q3 "
        "emergency admission analysis with 1,413 emergency admissions across October 2025–March 2026, "
        "and in Q10 with IPD revenue of ₹1,692.8L (2025) and OPD of ₹937.9L — a total billing of "
        "₹2,630L (₹26.3 Crore) in a single year. Processing Indian defence personnel health scheme "
        "claims from a foreign country represents a fundamental empanelment control failure, not merely "
        "a billing anomaly.", BODY))
    story.append(Spacer(1, 8))

    story.append(AlertBox(
        "Office ID 3613, MEDIPLUS HOSPITAL, POKHARA, NEPAL.  "
        "Total FY2025 billing: ₹2,630L (₹26.3 Crore).  "
        "Emergency admissions: 1,413 in 6 months.  "
        "Tier code: 70 (INVALID).  "
        "This matter exceeds the scope of fraud analytics and requires administrative and legal review."
    ))

    story.append(PageBreak())


def build_risk_register(story):
    story.append(Spacer(1, 4))
    story.append(Paragraph('UPDATED COMPOSITE RISK REGISTER', HEADING1))
    story.append(Paragraph('Combined Module 1 + Module 2 Findings', SMALL_GREY))
    story.append(HRFlowable(width='100%', thickness=1, color=GOLD, spaceAfter=6))
    story.append(Spacer(1, 4))

    headers = [['Priority', 'Hospital (ID)', 'City', 'Tier', 'Patterns\nTriggered',
                 '2025\nIPD (L)', 'Ded.%', 'Action']]
    rows = [
        ['P0\nCRITICAL', 'MEDIPLUS / POKHARA (3613)', 'Nepal',    '70', 'Q3+Q10\n+Foreign',   '1,692.8',  '—',     'Immediate escalation to ECHS HQ'],
        ['P1',           'VIJAY HOSPITAL (3149)',       '—',        '62', 'Q1+Q10',             '21,691.8', '34.2%', 'Field audit'],
        ['P1',           'STAR HOSPITAL (2694)',        '—',        '62', 'Q1+Q10\n+Pure-IPD',  '8,537.7',  '32.7%', 'Suspension review'],
        ['P1',           'YATHARTH SUPER SP (3625)',    'Gr Noida', '60', 'Q10 New',            '3,045.1',  '—',     'Empanelment review'],
        ['P1',           'METRO HOSP NOIDA (1042)',     'Noida',    '60', 'Q1+Q2\n+Q3+Q10',    '10,005.9', '20.3%', 'Panel + rate audit'],
        ['P1',           'SINGHANIA UNIV (2844)',       '—',        '62', 'Q1+Q10\n+Pure-IPD',  '3,305.9',  '28.8%', 'Claims sampling'],
        ['P1',           'GRAPHIC ERA (3706)',           'Dehradun', '61', 'Q10 New',            '1,323.5',  '—',     'Admission audit'],
        ['P1',           'VIRAT HOSPITAL (2856)',       '—',        '62', 'Q1+Q10',             '7,401.6',  '35.3%', 'Empanelment review'],
        ['P1',           'PRAYAG HOSPITAL (1065)',      'Noida',    '—',  'Q2+Q3+Q10\n+Pure-IPD','928.6',   '—',     'Admission records'],
        ['P2',           'JMC MEDICITY (3583)',         'Meerut',   '61', 'Q10\n+Pure-IPD',     '1,277.2',  '—',     'Spot verification'],
        ['P2',           'KRUSH DIVINE (3544)',         'GB Nagar', '62', 'Q10\n+Pure-IPD',     '1,817.4',  '—',     'Patient verification'],
        ['P2',           'PRATAP HOSPITAL (3980)',      '—',        '62', 'Q1',                 '—',        '30.3%', 'Claims review'],
        ['P2',           'RLKC HOSPITAL (1069)',        'Delhi',    '—',  'Q2+Q10',             '1,221.3',  '—',     'Admission audit'],
        ['P2',           'YASHLOK HOSPITAL (1305)',     '—',        '61', 'Q6',                 '—',        '95.0%', 'De-panel review'],
        ['P2',           'KAMINENI HOSPITALS (177)',    '—',        '60', 'Q6',                 '—',        '55.5%', 'Claims sampling'],
    ]
    data = headers + rows
    col_w = [44, 126, 52, 28, 74, 46, 36, 112]
    t = Table(data, colWidths=col_w, repeatRows=1)
    ts = std_table_style(len(data))
    ts.add('ALIGN', (0, 0), (0, -1), 'CENTER')
    ts.add('ALIGN', (3, 0), (3, -1), 'CENTER')
    ts.add('ALIGN', (5, 0), (6, -1), 'CENTER')
    # P0 row
    ts.add('BACKGROUND', (0, 1), (-1, 1), HexColor('#FFE0E0'))
    ts.add('TEXTCOLOR',  (0, 1), (0, 1),  RED_ALERT)
    ts.add('FONTNAME',   (0, 1), (-1, 1), 'Helvetica-Bold')
    # P1 rows
    for r in range(2, 10):
        ts.add('BACKGROUND', (0, r), (0, r), HexColor('#FFF3CD'))
        ts.add('TEXTCOLOR',  (0, r), (0, r), HexColor('#856404'))
        ts.add('FONTNAME',   (0, r), (0, r), 'Helvetica-Bold')
    # P2 rows
    for r in range(10, 16):
        ts.add('BACKGROUND', (0, r), (0, r), LIGHT_BLUE)
        ts.add('TEXTCOLOR',  (0, r), (0, r), NAVY)
        ts.add('FONTNAME',   (0, r), (0, r), 'Helvetica-Bold')
    t.setStyle(ts)
    story.append(t)
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        '<b>Note:</b> P0 = Immediate escalation (foreign entity). P1 = High-priority field audit '
        'within 30 days. P2 = Systematic review within 60 days. Deduction% from Module 1 claim-level '
        'data; "—" not yet available from settlement_stat aggregates.',
        SMALL_GREY
    ))


def build_content_pages():
    """Build pages 2-6 as a Platypus document."""
    doc = SimpleDocTemplate(
        CONTENT_TMP,
        pagesize=A4,
        leftMargin=36, rightMargin=36,
        topMargin=36, bottomMargin=30,
        title='ECHS Fraud Analytics Report — Module 2',
        author='IIT Kanpur',
    )
    story = []
    build_executive_summary(story)
    build_pattern7(story)
    build_pattern8(story)
    build_pattern9_10(story)
    build_risk_register(story)

    doc.build(story, onFirstPage=content_page_template,
              onLaterPages=content_page_template)


# ─── Merge PDFs ─────────────────────────────────────────────────────────────────
def merge_pdfs():
    """Merge cover (1 page) + content (5 pages) into final output."""
    try:
        # Try pypdf first (modern)
        from pypdf import PdfWriter, PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfWriter, PdfReader
        except ImportError:
            # Fallback: just concatenate using reportlab's canvas
            return False

    writer = PdfWriter()
    for path in [COVER_TMP, CONTENT_TMP]:
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)

    with open(OUTPUT_PATH, 'wb') as f:
        writer.write(f)
    return True


def merge_pdfs_canvas_fallback():
    """Fallback: re-render everything into one canvas."""
    # This should not be needed normally
    pass


# ─── Main ───────────────────────────────────────────────────────────────────────
def build_report():
    print("Generating cover page...")
    draw_cover_page()
    print(f"  Cover saved to {COVER_TMP}")

    print("Generating content pages...")
    build_content_pages()
    print(f"  Content saved to {CONTENT_TMP}")

    print("Merging PDF pages...")
    ok = merge_pdfs()
    if not ok:
        print("  PDF merge library not found — installing pypdf...")
        os.system('pip3 install pypdf -q')
        ok = merge_pdfs()

    if ok:
        size = os.path.getsize(OUTPUT_PATH)
        print(f"\nPDF successfully generated: {OUTPUT_PATH}")
        print(f"File size: {size:,} bytes  ({size/1024:.1f} KB)")
    else:
        print("ERROR: Could not merge PDFs.")

    # Clean up temp files
    for f in [COVER_TMP, CONTENT_TMP]:
        if os.path.exists(f):
            os.remove(f)


if __name__ == '__main__':
    build_report()
