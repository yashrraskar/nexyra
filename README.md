# MAHASync – The Digital Bridge

> *"MahaSync connects independent government systems so citizens do not have to act as the bridge between departments."*

**Smart India Hackathon 2026 Prototype**  
**Repository:** `nexyra` | **Monorepo Architecture**

---

## 1. Problem Statement
In state governance today, government departments operate in isolated functional silos with independent databases, legacy schemas, and proprietary APIs. When a citizen applies for an agricultural benefit (such as a Direct Benefit Transfer subsidy), the citizen is burdened with manually moving data between departments—physically travelling to the Revenue Department, obtaining a 7/12 Land Record certificate, and carrying paper documents to the Agriculture Department.

This fragmentation leads to:
- Severe administrative delays (weeks or months for simple scheme verification).
- Harassment and travel burden for rural citizens.
- Fraud and document tampering risks.
- Massive bureaucratic overhead for departmental officers.

---

## 2. The Solution: MAHASync
MahaSync acts as a digital interoperability layer between independent government systems:
- **Core Principle:** *"One Citizen. One Profile. One Platform. Connected Government."*
- **Non-Invasive Interoperability:** MahaSync does **not** replace government systems; it connects them.
- **DPDP Act 2023 Compliance:** Cross-departmental data exchange occurs only with explicit, informed citizen consent.
- **Asynchronous Reliability:** Decouples departmental systems via standardized adapters and a RabbitMQ event bus.

---

## 3. Target Architecture & Data Flow

```text
[Citizen Browser]
       │
       ▼ (1. Authenticate via Keycloak SSO)
[Next.js Citizen Portal] (Port 3000 / 8082)
       │
       ▼ (2. Select Scheme: Agriculture Subsidy)
[MahaSync FastAPI Backend Gateway] (Port 8082)
       │
       ▼ (3. Explicit DPDP Consent Challenge: "Allow / Deny")
[Consent & Audit Engine]
       │
       ▼ (4. Query Land Record)
[Revenue Department API] (Port 8000) ──▶ [revenue.db (land_records)]
       │
       ▼ (5. Raw Revenue JSON)
[Revenue Adapter] (revenue_adapter.py)
       │
       ▼ (6. Canonical MahaSync Format)
[RabbitMQ Event Bus] (Exchange: mahasync.events | Routing: land.verified)
       │
       ▼ (7. Consume Event)
[Agriculture Adapter] (agriculture_adapter.py)
       │
       ▼ (8. Standardized Agriculture Payload)
[Agriculture Department API] (Port 8001) ──▶ [agriculture.db (subsidy_applications)]
       │
       ▼ (9. Application A001 flips: PENDING ──▶ VERIFIED)
[MahaSync Real-time Application Tracker]
```

---

## 4. Team Responsibilities Matrix

| Member | Module | Key Responsibilities & Deliverables | Status |
| :--- | :--- | :--- | :--- |
| **Member 1** | **Frontend** (`frontend/`) | Next.js/React citizen portal, dashboard, service catalog, consent modal, 5-stage tracking timeline, MahaMitra AI chat. | **COMPLETED** |
| **Member 2** | **Backend Core** (`backend/`) | FastAPI orchestrator, application state machine, DPDP consent engine, append-only audit trail, schema validation. | **COMPLETED** |
| **Member 3** | **Government Systems** (`goverment_systems/`) | Autonomous Revenue API (:8000), Agriculture API (:8001), independent SQLite databases, and departmental visual portals. | **COMPLETED** |
| **Member 4** | **RabbitMQ Event Bus** (`rabbitmq/`) | Topic exchange topology, message persistence, publisher/consumer workers with automatic in-process fallback. | **COMPLETED** |
| **Member 5** | **Identity & IAM** (`keycloak/`) | Keycloak realm configuration, OAuth2/OIDC token verification, citizen/officer roles, and DPDP consent scopes. | **COMPLETED** |
| **Member 6** | **Documentation & Testing** (`documentation/`) | Architecture diagrams, 25+ judge Q&A guide, automated test suite, live demo scripts, Docker Compose orchestration. | **COMPLETED** |

---

## 5. Repository Structure

