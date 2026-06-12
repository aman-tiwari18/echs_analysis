"""
Generate Module 18 Report - Claim Processing Delay Analysis
Matches the exact formatting of Module 11 (Navy/Gold ECHS style).
"""
import os
import sys
import glob
import csv
import datetime
import time
from weasyprint import HTML

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, 'data')
OUT_DIR = os.path.join(BASE, 'reports')
os.makedirs(OUT_DIR, exist_ok=True)

today_str = datetime.date.today().strftime("%-d %B %Y")
ts        = time.strftime("%Y%m%d_%H%M%S")
PDF_OUT   = os.path.join(OUT_DIR, f"ECHS_Claim_Processing_Delay_Report_{ts}.pdf")

NAV  = "#1a2744"
GOLD = "#c9a84c"

def safe(v, d="—"):
    return str(v).strip() if v and str(v).strip() not in ("", "nan", "None", "0", "0.0") else d

def fmt(v):
    try: return f"{int(float(v)):,}"
    except: return str(v)

def fmt2(v):
    try: return f"{float(v):.2f}"
    except: return str(v)

def cr(v):
    try:
        val = float(v)
        if val >= 1e7:  return f"₹{val/1e7:.2f} Cr"
        if val >= 1e5:  return f"₹{val/1e5:.2f} L"
        return f"₹{val:,.0f}"
    except: return "₹0.00 Cr"

def th(*cols):
    return "<thead><tr>" + "".join(f"<th>{c}</th>" for c in cols) + "</tr></thead>"

