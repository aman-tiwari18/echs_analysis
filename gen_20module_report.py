from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable

W, H = A4

NAVY   = HexColor('#1a2744')
GOLD   = HexColor('#c8a84b')
RED    = HexColor('#cc2222')
ORANGE = HexColor('#d46a00')
GREEN  = HexColor('#1a6e1a')
LGRAY  = HexColor('#f4f4f4')
MGRAY  = HexColor('#dddddd')
DGRAY  = HexColor('#444444')
LBLUE  = HexColor('#e8ecf5')

def bs(**kw):
    defaults = dict(fontName='Helvetica', fontSize=9, leading=13, textColor=DGRAY, spaceAfter=3)
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
        ('TOPPADDING',   (0,0), (-1,-1), 3),
        ('BOTTOMPADDING',(0,0), (-1,-1), 3),
        ('LEFTPADDING',  (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ])

# ─── Cover Page ───────────────────────────────────────────────────────────────
class CoverPage(Flowable):
    def __init__(self): super().__init__(); self.width=W; self.height=H
    def draw(self):
        c = self.canv
        c.setFillColor(NAVY); c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(GOLD);  c.rect(0, H-8*mm, W, 8*mm, fill=1, stroke=0)
        c.setFillColor(GOLD);  c.rect(0, 0, W, 5*mm, fill=1, stroke=0)
        for i, x in enumerate([0, W*0.28, W*0.56, W*0.84]):
            c.setFillColor(GOLD if i % 2 == 0 else HexColor('#2a3d6a'))
            c.rect(x, H*0.62, W*0.25, H*0.28, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.rect(18*mm, H*0.63+2, W-36*mm, H*0.26-4, fill=1, stroke=0)
        c.setFillColor(white); c.setFont('Helvetica-Bold', 9)
        c.drawCentredString(W/2, H*0.86, 'GOVERNMENT OF INDIA  |  EX-SERVICEMEN CONTRIBUTORY HEALTH SCHEME')
        c.setFont('Helvetica', 8); c.setFillColor(HexColor('#aabbcc'))
        c.drawCentredString(W/2, H*0.83, 'Fraud Analytics & Intelligence Report')
        c.setFont('Helvetica-Bold', 28); c.setFillColor(GOLD)
        c.drawCentredString(W/2, H*0.76, 'ECHS FRAUD ANALYTICS')
        c.setFont('Helvetica-Bold', 18); c.setFillColor(white)
        c.drawCentredString(W/2, H*0.70, '20-MODULE DETECTION FRAMEWORK')
        c.setFont('Helvetica', 10); c.setFillColor(HexColor('#aabbcc'))
        c.drawCentredString(W/2, H*0.655, 'SQL Query Library  |  Fraud Typology Reference  |  VPN Risk Assessment')
        c.setFillColor(GOLD); c.rect(60*mm, H*0.605, W-120*mm, 0.6*mm, fill=1, stroke=0)
        c.setFont('Helvetica-Bold', 10); c.setFillColor(GOLD)
        c.drawCentredString(W/2, H*0.57, 'IIT KANPUR  ×  ECHS DIRECTORATE')
        c.setFont('Helvetica', 8); c.setFillColor(HexColor('#8899bb'))
        c.drawCentredString(W/2, H*0.54, 'Prepared under Data Analytics Project for Fraud Detection & Audit Efficiency')
        meta = [
            ('Database Scope', '33.4 Crore Claims  |  ₹55,453 Crore'),
            ('Coverage',       'Full ECHS History via settlement_stat'),
            ('Report Date',    'May 2026'),
            ('Classification', 'RESTRICTED — OFFICIAL USE ONLY'),
        ]
        bx, by, bw, bh = 30*mm, H*0.31, W-60*mm, 18*mm
        for i, (lbl, val) in enumerate(meta):
            y = by + (len(meta)-1-i) * (bh+2*mm)
            c.setFillColor(HexColor('#0d1929')); c.rect(bx, y, bw, bh, fill=1, stroke=0)
            c.setStrokeColor(GOLD); c.setLineWidth(0.5); c.rect(bx, y, bw, bh, fill=0, stroke=1)
            c.setFont('Helvetica-Bold', 7); c.setFillColor(GOLD)
            c.drawString(bx+5*mm, y+bh-5*mm, lbl.upper())
            c.setFont('Helvetica', 9); c.setFillColor(white)
            c.drawString(bx+5*mm, y+3*mm, val)
        c.setFont('Helvetica', 7); c.setFillColor(HexColor('#556688'))
        c.drawCentredString(W/2, 10*mm, 'CONFIDENTIAL — For authorized personnel only. Not for public distribution.')


# ─── Inner header / footer ────────────────────────────────────────────────────
def inner_hf(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY); canvas.rect(0, H-12*mm, W, 12*mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD); canvas.rect(0, H-12.5*mm, W, 0.5*mm, fill=1, stroke=0)
    canvas.setFont('Helvetica-Bold', 9); canvas.setFillColor(GOLD)
    canvas.drawString(15*mm, H-8*mm, 'ECHS FRAUD ANALYTICS — 20-MODULE DETECTION FRAMEWORK')
    canvas.setFont('Helvetica', 7.5); canvas.setFillColor(HexColor('#aabbcc'))
    canvas.drawRightString(W-15*mm, H-8*mm, 'IIT Kanpur × ECHS Directorate  |  May 2026')
    canvas.setFillColor(NAVY); canvas.rect(0, 0, W, 10*mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD); canvas.rect(0, 10*mm, W, 0.5*mm, fill=1, stroke=0)
    canvas.setFont('Helvetica', 7); canvas.setFillColor(HexColor('#8899bb'))
    canvas.drawString(15*mm, 3.5*mm, 'RESTRICTED — Authorized Personnel Only')
    canvas.setFont('Helvetica-Bold', 8); canvas.setFillColor(GOLD)
    canvas.drawRightString(W-15*mm, 3.5*mm, f'Page {doc.page}')
    canvas.restoreState()


# ─── Risk badge helper ────────────────────────────────────────────────────────
class RiskBadge(Flowable):
    COLORS = {'CRITICAL': RED, 'HIGH': ORANGE, 'MEDIUM': HexColor('#c8a84b'), 'LOW': GREEN}
    def __init__(self, level, w=38*mm, h=6*mm):
        super().__init__()
        self.level = level
        self.width = w
        self.height = h
    def draw(self):
        c = self.canv
        col = self.COLORS.get(self.level, MGRAY)
        c.setFillColor(col); c.roundRect(0, 0, self.width, self.height, 2, fill=1, stroke=0)
        c.setFont('Helvetica-Bold', 8); c.setFillColor(white)
        c.drawCentredString(self.width/2, 1.5*mm, f'▲  {self.level} RISK')


# ─── Module block builder ─────────────────────────────────────────────────────
def module_block(num, title, risk, category, tables, metric, threshold,
                 queries, finding, note=None):
    """Return a KeepTogether block for one fraud module."""
    safe_c = sum(1 for q in queries if '[SAFE]' in q)
    heavy_c = len(queries) - safe_c

    risk_colors = {'CRITICAL': ('#cc2222','#fff0f0'), 'HIGH': ('#d46a00','#fff5ee'),
                   'MEDIUM': ('#8a6000','#fffbe8'), 'LOW': ('#1a6e1a','#f0fff0')}
    rc, bg = risk_colors.get(risk, ('#444','#fff'))

    elems = []
    # Header row
    hdr_data = [[
        Paragraph(f'<font color="#c8a84b"><b>MODULE {num:02d}</b></font>  '
                  f'<font color="white"><b>{title}</b></font>', bs(fontSize=10, textColor=white, fontName='Helvetica-Bold', leading=13)),
        Paragraph(f'<font color="#c8a84b"><b>{category}</b></font>', bs(fontSize=8, textColor=GOLD, alignment=TA_RIGHT, fontName='Helvetica-Bold'))
    ]]
    hdr_tbl = Table(hdr_data, colWidths=[130*mm, 45*mm])
    hdr_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (0,-1), 6),
        ('RIGHTPADDING', (-1,0), (-1,-1), 6),
    ]))

    # Body row
    body_rows = [
        [Paragraph(bold('Fraud Indicator:'), bs(fontSize=8, textColor=NAVY, fontName='Helvetica-Bold')),
         Paragraph(finding, bs(fontSize=8, leading=12))],
        [Paragraph(bold('Key Tables:'), bs(fontSize=8, textColor=NAVY, fontName='Helvetica-Bold')),
         Paragraph(f'<font face="Courier" size="8">{tables}</font>', bs(fontSize=8, leading=11))],
        [Paragraph(bold('Primary Metric:'), bs(fontSize=8, textColor=NAVY, fontName='Helvetica-Bold')),
         Paragraph(metric, bs(fontSize=8, leading=12))],
        [Paragraph(bold('Detection Threshold:'), bs(fontSize=8, textColor=NAVY, fontName='Helvetica-Bold')),
         Paragraph(f'<font color="{rc}"><b>{threshold}</b></font>', bs(fontSize=8, leading=12))],
        [Paragraph(bold('Queries:'), bs(fontSize=8, textColor=NAVY, fontName='Helvetica-Bold')),
         Paragraph(f'{len(queries)} queries  |  '
                   f'{ok(str(safe_c)+" SAFE")}  '
                   f'{"  "+high(str(heavy_c)+" HEAVY") if heavy_c else ""}',
                   bs(fontSize=8, leading=12))],
    ]
    if note:
        body_rows.append([
            Paragraph(bold('Note:'), bs(fontSize=8, textColor=RED, fontName='Helvetica-Bold')),
            Paragraph(f'<font color="#cc2222">{note}</font>', bs(fontSize=8, leading=12))
        ])

    body_tbl = Table(body_rows, colWidths=[35*mm, 140*mm])
    body_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor(bg)),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('LINEBELOW', (0,-1), (-1,-1), 0.5, HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [HexColor(bg)]),
    ]))

    elems.append(hdr_tbl)
    elems.append(body_tbl)
    elems.append(Spacer(1, 5*mm))
    return KeepTogether(elems)


