"""
Memory retriever.

Combines:
- short-term memory
- long-term semantic memory

into a single context object.
"""

from backend.core.config import settings

from backend.memory.models import MemoryContext
from backend.memory.short_term import ShortTermMemory
from backend.memory.long_term import LongTermMemory


class MemoryRetriever:
    """
    Retrieves memory context using existing memory instances.

    IMPORTANT:
    This class does NOT create its own memory objects.
    It operates on the instances owned by MemoryManager.
    """

    def __init__(
        self,
        short_term: ShortTermMemory,
        long_term: LongTermMemory,
    ):

        self.short_term = short_term
        self.long_term = long_term

    def retrieve(
        self,
        query: str,
    ) -> MemoryContext:
        """
        Build the memory context for an LLM request.
        """

        context = MemoryContext()

        # Recent conversation
        context.short_term = self.short_term.get_all()

        # Relevant semantic memories
        context.long_term = self.long_term.search(
            query=query,
            top_k=settings.TOP_K_RESULTS,
        )

        return context

    def clear(self) -> None:
        """
        Clear both memory stores.
        """

        self.short_term.clear()
        self.long_term.clear()