"""
Conversation Service.

Central orchestrator for all chat requests.

Flow:
User
 ↓
ConversationService
 ↓
Memory
 ↓
Prompt Builder
 ↓
RAG
 ↓
Gemini
 ↓
Save Memory
 ↓
Return Response
"""

from backend.core.logger import logger

from backend.llm.gemini_client import GeminiClient
from backend.llm.models import (
    LLMRequest,
    LLMResponse,
)


class ConversationService:

    def __init__(self):

        self.llm = GeminiClient()

        logger.info(
            "Conversation Service initialized."
        )

    def chat(
        self,
        prompt: str,
        model: str | None = None,
    ) -> LLMResponse:

        logger.info(
            "New conversation request received."
        )

        #
        # Future:
        # memory
        # rag
        # prompt builder
        #

        request = LLMRequest(
            prompt=prompt,
            model=model,
        )

        response = self.llm.generate(request)

        logger.success(
            "Conversation completed."
        )

        return response