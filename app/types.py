from pydantic import BaseModel
from typing import Literal

class Question(BaseModel):
    question: str
    difficulty: str
    topic: str

class LLMResponse(BaseModel):
    content: dict
    usage: dict

class PromptRequest(BaseModel):
    prompt: str
    provider: Literal['openai', 'gemini']