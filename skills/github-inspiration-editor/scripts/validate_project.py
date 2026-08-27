#!/usr/bin/env python3
"""Validate a versioned app-ready GitHub inspiration project record."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate_visual_identity import MOTIFS, contrast_ratio  # noqa: E402


ROOT_FIELDS = {"schemaVersion", "id", "repository", "editorial", "visual"}
REPOSITORY_FIELDS = {
    "githubId", "fullName", "name", "stars", "forks", "language",
    "pushedAt", "license", "state", "fetchedAt",
}
EDITORIAL_FIELDS = {
    "hook", "summary", "meaning", "audience", "features", "stack",
    "opportunity", "directions",
}
VISUAL_FIELDS = {"generatorVersion", "seed", "accent", "foreground", "motif", "variant"}
DIRECTION_FIELDS = {
    "id", "name", "tagline", "problem", "audience", "approach",
    "difference", "scope",
}
REPOSITORY_STATES = {"active", "archived", "disabled", "unavailable"}
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FULL_NAME = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
END_PUNCTUATION = tuple("。！？.!?")


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def check_exact_fields(value: object, expected: set[str], path: str, errors: list[str]) -> bool:
    require(isinstance(value, dict), f"{path} must be an object", errors)
    if not isinstance(value, dict):
        return False
    require(not (expected - value.keys()), f"{path} missing fields: {', '.join(sorted(expected - value.keys()))}", errors)
    require(not (value.keys() - expected), f"{path} unexpected fields: {', '.join(sorted(value.keys() - expected))}", errors)
    return True


def check_string(value: object, path: str, errors: list[str]) -> None:
    require(isinstance(value, str) and bool(value.strip()), f"{path} must be a non-empty string", errors)


def check_list(value: object, minimum: int, maximum: int, path: str, errors: list[str]) -> None:
    require(isinstance(value, list), f"{path} must be an array", errors)
    if not isinstance(value, list):
        return
    require(minimum <= len(value) <= maximum, f"{path} must contain {minimum}-{maximum} items", errors)
    require(all(isinstance(item, str) and item.strip() for item in value), f"{path} items must be non-empty strings", errors)


def parse_utc_iso(value: object, path: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str):
        errors.append(f"{path} must be a UTC ISO 8601 string")
        return None
    require(value.endswith("Z"), f"{path} must end with Z", errors)
    try:
        timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{path} must be a valid UTC ISO 8601 timestamp")
        return None
    require(timestamp.tzinfo is not None, f"{path} must include a UTC timezone", errors)
    return timestamp


def validate(project: object) -> list[str]:
    errors: list[str] = []
    if not check_exact_fields(project, ROOT_FIELDS, "root", errors):
        return errors

    assert isinstance(project, dict)
    require(project.get("schemaVersion") == 2, "schemaVersion must be 2", errors)
    project_id = project.get("id")
    require(isinstance(project_id, str) and bool(SLUG.fullmatch(project_id)), "id must be a lowercase kebab-case slug", errors)

    repository = project.get("repository")
    if check_exact_fields(repository, REPOSITORY_FIELDS, "repository", errors):
        assert isinstance(repository, dict)
        github_id = repository.get("githubId")
        require(isinstance(github_id, int) and not isinstance(github_id, bool) and github_id > 0, "repository.githubId must be a positive integer", errors)
        full_name = repository.get("fullName")
        require(isinstance(full_name, str) and bool(FULL_NAME.fullmatch(full_name)), "repository.fullName must be owner/repository", errors)
        for field in ("name", "language", "license"):
            check_string(repository.get(field), f"repository.{field}", errors)
        for field in ("stars", "forks"):
            value = repository.get(field)
            require(isinstance(value, int) and not isinstance(value, bool) and value >= 0, f"repository.{field} must be a non-negative integer", errors)
        state = repository.get("state")
        require(state in REPOSITORY_STATES, f"repository.state must be one of: {', '.join(sorted(REPOSITORY_STATES))}", errors)
        pushed_at = parse_utc_iso(repository.get("pushedAt"), "repository.pushedAt", errors)
        fetched_at = parse_utc_iso(repository.get("fetchedAt"), "repository.fetchedAt", errors)
        if pushed_at is not None and fetched_at is not None:
            require(pushed_at <= fetched_at, "repository.pushedAt must not be later than repository.fetchedAt", errors)

    editorial = project.get("editorial")
    if check_exact_fields(editorial, EDITORIAL_FIELDS, "editorial", errors):
        assert isinstance(editorial, dict)
        for field in ("hook", "summary", "meaning", "audience"):
            check_string(editorial.get(field), f"editorial.{field}", errors)
        hook = editorial.get("hook")
        if isinstance(hook, str):
            require(10 <= len(hook) <= 28, "editorial.hook should contain 10-28 characters", errors)
            require(not hook.endswith(END_PUNCTUATION), "editorial.hook must not end with punctuation", errors)
        summary = editorial.get("summary")
        if isinstance(summary, str):
            require(60 <= len(summary) <= 180, "editorial.summary should contain 60-180 characters", errors)
        check_list(editorial.get("features"), 3, 6, "editorial.features", errors)
        check_list(editorial.get("stack"), 1, 8, "editorial.stack", errors)
        check_list(editorial.get("opportunity"), 2, 5, "editorial.opportunity", errors)
        validate_directions(editorial.get("directions"), errors)

    visual = project.get("visual")
    if check_exact_fields(visual, VISUAL_FIELDS, "visual", errors):
        assert isinstance(visual, dict)
        require(visual.get("generatorVersion") in {1, 2}, "visual.generatorVersion must be 1 or 2", errors)
        seed = visual.get("seed")
        require(isinstance(seed, str) and bool(FULL_NAME.fullmatch(seed)), "visual.seed must be owner/repository", errors)
        accent = visual.get("accent")
        require(isinstance(accent, str) and bool(HEX.fullmatch(accent)), "visual.accent must be a six-digit hex color", errors)
        if isinstance(accent, str) and HEX.fullmatch(accent):
            require(contrast_ratio(accent, "#ffffff") >= 4.5, "visual.accent must have at least 4.5:1 contrast against white", errors)
            expected_foreground = "#000000" if contrast_ratio(accent, "#000000") >= contrast_ratio(accent, "#ffffff") else "#ffffff"
            require(visual.get("foreground") == expected_foreground, f"visual.foreground must be {expected_foreground} for this accent", errors)
        motif = visual.get("motif")
        require(motif in MOTIFS, f"visual.motif must be one of: {', '.join(MOTIFS)}", errors)
        variant = visual.get("variant")
        require(isinstance(variant, int) and not isinstance(variant, bool) and 0 <= variant <= 0xFFFFFFFF, "visual.variant must be an unsigned 32-bit integer", errors)

    return errors


def validate_directions(directions: object, errors: list[str]) -> None:
    require(isinstance(directions, list), "editorial.directions must be an array", errors)
    if not isinstance(directions, list):
        return
    require(3 <= len(directions) <= 5, "editorial.directions must contain 3-5 items", errors)
    direction_ids: list[str] = []
    for index, direction in enumerate(directions):
        prefix = f"editorial.directions[{index}]"
        if not check_exact_fields(direction, DIRECTION_FIELDS, prefix, errors):
            continue
        assert isinstance(direction, dict)
        for field in DIRECTION_FIELDS - {"scope"}:
            check_string(direction.get(field), f"{prefix}.{field}", errors)
        direction_id = direction.get("id")
        require(isinstance(direction_id, str) and bool(SLUG.fullmatch(direction_id)), f"{prefix}.id must be a lowercase kebab-case slug", errors)
        if isinstance(direction_id, str):
            direction_ids.append(direction_id)
        check_list(direction.get("scope"), 3, 6, f"{prefix}.scope", errors)
    require(len(direction_ids) == len(set(direction_ids)), "direction IDs must be unique", errors)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_project.py <project.json>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        project = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    errors = validate(project)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {path} is a valid versioned GitHub inspiration project record")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
