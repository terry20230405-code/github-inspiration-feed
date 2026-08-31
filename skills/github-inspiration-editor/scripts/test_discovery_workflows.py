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
        self.assertNotIn("publish_discovery_batch.py", workflow)
        self.assertNotIn("git add src/data", workflow)

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
