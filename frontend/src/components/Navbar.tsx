import React from "react";
import Link from "next/link";
import { useRouter } from "next/router";

export const Navbar: React.FC = () => {
  const router = useRouter();

  const isActive = (path: string) => router.pathname === path;

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-40 shadow-sm">
      <div className="bg-slate-900 text-slate-300 text-xs px-6 py-1.5 flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <span>🇮🇳</span>
          <span className="font-semibold text-amber-400">Government of Maharashtra Interoperability Framework</span>
        </div>
        <div className="flex items-center space-x-4">
          <span className="text-emerald-400 font-mono text-[11px] flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            SIH 2026 Prototype
          </span>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-3.5 flex flex-col md:flex-row justify-between items-center gap-4">
        <Link href="/dashboard" className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-700 to-indigo-600 text-white flex items-center justify-center font-extrabold text-xl shadow-md">
            M
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-extrabold tracking-tight text-slate-900">MAHASync</h1>
              <span className="bg-blue-100 text-blue-800 text-[10px] font-bold px-2 py-0.5 rounded-full">
                The Digital Bridge
              </span>
            </div>
            <p className="text-[11px] text-slate-500">Connected Government Service Delivery</p>
          </div>
        </Link>

        <div className="flex items-center gap-3">
          <div className="bg-slate-50 border border-slate-200 px-3 py-1.5 rounded-xl flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-full bg-blue-600 text-white font-bold text-xs flex items-center justify-center">
              RP
            </div>
            <div>
              <div className="text-xs font-bold text-slate-800">Rahul Patil (C001)</div>
              <div className="text-[10px] text-emerald-600 font-medium">Keycloak Verified</div>
            </div>
          </div>
          <Link
            href="/login"
            className="text-xs text-slate-600 hover:text-slate-900 font-medium px-2 py-1"
          >
            Switch User
          </Link>
        </div>
      </div>

      <nav className="max-w-7xl mx-auto px-6 flex space-x-8 text-xs font-semibold text-slate-600 border-t border-slate-100">
        <Link
          href="/dashboard"
          className={`py-3 px-1 border-b-2 ${
            isActive("/dashboard") ? "border-blue-600 text-blue-700" : "border-transparent hover:text-slate-900"
          }`}
        >
          Dashboard
        </Link>
        <Link
          href="/services"
          className={`py-3 px-1 border-b-2 ${
            isActive("/services") ? "border-blue-600 text-blue-700" : "border-transparent hover:text-slate-900"
          }`}
        >
          Services Catalog
        </Link>
        <Link
          href="/applications"
          className={`py-3 px-1 border-b-2 ${
            router.pathname.startsWith("/applications") ? "border-blue-600 text-blue-700" : "border-transparent hover:text-slate-900"
          }`}
        >
          Applications Tracking
        </Link>
      </nav>
    </header>
  );
};
