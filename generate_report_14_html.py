#!/usr/bin/env python3
"""
ECHS Module 14 - Pre-Authorization Deviation : HTML + WeasyPrint report.

Same house style as generate_report_13_html.py (navy/gold cover, metric boxes,
gold left-bar section headers, CSS tables, key-findings boxes, running @page
header/footer) + embedded matplotlib charts. Reads module_14/data + charts.

Run:  build_module14_data.py  ->  this script.
"""
import os
os.environ.setdefault("DYLD_FALLBACK_LIBRARY_PATH", "/opt/homebrew/lib")

import csv
import json
import html
from datetime import date
from weasyprint import HTML

BASE = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.join(BASE, "module_14")
DATA = os.path.join(MOD, "data")
REPORTS = os.path.join(MOD, "reports")
os.makedirs(REPORTS, exist_ok=True)
OUT = os.path.join(REPORTS, "ECHS_Module14_PreAuth_Deviation_Report.pdf")
today_str = date.today().strftime("%d %B %Y")

def load_csv(n):
    p = os.path.join(DATA, n)
    return list(csv.DictReader(open(p, encoding="utf-8"))) if os.path.exists(p) else []

def load_json(n):
    p = os.path.join(DATA, n)
    return json.load(open(p)) if os.path.exists(p) else {}

S = load_json("module14_summary.json")
CASES = load_json("module14_cases.json")
Q14A = load_csv("q14a_hospital_deviation.csv")
Q14C = load_csv("q14c_escalation.csv")
TOP = load_csv("q14_top_claims.csv")
Q14BS = load_csv("q14b_sample.csv")
Q = S.get("q14b", {}); T1 = S.get("type1", {})

# ---- helpers (same as Module 13) -------------------------------------------
def e(t): return html.escape("" if t is None else str(t))
def fmt(n):
    try: return f"{int(float(n)):,}"
    except (TypeError, ValueError): return e(n)
def inr(v):
    try: v = float(v)
    except (TypeError, ValueError): return e(v)
    if v >= 1e7: return f"₹{v/1e7:.2f} Cr"
    if v >= 1e5: return f"₹{v/1e5:.2f} L"
    return f"₹{v:,.0f}"
def crr(v):
    try: return f"₹{float(v):,.2f} Cr"
    except (TypeError, ValueError): return e(v)
def lk(v):
    try: return f"₹{float(v):,.2f} L"
    except (TypeError, ValueError): return e(v)
def short(t, n=46):
    t = "" if t is None else str(t)
    return e(t if len(t) <= n else t[:n-1] + "…")
def risk_txt(b):
    c = {"CRITICAL": "#c0392b", "HIGH": "#d4680a", "MEDIUM": "#7f8c8d"}.get(str(b).upper(), "#27ae60")
    return f'<span style="color:{c};font-weight:700">{e(b)}</span>'
def th(*cols): return "<thead><tr>" + "".join(f"<th>{c}</th>" for c in cols) + "</tr></thead>"
def colgroup(*w): return "<colgroup>" + "".join(f'<col style="width:{x}"/>' for x in w) + "</colgroup>"

