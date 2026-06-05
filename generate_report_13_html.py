#!/usr/bin/env python3
"""
ECHS Module 13 - High-Value Claim Risk Scoring : HTML + WeasyPrint report.

Same house style as the senior's generate_module11_report_html.py (navy/gold
cover, metric boxes, gold left-bar section headers, CSS data tables, key-findings
boxes, running @page header/footer, consolidated risk register) - with the
padding/layout tightened up. Reads the existing module_13/data artifacts produced
by build_module13_data.py; no DB access.

Run:  .venv/bin/python build_module13_data.py  (already done)  ->  this script.
"""
import os
# WeasyPrint needs the Homebrew native libs; make them discoverable before import.
os.environ.setdefault("DYLD_FALLBACK_LIBRARY_PATH", "/opt/homebrew/lib")

import csv
import json
import html
from datetime import date

from weasyprint import HTML

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "module_13", "data")
REPORTS = os.path.join(BASE, "module_13", "reports")
os.makedirs(REPORTS, exist_ok=True)
OUT = os.path.join(REPORTS, "ECHS_Module13_High_Value_Risk_Report.pdf")
today_str = date.today().strftime("%d %B %Y")

# ---- data loading ----------------------------------------------------------
def load_csv(name):
    p = os.path.join(DATA, name)
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def load_json(name):
    p = os.path.join(DATA, name)
    return json.load(open(p)) if os.path.exists(p) else {}

S = load_json("module13_summary.json")
CASES = load_json("module13_cases.json")
DEEP = load_json("module13_hospital_deepdive.json")
Q13A = load_csv("q13a_top_claims.csv")
DUPS = load_csv("q13a2_duplicates.csv")
Q13B = load_csv("q13b_hospital_scorecard.csv")
REG = load_csv("q13c_regional.csv")
Q13D = load_csv("q13d_chronic_claimants.csv")
BULK = load_csv("q13f_bulk_injection.csv")
GHOST = load_csv("module13_ghost_claims.csv")

# ---- formatting helpers ----------------------------------------------------
def e(t):
    return html.escape("" if t is None else str(t))

def fmt(n):
    try:
        return f"{int(float(n)):,}"
    except (TypeError, ValueError):
        return e(n)

def inr(v):                      # raw rupees -> ₹.. Cr / L
    try:
        v = float(v)
    except (TypeError, ValueError):
        return e(v)
    if v >= 1e7:
        return f"₹{v/1e7:.2f} Cr"
    if v >= 1e5:
        return f"₹{v/1e5:.2f} L"
    return f"₹{v:,.0f}"

def crr(v):                      # value already in crore
    try:
        return f"₹{float(v):,.2f} Cr"
    except (TypeError, ValueError):
        return e(v)

def short(t, n=46):
    t = "" if t is None else str(t)
    return e(t if len(t) <= n else t[:n - 1] + "…")

def risk_txt(band):
    b = str(band).upper()
    c = {"CRITICAL": "#c0392b", "HIGH": "#d4680a", "MEDIUM": "#7f8c8d"}.get(b, "#27ae60")
    return f'<span style="color:{c};font-weight:700">{e(b)}</span>'

def score_cell(row):
    return f'{risk_txt(row.get("risk_band",""))} <span style="color:#555">{e(row.get("risk_score",""))}</span>'

def th(*cols):
    return "<thead><tr>" + "".join(f"<th>{c}</th>" for c in cols) + "</tr></thead>"

def colgroup(*widths):
    return "<colgroup>" + "".join(f'<col style="width:{w}"/>' for w in widths) + "</colgroup>"

NAVY, GOLD = "#1a2744", "#c9a84c"

