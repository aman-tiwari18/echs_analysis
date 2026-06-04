#!/usr/bin/env python3
"""
ECHS Module 13 - High-Value Claim Risk Scoring : PDF report generator.

Reuses the visual scaffold of the senior's generate_report_11.py (Navy/Gold
ReportLab theme, cover page, header/footer) and renders the processed datasets
from build_module13_data.py. The "Key fraud signals" are derived from the real
data, not hard-coded, so the report reflects whatever the last-5-year scan
actually surfaces.

Run order:  analyze_point13.py  ->  build_module13_data.py  ->  this script.
"""
import os
import json

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                 Spacer, Table, TableStyle, PageBreak, HRFlowable)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "module_13", "data")
OUT = os.path.join(HERE, "module_13", "reports", "ECHS_Module13_High_Value_Risk_Report.pdf")

W, H = A4
NAVY = HexColor('#1a2744'); GOLD = HexColor('#c8a84b'); RED = HexColor('#cc2222')
ORANGE = HexColor('#d46a00'); GREEN = HexColor('#1a6e1a'); LGRAY = HexColor('#f4f4f4')
MGRAY = HexColor('#dddddd'); DGRAY = HexColor('#444444')


def bs(**kw):
    d = dict(fontName='Helvetica', fontSize=10, leading=15, textColor=DGRAY, spaceAfter=6)
    d.update(kw); return ParagraphStyle('x', **d)


S_BODY = bs(alignment=TA_JUSTIFY, leading=13)
S_H1 = bs(fontName='Helvetica-Bold', fontSize=15, textColor=GOLD, leading=19, spaceBefore=12, spaceAfter=5)
S_H2 = bs(fontName='Helvetica-Bold', fontSize=11, textColor=NAVY, leading=15, spaceBefore=8, spaceAfter=3)
S_SMALL = bs(fontSize=7.5, textColor=DGRAY, leading=10)
S_WARN = bs(fontName='Helvetica-Bold', fontSize=8, textColor=RED, leading=12)


def crit(t): return f'<font color="#cc2222"><b>{t}</b></font>'
def high(t): return f'<font color="#d46a00"><b>{t}</b></font>'
def okc(t): return f'<font color="#1a6e1a"><b>{t}</b></font>'
def bold(t): return f'<b>{t}</b>'


def band_html(b):
    return {"CRITICAL": crit(b), "HIGH": high(b)}.get(b, b)


def tbl_style(hdr=1):
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, hdr - 1), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, hdr - 1), white),
        ('FONTNAME', (0, 0), (-1, hdr - 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.3),
        ('LEADING', (0, 0), (-1, -1), 9.5),
        ('ROWBACKGROUNDS', (0, hdr), (-1, -1), [white, LGRAY]),
        ('GRID', (0, 0), (-1, -1), 0.35, MGRAY),
        ('LINEBELOW', (0, 0), (-1, 0), 0.8, GOLD),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ])


# ---- formatting helpers ----------------------------------------------------
def inr(v):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return str(v)
    if v >= 1e7:
        return f'Rs {v/1e7:.2f} Cr'
    if v >= 1e5:
        return f'Rs {v/1e5:.2f} L'
    return f'Rs {v:,.0f}'


def P(t, style=S_SMALL):
    return Paragraph('' if t is None else str(t), style)


