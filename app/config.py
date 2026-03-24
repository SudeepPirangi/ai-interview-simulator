import os

from dotenv import load_dotenv

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# providers
OPEN_AI = "openai"
GEMINI = "gemini"
CLAUDE = "claude"

# general app constants
MAX_CHARS = 5000
MAX_RETRIES = 3

# caching
CACHE_TTL = 300  # 5 minutes

# rate-limiting
RATE_LIMIT = 5  # max requests
WINDOW_SIZE = 60  # seconds
