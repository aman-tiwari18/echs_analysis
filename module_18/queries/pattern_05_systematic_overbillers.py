"""
Module 18 — Pattern 05: Systematic Over-billers
Hospitals with highest mean UTI deduction %, indicating chronic over-billing.
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

query = """
    SELECT
        om.OM_OFFICE_NAME as hospital_name,
        ci.CI_CR_OFFICE_ID as hospital_id,
        COALESCE(crm.CRM_CITY_NAME, '?') as city,
        COALESCE(sm.SM_STATE_NAME, '?') as state,
        COUNT(*) as total_claims,
        ROUND(AVG(cs.CS_NET_CLAIM_AMT), 0) as mean_bill,
        SUM(cs.CS_NET_CLAIM_AMT) as total_claimed,
        SUM(cs.CS_UTI_APP_AMT) as total_approved,
        ROUND((SUM(cs.CS_NET_CLAIM_AMT) - SUM(cs.CS_UTI_APP_AMT)) / SUM(cs.CS_NET_CLAIM_AMT) * 100, 2) as deduction_pct,
        SUM(CASE WHEN cs.CS_NET_CLAIM_AMT > cs.CS_UTI_APP_AMT AND cs.CS_UTI_APP_AMT > 0
            THEN 1 ELSE 0 END) as deducted_claim_count,
        ROUND(SUM(CASE WHEN cs.CS_NET_CLAIM_AMT > cs.CS_UTI_APP_AMT AND cs.CS_UTI_APP_AMT > 0
            THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as pct_claims_deducted,
        ROUND(AVG(CASE WHEN cs.CS_SETTLE_DATE IS NOT NULL
            THEN DATEDIFF(cs.CS_SETTLE_DATE, cs.CS_SUB_DATE) ELSE NULL END), 0) as mean_appr_delay,
        GROUP_CONCAT(DISTINCT ci.CI_INTIMATION_ID SEPARATOR ', ') as claim_ids
    FROM claim_submission cs
    JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
    LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
    LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
    LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
    WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
      AND cs.CS_SETTLE_DATE IS NOT NULL
      AND cs.CS_UTI_APP_AMT > 0
    GROUP BY ci.CI_CR_OFFICE_ID, om.OM_OFFICE_NAME, crm.CRM_CITY_NAME, sm.SM_STATE_NAME
    HAVING COUNT(*) >= 50
      AND deduction_pct > 5
    ORDER BY deduction_pct DESC;
"""

def run_query():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to SSH {SSH_HOST}...")
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
        mysql_cmd = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{query.replace('\"', '\\\"')}\""
        print("Executing Pattern 05 (Systematic Over-billers)...")
        stdin, stdout, stderr = client.exec_command(mysql_cmd, timeout=600)
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
            fn = os.path.join(data_dir, f'05_Systematic_Overbillers_{ts}.csv')
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
