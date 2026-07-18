"""
Personality Loader.

Loads the active personality profile.
"""

from backend.personality.models import (
    PersonalityProfile,
)

from backend.personality.profile import (
    ANDREW_NG_PROFILE,
)


class PersonalityLoader:
    """
    Loads personality profiles.

    In the future this can load from:
    - YAML
    - JSON
    - Database
    - Remote API
    """

    def load(self) -> PersonalityProfile:
        """
        Return the active personality profile.
        """

        return ANDREW_NG_PROFILE