# ─── Module data ──────────────────────────────────────────────────────────────
MODULES = [
    dict(num=1, title='Hospital Revenue Inflation & Behavioural Shift',
         risk='HIGH', category='Annual / Periodic',
         tables='settlement_stat, office_master',
         metric='YoY revenue growth %, IPD/OPD ratio shift, deduction rate',
         threshold='>30% annual growth  |  IPD/OPD ratio > 1  |  Deduction > 25%',
         queries=['[SAFE] Q1a: YoY Revenue Growth', '[SAFE] Q1b: IPD/OPD Ratio', '[SAFE] Q1c: Deduction Rate'],
         finding='Hospitals showing >30% revenue growth or sudden IPD surge indicate inflated billing. '
                 'Deduction rate >25% at settlement confirms systemic overbilling.'),

    dict(num=2, title='Procedure-Level Upcoding Detection',
         risk='HIGH', category='Claim-Level',
         tables='hosp_exp_det, claim_intimation, office_master',
         metric='Avg deduction % per procedure category; high-value procedure frequency',
         threshold='Avg deduction >25% on procedures billed >₹10,000',
         queries=['[HEAVY] Q2a: Category Deduction by Hospital', '[HEAVY] Q2b: High-Value Procedure Deductions',
                  '[SAFE] Q2c: Category-wise Deduction Proxy'],
         finding='Hospitals repeatedly billing high-value procedures that attract >25% deductions are '
                 'systematically upcoding — charging for higher-tariff procedures than performed.'),

    dict(num=3, title='Doctor-Level Referral & Admission Pattern',
         risk='CRITICAL', category='Provider-Level',
         tables='claim_submission (CS_TREAT_DOCT), claim_intimation, office_master',
         metric='IPD conversion rate per doctor; hospitals per doctor; family referral clustering',
         threshold='IPD rate >70% per doctor  |  Same doctor at >2 hospitals  |  Family repeat ≥2 members',
         queries=['[HEAVY] Q3a: IPD Conversion Rate', '[HEAVY] Q3b: Multi-Hospital Doctors',
                  '[HEAVY] Q3c: Family Referral Repeat'],
         finding='Doctors with >70% IPD conversion are driving unnecessary admissions. '
                 'Doctors linked to >2 hospitals suggest referral syndicates.',
         note='No dedicated doctor master table — CS_TREAT_DOCT is free text, may have spelling variants.'),

    dict(num=4, title='Beneficiary-Level Utilisation Outliers',
         risk='HIGH', category='Beneficiary-Level',
         tables='claim_intimation, claim_submission, office_master',
         metric='Claim count per beneficiary; hospital count; total claimed amount',
         threshold='>6 claims/year per beneficiary  |  ≥3 hospitals visited',
         queries=['[HEAVY] Q4a: High-Frequency Claimants', '[HEAVY] Q4b: Multi-Hospital Beneficiaries',
                  '[SAFE] Q4c: Relation-wise Distribution'],
         finding='Beneficiaries with >6 annual claims or visiting ≥3 hospitals suggest '
                 'collusion with providers or identity misuse for repeated billing.'),

    dict(num=5, title='Repeat Admission Analysis',
         risk='HIGH', category='Monthly / Quarterly / Annual',
         tables='claim_intimation (self-join), office_master',
         metric='Readmission within 30 days; monthly/quarterly admission count per patient',
         threshold='Readmission ≤30 days  |  >1 IPD/month  |  >3 IPD/quarter  |  >6 IPD/year',
         queries=['[HEAVY] Q5a: 30-Day Readmissions', '[HEAVY] Q5b: Monthly Repeat',
                  '[HEAVY] Q5c: Quarterly Repeat'],
         finding='Staged admissions involve brief discharges followed by immediate readmission '
                 'to bill for additional stays. Exclusions: dialysis, chemotherapy, cataract.',
         note='Self-join on claim_intimation is VPN-heavy. Always run with LIMIT 200.'),

    dict(num=6, title='Pharmacy Billing Abuse',
         risk='MEDIUM', category='Claim-Level',
         tables='hosp_exp_det (HED_CAT_DESC), claim_intimation, office_master',
         metric='Pharmacy % of total billing; high-cost drug prescription frequency',
         threshold='Pharmacy billing >30% of total claim value per hospital',
         queries=['[HEAVY] Q6a: Pharmacy % by Hospital', '[HEAVY] Q6b: Top Over-Prescribed Drugs'],
         finding='Hospitals where pharmacy billing exceeds 30% of the claim value are likely '
                 'inflating drug costs or billing for non-administered medications.'),

    dict(num=7, title='Emergency Admission Misuse',
         risk='MEDIUM', category='Monthly / Quarterly',
         tables='claim_intimation (CI_IS_RTA), settlement_stat, office_master',
         metric='RTA/emergency rate per hospital; repeat emergency per beneficiary in quarter',
         threshold='Emergency rate outlier >3× peer average  |  >2 emergencies/quarter per patient',
         queries=['[HEAVY] Q7a: RTA Rate by Hospital', '[SAFE] Q7b: Monthly Volume Trend',
                  '[HEAVY] Q7c: Repeat Emergency per Beneficiary'],
         finding='Misclassifying elective admissions as emergencies bypasses pre-auth '
                 'requirements. CI_IS_RTA = 1 flags Road Traffic Accident/emergency cases.',
         note='Full emergency flag may need patient_type lookup. CI_IS_RTA is best available proxy.'),

    dict(num=8, title='Package vs Item Billing Anomaly',
         risk='HIGH', category='Claim-Level',
         tables='hosp_exp_det (HED_PROC_TYPE), claim_intimation, office_master',
         metric='Package vs item billing ratio; same procedure on same claim (double billing)',
         threshold='Same procedure code appearing >1× on single claim  |  Mixed billing types',
         queries=['[HEAVY] Q8a: Package/Item Mix', '[HEAVY] Q8b: Double Billing',
                  '[HEAVY] Q8c: Mixed Billing Claims'],
         finding='Double billing = same procedure billed twice on same intimation. '
                 'Mixed billing = both package and itemized claims on the same admission.'),

    dict(num=9, title='Geo-Spatial Fraud Clustering',
         risk='MEDIUM', category='Regional',
         tables='settlement_stat, office_master (OM_OFFICE_STATE_ID), claim_intimation',
         metric='Regional deduction rate; cross-state claims; high-deduction hospital clusters',
         threshold='Region deduction rate >15%  |  Cross-state claims >20 per hospital',
         queries=['[SAFE] Q9a: Regional Deduction Rate', '[HEAVY] Q9b: Cross-State Claims',
                  '[SAFE] Q9c: Top 20 Hospitals by Deduction'],
         finding='Cross-state claims where patient state ≠ hospital state may indicate '
                 'fictitious claims or coordinated regional fraud rings.'),

    dict(num=10, title='Time-Series Surge Detection',
         risk='HIGH', category='Monthly / Quarterly',
         tables='settlement_stat',
         metric='Monthly billing volume and amount; quarter-end surges; hospital-level surge ratio',
         threshold='Monthly claims >3× 12-month average for that hospital  |  March/December spikes',
         queries=['[SAFE] Q10a: Monthly Trend All Years', '[SAFE] Q10b: Quarter-End Detection',
                  '[SAFE] Q10c: Hospital-Level Surge'],
         finding='Artificial billing spikes in March (FY close) and December indicate '
                 'hospitals rushing to exhaust empanelment limits or exploit policy windows.'),

    dict(num=11, title='Duplicate Claims Detection',
         risk='CRITICAL', category='Claim-Level',
         tables='claim_intimation, claim_submission (self-join)',
         metric='Same beneficiary + date + amount; simultaneous dual-hospital admissions',
         threshold='Any exact duplicate triplet  |  Same patient, two hospitals, same admission date',
         queries=['[HEAVY] Q11a: Exact Duplicates', '[HEAVY] Q11b: Simultaneous Admissions',
                  '[HEAVY] Q11c: Service No. Duplication'],
         finding='Exact duplicates = same claim submitted twice. '
                 'Simultaneous admissions in two hospitals on the same date are physically impossible.',
         note='Self-join queries are slow. Run Q11a first (most actionable). Use LIMIT 200.'),

    dict(num=12, title='Hospital Specialty Misuse',
         risk='HIGH', category='Provider-Level',
         tables='office_master (OM_HOSP_TYPE, OM_NABH), settlement_stat, hosp_exp_det',
         metric='Procedures billed vs hospital type; NABH vs non-NABH deduction rates',
         threshold='Diagnostic labs (type 3) billing IPD = direct fraud flag',
         queries=['[SAFE] Q12a: NABH vs Non-NABH Rates', '[HEAVY] Q12b: Specialty Mismatch',
                  '[HEAVY] Q12c: Labs Billing IPD'],
         finding='Diagnostic labs are not authorized for IPD procedures. '
                 'Non-NABH hospitals claiming at NABH rates are policy violations. '
                 'Prior analysis confirmed PROGNOSIS LABORATORIES (ID 3112) as a flagged case.'),

    dict(num=13, title='High-Value Claim Risk Scoring',
         risk='CRITICAL', category='Claim-Level',
         tables='claim_intimation, claim_submission, office_master',
         metric='Claims >₹5 lakh with >25% deduction; top percentile by hospital',
         threshold='Claim value >₹5,00,000  |  Deduction rate >25% on high-value claims',
         queries=['[HEAVY] Q13a: Top High-Value Claims', '[HEAVY] Q13b: High-Value + High Deduction',
                  '[SAFE] Q13c: Regional High-Value Volume'],
         finding='High-value claims with systematic >25% deductions indicate '
                 'price inflation, upcoding, or billing for unreceived premium services.'),

    dict(num=14, title='Pre-Authorization Deviation',
         risk='HIGH', category='Pre-Auth vs Actual',
         tables='pre_auth (PA_EST_COST, PA_APPROVED), claim_intimation, claim_submission',
         metric='Pre-auth estimate vs actual claim deviation %; claims without pre-auth',
         threshold='Actual claim >25% above pre-auth estimate  |  Claims >₹1L without pre-auth',
         queries=['[MEDIUM] Q14a: Pre-Auth Deviation by Hospital', '[MEDIUM] Q14b: No Pre-Auth Claims',
                  '[MEDIUM] Q14c: Escalation Pattern'],
         finding='Hospitals that consistently bill 25%+ above their pre-auth estimates '
                 'are gaming the approval system. High-value claims without pre-auth bypass controls.'),

    dict(num=15, title='Length of Stay Manipulation',
         risk='HIGH', category='Claim-Level',
         tables='claim_intimation (CI_EXP_DOD, CI_EXTENDED_STAY), claim_submission',
         metric='Expected LOS vs billing period; extended stay claims by hospital',
         threshold='Expected LOS >14 days  |  CI_EXTENDED_STAY flag present',
         queries=['[SAFE] Q15a: Room Category Utilisation', '[HEAVY] Q15b: Expected Discharge Anomaly',
                  '[HEAVY] Q15c: Extended Stay by Hospital'],
         finding='Hospitals that inflate Length of Stay beyond clinical necessity bill '
                 'additional room charges, nursing, and procedure days.'),

    dict(num=16, title='Diagnostic Test Overutilisation',
         risk='MEDIUM', category='Claim-Level',
         tables='hosp_exp_det (HED_CAT_DESC), claim_intimation, office_master',
         metric='Lab/diagnostic % of total claim; standalone labs billing IPD',
         threshold='Lab billing >20% of total claim value  |  Labs (type 3) with IPD claims',
         queries=['[HEAVY] Q16a: Lab % by Hospital', '[HEAVY] Q16b: Labs Billing IPD',
                  '[HEAVY] Q16c: Most Duplicated Tests'],
         finding='Excessive diagnostic testing inflates claim values without clinical justification. '
                 'Standalone labs billing IPD admissions is a direct policy violation.'),

    dict(num=17, title='Network Collusion Detection',
         risk='CRITICAL', category='Multi-Entity',
         tables='claim_intimation, claim_submission, office_master',
         metric='Beneficiary-hospital repeat visits; doctor linked to multiple hospitals; '
                'service number with >5 dependents',
         threshold='Doctor at >3 hospitals  |  Patient >10 visits to same hospital  |  >5 dependents/service no.',
         queries=['[HEAVY] Q17a: Beneficiary-Hospital Links', '[HEAVY] Q17b: Doctor-Hospital Collusion',
                  '[HEAVY] Q17c: Service No. Anomalous Dependents'],
         finding='Network collusion involves coordinated fraud rings where doctors, hospitals, '
                 'and beneficiaries work together to generate fictitious or inflated claims.'),

    dict(num=18, title='Claim Processing Delay Analysis',
         risk='MEDIUM', category='Operational',
         tables='claim_submission (CS_SUB_DATE, CS_SETTLE_DATE), claim_intimation',
         metric='Average days to settle; same-day settlements; monthly submission surge',
         threshold='Same-day settlement on claims >₹50,000 = internal collusion flag',
         queries=['[HEAVY] Q18a: Avg Processing Days by Hospital', '[HEAVY] Q18b: Same-Day Settlements',
                  '[HEAVY] Q18c: Monthly Submission Volume'],
         finding='Same-day settlement of high-value claims bypasses normal review cycles '
                 'and may indicate internal insider fraud at processing offices.'),

    dict(num=19, title='Policy Abuse Patterns',
         risk='HIGH', category='System-Level',
         tables='claim_intimation, claim_submission, office_master',
         metric='% claims above 25% deduction threshold; room entitlement mismatch; '
                'non-empanelled hospital usage',
         threshold='>30% of a hospital\'s claims exceeding 25% deduction = systemic policy abuse',
         queries=['[HEAVY] Q19a: Hospitals Above 25% Threshold', '[HEAVY] Q19b: Room Entitlement Mismatch',
                  '[HEAVY] Q19c: Non-Empanelled Hospital Claims'],
         finding='Recurring exploitation of policy gaps: billing higher room categories than entitled, '
                 'using non-empanelled facilities, or gaming the 25% deduction threshold.'),

    dict(num=20, title='Budget Impact & Leakage Estimation',
         risk='HIGH', category='Strategic',
         tables='settlement_stat, office_master',
         metric='Annual claimed vs approved vs deducted; leakage % by hospital type; '
                'projected fraud recovery',
         threshold='Deduction rate >10.34% (system average) = above-average risk',
         queries=['[SAFE] Q20a: Annual Trend', '[SAFE] Q20b: Leakage by Hospital Type',
                  '[SAFE] Q20c: Overall Leakage Summary'],
         finding='System-level leakage estimated at ₹5,735 Cr deducted from ₹55,453 Cr claimed '
                 '(10.34%). Conservative fraud estimate: ₹1,720 Cr/yr. Moderate: ₹2,868 Cr/yr.'),
]

