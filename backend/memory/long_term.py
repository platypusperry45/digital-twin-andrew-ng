"""
Long-term memory using ChromaDB.

Responsibilities
----------------
- Store memories
- Retrieve memories
- Delete memories
- Persistent storage
"""

from typing import List
from uuid import uuid4

import chromadb

from backend.core.config import settings
from backend.core.logger import logger

from backend.memory.embeddings import EmbeddingService
from backend.memory.models import (
    MemoryItem,
    MemorySearchResult,
)


class LongTermMemory:

    def __init__(self):

        self.embedding_service = EmbeddingService()

        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_DB_PATH
        )

        self.collection = self.client.get_or_create_collection(
            name="digital_twin_memory"
        )

    def add(
        self,
        role: str,
        content: str,
        metadata: dict | None = None,
    ) -> str:
        """
        Store a memory.
        """

        if metadata is None:
            metadata = {}

        embedding = self.embedding_service.embed(content)

        memory_id = str(uuid4())

        self.collection.add(
            ids=[memory_id],
            embeddings=[embedding],
            documents=[content],
            metadatas=[
                {
                    "role": role,
                    **metadata,
                }
            ],
        )

        logger.info(
            f"Stored memory {memory_id}"
        )

        return memory_id

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[MemorySearchResult]:
        """
        Semantic search.
        """

        embedding = self.embedding_service.embed(query)

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )

        memories = []

        ids = results["ids"][0]
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        distances = results["distances"][0]

        for idx in range(len(ids)):

            memory = MemoryItem(
                id=ids[idx],
                role=metas[idx]["role"],
                content=docs[idx],
                metadata=metas[idx],
            )

            memories.append(

                MemorySearchResult(
                    memory=memory,
                    score=1 - distances[idx],
                )

            )

        return memories

    def delete(
        self,
        memory_id: str,
    ):

        self.collection.delete(
            ids=[memory_id]
        )

    def clear(self):

        self.client.delete_collection(
            "digital_twin_memory"
        )

        self.collection = (
            self.client.get_or_create_collection(
                "digital_twin_memory"
            )
        )

    def count(self):

        return self.collection.count()