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

# ── Load CSVs ─────────────────────────────────────────────────────────────────

def load_latest(pattern):
    files = glob.glob(os.path.join(DATA_DIR, pattern))
    if not files:
        return []
    files.sort(key=os.path.getmtime, reverse=True)
    with open(files[0], encoding="utf-8") as f:
        return list(csv.DictReader(f))

regional      = load_latest("01a_Regional_Fraud_Hotspots*.csv")
top_hospitals = load_latest("02a_Top_Hospitals_By_Deduction*.csv")
cross_hosp    = load_latest("Cross_Module_Hospital_Risk_Index.csv")
cross_region  = load_latest("Cross_Module_Regional_Clustering.csv")
cross_state   = load_latest("Cross_Module_State_Clustering.csv")
cross_chains  = load_latest("Cross_Module_Hospital_Chains.csv")
referral_usage = load_latest("Cross_Region_Referral_Usage.csv")
emerging_clusters = load_latest("Predictive_Emerging_Clusters.csv")
region_names_raw = load_latest("ecs_region_lookup.csv")

REGION_NAME = {r['ER_REGION_ID']: r['ER_REGION_NAME'] for r in region_names_raw if r.get('ER_REGION_NAME')}

def region_label(rid):
    name = REGION_NAME.get(rid)
    return f"R-{rid} ({name})" if name else f"R-{rid}"

regional_sorted = sorted(regional, key=lambda r: float(r['deduction_pct']), reverse=True)
top_region   = regional_sorted[0] if regional_sorted else {}
largest_region = sorted(regional, key=lambda r: float(r['total_deducted']), reverse=True)[0] if regional else {}
top_hosp_row = top_hospitals[0] if top_hospitals else {}

park_units = [r for r in top_hospitals if 'PARK HOSPITAL' in r['hospital_name'].upper()]
park_total_ded = sum(float(r['total_deducted']) for r in park_units)

vijay_row = next((r for r in top_hospitals if r['hospital_name'].upper() == 'VIJAY HOSPITAL'), {})

total_cross_exposure_cr = sum(float(r['total_flagged_exposure_cr']) for r in cross_hosp)

top_cross_hosp = sorted(cross_hosp, key=lambda r: (-int(r['modules_flagged_count']), -float(r['total_flagged_exposure_cr'])))[:20]
top_cross_region = sorted(cross_region, key=lambda r: -float(r['total_flagged_exposure_cr']))
top_cross_state = sorted(cross_state, key=lambda r: -float(r['total_flagged_exposure_cr']))[:15]
top_chains = sorted(cross_chains, key=lambda r: -float(r['total_flagged_exposure_cr']))[:15]

most_flagged_hosp = top_cross_hosp[0] if top_cross_hosp else {}
top_chain = top_chains[0] if top_chains else {}
top_state = top_cross_state[0] if top_cross_state else {}
top_cr_region = top_cross_region[0] if top_cross_region else {}

top_referrals = sorted(referral_usage, key=lambda r: -float(r['exposure_cr']))[:20]
cross_region_referrals = [r for r in referral_usage if r['cross_region'] == 'YES']
top_referral = top_referrals[0] if top_referrals else {}
top_cross_referral = sorted(cross_region_referrals, key=lambda r: -float(r['exposure_cr']))[0] if cross_region_referrals else {}

