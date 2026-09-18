#!/usr/bin/env python3
"""Preflight or execute the sealed seven-locus Experiment 1 confirmation."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from time import perf_counter
from typing import Any

from chemworld.eval.experiment_1_confirmation import (
    ELIGIBLE_LOCI,
    build_preflight,
    validate_public_contract,
    verify_self_hash,
)
from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
LOCUS_RUNNER = ROOT / "scripts/run_experiment_1_confirmation_locus.py"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--preflight", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--secret-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--preflight-receipt", type=Path)
    parser.add_argument("--allow-confirmation-execution", action="store_true")
    parser.add_argument("--workers", type=int, default=1)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    contract_path = args.contract.resolve()
    contract = _load(contract_path)
    validate_public_contract(ROOT, contract)
    secret_dir = args.secret_dir.resolve()
    if args.preflight:
        receipt = build_preflight(
            ROOT,
            contract,
            secret_dir=secret_dir,
            output_root=args.output.resolve(),
        )
        target = args.output.resolve()
        if target.exists():
            raise FileExistsError("refusing to overwrite confirmation preflight")
        write_json_atomic(target, receipt)
        print(
            json.dumps(
                {
                    "status": receipt["status"],
                    "atomic_units": receipt["atomic_units"],
                    "planned_primary_executions": receipt["planned_primary_executions"],
                    "planned_tolerance_zero_replays": receipt["planned_tolerance_zero_replays"],
                    "preflight_sha256": receipt["preflight_sha256"],
                },
                sort_keys=True,
            ),
            flush=True,
        )
        return 0
    if not args.allow_confirmation_execution:
        raise RuntimeError("confirmation execution requires --allow-confirmation-execution")
    if args.workers != 1:
        raise ValueError("v1.0 confirmation freezes worker_count=1")
    if args.preflight_receipt is None:
        raise ValueError("confirmation execution requires --preflight-receipt")
    preflight = _load(args.preflight_receipt.resolve())
    verify_self_hash(preflight, "preflight_sha256")
    if preflight.get("status") != "ready-but-not-executed":
        raise ValueError("confirmation preflight is not ready")
    if preflight.get("contract_sha256") != contract["contract_sha256"]:
        raise ValueError("confirmation preflight contract binding mismatch")
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError("one-shot confirmation output already exists")
    output.mkdir(parents=True)
    plan_path = secret_dir / "realized-plan.json"
    started = perf_counter()
    process_rows: list[dict[str, Any]] = []
    for index, block in enumerate(ELIGIBLE_LOCI, 1):
        locus_output = output / block
        command = [
            sys.executable,
            str(LOCUS_RUNNER),
            "--contract",
            str(contract_path),
            "--secret-plan",
            str(plan_path),
            "--locus",
            block,
            "--output",
            str(locus_output),
        ]
        completed = subprocess.run(command, cwd=ROOT, check=False)
        receipt_path = locus_output / "confirmation-receipt.json"
        receipt = _load(receipt_path) if receipt_path.is_file() else None
        process_rows.append(
            {
                "block": block,
                "world_denominator": 5,
                "returncode": completed.returncode,
                "receipt_sha256": receipt.get("receipt_sha256") if receipt else None,
                "five_world_qualified": (receipt.get("five_world_qualified") if receipt else False),
                "terminal": True,
                "process_failure_retained": completed.returncode != 0 or receipt is None,
            }
        )
        elapsed = perf_counter() - started
        rate = index / elapsed if elapsed else 0.0
        print(
            json.dumps(
                {
                    "event": "experiment_1_confirmation_progress",
                    "completed_loci": index,
                    "total_loci": 7,
                    "completed_atomic_units": index * 5,
                    "total_atomic_units": 35,
                    "last_block": block,
                    "elapsed_s": round(elapsed, 1),
                    "eta_s": round((7 - index) / rate, 1) if rate else None,
                },
                sort_keys=True,
            ),
            flush=True,
        )
    summary: dict[str, Any] = {
        "schema_version": "chemworld-experiment-1-confirmation-summary-1.0",
        "formal_result": True,
        "qualification_stage": "confirmation",
        "process_isolated": True,
        "one_shot": True,
        "contract_sha256": contract["contract_sha256"],
        "preflight_sha256": preflight["preflight_sha256"],
        "locus_denominator": 7,
        "atomic_unit_denominator": 35,
        "terminal_atomic_units": sum(row["world_denominator"] for row in process_rows),
        "qualified_loci": sum(row["five_world_qualified"] is True for row in process_rows),
        "failed_loci": sum(row["five_world_qualified"] is not True for row in process_rows),
        "process_rows": process_rows,
        "all_missing_rows_retained": True,
        "elapsed_s": round(perf_counter() - started, 3),
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(output / "summary.json", summary)
    return 0 if summary["failed_loci"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
