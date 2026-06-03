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

class CoverPage(Flowable):
    def __init__(self): super().__init__(); self.width=W; self.height=H
    def draw(self):
        c = self.canv
        # Full navy background
        c.setFillColor(NAVY); c.rect(0, 0, W, H, fill=1, stroke=0)
        # Top & bottom gold bars
        c.setFillColor(GOLD);  c.rect(0, H-8*mm, W, 8*mm, fill=1, stroke=0)
        c.setFillColor(GOLD);  c.rect(0, 0, W, 5*mm, fill=1, stroke=0)
        # Geometric stripe pattern
        for i, x in enumerate([0, W*0.28, W*0.56, W*0.84]):
            c.setFillColor(GOLD if i % 2 == 0 else HexColor('#2a3d6a'))
            c.rect(x, H*0.62, W*0.25, H*0.28, fill=1, stroke=0)
        # Navy overlay on stripes for text area
        c.setFillColor(NAVY)
        c.rect(18*mm, H*0.63+2, W-36*mm, H*0.26-4, fill=1, stroke=0)
        # Header text
        c.setFillColor(white); c.setFont('Helvetica-Bold', 9)
        c.drawCentredString(W/2, H*0.86, 'GOVERNMENT OF INDIA  |  EX-SERVICEMEN CONTRIBUTORY HEALTH SCHEME')
        c.setFont('Helvetica', 8); c.setFillColor(HexColor('#aabbcc'))
        c.drawCentredString(W/2, H*0.83, 'Fraud Analytics & Intelligence Report')
        # Main title
        c.setFont('Helvetica-Bold', 28); c.setFillColor(GOLD)
        c.drawCentredString(W/2, H*0.76, 'ECHS FRAUD ANALYTICS')
        c.setFont('Helvetica-Bold', 18); c.setFillColor(white)
        c.drawCentredString(W/2, H*0.70, 'MODULE 11: DUPLICATE CLAIMS & IDENTITY MISUSE')
        c.setFont('Helvetica', 10); c.setFillColor(HexColor('#aabbcc'))
        c.drawCentredString(W/2, H*0.655, 'Rule-Based Signal Detection  |  Top Flagged Cases')
        # Gold divider line
        c.setFillColor(GOLD); c.rect(60*mm, H*0.605, W-120*mm, 0.6*mm, fill=1, stroke=0)
        # IIT Kanpur credit
        c.setFont('Helvetica-Bold', 10); c.setFillColor(GOLD)
        c.drawCentredString(W/2, H*0.57, 'IIT KANPUR  ×  ECHS DIRECTORATE')
        c.setFont('Helvetica', 8); c.setFillColor(HexColor('#8899bb'))
        c.drawCentredString(W/2, H*0.54, 'Prepared under Data Analytics Project for Fraud Detection & Audit Efficiency')
        # Metadata boxes
        meta = [
            ('Database Scope', '33.4 Crore Claims  |  ₹55,453 Crore'),
            ('Coverage',       'Full ECHS History via claim_intimation & claim_submission'),
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
        # Footer disclaimer
        c.setFont('Helvetica', 7); c.setFillColor(HexColor('#556688'))
        c.drawCentredString(W/2, 10*mm, 'CONFIDENTIAL — For authorized personnel only. Not for public distribution.')

def inner_hf(canvas, doc):
    canvas.saveState()
    # Top header bar
    canvas.setFillColor(NAVY); canvas.rect(0, H-12*mm, W, 12*mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD); canvas.rect(0, H-12.5*mm, W, 0.5*mm, fill=1, stroke=0)
    canvas.setFont('Helvetica-Bold', 9); canvas.setFillColor(GOLD)
    canvas.drawString(15*mm, H-8*mm, 'ECHS FRAUD ANALYTICS — MODULE 11: DUPLICATE CLAIMS & IDENTITY MISUSE')
    canvas.setFont('Helvetica', 7.5); canvas.setFillColor(HexColor('#aabbcc'))
    canvas.drawRightString(W-15*mm, H-8*mm, 'IIT Kanpur × ECHS Directorate  |  May 2026')
    # Bottom footer bar
    canvas.setFillColor(NAVY); canvas.rect(0, 0, W, 10*mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD); canvas.rect(0, 10*mm, W, 0.5*mm, fill=1, stroke=0)
    canvas.setFont('Helvetica', 7); canvas.setFillColor(HexColor('#8899bb'))
    canvas.drawString(15*mm, 3.5*mm, 'RESTRICTED — Authorized Personnel Only')
    canvas.setFont('Helvetica-Bold', 8); canvas.setFillColor(GOLD)
    canvas.drawRightString(W-15*mm, 3.5*mm, f'Page {doc.page}')
    canvas.restoreState()

def read_csv(filename):
    data = []
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            for row in reader: data.append(row)
    return data

def build_fa_01(story):
    story.append(Paragraph('PATTERN 1 — EXACT DUPLICATE CLAIMS', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))
    story.append(Paragraph("A hospital submits the exact same claim (same patient, exact same admission date, discharge date, and amount) multiple times, generating a new claim ID to double-bill the system. This indicates bypass of basic duplicate checks.", S_BODY))
    
    rows = read_csv('/home/aman/Desktop/echs_analysis/Repeated_Exact_Duplicates.csv')
    total_dupes = sum(int(r[4]) for r in rows) if rows else 0
    total_exposure = sum(float(r[3]) * int(r[4]) for r in rows) if rows else 0.0

    stat_data = [
        ['Signal Statistics', 'Value', 'Notes'],
        ['Total Duplicate Submissions', f'{total_dupes:,}', 'Across all flagged pairs'],
        ['Total Financial Exposure', f'₹{total_exposure/100000:,.2f} Lakhs', 'Gross Claim Amount × Dupes']
    ]
    t_stat = Table(stat_data, colWidths=[53*mm, 35*mm, 70*mm])
    t_stat.setStyle(tbl_style())
    story.append(t_stat)
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph('Top Flagged Cases (Sample)', S_H2))
    table_data = [[bold('Patient ID'), bold('Hospital ID'), bold('Date'), bold('Claim Amt (₹)'), bold('Duplicates')]]
    for r in rows[:15]:
        table_data.append([Paragraph(r[0], S_SMALL), Paragraph(r[1] if r[1] else 'NULL', S_SMALL), 
                           Paragraph(r[2][:10], S_SMALL), Paragraph(f'{float(r[3]):,.2f}', S_SMALL), Paragraph(crit(r[4]), S_SMALL)])
    
    t_cases = Table(table_data, colWidths=[22*mm, 44*mm, 26*mm, 35*mm, 30*mm])
    t_cases.setStyle(tbl_style())
    story.append(t_cases)
    story.append(Spacer(1, 10*mm))