def esc(t):
    return str('' if t is None else t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def short(t, n=42):
    """Truncate AND html-escape free text (messy medical fields contain & < >)."""
    t = '' if t is None else str(t)
    if len(t) > n:
        t = t[:n - 1] + '...'
    return esc(t)


def load_csv(name):
    p = os.path.join(DATA, name)
    if os.path.exists(p) and os.path.getsize(p) > 0:
        return pd.read_csv(p, dtype=str, keep_default_na=False)
    return pd.DataFrame()


def load_summary():
    p = os.path.join(DATA, "module13_summary.json")
    return json.load(open(p)) if os.path.exists(p) else {}


# ---- cover + header/footer -------------------------------------------------
class CoverPage(Flowable):
    def __init__(self, summ): super().__init__(); self.width = W; self.height = H; self.s = summ
    def draw(self):
        c = self.canv
        c.setFillColor(NAVY); c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(GOLD); c.rect(0, H - 8 * mm, W, 8 * mm, fill=1, stroke=0)
        c.setFillColor(GOLD); c.rect(0, 0, W, 5 * mm, fill=1, stroke=0)
        for i, x in enumerate([0, W * 0.28, W * 0.56, W * 0.84]):
            c.setFillColor(GOLD if i % 2 == 0 else HexColor('#2a3d6a'))
            c.rect(x, H * 0.62, W * 0.25, H * 0.28, fill=1, stroke=0)
        c.setFillColor(NAVY); c.rect(18 * mm, H * 0.63 + 2, W - 36 * mm, H * 0.26 - 4, fill=1, stroke=0)
        c.setFillColor(white); c.setFont('Helvetica-Bold', 9)
        c.drawCentredString(W / 2, H * 0.86, 'GOVERNMENT OF INDIA  |  EX-SERVICEMEN CONTRIBUTORY HEALTH SCHEME')
        c.setFont('Helvetica', 8); c.setFillColor(HexColor('#aabbcc'))
        c.drawCentredString(W / 2, H * 0.83, 'Fraud Analytics & Intelligence Report')
        c.setFont('Helvetica-Bold', 28); c.setFillColor(GOLD)
        c.drawCentredString(W / 2, H * 0.76, 'ECHS FRAUD ANALYTICS')
        c.setFont('Helvetica-Bold', 16); c.setFillColor(white)
        c.drawCentredString(W / 2, H * 0.705, 'MODULE 13: HIGH-VALUE CLAIM RISK SCORING')
        c.setFont('Helvetica', 10); c.setFillColor(HexColor('#aabbcc'))
        c.drawCentredString(W / 2, H * 0.66, 'Claims above Rs 5 Lakh  |  Rule-Based Signals + Composite Risk Score')
        c.setFillColor(GOLD); c.rect(60 * mm, H * 0.61, W - 120 * mm, 0.6 * mm, fill=1, stroke=0)
        c.setFont('Helvetica-Bold', 10); c.setFillColor(GOLD)
        c.drawCentredString(W / 2, H * 0.575, 'IIT KANPUR  x  ECHS DIRECTORATE')
        cl = self.s.get('total_hv_claims', 0)
        amt = self.s.get('total_exposure_cr', 0)
        meta = [
            ('Database Scope', f"{cl:,} high-value claims  |  Rs {amt:,.0f} Cr total exposure"),
            ('Coverage', 'Last 5 years  |  claim_intimation + claim_submission'),
            ('Methodology', 'Rule-based signals + transparent composite risk score'),
            ('Classification', 'RESTRICTED - OFFICIAL USE ONLY'),
        ]
        bx, by, bw, bh = 30 * mm, H * 0.30, W - 60 * mm, 17 * mm
        for i, (lbl, val) in enumerate(meta):
            y = by + (len(meta) - 1 - i) * (bh + 2 * mm)
            c.setFillColor(HexColor('#0d1929')); c.rect(bx, y, bw, bh, fill=1, stroke=0)
            c.setStrokeColor(GOLD); c.setLineWidth(0.5); c.rect(bx, y, bw, bh, fill=0, stroke=1)
            c.setFont('Helvetica-Bold', 7); c.setFillColor(GOLD)
            c.drawString(bx + 5 * mm, y + bh - 5 * mm, lbl.upper())
            c.setFont('Helvetica', 9); c.setFillColor(white)
            c.drawString(bx + 5 * mm, y + 3 * mm, val)
        c.setFont('Helvetica', 7); c.setFillColor(HexColor('#556688'))
        c.drawCentredString(W / 2, 10 * mm, 'CONFIDENTIAL - For authorized personnel only. Not for public distribution.')


def inner_hf(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY); canvas.rect(0, H - 12 * mm, W, 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD); canvas.rect(0, H - 12.5 * mm, W, 0.5 * mm, fill=1, stroke=0)
    canvas.setFont('Helvetica-Bold', 9); canvas.setFillColor(GOLD)
    canvas.drawString(15 * mm, H - 8 * mm, 'ECHS FRAUD ANALYTICS - MODULE 13: HIGH-VALUE CLAIM RISK SCORING')
    canvas.setFont('Helvetica', 7.5); canvas.setFillColor(HexColor('#aabbcc'))
    canvas.drawRightString(W - 15 * mm, H - 8 * mm, 'IIT Kanpur x ECHS Directorate')
    canvas.setFillColor(NAVY); canvas.rect(0, 0, W, 10 * mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD); canvas.rect(0, 10 * mm, W, 0.5 * mm, fill=1, stroke=0)
    canvas.setFont('Helvetica', 7); canvas.setFillColor(HexColor('#8899bb'))
    canvas.drawString(15 * mm, 3.5 * mm, 'RESTRICTED - Authorized Personnel Only')
    canvas.setFont('Helvetica-Bold', 8); canvas.setFillColor(GOLD)
    canvas.drawRightString(W - 15 * mm, 3.5 * mm, f'Page {doc.page}')
    canvas.restoreState()


# ---- sections --------------------------------------------------------------
def h1(story, t):
    story.append(Paragraph(t, S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))


def exec_summary(story, s, q13b, q13d, bulk):
    h1(story, 'EXECUTIVE SUMMARY')
    story.append(Paragraph(
        "Module 13 targets the highest-financial-risk stratum of the ECHS claim ecosystem: individual "
        "claims exceeding <b>Rs 5 lakh</b> per admission, analysed across the <b>last five years</b>. Each "
        "claim, hospital login and beneficiary card is scored with a transparent, rule-based composite "
        "risk score (0-100); no black-box model is used, so every score is auditable. <b>Total Financial "
        "Exposure</b> is the gross claimed value of the flagged claims - an approximate figure; the actual "
        "recoverable amount is determined after audit.", S_BODY))
    story.append(Paragraph("NOTE: Every flagged case is an investigative lead, not a confirmed finding. "
                           "A qualified auditor must review each case before any action is taken.", S_WARN))
    rows = [
        ['Key Metric', 'Value'],
        ['High-value claims (> Rs 5 L)', f"{s.get('total_hv_claims',0):,}"],
        ['Total financial exposure (high-value)', f"Rs {s.get('total_exposure_cr',0):,.2f} Cr"],
        ['Total deducted (high-value)', f"Rs {s.get('total_deducted_cr',0):,.2f} Cr  ({s.get('overall_ded_pct',0)}%)"],
        ['Claims approved at Rs 0 (100% deducted)', f"{s.get('full_deduction_hv_claims',0):,}"],
        ['HV claims with NULL / anomalous hospital ID', f"{s.get('n_anomalous_hv_claims',0):,}  (Rs {s.get('anomalous_exposure_cr',0):,.0f} Cr exposure)"],
        ['Highest single claim', f"Rs {s.get('top_single_claim_cr',0):,.2f} Cr"],
        ['Hospital logins flagged (avg ded > 25%)', f"{s.get('n_flagged_hospitals',0):,}"],
        ['Chronic repeat claimants (>= 3 HV claims)', f"{s.get('n_chronic_claimants',0):,}"],
        ['Same-day duplicate claim groups', f"{s.get('n_duplicate_groups',0):,}"],
        ['Bulk claim-injection events', f"{s.get('n_bulk_events',0):,}  (system-compromise tier: {s.get('n_bulk_system_compromise',0)})"],
    ]
    t = Table(rows, colWidths=[95 * mm, 75 * mm]); t.setStyle(tbl_style()); story.append(t)
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph('Four systemic patterns concentrate the risk:', S_H2))
    pats = []
    if len(q13b):
        top = q13b.iloc[0]
        pats.append(f"<b>Hospital-level systematic overcharging</b> - login <b>{top['hospital_code']}</b> "
                    f"accounts for Rs {float(top['deducted_cr']):,.2f} Cr of deductions across {top['hv_claims']} high-value claims.")
    pats.append(f"<b>100% deduction claims</b> - {s.get('full_deduction_hv_claims',0):,} high-value claims were "
                f"approved at Rs 0, i.e. billed far beyond the ECHS package ceiling.")
    if len(q13d):
        top = q13d.iloc[0]
        pats.append(f"<b>Chronic repeat claimants</b> - e.g. {short(top['beneficiary'],28)} (card {top['card_id']}) "
                    f"with {top['hv_claims']} high-value claims, Rs {float(top['exposure_cr']):,.2f} Cr exposure.")
    if len(bulk):
        top = bulk.iloc[0]
        pats.append(f"<b>Bulk claim injection</b> - {short(top['beneficiary'],26)} shows {top['intimation_count']} "
                    f"intimation IDs created in a single day at {top['hospital_code']} (system-level event).")
    for p in pats:
        story.append(Paragraph('• ' + p, bs(leading=13, leftIndent=10)))
    story.append(PageBreak())


