from openai import OpenAI
from app.config import OPENAI_API_KEY
from .base import BaseLLMProvider

class OpenAIProvider(BaseLLMProvider):

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate(self, system_prompt: str, user_prompt: str, *, json_mode: bool = False) -> str:
        kwargs = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.3,
        }
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        response = self.client.chat.completions.create(**kwargs)

        print("OpenAI Usage:", response.usage)
        text = response.choices[0].message.content
        return text if text is not None else ""