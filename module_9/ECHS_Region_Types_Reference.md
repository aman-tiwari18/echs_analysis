# ECHS — Region Types (reference for the mentor)

The current ECHS database has region concepts under a few different names. This lists **all of
them in full** so we can confirm which "region" is meant for the hospital APIs.

## TL;DR

There are really **two underlying region systems**:

1. **ECHS Regional Centres** (`ecs_region`) — **13** — the administrative regional centres that run
   the scheme. Used on **claims / beneficiaries**.
2. **CGHS Regions / Cities** (`cghs_region_master`) — **34** — the location/rate grouping. A
   **hospital** links to this (enforced FK), and it's also what the hospital's **rate region**
   points to.

> The "rate region" (`OM_RATE_REGION` on a hospital) is **not a third list** — its values are the
> same CGHS region ids (e.g. `19 = Ahmedabad`, `1 = Delhi` in both). It just records which CGHS
> region's rate card applies to that hospital.

**How a hospital relates to each:**
- Hospital → **CGHS region**: `office_master.OM_OFFICE_CGHS_CITY_ID` → `cghs_region_master` (enforced FK).
- Hospital → **rate region**: `office_master.OM_RATE_REGION` → same CGHS list.
- Hospital → **ECHS region (13)**: *not stored directly on the hospital* — it's a claim/beneficiary
  attribute (`*_REGION_ID` → `ecs_region`), derivable via the hospital's state/city.

---

## 1. ECHS Regional Centres — `ecs_region` (13)

| id | code | name |
|----|------|------|
| 1 | 110 | New Delhi |
| 2 | 400 | Mumbai |
| 3 | 700 | Kolkata |
| 4 | 560 | Bangalore |
| 5 | 500 | Hyderabad |
| 6 | 600 | Chennai |
| 7 | 248 | Dehradun |
| 8 | 302 | Jaipur |
| 9 | 411 | Pune |
| 10 | 160 | Chandigarh |
| 11 | 211 | Allahabad |
| 12 | 800 | Patna |
| 13 | 380 | Ahmedabad |

## 2. CGHS Regions / Cities — `cghs_region_master` (34)

A hospital's location/rate region. (Code blank for a few.)

| id | code | name |
|----|------|------|
| 1 | DL1 | Delhi |
| 29 | DL2 | Delhi 2 |
| 2 | TR | Trivandrum |
| 3 | PU | Pune |
| 4 | CM | Chandimandir |
| 5 | HY | Secunderabad |
| 6 | LU | Lucknow |
| 7 | KO | Kochi |
| 8 | JA | Jaipur |
| 9 | JL | Jalandhar |
| 10 | KL | Kolkata |
| 11 | RA | Ranchi |
| 12 | JM | Jammu |
| 13 | CH | Chennai |
| 14 | VZ | Visakhapatnam |
| 15 | DH | Dehradun |
| 16 | NA | Nagpur |
| 17 | BA | Bangalore |
| 18 | JB | Jabalpur |
| 19 | AH | Ahmedabad |
| 20 | GU | Guwahati |
| 21 | PT | Patna |
| 23 | — | Kanpur |
| 24 | AM | Ambala |
| 25 | CO | Coimbatore |
| 26 | MU | Mumbai |
| 27 | HI | Hisar |
| 28 | AL | Allahabad |
| 30 | BR | Bareilly |
| 31 | BU | Bhubaneswar |
| 32 | NE | Nepal |
| 33 | YO | Yol |
| 34 | — | Meerut |
| 99 | — | Not Applicable |

## 3. Rate Region — `office_master.OM_RATE_REGION` (33 in use)

Same CGHS ids as above; shown here with **how many hospitals/offices fall under each** (useful to
see the spread). Total distinct values actually used: **33** (all of CGHS except `Yol`).

| CGHS id | name | hospitals/offices |
|---------|------|-------------------|
| 4 | Chandimandir | 896 |
| 1 | Delhi | 578 |
| 29 | Delhi 2 | 462 |
| 8 | Jaipur | 290 |
| 2 | Trivandrum | 272 |
| 3 | Pune | 265 |
| 5 | Secunderabad | 236 |
| 18 | Jabalpur | 179 |
| 13 | Chennai | 171 |
| 17 | Bangalore | 165 |
| 12 | Jammu | 162 |
| 27 | Hisar | 159 |
| 30 | Bareilly | 159 |
| 19 | Ahmedabad | 131 |
| 15 | Dehradun | 115 |
| 10 | Kolkata | 111 |
| 6 | Lucknow | 110 |
| 28 | Allahabad | 100 |
| 21 | Patna | 88 |
| 16 | Nagpur | 82 |
| 20 | Guwahati | 80 |
| 31 | Bhubaneswar | 59 |
| 32 | Nepal | 36 |
| 11 | Ranchi | 54 |
| 34 | Meerut | 44 |
| 9 | Jalandhar | 37 |
| 23 | Kanpur | 35 |
| 24 | Ambala | 14 |
| 25 | Coimbatore | 13 |
| 14 | Visakhapatnam | 3 |
| 99 | Not Applicable | 2 |
| 7 | Kochi | 1 |
| 26 | Mumbai | 1 |

*(Note: `OM_OFFICE_CGHS_CITY_ID` — the hospital's own CGHS region — is the same list and is the
cleaner field to use; `OM_RATE_REGION` happens to mirror it for most hospitals.)*

---

## Question for the mentor

When you say "region" for hospitals, do you mean:
- **(A) ECHS Regional Centre** — the 13 administrative regions (New Delhi, Mumbai, …)? *Lives on
  claims/beneficiaries; derived for a hospital.*
- **(B) CGHS region/city** — the ~34 location/rate regions (Delhi, Pune, Chandimandir, …)?
  *Directly on the hospital, enforced FK — easiest to add to the hospital API.*

Tell me which, and I'll add it to the hospital response accordingly.
