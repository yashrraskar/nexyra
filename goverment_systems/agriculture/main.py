from fastapi import FastAPI
from models import LandVerification
from database import create_database, verify_land

app = FastAPI(title="Agriculture Department API")


create_database()


@app.post("/agriculture/verify-land")
def verify_land_record(data: LandVerification):

    result = verify_land(data.citizen_id)

    return {
        "citizen_id": result[0],
        "land_verified": bool(result[1]),
        "status": result[2]
    }