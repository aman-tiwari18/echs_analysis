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
    
    # 1. Get all regions
    regions_raw = execute_query("SELECT ER_REGION_ID, ER_REGION_NAME FROM ecs_region WHERE ER_REGION_ACIVE='Y'")
    
    # 2. Get mapping of regions to states from office_master using OM_RATE_REGION (Assuming it maps to ecs_region)
    # Actually, cghs_region_master has CRM_CDA_REGION_ID and CRM_STATE_ID
    # But wait, what if OM_OFFICE_CGHS_CITY_ID maps to cghs_region_master.CRM_CITY_ID?
    # Let's just find distinct states for each OM_RATE_REGION
    region_state_mapping = execute_query("SELECT DISTINCT OM_RATE_REGION, OM_OFFICE_STATE_ID FROM office_master WHERE OM_RATE_REGION IS NOT NULL AND OM_OFFICE_STATE_ID IS NOT NULL")
    
    print("Region -> State mapping from office_master:")
    print(region_state_mapping)
    
    # Let's get all states
    states = execute_query("SELECT DISTINCT DM_STATE_CODE, DM_STATE_NAME FROM district_state")
    print("States:")
    print(states)

except Exception as e:
    print("Error:", e)
finally:
    client.close()
