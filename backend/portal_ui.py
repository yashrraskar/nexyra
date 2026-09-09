def get_portal_html() -> str:
    """Returns the complete, high-fidelity single-page Citizen Portal UI."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MAHASync – The Digital Bridge | Citizen Governance Portal</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .font-mono { font-family: 'JetBrains Mono', monospace; }
        .tab-active { border-bottom: 3px solid #2563eb; color: #1d4ed8; font-weight: 600; }
        @keyframes pulse-glow {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.7; transform: scale(1.05); }
        }
        .pulse-live { animation: pulse-glow 2s infinite ease-in-out; }
    </style>
</head>
<body class="bg-slate-50 text-slate-900 min-h-screen flex flex-col">

    <!-- Top Gov Bar -->
    <div class="bg-slate-900 text-slate-300 text-xs px-6 py-1.5 flex justify-between items-center border-b border-slate-800">
        <div class="flex items-center space-x-3">
            <span class="inline-flex items-center gap-1.5 font-medium text-amber-400">
                <span>🇮🇳</span> Government of Maharashtra Interoperability Framework
            </span>
            <span class="text-slate-600">|</span>
            <span class="text-slate-400">Smart India Hackathon 2026 Prototype</span>
        </div>
        <div class="flex items-center space-x-4">
            <span id="sys-status-badge" class="flex items-center gap-1.5 text-emerald-400 font-mono">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                Services Connected
            </span>
            <button onclick="resetAllDemo()" class="text-rose-400 hover:text-rose-300 transition text-[11px] underline">
                🔄 Reset Demo State
            </button>
        </div>
    </div>

    <!-- Main Navigation Header -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-40 shadow-sm">
        <div class="max-w-7xl mx-auto px-6 py-3.5 flex flex-col md:flex-row justify-between items-center gap-4">
            <div class="flex items-center space-x-3.5">
                <div class="w-11 h-11 rounded-xl bg-gradient-to-tr from-blue-700 via-indigo-600 to-blue-500 text-white flex items-center justify-center font-extrabold text-2xl shadow-md shadow-blue-500/20">
                    M
                </div>
                <div>
                    <div class="flex items-center gap-2">
                        <h1 class="text-xl font-extrabold tracking-tight text-slate-900">MAHASync</h1>
                        <span class="bg-blue-100 text-blue-800 text-[11px] font-bold px-2 py-0.5 rounded-full border border-blue-200">
                            The Digital Bridge
                        </span>
                    </div>
                    <p class="text-xs text-slate-500 font-medium">One Citizen • One Profile • One Platform • Connected Government</p>
                </div>
            </div>

            <!-- Citizen Profile / Auth Badge -->
            <div class="flex items-center gap-4">
                <div class="flex items-center gap-3 bg-slate-50 border border-slate-200 px-3.5 py-1.5 rounded-xl">
                    <div class="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-sm">
                        RP
                    </div>
                    <div class="text-left">
                        <div class="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                            Rahul Patil
                            <span class="bg-emerald-100 text-emerald-800 text-[10px] font-semibold px-1.5 py-0.2 rounded font-mono">C001</span>
                        </div>
                        <div class="text-[10px] text-slate-500">Keycloak Verified Citizen</div>
                    </div>
                </div>

                <!-- External Portals Dropdown / Links -->
                <div class="flex items-center gap-2">
                    <a href="http://127.0.0.1:8000/revenue/portal" target="_blank" class="text-xs bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 font-semibold px-2.5 py-1.5 rounded-lg transition flex items-center gap-1" title="View Revenue Department System">
                        🏛️ Revenue Portal
                    </a>
                    <a href="http://127.0.0.1:8001/agriculture/portal" target="_blank" class="text-xs bg-emerald-50 hover:bg-emerald-100 text-emerald-900 border border-emerald-300 font-semibold px-2.5 py-1.5 rounded-lg transition flex items-center gap-1" title="View Agriculture Department System">
                        🌾 Agriculture Portal
                    </a>
                </div>
            </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="max-w-7xl mx-auto px-6 flex space-x-8 text-sm font-medium text-slate-600 border-t border-slate-100">
            <button onclick="switchTab('dashboard')" id="tab-dashboard" class="py-3 px-1 tab-active transition-colors">
                Dashboard
            </button>
            <button onclick="switchTab('services')" id="tab-services" class="py-3 px-1 hover:text-slate-900 transition-colors">
                Service Catalog
            </button>
            <button onclick="switchTab('tracking')" id="tab-tracking" class="py-3 px-1 hover:text-slate-900 transition-colors flex items-center gap-1.5">
                Application Tracking
                <span id="nav-status-badge" class="bg-amber-100 text-amber-800 text-[10px] px-2 py-0.5 rounded-full font-semibold font-mono">
                    Pending
                </span>
            </button>
            <button onclick="switchTab('audit')" id="tab-audit" class="py-3 px-1 hover:text-slate-900 transition-colors">
                Audit Trail & Interoperability
            </button>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-6 py-8 flex-1 w-full">

        <!-- Banner Explaining Concept -->
        <div class="mb-8 bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 text-white p-6 rounded-2xl shadow-xl relative overflow-hidden">
            <div class="absolute right-0 top-0 w-96 h-full opacity-10 bg-repeat pointer-events-none text-9xl">🏛️</div>
            <div class="max-w-3xl relative z-10">
                <div class="inline-flex items-center gap-2 bg-blue-500/20 text-blue-200 border border-blue-400/30 text-xs px-3 py-1 rounded-full font-medium mb-3">
                    <span>⚡</span> Eliminating Fragmented Government Services
                </div>
                <h2 class="text-2xl font-black tracking-tight mb-2">
                    "MahaSync connects independent government systems so citizens do not have to act as the bridge."
                </h2>
                <p class="text-sm text-blue-100/90 leading-relaxed mb-4">
                    In traditional processes, Rahul had to visit the Revenue office, obtain physical 7/12 Land Records, and manually submit them to the Agriculture Department. With MahaSync, with <b>explicit consent</b>, data flows seamlessly through standardized adapters and an asynchronous event bus.
                </p>
                <div class="flex flex-wrap items-center gap-3">
                    <button onclick="triggerConsentFlow()" class="bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold px-4 py-2 rounded-xl text-xs shadow-lg shadow-emerald-500/20 transition flex items-center gap-2">
                        🚀 Run Primary Interoperability Demo (C001)
                    </button>
                    <button onclick="openChatDrawer()" class="bg-white/10 hover:bg-white/20 text-white font-medium px-4 py-2 rounded-xl text-xs backdrop-blur-md transition flex items-center gap-2">
                        💬 Ask MahaMitra AI Assistant
                    </button>
                </div>
            </div>
        </div>

        <!-- TAB 1: DASHBOARD -->
        <div id="view-dashboard" class="space-y-8">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-5">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <div class="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Citizen Profile</div>
                    <div class="text-xl font-bold text-slate-900">Rahul Patil</div>
                    <div class="text-xs text-slate-500 mt-1 font-mono">ID: C001 (Maharashtra)</div>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <div class="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Active Applications</div>
                    <div class="text-xl font-bold text-blue-600">1 Scheme</div>
                    <div class="text-xs text-slate-500 mt-1">Agriculture Subsidy (DBT)</div>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <div class="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Verification Status</div>
                    <div id="stat-status" class="text-xl font-bold text-amber-600">Consent Pending</div>
                    <div class="text-xs text-slate-500 mt-1">Requires 7/12 Land Record</div>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <div class="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Benefit Disbursal</div>
                    <div class="text-xl font-bold text-emerald-600">₹15,000</div>
                    <div class="text-xs text-slate-500 mt-1">Pending Department Approval</div>
                </div>
            </div>

            <!-- Active Application Card -->
            <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
                <div class="px-6 py-4 bg-slate-50/80 border-b border-slate-200 flex justify-between items-center">
                    <div>
                        <h3 class="font-bold text-slate-900">Active Service Application</h3>
                        <p class="text-xs text-slate-500">Real-time status synced with Agriculture Department</p>
                    </div>
                    <span id="app-badge-main" class="bg-amber-100 text-amber-900 border border-amber-300 font-bold px-3 py-1 rounded-full text-xs font-mono">
                        CONSENT_PENDING
                    </span>
                </div>
                <div class="p-6">
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                        <div>
                            <div class="text-xs text-slate-500 font-medium">Scheme Name</div>
                            <div class="text-base font-bold text-slate-800">Agriculture Subsidy Scheme (DBT)</div>
                            <div class="text-xs text-slate-500">Dept of Agriculture & Farmer Welfare</div>
                        </div>
                        <div>
                            <div class="text-xs text-slate-500 font-medium">Application Reference</div>
                            <div class="text-base font-mono font-bold text-slate-800" id="dash-app-id">APP-2026-001</div>
                            <div class="text-xs text-slate-500">Dept Scheme ID: A001</div>
                        </div>
                        <div>
                            <div class="text-xs text-slate-500 font-medium">Data Required</div>
                            <div class="text-base font-bold text-slate-800">7/12 Land Record (Survey MH-LAND-101)</div>
                            <div class="text-xs text-slate-500">Source: State Revenue Department</div>
                        </div>
                    </div>

                    <div id="consent-prompt-box" class="bg-amber-50 border border-amber-200 rounded-xl p-5 mb-6">
                        <div class="flex items-start gap-4">
                            <div class="w-10 h-10 rounded-xl bg-amber-500 text-white flex items-center justify-center font-bold text-xl flex-shrink-0">
                                ⚖️
                            </div>
                            <div class="flex-1">
                                <h4 class="font-bold text-amber-950 text-sm">Citizen Consent Required (DPDP Act 2023)</h4>
                                <p class="text-xs text-amber-900 mt-1 leading-relaxed">
                                    "Revenue Department land information is required to verify your Agriculture Subsidy application. By granting consent, MahaSync will securely fetch your land parcel (2.5 Acres) from the Revenue Registry and verify your subsidy application without manual paperwork."
                                </p>
                                <div class="mt-4 flex items-center gap-3">
                                    <button onclick="submitConsent('ALLOW')" class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-4 py-2 rounded-lg text-xs shadow-sm transition">
                                        ✓ Allow & Verify Automatically
                                    </button>
                                    <button onclick="submitConsent('DENY')" class="bg-slate-200 hover:bg-slate-300 text-slate-800 font-semibold px-4 py-2 rounded-lg text-xs transition">
                                        ✕ Deny Consent
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div id="verified-success-box" class="hidden bg-emerald-50 border border-emerald-200 rounded-xl p-5 mb-6">
                        <div class="flex items-center gap-4">
                            <div class="w-10 h-10 rounded-xl bg-emerald-600 text-white flex items-center justify-center font-bold text-xl flex-shrink-0">
                                ✓
                            </div>
                            <div class="flex-1">
                                <h4 class="font-bold text-emerald-950 text-sm">Application Fully Verified Across Departments!</h4>
                                <p class="text-xs text-emerald-900 mt-0.5">
                                    Land parcel <b id="verified-land-id">MH-LAND-101</b> (<span id="verified-area">2.5</span> Acres) verified via Revenue Department and confirmed in Agriculture Department system A001.
                                </p>
                            </div>
                            <button onclick="switchTab('tracking')" class="bg-emerald-700 hover:bg-emerald-800 text-white font-semibold px-4 py-2 rounded-lg text-xs transition">
                                View Full Timeline →
                            </button>
                        </div>
                    </div>

                    <div class="flex justify-between items-center text-xs text-slate-500 pt-2 border-t border-slate-100">
                        <span>Submitted on 10 Sep 2026</span>
                        <button onclick="switchTab('tracking')" class="text-blue-600 font-semibold hover:underline">
                            Track Detailed Interoperability Steps →
                        </button>
                    </div>
                </div>
            </div>

            <!-- Interoperability Comparison -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-rose-50/70 border border-rose-200 rounded-2xl p-6">
                    <div class="flex items-center gap-2 text-rose-800 font-bold text-sm mb-3">
                        <span>❌</span> WITHOUT MAHASync (Legacy Citizen Burden)
                    </div>
                    <ul class="text-xs text-rose-950 space-y-2.5">
                        <li class="flex items-start gap-2">
                            <span class="font-bold">•</span>
                            <span>Citizen travels to Taluk / Revenue office to apply for 7/12 extract certificate.</span>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="font-bold">•</span>
                            <span>Citizen physically takes paper certificate to Agriculture office.</span>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="font-bold">•</span>
                            <span>Manual officer verification introduces weeks of delays and human error.</span>
                        </li>
                    </ul>
                </div>

                <div class="bg-emerald-50/70 border border-emerald-200 rounded-2xl p-6">
                    <div class="flex items-center gap-2 text-emerald-800 font-bold text-sm mb-3">
                        <span>✅</span> WITH MAHASync (The Digital Bridge)
                    </div>
                    <ul class="text-xs text-emerald-950 space-y-2.5">
                        <li class="flex items-start gap-2">
                            <span class="font-bold">•</span>
                            <span>One login, unified citizen profile with Keycloak authenticated identity.</span>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="font-bold">•</span>
                            <span>Explicit consent granted digitally in 1 second under DPDP Act.</span>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="font-bold">•</span>
                            <span>Adapters standardize payloads; RabbitMQ event bus reliably syncs Agriculture system in milliseconds.</span>
                        </li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- TAB 2: SERVICE CATALOG -->
        <div id="view-services" class="hidden space-y-6">
            <div>
                <h3 class="text-lg font-bold text-slate-900">Integrated Government Schemes</h3>
                <p class="text-xs text-slate-500">Discover and apply for citizen services without repeated documentation</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6" id="services-grid">
                <!-- Dynamically loaded -->
            </div>
        </div>

        <!-- TAB 3: APPLICATION TRACKING & TIMELINE -->
        <div id="view-tracking" class="hidden space-y-8">
            <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
                <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-200 pb-5 mb-6">
                    <div>
                        <div class="flex items-center gap-2">
                            <h3 class="text-lg font-bold text-slate-900">Application Progress Stepper</h3>
                            <span id="tracker-status-pill" class="bg-amber-100 text-amber-800 text-xs font-bold px-2.5 py-0.5 rounded-full font-mono">
                                In Progress
                            </span>
                        </div>
                        <p class="text-xs text-slate-500 mt-1">
                            Application Ref: <span class="font-mono font-bold text-slate-700" id="track-app-ref">APP-2026-001</span> | Service: Agriculture Subsidy Scheme
                        </p>
                    </div>
                    <button onclick="refreshApplicationStatus()" class="text-xs font-semibold bg-slate-100 hover:bg-slate-200 text-slate-700 px-3 py-1.5 rounded-lg border border-slate-300 transition">
                        🔄 Refresh Tracker
                    </button>
                </div>

                <!-- 6-Stage Interoperability Stepper -->
                <div class="relative mb-10">
                    <div class="hidden md:block absolute top-1/2 left-0 right-0 h-1 bg-slate-200 -translate-y-1/2 z-0"></div>
                    <div class="grid grid-cols-1 md:grid-cols-6 gap-4 relative z-10" id="stepper-container">
                        <!-- Step 1 -->
                        <div class="bg-white p-3 rounded-xl border border-slate-200 text-center" id="step-1">
                            <div class="w-8 h-8 mx-auto rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-xs mb-2">1</div>
                            <div class="text-xs font-bold text-slate-800">Application Submitted</div>
                            <div class="text-[10px] text-slate-500 mt-0.5">Citizen Portal</div>
                        </div>
                        <!-- Step 2 -->
                        <div class="bg-white p-3 rounded-xl border border-slate-200 text-center" id="step-2">
                            <div class="w-8 h-8 mx-auto rounded-full bg-slate-200 text-slate-600 flex items-center justify-center font-bold text-xs mb-2">2</div>
                            <div class="text-xs font-bold text-slate-800">Consent Granted</div>
                            <div class="text-[10px] text-slate-500 mt-0.5">DPDP Consent</div>
                        </div>
                        <!-- Step 3 -->
                        <div class="bg-white p-3 rounded-xl border border-slate-200 text-center" id="step-3">
                            <div class="w-8 h-8 mx-auto rounded-full bg-slate-200 text-slate-600 flex items-center justify-center font-bold text-xs mb-2">3</div>
                            <div class="text-xs font-bold text-slate-800">Revenue Data Fetched</div>
                            <div class="text-[10px] text-slate-500 mt-0.5">Revenue Dept :8000</div>
                        </div>
                        <!-- Step 4 -->
                        <div class="bg-white p-3 rounded-xl border border-slate-200 text-center" id="step-4">
                            <div class="w-8 h-8 mx-auto rounded-full bg-slate-200 text-slate-600 flex items-center justify-center font-bold text-xs mb-2">4</div>
                            <div class="text-xs font-bold text-slate-800">Data Standardized</div>
                            <div class="text-[10px] text-slate-500 mt-0.5">Revenue Adapter</div>
                        </div>
                        <!-- Step 5 -->
                        <div class="bg-white p-3 rounded-xl border border-slate-200 text-center" id="step-5">
                            <div class="w-8 h-8 mx-auto rounded-full bg-slate-200 text-slate-600 flex items-center justify-center font-bold text-xs mb-2">5</div>
                            <div class="text-xs font-bold text-slate-800">Event Published</div>
                            <div class="text-[10px] text-slate-500 mt-0.5">RabbitMQ Broker</div>
                        </div>
                        <!-- Step 6 -->
                        <div class="bg-white p-3 rounded-xl border border-slate-200 text-center" id="step-6">
                            <div class="w-8 h-8 mx-auto rounded-full bg-slate-200 text-slate-600 flex items-center justify-center font-bold text-xs mb-2">6</div>
                            <div class="text-xs font-bold text-slate-800">Application Verified</div>
                            <div class="text-[10px] text-slate-500 mt-0.5">Agriculture Dept :8001</div>
                        </div>
                    </div>
                </div>

                <!-- Verification Data Display -->
                <div id="verified-details-card" class="hidden bg-slate-50 rounded-xl border border-slate-200 p-5">
                    <h4 class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">Interoperability Verification Record</h4>
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
                        <div>
                            <span class="text-slate-500 block">Citizen ID:</span>
                            <span class="font-mono font-bold text-slate-800">C001 (Rahul)</span>
                        </div>
                        <div>
                            <span class="text-slate-500 block">Survey Parcel ID:</span>
                            <span class="font-mono font-bold text-slate-800" id="card-land-id">MH-LAND-101</span>
                        </div>
                        <div>
                            <span class="text-slate-500 block">Cultivable Area:</span>
                            <span class="font-bold text-slate-800" id="card-land-area">2.5 Acres</span>
                        </div>
                        <div>
                            <span class="text-slate-500 block">Agriculture Status:</span>
                            <span class="font-bold text-emerald-600 font-mono">VERIFIED (A001)</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 4: AUDIT TRAIL & SYSTEM LOGS -->
        <div id="view-audit" class="hidden space-y-6">
            <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
                <div class="px-6 py-4 bg-slate-50 border-b border-slate-200 flex justify-between items-center">
                    <div>
                        <h3 class="font-bold text-slate-900">Application Audit Trail</h3>
                        <p class="text-xs text-slate-500">Traceable event history across citizen actions and departmental systems</p>
                    </div>
                    <span class="text-xs font-mono text-slate-500">Immutable Event Log</span>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs text-slate-600">
                        <thead class="bg-slate-100 text-slate-500 uppercase font-semibold border-b border-slate-200">
                            <tr>
                                <th class="px-6 py-3">Timestamp</th>
                                <th class="px-6 py-3">Source</th>
                                <th class="px-6 py-3">Event Type</th>
                                <th class="px-6 py-3">Description</th>
                                <th class="px-6 py-3">Status</th>
                            </tr>
                        </thead>
                        <tbody id="audit-table-body" class="divide-y divide-slate-100 font-mono">
                            <!-- Dynamically loaded -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

    </main>

    <!-- Floating MahaMitra AI Assistant Drawer -->
    <div id="ai-drawer" class="fixed bottom-6 right-6 z-50 flex flex-col items-end">
        <!-- Chat Panel -->
        <div id="ai-panel" class="hidden w-96 bg-white rounded-2xl shadow-2xl border border-slate-200 overflow-hidden mb-3 flex flex-col transition-all h-[480px]">
            <div class="bg-gradient-to-r from-blue-700 to-indigo-700 text-white px-5 py-3.5 flex justify-between items-center">
                <div class="flex items-center gap-2.5">
                    <span class="text-xl">🤖</span>
                    <div>
                        <div class="font-bold text-sm">MahaMitra AI Guide</div>
                        <div class="text-[10px] text-blue-200">Government Interoperability Assistant</div>
                    </div>
                </div>
                <button onclick="toggleChat()" class="text-white hover:text-slate-200 text-sm font-bold">✕</button>
            </div>
            <!-- Messages Container -->
            <div id="ai-messages" class="flex-1 p-4 overflow-y-auto space-y-3 text-xs">
                <div class="bg-slate-100 p-3 rounded-xl rounded-tl-none text-slate-800">
                    Namaskar Rahul! I am MahaMitra, your digital governance guide. Ask me about Agriculture Subsidy eligibility, DPDP consent, or how your 7/12 land records are verified!
                </div>
            </div>
            <!-- Suggestions -->
            <div id="ai-suggestions" class="px-4 py-2 bg-slate-50 border-t border-slate-100 flex flex-wrap gap-1.5 text-[10px]">
                <button onclick="askPreset('Why is consent required?')" class="bg-blue-50 text-blue-700 border border-blue-200 px-2 py-1 rounded-md hover:bg-blue-100">Why consent?</button>
                <button onclick="askPreset('How does land verification work?')" class="bg-blue-50 text-blue-700 border border-blue-200 px-2 py-1 rounded-md hover:bg-blue-100">Land verification</button>
                <button onclick="askPreset('What is the status of my application?')" class="bg-blue-50 text-blue-700 border border-blue-200 px-2 py-1 rounded-md hover:bg-blue-100">Application status</button>
            </div>
            <!-- Input -->
            <div class="p-3 bg-white border-t border-slate-200 flex gap-2">
                <input id="ai-input" type="text" placeholder="Ask anything about MahaSync..." class="flex-1 text-xs border border-slate-300 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-600" onkeydown="if(event.key==='Enter') sendChatMessage()">
                <button onclick="sendChatMessage()" class="bg-blue-600 hover:bg-blue-700 text-white font-bold px-3 py-2 rounded-lg text-xs transition">
                    Send
                </button>
            </div>
        </div>

        <!-- Launcher Button -->
        <button onclick="toggleChat()" class="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-3.5 rounded-full shadow-lg hover:shadow-xl hover:scale-105 transition flex items-center gap-2 font-semibold text-xs border border-blue-400">
            <span class="text-xl">🤖</span>
            <span>MahaMitra AI Guide</span>
        </button>
    </div>

    <!-- Frontend Script -->
    <script>
        const API_BASE = "";
        let currentAppId = "APP-2026-001";

        async function switchTab(tab) {
            ['dashboard', 'services', 'tracking', 'audit'].forEach(t => {
                document.getElementById('view-' + t).classList.add('hidden');
                document.getElementById('tab-' + t).classList.remove('tab-active');
            });
            document.getElementById('view-' + tab).classList.remove('hidden');
            document.getElementById('tab-' + tab).classList.add('tab-active');

            if (tab === 'services') loadServices();
            if (tab === 'tracking') refreshApplicationStatus();
            if (tab === 'audit') loadAuditEvents();
        }

        async function refreshApplicationStatus() {
            try {
                const res = await fetch(`${API_BASE}/api/v1/applications/${currentAppId}`);
                if (!res.ok) return;
                const data = await res.json();
                updateUIState(data);
            } catch (err) {
                console.error("Failed to fetch app status", err);
            }
        }

        function updateUIState(data) {
            const isVerified = data.status === "VERIFIED";
            const isDenied = data.status === "CONSENT_DENIED";

            // Status badges
            const badge = document.getElementById('app-badge-main');
            const navBadge = document.getElementById('nav-status-badge');
            const statStatus = document.getElementById('stat-status');
            const pill = document.getElementById('tracker-status-pill');

            if (isVerified) {
                badge.className = "bg-emerald-100 text-emerald-900 border border-emerald-300 font-bold px-3 py-1 rounded-full text-xs font-mono";
                badge.innerText = "VERIFIED";
                navBadge.className = "bg-emerald-100 text-emerald-800 text-[10px] px-2 py-0.5 rounded-full font-semibold font-mono";
                navBadge.innerText = "Verified";
                statStatus.className = "text-xl font-bold text-emerald-600";
                statStatus.innerText = "Verified (A001)";
                pill.className = "bg-emerald-100 text-emerald-800 text-xs font-bold px-2.5 py-0.5 rounded-full font-mono";
                pill.innerText = "Completed";

                document.getElementById('consent-prompt-box').classList.add('hidden');
                document.getElementById('verified-success-box').classList.remove('hidden');
                document.getElementById('verified-details-card').classList.remove('hidden');

                if (data.land_id) {
                    document.getElementById('verified-land-id').innerText = data.land_id;
                    document.getElementById('card-land-id').innerText = data.land_id;
                }
                if (data.land_area) {
                    document.getElementById('verified-area').innerText = data.land_area;
                    document.getElementById('card-land-area').innerText = data.land_area + " Acres";
                }

                // Highlight all 6 steps in stepper
                for (let i = 1; i <= 6; i++) {
                    const el = document.getElementById('step-' + i);
                    if (el) {
                        el.className = "bg-emerald-50 p-3 rounded-xl border border-emerald-300 text-center";
                        el.querySelector('div').className = "w-8 h-8 mx-auto rounded-full bg-emerald-600 text-white flex items-center justify-center font-bold text-xs mb-2";
                    }
                }
            } else if (isDenied) {
                badge.className = "bg-rose-100 text-rose-900 border border-rose-300 font-bold px-3 py-1 rounded-full text-xs font-mono";
                badge.innerText = "CONSENT_DENIED";
                navBadge.innerText = "Denied";
                statStatus.innerText = "Consent Denied";
                statStatus.className = "text-xl font-bold text-rose-600";
            } else {
                badge.className = "bg-amber-100 text-amber-900 border border-amber-300 font-bold px-3 py-1 rounded-full text-xs font-mono";
                badge.innerText = "CONSENT_PENDING";
                navBadge.innerText = "Pending";
                statStatus.innerText = "Consent Pending";
                statStatus.className = "text-xl font-bold text-amber-600";
                document.getElementById('consent-prompt-box').classList.remove('hidden');
                document.getElementById('verified-success-box').classList.add('hidden');
                document.getElementById('verified-details-card').classList.add('hidden');

                // Reset stepper to step 1
                for (let i = 2; i <= 6; i++) {
                    const el = document.getElementById('step-' + i);
                    if (el) {
                        el.className = "bg-white p-3 rounded-xl border border-slate-200 text-center";
                        el.querySelector('div').className = "w-8 h-8 mx-auto rounded-full bg-slate-200 text-slate-600 flex items-center justify-center font-bold text-xs mb-2";
                    }
                }
            }
        }

        async function submitConsent(action) {
            try {
                const res = await fetch(`${API_BASE}/api/v1/applications/${currentAppId}/consent`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: action })
                });
                const result = await res.json();
                await refreshApplicationStatus();
                if (action === 'ALLOW') {
                    switchTab('tracking');
                }
            } catch (err) {
                alert("Error submitting consent: " + err);
            }
        }

        async function triggerConsentFlow() {
            await submitConsent('ALLOW');
        }

        async function resetAllDemo() {
            try {
                await fetch(`${API_BASE}/api/v1/reset-demo`, { method: 'POST' });
                await refreshApplicationStatus();
                switchTab('dashboard');
                alert("Demo state successfully reset to initial PENDING state across all services.");
            } catch (err) {
                alert("Error resetting demo: " + err);
            }
        }

        async function loadServices() {
            const grid = document.getElementById('services-grid');
            grid.innerHTML = "<div class='text-xs text-slate-500'>Loading service catalog...</div>";
            try {
                const res = await fetch(`${API_BASE}/api/v1/services`);
                const services = await res.json();
                grid.innerHTML = services.map(s => `
                    <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col justify-between hover:shadow-md transition">
                        <div>
                            <div class="flex justify-between items-start mb-2">
                                <span class="bg-blue-50 text-blue-700 text-[10px] font-bold px-2 py-0.5 rounded uppercase font-mono">${s.category}</span>
                                <span class="text-xs font-bold text-emerald-600">${s.benefit_amount}</span>
                            </div>
                            <h4 class="font-bold text-slate-900 text-base mb-1">${s.title}</h4>
                            <p class="text-xs text-slate-500 mb-4 leading-relaxed">${s.description}</p>
                            <div class="bg-slate-50 p-3 rounded-xl border border-slate-200 text-xs mb-4">
                                <span class="text-[10px] text-slate-400 uppercase font-semibold block">Required Interoperability:</span>
                                <span class="font-medium text-slate-700">${s.required_data_source}</span>
                            </div>
                        </div>
                        <button onclick="switchTab('dashboard')" class="w-full bg-slate-900 hover:bg-blue-600 text-white font-semibold py-2 rounded-xl text-xs transition">
                            ${s.id === 'SRV-AGRI-001' ? 'View Active Application' : 'Apply via MahaSync'}
                        </button>
                    </div>
                `).join('');
            } catch (e) {
                grid.innerHTML = "<div class='text-xs text-rose-500'>Failed to load services</div>";
            }
        }

        async function loadAuditEvents() {
            const tbody = document.getElementById('audit-table-body');
            tbody.innerHTML = "<tr><td colspan='5' class='px-6 py-4 text-slate-400'>Loading audit trail...</td></tr>";
            try {
                const res = await fetch(`${API_BASE}/api/v1/applications/${currentAppId}/events`);
                const events = await res.json();
                tbody.innerHTML = events.map(e => `
                    <tr class="hover:bg-slate-50 transition">
                        <td class="px-6 py-3 font-mono text-slate-500 whitespace-nowrap">${new Date(e.timestamp).toLocaleTimeString()}</td>
                        <td class="px-6 py-3">
                            <span class="bg-slate-100 text-slate-700 px-2 py-0.5 rounded text-[11px] font-semibold">${e.source}</span>
                        </td>
                        <td class="px-6 py-3 font-bold text-slate-800">${e.event_type}</td>
                        <td class="px-6 py-3 text-slate-600 font-sans">${e.description}</td>
                        <td class="px-6 py-3">
                            <span class="px-2 py-0.5 rounded text-[10px] font-bold ${e.status === 'SUCCESS' ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'}">
                                ${e.status}
                            </span>
                        </td>
                    </tr>
                `).join('');
            } catch (err) {
                tbody.innerHTML = "<tr><td colspan='5' class='px-6 py-4 text-rose-500'>Failed to load audit events</td></tr>";
            }
        }

        function toggleChat() {
            const panel = document.getElementById('ai-panel');
            panel.classList.toggle('hidden');
        }
        function openChatDrawer() {
            const panel = document.getElementById('ai-panel');
            panel.classList.remove('hidden');
        }

        async function sendChatMessage() {
            const input = document.getElementById('ai-input');
            const msg = input.value.trim();
            if (!msg) return;
            input.value = "";

            const box = document.getElementById('ai-messages');
            box.innerHTML += `<div class="bg-blue-600 text-white p-3 rounded-xl rounded-tr-none text-right font-medium">${msg}</div>`;
            box.scrollTop = box.scrollHeight;

            try {
                const res = await fetch(`${API_BASE}/api/v1/assistant/chat`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: msg, citizen_id: "C001" })
                });
                const data = await res.json();
                box.innerHTML += `<div class="bg-slate-100 p-3 rounded-xl rounded-tl-none text-slate-800 leading-relaxed">${data.reply}</div>`;
                box.scrollTop = box.scrollHeight;
            } catch (e) {
                box.innerHTML += `<div class="bg-rose-50 text-rose-800 p-2 rounded-lg">MahaMitra AI temporarily unavailable.</div>`;
            }
        }

        function askPreset(text) {
            document.getElementById('ai-input').value = text;
            sendChatMessage();
        }

        // Init on page load
        refreshApplicationStatus();
    </script>
</body>
</html>"""
