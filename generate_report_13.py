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


def load_json(name):
    p = os.path.join(DATA, name)
    return json.load(open(p)) if os.path.exists(p) else {}


def fact_style():
    return TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 8), ('LEADING', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), NAVY), ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#eef0f5')),
        ('GRID', (0, 0), (-1, -1), 0.3, MGRAY), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ])


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


def bullet(story, t):
    story.append(Paragraph('•  ' + t, bs(leading=13, leftIndent=10, spaceAfter=4)))


def methodology(story, s):
    h1(story, 'Methodology & Data Sources')
    story.append(Paragraph(
        "<b>Data.</b> High-value claims (gross claimed &gt; Rs 5 lakh) over the <b>last five years</b>, taken "
        "from the ECHS claim_intimation and claim_submission tables and joined on the intimation ID. Regional "
        "figures use the pre-aggregated settlement_stat table.", S_BODY))
    story.append(Paragraph(
        "<b>Claim pipeline.</b> A claim moves through intimation (admission notified) -&gt; submission "
        "(hospital bills the gross amount) -&gt; UTI audit (an approved amount is set; the balance is the "
        "deduction) -&gt; settlement. <b>Deduction %</b> = (gross claimed - approved) / gross claimed; "
        "a 100% deduction means the audit approved nothing on a multi-lakh bill - a strong signal of billing "
        "beyond the ECHS package ceiling.", S_BODY))
    story.append(Paragraph(
        "<b>Risk score.</b> Every claim, hospital login and beneficiary card receives a transparent 0-100 "
        "weighted score - no machine learning, so every point is reconstructable from the source rows. "
        f"Bands: {crit('CRITICAL')} &gt;= 70, {high('HIGH')} 45-69, MEDIUM &lt; 45. The exact component "
        "weights are listed in the Composite Risk Score section.", S_BODY))
    story.append(Paragraph('Key definitions', S_H2))
    defs = [
        ['Term', 'Definition'],
        ['High-value claim', 'Gross claimed amount > Rs 5,00,000 for one admission'],
        ['Deduction %', '(gross claimed - UTI approved) / gross claimed x 100'],
        ['Chronic repeat claimant', 'One beneficiary card with >= 3 high-value claims'],
        ['Single-hospital lock-in', "Share of a card's high-value claims at one hospital login"],
        ['Bulk injection (tiers)', '>300 same-day intimations = system compromise; 100-300 = account abuse; 50-100 = watch'],
        ['Anomalous hospital ID', 'NULL, -1/0 placeholder, or a numeric/phone-like value (not a real login)'],
        ['Total Financial Exposure', 'Sum of gross claimed on flagged claims (approximate; recovery set at audit)'],
    ]
    t = Table([[P(a, bs(fontName='Helvetica-Bold', fontSize=8, textColor=white)) if i == 0 else P(a),
                P(b, bs(fontName='Helvetica-Bold', fontSize=8, textColor=white)) if i == 0 else P(b)]
               for i, (a, b) in enumerate(defs)], colWidths=[46 * mm, 124 * mm])
    t.setStyle(tbl_style()); story.append(t)
    story.append(PageBreak())


def limitations(story):
    h1(story, 'Limitations & Assumptions')
    bullet(story, "<b>Red flags, not verdicts.</b> Every item is an automated investigative lead, not a confirmed "
                  "finding. A qualified auditor must verify each case before any action.")
    bullet(story, "<b>Deduction is not fraud.</b> A high deduction can reflect a legitimate package ceiling, a "
                  "coding error, or incomplete documentation - it flags where billed value was removed, not why.")
    bullet(story, "<b>Login codes are identifiers.</b> Hospital login codes (e.g. parkhosg, pol.3325) are used as "
                  "identifiers only; this report does not assert their real-world hospital identity.")
    bullet(story, "<b>Data quality.</b> Findings depend on the accuracy of the intimation/submission tables and the "
                  "UTI deduction codes; systemic gaps (e.g. missing hospital IDs) can both create and hide signals.")
    bullet(story, "<b>Scope.</b> Analysis covers the last five years only; older claims are out of scope by design.")
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph("ALL CASES REQUIRE VERIFICATION BY QUALIFIED AUDITORS BEFORE ANY ACTION IS TAKEN.", S_WARN))
    story.append(PageBreak())


