"""Prepare, run, or resume the frozen live-LLM Train/Dev matrix."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from chemworld.eval.formal_matrix import build_formal_matrix_plan
from chemworld.eval.live_llm_development import (
    LIVE_STAGES,
    prepare_live_llm_development,
    run_live_llm_development,
)


def _progress(event: dict[str, Any]) -> None:
    public = {
        key: event[key]
        for key in (
            "sequence",
            "status",
            "task_id",
            "method_id",
            "pair_id",
            "spectrum_condition",
            "operation_count",
            "complete_experiment_count",
            "operation_type",
            "transaction_status",
            "trajectory_event_type",
            "replay_verified",
            "matrix_status",
        )
        if key in event
    }
    print(json.dumps(public, sort_keys=True), flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=LIVE_STAGES, required=True)
    parser.add_argument("--api-key-file", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--stop-after-new-terminals", type=int)
    args = parser.parse_args()

    if args.api_key_file is not None and not os.environ.get("DEEPSEEK_API_KEY"):
        os.environ["DEEPSEEK_API_KEY"] = args.api_key_file.read_text(
            encoding="utf-8"
        ).strip()
    if not args.dry_run and not os.environ.get("DEEPSEEK_API_KEY"):
        parser.error("set DEEPSEEK_API_KEY or pass --api-key-file")

    if args.dry_run:
        bundle, manifest_path, runtime_root, output_root = prepare_live_llm_development(
            stage=args.stage
        )
        plan = build_formal_matrix_plan(bundle.manifest)
        print(
            json.dumps(
                {
                    **plan.public_summary(),
                    "stage": args.stage,
                    "maximum_provider_call_count": bundle.maximum_provider_call_count,
                    "manifest_path": str(manifest_path),
                    "private_runtime_root": str(runtime_root),
                    "output_root": str(output_root),
                    "api_key_present": bool(os.environ.get("DEEPSEEK_API_KEY")),
                    "api_key_value_reported": False,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    report = run_live_llm_development(
        stage=args.stage,
        stop_after_new_terminals=args.stop_after_new_terminals,
        progress_callback=_progress,
    )
    print(
        json.dumps(
            {
                "status": report["status"],
                "stage": report["stage"],
                "cell_count": report["cell_count"],
                "formal_live_llm_development_ready": report[
                    "formal_live_llm_development_ready"
                ],
                "benchmark_claim_allowed": False,
            },
            indent=2,
            sort_keys=True,
        )
    )
    if report["matrix_run"]["status"] == "stopped_resumable":
        return 3
    return 0 if report["matrix_run"]["audit"]["aggregation_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
