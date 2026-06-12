# ECHS Fraud Analytics — Report Documentation

> **Prepared by:** IIT Kanpur — Data Analytics & Fraud Intelligence Division  
> **Classification:** RESTRICTED — Authorized Personnel Only  
> **Analysis Period:** FY 2021–2026 (Last 5 Years)  
> **Records Scanned:** 26+ Million Claim Records  

---

## Overview

The ECHS (Ex-Servicemen Contributory Health Scheme) fraud analytics framework is a structured, data-driven audit system built on top of the central ECHS MySQL database. Two report modules are currently active:

| Module | Focus Area | Patterns | File |
|--------|-----------|----------|------|
| **Module 11** | Identity Fraud & Duplicate Claim Detection | 6 Patterns | `generate_module11_report_html.py` |
| **Module 12** | Hospital Specialty Misuse & Empanelment Analysis | 5 Patterns | `generate_module12_report.py` |

Both modules use the same **Navy (#1a2744) + Gold (#c9a84c)** visual theme, share the same report architecture (Cover → Executive Summary → Pattern Breakdowns → Consolidated Summary), and are rendered to PDF using **WeasyPrint**.

---

---

# MODULE 11: Identity Fraud & Duplicate Claim Detection

## Purpose

Module 11 is the **beneficiary-side** fraud module. It investigates whether the *person* behind each claim is real and legitimate. It cross-references every ECHS card number, service number, Aadhaar UID, and mobile number to detect fraudulent identities, agent rings, ghost patients, and statistical over-utilization outliers.

## Data Sources

| Table | Purpose |
|-------|---------|
| `claim_intimation` | Primary claim record — card ID, service number, admission date, hospital |
| `claim_submission` | Financial record — claimed amount, approved amount, settlement date |
| `office_master` | Hospital details — name, city, type |
| `cghs_region_master` | City-to-state mapping |
| `state_master` | State names |

## Cover Page Metrics

| Box | Value |
|-----|-------|
| Classification | RESTRICTED |
| Period | FY 2021–26 |
| Records Scanned | 26M+ (claim intimation rows) |
| Patterns Run | 6 Patterns |
| Cases Flagged | Dynamic — total across all patterns |

---

## Pattern 1: Duplicate Card IDs — Identity Fraud & System Misuse

### What It Detects
Each ECHS health card is issued to exactly **one individual**. Pattern 1 finds cases where the same physical card number appears against **multiple distinct service numbers or beneficiary names** — a direct signal of card sharing, data entry fraud, or system bypass.

### Sub-Categories

| Sub-Pattern | File | Description |
|-------------|------|-------------|
| **True Fraud (01a)** | `01a_Duplicate_Card_IDs_True_Fraud*.csv` | Completely different people (different root service numbers AND different names) sharing the same card number. The most serious sub-type. |
| **Hospital Typos (01b)** | `01b_Duplicate_Card_IDs_Same_Name_Typos*.csv` | Same beneficiary, but hospital staff entered the service number inconsistently (e.g., "IC-12345" vs "12345"). Indicates poor hospital data quality. |
| **Operator Mistakes (01c)** | `01c_Duplicate_Card_IDs_Operator_Mistakes*.csv` | Hospitals bypassing the system by typing dummy text ("Card not handed over", "01", "N/A") into the card ID field instead of the real card. |
| **Ghost Patients (01e)** | `01e_Ghost_Patients_No_Real_Card*.csv` | Service numbers using dummy card text that have **never presented a real ECHS card**, yet had claims approved and paid by UTI. |

### Report Display
- **Table 1.1a:** Top 15 True Fraud cases, sorted by **`unique_service_numbers` descending** — shows cards being shared across the greatest number of different people at the top.
- **Table 1.1b:** Top 5 Operator Mistake cases — shows which dummy card texts (placeholder strings) allowed the most service numbers to bypass verification.

### Table Columns (1.1a)
| Column | Meaning |
|--------|---------|
| Card Number | The ECHS card number shared across identities |
| Svc #s | Count of distinct military service numbers using this card (higher = more severe) |
| Beneficiary Names | Names of people claiming under this card |
| Claims | Total number of claims filed |
| Hospitals | Where the claims were filed |
| Total Exposure | Total money claimed across all fraudulent uses |

### Key Detection Logic
- A card number is flagged if `COUNT(DISTINCT CI_SERVICE_NO) >= 2` with different root identities
- Dummy card text patterns (regex-based) filter out placeholder strings for sub-category (01c)

### Recommended Action
Freeze all ECHS cards sharing a duplicate card number. Block further claims until physical verification confirms the legitimate cardholder. Patch hospital PMS to reject dummy card texts.

---

## Pattern 2: Simultaneous Admissions — Physical Impossibility

### What It Detects
A beneficiary cannot be physically admitted to two different hospitals at the same time or within an impossibly short gap. Pattern 2 identifies claim pairs from the **same service number** where admissions at **different hospitals** overlap or are separated by **≤ 7 days**.

### Data File
`02_Simultaneous_Admissions*.csv`

### Detection Threshold
- **Gap ≤ 7 days** between discharge from Hospital 1 and admission to Hospital 2
- Negative gap = true overlap (still admitted to Hospital 1 when admitted to Hospital 2)
- Zero gap = same-day discharge and re-admission at a different facility

### Report Display
- **Table 2.1:** Top 15 pairs sorted by **`gap_days` descending** (largest gap first) — surfaces the most extreme hospital-hopping cases at the top.

### Table Columns
| Column | Meaning |
|--------|---------|
| Beneficiary | Name of the person involved |
| Svc # | Military service number |
| Hospital 1 | First hospital (with city) |
| Hospital 2 | Second hospital (with city) |
| Adm 1 | First admission date |
| Adm 2 | Second admission date |
| Gap (Days) | Days between the two admissions (negative = overlap) |
| Total Exposure | Combined financial exposure of both claims |

### Key Findings Note
- **Negative gap** = simultaneous overlap — physical impossibility for genuine inpatient care.
- Cases where Hospital 2 is a polyclinic (short code like "Rohtak") indicate **referral-chain fraud** where both a polyclinic and a private hospital file claims for the same episode of care.

### Recommended Action
Initiate field audit of all simultaneous admission pairs. Cross-reference hospital admission registers against ECHS claim dates to identify ghost patients.

---

## Pattern 3: Duplicate Bill Numbers — Resubmission Fraud

### What It Detects
Each hospital bill/invoice has a unique number. If the exact same bill number appears under **multiple different ECHS claim IDs**, the invoice was either physically resubmitted for payment twice, or the bill number was copy-pasted from another claim.

### Data File
`03_Duplicate_Bill_Numbers*.csv`

### Exclusions
All blank, "NA", "N/A", and null bill numbers are **excluded** — only real bill strings are analyzed.

### Report Display
- **Table 3.1:** Top 15 most-resubmitted bill numbers by **duplicate count**.

### Table Columns
| Column | Meaning |
|--------|---------|
| Bill Number | The invoice/bill string |
| Dup Count | How many times this exact bill string appeared across different claims |
| Claims | Total number of ECHS claim IDs carrying this bill number |
| Hospitals | Which hospitals filed claims with this bill |
| Beneficiary/Svc # | Who was claimed for |
| Total Exposure | Total money at risk |

### Key Findings Note
- Dup Count of 2 = one resubmission; Counts of 5+ = systematic template-based fraud.
- A bill number appearing across **multiple hospitals** is particularly severe — the same physical invoice cannot be issued by two separate facilities, confirming document fabrication.

### Recommended Action
Implement system-level bill number uniqueness enforcement to prevent re-entry of the same invoice across different claims.

---

## Pattern 4: Mobile Number Rings — Coordinated Fraud Agent Network

### What It Detects
An ECHS mobile number is the contact point for OTPs and claim alerts. A legitimate family shares at most 3–4 cards on one mobile (ex-serviceman + dependents). When a **single mobile is linked to 5+ cards** belonging to completely different service numbers, it indicates a **fraud agent** managing multiple ghost identities centrally.

### Data Files
- `04_Mobile_Number_Rings*.csv` — Real mobile numbers linked to 5+ cards
- `04_Mobile_Dummy_Numbers*.csv` — Placeholder numbers (000000, 111111, 999999) excluded from main analysis

### Detection Threshold
- Minimum **5 distinct ECHS cards** per mobile number to be flagged as a ring

### Report Display
- **Table 4.1:** Top 15 real mobile number rings by exposure.
- **Table 4.2:** Dummy/invalid mobile numbers (separate, for system integrity context).

### Table Columns (4.1)
| Column | Meaning |
|--------|---------|
| Mobile Number | The contact number |
| Cards | Count of distinct ECHS health cards under this mobile |
| Svc Numbers | Count of distinct service numbers |
| Claims | Total claims filed across all linked identities |
| Hospitals | Where these claims were filed |
| Total Exposure | Total financial exposure |

### Recommended Action
Investigate mobile number rings — a single mobile coordinating 5+ cards indicates a fraud agent. De-register the mobile from non-family cards. Dummy numbers should trigger mandatory re-registration of genuine contact details.

---

## Pattern 5: UID (Aadhaar) Duplication — Synthetic Identity Fraud

### What It Detects
The 12-digit Aadhaar UID is a biometric-linked national identifier — exactly **one UID per individual** by UIDAI mandate. If the same UID appears registered under **multiple ECHS service numbers**, it means either identity theft (one person's biometric used by another) or synthetic identity fraud (a single UID seeding multiple fabricated accounts).

### Data File
`05_UID_Duplication*.csv`

### Exclusions
Known dummy UIDs (all-zero, all-nine, sequential patterns) are **strictly excluded**.

### Privacy Handling
All 12-digit UIDs are **masked** in the report as `XXXX****XXXX` (first 4 + last 4 digits only).

### Report Display
- **Table 5.1:** Top 15 UID duplication cases.

### Table Columns
| Column | Meaning |
|--------|---------|
| UID (masked) | Partially masked Aadhaar number |
| Svc #s | Count of service numbers sharing this UID (≥2 = anomalous) |
| Claims | Total claims across all linked identities |
| Hospitals | Where these claims were filed |
| Locations | Geographic spread of the linked identities |
| Total Exposure | Total financial exposure |

### Key Findings Note
- 3+ service numbers + multiple geographic locations = a **large-scale synthetic identity ring** using one Aadhaar as the seed identity.
- Must be escalated to UIDAI and ECHS Directorate for biometric re-verification.

### Recommended Action
Audit all UID duplication cases. Each Aadhaar must map to exactly one identity. Escalate to UIDAI for verification and FIR filing.

---

## Pattern 6: High Frequency Claims — Over-Utilisation Fraud

### What It Detects
Beneficiaries who make an **anomalously high number of inpatient claims** in 5 years, flagged using a dynamically calculated statistical threshold. The threshold is derived from the actual claim distribution of all ~4.69 million ECHS beneficiaries — no arbitrary fixed number is assumed.

### Data File
`08_High_Frequency_Claims*.csv`

### How the Threshold Is Calculated (Tukey Fence Method)
| Statistic | Value |
|-----------|-------|
| Median | 2 claims (5-year baseline for a typical ex-serviceman) |
| Q1 | 1 claim |
| Q3 | 6 claims |
| IQR = Q3 − Q1 | 5 |
| **Tukey Fence = Q3 + 1.5 × IQR** | **6 + 7.5 = 13.5 → 13 claims** |

> **Any beneficiary with 14+ inpatient claims in 5 years is a statistical outlier** — appearing in the rarest 0.1% of the distribution. This is almost certainly not explained by age, illness, or any legitimate medical need alone.

### Report Display
- **Table 6.1:** Top 15 high-frequency claimants by total exposure.

### Table Columns
| Column | Meaning |
|--------|---------|
| Service # | Military service number |
| Beneficiary | Name |
| # Claims | Total inpatient claims in the 5-year window |
| Avg Claim | Average claim amount per episode |
| Hospitals | Number and names of hospitals used |
| Total Exposure | Total amount claimed |

### Key Findings Note
- Beneficiaries concentrated at a **single hospital** are the most suspicious — genuine chronic illness patients see multiple specialists. One hospital + high frequency = hospital-patient collusion for ghost billing.

### Recommended Action
Require pre-authorization and clinical justification for further admissions from all beneficiaries above the threshold.

---

## Module 11 — Consolidated Summary Table

The final page of the report shows a cross-pattern comparison:

| Pattern | Signal | Cases Flagged | Exposure |
|---------|--------|--------------|---------|
| 1 | Duplicate Card IDs | True + Typo + Dummy counts | Combined |
| 2 | Simultaneous Admissions (Gap ≤ 7 days) | Pairs count | Combined |
| 3 | Duplicate Bill Number Resubmission | Count | Combined |
| 4 | Mobile Number Rings (5+ cards) | Real + Dummy rings | Combined |
| 5 | UID (Aadhaar) Duplication | UID count | Combined |
| 6 | High Frequency Claims (≥13 claims) | Beneficiary count | Combined |
| **TOTAL** | — | **All cases** | **All exposure** |

---

---

# MODULE 12: Hospital Specialty Misuse & Empanelment Analysis

## Purpose

Module 12 is the **hospital-side** fraud module. While Module 11 focuses on who is claiming, Module 12 focuses on **which hospitals are claiming and whether they are entitled to**. It investigates hospitals billing for services outside their licensed category, exploiting NABH accreditation, filing IPD claims without IPD registration, suddenly spiking their billing, or billing extreme amounts from low-capacity facilities.

## Data Sources

| Table | Purpose |
|-------|---------|
| `claim_intimation` | Primary claim record — hospital ID, patient type (OPD/IPD), dates |
| `claim_submission` | Financial record — gross claimed, UTI approved amount |
| `office_master` | Hospital details — type code, NABH status, name, city |
| `empanel_hospital_service` | Which services each hospital is registered to provide |
| `empanel_facility` | Facility category names (IPD, OPD, Biochemistry, etc.) |
| `cghs_region_master` | City details |
| `state_master` | State names |

## Cover Page Metrics

| Box | Value |
|-----|-------|
| Classification | RESTRICTED |
| Period | FY 2021–26 |
| Records Scanned | 25.9M+ (5-year claim intimation count) |
| Patterns Run | 5 Patterns |
| Entities Flagged | Dynamic — total hospitals across all patterns |

---

## Pattern 1: Specialty Category Billing Fraud — Type-3 IPD Billing

### What It Detects
ECHS hospitals are classified by type. **Type-3** facilities are dental clinics and diagnostic/pathology laboratories. They are licensed and empanelled for **outpatient procedures only**. Billing for **inpatient (IPD) admissions** from a Type-3 facility is a direct policy violation — these facilities do not have the infrastructure for overnight care.

### Data Files Used
- `01a_specialty_misuse_hospitals*.csv` — Hospital-level summary (facilities flagged)
- `01b_specialty_misuse_claims*.csv` — Individual claim-level detail (top claims by amount)
- `01c_nabh_deduction_benchmark*.csv` — NABH vs Non-NABH deduction rate benchmark

### Detection Logic
- `WHERE ci.CI_PATIENT_TYPE = 'I'` (IPD admissions only)
- `AND om.OM_HOSP_TYPE IN ('3', '03')` (Type-3 facilities only)
- Data covers the full 5-year window, no limit on facilities returned

### Report Display
- **Table 1.1:** Top 15 Type-3 facilities billing IPD claims, sorted by total claimed amount descending.

### Table Columns
| Column | Meaning |
|--------|---------|
| Hospital Name | Name of the Type-3 facility |
| Type | Hospital type description (Dental, Diagnostic, etc.) |
| City | Location |
| State | State |
| IPD Claims | Number of inpatient claims filed (should be zero for Type-3) |
| Claimed Amt | Total gross amount claimed for IPD |
| Ded. % | Percentage of the claimed amount that was deducted by UTI |

### Key Findings Note
- IPD from a dental clinic implies fraudulent coding — either the claim type is wrong, or the hospital is admitting patients overnight in an unlicensed premise.
- High deduction % here means UTI partially caught the fraud — low deduction % means payments went through unchallenged.

### Recommended Action
Deny all IPD claims from dental/diagnostic clinics unless explicitly authorized. Conduct site inspection to verify if overnight facilities exist.

---

## Pattern 2: NABH Accreditation & High Deduction Anomalies

### What It Detects
NABH (National Accreditation Board for Hospitals) accreditation certifies higher quality standards, which should translate to **lower deduction rates** (bills are more accurate and less inflated). When a NABH hospital consistently suffers **deduction rates above 15%**, it means the hospital is exploiting its NABH status to attract ECHS patients while systematically inflating bills.

### System-Wide Context (displayed in report)
Derived from `02a_nabh_benchmark_by_type*.csv`:
- Total NABH-accredited hospitals in the dataset
- Total Non-NABH hospitals in the dataset

This gives auditors an immediate understanding of the scale of NABH vs non-NABH coverage.

### Data Files Used
- `02a_nabh_benchmark_by_type*.csv` — NABH vs Non-NABH summary benchmark
- `02b_nabh_high_deduction_anomalies*.csv` — NABH hospitals with >15% deduction
- `02c_non_nabh_low_deduction*.csv` — Non-NABH hospitals with unusually low deduction (<5%)
- `02d_military_hospital_breakdown*.csv` — Military hospital type breakdown

### Detection Thresholds
| Sub-Query | Threshold |
|-----------|----------|
| NABH anomalies (02b) | `om.OM_NABH = 'Y'` AND `deduction_pct > 15` AND `total_claims >= 100` |
| Non-NABH unexpectedly clean (02c) | `om.OM_NABH != 'Y'` AND `deduction_pct < 5` AND `total_claims >= 200` |

### Report Display
- **Table 2.1:** Top 15 NABH hospitals with anomalously high deduction rates.

### Table Columns
| Column | Meaning |
|--------|---------|
| Hospital Name | NABH-accredited hospital name |
| Type | Hospital type code |
| City | Location |
| Claims | Total claims filed in the 5-year window |
| Claimed (Lakh) | Total gross amount claimed |
| Approved (Lakh) | Total amount approved by UTI |
| Ded. % | Deduction percentage (red if > 15%) |

### Recommended Action
Investigate anomalous NABH hospitals for bill padding. A high deduction rate despite NABH status suggests potential bill inflation to maximize approved payouts. Consider temporary empanelment review.

---

## Pattern 3: Services Outside Empaneled Scope — IPD without IPD Empanelment

### What It Detects
Hospitals must be **explicitly registered in the ECHS empanelment system** for every service category they bill. Pattern 3 identifies hospitals that are filing **IPD (inpatient) claims** but are **NOT registered for IPD** in the `empanel_hospital_service` table. The empanelment registry lists allowed facilities (Biochemistry, Blood Bank, Cardiology, IPD, OPD, etc.) per hospital.

### Data Files Used
- `03a_empaneled_services_registry*.csv` — Full registry of empaneled services per hospital
- `03b_ipd_without_ipd_empanelment*.csv` — Hospitals with IPD claims but no IPD empanelment
- `03c_billing_without_any_empanelment*.csv` — Hospitals billing claims with zero empanelment at all

### Detection Logic (Query 3B)
```sql
WHERE ci.CI_PATIENT_TYPE = 'I'
  AND (
    emp.actual_empaneled_services IS NULL
    OR emp.actual_empaneled_services NOT LIKE '%IPD%'
    AND emp.actual_empaneled_services NOT LIKE '%Indoor%'
    AND emp.actual_empaneled_services NOT LIKE '%Inpatient%'
  )
```

No limit on rows — full set of violations is returned.

### Report Display
- **Table 3.1:** Top 15 hospitals with IPD claims but no IPD empanelment, sorted by total claimed amount.

### Table Columns
| Column | Meaning |
|--------|---------|
| Hospital | Hospital name |
| Type | Hospital type |
| City | Location |
| IPD Claims | Total number of inpatient claims filed |
| Claimed Amt | Total gross amount claimed for those IPD episodes |
| Empaneled Services | What the hospital IS actually registered for (confirms they are OPD-only) |

### Key Findings Note
- If `Empaneled Services` shows only "OPD", "Biochemistry", or similar — and the hospital is filing IPD claims — this is a **critical compliance failure**.
- Query 3C catches the even more severe case: hospitals with **zero empanelment** billing claims of any kind.

### Recommended Action
Implement hard system-level blocks at ECHS processing centers to automatically reject IPD claims from non-IPD-empaneled facilities.

---

## Pattern 4: Year-over-Year Billing Spike

### What It Detects
A hospital genuinely growing organically will have gradual year-over-year billing increases. A **100%+ increase in claimed amount in a single year** (doubling) indicates a deliberate strategy change — aggressive billing agent involvement, systematic upcoding, or a new fraud ring operation.

### Data Files Used
- `04a_hospital_yoy_billing_spike*.csv` — Hospital-level YoY comparison (1,677 facilities flagged)
- `04b_type_level_yoy_trend*.csv` — Aggregate trend by hospital type and year

### Detection Thresholds
```sql
WHERE prev.total_claims >= 50  -- Previous year must have meaningful volume
  AND (curr.total_claimed - prev.total_claimed) / prev.total_claimed >= 1.0
  -- i.e., 100%+ growth in claimed amount
ORDER BY yoy_amount_growth_pct DESC
```

No row limit — all facilities meeting the 100% growth threshold are returned.

### Report Display
- **Table 4.1:** Top 15 hospitals by billing spike, showing exact year comparison.

### Table Columns
| Column | Meaning |
|--------|---------|
| Hospital | Hospital name |
| City | Location |
| Prev Yr | The comparison base year (e.g., 2023) |
| Curr Yr | The spike year (e.g., 2024) |
| Prev Yr Amt | Total claimed in the previous year |
| Curr Yr Amt | Total claimed in the spike year |
| Claims Growth % | How many more individual claims were filed (volume comparison) |

> **Note:** The "Amt Growth %" column was intentionally removed from the report. The displayed columns are sufficient — the spike year vs previous year amount columns tell the full story without requiring a separate percentage column.

### Key Findings Note
- Where **Claims Growth % << Billing Growth %**, the hospital has started charging significantly more *per patient* — a signal of upcoding (billing a simple procedure as a complex one) or severity inflation.

### Recommended Action
Request clinical justification for any hospital that doubled its ECHS revenue in a single year. Cross-reference patient census records to verify the claim volume is real.

---

## Pattern 5: High-Value Claims at Low-Tier Facilities

### What It Detects
**Type-3 facilities** (dental, diagnostic, polyclinics) have inherently low infrastructure — no operating theatres, no ICUs, no overnight wards. When such a facility bills **₹50,000+ per claim** and does so repeatedly, it implies either (a) the bills are fabricated, (b) the hospital type is misclassified, or (c) procedures are being inflated beyond the facility's actual capability.

### Data Files Used
- `05a_high_value_low_tier_claims*.csv` — Individual claim-level detail (216 rows, claims ≥ ₹1,00,000)
- `05b_low_tier_hospitals_high_value*.csv` — Hospital-level summary (used in report)
- `05c_extreme_deduction_hospitals*.csv` — Hospitals with extreme deduction rates (≥80% deducted)

### Detection Thresholds (Verified from query source)
| Threshold | Value | Applied To |
|-----------|-------|-----------|
| Individual claim minimum | ≥ ₹50,000 | Query 5B (hospital summary) |
| Individual claim minimum | ≥ ₹1,00,000 | Query 5A (detail rows) |
| Minimum qualifying claims | ≥ 3 such claims | Hospital must have ≥3 high-value claims to be flagged |
| Hospital type filter | Type 3 / 03 only | All three queries |

### Report Display
- **Table 5.1:** Top 15 low-tier hospitals with high-value claims.

### Table Columns
| Column | Meaning |
|--------|---------|
| Hospital | Hospital name |
| Type | Hospital type (Dental, Diagnostic, etc.) |
| City | Location |
| High Val Claims | Number of claims exceeding the ₹50,000 threshold |
| Max Single Claim | The largest single claim amount billed |
| Total Claimed | Total gross amount across all high-value claims |

### Key Findings Note
- The threshold of ₹50,000 represents the upper limit of what is plausible for a single outpatient diagnostic or minor dental procedure. Anything beyond this — especially IPD-coded claims from a dental clinic — is anomalous.

### Recommended Action
Require mandatory pre-authorization for any Type-3 facility claim exceeding ₹50,000. Audit facilities where the max single claim approaches or exceeds ₹1,00,000.

---

## Module 12 — Consolidated Summary Table

The final page shows a cross-pattern comparison:

| Pattern | Fraud Pattern | Cases Flagged | Exposure |
|---------|--------------|--------------|---------|
| 1 | Specialty Category Billing Fraud | Hospital count | Exposure |
| 2 | NABH vs Non-NABH Divergence | Anomalous hospital count | Exposure |
| 3 | Out of Scope Empanelment | Facility count | Exposure |
| 4 | Year-over-Year Billing Spike | Facility count (1,677) | Current year exposure |
| 5 | High-Value Claims at Low-Tier | Facility count | Exposure |
| **TOTAL** | — | **All flagged** | **₹42,964+ Cr** |

---

---

# Technical Architecture

## Report Generation Pipeline

```
[SSH to ECHS DB] → [SQL Queries] → [CSV Files in /data/] 
      ↓
[Copy to /data/report_data/]  ← used by report generator
      ↓
[generate_module_XX_report.py] → [HTML String built] → [WeasyPrint] → [PDF]
```

## CSV Data Flow

All query scripts write to `/module_XX/data/`. The report generator reads from `/module_XX/data/report_data/` — a curated subfolder of the most recent, validated CSVs for each pattern.

## Column: `claim_ids`

All flagged hospital-level CSVs now contain a `claim_ids` column:
```
GROUP_CONCAT(DISTINCT ci.CI_INTIMATION_ID SEPARATOR ', ') AS claim_ids
```
This allows any auditor to directly verify a flagged hospital's data in the ECHS database using the exact `CI_INTIMATION_ID` values — no need to re-run the query.

## Formatting Helpers

| Function | Usage |
|----------|-------|
| `fmt(n)` | Format integer with commas (e.g., `1,677`) |
| `cr(n)` | Format rupee amount (auto-scales: ₹X.XX Cr / ₹X.XX L / ₹X,XXX) |
| `safe(v)` | Return value or `—` if null/empty/nan |

---

# Glossary

| Term | Meaning |
|------|---------|
| **IPD** | Inpatient Department — overnight hospital admission |
| **OPD** | Outpatient Department — visit without admission |
| **UTI** | UTI Infrastructure (the TPA processing ECHS claims) |
| **NABH** | National Accreditation Board for Hospitals — quality certification |
| **Type-3** | ECHS hospital classification for dental/diagnostic/polyclinic |
| **CI_INTIMATION_ID** | Primary key for a claim episode in `claim_intimation` |
| **Empanelment** | The official ECHS registration allowing a hospital to bill for specific services |
| **Deduction %** | `(Claimed - Approved) / Claimed × 100` — how much UTI cut from the bill |
| **IQR** | Interquartile Range — used in Tukey statistical outlier detection |
| **Tukey Fence** | Q3 + 1.5 × IQR — the standard statistical boundary for outliers |
| **YoY** | Year-over-Year — comparing a metric across consecutive calendar/fiscal years |
| **Ghost Patient** | A claim filed for a person who never actually received treatment |
| **Synthetic Identity** | A fabricated person assembled from partial real data to create fraudulent accounts |

---

*Last updated: June 2026 | IIT Kanpur — ECHS Fraud Analytics Project*
