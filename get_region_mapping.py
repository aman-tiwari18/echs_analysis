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
        
    print("Checking how many offices have non-null Region ID and District ID:")
    print(execute_query("SELECT COUNT(*) FROM office_master WHERE OM_REGION_ID IS NOT NULL AND OM_DISTRICT_ID IS NOT NULL"))
    
    print("Sample of office_master mapping:")
    print(execute_query("SELECT OM_OFFICE_NAME, OM_REGION_ID, OM_DISTRICT_ID FROM office_master LIMIT 10"))
    
    # Are there other tables like state_district_master or regional_center?
    print("Checking region IDs in office_master:")
    print(execute_query("SELECT DISTINCT OM_REGION_ID FROM office_master"))
    
except Exception as e:
    print("Error:", e)
finally:
    client.close()
