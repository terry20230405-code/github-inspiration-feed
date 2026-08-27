#!/usr/bin/env python3
"""Orchestrate the safe, deterministic parts of the repository refresh cycle."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Sequence

from manage_versions import create_snapshot, restore_snapshot, write_transaction


SCHEMA_VERSION = 1
OUTPUT_LIMIT = 4_000


@dataclass(frozen=True)
class CommandResult:
    returncode: int
    stdout: str = ""
    stderr: str = ""


CommandRunner = Callable[[Sequence[str], Path], CommandResult]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def read_json_object(path: Path, label: str) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"{label} could not be read: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def default_runner(command: Sequence[str], cwd: Path) -> CommandResult:
    completed = subprocess.run(
        list(command),
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    return CommandResult(completed.returncode, completed.stdout, completed.stderr)


def clipped(value: str) -> str:
    if len(value) <= OUTPUT_LIMIT:
        return value
    return "..." + value[-OUTPUT_LIMIT:]


def command_record(name: str, command: Sequence[str], result: CommandResult) -> dict[str, object]:
    return {
        "name": name,
        "command": list(command),
        "exitCode": result.returncode,
        "stdoutTail": clipped(result.stdout),
        "stderrTail": clipped(result.stderr),
    }


def report_summary(report: dict[str, object], label: str) -> dict[str, object]:
    summary = report.get("summary")
    if report.get("schemaVersion") != 1 or not isinstance(summary, dict):
        raise ValueError(f"{label} has an unsupported shape")
    return summary


def integer_count(summary: dict[str, object], field: str, label: str) -> int:
    value = summary.get(field)
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{label}.{field} must be a non-negative integer")
    return value


def status_from_research_report(report: dict[str, object]) -> tuple[str, str, str]:
    summary = report_summary(report, "stage-seven report")
    failed = integer_count(summary, "failed", "stage-seven summary")
    human = integer_count(summary, "humanDecisionRequired", "stage-seven summary")
    pending = integer_count(summary, "semanticReviewPending", "stage-seven summary")
    drafts = integer_count(summary, "contentDraftRequired", "stage-seven summary")
    if failed:
        return "failed", "ai", "Fix the technical failure, then rerun this cycle."
    if human:
        return "human-decision-required", "human", "Review the critical repository change before continuing."
    if pending:
        return "ai-review-required", "ai", "Create fingerprint-matched semantic reviews, validate them, then run the resume command."
    if drafts:
        return "content-draft-required", "ai", "Generate and quality-check draft artifacts under outputs/generated; do not publish them."
    return "completed", "none", "No further action is required for this cycle."


def create_lock(lock_path: Path, run_id: str, started_at: str) -> None:
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps({"runId": run_id, "startedAt": started_at, "pid": os.getpid()}, ensure_ascii=False)
    try:
        descriptor = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as error:
        try:
            current = lock_path.read_text(encoding="utf-8").strip()
        except OSError:
            current = "unreadable lock"
        raise RuntimeError(f"another refresh cycle is active: {current}") from error
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        handle.write(payload + "\n")


def run_step(
    *,
    name: str,
    command: Sequence[str],
    project_root: Path,
    runner: CommandRunner,
    records: list[dict[str, object]],
    allowed_exit_codes: set[int] | None = None,
) -> CommandResult:
    result = runner(command, project_root)
    records.append(command_record(name, command, result))
    allowed = allowed_exit_codes or {0}
    if result.returncode not in allowed:
        raise RuntimeError(f"{name} failed with exit code {result.returncode}")
    return result


def npm_command() -> str:
    return shutil.which("npm") or "npm"


def preflight_commands(python: str, npm: str | None = None) -> list[tuple[str, list[str]]]:
    npm = npm or npm_command()
    return [
        (
            "repository-refresh-tests",
            [python, "skills/github-inspiration-editor/scripts/test_refresh_repositories.py"],
        ),
        (
            "research-refresh-tests",
            [python, "skills/github-inspiration-editor/scripts/test_research_refresh.py"],
        ),
        (
            "refresh-cycle-tests",
            [python, "skills/github-inspiration-editor/scripts/test_refresh_cycle.py"],
        ),
        (
            "version-manager-tests",
            [python, "skills/github-inspiration-editor/scripts/test_version_manager.py"],
        ),
        (
            "visual-identity-tests",
            [python, "skills/github-inspiration-editor/scripts/test_visual_identity.py"],
        ),
        ("identity-renderer-tests", [npm, "run", "test:identity-renderer"]),
        ("lint", [npm, "run", "lint"]),
        ("build", [npm, "run", "build"]),
    ]


def run_commands(
    commands: list[tuple[str, list[str]]],
    project_root: Path,
    runner: CommandRunner,
    records: list[dict[str, object]],
) -> None:
    for name, command in commands:
        run_step(name=name, command=command, project_root=project_root, runner=runner, records=records)


def run_cycle(
    *,
    project_root: Path,
    mode: str,
    runner: CommandRunner = default_runner,
    python: str = sys.executable,
    run_validations_enabled: bool = True,
    now: Callable[[], str] = utc_now,
) -> tuple[dict[str, object], int]:
    if mode not in {"check", "write", "resume"}:
        raise ValueError(f"unsupported mode: {mode}")

    started_at = now()
    run_id = started_at.replace(":", "-")
    records: list[dict[str, object]] = []
    stage_six: dict[str, object] | None = None
    stage_seven: dict[str, object] | None = None
    versioning: dict[str, object] = {"outcome": "not-required", "snapshotId": None, "rollback": None}
    prewrite_snapshot: dict[str, object] | None = None
    mutation_started = False
    status = "running"
    actor = "none"
    next_action = ""
    exit_code = 0
    try:
        if run_validations_enabled and mode != "resume":
            run_commands(preflight_commands(python), project_root, runner, records)

        with tempfile.TemporaryDirectory(prefix="github-inspiration-refresh-") as directory:
            temporary_root = Path(directory)
            stage_six_dry_report = temporary_root / "stage-six-dry.json"
            stage_seven_dry_report = temporary_root / "stage-seven-dry.json"

            if mode != "resume":
                stage_six_dry_command = [
                    python,
                    "skills/github-inspiration-editor/scripts/refresh_repositories.py",
                    "--report",
                    str(stage_six_dry_report),
                ]
                result = run_step(
                    name="stage-six-dry-run",
                    command=stage_six_dry_command,
                    project_root=project_root,
                    runner=runner,
                    records=records,
                    allowed_exit_codes={0, 2},
                )
                stage_six = read_json_object(stage_six_dry_report, "stage-six dry-run report")
                stage_six_summary = report_summary(stage_six, "stage-six dry-run report")
                if result.returncode == 2 or integer_count(stage_six_summary, "reviewRequired", "stage-six summary"):
                    status = "human-decision-required"
                    actor = "human"
                    next_action = "Review the critical repository change; no files were written by this cycle."
                    exit_code = 2
                elif mode == "check":
                    stage_seven_dry_command = [
                        python,
                        "skills/github-inspiration-editor/scripts/refresh_research_sources.py",
                        "--stage-six-report",
                        str(stage_six_dry_report),
                        "--report",
                        str(stage_seven_dry_report),
                    ]
                    result = run_step(
                        name="stage-seven-dry-run",
                        command=stage_seven_dry_command,
                        project_root=project_root,
                        runner=runner,
                        records=records,
                        allowed_exit_codes={0, 2},
                    )
                    stage_seven = read_json_object(stage_seven_dry_report, "stage-seven dry-run report")
                    status, actor, next_action = status_from_research_report(stage_seven)
                    if result.returncode == 2 or status == "human-decision-required":
                        exit_code = 2
                    elif status == "failed":
                        exit_code = 1
                    else:
                        status = "check-completed"
                        actor = "none"
                        next_action = "Run the write command to persist safe metadata and source changes."

            if mode == "write" and status == "running":
                prewrite_snapshot = create_snapshot(project_root, f"before-refresh-cycle:{run_id}")
                versioning = {
                    "outcome": "snapshot-created",
                    "snapshotId": prewrite_snapshot["snapshotId"],
                    "rollback": None,
                }
                stage_six_write_report = project_root / "outputs/refresh/latest.json"
                mutation_started = True
                run_step(
                    name="stage-six-write",
                    command=[
                        python,
                        "skills/github-inspiration-editor/scripts/refresh_repositories.py",
                        "--write",
                        "--report",
                        str(stage_six_write_report),
                    ],
                    project_root=project_root,
                    runner=runner,
                    records=records,
                    allowed_exit_codes={0, 2},
                )
                stage_six = read_json_object(stage_six_write_report, "stage-six write report")
                stage_six_summary = report_summary(stage_six, "stage-six write report")
                if integer_count(stage_six_summary, "reviewRequired", "stage-six summary"):
                    status = "human-decision-required"
                    actor = "human"
                    next_action = "Review the critical repository change before running stage seven."
                    exit_code = 2
                else:
                    stage_seven_dry_command = [
                        python,
                        "skills/github-inspiration-editor/scripts/refresh_research_sources.py",
                        "--report",
                        str(stage_seven_dry_report),
                    ]
                    result = run_step(
                        name="stage-seven-dry-run",
                        command=stage_seven_dry_command,
                        project_root=project_root,
                        runner=runner,
                        records=records,
                        allowed_exit_codes={0, 2},
                    )
                    stage_seven = read_json_object(stage_seven_dry_report, "stage-seven dry-run report")
                    dry_status, _, _ = status_from_research_report(stage_seven)
                    if result.returncode == 2 or dry_status == "human-decision-required":
                        status = "human-decision-required"
                        actor = "human"
                        next_action = "Review the critical source change; stage-seven source state was not written."
                        exit_code = 2
                    else:
                        stage_seven_write_report = project_root / "outputs/refresh/research-latest.json"
                        result = run_step(
                            name="stage-seven-write",
                            command=[
                                python,
                                "skills/github-inspiration-editor/scripts/refresh_research_sources.py",
                                "--write",
                                "--report",
                                str(stage_seven_write_report),
                            ],
                            project_root=project_root,
                            runner=runner,
                            records=records,
                            allowed_exit_codes={0, 2},
                        )
                        stage_seven = read_json_object(stage_seven_write_report, "stage-seven write report")
                        status, actor, next_action = status_from_research_report(stage_seven)
                        if result.returncode == 2 or status == "human-decision-required":
                            exit_code = 2

            if mode == "resume":
                stage_six_path = project_root / "outputs/refresh/latest.json"
                stage_six = read_json_object(stage_six_path, "stage-six report")
                stage_six_summary = report_summary(stage_six, "stage-six report")
                if integer_count(stage_six_summary, "failed", "stage-six summary") or integer_count(
                    stage_six_summary, "reviewRequired", "stage-six summary"
                ):
                    raise RuntimeError("stage-six report is not safe to resume")
                prewrite_snapshot = create_snapshot(project_root, f"before-refresh-resume:{run_id}")
                versioning = {
                    "outcome": "snapshot-created",
                    "snapshotId": prewrite_snapshot["snapshotId"],
                    "rollback": None,
                }
                stage_seven_write_report = project_root / "outputs/refresh/research-latest.json"
                mutation_started = True
                result = run_step(
                    name="stage-seven-resume",
                    command=[
                        python,
                        "skills/github-inspiration-editor/scripts/refresh_research_sources.py",
                        "--write",
                        "--report",
                        str(stage_seven_write_report),
                    ],
                    project_root=project_root,
                    runner=runner,
                    records=records,
                    allowed_exit_codes={0, 2},
                )
                stage_seven = read_json_object(stage_seven_write_report, "stage-seven resume report")
                status, actor, next_action = status_from_research_report(stage_seven)
                if result.returncode == 2 or status == "human-decision-required":
                    exit_code = 2

        if run_validations_enabled and mode in {"write", "resume"} and status not in {"failed", "human-decision-required"}:
            run_commands(
                [
                    ("post-write-lint", [npm_command(), "run", "lint"]),
                    ("post-write-build", [npm_command(), "run", "build"]),
                ],
                project_root,
                runner,
                records,
            )

    except (OSError, ValueError, RuntimeError) as error:
        status = "failed"
        actor = "ai"
        next_action = str(error)
        exit_code = 1

    if prewrite_snapshot is not None:
        if mutation_started and status in {"failed", "human-decision-required"}:
            try:
                rollback = restore_snapshot(project_root, str(prewrite_snapshot["snapshotId"]))
                versioning = {
                    "outcome": "rolled-back",
                    "snapshotId": prewrite_snapshot["snapshotId"],
                    "rollback": rollback,
                }
                next_action = f"{next_action} Refresh-state writes were restored from snapshot {prewrite_snapshot['snapshotId']}."
            except (OSError, ValueError, RuntimeError) as rollback_error:
                versioning = {
                    "outcome": "rollback-failed",
                    "snapshotId": prewrite_snapshot["snapshotId"],
                    "rollback": {"error": str(rollback_error)},
                }
                status = "failed"
                actor = "human"
                next_action = f"Automatic rollback failed: {rollback_error}. Do not run another write cycle."
                exit_code = 1
        elif mutation_started:
            versioning["outcome"] = "committed"
        else:
            versioning["outcome"] = "no-write"

        try:
            transaction = {
                "schemaVersion": 1,
                "transactionId": run_id,
                "startedAt": started_at,
                "finishedAt": utc_now(),
                "mode": mode,
                "status": status,
                "snapshotId": prewrite_snapshot["snapshotId"],
                "outcome": versioning["outcome"],
                "rollback": versioning["rollback"],
                "publicationAuthorized": False,
            }
            transaction_path = write_transaction(project_root, transaction)
            versioning["transactionFile"] = transaction_path.relative_to(project_root).as_posix()
        except (OSError, ValueError) as transaction_error:
            if versioning["outcome"] == "committed":
                try:
                    rollback = restore_snapshot(project_root, str(prewrite_snapshot["snapshotId"]))
                    versioning.update({"outcome": "rolled-back", "rollback": rollback})
                except (OSError, ValueError, RuntimeError) as rollback_error:
                    versioning.update({"outcome": "rollback-failed", "rollback": {"error": str(rollback_error)}})
                    actor = "human"
            status = "failed"
            exit_code = 1
            next_action = f"Version transaction record failed: {transaction_error}."

    finished_at = now()
    report: dict[str, object] = {
        "schemaVersion": SCHEMA_VERSION,
        "runId": run_id,
        "mode": mode,
        "startedAt": started_at,
        "finishedAt": finished_at,
        "status": status,
        "nextActor": actor,
        "nextAction": next_action,
        "publicationAuthorized": False,
        "versioning": versioning,
        "stageSix": stage_six,
        "stageSeven": stage_seven,
        "steps": records,
    }
    return report, exit_code


def main() -> int:
    project_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="Persist safe stage-six and stage-seven refresh outputs")
    mode.add_argument("--resume", action="store_true", help="Re-evaluate stage seven after AI review files are ready")
    parser.add_argument(
        "--report",
        type=Path,
        default=project_root / "outputs/automation/latest.json",
        help="Automation report path",
    )
    parser.add_argument("--skip-validations", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--no-lock", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    selected_mode = "write" if args.write else "resume" if args.resume else "check"
    started_at = utc_now()
    run_id = started_at.replace(":", "-")
    lock_path = project_root / "outputs/automation/refresh.lock"
    locked = False

    try:
        if not args.no_lock:
            create_lock(lock_path, run_id, started_at)
            locked = True
        report, exit_code = run_cycle(
            project_root=project_root,
            mode=selected_mode,
            run_validations_enabled=not args.skip_validations,
        )
        write_json_atomic(args.report, report)
        history_path = project_root / "outputs/automation/runs" / f"{report['runId']}.json"
        write_json_atomic(history_path, report)
        # Keep the terminal copy ASCII-safe because Windows may still expose a
        # legacy GBK stdout even though child tools emit UTF-8 symbols such as ✓.
        # The persisted JSON remains UTF-8 and human-readable.
        print(json.dumps(report, ensure_ascii=True, indent=2))
        return exit_code
    except (OSError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    finally:
        if locked:
            try:
                lock_path.unlink()
            except FileNotFoundError:
                pass


if __name__ == "__main__":
    raise SystemExit(main())
