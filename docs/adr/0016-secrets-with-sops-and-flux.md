# ADR 0016: Secrets encrypted with SOPS and decrypted by Flux

## Status
Accepted. Supersedes ADR 0007.

## Context

ADR 0007 stored secret values in the deployment pipeline and stated that SOPS would be reconsidered if the cluster pulled its state from git. ADR 0013 adopts Flux, which applies the cluster's state from the repository, so secrets must reach the cluster through the repository. SOPS is a Cloud Native Computing Foundation (CNCF) Sandbox project that encrypts the values in a file while leaving its structure readable, and supports age keys; Flux documents decrypting SOPS-encrypted secrets. The Kubernetes guidance from ADR 0007 still applies: Secrets are stored unencrypted by default, and should be protected with encryption at rest and least-privilege access.

## Decision

Secret values are stored in the repository only in files encrypted with SOPS using an age key. Flux holds the private age key inside the cluster and decrypts the files when it applies them. The private age key is never committed; it is backed up securely outside the repository. Everything else in ADR 0007 remains: encryption at rest for Kubernetes Secrets, least-privilege access, each Secret available only to the containers that need it, `SECRET_KEY` retired, and `pydantic-settings` for configuration.

## Alternatives considered

| Option | Advantages | Disadvantages |
|---|---|---|
| SOPS with age, decrypted by Flux (chosen) | All cluster state, including secrets, is versioned in git; works for local and hosted clusters | The private age key becomes the single critical secret to protect, back up and rotate |
| Secret values held in the pipeline (ADR 0007) | Secrets never enter git, even encrypted | Does not fit delivery where the cluster pulls its state from git |
| Sealed secrets encrypted by an in-cluster controller | Encrypted files in git without a separate key tool | Encrypted files are tied to one cluster's controller key |
| External Secrets Operator with a cloud secret manager | Central management | Requires a cloud account and may cost money |

## Consequences

- A `.sops.yaml` file defines which files are encrypted and with which public age key.
- Unencrypted secret files are listed in `.gitignore`; a pre-commit or CI check rejects unencrypted secrets.
- A runbook covers backing up, restoring and rotating the age key, and re-encrypting files after rotation.
- The secret scan in CI (ADR 0013) treats any unencrypted secret value in the repository as a failure.
