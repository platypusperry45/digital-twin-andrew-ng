"""
Conversation summarizer.

Compresses old conversations into concise summaries
to reduce context size while preserving information.
"""

from backend.core.logger import logger

from backend.llm.gemini_client import GeminiClient
from backend.llm.models import (
    LLMRequest,
)


class ConversationSummarizer:

    def __init__(self):

        self.client = GeminiClient()

    def summarize(
        self,
        conversation: str,
    ) -> str:
        """
        Generate a concise summary of a conversation.
        """

        prompt = f"""
You are a memory compression system.

Summarize the following conversation.

Rules:
- Keep important facts.
- Keep names.
- Keep preferences.
- Keep decisions.
- Remove small talk.
- Maximum 250 words.

Conversation:

{conversation}
"""

        response = self.client.generate(

            LLMRequest(
                prompt=prompt,
            )

        )

        logger.info(
            "Conversation summarized."
        )

        return response.content