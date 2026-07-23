"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { FiCpu, FiDatabase, FiZap, FiCheckCircle } from "react-icons/fi";
import { useUiStore } from "@/store/useUiStore";
import { useChatStore } from "@/store/useChatStore";

export default function RightDiagnosticPanel() {
  const { isDiagnosticPanelOpen } = useUiStore();
  const { getActiveSession } = useChatStore();
  const activeSession = getActiveSession();

  const [latency, setLatency] = useState(310);
  const [tokens, setTokens] = useState(482);

  // Derive last retrieved sources
  const lastMessage = activeSession?.messages[activeSession.messages.length - 1];
  const activeSources = lastMessage?.sources || [];

  useEffect(() => {
    // Simulate slight live variance for latency indicators
    const interval = setInterval(() => {
      setLatency((prev) => Math.max(280, Math.min(420, prev + Math.floor(Math.random() * 21) - 10)));
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  if (!isDiagnosticPanelOpen) return null;

  return (
    <motion.aside
      initial={{ width: 0, opacity: 0 }}
      animate={{ width: 300, opacity: 1 }}
      exit={{ width: 0, opacity: 0 }}
      transition={{ duration: 0.2 }}
      className="h-screen bg-[#06070a]/90 border-l border-slate-800/60 backdrop-blur-2xl flex flex-col p-4 z-20 overflow-y-auto space-y-5 select-none shrink-0"
    >
      <div className="flex items-center justify-between border-b border-slate-800/50 pb-3">
        <span className="text-xs font-bold font-mono tracking-wider text-slate-200 uppercase flex items-center gap-2">
          <FiZap className="text-amber-400" /> SYSTEM DIAGNOSTICS
        </span>
        <span className="flex items-center space-x-1 text-[10px] font-mono text-emerald-400 bg-emerald-950/60 border border-emerald-800/60 px-2 py-0.5 rounded-full">
          <FiCheckCircle /> ONLINE
        </span>
      </div>

      {/* Realtime Metrics Cards */}
      <div className="grid grid-cols-2 gap-2 text-xs font-mono">
        <div className="bg-slate-900/80 border border-slate-800/80 p-3 rounded-xl flex flex-col justify-between space-y-1">
          <span className="text-[10px] text-slate-500 uppercase">Avg Latency</span>
          <span className="text-base font-bold text-indigo-400">{latency} ms</span>
        </div>
        <div className="bg-slate-900/80 border border-slate-800/80 p-3 rounded-xl flex flex-col justify-between space-y-1">
          <span className="text-[10px] text-slate-500 uppercase">Token Count</span>
          <span className="text-base font-bold text-emerald-400">{tokens}</span>
        </div>
      </div>

      {/* Vector Retrieval Context */}
      <div className="space-y-2">
        <span className="text-[11px] font-mono font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
          <FiDatabase className="text-indigo-400" /> RAG Grounded Sources ({activeSources.length})
        </span>

        {activeSources.length === 0 ? (
          <div className="bg-slate-900/40 border border-slate-800/60 rounded-xl p-3 text-[11px] text-slate-500 text-center">
            No active search vectors retrieved in current query.
          </div>
        ) : (
          <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
            {activeSources.map((source, idx) => (
              <div
                key={idx}
                className="bg-slate-900/90 border border-slate-800 p-2.5 rounded-xl space-y-1 text-xs"
              >
                <div className="flex justify-between items-center text-indigo-300 font-medium">
                  <span className="truncate pr-2">{source.title || "Reference Doc"}</span>
                  <span className="text-[10px] font-mono text-emerald-400 bg-emerald-950/80 px-1.5 py-0.5 rounded border border-emerald-800/60">
                    {Math.round((source.relevance_score || 0.9) * 100)}%
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 line-clamp-2 leading-relaxed">
                  "{source.content}"
                </p>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Memory Graph Status */}
      <div className="space-y-2 border-t border-slate-800/50 pt-3">
        <span className="text-[11px] font-mono font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
          <FiCpu className="text-emerald-400" /> Vector Memory State
        </span>
        <div className="bg-slate-900/80 border border-slate-800/80 p-3 rounded-xl space-y-2 text-xs">
          <div className="flex justify-between text-slate-300">
            <span>ChromaDB Nodes:</span>
            <span className="font-mono text-indigo-400 font-bold">1,420</span>
          </div>
          <div className="flex justify-between text-slate-300">
            <span>Embedding Dimensions:</span>
            <span className="font-mono text-slate-400">768 (Gemini)</span>
          </div>
          <div className="flex justify-between text-slate-300">
            <span>Similarity Metric:</span>
            <span className="font-mono text-slate-400">Cosine Distance</span>
          </div>
        </div>
      </div>
    </motion.aside>
  );
}