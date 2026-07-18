"""
Document Loader.

Loads knowledge documents for the RAG pipeline.

Supported formats:
- PDF
- TXT
- Markdown

Returns clean text documents that can later
be chunked and embedded.
"""

from pathlib import Path

from pypdf import PdfReader

from backend.core.logger import logger


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".md",
}


class DocumentLoader:

    def __init__(self):

        logger.info("Document Loader initialized.")

    def load_directory(
        self,
        directory: str | Path,
    ) -> list[dict]:

        directory = Path(directory)

        if not directory.exists():

            raise FileNotFoundError(
                f"{directory} does not exist."
            )

        documents = []

        for file in directory.rglob("*"):

            if (
                file.is_file()
                and file.suffix.lower()
                in SUPPORTED_EXTENSIONS
            ):

                try:

                    document = self.load_file(file)

                    if document:

                        documents.append(document)

                except Exception as exc:

                    logger.exception(
                        f"Failed loading {file}: {exc}"
                    )

        logger.success(
            f"Loaded {len(documents)} documents."
        )

        return documents

    def load_file(
        self,
        file: str | Path,
    ) -> dict | None:

        file = Path(file)

        suffix = file.suffix.lower()

        if suffix == ".pdf":

            text = self._load_pdf(file)

        elif suffix in {".txt", ".md"}:

            text = self._load_text(file)

        else:

            return None

        text = self._clean(text)

        if not text:

            return None

        return {

            "source": str(file),

            "filename": file.name,

            "text": text,

        }

    def _load_pdf(
        self,
        file: Path,
    ) -> str:

        reader = PdfReader(file)

        pages = []

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                pages.append(page_text)

        return "\n".join(pages)

    def _load_text(
        self,
        file: Path,
    ) -> str:

        return file.read_text(
            encoding="utf-8",
            errors="ignore",
        )

    def _clean(
        self,
        text: str,
    ) -> str:

        lines = []

        for line in text.splitlines():

            line = line.strip()

            if line:

                lines.append(line)

        return "\n".join(lines)