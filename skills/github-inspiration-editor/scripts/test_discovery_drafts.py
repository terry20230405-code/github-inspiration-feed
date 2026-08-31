#!/usr/bin/env python3
"""Offline tests for AI draft orchestration and artifact generation."""

from __future__ import annotations

import json
import copy
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import generate_discovery_drafts as drafts


def ai_provider() -> dict[str, object]:
    return {
        "protocol": "openai-chat-completions",
        "baseUrl": "https://4router.net/v1",
        "model": "gpt-5.4",
        "reasoningEffort": "medium",
        "maxCompletionTokens": 16000,
    }


def generation_payload() -> dict[str, object]:
    directions = [
        {
            "id": "family-memory-map",
            "name": "家庭回忆地图",
            "tagline": "导入照片位置，得到一张可以共同浏览的家庭旅程地图",
            "problem": "家庭成员的旅行照片散落在不同设备中，很难共同回顾完整旅程。",
            "audience": "希望共同整理旅行记忆的家庭成员",
            "approach": "连接照片目录，读取时间与位置，再用原项目的可视化能力生成可浏览的旅程节点。",
            "difference": "原项目展示通用数据，新产品围绕家庭照片形成共同整理和讲述旅程的流程。",
            "scope": ["导入照片", "读取位置", "生成地图", "补充说明"],
        },
        {
            "id": "learning-path-board",
            "name": "学习路径看板",
            "tagline": "输入课程资料，得到一张可以追踪进度的知识路线图",
            "problem": "自学者面对大量资料时，不容易判断知识之间的关系和下一步。",
            "audience": "正在自学一门新技能的学习者",
            "approach": "导入课程目录，提取主题关系，并复用原项目的节点布局生成学习路径。",
            "difference": "它不展示通用系统，而是把资料依赖变成带完成状态的个人学习流程。",
            "scope": ["导入目录", "生成节点", "标记进度", "查看前置知识"],
        },
        {
            "id": "community-resource-map",
            "name": "社区资源地图",
            "tagline": "填写服务地点，得到一张可以搜索的社区互助资源图",
            "problem": "社区成员不知道附近有哪些可以重复使用的公共与互助资源。",
            "audience": "社区志愿者和刚搬入社区的居民",
            "approach": "录入资源名称、地点和服务时间，复用原项目的连接与搜索能力形成资源网络。",
            "difference": "它把技术可视化能力改造成面向居民的地点发现和互助协调工具。",
            "scope": ["录入资源", "地点分类", "地图搜索", "查看服务时间"],
        },
    ]
    facts = [
        {"id": "F1", "claim": "该仓库是公开且活跃的原始项目。", "sourceIds": ["S1"]},
        {"id": "F2", "claim": "用户可以导入结构化资料并生成交互式节点图。", "sourceIds": ["S2"]},
        {"id": "F3", "claim": "生成结果支持搜索、连接查看和导出。", "sourceIds": ["S2"]},
    ]
    field_evidence = []
    for field in drafts.FIELD_NAMES:
        inferred = field in {"editorial.hook", "editorial.meaning", "editorial.opportunity"}
        field_evidence.append({
            "field": field,
            "plannedClaim": f"{field} 对应的已核对内容",
            "evidenceIds": ["I1"] if inferred else ["F1", "F2"],
            "status": "inferred" if inferred else "verified",
        })
    return {
        "eligible": True,
        "decisionReason": "README 足够解释产品输入、操作、结果与复用能力。",
        "familyHint": "data",
        "editorial": {
            "hook": "把复杂资料变成可以探索的关系地图",
            "summary": "它允许用户导入结构化资料，把内容整理成带连接关系的交互式节点图。用户可以搜索节点、沿连接查看上下文，并把结果导出分享，从而更直观地理解复杂信息。",
            "meaning": "把结构化信息转成可探索关系图的能力，可以帮助新产品降低理解复杂资料的门槛。",
            "audience": "需要整理和解释复杂结构信息的创作者与开发者",
            "features": ["导入结构化资料", "生成节点关系图", "搜索并追踪连接", "导出可分享结果"],
            "stack": ["TypeScript", "SVG", "JSON"],
            "opportunity": ["关系布局可以把分散资料整理成可探索路径。", "搜索和导出能力可以支持面向普通用户的专题工具。"],
            "directions": directions,
        },
        "facts": facts,
        "fieldEvidence": field_evidence,
        "inferences": [{"id": "I1", "statement": "这些能力适合改造成面向具体生活场景的关系工具。", "basis": ["F2", "F3"], "confidence": "high"}],
        "directionRationales": [
            {"directionId": item["id"], "reusedCapability": "节点布局、连接查看与搜索", "evidenceIds": ["F2", "F3"], "audienceAndProblem": item["problem"], "inputAndOutcome": item["tagline"], "difference": item["difference"]}
            for item in directions
        ],
        "uncertainty": ["没有扫描 Issues，因此不对市场需求作判断。"],
        "localizationDecisions": ["保留 JSON 与 SVG，因为它们帮助读者判断输入和输出形式。"],
    }


