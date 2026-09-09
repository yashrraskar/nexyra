from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime


class LandVerifiedEvent(BaseModel):
    eventType: str = "LandVerified"
    citizenId: str
    landId: str
    landArea: float
    verificationStatus: str = "VERIFIED"
    source: str = "Revenue"
    applicationId: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: Optional[dict[str, Any]] = None
