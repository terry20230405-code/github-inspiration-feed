#!/usr/bin/env python3
"""Offline tests for AI draft orchestration and artifact generation."""

from __future__ import annotations

import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

import generate_discovery_drafts as drafts


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


class DraftTests(unittest.TestCase):
    def test_zero_candidates_is_a_reported_normal_result(self) -> None:
        config = {
            "model": "test-model",
            "reasoningEffort": "medium",
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
            openai_call=lambda *_args, **_kwargs: self.fail("OpenAI should not be called"),
            evidence_fetcher=lambda _full_name, _token: evidence(),
            now=datetime(2026, 8, 30, 0, 0, tzinfo=timezone.utc),
            write=True,
        )
        self.assertEqual(result["status"], "no-candidates")
        self.assertEqual(result["candidateCount"], 0)
        self.assertEqual(result["rejectedCount"], 1)
        self.assertIn("README 信息不足", result["preview"])
        self.assertEqual(result["batchPath"], "")

    def test_openai_service_error_is_not_misreported_as_candidate_rejection(self) -> None:
        config = {
            "model": "test-model",
            "reasoningEffort": "medium",
            "minimumReadmeCharacters": 100,
            "aiAnalysisLimit": 1,
            "maxCandidatesPerRun": 1,
        }
        discovery = {
            "policySha256": "c" * 64,
            "aiQueue": [{"fullName": "example/visual-map"}],
        }

        def unavailable_openai(*_args: object, **_kwargs: object) -> dict[str, object]:
            raise drafts.OpenAIServiceError("OpenAI request failed (403): model access denied")

        with self.assertRaisesRegex(drafts.OpenAIServiceError, "example/visual-map.*403"):
            drafts.generate_batch(
                config,
                discovery,
                "test-key",
                openai_call=unavailable_openai,
                evidence_fetcher=lambda _full_name, _token: evidence(),
                now=datetime(2026, 8, 30, 0, 0, tzinfo=timezone.utc),
                write=False,
            )

    def test_generates_valid_fingerprinted_batch_without_network(self) -> None:
        payload = generation_payload()
        quality = {
            "items": [{"id": item, "status": "pass", "evidence": f"{item} has concrete evidence in F1-F3 and the matching project field."} for item in drafts.CHECK_IDS],
            "blockers": [],
        }
        calls = iter([payload, quality])

        def fake_openai(*_args: object, **_kwargs: object) -> dict[str, object]:
            return next(calls)

        config = {
            "model": "test-model",
            "reasoningEffort": "medium",
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
                    openai_call=fake_openai,
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


if __name__ == "__main__":
    unittest.main()
