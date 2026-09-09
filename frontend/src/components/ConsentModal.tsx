import React from "react";

interface ConsentModalProps {
  isOpen: boolean;
  onAllow: () => void;
  onDeny: () => void;
  isProcessing?: boolean;
}

export const ConsentModal: React.FC<ConsentModalProps> = ({
  isOpen,
  onAllow,
  onDeny,
  isProcessing = false,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-lg w-full shadow-2xl border border-slate-200 overflow-hidden animate-in fade-in zoom-in duration-200">
        <div className="bg-amber-500 text-white px-6 py-4 flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-amber-600 flex items-center justify-center font-bold text-lg">
            ⚖️
          </div>
          <div>
            <h3 className="font-bold text-base">Citizen Data Sharing Consent</h3>
            <p className="text-xs text-amber-100">Digital Personal Data Protection (DPDP) Act 2023</p>
          </div>
        </div>

        <div className="p-6 space-y-4">
          <div className="bg-amber-50/70 border border-amber-200 rounded-xl p-4 text-xs text-amber-950 font-medium leading-relaxed">
            "Revenue Department land information is required to verify your Agriculture Subsidy application."
          </div>

          <div className="space-y-2 text-xs text-slate-600">
            <div className="flex justify-between border-b border-slate-100 pb-1.5">
              <span className="text-slate-500">Data Source:</span>
              <span className="font-semibold text-slate-800">Revenue & Land Administration Dept</span>
            </div>
            <div className="flex justify-between border-b border-slate-100 pb-1.5">
              <span className="text-slate-500">Data Recipient:</span>
              <span className="font-semibold text-slate-800">Department of Agriculture</span>
            </div>
            <div className="flex justify-between border-b border-slate-100 pb-1.5">
              <span className="text-slate-500">Information Exchanged:</span>
              <span className="font-mono text-slate-800">Survey No: MH-LAND-101 (2.5 Acres)</span>
            </div>
            <div className="flex justify-between pb-1">
              <span className="text-slate-500">Purpose:</span>
              <span className="text-slate-800">Automated Direct Benefit Transfer (DBT) eligibility</span>
            </div>
          </div>

          <div className="bg-slate-50 p-3 rounded-lg text-[11px] text-slate-500">
            Your consent is voluntary and logged in the immutable application audit trail. If denied, the digital verification cannot proceed automatically.
          </div>
        </div>

        <div className="bg-slate-50 px-6 py-4 border-t border-slate-100 flex justify-end gap-3">
          <button
            onClick={onDeny}
            disabled={isProcessing}
            className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-200 transition"
          >
            Deny Consent
          </button>
          <button
            onClick={onAllow}
            disabled={isProcessing}
            className="px-5 py-2 rounded-xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 shadow-md shadow-emerald-600/20 transition flex items-center gap-1.5"
          >
            {isProcessing ? "Processing..." : "Allow & Share Verified Data"}
          </button>
        </div>
      </div>
    </div>
  );
};
