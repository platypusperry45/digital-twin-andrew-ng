"""
Application dependency container.

Maintains shared singleton services.
"""

from typing import Optional

from backend.llm import GeminiClient

from backend.memory.memory_manager import MemoryManager

from backend.rag.pipeline.knowledge_pipeline import KnowledgePipeline


class Container:

    def __init__(self):

        self._gemini_client: Optional[
            GeminiClient
        ] = None

        self._memory_manager: Optional[
            MemoryManager
        ] = None

        self._knowledge_pipeline: Optional[
            KnowledgePipeline
        ] = None

    def initialize(self):
        """
        Initialize all shared services.
        """

        self._gemini_client = GeminiClient()

        self._memory_manager = MemoryManager()

        self._knowledge_pipeline = KnowledgePipeline()

        self._knowledge_pipeline.initialize()

    def shutdown(self):
        """
        Cleanup resources.
        """

        self._gemini_client = None

        self._memory_manager = None

        self._knowledge_pipeline = None

    @property
    def gemini(
        self,
    ) -> GeminiClient:

        if self._gemini_client is None:

            raise RuntimeError(
                "Container not initialized"
            )

        return self._gemini_client

    @property
    def memory(
        self,
    ) -> MemoryManager:

        if self._memory_manager is None:

            raise RuntimeError(
                "Container not initialized"
            )

        return self._memory_manager

    @property
    def knowledge(
        self,
    ) -> KnowledgePipeline:

        if self._knowledge_pipeline is None:

            raise RuntimeError(
                "Container not initialized"
            )

        return self._knowledge_pipeline


container = Container()