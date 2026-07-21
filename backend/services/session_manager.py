"""
Session Manager.

Maintains one Conversation object per client session.

Each user/browser receives an independent conversation
history while sharing the same application services.
"""

from __future__ import annotations

from threading import Lock
from uuid import uuid4

from backend.llm.conversation import Conversation


class SessionManager:
    """
    Thread-safe session manager.

    Maps

        session_id -> Conversation
    """

    def __init__(self) -> None:

        self._sessions: dict[str, Conversation] = {}

        self._lock = Lock()

    # ==========================================================
    # Session Management
    # ==========================================================

    def create_session(self) -> str:
        """
        Create a new conversation session.
        """

        session_id = str(uuid4())

        with self._lock:
            self._sessions[session_id] = Conversation()

        return session_id

    def get(
        self,
        session_id: str,
    ) -> Conversation:
        """
        Return an existing conversation.

        If the session doesn't exist, create it.
        """

        with self._lock:

            conversation = self._sessions.get(session_id)

            if conversation is None:
                conversation = Conversation()
                self._sessions[session_id] = conversation

            return conversation

    def exists(
        self,
        session_id: str,
    ) -> bool:

        with self._lock:
            return session_id in self._sessions

    def delete(
        self,
        session_id: str,
    ) -> None:

        with self._lock:
            self._sessions.pop(session_id, None)

    def clear(self) -> None:

        with self._lock:
            self._sessions.clear()

    def count(self) -> int:

        with self._lock:
            return len(self._sessions)

    def session_ids(self) -> list[str]:

        with self._lock:
            return list(self._sessions.keys())