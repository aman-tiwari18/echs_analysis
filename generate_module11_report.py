import os
import csv
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable

W, H = A4

# ── Colour palette (identical to gen_20module_report.py) ─────────────────────
NAVY   = HexColor('#1a2744')
GOLD   = HexColor('#c8a84b')
RED    = HexColor('#cc2222')
ORANGE = HexColor('#d46a00')
GREEN  = HexColor('#1a6e1a')
LGRAY  = HexColor('#f4f4f4')
MGRAY  = HexColor('#dddddd')
DGRAY  = HexColor('#444444')
LBLUE  = HexColor('#e8ecf5')

# ── Paragraph styles (identical to gen_20module_report.py) ───────────────────
def bs(**kw):
    defaults = dict(fontName='Helvetica', fontSize=10, leading=15, textColor=DGRAY, spaceAfter=6)
    defaults.update(kw)
    return ParagraphStyle('x', **defaults)

S_BODY  = bs(alignment=TA_JUSTIFY, leading=13)
S_BODYL = bs(alignment=TA_LEFT, leading=13)
S_H1    = bs(fontName='Helvetica-Bold', fontSize=15, textColor=GOLD, leading=19, spaceBefore=12, spaceAfter=5)
S_H2    = bs(fontName='Helvetica-Bold', fontSize=11, textColor=NAVY, leading=15, spaceBefore=8, spaceAfter=3)
S_H3    = bs(fontName='Helvetica-Bold', fontSize=9.5, textColor=NAVY, leading=13, spaceBefore=6, spaceAfter=2)
S_SMALL = bs(fontSize=7.5, textColor=DGRAY, leading=11)
S_LABEL = bs(fontName='Helvetica-Bold', fontSize=7, textColor=GOLD, leading=10, alignment=TA_CENTER)
S_BULL  = bs(alignment=TA_LEFT, leading=13, leftIndent=10)
S_WARN  = bs(fontName='Helvetica-Bold', fontSize=8, textColor=RED, leading=12)
S_MONO  = bs(fontName='Courier', fontSize=7.5, textColor=DGRAY, leading=11)

def crit(t): return f'<font color="#cc2222"><b>{t}</b></font>'
def high(t): return f'<font color="#d46a00"><b>{t}</b></font>'
def ok(t):   return f'<font color="#1a6e1a"><b>{t}</b></font>'
def bold(t): return f'<b>{t}</b>'
def gold(t): return f'<font color="#c8a84b"><b>{t}</b></font>'

