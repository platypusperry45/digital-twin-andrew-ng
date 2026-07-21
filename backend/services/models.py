"""
Service Models for Digital Twin of Andrew Ng.

Defines Pydantic models for chat/conversation requests, responses, session payloads,
and source attribution tracking.
"""

from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Incoming chat message request schema."""
    session_id: str = Field(..., description="Unique conversation session identifier")
    message: str = Field(..., description="User prompt or question")
    user_id: Optional[str] = Field(default="default_user", description="Optional user identifier")


class ChatResponse(BaseModel):
    """Outgoing chat message response schema."""
    session_id: str
    response_text: str
    sources: List[Any] = Field(default_factory=list, description="Retrieved RAG knowledge snippets or citations")
    latency_ms: float = Field(default=0.0, description="End-to-end execution latency in milliseconds")
    model_used: str = Field(default="gemini-2.5-flash", description="LLM model used for generation")


# Aliases to support legacy imports in backend.services.__init__
ConversationRequest = ChatRequest
ConversationResponse = ChatResponse


class SessionState(BaseModel):
    """Represents full history and metadata for a conversation session."""
    session_id: str
    created_at: float
    updated_at: float
    history: List[Dict[str, str]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)