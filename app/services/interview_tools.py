"""Tool-style LLM helpers for the interview agent."""

from app.config import OPEN_AI
from app.services.llm_service import generate_response
from app.types import CustomPromptRequest, ResumeSkills


def _skills_context(skills: ResumeSkills | None) -> str:
    if not skills:
        return "No resume profile provided."
    return skills.model_dump_json()


def get_next_question(
    *,
    goal: str,
    resume_skills: ResumeSkills | None,
    history: list[dict[str, str]],
    provider: str = OPEN_AI,
) -> str:
    history_text = "\n".join(f"{m['role']}: {m['content']}" for m in history[-8:]) or "(none yet)"
    user_prompt = f"""
Interview goal: {goal}
Candidate skills: {_skills_context(resume_skills)}

Conversation so far:
{history_text}

Ask ONE new technical interview question suited to the goal and skills.
Do not repeat a prior question. Be concise (1-3 sentences).
Return only the question text.
"""
    response, _ = generate_response(
        CustomPromptRequest(provider=provider),
        "You are a senior technical interviewer.",
        user_prompt.strip(),
    )
    return response.strip()


def evaluate_answer(
    *,
    question: str,
    answer: str,
    provider: str = OPEN_AI,
) -> str:
    user_prompt = f"""
Question: {question}
Candidate answer: {answer}

Give brief constructive feedback (3-5 sentences): what was strong, what was missing, one improvement tip.
Return plain text only.
"""
    response, _ = generate_response(
        CustomPromptRequest(provider=provider),
        "You evaluate technical interview answers fairly and concisely.",
        user_prompt.strip(),
    )
    return response.strip()


def summarize_weak_areas(
    *,
    goal: str,
    history: list[dict[str, str]],
    provider: str = OPEN_AI,
) -> str:
    history_text = "\n".join(f"{m['role']}: {m['content']}" for m in history)
    user_prompt = f"""
Interview goal: {goal}

Full conversation:
{history_text}

Summarize the candidate's weak areas and top 3 study recommendations in plain text (short paragraphs + bullet list).
"""
    response, _ = generate_response(
        CustomPromptRequest(provider=provider),
        "You summarize interview performance for coaching.",
        user_prompt.strip(),
    )
    return response.strip()
