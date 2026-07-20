"""
Knowledge Base Indexer.

Supports:

- Single document indexing
- Multiple document indexing
- Directory indexing
- Statistics
- Vector management
"""

from __future__ import annotations

import time

from backend.core.logger import logger

from backend.rag.chunking import TextChunker
from backend.rag.embeddings import EmbeddingEngine
from backend.rag.indexing.index_models import IndexReport
from backend.rag.loaders import DocumentLoader
from backend.rag.vectorstore import (
    ChromaStore,
    StoredVector,
)


class Indexer:

    def __init__(self):

        self.loader = DocumentLoader()

        self.chunker = TextChunker()

        self.embedding = EmbeddingEngine()

        self.store = ChromaStore()

        logger.info(
            "Knowledge Indexer initialized."
        )

    # ---------------------------------------------------------
    # Internal helper
    # ---------------------------------------------------------

    def _store_embeddings(
        self,
        embeddings,
    ) -> int:

        vectors = []

        for emb in embeddings:

            vectors.append(

                StoredVector(

                    **emb.model_dump()

                )

            )

        self.store.add_many(
            vectors
        )

        return len(vectors)

    # ---------------------------------------------------------
    # Index one document
    # ---------------------------------------------------------

    def index_document(
        self,
        document: dict,
    ) -> IndexReport:

        start = time.time()

        chunks = self.chunker.chunk_document(
            document
        )

        embeddings = (
            self.embedding.embed_documents(
                chunks
            )
        )

        vector_count = self._store_embeddings(
            embeddings
        )

        elapsed = (
            time.time() - start
        )

        report = IndexReport(

            documents=1,

            chunks=len(chunks),

            vectors=vector_count,

            elapsed_seconds=elapsed,

        )

        logger.success(

            f"Indexed "

            f"{document['filename']} "

            f"({vector_count} vectors)"

        )

        return report

    # ---------------------------------------------------------
    # Index multiple documents
    # ---------------------------------------------------------

    def index_documents(
        self,
        documents: list[dict],
    ) -> IndexReport:

        start = time.time()

        total_chunks = 0

        total_vectors = 0

        for document in documents:

            report = self.index_document(
                document
            )

            total_chunks += report.chunks

            total_vectors += report.vectors

        elapsed = (
            time.time() - start
        )

        report = IndexReport(

            documents=len(documents),

            chunks=total_chunks,

            vectors=total_vectors,

            elapsed_seconds=elapsed,

        )

        logger.success(

            f"Indexed "

            f"{report.documents} documents "

            f"({report.vectors} vectors)"

        )

        return report

    # ---------------------------------------------------------
    # Index directory
    # ---------------------------------------------------------

    def index_directory(
        self,
        directory: str,
        clear_existing: bool = False,
    ) -> IndexReport:

        if clear_existing:

            self.clear()

        documents = (
            self.loader.load_directory(
                directory
            )
        )

        return self.index_documents(
            documents
        )

    # ---------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------

    def stats(self):

        return self.store.stats()

    def count(self):

        return self.store.count()

    def clear(self):

        self.store.clear()