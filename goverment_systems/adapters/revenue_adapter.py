def convert_revenue_to_mahasync(data):
    return {
        "citizenId": data["citizen_id"],
        "landId": data["land_id"],
        "landArea": data["area"],
        "verificationStatus": "VERIFIED" if data["verified"] else "NOT_VERIFIED"
    }