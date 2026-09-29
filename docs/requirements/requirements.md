# Requirements: work-order tracker

This document states what the first release of the work-order tracker must do, how well it must do it, and how it protects people and their data. Every requirement has an identifier, a priority, a source and a method of verification. Sources refer to the [engagement brief](../discovery/engagement-brief.md) (failure points P1 to P9 and pain points PP1 to PP4), the [problem statement](../problem/problem-statement.md) (targets T1 to T5 and the people who could be harmed) and the [data inventory](../governance/data-inventory.md).

Priorities follow the MoSCoW scheme: **Must** (the release fails without it), **Should** (important, with a manual workaround), **Could** (included if time allows). Items the release will not include are listed under "Out of scope".

The first release is a backend application programming interface (API). People use the system through a client application (web or mobile) that is built separately, by another developer, against the API's published contract. Requirements therefore state what the API accepts, returns and enforces.

## Definitions

- **Service level agreement (SLA) times:** each contract sets, per urgency level, a **response time** (the technician arrives) and a **resolution time** (the fault is fixed).
- **Working hours:** 07:00 to 19:00 West Africa Time (WAT), Monday to Saturday, excluding public holidays. One working day is 12 working hours. One working calendar applies to all contracts.
- **Urgency levels:** urgent, high and routine. The response and resolution times for each level are set per contract.
- **Clock hours:** every hour of every day. Urgent breakdowns are measured in clock hours; all other urgency levels are measured in working hours.
- **Customer-caused hold:** a pause for a reason on a fixed list that is the customer's responsibility, such as no access to the site. Customer-caused holds pause the SLA clock; holds for the client's own reasons, such as awaiting parts, do not.
- **Client application:** the web or mobile application, built separately, through which staff use the API.
- **Roles:** administrator, coordinator, supervisor, technician, manager and finance. The operations manager holds administrator rights.

## Functional requirements

