# ADR 0014: Hosting, region and cost

## Status
Accepted

## Context

The system runs on Kubernetes (ADR 0001) with network policies that must be enforced (ADR 0008), backups stored outside the cluster (ADR 0003), and a monthly infrastructure cost of zero during the engagement (NFR-13). Availability is measured during a pilot, and the production recommendation states the hosting and cost needed for 99.5% (NFR-7). Personal data sent outside Nigeria is subject to section 41 of the Nigeria Data Protection Act 2023. The engagement uses synthetic data only.

The development machine provides 7.6 GB of memory and 8 processor cores to the Linux environment, checked on 29 September 2026. The kind documentation describes kind as "a tool for running local Kubernetes clusters using Docker container 'nodes'", and states that its default network plugin can be disabled and that "many common CNI manifests are known to work, e.g. Calico"; it does not state whether the default plugin enforces network policies.

Oracle Cloud's "Always Free Resources" page, checked on 29 September 2026, lists Ampere A1 compute equivalent to 2 OCPUs and 12 GB of memory, 20 GB of Object Storage and 200 GB of block storage for Always Free tenancies, created in the tenancy's home region; its managed Kubernetes service is not listed. Oracle's regions in Africa are Casablanca and Johannesburg; none is in Nigeria.

## Decision

Three environments are used:

| Environment | Hosting | Cost | Data |
|---|---|---|---|
| Local | kind on the development machine, with its default network plugin replaced by Calico | Nothing | Synthetic |
| Pilot | One Oracle Cloud Always Free Ampere A1 virtual machine running k3s in the Johannesburg region; backups to Oracle Object Storage in the same region; certificates from cert-manager's private certificate authority, with no registered domain | Nothing | Synthetic |
| Production | A multi-node cluster with a database replica and a registered domain, recommended and costed during deployment, including an option to keep data in Nigeria | Paid, estimated during deployment | Real |

## Alternatives considered

| Option | Advantages | Disadvantages |
|---|---|---|
| kind with Calico locally, and an Oracle Always Free virtual machine with k3s as the pilot (chosen) | No cost; standard Kubernetes locally; network policies enforced; a hosted pilot for measuring availability | The pilot is a single virtual machine and a single point of failure; free tiers can change |
| k3d locally | Lighter than kind | Runs a Kubernetes distribution that differs more from most hosted clusters |
| A managed Kubernetes service for the pilot | Less cluster administration | Worker nodes are not free on the services considered |
| Cloudflare R2 for pilot backups | 10 GB of storage and free egress each month | A second provider and a second location to record for the pilot |

## Consequences

- The local cluster is created without kind's default network plugin, and Calico is installed; the negative tests from ADR 0008 confirm enforcement.
- The local cluster runs a lean set of components; a full monitoring stack is not assumed to fit in 7.6 GB of memory.
- The data inventory records the pilot's location (Johannesburg) for the database and backups. With synthetic data, no real personal data leaves Nigeria; a production deployment with real data addresses section 41 before go-live.
- The free-tier terms relied on are recorded with the date they were checked, and are checked again before the pilot starts.
- The production recommendation evaluates hosting in Lagos, which press reports describe as available through an AWS Local Zone, confirmed against the provider's own documentation at that stage.
