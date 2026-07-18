"""
Knowledge Base Indexer.

Pipeline:

Directory
    ↓
Document Loader
    ↓
Chunker
    ↓
Embedding Engine
    ↓
Vector Store
"""

import time

from backend.core.logger import logger

from backend.rag.chunking import TextChunker
from backend.rag.embeddings import EmbeddingEngine
from backend.rag.indexing.index_models import (
    IndexReport,
)
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

    def index_directory(
        self,
        directory: str,
        clear_existing: bool = False,
    ) -> IndexReport:

        start = time.time()

        if clear_existing:

            self.store.clear()

        logger.info(
            f"Indexing directory: {directory}"
        )

        documents = (
            self.loader.load_directory(
                directory
            )
        )

        chunks = (
            self.chunker.chunk_documents(
                documents
            )
        )

        embeddings = (
            self.embedding.embed_documents(
                chunks
            )
        )

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

        elapsed = (
            time.time() - start
        )

        report = IndexReport(

            documents=len(documents),

            chunks=len(chunks),

            vectors=len(vectors),

            elapsed_seconds=elapsed,

        )

        logger.success(

            f"Indexed "

            f"{report.documents} docs | "

            f"{report.chunks} chunks | "

            f"{report.vectors} vectors "

            f"in {elapsed:.2f}s"

        )

        return report

    def stats(self):

        return self.store.stats()

    def count(self):

        return self.store.count()

    def clear(self):

        self.store.clear()