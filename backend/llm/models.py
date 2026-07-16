"""
LLM request and response models.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class LLMRequest(BaseModel):

    prompt: str = Field(
        ...,
        min_length=1
    )

    model: Optional[str] = None

    temperature: float = 0.7


    metadata: dict = Field(
        default_factory=dict
    )



class LLMResponse(BaseModel):

    content: str

    model_used: str

    key_index: int

    latency_ms: float

    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )



class KeyStatus(BaseModel):

    index: int

    active: bool

    failures: int

    last_used: Optional[datetime] = None

    cooldown_until: Optional[datetime] = None