# ---- CSS (padding tightened vs the uploaded file) --------------------------
CSS = """
* { box-sizing:border-box; margin:0; padding:0; }
body { font-family:'DejaVu Sans',Arial,Helvetica,sans-serif; font-size:9pt; color:#222b36; line-height:1.5; }

@page {
  size:A4; margin:24mm 16mm 20mm 16mm;
  @top-left { content:"ECHS FRAUD ANALYTICS  ·  MODULE 13  ·  CONFIDENTIAL";
              font-family:'DejaVu Sans'; font-size:7.5pt; font-weight:bold; color:#1a2744; }
  @top-right { content:"IIT Kanpur  ·  Page " counter(page);
               font-family:'DejaVu Sans'; font-size:7.5pt; color:#666; }
  @bottom-left { content:"RESTRICTED — For internal audit and investigative use only. Not for distribution.";
                 font-family:'DejaVu Sans'; font-size:7pt; color:#777; }
  @bottom-right { content:"Generated: __DATE__"; font-family:'DejaVu Sans'; font-size:7pt; color:#777; }
}
@page cover { margin:0; @top-left{content:none} @top-right{content:none}
              @bottom-left{content:none} @bottom-right{content:none} }

/* ---- cover ---- */
.cover { page:cover; background:#1a2744; width:210mm; height:297mm; position:relative; color:#fff; }
.cover-band-t,.cover-band-b { position:absolute; left:0; right:0; height:11px; background:#c9a84c; }
.cover-band-t { top:0; } .cover-band-b { bottom:0; }
.cover-in { position:absolute; left:24mm; right:24mm; top:52mm; text-align:center; }
.cover-gov { font-size:9pt; letter-spacing:1px; color:#aeb6c8; margin-bottom:34mm; }
.cover-kick { font-size:8.5pt; letter-spacing:3px; color:#c9a84c; font-weight:bold; margin-bottom:12px; }
.cover-title { font-size:31pt; font-weight:bold; letter-spacing:1px; line-height:1.1; margin-bottom:10px; }
.cover-sub { font-size:13pt; color:#cfd5e2; margin-bottom:6px; }
.cover-mod { font-size:9pt; letter-spacing:2px; color:#c9a84c; margin-bottom:24px; }
.cover-rule { width:62mm; height:2px; background:#c9a84c; margin:0 auto 26px auto; }
table.cover-boxes { margin:0 auto 30px auto; border-collapse:separate; border-spacing:6px; }
.cover-box { background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.16);
             padding:12px 14px; text-align:center; vertical-align:middle; }
.cover-box-l { font-size:6.5pt; color:#aeb6c8; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:6px; }
.cover-box-v { font-size:13pt; font-weight:bold; color:#fff; }
.cover-org { font-size:11pt; color:#c9a84c; font-weight:bold; margin-bottom:6px; }
.cover-date { font-size:8.5pt; color:#aeb6c8; }

/* ---- sections ---- */
.section { page-break-before:always; }
.sec { border-left:5px solid #c9a84c; padding:3px 0 3px 14px; margin:0 0 14px 0; page-break-after:avoid; }
table.sec-h { width:100%; border-collapse:collapse; }
.sec-h-l { vertical-align:middle; }
.sec-h-r { vertical-align:middle; text-align:right; width:56mm; font-size:8pt; color:#8a90a0;
           font-style:italic; line-height:1.35; }
.sec-kick { font-size:7.5pt; font-weight:bold; letter-spacing:2px; color:#c9a84c;
            text-transform:uppercase; margin-bottom:4px; }
.sec-title { font-size:15pt; font-weight:bold; color:#1a2744; letter-spacing:0.3px; }
h2 { font-size:11pt; color:#1a2744; margin:16px 0 7px 0; page-break-after:avoid; }

p { margin-bottom:9px; text-align:justify; }
b { font-weight:700; } .muted { color:#667; }
.lead { margin-bottom:11px; }

/* ---- metric boxes ---- */
table.metrics { width:100%; border-collapse:separate; border-spacing:6px; margin:6px 0 14px 0; }
.mbox { background:#1a2744; color:#fff; padding:14px 12px; text-align:center; vertical-align:middle; }
.mbox-l { font-size:6.8pt; color:#aeb6c8; text-transform:uppercase; letter-spacing:1px; margin-bottom:5px; }
.mbox-v { font-size:16pt; font-weight:bold; }
.mbox-s { font-size:6.8pt; color:#aeb6c8; margin-top:4px; }

/* ---- data tables ---- */
table.dt { width:100%; border-collapse:collapse; table-layout:fixed; margin:6px 0 16px 0; font-size:8pt; }
table.dt thead tr { background:#1a2744; color:#fff; }
table.dt thead th { padding:7px 9px; text-align:left; font-weight:700; font-size:7.8pt;
                    border-bottom:2px solid #c9a84c; word-wrap:break-word; }
table.dt tbody td { padding:6px 9px; border-bottom:1px solid #e7e9ee; vertical-align:top;
                    word-wrap:break-word; overflow-wrap:break-word; }
table.dt tbody tr:nth-child(even) { background:#f5f7fa; }
.tcap { font-size:7.5pt; color:#7a8190; margin:2px 0 4px 0; font-weight:bold; letter-spacing:0.4px; }
.num { font-weight:700; } .red { color:#c0392b; font-weight:700; }

/* ---- key findings + callout ---- */
.kf { background:#faf7ef; border-left:3px solid #c9a84c; padding:8px 12px; margin-bottom:8px;
      font-size:8.5pt; line-height:1.5; }
.kf-h { font-size:10.5pt; font-weight:bold; color:#1a2744; margin:12px 0 7px 0; }
.callout { background:#fdf1f1; border:1px solid #e7b8b8; border-left:4px solid #c0392b;
           padding:10px 13px; margin:8px 0 12px 0; font-size:8.5pt; }
.callout b { color:#a02020; }

/* ---- case studies ---- */
.case { border:1px solid #e2e5ec; border-top:3px solid #c9a84c; padding:11px 14px; margin-bottom:12px;
        page-break-inside:avoid; }
.case-h { font-size:11pt; font-weight:bold; color:#1a2744; margin-bottom:7px; }
table.facts { width:100%; border-collapse:collapse; margin-bottom:8px; font-size:8.2pt; }
table.facts td { padding:4px 8px; border-bottom:1px solid #eef0f4; vertical-align:top; }
table.facts td.k { width:30mm; font-weight:bold; color:#1a2744; background:#f4f6f9; }
.action { font-size:8.4pt; color:#1a2744; }

/* ---- recommendations / register ---- */
ol.acts { margin:4px 0 6px 18px; } ol.acts li { margin-bottom:6px; font-size:8.6pt; }
"""

# ---- builders --------------------------------------------------------------
H = [f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS.replace("__DATE__", today_str)}</style></head><body>']

def sec(title, kicker="", context=""):
    kick = f'<div class="sec-kick">{kicker}</div>' if kicker else ""
    return ('<div class="sec"><table class="sec-h"><tr>'
            f'<td class="sec-h-l">{kick}<div class="sec-title">{title}</div></td>'
            f'<td class="sec-h-r">{context}</td></tr></table></div>')

def mbox(label, value, sub="", vcolor=""):
    style = f' style="color:{vcolor}"' if vcolor else ""
    return (f'<td class="mbox"><div class="mbox-l">{label}</div>'
            f'<div class="mbox-v"{style}>{value}</div>'
            f'<div class="mbox-s">{sub}</div></td>')

# ===== COVER =====
H.append(f"""
<div class="cover">
  <div class="cover-band-t"></div>
  <div class="cover-in">
    <div class="cover-gov">GOVERNMENT OF INDIA &nbsp;·&nbsp; EX-SERVICEMEN CONTRIBUTORY HEALTH SCHEME</div>
    <div class="cover-kick">FRAUD ANALYTICS &amp; INTELLIGENCE REPORT</div>
    <div class="cover-title">ECHS FRAUD ANALYTICS</div>
    <div class="cover-sub">Module 13 — High-Value Claim Risk Scoring</div>
    <div class="cover-mod">CLAIMS ABOVE ₹5 LAKH &nbsp;|&nbsp; LAST 5 YEARS &nbsp;|&nbsp; RULE-BASED SIGNALS + COMPOSITE RISK SCORE</div>
    <div class="cover-rule"></div>
    <table class="cover-boxes"><tr>
      <td class="cover-box"><div class="cover-box-l">High-Value Claims</div><div class="cover-box-v">{fmt(S.get('total_hv_claims',0))}</div></td>
      <td class="cover-box"><div class="cover-box-l">Total Exposure</div><div class="cover-box-v">{crr(S.get('total_exposure_cr',0))}</div></td>
      <td class="cover-box"><div class="cover-box-l">Deducted</div><div class="cover-box-v">{crr(S.get('total_deducted_cr',0))}</div></td>
      <td class="cover-box"><div class="cover-box-l">100% Deducted</div><div class="cover-box-v">{fmt(S.get('full_deduction_hv_claims',0))}</div></td>
      <td class="cover-box"><div class="cover-box-l">Flagged Logins</div><div class="cover-box-v">{fmt(S.get('n_flagged_hospitals',0))}</div></td>
    </tr></table>
    <div class="cover-org">IIT KANPUR — Data Analytics &amp; Fraud Intelligence Division</div>
    <div class="cover-date">{today_str} &nbsp;|&nbsp; Classification: RESTRICTED</div>
  </div>
  <div class="cover-band-b"></div>
</div>""")

