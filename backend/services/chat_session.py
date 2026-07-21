"""
Chat Session model representing an active user conversation.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional


class ChatSession:
    """
    Holds conversation history and turn state for a single active session.
    """

    def __init__(
        self,
        session_id: str,
        user_id: Optional[str] = "default_user",
    ) -> None:
        self.session_id = session_id
        self.user_id = user_id
        self.created_at = time.time()
        self.updated_at = time.time()
        self.messages: List[Dict[str, str]] = []

    def add_user_message(self, content: str) -> None:
        """Appends a user message turn."""
        self.messages.append({"role": "user", "content": content})
        self.updated_at = time.time()

    def add_assistant_message(self, content: str) -> None:
        """Appends an assistant message turn."""
        self.messages.append({"role": "assistant", "content": content})
        self.updated_at = time.time()

    def get_history(self) -> List[Dict[str, str]]:
        """Returns the complete sequence of message turns."""
        return list(self.messages)

    def clear(self) -> None:
        """Resets conversation history."""
        self.messages.clear()
        self.updated_at = time.time()