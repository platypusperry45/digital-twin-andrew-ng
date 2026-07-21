"""
Knowledge Base Indexer.

Supports

- Incremental indexing
- Single document indexing
- Multiple document indexing
- Directory indexing
- Registry synchronization
- Statistics
- Vector management
"""

from __future__ import annotations

import time
from pathlib import Path

from backend.core.logger import logger

from backend.knowledge.corpus_manager import CorpusManager
from backend.knowledge.registry import Registry

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

        self.registry = Registry()

        self.corpus = CorpusManager()

        logger.info(
            "Knowledge Indexer initialized."
        )

    # =====================================================
    # Internal Helpers
    # =====================================================

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

    # =====================================================
    # Single Document
    # =====================================================

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

        elapsed = time.time() - start

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

    # =====================================================
    # Multiple Documents
    # =====================================================

    def index_documents(
        self,
        documents: list[dict],
    ) -> IndexReport:

        start = time.time()

        total_chunks = 0

        total_vectors = 0

        indexed_documents = 0

        for document in documents:

            report = self.index_document(
                document
            )

            indexed_documents += 1

            total_chunks += report.chunks

            total_vectors += report.vectors

        elapsed = time.time() - start

        report = IndexReport(

            documents=indexed_documents,

            chunks=total_chunks,

            vectors=total_vectors,

            elapsed_seconds=elapsed,

        )

        logger.success(

            f"Indexed "

            f"{indexed_documents} documents "

            f"({total_vectors} vectors)"

        )

        return report

    # =====================================================
    # Incremental Corpus Indexing
    # =====================================================

    def index_corpus(
        self,
    ) -> IndexReport:

        logger.info(
            "Scanning knowledge corpus..."
        )

        corpus_documents = self.corpus.scan()

        documents_to_index = []

        for corpus_doc in corpus_documents:

            if self.registry.contains(
                corpus_doc.checksum
            ):

                logger.debug(
                    f"Skipping unchanged document: "
                    f"{corpus_doc.title}"
                )

                continue

            loaded = self.loader.load_file(
                corpus_doc.path
            )

            if loaded is None:
                continue

            documents_to_index.append(
                (
                    corpus_doc,
                    loaded,
                )
            )

        if not documents_to_index:

            logger.success(
                "Knowledge base already up to date."
            )

            return IndexReport(
                documents=0,
                chunks=0,
                vectors=0,
                elapsed_seconds=0,
            )

        start = time.time()

        total_documents = 0

        total_chunks = 0

        total_vectors = 0

        for corpus_doc, loaded_doc in documents_to_index:

            report = self.index_document(
                loaded_doc
            )

            total_documents += report.documents

            total_chunks += report.chunks

            total_vectors += report.vectors

            self.registry.update(
                corpus_doc
            )

        self.registry.save()

        elapsed = time.time() - start

        logger.success(

            f"Incremental indexing complete. "

            f"{total_documents} new documents."

        )

        return IndexReport(

            documents=total_documents,

            chunks=total_chunks,

            vectors=total_vectors,

            elapsed_seconds=elapsed,

        )

    # =====================================================
    # Directory Indexing (Legacy)
    # =====================================================

    def index_directory(
        self,
        directory: str | Path,
        clear_existing: bool = False,
    ) -> IndexReport:

        if clear_existing:

            self.clear()

        documents = self.loader.load_directory(
            directory
        )

        return self.index_documents(
            documents
        )

    # =====================================================
    # Utilities
    # =====================================================

    def stats(self):

        stats = self.store.stats()

        stats["registry_documents"] = len(
            self.registry.all()
        )

        return stats

    def count(self):

        return self.store.count()

    def clear(self):

        self.store.clear()

        self.registry.clear()

        logger.warning(
            "Knowledge index cleared."
        )