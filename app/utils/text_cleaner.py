import re


def clean_text(text: str) -> str:
    # Remove multiple spaces/newlines
    text = re.sub(r"\s+", " ", text)

    # Remove weird characters (basic cleanup)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    # Optional: remove excessive punctuation noise
    text = re.sub(r"[•●▪]", " ", text)

    return text.strip()
