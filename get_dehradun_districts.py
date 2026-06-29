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
        
    print("UTTRAKHAND districts in district_state:")
    utt_districts = execute_query("SELECT DM_DISTRICT_CODE, DM_DISTRICT_NAME FROM district_state WHERE DM_STATE_NAME LIKE '%UTTRAKHAND%' OR DM_STATE_NAME LIKE '%UTTARAKHAND%'")
    print(utt_districts)

    print("Checking office_master structure:")
    print(execute_query("DESCRIBE office_master"))
    
    print("Checking if any offices have Dehradun:")
    print(execute_query("SELECT OM_OFFICE_NAME, OM_DISTRICT_ID, OM_STATE_ID FROM office_master WHERE OM_OFFICE_NAME LIKE '%DEHRADUN%'"))
    
except Exception as e:
    print("Error:", e)
finally:
    client.close()
