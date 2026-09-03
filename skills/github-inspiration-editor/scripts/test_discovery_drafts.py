#!/usr/bin/env python3
"""Offline tests for AI draft orchestration and artifact generation."""

from __future__ import annotations

import json
import io
import copy
import tempfile
import threading
import time
import unittest
from datetime import datetime, timezone
from contextlib import redirect_stderr, redirect_stdout
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from unittest.mock import MagicMock, patch

import generate_discovery_drafts as drafts
import ai_stream
import publish_discovery_batch as publisher


def ai_provider() -> dict[str, object]:
    return {
        "protocol": "openai-chat-completions",
        "baseUrl": "https://4router.net/v1",
        "model": "gpt-5.4",
        "reasoningEffort": "medium",
        "maxCompletionTokens": 16000,
    }


class StreamResponse(io.BytesIO):
    def __init__(self, body: bytes, content_type: str = "text/event-stream; charset=utf-8") -> None:
        super().__init__(body)
        self.headers = {"Content-Type": content_type}


def sse_event(value: object) -> bytes:
    data = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    return f"data: {data}\r\n\r\n".encode("utf-8")


def sse_choice(content: str | None = None, *, reason: str | None = None, **delta: object) -> bytes:
    if content is not None:
        delta["content"] = content
    return sse_event({"choices": [{"index": 0, "delta": delta, "finish_reason": reason}]})


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
        {
            "id": "research-evidence-trail",
            "name": "研究证据路线",
            "tagline": "导入资料来源，得到一张可以回查结论依据的证据路线图",
            "problem": "研究者整理多份材料时，结论与来源之间的关系容易丢失。",
            "audience": "需要反复核对资料出处的学生和研究者",
            "approach": "导入资料目录和引用关系，复用原项目的节点布局与搜索能力形成可回查的证据路径。",
            "difference": "原项目展示通用数据，新产品围绕论点、来源和复核状态形成研究工作流。",
            "scope": ["导入资料", "绑定引用", "生成证据路线", "标记复核状态"],
        },
        {
            "id": "accessible-event-guide",
            "name": "无障碍活动指南",
            "tagline": "录入场地信息，得到一张按无障碍条件筛选的活动路线图",
            "problem": "行动不便的参与者很难在出发前确认场地、入口和设施是否适合自己。",
            "audience": "需要提前规划无障碍出行的活动参与者和陪同者",
            "approach": "录入活动地点、入口和设施条件，复用搜索与关系展示能力生成可筛选的到场路线。",
            "difference": "它把通用关系图改造成围绕场地条件核对和到场规划的无障碍决策流程。",
            "scope": ["录入场地", "标记设施", "条件筛选", "生成到场路线"],
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
            {
                "directionId": item["id"],
                "reusedCapability": "节点布局、连接查看与搜索",
                "evidenceIds": ["F2", "F3"],
                "audienceAndProblem": item["problem"],
                "inputAndOutcome": item["tagline"],
                "originalWorkflow": "用户导入通用结构化资料，探索节点关系并导出关系图。",
                "newWorkflow": f"{item['audience']}在具体场景中使用专门输入，经过收窄流程后得到{item['tagline']}。",
                "changedAxes": ["audience", "input", "workflow", "outcome"],
                "productForm": "end-user-product",
                "productBoundary": "用户直接完成一条有明确输入和结果的专用流程，不是裸露节点 API 或通用画布。",
                "difference": item["difference"],
            }
            for item in directions
        ],
        "directionComparisons": [
            {
                "leftDirectionId": directions[left]["id"],
                "rightDirectionId": directions[right]["id"],
                "differentAxes": ["audience", "input", "workflow", "outcome"],
                "comparison": (
                    f"{directions[left]['name']}与{directions[right]['name']}面向不同用户，"
                    "接收不同资料，完成不同流程并产生不同结果。"
                ),
            }
            for left in range(len(directions))
            for right in range(left + 1, len(directions))
        ],
        "uncertainty": ["没有扫描 Issues，因此不对市场需求作判断。"],
        "localizationDecisions": ["保留 JSON 与 SVG，因为它们帮助读者判断输入和输出形式。"],
    }


