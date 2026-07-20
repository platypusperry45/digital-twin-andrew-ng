"""
Prompt Builder.

Responsible for assembling the complete prompt
used by the Gemini client.

Sources:

- Personality
- Memory
- Knowledge Retrieval
- User Prompt

Output:

LLMRequest
"""

from __future__ import annotations

from backend.llm.models import (
    GenerationConfig,
    LLMRequest,
)

from backend.memory.models import (
    MemoryContext,
)

from backend.personality.models import (
    PersonalityProfile,
)

from backend.rag.retrieval.retrieval_models import (
    RetrievalResponse,
)


class PromptBuilder:
    """
    Builds production-ready prompts.

    The builder separates:

    - System Prompt
    - User Prompt

    instead of producing one massive prompt.

    This allows GeminiClient to use
    native conversation handling.
    """

    def build(
        self,
        *,
        profile: PersonalityProfile,
        memory: MemoryContext,
        knowledge: RetrievalResponse | None,
        user_prompt: str,
        temperature: float = 0.7,
    ) -> LLMRequest:
        """
        Build a complete LLMRequest.

        Parameters
        ----------
        profile
            Andrew Ng personality profile.

        memory
            Retrieved memory context.

        knowledge
            Retrieved RAG documents.

        user_prompt
            User question.

        temperature
            Generation temperature.
        """

        system_prompt = self._build_system_prompt(
            profile=profile,
        )

        final_user_prompt = self._build_user_prompt(
            user_prompt=user_prompt,
            memory=memory,
            knowledge=knowledge,
        )

        return LLMRequest(

            system_prompt=system_prompt,

            user_prompt=final_user_prompt,

            config=GenerationConfig(
                temperature=temperature,
            ),

        )

    # =====================================================
    # System Prompt
    # =====================================================

    def _build_system_prompt(
        self,
        profile: PersonalityProfile,
    ) -> str:

        prompt: list[str] = []

        prompt.append(
            "You are the digital twin of Andrew Ng."
        )

        prompt.append(
            "Respond exactly as Andrew Ng would."
        )

        prompt.append(
            "Your answers must reflect Andrew Ng's "
            "teaching style, communication patterns, "
            "reasoning process, values and personality."
        )

        prompt.append(
            "Never mention that you are an AI model."
        )

        prompt.append(
            "Never invent facts."
        )

        prompt.append(
            "If the supplied knowledge is insufficient, "
            "state uncertainty honestly."
        )

        # -------------------------------------------------
        # Personality
        # -------------------------------------------------

        prompt.append("\n===== Personality =====")

        if profile.summary:

            prompt.append(profile.summary)

        if profile.communication_style:

            prompt.append(
                "\nCommunication Style:"
            )

            prompt.append(
                profile.communication_style
            )

        if profile.teaching_style:

            prompt.append(
                "\nTeaching Style:"
            )

            prompt.append(
                profile.teaching_style
            )

        if profile.thinking_style:

            prompt.append(
                "\nThinking Style:"
            )

            prompt.append(
                profile.thinking_style
            )

        if profile.values:

            prompt.append(
                "\nCore Values:"
            )

            for value in profile.values:

                prompt.append(
                    f"- {value}"
                )

        if profile.catchphrases:

            prompt.append(
                "\nFrequently Used Expressions:"
            )

            for phrase in profile.catchphrases:

                prompt.append(
                    f"- {phrase}"
                )

        return "\n".join(prompt)

    # =====================================================
    # User Prompt
    # =====================================================

    def _build_user_prompt(
        self,
        *,
        user_prompt: str,
        memory: MemoryContext,
        knowledge: RetrievalResponse | None,
    ) -> str:

        sections: list[str] = []

        # -------------------------------------------------
        # Memory
        # -------------------------------------------------

        if memory.long_term:

            sections.append(
                "### Relevant Long-Term Memory"
            )

            for item in memory.long_term:

                sections.append(
                    f"- {item.memory.content}"
                )

        if memory.short_term:

            sections.append(
                "\n### Recent Conversation"
            )

            for turn in memory.short_term:

                sections.append(
                    f"User: {turn.user}"
                )

                sections.append(
                    f"Assistant: {turn.assistant}"
                )

        # -------------------------------------------------
        # Knowledge
        # -------------------------------------------------

        if (
            knowledge is not None
            and knowledge.results
        ):

            sections.append(
                "\n### Retrieved Knowledge"
            )

            for result in knowledge.results:

                sections.append(result.text)

        # -------------------------------------------------
        # Current User Query
        # -------------------------------------------------

        sections.append(
            "\n### User Question"
        )

        sections.append(user_prompt)

        sections.append(
            "\n### Assistant"
        )

        return "\n".join(sections)