# ===== EXECUTIVE SUMMARY =====
cbd = S.get("claimants_band_dist", {}); hbd = S.get("hospitals_band_dist", {})
H.append('<div class="section">' + sec("Executive Summary"))
H.append(f"""<p class="lead">Module 13 targets the highest-financial-risk stratum of the ECHS claim ecosystem:
individual claims exceeding <b>₹5 lakh</b> per admission, analysed across the <b>last five years</b> from the
<b>claim_intimation</b> and <b>claim_submission</b> tables. Each claim, hospital login and beneficiary card is
scored with a transparent, rule-based composite risk score (0–100) — no machine learning, so every score is
auditable. <b>Total Financial Exposure</b> is the gross claimed value of the flagged claims (approximate; the
recoverable amount is set at audit).</p>""")
H.append('<table class="metrics"><tr>' +
         mbox("Total Exposure", crr(S.get('total_exposure_cr',0)), "gross claimed, &gt;₹5L") +
         mbox("Total Deducted", crr(S.get('total_deducted_cr',0)), f"{S.get('overall_ded_pct',0)}% overall", "#e74c3c") +
         mbox("100% Deducted", fmt(S.get('full_deduction_hv_claims',0)), "approved at ₹0") +
         mbox("Chronic Claimants", fmt(S.get('n_chronic_claimants',0)), "≥3 high-value claims") +
         mbox("Bulk Events", fmt(S.get('n_bulk_events',0)), f"{S.get('n_bulk_system_compromise',0)} system-compromise") +
         '</tr></table>')
H.append(f"""<p>By composite risk band, <b>{fmt(cbd.get('CRITICAL',0)+cbd.get('HIGH',0))}</b> beneficiary cards and
<b>{fmt(hbd.get('CRITICAL',0)+hbd.get('HIGH',0))}</b> hospital logins fall in the CRITICAL/HIGH tiers and head the
verification queue. Flagged claims span {e(S.get('earliest_admit',''))} to {e(S.get('latest_admit',''))}.</p>""")

H.append('<div class="kf-h">Fraud patterns at a glance</div>')
H.append('<table class="dt">' + colgroup("7%", "27%", "44%", "13%", "9%") +
         th("#", "Pattern", "What it detects", "Count", "Risk") + "<tbody>")
pat_rows = [
    ("1", "High-value claims (&gt;₹5L)", "Exposure concentration in the top claim stratum",
     f"{fmt(S.get('total_hv_claims',0))}", "CRITICAL"),
    ("2", "100% deduction", "Multi-lakh bills approved at ₹0 — billing beyond the package ceiling",
     f"{fmt(S.get('full_deduction_hv_claims',0))}", "CRITICAL"),
    ("3", "Hospital overcharging", "Logins with avg deduction &gt; 25% on high-value claims",
     f"{fmt(S.get('n_flagged_hospitals',0))} logins", "CRITICAL"),
    ("4", "Chronic repeat claimants", "One card with ≥3 high-value claims",
     f"{fmt(S.get('n_chronic_claimants',0))}", "HIGH"),
    ("5", "Same-day duplicate billing", "Same card+date+amount under multiple intimation IDs",
     f"{fmt(S.get('n_duplicate_groups',0))} groups", "CRITICAL"),
    ("6", "Bulk claim injection", "Hundreds of intimation IDs created in one day (programmatic)",
     f"{fmt(S.get('n_bulk_events',0))} events", "CRITICAL"),
    ("7", "Ghost / anomalous hospital ID", "High-value claims with NULL or phone-like hospital IDs",
     f"{fmt(S.get('n_anomalous_hv_claims',0))}", "HIGH"),
    ("8", "ECHS polyclinic abuse", "Polyclinic logins routing high-value IPD claims (high deduction)",
     f"{fmt(S.get('n_polyclinic_claims',0))}", "HIGH"),
]
for n, p, w, c, r in pat_rows:
    H.append(f'<tr><td>{n}</td><td><b>{p}</b></td><td>{w}</td><td class="num">{c}</td><td>{risk_txt(r)}</td></tr>')
H.append("</tbody></table>")

H.append('<div class="kf-h">Immediate recommended actions</div><ol class="acts">')
for a in [
    f"<b>Treat bulk-injection events as a security incident</b> ({fmt(S.get('n_bulk_events',0))} events) — pull portal access logs and escalate to ECHS IT / CERT-In.",
    f"<b>Recover on same-day duplicates</b> ({fmt(S.get('n_duplicate_groups',0))} groups) — confirm which submissions were paid and reclaim the surplus.",
    f"<b>Physically verify the top chronic claimants</b> ({fmt(S.get('n_chronic_claimants',0))} cards ≥3 claims) — discharge-summary sampling.",
    f"<b>Audit the top-deduction hospital logins</b> ({fmt(S.get('n_flagged_hospitals',0))} logins &gt;25% deduction) — empanelment + package-rate review.",
    f"<b>Reject invalid hospital IDs at intake</b> ({fmt(S.get('n_anomalous_hv_claims',0))} claims, {crr(S.get('anomalous_exposure_cr',0))}) — block NULL/phone-like IDs.",
]:
    H.append(f"<li>{a}</li>")
H.append("</ol></div>")

