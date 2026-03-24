from typing import Literal

from pydantic import BaseModel

from app.config import CLAUDE, GEMINI, OPEN_AI


class Question(BaseModel):
    question: str
    difficulty: str
    topic: str


class LLMResponse(BaseModel):
    content: dict
    usage: dict


class PromptRequest(BaseModel):
    prompt: str
    provider: Literal[OPEN_AI, GEMINI, CLAUDE]


class CustomPromptRequest:
    def __init__(self, prompt="", provider=OPEN_AI):
        self.prompt = prompt
        self.provider = provider
