-- =====================================================================
-- ECHS MODULE 13: HIGH-VALUE CLAIM RISK SCORING - SQL QUERIES
-- =====================================================================
-- Framework point 13: "High-Value Claim Risk Scoring".
-- Scope        : LAST 5 YEARS  (CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR);
--                settlement_stat via SS_YEAR >= YEAR(CURDATE()) - 5).
-- High-value   : CS_GR_CLAIM_AMT > 500000  (Rs 5 lakh, gross claimed).
-- EXPOSURE     : "Total Financial Exposure" = SUM of gross claimed (CS_GR_CLAIM_AMT)
--                of the flagged high-value claims - an approximate gross figure
--                (house convention; actual recoverable amount differs after audit).
-- Deduction %  : (CS_GR_CLAIM_AMT - CS_UTI_APP_AMT) / CS_GR_CLAIM_AMT * 100.
-- Hospital unit: CI_HOSPITAL_ID  (login-code alias e.g. parkhosg, metro,
--                pol.3325, p.chennai, fortis@D1). Module 13 analyses behaviour
--                at the login-code level, so CI_HOSPITAL_ID is correct here.
-- Join         : claim_intimation.CI_INTIMATION_ID = claim_submission.CS_INTIMATION_ID
--
-- In practice the BASE scan runs once; Q13a/Q13b/Q13d/duplicates are derived
-- from it in Python (build_module13_data.py). Q13c/Q13f run directly. READ-ONLY.
-- =====================================================================


-- ---------------------------------------------------------------------
-- BASE SCAN: every high-value claim in the last 5 years. Q13a/Q13b/Q13d/
-- duplicates are derived from this one scan.
-- ---------------------------------------------------------------------
SELECT ci.CI_CARD_ID, ci.CI_SERVICE_NO, ci.CI_BENEFICIARY_NAME, ci.CI_PATIENT_NAME,
       ci.CI_HOSPITAL_ID, ci.CI_ADMISSION_DATE, ci.CI_ADM_AILMENT, ci.CI_INTIMATION_ID,
       cs.CS_GR_CLAIM_AMT, cs.CS_UTI_APP_AMT, cs.CS_NET_CLAIM_AMT, ci.CI_CR_DATE
FROM claim_submission cs
JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
WHERE cs.CS_GR_CLAIM_AMT > 500000
  AND ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR);


-- ---------------------------------------------------------------------
-- Q13a: TOP HIGH-VALUE INDIVIDUAL CLAIMS (>Rs 5 lakh), ranked by exposure
-- (gross claimed), with Ded%. (Derived in Python; equivalent SQL below.)
-- ---------------------------------------------------------------------
SELECT ci.CI_CARD_ID, ci.CI_BENEFICIARY_NAME, ci.CI_PATIENT_NAME, ci.CI_HOSPITAL_ID,
       ci.CI_ADMISSION_DATE, ci.CI_ADM_AILMENT,
       cs.CS_GR_CLAIM_AMT AS exposure, cs.CS_UTI_APP_AMT AS approved,
       ROUND((cs.CS_GR_CLAIM_AMT - cs.CS_UTI_APP_AMT)/NULLIF(cs.CS_GR_CLAIM_AMT,0)*100, 2) AS ded_pct,
       ci.CI_INTIMATION_ID
FROM claim_submission cs
JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
WHERE cs.CS_GR_CLAIM_AMT > 500000
  AND ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
ORDER BY cs.CS_GR_CLAIM_AMT DESC
LIMIT 200;


-- ---------------------------------------------------------------------
-- Q13a-2: REPEAT / DUPLICATE high-value claims - same card, same admission
-- date, same amount across multiple intimation IDs. (Derived in Python.)
-- ---------------------------------------------------------------------
SELECT ci.CI_CARD_ID, ci.CI_BENEFICIARY_NAME, ci.CI_HOSPITAL_ID,
       ci.CI_ADMISSION_DATE, cs.CS_GR_CLAIM_AMT AS exposure,
       COUNT(*) AS dup_count,
       GROUP_CONCAT(ci.CI_INTIMATION_ID) AS intimation_ids
FROM claim_submission cs
JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
WHERE cs.CS_GR_CLAIM_AMT > 500000
  AND ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
GROUP BY ci.CI_CARD_ID, ci.CI_ADMISSION_DATE, cs.CS_GR_CLAIM_AMT
HAVING dup_count > 1
ORDER BY cs.CS_GR_CLAIM_AMT DESC
LIMIT 100;


-- ---------------------------------------------------------------------
-- Q13b: HOSPITAL RISK SCORECARD - high-value claims, avg Ded% > 25%,
-- ranked by absolute deduction. exposure_cr = gross claimed (Rs Cr).
-- (Derived in Python.)
-- ---------------------------------------------------------------------
SELECT ci.CI_HOSPITAL_ID AS hospital_code,
       COUNT(*)                                                       AS hv_claims,
       ROUND(SUM(cs.CS_GR_CLAIM_AMT)/1e7, 2)                          AS exposure_cr,
       ROUND(SUM(cs.CS_GR_CLAIM_AMT - cs.CS_UTI_APP_AMT)/1e7, 2)      AS deducted_cr,
       ROUND(SUM(cs.CS_GR_CLAIM_AMT - cs.CS_UTI_APP_AMT)/NULLIF(SUM(cs.CS_GR_CLAIM_AMT),0)*100, 2) AS avg_ded_pct,
       SUM(cs.CS_UTI_APP_AMT = 0)                                     AS full_ded_claims
