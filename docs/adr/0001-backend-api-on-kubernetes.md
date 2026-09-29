# ADR 0001: Backend API as one service on Kubernetes

## Status
Accepted

## Context

The work-order tracker must record jobs, calculate service level agreement (SLA) due times, enforce who may do what, keep a full history of changes and produce weekly and monthly reports ([requirements](../requirements/requirements.md)). The expected load is small: about 3 requests per second at the morning peak today, and 18 requests per second at the designed peak (NFR-1). Completing a job must change the job, its history and its SLA status together or not at all.

The engagement delivers the backend only. Staff use the system through a web or mobile client application that another developer builds against the application programming interface (API) contract (FR-30). The system is operated after handover by an external system support provider, which runs several clients' systems and needs one standard way to deploy and operate them. The engagement has a monthly infrastructure budget of zero (NFR-13).

## Decision

The backend is one FastAPI application, organised internally into modules (accounts and access; customers, buildings and contracts; work orders; SLA clock and working calendar; planned maintenance; reports; governance), deployed on Kubernetes as two services: the API service and the database service. Scheduled tasks run as Kubernetes CronJobs using the same container image as the API.

## Alternatives considered

| Option | Advantages | Disadvantages |
|---|---|---|
| One API service and a database service on Kubernetes (chosen) | One database transaction updates a job, its history and its SLA status together; one code base to test and release; Kubernetes gives the support provider a standard way to deploy, restart and update the system | Module boundaries inside the application must be kept deliberately; Kubernetes adds container and cluster work compared with a single server |
| Core service plus separate reporting and notification services | Reporting and email isolated from job updates | Events and two more services to build and operate; not needed at this load |
| Full microservices, one service per area | Each area deployed independently | Updating a job and its history across services needs distributed transaction patterns; many services for one developer and one support provider |
| Server-rendered web pages in the same application | Users get screens without a separate client application | Outside the engagement's scope; the client application is built separately |
| Serverless functions | No servers to manage | Start-up delays at the morning peak; harder shared transactions; tied to one provider |

The chosen option keeps the transactional core in one place, which the lifecycle rules require, and uses Kubernetes for deployment and operation rather than for splitting the software. Splitting into more services was rejected because the load is small and the areas that share transactions would have to be kept consistent across a network.

## Consequences

- A job update, its history entry and its SLA status are saved in one database transaction.
- The existing server-rendered pages (`templates/`, `static/`) and their dependencies are removed; the routers return JSON only.
- The OpenAPI description published by FastAPI becomes the contract for the client application and must be kept accurate (FR-30).
- Container images, Kubernetes manifests, health checks and CronJobs must be built and tested; a local cluster is used during development.
- Running the database inside Kubernetes makes backups, upgrades and restores (NFR-12) the responsibility of the engagement and the support provider; the database engine and its operation are decided in ADR 0002.
- Where the cluster is hosted, and its cost, is decided in a later ADR, with a cost estimate as NFR-13 requires.
- Module boundaries are enforced by rule: only the work-orders module changes job status, and the reports module only reads data.
