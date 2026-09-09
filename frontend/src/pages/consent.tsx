import React, { useState } from "react";
import { useRouter } from "next/router";
import axios from "axios";
import { Navbar } from "@/components/Navbar";

export default function ConsentPage() {
  const router = useRouter();
  const { appId } = router.query;
  const applicationId = (appId as string) || "APP-2026-001";
  const [loading, setLoading] = useState(false);

  const handleDecision = async (action: "ALLOW" | "DENY") => {
    setLoading(true);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8082";
      await axios.post(`${apiUrl}/api/v1/applications/${applicationId}/consent`, {
        action: action,
      });
      router.push(`/applications/${applicationId}`);
    } catch (e) {
      alert("Error processing consent: " + e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Navbar />

      <main className="max-w-2xl mx-auto px-6 py-12 flex-1 w-full">
        <div className="bg-white rounded-2xl border border-slate-200 shadow-xl overflow-hidden">
          <div className="bg-gradient-to-r from-amber-600 to-amber-700 text-white p-6 flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-white/10 flex items-center justify-center font-bold text-2xl">
              ⚖️
            </div>
            <div>
              <h2 className="text-xl font-bold">Citizen Data Sharing Consent</h2>
              <p className="text-xs text-amber-100">
                Digital Personal Data Protection (DPDP) Act 2023 Compliance
              </p>
            </div>
          </div>

          <div className="p-8 space-y-6">
            <div className="bg-amber-50 border border-amber-200 rounded-xl p-5 text-sm text-amber-950 font-semibold leading-relaxed">
              "Revenue Department land information is required to verify your Agriculture Subsidy application."
            </div>

            <div className="space-y-3 text-xs">
              <div className="flex justify-between border-b border-slate-100 pb-2">
                <span className="text-slate-500 font-medium">Application Reference:</span>
                <span className="font-mono font-bold text-slate-800">{applicationId}</span>
              </div>
              <div className="flex justify-between border-b border-slate-100 pb-2">
                <span className="text-slate-500 font-medium">Data Provider:</span>
                <span className="font-semibold text-slate-800">State Revenue & Land Registry Dept</span>
              </div>
              <div className="flex justify-between border-b border-slate-100 pb-2">
                <span className="text-slate-500 font-medium">Data Consumer:</span>
                <span className="font-semibold text-slate-800">Department of Agriculture</span>
              </div>
              <div className="flex justify-between border-b border-slate-100 pb-2">
                <span className="text-slate-500 font-medium">Attributes Shared:</span>
                <span className="font-mono text-slate-800">Survey No. (MH-LAND-101), Land Area (2.5 Acres), Verification Flag</span>
              </div>
              <div className="flex justify-between pb-1">
                <span className="text-slate-500 font-medium">Purpose:</span>
                <span className="text-slate-800">Farmer verification for DBT subsidy disbursement</span>
              </div>
            </div>

            <div className="bg-slate-50 p-4 rounded-xl text-xs text-slate-600 leading-relaxed border border-slate-200">
              <div className="font-bold text-slate-800 mb-1">Your Rights:</div>
              Consent is voluntary. By clicking <b>Allow</b>, MahaSync will securely fetch your land record, standardize the format, and dispatch an event to the Agriculture Department via RabbitMQ. If you <b>Deny</b>, the digital verification is cancelled.
            </div>

            <div className="flex justify-end gap-3 pt-2">
              <button
                onClick={() => handleDecision("DENY")}
                disabled={loading}
                className="px-5 py-2.5 rounded-xl text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 transition"
              >
                Deny Consent
              </button>
              <button
                onClick={() => handleDecision("ALLOW")}
                disabled={loading}
                className="px-6 py-2.5 rounded-xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 shadow-md shadow-emerald-600/20 transition flex items-center gap-2"
              >
                {loading ? "Authorizing..." : "Allow & Share Verified Record"}
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
