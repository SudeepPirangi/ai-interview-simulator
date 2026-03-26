from google import genai

from app.config import GEMINI_API_KEY
from .base import BaseLLMProvider

class GeminiProvider(BaseLLMProvider):

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate(self, system_prompt: str, user_prompt: str, *, json_mode: bool = False) -> str:
        # json_mode is ignored here; Gemini can be wired to JSON MIME types later if needed.
        _ = json_mode
        prompt = f"{system_prompt}\n\n{user_prompt}"

        response = self.client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
            config={
                'temperature': 0.3
            }
        )
        print('Gemini Usage', response.usage_metadata)
        return response.text