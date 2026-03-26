"""Split long resume text into overlapping segments for per-chunk LLM calls."""

from app.config import CHUNK_OVERLAP, CHUNK_SIZE


def chunk_resume_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[str]:
    """
    Return non-empty chunks of at most `chunk_size` characters.
    Overlap lets entities that sit on a boundary appear in two chunks, reducing missed extractions.
    """
    text = text.strip()
    if not text:
        return []

    if len(text) <= chunk_size:
        return [text]

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = max(0, end - overlap)

    return chunks
