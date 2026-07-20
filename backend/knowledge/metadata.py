"""
Knowledge Metadata Extractor.

Extracts metadata from corpus documents.
"""

from __future__ import annotations

from pathlib import Path

from backend.core.logger import logger

from backend.knowledge.models import (
    CorpusDocument,
)


class MetadataExtractor:
    """
    Extract metadata from a corpus document.

    Future versions can extract:
    - PDF metadata
    - DOCX metadata
    - Markdown frontmatter
    - Transcript information
    """

    def extract(
        self,
        document: CorpusDocument,
    ) -> CorpusDocument:

        path = Path(document.path)

        # ------------------------------------
        # Category
        # ------------------------------------

        try:

            category = path.relative_to(
                path.parents[1]
            ).parts[0]

        except Exception:

            category = document.category

        document.category = category

        # ------------------------------------
        # Extension
        # ------------------------------------

        document.extension = (
            path.suffix.lower()
        )

        # ------------------------------------
        # Title
        # ------------------------------------

        document.title = path.stem.replace(
            "_",
            " ",
        )

        # ------------------------------------
        # Source
        # ------------------------------------

        document.source = str(path)

        # ------------------------------------
        # Automatic Tags
        # ------------------------------------

        tags = set(document.tags)

        tags.add(category.lower())

        filename = document.title.lower()

        if "course" in filename:
            tags.add("course")

        if "lecture" in filename:
            tags.add("lecture")

        if "interview" in filename:
            tags.add("interview")

        if "podcast" in filename:
            tags.add("podcast")

        if "blog" in filename:
            tags.add("blog")

        if "research" in filename:
            tags.add("research")

        if "paper" in filename:
            tags.add("paper")

        document.tags = sorted(tags)

        logger.info(
            f"Metadata extracted: {document.title}"
        )

        return document