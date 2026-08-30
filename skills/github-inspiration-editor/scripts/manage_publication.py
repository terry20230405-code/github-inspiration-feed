#!/usr/bin/env python3
"""Prepare, approve, publish, and roll back inspiration-feed candidates."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate_visual_identity import colors_are_distinct  # noqa: E402
from validate_project import validate as validate_project  # noqa: E402
from validate_quality_review import validate as validate_quality  # noqa: E402
from validate_research import validate as validate_research  # noqa: E402


SCHEMA_VERSION = 1
DATA_PATHS = (
    "src/data/order.json",
    "src/data/repositories.json",
    "src/data/editorial.json",
    "src/data/visuals.json",
)
CANDIDATE_ROOT = "outputs/generated/publication-candidates"
TRANSACTION_ROOT = "outputs/versions/publications"
MANIFEST_FIELDS = {
    "schemaVersion", "candidateId", "createdAt", "status", "mode", "projectId",
    "fullName", "githubId", "insertAfter", "artifacts", "candidateFingerprint",
    "baselineDataFingerprint", "publicationAuthorized",
}
APPROVAL_FIELDS = {
    "schemaVersion", "candidateId", "candidateFingerprint", "approvedAt",
    "approvedBy", "publicationAuthorized",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path, label: str) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"{label} could not be read: {error}") from error


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_value(value: object) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f".{uuid.uuid4().hex[:8]}.tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, path)


def write_json_atomic(path: Path, value: object) -> None:
    write_text_atomic(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def load_layers(project_root: Path) -> tuple[list[str], dict[str, object], dict[str, object], dict[str, object]]:
    values = [read_json(project_root / relative, relative) for relative in DATA_PATHS]
    order, repositories, editorial, visuals = values
    if not isinstance(order, list) or not order or not all(isinstance(item, str) for item in order):
        raise ValueError("src/data/order.json must be a non-empty string array")
    if len(order) != len(set(order)):
        raise ValueError("src/data/order.json contains duplicate IDs")
    if not all(isinstance(layer, dict) for layer in (repositories, editorial, visuals)):
        raise ValueError("published data layers must be JSON objects")
    expected = set(order)
    for name, layer in (("repositories", repositories), ("editorial", editorial), ("visuals", visuals)):
        if set(layer) != expected:
            raise ValueError(f"{name} IDs do not match order.json")
    return order, repositories, editorial, visuals


def data_fingerprint(project_root: Path) -> str:
    return sha256_value({relative: sha256_file(project_root / relative) for relative in DATA_PATHS})


def dirty_data_paths(project_root: Path) -> list[str]:
    if not (project_root / ".git").exists():
        return []
    command = ["git", "status", "--porcelain", "--", *DATA_PATHS]
    result = subprocess.run(command, cwd=project_root, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise ValueError(f"Git data-state check failed: {result.stderr.strip()}")
    return [line for line in result.stdout.splitlines() if line.strip()]


def validate_artifacts(project_root: Path, project_path: Path, research_path: Path, quality_path: Path) -> tuple[dict[str, object], dict[str, object]]:
    project = read_json(project_path, "project artifact")
    if not isinstance(project, dict):
        raise ValueError("project artifact must be a JSON object")
    project_errors = validate_project(project)
    if project_errors:
        raise ValueError("project validation failed: " + "; ".join(project_errors))
    research_text = research_path.read_text(encoding="utf-8")
    research_errors = validate_research(research_text)
    if research_errors:
        raise ValueError("research validation failed: " + "; ".join(research_errors))
    quality = read_json(quality_path, "quality review")
    quality_errors = validate_quality(quality, project_root)
    if quality_errors:
        raise ValueError("quality review failed: " + "; ".join(quality_errors))
    if quality.get("projectId") != project.get("id"):
        raise ValueError("quality review projectId does not match the project artifact")
    if quality.get("projectSha256") != sha256_file(project_path) or quality.get("researchSha256") != sha256_file(research_path):
        raise ValueError("quality review fingerprints do not match the supplied artifacts")
    return project, quality


def insertion_index(order: list[str], insert_after: str | None) -> int:
    if insert_after is None:
        return len(order)
    if insert_after not in order:
        raise ValueError(f"insert-after project does not exist: {insert_after}")
    return order.index(insert_after) + 1


def validate_candidate_against_layers(
    project: dict[str, object],
    mode: str,
    insert_after: str | None,
    layers: tuple[list[str], dict[str, object], dict[str, object], dict[str, object]],
) -> dict[str, object]:
    order, repositories, editorial, visuals = layers
    project_id = project["id"]
    repository = project["repository"]
    visual = project["visual"]
    assert isinstance(project_id, str) and isinstance(repository, dict) and isinstance(visual, dict)
    matching_id = project_id in repositories
    matching_full_name = [item_id for item_id, item in repositories.items() if isinstance(item, dict) and str(item.get("fullName", "")).lower() == str(repository["fullName"]).lower()]
    matching_github_id = [item_id for item_id, item in repositories.items() if isinstance(item, dict) and item.get("githubId") == repository["githubId"]]

    if mode == "add":
        duplicates = sorted(set(([project_id] if matching_id else []) + matching_full_name + matching_github_id))
        if duplicates:
            raise ValueError(f"candidate duplicates published project(s): {', '.join(duplicates)}")
        if visual.get("generatorVersion") != 2:
            raise ValueError("new projects must use visual generator version 2")
        if visual.get("seed") != repository.get("fullName"):
            raise ValueError("new project visual.seed must match repository.fullName")
        index = insertion_index(order, insert_after)
        previous_id = order[index - 1] if index > 0 else None
        next_id = order[index] if index < len(order) else None
        accent = visual["accent"]
        for neighbor_id in (previous_id, next_id):
            if neighbor_id is None:
                continue
            neighbor = visuals[neighbor_id]
            assert isinstance(neighbor, dict)
            if not colors_are_distinct(str(accent), str(neighbor["accent"])):
                raise ValueError(f"candidate accent {accent} is too close to adjacent project {neighbor_id} ({neighbor['accent']})")
    elif mode == "replace":
        if not matching_id:
            raise ValueError("replace mode requires an existing project ID")
        current_repository = repositories[project_id]
        if not isinstance(current_repository, dict) or current_repository.get("githubId") != repository.get("githubId") or str(current_repository.get("fullName", "")).lower() != str(repository.get("fullName", "")).lower():
            raise ValueError("replace mode cannot change repository identity")
        if repository != current_repository:
            raise ValueError("replace mode cannot change refresh-managed repository metadata")
        if visual != visuals[project_id]:
            raise ValueError("replace mode cannot change the persisted visual identity")
        if insert_after is not None:
            raise ValueError("replace mode cannot change feed order")
        previous_id = order[order.index(project_id) - 1] if order.index(project_id) > 0 else None
        next_id = order[order.index(project_id) + 1] if order.index(project_id) + 1 < len(order) else None
    else:
        raise ValueError("mode must be add or replace")

    return {
        "previous": {"id": previous_id, "accent": visuals[previous_id]["accent"]} if previous_id else None,
        "next": {"id": next_id, "accent": visuals[next_id]["accent"]} if next_id else None,
    }


def candidate_directory(project_root: Path, candidate_id: str) -> Path:
    if not candidate_id or any(character not in "abcdefghijklmnopqrstuvwxyz0123456789-_" for character in candidate_id):
        raise ValueError("invalid candidate ID")
    return project_root / CANDIDATE_ROOT / candidate_id


def candidate_fingerprint(manifest_core: dict[str, object]) -> str:
    return sha256_value(manifest_core)


def preview_markdown(project: dict[str, object], mode: str, insert_after: str | None, neighbors: dict[str, object]) -> str:
    repository = project["repository"]
    editorial = project["editorial"]
    visual = project["visual"]
    assert isinstance(repository, dict) and isinstance(editorial, dict) and isinstance(visual, dict)
    directions = editorial["directions"]
    assert isinstance(directions, list)
    lines = [
        f"# 发布预览：{repository['fullName']}",
        "",
        f"- 操作：{'新增项目' if mode == 'add' else '替换已发布中文内容'}",
        f"- 插入位置：{'末尾' if insert_after is None else f'{insert_after} 之后'}",
        f"- 上一个项目：{neighbors['previous']['id'] if neighbors['previous'] else '无'}",
        f"- 下一个项目：{neighbors['next']['id'] if neighbors['next'] else '无'}",
        f"- 主题色：{visual['accent']}",
        f"- 图案：{visual['motif']}",
        f"- 许可证：{repository['license']}",
        "",
        "## 页面内容",
        "",
        f"- Hook：{editorial['hook']}",
        f"- 原项目介绍：{editorial['summary']}",
        f"- 适合谁：{editorial['audience']}",
        "",
        "## 改造方向",
        "",
    ]
    for direction in directions:
        assert isinstance(direction, dict)
        lines.append(f"- {direction['name']}：{direction['tagline']}")
    lines.extend(["", "这只是预览，不代表已批准发布。", ""])
    return "\n".join(lines)


def prepare_candidate(
    project_root: Path,
    project_path: Path,
    research_path: Path,
    quality_path: Path,
    *,
    mode: str = "add",
    insert_after: str | None = None,
    write: bool = False,
    now: Callable[[], str] = utc_now,
) -> dict[str, object]:
    project_root = project_root.resolve()
    dirty = dirty_data_paths(project_root)
    if dirty:
        raise ValueError("published data has uncommitted changes; commit or restore it before preparing a candidate: " + " | ".join(dirty))
    project, _ = validate_artifacts(project_root, project_path.resolve(), research_path.resolve(), quality_path.resolve())
    layers = load_layers(project_root)
    neighbors = validate_candidate_against_layers(project, mode, insert_after, layers)
    project_hash = sha256_file(project_path)
    research_hash = sha256_file(research_path)
    quality_hash = sha256_file(quality_path)
    project_id = str(project["id"])
    candidate_id = f"{project_id}-{project_hash[:12]}"
    repository = project["repository"]
    assert isinstance(repository, dict)
    artifacts = {
        "project": {"file": "project.json", "sha256": project_hash},
        "research": {"file": "research.md", "sha256": research_hash},
        "quality": {"file": "quality.json", "sha256": quality_hash},
    }
    core = {
        "mode": mode,
        "projectId": project_id,
        "fullName": repository["fullName"],
        "githubId": repository["githubId"],
        "insertAfter": insert_after,
        "artifacts": artifacts,
    }
    manifest = {
        "schemaVersion": SCHEMA_VERSION,
        "candidateId": candidate_id,
        "createdAt": now(),
        "status": "awaiting-approval",
        **core,
        "candidateFingerprint": candidate_fingerprint(core),
        "baselineDataFingerprint": data_fingerprint(project_root),
        "publicationAuthorized": False,
    }
    result = {
        "mode": "write" if write else "dry-run",
        "candidateId": candidate_id,
        "status": manifest["status"],
        "projectId": project_id,
        "neighbors": neighbors,
        "candidateFingerprint": manifest["candidateFingerprint"],
        "publicationAuthorized": False,
    }
    if not write:
        return result
    destination = candidate_directory(project_root, candidate_id)
    if destination.exists():
        raise ValueError(f"candidate already exists: {candidate_id}")
    temporary = destination.with_name(destination.name + f".prepare-{uuid.uuid4().hex[:8]}")
    temporary.mkdir(parents=True)
    try:
        shutil.copy2(project_path, temporary / "project.json")
        shutil.copy2(research_path, temporary / "research.md")
        shutil.copy2(quality_path, temporary / "quality.json")
        write_json_atomic(temporary / "manifest.json", manifest)
        write_text_atomic(temporary / "preview.md", preview_markdown(project, mode, insert_after, neighbors))
        destination.parent.mkdir(parents=True, exist_ok=True)
        os.replace(temporary, destination)
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
    result["candidatePath"] = destination.relative_to(project_root).as_posix()
    return result


def load_candidate(project_root: Path, candidate_id: str) -> tuple[Path, dict[str, object]]:
    directory = candidate_directory(project_root.resolve(), candidate_id)
    manifest = read_json(directory / "manifest.json", "candidate manifest")
    if not isinstance(manifest, dict) or set(manifest) != MANIFEST_FIELDS:
        raise ValueError("candidate manifest has unexpected fields")
    if manifest.get("schemaVersion") != SCHEMA_VERSION or manifest.get("candidateId") != candidate_id:
        raise ValueError("candidate manifest identity is invalid")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict):
        raise ValueError("candidate artifacts are invalid")
    for name in ("project", "research", "quality"):
        item = artifacts.get(name)
        if not isinstance(item, dict) or set(item) != {"file", "sha256"}:
            raise ValueError(f"candidate {name} artifact entry is invalid")
        path = directory / str(item["file"])
        if not path.is_file() or sha256_file(path) != item["sha256"]:
            raise ValueError(f"candidate {name} artifact fingerprint failed")
    core = {key: manifest[key] for key in ("mode", "projectId", "fullName", "githubId", "insertAfter", "artifacts")}
    if candidate_fingerprint(core) != manifest.get("candidateFingerprint"):
        raise ValueError("candidate fingerprint failed")
    return directory, manifest


def approve_candidate(
    project_root: Path,
    candidate_id: str,
    approved_by: str,
    *,
    write: bool = False,
    now: Callable[[], str] = utc_now,
) -> dict[str, object]:
    if not approved_by.strip():
        raise ValueError("approved-by must identify the human approver")
    directory, manifest = load_candidate(project_root, candidate_id)
    if manifest["status"] not in {"awaiting-approval", "approved"}:
        raise ValueError(f"candidate cannot be approved from status {manifest['status']}")
    approval = {
        "schemaVersion": SCHEMA_VERSION,
        "candidateId": candidate_id,
        "candidateFingerprint": manifest["candidateFingerprint"],
        "approvedAt": now(),
        "approvedBy": approved_by.strip(),
        "publicationAuthorized": True,
    }
    if write:
        write_json_atomic(directory / "approval.json", approval)
        manifest["status"] = "approved"
        manifest["publicationAuthorized"] = True
        write_json_atomic(directory / "manifest.json", manifest)
    return {"mode": "write" if write else "dry-run", **approval, "status": "approved" if write else "would-approve"}


def load_approval(directory: Path, manifest: dict[str, object]) -> dict[str, object]:
    approval = read_json(directory / "approval.json", "publication approval")
    if not isinstance(approval, dict) or set(approval) != APPROVAL_FIELDS:
        raise ValueError("publication approval has unexpected fields")
    if approval.get("schemaVersion") != SCHEMA_VERSION or approval.get("candidateId") != manifest.get("candidateId"):
        raise ValueError("publication approval identity is invalid")
    if approval.get("candidateFingerprint") != manifest.get("candidateFingerprint"):
        raise ValueError("publication approval is stale for this candidate")
    if approval.get("publicationAuthorized") is not True:
        raise ValueError("publication approval is not authorized")
    return approval


def apply_project_to_layers(
    project: dict[str, object],
    mode: str,
    insert_after: str | None,
    layers: tuple[list[str], dict[str, object], dict[str, object], dict[str, object]],
) -> tuple[list[str], dict[str, object], dict[str, object], dict[str, object]]:
    order, repositories, editorial, visuals = layers
    new_order = list(order)
    new_repositories = dict(repositories)
    new_editorial = dict(editorial)
    new_visuals = dict(visuals)
    project_id = str(project["id"])
    if mode == "add":
        new_order.insert(insertion_index(new_order, insert_after), project_id)
    new_repositories[project_id] = project["repository"]
    new_editorial[project_id] = project["editorial"]
    new_visuals[project_id] = project["visual"]
    expected = set(new_order)
    if len(new_order) != len(expected) or any(set(layer) != expected for layer in (new_repositories, new_editorial, new_visuals)):
        raise ValueError("candidate would create inconsistent published data layers")
    return new_order, new_repositories, new_editorial, new_visuals


def create_publication_backup(project_root: Path, transaction_id: str, candidate_id: str) -> Path:
    destination = project_root / TRANSACTION_ROOT / transaction_id
    destination.mkdir(parents=True, exist_ok=False)
    files = []
    for relative in DATA_PATHS:
        source = project_root / relative
        target = destination / "files" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        files.append({"path": relative, "sha256": sha256_file(source), "size": source.stat().st_size})
    write_json_atomic(destination / "manifest.json", {
        "schemaVersion": SCHEMA_VERSION,
        "transactionId": transaction_id,
        "candidateId": candidate_id,
        "createdAt": utc_now(),
        "status": "backup-created",
        "files": files,
    })
    return destination


def publication_transaction_directory(project_root: Path, transaction_id: str) -> Path:
    if not transaction_id or any(character not in "abcdefghijklmnopqrstuvwxyz0123456789-_" for character in transaction_id):
        raise ValueError("invalid publication transaction ID")
    directory = project_root.resolve() / TRANSACTION_ROOT / transaction_id
    if not directory.is_dir():
        raise ValueError(f"publication transaction does not exist: {transaction_id}")
    return directory


def incomplete_publication_transactions(project_root: Path) -> list[str]:
    root = project_root.resolve() / TRANSACTION_ROOT
    if not root.exists():
        return []
    incomplete = []
    for directory in root.iterdir():
        if not directory.is_dir():
            continue
        try:
            manifest = read_json(directory / "manifest.json", "publication transaction")
        except ValueError:
            incomplete.append(directory.name)
            continue
        if not isinstance(manifest, dict) or manifest.get("status") == "backup-created":
            incomplete.append(directory.name)
    return sorted(incomplete)


def restore_publication_backup(project_root: Path, backup: Path) -> None:
    manifest = read_json(backup / "manifest.json", "publication transaction")
    if not isinstance(manifest, dict) or not isinstance(manifest.get("files"), list):
        raise RuntimeError("publication backup manifest is invalid")
    for item in manifest["files"]:
        if not isinstance(item, dict) or item.get("path") not in DATA_PATHS:
            raise RuntimeError("publication backup contains an invalid path")
        relative = str(item["path"])
        source = backup / "files" / relative
        if not source.is_file() or sha256_file(source) != item.get("sha256"):
            raise RuntimeError(f"publication backup fingerprint failed: {relative}")
        temporary = project_root / f"{relative}.restore-{uuid.uuid4().hex[:8]}.tmp"
        temporary.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, temporary)
        os.replace(temporary, project_root / relative)
    for item in manifest["files"]:
        relative = str(item["path"])
        if sha256_file(project_root / relative) != item.get("sha256"):
            raise RuntimeError(f"publication rollback verification failed: {relative}")


def recover_publication(project_root: Path, transaction_id: str, *, write: bool = False, now: Callable[[], str] = utc_now) -> dict[str, object]:
    project_root = project_root.resolve()
    backup = publication_transaction_directory(project_root, transaction_id)
    manifest = read_json(backup / "manifest.json", "publication transaction")
    if not isinstance(manifest, dict) or not isinstance(manifest.get("files"), list):
        raise ValueError("publication transaction manifest is invalid")
    result = {
        "mode": "write" if write else "dry-run",
        "transactionId": transaction_id,
        "currentStatus": manifest.get("status"),
        "wouldRestore": [item.get("path") for item in manifest["files"] if isinstance(item, dict)],
        "publicationAuthorized": False,
    }
    if not write:
        return result
    restore_publication_backup(project_root, backup)
    manifest.update({"status": "manually-restored", "restoredAt": now()})
    write_json_atomic(backup / "manifest.json", manifest)
    return {**result, "status": "manually-restored", "verified": True}


def default_check_runner(project_root: Path) -> list[dict[str, object]]:
    npm = "npm.cmd" if os.name == "nt" else "npm"
    commands = (
        (npm, "run", "test:visual-identity"),
        (npm, "run", "test:identity-renderer"),
        (npm, "run", "lint"),
        (npm, "run", "build"),
    )
    results = []
    for command in commands:
        completed = subprocess.run(
            command,
            cwd=project_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        results.append({"command": " ".join(command), "exitCode": completed.returncode})
        if completed.returncode != 0:
            tail = "\n".join((completed.stdout + "\n" + completed.stderr).splitlines()[-30:])
            raise RuntimeError(f"publication check failed: {' '.join(command)}\n{tail}")
    return results


def publish_candidate(
    project_root: Path,
    candidate_id: str,
    *,
    write: bool = False,
    now: Callable[[], str] = utc_now,
    id_factory: Callable[[], str] | None = None,
    check_runner: Callable[[Path], list[dict[str, object]]] = default_check_runner,
) -> dict[str, object]:
    project_root = project_root.resolve()
    incomplete = incomplete_publication_transactions(project_root)
    if incomplete:
        raise ValueError("unfinished publication transaction requires recovery first: " + ", ".join(incomplete))
    directory, manifest = load_candidate(project_root, candidate_id)
    if manifest.get("status") != "approved" or manifest.get("publicationAuthorized") is not True:
        raise ValueError("candidate requires a current human approval before publication")
    approval = load_approval(directory, manifest)
    if data_fingerprint(project_root) != manifest.get("baselineDataFingerprint"):
        raise ValueError("published data changed after candidate preparation; prepare and approve a fresh candidate")
    dirty = dirty_data_paths(project_root)
    if dirty:
        raise ValueError("published data has uncommitted changes; publication stopped: " + " | ".join(dirty))
    project = read_json(directory / "project.json", "candidate project")
    if not isinstance(project, dict):
        raise ValueError("candidate project is invalid")
    layers = load_layers(project_root)
    validate_candidate_against_layers(project, str(manifest["mode"]), manifest.get("insertAfter"), layers)
    updated_layers = apply_project_to_layers(project, str(manifest["mode"]), manifest.get("insertAfter"), layers)
    plan = {
        "mode": "write" if write else "dry-run",
        "candidateId": candidate_id,
        "operation": manifest["mode"],
        "projectId": manifest["projectId"],
        "changedFiles": list(DATA_PATHS),
        "approvedBy": approval["approvedBy"],
        "publicationAuthorized": True,
    }
    if not write:
        return plan

    transaction_id = id_factory() if id_factory else f"publish-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    backup = create_publication_backup(project_root, transaction_id, candidate_id)
    try:
        for relative, value in zip(DATA_PATHS, updated_layers):
            write_json_atomic(project_root / relative, value)
        checks = check_runner(project_root)
        manifest["status"] = "published"
        write_json_atomic(directory / "manifest.json", manifest)
        transaction = read_json(backup / "manifest.json", "publication transaction")
        assert isinstance(transaction, dict)
        transaction.update({"status": "published", "publishedAt": now(), "checks": checks})
        write_json_atomic(backup / "manifest.json", transaction)
        return {**plan, "status": "published", "transactionId": transaction_id, "checks": checks, "rolledBack": False}
    except Exception as error:
        restore_publication_backup(project_root, backup)
        transaction = read_json(backup / "manifest.json", "publication transaction")
        assert isinstance(transaction, dict)
        transaction.update({"status": "rolled-back", "rolledBackAt": now(), "error": str(error)})
        write_json_atomic(backup / "manifest.json", transaction)
        raise RuntimeError(f"publication failed and data was restored: {error}") from error


def main() -> int:
    project_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare_parser = subparsers.add_parser("prepare", help="Validate and freeze a publication candidate")
    prepare_parser.add_argument("project")
    prepare_parser.add_argument("research")
    prepare_parser.add_argument("quality")
    prepare_parser.add_argument("--mode", choices=("add", "replace"), default="add")
    prepare_parser.add_argument("--after")
    prepare_parser.add_argument("--write", action="store_true")

    approve_parser = subparsers.add_parser("approve", help="Record explicit human publication approval")
    approve_parser.add_argument("candidate_id")
    approve_parser.add_argument("--approved-by", required=True)
    approve_parser.add_argument("--write", action="store_true")

    publish_parser = subparsers.add_parser("publish", help="Preview or execute an approved publication")
    publish_parser.add_argument("candidate_id")
    publish_parser.add_argument("--write", action="store_true")

    recover_parser = subparsers.add_parser("recover", help="Preview or restore a publication transaction backup")
    recover_parser.add_argument("transaction_id")
    recover_parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    try:
        if args.command == "prepare":
            result = prepare_candidate(
                project_root,
                (project_root / args.project),
                (project_root / args.research),
                (project_root / args.quality),
                mode=args.mode,
                insert_after=args.after,
                write=args.write,
            )
        elif args.command == "approve":
            result = approve_candidate(project_root, args.candidate_id, args.approved_by, write=args.write)
        elif args.command == "publish":
            result = publish_candidate(project_root, args.candidate_id, write=args.write)
        else:
            result = recover_publication(project_root, args.transaction_id, write=args.write)
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return 0
    except (OSError, ValueError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
