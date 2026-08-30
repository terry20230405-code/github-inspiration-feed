#!/usr/bin/env python3
"""Tests for the stage-ten approval and atomic publication workflow."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from dataclasses import asdict
from pathlib import Path

from generate_visual_identity import generate_visual_identity
from manage_publication import (
    DATA_PATHS,
    approve_candidate,
    create_publication_backup,
    data_fingerprint,
    prepare_candidate,
    publish_candidate,
    recover_publication,
)
from validate_quality_review import CHECK_IDS


def write_json(root: Path, relative: str, value: object) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def editorial(suffix: str = "") -> dict[str, object]:
    return {
        "hook": f"把零散输入变成清楚可用的结果{suffix}",
        "summary": "用户先输入一组结构化资料，系统再通过清楚的操作流程完成整理、连接和检查，最后生成可以直接查看、分享与继续编辑的页面结果。",
        "meaning": "现有项目已经提供稳定的输入、处理与输出底座，因此可以继续包装成面向具体人群的轻量产品。",
        "audience": "需要整理资料并得到清楚结果的个人与小团队",
        "features": ["结构化资料输入", "可视化处理流程", "结果页面导出"],
        "stack": ["React", "TypeScript"],
        "opportunity": ["通用界面仍需要用户自行设计流程", "稳定底座可以承载更聚焦的使用场景"],
        "directions": [
            {
                "id": "personal-review", "name": "个人资料回顾", "tagline": "输入每日记录，得到一页回顾",
                "problem": "个人记录很多内容，却很少重新整理和回顾。", "audience": "持续记录的个人用户",
                "approach": "导入每日记录，按主题整理，再生成一页可确认的回顾。", "difference": "从通用工具变成固定频率的个人回顾流程。",
                "scope": ["记录导入", "主题整理", "回顾页面"],
            },
            {
                "id": "lesson-helper", "name": "课堂资料助手", "tagline": "输入课程资料，得到讲解卡片",
                "problem": "教师每周都要把零散资料重新整理成讲解顺序。", "audience": "中小学教师",
                "approach": "导入课程资料，确认讲解顺序，再导出课堂卡片。", "difference": "围绕教学输入和课堂结果提供固定流程。",
                "scope": ["资料导入", "顺序确认", "卡片导出"],
            },
            {
                "id": "team-brief", "name": "团队简报生成器", "tagline": "连接项目更新，得到团队简报",
                "problem": "小团队每周重复收集进度并整理成简报。", "audience": "小团队负责人",
                "approach": "连接项目更新，按成员和主题归类，再生成可分享简报。", "difference": "将自由整理收窄为团队周报工作流。",
                "scope": ["更新导入", "成员归类", "简报分享"],
            },
        ],
    }


def repository(github_id: int, full_name: str, name: str) -> dict[str, object]:
    return {
        "githubId": github_id, "fullName": full_name, "name": name, "stars": 10, "forks": 2,
        "language": "TypeScript", "pushedAt": "2026-08-29T00:00:00Z", "license": "MIT",
        "state": "active", "fetchedAt": "2026-08-30T00:00:00Z",
    }


def project(project_id: str, github_id: int, full_name: str, *, avoid: tuple[str, ...] = (), copy: dict[str, object] | None = None) -> dict[str, object]:
    return {
        "schemaVersion": 2,
        "id": project_id,
        "repository": repository(github_id, full_name, project_id.title()),
        "editorial": copy or editorial(),
        "visual": asdict(generate_visual_identity(full_name, avoid=avoid)),
    }


def research_note(full_name: str, project_id: str) -> str:
    fields = (
        "repository.githubId", "repository.fullName", "repository.name", "repository.stars",
        "repository.forks", "repository.language", "repository.pushedAt", "repository.license",
        "repository.state", "editorial.hook", "editorial.summary", "editorial.meaning",
        "editorial.audience", "editorial.features", "editorial.stack", "editorial.opportunity",
    )
    table = "\n".join(f"| `{field}` | claim | F1 | verified |" for field in fields)
    return f"""# {full_name} research notes

Research date: 2026-08-30
Repository: https://github.com/{full_name}
Research mode: new

## Snapshot

- Repository state: active
- Fetched at: 2026-08-30T00:00:00Z

## Sources

- [S1] Official repository — https://github.com/{full_name}

## Verified repository facts

