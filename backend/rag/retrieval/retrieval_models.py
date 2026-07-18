"""
Retriever models.
"""

from pydantic import BaseModel, Field


class RetrievalResult(BaseModel):
    """
    One retrieved document.
    """

    text: str

    score: float

    source: str

    filename: str


class RetrievalResponse(BaseModel):
    """
    Retrieval response.
    """

    query: str

    results: list[RetrievalResult] = Field(
        default_factory=list
    )