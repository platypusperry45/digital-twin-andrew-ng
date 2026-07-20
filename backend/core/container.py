"""
Application Dependency Container.

Creates singleton instances used throughout
the backend.

Nothing outside this module should instantiate
large services directly.
"""

from __future__ import annotations

from functools import cached_property

from backend.core.logger import logger

from backend.llm.gemini_client import GeminiClient

from backend.memory.memory_manager import MemoryManager

from backend.personality.manager import PersonalityManager

from backend.prompt.prompt_builder import PromptBuilder

from backend.rag.retrieval.retriever import Retriever

from backend.services.conversation_service import (
    ConversationService,
)


class ApplicationContainer:
    """
    Global dependency container.

    Every heavyweight object is created once.
    """

    @cached_property
    def personality(
        self,
    ) -> PersonalityManager:

        logger.info(
            "Initializing PersonalityManager"
        )

        return PersonalityManager()

    @cached_property
    def memory(
        self,
    ) -> MemoryManager:

        logger.info(
            "Initializing MemoryManager"
        )

        return MemoryManager()

    @cached_property
    def retriever(
        self,
    ) -> Retriever:

        logger.info(
            "Initializing Retriever"
        )

        return Retriever()

    @cached_property
    def prompt_builder(
        self,
    ) -> PromptBuilder:

        logger.info(
            "Initializing PromptBuilder"
        )

        return PromptBuilder()

    @cached_property
    def llm(
        self,
    ) -> GeminiClient:

        logger.info(
            "Initializing GeminiClient"
        )

        return GeminiClient()

    @cached_property
    def conversation_service(
        self,
    ) -> ConversationService:

        logger.info(
            "Initializing ConversationService"
        )

        return ConversationService(
            personality=self.personality,
            memory=self.memory,
            retriever=self.retriever,
            prompt_builder=self.prompt_builder,
            llm=self.llm,
        )


container = ApplicationContainer()