def load_latest(pattern):
    files = glob.glob(os.path.join(DATA_DIR, pattern))
    if not files: return []
    latest = max(files, key=os.path.getmtime)
    data = []
    with open(latest, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

p01 = load_latest("01_Dataset_Overview*.csv")
p02 = load_latest("02_Delay_Analysis*.csv")
p03 = load_latest("03_Deduction_By_Speed*.csv")
p04 = load_latest("04_Suspicious_Claims*.csv")
p05 = load_latest("05_Systematic_Overbillers*.csv")
p06 = load_latest("06_Untouched_High_Billers*.csv")

tot_claims = 0
tot_exposure = 0
if p01:
    tot_claims = float(p01[0].get('total_claims', 0))
    tot_exposure = float(p01[0].get('total_claimed', 0))

total_cases = len(p04) + len(p05) + len(p06)
patterns_found = 6

# Exact CSS matched from Module 11
CSS_STR = f"""
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ font-family:Arial,Helvetica,sans-serif; font-size:9pt; color:#1a1a1a; line-height:1.55; background:#fff; }}

@page {{
    size:A4; margin:20mm 15mm 18mm 15mm;
    @top-left   {{ content:"ECHS FRAUD ANALYTICS REPORT — CONFIDENTIAL";
                  font-family:Arial; font-size:7.5pt; font-weight:700; color:{NAV};
                  border-bottom:1px solid #ccc; padding-bottom:4px; vertical-align:bottom; }}
    @top-right  {{ content:"IIT Kanpur | Page " counter(page);
                  font-family:Arial; font-size:7.5pt; color:#555;
                  border-bottom:1px solid #ccc; padding-bottom:4px; vertical-align:bottom; }}
    @bottom-left  {{ content:"RESTRICTED — For internal audit and investigative use only. Do not distribute without authorisation.";
                    font-family:Arial; font-size:7pt; color:#555; border-top:1px solid #ddd; padding-top:3px; }}
    @bottom-right {{ content:"Generated: {today_str}";
                    font-family:Arial; font-size:7pt; color:#555; border-top:1px solid #ddd; padding-top:3px; }}
}}
@page cover {{
    margin:0;
    @top-left{{content:none}} @top-right{{content:none}}
    @bottom-left{{content:none}} @bottom-right{{content:none}}
}}
.cover {{ page:cover; page-break-after:always; background:{NAV};
          width:210mm; height:297mm; display:flex; flex-direction:column;
          justify-content:center; align-items:center; text-align:center; position:relative; }}
.cover-topbar,.cover-botbar {{ position:absolute; left:0; right:0; height:8px; background:{GOLD}; }}
.cover-topbar {{ top:0; }} .cover-botbar {{ bottom:0; }}
.cover-title {{ font-size:32pt; font-weight:900; color:#fff; letter-spacing:2px; margin-bottom:10px; }}
.cover-sub   {{ font-size:12pt; color:#ccc; font-weight:300; margin-bottom:16px; }}
.cover-mod   {{ font-size:9pt; color:{GOLD}; font-weight:700; letter-spacing:2px; margin-bottom:28px; }}
.cover-boxes {{ display:flex; gap:2px; margin-bottom:32px; }}
.cover-box   {{ background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15);
                padding:10px 18px; min-width:120px; white-space:nowrap; text-align:center; }}
.cover-box-label {{ font-size:6.5pt; color:#aaa; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:5px; }}
.cover-box-val   {{ font-size:13pt; font-weight:800; color:#fff; }}
.cover-org  {{ font-size:11pt; color:{GOLD}; font-weight:700; margin-bottom:5px; }}
.cover-date {{ font-size:8.5pt; color:#aaa; }}

.pb  {{ page-break-before:always; }}
.nob {{ page-break-inside:avoid; }}

.metric-row {{ display:flex; gap:4px; margin:14px 0; }}
.mbox {{ background:{NAV}; color:#fff; flex:1; padding:12px 10px; text-align:center; }}
.mbox-label {{ font-size:6.5pt; color:#aaa; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px; }}
.mbox-val   {{ font-size:17pt; font-weight:900; color:#fff; }}
.mbox-sub   {{ font-size:6.5pt; color:#aaa; margin-top:3px; }}

h1 {{ font-size:13pt; font-weight:800; color:{NAV}; text-transform:uppercase;
      letter-spacing:1px; margin:18px 0 10px 0; }}

.ph {{ border-left:4px solid {GOLD}; padding:0 0 2px 12px; margin:18px 0 12px 0; }}
.ph-label {{ font-size:7.5pt; font-weight:700; color:{GOLD}; letter-spacing:2px; text-transform:uppercase; margin-bottom:4px; }}
.ph-ctx   {{ float:right; font-size:7.5pt; color:#888; font-style:italic; text-align:right; max-width:180px; line-height:1.3; margin-top:4px; }}
.ph-title {{ font-size:14pt; font-weight:900; color:{NAV}; text-transform:uppercase; letter-spacing:0.5px; clear:right; }}

p   {{ margin-bottom:7px; text-align:justify; }}
b   {{ font-weight:700; }}
ul  {{ margin:4px 0 8px 16px; }}
li  {{ margin-bottom:3px; }}

.tc {{ font-size:7.5pt; color:#666; margin-bottom:4px; }}

table.dt {{ width:100%; border-collapse:collapse; margin:6px 0 14px 0; font-size:8pt; }}
table.dt thead tr {{ background:{NAV}; color:#fff; }}
table.dt thead th {{ padding:6px 7px; text-align:left; font-weight:700; }}
table.dt tbody tr:nth-child(even) {{ background:#f4f6f9; }}
table.dt tbody td {{ padding:5px 7px; border-bottom:1px solid #e5e5e5; vertical-align:top; }}

.kf-head {{ font-size:11pt; font-weight:700; color:{NAV}; margin:14px 0 6px 0; }}
.kf-item {{ margin-bottom:7px; padding-left:8px; border-left:3px solid {GOLD}; font-size:8.5pt; line-height:1.5; }}

.action-item {{ margin-bottom:7px; font-size:8.5pt; }}
.action-num  {{ font-weight:800; color:{NAV}; }}
"""

H = [f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS_STR}</style></head><body>"""]

# ── COVER PAGE ────────────────────────────────────────────────────────────────
H.append(f"""
<div class="cover">
  <div class="cover-topbar"></div>
  <div class="cover-title">ECHS FRAUD ANALYTICS</div>
  <div class="cover-sub">Claim Processing Delay &amp; Fast-Track Vulnerability Analysis</div>
  <div class="cover-mod">COMPREHENSIVE REPORT — FY 2021–2026 EDITION (LAST 5 YEARS)</div>
  <div class="cover-boxes">
    <div class="cover-box"><div class="cover-box-label">Classification</div><div class="cover-box-val">RESTRICTED</div></div>
    <div class="cover-box"><div class="cover-box-label">Period</div><div class="cover-box-val">FY 2021–26</div></div>
    <div class="cover-box"><div class="cover-box-label">Records Scanned</div><div class="cover-box-val">25.9M+</div></div>
    <div class="cover-box"><div class="cover-box-label">Patterns Run</div><div class="cover-box-val">6 Patterns</div></div>
    <div class="cover-box"><div class="cover-box-label">Cases Flagged</div><div class="cover-box-val">{fmt(total_cases)}</div></div>
  </div>
  <div class="cover-org">IIT KANPUR — Data Analytics &amp; Fraud Intelligence Division</div>
  <div class="cover-date">{today_str} | Ex-Servicemen Contributory Health Scheme (ECHS)</div>
  <div class="cover-botbar"></div>
</div>
""")

# ── EXECUTIVE SUMMARY ─────────────────────────────────────────────────────────
H.append(f"""
<div class="pb">
<h1>Executive Summary</h1>
<p>This report investigates <b>Claim Processing Delays</b> and identifies vulnerabilities in UTI's adjudication process. The core finding is that speed shields claims from scrutiny: high-value claims processed on fast administrative tracks face practically zero deduction or audit review.</p>

<div class="metric-row">
  <div class="mbox"><div class="mbox-label">Total Cases Flagged</div><div class="mbox-val" style="color:#e74c3c">{fmt(total_cases)}</div><div class="mbox-sub">across 6 fraud patterns</div></div>
  <div class="mbox"><div class="mbox-label">Total Exposure</div><div class="mbox-val">{cr(tot_exposure)}</div><div class="mbox-sub">estimated financial risk</div></div>
  <div class="mbox"><div class="mbox-label">Patterns w/ Findings</div><div class="mbox-val">{patterns_found}</div><div class="mbox-sub">of 6 patterns</div></div>
  <div class="mbox"><div class="mbox-label">Analysis Period</div><div class="mbox-val">5 Yrs</div><div class="mbox-sub">FY 2021–2026</div></div>
</div>

<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>The Fast-Track Shielding Effect:</b> Claims approved in 0-15 days are deducted only {p03[0].get('pct_with_deduction','0') if p03 else '0'}% of the time, compared to standard claims.</div>
<div class="kf-item"><b>Suspicious Convergent Claims:</b> We flagged {fmt(len(p04))} anomalous cases where claims exceeding ₹1.2L were approved in under 10 days with absolutely zero deductions, bypassing all standard UTI procedures.</div>
<div class="kf-item"><b>Untouched High-Billers:</b> {fmt(len(p06))} top-billing hospitals have submitted high-value claims without facing a single UTI deduction or audit rejection in 5 years.</div>
<div class="kf-item"><b>Systematic Over-Billers:</b> {fmt(len(p05))} hospitals suffer chronic high UTI deductions (averaging >5%), indicating systematic padding of bills.</div>

<h1 style="margin-top:14px">Six Fraud Patterns — Summary</h1>
<table class="dt">
{th("#","Pattern","What It Detects","Cases Flagged")}
<tbody>
<tr><td>1</td><td>Dataset Overview</td><td>Total breakdown by audit grouping.</td><td><b>{fmt(len(p01))}</b> strata analyzed</td></tr>
<tr><td>2</td><td>Delay Analysis</td><td>Median E2E delays by audit state.</td><td><b>{fmt(len(p02))}</b> groups compared</td></tr>
<tr><td>3</td><td>Deduction by Speed</td><td>Correlation of approval speed to cut %.</td><td><b>{fmt(len(p03))}</b> time windows</td></tr>
<tr><td>4</td><td>Suspicious Fast-Track</td><td>High-bill + fast-appr + zero ded.</td><td><b>{fmt(len(p04))}</b> hospitals flagged</td></tr>
<tr><td>5</td><td>Systematic Overbillers</td><td>Hospitals with highest UTI cuts.</td><td><b>{fmt(len(p05))}</b> hospitals flagged</td></tr>
<tr><td>6</td><td>Untouched High-Billers</td><td>Hospitals with zero UTI cuts/audits.</td><td><b>{fmt(len(p06))}</b> hospitals flagged</td></tr>
</tbody>
</table>

<h1 style="margin-top:12px">Immediate Recommended Actions</h1>
<div class="action-item"><span class="action-num">1.</span> <b>Suspend Fast-Track for High-Value Claims:</b> Immediately route any claim >₹1.2L approved in <10 days to a mandatory secondary audit review before payment ({fmt(len(p04))} anomalous hospitals flagged).</div>
<div class="action-item"><span class="action-num">2.</span> <b>Audit Zero-Deduction Whitelists:</b> Initiate a retrospective manual audit of the {fmt(len(p06))} "Untouched High-Billers" who bypassed all UTI scrutiny over 5 years despite massive volumes.</div>
<div class="action-item"><span class="action-num">3.</span> <b>Investigate Systematic Over-Billers:</b> Send show-cause notices to the {fmt(len(p05))} hospitals facing chronic UTI deductions (>5%) demanding itemized justification for inflated billings.</div>
<div class="action-item"><span class="action-num">4.</span> <b>Implement Algorithmic Speed Bumps:</b> Introduce a system check preventing any hospital from receiving 100% approval across all their claims without triggering a randomized sampling audit.</div>
</div>""")

# ── PATTERN 1: Dataset Overview ───────────────────────────────────────────────
if p01:
    H.append(f"""<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 1</div>
  <div class="ph-ctx">Macro Claim Volumes by Audit Intensity</div>
  <div class="ph-title">System-wide Dataset Overview</div>
</div></div>
<p><b>Description:</b> A macro-level breakdown of the entire 5-year dataset, categorizing total claim volumes and financial exposure by their respective audit statuses.</p>

<div class="tc">Table 1.0 — Claims Breakdown by Audit Group</div>
<table class="dt">
{th("Audit Group","Total Claims","Total Claimed (₹)","Settled Claims","Pending Claims","Mean Bill")}
<tbody>""")
    for r in p01:
        H.append(f"<tr><td><b>{r.get('audit_group','')}</b></td>"
                 f"<td>{fmt(r.get('total_claims','0'))}</td>"
                 f"<td>{cr(r.get('total_claimed','0'))}</td>"
                 f"<td>{fmt(r.get('settled_claims','0'))}</td>"
                 f"<td>{fmt(r.get('pending_claims','0'))}</td>"
                 f"<td>₹{fmt(r.get('mean_bill','0'))}</td></tr>")
    
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item">The total dataset spans {fmt(tot_claims)} claims over 5 years, highlighting distinct adjudication channels based on audit intensity.</div>
</div>""")

