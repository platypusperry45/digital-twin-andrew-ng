"""
Gemini Embedding Service.

Responsibilities
----------------
- Generate embeddings using Gemini
- Normalize API responses
- Hide SDK implementation
"""

from typing import List

from google import genai

from backend.core.config import settings
from backend.core.logger import logger


class EmbeddingService:

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEYS[0]
        )

        self.model = settings.EMBEDDING_MODEL

    def embed(
        self,
        text: str,
    ) -> List[float]:
        """
        Generate embedding for one text.
        """

        try:

            response = self.client.models.embed_content(
                model=self.model,
                contents=text,
            )

            return response.embeddings[0].values

        except Exception as exc:

            logger.exception(
                "Embedding generation failed."
            )

            raise RuntimeError(
                f"Embedding failed: {exc}"
            )

    def embed_batch(
        self,
        texts: List[str],
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        """

        embeddings = []

        for text in texts:
            embeddings.append(
                self.embed(text)
            )

        return embeddings