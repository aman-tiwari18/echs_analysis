import os
import json
import datetime
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether)
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
S_XSMALL = bs(fontSize=7, textColor=DGRAY, leading=10)
S_LABEL = bs(fontName='Helvetica-Bold', fontSize=7, textColor=GOLD, leading=10, alignment=TA_CENTER)
S_BULL  = bs(alignment=TA_LEFT, leading=13, leftIndent=10)
S_WARN  = bs(fontName='Helvetica-Bold', fontSize=8, textColor=RED, leading=12)
S_DEF   = bs(fontSize=7.5, textColor=DGRAY, leading=11, alignment=TA_JUSTIFY, leftIndent=5, rightIndent=5)

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

# ── Cover Page (same as before) ──────────────────────────────────────────────
class CoverPage(Flowable):
    def __init__(self, total_tables=0, total_size_gb=0.0):
        super().__init__()
        self.width = W; self.height = H
        self.total_tables = total_tables
        self.total_size_gb = total_size_gb

    def draw(self):
        c = self.canv
        c.setFillColor(NAVY); c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(HexColor('#0d1929')); c.rect(0, H-22*mm, W, 22*mm, fill=1, stroke=0)
        c.setFillColor(white); c.setFont('Helvetica-Bold', 8)
        c.drawCentredString(W/2, H-10*mm, 'GOVERNMENT OF INDIA  |  EX-SERVICEMEN CONTRIBUTORY HEALTH SCHEME')
        c.setFont('Helvetica', 7.5); c.setFillColor(HexColor('#aabbcc'))
        c.drawCentredString(W/2, H-16*mm, 'Database Architecture & Metadata Audit')
        c.setFont('Helvetica-Bold', 40); c.setFillColor(GOLD)
        c.drawCentredString(W/2, H-45*mm, 'ECHS DATABASE DICTIONARY')
        c.setFont('Helvetica', 16); c.setFillColor(white)
        c.drawCentredString(W/2, H-57*mm, 'Comprehensive Table Metadata & Storage Analysis')
        c.setFont('Helvetica-Bold', 9); c.setFillColor(GOLD)
        c.drawCentredString(W/2, H-66*mm, 'SYSTEM REPORT  |  MAY 2026  |  CONFIDENTIAL')
        c.setStrokeColor(GOLD); c.setLineWidth(1)
        c.line(25*mm, H-71*mm, W-25*mm, H-71*mm)
        bx  = 18*mm; bw  = W - 36*mm; bh  = 32*mm; by  = H - 110*mm; col_w = bw / 4
        metrics = [
            ('DATABASE SCHEMA', 'ECHS'),
            ('TOTAL TABLES',    f'{self.total_tables}'),
            ('TOTAL SIZE',      f'{self.total_size_gb:.1f} GB'),
            ('EXTRACT DATE',    datetime.datetime.now().strftime('%d %b %Y')),
        ]
        c.setStrokeColor(GOLD); c.setLineWidth(1); c.rect(bx, by, bw, bh, fill=0, stroke=1)
        for i, (label, value) in enumerate(metrics):
            cx = bx + i * col_w
            c.setFillColor(HexColor('#0d1929')); c.rect(cx, by, col_w, bh, fill=1, stroke=0)
            if i > 0:
                c.setStrokeColor(GOLD); c.setLineWidth(0.5); c.line(cx, by, cx, by + bh)
            c.setFont('Helvetica-Bold', 7); c.setFillColor(GOLD)
            c.drawCentredString(cx + col_w/2, by + bh - 9*mm, label)
            c.setFont('Helvetica-Bold', 16); c.setFillColor(white)
            c.drawCentredString(cx + col_w/2, by + 8*mm, value)
        c.setStrokeColor(GOLD); c.setLineWidth(1); c.rect(bx, by, bw, bh, fill=0, stroke=1)
        c.setFont('Helvetica-Bold', 10); c.setFillColor(GOLD)
        c.drawCentredString(W/2, 28*mm, 'IIT KANPUR — Data Analytics & Fraud Intelligence Division')
        c.setFont('Helvetica', 8); c.setFillColor(white)
        c.drawCentredString(W/2, 21*mm, 'Report Date: May 2026  |  Ex-Servicemen Contributory Health Scheme (ECHS)')
        c.setFont('Helvetica', 7); c.setFillColor(HexColor('#556688'))
        c.drawCentredString(W/2, 12*mm, 'CONFIDENTIAL — For authorized personnel only. Not for public distribution.')

