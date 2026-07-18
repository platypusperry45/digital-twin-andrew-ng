"""
Short-term conversation memory.

Stores the most recent conversation turns in memory.
"""

from collections import deque
from threading import Lock
from typing import List

from backend.memory.models import (
    ConversationTurn,
)


class ShortTermMemory:
    """
    Thread-safe FIFO conversation buffer.
    """

    def __init__(
        self,
        max_turns: int = 20,
    ):

        self.max_turns = max_turns

        self.buffer = deque(maxlen=max_turns)

        self.lock = Lock()

    def add(
        self,
        user: str,
        assistant: str,
    ) -> None:

        with self.lock:

            self.buffer.append(
                ConversationTurn(
                    user=user,
                    assistant=assistant,
                )
            )

    def get_all(
        self,
    ) -> List[ConversationTurn]:

        with self.lock:

            return list(self.buffer)

    def last(
        self,
        n: int = 5,
    ) -> List[ConversationTurn]:

        with self.lock:

            if n <= 0:
                return []

            return list(self.buffer)[-n:]

    def clear(
        self,
    ) -> None:

        with self.lock:

            self.buffer.clear()

    def size(
        self,
    ) -> int:

        with self.lock:

            return len(self.buffer)

    def is_empty(
        self,
    ) -> bool:

        return self.size() == 0