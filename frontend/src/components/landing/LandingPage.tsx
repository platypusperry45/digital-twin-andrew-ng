"use client";

import { motion } from "framer-motion";
import {
  FiArrowRight,
  FiCpu,
  FiDatabase,
  FiLayers,
  FiZap,
  FiBookOpen,
  FiSliders,
} from "react-icons/fi";
import ParticleOrb from "../canvas/ParticleOrb";

interface LandingPageProps {
  onEnterOS: () => void;
}

export default function LandingPage({ onEnterOS }: LandingPageProps) {
  const features = [
    {
      icon: FiCpu,
      title: "Pedagogical Intelligence",
      description:
        "Trained to structure answers with intuitive analogies, step-by-step calculus derivations, and first-principles clarity.",
    },
    {
      icon: FiDatabase,
      title: "ChromaDB RAG Ingestion",
      description:
        "Grounded in Stanford CS229 lecture notes, Machine Learning Yearning, and custom document libraries.",
    },
    {
      icon: FiLayers,
      title: "3D Neural Memory",
      description:
        "Visualizes semantic concepts, vector similarity distances, and conversational context clusters in real-time.",
    },
  ];

  return (
    <div className="min-h-screen bg-[#040407] text-slate-100 flex flex-col justify-between relative overflow-hidden select-none">
      {/* Dynamic Background Gradients */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[450px] bg-indigo-600/10 blur-[140px] pointer-events-none rounded-full" />
      <div className="absolute bottom-0 right-0 w-[600px] h-[400px] bg-emerald-600/10 blur-[160px] pointer-events-none rounded-full" />

      {/* Landing Header */}
      <header className="max-w-7xl mx-auto w-full px-8 py-6 flex justify-between items-center z-10">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-2xl bg-indigo-600/20 border border-indigo-500/40 flex items-center justify-center text-indigo-400 font-bold shadow-lg shadow-indigo-500/20">
            AN
          </div>
          <span className="font-bold text-sm tracking-wider uppercase">
            Andrew Ng Digital Twin <span className="text-indigo-400 font-mono text-xs ml-1">v2.5</span>
          </span>
        </div>

        <button
          onClick={onEnterOS}
          className="flex items-center space-x-2 px-5 py-2.5 rounded-full bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-xs shadow-lg shadow-indigo-600/30 hover:scale-105 transition-all"
        >
          <span>Launch AI-OS Console</span>
          <FiArrowRight />
        </button>
      </header>

      {/* Hero Section */}
      <main className="max-w-6xl mx-auto w-full px-8 py-12 flex flex-col md:flex-row items-center justify-between z-10 gap-12">
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6 }}
          className="flex-1 space-y-6"
        >
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-slate-900/90 border border-slate-800 text-xs font-mono text-indigo-300">
            <FiZap className="text-amber-400" />
            <span>"Let's build some intuition first."</span>
          </div>

          <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight leading-tight text-white">
            The Interactive AI Twin of <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-300 to-emerald-400">Andrew Ng</span>
          </h1>

          <p className="text-slate-400 text-sm md:text-base leading-relaxed max-w-xl">
            A flagship AI operating system engineered for intuitive machine learning instruction, data-centric AI strategy, and vector-grounded pedagogical exploration.
          </p>

          <div className="flex items-center space-x-4 pt-2">
            <button
              onClick={onEnterOS}
              className="flex items-center space-x-2 px-7 py-3.5 rounded-2xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-sm shadow-xl shadow-indigo-600/30 transition-all hover:scale-105"
            >
              <span>Explore Workspace</span>
              <FiArrowRight size={16} />
            </button>
          </div>
        </motion.div>

        {/* Hero 3D Orb Visualizer */}
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="flex-1 flex justify-center"
        >
          <ParticleOrb />
        </motion.div>
      </main>

      {/* Feature Cards Grid */}
      <section className="max-w-6xl mx-auto w-full px-8 py-10 z-10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {features.map((feat, idx) => {
            const Icon = feat.icon;
            return (
              <div
                key={idx}
                className="bg-slate-900/40 border border-slate-800/80 p-6 rounded-3xl space-y-3 backdrop-blur-xl hover:border-indigo-500/40 transition-all"
              >
                <div className="w-10 h-10 rounded-2xl bg-indigo-950/80 border border-indigo-800/60 flex items-center justify-center text-indigo-400">
                  <Icon size={20} />
                </div>
                <h3 className="text-sm font-bold text-slate-100">{feat.title}</h3>
                <p className="text-xs text-slate-400 leading-relaxed">{feat.description}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* Footer */}
      <footer className="max-w-7xl mx-auto w-full px-8 py-6 border-t border-slate-800/60 flex justify-between items-center text-xs text-slate-500 font-mono z-10">
        <span>Andrew Ng Digital Twin AI-OS v2.5</span>
        <span>Powered by Gemini 1.5 Pro & ChromaDB</span>
      </footer>
    </div>
  );
}