# ── PATTERN 2: Delay Analysis ──────────────────────────────────────────────────
if p02:
    H.append(f"""<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 2</div>
  <div class="ph-ctx">Processing Timelines by Audit State</div>
  <div class="ph-title">End-to-End Delay Analysis</div>
</div></div>
<p><b>Description:</b> Measures the average processing delays across the claim lifecycle. 
<b>Avg Sub Delay:</b> Days from patient discharge to hospital submission. 
<b>Avg Appr Delay:</b> Days from submission to UTI approval. 
<b>Avg E2E Delay:</b> Total End-to-End days from discharge to final settlement. 
<b>Mean Bill:</b> Average financial value claimed by the hospital.</p>

<div class="tc">Table 2.0 — Cycle Times by Audit Group</div>
<table class="dt">
{th("Audit Group","Claims","Mean Bill","Avg Sub Delay","Avg Appr Delay","Avg E2E Delay","Deducted Claims")}
<tbody>""")
    for r in p02:
        H.append(f"<tr><td><b>{r.get('audit_group','')}</b></td>"
                 f"<td>{fmt(r.get('total_claims','0'))}</td>"
                 f"<td>₹{fmt(r.get('mean_bill','0'))}</td>"
                 f"<td>{fmt2(r.get('avg_sub_delay','0'))}d</td>"
                 f"<td>{fmt2(r.get('avg_appr_delay','0'))}d</td>"
                 f"<td><b>{fmt2(r.get('avg_e2e_delay','0'))}d</b></td>"
                 f"<td>{fmt(r.get('deducted_claims','0'))} ({fmt2(r.get('mean_deduction_pct','0'))}%)</td></tr>")
    
    avg_e2e_rej = fmt2(p02[-1].get('avg_e2e_delay', 0)) if p02 else '0'
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item">Claims that eventually face Audit Rejection average a significantly higher processing delay ({avg_e2e_rej} days end-to-end) compared to non-audited claims.</div>
</div>""")

# ── PATTERN 3: Speed vs Deduction ─────────────────────────────────────────────
if p03:
    H.append(f"""<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 3</div>
  <div class="ph-ctx">UTI Adjudication Stringency vs Processing Speed</div>
  <div class="ph-title">The Fast-Track Shielding Effect</div>
