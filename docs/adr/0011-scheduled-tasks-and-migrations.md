# ADR 0011: Scheduled tasks as CronJobs and migrations as a single Job

## Status
Accepted

## Context

Some work runs without a user: creating planned work orders (FR-14), selecting weekly spot checks (FR-28), applying retention (GR-3), and removing expired idempotency, session and failed-login records (ADR 0004, ADR 0010). The Kubernetes documentation for CronJobs states: "CronJobs may create more than one Job or none. Jobs should be idempotent." The CronJob API reference describes the `timeZone` field as "The time zone name for the given schedule"; if it is not set, the schedule follows the time zone of the cluster's controller manager.

Database structure changes are made with Alembic. During a rolling update, old and new API pods run at the same time, and several new pods start together. The current code also creates tables at startup with `create_all` in `main.py` and `routers/auth.py`, outside Alembic.

## Decision

**Scheduled tasks.** Four Kubernetes CronJobs run commands from the API's container image, with `timeZone: Africa/Lagos`, `concurrencyPolicy: Forbid`, a starting deadline of one hour and the default history limits:

| Task | Schedule (West Africa Time) | Why a repeated run is safe |
|---|---|---|
| Create planned work orders | Daily at 05:00 | A unique rule on schedule and due date prevents a second work order for the same visit |
| Select weekly spot checks | Monday at 06:00 | The selection is recorded per week; a repeated run finds the week already selected |
| Apply retention | Daily at 02:00 | Records already processed no longer meet the selection criteria |
| Remove expired idempotency, session and failed-login records | Hourly | Deleting records that are already gone has no effect |

Reports and deadline lists are calculated when requested, from stored data. Backups are scheduled by CloudNativePG (ADR 0003).

**Migrations.** Before each release, the deployment pipeline runs one Kubernetes Job that applies `alembic upgrade head`, and starts the new API pods only if the Job succeeds. Every migration follows an expand-then-contract rule: a release adds new structures without removing ones that running code uses, and removal happens in a later release once no older pods remain. Alembic is the only way the database structure changes.

## Alternatives considered

| Option | Advantages | Disadvantages |
|---|---|---|
| CronJobs from the API image, and one migration Job before rollout (chosen) | Tasks share the API's code and SLA clock; migrations run once per release, and a failure stops the release | The pipeline must order the migration Job before the rollout |
| A scheduler library running inside the API pods | No Kubernetes scheduling resources | With two or more pods, each would run every task unless a leader is elected |
| Pre-calculated reports on a schedule | Faster report requests | More moving parts and stale figures; unnecessary at this data volume |
| Migrations in an init container of every API pod, or at application startup | Automatic | Several pods migrate at once and race; startup migration bypasses Alembic's history |
| A Helm pre-upgrade hook for migrations | The same single run, automated by Helm | Depends on Helm being chosen for packaging in ADR 0013 |

## Consequences

- A task entry point is added to the application, for example `python -m app.tasks create-planned-jobs`, with one command per task.
- A unique rule on planned work orders (schedule and due date) is added to the database.
- The `create_all` calls in `main.py` and `routers/auth.py` are removed; the existing migration's empty `downgrade()` is completed; `alembic.ini` reads the database address from configuration (ADR 0007).
- Reviews of each migration check that it keeps older pods working until the contract step.
- If ADR 0013 packages the system with Helm, the migration Job may run as a pre-upgrade hook with the same behaviour.
