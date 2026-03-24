import time

from app.config import OPEN_AI
from app.core.cache import get_cache_key, get_from_cache, set_cache
from app.core.retry import call_with_retry
from app.llm.gemini_provider import GeminiProvider
from app.llm.openai_provider import OpenAIProvider
from app.types import PromptRequest


def generate_response(request: PromptRequest, system_prompt: str, user_prompt: str):
    if request.provider == OPEN_AI:
        provider = OpenAIProvider()
    else:
        provider = GeminiProvider()

    start = time.time()

    key = get_cache_key(system_prompt, user_prompt)

    # Check cache first
    cached = get_from_cache(key)
    if cached:
        # If cached → cached response
        response = cached
    else:
        # If not cached → call LLM
        response = call_with_retry(
            lambda: provider.generate(system_prompt, user_prompt)
        )

    end = time.time()
    latency = end - start
    print(f"[Latency] {latency:.2f} seconds")

    # Store in cache
    set_cache(key, response)

    return (response, latency)
