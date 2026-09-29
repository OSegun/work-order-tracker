# Problem statement: work-order tracker

## Statement

The client, a facility-maintenance company in Lagos, pays about ₦8,700,000 a month in service credits because breakdowns are recorded as missing their service level agreement (SLA) times. Its manual weekly report puts SLA compliance for breakdowns at 80%, but requests are logged by hand from phone, email and WhatsApp, completion is reported by phone, and paper job cards reach the office days later, so the client can neither trust the figure nor prove that a job was on time when a customer deducts a credit. The same missing record leaves about ₦2,600,000 a month of extra work unbilled and lets about 48 planned maintenance visits a week be skipped unnoticed. The problem matters now because the client plans to grow from 80 to 150 technicians within two years, and a process run on phones, spreadsheets and paper does not scale to that size. All figures in this document are estimates from the [engagement brief](../discovery/engagement-brief.md).

## Baseline

| Measure | Current value | Source |
|---|---|---|
| Breakdowns with recorded reported, arrival and completion times | Not measured: arrival and completion times exist only on paper job cards | Engagement brief, current process |
| Breakdowns finished within their resolution SLA | 80% | Client's manual weekly SLA report |
| Service credits paid per month | About ₦8,700,000 | Engagement brief, pain point PP1 |
| Value of parts recorded on jobs, as a share of parts issued from stores | Not measured: about 25% of billable extras are estimated never to be billed | Engagement brief, pain point PP2 |
| Spot-checked breakdowns whose recorded times are confirmed within 30 minutes | Not measured | No spot checks take place today |
| Planned maintenance visits completed within 3 working days of their due date | 92% | Engagement brief, pain point PP3 |

The second measure is the headline. The 80% figure is not reliable, and its error has no known direction: request times typed late move the SLA clock later and make jobs look on time, while completions reported late or not at all make jobs look late. The first four weeks after go-live therefore establish a trusted baseline, and the headline target is set relative to it. The same four weeks confirm the weekly job volume; if it differs materially from about 1,000 work orders, the pain-point costs are recalculated and the change is recorded as a decision.

## Target

| ID | Measure | Target value | By when |
|---|---|---|---|
| T1 | Breakdowns with system-recorded reported, arrival and completion times | 98% or more | Within 8 weeks of go-live |
| T1a | Spot-checked breakdowns whose recorded times are confirmed within 30 minutes | 95% or more | Within 8 weeks of go-live |
| T2 | Breakdowns finished within their resolution SLA, as a four-week average | At least 2 percentage points above the trusted four-week baseline from weeks 1 to 4 | By week 16 after go-live |
| T3 | Service credits paid per month | At least 25% below ₦8,700,000 | By week 16 after go-live |
| T4 | Value of parts recorded on jobs each month, as a share of the value of parts issued from the client's stores | 95% or more, reconciled monthly with the finance team | Within 8 weeks of go-live |
| T5 | Planned maintenance visits completed within 3 working days of their due date | 97% or more | Within 12 weeks of go-live |

T1 comes first because every other measure depends on complete records, and it is the target the system controls most directly. T1a checks that the records are true as well as complete: each week, supervisors check a random 5% of completed breakdowns with the customer contact or on site. T2 compares four-week averages because a weekly figure based on about 400 breakdowns varies by about 2 percentage points by chance alone; a four-week average varies by about 1 point. T2 assumes that deadline warnings prevent about a quarter of real misses, an improvement of about 2.5 to 3 percentage points, and sets the target slightly below that so that a real improvement is not hidden by chance variation. T3 assumes that about half of today's misses are jobs finished on time that the client cannot prove, worth about ₦4,300,000 a month, and that half of the disputes over those credits succeed; it applies where contracts allow credits to be disputed with timestamp evidence. T4 compares parts recorded on jobs with parts issued from stores, because parts that are never recorded cannot be counted from job records alone. T5 is reached when the system creates every planned visit and makes skipped visits visible. All targets apply once a client application built on the API is in use, because staff record work through that application.

## Is AI the right tool?

No. The problem is missing, late and untrusted records, and the lack of a shared view of jobs and deadlines. Rules and reports solve it: the system timestamps each event, sets each job's SLA due times from the contract terms, warns supervisors before a deadline passes, and produces fixed reports. These rules can be explained to a technician or a customer in a dispute, which an artificial intelligence (AI) model's output cannot always be.

Three AI uses were considered and not chosen:

- **Automatic job assignment or route planning:** supervisors' knowledge of skills, sites and traffic is sufficient at this size once they can see workload and deadlines; automatic assignment would also shape decisions about individual technicians.
- **Predicting equipment breakdowns:** this needs equipment sensor or failure history data, which the client does not hold.
- **Classifying request urgency from message text:** coordinators set urgency when logging a request; the contract defines the urgency levels.

Because the system contains no AI, it stays at governance tier 1.

## People who could be harmed

| Who | How they could be harmed if the solution goes wrong |
|---|---|
| Technicians | Recorded as late because of a system error, a lost update or a failed save on a weak mobile connection, and blamed or disciplined for it; feeling watched, or pressured to rush work, including safety-critical electrical work |
| Supervisors | Judged on team figures distorted by recording errors |
| Help-desk coordinators | Blamed for missed SLAs when the clock starts at logging and a request arrived through a channel they could not see |
| Customer facility managers and building occupants | An urgent fault, such as an electrical, lift or generator fault, delayed because a request was lost, logged with the wrong urgency, or the system was unavailable during morning dispatch |
| All staff and customer contacts | Personal data exposed through a security breach |
| The client | Wrong reports leading it to pay credits it does not owe, or to dispute credits it does owe, damaging customer trust |

The table lists the people affected if the system records something wrong, loses data or is unavailable. The requirements and design phases set a control for each harm.

## Not part of this problem

- Travel time across Lagos and technicians who do not attend jobs; the system makes both visible but does not remove them.
- Contract prices, SLA response and resolution times, and service credit rates, which the client sets with its customers.
- Individual performance management of technicians.
- The invoicing process, which stays with the finance team.
