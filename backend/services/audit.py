import json
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import AuditEvent

logger = logging.getLogger("MahaSync.AuditTrail")


def log_audit_event(
    db: Session,
    application_id: str,
    event_type: str,
    source: str,
    description: str,
    status: str = "SUCCESS",
    metadata: dict = None
) -> AuditEvent:
    """
    Appends an event record to the application's audit trail.
    Ensures complete traceability across all integration steps.
    """
    event = AuditEvent(
        application_id=application_id,
        event_type=event_type,
        source=source,
        description=description,
        status=status,
        metadata_json=json.dumps(metadata) if metadata else None,
        timestamp=datetime.utcnow()
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    logger.info(f"[AUDIT] [{source}] [{event_type}] App: {application_id} -> {description}")
    return event
