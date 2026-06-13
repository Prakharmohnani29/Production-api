from datetime import datetime, timezone
from functools import wraps
import json
import logging
import time
from typing import Any, Callable


class JSONFormatter(logging.Formatter):
    """Format log records as JSON for log aggregation (ELK, Datadog, etc.)."""

    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }

        if hasattr(record, "extra_data"):
            log_obj.update(record.extra_data)

        return json.dumps(log_obj)


def get_logger(name: str = "production-api") -> logging.Logger:
    """Create a structured JSON logger."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger


class MetricsCollector:
    """Collects and aggregates application metrics."""

    def __init__(self):
        self._requests_total = 0
        self._errors_total = 0
        self._latency_sum = 0.0
        self._latency_count = 0
        self._tokens_input = 0
        self._tokens_output = 0
        self._cache_hits = 0
        self._cache_misses = 0

    def record_request(
        self,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        error: bool = False,
        cache_hit: bool = False,
    ) -> None:
        """Record performance and usage metrics for a request execution."""
        self._requests_total += 1
        if error:
            self._errors_total += 1

        self._latency_sum += latency_ms
        self._latency_count += 1

        self._tokens_input += input_tokens
        self._tokens_output += output_tokens

        if cache_hit:
            self._cache_hits += 1
        else:
            self._cache_misses += 1

    @property
    def summary(self) -> dict:
        """Return aggregated operational metrics telemetry."""
        avg_latency = (
            self._latency_sum / self._latency_count
            if self._latency_count > 0
            else 0.0
        )
        return {
            "requests_total": self._requests_total,
            "errors_total": self._errors_total,
            "avg_latency_ms": round(avg_latency, 2),
            "tokens_consumed": {
                "input": self._tokens_input,
                "output": self._tokens_output,
                "total": self._tokens_input + self._tokens_output,
            },
            "cache_telemetry": {
                "hits": self._cache_hits,
                "misses": self._cache_misses,
                "hit_rate": (
                    f"{(self._cache_hits / (self._cache_hits + self._cache_misses)):.1%}"
                    if (self._cache_hits + self._cache_misses) > 0
                    else "0.0%"
                ),
            },
        }


class RequestTimer:
    """Context manager to measure code block and API routing execution latencies."""

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed_ms = (time.time() - self.start) * 1000