from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime


class ServiceResponse(BaseModel):
    id: str
    title: str
    department: str
    category: str
    description: str
    benefit_amount: str
    eligibility: Optional[str] = None
    required_data_source: str
    is_active: bool

    class Config:
        from_attributes = True


class ApplicationCreate(BaseModel):
    service_id: str = "SRV-AGRI-001"
    citizen_id: Optional[str] = "C001"
    department_application_id: Optional[str] = "A001"


class ConsentAction(BaseModel):
    action: str = Field(..., description="'ALLOW' or 'DENY'")
    notes: Optional[str] = None


class ConsentResponse(BaseModel):
    id: str
    application_id: str
    citizen_id: str
    purpose: str
    data_source: str
    data_recipient: str
    status: str
    granted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AuditEventResponse(BaseModel):
    id: int
    application_id: str
    event_type: str
    source: str
    description: str
    status: str
    metadata_json: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True


class ApplicationResponse(BaseModel):
    id: str
    citizen_id: str
    service_id: str
    service_title: Optional[str] = None
    status: str
    department_application_id: Optional[str] = None
    land_id: Optional[str] = None
    land_area: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    consent: Optional[ConsentResponse] = None
    audit_events: List[AuditEventResponse] = []

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    message: str
    citizen_id: Optional[str] = "C001"
    application_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    suggested_actions: List[str] = []
    relevant_scheme: Optional[str] = None
