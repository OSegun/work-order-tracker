# Data protection impact assessment: work-order tracker

Required by Article 35 of the EU General Data Protection Regulation (GDPR) and by the Nigeria Data Protection Act 2023 (NDPA) when processing is likely to result in a high risk to people. This assessment follows the screening below and covers the first release described in the [requirements](../requirements/requirements.md) and the [data inventory](data-inventory.md).

## 1. Screening

| Question | Yes / No |
|---|---|
| Is personal data processed at large scale? | No: about 100 staff and 30 customer contacts |
| Is special-category data processed? | No: none is collected, and the job notes field carries a reminder (GR-8) |
| Does automated processing, including AI, make or shape decisions about people? | No: the system contains no AI; reports are grouped by team; corrections are decided by people |
| Are people systematically monitored? | Yes: each technician's arrival, completion and hold times are recorded, compared with deadlines and spot-checked |
| Is data combined from several sources? | No: one system; the one-time import covers buildings, contacts and schedules only |
| Are vulnerable people (for example children or employees) affected? | Yes: the people monitored are employees of the client |
| Is new technology used in a way people would not expect? | No: an ordinary job-tracking system, explained in the privacy notice (GR-1) |

Result: Full DPIA required. Reason: two criteria are met, systematic monitoring and data about vulnerable people (employees). Guidance from the UK Information Commissioner's Office on the European criteria states: "In most cases, a combination of two of these factors indicates the need for a DPIA", and that employees "could be considered vulnerable data subjects where a power imbalance means they cannot easily consent or object to the processing of their data by an employer."

## 2. Description of the processing

- **Purpose:** to record, assign and track repair and maintenance jobs; to measure service level agreement (SLA) compliance by customer, trade and team; to identify billable work; and to keep the system secure. The purposes are P-1 to P-6 in the data inventory.
- **Personal data involved:** staff accounts (D-1), customer contacts (D-3), work orders with times and notes (D-5), work-order history (D-6), logs (D-8), access tokens (D-9), idempotency records (D-11), failed login records (D-12) and the audit log (D-13).
- **People affected:** about 80 technicians, 8 supervisors, 4 help-desk coordinators, managers and the finance team; about 30 customer facility managers.
- **Systems and recipients:** one API service and one PostgreSQL database in a Kubernetes cluster; staff according to the access-control matrix (`docs/design/access-control.md`); an external system support provider for operation.
- **Retention:** as set in GR-3: work orders and history in full for 2 years, then pseudonymised, then deleted after 6 years; leavers' account details pseudonymised after 12 months; customer contacts deleted 12 months after contract end; logs 90 days; audit log 2 years; idempotency records 24 hours; backups 30 days.

## 3. Necessity and proportionality

- **Lawful basis for each processing purpose:** contract of employment for staff access and job work (P-1, P-2); legitimate interests, each supported by a written legitimate interests assessment, for customer contacts, the change history, team-level reporting and security logs (P-3 to P-6). Consent is not used, because employees cannot freely refuse their employer (GR-1).
- **Why each data item is necessary (data minimisation):**
  - Arrival and completion times are the evidence for SLA disputes, the main cost the system addresses.
  - The phone's time is stored alongside the server's time so that a technician recorded late by a network delay can be corrected fairly.
  - Customer contact details let technicians gain access to sites.
  - IP addresses in failed login records support protection against password guessing.
  - Live location is not collected: arrival and completion events at buildings meet the need with less intrusion.
  - Payroll, attendance and HR records are not collected.
- **How people are informed:** a plain-language privacy notice is provided through the client application and acknowledged by each user before first use (GR-1, CA-4).
- **How data subject rights are supported:** an administrator can find, export, correct and restrict one person's data and apply deletion under the retention rules, and requests are answered within one month (GR-2).

## 4. Risks to people

