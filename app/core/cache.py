"""
LLM response cache: Redis when REDIS_URL is set, else in-process dict + TTL.
"""

from __future__ import annotations

import hashlib
import time

from app.config import CACHE_TTL
from app.core.redis_client import get_redis

cache_store: dict[str, tuple[str, float]] = {}

LOG_PREFIX = "llm_cache"


def _fingerprint(key: str) -> str:
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def get_cache_key(system_prompt: str, user_prompt: str, json_mode: bool = False) -> str:
    suffix = "|json=1" if json_mode else ""
    return f"{system_prompt}:{user_prompt}{suffix}"


def get_from_cache(key: str):
    r = get_redis()
    fp = _fingerprint(key)
    if r:
        try:
            val = r.get(f"{LOG_PREFIX}:{fp}")
            if val is not None:
                return val
        except Exception:
            pass
        return None

    if key in cache_store:
        data, timestamp = cache_store[key]
        if time.time() - timestamp < CACHE_TTL:
            return data
        del cache_store[key]

    return None


def set_cache(key: str, value: str):
    r = get_redis()
    fp = _fingerprint(key)
    if r:
        try:
            r.setex(f"{LOG_PREFIX}:{fp}", CACHE_TTL, value)
        except Exception:
            pass
        return

    cache_store[key] = (value, time.time())