def _case_block(story, title, rows, paras):
    story.append(Paragraph(title, S_H2))
    body = [[k, P(v)] for k, v in rows]
    t = Table(body, colWidths=[30 * mm, 140 * mm]); t.setStyle(fact_style()); story.append(t)
    story.append(Spacer(1, 1.5 * mm))
    for p in paras:
        story.append(Paragraph(p, S_BODY))
    story.append(Spacer(1, 4 * mm))


def case_studies(story, cases):
    if not cases:
        return
    h1(story, 'Case Studies')
    story.append(Paragraph("Representative cases drawn directly from the flagged data. Names and card numbers are "
                           "shown as recorded; each is a lead for verification, not a verdict.", S_BODY))

    c = cases.get('top_repeat_claimant')
    if c:
        rows = [
            ['Beneficiary', f"{esc(c['beneficiary'])} (card {esc(c['card_id'])})"],
            ['Pattern', f"{c['claims']} high-value claims; {c['lockin_pct']}% at one login ({esc(c['primary_hospital'])})"],
            ['Exposure', f"Rs {c['exposure_cr']:.2f} Cr claimed / Rs {c['approved_cr']:.2f} Cr approved ({c['ded_pct']}% deducted)"],
            ['Window', f"{c['first_admit']} to {c['last_admit']} (~{c['span_months']:.0f} months; on average one admission every {c['avg_interval_days']:.0f} days)"],
        ]
        para = (f"{esc(c['beneficiary'])} filed <b>{c['claims']} separate high-value claims</b> in about "
                f"{c['span_months']:.0f} months - on average one admission every <b>{c['avg_interval_days']:.0f} days</b> - "
                f"with {c['lockin_pct']}% at a single login. The low {c['ded_pct']}% deduction means most claims pass "
                f"audit, so the test is documentary: either a genuine chronic condition needing case management, or "
                f"manufactured admission episodes generating a fresh base fee each time.")
        action = "<b>Action:</b> pull discharge summaries for a 20-claim sample and reconcile admission dates / ICU notes with the billed episodes (14 days)."
        _case_block(story, 'Case 1 - Chronic Repeat Claimant', rows, [para, action])

    g = cases.get('ghost_repeat_claimant')
    if g:
        rows = [
            ['Beneficiary', f"{esc(g['beneficiary'])} (card {esc(g['card_id'])})"],
            ['Pattern', f"{g['claims']} high-value claims, primary hospital ID = {esc(g['primary_hospital'])} (untraceable)"],
            ['Exposure', f"Rs {g['exposure_cr']:.2f} Cr claimed ({g['ded_pct']}% deducted)"],
        ]
        para = (f"Every one of {esc(g['beneficiary'])}'s {g['claims']} high-value claims (Rs {g['exposure_cr']:.2f} Cr) "
                f"carries no traceable hospital ID. High-value admissions with no identifiable provider are a classic "
                f"<b>ghost-admission</b> pattern; the partial deduction shows the system flags but does not fully "
                f"reject them.")
        action = "<b>Action:</b> trace the actual servicing facility from settlement/bank records; if none exists, treat as fabricated claims (30 days)."
        _case_block(story, 'Case 2 - Ghost-Hospital Repeat Claimant', rows, [para, action])

    d = cases.get('top_duplicate')
    if d:
        ids = ", ".join(str(x) for x in d.get('intimation_ids', []))
        rows = [
            ['Beneficiary', f"{esc(d['beneficiary'])} (card {esc(d['card_id'])})"],
            ['Duplicate', f"{d['dup_count']} identical {inr(d['exposure'])} claims on {d['admission_date']} at {esc(d['hospital'])}"],
            ['Intimation IDs', f"{ids}" + ("  (near-consecutive)" if d.get('consecutive') else "")],
        ]
        para = (f"The same card, same admission date and same amount ({inr(d['exposure'])}) were submitted under "
                f"{d['dup_count']} different intimation IDs - the textbook signature of duplicate billing to collect "
                f"reimbursement more than once.")
        action = "<b>Action:</b> confirm whether more than one submission was paid and recover the surplus; sweep this login for other same-day duplicates (7 days)."
        _case_block(story, 'Case 3 - Same-Day Duplicate Billing', rows, [para, action])

    cv = cases.get('card_variation')
    if cv:
        rows = [
            ['Beneficiary', f"{esc(cv['beneficiary'])}"],
            ['Two cards', f"{esc(cv['card_a'])}  vs  {esc(cv['card_b'])} (differ by one character)"],
            ['Combined', f"{cv['claims']} high-value claims, Rs {cv['exposure_cr']:.2f} Cr, at {', '.join(esc(h) for h in cv['hospitals'])}"],
        ]
        para = (f"The same beneficiary name appears on two card numbers that differ by a single character "
                f"(<b>{esc(cv['card_a'])}</b> vs <b>{esc(cv['card_b'])}</b>). This can indicate duplicate card "
                f"issuance / card-ID manipulation used to split a fraud trail across two IDs - or, less likely, two "
                f"distinct people sharing a common name. It is a lead, not a conclusion.")
        action = "<b>Action:</b> verify both cards against the service record - one pensioner or two? (immediate)."
        _case_block(story, 'Case 4 - Possible Card-ID Manipulation', rows, [para, action])

    b = cases.get('top_bulk')
    if b:
        rows = [
            ['Beneficiary', f"{esc(b['beneficiary'])}"],
            ['Event', f"{b['count']} intimation IDs in ONE day ({b['date']}) at {esc(b['hospital'])}"],
            ['ID range', f"{b['first_id']} - {b['last_id']}" + ("  (near-consecutive)" if b.get('consecutive') else "")],
            ['Tier', b['tier']],
        ]
        para = (f"<b>{b['count']} claim-intimation records created for one card on a single day</b> is far beyond "
                f"manual web-portal entry. The near-consecutive ID range is the signature of programmatic batch "
                f"insertion - i.e. portal credential compromise or insider database access, not ordinary claim fraud.")
        action = "<b>Action:</b> obtain portal access logs (IP/session/timestamps) for that date, suspend the login, and escalate to ECHS IT / CERT-In (immediate)."
        _case_block(story, 'Case 5 - Extreme Bulk Claim Injection', rows, [para, action])
    story.append(PageBreak())


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
    story.append(Spacer(1, 3 * mm))
    cbd = s.get('claimants_band_dist', {})
    hbd = s.get('hospitals_band_dist', {})
    story.append(Paragraph(
        f"By composite risk band: {cbd.get('CRITICAL',0)+cbd.get('HIGH',0):,} beneficiary cards and "
        f"{hbd.get('CRITICAL',0)+hbd.get('HIGH',0):,} hospital logins fall in the CRITICAL/HIGH tiers and head the "
        f"verification queue. Flagged claims span {s.get('earliest_admit','')} to {s.get('latest_admit','')}.", S_BODY))
    story.append(Spacer(1, 2 * mm))
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


