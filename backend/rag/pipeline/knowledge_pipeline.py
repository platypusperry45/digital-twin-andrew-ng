"""
Knowledge Pipeline.

Responsible for building the knowledge base.

Flow:

Documents
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Store
"""

from backend.core.logger import logger

from backend.rag.loaders.document_loader import DocumentLoader
from backend.rag.chunking.text_chunker import TextChunker
from backend.rag.embeddings.embedding_engine import EmbeddingEngine
from backend.rag.vectorstore.chroma_store import ChromaStore


class KnowledgePipeline:

    def __init__(self):

        self.loader = DocumentLoader()

        self.chunker = TextChunker()

        self.embedding = EmbeddingEngine()

        self.store = ChromaStore()

        logger.info(
            "Knowledge Pipeline initialized."
        )

    def initialize(self):

        logger.info(
            "Initializing Knowledge Base..."
        )

        documents = self.loader.load_directory()

        if not documents:

            logger.warning(
                "No knowledge documents found."
            )

            return

        chunks = self.chunker.chunk_documents(
            documents
        )

        if not chunks:

            logger.warning(
                "No chunks created."
            )

            return

        vectors = self.embedding.embed_documents(
            chunks
        )

        if not vectors:

            logger.warning(
                "No vectors generated."
            )

            return

        self.store.clear()

        self.store.add_many(
            vectors
        )

        logger.success(
            f"Knowledge Base Ready ({len(vectors)} vectors)."
        )

    def rebuild(self):

        logger.info(
            "Rebuilding knowledge base..."
        )

        self.initialize()

    def clear(self):

        self.store.clear()

        logger.warning(
            "Knowledge Base cleared."
        )