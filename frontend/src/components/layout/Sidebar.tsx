"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  FiMessageSquare,
  FiBookOpen,
  FiCpu,
  FiSliders,
  FiActivity,
  FiSettings,
  FiShield,
  FiPlus,
  FiSearch,
  FiPin,
  FiTrash2,
  FiChevronLeft,
  FiChevronRight,
} from "react-icons/fi";
import { useUiStore } from "@/store/useUiStore";
import { useChatStore } from "@/store/useChatStore";

export default function Sidebar() {
  const { activeTab, setActiveTab, isSidebarOpen, toggleSidebar } = useUiStore();
  const {
    sessions,
    activeSessionId,
    createSession,
    setActiveSession,
    deleteSession,
    togglePinSession,
    searchQuery,
    setSearchQuery,
  } = useChatStore();

  const [hoveredSession, setHoveredSession] = useState<string | null>(null);

  const filteredSessions = sessions.filter((s) =>
    s.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const pinnedSessions = filteredSessions.filter((s) => s.isPinned);
  const unpinnedSessions = filteredSessions.filter((s) => !s.isPinned);

  const navItems = [
    { id: "chat", label: "Chat Console", icon: FiMessageSquare },
    { id: "knowledge", label: "Knowledge Base", icon: FiBookOpen },
    { id: "memory", label: "Memory Graph", icon: FiCpu },
    { id: "personality", label: "Personality Tuning", icon: FiSliders },
    { id: "developer", label: "Developer Telemetry", icon: FiActivity },
    { id: "settings", label: "System Settings", icon: FiSettings },
    { id: "admin", label: "Admin Console", icon: FiShield },
  ] as const;

  return (
    <motion.aside
      animate={{ width: isSidebarOpen ? 280 : 72 }}
      transition={{ duration: 0.2, ease: "easeInOut" }}
      className="relative h-screen bg-[#06070a]/90 border-r border-slate-800/60 backdrop-blur-2xl flex flex-col z-30 select-none overflow-hidden shrink-0"
    >
      {/* Sidebar Header */}
      <div className="p-4 flex items-center justify-between border-b border-slate-800/50">
        <div className="flex items-center space-x-3 overflow-hidden">
          <div className="w-9 h-9 rounded-xl bg-indigo-600/20 border border-indigo-500/40 flex items-center justify-center shrink-0 text-indigo-400 font-bold shadow-lg shadow-indigo-500/10">
            AN
          </div>
          {isSidebarOpen && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex flex-col overflow-hidden"
            >
              <span className="text-xs font-bold tracking-widest text-slate-100 uppercase truncate">
                ANDREW NG
              </span>
              <span className="text-[10px] font-mono text-indigo-400 truncate">
                DIGITAL TWIN AI-OS
              </span>
            </motion.div>
          )}
        </div>

        <button
          onClick={toggleSidebar}
          className="p-1.5 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800/60 transition-colors shrink-0"
        >
          {isSidebarOpen ? <FiChevronLeft size={16} /> : <FiChevronRight size={16} />}
        </button>
      </div>

      {/* Main Navigation Tabs */}
      <div className="p-2 space-y-1 border-b border-slate-800/50">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center space-x-3 px-3 py-2 rounded-xl text-xs font-medium transition-all ${
                isActive
                  ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/20 font-semibold"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/40"
              }`}
            >
              <Icon size={16} className="shrink-0" />
              {isSidebarOpen && <span className="truncate">{item.label}</span>}
            </button>
          );
        })}
      </div>

      {/* Chat Session Thread Engine (Only visible when Chat active & Sidebar Expanded) */}
      {isSidebarOpen && activeTab === "chat" && (
        <div className="flex-1 flex flex-col overflow-hidden p-3 space-y-3">
          {/* New Chat Button */}
          <button
            onClick={() => createSession()}
            className="w-full flex items-center justify-center space-x-2 py-2 px-3 rounded-xl bg-slate-900 border border-indigo-500/30 text-indigo-300 hover:bg-indigo-950/40 hover:border-indigo-500/60 transition-all text-xs font-medium shadow-sm"
          >
            <FiPlus size={14} />
            <span>New Conversation</span>
          </button>

          {/* Search Box */}
          <div className="relative">
            <FiSearch className="absolute left-3 top-2.5 text-slate-500" size={13} />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search threads..."
              className="w-full pl-8 pr-3 py-1.5 bg-slate-900/60 border border-slate-800 rounded-lg text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500/50"
            />
          </div>

          {/* Session List */}
          <div className="flex-1 overflow-y-auto space-y-4 pr-1 text-xs">
            {/* Pinned Threads */}
            {pinnedSessions.length > 0 && (
              <div>
                <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider px-2 block mb-1">
                  Pinned
                </span>
                <div className="space-y-1">
                  {pinnedSessions.map((session) => (
                    <SessionItem
                      key={session.id}
                      session={session}
                      isActive={activeSessionId === session.id}
                      hoveredSession={hoveredSession}
                      setHoveredSession={setHoveredSession}
                      setActiveSession={setActiveSession}
                      togglePinSession={togglePinSession}
                      deleteSession={deleteSession}
                    />
                  ))}
                </div>
              </div>
            )}

            {/* Unpinned Threads */}
            <div>
              <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider px-2 block mb-1">
                Recent Conversations
              </span>
              <div className="space-y-1">
                {unpinnedSessions.map((session) => (
                  <SessionItem
                    key={session.id}
                    session={session}
                    isActive={activeSessionId === session.id}
                    hoveredSession={hoveredSession}
                    setHoveredSession={setHoveredSession}
                    setActiveSession={setActiveSession}
                    togglePinSession={togglePinSession}
                    deleteSession={deleteSession}
                  />
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Sidebar Footer User Info */}
      <div className="p-3 border-t border-slate-800/50 mt-auto flex items-center space-x-3">
        <div className="w-8 h-8 rounded-full bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400 font-mono text-xs shrink-0">
          AN
        </div>
        {isSidebarOpen && (
          <div className="flex flex-col overflow-hidden">
            <span className="text-xs text-slate-200 font-medium truncate">Andrew's Workspace</span>
            <span className="text-[10px] text-emerald-400 font-mono flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping" /> System Ready
            </span>
          </div>
        )}
      </div>
    </motion.aside>
  );
}

function SessionItem({
  session,
  isActive,
  hoveredSession,
  setHoveredSession,
  setActiveSession,
  togglePinSession,
  deleteSession,
}: any) {
  return (
    <div
      onMouseEnter={() => setHoveredSession(session.id)}
      onMouseLeave={() => setHoveredSession(null)}
      onClick={() => setActiveSession(session.id)}
      className={`group relative flex items-center justify-between px-2.5 py-2 rounded-lg cursor-pointer transition-all ${
        isActive
          ? "bg-slate-800/90 text-slate-100 border border-slate-700/60 font-medium"
          : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/60"
      }`}
    >
      <span className="truncate pr-4 text-xs">{session.title}</span>

      {hoveredSession === session.id && (
        <div className="absolute right-2 flex items-center space-x-1 bg-slate-900/90 px-1 py-0.5 rounded border border-slate-700/80">
          <button
            onClick={(e) => {
              e.stopPropagation();
              togglePinSession(session.id);
            }}
            className="p-1 hover:text-indigo-400 text-slate-400"
            title="Pin thread"
          >
            <FiPin size={11} className={session.isPinned ? "text-indigo-400" : ""} />
          </button>
          <button
            onClick={(e) => {
              e.stopPropagation();
              deleteSession(session.id);
            }}
            className="p-1 hover:text-rose-400 text-slate-400"
            title="Delete thread"
          >
            <FiTrash2 size={11} />
          </button>
        </div>
      )}
    </div>
  );
}