| ID | The system must… | Priority | Source | How it is verified |
|---|---|---|---|---|
| FR-1 | Allow only administrators to create, edit and deactivate staff accounts; give each account one role, and give each technician one trade and one supervisor | Must | Code review (self-registration as administrator); team reporting | API tests: self-registration is refused; role, trade and supervisor are set only by an administrator |
| FR-2 | Store customers, buildings (with area of Lagos and building type) and each building's contract terms: included breakdown call-outs per month, response and resolution times per urgency level, and service credit amount | Must | PP1, PP2 | API tests |
| FR-3 | Allow coordinators, and supervisors on call, to log a breakdown with building, trade, fault, urgency and reporting channel; record the logging time automatically; accept an earlier "reported at" time and refuse a later one | Must | P1, P3, T1 | AC-4 |
| FR-4 | Return open jobs for the same building and trade when a request is being logged | Must | P2 | API test |
| FR-5 | Calculate each job's response and resolution due times from its reported time, the contract's SLA times and the working calendar; pause the clock during confirmed customer-caused holds; prevent any user from editing due times directly | Must | P3, PP1 | AC-1, AC-2, AC-3 |
| FR-6 | Allow a supervisor to assign or reassign a job to a technician of the right trade, and return each technician's open jobs and their buildings | Must | P4 | API tests |
| FR-7 | Return to each technician only their own assigned jobs: building, area, fault, urgency, due times and the customer contact | Must | P4, P5 | API tests |
| FR-8 | Allow a technician to record "arrived", "on hold" (with a reason from a fixed list) and "completed" (with optional notes); use the server's time for SLA purposes and store the phone's time alongside; apply each save once, even if it is sent more than once | Must | P5; harm: technicians blamed for recording errors | AC-6 |
| FR-9 | Allow a technician to record parts used and to mark work as outside the contract; flag the job as billable, including breakdown call-outs beyond the building's monthly allowance | Must | P6, PP2 | API tests |
| FR-10 | Enforce the job lifecycle (open, assigned, in progress, on hold, completed, verified, cancelled) and accept only allowed moves; allow cancellation only before arrival and only with a reason | Must | P2, P5, P8 | API tests for every allowed and refused move; AC-8 |
| FR-11 | Allow a supervisor to correct a recorded time or status only with a written reason, keeping the original value; require a manager's approval for any correction that changes a missed SLA to a met one; flag every correction in the weekly SLA report | Must | Harm: technicians blamed; supervisors judged on their own figures | AC-7 |
| FR-12 | Record every change to a job (user, time, old value, new value) and return it as the job's history | Must | P8, PP1 | API tests |
| FR-13 | Return to supervisors a deadline list of jobs with 25% or less of their SLA time remaining and jobs already overdue | Must | P4, P5, T2 | API tests |
| FR-14 | Store planned maintenance schedules with a calendar frequency (weekly, monthly or quarterly) and a completion tolerance (default 3 working days), and create planned work orders ahead of each due date | Must | P9, PP3, T5 | API tests with time moved forward |
| FR-15 | Produce a weekly SLA compliance report by customer, trade and team for both response and resolution times, excluding cancelled jobs, totalling customer-caused holds per team and flagging corrected times | Must | P7, PP1, T2 | API tests; AC-8 |
| FR-16 | Produce a monthly billable-extras list per customer as a comma-separated values (CSV) file for the finance team, neutralising any cell that begins with =, +, - or @ | Must | P6, PP2 | AC-13 |
| FR-17 | Produce a planned maintenance completion report showing visits completed within their tolerance | Must | PP3, T5 | API tests |
| FR-18 | Refuse a save when another user has changed the same job since it was opened, with a clear message, instead of overwriting the other change | Must | Harm: wrong reports | AC-5 |
| FR-19 | Produce a job log per customer with reported, due and completed times, for use as evidence in disputes | Should | P8, T3 | API test |
| FR-20 | Import buildings, customer contacts and planned maintenance schedules once from CSV files | Should | Data inventory: import of current lists | Import test with synthetic files |
| FR-21 | Search and filter jobs by status, building, customer, technician and date | Should | P4, P7 | API tests |
| FR-22 | Email a technician when a job is assigned to them | Could | P4 | API test with a test mail server |
| FR-23 | Allow a supervisor to verify a completed job, or to reopen it with a reason | Must | Governance: supervisor verification replaces live location tracking | API tests |
| FR-24 | Allow an administrator to reset a user's password, forcing a change at the next login, and allow every user to change their own password; accept only passwords of 15 to 64 characters that are not on a list of common passwords, with no composition rules and no forced periodic change | Must | Staff locked out at the start of a shift | API tests |
| FR-25 | Refuse to deactivate a user who still has open jobs, and refuse a deactivated user's login token on its next request | Must | Jobs stranded when staff leave | AC-9 |
| FR-26 | Allow an administrator to maintain the working calendar and public holidays at short notice; recalculate the due times of open jobs affected by a change and record the recalculation in each job's history | Must | Public holidays confirmed close to their date | API tests |
| FR-27 | Produce a weekly record completeness report listing breakdowns missing a reported, arrival or completion time | Must | T1 | API tests |
| FR-28 | Select a random 5% of each week's completed breakdowns for spot checks and allow supervisors to record whether the recorded times were confirmed within 30 minutes | Must | T1a | API tests |
| FR-29 | Require supervisor confirmation before a customer-caused hold longer than 1 hour pauses the SLA clock | Must | Holds used to hide late arrival | AC-3 |
| FR-30 | Publish a machine-readable OpenAPI description of every endpoint, with example requests, responses and error codes | Must | Client application built separately against the API | Automated check that the published description matches the running API; review by the client application developer |

FR-1 to FR-5 cover getting a job into the system with a correct SLA clock. FR-6 to FR-13 cover moving the job to completion, with protections for the people who could be harmed by recording errors (FR-8, FR-11, FR-18, FR-29). FR-14 to FR-17 and FR-27 produce the reports that measure the targets. FR-23 to FR-26 and FR-28 cover verification, account management, the working calendar and spot checks. FR-30 publishes the contract that the separately built client application depends on. FR-19 to FR-22 have manual workarounds and are therefore Should or Could.

## Non-functional requirements

