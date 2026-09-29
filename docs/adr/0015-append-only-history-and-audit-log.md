# ADR 0015: Append-only job history and audit log

## Status
Accepted

## Context

The job history is the evidence for disputes over service credits (PP1, failure point P8), for fair corrections (FR-11) and for verification (FR-23). Every change to a job must be recorded with who made it, when and why (FR-12). Administrator actions and personal-data exports must also be recorded (GR-4). History that can be edited proves nothing. Retention requires staff identities in job history to be pseudonymised after 2 years and records deleted after 6 years (GR-3).

The PostgreSQL documentation lists the privileges that can be granted on a table, including "SELECT, INSERT, UPDATE, DELETE, TRUNCATE", which are assigned with GRANT and removed with REVOKE.

## Decision

Every change to a job writes a row to a job history table in the same database transaction as the change. Each row holds the job, a sequence number, the server time, the phone time where sent, the acting user and role, the business action, the fields changed with their values before and after, the reason where required, and the request ID.

Administrator actions and personal-data exports write rows to a separate audit log table in the same way. The audit log is kept for 2 years and then deleted.

Three database roles are used. The application role, used by the API and most scheduled tasks, may only read and insert rows in the history and audit tables. The retention role, used only by the retention task, may update the person columns of those tables for pseudonymisation and delete rows at the end of their retention period. The migration role, used only by the migration Job, changes table structure. A test fails if any function that changes a job does not write a history row.

## Alternatives considered

| Option | Advantages | Disadvantages |
|---|---|---|
| History written by the application in the same transaction, protected by database privileges (chosen) | Records business actions and reasons; a change cannot be saved without its history; the database refuses edits and deletions by the application | The application must write history for every change, which a test enforces |
| Database triggers that write history automatically | Cannot be forgotten | Record column changes only, without the business action, actor or reason |
| Event sourcing, rebuilding each job's state from its events | Complete history by design | Changes how the whole system stores data; far beyond the system's needs |
| A versioning library that copies whole rows | Little code to write | A new dependency that records rows rather than business actions and reasons |
| A PostgreSQL statement-audit extension | Records database activity for security audits | Designed for query auditing, not history that users read |

## Consequences

- A job history table and an audit log table are created, each with a sequence or ordering column so that missing rows can be detected.
- Separate database credentials exist for the application, retention and migration roles; each is stored as its own Secret and given only to the workload that uses it (ADR 0016).
- GR-3 and the data inventory record a retention period of 2 years for the audit log.
- Pseudonymisation replaces person identifiers in history rows with codes and does not change the recorded times, actions or values.
