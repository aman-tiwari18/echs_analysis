-- =====================================================================
-- ECHS MODULE 14: PRE-AUTHORIZATION DEVIATION - SQL QUERIES
-- =====================================================================
-- Framework point 14: "Pre-Authorization Deviation" (estimate vs actual; no pre-auth).
-- Scope        : LAST 5 YEARS  (UP_APPLY_DATE / CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)).
-- Primary data : `unlisted_procedure` (live pre-auth system, Dec 2021 -> now).
--                Legacy `pre_auth` (2012-2017, 2,949 rows) is a historical note only.
-- Hospital name: office_master.OM_OFFICE_NAME via claim_intimation.CI_CR_OFFICE_ID
--                (100% coverage; CI_HOSPITAL_ID login is only ~33% populated here).
-- Metrics      : sanction(claim) = SUM(UP_SANC_TOTAL) over deduped procedures;
--                bill/sanction ratio = CS_GR_CLAIM_AMT / sanction; excess = billed - sanction;
--                breach = billed > 1.25 * sanction (">25% above estimate").
-- CAVEAT       : a ratio >1 is structurally expected (the sanction covers only the unlisted
--                procedure, not the whole admission) - flag EXTREME + CONSISTENT ratios.
-- In practice the BASE scan runs once; Q14a/Q14c/top-claims/charts are derived in Python
-- (build_module14_data.py). Q14b runs directly. All queries are READ-ONLY.
-- =====================================================================


-- ---------------------------------------------------------------------
-- BASE: every unlisted-procedure row (last 5y) + its claim context.
-- Per-claim dedup (latest UP_PROCESS_DATE per claim+procedure) + aggregation done in Python.
-- ---------------------------------------------------------------------
SELECT up.UP_CLAIM_ID, up.UP_APPLY_DATE, up.UP_PROCEDURE, up.UP_PROCESS_DATE, up.UP_PROCESS_STAGE,
       up.UP_ESTIMATE_COST, up.UP_SANC_TOTAL, up.UP_TOTAL_COST,
       om.OM_OFFICE_NAME AS hospital, ci.CI_HOSPITAL_ID, ci.CI_CR_OFFICE_ID,
       ci.CI_BENEFICIARY_NAME, ci.CI_CARD_ID, ci.CI_CR_DATE, ci.CI_ADM_AILMENT,
       cs.CS_GR_CLAIM_AMT, cs.CS_UTI_APP_AMT
FROM unlisted_procedure up
JOIN claim_intimation ci ON up.UP_CLAIM_ID = ci.CI_INTIMATION_ID
LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN claim_submission cs ON up.UP_CLAIM_ID = cs.CS_INTIMATION_ID
WHERE up.UP_APPLY_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR);


-- ---------------------------------------------------------------------
-- Q14a: PRE-AUTH DEVIATION BY HOSPITAL (derived in Python from BASE).
-- Per hospital (OM_OFFICE_NAME): claims, SUM sanction, SUM billed, excess billed,
-- aggregate bill/sanction ratio, breach count, UTI disallow %. Ranked by excess. Top 20.
-- Equivalent server-side aggregation:
-- ---------------------------------------------------------------------
SELECT om.OM_OFFICE_NAME AS hospital,
       COUNT(*)                                                        AS claims,
       ROUND(SUM(up.UP_SANC_TOTAL)/1e7, 2)                             AS sanction_cr,
       ROUND(SUM(cs.CS_GR_CLAIM_AMT)/1e7, 2)                           AS billed_cr,
       ROUND(SUM(GREATEST(cs.CS_GR_CLAIM_AMT - up.UP_SANC_TOTAL, 0))/1e7, 2) AS excess_cr,
       ROUND(SUM(cs.CS_GR_CLAIM_AMT)/NULLIF(SUM(up.UP_SANC_TOTAL),0), 2)     AS avg_bill_sanction
FROM unlisted_procedure up
JOIN claim_intimation ci ON up.UP_CLAIM_ID = ci.CI_INTIMATION_ID
LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
JOIN claim_submission cs ON up.UP_CLAIM_ID = cs.CS_INTIMATION_ID
WHERE up.UP_APPLY_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
  AND up.UP_SANC_TOTAL > 0 AND cs.CS_GR_CLAIM_AMT > 0
GROUP BY om.OM_OFFICE_NAME
HAVING claims >= 20
ORDER BY excess_cr DESC
LIMIT 20;
-- (Python version dedups revised UP rows first; this illustrative SQL omits that step.)


-- ---------------------------------------------------------------------
-- Q14b: PRE-AUTH COVERAGE / "NO PRE-AUTH" (control-bypass context). Runs directly.
-- Of high-value (>Rs 1L) claims in the last 5y, how many went through the pre-auth channel.
-- NOTE: most high-value claims are listed-package admissions that do NOT require unlisted-
-- procedure pre-auth, so a low coverage % is expected - this is context, not a fraud count.
-- ---------------------------------------------------------------------
SELECT COUNT(*) AS hv_claims,
       ROUND(SUM(cs.CS_GR_CLAIM_AMT)/1e7, 2) AS hv_gross_cr,
       SUM(up.UP_CLAIM_ID IS NULL) AS no_preauth_claims,
       ROUND(SUM(CASE WHEN up.UP_CLAIM_ID IS NULL THEN cs.CS_GR_CLAIM_AMT ELSE 0 END)/1e7, 2) AS no_preauth_gross_cr
FROM claim_submission cs
JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
LEFT JOIN (SELECT DISTINCT UP_CLAIM_ID FROM unlisted_procedure) up ON cs.CS_INTIMATION_ID = up.UP_CLAIM_ID
WHERE cs.CS_GR_CLAIM_AMT > 100000
  AND ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR);


-- ---------------------------------------------------------------------
-- Q14c: COST ESCALATION BY FINANCIAL YEAR (derived in Python from BASE).
-- Per FY (matched claims): claims, avg sanction, avg billed, avg UTI, bill/sanction ratio.
-- ---------------------------------------------------------------------
-- (Python groups the matched per-claim rows by Indian FY of CI_CR_DATE.)


-- ---------------------------------------------------------------------
-- TYPE-1 (legacy pre_auth, 2012-2017) - historical note only.
-- ---------------------------------------------------------------------
SELECT PA_APPROVED, COUNT(*) AS claims, ROUND(SUM(PA_EST_COST)/1e5, 2) AS est_lakh,
       MIN(PA_DATE) AS first_date, MAX(PA_DATE) AS last_date
FROM pre_auth
GROUP BY PA_APPROVED
ORDER BY claims DESC;

-- =====================================================================
-- END OF MODULE 14 QUERIES
-- =====================================================================
