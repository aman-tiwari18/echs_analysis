#!/usr/bin/env python3
"""
ECHS Module 13 - derive report-ready datasets + composite risk scores.

Reads the raw extracts produced by analyze_point13.py:
    module_13/data/high_value_claims_base.csv   (every claim > Rs 5 lakh gross)
    module_13/data/q13c_regional.csv
    module_13/data/q13f_bulk_injection.csv

Writes processed, report-ready CSVs + a headline-metrics JSON:
    q13a_top_claims.csv          top 200 high-value claims + claim risk score
    q13a2_duplicates.csv         same card+date+amount, multiple intimation IDs
    q13b_hospital_scorecard.csv  per login-code, avg ded% > 25%, + hospital risk score
    q13d_chronic_claimants.csv   cards with >= 3 high-value claims, + claimant risk score
    q13c_regional.csv            cleaned (Region <id> when command name missing)
    q13f_bulk_injection.csv      + severity tier
    module13_summary.json        headline metrics for the executive summary

Risk scores are transparent weighted sums (0-100) - NO machine learning. The
weights are emitted to module13_summary.json so the report can print them.
"""
import os
import re
import json
import math

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "module_13", "data")

HV = 500000.0
CRORE = 1e7

# ---- transparent risk-score weights (documented in the report) -------------
CLAIM_WEIGHTS = {"deduction": 35, "magnitude": 25, "full_deduction": 15,
                 "same_day_duplicate": 15, "anomalous_hospital": 10}
HOSPITAL_WEIGHTS = {"avg_deduction": 40, "absolute_deducted": 30,
                    "volume": 15, "full_deduction_share": 15}
CLAIMANT_WEIGHTS = {"volume": 35, "single_hospital_lockin": 25,
                    "total_claimed": 25, "bulk_injection": 15}
BANDS = [(70, "CRITICAL"), (45, "HIGH"), (0, "MEDIUM")]


def band(score):
    for cut, label in BANDS:
        if score >= cut:
            return label
    return "MEDIUM"


def is_anomalous_hospital(code):
    if code is None:
        return True
    c = str(code).strip()
    if c in ("", "NULL", "-1", "0"):
        return True
    if c.isdigit():               # phone numbers / numeric placeholders used as hospital IDs
        return True
    return False


def load_base():
    path = os.path.join(DATA, "high_value_claims_base.csv")
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        raise SystemExit(f"missing/empty base extract: {path} (run analyze_point13.py first)")
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    for col in ("claimed", "approved", "net_claim"):
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
    # guard: only true high-value rows
    df = df[df["claimed"] > HV].copy()
    df["ded_amt"] = (df["claimed"] - df["approved"]).clip(lower=0)
    df["ded_pct"] = np.where(df["claimed"] > 0, df["ded_amt"] / df["claimed"] * 100, 0).round(2)
    df["full_ded"] = (df["approved"] <= 0).astype(int)
    df["anom_hosp"] = df["hospital_code"].map(is_anomalous_hospital).astype(int)
    return df


def add_duplicate_flag(df):
    key = ["card_id", "admission_date", "claimed"]
    grp = df.groupby(key)["intimation_id"].transform("size")
    df["same_day_dup"] = (grp > 1).astype(int)
    return df


def claim_risk(df):
    w = CLAIM_WEIGHTS
    ded = (df["ded_pct"] / 100.0).clip(0, 1)
    mag = (df["claimed"] / CRORE).clip(0, 1)               # Rs 1 crore -> full marks
    s = (ded * w["deduction"] + mag * w["magnitude"]
         + df["full_ded"] * w["full_deduction"]
         + df["same_day_dup"] * w["same_day_duplicate"]
         + df["anom_hosp"] * w["anomalous_hospital"])
    return s.round(1)


def build_q13a(df):
    top = df.sort_values("claimed", ascending=False).head(200).copy()
    top["risk_score"] = claim_risk(top)
    top["risk_band"] = top["risk_score"].map(band)
    cols = ["risk_score", "risk_band", "card_id", "beneficiary", "patient", "hospital_code",
            "admission_date", "diagnosis", "claimed", "approved", "ded_pct",
            "same_day_dup", "full_ded", "anom_hosp", "intimation_id"]
    top[cols].rename(columns={"claimed": "exposure"}).to_csv(
        os.path.join(DATA, "q13a_top_claims.csv"), index=False)
    return top


