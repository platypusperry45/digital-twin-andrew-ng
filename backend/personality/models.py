"""
Personality Models for Digital Twin of Andrew Ng.

Defines Pydantic models for representing Andrew Ng's teaching style,
speaking style, humor style, reasoning style, personality traits,
response rules, communication preferences, core values, domain expertise,
and overarching persona profile.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ResponseRules(BaseModel):
    """Rules and constraints guiding response generation behavior."""
    do_rules: List[str] = Field(default_factory=list, description="Mandatory behavioral guidelines")
    dont_rules: List[str] = Field(default_factory=list, description="Prohibited behaviors or tones")
    formatting_rules: List[str] = Field(default_factory=list, description="Response structure guidelines")


class PersonalityTraits(BaseModel):
    """Core behavioral and psychological personality traits."""
    openness: Optional[str] = Field(default="High - Passionate about new AI frontiers and continuous learning")
    conscientiousness: Optional[str] = Field(default="High - Rigorous, data-centric, and methodical")
    extraversion: Optional[str] = Field(default="Moderate - Clear communicator, accessible educator")
    agreeableness: Optional[str] = Field(default="High - Encouraging, supportive, and humble")
    neuroticism: Optional[str] = Field(default="Low - Calm under pressure, deliberate, patient")
    key_traits: List[str] = Field(default_factory=list, description="Notable character traits")


class TeachingStyle(BaseModel):
    """Pedagogical principles and instructional guidelines."""
    approach: str = Field(default="Bottom-up, intuition-first teaching", description="Core educational methodology")
    key_principles: List[str] = Field(default_factory=list, description="Guiding principles in teaching")
    common_analogies: List[str] = Field(default_factory=list, description="Frequently used analogies")
    problem_solving_steps: List[str] = Field(default_factory=list, description="Step-by-step diagnostic workflow")


class SpeakingStyle(BaseModel):
    """Rhetorical and verbal communication traits."""
    tone: str = Field(default="Encouraging, calm, structured, and pragmatic")
    pacing: str = Field(default="Deliberate and clear")
    signature_phrases: List[str] = Field(default_factory=list, description="Key quotes and phrases")
    rhetorical_devices: List[str] = Field(default_factory=list, description="Frequent rhetorical structures")


class CommunicationStyle(BaseModel):
    """Overall communication parameters."""
    tone: str = Field(default="Encouraging, structured, accessible, and pragmatic")
    catchphrases: List[str] = Field(default_factory=list, description="Famous quotes and recurring phrases")
    formatting_preferences: List[str] = Field(default_factory=list, description="Preferred response structures")


class HumorStyle(BaseModel):
    """Humor characteristics and usage patterns."""
    frequency: str = Field(default="Subtle and sparse")
    type: str = Field(default="Self-deprecating tech humor and light educational anecdotes")
    examples: List[str] = Field(default_factory=list, description="Example humorous statements or jokes")


class ReasoningStyle(BaseModel):
    """Problem analysis and logical framing methodology."""
    framework: str = Field(default="First-principles and empirical error analysis")
    approaches: List[str] = Field(default_factory=list, description="Reasoning steps and guidelines")


class CoreValue(BaseModel):
    """Core beliefs and professional philosophy."""
    name: str
    description: str


class ValueSystem(BaseModel):
    """Structured collection of core values and ethics."""
    values: List[CoreValue] = Field(default_factory=list)
    philosophies: List[str] = Field(default_factory=list)


class DomainExpertise(BaseModel):
    """Technical knowledge domains and topics."""
    area: str
    topics: List[str] = Field(default_factory=list)


class PersonaMetadata(BaseModel):
    """Metadata regarding persona versioning and configuration."""
    version: str = "1.0.0"
    author: str = "Digital Twin Team"
    description: Optional[str] = None


class PersonalityProfile(BaseModel):
    """Complete structured persona model for the Digital Twin."""
    name: str = "Andrew Ng"
    title: str = "AI Pioneer, Founder of DeepLearning.AI & Landing AI, Co-founder of Coursera"
    bio: str = "AI researcher, educator, and entrepreneur focusing on democratizing AI education."
    traits: Optional[PersonalityTraits] = None
    teaching_style: Optional[TeachingStyle] = None
    speaking_style: Optional[SpeakingStyle] = None
    communication_style: Optional[CommunicationStyle] = None
    humor_style: Optional[HumorStyle] = None
    reasoning_style: Optional[ReasoningStyle] = None
    response_rules: Optional[ResponseRules] = None
    value_system: Optional[ValueSystem] = None
    core_values: List[CoreValue] = Field(default_factory=list)
    expertise: List[DomainExpertise] = Field(default_factory=list)
    timeline_milestones: List[str] = Field(default_factory=list)
    metadata: Optional[PersonaMetadata] = None