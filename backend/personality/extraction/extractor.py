"""
Personality Extractor.

Uses ONE Gemini request to extract Andrew Ng's
complete personality profile.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from backend.core.logger import logger

from backend.llm.gemini_client import GeminiClient
from backend.llm.models import LLMRequest

from backend.personality.extraction.extraction_models import (
    Transcript,
    PersonalityExtraction,
)

from backend.personality.extraction.profile_builder import (
    ProfileBuilder,
)

from backend.personality.extraction.transcript_parser import (
    TranscriptParser,
)


class PersonalityExtractor:

    def __init__(
        self,
        llm: GeminiClient,
    ):

        self.llm = llm

        self.parser = TranscriptParser()

        self.builder = ProfileBuilder()

    def extract(

        self,

        path: Path,

        text: str,

    ):

        transcript = self.parser.parse(

            path,

            text,

        )

        prompt = self._build_prompt(

            transcript

        )

        response = self.llm.generate(

            LLMRequest(

                prompt=prompt,

                model="gemini-2.5-flash",

            )

        )

        content = self._clean_json(

            response.content

        )

        extraction = PersonalityExtraction.model_validate_json(

            content

        )

        profile = self.builder.build(

            vocabulary=extraction.vocabulary,

            phrases=extraction.phrases,

            analogies=extraction.analogies,

            humor=extraction.humor,

            teaching=extraction.teaching,

            style=extraction.style,

            response_structure=extraction.response_structure,

        )

        logger.success(

            "Personality extraction complete."

        )

        return profile

    def _build_prompt(

        self,

        transcript: Transcript,

    ) -> str:

        return f"""
You are analyzing Andrew Ng.

Return ONLY valid JSON.

Extract ALL of the following.

1. Vocabulary
    - common_words
    - transition_words
    - technical_terms
    - favorite_verbs

2. Frequently used teaching phrases

3. Teaching analogies

4. Humor examples

5. Teaching methodology

6. Communication style

7. Response structure

Return JSON matching this schema exactly:

{PersonalityExtraction.model_json_schema()}

Rules

- No markdown
- No explanations
- No comments
- JSON only
- Do not invent information
- Use only evidence from the transcript

Transcript

{transcript.text}
"""

    @staticmethod
    def _clean_json(

        text: str,

    ) -> str:

        text = text.strip()

        text = re.sub(

            r"^```json",

            "",

            text,

            flags=re.IGNORECASE,

        )

        text = re.sub(

            r"^```",

            "",

            text,

        )

        text = re.sub(

            r"```$",

            "",

            text,

        )

        return text.strip()