// ==========================================
// 1. CORE BACKEND DATA CONTRACTS
// ==========================================

export interface SourceDocument {
  id?: string;
  title?: string;
  source_name?: string;
  content: string;
  relevance_score?: number;
  metadata?: Record<string, any>;
}

export interface ChatResponse {
  response_text: string;
  sources: SourceDocument[];
  session_id: string;
  latency_ms?: number;
  tokens_used?: number;
}

export interface MemoryNode {
  id: string;
  label: string;
  val?: number;
  color?: string;
  group?: string;
  details?: string;
}

export interface MemoryEdge {
  source: string;
  target: string;
  label?: string;
  weight?: number;
}

export interface MemoryGraphData {
  nodes: MemoryNode[];
  links: MemoryEdge[];
}

export interface VoiceSynthesizeResponse {
  status: "success" | "error";
  audio_base64?: string;
  mime_type?: string;
  message?: string;
}

// ==========================================
// 2. EXTENDED AI-OS DATA CONTRACTS
// ==========================================

export interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  sources?: SourceDocument[];
  timestamp: string;
  isStreaming?: boolean;
  reasoningSteps?: string[];
  latencyMs?: number;
  tokenCount?: number;
}

export interface ChatSession {
  id: string;
  title: string;
  createdAt: string;
  updatedAt: string;
  isPinned?: boolean;
  messages: ChatMessage[];
}

export interface KnowledgeDocument {
  id: string;
  name: string;
  fileType: "pdf" | "docx" | "md" | "txt";
  sizeBytes: number;
  uploadedAt: string;
  status: "indexing" | "ready" | "failed";
  chunkCount: number;
  folder?: string;
  chunks?: { id: string; text: string; embeddingPreview?: number[] }[];
}

export interface PersonalityConfig {
  tone: "pedagogical" | "encouraging" | "rigorous" | "concise";
  analogiesFrequency: number; // 0 to 100
  firstPrinciplesFocus: number; // 0 to 100
  codeExplanationDepth: "high" | "medium" | "low";
  mathRigorLevel: "intuitive" | "balanced" | "formal";
}

export interface TelemetryMetrics {
  totalRequests: number;
  avgLatencyMs: number;
  activeModel: string;
  fallbackCount: number;
  vectorDbStatus: "healthy" | "degraded" | "offline";
  geminiQuotaRemaining: number;
}

export interface UserProfile {
  id: string;
  name: string;
  email: string;
  role: "admin" | "developer" | "user";
  avatarUrl?: string;
}