def signals_section(story, s, q13a, q13b, q13d, dups, bulk):
    h1(story, 'KEY FRAUD SIGNALS')
    story.append(Paragraph("Derived directly from the last-5-year scan. Risk band reflects the composite score.", S_BODY))
    data = [['#', 'Signal', 'Finding', 'Risk']]
    i = 1

    def add(name, finding, bandlab):
        nonlocal i
        data.append([str(i), P(name), P(finding), P(band_html(bandlab))]); i += 1

    if len(q13a):
        r = q13a.iloc[0]
        add('Largest single high-value claim',
            f"{inr(r['exposure'])} at {r['hospital_code']} ({short(r['beneficiary'],26)}); {r['ded_pct']}% deducted.",
            r['risk_band'])
    if len(q13b):
        bydev = q13b.assign(_rate=pd.to_numeric(q13b['avg_ded_pct'], errors='coerce')) \
                    .sort_values('_rate', ascending=False).iloc[0]
        rate = float(bydev['_rate'])
        rate_band = 'CRITICAL' if rate >= 70 else ('HIGH' if rate >= 50 else 'MEDIUM')
        add('Highest hospital deduction rate',
            f"{bydev['hospital_code']}: {bydev['avg_ded_pct']}% avg deduction on {bydev['hv_claims']} high-value claims.",
            rate_band)
        r = q13b.iloc[0]
        add('Largest absolute hospital deduction',
            f"{r['hospital_code']}: Rs {float(r['deducted_cr']):,.2f} Cr deducted across {r['hv_claims']} claims.",
            r['risk_band'])
    add('100% deduction claims',
        f"{s.get('full_deduction_hv_claims',0):,} high-value claims approved at Rs 0 - billing beyond package ceiling.",
        'HIGH')
    if len(dups):
        r = dups.iloc[0]
        add('Same-day duplicate billing',
            f"{short(r['beneficiary'],24)} (card {r['card_id']}): {r['dup_count']} identical {inr(r['exposure'])} claims on {str(r['admission_date'])[:10]}.",
            'CRITICAL')
    if len(q13d):
        r = q13d.iloc[0]
        add('Chronic repeat claimant',
            f"{short(r['beneficiary'],24)} (card {r['card_id']}): {r['hv_claims']} HV claims, Rs {float(r['exposure_cr']):,.2f} Cr exposure, "
            f"{int(float(r['lockin'])*100)}% at {r['primary_hospital']}.",
            r['risk_band'])
    if len(bulk):
        r = bulk.iloc[0]
        add('Extreme bulk claim injection',
            f"{short(r['beneficiary'],22)}: {r['intimation_count']} intimation IDs in one day at {r['hospital_code']} ({r['tier']}).",
            'CRITICAL')
    if s.get('n_anomalous_hv_claims', 0):
        add('Anomalous / missing hospital identifiers',
            f"{s.get('n_anomalous_hv_claims',0):,} high-value claims (Rs {s.get('anomalous_exposure_cr',0):,.0f} Cr) carry "
            f"NULL or numeric (phone-like) hospital IDs - probable ghost admissions.",
            'HIGH')
    t = Table(data, colWidths=[8 * mm, 42 * mm, 102 * mm, 18 * mm]); t.setStyle(tbl_style()); story.append(t)
    story.append(PageBreak())


