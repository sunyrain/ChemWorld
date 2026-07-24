"""Validate frozen A2/A3 production entry paths without consuming a trial."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import chemworld.eval.mechanism_adaptation_execution as execution  # noqa: E402


class _FirstFormalJobReachedError(RuntimeError):
    pass


def _stop_before_first_job(*args: Any, **kwargs: Any) -> Any:
    raise _FirstFormalJobReachedError


def _validate_entry(
    stage: str,
    protocol: dict[str, Any],
    plan: dict[str, Any],
    *,
    pending_a3_path: Path,
) -> None:
    original = execution.execute_jobs_resumable
    execution.execute_jobs_resumable = _stop_before_first_job
    try:
        with tempfile.TemporaryDirectory(
            prefix=f"chemworld-{stage}-entry-validation-"
        ) as raw:
            design_audit = execution.load_json_object(
                ROOT / plan["design_validity_precondition"]["report"]
            )
            if stage == "a3":
                execution.run_online_attainability_certificate(
                    protocol,
                    plan,
                    design_validity_audit=design_audit,
                    trial_store_root=Path(raw),
                )
            else:
                execution.run_gate_a(
                    protocol,
                    plan,
                    online_attainability_certificate=(
                        execution.load_json_object(pending_a3_path)
                    ),
                    design_validity_audit=design_audit,
                    trial_store_root=Path(raw),
                )
    except _FirstFormalJobReachedError:
        return
    finally:
        execution.execute_jobs_resumable = original
    raise RuntimeError(f"{stage.upper()} did not reach its first formal job")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--protocol",
        type=Path,
        default=execution.DEFAULT_PROTOCOL_PATH,
    )
    parser.add_argument(
        "--plan",
        type=Path,
        default=execution.DEFAULT_GATE_A_PLAN_PATH,
    )
    parser.add_argument(
        "--pending-a3",
        type=Path,
        required=True,
    )
    args = parser.parse_args()
    protocol = execution.load_protocol_object(args.protocol)
    plan = execution.load_json_object(args.plan)
    for stage in ("a3", "a2"):
        _validate_entry(
            stage,
            protocol,
            plan,
            pending_a3_path=args.pending_a3,
        )
    print(
        json.dumps(
            {
                "status": "passed",
                "formal_trials_consumed": 0,
                "validated_entries": ["a3", "a2"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