# ─── Repeat event data ────────────────────────────────────────────────────────
REPEAT_MONTHLY = [
    ('Multiple family members (ESM + Deps) treated in same hospital in same month',
     'CI_SERVICE_NO + hospital + month GROUP BY', 'family_members ≥ 2', '[HEAVY] RE-1'),
    ('Major procedure (IPD) performed >2 times in a month for same patient',
     'CI_PATIENT_TYPE=I + month GROUP BY card', 'ipd_in_month > 2', '[HEAVY] RE-3'),
    ('IPD/OPD ratio > 1 at hospital level',
     'settlement_stat PAT_TYPE pivot', 'ipd/opd_ratio > 1', '[SAFE] Q1b'),
    ('Referral per polyclinic > 30%',
     'settlement_stat SS_REF_TYPE_ID % by office', 'ref_pct > 30%', '[SAFE] RE-10'),
    ('Emergency admission >2 in a month per patient',
     'CI_IS_RTA=1 + month GROUP BY card', 'emergency_count > 2', '[HEAVY] Q7c'),
    ('Repeat OPD visits >4 in a month per patient',
     'CI_PATIENT_TYPE=O + month GROUP BY card', 'opd_visits > 4', '[HEAVY] RE-2'),
    ('Repeat admissions of single patient >1 in a month',
     'CI_ADMISSION_DATE month GROUP BY card', 'admissions > 1', '[HEAVY] Q5b'),
    ('Simultaneous admission ESM and dependent in same hospital',
     'CI_SERVICE_NO + hospital + date GROUP BY', 'family_admitted ≥ 2', '[HEAVY] RE-5'),
    ('Overlapping admissions in multiple hospitals same day',
     'claim_intimation self-join on card + date', 'same date different hospital', '[HEAVY] Q11b'),
    ('Claimed vs approved >25% in a single claim',
     'claim_submission amount ratio', '(claimed-approved)/claimed > 0.25', '[HEAVY] RE-4'),
]

