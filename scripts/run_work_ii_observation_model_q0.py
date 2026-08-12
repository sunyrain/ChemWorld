#!/usr/bin/env python3
"""Run the provider-free Work II observation/measurement Q0 audit."""

from __future__ import annotations

import argparse
from pathlib import Path
from time import perf_counter
from typing import Any

from chemworld.eval.observation_identifiability import (
    audit_observation_identifiability,
    load_observation_identifiability_protocol,
)
from chemworld.eval.provenance import canonical_json_sha256, git_source_commit, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-observation-model-q0-20260812.json"
)
SUMMARY_VERSION = "chemworld-work-ii-observation-model-q0-summary-0.1"


def run(output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite Work II observation Q0 output: {output}")
    started = perf_counter()
    protocol = load_observation_identifiability_protocol()
    audit = audit_observation_identifiability(protocol, workspace=ROOT)
    instruments = audit["instruments"]
    controls = audit["controls"]
    failures = sorted(key for key, passed in controls.items() if not passed)
    summary: dict[str, Any] = {
        "schema_version": SUMMARY_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "participant_session_count": 0,
        "source_commit": git_source_commit(ROOT),
        "source_tree_dirty": audit["source_tree_dirty"],
        "protocol_id": audit["protocol_id"],
        "protocol_sha256": audit["protocol_sha256"],
        "coverage": {
            "spectral_instrument_count": len(instruments),
            "high_contrast_state_pair_count": 1,
            "low_signal_state_pair_count": 1,
            "ph_high_contrast_pair_count": 1,
            "ph_low_contrast_pair_count": 1,
            "spectrum_condition_count": len(audit["spectrum_conditions"]["condition_sha256"]),
            "archive_record_count": len(audit["history_archive"]["catalog"]),
            "archive_retrieval_attempt_count": len(audit["history_archive"]["ledger"]),
        },
        "controls": controls,
        "failure_count": len(failures),
        "failures": failures,
        "instruments": instruments,
        "ph_meter": audit["ph_meter"],
        "spectrum_conditions": audit["spectrum_conditions"],
        "history_archive": audit["history_archive"],
        "leakage_matches": audit["leakage_matches"],
        "q0_passed": bool(audit["controls_ready"] and not failures),
        "provider_execution_authorized": False,
        "participant_d1_authorized": False,
        "decision": (
            "proceed_to_two_task_five_world_observation_screen_design"
            if audit["controls_ready"] and not failures
            else "repair_observation_q0_before_cross_task_screen"
        ),
        "limitations": audit["limitations"],
        "elapsed_s": round(perf_counter() - started, 3),
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(output, summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    summary = run(args.output)
    print(
        {
            "q0_passed": summary["q0_passed"],
            "failure_count": summary["failure_count"],
            "decision": summary["decision"],
            "elapsed_s": summary["elapsed_s"],
        },
        flush=True,
    )
    return 0 if summary["q0_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
