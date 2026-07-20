"""
Markdown parser.
"""

from pathlib import Path

from backend.rag.parsers.base_parser import BaseParser


class MarkdownParser(BaseParser):

    def parse(
        self,
        path: Path,
    ) -> str:

        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )