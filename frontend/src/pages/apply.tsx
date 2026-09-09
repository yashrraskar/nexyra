import React, { useState } from "react";
import { useRouter } from "next/router";
import axios from "axios";
import { Navbar } from "@/components/Navbar";

export default function ApplyPage() {
  const router = useRouter();
  const [serviceId, setServiceId] = useState("SRV-AGRI-001");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8082";
      const res = await axios.post(`${apiUrl}/api/v1/applications`, {
        service_id: serviceId,
        citizen_id: "C001",
        department_application_id: "A001",
      });
      router.push(`/consent?appId=${res.data.id}`);
    } catch (err) {
      alert("Application submission error: " + err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Navbar />

      <main className="max-w-2xl mx-auto px-6 py-8 flex-1 w-full">
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-8 space-y-6">
          <div className="border-b border-slate-100 pb-4">
            <h2 className="text-xl font-bold text-slate-900">New Service Application</h2>
            <p className="text-xs text-slate-500 mt-1">
              Apply with your verified citizen profile. Data from other departments will be fetched on consent.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4 text-xs">
            <div>
              <label className="block font-bold text-slate-700 uppercase tracking-wider mb-1">
                Applying Citizen
              </label>
              <div className="bg-slate-100 p-3 rounded-xl border border-slate-200 flex justify-between items-center">
                <div>
                  <div className="font-bold text-slate-800">Rahul Patil</div>
                  <div className="text-slate-500 font-mono">Citizen ID: C001 (Maharashtra)</div>
                </div>
                <span className="bg-emerald-100 text-emerald-800 text-[10px] font-bold px-2 py-0.5 rounded font-mono">
                  VERIFIED
                </span>
              </div>
            </div>

            <div>
              <label className="block font-bold text-slate-700 uppercase tracking-wider mb-1">
                Selected Scheme
              </label>
              <select
                value={serviceId}
                onChange={(e) => setServiceId(e.target.value)}
                className="w-full border border-slate-300 rounded-xl p-3 bg-white text-slate-800 focus:outline-none focus:border-blue-600"
              >
                <option value="SRV-AGRI-001">Agriculture Subsidy Scheme (DBT) - Dept of Agriculture</option>
                <option value="SRV-KISAN-002">PM-KISAN Samman Nidhi - Direct Income Transfer</option>
              </select>
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 text-blue-900 space-y-1">
              <div className="font-bold">Next Step: Citizen Consent</div>
              <p>
                To process your Agriculture Subsidy, MahaSync will request permission to fetch your verified 7/12 land parcel from the Revenue Department.
              </p>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-xl shadow-md transition text-xs"
            >
              {loading ? "Submitting..." : "Proceed to Consent Authorization →"}
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}
