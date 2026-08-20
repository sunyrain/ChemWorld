#!/usr/bin/env python3
"""Validate and materialize the provider-free evidence-to-action design denominator."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_evidence_to_action import (
    build_design_manifest,
    validate_protocol,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = (
    ROOT / "configs/benchmark/work_ii_evidence_to_action_causal_decomposition_v0.1.json"
)
DEFAULT_OUTPUT = (
    ROOT
    / "runs/development/work-ii-evidence-to-action-causal-decomposition-v0.1/design-manifest.json"
)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    protocol_path = (
        args.protocol if args.protocol.is_absolute() else ROOT / args.protocol
    ).resolve()
    protocol = _load(protocol_path)
    errors = validate_protocol(protocol)
    if errors:
        raise ValueError("; ".join(errors))
    manifest = build_design_manifest(protocol)
    summary = {
        "study_id": manifest["study_id"],
        "task_world_clusters": manifest["task_world_cluster_count"],
        "task_world_prior_strata": manifest["task_world_prior_stratum_count"],
        "scheduled_sessions": manifest["scheduled_session_count"],
        "autonomous_sessions": manifest["autonomous_session_count"],
        "donor_dependent_sessions": manifest["donor_dependent_session_count"],
        "participant_physical_experiments": manifest["participant_physical_experiment_count"],
        "provider_execution_authorized": manifest["provider_execution_authorized"],
    }
    if not args.check_only:
        output_path = (args.output if args.output.is_absolute() else ROOT / args.output).resolve()
        write_json_atomic(output_path, manifest)
        summary["output"] = str(output_path)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