- [F1] Official identity and product capability. Sources: S1
- [F2] Official workflow and visible outcome. Sources: S1
- [F3] Official technology and license. Sources: S1

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
{table}

## Product inferences

- [I1] The focused products are proposals. Basis: F1, F2. Confidence: medium

## Direction rationale

### D1 — 个人资料回顾
- Reuses F1 and produces a review page.

### D2 — 课堂资料助手
- Reuses F2 and produces lesson cards.

### D3 — 团队简报生成器
- Reuses F1 and produces a team brief.

## Uncertainty

- Dynamic counts are snapshots.

## Localization decisions

- Basic frontend terms are retained.

## Refresh notes

- Initial candidate for {project_id}.
"""


def seed_root(root: Path) -> dict[str, object]:
    alpha = project("alpha", 1, "example/alpha")
    write_json(root, "src/data/order.json", ["alpha"])
    write_json(root, "src/data/repositories.json", {"alpha": alpha["repository"]})
    write_json(root, "src/data/editorial.json", {"alpha": alpha["editorial"]})
    write_json(root, "src/data/visuals.json", {"alpha": alpha["visual"]})
    return alpha


def make_artifacts(root: Path, candidate: dict[str, object], label: str = "candidate") -> tuple[Path, Path, Path]:
    base = f"outputs/generated/{label}"
    project_path = write_json(root, f"{base}.project.json", candidate)
    research_path = root / f"{base}.research.md"
    research_path.parent.mkdir(parents=True, exist_ok=True)
    research_path.write_text(research_note(candidate["repository"]["fullName"], candidate["id"]), encoding="utf-8")
    quality = {
        "schemaVersion": 1,
        "projectId": candidate["id"],
        "projectPath": project_path.relative_to(root).as_posix(),
        "researchPath": research_path.relative_to(root).as_posix(),
        "projectSha256": sha256(project_path),
        "researchSha256": sha256(research_path),
        "reviewedAt": "2026-08-30T00:00:00Z",
        "items": [{"id": check_id, "status": "pass", "evidence": f"Verified {check_id} against F1-F3."} for check_id in CHECK_IDS],
        "blockers": [],
        "publicationCandidate": True,
        "publicationAuthorized": False,
    }
    quality_path = write_json(root, f"{base}.quality.json", quality)
    return project_path, research_path, quality_path


def no_op_checks(_: Path) -> list[dict[str, object]]:
    return [{"command": "test", "exitCode": 0}]


class PublicationWorkflowTests(unittest.TestCase):
    def prepare(self, root: Path, candidate: dict[str, object], *, mode: str = "add", label: str = "candidate") -> str:
        paths = make_artifacts(root, candidate, label)
        result = prepare_candidate(root, *paths, mode=mode, write=True, now=lambda: "2026-08-30T00:00:00Z")
        return str(result["candidateId"])

    def test_prepare_freezes_validated_candidate_and_preview(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            alpha = seed_root(root)
            beta = project("beta", 2, "example/beta", avoid=(alpha["visual"]["accent"],))
            candidate_id = self.prepare(root, beta)
            candidate_root = root / "outputs/generated/publication-candidates" / candidate_id
            manifest = json.loads((candidate_root / "manifest.json").read_text(encoding="utf-8"))
            preview_exists = (candidate_root / "preview.md").is_file()
        self.assertEqual(manifest["status"], "awaiting-approval")
        self.assertFalse(manifest["publicationAuthorized"])
        self.assertTrue(preview_exists)

    def test_duplicate_repository_identity_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            alpha = seed_root(root)
            duplicate = project("other", 1, "example/other", avoid=(alpha["visual"]["accent"],))
            paths = make_artifacts(root, duplicate)
            with self.assertRaisesRegex(ValueError, "duplicates published"):
                prepare_candidate(root, *paths)

    def test_adjacent_color_collision_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            alpha = seed_root(root)
            beta = project("beta", 2, "example/beta")
            beta["visual"]["accent"] = alpha["visual"]["accent"]
            beta["visual"]["foreground"] = alpha["visual"]["foreground"]
            paths = make_artifacts(root, beta)
            with self.assertRaisesRegex(ValueError, "too close"):
                prepare_candidate(root, *paths)

    def test_publication_requires_written_human_approval(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            alpha = seed_root(root)
            beta = project("beta", 2, "example/beta", avoid=(alpha["visual"]["accent"],))
            candidate_id = self.prepare(root, beta)
            approve_candidate(root, candidate_id, "Terry", write=False)
            with self.assertRaisesRegex(ValueError, "requires a current human approval"):
                publish_candidate(root, candidate_id)

    def test_approved_publication_updates_all_layers_atomically(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            alpha = seed_root(root)
            beta = project("beta", 2, "example/beta", avoid=(alpha["visual"]["accent"],))
            candidate_id = self.prepare(root, beta)
            approve_candidate(root, candidate_id, "Terry", write=True, now=lambda: "2026-08-30T00:01:00Z")
            result = publish_candidate(root, candidate_id, write=True, now=lambda: "2026-08-30T00:02:00Z", id_factory=lambda: "publish-test", check_runner=no_op_checks)
            order = json.loads((root / DATA_PATHS[0]).read_text(encoding="utf-8"))
            layers = [json.loads((root / path).read_text(encoding="utf-8")) for path in DATA_PATHS[1:]]
        self.assertEqual(order, ["alpha", "beta"])
        self.assertTrue(all("beta" in layer for layer in layers))
        self.assertEqual(result["status"], "published")
        self.assertFalse(result["rolledBack"])

    def test_failed_check_restores_every_data_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            alpha = seed_root(root)
            beta = project("beta", 2, "example/beta", avoid=(alpha["visual"]["accent"],))
            before = {path: (root / path).read_bytes() for path in DATA_PATHS}
            candidate_id = self.prepare(root, beta)
            approve_candidate(root, candidate_id, "Terry", write=True)
            def fail(_: Path) -> list[dict[str, object]]:
                raise RuntimeError("simulated build failure")
            with self.assertRaisesRegex(RuntimeError, "data was restored"):
                publish_candidate(root, candidate_id, write=True, id_factory=lambda: "publish-fail", check_runner=fail)
            after = {path: (root / path).read_bytes() for path in DATA_PATHS}
            transaction = json.loads((root / "outputs/versions/publications/publish-fail/manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(before, after)
        self.assertEqual(transaction["status"], "rolled-back")

    def test_changed_data_invalidates_old_approval(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            alpha = seed_root(root)
            beta = project("beta", 2, "example/beta", avoid=(alpha["visual"]["accent"],))
            candidate_id = self.prepare(root, beta)
            approve_candidate(root, candidate_id, "Terry", write=True)
            repositories = json.loads((root / "src/data/repositories.json").read_text(encoding="utf-8"))
            repositories["alpha"]["stars"] = 99
            write_json(root, "src/data/repositories.json", repositories)
            with self.assertRaisesRegex(ValueError, "changed after candidate preparation"):
                publish_candidate(root, candidate_id)

    def test_interrupted_transaction_can_be_manually_recovered(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            seed_root(root)
            before = {path: (root / path).read_bytes() for path in DATA_PATHS}
            create_publication_backup(root, "interrupted-test", "beta-candidate")
            write_json(root, "src/data/order.json", ["partial-write"])
            preview = recover_publication(root, "interrupted-test")
            result = recover_publication(root, "interrupted-test", write=True, now=lambda: "2026-08-30T00:03:00Z")
            after = {path: (root / path).read_bytes() for path in DATA_PATHS}
        self.assertEqual(preview["currentStatus"], "backup-created")
        self.assertEqual(before, after)
        self.assertTrue(result["verified"])

    def test_replace_mode_changes_editorial_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            alpha = seed_root(root)
            replacement = {**alpha, "editorial": editorial("新")}
            candidate_id = self.prepare(root, replacement, mode="replace", label="replacement")
            approve_candidate(root, candidate_id, "Terry", write=True)
            publish_candidate(root, candidate_id, write=True, id_factory=lambda: "replace-test", check_runner=no_op_checks)
            order = json.loads((root / "src/data/order.json").read_text(encoding="utf-8"))
            repositories = json.loads((root / "src/data/repositories.json").read_text(encoding="utf-8"))
            visuals = json.loads((root / "src/data/visuals.json").read_text(encoding="utf-8"))
            published_editorial = json.loads((root / "src/data/editorial.json").read_text(encoding="utf-8"))
        self.assertEqual(order, ["alpha"])
        self.assertEqual(repositories["alpha"], alpha["repository"])
        self.assertEqual(visuals["alpha"], alpha["visual"])
        self.assertTrue(published_editorial["alpha"]["hook"].endswith("新"))


if __name__ == "__main__":
    unittest.main()
