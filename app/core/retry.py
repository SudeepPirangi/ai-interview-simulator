import random
import time


def call_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            wait_time = (2**attempt) + random.uniform(0, 1)
            print(f"[Retry] Attempt {attempt + 1} failed: {e.message}")
            print(f"[Retry] Waiting {wait_time:.2f}s before retrying...")
            time.sleep(wait_time)

    raise Exception("Max retries exceeded")
