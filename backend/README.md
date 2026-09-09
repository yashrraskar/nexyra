# MahaSync Core Interoperability Backend (Member 2)

## Architecture Overview
The MahaSync Backend acts as the interoperability orchestration engine connecting independent state government departments. Built on **FastAPI and SQLAlchemy**, it governs citizen consent under India's DPDP Act 2023, queries departmental systems, standardizes payloads via adapters, and publishes events to RabbitMQ.

## API Contracts

### Services
- `GET /api/v1/services`: Returns available government schemes (e.g., Agriculture Subsidy DBT, PM-KISAN).
- `GET /api/v1/services/{service_id}`: Scheme details, eligibility criteria, and required data sources.

### Applications & Consent
- `POST /api/v1/applications`: Initiates a service application in `CONSENT_PENDING` status.
- `GET /api/v1/applications?citizen_id=C001`: Lists active applications for the citizen.
- `GET /api/v1/applications/{application_id}`: Comprehensive status, consent record, and audit trail.
- `GET /api/v1/applications/{application_id}/status`: Lightweight status check for UI badges.
- `POST /api/v1/applications/{application_id}/consent`:
  - Payload: `{"action": "ALLOW"}` or `{"action": "DENY"}`
  - If `ALLOW`: Executes the complete multi-department interoperability flow.
  - If `DENY`: Halts execution safely, marks status `CONSENT_DENIED`, and records audit entry.

### Audit Trail
- `GET /api/v1/applications/{application_id}/events`: Returns timestamped, chronological audit events.

### AI Governance Assistant
- `POST /api/v1/assistant/chat`: Interacts with the context-aware MahaMitra guide for scheme guidance.

## Database Entities
1. `Citizen`: Central citizen identity (`id`, `name`, `email`, `phone`).
2. `Service`: Catalog of government benefits and integration requirements.
3. `Application`: Application state machine (`status`, `land_id`, `land_area`, `created_at`).
4. `ConsentRecord`: Signed DPDP consent artifact (`status`, `purpose`, `data_source`, `granted_at`).
5. `AuditEvent`: Append-only audit log (`timestamp`, `event_type`, `source`, `description`, `status`).

## Running Standalone
```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8082 --reload
```
Interactive Swagger Documentation available at: `http://127.0.0.1:8082/docs`.
