"""
Prompt models.

Defines the structure used by the PromptBuilder before
sending a request to the LLM.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class PromptContext(BaseModel):
    """
    Complete context required for prompt construction.
    """

    user_message: str

    personality: str = ""

    memories: list[str] = Field(default_factory=list)

    retrieved_documents: list[str] = Field(default_factory=list)

    conversation_history: list[str] = Field(default_factory=list)

    additional_context: dict[str, Any] = Field(
        default_factory=dict
    )


class PromptResult(BaseModel):
    """
    Final prompt ready for Gemini.
    """

    system_prompt: str

    user_prompt: str

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )