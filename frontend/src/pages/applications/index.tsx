import React, { useEffect, useState } from "react";
import Link from "next/link";
import axios from "axios";
import { Navbar } from "@/components/Navbar";

export default function ApplicationsList() {
  const [apps, setApps] = useState<any[]>([]);

  useEffect(() => {
    const fetchApps = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8082";
        const res = await axios.get(`${apiUrl}/api/v1/applications?citizen_id=C001`);
        setApps(res.data);
      } catch (e) {
        console.error(e);
      }
    };
    fetchApps();
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Navbar />

      <main className="max-w-7xl mx-auto px-6 py-8 flex-1 w-full space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Your Submitted Applications</h2>
          <p className="text-xs text-slate-500 mt-1">
            Real-time tracking of benefit applications and cross-departmental verifications.
          </p>
        </div>

        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <table className="w-full text-left text-xs text-slate-600">
            <thead className="bg-slate-50 text-slate-500 uppercase font-semibold border-b border-slate-200">
              <tr>
                <th className="px-6 py-4">Application ID</th>
                <th className="px-6 py-4">Scheme</th>
                <th className="px-6 py-4">Dept Ref</th>
                <th className="px-6 py-4">Verification Status</th>
                <th className="px-6 py-4">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-mono">
              {apps.map((a) => (
                <tr key={a.id} className="hover:bg-slate-50 transition">
                  <td className="px-6 py-4 font-bold text-slate-900">{a.id}</td>
                  <td className="px-6 py-4 font-sans font-medium text-slate-800">
                    {a.service_title || "Agriculture Subsidy Scheme"}
                  </td>
                  <td className="px-6 py-4 text-slate-500">{a.department_application_id || "A001"}</td>
                  <td className="px-6 py-4">
                    <span
                      className={`px-2.5 py-0.5 rounded-full font-bold text-[11px] ${
                        a.status === "VERIFIED"
                          ? "bg-emerald-100 text-emerald-800 border border-emerald-300"
                          : a.status === "CONSENT_DENIED"
                          ? "bg-rose-100 text-rose-800 border border-rose-300"
                          : "bg-amber-100 text-amber-800 border border-amber-300"
                      }`}
                    >
                      {a.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 font-sans">
                    <Link
                      href={`/applications/${a.id}`}
                      className="text-blue-600 hover:text-blue-800 font-semibold"
                    >
                      View Tracking Timeline →
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}
