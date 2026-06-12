import os, time
from datetime import date

try:
    from weasyprint import HTML, CSS
except ImportError:
    print("ERROR: weasyprint not installed. Run: pip install weasyprint")
    exit(1)

BASE = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(BASE, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

today_str = date.today().strftime("%-d %B %Y")
ts = time.strftime("%Y%m%d_%H%M%S")
PDF_OUT = os.path.join(REPORTS_DIR, f"ECHS_Time_Series_Surge_Report_{ts}.pdf")

NAV = "#1a2744"
GOLD = "#c9a84c"

# Helpers
def fmt(n):
    try: return f"{int(float(n)):,}"
    except: return str(n)

# Hardcoded data from 10main2.txt
p1_data = [
    ["FORTIS HOSPITAL LTD - JAIPUR", "2025", "1", "2,596", "1,778", "68.49%", "₹ 94,565,265", "₹ 44,672,603.55"],
    ["SMSG MULTISPECIALITY HOSPITAL", "2025", "2", "246", "172", "69.92%", "₹ 37,829,018", "₹ 23,209,092.18"],
    ["R P ARORA MEDICITY", "2023", "4", "412", "378", "91.75%", "₹ 35,740,258", "₹ 21,809,210.95"],
    ["KONARC MULTISPECIALITY HOSPITAL", "2023", "4", "210", "147", "70.00%", "₹ 29,416,063", "₹ 18,620,120.03"],
    ["TATA MEMORIAL HOSPITAL, PAREL, MUMBAI", "2023", "2", "343", "232", "67.64%", "₹ 26,158,171", "₹ 17,553,676.00"],
    ["Basavatarakam INDO - American Cancer Hospital", "2024", "4", "321", "216", "67.29%", "₹ 31,338,986", "₹ 14,456,712.25"],
    ["R J SUPER SPECIALITY HOSPITAL", "2023", "4", "235", "165", "70.21%", "₹ 26,705,703", "₹ 13,947,995.59"],
    ["POSITRON HOSPITAL", "2023", "1", "514", "455", "88.52%", "₹ 17,312,435", "₹ 13,154,777.44"],
    ["RPS HOSPITAL MATERNITY & TRAUMA CENTRE", "2023", "1", "158", "108", "68.35%", "₹ 24,108,731", "₹ 12,967,567.50"],
    ["MEHTA MULTISPECIALITY HOSPITAL", "2023", "4", "323", "240", "74.30%", "₹ 21,124,120", "₹ 12,379,724.76"]
]

p2_data = [
    ["MAX HEALTH CARE INSTITUTE LTD - DEHRADUN", "2022-04", "483", "423", "87.58%", "₹ 9,167,027", "₹ 6,600,890.89"],
    ["NORTH BENGAL NEURO RESEARCH CENTRE PVT LTD", "2025-03", "242", "189", "78.10%", "₹ 8,936,539", "₹ 3,409,132.79"],
    ["Secunderabad Main", "2023-08", "2,059", "1,595", "77.46%", "₹ 12,224,564", "₹ 3,113,483.00"],
    ["PARAS HEALTHCARE PVT LTD - SUSHANT LOK -I", "2024-06", "231", "187", "80.95%", "₹ 12,061,182", "₹ 2,186,135.20"],
    ["AMRITA HOSPITAL", "2025-10", "481", "394", "81.91%", "₹ 5,839,736", "₹ 1,999,051.67"],
    ["GUPTA HOSPITAL & RESEARCH CENTRE - KATHUA", "2021-02", "136", "110", "80.88%", "₹ 3,453,471", "₹ 1,726,139.80"],
    ["Gurgaon (Sohana Rd)", "2023-04", "431", "399", "92.58%", "₹ 2,381,748", "₹ 1,698,580.00"],
    ["PRAKASH HOSPITAL P LTD - Noida", "2024-11", "119", "108", "90.76%", "₹ 3,801,479", "₹ 1,649,365.27"],
    ["RUBAN MEMORIAL HOSPITAL RATAN STONE CLINIC", "2021-09", "309", "245", "79.29%", "₹ 2,964,838", "₹ 1,448,224.93"],
    ["GIRIDHAR EYE INSTITUTE PRIVATE LIMITED", "2023-02", "240", "194", "80.83%", "₹ 1,714,111", "₹ 1,209,227.26"]
]

p3_data = [
    ["STAR HOSPITAL (A UNIT OF OM MEDICENTRE PVT LTD)", "2025-06", "543", "37", "14.68x", "₹ 145,246,379", "₹ 92,769,595.72"],
    ["STAR HOSPITAL (A UNIT OF OM MEDICENTRE PVT LTD)", "2025-03", "562", "37", "15.19x", "₹ 138,167,621", "₹ 80,469,302.29"],
    ["STAR HOSPITAL (A UNIT OF OM MEDICENTRE PVT LTD)", "2025-07", "540", "37", "14.59x", "₹ 123,476,340", "₹ 80,096,717.14"],
    ["STAR HOSPITAL (A UNIT OF OM MEDICENTRE PVT LTD)", "2025-05", "405", "37", "10.95x", "₹ 110,775,585", "₹ 72,125,497.64"],
    ["STAR HOSPITAL (A UNIT OF OM MEDICENTRE PVT LTD)", "2025-09", "541", "37", "14.62x", "₹ 111,910,940", "₹ 69,782,718.44"],
    ["STAR HOSPITAL (A UNIT OF OM MEDICENTRE PVT LTD)", "2025-02", "426", "37", "11.51x", "₹ 109,512,368", "₹ 62,209,102.78"],
    ["STAR HOSPITAL (A UNIT OF OM MEDICENTRE PVT LTD)", "2025-10", "579", "37", "15.65x", "₹ 109,990,310", "₹ 61,754,402.45"],
    ["DR S P YADAV HOSPITAL", "2025-10", "495", "67.5", "7.33x", "₹ 97,232,915", "₹ 57,552,450.54"],
    ["DESUN HOSPITAL - KOLKATA", "2025-11", "1,158", "336", "3.45x", "₹ 90,740,588", "₹ 57,224,333.01"],
    ["PARAS HMRI HOSPITAL - PATNA", "2025-09", "5,603", "1,790", "3.13x", "₹ 70,242,543", "₹ 55,996,682.74"]
]

p4_data = [
    ["STAR HOSPITAL (A UNIT OF OM MEDICENTRE)", "2021", "2025", "349", "5673", "244.65%", "₹ 1,349,741,946", "₹ 762,182,272.41"],
    ["GRECIAN SUPER - SPECIALITY HOSPITAL", "2020", "2025", "156", "5857", "200.21%", "₹ 475,279,739", "₹ 371,854,007.04"],
    ["EMC Super Speciality Hospital Pvt. Ltd.", "2021", "2022", "969", "3318", "242.41%", "₹ 439,415,642", "₹ 365,667,913.90"],
    ["MAX SUPER SPECIALITY HOSPITAL - MOHALI", "2024", "2025", "223", "15539", "6868.16%", "₹ 441,055,046", "₹ 364,981,028.46"],
    ["SINGHANIA UNIVERSITY HOSPITAL AND RESEARCH", "2023", "2024", "536", "1896", "253.73%", "₹ 361,889,554", "₹ 229,535,327.46"],
    ["BABY MEMORIAL HOSPITAL LTD, KOZHIKODE", "2022", "2023", "8087", "26026", "221.83%", "₹ 274,629,397", "₹ 223,809,000.62"],
    ["STAR HOSPITAL (A UNIT OF OM MEDICENTRE)", "2023", "2024", "397", "1646", "314.61%", "₹ 345,320,316", "₹ 217,271,595.04"],
    ["DESUN HOSPITAL - KOLKATA", "2022", "2023", "407", "3165", "677.64%", "₹ 257,944,153", "₹ 212,565,775.63"],
    ["SHRI K M MEMORIAL JAIN HEART & GEN", "2024", "2025", "370", "1835", "395.95%", "₹ 357,685,456", "₹ 170,924,676.05"],
    ["YASHODA HOSPITAL AND CANCER INSTITUTE", "2024", "2025", "833", "3731", "347.90%", "₹ 204,248,540", "₹ 145,992,480.79"]
]

total_cases = len(p1_data) + len(p2_data) + len(p3_data) + len(p4_data)

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

H = [f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS_STR}</style></head><body>"]

H.append(f"""
<div class="cover">
  <div class="cover-topbar"></div>
  <div class="cover-title">ECHS FRAUD ANALYTICS</div>
  <div class="cover-sub">Time-Series Surge Analytics &amp; Financial Impact Analysis</div>
  <div class="cover-mod">COMPREHENSIVE REPORT — FY 2021–2026 EDITION (LAST 5 YEARS)</div>
  <div class="cover-boxes">
    <div class="cover-box"><div class="cover-box-label">Classification</div><div class="cover-box-val">RESTRICTED</div></div>
    <div class="cover-box"><div class="cover-box-label">Period</div><div class="cover-box-val">FY 2021–26</div></div>
    <div class="cover-box"><div class="cover-box-label">Records Scanned</div><div class="cover-box-val">2.6Cr+</div></div>
    <div class="cover-box"><div class="cover-box-label">Patterns Run</div><div class="cover-box-val">4 Patterns</div></div>
    <div class="cover-box"><div class="cover-box-label">Cases Flagged</div><div class="cover-box-val">{fmt(total_cases)}</div></div>
  </div>
  <div class="cover-org">IIT KANPUR — Data Analytics &amp; Fraud Intelligence Division</div>
  <div class="cover-date">{today_str} | Ex-Servicemen Contributory Health Scheme (ECHS)</div>
  <div class="cover-botbar"></div>
</div>
""")

# --- EXECUTIVE SUMMARY ---
H.append(f"""
<div class="pb">
<h1>Executive Summary</h1>
<p>This report presents findings from time-series surge analytics conducted on the ECHS database
covering the timeframe from Jan 2021 to Mar 2026. Four independent temporal fraud patterns were applied across
<b>Over 2.6 Crore claim records</b> from 4,091 empanelled hospitals to identify abnormal billing behaviour.</p>

<div class="metric-row">
  <div class="mbox"><div class="mbox-label">Total Cases Flagged</div><div class="mbox-val" style="color:#e74c3c">{fmt(total_cases)}</div><div class="mbox-sub">across 4 fraud patterns</div></div>
  <div class="mbox"><div class="mbox-label">Total Exposure</div><div class="mbox-val">₹1,342 Cr</div><div class="mbox-sub">estimated financial risk</div></div>
  <div class="mbox"><div class="mbox-label">Patterns w/ Findings</div><div class="mbox-val">4</div><div class="mbox-sub">of 4 patterns</div></div>
  <div class="mbox"><div class="mbox-label">Analysis Period</div><div class="mbox-val">5 Yrs</div><div class="mbox-sub">FY 2021–2026</div></div>
</div>

<h1 style="margin-top:14px">Four Time-Series Patterns — Summary</h1>
<table class="dt">
<thead>
<tr><th>#</th><th>Pattern</th><th>What It Detects</th><th>Cases Flagged</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>End-of-Quarter Surge</td><td>Hospitals submitting ≥ 66% of quarterly claims in the final month</td><td><b>{fmt(len(p1_data))}</b></td></tr>
<tr><td>2</td><td>End-of-Month Dump</td><td>Hospitals submitting ≥ 75% of monthly claims in the last week</td><td><b>{fmt(len(p2_data))}</b></td></tr>
<tr><td>3</td><td>Abnormal Monthly Spikes</td><td>Hospitals submitting ≥ 3x their historical median claims in a single month</td><td><b>{fmt(len(p3_data))}</b></td></tr>
<tr><td>4</td><td>Abnormal YoY Spikes</td><td>Hospitals submitting ≥ 3x total claims compared to the previous year</td><td><b>{fmt(len(p4_data))}</b></td></tr>
</tbody>
</table>

<h1 style="margin-top:12px">Immediate Recommended Actions</h1>
<div class="action-item"><span class="action-num">1.</span> <b>Audit all hospitals triggering the EOQ and EOM dump rules</b> ({fmt(len(p1_data) + len(p2_data))} cases) — investigate delayed batching practices or data entry fraud happening just prior to audit cycles.</div>
<div class="action-item"><span class="action-num">2.</span> <b>Initiate field investigations for Abnormal Monthly Spikes</b> ({fmt(len(p3_data))} cases) — hospitals submitting 10x-15x their monthly median frequently signify onboarding of fraudulent billing agents or orchestrated ghost patient cycles.</div>
<div class="action-item"><span class="action-num">3.</span> <b>Verify hospital capacity for YoY outliers</b> ({fmt(len(p4_data))} cases) — request infrastructure and clinical rationale from hospitals experiencing >200% billing growth in one year.</div>
</div>
""")

# --- PATTERN 1 ---
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 1</div>
  <div class="ph-ctx">Time-Series Surge Analytics<br/>(≥ 66% Quarterly Claims in Month 3)</div>
  <div class="ph-title">End-of-Quarter Surge</div>
</div></div>
<p><b>Description:</b> This pattern identifies End-of-Quarter Surges, specifically highlighting instances where 66% or more of a hospital's total quarterly claims were submitted in the last month of that respective quarter.</p>
<div class="tc">Table 1.1 — Top Hospitals with EOQ Surges</div>
<table class="dt">
<thead>
<tr><th>Hospital Name</th><th>Year</th><th>Quarter</th><th>Qtr Claims</th><th>Month 3 Claims</th><th>EOQ Claim %</th><th>Quarterly Billed</th><th>Exposure</th></tr>
</thead>
<tbody>
""")
for row in p1_data:
    H.append(f"<tr><td><b>{row[0][:35]}</b></td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td><b style='color:#c0392b'>{row[5]}</b></td><td>{row[6]}</td><td><b>{row[7]}</b></td></tr>")
H.append("""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item">Filing massive volumes in the final month of the quarter suggests delayed batching or deliberate obfuscation of claim details to rush past the audit cycle.</div>
</div>
""")

# --- PATTERN 2 ---
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 2</div>
  <div class="ph-ctx">Time-Series Surge Analytics<br/>(≥ 75% Monthly Claims in Last Week)</div>
  <div class="ph-title">End-of-Month Dump</div>
</div></div>
<p><b>Description:</b> This pattern identifies the End-of-Month Dump, specifically isolating hospitals where 75% or more of the claims were submitted in the last week of that month.</p>
<div class="tc">Table 2.1 — Top Hospitals with EOM Dumps</div>
<table class="dt">
<thead>
<tr><th>Hospital Name</th><th>Billing Month</th><th>Total Claims</th><th>Last Week Claims</th><th>Dump %</th><th>Total Billed</th><th>Exposure</th></tr>
</thead>
<tbody>
""")
for row in p2_data:
    H.append(f"<tr><td><b>{row[0][:35]}</b></td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td><b style='color:#c0392b'>{row[4]}</b></td><td>{row[5]}</td><td><b>{row[6]}</b></td></tr>")
