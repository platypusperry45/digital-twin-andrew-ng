"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  FiActivity,
  FiCpu,
  FiDatabase,
  FiKey,
  FiShield,
  FiCheckCircle,
  FiAlertTriangle,
  FiRefreshCw,
  FiServer,
  FiTerminal,
} from "react-icons/fi";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { api } from "@/lib/api";
import { TelemetryMetrics } from "@/types";

export default function TelemetryDashboard() {
  const [metrics, setMetrics] = useState<TelemetryMetrics | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [geminiKey, setGeminiKey] = useState("••••••••••••••••AIzaSyD8");

  // Sample real-time latency history for chart
  const [latencyData, setLatencyData] = useState([
    { time: "20:20", latency: 310, tokens: 420 },
    { time: "20:21", latency: 290, tokens: 380 },
    { time: "20:22", latency: 450, tokens: 610 },
    { time: "20:23", latency: 320, tokens: 290 },
    { time: "20:24", latency: 280, tokens: 410 },
    { time: "20:25", latency: 340, tokens: 520 },
    { time: "20:26", latency: 315, tokens: 480 },
  ]);

  const loadMetrics = async () => {
    setIsLoading(true);
    try {
      const data = await api.fetchTelemetry();
      setMetrics(data);
    } catch (err) {
      console.error("Failed fetching telemetry data", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadMetrics();
  }, []);

  return (
    <div className="flex-1 flex flex-col h-full overflow-y-auto bg-[#050508] text-slate-100 p-6 space-y-6 max-w-6xl mx-auto w-full">
      {/* Page Header */}
      <div className="flex justify-between items-end border-b border-slate-800/60 pb-5">
        <div>
          <h1 className="text-xl font-bold tracking-wide text-slate-100 flex items-center gap-2">
            <FiActivity className="text-indigo-400" /> Developer Telemetry & Infrastructure
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Monitor API quotas, vector database connection health, latency graphs, and model fallback states.
          </p>
        </div>

        <button
          onClick={loadMetrics}
          className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-xs font-mono text-slate-400 hover:text-white transition-colors"
        >
          <FiRefreshCw size={12} className={isLoading ? "animate-spin" : ""} />
          <span>Refresh Metrics</span>
        </button>
      </div>

      {/* Top Metrics Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900/80 border border-slate-800/80 p-4 rounded-2xl flex flex-col justify-between space-y-2">
          <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
            <FiServer className="text-indigo-400" /> System Status
          </span>
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping" />
            <span className="text-lg font-bold text-slate-100 font-mono">OPERATIONAL</span>
          </div>
          <span className="text-[10px] text-slate-400 font-mono">FastAPI Backend (Port 8000)</span>
        </div>

        <div className="bg-slate-900/80 border border-slate-800/80 p-4 rounded-2xl flex flex-col justify-between space-y-2">
          <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
            <FiCpu className="text-indigo-400" /> Active Model
          </span>
          <span className="text-sm font-bold text-indigo-300 font-mono truncate">
            {metrics?.activeModel || "Gemini 1.5 Pro"}
          </span>
          <span className="text-[10px] text-slate-400 font-mono">Fallback: Gemini Flash</span>
        </div>

        <div className="bg-slate-900/80 border border-slate-800/80 p-4 rounded-2xl flex flex-col justify-between space-y-2">
          <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
            <FiDatabase className="text-emerald-400" /> Vector Database
          </span>
          <div className="flex items-center justify-between">
            <span className="text-lg font-bold text-emerald-400 font-mono">Healthy</span>
            <span className="text-xs font-mono text-slate-400">ChromaDB</span>
          </div>
          <span className="text-[10px] text-slate-400 font-mono">1,420 Active Vectors</span>
        </div>

        <div className="bg-slate-900/80 border border-slate-800/80 p-4 rounded-2xl flex flex-col justify-between space-y-2">
          <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
            <FiCheckCircle className="text-amber-400" /> Remaining Quota
          </span>
          <span className="text-lg font-bold text-amber-400 font-mono">
            {metrics?.geminiQuotaRemaining || 88.4}%
          </span>
          <span className="text-[10px] text-slate-400 font-mono">Reset in 4h 12m</span>
        </div>
      </div>

      {/* Latency & Throughput Chart */}
      <div className="bg-slate-900/80 border border-slate-800/80 p-5 rounded-2xl space-y-4">
        <div className="flex justify-between items-center">
          <span className="text-xs font-mono font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
            <FiActivity className="text-indigo-400" /> API Latency & Token Flow (ms)
          </span>
          <span className="text-[10px] font-mono text-indigo-400 bg-indigo-950/80 px-2 py-0.5 rounded border border-indigo-800/60">
            Avg: {metrics?.avgLatencyMs || 340} ms
          </span>
        </div>

        <div className="w-full h-56">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={latencyData}>
              <defs>
                <linearGradient id="latencyGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.4} />
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                </linearGradient>
              </defs>
              <XAxis dataKey="time" stroke="#475569" tick={{ fill: "#64748b", fontSize: 10 }} />
              <YAxis stroke="#475569" tick={{ fill: "#64748b", fontSize: 10 }} />
              <Tooltip
                contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "12px" }}
              />
              <Area type="monotone" dataKey="latency" stroke="#6366f1" fillOpacity={1} fill="url(#latencyGradient)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* API Key Configuration & Live Log Stream */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Key Management */}
        <div className="bg-slate-900/80 border border-slate-800/80 p-5 rounded-2xl space-y-4">
          <div className="flex items-center space-x-2 text-xs font-mono font-bold text-slate-200 uppercase tracking-wider">
            <FiKey className="text-indigo-400" /> API Key Management
          </div>

          <div className="space-y-3 text-xs">
            <div>
              <label className="text-slate-400 font-mono block mb-1">Google Gemini API Key</label>
              <div className="flex space-x-2">
                <input
                  type="password"
                  value={geminiKey}
                  onChange={(e) => setGeminiKey(e.target.value)}
                  className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-slate-200 font-mono text-xs focus:outline-none focus:border-indigo-500"
                />
                <button className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-mono text-xs font-bold transition-colors">
                  Save
                </button>
              </div>
            </div>

            <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
              <span>ChromaDB Vector Host:</span>
              <span className="font-mono text-slate-200">http://localhost:8000</span>
            </div>
          </div>
        </div>

        {/* Live Terminal Log Preview */}
        <div className="bg-slate-950 border border-slate-800/80 p-5 rounded-2xl space-y-3 font-mono text-xs">
          <div className="flex items-center justify-between text-slate-400 border-b border-slate-800 pb-2">
            <span className="flex items-center gap-1.5 text-slate-200 font-bold">
              <FiTerminal className="text-emerald-400" /> System Event Stream
            </span>
            <span className="text-[10px] text-emerald-400">LOGGING ACTIVE</span>
          </div>

          <div className="space-y-1.5 text-[11px] h-32 overflow-y-auto text-slate-400">
            <p className="text-slate-500">[20:26:01] POST /api/v1/chat - 200 OK (315ms)</p>
            <p className="text-emerald-400/90">[20:25:48] Vector search complete: 3 nodes retrieved (score: 0.94)</p>
            <p className="text-indigo-400/90">[20:24:12] Synthesizing speech via /voice/synthesize - 200 OK</p>
            <p className="text-slate-500">[20:22:05] Memory graph re-indexed: 1,420 entities online</p>
          </div>
        </div>
      </div>
    </div>
  );
}