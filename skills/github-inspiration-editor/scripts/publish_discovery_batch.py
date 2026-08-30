#!/usr/bin/env python3
"""Publish a fingerprinted discovery batch after a human merges its review PR."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manage_publication import (  # noqa: E402
    DATA_PATHS,
    apply_project_to_layers,
    create_publication_backup,
    default_check_runner,
    dirty_data_paths,
    incomplete_publication_transactions,
    load_layers,
    read_json,
    restore_publication_backup,
    utc_now,
    validate_artifacts,
    validate_candidate_against_layers,
    write_json_atomic,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]
BATCH_ROOT = PROJECT_ROOT / "outputs/generated/discovery-batches"
MANIFEST_FIELDS = {
    "schemaVersion", "batchId", "createdAt", "status", "sourceDiscovery",
    "candidates", "batchFingerprint", "rejected", "publicationAuthorized",
}
APPROVAL_FIELDS = {
    "schemaVersion", "batchId", "batchFingerprint", "approvedAt", "approvedBy",
    "approvalSource", "sourcePullRequest", "publicationAuthorized",
}


class BatchPublicationError(RuntimeError):
    """Raised when a discovery batch cannot be safely published."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_value(value: object) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def batch_directory(batch_id: str) -> Path:
    if not batch_id or any(character not in "abcdefghijklmnopqrstuvwxyz0123456789-_" for character in batch_id):
        raise BatchPublicationError("invalid batch ID")
    directory = BATCH_ROOT / batch_id
    if not directory.is_dir():
        raise BatchPublicationError(f"discovery batch does not exist: {batch_id}")
    return directory


def resolve_artifact(directory: Path, value: object) -> Path:
    if not isinstance(value, dict) or set(value) != {"path", "sha256"}:
        raise BatchPublicationError("batch artifact entry is invalid")
    relative = value.get("path")
    expected_hash = value.get("sha256")
    if not isinstance(relative, str) or not isinstance(expected_hash, str):
        raise BatchPublicationError("batch artifact path or fingerprint is invalid")
    path = (PROJECT_ROOT / relative).resolve()
    if not path.is_relative_to(directory.resolve()) or not path.is_file():
        raise BatchPublicationError(f"batch artifact path escapes its frozen directory: {relative}")
    if sha256_file(path) != expected_hash:
        raise BatchPublicationError(f"batch artifact fingerprint failed: {relative}")
    return path


def load_batch(batch_id: str) -> tuple[Path, dict[str, object], list[dict[str, object]]]:
    directory = batch_directory(batch_id)
    manifest = read_json(directory / "manifest.json", "discovery batch manifest")
    if not isinstance(manifest, dict) or set(manifest) != MANIFEST_FIELDS:
        raise BatchPublicationError("discovery batch manifest has unexpected fields")
    if manifest.get("schemaVersion") != 1 or manifest.get("batchId") != batch_id:
        raise BatchPublicationError("discovery batch identity is invalid")
    if manifest.get("status") not in {"awaiting-approval", "published"}:
        raise BatchPublicationError(f"discovery batch cannot publish from status {manifest.get('status')}")
    candidates = manifest.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        raise BatchPublicationError("discovery batch must contain at least one candidate")
    core = {
        "batchId": manifest["batchId"],
        "sourceDiscovery": manifest["sourceDiscovery"],
        "candidates": candidates,
    }
    if sha256_value(core) != manifest.get("batchFingerprint"):
        raise BatchPublicationError("discovery batch fingerprint failed")
    loaded: list[dict[str, object]] = []
    project_ids: set[str] = set()
    full_names: set[str] = set()
    github_ids: set[int] = set()
    for candidate in candidates:
        if not isinstance(candidate, dict) or set(candidate) != {"projectId", "fullName", "githubId", "artifacts"}:
            raise BatchPublicationError("discovery batch candidate entry is invalid")
        artifacts = candidate.get("artifacts")
        if not isinstance(artifacts, dict) or set(artifacts) != {"project", "research", "quality"}:
            raise BatchPublicationError("discovery batch candidate artifacts are invalid")
        project_path = resolve_artifact(directory, artifacts["project"])
        research_path = resolve_artifact(directory, artifacts["research"])
        quality_path = resolve_artifact(directory, artifacts["quality"])
        project, _ = validate_artifacts(PROJECT_ROOT, project_path, research_path, quality_path)
        repository = project.get("repository")
        if not isinstance(repository, dict):
            raise BatchPublicationError("candidate repository layer is invalid")
        if project.get("id") != candidate.get("projectId") or repository.get("fullName") != candidate.get("fullName") or repository.get("githubId") != candidate.get("githubId"):
            raise BatchPublicationError("candidate manifest identity does not match its project artifact")
        project_id = str(project["id"])
        full_name = str(repository["fullName"]).lower()
        github_id = int(repository["githubId"])
        if project_id in project_ids or full_name in full_names or github_id in github_ids:
            raise BatchPublicationError("discovery batch contains duplicate repository identities")
        project_ids.add(project_id)
        full_names.add(full_name)
        github_ids.add(github_id)
        loaded.append(project)
    return directory, manifest, loaded


