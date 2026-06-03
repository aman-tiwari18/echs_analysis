# Point 11 Enhanced Fraud Detection Queries - README

## Overview
This document describes the enhanced comprehensive fraud detection queries for Point 11 that include **complete descriptive information** for all IDs shown in the results.

## Time Period
**Last 5 Years Data Only** - All queries filter using:
```sql
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
```

---

## Enhanced Data Fields - What's New

### For ALL Hospital IDs, we now show:
- **Hospital ID** - HM_HOSP_ID
- **Hospital Name** - HM_HOSP_NAME
- **Hospital Location** - City + State (CRM_CITY_NAME + SM_STATE_NAME)
- **Hospital Address** - HM_ADDRESS (where applicable)

### For ALL Beneficiaries, we now show:
- **Service Number** - CI_SERVICE_NO
- **Card Number** - CI_CARD_ID
- **Beneficiary Name** - CI_BENEFICIARY_NAME
- **Service Type** - STM_SERVICE_NAME (e.g., Army, Navy, Air Force)
- **Rank** - RM_RANK_NAME (e.g., Major, Colonel)
- **Contact Mobile** - CI_MOBILE
- **Address** - CI_ADDRESS1

### For ALL Patients, we now show:
- **Patient Name** - CI_PATIENT_NAME
- **Patient Age** - CI_AGE
- **Patient Gender** - CI_SEX
- **Relationship** - Both code (CI_RELATION_ID) and description (RM_RELATION_DESC)

### For ALL Claims, we now show:
- **Claim ID** - CI_INTIMATION_ID
- **Admission Date** - CI_ADMISSION_DATE
- **Discharge Date** - CS_DOD
- **Claim Submission Date** - CS_SUB_DATE
- **Ailment/Diagnosis** - CI_ADM_AILMENT
- **Treating Doctor** - CS_TREAT_DOCT
- **Claimed Amount** - CS_NET_CLAIM_AMT
- **Approved Amount** - CS_UTI_APP_AMT
- **Claim Stage** - CI_INT_STAGE
- **Claim Status** - CI_INT_STATUS

---

## Query-by-Query Enhanced Details

### 1. Duplicate Card IDs
**New Fields Added:**
- Hospital names with locations (not just IDs)
- Complete list of claim IDs
- Geographic locations (City-State)
- Fraud span in days
- Count of unique hospitals

**Sample Output Format:**
```
card_number: 12345678
unique_service_numbers: 3
hospitals_used: H001:Apollo Hospital | H045:Fortis Healthcare | H089:Max Hospital
locations: Delhi-Delhi | Mumbai-Maharashtra | Bangalore-Karnataka
fraud_span_days: 1095
```

### 2. Simultaneous Admissions
**New Fields Added:**
- Complete hospital information for both admissions
- City and state for both hospitals
- Patient demographics (age, gender)
- Treating doctors for both claims
- Ailment descriptions

**Sample Output Format:**
```
service_number: ABC123456
hospital_1: H001:Apollo Hospital
city_1: Delhi, Delhi
hospital_2: H089:Max Hospital
city_2: Bangalore, Karnataka
overlap_days: 15
```

### 3. Duplicate Bill Numbers
**New Fields Added:**
- Combined beneficiary info (Service No + Name)
- Hospital name with ID
- Location information
- Admission dates for all duplicates
- Card numbers involved

### 4. Mobile Number Rings
**New Fields Added:**
- Hospital names and locations for all hospitals used
- Complete beneficiary information
- Date range of fraudulent activity
- Count of unique hospitals

### 5. UID Duplication
**New Fields Added:**
- Hospital names and locations
- Complete beneficiary details
- Geographic distribution
- Date range analysis

### 6. Post-Death Claims (Lazarus)
**New Fields Added:**
- Complete patient demographics
- Relationship information
- Hospital full details with location
- Treating doctor name
- Ailment description
- Days after death metrics

### 7. Chronic Stay / Forever Patient
**New Fields Added:**
- Complete patient demographics
- Relationship details
- Room type information
- Hospital complete information
- Treating doctor
- Stay duration analysis

### 8. High Frequency Claims
**New Fields Added:**
- Service type and rank
- Multiple patient names treated
- Complete hospital and location details
- Contact information
- Address details
- Fraud span analysis
- Count of unique patients

### 9. Impossible Dependent Claims
**New Fields Added:**
- Complete patient demographics
- Discharge date
- Hospital location details
- Treating doctor
- Contact information
- Detailed issue type classification

