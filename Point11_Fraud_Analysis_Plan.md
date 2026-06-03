# ECHS Fraud Analytics - Point 11: Identity Fraud Detection

## Overview
This document outlines the fraud detection patterns for Point 11 based on the ECHS Fraud Analytics Framework. The focus is on detecting identity-related frauds including ID duplication, simultaneous admissions, repeated claims, and predictive identity misuse.

## Data Collection Period
**Last 5 Years Data** - From 2020-01-01 to Present

---

## 1. IDENTIFIED FRAUD PATTERNS

### Pattern 1: Duplicate Card IDs (Same ECHS Card Used Multiple Times)
**Description**: Multiple beneficiaries using the same ECHS card number

**Key Tables**:
- `benf_master_live` - Beneficiary master data
- `claim_intimation` - Claim records with card information
- `claim_submission` - Submitted claims

**Detection Logic**: Find card IDs associated with multiple different beneficiaries or service numbers

---

### Pattern 2: Simultaneous Admissions (Same Patient, Different Hospitals)
**Description**: Same beneficiary admitted to multiple hospitals on overlapping dates

**Key Tables**:
- `claim_intimation` - Admission dates and hospital info
- `claim_submission` - Discharge dates
- `hospital_master` - Hospital details

**Detection Logic**: Identify cases where admission period overlaps for same beneficiary at different locations

---

### Pattern 3: Repeated Claims (Duplicate Bills/Claims)
**Description**: Same claim submitted multiple times or exact duplicate claims

**Key Tables**:
- `claim_intimation` - Claim basic info
- `claim_submission` - Bill numbers, amounts, dates
- `expenses_details` - Itemized expenses

**Detection Logic**: Detect duplicate bill numbers, identical amounts, or same treatment dates

---

### Pattern 4: Identity Misuse - Wrong Relationship Claims
**Description**: Dependent relationships that don't match beneficiary records or impossible relationships

**Key Tables**:
- `benf_master_live` - Beneficiary and dependent master
- `claim_intimation` - Patient and beneficiary relationship
- `dependent_master_live` - Dependent details
- `relation_master` - Valid relationship types

**Detection Logic**: Verify age-relationship consistency, duplicate dependents

---

### Pattern 5: Mobile Number Rings (Multiple Cards, Same Mobile)
**Description**: Multiple ECHS cards registered with same mobile number indicating potential fraud ring

**Key Tables**:
- `benf_master_live` - Mobile numbers
- `claim_intimation` - Contact details
- `claim_submission` - Claim data

**Detection Logic**: Find mobile numbers associated with unusually high number of cards

---

### Pattern 6: UID Number Duplication
**Description**: Same Aadhaar/UID used for multiple beneficiaries

**Key Tables**:
- `claim_intimation` - UID numbers
- `benf_master_live` - Beneficiary UID

**Detection Logic**: Identify UID numbers linked to multiple service numbers or cards

---

### Pattern 7: Doctor/Hospital Teleportation
**Description**: Same doctor treating patients at geographically distant hospitals on same day

**Key Tables**:
- `claim_intimation` - Treatment doctor, hospital, dates
- `hospital_master` - Hospital location
- `cghs_region_master` - Geographic regions

**Detection Logic**: Detect physically impossible scenarios of same doctor at multiple distant locations

---

### Pattern 8: Post-Death Claims (Lazarus Claims)
**Description**: Claims submitted after beneficiary's recorded death date

**Key Tables**:
- `claim_intimation` - Death date (CI_EXP_DOD), admission date
- `claim_submission` - Submission date
- `benf_master_live` - Death date (BM_DOM)

**Detection Logic**: Compare claim dates with death dates

---

### Pattern 9: Impossible Dependent Claims
**Description**: Claims for dependents who shouldn't be eligible (age, relationship issues)

**Key Tables**:
- `claim_intimation` - Patient age, relationship
- `benf_master_live` - Beneficiary DOB
- `dependent_master_live` - Dependent DOB, relationship

**Detection Logic**: Age validation, eligibility rules

---

### Pattern 10: Chronic Stay / Forever Patient
**Description**: Patients with unreasonably long hospital stays or continuous readmissions

**Key Tables**:
- `claim_intimation` - Admission dates
- `claim_submission` - Discharge dates, DOD
- `intimation_history` - Claim history

**Detection Logic**: Calculate admission duration, frequency of same patient claims

---

## 2. DATABASE TABLES MAPPING

