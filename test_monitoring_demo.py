import json
import time
from app.monitoring import MetricsCollector, RequestTimer, get_logger

logger = get_logger()
metrics = MetricsCollector()

print("=== STRUCTURED LOGGING ===")
print()
logger.info("Application starting")

# Testing dictionary metadata structures mapping inside the JSONFormatter
logger.info(
    "Processing request",
    extra={"extra_data": {"user_id": "user-123", "thread_id": "thread-abc"}},
)
logger.warning(
    "Rate limit approaching",
    extra={"extra_data": {"current_rate": 18, "limit": 20}},
)

print()
print("=== METRICS COLLECTION ===")
print()

# Simulate Request 1 (Standard execution flow)
with RequestTimer() as timer:
    time.sleep(0.1)  # Simulate model latency processing work
metrics.record_request(
    latency_ms=timer.elapsed_ms, input_tokens=50, output_tokens=100
)
print(f"Request 1: {timer.elapsed_ms:.1f}ms")

# Simulate Request 2 (Cache Hit execution flow)
with RequestTimer() as timer:
    time.sleep(0.05)  # Faster block lookup execution
metrics.record_request(
    latency_ms=timer.elapsed_ms,
    input_tokens=30,
    output_tokens=80,
    cache_hit=True,
)
print(f"Request 2: {timer.elapsed_ms:.1f}ms (cache hit)")

# Simulate Request 3 (System Failure Endpoint Exception)
metrics.record_request(latency_ms=5.0, error=True)
print("Request 3: error")

print()
print("=== METRICS SUMMARY ===")
print(json.dumps(metrics.summary, indent=2))