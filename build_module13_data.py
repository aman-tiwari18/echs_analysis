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
    module13_cases.json          structured facts for the narrative case studies
    module13_hospital_deepdive.json  top-hospital deep-dives + ECHS-polyclinic view
    module13_ghost_claims.csv    HV claims with NULL/numeric/phone hospital IDs

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


# ---------------------------------------------------------------------------
# Narrative-detail derivations (all from the existing base extract; no new DB).
# These feed the case studies / deep-dives / ghost-claim tables in the report.
# ---------------------------------------------------------------------------
STATE_PREFIX = {"DL": "Delhi", "MU": "Mumbai", "HY": "Hyderabad", "KL": "Kerala",
                "CH": "Chandigarh", "PN": "Pune", "BL": "Bangalore", "JP": "Jaipur",
                "KK": "Kolkata", "AH": "Ahmedabad", "LK": "Lucknow"}
POLY_RE = r"^p(ol)?\."   # ECHS polyclinic login codes: p.<x> / pol.<x>


def _ghost_category(code):
    c = str(code).strip()
    if c in ("", "NULL"):
        return "NULL (missing)"
    if c in ("-1", "0"):
        return "Placeholder"
    if c.isdigit() and len(c) >= 10:
        return "Phone-like"
    if c.isdigit():
        return "Numeric"
    return "Other"


def _band_dist(series):
    vc = series.value_counts()
    return {b: int(vc.get(b, 0)) for b in ("CRITICAL", "HIGH", "MEDIUM")}


def _claimant_detail(base, card):
    sub = base[base["card_id"] == card]
    dates = pd.to_datetime(sub["admission_date"], errors="coerce").dropna().sort_values()
    n = int(len(sub))
    span_days = int((dates.iloc[-1] - dates.iloc[0]).days) if len(dates) >= 2 else 0
    exp = float(sub["claimed"].sum())
    ded = float(sub["ded_amt"].sum())
    vc = sub["hospital_code"].value_counts()
    prim_hosp, prim_n = str(vc.index[0]), int(vc.iloc[0])
    return {
        "beneficiary": str(sub["beneficiary"].iloc[0]), "card_id": str(card), "claims": n,
        "exposure_cr": round(exp / CRORE, 2), "approved_cr": round(float(sub["approved"].sum()) / CRORE, 2),
        "deducted_cr": round(ded / CRORE, 2), "ded_pct": round(ded / exp * 100, 1) if exp else 0,
        "primary_hospital": prim_hosp, "lockin_pct": round(prim_n / n * 100) if n else 0,
        "distinct_hospitals": int(sub["hospital_code"].nunique()),
        "first_admit": str(dates.iloc[0].date()) if len(dates) else "",
        "last_admit": str(dates.iloc[-1].date()) if len(dates) else "",
        "span_months": round(span_days / 30.4, 1) if span_days else 0,
        "avg_interval_days": round(span_days / (n - 1), 1) if n > 1 and span_days else 0,
        "distinct_diagnoses": int(sub.loc[sub["diagnosis"] != "", "diagnosis"].nunique()),
        "anomalous_primary": bool(is_anomalous_hospital(prim_hosp)),
    }


def _detect_card_variation(base):
    """Possible card-ID manipulation: ONE beneficiary on TWO near-identical card
    numbers (equal length, differing by a single character in the first 3
    positions, e.g. DL1...517957 vs DL2...517957). Strict to avoid common-name
    coincidence: a real single fraudster holds very few cards, so we only look at
    names with 2-4 distinct cards and report ONLY the matching pair (not the name
    aggregate). Returned hedged in the report - it is a lead, not a conclusion."""
    best = None
    by_name = base[base["card_id"] != ""].groupby("beneficiary")["card_id"]
    for name, s in by_name:
        cards = sorted(set(s))
        if not name or not (2 <= len(cards) <= 4):
            continue
        for i in range(len(cards)):
            for j in range(i + 1, len(cards)):
                a, b = cards[i], cards[j]
                if len(a) != len(b):
                    continue
                diffs = [k for k in range(len(a)) if a[k] != b[k]]
                if len(diffs) == 1 and diffs[0] < 3:
                    pair = base[base["card_id"].isin([a, b])]   # ONLY the two cards
                    if len(pair) < 3:
                        continue
                    cand = {"beneficiary": str(name), "card_a": a, "card_b": b,
                            "diff_pos": int(diffs[0]), "claims": int(len(pair)),
                            "exposure_cr": round(float(pair["claimed"].sum()) / CRORE, 2),
                            "hospitals": sorted(set(pair["hospital_code"]))[:4]}
                    if best is None or cand["exposure_cr"] > best["exposure_cr"]:
                        best = cand
    return best


