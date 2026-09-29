# ADR 0006: Gateway API as the entry point, with cert-manager

## Status
Accepted

## Context

Requests from the client application must reach the API service over encrypted connections (NFR-9), be routed to the API, and be limited in size and rate before they reach the pods (ADR 0001). Certificates must be renewed before they expire. Only one service is exposed, so no separate API gateway product is used; authentication and authorisation stay in the API (ADR 0004, ADR 0005).

The Kubernetes documentation for Ingress states: "The Kubernetes project recommends using Gateway instead of Ingress. The Ingress API has been frozen." The Kubernetes blog post "Ingress NGINX Retirement: What You Need to Know" (11 November 2025) states that for the ingress-nginx controller, "Best-effort maintenance will continue until March 2026. Afterward, there will be no further releases, no bugfixes, and no updates to resolve any security vulnerabilities that may be discovered."

## Decision

External traffic enters through the Kubernetes Gateway API, implemented by Envoy Gateway: a Gateway listens on port 443 with the TLS certificate, and an HTTPRoute sends API requests to the API service. cert-manager obtains and renews certificates; in local development it issues them from a private certificate authority, and in a real deployment from a public certificate authority for a registered domain. Envoy Gateway's conformance with the current Gateway API release is confirmed against the Gateway API project's implementations list before installation.

## Alternatives considered

| Option | Advantages | Disadvantages |
|---|---|---|
| Gateway API with Envoy Gateway and cert-manager (chosen) | Follows the Kubernetes project's recommendation; separates the listening point (Gateway) from routing rules (HTTPRoute); automatic certificate renewal | Newer than Ingress, so fewer older tutorials; per-address rate limiting depends on the controller's own policy resources |
| Ingress with the ingress-nginx controller | Widely documented | The Ingress API is frozen and the controller receives no security fixes after March 2026, which conflicts with NFR-11 |
| Ingress with another maintained controller | Maintained controller; familiar Ingress resources | Builds on an API the Kubernetes project no longer develops |
| A separate API gateway product in front of the service | Central routing, authentication and rate limiting for many services | Only one service is exposed; authentication needs the database and stays in the API |

The Gateway API is the maintained standard for Kubernetes traffic entry, and cert-manager removes manual certificate renewal. Per-account login limits remain in the API; per-address limits use the controller's policy resources.

## Consequences

- The Gateway API resources, Envoy Gateway and cert-manager are installed in the cluster and upgraded with the platform.
- The `.example` domain cannot receive a public certificate; local development uses a private certificate authority trusted by the developer's machine.
- A real deployment needs a registered domain, whose cost is recorded in the hosting ADR (NFR-13).
- If Envoy Gateway does not appear as conformant for the current release, NGINX Gateway Fabric or Traefik is evaluated instead and this ADR is superseded.
