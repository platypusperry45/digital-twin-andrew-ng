"""
Thread-safe API key manager.

Responsibilities
----------------
- Round-robin key rotation
- Cooldown management
- Success/failure tracking
- Health reporting
- Thread-safe operation
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import List, Tuple

from backend.llm.exceptions import AllKeysExhaustedError
from backend.llm.models import KeyStatus


@dataclass(slots=True)
class _KeyInfo:
    key: str
    index: int
    requests: int = 0
    successes: int = 0
    failures: int = 0
    last_used: float = 0.0
    cooldown_until: float = 0.0

    @property
    def active(self) -> bool:
        return time.time() >= self.cooldown_until

    @property
    def failure_rate(self) -> float:
        if self.requests == 0:
            return 0.0
        return self.failures / self.requests


class KeyManager:
    """
    Thread-safe Gemini API key rotation manager.
    """

    def __init__(
        self,
        api_keys: List[str],
        cooldown_seconds: float,
    ) -> None:

        if not api_keys:
            raise ValueError("At least one API key is required.")

        self._cooldown_seconds = cooldown_seconds
        self._lock = threading.Lock()
        self._cursor = 0
        self._keys = [
            _KeyInfo(
                key=key,
                index=index,
            )
            for index, key in enumerate(api_keys)
        ]

    def get_key(self) -> Tuple[str, int]:
        """Returns the next available API key in round-robin sequence."""
        with self._lock:
            now = time.time()
            total = len(self._keys)

            for _ in range(total):
                info = self._keys[self._cursor]
                self._cursor = (self._cursor + 1) % total

                if now >= info.cooldown_until:
                    info.requests += 1
                    info.last_used = now
                    return info.key, info.index

        raise AllKeysExhaustedError("All Gemini API keys are currently cooling down.")

    def mark_success(self, index: int) -> None:
        """Registers a successful API interaction for the key at index."""
        with self._lock:
            if 0 <= index < len(self._keys):
                self._keys[index].successes += 1

    def mark_failure(self, index: int) -> None:
        """Places key into cooldown following a rate-limit or API failure."""
        with self._lock:
            if 0 <= index < len(self._keys):
                info = self._keys[index]
                info.failures += 1
                info.cooldown_until = time.time() + self._cooldown_seconds

    def wait_until_available(self) -> None:
        """Blocks thread until at least one API key clears its cooldown period."""
        while True:
            with self._lock:
                now = time.time()
                remaining = [
                    max(0.0, key.cooldown_until - now)
                    for key in self._keys
                ]
            minimum = min(remaining)
            if minimum <= 0:
                return
            time.sleep(min(minimum, 0.5))

    def reset(self) -> None:
        """Resets all cooldown states and metrics tracking counters."""
        with self._lock:
            for key in self._keys:
                key.cooldown_until = 0.0
                key.requests = 0
                key.successes = 0
                key.failures = 0
                key.last_used = 0.0

    def status(self) -> List[KeyStatus]:
        """Returns diagnostic operational status for all managed keys."""
        with self._lock:
            now = time.time()
            return [
                KeyStatus(
                    index=key.index,
                    active=key.active,
                    requests=key.requests,
                    successes=key.successes,
                    failures=key.failures,
                    failure_rate=key.failure_rate,
                    last_used=key.last_used,
                    cooldown_until=key.cooldown_until,
                    seconds_remaining=max(0.0, key.cooldown_until - now),
                )
                for key in self._keys
            ]

    @property
    def total_keys(self) -> int:
        return len(self._keys)

    @property
    def active_keys(self) -> int:
        with self._lock:
            return sum(key.active for key in self._keys)