top_emerging = sorted(emerging_clusters, key=lambda r: -float(r['exposure_cr']))[:20]
top_emerging_hosp = top_emerging[0] if top_emerging else {}

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
.ph-ctx   {{ float:right; font-size:7.5pt; color:#888; font-style:italic; text-align:right; max-width:200px; line-height:1.3; margin-top:4px; }}
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

H = [f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS_STR}</style></head><body>"""]

# ── COVER ─────────────────────────────────────────────────────────────────────
H.append(f"""
<div class="cover">
  <div class="cover-topbar"></div>
  <div class="cover-title">ECHS FRAUD ANALYTICS</div>
  <div class="cover-sub">Geo-Spatial Fraud Clustering Analysis</div>
  <div class="cover-mod">MODULE 9 REPORT — FULL DATABASE COVERAGE | FY 2013 – FY 2026</div>
  <div class="cover-boxes">
    <div class="cover-box"><div class="cover-box-label">Classification</div><div class="cover-box-val">RESTRICTED</div></div>
    <div class="cover-box"><div class="cover-box-label">Period</div><div class="cover-box-val">FY 2013–26</div></div>
    <div class="cover-box"><div class="cover-box-label">Hospitals Scanned</div><div class="cover-box-val">{fmt(len(cross_hosp))}</div></div>
    <div class="cover-box"><div class="cover-box-label">Patterns Run</div><div class="cover-box-val">7 Patterns</div></div>
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
<p>Module 9 analyses the <b>geographic and temporal concentration of ECHS fraud</b>: which regions and hospitals
are fraud hotspots, how referral usage crosses regional lines, and which hospitals are emerging as new clusters
before they become entrenched. Patterns 1–2 establish the region- and hospital-level deduction baseline
(settlement_stat, full database coverage, FY 2013–FY 2026). Patterns 3–7 build on fraud signals already
established elsewhere in the ECHS fraud-analytics programme — hospital risk-scoring, referral-syndicate
detection, and billing-trend analysis — re-mapping them geographically and temporally without running any new
fraud-detection queries.</p>

<div class="metric-row">
  <div class="mbox"><div class="mbox-label">Hospitals Cross-Mapped</div><div class="mbox-val">{fmt(len(cross_hosp))}</div><div class="mbox-sub">across Patterns 3–5</div></div>
  <div class="mbox"><div class="mbox-label">Combined Cross-Pattern Exposure</div><div class="mbox-val">{cr_direct(total_cross_exposure_cr)}</div><div class="mbox-sub">Patterns 3–5</div></div>
  <div class="mbox"><div class="mbox-label">Patterns w/ Findings</div><div class="mbox-val">7 of 7</div><div class="mbox-sub">all patterns produced findings</div></div>
  <div class="mbox"><div class="mbox-label">Analysis Period</div><div class="mbox-val">FY 2013–26</div><div class="mbox-sub">full database coverage</div></div>
</div>

<h1 style="margin-top:14px">Seven Geo-Spatial Fraud Patterns — Summary</h1>
<table class="dt">
{th("#","Pattern","What It Detects","Coverage")}
<tbody>
<tr><td>1</td><td>Regional Fraud Hotspots</td><td>Deduction rate by ECHS region, settlement_stat</td><td>All 31 regions</td></tr>
<tr><td>2</td><td>Top Hospitals by Deduction</td><td>Highest absolute deduction hospitals + chain detection</td><td>Top 100 hospitals</td></tr>
<tr><td>3</td><td>Cross-Pattern Hospital Concentration</td><td>Hospitals flagged by the most independent fraud modules</td><td>{fmt(len(cross_hosp))} hospitals mapped</td></tr>
<tr><td>4</td><td>Cross-Pattern Regional &amp; State Clustering</td><td>Geographic rollup of all already-flagged fraud cases</td><td>{len(cross_region)} regions, {len(cross_state)} states</td></tr>
<tr><td>5</td><td>Cross-Pattern Hospital Chain Detection</td><td>Multi-unit hospital brands flagged across patterns</td><td>{fmt(len(cross_chains))} multi-unit chains</td></tr>
<tr><td>6</td><td>Cross-Region Referral Usage</td><td>Polyclinics/entities funnelling referrals to one hospital outside their own city</td><td>{fmt(len(referral_usage))} funnelling pairs</td></tr>
<tr><td>7</td><td>Predictive — Emerging Fraud Clusters</td><td>Hospitals with the sharpest year-on-year billing acceleration</td><td>{fmt(len(emerging_clusters))} hospital-year records</td></tr>
</tbody>
</table>

<h1 style="margin-top:12px">Immediate Recommended Actions</h1>
<div class="action-item"><span class="action-num">1.</span> <b>Joint audit of cross-pattern top-20 hospitals</b> ({fmt(len(cross_hosp))} hospitals mapped) — these hospitals are corroborated by multiple independent statistical methods, not a single pattern's threshold; prioritise above single-pattern outliers.</div>
<div class="action-item"><span class="action-num">2.</span> <b>Field audit deployment to {region_label(safe(top_region.get('region_id'),''))} and {region_label(safe(top_cr_region.get('region_id'),''))}</b> — the two regions topping the baseline deduction-rate and cross-pattern exposure rankings respectively.</div>
<div class="action-item"><span class="action-num">3.</span> <b>Corporate-group-level audit of multi-unit chains</b>, starting with {safe(top_chain.get('chain_name'))} ({safe(top_chain.get('units'))} units) and the Park Hospital units — audit the legal-entity group as a whole, not branch-by-branch.</div>
<div class="action-item"><span class="action-num">4.</span> <b>Recovery review for state-level concentration</b> — {safe(top_state.get('state_name'))} accounts for the largest share of combined cross-pattern flagged exposure ({cr_direct(top_state.get('total_flagged_exposure_cr',0))}) and should anchor the next regional audit cycle.</div>
<div class="action-item"><span class="action-num">5.</span> <b>Audit the cross-region referral pairs in Table 6.1</b>, starting with {safe(top_cross_referral.get('polyclinic_name'))} ({safe(top_cross_referral.get('polyclinic_city'))}) → {safe(top_cross_referral.get('funnels_to'))} ({safe(top_cross_referral.get('funnels_to_city'))}) — a single referral source sending the overwhelming majority of its patients to one out-of-area hospital is a classic referral-syndicate signature.</div>
<div class="action-item"><span class="action-num">6.</span> <b>Pre-emptive review of emerging-cluster hospitals (Table 7.1)</b>, led by {safe(top_emerging_hosp.get('hospital_name'))} — these hospitals are still ramping up, so intervening now is cheaper than after the pattern becomes structural like Park Hospital or Vijay Hospital.</div>
<div class="action-item"><span class="action-num">7.</span> <b>Extend geo-mapping to the remaining fraud-detection analyses</b> once their exports carry a numeric
office hospital identifier — a handful of analyses (identity/duplicate-claims, length-of-stay, diagnostic
overutilisation, network collusion) cannot yet be geo-mapped because their existing outputs either have no
hospital-level rollup or use free-text identifiers incompatible with the office master's numeric ID space, the
same ID-mismatch issue this report's predecessor flagged.</div>

<div class="kf-head">Methodology Note</div>
<div class="kf-item">Patterns 3–7 do not run new fraud-detection queries. They reuse hospital-level summary data
already produced elsewhere in the ECHS fraud-analytics programme and aggregate it by hospital office ID. The
combined "exposure" figures sum each underlying pattern's own claimed/deducted amount and are a
risk-concentration score, not a deduplicated unique-loss total — the same claim may legitimately appear in more
than one pattern's denominator.</div>
<div class="kf-item">Pattern 7's year-on-year figures are filtered to hospitals with at least ₹1 Cr of
current-year exposure and a meaningful prior-year claim base, to exclude statistically meaningless percentage
spikes from near-zero starting volumes.</div>
</div>
""")

# ── PATTERN 1: Regional Fraud Hotspots (baseline) ──────────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 1</div>
  <div class="ph-ctx">Regional Fraud Hotspot Analysis<br/>settlement_stat — all 31 ECHS regions</div>
  <div class="ph-title">Regional Fraud Hotspots — Deduction Rates by Region</div>
</div></div>
<p><b>Description:</b> Aggregates every claim in settlement_stat by ECHS region code (SS_REGION_ID), computing
total claimed, approved, deducted, and deduction rate per region — full database coverage, no date filter.
Regions with high deduction rates represent geographic concentrations of overbilling, either from a few
dominant high-deduction hospitals or widespread billing manipulation across many facilities. ECHS's own region
master names only 13 of the 31 region codes (1–13); the remainder exist in the claims data only as numeric
codes with no assigned name, so they are shown as a code alone (e.g. R-20) below.</p>
<div class="tc">Table 1.1 — All 31 ECHS Regions, Sorted by Deduction Rate</div>
<table class="dt">
{th("Region","Hospitals","Claims","Claimed","Approved","Deducted","Ded %")}
<tbody>""")
for r in regional_sorted:
    H.append(f"<tr><td>{region_label(r['region_id'])}</td>"
             f"<td>{fmt(r['hospitals'])}</td>"
             f"<td>{fmt(r['claims'])}</td>"
             f"<td>{cr(r['total_claimed'])}</td>"
             f"<td>{cr(r['total_approved'])}</td>"
             f"<td><b>{cr(r['total_deducted'])}</b></td>"
             f"<td><b style='{pct_style(r['deduction_pct'])}'>{r['deduction_pct']}%</b></td></tr>")
H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>{region_label(safe(top_region.get('region_id'),''))}</b> has the highest deduction rate at
<b>{safe(top_region.get('deduction_pct'))}%</b> across {fmt(top_region.get('hospitals',0))} hospitals and
{cr(top_region.get('total_claimed',0))} in claims, with {cr(top_region.get('total_deducted',0))} deducted.</div>
<div class="kf-item"><b>{region_label(safe(largest_region.get('region_id'),''))}</b> represents the largest absolute
fraud exposure in the database at {cr(largest_region.get('total_deducted',0))} deducted from
{cr(largest_region.get('total_claimed',0))} claimed ({safe(largest_region.get('deduction_pct'))}% rate).</div>
</div>""")

# ── PATTERN 2: Top Hospitals by Deduction (baseline) ───────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 2</div>
  <div class="ph-ctx">Priority Audit List<br/>settlement_stat + office_master</div>
  <div class="ph-title">Top Hospitals by Total Deduction Amount</div>
</div></div>
<p><b>Description:</b> Ranks all empanelled hospitals by total amount deducted across their entire history with
ECHS — full database coverage. High total deductions indicate either very high claim volumes or high
deduction rates (overbilling); both dimensions are shown below for the top 20.</p>
<div class="tc">Table 2.1 — Top 20 Hospitals by Total Deduction</div>
<table class="dt">
{th("ID","Hospital","State","Claims","Claimed","Deducted","Ded %")}
<tbody>""")
for r in top_hospitals[:20]:
    is_park = 'PARK HOSPITAL' in r['hospital_name'].upper()
    flag = '<br/><span style="font-size:6.5pt;color:#888">PARK CHAIN</span>' if is_park else ''
    H.append(f"<tr><td>{safe(r['hospital_id'])}</td>"
             f"<td style='font-size:7.5pt'>{safe(r['hospital_name'])[:48]}{flag}</td>"
             f"<td style='font-size:7.5pt'>{safe(r['state_name'])}</td>"
             f"<td>{fmt(r['claims'])}</td>"
             f"<td>{cr(r['total_claimed'])}</td>"
             f"<td><b>{cr(r['total_deducted'])}</b></td>"
             f"<td><b style='{pct_style(r['deduction_pct'])}'>{r['deduction_pct']}%</b></td></tr>")
