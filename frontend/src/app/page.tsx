"use client";

import { useState } from "react";
import Sidebar from "@/components/layout/Sidebar";
import Header from "@/components/layout/Header";
import RightDiagnosticPanel from "@/components/layout/RightDiagnosticPanel";
import LandingPage from "@/components/landing/LandingPage";

// Tab Dashboards
import ChatInterface from "@/components/chat/ChatInterface";
import KnowledgeDashboard from "@/components/knowledge/KnowledgeDashboard";
import MemoryDashboard from "@/components/memory/MemoryDashboard";
import PersonalityDashboard from "@/components/personality/PersonalityDashboard";
import TelemetryDashboard from "@/components/developer/TelemetryDashboard";
import AdminDashboard from "@/components/admin/AdminDashboard";

import { useUiStore } from "@/store/useUiStore";

export default function Home() {
  const [showLanding, setShowLanding] = useState(true);
  const { activeTab } = useUiStore();

  if (showLanding) {
    return <LandingPage onEnterOS={() => setShowLanding(false)} />;
  }

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#050508]">
      {/* Master Left Operating System Navigation */}
      <Sidebar />

      {/* Main Workspace Frame */}
      <div className="flex-1 flex flex-col h-full overflow-hidden relative">
        <Header />

        {/* Dynamic View Router */}
        <main className="flex-1 overflow-hidden flex relative">
          {activeTab === "chat" && <ChatInterface />}
          {activeTab === "knowledge" && <KnowledgeDashboard />}
          {activeTab === "memory" && <MemoryDashboard />}
          {activeTab === "personality" && <PersonalityDashboard />}
          {activeTab === "developer" && <TelemetryDashboard />}
          {activeTab === "settings" && <TelemetryDashboard />}
          {activeTab === "admin" && <AdminDashboard />}
        </main>
      </div>

      {/* Right Realtime Diagnostics Panel */}
      <RightDiagnosticPanel />
    </div>
  );
}