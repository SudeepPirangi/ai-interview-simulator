from openai import OpenAI
from app.config import OPENAI_API_KEY
from .base import BaseLLMProvider

class OpenAIProvider(BaseLLMProvider):

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )

        print("OpenAI Usage:", response.usage)
        return response.choices[0].message.content