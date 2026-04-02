"""Lazy Redis connection. Used when REDIS_URL is set; otherwise callers fall back to in-memory."""

from app.config import REDIS_URL

_client = None


def get_redis():
    """Return a shared Redis client, or None if REDIS_URL is not configured."""
    global _client
    if not REDIS_URL:
        return None
    if _client is None:
        import redis

        _client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    return _client
