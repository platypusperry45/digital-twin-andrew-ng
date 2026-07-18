"""
Prompt Builder.

Combines:

- System Prompt
- Retrieved Memory
- Retrieved Knowledge
- Current User Prompt
"""

from backend.memory.models import MemoryContext
from backend.rag.retrieval.retrieval_models import RetrievalResponse


class PromptBuilder:

    def build(
        self,
        user_prompt: str,
        memory: MemoryContext,
        knowledge: RetrievalResponse | None = None,
    ) -> str:

        prompt = []

        prompt.append(
            """
You are a digital twin of Andrew Ng.

You answer exactly as Andrew Ng would.

Use the supplied memory and knowledge whenever relevant.

If knowledge contradicts memory,
prefer knowledge.

Never mention that you are an AI model.
""".strip()
        )

        # ----------------------
        # Long-term memory
        # ----------------------

        if memory.long_term:

            prompt.append("\n### Long-Term Memory")

            for item in memory.long_term:

                prompt.append(
                    f"- {item.memory.content}"
                )

        # ----------------------
        # Recent conversation
        # ----------------------

        if memory.short_term:

            prompt.append("\n### Recent Conversation")

            for turn in memory.short_term:

                prompt.append(
                    f"User: {turn.user}"
                )

                prompt.append(
                    f"Assistant: {turn.assistant}"
                )

        # ----------------------
        # Knowledge
        # ----------------------

        if (
            knowledge is not None
            and knowledge.results
        ):

            prompt.append("\n### Knowledge Base")

            for result in knowledge.results:

                prompt.append(result.text)

        # ----------------------
        # Current question
        # ----------------------

        prompt.append("\n### User")

        prompt.append(user_prompt)

        prompt.append("\n### Assistant")

        return "\n".join(prompt)