import paramiko, os
from dotenv import load_dotenv
load_dotenv()

SSH_HOST = os.getenv('SSH_HOST')
SSH_PORT = int(os.getenv('SSH_PORT', 22))
SSH_USER = os.getenv('SSH_USER')
SSH_PASS = os.getenv('SSH_PASS')
DB_USER  = os.getenv('DB_USER')
DB_PASS  = os.getenv('DB_PASS')
DB_NAME  = os.getenv('DB_NAME')

query = "SELECT COUNT(*) FROM claim_intimation WHERE CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR);"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
mysql_cmd = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{query}\""
stdin, stdout, stderr = client.exec_command(mysql_cmd, timeout=600)
print(stdout.read().decode('utf-8'))
client.close()
