"""Run or inspect a preflight-issued ChemWorld formal matrix."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from chemworld.eval.formal_matrix import (
    SubprocessCellExecutor,
    build_formal_matrix_plan,
    run_formal_matrix,
)


def _read_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON object required: {path}")
    return payload


def _print_progress(event: dict[str, Any]) -> None:
    visible = {
        key: event[key]
        for key in (
            "sequence",
            "status",
            "task_id",
            "method_id",
            "pair_id",
            "spectrum_condition",
            "queue",
            "complete_experiment_count",
            "replay_verified",
            "matrix_status",
        )
        if key in event
    }
    print(json.dumps(visible, sort_keys=True), flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--private-runtime-root", type=Path)
    parser.add_argument("--adapter-factory")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--diagnostic-serial",
        action="store_true",
        help="run the issued cells serially for nonformal equivalence diagnostics",
    )
    parser.add_argument(
        "--stop-after-new-terminals",
        type=int,
        help="controlled resumability probe; never changes cell identity",
    )
    args = parser.parse_args()

    try:
        manifest_path = args.manifest.resolve(strict=True)
        manifest = _read_object(manifest_path)
        plan = build_formal_matrix_plan(manifest)
        print(json.dumps(plan.public_summary(), indent=2, sort_keys=True), flush=True)
        if args.dry_run:
            return 0
        if args.private_runtime_root is None or args.adapter_factory is None:
            parser.error("execution requires --private-runtime-root and --adapter-factory")
        executor = SubprocessCellExecutor(
            manifest_path=str(manifest_path),
            output_root=str(args.output_dir.resolve()),
            private_runtime_root=str(args.private_runtime_root.resolve(strict=True)),
            adapter_factory=args.adapter_factory,
            python_executable=sys.executable,
            cell_script=str(Path(__file__).resolve().parent / "run_formal_cell.py"),
        )
        outcome = run_formal_matrix(
            plan=plan,
            executor=executor,
            output_root=args.output_dir,
            mode="diagnostic_serial" if args.diagnostic_serial else "parallel",
            progress_callback=_print_progress,
            stop_after_new_terminals=args.stop_after_new_terminals,
        )
    except (OSError, ValueError, TypeError, RuntimeError) as exc:
        parser.exit(2, f"formal matrix rejected: {type(exc).__name__}: {exc}\n")

    status = str(outcome.report["status"])
    if status == "complete_aggregation_ready":
        return 0
    if status == "stopped_resumable":
        return 3
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
