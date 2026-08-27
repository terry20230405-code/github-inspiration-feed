#!/usr/bin/env python3
"""Tests for phase-eight refresh snapshots and rollback."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from manage_versions import (
    FIXED_PATHS,
    compare_snapshot,
    create_snapshot,
    list_snapshots,
    load_snapshot,
    restore_snapshot,
)


def write_json(root: Path, relative: str, value: object) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def read_json(root: Path, relative: str) -> dict[str, object]:
    return json.loads((root / relative).read_text(encoding="utf-8"))


def seed_project(root: Path) -> None:
    repositories = {
        "alpha": {"stars": 10, "forks": 2, "fetchedAt": "old"},
        "beta": {"stars": 20, "forks": 4, "fetchedAt": "old"},
    }
    cache = {"schemaVersion": 1, "repositories": {"alpha": {"etag": "a"}, "beta": {"etag": "b"}}}
    state = {"schemaVersion": 1, "repositories": {"alpha": {"fingerprint": "a"}, "beta": {"fingerprint": "b"}}}
    write_json(root, "src/data/repositories.json", repositories)
    write_json(root, "outputs/refresh/github-cache.json", cache)
    write_json(root, "outputs/refresh/latest.json", {"schemaVersion": 1, "summary": {}, "repositories": []})
    write_json(root, "outputs/refresh/source-state.json", state)
    write_json(root, "outputs/refresh/source-cache.json", cache)
    write_json(root, "outputs/refresh/research-latest.json", {"schemaVersion": 1, "summary": {}, "repositories": []})
    write_json(root, "outputs/generated/research-refresh/alpha.source.json", {"projectId": "alpha", "value": "old"})
    write_json(root, "outputs/generated/research-refresh/beta.source.json", {"projectId": "beta", "value": "old"})


class VersionManagerTests(unittest.TestCase):
    def create(self, root: Path, snapshot_id: str = "snapshot-one") -> dict[str, object]:
        return create_snapshot(
            root,
            "test",
            now=lambda: "2026-08-27T00:00:00Z",
            id_factory=lambda: snapshot_id,
        )

    def test_snapshot_captures_every_managed_file_and_verifies_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            seed_project(root)
            manifest = self.create(root)
            _, loaded = load_snapshot(root, "snapshot-one")
        self.assertEqual(manifest, loaded)
        self.assertEqual(sum(entry["existed"] is True for entry in manifest["files"]), len(FIXED_PATHS) + 2)

    def test_checksum_tampering_invalidates_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            seed_project(root)
            self.create(root)
            stored = root / "outputs/versions/snapshots/snapshot-one/files/src/data/repositories.json"
            stored.write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "checksum failed"):
                load_snapshot(root, "snapshot-one")

    def test_diff_names_the_changed_json_field(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            seed_project(root)
            self.create(root)
            repositories = read_json(root, "src/data/repositories.json")
            repositories["alpha"]["stars"] = 99
            write_json(root, "src/data/repositories.json", repositories)
            result = compare_snapshot(root, "snapshot-one")
        repository_diff = next(item for item in result["files"] if item["path"] == "src/data/repositories.json")
        self.assertEqual(repository_diff["status"], "modified")
        self.assertIn("$.alpha.stars", [change["path"] for change in repository_diff["changes"]])

    def test_full_restore_restores_modified_files_and_removes_new_source_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            seed_project(root)
            self.create(root)
            repositories = read_json(root, "src/data/repositories.json")
            repositories["alpha"]["stars"] = 99
            write_json(root, "src/data/repositories.json", repositories)
            write_json(root, "outputs/generated/research-refresh/new.source.json", {"projectId": "new"})
            result = restore_snapshot(root, "snapshot-one")
            restored = read_json(root, "src/data/repositories.json")
            comparison = compare_snapshot(root, "snapshot-one")
        self.assertEqual(restored["alpha"]["stars"], 10)
        self.assertFalse((root / "outputs/generated/research-refresh/new.source.json").exists())
        self.assertEqual(comparison["changedFiles"], 0)
        self.assertTrue(result["verified"])
        self.assertIsNotNone(result["safetySnapshotId"])

    def test_project_restore_changes_only_selected_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            seed_project(root)
            self.create(root)
            repositories = read_json(root, "src/data/repositories.json")
            repositories["alpha"]["stars"] = 99
            repositories["beta"]["stars"] = 88
            write_json(root, "src/data/repositories.json", repositories)
            restore_snapshot(root, "snapshot-one", project_id="alpha")
            restored = read_json(root, "src/data/repositories.json")
            alpha_comparison = compare_snapshot(root, "snapshot-one", "alpha")
        self.assertEqual(restored["alpha"]["stars"], 10)
        self.assertEqual(restored["beta"]["stars"], 88)
        self.assertEqual(alpha_comparison["changedFiles"], 0)

    def test_invalid_manifest_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            seed_project(root)
            self.create(root)
            manifest_path = root / "outputs/versions/snapshots/snapshot-one/manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["files"][0]["path"] = "../outside.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unsafe snapshot path"):
                load_snapshot(root, "snapshot-one")

    def test_snapshot_listing_marks_valid_history(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            seed_project(root)
            self.create(root)
            result = list_snapshots(root)
        self.assertEqual(len(result["snapshots"]), 1)
        self.assertTrue(result["snapshots"][0]["valid"])


if __name__ == "__main__":
    unittest.main()
