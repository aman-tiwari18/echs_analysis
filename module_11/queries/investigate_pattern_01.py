import paramiko
import csv
import datetime
import os
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
    WITH BaseData AS (
        SELECT 
            ci.CI_CARD_ID as card_number,
            COUNT(DISTINCT ci.CI_BENEFICIARY_NAME) as unique_names,
            -- Remove all non-numeric characters to find the root service number
            COUNT(DISTINCT REGEXP_REPLACE(ci.CI_SERVICE_NO, '[^0-9]', '')) as unique_root_service_numbers,
            GROUP_CONCAT(DISTINCT ci.CI_SERVICE_NO ORDER BY ci.CI_SERVICE_NO SEPARATOR ' | ') as raw_service_numbers,
            GROUP_CONCAT(DISTINCT ci.CI_BENEFICIARY_NAME ORDER BY ci.CI_BENEFICIARY_NAME SEPARATOR ' | ') as beneficiary_names
        FROM claim_intimation ci
        WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
            AND ci.CI_CARD_ID IS NOT NULL
            AND ci.CI_CARD_ID != ''
        GROUP BY ci.CI_CARD_ID
        HAVING COUNT(DISTINCT ci.CI_SERVICE_NO) >= 3
    )
    SELECT 
        COUNT(*) as total_legacy_flagged,
        SUM(CASE WHEN unique_names = 1 THEN 1 ELSE 0 END) as exact_same_name_count,
        SUM(CASE WHEN unique_root_service_numbers = 1 THEN 1 ELSE 0 END) as exact_same_root_service_count,
        SUM(CASE WHEN unique_root_service_numbers > 1 AND unique_names > 1 THEN 1 ELSE 0 END) as true_fraud_count
    FROM BaseData;
"""

def run_investigation():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Connecting to database...")
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
        
        mysql_cmd = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{query.replace('\"', '\\\"')}\""
        
        print("Executing investigative query on Pattern 01...")
        start_time = datetime.datetime.now()
        stdin, stdout, stderr = client.exec_command(mysql_cmd)
        
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        if error and "mysql: [Warning]" not in error:
            print(f"Error: {error}")
            return
            
        print("\n=== Investigation Results ===")
        print(output)
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    run_investigation()
