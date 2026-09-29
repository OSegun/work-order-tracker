# ADR 0012: Structured logs, Prometheus metrics and separate health checks

## Status
Accepted

## Context

The system must show whether it meets NFR-1 (response times and failure rate), reveal scheduled tasks that stop running (ADR 0011), and allow a single request to be traced when a user reports a problem. Logs contain personal data (data inventory D-8) and must never contain passwords or tokens (GR-4).

The Prometheus documentation states that Prometheus "joined the Cloud Native Computing Foundation in 2016 as the second hosted project, after Kubernetes", and that "If you need 100% accuracy, such as for per-request billing, Prometheus is not a good choice". The Kubernetes documentation on probes states that "Incorrect implementation of liveness probes can lead to cascading failures" and advises that "The liveness probe passes when the app itself is healthy, but the readiness probe additionally checks that each required back-end service is available."

## Decision

**Logs.** The API and scheduled tasks write one JSON line per event to standard output, using Python's `logging` module with a JSON formatter. Request logs contain the time in Coordinated Universal Time (UTC), level, request ID, user ID and role, method and route, status and duration. The request ID is returned to the client in a response header. Passwords, tokens, job-note text, names, phone numbers and email addresses are never logged.

**Metrics.** The API exposes Prometheus metrics with `prometheus-client` on a separate internal port that the Gateway does not route to: request count and duration by route and status, login attempts and failures, version conflicts and idempotent replays, database connection-pool use, and the last successful run time of each scheduled task, which each task records in the database. Service level agreement (SLA) compliance, service credits and billable extras are always reported from the database, never from metrics.

**Health checks.** `/health/live` confirms only that the application process responds and never checks the database. `/health/ready` also runs a quick database query. A startup probe uses the liveness endpoint with a longer allowance during start-up.

**Storage of logs and metrics.** Where logs and metrics are stored, viewed and alerted on is decided with hosting and during monitoring and operations, including the resources available and any transfer of personal data outside Nigeria.

## Alternatives considered

| Option | Advantages | Disadvantages |
|---|---|---|
| JSON logs, `prometheus-client` metrics and separate probes (chosen) | Standard formats collected by common tools; one small dependency; probes that do not restart pods during a database interruption | Traces across services are not available, which one service does not need |
| OpenTelemetry instrumentation for logs, metrics and traces | Vendor-neutral and ready for several services | More packages and configuration than one service needs |
| Plain-text logs and no metrics | Nothing to add | Performance requirements cannot be measured, and requests cannot be followed |
| A liveness probe that also checks the database | One endpoint | A short database interruption restarts every API pod at once |

## Consequences

- A JSON log formatter and request-ID middleware are added; tests confirm that secrets and contact details do not appear in logs.
- `prometheus-client` is added as a dependency; metrics are served on an internal port.
- A table records the last successful run of each scheduled task.
- ADR 0008 gains one allowed connection: from the monitoring system to the API's metrics port.
- OpenTelemetry is reconsidered if the backend is ever split into several services.
