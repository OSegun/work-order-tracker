# ADR 0009: SLA clock as a pure, stored-result module

## Status
Accepted

## Context

Every target, report and dispute depends on correct service level agreement (SLA) due times (FR-5, FR-13, FR-15, FR-19, FR-26, FR-29). Urgent breakdowns are measured in clock hours; other urgency levels in working hours, 07:00 to 19:00 West Africa Time (WAT), Monday to Saturday, excluding public holidays. Confirmed customer-caused holds extend the due time by their length; holds for the client's own reasons do not. A holiday added after a job is logged changes that job's due time. Times are stored in Coordinated Universal Time (UTC) (NFR-8). The Africa/Lagos time zone has an offset of one hour from UTC throughout the year, checked with Python's `zoneinfo` for every month of 2026.

An error in this calculation produces wrong compliance figures and wrong service credits, and can lead to staff being blamed for late jobs that were on time, which the problem statement names as a harm.

## Decision

The SLA clock is a self-contained Python module with no database or web framework imports. It receives the current time as a parameter rather than reading the system clock. It calculates response and resolution due times from the reported time, the contract's SLA times, the urgency level, confirmed customer-caused holds and the working calendar, using Python's built-in `zoneinfo` for the Africa/Lagos time zone. Due times are calculated when an event occurs (a job is reported, a hold is confirmed, the calendar changes), stored on the job and recorded in its history. The module is tested with example tests for AC-1 to AC-3 and with property-based tests using the Hypothesis library.

## Alternatives considered

| Option | Advantages | Disadvantages |
|---|---|---|
| Pure module, results stored at events, example and property-based tests (chosen) | Rules readable in one place; fast, isolated tests; deadline lists and reports query stored values; past deadlines stay as they were, with every change recorded | Stored due times must be recalculated whenever a hold is confirmed or the calendar changes |
| Calculation inside the database as SQL functions | Close to the data | Harder to read and test; ties the rules to PostgreSQL |
| Calculation at read time, never stored | No stored values to keep up to date | Slower lists and reports; past deadlines change silently when the calendar changes |
| A third-party business-hours package | Less code to write | A dependency at the centre of the product, with rules not fully under the engagement's control |

The chosen option keeps the most important rules small, explicit and exhaustively tested.

## Consequences

- An SLA clock module and a working calendar data structure are added; the work-orders module calls the SLA clock and never calculates due times itself.
- Hypothesis is added as a test-only dependency. Properties tested include: a due time is never earlier than the reported time; adding a working duration and then measuring the working time between start and due time returns the same duration; a non-urgent due time never falls outside working hours.
- A job reported outside working hours with a non-urgent level starts its clock at the next working opening.
- When the calendar changes, the due times of affected open jobs are recalculated and each recalculation is recorded in the job's history (FR-26).
- The module works in UTC and converts to Africa/Lagos only for calendar rules, so it does not depend on the absence of daylight saving time.
