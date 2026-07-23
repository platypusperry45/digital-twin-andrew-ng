import { create } from "zustand";
import { KnowledgeDocument } from "@/types";
import { api } from "@/lib/api";

interface KnowledgeState {
  documents: KnowledgeDocument[];
  isLoading: boolean;
  searchQuery: string;
  selectedDocId: string | null;

  // Actions
  loadDocuments: () => Promise<void>;
  uploadDocument: (file: File) => Promise<KnowledgeDocument>;
  deleteDocument: (id: string) => void;
  setSearchQuery: (query: string) => void;
  setSelectedDocId: (id: string | null) => void;
}

export const useKnowledgeStore = create<KnowledgeState>((set, get) => ({
  documents: [],
  isLoading: false,
  searchQuery: "",
  selectedDocId: null,

  loadDocuments: async () => {
    set({ isLoading: true });
    try {
      const docs = await api.fetchKnowledgeDocuments();
      set({ documents: docs, isLoading: false });
    } catch (err) {
      console.error("Failed loading knowledge documents", err);
      set({ isLoading: false });
    }
  },

  uploadDocument: async (file) => {
    set({ isLoading: true });
    try {
      const doc = await api.uploadKnowledgeDocument(file);
      set((state) => ({
        documents: [doc, ...state.documents],
        isLoading: false,
      }));
      return doc;
    } catch (err) {
      console.error("Failed uploading document", err);
      set({ isLoading: false });
      throw err;
    }
  },

  deleteDocument: (id) => {
    set((state) => {
      const updated = state.documents.filter((d) => d.id !== id);
      if (typeof window !== "undefined") {
        localStorage.setItem("ng_twins_knowledge", JSON.stringify(updated));
      }
      return {
        documents: updated,
        selectedDocId: state.selectedDocId === id ? null : state.selectedDocId,
      };
    });
  },

  setSearchQuery: (query) => set({ searchQuery: query }),

  setSelectedDocId: (id) => set({ selectedDocId: id }),
}));