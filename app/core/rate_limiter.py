"""Sliding-window rate limit: Redis sorted sets when REDIS_URL is set, else in-process."""

from __future__ import annotations

import uuid
from time import time

from app.config import RATE_LIMIT, WINDOW_SIZE
from app.core.redis_client import get_redis

user_requests: dict[str, list[float]] = {}


def is_allowed(user_id: str) -> bool:
    r = get_redis()
    now = time()
    if r:
        key = f"ratelimit:{user_id}"
        try:
            r.zremrangebyscore(key, "-inf", now - WINDOW_SIZE)
            if r.zcard(key) >= RATE_LIMIT:
                return False
            r.zadd(key, {str(uuid.uuid4()): now})
            r.expire(key, WINDOW_SIZE + 1)
            return True
        except Exception:
            return _is_allowed_memory(user_id, now)

    return _is_allowed_memory(user_id, now)


def _is_allowed_memory(user_id: str, now: float) -> bool:
    if user_id not in user_requests:
        user_requests[user_id] = []

    user_requests[user_id] = [t for t in user_requests[user_id] if now - t < WINDOW_SIZE]

    if len(user_requests[user_id]) >= RATE_LIMIT:
        return False

    user_requests[user_id].append(now)
    return True
