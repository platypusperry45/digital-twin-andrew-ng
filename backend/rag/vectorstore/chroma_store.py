"""
Thread-safe persistent ChromaDB vector store manager.
"""

from __future__ import annotations

import os
import threading
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.config import Settings as ChromaSettings

from backend.core.config import settings
from backend.core.logger import logger


_CLIENT_CACHE: Dict[str, chromadb.PersistentClient] = {}
_CLIENT_LOCK = threading.Lock()


def get_chroma_client(db_path: str) -> chromadb.PersistentClient:
    """
    Returns a cached Chroma PersistentClient instance for the given directory path.
    """
    abs_path = os.path.abspath(db_path)
    os.makedirs(abs_path, exist_ok=True)

    with _CLIENT_LOCK:
        if abs_path not in _CLIENT_CACHE:
            logger.info(f"Creating shared ChromaDB PersistentClient at path: {abs_path}")
            _CLIENT_CACHE[abs_path] = chromadb.PersistentClient(
                path=abs_path,
                settings=ChromaSettings(
                    allow_reset=True,
                    anonymized_telemetry=False,
                    is_persistent=True,
                )
            )
        return _CLIENT_CACHE[abs_path]


class ChromaStore:
    """
    High-level vector collection interface for RAG index and memory storage.
    """

    def __init__(self, collection_name: str = "knowledge_base", db_path: Optional[str] = None) -> None:
        self.db_path = db_path or getattr(settings, "CHROMA_DB_PATH", "backend/data/vectorstore")
        self.collection_name = collection_name
        self.client = get_chroma_client(self.db_path)
        self.collection = self.client.get_or_create_collection(name=self.collection_name)
        logger.info(f"ChromaStore initialized for collection '{self.collection_name}'.")

    def add_documents(
        self,
        ids: List[str],
        embeddings: List[List[float]],
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """Upserts vectorized documents into the collection."""
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

    def query(
        self,
        query_embedding: Optional[List[float]] = None,
        embedding: Optional[List[float]] = None,
        top_k: int = 5,
        where: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Queries nearest neighbors from the collection."""
        target_vec = query_embedding or embedding
        if target_vec is None:
            raise ValueError("Must provide either query_embedding or embedding vector.")

        return self.collection.query(
            query_embeddings=[target_vec],
            n_results=top_k,
            where=where,
        )

    def search(
        self,
        query_embedding: Optional[List[float]] = None,
        embedding: Optional[List[float]] = None,
        top_k: int = 5,
        where: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Flexible search interface wrapping query execution."""
        return self.query(
            query_embedding=query_embedding,
            embedding=embedding,
            top_k=top_k,
            where=where,
            **kwargs,
        )

    def count(self) -> int:
        """Returns the total number of items stored in the collection."""
        return self.collection.count()