"""
Knowledge corpus models.

Defines all models used by the knowledge ingestion pipeline.
"""

from datetime import datetime
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field


class CorpusDocument(BaseModel):
    """
    Represents one document inside the knowledge corpus.
    """

    # ----------------------------
    # Identity
    # ----------------------------

    id: str

    title: str

    author: str = "Andrew Ng"

    # ----------------------------
    # File Information
    # ----------------------------

    path: Path

    source: str

    category: str

    extension: str

    checksum: str

    language: str = "en"

    tags: List[str] = Field(default_factory=list)

    # ----------------------------
    # Knowledge Pipeline
    # ----------------------------

    indexed: bool = False

    embedding_model: Optional[str] = None

    chunk_count: int = 0

    vector_count: int = 0

    last_indexed: Optional[datetime] = None

    # ----------------------------
    # Personality Pipeline
    # ----------------------------

    personality_processed: bool = False

    last_personality_update: Optional[datetime] = None

    # ----------------------------
    # Metadata
    # ----------------------------

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow
    )


class CorpusRegistry(BaseModel):
    """
    Registry of every imported document.
    """

    documents: List[
        CorpusDocument
    ] = Field(default_factory=list)


class CorpusStats(BaseModel):
    """
    Overall corpus statistics.
    """

    total_documents: int = 0

    indexed_documents: int = 0

    personality_documents: int = 0

    total_chunks: int = 0

    total_vectors: int = 0

    total_size_mb: float = 0.0

    last_updated: Optional[datetime] = None