from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

try:
    from .database import create_database, get_land_record, get_all_land_records, reset_database
except ImportError:
    from database import create_database, get_land_record, get_all_land_records, reset_database

app = FastAPI(title="Revenue Department API", description="State Revenue Department Land Records System (Member 3)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_database()


@app.get("/revenue/land/{citizen_id}")
def get_land(citizen_id: str, response: Response = None):
    result = get_land_record(citizen_id)

    if result is None:
        if response:
            response.status_code = 404
        return {"message": "Land record not found", "citizen_id": citizen_id}

    return {
        "citizen_id": result[0],
        "citizen_name": result[1],
        "land_id": result[2],
        "area": result[3],
        "verified": bool(result[4])
    }


@app.get("/revenue/land")
def list_all_land():
    records = get_all_land_records()
    return [
        {
            "citizen_id": r[0],
            "citizen_name": r[1],
            "land_id": r[2],
            "area": r[3],
            "verified": bool(r[4])
        }
        for r in records
    ]


@app.post("/revenue/reset")
def reset_revenue():
    reset_database()
    return {"status": "success", "message": "Revenue Department database reset to initial seed state"}


@app.get("/revenue/portal", response_class=HTMLResponse)
def revenue_portal():
    records = get_all_land_records()
    rows_html = "".join([
        f"""
        <tr class="hover:bg-amber-50/50 transition-colors">
            <td class="px-6 py-4 font-mono font-bold text-amber-900">{r[0]}</td>
            <td class="px-6 py-4 font-semibold text-slate-800">{r[1]}</td>
            <td class="px-6 py-4 font-mono text-slate-600">{r[2]}</td>
            <td class="px-6 py-4 text-slate-700">{r[3]} Acres</td>
            <td class="px-6 py-4">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold {'bg-emerald-100 text-emerald-800' if r[4] else 'bg-rose-100 text-rose-800'}">
                    {'● VERIFIED' if r[4] else '○ NOT VERIFIED'}
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
    <title>Revenue Department Portal - Land Records Division</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Inter', sans-serif; }}</style>
</head>
<body class="bg-slate-100 text-slate-900 min-h-screen">
    <header class="bg-amber-800 text-white shadow-lg border-b-4 border-amber-900">
        <div class="max-w-6xl mx-auto px-6 py-4 flex flex-col md:flex-row justify-between items-center gap-4">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-lg bg-amber-600 border border-amber-400 flex items-center justify-center font-bold text-lg shadow-inner">
                    🏛️
                </div>
                <div>
                    <div class="text-xs tracking-wider uppercase text-amber-200 font-semibold">Government of Maharashtra</div>
                    <h1 class="text-xl font-bold tracking-tight">Revenue & Land Administration Department</h1>
                </div>
            </div>
            <div class="flex items-center gap-2">
                <span class="bg-amber-900/60 text-amber-100 text-xs px-3 py-1.5 rounded-md border border-amber-700 font-mono">
                    Service Port: 8000
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
                <h2 class="text-lg font-bold text-slate-900">Official Land Registry (7/12 Extract Verification)</h2>
                <p class="text-sm text-slate-500">Autonomous departmental database for land ownership and cadastral records.</p>
            </div>
            <div class="flex gap-2">
                <a href="/docs" target="_blank" class="px-3.5 py-1.5 text-xs font-semibold bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg border border-slate-300 transition">
                    Swagger Docs
                </a>
                <button onclick="location.reload()" class="px-3.5 py-1.5 text-xs font-semibold bg-amber-700 hover:bg-amber-800 text-white rounded-lg shadow-sm transition">
                    🔄 Refresh Data
                </button>
            </div>
        </div>

        <div class="bg-white rounded-xl shadow-md border border-slate-200 overflow-hidden mb-8">
            <div class="px-6 py-4 bg-slate-50 border-b border-slate-200 font-semibold text-slate-700 flex justify-between items-center">
                <span>Registered Citizen Land Holdings</span>
                <span class="text-xs font-mono text-slate-400">TABLE: land_records</span>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full text-left text-sm text-slate-600">
                    <thead class="bg-slate-100/75 text-xs uppercase font-semibold text-slate-500 border-b border-slate-200">
                        <tr>
                            <th class="px-6 py-3">Citizen ID</th>
                            <th class="px-6 py-3">Citizen Name</th>
                            <th class="px-6 py-3">Survey / Land ID</th>
                            <th class="px-6 py-3">Cultivable Area</th>
                            <th class="px-6 py-3">Registry Status</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100">
                        {rows_html}
                    </tbody>
                </table>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-amber-50/50 p-5 rounded-xl border border-amber-200">
                <h3 class="font-bold text-amber-900 text-sm mb-2 flex items-center gap-2">
                    <span>⚡</span> Integration Endpoint
                </h3>
                <p class="text-xs text-amber-800 mb-3">MahaSync retrieves authentic land records using citizen identity via secured REST queries:</p>
                <div class="bg-amber-950 text-amber-200 p-3 rounded-lg font-mono text-xs overflow-x-auto">
                    GET /revenue/land/C001
                </div>
            </div>

            <div class="bg-slate-50 p-5 rounded-xl border border-slate-200">
                <h3 class="font-bold text-slate-800 text-sm mb-2">System Architecture Notice</h3>
                <p class="text-xs text-slate-600 leading-relaxed">
                    This Revenue system operates completely independently. It does not share a database with the Agriculture Department or MahaSync. MahaSync connects via data standardization adapters.
                </p>
            </div>
        </div>
    </main>
</body>
</html>"""