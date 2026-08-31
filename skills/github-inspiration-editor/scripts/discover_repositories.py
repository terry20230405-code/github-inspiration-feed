#!/usr/bin/env python3
"""Discover and rank public GitHub repositories for the inspiration feed."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable

try:
    import certifi
except ImportError:  # pragma: no cover - system certificate store is the fallback
    certifi = None


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG = PROJECT_ROOT / "config/discovery.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "outputs/discovery/latest.json"
DEFAULT_REPORT = PROJECT_ROOT / "outputs/discovery/latest.md"
GITHUB_API = "https://api.github.com"
USER_AGENT = "github-inspiration-feed-discovery/1.0"
FULL_NAME = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where() if certifi else None)


class DiscoveryError(RuntimeError):
    """Raised when discovery cannot produce a trustworthy result."""


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def iso_z(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise DiscoveryError(f"Could not read {path}: {error}") from error


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_config(value: object) -> dict[str, object]:
    if not isinstance(value, dict) or value.get("schemaVersion") != 2:
        raise DiscoveryError("config/discovery.json must use schemaVersion 2")
    integer_fields = {
        "maxSearchResultsPerQuery": (1, 100),
        "shortlistSize": (1, 200),
        "aiAnalysisLimit": (1, 50),
        "maxCandidatesPerRun": (1, 20),
        "activeWithinDays": (30, 1825),
        "minimumStars": (0, 1_000_000),
        "minimumReadmeCharacters": (100, 100_000),
    }
    for field, (minimum, maximum) in integer_fields.items():
        item = value.get(field)
        if not isinstance(item, int) or isinstance(item, bool) or not minimum <= item <= maximum:
            raise DiscoveryError(f"{field} must be an integer between {minimum} and {maximum}")
    if int(value["maxCandidatesPerRun"]) > int(value["aiAnalysisLimit"]):
        raise DiscoveryError("maxCandidatesPerRun cannot exceed aiAnalysisLimit")
    lanes = value.get("searchLanes")
    if not isinstance(lanes, list) or not lanes:
        raise DiscoveryError("searchLanes must be a non-empty array")
    lane_ids: set[str] = set()
    for lane in lanes:
        if not isinstance(lane, dict) or set(lane) != {"id", "label", "familyHint", "query"}:
            raise DiscoveryError("each search lane must contain id, label, familyHint, and query")
        lane_id = lane.get("id")
        if not isinstance(lane_id, str) or not lane_id or lane_id in lane_ids:
            raise DiscoveryError("search lane IDs must be unique non-empty strings")
        lane_ids.add(lane_id)
        if lane.get("familyHint") not in {"video", "design", "photo", "automation", "data", "ai", "general"}:
            raise DiscoveryError(f"search lane {lane_id} has an invalid familyHint")
        if not isinstance(lane.get("query"), str) or not lane["query"].strip():
            raise DiscoveryError(f"search lane {lane_id} needs a query")
    provider = value.get("aiProvider")
    required_provider_fields = {"protocol", "baseUrl", "model", "reasoningEffort", "maxCompletionTokens"}
    if not isinstance(provider, dict) or set(provider) != required_provider_fields:
        raise DiscoveryError(f"aiProvider must contain exactly: {', '.join(sorted(required_provider_fields))}")
    if provider.get("protocol") != "openai-chat-completions":
        raise DiscoveryError("aiProvider.protocol must be openai-chat-completions")
    parsed_base_url = urllib.parse.urlsplit(str(provider.get("baseUrl") or ""))
    if (
        parsed_base_url.scheme != "https"
        or not parsed_base_url.hostname
        or parsed_base_url.username is not None
        or parsed_base_url.password is not None
        or parsed_base_url.query
        or parsed_base_url.fragment
    ):
        raise DiscoveryError("aiProvider.baseUrl must be a plain HTTPS URL without credentials, query, or fragment")
    provider["baseUrl"] = str(provider["baseUrl"]).rstrip("/")
    if not provider["baseUrl"]:
        raise DiscoveryError("aiProvider.baseUrl must not be empty")
    if urllib.parse.urlsplit(str(provider["baseUrl"])).path.rstrip("/").endswith("/chat/completions"):
        raise DiscoveryError("aiProvider.baseUrl must stop at the API base path, not include /chat/completions")
    for field in ("model", "reasoningEffort"):
        if not isinstance(provider.get(field), str) or not str(provider[field]).strip():
            raise DiscoveryError(f"aiProvider.{field} must be a non-empty string")
    if provider["reasoningEffort"] not in {"minimal", "low", "medium", "high", "xhigh"}:
        raise DiscoveryError("aiProvider.reasoningEffort must be minimal, low, medium, high, or xhigh")
    max_completion_tokens = provider.get("maxCompletionTokens")
    if not isinstance(max_completion_tokens, int) or isinstance(max_completion_tokens, bool) or not 512 <= max_completion_tokens <= 100_000:
        raise DiscoveryError("aiProvider.maxCompletionTokens must be an integer between 512 and 100000")
    for field in ("excludedTopics", "excludedNameFragments"):
        items = value.get(field)
        if not isinstance(items, list) or not all(isinstance(item, str) and item for item in items):
            raise DiscoveryError(f"{field} must be an array of non-empty strings")
    return value


def apply_environment_overrides(config: dict[str, object]) -> dict[str, object]:
    updated = dict(config)
    overrides = {
        "DISCOVERY_AI_ANALYSIS_LIMIT": ("aiAnalysisLimit", 1, 50),
        "DISCOVERY_MAX_CANDIDATES": ("maxCandidatesPerRun", 1, 20),
    }
    for environment_name, (field, minimum, maximum) in overrides.items():
        raw = os.environ.get(environment_name)
        if raw in {None, ""}:
            continue
        try:
            value = int(raw)
        except ValueError as error:
            raise DiscoveryError(f"{environment_name} must be an integer") from error
        if not minimum <= value <= maximum:
            raise DiscoveryError(f"{environment_name} must be between {minimum} and {maximum}")
        updated[field] = value
    provider = updated.get("aiProvider")
    if isinstance(provider, dict):
        provider = dict(provider)
        base_url = os.environ.get("AI_API_BASE_URL")
        model = os.environ.get("AI_MODEL")
        if base_url:
            provider["baseUrl"] = base_url
        if model:
            provider["model"] = model
        updated["aiProvider"] = provider
    return validate_config(updated)


def github_request_json(url: str, token: str | None, *, attempts: int = 3) -> object:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    for attempt in range(attempts):
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=30, context=SSL_CONTEXT) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            if error.code in {403, 429} and attempt + 1 < attempts:
                retry_after = error.headers.get("Retry-After")
                wait_seconds = int(retry_after) if retry_after and retry_after.isdigit() else 2 ** attempt
                time.sleep(min(wait_seconds, 30))
                continue
            detail = error.read().decode("utf-8", errors="replace")[:500]
            raise DiscoveryError(f"GitHub request failed ({error.code}): {detail}") from error
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
            if attempt + 1 < attempts:
                time.sleep(2 ** attempt)
                continue
            raise DiscoveryError(f"GitHub request failed: {error}") from error
    raise DiscoveryError("GitHub request failed after retries")


def published_repositories(project_root: Path) -> tuple[set[int], set[str]]:
    value = read_json(project_root / "src/data/repositories.json")
    if not isinstance(value, dict):
        raise DiscoveryError("src/data/repositories.json must be an object")
    ids: set[int] = set()
    names: set[str] = set()
    for item in value.values():
        if not isinstance(item, dict):
            continue
        github_id = item.get("githubId")
        full_name = item.get("fullName")
        if isinstance(github_id, int):
            ids.add(github_id)
        if isinstance(full_name, str):
            names.add(full_name.lower())
    return ids, names


def generated_repositories(project_root: Path) -> tuple[set[int], set[str]]:
    ids: set[int] = set()
    names: set[str] = set()
    root = project_root / "outputs/generated"
    if not root.exists():
        return ids, names
    for path in root.rglob("*.project.json"):
        if "published-baseline" in path.parts:
            continue
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        repository = value.get("repository") if isinstance(value, dict) else None
        if not isinstance(repository, dict):
            continue
        github_id = repository.get("githubId")
        full_name = repository.get("fullName")
        if isinstance(github_id, int):
            ids.add(github_id)
        if isinstance(full_name, str):
            names.add(full_name.lower())
    return ids, names


def parse_time(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def exclusion_reason(item: dict[str, object], config: dict[str, object], cutoff: datetime, known_ids: set[int], known_names: set[str]) -> str | None:
    github_id = item.get("id")
    full_name = item.get("full_name")
    if not isinstance(github_id, int) or not isinstance(full_name, str) or not FULL_NAME.fullmatch(full_name):
        return "invalid-identity"
    if github_id in known_ids or full_name.lower() in known_names:
        return "already-known"
    if item.get("private") is True or item.get("visibility") not in {None, "public"}:
        return "not-public"
    if item.get("fork") is True:
        return "fork"
    if item.get("archived") is True:
        return "archived"
    if item.get("disabled") is True:
        return "disabled"
    if item.get("mirror_url"):
        return "mirror"
    if item.get("is_template") is True:
        return "template"
    stars = item.get("stargazers_count")
    if not isinstance(stars, int) or stars < int(config["minimumStars"]):
        return "too-few-stars"
    pushed_at = parse_time(item.get("pushed_at"))
    if pushed_at is None or pushed_at < cutoff:
        return "inactive"
    name = full_name.lower()
    if any(str(fragment).lower() in name for fragment in config["excludedNameFragments"]):
        return "excluded-name"
    topics = {str(topic).lower() for topic in item.get("topics", []) if isinstance(topic, str)} if isinstance(item.get("topics"), list) else set()
    if topics.intersection(str(topic).lower() for topic in config["excludedTopics"]):
        return "excluded-topic"
    if not isinstance(item.get("description"), str) or len(str(item["description"]).strip()) < 20:
        return "missing-description"
    if not isinstance(item.get("license"), dict) or not item["license"].get("spdx_id"):
        return "missing-license"
    return None


def candidate_score(item: dict[str, object], now: datetime, lane_count: int) -> tuple[float, list[str], str]:
    stars = int(item.get("stargazers_count", 0))
    forks = int(item.get("forks_count", 0))
    topics = item.get("topics") if isinstance(item.get("topics"), list) else []
    pushed_at = parse_time(item.get("pushed_at")) or now - timedelta(days=3650)
    created_at = parse_time(item.get("created_at")) or now - timedelta(days=3650)
    age_days = max(0, (now - created_at).days)
    inactive_days = max(0, (now - pushed_at).days)
    maturity = "new" if age_days <= 180 and stars < 5000 else "growing" if stars < 5000 else "established"
    score = min(30.0, math.log10(max(stars, 1)) * 8.0)
    score += max(0.0, 28.0 - inactive_days / 10.0)
    score += min(10.0, len(topics) * 1.5)
    score += min(8.0, math.log10(max(forks, 1)) * 2.5)
    score += min(8.0, lane_count * 3.0)
    if maturity == "new" and stars >= 100:
        score += 8.0
    reasons = [
        f"{stars:,} Star，属于{ {'new': '新锐', 'growing': '成长', 'established': '成熟'}[maturity] }项目池",
        f"最近 {inactive_days} 天内有代码推送",
        f"命中 {lane_count} 条搜索路线",
    ]
    return round(score, 2), reasons, maturity


def normalize_candidate(item: dict[str, object], matches: list[dict[str, str]], now: datetime) -> dict[str, object]:
    score, reasons, maturity = candidate_score(item, now, len(matches))
    license_value = item.get("license")
    assert isinstance(license_value, dict)
    return {
        "githubId": item["id"],
        "fullName": item["full_name"],
        "url": item.get("html_url") or f"https://github.com/{item['full_name']}",
        "name": item.get("name") or str(item["full_name"]).split("/", 1)[1],
        "description": item["description"],
        "stars": item["stargazers_count"],
        "forks": item.get("forks_count", 0),
        "language": item.get("language") or "未知",
        "pushedAt": item["pushed_at"],
        "createdAt": item.get("created_at"),
        "license": license_value.get("name") or license_value.get("spdx_id"),
        "defaultBranch": item.get("default_branch") or "main",
        "topics": sorted({str(topic) for topic in item.get("topics", [])}) if isinstance(item.get("topics"), list) else [],
        "openIssues": item.get("open_issues_count", 0),
        "maturity": maturity,
        "score": score,
        "reasons": reasons,
        "matchedLanes": matches,
        "suggestedFamilyHint": matches[0]["familyHint"],
    }


def choose_diverse(candidates: list[dict[str, object]], limit: int) -> list[dict[str, object]]:
    by_lane: dict[str, list[dict[str, object]]] = defaultdict(list)
    for candidate in candidates:
        matches = candidate.get("matchedLanes")
        lane_id = str(matches[0]["id"]) if isinstance(matches, list) and matches else "other"
        by_lane[lane_id].append(candidate)
    for items in by_lane.values():
        items.sort(key=lambda item: (-float(item["score"]), str(item["fullName"]).lower()))
    lane_order = sorted(by_lane, key=lambda lane: (-float(by_lane[lane][0]["score"]), lane))
    selected: list[dict[str, object]] = []
    while len(selected) < limit:
        progressed = False
        for lane in lane_order:
            if by_lane[lane] and len(selected) < limit:
                selected.append(by_lane[lane].pop(0))
                progressed = True
        if not progressed:
            break
    return selected


def discover(config: dict[str, object], request_json: Callable[[str, str | None], object], token: str | None, *, now: datetime | None = None, project_root: Path = PROJECT_ROOT) -> dict[str, object]:
    current_time = now or utc_now()
    cutoff = current_time - timedelta(days=int(config["activeWithinDays"]))
    published_ids, published_names = published_repositories(project_root)
    generated_ids, generated_names = generated_repositories(project_root)
    known_ids = published_ids | generated_ids
    known_names = published_names | generated_names
    raw_by_id: dict[int, dict[str, object]] = {}
    matches_by_id: dict[int, list[dict[str, str]]] = defaultdict(list)
    excluded: dict[str, int] = defaultdict(int)
    query_summaries: list[dict[str, object]] = []

    configured_lanes = config["searchLanes"]
    assert isinstance(configured_lanes, list)
    search_lanes = configured_lanes if token or len(configured_lanes) <= 5 else configured_lanes[:5]

    for lane_value in search_lanes:
        assert isinstance(lane_value, dict)
        lane = {key: str(lane_value[key]) for key in ("id", "label", "familyHint", "query")}
        qualifiers = (
            f"{lane['query']} is:public archived:false mirror:false template:false "
            f"stars:>={config['minimumStars']} pushed:>={cutoff.date().isoformat()}"
        )
        params = urllib.parse.urlencode({
            "q": qualifiers,
            "sort": "updated",
            "order": "desc",
            "per_page": int(config["maxSearchResultsPerQuery"]),
        })
        payload = request_json(f"{GITHUB_API}/search/repositories?{params}", token)
        if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
            raise DiscoveryError(f"GitHub search returned an invalid payload for lane {lane['id']}")
        accepted = 0
        for raw_item in payload["items"]:
            if not isinstance(raw_item, dict):
                excluded["invalid-item"] += 1
                continue
            item = dict(raw_item)
            reason = exclusion_reason(item, config, cutoff, known_ids, known_names)
            if reason:
                excluded[reason] += 1
                continue
            github_id = item["id"]
            assert isinstance(github_id, int)
            raw_by_id[github_id] = item
            if lane["id"] not in {match["id"] for match in matches_by_id[github_id]}:
                matches_by_id[github_id].append(lane)
            accepted += 1
        query_summaries.append({"laneId": lane["id"], "label": lane["label"], "received": len(payload["items"]), "acceptedBeforeDedupe": accepted})

    candidates = [normalize_candidate(item, matches_by_id[github_id], current_time) for github_id, item in raw_by_id.items()]
    candidates.sort(key=lambda item: (-float(item["score"]), str(item["fullName"]).lower()))
    shortlist = choose_diverse(candidates, int(config["shortlistSize"]))
    ai_queue = shortlist[: int(config["aiAnalysisLimit"])]
    policy_hash = hashlib.sha256(json.dumps(config, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    return {
        "schemaVersion": 1,
        "generatedAt": iso_z(current_time),
        "policySha256": policy_hash,
        "authentication": "authenticated" if token else "unauthenticated-limited",
        "searchedLaneCount": len(search_lanes),
        "configuredLaneCount": len(configured_lanes),
        "limits": {
            "shortlistSize": config["shortlistSize"],
            "aiAnalysisLimit": config["aiAnalysisLimit"],
            "maxCandidatesPerRun": config["maxCandidatesPerRun"],
        },
        "counts": {
            "uniqueEligible": len(candidates),
            "shortlisted": len(shortlist),
            "queuedForAI": len(ai_queue),
        },
        "excluded": dict(sorted(excluded.items())),
        "queries": query_summaries,
        "aiQueue": ai_queue,
        "shortlist": shortlist,
        "publicationAuthorized": False,
    }


def report_markdown(result: dict[str, object]) -> str:
    counts = result["counts"]
    limits = result["limits"]
    assert isinstance(counts, dict) and isinstance(limits, dict)
    lines = [
        "# GitHub 自动发现报告",
        "",
        f"- 生成时间：{result['generatedAt']}",
        f"- 搜索路线：{result['searchedLaneCount']} / {result['configuredLaneCount']}",
        f"- API 模式：{result['authentication']}",
        f"- 可用仓库：{counts['uniqueEligible']}",
        f"- 初选仓库：{counts['shortlisted']}",
        f"- 等待 AI 深读：{counts['queuedForAI']}",
        f"- 本轮最多生成候选：{limits['maxCandidatesPerRun']}",
        "- 发布授权：否",
        "",
        "## AI 深读队列",
        "",
    ]
    for index, candidate in enumerate(result["aiQueue"], start=1):
        assert isinstance(candidate, dict)
        matches = candidate.get("matchedLanes")
        label = matches[0]["label"] if isinstance(matches, list) and matches else "未分类"
        lines.extend([
            f"### {index}. {candidate['fullName']}",
            "",
            f"- 搜索方向：{label}",
            f"- 评分：{candidate['score']}",
            f"- Star：{candidate['stars']}",
            f"- 语言：{candidate['language']}",
            f"- 简介：{candidate['description']}",
            "",
        ])
    if not result["aiQueue"]:
        lines.extend(["本轮没有找到符合硬性条件的新仓库。", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(DEFAULT_CONFIG.relative_to(PROJECT_ROOT)))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT.relative_to(PROJECT_ROOT)))
    parser.add_argument("--report", default=str(DEFAULT_REPORT.relative_to(PROJECT_ROOT)))
    parser.add_argument("--lane-limit", type=int, help="Temporarily use only the first N configured search lanes")
    parser.add_argument("--write", action="store_true", help="Write JSON and Markdown discovery reports")
    args = parser.parse_args()
    try:
        config = apply_environment_overrides(validate_config(read_json(PROJECT_ROOT / args.config)))
        if args.lane_limit is not None:
            if not 1 <= args.lane_limit <= len(config["searchLanes"]):
                raise DiscoveryError("--lane-limit must be between 1 and the configured lane count")
            config = {**config, "searchLanes": list(config["searchLanes"])[:args.lane_limit]}
        result = discover(config, github_request_json, os.environ.get("GITHUB_TOKEN"))
        if args.write:
            write_json(PROJECT_ROOT / args.output, result)
            report_path = PROJECT_ROOT / args.report
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_text(report_markdown(result), encoding="utf-8")
        print(json.dumps({
            "mode": "write" if args.write else "dry-run",
            "generatedAt": result["generatedAt"],
            "authentication": result["authentication"],
            "searchedLaneCount": result["searchedLaneCount"],
            "counts": result["counts"],
            "output": args.output if args.write else None,
            "report": args.report if args.write else None,
            "publicationAuthorized": False,
        }, ensure_ascii=False, indent=2))
        return 0
    except DiscoveryError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