REPEAT_QUARTERLY = [
    ('Major procedure >3 times in a quarter per patient', 'Q PARTITION BY card', 'ipd_per_qtr > 3', '[HEAVY]'),
    ('Repeat admissions >3 in a quarter', 'Q PARTITION BY card', 'admissions_qtr > 3', '[HEAVY] Q5c'),
    ('OPD visits >12 in a quarter', 'Q PARTITION BY card', 'opd_qtr > 12', '[HEAVY]'),
    ('Emergency admission >3 in a quarter', 'CI_IS_RTA + QUARTER()', 'emergency_qtr > 3', '[HEAVY] Q7c'),
]

REPEAT_ANNUAL = [
    ('YoY revenue increase >30%', 'settlement_stat FY pivot', 'growth_pct > 30', '[SAFE] Q1a / RE-6'),
    ('Major procedure >5 times in a year per patient', 'YEAR() GROUP BY card', 'ipd_yr > 5', '[HEAVY] RE-7'),
    ('Repeat admissions >6 in a year per patient', 'YEAR() GROUP BY card', 'admissions_yr > 6', '[HEAVY] RE-9'),
    ('OPD visits >12 in a year per patient', 'YEAR() GROUP BY card', 'opd_yr > 12', '[HEAVY] RE-8'),
    ('Emergency admissions >12 in a year', 'CI_IS_RTA YEAR() GROUP BY card', 'emergency_yr > 12', '[HEAVY]'),
    ('Claimed vs approved >25% in any claim during year', 'claim_submission ratio', '>25%', '[SAFE] Q1c'),
]