NAVY, GOLD = "#1a2744", "#c9a84c"
CSS = """
* { box-sizing:border-box; margin:0; padding:0; }
body { font-family:'DejaVu Sans',Arial,Helvetica,sans-serif; font-size:9pt; color:#222b36; line-height:1.5; }
@page { size:A4; margin:24mm 16mm 20mm 16mm;
  @top-left { content:"ECHS FRAUD ANALYTICS  ·  MODULE 14  ·  CONFIDENTIAL"; font-family:'DejaVu Sans'; font-size:7.5pt; font-weight:bold; color:#1a2744; }
  @top-right { content:"IIT Kanpur  ·  Page " counter(page); font-family:'DejaVu Sans'; font-size:7.5pt; color:#666; }
  @bottom-left { content:"RESTRICTED — For internal audit and investigative use only. Not for distribution."; font-family:'DejaVu Sans'; font-size:7pt; color:#777; }
  @bottom-right { content:"Generated: __DATE__"; font-family:'DejaVu Sans'; font-size:7pt; color:#777; } }
@page cover { margin:0; @top-left{content:none} @top-right{content:none} @bottom-left{content:none} @bottom-right{content:none} }
.cover { page:cover; background:#1a2744; width:210mm; height:297mm; position:relative; color:#fff; }
.cover-band-t,.cover-band-b { position:absolute; left:0; right:0; height:11px; background:#c9a84c; }
.cover-band-t { top:0; } .cover-band-b { bottom:0; }
.cover-in { position:absolute; left:24mm; right:24mm; top:50mm; text-align:center; }
.cover-gov { font-size:9pt; letter-spacing:1px; color:#aeb6c8; margin-bottom:32mm; }
.cover-kick { font-size:8.5pt; letter-spacing:3px; color:#c9a84c; font-weight:bold; margin-bottom:12px; }
.cover-title { font-size:31pt; font-weight:bold; letter-spacing:1px; line-height:1.1; margin-bottom:10px; }
.cover-sub { font-size:13pt; color:#cfd5e2; margin-bottom:6px; }
.cover-mod { font-size:9pt; letter-spacing:2px; color:#c9a84c; margin-bottom:24px; }
.cover-rule { width:62mm; height:2px; background:#c9a84c; margin:0 auto 26px auto; }
table.cover-boxes { margin:0 auto 30px auto; border-collapse:separate; border-spacing:6px; }
.cover-box { background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.16); padding:12px 14px; text-align:center; vertical-align:middle; }
.cover-box-l { font-size:6.5pt; color:#aeb6c8; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:6px; }
.cover-box-v { font-size:13pt; font-weight:bold; color:#fff; }
.cover-org { font-size:11pt; color:#c9a84c; font-weight:bold; margin-bottom:6px; }
.cover-date { font-size:8.5pt; color:#aeb6c8; }
.section { page-break-before:always; }
.sec { border-left:5px solid #c9a84c; padding:3px 0 3px 14px; margin:0 0 14px 0; page-break-after:avoid; }
table.sec-h { width:100%; border-collapse:collapse; }
.sec-h-l { vertical-align:middle; } .sec-h-r { vertical-align:middle; text-align:right; width:56mm; font-size:8pt; color:#8a90a0; font-style:italic; line-height:1.35; }
.sec-kick { font-size:7.5pt; font-weight:bold; letter-spacing:2px; color:#c9a84c; text-transform:uppercase; margin-bottom:4px; }
.sec-title { font-size:15pt; font-weight:bold; color:#1a2744; letter-spacing:0.3px; }
h2 { font-size:11pt; color:#1a2744; margin:16px 0 7px 0; page-break-after:avoid; }
p { margin-bottom:9px; text-align:justify; } b { font-weight:700; } .muted { color:#667; } .lead { margin-bottom:11px; }
table.metrics { width:100%; border-collapse:separate; border-spacing:6px; margin:6px 0 14px 0; }
.mbox { background:#1a2744; color:#fff; padding:14px 12px; text-align:center; vertical-align:middle; }
.mbox-l { font-size:6.8pt; color:#aeb6c8; text-transform:uppercase; letter-spacing:1px; margin-bottom:5px; }
.mbox-v { font-size:15.5pt; font-weight:bold; } .mbox-s { font-size:6.8pt; color:#aeb6c8; margin-top:4px; }
table.dt { width:100%; border-collapse:collapse; table-layout:fixed; margin:6px 0 16px 0; font-size:8pt; }
table.dt thead tr { background:#1a2744; color:#fff; }
table.dt thead th { padding:7px 9px; text-align:left; font-weight:700; font-size:7.8pt; border-bottom:2px solid #c9a84c; word-wrap:break-word; }
table.dt tbody td { padding:6px 9px; border-bottom:1px solid #e7e9ee; vertical-align:top; word-wrap:break-word; overflow-wrap:break-word; }
table.dt tbody tr:nth-child(even) { background:#f5f7fa; }
.tcap { font-size:7.5pt; color:#7a8190; margin:2px 0 4px 0; font-weight:bold; letter-spacing:0.4px; }
.num { font-weight:700; } .red { color:#c0392b; font-weight:700; }
.kf { background:#faf7ef; border-left:3px solid #c9a84c; padding:8px 12px; margin-bottom:8px; font-size:8.5pt; line-height:1.5; }
.kf-h { font-size:10.5pt; font-weight:bold; color:#1a2744; margin:12px 0 7px 0; }
.callout { background:#fdf1f1; border:1px solid #e7b8b8; border-left:4px solid #c0392b; padding:10px 13px; margin:8px 0 12px 0; font-size:8.5pt; } .callout b { color:#a02020; }
img.chart { width:100%; height:auto; border:1px solid #e2e5ec; margin:6px 0 14px 0; }
ol.acts { margin:4px 0 6px 18px; } ol.acts li { margin-bottom:6px; font-size:8.6pt; }
"""

