#!/usr/bin/env python3
"""Stage-aware recovery for the EQ v2 K1/Q/K2/EQS execution block."""
# ruff: noqa: E501

from __future__ import annotations

import os
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import scripts.recover_work_ii_eq_bounded_equilibrium as legacy
import scripts.run_work_ii_eq_bounded_equilibrium_v2 as eq

legacy.eq = eq
legacy.STAGES = eq.POSTTEST_STAGES

interrupted_snapshot = legacy.interrupted_snapshot
recovery_kind = legacy.recovery_kind
latest_recovery = legacy.latest_recovery
effective_result = legacy.effective_result
source_receipt_folder = legacy.source_receipt_folder
recover_posttests = legacy.recover_posttests
recover_one = legacy.recover_one
plan = legacy.plan


def finalize(
    root: Path, config: Mapping[str, Any], schedule: Sequence[Mapping[str, Any]]
) -> dict[str, Any] | None:
    resolved = [effective_result(root, config, cell) for cell in schedule]
    if len(resolved) != 15 or not all(
        result
        and result.get("status") == "completed"
        and result.get("posttest_chain_sealed") is True
        for result, _ in resolved
    ):
        return None
    truth = eq.generate_truth(root, config)
    for result, _ in resolved:
        assert result is not None
        evaluation = eq.evaluate_predictions(
            result["posttests"]["Q"].get("payload"),
            eq.queries(config),
            truth[result["world_id"]],
        )
        evaluation["eqs"] = eq.evaluate_eqs(
            result["posttests"]["EQS"].get("payload"),
            float(eq.world_by_id(config, result["world_id"])["private_authoring"]["effective_pka"]),
        )
        eq.write(root / "evaluations" / f"{result['cell_id']}.json", evaluation)
    summary = {
        "schema_version": "work-ii-eq-effective-summary-2.0",
        "phase": "complete",
        "planned_sources": 15,
        "effective_sources": 15,
        "effective_source_batches": sum(len(result.get("batches", [])) for result, _ in resolved if result),
        "sealed_posttests": sum(len(result.get("posttests", {})) for result, _ in resolved if result),
        "sealed_posttest_chains": sum(result.get("posttest_chain_sealed") is True for result, _ in resolved if result),
        "failures": [],
        "cells": [
            {
                "cell_id": result["cell_id"],
                "status": result["status"],
                "effective_result": os.path.relpath(path, root),
            }
            for result, path in resolved
            if result
        ],
    }
    eq.write(root / "effective-summary.json", summary)
    completion = {
        "schema_version": "work-ii-eq-completion-2.0",
        "completed_epoch": time.time(),
        "source_sessions": 15,
        "source_batches": 180,
        "posttests": 60,
        "reference_executions": 300,
        "equilibrium_confidence_used_as_agent_uncertainty_or_score": False,
        "effective_summary_sha256": eq.digest(summary),
    }
    eq.write(root / "completion.json", completion)
    return completion


def main() -> None:
    legacy.finalize = finalize
    legacy.main()


if __name__ == "__main__":
    main()
