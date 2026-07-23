"use client";

import { useState } from "react";
import {
  FiShield,
  FiUsers,
  FiDatabase,
  FiFileText,
  FiSliders,
  FiCheckCircle,
  FiAlertCircle,
} from "react-icons/fi";

export default function AdminDashboard() {
  const [activeSubTab, setActiveSubTab] = useState<"analytics" | "users" | "logs">("analytics");

  return (
    <div className="flex-1 flex flex-col h-full overflow-y-auto bg-[#050508] text-slate-100 p-6 space-y-6 max-w-6xl mx-auto w-full">
      {/* Header */}
      <div className="flex justify-between items-end border-b border-slate-800/60 pb-5">
        <div>
          <h1 className="text-xl font-bold tracking-wide text-slate-100 flex items-center gap-2">
            <FiShield className="text-indigo-400" /> Admin Control & Operations Center
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Global administrative controls, session inspection, safety parameters, and user privileges.
          </p>
        </div>

        <div className="flex space-x-1 bg-slate-900 border border-slate-800 p-1 rounded-xl text-xs font-mono">
          <button
            onClick={() => setActiveSubTab("analytics")}
            className={`px-3 py-1.5 rounded-lg transition-all ${
              activeSubTab === "analytics" ? "bg-indigo-600 text-white font-bold" : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Analytics
          </button>
          <button
            onClick={() => setActiveSubTab("users")}
            className={`px-3 py-1.5 rounded-lg transition-all ${
              activeSubTab === "users" ? "bg-indigo-600 text-white font-bold" : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Users & Roles
          </button>
          <button
            onClick={() => setActiveSubTab("logs")}
            className={`px-3 py-1.5 rounded-lg transition-all ${
              activeSubTab === "logs" ? "bg-indigo-600 text-white font-bold" : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Audit Logs
          </button>
        </div>
      </div>

      {/* Main Content Area */}
      {activeSubTab === "analytics" && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-slate-900/80 border border-slate-800/80 p-4 rounded-2xl space-y-2">
              <span className="text-[10px] font-mono text-slate-500 uppercase">Total Active Users</span>
              <span className="text-2xl font-bold font-mono text-slate-100 block">1,248</span>
              <span className="text-[10px] text-emerald-400 font-mono">+12.4% this week</span>
            </div>
            <div className="bg-slate-900/80 border border-slate-800/80 p-4 rounded-2xl space-y-2">
              <span className="text-[10px] font-mono text-slate-500 uppercase">Conversations Processed</span>
              <span className="text-2xl font-bold font-mono text-indigo-400 block">18,920</span>
              <span className="text-[10px] text-slate-400 font-mono">Avg 14 turns per session</span>
            </div>
            <div className="bg-slate-900/80 border border-slate-800/80 p-4 rounded-2xl space-y-2">
              <span className="text-[10px] font-mono text-slate-500 uppercase">RAG Ingestion Queue</span>
              <span className="text-2xl font-bold font-mono text-emerald-400 block">0 Pending</span>
              <span className="text-[10px] text-emerald-400 font-mono">All jobs completed</span>
            </div>
          </div>
        </div>
      )}

      {activeSubTab === "users" && (
        <div className="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-5 space-y-4">
          <span className="text-xs font-mono font-bold text-slate-200 uppercase tracking-wider block">
            Workspace Permissions
          </span>
          <div className="space-y-2 text-xs">
            <div className="flex justify-between items-center p-3 bg-slate-950 border border-slate-800 rounded-xl">
              <div>
                <span className="font-bold text-slate-200 block">Andrew Ng (Workspace Owner)</span>
                <span className="text-[10px] text-slate-500 font-mono">andrew@stanford.edu</span>
              </div>
              <span className="px-2 py-1 rounded bg-indigo-950 border border-indigo-800 text-indigo-300 font-mono text-[10px]">
                ADMIN
              </span>
            </div>
          </div>
        </div>
      )}

      {activeSubTab === "logs" && (
        <div className="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-5 space-y-3 font-mono text-xs">
          <span className="text-xs font-mono font-bold text-slate-200 uppercase tracking-wider block">
            Administrative Audit Trail
          </span>
          <div className="space-y-2 text-[11px] text-slate-400">
            <div className="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between">
              <span>Updated Pedagogy Parameters (First Principles set to 90%)</span>
              <span className="text-slate-500">10 mins ago</span>
            </div>
            <div className="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between">
              <span>Ingested Document: "CS229_Lecture_Notes.md"</span>
              <span className="text-slate-500">1 hour ago</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}