#!/usr/bin/env python3
"""
ECHS Module 14 - Pre-Authorization Deviation : derive datasets + charts.

Reads module_14/data/up_base.csv (every unlisted_procedure row, last 5y, joined
to its claim) + q14b_*.csv + type1_preauth.csv, and produces report-ready CSVs,
a summary/cases JSON, and matplotlib charts.

Pre-auth deviation logic (Type-2 / unlisted_procedure):
  * dedup revised rows: keep latest UP_PROCESS_DATE per (claim, procedure)
  * per claim: sanction = SUM(UP_SANC_TOTAL); billed = CS_GR_CLAIM_AMT; uti = CS_UTI_APP_AMT
  * matched = claims with sanction>0 AND billed>0
  * bill/sanction ratio = billed/sanction ; excess = billed - sanction ; breach = ratio > 1.25
  CAVEAT (carried into the report): a ratio >1 is structurally expected because the
  pre-auth sanction covers only the unlisted procedure, not the whole admission. Flag
  EXTREME + CONSISTENT ratios, not every ratio >1. No ML; scores are transparent.
"""
import os
import csv
import json
import math

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "module_14", "data")
CHARTS = os.path.join(HERE, "module_14", "charts")
os.makedirs(CHARTS, exist_ok=True)

CRORE, LAKH = 1e7, 1e5
BREACH = 1.25                      # >25% above sanction
MIN_HOSP_CLAIMS = 20               # min matched claims for a hospital to be scored
NAVY, GOLD, RED = "#1a2744", "#c9a84c", "#c0392b"
BANDS = [(70, "CRITICAL"), (45, "HIGH"), (0, "MEDIUM")]
HOSPITAL_WEIGHTS = {"excess_magnitude": 35, "avg_ratio": 30, "breach_rate": 20, "volume": 15}


def band(s):
    for cut, lab in BANDS:
        if s >= cut:
            return lab
    return "MEDIUM"


def fy(ts):
    if pd.isna(ts):
        return None
    y = ts.year
    return f"FY{y}-{str(y+1)[-2:]}" if ts.month >= 4 else f"FY{y-1}-{str(y)[-2:]}"


def load_base():
    df = pd.read_csv(os.path.join(DATA, "up_base.csv"), dtype=str, keep_default_na=False)
    for c in ("UP_ESTIMATE_COST", "UP_SANC_TOTAL", "UP_TOTAL_COST", "CS_GR_CLAIM_AMT", "CS_UTI_APP_AMT"):
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)
    for c in ("UP_PROCESS_DATE", "UP_APPLY_DATE", "CI_CR_DATE"):
        df[c] = pd.to_datetime(df[c], errors="coerce")
    df["hospital"] = df["hospital"].replace("", "(unmapped office)").fillna("(unmapped office)")
    return df


def per_claim(df):
    # keep the latest revision per (claim, procedure)
    d = df.sort_values("UP_PROCESS_DATE", na_position="first") \
          .drop_duplicates(subset=["UP_CLAIM_ID", "UP_PROCEDURE"], keep="last")
    g = d.groupby("UP_CLAIM_ID").agg(
        hospital=("hospital", "first"), beneficiary=("CI_BENEFICIARY_NAME", "first"),
        card_id=("CI_CARD_ID", "first"), cr_date=("CI_CR_DATE", "first"),
        ailment=("CI_ADM_AILMENT", "first"), procedures=("UP_PROCEDURE", "nunique"),
        sanction=("UP_SANC_TOTAL", "sum"), estimate=("UP_TOTAL_COST", "sum"),
        billed=("CS_GR_CLAIM_AMT", "first"), uti=("CS_UTI_APP_AMT", "first"),
        apply_date=("UP_APPLY_DATE", "min"),
    ).reset_index()
    return g


def matched_claims(g):
    m = g[(g["sanction"] > 0) & (g["billed"] > 0)].copy()
    m["ratio"] = m["billed"] / m["sanction"]
    m["excess"] = m["billed"] - m["sanction"]
    m["breach"] = (m["ratio"] > BREACH).astype(int)
    m["fy"] = m["cr_date"].map(fy)
    return m