| ID | Quality | Requirement | How it is verified |
|---|---|---|---|
| NFR-1 | Performance | At 18 requests per second, 95% of API requests other than logins complete within 500 milliseconds and fewer than 0.1% fail; at 1 login per second during that load, 95% of logins complete within 2 seconds and other requests still meet their target | Load test against a test deployment with resources matching the chosen hosting |
| NFR-2 | Scalability | NFR-1 holds with data for 150 technicians and 2,000 work orders a week | Load test with doubled synthetic data |
| NFR-3 | Concurrency | Under the NFR-1 load, with many users updating jobs at the same time, no update is lost and no database locking errors occur | Load test with concurrent updates; job histories compared with the requests sent |
| NFR-4 | Mobile efficiency | Responses are compressed; a technician's job list for one day (up to 20 jobs) transfers at most 20 KB | API test measuring response size |
| NFR-5 | Unreliable networks | Every request that changes data can be retried safely: a repeated request with the same request ID is applied once and returns the original result | AC-6 |
| NFR-6 | API usability | Completing a job is a single request; every error response contains a stable error code and a plain-language message | API tests; review of the OpenAPI description |
| NFR-7 | Availability | Availability from 07:00 to 19:00 WAT, Monday to Saturday, is measured during a 2-week pilot and reported; the production hosting recommendation states the hosting and monthly cost needed for at least 99.5% | Uptime monitor during the pilot; deployment recommendation |
| NFR-8 | Time correctness | All times are stored in Coordinated Universal Time (UTC) and returned in WAT; due-time calculations are correct across midnight, Sundays and public holidays | AC-1, AC-2; automated tests near midnight |
| NFR-9 | Security: transport and login | Encrypted connections (HTTPS) only; passwords stored as Argon2id hashes with at least the OWASP minimum parameters; access tokens are random, stored only as hashes, sent in the Authorization header, expire within 8 hours and are checked on every request, so that a deactivated account or revoked token is refused on its next request; login is rate-limited after 5 failed attempts in 15 minutes | Automated tests |
| NFR-10 | Security: authorisation | Every endpoint checks the user's role, and each role reaches only the data the functional requirements allow; a job belonging to another technician is reported as not found | Automated tests calling every endpoint as every role; AC-10 |
| NFR-11 | Security: secrets and dependencies | No secret appears in source code or git history; dependencies are pinned and scanned for known vulnerabilities on every change | Automated secret and dependency scans in continuous integration (CI) |
| NFR-12 | Recovery | Daily backups; a recovery point objective (RPO, the most data that can be lost) of 24 hours; a recovery time objective (RTO, the time to restore service) of 4 hours; a restore is tested before go-live; backup storage location and retention are recorded in the data inventory | Restore test recorded in a runbook |
| NFR-13 | Cost | Infrastructure costs nothing each month during the engagement; any paid service requires a cost estimate, a teardown plan and an Architecture Decision Record (ADR) before it is created | Hosting bills; ADR list |
| NFR-14 | Maintainability | Formatting and linting (Ruff) and type checking (mypy) pass; automated tests cover at least 80% of lines; all run in CI on every pull request | CI results on each pull request |

NFR-1 to NFR-3 cover the morning peak: 18 requests per second allows for twice today's staff and a threefold burst at 07:45. NFR-4 to NFR-6 keep the API efficient and safe for a client application used on phones with weak mobile data. NFR-7 is measured rather than guaranteed, because free hosting carries no uptime commitment. NFR-8 to NFR-12 cover correctness, security and recovery; NFR-13 and NFR-14 cover cost and code quality.

## Governance requirements