H = [f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS.replace("__DATE__", today_str)}</style></head><body>']

def sec(title, kicker="", context=""):
    kick = f'<div class="sec-kick">{kicker}</div>' if kicker else ""
    return ('<div class="sec"><table class="sec-h"><tr>'
            f'<td class="sec-h-l">{kick}<div class="sec-title">{title}</div></td>'
            f'<td class="sec-h-r">{context}</td></tr></table></div>')

def mbox(l, v, s="", vc=""):
    st = f' style="color:{vc}"' if vc else ""
    return f'<td class="mbox"><div class="mbox-l">{l}</div><div class="mbox-v"{st}>{v}</div><div class="mbox-s">{s}</div></td>'

def facts(rows):
    return ('<table class="dt" style="font-size:8.2pt"><colgroup><col style="width:30mm"/><col/></colgroup><tbody>'
            + "".join(f'<tr><td style="font-weight:700;color:#1a2744">{e(k)}</td><td>{v}</td></tr>' for k, v in rows)
            + "</tbody></table>")

# ===== COVER =====
H.append(f"""
<div class="cover"><div class="cover-band-t"></div>
  <div class="cover-in">
    <div class="cover-gov">GOVERNMENT OF INDIA &nbsp;·&nbsp; EX-SERVICEMEN CONTRIBUTORY HEALTH SCHEME</div>
    <div class="cover-kick">FRAUD ANALYTICS &amp; INTELLIGENCE REPORT</div>
    <div class="cover-title">ECHS FRAUD ANALYTICS</div>
    <div class="cover-sub">Module 14 — Pre-Authorization Deviation</div>
    <div class="cover-mod">PRE-AUTH ESTIMATE vs ACTUAL BILLED &nbsp;|&nbsp; LAST 5 YEARS &nbsp;|&nbsp; COST ESCALATION &amp; CONTROL BYPASS</div>
    <div class="cover-rule"></div>
    <table class="cover-boxes"><tr>
      <td class="cover-box"><div class="cover-box-l">Pre-Auth Claims</div><div class="cover-box-v">{fmt(S.get('matched_claims',0))}</div></td>
      <td class="cover-box"><div class="cover-box-l">Gross Billed</div><div class="cover-box-v">{crr(S.get('total_billed_cr',0))}</div></td>
      <td class="cover-box"><div class="cover-box-l">Sanctioned</div><div class="cover-box-v">{crr(S.get('total_sanction_cr',0))}</div></td>
      <td class="cover-box"><div class="cover-box-l">Excess Billed</div><div class="cover-box-v">{crr(S.get('total_excess_cr',0))}</div></td>
      <td class="cover-box"><div class="cover-box-l">Bill / Sanction</div><div class="cover-box-v">{S.get('overall_ratio',0)}×</div></td>
    </tr></table>
    <div class="cover-org">IIT KANPUR — Data Analytics &amp; Fraud Intelligence Division</div>
    <div class="cover-date">{today_str} &nbsp;|&nbsp; Classification: RESTRICTED</div>
  </div><div class="cover-band-b"></div></div>""")

# ===== EXECUTIVE SUMMARY =====
H.append('<div class="section">' + sec("Executive Summary"))
H.append(f"""<p class="lead">Module 14 examines the <b>pre-authorization</b> control: the gap between what a hospital
declares (and ECHS sanctions) <i>before</i> treatment and what it actually <b>bills</b> afterwards. Over the last five
years, <b>{fmt(S.get('matched_claims',0))}</b> claims passed through the live unlisted-procedure pre-auth channel with
both a sanction and a final bill. They were sanctioned for <b>{crr(S.get('total_sanction_cr',0))}</b> but billed
<b>{crr(S.get('total_billed_cr',0))}</b> — an overall <b>{S.get('overall_ratio',0)}× </b> ratio and
<b>{crr(S.get('total_excess_cr',0))}</b> billed above sanction.""")
H.append('<table class="metrics"><tr>' +
         mbox("Gross Billed", crr(S.get('total_billed_cr',0)), "actual hospital bills") +
         mbox("Sanctioned", crr(S.get('total_sanction_cr',0)), "pre-auth approved") +
         mbox("Excess Billed", crr(S.get('total_excess_cr',0)), "above sanction", "#e74c3c") +
         mbox("Exceeded Sanction", f"{S.get('exceed_pct',0)}%", "of claims billed &gt; sanction") +
         mbox("Breach (&gt;25%)", f"{S.get('breach_pct',0)}%", "of claims") +
         '</tr></table>')
