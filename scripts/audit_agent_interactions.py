"""Audit retained algorithm and LLM interaction evidence before vNext redesign."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from chemworld.eval.interaction_audit import build_agent_interaction_audit


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _task_lab_artifacts(root: Path) -> list[dict[str, Any]]:
    artifacts: list[dict[str, Any]] = []
    if not root.exists():
        return artifacts
    for result_path in sorted(root.rglob("evaluation_result.json")):
        payload = _load_json(result_path)
        trajectory_path = result_path.with_name("trajectory.jsonl")
        artifacts.append(
            {
                "artifact_sha256": hashlib.sha256(result_path.read_bytes()).hexdigest(),
                "verified": bool(payload.get("verified")),
                "trajectory_retained": trajectory_path.is_file(),
                "uses_spectra": bool(payload.get("spectrum_disclosure")),
                "adapts_within_experiment": payload.get("agent_name")
                == "deepseek_task_lab",
            }
        )
    return artifacts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--task-lab-root", type=Path, default=Path("runs/task_lab"))
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workstreams/benchmark_v1/reports/agent-interaction-audit.json"),
    )
    args = parser.parse_args()
    results = _load_json(args.results)
    if not isinstance(results, list):
        raise ValueError("--results must contain a JSON list")
    report = build_agent_interaction_audit(
        results,
        task_lab_artifacts=_task_lab_artifacts(args.task_lab_root),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(args.output),
                "status": report["status"],
                "gates": report["gates"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
