# ADR 0008: Default-deny network policies

## Status
Accepted

## Context

By default, Kubernetes allows every pod to connect to every other pod and to the internet. The Kubernetes documentation for network policies states: "By default, a pod is non-isolated for ingress; all inbound connections are allowed", and the same applies to outbound traffic. A compromised container could therefore reach the database directly, bypassing the API's authentication and authorisation (ADR 0004, ADR 0005), or send data out of the cluster.

The same documentation states: "Creating a NetworkPolicy resource without a controller that implements it will have no effect." Policies work only when the cluster's network plugin enforces them.

## Decision

The `workorders` namespace, which holds the API, the scheduled tasks and PostgreSQL, denies all incoming and outgoing traffic by default. Only these connections are allowed:

1. From the Envoy Gateway pods to the API pods on port 8000.
2. From the API pods to the PostgreSQL pods on port 5432.
3. From the scheduled task pods to the PostgreSQL pods on port 5432.
4. From all pods in the namespace to the cluster's DNS service on port 53.
5. From the CloudNativePG operator to the PostgreSQL pods, on the ports its documentation requires.
6. From the PostgreSQL pods to object storage on port 443, for backups.
7. From the monitoring system to the API pods' internal metrics port, added by ADR 0012.

The Envoy Gateway is the only component reachable from outside the cluster. The API and PostgreSQL services have internal addresses only; administrators reach the database temporarily through `kubectl port-forward`. The cluster uses a network plugin that enforces network policies, and automated tests confirm that forbidden connections fail.

## Alternatives considered

| Option | Advantages | Disadvantages |
|---|---|---|
| Default deny with named exceptions, verified by tests (chosen) | A compromised container reaches only what its rules allow; the API cannot send data out of the cluster | Every new connection needs a rule; a missing DNS rule breaks name lookups |
| Rules only for the database, other traffic open | Fewer rules | The API and scheduled tasks could still send data anywhere |
| No network policies | Nothing to write or maintain | Any pod can reach the database and the internet |
| A service mesh with encrypted, identity-based traffic between services | Stronger controls and encrypted internal traffic | A large additional platform component for two services |

Default deny gives the strongest protection that core Kubernetes provides, at the cost of maintaining a short list of rules.

## Consequences

- Network policy resources are written for each allowed connection and kept with the Kubernetes manifests.
- The local cluster runs a network plugin that enforces network policies.
- Negative tests run after each deployment: a connection from a test pod to PostgreSQL must fail, a connection from an API pod to an outside address must fail, and a connection from an API pod to PostgreSQL must succeed.
- Kubernetes network policies filter by address and port, not by host name, so rule 6 allows the database outbound traffic on port 443 without naming the storage provider.
- If FR-22 is built, one further rule allows the API to reach the mail server only.
