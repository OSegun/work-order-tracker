# ADR 0003: PostgreSQL on Kubernetes with CloudNativePG

## Status
Accepted

## Context

ADR 0001 runs the database as a service inside Kubernetes, and ADR 0002 chooses PostgreSQL. A database keeps state that must survive restarts and be recoverable: daily backups, a recovery point objective of 24 hours, a recovery time objective of 4 hours and a tested restore before go-live (NFR-12). Dependencies must stay patched (NFR-11). Backups must be stored outside the cluster, because a backup inside the cluster is lost with it.

## Decision

PostgreSQL runs under the CloudNativePG operator. Backups are taken continuously to object storage outside the cluster through the Barman Cloud Plugin, which supports point-in-time recovery. The database starts as one instance; production runs two instances, a primary and a replica.

## Alternatives considered

| Option | Advantages | Disadvantages |
|---|---|---|
| CloudNativePG operator with the Barman Cloud Plugin (chosen) | Automates backup, restore and failover; continuous backup with point-in-time recovery; open source under the Apache 2 licence; accepted into the Cloud Native Computing Foundation (CNCF) at Sandbox level on 21 January 2025 | The operator and plugin are extra components to install and upgrade |
| Official PostgreSQL image in a StatefulSet, with a backup CronJob | Uses only core Kubernetes resources | Backup, restore and failover are built and maintained by hand; a nightly dump allows only restores to the time of the dump |
| Bitnami Helm chart | Quick to install | The free images were moved to a legacy repository that its announcement says "will no longer receive updates", which conflicts with NFR-11 |
| Managed PostgreSQL outside the cluster | Least operational work | Excluded by ADR 0001, which places the database inside Kubernetes |

CloudNativePG meets NFR-12 with continuous backup and point-in-time recovery, which exceeds the 24-hour recovery point objective, and is maintained under a public foundation. Its documentation states that the operator's built-in object-store backup was "deprecated starting with v1.26 in favor of the Barman Cloud Plugin", so the plugin is used from the start.

## Consequences

- The CloudNativePG operator and the Barman Cloud Plugin are installed in the cluster and upgraded with the platform's other dependencies.
- An object storage service outside the cluster is required. Its provider, region and cost are decided in the hosting ADR, together with the cluster's location.
- Where backups or the database are stored outside Nigeria, the transfer is recorded in the data inventory with its legal basis under section 41 of the Nigeria Data Protection Act 2023, and assessed in the data protection impact assessment.
- Backup storage location and retention are recorded in the data inventory (NFR-12); backups are kept for 30 days (GR-3).
- A restore, including a point-in-time restore, is tested and recorded in a runbook before go-live.
- Moving from one instance to two, for production, changes one setting and doubles database memory and disk use.