# ===== PARAMETERS & METHODOLOGY =====
H.append('<div class="section">' + sec("Parameters &amp; Methodology", "How the analysis works"))
H.append("""<p class="lead"><b>Data.</b> High-value claims (gross claimed &gt; ₹5 lakh) over the last five years,
joined from <b>claim_intimation</b> and <b>claim_submission</b> on the intimation ID. Regional figures use the
pre-aggregated <b>settlement_stat</b> table.</p>
<p><b>Claim pipeline.</b> A claim flows: intimation (admission notified) → submission (hospital bills the gross
amount) → UTI audit (an approved amount is set; the balance is the <b>deduction</b>) → settlement. A 100%
deduction means the audit approved nothing on a multi-lakh bill.</p>""")
H.append('<div class="tcap">Table P.1 — Parameters &amp; definitions</div>')
H.append('<table class="dt">' + colgroup("26%", "74%") + th("Parameter", "Definition / threshold") + "<tbody>")
for k, v in [
    ("High-value claim", "Gross claimed amount &gt; ₹5,00,000 for a single admission"),
    ("Deduction %", "(gross claimed − UTI approved) / gross claimed × 100"),
    ("Chronic repeat claimant", "One beneficiary card with ≥ 3 high-value claims"),
    ("Single-hospital lock-in", "Share of a card's high-value claims filed at one hospital login"),
    ("Bulk injection (tiers)", "Same-day intimations per card: &gt;300 = system compromise; 100–300 = account abuse; 50–100 = watch"),
    ("Anomalous hospital ID", "NULL, −1/0 placeholder, or a numeric/phone-like value (not a real login)"),
    ("Total Financial Exposure", "Sum of gross claimed on flagged claims (approximate; recovery set at audit)"),
]:
    H.append(f'<tr><td><b>{k}</b></td><td>{v}</td></tr>')
H.append("</tbody></table>")

H.append('<div class="kf-h">Composite risk score — component weights (0–100, no ML)</div>')
H.append('<p>Bands: ' + risk_txt("CRITICAL") + ' ≥ 70, ' + risk_txt("HIGH") + ' 45–69, ' + risk_txt("MEDIUM") + ' &lt; 45. '
         'Each score is a plain weighted sum of normalised signals — fully reconstructable from the source rows.</p>')
W = S.get("weights", {})
for title, key in [("Claim-level score", "claim"), ("Hospital-level score", "hospital"), ("Claimant-level score", "claimant")]:
    ww = W.get(key, {})
    if not ww:
        continue
    H.append(f'<div class="tcap">{title}</div><table class="dt">' + colgroup("74%", "26%") +
             th("Component", "Weight") + "<tbody>")
    for k, v in ww.items():
        H.append(f'<tr><td>{e(k.replace("_"," ").title())}</td><td class="num">{v}</td></tr>')
    H.append("</tbody></table>")
H.append("</div>")

# ===== LIMITATIONS =====
H.append('<div class="section">' + sec("Limitations &amp; Assumptions"))
H.append('<div class="callout">')
for t in [
    "<b>Red flags, not verdicts.</b> Every item is an automated investigative lead, not a confirmed finding. A qualified auditor must verify each case before any action.",
    "<b>Deduction is not fraud.</b> A high deduction can reflect a legitimate package ceiling, a coding error, or incomplete documentation — it flags where billed value was removed, not why.",
    "<b>Login codes are identifiers.</b> Hospital login codes (e.g. parkhosg, pol.3325) are used as identifiers only; this report does not assert their real-world hospital identity.",
    "<b>Data quality.</b> Findings depend on the accuracy of the intimation/submission tables and the UTI deduction codes; systemic gaps (e.g. missing hospital IDs) can both create and hide signals.",
    "<b>Scope.</b> Analysis covers the last five years only; older claims are out of scope by design.",
]:
    H.append(f'<p style="margin-bottom:6px">• {t}</p>')
H.append('<p style="margin:0"><b>ALL CASES REQUIRE VERIFICATION BY QUALIFIED AUDITORS BEFORE ANY ACTION IS TAKEN.</b></p>')
H.append('</div></div>')

# ===== KEY FRAUD SIGNALS =====
H.append('<div class="section">' + sec("Key Fraud Signals", "Q13 · data-derived", "Derived directly from the last-5-year scan; risk band reflects the composite score"))
H.append('<table class="dt">' + colgroup("5%", "26%", "55%", "14%") + th("#", "Signal", "Finding", "Risk") + "<tbody>")
sig = []
if Q13A:
    r = Q13A[0]
    sig.append(("Largest single high-value claim",
                f"{inr(r['exposure'])} at {e(r['hospital_code'])} ({short(r['beneficiary'],26)}); {e(r['ded_pct'])}% deducted.", r["risk_band"]))
if Q13B:
    bydev = max(Q13B, key=lambda x: float(x["avg_ded_pct"]))
    rate = float(bydev["avg_ded_pct"]); rb = "CRITICAL" if rate >= 70 else ("HIGH" if rate >= 50 else "MEDIUM")
    sig.append(("Highest hospital deduction rate",
                f"{e(bydev['hospital_code'])}: {e(bydev['avg_ded_pct'])}% avg deduction on {fmt(bydev['hv_claims'])} high-value claims.", rb))
    top = Q13B[0]
    sig.append(("Largest absolute hospital deduction",
                f"{e(top['hospital_code'])}: {crr(top['deducted_cr'])} deducted across {fmt(top['hv_claims'])} claims.", top["risk_band"]))
sig.append(("100% deduction claims",
            f"{fmt(S.get('full_deduction_hv_claims',0))} high-value claims approved at ₹0 — billing beyond the package ceiling.", "HIGH"))
if DUPS:
    r = DUPS[0]
    sig.append(("Same-day duplicate billing",
                f"{short(r['beneficiary'],24)} (card {e(r['card_id'])}): {e(r['dup_count'])} identical {inr(r['exposure'])} claims on {e(str(r['admission_date'])[:10])}.", "CRITICAL"))
if Q13D:
    r = Q13D[0]
    sig.append(("Chronic repeat claimant",
                f"{short(r['beneficiary'],24)} (card {e(r['card_id'])}): {fmt(r['hv_claims'])} HV claims, {crr(r['exposure_cr'])} exposure, {round(float(r['lockin'])*100)}% at {e(r['primary_hospital'])}.", r["risk_band"]))
if BULK:
    r = BULK[0]
    sig.append(("Extreme bulk claim injection",
                f"{short(r['beneficiary'],22)}: {fmt(r['intimation_count'])} intimation IDs in one day at {e(r['hospital_code'])} ({e(r['tier'])}).", "CRITICAL"))
if S.get("n_anomalous_hv_claims", 0):
    sig.append(("Anomalous / missing hospital IDs",
                f"{fmt(S.get('n_anomalous_hv_claims',0))} high-value claims ({crr(S.get('anomalous_exposure_cr',0))}) carry NULL or phone-like hospital IDs — probable ghost admissions.", "HIGH"))
for i, (name, finding, band) in enumerate(sig, 1):
    H.append(f'<tr><td>{i}</td><td><b>{e(name)}</b></td><td>{finding}</td><td>{risk_txt(band)}</td></tr>')
H.append("</tbody></table></div>")

