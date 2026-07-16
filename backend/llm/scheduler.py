"""
LLM scheduler.

Controls:
- model priority
- fallback sequence
- retry decisions
"""


from backend.core.config import settings


class LLMScheduler:


    def __init__(self):

        self.primary = (
            settings.PRIMARY_MODEL
        )

        self.fallback = (
            settings.FALLBACK_MODEL
        )

        self.fast = (
            settings.FAST_MODEL
        )


    def get_model_sequence(
        self,
        requested=None,
    ):

        if requested:
            return [
                requested,
                self.fallback,
                self.fast,
            ]


        return [
            self.primary,
            self.fast,
            self.fallback,
        ]



    def should_retry(
        self,
        attempt: int,
    ):

        return (
            attempt
            <
            settings.LLM_MAX_RETRIES
        )