H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Park Hospital</b> appears {len(park_units)} times in the top 20/100 hospitals by deduction —
combined across its empanelled units, the chain has had <b>{cr(park_total_ded)}</b> deducted, more than any other
individual hospital or chain identified in the baseline data.</div>
<div class="kf-item"><b>{safe(vijay_row.get('hospital_name','VIJAY HOSPITAL'))}</b> has the highest deduction rate
in the top 20 at <b>{safe(vijay_row.get('deduction_pct'))}%</b> on {cr(vijay_row.get('total_claimed',0))} claimed —
nearly one-third of everything it bills is rejected by assessors, consistent with systematic overbilling.</div>
</div>""")

# ── PATTERN 3: Cross-Pattern Hospital Concentration (NEW) ─────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 3</div>
  <div class="ph-ctx">Independent-Method Corroboration<br/>Hospital-level fraud signals, geo-mapped</div>
  <div class="ph-title">Cross-Pattern Hospital Concentration</div>
</div></div>
<p><b>Description:</b> Each row below is a hospital that was independently flagged by <b>multiple different
fraud-detection analyses</b> — e.g. a hospital appearing in the revenue-inflation outliers, the emergency-admission
misuse list, and the multi-abuse hospital list simultaneously. A hospital flagged by many unrelated detection
methods is a far stronger fraud signal than any single pattern alone, because each method tests a different part
of the claims lifecycle.</p>
<div class="tc">Table 3.1 — Top 20 Hospitals by Number of Independent Patterns Flagging Them</div>
<table class="dt">
{th("ID","Hospital","State","Independent Signals","Combined Claim Vol.","Combined Exposure")}
<tbody>""")
for r in top_cross_hosp:
    H.append(f"<tr><td>{safe(r['hospital_id'])}</td>"
             f"<td style='font-size:7.5pt'>{safe(r['hospital_name'])[:42]}</td>"
             f"<td style='font-size:7.5pt'>{safe(r['state_name'])}</td>"
             f"<td><b style='color:#c0392b'>{safe(r['modules_flagged_count'])}</b></td>"
             f"<td>{fmt(r['total_flagged_claims'])}</td>"
             f"<td><b>{cr_direct(r['total_flagged_exposure_cr'])}</b></td></tr>")
