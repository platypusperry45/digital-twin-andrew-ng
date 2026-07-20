"""
PDF parser using PyMuPDF.
"""

from pathlib import Path

import fitz

from backend.rag.parsers.base_parser import BaseParser


class PDFParser(BaseParser):

    def parse(
        self,
        path: Path,
    ) -> str:

        document = fitz.open(path)

        pages = []

        for page in document:

            pages.append(
                page.get_text()
            )

        document.close()

        return "\n".join(pages)