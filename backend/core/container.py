"""
Application Dependency Injection Container.

Manages initializations, singletons, and service instantiations across
the Digital Twin backend graph.
"""

from __future__ import annotations

import threading
from functools import cached_property
from typing import Optional

from backend.core.logger import logger
from backend.llm.gemini_client import GeminiClient
from backend.memory.memory_manager import MemoryManager
from backend.personality.manager import PersonalityManager
from backend.prompt.prompt_builder import PromptBuilder
from backend.rag.embeddings.embedding_engine import EmbeddingEngine
from backend.rag.retrieval.retriever import Retriever
from backend.rag.vectorstore.chroma_store import ChromaStore
from backend.services.conversation_service import ConversationService
from backend.services.session_manager import SessionManager


class ApplicationContainer:
    """
    Central dependency injection graph container.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._initialized = False

    @cached_property
    def personality(self) -> PersonalityManager:
        logger.info("Initializing PersonalityManager")
        return PersonalityManager()

    @cached_property
    def memory(self) -> MemoryManager:
        logger.info("Initializing MemoryManager")
        return MemoryManager()

    @cached_property
    def embedding_engine(self) -> EmbeddingEngine:
        logger.info("Initializing EmbeddingEngine")
        return EmbeddingEngine()

    @cached_property
    def vector_store(self) -> ChromaStore:
        logger.info("Initializing ChromaStore")
        return ChromaStore(collection_name="knowledge_base")

    @cached_property
    def retriever(self) -> Retriever:
        logger.info("Initializing Retriever")
        return Retriever(
            vectorstore=self.vector_store,
            embedding_engine=self.embedding_engine,
        )

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

    def initialize(self) -> None:
        """Eagerly initializes all dependency singletons."""
        with self._lock:
            if not self._initialized:
                logger.info("Initializing application container and dependency graph...")
                _ = self.personality
                _ = self.memory
                _ = self.embedding_engine
                _ = self.vector_store
                _ = self.retriever
                _ = self.prompt_builder
                _ = self.llm
                _ = self.sessions
                _ = self.conversation_service
                self._initialized = True
                logger.info("Application container initialized successfully.")

    def shutdown(self) -> None:
        """Gracefully releases container resources during server shutdown."""
        with self._lock:
            if self._initialized:
                logger.info("Shutting down application container resources...")
                self._initialized = False
                logger.info("Application container shutdown cleanly.")


# Global Container Instance
container = ApplicationContainer()