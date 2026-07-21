"""
Knowledge Retriever for Digital Twin RAG Pipeline.
"""

from typing import List, Any, Dict, Optional
from backend.core.logger import logger


class Retriever:
    """Retrieves relevant knowledge base passages for prompt grounding."""

    def __init__(self, vectorstore: Any, embedding_engine: Any) -> None:
        self.vectorstore = vectorstore
        self.embedding_engine = embedding_engine
        logger.info("Knowledge Retriever initialized.")

    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        """
        Embeds query and searches ChromaStore, returning plain document text strings.
        """
        logger.info(f"Searching knowledge base for query: '{query}'")
        
        try:
            query_vector = self.embedding_engine.embed_query(query)
            if not query_vector:
                logger.warning("Query embedding returned empty vector.")
                return []

            raw_results = self.vectorstore.search(
                query_embedding=query_vector,
                top_k=top_k,
            )

            documents: List[str] = []

            if isinstance(raw_results, dict) and "documents" in raw_results:
                docs = raw_results.get("documents", [])
                if docs and isinstance(docs, list):
                    first_elem = docs[0]
                    if isinstance(first_elem, list):
                        documents = [str(doc) for doc in first_elem if doc]
                    else:
                        documents = [str(doc) for doc in docs if doc]
            elif isinstance(raw_results, list):
                for item in raw_results:
                    if isinstance(item, str):
                        documents.append(item)
                    elif hasattr(item, "page_content"):
                        documents.append(str(item.page_content))
                    elif hasattr(item, "document"):
                        documents.append(str(item.document))

            return documents[:top_k]

        except Exception as e:
            logger.warning(f"RAG retrieval encountered an error (continuing without RAG context): {e}")
            return []