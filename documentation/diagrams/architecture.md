# MAHASync Architecture Diagrams (Member 6)

## 1. High-Level Interoperability Architecture
```mermaid
flowchart TD
    subgraph Citizen Layer
        Citizen["👤 Citizen (Rahul - C001)"]
        UI["🌐 MahaSync Citizen Portal<br/>(Next.js / Port 3000 or 8082)<br/>Dashboard • Consent • Stepper"]
    end

    subgraph Security & IAM
        Keycloak["🔐 Keycloak IAM (Port 8080)<br/>Realm: mahasync | User: rahul<br/>OIDC Tokens & Consent Scope"]
    end

    subgraph Interoperability Core [MahaSync Backend - Port 8082]
        Gateway["⚡ FastAPI Interoperability Gateway"]
        ConsentEngine["⚖️ DPDP Consent & State Engine"]
        Orchestrator["🔄 Data Exchange Orchestrator"]
        AuditLog["📜 Immutable Audit Trail Engine<br/>(PostgreSQL / SQLite)"]
        AIAssistant["🤖 MahaMitra AI Government Assistant"]
    end

    subgraph Adapters & Event Bus
        RevAdapter["🔄 Revenue Adapter<br/>(revenue_adapter.py)"]
        AgriAdapter["🔄 Agriculture Adapter<br/>(agriculture_adapter.py)"]
        RabbitMQ["📨 RabbitMQ Event Bus (Port 5672)<br/>Exchange: mahasync.events<br/>Queue: agriculture.land_verified"]
    end

    subgraph Independent Government Systems
        subgraph Revenue Department [Port 8000]
            RevAPI["🏛️ Revenue API (FastAPI)"]
            RevDB[("💾 revenue.db<br/>(land_records)")]
            RevPortal["🖥️ Revenue Dept Portal<br/>(/revenue/portal)"]
            RevAPI <--> RevDB
            RevPortal <--> RevDB
        end

        subgraph Agriculture Department [Port 8001]
            AgriAPI["🌾 Agriculture API (FastAPI)"]
            AgriDB[("💾 agriculture.db<br/>(subsidy_applications)")]
            AgriPortal["🖥️ Agriculture Dept Portal<br/>(/agriculture/portal)"]
            AgriAPI <--> AgriDB
            AgriPortal <--> AgriDB
        end
    end

    Citizen -->|1. Authenticate / Login| UI
    UI <-->|2. OIDC Token / Identity| Keycloak
    UI -->|3. Apply Agriculture Subsidy| Gateway
    Gateway --> ConsentEngine
    ConsentEngine -->|4. Request Explicit Consent| UI
    Citizen -->|5. Grant Consent (ALLOW)| ConsentEngine
    ConsentEngine -->|6. Log Consent Artifact| AuditLog
    ConsentEngine --> Orchestrator
    Orchestrator -->|7. Query 7/12 Land Record| RevAPI
    RevAPI -->|8. Raw Revenue JSON| RevAdapter
    RevAdapter -->|9. Standard MahaSync JSON| Orchestrator
    Orchestrator -->|10. Publish LandVerifiedEvent| RabbitMQ
    RabbitMQ -->|11. Consume Event| AgriAdapter
    AgriAdapter -->|12. Standardized Agriculture Payload| AgriAPI
    AgriAPI -->|13. Update A001 -> VERIFIED| AgriDB
    AgriAPI -->|14. Status Confirmation| Orchestrator
    Orchestrator -->|15. Finalize APP-2026-001 -> VERIFIED| AuditLog
    AuditLog -->|16. Real-time Stepper Update| UI
```

---

## 2. End-to-End Interoperability Sequence Flow
```mermaid
sequenceDiagram
    autonumber
    actor Citizen as Rahul (Citizen C001)
    participant UI as MahaSync Portal
    participant Core as MahaSync Orchestrator
    participant Rev as Revenue Dept (:8000)
    participant RevAdap as Revenue Adapter
    participant RMQ as RabbitMQ (mahasync.events)
    participant AgriAdap as Agriculture Adapter
    participant Agri as Agriculture Dept (:8001)

    Citizen->>UI: Selects "Agriculture Subsidy Scheme"
    Citizen->>UI: Submits Application
    UI->>Core: POST /api/v1/applications
    Core-->>UI: Returns APP-2026-001 (CONSENT_PENDING)
    UI->>Citizen: Displays DPDP Consent Challenge
    Note over Citizen,UI: "Revenue Dept land info is required to verify your Agriculture Subsidy."
    Citizen->>UI: Clicks "ALLOW"
    UI->>Core: POST /api/v1/applications/APP-2026-001/consent (action="ALLOW")
    Core->>Core: Logs CONSENT_GRANTED to Audit Trail

    Core->>Rev: GET /revenue/land/C001
    Rev-->>Core: Returns {"citizen_id": "C001", "land_id": "MH-LAND-101", "area": 2.5, "verified": true}
    Core->>RevAdap: convert_revenue_to_mahasync(data)
    RevAdap-->>Core: Standardized {"citizenId": "C001", "landId": "MH-LAND-101", "landArea": 2.5, "verificationStatus": "VERIFIED"}

    Core->>RMQ: Publish LandVerified event (routing: land.verified)
    RMQ->>AgriAdap: Event received by Consumer
    AgriAdap->>AgriAdap: convert_mahasync_to_agriculture(event)
    AgriAdap->>Agri: POST /agriculture/verify-land
    Agri->>Agri: UPDATE subsidy_applications SET land_verified=1, status='Verified' WHERE citizen_id='C001'
    Agri-->>AgriAdap: 200 OK {"status": "Verified", "application_id": "A001"}
    
    Core->>Core: Update Application APP-2026-001 -> VERIFIED
    Core->>Core: Record APPLICATION_FINALIZED Audit Event
    Core-->>UI: 200 OK {"application_status": "VERIFIED"}
    UI->>Citizen: Updates Stepper to 100% Completed & Verified
```

---

## 3. Data Transformation & Canonical Model
```text
[Revenue Department Model]
{
  "citizen_id": "C001",
  "citizen_name": "Rahul",
  "land_id": "MH-LAND-101",
  "area": 2.5,
  "verified": true
}
              │
              ▼ convert_revenue_to_mahasync()
[Canonical MahaSync Model]
{
  "citizenId": "C001",
  "landId": "MH-LAND-101",
  "landArea": 2.5,
  "verificationStatus": "VERIFIED"
}
              │
              ▼ convert_mahasync_to_agriculture()
[Agriculture Department Model]
{
  "applicantId": "C001",
  "propertyNumber": "MH-LAND-101",
  "landArea": 2.5,
  "verificationStatus": "VERIFIED"
}
```