def derive_cases(base, q13d, dups, bulk):
    cases = {}
    # chronic repeat claimant (most claims) + a ghost-hospital variant
    if len(q13d):
        top_card = q13d.loc[q13d["hv_claims"].idxmax(), "card_id"]
        cases["top_repeat_claimant"] = _claimant_detail(base, top_card)
        ghosts = q13d[q13d["primary_hospital"].map(is_anomalous_hospital)]
        if len(ghosts):
            cases["ghost_repeat_claimant"] = _claimant_detail(
                base, ghosts.sort_values("claimed_cr", ascending=False).iloc[0]["card_id"])
        lock = q13d[(q13d["hv_claims"] >= 40) & (q13d["lockin"] >= 0.8)
                    & (~q13d["primary_hospital"].map(is_anomalous_hospital))
                    & (q13d["card_id"] != top_card)]      # don't repeat the headline claimant
        lock = lock.sort_values("hv_claims", ascending=False).head(3)
        cases["lockin_examples"] = [
            {"beneficiary": str(r["beneficiary"]), "claims": int(r["hv_claims"]),
             "hospital": str(r["primary_hospital"]), "lockin_pct": round(float(r["lockin"]) * 100),
             "exposure_cr": round(float(r["claimed_cr"]), 2)}
            for _, r in lock.iterrows()]
    # top same-day duplicate
    if len(dups):
        d = dups.iloc[0]
        ids = [int(x) for x in str(d["intimation_ids"]).replace(" ", "").split(",") if x.strip().isdigit()]
        consecutive = (max(ids) - min(ids) <= len(ids) * 3) if len(ids) >= 2 else False
        cases["top_duplicate"] = {
            "beneficiary": str(d["beneficiary"]), "card_id": str(d["card_id"]),
            "hospital": str(d["hospital_code"]), "admission_date": str(d["admission_date"])[:10],
            "exposure": float(d["claimed"]), "dup_count": int(d["dup_count"]),
            "intimation_ids": ids[:6], "consecutive": bool(consecutive),
        }
    # card-ID variation (best-effort)
    cv = _detect_card_variation(base)
    if cv:
        cases["card_variation"] = cv
    # top bulk-injection event + multi-region spread
    if len(bulk):
        b0 = bulk.iloc[0]
        fid, lid = str(b0["first_intimation_id"]), str(b0["last_intimation_id"])
        span = (int(lid) - int(fid) + 1) if fid.isdigit() and lid.isdigit() else 0
        cnt = int(b0["intimation_count"])
        pref = re.match(r"^[A-Za-z]+", str(b0["card_id"]))
        cases["top_bulk"] = {
            "beneficiary": str(b0["beneficiary"]), "hospital": str(b0["hospital_code"]),
            "date": str(b0["creation_date"])[:10], "count": cnt,
            "first_id": fid, "last_id": lid, "id_span": span,
            "consecutive": bool(span and span <= cnt * 3),
            "tier": str(b0["tier"]), "card_prefix": pref.group(0) if pref else "",
        }
        prefixes = {}
        for _, r in bulk.iterrows():
            m = re.match(r"^[A-Za-z]+", str(r["card_id"]))
            if m:
                p = m.group(0)
                prefixes[p] = prefixes.get(p, 0) + 1
        cases["bulk_spread"] = {
            "n_events": int(len(bulk)),
            "prefixes": [{"prefix": p, "region": STATE_PREFIX.get(p, ""), "events": n}
                         for p, n in sorted(prefixes.items(), key=lambda kv: -kv[1])],
        }
    return cases


def derive_hospital_deepdive(base, q13b):
    out = {"hospitals": [], "polyclinic": {}}
    if len(q13b):
        codes = list(dict.fromkeys(
            list(q13b.sort_values("deducted_cr", ascending=False).head(3)["hospital_code"])
            + [q13b.sort_values("avg_ded_pct", ascending=False).iloc[0]["hospital_code"]]))
        for code in codes:
            row = q13b[q13b["hospital_code"] == code].iloc[0]
            sub = base[(base["hospital_code"] == code) & (base["full_ded"] == 1)]
            named = sub.sort_values("claimed", ascending=False).head(10)[["beneficiary", "claimed"]]
            out["hospitals"].append({
                "hospital_code": str(code), "hv_claims": int(row["hv_claims"]),
                "exposure_cr": round(float(row["claimed_cr"]), 2),
                "deducted_cr": round(float(row["deducted_cr"]), 2),
                "avg_ded_pct": round(float(row["avg_ded_pct"]), 2),
                "full_ded_claims": int(row["full_ded_claims"]),
                "is_polyclinic": bool(re.match(POLY_RE, str(code))),
                "named_full_ded": [{"beneficiary": str(b), "exposure": float(c)}
                                   for b, c in named.values],
            })
    poly = base[base["hospital_code"].str.match(POLY_RE, na=False)]
    if len(poly):
        exp = float(poly["claimed"].sum()); ded = float(poly["ded_amt"].sum())
        out["polyclinic"] = {"claims": int(len(poly)), "exposure_cr": round(exp / CRORE, 2),
                             "deducted_cr": round(ded / CRORE, 2),
                             "avg_ded_pct": round(ded / exp * 100, 2) if exp else 0,
                             "top_logins": []}
        if len(q13b):
            pq = q13b[q13b["hospital_code"].str.match(POLY_RE, na=False)]
            pq = pq.sort_values("avg_ded_pct", ascending=False).head(6)
            out["polyclinic"]["top_logins"] = [
                {"hospital_code": str(r["hospital_code"]), "avg_ded_pct": round(float(r["avg_ded_pct"]), 2),
                 "hv_claims": int(r["hv_claims"]), "deducted_cr": round(float(r["deducted_cr"]), 2)}
                for _, r in pq.iterrows()]
    return out