def q13a_section(story, q13a, dups):
    h1(story, 'Q13a - Top High-Value Individual Claims (> Rs 5 Lakh)')
    story.append(Paragraph("Ranked by gross claimed amount. <b>Ded%</b> = (claimed - approved) / claimed. "
                           "A 100% deduction means the approval stage recorded zero approved - a signal of "
                           "billing far beyond the ECHS package rate.", S_BODY))
    head = [['Score', 'Beneficiary', 'Hospital', 'Admission', 'Diagnosis', 'Exposure', 'Ded%']]
    for _, r in q13a.head(25).iterrows():
        sc = band_html(r['risk_band']) + f" {r['risk_score']}"
        head.append([P(sc), P(short(r['beneficiary'], 22)), P(short(r['hospital_code'], 12)),
                     P(str(r['admission_date'])[:10]), P(short(r['diagnosis'], 22)),
                     P(inr(r['exposure'])), P(crit(r['ded_pct']) if float(r['ded_pct']) >= 99 else r['ded_pct'])])
    t = Table(head, colWidths=[20 * mm, 33 * mm, 22 * mm, 20 * mm, 35 * mm, 24 * mm, 16 * mm])
    t.setStyle(tbl_style()); story.append(t); story.append(Spacer(1, 5 * mm))

    story.append(Paragraph('Repeat & Duplicate High-Value Claims', S_H2))
    story.append(Paragraph("Same card + same admission date + same amount, submitted under multiple "
                           "intimation IDs - textbook duplicate billing.", S_BODY))
    if len(dups):
        d = [['Beneficiary', 'Card', 'Hospital', 'Admission', 'Exposure', 'Dups']]
        for _, r in dups.head(12).iterrows():
            d.append([P(short(r['beneficiary'], 24)), P(short(r['card_id'], 16)), P(short(r['hospital_code'], 12)),
                      P(str(r['admission_date'])[:10]), P(inr(r['exposure'])), P(crit(r['dup_count']))])
        t = Table(d, colWidths=[37 * mm, 30 * mm, 24 * mm, 22 * mm, 30 * mm, 14 * mm])
        t.setStyle(tbl_style()); story.append(t)
    else:
        story.append(Paragraph('No same-day duplicate high-value groups detected.', S_BODY))
    story.append(PageBreak())


