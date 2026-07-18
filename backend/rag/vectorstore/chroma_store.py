"""
Persistent ChromaDB Vector Store.
"""

from pathlib import Path

import chromadb
from chromadb.config import Settings

from backend.core.config import settings
from backend.core.logger import logger

from backend.rag.vectorstore.vector_models import (
    RetrievedVector,
    StoredVector,
)


class ChromaStore:

    def __init__(self):

        db_path = Path(
            settings.CHROMA_DB_PATH
        )

        db_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.client = (
            chromadb.PersistentClient(
                path=str(db_path),
                settings=Settings(
                    anonymized_telemetry=False,
                ),
            )
        )

        self.collection = (
            self.client.get_or_create_collection(
                name="knowledge_base",
                metadata={
                    "description":
                    "Andrew Ng Knowledge Base",
                },
            )
        )

        logger.info(
            "Chroma Vector Store initialized."
        )

    def add(
        self,
        vector: StoredVector,
    ):

        self.collection.add(

            ids=[vector.id],

            embeddings=[vector.vector],

            documents=[vector.text],

            metadatas=[

                {

                    "source":
                        vector.source,

                    "filename":
                        vector.filename,

                    **vector.metadata,

                }

            ],

        )

    def add_many(
        self,
        vectors: list[StoredVector],
    ):

        if not vectors:
            return

        ids = []

        embeddings = []

        documents = []

        metadatas = []

        for item in vectors:

            ids.append(item.id)

            embeddings.append(item.vector)

            documents.append(item.text)

            metadatas.append(

                {

                    "source":
                        item.source,

                    "filename":
                        item.filename,

                    **item.metadata,

                }

            )

        self.collection.add(

            ids=ids,

            embeddings=embeddings,

            documents=documents,

            metadatas=metadatas,

        )

        logger.success(
            f"Stored {len(vectors)} vectors."
        )

    def search(
        self,
        embedding: list[float],
        top_k: int = 5,
    ) -> list[RetrievedVector]:

        results = self.collection.query(

            query_embeddings=[embedding],

            n_results=top_k,

        )

        retrieved = []

        ids = results["ids"][0]

        docs = results["documents"][0]

        metas = results["metadatas"][0]

        distances = results["distances"][0]

        for idx in range(len(ids)):

            meta = metas[idx] or {}

            retrieved.append(

                RetrievedVector(

                    id=ids[idx],

                    score=1 - distances[idx],

                    text=docs[idx],

                    source=meta.get(
                        "source",
                        "",
                    ),

                    filename=meta.get(
                        "filename",
                        "",
                    ),

                    metadata=meta,

                )

            )

        logger.info(
            f"Retrieved {len(retrieved)} vectors."
        )

        return retrieved

    def delete(
        self,
        vector_id: str,
    ):

        self.collection.delete(
            ids=[vector_id],
        )

        logger.info(
            f"Deleted vector {vector_id}"
        )

    def clear(self):

        ids = self.collection.get()["ids"]

        if ids:

            self.collection.delete(
                ids=ids,
            )

        logger.warning(
            "Vector store cleared."
        )

    def count(self) -> int:

        return self.collection.count()

    def stats(self):

        return {

            "collection":
                self.collection.name,

            "vectors":
                self.collection.count(),

        }