# ── Header / Footer ──────────────────────────────────────────────────────────
def inner_hf(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY); canvas.rect(0, H-12*mm, W, 12*mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD); canvas.rect(0, H-12.5*mm, W, 0.5*mm, fill=1, stroke=0)
    canvas.setFont('Helvetica-Bold', 9); canvas.setFillColor(GOLD)
    canvas.drawString(15*mm, H-8*mm, 'ECHS DATABASE DICTIONARY — SYSTEM REPORT')
    canvas.setFont('Helvetica', 7.5); canvas.setFillColor(HexColor('#aabbcc'))
    canvas.drawRightString(W-15*mm, H-8*mm, 'IIT Kanpur × ECHS Directorate  |  May 2026')
    canvas.setFillColor(NAVY); canvas.rect(0, 0, W, 10*mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD); canvas.rect(0, 10*mm, W, 0.5*mm, fill=1, stroke=0)
    canvas.setFont('Helvetica', 7); canvas.setFillColor(HexColor('#8899bb'))
    canvas.drawString(15*mm, 3.5*mm, 'RESTRICTED — Authorized Personnel Only')
    canvas.setFont('Helvetica-Bold', 8); canvas.setFillColor(GOLD)
    canvas.drawRightString(W-15*mm, 3.5*mm, f'Page {doc.page}')
    canvas.restoreState()