H.append("""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item">Claim submission should logically follow patient discharge naturally throughout the month. Extreme week-4 concentration indicates either systematic withholding of records or fabricated end-of-cycle generation.</div>
</div>
""")

# --- PATTERN 3 ---
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 3</div>
  <div class="ph-ctx">Time-Series Surge Analytics<br/>(> 3x Historical Median)</div>
  <div class="ph-title">Abnormal Monthly Spikes</div>
</div></div>
<p><b>Description:</b> This pattern detects Abnormal Monthly Spikes, specifically showing only hospitals which have submitted claims over triple (3x) their historical median for a single month.</p>
<div class="tc">Table 3.1 — High Multiplier Spikes (Top 10)</div>
<table class="dt">
<thead>
<tr><th>Hospital Name</th><th>Spike Month</th><th>Spike Claims</th><th>Median</th><th>Multiplier</th><th>Amount Billed</th><th>Exposure</th></tr>
</thead>
<tbody>
""")
for row in p3_data:
    H.append(f"<tr><td><b>{row[0][:35]}</b></td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td><b style='color:#c0392b'>{row[4]}</b></td><td>{row[5]}</td><td><b>{row[6]}</b></td></tr>")
H.append("""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item">A hospital billing 15x its normal median in a single month is almost exclusively linked to a sudden change in management strategy towards fraudulent upcoding or agent onboarding.</div>
</div>
""")

# --- PATTERN 4 ---
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 4</div>
  <div class="ph-ctx">Time-Series Surge Analytics<br/>(> 3x Previous Year Claims)</div>
  <div class="ph-title">Abnormal YoY Spikes</div>
</div></div>
<p><b>Description:</b> This pattern identifies Abnormal YoY Spikes, focusing on hospitals which submitted triple (3x) or more claims than the previous year.</p>
<div class="tc">Table 4.1 — Top Hospitals with 3x+ YoY Spikes</div>
<table class="dt">
<thead>
<tr><th>Hospital Name</th><th>Prev Yr</th><th>Spike Yr</th><th>Prev Claims</th><th>Spike Claims</th><th>YoY Growth</th><th>Amount Billed</th><th>Exposure</th></tr>
</thead>
<tbody>
""")
for row in p4_data:
    H.append(f"<tr><td><b>{row[0][:35]}</b></td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td><b style='color:#c0392b'>{row[5]}</b></td><td>{row[6]}</td><td><b>{row[7]}</b></td></tr>")