# ── Table style (identical to gen_20module_report.py) ────────────────────────
def tbl_style(hdr=1):
    return TableStyle([
        ('BACKGROUND',   (0,0), (-1, hdr-1), NAVY),
        ('TEXTCOLOR',    (0,0), (-1, hdr-1), white),
        ('FONTNAME',     (0,0), (-1, hdr-1), 'Helvetica-Bold'),
        ('FONTSIZE',     (0,0), (-1,-1), 7.5),
        ('LEADING',      (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,hdr), (-1,-1), [white, LGRAY]),
        ('GRID',         (0,0), (-1,-1), 0.35, MGRAY),
        ('LINEBELOW',    (0,0), (-1,0), 0.8, GOLD),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',   (0,0), (-1,-1), 6),
        ('BOTTOMPADDING',(0,0), (-1,-1), 6),
        ('LEFTPADDING',  (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ])

# ── Cover Page — matches previous report style (clean navy, metrics boxes) ────
class CoverPage(Flowable):
    def __init__(self, dupes=0, exposure_l=0.0, sim_adm=0, uid_clusters=0):
        super().__init__()
        self.width = W; self.height = H
        self.dupes = dupes; self.exposure_l = exposure_l
        self.sim_adm = sim_adm; self.uid_clusters = uid_clusters

    def draw(self):
        c = self.canv

        # ── Full navy background ──────────────────────────────────────────────
        c.setFillColor(NAVY); c.rect(0, 0, W, H, fill=1, stroke=0)

        # ── Top header bar ────────────────────────────────────────────────────
        c.setFillColor(HexColor('#0d1929')); c.rect(0, H-22*mm, W, 22*mm, fill=1, stroke=0)
        c.setFillColor(white); c.setFont('Helvetica-Bold', 8)
        c.drawCentredString(W/2, H-10*mm,
            'GOVERNMENT OF INDIA  |  EX-SERVICEMEN CONTRIBUTORY HEALTH SCHEME  |  ECHS DIRECTORATE')
        c.setFont('Helvetica', 7.5); c.setFillColor(HexColor('#aabbcc'))
        c.drawCentredString(W/2, H-16*mm, 'Fraud Analytics & Financial Intelligence Report')

        # ── Main title ────────────────────────────────────────────────────────
        c.setFont('Helvetica-Bold', 42); c.setFillColor(GOLD)
        c.drawCentredString(W/2, H-42*mm, 'ECHS FRAUD ANALYTICS')

        # ── Subtitle ──────────────────────────────────────────────────────────
        c.setFont('Helvetica', 16); c.setFillColor(white)
        c.drawCentredString(W/2, H-54*mm, 'Duplicate Claims & Identity Misuse Analysis')

        # ── Module tag line ───────────────────────────────────────────────────
        c.setFont('Helvetica-Bold', 9); c.setFillColor(GOLD)
        c.drawCentredString(W/2, H-63*mm,
            'MODULE 11 REPORT  |  FY 2014 \u2013 FY 2026  |  RULE-BASED DETECTION')

        # ── Gold divider ──────────────────────────────────────────────────────
        c.setStrokeColor(GOLD); c.setLineWidth(1)
        c.line(25*mm, H-68*mm, W-25*mm, H-68*mm)

        # ── 4-column metrics box ──────────────────────────────────────────────
        bx  = 18*mm
        bw  = W - 36*mm
        bh  = 32*mm
        by  = H - 105*mm
        col_w = bw / 4

        metrics = [
            ('TOTAL CLAIMS',      '33.4 Crore'),
            ('DUPLICATES FOUND',  f'{self.dupes:,}'),
            ('EXPOSURE',          f'\u20b9{self.exposure_l:,.1f}L'),
            ('PATTERNS SCREENED', '5 Signals'),
        ]

        # Outer gold border
        c.setStrokeColor(GOLD); c.setLineWidth(1)
        c.rect(bx, by, bw, bh, fill=0, stroke=1)

        for i, (label, value) in enumerate(metrics):
            cx = bx + i * col_w
            # Cell background
            c.setFillColor(HexColor('#0d1929'))
            c.rect(cx, by, col_w, bh, fill=1, stroke=0)
            # Vertical divider (except first)
            if i > 0:
                c.setStrokeColor(GOLD); c.setLineWidth(0.5)
                c.line(cx, by, cx, by + bh)
            # Label
            c.setFont('Helvetica-Bold', 7); c.setFillColor(GOLD)
            c.drawCentredString(cx + col_w/2, by + bh - 9*mm, label)
            # Value
            c.setFont('Helvetica-Bold', 16); c.setFillColor(white)
            c.drawCentredString(cx + col_w/2, by + 8*mm, value)

        # Redraw outer border on top
        c.setStrokeColor(GOLD); c.setLineWidth(1)
        c.rect(bx, by, bw, bh, fill=0, stroke=1)

        # ── 3 fraud estimate boxes ────────────────────────────────────────────
        eb_y  = H - 150*mm
        eb_h  = 30*mm
        eb_w  = (W - 50*mm) / 3
        estimates = [
            ('Exact Duplicates',     f'{self.dupes:,} submissions'),
            ('Simultaneous Admissions', f'{self.sim_adm} impossible pairs'),
            ('UID Fraud Clusters',   f'{self.uid_clusters} shared UIDs'),
        ]
        for i, (label, val) in enumerate(estimates):
            ex = 18*mm + i * (eb_w + 7*mm)
            c.setFillColor(HexColor('#0d1929'))
            c.rect(ex, eb_y, eb_w, eb_h, fill=1, stroke=0)
            c.setStrokeColor(GOLD); c.setLineWidth(0.5)
            c.rect(ex, eb_y, eb_w, eb_h, fill=0, stroke=1)
            c.setFont('Helvetica', 7); c.setFillColor(HexColor('#aabbcc'))
            c.drawCentredString(ex + eb_w/2, eb_y + eb_h - 8*mm, label)
            c.setFont('Helvetica-Bold', 12); c.setFillColor(GOLD)
            c.drawCentredString(ex + eb_w/2, eb_y + 7*mm, val)

        # ── IIT Kanpur footer ─────────────────────────────────────────────────
        c.setFont('Helvetica-Bold', 10); c.setFillColor(GOLD)
        c.drawCentredString(W/2, 28*mm, 'IIT KANPUR \u2014 Data Analytics & Fraud Intelligence Division')
        c.setFont('Helvetica', 8); c.setFillColor(white)
        c.drawCentredString(W/2, 21*mm,
            'Report Date: May 2026  |  Ex-Servicemen Contributory Health Scheme (ECHS)')
        c.setFont('Helvetica', 7); c.setFillColor(HexColor('#556688'))
        c.drawCentredString(W/2, 12*mm,
            'CONFIDENTIAL \u2014 For authorized personnel only. Not for public distribution.')

# ── Header / Footer (identical to gen_20module_report.py) ────────────────────
def inner_hf(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY); canvas.rect(0, H-12*mm, W, 12*mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD); canvas.rect(0, H-12.5*mm, W, 0.5*mm, fill=1, stroke=0)
    canvas.setFont('Helvetica-Bold', 9); canvas.setFillColor(GOLD)
    canvas.drawString(15*mm, H-8*mm, 'ECHS FRAUD ANALYTICS \u2014 MODULE 11: DUPLICATE CLAIMS & IDENTITY MISUSE')
    canvas.setFont('Helvetica', 7.5); canvas.setFillColor(HexColor('#aabbcc'))
    canvas.drawRightString(W-15*mm, H-8*mm, 'IIT Kanpur \u00d7 ECHS Directorate  |  May 2026')
    canvas.setFillColor(NAVY); canvas.rect(0, 0, W, 10*mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD); canvas.rect(0, 10*mm, W, 0.5*mm, fill=1, stroke=0)
    canvas.setFont('Helvetica', 7); canvas.setFillColor(HexColor('#8899bb'))
    canvas.drawString(15*mm, 3.5*mm, 'RESTRICTED \u2014 Authorized Personnel Only')
    canvas.setFont('Helvetica-Bold', 8); canvas.setFillColor(GOLD)
    canvas.drawRightString(W-15*mm, 3.5*mm, f'Page {doc.page}')
    canvas.restoreState()

# ── CSV helper ────────────────────────────────────────────────────────────────
BASE = '/home/aman/Desktop/echs_analysis'

def read_csv(filename):
    path = os.path.join(BASE, filename)
    data = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                data.append(row)
    return data

# ── Pattern sections ──────────────────────────────────────────────────────────
def build_executive_summary(story):
    story.append(Paragraph('EXECUTIVE SUMMARY', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))
    story.append(Paragraph(
        "This Module 11 report presents findings from a systematic ECHS claims screening exercise "
        "targeting duplicate billing, identity misuse, and anecdotal fraud. Five distinct patterns "
        "are analysed — exact duplicate submissions, simultaneous admissions, synthetic UID sharing, "
        "claim unbundling, and post-death (Lazarus) billing. Each flagged case is an investigative "
        "lead requiring auditor review before action.", S_BODY))
    story.append(Spacer(1, 6*mm))

    rows = read_csv('Repeated_Exact_Duplicates.csv')
    dupes = sum(int(r[4]) for r in rows if len(r) > 4) if rows else 0
    exp   = sum(float(r[3]) * int(r[4]) for r in rows if len(r) > 4) if rows else 0.0

    summary_data = [
        ['Metric', 'Value', 'Notes'],
        ['Total Exact Duplicate Submissions', f'{dupes:,}',            'Across all flagged pairs'],
        ['Estimated Financial Exposure',      f'\u20b9{exp/100000:,.2f} Lakhs', 'Gross Claim Amount \u00d7 Duplicates'],
        ['Patterns Screened',                 '5 Fraud Signals',       'FA-01 through FA-05'],
        ['Data Coverage',                     '33.4 Crore Claims',     'Full ECHS history 2014\u20132026'],
    ]
    t = Table(summary_data, colWidths=[66*mm, 39*mm, 48*mm])
    t.setStyle(tbl_style())
    story.append(t)
    story.append(Spacer(1, 6*mm))

    story.append(Paragraph('Fraud Patterns — Module 11 Overview', S_H2))
    overview = [
        ['#', 'Pattern', 'Key Signal', 'Risk'],
        ['1', 'Exact Duplicate Claims',    f'{dupes} duplicate submissions detected',              Paragraph(crit('CRITICAL'), S_SMALL)],
        ['2', 'Simultaneous Admissions',   'Patients admitted at 2+ hospitals simultaneously',     Paragraph(crit('CRITICAL'), S_SMALL)],
        ['3', 'Synthetic Identities',      'Aadhaar UIDs shared by up to 22 different profiles',   Paragraph(high('HIGH'), S_SMALL)],
        ['4', 'Claim Unbundling',          '500+ claims on same day for same patient',              Paragraph(high('HIGH'), S_SMALL)],
        ['5', 'Post-Death Billing',        'Claims submitted after patient recorded deceased',      Paragraph(crit('CRITICAL'), S_SMALL)],

    ]
    t2 = Table(overview, colWidths=[8*mm, 44*mm, 75*mm, 26*mm])
    t2.setStyle(tbl_style())
    story.append(t2)
    story.append(Spacer(1, 6*mm))

    story.append(Paragraph('Immediate Actions Required', S_H2))
    for num, text in [
        ('1.', 'Suspend all claims linked to duplicate groups with extreme submission counts (FA-01).'),
        ('2.', 'Initiate verification for all patients flagged for simultaneous admissions (FA-02).'),
        ('3.', 'Freeze accounts sharing critical UID clusters indicating synthetic profiles (FA-03).'),
        ('4.', 'Immediate investigation into post-death billing anomalies (FA-05 Lazarus Pattern).'),
    ]:
        story.append(Paragraph(f'{bold(num)}  {text}', S_BULL))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        f'{bold("NOTE:")} This report is produced by an automated screening system. '
        'Every flagged case is an investigative lead, not a confirmed finding. '
        'A qualified auditor must review each case before any action is taken.', S_WARN))
    story.append(PageBreak())

