"""Run the local ChemWorld release gate.

This script is intentionally CI-like but local-first. It runs the same command
sequence a maintainer should use before publishing a versioned release.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


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
        GateCommand("lint", [python, "-m", "ruff", "check", "."]),
        GateCommand("type_check", [python, "-m", "mypy", "src/chemworld"]),
        GateCommand("tests", [python, "-m", "pytest"]),
        GateCommand("docs", [python, "-m", "mkdocs", "build", "--strict"]),
        GateCommand("wheel_smoke", [python, "scripts/smoke_test_wheel.py"]),
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
            "model_adapter_intake",
            [
                python,
                "scripts/validate_model_adapters.py",
                "--output",
                str(output_dir / "model_adapter_intake_report.json"),
            ],
        ),
        GateCommand(
            "vnext_staging_plan",
            [
                python,
                "scripts/build_vnext_integration_plan.py",
                "--output",
                str(output_dir / "vnext_integration_plan.json"),
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
    return parser.parse_args()


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

    output_dir.mkdir(parents=True, exist_ok=True)
    summary: dict[str, Any] = {
        "schema_version": "chemworld-release-gate-0.1",
        "started_at": datetime.now(UTC).isoformat(),
        "output_dir": str(output_dir),
        "benchmark_mode": ("strict_frozen" if args.require_frozen_benchmark else "candidate"),
        "release_claim_ready": False,
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

    summary["finished_at"] = datetime.now(UTC).isoformat()
    summary["success"] = overall_success
    summary["release_claim_ready"] = bool(overall_success and args.require_frozen_benchmark)
    (output_dir / "release_gate_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return 0 if overall_success else 1


if __name__ == "__main__":
    raise SystemExit(main())
