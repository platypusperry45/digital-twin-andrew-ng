"""
Indexer models.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class IndexReport(BaseModel):
    """
    Result of an indexing operation.
    """

    documents: int

    chunks: int

    vectors: int

    elapsed_seconds: float

    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )