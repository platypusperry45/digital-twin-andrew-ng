"""
Production-grade Gemini client.

Responsibilities:
- Exclusive gateway to Google Gemini API
- HTTP client caching per API key
- Automatic key rotation with cooldown awareness
- Model fallback with configurable sequence
- Retry logic with exponential backoff
- Request/response metrics tracking
- Comprehensive logging at each stage
- Structured output support with Pydantic validation
- Streaming responses
- Embeddings generation
- Health status reporting

Compatible with:
- Python 3.13
- google-genai==1.30.0
- Pydantic v2
- FastAPI

Architecture:
- Single GeminiClient class (no composition)
- Reuses existing: KeyManager, LLMScheduler, Metrics, logger, exceptions
- Caches one genai.Client per API key
- No duplicate retry or metrics logic
- Type-safe with full docstrings
"""

from __future__ import annotations

import json
import time
from typing import Any, Generator, Optional, Type, TypeVar

from google import genai
from google.genai import types
from google.genai.types import GenerateContentResponse
from pydantic import BaseModel, ValidationError

from backend.core.config import settings
from backend.core.logger import logger

from backend.llm.exceptions import (
    AllKeysExhaustedError,
    LLMException,
    ModelUnavailableError,
)
from backend.llm.key_manager import KeyManager
from backend.llm.metrics import metrics
from backend.llm.models import (
    ChatMessage,
    EmbeddingRequest,
    EmbeddingResponse,
    GenerationConfig,
    LLMHealth,
    LLMRequest,
    LLMResponse,
    TokenUsage,
)
from backend.llm.scheduler import LLMScheduler

T = TypeVar("T", bound=BaseModel)


