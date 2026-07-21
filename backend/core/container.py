"""
Application Dependency Container.

Creates and owns singleton instances used throughout
the backend.

No heavyweight service should be instantiated outside
this container.
"""

from __future__ import annotations

from functools import cached_property

from backend.core.logger import logger

from backend.llm.gemini_client import GeminiClient
from backend.memory.memory_manager import MemoryManager
from backend.personality.manager import PersonalityManager
from backend.prompt.prompt_builder import PromptBuilder
from backend.rag.retrieval.retriever import Retriever

from backend.services.session_manager import SessionManager
from backend.services.conversation_service import ConversationService


class ApplicationContainer:
    """
    Global dependency container.

    Responsible for creating and owning every
    heavyweight singleton used by the application.
    """

    def __init__(self) -> None:
        self._initialized = False

    # =====================================================
    # Core Services
    # =====================================================

    @cached_property
    def personality(self) -> PersonalityManager:
        logger.info("Initializing PersonalityManager")
        return PersonalityManager()

    @cached_property
    def memory(self) -> MemoryManager:
        logger.info("Initializing MemoryManager")
        return MemoryManager()

    @cached_property
    def retriever(self) -> Retriever:
        logger.info("Initializing Retriever")
        return Retriever()

    @cached_property
    def prompt_builder(self) -> PromptBuilder:
        logger.info("Initializing PromptBuilder")
        return PromptBuilder()

    @cached_property
    def llm(self) -> GeminiClient:
        logger.info("Initializing GeminiClient")
        return GeminiClient()

    @cached_property
    def sessions(self) -> SessionManager:
        """
        Global session manager.

        Maintains one Conversation object per client.
        """
        logger.info("Initializing SessionManager")
        return SessionManager()

    @cached_property
    def conversation_service(self) -> ConversationService:
        logger.info("Initializing ConversationService")

        return ConversationService(
            personality=self.personality,
            memory=self.memory,
            retriever=self.retriever,
            prompt_builder=self.prompt_builder,
            llm=self.llm,
            sessions=self.sessions,
        )

    # =====================================================
    # Lifecycle
    # =====================================================

    def initialize(self) -> None:
        """
        Initialize the complete dependency graph.

        Forces creation of every singleton during startup
        so configuration and dependency errors are detected
        before the server begins accepting requests.
        """

        if self._initialized:
            logger.debug(
                "ApplicationContainer already initialized."
            )
            return

        logger.info(
            "Initializing application container..."
        )

        # Force singleton creation

        _ = self.personality
        _ = self.memory
        _ = self.retriever
        _ = self.prompt_builder
        _ = self.llm
        _ = self.sessions
        _ = self.conversation_service

        self._initialized = True

        logger.success(
            "Application container initialized."
        )

    def shutdown(self) -> None:
        """
        Shutdown hook.

        Allows future cleanup of shared resources
        such as:

        - database engines
        - vector databases
        - HTTP clients
        - thread pools
        - async tasks
        - session caches
        """

        if not self._initialized:
            return

        logger.info(
            "Shutting down application container."
        )

        # Cleanup session cache

        self.sessions.clear()

        # Future cleanup hooks

        self._initialized = False

        logger.success(
            "Application container shut down."
        )


container = ApplicationContainer()