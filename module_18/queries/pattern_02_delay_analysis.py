"""
Module 18 — Pattern 02: Delay Analysis by Audit Category
Computes median delays: discharge→submission, submission→settlement, end-to-end
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
        CASE
            WHEN COALESCE(aq.AQ_RECOVER_AMT, 0) > 0 OR COALESCE(ast.AS_RECOVER_AMT, 0) > 0
                THEN 'Audit-Rejected'
            WHEN aq.AQ_CLAIM_ID IS NOT NULL OR ast.AS_CLAIM_ID IS NOT NULL
                THEN 'Audited-Not-Rejected'
            ELSE 'Not-Audited'
        END as audit_group,
        COUNT(*) as total_claims,
        AVG(DATEDIFF(cs.CS_SUB_DATE, cs.CS_DOD)) as avg_sub_delay,
        AVG(CASE WHEN cs.CS_SETTLE_DATE IS NOT NULL
            THEN DATEDIFF(cs.CS_SETTLE_DATE, cs.CS_SUB_DATE) ELSE NULL END) as avg_appr_delay,
        AVG(CASE WHEN cs.CS_SETTLE_DATE IS NOT NULL
            THEN DATEDIFF(cs.CS_SETTLE_DATE, cs.CS_DOD) ELSE NULL END) as avg_e2e_delay,
        AVG(cs.CS_NET_CLAIM_AMT) as mean_bill,
        SUM(cs.CS_NET_CLAIM_AMT) as total_claimed,
        SUM(CASE WHEN cs.CS_NET_CLAIM_AMT > cs.CS_UTI_APP_AMT AND cs.CS_UTI_APP_AMT > 0
            THEN 1 ELSE 0 END) as deducted_claims,
        AVG(CASE WHEN cs.CS_NET_CLAIM_AMT > 0 AND cs.CS_UTI_APP_AMT > 0
            THEN (cs.CS_NET_CLAIM_AMT - cs.CS_UTI_APP_AMT) / cs.CS_NET_CLAIM_AMT * 100
            ELSE NULL END) as mean_deduction_pct
    FROM claim_submission cs
    JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
    LEFT JOIN audit_query aq ON ci.CI_INTIMATION_ID = aq.AQ_CLAIM_ID
    LEFT JOIN audit_status ast ON ci.CI_INTIMATION_ID = ast.AS_CLAIM_ID
    WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
      AND cs.CS_DOD IS NOT NULL
      AND cs.CS_SUB_DATE IS NOT NULL
    GROUP BY audit_group
    ORDER BY FIELD(audit_group, 'Audit-Rejected', 'Audited-Not-Rejected', 'Not-Audited');
"""

def run_query():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to SSH {SSH_HOST}...")
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
        mysql_cmd = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{query.replace('\"', '\\\"')}\""
        print("Executing Pattern 02 (Delay Analysis)...")
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
            fn = os.path.join(data_dir, f'02_Delay_Analysis_{ts}.csv')
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
