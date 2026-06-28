"""In-memory multi-turn interview sessions (agent orchestration)."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from app.config import OPEN_AI
from app.services.interview_tools import (
    evaluate_answer,
    get_next_question,
    summarize_weak_areas,
)
from app.types import ResumeSkills

_sessions: dict[str, "InterviewSession"] = {}


@dataclass
class InterviewSession:
    session_id: str
    goal: str
    resume_skills: ResumeSkills | None
    provider: str
    max_turns: int
    turn_count: int = 0
    current_question: str | None = None
    messages: list[dict[str, str]] = field(default_factory=list)
    status: str = "active"  # active | completed
    last_evaluation: str | None = None
    summary: str | None = None


def start_session(
    *,
    goal: str = "30-minute senior backend technical screen",
    resume_skills: ResumeSkills | None = None,
    provider: str = OPEN_AI,
    max_turns: int = 5,
) -> InterviewSession:
    session_id = str(uuid.uuid4())
    session = InterviewSession(
        session_id=session_id,
        goal=goal,
        resume_skills=resume_skills,
        provider=provider,
        max_turns=max_turns,
    )
    question = get_next_question(
        goal=session.goal,
        resume_skills=session.resume_skills,
        history=session.messages,
        provider=session.provider,
    )
    session.current_question = question
    session.messages.append({"role": "assistant", "content": question})
    _sessions[session_id] = session
    return session


def get_session(session_id: str) -> InterviewSession | None:
    return _sessions.get(session_id)


def process_turn(session_id: str, answer: str) -> InterviewSession:
    session = _sessions.get(session_id)
    if not session:
        raise KeyError("Session not found")
    if session.status == "completed":
        raise ValueError("Session already completed")

    if not session.current_question:
        raise ValueError("No active question for this session")

    session.messages.append({"role": "user", "content": answer})
    session.last_evaluation = evaluate_answer(
        question=session.current_question,
        answer=answer,
        provider=session.provider,
    )
    session.messages.append(
        {"role": "assistant", "content": f"Feedback: {session.last_evaluation}"}
    )
    session.turn_count += 1

    if session.turn_count >= session.max_turns:
        session.summary = summarize_weak_areas(
            goal=session.goal,
            history=session.messages,
            provider=session.provider,
        )
        session.status = "completed"
        session.current_question = None
        return session

    next_q = get_next_question(
        goal=session.goal,
        resume_skills=session.resume_skills,
        history=session.messages,
        provider=session.provider,
    )
    session.current_question = next_q
    session.messages.append({"role": "assistant", "content": next_q})
    return session