def build_duplicates(df):
    key = ["card_id", "admission_date", "claimed"]
    g = (df.groupby(key)
           .agg(dup_count=("intimation_id", "size"),
                beneficiary=("beneficiary", "first"),
                hospital_code=("hospital_code", "first"),
                approved=("approved", "first"),
                ded_pct=("ded_pct", "first"),
                intimation_ids=("intimation_id", lambda s: ", ".join(map(str, s))))
           .reset_index())
    g = g[g["dup_count"] > 1].sort_values(["claimed", "dup_count"], ascending=False)
    g["duplicated_value"] = g["claimed"] * (g["dup_count"] - 1)   # extra billed by the dups
    g.rename(columns={"claimed": "exposure"}).head(100).to_csv(
        os.path.join(DATA, "q13a2_duplicates.csv"), index=False)
    return g


def build_q13b(df):
    g = (df.groupby("hospital_code")
           .agg(hv_claims=("intimation_id", "size"),
                claimed=("claimed", "sum"),
                ded_amt=("ded_amt", "sum"),
                full_ded_claims=("full_ded", "sum"))
           .reset_index())
    # The scorecard ranks REAL hospital logins; NULL/numeric placeholder IDs are
    # not hospitals (they are surfaced separately as the ghost-claim signal).
    g = g[~g["hospital_code"].map(is_anomalous_hospital)].copy()
    g["claimed_cr"] = (g["claimed"] / CRORE).round(2)
    g["deducted_cr"] = (g["ded_amt"] / CRORE).round(2)
    g["avg_ded_pct"] = np.where(g["claimed"] > 0, g["ded_amt"] / g["claimed"] * 100, 0).round(2)
    g["full_ded_share"] = (g["full_ded_claims"] / g["hv_claims"]).round(3)
    flagged = g[(g["hv_claims"] >= 10) & (g["avg_ded_pct"] > 25)].copy()
    # hospital risk score
    w = HOSPITAL_WEIGHTS
    max_ded = max(flagged["deducted_cr"].max(), 1e-9) if len(flagged) else 1.0
    max_vol = max(flagged["hv_claims"].max(), 1) if len(flagged) else 1
    flagged["risk_score"] = (
        (flagged["avg_ded_pct"] / 100).clip(0, 1) * w["avg_deduction"]
        + (flagged["deducted_cr"] / max_ded).clip(0, 1) * w["absolute_deducted"]
        + (np.log1p(flagged["hv_claims"]) / math.log1p(max_vol)) * w["volume"]
        + flagged["full_ded_share"].clip(0, 1) * w["full_deduction_share"]
    ).round(1)
    flagged["risk_band"] = flagged["risk_score"].map(band)
    flagged = flagged.sort_values("deducted_cr", ascending=False)
    cols = ["risk_score", "risk_band", "hospital_code", "hv_claims", "claimed_cr",
            "deducted_cr", "avg_ded_pct", "full_ded_claims"]
    flagged[cols].head(50).rename(columns={"claimed_cr": "exposure_cr"}).to_csv(
        os.path.join(DATA, "q13b_hospital_scorecard.csv"), index=False)
    return flagged


def build_q13d(df, bulk_cards):
    def primary(s):
        vc = s.value_counts()
        return vc.index[0], int(vc.iloc[0])
    rows = []
    for card, sub in df[df["card_id"] != ""].groupby("card_id"):
        n = len(sub)
        if n < 3:
            continue
        prim_hosp, prim_n = primary(sub["hospital_code"])
        rows.append({
            "card_id": card,
            "beneficiary": sub["beneficiary"].iloc[0],
            "hv_claims": n,
            "claimed_cr": round(sub["claimed"].sum() / CRORE, 2),
            "approved_cr": round(sub["approved"].sum() / CRORE, 2),
            "deducted_cr": round(sub["ded_amt"].sum() / CRORE, 2),
            "first_admit": sub["admission_date"].min(),
            "last_admit": sub["admission_date"].max(),
            "hosp_cnt": sub["hospital_code"].nunique(),
            "primary_hospital": prim_hosp,
            "lockin": round(prim_n / n, 3),
            "in_bulk_injection": int(card in bulk_cards),
        })
    g = pd.DataFrame(rows)
    if g.empty:
        g.to_csv(os.path.join(DATA, "q13d_chronic_claimants.csv"), index=False)
        return g
    w = CLAIMANT_WEIGHTS
    max_vol = max(g["hv_claims"].max(), 1)
    max_cl = max(g["claimed_cr"].max(), 1e-9)
    g["risk_score"] = (
        (np.log1p(g["hv_claims"]) / math.log1p(max_vol)) * w["volume"]
        + g["lockin"].clip(0, 1) * w["single_hospital_lockin"]
        + (g["claimed_cr"] / max_cl).clip(0, 1) * w["total_claimed"]
        + g["in_bulk_injection"] * w["bulk_injection"]
    ).round(1)
    g["risk_band"] = g["risk_score"].map(band)
    g = g.sort_values("claimed_cr", ascending=False)
    cols = ["risk_score", "risk_band", "card_id", "beneficiary", "hv_claims", "claimed_cr",
            "approved_cr", "deducted_cr", "first_admit", "last_admit", "hosp_cnt",
            "primary_hospital", "lockin", "in_bulk_injection"]
    g[cols].head(50).rename(columns={"claimed_cr": "exposure_cr"}).to_csv(
        os.path.join(DATA, "q13d_chronic_claimants.csv"), index=False)
    return g


