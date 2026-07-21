"""
Conversation manager.

Maintains per-session chat history and short-term memory.
"""

from __future__ import annotations

from backend.llm.models import (
    ChatMessage,
    GenerationConfig,
    LLMRequest,
)
from backend.memory.short_term import ShortTermMemory


class Conversation:
    """
    Session-scoped conversation.

    Owns:
    - Chat history sent to Gemini
    - Session short-term memory used by MemoryManager
    """

    def __init__(
        self,
        max_history: int = 100,
        short_term_turns: int = 20,
    ) -> None:

        self.messages: list[ChatMessage] = []

        self.short_term = ShortTermMemory(
            max_turns=short_term_turns,
        )

        self.max_history = max_history

    # ==========================================================
    # Chat History
    # ==========================================================

    def clear(self) -> None:

        self.messages.clear()
        self.short_term.clear()

    def add_user(
        self,
        message: str,
    ) -> None:

        self.messages.append(
            ChatMessage(
                role="user",
                content=message,
            )
        )

        self._trim_history()

    def add_assistant(
        self,
        message: str,
    ) -> None:

        self.messages.append(
            ChatMessage(
                role="assistant",
                content=message,
            )
        )

        self._trim_history()

    def history(
        self,
        limit: int | None = None,
    ) -> list[ChatMessage]:

        if limit is None:
            return list(self.messages)

        if limit <= 0:
            return []

        return list(self.messages)[-limit:]

    # ==========================================================
    # Short-Term Memory
    # ==========================================================

    def remember(
        self,
        *,
        user: str,
        assistant: str,
    ) -> None:

        self.short_term.add(
            user=user,
            assistant=assistant,
        )

    def memory(self) -> ShortTermMemory:

        return self.short_term

    # ==========================================================
    # Request Builder
    # ==========================================================

    def build_request(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        model: str | None = None,
        config: GenerationConfig | None = None,
    ) -> LLMRequest:

        return LLMRequest(
            user_prompt=prompt,
            system_prompt=system_prompt,
            messages=self.history(),
            model=model,
            config=config or GenerationConfig(),
        )

    # ==========================================================
    # Internal
    # ==========================================================

    def _trim_history(self) -> None:

        if len(self.messages) <= self.max_history:
            return

        excess = len(self.messages) - self.max_history

        del self.messages[:excess]