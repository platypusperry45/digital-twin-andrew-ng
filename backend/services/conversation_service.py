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

import time

from backend.core.logger import logger

from backend.llm.exceptions import (
    LLMException,
    SafetyBlockedError,
    RateLimitError,
    ModelUnavailableError,
)

from backend.llm.gemini_client import GeminiClient
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
    Coordinates every backend subsystem.

    This class contains orchestration logic only.
    """

    def __init__(
        self,
        *,
        personality: PersonalityManager,
        memory: MemoryManager,
        retriever: Retriever,
        prompt_builder: PromptBuilder,
        llm: GeminiClient,
    ) -> None:

        self.personality = personality
        self.memory = memory
        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.llm = llm

        logger.info(
            "ConversationService initialized."
        )

    # ==========================================================
    # Chat
    # ==========================================================

    def chat(
        self,
        request: ConversationRequest,
    ) -> ConversationResponse:

        logger.info(
            "Conversation request received."
        )

        started = time.time()

        try:

            # --------------------------------------------------
            # Memory
            # --------------------------------------------------

            memory_context = (
                self.memory.retrieve_context(
                    request.message
                )
            )

            # --------------------------------------------------
            # Knowledge
            # --------------------------------------------------

            knowledge_context = (
                self.retriever.retrieve(
                    request.message
                )
            )

            # --------------------------------------------------
            # Personality
            # --------------------------------------------------

            profile = (
                self.personality.get_profile()
            )

            # --------------------------------------------------
            # Prompt
            # --------------------------------------------------

            llm_request = (
                self.prompt_builder.build(
                    profile=profile,
                    memory=memory_context,
                    knowledge=knowledge_context,
                    user_prompt=request.message,
                )
            )

            # --------------------------------------------------
            # Generate
            # --------------------------------------------------

            llm_response = (
                self.llm.generate(
                    llm_request
                )
            )

            # --------------------------------------------------
            # Persist Conversation
            # --------------------------------------------------

            self.memory.add_conversation(
                user=request.message,
                assistant=llm_response.text,
            )

            elapsed = (
                time.time() - started
            ) * 1000

            logger.success(
                f"Conversation completed "
                f"in {elapsed:.2f} ms."
            )

            return ConversationResponse(

                response=llm_response.text,

                model=llm_response.model_used,

                latency_ms=llm_response.latency_ms,

                prompt_tokens=llm_response.usage.prompt_tokens,

                completion_tokens=llm_response.usage.completion_tokens,

                total_tokens=llm_response.usage.total_tokens,

            )

        except SafetyBlockedError:

            logger.warning(
                "Conversation blocked by Gemini safety."
            )

            raise

        except RateLimitError:

            logger.warning(
                "Rate limit reached."
            )

            raise

        except ModelUnavailableError:

            logger.error(
                "No Gemini model available."
            )

            raise

        except LLMException:

            logger.exception(
                "LLM pipeline failed."
            )

            raise

        except Exception:

            logger.exception(
                "Conversation pipeline crashed."
            )

            raise

    # ==========================================================
    # Health
    # ==========================================================

    def health(self) -> dict:

        return {

            "memory": self.memory.stats(),

            "retriever": self.retriever.store.stats(),

            "llm": self.llm.health(),

        }