def clean_regional():
    path = os.path.join(DATA, "q13c_regional.csv")
    if not os.path.exists(path):
        return None
    r = pd.read_csv(path, dtype=str, keep_default_na=False)
    if "claimed_cr" in r.columns:                          # raw extract -> present as exposure
        r = r.rename(columns={"claimed_cr": "exposure_cr"})
    r["command"] = [c if c not in ("", "NULL") else f"Region {rid}"
                    for c, rid in zip(r["command"], r["region_id"])]
    for c in ("exposure_cr", "approved_cr", "deducted_cr", "ded_pct"):
        r[c] = pd.to_numeric(r[c], errors="coerce")
    r.to_csv(path, index=False)                            # idempotent: safe to re-run
    return r


def process_bulk():
    path = os.path.join(DATA, "q13f_bulk_injection.csv")
    if not os.path.exists(path):
        return pd.DataFrame(), set()
    b = pd.read_csv(path, dtype=str, keep_default_na=False)
    b["intimation_count"] = pd.to_numeric(b["intimation_count"], errors="coerce").fillna(0).astype(int)

    def tier(n):
        if n > 300:
            return "SYSTEM COMPROMISE"
        if n >= 100:
            return "ACCOUNT ABUSE"
        return "WATCH"
    b["tier"] = b["intimation_count"].map(tier)
    b = b.sort_values("intimation_count", ascending=False)
    b.to_csv(path, index=False)
    return b, set(b["card_id"].unique())


def main():
    base = add_duplicate_flag(load_base())
    bulk, bulk_cards = process_bulk()
    regional = clean_regional()

    q13a = build_q13a(base)
    dups = build_duplicates(base)
    q13b = build_q13b(base)
    q13d = build_q13d(base, bulk_cards)

    total_claimed_cr = round(base["claimed"].sum() / CRORE, 2)
    total_deducted_cr = round(base["ded_amt"].sum() / CRORE, 2)
    anom = base[base["anom_hosp"] == 1]
    summary = {
        "scope": "Full history (all years)",
        "hv_threshold_rs": HV,
        "total_hv_claims": int(len(base)),
        "total_exposure_cr": total_claimed_cr,
        "total_deducted_cr": total_deducted_cr,
        "overall_ded_pct": round(total_deducted_cr / total_claimed_cr * 100, 2) if total_claimed_cr else 0,
        "full_deduction_hv_claims": int(base["full_ded"].sum()),
        "n_anomalous_hv_claims": int(len(anom)),
        "anomalous_exposure_cr": round(anom["claimed"].sum() / CRORE, 2),
        "top_single_claim_cr": round(base["claimed"].max() / CRORE, 2),
        "n_flagged_hospitals": int(len(q13b)),
        "n_chronic_claimants": int((base.groupby("card_id").size() >= 3).sum()),
        "n_duplicate_groups": int(len(dups)),
        "n_bulk_events": int(len(bulk)),
        "n_bulk_system_compromise": int((bulk["tier"] == "SYSTEM COMPROMISE").sum()) if len(bulk) else 0,
        "n_regions": int(len(regional)) if regional is not None else 0,
        "weights": {"claim": CLAIM_WEIGHTS, "hospital": HOSPITAL_WEIGHTS, "claimant": CLAIMANT_WEIGHTS},
        "bands": {label: cut for cut, label in BANDS},
    }
    with open(os.path.join(DATA, "module13_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print("Built Module 13 datasets:")
    print(f"  high-value claims     : {summary['total_hv_claims']:,}")
    print(f"  total exposure        : Rs {total_claimed_cr:,.2f} Cr")
    print(f"  total deducted        : Rs {total_deducted_cr:,.2f} Cr ({summary['overall_ded_pct']}%)")
    print(f"  100% deducted (HV)    : {summary['full_deduction_hv_claims']:,}")
    print(f"  flagged hospitals     : {summary['n_flagged_hospitals']}")
    print(f"  chronic claimants >=3 : {summary['n_chronic_claimants']:,}")
    print(f"  duplicate groups      : {summary['n_duplicate_groups']:,}")
    print(f"  bulk-injection events : {summary['n_bulk_events']} (system-compromise: {summary['n_bulk_system_compromise']})")
    print("  top hospitals:", ", ".join(q13b["hospital_code"].head(6))) if len(q13b) else None


if __name__ == "__main__":
    main()