</div></div>
<p><b>Description:</b> This table maps UTI deduction frequency against claim approval speed. It reveals a critical vulnerability: claims pushed through faster administrative tracks (0-15 days) experience drastically lower deduction rates than claims processed in the standard timeframe.</p>

<div class="tc">Table 3.0 — Deduction Frequency by Approval Speed Window</div>
<table class="dt">
{th("Approval Window","Claims","Deducted Count","% Deducted","Mean Bill","Total Exposure")}
<tbody>""")
    for r in p03:
        H.append(f"<tr><td><b>{r.get('approval_window','')}</b></td>"
                 f"<td>{fmt(r.get('total_claims','0'))}</td>"
                 f"<td>{fmt(r.get('deducted_claims','0'))}</td>"
                 f"<td><b style='color:#c0392b'>{r.get('pct_with_deduction','0')}%</b></td>"
                 f"<td>₹{fmt(r.get('mean_bill','0'))}</td>"
                 f"<td>{cr(r.get('total_exposure','0'))}</td></tr>")
    
    ded_pct = p03[0].get('pct_with_deduction','0') if p03 else '0'
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item">There is a glaring systemic flaw where adjudication speed actively prevents scrutiny: claims approved on the 0-15 day "fast-track" face deductions only {ded_pct}% of the time.</div>
<div class="kf-item">As approval speed slows down into longer windows, the probability of UTI deductions drastically increases, exposing the lack of automated checks on fast-tracked claims.</div>
</div>""")