bd = S.get("band_dist", {})
H.append(f"""<p>By composite risk band, <b>{fmt(bd.get('CRITICAL',0)+bd.get('HIGH',0))}</b> hospital logins (of
{fmt(S.get('n_flagged_hospitals',0))} with ≥20 pre-auth claims) fall in the CRITICAL/HIGH tiers. The bill-to-sanction
ratio has risen steadily from {CASES.get('escalation',{}).get('first_ratio','?')}× to
{CASES.get('escalation',{}).get('last_ratio','?')}× across the period — a sustained escalation, not a one-off.</p>""")

H.append('<div class="kf-h">Patterns at a glance</div><table class="dt">' + colgroup("6%","27%","45%","13%","9%") +
         th("#","Pattern","What it detects","Metric","Risk") + "<tbody>")
pats = [
    ("1","Bill inflation above sanction","Hospitals billing far more than the pre-authorised amount",f"{S.get('exceed_pct',0)}% exceed","CRITICAL"),
    ("2","Excess billed","Total actual bill beyond what was sanctioned",crr(S.get('total_excess_cr',0)),"CRITICAL"),
    ("3","Hospital systematic overbilling","Specific logins with large, consistent excess",f"{fmt(S.get('n_flagged_hospitals',0))} logins","CRITICAL"),
    ("4","Cost escalation","Bill/sanction ratio rising year on year",f"{CASES.get('escalation',{}).get('first_ratio','?')}→{CASES.get('escalation',{}).get('last_ratio','?')}×","HIGH"),
    ("5","Rubber-stamp sanction","Sanction set equal to the hospital's own estimate (no scrutiny)","≈1.00× at stage 2","HIGH"),
    ("6","Pre-auth coverage gap","High-value claims not routed through pre-auth (context)",f"{S.get('q14b',{}).get('preauth_coverage_pct',0)}% covered","MEDIUM"),
]
for n,p,w,mtr,r in pats:
    H.append(f'<tr><td>{n}</td><td><b>{p}</b></td><td>{w}</td><td class="num">{mtr}</td><td>{risk_txt(r)}</td></tr>')
H.append("</tbody></table>")
H.append('<div class="kf-h">Immediate recommended actions</div><ol class="acts">')
for a in [
    f"<b>Audit the top-excess hospitals</b> ({fmt(S.get('n_flagged_hospitals',0))} logins ≥20 claims) — reconcile a sample of bills against their pre-auth sanctions and CGHS package rates.",
    "<b>Introduce partial sanction / CGHS benchmarking at Stage 2</b> — today the sanction simply equals the hospital's own estimate, so there is no financial gate.",
    f"<b>Investigate the steepest bill/sanction ratios</b> — they reached {CASES.get('escalation',{}).get('last_ratio','?')}× on average and far higher per claim.",
    "<b>Recover demonstrable overbilling</b> where the actual bill cannot be justified against the sanctioned, documented procedure.",
]:
    H.append(f"<li>{a}</li>")
H.append("</ol></div>")

# ===== PARAMETERS & METHODOLOGY =====
H.append('<div class="section">' + sec("Parameters &amp; Methodology", "How the analysis works"))
H.append("""<p class="lead"><b>Data.</b> The live pre-auth system (<b>unlisted_procedure</b>, Dec 2021 onward) joined to
its claim (<b>claim_intimation</b> for the treating hospital via office master, <b>claim_submission</b> for the actual
billed and UTI-approved amounts). Revised pre-auth rows are deduplicated to the latest per (claim, procedure), then
summed per claim.</p>
<p><b>Five-stage pipeline.</b> (1) hospital submits a pre-auth request with a cost estimate → (2) ECHS sanctions it
(in practice, at the declared estimate) → (3) hospital treats and submits the actual bill → (4) UTI audits and approves
→ (5) net payment. Module 14 measures the gap between the <b>Stage-2 sanction</b> and the <b>Stage-3 actual bill</b>.</p>""")
H.append('<div class="tcap">Table P.1 — Parameters &amp; definitions</div><table class="dt">' + colgroup("26%","74%") +
         th("Parameter","Definition") + "<tbody>")
