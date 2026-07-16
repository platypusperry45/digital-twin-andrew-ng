"""
Production Gemini client.

Responsibilities
----------------
- Gemini SDK communication
- key rotation
- retries
- model fallback
- cooldown awareness
- logging
- metrics
"""

import time

from google import genai

from backend.core.config import settings
from backend.core.logger import logger

from backend.llm.key_manager import KeyManager
from backend.llm.scheduler import LLMScheduler
from backend.llm.metrics import metrics

from backend.llm.models import (
    LLMRequest,
    LLMResponse,
)

from backend.llm.exceptions import (
    AllKeysExhaustedError,
)


class GeminiClient:

    def __init__(self):

        self.key_manager = KeyManager(
            settings.GEMINI_API_KEYS,
            settings.KEY_COOLDOWN_SECONDS,
        )

        self.scheduler = LLMScheduler()

    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:

        metrics.record_request()

        start = time.time()

        models = self.scheduler.get_model_sequence(
            request.model
        )

        last_error = None

        for model in models:

            logger.info(f"Trying model: {model}")

            for attempt in range(settings.LLM_MAX_RETRIES):

                # --------------------------------------------------
                # Obtain available key
                # --------------------------------------------------

                try:

                    api_key, key_index = (
                        self.key_manager.get_key()
                    )

                except RuntimeError:

                    logger.warning(
                        "All keys cooling down. Waiting..."
                    )

                    self.key_manager.wait_until_available()

                    continue

                try:

                    client = genai.Client(
                        api_key=api_key
                    )

                    response = (
                        client.models.generate_content(
                            model=model,
                            contents=request.prompt,
                        )
                    )

                    latency = (
                        time.time() - start
                    ) * 1000

                    self.key_manager.mark_success(
                        key_index
                    )

                    metrics.record_success(
                        latency
                    )

                    logger.success(
                        f"{model} succeeded "
                        f"(key {key_index})"
                    )

                    return LLMResponse(
                        content=response.text,
                        model_used=model,
                        key_index=key_index,
                        latency_ms=latency,
                    )

                except Exception as exc:

                    last_error = exc

                    self.key_manager.mark_failure(
                        key_index
                    )

                    metrics.record_failure()

                    logger.error(
                        f"""
Gemini Request Failed

Model      : {model}
Attempt    : {attempt + 1}/{settings.LLM_MAX_RETRIES}
Key Index  : {key_index}
Error Type : {type(exc).__name__}
Error      : {exc}
"""
                    )

                    time.sleep(
                        settings.LLM_RETRY_DELAY
                    )

            logger.warning(
                f"Switching to fallback model: {model}"
            )

        logger.error(
            "Every Gemini model failed."
        )

        raise AllKeysExhaustedError(
            str(last_error)
        )