# Project plan: work-order tracker

This plan orders the build into nine releases, R0 to R8, each usable on its own and ending with a checkable definition of done. It schedules every governance requirement into a release, lists the prerequisites each release needs, and records the risks to delivery. It implements the [requirements](../requirements/requirements.md) and the [architecture](../design/architecture.md).

## Working rules

- Each release is delivered as a series of small pull requests, each reviewed and merged into main with passing checks (engineering standards).
- Within a release, one component or feature is built and verified before the next starts.
- A deviation from the design is raised before it is made and recorded in an ADR.
- Governance requirements are implemented in the same release as the features they protect.
- A release is complete only when every item in its definition of done has a recorded result.

## Releases

| Release | Scope | Requirements | Definition of done |
|---|---|---|---|
| R0 Foundations | Remove the server-rendered pages and SQLite; settings with `pydantic-settings`; Alembic baseline; CI with Ruff, mypy and tests against PostgreSQL; local kind cluster with Calico; Flux; CloudNativePG; Envoy Gateway and cert-manager; default-deny network policies; SOPS-encrypted secrets; an API that answers health checks | NFR-11 and NFR-14 (start); ADR 0001 to 0003, 0006, 0008, 0011 to 0013, 0016 | `/health/ready` answers through the Gateway on the local cluster; CI passes on a pull request; the network-policy negative tests pass; the database takes a backup |
| R1 Accounts and access | Users, roles, trades and supervisors; login with stored tokens; Argon2id and password rules; rate limiting; deactivation; policy module with deny-by-default test; privacy notice and acknowledgement; audit log | FR-1, FR-24, FR-25; GR-1, GR-4 (start); NFR-9, NFR-10 | Every endpoint tested as every role; a deactivated user is refused on the next request; the privacy notice must be acknowledged before other use |
| R2 Reference data and the SLA clock | Customers, buildings, contacts, contracts and SLA terms; working calendar and holidays; SLA clock module | FR-2, FR-5 (clock), FR-26; NFR-8 | AC-1, AC-2 and AC-3 pass; property-based tests pass |
| R3 Work-order core | Logging with duplicate warning; assignment; technician arrival, holds and completion; lifecycle; history; version checks; idempotency keys | FR-3 to FR-8, FR-10, FR-12, FR-18, FR-29; NFR-5 | A job moves from logged to completed with a full history; AC-4, AC-5 and AC-6 pass |
| R4 Quality of completion | Parts and billable flag; corrections with approval; verification; deadline list; spot checks | FR-9, FR-11, FR-13, FR-23, FR-28; GR-8 | AC-7 passes; spot-check selection and recording work |
| R5 Planned maintenance and scheduled tasks | Maintenance schedules; CronJobs for planned work orders, spot checks and clean-up; task-run records | FR-14, FR-17 | Planned work orders are created on Africa/Lagos time; a repeated run creates no duplicates |
| R6 Reports | Weekly SLA report; record completeness report; billable-extras CSV; customer job log; search | FR-15, FR-16, FR-19, FR-21, FR-27 | AC-8 and AC-13 pass |
| R7 Governance automation | Finding, exporting, correcting and restricting one person's data; retention task with pseudonymisation; tests that logs contain no secrets or contact details | GR-2, GR-3, GR-4 (complete) | AC-11 and AC-12 pass |
| R8 Hardening and pilot | Metrics and probes; response compression; load tests; backup restore test; image scans; OpenAPI check; deployment to the pilot environment | NFR-1 to NFR-4, NFR-7, NFR-12; FR-30 | NFR-1 met at 18 requests per second; a point-in-time restore is tested and recorded; the pilot answers health checks |

R0 builds the platform every later release depends on. R1 comes next because every endpoint needs authentication and authorisation. R2 isolates the service level agreement (SLA) clock, the most rule-heavy component, so that it is tested before any job depends on it. R3 and R4 deliver the core product; R5 and R6 add scheduled work and reports; R7 completes the governance automation; R8 proves performance and recovery and deploys the pilot. FR-20 (CSV import) and FR-22 (assignment email) follow R8 if capacity allows.

## Milestones

| Milestone | Reached when |
|---|---|
| M0 Platform running | R0 is done |
| M1 Secure API | R1 is done |
| M2 SLA clock verified | R2 is done |
| M3 End-to-end job | R3 and R4 are done |
| M4 Planned work and reports | R5 and R6 are done |
| M5 Governance complete | R7 is done |
| M6 Pilot live and measured | R8 is done; testing and evaluation starts |