for k, v in [
    ("Pre-auth sanction","SUM(UP_SANC_TOTAL) per claim — the amount ECHS authorised before treatment"),
    ("Actual billed","CS_GR_CLAIM_AMT — the gross amount the hospital billed after treatment"),
    ("Bill / Sanction ratio","actual billed ÷ pre-auth sanction (aggregate: total billed ÷ total sanction)"),
    ("Excess billed","actual billed − sanction, summed over claims that exceeded sanction"),
    ("Exceedance","share of claims with bill &gt; sanction (ratio &gt; 1.0)"),
    ("Breach","bill &gt; 1.25× sanction (the framework's '&gt;25% above estimate')"),
    ("Disallow %","(billed − UTI approved) / billed — the share the UTI audit later cut"),
    ("Matched claim","a pre-auth claim with both a sanction (&gt;0) and a final bill (&gt;0)"),
]:
    H.append(f'<tr><td><b>{e(k)}</b></td><td>{v}</td></tr>')
H.append("</tbody></table>")
H.append('<div class="kf-h">Hospital risk score — component weights (0–100, no ML)</div>')
H.append('<p>Bands: ' + risk_txt("CRITICAL") + ' ≥ 70, ' + risk_txt("HIGH") + ' 45–69, ' + risk_txt("MEDIUM") +
         ' &lt; 45. A plain weighted sum of normalised signals — fully reconstructable from the source rows.</p>')
H.append('<table class="dt">' + colgroup("74%","26%") + th("Component","Weight") + "<tbody>")
for k, v in (S.get("weights", {}) or {}).items():
    H.append(f'<tr><td>{e(k.replace("_"," ").title())}</td><td class="num">{v}</td></tr>')
H.append("</tbody></table></div>")

# ===== LIMITATIONS =====
H.append('<div class="section">' + sec("Limitations &amp; Assumptions"))
H.append('<div class="callout">')
for t in [
    "<b>A ratio above 1 is partly structural.</b> The pre-auth sanction covers only the <i>unlisted procedure</i>, while the final bill includes the whole admission (room, nursing, drugs, listed packages). So a bill above sanction is expected; what is anomalous is an <b>extreme and consistent</b> gap across many claims at one hospital.",
    "<b>Aggregate ratio, not mean-of-ratios.</b> We rank by absolute excess billed and report the aggregate bill/sanction ratio (total bill ÷ total sanction). Per-claim ratios can look far higher because some sanctions are tiny — we avoid that denominator inflation.",
    f"<b>Coverage, not bypass.</b> Only {S.get('q14b',{}).get('preauth_coverage_pct',0)}% of &gt;₹1L claims went through this pre-auth channel — because most are listed-package claims that do not require unlisted-procedure pre-auth. The {fmt(S.get('q14b',{}).get('no_preauth_claims',0))} 'no pre-auth' claims are a coverage observation, NOT a fraud count.",
    "<b>Identifiers, not verdicts.</b> Hospital/office names are identifiers; a high deduction or ratio is an investigative lead. Every case needs verification before any action.",
    "<b>Scope.</b> Primary analysis = last five years (Type-2 unlisted_procedure). The legacy pre_auth system (Type-1, 2012–2017) is summarised separately as historical context.",
]:
    H.append(f'<p style="margin-bottom:6px">• {t}</p>')
H.append('<p style="margin:0"><b>ALL CASES REQUIRE VERIFICATION BY QUALIFIED AUDITORS BEFORE ANY ACTION IS TAKEN.</b></p></div></div>')

# ===== COST ESCALATION (Q14c + charts) =====
H.append('<div class="section">' + sec("Cost Escalation", "Q14c · year-on-year", "Bill-to-sanction gap by financial year"))
H.append('<div class="tcap">Table Q14c.1 — Average sanction vs actual billed, by financial year</div>')
H.append('<table class="dt">' + colgroup("16%","13%","21%","21%","17%","12%") +
         th("FY","Claims","Avg Sanction","Avg Billed","Avg UTI Approved","Bill/Sanc") + "<tbody>")
for r in Q14C:
    H.append(f'<tr><td><b>{e(r["fy"])}</b></td><td class="num">{fmt(r["claims"])}</td>'
             f'<td>{inr(r["avg_sanction"])}</td><td class="num">{inr(r["avg_billed"])}</td>'
             f'<td>{inr(r["avg_uti"])}</td><td class="red">{e(r["ratio"])}×</td></tr>')