def evidence() -> dict[str, object]:
    return {
        "repository": {
            "id": 987654321,
            "full_name": "example/visual-map",
            "name": "visual-map",
            "description": "Turn structured data into an interactive map.",
            "stargazers_count": 1500,
            "forks_count": 120,
            "language": "TypeScript",
            "pushed_at": "2026-08-20T00:00:00Z",
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2026-08-20T00:00:00Z",
            "license": {"name": "MIT License", "spdx_id": "MIT"},
            "archived": False,
            "disabled": False,
            "fork": False,
            "mirror_url": None,
            "default_branch": "main",
            "topics": ["data-visualization"],
            "homepage": None,
            "owner": {"login": "example"},
        },
        "readme": "Visual Map accepts structured JSON and renders an interactive SVG node map with search and exports. " * 20,
        "readmeSha": "abc123",
        "readmeUrl": "https://github.com/example/visual-map/blob/main/README.md",
        "release": None,
    }


def quality_payload(*failed_ids: str) -> dict[str, object]:
    failed = set(failed_ids)
    return {
        "items": [
            {
                "id": item,
                "status": "fail" if item in failed else "pass",
                "evidence": f"{item} 的具体审核证据：{'仍与来源存在无法消除的矛盾' if item in failed else '对应字段与证据已经一致'}。",
            }
            for item in drafts.CHECK_IDS
        ],
        "blockers": [],
    }


