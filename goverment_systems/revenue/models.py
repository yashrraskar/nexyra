from pydantic import BaseModel


class LandRecord(BaseModel):
    citizen_id: str
    citizen_name: str
    land_id: str
    area: float
    verified: bool