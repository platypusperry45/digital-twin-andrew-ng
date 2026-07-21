"""
LLM shared models.

Central contracts between:
- Conversation Service
- Prompt Builder
- Gemini Client
- Streaming layer
"""

from __future__ import annotations

from typing import Any, Type

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):

    role: str

    content: str



class GenerationConfig(BaseModel):

    temperature: float = 0.3

    top_p: float | None = None

    top_k: int | None = None

    max_output_tokens: int | None = None

    candidate_count: int = 1

    stop_sequences: list[str] | None = None



class LLMRequest(BaseModel):

    user_prompt: str

    system_prompt: str | None = None

    messages: list[ChatMessage] = Field(
        default_factory=list
    )

    model: str | None = None

    config: GenerationConfig = Field(
        default_factory=GenerationConfig
    )

    response_schema: Type[BaseModel] | None = None



class TokenUsage(BaseModel):

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0



class LLMResponse(BaseModel):

    text: str

    model_used: str

    latency_ms: float

    usage: TokenUsage

    key_index: int | None = None

    finish_reason: str = "UNKNOWN"

    cached: bool = False

    request_id: str | None = None

    retry_count: int = 0

    raw: Any | None = None



class EmbeddingRequest(BaseModel):

    text: str

    model: str | None = None



class EmbeddingResponse(BaseModel):

    vector: list[float]

    model_used: str

    latency_ms: float



class LLMHealth(BaseModel):

    available_models: list[str]

    cached_clients: int

    active_keys: int

    total_keys: int

    key_statuses: list[Any]

    metrics_summary: dict

    scheduler_mode: str

    embedding_model: str

    chat_model: str
    
class KeyStatus(BaseModel):
    """
    Runtime status of a single Gemini API key.
    """

    index: int

    active: bool

    requests: int = 0

    successes: int = 0

    failures: int = 0

    failure_rate: float = 0.0

    last_used: float = 0.0

    cooldown_until: float = 0.0

    seconds_remaining: float = 0.0