```text
nexyra/
├── README.md                              # Main project documentation
├── docker-compose.yml                     # Multi-service container orchestration
├── run_demo.py                            # Master one-click local presentation runner
├── start_demo.bat                         # Windows batch launcher
│
├── backend/                               # Member 2: FastAPI Interoperability Core
│   ├── api/v1/                            # REST routers (services, applications, assistant)
│   ├── services/                          # Orchestrator, audit logger, AI assistant
│   ├── config.py                          # Environmental configuration
│   ├── database.py                        # SQLAlchemy connection & session management
│   ├── models.py                          # Citizen, Service, Application, Consent, AuditEvent
│   ├── schemas.py                         # Pydantic validation schemas
│   ├── portal_ui.py                       # Embedded zero-dependency citizen frontend
│   └── main.py                            # FastAPI application entrypoint
│
├── frontend/                              # Member 1: Next.js Citizen Web Portal
│   ├── src/pages/                         # /login, /dashboard, /services, /apply, /consent, /applications
│   ├── src/components/                    # Navbar, ConsentModal, MahaMitraChat
│   ├── package.json                       # Next.js 14, React 18, Tailwind CSS
│   └── next.config.js                     # Next.js configuration
│
├── goverment_systems/                     # Member 3: Mock Autonomous Departments
│   ├── revenue/                           # Revenue API (:8000), revenue.db, /revenue/portal
│   ├── agriculture/                       # Agriculture API (:8001), agriculture.db, /agriculture/portal
│   └── adapters/                          # Canonical adapters (revenue_adapter, agriculture_adapter)
│
├── rabbitmq/                              # Member 4: RabbitMQ Event Bus
│   ├── connection.py                      # Broker manager with resilient in-process fallback
│   ├── publisher.py                       # Publishes LandVerified persistent events
│   ├── consumer.py                        # Consumes events & triggers Agriculture API
│   ├── schemas.py                         # Event payload definitions
│   └── definitions.json                   # Automated RabbitMQ exchange & queue topology
│
├── keycloak/                              # Member 5: Identity & Access Management
│   ├── realm-export.json                  # Pre-configured mahasync realm, clients, roles, users
│   ├── auth_middleware.py                 # JWT token validator & local demo session provider
│   └── docker-compose.yml                 # Standalone Keycloak 24 + PostgreSQL stack
│
├── documentation/                         # Member 6: Project Documentation & Judging
│   ├── diagrams/                          # Mermaid system and sequence flow diagrams
│   ├── judge_qa/                          # 25+ detailed jury questions & technical answers
│   ├── demo/                              # 3-minute pitch & 5-minute deep dive scripts
│   └── testing/                           # Test execution matrix and verification proofs
│
└── tests/                                 # Automated Test Suite
    ├── test_e2e_integration.py            # Comprehensive end-to-end Python test cases
    └── run_tests.py                       # Standalone test runner (8/8 tests passing)
```

---

## 6. Quickstart: Running the Live Demonstration

### Option A: Master One-Click Local Runner (Recommended for SIH Judging)
Requires only standard Python (Python 3.10+):
```bash
python run_demo.py
```
*Or on Windows, simply double click [`start_demo.bat`](file:///d:/Yash/VS%20CODE/nexyra/start_demo.bat).*

This launches all microservices and displays active portal URLs:
- **🌐 Citizen Portal:** [`http://127.0.0.1:8082/portal`](http://127.0.0.1:8082/portal)
- **🏛️ Revenue Department Portal:** [`http://127.0.0.1:8000/revenue/portal`](http://127.0.0.1:8000/revenue/portal)
- **🌾 Agriculture Department Portal:** [`http://127.0.0.1:8001/agriculture/portal`](http://127.0.0.1:8001/agriculture/portal)
- **📚 Interactive Swagger Docs:** [`http://127.0.0.1:8082/docs`](http://127.0.0.1:8082/docs)

### Option B: Docker Compose (Full Stack)
```bash
docker compose up --build
```

---

## 7. Primary Demonstration Walkthrough

1. **Inspect Revenue Department:** Open `http://127.0.0.1:8000/revenue/portal`. Observe that citizen **Rahul Patil (C001)** has registered land parcel **MH-LAND-101 (2.5 Acres)** marked as **VERIFIED**.
2. **Inspect Agriculture Department:** Open `http://127.0.0.1:8001/agriculture/portal`. Observe that application **A001** is in **PENDING** status with land verification unconfirmed.
3. **Open Citizen Portal:** Open `http://127.0.0.1:8082/portal`. Rahul views his active Agriculture Subsidy application.
4. **Grant Explicit Consent:** Review the DPDP Consent challenge: *"Revenue Department land information is required to verify your Agriculture Subsidy application."* Click **"Allow & Verify Automatically"**.
5. **Real-Time Interoperability:** In under one second, the 6-stage tracker completes:
   - Application Submitted ➔ Consent Granted ➔ Revenue Queried ➔ Adapter Standardized ➔ RabbitMQ Event Published ➔ Agriculture Application Verified.
6. **Confirm Autonomous Update:** Refresh the Agriculture Department Portal (`http://127.0.0.1:8001/agriculture/portal`). Application **A001** has automatically updated to **VERIFIED**!
7. **Inspect Audit Trail:** Switch to the *"Audit Trail & Interoperability"* tab to review the immutable, timestamped log of all cross-departmental operations.

---

## 8. Automated Testing
Run the automated integration test suite:
```bash
python tests/run_tests.py
```
**Results:** `8 PASSED, 0 FAILED out of 8 tests` (verifying Revenue API, Agriculture API, Adapters, Consent denial safety, end-to-end integration flow, and AI assistant).

---

## 9. Limitations & Future Roadmap
- **Prototype vs Production:** In this SIH prototype, government systems are simulated via microservices with SQLite databases. In production, adapters interface with state APIs (such as MahaBhumi / 7/12 land registry and MahaDBT).
- **Audit Immutability:** Audit trails are currently recorded in append-only relational database tables; production deployments will anchor transaction root hashes to a government permissioned blockchain or WORM storage.
- **Future Scope:** Expanding adapters to include Civil Supplies (Ration Cards), Energy Department (Solar pump electricity subsidy), and Health Services (Ayushman Bharat).
