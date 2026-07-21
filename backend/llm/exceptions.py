"""
LLM exception hierarchy.

Shared across:
- GeminiClient
- ConversationService
- API routes
- Embedding engine
"""

from __future__ import annotations

from typing import Optional


class LLMException(Exception):
    """
    Base exception for all LLM-related failures.
    """

    def __init__(
        self,
        message: str,
        *,
        original_exception: Exception | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.original_exception = original_exception

    def __str__(self) -> str:
        return self.message


class RetryableLLMError(LLMException):
    """
    Temporary provider-side failure.
    Safe to retry.
    """
    pass


class ModelUnavailableError(RetryableLLMError):
    """
    No model could successfully generate a response.
    """
    pass


class RateLimitError(RetryableLLMError):
    """
    API quota or rate limit exceeded.
    """
    pass


class AllKeysExhaustedError(RetryableLLMError):
    """
    Every configured API key is cooling down.
    """
    pass


class StructuredOutputError(LLMException):
    """
    Generated structured output could not be parsed
    or validated.
    """
    pass


class SafetyBlockedError(LLMException):
    """
    Gemini safety system blocked the request or response.
    """

    def __init__(
        self,
        message: str,
        *,
        blocked_reason: str | None = None,
        original_exception: Exception | None = None,
    ) -> None:

        super().__init__(
            message,
            original_exception=original_exception,
        )

        self.blocked_reason = blocked_reason


class InvalidConfigurationError(LLMException):
    """
    Invalid backend configuration.
    """
    pass


class AuthenticationError(LLMException):
    """
    Invalid API credentials.
    """
    pass


class TimeoutError(RetryableLLMError):
    """
    Upstream request timed out.
    """
    pass