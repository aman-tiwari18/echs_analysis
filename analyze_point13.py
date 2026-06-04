#!/usr/bin/env python3
"""
ECHS Module 13 - High-Value Claim Risk Scoring : data extraction.

Runs the Module-13 SQL over the authorised SSH path (paramiko -> samar.iitk.ac.in
-> mysql ECHS) and saves each result as a CSV under module_13/data/.

Design notes
------------
* High-value = CS_GR_CLAIM_AMT > 500000 (gross). That column is NOT indexed, so
  these are full-table scans on claim_submission (~37M rows) -> each heavy query
  takes minutes. Run this in the BACKGROUND.
* We pull the high-value claims ONCE (base scan) and derive Q13a / Q13b / Q13d /
  duplicates / composite scores locally in Python (see build_module13_data.py),
  instead of scanning the 12.5 GB table several times.
* Bulk injection (Q13f) and regional (Q13c) are separate, smaller queries.
* Each CSV is written incrementally; a query whose CSV already exists & is
  non-empty is skipped (pass --force to re-run everything). So a re-run only
  repeats what is missing.

READ-ONLY: every statement is a SELECT. Nothing is modified on the server.
"""
import os
import sys
import csv
import time
import paramiko

SSH_HOST = "samar.iitk.ac.in"
SSH_PORT = 22
SSH_USER = "echs_aman"
SSH_PASS = "aman@2026"

DB_USER = "aman"
DB_PASS = "aman@2026"
DB_NAME = "ECHS"

HV_THRESHOLD = 500000  # Rs 5 lakh (gross). SCOPE: last 5 years (CI_CR_DATE >= now-5y).

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "module_13", "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Per-query read timeout (seconds). Aggregation queries stay silent until the
# full scan completes, so this must comfortably exceed the slowest query.
QUERY_TIMEOUT = 2400

# ---------------------------------------------------------------------------
# Queries. Order: cheapest first so early CSVs appear, heaviest (base) last.
# ---------------------------------------------------------------------------
QUERIES = {
    # Q13c - regional risk distribution (pre-aggregated table, ~20s).
    "q13c_regional": f"""
        SELECT ss.SS_REGION_ID                                        AS region_id,
               er.ER_REGION_NAME                                      AS command,
               SUM(ss.SS_CLAIM_CNT)                                   AS claim_cnt,
               ROUND(SUM(ss.SS_CLAIM_AMT)/1e7, 2)                     AS exposure_cr,
               ROUND(SUM(ss.SS_APPR_AMT)/1e7, 2)                      AS approved_cr,
               ROUND(SUM(ss.SS_DED_AMT)/1e7, 2)                       AS deducted_cr,
               ROUND(SUM(ss.SS_DED_AMT)/NULLIF(SUM(ss.SS_CLAIM_AMT),0)*100, 2) AS ded_pct
        FROM settlement_stat ss
        LEFT JOIN ecs_region er ON TRIM(ss.SS_REGION_ID) = TRIM(er.ER_REGION_ID)
        WHERE ss.SS_YEAR >= YEAR(CURDATE()) - 5
        GROUP BY ss.SS_REGION_ID, er.ER_REGION_NAME
        ORDER BY exposure_cr DESC
    """,

    # Q13f - extreme bulk claim injection: many intimation IDs for one card on
    # one day at one hospital login. Scan of claim_intimation + group-by.
    "q13f_bulk_injection": f"""
        SELECT ci.CI_CARD_ID                                          AS card_id,
               MAX(ci.CI_BENEFICIARY_NAME)                            AS beneficiary,
               ci.CI_HOSPITAL_ID                                      AS hospital_code,
               DATE(ci.CI_CR_DATE)                                    AS creation_date,
               COUNT(DISTINCT ci.CI_INTIMATION_ID)                    AS intimation_count,
               MIN(ci.CI_INTIMATION_ID)                               AS first_intimation_id,
               MAX(ci.CI_INTIMATION_ID)                               AS last_intimation_id
        FROM claim_intimation ci
        WHERE ci.CI_CARD_ID IS NOT NULL AND ci.CI_CARD_ID <> ''
          AND ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
        GROUP BY ci.CI_CARD_ID, DATE(ci.CI_CR_DATE), ci.CI_HOSPITAL_ID
        HAVING intimation_count >= 50
        ORDER BY intimation_count DESC
        LIMIT 300
    """,

    # Base scan - every high-value claim (>Rs 5 lakh gross). Streams with --quick.
    # Q13a / Q13b / Q13d / duplicates / composite scores are all derived from this.
    "high_value_claims_base": f"""
        SELECT ci.CI_CARD_ID                                          AS card_id,
               ci.CI_SERVICE_NO                                       AS service_no,
               ci.CI_BENEFICIARY_NAME                                 AS beneficiary,
               ci.CI_PATIENT_NAME                                     AS patient,
               ci.CI_HOSPITAL_ID                                      AS hospital_code,
               ci.CI_ADMISSION_DATE                                   AS admission_date,
               ci.CI_ADM_AILMENT                                      AS diagnosis,
               ci.CI_INTIMATION_ID                                    AS intimation_id,
               cs.CS_GR_CLAIM_AMT                                     AS claimed,
               cs.CS_UTI_APP_AMT                                      AS approved,
               cs.CS_NET_CLAIM_AMT                                    AS net_claim,
               ci.CI_CR_DATE                                          AS cr_date
        FROM claim_submission cs
        JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
        WHERE cs.CS_GR_CLAIM_AMT > {HV_THRESHOLD}
          AND ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    """,
}