def build_fa_01(story):
    story.append(Paragraph('FA-01 \u2014 EXACT DUPLICATE CLAIMS', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))
    story.append(Paragraph(
        "A hospital submits the exact same claim (same patient, same admission date, discharge date, "
        "and amount) multiple times under new claim IDs to double-bill the system. "
        "This indicates bypass of basic duplicate checks in the submission portal.", S_BODY))
    story.append(Spacer(1, 5*mm))

    rows = read_csv('Repeated_Exact_Duplicates.csv')
    total_dupes = sum(int(r[4]) for r in rows if len(r) > 4) if rows else 0
    total_exp   = sum(float(r[3]) * int(r[4]) for r in rows if len(r) > 4) if rows else 0.0

    stat_data = [
        ['Signal Statistics', 'Value', 'Notes'],
        ['Total Duplicate Submissions', f'{total_dupes:,}',                 'Across all flagged pairs'],
        ['Total Financial Exposure',    f'\u20b9{total_exp/100000:,.2f} Lakhs', 'Gross Claim Amount \u00d7 Duplicates'],
    ]
    t = Table(stat_data, colWidths=[53*mm, 35*mm, 66*mm])
    t.setStyle(tbl_style())
    story.append(t)
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph('Top Flagged Cases', S_H2))
    hdr = [['Patient ID', 'Hospital ID', 'Date', 'Claim Amt (\u20b9)', 'Duplicates']]
    tbl = hdr + [
        [Paragraph(r[0], S_SMALL), Paragraph(r[1] if r[1] else 'NULL', S_SMALL),
         Paragraph(r[2][:10], S_SMALL), Paragraph(f'{float(r[3]):,.2f}', S_SMALL),
         Paragraph(crit(r[4]), S_SMALL)]
        for r in rows[:15] if len(r) > 4
    ]
    t2 = Table(tbl, colWidths=[22*mm, 44*mm, 24*mm, 33*mm, 30*mm])
    t2.setStyle(tbl_style())
    story.append(t2)
    story.append(Spacer(1, 10*mm))

