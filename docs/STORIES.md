# STORIES.md

## Project: flux‑trace  
**Domain:** Payment Processing  
**Goal:** Deliver a reliable, retry‑enabled payment processor that can be integrated into downstream services while providing clear observability and extensibility.

---

## Epics & Backlog

| Epic | Description |
|------|-------------|
| **E1 – Core Payment Flow** | Implement the fundamental “pay” endpoint, validation, and retry logic. |
| **E2 – Retry & Failure Handling** | Provide configurable retry policies, exponential back‑off, and dead‑letter handling. |
| **E3 – Observability & Monitoring** | Expose metrics, logs, and tracing for every payment attempt. |
| **E4 – Security & Compliance** | Ensure PCI‑ DSS‑compatible handling of card data and secure storage of secrets. |
| **E5 – Integration & Extensibility** | Offer SDKs / webhooks and a plug‑in architecture for alternative payment gateways. |
| **E6 – Admin & Dashboard** | Simple UI/API for admins to view transaction status, retry history, and manually reprocess. |

> **MVP Scope** – Complete **E1**, **E2**, and **E3**. Remaining epics are slated for Phase 2.

---

## User Stories

### Epic E1 – Core Payment Flow

| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E1‑01** | **As a** downstream service, **I want** a `POST /payments` endpoint that accepts a payment payload, **so that** I can initiate a charge. | 1. Endpoint validates required fields (`amount`, `currency`, `card_token`). <br>2. Returns `202 Accepted` with a UUID `payment_id`. <br>3. Stores the request in a durable queue (e.g., PostgreSQL `payments` table). |
| **E1‑02** | **As a** payment processor, **I want** to persist each payment attempt atomically, **so that** retries are idempotent. | 1. `payment_id` is primary key; attempts are stored in `payment_attempts` with a unique `attempt_id`. <br>2. Duplicate `payment_id` submissions are rejected with `409 Conflict`. |
| **E1‑03** | **As a** developer, **I want** the system to emit a `PaymentCreated` event, **so that** other services can react (e.g., order fulfillment). | 1. Event published to the internal message bus (Kafka/RabbitMQ). <br>2. Payload includes `payment_id`, `status: pending`, and original request data. |
| **E1‑04** | **As a** QA engineer, **I want** deterministic test fixtures for successful and failed payments, **so that** automated tests are reliable. | 1. Mock gateway can be toggled via env var (`MOCK_GATEWAY=success|failure`). <br>2. Test suite covers happy path, validation errors, and gateway timeouts. |

### Epic E2 – Retry & Failure Handling

| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E2‑01** | **As a** payment processor, **I want** to automatically retry a failed payment up to 3 times, **so that** transient errors are resolved without manual intervention. | 1. Retry count stored per `payment_id`. <br>2. Retries triggered via background worker (e.g., Celery/Sidekiq). <br>3. After 3 attempts, status set to `failed`. |
| **E2‑02** | **As a** system admin, **I want** exponential back‑off (e.g., 1s, 2s, 4s) between retries, **so that** we avoid hammering the downstream gateway. | 1. Back‑off algorithm configurable via `RETRY_BACKOFF_MS`. <br>2. Logs show the scheduled next attempt timestamp. |
| **E2‑03** | **As a** support engineer, **I want** failed payments to be moved to a dead‑letter queue, **so that** they can be inspected and manually reprocessed. | 1. After max retries, message is published to `payments.dlq`. <br>2. DLQ entry contains full request payload and error stack trace. |
| **E2‑04** | **As a** product owner, **I want** the max‑retry count to be configurable per merchant, **so that** high‑risk merchants can have stricter policies. | 1. `merchants` table stores `max_retries`. <br>2. Processor reads this value at runtime; defaults to 3 if not set. |

### Epic E3 – Observability & Monitoring

| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E3‑01** | **As an** ops engineer, **I want** Prometheus metrics for total payments, successes, failures, and retries, **so that** we can monitor system health. | 1. `/metrics` endpoint exposes `payment_total`, `payment_success`, `payment_failed`, `payment_retries`. <br>2. Metrics are labelled by `merchant_id` and `status`. |
| **E3‑02** | **As a** developer, **I want** structured JSON logs for each attempt, **so that** log aggregation tools can parse them. | 1. Log fields: `payment_id`, `attempt_number`, `status`, `duration_ms`, `error_code` (if any). |
| **E3‑03** | **As a** tracing specialist, **I want** OpenTelemetry spans covering the entire payment lifecycle, **so that** we can trace latency across services. | 1. Span named `payment.process`. <br>2. Child spans for `gateway.request` and `retry.scheduler`. |
| **E3‑04** | **As a** product manager, **I want** an alert when failure rate exceeds 2% over a 5‑minute window, **so that** we can react quickly. | 1. Alert rule defined in Prometheus/Alertmanager. <br>2. Notification sent to Slack channel `#payments-alerts`. |

### Epic E4 – Security & Compliance (Phase 2)

| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E4‑01** | **As a** security auditor, **I want** card data to be tokenized before storage, **so that** we never persist raw PANs. | 1. Integration with a PCI‑compliant tokenization service. <br>2. Database column `card_token` is opaque; raw card numbers never written. |
| **E4‑02** | **As a** DevOps engineer, **I want** secret values (API keys, DB passwords) loaded from a vault, **so that** they are not hard‑coded. | 1. Use HashiCorp Vault or AWS Secrets Manager. <br>2. Application fails to start if required secrets are missing. |

### Epic E5 – Integration & Extensibility (Phase 2)

| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E5‑01** | **As a** third‑party developer, **I want** a Python SDK that wraps the `/payments` API, **so that** I can integrate quickly. | 1. SDK published to PyPI. <br>2. Includes type hints, retry handling, and example usage. |
| **E5‑02** | **As a** merchant, **I want** webhook callbacks on status changes, **so that** my order system can update automatically. | 1. Configurable webhook URL per merchant. <br>2. Payload includes `payment_id`, `old_status`, `new_status`. |
| **E5‑03** | **As a** system architect, **I want** a plug‑in interface for alternative gateways, **so that** we can add new providers without core changes. | 1. Gateway interface defines `charge(payload) -> Result`. <br>2. Discovery via entry‑point `flux_trace.gateway`. |

### Epic E6 – Admin & Dashboard (Phase 2)

| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E6‑01** | **As an** admin, **I want** a web UI listing recent payments with filter/sort, **so that** I can investigate issues. | 1. UI built with React + Ant Design. <br>2. Supports filtering by `merchant_id`, `status`, date range. |
| **E6‑02** | **As an** support agent, **I want** a “Re‑process” button on failed payments, **so that** I can trigger a manual retry. | 1. Button calls internal `/payments/{id}/retry` endpoint. <br>2. UI updates status in real‑time via WebSocket. |

---

## Prioritisation for MVP (Sprint 1‑3)

1. **E1‑01**, **E1‑02**, **E1‑03**, **E1‑04** – foundational API & persistence.  
2. **E2‑01**, **E2‑02**, **E2‑03** – automatic retry & dead‑letter handling.  
3. **E3‑01**, **E3‑02**, **E3‑03** – observability (metrics, logs, tracing).  
4. **E3‑04** – alerting (can be added after metrics are live).  

*Remaining stories (E4‑E6) will be scoped into Phase 2 after MVP validation.*

--- 

*All stories are written to be testable, shippable, and aligned with the company’s “validated paying need” principle.*
