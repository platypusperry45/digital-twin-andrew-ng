"use client";

import { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble";
import ChatInput from "./ChatInput";
import { useChatStore } from "@/store/useChatStore";
import { api } from "@/lib/api";

export default function ChatInterface() {
  const {
    getActiveSession,
    activeSessionId,
    addMessage,
    updateLastMessageContent,
    isGenerating,
    setGenerating,
  } = useChatStore();

  const activeSession = getActiveSession();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when messages update
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [activeSession?.messages, isGenerating]);

  const handleSendMessage = async (userText: string) => {
    if (!activeSessionId) return;

    // 1. Append User Message
    addMessage(activeSessionId, {
      role: "user",
      content: userText,
    });

    setGenerating(true);

    // 2. Append Empty Placeholder Assistant Message
    addMessage(activeSessionId, {
      role: "assistant",
      content: "",
      isStreaming: true,
    });

    try {
      // 3. Request Completion from FastAPI
      const response = await api.sendMessage(activeSessionId, userText);

      // 4. Update Assistant Message Content
      updateLastMessageContent(
        activeSessionId,
        response.response_text,
        response.sources
      );
    } catch (err) {
      console.error("Chat error:", err);
      updateLastMessageContent(
        activeSessionId,
        "I ran into a temporary issue retrieving data. Please check your backend connection on port 8000."
      );
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden p-6 max-w-5xl mx-auto w-full">
      {/* Scrollable Chat Area */}
      <div className="flex-1 overflow-y-auto pr-2 space-y-2">
        {activeSession?.messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}

        {isGenerating && (
          <div className="flex items-center space-x-3 py-3 px-4 text-xs font-mono text-indigo-400">
            <div className="w-2 h-2 rounded-full bg-indigo-400 animate-ping" />
            <span>Synthesizing pedagogical response & retrieving vector embeddings...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Dock */}
      <div className="pt-4 border-t border-slate-800/60">
        <ChatInput
          onSendMessage={handleSendMessage}
          isGenerating={isGenerating}
          onStopGeneration={() => setGenerating(false)}
        />
      </div>
    </div>
  );
}