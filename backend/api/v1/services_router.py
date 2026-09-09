from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ...database import get_db
from ...models import Service
from ...schemas import ServiceResponse

router = APIRouter(prefix="/services", tags=["Services"])


@router.get("", response_model=List[ServiceResponse])
def list_services(db: Session = Depends(get_db)):
    """Returns available government schemes and integration services."""
    services = db.query(Service).filter(Service.is_active == True).all()
    return services


@router.get("/{service_id}", response_model=ServiceResponse)
def get_service(service_id: str, db: Session = Depends(get_db)):
    """Returns details, eligibility, and required data sources for a specific scheme."""
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail=f"Service {service_id} not found")
    return service
