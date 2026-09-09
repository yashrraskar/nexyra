from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid

from ...database import get_db
from ...models import Application, Service, ConsentRecord, AuditEvent, Citizen
from ...schemas import (
    ApplicationCreate,
    ApplicationResponse,
    ConsentAction,
    AuditEventResponse
)
from ...services.audit import log_audit_event
from ...services.orchestrator import execute_interoperability_flow

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.get("", response_model=List[ApplicationResponse])
def list_applications(
    citizen_id: Optional[str] = "C001",
    db: Session = Depends(get_db)
):
    """Retrieves all applications for the authenticated citizen."""
    apps = db.query(Application).filter(Application.citizen_id == citizen_id).all()
    # Populate service titles
    for app in apps:
        if app.service:
            app.service_title = app.service.title
    return apps


@router.post("", response_model=ApplicationResponse, status_code=201)
def create_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db)
):
    """Creates a new application and initializes pending consent."""
    service = db.query(Service).filter(Service.id == payload.service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail=f"Service {payload.service_id} not found")

    citizen = db.query(Citizen).filter(Citizen.id == payload.citizen_id).first()
    if not citizen:
        # Create citizen record if first time
        citizen = Citizen(id=payload.citizen_id, name="Rahul Patil")
        db.add(citizen)
        db.commit()

    app_id = f"APP-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"
    new_app = Application(
        id=app_id,
        citizen_id=payload.citizen_id,
        service_id=payload.service_id,
        status="CONSENT_PENDING",
        department_application_id=payload.department_application_id or "A001"
    )
    db.add(new_app)
    db.commit()

    # Create associated consent record
    consent = ConsentRecord(
        id=f"CNS-{app_id}",
        application_id=app_id,
        citizen_id=payload.citizen_id,
        purpose=f"Automated verification of 7/12 Land Records with Revenue Department for {service.title}",
        data_source="Revenue Department",
        data_recipient="Department of Agriculture",
        status="PENDING"
    )
    db.add(consent)
    db.commit()

    # Log audit event
    log_audit_event(
        db,
        application_id=app_id,
        event_type="APPLICATION_SUBMITTED",
        source="CitizenPortal",
        description=f"Citizen {payload.citizen_id} initiated application for {service.title}."
    )

    db.refresh(new_app)
    new_app.service_title = service.title
    return new_app


@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(application_id: str, db: Session = Depends(get_db)):
    """Fetches application details, consent state, and complete audit trail."""
    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail=f"Application {application_id} not found")
    if app.service:
        app.service_title = app.service.title
    return app


@router.get("/{application_id}/status")
def get_application_status(application_id: str, db: Session = Depends(get_db)):
    """Lightweight endpoint returning current status and land verification details."""
    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail=f"Application {application_id} not found")
    return {
        "application_id": app.id,
        "citizen_id": app.citizen_id,
        "status": app.status,
        "department_application_id": app.department_application_id,
        "land_id": app.land_id,
        "land_area": app.land_area,
        "is_verified": app.status == "VERIFIED"
    }


@router.get("/{application_id}/events", response_model=List[AuditEventResponse])
def get_application_events(application_id: str, db: Session = Depends(get_db)):
    """Returns chronological audit trail events for timeline visualization."""
    events = (
        db.query(AuditEvent)
        .filter(AuditEvent.application_id == application_id)
        .order_by(AuditEvent.timestamp.asc())
        .all()
    )
    return events


@router.post("/{application_id}/consent")
async def process_consent(
    application_id: str,
    payload: ConsentAction,
    db: Session = Depends(get_db)
):
    """
    Submits citizen consent decision (ALLOW or DENY).
    If ALLOW, triggers the complete interoperability orchestrator:
    Revenue query -> Adapter standardization -> RabbitMQ event -> Agriculture verification.
    """
    if payload.action.upper() not in ["ALLOW", "DENY"]:
        raise HTTPException(status_code=400, detail="Action must be 'ALLOW' or 'DENY'")

    result = await execute_interoperability_flow(db, application_id, payload.action)
    return result