def build_fa_02(story):
    story.append(Paragraph('PATTERN 2 — SIMULTANEOUS ADMISSIONS', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))
    story.append(Paragraph("A beneficiary profile is shown as admitted to two different hospitals at the exact same time. This is physically impossible and provides absolute proof that the identity (physical card or profile) is being misused or cloned concurrently.", S_BODY))
    
    rows = read_csv('/home/aman/Desktop/echs_analysis/Point11_Predictive_Identity_Misuse.csv')
    
    stat_data = [
        [bold('Signal Statistics'), bold('Value'), bold('Notes')],
        ['Total Impossible Overlaps', f'{len(rows)}', 'Simultaneous admissions'],
        ['Status', crit('CRITICAL'), 'Requires immediate suspension']
    ]
    t_stat = Table(stat_data, colWidths=[53*mm, 35*mm, 70*mm])
    t_stat.setStyle(tbl_style())
    story.append(t_stat)
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph('Top Flagged Cases (Sample)', S_H2))
    table_data = [['Patient ID', 'Hospital A', 'Hospital B', 'Admission A', 'Admission B']]
    for r in rows[:15]:
        table_data.append([Paragraph(r[0], S_SMALL), Paragraph(r[1], S_SMALL), Paragraph(r[2], S_SMALL), 
                           Paragraph(r[3][:10], S_SMALL), Paragraph(r[4][:10], S_SMALL)])
    
    t_cases = Table(table_data, colWidths=[22*mm, 35*mm, 35*mm, 30*mm, 30*mm])
    t_cases.setStyle(tbl_style())
    story.append(t_cases)
    story.append(PageBreak())

