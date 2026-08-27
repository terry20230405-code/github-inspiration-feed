#!/usr/bin/env python3
"""Refresh published repository snapshots without changing editorial or visual data."""

from __future__ import annotations

import argparse
import copy
import json
import os
import ssl
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

try:
    import certifi
except ImportError:  # Standard Python trust store remains the fallback.
    certifi = None


API_VERSION = "2026-03-10"
USER_AGENT = "github-inspiration-feed-metadata-refresh"
SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where() if certifi else None)
REPOSITORY_FIELDS = (
    "githubId", "fullName", "name", "stars", "forks", "language",
    "pushedAt", "license", "state", "fetchedAt",
)
CRITICAL_FIELDS = {"githubId", "fullName", "license", "state"}
ACTIVITY_FIELDS = {"pushedAt"}
METADATA_FIELDS = {"name", "language"}
STATISTIC_FIELDS = {"stars", "forks"}


@dataclass(frozen=True)
class FetchResult:
    status: int
    payload: dict[str, object] | None
    etag: str | None
    rate_limit_remaining: str | None
    error: str | None = None


Fetcher = Callable[[str, str | None], FetchResult]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False, newline="\n") as handle:
        handle.write(content)
        temporary_path = Path(handle.name)
    temporary_path.replace(path)


def validate_snapshot(snapshot: object, project_id: str) -> dict[str, object]:
    if not isinstance(snapshot, dict):
        raise ValueError(f"{project_id}: repository snapshot must be an object")
    if set(snapshot) != set(REPOSITORY_FIELDS):
        raise ValueError(f"{project_id}: repository snapshot fields do not match the content contract")
    if not isinstance(snapshot["githubId"], int) or isinstance(snapshot["githubId"], bool) or snapshot["githubId"] <= 0:
        raise ValueError(f"{project_id}: githubId must be a positive integer")
    for field in ("fullName", "name", "language", "pushedAt", "license", "state", "fetchedAt"):
        if not isinstance(snapshot[field], str) or not str(snapshot[field]).strip():
            raise ValueError(f"{project_id}: {field} must be a non-empty string")
    for field in ("stars", "forks"):
        if not isinstance(snapshot[field], int) or isinstance(snapshot[field], bool) or snapshot[field] < 0:
            raise ValueError(f"{project_id}: {field} must be a non-negative integer")
    if snapshot["state"] not in {"active", "archived", "disabled", "unavailable"}:
        raise ValueError(f"{project_id}: invalid repository state")
    return snapshot


def reliable_license(payload: dict[str, object], current_license: str) -> str:
    license_value = payload.get("license")
    if not isinstance(license_value, dict):
        return current_license
    spdx_id = license_value.get("spdx_id")
    name = license_value.get("name")
    if isinstance(spdx_id, str) and spdx_id.upper() not in {"", "NOASSERTION", "OTHER"}:
        return spdx_id
    if isinstance(name, str) and name.strip().lower() not in {"", "other", "other license"}:
        return name.strip()
    return current_license


def required_api_value(payload: dict[str, object], field: str, expected_type: type) -> object:
    value = payload.get(field)
    if not isinstance(value, expected_type) or isinstance(value, bool) and expected_type is int:
        raise ValueError(f"GitHub response has an invalid {field}")
    return value


def build_candidate(current: dict[str, object], payload: dict[str, object], fetched_at: str) -> dict[str, object]:
    github_id = required_api_value(payload, "id", int)
    full_name = required_api_value(payload, "full_name", str)
    api_name = required_api_value(payload, "name", str)
    current_name = str(current["name"])
    name = current_name if str(api_name).casefold() == current_name.casefold() else api_name
    stars = required_api_value(payload, "stargazers_count", int)
    forks = required_api_value(payload, "forks_count", int)
    pushed_at = required_api_value(payload, "pushed_at", str)
    language_value = payload.get("language")
    language = language_value if isinstance(language_value, str) and language_value.strip() else "未知"
    state = "disabled" if payload.get("disabled") is True else "archived" if payload.get("archived") is True else "active"
    return {
        "githubId": github_id,
        "fullName": full_name,
        "name": name,
        "stars": stars,
        "forks": forks,
        "language": language,
        "pushedAt": pushed_at,
        "license": reliable_license(payload, str(current["license"])),
        "state": state,
        "fetchedAt": fetched_at,
    }


def compare_snapshots(current: dict[str, object], candidate: dict[str, object]) -> list[dict[str, object]]:
    changes: list[dict[str, object]] = []
    for field in REPOSITORY_FIELDS:
        if field == "fetchedAt" or current[field] == candidate[field]:
            continue
        if field in CRITICAL_FIELDS:
            level = "critical"
        elif field in ACTIVITY_FIELDS:
            level = "activity"
        elif field in METADATA_FIELDS:
            level = "metadata"
        elif field in STATISTIC_FIELDS:
            level = "statistics"
        else:
            level = "metadata"
        changes.append({"field": field, "before": current[field], "after": candidate[field], "level": level})
    return changes


