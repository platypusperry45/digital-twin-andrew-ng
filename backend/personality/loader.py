"""
Personality Loader.

Loads the active personality profile instance.
"""

from backend.personality.models import PersonalityProfile
from backend.personality.profile import ANDREW_NG_PROFILE


class PersonalityLoader:

    def load(self) -> PersonalityProfile:
        """Returns the canonical Andrew Ng personality profile."""
        return ANDREW_NG_PROFILE