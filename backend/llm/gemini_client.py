"""
Production-grade Gemini API Client for the Andrew Ng Digital Twin platform.

Responsibilities:
- Thread-safe HTTP Client lifecycle resource re-use using localized threading locks.
- Advanced retry engine featuring exponential backoff, random uniform jitter, and retry budgets.
- Selective status error filtering recognizing distinct transient vs terminal exception patterns.
- Robust cascade structural data extractor utilizing balanced bracket parsing logic.
- Comprehensive safety enforcement auditing response level prompt feedbacks and candidate ratings.
- Transparent telemetry capturing fine-grained operations metrics parameters.

Compatible with:
- Python 3.13
- google-genai==1.30.0
- Pydantic v2
- FastAPI
"""

from __future__ import annotations

import copy
import json
import time
import random
import uuid
import re
import threading
from typing import Any, Generator, Optional, Type, TypeVar, Dict, List, Tuple

from google import genai
from google.genai import types
from google.genai.errors import APIError
from google.genai.types import GenerateContentResponse
from pydantic import BaseModel, ValidationError

from backend.core.config import settings
from backend.core.logger import logger

from backend.llm.exceptions import (
    LLMException,
    ModelUnavailableError,
    AllKeysExhaustedError,
    RateLimitError,
    SafetyBlockedError,
    StructuredOutputError,
    RetryableLLMError,
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
    Principal interface managing multi-turn text generation, structured JSON mode parsing,
    and high-throughput vector embedding requests using the modern Google GenAI SDK framework.
    """

    def __init__(self) -> None:
        """
        Initializes backend dependencies allocating atomic lock parameters managing cross-thread connection caches structures.
        """
        if not getattr(settings, "GEMINI_API_KEYS", None):
            raise ValueError(
                "No Gemini API keys configured. Set GEMINI_API_KEYS in environment."
            )

        cooldown_val = getattr(settings, "KEY_COOLDOWN_SECONDS", 60.0)
        self.key_manager = KeyManager(
            settings.GEMINI_API_KEYS,
            cooldown_val,
        )

        self.scheduler = LLMScheduler()

        # Core thread-safe connection mapping elements
        self._client_cache: Dict[str, genai.Client] = {}
        self._lock = threading.Lock()
        
        # Precomputed immutable configuration parameters cache tracking layer
        self._config_cache: Dict[str, types.GenerateContentConfig] = {}
        self._config_lock = threading.Lock()

        logger.info(
            f"Gemini client initialized successfully with {len(settings.GEMINI_API_KEYS)} managed keys."
        )

    # ========================================================================
    # Core Generation Methods
    # ========================================================================

    def generate(self, request: LLMRequest) -> LLMResponse:
        """
        Generate complete text returns, supporting dynamic fallbacks, backoff limits, and runtime validation metrics.
        
        Args:
            request: Unified request configuration wrapper containing message sequence parameters.
            
        Returns:
            Structured LLMResponse entity detailing output contents and resource tracking usage.
            
        Raises:
            ModelUnavailableError: If all fallback models and retries are exhausted.
            SafetyBlockedError: If explicit content filtration boundaries trigger rejection parameters.
            RateLimitError: If explicit provider request volumes exhaust threshold limits.
            LLMException: For terminal orchestration infrastructure issues.
        """
        req_id = str(uuid.uuid4())
        metrics.record_request()
        start_time = time.time()
        
        last_error: Optional[Exception] = None
        current_key_index: Optional[int] = None
        cumulative_retries = 0

        model_sequence: List[str] = self.scheduler.get_model_sequence(request.model)
        primary_model = model_sequence[0] if model_sequence else request.model

        contents = self._build_content_parts(request)
        generation_config = self._build_generation_config(request)

        logger.info(
            f"[LLM_REQ_START] id={req_id} model={request.model} historical_turns={len(request.messages)}"
        )

        for model in model_sequence:
            if model != primary_model:
                metrics.record_model_fallback()
                logger.warning(f"[LLM_FALLBACK] id={req_id} switching target model to candidate={model}")

            max_retries = getattr(settings, "LLM_MAX_RETRIES", 3)
            for attempt in range(max_retries):
                try:
                    while True:
                        try:
                            api_key, key_index = self._get_available_key()
                            break
                        except AllKeysExhaustedError:
                            logger.warning(f"[LLM_KEY_EXHAUSTION] id={req_id} All keys are cooling down. Blocking thread until key becomes available.")
                            self.key_manager.wait_until_available()
                    
                    if current_key_index is not None and current_key_index != key_index:
                        metrics.record_key_switch()
                        logger.info(f"[LLM_KEY_SWITCH] id={req_id} rotating index from {current_key_index} to {key_index}")
                    current_key_index = key_index

                    if attempt > 0:
                        metrics.record_retry()
                        cumulative_retries += 1
                        
                        base_delay = getattr(settings, "LLM_RETRY_DELAY", 1.0)
                        calculated_delay = base_delay * (2 ** (attempt - 1)) + random.uniform(0.1, 0.4)
                        logger.info(f"[LLM_RETRY_BACKOFF] id={req_id} attempt={attempt} code={getattr(last_error, 'code', 'UNKNOWN')} sleeping duration={calculated_delay:.2f}s before attempt={attempt+1}")
                        time.sleep(calculated_delay)

                    client = self._get_client(api_key)
                    
                    logger.debug(f"Calling generate_content id={req_id} model={model} key={key_index} attempt={attempt+1}")
                    raw_response = client.models.generate_content(
                        model=model,
                        contents=contents,
                        config=generation_config,
                    )

                    self._assert_response_safety(raw_response, req_id)

                    latency_ms = (time.time() - start_time) * 1000
                    self._record_success(key_index, latency_ms)

                    parsed_response = self._parse_response(
                        response=raw_response,
                        model=model,
                        key_index=key_index,
                        latency_ms=latency_ms,
                    )
                    parsed_response.request_id = req_id
                    parsed_response.retry_count = cumulative_retries

                    logger.info(
                        f"[LLM_REQ_SUCCESS] id={req_id} resolved_model={model} "
                        f"latency={latency_ms:.2f}ms finish_reason={parsed_response.finish_reason}"
                    )
                    return parsed_response

                except AllKeysExhaustedError as ake:
                    raise ake
                except APIError as api_exc:
                    last_error = api_exc
                    if current_key_index is not None:
                        self.key_manager.mark_failure(current_key_index)
                    self._record_failure()

                    if api_exc.code == 429:
                        logger.warning(f"[LLM_RATE_LIMIT] id={req_id} code=429 key_index={current_key_index} marked for immediate rotation.")
                        continue

                    if not self._is_retryable_http_code(api_exc.code):
                        logger.error(f"[LLM_TERMINAL_API_ERROR] id={req_id} status={api_exc.code} msg={api_exc.message}")
                        self._raise_specific_exception(api_exc)

                    logger.warning(f"[LLM_RETRYABLE_API_ERROR] id={req_id} message={api_exc.message} triggering backoff retry loop iteration.")

                except (SafetyBlockedError, StructuredOutputError) as strict_exc:
                    last_error = strict_exc
                    if current_key_index is not None:
                        self.key_manager.mark_failure(current_key_index)
                    self._record_failure()
                    logger.error(f"[LLM_TERMINAL_CRITERIA_ERROR] id={req_id} description={str(strict_exc)}")
                    raise strict_exc

                except Exception as generic_exc:
                    last_error = generic_exc
                    if current_key_index is not None:
                        self.key_manager.mark_failure(current_key_index)
                    self._record_failure()
                    logger.warning(f"[LLM_GENERIC_INTERNAL_ERROR] id={req_id} exception={type(generic_exc).__name__} msg={str(generic_exc)}")

        logger.error(f"[LLM_EXHAUSTED_ERROR] id={req_id} execution metrics completely failed. Final trace={str(last_error)}")
        raise ModelUnavailableError(f"Generation completely failed across execution tiers chain routes: {str(last_error)}")

    def generate_structured(
        self,
        request: LLMRequest,
        response_schema: Type[T],
    ) -> T:
        """
        Executes generation parameters applying parsing filters that unpack structured objects bound onto explicit target input structural schemas.
        """
        metrics.record_structured()
        
        request_copy = request.model_copy()
        request_copy.response_schema = response_schema
        
        max_structured_attempts = 3
        last_extraction_error: Optional[Exception] = None

        for attempt in range(max_structured_attempts):
            try:
                response = self.generate(request_copy)
                extracted_dict = self._extract_json(response.text)
                validated_model = response_schema.model_validate(extracted_dict)
                return validated_model
            except (ValidationError, json.JSONDecodeError) as exc:
                last_extraction_error = exc
                logger.warning(
                    f"[LLM_STRUCTURED_RETRY] Validation step failed "
                    f"attempt={attempt+1}/{max_structured_attempts}: {str(exc)}"
                )
                if attempt < max_structured_attempts - 1:
                    time.sleep(getattr(settings, "LLM_RETRY_DELAY", 1.0))
        
        raise StructuredOutputError(
            f"Failed validating output structure targeting schema model class '{response_schema.__name__}' "
            f"after total allocation limits attempts: {str(last_extraction_error)}"
        )

    def stream(
        self,
        request: LLMRequest,
    ) -> Generator[str, None, None]:
        """
        Streams incremental chunk pieces, maintaining robust connectivity handling throughout operation cycles lifetimes.
        """
        req_id = str(uuid.uuid4())
        metrics.record_stream()
        metrics.record_request()
        
        start_time = time.time()
        last_error: Optional[Exception] = None
        current_key_index: Optional[int] = None

        model_sequence = self.scheduler.get_model_sequence(request.model)
        primary_model = model_sequence[0] if model_sequence else request.model

        contents = self._build_content_parts(request)
        generation_config = self._build_generation_config(request)

        logger.info(f"[LLM_STREAM_START] id={req_id} model={request.model}")

        for model in model_sequence:
            if model != primary_model:
                metrics.record_model_fallback()
                logger.warning(f"[LLM_STREAM_FALLBACK] id={req_id} shifting target stream model to candidate={model}")

            max_retries = getattr(settings, "LLM_MAX_RETRIES", 3)
            for attempt in range(max_retries):
                try:
                    while True:
                        try:
                            api_key, key_index = self._get_available_key()
                            break
                        except AllKeysExhaustedError:
                            logger.warning(f"[LLM_STREAM_KEY_EXHAUSTION] id={req_id} All keys are cooling down. Blocking thread until key becomes available.")
                            self.key_manager.wait_until_available()
                    
                    if current_key_index is not None and current_key_index != key_index:
                        metrics.record_key_switch()
                    current_key_index = key_index

                    if attempt > 0:
                        metrics.record_retry()
                        base_delay = getattr(settings, "LLM_RETRY_DELAY", 1.0)
                        calculated_delay = base_delay * (2 ** (attempt - 1)) + random.uniform(0.1, 0.4)
                        logger.info(f"[LLM_STREAM_RETRY_BACKOFF] id={req_id} attempt={attempt} code={getattr(last_error, 'code', 'UNKNOWN')} sleeping duration={calculated_delay:.2f}s before attempt={attempt+1}")
                        time.sleep(calculated_delay)

                    client = self._get_client(api_key)
                    stream_response = client.models.generate_content(
                        model=model,
                        contents=contents,
                        config=generation_config,
                        stream=True,
                    )

                    chunk_count = 0
                    for chunk in stream_response:
                        self._assert_response_safety(chunk, req_id)
                        chunk_text = getattr(chunk, "text", "")
                        if chunk_text:
                            chunk_count += 1
                            yield chunk_text

                    latency_ms = (time.time() - start_time) * 1000
                    self._record_success(key_index, latency_ms)
                    logger.info(f"[LLM_STREAM_SUCCESS] id={req_id} complete chunks_count={chunk_count} total_latency={latency_ms:.2f}ms")
                    return

                except AllKeysExhaustedError as ake:
                    raise ake
                except (APIError, SafetyBlockedError, Exception) as stream_exc:
                    last_error = stream_exc
                    if current_key_index is not None:
                        self.key_manager.mark_failure(current_key_index)
                    self._record_failure()
                    
                    if isinstance(stream_exc, SafetyBlockedError):
                        logger.error(f"[LLM_STREAM_SAFETY_BLOCKED] id={req_id} description={str(stream_exc)}")
                        raise stream_exc
                    
                    if isinstance(stream_exc, APIError):
                        if stream_exc.code == 429:
                            continue
                        if self._is_retryable_http_code(stream_exc.code):
                            continue
                        self._raise_specific_exception(stream_exc)
                    
                    logger.warning(f"[LLM_STREAM_RETRY_ERR] id={req_id} error={str(stream_exc)}")

        raise ModelUnavailableError(f"Streaming execution path completely failed exhaustion limits tracking: {str(last_error)}")

    # ========================================================================
    # Embedding Methods
    # ========================================================================

    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        """
        Generates embedding multi-dimensional float arrays targeting data pipelines calculation frames processing needs.
        """
        metrics.record_embedding()
        metrics.record_request()
        
        start_time = time.time()
        last_error: Optional[Exception] = None
        current_key_index: Optional[int] = None

        model = request.model or getattr(settings, "EMBEDDING_MODEL", "text-embedding-004")
        logger.info(f"[LLM_EMBED_START] model={model} length_chars={len(request.text)}")

        max_retries = getattr(settings, "LLM_MAX_RETRIES", 3)
        for attempt in range(max_retries):
            try:
                while True:
                    try:
                        api_key, key_index = self._get_available_key()
                        break
                    except AllKeysExhaustedError:
                        logger.warning(f"[LLM_EMBED_KEY_EXHAUSTION] All keys are cooling down. Blocking thread until key becomes available.")
                        self.key_manager.wait_until_available()
                
                if current_key_index is not None and current_key_index != key_index:
                    metrics.record_key_switch()
                current_key_index = key_index

                if attempt > 0:
                    metrics.record_retry()
                    base_delay = getattr(settings, "LLM_RETRY_DELAY", 1.0)
                    calculated_delay = base_delay * (2 ** (attempt - 1)) + random.uniform(0.1, 0.4)
                    logger.info(f"[LLM_EMBED_RETRY_BACKOFF] attempt={attempt} code={getattr(last_error, 'code', 'UNKNOWN')} sleeping duration={calculated_delay:.2f}s before attempt={attempt+1}")
                    time.sleep(calculated_delay)

                client = self._get_client(api_key)
                raw_embed_res = client.models.embed_content(
                    model=model,
                    contents=request.text,
                )

                vector_output: Optional[List[float]] = None
                
                if hasattr(raw_embed_res, "embedding") and raw_embed_res.embedding is not None:
                    emb_obj = raw_embed_res.embedding
                    if hasattr(emb_obj, "values") and isinstance(emb_obj.values, list):
                        vector_output = emb_obj.values
                    elif isinstance(emb_obj, list):
                        vector_output = emb_obj

                if vector_output is None and hasattr(raw_embed_res, "embeddings") and isinstance(raw_embed_res.embeddings, list) and len(raw_embed_res.embeddings) > 0:
                    first_elem = raw_embed_res.embeddings[0]
                    if hasattr(first_elem, "values") and isinstance(first_elem.values, list):
                        vector_output = first_elem.values
                    elif isinstance(first_elem, list):
                        vector_output = first_elem

                if vector_output is None:
                    logger.error("Extracted structural embedding components resolved to completely null matrix states unexpectedly.")
                    raise LLMException("Malformed response structural payload metadata returned from downstream embedding models systems.")

                if len(vector_output) == 0 or not all(isinstance(val, (int, float)) for val in vector_output):
                    raise LLMException("Malformed response payload: embedding array contained non-numeric or empty instances parameters.")

                latency_ms = (time.time() - start_time) * 1000
                self._record_success(key_index, latency_ms)

                logger.info(f"[LLM_EMBED_SUCCESS] dimensions={len(vector_output)} latency={latency_ms:.2f}ms")
                return EmbeddingResponse(
                    vector=vector_output,
                    model_used=model,
                    latency_ms=latency_ms
                )

            except AllKeysExhaustedError as ake:
                raise ake
            except APIError as api_exc:
                last_error = api_exc
                if current_key_index is not None:
                    self.key_manager.mark_failure(current_key_index)
                self._record_failure()
                if not self._is_retryable_http_code(api_exc.code):
                    self._raise_specific_exception(api_exc)

            except Exception as generic_exc:
                last_error = generic_exc
                if current_key_index is not None:
                    self.key_manager.mark_failure(current_key_index)
                self._record_failure()
                logger.warning(f"Embedding generation attempt error trace generated: {str(generic_exc)}")

        raise ModelUnavailableError(f"Embedding vector extraction failed execution sequence logic loop thresholds: {str(last_error)}")

    def embed_query(self, query: str) -> List[float]:
        """
        Convenience execution shortcut converting plain query strings directly into primitive numerical float lists.
        """
        request = EmbeddingRequest(
            text=query,
            model=getattr(settings, "EMBEDDING_MODEL", "text-embedding-004")
        )
        return self.embed(request).vector

    # ========================================================================
    # Health & Status Methods
    # ========================================================================

    def health(self) -> LLMHealth:
        """
        Returns full monitoring diagnostics aggregating telemetry cache indicators context maps.
        """
        with self._lock:
            cached_count = len(self._client_cache)

        key_statuses_data = self.key_manager.status()
        active_keys_count = sum(1 for status in key_statuses_data if status.active)
        summary_metrics = metrics.summary()

        return LLMHealth(
            available_models=[
                self.scheduler.primary,
                self.scheduler.fast,
                self.scheduler.fallback,
            ],
            cached_clients=cached_count,
            active_keys=active_keys_count,
            total_keys=len(key_statuses_data),
            key_statuses=key_statuses_data,
            metrics_summary=summary_metrics,
            scheduler_mode="resilient_cascading_fallback",
            embedding_model=getattr(settings, "EMBEDDING_MODEL", "text-embedding-004"),
            chat_model=self.scheduler.primary,
        )

    # ========================================================================
    # Internal Helper Methods
    # ========================================================================

    def _get_available_key(self) -> Tuple[str, int]:
        """Fetches active key references via tracking proxies encapsulation routines."""
        return self.key_manager.get_key()

    def _get_client(self, api_key: str) -> genai.Client:
        """ Thread-safe connection cache lookup manager minimizing invocation bottlenecks securely. """
        with self._lock:
            if api_key not in self._client_cache:
                metrics.record_cache_miss()
                self._client_cache[api_key] = genai.Client(api_key=api_key)
            else:
                metrics.record_cache_hit()
            return self._client_cache[api_key]

    def _execute_with_retry(
        self,
        api_key: str,
        key_index: int,
        model: str,
        request: LLMRequest,
        attempt: int,
    ) -> GenerateContentResponse:
        """ Legacy internal routing capability hook maintaining absolute backwards signature runtime code compatibility. """
        client = self._get_client(api_key)
        contents = self._build_content_parts(request)
        generation_config = self._build_generation_config(request)
        return client.models.generate_content(
            model=model,
            contents=contents,
            config=generation_config,
        )

    def _build_content_parts(self, request: LLMRequest) -> List[Dict[str, Any]]:
        """ Unpacks explicit structural models arrays passing content body maps accurately down to SDK network modules layer templates. """
        contents: List[Dict[str, Any]] = []
        for msg in request.messages:
            contents.append({
                "role": msg.role,
                "parts": [{"text": msg.content}]
            })
        contents.append({
            "role": "user",
            "parts": [{"text": request.user_prompt}]
        })
        return contents

    def _build_generation_config(self, request: LLMRequest) -> types.GenerateContentConfig:
        """ Unpacks request parameters into pre-allocated immutable structural definition wrappers. """
        cfg = request.config
        
        sys_prompt_str = request.system_prompt or ""
        schema_name = request.response_schema.__name__ if request.response_schema else "None"
        cache_key = (
            f"t={cfg.temperature}:p={cfg.top_p}:k={cfg.top_k}:m={cfg.max_output_tokens}:"
            f"c={cfg.candidate_count}:s={','.join(cfg.stop_sequences or [])}:"
            f"sys={sys_prompt_str}:sch={schema_name}"
        )
        
        with self._config_lock:
            if cache_key in self._config_cache:
                return copy.deepcopy(self._config_cache[cache_key])

        generation_config = types.GenerateContentConfig(
            temperature=cfg.temperature,
            top_p=cfg.top_p,
            top_k=cfg.top_k,
            max_output_tokens=cfg.max_output_tokens,
            candidate_count=cfg.candidate_count,
        )

        if cfg.stop_sequences:
            generation_config.stop_sequences = cfg.stop_sequences

        if request.system_prompt:
            generation_config.system_instruction = request.system_prompt

        if request.response_schema:
            generation_config.response_mime_type = "application/json"
            generation_config.response_schema = request.response_schema

        with self._config_lock:
            if len(self._config_cache) > 128:
                self._config_cache.clear()
            self._config_cache[cache_key] = generation_config
            return copy.deepcopy(generation_config)

    def _assert_response_safety(self, response: GenerateContentResponse, req_id: str) -> None:
        """
        Deep structural safety validation checking prompt feedbacks and individual candidate rating items fields.
        """
        prompt_feedback = getattr(response, "prompt_feedback", None)
        if prompt_feedback:
            block_reason = getattr(prompt_feedback, "block_reason", None)
            if block_reason and str(block_reason) != "BLOCKED_REASON_UNSPECIFIED" and str(block_reason) != "None":
                raise SafetyBlockedError(
                    message=f"Gemini API prompt verification rejected target contents: {block_reason}",
                    blocked_reason=str(block_reason)
                )

        candidates = getattr(response, "candidates", None)
        if candidates and len(candidates) > 0:
            first_candidate = candidates[0]
            
            safety_ratings = getattr(first_candidate, "safety_ratings", None)
            if safety_ratings:
                for rating in safety_ratings:
                    probability = getattr(rating, "probability", None)
                    if probability and str(probability) == "HIGH":
                        category = getattr(rating, "category", "UNKNOWN")
                        raise SafetyBlockedError(
                            message=f"Gemini candidate safety trigger violated: {category} status probability={probability}",
                            blocked_reason=f"Violated explicit category constraint {category}"
                        )

    def _parse_response(
        self,
        response: GenerateContentResponse,
        model: str,
        key_index: int,
        latency_ms: float,
    ) -> LLMResponse:
        """ Sanitizes response candidate parameters ensuring execution validity boundaries stand perfectly solid before consumption patterns begin. """
        candidates = getattr(response, "candidates", None)
        if not candidates or len(candidates) == 0:
            raise LLMException("Downstream server model integration layer evaluated back completely zero valid response candidates.")

        primary_candidate = candidates[0]
        finish_reason = getattr(primary_candidate, "finish_reason", "UNKNOWN")
        finish_reason_str = str(finish_reason) if finish_reason else "UNKNOWN"
        
        if finish_reason_str in ("SAFETY", "BLOCKLIST", "PROMPT_BLOCKED"):
            raise SafetyBlockedError(
                message=f"Generation transaction aborted. Block flag: {finish_reason_str}",
                blocked_reason=finish_reason_str
            )

        extracted_text = getattr(response, "text", None)
        if not extracted_text:
            content_obj = getattr(primary_candidate, "content", None)
            if content_obj and hasattr(content_obj, "parts") and content_obj.parts:
                part_texts = [getattr(p, "text", "") for p in content_obj.parts if getattr(p, "text", "")]
                extracted_text = "".join(part_texts)

        if not extracted_text:
            if finish_reason_str in ("STOP", "MAX_TOKENS"):
                raise LLMException(f"Model processing complete but textual content resolved completely blank. Finish Reason: {finish_reason_str}")
            else:
                raise LLMException(f"Unusable output resolved with underlying execution termination state flag: {finish_reason_str}")
        else:
            if finish_reason_str == "MAX_TOKENS":
                pass  # normal return since extracted_text contains valid data

        usage_metadata = getattr(response, "usage_metadata", None)
        
        p_tokens = getattr(usage_metadata, "prompt_token_count", 0)
        c_tokens = getattr(usage_metadata, "candidates_token_count", 0)
        t_tokens = getattr(usage_metadata, "total_token_count", 0)
        
        token_usage = TokenUsage(
            prompt_tokens=p_tokens if isinstance(p_tokens, int) else 0,
            completion_tokens=c_tokens if isinstance(c_tokens, int) else 0,
            total_tokens=t_tokens if isinstance(t_tokens, int) else 0
        )

        return LLMResponse(
            text=extracted_text,
            raw=response,
            model_used=model,
            key_index=key_index,
            latency_ms=latency_ms,
            usage=token_usage,
            finish_reason=finish_reason_str,
            cached=False
        )

    def _extract_json(self, text: str) -> Dict[str, Any]:
        """
        Robust cascade parser traversing alternate structural format combinations sequentially to isolate completely sanitized raw JSON blocks.
        """
        cleaned_text = text.strip()

        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            pass

        md_json_pattern = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)
        match = md_json_pattern.search(cleaned_text)
        if match:
            try:
                return json.loads(match.group(1).strip())
            except json.JSONDecodeError:
                pass

        first_brace_pos = cleaned_text.find("{")
        if first_brace_pos != -1:
            brace_stack_count = 0
            matching_closing_pos = -1
            for index in range(first_brace_pos, len(cleaned_text)):
                char = cleaned_text[index]
                if char == "{":
                    brace_stack_count += 1
                elif char == "}":
                    brace_stack_count -= 1
                    if brace_stack_count == 0:
                        matching_closing_pos = index
                        
                        sliced_bracket_string = cleaned_text[first_brace_pos : matching_closing_pos + 1]
                        try:
                            return json.loads(sliced_bracket_string)
                        except json.JSONDecodeError:
                            pass
                            
        logger.error(f"Unparseable structural target output textual data content trace encountered: {text}")
        raise json.JSONDecodeError("Failed to isolate valid parseable JSON parameters fields blocks elements structural markers definitions from response text.", text, 0)

    def _is_retryable_http_code(self, status_code: Optional[int]) -> bool:
        """ Matches error status designators against retryable operational matrices parameters. """
        if not status_code:
            return True
        return status_code in (429, 500, 502, 503, 504)

    def _raise_specific_exception(self, api_exc: APIError) -> None:
        """ Unpacks external error status footprints directly into corresponding explicit customized project class variants definitions. """
        code = api_exc.code
        if code in (400, 401):
            raise LLMException(f"Gemini API Error ({code}): {api_exc.message}", original_exception=api_exc)
        elif code == 403:
            raise SafetyBlockedError(f"Access denied or action blocked by safety policies ({code}): {api_exc.message}", original_exception=api_exc)
        elif code == 404:
            raise ModelUnavailableError(f"The requested model resource was not found ({code}): {api_exc.message}", original_exception=api_exc)
        elif code == 429:
            raise RateLimitError(f"API Rate Limit validation ceiling breached ({code}): {api_exc.message}", original_exception=api_exc)
        elif code in (500, 502, 503, 504):
            raise RetryableLLMError(f"Transient downstream server error encountered ({code}): {api_exc.message}", original_exception=api_exc)
        else:
            raise LLMException(f"Gemini API Platform pipeline runtime operation execution trace failure ({code}): {api_exc.message}", original_exception=api_exc)

    def _record_success(self, key_index: int, latency_ms: float) -> None:
        """ Commits success records metrics data blocks downstream to internal rotaters tracking components safely. """
        self.key_manager.mark_success(key_index)
        metrics.record_success(latency_ms)

    def _record_failure(self) -> None:
        """ Commits failures indicators globally. """
        metrics.record_failure()