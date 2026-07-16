"""
Gemini API key manager.

Handles:
- round robin rotation
- cooldown
- failures
- thread safety
"""

from datetime import datetime, timedelta
from threading import Lock
from typing import List, Optional

from backend.llm.models import KeyStatus
from backend.llm.exceptions import AllKeysExhaustedError


class KeyManager:

    def __init__(
        self,
        keys: List[str],
        cooldown_seconds: int = 60,
    ):

        if not keys:
            raise ValueError("No Gemini API keys provided")

        self.keys = [
            key.strip()
            for key in keys
            if key.strip()
        ]

        self.cooldown_seconds = cooldown_seconds

        self.current_index = 0

        self.failures = {
            i: 0
            for i in range(len(self.keys))
        }

        self.cooldown_until = {
            i: None
            for i in range(len(self.keys))
        }

        self.last_used = {
            i: None
            for i in range(len(self.keys))
        }

        self.lock = Lock()

    def get_key(self):
        """
        Returns the next available key.

        Raises:
            AllKeysExhaustedError
        """

        with self.lock:

            total = len(self.keys)

            for _ in range(total):

                index = self.current_index

                self.current_index = (
                    self.current_index + 1
                ) % total

                if self._available(index):

                    self.last_used[index] = datetime.utcnow()

                    return (
                        self.keys[index],
                        index,
                    )

        raise AllKeysExhaustedError(
            "All Gemini API keys are cooling down or exhausted."
        )

    def mark_failure(
        self,
        index: int,
    ):

        with self.lock:

            self.failures[index] += 1

            self.cooldown_until[index] = (
                datetime.utcnow()
                + timedelta(
                    seconds=self.cooldown_seconds
                )
            )

    def mark_success(
        self,
        index: int,
    ):

        with self.lock:

            self.failures[index] = 0

            self.cooldown_until[index] = None

    def _available(
        self,
        index: int,
    ) -> bool:

        cooldown = self.cooldown_until[index]

        if cooldown is None:
            return True

        if datetime.utcnow() >= cooldown:

            self.cooldown_until[index] = None

            return True

        return False

    def status(self):

        result = []

        for index in range(len(self.keys)):

            result.append(

                KeyStatus(

                    index=index,

                    active=self._available(index),

                    failures=self.failures[index],

                    last_used=self.last_used[index],

                    cooldown_until=self.cooldown_until[index],
                )

            )

        return result

    def reset(self):
        """
        Clears cooldowns.
        Useful after replacing API keys.
        """

        with self.lock:

            for i in range(len(self.keys)):
                self.failures[i] = 0
                self.cooldown_until[i] = None

    def wait_until_available(self):

       while True:

            with self.lock:

                for index in range(len(self.keys)):

                   if self._available(index):
                       return

            import time
            time.sleep(1)