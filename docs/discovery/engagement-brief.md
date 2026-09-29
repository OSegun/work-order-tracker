# Engagement brief: work-order tracker

## Client

- **Industry and city:** facility maintenance; Lagos, Nigeria.
- **Size (estimate):** about 100 staff: 80 technicians in four trades (electrical and generators; heating, ventilation and air conditioning (HVAC); plumbing; general building repairs), 8 supervisors, 4 help-desk coordinators, an operations manager, a managing director and a finance team of 2. The client maintains 120 buildings for 30 customer organisations (banks, office landlords, residential estates and shopping malls) across Lagos Island (Victoria Island, Ikoyi, Lekki) and the Mainland (Ikeja, Yaba). It handles about 1,000 work orders a week, 60% planned maintenance and 40% breakdowns, over a six-day working week. The growth plan is 150 technicians within two years. A residential estate counts as one building in its contract but contains many housing units, which accounts for much of the breakdown volume.
- **What the business does and how it earns money:** the client services and repairs building equipment for its customers under a monthly contract per building. The monthly fee covers planned maintenance and a set number of breakdown call-outs, with service level agreement (SLA) times for each urgency level: a response time (the technician arrives) and a resolution time (the fault is fixed). When a breakdown misses its SLA, the customer deducts a service credit from the fee. Call-outs beyond the included number, and parts, are billed separately. The average monthly fee is ₦1,200,000 per building, about ₦144,000,000 a month across 120 buildings (estimate).

## Users and stakeholders

| Role | What they need | How they are affected today |
|---|---|---|
| Help-desk coordinator (4; system user) | Log a request quickly, with building, fault and urgency, and see whether it is already logged | Requests arrive by phone, email and WhatsApp and are copied into a shared spreadsheet; some are lost or logged twice |
| Supervisor (8; system user) | Assign jobs to the right technician, and see team workload and jobs close to their SLA deadline | Phones technicians for status updates; learns about late jobs when a customer complains |
| Technician (80; system user on an Android phone) | See the day's jobs with location and details, and update status and notes on site | Receives jobs by call or WhatsApp; fills paper job cards that reach the office days later |
| Operations manager (system user; holds administrator rights) | SLA compliance by customer, trade and team; workload balance; staff accounts managed in one place | Builds a weekly report by hand from spreadsheets and job cards |
| Managing director (reads reports) | A monthly view of SLA performance, service credits paid and billable extras captured | Sees problems only after credits are deducted or a contract is at risk |
| Finance team (2; reads reports) | A monthly list of billable extras per customer, with evidence | Depends on paper job cards; extras that are not written down are never billed |
| Customer facility managers (30 organisations; not system users in the first release) | Jobs completed within SLA, and proof on request | Chase the client by phone for updates |
| Building occupants (not system users) | Faults fixed quickly | Report faults to their facility manager and wait |
| System support (external technical support provider) | Monitor the system, restore it after a failure and apply updates | Not applicable: the client has no in-house technical staff |

The first four roles work in the system every day. The managing director and the finance team read its results. Customer facility managers and building occupants are outside the client's organisation: they never log in, but the business exists to serve them. System support keeps the system running after handover, because the client employs no technical staff. Technicians are also the people whose work the system records most closely, which the governance section addresses.

## Current process

### Breakdown (40% of work orders)

1. A building occupant reports a fault to the customer's facility manager.
2. The facility manager reports it to the client by phone, email or WhatsApp message to a coordinator's phone.
   - Failure point P1: requests arrive through three channels and on personal phones; requests sent after hours or to an absent coordinator can be missed.
   - Outside coordinators' hours (07:00 to 19:00, Monday to Saturday), an on-call supervisor takes urgent calls by phone and sends a technician; the request is added to the spreadsheet the next working morning.
3. A coordinator logs the request in a shared spreadsheet: building, fault, urgency and time received.
   - Failure point P2: a fault reported through two channels is logged twice.
   - Failure point P3: the time received is typed by hand, sometimes much later, so the SLA clock starts at the wrong time.
4. The coordinator tells the supervisor for the trade by phone or WhatsApp.
5. The supervisor chooses a technician from memory of who is free and nearby, and phones them.
   - Failure point P4: there is no view of each technician's workload or current job location, so work collects on a few technicians and travel time across Lagos is not considered.
6. The technician travels, completes the repair and writes a paper job card: work done, parts used, arrival time and completion time.
7. The technician phones or messages the supervisor to report completion.
   - Failure point P5: when this is forgotten, the job appears open for days; late jobs surface only through customer complaints.
8. The paper job card returns to the office on the technician's next visit, often several days later, and a coordinator updates the spreadsheet.
   - Failure point P6: cards are lost or unreadable; extra parts and out-of-scope work recorded on them never reach finance and are never billed.
9. Each week, the operations manager compiles an SLA report by hand from the spreadsheet and job cards.
   - Failure point P7: the report takes hours, is always behind and is not fully trusted.
10. Each month, finance invoices billable extras from the cards that arrived. Separately, each customer deducts service credits for missed SLAs using its own records.
    - Failure point P8: the client cannot dispute a credit, because it has no reliable timestamps to prove a job was completed on time.

### Planned maintenance (60% of work orders)

1. Maintenance schedules are kept in a spreadsheet per customer, for example "service generator every 250 running hours" or "clean air-conditioning filters monthly".
2. Each week, a supervisor reads the schedule and assigns visits to technicians by phone or WhatsApp.
   - Failure point P9: when a supervisor is busy or absent, scheduled visits are skipped unnoticed; skipped maintenance leads to more breakdowns.