### Primary Tables:
1. **benf_master_live** - Core beneficiary information (Card No, Service No, DOB, Mobile, UID)
2. **claim_intimation** - Claim initiation data (Card ID, Patient details, Hospital, Dates)
3. **claim_submission** - Claim submission details (Bill No, Amounts, Dates)
4. **dependent_master_live** - Dependent information
5. **hospital_master** - Hospital details and location
6. **cghs_region_master** - Geographic region information
7. **relation_master** - Valid relationship types
8. **intimation_history** - Historical claim data

### Supporting Tables:
- `claim_remarks` - Additional claim notes
- `claim_changes` - Modifications to claims
- `service_type_master` - Service types
- `rank_master` - Rank information
- `state_master` - State details
- `expenses_details` - Expense breakdowns (if needed)

---

## 3. SQL QUERIES STRUCTURE

### 3.1 Duplicate Card ID Detection
```sql
-- Find cards associated with multiple beneficiaries (last 5 years)
SELECT 
    ci.CI_CARD_ID,
    COUNT(DISTINCT ci.CI_SERVICE_NO) as unique_service_numbers,
    COUNT(DISTINCT ci.CI_BENEFICIARY_NAME) as unique_names,
    COUNT(DISTINCT ci.CI_INTIMATION_ID) as total_claims,
    SUM(cs.CS_NET_CLAIM_AMT) as total_claimed_amount,
    GROUP_CONCAT(DISTINCT ci.CI_SERVICE_NO) as service_numbers,
    GROUP_CONCAT(DISTINCT ci.CI_BENEFICIARY_NAME) as beneficiary_names
FROM claim_intimation ci
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    AND ci.CI_CARD_ID IS NOT NULL
    AND ci.CI_CARD_ID != ''
GROUP BY ci.CI_CARD_ID
HAVING COUNT(DISTINCT ci.CI_SERVICE_NO) > 1
ORDER BY total_claimed_amount DESC;
```

### 3.2 Simultaneous Admissions Detection
```sql
-- Find beneficiaries admitted to multiple hospitals with overlapping dates
SELECT 
    a.CI_SERVICE_NO,
    a.CI_BENEFICIARY_NAME,
    a.CI_INTIMATION_ID as claim_id_1,
    a.CI_ADMISSION_DATE as admission_date_1,
    a.CI_HOSPITAL_ID as hospital_1,
    b.CI_INTIMATION_ID as claim_id_2,
    b.CI_ADMISSION_DATE as admission_date_2,
    b.CI_HOSPITAL_ID as hospital_2,
    DATEDIFF(
        LEAST(COALESCE(cs1.CS_DOD, CURDATE()), COALESCE(cs2.CS_DOD, CURDATE())),
        GREATEST(a.CI_ADMISSION_DATE, b.CI_ADMISSION_DATE)
    ) as overlap_days,
    cs1.CS_NET_CLAIM_AMT as amount_1,
    cs2.CS_NET_CLAIM_AMT as amount_2
FROM claim_intimation a
JOIN claim_intimation b ON a.CI_SERVICE_NO = b.CI_SERVICE_NO
    AND a.CI_INTIMATION_ID < b.CI_INTIMATION_ID
    AND a.CI_HOSPITAL_ID != b.CI_HOSPITAL_ID
LEFT JOIN claim_submission cs1 ON a.CI_INTIMATION_ID = cs1.CS_INTIMATION_ID
LEFT JOIN claim_submission cs2 ON b.CI_INTIMATION_ID = cs2.CS_INTIMATION_ID
WHERE a.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    AND b.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    AND (
        (a.CI_ADMISSION_DATE BETWEEN b.CI_ADMISSION_DATE AND COALESCE(cs2.CS_DOD, DATE_ADD(b.CI_ADMISSION_DATE, INTERVAL 30 DAY)))
        OR
        (b.CI_ADMISSION_DATE BETWEEN a.CI_ADMISSION_DATE AND COALESCE(cs1.CS_DOD, DATE_ADD(a.CI_ADMISSION_DATE, INTERVAL 30 DAY)))
    )
ORDER BY a.CI_SERVICE_NO, a.CI_ADMISSION_DATE;
```

