# Data dictionary — datasets/

13 applications: the 9-member ring (cluster #4471) + 4 control applications (legitimate, plus one
single-applicant income-mismatch case, `A-88210`). All values synthetic.

## applications.csv
Master application records. Load to Fabric (Silver/Gold) as the `applications` table.

| Column | Description |
|--------|-------------|
| application_id | Primary key (e.g. `A-90412`) |
| applicant_name | Synthetic name |
| national_id | Synthetic national ID (`UT-…`) |
| dob | Date of birth |
| address | Residential address (ring shares a few addresses) |
| employer | Claimed employer |
| declared_annual_income_eur | Income stated on the application |
| monthly_benefit_eur | Benefit requested/awarded per month |
| iban | Bank account (ring largely shares `…4471`) |
| phone | Contact number (ring shares some) |
| benefit_types | `;`-separated (unemployment, housing) |
| channel | web / mobile |
| submitted_at | ISO timestamp |
| cluster_id | `4471` for ring members, blank otherwise |

## submission_telemetry.csv
Per-submission signals for the Cyber Signals Agent. Stream to Sentinel / Azure ML.

| Column | Description |
|--------|-------------|
| application_id | FK → applications |
| submitted_at | ISO timestamp |
| source_ip | Submission IP (ring all `203.0.113.45`) |
| asn / asn_type | Network + class (`hosting/vpn` vs `residential`) |
| device_fingerprint | Device hash (ring reuses one) |
| fields_per_second | Form-fill speed (ring ≈13.5 = bot; humans <1) |
| session_duration_s | Session length |
| user_agent | Browser / automation signature |

## tax_records.csv
Authoritative income for the Consistency Checker cross-match.

| Column | Description |
|--------|-------------|
| national_id | FK → applications.national_id |
| reported_annual_income_eur | Income on file (ring = 0 / no record) |
| declared_annual_income_eur | Income declared on application |
| variance_pct | Declared vs reported (`n/a` when no record) |
| match | true/false |
| source | `matched`, `mismatch`, or `no-record` |

## business_registry.csv
Employer verification. "Northwind Staffing Solutions LLC" is **UNREGISTERED / VAT-INVALID**; controls are active.

| Column | Description |
|--------|-------------|
| employer_name, registration_status, vat_id, vat_valid, registered_address, notes | Registry fields |

## graph_edges.csv
Edge list for the Cosmos DB (Gremlin) relationship graph (ring subgraph only).

| Column | Description |
|--------|-------------|
| source_id | Application vertex |
| target_id | Entity vertex (`ip:…`, `device:…`, `employer:…`, `iban:…`, `phone:…`, `address:…`) |
| target_type | ip / device / employer / iban / phone / address |
| edge_type | USED_IP, USED_DEVICE, CLAIMS_EMPLOYER, USES_IBAN, USES_PHONE, RESIDES_AT |

**Gremlin load sketch:** upsert one vertex per distinct `source_id` and `target_id`, then add an
`edge_type` edge for each row. Shared `target_id` vertices (the IP, employer, IBAN, phones) are what
make the ring visible.

## watchlist.csv
Known-bad indicators emitted by the investigation (IP, device, IBAN, employer, phone, ASN) for reuse
in future screening.
