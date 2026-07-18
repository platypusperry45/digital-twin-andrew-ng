"""
Text Chunker.

Splits long documents into overlapping chunks for
embedding and retrieval.
"""

from backend.core.logger import logger


class TextChunker:

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 100,
    ):

        self.chunk_size = chunk_size
        self.overlap = overlap

        logger.info(
            "Text Chunker initialized."
        )

    def chunk_document(
        self,
        document: dict,
    ) -> list[dict]:

        text = document["text"]

        chunks = []

        start = 0

        while start < len(text):

            end = start + self.chunk_size

            chunk = text[start:end]

            chunks.append(

                {

                    "source": document["source"],

                    "filename": document["filename"],

                    "text": chunk,

                }

            )

            start += (
                self.chunk_size
                - self.overlap
            )

        logger.debug(
            f"{document['filename']} -> "
            f"{len(chunks)} chunks"
        )

        return chunks

    def chunk_documents(
        self,
        documents: list[dict],
    ) -> list[dict]:

        all_chunks = []

        for document in documents:

            all_chunks.extend(

                self.chunk_document(
                    document
                )

            )

        logger.success(
            f"Created {len(all_chunks)} chunks."
        )

        return all_chunks