import time

from app.config import OPEN_AI
from app.core.cache import get_cache_key, get_from_cache, set_cache
from app.core.retry import call_with_retry
from app.llm.gemini_provider import GeminiProvider
from app.llm.openai_provider import OpenAIProvider
from app.observability.log import log_event
from app.types import PromptRequest


def generate_response(request: PromptRequest, system_prompt: str, user_prompt: str):
    if request.provider == OPEN_AI:
        provider = OpenAIProvider()
    else:
        provider = GeminiProvider()

    start = time.time()

    json_mode = getattr(request, "json_mode", False)
    key = get_cache_key(system_prompt, user_prompt, json_mode=json_mode)

    cached = get_from_cache(key)
    if cached:
        response = cached
        log_event("llm_cache_hit", provider=request.provider, json_mode=json_mode)
    else:
        response = call_with_retry(
            lambda: provider.generate(system_prompt, user_prompt, json_mode=json_mode)
        )
        log_event("llm_cache_miss", provider=request.provider, json_mode=json_mode)

    end = time.time()
    latency = end - start
    log_event(
        "llm_call_complete",
        provider=request.provider,
        json_mode=json_mode,
        latency_sec=round(latency, 3),
    )

    set_cache(key, response)

    return (response, latency)
