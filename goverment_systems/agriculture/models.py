from pydantic import BaseModel, model_validator
from typing import Any


class LandVerification(BaseModel):
    citizen_id: str
    land_id: str
    area: float
    verified: bool

    @model_validator(mode="before")
    @classmethod
    def normalize_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # Support both original snake_case and adapter camelCase (applicantId, propertyNumber, landArea, verificationStatus)
            cid = data.get("citizen_id") or data.get("applicantId") or data.get("citizenId")
            lid = data.get("land_id") or data.get("propertyNumber") or data.get("landId")
            ar = data.get("area") or data.get("landArea")
            ver = data.get("verified")
            if ver is None and "verificationStatus" in data:
                ver = (data["verificationStatus"] == "VERIFIED")

            return {
                "citizen_id": str(cid) if cid is not None else "",
                "land_id": str(lid) if lid is not None else "",
                "area": float(ar) if ar is not None else 0.0,
                "verified": bool(ver) if ver is not None else False
            }
        return data