H.append("</tbody></table>")
H.append('<img class="chart" src="charts/escalation.png"/>')
H.append('<p>The average bill has pulled steadily away from the average sanction every year, while the sanction itself '
         'barely moves — consistent with hospitals treating the pre-auth as an entry token rather than a cost ceiling. '
         'Sanction amounts also cluster at round figures:</p>')
H.append('<img class="chart" src="charts/clustering.png"/>')
H.append('<p>The spike at ₹2 lakh is notable: it is <b>not</b> a formal ECHS threshold (₹1 L and ₹3 L are), yet it draws '
         'more sanctions than either — suggesting estimates are deliberately set just under the level that would trigger '
         'higher scrutiny.</p></div>')

# ===== Q14a HOSPITAL SCORECARD =====
H.append('<div class="section">' + sec("Hospital Deviation Scorecard — Top 20", "Q14a · Provider-level",
         "Pre-auth hospitals ranked by excess billed above sanction"))
H.append('<div class="tcap">Table Q14a.1 — Top 20 hospitals by excess billed</div>')
H.append('<table class="dt">' + colgroup("11%","30%","9%","12%","12%","11%","8%","7%") +
         th("Risk","Hospital","Claims","Billed","Excess","Avg B/S","Disallow","Breach") + "<tbody>")
for r in Q14A[:20]:
    H.append(f'<tr><td>{risk_txt(r["risk_band"])} <span style="color:#555">{e(r["risk_score"])}</span></td>'
             f'<td>{short(r["hospital"],40)}</td><td class="num">{fmt(r["claims"])}</td>'
             f'<td>{crr(r["billed_cr"])}</td><td class="num">{crr(r["excess_cr"])}</td>'
             f'<td class="red">{e(r["avg_ratio"])}×</td><td>{e(r["disallow_pct"])}%</td><td>{fmt(r["breaches"])}</td></tr>')
H.append("</tbody></table>")
H.append('<img class="chart" src="charts/top_hospitals.png"/>')
H.append('<h2>Hospital deep-dives</h2>')
for r in Q14A[:3]:
    H.append(f'<div class="kf"><b>{e(r["hospital"])}</b> — {fmt(r["claims"])} pre-auth claims, billed {crr(r["billed_cr"])} '
             f'against {crr(r["sanction_cr"])} sanctioned, i.e. <b>{crr(r["excess_cr"])} excess</b> (aggregate '
             f'{e(r["avg_ratio"])}× bill/sanction). The UTI audit later disallowed {e(r["disallow_pct"])}% of the billed '
             f'amount, and {fmt(r["breaches"])} of its claims breached the 25% threshold — a consistent, hospital-wide '
             f'pattern of billing well beyond the authorised estimate.</div>')
H.append("</div>")

# ===== TOP HIGH-DEVIATION CLAIMS =====
H.append('<div class="section">' + sec("Top High-Deviation Claims", "Q14a · Claim-level",
         "Individual claims with the largest gap between sanction and actual bill"))
H.append('<div class="tcap">Table Q14a.2 — Top 20 claims by excess billed above sanction</div>')
H.append('<table class="dt">' + colgroup("24%","16%","26%","12%","12%","10%") +
         th("Beneficiary","Card","Hospital","Sanctioned","Billed","B/S") + "<tbody>")
for r in TOP[:20]:
    H.append(f'<tr><td>{short(r["beneficiary"],22)}</td><td>{short(r["card_id"],16)}</td><td>{short(r["hospital"],28)}</td>'
             f'<td>{lk(r["sanction_l"])}</td><td class="num">{lk(r["billed_l"])}</td><td class="red">{e(r["ratio"])}×</td></tr>')
H.append("</tbody></table>")
H.append('<p class="muted" style="font-size:8pt">Note: a large gap can reflect a small unlisted-procedure sanction against '
         'a large whole-admission bill; these are leads for line-item verification, not confirmed overbilling.</p></div>')

# ===== Q14b COVERAGE =====
H.append('<div class="section">' + sec("Pre-Auth Coverage &amp; Control Bypass", "Q14b · context",
         "How much of the high-value claim flow actually passes through pre-auth"))
