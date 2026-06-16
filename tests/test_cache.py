"""Tests for the caching layer.

Fast, deterministic, no external dependencies.
"""

import time
from app.cache import ResponseCache


class TestResponseCache:
    """Test the response cache."""

    def setup_method(self):
        # Set a short TTL of 2 seconds to make expiration testing immediate
        self.cache = ResponseCache(ttl_seconds=2)

    def test_cache_miss_returns_none(self):
        assert self.cache.get("unknown query") is None

    def test_cache_hit_returns_response(self):
        self.cache.set("What is Python?", "A programming language.")
        result = self.cache.get("What is Python?")
        assert result == "A programming language."

    def test_ttl_expiration(self):
        self.cache.set("query", "value")
        
        # Sleep for 2.1 seconds to cross the explicit 2-second TTL expiration window
        time.sleep(2.1)
        
        assert self.cache.get("query") is None

    def test_stats_tracking(self):
        # Trigger 2 cache misses
        self.cache.get("miss1")
        self.cache.get("miss2")
        
        # Add an entry to the cache
        self.cache.set("hit", "value")
        
        # Trigger 1 cache hit
        self.cache.get("hit")

        stats = self.cache.stats
        assert stats["hits"] == 1
        assert stats["misses"] == 2
        assert stats["cached_entries"] == 1