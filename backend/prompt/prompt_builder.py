"""
Prompt Builder.

Responsible for assembling the complete prompt
used by the Gemini client.

Sources

- Personality
- Long-term Memory
- Knowledge Retrieval
- User Prompt

Conversation history is supplied separately through
LLMRequest.messages and is NOT duplicated inside the
constructed prompt.
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
    Production prompt builder.

    Converts structured application state into an
    LLMRequest suitable for Gemini.

    Responsibilities

    - Build the system prompt from the Andrew Ng
      personality profile.

    - Inject long-term semantic memories.

    - Inject retrieved knowledge.

    - Keep conversation history separate from the
      prompt. Chat history is supplied through
      LLMRequest.messages.
    """

    def build(
        self,
        *,
        profile: PersonalityProfile,
        memory: MemoryContext,
        knowledge: RetrievalResponse | None,
        user_prompt: str,
        temperature: float = 0.3,
    ) -> LLMRequest:

        return LLMRequest(
            system_prompt=self._build_system_prompt(
                profile,
            ),
            user_prompt=self._build_user_prompt(
                user_prompt=user_prompt,
                memory=memory,
                knowledge=knowledge,
            ),
            config=GenerationConfig(
                temperature=temperature,
            ),
        )

    # ==========================================================
    # System Prompt
    # ==========================================================

    def _build_system_prompt(
        self,
        profile: PersonalityProfile,
    ) -> str:

        sections: list[str] = []

        sections.append(
            "You are the digital twin of Andrew Ng."
        )

        sections.append(
            "Your goal is to respond exactly as Andrew Ng would."
        )

        sections.append(
            "Never reveal that you are an AI model."
        )

        sections.append(
            "Never invent facts."
        )

        sections.append(
            "If the supplied knowledge is insufficient, clearly state uncertainty."
        )

        sections.append(
            "Always prioritize educational value over brevity."
        )

        sections.append(
            "Explain concepts clearly, progressively, and accurately."
        )

        sections.append(
            "\n========== PERSONALITY =========="
        )

        # ------------------------------------------------------
        # Style
        # ------------------------------------------------------

        if profile.style.tone:
            sections.append(
                f"Tone: {profile.style.tone}"
            )

        if profile.style.verbosity:
            sections.append(
                f"Verbosity: {profile.style.verbosity}"
            )

        if profile.style.confidence:
            sections.append(
                f"Confidence: {profile.style.confidence}"
            )

        if profile.style.reading_level:
            sections.append(
                f"Reading Level: {profile.style.reading_level}"
            )

        # ------------------------------------------------------
        # Teaching
        # ------------------------------------------------------

        sections.append(
            "\nTeaching Style"
        )

        if profile.teaching.explanation_order:

            sections.append(
                "Preferred explanation order:"
            )

            for step in profile.teaching.explanation_order:
                sections.append(
                    f"- {step}"
                )

        sections.append(
            f"Intuition before mathematics: "
            f"{profile.teaching.intuition_before_math}"
        )

        sections.append(
            f"Example frequency: "
            f"{profile.teaching.example_frequency}"
        )

        sections.append(
            f"Question frequency: "
            f"{profile.teaching.question_frequency}"
        )

        # ------------------------------------------------------
        # Vocabulary
        # ------------------------------------------------------

        if profile.vocabulary.common_words:

            sections.append(
                "\nCommon Vocabulary"
            )

            sections.extend(
                f"- {word}"
                for word in profile.vocabulary.common_words
            )

        if profile.vocabulary.transition_words:

            sections.append(
                "\nTransition Words"
            )

            sections.extend(
                f"- {word}"
                for word in profile.vocabulary.transition_words
            )

        if profile.vocabulary.technical_terms:

            sections.append(
                "\nTechnical Terms"
            )

            sections.extend(
                f"- {word}"
                for word in profile.vocabulary.technical_terms
            )

        # ------------------------------------------------------
        # Phrases
        # ------------------------------------------------------

        if profile.phrases.introductions:

            sections.append(
                "\nTypical Introductions"
            )

            sections.extend(
                f"- {text}"
                for text in profile.phrases.introductions
            )

        if profile.phrases.transitions:

            sections.append(
                "\nTypical Transitions"
            )

            sections.extend(
                f"- {text}"
                for text in profile.phrases.transitions
            )

        if profile.phrases.explanations:

            sections.append(
                "\nTypical Explanations"
            )

            sections.extend(
                f"- {text}"
                for text in profile.phrases.explanations
            )

        if profile.phrases.summaries:

            sections.append(
                "\nTypical Summaries"
            )

            sections.extend(
                f"- {text}"
                for text in profile.phrases.summaries
            )

        if profile.phrases.encouragements:

            sections.append(
                "\nEncouragement Style"
            )

            sections.extend(
                f"- {text}"
                for text in profile.phrases.encouragements
            )

        # ------------------------------------------------------
        # Analogies
        # ------------------------------------------------------

        if profile.analogies.analogies:

            sections.append(
                "\nPreferred Analogies"
            )

            sections.extend(
                f"- {text}"
                for text in profile.analogies.analogies
            )

        # ------------------------------------------------------
        # Response Structure
        # ------------------------------------------------------

        if profile.response_structure.sections:

            sections.append(
                "\nPreferred Response Structure"
            )

            sections.extend(
                f"- {text}"
                for text in profile.response_structure.sections
            )

        sections.append(
            "\nMaintain these characteristics consistently while remaining natural."
        )

        return "\n".join(sections)

    # ==========================================================
    # User Prompt
    # ==========================================================

    def _build_user_prompt(
        self,
        *,
        user_prompt: str,
        memory: MemoryContext,
        knowledge: RetrievalResponse | None,
    ) -> str:

        sections: list[str] = []

        # ------------------------------------------------------
        # Long-Term Semantic Memory
        # ------------------------------------------------------

        if memory.long_term:

            sections.append(
                "### Relevant Long-Term Memory"
            )

            for item in memory.long_term:

                sections.append(
                    f"- {item.memory.content}"
                )

        # ------------------------------------------------------
        # Retrieved Knowledge
        # ------------------------------------------------------

        if knowledge and knowledge.results:

            sections.append(
                "\n### Retrieved Knowledge"
            )

            for result in knowledge.results:

                sections.append(
                    f"[Source: {result.filename}]"
                )

                sections.append(
                    result.text
                )

        # ------------------------------------------------------
        # Current User Question
        # ------------------------------------------------------

        sections.append(
            "\n### Current User Question"
        )

        sections.append(
            user_prompt
        )

        sections.append(
            "\n### Response"
        )

        return "\n".join(sections)