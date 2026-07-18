"""
Memory models.

Shared models used by the entire memory system.
"""

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class MemoryItem(BaseModel):
    """
    Single memory entry.
    """

    id: str

    role: str

    content: str

    timestamp: datetime = Field(default_factory=datetime.utcnow)

    metadata: Dict = Field(default_factory=dict)


class MemorySearchResult(BaseModel):
    """
    Retrieved memory.
    """

    memory: MemoryItem

    score: float


class ConversationTurn(BaseModel):
    """
    One user-assistant interaction.
    """

    user: str

    assistant: str

    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MemoryContext(BaseModel):
    """
    Context sent into the LLM.
    """

    short_term: List[ConversationTurn] = Field(default_factory=list)

    long_term: List[MemorySearchResult] = Field(default_factory=list)


class MemoryStats(BaseModel):
    """
    Memory statistics.
    """

    total_memories: int = 0

    total_embeddings: int = 0

    total_queries: int = 0

    cache_hits: int = 0