def approval_record(batch_id: str, fingerprint: str, approved_by: str, source_pr: int, *, now: str | None = None) -> dict[str, object]:
    if not approved_by.strip():
        raise BatchPublicationError("approved-by must identify the human who merged the review PR")
    if source_pr <= 0:
        raise BatchPublicationError("source PR number must be positive")
    return {
        "schemaVersion": 1,
        "batchId": batch_id,
        "batchFingerprint": fingerprint,
        "approvedAt": now or utc_now(),
        "approvedBy": approved_by.strip(),
        "approvalSource": "merged-review-pull-request",
        "sourcePullRequest": source_pr,
        "publicationAuthorized": True,
    }


def publish_batch(batch_id: str, approved_by: str, source_pr: int, *, write: bool = False, run_checks=default_check_runner, now: str | None = None) -> dict[str, object]:
    directory, manifest, projects = load_batch(batch_id)
    if manifest.get("status") == "published":
        return {
            "mode": "write" if write else "dry-run",
            "batchId": batch_id,
            "status": "already-published",
            "candidateCount": len(projects),
            "publicationAuthorized": True,
        }
    approval = approval_record(batch_id, str(manifest["batchFingerprint"]), approved_by, source_pr, now=now)
    dirty = dirty_data_paths(PROJECT_ROOT)
    if dirty:
        raise BatchPublicationError("published data has uncommitted changes: " + " | ".join(dirty))
    incomplete = incomplete_publication_transactions(PROJECT_ROOT)
    if incomplete:
        raise BatchPublicationError("unfinished publication transaction requires recovery first: " + ", ".join(incomplete))

    layers = load_layers(PROJECT_ROOT)
    published_ids = set(layers[0])
    published_full_names = {
        str(item.get("fullName", "")).lower()
        for item in layers[1].values()
        if isinstance(item, dict)
    }
    published_github_ids = {
        item.get("githubId")
        for item in layers[1].values()
        if isinstance(item, dict)
    }
    for project in projects:
        repository = project["repository"]
        assert isinstance(repository, dict)
        if project["id"] in published_ids or str(repository["fullName"]).lower() in published_full_names or repository["githubId"] in published_github_ids:
            raise BatchPublicationError(f"candidate now duplicates a published project: {repository['fullName']}")
        insert_after = layers[0][-1]
        validate_candidate_against_layers(project, "add", insert_after, layers)
        layers = apply_project_to_layers(project, "add", insert_after, layers)
        published_ids.add(str(project["id"]))
        published_full_names.add(str(repository["fullName"]).lower())
        published_github_ids.add(repository["githubId"])

    plan = {
        "mode": "write" if write else "dry-run",
        "batchId": batch_id,
        "candidateCount": len(projects),
        "projectIds": [project["id"] for project in projects],
        "approvedBy": approved_by,
        "sourcePullRequest": source_pr,
        "changedFiles": list(DATA_PATHS),
        "publicationAuthorized": True,
    }
    if not write:
        return plan

    transaction_id = f"publish-batch-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    backup = create_publication_backup(PROJECT_ROOT, transaction_id, f"batch-{batch_id}")
    write_json_atomic(directory / "approval.json", approval)
    try:
        for relative, value in zip(DATA_PATHS, layers):
            write_json_atomic(PROJECT_ROOT / relative, value)
        checks = run_checks(PROJECT_ROOT)
        manifest["status"] = "published"
        manifest["publicationAuthorized"] = True
        write_json_atomic(directory / "manifest.json", manifest)
        transaction = read_json(backup / "manifest.json", "publication transaction")
        assert isinstance(transaction, dict)
        transaction.update({
            "status": "published",
            "publishedAt": now or utc_now(),
            "batchId": batch_id,
            "sourcePullRequest": source_pr,
            "checks": checks,
        })
        write_json_atomic(backup / "manifest.json", transaction)
        return {**plan, "status": "published", "transactionId": transaction_id, "checks": checks, "rolledBack": False}
    except Exception as error:
        restore_publication_backup(PROJECT_ROOT, backup)
        manifest["status"] = "publication-failed"
        manifest["publicationAuthorized"] = False
        write_json_atomic(directory / "manifest.json", manifest)
        transaction = read_json(backup / "manifest.json", "publication transaction")
        assert isinstance(transaction, dict)
        transaction.update({"status": "rolled-back", "rolledBackAt": now or utc_now(), "error": str(error), "batchId": batch_id})
        write_json_atomic(backup / "manifest.json", transaction)
        raise BatchPublicationError(f"batch publication failed and all feed data was restored: {error}") from error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch_id")
    parser.add_argument("--approved-by", required=True)
    parser.add_argument("--source-pr", type=int, required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        result = publish_batch(args.batch_id, args.approved_by, args.source_pr, write=args.write)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (BatchPublicationError, OSError, ValueError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
