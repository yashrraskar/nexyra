from fastapi import FastAPI
from database import create_database, get_land_record

app = FastAPI(title="Revenue Department API")

create_database()


@app.get("/revenue/land/{citizen_id}")
def get_land(citizen_id: str):
    result = get_land_record(citizen_id)

    if result is None:
        return {"message": "Land record not found"}

    return {
        "citizen_id": result[0],
        "citizen_name": result[1],
        "land_id": result[2],
        "area": result[3],
        "verified": bool(result[4])
    }