"""
Vector Store models.
"""

from datetime import datetime
from typing import Dict

from pydantic import BaseModel, Field


class StoredVector(BaseModel):
    """
    Vector stored inside ChromaDB.
    """

    id: str

    vector: list[float]

    text: str

    source: str

    filename: str

    metadata: Dict = Field(
        default_factory=dict
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )


class RetrievedVector(BaseModel):
    """
    Result returned from similarity search.
    """

    id: str

    score: float

    text: str

    source: str

    filename: str

    metadata: Dict = Field(
        default_factory=dict
    )