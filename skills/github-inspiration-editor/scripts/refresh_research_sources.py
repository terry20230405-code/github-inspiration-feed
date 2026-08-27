#!/usr/bin/env python3
"""Compare published repositories' research signals and create review evidence bundles."""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from refresh_repositories import API_VERSION, SSL_CONTEXT, read_json, validate_snapshot, write_json_atomic


USER_AGENT = "github-inspiration-feed-research-refresh"
SIGNALS = ("metadata", "readme", "release")
MAX_README_CHARACTERS = 250_000
MAX_RELEASE_CHARACTERS = 100_000
REVIEW_ACTIONS = {"keep-published", "draft", "human-decision"}
REVIEW_IMPACTS = {"none", "minor", "meaningful", "critical"}
EDITORIAL_FIELDS = {
    "editorial.hook", "editorial.summary", "editorial.meaning", "editorial.audience",
    "editorial.features", "editorial.stack", "editorial.opportunity", "editorial.directions",
}


@dataclass(frozen=True)
class SourceFetchResult:
    status: int
    payload: dict[str, object] | None
    etag: str | None
    rate_limit_remaining: str | None
    error: str | None = None


SourceFetcher = Callable[[str, str, str | None], SourceFetchResult]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def source_fingerprint(snapshot: dict[str, object]) -> str:
    stable = {key: value for key, value in snapshot.items() if key not in {"capturedAt", "fingerprint"}}
    serialized = json.dumps(stable, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256_text(serialized)


def required_value(payload: dict[str, object], field: str, expected_type: type) -> object:
    value = payload.get(field)
    if not isinstance(value, expected_type) or expected_type is int and isinstance(value, bool):
        raise ValueError(f"GitHub response has an invalid {field}")
    return value


def nullable_text(value: object) -> str | None:
    return value.strip() if isinstance(value, str) and value.strip() else None


def build_metadata(payload: dict[str, object], repository: dict[str, object]) -> dict[str, object]:
    github_id = required_value(payload, "id", int)
    full_name = required_value(payload, "full_name", str)
    if github_id != repository["githubId"]:
        raise ValueError("repository identity changed during source inspection")
    if str(full_name).casefold() != str(repository["fullName"]).casefold():
        raise ValueError("repository full name changed during source inspection")
    if payload.get("private") is True:
        raise ValueError("repository became private or requires different access")
    if payload.get("fork") is True:
        raise ValueError("canonical repository is now reported as a fork")
    if payload.get("archived") is True or payload.get("disabled") is True:
        raise ValueError("repository is archived or disabled")
    default_branch = required_value(payload, "default_branch", str)
    topics = payload.get("topics", [])
    if not isinstance(topics, list) or not all(isinstance(topic, str) and topic for topic in topics):
        raise ValueError("GitHub response has invalid topics")
    return {
        "githubId": github_id,
        "fullName": full_name,
        "defaultBranch": default_branch,
        "description": nullable_text(payload.get("description")),
        "homepage": nullable_text(payload.get("homepage")),
        "topics": sorted(set(topics), key=str.casefold),
    }


def build_readme(payload: dict[str, object]) -> tuple[dict[str, object], dict[str, object]]:
    sha = required_value(payload, "sha", str)
    path = required_value(payload, "path", str)
    html_url = required_value(payload, "html_url", str)
    encoding = required_value(payload, "encoding", str)
    content_value = required_value(payload, "content", str)
    if encoding != "base64":
        raise ValueError("README response must use base64 encoding")
    try:
        raw_content = base64.b64decode(content_value, validate=False)
        content = raw_content.decode("utf-8")
    except (ValueError, UnicodeDecodeError) as error:
        raise ValueError(f"README content could not be decoded: {error}") from error
    truncated = len(content) > MAX_README_CHARACTERS
    state = {"sha": sha, "path": path, "htmlUrl": html_url, "contentSha256": hashlib.sha256(raw_content).hexdigest()}
    evidence = {**state, "content": content[:MAX_README_CHARACTERS], "contentTruncated": truncated}
    return state, evidence


def build_release(payload: dict[str, object]) -> tuple[dict[str, object], dict[str, object]]:
    release_id = required_value(payload, "id", int)
    tag_name = required_value(payload, "tag_name", str)
    html_url = required_value(payload, "html_url", str)
    published_at = required_value(payload, "published_at", str)
    name = nullable_text(payload.get("name")) or tag_name
    body = payload.get("body") if isinstance(payload.get("body"), str) else ""
    state = {
        "id": release_id,
        "tagName": tag_name,
        "name": name,
        "publishedAt": published_at,
        "htmlUrl": html_url,
        "bodySha256": sha256_text(body),
    }
    evidence = {**state, "body": body[:MAX_RELEASE_CHARACTERS], "bodyTruncated": len(body) > MAX_RELEASE_CHARACTERS}
    return state, evidence


def compare_source_snapshots(previous: dict[str, object] | None, candidate: dict[str, object]) -> tuple[str, list[dict[str, object]]]:
    if previous is None:
        return "baseline", [{"field": "sourceBaseline", "before": None, "after": "created", "level": "baseline"}]
    changes: list[dict[str, object]] = []
    for field in ("defaultBranch", "description", "homepage", "topics"):
        if previous.get(field) != candidate.get(field):
            changes.append({"field": field, "before": previous.get(field), "after": candidate.get(field), "level": "source-metadata"})
    previous_readme = previous.get("readme") if isinstance(previous.get("readme"), dict) else None
    candidate_readme = candidate.get("readme") if isinstance(candidate.get("readme"), dict) else None
    for field in ("sha", "path", "contentSha256"):
        before = previous_readme.get(field) if previous_readme else None
        after = candidate_readme.get(field) if candidate_readme else None
        if before != after:
            changes.append({"field": f"readme.{field}", "before": before, "after": after, "level": "readme"})
    previous_release = previous.get("latestRelease") if isinstance(previous.get("latestRelease"), dict) else None
    candidate_release = candidate.get("latestRelease") if isinstance(candidate.get("latestRelease"), dict) else None
    for field in ("id", "tagName", "publishedAt", "bodySha256"):
        before = previous_release.get(field) if previous_release else None
        after = candidate_release.get(field) if candidate_release else None
        if before != after:
            changes.append({"field": f"latestRelease.{field}", "before": before, "after": after, "level": "release"})
    return ("source-changed" if changes else "unchanged"), changes


def fetch_github_source(
    full_name: str,
    signal: str,
    etag: str | None,
    token: str | None,
    api_base: str = "https://api.github.com",
    timeout: float = 20,
) -> SourceFetchResult:
    owner, repository = full_name.split("/", 1)
    root = f"{api_base.rstrip('/')}/repos/{urllib.parse.quote(owner, safe='')}/{urllib.parse.quote(repository, safe='')}"
    suffix = {"metadata": "", "readme": "/readme", "release": "/releases/latest"}[signal]
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": API_VERSION,
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if etag:
        headers["If-None-Match"] = etag
    request = urllib.request.Request(root + suffix, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=SSL_CONTEXT) as response:
            payload = json.loads(response.read().decode("utf-8"))
            if not isinstance(payload, dict):
                return SourceFetchResult(response.status, None, response.headers.get("etag"), response.headers.get("x-ratelimit-remaining"), "GitHub returned a non-object response")
            return SourceFetchResult(response.status, payload, response.headers.get("etag"), response.headers.get("x-ratelimit-remaining"))
    except urllib.error.HTTPError as error:
        remaining = error.headers.get("x-ratelimit-remaining")
        if error.code == 304:
            return SourceFetchResult(304, None, etag, remaining)
        if error.code == 404:
            message = "No preferred README was found" if signal == "readme" else "No published release was found" if signal == "release" else "Repository was not found or is inaccessible"
            return SourceFetchResult(404, None, None, remaining, message)
        if error.code in {403, 429} and remaining == "0":
            reset = error.headers.get("x-ratelimit-reset") or "unknown"
            return SourceFetchResult(error.code, None, None, remaining, f"GitHub rate limit reached; reset epoch is {reset}")
        return SourceFetchResult(error.code, None, None, remaining, f"GitHub request failed with HTTP {error.code}")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        return SourceFetchResult(0, None, None, None, f"GitHub request failed: {error}")


def validate_review(review: object, project_id: str, fingerprint: str) -> list[str]:
    errors: list[str] = []
    expected = {"schemaVersion", "projectId", "sourceFingerprint", "reviewedAt", "impact", "summary", "affectedFields", "evidence", "recommendedAction", "publicationAuthorized"}
    if not isinstance(review, dict):
        return ["review must be an object"]
    if set(review) != expected:
        errors.append("review fields do not match the stage-seven contract")
    if review.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    if review.get("projectId") != project_id:
        errors.append("projectId does not match the evidence bundle")
    if review.get("sourceFingerprint") != fingerprint:
        errors.append("sourceFingerprint does not match the current source snapshot")
    reviewed_at = review.get("reviewedAt")
    if not isinstance(reviewed_at, str) or not reviewed_at.endswith("Z"):
        errors.append("reviewedAt must be a UTC timestamp ending in Z")
    impact = review.get("impact")
    action = review.get("recommendedAction")
    if impact not in REVIEW_IMPACTS:
        errors.append("impact is invalid")
    if action not in REVIEW_ACTIONS:
        errors.append("recommendedAction is invalid")
    if impact == "none" and action != "keep-published":
        errors.append("impact none requires keep-published")
    if impact == "meaningful" and action != "draft":
        errors.append("meaningful impact requires draft")
    if impact == "critical" and action != "human-decision":
        errors.append("critical impact requires human-decision")
    if not isinstance(review.get("summary"), str) or not str(review.get("summary")).strip():
        errors.append("summary must be non-empty")
    affected = review.get("affectedFields")
    if not isinstance(affected, list) or not all(field in EDITORIAL_FIELDS for field in affected):
        errors.append("affectedFields contains unsupported fields")
    evidence = review.get("evidence")
    if not isinstance(evidence, list) or not evidence or not all(
        isinstance(item, dict) and isinstance(item.get("sourceId"), str) and item.get("sourceId", "").startswith("S") and isinstance(item.get("finding"), str) and item.get("finding", "").strip()
        for item in evidence
    ):
        errors.append("evidence must contain at least one source finding")
    if review.get("publicationAuthorized") is not False:
        errors.append("publicationAuthorized must be false")
    return errors


def refresh_sources(
    dataset: dict[str, object],
    source_state: dict[str, object],
    cache: dict[str, object],
    selected_ids: list[str],
    fetcher: SourceFetcher,
    captured_at: str,
    reviews: dict[str, object] | None = None,
) -> tuple[dict[str, object], dict[str, object], list[dict[str, object]], dict[str, dict[str, object]]]:
    updated_state = copy.deepcopy(source_state)
    updated_cache = copy.deepcopy(cache)
    state_repositories = updated_state.setdefault("repositories", {})
    cache_repositories = updated_cache.setdefault("repositories", {})
    if not isinstance(state_repositories, dict) or not isinstance(cache_repositories, dict):
        raise ValueError("source state and cache repositories must be objects")
    reviews = reviews or {}
    results: list[dict[str, object]] = []
    bundles: dict[str, dict[str, object]] = {}
    stop_queue = False

    for project_id in selected_ids:
        repository = validate_snapshot(dataset[project_id], project_id)
        previous = state_repositories.get(project_id)
        previous = previous if isinstance(previous, dict) else None
        candidate = copy.deepcopy(previous) if previous else {
            "githubId": repository["githubId"],
            "fullName": repository["fullName"],
            "defaultBranch": None,
            "description": None,
            "homepage": None,
            "topics": [],
            "readme": None,
            "latestRelease": None,
        }
        cache_key = str(repository["githubId"])
        cached_signals = cache_repositories.get(cache_key)
        cached_signals = cached_signals if isinstance(cached_signals, dict) else {}
        next_cache = copy.deepcopy(cached_signals)
        source_entries: list[dict[str, object]] = []
        rate_remaining: str | None = None
        project_error: tuple[str, str] | None = None

        for source_index, signal in enumerate(SIGNALS, start=1):
            cached_signal = cached_signals.get(signal)
            cached_etag = cached_signal.get("etag") if isinstance(cached_signal, dict) and isinstance(cached_signal.get("etag"), str) and previous is not None else None
            response = fetcher(str(repository["fullName"]), signal, cached_etag)
            rate_remaining = response.rate_limit_remaining
            source_id = f"S{source_index}"

            if response.status == 304:
                if previous is None:
                    project_error = ("failed", f"{signal} returned 304 without a stored source baseline")
                    break
                source_entries.append({"id": source_id, "kind": signal, "retrievalStatus": "not-modified", "content": None})
                next_cache[signal] = {"etag": response.etag, "lastCheckedAt": captured_at}
                continue

            if response.status == 404 and signal in {"readme", "release"}:
                key = "readme" if signal == "readme" else "latestRelease"
                candidate[key] = None
                source_entries.append({"id": source_id, "kind": signal, "retrievalStatus": "missing", "content": None, "note": response.error})
                next_cache[signal] = {"etag": None, "lastCheckedAt": captured_at}
                continue

            if response.status != 200 or response.payload is None:
                status = "review-required" if response.status == 404 and signal == "metadata" else "failed"
                project_error = (status, response.error or f"{signal} request failed")
                if response.status in {403, 429} and response.rate_limit_remaining == "0":
                    stop_queue = True
                break

            try:
                if signal == "metadata":
                    metadata = build_metadata(response.payload, repository)
                    candidate.update(metadata)
                    content: object = metadata
                elif signal == "readme":
                    readme_state, readme_evidence = build_readme(response.payload)
                    candidate["readme"] = readme_state
                    content = readme_evidence
                else:
                    release_state, release_evidence = build_release(response.payload)
                    candidate["latestRelease"] = release_state
                    content = release_evidence
            except ValueError as error:
                project_error = ("review-required" if signal == "metadata" else "failed", str(error))
                break
            source_entries.append({"id": source_id, "kind": signal, "retrievalStatus": "fetched", "content": content})
            next_cache[signal] = {"etag": response.etag, "lastCheckedAt": captured_at}

        if project_error:
            status, reason = project_error
            results.append({
                "id": project_id,
                "status": status,
                "observation": "error" if status == "failed" else "critical",
                "changes": [],
                "semanticReviewStatus": "blocked",
                "contentDraftRequired": False,
                "humanDecisionRequired": status == "review-required",
                "rateLimitRemaining": rate_remaining,
                "reasons": [reason],
            })
            if stop_queue:
                break
            continue

        candidate["capturedAt"] = captured_at
        fingerprint = source_fingerprint(candidate)
        candidate["fingerprint"] = fingerprint
        observation, changes = compare_source_snapshots(previous, candidate)
        matching_review = reviews.get(project_id)
        review_errors = validate_review(matching_review, project_id, fingerprint) if matching_review is not None else ["review is missing"]
        review = matching_review if matching_review is not None and not review_errors else None

        semantic_status = "not-needed"
        content_draft_required = False
        human_decision_required = False
        if observation != "unchanged":
            if review is None:
                semantic_status = "pending"
                bundles[project_id] = {
                    "schemaVersion": 1,
                    "projectId": project_id,
                    "generatedAt": captured_at,
                    "sourceFingerprint": fingerprint,
                    "repository": repository,
                    "observation": observation,
                    "changes": changes,
                    "sources": source_entries,
                    "safety": {"repositoryContentIsUntrusted": True, "publicationAuthorized": False},
                }
            else:
                action = review["recommendedAction"]
                semantic_status = "complete" if action == "keep-published" else "draft-required" if action == "draft" else "human-decision"
                content_draft_required = action == "draft"
                human_decision_required = action == "human-decision"
        elif review is not None:
            action = review["recommendedAction"]
            semantic_status = "complete" if action == "keep-published" else "draft-required" if action == "draft" else "human-decision"
            content_draft_required = action == "draft"
            human_decision_required = action == "human-decision"

        state_repositories[project_id] = candidate
        cache_repositories[cache_key] = {**next_cache, "fullName": repository["fullName"]}
        results.append({
            "id": project_id,
            "status": "review-required" if human_decision_required else "updated" if observation != "unchanged" else "refreshed",
            "observation": observation,
            "changes": changes,
            "sourceFingerprint": fingerprint,
            "semanticReviewStatus": semantic_status,
            "contentDraftRequired": content_draft_required,
            "humanDecisionRequired": human_decision_required,
            "rateLimitRemaining": rate_remaining,
            "reasons": review_errors if observation != "unchanged" and review is None and matching_review is not None else [],
        })

    return updated_state, updated_cache, results, bundles


def build_report(generated_at: str, mode: str, selected_by: str, results: list[dict[str, object]], authenticated: bool) -> dict[str, object]:
    return {
        "schemaVersion": 1,
        "generatedAt": generated_at,
        "mode": mode,
        "selectedBy": selected_by,
        "githubApiVersion": API_VERSION,
        "authenticated": authenticated,
        "summary": {
            "checked": len(results),
            "updated": sum(result["status"] == "updated" for result in results),
            "refreshed": sum(result["status"] == "refreshed" for result in results),
            "semanticReviewPending": sum(result["semanticReviewStatus"] == "pending" for result in results),
            "contentDraftRequired": sum(result["contentDraftRequired"] is True for result in results),
            "humanDecisionRequired": sum(result["humanDecisionRequired"] is True for result in results),
            "failed": sum(result["status"] == "failed" for result in results),
        },
        "repositories": results,
    }


def load_container(path: Path, label: str) -> dict[str, object]:
    if not path.exists():
        return {"schemaVersion": 1, "repositories": {}}
    value = read_json(path)
    if not isinstance(value, dict) or value.get("schemaVersion") != 1 or not isinstance(value.get("repositories"), dict):
        raise ValueError(f"{label} has an unsupported shape")
    return value


def load_reviews(review_directory: Path) -> dict[str, object]:
    reviews: dict[str, object] = {}
    if not review_directory.exists():
        return reviews
    for path in review_directory.glob("*.review.json"):
        try:
            value = read_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(value, dict) and isinstance(value.get("projectId"), str):
            reviews[value["projectId"]] = value
    return reviews


def selected_from_stage_six(report: object, dataset: dict[str, object]) -> list[str]:
    if not isinstance(report, dict) or report.get("schemaVersion") != 1 or not isinstance(report.get("repositories"), list):
        raise ValueError("stage-six report has an unsupported shape")
    summary = report.get("summary")
    if not isinstance(summary, dict) or summary.get("failed", 0) or summary.get("reviewRequired", 0):
        raise ValueError("stage-six report contains failures or mandatory human review")
    selected: list[str] = []
    for result in report["repositories"]:
        if not isinstance(result, dict):
            continue
        project_id = result.get("id")
        if project_id in dataset and (result.get("researchRefreshRecommended") is True or result.get("contentReviewRecommended") is True):
            selected.append(str(project_id))
    return selected


def main() -> int:
    project_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=project_root / "src/data/repositories.json")
    parser.add_argument("--stage-six-report", type=Path, default=project_root / "outputs/refresh/latest.json")
    parser.add_argument("--state", type=Path, default=project_root / "outputs/refresh/source-state.json")
    parser.add_argument("--cache", type=Path, default=project_root / "outputs/refresh/source-cache.json")
    parser.add_argument("--report", type=Path, help="Optional report path; --write defaults to outputs/refresh/research-latest.json")
    parser.add_argument("--evidence-dir", type=Path, default=project_root / "outputs/generated/research-refresh")
    parser.add_argument("--only", action="append", default=[], help="Inspect one project ID; repeat for more")
    parser.add_argument("--all", action="store_true", help="Inspect every published project instead of the stage-six queue")
    parser.add_argument("--write", action="store_true", help="Persist source state, cache, report, and pending evidence bundles")
    parser.add_argument("--api-base", default="https://api.github.com", help=argparse.SUPPRESS)
    parser.add_argument("--timeout", type=float, default=20, help=argparse.SUPPRESS)
    args = parser.parse_args()

    try:
        dataset_value = read_json(args.data)
        if not isinstance(dataset_value, dict) or not dataset_value:
            raise ValueError("repository data must be a non-empty object")
        for project_id, snapshot in dataset_value.items():
            validate_snapshot(snapshot, project_id)
        source_state = load_container(args.state, "source state")
        cache = load_container(args.cache, "source cache")
        if args.only:
            selected_ids = args.only
            selected_by = "only"
        elif args.all:
            selected_ids = list(dataset_value)
            selected_by = "all"
        else:
            selected_ids = selected_from_stage_six(read_json(args.stage_six_report), dataset_value)
            selected_by = "stage-six-report"
        unknown = [project_id for project_id in selected_ids if project_id not in dataset_value]
        if unknown:
            raise ValueError(f"unknown project IDs: {', '.join(unknown)}")
        reviews = load_reviews(args.evidence_dir)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    generated_at = utc_now()
    token = os.environ.get("GITHUB_TOKEN")

    def fetcher(full_name: str, signal: str, etag: str | None) -> SourceFetchResult:
        return fetch_github_source(full_name, signal, etag, token, args.api_base, args.timeout)

    updated_state, updated_cache, results, bundles = refresh_sources(dataset_value, source_state, cache, selected_ids, fetcher, generated_at, reviews)
    report = build_report(generated_at, "write" if args.write else "dry-run", selected_by, results, token is not None)
    print(json.dumps(report, ensure_ascii=False, indent=2))

    report_path = args.report or (project_root / "outputs/refresh/research-latest.json" if args.write else None)
    if args.write:
        write_json_atomic(args.state, updated_state)
        write_json_atomic(args.cache, updated_cache)
        for project_id, bundle in bundles.items():
            write_json_atomic(args.evidence_dir / f"{project_id}.source.json", bundle)
    if report_path is not None:
        write_json_atomic(report_path, report)

    if report["summary"]["failed"]:
        return 1
    if report["summary"]["humanDecisionRequired"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
