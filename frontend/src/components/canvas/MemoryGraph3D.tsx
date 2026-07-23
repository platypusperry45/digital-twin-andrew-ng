"use client";

import { useEffect, useRef, useState } from "react";
import { FiRefreshCw, FiZoomIn, FiZoomOut, FiCpu } from "react-icons/fi";
import { MemoryGraphData, MemoryNode } from "@/types";
import { api } from "@/lib/api";
import { useChatStore } from "@/store/useChatStore";

export default function MemoryGraph3D() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const { activeSessionId } = useChatStore();
  const [graphData, setGraphData] = useState<MemoryGraphData | null>(null);
  const [selectedNode, setSelectedNode] = useState<MemoryNode | null>(null);
  const [zoom, setZoom] = useState(1);
  const [isLoading, setIsLoading] = useState(true);

  // Fetch memory graph data from backend / fallback
  const loadGraph = async () => {
    setIsLoading(true);
    try {
      const data = await api.fetchMemoryGraph(activeSessionId || "default_session");
      setGraphData(data);
    } catch (err) {
      console.error("Failed to load memory graph:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadGraph();
  }, [activeSessionId]);

  // Canvas 2D/Interactive Graph Renderer with smooth animation loop
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !graphData) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationFrameId: number;
    let width = (canvas.width = canvas.parentElement?.clientWidth || 800);
    let height = (canvas.height = canvas.parentElement?.clientHeight || 600);

    // Initial node positions in 2D projected space
    const nodes = graphData.nodes.map((node, index) => {
      const angle = (index / graphData.nodes.length) * Math.PI * 2;
      const radius = index === 0 ? 0 : 140 + (index % 3) * 40;
      return {
        ...node,
        x: width / 2 + Math.cos(angle) * radius,
        y: height / 2 + Math.sin(angle) * radius,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
      };
    });

    const render = () => {
      ctx.clearRect(0, 0, width, height);

      // Draw Edges / Memory Links
      graphData.links.forEach((link) => {
        const sourceNode = nodes.find((n) => n.id === link.source);
        const targetNode = nodes.find((n) => n.id === link.target);

        if (sourceNode && targetNode) {
          ctx.beginPath();
          ctx.moveTo(sourceNode.x, sourceNode.y);
          ctx.lineTo(targetNode.x, targetNode.y);
          ctx.strokeStyle = `rgba(99, 102, 241, ${link.weight || 0.4})`;
          ctx.lineWidth = (link.weight || 0.5) * 2 * zoom;
          ctx.stroke();
        }
      });

      // Draw Memory Nodes
      nodes.forEach((node) => {
        // Floating physics micro-movement
        node.x += node.vx;
        node.y += node.vy;

        if (node.x < 100 || node.x > width - 100) node.vx *= -1;
        if (node.y < 100 || node.y > height - 100) node.vy *= -1;

        const isSelected = selectedNode?.id === node.id;
        const radius = (node.val || 10) * 0.8 * zoom;

        // Glow effect
        ctx.beginPath();
        ctx.arc(node.x, node.y, radius + 6, 0, Math.PI * 2);
        ctx.fillStyle = isSelected
          ? "rgba(99, 102, 241, 0.4)"
          : "rgba(16, 185, 129, 0.15)";
        ctx.fill();

        // Node Circle
        ctx.beginPath();
        ctx.arc(node.x, node.y, radius, 0, Math.PI * 2);
        ctx.fillStyle = node.group === "core" ? "#6366f1" : "#10b981";
        ctx.fill();
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = isSelected ? 2 : 0.5;
        ctx.stroke();

        // Label
        ctx.font = `${Math.max(10, 11 * zoom)}px JetBrains Mono, monospace`;
        ctx.fillStyle = "#e2e8f0";
        ctx.fillText(node.label, node.x + radius + 8, node.y + 4);
      });

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animationFrameId);
    };
  }, [graphData, zoom, selectedNode]);

  return (
    <div className="relative w-full h-full bg-[#050508] flex flex-col overflow-hidden">
      {/* Top Controls Bar */}
      <div className="absolute top-4 left-4 z-10 flex items-center space-x-2 bg-slate-900/80 border border-slate-800/80 p-2 rounded-xl backdrop-blur-md">
        <button
          onClick={() => setZoom((z) => Math.min(2, z + 0.2))}
          className="p-1.5 text-slate-300 hover:text-white rounded-lg hover:bg-slate-800"
          title="Zoom In"
        >
          <FiZoomIn size={16} />
        </button>
        <button
          onClick={() => setZoom((z) => Math.max(0.5, z - 0.2))}
          className="p-1.5 text-slate-300 hover:text-white rounded-lg hover:bg-slate-800"
          title="Zoom Out"
        >
          <FiZoomOut size={16} />
        </button>
        <div className="w-px h-4 bg-slate-800" />
        <button
          onClick={loadGraph}
          className="p-1.5 text-slate-300 hover:text-white rounded-lg hover:bg-slate-800"
          title="Refresh Network"
        >
          <FiRefreshCw size={16} className={isLoading ? "animate-spin" : ""} />
        </button>
      </div>

      {/* Canvas Area */}
      <div className="flex-1 w-full h-full relative cursor-grab active:cursor-grabbing">
        <canvas ref={canvasRef} className="w-full h-full block" />
      </div>

      {/* Selected Node Details Overlay */}
      {selectedNode && (
        <div className="absolute bottom-4 right-4 z-10 w-80 bg-slate-900/90 border border-slate-800 p-4 rounded-2xl backdrop-blur-2xl shadow-2xl space-y-2 text-xs">
          <div className="flex items-center space-x-2 text-indigo-400 font-mono font-bold">
            <FiCpu />
            <span>{selectedNode.label}</span>
          </div>
          <p className="text-slate-300 leading-relaxed">
            {selectedNode.details || "Active neural concept retrieved during semantic search across lecture embeddings."}
          </p>
          <div className="flex justify-between text-[10px] font-mono text-slate-500 pt-2 border-t border-slate-800">
            <span>Group: {selectedNode.group || "ML Core"}</span>
            <span>Weight: {selectedNode.val || 10}</span>
          </div>
        </div>
      )}
    </div>
  );
}