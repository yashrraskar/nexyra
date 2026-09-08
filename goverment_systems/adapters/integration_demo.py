import requests

from revenue_adapter import convert_revenue_to_mahasync
from agriculture_adapter import convert_mahasync_to_agriculture


# 1. Get land record from Revenue Department
response = requests.get(
    "http://127.0.0.1:8000/revenue/land/C001"
)

revenue_data = response.json()

print("1. Revenue Department:")
print(revenue_data)


# 2. Convert Revenue format → MahaSync format
mahasync_data = convert_revenue_to_mahasync(revenue_data)

print("\n2. MahaSync Format:")
print(mahasync_data)


# 3. Convert MahaSync format → Agriculture format
agriculture_data = convert_mahasync_to_agriculture(mahasync_data)

print("\n3. Agriculture Format:")
print(agriculture_data)


# 4. Send verified data to Agriculture Department
response = requests.post(
    "http://127.0.0.1:8001/agriculture/verify-land",
    json={
        "citizen_id": mahasync_data["citizenId"],
        "land_id": mahasync_data["landId"],
        "area": mahasync_data["landArea"],
        "verified": mahasync_data["verificationStatus"] == "VERIFIED"
    }
)

print("\n4. Agriculture Department Response:")
print(response.json())