def classify_change(changes: list[dict[str, object]]) -> str:
    levels = {str(change["level"]) for change in changes}
    for level in ("critical", "activity", "metadata", "statistics"):
        if level in levels:
            return level
    return "freshness"


def critical_reasons(current: dict[str, object], candidate: dict[str, object], payload: dict[str, object], changes: list[dict[str, object]]) -> list[str]:
    reasons = [f"{change['field']} changed" for change in changes if change["field"] in CRITICAL_FIELDS]
    if payload.get("private") is True:
        reasons.append("repository became private or requires different access")
    if payload.get("fork") is True:
        reasons.append("canonical repository is now reported as a fork")
    if candidate["state"] != "active" and current["state"] == "active":
        reasons.append(f"repository state changed to {candidate['state']}")
    return list(dict.fromkeys(reasons))


def fetch_github_repository(
    full_name: str,
    etag: str | None,
    token: str | None,
    api_base: str = "https://api.github.com",
    timeout: float = 20,
) -> FetchResult:
    owner, repository = full_name.split("/", 1)
    url = f"{api_base.rstrip('/')}/repos/{urllib.parse.quote(owner, safe='')}/{urllib.parse.quote(repository, safe='')}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": API_VERSION,
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if etag:
        headers["If-None-Match"] = etag
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=SSL_CONTEXT) as response:
            payload = json.loads(response.read().decode("utf-8"))
            if not isinstance(payload, dict):
                return FetchResult(response.status, None, response.headers.get("etag"), response.headers.get("x-ratelimit-remaining"), "GitHub returned a non-object response")
            return FetchResult(response.status, payload, response.headers.get("etag"), response.headers.get("x-ratelimit-remaining"))
    except urllib.error.HTTPError as error:
        if error.code == 304:
            return FetchResult(304, None, etag, error.headers.get("x-ratelimit-remaining"))
        if error.code == 404:
            return FetchResult(404, None, None, error.headers.get("x-ratelimit-remaining"), "GitHub returned 404; this can mean deleted, private, renamed, or inaccessible")
        remaining = error.headers.get("x-ratelimit-remaining")
        if error.code in {403, 429} and remaining == "0":
            reset = error.headers.get("x-ratelimit-reset") or "unknown"
            return FetchResult(error.code, None, None, remaining, f"GitHub rate limit reached; reset epoch is {reset}")
        return FetchResult(error.code, None, None, remaining, f"GitHub request failed with HTTP {error.code}")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        return FetchResult(0, None, None, None, f"GitHub request failed: {error}")


def refresh_dataset(
    dataset: dict[str, object],
    cache: dict[str, object],
    selected_ids: list[str],
    fetcher: Fetcher,
    fetched_at: str,
) -> tuple[dict[str, object], dict[str, object], list[dict[str, object]]]:
    updated_dataset = copy.deepcopy(dataset)
    updated_cache = copy.deepcopy(cache)
    cache_repositories = updated_cache.setdefault("repositories", {})
    if not isinstance(cache_repositories, dict):
        raise ValueError("refresh cache repositories must be an object")
    results: list[dict[str, object]] = []

    for project_id in selected_ids:
        current = validate_snapshot(dataset[project_id], project_id)
        cache_key = str(current["githubId"])
        cached = cache_repositories.get(cache_key)
        cached_etag = cached.get("etag") if isinstance(cached, dict) and isinstance(cached.get("etag"), str) else None
        response = fetcher(str(current["fullName"]), cached_etag)
        base_result: dict[str, object] = {
            "id": project_id,
            "requestedFullName": current["fullName"],
            "httpStatus": response.status,
            "rateLimitRemaining": response.rate_limit_remaining,
        }

        if response.status == 304:
            refreshed = dict(current)
            refreshed["fetchedAt"] = fetched_at
            updated_dataset[project_id] = refreshed
            cache_repositories[cache_key] = {"fullName": current["fullName"], "etag": response.etag, "lastCheckedAt": fetched_at}
            results.append({**base_result, "status": "refreshed", "changeLevel": "freshness", "changes": [], "researchRefreshRecommended": False, "contentReviewRecommended": False, "reviewReasons": []})
            continue

        if response.status == 404:
            results.append({**base_result, "status": "review-required", "changeLevel": "critical", "changes": [], "researchRefreshRecommended": False, "contentReviewRecommended": False, "reviewReasons": [response.error]})
            continue

        if response.status != 200 or response.payload is None:
            results.append({**base_result, "status": "failed", "changeLevel": "error", "changes": [], "researchRefreshRecommended": False, "contentReviewRecommended": False, "reviewReasons": [response.error or "Unknown GitHub API failure"]})
            if response.status in {403, 429} and response.rate_limit_remaining == "0":
                break
            continue

        try:
            candidate = build_candidate(current, response.payload, fetched_at)
            validate_snapshot(candidate, project_id)
        except ValueError as error:
            results.append({**base_result, "status": "failed", "changeLevel": "error", "changes": [], "researchRefreshRecommended": False, "contentReviewRecommended": False, "reviewReasons": [str(error)]})
            continue

        changes = compare_snapshots(current, candidate)
        change_level = classify_change(changes)
        reasons = critical_reasons(current, candidate, response.payload, changes)
        if reasons:
            results.append({**base_result, "status": "review-required", "changeLevel": "critical", "changes": changes, "researchRefreshRecommended": False, "contentReviewRecommended": False, "reviewReasons": reasons})
            continue

        updated_dataset[project_id] = candidate
        cache_repositories[cache_key] = {"fullName": candidate["fullName"], "etag": response.etag, "lastCheckedAt": fetched_at}
        results.append({
            **base_result,
            "status": "updated" if changes else "refreshed",
            "changeLevel": change_level,
            "changes": changes,
            "researchRefreshRecommended": change_level in {"activity", "metadata"},
            "contentReviewRecommended": change_level == "metadata",
            "reviewReasons": [],
        })

    return updated_dataset, updated_cache, results


