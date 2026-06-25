# REQUIREMENTS.md

## Overview
**Project:** flux‑trace  
**Purpose:** Implement a lightweight, reliable payment‑processing service that automatically retries failed transactions up to three times before marking them as permanently failed. The service will expose a clean API for initiating payments, querying status, and retrieving audit logs. It must be production‑ready, secure, and easy to integrate with existing e‑commerce platforms.

---

## 1. Functional Requirements

| ID | Description |
|----|-------------|
| **FR‑1** | **Create Payment Request** – The system shall expose an endpoint `POST /payments` that accepts a JSON payload containing: <br>• `amount` (decimal, > 0) <br>• `currency` (ISO‑4217 code) <br>• `payment_method` (token or reference) <br>• `metadata` (optional key‑value map) <br>and returns a unique `payment_id` with initial status `PENDING`. |
| **FR‑2** | **Process Payment** – Upon receipt of a payment request, the service shall invoke the configured downstream payment gateway (e.g., Stripe, PayPal) to attempt the transaction. |
| **FR‑3** | **Automatic Retry Logic** – If a payment attempt fails with a *transient* error (network timeout, 5xx gateway response, or specific retry‑eligible error codes), the system shall automatically retry the transaction up to **3** additional times, with exponential back‑off (1 s, 2 s, 4 s). After the final attempt, the status becomes `FAILED`. |
| **FR‑4** | **Idempotent Requests** – Re‑submitting the same `payment_id` must not create duplicate charges. The service shall detect duplicate `POST /payments` calls (via client‑provided idempotency key) and return the existing payment status. |
| **FR‑5** | **Query Payment Status** – Provide `GET /payments/{payment_id}` returning the current status (`PENDING`, `SUCCESS`, `FAILED`), number of attempts, timestamps, and any error messages. |
| **FR‑6** | **Webhook Notifications** – Allow registration of a webhook URL (`POST /webhooks`) and emit events (`payment_success`, `payment_failed`) with payload containing `payment_id` and final status. |
| **FR‑7** | **Audit Log** – Persist an immutable audit trail for each payment, recording: request payload, gateway responses, retry attempts, timestamps, and final outcome. Expose `GET /payments/{payment_id}/audit` (admin‑only). |
| **FR‑8** | **Admin Dashboard API** – Endpoints to list payments with filters (date range, status, amount) and to manually trigger a retry for a `FAILED` payment. |
| **FR‑9** | **Health Check** – `GET /healthz` must return `200 OK` with JSON `{status: "ok"}` when the service and its downstream gateway connectivity are healthy. |
| **FR‑10** | **Configuration Management** – Load runtime configuration (gateway credentials, retry limits, back‑off policy, webhook secret) from environment variables or a secure config store. |

---

## 2. Non‑Functional Requirements

| ID | Requirement |
|----|-------------|
| **NFR‑1** | **Performance** – Average payment processing latency (including retries) must be ≤ 500 ms for successful transactions; 95th‑percentile ≤ 1 s. |
| **NFR‑2** | **Scalability** – The service shall be horizontally scalable; each instance must be stateless aside from persisted audit data. |
| **NFR‑3** | **Reliability** – Achieve ≥ 99.9 % uptime. Retries must be persisted so that a crash does not lose in‑flight attempts. |
| **NFR‑4** | **Security** – All external communication must use TLS 1.2+. Sensitive data (gateway API keys, webhook secrets) stored encrypted at rest. PCI‑DSS compliance for card data: the service never stores raw card numbers; it only forwards tokenized `payment_method`. |
| **NFR‑5** | **Observability** – Emit structured logs (JSON) and metrics (Prometheus) for: request count, success/failure rates, retry count, latency histograms, and webhook delivery status. |
| **NFR‑6** | **Data Integrity** – Use ACID‑compliant storage (e.g., PostgreSQL) for audit logs and payment state. Transactions must be atomic across retry updates. |
| **NFR‑7** | **Compliance** – Support GDPR “right to be forgotten” for metadata (non‑financial fields) via an admin endpoint that redacts data while preserving audit integrity. |
| **NFR‑8** | **Maintainability** – Codebase must follow the Axentx C‑Framework style guide, include unit tests covering ≥ 90 % of core logic, and CI pipeline must enforce linting and static analysis. |
| **NFR‑9** | **Portability** – Containerize the service (Docker) with a minimal base image (e.g., `python:3.11-slim` or `golang:1.22-alpine`). Provide a Helm chart for Kubernetes deployment. |
| **NFR‑10** | **Backup & Recovery** – Daily automated backups of the audit database with point‑in‑time recovery capability within 24 h. |

---

## 3. Constraints

1. **Technology Stack** – Must use one of the approved Axentx runtimes: Python 3.11 (FastAPI) **or** Go 1.22 (Gin). No external proprietary libraries beyond the approved payment‑gateway SDKs.
2. **Third‑Party Gateways** – Only gateways with SDKs that support idempotent charge creation may be integrated.
3. **Retry Limit** – Fixed at 3 retries (configurable only for testing; production limit immutable).
4. **Data Residency** – All persisted data must reside in EU‑based data centers to satisfy GDPR.
5. **Deployment** – Must be deployable via the existing CI/CD pipeline (GitHub Actions) and pass the Axentx OS chain‑playbook validation steps.

---

## 4. Assumptions

| ID | Assumption |
|----|------------|
| **A‑1** | Downstream payment gateways provide deterministic error codes that allow classification into *transient* vs *permanent* failures. |
| **A‑2** | Clients will supply a unique idempotency key for each logical payment attempt. |
| **A‑3** | Network latency between the service and the gateway is ≤ 200 ms under normal load. |
| **A‑4** | The audit database can handle the expected write volume (≈ 10 k payments/day) without additional sharding. |
| **A‑5** | Webhook consumers will acknowledge receipt with a `2xx` response within 5 seconds; otherwise, the service will retry delivery up to 3 times. |
| **A‑6** | No support for multi‑currency conversion; the amount is charged in the currency supplied by the client. |
| **A‑7** | The service will run behind Axentx’s API gateway which handles authentication/authorization; internal endpoints assume trusted internal traffic. |

---

## 5. Acceptance Criteria

- All functional requirements are implemented and verified by integration tests.
- Performance benchmarks meet NFR‑1 under a simulated load of 500 concurrent payment requests.
- Security scan (OWASP ZAP) reports no critical findings; PCI‑DSS checklist is signed off.
- Deployment to staging passes health checks, webhook delivery, and audit log verification.
- Documentation (API spec, README, operational runbook) is complete and reviewed.

--- 

*Prepared by the senior product/engineering lead for the flux‑trace project.*
