#!/usr/bin/env python3
"""
ECHS Module 14 - Pre-Authorization Deviation : data extraction.

Pulls the pre-auth / unlisted-procedure data over the authorised SSH path
(paramiko -> samar.iitk.ac.in -> mysql ECHS) into CSVs under module_14/data/.

Design (scope = last 5 years, matching Module 13):
* Type 2 = `unlisted_procedure` (Dec 2021 -> now) is the live pre-auth system and
  the real basis of Module 14. The BASE query pulls every unlisted-procedure row
  joined to its claim (billed/approved/hospital). ~305K rows, fast. Q14a/Q14c/
  charts/top-claims all derive from this in Python (build_module14_data.py).
* Q14b = high-value (>Rs 1L) claims WITHOUT any pre-auth link = control-bypass
  context. One LEFT-JOIN scan of claim_submission (~37M) -> heavy -> run in BG.
* Type 1 = legacy `pre_auth` (2012-2017, tiny) -> a small aggregate for a note.

READ-ONLY: every statement is a SELECT. Run in the background (heavy scans).
"""
import os
import sys
import csv
import time
import paramiko

SSH_HOST, SSH_PORT, SSH_USER, SSH_PASS = "samar.iitk.ac.in", 22, "echs_aman", "aman@2026"
DB_USER, DB_PASS, DB_NAME = "aman", "aman@2026", "ECHS"

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "module_14", "data")
os.makedirs(DATA_DIR, exist_ok=True)
QUERY_TIMEOUT = 2400

QUERIES = {
    # quick: does UP_CLAIM_ID join to claim_intimation?
    "join_check": """
        SELECT COUNT(*) AS up_rows_5y,
               COUNT(ci.CI_INTIMATION_ID) AS matched_intimation,
               COUNT(cs.CS_INTIMATION_ID) AS matched_submission
        FROM unlisted_procedure up
        LEFT JOIN claim_intimation ci ON up.UP_CLAIM_ID = ci.CI_INTIMATION_ID
        LEFT JOIN claim_submission cs ON up.UP_CLAIM_ID = cs.CS_INTIMATION_ID
        WHERE up.UP_APPLY_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    """,

    # quick: legacy pre_auth (Type-1) approval distribution + estimate sum
    "type1_preauth": """
        SELECT COALESCE(NULLIF(TRIM(PA_APPROVED), ''), '(blank)') AS pa_approved,
               COUNT(*) AS claims,
               ROUND(SUM(PA_EST_COST)/1e5, 2) AS est_lakh,
               MIN(PA_DATE) AS first_date, MAX(PA_DATE) AS last_date
        FROM pre_auth
        GROUP BY pa_approved
        ORDER BY claims DESC
    """,

    # BASE: every unlisted-procedure row (last 5y) + its claim context. Streams.
    "up_base": """
        SELECT up.UP_CLAIM_ID, up.UP_APPLY_DATE, up.UP_PROCEDURE, up.UP_PROCESS_DATE,
               up.UP_PROCESS_STAGE, up.UP_ESTIMATE_COST, up.UP_SANC_TOTAL, up.UP_TOTAL_COST,
               om.OM_OFFICE_NAME AS hospital, ci.CI_HOSPITAL_ID, ci.CI_CR_OFFICE_ID,
               ci.CI_BENEFICIARY_NAME, ci.CI_CARD_ID, ci.CI_CR_DATE, ci.CI_ADM_AILMENT,
               cs.CS_GR_CLAIM_AMT, cs.CS_UTI_APP_AMT
        FROM unlisted_procedure up
        JOIN claim_intimation ci ON up.UP_CLAIM_ID = ci.CI_INTIMATION_ID
        LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        LEFT JOIN claim_submission cs ON up.UP_CLAIM_ID = cs.CS_INTIMATION_ID
        WHERE up.UP_APPLY_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    """,

    # Q14b coverage: high-value claims (>Rs 1L) in last 5y with NO pre-auth link. HEAVY.
    "q14b_coverage": """
        SELECT COUNT(*) AS hv_claims,
               ROUND(SUM(cs.CS_GR_CLAIM_AMT)/1e7, 2) AS hv_gross_cr,
               SUM(up.UP_CLAIM_ID IS NULL) AS no_preauth_claims,
               ROUND(SUM(CASE WHEN up.UP_CLAIM_ID IS NULL THEN cs.CS_GR_CLAIM_AMT ELSE 0 END)/1e7, 2) AS no_preauth_gross_cr
        FROM claim_submission cs
        JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
        LEFT JOIN (SELECT DISTINCT UP_CLAIM_ID FROM unlisted_procedure) up ON cs.CS_INTIMATION_ID = up.UP_CLAIM_ID
        WHERE cs.CS_GR_CLAIM_AMT > 100000
          AND ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    """,

    # Q14b sample: top high-value claims with NO pre-auth link. HEAVY.
    "q14b_sample": """
        SELECT ci.CI_BENEFICIARY_NAME, ci.CI_CARD_ID, om.OM_OFFICE_NAME AS hospital,
               ci.CI_ADMISSION_DATE, cs.CS_GR_CLAIM_AMT, cs.CS_UTI_APP_AMT, ci.CI_ADM_AILMENT
        FROM claim_submission cs
        JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
        LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        LEFT JOIN (SELECT DISTINCT UP_CLAIM_ID FROM unlisted_procedure) up ON cs.CS_INTIMATION_ID = up.UP_CLAIM_ID
        WHERE cs.CS_GR_CLAIM_AMT > 100000
          AND ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
          AND up.UP_CLAIM_ID IS NULL
        ORDER BY cs.CS_GR_CLAIM_AMT DESC
        LIMIT 30
    """,
}
STREAMING = {"up_base"}


