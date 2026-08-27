#!/usr/bin/env python3
"""Tests for safe repository metadata refreshes."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from refresh_repositories import FetchResult, build_candidate, compare_snapshots, refresh_dataset, reliable_license, write_json_atomic


CURRENT = {
    "githubId": 123,
    "fullName": "owner/repository",
    "name": "Repository",
    "stars": 100,
    "forks": 10,
    "language": "TypeScript",
    "pushedAt": "2026-08-26T10:00:00Z",
    "license": "Custom License",
    "state": "active",
    "fetchedAt": "2026-08-26T11:00:00Z",
}


def payload(**overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "id": 123,
        "full_name": "owner/repository",
        "name": "Repository",
        "stargazers_count": 120,
        "forks_count": 12,
        "language": "TypeScript",
        "pushed_at": "2026-08-27T10:00:00Z",
        "license": {"spdx_id": "NOASSERTION", "name": "Other"},
        "archived": False,
        "disabled": False,
        "private": False,
        "fork": False,
    }
    value.update(overrides)
    return value


class RepositoryRefreshTests(unittest.TestCase):
    def test_custom_license_is_preserved_when_api_only_says_other(self) -> None:
        self.assertEqual(reliable_license(payload(), "Custom License"), "Custom License")

    def test_standard_license_uses_spdx_identifier(self) -> None:
        self.assertEqual(reliable_license(payload(license={"spdx_id": "MIT", "name": "MIT License"}), "未知"), "MIT")

    def test_activity_and_statistics_are_classified_separately(self) -> None:
        candidate = build_candidate(CURRENT, payload(), "2026-08-27T11:00:00Z")
        changes = compare_snapshots(CURRENT, candidate)
        levels = {change["field"]: change["level"] for change in changes}
        self.assertEqual(levels["stars"], "statistics")
        self.assertEqual(levels["forks"], "statistics")
        self.assertEqual(levels["pushedAt"], "activity")

    def test_api_slug_casing_does_not_replace_product_display_name(self) -> None:
        candidate = build_candidate(CURRENT, payload(name="repository"), "2026-08-27T11:00:00Z")
        self.assertEqual(candidate["name"], "Repository")

    def test_critical_identity_change_is_not_written(self) -> None:
        dataset = {"sample": copy.deepcopy(CURRENT)}
        response = FetchResult(200, payload(full_name="new-owner/repository"), '"etag"', "59")
        updated, cache, results = refresh_dataset(dataset, {"schemaVersion": 1, "repositories": {}}, ["sample"], lambda _name, _etag: response, "2026-08-27T11:00:00Z")
        self.assertEqual(updated, dataset)
        self.assertEqual(cache["repositories"], {})
        self.assertEqual(results[0]["status"], "review-required")

    def test_license_change_requires_review_and_preserves_snapshot(self) -> None:
        dataset = {"sample": copy.deepcopy(CURRENT)}
        response = FetchResult(200, payload(license={"spdx_id": "MIT", "name": "MIT License"}), '"etag"', "59")
        updated, _, results = refresh_dataset(dataset, {"schemaVersion": 1, "repositories": {}}, ["sample"], lambda _name, _etag: response, "2026-08-27T11:00:00Z")
        self.assertEqual(updated, dataset)
        self.assertEqual(results[0]["changeLevel"], "critical")
        self.assertIn("license changed", results[0]["reviewReasons"])

    def test_archived_repository_requires_review(self) -> None:
        dataset = {"sample": copy.deepcopy(CURRENT)}
        response = FetchResult(200, payload(archived=True), '"etag"', "59")
        updated, _, results = refresh_dataset(dataset, {"schemaVersion": 1, "repositories": {}}, ["sample"], lambda _name, _etag: response, "2026-08-27T11:00:00Z")
        self.assertEqual(updated, dataset)
        self.assertEqual(results[0]["status"], "review-required")

    def test_cached_etag_is_sent_to_fetcher(self) -> None:
        dataset = {"sample": copy.deepcopy(CURRENT)}
        seen: list[str | None] = []

        def fetcher(_name: str, etag: str | None) -> FetchResult:
            seen.append(etag)
            return FetchResult(304, None, etag, "60")

        cache = {"schemaVersion": 1, "repositories": {"123": {"fullName": "owner/repository", "etag": '"cached"', "lastCheckedAt": "2026-08-26T11:00:00Z"}}}
        refresh_dataset(dataset, cache, ["sample"], fetcher, "2026-08-27T11:00:00Z")
        self.assertEqual(seen, ['"cached"'])

    def test_safe_refresh_changes_only_repository_file(self) -> None:
        dataset = {"sample": copy.deepcopy(CURRENT)}
        response = FetchResult(200, payload(), '"etag"', "59")
        updated, _, results = refresh_dataset(dataset, {"schemaVersion": 1, "repositories": {}}, ["sample"], lambda _name, _etag: response, "2026-08-27T11:00:00Z")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repository_path = root / "repositories.json"
            editorial_path = root / "editorial.ts"
            visual_path = root / "visuals.ts"
            editorial_path.write_text("editorial sentinel", encoding="utf-8")
            visual_path.write_text("visual sentinel", encoding="utf-8")
            write_json_atomic(repository_path, updated)
            self.assertEqual(json.loads(repository_path.read_text(encoding="utf-8"))["sample"]["stars"], 120)
            self.assertEqual(editorial_path.read_text(encoding="utf-8"), "editorial sentinel")
            self.assertEqual(visual_path.read_text(encoding="utf-8"), "visual sentinel")
        self.assertEqual(results[0]["status"], "updated")
        self.assertTrue(results[0]["researchRefreshRecommended"])
        self.assertFalse(results[0]["contentReviewRecommended"])

    def test_not_modified_refreshes_only_fetched_at(self) -> None:
        dataset = {"sample": copy.deepcopy(CURRENT)}
        response = FetchResult(304, None, '"etag"', "60")
        updated, _, results = refresh_dataset(dataset, {"schemaVersion": 1, "repositories": {}}, ["sample"], lambda _name, _etag: response, "2026-08-27T11:00:00Z")
        expected = copy.deepcopy(CURRENT)
        expected["fetchedAt"] = "2026-08-27T11:00:00Z"
        self.assertEqual(updated["sample"], expected)
        self.assertEqual(results[0]["changeLevel"], "freshness")

    def test_rate_limit_stops_the_remaining_queue(self) -> None:
        dataset = {"first": copy.deepcopy(CURRENT), "second": {**copy.deepcopy(CURRENT), "githubId": 456, "fullName": "owner/second"}}
        calls: list[str] = []

        def fetcher(full_name: str, _etag: str | None) -> FetchResult:
            calls.append(full_name)
            return FetchResult(403, None, None, "0", "rate limit reached")

        _, _, results = refresh_dataset(dataset, {"schemaVersion": 1, "repositories": {}}, ["first", "second"], fetcher, "2026-08-27T11:00:00Z")
        self.assertEqual(calls, ["owner/repository"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["status"], "failed")


if __name__ == "__main__":
    unittest.main()
