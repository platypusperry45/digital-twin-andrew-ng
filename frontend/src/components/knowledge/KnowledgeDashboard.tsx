"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  FiUploadCloud,
  FiFileText,
  FiTrash2,
  FiSearch,
  FiFolder,
  FiDatabase,
  FiEye,
  FiCheckCircle,
} from "react-icons/fi";
import { useKnowledgeStore } from "@/store/useKnowledgeStore";
import DocumentInspector from "./DocumentInspector";

export default function KnowledgeDashboard() {
  const {
    documents,
    isLoading,
    loadDocuments,
    uploadDocument,
    deleteDocument,
    searchQuery,
    setSearchQuery,
    selectedDocId,
    setSelectedDocId,
  } = useKnowledgeStore();

  const [isDragging, setIsDragging] = useState(false);

  useEffect(() => {
    loadDocuments();
  }, [loadDocuments]);

  const handleFileUpload = async (files: FileList | null) => {
    if (!files || files.length === 0) return;
    for (let i = 0; i < files.length; i++) {
      await uploadDocument(files[i]);
    }
  };

  const filteredDocs = documents.filter((doc) =>
    doc.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const selectedDoc = documents.find((d) => d.id === selectedDocId);

  return (
    <div className="flex-1 flex h-full overflow-hidden bg-[#050508] text-slate-100 relative">
      {/* Main Container */}
      <div className="flex-1 flex flex-col p-6 overflow-y-auto space-y-6 max-w-6xl mx-auto w-full">
        {/* Header & Subtitle */}
        <div className="flex justify-between items-end border-b border-slate-800/60 pb-5">
          <div>
            <h1 className="text-xl font-bold tracking-wide text-slate-100 flex items-center gap-2">
              <FiDatabase className="text-indigo-400" /> Grounding Knowledge Index
            </h1>
            <p className="text-xs text-slate-400 mt-1">
              Upload course materials, lecture transcripts, and books to build Andrew Ng's custom RAG vector store.
            </p>
          </div>

          <div className="relative">
            <FiSearch className="absolute left-3 top-2.5 text-slate-500" size={14} />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search knowledge base..."
              className="pl-9 pr-4 py-1.5 bg-slate-900 border border-slate-800 rounded-xl text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
            />
          </div>
        </div>

        {/* Drag & Drop Upload Zone */}
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setIsDragging(true);
          }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={(e) => {
            e.preventDefault();
            setIsDragging(false);
            handleFileUpload(e.dataTransfer.files);
          }}
          className={`relative border-2 border-dashed rounded-2xl p-8 flex flex-col items-center justify-center text-center transition-all ${
            isDragging
              ? "border-indigo-500 bg-indigo-950/20 shadow-lg shadow-indigo-500/10"
              : "border-slate-800 hover:border-slate-700 bg-slate-950/40"
          }`}
        >
          <input
            type="file"
            multiple
            accept=".pdf,.docx,.md,.txt"
            onChange={(e) => handleFileUpload(e.target.files)}
            className="absolute inset-0 opacity-0 cursor-pointer"
          />
          <div className="w-12 h-12 rounded-full bg-indigo-600/20 border border-indigo-500/40 flex items-center justify-center text-indigo-400 mb-3 shadow-md">
            <FiUploadCloud size={24} />
          </div>
          <p className="text-sm font-semibold text-slate-200">
            Drag and drop documents here, or <span className="text-indigo-400 underline">browse</span>
          </p>
          <p className="text-xs text-slate-500 mt-1">Supports PDF, DOCX, Markdown, and TXT files</p>
        </div>

        {/* Knowledge Catalog List */}
        <div className="space-y-3">
          <div className="flex justify-between items-center text-xs font-mono text-slate-400 px-1">
            <span>INGESTED DOCUMENTS ({filteredDocs.length})</span>
            {isLoading && <span className="text-indigo-400 animate-pulse">Indexing vector embeddings...</span>}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {filteredDocs.map((doc) => (
              <motion.div
                key={doc.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`group relative bg-slate-900/80 border p-4 rounded-2xl flex items-center justify-between hover:border-indigo-500/50 transition-all ${
                  selectedDocId === doc.id ? "border-indigo-500 bg-indigo-950/20" : "border-slate-800/80"
                }`}
              >
                <div className="flex items-center space-x-3 overflow-hidden pr-2">
                  <div className="w-10 h-10 rounded-xl bg-slate-800 border border-slate-700/60 flex items-center justify-center text-indigo-400 shrink-0">
                    <FiFileText size={18} />
                  </div>
                  <div className="flex flex-col overflow-hidden">
                    <span className="text-xs font-bold text-slate-200 truncate">{doc.name}</span>
                    <div className="flex items-center space-x-2 text-[10px] text-slate-400 font-mono mt-0.5">
                      <span className="flex items-center gap-1">
                        <FiFolder size={10} /> {doc.folder || "Root"}
                      </span>
                      <span>•</span>
                      <span>{doc.chunkCount} chunks</span>
                      <span>•</span>
                      <span className="text-emerald-400 flex items-center gap-1">
                        <FiCheckCircle size={10} /> Indexed
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => setSelectedDocId(doc.id)}
                    className="p-2 rounded-lg bg-slate-800/60 text-slate-300 hover:text-indigo-300 hover:bg-slate-800 transition-colors"
                    title="Inspect Chunks"
                  >
                    <FiEye size={14} />
                  </button>
                  <button
                    onClick={() => deleteDocument(doc.id)}
                    className="p-2 rounded-lg bg-slate-800/60 text-slate-400 hover:text-rose-400 hover:bg-slate-800 transition-colors"
                    title="Delete Document"
                  >
                    <FiTrash2 size={14} />
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* Side Inspector Drawer */}
      <AnimatePresence>
        {selectedDoc && (
          <DocumentInspector document={selectedDoc} onClose={() => setSelectedDocId(null)} />
        )}
      </AnimatePresence>
    </div>
  );
}