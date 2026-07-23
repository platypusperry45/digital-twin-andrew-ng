import { create } from "zustand";
import { persist } from "zustand/middleware";
import { ChatMessage, ChatSession, SourceDocument } from "@/types";

interface ChatState {
  sessions: ChatSession[];
  activeSessionId: string | null;
  isGenerating: boolean;
  searchQuery: string;

  // Actions
  createSession: (title?: string) => string;
  setActiveSession: (id: string) => void;
  deleteSession: (id: string) => void;
  renameSession: (id: string, newTitle: string) => void;
  togglePinSession: (id: string) => void;
  addMessage: (sessionId: string, message: Omit<ChatMessage, "id" | "timestamp">) => void;
  updateLastMessageContent: (sessionId: string, content: string, sources?: SourceDocument[]) => void;
  setGenerating: (status: boolean) => void;
  setSearchQuery: (query: string) => void;
  getActiveSession: () => ChatSession | undefined;
}

const DEFAULT_SESSION_ID = "session_default_1";

export const useChatStore = create<ChatState>()(
  persist(
    (set, get) => ({
      sessions: [
        {
          id: DEFAULT_SESSION_ID,
          title: "Supervised Learning Fundamentals",
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
          isPinned: true,
          messages: [
            {
              id: "msg_welcome",
              role: "assistant",
              content:
                "Welcome! I am Andrew Ng's Digital Twin. Let's build intuition together around Machine Learning, Deep Learning, and Data-Centric AI. What topic would you like to explore today?",
              timestamp: new Date().toISOString(),
            },
          ],
        },
      ],
      activeSessionId: DEFAULT_SESSION_ID,
      isGenerating: false,
      searchQuery: "",

      createSession: (title) => {
        const id = `session_${Date.now()}`;
        const newSession: ChatSession = {
          id,
          title: title || "New Conversation",
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
          isPinned: false,
          messages: [],
        };

        set((state) => ({
          sessions: [newSession, ...state.sessions],
          activeSessionId: id,
        }));

        return id;
      },

      setActiveSession: (id) => set({ activeSessionId: id }),

      deleteSession: (id) => {
        set((state) => {
          const filtered = state.sessions.filter((s) => s.id !== id);
          const nextActive = filtered.length > 0 ? filtered[0].id : null;
          return {
            sessions: filtered,
            activeSessionId: state.activeSessionId === id ? nextActive : state.activeSessionId,
          };
        });
      },

      renameSession: (id, newTitle) => {
        set((state) => ({
          sessions: state.sessions.map((s) =>
            s.id === id ? { ...s, title: newTitle, updatedAt: new Date().toISOString() } : s
          ),
        }));
      },

      togglePinSession: (id) => {
        set((state) => ({
          sessions: state.sessions.map((s) =>
            s.id === id ? { ...s, isPinned: !s.isPinned } : s
          ),
        }));
      },

      addMessage: (sessionId, messageData) => {
        const newMessage: ChatMessage = {
          ...messageData,
          id: `msg_${Date.now()}_${Math.random().toString(36).substring(2, 6)}`,
          timestamp: new Date().toISOString(),
        };

        set((state) => ({
          sessions: state.sessions.map((session) => {
            if (session.id === sessionId) {
              return {
                ...session,
                updatedAt: new Date().toISOString(),
                messages: [...session.messages, newMessage],
              };
            }
            return session;
          }),
        }));
      },

      updateLastMessageContent: (sessionId, content, sources) => {
        set((state) => ({
          sessions: state.sessions.map((session) => {
            if (session.id === sessionId && session.messages.length > 0) {
              const updatedMessages = [...session.messages];
              const lastMsg = updatedMessages[updatedMessages.length - 1];
              updatedMessages[updatedMessages.length - 1] = {
                ...lastMsg,
                content,
                sources: sources || lastMsg.sources,
              };
              return { ...session, messages: updatedMessages };
            }
            return session;
          }),
        }));
      },

      setGenerating: (status) => set({ isGenerating: status }),

      setSearchQuery: (query) => set({ searchQuery: query }),

      getActiveSession: () => {
        const { sessions, activeSessionId } = get();
        return sessions.find((s) => s.id === activeSessionId);
      },
    }),
    {
      name: "andrew_ng_chat_store",
      partialize: (state) => ({
        sessions: state.sessions,
        activeSessionId: state.activeSessionId,
      }),
    }
  )
);