# Queries that stream large row counts benefit from mysql --quick (don't buffer
# the whole result server-side); aggregation queries don't, but it's harmless.
STREAMING = {"high_value_claims_base"}


def one_line(sql: str) -> str:
    return " ".join(sql.split())


def run_query(client, name, sql, force=False):
    out_path = os.path.join(DATA_DIR, name + ".csv")
    if (not force) and os.path.exists(out_path) and os.path.getsize(out_path) > 0:
        print(f"[skip] {name}: {out_path} already exists", flush=True)
        return
    quick = "--quick " if name in STREAMING else ""
    cmd = f'mysql -u {DB_USER} -p{DB_PASS} {DB_NAME} -B {quick}-e "{one_line(sql)}"'
    print(f"[run ] {name} ...", flush=True)
    t0 = time.time()
    chan = client.get_transport().open_session()
    chan.settimeout(QUERY_TIMEOUT)
    chan.exec_command(cmd)
    stdout = chan.makefile("r")
    rows = 0
    tmp_path = out_path + ".part"
    with open(tmp_path, "w", newline="") as f:
        w = csv.writer(f)
        try:
            for line in stdout:
                w.writerow(line.rstrip("\n").split("\t"))
                rows += 1
                if rows % 50000 == 0:
                    print(f"        {name}: {rows:,} rows ...", flush=True)
        except Exception as e:  # timeout / connection issue mid-stream
            print(f"[ERR ] {name} after {rows:,} rows: {e!r}", flush=True)
            raise
    rc = chan.recv_exit_status()
    err = chan.makefile_stderr("r").read()
    if isinstance(err, bytes):
        err = err.decode("utf-8", "replace")
    dt = time.time() - t0
    if rc != 0:
        print(f"[FAIL] {name}: exit {rc} after {dt:.0f}s :: {err[:300]}", flush=True)
        return
    os.replace(tmp_path, out_path)
    print(f"[done] {name}: {rows:,} rows in {dt:.0f}s -> {out_path}", flush=True)
    if err and "Using a password" not in err:
        print(f"        note(stderr): {err[:200]}", flush=True)


def main():
    force = "--force" in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    print(f"[{time.strftime('%H:%M:%S')}] connecting to {SSH_HOST} ...", flush=True)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS, timeout=30)
    print("connected.", flush=True)
    try:
        for name, sql in QUERIES.items():
            if only and name not in only:
                continue
            run_query(client, name, sql, force=force)
    finally:
        client.close()
    print(f"[{time.strftime('%H:%M:%S')}] ALL_DONE", flush=True)


if __name__ == "__main__":
    main()
