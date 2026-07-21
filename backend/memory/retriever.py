"""
Memory retriever.

Combines:
- session short-term memory
- global long-term semantic memory

into a single context object.
"""

from __future__ import annotations

from backend.core.config import settings

from backend.memory.long_term import LongTermMemory
from backend.memory.models import MemoryContext
from backend.memory.short_term import ShortTermMemory


class MemoryRetriever:
    """
    Retrieves memory context.

    Long-term memory is shared globally.

    Short-term memory is supplied by the active
    ChatSession.
    """

    def __init__(
        self,
        long_term: LongTermMemory,
    ) -> None:

        self.long_term = long_term

    def retrieve(
        self,
        *,
        query: str,
        short_term: ShortTermMemory,
    ) -> MemoryContext:
        """
        Build the complete memory context.
        """

        return MemoryContext(
            short_term=short_term.get_all(),
            long_term=self.long_term.search(
                query=query,
                top_k=settings.TOP_K_RESULTS,
            ),
        )

    def clear(
        self,
        short_term: ShortTermMemory,
    ) -> None:
        """
        Clear session short-term memory and
        global long-term memory.
        """

        short_term.clear()

        self.long_term.clear()