# ===== CASE STUDIES =====
H.append('<div class="section">' + sec("Case Studies", "Representative flagged cases", "Drawn directly from the data; each is a lead for verification, not a verdict"))

def facts(rows):
    return '<table class="facts">' + "".join(f'<tr><td class="k">{e(k)}</td><td>{v}</td></tr>' for k, v in rows) + "</table>"

c = CASES.get("top_repeat_claimant")
if c:
    H.append('<div class="case"><div class="case-h">Case 1 — Chronic Repeat Claimant</div>' + facts([
        ("Beneficiary", f"{e(c['beneficiary'])} (card {e(c['card_id'])})"),
        ("Pattern", f"{c['claims']} high-value claims; {c['lockin_pct']}% at one login ({e(c['primary_hospital'])})"),
        ("Exposure", f"{crr(c['exposure_cr'])} claimed / {crr(c['approved_cr'])} approved ({c['ded_pct']}% deducted)"),
        ("Window", f"{e(c['first_admit'])} to {e(c['last_admit'])} (~{c['span_months']:.0f} months; on average one admission every {c['avg_interval_days']:.0f} days)"),
    ]) +
    f"<p>{e(c['beneficiary'])} filed <b>{c['claims']} separate high-value claims</b> in about {c['span_months']:.0f} months — "
    f"on average one admission every <b>{c['avg_interval_days']:.0f} days</b>. The low {c['ded_pct']}% deduction means most "
    f"claims pass audit, so the test is documentary: either a genuine chronic condition needing case management, or "
    f"manufactured admission episodes generating a fresh base fee each time.</p>"
    f'<p class="action"><b>Action:</b> pull discharge summaries for a 20-claim sample and reconcile admission dates / ICU notes (14 days).</p></div>')

g = CASES.get("ghost_repeat_claimant")
if g:
    H.append('<div class="case"><div class="case-h">Case 2 — Ghost-Hospital Repeat Claimant</div>' + facts([
        ("Beneficiary", f"{e(g['beneficiary'])} (card {e(g['card_id'])})"),
        ("Pattern", f"{g['claims']} high-value claims; primary hospital ID = {e(g['primary_hospital'])} (untraceable)"),
        ("Exposure", f"{crr(g['exposure_cr'])} claimed ({g['ded_pct']}% deducted)"),
    ]) +
    f"<p>Every one of {e(g['beneficiary'])}'s {g['claims']} high-value claims ({crr(g['exposure_cr'])}) carries no traceable "
    f"hospital ID — a classic <b>ghost-admission</b> pattern; the partial deduction shows the system flags but does not fully "
    f"reject them.</p>"
    f'<p class="action"><b>Action:</b> trace the servicing facility from settlement/bank records; if none exists, treat as fabricated (30 days).</p></div>')

d = CASES.get("top_duplicate")
if d:
    ids = ", ".join(str(x) for x in d.get("intimation_ids", []))
    H.append('<div class="case"><div class="case-h">Case 3 — Same-Day Duplicate Billing</div>' + facts([
        ("Beneficiary", f"{e(d['beneficiary'])} (card {e(d['card_id'])})"),
        ("Duplicate", f"{d['dup_count']} identical {inr(d['exposure'])} claims on {e(d['admission_date'])} at {e(d['hospital'])}"),
        ("Intimation IDs", e(ids) + ("  (near-consecutive)" if d.get("consecutive") else "")),
    ]) +
    f"<p>The same card, admission date and amount ({inr(d['exposure'])}) were submitted under {d['dup_count']} different "
    f"intimation IDs — the textbook signature of duplicate billing to collect reimbursement more than once.</p>"
    f'<p class="action"><b>Action:</b> confirm whether more than one submission was paid, recover the surplus, sweep the login for other duplicates (7 days).</p></div>')

cv = CASES.get("card_variation")
if cv:
    H.append('<div class="case"><div class="case-h">Case 4 — Possible Card-ID Manipulation</div>' + facts([
        ("Beneficiary", e(cv["beneficiary"])),
        ("Two cards", f"{e(cv['card_a'])} &nbsp;vs&nbsp; {e(cv['card_b'])} (differ by one character)"),
        ("Combined", f"{cv['claims']} high-value claims, {crr(cv['exposure_cr'])}, at {', '.join(e(h) for h in cv['hospitals'])}"),
    ]) +
    f"<p>The same beneficiary name appears on two card numbers that differ by a single character "
    f"(<b>{e(cv['card_a'])}</b> vs <b>{e(cv['card_b'])}</b>). This can indicate duplicate card issuance / card-ID "
    f"manipulation used to split a fraud trail — or, less likely, two distinct people sharing a common name. It is a "
    f"lead, not a conclusion.</p>"
    f'<p class="action"><b>Action:</b> verify both cards against the service record — one pensioner or two? (immediate).</p></div>')

b = CASES.get("top_bulk")
if b:
    H.append('<div class="case"><div class="case-h">Case 5 — Extreme Bulk Claim Injection</div>' + facts([
        ("Beneficiary", e(b["beneficiary"])),
        ("Event", f"{b['count']} intimation IDs in ONE day ({e(b['date'])}) at {e(b['hospital'])}"),
        ("ID range", f"{e(b['first_id'])} – {e(b['last_id'])}" + ("  (near-consecutive)" if b.get("consecutive") else "")),
        ("Tier", e(b["tier"])),
    ]) +
    f"<p><b>{b['count']} claim-intimation records created for one card on a single day</b> is far beyond manual web-portal "
    f"entry. The near-consecutive ID range is the signature of programmatic batch insertion — portal credential compromise "
    f"or insider database access, not ordinary claim fraud.</p>"
    f'<p class="action"><b>Action:</b> obtain portal access logs (IP/session/timestamps) for that date, suspend the login, escalate to ECHS IT / CERT-In (immediate).</p></div>')
H.append("</div>")

# ===== Q13a TOP CLAIMS =====
H.append('<div class="section">' + sec("Top High-Value Individual Claims", "Q13a · Claim-level",
         "Ranked by gross claimed (exposure). Ded% = (claimed − approved) / claimed"))
H.append('<div class="tcap">Table Q13a.1 — Top 30 high-value claims</div>')
H.append('<table class="dt">' + colgroup("13%", "23%", "14%", "12%", "20%", "11%", "7%") +
         th("Risk", "Beneficiary", "Hospital", "Admission", "Diagnosis", "Exposure", "Ded%") + "<tbody>")
