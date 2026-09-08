from pydantic import BaseModel


class LandVerification(BaseModel):
    citizen_id: str
    land_id: str
    area: float
    verified: bool