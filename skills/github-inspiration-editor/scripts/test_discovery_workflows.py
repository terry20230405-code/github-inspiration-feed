#!/usr/bin/env python3
"""Static safety-contract checks for automated discovery workflows."""

from __future__ import annotations

import json
import os
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch


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

    def test_discovery_preserves_artifacts_and_reports_technical_failure_after_pr(self) -> None:
        workflow = DISCOVERY_WORKFLOW.read_text(encoding="utf-8")
        capture_step = workflow.split("- name: AI 深读并生成候选批次", 1)[1].split("- name: 保存本轮发现审计报告", 1)[0]
        self.assertIn("set +e", capture_step)
        self.assertIn("draft_exit_code=$?", capture_step)
        self.assertIn('output.write(f"exit_code={exit_code}', capture_step)
        self.assertIn('GITHUB_STEP_SUMMARY\"]).open("a"', capture_step)
        upload_step = workflow.split("- name: 保存本轮发现审计报告", 1)[1].split("- name: 运行自动化测试", 1)[0]
        self.assertIn("if: always()", upload_step)
        self.assertIn("${{ steps.drafts.outputs.batch_path }}", upload_step)
        status_step = workflow.split("- name: 报告新项目发现状态", 1)[1].split("- name: 报告旧项目巡检状态", 1)[0]
        self.assertIn("if: always()", status_step)
        self.assertIn("exit 1", status_step)
        self.assertLess(workflow.index("- name: 创建候选审核分支"), workflow.index("- name: 报告新项目发现状态"))

    def test_discovery_summary_preserves_partial_success_and_handles_empty_report(self) -> None:
        workflow = DISCOVERY_WORKFLOW.read_text(encoding="utf-8")
        capture_step = workflow.split("- name: AI 深读并生成候选批次", 1)[1].split("- name: 保存本轮发现审计报告", 1)[0]
        source = textwrap.dedent(capture_step.split("python - <<'PY'\n", 1)[1].split("\n          PY", 1)[0])
        cases = [
            (json.dumps({"batchId": "test-batch", "batchPath": "outputs/generated/discovery-batches/test-batch",
                         "candidateCount": 1, "errorCount": 1, "preview": "partial batch preview"}), "1", "1", "1"),
            ("", "1", "0", "1"),
            (json.dumps({"batchId": "test-batch", "batchPath": "", "candidateCount": 0, "preview": "no candidates"}), "0", "0", "0"),
        ]
        for raw, process_exit, expected_candidates, expected_exit in cases:
            with self.subTest(raw=raw), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                (root / "outputs/discovery").mkdir(parents=True)
                (root / "outputs/discovery/draft-result.json").write_text(raw, encoding="utf-8")
                summary = root / "summary.md"
                summary.write_text("old repository summary\n", encoding="utf-8")
                output = root / "github-output.txt"
                with patch.dict(os.environ, {"DRAFT_EXIT_CODE": process_exit, "GITHUB_OUTPUT": str(output),
                                             "GITHUB_STEP_SUMMARY": str(summary)}):
                    # Bind only this snippet's relative filesystem paths to the isolated test directory.
                    source_for_test = source.replace("from pathlib import Path", "")
                    exec(compile(source_for_test, "workflow-summary", "exec"), {"Path": lambda path: root / path})
                fields = dict(line.split("=", 1) for line in output.read_text(encoding="utf-8").splitlines())
                self.assertEqual(fields["candidate_count"], expected_candidates)
                self.assertEqual(fields["exit_code"], expected_exit)
                self.assertTrue(summary.read_text(encoding="utf-8").startswith("old repository summary\n"))
                self.assertIsInstance(json.loads((root / "outputs/discovery/draft-result.json").read_text(encoding="utf-8")), dict)

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
