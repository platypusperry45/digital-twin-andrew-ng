"""
Knowledge Pipeline for managing vector store synchronization and corpus maintenance.
"""

from __future__ import annotations

from backend.core.logger import logger
from backend.knowledge.corpus_manager import CorpusManager
from backend.knowledge.registry import Registry
from backend.rag.indexing.indexer import Indexer


class KnowledgePipeline:
    """
    Production Knowledge Pipeline orchestrating corpus loading and indexing.
    """

    def __init__(self) -> None:
        self.corpus = CorpusManager()
        self.registry = Registry()
        self.indexer = Indexer()
        logger.info("Knowledge Pipeline initialized.")

    def initialize(self):
        """Initializes corpus folders and indexes missing documents."""
        logger.info("Initializing Knowledge Base...")
        try:
            self.corpus.initialize()
            report = self.indexer.index_corpus()

            logger.success(
                f"Knowledge Base Ready | "
                f"Documents: {getattr(report, 'documents', 0)} | "
                f"Chunks: {getattr(report, 'chunks', 0)} | "
                f"Vectors: {getattr(report, 'vectors', 0)}"
            )
            return report
        except Exception as e:
            logger.warning(f"Knowledge Pipeline initialization encountered a non-fatal warning: {e}")
            return None

    def rebuild(self):
        """Performs complete knowledge base re-indexing."""
        logger.warning("Performing complete knowledge rebuild...")
        self.clear()
        self.registry.clear()
        report = self.indexer.index_corpus()
        logger.success("Knowledge Base rebuilt successfully.")
        return report

    def refresh(self):
        """Scans for newly added or modified documents."""
        logger.info("Refreshing knowledge base...")
        return self.indexer.index_corpus()

    def stats(self):
        return self.indexer.stats()

    def count(self):
        return self.indexer.count()

    def clear(self):
        logger.warning("Clearing knowledge base...")
        self.indexer.clear()
        logger.warning("Knowledge base cleared.")