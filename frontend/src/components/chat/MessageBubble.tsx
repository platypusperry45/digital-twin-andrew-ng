"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { FiBookOpen, FiCopy, FiCheck, FiVolume2, FiRotateCw } from "react-icons/fi";
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";
import { ChatMessage } from "@/types";
import { useUiStore } from "@/store/useUiStore";
import { api } from "@/lib/api";

interface MessageBubbleProps {
  message: ChatMessage;
  onRegenerate?: () => void;
}

export default function MessageBubble({ message, onRegenerate }: MessageBubbleProps) {
  const { setSourcesModalData } = useUiStore();
  const [copied, setCopied] = useState(false);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);

  const isUser = message.role === "user";

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handlePlayVoice = async () => {
    if (isPlayingAudio) return;
    setIsPlayingAudio(true);

    try {
      const voiceRes = await api.synthesizeVoice(message.content);
      if (voiceRes.status === "success" && voiceRes.audio_base64) {
        const audio = new Audio(`data:${voiceRes.mime_type || "audio/wav"};base64,${voiceRes.audio_base64}`);
        audio.onended = () => setIsPlayingAudio(false);
        audio.onerror = () => fallbackWebSpeech(message.content);
        await audio.play();
      } else {
        fallbackWebSpeech(message.content);
      }
    } catch {
      fallbackWebSpeech(message.content);
    }
  };

  const fallbackWebSpeech = (text: string) => {
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.95;
      utterance.onend = () => setIsPlayingAudio(false);
      utterance.onerror = () => setIsPlayingAudio(false);
      window.speechSynthesis.speak(utterance);
    } else {
      setIsPlayingAudio(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25 }}
      className={`flex ${isUser ? "justify-end" : "justify-start"} my-4`}
    >
      <div className={`flex flex-col max-w-[85%] ${isUser ? "items-end" : "items-start"}`}>
        {/* Role Header */}
        <div className="flex items-center space-x-2 mb-1.5 px-1">
          <span className="text-[11px] font-mono font-semibold tracking-wider text-slate-400 uppercase">
            {isUser ? "You" : "Andrew Ng Twin"}
          </span>
          {message.latencyMs && !isUser && (
            <span className="text-[10px] font-mono text-indigo-400 bg-indigo-950/60 border border-indigo-800/60 px-1.5 py-0.2 rounded-full">
              {message.latencyMs}ms
            </span>
          )}
        </div>

        {/* Message Bubble Card */}
        <div
          className={`relative rounded-2xl px-5 py-4 text-sm leading-relaxed ${
            isUser
              ? "bg-indigo-600 text-white rounded-tr-none shadow-lg shadow-indigo-600/20"
              : "bg-slate-900/90 text-slate-100 rounded-tl-none border border-slate-800/80 shadow-xl backdrop-blur-xl"
          }`}
        >
          {/* Reasoning / Thinking Expansion if exists */}
          {message.reasoningSteps && message.reasoningSteps.length > 0 && (
            <details className="mb-3 border-b border-slate-800 pb-2 text-xs text-indigo-300 cursor-pointer">
              <summary className="font-mono font-medium hover:text-indigo-200 transition-colors">
                💭 Thought Process & Pedagogical Reasoning ({message.reasoningSteps.length} steps)
              </summary>
              <ul className="mt-2 space-y-1 list-disc list-inside text-slate-400 font-mono text-[11px]">
                {message.reasoningSteps.map((step, i) => (
                  <li key={i}>{step}</li>
                ))}
              </ul>
            </details>
          )}

          {/* Render Markdown & KaTeX Math */}
          <div className="prose prose-invert prose-sm max-w-none break-words">
            <ReactMarkdown
              remarkPlugins={[remarkMath]}
              rehypePlugins={[rehypeKatex]}
              components={{
                code({ inline, className, children, ...props }: any) {
                  return inline ? (
                    <code className="bg-slate-800 px-1.5 py-0.5 rounded text-indigo-300 font-mono text-xs" {...props}>
                      {children}
                    </code>
                  ) : (
                    <pre className="bg-slate-950 p-4 rounded-xl border border-slate-800 overflow-x-auto text-xs font-mono my-3">
                      <code className={className} {...props}>
                        {children}
                      </code>
                    </pre>
                  );
                },
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>

          {/* RAG Citation Drawer Trigger */}
          {message.sources && message.sources.length > 0 && (
            <div className="mt-3 pt-3 border-t border-slate-800/80 flex items-center justify-between">
              <button
                onClick={() => setSourcesModalData(message.sources || [])}
                className="flex items-center space-x-1.5 text-xs text-indigo-400 hover:text-indigo-300 font-mono transition-colors"
              >
                <FiBookOpen size={13} />
                <span>Grounded in {message.sources.length} RAG Sources</span>
              </button>
            </div>
          )}
        </div>

        {/* Message Action Bar (Copy, Regenerate, Voice Audio) */}
        {!isUser && (
          <div className="flex items-center space-x-3 mt-1.5 px-1 text-slate-400 text-xs">
            <button
              onClick={handleCopy}
              className="flex items-center space-x-1 hover:text-slate-200 transition-colors"
              title="Copy response"
            >
              {copied ? <FiCheck className="text-emerald-400" /> : <FiCopy />}
              <span>{copied ? "Copied" : "Copy"}</span>
            </button>

            <button
              onClick={handlePlayVoice}
              disabled={isPlayingAudio}
              className="flex items-center space-x-1 hover:text-indigo-300 transition-colors disabled:opacity-50"
              title="Listen to audio"
            >
              <FiVolume2 className={isPlayingAudio ? "text-indigo-400 animate-pulse" : ""} />
              <span>{isPlayingAudio ? "Speaking..." : "Voice"}</span>
            </button>

            {onRegenerate && (
              <button
                onClick={onRegenerate}
                className="flex items-center space-x-1 hover:text-slate-200 transition-colors"
                title="Regenerate response"
              >
                <FiRotateCw />
                <span>Regenerate</span>
              </button>
            )}
          </div>
        )}
      </div>
    </motion.div>
  );
}