### 10. Doctor Teleportation
**New Fields Added:**
- Complete hospital information with locations
- Cities visited in formatted list
- Patient names treated
- Service numbers involved
- Time stamps of treatments
- Distance impossibility evidence

---

## Data Joins and Master Tables Used

### Primary Tables:
- `claim_intimation` - Main claim data
- `claim_submission` - Submission and payment details

### Master Data Tables (for descriptive information):
- `hospital_master` - Hospital details
- `cghs_region_master` - City/Region information
- `state_master` - State information
- `relation_master` - Relationship descriptions
- `service_type_master` - Service type names
- `rank_master` - Rank information

---

## Output Formats

### CSV Files Generated:
Each pattern generates a separate CSV file with complete information:
1. `01_Duplicate_Card_IDs.csv`
2. `02_Simultaneous_Admissions.csv`
3. `03_Duplicate_Bill_Numbers.csv`
4. `04_Mobile_Number_Rings.csv`
5. `05_UID_Duplication.csv`
6. `06_Post_Death_Claims_Lazarus.csv`
7. `07_Chronic_Stay_Forever_Patient.csv`
8. `08_High_Frequency_Claims.csv`
9. `09_Impossible_Dependent_Claims.csv`
10. `10_Doctor_Teleportation.csv`

### JSON File Generated:
`Point11_Fraud_Detection_Complete_Data.json` - Contains all data in structured JSON format for report generation

---

## Key Improvements Over Previous Version

### 1. **No More Naked IDs**
- ✅ Every Hospital ID now shows name and location
- ✅ Every relationship code shows description
- ✅ Service types and ranks shown as names, not codes

### 2. **Geographic Context**
- ✅ Full location information (City, State)
- ✅ Easier to identify fraud patterns across regions
- ✅ Distance analysis for doctor teleportation

### 3. **Complete Patient Information**
- ✅ Age, gender, relationship for all patients
- ✅ Contact details included
- ✅ Ailment descriptions for medical context

### 4. **Temporal Analysis Enhanced**
- ✅ Date ranges for fraud activity
- ✅ Fraud span calculations
- ✅ Days after death metrics
- ✅ Stay duration analysis

### 5. **Financial Completeness**
- ✅ Both claimed and approved amounts
- ✅ Easy calculation of fraud impact
- ✅ Average claim analysis

### 6. **Report-Ready Data**
- ✅ All information needed for official reports
- ✅ No need for additional lookups
- ✅ Human-readable format
- ✅ Ready for PDF report generation

---

## Usage Instructions

### Running the Script:
```bash
cd /home/aman/Desktop/echs_analysis
python3 point11_comprehensive_fraud_detection.py
```

### Expected Output:
- 10 CSV files with complete fraud data
- 1 JSON file with all data structured
- Console summary with record counts
- Execution time logs

### Data Validation:
All data is filtered for:
- ✅ Last 5 years only
- ✅ Non-null essential fields
- ✅ Valid card numbers, UIDs, mobile numbers
- ✅ Meaningful amounts

---

## Next Steps After Data Collection

1. **Review CSV Files** - Check data quality and completeness
2. **Analyze JSON** - Use for automated report generation
3. **Generate Statistics** - Summary metrics for each pattern
4. **Create Visualizations** - Charts and graphs for report
5. **Compile Report** - Generate final PDF report for officials

---

## Notes for Officials

### Data Interpretation:
- **Claimed Amount** = Amount requested by hospital/beneficiary
- **Approved Amount** = Amount actually approved for payment
- **Fraud Span** = Time period over which fraud occurred
- **Overlap Days** = Days where patient was at multiple hospitals simultaneously

### Red Flags:
- Multiple service numbers using same card
- Mobile numbers with 5+ different cards
- Claims after recorded death date
- Hospital stays exceeding 90 days
- Dependents over age limits
- Doctors treating in multiple cities same day

### Action Items:
Each detected case should be:
1. Verified against original documents
2. Cross-checked with hospital records
3. Investigated for patterns
4. Referred to fraud investigation team if confirmed
5. Recovery process initiated if applicable

---

## Contact for Issues

If any queries fail or data looks incorrect:
1. Check database connectivity
2. Verify table structures match schema
3. Review date filters (5-year window)
4. Check for NULL handling in queries
5. Validate master data completeness

---

**Generated Date:** 2024
**Version:** 2.0 - Enhanced with Complete Descriptive Information
**Status:** Ready for Production Execution
