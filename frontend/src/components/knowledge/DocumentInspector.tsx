"use client";

import { motion } from "framer-motion";
import { FiX, FiFileText, FiLayers, FiDatabase, FiTag } from "react-icons/fi";
import { KnowledgeDocument } from "@/types";

interface DocumentInspectorProps {
  document: KnowledgeDocument;
  onClose: () => void;
}

export default function DocumentInspector({ document, onClose }: DocumentInspectorProps) {
  return (
    <motion.div
      initial={{ x: "100%", opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      exit={{ x: "100%", opacity: 0 }}
      transition={{ type: "spring", stiffness: 300, damping: 30 }}
      className="w-96 h-full bg-[#08090d]/95 border-l border-slate-800/80 backdrop-blur-2xl flex flex-col p-5 z-30 shadow-2xl overflow-hidden shrink-0"
    >
      {/* Drawer Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center space-x-2 truncate pr-2">
          <FiFileText className="text-indigo-400 shrink-0" size={18} />
          <h2 className="text-sm font-bold text-slate-100 truncate">{document.name}</h2>
        </div>
        <button
          onClick={onClose}
          className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
        >
          <FiX size={16} />
        </button>
      </div>

      {/* Metadata Section */}
      <div className="my-4 p-3 bg-slate-900/80 border border-slate-800/80 rounded-xl space-y-2 text-xs font-mono">
        <div className="flex justify-between text-slate-400">
          <span>Folder Location:</span>
          <span className="text-indigo-300 font-bold flex items-center gap-1">
            <FiTag size={12} /> {document.folder || "Root"}
          </span>
        </div>
        <div className="flex justify-between text-slate-400">
          <span>Total Chunks:</span>
          <span className="text-emerald-400 font-bold">{document.chunkCount}</span>
        </div>
        <div className="flex justify-between text-slate-400">
          <span>File Size:</span>
          <span className="text-slate-300">{(document.sizeBytes / 1024).toFixed(1)} KB</span>
        </div>
        <div className="flex justify-between text-slate-400">
          <span>Ingested At:</span>
          <span className="text-slate-300">
            {new Date(document.uploadedAt).toLocaleDateString()}
          </span>
        </div>
      </div>

      {/* Chunk Viewer Header */}
      <div className="flex items-center space-x-2 mb-3">
        <FiLayers className="text-indigo-400" size={14} />
        <span className="text-xs font-mono font-bold text-slate-300 uppercase tracking-wider">
          Extracted Vectors & Chunks
        </span>
      </div>

      {/* Chunk List Container */}
      <div className="flex-1 overflow-y-auto space-y-3 pr-1">
        {document.chunks && document.chunks.length > 0 ? (
          document.chunks.map((chunk, idx) => (
            <div
              key={chunk.id || idx}
              className="bg-slate-900/90 border border-slate-800/90 p-3 rounded-xl space-y-2 text-xs"
            >
              <div className="flex justify-between items-center font-mono text-[10px] text-slate-500">
                <span>CHUNK #{idx + 1}</span>
                <span className="text-indigo-400 flex items-center gap-1">
                  <FiDatabase size={10} /> Vector 768-d
                </span>
              </div>
              <p className="text-slate-300 leading-relaxed font-sans">{chunk.text}</p>
            </div>
          ))
        ) : (
          <div className="h-40 flex flex-col items-center justify-center text-center text-slate-500 text-xs space-y-2">
            <FiDatabase size={24} className="text-slate-600 animate-pulse" />
            <p>Indexed into ChromaDB vector store. Preview chunks extracted during search queries.</p>
          </div>
        )}
      </div>
    </motion.div>
  );
}