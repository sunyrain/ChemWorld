"""Run Gate A or resumable paired campaigns for mechanism adaptation v0.2.1."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from chemworld.eval.mechanism_adaptation_execution import (  # noqa: E402
    DEFAULT_GATE_A_PLAN_PATH,
    DEFAULT_LLM_METHODS_PATH,
    DEFAULT_PROTOCOL_PATH,
    load_json_object,
    run_campaign_row,
    run_gate_a,
    selected_campaign_rows,
)

DEFAULT_GATE_A_REPORT = (
    ROOT / "workstreams/flagship_tasks/reports/mechanism-adaptation-gate-a-v0.2.1.json"
)
DEFAULT_RUNTIME_ROOT = ROOT / "runs/mechanism-adaptation-v0.2.1"


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _run_gate_a(args: argparse.Namespace) -> int:
    protocol = load_json_object(args.protocol)
    plan = load_json_object(args.gate_a_plan)
    print(
        json.dumps(
            {
                "status": "starting",
                "stage": "gate-a",
                "tasks": protocol["design"]["tasks"],
                "budgets": plan["held_out_certificate"]["budgets"],
                "world_seeds_per_family": plan["held_out_certificate"][
                    "world_seeds_per_family"
                ],
                "external_provider_calls": False,
            },
            sort_keys=True,
        ),
        flush=True,
    )
    report = run_gate_a(protocol, plan)
    _write_json(args.output, report)
    print(
        json.dumps(
            {
                "status": report["status"],
                "gate_a_pass": report["gate_a_pass"],
                "primary_gate_budget": report["primary_gate_budget"],
                "output": str(args.output),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["gate_a_pass"] else 1


def _run_campaigns(args: argparse.Namespace) -> int:
    protocol = load_json_object(args.protocol)
    methods = load_json_object(args.llm_methods)
    rows = selected_campaign_rows(
        protocol,
        tasks=args.task,
        pair_ids=args.pair_id,
        limit=args.pair_limit,
    )
    summaries = args.runtime_root / "campaigns"
    completed = 0
    reused = 0
    for row in rows:
        path = summaries / f"{row['pair_id']}--{row['arm']}.json"
        if args.resume and path.is_file():
            _validate_resumable_campaign(path, row=row, protocol=protocol)
            reused += 1
            print(json.dumps({"status": "reused", "path": str(path)}), flush=True)
            continue
        print(
            json.dumps(
                {
                    "status": "starting",
                    "pair_id": row["pair_id"],
                    "arm": row["arm"],
                    "task_id": row["task_id"],
                }
            ),
            flush=True,
        )
        result = run_campaign_row(
            protocol,
            row,
            output_root=args.runtime_root,
            llm_methods=methods,
            method_id=args.method_id,
            spectrum_disclosure=args.spectrum_disclosure,
        )
        _write_json(path, result)
        completed += 1
    index = {
        "schema_version": "chemworld-mechanism-adaptation-campaign-index-0.2",
        "protocol_id": protocol["protocol_id"],
        "selected_row_count": len(rows),
        "selected_pair_count": len({row["pair_id"] for row in rows}),
        "completed_this_invocation": completed,
        "reused_this_invocation": reused,
        "campaign_paths": [
            str(summaries / f"{row['pair_id']}--{row['arm']}.json") for row in rows
        ],
        "formal_result": False,
    }
    _write_json(args.runtime_root / "campaign-index.json", index)
    print(json.dumps(index, indent=2, sort_keys=True))
    return 0


def _validate_resumable_campaign(
    path: Path,
    *,
    row: dict[str, Any],
    protocol: dict[str, Any],
) -> None:
    payload = load_json_object(path)
    expected_protocol = hashlib.sha256(
        json.dumps(protocol, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if payload.get("protocol_sha256") != expected_protocol:
        raise RuntimeError(f"refusing stale campaign protocol binding: {path}")
    if payload.get("matrix_row") != row:
        raise RuntimeError(f"refusing stale campaign matrix-row binding: {path}")
    for phase in ("iid", "shifted"):
        phase_payload = payload.get(phase)
        if not isinstance(phase_payload, dict):
            raise RuntimeError(f"resumable campaign lacks {phase} phase: {path}")
        trajectory_path = Path(str(phase_payload.get("trajectory_path") or ""))
        if not trajectory_path.is_absolute():
            trajectory_path = ROOT / trajectory_path
        if not trajectory_path.is_file():
            raise RuntimeError(f"resumable campaign trajectory is missing: {trajectory_path}")
        observed = hashlib.sha256(trajectory_path.read_bytes()).hexdigest()
        if observed != phase_payload.get("trajectory_sha256"):
            raise RuntimeError(f"resumable campaign trajectory digest is stale: {trajectory_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stage",
        choices=("gate-a", "campaign"),
        default="gate-a",
        help="Gate A is environment-only; campaign makes external provider calls.",
    )
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL_PATH)
    parser.add_argument("--gate-a-plan", type=Path, default=DEFAULT_GATE_A_PLAN_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_GATE_A_REPORT)
    parser.add_argument("--llm-methods", type=Path, default=DEFAULT_LLM_METHODS_PATH)
    parser.add_argument("--runtime-root", type=Path, default=DEFAULT_RUNTIME_ROOT)
    parser.add_argument("--method-id", default="live_llm_b")
    parser.add_argument(
        "--spectrum-disclosure", choices=("assigned", "unassigned", "masked"), default="assigned"
    )
    parser.add_argument("--task", action="append")
    parser.add_argument("--pair-id", action="append")
    parser.add_argument("--pair-limit", type=int)
    parser.add_argument("--resume", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return _run_gate_a(args) if args.stage == "gate-a" else _run_campaigns(args)


if __name__ == "__main__":
    raise SystemExit(main())
