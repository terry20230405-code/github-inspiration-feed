#!/usr/bin/env python3
"""Tests for stage-seven research source refreshes and semantic review gating."""

from __future__ import annotations

import base64
import copy
import json
import tempfile
import unittest
from pathlib import Path

from refresh_repositories import write_json_atomic
from refresh_research_sources import (
    SourceFetchResult,
    refresh_sources,
    selected_from_stage_six,
    validate_review,
)


REPOSITORY = {
    "githubId": 123,
    "fullName": "owner/repository",
    "name": "Repository",
    "stars": 100,
    "forks": 10,
    "language": "TypeScript",
    "pushedAt": "2026-08-27T10:00:00Z",
    "license": "MIT",
    "state": "active",
    "fetchedAt": "2026-08-27T11:00:00Z",
}
EMPTY_CONTAINER = {"schemaVersion": 1, "repositories": {}}


def metadata_payload(**overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "id": 123,
        "full_name": "owner/repository",
        "default_branch": "main",
        "description": "A useful product",
        "homepage": "https://example.com",
        "topics": ["automation", "typescript"],
        "private": False,
        "fork": False,
        "archived": False,
        "disabled": False,
    }
    value.update(overrides)
    return value


def readme_payload(sha: str = "readme-sha", content: str = "# Repository\n\nCurrent product capabilities.") -> dict[str, object]:
    return {
        "sha": sha,
        "path": "README.md",
        "html_url": "https://github.com/owner/repository/blob/main/README.md",
        "encoding": "base64",
        "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
    }


def release_payload(release_id: int = 9, body: str = "New product capability") -> dict[str, object]:
    return {
        "id": release_id,
        "tag_name": f"v{release_id}.0.0",
        "name": f"Version {release_id}",
        "published_at": "2026-08-27T09:00:00Z",
        "html_url": f"https://github.com/owner/repository/releases/tag/v{release_id}.0.0",
        "body": body,
    }


def fetched(payload: dict[str, object], etag: str = '"etag"') -> SourceFetchResult:
    return SourceFetchResult(200, payload, etag, "50")


def baseline_fetcher(_name: str, signal: str, _etag: str | None) -> SourceFetchResult:
    responses = {
        "metadata": fetched(metadata_payload(), '"metadata"'),
        "readme": fetched(readme_payload(), '"readme"'),
        "release": fetched(release_payload(), '"release"'),
    }
    return responses[signal]