# ─── VPN risk data ────────────────────────────────────────────────────────────
VPN_RISKS = [
    ('Connection Timeout', 'CRITICAL',
     'Self-join queries on claim_intimation (~100M+ rows) can run for hours. VPN with small '
     'bandwidth will disconnect mid-query, returning no result or partial data.'),
    ('Partial Result Sets', 'HIGH',
     'Queries on hosp_exp_det without date filters may return incomplete aggregates '
     'if VPN drops. Results appear valid but are statistically wrong.'),
    ('Table Lock Risk', 'HIGH',
     'Long-running heavy queries may hold read locks on InnoDB tables, slowing '
     'other active users on the production DB (10.192.206.91:3306).'),
    ('3 Tables Effectively Inaccessible', 'CRITICAL',
     'claim_remarks (413M rows, 95.7 GB), audit_remarks (245M rows), '
     'document_submitted (244M rows) cannot be queried over VPN within reasonable time.'),
    ('No Real-Time Scoring', 'HIGH',
     'ML-based real-time fraud scoring (Module 13) requires sub-second response. '
     'VPN adds 80–200ms latency per packet; large result sets are impractical.'),
    ('Bandwidth Saturation', 'MEDIUM',
     'Large result sets (>10,000 rows) saturate a small VPN pipe. '
     'Use LIMIT and GROUP BY to reduce output before transmission.'),
    ('No Parallel Execution', 'MEDIUM',
     'Cannot run multiple heavy queries simultaneously. Each must complete before '
     'the next starts to avoid VPN saturation and connection drops.'),
    ('Index Benefit Wasted', 'LOW',
     'Even well-indexed queries require the MySQL optimizer to communicate the plan '
     'over VPN. Complex plans with 3+ table joins add significant round-trip overhead.'),
]

