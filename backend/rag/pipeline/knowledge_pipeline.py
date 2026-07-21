"""
Knowledge Pipeline.

Responsible for maintaining the knowledge base.

Features
--------
- Incremental indexing
- Full rebuild
- Automatic corpus initialization
- Registry synchronization
"""

from __future__ import annotations

from backend.core.logger import logger

from backend.knowledge.corpus_manager import CorpusManager
from backend.knowledge.registry import Registry

from backend.rag.indexing.indexer import Indexer


class KnowledgePipeline:
    """
    Production knowledge pipeline.

    Startup Flow

    Initialize corpus folders
            ↓
    Scan knowledge directory
            ↓
    Compare against registry
            ↓
    Index only new/changed files
            ↓
    Save registry
    """

    def __init__(self):

        self.corpus = CorpusManager()

        self.registry = Registry()

        self.indexer = Indexer()

        logger.info(
            "Knowledge Pipeline initialized."
        )

    # =====================================================
    # Startup
    # =====================================================

    def initialize(self):

        logger.info(
            "Initializing Knowledge Base..."
        )

        # Ensure directory structure exists
        self.corpus.initialize()

        report = self.indexer.index_corpus()

        logger.success(

            "Knowledge Base Ready | "

            f"Documents Indexed: {report.documents} | "

            f"Chunks: {report.chunks} | "

            f"Vectors: {report.vectors}"

        )

        return report

    # =====================================================
    # Full Rebuild
    # =====================================================

    def rebuild(self):

        logger.warning(
            "Performing complete knowledge rebuild..."
        )

        self.clear()

        self.registry.clear()

        report = self.indexer.index_corpus()

        logger.success(
            "Knowledge Base rebuilt successfully."
        )

        return report

    # =====================================================
    # Refresh
    # =====================================================

    def refresh(self):
        """
        Scan for newly added or modified documents.

        Existing indexed documents are skipped.
        """

        logger.info(
            "Refreshing knowledge base..."
        )

        return self.indexer.index_corpus()

    # =====================================================
    # Utilities
    # =====================================================

    def stats(self):

        return self.indexer.stats()

    def count(self):

        return self.indexer.count()

    def clear(self):

        logger.warning(
            "Clearing knowledge base..."
        )

        self.indexer.clear()

        logger.warning(
            "Knowledge base cleared."
        )