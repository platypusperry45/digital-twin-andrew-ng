"""
Conversation Service.

Coordinates the complete conversation pipeline.

Flow
----
User
    ↓
Memory Retrieval
    ↓
Knowledge Retrieval
    ↓
Prompt Builder
    ↓
Gemini
    ↓
Memory Storage
"""

from backend.core.logger import logger

from backend.llm.gemini_client import GeminiClient
from backend.llm.models import (
    LLMRequest,
)

from backend.memory.memory_manager import MemoryManager

from backend.rag.retrieval.retriever import Retriever

from backend.services.prompt_builder import PromptBuilder
from backend.services.models import (
    ConversationResponse,
)


class ConversationService:

    def __init__(
        self,
        llm: GeminiClient,
        memory: MemoryManager,
        retriever: Retriever,
        prompt_builder: PromptBuilder,
    ):

        self.llm = llm
        self.memory = memory
        self.retriever = retriever
        self.prompt_builder = prompt_builder

        logger.info(
            "Conversation Service initialized."
        )

    def chat(
        self,
        request: LLMRequest,
    ) -> ConversationResponse:

        logger.info(
            "Conversation started."
        )

        # -----------------------------
        # Memory
        # -----------------------------

        memory = self.memory.retrieve_context(
            request.prompt
        )

        # -----------------------------
        # Knowledge
        # -----------------------------

        knowledge = self.retriever.retrieve(
            request.prompt
        )

        # -----------------------------
        # Prompt
        # -----------------------------

        final_prompt = self.prompt_builder.build(
            user_prompt=request.prompt,
            memory=memory,
            knowledge=knowledge,
        )

        # -----------------------------
        # LLM
        # -----------------------------

        llm_response = self.llm.generate(

            LLMRequest(

                prompt=final_prompt,

                model=request.model,

                temperature=request.temperature,

                metadata=request.metadata,

            )

        )

        # -----------------------------
        # Store Conversation
        # -----------------------------

        self.memory.add_conversation(

            user=request.prompt,

            assistant=llm_response.content,

        )

        logger.success(
            "Conversation completed."
        )

        return ConversationResponse(

            llm=llm_response,

            memory=memory,

            knowledge=knowledge,

            final_prompt=final_prompt,

        )