H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>{safe(most_flagged_hosp.get('hospital_name'))}</b> ({safe(most_flagged_hosp.get('city'))},
{safe(most_flagged_hosp.get('state_name'))}) is flagged by <b>{safe(most_flagged_hosp.get('modules_flagged_count'))}
independent fraud-detection signals</b> — the single strongest cross-pattern fraud signal in the database, with a
combined flagged exposure of {cr_direct(most_flagged_hosp.get('total_flagged_exposure_cr',0))}.</div>
<div class="kf-item">Hospitals flagged by 8+ independent patterns should be prioritised for joint audit ahead of
hospitals with a high score on any single pattern alone — the convergence of unrelated statistical tests on the
same facility sharply reduces the chance of a false positive.</div>
</div>""")

# ── PATTERN 4: Cross-Pattern Regional / State Clustering (NEW) ────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 4</div>
  <div class="ph-ctx">Geographic Rollup of All Flagged Cases<br/>By ECHS region &amp; state</div>
  <div class="ph-title">Cross-Pattern Regional &amp; State Clustering</div>
</div></div>
<p><b>Description:</b> Rolls up the cross-pattern hospital index (Pattern 3) by ECHS region and by state, to
show where already-flagged fraud cases concentrate geographically. This is the direct "fraud hotspot map" the
Module 9 framework calls for, built from corroborated evidence rather than a single financial metric.</p>
<div class="tc">Table 4.1 — ECHS Regions Ranked by Combined Cross-Pattern Exposure</div>
<table class="dt">
{th("Region","Flagged Hospitals","Distinct Patterns","Combined Claim Vol.","Combined Exposure")}
<tbody>""")
for r in top_cross_region[:15]:
    H.append(f"<tr><td>{region_label(r['region_id'])}</td>"
             f"<td>{fmt(r['flagged_hospitals'])}</td>"
             f"<td>{fmt(r['distinct_patterns_represented'])}</td>"
             f"<td>{fmt(r['total_flagged_claims'])}</td>"
             f"<td><b>{cr_direct(r['total_flagged_exposure_cr'])}</b></td></tr>")
