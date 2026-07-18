"""
Personality models.

Defines the complete personality profile used
by the Prompt Builder.
"""

from typing import List

from pydantic import BaseModel, Field


class TeachingStyle(BaseModel):
    """
    How the person teaches.
    """

    explanation_order: List[str] = Field(default_factory=list)

    prefers_intuition: bool = True

    uses_math_after_intuition: bool = True

    encourages_learning: bool = True

    asks_reflective_questions: bool = False

    uses_step_by_step: bool = True


class SpeakingStyle(BaseModel):
    """
    Speaking characteristics.
    """

    tone: str

    sentence_style: str

    vocabulary: str

    pacing: str

    enthusiasm: str


class HumorStyle(BaseModel):
    """
    Humor characteristics.
    """

    uses_humor: bool

    humor_style: str

    sarcasm: bool


class PersonalityTraits(BaseModel):
    """
    General personality.
    """

    traits: List[str] = Field(default_factory=list)


class ResponseRules(BaseModel):
    """
    Hard rules that should always be followed.
    """

    always_do: List[str] = Field(default_factory=list)

    never_do: List[str] = Field(default_factory=list)


class PersonalityProfile(BaseModel):
    """
    Complete personality profile.
    """

    name: str

    role: str

    biography: str

    mission: str

    teaching: TeachingStyle

    speaking: SpeakingStyle

    humor: HumorStyle

    personality: PersonalityTraits

    rules: ResponseRules

    favorite_phrases: List[str] = Field(default_factory=list)

    favorite_examples: List[str] = Field(default_factory=list)

    preferred_analogies: List[str] = Field(default_factory=list)