def derive_ghost_claims(base):
    g = base[base["anom_hosp"] == 1].sort_values("claimed", ascending=False).head(30).copy()
    g["category"] = g["hospital_code"].map(_ghost_category)
    g = g.rename(columns={"claimed": "exposure"})
    cols = ["beneficiary", "exposure", "hospital_code", "category", "admission_date", "ded_pct"]
    g[cols].to_csv(os.path.join(DATA, "module13_ghost_claims.csv"), index=False)


def main():
    base = add_duplicate_flag(load_base())
    bulk, bulk_cards = process_bulk()
    regional = clean_regional()

    q13a = build_q13a(base)
    dups = build_duplicates(base)
    q13b = build_q13b(base)
    q13d = build_q13d(base, bulk_cards)

    # narrative-detail artifacts (case studies / hospital deep-dives / ghost table)
    cases = derive_cases(base, q13d, dups, bulk)
    deepdive = derive_hospital_deepdive(base, q13b)
    derive_ghost_claims(base)
    with open(os.path.join(DATA, "module13_cases.json"), "w") as f:
        json.dump(cases, f, indent=2, default=str)
    with open(os.path.join(DATA, "module13_hospital_deepdive.json"), "w") as f:
        json.dump(deepdive, f, indent=2, default=str)

    adm = pd.to_datetime(base["admission_date"], errors="coerce").dropna()
    anom = base[base["anom_hosp"] == 1].copy()
    anom["category"] = anom["hospital_code"].map(_ghost_category)
    anom_breakdown = {cat: {"claims": int(c),
                            "exposure_cr": round(float(anom.loc[anom["category"] == cat, "claimed"].sum()) / CRORE, 2)}
                      for cat, c in anom["category"].value_counts().items()}

    total_claimed_cr = round(base["claimed"].sum() / CRORE, 2)
    total_deducted_cr = round(base["ded_amt"].sum() / CRORE, 2)
    summary = {
        "scope": "Last 5 years (CI_CR_DATE >= current date - 5 years)",
        "hv_threshold_rs": HV,
        "total_hv_claims": int(len(base)),
        "total_exposure_cr": total_claimed_cr,
        "total_deducted_cr": total_deducted_cr,
        "overall_ded_pct": round(total_deducted_cr / total_claimed_cr * 100, 2) if total_claimed_cr else 0,
        "full_deduction_hv_claims": int(base["full_ded"].sum()),
        "n_anomalous_hv_claims": int(len(anom)),
        "anomalous_exposure_cr": round(float(anom["claimed"].sum()) / CRORE, 2),
        "anomalous_breakdown": anom_breakdown,
        "top_single_claim_cr": round(base["claimed"].max() / CRORE, 2),
        "earliest_admit": str(adm.min().date()) if len(adm) else "",
        "latest_admit": str(adm.max().date()) if len(adm) else "",
        "n_flagged_hospitals": int(len(q13b)),
        "n_chronic_claimants": int((base.groupby("card_id").size() >= 3).sum()),
        "n_duplicate_groups": int(len(dups)),
        "n_bulk_events": int(len(bulk)),
        "n_bulk_system_compromise": int((bulk["tier"] == "SYSTEM COMPROMISE").sum()) if len(bulk) else 0,
        "n_regions": int(len(regional)) if regional is not None else 0,
        "claims_band_dist": _band_dist(q13a["risk_band"]) if len(q13a) else {},
        "hospitals_band_dist": _band_dist(q13b["risk_band"]) if len(q13b) else {},
        "claimants_band_dist": _band_dist(q13d["risk_band"]) if len(q13d) else {},
        "n_polyclinic_claims": deepdive.get("polyclinic", {}).get("claims", 0),
        "polyclinic_deducted_cr": deepdive.get("polyclinic", {}).get("deducted_cr", 0),
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
    print(f"  polyclinic HV claims  : {summary['n_polyclinic_claims']:,} (deducted Rs {summary['polyclinic_deducted_cr']:,.2f} Cr)")
    print(f"  anomalous HV claims   : {summary['n_anomalous_hv_claims']:,} (Rs {summary['anomalous_exposure_cr']:,.2f} Cr)")
    print(f"  case studies built    : {', '.join(cases.keys()) if cases else '(none)'}")


if __name__ == "__main__":
    main()
