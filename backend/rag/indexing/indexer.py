"""
Knowledge Base Indexer.

Supports:
- Incremental indexing
- Single document indexing
- Multiple document indexing
- Directory indexing
- Registry synchronization
- Vector management
"""

from __future__ import annotations

import time
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

from backend.core.logger import logger
from backend.knowledge.corpus_manager import CorpusManager
from backend.knowledge.registry import Registry
from backend.rag.chunking.text_chunker import TextChunker
from backend.rag.embeddings.embedding_engine import EmbeddingEngine
from backend.rag.indexing.index_models import IndexReport
from backend.rag.loaders.document_loader import DocumentLoader
from backend.rag.vectorstore.chroma_store import ChromaStore


class Indexer:

    def __init__(self) -> None:
        self.loader = DocumentLoader()
        self.chunker = TextChunker()
        self.embedding = EmbeddingEngine()
        self.store = ChromaStore()
        self.registry = Registry()
        self.corpus = CorpusManager()
        logger.info("Knowledge Indexer initialized.")

    def _store_embeddings(self, embeddings: List[Any]) -> int:
        """Stores embedding vectors into ChromaStore, ensuring non-empty metadata."""
        if not embeddings:
            return 0

        ids = []
        vectors = []
        documents = []
        metadatas = []

        for emb in embeddings:
            chunk_id = str(uuid.uuid4())
            chunk_vector = []
            chunk_text = ""
            chunk_meta = {}

            if hasattr(emb, "id"):
                chunk_id = getattr(emb, "id", chunk_id)
                chunk_vector = getattr(emb, "vector", [])
                chunk_text = getattr(emb, "text", "")
                chunk_meta = getattr(emb, "metadata", {}) or {}
                # Also capture filename/source directly if present on EmbeddingVector
                if hasattr(emb, "filename") and getattr(emb, "filename"):
                    chunk_meta["filename"] = str(getattr(emb, "filename"))
                if hasattr(emb, "source") and getattr(emb, "source"):
                    chunk_meta["source"] = str(getattr(emb, "source"))
            elif isinstance(emb, dict):
                chunk_id = emb.get("id", chunk_id)
                chunk_vector = emb.get("vector", [])
                chunk_text = emb.get("text", "")
                chunk_meta = emb.get("metadata", {}) or {}

            # Ensure metadata is never an empty dict to satisfy ChromaDB requirements
            if not chunk_meta:
                chunk_meta = {"source": "knowledge_base", "indexed": True}

            ids.append(chunk_id)
            vectors.append(chunk_vector)
            documents.append(chunk_text)
            metadatas.append(chunk_meta)

        self.store.add_documents(
            ids=ids,
            embeddings=vectors,
            documents=documents,
            metadatas=metadatas,
        )

        return len(ids)

    def index_document(self, document: Dict[str, Any]) -> IndexReport:
        """Indexes a single document dictionary."""
        start = time.time()

        chunks = self.chunker.chunk_document(document)
        embeddings = self.embedding.embed_documents(chunks)
        vector_count = self._store_embeddings(embeddings)

        elapsed = time.time() - start
        report = IndexReport(
            documents=1,
            chunks=len(chunks),
            vectors=vector_count,
            elapsed_seconds=elapsed,
        )

        filename = document.get("filename", "unknown.txt")
        logger.success(f"Indexed {filename} ({vector_count} vectors)")
        return report

    def index_documents(self, documents: List[Dict[str, Any]]) -> IndexReport:
        """Indexes a list of document dictionaries."""
        start = time.time()

        total_chunks = 0
        total_vectors = 0
        indexed_documents = 0

        for document in documents:
            report = self.index_document(document)
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

        logger.success(f"Indexed {indexed_documents} documents ({total_vectors} vectors)")
        return report

    def index_corpus(self) -> IndexReport:
        """Performs incremental scan and index on corpus directory."""
        logger.info("Scanning knowledge corpus...")
        corpus_documents = self.corpus.scan() if hasattr(self.corpus, "scan") else []

        documents_to_index = []

        for corpus_doc in corpus_documents:
            checksum = getattr(corpus_doc, "checksum", "")
            if checksum and hasattr(self.registry, "contains") and self.registry.contains(checksum):
                title = getattr(corpus_doc, "title", "document")
                logger.debug(f"Skipping unchanged document: {title}")
                continue

            doc_path = getattr(corpus_doc, "path", None)
            if not doc_path:
                continue

            loaded = self.loader.load_file(doc_path) if hasattr(self.loader, "load_file") else None
            if loaded is None:
                continue

            documents_to_index.append((corpus_doc, loaded))

        if not documents_to_index:
            logger.success("Knowledge base already up to date.")
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
            report = self.index_document(loaded_doc)
            total_documents += report.documents
            total_chunks += report.chunks
            total_vectors += report.vectors

            if hasattr(self.registry, "update"):
                self.registry.update(corpus_doc)

        if hasattr(self.registry, "save"):
            self.registry.save()

        elapsed = time.time() - start
        logger.success(f"Incremental indexing complete. {total_documents} new documents.")

        return IndexReport(
            documents=total_documents,
            chunks=total_chunks,
            vectors=total_vectors,
            elapsed_seconds=elapsed,
        )

    def index_directory(
        self,
        directory: Union[str, Path],
        clear_existing: bool = False,
    ) -> IndexReport:
        if clear_existing:
            self.clear()

        documents = self.loader.load_directory(directory) if hasattr(self.loader, "load_directory") else []
        return self.index_documents(documents)

    def stats(self) -> Dict[str, Any]:
        count_val = self.store.count()
        reg_docs = len(self.registry.all()) if hasattr(self.registry, "all") else 0
        return {
            "indexed_vectors": count_val,
            "registry_documents": reg_docs,
        }

    def count(self) -> int:
        return self.store.count()

    def clear(self) -> None:
        if hasattr(self.store, "clear"):
            self.store.clear()
        if hasattr(self.registry, "clear"):
            self.registry.clear()
        logger.warning("Knowledge index cleared.")