def build_fa_02(story):
    story.append(Paragraph('FA-02 \u2014 SIMULTANEOUS ADMISSIONS', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))
    story.append(Paragraph(
        "A beneficiary profile is shown as admitted to two different hospitals at the exact same "
        "time. This is physically impossible and proves identity misuse or card cloning.", S_BODY))
    story.append(Spacer(1, 5*mm))

    rows = read_csv('Point11_Predictive_Identity_Misuse.csv')
    stat_data = [
        ['Signal Statistics', 'Value', 'Notes'],
        ['Total Impossible Overlaps', f'{len(rows)}',  'Simultaneous admission pairs'],
        ['Status',                    Paragraph(crit('CRITICAL'), S_SMALL), 'Requires immediate suspension'],
    ]
    t = Table(stat_data, colWidths=[53*mm, 35*mm, 66*mm])
    t.setStyle(tbl_style())
    story.append(t)
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph('Top Flagged Cases', S_H2))
    hdr = [['Patient ID', 'Hospital A', 'Hospital B', 'Admission A', 'Admission B']]
    tbl = hdr + [
        [Paragraph(r[0], S_SMALL), Paragraph(r[1], S_SMALL), Paragraph(r[2], S_SMALL),
         Paragraph(r[3][:10], S_SMALL), Paragraph(r[4][:10], S_SMALL)]
        for r in rows[:15] if len(r) > 4
    ]
    t2 = Table(tbl, colWidths=[22*mm, 33*mm, 33*mm, 30*mm, 30*mm])
    t2.setStyle(tbl_style())
    story.append(t2)
    story.append(PageBreak())