### 3.3 Repeated/Duplicate Claims Detection
```sql
-- Find duplicate bill numbers or identical claims
SELECT 
    cs.CS_BILL_NO,
    COUNT(*) as duplicate_count,
    SUM(cs.CS_NET_CLAIM_AMT) as total_amount,
    GROUP_CONCAT(ci.CI_INTIMATION_ID) as claim_ids,
    GROUP_CONCAT(ci.CI_SERVICE_NO) as service_numbers,
    GROUP_CONCAT(ci.CI_BENEFICIARY_NAME) as beneficiary_names,
    GROUP_CONCAT(ci.CI_HOSPITAL_ID) as hospital_ids
FROM claim_submission cs
JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
WHERE cs.CS_SUB_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    AND cs.CS_BILL_NO IS NOT NULL
    AND cs.CS_BILL_NO != ''
GROUP BY cs.CS_BILL_NO
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC, total_amount DESC;
```

### 3.4 Mobile Number Rings Detection
```sql
-- Find mobile numbers associated with multiple cards/beneficiaries
SELECT 
    ci.CI_MOBILE,
    COUNT(DISTINCT ci.CI_CARD_ID) as unique_cards,
    COUNT(DISTINCT ci.CI_SERVICE_NO) as unique_service_numbers,
    COUNT(DISTINCT ci.CI_INTIMATION_ID) as total_claims,
    SUM(cs.CS_NET_CLAIM_AMT) as total_claimed_amount,
    GROUP_CONCAT(DISTINCT ci.CI_CARD_ID) as card_numbers,
    GROUP_CONCAT(DISTINCT ci.CI_SERVICE_NO) as service_numbers
FROM claim_intimation ci
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    AND ci.CI_MOBILE IS NOT NULL
    AND ci.CI_MOBILE != ''
    AND LENGTH(ci.CI_MOBILE) = 10
GROUP BY ci.CI_MOBILE
HAVING COUNT(DISTINCT ci.CI_CARD_ID) >= 5
ORDER BY unique_cards DESC, total_claimed_amount DESC;
```

### 3.5 UID Duplication Detection
```sql
-- Find UID numbers associated with multiple beneficiaries
SELECT 
    ci.CI_UID_NUMBER,
    COUNT(DISTINCT ci.CI_SERVICE_NO) as unique_service_numbers,
    COUNT(DISTINCT ci.CI_CARD_ID) as unique_cards,
    COUNT(DISTINCT ci.CI_INTIMATION_ID) as total_claims,
    SUM(cs.CS_NET_CLAIM_AMT) as total_claimed_amount,
    GROUP_CONCAT(DISTINCT ci.CI_SERVICE_NO) as service_numbers,
    GROUP_CONCAT(DISTINCT ci.CI_CARD_ID) as card_numbers,
    GROUP_CONCAT(DISTINCT ci.CI_BENEFICIARY_NAME) as names
FROM claim_intimation ci
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    AND ci.CI_UID_NUMBER IS NOT NULL
    AND ci.CI_UID_NUMBER != ''
    AND LENGTH(ci.CI_UID_NUMBER) = 12
GROUP BY ci.CI_UID_NUMBER
HAVING COUNT(DISTINCT ci.CI_SERVICE_NO) > 1
ORDER BY unique_service_numbers DESC, total_claimed_amount DESC;
```

### 3.6 Post-Death Claims (Lazarus) Detection
```sql
-- Find claims submitted after death date
SELECT 
    ci.CI_INTIMATION_ID,
    ci.CI_SERVICE_NO,
    ci.CI_CARD_ID,
    ci.CI_BENEFICIARY_NAME,
    ci.CI_PATIENT_NAME,
    ci.CI_RELATION_ID,
    cs.CS_DOD as death_date_in_claim,
    ci.CI_ADMISSION_DATE,
    cs.CS_SUB_DATE as claim_submission_date,
    DATEDIFF(ci.CI_ADMISSION_DATE, cs.CS_DOD) as days_after_death_admission,
    DATEDIFF(cs.CS_SUB_DATE, cs.CS_DOD) as days_after_death_submission,
    cs.CS_NET_CLAIM_AMT as claimed_amount,
    ci.CI_HOSPITAL_ID,
    ci.CI_INT_STAGE,
    ci.CI_INT_STATUS
FROM claim_intimation ci
JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    AND cs.CS_DOD IS NOT NULL
    AND (
        ci.CI_ADMISSION_DATE > cs.CS_DOD
        OR cs.CS_SUB_DATE > DATE_ADD(cs.CS_DOD, INTERVAL 90 DAY)
    )
ORDER BY days_after_death_admission DESC;
```

