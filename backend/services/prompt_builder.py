"""
Prompt Builder.

Responsible for assembling the final prompt sent to the LLM.

Combines:
- System prompt
- Long-term memory
- Recent conversation
- Retrieved knowledge
- Current user message
"""

from backend.memory.models import MemoryContext
from backend.rag.retrieval.retrieval_models import RetrievalResponse


class PromptBuilder:

    def __init__(self):

        self.system_prompt = """
You are the Digital Twin of Andrew Ng.

Your identity:
- You are Andrew Ng.
- Speak naturally and professionally.
- Explain difficult concepts simply.
- Prefer teaching over giving direct answers.
- Think step by step.
- Be concise unless the user asks for detail.
- Never mention you are Gemini or an AI model.
"""

    def build(
        self,
        user_prompt: str,
        memory: MemoryContext | None = None,
        knowledge: RetrievalResponse | None = None,
    ) -> str:

        sections = []

        # -------------------------------------------------
        # System Prompt
        # -------------------------------------------------

        sections.append(self.system_prompt.strip())

        # -------------------------------------------------
        # Long-term Memory
        # -------------------------------------------------

        if memory and memory.long_term:

            text = [
                "Relevant Long-Term Memory",
                "-------------------------",
            ]

            for item in memory.long_term:
                text.append(f"- {item.memory.content}")

            sections.append("\n".join(text))

        # -------------------------------------------------
        # Recent Conversation
        # -------------------------------------------------

        if memory and memory.short_term:

            text = [
                "Recent Conversation",
                "-------------------",
            ]

            for turn in memory.short_term:

                text.append(f"User: {turn.user}")
                text.append(f"Assistant: {turn.assistant}")
                text.append("")

            sections.append("\n".join(text))

        # -------------------------------------------------
        # Retrieved Knowledge
        # -------------------------------------------------

        if knowledge and knowledge.results:

            text = [
                "Knowledge Base",
                "--------------",
            ]

            for result in knowledge.results:

                text.append(result.text)

                text.append("")

            sections.append("\n".join(text))

        # -------------------------------------------------
        # Current User Prompt
        # -------------------------------------------------

        sections.append(
            "Current User Message\n"
            "--------------------\n"
            f"{user_prompt}"
        )

        return "\n\n".join(sections)