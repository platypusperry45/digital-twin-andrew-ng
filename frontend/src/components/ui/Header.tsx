"use client";

import React from "react";
import { FiCpu, FiGrid, FiActivity } from "react-icons/fi";

interface HeaderProps {
  activeTab: "chat" | "memory";
  setActiveTab: (tab: "chat" | "memory") => void;
  isSpeaking: boolean;
}

export default function Header({ activeTab, setActiveTab, isSpeaking }: HeaderProps) {
  return (
    <header className="flex justify-between items-center z-10 w-full max-w-5xl mx-auto px-4 pt-2">
      <div className="flex items-center space-x-3">
        <div className={`w-3 h-3 rounded-full ${isSpeaking ? "bg-emerald-400 animate-ping" : "bg-indigo-500 animate-pulse"}`} />
        <h1 className="text-lg font-bold tracking-wider text-slate-100 flex items-center gap-2">
          ANDREW NG <span className="text-[10px] text-indigo-400 font-mono bg-indigo-950/60 border border-indigo-800/80 px-2 py-0.5 rounded-full">DIGITAL TWIN v2.5</span>
        </h1>
      </div>

      <div className="flex items-center space-x-2 glass-pill px-3 py-1.5 rounded-full text-xs font-mono text-slate-300">
        <button
          onClick={() => setActiveTab("chat")}
          className={`px-3 py-1 rounded-full transition-all flex items-center gap-1.5 ${
            activeTab === "chat" ? "bg-indigo-600 text-white shadow-lg shadow-indigo-600/30" : "hover:text-white"
          }`}
        >
          <FiCpu /> Chat Console
        </button>
        <button
          onClick={() => setActiveTab("memory")}
          className={`px-3 py-1 rounded-full transition-all flex items-center gap-1.5 ${
            activeTab === "memory" ? "bg-indigo-600 text-white shadow-lg shadow-indigo-600/30" : "hover:text-white"
          }`}
        >
          <FiGrid /> Memory Graph
        </button>
      </div>
    </header>
  );
}