def build_q14a(m):
    h = m.groupby("hospital").agg(
        claims=("UP_CLAIM_ID", "size"), sanction=("sanction", "sum"),
        billed=("billed", "sum"), uti=("uti", "sum"),
        excess=("excess", lambda s: float(s[s > 0].sum())), breaches=("breach", "sum"),
    ).reset_index()
    h["sanction_cr"] = (h["sanction"] / CRORE).round(2)
    h["billed_cr"] = (h["billed"] / CRORE).round(2)
    h["excess_cr"] = (h["excess"] / CRORE).round(2)
    h["avg_ratio"] = (h["billed"] / h["sanction"]).round(2)
    h["disallow_pct"] = np.where(h["billed"] > 0, (h["billed"] - h["uti"]) / h["billed"] * 100, 0).round(1)
    h["breach_rate"] = (h["breaches"] / h["claims"]).round(3)
    f = h[h["claims"] >= MIN_HOSP_CLAIMS].copy()
    max_ex = max(f["excess_cr"].max(), 1e-9) if len(f) else 1.0
    max_vol = max(f["claims"].max(), 1) if len(f) else 1
    f["risk_score"] = (
        (f["excess_cr"] / max_ex).clip(0, 1) * HOSPITAL_WEIGHTS["excess_magnitude"]
        + ((f["avg_ratio"].clip(1, 15) - 1) / 14) * HOSPITAL_WEIGHTS["avg_ratio"]
        + f["breach_rate"].clip(0, 1) * HOSPITAL_WEIGHTS["breach_rate"]
        + (np.log1p(f["claims"]) / math.log1p(max_vol)) * HOSPITAL_WEIGHTS["volume"]
    ).round(1)
    f["risk_band"] = f["risk_score"].map(band)
    f = f.sort_values("excess_cr", ascending=False)
    cols = ["risk_score", "risk_band", "hospital", "claims", "sanction_cr", "billed_cr",
            "excess_cr", "avg_ratio", "disallow_pct", "breaches"]
    f[cols].head(40).to_csv(os.path.join(DATA, "q14a_hospital_deviation.csv"), index=False)
    return f


def build_q14c(m):
    e = m.groupby("fy").agg(claims=("UP_CLAIM_ID", "size"), sanction=("sanction", "sum"),
                            billed=("billed", "sum"), uti=("uti", "sum")).reset_index()
    e = e[e["fy"].notna()].copy()
    e["avg_sanction"] = (e["sanction"] / e["claims"]).round(0)
    e["avg_billed"] = (e["billed"] / e["claims"]).round(0)
    e["avg_uti"] = (e["uti"] / e["claims"]).round(0)
    e["ratio"] = (e["billed"] / e["sanction"]).round(2)
    e = e.sort_values("fy")
    e.to_csv(os.path.join(DATA, "q14c_escalation.csv"), index=False)
    return e


def build_top_claims(m):
    t = m.sort_values("excess", ascending=False).head(30).copy()
    t["sanction_l"] = (t["sanction"] / LAKH).round(2)
    t["billed_l"] = (t["billed"] / LAKH).round(2)
    t["excess_l"] = (t["excess"] / LAKH).round(2)
    t["ratio"] = t["ratio"].round(2)
    cols = ["beneficiary", "card_id", "hospital", "ailment", "sanction_l", "billed_l", "excess_l", "ratio"]
    t[cols].to_csv(os.path.join(DATA, "q14_top_claims.csv"), index=False)
    return t


