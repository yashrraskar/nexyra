from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

try:
    from .models import LandVerification
    from .database import (
        create_database,
        verify_land,
        get_application,
        get_application_by_citizen,
        get_all_applications,
        reset_database
    )
except ImportError:
    from models import LandVerification
    from database import (
        create_database,
        verify_land,
        get_application,
        get_application_by_citizen,
        get_all_applications,
        reset_database
    )

app = FastAPI(title="Agriculture Department API", description="State Department of Agriculture Schemes & Subsidies (Member 3)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_database()


@app.post("/agriculture/verify-land")
def verify_land_record(data: LandVerification, response: Response = None):
    result = verify_land(data.citizen_id)

    if result is None:
        if response:
            response.status_code = 404
        return {
            "error": "Subsidy application not found for citizen",
            "citizen_id": data.citizen_id,
            "land_verified": False,
            "status": "NotFound"
        }

    return {
        "citizen_id": result[0],
        "land_verified": bool(result[1]),
        "status": result[2],
        "application_id": result[3] if len(result) > 3 else "A001",
        "subsidy_type": result[4] if len(result) > 4 else "Agriculture Subsidy"
    }


@app.get("/agriculture/applications")
def list_applications():
    records = get_all_applications()
    return [
        {
            "application_id": r[0],
            "citizen_id": r[1],
            "subsidy_type": r[2],
            "land_verified": bool(r[3]),
            "status": r[4]
        }
        for r in records
    ]


@app.get("/agriculture/applications/{application_id}")
def get_single_application(application_id: str, response: Response = None):
    result = get_application(application_id)
    if result is None:
        if response:
            response.status_code = 404
        return {"message": "Application not found", "application_id": application_id}

    return {
        "application_id": result[0],
        "citizen_id": result[1],
        "subsidy_type": result[2],
        "land_verified": bool(result[3]),
        "status": result[4]
    }


@app.get("/agriculture/applications/citizen/{citizen_id}")
def get_citizen_application(citizen_id: str, response: Response = None):
    result = get_application_by_citizen(citizen_id)
    if result is None:
        if response:
            response.status_code = 404
        return {"message": "No application found for citizen", "citizen_id": citizen_id}

    return {
        "application_id": result[0],
        "citizen_id": result[1],
        "subsidy_type": result[2],
        "land_verified": bool(result[3]),
        "status": result[4]
    }


@app.post("/agriculture/reset")
def reset_agriculture():
    reset_database()
    return {"status": "success", "message": "Agriculture Department database reset to initial seed state"}


@app.get("/agriculture/portal", response_class=HTMLResponse)
def agriculture_portal():
    records = get_all_applications()
    rows_html = "".join([
        f"""
        <tr class="hover:bg-emerald-50/50 transition-colors">
            <td class="px-6 py-4 font-mono font-bold text-emerald-900">{r[0]}</td>
            <td class="px-6 py-4 font-mono text-slate-700">{r[1]}</td>
            <td class="px-6 py-4 font-medium text-slate-800">{r[2]}</td>
            <td class="px-6 py-4">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold {'bg-emerald-100 text-emerald-800' if r[3] else 'bg-amber-100 text-amber-800'}">
                    {'● VERIFIED' if r[3] else '⏳ PENDING'}
                </span>
            </td>
            <td class="px-6 py-4">
                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold {'bg-emerald-600 text-white shadow-sm' if r[4] == 'Verified' else 'bg-slate-200 text-slate-700'}">
                    {r[4]}
                </span>
            </td>
        </tr>
        """
        for r in records
    ])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agriculture Department Portal - Farmer Subsidy Management</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Inter', sans-serif; }}</style>
</head>
<body class="bg-slate-100 text-slate-900 min-h-screen">
    <header class="bg-emerald-800 text-white shadow-lg border-b-4 border-emerald-900">
        <div class="max-w-6xl mx-auto px-6 py-4 flex flex-col md:flex-row justify-between items-center gap-4">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-lg bg-emerald-600 border border-emerald-400 flex items-center justify-center font-bold text-lg shadow-inner">
                    🌾
                </div>
                <div>
                    <div class="text-xs tracking-wider uppercase text-emerald-200 font-semibold">Government of Maharashtra</div>
                    <h1 class="text-xl font-bold tracking-tight">Department of Agriculture & Farmer Welfare</h1>
                </div>
            </div>
            <div class="flex items-center gap-2">
                <span class="bg-emerald-900/60 text-emerald-100 text-xs px-3 py-1.5 rounded-md border border-emerald-700 font-mono">
                    Service Port: 8001
                </span>
                <span class="bg-emerald-500/20 text-emerald-300 text-xs px-3 py-1.5 rounded-md border border-emerald-500/40 flex items-center gap-1.5 font-medium">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    API Active
                </span>
            </div>
        </div>
    </header>

    <main class="max-w-6xl mx-auto px-6 py-8">
        <div class="mb-6 bg-white p-5 rounded-xl shadow-sm border border-slate-200 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
                <h2 class="text-lg font-bold text-slate-900">Direct Benefit Transfer (DBT) Subsidy Applications</h2>
                <p class="text-sm text-slate-500">Autonomous departmental registry tracking agricultural scheme disbursals.</p>
            </div>
            <div class="flex gap-2">
                <a href="/docs" target="_blank" class="px-3.5 py-1.5 text-xs font-semibold bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg border border-slate-300 transition">
                    Swagger Docs
                </a>
                <button onclick="location.reload()" class="px-3.5 py-1.5 text-xs font-semibold bg-emerald-700 hover:bg-emerald-800 text-white rounded-lg shadow-sm transition">
                    🔄 Refresh Data
                </button>
            </div>
        </div>

        <div class="bg-white rounded-xl shadow-md border border-slate-200 overflow-hidden mb-8">
            <div class="px-6 py-4 bg-slate-50 border-b border-slate-200 font-semibold text-slate-700 flex justify-between items-center">
                <span>Farmer Benefit Applications</span>
                <span class="text-xs font-mono text-slate-400">TABLE: subsidy_applications</span>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full text-left text-sm text-slate-600">
                    <thead class="bg-slate-100/75 text-xs uppercase font-semibold text-slate-500 border-b border-slate-200">
                        <tr>
                            <th class="px-6 py-3">Application ID</th>
                            <th class="px-6 py-3">Citizen ID</th>
                            <th class="px-6 py-3">Scheme / Benefit</th>
                            <th class="px-6 py-3">Land Ownership Status</th>
                            <th class="px-6 py-3">Application Status</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100">
                        {rows_html}
                    </tbody>
                </table>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-emerald-50/50 p-5 rounded-xl border border-emerald-200">
                <h3 class="font-bold text-emerald-900 text-sm mb-2 flex items-center gap-2">
                    <span>⚡</span> Automated Verification Endpoint
                </h3>
                <p class="text-xs text-emerald-800 mb-3">Accepts land verification data received through MahaSync interoperability layer:</p>
                <div class="bg-emerald-950 text-emerald-200 p-3 rounded-lg font-mono text-xs overflow-x-auto">
                    POST /agriculture/verify-land
                </div>
            </div>

            <div class="bg-slate-50 p-5 rounded-xl border border-slate-200">
                <h3 class="font-bold text-slate-800 text-sm mb-2">Independent System Boundary</h3>
                <p class="text-xs text-slate-600 leading-relaxed">
                    The Agriculture Department requires valid land ownership records before approving subsidies. In the legacy manual process, citizens carried physical 7/12 extract certificates. MahaSync performs this automatically with citizen consent.
                </p>
            </div>
        </div>
    </main>
</body>
</html>"""