def q13a_section(story, q13a, dups, ghosts):
    h1(story, 'Q13a - Top High-Value Individual Claims (> Rs 5 Lakh)')
    story.append(Paragraph("Ranked by gross claimed amount (= exposure). <b>Ded%</b> = (claimed - approved) / "
                           "claimed. A 100% deduction means the approval stage recorded zero approved - a signal "
                           "of billing far beyond the ECHS package rate.", S_BODY))
    head = [['Score', 'Beneficiary', 'Hospital', 'Admission', 'Diagnosis', 'Exposure', 'Ded%']]
    for _, r in q13a.head(30).iterrows():
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

    if len(ghosts):
        story.append(Spacer(1, 5 * mm))
        story.append(Paragraph('Ghost &amp; Anomalous-Hospital Claims', S_H2))
        story.append(Paragraph("High-value claims whose hospital ID is missing (NULL), a placeholder, or a phone "
                               "number - i.e. no traceable provider. These are prime ghost-admission leads.", S_BODY))
        gg = [['Beneficiary', 'Hospital ID', 'Type', 'Admission', 'Exposure', 'Ded%']]
        for _, r in ghosts.head(12).iterrows():
            gg.append([P(short(r['beneficiary'], 22)), P(short(r['hospital_code'], 16)), P(short(r['category'], 14)),
                       P(str(r['admission_date'])[:10]), P(inr(r['exposure'])), P(r['ded_pct'])])
        t = Table(gg, colWidths=[36 * mm, 32 * mm, 26 * mm, 22 * mm, 30 * mm, 14 * mm])
        t.setStyle(tbl_style()); story.append(t)
    story.append(PageBreak())


