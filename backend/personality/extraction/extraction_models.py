"""
Personality Extraction Models.
"""

from __future__ import annotations

from pydantic import BaseModel

from backend.personality.models import (
    VocabularyProfile,
    PhraseProfile,
    AnalogyProfile,
    HumorProfile,
    TeachingProfile,
    StyleProfile,
    ResponseStructureProfile,
)


class Transcript(BaseModel):

    source: str

    title: str

    text: str


class PersonalityExtraction(BaseModel):

    vocabulary: VocabularyProfile

    phrases: PhraseProfile

    analogies: AnalogyProfile

    humor: HumorProfile

    teaching: TeachingProfile

    style: StyleProfile

    response_structure: ResponseStructureProfile


class ExtractionResult(BaseModel):

    transcript: Transcript

    profile: PersonalityExtraction