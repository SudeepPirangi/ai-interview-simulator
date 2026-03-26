"""Reduce step: combine per-chunk skill JSON dicts into one profile."""

from typing import Any

_SKILL_KEYS = ("languages", "frameworks", "databases", "cloud", "devops")


def _norm(s: str) -> str:
    return " ".join(s.lower().split())


def _dedupe_preserve_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        key = _norm(item)
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(item.strip())
    return out


def merge_raw_skill_payloads(partials: list[dict[str, Any] | None]) -> dict[str, list[str]]:
    """Union list fields from each chunk; skip Nones; dedupe case-insensitively per category."""
    merged: dict[str, list[str]] = {k: [] for k in _SKILL_KEYS}

    for part in partials:
        if not part or not isinstance(part, dict):
            continue
        for key in _SKILL_KEYS:
            raw = part.get(key) or []
            if isinstance(raw, list):
                merged[key].extend(str(x) for x in raw if x is not None and str(x).strip())

    for key in _SKILL_KEYS:
        merged[key] = _dedupe_preserve_order(merged[key])

    return merged
