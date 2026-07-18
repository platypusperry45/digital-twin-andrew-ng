"""
Personality Manager.

Provides application-wide access
to the active personality profile.
"""

from backend.personality.loader import (
    PersonalityLoader,
)

from backend.personality.models import (
    PersonalityProfile,
)


class PersonalityManager:

    def __init__(self):

        self.loader = PersonalityLoader()

        self.profile = self.loader.load()

    def get_profile(self) -> PersonalityProfile:
        """
        Return the active personality.
        """

        return self.profile

    def reload(self):
        """
        Reload the profile.

        Useful later if profiles
        become editable without
        restarting the backend.
        """

        self.profile = self.loader.load()