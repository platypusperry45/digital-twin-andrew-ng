"""
Central Memory Manager coordinating global short-term and long-term memory.
"""

from __future__ import annotations

from typing import Any, Dict, Optional
from backend.core.logger import logger
from backend.memory.long_term import LongTermMemory
from backend.memory.retriever import MemoryRetriever
from backend.memory.short_term import ShortTermMemory
from backend.memory.summarizer import ConversationSummarizer


class MemoryManager:
    """
    Coordinates global memory services across session buffers and persistent vector storage.
    """

    def __init__(self) -> None:
        self.long_term = LongTermMemory()
        self.retriever = MemoryRetriever(self.long_term)
        self.summarizer = ConversationSummarizer()
        self.summary_threshold = 20

    def retrieve_context(
        self,
        *,
        query: str,
        short_term: ShortTermMemory,
    ):
        """Retrieves combined memory context across session turns and vector storage."""
        return self.retriever.retrieve(
            query=query,
            short_term=short_term,
        )

    def add_conversation(
        self,
        *,
        short_term: ShortTermMemory,
        user: str,
        assistant: str,
    ) -> None:
        """Stores a turn pair in short-term buffer and persists to long-term memory."""
        short_term.add(
            user=user,
            assistant=assistant,
        )

        try:
            self.long_term.add(role="user", content=user)
            self.long_term.add(role="assistant", content=assistant)
        except Exception as e:
            logger.warning(f"Failed to index turn in long-term memory store: {e}")

        logger.info("Conversation turn stored.")

        if short_term.size() >= self.summary_threshold:
            self._summarize(short_term)

    def clear(self, short_term: ShortTermMemory) -> None:
        """Clears session and global long-term memory entries."""
        short_term.clear()
        try:
            self.long_term.clear()
        except Exception as e:
            logger.warning(f"Error clearing long-term store: {e}")
        logger.info("Memory cleared.")

    def stats(self) -> Dict[str, Any]:
        count = self.long_term.count() if hasattr(self.long_term, "count") else 0
        return {"long_term": count}

    def _summarize(self, short_term: ShortTermMemory) -> None:
        """Summarizes old turns and archives to long-term memory."""
        turns = short_term.get_all()
        if not turns:
            return

        conversation = ""
        for turn in turns:
            conversation += f"User: {turn.user}\nAssistant: {turn.assistant}\n\n"

        try:
            summary = self.summarizer.summarize(conversation)
            self.long_term.add(
                role="summary",
                content=summary,
                metadata={"generated": True},
            )
            short_term.clear()
            logger.info("Conversation summarized and archived cleanly.")
        except Exception as e:
            logger.warning(f"Conversation summarization encountered an error: {e}")