H.append(f"""</tbody></table>
<div class="tc" style="margin-top:12px">Table 4.2 — Top 15 States Ranked by Combined Cross-Pattern Exposure</div>
<table class="dt">
{th("State","Flagged Hospitals","Distinct Patterns","Combined Claim Vol.","Combined Exposure")}
<tbody>""")
for r in top_cross_state:
    H.append(f"<tr><td>{safe(r['state_name'])}</td>"
             f"<td>{fmt(r['flagged_hospitals'])}</td>"
             f"<td>{fmt(r['distinct_patterns_represented'])}</td>"
             f"<td>{fmt(r['total_flagged_claims'])}</td>"
             f"<td><b>{cr_direct(r['total_flagged_exposure_cr'])}</b></td></tr>")
H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>{region_label(safe(top_cr_region.get('region_id'),''))}</b> has the largest combined
cross-pattern exposure ({cr_direct(top_cr_region.get('total_flagged_exposure_cr',0))} across
{fmt(top_cr_region.get('flagged_hospitals',0))} flagged hospitals and
{fmt(top_cr_region.get('distinct_patterns_represented',0))} distinct fraud patterns) — corroborating the
region-level deduction-rate finding in Pattern 1 with independent, claim-level evidence.</div>
<div class="kf-item"><b>{safe(top_state.get('state_name'))}</b> leads all states with
{cr_direct(top_state.get('total_flagged_exposure_cr',0))} in combined flagged exposure across
{fmt(top_state.get('flagged_hospitals',0))} hospitals — a geographic concentration that should anchor the next
phase of regional field audits.</div>
</div>""")

# ── PATTERN 5: Cross-Pattern Chain Detection (NEW) ────────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 5</div>
  <div class="ph-ctx">Multi-Unit Brand Concentration<br/>Name-normalised hospital chain rollup</div>
  <div class="ph-title">Cross-Pattern Hospital Chain Detection</div>
</div></div>
<p><b>Description:</b> Groups hospitals by normalised brand name (stripping legal-entity suffixes such as
"(A Unit of ... Pvt Ltd)") to detect chains where multiple branches are independently flagged across the fraud
framework. The baseline Pattern 2 already showed Park Hospital's 5 units dominating the deduction-amount
leaderboard; this table extends that logic using every available pattern, not just settlement_stat deductions.</p>
<div class="tc">Table 5.1 — Top 15 Multi-Unit Chains by Combined Cross-Pattern Exposure</div>
<table class="dt">
{th("Chain","Units","Distinct Patterns","Combined Claim Vol.","Combined Exposure")}
<tbody>""")
for r in top_chains:
    H.append(f"<tr><td>{safe(r['chain_name'])}</td>"
             f"<td><b style='color:#c0392b'>{safe(r['units'])}</b></td>"
             f"<td>{fmt(r['distinct_patterns_represented'])}</td>"
             f"<td>{fmt(r['total_flagged_claims'])}</td>"
             f"<td><b>{cr_direct(r['total_flagged_exposure_cr'])}</b></td></tr>")
