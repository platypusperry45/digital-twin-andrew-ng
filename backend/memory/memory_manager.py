"""
Central memory manager.

Coordinates:
- Short-term memory
- Long-term memory
- Retrieval
- Summarization
"""

from backend.core.logger import logger

from backend.memory.short_term import ShortTermMemory
from backend.memory.long_term import LongTermMemory
from backend.memory.retriever import MemoryRetriever
from backend.memory.summarizer import ConversationSummarizer


class MemoryManager:

    def __init__(self):

        self.short_term = ShortTermMemory()

        self.long_term = LongTermMemory()

        self.retriever = MemoryRetriever(
            self.short_term,
            self.long_term,
            )

        self.summarizer = ConversationSummarizer()

        # Number of conversation turns before summarization
        self.summary_threshold = 20

    def add_conversation(
        self,
        user: str,
        assistant: str,
    ) -> None:
        """
        Store one conversation turn.
        """

        self.short_term.add(
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

        logger.info(
            "Conversation stored."
        )

        if self.short_term.size() >= self.summary_threshold:

            self._summarize()

    def retrieve_context(
        self,
        query: str,
    ):

        return self.retriever.retrieve(
            query=query,
        )

    def clear(self):

        self.short_term.clear()

        self.long_term.clear()

        logger.info(
            "Memory cleared."
        )

    def stats(self):

        return {

            "short_term": self.short_term.size(),

            "long_term": self.long_term.count(),

        }

    def _summarize(self):

        turns = self.short_term.get_all()

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

        self.short_term.clear()

        logger.info(
            "Conversation summarized and archived."
        )