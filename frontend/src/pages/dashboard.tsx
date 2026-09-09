import React, { useEffect, useState } from "react";
import Link from "next/link";
import axios from "axios";
import { Navbar } from "@/components/Navbar";
import { MahaMitraChat } from "@/components/MahaMitraChat";
import { ConsentModal } from "@/components/ConsentModal";

export default function Dashboard() {
  const [appData, setAppData] = useState<any>(null);
  const [isConsentOpen, setIsConsentOpen] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);

  const fetchApp = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8082";
      const res = await axios.get(`${apiUrl}/api/v1/applications/APP-2026-001`);
      setAppData(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchApp();
  }, []);

  const handleConsent = async (action: "ALLOW" | "DENY") => {
    setIsProcessing(true);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8082";
      await axios.post(`${apiUrl}/api/v1/applications/APP-2026-001/consent`, { action });
      await fetchApp();
    } catch (e) {
      alert("Error submitting consent: " + e);
    } finally {
      setIsProcessing(false);
      setIsConsentOpen(false);
    }
  };

  const isVerified = appData?.status === "VERIFIED";

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Navbar />

      <main className="max-w-7xl mx-auto px-6 py-8 flex-1 w-full space-y-8">
        <!-- Welcome Hero -->
        <div className="bg-gradient-to-r from-blue-900 to-indigo-950 text-white p-8 rounded-2xl shadow-xl flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
          <div>
            <div className="text-xs font-semibold uppercase tracking-wider text-blue-300 mb-1">
              Citizen Interoperability Dashboard
            </div>
            <h2 className="text-2xl font-black tracking-tight">Welcome, Rahul Patil!</h2>
            <p className="text-sm text-blue-200 mt-1 max-w-xl">
              MahaSync connects your verified records across Maharashtra state departments with your consent.
            </p>
          </div>
          <div className="flex gap-3">
            <Link
              href="/services"
              className="bg-blue-600 hover:bg-blue-500 text-white font-bold px-4 py-2.5 rounded-xl text-xs shadow-md transition"
            >
              Explore Services
            </Link>
            <Link
              href="/applications/APP-2026-001"
              className="bg-white/10 hover:bg-white/20 text-white font-semibold px-4 py-2.5 rounded-xl text-xs backdrop-blur-md transition"
            >
              Track Application
            </Link>
          </div>
        </div>

        <!-- Metric Cards -->
        <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
          <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Citizen ID</div>
            <div className="text-xl font-bold font-mono text-slate-900">C001</div>
            <div className="text-xs text-slate-500 mt-1">Keycloak Authenticated</div>
          </div>
          <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Active Scheme</div>
            <div className="text-xl font-bold text-blue-600">Agri Subsidy</div>
            <div className="text-xs text-slate-500 mt-1">Direct Benefit Transfer</div>
          </div>
          <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Verification Status</div>
            <div className={`text-xl font-bold ${isVerified ? "text-emerald-600" : "text-amber-600"}`}>
              {isVerified ? "Verified (A001)" : "Consent Pending"}
            </div>
            <div className="text-xs text-slate-500 mt-1">
              {isVerified ? "Land parcel confirmed" : "Requires 7/12 record"}
            </div>
          </div>
          <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Disbursal Amount</div>
            <div className="text-xl font-bold text-emerald-600">₹15,000</div>
            <div className="text-xs text-slate-500 mt-1">Approved for release</div>
          </div>
        </div>

        <!-- Active Application Card -->
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <div className="px-6 py-4 bg-slate-50 border-b border-slate-200 flex justify-between items-center">
            <div>
              <h3 className="font-bold text-slate-900">Active DBT Application</h3>
              <p className="text-xs text-slate-500">Ref: APP-2026-001 | Mapped Dept ID: A001</p>
            </div>
            <span
              className={`font-mono text-xs font-bold px-3 py-1 rounded-full border ${
                isVerified
                  ? "bg-emerald-100 text-emerald-900 border-emerald-300"
                  : "bg-amber-100 text-amber-900 border-amber-300"
              }`}
            >
              {appData?.status || "CONSENT_PENDING"}
            </span>
          </div>

          <div className="p-6">
            {!isVerified ? (
              <div className="bg-amber-50 border border-amber-200 rounded-xl p-5 mb-6">
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 rounded-xl bg-amber-500 text-white flex items-center justify-center font-bold text-xl flex-shrink-0">
                    ⚖️
                  </div>
                  <div className="flex-1">
                    <h4 className="font-bold text-amber-950 text-sm">Citizen Consent Required</h4>
                    <p className="text-xs text-amber-900 mt-1 leading-relaxed">
                      "Revenue Department land information is required to verify your Agriculture Subsidy application."
                    </p>
                    <div className="mt-4 flex items-center gap-3">
                      <button
                        onClick={() => setIsConsentOpen(true)}
                        className="bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-4 py-2 rounded-lg text-xs shadow-sm transition"
                      >
                        Review & Grant Consent
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-5 mb-6">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-xl bg-emerald-600 text-white flex items-center justify-center font-bold text-xl flex-shrink-0">
                    ✓
                  </div>
                  <div>
                    <h4 className="font-bold text-emerald-950 text-sm">
                      Land Verified Across Revenue & Agriculture Systems!
                    </h4>
                    <p className="text-xs text-emerald-900 mt-0.5">
                      Parcel {appData?.land_id} ({appData?.land_area} Acres) verified via Revenue adapter and RabbitMQ event bus.
                    </p>
                  </div>
                </div>
              </div>
            )}

            <div className="flex justify-between items-center text-xs pt-2">
              <span className="text-slate-500">Service: Department of Agriculture & Farmer Welfare</span>
              <Link href="/applications/APP-2026-001" className="text-blue-600 font-semibold hover:underline">
                View Full Tracking Stepper & Audit Log →
              </Link>
            </div>
          </div>
        </div>
      </main>

      <ConsentModal
        isOpen={isConsentOpen}
        onAllow={() => handleConsent("ALLOW")}
        onDeny={() => handleConsent("DENY")}
        isProcessing={isProcessing}
      />

      <MahaMitraChat />
    </div>
  );
}
