"""
ECHS Hospital Specialty Misuse — Module 12 Report
HTML + WeasyPrint architecture.
"""

import os, csv, glob, re, time
from datetime import date

try:
    from weasyprint import HTML, CSS
except ImportError:
    print("ERROR: weasyprint not installed. Run: pip install weasyprint")
    exit(1)

BASE        = os.path.dirname(os.path.abspath(__file__))
DATA_DIR    = os.path.join(BASE, "data", "report_data")
REPORTS_DIR = os.path.join(BASE, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

today_str = date.today().strftime("%-d %B %Y")
ts        = time.strftime("%Y%m%d_%H%M%S")
PDF_OUT   = os.path.join(REPORTS_DIR, f"ECHS_Hospital_Specialty_Misuse_Report_{ts}.pdf")

NAV  = "#1a2744"
GOLD = "#c9a84c"

# ── Helpers ──────────────────────────────────────────────────────────────────

def fmt(n):
    try: return f"{int(float(n)):,}"
    except: return str(n)

def cr(n):
    try:
        v = float(n)
        if v >= 1e7:  return f"₹{v/1e7:.2f} Cr"
        if v >= 1e5:  return f"₹{v/1e5:.2f} L"
        return f"₹{v:,.0f}"
    except: return str(n)

def safe(v, d="—"):
    return str(v).strip() if v and str(v).strip() not in ("", "nan", "None", "0", "0.0") else d

def risk_txt(r):
    r = str(r).upper()
    if "CRITICAL" in r: return f'<span style="color:#c0392b;font-weight:700">CRITICAL</span>'
    if "HIGH"     in r: return f'<span style="color:#d4680a;font-weight:700">HIGH</span>'
    if "MEDIUM"   in r: return f'<span style="color:#7f8c8d;font-weight:600">MEDIUM</span>'
    return f'<span style="color:#27ae60;font-weight:600">LOW</span>'

def th(*cols):
    return "<thead><tr>" + "".join(f"<th>{c}</th>" for c in cols) + "</tr></thead>"

# ── Load CSVs ─────────────────────────────────────────────────────────────────

def load_latest(pattern):
    files = glob.glob(os.path.join(DATA_DIR, pattern))
    if not files:
        return []
    files.sort(key=os.path.getmtime, reverse=True)
    rows = []
    with open(files[0], encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

p01a = load_latest("01a_specialty_misuse_hospitals*.csv")
p01a = [r for r in p01a if float(r.get('total_claimed', 0)) > 0]
p01a = sorted(p01a, key=lambda r: float(r.get('total_claimed', 0)), reverse=True)

p02a = load_latest("02a_nabh_benchmark_by_type*.csv")
p02b = load_latest("02b_nabh_high_deduction_anomalies*.csv")
p02d = load_latest("02d_military_hospital_breakdown*.csv")
p03b_all = load_latest("03b_ipd_without_ipd_empanelment*.csv")
# Refine: The empanelment registry uses clinical specialty names (e.g. 'General Medicine'),
# NOT 'IPD'/'Indoor'/'Inpatient'. So the SQL LIKE filter flags ALL hospitals.
# Classify into 3 tiers based on empanelment content.
p03b_no_emp = [r for r in p03b_all if str(r.get('actual_empaneled_services','')).strip().upper() in ('', 'NULL', 'NONE', '—')]
p03b_has_emp = [r for r in p03b_all if str(r.get('actual_empaneled_services','')).strip().upper() not in ('', 'NULL', 'NONE', '—')]

# Further split has_emp into IPD-capable vs OPD-only
IPD_INHERENT_KW = ['icu', 'intensive care', 'critical care', 'coronary care', 'burn unit',
    'surgery', 'surgical', 'nicu', 'picu', 'micu', 'nsicu', 'cticu', 'iccu',
    'obstetrics', 'neonatal', 'neonatology', 'joint replacement', 'arthroplasty',
    'arthroscop', 'spine', 'transplant', 'chemotherapy', 'radiation oncology',
    'radiotherapy', 'bone marrow', 'heart transplant', 'trauma', 'cochlear implant']
def _has_ipd_capability(emp_str):
    s = str(emp_str).lower()
    return any(kw in s for kw in IPD_INHERENT_KW)

p03b_opd_only = [r for r in p03b_has_emp if not _has_ipd_capability(r.get('actual_empaneled_services',''))]
p03b_ipd_capable = [r for r in p03b_has_emp if _has_ipd_capability(r.get('actual_empaneled_services',''))]
p03b = p03b_no_emp  # Primary flagged set for exposure calculation
p04a = load_latest("04a_hospital_yoy_billing_spike*.csv")
p05b = load_latest("05b_low_tier_hospitals_high_value*.csv")

# Computations for Executive Summary
def sum_exposure(rows, key="total_claimed"):
    s = 0
    for r in rows:
        try:
            v = r.get(key) or r.get("claimed_cr") or r.get("total_claimed_lakh") or 0
            if key == "claimed_cr": v = float(v) * 1e7
            elif key == "total_claimed_lakh": v = float(v) * 1e5
            s += float(v)
        except: pass
    return s

total_exposure = sum([
    sum_exposure(p01a), sum_exposure(p02b, "claimed_lakh"),
    sum_exposure(p03b), sum_exposure(p03b_opd_only),  # Tier A + Tier B only
    sum_exposure(p04a, "curr_claimed_lakh"), sum_exposure(p05b, "total_claimed_lakh")
])

p03b_flagged_total = len(p03b) + len(p03b_opd_only)  # Only CRITICAL + HIGH tiers
total_hospitals_flagged = len(p01a) + len(p02b) + p03b_flagged_total + len(p04a) + len(p05b)
patterns_found = sum(1 for p in [p01a, p02b, p03b, p04a, p05b] if p)

# ── CSS ───────────────────────────────────────────────────────────────────────

CSS_STR = f"""
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ font-family:Arial,Helvetica,sans-serif; font-size:9pt; color:#1a1a1a; line-height:1.55; background:#fff; }}

@page {{
    size:A4; margin:20mm 15mm 18mm 15mm;
    @top-left   {{ content:"ECHS FRAUD ANALYTICS REPORT — CONFIDENTIAL"; font-family:Arial; font-size:7.5pt; font-weight:700; color:{NAV}; border-bottom:1px solid #ccc; padding-bottom:4px; vertical-align:bottom; }}
    @top-right  {{ content:"IIT Kanpur | Page " counter(page); font-family:Arial; font-size:7.5pt; color:#555; border-bottom:1px solid #ccc; padding-bottom:4px; vertical-align:bottom; }}
    @bottom-left  {{ content:"RESTRICTED — For internal audit and investigative use only. Do not distribute without authorisation."; font-family:Arial; font-size:7pt; color:#555; border-top:1px solid #ddd; padding-top:3px; }}
    @bottom-right {{ content:"Generated: {today_str}"; font-family:Arial; font-size:7pt; color:#555; border-top:1px solid #ddd; padding-top:3px; }}
}}
@page cover {{ margin:0; @top-left{{content:none}} @top-right{{content:none}} @bottom-left{{content:none}} @bottom-right{{content:none}} }}
.cover {{ page:cover; page-break-after:always; background:{NAV}; width:210mm; height:297mm; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; position:relative; }}
.cover-topbar,.cover-botbar {{ position:absolute; left:0; right:0; height:8px; background:{GOLD}; }}
.cover-topbar {{ top:0; }} .cover-botbar {{ bottom:0; }}
.cover-title {{ font-size:32pt; font-weight:900; color:#fff; letter-spacing:2px; margin-bottom:10px; }}
.cover-sub   {{ font-size:12pt; color:#ccc; font-weight:300; margin-bottom:16px; }}
.cover-mod   {{ font-size:9pt; color:{GOLD}; font-weight:700; letter-spacing:2px; margin-bottom:28px; }}
.cover-boxes {{ display:flex; gap:2px; margin-bottom:32px; }}
.cover-box   {{ background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); padding:10px 18px; min-width:120px; white-space:nowrap; text-align:center; }}
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

h1 {{ font-size:13pt; font-weight:800; color:{NAV}; text-transform:uppercase; letter-spacing:1px; margin:18px 0 10px 0; }}

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

# ── BUILD HTML ────────────────────────────────────────────────────────────────

H = [f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS_STR}</style></head><body>"]

# ── COVER ─────────────────────────────────────────────────────────────────────
H.append(f"""
<div class="cover">
  <div class="cover-topbar"></div>
  <div class="cover-title">ECHS FRAUD ANALYTICS</div>
  <div class="cover-sub">Hospital Specialty Misuse &amp; Service Empanelment Analysis</div>
  <div class="cover-mod">COMPREHENSIVE REPORT — FY 2021–2026 EDITION (LAST 5 YEARS)</div>
  <div class="cover-boxes">
    <div class="cover-box"><div class="cover-box-label">Classification</div><div class="cover-box-val">RESTRICTED</div></div>
    <div class="cover-box"><div class="cover-box-label">Period</div><div class="cover-box-val">FY 2021–26</div></div>
    <div class="cover-box"><div class="cover-box-label">Records Scanned</div><div class="cover-box-val">25.9M+</div></div>
    <div class="cover-box"><div class="cover-box-label">Patterns Run</div><div class="cover-box-val">5 Patterns</div></div>
    <div class="cover-box"><div class="cover-box-label">Entities Flagged</div><div class="cover-box-val">{fmt(total_hospitals_flagged)}</div></div>
  </div>
  <div class="cover-org">IIT KANPUR — Data Analytics &amp; Fraud Intelligence Division</div>
  <div class="cover-date">{today_str} | Ex-Servicemen Contributory Health Scheme (ECHS)</div>
  <div class="cover-botbar"></div>
</div>
""")

# ── EXECUTIVE SUMMARY ─────────────────────────────────────────────────────────
H.append(f"""<div class="pb">
<h1>Executive Summary</h1>
<p>This report investigates hospital specialty misuse — cases where facilities bill for services outside their
designated category, and anomalous deduction patterns across hospitals. Five primary fraud patterns are confirmed.</p>

<div class="metric-row">
  <div class="mbox"><div class="mbox-label">Hospitals Flagged</div><div class="mbox-val" style="color:#e74c3c">{fmt(total_hospitals_flagged)}</div><div class="mbox-sub">across 5 fraud patterns</div></div>
  <div class="mbox"><div class="mbox-label">Total Exposure</div><div class="mbox-val">{cr(total_exposure)}</div><div class="mbox-sub">estimated financial risk</div></div>
  <div class="mbox"><div class="mbox-label">Patterns w/ Findings</div><div class="mbox-val">{patterns_found}</div><div class="mbox-sub">of 5 patterns</div></div>
  <div class="mbox"><div class="mbox-label">Analysis Period</div><div class="mbox-val">5 Yrs</div><div class="mbox-sub">FY 2021–2026</div></div>
</div>

<h1 style="margin-top:14px">Five Fraud Patterns — Summary</h1>
<table class="dt">
{th("#","Pattern","What It Detects","Cases Flagged")}
<tbody>
<tr><td>1</td><td>Specialty Category Billing Fraud</td><td>Type-3 facilities (dental clinics and diagnostic labs) billing IPD admissions.</td><td><b>{fmt(len(p01a))}</b> facilities</td></tr>
<tr><td>2</td><td>NABH vs Non-NABH Divergence</td><td>NABH-accredited facilities show consistently lower deduction rates, but some anomalies exist.</td><td><b>{fmt(len(p02b))}</b> anomalous</td></tr>
<tr><td>3</td><td>Out of Scope Empanelment</td><td>Hospitals billing for IPD services when they are NOT empaneled for IPD.</td><td><b>{fmt(p03b_flagged_total)}</b> facilities</td></tr>
<tr><td>4</td><td>Year-over-Year Billing Spike</td><td>Sudden 100%+ annual growth in claim amount indicating deliberate strategy change.</td><td><b>{fmt(len(p04a))}</b> facilities</td></tr>
<tr><td>5</td><td>High-Value Claims at Low-Tier</td><td>Type-3 facilities billing abnormally high individual claim amounts (over ₹1L).</td><td><b>{fmt(len(p05b))}</b> facilities</td></tr>
</tbody>
</table>

<h1 style="margin-top:12px">Immediate Recommended Actions</h1>
<div class="action-item"><span class="action-num">1.</span> <b>Audit all Type-3 IPD Billings</b> ({fmt(len(p01a))} cases) — Deny all IPD claims from dental clinics unless explicitly authorized.</div>
<div class="action-item"><span class="action-num">2.</span> <b>Investigate anomalous NABH hospitals</b> ({fmt(len(p02b))} cases) — A high deduction rate despite NABH status suggests potential bill padding.</div>
<div class="action-item"><span class="action-num">3.</span> <b>Block out-of-scope empanelment billing</b> ({fmt(p03b_flagged_total)} facilities) — Enforce system-level blocks preventing non-IPD hospitals from submitting IPD bills.</div>
<div class="action-item"><span class="action-num">4.</span> <b>Review YoY billing spike</b> ({fmt(len(p04a))} facilities) — Request clinical justification for hospital billing that has doubled year-over-year.</div>
<div class="action-item"><span class="action-num">5.</span> <b>Flag high-value Type-3 claims</b> ({fmt(len(p05b))} facilities) — Require manual pre-authorization for any Type-3 claim exceeding ₹50k.</div>
</div>
""")

# ── PATTERN 1 ─────────────────────────────────────────────────────────────────
if p01a:
    H.append(f"""<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 1</div>
  <div class="ph-ctx">Type-3 Facilities (Dental/Diag)</div>
  <div class="ph-title">Specialty Category Billing Fraud (IPD)</div>
</div></div>
<p><b>Description:</b> Type-3 facilities (dental clinics and diagnostic laboratories) are billing
inpatient (IPD) admissions — a service category they are not licensed or equipped to provide.
These facilities should only handle outpatient procedures. <b>All such IPD claims represent severe
policy violations.</b></p>
<p><b>Total Facilities Flagged:</b> <span style="color:#c0392b;font-weight:700">{fmt(len(p01a))}</span></p>
<div class="tc">Table 1.1 — Type-3 Facilities Billing IPD Claims (Top 15 by Claimed Amount)</div>
<table class="dt">
{th("Hospital Name","Type","City","State","IPD Claims","Claimed Amt","Ded. %")}
<tbody>""")
    for r in p01a[:15]:
        H.append(f"<tr><td><b>{safe(r.get('hospital_name',''))[:30]}</b></td>"
                 f"<td>{safe(r.get('hosp_type_desc',''))}</td>"
                 f"<td>{safe(r.get('city',''))}</td>"
                 f"<td>{safe(r.get('state',''))}</td>"
                 f"<td><b style='color:#c0392b'>{safe(r.get('ipd_claims','0'))}</b></td>"
                 f"<td><b>{cr(r.get('total_claimed',0))}</b></td>"
                 f"<td>{safe(r.get('deduction_pct','0'))}%</td></tr>")
    # Sub-type breakdown
    p01a_dental = [r for r in p01a if r.get('hosp_type_desc','') == 'D']
    p01a_lab = [r for r in p01a if r.get('hosp_type_desc','') == 'L']
    p01a_other = [r for r in p01a if r.get('hosp_type_desc','') not in ('D', 'L')]
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Sub-Type Breakdown:</b> Of the {fmt(len(p01a))} Type-3 facilities flagged,
<b>{fmt(len(p01a_dental))}</b> are Dental clinics (D), <b>{fmt(len(p01a_lab))}</b> are Diagnostic
Laboratories (L), and <b>{fmt(len(p01a_other))}</b> have other/miscategorised descriptions. Dental clinics
filing IPD is the most clear-cut fraud signal — these have no beds, no wards, no operating theatres.</div>
<div class="kf-item"><b>Possible Misclassification:</b> Some entries (e.g. medical colleges categorised
as Type-3) may reflect database misclassification rather than fraud. However, the billing itself
remains a policy violation until the hospital type is officially corrected.</div>
<div class="kf-item"><b>Recommended Action:</b> Deny all IPD claims from dental/diagnostic clinics unless
explicitly authorised. Conduct site inspections to verify if overnight facilities exist. Correct hospital
type misclassifications in the office_master table.</div>
</div>""")

# ── PATTERN 2 ─────────────────────────────────────────────────────────────────
if p02b:
    nabh_count = sum(int(r.get('hospital_count', 0)) for r in p02a if r.get('nabh_status') == 'NABH')
    non_nabh_count = sum(int(r.get('hospital_count', 0)) for r in p02a if r.get('nabh_status') == 'Non-NABH')
    H.append(f"""<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 2</div>
  <div class="ph-ctx">NABH Divergence Anomaly<br/>(&gt;15% Deduction in NABH)</div>
  <div class="ph-title">NABH Accreditation &amp; High Deduction Anomalies</div>
</div></div>
<p><b>Description:</b> NABH-accredited facilities are expected to adhere to higher billing standards,
typically resulting in lower deduction rates (the difference between claimed and approved amounts). 
When an NABH hospital consistently suffers extremely high deductions (over 15%), it indicates chronic
over-billing, unbundled charging, or billing for non-entitled items despite their accreditation.</p>
<p><b>System-wide Context:</b> There are <b style="color:{NAV}">{fmt(nabh_count)}</b> NABH-accredited hospitals and <b style="color:{NAV}">{fmt(non_nabh_count)}</b> Non-NABH hospitals currently active in the dataset.</p>
<p><b>Total Anomalous Hospitals:</b> <span style="color:#c0392b;font-weight:700">{fmt(len(p02b))}</span></p>
<div class="tc">Table 2.1 — NABH Hospitals with Anomalously High Deduction Rates (Top 15)</div>
<table class="dt">
{th("Hospital Name","Type","City","Claims","Claimed (Lakh)","Approved (Lakh)","Ded. %")}
<tbody>""")
    for r in p02b[:15]:
        H.append(f"<tr><td><b>{safe(r.get('hospital_name',''))[:30]}</b></td>"
                 f"<td>{safe(r.get('hosp_type_desc',''))[:20]}</td>"
                 f"<td>{safe(r.get('city',''))}</td>"
                 f"<td>{safe(r.get('total_claims','0'))}</td>"
                 f"<td><b>{cr(float(r.get('claimed_lakh',0))*100000)}</b></td>"
                 f"<td>{cr(float(r.get('approved_lakh',0))*100000)}</td>"
                 f"<td><b style='color:#c0392b'>{safe(r.get('deduction_pct','0'))}%</b></td></tr>")
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Ded. % (Deduction Percentage):</b> A high deduction rate in an NABH hospital 
contradicts the expected billing quality of an accredited facility. These hospitals may be utilizing 
their NABH status to attract ECHS patients while systematically inflating bills to maximize approved payouts.</div>
<div class="kf-item">Military Hospitals (Type M) often show very high deductions, but they are not the 
focus here; these are private empanelled NABH facilities exhibiting predatory billing behaviors.</div>
</div>""")

# ── PATTERN 3 ─────────────────────────────────────────────────────────────────
if p03b or p03b_opd_only:
    p03b_sorted = sorted(p03b, key=lambda r: float(r.get('total_claimed', 0)), reverse=True)
    p03b_opd_sorted = sorted(p03b_opd_only, key=lambda r: float(r.get('total_claimed', 0)), reverse=True)
    H.append(f"""<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 3</div>
  <div class="ph-ctx">Services vs Claims<br/>(IPD Billing Scope Violations)</div>
  <div class="ph-title">Services Outside Empaneled Scope</div>
</div></div>
<p><b>Description:</b> Hospitals must be registered in the ECHS empanelment system
(<code>empanel_hospital_service</code>) to bill for any service. The registry tracks <b>300 clinical
specialties</b> grouped under 10 headers, but does <b>not</b> use "IPD" as a service category.
Out of <b>{fmt(len(p03b_all))}</b> hospitals filing IPD claims, <b>{fmt(len(p03b_ipd_capable))}</b>
have IPD-inherent services (ICU, Surgery, Critical Care) in their empanelment and are considered
legitimate — these are <b>excluded</b> from this analysis. The remaining
<b style="color:#c0392b">{fmt(p03b_flagged_total)}</b> hospitals are flagged below.</p>

<p>
<span style="color:#c0392b;font-weight:700">● CRITICAL:</span> {fmt(len(p03b))} hospitals — Zero empanelment record
&nbsp;&nbsp;|&nbsp;&nbsp;
<span style="color:#d4680a;font-weight:700">● HIGH:</span> {fmt(len(p03b_opd_only))} hospitals — OPD-only empanelment billing IPD
</p>

<p><b>Total Facilities Flagged:</b> <span style="color:#c0392b;font-weight:700">{fmt(p03b_flagged_total)}</span></p>

<div class="tc">Table 3.1 — CRITICAL: IPD Claims from Hospitals with Zero Empanelment (Top 5)</div>
<table class="dt">
{th("Hospital","Type","City","IPD Claims","Claimed Amt","Status")}
<tbody>""")
    for r in p03b_sorted[:5]:
        H.append(f"<tr><td><b>{safe(r.get('hospital_name',''))[:30]}</b></td>"
                 f"<td>{safe(r.get('hosp_type_desc',''))[:15]}</td>"
                 f"<td>{safe(r.get('city',''))}</td>"
                 f"<td><b style='color:#c0392b'>{safe(r.get('ipd_claims_filed','0'))}</b></td>"
                 f"<td><b>{cr(r.get('total_claimed',0))}</b></td>"
                 f"<td style='font-size:7pt;color:#c0392b;font-weight:700'>No Empanelment Record</td></tr>")
    H.append(f"""</tbody></table>

<div class="tc">Table 3.2 — HIGH: OPD-Only Empanelment but Billing IPD (Top 5)</div>
<table class="dt">
{th("Hospital","Type","City","IPD Claims","Claimed Amt","Empaneled Services")}
<tbody>""")
    for r in p03b_opd_sorted[:5]:
        emp = safe(r.get('actual_empaneled_services',''))
        if len(emp) > 45: emp = emp[:42] + '...'
        H.append(f"<tr><td><b>{safe(r.get('hospital_name',''))[:30]}</b></td>"
                 f"<td>{safe(r.get('hosp_type_desc',''))[:15]}</td>"
                 f"<td>{safe(r.get('city',''))}</td>"
                 f"<td><b style='color:#d4680a'>{safe(r.get('ipd_claims_filed','0'))}</b></td>"
                 f"<td><b>{cr(r.get('total_claimed',0))}</b></td>"
                 f"<td style='font-size:6.5pt'>{emp}</td></tr>")
    H.append(f"""</tbody></table>

<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Zero Empanelment (CRITICAL):</b> {fmt(len(p03b))} hospitals have no entry in the
<code>empanel_hospital_service</code> table. They bill ECHS for inpatient services without any formal
authorisation. Major hospitals (Artemis, Park Hospital, Paras Healthcare) appear in this list,
suggesting the empanelment registry itself is incomplete for a large portion of the ECHS network.</div>
<div class="kf-item"><b>OPD-Only Empanelment (HIGH):</b> {fmt(len(p03b_opd_only))} hospitals are empaneled
only for consultative/diagnostic services (e.g. Cardiology, Dialysis, Ophthalmology) that do not
inherently require overnight admission, yet they are filing IPD claims. These are the most actionable
fraud signals — the hospital's own empanelment proves it lacks IPD infrastructure.</div>
<div class="kf-item"><b>Excluded from flagging:</b> {fmt(len(p03b_ipd_capable))} hospitals with IPD-inherent
services (ICU, Surgery, Obstetrics, Critical Care) in their empanelment are considered legitimate IPD
facilities and are not flagged. The registry's lack of an explicit "IPD" category is a design gap,
not a fraud indicator for these hospitals.</div>
</div>""")

# ── PATTERN 4 ─────────────────────────────────────────────────────────────────
if p04a:
    H.append(f"""<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 4</div>
  <div class="ph-ctx">YoY Financial Trend<br/>(&gt;100% Annual Amount Growth)</div>
  <div class="ph-title">Year-over-Year Billing Spike by Hospital</div>
</div></div>
<p><b>Description:</b> Detects hospitals demonstrating a sudden <b>100%+ annual growth</b> in claim amounts 
without a corresponding growth in their registered patient base or empanelled capacity. A cliff-edge 
spike of this magnitude indicates a deliberate change in aggressive billing strategies rather than organic demographic growth.</p>
<p><b>Total Facilities Flagged:</b> <span style="color:#c0392b;font-weight:700">{fmt(len(p04a))}</span></p>
<div class="tc">Table 4.1 — Hospital YoY Billing Spike (Top 15)</div>
<table class="dt">
{th("Hospital","City","Prev Yr","Curr Yr","Prev Yr Amt","Curr Yr Amt","Claims Growth %")}
<tbody>""")
    for r in p04a[:15]:
        H.append(f"<tr><td><b>{safe(r.get('hospital_name',''))[:30]}</b></td>"
                 f"<td>{safe(r.get('city',''))}</td>"
                 f"<td>{safe(r.get('prev_year',''))}</td>"
                 f"<td>{safe(r.get('curr_year',''))}</td>"
                 f"<td>{cr(float(r.get('prev_claimed_lakh',0))*100000)}</td>"
                 f"<td><b>{cr(float(r.get('curr_claimed_lakh',0))*100000)}</b></td>"
                 f"<td>+{safe(r.get('yoy_claim_growth_pct','0'))}%</td></tr>")
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Amt Growth %:</b> Hospitals doubling their ECHS revenue in a single year must be 
audited. This often correlates with a new fraud ring operation, hiring of aggressive billing agents, or 
systematic upcoding of procedures.</div>
<div class="kf-item">Discrepancies where Amount Growth far exceeds Claims Growth indicate the hospital 
has started charging significantly more per patient (inflation of severity, unbundling).</div>
</div>""")