for r in Q13A[:30]:
    dedc = f'<span class="red">{e(r["ded_pct"])}</span>' if float(r["ded_pct"]) >= 99 else e(r["ded_pct"])
    H.append(f'<tr><td>{score_cell(r)}</td><td>{short(r["beneficiary"],24)}</td><td>{short(r["hospital_code"],14)}</td>'
             f'<td>{e(str(r["admission_date"])[:10])}</td><td>{short(r["diagnosis"],30)}</td>'
             f'<td class="num">{inr(r["exposure"])}</td><td>{dedc}</td></tr>')
H.append("</tbody></table>")
if GHOST:
    H.append('<h2>Ghost &amp; anomalous-hospital claims</h2>')
    H.append('<p>High-value claims whose hospital ID is missing (NULL), a placeholder, or a phone number — i.e. no '
             'traceable provider. These are prime ghost-admission leads.</p>')
    H.append('<div class="tcap">Table Q13a.2 — Top ghost / anomalous-hospital claims</div>')
    H.append('<table class="dt">' + colgroup("26%", "18%", "16%", "15%", "16%", "9%") +
             th("Beneficiary", "Hospital ID", "Type", "Admission", "Exposure", "Ded%") + "<tbody>")
    for r in GHOST[:12]:
        H.append(f'<tr><td>{short(r["beneficiary"],24)}</td><td>{short(r["hospital_code"],16)}</td><td>{e(r["category"])}</td>'
                 f'<td>{e(str(r["admission_date"])[:10])}</td><td class="num">{inr(r["exposure"])}</td><td>{e(r["ded_pct"])}</td></tr>')
    H.append("</tbody></table>")
H.append("</div>")

# ===== Q13b HOSPITAL SCORECARD (TOP 20) =====
H.append('<div class="section">' + sec("Hospital Risk Scorecard — Top 20", "Q13b · Provider-level",
         "Logins with ≥10 high-value claims and avg deduction &gt; 25%, ranked by absolute deduction"))
H.append('<div class="tcap">Table Q13b.1 — Top 20 hospital logins by absolute deduction</div>')
H.append('<table class="dt">' + colgroup("6%", "13%", "18%", "11%", "13%", "13%", "10%", "16%") +
         th("Rank", "Login", "HV Claims", "Exposure", "Deducted", "Avg Ded%", "100% Ded", "Risk") + "<tbody>")
for i, r in enumerate(Q13B[:20], 1):
    avg = f'<span class="red">{e(r["avg_ded_pct"])}</span>' if float(r["avg_ded_pct"]) >= 50 else e(r["avg_ded_pct"])
    H.append(f'<tr><td>{i}</td><td><b>{short(r["hospital_code"],14)}</b></td><td class="num">{fmt(r["hv_claims"])}</td>'
             f'<td>{crr(r["exposure_cr"])}</td><td class="num">{crr(r["deducted_cr"])}</td><td>{avg}</td>'
             f'<td>{fmt(r["full_ded_claims"])}</td><td>{score_cell(r)}</td></tr>')
H.append("</tbody></table>")

# deep dives + polyclinic
if DEEP.get("hospitals"):
    H.append('<h2>Hospital deep-dives</h2>')
    for h in DEEP["hospitals"][:3]:
        names = ", ".join(f"{e(n['beneficiary'])} ({inr(n['exposure'])})" for n in h.get("named_full_ded", [])[:6])
        para = (f"<b>{e(h['hospital_code'])}</b> — {fmt(h['hv_claims'])} high-value claims, {crr(h['exposure_cr'])} exposure, "
                f"{crr(h['deducted_cr'])} deducted ({h['avg_ded_pct']}% average), of which <b>{h['full_ded_claims']}</b> were "
                f"approved at ₹0. ")
        if names:
            para += f"Beneficiaries with a 100% deduction here include {names}. "
        if h["full_ded_claims"] >= 5:
            para += ("Different beneficiaries at one login all hitting 100% deduction points to systematic billing above "
                     "the package ceiling rather than isolated patient fraud.")
        H.append(f'<div class="kf">{para}</div>')
poly = DEEP.get("polyclinic") or {}
if poly.get("claims"):
    tops = ", ".join(f"{e(x['hospital_code'])} ({x['avg_ded_pct']}%)" for x in poly.get("top_logins", [])[:5])
    H.append('<h2>ECHS polyclinic login pattern</h2>')
    H.append(f'<div class="kf">Login codes of the form <b>p.</b> / <b>pol.</b> (ECHS polyclinics) carry '
             f'{fmt(poly["claims"])} high-value claims with {crr(poly["deducted_cr"])} deducted at a {poly["avg_ded_pct"]}% '
             f'average — far above private-hospital norms' + (f". Highest-deduction polyclinic logins: {tops}" if tops else "") +
             '. Polyclinic credentials routing high-value IPD claims that are then almost entirely rejected suggests these '
             'internal channels are being used to bypass pre-authorisation controls.</div>')
H.append("</div>")

# ===== Q13c REGIONAL =====
H.append('<div class="section">' + sec("Regional Risk Distribution", "Q13c · Region-level",
         "From the pre-aggregated settlement statistics; a region-level proxy"))
regn = sorted(REG, key=lambda r: float(r.get("exposure_cr") or 0), reverse=True)
H.append('<div class="tcap">Table Q13c.1 — Regional claimed value and deduction rate (top 16 by exposure)</div>')
H.append('<table class="dt">' + colgroup("9%", "31%", "17%", "16%", "16%", "11%") +
         th("Region", "ECHS Command", "Claims", "Exposure", "Deducted", "Ded%") + "<tbody>")
for r in regn[:16]:
    dp = float(r["ded_pct"] or 0)
    dpc = f'<span style="color:#d4680a;font-weight:700">{e(r["ded_pct"])}</span>' if dp >= 15 else e(r["ded_pct"])
    H.append(f'<tr><td>{e(r["region_id"])}</td><td>{short(r["command"],26)}</td><td>{fmt(r["claim_cnt"])}</td>'
             f'<td>{crr(r["exposure_cr"])}</td><td class="num">{crr(r["deducted_cr"])}</td><td>{dpc}</td></tr>')
