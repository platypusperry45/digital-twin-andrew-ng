"""
LLM Scheduler for model ordering and fallback routing.
"""

from __future__ import annotations

from typing import List, Dict, Any, Optional
from backend.core.config import settings
from backend.core.logger import logger


class LLMScheduler:
    """
    Model scheduler used by GeminiClient to manage cascading fallbacks.
    """

    def __init__(self) -> None:
        self.primary = getattr(settings, "PRIMARY_MODEL", "gemini-2.5-flash")
        self.fast = getattr(settings, "FAST_MODEL", "gemini-2.5-flash")
        self.fallback = getattr(settings, "FALLBACK_MODEL", "gemini-3.1-flash-lite")

        logger.info("LLM Scheduler initialized.")

    def get_model_sequence(
        self,
        requested_model: Optional[str] = None,
    ) -> List[str]:
        """
        Returns the ordered model fallback chain.
        """
        sequence: List[str] = []

        if requested_model:
            sequence.append(requested_model)

        sequence.extend([self.primary, self.fast, self.fallback])

        unique: List[str] = []
        seen: set[str] = set()

        for model in sequence:
            if model and model not in seen:
                seen.add(model)
                unique.append(model)

        return unique

    def choose(
        self,
        requested_model: Optional[str] = None,
    ) -> str:
        """Returns the primary model selected for execution."""
        return self.get_model_sequence(requested_model)[0]

    @property
    def models(self) -> List[str]:
        return [self.primary, self.fast, self.fallback]

    def health(self) -> Dict[str, Any]:
        return {
            "primary": self.primary,
            "fast": self.fast,
            "fallback": self.fallback,
            "available_models": self.models,
        }