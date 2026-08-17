"""Shared runtime helpers for retained and future longitudinal decision blocks."""

from __future__ import annotations

import json
import threading
from collections.abc import Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from pathlib import Path
from time import perf_counter
from typing import Any

from run_work_ii_campaign_pilot import _run_cell

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_law_summary import evaluate_final_law_summary
from chemworld.eval.work_ii_longitudinal_action_readout import evaluate_terminal_readout
from chemworld.eval.work_ii_resource_calibration_v02 import (
    AGENT_INVALID_ENFORCEMENT_POLICY,
    PROVIDER_ERROR_ENFORCEMENT_POLICY,
)

LAW_EVALUATION_CONTRACT = {
    "schema_version": "chemworld-work-ii-as-longitudinal-law-evaluation-contract-0.1",
    "role": "pre_reveal_final_checkpoint_mechanism_adequacy",
    "maximum_adequate_law_normalized_mae": 0.05,
    "candidate_packet_may_not_update_checkpoint": True,
}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


class Progress:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.lock = threading.Lock()

    def emit(self, payload: Mapping[str, Any]) -> None:
        rendered = json.dumps(dict(payload), ensure_ascii=False, sort_keys=True)
        with self.lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(rendered + "\n")
            print(rendered, flush=True)


def _final_snapshot(summary: Mapping[str, Any]) -> dict[str, Any] | None:
    analysis = summary.get("analysis")
    analysis = analysis if isinstance(analysis, Mapping) else {}
    snapshots = analysis.get("belief_snapshots")
    snapshots = snapshots if isinstance(snapshots, list) else []
    finals = [
        dict(item)
        for item in snapshots
        if isinstance(item, Mapping) and item.get("stage") == "final"
    ]
    return finals[0] if len(finals) == 1 else None


def _law_evaluation(cell: Mapping[str, Any], summary: Mapping[str, Any]) -> dict[str, Any]:
    final = _final_snapshot(summary)
    return evaluate_final_law_summary(
        final.get("law_summary") if final is not None else None,
        truth_plan=cell["checkpoint_truth_plan"],
        evaluator_truth=cell["checkpoint_truth"],
        final_checkpoint_predictions=(final.get("predictions") if final is not None else None),
        effective_pre_error=None,
        effective_final_error=None,
        evaluation_contract=LAW_EVALUATION_CONTRACT,
    )


def _run_one_cell(
    cell: Mapping[str, Any],
    *,
    output_root: Path,
    phase: str,
    progress: Progress,
    cell_index: int,
    total_cells: int,
) -> dict[str, Any]:
    cell_id = str(cell["cell_id"])
    config = _load(output_root / str(cell["campaign_config_path"]))
    started = perf_counter()
    progress.emit(
        {
            "stage": f"lar_{phase}_cell_started",
            "cell_id": cell_id,
            "cell": cell_index,
            "total_cells": total_cells,
        }
    )
    campaign_summary = _run_cell(
        config=config,
        world_seed=int(cell["world_seed"]),
        arm=str(cell["arm"]),
        cell_index=cell_index,
        total_cells=total_cells,
        cell_root=output_root / phase / "campaigns" / cell_id,
        progress_path=output_root / phase / "campaign-progress" / f"{cell_id}.jsonl",
        agent_invalid_enforcement=AGENT_INVALID_ENFORCEMENT_POLICY,
        provider_error_enforcement=PROVIDER_ERROR_ENFORCEMENT_POLICY,
        provider_resource_limits_report_only=True,
    )
    campaign_summary = deepcopy(dict(campaign_summary))
    campaign_summary["law_summary_evaluation"] = _law_evaluation(cell, campaign_summary)
    action = evaluate_terminal_readout(
        cell,
        campaign_summary,
        maximum_adequate_law_normalized_mae=float(
            LAW_EVALUATION_CONTRACT["maximum_adequate_law_normalized_mae"]
        ),
    )
    result: dict[str, Any] = {
        "schema_version": "chemworld-work-ii-as-longitudinal-action-readout-result-0.1",
        "cell_id": cell_id,
        "cluster_id": cell["cluster_id"],
        "world_seed": cell["world_seed"],
        "arm": cell["arm"],
        "phase": phase,
        "terminal_action_contract_sha256": cell["terminal_action_readout"][
            "contract_sha256"
        ],
        "campaign_summary": campaign_summary,
        **action,
        "elapsed_s": round(perf_counter() - started, 3),
    }
    result["result_sha256"] = canonical_json_sha256(result)
    write_json_atomic(output_root / phase / "cells" / f"{cell_id}.json", result)
    progress.emit(
        {
            "stage": f"lar_{phase}_cell_terminal",
            "cell_id": cell_id,
            "cell": cell_index,
            "total_cells": total_cells,
            "status": result.get("status"),
            "campaign_completed": campaign_summary.get("completed"),
            "elapsed_s": result["elapsed_s"],
        }
    )
    return result


def _execute_cells(
    cells: Sequence[Mapping[str, Any]],
    *,
    output_root: Path,
    phase: str,
    workers: int,
    progress: Progress,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    started = perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(
                _run_one_cell,
                cell,
                output_root=output_root,
                phase=phase,
                progress=progress,
                cell_index=index,
                total_cells=len(cells),
            ): cell
            for index, cell in enumerate(cells, start=1)
        }
        for future in as_completed(futures):
            results.append(future.result())
            completed = len(results)
            elapsed = max(perf_counter() - started, 1.0e-9)
            throughput = completed / elapsed
            progress.emit(
                {
                    "stage": f"lar_{phase}_progress",
                    "completed_cells": completed,
                    "total_cells": len(cells),
                    "eligible_cells": sum(
                        row.get("status") == "completed_uncontaminated"
                        for row in results
                    ),
                    "throughput_cells_per_hour": round(throughput * 3600.0, 3),
                    "eta_seconds": (
                        round((len(cells) - completed) / throughput, 1)
                        if throughput > 0.0
                        else None
                    ),
                }
            )
    return results


__all__ = [
    "LAW_EVALUATION_CONTRACT",
    "Progress",
    "_execute_cells",
    "_law_evaluation",
]
