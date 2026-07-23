"use client";

import { FiActivity, FiLayers, FiRadio, FiShieldAlert } from "react-icons/fi";
import { useUiStore } from "@/store/useUiStore";

export default function Header() {
  const { activeTab, activeModelName, setActiveModelName, toggleDiagnosticPanel, isDiagnosticPanelOpen } =
    useUiStore();

  const titleMap: Record<string, string> = {
    chat: "Interactive AI Chat Console",
    knowledge: "Knowledge Base & RAG Indexer",
    memory: "3D Memory Network Visualizer",
    personality: "Pedagogical Persona Tuning",
    developer: "Real-Time Telemetry & Diagnostics",
    settings: "System & API Configuration",
    admin: "Admin Control & Operations Center",
  };

  return (
    <header className="h-14 border-b border-slate-800/60 bg-[#08090d]/80 backdrop-blur-xl px-6 flex items-center justify-between z-20 shrink-0">
      {/* Current Context Title */}
      <div className="flex items-center space-x-3">
        <h1 className="text-sm font-semibold text-slate-100 tracking-wide">
          {titleMap[activeTab] || "Digital Twin Console"}
        </h1>
        <span className="px-2 py-0.5 rounded-full text-[10px] font-mono bg-indigo-950/80 border border-indigo-800/60 text-indigo-300">
          v2.5 PRO
        </span>
      </div>

      {/* Model Selector & Telemetry Toggles */}
      <div className="flex items-center space-x-3">
        {/* Model Selector Badge */}
        <div className="flex items-center space-x-2 bg-slate-900/90 border border-slate-800 px-3 py-1 rounded-xl text-xs font-mono text-slate-300">
          <FiLayers className="text-indigo-400" />
          <select
            value={activeModelName}
            onChange={(e) => setActiveModelName(e.target.value)}
            className="bg-transparent text-slate-200 text-xs focus:outline-none cursor-pointer"
          >
            <option value="Gemini 1.5 Pro + RAG ChromaDB" className="bg-slate-900">
              Gemini 1.5 Pro + RAG ChromaDB
            </option>
            <option value="Gemini 1.5 Flash (Fast)" className="bg-slate-900">
              Gemini 1.5 Flash (Fast)
            </option>
            <option value="Data-Centric Expert Mode" className="bg-slate-900">
              Data-Centric Expert Mode
            </option>
          </select>
        </div>

        {/* Diagnostic Panel Toggle */}
        <button
          onClick={toggleDiagnosticPanel}
          className={`flex items-center space-x-2 px-3 py-1 rounded-xl border text-xs font-mono transition-all ${
            isDiagnosticPanelOpen
              ? "bg-indigo-600/20 border-indigo-500/50 text-indigo-300 shadow-sm"
              : "bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200"
          }`}
        >
          <FiActivity size={13} />
          <span>Telemetry</span>
        </button>
      </div>
    </header>
  );
}