"""
Temporary in-memory caching implemented.
This needs to be updated later with production grade caching.
"""

import time

cache_store = {}

CACHE_TTL = 300  # 5 minutes


def get_cache_key(system_prompt: str, user_prompt: str) -> str:
    return f"{system_prompt}:{user_prompt}"


def get_from_cache(key: str):
    if key in cache_store:
        data, timestamp = cache_store[key]

        if time.time() - timestamp < CACHE_TTL:
            print("[Cache] HIT")
            return data
        else:
            print("[Cache] EXPIRED")
            del cache_store[key]

    return None


def set_cache(key: str, value):
    cache_store[key] = (value, time.time())
    # print("cache_store", cache_store)
