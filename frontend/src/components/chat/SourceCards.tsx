"use client";

import React from "react";
import { motion } from "framer-motion";
import { FiBookOpen, FiX } from "react-icons/fi";

interface SourceCardsProps {
  sources: any[];
  onClose: () => void;
}

export default function SourceCards({ sources, onClose }: SourceCardsProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 30 }}
      className="fixed bottom-6 right-6 z-50 max-w-md w-full glass-panel p-5 rounded-2xl border border-slate-700/60 shadow-2xl"
    >
      <div className="flex justify-between items-center mb-3 pb-2 border-b border-slate-800">
        <h3 className="font-bold text-xs text-indigo-400 flex items-center gap-2 tracking-wide font-mono">
          <FiBookOpen /> GROUNDED RAG SOURCE PASSAGES
        </h3>
        <button onClick={onClose} className="p-1 text-slate-400 hover:text-white rounded-md transition-colors">
          <FiX />
        </button>
      </div>

      <div className="space-y-2.5 max-h-64 overflow-y-auto pr-1 text-xs text-slate-300 font-mono">
        {sources.map((src, i) => (
          <div key={i} className="p-2.5 bg-slate-950/80 rounded-lg border border-slate-800/80">
            <span className="text-[10px] text-indigo-400 font-bold block mb-1">// PASSAGE {i + 1}</span>
            <p className="text-slate-300 leading-relaxed text-[11px]">{String(src)}</p>
          </div>
        ))}
      </div>
    </motion.div>
  );
}