def q13b_section(story, q13b):
    h1(story, 'Q13b - Hospital Risk Scorecard (Avg Deduction > 25%)')
    story.append(Paragraph("Hospital logins with at least 10 high-value claims and an average deduction "
                           "above 25%, ranked by absolute deduction. High deduction rates indicate "
                           "systematic billing above admissible ECHS rates.", S_BODY))
    if not len(q13b):
        story.append(Paragraph('No hospital logins crossed the threshold.', S_BODY)); story.append(PageBreak()); return
    head = [['Score', 'Hospital Login', 'HV Claims', 'Exposure', 'Deducted', 'Avg Ded%', '100% Ded']]
    for _, r in q13b.head(20).iterrows():
        sc = band_html(r['risk_band']) + f" {r['risk_score']}"
        head.append([P(sc), P(short(r['hospital_code'], 16)), P(r['hv_claims']),
                     P(f"Rs {float(r['exposure_cr']):,.2f} Cr"), P(f"Rs {float(r['deducted_cr']):,.2f} Cr"),
                     P(crit(r['avg_ded_pct']) if float(r['avg_ded_pct']) >= 50 else r['avg_ded_pct']),
                     P(r['full_ded_claims'])])
    t = Table(head, colWidths=[22 * mm, 30 * mm, 18 * mm, 28 * mm, 28 * mm, 20 * mm, 18 * mm])
    t.setStyle(tbl_style()); story.append(t); story.append(PageBreak())