def build_fa_03(story):
    story.append(Paragraph('FA-03 \u2014 SYNTHETIC IDENTITIES', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))
    story.append(Paragraph(
        "Multiple distinct beneficiary profiles share the exact same Government UID (Aadhaar). "
        "Bulk sharing of a single UID across dozens of profiles strongly indicates fabricated "
        "identities created to funnel fraudulent claims.", S_BODY))
    story.append(Spacer(1, 5*mm))

    rows = read_csv('Point11_ID_Duplication.csv')
    total_profiles = sum(int(r[1]) for r in rows if len(r) > 1) if rows else 0
    stat_data = [
        ['Signal Statistics', 'Value', 'Notes'],
        ['Total Profiles Sharing UIDs', f'{total_profiles:,}',                        'Spanning top flagged UIDs'],
        ['Largest Cluster',             Paragraph(crit(f'{rows[0][1] if rows else 0} profiles'), S_SMALL), 'Sharing a single UID'],
    ]
    t = Table(stat_data, colWidths=[53*mm, 35*mm, 66*mm])
    t.setStyle(tbl_style())
    story.append(t)
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph('Top UID Clusters', S_H2))
    hdr = [['Govt UID', 'Profiles', 'Sample Names Associated']]
    tbl = hdr + [
        [Paragraph(r[0], S_SMALL), Paragraph(crit(r[1]), S_SMALL),
         Paragraph((r[2][:80] + '...') if len(r[2]) > 80 else r[2], S_SMALL)]
        for r in rows[:15] if len(r) > 2
    ]
    t2 = Table(tbl, colWidths=[33*mm, 15*mm, 105*mm])
    t2.setStyle(tbl_style())
    story.append(t2)
    story.append(Spacer(1, 10*mm))

def build_fa_04(story):
    story.append(Paragraph("FA-04 \u2014 CLAIM SPLITTING (REVOLVING DOOR)", S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))
    story.append(Paragraph(
        "A hospital repeatedly discharges and readmits the same patient within a very short window "
        "— sometimes the same day — to generate a new base admission fee per episode, or unbundles "
        "daily claims to bypass package billing limits.", S_BODY))
    story.append(Spacer(1, 5*mm))

    rows = read_csv('Repeated_Claim_Splitting_Unbundling.csv')
    stat_data = [
        ['Signal Statistics', 'Value', 'Notes'],
        ['Patient-Hospital Pairs',   f'{len(rows)}+',                                  'Top pairs shown'],
        ['Highest Single-Day Claims', Paragraph(crit(f'{rows[0][3] if rows else 0}'), S_SMALL), 'Unbundled on same day'],
    ]
    t = Table(stat_data, colWidths=[53*mm, 35*mm, 66*mm])
    t.setStyle(tbl_style())
    story.append(t)
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph('Top Flagged Cases', S_H2))
    hdr = [['Hospital ID', 'Patient ID', 'Admission Date', 'Daily Claims', 'Daily Billed (\u20b9)']]
    tbl = hdr + [
        [Paragraph(r[1] if len(r) > 1 and r[1] else 'NULL', S_SMALL), Paragraph(r[0], S_SMALL),
         Paragraph(r[2][:10], S_SMALL), Paragraph(crit(r[3]), S_SMALL),
         Paragraph(f'{float(r[4]):,.2f}', S_SMALL)]
        for r in rows[:15] if len(r) > 4
    ]
    t2 = Table(tbl, colWidths=[38*mm, 29*mm, 29*mm, 24*mm, 33*mm])
    t2.setStyle(tbl_style())
    story.append(t2)
    story.append(PageBreak())

