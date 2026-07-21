"""
Conversation Service for Digital Twin of Andrew Ng.

Orchestrates multi-turn dialogs by blending:
- Personality injection
- Short-term & Long-term Memory recall
- RAG groundings retrieval
- Dynamic Prompt Building
- Gemini 2.5 Flash execution
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

from backend.core.logger import logger
from backend.llm.gemini_client import GeminiClient
from backend.llm.models import ChatMessage, LLMRequest
from backend.memory.memory_manager import MemoryManager
from backend.personality.manager import PersonalityManager
from backend.prompt.prompt_builder import PromptBuilder
from backend.rag.retrieval.retriever import Retriever
from backend.services.models import ChatResponse
from backend.services.session_manager import SessionManager


class ConversationService:
    """
    Main orchestration engine managing end-to-end conversation flows.
    """

    def __init__(
        self,
        personality: PersonalityManager,
        memory: MemoryManager,
        retriever: Retriever,
        prompt_builder: PromptBuilder,
        llm: GeminiClient,
        sessions: Optional[SessionManager] = None,
        session_manager: Optional[SessionManager] = None,
    ) -> None:
        self.personality = personality
        self.memory = memory
        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.llm = llm
        self.sessions = sessions or session_manager or SessionManager()
        logger.info("ConversationService initialized successfully.")

    def chat(
        self,
        session_id: str,
        message: str,
        user_id: str = "default_user",
    ) -> ChatResponse:
        """
        Executes a single turn in a multi-turn conversation session.
        """
        start_time = time.time()
        logger.info(f"Processing chat message for session='{session_id}'...")

        # 1. Fetch or create session state
        chat_session = self.sessions.get_or_create(session_id)

        # 2. Retrieve RAG Knowledge Context
        rag_context_docs: List[str] = []
        try:
            rag_results = self.retriever.retrieve(query=message, top_k=3)
            if hasattr(rag_results, "documents"):
                rag_context_docs = [str(doc) for doc in rag_results.documents]
            elif isinstance(rag_results, list):
                rag_context_docs = [str(doc) for doc in rag_results]
        except Exception as e:
            logger.warning(f"RAG retrieval skipped or encountered error: {e}")

        # 3. Retrieve Long-Term & Short-Term Memory Context
        memory_context = ""
        try:
            if hasattr(self.memory, "get_context"):
                memory_context = self.memory.get_context(session_id=session_id, query=message)
        except Exception as e:
            logger.warning(f"Memory context lookup skipped: {e}")

        # 4. Construct Prompt
        history = chat_session.get_history()
        system_prompt = self.prompt_builder.build_system_prompt(
            personality=self.personality.get_profile(),
            rag_context=rag_context_docs,
            memory_context=memory_context,
        )

        messages_sequence = [
            ChatMessage(role=msg.get("role", "user"), content=msg.get("content", ""))
            for msg in history
        ]

        # 5. Call LLM Engine (Gemini 2.5 Flash)
        llm_request = LLMRequest(
            user_prompt=message,
            system_prompt=system_prompt,
            messages=messages_sequence,
        )

        llm_response = self.llm.generate(llm_request)

        # 6. Update Session History & Memory
        chat_session.add_user_message(message)
        chat_session.add_assistant_message(llm_response.text)

        try:
            if hasattr(self.memory, "add_conversation"):
                short_term_ref = getattr(chat_session, "short_term", None)
                if short_term_ref:
                    self.memory.add_conversation(
                        short_term=short_term_ref,
                        user=message,
                        assistant=llm_response.text,
                    )
            elif hasattr(self.memory, "save_turn"):
                self.memory.save_turn(session_id=session_id, user_msg=message, assistant_msg=llm_response.text)
        except Exception as e:
            logger.warning(f"Failed saving memory turn: {e}")

        latency_ms = (time.time() - start_time) * 1000

        return ChatResponse(
            session_id=session_id,
            response_text=llm_response.text,
            sources=rag_context_docs,
            latency_ms=latency_ms,
            model_used=llm_response.model_used,
        )