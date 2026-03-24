from app.config import GEMINI, OPEN_AI
from app.services.llm_service import generate_response
from app.types import CustomPromptRequest
from app.utils.index import parse_json_response


def build_skill_extraction_prompt(resume_text: str) -> str:
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


def extract_skills(resume_text, provider=OPEN_AI):
    prompt = build_skill_extraction_prompt(resume_text)

    response = generate_response(
        request=CustomPromptRequest(provider=GEMINI),
        system_prompt="You extract structured data from resumes.",
        user_prompt=prompt,
    )

    json_response = parse_json_response(response[0])

    return json_response
