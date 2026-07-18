"""
Service models.

Models shared by the service layer.
"""

from typing import List

from pydantic import BaseModel

from backend.llm.models import LLMResponse

from backend.memory.models import MemoryContext

from backend.rag.retrieval.retrieval_models import (
    RetrievalResponse,
)


class ConversationResponse(BaseModel):
    """
    Complete response returned by the
    Conversation Service.
    """

    llm: LLMResponse

    memory: MemoryContext

    knowledge: RetrievalResponse

    final_prompt: str


class SourceReference(BaseModel):
    """
    One knowledge source used in the response.
    """

    filename: str

    source: str

    score: float


class ChatResponse(BaseModel):
    """
    Final API response.
    """

    success: bool

    response: str

    model: str

    latency_ms: float

    timestamp: str

    sources: List[SourceReference] = []