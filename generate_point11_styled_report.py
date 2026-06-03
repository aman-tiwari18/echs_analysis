#!/usr/bin/env python3
"""
ECHS Point 11 Fraud Detection Report
Styled exactly like the 20-Module Framework Report
Using comprehensive data from last 5 years analysis
"""
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

# Exact color palette from reference
NAVY   = HexColor('#1a2744')
GOLD   = HexColor('#c8a84b')
RED    = HexColor('#cc2222')
ORANGE = HexColor('#d46a00')
GREEN  = HexColor('#1a6e1a')
LGRAY  = HexColor('#f4f4f4')
MGRAY  = HexColor('#dddddd')
DGRAY  = HexColor('#444444')
LBLUE  = HexColor('#e8ecf5')

# Exact paragraph styles from reference
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

# Exact table style from reference
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

# CSV helper
def read_csv(filename):
    data = []
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                data.append(row)
    return data

# Cover Page - exact style from reference
class CoverPage(Flowable):
    def __init__(self): 
        super().__init__()
        self.width = W
        self.height = H
    
    def draw(self):
        c = self.canv
        c.setFillColor(NAVY); c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(GOLD);  c.rect(0, H-8*mm, W, 8*mm, fill=1, stroke=0)
        c.setFillColor(GOLD);  c.rect(0, 0, W, 5*mm, fill=1, stroke=0)
        
        # Decorative blocks
        for i, x in enumerate([0, W*0.28, W*0.56, W*0.84]):
            c.setFillColor(GOLD if i % 2 == 0 else HexColor('#2a3d6a'))
            c.rect(x, H*0.62, W*0.25, H*0.28, fill=1, stroke=0)
        
        # Center content box
        c.setFillColor(NAVY)
        c.rect(18*mm, H*0.63+2, W-36*mm, H*0.26-4, fill=1, stroke=0)
        
        # Header text
        c.setFillColor(white); c.setFont('Helvetica-Bold', 9)
        c.drawCentredString(W/2, H*0.86, 'GOVERNMENT OF INDIA  |  EX-SERVICEMEN CONTRIBUTORY HEALTH SCHEME')
        c.setFont('Helvetica', 8); c.setFillColor(HexColor('#aabbcc'))
        c.drawCentredString(W/2, H*0.83, 'Fraud Analytics & Intelligence Report')
        
        # Main title
        c.setFont('Helvetica-Bold', 28); c.setFillColor(GOLD)
        c.drawCentredString(W/2, H*0.76, 'POINT 11 ANALYSIS')
        
        # Subtitle
        c.setFont('Helvetica-Bold', 18); c.setFillColor(white)
        c.drawCentredString(W/2, H*0.70, 'DUPLICATE CLAIMS & IDENTITY FRAUD')
        
        # Sub-subtitle
        c.setFont('Helvetica', 10); c.setFillColor(HexColor('#aabbcc'))
        c.drawCentredString(W/2, H*0.655, '8 Fraud Patterns  |  Last 5 Years  |  Complete Descriptive Data')
        
        # Gold divider
        c.setFillColor(GOLD); c.rect(60*mm, H*0.605, W-120*mm, 0.6*mm, fill=1, stroke=0)
        
        # IIT Kanpur branding
        c.setFont('Helvetica-Bold', 10); c.setFillColor(GOLD)
        c.drawCentredString(W/2, H*0.57, 'IIT KANPUR  ×  ECHS DIRECTORATE')
        c.setFont('Helvetica', 8); c.setFillColor(HexColor('#8899bb'))
        c.drawCentredString(W/2, H*0.54, 'Prepared under Point 11 Fraud Detection — Identity Misuse & Duplicate Claims')
        
        # Metadata boxes
        meta = [
            ('Analysis Period', 'Last 5 Years (2021–2026)'),
            ('Total Cases Flagged', '4,006 Fraud Cases Detected'),
            ('Report Date', 'June 2026'),
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
        
        # Footer
        c.setFont('Helvetica', 7); c.setFillColor(HexColor('#556688'))
        c.drawCentredString(W/2, 10*mm, 'CONFIDENTIAL — For authorized personnel only. Not for public distribution.')

# Inner header / footer - exact style from reference
def inner_hf(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY); canvas.rect(0, H-12*mm, W, 12*mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD); canvas.rect(0, H-12.5*mm, W, 0.5*mm, fill=1, stroke=0)
    canvas.setFont('Helvetica-Bold', 9); canvas.setFillColor(GOLD)
    canvas.drawString(15*mm, H-8*mm, 'ECHS POINT 11 — DUPLICATE CLAIMS & IDENTITY FRAUD DETECTION')
    canvas.setFont('Helvetica', 7.5); canvas.setFillColor(HexColor('#aabbcc'))
    canvas.drawRightString(W-15*mm, H-8*mm, 'IIT Kanpur × ECHS Directorate  |  June 2026')
    canvas.setFillColor(NAVY); canvas.rect(0, 0, W, 10*mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD); canvas.rect(0, 10*mm, W, 0.5*mm, fill=1, stroke=0)
    canvas.setFont('Helvetica', 7); canvas.setFillColor(HexColor('#8899bb'))
    canvas.drawString(15*mm, 3.5*mm, 'RESTRICTED — Authorized Personnel Only')
    canvas.setFont('Helvetica-Bold', 8); canvas.setFillColor(GOLD)
    canvas.drawRightString(W-15*mm, 3.5*mm, f'Page {doc.page}')
    canvas.restoreState()

# Module block builder - exact style from reference
def pattern_block(num, title, risk, tables, metric, threshold, finding, cases, note=None):
    """Return a KeepTogether block for one fraud pattern."""
    risk_colors = {'CRITICAL': ('#cc2222','#fff0f0'), 'HIGH': ('#d46a00','#fff5ee'),
                   'MEDIUM': ('#8a6000','#fffbe8'), 'LOW': ('#1a6e1a','#f0fff0')}
    rc, bg = risk_colors.get(risk, ('#444','#fff'))

    elems = []
    # Header row
    hdr_data = [[
        Paragraph(f'<font color="#c8a84b"><b>PATTERN {num:02d}</b></font>  '
                  f'<font color="white"><b>{title}</b></font>', 
                  bs(fontSize=10, textColor=white, fontName='Helvetica-Bold', leading=13)),
        Paragraph(f'<font color="#c8a84b"><b>{cases:,} CASES</b></font>', 
                  bs(fontSize=8, textColor=GOLD, alignment=TA_RIGHT, fontName='Helvetica-Bold'))
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
        [Paragraph(bold('Data Completeness:'), bs(fontSize=8, textColor=NAVY, fontName='Helvetica-Bold')),
         Paragraph(ok('100% Complete')  + ' — Full hospital names, locations, patient details included', bs(fontSize=8, leading=12))],
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
        ('BOTTOMPADDING',(0,0), (-1,-1), 3),
        ('LEFTPADDING',  (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('LINEBELOW', (0,-1), (-1,-1), 0.5, HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [HexColor(bg)]),
    ]))

    elems.append(hdr_tbl)
    elems.append(body_tbl)
    elems.append(Spacer(1, 5*mm))
    return KeepTogether(elems)

# Pattern data
PATTERNS = [
    dict(num=1, title='Duplicate Card IDs',
         risk='CRITICAL', cases=500,
         tables='claim_intimation, office_master, cghs_region_master',
         metric='Unique service numbers per card; unique beneficiary names per card',
         threshold='COUNT(DISTINCT service_no) > 1 per card',
         finding='Single ECHS card number used by multiple different service numbers and beneficiaries '
                 'indicates card cloning or identity theft. Physical card should be unique to one beneficiary.'),

    dict(num=2, title='Simultaneous Admissions',
         risk='CRITICAL', cases=500,
         tables='claim_intimation (self-join), claim_submission, office_master',
         metric='Overlapping admission dates at different hospitals',
         threshold='Same beneficiary admitted to ≥2 hospitals on same date',
         finding='Patient shown as admitted to two or more different hospitals at overlapping times. '
                 'This is physically impossible and proves identity misuse or card sharing.'),

    dict(num=3, title='Duplicate Bill Numbers',
         risk='HIGH', cases=500,
         tables='claim_submission, claim_intimation, office_master',
         metric='Bill number repetition across different claims',
         threshold='Same bill number used >1 time',
         finding='Same bill number submitted multiple times for different claims, beneficiaries, or dates. '
                 'Indicates systematic billing fraud or recycling of authentic hospital bills.'),

    dict(num=4, title='Mobile Number Rings',
         risk='HIGH', cases=500,
         tables='claim_intimation, office_master, cghs_region_master',
         metric='Unique cards and service numbers per mobile',
         threshold='Mobile linked to ≥5 different cards',
         finding='Single mobile number linked to multiple unrelated ECHS cards and service numbers. '
                 'Suggests organized fraud rings using a central contact point to coordinate fake claims.'),

    dict(num=5, title='UID Duplication (Synthetic Identities)',
         risk='CRITICAL', cases=500,
         tables='claim_intimation, office_master, cghs_region_master',
         metric='Unique service numbers sharing same Aadhaar UID',
         threshold='COUNT(DISTINCT service_no) > 1 per UID',
         finding='Same Aadhaar UID number shared by multiple different service numbers and profiles. '
                 'Indicates synthetic identity creation for fraudulent claim submission.'),

    dict(num=6, title='Post-Death Claims (Lazarus Pattern)',
         risk='CRITICAL', cases=500,
         tables='claim_intimation, claim_submission, office_master, relation_master',
         metric='Admission date after recorded death date',
         threshold='Admission date > death date  OR  Submission >90 days after death',
         finding='Claims submitted for patients AFTER their recorded date of death in ECHS system. '
                 'This is definitive fraud with zero tolerance — all cases require immediate investigation.',
         note='Named "Lazarus Pattern" after biblical resurrection. Impossible unless data error.'),

    dict(num=7, title='Chronic Stay (Forever Patient)',
         risk='HIGH', cases=506,
         tables='claim_intimation, claim_submission, office_master, relation_master',
         metric='Continuous hospital stay duration in days',
         threshold='Stay duration > 90 days continuously',
         finding='Patients with extremely long continuous hospital stays suggesting possible abuse '
                 'of per-diem payments or fabricated admissions for recurring billing.'),

    dict(num=8, title='High Frequency Claims',
         risk='HIGH', cases=500,
         tables='claim_intimation, claim_submission, office_master, service_master, rank_master',
         metric='Total claims per beneficiary in analysis period',
         threshold='≥10 distinct claims per service number',
         finding='Beneficiaries with unusually high number of claims suggesting possible '
                 'overutilization, unnecessary procedures, or claim fabrication by colluding providers.'),
]

def build():
    OUT = 'ECHS_Fraud_Analytics_Module_11.pdf'
    
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

    # Page 2: Analysis Scope & Database Overview
    story.append(Paragraph('ANALYSIS SCOPE & DATABASE OVERVIEW', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))

    scope_data = [
        [bold('Parameter'), bold('Detail')],
        ['Database', 'ECHS Production (samar.iitk.ac.in:3306)'],
        ['Analysis Period', 'Last 5 Years (2021–2026)  |  DATE_SUB(CURDATE(), INTERVAL 5 YEAR)'],
        ['Primary Tables', 'claim_intimation, claim_submission, office_master, cghs_region_master, state_master'],
        ['Master Tables', 'relation_master, service_master, rank_master (for complete descriptions)'],
        ['Total Records Analyzed', '26+ Million Claims from ECHS database'],
        ['Fraud Cases Detected', '4,006 Cases flagged across 8 patterns'],
        ['Data Completeness', '100% — Every ID includes full names, locations, demographics'],
        ['Execution Date', 'June 3, 2026  |  Complete analysis finalized'],
    ]
    t = Table(scope_data, colWidths=[45*mm, 130*mm])
    t.setStyle(tbl_style())
    story += [t, Spacer(1, 6*mm)]

    story.append(Paragraph('COMPLETE DESCRIPTIVE INFORMATION INCLUDED', S_H2))
    info_data = [
        [bold('Category'), bold('Information Provided'), bold('Source Tables')],
        ['Hospital Info', 'ID, Name, City, State, Address, CGHS Region', 'office_master, cghs_region_master, state_master'],
        ['Beneficiary', 'Service No., Name, Rank, Service Type, Card No.', 'claim_intimation, rank_master, service_master'],
        ['Patient', 'Name, Age, Gender, Relationship, UID Number', 'claim_intimation, relation_master'],
        ['Claim Details', 'Dates, Amounts, Doctor, Ailment, Stage, Status', 'claim_intimation, claim_submission'],
    ]
    t2 = Table(info_data, colWidths=[30*mm, 75*mm, 70*mm])
    t2.setStyle(tbl_style())
    story += [t2, Spacer(1, 3*mm)]

    story.append(Paragraph(
        f'{bold("No Additional Database Access Required:")} All flagged cases include complete descriptive '
        'information. Investigators can proceed with verification immediately without querying the database again. '
        'Hospital names, locations, patient demographics, and beneficiary details are fully populated in all CSV files.',
        S_BODY))
    story.append(PageBreak())

    # Pages 3-6: Pattern blocks (2 per page)
    story.append(Paragraph('8 FRAUD PATTERNS — POINT 11 DETECTION FRAMEWORK', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=8))

    for i, p in enumerate(PATTERNS):
        story.append(pattern_block(**p))
        if (i + 1) % 2 == 0 and i < len(PATTERNS) - 1:
            story.append(PageBreak())
            story.append(Paragraph('8 FRAUD PATTERNS — POINT 11 FRAMEWORK (continued)', S_H1))
            story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=8))

    story.append(PageBreak())

    # Consolidated Risk Matrix
    story.append(Paragraph('CONSOLIDATED RISK MATRIX — ALL 8 PATTERNS', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))

    matrix_hdr = [[bold('#'), bold('Pattern'), bold('Cases'), bold('Risk'), bold('Priority')]]
    risk_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
    sorted_patterns = sorted(PATTERNS, key=lambda p: (risk_order.get(p['risk'], 9), p['num']))

    for p in sorted_patterns:
        risk_fmt = {'CRITICAL': crit(p['risk']), 'HIGH': high(p['risk']),
                    'MEDIUM': bold(p['risk']), 'LOW': ok(p['risk'])}.get(p['risk'], p['risk'])
        priority = crit('IMMEDIATE') if p['risk'] == 'CRITICAL' else high('URGENT')
        matrix_hdr.append([
            Paragraph(f'{p["num"]:02d}', S_SMALL),
            Paragraph(p['title'], S_SMALL),
            Paragraph(f'{p["cases"]:,}', S_SMALL),
            Paragraph(risk_fmt, S_SMALL),
            Paragraph(priority, S_SMALL),
        ])
    t3 = Table(matrix_hdr, colWidths=[10*mm, 82*mm, 20*mm, 25*mm, 38*mm])
    t3.setStyle(tbl_style())
    story.append(t3)
    story.append(Spacer(1, 5*mm))

    # Summary
    critical_count = sum(1 for p in PATTERNS if p['risk'] == 'CRITICAL')
    high_count = sum(1 for p in PATTERNS if p['risk'] == 'HIGH')
    critical_cases = sum(p['cases'] for p in PATTERNS if p['risk'] == 'CRITICAL')
    high_cases = sum(p['cases'] for p in PATTERNS if p['risk'] == 'HIGH')
    
    story.append(Paragraph(
        f'Risk Distribution: {crit(str(critical_count)+" CRITICAL")} patterns ({critical_cases:,} cases) '
        f'| {high(str(high_count)+" HIGH")} patterns ({high_cases:,} cases).  '
        f'{bold("Immediate Action Required:")} Patterns 01, 02, 05, 06 (CRITICAL) — '
        'Suspend payment cycles pending investigation.  '
        f'{bold("Urgent Review:")} Patterns 03, 04, 07, 08 (HIGH) — '
        'Initiate verification procedures within 7 days.',
        S_BODY))
    story.append(Spacer(1, 6*mm))

    # Action Items
    story.append(Paragraph('RECOMMENDED IMMEDIATE ACTIONS', S_H2))
    actions = [
        'Pattern 01 (Duplicate Cards): Freeze all cards with >1 service number. Physical card inspection required.',
        'Pattern 02 (Simultaneous Admissions): Suspend both hospitals pending investigation — physical impossibility.',
        'Pattern 05 (UID Duplication): Verify Aadhaar records. Flag all service numbers sharing UID for identity audit.',
        'Pattern 06 (Lazarus): Zero tolerance — immediate payment freeze for all post-death claims.',
        'Pattern 03 (Duplicate Bills): Audit hospital billing systems. Check for bill number reuse or system fraud.',
        'Pattern 04 (Mobile Rings): Investigate coordinated fraud rings. Single contact managing multiple identities.',
        'Pattern 07 (Chronic Stay): Review admissions >90 days for medical justification. Check room charge abuse.',
        'Pattern 08 (High Frequency): Verify medical necessity for 10+ claims. Check provider-patient collusion.',
    ]
    for i, action in enumerate(actions, 1):
        story.append(Paragraph(f'{i}. {action}', S_BULL))
    story.append(Spacer(1, 6*mm))

    # Data Files Reference
    story.append(Paragraph('OUTPUT FILES & DATA ACCESS', S_H2))
    story.append(Paragraph(
        'All fraud detection data is available in CSV format with complete information. '
        'Each file contains up to 500 top flagged cases per pattern:',
        S_BODY))
    story.append(Spacer(1, 3*mm))

    files_data = [
        [bold('Pattern'), bold('File Name'), bold('Records')],
        ['01 — Duplicate Card IDs', '01_Duplicate_Card_IDs.csv', '500'],
        ['02 — Simultaneous Admissions', '02_Simultaneous_Admissions.csv', '500'],
        ['03 — Duplicate Bill Numbers', '03_Duplicate_Bill_Numbers.csv', '500'],
        ['04 — Mobile Number Rings', '04_Mobile_Number_Rings.csv', '500'],
        ['05 — UID Duplication', '05_UID_Duplication.csv', '500'],
        ['06 — Post-Death Claims', '06_Post_Death_Claims_Lazarus.csv', '500'],
        ['07 — Chronic Stay', '07_Chronic_Stay_Forever_Patient.csv', '506'],
        ['08 — High Frequency', '08_High_Frequency_Claims.csv', '500'],
    ]
    t4 = Table(files_data, colWidths=[35*mm, 70*mm, 20*mm])
    t4.setStyle(tbl_style())
    story.append(t4)
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph(
        f'{bold("Additional Data:")} Point11_Fraud_Detection_Complete_Data.json (5.3 MB) contains all '
        'structured data with metadata and can be imported into analytical tools for further processing.',
        S_BODY))

    doc.build(story)
    print(f'\n{"="*80}')
    print(f'PDF GENERATION COMPLETE')
    print(f'{"="*80}')
    print(f'Output: {OUT}')
    print(f'Styled exactly like the 20-Module Framework Report')
    print(f'Total Patterns: 8')
    print(f'Total Cases: 4,006')
    print(f'{"="*80}\n')

if __name__ == '__main__':
    build()
