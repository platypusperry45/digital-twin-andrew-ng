"""
Conversation service models.
"""

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


class ConversationResponse(BaseModel):
    """
    Response returned by ConversationService.
    """

    response: str

    model: str

    latency_ms: float

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0

    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )