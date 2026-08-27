#!/usr/bin/env python3
"""Validate a stage-seven semantic source review against its evidence bundle."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from refresh_research_sources import validate_review


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: validate_research_review.py <source-bundle.json> <review.json>", file=sys.stderr)
        return 2
    source_path, review_path = map(Path, sys.argv[1:])
    try:
        source = json.loads(source_path.read_text(encoding="utf-8"))
        review = json.loads(review_path.read_text(encoding="utf-8"))
        project_id = source["projectId"]
        fingerprint = source["sourceFingerprint"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    errors = validate_review(review, project_id, fingerprint)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {review_path} is a valid stage-seven semantic review")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
