# Design risks

This document lists risks that could make the design fail or cost more than planned, with a response and an owner for each. Risks to people are assessed separately in the [data protection impact assessment](../governance/dpia.md). The project plan builds its risk register from this list.

| ID | Risk | Likelihood | Impact | Response | Owner |
|---|---|---|---|---|---|
| DR-1 | Technicians record arrival and completion late or in batches, so records are complete but not true | High | High | Weekly spot checks (T1a, FR-28); single-request completion and a three-tap client application (NFR-6, CA-1); a monthly mobile-data allowance; training at go-live | Engagement lead |
| DR-2 | The separately built client application is late or misreads the API contract | Medium | High | Published OpenAPI description with examples (FR-30); client application expectations CA-1 to CA-9; the description is checked against the API in CI | Engagement lead |
| DR-3 | The scope is too large for one developer | High | High | The build is divided into small releases, each usable on its own, with timings based on progress | Engagement lead |
| DR-4 | Platform components (Kubernetes, Calico, Flux, CloudNativePG, Envoy Gateway, cert-manager, SOPS) are misconfigured or slow the build | High | Medium | The platform is built locally one component at a time, each verified before the next; runbooks are written alongside | Platform engineer |
| DR-5 | The development machine cannot run the build: 149 MB free on its main drive and 7.6 GB of memory for the Linux environment, measured on 29 September 2026 | High | High | At least 20 GB is freed before the build; the local cluster runs a lean set of components; memory use is measured | Platform engineer |
| DR-6 | Free-tier terms change, or the single pilot virtual machine fails | Medium | Medium | The pilot carries synthetic data only; free-tier terms are checked again before use; the cluster is rebuilt from the repository by Flux and the database restored from backups | Platform engineer |
| DR-7 | The SLA clock calculates wrong due times | Medium | High | A pure module with acceptance and property-based tests (ADR 0009) | Data engineer |
| DR-8 | An account is taken over; multi-factor authentication is not in the first release | Low | High | Passwords of at least 15 characters checked against common passwords, rate-limited login and revocable tokens (ADR 0004); multi-factor authentication for administrators is the first addition | Platform engineer |
| DR-9 | The SOPS age key is lost, so secrets cannot be decrypted | Low | High | The key is backed up outside the repository, with a restore and rotation runbook (ADR 0016) | Platform engineer |
| DR-10 | A chosen tool changes status or does not conform as expected, as happened with the ingress-nginx controller | Medium | Medium | Conformance and maintenance status are confirmed before installation; decisions are changed by superseding ADRs | Platform engineer |
| DR-11 | Production hosting stores real personal data outside Nigeria without a lawful transfer mechanism | Medium | Medium | Addressed in the data protection impact assessment (R8) and decided with production hosting, including an option in Lagos | Governance lead |
| DR-12 | The estimated baseline and job volume differ materially from reality | Medium | Medium | The first four weeks establish a trusted baseline and volume; targets are revisited as a recorded decision | Engagement lead |
| DR-13 | The Idempotency-Key header is not a published standard | Low | Low | The header is documented in the OpenAPI description; the API's behaviour does not depend on the draft | Platform engineer |
| DR-14 | Loss of the pilot virtual machine loses the database | Medium | Medium | Continuous backups outside the cluster (ADR 0003); a restore is tested before go-live | Platform engineer |

DR-1 to DR-5 are the risks most likely to affect the engagement: four are rated high likelihood, and they concern people's habits, a dependency outside the engagement, and the capacity of the developer and the development machine rather than the software design itself. DR-6 to DR-14 are contained by decisions already recorded in the ADRs, tests or runbooks. Owners are the engagement roles defined by the delivery organisation; on a small engagement one person holds several roles.