# ── PATTERN 4: Suspicious Fast-Track ──────────────────────────────────────────
if p04:
    H.append(f"""<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 4</div>
  <div class="ph-ctx">Anomalous Convergence: Fast + High Value + Zero Scrutiny</div>
  <div class="ph-title">Suspicious Fast-Track Claims</div>
</div></div>
<p><b>Description:</b> Highlights hospitals exploiting the fast-track vulnerability. These facilities submitted claims in the top 5% by value (>₹1.2L) that were approved in the top 5% of speed (<=10 days) with absolutely zero UTI deductions.</p>

<div class="tc">Table 4.0 — Suspicious Fast-Track Exploitation (Top 15)</div>
<table class="dt">
{th("Hospital","City","Flagged Claims","Mean Bill","Mean Appr Delay","Total Exposure","Audited","Rejected")}
<tbody>""")
    for r in p04[:15]:
        H.append(f"<tr><td><b>{r.get('hospital_name','')}</b></td>"
                 f"<td>{r.get('city','')}</td>"
                 f"<td><b style='color:#c0392b'>{fmt(r.get('flagged_claims','0'))}</b></td>"
                 f"<td>₹{fmt(r.get('mean_bill','0'))}</td>"
                 f"<td>{r.get('mean_approval_days','0')}d</td>"
                 f"<td>{cr(r.get('total_exposure','0'))}</td>"
                 f"<td>{r.get('audited_count','0')}</td>"
                 f"<td>{r.get('rejected_count','0')}</td></tr>")
    
    exp_4 = cr(sum([float(r.get('total_exposure',0)) for r in p04]))
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item">Identified {fmt(len(p04))} anomalous hospitals that explicitly target the 0-15 day fast-track vulnerability.</div>
<div class="kf-item">These flagged hospitals submitted massive claims (mean bill >₹1.2L) that were instantly approved (mean <10 days) with absolutely zero UTI deductions, exposing {exp_4} in highly suspicious billing.</div>
</div>""")

# ── PATTERN 5: Systematic Over-billers ────────────────────────────────────────
if p05:
    H.append(f"""<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 5</div>
  <div class="ph-ctx">Chronic Deduction Hospitals</div>
  <div class="ph-title">Systematic Over-Billers</div>
</div></div>
<p><b>Description:</b> Hospitals facing the highest aggregate UTI cuts across all claims. A consistently high deduction percentage indicates a hospital that systematically inflates bills or charges for unapproved consumables.</p>

<div class="tc">Table 5.0 — Systematic Over-Billers (Top 15 by Deduction %)</div>
<table class="dt">
{th("Hospital","City","Claims","Mean Bill","% Deducted Overall","Claims Deducted","Mean Appr Delay")}
<tbody>""")
    for r in p05[:15]:
        H.append(f"<tr><td><b>{r.get('hospital_name','')[:35]}</b></td>"
                 f"<td>{r.get('city','')}</td>"
                 f"<td>{fmt(r.get('total_claims','0'))}</td>"
                 f"<td>₹{fmt(r.get('mean_bill','0'))}</td>"
                 f"<td><b style='color:#c0392b'>{r.get('deduction_pct','0')}%</b></td>"
                 f"<td>{r.get('pct_claims_deducted','0')}%</td>"
                 f"<td>{r.get('mean_appr_delay','0')}d</td></tr>")
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item">Flagged {fmt(len(p05))} "Systematic Over-billers" who maintain chronic UTI deduction rates exceeding 5% on average.</div>
<div class="kf-item">A consistently high deduction percentage is the primary indicator of systematic hospital bill inflation or repeated charging for non-entitled consumables.</div>
</div>""")

