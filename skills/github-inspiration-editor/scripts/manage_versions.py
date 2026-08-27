#!/usr/bin/env python3
"""Create, inspect, compare, and restore refresh-data snapshots."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Callable


SCHEMA_VERSION = 1
FIXED_PATHS = (
    "src/data/repositories.json",
    "outputs/refresh/github-cache.json",
    "outputs/refresh/latest.json",
    "outputs/refresh/source-state.json",
    "outputs/refresh/source-cache.json",
    "outputs/refresh/research-latest.json",
)
SOURCE_DIRECTORY = "outputs/generated/research-refresh"
SOURCE_PATTERN = "*.source.json"
PROJECT_KEYED_PATHS = {
    "src/data/repositories.json": None,
    "outputs/refresh/github-cache.json": "repositories",
    "outputs/refresh/source-state.json": "repositories",
    "outputs/refresh/source-cache.json": "repositories",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def default_snapshot_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{stamp}-{uuid.uuid4().hex[:8]}"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def read_json_object(path: Path, label: str) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"{label} could not be read: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def safe_relative_path(value: str) -> str:
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or ".." in path.parts or "\\" in value:
        raise ValueError(f"unsafe snapshot path: {value}")
    normalized = path.as_posix()
    if normalized in FIXED_PATHS:
        return normalized
    source_root = PurePosixPath(SOURCE_DIRECTORY)
    if path.parent == source_root and path.match(f"{SOURCE_DIRECTORY}/{SOURCE_PATTERN}"):
        return normalized
    raise ValueError(f"path is outside the managed refresh state: {value}")


def resolve_relative(project_root: Path, relative: str) -> Path:
    normalized = safe_relative_path(relative)
    resolved = (project_root / Path(normalized)).resolve()
    if not resolved.is_relative_to(project_root.resolve()):
        raise ValueError(f"path escapes project root: {relative}")
    return resolved


def snapshot_root(project_root: Path) -> Path:
    return project_root / "outputs/versions/snapshots"


def transaction_root(project_root: Path) -> Path:
    return project_root / "outputs/versions/transactions"


def source_members(project_root: Path) -> list[str]:
    directory = project_root / SOURCE_DIRECTORY
    if not directory.exists():
        return []
    return sorted(path.relative_to(project_root).as_posix() for path in directory.glob(SOURCE_PATTERN) if path.is_file())


def inventory_paths(project_root: Path) -> list[str]:
    return list(FIXED_PATHS) + source_members(project_root)


def create_snapshot(
    project_root: Path,
    reason: str,
    *,
    now: Callable[[], str] = utc_now,
    id_factory: Callable[[], str] = default_snapshot_id,
) -> dict[str, object]:
    project_root = project_root.resolve()
    snapshot_id = id_factory()
    if not snapshot_id or any(character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for character in snapshot_id):
        raise ValueError("snapshot ID contains unsupported characters")
    destination = snapshot_root(project_root) / snapshot_id
    if destination.exists():
        raise ValueError(f"snapshot already exists: {snapshot_id}")
    destination.mkdir(parents=True, exist_ok=False)
    entries: list[dict[str, object]] = []
    try:
        for relative in inventory_paths(project_root):
            current = resolve_relative(project_root, relative)
            existed = current.is_file()
            entry: dict[str, object] = {"path": relative, "existed": existed}
            if existed:
                stored = destination / "files" / Path(relative)
                stored.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(current, stored)
                entry.update({"size": current.stat().st_size, "sha256": sha256_file(current)})
            entries.append(entry)
        manifest: dict[str, object] = {
            "schemaVersion": SCHEMA_VERSION,
            "snapshotId": snapshot_id,
            "createdAt": now(),
            "reason": reason,
            "managedSourceDirectory": SOURCE_DIRECTORY,
            "managedSourcePattern": SOURCE_PATTERN,
            "files": entries,
        }
        # The manifest is written last and is the completion marker. This is
        # reliable on Windows, where replacing a populated directory can fail.
        write_json_atomic(destination / "manifest.json", manifest)
        return manifest
    except Exception:
        shutil.rmtree(destination, ignore_errors=True)
        raise


def load_snapshot(project_root: Path, snapshot_id: str) -> tuple[Path, dict[str, object]]:
    if not snapshot_id or any(character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for character in snapshot_id):
        raise ValueError("invalid snapshot ID")
    directory = snapshot_root(project_root.resolve()) / snapshot_id
    manifest = read_json_object(directory / "manifest.json", "snapshot manifest")
    if manifest.get("schemaVersion") != SCHEMA_VERSION or manifest.get("snapshotId") != snapshot_id:
        raise ValueError("snapshot manifest has an unsupported identity")
    entries = manifest.get("files")
    if not isinstance(entries, list):
        raise ValueError("snapshot manifest files must be an array")
    seen: set[str] = set()
    for raw_entry in entries:
        if not isinstance(raw_entry, dict) or not isinstance(raw_entry.get("path"), str):
            raise ValueError("snapshot manifest contains an invalid file entry")
        relative = safe_relative_path(raw_entry["path"])
        if relative in seen:
            raise ValueError(f"snapshot manifest repeats a path: {relative}")
        seen.add(relative)
        existed = raw_entry.get("existed")
        if not isinstance(existed, bool):
            raise ValueError(f"snapshot existed flag is invalid: {relative}")
        stored = directory / "files" / Path(relative)
        if existed:
            expected_hash = raw_entry.get("sha256")
            expected_size = raw_entry.get("size")
            if not isinstance(expected_hash, str) or not isinstance(expected_size, int) or not stored.is_file():
                raise ValueError(f"snapshot payload is incomplete: {relative}")
            if stored.stat().st_size != expected_size or sha256_file(stored) != expected_hash:
                raise ValueError(f"snapshot payload checksum failed: {relative}")
        elif stored.exists():
            raise ValueError(f"snapshot unexpectedly stores a missing file: {relative}")
    for required in FIXED_PATHS:
        if required not in seen:
            raise ValueError(f"snapshot is missing managed path: {required}")
    return directory, manifest


def snapshot_entries(manifest: dict[str, object]) -> dict[str, dict[str, object]]:
    return {str(entry["path"]): entry for entry in manifest["files"] if isinstance(entry, dict)}


def concise(value: object, limit: int = 180) -> object:
    if isinstance(value, (dict, list)):
        rendered = json.dumps(value, ensure_ascii=False, sort_keys=True)
        return rendered if len(rendered) <= limit else rendered[: limit - 3] + "..."
    if isinstance(value, str) and len(value) > limit:
        return value[: limit - 3] + "..."
    return value


def json_changes(before: object, after: object, path: str = "$", limit: int = 200) -> list[dict[str, object]]:
    changes: list[dict[str, object]] = []

    def walk(left: object, right: object, current_path: str) -> None:
        if len(changes) >= limit or left == right:
            return
        if isinstance(left, dict) and isinstance(right, dict):
            for key in sorted(set(left) | set(right)):
                child = f"{current_path}.{key}"
                if key not in left:
                    changes.append({"path": child, "before": None, "after": concise(right[key])})
                elif key not in right:
                    changes.append({"path": child, "before": concise(left[key]), "after": None})
                else:
                    walk(left[key], right[key], child)
            return
        if isinstance(left, list) and isinstance(right, list):
            for index in range(max(len(left), len(right))):
                child = f"{current_path}[{index}]"
                if index >= len(left):
                    changes.append({"path": child, "before": None, "after": concise(right[index])})
                elif index >= len(right):
                    changes.append({"path": child, "before": concise(left[index]), "after": None})
                else:
                    walk(left[index], right[index], child)
            return
        changes.append({"path": current_path, "before": concise(left), "after": concise(right)})

    walk(before, after, path)
    return changes


def compare_snapshot(project_root: Path, snapshot_id: str, project_id: str | None = None) -> dict[str, object]:
    directory, manifest = load_snapshot(project_root, snapshot_id)
    entries = snapshot_entries(manifest)
    paths = set(entries)
    paths.update(source_members(project_root))
    results: list[dict[str, object]] = []
    for relative in sorted(paths):
        if project_id and not path_applies_to_project(relative, project_id):
            continue
        entry = entries.get(relative)
        current = resolve_relative(project_root, relative)
        before_exists = bool(entry and entry.get("existed") is True)
        current_exists = current.is_file()
        selected_before: object | None = None
        selected_after: object | None = None
        if project_id and relative in PROJECT_KEYED_PATHS and before_exists and current_exists:
            try:
                before_json = json.loads((directory / "files" / Path(relative)).read_text(encoding="utf-8"))
                after_json = json.loads(current.read_text(encoding="utf-8"))
                selected_before = project_value(relative, before_json, project_id)
                selected_after = project_value(relative, after_json, project_id)
                status = "unchanged" if selected_before == selected_after else "modified"
            except (OSError, json.JSONDecodeError, ValueError):
                status = "modified"
        elif before_exists and current_exists:
            before_hash = str(entry["sha256"])
            after_hash = sha256_file(current)
            status = "unchanged" if before_hash == after_hash else "modified"
        elif before_exists:
            status = "missing"
        elif current_exists:
            status = "added"
        else:
            status = "unchanged"
        item: dict[str, object] = {"path": relative, "status": status}
        if status == "modified" and relative.endswith(".json"):
            try:
                if project_id and relative in PROJECT_KEYED_PATHS:
                    before_value = selected_before
                    after_value = selected_after
                else:
                    before_value = json.loads((directory / "files" / Path(relative)).read_text(encoding="utf-8"))
                    after_value = json.loads(current.read_text(encoding="utf-8"))
                if project_id and relative in PROJECT_KEYED_PATHS and selected_before is None and selected_after is None:
                    before_value = project_value(relative, before_value, project_id)
                    after_value = project_value(relative, after_value, project_id)
                item["changes"] = json_changes(before_value, after_value)
            except (OSError, json.JSONDecodeError, ValueError):
                item["changes"] = []
        if status != "unchanged":
            results.append(item)
    return {
        "schemaVersion": SCHEMA_VERSION,
        "snapshotId": snapshot_id,
        "comparedTo": "current",
        "projectId": project_id,
        "changedFiles": len(results),
        "files": results,
    }


def path_applies_to_project(relative: str, project_id: str) -> bool:
    return relative in PROJECT_KEYED_PATHS or relative == f"{SOURCE_DIRECTORY}/{project_id}.source.json"


def project_value(relative: str, value: object, project_id: str) -> object:
    if not isinstance(value, dict):
        raise ValueError(f"project-keyed JSON must be an object: {relative}")
    container_key = PROJECT_KEYED_PATHS.get(relative)
    container: object = value if container_key is None else value.get(container_key)
    if not isinstance(container, dict):
        raise ValueError(f"project container is invalid: {relative}")
    return container.get(project_id)


def write_project_value(relative: str, current: dict[str, object], snapshot_value: object, project_id: str) -> None:
    container_key = PROJECT_KEYED_PATHS[relative]
    container: object = current if container_key is None else current.get(container_key)
    if not isinstance(container, dict):
        raise ValueError(f"project container is invalid: {relative}")
    if snapshot_value is None:
        container.pop(project_id, None)
    else:
        container[project_id] = snapshot_value


def atomic_restore_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + f".restore-{uuid.uuid4().hex[:8]}.tmp")
    shutil.copy2(source, temporary)
    os.replace(temporary, destination)


def restore_snapshot(
    project_root: Path,
    snapshot_id: str,
    *,
    project_id: str | None = None,
    create_safety_snapshot: bool = True,
) -> dict[str, object]:
    project_root = project_root.resolve()
    directory, manifest = load_snapshot(project_root, snapshot_id)
    safety = None
    if create_safety_snapshot:
        safety = create_snapshot(project_root, f"before-restore:{snapshot_id}")
    entries = snapshot_entries(manifest)

    if project_id:
        for relative in PROJECT_KEYED_PATHS:
            entry = entries[relative]
            stored = directory / "files" / Path(relative)
            target = resolve_relative(project_root, relative)
            if entry.get("existed") is not True or not target.is_file():
                raise ValueError(f"cannot perform project restore without both JSON files: {relative}")
            snapshot_json = read_json_object(stored, f"snapshot {relative}")
            current_json = read_json_object(target, f"current {relative}")
            write_project_value(relative, current_json, project_value(relative, snapshot_json, project_id), project_id)
            write_json_atomic(target, current_json)
        source_relative = f"{SOURCE_DIRECTORY}/{project_id}.source.json"
        source_entry = entries.get(source_relative)
        source_target = resolve_relative(project_root, source_relative)
        if source_entry and source_entry.get("existed") is True:
            atomic_restore_file(directory / "files" / Path(source_relative), source_target)
        elif source_target.exists():
            source_target.unlink()
    else:
        for relative in FIXED_PATHS:
            entry = entries[relative]
            target = resolve_relative(project_root, relative)
            if entry.get("existed") is True:
                atomic_restore_file(directory / "files" / Path(relative), target)
            elif target.exists():
                target.unlink()
        expected_sources = {
            relative for relative, entry in entries.items() if relative.startswith(SOURCE_DIRECTORY + "/") and entry.get("existed") is True
        }
        for relative in source_members(project_root):
            if relative not in expected_sources:
                resolve_relative(project_root, relative).unlink()
        for relative in expected_sources:
            atomic_restore_file(directory / "files" / Path(relative), resolve_relative(project_root, relative))

    remaining = compare_snapshot(project_root, snapshot_id, project_id)
    if remaining["changedFiles"]:
        raise RuntimeError("restore verification failed; current state does not match the snapshot")
    return {
        "schemaVersion": SCHEMA_VERSION,
        "restoredAt": utc_now(),
        "snapshotId": snapshot_id,
        "projectId": project_id,
        "safetySnapshotId": safety["snapshotId"] if safety else None,
        "verified": True,
        "publicationAuthorized": False,
    }


def list_snapshots(project_root: Path) -> dict[str, object]:
    snapshots: list[dict[str, object]] = []
    root = snapshot_root(project_root)
    if root.exists():
        for directory in sorted((path for path in root.iterdir() if path.is_dir() and not path.name.startswith(".")), reverse=True):
            try:
                _, manifest = load_snapshot(project_root, directory.name)
            except ValueError as error:
                snapshots.append({"snapshotId": directory.name, "valid": False, "error": str(error)})
                continue
            snapshots.append(
                {
                    "snapshotId": manifest["snapshotId"],
                    "createdAt": manifest["createdAt"],
                    "reason": manifest["reason"],
                    "fileCount": sum(entry.get("existed") is True for entry in manifest["files"]),
                    "valid": True,
                }
            )
    return {"schemaVersion": SCHEMA_VERSION, "snapshots": snapshots}


def write_transaction(project_root: Path, value: dict[str, object]) -> Path:
    transaction_id = value.get("transactionId")
    if not isinstance(transaction_id, str) or not transaction_id:
        raise ValueError("transaction record requires transactionId")
    path = transaction_root(project_root) / f"{transaction_id}.json"
    write_json_atomic(path, value)
    return path


def main() -> int:
    project_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="Create an immutable refresh-state snapshot")
    create_parser.add_argument("--reason", default="manual")

    subparsers.add_parser("list", help="List and verify available snapshots")

    show_parser = subparsers.add_parser("show", help="Show one verified snapshot manifest")
    show_parser.add_argument("snapshot_id")

    diff_parser = subparsers.add_parser("diff", help="Compare one snapshot with current refresh state")
    diff_parser.add_argument("snapshot_id")
    diff_parser.add_argument("--project")

    restore_parser = subparsers.add_parser("restore", help="Preview or execute a verified rollback")
    restore_parser.add_argument("snapshot_id")
    restore_parser.add_argument("--project")
    restore_parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    try:
        if args.command == "create":
            result = create_snapshot(project_root, args.reason)
        elif args.command == "list":
            result = list_snapshots(project_root)
        elif args.command == "show":
            _, result = load_snapshot(project_root, args.snapshot_id)
        elif args.command == "diff":
            result = compare_snapshot(project_root, args.snapshot_id, args.project)
        else:
            comparison = compare_snapshot(project_root, args.snapshot_id, args.project)
            if args.write:
                result = restore_snapshot(project_root, args.snapshot_id, project_id=args.project)
                transaction_id = f"restore-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
                write_transaction(project_root, {**result, "transactionId": transaction_id, "status": "restored"})
            else:
                result = {
                    "schemaVersion": SCHEMA_VERSION,
                    "mode": "dry-run",
                    "snapshotId": args.snapshot_id,
                    "projectId": args.project,
                    "wouldChangeFiles": comparison["changedFiles"],
                    "files": comparison["files"],
                    "nextAction": "Add --write to restore after reviewing this plan.",
                    "publicationAuthorized": False,
                }
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return 0
    except (OSError, ValueError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