H.append(f"""<p class="lead">Of <b>{fmt(Q.get('hv_claims',0))}</b> high-value claims (&gt;₹1 lakh) in the last five years
({crr(Q.get('hv_gross_cr',0))} gross), only <b>{S.get('q14b',{}).get('preauth_coverage_pct',0)}%</b> went through the
unlisted-procedure pre-auth channel. The remaining <b>{fmt(Q.get('no_preauth_claims',0))}</b> ({crr(Q.get('no_preauth_gross_cr',0))})
carry no pre-auth record.</p>""")
H.append('<div class="callout"><b>Read this as coverage, not fraud.</b> ECHS pre-auth (unlisted procedure) is required '
         'only for specific non-package procedures; the vast majority of high-value claims are listed-package admissions '
         'that legitimately need no pre-auth. The figure simply shows how narrow the pre-auth net is — and therefore how '
         'few high-value claims are subject to any pre-treatment cost check.</div>')
if Q14BS:
    H.append('<div class="tcap">Table Q14b.1 — Largest high-value claims with no pre-auth record (sample)</div>')
    H.append('<table class="dt">' + colgroup("26%","16%","26%","16%","16%") +
             th("Beneficiary","Card","Hospital","Billed","UTI Approved") + "<tbody>")
    for r in Q14BS[:12]:
        H.append(f'<tr><td>{short(r["CI_BENEFICIARY_NAME"],22)}</td><td>{short(r["CI_CARD_ID"],16)}</td>'
                 f'<td>{short(r.get("hospital",""),28)}</td><td class="num">{inr(r["CS_GR_CLAIM_AMT"])}</td>'
                 f'<td>{inr(r["CS_UTI_APP_AMT"])}</td></tr>')
    H.append("</tbody></table>")
H.append("</div>")

# ===== TYPE-1 HISTORICAL NOTE =====
H.append('<div class="section">' + sec("Legacy Pre-Auth System (Type-1) — Historical Note", "2012–2017",
         "The discontinued pre_auth table, for context"))
H.append(f"""<p>Before the current system, ECHS ran a separate <b>pre_auth</b> table (2012–2017, now discontinued). It held
just <b>{fmt(T1.get('total',0))}</b> records, of which <b>{T1.get('rejected_pct',0)}%</b> were marked rejected
(PA_APPROVED = N) — yet historical analysis showed rejected pre-auths were still settled and paid at almost the same rate
as approved ones. In other words, the legacy approval gate had little bearing on payment. It is included here only as
historical context; the last-five-year analysis above is based entirely on the live unlisted-procedure system.</p>""")
if T1.get("by_status"):
    H.append('<div class="tcap">Table T1.1 — Legacy pre_auth decisions (2012–2017)</div>')
    H.append('<table class="dt">' + colgroup("34%","33%","33%") + th("Decision","Claims","Est. cost (₹L)") + "<tbody>")
    lbl = {"N": "N — Rejected", "Y": "Y — Approved", "X": "X — Cancelled"}
    for r in T1["by_status"]:
        H.append(f'<tr><td>{e(lbl.get(r["status"], r["status"]))}</td><td class="num">{fmt(r["claims"])}</td><td>₹{float(r["est_lakh"]):,.2f} L</td></tr>')
    H.append("</tbody></table>")
H.append("</div>")

# ===== CONCLUSIONS =====
H.append('<div class="section">' + sec("Conclusions"))
H.append(f"""<p class="lead">The pre-authorization control, as currently operated, does not constrain cost. Across
{fmt(S.get('matched_claims',0))} pre-auth claims in the last five years, hospitals billed
<b>{crr(S.get('total_billed_cr',0))}</b> against <b>{crr(S.get('total_sanction_cr',0))}</b> sanctioned —
<b>{crr(S.get('total_excess_cr',0))}</b> in excess, with <b>{S.get('exceed_pct',0)}%</b> of claims billed above their
sanction.</p>""")
H.append("""<p>The root cause is structural: ECHS sanctions at the hospital's own declared estimate, with no partial
sanction, CGHS benchmarking or cost negotiation at Stage 2. The pre-auth therefore functions as an entry token, not a
ceiling — and the gap has widened every year. The concentration of excess at a small set of hospitals, and the deliberate
clustering of estimates just under scrutiny thresholds, are the clearest leads for audit.</p>""")
H.append("""<p>The fix is a financial gate at Stage 2 (partial sanction against CGHS/package rates), backed by post-hoc
audit of the top-excess hospitals. As always, these are prioritised leads — each must be confirmed against itemised bills
and clinical records before recovery or enforcement.</p></div>""")

# ===== RISK REGISTER + RECOMMENDATIONS =====
H.append('<div class="section">' + sec("Consolidated Risk Register &amp; Recommendations"))
H.append('<div class="tcap">Table R.1 — Risk register</div><table class="dt">' + colgroup("36%","24%","24%","16%") +
         th("Signal","Scale","Exposure","Risk") + "<tbody>")