def render_charts(m, q14a, q14c):
    plt.rcParams.update({"font.size": 10, "axes.edgecolor": "#888", "savefig.dpi": 150,
                         "figure.autolayout": True})

    # 1) FY cost escalation: avg sanction vs avg billed (Rs L) + ratio line
    if len(q14c):
        fig, ax = plt.subplots(figsize=(7.6, 3.4))
        x = np.arange(len(q14c)); w = 0.38
        ax.bar(x - w/2, q14c["avg_sanction"]/LAKH, w, label="Avg sanction (₹L)", color=GOLD)
        ax.bar(x + w/2, q14c["avg_billed"]/LAKH, w, label="Avg billed (₹L)", color=NAVY)
        ax.set_xticks(x); ax.set_xticklabels(q14c["fy"], rotation=0, fontsize=9)
        ax.set_ylabel("₹ Lakh / claim"); ax.legend(loc="upper left", fontsize=8, frameon=False)
        ax2 = ax.twinx()
        ax2.plot(x, q14c["ratio"], color=RED, marker="o", lw=2, label="Bill/Sanction ×")
        ax2.set_ylabel("Bill / Sanction (×)", color=RED); ax2.tick_params(axis="y", colors=RED)
        ax2.set_ylim(0, max(q14c["ratio"]) * 1.3)
        for xi, r in zip(x, q14c["ratio"]):
            ax2.annotate(f"{r:.2f}×", (xi, r), textcoords="offset points", xytext=(0, 6),
                         ha="center", fontsize=8, color=RED, fontweight="bold")
        ax.set_title("Cost escalation by financial year — sanction vs actual billed", fontsize=11, color=NAVY, fontweight="bold")
        fig.savefig(os.path.join(CHARTS, "escalation.png")); plt.close(fig)

    # 2) clustering histogram of per-claim sanction (highlight Rs 2L)
    s = m["sanction"].clip(0, 500000)
    fig, ax = plt.subplots(figsize=(7.6, 3.2))
    ax.hist(s, bins=50, color=NAVY, alpha=0.85)
    ax.axvline(200000, color=RED, ls="--", lw=1.6); ax.axvline(100000, color=GOLD, ls=":", lw=1.4); ax.axvline(300000, color=GOLD, ls=":", lw=1.4)
    ax.annotate("₹2 L spike", (200000, ax.get_ylim()[1]*0.9), color=RED, fontsize=9, fontweight="bold", ha="center")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v/LAKH:.0f}L"))
    ax.set_xlabel("Pre-auth sanction per claim"); ax.set_ylabel("Claims")
    ax.set_title("Pre-auth sanction clustering (formal thresholds ₹1L/₹3L dotted)", fontsize=11, color=NAVY, fontweight="bold")
    fig.savefig(os.path.join(CHARTS, "clustering.png")); plt.close(fig)

    # 3) top-10 hospitals by excess billed
    top = q14a.head(10).iloc[::-1]
    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    ax.barh([h[:34] for h in top["hospital"]], top["excess_cr"], color=NAVY)
    for i, v in enumerate(top["excess_cr"]):
        ax.annotate(f"₹{v:.0f} Cr", (v, i), textcoords="offset points", xytext=(4, 0), va="center", fontsize=8)
    ax.set_xlabel("Excess billed above sanction (₹ Cr)")
    ax.set_title("Top 10 hospitals by excess billed above pre-auth sanction", fontsize=11, color=NAVY, fontweight="bold")
    fig.savefig(os.path.join(CHARTS, "top_hospitals.png")); plt.close(fig)


def load_csv(name):
    p = os.path.join(DATA, name)
    return list(csv.DictReader(open(p, encoding="utf-8"))) if os.path.exists(p) else []


