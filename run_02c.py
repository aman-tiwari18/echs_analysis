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

QUERY_2C = """
SELECT
    om.OM_OFFICE_ID                      AS hospital_id,
    om.OM_OFFICE_NAME                    AS hospital_name,
    om.OM_HOSP_TYPE                      AS hosp_type,
    COALESCE(om.OM_HOSP_TYPES,'—')       AS hosp_type_desc,
    om.OM_OFFICE_CITY                    AS city,
    COUNT(DISTINCT ci.CI_INTIMATION_ID)  AS total_claims,
    ROUND(SUM(cs.CS_GR_CLAIM_AMT)/1e5,2) AS claimed_lakh,
    ROUND(SUM(cs.CS_UTI_APP_AMT)/1e5,2)  AS approved_lakh,
    ROUND(
        (SUM(cs.CS_GR_CLAIM_AMT)-SUM(cs.CS_UTI_APP_AMT))/SUM(cs.CS_GR_CLAIM_AMT)*100, 2
    )                                    AS deduction_pct,
    GROUP_CONCAT(DISTINCT ci.CI_INTIMATION_ID SEPARATOR ', ') as claim_ids
FROM claim_intimation ci
JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
  AND (om.OM_NABH IS NULL OR om.OM_NABH != 'Y')
  AND cs.CS_GR_CLAIM_AMT IS NOT NULL
GROUP BY om.OM_OFFICE_ID, om.OM_OFFICE_NAME, om.OM_HOSP_TYPE,
         om.OM_HOSP_TYPES, om.OM_OFFICE_CITY
HAVING total_claims >= 200 AND deduction_pct < 5
ORDER BY deduction_pct ASC
LIMIT 30;
"""
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
    rows = [r for r in csv.reader(io.StringIO(out), delimiter='\t') if r]
    return rows

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'module_12', 'data')
os.makedirs(data_dir, exist_ok=True)
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
rows = run_query(client, QUERY_2C)
if len(rows) > 1:
    fname = os.path.join(data_dir, f'02c_non_nabh_low_deduction_{ts}.csv')
    with open(fname, 'w', newline='', encoding='utf-8') as f:
        csv.writer(f, quoting=csv.QUOTE_ALL).writerows(rows)
    print(f"Saved {len(rows)-1} rows to {fname}")
client.close()