def build_fa_03(story):
    story.append(Paragraph('PATTERN 3 — SYNTHETIC IDENTITIES', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))
    story.append(Paragraph("Multiple distinct beneficiary profiles share the exact same Government UID (Aadhaar number). Bulk sharing of a single UID across dozens of profiles is a strong indicator that synthetic (fabricated) identities were created to funnel fraudulent claims.", S_BODY))
    
    rows = read_csv('/home/aman/Desktop/echs_analysis/Point11_ID_Duplication.csv')
    total_profiles = sum(int(r[1]) for r in rows) if rows else 0

    stat_data = [
        [bold('Signal Statistics'), bold('Value'), bold('Notes')],
        ['Total Profiles Sharing UIDs', f'{total_profiles:,}', 'Profiles spanning top UIDs'],
        ['Largest Cluster Size', crit(f'{rows[0][1] if rows else 0} profiles'), 'Sharing a single UID']
    ]
    t_stat = Table(stat_data, colWidths=[53*mm, 35*mm, 70*mm])
    t_stat.setStyle(tbl_style())
    story.append(t_stat)
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph('Top Flagged Cases (Sample)', S_H2))
    table_data = [['Govt UID', 'Profiles', 'Sample Names Associated']]
    for r in rows[:15]:
        names = r[2]
        if len(names) > 80: names = names[:77] + '...'
        table_data.append([Paragraph(r[0], S_SMALL), Paragraph(crit(r[1]), S_SMALL), Paragraph(names, S_SMALL)])
    
    t_cases = Table(table_data, colWidths=[35*mm, 17*mm, 106*mm])
    t_cases.setStyle(tbl_style())
    story.append(t_cases)
    story.append(Spacer(1, 10*mm))

def build_fa_04(story):
    story.append(Paragraph("PATTERN 4 — THE 'REVOLVING DOOR'", S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))
    story.append(Paragraph("A hospital repeatedly discharges and readmits the same patient within a very short window — sometimes the same day — solely to generate a new base admission fee for each episode, or unbundles daily claims. This bypasses continuous-stay billing audits.", S_BODY))
    
    rows = read_csv('/home/aman/Desktop/echs_analysis/Repeated_Claim_Splitting_Unbundling.csv')
    
    stat_data = [
        ['Signal Statistics', 'Value', 'Notes'],
        ['Patient-Hospital Pairs', f'{len(rows)}+', 'Top pairs shown'],
        ['Highest Single-Day Claims', Paragraph(crit(f'{rows[0][3] if rows else 0}'), S_SMALL), 'Unbundled on same day']
    ]
    t_stat = Table(stat_data, colWidths=[53*mm, 35*mm, 70*mm])
    t_stat.setStyle(tbl_style())
    story.append(t_stat)
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph('Top Flagged Cases (Sample)', S_H2))
    table_data = [[bold('Hospital ID'), bold('Patient ID'), bold('Admission Date'), bold('Daily Claims'), bold('Daily Billed (₹)')]]
    for r in rows[:15]:
        table_data.append([Paragraph(r[1] if r[1] else 'NULL', S_SMALL), Paragraph(r[0], S_SMALL), 
                           Paragraph(r[2][:10], S_SMALL), Paragraph(crit(r[3]), S_SMALL), Paragraph(f'{float(r[4]):,.2f}', S_SMALL)])
    
    t_cases = Table(table_data, colWidths=[39*mm, 30*mm, 30*mm, 26*mm, 30*mm])
    t_cases.setStyle(tbl_style())
    story.append(t_cases)
    story.append(PageBreak())

def build():
    OUTPUT_PATH = '/home/aman/Desktop/echs_analysis/new_reports/Module_11.pdf'
    
    # Ensure reports directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    doc = BaseDocTemplate(OUTPUT_PATH, pagesize=A4,
                          topMargin=25*mm, bottomMargin=25*mm,
                          leftMargin=25*mm, rightMargin=25*mm)
    frame      = Frame(25*mm, 20*mm, W-50*mm, H-45*mm, id='main')
    inner = PageTemplate(id='inner', frames=[frame], onPage=inner_hf)
    cover_frame = Frame(0, 0, W, H, leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0, id='cover')
    cover_tmpl = PageTemplate(id='cover', frames=[cover_frame])
    doc.addPageTemplates([cover_tmpl, inner])

    story = [CoverPage(), PageBreak()]
    
    # Intro
    story.append(Paragraph('EXECUTIVE SUMMARY', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))
    story.append(Paragraph("This report presents the findings of ECHS Fraud Analytics patterns FA-01 through FA-04 — a systematic screening exercise applied to ECHS claims data. The analysis uses independent rule-based checks, each designed to detect a specific billing pattern associated with fraud or irregular conduct.", S_BODY))
    story.append(Paragraph("NOTE: This report is produced by an automated screening system. Every flagged case is an investigative lead, not a confirmed finding. A qualified auditor must review each case before any action is taken.", S_WARN))
    story.append(Spacer(1, 10*mm))
    
    build_fa_01(story)
    build_fa_02(story)
    build_fa_03(story)
    build_fa_04(story)
    
    doc.build(story)
    print(f'PDF saved: {OUTPUT_PATH}')

if __name__ == '__main__':
    build()
