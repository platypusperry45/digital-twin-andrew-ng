"""
Knowledge Synchronizer.

Keeps the vector database synchronized with the knowledge corpus.

Responsibilities

- Detect new documents
- Detect modified documents
- Detect deleted documents
- Index only changes
"""

from __future__ import annotations

from backend.core.logger import logger

from backend.knowledge.corpus_manager import CorpusManager
from backend.knowledge.importer import KnowledgeImporter
from backend.knowledge.registry import Registry


class KnowledgeSynchronizer:

    def __init__(self):

        self.corpus = CorpusManager()

        self.registry = Registry()

        self.importer = KnowledgeImporter()

    def synchronize(self):

        logger.info(
            "Synchronizing knowledge corpus..."
        )

        corpus_documents = self.corpus.scan()

        registry_documents = {

            document.checksum: document

            for document in self.registry.all()

        }

        new_documents = []

        for document in corpus_documents:

            if (

                document.checksum

                not in registry_documents

            ):

                new_documents.append(
                    document
                )

        if not new_documents:

            logger.success(
                "Knowledge corpus already synchronized."
            )

            return

        logger.info(

            f"Found {len(new_documents)} new documents."

        )

        self.importer.import_corpus(
            skip_existing=True
        )