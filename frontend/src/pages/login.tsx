import React, { useState } from "react";
import { useRouter } from "next/router";

export default function Login() {
  const router = useRouter();
  const [citizenId, setCitizenId] = useState("C001");
  const [password, setPassword] = useState("rahul123");

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    // Simulate login for C001
    router.push("/dashboard");
  };

  const handleKeycloakSSO = () => {
    // Redirect to Keycloak auth server if enabled or demo login
    const keycloakUrl = process.env.NEXT_PUBLIC_KEYCLOAK_URL || "http://127.0.0.1:8080";
    window.location.href = `${keycloakUrl}/realms/mahasync/account`;
  };

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col justify-center items-center p-4">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-xl border border-slate-200 overflow-hidden">
        <div className="bg-gradient-to-r from-blue-800 to-indigo-800 p-8 text-white text-center">
          <div className="w-14 h-14 mx-auto rounded-2xl bg-white/10 backdrop-blur-md flex items-center justify-center font-black text-3xl mb-3 border border-white/20">
            M
          </div>
          <h1 className="text-2xl font-black tracking-tight">MAHASync</h1>
          <p className="text-xs text-blue-200 mt-1">The Digital Bridge • Interoperability Platform</p>
        </div>

        <form onSubmit={handleLogin} className="p-8 space-y-5">
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              Citizen ID / Aadhaar
            </label>
            <input
              type="text"
              value={citizenId}
              onChange={(e) => setCitizenId(e.target.value)}
              className="w-full text-sm border border-slate-300 rounded-xl px-4 py-2.5 font-mono focus:outline-none focus:border-blue-600"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full text-sm border border-slate-300 rounded-xl px-4 py-2.5 focus:outline-none focus:border-blue-600"
              required
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2.5 rounded-xl text-sm shadow-md shadow-blue-600/20 transition"
          >
            Login to MahaSync
          </button>

          <div className="relative flex py-1 items-center">
            <div className="flex-grow border-t border-slate-200"></div>
            <span className="flex-shrink mx-3 text-slate-400 text-xs uppercase font-bold">Or</span>
            <div className="flex-grow border-t border-slate-200"></div>
          </div>

          <button
            type="button"
            onClick={handleKeycloakSSO}
            className="w-full bg-slate-900 hover:bg-slate-800 text-white font-semibold py-2.5 rounded-xl text-xs flex items-center justify-center gap-2 transition"
          >
            <span>🔐</span> Authenticate via Keycloak SSO
          </button>

          <div className="bg-blue-50 border border-blue-200 rounded-xl p-3 text-[11px] text-blue-900">
            <b>SIH Demo User:</b> Pre-configured credentials for Rahul Patil (Citizen ID: <code>C001</code>). Click Login to proceed to the citizen dashboard.
          </div>
        </form>
      </div>
    </div>
  );
}
