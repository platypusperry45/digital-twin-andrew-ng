"""
Knowledge Registry.

Tracks every document imported into the knowledge corpus.

Responsibilities

- Persist registry
- Detect duplicates
- Detect updated documents
- Track indexing status
"""

from __future__ import annotations

import json
from pathlib import Path

from backend.core.logger import logger

from backend.knowledge.models import (
    CorpusDocument,
    CorpusRegistry,
)


class Registry:

    def __init__(self):

        self.registry_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "knowledge"
            / "registry.json"
        )

        self.registry = self._load()

    def _load(
        self,
    ) -> CorpusRegistry:

        if not self.registry_path.exists():

            logger.info(
                "Knowledge registry not found. Creating new registry."
            )

            return CorpusRegistry()

        with open(
            self.registry_path,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        logger.info(
            "Knowledge registry loaded."
        )

        return CorpusRegistry.model_validate(data)

    def save(self) -> None:

        self.registry_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            self.registry_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self.registry.model_dump(
                    mode="json"
                ),
                file,
                indent=4,
            )

        logger.success(
            "Knowledge registry saved."
        )

    def contains(
        self,
        checksum: str,
    ) -> bool:

        return any(

            document.checksum == checksum

            for document in self.registry.documents

        )

    def get(
        self,
        checksum: str,
    ) -> CorpusDocument | None:

        for document in self.registry.documents:

            if document.checksum == checksum:

                return document

        return None

    def add(
        self,
        document: CorpusDocument,
    ) -> None:

        if self.contains(
            document.checksum
        ):

            return

        self.registry.documents.append(
            document
        )

        logger.info(
            f"Registered: {document.title}"
        )

    def update(
        self,
        document: CorpusDocument,
    ) -> None:

        for index, existing in enumerate(
            self.registry.documents
        ):

            if (
                existing.checksum
                == document.checksum
            ):

                self.registry.documents[
                    index
                ] = document

                return

        self.registry.documents.append(
            document
        )

    def all(
        self,
    ) -> list[CorpusDocument]:

        return self.registry.documents

    def clear(
        self,
    ) -> None:

        self.registry.documents.clear()

        self.save()

        logger.warning(
            "Knowledge registry cleared."
        )