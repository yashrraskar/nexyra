import React, { useEffect, useState } from "react";
import { useRouter } from "next/router";
import Link from "next/link";
import axios from "axios";
import { Navbar } from "@/components/Navbar";

export default function ApplicationTracking() {
  const router = useRouter();
  const { id } = router.query;
  const appId = (id as string) || "APP-2026-001";

  const [app, setApp] = useState<any>(null);
  const [events, setEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8082";
      const [appRes, eventsRes] = await Promise.all([
        axios.get(`${apiUrl}/api/v1/applications/${appId}`),
        axios.get(`${apiUrl}/api/v1/applications/${appId}/events`),
      ]);
      setApp(appRes.data);
      setEvents(eventsRes.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (appId) fetchData();
  }, [appId]);

  const isVerified = app?.status === "VERIFIED";

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Navbar />

      <main className="max-w-5xl mx-auto px-6 py-8 flex-1 w-full space-y-8">
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-8">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-100 pb-6 mb-8">
            <div>
              <div className="flex items-center gap-3">
                <h2 className="text-2xl font-bold text-slate-900">Application Interoperability Tracker</h2>
                <span
                  className={`text-xs font-bold px-3 py-1 rounded-full font-mono ${
                    isVerified
                      ? "bg-emerald-100 text-emerald-800 border border-emerald-300"
                      : "bg-amber-100 text-amber-800 border border-amber-300"
                  }`}
                >
                  {app?.status || "IN_PROGRESS"}
                </span>
              </div>
              <p className="text-xs text-slate-500 mt-1">
                Ref: <span className="font-mono font-bold text-slate-700">{appId}</span> | Citizen: Rahul Patil (C001)
              </p>
            </div>
            <button
              onClick={fetchData}
              className="text-xs font-semibold bg-slate-100 hover:bg-slate-200 text-slate-700 px-4 py-2 rounded-xl transition"
            >
              🔄 Refresh Tracking
            </button>
          </div>

          <!-- 5-Stage Interoperability Timeline -->
          <div className="space-y-6 mb-10">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Inter-Department Verification Stepper
            </h3>

            <div className="space-y-4">
              <!-- Stage 1 -->
              <div className="flex items-start gap-4">
                <div className="w-8 h-8 rounded-full bg-emerald-600 text-white flex items-center justify-center font-bold text-xs flex-shrink-0">
                  ✓
                </div>
                <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 flex-1 text-xs">
                  <div className="font-bold text-slate-800">1. Application Submitted</div>
                  <div className="text-slate-500">Citizen submitted Agriculture Subsidy application via MahaSync Portal.</div>
                </div>
              </div>

              <!-- Stage 2 -->
              <div className="flex items-start gap-4">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs flex-shrink-0 ${
                    app?.consent?.status === "GRANTED" || isVerified
                      ? "bg-emerald-600 text-white"
                      : "bg-amber-500 text-white"
                  }`}
                >
                  {app?.consent?.status === "GRANTED" || isVerified ? "✓" : "2"}
                </div>
                <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 flex-1 text-xs">
                  <div className="font-bold text-slate-800">2. Citizen Consent Granted</div>
                  <div className="text-slate-500">
                    Explicit consent authorized under DPDP Act to query Revenue Department 7/12 land registry.
                  </div>
                </div>
              </div>

              <!-- Stage 3 -->
              <div className="flex items-start gap-4">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs flex-shrink-0 ${
                    isVerified ? "bg-emerald-600 text-white" : "bg-slate-300 text-slate-600"
                  }`}
                >
                  {isVerified ? "✓" : "3"}
                </div>
                <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 flex-1 text-xs">
                  <div className="font-bold text-slate-800">3. Revenue Data Retrieved & Standardized</div>
                  <div className="text-slate-500">
                    Revenue API queried (Port 8000). Standardized via Revenue Adapter into canonical MahaSync format.
                  </div>
                </div>
              </div>

              <!-- Stage 4 -->
              <div className="flex items-start gap-4">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs flex-shrink-0 ${
                    isVerified ? "bg-emerald-600 text-white" : "bg-slate-300 text-slate-600"
                  }`}
                >
                  {isVerified ? "✓" : "4"}
                </div>
                <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 flex-1 text-xs">
                  <div className="font-bold text-slate-800">4. Land Verified Event Dispatched (RabbitMQ)</div>
                  <div className="text-slate-500">
                    Asynchronous LandVerified event published to topic exchange <code>mahasync.events</code>.
                  </div>
                </div>
              </div>

              <!-- Stage 5 -->
              <div className="flex items-start gap-4">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs flex-shrink-0 ${
                    isVerified ? "bg-emerald-600 text-white" : "bg-slate-300 text-slate-600"
                  }`}
                >
                  {isVerified ? "✓" : "5"}
                </div>
                <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 flex-1 text-xs">
                  <div className="font-bold text-slate-800">5. Agriculture Application Verified</div>
                  <div className="text-slate-500">
                    Agriculture Department API (Port 8001) updated subsidy application A001 to <b>VERIFIED</b>.
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Audit Log Table -->
          <div className="space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Immutable Application Audit Trail
            </h3>
            <div className="bg-slate-50 rounded-xl border border-slate-200 overflow-hidden">
              <table className="w-full text-left text-xs text-slate-600">
                <thead className="bg-slate-100 text-slate-500 uppercase font-semibold border-b border-slate-200">
                  <tr>
                    <th className="px-4 py-3">Timestamp</th>
                    <th className="px-4 py-3">Source</th>
                    <th className="px-4 py-3">Event Type</th>
                    <th className="px-4 py-3">Details</th>
                    <th className="px-4 py-3">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200 font-mono">
                  {events.map((e) => (
                    <tr key={e.id} className="hover:bg-white transition">
                      <td className="px-4 py-2.5 whitespace-nowrap text-slate-500">
                        {new Date(e.timestamp).toLocaleTimeString()}
                      </td>
                      <td className="px-4 py-2.5">
                        <span className="bg-slate-200 text-slate-800 px-1.5 py-0.5 rounded text-[10px] font-bold">
                          {e.source}
                        </span>
                      </td>
                      <td className="px-4 py-2.5 font-bold text-slate-800">{e.event_type}</td>
                      <td className="px-4 py-2.5 font-sans text-slate-700">{e.description}</td>
                      <td className="px-4 py-2.5">
                        <span className="text-emerald-700 font-bold">{e.status}</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
