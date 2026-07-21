"""
LLM Scheduler.

Responsible for model selection and fallback order.

Responsibilities
----------------
- Primary model selection
- Fast model selection
- Fallback model selection
- Ordered retry chain
"""

from __future__ import annotations

from backend.core.config import settings
from backend.core.logger import logger


class LLMScheduler:
    """
    Model scheduler used by GeminiClient.
    """

    def __init__(self) -> None:

        self.primary = getattr(
            settings,
            "GEMINI_MODEL",
            "gemini-2.5-pro",
        )

        self.fast = getattr(
            settings,
            "FAST_MODEL",
            "gemini-2.5-flash",
        )

        self.fallback = getattr(
            settings,
            "FALLBACK_MODEL",
            "gemini-2.5-flash-lite",
        )

        logger.info(
            "LLM Scheduler initialized."
        )

    # =========================================================

    def get_model_sequence(
        self,
        requested_model: str | None = None,
    ) -> list[str]:
        """
        Returns the ordered model fallback chain.

        Priority:

        requested model
              ↓
        primary
              ↓
        fast
              ↓
        fallback
        """

        sequence: list[str] = []

        if requested_model:
            sequence.append(requested_model)

        sequence.extend(
            [
                self.primary,
                self.fast,
                self.fallback,
            ]
        )

        # remove duplicates while preserving order
        unique: list[str] = []
        seen: set[str] = set()

        for model in sequence:

            if model not in seen:
                seen.add(model)
                unique.append(model)

        return unique

    # =========================================================

    def choose(
        self,
        requested_model: str | None = None,
    ) -> str:
        """
        Returns the first model that should be tried.
        """

        return self.get_model_sequence(
            requested_model
        )[0]

    # =========================================================

    @property
    def models(self) -> list[str]:

        return [
            self.primary,
            self.fast,
            self.fallback,
        ]

    # =========================================================

    def health(self) -> dict:

        return {
            "primary": self.primary,
            "fast": self.fast,
            "fallback": self.fallback,
            "available_models": self.models,
        }