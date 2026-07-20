"""
Knowledge Validator.

Validates corpus documents before ingestion.
"""

from __future__ import annotations

from pathlib import Path

from backend.core.logger import logger

from backend.knowledge.models import (
    CorpusDocument,
)


class ValidationError(Exception):
    """
    Raised when a corpus document fails validation.
    """
    pass


class KnowledgeValidator:

    SUPPORTED_EXTENSIONS = {
        ".pdf",
        ".txt",
        ".md",
        ".docx",
    }

    MAX_FILE_SIZE_MB = 100

    def validate(
        self,
        document: CorpusDocument,
    ) -> bool:
        """
        Validate a corpus document.

        Raises:
            ValidationError
        """

        self._exists(document)

        self._extension(document)

        self._size(document)

        self._metadata(document)

        logger.info(
            f"Validated: {document.title}"
        )

        return True

    def _exists(
        self,
        document: CorpusDocument,
    ) -> None:

        if not Path(document.path).exists():

            raise ValidationError(
                f"Missing file: {document.path}"
            )

    def _extension(
        self,
        document: CorpusDocument,
    ) -> None:

        if (
            document.extension.lower()
            not in self.SUPPORTED_EXTENSIONS
        ):

            raise ValidationError(
                f"Unsupported file type: {document.extension}"
            )

    def _size(
        self,
        document: CorpusDocument,
    ) -> None:

        size_mb = (
            Path(document.path)
            .stat()
            .st_size
            / (1024 * 1024)
        )

        if size_mb == 0:

            raise ValidationError(
                f"Empty file: {document.title}"
            )

        if size_mb > self.MAX_FILE_SIZE_MB:

            raise ValidationError(
                f"File too large ({size_mb:.2f} MB): {document.title}"
            )

    def _metadata(
        self,
        document: CorpusDocument,
    ) -> None:

        if not document.id:

            raise ValidationError(
                "Missing document id."
            )

        if not document.title:

            raise ValidationError(
                "Missing title."
            )

        if not document.category:

            raise ValidationError(
                "Missing category."
            )

        if not document.checksum:

            raise ValidationError(
                "Missing checksum."
            )

        if not document.source:

            raise ValidationError(
                "Missing source."
            )