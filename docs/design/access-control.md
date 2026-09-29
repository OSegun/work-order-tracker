# Access control

This document states which role may perform each action, and how the API enforces it. It implements FR-1, NFR-10 and GR-4 of the [requirements](../requirements/requirements.md); the approach is recorded in [ADR 0005](../adr/0005-authorisation-policy-module.md).

## Roles

| Role | Held by |
|---|---|
| Administrator | Operations manager; includes every manager permission |
| Manager | Managing director |
| Coordinator | Help-desk coordinators |
| Supervisor | Supervisors |
| Technician | Technicians |
| Finance | Finance team |

Each account has exactly one role (FR-1). The administrator role includes the manager role's permissions, so that the operations manager can administer the system and read its reports with one account.

## Matrix

**All** means every record; **Team** means the technicians a supervisor supervises and their jobs; **Own** means records assigned to the user; **No** means the request is refused.

| Action | Administrator | Manager | Coordinator | Supervisor | Technician | Finance |
|---|---|---|---|---|---|---|
| Manage staff accounts and reset passwords | All | No | No | No | No | No |
| Change own password; read and acknowledge the privacy notice | Own | Own | Own | Own | Own | Own |
| Edit customers, buildings and customer contacts | All | No | All | No | No | No |
| Edit contract and SLA terms | All | No | No | No | No | No |
| Read contract terms | All | All | All | All | No | All |
| Maintain the working calendar and public holidays | All | No | No | No | No | No |
| Log a breakdown | No | No | All | All | No | No |
| Cancel a job before arrival | No | No | All | Team | No | No |
| View jobs | All | All | All | All | Own | No |
| Read a job's customer contact | All | All | All | All | Own | No |
| Assign or reassign a job | No | No | No | Team | No | No |
| Record arrived, on hold, completed and parts used | No | No | No | No | Own | No |
| Confirm a customer-caused hold longer than 1 hour | No | No | No | Team | No | No |
| Verify or reopen a completed job | No | No | No | Team | No | No |
| Correct a recorded time or status | No | No | No | Team | No | No |
| Approve a correction that changes a missed SLA to a met one | All | All | No | No | No | No |
| Record spot-check results | No | No | No | Team | No | No |
| Manage planned maintenance schedules | All | No | No | All | No | No |
| Read SLA, record completeness and planned maintenance reports | All | All | No | All | No | No |
| Download the billable-extras CSV | All | All | No | No | No | All |
| Find, export, correct and restrict one person's data (GR-2) | All | No | No | No | No | No |
| Read audit logs | All | No | No | No | No | No |

Changes to accounts, the working calendar and contract terms alter every SLA figure, so they are limited to the administrator. Coordinators log and maintain requests but do not assign work. Supervisors can see all jobs, so that they can cover absences, but act only on their own team. Technicians see and act only on their own jobs. A correction that turns a missed SLA into a met one is approved by a manager or administrator, never by the supervisor who made it. The finance team sees contract terms and billable extras only.

## Enforcement

1. **One policy module.** A single function decides whether a user may perform an action on a record. Every endpoint declares its action through a FastAPI dependency that calls this function.
2. **Scope inside queries.** Records outside a user's scope are excluded by the database query itself, for example "jobs where the assigned technician is the current user", so they are never loaded.
3. **Deny by default.** An automated test lists every endpoint in the application and fails if any endpoint has no declared action.
4. **Response codes.** A role that may never perform an action receives 403 (forbidden). A record outside the user's scope returns 404 (not found), so its existence is not revealed (AC-10). A move that the job's current state does not allow returns 409 (conflict).
