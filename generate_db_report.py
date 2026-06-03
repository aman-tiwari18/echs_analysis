import os
import json
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable

W, H = A4

# ── Colour palette ───────────────────────────────────────────────────────────
NAVY   = HexColor('#1a2744')
GOLD   = HexColor('#c8a84b')
RED    = HexColor('#cc2222')
ORANGE = HexColor('#d46a00')
GREEN  = HexColor('#1a6e1a')
LGRAY  = HexColor('#f4f4f4')
MGRAY  = HexColor('#dddddd')
DGRAY  = HexColor('#444444')
LBLUE  = HexColor('#e8ecf5')

# ── Paragraph styles ─────────────────────────────────────────────────────────
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

def bold(t): return f'<b>{t}</b>'

# ── Table style ──────────────────────────────────────────────────────────────
def tbl_style(hdr=1):
    return TableStyle([
        ('BACKGROUND',   (0,0), (-1, hdr-1), NAVY),
        ('TEXTCOLOR',    (0,0), (-1, hdr-1), white),
        ('FONTNAME',     (0,0), (-1, hdr-1), 'Helvetica-Bold'),
        ('FONTSIZE',     (0,0), (-1,-1), 8.5),
        ('LEADING',      (0,0), (-1,-1), 12),
        ('ROWBACKGROUNDS', (0,hdr), (-1,-1), [white, LGRAY]),
        ('GRID',         (0,0), (-1,-1), 0.35, MGRAY),
        ('LINEBELOW',    (0,0), (-1,0), 0.8, GOLD),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',   (0,0), (-1,-1), 6),
        ('BOTTOMPADDING',(0,0), (-1,-1), 6),
        ('LEFTPADDING',  (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ])

# ── Cover Page ───────────────────────────────────────────────────────────────
class CoverPage(Flowable):
    def __init__(self, total_tables=0, total_size_gb=0.0):
        super().__init__()
        self.width = W; self.height = H
        self.total_tables = total_tables
        self.total_size_gb = total_size_gb

    def draw(self):
        c = self.canv
        # Full navy background
        c.setFillColor(NAVY); c.rect(0, 0, W, H, fill=1, stroke=0)

        # Top header bar
        c.setFillColor(HexColor('#0d1929')); c.rect(0, H-22*mm, W, 22*mm, fill=1, stroke=0)
        c.setFillColor(white); c.setFont('Helvetica-Bold', 8)
        c.drawCentredString(W/2, H-10*mm, 'GOVERNMENT OF INDIA  |  EX-SERVICEMEN CONTRIBUTORY HEALTH SCHEME')
        c.setFont('Helvetica', 7.5); c.setFillColor(HexColor('#aabbcc'))
        c.drawCentredString(W/2, H-16*mm, 'Database Architecture & Metadata Audit')

        # Main title
        c.setFont('Helvetica-Bold', 40); c.setFillColor(GOLD)
        c.drawCentredString(W/2, H-45*mm, 'ECHS DATABASE DICTIONARY')
        
        # Subtitle
        c.setFont('Helvetica', 16); c.setFillColor(white)
        c.drawCentredString(W/2, H-57*mm, 'Comprehensive Table Metadata & Storage Analysis')

        # Module tag line
        c.setFont('Helvetica-Bold', 9); c.setFillColor(GOLD)
        c.drawCentredString(W/2, H-66*mm, 'SYSTEM REPORT  |  MAY 2026  |  CONFIDENTIAL')

        # Gold divider
        c.setStrokeColor(GOLD); c.setLineWidth(1)
        c.line(25*mm, H-71*mm, W-25*mm, H-71*mm)

        # 4-column metrics box
        bx  = 18*mm
        bw  = W - 36*mm
        bh  = 32*mm
        by  = H - 110*mm
        col_w = bw / 4

        metrics = [
            ('DATABASE SCHEMA', 'ECHS'),
            ('TOTAL TABLES',    f'{self.total_tables}'),
            ('TOTAL SIZE',      f'{self.total_size_gb:.1f} GB'),
            ('EXTRACT DATE',    datetime.datetime.now().strftime('%d %b %Y')),
        ]

        c.setStrokeColor(GOLD); c.setLineWidth(1)
        c.rect(bx, by, bw, bh, fill=0, stroke=1)

        for i, (label, value) in enumerate(metrics):
            cx = bx + i * col_w
            c.setFillColor(HexColor('#0d1929'))
            c.rect(cx, by, col_w, bh, fill=1, stroke=0)
            if i > 0:
                c.setStrokeColor(GOLD); c.setLineWidth(0.5)
                c.line(cx, by, cx, by + bh)
            c.setFont('Helvetica-Bold', 7); c.setFillColor(GOLD)
            c.drawCentredString(cx + col_w/2, by + bh - 9*mm, label)
            c.setFont('Helvetica-Bold', 16); c.setFillColor(white)
            c.drawCentredString(cx + col_w/2, by + 8*mm, value)

        c.setStrokeColor(GOLD); c.setLineWidth(1)
        c.rect(bx, by, bw, bh, fill=0, stroke=1)

        # IIT Kanpur footer
        c.setFont('Helvetica-Bold', 10); c.setFillColor(GOLD)
        c.drawCentredString(W/2, 28*mm, 'IIT KANPUR \u2014 Data Analytics & Fraud Intelligence Division')
        c.setFont('Helvetica', 8); c.setFillColor(white)
        c.drawCentredString(W/2, 21*mm, 'Report Date: May 2026  |  Ex-Servicemen Contributory Health Scheme (ECHS)')
        c.setFont('Helvetica', 7); c.setFillColor(HexColor('#556688'))
        c.drawCentredString(W/2, 12*mm, 'CONFIDENTIAL \u2014 For authorized personnel only. Not for public distribution.')

# ── Header / Footer ──────────────────────────────────────────────────────────
def inner_hf(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY); canvas.rect(0, H-12*mm, W, 12*mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD); canvas.rect(0, H-12.5*mm, W, 0.5*mm, fill=1, stroke=0)
    canvas.setFont('Helvetica-Bold', 9); canvas.setFillColor(GOLD)
    canvas.drawString(15*mm, H-8*mm, 'ECHS DATABASE DICTIONARY \u2014 SYSTEM REPORT')
    canvas.setFont('Helvetica', 7.5); canvas.setFillColor(HexColor('#aabbcc'))
    canvas.drawRightString(W-15*mm, H-8*mm, 'IIT Kanpur \u00d7 ECHS Directorate  |  May 2026')
    canvas.setFillColor(NAVY); canvas.rect(0, 0, W, 10*mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD); canvas.rect(0, 10*mm, W, 0.5*mm, fill=1, stroke=0)
    canvas.setFont('Helvetica', 7); canvas.setFillColor(HexColor('#8899bb'))
    canvas.drawString(15*mm, 3.5*mm, 'RESTRICTED \u2014 Authorized Personnel Only')
    canvas.setFont('Helvetica-Bold', 8); canvas.setFillColor(GOLD)
    canvas.drawRightString(W-15*mm, 3.5*mm, f'Page {doc.page}')
    canvas.restoreState()

# ── Document builder ─────────────────────────────────────────────────────────
def build():
    INPUT_JSON = '/home/aman/Desktop/echs_analysis/echs_db_metadata.json'
    OUTPUT_PDF = '/home/aman/Desktop/echs_analysis/new_reports/ECHS_Database_Report.pdf'
    os.makedirs(os.path.dirname(OUTPUT_PDF), exist_ok=True)

    with open(INPUT_JSON, 'r') as f:
        data = json.load(f)

    total_tables = len(data)
    total_size_mb = sum(t.get('data_mb', 0) for t in data)
    total_size_gb = total_size_mb / 1024

    doc = BaseDocTemplate(OUTPUT_PDF, pagesize=A4,
                          topMargin=25*mm, bottomMargin=25*mm,
                          leftMargin=25*mm, rightMargin=25*mm)
    frame = Frame(25*mm, 20*mm, W-50*mm, H-45*mm, id='main')
    inner = PageTemplate(id='inner', frames=[frame], onPage=inner_hf)
    cover_frame = Frame(0, 0, W, H, leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0, id='cover')
    cover_tmpl = PageTemplate(id='cover', frames=[cover_frame])
    doc.addPageTemplates([cover_tmpl, inner])

    story = [CoverPage(total_tables=total_tables, total_size_gb=total_size_gb), PageBreak()]

    story.append(Paragraph('EXECUTIVE SUMMARY', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))
    story.append(Paragraph(
        "This document provides a comprehensive dictionary of the ECHS central database. "
        "It outlines the structural metadata of every base table, grouped into logical functional "
        "domains. This audit is critical for understanding data availability for fraud analytics and system integrations.", S_BODY))
    story.append(Spacer(1, 4*mm))

    def get_group(name):
        n = name.lower()
        if any(x in n for x in ['claim', 'bill', 'settlement', 'reimb', 'payment', 'bpa']): return 'Claims, Billing & BPA'
        if any(x in n for x in ['audit', 'cda', 'remark', 'cfa']): return 'Audits & CDA'
        if any(x in n for x in ['hosp', 'empanel', 'referral', 'document', 'clinic']): return 'Hospitals, Referrals & Documents'
        if any(x in n for x in ['benf', 'patient', 'card', 'dep', 'esm', 'uid']): return 'Beneficiaries & Patients'
        if any(x in n for x in ['user', 'login', 'role']): return 'Users & Access'
        if any(x in n for x in ['master', 'type', 'status', 'category', 'map', 'list']): return 'Master & Config Data'
        if any(x in n for x in ['log', 'trail', 'history', 'sms', 'msg']): return 'Logs & History'
        return 'Other Tables'

    groups = {}
    for t in data:
        g = get_group(t['table'])
        groups.setdefault(g, []).append(t)

    # Sort groups in a logical order
    group_order = [
        'Claims, Billing & BPA', 'Audits & CDA', 'Hospitals, Referrals & Documents',
        'Beneficiaries & Patients', 'Users & Access', 'Master & Config Data',
        'Logs & History', 'Other Tables'
    ]

    story.append(Paragraph('TABLE METADATA DIRECTORY', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))

    for g_name in group_order:
        g_tables = groups.get(g_name, [])
        if not g_tables: continue

        # Sort tables by size descending within the group
        g_tables.sort(key=lambda x: x.get('data_mb', 0), reverse=True)

        story.append(Paragraph(g_name.upper(), S_H2))
        
        hdr = [['Table Name', 'Rows', 'Size (MB)', 'Earliest Date', 'Latest Date']]
        tbl_data = hdr
        
        for t in g_tables:
            name = t['table']
            rows = int(t['row_count']) if t['row_count'] else 0
            size_mb = t.get('data_mb', 0.0)
            earliest = str(t['earliest_date'])[:10] if t['earliest_date'] else 'N/A'
            latest = str(t['latest_date'])[:10] if t['latest_date'] else 'N/A'
            
            # Highlight large tables
            if size_mb > 1000:
                name_p = Paragraph(f'<font color="#cc2222"><b>{name}</b></font>', S_SMALL)
            else:
                name_p = Paragraph(name, S_SMALL)
                
            row_str = f"{rows:,}" + ("*" if not t.get('row_count_exact', True) else "")
            
            tbl_data.append([
                name_p,
                Paragraph(row_str, S_SMALL),
                Paragraph(f"{size_mb:,.1f}", S_SMALL),
                Paragraph(earliest, S_SMALL),
                Paragraph(latest, S_SMALL)
            ])

        # Sum of colWidths = W - 50*mm (which is 160mm) -> 55 + 28 + 22 + 27 + 27 = 159mm
        t_flow = Table(tbl_data, colWidths=[55*mm, 28*mm, 22*mm, 27*mm, 27*mm], repeatRows=1)
        t_flow.setStyle(tbl_style())
        story.append(t_flow)
        story.append(Spacer(1, 6*mm))
    
    story.append(Paragraph("* Approximate row counts used for tables >500 MB to optimize extraction performance.", S_SMALL))

    doc.build(story)
    print(f'PDF saved: {OUTPUT_PDF}')

if __name__ == '__main__':
    build()
