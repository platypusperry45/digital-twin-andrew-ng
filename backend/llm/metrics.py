"""
Thread-safe LLM telemetry.

Collects runtime metrics for:

- Requests
- Success / failure
- Retry count
- Latency
- Streaming
- Embeddings
- Structured outputs
- Cache efficiency
- Model fallbacks
- API key switches
"""

from __future__ import annotations

import threading
from dataclasses import dataclass


@dataclass(slots=True)
class _MetricsState:

    requests: int = 0

    successes: int = 0

    failures: int = 0

    retries: int = 0

    embeddings: int = 0

    streams: int = 0

    structured: int = 0

    cache_hits: int = 0

    cache_misses: int = 0

    key_switches: int = 0

    model_fallbacks: int = 0

    total_latency_ms: float = 0.0


class Metrics:

    """
    Thread-safe runtime metrics.
    """

    def __init__(self):

        self._lock = threading.Lock()

        self._state = _MetricsState()

    # ==========================================================
    # Recording
    # ==========================================================

    def record_request(self):

        with self._lock:

            self._state.requests += 1

    def record_success(
        self,
        latency_ms: float,
    ):

        with self._lock:

            self._state.successes += 1

            self._state.total_latency_ms += latency_ms

    def record_failure(self):

        with self._lock:

            self._state.failures += 1

    def record_retry(self):

        with self._lock:

            self._state.retries += 1

    def record_embedding(self):

        with self._lock:

            self._state.embeddings += 1

    def record_stream(self):

        with self._lock:

            self._state.streams += 1

    def record_structured(self):

        with self._lock:

            self._state.structured += 1

    def record_cache_hit(self):

        with self._lock:

            self._state.cache_hits += 1

    def record_cache_miss(self):

        with self._lock:

            self._state.cache_misses += 1

    def record_key_switch(self):

        with self._lock:

            self._state.key_switches += 1

    def record_model_fallback(self):

        with self._lock:

            self._state.model_fallbacks += 1

    # ==========================================================
    # Utilities
    # ==========================================================

    def reset(self):

        with self._lock:

            self._state = _MetricsState()

    def summary(self) -> dict:

        with self._lock:

            state = self._state

            average_latency = 0.0

            if state.successes:

                average_latency = (
                    state.total_latency_ms
                    / state.successes
                )

            total_cache = (
                state.cache_hits
                + state.cache_misses
            )

            cache_hit_rate = 0.0

            if total_cache:

                cache_hit_rate = (
                    state.cache_hits
                    / total_cache
                )

            success_rate = 0.0

            if state.requests:

                success_rate = (
                    state.successes
                    / state.requests
                )

            return {

                "requests": state.requests,

                "successes": state.successes,

                "failures": state.failures,

                "success_rate": round(
                    success_rate,
                    4,
                ),

                "retries": state.retries,

                "embeddings": state.embeddings,

                "streams": state.streams,

                "structured": state.structured,

                "cache_hits": state.cache_hits,

                "cache_misses": state.cache_misses,

                "cache_hit_rate": round(
                    cache_hit_rate,
                    4,
                ),

                "key_switches": state.key_switches,

                "model_fallbacks": state.model_fallbacks,

                "average_latency_ms": round(
                    average_latency,
                    2,
                ),

            }


metrics = Metrics()