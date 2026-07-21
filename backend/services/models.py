"""
Conversation service models.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ConversationRequest(BaseModel):
    """
    Incoming chat request.
    """

    message: str = Field(
        ...,
        min_length=1,
    )

    session_id: str | None = None


class ConversationResponse(BaseModel):
    """
    Response returned by ConversationService.
    """

    response: str

    session_id: str

    model: str

    latency_ms: float

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0

    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
    )