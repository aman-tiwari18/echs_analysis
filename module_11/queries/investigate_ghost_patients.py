"""
Module 11 — Investigation: Ghost Patient Detection
Finds service numbers that ONLY ever filed claims using dummy card IDs
(like 'Card not handed over', '01', blank, etc.) and have ZERO claims
with a real physical ECHS card anywhere in the entire system.

These are the truly suspicious cases — legitimate veterans always have
at least one claim with their real card number.

Tables Used:
  - claim_intimation: CI_SERVICE_NO, CI_CARD_ID, CI_BENEFICIARY_NAME,
                      CI_ADMISSION_DATE, CI_CR_OFFICE_ID
  - claim_submission: CS_NET_CLAIM_AMT, CS_UTI_APP_AMT
  - office_master:    OM_OFFICE_NAME (hospital name)
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

# Step 1: Find service numbers that used dummy card IDs
# Step 2: Exclude those who also have claims with real cards
# Result: People who ONLY have dummy cards = potential ghost patients

query = """
    SELECT
        ci.CI_SERVICE_NO as service_no,
        ci.CI_BENEFICIARY_NAME as beneficiary_name,
        GROUP_CONCAT(DISTINCT ci.CI_CARD_ID ORDER BY ci.CI_CARD_ID SEPARATOR ' | ') as card_ids_used,
        COUNT(*) as total_claims,
        SUM(COALESCE(cs.CS_NET_CLAIM_AMT, 0)) as total_claimed,
        SUM(COALESCE(cs.CS_UTI_APP_AMT, 0)) as total_approved,
        MIN(ci.CI_ADMISSION_DATE) as first_claim,
        MAX(ci.CI_ADMISSION_DATE) as last_claim,
        DATEDIFF(MAX(ci.CI_ADMISSION_DATE), MIN(ci.CI_ADMISSION_DATE)) as span_days,
        COUNT(DISTINCT ci.CI_CR_OFFICE_ID) as hospitals_visited,
        GROUP_CONCAT(DISTINCT CONCAT(ci.CI_CR_OFFICE_ID, ':', COALESCE(om.OM_OFFICE_NAME, 'Unknown'))
            ORDER BY ci.CI_CR_OFFICE_ID SEPARATOR ' | ') as hospitals_list,
        GROUP_CONCAT(DISTINCT CONCAT(COALESCE(crm.CRM_CITY_NAME,'?'), '-', COALESCE(sm.SM_STATE_NAME,'?'))
            ORDER BY crm.CRM_CITY_NAME SEPARATOR ' | ') as locations
    FROM claim_intimation ci
    LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
    LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
    LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
    LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
    WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
      AND (
          ci.CI_CARD_ID IS NULL
          OR ci.CI_CARD_ID = ''
          OR ci.CI_CARD_ID = 'Card not handed over'
          OR ci.CI_CARD_ID IN ('0', '00', '01', '1', 'NA', 'N/A', 'na', 'nil', 'NIL', 'None', 'NONE', 'null')
          OR LENGTH(TRIM(ci.CI_CARD_ID)) <= 3
      )
      AND ci.CI_SERVICE_NO IS NOT NULL
      AND ci.CI_SERVICE_NO != ''
    GROUP BY ci.CI_SERVICE_NO, ci.CI_BENEFICIARY_NAME
    HAVING ci.CI_SERVICE_NO NOT IN (
        SELECT DISTINCT ci2.CI_SERVICE_NO
        FROM claim_intimation ci2
        WHERE ci2.CI_SERVICE_NO IS NOT NULL
          AND ci2.CI_SERVICE_NO != ''
          AND ci2.CI_CARD_ID IS NOT NULL
          AND ci2.CI_CARD_ID != ''
          AND ci2.CI_CARD_ID != 'Card not handed over'
          AND ci2.CI_CARD_ID NOT IN ('0', '00', '01', '1', 'NA', 'N/A', 'na', 'nil', 'NIL', 'None', 'NONE', 'null')
          AND LENGTH(TRIM(ci2.CI_CARD_ID)) > 3
    )
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

        print("Executing Ghost Patient Detection query...")
        print("(Finding service numbers with ONLY dummy card IDs, no real card ever)")
        mysql_cmd = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{query.replace('\"', '\\\"')}\""
        stdin, stdout, stderr = client.exec_command(mysql_cmd, timeout=600)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        if error and "mysql: [Warning]" not in error:
            print(f"Error: {error}")
            return

        lines = [l for l in output.split('\n') if l.strip()]
        if len(lines) > 1:
            fn = os.path.join(data_dir, f'01e_Ghost_Patients_No_Real_Card_{ts}.csv')
            with open(fn, 'w', newline='', encoding='utf-8') as f:
                w = csv.writer(f, quoting=csv.QUOTE_ALL)
                for line in lines:
                    w.writerow(line.split('\t'))
            print(f"\n🔴 FOUND {len(lines)-1} suspicious service numbers!")
            print(f"   These people filed claims but NEVER had a real ECHS card.")
            print(f"   Saved to {fn}")

            # Print top 10
            print(f"\nTop 10 by amount claimed:")
            for i, line in enumerate(lines[1:11]):
                row = line.split('\t')
                svc = row[0] if len(row) > 0 else '?'
                name = row[1] if len(row) > 1 else '?'
                cards = row[2] if len(row) > 2 else '?'
                claims = row[3] if len(row) > 3 else '?'
                amt = row[4] if len(row) > 4 else '0'
                try:
                    amt_fmt = f"₹{float(amt):,.0f}"
                except:
                    amt_fmt = amt
                print(f"  {i+1}. {svc} | {name[:25]} | {claims} claims | {amt_fmt} | Card: {cards[:30]}")
        else:
            print("No ghost patients found.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    run_query()