| ID | Area | Requirement | Tier | How it is verified |
|---|---|---|---|---|
| GR-1 | Lawful basis and privacy notice | Each use of personal data in the data inventory has a recorded lawful basis: contract of employment for staff access and job work (P-1, P-2); legitimate interests, supported by a written legitimate interests assessment (LIA), for customer contacts, the change history, team-level reporting and security logs (P-3 to P-6). Consent is not used. A plain-language privacy notice for staff and for customer contacts is provided by the API, and each user's acknowledgement is recorded before other use | 1+ | Data inventory review; API tests for the notice and acknowledgement |
| GR-2 | Data subject rights | An administrator can find, export as a machine-readable file, correct and restrict one person's data, and apply deletion under GR-3, in one documented procedure; exports contain the person's own data and actions but not other people's personal details; requests are answered within one month | 1+ | AC-11; automated test covering export, correction, restriction and deletion |
| GR-3 | Retention and deletion | Work orders and their history are kept in full for 2 years after closure, then staff identities on them are pseudonymised, and they are deleted after 6 years; a leaver's account details are pseudonymised 12 months after deactivation; customer contacts are deleted 12 months after their contract ends or when replaced; logs are kept for 90 days; the audit log of administrator actions and exports is kept for 2 years; backups are kept for 30 days on a rolling basis; retention runs automatically | 1+ | AC-12; automated tests with time moved forward; record of each retention run |
| GR-4 | Access control and audit logging | Access follows role (NFR-10); every change to personal data, every export and every administrator action is logged with user, action and time; logs never contain passwords or login tokens | 1+ | Automated tests per role; log inspection |
| GR-5 | Human oversight of AI output | Not applicable: the system contains no artificial intelligence (AI) component, as recorded in the problem statement | 2+ | Tier review at each exit gate |
| GR-6 | Fairness | Not applicable: the system makes no automated decisions about people and is not a Tier 3 system | 3 | Tier review at each exit gate |
| GR-7 | Breach response | Security events are logged in enough detail to investigate a breach; a breach response runbook enables the client to notify the regulator within 72 hours of becoming aware of a breach | 1+ | Runbook walk-through during monitoring and operations |
| GR-8 | Data minimisation | Only the fields listed in the data inventory are collected; the job notes field reminds users not to record health information or unnecessary personal details | 1+ | Data inventory compared with the database schema; manual check of the reminder |

GR-1 to GR-4, GR-7 and GR-8 apply because the system holds personal data (Tier 1). GR-5 and GR-6 apply only to systems with AI components and are recorded as not applicable, with the reason, so that each tier review can confirm the position. The 6-year deletion period in GR-3 reflects a common period for contract disputes and is subject to confirmation of Nigerian limitation periods.

## Success metrics

| Metric | Baseline | Target | Measured by |
|---|---|---|---|
| T1: breakdowns with reported, arrival and completion times recorded | Not measured | 98% or more within 8 weeks of go-live | Record completeness report (FR-27) |
| T1a: spot-checked breakdowns with times confirmed within 30 minutes | Not measured | 95% or more within 8 weeks of go-live | Spot-check records (FR-28) |
| T2: breakdowns within resolution SLA, four-week average | Trusted four-week baseline from weeks 1 to 4 | Baseline plus 2 percentage points by week 16 | Weekly SLA compliance report (FR-15) |
| T3: service credits paid per month | About ₦8,700,000 (estimate) | At least 25% lower by week 16 | Credit records from the finance team, checked against the SLA report |
| T4: value of parts recorded on jobs as a share of parts issued from stores | Not measured | 95% or more within 8 weeks of go-live | Monthly reconciliation with the finance team's stores records |
| T5: planned visits completed within tolerance | 92% (estimate) | 97% or more within 12 weeks of go-live | Planned maintenance completion report (FR-17) |

Each target in the problem statement is measured by a named source, and applies once a client application built on the API is in use. T1, T1a, T2 and T5 come from reports the system produces. T3 and T4 depend on the finance team's records, because service credits are deducted by customers and parts are issued from stores outside the system.

## Acceptance criteria

