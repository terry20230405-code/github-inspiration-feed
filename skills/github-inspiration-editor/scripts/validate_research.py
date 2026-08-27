#!/usr/bin/env python3
"""Validate the traceability structure of a repository research note."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_HEADINGS = (
    "## Snapshot",
    "## Sources",
    "## Verified repository facts",
    "## Page field evidence",
    "## Product inferences",
    "## Direction rationale",
    "## Uncertainty",
    "## Localization decisions",
    "## Refresh notes",
)
REQUIRED_FIELDS = (
    "repository.githubId", "repository.fullName", "repository.name",
    "repository.stars", "repository.forks", "repository.language",
    "repository.pushedAt", "repository.license", "repository.state",
    "editorial.hook", "editorial.summary", "editorial.meaning",
    "editorial.audience", "editorial.features", "editorial.stack",
    "editorial.opportunity",
)
DATE = re.compile(r"^Research date: \d{4}-\d{2}-\d{2}$", re.MULTILINE)
REPOSITORY = re.compile(r"^Repository: https://github\.com/[^/\s]+/[^/\s]+/?$", re.MULTILINE)
MODE = re.compile(r"^Research mode: (new|refresh)$", re.MULTILINE)
FETCHED_AT = re.compile(r"^- Fetched at: \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", re.MULTILINE)
REPOSITORY_STATE = re.compile(r"^- Repository state: (active|archived|disabled|unavailable)$", re.MULTILINE)
SOURCE_ID = re.compile(r"^- \[(S\d+)\] ", re.MULTILINE)
FACT_ID = re.compile(r"^- \[(F\d+)\] .+Sources: (S\d+(?:, S\d+)*)", re.MULTILINE)
DIRECTION = re.compile(r"^### D\d+ — .+$", re.MULTILINE)


def validate(text: str) -> list[str]:
    errors: list[str] = []
    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"missing heading: {heading}")

    if not DATE.search(text):
        errors.append("Research date must use YYYY-MM-DD")
    if not REPOSITORY.search(text):
        errors.append("Repository must be a canonical https://github.com/owner/repo URL")
    if not MODE.search(text):
        errors.append("Research mode must be new or refresh")
    if not FETCHED_AT.search(text):
        errors.append("Snapshot must include Fetched at as a UTC ISO 8601 timestamp")
    if not REPOSITORY_STATE.search(text):
        errors.append("Repository state must be active, archived, disabled, or unavailable")

    source_ids = set(SOURCE_ID.findall(text))
    if not source_ids:
        errors.append("at least one [S#] source is required")

    fact_matches = FACT_ID.findall(text)
    if len(fact_matches) < 3:
        errors.append("at least three [F#] facts with Sources are required")
    for _, citations in fact_matches:
        for citation in citations.split(", "):
            if citation not in source_ids:
                errors.append(f"fact cites undefined source: {citation}")

    for field in REQUIRED_FIELDS:
        if f"| `{field}` |" not in text:
            errors.append(f"page field evidence is missing `{field}`")

    direction_count = len(DIRECTION.findall(text))
    if not 3 <= direction_count <= 5:
        errors.append("direction rationale must contain 3-5 D# sections")

    inference_ids = re.findall(r"^- \[I\d+\] ", text, re.MULTILINE)
    if inference_ids and "Confidence:" not in text:
        errors.append("product inferences must state Confidence")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_research.py <research.md>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    errors = validate(text)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"OK: {path} is a valid repository research note")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