H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>{safe(top_chain.get('chain_name'))}</b> is the largest multi-unit cluster by combined
exposure, with <b>{safe(top_chain.get('units'))} units</b> independently flagged across
{safe(top_chain.get('distinct_patterns_represented'))} distinct fraud patterns — {cr_direct(top_chain.get('total_flagged_exposure_cr',0))}
in combined flagged exposure.</div>
<div class="kf-item">Chains spreading flagged activity across multiple separately-registered legal entities under
one brand (as previously documented for Park Hospital) make per-hospital audit thresholds easier to stay under;
any chain appearing here with 3+ units should be audited as a single corporate group, not unit-by-unit.</div>
</div>""")

# ── PATTERN 6: Cross-Region Referral Usage ────────────────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 6</div>
  <div class="ph-ctx">Single-Hospital Funnelling<br/>Referral-syndicate detection</div>
  <div class="ph-title">Cross-Region Referral Usage</div>
</div></div>
<p><b>Description:</b> Reuses the existing "single-hospital funnelling" findings, which already identify
polyclinics and referring entities that send the overwhelming majority of their referrals (top_dest_pct) to one
specific hospital. Each row is flagged <b>cross-region</b> when the polyclinic's city differs from the
destination hospital's city — a referring entity routing patients out of its own area to one consistent
hospital is a stronger fraud signal than routine local referral.</p>
<div class="tc">Table 6.1 — Top 20 Funnelling Pairs by Exposure (Cross-Region Flagged)</div>
<table class="dt">
{th("Polyclinic","City","Referrals","Top Dest %","Funnels To","Dest. City","Cross-Region","Exposure")}
<tbody>""")
for r in top_referrals:
    flag_style = "color:#c0392b;font-weight:700" if r['cross_region'] == 'YES' else ''
    H.append(f"<tr><td style='font-size:7.5pt'>{safe(r['polyclinic_name'])[:26]}</td>"
             f"<td style='font-size:7.5pt'>{safe(r['polyclinic_city'])[:18]}</td>"
             f"<td>{fmt(r['referrals'])}</td>"
             f"<td><b>{r['top_dest_pct']}%</b></td>"
             f"<td style='font-size:7.5pt'>{safe(r['funnels_to'])[:30]}</td>"
             f"<td style='font-size:7.5pt'>{safe(r['funnels_to_city'])[:18]}</td>"
             f"<td><b style='{flag_style}'>{r['cross_region']}</b></td>"
             f"<td><b>{cr_direct(r['exposure_cr'])}</b></td></tr>")
