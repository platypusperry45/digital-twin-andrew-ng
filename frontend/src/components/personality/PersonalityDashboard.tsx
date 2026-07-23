"use client";

import { useEffect } from "react";
import { motion } from "framer-motion";
import {
  FiSliders,
  FiRotateCcw,
  FiSave,
  FiBookOpen,
  FiCheck,
  FiAward,
} from "react-icons/fi";
import { usePersonalityStore } from "@/store/usePersonalityStore";
import PersonalityRadar from "./PersonalityRadar";

export default function PersonalityDashboard() {
  const { config, isLoading, loadConfig, updateConfig } = usePersonalityStore();

  useEffect(() => {
    loadConfig();
  }, [loadConfig]);

  const handleReset = () => {
    updateConfig({
      tone: "pedagogical",
      analogiesFrequency: 85,
      firstPrinciplesFocus: 90,
      codeExplanationDepth: "high",
      mathRigorLevel: "balanced",
    });
  };

  return (
    <div className="flex-1 flex h-full overflow-hidden bg-[#050508] text-slate-100">
      {/* Left Control Sliders */}
      <div className="flex-1 flex flex-col p-6 overflow-y-auto space-y-6 max-w-4xl mx-auto w-full">
        <div className="flex justify-between items-end border-b border-slate-800/60 pb-5">
          <div>
            <h1 className="text-xl font-bold tracking-wide text-slate-100 flex items-center gap-2">
              <FiSliders className="text-indigo-400" /> Pedagogy & Persona Configuration
            </h1>
            <p className="text-xs text-slate-400 mt-1">
              Tune how Andrew Ng’s digital twin structures intuitions, mathematical derivations, and technical explanations.
            </p>
          </div>

          <button
            onClick={handleReset}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-xs font-mono text-slate-400 hover:text-white transition-colors"
          >
            <FiRotateCcw size={12} />
            <span>Reset Defaults</span>
          </button>
        </div>

        {/* Configuration Sliders & Selectors */}
        <div className="space-y-6">
          {/* Tone Selector */}
          <div className="bg-slate-900/80 border border-slate-800/80 p-5 rounded-2xl space-y-3">
            <div className="flex justify-between items-center">
              <label className="text-sm font-bold text-slate-200">Teaching & Pedagogical Tone</label>
              <span className="text-xs font-mono text-indigo-400 capitalize">{config.tone}</span>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
              {(["pedagogical", "encouraging", "rigorous", "concise"] as const).map((tone) => (
                <button
                  key={tone}
                  onClick={() => updateConfig({ tone })}
                  className={`py-2 px-3 rounded-xl border text-xs font-mono capitalize transition-all ${
                    config.tone === tone
                      ? "bg-indigo-600 border-indigo-500 text-white font-bold shadow-md shadow-indigo-600/20"
                      : "bg-slate-950/60 border-slate-800/80 text-slate-400 hover:text-slate-200"
                  }`}
                >
                  {tone}
                </button>
              ))}
            </div>
          </div>

          {/* Analogies Slider */}
          <div className="bg-slate-900/80 border border-slate-800/80 p-5 rounded-2xl space-y-3">
            <div className="flex justify-between items-center">
              <label className="text-sm font-bold text-slate-200">Intuitive Analogy Frequency</label>
              <span className="text-xs font-mono text-emerald-400">{config.analogiesFrequency}%</span>
            </div>
            <input
              type="range"
              min={0}
              max={100}
              value={config.analogiesFrequency}
              onChange={(e) => updateConfig({ analogiesFrequency: Number(e.target.value) })}
              className="w-full accent-indigo-500 cursor-pointer"
            />
            <p className="text-xs text-slate-400">
              Higher values ensure complex algorithms (e.g., Backpropagation, Attention) start with relatable real-world metaphors.
            </p>
          </div>

          {/* First Principles Focus */}
          <div className="bg-slate-900/80 border border-slate-800/80 p-5 rounded-2xl space-y-3">
            <div className="flex justify-between items-center">
              <label className="text-sm font-bold text-slate-200">First-Principles Emphasis</label>
              <span className="text-xs font-mono text-emerald-400">{config.firstPrinciplesFocus}%</span>
            </div>
            <input
              type="range"
              min={0}
              max={100}
              value={config.firstPrinciplesFocus}
              onChange={(e) => updateConfig({ firstPrinciplesFocus: Number(e.target.value) })}
              className="w-full accent-indigo-500 cursor-pointer"
            />
            <p className="text-xs text-slate-400">
              Forces answers to ground concepts in core linear algebra, calculus, and fundamental cost function definitions.
            </p>
          </div>

          {/* Math Rigor Level */}
          <div className="bg-slate-900/80 border border-slate-800/80 p-5 rounded-2xl space-y-3">
            <div className="flex justify-between items-center">
              <label className="text-sm font-bold text-slate-200">Mathematical Rigor Level</label>
              <span className="text-xs font-mono text-indigo-400 capitalize">{config.mathRigorLevel}</span>
            </div>
            <div className="grid grid-cols-3 gap-3">
              {(["intuitive", "balanced", "formal"] as const).map((level) => (
                <button
                  key={level}
                  onClick={() => updateConfig({ mathRigorLevel: level })}
                  className={`py-2 px-3 rounded-xl border text-xs font-mono capitalize transition-all ${
                    config.mathRigorLevel === level
                      ? "bg-indigo-600 border-indigo-500 text-white font-bold shadow-md"
                      : "bg-slate-950/60 border-slate-800/80 text-slate-400 hover:text-slate-200"
                  }`}
                >
                  {level}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Right Radar Preview Drawer */}
      <div className="w-80 h-full bg-[#08090d]/90 border-l border-slate-800/80 flex flex-col p-5 space-y-6 overflow-y-auto shrink-0">
        <div className="flex items-center space-x-2 text-xs font-bold font-mono text-slate-200 uppercase tracking-wider border-b border-slate-800 pb-3">
          <FiAward className="text-indigo-400" /> Persona Profile Radar
        </div>

        {/* Radar Graphic */}
        <PersonalityRadar config={config} />

        {/* Persona Active Summary */}
        <div className="bg-slate-900/90 border border-slate-800/90 p-4 rounded-2xl space-y-3 text-xs">
          <span className="font-mono text-[10px] text-slate-500 uppercase tracking-wider block">
            System Prompt Override
          </span>
          <p className="text-slate-300 leading-relaxed font-sans">
            "You are Andrew Ng. Always start by building intuition first. Use structured analogies, clear step-by-step reasoning, and maintain a warm, encouraging tone."
          </p>
        </div>
      </div>
    </div>
  );
}