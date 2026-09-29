# Traceability

This document maps every functional, governance and non-functional requirement in the [requirements](../requirements/requirements.md) to the component that implements it, the tables it uses (see the [data model](data-model.md)) and the decisions that shape it (`docs/adr/`).

## Components

The API service contains seven modules (ADR 0001): **Accounts** (accounts and access), **Customers** (customers, buildings and contracts), **Work orders**, **SLA clock** (SLA clock and working calendar), **Planned maintenance**, **Reports** and **Governance**. Platform components are the **Gateway** (Envoy Gateway and cert-manager), **CronJobs**, the **Database** (PostgreSQL under CloudNativePG), **CI/CD** (GitHub Actions and Flux) and **Observability** (logs, metrics and probes).

## Functional requirements

| Requirement | Component | Tables | Decisions |
|---|---|---|---|
| FR-1 Accounts, roles, trades and supervisors | Accounts | users | ADR 0005 |
| FR-2 Customers, buildings and contract terms | Customers | customers, buildings, contracts, contract_sla_terms | ADR 0002 |
| FR-3 Log a breakdown | Work orders | work_orders | ADR 0009 |
| FR-4 Duplicate warning | Work orders | work_orders | — |
| FR-5 Calculate due times | SLA clock, called by Work orders | work_orders, work_order_holds, contract_sla_terms, holidays, calendar_settings | ADR 0009 |
| FR-6 Assign and reassign | Work orders | work_orders, users | ADR 0005 |
| FR-7 Technician's own jobs | Work orders | work_orders, customer_contacts | ADR 0005 |
| FR-8 Arrived, on hold, completed | Work orders | work_orders, work_order_holds | ADR 0010 |
| FR-9 Parts and billable flag | Work orders | work_order_parts, work_orders, contracts | — |
| FR-10 Job lifecycle | Work orders | work_orders | ADR 0005 |
| FR-11 Corrections with approval | Work orders | corrections, work_order_history | ADR 0015 |
| FR-12 Job history | Work orders | work_order_history | ADR 0015 |
| FR-13 Deadline list | Reports | work_orders | ADR 0009 |
| FR-14 Planned work orders | Planned maintenance, CronJobs | maintenance_schedules, work_orders | ADR 0011 |
| FR-15 Weekly SLA report | Reports | work_orders, work_order_holds, corrections, work_order_history | ADR 0009 |
| FR-16 Billable-extras CSV | Reports | work_order_parts, work_orders, contracts | — |
| FR-17 Planned maintenance report | Reports | maintenance_schedules, work_orders | — |
| FR-18 Refuse stale saves | Work orders | work_orders (version) | ADR 0010 |
| FR-19 Job log per customer | Reports | work_orders | — |
| FR-20 CSV import | Customers | customers, buildings, customer_contacts, maintenance_schedules | — |
| FR-21 Search and filter | Work orders | work_orders | ADR 0005 |
| FR-22 Assignment email | Work orders | — | ADR 0008 |
| FR-23 Verify or reopen | Work orders | work_orders, work_order_history | ADR 0015 |
| FR-24 Password reset and rules | Accounts | users, sessions | ADR 0004 |
| FR-25 Deactivation | Accounts | users, sessions | ADR 0004 |
| FR-26 Working calendar | SLA clock | holidays, calendar_settings, work_orders, work_order_history | ADR 0009 |
| FR-27 Record completeness report | Reports | work_orders | — |
| FR-28 Spot checks | Work orders, CronJobs | spot_checks | ADR 0011 |
| FR-29 Hold confirmation | Work orders, SLA clock | work_order_holds | ADR 0009 |
| FR-30 OpenAPI description | All modules, CI/CD | — | ADR 0001, ADR 0013 |

## Governance requirements

| Requirement | Component | Tables | Decisions |
|---|---|---|---|
| GR-1 Lawful basis and privacy notice | Accounts | privacy_acknowledgements | Data inventory |
| GR-2 Data subject rights | Governance | users and every table holding their data | ADR 0005 |
| GR-3 Retention and deletion | Governance, CronJobs, Database | users, customer_contacts, work_order_history, audit_log, idempotency_records, failed_logins; backups | ADR 0003, ADR 0011, ADR 0015 |
| GR-4 Access control and audit logging | Accounts, Governance | audit_log, work_order_history | ADR 0005, ADR 0012, ADR 0015 |
| GR-5 Human oversight of AI output | Not applicable | — | Problem statement |
| GR-6 Fairness | Not applicable | — | Problem statement |
| GR-7 Breach response | Observability | audit_log; logs | ADR 0012 |
| GR-8 Data minimisation | Work orders | work_orders (notes) | Data inventory |

## Non-functional requirements

| Requirement | Component | Decisions |
|---|---|---|
| NFR-1 Performance | API pods, Database | ADR 0001, ADR 0002, ADR 0004 |
| NFR-2 Scalability | API pods, Database | ADR 0001, ADR 0002 |
| NFR-3 Concurrency | Work orders, Database | ADR 0002, ADR 0010 |
| NFR-4 Mobile efficiency | All modules (response compression) | ADR 0001 |
| NFR-5 Unreliable networks | Work orders | ADR 0010 |
| NFR-6 API usability | All modules | ADR 0010 |
| NFR-7 Availability | Gateway, API pods, Observability | ADR 0012, ADR 0014 |
| NFR-8 Time correctness | SLA clock | ADR 0009 |
| NFR-9 Transport and login security | Gateway, Accounts | ADR 0004, ADR 0006 |
| NFR-10 Authorisation | Accounts (policy module) | ADR 0005 |
| NFR-11 Secrets and dependencies | CI/CD | ADR 0013, ADR 0016 |
| NFR-12 Recovery | Database | ADR 0003 |
| NFR-13 Cost | All platform components | ADR 0014 |
| NFR-14 Maintainability | CI/CD | ADR 0013 |

Every functional and governance requirement is assigned to at least one component; GR-5 and GR-6 are recorded as not applicable.
