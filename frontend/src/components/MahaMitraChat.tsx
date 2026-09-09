import React, { useState } from "react";
import axios from "axios";

export const MahaMitraChat: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Array<{ sender: "user" | "ai"; text: string }>>([
    {
      sender: "ai",
      text: "Namaskar Rahul! I am MahaMitra, your digital governance guide. Ask me about scheme eligibility, DPDP consent, or how your 7/12 land records are verified.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async (textToSend?: string) => {
    const query = textToSend || input;
    if (!query.trim()) return;

    const newMsgs = [...messages, { sender: "user" as const, text: query }];
    setMessages(newMsgs);
    setInput("");
    setLoading(true);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8082";
      const res = await axios.post(`${apiUrl}/api/v1/assistant/chat`, {
        message: query,
        citizen_id: "C001",
      });
      setMessages([...newMsgs, { sender: "ai", text: res.data.reply }]);
    } catch (e) {
      setMessages([
        ...newMsgs,
        { sender: "ai", text: "MahaMitra is temporarily offline. Please check back shortly." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end">
      {isOpen && (
        <div className="w-96 bg-white rounded-2xl shadow-2xl border border-slate-200 overflow-hidden mb-3 flex flex-col h-[460px]">
          <div className="bg-gradient-to-r from-blue-700 to-indigo-700 text-white px-5 py-3.5 flex justify-between items-center">
            <div className="flex items-center gap-2">
              <span className="text-xl">🤖</span>
              <div>
                <div className="font-bold text-sm">MahaMitra AI Guide</div>
                <div className="text-[10px] text-blue-200">Governance Assistant</div>
              </div>
            </div>
            <button onClick={() => setIsOpen(false)} className="text-white hover:text-slate-200 font-bold text-sm">
              ✕
            </button>
          </div>

          <div className="flex-1 p-4 overflow-y-auto space-y-3 text-xs">
            {messages.map((m, idx) => (
              <div
                key={idx}
                className={`p-3 rounded-xl ${
                  m.sender === "user"
                    ? "bg-blue-600 text-white ml-6 rounded-tr-none"
                    : "bg-slate-100 text-slate-800 mr-6 rounded-tl-none leading-relaxed"
                }`}
              >
                {m.text}
              </div>
            ))}
            {loading && <div className="text-[11px] text-slate-400 italic">MahaMitra is thinking...</div>}
          </div>

          <div className="p-3 bg-white border-t border-slate-200 flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              placeholder="Ask about schemes, consent, land..."
              className="flex-1 text-xs border border-slate-300 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-600"
            />
            <button
              onClick={() => sendMessage()}
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold px-3 py-2 rounded-lg text-xs"
            >
              Send
            </button>
          </div>
        </div>
      )}

      <button
        onClick={() => setIsOpen(!isOpen)}
        className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-4 py-3 rounded-full shadow-lg hover:shadow-xl hover:scale-105 transition flex items-center gap-2 text-xs font-bold border border-blue-400"
      >
        <span className="text-lg">🤖</span>
        <span>MahaMitra AI</span>
      </button>
    </div>
  );
};
