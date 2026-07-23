"use client";

import { useState, useRef, useEffect } from "react";
import { FiSend, FiPaperclip, FiMic, FiSparkles, FiSquare } from "react-icons/fi";

interface ChatInputProps {
  onSendMessage: (text: string) => void;
  isGenerating: boolean;
  onStopGeneration?: () => void;
}

export default function ChatInput({ onSendMessage, isGenerating, onStopGeneration }: ChatInputProps) {
  const [text, setText] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Suggested Prompts
  const suggestions = [
    "Explain Gradient Descent with a intuitive analogy",
    "How should I structure an ML team for data-centric AI?",
    "What is the key difference between Bias and Variance?",
    "Explain Transformers from first principles",
  ];

  // Auto-grow textarea height dynamically
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 180)}px`;
    }
  }, [text]);

  const handleSubmit = () => {
    if (!text.trim() || isGenerating) return;
    onSendMessage(text);
    setText("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto space-y-3">
      {/* Quick Prompt Suggestions */}
      {text.length === 0 && (
        <div className="flex items-center space-x-2 overflow-x-auto pb-1 scrollbar-none">
          <FiSparkles className="text-indigo-400 shrink-0 text-xs" />
          {suggestions.map((prompt, idx) => (
            <button
              key={idx}
              onClick={() => onSendMessage(prompt)}
              className="shrink-0 px-3 py-1.5 rounded-full bg-slate-900/80 hover:bg-slate-800 border border-slate-800/80 text-xs text-slate-300 hover:text-white transition-all shadow-sm"
            >
              {prompt}
            </button>
          ))}
        </div>
      )}

      {/* Main Glassmorphic Input Bar */}
      <div className="relative flex items-end bg-slate-900/90 border border-slate-800/90 rounded-2xl p-2 shadow-2xl backdrop-blur-2xl focus-within:border-indigo-500/60 transition-all">
        <button
          className="p-2 text-slate-400 hover:text-slate-200 transition-colors rounded-xl hover:bg-slate-800/60 mb-0.5"
          title="Attach files or documentation"
        >
          <FiPaperclip size={18} />
        </button>

        <textarea
          ref={textareaRef}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={1}
          placeholder="Ask Andrew Ng anything about Machine Learning, AI strategy, or career growth..."
          className="flex-1 bg-transparent px-3 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none resize-none max-h-44 leading-relaxed"
        />

        <div className="flex items-center space-x-1.5 mb-0.5">
          <button
            className="p-2 text-slate-400 hover:text-slate-200 transition-colors rounded-xl hover:bg-slate-800/60"
            title="Voice prompt"
          >
            <FiMic size={18} />
          </button>

          {isGenerating ? (
            <button
              onClick={onStopGeneration}
              className="p-2.5 bg-rose-600 hover:bg-rose-500 text-white rounded-xl transition-all shadow-md shadow-rose-600/30"
              title="Stop Generation"
            >
              <FiSquare size={16} />
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={!text.trim()}
              className="p-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl transition-all disabled:opacity-40 disabled:hover:bg-indigo-600 shadow-md shadow-indigo-600/30"
              title="Send message"
            >
              <FiSend size={16} />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}