import time
from app.cache import ResponseCache

# Initialize cache with a short 3-second TTL for testing expiration
cache = ResponseCache(ttl_seconds=3)

print("=== CACHE DEMO ===")
print()

# --- Cache Miss Scenario ---
result = cache.get("What is Python?")
print(f"f1. First lookup: {result} (miss - nothing cached yet)")

# --- Cache Store Scenario ---
cache.set("What is Python?", "Python is a programming language.")
print("f2. Stored response in cache")

# --- Cache Hit Scenario ---
result = cache.get("What is Python?")
print(f"f3. Second lookup: {result} (HIT!)")