def q13b_section(story, q13b, deep):
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
    t.setStyle(tbl_style()); story.append(t)

    if deep and deep.get('hospitals'):
        story.append(Spacer(1, 5 * mm))
        story.append(Paragraph('Hospital deep-dives', S_H2))
        for h in deep['hospitals'][:3]:
            para = (f"<b>{esc(h['hospital_code'])}</b> - {h['hv_claims']:,} high-value claims, "
                    f"Rs {h['exposure_cr']:.2f} Cr exposure, Rs {h['deducted_cr']:.2f} Cr deducted "
                    f"({h['avg_ded_pct']}% average), of which <b>{h['full_ded_claims']}</b> were approved at Rs 0. ")
            if h.get('named_full_ded'):
                names = ", ".join(f"{esc(n['beneficiary'])} ({inr(n['exposure'])})" for n in h['named_full_ded'][:6])
                para += f"Beneficiaries with a 100% deduction here include {names}. "
            if h['full_ded_claims'] >= 5:
                para += ("Different beneficiaries at one login all hitting 100% deduction points to systematic "
                         "billing above the package ceiling rather than isolated patient fraud.")
            story.append(Paragraph(para, S_BODY))

    poly = (deep or {}).get('polyclinic') or {}
    if poly.get('claims'):
        story.append(Paragraph('ECHS polyclinic login pattern', S_H2))
        tops = ", ".join(f"{esc(x['hospital_code'])} ({x['avg_ded_pct']}%)" for x in poly.get('top_logins', [])[:5])
        story.append(Paragraph(
            f"Login codes of the form <b>p.</b> / <b>pol.</b> (ECHS polyclinics) carry {poly['claims']:,} high-value "
            f"claims with Rs {poly['deducted_cr']:.2f} Cr deducted at a {poly['avg_ded_pct']}% average - far above "
            f"private-hospital norms" + (f". Highest-deduction polyclinic logins: {tops}" if tops else "") + ". "
            "Polyclinic credentials routing high-value IPD claims that are then almost entirely rejected suggests "
            "these internal channels are being used to bypass pre-authorisation controls.", S_BODY))
    story.append(PageBreak())


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
    t.setStyle(tbl_style()); story.append(t)

    reg['ded_f'] = pd.to_numeric(reg['ded_pct'], errors='coerce').fillna(0)
    hi_ded = reg.sort_values('ded_f', ascending=False).iloc[0]
    hi_vol = reg.iloc[0]   # already sorted by exposure desc
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph('Regional implications', S_H2))
    story.append(Paragraph(
        f"<b>{esc(str(hi_ded['command']))}</b> shows the highest deduction rate ({hi_ded['ded_pct']}%) - the command "
        f"where claim scrutiny removes the largest share of billed value. <b>{esc(str(hi_vol['command']))}</b> carries "
        f"the largest absolute exposure (Rs {float(hi_vol['exposure_cr']):,.0f} Cr): a concentration of high-volume "
        f"hospital logins makes it the biggest absolute leakage surface even at a moderate rate. High-deduction "
        f"commands warrant a region-level audit of their top high-value hospitals.", S_BODY))
    story.append(PageBreak())


