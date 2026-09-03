#!/usr/bin/env python3
"""Offline tests for deterministic repository discovery."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from discover_repositories import DiscoveryError, apply_environment_overrides, discover, generated_repositories, validate_config


NOW = datetime(2026, 8, 30, 0, 0, tzinfo=timezone.utc)


def repository(repo_id: int, full_name: str, *, stars: int, topic: str, license_id: str | None = "MIT", archived: bool = False) -> dict[str, object]:
    return {
        "id": repo_id,
        "full_name": full_name,
        "name": full_name.split("/")[1],
        "private": False,
        "visibility": "public",
        "fork": False,
        "archived": archived,
        "disabled": False,
        "mirror_url": None,
        "is_template": False,
        "stargazers_count": stars,
        "forks_count": max(1, stars // 20),
        "language": "TypeScript",
        "pushed_at": "2026-08-20T00:00:00Z",
        "created_at": "2026-04-01T00:00:00Z",
        "description": "A complete product with a clear workflow and visible outcome.",
        "topics": [topic],
        "license": {"spdx_id": license_id, "name": license_id} if license_id else None,
        "default_branch": "main",
        "open_issues_count": 4,
        "html_url": f"https://github.com/{full_name}",
    }


class DiscoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "src/data").mkdir(parents=True)
        (self.root / "src/data/repositories.json").write_text(json.dumps({
            "existing": {"githubId": 1, "fullName": "owner/existing"},
        }), encoding="utf-8")
        self.config = validate_config({
            "schemaVersion": 2,
            "maxSearchResultsPerQuery": 20,
            "shortlistSize": 5,
            "aiAnalysisLimit": 4,
            "maxCandidatesPerRun": 3,
            "maxConcurrentCandidates": 2,
            "activeWithinDays": 365,
            "minimumStars": 30,
            "minimumReadmeCharacters": 800,
            "aiProvider": {
                "protocol": "openai-chat-completions",
                "baseUrl": "https://4router.net/v1",
                "model": "gpt-5.4",
                "reasoningEffort": "medium",
                "maxCompletionTokens": 16000,
            },
            "searchLanes": [
                {"id": "ai", "label": "AI", "familyHint": "ai", "query": "topic:ai"},
                {"id": "design", "label": "设计", "familyHint": "design", "query": "topic:design"},
            ],
            "excludedTopics": ["malware"],
            "excludedNameFragments": ["awesome-"],
        })

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_optional_streaming_setting_is_strictly_boolean(self) -> None:
        for enabled in (True, False):
            config = deepcopy(self.config)
            config["aiProvider"]["stream"] = enabled
            self.assertIs(validate_config(config)["aiProvider"]["stream"], enabled)
        self.assertNotIn("stream", validate_config(deepcopy(self.config))["aiProvider"])
        for invalid in ("true", 1, None):
            config = deepcopy(self.config)
            config["aiProvider"]["stream"] = invalid
            with self.assertRaises(DiscoveryError):
                validate_config(config)

    def test_stream_environment_override_does_not_mutate_config(self) -> None:
        for raw, expected in (("true", True), ("false", False)):
            with patch.dict(os.environ, {"AI_STREAM": raw}, clear=True):
                updated = apply_environment_overrides(self.config)
                self.assertIs(updated["aiProvider"]["stream"], expected)
                self.assertNotIn("stream", self.config["aiProvider"])
        with patch.dict(os.environ, {"AI_STREAM": "yes"}, clear=True):
            with self.assertRaisesRegex(DiscoveryError, "AI_STREAM"):
                apply_environment_overrides(self.config)

    def test_filters_known_archived_and_missing_license(self) -> None:
        items = [
            repository(1, "owner/existing", stars=1000, topic="ai"),
            repository(2, "owner/archived", stars=1000, topic="ai", archived=True),
            repository(3, "owner/no-license", stars=1000, topic="ai", license_id=None),
            repository(4, "owner/good-ai", stars=800, topic="ai"),
            repository(5, "owner/good-design", stars=600, topic="design"),
        ]

        def request(_url: str, _token: str | None) -> object:
            return {"items": items}

        result = discover(self.config, request, None, now=NOW, project_root=self.root)
        names = [candidate["fullName"] for candidate in result["aiQueue"]]
        self.assertEqual(names, ["owner/good-ai", "owner/good-design"])
        self.assertGreaterEqual(result["excluded"]["already-known"], 1)
        self.assertGreaterEqual(result["excluded"]["archived"], 1)
        self.assertGreaterEqual(result["excluded"]["missing-license"], 1)

    def test_rejects_unsafe_or_complete_ai_endpoint_urls(self) -> None:
        for base_url in (
            "http://4router.net/v1",
            "https://user:password@4router.net/v1",
            "https://4router.net/v1?key=secret",
            "https://4router.net/v1/chat/completions",
        ):
            config = deepcopy(self.config)
            config["aiProvider"]["baseUrl"] = base_url
            with self.subTest(base_url=base_url), self.assertRaisesRegex(DiscoveryError, "aiProvider.baseUrl"):
                validate_config(config)

    def test_round_robin_keeps_search_lanes_diverse(self) -> None:
        ai_items = [repository(10 + index, f"owner/ai-{index}", stars=1000 - index, topic="ai") for index in range(4)]
        design_items = [repository(30, "owner/design-0", stars=200, topic="design")]

        def request(url: str, _token: str | None) -> object:
            return {"items": design_items if "topic%3Adesign" in url else ai_items}

        result = discover(self.config, request, None, now=NOW, project_root=self.root)
        first_two = [candidate["matchedLanes"][0]["id"] for candidate in result["aiQueue"][:2]]
        self.assertEqual(set(first_two), {"ai", "design"})

    def test_revoked_batch_does_not_permanently_exclude_repository(self) -> None:
        batch_root = self.root / "outputs/generated/discovery-batches"
        for batch_id, status, github_id, full_name in (
            ("20260901T030804Z-revoked1", "revoked", 20, "owner/retry-later"),
            ("20260901T030804Z-waiting1", "awaiting-approval", 21, "owner/still-waiting"),
        ):
            directory = batch_root / batch_id
            directory.mkdir(parents=True)
            (directory / "manifest.json").write_text(json.dumps({"status": status}), encoding="utf-8")
            (directory / f"{github_id}.project.json").write_text(json.dumps({
                "repository": {"githubId": github_id, "fullName": full_name},
            }), encoding="utf-8")

        ids, names = generated_repositories(self.root)
        self.assertNotIn(20, ids)
        self.assertNotIn("owner/retry-later", names)
        self.assertIn(21, ids)
        self.assertIn("owner/still-waiting", names)


if __name__ == "__main__":
    unittest.main()
