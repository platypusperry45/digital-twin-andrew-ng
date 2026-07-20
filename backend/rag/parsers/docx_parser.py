"""
DOCX parser.
"""

from pathlib import Path

from docx import Document

from backend.rag.parsers.base_parser import BaseParser


class DOCXParser(BaseParser):

    def parse(
        self,
        path: Path,
    ) -> str:

        document = Document(path)

        return "\n".join(

            paragraph.text

            for paragraph in document.paragraphs

        )