def q13d_section(story, q13d, cases):
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
    t.setStyle(tbl_style()); story.append(t)

    le = (cases or {}).get('lockin_examples')
    if le:
        ex = "; ".join(f"{esc(x['beneficiary'])} ({x['claims']} claims, {x['lockin_pct']}% at {esc(x['hospital'])})"
                       for x in le)
        story.append(Spacer(1, 4 * mm))
        story.append(Paragraph('Single-hospital lock-in', S_H2))
        story.append(Paragraph(
            "Natural medical histories spread across providers. Near-perfect single-hospital concentration over "
            "dozens of high-value admissions is the strongest repeat-claimant signal - it points to a fixed "
            f"beneficiary-hospital relationship that should be examined for any financial arrangement. Examples: "
            f"{ex}.", S_BODY))
    story.append(PageBreak())


def q13f_section(story, bulk, cases):
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
    t.setStyle(tbl_style()); story.append(t)

    tb = (cases or {}).get('top_bulk')
    spread = (cases or {}).get('bulk_spread')
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph('Why this matters', S_H2))
    if tb:
        story.append(Paragraph(
            f"The top event - <b>{esc(tb['beneficiary'])}</b> at <b>{esc(tb['hospital'])}</b> on {tb['date']} - "
            f"created <b>{tb['count']} intimation IDs in a single day</b>"
            + (f", spanning IDs {tb['first_id']}-{tb['last_id']} (near-consecutive). " if tb.get('consecutive') else ". ")
            + "Creating hundreds of records in one day is impossible through manual web-portal entry; near-consecutive "
              "ID ranges are the signature of programmatic batch insertion - portal credential compromise or insider "
              "database access, not ordinary claim fraud.", S_BODY))
    if spread and spread.get('prefixes'):
        known = [p['region'] for p in spread['prefixes'] if p['region']]
        rtxt = (", including " + ", ".join(known[:5])) if known else ""
        story.append(Paragraph(
            f"These {spread['n_events']} events span <b>{len(spread['prefixes'])} distinct card-prefix codes</b> "
            f"(each encoding an issuing ECHS region{rtxt}) - so this is not a single compromised login but a "
            f"multi-region pattern. Response: pull portal access logs (IP, session, timestamps) for these dates and "
            f"escalate to ECHS IT / CERT-In as a security incident.", S_BODY))
    story.append(PageBreak())


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


