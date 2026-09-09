try:
    import pytest
except ImportError:
    pytest = None
import asyncio
from fastapi.testclient import TestClient

from goverment_systems.revenue.main import app as revenue_app
from goverment_systems.agriculture.main import app as agriculture_app
from goverment_systems.adapters.revenue_adapter import convert_revenue_to_mahasync
from goverment_systems.adapters.agriculture_adapter import convert_mahasync_to_agriculture
from backend.main import app as backend_app
from backend.database import SessionLocal, Base, engine
from backend.models import Application, ConsentRecord, AuditEvent

import httpx
from httpx import ASGITransport

transport_rev = ASGITransport(app=revenue_app)
transport_agri = ASGITransport(app=agriculture_app)

orig_client = httpx.AsyncClient

def mock_async_client(*args, **kwargs):
    mounts = kwargs.get("mounts", {})
    mounts.update({
        "http://127.0.0.1:8000": transport_rev,
        "http://127.0.0.1:8001": transport_agri,
        "http://localhost:8000": transport_rev,
        "http://localhost:8001": transport_agri,
    })
    kwargs["mounts"] = mounts
    return orig_client(*args, **kwargs)

httpx.AsyncClient = mock_async_client

client_rev = TestClient(revenue_app)
client_agri = TestClient(agriculture_app)
client_backend = TestClient(backend_app)


def setup_module():
    """Reset databases prior to running end-to-end tests."""
    from goverment_systems.revenue.database import reset_database as reset_rev
    from goverment_systems.agriculture.database import reset_database as reset_agri
    from backend.main import seed_database
    reset_rev()
    reset_agri()
    seed_database()



def test_revenue_api():
    """Verify Revenue Department API returns accurate land records."""
    # 1. Existing citizen C001
    res = client_rev.get("/revenue/land/C001")
    assert res.status_code == 200
    data = res.json()
    assert data["citizen_id"] == "C001"
    assert data["citizen_name"] == "Rahul"
    assert data["land_id"] == "MH-LAND-101"
    assert data["area"] == 2.5
    assert data["verified"] is True

    # 2. Non-existent citizen
    res_404 = client_rev.get("/revenue/land/C999")
    assert res_404.status_code == 404
    assert "not found" in res_404.json()["message"].lower()


def test_agriculture_api_initial_state():
    """Verify Agriculture Department application A001 begins in Pending status."""
    res = client_agri.get("/agriculture/applications/A001")
    assert res.status_code == 200
    data = res.json()
    assert data["application_id"] == "A001"
    assert data["citizen_id"] == "C001"
    assert data["status"] == "Pending"
    assert data["land_verified"] is False


def test_adapters_bidirectional_mapping():
    """Verify Revenue -> MahaSync and MahaSync -> Agriculture adapter transformations."""
    raw_revenue = {
        "citizen_id": "C001",
        "citizen_name": "Rahul",
        "land_id": "MH-LAND-101",
        "area": 2.5,
        "verified": True
    }

    # Revenue -> MahaSync
    mahasync = convert_revenue_to_mahasync(raw_revenue)
    assert mahasync["citizenId"] == "C001"
    assert mahasync["landId"] == "MH-LAND-101"
    assert mahasync["landArea"] == 2.5
    assert mahasync["verificationStatus"] == "VERIFIED"

    # MahaSync -> Agriculture
    agri = convert_mahasync_to_agriculture(mahasync)
    assert agri["applicantId"] == "C001"
    assert agri["propertyNumber"] == "MH-LAND-101"
    assert agri["landArea"] == 2.5
    assert agri["verificationStatus"] == "VERIFIED"


def test_agriculture_api_direct_verification():
    """Verify Agriculture API accepts standardized adapter payload directly."""
    adapter_payload = {
        "applicantId": "C002",
        "propertyNumber": "MH-LAND-102",
        "landArea": 4.0,
        "verificationStatus": "VERIFIED"
    }
    res = client_agri.post("/agriculture/verify-land", json=adapter_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["citizen_id"] == "C002"
    assert data["land_verified"] is True
    assert data["status"] == "Verified"


def test_backend_services_endpoint():
    """Verify MahaSync services catalog listing."""
    res = client_backend.get("/api/v1/services")
    assert res.status_code == 200
    services = res.json()
    assert len(services) >= 1
    agri_service = next((s for s in services if s["id"] == "SRV-AGRI-001"), None)
    assert agri_service is not None
    assert "Agriculture Subsidy" in agri_service["title"]


def test_backend_consent_denial():
    """Verify denying consent halts the workflow safely without error."""
    # Create application
    create_res = client_backend.post("/api/v1/applications", json={
        "service_id": "SRV-AGRI-001",
        "citizen_id": "C001"
    })
    assert create_res.status_code == 201
    app_id = create_res.json()["id"]

    # Submit DENY
    consent_res = client_backend.post(f"/api/v1/applications/{app_id}/consent", json={"action": "DENY"})
    assert consent_res.status_code == 200
    assert consent_res.json()["status"] == "stopped"

    # Verify status is CONSENT_DENIED
    status_res = client_backend.get(f"/api/v1/applications/{app_id}/status")
    assert status_res.json()["status"] == "CONSENT_DENIED"


def test_primary_e2e_demo_flow():
    """
    PRIMARY DEMO SCENARIO:
    1. Rahul C001
    2. Agriculture Subsidy application
    3. Grant Consent (ALLOW)
    4. Revenue Data Retrieved
    5. Adapter Standardization
    6. RabbitMQ Event Published
    7. Agriculture Application Verified
    8. MahaSync status confirmed
    """
    # Create fresh application
    create_res = client_backend.post("/api/v1/applications", json={
        "service_id": "SRV-AGRI-001",
        "citizen_id": "C001",
        "department_application_id": "A001"
    })
    assert create_res.status_code == 201
    app_id = create_res.json()["id"]

    # Grant explicit consent
    consent_res = client_backend.post(f"/api/v1/applications/{app_id}/consent", json={"action": "ALLOW"})
    assert consent_res.status_code == 200
    result = consent_res.json()
    assert result["status"] == "success"
    assert result["application_status"] == "VERIFIED"
    assert result["land_id"] == "MH-LAND-101"
    assert result["land_area"] == 2.5

    # Check audit events
    events_res = client_backend.get(f"/api/v1/applications/{app_id}/events")
    assert events_res.status_code == 200
    events = events_res.json()
    event_types = [e["event_type"] for e in events]
    assert "APPLICATION_SUBMITTED" in event_types
    assert "CONSENT_GRANTED" in event_types
    assert "REVENUE_DATA_REQUESTED" in event_types
    assert "REVENUE_DATA_RECEIVED" in event_types
    assert "ADAPTER_STANDARDIZED" in event_types
    assert "RABBITMQ_EVENT_PUBLISHED" in event_types
    assert "AGRICULTURE_VERIFIED" in event_types
    assert "APPLICATION_FINALIZED" in event_types


def test_ai_assistant():
    """Verify MahaMitra AI Government Assistant answers queries."""
    res = client_backend.post("/api/v1/assistant/chat", json={
        "message": "Why do you need my consent for land records?",
        "citizen_id": "C001"
    })
    assert res.status_code == 200
    data = res.json()
    assert "reply" in data
    assert "dpdp" in data["reply"].lower() or "consent" in data["reply"].lower()


if __name__ == "__main__":
    pytest.main(["-v", __file__])
