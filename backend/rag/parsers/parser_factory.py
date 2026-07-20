"""
Parser Factory.

Returns the appropriate parser for a document.
"""

from pathlib import Path

from backend.rag.parsers.base_parser import BaseParser
from backend.rag.parsers.docx_parser import DOCXParser
from backend.rag.parsers.markdown_parser import MarkdownParser
from backend.rag.parsers.pdf_parser import PDFParser
from backend.rag.parsers.txt_parser import TXTParser


class ParserFactory:

    _parsers = {

        ".txt": TXTParser,

        ".md": MarkdownParser,

        ".pdf": PDFParser,

        ".docx": DOCXParser,

    }

    @classmethod
    def create(
        cls,
        path: Path,
    ) -> BaseParser:

        extension = path.suffix.lower()

        parser = cls._parsers.get(
            extension
        )

        if parser is None:

            raise ValueError(
                f"No parser for {extension}"
            )

        return parser()