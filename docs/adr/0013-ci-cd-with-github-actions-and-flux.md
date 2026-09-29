# ADR 0013: CI with GitHub Actions and GitOps delivery with Flux

## Status
Accepted

## Context

Every change must pass formatting, linting, type checks and tests with at least 80% line coverage (NFR-14), secret and dependency scans (NFR-11), and a check that the published OpenAPI description matches the API (FR-30). Tests run against PostgreSQL (ADR 0002). Migrations run once before new API pods start (ADR 0011). The main branch changes only through reviewed pull requests with passing checks (engineering standards). The monthly infrastructure budget is zero (NFR-13), and the repository is public.

The cluster runs on a developer's machine during development and may run on a hosted cluster later. GitHub's hosted runners cannot reach a cluster on a developer's machine.

GitHub's billing documentation states that "GitHub Actions usage is free for self-hosted runners and for public repositories that use standard GitHub-hosted runners" and that "GitHub Packages usage is free for public packages". Flux describes itself as an "Open and extensible continuous delivery solution for Kubernetes", is listed as a Cloud Native Computing Foundation (CNCF) Graduated project, and documents decrypting secrets encrypted with SOPS.

## Decision

**Continuous integration.** GitHub Actions runs on every pull request: Ruff, mypy, tests against a temporary PostgreSQL container with coverage of at least 80%, a secret scan, a dependency vulnerability scan, a check of the OpenAPI description, and a container image build with an image scan. On merge to main, the image is pushed to the GitHub Container Registry, tagged with the commit identifier; no floating `latest` tag is used.

**Continuous delivery.** Flux runs inside the cluster and applies the state held in the repository. A release is a reviewed pull request that changes the image tag in the Kubernetes files. Flux applies the migration Job before updating the API pods.

**Packaging.** The application's Kubernetes files use Kustomize, with a base and overlays for local and production settings. CloudNativePG, Envoy Gateway and cert-manager are installed by Flux from their Helm charts.

## Alternatives considered

| Option | Advantages | Disadvantages |
|---|---|---|
| GitHub Actions for integration and Flux for GitOps delivery (chosen) | Works for a cluster that GitHub cannot reach; GitHub holds no cluster credentials; every deployment is a reviewed commit | Flux is another component in the cluster; releases need a pull request that changes the image tag |
| GitHub Actions deploying directly to the cluster | One tool | Requires the cluster to be reachable from GitHub and GitHub to hold cluster credentials |
| Argo CD for GitOps delivery | Visual dashboard of cluster state | Heavier than Flux for one application; secret decryption needs extra components |
| Helm for the application's own manifests | Templating and packaging | More indirection than Kustomize overlays need for two environments |

## Consequences

- Workflow files for pull requests and for merges to main are added under `.github/workflows/`.
- The tools for the secret, dependency and image scans are chosen and verified when the workflows are written.
- Kubernetes files are organised as a Kustomize base with `local` and `production` overlays, plus Flux resources that install third-party components.
- The Flux setting that makes the application wait for the migration Job to succeed is confirmed during the build.
- Branch protection on main is enabled in the repository settings.
- Secret handling changes to SOPS-encrypted files decrypted by Flux, recorded in ADR 0016, which supersedes ADR 0007.
