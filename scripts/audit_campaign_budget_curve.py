"""Audit paired adaptive value at prefixes of long campaign trajectories."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from chemworld.data.logging import load_jsonl
from chemworld.data.submission import git_commit
from chemworld.eval.metrics import evaluate_records
from chemworld.eval.validity_power import audit_validity_power, campaign_record_prefix
from chemworld.tasks import SERIOUS_TASK_IDS, get_task
from chemworld.world.parameters import WORLD_FAMILY_VERSION


def _tracked_tree_dirty() -> bool:
    completed = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        check=True,
        capture_output=True,
        text=True,
    )
    return bool(completed.stdout.strip())


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _corpus_digest(paths: list[Path], root: Path) -> str:
    digest = hashlib.sha256()
    for path in paths:
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(_sha256(path).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trajectory-root", type=Path, required=True)
    parser.add_argument("--checkpoints", nargs="+", type=int, default=[4, 8, 12, 20, 40])
    parser.add_argument("--practical-effect", type=float, default=0.05)
    parser.add_argument("--planned-seeds", type=int, default=20)
    parser.add_argument("--evaluation-manifest", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workstreams/benchmark_v1/reports/campaign-budget-curve.json"),
    )
    args = parser.parse_args()
    checkpoints = sorted(set(args.checkpoints))
    if not checkpoints or checkpoints[0] < 1:
        parser.error("checkpoints must be positive")

    paths = sorted(args.trajectory_root.rglob("*.jsonl"))
    if not paths:
        raise ValueError(f"No trajectories found under {args.trajectory_root}")
    results_by_checkpoint: dict[int, list[dict[str, Any]]] = {
        checkpoint: [] for checkpoint in checkpoints
    }
    source_commits: set[str] = set()
    for path in paths:
        records = load_jsonl(path)
        if not records:
            raise ValueError(f"Empty trajectory: {path}")
        first = records[0]
        task_id = str(first.get("benchmark_task_id") or "")
        if task_id not in SERIOUS_TASK_IDS:
            raise ValueError(f"Unexpected task in {path}: {task_id!r}")
        metadata = first.get("agent_metadata", {})
        method = str(metadata.get("agent_name") or metadata.get("agent_family") or "")
        if not method:
            raise ValueError(f"Missing agent name in {path}")
        commit = metadata.get("git_commit")
        if commit:
            source_commits.add(str(commit))
        for checkpoint in checkpoints:
            prefix = campaign_record_prefix(records, checkpoint)
            result = evaluate_records(prefix, threshold=get_task(task_id).threshold).to_dict()
            result.update(
                {
                    "task_id": task_id,
                    "baseline_agent": method,
                    "evaluation_budget_steps": len(prefix),
                    "diagnostic_complete_experiments": checkpoint,
                    "trajectory_path": path.relative_to(args.trajectory_root).as_posix(),
                }
            )
            results_by_checkpoint[checkpoint].append(result)

    audits = {
        str(checkpoint): audit_validity_power(
            results,
            practical_effect=args.practical_effect,
            planned_seed_count=args.planned_seeds,
        )
        for checkpoint, results in results_by_checkpoint.items()
    }
    evaluation_manifest: dict[str, Any] | None = None
    if args.evaluation_manifest is not None:
        evaluation_manifest = json.loads(args.evaluation_manifest.read_text(encoding="utf-8"))
    report = {
        "schema_version": "chemworld-campaign-budget-curve-0.1",
        "status": "diagnostic_only",
        "paper_claim_allowed": False,
        "checkpoints_complete_experiments": checkpoints,
        "practical_effect_threshold": args.practical_effect,
        "audits": audits,
        "provenance": {
            "report_source_commit": git_commit(),
            "report_source_tree_dirty": _tracked_tree_dirty(),
            "evaluated_source_commits": sorted(source_commits),
            "evaluation_source_tree_dirty": (
                None
                if evaluation_manifest is None
                else bool(evaluation_manifest.get("evaluation_source_tree_dirty"))
            ),
            "evaluation_manifest_sha256": (
                None
                if args.evaluation_manifest is None
                else _sha256(args.evaluation_manifest)
            ),
            "trajectory_count": len(paths),
            "trajectory_corpus_sha256": _corpus_digest(paths, args.trajectory_root),
            "world_law_id": WORLD_FAMILY_VERSION,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(
        (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8")
    )
    summary = {
        "output": str(args.output),
        "trajectory_count": len(paths),
        "adaptive_value_task_count_by_checkpoint": {
            checkpoint: audit["adaptive_value_task_count"]
            for checkpoint, audit in audits.items()
        },
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
