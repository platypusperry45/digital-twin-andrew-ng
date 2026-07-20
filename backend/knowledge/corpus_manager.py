"""
Corpus Manager.

Responsible for:

- Initializing the knowledge corpus
- Creating folder structure
- Scanning documents
- Creating registry
- Returning corpus documents
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from backend.core.logger import logger

from backend.knowledge.models import (
    CorpusDocument,
)


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".md",
    ".docx",
}


class CorpusManager:

    def __init__(self):

        self.data_root = (
            Path(__file__).resolve().parent.parent
            / "data"
        )

        self.knowledge_root = (
            self.data_root
            / "knowledge"
            / "AndrewNg"
        )

        self.structure = [
            "Courses",
            "Interviews",
            "Talks",
            "Blog",
            "Newsletters",
            "Research Papers",
            "Books",
            "FAQs",
            "Career Advice",
            "Quotes",
            "Misc",
        ]

    def initialize(self) -> None:
        """
        Create corpus directory structure.
        """

        self.knowledge_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        for folder in self.structure:

            (
                self.knowledge_root / folder
            ).mkdir(
                parents=True,
                exist_ok=True,
            )

        logger.success(
            "Knowledge corpus initialized."
        )

    def scan(self) -> list[CorpusDocument]:
        """
        Scan the knowledge corpus and return all supported documents.
        """

        documents: list[
            CorpusDocument
        ] = []

        for path in self.knowledge_root.rglob("*"):

            if (
                not path.is_file()
                or path.suffix.lower()
                not in SUPPORTED_EXTENSIONS
            ):
                continue

            documents.append(
                self._build_document(path)
            )

        logger.info(
            f"Discovered {len(documents)} corpus documents."
        )

        return documents

    def _build_document(
        self,
        path: Path,
    ) -> CorpusDocument:

        relative = path.relative_to(
            self.knowledge_root
        )

        checksum = self._checksum(path)

        return CorpusDocument(

            id=checksum[:16],

            title=path.stem,

            path=path,

            category=relative.parts[0],

            source=str(relative),

            extension=path.suffix.lower(),

            checksum=checksum,

        )

    @staticmethod
    def _checksum(
        path: Path,
    ) -> str:

        hasher = hashlib.sha256()

        with open(path, "rb") as file:

            while True:

                chunk = file.read(8192)

                if not chunk:
                    break

                hasher.update(chunk)

        return hasher.hexdigest()