for sg, sc, ex, rk in [
    ("Excess billed above sanction", f"{S.get('exceed_pct',0)}% of claims", crr(S.get('total_excess_cr',0)), "CRITICAL"),
    ("Hospital systematic overbilling", f"{fmt(S.get('n_flagged_hospitals',0))} logins", "see scorecard", "CRITICAL"),
    ("Cost escalation (year on year)", f"{CASES.get('escalation',{}).get('first_ratio','?')}→{CASES.get('escalation',{}).get('last_ratio','?')}×", "widening gap", "HIGH"),
    ("Rubber-stamp sanction (Stage 2)", "≈1.00× sanction:estimate", "no financial gate", "HIGH"),
    ("Pre-auth coverage gap", f"{S.get('q14b',{}).get('preauth_coverage_pct',0)}% of &gt;₹1L covered", crr(Q.get('no_preauth_gross_cr',0)) + " outside", "MEDIUM"),
    ("Legacy approval gate (Type-1)", f"{T1.get('rejected_pct',0)}% rejected yet paid", "historical", "MEDIUM"),
]:
    H.append(f'<tr><td><b>{sg}</b></td><td>{sc}</td><td>{ex}</td><td>{risk_txt(rk)}</td></tr>')
H.append("</tbody></table>")

ov = CASES.get("top_overbiller", {}); esc = CASES.get("escalation", {})
H.append('<div class="tcap" style="margin-top:6px">Table R.2 — Strategic recommendations (priority · SLA · target)</div>')
H.append('<table class="dt">' + colgroup("11%","12%","30%","47%") + th("Priority","SLA","Recommendation","Action") + "<tbody>")
recs = [
    ("CRITICAL","30 days","Audit the top-excess hospital",
     f"{e(ov.get('hospital',''))} — billed {crr(ov.get('billed_cr',0))} vs sanctioned, {crr(ov.get('excess_cr',0))} excess ({ov.get('avg_ratio','?')}×). Reconcile a 25-claim line-item sample against sanctioned procedures and CGHS rates."),
    ("CRITICAL","60 days","Install a financial gate at Stage 2",
     "Replace rubber-stamp sanctioning (sanction = estimate) with partial sanction against CGHS/package benchmarks and a documented cost-negotiation step."),
    ("HIGH","60 days","Profile the top-20 deviation hospitals",
     f"All {fmt(S.get('n_flagged_hospitals',0))} logins with ≥20 pre-auth claims and high excess — empanelment review + billing audit; suspend the worst pending audit."),
    ("HIGH","90 days","Investigate estimate clustering at ₹2 L",
     "The ₹2-lakh spike is not a formal threshold; review why estimates bunch there and whether it is used to stay under scrutiny limits."),
    ("MEDIUM","Ongoing","Widen pre-auth coverage of high-value claims",
     f"Only {S.get('q14b',{}).get('preauth_coverage_pct',0)}% of &gt;₹1L claims pass any pre-treatment check; extend pre-auth to more high-cost admissions."),
    ("MEDIUM","Ongoing","Operationalise the deviation score",
     "Recompute the hospital deviation score each cycle and route CRITICAL-band hospitals to audit before settlement."),
]
for pr, sla, t1, t2 in recs:
    H.append(f'<tr><td>{risk_txt(pr)}</td><td>{sla}</td><td><b>{t1}</b></td><td>{t2}</td></tr>')
H.append("</tbody></table>")
H.append('<div class="callout" style="margin-top:10px"><b>This report is produced by an automated screening system.</b> '
         'Every flagged case is an investigative lead, not a confirmed finding, and must be reviewed by a qualified auditor '
         'before any action is taken.</div>')
H.append(f'<p style="text-align:center;font-size:7.5pt;color:#777;margin-top:10px">Prepared by IIT Kanpur — Data Analytics &amp; '
         f'Fraud Intelligence Division &nbsp;|&nbsp; {today_str} &nbsp;|&nbsp; RESTRICTED</p></div>')

H.append("</body></html>")


def main():
    full = "\n".join(H)
    open(os.path.join(REPORTS, "_module14_report.html"), "w", encoding="utf-8").write(full)
    HTML(string=full, base_url=MOD).write_pdf(OUT)
    print(f"PDF saved: {OUT}")


if __name__ == "__main__":
    main()