H.append("</tbody></table>")
if regn:
    hi_ded = max(regn, key=lambda r: float(r["ded_pct"] or 0)); hi_vol = regn[0]
    H.append('<h2>Regional implications</h2>')
    H.append(f'<p><b>{e(hi_ded["command"])}</b> shows the highest deduction rate ({e(hi_ded["ded_pct"])}%) — the command where '
             f'claim scrutiny removes the largest share of billed value. <b>{e(hi_vol["command"])}</b> carries the largest '
             f'absolute exposure ({crr(hi_vol["exposure_cr"])}): a concentration of high-volume hospital logins makes it the '
             f'biggest absolute leakage surface even at a moderate rate. High-deduction commands warrant a region-level audit '
             f'of their top high-value hospitals.</p>')
H.append("</div>")

# ===== Q13d CHRONIC =====
H.append('<div class="section">' + sec("Chronic Repeat High-Value Claimants", "Q13d · Beneficiary-level",
         "Cards with ≥3 high-value claims, ranked by total exposure. Lock-in = share at a single login"))
H.append('<div class="tcap">Table Q13d.1 — Top 20 chronic repeat claimants</div>')
H.append('<table class="dt">' + colgroup("12%", "19%", "16%", "8%", "12%", "12%", "13%", "8%") +
         th("Risk", "Beneficiary", "Card", "Claims", "Exposure", "Deducted", "Primary Hosp", "Lock-in") + "<tbody>")
for r in Q13D[:20]:
    H.append(f'<tr><td>{score_cell(r)}</td><td>{short(r["beneficiary"],20)}</td><td>{short(r["card_id"],16)}</td>'
             f'<td class="num">{fmt(r["hv_claims"])}</td><td>{crr(r["exposure_cr"])}</td><td class="num">{crr(r["deducted_cr"])}</td>'
             f'<td>{short(r["primary_hospital"],12)}</td><td>{round(float(r["lockin"])*100)}%</td></tr>')
H.append("</tbody></table>")
le = CASES.get("lockin_examples")
if le:
    ex = "; ".join(f"{e(x['beneficiary'])} ({x['claims']} claims, {x['lockin_pct']}% at {e(x['hospital'])})" for x in le)
    H.append('<h2>Single-hospital lock-in</h2>')
    H.append(f'<p>Natural medical histories spread across providers. Near-perfect single-hospital concentration over dozens '
             f'of high-value admissions is the strongest repeat-claimant signal — it points to a fixed beneficiary-hospital '
             f'relationship that should be examined for any financial arrangement. Examples: {ex}.</p>')
H.append("</div>")

# ===== Q13f BULK =====
H.append('<div class="section">' + sec("Extreme Bulk Claim Injection", "Q13f · System-level",
         "Hundreds of intimation IDs for one card on one day. Tiers: &gt;300 = system compromise, 100–300 = account abuse, 50–100 = watch"))
H.append('<div class="tcap">Table Q13f.1 — Bulk-injection events (same-day mass intimation)</div>')
H.append('<table class="dt">' + colgroup("20%", "17%", "13%", "12%", "10%", "18%", "10%") +
         th("Beneficiary", "Card", "Hospital", "Date", "Intim.", "ID Range", "Tier") + "<tbody>")
for r in BULK[:16]:
    tcol = {"SYSTEM COMPROMISE": "#c0392b", "ACCOUNT ABUSE": "#d4680a"}.get(r["tier"], "#7f8c8d")
    H.append(f'<tr><td>{short(r["beneficiary"],20)}</td><td>{short(r["card_id"],16)}</td><td>{short(r["hospital_code"],12)}</td>'
             f'<td>{e(str(r["creation_date"])[:10])}</td><td class="red">{fmt(r["intimation_count"])}</td>'
             f'<td>{e(r["first_intimation_id"])}–{e(r["last_intimation_id"])}</td>'
             f'<td><span style="color:{tcol};font-weight:700">{e(r["tier"])}</span></td></tr>')
H.append("</tbody></table>")
tb = CASES.get("top_bulk"); spread = CASES.get("bulk_spread")
H.append('<h2>Why this matters</h2>')
if tb:
    H.append(f'<p>The top event — <b>{e(tb["beneficiary"])}</b> at <b>{e(tb["hospital"])}</b> on {e(tb["date"])} — created '
             f'<b>{tb["count"]} intimation IDs in a single day</b>'
             + (f', spanning IDs {e(tb["first_id"])}–{e(tb["last_id"])} (near-consecutive). ' if tb.get("consecutive") else ". ")
             + 'Creating hundreds of records in one day is impossible through manual web-portal entry; near-consecutive ID '
             'ranges are the signature of programmatic batch insertion — portal credential compromise or insider database '
             'access, not ordinary claim fraud.</p>')
if spread and spread.get("prefixes"):
    known = [p["region"] for p in spread["prefixes"] if p["region"]]
    rtxt = (", including " + ", ".join(known[:5])) if known else ""
    H.append(f'<p>These {spread["n_events"]} events span <b>{len(spread["prefixes"])} distinct card-prefix codes</b> (each '
             f'encoding an issuing ECHS region{rtxt}) — so this is not a single compromised login but a multi-region pattern. '
             f'Response: pull portal access logs (IP, session, timestamps) for these dates and escalate to ECHS IT / CERT-In.</p>')
H.append("</div>")

# ===== CONCLUSIONS =====
H.append('<div class="section">' + sec("Conclusions"))
H.append(f"""<p class="lead">Across the last five years, <b>{fmt(S.get('total_hv_claims',0))} claims above ₹5 lakh</b>
represent <b>{crr(S.get('total_exposure_cr',0))}</b> of gross exposure, of which <b>{crr(S.get('total_deducted_cr',0))}
({S.get('overall_ded_pct',0)}%)</b> was removed at audit — a deduction rate far above routine norms and evidence that
high-value billing is systematically inflated.</p>""")
H.append(f"""<p>The single largest issue is <b>data integrity</b>: {fmt(S.get('n_anomalous_hv_claims',0))} high-value claims
({crr(S.get('anomalous_exposure_cr',0))}) carry no traceable hospital ID. Fraud then concentrates in three places —
<b>providers</b> (a handful of logins and the ECHS-polyclinic channel drive most of the absolute deduction),
<b>beneficiaries</b> (chronic claimants with extreme admission frequency and near-total single-hospital lock-in), and a
<b>system-security</b> exposure (same-day bulk injection of hundreds of intimation IDs across multiple regions, indicating
credential compromise rather than ordinary fraud).</p>""")
H.append("""<p>The composite risk score turns these signals into a single ranked queue, so auditors can act on the
CRITICAL/HIGH tier first. Because every score is a transparent weighted sum, each ranking can be explained and defended.
None of these findings is a conviction — they are prioritised leads, and each must be confirmed against physical records
(discharge summaries, portal access logs, service records) before recovery or enforcement.</p>""")
H.append("</div>")