### 3.7 Chronic Stay / Forever Patient Detection
```sql
-- Find patients with unusually long hospital stays
SELECT 
    ci.CI_SERVICE_NO,
    ci.CI_CARD_ID,
    ci.CI_BENEFICIARY_NAME,
    ci.CI_INTIMATION_ID,
    ci.CI_ADMISSION_DATE,
    cs.CS_DOD as discharge_date,
    DATEDIFF(COALESCE(cs.CS_DOD, CURDATE()), ci.CI_ADMISSION_DATE) as stay_duration_days,
    ci.CI_HOSPITAL_ID,
    ci.CI_ADM_AILMENT,
    cs.CS_NET_CLAIM_AMT as claimed_amount,
    ci.CI_INT_STAGE,
    ci.CI_INT_STATUS
FROM claim_intimation ci
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    AND ci.CI_ADMISSION_DATE IS NOT NULL
    AND DATEDIFF(COALESCE(cs.CS_DOD, CURDATE()), ci.CI_ADMISSION_DATE) > 90
ORDER BY stay_duration_days DESC;
```

### 3.8 Repeated Claims by Same Patient Detection
```sql
-- Find beneficiaries with high frequency of claims
SELECT 
    ci.CI_SERVICE_NO,
    ci.CI_CARD_ID,
    ci.CI_BENEFICIARY_NAME,
    COUNT(DISTINCT ci.CI_INTIMATION_ID) as total_claims,
    COUNT(DISTINCT ci.CI_HOSPITAL_ID) as unique_hospitals,
    COUNT(DISTINCT YEAR(ci.CI_ADMISSION_DATE)) as years_with_claims,
    MIN(ci.CI_ADMISSION_DATE) as first_claim_date,
    MAX(ci.CI_ADMISSION_DATE) as last_claim_date,
    SUM(cs.CS_NET_CLAIM_AMT) as total_claimed_amount,
    AVG(cs.CS_NET_CLAIM_AMT) as avg_claim_amount,
    GROUP_CONCAT(DISTINCT ci.CI_HOSPITAL_ID) as hospitals_used
FROM claim_intimation ci
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
GROUP BY ci.CI_SERVICE_NO, ci.CI_CARD_ID, ci.CI_BENEFICIARY_NAME
HAVING COUNT(DISTINCT ci.CI_INTIMATION_ID) >= 10
ORDER BY total_claims DESC, total_claimed_amount DESC;
```

### 3.9 Impossible Dependent Claims Detection
```sql
-- Find dependent relationship issues (age-based validation)
SELECT 
    ci.CI_INTIMATION_ID,
    ci.CI_SERVICE_NO,
    ci.CI_BENEFICIARY_NAME,
    ci.CI_PATIENT_NAME,
    ci.CI_RELATION_ID,
    rm.RM_RELATION_DESC as relationship,
    ci.CI_AGE as patient_age,
    YEAR(CURDATE()) - YEAR(bm.BM_DOB) as beneficiary_age,
    ci.CI_ADMISSION_DATE,
    cs.CS_NET_CLAIM_AMT as claimed_amount,
    ci.CI_HOSPITAL_ID,
    CASE 
        WHEN ci.CI_RELATION_ID = 'SON' AND ci.CI_AGE > (YEAR(CURDATE()) - YEAR(bm.BM_DOB) - 15) THEN 'Son older than possible'
        WHEN ci.CI_RELATION_ID = 'DAU' AND ci.CI_AGE > (YEAR(CURDATE()) - YEAR(bm.BM_DOB) - 15) THEN 'Daughter older than possible'
        WHEN ci.CI_RELATION_ID IN ('SON', 'DAU') AND ci.CI_AGE > 25 THEN 'Dependent over age limit'
        WHEN ci.CI_RELATION_ID = 'WIF' AND ci.CI_AGE > (YEAR(CURDATE()) - YEAR(bm.BM_DOB) + 10) THEN 'Wife age inconsistent'
        ELSE 'Age relationship mismatch'
    END as issue_type
FROM claim_intimation ci
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
LEFT JOIN benf_master_live bm ON ci.CI_SERVICE_NO = bm.BM_SERVICE_NO 
    AND ci.CI_SERVICE_TYPE = bm.BM_FORCE_TYPE
LEFT JOIN relation_master rm ON ci.CI_RELATION_ID = rm.RM_RELATION_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    AND ci.CI_RELATION_ID IS NOT NULL
    AND ci.CI_RELATION_ID != 'SEL'
    AND (
        (ci.CI_RELATION_ID IN ('SON', 'DAU') AND CAST(ci.CI_AGE AS UNSIGNED) > 25)
        OR (ci.CI_RELATION_ID IN ('SON', 'DAU') AND CAST(ci.CI_AGE AS UNSIGNED) > (YEAR(CURDATE()) - YEAR(bm.BM_DOB) - 15))
        OR (ci.CI_RELATION_ID = 'WIF' AND CAST(ci.CI_AGE AS UNSIGNED) > (YEAR(CURDATE()) - YEAR(bm.BM_DOB) + 15))
    )
ORDER BY claimed_amount DESC;
```

