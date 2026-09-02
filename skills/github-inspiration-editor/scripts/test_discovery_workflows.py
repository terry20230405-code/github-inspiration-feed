#!/usr/bin/env python3
"""Static safety-contract checks for automated discovery workflows."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DISCOVERY_WORKFLOW = PROJECT_ROOT / ".github/workflows/discover-projects.yml"
PUBLICATION_WORKFLOW = PROJECT_ROOT / ".github/workflows/publish-discovery-batch.yml"


class DiscoveryWorkflowContractTests(unittest.TestCase):
    def test_ci_dependencies_are_cross_platform(self) -> None:
        package = json.loads((PROJECT_ROOT / "package.json").read_text(encoding="utf-8"))
        identity_test = (PROJECT_ROOT / "scripts/test-project-identity.mjs").read_text(encoding="utf-8")
        required = {
            **package.get("dependencies", {}),
            **package.get("devDependencies", {}),
        }
        self.assertNotIn("@rolldown/binding-win32-x64-msvc", required)
        self.assertNotIn("lightningcss-win32-x64-msvc", required)
        self.assertEqual(
            package.get("optionalDependencies", {}).get("@terry/selector-dev"),
            "file:../plugins/selector-dev",
        )
        self.assertIn("configFile: false", identity_test)

    def test_discovery_only_creates_review_batch(self) -> None:
        workflow = DISCOVERY_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn('cron: "0 9 * * 2,5"', workflow)
        self.assertIn('timezone: "Asia/Shanghai"', workflow)
        self.assertIn("OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}", workflow)
        self.assertIn("AI_API_BASE_URL: ${{ vars.AI_API_BASE_URL }}", workflow)
        self.assertIn("AI_MODEL: ${{ vars.AI_MODEL }}", workflow)
        self.assertIn("pull-requests: write", workflow)
        self.assertIn("gh pr create", workflow)
        self.assertIn("if: steps.drafts.outputs.candidate_count != '0'", workflow)
        self.assertIn("uses: actions/upload-artifact@v7", workflow)
        self.assertIn("name: discovery-audit-${{ github.run_id }}", workflow)
        self.assertIn("outputs/discovery/draft-result.json", workflow)
        self.assertIn("retention-days: 30", workflow)
        self.assertNotIn("publish_discovery_batch.py", workflow)
        self.assertNotIn("src/data/editorial.json", workflow)
        self.assertNotIn("src/data/visuals.json", workflow)
        self.assertNotIn("src/data/order.json", workflow)

    def test_discovery_safely_refreshes_published_repository_snapshots(self) -> None:
        discovery = DISCOVERY_WORKFLOW.read_text(encoding="utf-8")
        publication = PUBLICATION_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("run_refresh_cycle.py --write", discovery)
        self.assertIn("id: published_refresh", discovery)
        self.assertIn("src/data/repositories.json", discovery)
        self.assertIn("outputs/refresh", discovery)
        self.assertIn("outputs/versions/snapshots", discovery)
        self.assertIn("name: published-refresh-audit-${{ github.run_id }}", discovery)
        self.assertIn("if: steps.published_refresh.outputs.exit_code == '0'", discovery)
        self.assertIn("REFRESH_EXIT_CODE: ${{ steps.published_refresh.outputs.exit_code }}", discovery)
        refresh_status_step = discovery.split("- name: 报告旧项目巡检状态", 1)[1]
        self.assertIn("::warning title=旧项目巡检需要人工确认::", refresh_status_step)
        self.assertIn("新项目发现结果和候选 PR 保持有效", refresh_status_step)
        review_required_branch = refresh_status_step.split("2)", 1)[1].split(";;", 1)[0]
        self.assertNotIn("exit 2", review_required_branch)
        technical_failure_branch = refresh_status_step.split("*)", 1)[1]
        self.assertIn("exit 1", technical_failure_branch)
        self.assertIn("group: github-inspiration-main-writes", discovery)
        self.assertIn("group: github-inspiration-main-writes", publication)

        commit_step = discovery.split("- name: 提交安全的旧项目刷新结果", 1)[1].split(
            "- name: 搜索并筛选 GitHub 仓库", 1
        )[0]
        self.assertIn("outputs/refresh", commit_step)
        self.assertIn("outputs/generated/research-refresh", commit_step)
        self.assertNotIn("outputs/automation", commit_step)
        self.assertNotIn("outputs/versions", commit_step)

    def test_publication_requires_merged_discovery_pr(self) -> None:
        workflow = PUBLICATION_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("github.event.pull_request.merged == true", workflow)
        self.assertIn("startsWith(github.event.pull_request.head.ref, 'automation/discovery-')", workflow)
        self.assertIn("publish_discovery_batch.py", workflow)
        self.assertIn('--approved-by "$APPROVED_BY"', workflow)
        self.assertIn('--source-pr "$SOURCE_PR"', workflow)
        self.assertIn("git add src/data outputs/generated/discovery-batches", workflow)


if __name__ == "__main__":
    unittest.main(verbosity=2)