def recommendations(story, s, cases, deep):
    h1(story, 'Strategic Recommendations')
    story.append(Paragraph("Prioritised by composite risk and tied to the specific cases surfaced above. SLAs are "
                           "indicative response windows.", S_BODY))
    c = cases or {}
    tb, rc, du, cv = c.get('top_bulk'), c.get('top_repeat_claimant'), c.get('top_duplicate'), c.get('card_variation')
    hosps = (deep or {}).get('hospitals', [])
    hosp = hosps[0] if hosps else None
    poly = (deep or {}).get('polyclinic') or {}
    recs = []
    if tb:
        recs.append(('CRITICAL', 'Immediate', 'Portal-security investigation of bulk injection',
                     f"{esc(tb['beneficiary'])} created {tb['count']} intimation IDs in one day at {esc(tb['hospital'])}. "
                     f"Pull portal access logs (IP/session) for all {s.get('n_bulk_events',0)} events, suspend the involved "
                     f"logins, and escalate to ECHS IT / CERT-In."))
    if du:
        recs.append(('CRITICAL', '7 days', 'Recover same-day duplicate payments',
                     f"{esc(du['beneficiary'])}: {du['dup_count']} identical {inr(du['exposure'])} claims on "
                     f"{du['admission_date']} at {esc(du['hospital'])}. Confirm which submissions were paid, recover the "
                     f"surplus, and sweep that login for other same-day duplicates."))
    if rc:
        recs.append(('CRITICAL', '14 days', 'Physically verify the top chronic claimant',
                     f"{esc(rc['beneficiary'])} - {rc['claims']} high-value claims at {esc(rc['primary_hospital'])}. Obtain "
                     f"discharge summaries for a 20-claim sample and reconcile admission dates / ICU notes."))
    if cv:
        recs.append(('CRITICAL', 'Immediate', 'Investigate possible card-ID manipulation',
                     f"{esc(cv['beneficiary'])} appears on two near-identical cards ({esc(cv['card_a'])} / "
                     f"{esc(cv['card_b'])}). Verify against the service record - one pensioner or two?"))
    if hosp:
        recs.append(('HIGH', '60 days', 'Empanelment & billing audit of the top-deduction hospital',
                     f"{esc(hosp['hospital_code'])} - Rs {hosp['deducted_cr']:.2f} Cr deducted across {hosp['hv_claims']:,} "
                     f"claims ({hosp['full_ded_claims']} at 100%). Audit the empanelment package rates and a 10-claim "
                     f"line-item sample."))
    if poly.get('claims'):
        recs.append(('HIGH', '60 days', 'Segregate ECHS polyclinic claim channels',
                     f"Polyclinic logins carry {poly['claims']:,} high-value claims at {poly['avg_ded_pct']}% deduction. "
                     f"Restrict polyclinic logins to OPD/pharmacy and quarantine high-value IPD claims submitted through them."))
    recs.append(('HIGH', '30 days', 'Reject invalid hospital identifiers at intake',
                 f"{s.get('n_anomalous_hv_claims',0):,} high-value claims (Rs {s.get('anomalous_exposure_cr',0):,.0f} Cr) "
                 f"carry NULL or phone-like hospital IDs. Block submission where the hospital ID is not a valid portal login."))
    recs.append(('MEDIUM', 'Ongoing', 'Operationalise the risk score',
                 'Run the composite score nightly and route CRITICAL-band claims to auditors before settlement.'))
    data = [['Priority', 'SLA', 'Recommendation', 'Action']]
    for pr, sla, t1, t2 in recs:
        data.append([P(band_html(pr)), P(sla), P(bold(t1)), P(t2)])
    t = Table(data, colWidths=[18 * mm, 16 * mm, 44 * mm, 92 * mm]); t.setStyle(tbl_style()); story.append(t)
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("This report is produced by an automated screening system. Every flagged case is an "
                           "investigative lead, not a confirmed finding, and must be reviewed by a qualified auditor "
                           "before any action is taken.", S_WARN))


def build():
    s = load_summary()
    cases = load_json('module13_cases.json')
    deep = load_json('module13_hospital_deepdive.json')
    q13a = load_csv('q13a_top_claims.csv')
    dups = load_csv('q13a2_duplicates.csv')
    q13b = load_csv('q13b_hospital_scorecard.csv')
    reg = load_csv('q13c_regional.csv')
    q13d = load_csv('q13d_chronic_claimants.csv')
    bulk = load_csv('q13f_bulk_injection.csv')
    ghosts = load_csv('module13_ghost_claims.csv')

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
    methodology(story, s)
    limitations(story)
    signals_section(story, s, q13a, q13b, q13d, dups, bulk)
    case_studies(story, cases)
    q13a_section(story, q13a, dups, ghosts)
    q13b_section(story, q13b, deep)
    q13c_section(story, reg)
    q13d_section(story, q13d, cases)
    q13f_section(story, bulk, cases)
    scoring_section(story, s)
    recommendations(story, s, cases, deep)
    doc.build(story)
    print(f'PDF saved: {OUT}')


if __name__ == '__main__':
    build()
