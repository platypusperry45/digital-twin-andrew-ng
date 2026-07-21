"""
Session Manager for Digital Twin of Andrew Ng.

Manages active conversation sessions, turn histories, and state lifecycles in memory.
"""

from __future__ import annotations

import time
import threading
from typing import Dict, List, Any, Optional

from backend.core.logger import logger
from backend.services.chat_session import ChatSession


class SessionManager:
    """
    Thread-safe manager storing active conversation sessions.
    """

    def __init__(self) -> None:
        self._sessions: Dict[str, ChatSession] = {}
        self._lock = threading.Lock()
        logger.info("SessionManager initialized.")

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Retrieves an existing session if found."""
        with self._lock:
            return self._sessions.get(session_id)

    def create_session(self, session_id: str) -> ChatSession:
        """Creates and stores a new ChatSession instance."""
        with self._lock:
            session = ChatSession(session_id=session_id)
            self._sessions[session_id] = session
            logger.info(f"Created new session: '{session_id}'")
            return session

    def get_or_create(self, session_id: str) -> ChatSession:
        """
        Retrieves an existing session or creates a new one atomically.
        """
        with self._lock:
            if session_id not in self._sessions:
                logger.info(f"Session '{session_id}' not found. Creating new session.")
                self._sessions[session_id] = ChatSession(session_id=session_id)
            return self._sessions[session_id]

    def remove_session(self, session_id: str) -> bool:
        """Removes a session from memory."""
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
                logger.info(f"Removed session: '{session_id}'")
                return True
            return False

    def clear(self) -> None:
        """Clears all active sessions."""
        with self._lock:
            count = len(self._sessions)
            self._sessions.clear()
            logger.info(f"Cleared {count} active sessions from SessionManager.")