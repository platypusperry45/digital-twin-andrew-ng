"""
Per-conversation chat session.

Owns all session-scoped state.

Responsibilities
----------------
- Conversation history
- Short-term memory
- Session metadata
"""

from __future__ import annotations

from datetime import datetime
from threading import Lock
from uuid import uuid4

from backend.llm.conversation import Conversation
from backend.memory.short_term import ShortTermMemory


class ChatSession:
    """
    Represents one active chat session.

    Each user conversation receives its own instance.
    """

    def __init__(self) -> None:

        self.id = str(uuid4())

        self.created_at = datetime.utcnow()

        self.last_access = self.created_at

        self.lock = Lock()

        self.conversation = Conversation()

        self.short_term = ShortTermMemory()

        self.metadata: dict = {}

    def touch(self) -> None:
        """
        Update last-access timestamp.
        """
        with self.lock:
            self.last_access = datetime.utcnow()

    def clear(self) -> None:
        """
        Reset session state.
        """
        with self.lock:
            self.conversation.clear()
            self.short_term.clear()

    @property
    def age_seconds(self) -> float:
        return (
            datetime.utcnow() - self.created_at
        ).total_seconds()

    @property
    def idle_seconds(self) -> float:
        return (
            datetime.utcnow() - self.last_access
        ).total_seconds()