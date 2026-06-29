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

    regions = [
        {"id": "1", "name": "NEW DELHI", "states": ["DELHI"]},
        {"id": "2", "name": "MUMBAI", "states": ["MAHARASHTRA"]},
        {"id": "3", "name": "KOLKATA", "states": ["WEST BENGAL", "SIKKIM", "ANDMAN NICOBAR", "TRIPURA", "ASSAM", "MANIPUR", "MEGHALAYA", "MIZORAM", "NAGALAND", "ARUNACHAL PR"]},
        {"id": "4", "name": "BANGALORE", "states": ["KARNATAKA"]},
        {"id": "5", "name": "HYDERABAD", "states": ["ANDHRA PRADESH", "TELANGANA"]},
        {"id": "6", "name": "CHENNAI", "states": ["TAMILNADU", "PONDICHERRY", "KERALA", "LAKHSWADEEP"]},
        {"id": "7", "name": "DEHRADUN", "states": ["UTTRAKHAND"]},
        {"id": "8", "name": "JAIPUR", "states": ["RAJASTHAN"]},
        {"id": "9", "name": "PUNE", "states": ["MAHARASHTRA", "GOA"]},
        {"id": "10", "name": "CHANDIGARH", "states": ["CHANDIGARH", "PUNJAB", "HARYANA", "HIMACHAL PR", "JAMMU KASHMIR"]},
        {"id": "11", "name": "ALLAHABAD", "states": ["UTTAR PRADESH", "MADHYA PRADESH", "CHHATISHGARH"]},
        {"id": "12", "name": "PATNA", "states": ["BIHAR", "JHARKHAND", "ORISSA"]},
        {"id": "13", "name": "AHMEDABAD", "states": ["GUJARAT", "DAMAN AND DIU", "DADR & NAGAR H"]}
    ]
    
    output = []
    
    for r in regions:
        state_list = "','".join(r["states"])
        query = f"SELECT DM_DISTRICT_CODE, DM_DISTRICT_NAME, DM_STATE_NAME FROM district_state WHERE DM_STATE_NAME IN ('{state_list}')"
        res = execute_query(query)
        
        districts = []
        if res:
            lines = res.strip().split('\n')[1:] # skip header
            for line in lines:
                parts = line.split('\t')
                if len(parts) >= 3:
                    districts.append({
                        "district_code": parts[0].strip(),
                        "district_name": parts[1].strip(),
                        "state_name": parts[2].strip()
                    })
                    
        # deduplicate
        unique_districts = {d['district_code']: d for d in districts}.values()
        
        output.append({
            "region_id": r["id"],
            "region_name": r["name"],
            "districts": list(unique_districts)
        })
        
    with open('all_regions_districts.json', 'w') as f:
        json.dump(output, f, indent=2)
        
    print("Successfully generated all_regions_districts.json")

except Exception as e:
    print("Error:", e)
finally:
    client.close()