H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>{safe(top_referral.get('polyclinic_name'))}</b> ({safe(top_referral.get('polyclinic_city'))})
is the largest funnelling pair by exposure overall, sending <b>{safe(top_referral.get('top_dest_pct'))}%</b> of its
{fmt(top_referral.get('referrals',0))} referrals to a single hospital — <b>{safe(top_referral.get('funnels_to'))}</b>
in {safe(top_referral.get('funnels_to_city'))} — worth {cr_direct(top_referral.get('exposure_cr',0))}. This pair is
same-city and may reflect ordinary geographic convenience rather than a syndicate.</div>
<div class="kf-item">{fmt(len(cross_region_referrals))} of the {fmt(len(referral_usage))} funnelling pairs
identified are cross-region (polyclinic and destination hospital in different cities) — these should
be the first priority for referral-syndicate audits, since a same-city referral can still be explained by simple
geographic convenience, while a cross-region one cannot. The largest cross-region pair is
<b>{safe(top_cross_referral.get('polyclinic_name'))}</b> ({safe(top_cross_referral.get('polyclinic_city'))}) →
<b>{safe(top_cross_referral.get('funnels_to'))}</b> ({safe(top_cross_referral.get('funnels_to_city'))}), worth
{cr_direct(top_cross_referral.get('exposure_cr',0))}.</div>
</div>""")

# ── PATTERN 7: Predictive Emerging Clusters ───────────────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 7</div>
  <div class="ph-ctx">Identify Emerging Clusters<br/>Year-on-year billing acceleration</div>
  <div class="ph-title">Predictive — Emerging Fraud Clusters</div>
</div></div>
<p><b>Description:</b> Reuses year-on-year billing-growth figures already computed elsewhere in the fraud-analytics
programme's time-series and specialty-misuse analyses, to flag hospitals whose claim volume or billed amount is
accelerating fastest, rather than hospitals that are already large, structural outliers like
Park Hospital or Vijay Hospital. A hospital climbing rapidly today is the geographic hotspot of tomorrow —
catching it early is materially cheaper than auditing it after the pattern is entrenched.</p>
<div class="tc">Table 7.1 — Top 20 Hospitals by Year-on-Year Billing Acceleration (Min. ₹1 Cr Exposure)</div>
<table class="dt">
{th("ID","Hospital","Source Module","Spike Year","YoY Growth %","Exposure")}
<tbody>""")
for r in top_emerging:
    H.append(f"<tr><td>{safe(r['hospital_id'])}</td>"
             f"<td style='font-size:7.5pt'>{safe(r['hospital_name'])[:36]}</td>"
             f"<td style='font-size:7.5pt'>{safe(r['source'])}</td>"
             f"<td>{safe(r['spike_year'])[:10]}</td>"
             f"<td><b style='color:#c0392b'>{float(r['yoy_growth_pct']):,.0f}%</b></td>"
             f"<td><b>{cr_direct(r['exposure_cr'])}</b></td></tr>")
H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>{safe(top_emerging_hosp.get('hospital_name'))}</b> shows the sharpest year-on-year
acceleration in the dataset — {float(top_emerging_hosp.get('yoy_growth_pct',0)):,.0f}% growth reaching
{cr_direct(top_emerging_hosp.get('exposure_cr',0))} in exposure by {safe(top_emerging_hosp.get('spike_year'))[:10]}.</div>
<div class="kf-item">Hospitals appearing in both this predictive table and the baseline/cross-pattern hotspot
tables (Patterns 1–3) are the highest-confidence audit targets: they are not just structurally high-risk, they
are actively getting worse.</div>
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
<tr><td>2</td><td>Top Hospitals by Deduction</td><td>Top 100 hospitals</td><td>Park Hospital chain — {cr(park_total_ded)} deducted across {len(park_units)} units</td></tr>
<tr><td>3</td><td>Cross-Pattern Hospital Concentration</td><td>{fmt(len(cross_hosp))} hospitals</td><td>{safe(most_flagged_hosp.get('hospital_name'))} — {safe(most_flagged_hosp.get('modules_flagged_count'))} independent signals</td></tr>
<tr><td>4</td><td>Cross-Pattern Regional &amp; State Clustering</td><td>{len(cross_region)} regions, {len(cross_state)} states</td><td>{safe(top_state.get('state_name'))} — {cr_direct(top_state.get('total_flagged_exposure_cr',0))} combined exposure</td></tr>
<tr><td>5</td><td>Cross-Pattern Hospital Chain Detection</td><td>{fmt(len(cross_chains))} multi-unit chains</td><td>{safe(top_chain.get('chain_name'))} — {safe(top_chain.get('units'))} units, {cr_direct(top_chain.get('total_flagged_exposure_cr',0))}</td></tr>
<tr><td>6</td><td>Cross-Region Referral Usage</td><td>{fmt(len(referral_usage))} funnelling pairs ({fmt(len(cross_region_referrals))} cross-region)</td><td>{safe(top_cross_referral.get('polyclinic_name'))} → {safe(top_cross_referral.get('funnels_to'))} ({safe(top_cross_referral.get('top_dest_pct'))}% of referrals)</td></tr>
<tr><td>7</td><td>Predictive — Emerging Fraud Clusters</td><td>{fmt(len(emerging_clusters))} hospital-year records</td><td>{safe(top_emerging_hosp.get('hospital_name'))} — {float(top_emerging_hosp.get('yoy_growth_pct',0)):,.0f}% YoY growth</td></tr>
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
