"""
Conversation Service.

Central orchestration layer.

Pipeline

User
 ↓
Memory Retrieval
 ↓
Knowledge Retrieval
 ↓
Personality
 ↓
Prompt Builder
 ↓
Gemini
 ↓
Store Conversation
 ↓
Return Response
"""

from __future__ import annotations

from backend.core.logger import logger

from backend.llm.gemini_client import GeminiClient
from backend.llm.models import LLMRequest

from backend.memory.memory_manager import MemoryManager

from backend.personality.manager import PersonalityManager

from backend.prompt.prompt_builder import PromptBuilder

from backend.rag.retrieval.retriever import Retriever

from backend.services.models import (
    ConversationRequest,
    ConversationResponse,
)


class ConversationService:
    """
    Coordinates every subsystem.

    Memory
        ↓
    Knowledge
        ↓
    Personality
        ↓
    Prompt
        ↓
    Gemini
        ↓
    Save Conversation
    """

    def __init__(self):

        self.memory = MemoryManager()

        self.personality = PersonalityManager()

        self.knowledge = Retriever()

        self.prompt_builder = PromptBuilder()

        self.llm = GeminiClient()

    def chat(
        self,
        request: ConversationRequest,
    ) -> ConversationResponse:

        logger.info(
            "Conversation request received."
        )

        # --------------------------------------------------
        # Memory Retrieval
        # --------------------------------------------------

        memory = self.memory.retrieve_context(
            request.message
        )

        # --------------------------------------------------
        # Knowledge Retrieval
        # --------------------------------------------------

        knowledge = self.knowledge.retrieve(
            request.message
        )

        # --------------------------------------------------
        # Personality
        # --------------------------------------------------

        profile = self.personality.get_profile()

        # --------------------------------------------------
        # Prompt Construction
        # --------------------------------------------------

        llm_request = self.prompt_builder.build(
            user_prompt=request.message,
            personality=profile,
            memory=memory,
            knowledge=knowledge,
        )

        # --------------------------------------------------
        # Gemini
        # --------------------------------------------------

        llm_response = self.llm.generate(
            llm_request
        )

        # --------------------------------------------------
        # Save Memory
        # --------------------------------------------------

        self.memory.add_conversation(
            user=request.message,
            assistant=llm_response.text,
        )

        logger.success(
            "Conversation completed."
        )

        return ConversationResponse(
            response=llm_response.text,
            model=llm_response.model_used,
            latency_ms=llm_response.latency_ms,
            prompt_tokens=llm_response.usage.prompt_tokens,
            completion_tokens=llm_response.usage.completion_tokens,
            total_tokens=llm_response.usage.total_tokens,
        )