def build_report(generated_at: str, mode: str, data_path: Path, results: list[dict[str, object]], authenticated: bool) -> dict[str, object]:
    summary = {
        "checked": len(results),
        "updated": sum(result["status"] == "updated" for result in results),
        "refreshed": sum(result["status"] == "refreshed" for result in results),
        "reviewRequired": sum(result["status"] == "review-required" for result in results),
        "failed": sum(result["status"] == "failed" for result in results),
        "researchRefreshRecommended": sum(result["researchRefreshRecommended"] is True for result in results),
        "contentReviewRecommended": sum(result["contentReviewRecommended"] is True for result in results),
    }
    return {
        "schemaVersion": 1,
        "generatedAt": generated_at,
        "mode": mode,
        "dataFile": str(data_path),
        "githubApiVersion": API_VERSION,
        "authenticated": authenticated,
        "summary": summary,
        "repositories": results,
    }


def load_cache(path: Path) -> dict[str, object]:
    if not path.exists():
        return {"schemaVersion": 1, "repositories": {}}
    value = read_json(path)
    if not isinstance(value, dict) or value.get("schemaVersion") != 1 or not isinstance(value.get("repositories"), dict):
        raise ValueError("refresh cache has an unsupported shape")
    return value


def main() -> int:
    project_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=project_root / "src/data/repositories.json")
    parser.add_argument("--cache", type=Path, default=project_root / "outputs/refresh/github-cache.json")
    parser.add_argument("--report", type=Path, help="Optional report path; --write defaults to outputs/refresh/latest.json")
    parser.add_argument("--only", action="append", default=[], help="Refresh one project ID; repeat for more")
    parser.add_argument("--write", action="store_true", help="Persist safe repository refreshes, cache, and report")
    parser.add_argument("--api-base", default="https://api.github.com", help=argparse.SUPPRESS)
    parser.add_argument("--timeout", type=float, default=20, help=argparse.SUPPRESS)
    args = parser.parse_args()

    try:
        dataset_value = read_json(args.data)
        if not isinstance(dataset_value, dict) or not dataset_value:
            raise ValueError("repository data must be a non-empty object")
        for project_id, snapshot in dataset_value.items():
            validate_snapshot(snapshot, project_id)
        selected_ids = args.only or list(dataset_value)
        unknown_ids = [project_id for project_id in selected_ids if project_id not in dataset_value]
        if unknown_ids:
            raise ValueError(f"unknown project IDs: {', '.join(unknown_ids)}")
        cache = load_cache(args.cache)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    generated_at = utc_now()
    token = os.environ.get("GITHUB_TOKEN")

    def fetcher(full_name: str, etag: str | None) -> FetchResult:
        return fetch_github_repository(full_name, etag, token, args.api_base, args.timeout)

    updated_dataset, updated_cache, results = refresh_dataset(dataset_value, cache, selected_ids, fetcher, generated_at)
    try:
        report_data_path = args.data.resolve().relative_to(project_root)
    except ValueError:
        report_data_path = args.data.resolve()
    report = build_report(generated_at, "write" if args.write else "dry-run", report_data_path, results, token is not None)
    print(json.dumps(report, ensure_ascii=False, indent=2))

    report_path = args.report or (project_root / "outputs/refresh/latest.json" if args.write else None)
    if args.write:
        write_json_atomic(args.data, updated_dataset)
        write_json_atomic(args.cache, updated_cache)
    if report_path is not None:
        write_json_atomic(report_path, report)

    if report["summary"]["failed"]:
        return 1
    if report["summary"]["reviewRequired"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
