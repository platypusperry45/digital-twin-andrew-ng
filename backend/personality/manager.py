"""
Personality Manager.

Provides application-wide access to the active personality profile.
"""

from backend.personality.loader import PersonalityLoader
from backend.personality.models import PersonalityProfile


class PersonalityManager:

    def __init__(self) -> None:
        self.loader = PersonalityLoader()
        self.profile = self.loader.load()

    def get_profile(self) -> PersonalityProfile:
        """Returns the active personality profile."""
        return self.profile

    def reload(self) -> None:
        """Reloads the active personality profile."""
        self.profile = self.loader.load()