# ── PATTERN 6: Untouched High-Billers ─────────────────────────────────────────
if p06:
    H.append(f"""<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 6</div>
  <div class="ph-ctx">High Volume, High Value, Zero Scrutiny</div>
  <div class="ph-title">Untouched High-Billers</div>
</div></div>
<p><b>Description:</b> Hospitals processing massive volumes of high-value claims (>₹1L mean bill) where UTI has <b>never</b> deducted a rupee and Audit has <b>never</b> rejected a claim. Identifies potential "whitelist" exploitation or extreme UTI negligence.</p>

<div class="tc">Table 6.0 — Untouched High-Billers (Top 15 by Volume)</div>
<table class="dt">
{th("Hospital","City","Total Claims","Mean Bill","UTI Ded %","Rejections","Mean Appr Delay")}
<tbody>""")
    for r in p06[:15]:
        H.append(f"<tr><td><b>{r.get('hospital_name','')[:35]}</b></td>"
                 f"<td>{r.get('city','')}</td>"
                 f"<td><b style='color:#c0392b'>{fmt(r.get('total_claims','0'))}</b></td>"
                 f"<td>₹{fmt(r.get('mean_bill','0'))}</td>"
                 f"<td>{r.get('deduction_pct','0')}%</td>"
                 f"<td>0</td>"
                 f"<td>{r.get('mean_appr_delay','0')}d</td></tr>")
    
    exp_6 = cr(sum([float(r.get('total_claimed',0)) for r in p06]))
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item">Identified {fmt(len(p06))} "Untouched High-Billers" processing high-value claims (mean bill >₹1L) with massive volumes.</div>
<div class="kf-item">These top-billing entities have billed {exp_6} with a highly unnatural <b>zero</b> percent UTI deduction and <b>zero</b> audit rejections over a 5-year span.</div>
</div>""")


# ── CONSOLIDATED SUMMARY ──────────────────────────────────────────────────────
H.append(f"""<div class="pb">
<h1>Consolidated Summary</h1>
<p class="tc" style="margin-bottom:10px">All findings are based on structured database analysis and must be
corroborated with physical audit records before enforcement action is taken.</p>
<table class="dt">
{th("Pattern","Fraud Pattern","Cases Flagged","Exposure")}
<tbody>
<tr><td>Delay</td><td>Audit vs Admin Fast-Track Discrepancy</td><td><b>{fmt(len(p02))}</b> groups</td><td>System-wide</td></tr>
<tr><td>Speed</td><td>Fast-Track Shielding (0-15d approvals)</td><td><b>{fmt(p03[0].get('total_claims','0') if p03 else '0')}</b></td><td>{cr(p03[0].get('total_exposure','0') if p03 else '0')}</td></tr>
<tr><td>Fast-Track</td><td>High-Value Claims Bypassing Scrutiny</td><td><b>{fmt(len(p04))}</b> hosp</td><td>{cr(sum([float(r.get('total_exposure',0)) for r in p04]))}</td></tr>
<tr><td>Over-Bill</td><td>Systematic Hospital Bill Inflation</td><td><b>{fmt(len(p05))}</b> hosp</td><td>{cr(sum([float(r.get('total_claimed',0)) for r in p05]))}</td></tr>
<tr><td>Untouched</td><td>High-Value Zero-Scrutiny Whitelists</td><td><b>{fmt(len(p06))}</b> hosp</td><td>{cr(sum([float(r.get('total_claimed',0)) for r in p06]))}</td></tr>
</tbody>
</table>

</div>
</body></html>""")

# ── RENDER ────────────────────────────────────────────────────────────────────
full_html = "".join(H)
print("Generating PDF ...")
HTML(string=full_html, base_url=BASE).write_pdf(PDF_OUT)
print(f"✅ Saved → {PDF_OUT}")
