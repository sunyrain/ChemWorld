"""Run the local ChemWorld release gate.

This script is intentionally CI-like but local-first. It runs the same command
sequence a maintainer should use before publishing a versioned release.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BACKEND_REPORT = ROOT / "workstreams/world_foundation/reports/backend-v0.5.json"


@dataclass(frozen=True)
class GateCommand:
    name: str
    command: list[str]

    def to_dict(self) -> dict[str, object]:
        return {"name": self.name, "command": self.command}


def release_gate_commands(
    *,
    python: str,
    output_dir: Path,
    require_frozen_benchmark: bool = False,
) -> list[GateCommand]:
    audit_dir = output_dir / "audit"
    baseline_dir = output_dir / "baseline_smoke"
    return [
        GateCommand("claims", [python, "scripts/manage_claims.py", "check"]),
        GateCommand(
            "current_evidence",
            [python, "scripts/evidence_pipeline.py", "--check"],
        ),
        GateCommand("lint", [python, "-m", "ruff", "check", "."]),
        GateCommand("type_check", [python, "-m", "mypy", "src/chemworld"]),
        GateCommand("tests", [python, "-m", "pytest"]),
        GateCommand("docs", [python, "-m", "mkdocs", "build", "--strict"]),
        GateCommand(
            "wheel_smoke",
            [
                python,
                "scripts/smoke_test_wheel.py",
                *(
                    ["--require-validated-benchmark"]
                    if require_frozen_benchmark
                    else []
                ),
            ],
        ),
        GateCommand(
            "reference_validation",
            [python, "scripts/run_reference_validation.py"],
        ),
        GateCommand(
            "runtime_boundary_audit",
            [
                python,
                "scripts/audit_runtime_boundary.py",
                "--output",
                str(output_dir / "runtime_boundary_report.json"),
            ],
        ),
        GateCommand(
            "model_reachability_audit",
            [
                python,
                "scripts/audit_model_reachability.py",
                "--output",
                str(output_dir / "model_reachability_report.json"),
            ],
        ),
        GateCommand(
            "environment_audit",
            [
                python,
                "scripts/audit_environment_consistency.py",
                "--tasks",
                "all",
                "--seeds",
                "0",
                "1",
                "2",
                "--output-dir",
                str(audit_dir),
            ],
        ),
        GateCommand(
            "baseline_smoke",
            [
                python,
                "-m",
                "chemworld.cli",
                "baselines",
                "report",
                "--tasks",
                "reaction-to-assay",
                "--agents",
                "scripted_chemistry",
                "--seeds",
                "0",
                "--output-dir",
                str(baseline_dir),
            ],
        ),
        GateCommand(
            "frozen_benchmark" if require_frozen_benchmark else "benchmark_candidate_integrity",
            [
                python,
                "scripts/check_frozen_benchmark.py",
                *([] if require_frozen_benchmark else ["--allow-candidate"]),
                "--output",
                str(output_dir / "benchmark_release_integrity.json"),
            ],
        ),
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        default="runs/release_gate",
        help="Directory for release gate summaries and smoke artifacts.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the command plan without executing it.",
    )
    parser.add_argument(
        "--continue-on-failure",
        action="store_true",
        help="Run remaining commands even if one gate fails.",
    )
    parser.add_argument(
        "--require-frozen-benchmark",
        action="store_true",
        help="Require a current immutable benchmark bundle instead of candidate integrity only.",
    )
    parser.add_argument(
        "--allow-dirty-candidate",
        action="store_true",
        help=(
            "Allow a dirty tracked tree only for a non-claiming candidate audit. "
            "The summary records the dirty state and cannot enable a frozen release claim."
        ),
    )
    parser.add_argument(
        "--summary-path",
        type=Path,
        help="Optional stable path for the final machine-readable summary.",
    )
    return parser.parse_args()


def _git_commit() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _tracked_tree_dirty() -> bool:
    completed = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        check=True,
        capture_output=True,
        text=True,
    )
    return bool(completed.stdout.strip())


def _source_state_control(
    *,
    source_commit: str,
    finished_source_commit: str,
    dirty_at_finish: bool,
    allow_dirty_candidate: bool = False,
) -> dict[str, object]:
    commit_stable = source_commit == finished_source_commit
    source_integrity_passed = commit_stable and (
        not dirty_at_finish or allow_dirty_candidate
    )
    return {
        "status": "passed" if source_integrity_passed else "blocked",
        "source_commit_at_finish": finished_source_commit,
        "source_commit_stable": commit_stable,
        "source_tree_dirty_at_finish": dirty_at_finish,
        "dirty_candidate_mode": allow_dirty_candidate,
        "source_integrity_passed": source_integrity_passed,
    }


def _release_status(*, succeeded: bool, require_frozen_benchmark: bool) -> str:
    if not succeeded:
        return "blocked"
    return "release_ready" if require_frozen_benchmark else "candidate_gate_passed"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _backend_evidence() -> dict[str, Any]:
    report = json.loads(BACKEND_REPORT.read_text(encoding="utf-8"))
    return {
        "path": BACKEND_REPORT.relative_to(ROOT).as_posix(),
        "file_sha256": _sha256(BACKEND_REPORT),
        "schema_version": report.get("schema_version"),
        "backend_id": report.get("backend_id"),
        "report_hash": report.get("report_hash"),
        "status": report.get("status"),
        "backend_contract_validated": report.get("backend_contract_validated"),
        "clean_release_attestation": report.get("clean_release_attestation"),
        "backend_freeze_allowed": report.get("backend_freeze_allowed"),
        "benchmark_claim_allowed": report.get("benchmark_claim_allowed"),
    }


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    commands = release_gate_commands(
        python=sys.executable,
        output_dir=output_dir,
        require_frozen_benchmark=args.require_frozen_benchmark,
    )
    if args.dry_run:
        print(json.dumps([command.to_dict() for command in commands], indent=2))
        return 0
    if args.allow_dirty_candidate and args.require_frozen_benchmark:
        raise RuntimeError("dirty candidate mode cannot require a frozen benchmark")

    output_dir.mkdir(parents=True, exist_ok=True)
    source_commit = _git_commit()
    dirty_at_start = _tracked_tree_dirty()
    if dirty_at_start and not args.allow_dirty_candidate:
        raise RuntimeError("release gate requires a clean tracked source tree")
    summary: dict[str, Any] = {
        "schema_version": "chemworld-release-gate-0.3",
        "status": "running",
        "gate_state": "pending",
        "started_at": datetime.now(UTC).isoformat(),
        "source_commit": source_commit,
        "source_tree_dirty_at_start": dirty_at_start,
        "dirty_candidate_mode": bool(args.allow_dirty_candidate),
        "backend_evidence": _backend_evidence(),
        "output_dir": str(output_dir),
        "benchmark_mode": ("strict_frozen" if args.require_frozen_benchmark else "candidate"),
        "backend_candidate_gate_ready": False,
        "release_claim_ready": False,
        "benchmark_claim_allowed": False,
        "commands": [],
    }
    overall_success = True
    for gate in commands:
        print(f"[release-gate] running {gate.name}: {' '.join(gate.command)}", flush=True)
        started = time.perf_counter()
        completed = subprocess.run(gate.command, check=False)
        elapsed_s = time.perf_counter() - started
        success = completed.returncode == 0
        overall_success = overall_success and success
        summary["commands"].append(
            {
                "name": gate.name,
                "command": gate.command,
                "returncode": completed.returncode,
                "elapsed_s": elapsed_s,
                "success": success,
            }
        )
        (output_dir / "release_gate_summary.json").write_text(
            json.dumps(summary, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        if not success and not args.continue_on_failure:
            break

    finished_source_commit = _git_commit()
    dirty_at_finish = _tracked_tree_dirty()
    source_state = _source_state_control(
        source_commit=source_commit,
        finished_source_commit=finished_source_commit,
        dirty_at_finish=dirty_at_finish,
        allow_dirty_candidate=bool(args.allow_dirty_candidate),
    )
    overall_success = overall_success and bool(source_state["source_integrity_passed"])
    summary["finished_at"] = datetime.now(UTC).isoformat()
    summary["source_control"] = source_state
    summary["status"] = _release_status(
        succeeded=overall_success,
        require_frozen_benchmark=bool(args.require_frozen_benchmark),
    )
    summary["gate_state"] = "passed" if overall_success else "blocked"
    summary["success"] = overall_success
    summary["backend_candidate_gate_ready"] = overall_success
    summary["release_claim_ready"] = bool(overall_success and args.require_frozen_benchmark)
    encoded = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    (output_dir / "release_gate_summary.json").write_text(encoded, encoding="utf-8")
    if args.summary_path is not None:
        args.summary_path.parent.mkdir(parents=True, exist_ok=True)
        args.summary_path.write_text(encoded, encoding="utf-8")
    return 0 if overall_success else 1


if __name__ == "__main__":
    raise SystemExit(main())
