import {
  ChatResponse,
  MemoryGraphData,
  VoiceSynthesizeResponse,
  KnowledgeDocument,
  PersonalityConfig,
  TelemetryMetrics,
  ChatSession,
} from "@/types";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  // Helper for REST requests
  private async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = {
      "Content-Type": "application/json",
      ...(options?.headers || {}),
    };

    try {
      const response = await fetch(url, { ...options, headers });
      if (!response.ok) {
        throw new Error(`HTTP Error ${response.status}: ${response.statusText}`);
      }
      return (await response.json()) as T;
    } catch (error) {
      console.error(`API Error on [${endpoint}]:`, error);
      throw error;
    }
  }

  // ========================================================
  // 1. EXISTING BACKEND API BINDINGS (STRICT COMPATIBILITY)
  // ========================================================

  /**
   * Post chat message to existing FastAPI endpoint `/chat`
   */
  async sendMessage(sessionId: string, message: string): Promise<ChatResponse> {
    const startTime = performance.now();
    try {
      const res = await this.request<ChatResponse>("/chat", {
        method: "POST",
        body: JSON.stringify({
          session_id: sessionId,
          message: message,
        }),
      });

      const latencyMs = Math.round(performance.now() - startTime);
      return {
        ...res,
        latency_ms: res.latency_ms ?? latencyMs,
        tokens_used: res.tokens_used ?? Math.round(message.length * 1.3 + (res.response_text?.length || 0) * 1.3),
      };
    } catch (err) {
      console.warn("Backend chat endpoint failed. Generating graceful fallback response.", err);
      // Fallback response if backend is offline
      return {
        session_id: sessionId,
        response_text:
          "Let's build intuition for this concept step-by-step. In supervised learning, our main goal is learning a mapping from input x to output y. What specific part of this algorithm would you like to explore first?",
        sources: [
          {
            id: "fallback_1",
            title: "Machine Learning Yearning - Chapter 2",
            content: "Break complex problems into independent components to analyze error sources systematically.",
            relevance_score: 0.94,
          },
        ],
        latency_ms: Math.round(performance.now() - startTime),
        tokens_used: 120,
      };
    }
  }

  /**
   * Fetch 3D Memory Graph node network from `/memory/graph`
   */
  async fetchMemoryGraph(sessionId: string): Promise<MemoryGraphData> {
    try {
      return await this.request<MemoryGraphData>(`/memory/graph?session_id=${encodeURIComponent(sessionId)}`);
    } catch (err) {
      console.warn("Backend memory endpoint unreachable. Serving fallback vector state.", err);
      return {
        nodes: [
          { id: "root", label: "Andrew Ng AI Persona", group: "core", val: 20 },
          { id: "concept_1", label: "Supervised Learning", group: "ml", val: 14 },
          { id: "concept_2", label: "Gradient Descent", group: "math", val: 12 },
          { id: "concept_3", label: "Data-Centric AI", group: "data", val: 16 },
          { id: "concept_4", label: "Deep Learning Specialization", group: "course", val: 15 },
          { id: "concept_5", label: "Structuring ML Projects", group: "strategy", val: 10 },
        ],
        links: [
          { source: "root", target: "concept_1", weight: 0.9 },
          { source: "root", target: "concept_3", weight: 0.85 },
          { source: "concept_1", target: "concept_2", weight: 0.95 },
          { source: "root", target: "concept_4", weight: 0.78 },
          { source: "concept_3", target: "concept_5", weight: 0.88 },
        ],
      };
    }
  }

  /**
   * Synthesize audio from text using `/voice/synthesize`
   */
  async synthesizeVoice(text: string): Promise<VoiceSynthesizeResponse> {
    try {
      return await this.request<VoiceSynthesizeResponse>("/voice/synthesize", {
        method: "POST",
        body: JSON.stringify({ text }),
      });
    } catch (err) {
      console.warn("Voice endpoint unreachable. Fallback to Web Speech API.", err);
      return {
        status: "error",
        message: "Backend voice server unavailable. Client fallback active.",
      };
    }
  }

  // ========================================================
  // 2. EXTENDED AI-OS CLIENT SERVICES (PERSISTENCE & MOCKS)
  // ========================================================

  /**
   * Fetch Knowledge Base documents
   */
  async fetchKnowledgeDocuments(): Promise<KnowledgeDocument[]> {
    const saved = typeof window !== "undefined" ? localStorage.getItem("ng_twins_knowledge") : null;
    if (saved) return JSON.parse(saved);

    const defaultDocs: KnowledgeDocument[] = [
      {
        id: "doc_1",
        name: "Machine_Learning_Yearning_Draft.pdf",
        fileType: "pdf",
        sizeBytes: 2450000,
        uploadedAt: new Date(Date.now() - 86400000 * 3).toISOString(),
        status: "ready",
        chunkCount: 142,
        folder: "Books",
        chunks: [
          { id: "c1", text: "When building a complex machine learning system, set up your dev/test sets early." },
          { id: "c2", text: "Data-centric AI focuses on systematically improving data quality rather than tweaking model architectures." },
        ],
      },
      {
        id: "doc_2",
        name: "Deep_Learning_Lecture_Notes_CS229.md",
        fileType: "md",
        sizeBytes: 840000,
        uploadedAt: new Date(Date.now() - 86400000).toISOString(),
        status: "ready",
        chunkCount: 88,
        folder: "Stanford CS229",
      },
    ];

    if (typeof window !== "undefined") {
      localStorage.setItem("ng_twins_knowledge", JSON.stringify(defaultDocs));
    }
    return defaultDocs;
  }

  /**
   * Upload Document to Knowledge Base
   */
  async uploadKnowledgeDocument(file: File): Promise<KnowledgeDocument> {
    const newDoc: KnowledgeDocument = {
      id: `doc_${Date.now()}`,
      name: file.name,
      fileType: (file.name.split(".").pop() as any) || "txt",
      sizeBytes: file.size,
      uploadedAt: new Date().toISOString(),
      status: "ready",
      chunkCount: Math.floor(file.size / 1024) + 1,
      folder: "Uploads",
    };

    const existing = await this.fetchKnowledgeDocuments();
    const updated = [newDoc, ...existing];
    if (typeof window !== "undefined") {
      localStorage.setItem("ng_twins_knowledge", JSON.stringify(updated));
    }
    return newDoc;
  }

  /**
   * Fetch System Telemetry & Developer Metrics
   */
  async fetchTelemetry(): Promise<TelemetryMetrics> {
    return {
      totalRequests: 1420,
      avgLatencyMs: 340,
      activeModel: "gemini-1.5-pro / RAG ChromaDB",
      fallbackCount: 2,
      vectorDbStatus: "healthy",
      geminiQuotaRemaining: 88.4,
    };
  }

  /**
   * Fetch Personality Settings
   */
  async fetchPersonalityConfig(): Promise<PersonalityConfig> {
    const saved = typeof window !== "undefined" ? localStorage.getItem("ng_twins_personality") : null;
    if (saved) return JSON.parse(saved);

    return {
      tone: "pedagogical",
      analogiesFrequency: 85,
      firstPrinciplesFocus: 90,
      codeExplanationDepth: "high",
      mathRigorLevel: "balanced",
    };
  }

  /**
   * Save Personality Settings
   */
  async savePersonalityConfig(config: PersonalityConfig): Promise<void> {
    if (typeof window !== "undefined") {
      localStorage.setItem("ng_twins_personality", JSON.stringify(config));
    }
  }
}

export const api = new ApiClient(BASE_URL);