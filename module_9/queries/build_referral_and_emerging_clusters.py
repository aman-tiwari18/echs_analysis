"""
Module 9 — Cross-Region Referral Usage & Predictive Emerging Clusters
==========================================================================
Builds the two remaining Module 9 framework components ("Cross-region
referral usage" and "Predictive: Identify emerging clusters") entirely from
data already produced by other modules' reports — no new database queries.

  - Cross-Region Referral Usage   <- Module 3's (FA03) single-hospital
    funnelling export: polyclinic_id/city -> the one hospital it funnels
    the overwhelming majority of its referrals to. A polyclinic_city that
    differs from the destination hospital's city is flagged cross-region.

  - Predictive Emerging Clusters  <- Module 10's (Time-Series Surge) YoY
    spike export and Module 12's hospital YoY billing-spike export. Both
    already compute year-on-year growth per hospital; this script merely
    re-surfaces the top accelerating hospitals as the Module 9 "emerging
    cluster" view.
"""

import csv, os
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(BASE, 'data', 'source')
LOCAL_MODULES = os.path.dirname(BASE)

def to_float(v, default=0.0):
    try: return float(str(v).replace(',', '').strip())
    except Exception: return default

def norm_city(c):
    return str(c).strip().upper()

def read_csv(path):
    with open(path, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

# ── Cross-Region Referral Usage (from FA03 funnelling institutions) ──────────
def build_referral_usage():
    rows = read_csv(os.path.join(SRC, 'module_03_FA03', 'FA03_funnelling_institutions.csv'))
    out = []
    for r in rows:
        poly_city = norm_city(r.get('polyclinic_city', ''))
        dest_city = norm_city(r.get('funnels_to_city', ''))
        if not poly_city or not dest_city:
            continue
        cross_region = poly_city != dest_city
        out.append({
            'polyclinic_id': r.get('polyclinic_id', ''),
            'polyclinic_name': r.get('polyclinic_name', ''),
            'polyclinic_city': r.get('polyclinic_city', ''),
            'referrals': r.get('referrals', '0'),
            'top_dest_pct': r.get('top_dest_pct', '0'),
            'funnels_to': r.get('funnels_to', ''),
            'funnels_to_city': r.get('funnels_to_city', ''),
            'cross_region': 'YES' if cross_region else 'NO',
            'exposure_cr': r.get('exposure_cr', '0'),
        })
    out.sort(key=lambda r: -to_float(r['exposure_cr']))

    out_path = os.path.join(BASE, 'data', 'Cross_Region_Referral_Usage.csv')
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()), quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(out)
    cross_count = sum(1 for r in out if r['cross_region'] == 'YES')
    print(f"Wrote Cross_Region_Referral_Usage.csv: {len(out)} polyclinic-funnel pairs "
          f"({cross_count} cross-region, {len(out)-cross_count} same-region)")

# ── Predictive Emerging Clusters (from Module 10 + Module 12 YoY exports) ────
def build_emerging_clusters():
    out = []

    MIN_EXPOSURE_CR = 1.0   # ignore spikes too small to matter (avoids div-by-near-zero noise)
    MIN_PREV_CLAIMS = 10    # module 12 only: require a meaningful prior-year base

    m10 = read_csv(os.path.join(SRC, 'module_10', 'query5a_yoy_spike.csv'))
    for r in m10:
        oid = str(r.get('Office ID', '')).strip()
        if not oid.isdigit():
            continue
        exposure_cr = to_float(r.get('Exposure', 0)) / 1e7
        if exposure_cr < MIN_EXPOSURE_CR:
            continue
        out.append({
            'hospital_id': oid,
            'hospital_name': r.get('Hospital Name', ''),
            'source': 'Time-Series Billing Surge',
            'spike_year': r.get('Spike Year', ''),
            'yoy_growth_pct': to_float(r.get('YoY Growth %', 0)),
            'exposure_cr': exposure_cr,
        })

    m12 = read_csv(os.path.join(LOCAL_MODULES, 'module_12', 'data', 'report_data',
                                 '04a_hospital_yoy_billing_spike_20260612_115946.csv'))
    for r in m12:
        oid = str(r.get('hospital_id', '')).strip()
        if not oid.isdigit():
            continue
        if to_float(r.get('prev_claims', 0)) < MIN_PREV_CLAIMS:
            continue
        exposure_cr = to_float(r.get('curr_claimed_lakh', 0)) / 100
        if exposure_cr < MIN_EXPOSURE_CR:
            continue
        out.append({
            'hospital_id': oid,
            'hospital_name': r.get('hospital_name', ''),
            'source': 'Hospital Specialty Misuse',
            'spike_year': r.get('curr_year', ''),
            'yoy_growth_pct': to_float(r.get('yoy_amount_growth_pct', 0)),
            'exposure_cr': exposure_cr,
        })

    out.sort(key=lambda r: -r['yoy_growth_pct'])

    out_path = os.path.join(BASE, 'data', 'Predictive_Emerging_Clusters.csv')
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()), quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(out)
    print(f"Wrote Predictive_Emerging_Clusters.csv: {len(out)} hospital-year spike records")

if __name__ == '__main__':
    build_referral_usage()
    build_emerging_clusters()
