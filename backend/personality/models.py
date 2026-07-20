"""
Personality Models.

Shared models used by every personality extraction module.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class VocabularyProfile(BaseModel):

    common_words: list[str] = Field(default_factory=list)

    transition_words: list[str] = Field(default_factory=list)

    technical_terms: list[str] = Field(default_factory=list)

    favorite_verbs: list[str] = Field(default_factory=list)


class PhraseProfile(BaseModel):

    introductions: list[str] = Field(default_factory=list)

    transitions: list[str] = Field(default_factory=list)

    explanations: list[str] = Field(default_factory=list)

    summaries: list[str] = Field(default_factory=list)

    encouragements: list[str] = Field(default_factory=list)


class AnalogyProfile(BaseModel):

    analogies: list[str] = Field(default_factory=list)


class HumorProfile(BaseModel):

    examples: list[str] = Field(default_factory=list)

    humor_density: float = 0.0


class TeachingProfile(BaseModel):

    explanation_order: list[str] = Field(default_factory=list)

    example_frequency: float = 0.0

    intuition_before_math: bool = True

    question_frequency: float = 0.0


class StyleProfile(BaseModel):

    tone: str = ""

    verbosity: str = ""

    confidence: str = ""

    reading_level: str = ""

    encouragement_level: float = 0.0

class ResponseStructureProfile(BaseModel):

    sections: list[str] = Field(
        default_factory=list
    )

class PersonalityProfile(BaseModel):

    vocabulary: VocabularyProfile = Field(
        default_factory=VocabularyProfile
    )

    phrases: PhraseProfile = Field(
        default_factory=PhraseProfile
    )

    analogies: AnalogyProfile = Field(
        default_factory=AnalogyProfile
    )

    humor: HumorProfile = Field(
        default_factory=HumorProfile
    )

    teaching: TeachingProfile = Field(
        default_factory=TeachingProfile
    )

    style: StyleProfile = Field(
        default_factory=StyleProfile
    )

    response_structure: ResponseStructureProfile = Field(
        default_factory=ResponseStructureProfile
    )