FROM claim_submission cs
JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
WHERE cs.CS_GR_CLAIM_AMT > 500000
  AND ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
GROUP BY ci.CI_HOSPITAL_ID
HAVING hv_claims >= 10 AND avg_ded_pct > 25
ORDER BY deducted_cr DESC
LIMIT 50;


-- ---------------------------------------------------------------------
-- Q13c: REGIONAL RISK DISTRIBUTION (pre-aggregated settlement_stat; fast).
-- Region-level proxy. exposure_cr = SS_CLAIM_AMT (Rs Cr). Runs directly.
-- ---------------------------------------------------------------------
SELECT ss.SS_REGION_ID AS region_id, er.ER_REGION_NAME AS command,
       SUM(ss.SS_CLAIM_CNT)                                           AS claim_cnt,
       ROUND(SUM(ss.SS_CLAIM_AMT)/1e7, 2)                             AS exposure_cr,
       ROUND(SUM(ss.SS_APPR_AMT)/1e7, 2)                              AS approved_cr,
       ROUND(SUM(ss.SS_DED_AMT)/1e7, 2)                               AS deducted_cr,
       ROUND(SUM(ss.SS_DED_AMT)/NULLIF(SUM(ss.SS_CLAIM_AMT),0)*100, 2) AS ded_pct
FROM settlement_stat ss
LEFT JOIN ecs_region er ON TRIM(ss.SS_REGION_ID) = TRIM(er.ER_REGION_ID)
WHERE ss.SS_YEAR >= YEAR(CURDATE()) - 5
GROUP BY ss.SS_REGION_ID, er.ER_REGION_NAME
ORDER BY exposure_cr DESC;


-- ---------------------------------------------------------------------
-- Q13d: CHRONIC REPEAT HIGH-VALUE CLAIMANTS (>= 3 high-value claims),
-- ranked by total exposure. (Derived in Python.)
-- ---------------------------------------------------------------------
SELECT ci.CI_CARD_ID, MAX(ci.CI_BENEFICIARY_NAME) AS beneficiary,
       COUNT(*)                                                       AS hv_claims,
       ROUND(SUM(cs.CS_GR_CLAIM_AMT)/1e7, 2)                          AS exposure_cr,
       ROUND(SUM(cs.CS_UTI_APP_AMT)/1e7, 2)                           AS approved_cr,
       ROUND(SUM(cs.CS_GR_CLAIM_AMT - cs.CS_UTI_APP_AMT)/1e7, 2)      AS deducted_cr,
       MIN(ci.CI_ADMISSION_DATE)                                      AS first_admit,
       MAX(ci.CI_ADMISSION_DATE)                                      AS last_admit,
       COUNT(DISTINCT ci.CI_HOSPITAL_ID)                              AS hosp_cnt,
       GROUP_CONCAT(DISTINCT ci.CI_HOSPITAL_ID SEPARATOR ', ')        AS hospitals
FROM claim_submission cs
JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
WHERE cs.CS_GR_CLAIM_AMT > 500000 AND ci.CI_CARD_ID <> ''
  AND ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
GROUP BY ci.CI_CARD_ID
HAVING hv_claims >= 3
ORDER BY exposure_cr DESC
LIMIT 50;


-- ---------------------------------------------------------------------
-- Q13f: EXTREME BULK CLAIM INJECTION - many intimation IDs for one card on
-- one day at one hospital login (last 5 years). Runs directly.
-- Tiers: >300 = system compromise | 100-300 = account abuse | 50-100 = watch.
-- ---------------------------------------------------------------------
SELECT ci.CI_CARD_ID AS card_id, MAX(ci.CI_BENEFICIARY_NAME) AS beneficiary,
       ci.CI_HOSPITAL_ID AS hospital_code, DATE(ci.CI_CR_DATE) AS creation_date,
       COUNT(DISTINCT ci.CI_INTIMATION_ID)                            AS intimation_count,
       MIN(ci.CI_INTIMATION_ID)                                       AS first_intimation_id,
       MAX(ci.CI_INTIMATION_ID)                                       AS last_intimation_id
FROM claim_intimation ci
WHERE ci.CI_CARD_ID IS NOT NULL AND ci.CI_CARD_ID <> ''
  AND ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
GROUP BY ci.CI_CARD_ID, DATE(ci.CI_CR_DATE), ci.CI_HOSPITAL_ID
HAVING intimation_count >= 50
ORDER BY intimation_count DESC
LIMIT 300;

-- =====================================================================
-- END OF MODULE 13 QUERIES
-- =====================================================================
