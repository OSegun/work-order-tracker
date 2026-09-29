# ADR 0007: Secrets and configuration

## Status
Superseded by ADR 0016

## Context

No secret may appear in source code or git history (NFR-11). The Kubernetes documentation for Secrets states: "Kubernetes Secrets are, by default, stored unencrypted in the API server's underlying data store (etcd). Anyone with API access can retrieve or modify a Secret." It recommends, as a minimum, enabling encryption at rest for Secrets, least-privilege access rules, restricting Secret access to specific containers, and considering external secret stores.

After ADR 0004, the system no longer signs tokens, so the token-signing key (`SECRET_KEY`) is no longer needed. The remaining secrets are the database credentials, used by the API and scheduled tasks; the object storage credentials for backups, used only by the database's backup plugin (ADR 0003); and mail server credentials, only if FR-22 is built. Ordinary settings include the time zone, log level and token lifetime.

## Decision

Secrets are Kubernetes Secrets with encryption at rest enabled and least-privilege access rules. Each Secret is made available only to the containers that need it. Secret values are held in the deployment pipeline's secret store and written into the cluster at deployment; they are never committed to git. In local development they come from a `.env` file that git ignores. Ordinary settings are held in ConfigMaps and passed to the application as environment variables, and the application reads and validates all settings at startup with `pydantic-settings`, stopping with a clear error if any required setting is missing or invalid.

## Alternatives considered

| Option | Advantages | Disadvantages |
|---|---|---|
| Kubernetes Secrets with encryption at rest, least privilege and values supplied by the pipeline (chosen) | Meets the minimum steps in the Kubernetes documentation without new tools | Secret values are managed outside git, so each environment's values are set up and rotated through the pipeline |
| Secrets encrypted with SOPS and age keys and committed to git | All configuration in git, which suits deployments where the cluster pulls its state from git; SOPS is a Cloud Native Computing Foundation (CNCF) Sandbox project | The private age key becomes a critical secret to protect and rotate |
| External Secrets Operator with a cloud secret manager | Central management and audit of secrets | Requires a cloud account, may cost money, and ties the design to one provider |
| Vault or OpenBao inside the cluster | Full secrets management features | Another stateful service to run and back up for three secrets |

The chosen option applies the documented minimum protections with the fewest components. If the deployment approach in ADR 0013 has the cluster pull its state from git, SOPS is reconsidered and this ADR is superseded.

## Consequences

- `SECRET_KEY`, the code that reads it and its entry in `.env.example` are removed with the JSON Web Token code.
- `.env.example` lists every setting with safe example values, including the database address.
- `pydantic-settings` is added as a dependency; whether reading `.env` files needs `python-dotenv` as well is checked when it is added.
- Encryption at rest is enabled on the local cluster; for a hosted cluster, whether it is enabled by default is confirmed in the hosting ADR.
- Access rules allow the API and scheduled tasks to read only the database credentials, and the database to read only the backup storage credentials.
- A secret rotation procedure is written as a runbook during monitoring and operations.
