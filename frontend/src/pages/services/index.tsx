import React, { useEffect, useState } from "react";
import Link from "next/link";
import axios from "axios";
import { Navbar } from "@/components/Navbar";
import { MahaMitraChat } from "@/components/MahaMitraChat";

export default function ServicesPage() {
  const [services, setServices] = useState<any[]>([]);

  useEffect(() => {
    const fetchServices = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8082";
        const res = await axios.get(`${apiUrl}/api/v1/services`);
        setServices(res.data);
      } catch (e) {
        console.error(e);
      }
    };
    fetchServices();
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Navbar />

      <main className="max-w-7xl mx-auto px-6 py-8 flex-1 w-full space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Government Service Catalog</h2>
          <p className="text-xs text-slate-500 mt-1">
            Discover schemes with automated cross-departmental record verification.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {services.map((s) => (
            <div
              key={s.id}
              className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col justify-between hover:shadow-md transition"
            >
              <div>
                <div className="flex justify-between items-start mb-2">
                  <span className="bg-blue-50 text-blue-700 text-[10px] font-bold px-2 py-0.5 rounded uppercase font-mono">
                    {s.category}
                  </span>
                  <span className="text-xs font-bold text-emerald-600">{s.benefit_amount}</span>
                </div>
                <h3 className="font-bold text-slate-900 text-base mb-1">{s.title}</h3>
                <p className="text-xs text-slate-500 mb-4 leading-relaxed">{s.description}</p>
                <div className="bg-slate-50 p-3 rounded-xl border border-slate-200 text-xs mb-4">
                  <span className="text-[10px] text-slate-400 uppercase font-semibold block">
                    Required Interoperability:
                  </span>
                  <span className="font-medium text-slate-700">{s.required_data_source}</span>
                </div>
              </div>

              <Link
                href={s.id === "SRV-AGRI-001" ? "/services/agriculture-subsidy" : "/apply"}
                className="w-full bg-slate-900 hover:bg-blue-600 text-white font-semibold py-2.5 rounded-xl text-xs text-center transition"
              >
                View Scheme Details & Apply →
              </Link>
            </div>
          ))}
        </div>
      </main>

      <MahaMitraChat />
    </div>
  );
}