VPN_SOLUTIONS = [
    'Use settlement_stat for all baseline analysis — 18 of 65 queries are [SAFE].',
    'Add LIMIT clause to every [HEAVY] query before running.',
    'Use date/hospital WHERE filters to reduce working set: WHERE CI_HOSPITAL_ID = X.',
    'Schedule heavy queries (Q2a, Q5a, Q11b) during off-hours (2–6 AM IST).',
    'Request a local dump of key columns from claim_intimation + claim_submission.',
    'Consider ETL: extract flagged rows to a smaller analytical table.',
    'Use MySQL streaming: add LIMIT 500 → process → next batch (cursor pagination).',
    'Run one module per VPN session. Do not chain heavy queries end-to-end.',
]


# ─── Main build ────────────────────────────────────────────────────────────────
def build():
    OUT = '/home/abhishekpathak/Downloads/ECHS/ECHS_20Module_Framework_Report.pdf'
    doc = BaseDocTemplate(OUT, pagesize=A4,
                          topMargin=16*mm, bottomMargin=14*mm,
                          leftMargin=15*mm, rightMargin=15*mm)
    frame = Frame(15*mm, 14*mm, W-30*mm, H-30*mm, id='main')
    inner = PageTemplate(id='inner', frames=[frame], onPage=inner_hf)
    cover_frame = Frame(0, 0, W, H, leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0, id='cover')
    cover_tmpl = PageTemplate(id='cover', frames=[cover_frame])
    doc.addPageTemplates([cover_tmpl, inner])

    story = [CoverPage(), PageBreak()]

    # ── Page 2: Scope + Database + VPN intro ──────────────────────────────────
    story.append(Paragraph('ANALYTICAL SCOPE & DATABASE OVERVIEW', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))

    scope_data = [
        [bold('Database'), bold('Detail')],
        ['Host', '10.192.206.91:3306  (MySQL 8.x)'],
        ['Schema', 'echs  |  319 tables  |  ~499 GB total'],
        ['Primary Tables', 'settlement_stat, claim_intimation, claim_submission, hosp_exp_det, office_master, pre_auth'],
        ['Claim Universe', '33.4 Crore claims  |  ₹55,453 Crore total claimed'],
        ['Deductions', '₹5,735 Crore deducted  |  Overall deduction rate: 10.34%'],
        ['History Tables', 'his_claim_intimation, his_claim_submission (Oct 2025–Mar 2026 snapshot only)'],
        ['VPN Connection', 'Cisco AnyConnect  |  Client: 10.26.35.90  |  Server: 164.100.28.19  |  DTLSv1.2'],
    ]
    t = Table(scope_data, colWidths=[45*mm, 130*mm])
    t.setStyle(tbl_style())
    story += [t, Spacer(1, 6*mm)]

    story.append(Paragraph('QUERY SAFETY CLASSIFICATION', S_H2))
    safety_data = [
        [bold('Level'), bold('Description'), bold('Tables Used'), bold('Run Time'), bold('VPN Safe')],
        ['[SAFE]',   'Uses settlement_stat only',       'settlement_stat, office_master',         '< 2 sec',   ok('YES')],
        ['[MEDIUM]', 'Small join on master + pre_auth', 'pre_auth, claim_intimation (indexed)',   '5–30 sec',  high('CAUTION')],
        ['[HEAVY]',  'Full table scan with LIMIT',      'claim_intimation, hosp_exp_det, CS',     '30s–5 min', crit('LIMIT REQUIRED')],
    ]
    t2 = Table(safety_data, colWidths=[22*mm, 60*mm, 65*mm, 22*mm, 26*mm])
    t2.setStyle(tbl_style())
    story += [t2, Spacer(1, 3*mm)]

    story.append(Paragraph(
        f'Of the {bold("65 total queries")} in this framework: '
        f'{ok("18 are [SAFE]")} and can be run anytime.  '
        f'{high("6 are [MEDIUM]")} and require a stable connection.  '
        f'{crit("41 are [HEAVY]")} and must always include a LIMIT clause.',
        S_BODY))
    story.append(PageBreak())

    # ── Pages 3–12: Module blocks (2 per page) ───────────────────────────────
    story.append(Paragraph('20-MODULE FRAUD DETECTION FRAMEWORK', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=8))

    for i, m in enumerate(MODULES):
        story.append(module_block(**m))
        if (i + 1) % 2 == 0 and i < len(MODULES) - 1:
            story.append(PageBreak())
            story.append(Paragraph('20-MODULE FRAUD DETECTION FRAMEWORK (continued)', S_H1))
            story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=8))

    story.append(PageBreak())

    # ── Repeat Event Flags ───────────────────────────────────────────────────
    story.append(Paragraph('REPEAT EVENT FLAG LIBRARY', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=4))
    story.append(Paragraph(
        'The following flags are derived from the fraud criteria document. '
        'Each flag maps to a specific SQL query in echs_20module_queries.sql.',
        S_BODY))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph('Monthly Flags', S_H2))
    mh = [[bold('Rule'), bold('SQL Approach'), bold('Threshold'), bold('Query')]]
    for row in REPEAT_MONTHLY:
        mh.append([Paragraph(row[0], S_SMALL), Paragraph(f'<font face="Courier" size="7">{row[1]}</font>', S_SMALL),
                   Paragraph(f'<b>{row[2]}</b>', S_SMALL), Paragraph(row[3], S_SMALL)])
    t3 = Table(mh, colWidths=[68*mm, 52*mm, 34*mm, 21*mm])
    t3.setStyle(tbl_style())
    story += [t3, Spacer(1, 5*mm)]

    story.append(Paragraph('Quarterly Flags', S_H2))
    qh = [[bold('Rule'), bold('SQL Approach'), bold('Threshold'), bold('Query')]]
    for row in REPEAT_QUARTERLY:
        qh.append([Paragraph(row[0], S_SMALL), Paragraph(f'<font face="Courier" size="7">{row[1]}</font>', S_SMALL),
                   Paragraph(f'<b>{row[2]}</b>', S_SMALL), Paragraph(row[3], S_SMALL)])
    t4 = Table(qh, colWidths=[68*mm, 52*mm, 34*mm, 21*mm])
    t4.setStyle(tbl_style())
    story += [t4, Spacer(1, 5*mm)]

    story.append(Paragraph('Annual Flags', S_H2))
    ah = [[bold('Rule'), bold('SQL Approach'), bold('Threshold'), bold('Query')]]
    for row in REPEAT_ANNUAL:
        ah.append([Paragraph(row[0], S_SMALL), Paragraph(f'<font face="Courier" size="7">{row[1]}</font>', S_SMALL),
                   Paragraph(f'<b>{row[2]}</b>', S_SMALL), Paragraph(row[3], S_SMALL)])
    t5 = Table(ah, colWidths=[68*mm, 52*mm, 34*mm, 21*mm])
    t5.setStyle(tbl_style())
    story += [t5]
    story.append(PageBreak())

    # ── VPN Risk Analysis ────────────────────────────────────────────────────
    story.append(Paragraph('VPN ACCESS LIMITATIONS & FRAUD ANALYSIS CONSEQUENCES', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))
    story.append(Paragraph(
        'The ECHS production database (499 GB) is accessible only via Cisco AnyConnect VPN '
        '(Client: 10.26.35.90 → Server: 164.100.28.19). This creates significant constraints '
        'for large-scale fraud analysis. The following risks and consequences apply:',
        S_BODY))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph('Risk Assessment', S_H2))
    vh = [[bold('Risk'), bold('Severity'), bold('Impact on Fraud Analysis')]]
    for risk_name, sev, impact in VPN_RISKS:
        sev_col = {'CRITICAL': crit(sev), 'HIGH': high(sev), 'MEDIUM': bold(sev), 'LOW': ok(sev)}.get(sev, sev)
        vh.append([Paragraph(risk_name, S_SMALL), Paragraph(sev_col, S_SMALL),
                   Paragraph(impact, S_SMALL)])
    t6 = Table(vh, colWidths=[46*mm, 22*mm, 107*mm])
    t6.setStyle(tbl_style())
    story += [t6, Spacer(1, 6*mm)]

    story.append(Paragraph('Key Consequence: Three Major Tables Inaccessible', S_H2))
    inacc_data = [
        [bold('Table'), bold('Rows'), bold('Size'), bold('Fraud Signal Lost')],
        ['claim_remarks',      '413 Million', '95.7 GB',
         'Rejection reason text — identifies what auditors flagged as non-payable'],
        ['audit_remarks',      '245 Million', 'Large',
         'Full audit trail — identifies which claims were manually reviewed and why'],
        ['document_submitted', '244 Million', 'Large',
         'Document tracking — identifies claims with missing or forged supporting documents'],
    ]
    t7 = Table(inacc_data, colWidths=[40*mm, 22*mm, 18*mm, 95*mm])
    t7.setStyle(tbl_style())
    story += [t7, Spacer(1, 6*mm)]

    story.append(Paragraph('Recommended Mitigations', S_H2))
    for i, sol in enumerate(VPN_SOLUTIONS, 1):
        story.append(Paragraph(f'{i}. {sol}', S_BULL))
    story.append(Spacer(1, 6*mm))

    story.append(Paragraph('Strategic Recommendation', S_H2))
    story.append(Paragraph(
        'The most impactful long-term solution is to '
        f'{bold("request a database export of key analytical columns")} '
        f'from the ECHS IT team — specifically: {bold("claim_intimation")} (selected columns), '
        f'{bold("claim_submission")} (amounts), and {bold("claim_remarks")} (rejection reasons). '
        'A targeted extract of ~15 columns from these three tables, covering the last 3 financial years, '
        'would be under 20 GB and enable full offline analysis without VPN constraints. '
        'This would unlock all 65 queries at full table scale and enable ML model training for '
        'Module 13 (High-Value Risk Scoring) and Module 17 (Network Collusion Detection).',
        S_BODY))
    story.append(PageBreak())

    # ── Risk Matrix ──────────────────────────────────────────────────────────
    story.append(Paragraph('CONSOLIDATED RISK MATRIX — ALL 20 MODULES', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))

    matrix_hdr = [[bold('Module'), bold('Title'), bold('Category'), bold('Risk'), bold('Queries'), bold('VPN Load')]]
    risk_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
    sorted_modules = sorted(MODULES, key=lambda m: (risk_order.get(m['risk'], 9), m['num']))

    for m in sorted_modules:
        safe_c = sum(1 for q in m['queries'] if '[SAFE]' in q)
        heavy_c = len(m['queries']) - safe_c
        risk_fmt = {'CRITICAL': crit(m['risk']), 'HIGH': high(m['risk']),
                    'MEDIUM': bold(m['risk']), 'LOW': ok(m['risk'])}.get(m['risk'], m['risk'])
        vpn_load = ok('SAFE') if heavy_c == 0 else (crit('HIGH') if heavy_c >= 2 else high('MED'))
        matrix_hdr.append([
            Paragraph(f'{m["num"]:02d}', S_SMALL),
            Paragraph(m['title'], S_SMALL),
            Paragraph(m['category'], S_SMALL),
            Paragraph(risk_fmt, S_SMALL),
            Paragraph(f'{len(m["queries"])} ({safe_c}S/{heavy_c}H)', S_SMALL),
            Paragraph(vpn_load, S_SMALL),
        ])
    t8 = Table(matrix_hdr, colWidths=[10*mm, 69*mm, 30*mm, 22*mm, 22*mm, 22*mm])
    t8.setStyle(tbl_style())
    story.append(t8)
    story.append(Spacer(1, 5*mm))

    # Risk count summary
    risk_counts = {}
    for m in MODULES:
        risk_counts[m['risk']] = risk_counts.get(m['risk'], 0) + 1
    summary_parts = [f'{crit(str(risk_counts.get("CRITICAL",0))+" CRITICAL")}',
                     f'{high(str(risk_counts.get("HIGH",0))+" HIGH")}',
                     f'{bold(str(risk_counts.get("MEDIUM",0))+" MEDIUM")}']
    story.append(Paragraph(
        f'Risk distribution across 20 modules: ' + '  |  '.join(summary_parts) + '.  '
        f'Priority execution order: Modules 3, 11, 12, 13, 17 (CRITICAL) → '
        f'then HIGH-risk modules → MEDIUM.  '
        f'Start with {ok("[SAFE] queries")} to establish baseline before running HEAVY queries.',
        S_BODY))

    doc.build(story)
    print(f'PDF saved: {OUT}')


if __name__ == '__main__':
    build()
