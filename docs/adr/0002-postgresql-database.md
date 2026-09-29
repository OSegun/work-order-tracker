# ADR 0002: PostgreSQL as the database

## Status
Accepted

## Context

ADR 0001 places the database in its own service inside Kubernetes, used by two or more API pods and by scheduled tasks. The database must accept many simultaneous writes at the morning peak without lost updates or locking errors (NFR-3), store every time as an instant in Coordinated Universal Time (UTC) for the service level agreement (SLA) clock (NFR-8), support backups and restores (NFR-12), and apply schema migrations with Alembic, which the code base already uses.

The current code uses SQLite. SQLite is a library that reads and writes a file inside the application's own process, and its documentation, under "Situations Where A Client/Server RDBMS May Work Better", states that "it will only allow one writer at any instant in time."

## Decision

The system uses PostgreSQL as its only database, running as the database service inside Kubernetes.

## Alternatives considered

| Option | Advantages | Disadvantages |
|---|---|---|
| PostgreSQL (chosen) | Runs as a separate server; locks at row level, so updates to different jobs do not block each other; stores timestamps with time zone; schema changes run inside transactions, so a failed migration is undone; the PostgreSQL driver is already listed in `requirements.txt` | Database operation, including backups and upgrades, must be designed and run |
| MySQL or MariaDB | Runs as a separate server; handles simultaneous writes | No advantage over PostgreSQL for these requirements; time zone handling fits the SLA clock less directly |
| SQLite | No server to run; already used by the current code | Cannot run as a separate service; each API pod would hold its own file; one writer at a time |

PostgreSQL meets every database-related requirement and fits the separate database service that ADR 0001 requires. SQLite was rejected because it cannot be shared by several API pods.

## Consequences

- The SQLite database files and SQLite-specific settings (such as `check_same_thread`) are removed from the code; the connection address comes from configuration.
- Tests run against PostgreSQL, so that they exercise the same locking and time behaviour as production.
- Unused database drivers (`PyMySQL`) are removed from `requirements.txt`.
- Times are stored in columns of type "timestamp with time zone".
- How PostgreSQL runs inside Kubernetes, and where its backups are stored, is decided in ADR 0003.