class DraftTests(unittest.TestCase):
    def test_research_snapshot_keeps_raw_github_facts(self) -> None:
        note = drafts.research_markdown(
            generation_payload(),
            evidence(),
            "2026-08-30T00:00:00Z",
        )
        self.assertIn("- Repository full name: example/visual-map", note)
        self.assertIn("- Stars at fetch time: 1500", note)
        self.assertIn("- Forks at fetch time: 120", note)
        self.assertIn("- Latest push at fetch time: 2026-08-20T00:00:00Z", note)
        self.assertIn("- License: MIT License", note)
        self.assertIn("captured facts from this fetch, not live values", note)

    def test_a3_is_replaced_by_deterministic_github_check(self) -> None:
        fetched_at = "2026-08-30T00:00:00Z"
        project = {"repository": drafts.repository_layer(evidence(), fetched_at)}
        ai_quality = quality_payload("A3")
        checked = drafts.apply_deterministic_a3(ai_quality, project, evidence(), fetched_at)
        a3 = next(item for item in checked["items"] if item["id"] == "A3")
        self.assertEqual(a3["status"], "pass")
        self.assertIn("程序已逐项核对", a3["evidence"])

        tampered = copy.deepcopy(project)
        tampered["repository"]["stars"] += 1
        failed = drafts.deterministic_a3_item(tampered, evidence(), fetched_at)
        self.assertEqual(failed["status"], "fail")
        self.assertIn("repository.stars", failed["evidence"])

    def test_a3_fixed_benchmark_snapshots_pass_and_tampering_fails(self) -> None:
        published = drafts.read_json(drafts.PROJECT_ROOT / "src/data/repositories.json")
        memos = drafts.read_json(drafts.PROJECT_ROOT / "outputs/generated/usememos-memos.project.json")["repository"]
        benchmark = [published[key] for key in ("remotion", "excalidraw", "immich", "n8n")] + [memos]
        for repository in benchmark:
            with self.subTest(repository=repository["fullName"]):
                source = {
                    "repository": {
                        "id": repository["githubId"],
                        "full_name": repository["fullName"],
                        "stargazers_count": repository["stars"],
                        "forks_count": repository["forks"],
                        "pushed_at": repository["pushedAt"],
                        "license": {"name": repository["license"]},
                        "archived": repository["state"] == "archived",
                        "disabled": repository["state"] == "disabled",
                    }
                }
                exact = drafts.deterministic_a3_item(
                    {"repository": repository},
                    source,
                    repository["fetchedAt"],
                )
                self.assertEqual(exact["status"], "pass")
                tampered = copy.deepcopy(repository)
                tampered["forks"] += 1
                mismatch = drafts.deterministic_a3_item(
                    {"repository": tampered},
                    source,
                    repository["fetchedAt"],
                )
                self.assertEqual(mismatch["status"], "fail")

    def test_builds_chat_completions_request_contract(self) -> None:
        provider = ai_provider()
        schema = {"type": "object", "properties": {"ok": {"type": "boolean"}}, "required": ["ok"], "additionalProperties": False}
        payload = drafts.chat_completions_payload(provider, "system rules", "repository evidence", "test_schema", schema)

        self.assertEqual(drafts.chat_completions_endpoint(provider), "https://4router.net/v1/chat/completions")
        self.assertEqual(payload["model"], "gpt-5.4")
        self.assertEqual(payload["messages"], [
            {"role": "system", "content": "system rules"},
            {"role": "user", "content": "repository evidence"},
        ])
        self.assertEqual(payload["reasoning_effort"], "medium")
        self.assertEqual(payload["max_completion_tokens"], 16000)
        self.assertEqual(payload["response_format"]["json_schema"], {
            "name": "test_schema",
            "strict": True,
            "schema": schema,
        })
        self.assertNotIn("instructions", payload)
        self.assertNotIn("input", payload)

    def test_calls_configured_provider_and_parses_json(self) -> None:
        class FakeResponse:
            def __enter__(self) -> "FakeResponse":
                return self

            def __exit__(self, *_args: object) -> None:
                return None

            def read(self) -> bytes:
                return json.dumps({
                    "choices": [{
                        "finish_reason": "stop",
                        "message": {"role": "assistant", "content": '{"ok":true}'},
                    }],
                }).encode("utf-8")

        schema = {"type": "object", "properties": {"ok": {"type": "boolean"}}, "required": ["ok"], "additionalProperties": False}
        with patch.object(drafts.urllib.request, "urlopen", return_value=FakeResponse()) as urlopen:
            result = drafts.call_ai("sk-test-secret", ai_provider(), "rules", "evidence", "test_schema", schema)

        self.assertEqual(result, {"ok": True})
        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, "https://4router.net/v1/chat/completions")
        self.assertEqual(request.get_header("Authorization"), "Bearer sk-test-secret")
        sent = json.loads(request.data.decode("utf-8"))
        self.assertEqual(sent["response_format"]["type"], "json_schema")

    def test_reads_chat_completion_content_and_rejects_truncation(self) -> None:
        response = {
            "choices": [{
                "finish_reason": "stop",
                "message": {"role": "assistant", "content": '{"ok":true}'},
            }],
        }
        self.assertEqual(drafts.extract_chat_completion_text(response), '{"ok":true}')
        response["choices"][0]["finish_reason"] = "length"
        with self.assertRaisesRegex(drafts.DraftError, "token limit"):
            drafts.extract_chat_completion_text(response)

    def test_redacts_provider_keys_from_error_details(self) -> None:
        key = "sk-sensitive-secret-value"
        detail = f"Incorrect key {key}; fallback sk-anothersecretvalue"
        redacted = drafts.redact_service_detail(detail, key)
        self.assertNotIn(key, redacted)
        self.assertNotIn("sk-anothersecretvalue", redacted)

    def test_zero_candidates_is_a_reported_normal_result(self) -> None:
        config = {
            "aiProvider": ai_provider(),
            "minimumReadmeCharacters": 10_000,
            "aiAnalysisLimit": 1,
            "maxCandidatesPerRun": 1,
        }
        discovery = {
            "policySha256": "b" * 64,
            "aiQueue": [{"fullName": "example/visual-map"}],
        }
        result = drafts.generate_batch(
            config,
            discovery,
            "test-key",
            ai_call=lambda *_args, **_kwargs: self.fail("AI should not be called"),
            evidence_fetcher=lambda _full_name, _token: evidence(),
            now=datetime(2026, 8, 30, 0, 0, tzinfo=timezone.utc),
            write=True,
        )
        self.assertEqual(result["status"], "no-candidates")
        self.assertEqual(result["candidateCount"], 0)
        self.assertEqual(result["rejectedCount"], 1)
        self.assertIn("README 信息不足", result["preview"])
        self.assertEqual(result["batchPath"], "")

    def test_ai_service_error_is_not_misreported_as_candidate_rejection(self) -> None:
        config = {
            "aiProvider": ai_provider(),
            "minimumReadmeCharacters": 100,
            "aiAnalysisLimit": 1,
            "maxCandidatesPerRun": 1,
        }
        discovery = {
            "policySha256": "c" * 64,
            "aiQueue": [{"fullName": "example/visual-map"}],
        }

        def unavailable_ai(*_args: object, **_kwargs: object) -> dict[str, object]:
            raise drafts.AIServiceError("AI provider request failed (403): model access denied")

        with self.assertRaisesRegex(drafts.AIServiceError, "example/visual-map.*403"):
            drafts.generate_batch(
                config,
                discovery,
                "test-key",
                ai_call=unavailable_ai,
                evidence_fetcher=lambda _full_name, _token: evidence(),
                now=datetime(2026, 8, 30, 0, 0, tzinfo=timezone.utc),
                write=False,
            )

    def test_generates_valid_fingerprinted_batch_without_network(self) -> None:
        payload = generation_payload()
        quality = quality_payload()
        calls = iter([payload, quality])

        def fake_ai(*_args: object, **_kwargs: object) -> dict[str, object]:
            return next(calls)

        config = {
            "aiProvider": ai_provider(),
            "minimumReadmeCharacters": 100,
            "aiAnalysisLimit": 2,
            "maxCandidatesPerRun": 1,
        }
        discovery = {
            "policySha256": "a" * 64,
            "aiQueue": [{"fullName": "example/visual-map"}],
        }
        original_root = drafts.GENERATED_ROOT
        with tempfile.TemporaryDirectory(dir=drafts.PROJECT_ROOT / "outputs/generated") as temporary:
            drafts.GENERATED_ROOT = Path(temporary) / "batches"
            try:
                result = drafts.generate_batch(
                    config,
                    discovery,
                    "test-key",
                    ai_call=fake_ai,
                    evidence_fetcher=lambda _full_name, _token: evidence(),
                    now=datetime(2026, 8, 30, 0, 0, tzinfo=timezone.utc),
                    write=True,
                )
                batch = drafts.PROJECT_ROOT / result["batchPath"]
                self.assertTrue((batch / "manifest.json").is_file())
                self.assertTrue((batch / "preview.md").is_file())
                manifest = drafts.read_json(batch / "manifest.json")
                self.assertEqual(len(manifest["candidates"]), 1)
                project_path = next(batch.glob("*.project.json"))
                research_path = next(batch.glob("*.research.md"))
                self.assertEqual(drafts.validate_project(drafts.read_json(project_path)), [])
                self.assertEqual(drafts.validate_research(research_path.read_text(encoding="utf-8")), [])
            finally:
                drafts.GENERATED_ROOT = original_root

    def test_two_failed_repairs_preserve_a4_evidence_and_history(self) -> None:
        first = generation_payload()
        repair_one = copy.deepcopy(first)
        repair_one["editorial"]["summary"] += " 第一轮只收窄了无法验证的表述。"
        repair_two = copy.deepcopy(repair_one)
        repair_two["editorial"]["summary"] = "第二轮从已验证的输入、操作与结果重新构造摘要。"
        calls = iter([
            first,
            quality_payload("A3", "A4"),
            repair_one,
            quality_payload("A4"),
            repair_two,
            quality_payload("A4"),
        ])

        result = drafts.generate_batch(
            {
                "aiProvider": ai_provider(),
                "minimumReadmeCharacters": 100,
                "aiAnalysisLimit": 1,
                "maxCandidatesPerRun": 1,
            },
            {"policySha256": "d" * 64, "aiQueue": [{"fullName": "example/visual-map"}]},
            "test-key",
            ai_call=lambda *_args, **_kwargs: next(calls),
            evidence_fetcher=lambda _full_name, _token: evidence(),
            now=datetime(2026, 8, 30, 0, 0, tzinfo=timezone.utc),
            write=False,
        )

        self.assertEqual(result["status"], "no-candidates")
        rejected = result["rejected"][0]
        self.assertEqual(rejected["stage"], "两轮自动修复后质量复检")
        self.assertEqual([item["id"] for item in rejected["failedChecks"]], ["A4"])
        self.assertIn("仍与来源存在无法消除的矛盾", rejected["failedChecks"][0]["evidence"])
        self.assertEqual(len(rejected["repairHistory"]), 3)
        self.assertEqual(rejected["repairHistory"][0]["failedChecks"][0]["id"], "A4")
        self.assertIn("editorial.summary", rejected["repairHistory"][1]["changedPaths"])
        self.assertNotEqual(rejected["repairHistory"][1]["strategy"], rejected["repairHistory"][2]["strategy"])
        self.assertIn("最终失败证据", result["preview"])
        self.assertIn("A4", result["preview"])


if __name__ == "__main__":
    unittest.main()
