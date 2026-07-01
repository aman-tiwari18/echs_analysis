"""
ECHS Geo-Spatial Fraud Clustering — Module 9 Report
HTML + WeasyPrint approach matching FA-07/FA-08/Module-11 architecture.
Navy + Gold theme, IIT Kanpur branding, pattern headers with left gold bar.
"""

import os, csv, glob, time
from datetime import date

try:
    from weasyprint import HTML
except ImportError:
    print("ERROR: weasyprint not installed. Run: pip install weasyprint")
    exit(1)

BASE        = os.path.dirname(os.path.abspath(__file__))
DATA_DIR    = os.path.join(BASE, "data")
REPORTS_DIR = os.path.join(BASE, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

today_str = date.today().strftime("%-d %B %Y")
ts        = time.strftime("%Y%m%d_%H%M%S")
PDF_OUT   = os.path.join(REPORTS_DIR, f"ECHS_GeoSpatial_Fraud_Clustering_Report_{ts}.pdf")

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

def cr_direct(n):
    """Value already expressed in crore units."""
    try: return f"₹{float(n):,.2f} Cr"
    except: return str(n)

def safe(v, d="—"):
    return str(v).strip() if v and str(v).strip() not in ("", "nan", "None") else d

def pct_style(p):
    try: v = float(p)
    except: return ""
    if v >= 15: return 'color:#c0392b;font-weight:700'
    if v >= 10: return 'color:#d4680a;font-weight:600'
    return ''

def th(*cols):
    return "<thead><tr>" + "".join(f"<th>{c}</th>" for c in cols) + "</tr></thead>"

def quartile(sorted_vals, p):
    n = len(sorted_vals)
    idx = (n - 1) * p
    lo = int(idx); hi = min(lo + 1, n - 1); frac = idx - lo
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * frac

# ── Load CSVs ─────────────────────────────────────────────────────────────────

def load_latest(pattern):
    files = glob.glob(os.path.join(DATA_DIR, pattern))
    if not files:
        return []
    files.sort(key=os.path.getmtime, reverse=True)
    with open(files[0], encoding="utf-8") as f:
        return list(csv.DictReader(f))

regional       = load_latest("01a_Regional_Fraud_Hotspots*.csv")
cross_hosp     = load_latest("Cross_Module_Hospital_Risk_Index.csv")
cross_region   = load_latest("Cross_Module_Regional_Clustering.csv")
cross_state    = load_latest("Cross_Module_State_Clustering.csv")
cross_chains   = load_latest("Cross_Module_Hospital_Chains.csv")
referral_usage = load_latest("Cross_Region_Referral_Usage.csv")
cghs_region_master = load_latest("CGHS_Region_Master.csv")

REGION_NAME = {r['region_id']: r['region_name'] for r in cghs_region_master if r.get('region_name')}

def region_label(rid):
    name = REGION_NAME.get(rid)
    return f"R-{rid} ({name})" if name else f"R-{rid}"

region_flagged_lookup = {r['region_id']: r for r in cross_region}
cross_region_clean = [r for r in cross_region if r['region_id'] != 'UNKNOWN']

regional_sorted = sorted(regional, key=lambda r: float(r['deduction_pct']), reverse=True)
top_region     = regional_sorted[0] if regional_sorted else {}
largest_region = sorted(regional, key=lambda r: float(r['total_deducted']), reverse=True)[0] if regional else {}

total_cross_exposure_cr = sum(float(r['total_flagged_exposure_cr']) for r in cross_hosp)
hosp_10plus  = sum(1 for r in cross_hosp if int(r['modules_flagged_count']) >= 10)
hosp_15plus  = sum(1 for r in cross_hosp if int(r['modules_flagged_count']) >= 15)
total_hosp_in_system = sum(int(r['total_hospitals']) for r in cross_region_clean)

top_cross_hosp   = sorted(cross_hosp, key=lambda r: (-int(r['modules_flagged_count']), -float(r['total_flagged_exposure_cr'])))[:20]
top_cross_region = sorted(cross_region_clean, key=lambda r: -float(r['total_flagged_exposure_cr']))
top_cross_state  = sorted(cross_state, key=lambda r: -float(r['total_flagged_exposure_cr']))[:15]
top_chains       = sorted(cross_chains, key=lambda r: -float(r['total_flagged_exposure_cr']))[:15]

most_flagged_hosp = top_cross_hosp[0] if top_cross_hosp else {}
top_chain     = top_chains[0] if top_chains else {}
top_state     = top_cross_state[0] if top_cross_state else {}
top_cr_region = top_cross_region[0] if top_cross_region else {}

top_referrals = sorted(referral_usage, key=lambda r: -float(r['exposure_cr']))[:20]
cross_region_referrals = [r for r in referral_usage if r['cross_region'] == 'YES']
top_referral = top_referrals[0] if top_referrals else {}
top_cross_referral = sorted(cross_region_referrals, key=lambda r: -float(r['exposure_cr']))[0] if cross_region_referrals else {}

DETECTION_SIGNALS = [
    'Revenue Inflation Outliers', 'Procedure Upcoding', 'Doctor Referral Concentration',
    'Beneficiary Utilisation Outliers', 'Repeat Admission Outliers', 'Procedure Mislabelling',
    'Emergency Admission Misuse', 'Package/Item Billing Anomaly', 'Time-Series Billing Surge',
    'Hospital Specialty Misuse', 'High-Value Claim Risk Scoring', 'Pre-Authorization Deviation',
    'Claim Processing / Overbilling Pattern', 'Policy Abuse Pattern', 'Implausible Claim Volume',
    'Extreme Deduction Outliers', 'Same-Day Zero-Stay High-Value IPD',
    'Hospital Escalation (YoY Ratio Rise)', 'Room Entitlement Mismatch', 'Emergency Claim Flag Abuse',
]

# top 5 states by combined cross-pattern exposure, for the national-clustering narrative
top5_states = top_cross_state[:5]
top5_states_share = round(100 * sum(float(s['total_flagged_exposure_cr']) for s in top5_states)
                           / sum(float(s['total_flagged_exposure_cr']) for s in cross_state), 1)

# ── Tukey fence — referral concentration (Pattern 5) ──────────────────────────
# Applied to referral count (total referral transactions per polyclinic).
_ref_vals = sorted(int(float(r['referrals'])) for r in referral_usage)
ref_cnt_q1  = quartile(_ref_vals, .25)
ref_cnt_q3  = quartile(_ref_vals, .75)
ref_cnt_iqr = ref_cnt_q3 - ref_cnt_q1
ref_cnt_fence = ref_cnt_q3 + 1.5 * ref_cnt_iqr
referral_outliers = [r for r in referral_usage if int(float(r['referrals'])) > ref_cnt_fence]
referral_outliers_cross = [r for r in referral_outliers if r['cross_region'] == 'YES']

# ── CSS ───────────────────────────────────────────────────────────────────────

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
    @bottom-left  {{ content:""; }}
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
.ph-ctx   {{ float:right; font-size:7.5pt; color:#888; font-style:italic; text-align:right; max-width:200px; line-height:1.3; margin-top:4px; }}
.ph-title {{ font-size:14pt; font-weight:900; color:{NAV}; text-transform:uppercase; letter-spacing:0.5px; clear:right; }}

p   {{ margin-bottom:7px; text-align:justify; }}
b   {{ font-weight:700; }}
ul  {{ margin:4px 0 8px 16px; }}
li  {{ margin-bottom:3px; }}

.tc {{ font-size:7.5pt; color:#666; margin-bottom:4px; }}

.heatmap-img {{ display:block; width:140mm; margin:4px auto 0 auto; }}

table.dt {{ width:100%; border-collapse:collapse; margin:6px 0 14px 0; font-size:8pt; }}
table.dt thead tr {{ background:{NAV}; color:#fff; }}
table.dt thead th {{ padding:6px 7px; text-align:left; font-weight:700; }}
table.dt tbody tr:nth-child(even) {{ background:#f4f6f9; }}
table.dt tbody td {{ padding:5px 7px; border-bottom:1px solid #e5e5e5; vertical-align:top; }}
table.dt tbody tr {{ break-inside:avoid; page-break-inside:avoid; }}

.kf-head {{ font-size:11pt; font-weight:700; color:{NAV}; margin:14px 0 6px 0; }}
.kf-item {{ margin-bottom:7px; padding-left:8px; border-left:3px solid {GOLD}; font-size:8.5pt; line-height:1.5; }}

.action-item {{ margin-bottom:7px; font-size:8.5pt; }}
.action-num  {{ font-weight:800; color:{NAV}; }}
"""

# ── BUILD HTML ────────────────────────────────────────────────────────────────

H = [f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS_STR}</style></head><body>"""]

# ── COVER ─────────────────────────────────────────────────────────────────────
H.append(f"""
<div class="cover">
  <div class="cover-topbar"></div>
  <div class="cover-title">ECHS FRAUD ANALYTICS</div>
  <div class="cover-sub">Geo-Spatial Fraud Clustering Analysis</div>
  <div class="cover-mod">MODULE 9 REPORT — FY 2021–2026 EDITION (LAST 5 YEARS)</div>
  <div class="cover-boxes">
    <div class="cover-box"><div class="cover-box-label">Classification</div><div class="cover-box-val">RESTRICTED</div></div>
    <div class="cover-box"><div class="cover-box-label">Period</div><div class="cover-box-val">FY 2021–26</div></div>
    <div class="cover-box"><div class="cover-box-label">Hospitals Scanned</div><div class="cover-box-val">{fmt(len(cross_hosp))}</div></div>
    <div class="cover-box"><div class="cover-box-label">Patterns Run</div><div class="cover-box-val">5 Patterns</div></div>
    <div class="cover-box"><div class="cover-box-label">Peak Deduction</div><div class="cover-box-val">{safe(top_region.get('deduction_pct'))}%</div></div>
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
<p>This report analyses the <b>geographic concentration of ECHS fraud across India</b>, organised by ECHS's own
regional/state geography: which regions and states are fraud hotspots, how concentrated hospital chains and
referral relationships are, and where flagged claim activity clusters nationally. Pattern 1 establishes the
region-level deduction baseline (settlement_stat, last 5 financial years, FY 2021-22 to FY 2025-26). Patterns
2–5 cross-reference {len(DETECTION_SIGNALS)} named fraud-detection signals against the full ECHS geography,
mapping hospital-level findings to regions and states. The
headline finding: ECHS fraud is not spread evenly across the country —
<b>{", ".join(s['state_name'] for s in top5_states)} account for {top5_states_share}% of all cross-pattern
flagged exposure nationally</b> (Pattern 3).</p>

<div class="metric-row">
  <div class="mbox"><div class="mbox-label">Hospitals with ≥10 Signals</div><div class="mbox-val" style="color:#e74c3c">{fmt(hosp_10plus)}</div><div class="mbox-sub">high-confidence cases of {fmt(len(cross_hosp))} touched</div></div>
  <div class="mbox"><div class="mbox-label">Combined Exposure</div><div class="mbox-val">{cr_direct(total_cross_exposure_cr)}</div><div class="mbox-sub">estimated financial risk</div></div>
  <div class="mbox"><div class="mbox-label">Fraud Patterns</div><div class="mbox-val">5</div><div class="mbox-sub">all with findings</div></div>
  <div class="mbox"><div class="mbox-label">National Cluster Share</div><div class="mbox-val">{top5_states_share}%</div><div class="mbox-sub">top 5 states of {fmt(len(cross_state))}</div></div>
</div>

<h1 style="margin-top:14px">Five Geo-Spatial Fraud Patterns — Summary</h1>
<table class="dt">
{th("#","Pattern","What It Detects","Flagged / Analysed")}
<tbody>
<tr><td>1</td><td>Regional Fraud Hotspots</td><td>Deduction rate and total claims by ECHS region (settlement baseline)</td><td>31 regions — highest {safe(top_region.get('deduction_pct'))}% deduction</td></tr>
<tr><td>2</td><td>Cross-Pattern Hospital Concentration</td><td>{len(DETECTION_SIGNALS)} named fraud-detection signals — hospitals triggering ≥10 signals are high-priority</td><td>{fmt(hosp_10plus)} hospitals ≥10 signals; {fmt(len(cross_hosp))} touched by ≥1</td></tr>
<tr><td>3</td><td>Cross-Pattern Regional &amp; State Clustering</td><td>Geographic rollup of flagged cases vs. total hospitals and claims</td><td>31 regions, {len(cross_state)} states — top 5 = {top5_states_share}% of exposure</td></tr>
<tr><td>4</td><td>Cross-Pattern Hospital Chain Detection</td><td>Multi-unit hospital brands — total vs. flagged units per chain</td><td>{fmt(len(cross_chains))} chains — {safe(top_chain.get('flagged_units'))}/{safe(top_chain.get('total_units'))} flagged in top chain</td></tr>
<tr><td>5</td><td>Cross-Region Referral Usage</td><td>Single-hospital referral funnelling — Tukey-fence outliers by exposure</td><td>{fmt(len(referral_outliers))} statistical outliers of {fmt(len(referral_usage))} pairs</td></tr>
</tbody>
</table>

<h1 style="margin-top:12px">Immediate Recommended Actions</h1>
<div class="action-item"><span class="action-num">1.</span> <b>Joint audit of hospitals triggering ≥10 of the {len(DETECTION_SIGNALS)} named fraud signals</b> ({fmt(hosp_10plus)} hospitals) — these are corroborated by multiple independent statistical methods, not a single pattern's threshold; prioritise above single-signal outliers.</div>
<div class="action-item"><span class="action-num">2.</span> <b>Field audit deployment to {region_label(safe(top_region.get('region_id'),''))} and {region_label(safe(top_cr_region.get('region_id'),''))}</b> — the two regions topping the baseline deduction-rate and cross-pattern exposure rankings respectively.</div>
<div class="action-item"><span class="action-num">3.</span> <b>Corporate-group-level audit of multi-unit chains</b>, starting with {safe(top_chain.get('chain_name'))} ({safe(top_chain.get('flagged_units'))} of {safe(top_chain.get('total_units'))} units flagged) — audit the legal-entity group as a whole, not branch-by-branch.</div>
<div class="action-item"><span class="action-num">4.</span> <b>Recovery review for state-level concentration</b> — {safe(top_state.get('state_name'))} accounts for the largest share of combined cross-pattern flagged exposure ({cr_direct(top_state.get('total_flagged_exposure_cr',0))}) and should anchor the next regional audit cycle.</div>
<div class="action-item"><span class="action-num">5.</span> <b>Audit the {fmt(len(referral_outliers))} referral pairs exceeding the Tukey-fence referral-count threshold</b> ({fmt(int(ref_cnt_fence))} referrals; Table 5.1), starting with {safe(top_cross_referral.get('polyclinic_name'))} ({safe(top_cross_referral.get('polyclinic_city'))}) → {safe(top_cross_referral.get('funnels_to'))} ({safe(top_cross_referral.get('funnels_to_city'))}) — a single referral source sending the overwhelming majority of its patients to one out-of-area hospital is a classic referral-syndicate signature.</div>
<div class="action-item"><span class="action-num">6.</span> <b>Extend geo-mapping to the remaining fraud-detection analyses</b> once their exports carry a numeric
office hospital identifier — a handful of analyses (identity/duplicate-claims, length-of-stay, diagnostic
overutilisation, network collusion) cannot yet be geo-mapped because their existing outputs either have no
hospital-level rollup or use free-text identifiers incompatible with the office master's numeric ID space, the
same ID-mismatch issue this report's predecessor flagged.</div>
</div>
""")

# ── PATTERN 1: Regional Fraud Hotspots (baseline) ──────────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 1</div>
  <div class="ph-ctx">Regional Fraud Hotspot Analysis<br/>settlement_stat — all 31 ECHS regions, last 5 years</div>
  <div class="ph-title">Regional Fraud Hotspots</div>
</div></div>
<p><b>Description:</b> Aggregates claims in settlement_stat by ECHS region code (SS_REGION_ID) — last 5
financial years (FY 2021-22 to FY 2025-26). Shows the financial baseline for each ECHS region:
total settlement volume, claimed and approved amounts, and the deduction rate (Approved ÷ Claimed). Regions
with high deduction rates signal systematic over-billing in that geography. SS_REGION_ID is the CGHS
Region/City code space, annotated with the matching CGHS region name below.</p>
<div class="tc">Table 1.1 — All 31 ECHS Regions, Sorted by Deduction Rate</div>
<table class="dt">
{th("Region","Hospitals","Total Claims","Claimed","Approved","Ded %")}
<tbody>""")
for r in regional_sorted:
    H.append(f"<tr><td>{region_label(r['region_id'])}</td>"
             f"<td>{fmt(r['hospitals'])}</td>"
             f"<td>{fmt(r['claims'])}</td>"
             f"<td>{cr(r['total_claimed'])}</td>"
             f"<td>{cr(r['total_approved'])}</td>"
             f"<td><b style='{pct_style(r['deduction_pct'])}'>{r['deduction_pct']}%</b></td></tr>")
H.append(f"""</tbody></table>
<div class="tc" style="margin-top:14px">Figure 1.1 — Regional Claim-Volume Heatmap, All India (Last 5 FYs)</div>
<img class="heatmap-img" src="data/india_region_heatmap.png"/>
<p class="tc" style="text-align:center;margin-top:2px">Each bubble is one <b>CGHS Region</b> — the city-based
location/rate-region classification ECHS's own claims data uses internally (e.g. R-9 = the Jalandhar region;
see the CGHS Region Master for the full list). ECHS itself is headquartered in New Delhi and administers all
31 regions nationally; CGHS naming is simply the geographic key the underlying claims table uses. Bubble size
and colour both scale with claim count, in Lakh — darker/larger = higher claim volume passing through that
region. The map shows India's full national boundary, including Jammu &amp; Kashmir, Ladakh and Aksai Chin,
per India's official territorial extent.</p>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>{region_label(safe(top_region.get('region_id'),''))}</b> has the highest deduction rate at
<b>{safe(top_region.get('deduction_pct'))}%</b> — {cr(top_region.get('total_claimed',0))} claimed vs.
{cr(top_region.get('total_approved',0))} approved across {fmt(top_region.get('hospitals',0))} hospitals and
{fmt(top_region.get('claims',0))} total claims.</div>
<div class="kf-item"><b>{region_label(safe(largest_region.get('region_id'),''))}</b> has the largest absolute
deduction — {cr(largest_region.get('total_deducted',0))} deducted from {cr(largest_region.get('total_claimed',0))} claimed
({safe(largest_region.get('deduction_pct'))}% rate) across {fmt(largest_region.get('hospitals',0))} hospitals.</div>
</div>""")

# ── PATTERN 2: Cross-Pattern Hospital Concentration ───────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 2</div>
  <div class="ph-ctx">Independent-Method Corroboration<br/>Hospital-level fraud signals, geo-mapped</div>
  <div class="ph-title">Cross-Pattern Hospital Concentration</div>
</div></div>
<p><b>Description:</b> Each row is a hospital showing its <b>Total Claims</b> (real settlement volume, last 5
FYs), how many of the {len(DETECTION_SIGNALS)} named fraud-detection signals it triggered, and its
<b>Combined Exposure</b> (total flagged amount in ₹ Cr). Across all {len(DETECTION_SIGNALS)} signals,
<b>{fmt(len(cross_hosp))} unique hospitals</b> were touched by ≥1 signal; of these,
<b>{fmt(hosp_10plus)}</b> trigger ≥10 signals and <b>{fmt(hosp_15plus)}</b> trigger ≥15 — the higher the
signal count, the stronger the corroboration. The signals used are: {", ".join(DETECTION_SIGNALS)}.
Table 2.2 names exactly which signals fired for each top hospital.</p>
<div class="tc">Table 2.1 — Top 20 Hospitals by Number of Distinct Signals Triggered</div>
<table class="dt">
{th("ID","Hospital","State","Signals Triggered","Total Claims","Combined Exposure")}
<tbody>""")
for r in top_cross_hosp:
    H.append(f"<tr><td>{safe(r['hospital_id'])}</td>"
             f"<td style='font-size:7.5pt'>{safe(r['hospital_name'])[:36]}</td>"
             f"<td style='font-size:7.5pt'>{safe(r['state_name'])}</td>"
             f"<td><b style='color:#c0392b'>{safe(r['modules_flagged_count'])} / {len(DETECTION_SIGNALS)}</b></td>"
             f"<td>{fmt(r.get('total_claims_baseline',0))}</td>"
             f"<td><b>{cr_direct(r['total_flagged_exposure_cr'])}</b></td></tr>")
H.append(f"""</tbody></table>
<div class="tc" style="margin-top:12px">Table 2.2 — Which Signals Fired (Top 10 Hospitals)</div>
<table class="dt">
{th("Hospital","Signals Triggered (Named)")}
<tbody>""")
for r in top_cross_hosp[:10]:
    signals = safe(r.get('modules_flagged_list', '')).replace(' | ', ', ')
    H.append(f"<tr><td style='font-size:7.5pt;white-space:nowrap'>{safe(r['hospital_name'])[:30]}</td>"
             f"<td style='font-size:7.5pt'>{signals}</td></tr>")
H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>{safe(most_flagged_hosp.get('hospital_name'))}</b> ({safe(most_flagged_hosp.get('city'))},
{safe(most_flagged_hosp.get('state_name'))}) is flagged by <b>{safe(most_flagged_hosp.get('modules_flagged_count'))}
of the {len(DETECTION_SIGNALS)} named signals</b> (see Table 2.2) — {fmt(most_flagged_hosp.get('total_claims_baseline',0))} total claims
handled, combined flagged exposure of {cr_direct(most_flagged_hosp.get('total_flagged_exposure_cr',0))}.</div>
<div class="kf-item">Hospitals triggering 10+ of the {len(DETECTION_SIGNALS)} named signals should be prioritised for joint audit ahead
of hospitals with a high score on any single signal alone — the convergence of unrelated statistical tests on
the same facility sharply reduces the chance of a false positive.</div>
</div>""")

# ── PATTERN 3: Cross-Pattern Regional / State Clustering ──────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 3</div>
  <div class="ph-ctx">Geographic Rollup of All Flagged Cases<br/>By ECHS region &amp; state</div>
  <div class="ph-title">Cross-Pattern Regional &amp; State Clustering</div>
</div></div>
<p><b>Description:</b> Rolls up the cross-pattern hospital index by ECHS region and by state, to show where
flagged hospitals concentrate geographically. All <b>{fmt(len(cross_region_clean))} of 31 ECHS regions</b>
and <b>{fmt(len(cross_state))} states</b> have at least one flagged hospital; the total flagged hospital
count across all regions is <b>{fmt(sum(int(r['flagged_hospitals']) for r in cross_region_clean))}</b>
(out of {fmt(total_hosp_in_system)} empanelled). <b>Flagged Hospitals</b> is the subset triggering at least
one of the {len(DETECTION_SIGNALS)} named signals; <b>Distinct Signals</b> is how many of those
{len(DETECTION_SIGNALS)} independent methods flagged activity in that geography;
<b>Combined Exposure</b> is the total flagged amount in ₹ Cr.</p>
<div class="tc">Table 3.1 — ECHS Regions Ranked by Combined Cross-Pattern Exposure</div>
<table class="dt">
{th("Region","Total Hospitals","Flagged Hospitals","Distinct Signals","Total Claims","Combined Exposure")}
<tbody>""")
for r in top_cross_region[:15]:
    H.append(f"<tr><td>{region_label(r['region_id'])}</td>"
             f"<td>{fmt(r.get('total_hospitals',0))}</td>"
             f"<td>{fmt(r['flagged_hospitals'])}</td>"
             f"<td>{fmt(r['distinct_patterns_represented'])} / {len(DETECTION_SIGNALS)}</td>"
             f"<td>{fmt(r.get('total_claims_baseline',0))}</td>"
             f"<td><b>{cr_direct(r['total_flagged_exposure_cr'])}</b></td></tr>")
H.append(f"""</tbody></table>
<div class="tc" style="margin-top:12px">Table 3.2 — Top 15 States Ranked by Combined Cross-Pattern Exposure</div>
<table class="dt">
{th("State","Total Hospitals","Flagged Hospitals","Distinct Signals","Total Claims","Combined Exposure")}
<tbody>""")
for r in top_cross_state:
    H.append(f"<tr><td>{safe(r['state_name'])}</td>"
             f"<td>{fmt(r.get('total_hospitals',0))}</td>"
             f"<td>{fmt(r['flagged_hospitals'])}</td>"
             f"<td>{fmt(r['distinct_patterns_represented'])} / {len(DETECTION_SIGNALS)}</td>"
             f"<td>{fmt(r.get('total_claims_baseline',0))}</td>"
             f"<td><b>{cr_direct(r['total_flagged_exposure_cr'])}</b></td></tr>")
H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>National cluster belt:</b> {", ".join(s['state_name'] for s in top5_states)} —
the top 5 states by combined cross-pattern exposure — together account for <b>{top5_states_share}%</b> of all
flagged exposure nationally, out of {fmt(len(cross_state))} states with any flagged hospitals. ECHS fraud is not
spread evenly across India; it is heavily concentrated in this north/north-west belt.</div>
<div class="kf-item"><b>{region_label(safe(top_cr_region.get('region_id'),''))}</b> has the largest combined
cross-pattern exposure ({cr_direct(top_cr_region.get('total_flagged_exposure_cr',0))} across
{fmt(top_cr_region.get('flagged_hospitals',0))} of its {fmt(top_cr_region.get('total_hospitals',0))} hospitals
flagged, on {fmt(top_cr_region.get('distinct_patterns_represented',0))} of the {len(DETECTION_SIGNALS)} named
signals) — corroborating the region-level deduction-rate finding in Pattern 1 with independent, claim-level
evidence.</div>
<div class="kf-item"><b>{safe(top_state.get('state_name'))}</b> leads all states with
{cr_direct(top_state.get('total_flagged_exposure_cr',0))} in combined flagged exposure across
{fmt(top_state.get('flagged_hospitals',0))} of its {fmt(top_state.get('total_hospitals',0))} hospitals — a
geographic concentration that should anchor the next phase of regional field audits.</div>
</div>""")

# ── PATTERN 4: Cross-Pattern Hospital Chain Detection ─────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 4</div>
  <div class="ph-ctx">Multi-Unit Brand Concentration<br/>Name-normalised hospital chain rollup</div>
  <div class="ph-title">Cross-Pattern Hospital Chain Detection</div>
</div></div>
<p><b>Description:</b> Groups hospitals by normalised brand name (stripping legal-entity suffixes such as
"(A Unit of ... Pvt Ltd)") to detect chains where multiple branches are independently flagged.
This analysis identified <b>{fmt(len(cross_chains))} multi-unit chains</b>; across them,
<b>{fmt(sum(int(r.get('flagged_units',0)) for r in cross_chains))} of {fmt(sum(int(r.get('total_units',0)) for r in cross_chains))}</b>
total chain units are flagged by at least one signal. <b>Total Units</b> is every empanelled hospital
nationally matching that brand; <b>Flagged Units</b> is the flagged subset — a chain where most or all
units are flagged is a stronger signature of deliberate, group-wide structuring than a single outlier branch.
The top 15 chains by combined exposure are shown below.</p>
<div class="tc">Table 4.1 — Top 15 Multi-Unit Chains by Combined Cross-Pattern Exposure</div>
<table class="dt">
{th("Chain","Total Units","Flagged Units","Distinct Signals","Combined Exposure")}
<tbody>""")
for r in top_chains:
    H.append(f"<tr><td>{safe(r['chain_name'])}</td>"
             f"<td>{fmt(r.get('total_units',0))}</td>"
             f"<td><b style='color:#c0392b'>{fmt(r.get('flagged_units',0))}</b></td>"
             f"<td>{fmt(r['distinct_patterns_represented'])} / {len(DETECTION_SIGNALS)}</td>"
             f"<td><b>{cr_direct(r['total_flagged_exposure_cr'])}</b></td></tr>")
H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>{safe(top_chain.get('chain_name'))}</b> is the largest multi-unit cluster by combined
exposure: <b>{safe(top_chain.get('flagged_units'))} of its {safe(top_chain.get('total_units'))} units</b> nationally
are independently flagged, across {safe(top_chain.get('distinct_patterns_represented'))} of the {len(DETECTION_SIGNALS)}
named signals — {cr_direct(top_chain.get('total_flagged_exposure_cr',0))} in combined flagged exposure.</div>
<div class="kf-item">Chains where Flagged Units is close to Total Units (i.e. nearly every branch is flagged,
not just one outlier) should be audited as a single corporate group rather than unit-by-unit — spreading
activity across separately-registered legal entities under one brand makes per-hospital audit thresholds
easier to stay under.</div>
</div>""")

# ── PATTERN 5: Cross-Region Referral Usage ────────────────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 5</div>
  <div class="ph-ctx">Single-Hospital Funnelling<br/>Referral-syndicate detection, Tukey-fenced</div>
  <div class="ph-title">Cross-Region Referral Usage</div>
</div></div>
<p><b>Description:</b> Identifies polyclinics and referring entities that funnel most of their referrals to a single hospital.
<b>Referrals</b> is the total count of referral transactions issued by that polyclinic.
<b>Top Dest %</b> is the share of those referrals directed to its single most-favoured destination hospital
(e.g. 80% means 8 in 10 referred patients all end up at the same hospital) — the higher this number,
the more it looks like a steered pipeline rather than routine clinical choice. Each row is flagged
<b>cross-region</b> when the polyclinic's city differs from the destination hospital's city.
This analysis covers <b>{fmt(len(referral_usage))}</b> funnelling pairs;
<b>{fmt(len(referral_outliers))}</b> are statistically extreme by referral volume and <b>{fmt(len(cross_region_referrals))}</b> are cross-region.</p>

<p><b>Statistical threshold (Tukey fence):</b> Applied to <b>referral count</b> across all {fmt(len(referral_usage))} pairs —
Q3 = {fmt(int(ref_cnt_q3))} referrals, IQR = {fmt(int(ref_cnt_iqr))} referrals,
fence = <b>{ref_cnt_fence:.4f} referrals</b>.
The <b>{fmt(len(referral_outliers))} pairs</b> exceeding this threshold are statistically extreme in referral volume and are highlighted below.</p>

<div class="tc">Table 5.1 — Top 20 Funnelling Pairs by Exposure (Tukey-Fence Outliers Marked)</div>
<table class="dt">
{th("Polyclinic","City","Referrals","Top Dest %","Funnels To","Dest. City","Cross-Region","Exposure")}
<tbody>""")
for r in top_referrals:
    flag_style = "color:#c0392b;font-weight:700" if r['cross_region'] == 'YES' else ''
    is_outlier = int(float(r['referrals'])) > ref_cnt_fence
    exp_style = "font-weight:700"
    ref_style = "color:#c0392b;font-weight:700" if is_outlier else "font-weight:700"
    H.append(f"<tr><td style='font-size:7.5pt'>{safe(r['polyclinic_name'])[:26]}</td>"
             f"<td style='font-size:7.5pt'>{safe(r['polyclinic_city'])[:18]}</td>"
             f"<td><b style='{ref_style}'>{fmt(r['referrals'])}</b></td>"
             f"<td><b>{r['top_dest_pct']}%</b></td>"
             f"<td style='font-size:7.5pt'>{safe(r['funnels_to'])[:30]}</td>"
             f"<td style='font-size:7.5pt'>{safe(r['funnels_to_city'])[:18]}</td>"
             f"<td><b style='{flag_style}'>{r['cross_region']}</b></td>"
             f"<td><b style='{exp_style}'>{cr_direct(r['exposure_cr'])}</b></td></tr>")
H.append(f"""</tbody></table>
<div class="tc">Highlighted red = exceeds the Tukey-fence referral threshold of {ref_cnt_fence:.4f} referrals (statistical outlier)</div>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>{fmt(len(referral_outliers))} funnelling pairs</b> exceed the Tukey-fence referral
threshold of {fmt(int(ref_cnt_fence))} referrals, of which <b>{fmt(len(referral_outliers_cross))}</b> are also cross-region —
these are the highest-confidence referral-syndicate candidates in the dataset, combining statistical extremity
with a geography that rules out routine convenience.</div>
<div class="kf-item">{fmt(len(cross_region_referrals))} of the {fmt(len(referral_usage))} funnelling pairs
overall are cross-region (polyclinic and destination hospital in different cities). The largest cross-region
pair is <b>{safe(top_cross_referral.get('polyclinic_name'))}</b> ({safe(top_cross_referral.get('polyclinic_city'))}) →
<b>{safe(top_cross_referral.get('funnels_to'))}</b> ({safe(top_cross_referral.get('funnels_to_city'))}), worth
{cr_direct(top_cross_referral.get('exposure_cr',0))}.</div>
</div>""")

# ── CONSOLIDATED SUMMARY ────────────────────────────────────────────────
H.append(f"""
<div class="pb">
<h1>Consolidated Summary</h1>
<p class="tc" style="margin-bottom:10px">All findings are based on structured database analysis and must be
corroborated with physical audit records before enforcement action is taken.</p>
<table class="dt">
{th("#","Pattern","Coverage","Headline Finding")}
<tbody>
<tr><td>1</td><td>Regional Fraud Hotspots</td><td>31 regions</td><td>{region_label(safe(top_region.get('region_id'),''))} — {safe(top_region.get('deduction_pct'))}% deduction</td></tr>
<tr><td>2</td><td>Cross-Pattern Hospital Concentration</td><td>{fmt(len(cross_hosp))} hospitals</td><td>{safe(most_flagged_hosp.get('hospital_name'))} — {safe(most_flagged_hosp.get('modules_flagged_count'))} of {len(DETECTION_SIGNALS)} named signals</td></tr>
<tr><td>3</td><td>Cross-Pattern Regional &amp; State Clustering</td><td>31 regions, {len(cross_state)} states</td><td>{safe(top_state.get('state_name'))} — {cr_direct(top_state.get('total_flagged_exposure_cr',0))} combined exposure</td></tr>
<tr><td>4</td><td>Cross-Pattern Hospital Chain Detection</td><td>{fmt(len(cross_chains))} multi-unit chains</td><td>{safe(top_chain.get('chain_name'))} — {safe(top_chain.get('flagged_units'))}/{safe(top_chain.get('total_units'))} units flagged</td></tr>
<tr><td>5</td><td>Cross-Region Referral Usage</td><td>{fmt(len(referral_usage))} funnelling pairs ({fmt(len(referral_outliers))} Tukey outliers)</td><td>{safe(top_cross_referral.get('polyclinic_name'))} → {safe(top_cross_referral.get('funnels_to'))} ({safe(top_cross_referral.get('top_dest_pct'))}% of referrals)</td></tr>
</tbody>
</table>

<p style="margin-top:16px;font-size:7.5pt;color:#555;text-align:center">
Prepared by IIT Kanpur — Data Analytics &amp; Fraud Intelligence Division | {today_str}<br/>
All findings are based on structured database analysis and must be corroborated with physical audit records before enforcement action.
</p>
</div>

</body></html>""")

# ── RENDER ────────────────────────────────────────────────────────────────────
full_html = "\n".join(H)
print("Generating PDF ...")
HTML(string=full_html, base_url=BASE).write_pdf(PDF_OUT)
print(f"Saved -> {PDF_OUT}")
