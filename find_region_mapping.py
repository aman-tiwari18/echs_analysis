import paramiko
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

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS, timeout=30)
    
    def execute_query(query):
        cmd = f'mysql -u {DB_USER} -p{DB_PASS} {DB_NAME} -B -e "{query}"'
        stdin, stdout, stderr = client.exec_command(cmd)
        return stdout.read().decode('utf-8')
        
    print("Tables with 'region':")
    print(execute_query("SHOW TABLES LIKE '%region%'"))
    
    print("Tables with 'office':")
    print(execute_query("SHOW TABLES LIKE '%office%'"))
    
    print("Tables with 'poly':")
    print(execute_query("SHOW TABLES LIKE '%poly%'"))
    
    print("Columns in office_master:")
    print(execute_query("SHOW COLUMNS FROM office_master"))
    
except Exception as e:
    print("Error:", e)
finally:
    client.close()
