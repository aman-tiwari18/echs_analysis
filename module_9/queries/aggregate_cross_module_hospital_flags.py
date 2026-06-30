"""
Module 9 — Cross-Module Geo-Spatial Fraud Clustering Aggregator
====================================================================
Module 9's brief (per the ECHS Fraud Analytics Framework) is "Geo-Spatial
Fraud Clustering": identify fraud hotspots and cross-region usage patterns.
Rather than re-deriving fraud signals from raw claims, this script reuses
the fraud cases ALREADY flagged and exported by Modules 1-8, 10, 12-14,
18-19 (each module's own hospital-level summary CSV) and aggregates them
geographically: which hospitals are flagged by the most independent fraud
patterns, and which ECHS regions/states concentrate the most flagged
exposure across the whole framework.

Modules 11, 15, 16 and 17 are EXCLUDED from this index because their
existing exports either have no hospital-level rollup (11, 17 — card/
mobile/UID and account/doctor level only) or use free-text hospital
identifiers incompatible with office_master's numeric OM_OFFICE_ID (15, 16
— e.g. "p.kullu", "hos.3158"). This mirrors the exact ID-mismatch caveat
the original Module 9 report raised for Q9b.

Output:
  - Cross_Module_Hospital_Risk_Index.csv   (one row per hospital)
  - Cross_Module_Regional_Clustering.csv   (rollup by ECHS region)
  - Cross_Module_State_Clustering.csv      (rollup by state)
  - Cross_Module_Hospital_Chains.csv       (brand-name chain rollup)
"""

import csv, os, re
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(BASE, 'data', 'source')
LOCAL_MODULES = os.path.dirname(BASE)  # echs_analysis/

def to_float(v, default=0.0):
    try:
        return float(str(v).replace(',', '').strip())
    except Exception:
        return default

def parse_exposure_text(v):
    """Parses strings like '400.57 Cr' -> crore value."""
    s = str(v).strip()
    m = re.match(r'([\d.]+)\s*Cr', s, re.IGNORECASE)
    if m:
        return to_float(m.group(1))
    return 0.0

UNIT_TO_CR = {'rupee': 1e7, 'lakh': 1e5, 'crore': 1}

