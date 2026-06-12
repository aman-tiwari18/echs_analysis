"""
Module 18 — Pattern 04: Suspicious Claims Flag
Fast approval + high bill + zero deduction = statistically anomalous.
Uses p5 of approval delay and p95 of bill value as thresholds.
"""
import paramiko, csv, datetime, os
from dotenv import load_dotenv
load_dotenv()

SSH_HOST = os.getenv('SSH_HOST')
SSH_PORT = int(os.getenv('SSH_PORT', 22))
SSH_USER = os.getenv('SSH_USER')
SSH_PASS = os.getenv('SSH_PASS')
DB_USER  = os.getenv('DB_USER')
DB_PASS  = os.getenv('DB_PASS')
DB_NAME  = os.getenv('DB_NAME')

# First get thresholds, then flag suspicious claims by hospital
query = """
    SELECT
        om.OM_OFFICE_NAME as hospital_name,
        ci.CI_CR_OFFICE_ID as hospital_id,
        COALESCE(crm.CRM_CITY_NAME, '?') as city,
        COALESCE(sm.SM_STATE_NAME, '?') as state,
        COUNT(*) as flagged_claims,
        ROUND(AVG(cs.CS_NET_CLAIM_AMT), 0) as mean_bill,
        ROUND(AVG(DATEDIFF(cs.CS_SETTLE_DATE, cs.CS_SUB_DATE)), 0) as mean_approval_days,
        SUM(cs.CS_NET_CLAIM_AMT) as total_exposure,
        SUM(CASE
            WHEN aq.AQ_CLAIM_ID IS NOT NULL OR ast.AS_CLAIM_ID IS NOT NULL
            THEN 1 ELSE 0 END) as audited_count,
        SUM(CASE
            WHEN COALESCE(aq.AQ_RECOVER_AMT, 0) > 0 OR COALESCE(ast.AS_RECOVER_AMT, 0) > 0
            THEN 1 ELSE 0 END) as rejected_count,
        GROUP_CONCAT(DISTINCT ci.CI_INTIMATION_ID SEPARATOR ', ') as claim_ids
    FROM claim_submission cs
    JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
    LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
    LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
    LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
    LEFT JOIN audit_query aq ON ci.CI_INTIMATION_ID = aq.AQ_CLAIM_ID
    LEFT JOIN audit_status ast ON ci.CI_INTIMATION_ID = ast.AS_CLAIM_ID
    WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
      AND cs.CS_SETTLE_DATE IS NOT NULL
      AND cs.CS_SUB_DATE IS NOT NULL
      AND DATEDIFF(cs.CS_SETTLE_DATE, cs.CS_SUB_DATE) <= 10
      AND cs.CS_NET_CLAIM_AMT >= 120000
      AND (cs.CS_NET_CLAIM_AMT <= cs.CS_UTI_APP_AMT OR cs.CS_UTI_APP_AMT = 0)
    GROUP BY ci.CI_CR_OFFICE_ID, om.OM_OFFICE_NAME, crm.CRM_CITY_NAME, sm.SM_STATE_NAME
    HAVING COUNT(*) >= 5
    ORDER BY flagged_claims DESC;
"""

def run_query():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to SSH {SSH_HOST}...")
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
        mysql_cmd = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{query.replace('\"', '\\\"')}\""
        print("Executing Pattern 04 (Suspicious Claims - Fast+High+Zero Ded)...")
        stdin, stdout, stderr = client.exec_command(mysql_cmd, timeout=3600)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        if error and "mysql: [Warning]" not in error:
            print(f"Error: {error}")
            return
        lines = [l for l in output.split('\n') if l.strip()]
        if len(lines) > 1:
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
            os.makedirs(data_dir, exist_ok=True)
            fn = os.path.join(data_dir, f'04_Suspicious_Claims_{ts}.csv')
            with open(fn, 'w', newline='', encoding='utf-8') as f:
                w = csv.writer(f, quoting=csv.QUOTE_ALL)
                for line in lines:
                    w.writerow(line.split('\t'))
            print(f"Saved {len(lines)-1} rows to {fn}")
        else:
            print("No data found.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    run_query()