# ── PATTERN 5 ─────────────────────────────────────────────────────────────────
if p05b:
    H.append(f"""<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 5</div>
  <div class="ph-ctx">Type-3 Facilities<br/>(Extreme High-Value Claims &gt;₹1L)</div>
  <div class="ph-title">High-Value Claims at Low-Tier Facilities</div>
</div></div>
<p><b>Description:</b> Small or specialist-only hospitals (Type 3: Dental, Diagnostic, Polyclinics) 
billing individual claim amounts that exceed their clinical capabilities. A dental clinic billing 
₹50,000+ for a single admission is a strong indicator of fabricated bills or incorrect hospital classification.</p>
<p><b>Detection Thresholds Applied:</b> Flagged hospitals are Type-3 facilities where: (a) at least <b>3 individual claims each exceed ₹50,000</b>, and (b) any single claim reaches up to or beyond <b>₹1,00,000</b>. These limits reflect the maximum plausible billing capacity for a dental clinic or diagnostic lab.</p>
<p><b>Total Facilities Flagged:</b> <span style="color:#c0392b;font-weight:700">{fmt(len(p05b))}</span></p>
<div class="tc">Table 5.1 — Low-Tier Hospitals with High-Value Claims (Top 15)</div>
<table class="dt">
{th("Hospital","Type","City","High Val Claims","Max Single Claim","Total Claimed")}
<tbody>""")
    for r in p05b[:15]:
        H.append(f"<tr><td><b>{safe(r.get('hospital_name',''))[:30]}</b></td>"
                 f"<td>{safe(r.get('hosp_type_desc',''))[:15]}</td>"
                 f"<td>{safe(r.get('city',''))}</td>"
                 f"<td><b style='color:#c0392b'>{safe(r.get('high_val_claims','0'))}</b></td>"
                 f"<td>{cr(float(r.get('max_single_claim_lakh',0))*100000)}</td>"
                 f"<td><b>{cr(float(r.get('total_claimed_lakh',0))*100000)}</b></td></tr>")
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Max Single Claim:</b> The maximum amount billed for a single patient episode. 
For Type-3 facilities, claims exceeding ₹50,000 are extremely rare and highly anomalous.</div>
<div class="kf-item">Facilities flagged here must provide detailed clinical justification for these 
high-value bills, as their infrastructure typically does not support procedures of this cost magnitude.</div>
</div>""")

# ── CONSOLIDATED SUMMARY ────────────────────────────────────────────────
H.append(f"""<div class="pb">
<h1>Consolidated Summary</h1>
<p class="tc" style="margin-bottom:10px">All findings are based on structured database analysis and must be
corroborated with physical audit records before enforcement action is taken.</p>
<table class="dt">
{th("Pattern","Fraud Pattern","Cases Flagged","Exposure")}
<tbody>
<tr><td>1</td><td>Specialty Category Billing Fraud</td><td><b>{fmt(len(p01a))}</b></td><td>{cr(sum_exposure(p01a))}</td></tr>
<tr><td>2</td><td>NABH vs Non-NABH Divergence</td><td><b>{fmt(len(p02b))}</b></td><td>{cr(sum_exposure(p02b, 'claimed_lakh'))}</td></tr>
<tr><td>3</td><td>Out of Scope Empanelment</td><td><b>{fmt(p03b_flagged_total)}</b> ({fmt(len(p03b))} Critical + {fmt(len(p03b_opd_only))} High)</td><td>{cr(sum_exposure(p03b) + sum_exposure(p03b_opd_only))}</td></tr>
<tr><td>4</td><td>Year-over-Year Billing Spike</td><td><b>{fmt(len(p04a))}</b></td><td>{cr(sum_exposure(p04a, 'curr_claimed_lakh'))}</td></tr>
<tr><td>5</td><td>High-Value Claims at Low-Tier</td><td><b>{fmt(len(p05b))}</b></td><td>{cr(sum_exposure(p05b, 'total_claimed_lakh'))}</td></tr>
<tr style="background:#fdf0f0;font-weight:700"><td colspan="2"><b>TOTAL</b></td><td><b style="color:#c0392b">{fmt(total_hospitals_flagged)}</b></td><td><b>{cr(total_exposure)}</b></td></tr>
</tbody>
</table>

<p style="margin-top:16px;font-size:7.5pt;color:#555;text-align:center">
Prepared by IIT Kanpur — Data Analytics &amp; Fraud Intelligence Division | {today_str}<br/>
All findings are based on structured database analysis and must be corroborated with physical audit records before enforcement action.
</p>
</div>

</body></html>""")

# ── RENDER ────────────────────────────────────────────────────────────────────
full_html = "".join(H)
print("Generating PDF ...")
HTML(string=full_html, base_url=BASE).write_pdf(PDF_OUT)
print(f"✅ Saved → {PDF_OUT}")
print(f"Total exposure: {cr(total_exposure)}")
