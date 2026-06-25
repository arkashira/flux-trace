# ROADMAP.md – flux‑trace

## Overview
**flux‑trace** is a lightweight, retry‑aware payment processor that guarantees up to three attempts for any failed transaction. The roadmap below defines a clear, shippable path from a **Minimum Viable Product (MVP)** to a full‑featured, production‑ready service (v1 & v2). Each milestone is tied to concrete deliverables, acceptance criteria, and measurable success signals.

---

## 📅 Milestones

| Milestone | Target Release | Core Theme | MVP‑Critical? |
|-----------|----------------|------------|---------------|
| **MVP**   | **2026‑09‑30** | Reliable core payment flow with retry logic | ✅ |
| **v1**    | **2026‑12‑15** | Observability, extensibility & compliance | ❌ |
| **v2**    | **2027‑03‑31** | Scaling, ecosystem integration & advanced risk controls | ❌ |

---

## 🚀 MVP – Core Processor (Must‑Have for Launch)

| Feature | Description | Acceptance Criteria |
|---------|-------------|----------------------|
| **1️⃣ Payment API** | RESTful `POST /payments` accepting `{amount, currency, source, destination}` | - Returns `202 Accepted` with a unique `payment_id`.<br>- Validates schema & required fields. |
| **2️⃣ Retry Engine** | Automatic retry of failed payments up to **3** attempts with exponential back‑off (1s → 2s → 4s). | - On transient error (network/5xx) the engine retries exactly 3 times.<br>- Final status persisted as `succeeded` or `failed`. |
| **3️⃣ Persistence Layer** | PostgreSQL schema for `payments` (id, amount, currency, source, destination, status, attempt_count, timestamps). | - All state changes are ACID‑compliant.<br>- Ability to query by `payment_id`. |
| **4️⃣ Idempotency** | Idempotency‑key header support to avoid duplicate charges on retries/re‑submissions. | - Duplicate request with same key returns original `payment_id` and status. |
| **5️⃣ Basic CLI / SDK** | Minimal Python client (`flux_trace.Client`) wrapping the HTTP API. | - Can create a payment and poll status via SDK. |
| **6️⃣ Test Suite** | Unit + integration tests covering happy path, retry logic, and idempotency. | - ≥ 90 % coverage; CI pipeline passes on every push. |
| **7️⃣ CI/CD Pipeline** | GitHub Actions workflow: lint → test → Docker build → push to registry. | - Automated builds on `main` and PRs; deployable artifact produced. |
| **8️⃣ Documentation** | README with quick‑start, API spec (OpenAPI 3.0), and SDK usage examples. | - New developer can spin up a local instance in ≤ 10 min. |

### Success Metrics (MVP)
- **Reliability**: 99.5 % of payments processed without manual intervention in staging.
- **Latency**: 95 th percentile end‑to‑end processing ≤ 500 ms (excluding back‑off retries).
- **Stability**: No critical bugs in CI for 2 consecutive weeks post‑release.

---

## 🌱 v1 – Observability, Extensibility & Compliance

| Feature | Description | Acceptance Criteria |
|---------|-------------|----------------------|
| **1️⃣ Structured Logging & Tracing** | OpenTelemetry integration; logs in JSON; trace IDs propagated across retries. | - Logs searchable in ELK/Datadog.<br>- End‑to‑end trace visible for each payment. |
| **2️⃣ Metrics & Alerting** | Prometheus exporter exposing `payments_total`, `payments_successful`, `payments_failed`, `retry_attempts`. | - Grafana dashboards ready.<br>- Alerts on failure rate > 2 % over 5 min. |
| **3️⃣ Webhook Callbacks** | Configurable webhook URLs for `payment_success` and `payment_failure`. | - Secure HMAC signature verification.<br>- Retries on webhook delivery up to 3 times. |
| **4️⃣ PCI‑DSS Minimal Controls** | Tokenization of card data via a third‑party vault (e.g., Stripe Token API). | - No raw PAN stored; audit logs for token access. |
| **5️⃣ Plugin Architecture** | Hook points for custom payment gateways (e.g., Stripe, PayPal). | - Sample gateway plugin included; can be swapped without code change. |
| **6️⃣ Multi‑Region Deploy** | Helm chart with Helm values for region‑specific PostgreSQL replicas. | - Deployable to two Kubernetes clusters; traffic routing via DNS. |
| **7️⃣ Upgrade Migration Scripts** | DB migration (Flyway) from MVP schema to v1 schema (adds webhook table, audit fields). | - Zero‑downtime migration verified in staging. |
| **8️⃣ Expanded SDKs** | Node.js and Go client libraries. | - Feature parity with Python SDK; CI coverage ≥ 80 %. |

### Success Metrics (v1)
- **Observability**: 99 % of payment flows have complete trace data.
- **Compliance**: Pass internal PCI‑DSS checklist audit.
- **Extensibility**: At least one external gateway integrated via plugin.

---

## 📈 v2 – Scaling, Ecosystem Integration & Advanced Risk Controls

| Feature | Description | Acceptance Criteria |
|---------|-------------|----------------------|
| **1️⃣ Horizontal Scaling** | Stateless API servers behind Envoy; auto‑scaling based on CPU & queue depth. | - System handles 10 k TPS in load‑test with ≤ 1 % error rate. |
| **2️⃣ Distributed Queue** | Kafka (or Pulsar) backed event queue for payment jobs; decouples API from worker pool. | - End‑to‑end latency ≤ 1 s under peak load.<br>- Exactly‑once processing guaranteed. |
| **3️⃣ Fraud & Risk Engine** | Real‑time risk scoring (ML model) that can abort or flag payments. | - Model integrated via gRPC; false‑positive rate < 0.5 %. |
| **4️⃣ Settlement & Reconciliation** | Batch job that reconciles processed payments with downstream acquirer reports. | - Daily reconciliation reports generated automatically; variance < 0.1 %. |
| **5️⃣ Multi‑Currency & FX** | Support for > 30 currencies; automatic FX conversion via external rate provider. | - End‑to‑end conversion accuracy ±0.0005. |
| **6️⃣ SLA & Rate Limiting** | Per‑client SLA contracts; token‑bucket rate limiter per API key. | - Violations logged and throttled; SLA dashboard visible. |
| **7️⃣ Self‑Service Portal** | Web UI for merchants to view payment history, configure webhooks, and manage API keys. | - Auth via OAuth2; UI responsive on desktop & mobile. |
| **8️⃣ Disaster Recovery** | Active‑passive DR site with automated failover testing. | - RTO < 5 min, RPO < 30 s; quarterly DR drills passed. |

### Success Metrics (v2)
- **Throughput**: Sustain 10 k TPS with < 1 % error.
- **Risk**: Fraud detection reduces chargebacks by ≥ 30 % vs. baseline.
- **Customer Ops**: 90 % of merchants self‑service via portal; support tickets ↓ 40 %.

---

## 📌 How to Use This Roadmap
1. **Align Teams** – Each milestone is a cross‑functional sprint (PM, Eng, QA, Ops).  
2. **Track Progress** – Create GitHub Projects columns matching the tables above; move issues as work completes.  
3. **Validate Early** – After MVP launch, collect real‑world payment data to inform v1 risk models and scaling assumptions.  
4. **Iterate** – Review metrics at the end of each phase; adjust scope before committing to the next.

--- 

*Prepared by the senior product/engineering lead, 2026‑06‑25.*
