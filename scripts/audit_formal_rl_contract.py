"""Audit and optionally validate the benchmark-v0.5 formal RL contract slice."""

from __future__ import annotations

import argparse
import json
import platform
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from chemworld.eval.formal_rl import (
    DEFAULT_CONFIG_PATH,
    audit_formal_rl_contract,
    file_sha256,
    load_formal_rl_config,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "workstreams/benchmark_v1/reports/rl-contract-v0.4.json"
SOURCE_FILES = (
    "configs/methods/rl_v0.4/rl_methods.json",
    "scripts/audit_formal_rl_contract.py",
    "src/chemworld/eval/formal_rl.py",
    "src/chemworld/agents/rl.py",
    "src/chemworld/rl/hybrid_actions.py",
    "src/chemworld/rl/hybrid_policy.py",
    "src/chemworld/rl/environment.py",
    "src/chemworld/rl/training.py",
    "src/chemworld/rl/evaluation.py",
    "tests/test_formal_rl.py",
    "tests/test_rl_training_accounting.py",
    "tests/test_rl_foundation_contract.py",
)


def _git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _tracked_tree_dirty(*, exclude: Path) -> bool:
    relative_exclude = exclude.resolve().relative_to(ROOT).as_posix()
    output = _git("status", "--porcelain", "--untracked-files=all")
    for line in output.splitlines():
        candidate = line[3:].replace("\\", "/")
        if " -> " in candidate:
            candidate = candidate.rsplit(" -> ", 1)[1]
        if candidate != relative_exclude:
            return True
    return False


def _run(command: list[str]) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    output = "\n".join(
        item for item in (completed.stdout.strip(), completed.stderr.strip()) if item
    )
    summary = output.splitlines()[-1] if output else "no output"
    passed_match = re.search(r"(\d+) passed", output)
    skipped_match = re.search(r"(\d+) skipped", output)
    return {
        "command": command,
        "exit_code": completed.returncode,
        "passed": int(passed_match.group(1)) if passed_match else None,
        "skipped": int(skipped_match.group(1)) if skipped_match else 0,
        "summary": summary[:500],
        "result": "passed" if completed.returncode == 0 else "failed",
    }


def _validation(python: str) -> dict[str, Any]:
    pytest_result = _run(
        [
            python,
            "-m",
            "pytest",
            "tests/test_formal_rl.py",
            "tests/test_rl_training_accounting.py",
            "tests/test_rl_foundation_contract.py",
            "--no-cov",
            "-q",
        ]
    )
    ruff_result = _run(
        [
            python,
            "-m",
            "ruff",
            "check",
            "src/chemworld/eval/formal_rl.py",
            "src/chemworld/agents/rl.py",
            "src/chemworld/rl/hybrid_actions.py",
            "src/chemworld/rl/hybrid_policy.py",
            "src/chemworld/rl/training.py",
            "src/chemworld/rl/evaluation.py",
            "scripts/audit_formal_rl_contract.py",
            "tests/test_formal_rl.py",
            "tests/test_rl_training_accounting.py",
            "tests/test_rl_foundation_contract.py",
        ]
    )
    mypy_result = _run(
        [
            python,
            "-m",
            "mypy",
            "src/chemworld/eval/formal_rl.py",
            "src/chemworld/agents/rl.py",
            "src/chemworld/rl/hybrid_actions.py",
            "src/chemworld/rl/hybrid_policy.py",
            "src/chemworld/rl/training.py",
            "src/chemworld/rl/evaluation.py",
        ]
    )
    return {
        "focused_tests": pytest_result,
        "ruff": ruff_result,
        "mypy": mypy_result,
        "all_passed": all(
            result["exit_code"] == 0
            for result in (pytest_result, ruff_result, mypy_result)
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / DEFAULT_CONFIG_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--run-validation", action="store_true")
    parser.add_argument("--validation-python", default=sys.executable)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = load_formal_rl_config(args.config)
    report = audit_formal_rl_contract(config, root=ROOT)
    report.update(
        {
            "source_commit": _git("rev-parse", "HEAD"),
            "source_tree_dirty_during_validation": _tracked_tree_dirty(
                exclude=args.output
            ),
            "source_files": {
                path: file_sha256(ROOT / path)
                for path in SOURCE_FILES
                if (ROOT / path).is_file()
            },
            "environment": {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "machine": platform.machine(),
                "processor": platform.processor(),
            },
            "validation": (
                _validation(args.validation_python)
                if args.run_validation
                else {
                    "all_passed": None,
                    "status": "not_run_by_this_invocation",
                }
            ),
            "audit_command": [
                args.validation_python,
                "scripts/audit_formal_rl_contract.py",
                *( ["--run-validation"] if args.run_validation else [] ),
            ],
        }
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": report["status"],
                "controls_ready": report["controls_ready"],
                "validation_passed": report["validation"]["all_passed"],
                "output": str(args.output),
            },
            indent=2,
        )
    )
    controls_passed = report["controls_ready"] is True
    validation_passed = not args.run_validation or report["validation"]["all_passed"] is True
    return 0 if controls_passed and validation_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
