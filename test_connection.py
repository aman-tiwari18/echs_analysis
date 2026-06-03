import paramiko
import datetime

SSH_HOST = 'samar.iitk.ac.in'
SSH_PORT = 22
SSH_USER = 'echs_aman'
SSH_PASS = 'aman@2026'
DB_USER = 'aman'
DB_PASS = 'aman@2026'
DB_NAME = 'ECHS'

print(f"Starting connection test at {datetime.datetime.now()}")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print(f"Connecting to {SSH_HOST}...")
    client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS, timeout=30)
    print("✓ SSH Connected")
    
    # Test simple query
    print("Testing simple query...")
    mysql_cmd = f'mysql -u {DB_USER} -p{DB_PASS} {DB_NAME} -B -e "SELECT COUNT(*) as count FROM claim_intimation WHERE CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR) LIMIT 1;"'
    stdin, stdout, stderr = client.exec_command(mysql_cmd, timeout=60)
    
    out = stdout.read().decode('utf-8')
    err = stderr.read().decode('utf-8')
    
    print(f"Output: {out}")
    if err and 'Using a password' not in err:
        print(f"Error: {err}")
    
    print(f"✓ Test completed at {datetime.datetime.now()}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
    print("Connection closed")