### 3.10 Doctor Teleportation Detection
```sql
-- Find same doctor treating patients at distant locations on same day
SELECT 
    a.CS_TREAT_DOCT as doctor_name,
    DATE(a.CI_ADMISSION_DATE) as treatment_date,
    COUNT(DISTINCT a.CI_HOSPITAL_ID) as number_of_hospitals,
    COUNT(*) as number_of_patients,
    GROUP_CONCAT(DISTINCT a.CI_HOSPITAL_ID ORDER BY a.CI_HOSPITAL_ID) as hospital_ids,
    GROUP_CONCAT(DISTINCT crm.CRM_CITY_NAME ORDER BY a.CI_HOSPITAL_ID) as cities,
    GROUP_CONCAT(DISTINCT a.CI_INTIMATION_ID ORDER BY a.CI_ADMISSION_DATE) as claim_ids,
    SUM(cs.CS_NET_CLAIM_AMT) as total_claimed_amount
FROM claim_intimation a
JOIN claim_submission cs ON a.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
LEFT JOIN hospital_master hm ON a.CI_HOSPITAL_ID = hm.HM_HOSP_ID
LEFT JOIN cghs_region_master crm ON hm.HM_REGION_ID = crm.CRM_CITY_ID
WHERE a.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    AND cs.CS_TREAT_DOCT IS NOT NULL
    AND cs.CS_TREAT_DOCT != ''
GROUP BY cs.CS_TREAT_DOCT, DATE(a.CI_ADMISSION_DATE)
HAVING COUNT(DISTINCT a.CI_HOSPITAL_ID) >= 2
    AND COUNT(DISTINCT crm.CRM_CITY_ID) >= 2
ORDER BY number_of_hospitals DESC, total_claimed_amount DESC;
```

---

## 4. REPORT OUTPUT STRUCTURE

### For Each Pattern, Generate:

1. **Summary Statistics**:
   - Total number of fraud cases detected
   - Total amount involved
   - Number of unique beneficiaries
   - Number of unique hospitals involved
   - Time period distribution

2. **Detailed Case List**:
   - Claim ID
   - Beneficiary details (Service No, Card No, Name)
   - Hospital details
   - Dates (Admission, Discharge, Submission)
   - Amounts (Claimed, Approved)
   - Fraud indicators/red flags
   - Current claim status

3. **Financial Impact**:
   - Total claimed amount
   - Total approved amount
   - Potential fraud amount
   - Recovery potential

4. **Geographic Distribution**:
   - Region-wise breakdown
   - Hospital-wise breakdown

5. **Temporal Analysis**:
   - Year-wise trend
   - Month-wise distribution
   - Peak fraud periods

---

## 5. NEXT STEPS

1. **Execute Queries**: Run each SQL query against the database
2. **Data Validation**: Verify results for accuracy
3. **Export Results**: Save each pattern's results to CSV
4. **Generate Report**: Create comprehensive PDF report following Module 11 format
5. **Risk Scoring**: Assign risk scores to each case
6. **Recommendations**: Provide actionable fraud prevention recommendations

---

## 6. ADDITIONAL PATTERNS TO CONSIDER

### Pattern 11: Claim Splitting/Unbundling
- Same patient, same ailment, split into multiple bills
- Table: `claim_submission`, `expenses_details`

### Pattern 12: Synthetic Identities
- New service numbers with immediate high-value claims
- Table: `benf_master_live`, `claim_intimation`

### Pattern 13: Revolving Door Pattern
- Frequent readmissions within short intervals
- Table: `claim_intimation`, `claim_submission`

---

## NOTES:
- All date filters use last 5 years: `>= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)`
- Amounts are in CS_NET_CLAIM_AMT (net claimed amount)
- Join conditions handle NULL values appropriately
- GROUP_CONCAT used for summarizing multiple values
- Results ordered by fraud severity (amount/frequency)
