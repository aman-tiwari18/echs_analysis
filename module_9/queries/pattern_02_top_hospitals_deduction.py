"""
Module 9 — Hospital Claims Baseline (full coverage, no top-N limit)
=======================================================================
Total claim volume, claimed/approved/deducted amounts and deduction rate
for EVERY empanelled hospital with settlement activity in the last 5
financial years (FY 2021-22 to FY 2025-26). This is the baseline "Total
Claims" figure cross-referenced against "Fraud Occurrence" (flagged claim
volume) throughout the report's hospital/region/chain tables.

Tables used:
  - settlement_stat : SS_OFFICE_ID, SS_FY_YEAR, SS_CLAIM_AMT, SS_APPR_AMT, SS_DED_AMT
  - office_master   : OM_OFFICE_ID, OM_OFFICE_NAME, OM_OFFICE_STATE_ID
"""

import paramiko, csv, io, datetime, os
from dotenv import load_dotenv
load_dotenv()

SSH_HOST = os.getenv('SSH_HOST')
SSH_PORT = int(os.getenv('SSH_PORT', 22))
SSH_USER = os.getenv('SSH_USER')
SSH_PASS = os.getenv('SSH_PASS')
DB_USER  = os.getenv('DB_USER')
DB_PASS  = os.getenv('DB_PASS')
DB_NAME  = os.getenv('DB_NAME')

# ── Query: full hospital claims baseline, no LIMIT ────────────────────────────
QUERY_2A = """
SELECT
    om.OM_OFFICE_ID                       AS hospital_id,
    om.OM_OFFICE_NAME                     AS hospital_name,
    om.OM_OFFICE_STATE_ID                 AS state_id,
    sm.SM_STATE_NAME                      AS state_name,
    SUM(ss.SS_CLAIM_CNT)                   AS claims,
    SUM(ss.SS_CLAIM_AMT)                   AS total_claimed,
    SUM(ss.SS_APPR_AMT)                    AS total_approved,
    SUM(ss.SS_DED_AMT)                     AS total_deducted,
    ROUND(
        CASE WHEN SUM(ss.SS_CLAIM_AMT) > 0
             THEN SUM(ss.SS_DED_AMT)/SUM(ss.SS_CLAIM_AMT)*100
             ELSE 0 END, 2
    )                                      AS deduction_pct
FROM settlement_stat ss
JOIN office_master om ON ss.SS_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN state_master sm ON om.OM_OFFICE_STATE_ID = sm.SM_STATE_ID
WHERE ss.SS_FY_YEAR >= 2021
GROUP BY om.OM_OFFICE_ID, om.OM_OFFICE_NAME, om.OM_OFFICE_STATE_ID, sm.SM_STATE_NAME
HAVING total_claimed > 0
ORDER BY total_deducted DESC;
"""

QUERIES = {
    '02a_Hospital_Claims_Baseline': QUERY_2A,
}

def run_query(client, sql):
    escaped = sql.replace("'", "'\\''")
    cmd = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e '{escaped}'"
    _, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode('utf-8')
    err = stderr.read().decode('utf-8')
    err_lines = [l for l in err.split('\n') if l.strip() and 'Warning' not in l]
    if err_lines:
        print(f"  SQL error: {'; '.join(err_lines)}")
        return []
    reader = csv.reader(io.StringIO(out), delimiter='\t')
    rows = [r for r in reader if r]
    return rows

def main():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    os.makedirs(data_dir, exist_ok=True)
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {SSH_HOST}...")
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
        for name, sql in QUERIES.items():
            print(f"Running {name}...")
            t0 = datetime.datetime.now()
            rows = run_query(client, sql)
            elapsed = datetime.datetime.now() - t0
            if len(rows) > 1:
                fname = os.path.join(data_dir, f'{name}_{ts}.csv')
                with open(fname, 'w', newline='', encoding='utf-8') as f:
                    csv.writer(f, quoting=csv.QUOTE_ALL).writerows(rows)
                print(f"  done: {len(rows)-1} rows -> {os.path.basename(fname)}  ({elapsed})")
            else:
                print(f"  no data returned for {name}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    main()