- **AC-1:** Given a contract with an urgent resolution time of 4 hours, when an urgent breakdown is reported on Friday at 22:30 WAT, then its resolution due time is Saturday at 02:30 WAT.
- **AC-2:** Given a routine resolution time of 2 working days (24 working hours), when a routine breakdown is reported on Saturday at 18:00 WAT, then its resolution due time is Tuesday at 18:00 WAT; if the Monday is a public holiday, the due time is Wednesday at 18:00 WAT.
- **AC-3:** Given an urgent job due at 13:00, when it is on hold for "no access to site" from 10:00 to 11:30 and a supervisor confirms the hold, then its due time becomes 14:30; when the hold reason is "awaiting parts", the due time stays at 13:00; when a customer-caused hold longer than 1 hour is not confirmed, the due time stays at 13:00.
- **AC-4:** Given a coordinator logging a request at 08:10, when "reported at 07:40" is entered, then it is accepted and recorded in the job's history; when "reported at 08:30" is entered, then it is refused with a message.
- **AC-5:** Given two supervisors who opened the same job, when the second saves after the first, then the second save is refused with status 412 and the message "This job was changed by another user; reload to see the latest version", and the first change is kept.
- **AC-6:** Given a completion request with request ID R, when the same request with ID R is sent again after a timeout, then the job is completed once, the second response returns the original result, and the completion time is the server's time of first receipt, with the phone's time of the original request stored alongside.
- **AC-7:** Given a job recorded as missing its resolution SLA, when a supervisor corrects its completion time so that it meets the SLA, then the correction waits for a manager's approval, and once approved it is flagged in the weekly SLA report.
- **AC-8:** Given a duplicate job cancelled with a reason before arrival, when the weekly SLA report runs, then the job is excluded from compliance figures and listed as cancelled.
- **AC-9:** Given a technician with 2 open jobs, when an administrator tries to deactivate them, then the deactivation is refused until both jobs are reassigned; after deactivation, the technician's existing login token is refused on its next request.
- **AC-10:** Given technician A, when A requests a job assigned to technician B, then the system responds "not found".
- **AC-11:** Given a staff member, when an administrator runs the export for them, then one file contains their account details, their assigned jobs and the history entries they made, without other people's personal details, and the export is recorded in the audit log.
- **AC-12:** Given a job closed 2 years and 1 day ago, when the retention job runs, then the technician's identity on that job is replaced by a code, and the job's times and status remain.
- **AC-13:** Given a job note beginning with "=SUM(", when the billable-extras CSV is downloaded, then the cell begins with an apostrophe, so a spreadsheet shows it as text instead of running it as a formula.

The acceptance criteria cover the rules most likely to be built incorrectly: the SLA clock (AC-1 to AC-4), conflicting and repeated saves (AC-5, AC-6), fairness to staff (AC-7, AC-9), report accuracy (AC-8), security (AC-10, AC-13) and data protection (AC-11, AC-12). Every other requirement is verified by the method in its table row.

## Expectations of the client application

The client application is outside the scope of this repository and is built and tested by its own developer. The API is designed for a client application that meets the expectations below; they are listed here so that both sides work to the same contract.

| ID | The client application is expected to… | Related requirement |
|---|---|---|
| CA-1 | Let a technician mark an assigned job completed in no more than 3 taps from their job list, with notes optional, on a screen 360 pixels wide | NFR-6 |
| CA-2 | Keep a user's input on screen when a request fails, show a clear message, and retry with the same request ID | NFR-5, AC-6 |
| CA-3 | Send the access token in the Authorization header of every request, store it in the device's secure storage, and return the user to the login screen when the API refuses it | NFR-9, FR-25 |
| CA-4 | Show the privacy notice returned by the API and send the user's acknowledgement before any other use | GR-1 |
| CA-5 | Show the duplicate-job warning returned while a request is being logged | FR-4 |
| CA-6 | Show the reminder not to record health information or unnecessary personal details next to the job notes field | GR-8 |
| CA-7 | Show all times in West Africa Time as returned by the API | NFR-8 |
| CA-8 | Show the plain-language message from each API error response, and treat "not found" as a normal result | NFR-6, AC-10 |
| CA-9 | Keep the first load of any web version to at most 150 KB and usable within 5 seconds at 400 kbit/s with 400 milliseconds of latency | Constraint: slow mobile data |

These expectations are verified by the client application's developer. The API's side of each is verified by the requirement in the last column.

## Out of scope

The first release does not include the items listed under "Out of scope" in the engagement brief, including the user interface (web or mobile client application), a customer portal, invoicing, live location tracking, full offline operation, photo uploads, automatic request intake, spare-parts stock management, automatic scheduling or any AI component, payroll and HR records, schedules based on equipment running hours, jobs assigned to more than one technician, customer sign-off in the system and customer-specific working calendars.
