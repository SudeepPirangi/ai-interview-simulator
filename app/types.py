from typing import Literal

from pydantic import BaseModel, Field

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


class ResumeSkills(BaseModel):
    """Structured skill buckets returned by /upload-resume and used after merge."""

    languages: list[str] = Field(default_factory=list)
    frameworks: list[str] = Field(default_factory=list)
    databases: list[str] = Field(default_factory=list)
    cloud: list[str] = Field(default_factory=list)
    devops: list[str] = Field(default_factory=list)


class CustomPromptRequest:
    def __init__(self, prompt="", provider=OPEN_AI, json_mode: bool = False):
        self.prompt = prompt
        self.provider = provider
        self.json_mode = json_mode


class SessionStartRequest(BaseModel):
    goal: str = "30-minute senior backend technical screen"
    resume_skills: ResumeSkills | None = None
    provider: Literal[OPEN_AI, GEMINI, CLAUDE] = OPEN_AI
    max_turns: int = Field(default=5, ge=1, le=20)


class SessionTurnRequest(BaseModel):
    session_id: str
    answer: str = Field(min_length=1)
