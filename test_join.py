import paramiko
import os
import json
from dotenv import load_dotenv

load_dotenv()

SSH_HOST = os.getenv('SSH_HOST')
SSH_PORT = int(os.getenv('SSH_PORT', 22))
SSH_USER = os.getenv('SSH_USER')
SSH_PASS = os.getenv('SSH_PASS')
DB_USER  = os.getenv('DB_USER')
DB_PASS  = os.getenv('DB_PASS')
DB_NAME  = os.getenv('DB_NAME')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS, timeout=30)
    
    def execute_query(query):
        cmd = f'mysql -u {DB_USER} -p{DB_PASS} {DB_NAME} -B -e "{query}"'
        stdin, stdout, stderr = client.exec_command(cmd)
        return stdout.read().decode('utf-8')
    
    print("Testing Region -> State mapping in cghs_region_master:")
    print(execute_query("SELECT * FROM cghs_region_master LIMIT 10"))

    print("Checking if ecs_region maps to cghs_region_master:")
    q = """
    SELECT r.ER_REGION_NAME, crm.CRM_STATE_ID 
    FROM ecs_region r 
    JOIN cghs_region_master crm ON r.ER_REGION_ID = crm.CRM_CDA_REGION_ID 
    LIMIT 10
    """
    print(execute_query(q))
    
    # Just in case, also check if state_district_master maps anything
    print("state_district_master:")
    print(execute_query("SELECT * FROM state_district_master LIMIT 5"))

except Exception as e:
    print("Error:", e)
finally:
    client.close()
