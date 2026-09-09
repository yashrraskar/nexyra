import React from "react";
import Link from "next/link";
import { Navbar } from "@/components/Navbar";
import { MahaMitraChat } from "@/components/MahaMitraChat";

export default function AgricultureSubsidyDetail() {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Navbar />

      <main className="max-w-4xl mx-auto px-6 py-8 flex-1 w-full space-y-6">
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-8 space-y-6">
          <div className="flex justify-between items-start border-b border-slate-100 pb-6">
            <div>
              <span className="bg-emerald-100 text-emerald-800 text-xs font-bold px-2.5 py-1 rounded-full font-mono uppercase">
                Department of Agriculture
              </span>
              <h2 className="text-2xl font-black text-slate-900 mt-2">
                Agriculture Subsidy Scheme (DBT)
              </h2>
              <p className="text-xs text-slate-500 mt-1">
                Direct Benefit Transfer for Fertilisers, Seeds, and Micro-Irrigation Infrastructure
              </p>
            </div>
            <div className="text-right">
              <div className="text-xs text-slate-400 font-semibold uppercase">Benefit Amount</div>
              <div className="text-2xl font-black text-emerald-600">₹15,000 / Season</div>
            </div>
          </div>

          <div className="space-y-4 text-xs text-slate-700 leading-relaxed">
            <h4 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
              Scheme Description
            </h4>
            <p>
              The Government of Maharashtra provides financial assistance to eligible farmers to encourage adoption of high-yielding crop varieties and eco-friendly farming practices. Benefits are transferred directly to verified bank accounts.
            </p>

            <h4 className="text-sm font-bold text-slate-900 uppercase tracking-wider pt-2">
              Eligibility Criteria
            </h4>
            <ul className="list-disc list-inside space-y-1 text-slate-600">
              <li>Individual must be a registered resident citizen of Maharashtra state.</li>
              <li>Must hold active title to cultivable agricultural land documented in the Revenue Registry.</li>
              <li>Minimum agricultural land holding of 1.0 Acre.</li>
            </ul>

            <h4 className="text-sm font-bold text-slate-900 uppercase tracking-wider pt-2">
              Automated Interoperability Requirement
            </h4>
            <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 text-amber-950">
              <div className="font-bold mb-1">⚡ No Manual 7/12 Upload Required</div>
              MahaSync will digitally query your 7/12 extract directly from the <b>State Revenue Department</b> using your authenticated citizen profile upon your explicit consent.
            </div>
          </div>

          <div className="border-t border-slate-100 pt-6 flex justify-between items-center">
            <Link href="/services" className="text-xs text-slate-500 hover:text-slate-800 font-medium">
              ← Back to Catalog
            </Link>
            <Link
              href="/apply?service=SRV-AGRI-001"
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold px-6 py-2.5 rounded-xl text-xs shadow-md shadow-blue-600/20 transition"
            >
              Apply for Scheme →
            </Link>
          </div>
        </div>
      </main>

      <MahaMitraChat />
    </div>
  );
}
