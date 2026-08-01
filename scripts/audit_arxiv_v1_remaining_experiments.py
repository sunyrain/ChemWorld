"""Audit the remaining first-arXiv experiment matrix without promoting live data."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic

SCHEMA_VERSION = "chemworld-arxiv-v1-remaining-experiment-audit-0.1"
EXPECTED_CELLS = 20
EXPECTED_VESSELS_PER_CELL = 6
EXPECTED_OPPORTUNITIES = EXPECTED_CELLS * EXPECTED_VESSELS_PER_CELL
EXISTING_G0_EXPERIMENTS = 29_580
EXISTING_G2_V04_EXPERIMENTS = 60


def _load_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return payload


def _load_last_jsonl(path: Path) -> tuple[int, dict[str, Any] | None]:
    count = 0
    last: dict[str, Any] | None = None
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            payload = json.loads(line)
            if not isinstance(payload, dict):
                raise ValueError(f"trajectory row is not an object: {path}")
            count += 1
            last = payload
    return count, last


def _dig(payload: Mapping[str, Any], dotted: str) -> Any:
    current: Any = payload
    for part in dotted.split("."):
        if not isinstance(current, Mapping):
            return None
        current = current.get(part)
    return current


def _campaign_counts(last: Mapping[str, Any] | None) -> dict[str, int]:
    if last is None:
        return {
            "vessel_starts": 0,
            "final_assays": 0,
            "discarded_vessels": 0,
        }
    state = _dig(
        last,
        "agent_view.tool_json.campaign_state.campaign_resources.state",
    )
    campaign = _dig(last, "agent_view.tool_json.campaign_state")
    if not isinstance(state, Mapping) or not isinstance(campaign, Mapping):
        raise ValueError("trajectory lacks public campaign resource state")
    discarded = campaign.get("discarded_batches", [])
    return {
        "vessel_starts": int(state.get("vessel_starts", 0) or 0),
        "final_assays": int(campaign.get("final_assay_count", 0) or 0),
        "discarded_vessels": len(discarded) if isinstance(discarded, list) else 0,
    }


def _latest_attempt_dir(run_root: Path, cell_id: str) -> Path | None:
    cell_root = run_root / cell_id
    attempts = sorted(
        path for path in cell_root.glob("attempt-*") if path.is_dir()
    )
    return attempts[-1] if attempts else None


def _cell_observation(
    run_root: Path,
    state: Mapping[str, Any],
) -> dict[str, Any]:
    cell = state.get("cell")
    if not isinstance(cell, Mapping):
        raise ValueError("manifest cell state lacks cell identity")
    cell_id = str(cell.get("cell_id"))
    authoritative = state.get("authoritative_attempt_dir")
    attempt_dir = (
        run_root / str(authoritative)
        if isinstance(authoritative, str) and authoritative
        else _latest_attempt_dir(run_root, cell_id)
    )
    trajectory = None if attempt_dir is None else attempt_dir / "trajectory.jsonl"
    operation_count = 0
    last = None
    if trajectory is not None and trajectory.is_file():
        operation_count, last = _load_last_jsonl(trajectory)
    counts = _campaign_counts(last)
    return {
        "cell_id": cell_id,
        "world_seed": int(cell["world_seed"]),
        "trajectory_replicate_id": str(cell["trajectory_replicate_id"]),
        "condition_id": str(cell["condition_id"]),
        "manifest_state": str(state.get("state")),
        "formally_promotable": state.get("state") in {"completed", "right_censored"},
        "operation_count_observed": operation_count,
        **counts,
    }


def _pair_accounting(cells: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    pairs: dict[tuple[int, str], list[Mapping[str, Any]]] = {}
    for cell in cells:
        key = (int(cell["world_seed"]), str(cell["trajectory_replicate_id"]))
        pairs.setdefault(key, []).append(cell)
    if len(pairs) != 10 or any(len(pair) != 2 for pair in pairs.values()):
        raise ValueError("manifest does not contain ten complete pair identities")
    rows: list[dict[str, Any]] = []
    for (world_seed, replicate_id), pair in sorted(pairs.items()):
        states = sorted(str(cell["manifest_state"]) for cell in pair)
        both_terminal = all(
            state in {"completed", "right_censored"} for state in states
        )
        both_completed = states == ["completed", "completed"]
        classification = (
            "completed_pair"
            if both_completed
            else "right_censored_pair"
            if both_terminal
            else "unresolved_pair"
        )
        rows.append(
            {
                "world_seed": world_seed,
                "trajectory_replicate_id": replicate_id,
                "states": states,
                "classification": classification,
            }
        )
    counts = Counter(row["classification"] for row in rows)
    per_world: dict[str, Any] = {}
    for world_seed in sorted({int(row["world_seed"]) for row in rows}):
        world_rows = [row for row in rows if row["world_seed"] == world_seed]
        world_counts = Counter(row["classification"] for row in world_rows)
        per_world[str(world_seed)] = {
            "planned_pairs": len(world_rows),
            "completed_pairs": world_counts["completed_pair"],
            "right_censored_pairs": world_counts["right_censored_pair"],
            "unresolved_pairs": world_counts["unresolved_pair"],
            "maximum_possible_completed_pairs": (
                world_counts["completed_pair"] + world_counts["unresolved_pair"]
            ),
        }
    return {
        "planned_pairs": len(rows),
        "completed_pairs": counts["completed_pair"],
        "right_censored_pairs": counts["right_censored_pair"],
        "unresolved_pairs": counts["unresolved_pair"],
        "maximum_possible_completed_pairs": (
            counts["completed_pair"] + counts["unresolved_pair"]
        ),
        "per_world": per_world,
        "pairs": rows,
    }


def audit_remaining_experiments(manifest_path: Path) -> dict[str, Any]:
    manifest_path = manifest_path.resolve()
    run_root = manifest_path.parent
    manifest = _load_object(manifest_path)
    states = manifest.get("cells")
    if not isinstance(states, list) or len(states) != EXPECTED_CELLS:
        raise ValueError("G2 v0.5 manifest must contain exactly 20 cells")
    if int(manifest.get("planned_physical_experiment_count", -1)) != (
        EXPECTED_OPPORTUNITIES
    ):
        raise ValueError("G2 v0.5 manifest must declare 120 vessel opportunities")
    cells = [
        _cell_observation(run_root, state)
        for state in states
        if isinstance(state, Mapping)
    ]
    if len(cells) != len(states):
        raise ValueError("manifest cell states must be objects")
    state_counts = Counter(cell["manifest_state"] for cell in cells)
    unexpected_states = set(state_counts) - {
        "pending",
        "completed",
        "right_censored",
    }
    if unexpected_states:
        raise ValueError(f"unexpected manifest states: {sorted(unexpected_states)}")

    terminal = [cell for cell in cells if cell["formally_promotable"]]
    pending = [cell for cell in cells if not cell["formally_promotable"]]
    terminal_started = sum(int(cell["vessel_starts"]) for cell in terminal)
    terminal_final = sum(int(cell["final_assays"]) for cell in terminal)
    terminal_discarded = sum(int(cell["discarded_vessels"]) for cell in terminal)
    terminal_slots = len(terminal) * EXPECTED_VESSELS_PER_CELL
    terminal_started_censored = max(
        0,
        terminal_started - terminal_final - terminal_discarded,
    )
    terminal_unstarted = max(0, terminal_slots - terminal_started)
    remaining_slots = EXPECTED_OPPORTUNITIES - terminal_slots
    live_started = sum(int(cell["vessel_starts"]) for cell in cells)
    live_final = sum(int(cell["final_assays"]) for cell in cells)
    pair_accounting = _pair_accounting(cells)

    report: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "scope": "first arXiv required scientific experiment matrix",
        "manifest_path": manifest_path.as_posix(),
        "fixed_design": {
            "g0_new_experiments_required": 0,
            "g2_v0_5_cells": EXPECTED_CELLS,
            "g2_v0_5_vessels_per_cell": EXPECTED_VESSELS_PER_CELL,
            "g2_v0_5_planned_vessel_opportunities": EXPECTED_OPPORTUNITIES,
            "existing_completed_or_audited_experiments": {
                "g0": EXISTING_G0_EXPERIMENTS,
                "g2_v0_4": EXISTING_G2_V04_EXPERIMENTS,
                "total": EXISTING_G0_EXPERIMENTS + EXISTING_G2_V04_EXPERIMENTS,
            },
        },
        "formal_terminal_accounting": {
            "completed_cells": state_counts["completed"],
            "right_censored_cells": state_counts["right_censored"],
            "cells_still_to_terminalize": len(pending),
            "resolved_vessel_opportunity_slots": terminal_slots,
            "vessel_opportunity_slots_still_to_resolve": remaining_slots,
            "executed_vessels_in_terminal_cells": terminal_started,
            "completed_final_assays_in_terminal_cells": terminal_final,
            "discarded_vessels_in_terminal_cells": terminal_discarded,
            "started_right_censored_vessels_in_terminal_cells": (
                terminal_started_censored
            ),
            "unstarted_slots_lost_to_terminal_cell_censoring": terminal_unstarted,
        },
        "durable_live_preview_not_promoted": {
            "observed_operation_count": sum(
                int(cell["operation_count_observed"]) for cell in cells
            ),
            "observed_vessel_starts": live_started,
            "observed_final_assays": live_final,
            "additional_vessel_starts_in_pending_cells": (
                live_started - terminal_started
            ),
            "additional_final_assays_in_pending_cells": live_final - terminal_final,
            "caveat": (
                "pending-cell bytes are a read-only progress preview and cannot enter "
                "the paper until the cell is terminal and passes the frozen audit"
            ),
        },
        "final_count_bounds_if_all_unresolved_slots_complete": {
            "maximum_g2_v0_5_executed_vessels": terminal_started + remaining_slots,
            "maximum_g2_v0_5_completed_final_assays": terminal_final + remaining_slots,
            "maximum_total_executed_physical_experiments": (
                EXISTING_G0_EXPERIMENTS
                + EXISTING_G2_V04_EXPERIMENTS
                + terminal_started
                + remaining_slots
            ),
            "maximum_total_completed_final_assays_or_compiled_experiments": (
                EXISTING_G0_EXPERIMENTS
                + EXISTING_G2_V04_EXPERIMENTS
                + terminal_final
                + remaining_slots
            ),
            "planned_opportunity_denominator": (
                EXISTING_G0_EXPERIMENTS
                + EXISTING_G2_V04_EXPERIMENTS
                + EXPECTED_OPPORTUNITIES
            ),
            "counting_warning": (
                "the planned opportunity denominator is not the executed-vessel or "
                "completed-final-assay total when right-censoring leaves slots unstarted"
            ),
        },
        "paired_analysis_capacity": pair_accounting,
        "cells": cells,
        "remaining_required_scientific_work": {
            "new_g0_experiments": 0,
            "g2_cells_to_terminalize": len(pending),
            "g2_vessel_opportunity_slots_to_resolve": remaining_slots,
            "optional_post_arxiv_experiments_required": 0,
        },
    }
    report["audit_sha256"] = canonical_json_sha256(report)
    return report


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--json-output", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    report = audit_remaining_experiments(args.manifest)
    if args.json_output is not None:
        if "experiment-ledger" in args.json_output.name.lower():
            raise ValueError(
                "remaining-experiment audit cannot overwrite the fixed experiment ledger"
            )
        write_json_atomic(args.json_output, report)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
