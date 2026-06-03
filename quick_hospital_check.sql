-- Quick Hospital ID Mapping Check
-- Run this to understand the hospital ID mismatch issue

-- 1. Check sample hospital IDs from claim_intimation
SELECT 'Sample Hospital IDs from claim_intimation:' as info;
SELECT DISTINCT CI_HOSPITAL_ID, COUNT(*) as claim_count
FROM claim_intimation
WHERE CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
GROUP BY CI_HOSPITAL_ID
ORDER BY claim_count DESC
LIMIT 10;

-- 2. Check sample hospital IDs from office_master
SELECT 'Sample Hospital IDs from office_master:' as info;
SELECT OM_OFFICE_ID, OM_OFFICE_NAME, OM_OFFICE_CITY, OM_HOSP_TYPE
FROM office_master
WHERE OM_OFFICE_ENTITY_ID = '6'  -- Usually '6' is hospitals
LIMIT 10;

-- 3. Check if there's a direct match
SELECT 'Direct Match Count:' as info;
SELECT COUNT(DISTINCT ci.CI_HOSPITAL_ID) as total_hosp_in_claims,
       COUNT(DISTINCT om.OM_OFFICE_ID) as matched_with_office_master
FROM claim_intimation ci
LEFT JOIN office_master om ON ci.CI_HOSPITAL_ID = om.OM_OFFICE_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR);

-- 4. Sample unmatched hospital IDs
SELECT 'Top 10 Unmatched Hospital IDs:' as info;
SELECT ci.CI_HOSPITAL_ID, COUNT(*) as claim_count
FROM claim_intimation ci
LEFT JOIN office_master om ON ci.CI_HOSPITAL_ID = om.OM_OFFICE_ID
WHERE om.OM_OFFICE_ID IS NULL
  AND ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
GROUP BY ci.CI_HOSPITAL_ID
ORDER BY claim_count DESC
LIMIT 10;

-- 5. Check for alternate hospital tables
SELECT 'Checking for hospital-related tables:' as info;
SHOW TABLES LIKE '%hospital%';
SHOW TABLES LIKE '%hosp%';
SHOW TABLES LIKE '%clinic%';

-- 6. Check if CI_HOSPITAL_ID might be in a different field
SELECT 'Check office_master alternate ID fields:' as info;
SELECT OM_OFFICE_ID, OM_OFFICE_NAME, OM_EMPANEL_NO, OM_SOURCE_POLY_ID
FROM office_master
LIMIT 5;
