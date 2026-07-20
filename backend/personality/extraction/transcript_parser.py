"""
Transcript Parser.

Converts raw documents into a normalized transcript
for downstream personality extraction.
"""

from __future__ import annotations

from pathlib import Path

from backend.core.logger import logger

from backend.personality.extraction.extraction_models import (
    Transcript,
)


class TranscriptParser:

    def parse(
        self,
        path: Path,
        text: str,
    ) -> Transcript:
        """
        Convert extracted document text into a transcript.
        """

        transcript = Transcript(

            source=str(path),

            title=path.stem,

            text=text.strip(),

        )

        logger.info(
            f"Transcript parsed: {transcript.title}"
        )

        return transcript