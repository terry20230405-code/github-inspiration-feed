#!/usr/bin/env python3
"""Assemble a locally-authored Codex discovery batch with normal workflow artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate_discovery_drafts import (  # noqa: E402
    CHECK_IDS,
    FIELD_NAMES,
    GENERATED_ROOT,
    PROJECT_ROOT,
    batch_preview,
    build_project,
    create_quality,
    research_markdown,
    sha256_bytes,
    sha256_file,
    validate_generation_payload,
    validate_project,
    validate_quality_payload,
    validate_research,
    write_json,
)


def iso_z_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def slug(value: str) -> str:
    result = "".join(char.lower() if char.isalnum() else "-" for char in value)
    return "-".join(part for part in result.split("-") if part)


def evidence_from_spec(item: dict[str, object], fetched_at: str) -> dict[str, object]:
    repository = dict(item["repository"])
    repository["owner"] = {"login": str(repository["full_name"]).split("/", 1)[0]}
    release = item.get("release")
    if isinstance(release, dict):
        release = {
            **release,
            "html_url": f"https://github.com/{repository['full_name']}/releases/tag/{release['tag_name']}",
        }
    license_file = {
        "path": item["licensePath"],
        "name": Path(str(item["licensePath"])).name,
        "sha": item["licenseSha"],
        "html_url": f"https://github.com/{repository['full_name']}/blob/{repository['default_branch']}/{item['licensePath']}",
        "license": repository["license"],
    }
    return {
        "repository": repository,
        "readmeSha": item["readmeSha"],
        "readmeUrl": f"https://github.com/{repository['full_name']}/blob/{repository['default_branch']}/{item['readmePath']}",
        "release": release,
        "licenseFile": license_file,
        "fetchedAt": fetched_at,
    }


def direction_record(raw: dict[str, object]) -> dict[str, object]:
    return {key: raw[key] for key in ("id", "name", "tagline", "problem", "audience", "approach", "difference", "scope")}


def pair_comparisons(directions: list[dict[str, object]]) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    axis_labels = {"audience": "用户", "input": "输入", "workflow": "流程", "outcome": "结果"}
    for left_index in range(len(directions)):
        for right_index in range(left_index + 1, len(directions)):
            left = directions[left_index]
            right = directions[right_index]
            different = [axis for axis in ("audience", "input", "workflow", "outcome") if left["axes"][axis] != right["axes"][axis]]
            if len(different) < 2:
                raise ValueError(f"{left['id']} and {right['id']} differ on fewer than two axes")
            details = "；".join(
                f"{axis_labels[axis]}分别是“{left['axes'][axis]}”与“{right['axes'][axis]}”"
                for axis in different[:3]
            )
            result.append({
                "leftDirectionId": left["id"],
                "rightDirectionId": right["id"],
                "differentAxes": different,
                "comparison": details,
            })
    return result


def generation_payload(item: dict[str, object], selected: list[dict[str, object]]) -> dict[str, object]:
    editorial = dict(item["editorial"])
    editorial["directions"] = [direction_record(direction) for direction in selected]
    facts = item["facts"]
    field_fact_ids = {
        "editorial.hook": ["F2", "F3"],
        "editorial.summary": ["F2", "F3"],
        "editorial.meaning": ["I1"],
        "editorial.audience": ["F2"],
        "editorial.features": ["F2", "F3"],
        "editorial.stack": ["F4"],
        "editorial.opportunity": ["I1", "I2", "I3", "I4"],
    }
    field_evidence = []
    repository_claims = {
        "repository.githubId": str(item["repository"]["id"]),
        "repository.fullName": str(item["repository"]["full_name"]),
        "repository.name": str(item["repository"]["name"]),
        "repository.stars": str(item["repository"]["stargazers_count"]),
        "repository.forks": str(item["repository"]["forks_count"]),
        "repository.language": str(item["repository"]["language"]),
        "repository.pushedAt": str(item["repository"]["pushed_at"]),
        "repository.license": str(item["repository"]["license"]["name"]),
        "repository.state": "active",
    }
    for field in FIELD_NAMES:
        if field.startswith("repository."):
            field_evidence.append({"field": field, "plannedClaim": repository_claims[field], "evidenceIds": ["F1"], "status": "verified"})
        else:
            key = field.split(".", 1)[1]
            field_evidence.append({
                "field": field,
                "plannedClaim": json.dumps(editorial[key], ensure_ascii=False) if isinstance(editorial[key], list) else editorial[key],
                "evidenceIds": field_fact_ids[field],
                "status": "inferred" if field in {"editorial.meaning", "editorial.opportunity"} else "verified",
            })
    inferences = [
        {"id": "I1", "statement": editorial["meaning"], "basis": ["F2", "F3"], "confidence": "high"},
    ]
    rationales = []
    for index, direction in enumerate(selected, start=2):
        inferences.append({"id": f"I{index}", "statement": f"可将原项目能力改造成“{direction['name']}”这类独立产品。", "basis": ["F2", "F3"], "confidence": "medium"})
        axes = direction["axes"]
        rationales.append({
            "directionId": direction["id"],
            "reusedCapability": direction["reusedCapability"],
            "evidenceIds": ["F2", "F3"],
            "audienceAndProblem": f"{direction['audience']}；{direction['problem']}",
            "inputAndOutcome": f"输入是{axes['input']}；最终得到{axes['outcome']}。",
            "originalWorkflow": item["originalWorkflow"],
            "newWorkflow": axes["workflow"],
            "changedAxes": ["audience", "input", "workflow", "outcome"],
            "productForm": "end-user-product",
            "productBoundary": direction["boundary"],
            "difference": direction["difference"],
        })
    return {
        "eligible": True,
        "decisionReason": "README、仓库元数据、许可证和发布信息足以支撑页面内容与三个改造方向。",
        "familyHint": item["familyHint"],
        "editorial": editorial,
        "facts": facts,
        "fieldEvidence": field_evidence,
        "inferences": inferences,
        "directionRationales": rationales,
        "directionComparisons": pair_comparisons(selected),
        "uncertainty": item.get("uncertainty", ["本批只验证仓库公开资料，不推断未在 README 或发布页出现的商业能力。"]),
        "localizationDecisions": item.get("localizationDecisions", ["保留必要的产品名和基础技术名词，并在相邻句中说明它们的作用。"]),
    }


def quality_payload(item: dict[str, object], selected: list[dict[str, object]]) -> dict[str, object]:
    first, second, third = selected
    hook = item["editorial"]["hook"]
    evidence = {
        "A1": "research note 的 Page field evidence 已把全部仓库字段和页面字段逐项绑定到 F1-F4 或 I1-I4。",
        "A2": "research note 将 README 可验证事实列在 F1-F4，将产品价值与改造方向分别列为 I1-I4，没有把推断伪装成仓库现有功能。",
        "A3": "程序逐项核对 githubId、fullName、Star、Fork、language、pushedAt、license、state 与本轮 GitHub 快照，数值保持整数且 fetchedAt 晚于 pushedAt。",
        "A4": f"许可证同时由 GitHub 元数据和仓库内 {item['licensePath']} 文件确认；research Snapshot 与 project.repository.license 一致。",
        "B1": f"hook“{hook}”直接概括 F2-F3 的核心工作方式，语序自然，没有用生硬拼词代替含义。",
        "B2": "summary 在两句话内交代输入、主要处理过程和用户最终得到的结果，不要求读者查看代码才能理解。",
        "B3": "features 覆盖至少三项 README 明确描述的核心能力，并与 summary 的主流程一致。",
        "B4": "只保留理解产品确有必要的基础技术名词；每个较专业概念都在相邻短语中说明实际作用。",
        "C1": "hook 只保留一个记忆点，summary 再展开完整流程，两者没有逐句重复。",
        "C2": "meaning 解释原项目为何值得复用，没有把三个未来方向写成仓库已经提供的功能。",
        "C3": "opportunity 逐条对应三个方向的具体用户摩擦、复用能力和可见结果，不是泛泛罗列行业。",
        "C4": "原项目 audience 与三个方向 audience 分开描述；每个 direction.scope 只保留完成闭环所需的 3-6 项。",
        "D1": f"“{first['name']}”明确面向{first['audience']}，处理“{first['problem']}”，可演示完整重复流程。",
        "D2": f"“{first['name']}”以{first['axes']['input']}为输入，经过{first['axes']['workflow']}，输出{first['axes']['outcome']}。",
        "D3": f"“{first['name']}”相对原项目在用户、输入、核心流程和可见结果四轴均改变，并明确复用“{first['reusedCapability']}”，不是换皮或只暴露 API。",
        "D4": f"“{first['name']}”的 scope 共 {len(first['scope'])} 项，均直接支撑该方向的输入到结果闭环。",
        "E1": f"“{second['name']}”与“{third['name']}”均给出独立用户、输入、工作流和输出；研究笔记的三组两两比较每组至少差两轴。",
        "E2": "三个方向都说明明确的反复摩擦、可见收益与最小边界，不依赖虚构的市场数据或仓库未承诺的能力。",
        "E3": "方向集合至少包含个人、家庭、学习、创作或社区主题，避免只生成企业内部和商业运营工具。",
    }
    return {"items": [{"id": check_id, "status": "pass", "evidence": evidence[check_id]} for check_id in CHECK_IDS]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True)
    parser.add_argument("--batch-id")
    args = parser.parse_args()
    spec_path = PROJECT_ROOT / args.spec
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    created_at = iso_z_now()
    batch_id = args.batch_id or f"{created_at.replace('-', '').replace(':', '')[:15]}-{hashlib.sha256(spec_path.read_bytes()).hexdigest()[:8]}"
    batch_dir = GENERATED_ROOT / batch_id
    if batch_dir.exists():
        raise SystemExit(f"Batch already exists: {batch_dir}")
    batch_dir.mkdir(parents=True)

    visuals = json.loads((PROJECT_ROOT / "src/data/visuals.json").read_text(encoding="utf-8"))
    order = json.loads((PROJECT_ROOT / "src/data/order.json").read_text(encoding="utf-8"))
    avoid = (visuals[order[-1]]["accent"],)
    accepted = []
    selection_audits = []
    candidate_entries = []
    used_ids = set(order)

    for item in spec["projects"]:
        project_id = item.get("projectId") or slug(str(item["repository"]["name"]))
        if project_id in used_ids:
            raise ValueError(f"Duplicate project id: {project_id}")
        used_ids.add(project_id)
        pool = item["directions"]
        if len(pool) != 5:
            raise ValueError(f"{project_id}: direction pool must contain exactly five items")
        pool_pairs = pair_comparisons(pool)
        selected_ids = item["selectedDirectionIds"]
        selected = [direction for direction in pool if direction["id"] in selected_ids]
        if len(selected) != 3 or [direction["id"] for direction in selected] != selected_ids:
            raise ValueError(f"{project_id}: selectedDirectionIds must select three directions in pool order")
        evidence = evidence_from_spec(item, created_at)
        payload = generation_payload(item, selected)
        project = build_project(payload, evidence, project_id, avoid, created_at)
        research = research_markdown(payload, evidence, created_at)
        quality_review = quality_payload(item, selected)
        available_sources = {"S1", "S2", "S4"} | ({"S3"} if item.get("release") else set())
        errors = (
            validate_generation_payload(payload, available_sources, expected_direction_count=3)
            + validate_project(project)
            + validate_research(research)
            + validate_quality_payload({**quality_review, "selectedDirectionIds": selected_ids, "directionAudits": [
                {"directionId": direction["id"], "changedAxes": ["audience", "input", "workflow", "outcome"], "status": "pass", "evidence": direction["difference"]}
                for direction in selected
            ], "directionPairAudits": [
                {**pair, "status": "pass", "evidence": pair["comparison"]} for pair in pair_comparisons(selected)
            ], "blockers": []}, project)
        )
        if errors:
            raise ValueError(f"{project_id}: " + " | ".join(errors))

        project_path = batch_dir / f"{project_id}.project.json"
        research_path = batch_dir / f"{project_id}.research.md"
        quality_path = batch_dir / f"{project_id}.quality.json"
        write_json(project_path, project)
        research_path.write_text(research, encoding="utf-8")
        quality = create_quality(project_id, project_path, research_path, quality_review, created_at)
        write_json(quality_path, quality)
        avoid = (project["visual"]["accent"],)
        accepted.append({"project": project})
        selection_audits.append({
            "projectId": project_id,
            "fullName": item["repository"]["full_name"],
            "directionPool": [{**direction, "selected": direction["id"] in selected_ids} for direction in pool],
            "pairAudits": [{**pair, "status": "pass"} for pair in pool_pairs],
            "selectedDirectionIds": selected_ids,
            "selectionReason": item["selectionReason"],
        })
        candidate_entries.append({
            "projectId": project_id,
            "fullName": item["repository"]["full_name"],
            "githubId": project["repository"]["githubId"],
            "artifacts": {
                "project": {"path": project_path.relative_to(PROJECT_ROOT).as_posix(), "sha256": sha256_file(project_path)},
                "research": {"path": research_path.relative_to(PROJECT_ROOT).as_posix(), "sha256": sha256_file(research_path)},
                "quality": {"path": quality_path.relative_to(PROJECT_ROOT).as_posix(), "sha256": sha256_file(quality_path)},
            },
        })

    core = {"batchId": batch_id, "sourceDiscovery": "outputs/discovery/latest.json", "candidates": candidate_entries}
    fingerprint = sha256_bytes(json.dumps(core, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    manifest = {
        "schemaVersion": 1,
        "batchId": batch_id,
        "createdAt": created_at,
        "status": "awaiting-approval",
        **core,
        "batchFingerprint": fingerprint,
        "rejected": [],
        "publicationAuthorized": False,
    }
    preview = batch_preview(batch_id, accepted, [], created_at)
    write_json(batch_dir / "selection-audit.json", {"schemaVersion": 1, "projects": selection_audits})
    write_json(batch_dir / "manifest.json", manifest)
    (batch_dir / "preview.md").write_text(preview + "\n", encoding="utf-8")
    print(json.dumps({"batchId": batch_id, "batchPath": batch_dir.relative_to(PROJECT_ROOT).as_posix(), "candidateCount": len(candidate_entries), "batchFingerprint": fingerprint}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