def q13c_section(story, reg):
    h1(story, 'Q13c - Regional Risk Distribution')
    story.append(Paragraph("Region-level claimed value and deduction rate (from the pre-aggregated "
                           "settlement statistics). A region-level proxy: high deduction rates flag "
                           "commands where claim scrutiny is removing a large share of billed value.", S_BODY))
    if not len(reg):
        story.append(Paragraph('Regional data unavailable.', S_BODY)); story.append(PageBreak()); return
    reg = reg.copy()
    reg['exposure_cr_f'] = pd.to_numeric(reg['exposure_cr'], errors='coerce').fillna(0)
    reg = reg.sort_values('exposure_cr_f', ascending=False)
    head = [['Region', 'ECHS Command', 'Claims', 'Exposure', 'Deducted', 'Ded%']]
    for _, r in reg.head(16).iterrows():
        dp = float(r['ded_pct']) if str(r['ded_pct']) not in ('', 'nan') else 0
        head.append([P(r['region_id']), P(short(r['command'], 24)), P(f"{int(float(r['claim_cnt'])):,}"),
                     P(f"Rs {float(r['exposure_cr']):,.0f} Cr"), P(f"Rs {float(r['deducted_cr']):,.0f} Cr"),
                     P(high(r['ded_pct']) if dp >= 15 else r['ded_pct'])])
    t = Table(head, colWidths=[16 * mm, 44 * mm, 28 * mm, 30 * mm, 30 * mm, 16 * mm])
    t.setStyle(tbl_style()); story.append(t); story.append(PageBreak())


def q13d_section(story, q13d):
    h1(story, 'Q13d - Chronic Repeat High-Value Claimants (>= 3 Claims)')
    story.append(Paragraph("Beneficiary cards with three or more high-value claims, ranked by total "
                           "claimed. <b>Lock-in</b> = share of claims at a single hospital; a high lock-in "
                           "with many claims is the strongest repeat-claimant signal.", S_BODY))
    if not len(q13d):
        story.append(Paragraph('No cards crossed the threshold.', S_BODY)); story.append(PageBreak()); return
    head = [['Score', 'Beneficiary', 'Card', 'Claims', 'Exposure', 'Deducted', 'Primary Hosp', 'Lock-in', 'Span']]
    for _, r in q13d.head(16).iterrows():
        sc = band_html(r['risk_band']) + f" {r['risk_score']}"
        span = f"{str(r['first_admit'])[2:7]}..{str(r['last_admit'])[2:7]}"
        head.append([P(sc), P(short(r['beneficiary'], 18)), P(short(r['card_id'], 14)), P(r['hv_claims']),
                     P(f"Rs {float(r['exposure_cr']):,.2f} Cr"), P(f"Rs {float(r['deducted_cr']):,.2f} Cr"),
                     P(short(r['primary_hospital'], 12)), P(f"{int(float(r['lockin'])*100)}%"), P(span)])
    t = Table(head, colWidths=[18 * mm, 24 * mm, 24 * mm, 12 * mm, 22 * mm, 22 * mm, 16 * mm, 12 * mm, 20 * mm])
    t.setStyle(tbl_style()); story.append(t); story.append(PageBreak())


def q13f_section(story, bulk):
    h1(story, 'Q13f - Extreme Bulk Claim Injection (Same-Day Mass Intimation)')
    story.append(Paragraph("Hundreds of claim-intimation records created for a single card, on a single "
                           "day, at a single hospital login - far beyond manual entry. Tiers: "
                           "<b>&gt;300</b> = system compromise, <b>100-300</b> = account abuse, "
                           "<b>50-100</b> = watch. Near-consecutive intimation IDs confirm programmatic "
                           "batch insertion.", S_BODY))
    if not len(bulk):
        story.append(Paragraph('No bulk-injection events at/above the threshold.', S_BODY)); story.append(PageBreak()); return
    head = [['Beneficiary', 'Card', 'Hospital', 'Date', 'Intimations', 'ID Range', 'Tier']]
    for _, r in bulk.head(14).iterrows():
        tlab = crit(r['tier']) if r['tier'] == 'SYSTEM COMPROMISE' else (high(r['tier']) if r['tier'] == 'ACCOUNT ABUSE' else r['tier'])
        head.append([P(short(r['beneficiary'], 20)), P(short(r['card_id'], 14)), P(short(r['hospital_code'], 12)),
                     P(str(r['creation_date'])[:10]), P(crit(r['intimation_count'])),
                     P(f"{r['first_intimation_id']}-{r['last_intimation_id']}"), P(tlab)])
    t = Table(head, colWidths=[30 * mm, 26 * mm, 22 * mm, 20 * mm, 20 * mm, 30 * mm, 22 * mm])
    t.setStyle(tbl_style()); story.append(t); story.append(PageBreak())


