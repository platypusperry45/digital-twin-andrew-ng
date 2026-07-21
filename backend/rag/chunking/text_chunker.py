"""
Text Chunker.

Splits long documents into overlapping chunks for embedding and retrieval.
"""

from typing import List, Dict, Any
from backend.core.logger import logger


class TextChunker:

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 100,
    ) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap
        logger.info("Text Chunker initialized.")

    def chunk_document(self, document: Dict[str, Any]) -> List[Dict[str, Any]]:
        text = document.get("text", "")
        source = document.get("source", "unknown")
        filename = document.get("filename", "document.txt")

        chunks: List[Dict[str, Any]] = []
        if not text:
            return chunks

        start = 0
        text_length = len(text)
        step = max(1, self.chunk_size - self.overlap)

        while start < text_length:
            end = min(start + self.chunk_size, text_length)
            chunk = text[start:end]

            chunks.append({
                "source": source,
                "filename": filename,
                "text": chunk,
            })

            start += step

        logger.debug(f"{filename} -> {len(chunks)} chunks")
        return chunks

    def chunk_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        all_chunks: List[Dict[str, Any]] = []
        for document in documents:
            all_chunks.extend(self.chunk_document(document))

        logger.success(f"Created {len(all_chunks)} total chunks.")
        return all_chunks