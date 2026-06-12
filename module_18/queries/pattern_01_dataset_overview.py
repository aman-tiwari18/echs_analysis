"""
Module 18 — Pattern 01: Dataset Overview
Breaks down total claims by audit status (rejected, audited-not-rejected, not-audited)
over the last 5 years.
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
        SUM(cs.CS_NET_CLAIM_AMT) as total_claimed,
        SUM(CASE WHEN cs.CS_SETTLE_DATE IS NOT NULL THEN 1 ELSE 0 END) as settled_claims,
        SUM(CASE WHEN cs.CS_SETTLE_DATE IS NOT NULL THEN cs.CS_NET_CLAIM_AMT ELSE 0 END) as settled_amount,
        SUM(CASE WHEN cs.CS_SETTLE_DATE IS NULL THEN 1 ELSE 0 END) as pending_claims,
        SUM(CASE WHEN cs.CS_SETTLE_DATE IS NULL THEN cs.CS_NET_CLAIM_AMT ELSE 0 END) as pending_amount,
        AVG(cs.CS_NET_CLAIM_AMT) as mean_bill
    FROM claim_submission cs
    JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
    LEFT JOIN audit_query aq ON ci.CI_INTIMATION_ID = aq.AQ_CLAIM_ID
    LEFT JOIN audit_status ast ON ci.CI_INTIMATION_ID = ast.AS_CLAIM_ID
    WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    GROUP BY audit_group;
"""

def run_query():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to SSH {SSH_HOST}...")
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
        mysql_cmd = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{query.replace('\"', '\\\"')}\""
        print("Executing Pattern 01 (Dataset Overview)...")
        stdin, stdout, stderr = client.exec_command(mysql_cmd, timeout=600)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        if error and "mysql: [Warning]" not in error:
            print(f"Error: {error}")
            return
        lines = [l for l in output.split('\n') if l.strip()]
        if len(lines) > 1:
            # Manually calculate 'Total' row
            headers = lines[0].split('\t')
            data_rows = []
            
            tot_claims = 0
            tot_claimed = 0.0
            tot_settled_claims = 0
            tot_settled_amt = 0.0
            tot_pending_claims = 0
            tot_pending_amt = 0.0
            
            for line in lines[1:]:
                row = line.split('\t')
                data_rows.append(row)
                tot_claims += int(row[1])
                tot_claimed += float(row[2]) if row[2] != 'NULL' else 0
                tot_settled_claims += int(row[3]) if row[3] != 'NULL' else 0
                tot_settled_amt += float(row[4]) if row[4] != 'NULL' else 0
                tot_pending_claims += int(row[5]) if row[5] != 'NULL' else 0
                tot_pending_amt += float(row[6]) if row[6] != 'NULL' else 0
            
            mean_bill = tot_claimed / tot_claims if tot_claims > 0 else 0
            
            total_row = [
                'Total', str(tot_claims), str(tot_claimed), str(tot_settled_claims),
                str(tot_settled_amt), str(tot_pending_claims), str(tot_pending_amt), str(mean_bill)
            ]
            
            data_rows.insert(0, total_row)
            
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
            os.makedirs(data_dir, exist_ok=True)
            fn = os.path.join(data_dir, f'01_Dataset_Overview_{ts}.csv')
            with open(fn, 'w', newline='', encoding='utf-8') as f:
                w = csv.writer(f, quoting=csv.QUOTE_ALL)
                w.writerow(headers)
                for row in data_rows:
                    w.writerow(row)
            print(f"Saved {len(data_rows)} rows to {fn}")
        else:
            print("No data found.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    run_query()