def build_fa_05(story):
    story.append(Paragraph('FA-05 \u2014 POST-DEATH BILLING (LAZARUS PATTERN)', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))
    story.append(Paragraph(
        "Highly specific, high-confidence fraud: claims are submitted for patients after their "
        "recorded date of death in the ECHS system. Any such submission is a definitive fraud "
        "indicator requiring immediate payment freeze.", S_BODY))
    story.append(Spacer(1, 5*mm))

    rows = read_csv('Anecdotal_1_Lazarus_Post_Death_Billing.csv')
    stat_data = [
        ['Signal Statistics', 'Value', 'Notes'],
        ['Post-Death Claims Found', Paragraph(crit(f'{len(rows)}'), S_SMALL), 'Zero tolerance \u2014 all require investigation'],
        ['Action Required',         Paragraph(crit('IMMEDIATE'), S_SMALL),    'Freeze payment cycle pending audit'],
    ]
    t = Table(stat_data, colWidths=[53*mm, 35*mm, 66*mm])
    t.setStyle(tbl_style())
    story.append(t)
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph('Lazarus Pattern Cases', S_H2))
    if rows:
        hdr = [['Deceased Patient ID', 'Date of Death', 'Zombie Admission', 'Hospital ID', 'Amount (\u20b9)']]
        tbl = hdr + [
            [Paragraph(r[0], S_SMALL), Paragraph(r[1], S_SMALL), Paragraph(r[2][:10], S_SMALL),
             Paragraph(r[3], S_SMALL), Paragraph(r[4], S_SMALL)]
            for r in rows[:15] if len(r) > 4
        ]
        t2 = Table(tbl, colWidths=[33*mm, 29*mm, 29*mm, 33*mm, 29*mm])
        t2.setStyle(tbl_style())
        story.append(t2)
    else:
        story.append(Paragraph('No post-death billing cases detected in current dataset.', S_BODYL))
    story.append(Spacer(1, 6*mm))

    # Alert box using table (same pattern as gen_20module_report.py)
    alert_data = [[Paragraph(
        f'{crit("ESCALATION REQUIRED:")} Any hospital submitting a claim for a patient officially '
        'recorded as deceased must have its payment cycle frozen immediately pending a full physical audit. '
        'This pattern cannot be explained by data entry error alone.', S_WARN)]]
    t_alert = Table(alert_data, colWidths=[154*mm])
    t_alert.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,-1), HexColor('#fff0f0')),
        ('BOX',          (0,0), (-1,-1), 1.5, RED),
        ('LEFTPADDING',  (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING',   (0,0), (-1,-1), 8),
        ('BOTTOMPADDING',(0,0), (-1,-1), 8),
    ]))
    story.append(t_alert)

# ── Document builder ──────────────────────────────────────────────────────────
def build():
    OUTPUT_PATH = '/home/aman/Desktop/echs_analysis/new_reports/Module_11.pdf'
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # Compute live stats for cover page
    dup_rows    = read_csv('Repeated_Exact_Duplicates.csv')
    sim_rows    = read_csv('Point11_Predictive_Identity_Misuse.csv')
    uid_rows    = read_csv('Point11_ID_Duplication.csv')
    dupes       = sum(int(r[4]) for r in dup_rows if len(r) > 4) if dup_rows else 0
    exposure_l  = sum(float(r[3]) * int(r[4]) for r in dup_rows if len(r) > 4) / 100000 if dup_rows else 0.0
    sim_adm     = len(sim_rows)
    uid_clusters = len(uid_rows)

    doc = BaseDocTemplate(OUTPUT_PATH, pagesize=A4,
                          topMargin=25*mm, bottomMargin=25*mm,
                          leftMargin=25*mm, rightMargin=25*mm)
    frame      = Frame(25*mm, 20*mm, W-50*mm, H-45*mm, id='main')
    inner      = PageTemplate(id='inner', frames=[frame], onPage=inner_hf)
    cover_frame = Frame(0, 0, W, H, leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0, id='cover')
    cover_tmpl  = PageTemplate(id='cover', frames=[cover_frame])
    doc.addPageTemplates([cover_tmpl, inner])

    story = [CoverPage(dupes=dupes, exposure_l=exposure_l,
                       sim_adm=sim_adm, uid_clusters=uid_clusters), PageBreak()]
    build_executive_summary(story)
    build_fa_01(story)
    build_fa_02(story)
    build_fa_03(story)
    build_fa_04(story)
    build_fa_05(story)

    doc.build(story)
    print(f'PDF saved: {OUTPUT_PATH}')

if __name__ == '__main__':
    build()
