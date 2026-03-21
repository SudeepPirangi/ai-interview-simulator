from time import time

# user_id → list of timestamps
user_requests = {}

RATE_LIMIT = 5  # max requests
WINDOW_SIZE = 60  # seconds


def is_allowed(user_id: str) -> bool:
    now = time()

    if user_id not in user_requests:
        user_requests[user_id] = []

    # Remove old requests
    user_requests[user_id] = [
        t for t in user_requests[user_id] if now - t < WINDOW_SIZE
    ]

    if len(user_requests[user_id]) >= RATE_LIMIT:
        return False

    user_requests[user_id].append(now)
    return True
