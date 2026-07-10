"""Run the ChemWorld serious-task candidate experiment package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.baseline_report import (
    SERIOUS_BASELINE_AGENTS,
    generate_baseline_report,
)
from chemworld.eval.paper_artifact import create_paper_artifact
from chemworld.task_design import serious_task_readiness_manifest
from chemworld.tasks import SERIOUS_TASK_IDS


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="runs/serious_task_suite")
    parser.add_argument("--smoke", action="store_true", help="Run a small fast slice.")
    parser.add_argument("--tasks", nargs="+")
    parser.add_argument("--agents", nargs="+")
    parser.add_argument("--seeds", nargs="+", type=int)
    args = parser.parse_args()

    root = Path(args.output_dir)
    root.mkdir(parents=True, exist_ok=True)
    tasks = args.tasks or list(SERIOUS_TASK_IDS)
    if args.smoke:
        agents = args.agents or ["scripted_chemistry", "tool_using_llm_stub"]
        seeds = args.seeds or [0]
    else:
        agents = args.agents or list(SERIOUS_BASELINE_AGENTS)
        seeds = args.seeds

    baseline_report = generate_baseline_report(
        task_ids=tasks,
        agents=agents,
        seeds=seeds,
        output_dir=root / "baseline_report",
    )
    artifact_summary = create_paper_artifact(
        output_dir=root / "artifact",
        task_ids=tasks,
        agents=agents,
        seeds=seeds or [0],
    )
    manifest = {
        "schema_version": "chemworld-serious-task-suite-run-0.1",
        "suite_status": "candidate",
        "tasks": tasks,
        "agents": agents,
        "seeds": seeds,
        "smoke": bool(args.smoke),
        "readiness": serious_task_readiness_manifest(),
        "baseline_report": str(root / "baseline_report" / "baseline_report.json"),
        "artifact_summary": str(root / "artifact" / "artifact_summary.json"),
        "baseline_result_count": baseline_report.result_count,
        "artifact_replay_verified": artifact_summary["replay_verified"],
    }
    (root / "serious_task_suite_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
