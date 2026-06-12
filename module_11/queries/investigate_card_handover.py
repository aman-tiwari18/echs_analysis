"""
Module 11 — Investigation: Card Handover Reconciliation
Investigates service numbers that were previously in the "Card not handed over"
group but now have physical cards assigned.

Tables Used:
  - claim_intimation: CI_SERVICE_NO, CI_CARD_ID, CI_BENEFICIARY_NAME,
                      CI_ADMISSION_DATE, CI_CR_DATE, CI_CR_OFFICE_ID
  - claim_submission: CS_NET_CLAIM_AMT, CS_SETTLE_DATE, CS_UTI_APP_AMT
  - office_master:    OM_OFFICE_NAME (hospital name)

Goal: For each service number, pull ALL claims showing:
  - Which card ID was used (was it 'Card not handed over' or a real card?)
  - When the transition happened
  - How many claims were filed without a card vs with a card
  - Total amounts claimed in each phase
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

# Service numbers to investigate with their card handover dates
CASES = [
    ('03982058A', '2020-01-07', 'Card handed over'),
    ('04257035X', '2018-12-12', 'Card handed over'),
    ('04263969L', '2026-05-25', 'Awaiting collection'),
    ('057287Z',   '2022-09-13', 'Card handed over'),
    ('058152R',   '2022-07-15', 'Card handed over'),
    ('07430369',  '2021-10-26', 'Card handed over'),
]

svc_list = "','".join([c[0] for c in CASES])

# Query 1: Full claim history for each service number
query_detail = f"""
    SELECT
        ci.CI_SERVICE_NO as service_no,
        ci.CI_BENEFICIARY_NAME as beneficiary_name,
        ci.CI_CARD_ID as card_id_used,
        ci.CI_INTIMATION_ID as claim_id,
        ci.CI_ADMISSION_DATE as admission_date,
        ci.CI_CR_DATE as claim_created,
        om.OM_OFFICE_NAME as hospital_name,
        ci.CI_CR_OFFICE_ID as hospital_id,
        cs.CS_NET_CLAIM_AMT as claimed_amount,
        cs.CS_UTI_APP_AMT as approved_amount,
        cs.CS_SETTLE_DATE as settle_date,
        CASE
            WHEN ci.CI_CARD_ID IS NULL OR ci.CI_CARD_ID = '' 
                 OR ci.CI_CARD_ID = 'Card not handed over'
                 OR LENGTH(ci.CI_CARD_ID) <= 4
            THEN 'NO_CARD'
            ELSE 'HAS_CARD'
        END as card_status
    FROM claim_intimation ci
    LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
    LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
    WHERE ci.CI_SERVICE_NO IN ('{svc_list}')
    ORDER BY ci.CI_SERVICE_NO, ci.CI_ADMISSION_DATE;