Each milestone is reached only when all its releases meet their definitions of done.

## Governance schedule

| Governance item | Release or phase | Evidence |
|---|---|---|
| GR-1 Lawful basis and privacy notice; written legitimate interests assessments for P-3 to P-6 | R1 | Notice text and acknowledgement tests; assessments in `docs/governance/` |
| GR-2 Data subject rights | R7 | AC-11 and the rights procedure |
| GR-3 Retention and deletion | R5 (scheduled task platform), R7 (retention task) | AC-12 and a recorded retention run |
| GR-4 Access control and audit logging | R1 (policy module, audit log), R7 (export logging, log-content tests) | Role tests; audit log entries |
| GR-5 Human oversight of AI output | Not applicable | Tier review at each exit gate |
| GR-6 Fairness | Not applicable | Tier review at each exit gate |
| GR-7 Breach response | R8 (security event logging); monitoring and operations (runbook) | Runbook walk-through |
| GR-8 Data minimisation | R4 (notes reminder field), every release (schema compared with the data inventory) | Inventory review at each release |
| DPIA measures R1 to R10 | R1: security and transparency (R5, R9); R1 and R3: access to personal data (R4); R3, R4 and R6: fair and accurate times (R1, R7); R4: corrections and the notes reminder (R3, R10); R6: team-level reporting (R2); R7: retention and correction of notes (R6, R10); deployment: data location (R8) | Each measure's requirement tested in its release |
| Go-live governance checklist, including the client's commitment on the use of SLA figures and the production transfer decision | Deployment | Signed checklist |

Every governance requirement for Tier 1 is scheduled in a release or a later phase. The data protection impact assessment measures are delivered with the requirements that implement them.

## Prerequisites

| Release | Prerequisites |
|---|---|
| R0 | At least 20 GB free on the development machine; Docker, `kubectl`, `kind`, the Flux command-line tool, `sops`, `age` and `uv` installed; branch protection enabled on main |
| R1 | R0 done; a bundled common-password list chosen, with its source and licence recorded |
| R2 | R1 done; the Nigerian public holidays for the current year entered as test data |
| R3 to R7 | The previous release done |
| R8 | R7 done; an Oracle Cloud Always Free account in the Johannesburg region; free-tier terms checked again |

Each prerequisite is confirmed before its release starts.

## Delivery risks

This register combines the [design risks](../design/design-risks.md) with risks to the schedule. Risks to people are in the [data protection impact assessment](../governance/dpia.md).

| ID | Risk | Likelihood | Impact | Response | Owner |
|---|---|---|---|---|---|
| PR-1 | Build capacity comes from one part-time developer who is learning the platform, so releases take longer than planned | High | High | Small releases; actual effort compared with the estimate after each release and the remaining plan adjusted | Engagement lead |
| PR-2 | R0 stalls because several platform components are new (design risk DR-4) | High | High | Components installed one at a time, each verified before the next; the release is split into pull requests per component | Platform engineer |
| PR-3 | Scope grows during the build | Medium | High | Changes go through the requirements document and an ADR; Should and Could items wait until after R8 | Engagement lead |
| PR-4 | A tool changes status or a version breaks compatibility during the build (DR-10) | Medium | Medium | Versions pinned; changes made by superseding ADRs | Platform engineer |
| PR-5 | The development machine runs out of disk space or memory again (DR-5) | Medium | High | Free space checked before each release; unused images and clusters removed | Platform engineer |
| PR-6 | The client application is not ready when the pilot starts (DR-2) | Medium | Medium | The API is tested through its OpenAPI description and automated tests; pilot measurements that need staff use wait for the client application | Engagement lead |
| PR-7 | The pilot account cannot be created or the free tier changes (DR-6) | Medium | Medium | Checked before R8; the local environment remains the fallback for all testing | Platform engineer |
| PR-8 | Technicians record times late once the system is used (DR-1) | High | High | Spot checks, training and the go-live governance checklist | Engagement lead |

The first two risks are the most likely to affect delivery, and both are reduced by building in small verified steps. The remaining design risks (DR-7 to DR-9, DR-11 to DR-14) keep the responses recorded in the design risks document.