def evidence() -> dict[str, object]:
    return {
        "fetchedAt": "2026-08-30T00:00:00Z",
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
    direction_ids = [
        "family-memory-map",
        "learning-path-board",
        "community-resource-map",
        "research-evidence-trail",
        "accessible-event-guide",
    ]
    return {
        "selectedDirectionIds": direction_ids[:3],
        "items": [
            {
                "id": item,
                "status": "fail" if item in failed else "pass",
                "evidence": f"{item} 的具体审核证据：{'仍与来源存在无法消除的矛盾' if item in failed else '对应字段与证据已经一致'}。",
            }
            for item in drafts.CHECK_IDS
        ],
        "directionAudits": [
            {
                "directionId": direction_id,
                "changedAxes": ["audience", "input", "workflow", "outcome"],
                "status": "pass",
                "evidence": f"{direction_id} 与原项目相比改变了用户、输入、流程和可见结果。",
            }
            for direction_id in direction_ids
        ],
        "directionPairAudits": [
            {
                "leftDirectionId": direction_ids[left],
                "rightDirectionId": direction_ids[right],
                "differentAxes": ["audience", "input", "workflow", "outcome"],
                "status": "pass",
                "evidence": "这一对方向的用户、输入、核心流程和可见结果均不同。",
            }
            for left in range(len(direction_ids))
            for right in range(left + 1, len(direction_ids))
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
        self.assertIn("## Pairwise direction comparison", note)
        self.assertIn("- Materially changed axes: audience, input, workflow, outcome", note)

    def test_official_license_file_resolves_other_metadata_without_readme_guessing(self) -> None:
        value = evidence()
        value["repository"]["license"] = {"name": "Other", "spdx_id": "NOASSERTION"}
        value["licenseFile"] = {
            "html_url": "https://github.com/example/visual-map/blob/main/LICENSE",
            "license": {"name": "MIT License", "spdx_id": "MIT"},
            "content": "MIT License\n\nCopyright example",
        }

        self.assertEqual(drafts.repository_license_label(value), "MIT License")
        self.assertIn("S4", {item["id"] for item in drafts.source_records(value, "2026-09-03")})
        self.assertIn("officialLicenseFile", json.loads(drafts.evidence_input(value)))

    def test_equivalent_spdx_and_license_name_do_not_conflict(self) -> None:
        value = evidence()
        value["repository"]["license"] = {"name": "MIT License", "spdx_id": "MIT"}
        value["licenseFile"] = {
            "html_url": "https://github.com/example/visual-map/blob/main/LICENSE",
            "license": {"name": "MIT License", "spdx_id": "NOASSERTION"},
            "content": "MIT License\n",
        }

        self.assertEqual(drafts.repository_license_label(value), "MIT License")

    def test_custom_license_uses_title_from_official_file(self) -> None:
        value = evidence()
        value["repository"]["license"] = {"name": "Other", "spdx_id": "NOASSERTION"}
        value["licenseFile"] = {
            "html_url": "https://github.com/example/visual-map/blob/main/LICENSE.md",
            "license": {"name": "Other", "spdx_id": "NOASSERTION"},
            "content": "# Example Community License 1.0\n\nTerms follow.",
        }
        self.assertEqual(drafts.repository_license_label(value), "Example Community License 1.0")

    def test_conflicting_official_license_identities_still_stop(self) -> None:
        value = evidence()
        value["licenseFile"] = {
            "html_url": "https://github.com/example/visual-map/blob/main/LICENSE",
            "license": {"name": "Apache License 2.0", "spdx_id": "Apache-2.0"},
            "content": "Apache License 2.0",
        }
        with self.assertRaisesRegex(drafts.DraftError, "conflicts with official license file"):
            drafts.repository_license_label(value)

    def test_direction_reasoning_requires_real_transformation_matrix(self) -> None:
        payload = generation_payload()
        self.assertEqual(
            drafts.validate_generation_payload(
                payload,
                {"S1", "S2", "S3"},
                expected_direction_count=drafts.DIRECTION_POOL_SIZE,
            ),
            [],
        )

        weak_change = copy.deepcopy(payload)
        weak_change["directionRationales"][0]["changedAxes"] = ["audience"]
        errors = drafts.validate_generation_payload(weak_change, {"S1", "S2", "S3"})
        self.assertTrue(any("at least two unique changed axes" in error for error in errors))

        too_much_infrastructure = copy.deepcopy(payload)
        too_much_infrastructure["directionRationales"][0]["productForm"] = "developer-infrastructure"
        too_much_infrastructure["directionRationales"][1]["productForm"] = "developer-infrastructure"
        errors = drafts.validate_generation_payload(too_much_infrastructure, {"S1", "S2", "S3"})
        self.assertIn("at most one direction may be developer infrastructure", errors)

        missing_pair = copy.deepcopy(payload)
        missing_pair["directionComparisons"].pop()
        errors = drafts.validate_generation_payload(missing_pair, {"S1", "S2", "S3"})
        self.assertIn("direction comparisons must contain every unique direction pair exactly once and in order", errors)

    def test_quality_review_must_challenge_declared_direction_differences(self) -> None:
        instructions = drafts.quality_instructions()
        self.assertIn("Do not accept the generator's changedAxes declarations", instructions)
        self.assertIn("exposing an already-existing API is not enough", instructions)
        self.assertIn("At most one developer-infrastructure direction", instructions)

        project = {"editorial": generation_payload()["editorial"]}
        false_pass = quality_payload()
        false_pass["directionAudits"][0]["status"] = "fail"
        false_pass["directionAudits"][0]["changedAxes"] = ["audience"]
        errors = drafts.validate_quality_payload(false_pass, project)
        self.assertIn("D3 must fail when any selected direction audit fails", errors)
        audit = drafts.quality_audit_entry(0, false_pass, errors, strategy="test", changed_paths=[])
        self.assertEqual(audit["failedDirectionAudits"][0]["directionId"], "family-memory-map")

        pair_false_pass = quality_payload()
        pair_false_pass["directionPairAudits"][0]["status"] = "fail"
        pair_false_pass["directionPairAudits"][0]["differentAxes"] = ["input"]
        errors = drafts.validate_quality_payload(pair_false_pass, project)
        self.assertIn("E1 must fail when any selected direction pair audit fails", errors)
        audit = drafts.quality_audit_entry(0, pair_false_pass, errors, strategy="test", changed_paths=[])
        self.assertEqual(audit["failedDirectionPairAudits"][0]["leftDirectionId"], "family-memory-map")

    def test_quality_review_can_discard_two_weak_directions_and_keep_three(self) -> None:
        payload = generation_payload()
        project = {"editorial": payload["editorial"]}
        quality = quality_payload()
        quality["directionAudits"][3]["status"] = "fail"
        quality["directionAudits"][3]["changedAxes"] = ["audience"]
        quality["directionPairAudits"][6]["status"] = "fail"
        quality["directionPairAudits"][6]["differentAxes"] = ["input"]

        self.assertEqual(drafts.validate_quality_payload(quality, project), [])
        selected_payload = drafts.select_final_generation(payload, quality)
        selected_quality = drafts.select_final_quality(quality, quality["selectedDirectionIds"])

        self.assertEqual(len(selected_payload["editorial"]["directions"]), 3)
        self.assertEqual(
            [direction["id"] for direction in selected_payload["editorial"]["directions"]],
            quality["selectedDirectionIds"],
        )
        self.assertEqual(len(selected_payload["directionComparisons"]), 3)
        self.assertEqual(len(selected_quality["directionAudits"]), 3)
        self.assertEqual(len(selected_quality["directionPairAudits"]), 3)

    def test_review_cannot_fail_an_audit_after_confirming_two_axes(self) -> None:
        project = {"editorial": generation_payload()["editorial"]}
        quality = quality_payload("D3")
        quality["directionAudits"][0]["status"] = "fail"
        errors = drafts.validate_quality_payload(quality, project)
        self.assertTrue(any("cannot fail with two or more verified changed axes" in error for error in errors))

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

    def test_quality_schema_uses_fixed_check_keys_and_normalizes_order(self) -> None:
        schema = drafts.quality_schema()
        items_schema = schema["properties"]["items"]
        self.assertEqual(items_schema["type"], "object")
        self.assertEqual(items_schema["required"], list(drafts.CHECK_IDS))

        quality = quality_payload()
        keyed_items = {
            item["id"]: {"status": item["status"], "evidence": item["evidence"]}
            for item in reversed(quality["items"])
        }
        quality["items"] = keyed_items
        normalized = drafts.normalize_quality_payload(quality)
        self.assertEqual([item["id"] for item in normalized["items"]], list(drafts.CHECK_IDS))

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
                    "usage": {
                        "prompt_tokens": 120,
                        "completion_tokens": 30,
                        "total_tokens": 150,
                        "prompt_tokens_details": {"cached_tokens": 80},
                        "completion_tokens_details": {"reasoning_tokens": 10},
                    },
                }).encode("utf-8")

        schema = {"type": "object", "properties": {"ok": {"type": "boolean"}}, "required": ["ok"], "additionalProperties": False}
        with patch.object(drafts.urllib.request, "urlopen", return_value=FakeResponse()) as urlopen:
            result = drafts.call_ai("sk-test-secret", ai_provider(), "rules", "evidence", "test_schema", schema)

        self.assertEqual(result, {"ok": True})
        self.assertIsInstance(result, drafts.AIResult)
        self.assertEqual(result.telemetry["usage"]["totalTokens"], 150)
        self.assertEqual(result.telemetry["usage"]["cachedPromptTokens"], 80)
        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, "https://4router.net/v1/chat/completions")
        self.assertEqual(request.get_header("Authorization"), "Bearer sk-test-secret")
        sent = json.loads(request.data.decode("utf-8"))
        self.assertEqual(sent["response_format"]["type"], "json_schema")

    def test_stream_keeps_strict_schema_and_assembles_chinese_and_usage(self) -> None:
        body = b": heartbeat\r\n\r\n"
        body += sse_choice(role="assistant")
        body += sse_choice(reasoning_content="not part of the JSON")
        for piece in ('{"句子":', '"流式', '接收完整结果"}'):
            body += sse_choice(piece)
        body += sse_choice(reason="stop")
        body += sse_event({"choices": [], "usage": {"prompt_tokens": 100, "completion_tokens": 30, "total_tokens": 130}})
        body += sse_event("[DONE]")
        provider = {**ai_provider(), "stream": True}
        schema = drafts.generation_schema()
        with patch.object(drafts.urllib.request, "urlopen", return_value=StreamResponse(body)) as urlopen:
            result = drafts.call_ai("test-key", provider, "rules", "evidence", "stream_test", schema)
        self.assertEqual(result, {"句子": "流式接收完整结果"})
        self.assertEqual(result.telemetry["usage"]["totalTokens"], 130)
        self.assertEqual(result.telemetry["transport"]["responseMode"], "stream")
        self.assertIsNotNone(result.telemetry["transport"]["firstEventSeconds"])
        sent = json.loads(urlopen.call_args.args[0].data)
        ordinary = drafts.chat_completions_payload(ai_provider(), "rules", "evidence", "stream_test", schema)
        self.assertEqual(sent.pop("stream_options"), {"include_usage": True})
        self.assertIs(sent.pop("stream"), True)
        self.assertEqual(sent, ordinary)

    def test_stream_without_usage_is_not_reported_as_zero_usage(self) -> None:
        body = sse_choice('{"ok":true}') + sse_choice(reason="stop") + sse_event("[DONE]")
        with patch.object(drafts.urllib.request, "urlopen", return_value=StreamResponse(body)):
            result = drafts.call_ai("test-key", {**ai_provider(), "stream": True}, "rules", "evidence", "test", {})
        self.assertEqual(result, {"ok": True})
        self.assertIsNone(result.telemetry["usage"])

    def test_real_urllib_reads_chunked_sse_with_split_utf8_bytes(self) -> None:
        body = sse_choice('{"句子":"完整结果"}') + sse_choice(reason="stop") + sse_event("[DONE]")
        received: list[dict[str, object]] = []

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, *_args: object) -> None:
                pass

            def do_POST(self) -> None:
                received.append(json.loads(self.rfile.read(int(self.headers["Content-Length"]))))
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Transfer-Encoding", "chunked")
                self.end_headers()
                # Split every byte, including within Chinese UTF-8 sequences.
                for byte in body:
                    self.wfile.write(b"1\r\n" + bytes([byte]) + b"\r\n")
                self.wfile.write(b"0\r\n\r\n")
                self.wfile.flush()

        with HTTPServer(("127.0.0.1", 0), Handler) as server:
            server.timeout = 2
            worker = threading.Thread(target=server.handle_request, daemon=True)
            worker.start()
            try:
                endpoint = f"http://127.0.0.1:{server.server_port}/chat/completions"
                with patch.object(drafts, "chat_completions_endpoint", return_value=endpoint):
                    result = drafts.call_ai("local-test-key", {**ai_provider(), "stream": True}, "rules", "evidence", "test", {}, attempts=1)
                self.assertEqual(result, {"句子": "完整结果"})
                self.assertTrue(received[0]["stream"])
                self.assertTrue(received[0]["response_format"]["json_schema"]["strict"])
            finally:
                worker.join(timeout=3)
            self.assertFalse(worker.is_alive())

    def test_stream_multiline_data_and_bom(self) -> None:
        body = b'\xef\xbb\xbfdata: {"choices":\r\ndata: [{"index":0,"delta":{"content":"{\\"ok\\":true}"},"finish_reason":"stop"}]}\r\n\r\n'
        body += sse_event("[DONE]")
        result = ai_stream.read_chat_stream(StreamResponse(body), started_at=time.monotonic(), on_first_event=lambda: None)
        self.assertEqual(drafts.extract_chat_completion_text(result), '{"ok":true}')

    def test_complete_json_without_stream_terminator_retries_and_discards_partial(self) -> None:
        incomplete = sse_choice('{"wrong":true}') + sse_choice(reason="stop")
        complete = sse_choice('{"ok":true}') + sse_choice(reason="stop") + sse_event("[DONE]")
        with patch.object(drafts.urllib.request, "urlopen", side_effect=[StreamResponse(incomplete), StreamResponse(complete)]) as urlopen, patch.object(drafts.time, "sleep"):
            result = drafts.call_ai("test-key", {**ai_provider(), "stream": True}, "rules", "evidence", "test", {})
        self.assertEqual(result, {"ok": True})
        self.assertEqual(result.telemetry["attempts"], 2)
        self.assertEqual(urlopen.call_args_list[0].args[0].data, urlopen.call_args_list[1].args[0].data)

    def test_stream_failures_keep_attempt_count_in_metrics(self) -> None:
        collector = drafts.AIMetricsCollector()
        broken = sse_choice('{"ok":true}') + sse_choice(reason="stop")
        with patch.object(drafts.urllib.request, "urlopen", side_effect=lambda *_args, **_kwargs: StreamResponse(broken)) as urlopen, patch.object(drafts.time, "sleep"):
            with self.assertRaisesRegex(drafts.AIServiceError, "StreamInterrupted"):
                drafts.invoke_ai(drafts.call_ai, collector, "example/test", "test-key", {**ai_provider(), "stream": True}, "rules", "evidence", "test", {})
        self.assertEqual(urlopen.call_count, 3)
        report = collector.report(wall_time_seconds=1, max_concurrency=1)
        self.assertEqual(report["calls"][0]["attempts"], 3)
        self.assertEqual(report["calls"][0]["transport"]["responseMode"], "stream")
        self.assertIsNone(report["calls"][0]["usage"])
        self.assertEqual(report["successfulCallCount"], 0)

    def test_stream_rejects_missing_stop_even_with_done_and_valid_json(self) -> None:
        body = sse_choice('{"ok":true}') + sse_event("[DONE]")
        with self.assertRaises(ai_stream.StreamInterrupted):
            ai_stream.read_chat_stream(StreamResponse(body), started_at=time.monotonic(), on_first_event=lambda: None)

    def test_stream_rejects_refusal_limit_filter_tool_calls_and_wrong_choice(self) -> None:
        bodies = [
            sse_choice(reason="length"), sse_choice(reason="content_filter"),
            sse_choice(refusal="sk-private-provider-key"),
            sse_choice(tool_calls=[{"name": "unexpected"}]),
            sse_event({"choices": [{"index": 1, "delta": {}, "finish_reason": "stop"}]}),
            sse_event({"error": {"message": "sk-private-provider-key"}}),
            sse_choice('{"ok":true}', reason="stop") + sse_choice("more text"),
        ]
        for body in bodies:
            with self.subTest(body=body), patch.object(drafts.urllib.request, "urlopen", return_value=StreamResponse(body + sse_event("[DONE]"))) as urlopen:
                with self.assertRaises(drafts.AIServiceError) as raised:
                    drafts.call_ai("test-key", {**ai_provider(), "stream": True}, "rules", "evidence", "test", {})
                self.assertEqual(urlopen.call_count, 1)
                self.assertNotIn("sk-private-provider-key", str(raised.exception))

    def test_stream_rejects_malformed_event_and_structured_json(self) -> None:
        bodies = [sse_event("{not-json"), sse_choice("{not-json", reason="stop") + sse_event("[DONE]")]
        for body in bodies:
            with self.subTest(body=body), patch.object(drafts.urllib.request, "urlopen", return_value=StreamResponse(body)):
                with self.assertRaisesRegex(drafts.AIServiceError, "JSONDecodeError"):
                    drafts.call_ai("test-key", {**ai_provider(), "stream": True}, "rules", "evidence", "test", {}, attempts=1)

    def test_stream_reader_has_size_and_elapsed_time_budgets(self) -> None:
        with patch.object(ai_stream, "MAX_LINE_BYTES", 8):
            with self.assertRaisesRegex(ai_stream.StreamProtocolError, "size budget"):
                ai_stream.read_chat_stream(StreamResponse(b"data: too long\n"), started_at=time.monotonic(), on_first_event=lambda: None)
        with patch.object(ai_stream, "MAX_RESPONSE_BYTES", 10):
            with self.assertRaisesRegex(ai_stream.StreamProtocolError, "size budget"):
                ai_stream.read_chat_stream(StreamResponse(b":ping\n" * 3), started_at=time.monotonic(), on_first_event=lambda: None)
        with patch.object(ai_stream.time, "monotonic", side_effect=[0, 1, 2, 601]):
            with self.assertRaisesRegex(ai_stream.StreamInterrupted, "read budget"):
                ai_stream.read_chat_stream(StreamResponse(b":ping\n" * 3), started_at=0, on_first_event=lambda: None)

    def test_stream_request_accepts_complete_json_when_gateway_ignores_stream(self) -> None:
        body = json.dumps({"choices": [{"finish_reason": "stop", "message": {"content": '{"ok":true}'}}]}).encode()
        with patch.object(drafts.urllib.request, "urlopen", return_value=StreamResponse(body, "application/json")) as urlopen:
            result = drafts.call_ai("test-key", {**ai_provider(), "stream": True}, "rules", "evidence", "test", {})
        self.assertEqual(result, {"ok": True})
        self.assertEqual(result.telemetry["transport"]["responseMode"], "json")
        self.assertEqual(urlopen.call_count, 1)

    def test_stream_does_not_retry_unsupported_parameters_or_accept_html(self) -> None:
        error = drafts.urllib.error.HTTPError("https://example.test", 400, "Bad Request", {}, io.BytesIO(b"stream unsupported"))
        with patch.object(drafts.urllib.request, "urlopen", side_effect=error) as urlopen:
            with self.assertRaises(drafts.AIServiceError) as raised:
                drafts.call_ai("test-key", {**ai_provider(), "stream": True}, "rules", "evidence", "test", {})
        self.assertTrue(raised.exception.fatal)
        self.assertEqual(raised.exception.telemetry["attempts"], 1)
        self.assertEqual(urlopen.call_count, 1)
        with patch.object(drafts.urllib.request, "urlopen", return_value=StreamResponse(b"<html>error</html>", "text/html")):
            with self.assertRaisesRegex(drafts.AIServiceError, "compatibility"):
                drafts.call_ai("test-key", {**ai_provider(), "stream": True}, "rules", "evidence", "test", {})

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

    def test_disconnected_ai_request_retries_identical_strict_request(self) -> None:
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = json.dumps({"choices": [{"finish_reason": "stop",
            "message": {"content": '{"ok":true}'}}]}).encode()
        with patch.object(drafts.urllib.request, "urlopen", side_effect=[
            drafts.http.client.RemoteDisconnected("Remote end closed connection without response"), response,
        ]) as urlopen, patch.object(drafts.time, "sleep") as sleep:
            result = drafts.call_ai("test-key", ai_provider(), "rules", "evidence", "retry_test", {"type": "object"})
        self.assertEqual(result, {"ok": True})
        self.assertEqual(result.telemetry["attempts"], 2)
        self.assertEqual(urlopen.call_count, 2)
        sleep.assert_called_once()
        self.assertEqual(urlopen.call_args_list[0].args[0].data, urlopen.call_args_list[1].args[0].data)
        self.assertTrue(json.loads(urlopen.call_args.args[0].data)["response_format"]["json_schema"]["strict"])

    def test_broken_ai_response_retries_are_bounded(self) -> None:
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.side_effect = drafts.http.client.IncompleteRead(b"partial")
        with patch.object(drafts.urllib.request, "urlopen", return_value=response) as urlopen, patch.object(drafts.time, "sleep"):
            with self.assertRaisesRegex(drafts.AIServiceError, "IncompleteRead"):
                drafts.call_ai("test-key", ai_provider(), "rules", "evidence", "retry_test", {"type": "object"})
        self.assertEqual(urlopen.call_count, 3)

    def test_authentication_error_stops_without_retrying(self) -> None:
        error = drafts.urllib.error.HTTPError("https://example.test", 401, "Unauthorized", {}, io.BytesIO(b"bad key"))
        with patch.object(drafts.urllib.request, "urlopen", side_effect=error) as urlopen, patch.object(drafts.time, "sleep") as sleep:
            with self.assertRaises(drafts.AIServiceError) as raised:
                drafts.call_ai("test-key", ai_provider(), "rules", "evidence", "retry_test", {"type": "object"})
        self.assertTrue(raised.exception.fatal)
        self.assertEqual(urlopen.call_count, 1)
        sleep.assert_not_called()

    def test_github_evidence_disconnection_retries_then_recovers(self) -> None:
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = b'{"id":123}'
        with patch.object(drafts.urllib.request, "urlopen", side_effect=[
            drafts.http.client.RemoteDisconnected("closed"), response,
        ]) as urlopen, patch.object(drafts.time, "sleep"):
            self.assertEqual(drafts.request_json("https://api.github.com/repos/example/test", None), {"id": 123})
        self.assertEqual(urlopen.call_count, 2)

    def test_redacts_provider_keys_from_error_details(self) -> None:
        key = "sk-sensitive-secret-value"
        detail = f"Incorrect key {key}; fallback sk-anothersecretvalue"
        redacted = drafts.redact_service_detail(detail, key)
        self.assertNotIn(key, redacted)
        self.assertNotIn("sk-anothersecretvalue", redacted)

    def test_repair_input_omits_deterministic_duplicate_artifacts(self) -> None:
        encoded = drafts.repair_input(
            evidence(),
            generation_payload(),
            quality_payload("B4"),
            ["fieldEvidence is incomplete"],
            1,
        )
        value = json.loads(encoded)
        self.assertIn("primaryEvidence", value)
        self.assertIn("previousGeneration", value)
        self.assertNotIn("previousProject", value)
        self.assertNotIn("previousResearch", value)
        self.assertIn("deterministic derivatives", value["derivedArtifactsOmitted"])
        self.assertEqual(value["repairMode"], "complete-unit-rewrite")
        self.assertEqual(len(value["passingQualityConstraints"]), len(drafts.CHECK_IDS) - 1)

    def test_b1_failure_routes_to_whole_hook_rewrite(self) -> None:
        value = json.loads(drafts.repair_input(
            evidence(),
            generation_payload(),
            quality_payload("B1"),
            [],
            1,
        ))

        guidance = value["targetedRepairRequirements"]
        self.assertEqual(len(guidance), 1)
        self.assertIn("editorial.hook", guidance[0]["scope"])
        self.assertIn("整句重写", guidance[0]["action"])

        unrelated = json.loads(drafts.repair_input(
            evidence(),
            generation_payload(),
            quality_payload("B4"),
            [],
            1,
        ))
        self.assertFalse(any("editorial.hook" in item["scope"] for item in unrelated["targetedRepairRequirements"]))

    def test_second_repair_rebuilds_failed_direction_and_receives_audits(self) -> None:
        review = quality_payload("D3", "E1")
        review["directionAudits"][0] = {
            "directionId": "family-memory-map",
            "changedAxes": ["audience"],
            "status": "fail",
            "evidence": "只更换了用户，输入、流程和结果仍与原项目相同。",
        }
        review["directionPairAudits"][0] = {
            "leftDirectionId": "family-memory-map",
            "rightDirectionId": "learning-path-board",
            "differentAxes": ["audience"],
            "status": "fail",
            "evidence": "两个方向只更换了人群，核心流程仍相同。",
        }

        value = json.loads(drafts.repair_input(evidence(), generation_payload(), review, [], 2))

        self.assertEqual(value["repairMode"], "replacement-rebuild")
        self.assertEqual(value["failedDirectionAudits"][0]["directionId"], "family-memory-map")
        self.assertEqual(value["failedDirectionPairAudits"][0]["leftDirectionId"], "family-memory-map")
        direction_requirement = next(
            item for item in value["targetedRepairRequirements"] if "D3" in item["checks"]
        )
        self.assertIn("删除审核中仍失败的方向", direction_requirement["action"])
        self.assertTrue(any(scope.startswith("directionRationales[") for scope in direction_requirement["scope"]))

    def test_direction_only_repair_cannot_rewrite_passing_project_copy(self) -> None:
        previous = generation_payload()
        repaired = copy.deepcopy(previous)
        repaired["editorial"]["hook"] = "被误改的 Hook"
        repaired["editorial"]["summary"] = "被误改的摘要"
        repaired["facts"][0]["claim"] = "被误改的事实"
        repaired["editorial"]["directions"][0]["name"] = "真正替换的新方向"
        quality = quality_payload("D3", "E3")
        quality["directionAudits"][0]["status"] = "fail"
        quality["directionAudits"][0]["changedAxes"] = ["audience"]

        protected = drafts.enforce_repair_scope(previous, repaired, quality)

        self.assertEqual(protected["editorial"]["hook"], previous["editorial"]["hook"])
        self.assertEqual(protected["editorial"]["summary"], previous["editorial"]["summary"])
        self.assertEqual(protected["facts"], previous["facts"])
        self.assertEqual(protected["editorial"]["directions"][0]["name"], "真正替换的新方向")

    def test_invalid_quality_shape_retries_reviewer_without_rewriting_content(self) -> None:
        invalid_quality = quality_payload()
        invalid_quality["items"] = invalid_quality["items"][:-1]
        calls = iter([generation_payload(), invalid_quality, quality_payload()])

        result = drafts.generate_batch(
            {
                "aiProvider": ai_provider(),
                "minimumReadmeCharacters": 100,
                "aiAnalysisLimit": 1,
                "maxCandidatesPerRun": 1,
            },
            {"policySha256": "9" * 64, "aiQueue": [{"fullName": "example/visual-map"}]},
            "test-key",
            ai_call=lambda *_args, **_kwargs: next(calls),
            evidence_fetcher=lambda _full_name, _token: evidence(),
            now=datetime(2026, 9, 3, 0, 0, tzinfo=timezone.utc),
            write=False,
        )

        self.assertEqual(result["candidateCount"], 1)
        self.assertEqual(result["aiMetrics"]["logicalCallCount"], 3)
        self.assertEqual(
            [call["stage"] for call in result["aiMetrics"]["calls"]],
            ["inspiration_project_draft", "inspiration_quality_review", "inspiration_quality_review_retry"],
        )

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

        result = drafts.generate_batch(
            config, discovery, "test-key", ai_call=unavailable_ai,
            evidence_fetcher=lambda _full_name, _token: evidence(),
            now=datetime(2026, 8, 30, 0, 0, tzinfo=timezone.utc), write=False,
        )
        self.assertEqual(result["status"], "technical-failure")
        self.assertEqual(result["rejectedCount"], 0)
        self.assertEqual(result["errorCount"], 1)
        self.assertIn("403", result["errors"][0]["reason"])

    def test_failed_parallel_candidate_does_not_discard_valid_frozen_batch(self) -> None:
        def fake_evidence(full_name: str, _token: str | None) -> dict[str, object]:
            value = evidence()
            if full_name == "broken/service":
                value["repository"]["full_name"] = full_name
            return value

        def fake_ai(*args: object, **_kwargs: object) -> dict[str, object]:
            if "broken/service" in str(args[3]):
                raise drafts.AIServiceError("RemoteDisconnected after 3 attempts")
            return generation_payload() if args[4] == "inspiration_project_draft" else quality_payload()

        with tempfile.TemporaryDirectory(dir=drafts.PROJECT_ROOT / "outputs/generated") as temporary:
            batch_root = Path(temporary) / "batches"
            with patch.object(drafts, "GENERATED_ROOT", batch_root), patch.object(publisher, "BATCH_ROOT", batch_root):
                result = drafts.generate_batch(
                    {"aiProvider": ai_provider(), "minimumReadmeCharacters": 100, "aiAnalysisLimit": 2,
                     "maxCandidatesPerRun": 2, "maxConcurrentCandidates": 2},
                    {"policySha256": "a" * 64, "aiQueue": [{"fullName": "example/visual-map"}, {"fullName": "broken/service"}]},
                    "test-key", ai_call=fake_ai, evidence_fetcher=fake_evidence, write=True,
                    now=datetime(2026, 9, 3, 0, 0, tzinfo=timezone.utc),
                )
                self.assertEqual(result["status"], "partial-failure")
                self.assertEqual(result["candidateCount"], 1)
                self.assertEqual(result["errorCount"], 1)
                self.assertEqual(result["rejectedCount"], 0)
                self.assertEqual(result["errors"][0]["fullName"], "broken/service")
                self.assertIn("技术故障", result["preview"])
                _, manifest, projects = publisher.load_batch(result["batchId"])
                self.assertEqual(len(projects), 1)
                self.assertFalse(manifest["publicationAuthorized"])

    def test_fatal_service_error_does_not_start_remaining_candidates(self) -> None:
        def unavailable_ai(*_args: object, **_kwargs: object) -> dict[str, object]:
            raise drafts.AIServiceError("401: denied", fatal=True)
        result = drafts.generate_batch(
            {"aiProvider": ai_provider(), "minimumReadmeCharacters": 100, "aiAnalysisLimit": 3,
             "maxCandidatesPerRun": 3, "maxConcurrentCandidates": 1},
            {"policySha256": "a" * 64, "aiQueue": [{"fullName": name} for name in ["first/repo", "second/repo", "third/repo"]]},
            "test-key", ai_call=unavailable_ai, evidence_fetcher=lambda *_args: evidence(), write=False,
        )
        self.assertEqual(result["errorCount"], 1)
        self.assertEqual(result["notStartedCount"], 2)
        self.assertEqual(result["aiMetrics"]["logicalCallCount"], 1)

    def test_cli_partial_failure_outputs_usable_json_and_nonzero_exit(self) -> None:
        config = drafts.read_json(drafts.DEFAULT_CONFIG)
        result = {"status": "partial-failure", "candidateCount": 1, "errorCount": 1,
                  "batchId": "test-batch", "batchPath": "outputs/generated/discovery-batches/test-batch", "preview": "report"}
        stdout = io.StringIO()
        with patch.object(drafts.sys, "argv", ["generate_discovery_drafts.py", "--write"]), \
             patch.dict(drafts.os.environ, {"OPENAI_API_KEY": "test-key"}), \
             patch.object(drafts, "read_json", return_value=config), \
             patch.object(drafts, "generate_batch", return_value=result), \
             redirect_stdout(stdout):
            exit_code = drafts.main()
        self.assertEqual(exit_code, 1)
        self.assertEqual(json.loads(stdout.getvalue()), result)

    def test_cli_unexpected_network_failure_still_outputs_redacted_diagnostic(self) -> None:
        config = drafts.read_json(drafts.DEFAULT_CONFIG)
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(drafts.sys, "argv", ["generate_discovery_drafts.py", "--write"]), \
             patch.dict(drafts.os.environ, {"OPENAI_API_KEY": "test-key"}), \
             patch.object(drafts, "read_json", return_value=config), \
             patch.object(drafts, "generate_batch", side_effect=ConnectionResetError("closed test-key")), \
             redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = drafts.main()
        self.assertEqual(exit_code, 1)
        report = json.loads(stdout.getvalue())
        self.assertEqual(report["status"], "technical-failure")
        self.assertEqual(report["candidateCount"], 0)
        self.assertNotIn("test-key", stdout.getvalue() + stderr.getvalue())

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
                project = drafts.read_json(project_path)
                self.assertEqual(drafts.validate_project(project), [])
                self.assertEqual(len(project["editorial"]["directions"]), drafts.FINAL_DIRECTION_COUNT)
                self.assertEqual(drafts.validate_research(research_path.read_text(encoding="utf-8")), [])
            finally:
                drafts.GENERATED_ROOT = original_root

    def test_acquisition_timestamp_is_recorded_by_fetcher_not_github(self) -> None:
        captured = datetime(2026, 9, 4, 3, 2, 1, tzinfo=timezone.utc)

        def request(url: str, _token: str | None, **_kwargs: object) -> object:
            if url.endswith("/readme"):
                return {"content": drafts.base64.b64encode(b"Official README").decode(), "sha": "abc"}
            if url.endswith("/releases/latest") or url.endswith("/license"):
                return None
            return {**evidence()["repository"], "fetchedAt": "untrusted upstream field"}

        with patch.object(drafts, "utc_now", return_value=captured):
            snapshot = drafts.fetch_evidence("example/visual-map", None, request=request)
        self.assertEqual(snapshot["fetchedAt"], "2026-09-04T03:02:01Z")
        supplied = json.loads(drafts.evidence_input(snapshot))
        self.assertEqual(supplied["orchestratorContext"]["fetchedAt"], snapshot["fetchedAt"])
        self.assertNotIn("fetchedAt", supplied["metadata"])

    def test_missing_or_invalid_acquisition_time_is_a_technical_error(self) -> None:
        for timestamp in (None, "未知", "2026-02-31T00:00:00Z", "2026-09-04T00:00:00+00:00"):
            with self.subTest(timestamp=timestamp):
                snapshot = evidence()
                snapshot["fetchedAt"] = timestamp
                with self.assertRaises(drafts.RepositoryServiceError):
                    drafts.evidence_input(snapshot)

    def test_same_timestamp_reaches_generation_both_repairs_reviews_and_frozen_batch(self) -> None:
        timestamp = "2026-09-04T03:02:01Z"
        snapshot = evidence()
        snapshot["fetchedAt"] = timestamp
        captured_inputs: list[tuple[str, dict[str, object]]] = []
        replies = iter([generation_payload(), quality_payload("B1"), generation_payload(), quality_payload("B1"), generation_payload(), quality_payload()])

        def fake_ai(_key: str, _provider: object, _rules: str, input_text: str, stage: str, _schema: object) -> dict[str, object]:
            supplied = json.loads(input_text)
            captured_inputs.append((stage, supplied))
            if stage == "inspiration_project_draft":
                self.assertEqual(supplied["orchestratorContext"]["fetchedAt"], timestamp)
            elif "repair" in stage:
                self.assertEqual(supplied["primaryEvidence"]["orchestratorContext"]["fetchedAt"], timestamp)
            else:
                self.assertEqual(supplied["project"]["repository"]["fetchedAt"], timestamp)
                self.assertIn(f"- Fetched at: {timestamp}", supplied["research"])
            return next(replies)

        with tempfile.TemporaryDirectory(dir=drafts.PROJECT_ROOT / "outputs/generated") as temporary, patch.object(drafts, "GENERATED_ROOT", Path(temporary) / "batches"):
            result = drafts.generate_batch(
                {"aiProvider": ai_provider(), "minimumReadmeCharacters": 100, "aiAnalysisLimit": 1, "maxCandidatesPerRun": 1},
                {"policySha256": "b" * 64, "aiQueue": [{"fullName": "example/visual-map"}]},
                "test-key", ai_call=fake_ai, evidence_fetcher=lambda *_args: snapshot,
                now=datetime(2026, 9, 4, 3, 0, 0, tzinfo=timezone.utc), write=True,
            )
            self.assertEqual(result["candidateCount"], 1)
            self.assertEqual(len(captured_inputs), 6)
            batch = drafts.PROJECT_ROOT / result["batchPath"]
            project = drafts.read_json(next(batch.glob("*.project.json")))
            self.assertEqual(project["repository"]["fetchedAt"], timestamp)
            self.assertIn(f"- Fetched at: {timestamp}", next(batch.glob("*.research.md")).read_text(encoding="utf-8"))
            self.assertEqual(drafts.deterministic_a3_item(project, snapshot, timestamp)["status"], "pass")

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

    def test_direction_failure_without_first_round_progress_gets_replacement_rebuild(self) -> None:
        first = generation_payload()
        repair_one = copy.deepcopy(first)
        repair_one["editorial"]["directions"][0]["name"] = "仍未形成差异的家庭地图"
        repair_two = copy.deepcopy(first)
        repair_two["editorial"]["directions"][0]["name"] = "重新构造的不同产品"
        initial_quality = quality_payload("D3")
        initial_quality["directionAudits"][0]["status"] = "fail"
        initial_quality["directionAudits"][0]["changedAxes"] = ["audience"]
        repair_quality = copy.deepcopy(initial_quality)
        calls = iter([
            first,
            initial_quality,
            repair_one,
            repair_quality,
            repair_two,
            quality_payload(),
        ])
        call_count = 0

        def fake_ai(*_args: object, **_kwargs: object) -> dict[str, object]:
            nonlocal call_count
            call_count += 1
            return next(calls)

        result = drafts.generate_batch(
            {
                "aiProvider": ai_provider(),
                "minimumReadmeCharacters": 100,
                "aiAnalysisLimit": 1,
                "maxCandidatesPerRun": 1,
            },
            {"policySha256": "e" * 64, "aiQueue": [{"fullName": "example/visual-map"}]},
            "test-key",
            ai_call=fake_ai,
            evidence_fetcher=lambda _full_name, _token: evidence(),
            now=datetime(2026, 8, 30, 0, 0, tzinfo=timezone.utc),
            write=False,
        )

        self.assertEqual(call_count, 6)
        self.assertEqual(result["candidateCount"], 1)
        self.assertEqual(result["rejectedCount"], 0)

    def test_two_candidates_run_concurrently_but_results_keep_queue_order(self) -> None:
        active = 0
        max_active = 0
        lock = threading.Lock()

        def fake_ai(*args: object, **_kwargs: object) -> dict[str, object]:
            nonlocal active, max_active
            schema_name = str(args[4])
            with lock:
                active += 1
                max_active = max(max_active, active)
            time.sleep(0.03)
            with lock:
                active -= 1
            return copy.deepcopy(generation_payload() if schema_name == "inspiration_project_draft" else quality_payload())

        def candidate_evidence(full_name: str, _token: str | None) -> dict[str, object]:
            value = evidence()
            repository = value["repository"]
            assert isinstance(repository, dict)
            owner, name = full_name.split("/", 1)
            repository["id"] = 1000 if owner == "first" else 1001
            repository["full_name"] = full_name
            repository["name"] = name
            repository["owner"] = {"login": owner}
            value["readmeUrl"] = f"https://github.com/{full_name}/blob/main/README.md"
            return value

        result = drafts.generate_batch(
            {
                "aiProvider": ai_provider(),
                "minimumReadmeCharacters": 100,
                "aiAnalysisLimit": 2,
                "maxCandidatesPerRun": 2,
                "maxConcurrentCandidates": 2,
            },
            {
                "policySha256": "f" * 64,
                "aiQueue": [{"fullName": "first/shared"}, {"fullName": "second/shared"}],
            },
            "test-key",
            ai_call=fake_ai,
            evidence_fetcher=candidate_evidence,
            now=datetime(2026, 8, 30, 0, 0, tzinfo=timezone.utc),
            write=False,
        )

        self.assertGreaterEqual(max_active, 2)
        self.assertEqual(result["candidateCount"], 2)
        self.assertEqual(result["aiMetrics"]["maxConcurrentCandidates"], 2)
        self.assertEqual(result["aiMetrics"]["logicalCallCount"], 4)
        self.assertEqual(
            {call["candidate"] for call in result["aiMetrics"]["calls"]},
            {"first/shared", "second/shared"},
        )
        self.assertLess(result["preview"].index("first/shared"), result["preview"].index("second/shared"))

    def test_rolling_concurrency_starts_next_candidate_before_slowest_finishes(self) -> None:
        first_generation_finished = threading.Event()
        third_started_before_first_finished = False
        lock = threading.Lock()
        timestamps = {f"{owner}/shared": f"2026-09-03T00:00:0{index}Z" for index, owner in enumerate(("first", "second", "third"), 1)}

        def fake_ai(*args: object, **_kwargs: object) -> dict[str, object]:
            nonlocal third_started_before_first_finished
            input_value = json.loads(str(args[3]))
            schema_name = str(args[4])
            if schema_name == "inspiration_project_draft":
                full_name = str(input_value["metadata"]["full_name"])
                self.assertEqual(input_value["orchestratorContext"]["fetchedAt"], timestamps[full_name])
            else:
                full_name = str(input_value["project"]["repository"]["fullName"])
                self.assertEqual(input_value["project"]["repository"]["fetchedAt"], timestamps[full_name])
            if full_name == "first/shared" and schema_name == "inspiration_project_draft":
                time.sleep(0.20)
                first_generation_finished.set()
            else:
                if full_name == "third/shared" and schema_name == "inspiration_project_draft":
                    with lock:
                        third_started_before_first_finished = not first_generation_finished.is_set()
                time.sleep(0.01)
            return copy.deepcopy(generation_payload() if schema_name == "inspiration_project_draft" else quality_payload())

        def candidate_evidence(full_name: str, _token: str | None) -> dict[str, object]:
            value = evidence()
            repository = value["repository"]
            assert isinstance(repository, dict)
            owner, name = full_name.split("/", 1)
            repository["id"] = {"first": 2001, "second": 2002, "third": 2003}[owner]
            value["fetchedAt"] = timestamps[full_name]
            repository["full_name"] = full_name
            repository["name"] = name
            repository["owner"] = {"login": owner}
            value["readmeUrl"] = f"https://github.com/{full_name}/blob/main/README.md"
            return value

        result = drafts.generate_batch(
            {
                "aiProvider": ai_provider(),
                "minimumReadmeCharacters": 100,
                "aiAnalysisLimit": 3,
                "maxCandidatesPerRun": 3,
                "maxConcurrentCandidates": 2,
            },
            {
                "policySha256": "8" * 64,
                "aiQueue": [
                    {"fullName": "first/shared"},
                    {"fullName": "second/shared"},
                    {"fullName": "third/shared"},
                ],
            },
            "test-key",
            ai_call=fake_ai,
            evidence_fetcher=candidate_evidence,
            now=datetime(2026, 9, 3, 0, 0, tzinfo=timezone.utc),
            write=False,
        )

        self.assertTrue(third_started_before_first_finished)
        self.assertEqual(result["candidateCount"], 3)
        self.assertLess(result["preview"].index("first/shared"), result["preview"].index("second/shared"))
        self.assertLess(result["preview"].index("second/shared"), result["preview"].index("third/shared"))


if __name__ == "__main__":
    unittest.main()
