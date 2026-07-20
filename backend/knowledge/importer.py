"""
Knowledge Importer.

Coordinates the complete knowledge ingestion pipeline.

Pipeline

Corpus
    ↓
Metadata
    ↓
Validation
    ↓
Parsing
    ↓
Indexing
    ↓
Registry
"""

from __future__ import annotations

from backend.core.logger import logger

from backend.knowledge.corpus_manager import CorpusManager
from backend.knowledge.metadata import MetadataExtractor
from backend.knowledge.registry import Registry
from backend.knowledge.validator import (
    KnowledgeValidator,
    ValidationError,
)

from backend.rag.indexing import Indexer
from backend.rag.parsers.parser_factory import ParserFactory


class KnowledgeImporter:

    def __init__(self):

        self.corpus = CorpusManager()

        self.metadata = MetadataExtractor()

        self.validator = KnowledgeValidator()

        self.registry = Registry()

        self.indexer = Indexer()

        logger.info(
            "Knowledge Importer initialized."
        )

    def import_corpus(
        self,
        clear_existing: bool = False,
        skip_existing: bool = True,
    ) -> dict:

        logger.info(
            "Starting knowledge import..."
        )

        if clear_existing:

            self.indexer.clear()

            self.registry.clear()

        documents = self.corpus.scan()

        imported = 0

        skipped = 0

        failed = 0

        for document in documents:

            try:

                # -------------------------
                # Metadata
                # -------------------------

                document = self.metadata.extract(
                    document
                )

                # -------------------------
                # Validation
                # -------------------------

                self.validator.validate(
                    document
                )

                # -------------------------
                # Duplicate detection
                # -------------------------

                existing = self.registry.get(
                    document.checksum
                )

                if (
                    existing is not None
                    and skip_existing
                ):

                    logger.info(
                        f"Skipping existing: {document.title}"
                    )

                    skipped += 1

                    continue

                # -------------------------
                # Parse document
                # -------------------------

                parser = (
                    ParserFactory.create(
                        document.path
                    )
                )

                text = parser.parse(
                    document.path
                )

                if not text.strip():

                    logger.warning(
                        f"Empty document: {document.title}"
                    )

                    skipped += 1

                    continue

                # -------------------------
                # Index
                # -------------------------

                self.indexer.index_document(

                    {

                        "text": text,

                        "filename": document.title,

                        "source": str(
                            document.path
                        ),

                        "metadata": {

                            "category":
                                document.category,

                            "tags":
                                document.tags,

                            "checksum":
                                document.checksum,

                            "extension":
                                document.extension,

                        },

                    }

                )

                # -------------------------
                # Registry
                # -------------------------

                self.registry.update(
                    document
                )

                imported += 1

                logger.success(
                    f"Imported: {document.title}"
                )

            except ValidationError as exc:

                failed += 1

                logger.warning(
                    f"{document.title}: {exc}"
                )

            except Exception as exc:

                failed += 1

                logger.exception(exc)

        self.registry.save()

        report = {

            "documents": len(documents),

            "imported": imported,

            "skipped": skipped,

            "failed": failed,

            "vectors": self.indexer.count(),

        }

        logger.success(

            f"Knowledge import complete."

        )

        logger.info(report)

        return report