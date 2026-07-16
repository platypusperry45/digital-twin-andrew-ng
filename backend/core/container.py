"""
Application dependency container.

Maintains shared services.
"""


from typing import Optional

from backend.llm import GeminiClient


class Container:


    def __init__(self):

        self._gemini_client: Optional[
            GeminiClient
        ] = None



    def initialize(self):

        """
        Initialize application services.
        """

        self._gemini_client = GeminiClient()



    def shutdown(self):

        """
        Cleanup resources.
        """

        self._gemini_client = None



    @property
    def gemini(
        self
    ) -> GeminiClient:


        if self._gemini_client is None:

            raise RuntimeError(
                "Container not initialized"
            )


        return self._gemini_client



# Global container instance

container = Container()