class ResearchRefreshTests(unittest.TestCase):
    def test_initial_baseline_creates_pending_evidence_without_touching_editorial(self) -> None:
        dataset = {"sample": copy.deepcopy(REPOSITORY)}
        state, cache, results, bundles = refresh_sources(dataset, copy.deepcopy(EMPTY_CONTAINER), copy.deepcopy(EMPTY_CONTAINER), ["sample"], baseline_fetcher, "2026-08-27T12:00:00Z")
        self.assertEqual(results[0]["observation"], "baseline")
        self.assertEqual(results[0]["semanticReviewStatus"], "pending")
        self.assertIn("sample", bundles)
        self.assertFalse(bundles["sample"]["safety"]["publicationAuthorized"])
        self.assertEqual(state["repositories"]["sample"]["readme"]["sha"], "readme-sha")
        self.assertIn("metadata", cache["repositories"]["123"])

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            editorial = root / "editorial.ts"
            visual = root / "visuals.ts"
            editorial.write_text("editorial sentinel", encoding="utf-8")
            visual.write_text("visual sentinel", encoding="utf-8")
            write_json_atomic(root / "source-state.json", state)
            write_json_atomic(root / "sample.source.json", bundles["sample"])
            self.assertEqual(editorial.read_text(encoding="utf-8"), "editorial sentinel")
            self.assertEqual(visual.read_text(encoding="utf-8"), "visual sentinel")

    def test_matching_keep_review_completes_unchanged_source_check(self) -> None:
        dataset = {"sample": copy.deepcopy(REPOSITORY)}
        state, cache, first_results, _ = refresh_sources(dataset, copy.deepcopy(EMPTY_CONTAINER), copy.deepcopy(EMPTY_CONTAINER), ["sample"], baseline_fetcher, "2026-08-27T12:00:00Z")
        fingerprint = first_results[0]["sourceFingerprint"]
        review = {
            "schemaVersion": 1,
            "projectId": "sample",
            "sourceFingerprint": fingerprint,
            "reviewedAt": "2026-08-27T12:30:00Z",
            "impact": "none",
            "summary": "当前来源没有推翻已发布内容。",
            "affectedFields": [],
            "evidence": [{"sourceId": "S2", "finding": "README 与现有产品说明一致。"}],
            "recommendedAction": "keep-published",
            "publicationAuthorized": False,
        }
        seen_etags: list[str | None] = []

        def not_modified(_name: str, _signal: str, etag: str | None) -> SourceFetchResult:
            seen_etags.append(etag)
            return SourceFetchResult(304, None, etag, "49")

        _, _, results, bundles = refresh_sources(dataset, state, cache, ["sample"], not_modified, "2026-08-27T13:00:00Z", {"sample": review})
        self.assertEqual(results[0]["observation"], "unchanged")
        self.assertEqual(results[0]["semanticReviewStatus"], "complete")
        self.assertEqual(bundles, {})
        self.assertEqual(seen_etags, ['"metadata"', '"readme"', '"release"'])

    def test_readme_change_invalidates_old_review_and_creates_new_bundle(self) -> None:
        dataset = {"sample": copy.deepcopy(REPOSITORY)}
        state, cache, first_results, _ = refresh_sources(dataset, copy.deepcopy(EMPTY_CONTAINER), copy.deepcopy(EMPTY_CONTAINER), ["sample"], baseline_fetcher, "2026-08-27T12:00:00Z")
        old_review = {
            "schemaVersion": 1,
            "projectId": "sample",
            "sourceFingerprint": first_results[0]["sourceFingerprint"],
            "reviewedAt": "2026-08-27T12:30:00Z",
            "impact": "none",
            "summary": "旧来源已检查。",
            "affectedFields": [],
            "evidence": [{"sourceId": "S2", "finding": "旧 README 已检查。"}],
            "recommendedAction": "keep-published",
            "publicationAuthorized": False,
        }

        def changed_readme(_name: str, signal: str, etag: str | None) -> SourceFetchResult:
            if signal == "readme":
                return fetched(readme_payload("new-sha", "# Repository\n\nA genuinely new capability."), '"new-readme"')
            return SourceFetchResult(304, None, etag, "48")

        _, _, results, bundles = refresh_sources(dataset, state, cache, ["sample"], changed_readme, "2026-08-27T14:00:00Z", {"sample": old_review})
        self.assertEqual(results[0]["observation"], "source-changed")
        self.assertEqual(results[0]["semanticReviewStatus"], "pending")
        self.assertTrue(any(change["field"] == "readme.sha" for change in results[0]["changes"]))
        self.assertIn("sample", bundles)

    def test_topics_change_is_a_source_metadata_signal(self) -> None:
        dataset = {"sample": copy.deepcopy(REPOSITORY)}
        state, cache, _, _ = refresh_sources(dataset, copy.deepcopy(EMPTY_CONTAINER), copy.deepcopy(EMPTY_CONTAINER), ["sample"], baseline_fetcher, "2026-08-27T12:00:00Z")

        def changed_topics(_name: str, signal: str, etag: str | None) -> SourceFetchResult:
            if signal == "metadata":
                return fetched(metadata_payload(topics=["automation", "typescript", "ai"]), '"new-metadata"')
            return SourceFetchResult(304, None, etag, "47")

        _, _, results, _ = refresh_sources(dataset, state, cache, ["sample"], changed_topics, "2026-08-27T15:00:00Z")
        change = next(change for change in results[0]["changes"] if change["field"] == "topics")
        self.assertEqual(change["level"], "source-metadata")

    def test_missing_release_is_a_valid_state(self) -> None:
        dataset = {"sample": copy.deepcopy(REPOSITORY)}

        def no_release(name: str, signal: str, etag: str | None) -> SourceFetchResult:
            if signal == "release":
                return SourceFetchResult(404, None, None, "46", "No published release was found")
            return baseline_fetcher(name, signal, etag)

        state, _, results, bundles = refresh_sources(dataset, copy.deepcopy(EMPTY_CONTAINER), copy.deepcopy(EMPTY_CONTAINER), ["sample"], no_release, "2026-08-27T12:00:00Z")
        self.assertIsNone(state["repositories"]["sample"]["latestRelease"])
        self.assertEqual(results[0]["status"], "updated")
        release_source = next(source for source in bundles["sample"]["sources"] if source["kind"] == "release")
        self.assertEqual(release_source["retrievalStatus"], "missing")

    def test_identity_change_requires_review_and_preserves_state(self) -> None:
        dataset = {"sample": copy.deepcopy(REPOSITORY)}

        def changed_identity(_name: str, signal: str, _etag: str | None) -> SourceFetchResult:
            if signal == "metadata":
                return fetched(metadata_payload(id=456))
            raise AssertionError("later signals must not be fetched")

        state, cache, results, bundles = refresh_sources(dataset, copy.deepcopy(EMPTY_CONTAINER), copy.deepcopy(EMPTY_CONTAINER), ["sample"], changed_identity, "2026-08-27T12:00:00Z")
        self.assertEqual(results[0]["status"], "review-required")
        self.assertEqual(state, EMPTY_CONTAINER)
        self.assertEqual(cache, EMPTY_CONTAINER)
        self.assertEqual(bundles, {})

    def test_rate_limit_stops_remaining_projects(self) -> None:
        second = {**copy.deepcopy(REPOSITORY), "githubId": 456, "fullName": "owner/second"}
        calls: list[str] = []

        def limited(full_name: str, _signal: str, _etag: str | None) -> SourceFetchResult:
            calls.append(full_name)
            return SourceFetchResult(403, None, None, "0", "rate limit reached")

        _, _, results, _ = refresh_sources({"first": copy.deepcopy(REPOSITORY), "second": second}, copy.deepcopy(EMPTY_CONTAINER), copy.deepcopy(EMPTY_CONTAINER), ["first", "second"], limited, "2026-08-27T12:00:00Z")
        self.assertEqual(calls, ["owner/repository"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["status"], "failed")

    def test_review_contract_enforces_action_and_no_publication(self) -> None:
        review = {
            "schemaVersion": 1,
            "projectId": "sample",
            "sourceFingerprint": "abc",
            "reviewedAt": "2026-08-27T12:30:00Z",
            "impact": "meaningful",
            "summary": "来源显示产品能力发生了实质变化。",
            "affectedFields": ["editorial.summary"],
            "evidence": [{"sourceId": "S2", "finding": "README 新增了一项正式能力。"}],
            "recommendedAction": "keep-published",
            "publicationAuthorized": True,
        }
        errors = validate_review(review, "sample", "abc")
        self.assertIn("meaningful impact requires draft", errors)
        self.assertIn("publicationAuthorized must be false", errors)

    def test_stage_six_queue_selects_only_research_recommendations(self) -> None:
        report = {
            "schemaVersion": 1,
            "summary": {"failed": 0, "reviewRequired": 0},
            "repositories": [
                {"id": "first", "researchRefreshRecommended": True, "contentReviewRecommended": False},
                {"id": "second", "researchRefreshRecommended": False, "contentReviewRecommended": False},
            ],
        }
        self.assertEqual(selected_from_stage_six(report, {"first": {}, "second": {}}), ["first"])

    def test_stage_six_failures_block_source_refresh(self) -> None:
        report = {"schemaVersion": 1, "summary": {"failed": 1, "reviewRequired": 0}, "repositories": []}
        with self.assertRaises(ValueError):
            selected_from_stage_six(report, {"first": {}})

    def test_fixed_benchmark_repositories_use_the_same_source_change_gate(self) -> None:
        benchmarks = (
            ("remotion", 1, "remotion-dev/remotion"),
            ("excalidraw", 2, "excalidraw/excalidraw"),
            ("immich", 3, "immich-app/immich"),
            ("n8n", 4, "n8n-io/n8n"),
            ("memos", 5, "usememos/memos"),
        )
        for project_id, github_id, full_name in benchmarks:
            repository = {**copy.deepcopy(REPOSITORY), "githubId": github_id, "fullName": full_name}

            def initial(_name: str, signal: str, _etag: str | None) -> SourceFetchResult:
                if signal == "metadata":
                    return fetched(metadata_payload(id=github_id, full_name=full_name))
                if signal == "readme":
                    return fetched(readme_payload())
                return fetched(release_payload())

            state, cache, _, _ = refresh_sources({project_id: repository}, copy.deepcopy(EMPTY_CONTAINER), copy.deepcopy(EMPTY_CONTAINER), [project_id], initial, "2026-08-27T12:00:00Z")

            def changed(_name: str, signal: str, etag: str | None) -> SourceFetchResult:
                if signal == "readme":
                    return fetched(readme_payload("changed-sha", "# Repository\n\nChanged product evidence."))
                return SourceFetchResult(304, None, etag, "45")

            _, _, results, bundles = refresh_sources({project_id: repository}, state, cache, [project_id], changed, "2026-08-27T13:00:00Z")
            self.assertEqual(results[0]["semanticReviewStatus"], "pending")
            self.assertIn(project_id, bundles)


if __name__ == "__main__":
    unittest.main()
