"""
This module contains the services for extracting skills from a resume.
"""

from pydantic import ValidationError

from app.config import OPEN_AI
from app.exceptions import SkillsParsingError
from app.services.llm_service import generate_response
from app.services.skill_merge import merge_raw_skill_payloads
from app.types import CustomPromptRequest, ResumeSkills
from app.utils.chunking import chunk_resume_text
from app.utils.index import parse_json_response

# Single place for the default model for resume parsing. OpenAI tends to follow
# JSON-only instructions more reliably than Gemini for this task — Swap if you benchmark otherwise.
DEFAULT_EXTRACTION_PROVIDER = OPEN_AI


def build_skill_extraction_prompt(resume_text: str) -> str:
    """
    Build the prompt for the skill extraction task.
    """
    return f"""
    You are an expert resume analyzer.

    Extract the following categories:
    - Programming languages
    - Frameworks
    - Databases
    - Cloud technologies
    - DevOps tools

    IMPORTANT:
    - Return ONLY valid JSON
    - Do NOT include markdown
    - Do NOT include explanations
    - Ensure JSON is syntactically correct

    Return strictly valid JSON:
    {{
        "languages": [],
        "frameworks": [],
        "databases": [],
        "cloud": [],
        "devops": []
    }}

    Resume:
    {resume_text}
    """


def _validated_skills_dict(raw_text: str) -> dict | None:
    """Parse JSON from model text, then coerce into ResumeSkills (strict shape)."""
    data = parse_json_response(raw_text)
    if data is None:
        return None
    try:
        return ResumeSkills.model_validate(data).model_dump()
    except ValidationError:
        return None


def _extract_skills_single_chunk(resume_text: str, provider: str):
    """One LLM call for a single text segment (map step)."""
    prompt = build_skill_extraction_prompt(resume_text)
    use_json_mode = provider == OPEN_AI

    response = generate_response(
        request=CustomPromptRequest(provider=provider, json_mode=use_json_mode),
        system_prompt="You extract structured data from resumes.",
        user_prompt=prompt,
    )

    return _validated_skills_dict(response[0])


def extract_skills(resume_text: str, provider: str = DEFAULT_EXTRACTION_PROVIDER) -> dict:
    """
    Map-reduce over the resume: chunk long text, extract per chunk, merge and dedupe.
    Raises SkillsParsingError if the model returns unparseable or invalid structured data.
    """
    chunks = chunk_resume_text(resume_text)
    if not chunks:
        return ResumeSkills().model_dump()

    partials = [_extract_skills_single_chunk(ch, provider) for ch in chunks]

    if len(chunks) == 1:
        one = partials[0]
        if one is None:
            raise SkillsParsingError("Could not parse structured skills from model output")
        return one

    if all(p is None for p in partials):
        raise SkillsParsingError("Could not parse structured skills from any resume chunk")

    merged = merge_raw_skill_payloads(partials)
    return ResumeSkills.model_validate(merged).model_dump()