H.append("""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item">A Year-over-Year growth exceeding 200-300% without corresponding capacity increases strongly flags hospitals onboarding aggressive marketing/billing agents.</div>
</div>
""")

# --- CONSOLIDATED SUMMARY ---
H.append(f"""
<div class="pb">
<h1>Consolidated Summary</h1>
<p class="tc" style="margin-bottom:10px">All findings are based on structured database analysis and must be
corroborated with physical audit records before enforcement action is taken.</p>
<table class="dt">
<thead>
<tr><th>Pattern</th><th>Fraud Signal</th><th>Cases Flagged</th><th>Exposure</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>End-of-Quarter Surge</td><td><b>{fmt(len(p1_data))}</b></td><td>₹ 156.45 Cr</td></tr>
<tr><td>2</td><td>End-of-Month Dump</td><td><b>{fmt(len(p2_data))}</b></td><td>₹ 19.53 Cr</td></tr>
<tr><td>3</td><td>Abnormal Monthly Spikes</td><td><b>{fmt(len(p3_data))}</b></td><td>₹ 690.65 Cr</td></tr>
<tr><td>4</td><td>Abnormal YoY Spikes</td><td><b>{fmt(len(p4_data))}</b></td><td>₹ 3,064.78 Cr</td></tr>
<tr style="background:#fdf0f0;font-weight:700"><td colspan="2"><b>TOTAL (De-duplicated Estimate)</b></td><td><b style="color:#c0392b">{fmt(total_cases)}</b></td><td><b>Over ₹ 1,342 Cr</b></td></tr>
</tbody>
</table>

<p style="margin-top:16px;font-size:7.5pt;color:#555;text-align:center">
Prepared by IIT Kanpur — Data Analytics &amp; Fraud Intelligence Division | {today_str}<br/>
All findings are based on structured database analysis and must be corroborated with physical audit records before enforcement action.
</p>
</div>
""")


H.append("</body></html>")

full_html = "".join(H)
print("Generating PDF ...")
HTML(string=full_html, base_url=BASE).write_pdf(PDF_OUT)
print(f"✅ Saved → {PDF_OUT}")
