"""
Knowledge Retriever.

Flow:

Question
    ↓
Embedding
    ↓
Vector Search
    ↓
Relevant Chunks
"""

from backend.core.config import settings
from backend.core.logger import logger

from backend.rag.embeddings import EmbeddingEngine
from backend.rag.retrieval.retrieval_models import (
    RetrievalResult,
    RetrievalResponse,
)
from backend.rag.vectorstore import ChromaStore


class Retriever:

    def __init__(self):

        self.embedding = EmbeddingEngine()

        self.store = ChromaStore()

        logger.info(
            "Knowledge Retriever initialized."
        )

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
        min_score: float = 0.60,
    ) -> RetrievalResponse:

        if top_k is None:

            top_k = settings.TOP_K_RESULTS

        logger.info(
            f"Searching knowledge base: {query}"
        )

        query_embedding = (
            self.embedding.embed_query(
                query
            )
        )

        matches = self.store.search(
            embedding=query_embedding,
            top_k=top_k,
        )

        results = []

        for item in matches:

            if item.score < min_score:
                continue

            results.append(

                RetrievalResult(

                    text=item.text,

                    score=item.score,

                    source=item.source,

                    filename=item.filename,

                )

            )

        logger.success(
            f"Retrieved {len(results)} documents."
        )

        return RetrievalResponse(

            query=query,

            results=results,

        )
