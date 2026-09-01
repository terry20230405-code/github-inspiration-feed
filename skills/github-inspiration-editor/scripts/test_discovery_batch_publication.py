#!/usr/bin/env python3
"""Tests for all-or-nothing publication of a merged discovery batch."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

import generate_discovery_drafts as drafts
import publish_discovery_batch as batch
from test_discovery_drafts import evidence, generation_payload


class BatchPublicationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for relative in ("src/data", "outputs/generated/discovery-batches", "outputs/versions/publications"):
            (self.root / relative).mkdir(parents=True, exist_ok=True)
        for name in ("order.json", "repositories.json", "editorial.json", "visuals.json"):
            shutil.copy2(batch.PROJECT_ROOT / "src/data" / name, self.root / "src/data" / name)
        self.original_root = batch.PROJECT_ROOT
        self.original_batch_root = batch.BATCH_ROOT
        batch.PROJECT_ROOT = self.root
        batch.BATCH_ROOT = self.root / "outputs/generated/discovery-batches"

    def tearDown(self) -> None:
        batch.PROJECT_ROOT = self.original_root
        batch.BATCH_ROOT = self.original_batch_root
        self.temp.cleanup()

    def write_json(self, path: Path, value: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def create_valid_batch(self, batch_id: str) -> Path:
        directory = batch.BATCH_ROOT / batch_id
        directory.mkdir(parents=True)
        order = json.loads((self.root / "src/data/order.json").read_text(encoding="utf-8"))
        visuals = json.loads((self.root / "src/data/visuals.json").read_text(encoding="utf-8"))
        last_accent = visuals[order[-1]]["accent"]
        project = drafts.build_project(generation_payload(), evidence(), "visual-map", (last_accent,), "2026-08-30T00:00:00Z")
        research = drafts.research_markdown(generation_payload(), evidence(), "2026-08-30T00:00:00Z")
        project_path = directory / "visual-map.project.json"
        research_path = directory / "visual-map.research.md"
        quality_path = directory / "visual-map.quality.json"
        self.write_json(project_path, project)
        research_path.write_text(research, encoding="utf-8")
        quality = {
            "schemaVersion": 1,
            "projectId": "visual-map",
            "projectPath": project_path.relative_to(self.root).as_posix(),
            "researchPath": research_path.relative_to(self.root).as_posix(),
            "projectSha256": batch.sha256_file(project_path),
            "researchSha256": batch.sha256_file(research_path),
            "reviewedAt": "2026-08-30T00:00:00Z",
            "items": [{"id": item, "status": "pass", "evidence": f"{item} has concrete evidence in the frozen artifacts."} for item in drafts.CHECK_IDS],
            "blockers": [],
            "publicationCandidate": True,
            "publicationAuthorized": False,
        }
        self.write_json(quality_path, quality)
        artifacts = {
            "project": {"path": project_path.relative_to(self.root).as_posix(), "sha256": batch.sha256_file(project_path)},
            "research": {"path": research_path.relative_to(self.root).as_posix(), "sha256": batch.sha256_file(research_path)},
            "quality": {"path": quality_path.relative_to(self.root).as_posix(), "sha256": batch.sha256_file(quality_path)},
        }
        candidates = [{"projectId": "visual-map", "fullName": "example/visual-map", "githubId": 987654321, "artifacts": artifacts}]
        core = {"batchId": batch_id, "sourceDiscovery": "outputs/discovery/latest.json", "candidates": candidates}
        manifest = {
            "schemaVersion": 1,
            "batchId": batch_id,
            "createdAt": "2026-08-30T00:00:00Z",
            "status": "awaiting-approval",
            **core,
            "batchFingerprint": batch.sha256_value(core),
            "rejected": [],
            "publicationAuthorized": False,
        }
        self.write_json(directory / "manifest.json", manifest)
        return directory

    def test_invalid_batch_fingerprint_stops_before_data_write(self) -> None:
        batch_id = "20260830t000000z-deadbeef"
        directory = batch.BATCH_ROOT / batch_id
        directory.mkdir(parents=True)
        manifest = {
            "schemaVersion": 1,
            "batchId": batch_id,
            "createdAt": "2026-08-30T00:00:00Z",
            "status": "awaiting-approval",
            "sourceDiscovery": "outputs/discovery/latest.json",
            "candidates": [{"projectId": "fake", "fullName": "owner/fake", "githubId": 99, "artifacts": {}}],
            "batchFingerprint": "0" * 64,
            "rejected": [],
            "publicationAuthorized": False,
        }
        self.write_json(directory / "manifest.json", manifest)
        before = (self.root / "src/data/order.json").read_bytes()
        with self.assertRaises(batch.BatchPublicationError):
            batch.publish_batch(batch_id, "Terry", 12, write=True, run_checks=lambda _root: [])
        self.assertEqual((self.root / "src/data/order.json").read_bytes(), before)

    def test_approval_record_is_bound_to_batch_and_pull_request(self) -> None:
        approval = batch.approval_record("batch-1", "a" * 64, "Terry", 42, now="2026-08-30T00:00:00Z")
        self.assertEqual(set(approval), batch.APPROVAL_FIELDS)
        self.assertEqual(approval["sourcePullRequest"], 42)
        self.assertTrue(approval["publicationAuthorized"])

    def test_valid_merged_batch_updates_all_layers_once(self) -> None:
        batch_id = "20260830T000000Z-cafebabe"
        directory = self.create_valid_batch(batch_id)
        result = batch.publish_batch(batch_id, "Terry", 42, write=True, run_checks=lambda _root: [{"command": "tests", "exitCode": 0}], now="2026-08-30T00:01:00Z")
        order = json.loads((self.root / "src/data/order.json").read_text(encoding="utf-8"))
        self.assertEqual(order[-1], "visual-map")
        self.assertEqual(result["status"], "published")
        approval = json.loads((directory / "approval.json").read_text(encoding="utf-8"))
        self.assertEqual(approval["sourcePullRequest"], 42)

    def test_generated_uppercase_batch_id_is_accepted_but_path_escape_is_rejected(self) -> None:
        batch_id = "20260901T030804Z-80106c39"
        self.create_valid_batch(batch_id)
        plan = batch.publish_batch(batch_id, "Terry", 1, write=False)
        self.assertEqual(plan["batchId"], batch_id)
        with self.assertRaisesRegex(batch.BatchPublicationError, "invalid batch ID"):
            batch.publish_batch("../escape", "Terry", 1, write=False)

    def test_revoked_batch_cannot_be_published(self) -> None:
        batch_id = "20260901T030804Z-revoked1"
        directory = self.create_valid_batch(batch_id)
        manifest_path = directory / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["status"] = "revoked"
        self.write_json(manifest_path, manifest)
        with self.assertRaisesRegex(batch.BatchPublicationError, "cannot publish from status revoked"):
            batch.publish_batch(batch_id, "Terry", 1, write=False)

    def test_failed_batch_check_restores_every_feed_layer(self) -> None:
        batch_id = "20260830t000000z-badcheck"
        self.create_valid_batch(batch_id)
        before = {name: (self.root / "src/data" / name).read_bytes() for name in ("order.json", "repositories.json", "editorial.json", "visuals.json")}

        def fail_checks(_root: Path) -> list[dict[str, object]]:
            raise RuntimeError("simulated build failure")

        with self.assertRaises(batch.BatchPublicationError):
            batch.publish_batch(batch_id, "Terry", 43, write=True, run_checks=fail_checks, now="2026-08-30T00:01:00Z")
        after = {name: (self.root / "src/data" / name).read_bytes() for name in before}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