# ===== RISK REGISTER + RECOMMENDATIONS =====
H.append('<div class="section">' + sec("Consolidated Risk Register &amp; Recommendations"))
H.append('<div class="tcap">Table R.1 — Risk register</div>')
H.append('<table class="dt">' + colgroup("34%", "20%", "30%", "16%") +
         th("Fraud signal", "Scale", "Exposure", "Risk") + "<tbody>")
reg_rows = [
    ("High-value claims (&gt;₹5L)", f"{fmt(S.get('total_hv_claims',0))} claims", crr(S.get('total_exposure_cr',0)), "CRITICAL"),
    ("100% deduction claims", f"{fmt(S.get('full_deduction_hv_claims',0))} claims", "billed beyond ceiling", "CRITICAL"),
    ("Hospital overcharging (&gt;25% ded)", f"{fmt(S.get('n_flagged_hospitals',0))} logins", "see scorecard", "CRITICAL"),
    ("ECHS polyclinic abuse", f"{fmt(S.get('n_polyclinic_claims',0))} claims", crr(S.get('polyclinic_deducted_cr',0)) + " deducted", "HIGH"),
    ("Chronic repeat claimants", f"{fmt(S.get('n_chronic_claimants',0))} cards", "≥3 high-value claims", "HIGH"),
    ("Same-day duplicates", f"{fmt(S.get('n_duplicate_groups',0))} groups", "double billing", "CRITICAL"),
    ("Bulk claim injection", f"{fmt(S.get('n_bulk_events',0))} events", f"{S.get('n_bulk_system_compromise',0)} system-compromise", "CRITICAL"),
    ("Ghost / anomalous hospital IDs", f"{fmt(S.get('n_anomalous_hv_claims',0))} claims", crr(S.get('anomalous_exposure_cr',0)), "HIGH"),
]
for sgnl, scale, exp, rk in reg_rows:
    H.append(f'<tr><td><b>{sgnl}</b></td><td>{scale}</td><td>{exp}</td><td>{risk_txt(rk)}</td></tr>')
H.append("</tbody></table>")

H.append('<div class="tcap" style="margin-top:6px">Table R.2 — Strategic recommendations (priority · SLA · named case)</div>')
H.append('<table class="dt">' + colgroup("11%", "11%", "30%", "48%") +
         th("Priority", "SLA", "Recommendation", "Action") + "<tbody>")
tb = CASES.get("top_bulk"); rc = CASES.get("top_repeat_claimant"); du = CASES.get("top_duplicate"); cv = CASES.get("card_variation")
hosp = (DEEP.get("hospitals") or [None])[0]
recs = []
if tb:
    recs.append(("CRITICAL", "Immediate", "Portal-security investigation of bulk injection",
                 f"{e(tb['beneficiary'])} created {tb['count']} intimation IDs in one day at {e(tb['hospital'])}. Pull portal access logs for all {fmt(S.get('n_bulk_events',0))} events, suspend the logins, escalate to ECHS IT / CERT-In."))
if du:
    recs.append(("CRITICAL", "7 days", "Recover same-day duplicate payments",
                 f"{e(du['beneficiary'])}: {du['dup_count']} identical {inr(du['exposure'])} claims on {e(du['admission_date'])} at {e(du['hospital'])}. Confirm which were paid, recover the surplus, sweep the login."))
if rc:
    recs.append(("CRITICAL", "14 days", "Physically verify the top chronic claimant",
                 f"{e(rc['beneficiary'])} — {rc['claims']} high-value claims at {e(rc['primary_hospital'])}. Obtain discharge summaries for a 20-claim sample; reconcile admission dates / ICU notes."))
if cv:
    recs.append(("CRITICAL", "Immediate", "Investigate possible card-ID manipulation",
                 f"{e(cv['beneficiary'])} on two near-identical cards ({e(cv['card_a'])} / {e(cv['card_b'])}). Verify against the service record — one pensioner or two?"))
if hosp:
    recs.append(("HIGH", "60 days", "Empanelment &amp; billing audit of top-deduction login",
                 f"{e(hosp['hospital_code'])} — {crr(hosp['deducted_cr'])} deducted across {fmt(hosp['hv_claims'])} claims ({hosp['full_ded_claims']} at 100%). Audit package rates and a 10-claim line-item sample."))
recs.append(("HIGH", "60 days", "Segregate ECHS polyclinic claim channels",
             f"Polyclinic logins carry {fmt(S.get('n_polyclinic_claims',0))} high-value claims. Restrict them to OPD/pharmacy; quarantine high-value IPD claims submitted through them."))
recs.append(("HIGH", "30 days", "Reject invalid hospital identifiers at intake",
             f"{fmt(S.get('n_anomalous_hv_claims',0))} claims ({crr(S.get('anomalous_exposure_cr',0))}) carry NULL/phone-like IDs. Block submission where the hospital ID is not a valid portal login."))
recs.append(("MEDIUM", "Ongoing", "Operationalise the risk score",
             "Run the composite score nightly and route CRITICAL-band claims to auditors before settlement."))
for pr, sla, t1, t2 in recs:
    H.append(f'<tr><td>{risk_txt(pr)}</td><td>{sla}</td><td><b>{t1}</b></td><td>{t2}</td></tr>')
H.append("</tbody></table>")
H.append('<div class="callout" style="margin-top:10px"><b>This report is produced by an automated screening system.</b> '
         'Every flagged case is an investigative lead, not a confirmed finding, and must be reviewed by a qualified auditor '
         'before any action is taken.</div>')
H.append('<p style="text-align:center;font-size:7.5pt;color:#777;margin-top:10px">Prepared by IIT Kanpur — Data Analytics &amp; '
         f'Fraud Intelligence Division &nbsp;|&nbsp; {today_str} &nbsp;|&nbsp; RESTRICTED</p>')
H.append("</div>")

H.append("</body></html>")

# ---- render ----------------------------------------------------------------
def main():
    full = "\n".join(H)
    html_path = os.path.join(REPORTS, "_module13_report.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full)
    HTML(string=full, base_url=BASE).write_pdf(OUT)
    print(f"PDF saved: {OUT}")
    print(f"HTML saved: {html_path}  ({len(full):,} bytes)")


if __name__ == "__main__":
    main()
