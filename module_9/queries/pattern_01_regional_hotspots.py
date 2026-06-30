"""
Module 9 — Pattern 01: Regional Fraud Hotspot Analysis (Q9a)
==============================================================
Aggregates claims in settlement_stat by ECHS region code (SS_REGION_ID),
computing total claimed, approved, deducted, and deduction rate per region —
last 5 financial years (FY 2021-22 to FY 2025-26), matching the analysis
window used across the rest of the ECHS fraud-analytics programme. Regions
with high deduction rates represent geographic concentrations of overbilling.

Tables used:
  - settlement_stat : SS_REGION_ID, SS_OFFICE_ID, SS_FY_YEAR, SS_CLAIM_AMT, SS_APPR_AMT, SS_DED_AMT
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

# ── Query 1A: Region-level deduction summary, full history ───────────────────
QUERY_1A = """
SELECT
    ss.SS_REGION_ID                       AS region_id,
    COUNT(DISTINCT ss.SS_OFFICE_ID)        AS hospitals,
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
WHERE ss.SS_FY_YEAR >= 2021
GROUP BY ss.SS_REGION_ID
ORDER BY total_deducted DESC;
"""

QUERIES = {
    '01a_Regional_Fraud_Hotspots': QUERY_1A,
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