# ── Parse SQL Schema to extract table definitions ────────────────────────────
def parse_schema_for_definitions(schema_file):
    """Extract key columns and generate brief definitions for each table"""
    table_defs = {}
    
    with open(schema_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by CREATE TABLE statements
    table_pattern = r'CREATE TABLE `(\w+)`\s*\((.*?)\)\s*ENGINE'
    matches = re.findall(table_pattern, content, re.DOTALL | re.IGNORECASE)
    
    for table_name, columns_def in matches:
        # Extract primary key columns
        pk_match = re.search(r'PRIMARY KEY \(`([^`]+)`(?:,`([^`]+)`)*\)', columns_def)
        pk_cols = []
        if pk_match:
            pk_cols = [pk_match.group(1)]
            if pk_match.group(2):
                pk_cols.append(pk_match.group(2))
        
        # Extract first 3-5 significant columns (excluding IDs)
        col_lines = [line.strip() for line in columns_def.split('\n') if line.strip() and not line.strip().startswith('PRIMARY') and not line.strip().startswith('KEY') and not line.strip().startswith('UNIQUE') and not line.strip().startswith('CONSTRAINT')]
        
        key_columns = []
        for col_line in col_lines[:8]:  # Look at first 8 column definitions
            col_match = re.match(r'`(\w+)`', col_line)
            if col_match:
                col_name = col_match.group(1)
                # Skip pure ID columns unless they're in PK
                if '_ID' not in col_name or col_name in pk_cols:
                    key_columns.append(col_name)
                if len(key_columns) >= 4:
                    break
        
        # Generate definition based on table name and key columns
        definition = generate_table_definition(table_name, key_columns, pk_cols)
        table_defs[table_name] = definition
    
    return table_defs

def generate_table_definition(table_name, key_columns, pk_cols):
    """Generate a 2-line definition based on table name patterns and key columns"""
    
    name_lower = table_name.lower()
    
    # Pattern-based definitions
    if 'claim_intimation' == name_lower:
        return "Stores initial claim intimation details including patient, hospital, admission information, and referral data. Core table for tracking claim lifecycle from intimation to settlement."
    elif 'claim_submission' == name_lower:
        return "Contains detailed claim submission data with billing amounts, approval stages, and processing information. Links to intimation for complete claim history."
    elif 'claim_remarks' == name_lower:
        return "Tracks all remarks, comments, and annotations added by users during claim processing. Records stage-wise audit trail of claim reviews."
    elif 'hosp_exp_det' in name_lower:
        return "Hospital expense details capturing itemized billing breakup including room charges, procedures, pharmacy, and diagnostics. Critical for fraud detection."
    elif 'settlement_stat' in name_lower:
        return "Settlement statistics aggregating claim processing volumes and financial data by region, hospital, and time period. Primary table for analytics and reporting."
    elif 'office_master' == name_lower:
        return "Master registry of ECHS offices including hospitals, polyclinics, and regional centers. Contains entity types, locations, and empanelment status."
    elif 'audit' in name_lower and 'query' in name_lower:
        return "Audit queries raised during claim review process. Tracks questions, responses, and recovery amounts for quality control."
    elif 'audit' in name_lower and 'status' in name_lower:
        return "Maintains audit workflow status tracking claims through auditor, AAO, SAO, and CFA stages. Records query counts and recovery amounts."
    elif 'bpa' in name_lower and 'claim' in name_lower:
        return "BPA (Bill Passing Authority) claim allocation and processing queue. Manages workload distribution and priority-based claim assignment."
    elif 'bpa' in name_lower and 'allot' in name_lower:
        return "BPA daily allocation configuration defining targets, ranges, and user assignments. Controls automated claim distribution logic."
    elif 'pre_auth' in name_lower:
        return "Pre-authorization records for planned treatments. Captures estimated costs and approved amounts before admission."
    elif 'cda_payment' in name_lower:
        return "CDA payment file tracking and response management. Records payment status, UTR numbers, and rejection reasons from treasury."
    elif 'benf_master' in name_lower or 'beneficiary' in name_lower:
        return "Beneficiary master data including ESM details, dependents, card information, and entitlements. Core identity table linking service records."
    elif 'document' in name_lower and 'submit' in name_lower:
        return "Tracks all documents submitted with claims including medical records, bills, and supporting documents. Records upload status and file metadata."
    elif 'user_master' in name_lower:
        return "User accounts and authentication data for ECHS portal access. Defines roles, permissions, and office associations."
    elif 'audit_trail' in name_lower:
        return "Complete audit trail of user login sessions, IP addresses, and activity timestamps. Used for security monitoring and compliance."
    elif 'master' in name_lower:
        return f"Master data table for {table_name.replace('_master','').replace('_',' ')} codes and descriptions. Reference table used across the system."
    elif 'history' in name_lower or 'his_' in name_lower:
        return f"Historical snapshot of {table_name.replace('his_','').replace('_history','').replace('_',' ')} table. Archived data for audit and analysis purposes."
    elif 'status' in name_lower or 'stage' in name_lower:
        return f"Workflow status tracking for {table_name.replace('_status','').replace('_stage','').replace('_',' ')} process. Maintains state transitions and processing flags."
    elif 'type' in name_lower or 'category' in name_lower:
        return f"Classification codes for {table_name.replace('_type','').replace('_category','').replace('_',' ')}. Lookup table for standardized categorization."
    else:
        # Generic definition based on key columns
        if pk_cols:
            return f"Transaction/master table keyed by {', '.join(pk_cols[:2])}. Contains {len(key_columns)} key attributes supporting {table_name.replace('_',' ')} operations."
        else:
            return f"Supporting table for {table_name.replace('_',' ')} data management. Maintains related attributes and reference information."

# ── Document builder ─────────────────────────────────────────────────────────
def build():
    INPUT_JSON = '/home/aman/Desktop/echs_analysis/echs_db_metadata.json'
    SCHEMA_SQL = '/home/aman/Desktop/echs_analysis/ECHS_schema_full.sql'
    OUTPUT_PDF = '/home/aman/Desktop/echs_analysis/new_reports/ECHS_Database_Report.pdf'
    os.makedirs(os.path.dirname(OUTPUT_PDF), exist_ok=True)

    # Load metadata
    with open(INPUT_JSON, 'r') as f:
        data = json.load(f)

    # Parse schema for definitions
    print("Parsing schema for table definitions...")
    table_definitions = parse_schema_for_definitions(SCHEMA_SQL)
    print(f"Extracted definitions for {len(table_definitions)} tables")

    total_tables = len(data)
    total_size_mb = sum(t.get('data_mb', 0) for t in data)
    total_size_gb = total_size_mb / 1024

    doc = BaseDocTemplate(OUTPUT_PDF, pagesize=A4,
                          topMargin=16*mm, bottomMargin=14*mm,
                          leftMargin=15*mm, rightMargin=15*mm)
    frame = Frame(15*mm, 14*mm, W-30*mm, H-30*mm, id='main')
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
        "It outlines the structural metadata of every base table with detailed definitions, "
        "grouped into logical functional domains. This audit is critical for understanding data "
        "availability for fraud analytics and system integrations.", S_BODY))
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
        
        for t in g_tables:
            name = t['table']
            rows = int(t['row_count']) if t['row_count'] else 0
            size_mb = t.get('data_mb', 0.0)
            earliest = str(t['earliest_date'])[:10] if t['earliest_date'] else 'N/A'
            latest = str(t['latest_date'])[:10] if t['latest_date'] else 'N/A'
            
            # Get table definition
            table_def = table_definitions.get(name, f"Data table supporting {name.replace('_',' ')} operations and workflows.")
            
            # Build table block with definition
            elems = []
            
            # Table name row with highlighting
            if size_mb > 1000:
                name_text = f'<font color="#cc2222"><b>{name}</b></font>'
            else:
                name_text = f'<b>{name}</b>'
            
            row_str = f"{rows:,}" + ("*" if not t.get('row_count_exact', True) else "")
            
            # Create info table
            hdr = [[Paragraph(name_text, S_SMALL), 'Rows', 'Size (MB)', 'Earliest', 'Latest']]
            data_row = [[
                '',
                Paragraph(row_str, S_XSMALL),
                Paragraph(f"{size_mb:,.1f}", S_XSMALL),
                Paragraph(earliest, S_XSMALL),
                Paragraph(latest, S_XSMALL)
            ]]
            
            info_tbl = Table(hdr + data_row, colWidths=[65*mm, 22*mm, 20*mm, 22*mm, 22*mm])
            ts = TableStyle([
                ('BACKGROUND', (0,0), (0,0), LBLUE),
                ('BACKGROUND', (1,0), (-1,0), LGRAY),
                ('FONTNAME', (0,0), (0,0), 'Helvetica-Bold'),
                ('FONTNAME', (1,0), (-1,-1), 'Helvetica'),
                ('FONTSIZE', (0,0), (-1,-1), 7.5),
                ('TEXTCOLOR', (1,0), (-1,0), DGRAY),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('LEFTPADDING', (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
                ('GRID', (0,0), (-1,-1), 0.35, MGRAY),
                ('SPAN', (0,0), (0,1)),
            ])
            info_tbl.setStyle(ts)
            elems.append(info_tbl)
            
            # Add definition
            elems.append(Spacer(1, 2*mm))
            def_para = Paragraph(f'<i>{table_def}</i>', S_DEF)
            elems.append(def_para)
            elems.append(Spacer(1, 4*mm))
            
            # Keep table and definition together
            story.append(KeepTogether(elems))
        
        story.append(Spacer(1, 2*mm))
    
    story.append(Paragraph("* Approximate row counts used for tables >500 MB to optimize extraction performance.", S_SMALL))

    doc.build(story)
    print(f'PDF saved: {OUTPUT_PDF}')

if __name__ == '__main__':
    build()