# ── Source registry: one entry per already-flagged hospital-level export ─────
SOURCES = [
    dict(label='Revenue Inflation Outliers',      path=f'{SRC}/module_01/Module_01_PATTERN_01.csv',
         id_col='OM_OFFICE_ID', name_col='OM_OFFICE_NAME', claims_col='total_claims',
         exposure_col='total_claimed_amount', unit='rupee'),
    dict(label='Revenue Inflation Outliers',      path=f'{SRC}/module_01/Module_01_PATTERN_02.csv',
         id_col='OM_OFFICE_ID', name_col='OM_OFFICE_NAME', claims_col='total_claims',
         exposure_col='total_claimed_amount', unit='rupee'),
    dict(label='Revenue Inflation Outliers',      path=f'{SRC}/module_01/Module_01_PATTERN_03.csv',
         id_col='OM_OFFICE_ID', name_col='OM_OFFICE_NAME', claims_col='total_claims',
         exposure_col='total_claimed_amount', unit='rupee'),
    dict(label='Procedure Upcoding',     path=f'{SRC}/module_02/Module_02_PATTERN_01.csv',
         id_col='OM_OFFICE_ID', name_col='OM_OFFICE_NAME', claims_col='total_claims',
         exposure_col=None, unit=None, filter_col='flag', filter_val='TRUE'),
    dict(label='Procedure Upcoding',     path=f'{SRC}/module_02/Module_02_PATTERN_03.csv',
         id_col='OM_OFFICE_ID', name_col='OM_OFFICE_NAME', claims_col='total_claims',
         exposure_col=None, unit=None, filter_col='flag', filter_val='TRUE'),
    dict(label='Doctor Referral Concentration',    path=f'{SRC}/module_03_FA03/FA03_hospital_concentration.csv',
         id_col='hospital_id', name_col='hospital_name', claims_col='claims',
         exposure_col='claimed_cr', unit='crore'),
    dict(label='Beneficiary Utilisation Outliers', path=f'{SRC}/module_04_FA04/FA04_hospital_concentration.csv',
         id_col='hospital_id', name_col='hospital_name', claims_col='claims',
         exposure_col='claimed_cr', unit='crore'),
    dict(label='Repeat Admission Outliers',          path=f'{SRC}/module_05/High_Exposure_Hospital_Outlier_Queue.csv',
         id_col='hospital_id', name_col='hospital_name', claims_col='total_readmission_cases',
         exposure_col='total_exposure_display', unit='text_cr'),
    dict(label='Procedure Mislabelling', path=f'{SRC}/module_06/pattern_2_hospital_stats.csv',
         id_col=None, name_col='hospital_name', claims_col='total_claims',
         exposure_col='total_mislabeled_claimed', unit='rupee'),
    dict(label='Emergency Admission Misuse', path=f'{SRC}/module_07/q7_hospital.csv',
         id_col='office_id', name_col='hospital', claims_col='emerg_adm',
         exposure_col='emerg_billed', unit='rupee'),
    dict(label='Package/Item Billing Anomaly', path=f'{SRC}/module_08/pattern8_45_hospital_list.csv',
         id_col='SS_OFFICE_ID', name_col=None, claims_col='claims',
         exposure_col='deducted_cr', unit='crore'),
    dict(label='Package/Item Billing Anomaly', path=f'{SRC}/module_08/pattern8_pattern1_only_deduction.csv',
         id_col='SS_OFFICE_ID', name_col=None, claims_col='claims',
         exposure_col='deducted_cr', unit='crore'),
    dict(label='Time-Series Billing Surge',                path=f'{SRC}/module_10/query1c_eoq_surge.csv',
         id_col='Office ID', name_col='Hospital Name', claims_col='Quarterly Claims',
         exposure_col='Exposure', unit='rupee'),
    dict(label='Time-Series Billing Surge',                path=f'{SRC}/module_10/query5a_yoy_spike.csv',
         id_col='Office ID', name_col='Hospital Name', claims_col=None,
         exposure_col='Exposure', unit='rupee'),
    dict(label='Hospital Specialty Misuse',         path=f'{LOCAL_MODULES}/module_12/data/report_data/01a_specialty_misuse_hospitals_20260612_101351.csv',
         id_col='hospital_id', name_col='hospital_name', claims_col='ipd_claims',
         exposure_col='total_deducted', unit='rupee'),
    dict(label='Hospital Specialty Misuse',   path=f'{LOCAL_MODULES}/module_12/data/report_data/02b_nabh_high_deduction_anomalies_20260612_105821.csv',
         id_col='hospital_id', name_col='hospital_name', claims_col='total_claims',
         exposure_col='claimed_lakh', unit='lakh'),
    dict(label='Hospital Specialty Misuse', path=f'{LOCAL_MODULES}/module_12/data/report_data/02d_military_hospital_breakdown_20260612_105821.csv',
         id_col='hospital_id', name_col='hospital_name', claims_col='total_claims',
         exposure_col='claimed_cr', unit='crore'),
    dict(label='Hospital Specialty Misuse',  path=f'{LOCAL_MODULES}/module_12/data/report_data/03b_ipd_without_ipd_empanelment_20260612_113504.csv',
         id_col='hospital_id', name_col='hospital_name', claims_col='ipd_claims_filed',
         exposure_col='total_claimed', unit='rupee'),
    dict(label='Hospital Specialty Misuse',        path=f'{LOCAL_MODULES}/module_12/data/report_data/04a_hospital_yoy_billing_spike_20260612_115946.csv',
         id_col='hospital_id', name_col='hospital_name', claims_col='curr_claims',
         exposure_col='curr_claimed_lakh', unit='lakh'),
    dict(label='Hospital Specialty Misuse',      path=f'{LOCAL_MODULES}/module_12/data/report_data/05b_low_tier_hospitals_high_value_20260612_113405.csv',
         id_col='hospital_id', name_col='hospital_name', claims_col='high_val_claims',
         exposure_col='total_claimed_lakh', unit='lakh'),
    dict(label='High-Value Claim Risk Scoring', path=f'{SRC}/module_13/q13b_hospital_scorecard.csv',
         id_col='office_id', name_col='hospital_name', claims_col='hv_claims',
         exposure_col='exposure_cr', unit='crore'),
    dict(label='Pre-Authorization Deviation',       path=f'{SRC}/module_14/q14a_hospital_deviation.csv',
         id_col='office_id', name_col='hospital', claims_col='claims',
         exposure_col='billed_cr', unit='crore'),
    dict(label='Claim Processing / Overbilling Pattern',   path=f'{LOCAL_MODULES}/module_18/data/05_Systematic_Overbillers_20260612_134953.csv',
         id_col='hospital_id', name_col='hospital_name', claims_col='total_claims',
         exposure_col='total_claimed', unit='rupee'),
    dict(label='Claim Processing / Overbilling Pattern',   path=f'{LOCAL_MODULES}/module_18/data/06_Untouched_High_Billers_20260612_135716.csv',
         id_col='hospital_id', name_col='hospital_name', claims_col='total_claims',
         exposure_col='total_claimed', unit='rupee'),
    dict(label='Policy Abuse Pattern',  path=f'{SRC}/module_19/q19a_hospital_deduction_analysis.csv',
         id_col='office_id', name_col='hospital', claims_col='total_claims',
         exposure_col='claimed_cr', unit='crore'),
    dict(label='Policy Abuse Pattern',    path=f'{SRC}/module_19/q19d_multi_abuse_hospitals.csv',
         id_col='office_id', name_col=None, claims_col='total_claims',
         exposure_col='total_exposure', unit='rupee'),
    dict(label='Implausible Claim Volume',  path=f'{SRC}/module_03_FA03/FA03_implausible_volume.csv',
         id_col='hospital_id', name_col='hospital_name', claims_col='claims',
         exposure_col='claimed_cr', unit='crore'),
    dict(label='Extreme Deduction Outliers', path=f'{SRC}/module_03_FA03/FA03_extreme_deduction.csv',
         id_col='hospital_id', name_col='hospital_name', claims_col='claims',
         exposure_col='claimed_cr', unit='crore'),
    dict(label='Same-Day Zero-Stay High-Value IPD', path=f'{SRC}/module_03_FA03/FA03_sameday_ipd.csv',
         id_col='hospital_id', name_col='hospital_name', claims_col='repeat_cases',
         exposure_col='claimed_lakh', unit='lakh'),
    dict(label='Hospital Escalation (YoY Ratio Rise)', path=f'{SRC}/module_14/q14c_hospital_escalation.csv',
         id_col='office_id', name_col='hospital', claims_col='claims',
         exposure_col=None, unit=None),
    dict(label='Room Entitlement Mismatch', path=f'{SRC}/module_19/q19b_room_entitlement_mismatch.csv',
         id_col='hospital_id', name_col='hospital_name', claims_col='total_claims',
         exposure_col='claimed_cr', unit='crore'),
    dict(label='Emergency Claim Flag Abuse', path=f'{SRC}/module_19/q19c_private_hospital_yflag_claims.csv',
         id_col='hospital_id', name_col='hospital_name', claims_col='total_claims',
         exposure_col='claimed_cr', unit='crore'),
]