class GeminiClient:
    """
    Production Gemini API client.

    Single gateway for all Gemini interactions:
    - Text generation with system prompts and history
    - Structured output with Pydantic schema validation
    - Streaming responses
    - Embedding generation
    - Health monitoring

    Manages:
    - HTTP client caching (one per API key)
    - Automatic API key rotation
    - Model fallback sequences
    - Retry logic with exponential backoff
    - Request metrics
    - Detailed logging
    """

    def __init__(self) -> None:
        """
        Initialize Gemini client.

        Sets up:
        - Key manager for rotation and cooldown
        - Model scheduler for fallback sequences
        - Client cache (per API key)
        - Metrics tracking
        """
        if not settings.GEMINI_API_KEYS:
            raise ValueError(
                "No Gemini API keys configured. "
                "Set GEMINI_API_KEYS in environment."
            )

        self.key_manager = KeyManager(
            settings.GEMINI_API_KEYS,
            settings.KEY_COOLDOWN_SECONDS,
        )

        self.scheduler = LLMScheduler()

        # Cache: {api_key: genai.Client}
        self._client_cache: dict[str, genai.Client] = {}

        logger.info(
            f"Gemini client initialized with "
            f"{len(settings.GEMINI_API_KEYS)} API keys"
        )

    # ========================================================================
    # Core Generation Methods
    # ========================================================================

    def generate(self, request: LLMRequest) -> LLMResponse:
        """
        Generate text response with full feature support.

        Features:
        - System prompt support
        - Conversation history (multi-turn)
        - Configurable generation parameters
        - Automatic retry with backoff
        - Model fallback sequence
        - API key rotation
        - Detailed metrics and logging

        Args:
            request: LLMRequest with prompts, model, config, metadata

        Returns:
            LLMResponse with text, model, key index, latency, usage stats

        Raises:
            AllKeysExhaustedError: All keys failed or cooling down
            ModelUnavailableError: All models in fallback sequence failed
            LLMException: Unexpected error during generation
        """
        metrics.record_request()

        start_time = time.time()
        last_error: Exception | None = None

        logger.info(
            f"Starting generation request: "
            f"model={request.model}, "
            f"has_system_prompt={bool(request.system_prompt)}, "
            f"history_len={len(request.messages)}"
        )

        model_sequence = self.scheduler.get_model_sequence(request.model)

        for model in model_sequence:
            logger.debug(f"Attempting generation with model: {model}")

            for attempt in range(settings.LLM_MAX_RETRIES):
                try:
                    # Get available API key
                    api_key, key_index = self._get_available_key()

                    logger.debug(
                        f"Using API key index {key_index} "
                        f"(attempt {attempt + 1}/{settings.LLM_MAX_RETRIES})"
                    )

                    # Execute generation with retry logic
                    response = self._execute_with_retry(
                        api_key=api_key,
                        key_index=key_index,
                        model=model,
                        request=request,
                        attempt=attempt,
                    )

                    # Record metrics
                    latency_ms = (time.time() - start_time) * 1000
                    self._record_success(key_index, latency_ms)

                    logger.info(
                        f"Generation succeeded: "
                        f"model={model}, "
                        f"key_index={key_index}, "
                        f"latency_ms={latency_ms:.2f}"
                    )

                    # Parse response
                    return self._parse_response(
                        response=response,
                        model=model,
                        key_index=key_index,
                        latency_ms=latency_ms,
                    )

                except AllKeysExhaustedError as exc:
                    last_error = exc
                    logger.warning(
                        f"All keys exhausted on attempt {attempt + 1}. "
                        f"Waiting for key availability..."
                    )
                    self.key_manager.wait_until_available()

                except (LLMException, Exception) as exc:
                    last_error = exc
                    self._record_failure()

                    logger.warning(
                        f"Generation failed on {model}: "
                        f"attempt={attempt + 1}, "
                        f"error_type={type(exc).__name__}, "
                        f"error={str(exc)}"
                    )

                    if self.scheduler.should_retry(attempt):
                        delay = settings.LLM_RETRY_DELAY * (2 ** attempt)
                        logger.debug(
                            f"Retrying after {delay}s backoff..."
                        )
                        time.sleep(delay)
                    else:
                        logger.debug(
                            f"Max retries ({settings.LLM_MAX_RETRIES}) "
                            f"reached for model {model}"
                        )
                        break

        # All models and retries exhausted
        logger.error(
            f"Generation exhausted all models and retries. "
            f"Last error: {last_error}"
        )
        self._record_failure()
        raise ModelUnavailableError(
            f"All models failed. Last error: {str(last_error)}"
        )

    def generate_structured(
        self,
        request: LLMRequest,
        response_schema: Type[T],
    ) -> T:
        """
        Generate structured output validated against Pydantic schema.

        Features:
        - JSON mode with schema validation
        - Automatic retries on validation failure
        - Type-safe response parsing
        - Comprehensive error messages

        Args:
            request: LLMRequest with generation parameters
            response_schema: Pydantic BaseModel class for validation

        Returns:
            Validated instance of response_schema

        Raises:
            ValidationError: Response doesn't match schema
            ModelUnavailableError: Generation or validation failed
        """
        logger.info(
            f"Starting structured generation: "
            f"schema={response_schema.__name__}"
        )

        # Set response schema in request
        request_copy = request.model_copy()
        request_copy.response_schema = response_schema

        max_attempts = settings.LLM_MAX_RETRIES

        for attempt in range(max_attempts):
            try:
                # Generate with JSON mode
                response = self.generate(request_copy)

                logger.debug(
                    f"Parsing structured response "
                    f"(attempt {attempt + 1}/{max_attempts})"
                )

                # Extract and validate JSON
                parsed_json = self._extract_json(response.text)

                validated = response_schema.model_validate(parsed_json)

                logger.info(
                    f"Structured generation succeeded: "
                    f"schema={response_schema.__name__}"
                )

                return validated

            except ValidationError as exc:
                logger.warning(
                    f"Structured validation failed "
                    f"(attempt {attempt + 1}/{max_attempts}): {exc}"
                )

                if attempt < max_attempts - 1:
                    time.sleep(settings.LLM_RETRY_DELAY)
                else:
                    raise ModelUnavailableError(
                        f"Structured output validation failed after "
                        f"{max_attempts} attempts: {exc}"
                    ) from exc

            except json.JSONDecodeError as exc:
                logger.warning(
                    f"JSON extraction failed "
                    f"(attempt {attempt + 1}/{max_attempts}): {exc}"
                )

                if attempt < max_attempts - 1:
                    time.sleep(settings.LLM_RETRY_DELAY)
                else:
                    raise ModelUnavailableError(
                        f"Invalid JSON in structured response after "
                        f"{max_attempts} attempts: {exc}"
                    ) from exc

    def stream(
        self,
        request: LLMRequest,
    ) -> Generator[str, None, None]:
        """
        Generate streaming text response.
        """

        logger.info("Starting streaming generation")

        metrics.record_request()

        start_time = time.time()
        last_error: Exception | None = None

        model_sequence = self.scheduler.get_model_sequence(
            request.model
        )

        for model in model_sequence:

            for attempt in range(settings.LLM_MAX_RETRIES):

                try:

                    api_key, key_index = (
                        self._get_available_key()
                    )

                    logger.debug(
                        f"Streaming with {model} "
                        f"(key {key_index})"
                    )

                    client = self._get_client(api_key)

                    contents = self._build_content_parts(
                        request
                    )

                    generation_config = (
                        self._build_generation_config(
                            request
                        )
                    )

                    stream_response = (
                        client.models.generate_content(
                            model=model,
                            contents=contents,
                            config=generation_config,
                            stream=True,
                        )
                    )

                    chunk_count = 0

                    for chunk in stream_response:

                        if chunk.text:

                            chunk_count += 1

                            logger.debug(
                                f"Chunk {chunk_count} received"
                            )

                            yield chunk.text

                    latency_ms = (
                        time.time() - start_time
                    ) * 1000

                    self._record_success(
                        key_index,
                        latency_ms,
                    )

                    logger.info(
                        f"Streaming completed "
                        f"({chunk_count} chunks)"
                    )

                    return

                except Exception as exc:

                    last_error = exc

                    self._record_failure()

                    logger.warning(
                        f"Streaming failed on {model}: {exc}"
                    )

                    if self.scheduler.should_retry(
                        attempt
                    ):
                        time.sleep(
                            settings.LLM_RETRY_DELAY
                        )

        logger.error(
            f"Streaming exhausted all models: {last_error}"
        )

        raise ModelUnavailableError(
            f"Streaming failed: {last_error}"
        )

    # ========================================================================
    # Embedding Methods
    # ========================================================================

    def embed(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:
        """
        Generate embedding for single text.

        Args:
            request: EmbeddingRequest with text and optional model

        Returns:
            EmbeddingResponse with vector and metadata

        Raises:
            AllKeysExhaustedError: All keys failed
            ModelUnavailableError: Embedding generation failed
        """
        logger.info(
            f"Embedding text (length={len(request.text)}) "
            f"with model={request.model or settings.EMBEDDING_MODEL}"
        )

        metrics.record_request()
        start_time = time.time()
        last_error: Exception | None = None

        model = request.model or settings.EMBEDDING_MODEL

        for attempt in range(settings.LLM_MAX_RETRIES):
            try:
                api_key, key_index = self._get_available_key()

                client = self._get_client(api_key)

                logger.debug(
                    f"Calling embedding API (key {key_index})"
                )

                embedding_response = client.models.embed_content(
                    model=model,
                    contents=request.text,
                )

                latency_ms = (time.time() - start_time) * 1000
                self._record_success(key_index, latency_ms)

                logger.info(
                    f"Embedding generated: "
                    f"dimension={len(embedding_response.embedding)}, "
                    f"latency={latency_ms:.2f}ms"
                )

                return EmbeddingResponse(
                    vector=embedding_response.embedding,
                    model_used=model,
                    latency_ms=latency_ms,
                )

            except Exception as exc:
                last_error = exc
                self._record_failure()

                logger.warning(
                    f"Embedding failed (attempt {attempt + 1}): {exc}"
                )

                if attempt < settings.LLM_MAX_RETRIES - 1:
                    time.sleep(settings.LLM_RETRY_DELAY)

        logger.error(f"Embedding exhausted retries: {last_error}")
        raise ModelUnavailableError(
            f"Embedding generation failed: {last_error}"
        )

    def embed_query(self, query: str) -> list[float]:
        """
        Generate embedding for a query string.

        Convenience method wrapping embed().

        Args:
            query: Text to embed

        Returns:
            Embedding vector as list of floats

        Raises:
            ModelUnavailableError: Embedding generation failed
        """
        logger.debug(f"Embedding query (length={len(query)})")

        request = EmbeddingRequest(
            text=query,
            model=settings.EMBEDDING_MODEL,
        )

        # Correct indentation within logic block
        response = self.embed(request)

        return response.vector

    # ========================================================================
    # Health & Status Methods
    # ========================================================================

    def health(self) -> LLMHealth:
        """
        Get health status of Gemini client.

        Includes:
        - Available models from scheduler
        - Active/total API key count
        - Key cooldown status
        - Scheduler configuration
        - Model assignments

        Returns:
            LLMHealth with complete status information
        """
        logger.debug("Checking Gemini client health")

        key_statuses = self.key_manager.status()
        active_keys = sum(1 for k in key_statuses if k.active)

        logger.info(
            f"Health check: {active_keys}/{len(key_statuses)} "
            f"keys active"
        )

        return LLMHealth(
            available_models=[
                self.scheduler.primary,
                self.scheduler.fallback,
                self.scheduler.fast,
            ],
            active_keys=active_keys,
            total_keys=len(key_statuses),
            scheduler="round_robin",
            embedding_model=settings.EMBEDDING_MODEL,
            chat_model=self.scheduler.primary,
        )

    # ========================================================================
    # Internal Helper Methods
    # ========================================================================

    def _get_available_key(self) -> tuple[str, int]:
        """
        Get next available API key with rotation and cooldown.

        Blocks until a key is available if all are cooling down.

        Returns:
            Tuple of (api_key, key_index)

        Raises:
            AllKeysExhaustedError: All keys exhausted permanently
        """
        try:
            api_key, key_index = self.key_manager.get_key()
            logger.debug(f"Got API key at index {key_index}")
            return api_key, key_index

        except AllKeysExhaustedError:
            logger.warning(
                "All keys cooling down. Waiting for availability..."
            )
            self.key_manager.wait_until_available()
            return self.key_manager.get_key()

    def _get_client(self, api_key: str) -> genai.Client:
        """
        Get or create cached genai.Client for API key.

        Caches one client per unique API key to reuse HTTP connections.

        Args:
            api_key: Gemini API key

        Returns:
            Cached or newly created genai.Client
        """
        if api_key not in self._client_cache:
            logger.debug(f"Creating new Gemini client (cache miss)")
            self._client_cache[api_key] = genai.Client(
                api_key=api_key
            )

        return self._client_cache[api_key]

    def _execute_with_retry(
        self,
        api_key: str,
        key_index: int,
        model: str,
        request: LLMRequest,
        attempt: int,
    ) -> GenerateContentResponse:
        """
        Execute one Gemini request.
        """

        client = self._get_client(api_key)

        logger.debug(
            f"Building request for {model} "
            f"(attempt {attempt + 1})"
        )

        contents = self._build_content_parts(
            request
        )

        generation_config = (
            self._build_generation_config(
                request
            )
        )

        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generation_config,
        )

        logger.debug(
            f"Received response from {model}"
        )

        return response

    def _build_content_parts(
        self,
        request: LLMRequest,
    ) -> list[dict[str, Any]]:
        """
        Build Gemini conversation.
        """

        contents: list[dict[str, Any]] = []

        for message in request.messages:

            contents.append(
                {
                    "role": message.role,
                    "parts": [
                        {
                            "text": message.content,
                        }
                    ],
                }
            )

        contents.append(
            {
                "role": "user",
                "parts": [
                    {
                        "text": request.user_prompt,
                    }
                ],
            }
        )

        return contents

    def _build_generation_config(
        self,
        request: LLMRequest,
    ) -> types.GenerateContentConfig:
        """
        Build GenerateContentConfig.
        """

        config = request.config

        generation_config = (
            types.GenerateContentConfig(
                temperature=config.temperature,
                top_p=config.top_p,
                top_k=config.top_k,
                max_output_tokens=config.max_output_tokens,
                candidate_count=config.candidate_count,
            )
        )

        if config.stop_sequences:
            generation_config.stop_sequences = (
                config.stop_sequences
            )

        if request.system_prompt:
            generation_config.system_instruction = (
                request.system_prompt
            )

        if request.response_schema:
            generation_config.response_mime_type = (
                "application/json"
            )
            generation_config.response_schema = (
                request.response_schema
            )

        return generation_config

    def _parse_response(
        self,
        response: GenerateContentResponse,
        model: str,
        key_index: int,
        latency_ms: float,
    ) -> LLMResponse:
        """
        Parse Gemini API response into LLMResponse.

        Extracts:
        - Text content
        - Token usage statistics
        - Model and key metadata

        Args:
            response: GenerateContentResponse from API
            model: Model name used
            key_index: API key index
            latency_ms: Request latency

        Returns:
            Structured LLMResponse

        Raises:
            LLMException: Response parsing failed
        """
        try:
            logger.debug(f"Parsing response from {model}")

            text = response.text or ""

            # Extract usage stats if available
            usage = TokenUsage()
            if hasattr(response, "usage_metadata"):
                meta = response.usage_metadata
                usage.prompt_tokens = meta.prompt_token_count
                usage.completion_tokens = meta.candidates_token_count
                usage.total_tokens = meta.total_token_count

                logger.debug(
                    f"Usage: prompt={usage.prompt_tokens}, "
                    f"completion={usage.completion_tokens}"
                )

            return LLMResponse(
                text=text,
                raw=response,
                model_used=model,
                key_index=key_index,
                latency_ms=latency_ms,
                usage=usage,
            )

        except Exception as exc:
            logger.error(f"Failed to parse response: {exc}")
            raise LLMException(f"Response parsing failed: {exc}") from exc

    def _extract_json(self, text: str) -> dict[str, Any]:
        """
        Extract JSON from text response.

        Handles:
        - Raw JSON responses
        - JSON wrapped in markdown code blocks
        - JSON with surrounding text

        Args:
            text: Response text potentially containing JSON

        Returns:
            Parsed JSON as dictionary

        Raises:
            json.JSONDecodeError: Invalid or missing JSON
        """
        logger.debug("Extracting JSON from response")

        text = text.strip()

        # Try raw JSON first
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try markdown code block
        if "```json" in text:
            start = text.find("```json") + 7
            end = text.find("```", start)
            if end > start:
                json_text = text[start:end].strip()
                logger.debug("Found JSON in markdown code block")
                return json.loads(json_text)

        if "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            if end > start:
                json_text = text[start:end].strip()
                logger.debug("Found JSON in code block")
                return json.loads(json_text)

        logger.error("No valid JSON found in response")
        raise json.JSONDecodeError(
            "No JSON found in response",
            text,
            0,
        )

    def _record_success(
        self,
        key_index: int,
        latency_ms: float,
    ) -> None:
        """
        Record successful request.

        Updates:
        - Key manager (reset failures, clear cooldown)
        - Metrics (increment success, add latency)

        Args:
            key_index: Index of API key used
            latency_ms: Request latency in milliseconds
        """
        self.key_manager.mark_success(key_index)
        metrics.record_success(latency_ms)

        logger.debug(
            f"Recorded success: key {key_index}, "
            f"latency {latency_ms:.2f}ms"
        )

    def _record_failure(self) -> None:
        """
        Record failed request.

        Updates:
        - Metrics (increment failures)

        Note: Key failures are marked in _execute_with_retry
        by the caller to attach key_index.
        """
        metrics.record_failure()
        logger.debug("Recorded failure")