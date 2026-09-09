import logging
import httpx
from datetime import datetime
from sqlalchemy.orm import Session

from ..models import Application, ConsentRecord
from ..config import REVENUE_API_URL, AGRICULTURE_API_URL
from .audit import log_audit_event

try:
    from goverment_systems.adapters.revenue_adapter import convert_revenue_to_mahasync
    from goverment_systems.adapters.agriculture_adapter import convert_mahasync_to_agriculture
except ImportError:
    import sys
    from pathlib import Path
    adapters_path = str(Path(__file__).resolve().parent.parent.parent / "goverment_systems" / "adapters")
    if adapters_path not in sys.path:
        sys.path.append(adapters_path)
    from revenue_adapter import convert_revenue_to_mahasync
    from agriculture_adapter import convert_mahasync_to_agriculture

try:
    from rabbitmq.publisher import publish_event
except ImportError:
    import sys
    from pathlib import Path
    rabbit_path = str(Path(__file__).resolve().parent.parent.parent / "rabbitmq")
    if rabbit_path not in sys.path:
        sys.path.append(rabbit_path)
    from publisher import publish_event

logger = logging.getLogger("MahaSync.Orchestrator")


async def execute_interoperability_flow(db: Session, application_id: str, action: str) -> dict:
    """
    Coordinates the end-to-end multi-department data exchange:
    1. Consent Evaluation (Allow / Deny)
    2. Revenue API query
    3. Revenue Adapter standardization
    4. RabbitMQ LandVerified event publishing
    5. Agriculture Adapter transformation & verification posting
    6. Audit trail generation and status finalization
    """
    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise ValueError(f"Application {application_id} not found")

    consent = db.query(ConsentRecord).filter(ConsentRecord.application_id == application_id).first()
    if not consent:
        consent = ConsentRecord(
            id=f"CNS-{application_id}",
            application_id=application_id,
            citizen_id=app.citizen_id,
            purpose="Cross-departmental 7/12 Land Record verification for Agriculture Subsidy",
            status="PENDING"
        )
        db.add(consent)
        db.commit()
        db.refresh(consent)

    # 1. Handle DENY
    if action.upper() == "DENY":
        consent.status = "DENIED"
        app.status = "CONSENT_DENIED"
        db.commit()

        log_audit_event(
            db,
            application_id=application_id,
            event_type="CONSENT_DENIED",
            source="CitizenPortal",
            description=f"Citizen {app.citizen_id} denied consent to share Revenue Department data.",
            status="WARNING"
        )
        return {
            "status": "stopped",
            "reason": "Consent denied by citizen",
            "application_status": app.status
        }

    # 2. Handle ALLOW
    consent.status = "GRANTED"
    consent.granted_at = datetime.utcnow()
    app.status = "CONSENT_GRANTED"
    db.commit()

    log_audit_event(
        db,
        application_id=application_id,
        event_type="CONSENT_GRANTED",
        source="CitizenPortal",
        description=f"Citizen {app.citizen_id} granted explicit consent for 7/12 land record sharing under DPDP Act.",
        metadata={"purpose": consent.purpose, "recipient": consent.data_recipient}
    )

    # 3. Query Revenue Department API
    revenue_url = f"{REVENUE_API_URL}/revenue/land/{app.citizen_id}"
    log_audit_event(
        db,
        application_id=application_id,
        event_type="REVENUE_DATA_REQUESTED",
        source="MahaSyncCore",
        description=f"MahaSync dispatched secured query to Revenue API for citizen {app.citizen_id}."
    )

    raw_revenue_data = None
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            rev_res = await client.get(revenue_url)
            if rev_res.status_code == 200:
                raw_revenue_data = rev_res.json()
            elif rev_res.status_code == 404:
                app.status = "REVENUE_RECORD_NOT_FOUND"
                db.commit()
                log_audit_event(
                    db,
                    application_id=application_id,
                    event_type="REVENUE_RECORD_NOT_FOUND",
                    source="RevenueDepartment",
                    description=f"Revenue department has no land registry record for citizen {app.citizen_id}.",
                    status="FAILED"
                )
                return {"status": "failed", "reason": "Land record not found in Revenue Department"}
        except Exception as e:
            app.status = "REVENUE_SERVICE_UNAVAILABLE"
            db.commit()
            log_audit_event(
                db,
                application_id=application_id,
                event_type="SERVICE_ERROR",
                source="RevenueDepartment",
                description=f"Unable to connect to Revenue API at {revenue_url}: {str(e)}",
                status="ERROR"
            )
            return {"status": "error", "reason": f"Revenue department service unavailable: {str(e)}"}

    if not raw_revenue_data or "citizen_id" not in raw_revenue_data:
        app.status = "REVENUE_DATA_INVALID"
        db.commit()
        return {"status": "failed", "reason": "Invalid response format from Revenue API"}

    log_audit_event(
        db,
        application_id=application_id,
        event_type="REVENUE_DATA_RECEIVED",
        source="RevenueDepartment",
        description=f"Retrieved land parcel {raw_revenue_data.get('land_id')} ({raw_revenue_data.get('area')} Acres) from Revenue registry.",
        metadata=raw_revenue_data
    )

    # 4. Standardize via Revenue Adapter
    mahasync_data = convert_revenue_to_mahasync(raw_revenue_data)
    log_audit_event(
        db,
        application_id=application_id,
        event_type="ADAPTER_STANDARDIZED",
        source="RevenueAdapter",
        description="Standardized departmental data format into canonical MahaSync schema.",
        metadata=mahasync_data
    )

    # 5. Publish LandVerified Event to RabbitMQ
    event_payload = {
        "eventType": "LandVerified",
        "citizenId": mahasync_data["citizenId"],
        "landId": mahasync_data["landId"],
        "landArea": mahasync_data["landArea"],
        "verificationStatus": mahasync_data["verificationStatus"],
        "source": "Revenue",
        "applicationId": application_id,
        "timestamp": datetime.utcnow().isoformat()
    }

    pub_result = await publish_event(event_payload, routing_key="land.verified")
    log_audit_event(
        db,
        application_id=application_id,
        event_type="RABBITMQ_EVENT_PUBLISHED",
        source="RabbitMQEventBus",
        description=f"Published LandVerified event to topic exchange (transport: {pub_result.get('transport')}).",
        metadata=pub_result
    )

    # 6. Agriculture Processing & Verification
    agri_url = f"{AGRICULTURE_API_URL}/agriculture/verify-land"
    agri_payload = convert_mahasync_to_agriculture(mahasync_data)

    log_audit_event(
        db,
        application_id=application_id,
        event_type="AGRICULTURE_SUBMITTED",
        source="AgricultureAdapter",
        description="Converted canonical data to Agriculture Department schema and initiated benefit verification.",
        metadata=agri_payload
    )

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            agri_res = await client.post(agri_url, json=agri_payload)
            if agri_res.status_code == 200:
                agri_result = agri_res.json()
                log_audit_event(
                    db,
                    application_id=application_id,
                    event_type="AGRICULTURE_VERIFIED",
                    source="AgricultureDepartment",
                    description=f"Agriculture Department confirmed eligibility for application {app.department_application_id}. Status: VERIFIED.",
                    metadata=agri_result
                )

                # Finalize application status
                app.status = "VERIFIED"
                app.land_id = mahasync_data["landId"]
                app.land_area = float(mahasync_data["landArea"])
                db.commit()

                log_audit_event(
                    db,
                    application_id=application_id,
                    event_type="APPLICATION_FINALIZED",
                    source="MahaSyncCore",
                    description=f"End-to-end inter-departmental verification completed successfully without manual citizen intervention.",
                    status="SUCCESS"
                )

                return {
                    "status": "success",
                    "application_id": application_id,
                    "citizen_id": app.citizen_id,
                    "application_status": app.status,
                    "land_id": app.land_id,
                    "land_area": app.land_area,
                    "agriculture_status": agri_result.get("status", "Verified")
                }
            else:
                app.status = "AGRICULTURE_VERIFICATION_FAILED"
                db.commit()
                return {"status": "failed", "reason": f"Agriculture Department rejected verification: {agri_res.text}"}
        except Exception as e:
            app.status = "AGRICULTURE_SERVICE_UNAVAILABLE"
            db.commit()
            return {"status": "error", "reason": f"Failed to contact Agriculture service: {str(e)}"}
