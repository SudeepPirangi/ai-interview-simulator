import json
import re


def extract_json(text: str) -> str:
    # Remove ```json ... ``` blocks
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```", "", text)

    return text.strip()


def parse_json_response(text: str):
    cleaned = extract_json(text)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        print("Invalid JSON response")
        return None
