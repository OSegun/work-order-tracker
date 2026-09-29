# ADR 0004: Authentication with stored access tokens and Argon2id passwords

## Status
Accepted

## Context

Staff log in through the client application, usually once per 8-hour shift (NFR-9). A deactivated account or revoked token must be refused on its next request (FR-25), so every request needs a current view of the account in the database. The API runs as two or more pods (ADR 0001), so any shared state, such as failed-login counts, must be held outside a single pod.

The current code issues JSON Web Tokens (JWTs) with `python-jose`, hashes passwords with `passlib`, pins `bcrypt` to version 4.0.1, and accepts passwords of 3 characters. The latest release of `passlib` is 1.7.4, published on 8 October 2020.

NIST Special Publication 800-63B-4, section 3.1.1.2 "Password Verifiers", requires passwords used as a single factor "to be a minimum of 15 characters in length", recommends permitting "a maximum password length of at least 64 characters", forbids composition rules and periodic forced changes, and requires comparison against "a blocklist that contains known commonly used, expected, or compromised passwords". The OWASP Password Storage Cheat Sheet recommends: "Use Argon2id with a minimum configuration of 19 MiB of memory, an iteration count of 2, and 1 degree of parallelism", and notes that bcrypt accepts at most 72 bytes of input in most implementations.

## Decision

At login, the API issues a random access token (32 bytes from a cryptographically secure generator) and stores only a hash of it, with the user, issue time and an expiry of 8 hours. Every request presents the token in the Authorization header; the API refuses it if it is unknown, expired or revoked, or if the user is deactivated. Tokens are revoked on logout, deactivation and password reset. Failed-login counts are stored in PostgreSQL.

Passwords are 15 to 64 characters, are checked against a bundled list of common passwords, carry no composition rules and are never subject to forced periodic change. They are hashed with Argon2id through the `pwdlib` library, with at least the OWASP minimum parameters. Password hashing runs in FastAPI's worker thread pool so that it does not block other requests.

## Alternatives considered

| Option | Advantages | Disadvantages |
|---|---|---|
| Random tokens stored as hashes in PostgreSQL (chosen) | Immediate revocation; no signing keys to manage; no JWT library | One indexed database lookup per request, which is small at the designed load |
| JWT with a database check on every request | Familiar from the current code | The database check removes the benefit of a self-contained token while keeping signing-key handling and library risks |
| Short-lived JWT with refresh tokens | Common in mobile applications | A deactivated user keeps access until the short token expires, which does not meet FR-25; more moving parts |
| Separate identity server, such as Keycloak | Standard protocols, single sign-on and built-in multi-factor authentication | A third stateful service, outside the two-service architecture of ADR 0001; heavy for about 100 users |

Stored random tokens meet FR-25 directly with the least machinery. For password hashing, Argon2id through `pwdlib` replaces an unmaintained library and avoids bcrypt's 72-byte input limit, which a 64-character password with non-English characters can exceed.

## Consequences

- `python-jose`, `passlib` and the `bcrypt` pin are removed from `requirements.txt`; `pwdlib` with Argon2 support is added.
- A sessions table stores token hashes, expiry and revocation; a failed-login table supports rate limiting across pods.
- Existing password hashes in development data are not carried over; development and test data are regenerated (data inventory, D-10).
- A bundled list of common passwords is added to the repository, with its source and licence recorded.
- Multi-factor authentication is not part of the first release. This is recorded as a design risk; administrator accounts are the first candidates if it is added.
- The login endpoint is a synchronous function, so that password hashing runs in the thread pool.
