"""
Conversation manager.

Maintains chat history and prepares LLM requests.
"""

from __future__ import annotations

from backend.llm.models import (
    ChatMessage,
    LLMRequest,
    GenerationConfig,
)


class Conversation:

    def __init__(self) -> None:

        self.messages: list[ChatMessage] = []

    def clear(self) -> None:

        self.messages.clear()

    def add_user(
        self,
        message: str,
    ) -> None:

        self.messages.append(

            ChatMessage(

                role="user",

                content=message,

            )

        )

    def add_assistant(
        self,
        message: str,
    ) -> None:

        self.messages.append(

            ChatMessage(

                role="assistant",

                content=message,

            )

        )

    def history(
        self,
    ) -> list[ChatMessage]:

        return list(self.messages)

    def build_request(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        model: str | None = None,
        config: GenerationConfig | None = None,
    ) -> LLMRequest:

        return LLMRequest(

            user_prompt=prompt,

            system_prompt=system_prompt,

            messages=self.history(),

            model=model,

            config=config or GenerationConfig(),

        )