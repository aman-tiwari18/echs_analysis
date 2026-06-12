import subprocess
import time

scripts = [
    "module_12/queries/pattern_04_yoy_billing_spike.py",
    "module_18/queries/pattern_04_suspicious_claims.py",
    "module_18/queries/pattern_05_systematic_overbillers.py",
    "module_18/queries/pattern_06_untouched_high_billers.py"
]

for script in scripts:
    success = False
    attempts = 0
    while not success and attempts < 3:
        attempts += 1
        print(f"Running {script} (Attempt {attempts})...")
        result = subprocess.run([".venv/bin/python", script], capture_output=True, text=True)
        if "TimeoutError" in result.stderr or "Lost connection" in result.stdout or "Can't connect" in result.stdout:
            print(f"Failed with connection error on {script}, retrying in 30s...")
            time.sleep(30)
        elif result.returncode != 0:
            print(f"Script {script} failed with error:\n{result.stderr}")
            break
        else:
            print(f"Success for {script}!\n{result.stdout}")
            success = True
