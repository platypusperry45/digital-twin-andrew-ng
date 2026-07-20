"""
Profile Builder.

Combines all analyzer outputs into a single
PersonalityProfile and persists it.
"""

from __future__ import annotations

import json
from pathlib import Path

from backend.core.logger import logger

from backend.personality.models import (
    PersonalityProfile,
    VocabularyProfile,
    PhraseProfile,
    AnalogyProfile,
    HumorProfile,
    TeachingProfile,
    StyleProfile,
    ResponseStructureProfile,
)


class ProfileBuilder:

    def __init__(self):

        self.output = (

            Path(__file__).resolve().parents[2]

            / "data"

            / "personality"

            / "extracted"

            / "profile.json"

        )

        self.output.parent.mkdir(

            parents=True,

            exist_ok=True,

        )

    def build(

        self,

        vocabulary: VocabularyProfile,

        phrases: PhraseProfile,

        analogies: AnalogyProfile,

        humor: HumorProfile,

        teaching: TeachingProfile,

        style: StyleProfile,

        response_structure: ResponseStructureProfile,

    ) -> PersonalityProfile:

        profile = PersonalityProfile(

            vocabulary=vocabulary,

            phrases=phrases,

            analogies=analogies,

            humor=humor,

            teaching=teaching,

            style=style,

            response_structure=response_structure,

        )

        self.save(profile)

        logger.success(
            "Personality profile built."
        )

        return profile

    def save(
        self,
        profile: PersonalityProfile,
    ):

        with open(

            self.output,

            "w",

            encoding="utf-8",

        ) as file:

            json.dump(

                profile.model_dump(

                    mode="json"

                ),

                file,

                indent=4,

                ensure_ascii=False,

            )

        logger.success(
            "profile.json written."
        )

    def load(
        self,
    ) -> PersonalityProfile:

        if not self.output.exists():

            logger.warning(
                "profile.json not found."
            )

            return PersonalityProfile()

        with open(

            self.output,

            "r",

            encoding="utf-8",

        ) as file:

            data = json.load(file)

        return PersonalityProfile(

            **data

        )