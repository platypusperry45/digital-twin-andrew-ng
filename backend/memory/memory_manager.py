"""
Central memory manager.

Responsibilities
----------------
- Global long-term memory
- Semantic retrieval
- Conversation summarization

Session-specific short-term memory is owned by
ChatSession.
"""

from __future__ import annotations

from backend.core.logger import logger

from backend.memory.long_term import LongTermMemory
from backend.memory.retriever import MemoryRetriever
from backend.memory.short_term import ShortTermMemory
from backend.memory.summarizer import ConversationSummarizer


class MemoryManager:
    """
    Coordinates global memory services.

    ChatSession owns short-term memory.
    MemoryManager owns long-term memory.
    """

    def __init__(self) -> None:

        self.long_term = LongTermMemory()

        self.retriever = MemoryRetriever(
            self.long_term,
        )

        self.summarizer = ConversationSummarizer()

        self.summary_threshold = 20

    # ==========================================================
    # Retrieval
    # ==========================================================

    def retrieve_context(
        self,
        *,
        query: str,
        short_term: ShortTermMemory,
    ):
        """
        Retrieve context using the active session's
        short-term memory together with global
        long-term memory.
        """

        return self.retriever.retrieve(
            query=query,
            short_term=short_term,
        )

    # ==========================================================
    # Persistence
    # ==========================================================

    def add_conversation(
        self,
        *,
        short_term: ShortTermMemory,
        user: str,
        assistant: str,
    ) -> None:
        """
        Store conversation.

        Short-term memory is session scoped.

        Long-term memory is shared.
        """

        short_term.add(
            user=user,
            assistant=assistant,
        )

        self.long_term.add(
            role="user",
            content=user,
        )

        self.long_term.add(
            role="assistant",
            content=assistant,
        )

        logger.info("Conversation stored.")

        if short_term.size() >= self.summary_threshold:
            self._summarize(short_term)

    # ==========================================================
    # Maintenance
    # ==========================================================

    def clear(
        self,
        short_term: ShortTermMemory,
    ) -> None:

        short_term.clear()

        self.long_term.clear()

        logger.info("Memory cleared.")

    def stats(self) -> dict:

        return {
            "long_term": self.long_term.count(),
        }

    # ==========================================================
    # Internal
    # ==========================================================

    def _summarize(
        self,
        short_term: ShortTermMemory,
    ) -> None:

        turns = short_term.get_all()

        if not turns:
            return

        conversation = ""

        for turn in turns:

            conversation += (
                f"User: {turn.user}\n"
                f"Assistant: {turn.assistant}\n\n"
            )

        summary = self.summarizer.summarize(
            conversation
        )

        self.long_term.add(
            role="summary",
            content=summary,
            metadata={
                "generated": True,
            },
        )

        short_term.clear()

        logger.info(
            "Conversation summarized and archived."
        )