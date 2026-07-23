"use client";

import { useState } from "react";
import MemoryGraph3D from "../canvas/MemoryGraph3D";
import { FiCpu, FiLayers, FiZap, FiSearch } from "react-icons/fi";

export default function MemoryDashboard() {
  const [filterQuery, setFilterQuery] = useState("");

  const sampleMemories = [
    {
      concept: "Supervised Learning",
      category: "Foundational ML",
      similarityScore: 0.98,
      lastRetrieved: "2 mins ago",
    },
    {
      concept: "Gradient Descent Optimization",
      category: "Mathematics & Optimization",
      similarityScore: 0.94,
      lastRetrieved: "15 mins ago",
    },
    {
      concept: "Data-Centric AI Iteration",
      category: "Engineering Strategy",
      similarityScore: 0.89,
      lastRetrieved: "1 hour ago",
    },
    {
      concept: "Bias-Variance Tradeoff",
      category: "Model Evaluation",
      similarityScore: 0.86,
      lastRetrieved: "3 hours ago",
    },
  ];

  return (
    <div className="flex-1 flex h-full overflow-hidden bg-[#050508] text-slate-100">
      {/* Left / Main 3D Memory Canvas */}
      <div className="flex-1 flex flex-col relative border-r border-slate-800/60">
        <div className="p-4 border-b border-slate-800/60 bg-[#08090d]/80 backdrop-blur-xl flex items-center justify-between z-10">
          <div>
            <h1 className="text-base font-bold text-slate-100 flex items-center gap-2">
              <FiCpu className="text-emerald-400" /> Vector Memory Graph
            </h1>
            <p className="text-xs text-slate-400">
              Interactive visualization of semantic memory clusters and relational embeddings.
            </p>
          </div>
          <span className="text-xs font-mono bg-emerald-950/80 border border-emerald-800/60 text-emerald-300 px-3 py-1 rounded-full flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" /> 1,420 Nodes Active
          </span>
        </div>

        <div className="flex-1 relative">
          <MemoryGraph3D />
        </div>
      </div>

      {/* Right Similarity & Retrieval Matrix */}
      <div className="w-80 h-full bg-[#08090d]/90 border-l border-slate-800/80 flex flex-col p-4 space-y-4 overflow-y-auto shrink-0">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <span className="text-xs font-bold font-mono text-slate-200 uppercase tracking-wider flex items-center gap-1.5">
            <FiZap className="text-amber-400" /> Memory Matrix
          </span>
        </div>

        {/* Search Filter */}
        <div className="relative">
          <FiSearch className="absolute left-3 top-2.5 text-slate-500" size={13} />
          <input
            type="text"
            value={filterQuery}
            onChange={(e) => setFilterQuery(e.target.value)}
            placeholder="Filter memories..."
            className="w-full pl-8 pr-3 py-1.5 bg-slate-900 border border-slate-800 rounded-xl text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
          />
        </div>

        {/* Memory Clusters */}
        <div className="space-y-2">
          <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider">
            Recent Vector Retrievals
          </span>
          <div className="space-y-2">
            {sampleMemories
              .filter((m) => m.concept.toLowerCase().includes(filterQuery.toLowerCase()))
              .map((item, idx) => (
                <div
                  key={idx}
                  className="bg-slate-900/80 border border-slate-800/80 p-3 rounded-xl space-y-1.5 text-xs hover:border-slate-700 transition-colors"
                >
                  <div className="flex justify-between items-center text-slate-200 font-medium">
                    <span className="truncate pr-1">{item.concept}</span>
                    <span className="text-[10px] font-mono text-emerald-400 bg-emerald-950/80 px-1.5 py-0.5 rounded border border-emerald-800/60 shrink-0">
                      {(item.similarityScore * 100).toFixed(0)}%
                    </span>
                  </div>
                  <div className="flex justify-between text-[10px] font-mono text-slate-400">
                    <span>{item.category}</span>
                    <span className="text-slate-500">{item.lastRetrieved}</span>
                  </div>
                </div>
              ))}
          </div>
        </div>

        {/* Storage Health Summary */}
        <div className="mt-auto bg-slate-900/60 border border-slate-800/80 p-3 rounded-xl space-y-2 text-xs font-mono">
          <div className="flex items-center justify-between text-indigo-300 font-bold">
            <span className="flex items-center gap-1">
              <FiLayers size={13} /> ChromaDB Engine
            </span>
            <span>v0.5.0</span>
          </div>
          <p className="text-[11px] text-slate-400 font-sans leading-relaxed">
            All conversational turns are continuously chunked, embedded, and indexed into vector memory.
          </p>
        </div>
      </div>
    </div>
  );
}