def convert_mahasync_to_agriculture(data):
    return {
        "applicantId": data["citizenId"],
        "propertyNumber": data["landId"],
        "landArea": data["landArea"],
        "verificationStatus": data["verificationStatus"]
    }