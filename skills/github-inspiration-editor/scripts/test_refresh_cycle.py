#!/usr/bin/env python3
"""Tests for the phase-eight refresh-cycle orchestrator."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Sequence

from run_refresh_cycle import CommandResult, create_lock, npm_command, preflight_commands, run_cycle


def stage_six_report(*, review: int = 0, failed: int = 0, research: int = 0) -> dict[str, object]:
    return {
        "schemaVersion": 1,
        "summary": {
            "checked": 1,
            "updated": 0,
            "refreshed": 1,
            "reviewRequired": review,
            "failed": failed,
            "researchRefreshRecommended": research,
            "contentReviewRecommended": 0,
        },
        "repositories": [],
    }


def stage_seven_report(*, pending: int = 0, drafts: int = 0, human: int = 0, failed: int = 0) -> dict[str, object]:
    return {
        "schemaVersion": 1,
        "summary": {
            "checked": 1,
            "updated": 0,
            "refreshed": 1,
            "semanticReviewPending": pending,
            "contentDraftRequired": drafts,
            "humanDecisionRequired": human,
            "failed": failed,
        },
        "repositories": [],
    }


class FakeRunner:
    def __init__(
        self,
        *,
        stage_six: dict[str, object] | None = None,
        stage_seven: dict[str, object] | None = None,
        stage_six_exit: int = 0,
        stage_seven_exit: int = 0,
    ) -> None:
        self.stage_six = stage_six or stage_six_report()
        self.stage_seven = stage_seven or stage_seven_report()
        self.stage_six_exit = stage_six_exit
        self.stage_seven_exit = stage_seven_exit
        self.commands: list[list[str]] = []

    def __call__(self, command: Sequence[str], _cwd: Path) -> CommandResult:
        values = list(command)
        self.commands.append(values)
        report_index = values.index("--report") + 1 if "--report" in values else None
        if "refresh_repositories.py" in values[1]:
            if report_index is not None and self.stage_six_exit in {0, 2}:
                path = Path(values[report_index])
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(self.stage_six), encoding="utf-8")
            return CommandResult(self.stage_six_exit)
        if "refresh_research_sources.py" in values[1]:
            if report_index is not None and self.stage_seven_exit in {0, 2}:
                path = Path(values[report_index])
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(self.stage_seven), encoding="utf-8")
            return CommandResult(self.stage_seven_exit)
        return CommandResult(0)


class MutatingRunner(FakeRunner):
    def __init__(self, root: Path, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.root = root

    def __call__(self, command: Sequence[str], cwd: Path) -> CommandResult:
        values = list(command)
        if len(values) > 1 and "refresh_repositories.py" in values[1] and "--write" in values:
            path = self.root / "src/data/repositories.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps({"alpha": {"stars": 99}}), encoding="utf-8")
        return super().__call__(command, cwd)


class RefreshCycleTests(unittest.TestCase):
    def run_with(self, root: Path, mode: str, runner: FakeRunner) -> tuple[dict[str, object], int]:
        moments = iter(["2026-08-27T00:00:00Z", "2026-08-27T00:00:01Z"])
        return run_cycle(
            project_root=root,
            mode=mode,
            runner=runner,
            python="python",
            run_validations_enabled=False,
            now=lambda: next(moments),
        )

    def test_check_mode_never_uses_write_flags(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            runner = FakeRunner(
                stage_six=stage_six_report(research=1),
                stage_seven=stage_seven_report(pending=1),
            )
            report, exit_code = self.run_with(Path(directory), "check", runner)
        self.assertEqual(exit_code, 0)
        self.assertEqual(report["status"], "check-completed")
        self.assertEqual(report["nextActor"], "none")
        self.assertFalse(any("--write" in command for command in runner.commands))

    def test_write_mode_stops_for_ai_semantic_review_without_authorizing_publication(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            runner = FakeRunner(
                stage_six=stage_six_report(research=1),
                stage_seven=stage_seven_report(pending=1),
            )
            report, exit_code = self.run_with(Path(directory), "write", runner)
        self.assertEqual(exit_code, 0)
        self.assertEqual(report["status"], "ai-review-required")
        self.assertEqual(report["nextActor"], "ai")
        self.assertFalse(report["publicationAuthorized"])
        self.assertEqual(report["versioning"]["outcome"], "committed")
        self.assertEqual(sum("--write" in command for command in runner.commands), 2)

    def test_stage_six_critical_change_stops_before_any_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            runner = FakeRunner(stage_six=stage_six_report(review=1), stage_six_exit=2)
            report, exit_code = self.run_with(Path(directory), "write", runner)
        self.assertEqual(exit_code, 2)
        self.assertEqual(report["status"], "human-decision-required")
        self.assertEqual(len(runner.commands), 1)
        self.assertNotIn("--write", runner.commands[0])

    def test_stage_seven_critical_change_stops_before_source_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repository_path = root / "src/data/repositories.json"
            repository_path.parent.mkdir(parents=True)
            repository_path.write_text(json.dumps({"alpha": {"stars": 10}}), encoding="utf-8")
            runner = MutatingRunner(
                root,
                stage_six=stage_six_report(research=1),
                stage_seven=stage_seven_report(human=1),
                stage_seven_exit=2,
            )
            report, exit_code = self.run_with(root, "write", runner)
            restored = json.loads(repository_path.read_text(encoding="utf-8"))
        self.assertEqual(exit_code, 2)
        self.assertEqual(report["status"], "human-decision-required")
        self.assertEqual(report["versioning"]["outcome"], "rolled-back")
        self.assertEqual(restored["alpha"]["stars"], 10)
        research_commands = [command for command in runner.commands if "refresh_research_sources.py" in command[1]]
        self.assertEqual(len(research_commands), 1)
        self.assertNotIn("--write", research_commands[0])

    def test_resume_recognizes_content_draft_required(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report_path = root / "outputs/refresh/latest.json"
            report_path.parent.mkdir(parents=True)
            report_path.write_text(json.dumps(stage_six_report(research=1)), encoding="utf-8")
            runner = FakeRunner(stage_seven=stage_seven_report(drafts=1))
            report, exit_code = self.run_with(root, "resume", runner)
        self.assertEqual(exit_code, 0)
        self.assertEqual(report["status"], "content-draft-required")
        self.assertEqual(report["nextActor"], "ai")
        self.assertEqual(len(runner.commands), 1)
        self.assertIn("--write", runner.commands[0])

    def test_technical_failure_has_clear_failed_status(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            runner = FakeRunner(stage_six_exit=1)
            report, exit_code = self.run_with(Path(directory), "write", runner)
        self.assertEqual(exit_code, 1)
        self.assertEqual(report["status"], "failed")
        self.assertEqual(report["nextActor"], "ai")
        self.assertIn("stage-six-dry-run", str(report["nextAction"]))

    def test_lock_prevents_overlapping_cycles(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            lock = Path(directory) / "refresh.lock"
            create_lock(lock, "first", "2026-08-27T00:00:00Z")
            with self.assertRaisesRegex(RuntimeError, "another refresh cycle"):
                create_lock(lock, "second", "2026-08-27T00:01:00Z")

    def test_preflight_uses_the_resolved_npm_executable(self) -> None:
        commands = preflight_commands("python", npm="C:/tools/npm.cmd")
        npm_commands = [command for _, command in commands if len(command) > 1 and command[1] == "run"]
        self.assertTrue(npm_commands)
        self.assertTrue(all(command[0] == "C:/tools/npm.cmd" for command in npm_commands))
        self.assertTrue(npm_command())


if __name__ == "__main__":
    unittest.main()
