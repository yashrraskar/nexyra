# MAHASync - Live Judge Demo Script (Member 6)

This script outlines the exact live demonstration flow for the Smart India Hackathon 2026 jury.

---

## 3-Minute Rapid Pitch & Demonstration

### Step 1: Set the Stage (0:00 - 0:45)
- **Presenter Speaks:** 
  > *"Respected judges, in state governance today, government departments are completely siloed. When a farmer applies for an Agriculture Subsidy, they must physically travel to the Revenue office, procure a paper 7/12 land extract, and carry it to the Agriculture office. The citizen is forced to act as the human data bridge. With MAHASync, we present: One Citizen, One Profile, One Platform, Connected Government. MahaSync does not replace government systems; it connects them."*

### Step 2: Show Independent Department Systems (0:45 - 1:15)
- **Action:** Open two browser tabs side-by-side:
  - Tab 1: `http://127.0.0.1:8000/revenue/portal` (Revenue Registry)
  - Tab 2: `http://127.0.0.1:8001/agriculture/portal` (Agriculture Subsidy Registry)
- **Presenter Speaks:**
  > *"Notice that these systems are completely autonomous with separate databases. In the Revenue portal, citizen Rahul (C001) has verified ownership of 2.5 acres of land. But in the Agriculture Department, application A001 is currently PENDING because Agriculture has no direct access to Revenue records."*

### Step 3: Citizen Experience & Explicit DPDP Consent (1:15 - 2:00)
- **Action:** Open Tab 3: `http://127.0.0.1:8082/portal` (MahaSync Citizen Portal).
- **Presenter Speaks:**
  > *"Rahul logs into MahaSync. He sees his active application for Agriculture Subsidy. In strict compliance with India's DPDP Act 2023, MahaSync does not share data in secret. It presents an explicit consent challenge: 'Revenue Department land information is required to verify your Agriculture Subsidy application.'"*
- **Action:** Click **"Allow & Verify Automatically"**.

### Step 4: Live Interoperability & Real-Time Verification (2:00 - 2:45)
- **Action:** Watch the live Stepper update to 100% Completed, then switch to Tab 2 (`http://127.0.0.1:8001/agriculture/portal`) and click "Refresh Data".
- **Presenter Speaks:**
  > *"In under one second: MahaSync queried Revenue API (:8000), the Revenue Adapter standardized the payload into our canonical schema, a LandVerified event was published to our RabbitMQ event bus, and the Agriculture Adapter posted the verified data to Agriculture API (:8001). Notice that application A001 in the Agriculture Department has now flipped from PENDING to VERIFIED in real-time!"*

### Step 5: Audit Trail & Closing (2:45 - 3:00)
- **Action:** Click "Audit Trail & Interoperability" tab on MahaSync.
- **Presenter Speaks:**
  > *"Every single action—consent grant, API fetch, adapter translation, and event publication—is recorded in our immutable audit trail. This is digital governance that works for the citizen. Thank you!"*

---

## 5-Minute Technical Deep Dive (Extended Q&A)

1. **Architecture Overview:** Show [`architecture.md`](file:///d:/Yash/VS%20CODE/nexyra/documentation/diagrams/architecture.md) explaining the canonical data model and RabbitMQ topic exchange topology.
2. **Negative Testing / Consent Denial:** Click "Reset Demo State", click "Deny Consent", and show that the workflow safely halts and logs `CONSENT_DENIED` without crash.
3. **MahaMitra AI Assistant:** Open floating drawer, type `"Why is consent required?"`, and demonstrate context-aware DPDP explanations.
4. **Code Inspection:** Walk judges through [`goverment_systems/adapters/`](file:///d:/Yash/VS%20CODE/nexyra/goverment_systems/adapters) and [`backend/services/orchestrator.py`](file:///d:/Yash/VS%20CODE/nexyra/backend/services/orchestrator.py) to prove real algorithmic transformation.
