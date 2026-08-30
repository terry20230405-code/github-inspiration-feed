#!/usr/bin/env python3
"""Export the currently published JSON layers as versioned project records."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from validate_project import validate


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def export_records(project_root: Path) -> dict[str, dict[str, object]]:
    data_root = project_root / "src/data"
    order = read_json(data_root / "order.json")
    repositories = read_json(data_root / "repositories.json")
    editorial = read_json(data_root / "editorial.json")
    visuals = read_json(data_root / "visuals.json")
    if not isinstance(order, list) or not all(isinstance(project_id, str) for project_id in order):
        raise ValueError("order.json must be an array of project IDs")
    if not all(isinstance(layer, dict) for layer in (repositories, editorial, visuals)):
        raise ValueError("published layers must be JSON objects")
    expected = set(order)
    for name, layer in (("repositories", repositories), ("editorial", editorial), ("visuals", visuals)):
        if set(layer) != expected:
            raise ValueError(f"{name}.json IDs do not match order.json")
    records: dict[str, dict[str, object]] = {}
    for project_id in order:
        record = {
            "schemaVersion": 2,
            "id": project_id,
            "repository": repositories[project_id],
            "editorial": editorial[project_id],
            "visual": visuals[project_id],
        }
        errors = validate(record)
        if errors:
            raise ValueError(f"{project_id} is invalid: {'; '.join(errors)}")
        records[project_id] = record
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output", default="outputs/generated/published-baseline")
    args = parser.parse_args()
    project_root = Path(__file__).resolve().parents[3]
    try:
        records = export_records(project_root)
        output_root = (project_root / args.output).resolve()
        if not output_root.is_relative_to(project_root.resolve()):
            raise ValueError("output path escapes project root")
        outputs = []
        for record in records.values():
            slug = record["repository"]["fullName"].lower().replace("/", "-")
            path = output_root / f"{slug}.project.json"
            outputs.append(path.relative_to(project_root).as_posix())
            if args.write:
                write_json_atomic(path, record)
        print(json.dumps({"mode": "write" if args.write else "dry-run", "projects": len(records), "outputs": outputs}, ensure_ascii=True, indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
