# ADR 0005: Authorisation through one policy module

## Status
Accepted

## Context

Six roles share the API, and most actions depend on scope as well as role: technicians act only on their own jobs, and supervisors act only on their own team (FR-1, NFR-10). Job moves also depend on the job's current state (FR-10). A record outside a user's scope must be reported as not found (AC-10). The current code checks permissions separately in each endpoint, and one page loads a job by its identifier without checking its owner (`routers/todos.py`, the edit page).

## Decision

Authorisation is enforced in three layers: role, scope and state. One policy module decides role and scope for every endpoint through a FastAPI dependency; scope is applied inside database queries; state is enforced by the job lifecycle in the work-orders module. A test fails if any endpoint lacks a declared action. The full matrix is in [access control](../design/access-control.md).

## Alternatives considered

| Option | Advantages | Disadvantages |
|---|---|---|
| One policy module, scoping in queries and a deny-by-default test (chosen) | One place to read and test every rule; records outside scope are never loaded; a new endpoint cannot be left unprotected | Every endpoint must use the shared dependency, which the test enforces |
| Checks written inside each endpoint | Simple for a few endpoints | Easy to forget one check, as the current edit page shows; rules spread across the code |
| A general policy engine with rules in a separate policy language | Powerful and auditable for large rule sets | A new language and dependency for 6 roles and about 20 actions |

The chosen option gives one reviewable place for the rules and removes the most common authorisation fault, loading a record by identifier without checking scope.

## Consequences

- A policy module and a shared FastAPI dependency are added; every endpoint declares its action.
- List and detail queries take the current user's scope as a parameter.
- An automated test enumerates all endpoints and asserts that each declares an action; further tests call every endpoint as every role (NFR-10).
- Responses use 403 for a forbidden role, 404 for a record outside scope and 409 for a move the job's state does not allow.
- The administrator role includes all manager permissions, so the operations manager needs one account.
