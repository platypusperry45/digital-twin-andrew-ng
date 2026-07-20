"""
Production LLM request/response models.

These models are shared by every AI component:

- Conversation Service
- Personality Extraction
- RAG
- Embeddings
- Future Voice
- Future Vision
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


# ============================================================
# Chat Message
# ============================================================

class ChatMessage(BaseModel):
    """
    Represents one message in a conversation.
    """

    role: str = Field(
        description="system | user | assistant"
    )

    content: str


# ============================================================
# Generation Configuration
# ============================================================

class GenerationConfig(BaseModel):
    """
    Optional generation parameters.
    """

    temperature: float = 0.7

    top_p: float = 0.95

    top_k: int = 40

    max_output_tokens: int = 4096

    candidate_count: int = 1

    stop_sequences: list[str] = Field(
        default_factory=list
    )


# ============================================================
# LLM Request
# ============================================================

class LLMRequest(BaseModel):
    """
    Generic request model.

    Supports

    - Chat
    - Structured Extraction
    - Streaming
    - Future Vision
    """

    # -------------------------
    # Prompts
    # -------------------------

    system_prompt: str = ""

    user_prompt: str

    messages: list[ChatMessage] = Field(
        default_factory=list
    )

    # -------------------------
    # Model
    # -------------------------

    model: str | None = None

    # -------------------------
    # Generation
    # -------------------------

    config: GenerationConfig = Field(
        default_factory=GenerationConfig
    )

    # -------------------------
    # Structured Output
    # -------------------------

    response_schema: type[BaseModel] | None = None

    # -------------------------
    # Streaming
    # -------------------------

    stream: bool = False

    # -------------------------
    # Metadata
    # -------------------------

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


# ============================================================
# Embedding Request
# ============================================================

class EmbeddingRequest(BaseModel):

    text: str

    model: str | None = None


# ============================================================
# LLM Usage Statistics
# ============================================================

class TokenUsage(BaseModel):

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0


# ============================================================
# LLM Response
# ============================================================

class LLMResponse(BaseModel):
    """
    Unified response model.
    """

    text: str

    raw: Any | None = None

    model_used: str

    key_index: int

    latency_ms: float

    usage: TokenUsage = Field(
        default_factory=TokenUsage
    )

    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )


# ============================================================
# Embedding Response
# ============================================================

class EmbeddingResponse(BaseModel):

    vector: list[float]

    model_used: str

    latency_ms: float


# ============================================================
# API Key Status
# ============================================================

class KeyStatus(BaseModel):

    index: int

    active: bool

    failures: int

    requests: int = 0

    successes: int = 0

    last_used: datetime | None = None

    cooldown_until: datetime | None = None


# ============================================================
# Health Check
# ============================================================

class LLMHealth(BaseModel):

    available_models: list[str] = Field(
        default_factory=list
    )

    active_keys: int = 0

    total_keys: int = 0

    scheduler: str = ""

    embedding_model: str = ""

    chat_model: str = ""