# Region-level cross-check source (already aggregated by ECHS region, not hospital)
REGION_SOURCE = dict(
    label='M13 Regional Command Exposure',
    path=f'{SRC}/module_13/q13c_regional.csv',
    region_col='region_id', name_col='command',
    claims_col='claim_cnt', exposure_col='exposure_cr', unit='crore',
)

def load_office_lookup():
    path = os.path.join(BASE, 'data', 'office_master_lookup.csv')
    lookup = {}
    with open(path, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            oid = row.get('OM_OFFICE_ID', '').strip()
            if oid:
                lookup[oid] = {
                    'name': row.get('OM_OFFICE_NAME', '').strip(),
                    'city': row.get('OM_OFFICE_CITY', '').strip(),
                    'state_id': row.get('OM_OFFICE_STATE_ID', '').strip(),
                    'state_name': row.get('SM_STATE_NAME', '').strip(),
                    'region_id': row.get('region_id', '').strip(),
                }
    return lookup

def read_csv(path):
    if not os.path.exists(path):
        print(f"  MISSING: {path}")
        return []
    with open(path, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def load_claims_baseline():
    """Real (non-flagged) total claim volume per hospital, last 5 FYs — full coverage, no top-N limit."""
    import glob
    files = glob.glob(os.path.join(BASE, 'data', '02a_Hospital_Claims_Baseline*.csv'))
    if not files:
        return {}
    files.sort(key=os.path.getmtime, reverse=True)
    baseline = {}
    with open(files[0], encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            oid = row.get('hospital_id', '').strip()
            if oid:
                baseline[oid] = int(to_float(row.get('claims', 0)))
    return baseline

def normalize_name(n):
    n = str(n).upper()
    n = re.sub(r'\(A UNIT OF[^)]*\)', '', n)
    n = re.sub(r'[^A-Z0-9 ]', ' ', n)
    n = re.sub(r'\s+', ' ', n).strip()
    return n

def chain_key(name):
    """First 1-2 significant words of normalized hospital name, used to detect chains."""
    norm = normalize_name(name)
    words = [w for w in norm.split(' ') if w not in ('HOSPITAL', 'THE', 'A', 'OF')]
    return ' '.join(words[:2]) if words else norm

def main():
    office_lookup = load_office_lookup()
    claims_baseline = load_claims_baseline()
    name_to_id = {}
    for oid, info in office_lookup.items():
        nm = normalize_name(info['name'])
        if nm:
            name_to_id.setdefault(nm, oid)

    # hospital_id -> {modules:set, claims:int, exposure_cr:float, names:set}
    hospital_agg = defaultdict(lambda: {'modules': set(), 'claims': 0, 'exposure_cr': 0.0, 'names': set()})
    unmapped_count = 0

    for src in SOURCES:
        rows = read_csv(src['path'])
        if not rows:
            continue
        matched = 0
        for row in rows:
            if src.get('filter_col'):
                if str(row.get(src['filter_col'], '')).strip().upper() != src['filter_val']:
                    continue

            oid = None
            if src['id_col']:
                raw_id = str(row.get(src['id_col'], '')).strip()
                if raw_id.isdigit():
                    oid = raw_id
            if oid is None and src.get('name_col'):
                nm = normalize_name(row.get(src['name_col'], ''))
                oid = name_to_id.get(nm)
            if oid is None:
                unmapped_count += 1
                continue

            claims = to_float(row.get(src['claims_col'], 0)) if src.get('claims_col') else 0
            exposure_cr = 0.0
            if src.get('exposure_col'):
                raw_exp = row.get(src['exposure_col'], 0)
                if src['unit'] == 'text_cr':
                    exposure_cr = parse_exposure_text(raw_exp)
                else:
                    exposure_cr = to_float(raw_exp) / UNIT_TO_CR[src['unit']]

            agg = hospital_agg[oid]
            agg['modules'].add(src['label'])
            agg['claims'] += claims
            agg['exposure_cr'] += exposure_cr
            if src.get('name_col'):
                agg['names'].add(str(row.get(src['name_col'], '')).strip())
            matched += 1
        print(f"{src['label']:38s} {len(rows):>7,} rows -> {matched:>6,} matched to office IDs")

    print(f"\nTotal rows that could not be mapped to a numeric office ID: {unmapped_count:,}")

    # ── Build Cross_Module_Hospital_Risk_Index ────────────────────────────────
    out_rows = []
    for oid, agg in hospital_agg.items():
        info = office_lookup.get(oid, {})
        name = info.get('name') or (sorted(agg['names'])[0] if agg['names'] else f'Office {oid}')
        out_rows.append({
            'hospital_id': oid,
            'hospital_name': name,
            'city': info.get('city', ''),
            'state_id': info.get('state_id', ''),
            'state_name': info.get('state_name', ''),
            'region_id': info.get('region_id', ''),
            'modules_flagged_count': len(agg['modules']),
            'modules_flagged_list': ' | '.join(sorted(agg['modules'])),
            'total_claims_baseline': claims_baseline.get(oid, 0),
            'total_flagged_claims': int(agg['claims']),
            'total_flagged_exposure_cr': round(agg['exposure_cr'], 2),
        })
    out_rows.sort(key=lambda r: (-r['modules_flagged_count'], -r['total_flagged_exposure_cr']))

    data_dir = os.path.join(BASE, 'data')
    with open(os.path.join(data_dir, 'Cross_Module_Hospital_Risk_Index.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()), quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(out_rows)
    print(f"\nWrote Cross_Module_Hospital_Risk_Index.csv: {len(out_rows)} hospitals")

    # Full-universe totals (every empanelled hospital, not just flagged ones)
    region_universe = defaultdict(lambda: {'hospitals': set(), 'claims': 0})
    state_universe = defaultdict(lambda: {'hospitals': set(), 'claims': 0})
    for oid, info in office_lookup.items():
        rid = info.get('region_id') or 'UNKNOWN'
        sid = info.get('state_id') or 'UNKNOWN'
        region_universe[rid]['hospitals'].add(oid)
        region_universe[rid]['claims'] += claims_baseline.get(oid, 0)
        state_universe[sid]['hospitals'].add(oid)
        state_universe[sid]['claims'] += claims_baseline.get(oid, 0)

    # ── Regional rollup ────────────────────────────────────────────────────────
    region_agg = defaultdict(lambda: {'hospitals': set(), 'modules': set(), 'claims': 0, 'exposure_cr': 0.0})
    for r in out_rows:
        rid = r['region_id'] or 'UNKNOWN'
        ra = region_agg[rid]
        ra['hospitals'].add(r['hospital_id'])
        ra['modules'].update(r['modules_flagged_list'].split(' | '))
        ra['claims'] += r['total_flagged_claims']
        ra['exposure_cr'] += r['total_flagged_exposure_cr']

    region_rows = []
    for rid, ra in region_agg.items():
        region_rows.append({
            'region_id': rid,
            'total_hospitals': len(region_universe[rid]['hospitals']),
            'flagged_hospitals': len(ra['hospitals']),
            'distinct_patterns_represented': len(ra['modules']),
            'total_claims_baseline': region_universe[rid]['claims'],
            'total_flagged_claims': int(ra['claims']),
            'total_flagged_exposure_cr': round(ra['exposure_cr'], 2),
        })
    region_rows.sort(key=lambda r: -r['total_flagged_exposure_cr'])
    with open(os.path.join(data_dir, 'Cross_Module_Regional_Clustering.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(region_rows[0].keys()), quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(region_rows)
    print(f"Wrote Cross_Module_Regional_Clustering.csv: {len(region_rows)} regions")

    # ── State rollup ───────────────────────────────────────────────────────────
    state_agg = defaultdict(lambda: {'hospitals': set(), 'modules': set(), 'claims': 0, 'exposure_cr': 0.0, 'name': ''})
    for r in out_rows:
        sid = r['state_id'] or 'UNKNOWN'
        sa = state_agg[sid]
        sa['hospitals'].add(r['hospital_id'])
        sa['modules'].update(r['modules_flagged_list'].split(' | '))
        sa['claims'] += r['total_flagged_claims']
        sa['exposure_cr'] += r['total_flagged_exposure_cr']
        sa['name'] = r['state_name'] or sa['name']

    state_rows = []
    for sid, sa in state_agg.items():
        state_rows.append({
            'state_id': sid,
            'state_name': sa['name'] or 'Unknown',
            'total_hospitals': len(state_universe[sid]['hospitals']),
            'flagged_hospitals': len(sa['hospitals']),
            'distinct_patterns_represented': len(sa['modules']),
            'total_claims_baseline': state_universe[sid]['claims'],
            'total_flagged_claims': int(sa['claims']),
            'total_flagged_exposure_cr': round(sa['exposure_cr'], 2),
        })
    state_rows.sort(key=lambda r: -r['total_flagged_exposure_cr'])
    with open(os.path.join(data_dir, 'Cross_Module_State_Clustering.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(state_rows[0].keys()), quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(state_rows)
    print(f"Wrote Cross_Module_State_Clustering.csv: {len(state_rows)} states")

    # ── Chain rollup ───────────────────────────────────────────────────────────
    # Total units = every hospital nationally matching the chain's normalised name
    # (full office_master universe). Flagged units = the subset that triggered any signal.
    chain_universe = defaultdict(set)
    for oid, info in office_lookup.items():
        if info.get('name'):
            chain_universe[chain_key(info['name'])].add(oid)

    chain_agg = defaultdict(lambda: {'units': set(), 'modules': set(), 'claims': 0, 'exposure_cr': 0.0})
    for r in out_rows:
        key = chain_key(r['hospital_name'])
        ca = chain_agg[key]
        ca['units'].add(r['hospital_id'])
        ca['modules'].update(r['modules_flagged_list'].split(' | '))
        ca['claims'] += r['total_flagged_claims']
        ca['exposure_cr'] += r['total_flagged_exposure_cr']

    chain_rows = []
    for key, ca in chain_agg.items():
        if len(ca['units']) < 2:
            continue
        chain_rows.append({
            'chain_name': key,
            'total_units': len(chain_universe.get(key, ca['units'])),
            'flagged_units': len(ca['units']),
            'distinct_patterns_represented': len(ca['modules']),
            'total_flagged_claims': int(ca['claims']),
            'total_flagged_exposure_cr': round(ca['exposure_cr'], 2),
        })
    chain_rows.sort(key=lambda r: -r['total_flagged_exposure_cr'])
    with open(os.path.join(data_dir, 'Cross_Module_Hospital_Chains.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(chain_rows[0].keys()) if chain_rows else
                            ['chain_name','total_units','flagged_units','distinct_patterns_represented','total_flagged_claims','total_flagged_exposure_cr'],
                            quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(chain_rows)
    print(f"Wrote Cross_Module_Hospital_Chains.csv: {len(chain_rows)} multi-unit chains")

if __name__ == '__main__':
    main()
