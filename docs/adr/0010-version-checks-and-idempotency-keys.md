# ADR 0010: Version checks and idempotency keys

## Status
Accepted

## Context

Two people can change the same job at the same time; without protection, the later save silently overwrites the earlier one (FR-18, AC-5). Technicians work on weak mobile data, so the client application retries requests whose replies were lost; without protection, a retried completion is applied twice or produces a confusing error (FR-8, NFR-5, AC-6). Completing a job must be recorded once, with the server's time of first receipt as the completion time.

HTTP already defines the mechanism for the first problem. RFC 9110 describes an entity tag (ETag) as "an opaque validator for differentiating between multiple representations of the same resource", and the If-Match header as making "the request conditional on the recipient having at least one current representation of the target resource" whose entity tag matches. When the condition fails, the server answers 412 (Precondition Failed). RFC 6585 defines 428 (Precondition Required) and states that "Its typical use is to avoid the 'lost update' problem".

For the second problem, the IETF document "The Idempotency-Key HTTP Header Field" describes a header that "can be used to make non-idempotent HTTP methods such as POST or PATCH fault-tolerant". Its latest version, draft 07 of 15 October 2025, is listed as an expired Internet-Draft, so it is not a published standard; the header is agreed between the API and the client application through the OpenAPI description (FR-30).

## Decision

**Version checks.** Every job carries a version number that increases by one on every change. The API returns it in the ETag header of each job response. Requests that change a job must send it back in the If-Match header. The update and the version check happen in one database statement ("update the job where its version is still the one sent"). If the job has changed since it was read, the API answers 412 (Precondition Failed) with the message "This job was changed by another user; reload to see the latest version". A change request without If-Match is refused with 428 (Precondition Required).

**Idempotency keys.** Every request that changes data carries an `Idempotency-Key` header with a unique value created by the client application. The first request with a key is processed, and the key, a fingerprint of the request and the reply are stored in the same database transaction as the change. A later request with the same key and the same fingerprint receives the stored reply without the change being repeated. A request with a key whose first request is still being processed receives 409 (Conflict). A request that reuses a key with a different fingerprint receives 422 (Unprocessable Content). Stored keys and replies are deleted after 24 hours.

The idempotency check runs before the version check, so a retry of a request that has already succeeded receives its original reply rather than a version mismatch.

## Alternatives considered

| Option | Advantages | Disadvantages |
|---|---|---|
| Version checks with ETag and If-Match, and stored idempotency keys (chosen) | No silent overwrites; retries are safe; standard HTTP headers the client application can use | The client application must send If-Match and an idempotency key; a table of keys must be kept and cleaned |
| Last write wins (current behaviour) | Nothing to build | Changes are lost without notice |
| Locking a job while a user has it open | Conflicts cannot occur | Locks cannot be held safely between separate web requests; an abandoned session blocks everyone |
| Merging concurrent changes field by field | Fewer refused saves | Complex, and surprising when two people change the same field |
| Relying on the client application not to retry twice | Nothing to build on the server | Weak networks make duplicate requests certain; the server cannot depend on the client |

The chosen option prevents both silent overwrites and duplicate actions at the server, which the client application cannot guarantee on its own.

## Consequences

- Jobs gain a version column; update statements include the expected version and report whether a row changed.
- An idempotency table stores user, key, request fingerprint, reply status and body, state and creation time, with a unique constraint on user and key.
- A scheduled task deletes idempotency records older than 24 hours; the data inventory records them as containing personal data with a 24-hour retention period.
- The OpenAPI description (FR-30) documents the ETag, If-Match and Idempotency-Key headers and the 409, 412, 422 and 428 responses; the client application expectations (CA-2) use the same key on every retry.
- AC-5 is verified by expecting a 412 response.