| ID | Risk | Likelihood (Low / Medium / High) | Severity (Low / Medium / High) | Overall |
|---|---|---|---|---|
| R1 | A technician is recorded as late because of a system error, a failed save or a network delay, and is blamed or disciplined | Medium | High | High |
| R2 | Recorded times are used to rank or discipline individual technicians, beyond the stated purposes | Medium | High | High |
| R3 | A supervisor uses corrections to improve their team's figures or to treat a technician unfairly | Low | Medium | Medium |
| R4 | Staff see more personal data than their work needs | Medium | Low | Medium |
| R5 | A security breach exposes staff or customer contact data | Low | High | Medium |
| R6 | Personal data is kept longer than needed | Medium | Medium | Medium |
| R7 | Inaccurate times are recorded, for example a request logged late | Medium | Medium | Medium |
| R8 | Real personal data is stored outside Nigeria in production without a lawful transfer mechanism | Medium | Medium | Medium |
| R9 | Staff do not understand how their work data is used | Medium | Medium | Medium |
| R10 | Health information is written into job notes | Low | High | Medium |

The two high risks, R1 and R2, both concern how technicians' recorded times are used. The remaining risks are rated medium before the measures in section 5.

## 5. Measures to reduce risk

| Risk ID | Measure | Remaining risk | Approved by |
|---|---|---|---|
| R1 | Server and phone times stored side by side; safe retries with idempotency keys (ADR 0010); corrections with a written reason, and manager approval when a missed SLA becomes met (FR-11); every change visible in the append-only history (ADR 0015); supervisor verification (FR-23); the client's working practice that SLA figures alone are not a basis for disciplinary action | Low | Controller |
| R2 | SLA reporting by customer, trade and team only (FR-15, P-5); individual ranking and automated scoring out of scope; any change of purpose requires a new governance decision and tier review; purposes stated in the privacy notice | Low | Controller |
| R3 | Supervisors act only on their own team (ADR 0005); corrections flagged in the weekly report; manager approval for corrections that change a miss to a meet; append-only history and audit log | Low | Controller |
| R4 | Role, scope and state checks through one policy module (ADR 0005); technicians see customer contacts only for their own jobs; the finance team sees contract terms and billable extras only | Low | Controller |
| R5 | Argon2id password hashing with 15-character minimum passwords and a common-password check; hashed, revocable access tokens (ADR 0004); rate-limited login; encrypted connections (ADR 0006); default-deny network policies (ADR 0008); encrypted secrets (ADR 0016); audit log (ADR 0015); breach response runbook enabling notification within 72 hours (GR-7). Multi-factor authentication is not in the first release and is recorded as a design risk | Low to Medium | Controller |
| R6 | Automated retention (GR-3, ADR 0011); idempotency records deleted after 24 hours; logs kept 90 days; backups kept 30 days | Low | Controller |
| R7 | Logging time set by the system; "reported at" may only be earlier than logging (FR-3); record completeness report (FR-27); weekly spot checks (FR-28) | Low | Controller |
| R8 | Development and pilot use synthetic data only (ADR 0014); before production go-live, hosting either keeps data in Nigeria or relies on a lawful transfer mechanism under section 41 of the NDPA, recorded in the data inventory and the go-live governance checklist | Low | Controller |
| R9 | Privacy notice with acknowledgement (GR-1); staff briefing at go-live; data subject rights procedure (GR-2) | Low | Controller |
| R10 | Reminder beside the notes field (GR-8, CA-6); notes can be corrected or removed through the rights procedure (GR-2) | Low | Controller |

After these measures, no risk remains high. The measures for R1, R2 and R8 depend partly on the client's own practices and hosting decision, which the go-live governance checklist confirms.

## 6. Sign-off

- **Data protection officer advice:** the client has not appointed a data protection officer; advice was provided by the engagement's governance lead, who recommends proceeding with the measures in section 5.
- **Controller decision:** the processing proceeds with the measures in section 5. Approved for the build phase on 29 September 2026.