3. Steps 6 to 10 of the breakdown process then apply.

## Pain points

| Pain point | Who feels it | Cost or impact (estimate) |
|---|---|---|
| PP1. Service credits for missed or unprovable SLAs (P1, P3, P5, P8) | Managing director, operations manager, finance | About ₦8,700,000 a month (₦104,000,000 a year); about ₦4,300,000 a month of this is for jobs that were probably on time but cannot be proven |
| PP2. Billable extras never billed (P6) | Finance, managing director | About ₦2,600,000 a month (₦31,200,000 a year) |
| PP3. Planned maintenance visits skipped (P9) | Customer facility managers, building occupants, supervisors | 48 visits a week (about 208 a month), leading to more breakdowns and risk to contract renewals |
| PP4. Staff hours lost to chasing and re-typing (P2, P4, P5, P7) | Coordinators, supervisors, operations manager | 128 hours a week, about 2.7 full-time staff |

The four pain points share one root cause: there is no single, trusted, time-stamped record of each job. PP1 and PP2 are money lost every month, about ₦11,300,000 combined; PP3 is a risk that grows over time; PP4 is staff capacity spent on work a system can do.

The costs are calculated from these estimates:

- **PP1:** 1,000 work orders a week, 40% breakdowns, gives 400 breakdowns a week. 20% miss their SLA: 80 a week. At a service credit of ₦25,000 each, that is ₦2,000,000 a week, or about ₦8,700,000 a month (52 ÷ 12 weeks). Half of the misses are assumed to be jobs completed on time but recorded late or not at all.
- **PP2:** 15% of breakdowns involve billable extras (60 a week), averaging ₦40,000. 25% of these are never billed: 15 a week, or ₦600,000 a week.
- **PP3:** 60% of 1,000 work orders are planned visits (600 a week); 8% are skipped. No naira figure is given, because the cost arrives indirectly through later breakdowns and contract risk.
- **PP4:** coordinators re-type 1,000 job cards a week at 3 minutes each (50 hours); 8 supervisors spend 1.5 hours a day on status calls over 6 days (72 hours); the operations manager spends 6 hours a week on the SLA report. The total of 128 hours is divided by a 48-hour working week.

The baseline SLA compliance of 80% comes from the client's manual weekly report, which failure point P7 describes as not fully trusted.

## Governance

- **Governance tier:** Tier 1 (personal data, no AI).
- **Reason for the tier:** the system stores personal data about staff and customer contacts, and records each technician's work history. It contains no artificial intelligence (AI) or machine-learning component. Automated scoring of technicians would raise the tier and is out of scope.
- **Personal data involved:** staff name, work email, phone number, role, login details (passwords stored only as hashes) and job history with timestamps; customer facility managers' names, work phone numbers and work email addresses; free-text job notes, which can mention people. No special-category data is collected: job notes do not record health information, and injuries are handled through the client's existing safety process.
- **Location data:** the system records job arrival and completion events at buildings. It does not track technicians' live location. Because arrival is recorded by the technician, supervisors verify completed jobs and carry out spot checks.
- **Nigeria Data Protection Act 2023 (NDPA) applies:** yes. The client is a Nigerian company processing personal data in Nigeria.
- **EU General Data Protection Regulation (GDPR) applies:** not by law. The client serves buildings in Lagos only and does not offer services to, or monitor, people in the European Union. The system is designed to meet GDPR requirements as well as the NDPA.
- **Data inventory:** `docs/governance/data-inventory.md`.

## Constraints

- **Budget:** free-tier infrastructure. Any paid service requires a monthly cost estimate, a teardown plan and an Architecture Decision Record (ADR) before it is created.
- **Devices:** technicians use their own Android smartphones on mobile data; office staff use laptops. The client provides each technician with a monthly mobile-data allowance.
- **Connectivity:** mobile data at sites is slow and drops out; the API keeps technicians' requests small and safe to retry.
- **Digital skills:** technicians' confidence with apps varies; the client application requires very little typing.
- **Language:** English.
- **Technology already in use:** WhatsApp, email, spreadsheets and paper job cards; the finance team's accounting software, which the system does not connect to; an existing FastAPI code base.
- **Working hours:** the system is used mainly from 07:00 to 19:00, Monday to Saturday. Urgent faults outside those hours are handled by an on-call supervisor by phone and logged the next working morning with their true reported time.
- **Regulation:** NDPA, with the system designed to GDPR requirements.

## Out of scope

The first release does not include:

- a portal for customer facility managers; customers receive updates as they do now
- invoicing, payments or a connection to the accounting software; the system produces a monthly list of billable extras for the finance team
- live location tracking of technicians
- the user interface: a web or mobile client application is built separately, by another developer, against the API's published contract
- full offline operation; API requests are kept small and safe to retry for slow connections
- photo uploads as proof of work
- automatic intake of requests from WhatsApp, SMS or email; coordinators log requests in the system
- spare-parts stock management; parts used are recorded on each job for billing
- automatic scheduling, route planning or any AI component
- payroll, attendance or HR records
- maintenance schedules based on equipment running hours; schedules are calendar-based (weekly, monthly, quarterly)
- jobs assigned to more than one technician; each job has one lead technician, and linked jobs are logged where needed
- sign-off of completed jobs by customers in the system
- working calendars that differ by customer; one working calendar applies to all contracts

The system does not reduce travel time across Lagos or prevent missed visits. It makes both visible, so that supervisors can act on them.
