import os
import re
import csv
import glob
import locale
import datetime
from weasyprint import HTML

# ==============================================================================
# CONFIGURATION
# ==============================================================================
# Define the output path for your generated PDF report
REPORT_TITLE = "Your Report Title Here"
REPORT_SUBTITLE = "Subtitle or Description Here"
MODULE_NAME = "MODULE X — EDITION"
PDF_OUT = "custom_report.pdf"

# Base URL for local assets (if you include images)
BASE = f"file://{os.path.abspath(os.path.dirname(__file__))}/"

# Locale for Indian Rupee formatting
try: locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
except: pass

# Colors
NAV  = "#1a2c42"  # Deep Navy Blue
GOLD = "#c29b62"  # Professional Gold

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================
def fmt(num):
    """Format integers with commas."""
    try: return f"{int(num):,}"
    except: return str(num)

def cr(val):
    """Format currency values in Crores."""
    try:
        v = float(val)
        if v == 0: return "₹0"
        return f"₹{v/10000000:.2f} Cr"
    except:
        return "—"

def safe(txt):
    """Safely escape HTML characters."""
    return str(txt).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def th(*cols):
    """Generate HTML table headers."""
    return "<thead><tr>" + "".join(f"<th>{c}</th>" for c in cols) + "</tr></thead>"

def hosp_display(hospitals_raw, count):
    """Clean up and truncate long hospital lists for display."""
    if not hospitals_raw: return "—"
    if int(count) > 1:
        hosps = [h.split(":", 1)[-1] if ":" in h else h for h in str(hospitals_raw).split(" | ")]
        text = ", ".join(h.strip() for h in hosps if h.strip())
        return text[:60] + "…" if len(text) > 60 else text
    return fmt(count)