def one_line(sql):
    return " ".join(sql.split())


def run_query(client, name, sql, force=False):
    out = os.path.join(DATA_DIR, name + ".csv")
    if (not force) and os.path.exists(out) and os.path.getsize(out) > 0:
        print(f"[skip] {name}", flush=True); return
    quick = "--quick " if name in STREAMING else ""
    cmd = f'mysql -u {DB_USER} -p{DB_PASS} {DB_NAME} -B {quick}-e "{one_line(sql)}"'
    print(f"[run ] {name} ...", flush=True); t0 = time.time()
    chan = client.get_transport().open_session(); chan.settimeout(QUERY_TIMEOUT); chan.exec_command(cmd)
    rows = 0; tmp = out + ".part"
    with open(tmp, "w", newline="") as f:
        w = csv.writer(f)
        for line in chan.makefile("r"):
            w.writerow(line.rstrip("\n").split("\t")); rows += 1
            if rows % 50000 == 0:
                print(f"        {name}: {rows:,} rows ...", flush=True)
    rc = chan.recv_exit_status()
    err = chan.makefile_stderr("r").read()
    if isinstance(err, bytes):
        err = err.decode("utf-8", "replace")
    if rc != 0:
        print(f"[FAIL] {name}: exit {rc} :: {err[:300]}", flush=True); return
    os.replace(tmp, out)
    print(f"[done] {name}: {rows:,} rows in {time.time()-t0:.0f}s", flush=True)
    if err and "Using a password" not in err:
        print(f"        note: {err[:200]}", flush=True)


def main():
    force = "--force" in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    print(f"[{time.strftime('%H:%M:%S')}] connecting to {SSH_HOST} ...", flush=True)
    c = paramiko.SSHClient(); c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS, timeout=30)
    print("connected.", flush=True)
    try:
        for name, sql in QUERIES.items():
            if only and name not in only:
                continue
            run_query(c, name, sql, force=force)
    finally:
        c.close()
    print(f"[{time.strftime('%H:%M:%S')}] ALL_DONE", flush=True)


if __name__ == "__main__":
    main()