def main():
    base = load_base()
    g = per_claim(base)
    m = matched_claims(g)
    q14a = build_q14a(m)
    q14c = build_q14c(m)
    top = build_top_claims(m)
    render_charts(m, q14a, q14c)

    total_sanction_cr = round(float(m["sanction"].sum()) / CRORE, 2)
    total_billed_cr = round(float(m["billed"].sum()) / CRORE, 2)
    total_excess_cr = round(float(m.loc[m["excess"] > 0, "excess"].sum()) / CRORE, 2)
    total_uti_cr = round(float(m["uti"].sum()) / CRORE, 2)

    cov = (load_csv("q14b_coverage.csv") or [{}])[0]
    t1 = load_csv("type1_preauth.csv")
    t1_total = sum(int(r["claims"]) for r in t1) if t1 else 0
    t1_rej = sum(int(r["claims"]) for r in t1 if r.get("pa_approved") == "N")

    # cases
    cases = {}
    if len(q14a):
        r = q14a.iloc[0]
        cases["top_overbiller"] = {"hospital": r["hospital"], "claims": int(r["claims"]),
                                   "billed_cr": float(r["billed_cr"]), "excess_cr": float(r["excess_cr"]),
                                   "avg_ratio": float(r["avg_ratio"]), "breach_rate": float(r["breach_rate"]),
                                   "disallow_pct": float(r["disallow_pct"])}
        hr = q14a.sort_values("avg_ratio", ascending=False).iloc[0]
        cases["highest_ratio_hospital"] = {"hospital": hr["hospital"], "claims": int(hr["claims"]),
                                           "avg_ratio": float(hr["avg_ratio"]), "excess_cr": float(hr["excess_cr"])}
    if len(top):
        r = top.iloc[0]
        cases["top_excess_claim"] = {"beneficiary": r["beneficiary"], "hospital": r["hospital"],
                                     "sanction_l": float(r["sanction_l"]), "billed_l": float(r["billed_l"]),
                                     "excess_l": float(r["excess_l"]), "ratio": float(r["ratio"]),
                                     "ailment": str(r["ailment"])[:60]}
    if len(q14c) >= 2:
        cases["escalation"] = {"first_fy": q14c.iloc[0]["fy"], "first_ratio": float(q14c.iloc[0]["ratio"]),
                               "last_fy": q14c.iloc[-1]["fy"], "last_ratio": float(q14c.iloc[-1]["ratio"])}

    summary = {
        "scope": "Last 5 years (unlisted_procedure pre-auth, Dec 2021 onward)",
        "up_rows": int(len(base)), "preauth_claims": int(len(g)), "matched_claims": int(len(m)),
        "total_sanction_cr": total_sanction_cr, "total_billed_cr": total_billed_cr,
        "total_excess_cr": total_excess_cr, "total_uti_cr": total_uti_cr,
        "overall_ratio": round(total_billed_cr / total_sanction_cr, 2) if total_sanction_cr else 0,
        "breach_pct": round(float(m["breach"].mean()) * 100, 1) if len(m) else 0,
        "exceed_pct": round(float((m["ratio"] > 1.0).mean()) * 100, 1) if len(m) else 0,
        "median_ratio": round(float(m["ratio"].median()), 2) if len(m) else 0,
        "n_flagged_hospitals": int(len(q14a)),
        "band_dist": {b: int((q14a["risk_band"] == b).sum()) for b in ("CRITICAL", "HIGH", "MEDIUM")} if len(q14a) else {},
        "q14b": {"hv_claims": int(float(cov.get("hv_claims", 0) or 0)),
                 "hv_gross_cr": float(cov.get("hv_gross_cr", 0) or 0),
                 "no_preauth_claims": int(float(cov.get("no_preauth_claims", 0) or 0)),
                 "no_preauth_gross_cr": float(cov.get("no_preauth_gross_cr", 0) or 0)},
        "type1": {"total": t1_total, "rejected": t1_rej,
                  "rejected_pct": round(t1_rej / t1_total * 100, 1) if t1_total else 0,
                  "by_status": [{"status": r["pa_approved"], "claims": int(r["claims"]), "est_lakh": float(r["est_lakh"])} for r in t1]},
        "weights": HOSPITAL_WEIGHTS, "bands": {lab: cut for cut, lab in BANDS},
    }
    hv = summary["q14b"]["hv_claims"]
    summary["q14b"]["preauth_coverage_pct"] = round((hv - summary["q14b"]["no_preauth_claims"]) / hv * 100, 1) if hv else 0
    json.dump(summary, open(os.path.join(DATA, "module14_summary.json"), "w"), indent=2, default=str)
    json.dump(cases, open(os.path.join(DATA, "module14_cases.json"), "w"), indent=2, default=str)

    print("Built Module 14 datasets:")
    print(f"  unlisted-procedure rows (5y) : {len(base):,}")
    print(f"  distinct pre-auth claims     : {len(g):,}  (matched w/ sanction+bill: {len(m):,})")
    print(f"  total sanctioned             : Rs {total_sanction_cr:,.2f} Cr")
    print(f"  total billed (actual)        : Rs {total_billed_cr:,.2f} Cr   (overall {summary['overall_ratio']}x)")
    print(f"  excess billed above sanction : Rs {total_excess_cr:,.2f} Cr   ({summary['breach_pct']}% of claims breached >25%)")
    print(f"  flagged hospitals (>= {MIN_HOSP_CLAIMS} clm) : {len(q14a)}")
    if len(q14a):
        print("  top overbillers:", ", ".join(q14a["hospital"].head(4)))
    if "escalation" in cases:
        print(f"  bill/sanction trend          : {cases['escalation']['first_ratio']}x ({cases['escalation']['first_fy']}) -> {cases['escalation']['last_ratio']}x ({cases['escalation']['last_fy']})")
    print(f"  Q14b: {summary['q14b']['preauth_coverage_pct']}% of >Rs1L claims used the pre-auth channel")
    print(f"  charts -> {CHARTS}")


if __name__ == "__main__":
    main()