"""

# Query 2: Summary per service number
query_summary = f"""
    SELECT
        ci.CI_SERVICE_NO as service_no,
        ci.CI_BENEFICIARY_NAME as beneficiary_name,
        COUNT(*) as total_claims,
        SUM(CASE
            WHEN ci.CI_CARD_ID IS NULL OR ci.CI_CARD_ID = ''
                 OR ci.CI_CARD_ID = 'Card not handed over'
                 OR LENGTH(ci.CI_CARD_ID) <= 4
            THEN 1 ELSE 0
        END) as claims_without_card,
        SUM(CASE
            WHEN ci.CI_CARD_ID IS NOT NULL AND ci.CI_CARD_ID != ''
                 AND ci.CI_CARD_ID != 'Card not handed over'
                 AND LENGTH(ci.CI_CARD_ID) > 4
            THEN 1 ELSE 0
        END) as claims_with_card,
        GROUP_CONCAT(DISTINCT ci.CI_CARD_ID ORDER BY ci.CI_CARD_ID SEPARATOR ' | ') as all_card_ids_used,
        MIN(ci.CI_ADMISSION_DATE) as first_claim,
        MAX(ci.CI_ADMISSION_DATE) as last_claim,
        SUM(COALESCE(cs.CS_NET_CLAIM_AMT, 0)) as total_claimed,
        SUM(CASE
            WHEN ci.CI_CARD_ID IS NULL OR ci.CI_CARD_ID = ''
                 OR ci.CI_CARD_ID = 'Card not handed over'
                 OR LENGTH(ci.CI_CARD_ID) <= 4
            THEN COALESCE(cs.CS_NET_CLAIM_AMT, 0) ELSE 0
        END) as claimed_without_card,
        SUM(CASE
            WHEN ci.CI_CARD_ID IS NOT NULL AND ci.CI_CARD_ID != ''
                 AND ci.CI_CARD_ID != 'Card not handed over'
                 AND LENGTH(ci.CI_CARD_ID) > 4
            THEN COALESCE(cs.CS_NET_CLAIM_AMT, 0) ELSE 0
        END) as claimed_with_card,
        COUNT(DISTINCT ci.CI_CR_OFFICE_ID) as hospitals_visited
    FROM claim_intimation ci
    LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
    WHERE ci.CI_SERVICE_NO IN ('{svc_list}')
    GROUP BY ci.CI_SERVICE_NO, ci.CI_BENEFICIARY_NAME
    ORDER BY total_claimed DESC;
"""

def run_query():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to SSH {SSH_HOST}...")
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)

        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        os.makedirs(data_dir, exist_ok=True)

        # Run detail query
        print("Query 1: Full claim history for flagged service numbers...")
        mysql_cmd = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{query_detail.replace('\"', '\\\"')}\""
        stdin, stdout, stderr = client.exec_command(mysql_cmd, timeout=300)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        if error and "mysql: [Warning]" not in error:
            print(f"Error (detail): {error}")
            return

        lines = [l for l in output.split('\n') if l.strip()]
        if len(lines) > 1:
            fn = os.path.join(data_dir, f'01d_Card_Handover_Detail_{ts}.csv')
            with open(fn, 'w', newline='', encoding='utf-8') as f:
                w = csv.writer(f, quoting=csv.QUOTE_ALL)
                for line in lines:
                    w.writerow(line.split('\t'))
            print(f"  Saved {len(lines)-1} detail rows to {fn}")

        # Run summary query
        print("Query 2: Summary per service number...")
        mysql_cmd2 = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{query_summary.replace('\"', '\\\"')}\""
        stdin, stdout, stderr = client.exec_command(mysql_cmd2, timeout=300)
        output2 = stdout.read().decode('utf-8')
        error2 = stderr.read().decode('utf-8')
        if error2 and "mysql: [Warning]" not in error2:
            print(f"Error (summary): {error2}")
            return

        lines2 = [l for l in output2.split('\n') if l.strip()]
        if len(lines2) > 1:
            fn2 = os.path.join(data_dir, f'01d_Card_Handover_Summary_{ts}.csv')
            with open(fn2, 'w', newline='', encoding='utf-8') as f:
                w = csv.writer(f, quoting=csv.QUOTE_ALL)
                # Write header with extra handover info columns
                headers = lines2[0].split('\t')
                headers.extend(['handover_date', 'handover_status'])
                w.writerow(headers)
                # Write data rows with handover info
                for line in lines2[1:]:
                    row = line.split('\t')
                    svc = row[0].strip() if row else ''
                    # Match to our handover data
                    handover_date = ''
                    handover_status = ''
                    for case_svc, case_date, case_status in CASES:
                        if case_svc == svc:
                            handover_date = case_date
                            handover_status = case_status
                            break
                    row.extend([handover_date, handover_status])
                    w.writerow(row)
            print(f"  Saved {len(lines2)-1} summary rows to {fn2}")

        print("\n✅ Investigation complete!")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    run_query()
