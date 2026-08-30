#!/usr/bin/env python3
"""Validate a 19-item editorial quality review and its artifact fingerprints."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath


CHECK_IDS = (
    "A1", "A2", "A3", "A4",
    "B1", "B2", "B3", "B4",
    "C1", "C2", "C3", "C4",
    "D1", "D2", "D3", "D4",
    "E1", "E2", "E3",
)
ROOT_FIELDS = {
    "schemaVersion", "projectId", "projectPath", "researchPath", "projectSha256",
    "researchSha256", "reviewedAt", "items", "blockers", "publicationCandidate",
    "publicationAuthorized",
}
ITEM_FIELDS = {"id", "status", "evidence"}
SHA256 = re.compile(r"^[0-9a-f]{64}$")
TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def resolve_artifact(project_root: Path, value: object, field: str, errors: list[str]) -> Path | None:
    if not isinstance(value, str) or not value:
        errors.append(f"{field} must be a project-relative path")
        return None
    pure = PurePosixPath(value)
    if pure.is_absolute() or ".." in pure.parts or "\\" in value:
        errors.append(f"{field} is unsafe")
        return None
    path = (project_root / Path(value)).resolve()
    if not path.is_relative_to(project_root.resolve()) or not path.is_file():
        errors.append(f"{field} does not exist: {value}")
        return None
    return path


def validate(review: object, project_root: Path) -> list[str]:
    errors: list[str] = []
    if not isinstance(review, dict):
        return ["review must be a JSON object"]
    if set(review) != ROOT_FIELDS:
        errors.append("review fields do not match the quality-review schema")
    if review.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    if not isinstance(review.get("projectId"), str) or not review["projectId"]:
        errors.append("projectId must be a non-empty string")
    if not isinstance(review.get("reviewedAt"), str) or not TIMESTAMP.fullmatch(review["reviewedAt"]):
        errors.append("reviewedAt must be a UTC ISO timestamp")

    project_path = resolve_artifact(project_root, review.get("projectPath"), "projectPath", errors)
    research_path = resolve_artifact(project_root, review.get("researchPath"), "researchPath", errors)
    for field, path in (("projectSha256", project_path), ("researchSha256", research_path)):
        expected = review.get(field)
        if not isinstance(expected, str) or not SHA256.fullmatch(expected):
            errors.append(f"{field} must be a lowercase SHA-256 hash")
        elif path is not None and sha256_file(path) != expected:
            errors.append(f"{field} does not match the current artifact")

    items = review.get("items")
    if not isinstance(items, list):
        errors.append("items must be an array")
    else:
        ids: list[object] = []
        for item in items:
            if not isinstance(item, dict) or set(item) != ITEM_FIELDS:
                errors.append("each quality item must contain only id, status, and evidence")
                continue
            ids.append(item.get("id"))
            if item.get("status") != "pass":
                errors.append(f"quality item {item.get('id')} is not pass")
            if not isinstance(item.get("evidence"), str) or not item["evidence"].strip():
                errors.append(f"quality item {item.get('id')} needs concrete evidence")
        if tuple(ids) != CHECK_IDS:
            errors.append("items must contain A1-E3 exactly once and in rubric order")

    if review.get("blockers") != []:
        errors.append("blockers must be an empty array for a publication candidate")
    if review.get("publicationCandidate") is not True:
        errors.append("publicationCandidate must be true")
    if review.get("publicationAuthorized") is not False:
        errors.append("quality review never authorizes publication")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_quality_review.py <quality.json>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1]).resolve()
    project_root = Path(__file__).resolve().parents[3]
    try:
        review = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    errors = validate(review, project_root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {path} is a complete 19-item quality review")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