def scoring_section(story, s):
    h1(story, 'Composite Risk Score - Methodology')
    story.append(Paragraph("Each claim, hospital login and beneficiary card receives a transparent "
                           "weighted score from 0-100. The score is a plain weighted sum of normalised "
                           "signals - fully explainable, no machine-learning black box. Bands: "
                           f"{crit('CRITICAL')} &gt;= 70, {high('HIGH')} 45-69, MEDIUM &lt; 45.", S_BODY))
    w = s.get('weights', {})
    for title, key in [('Claim-level score', 'claim'), ('Hospital-level score', 'hospital'), ('Claimant-level score', 'claimant')]:
        ww = w.get(key, {})
        if not ww:
            continue
        story.append(Paragraph(title, S_H2))
        rows = [['Component', 'Weight']] + [[k.replace('_', ' ').title(), str(v)] for k, v in ww.items()]
        t = Table(rows, colWidths=[120 * mm, 50 * mm]); t.setStyle(tbl_style()); story.append(t)
        story.append(Spacer(1, 3 * mm))
    story.append(PageBreak())


def recommendations(story):
    h1(story, 'Strategic Recommendations')
    recs = [
        ('CRITICAL', 'Freeze & audit top-scored hospital logins', 'Suspend new high-value claim processing on logins with >50% average deduction pending physical audit.'),
        ('CRITICAL', 'Investigate bulk-injection events as credential compromise', 'Treat any login with >300 same-day intimations as a security incident; rotate credentials and trace the source IP/session.'),
        ('CRITICAL', 'Recover on same-day duplicate claims', 'Reclaim paid amounts where the same card+date+amount was submitted under multiple intimation IDs.'),
        ('HIGH', 'Cap & pre-authorise claims above Rs 5 lakh', 'Mandatory pre-authorisation and senior medical review for every claim exceeding Rs 5 lakh.'),
        ('HIGH', 'Profile chronic repeat claimants', 'Manually review cards with >= 3 high-value claims and high single-hospital lock-in.'),
        ('HIGH', 'Validate hospital identifiers', 'Reject claims carrying NULL or numeric (phone-like) hospital IDs at intake.'),
        ('MEDIUM', 'Operationalise the risk score', 'Run the composite score nightly and route CRITICAL-band claims to auditors before settlement.'),
    ]
    data = [['Priority', 'Recommendation', 'Action']]
    for pr, t1, t2 in recs:
        data.append([P(band_html(pr)), P(bold(t1)), P(t2)])
    t = Table(data, colWidths=[20 * mm, 55 * mm, 95 * mm]); t.setStyle(tbl_style()); story.append(t)
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("This report is produced by an automated screening system. Every flagged case "
                           "is an investigative lead, not a confirmed finding, and must be reviewed by a "
                           "qualified auditor before any action is taken.", S_WARN))


def build():
    s = load_summary()
    q13a = load_csv('q13a_top_claims.csv')
    dups = load_csv('q13a2_duplicates.csv')
    q13b = load_csv('q13b_hospital_scorecard.csv')
    reg = load_csv('q13c_regional.csv')
    q13d = load_csv('q13d_chronic_claimants.csv')
    bulk = load_csv('q13f_bulk_injection.csv')

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc = BaseDocTemplate(OUT, pagesize=A4, topMargin=25 * mm, bottomMargin=25 * mm,
                          leftMargin=20 * mm, rightMargin=20 * mm)
    frame = Frame(20 * mm, 18 * mm, W - 40 * mm, H - 42 * mm, id='main')
    inner = PageTemplate(id='inner', frames=[frame], onPage=inner_hf)
    cover_frame = Frame(0, 0, W, H, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='cover')
    cover = PageTemplate(id='cover', frames=[cover_frame])
    doc.addPageTemplates([cover, inner])

    story = [CoverPage(s), PageBreak()]
    exec_summary(story, s, q13b, q13d, bulk)
    signals_section(story, s, q13a, q13b, q13d, dups, bulk)
    q13a_section(story, q13a, dups)
    q13b_section(story, q13b)
    q13c_section(story, reg)
    q13d_section(story, q13d)
    q13f_section(story, bulk)
    scoring_section(story, s)
    recommendations(story)
    doc.build(story)
    print(f'PDF saved: {OUT}')


if __name__ == '__main__':
    build()