# ==============================================================================
# CSS STYLESHEET
# ==============================================================================
CSS_STR = f"""
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ font-family:Arial,Helvetica,sans-serif; font-size:9pt; color:#1a1a1a; line-height:1.55; background:#fff; }}

@page {{
    size:A4; margin:20mm 15mm 18mm 15mm;
    @top-left   {{ content:"{REPORT_TITLE} — CONFIDENTIAL";
                  font-family:Arial; font-size:7.5pt; font-weight:700; color:{NAV};
                  border-bottom:1px solid #ccc; padding-bottom:4px; vertical-align:bottom; }}
    @top-right  {{ content:"Page " counter(page);
                  font-family:Arial; font-size:7.5pt; color:#555;
                  border-bottom:1px solid #ccc; padding-bottom:4px; vertical-align:bottom; }}
    @bottom-left  {{ content:"RESTRICTED — For internal audit and investigative use only.";
                    font-family:Arial; font-size:7pt; color:#555; border-top:1px solid #ddd; padding-top:3px; }}
    @bottom-right {{ content:"Generated: {datetime.datetime.now().strftime('%d %b %Y, %H:%M')}";
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

# ==============================================================================
# HTML CONSTRUCTION
# ==============================================================================
def generate_report():
    today_str = datetime.datetime.now().strftime("%-d %B %Y")
    
    # You can define your dynamic variables here
    total_cases = 1500
    total_exposure = 250000000 # Example: 25 Cr
    
    H = [f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS_STR}</style></head><body>"]

    # 1. Cover Page
    # Prevent blank first page by ensuring no whitespace before the cover div
    H.append(f"""<div class="cover">
      <div class="cover-topbar"></div>
      <div class="cover-title">{REPORT_TITLE.upper()}</div>
      <div class="cover-sub">{REPORT_SUBTITLE}</div>
      <div class="cover-mod">{MODULE_NAME}</div>
      <div class="cover-boxes">
        <div class="cover-box"><div class="cover-box-label">Classification</div><div class="cover-box-val">RESTRICTED</div></div>
        <div class="cover-box"><div class="cover-box-label">Period</div><div class="cover-box-val">FY 2021–26</div></div>
        <div class="cover-box"><div class="cover-box-label">Records Scanned</div><div class="cover-box-val">26M+</div></div>
        <div class="cover-box"><div class="cover-box-label">Patterns Run</div><div class="cover-box-val">8 Patterns</div></div>
        <div class="cover-box"><div class="cover-box-label">Cases Flagged</div><div class="cover-box-val">{fmt(total_cases)}</div></div>
      </div>
      <div class="cover-org">IIT KANPUR — Data Analytics &amp; Fraud Intelligence Division</div>
      <div class="cover-date">{today_str} | Ex-Servicemen Contributory Health Scheme (ECHS)</div>
      <div class="cover-botbar"></div>
    </div>""")

    # 2. Executive Summary
    H.append(f"""<div class="pb">
    <h1>Executive Summary</h1>
    <p>Provide a high-level summary of the findings here. Explain what this report aims to uncover, the data scope, and the critical observations.</p>

    <div class="metric-row">
      <div class="mbox"><div class="mbox-label">Metric 1</div><div class="mbox-val">Value</div><div class="mbox-sub">subtext here</div></div>
      <div class="mbox"><div class="mbox-label">Metric 2</div><div class="mbox-val">Value</div><div class="mbox-sub">subtext here</div></div>
      <div class="mbox"><div class="mbox-label">Metric 3</div><div class="mbox-val">Value</div><div class="mbox-sub">subtext here</div></div>
    </div>
    
    <h1 style="margin-top:14px">Eight Patterns — Summary</h1>
    <table class="dt">
    {th("#","Pattern","What It Detects","Cases Flagged")}
    <tbody>
    <tr><td>1</td><td>Pattern Alpha</td><td>Detects anomalies in categorical assignments — indicative of misclassification</td><td><b>{fmt(500)}</b></td></tr>
    <tr><td>2</td><td>Pattern Beta</td><td>Identifies simultaneous overlapping records — physical impossibility indicating ghost entries</td><td><b>{fmt(350)}</b></td></tr>
    <tr><td>3</td><td>Pattern Gamma</td><td>Duplicate invoice resubmission — direct double-billing indicators</td><td><b>{fmt(200)}</b></td></tr>
    <tr><td>4</td><td>Pattern Delta</td><td>Agent coordination rings — multiple disparate accounts managed by single contact</td><td><b>{fmt(150)}</b> real + <b>{fmt(10)}</b> dummy</td></tr>
    <tr><td>5</td><td>Pattern Epsilon</td><td>Biometric or unique identifier duplication — synthetic identity creation</td><td><b>{fmt(250)}</b></td></tr>
    <tr><td>6</td><td>Pattern Zeta</td><td>Statistical over-utilisation outliers (Q3+1.5×IQR) — extreme frequency usage</td><td><b>{fmt(40)}</b></td></tr>
    <tr><td>7</td><td>Pattern Eta</td><td>Unusual geographic hopping — beneficiaries claiming treatments in distant locations within hours</td><td><b>{fmt(80)}</b></td></tr>
    <tr><td>8</td><td>Pattern Theta</td><td>Impossible medical combination — diagnosing contradictory conditions on the same day</td><td><b>{fmt(25)}</b></td></tr>
    </tbody>
    </table>

    <h1 style="margin-top:12px">Immediate Recommended Actions</h1>
    <div class="action-item"><span class="action-num">1.</span> <b>Action Step One</b> — description of the action and rationale here.</div>
    <div class="action-item"><span class="action-num">2.</span> <b>Action Step Two</b> — description of the action and rationale here.</div>
    <div class="action-item"><span class="action-num">3.</span> <b>Action Step Three</b> — description of the action and rationale here.</div>
    </div>
    """)

    # 3. Example Pattern
    # You can loop through your data here and build tables dynamically.
    H.append(f"""<div class="pb">
    <div class="nob">
    <div class="ph">
      <div class="ph-label">PATTERN 1</div>
      <div class="ph-ctx">Optional context label<br/>(e.g., specific rules)</div>
      <div class="ph-title">Pattern Title Goes Here</div>
    </div></div>
    <p><b>Description:</b> Explain what this specific pattern detects and how the data was filtered.</p>
    
    <table class="dt">
    {th("ID", "Name", "Score", "Exposure")}
    <tbody>
      <tr><td>001</td><td>John Doe</td><td>95</td><td>{cr(1500000)}</td></tr>
      <tr><td>002</td><td>Jane Smith</td><td>88</td><td>{cr(850000)}</td></tr>
    </tbody>
    </table>
    
    <div class="kf-head">Key Findings</div>
    <div class="kf-item">First key insight from the data above.</div>
    <div class="kf-item">Second key insight or anomaly detected.</div>
    </div>
    """)

    # 4. Final Footer/Consolidated View
    H.append(f"""<div class="pb">
    <h1>Consolidated Summary</h1>
    <p class="tc" style="margin-bottom:10px">All findings are based on structured database analysis and must be corroborated with physical audit records before enforcement action is taken.</p>
    <table class="dt">
    {th("Pattern", "Fraud Signal", "Cases Flagged", "Exposure")}
    <tbody>
      <tr><td>1</td><td>Duplicate Card IDs (3+ Svc Numbers)</td><td><b>{fmt(1220)}</b></td><td>{cr(308900000)}</td></tr>
      <tr><td>2</td><td>Simultaneous Admissions (Gap ≤ 7 days)</td><td><b>{fmt(6577520)}</b></td><td>{cr(182572600000)}</td></tr>
      <tr><td>3</td><td>Duplicate Bill Number Resubmission</td><td><b>{fmt(250090)}</b></td><td>{cr(9320300000)}</td></tr>
      <tr><td>4</td><td>Mobile Number Rings (5+ cards)</td><td><b>{fmt(177291)}</b> real + <b>{fmt(483)}</b> dummy</td><td>{cr(110639800000)}</td></tr>
      <tr><td>5</td><td>UID (Aadhaar) Duplication</td><td><b>{fmt(82930)}</b></td><td>{cr(18186000000)}</td></tr>
      <tr><td>6</td><td>High Frequency Claims (≥13 claims)</td><td><b>{fmt(486083)}</b></td><td>{cr(168607800000)}</td></tr>
      <tr><td>7</td><td>Unusual Geographic Hopping</td><td><b>{fmt(80)}</b></td><td>{cr(45000000)}</td></tr>
      <tr><td>8</td><td>Impossible Medical Combination</td><td><b>{fmt(25)}</b></td><td>{cr(12000000)}</td></tr>
      <tr style="background:#fdf0f0;font-weight:700"><td colspan="2"><b>TOTAL</b></td><td><b style="color:#c0392b">{fmt(7575134)}</b></td><td><b>{cr(489635300000)}</b></td></tr>
    </tbody>
    </table>
    
    <p style="margin-top:16px;font-size:7.5pt;color:#555;text-align:center">
    Prepared by IIT KANPUR — Data Analytics &amp; Fraud Intelligence Division | {today_str}<br/>
    All findings are based on structured database analysis and must be corroborated with physical audit records before enforcement action.
    </p>
    </div>
    """)

    H.append("</body></html>")
    
    # Write to PDF
    full_html = "".join(H)
    print("Generating PDF template...")
    HTML(string=full_html, base_url=BASE).write_pdf(PDF_OUT)
    print(f"✅ Saved template report to -> {PDF_OUT}")

if __name__ == '__main__':
    generate_report()
