"""Historical W2-47 feature-only design materializer; not a current authority."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from collections.abc import Mapping, Sequence
from copy import deepcopy
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256
from chemworld.eval.work_ii_longitudinal_action_readout import (
    ARMS,
    _checkpoint_action_hashes,
    build_terminal_contract,
)
from chemworld.eval.work_ii_reviewer_followup import build_b3_candidate_queries
from chemworld.eval.work_ii_truth import compile_evaluator_truth_query

PROTOCOL_VERSION = "chemworld-work-ii-as-longitudinal-decision-protocol-0.1"
DESIGN_VERSION = "chemworld-work-ii-as-longitudinal-decision-design-0.1"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _resolve(root: Path, value: object, *, field: str) -> Path:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be a non-empty path")
    path = Path(value)
    return path if path.is_absolute() else root / path


def load_decision_protocol(
    path: str | Path,
    *,
    repository_root: str | Path,
) -> tuple[Path, dict[str, Any]]:
    root = Path(repository_root).resolve()
    protocol_path = Path(path)
    protocol_path = protocol_path if protocol_path.is_absolute() else root / protocol_path
    protocol = _load(protocol_path)
    if protocol.get("schema_version") != PROTOCOL_VERSION:
        raise ValueError("unsupported longitudinal decision protocol")
    if protocol.get("status") != "design_frozen_provider_execution_not_authorized":
        raise ValueError("longitudinal decision protocol is not frozen and blocked")
    world_seeds = protocol.get("world_seeds")
    packet_seeds = protocol.get("candidate_packet_seeds")
    if (
        not isinstance(world_seeds, list)
        or len(world_seeds) != 5
        or len(set(world_seeds)) != 5
        or any(isinstance(item, bool) or not isinstance(item, int) for item in world_seeds)
    ):
        raise ValueError("longitudinal decision requires five distinct integer world seeds")
    if (
        not isinstance(packet_seeds, list)
        or len(packet_seeds) != 5
        or len(set(packet_seeds)) != 5
        or any(isinstance(item, bool) or not isinstance(item, int) for item in packet_seeds)
    ):
        raise ValueError("longitudinal decision requires five distinct packet seeds")
    if protocol.get("arms") != list(ARMS):
        raise ValueError("longitudinal decision arm order drifted")
    if protocol.get("campaign_complete_experiments") != 12:
        raise ValueError("longitudinal decision requires twelve experiments")
    if protocol.get("checkpoint_complete_experiments") != [0, 3, 6, 9, 12]:
        raise ValueError("longitudinal decision checkpoint schedule drifted")
    if protocol.get("prediction_mode") != "ranking_only":
        raise ValueError("longitudinal decision must use ranking-only terminal output")
    if protocol.get("selection_mode") != "rank_all_select_one":
        raise ValueError("longitudinal decision selection mode drifted")
    if protocol.get("terminal_reveal_gate") != (
        "campaign_terminal_and_all_belief_checkpoints_committed"
    ):
        raise ValueError("longitudinal decision reveal gate drifted")
    if protocol.get("candidate_count") != 8:
        raise ValueError("longitudinal decision requires eight candidates")
    if not isinstance(protocol.get("candidate_packet_namespace"), str) or not protocol[
        "candidate_packet_namespace"
    ]:
        raise ValueError("longitudinal decision packet namespace is unavailable")
    selection = protocol.get("candidate_selection")
    if not isinstance(selection, Mapping):
        raise ValueError("longitudinal decision candidate selection is unavailable")
    expected_selection = {
        "uses_hidden_truth": False,
        "uses_hidden_rank": False,
        "distinct_pair_count": 8,
        "volume_count_per_regime": 2,
        "mixing_count_per_regime": 4,
        "rule": "sha256_pair_permutation_then_balanced_public_axis_assignment",
    }
    if dict(selection) != expected_selection:
        raise ValueError("longitudinal decision candidate selection contract drifted")
    mechanism = protocol.get("mechanism_readout")
    if not isinstance(mechanism, Mapping):
        raise ValueError("longitudinal decision mechanism readout is unavailable")
    if (
        mechanism.get("checkpoint_query_count_per_world") != 16
        or mechanism.get("metric_ids")
        != ["product_in_organic", "product_in_aqueous", "phase_ratio", "score"]
        or mechanism.get("final_family_required") is not True
        or mechanism.get("final_exponent_required") is not True
        or mechanism.get("executable_law_required") is not True
        or mechanism.get("maximum_adequate_law_normalized_mae") != 0.05
    ):
        raise ValueError("longitudinal decision mechanism readout contract drifted")
    analysis = protocol.get("analysis")
    if not isinstance(analysis, Mapping):
        raise ValueError("longitudinal decision analysis contract is unavailable")
    if (
        analysis.get("statistical_unit") != "task_x_world_seed_cluster"
        or analysis.get("primary_endpoint") != "selected_action_raw_regret"
        or analysis.get("candidate_overlap_policy")
        != "retain_primary_and_label_direct_support"
        or analysis.get("low_score_range_policy") != "retain_and_report"
        or analysis.get("inference_scope")
        != "five_cluster_direction_consistency_and_paired_descriptive_effects"
        or analysis.get("strong_population_claim_allowed") is not False
    ):
        raise ValueError("longitudinal decision analysis contract drifted")
    execution = protocol.get("execution")
    if not isinstance(execution, Mapping):
        raise ValueError("longitudinal decision execution contract is unavailable")
    expected_counts = {
        "cluster_count": 5,
        "participant_session_count": 15,
        "participant_physical_experiment_count": 180,
        "candidate_truth_execution_count": 40,
        "checkpoint_truth_execution_count": 80,
        "provider_free_truth_execution_count": 120,
        "provider_free_exact_replay_count": 120,
    }
    if any(execution.get(key) != value for key, value in expected_counts.items()):
        raise ValueError("longitudinal decision execution denominators drifted")
    if execution.get("provider_execution_authorized") is not False:
        raise ValueError("longitudinal decision provider execution must remain blocked")
    if (
        execution.get("same_thread_required") is not True
        or execution.get("scientific_or_schema_failure_retained") is not True
        or execution.get("outcome_based_replacement_forbidden") is not True
    ):
        raise ValueError("longitudinal decision execution invariants drifted")
    return protocol_path, protocol


def build_candidate_pool(protocol: Mapping[str, Any]) -> list[dict[str, Any]]:
    pool: list[dict[str, Any]] = []
    for query in build_b3_candidate_queries(protocol):
        row = deepcopy(dict(query))
        query_id = str(row["query_id"])
        parts = query_id.split("-")
        if len(parts) != 5 or parts[0] != "b3":
            raise ValueError("candidate query identity drifted")
        row["query_id"] = "ldd-" + "-".join(parts[1:])
        row["volume_index"] = int(parts[3][1:])
        row["mixing_index"] = int(parts[4][1:])
        pool.append(row)
    if len(pool) != 128 or len({str(item["query_id"]) for item in pool}) != 128:
        raise ValueError("longitudinal decision candidate pool differs from 128")
    return pool


def _stable_key(namespace: str, packet_seed: int, value: str) -> str:
    payload = f"{namespace}:{packet_seed}:{value}".encode()
    return hashlib.sha256(payload).hexdigest()


def select_outcome_blind_packet(
    candidates: Sequence[Mapping[str, Any]],
    *,
    packet_seed: int,
    namespace: str,
) -> list[dict[str, Any]]:
    by_coordinate = {
        (
            str(item["pair_id"]),
            int(item["volume_index"]),
            int(item["mixing_index"]),
        ): item
        for item in candidates
    }
    pair_ids = sorted({str(item["pair_id"]) for item in candidates})
    if len(pair_ids) != 16:
        raise ValueError("longitudinal decision requires sixteen candidate pairs")
    ordered_pairs = sorted(
        pair_ids,
        key=lambda pair_id: (_stable_key(namespace, packet_seed, pair_id), pair_id),
    )[:8]
    rotation = packet_seed % 4
    packet: list[dict[str, Any]] = []
    for index, pair_id in enumerate(ordered_pairs):
        volume_index = (index + rotation) % 4
        mixing_index = (index + packet_seed) % 2
        candidate = by_coordinate.get((pair_id, volume_index, mixing_index))
        if candidate is None:
            raise ValueError("outcome-blind candidate coordinate is unavailable")
        packet.append(deepcopy(dict(candidate)))
    coverage = candidate_packet_coverage(packet)
    if coverage != {
        "candidate_count": 8,
        "distinct_pair_count": 8,
        "volume_index_counts": {0: 2, 1: 2, 2: 2, 3: 2},
        "mixing_index_counts": {0: 4, 1: 4},
    }:
        raise ValueError("outcome-blind candidate packet coverage drifted")
    return packet


def candidate_packet_coverage(packet: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "candidate_count": len(packet),
        "distinct_pair_count": len({str(item["pair_id"]) for item in packet}),
        "volume_index_counts": dict(
            sorted(Counter(int(item["volume_index"]) for item in packet).items())
        ),
        "mixing_index_counts": dict(
            sorted(Counter(int(item["mixing_index"]) for item in packet).items())
        ),
    }


def build_decision_design(
    protocol_path: str | Path,
    *,
    repository_root: str | Path,
) -> dict[str, Any]:
    root = Path(repository_root).resolve()
    protocol_file, protocol = load_decision_protocol(
        protocol_path,
        repository_root=root,
    )
    runtime = _load(_resolve(root, protocol["runtime_config"], field="runtime_config"))
    if runtime.get("campaign", {}).get("complete_experiments") != 12:
        raise ValueError("runtime does not implement twelve experiments")
    if runtime.get("campaign", {}).get("checkpoint_complete_experiments") != [0, 3, 6, 9, 12]:
        raise ValueError("runtime checkpoint schedule differs from the decision protocol")
    checkpoint_hashes = _checkpoint_action_hashes(runtime)
    pool = build_candidate_pool(protocol)
    clusters: list[dict[str, Any]] = []
    cells: list[dict[str, Any]] = []
    namespace = str(protocol["candidate_packet_namespace"])
    for world_seed, packet_seed in zip(
        protocol["world_seeds"],
        protocol["candidate_packet_seeds"],
        strict=True,
    ):
        packet = select_outcome_blind_packet(
            pool,
            packet_seed=int(packet_seed),
            namespace=namespace,
        )
        plans = {
            str(item["query_id"]): compile_evaluator_truth_query(runtime, item)
            for item in packet
        }
        if checkpoint_hashes.intersection(
            str(plan["action_plan_sha256"]) for plan in plans.values()
        ):
            raise ValueError("decision candidate collides with a checkpoint truth query")
        contract = build_terminal_contract(
            study_id=str(protocol["study_id"]),
            world_seed=int(world_seed),
            candidates=packet,
            prediction_mode="ranking_only",
        )
        cluster_id = f"A_S_LDD--partition-discovery--seed{world_seed}"
        cluster = {
            "cluster_id": cluster_id,
            "world_seed": int(world_seed),
            "candidate_packet_seed": int(packet_seed),
            "candidate_selection_uses_hidden_truth": False,
            "candidate_selection_uses_hidden_rank": False,
            "candidate_packet_coverage": candidate_packet_coverage(packet),
            "terminal_action_readout": contract,
            "candidate_action_plan_sha256": {
                query_id: str(plan["action_plan_sha256"])
                for query_id, plan in plans.items()
            },
        }
        clusters.append(cluster)
        for arm in ARMS:
            cells.append(
                {
                    "cell_id": f"{cluster_id}--{arm}",
                    "cluster_id": cluster_id,
                    "world_seed": int(world_seed),
                    "arm": arm,
                    "terminal_action_readout": deepcopy(contract),
                }
            )
    design: dict[str, Any] = {
        "schema_version": DESIGN_VERSION,
        "study_id": protocol["study_id"],
        "status": "design_materialized_provider_execution_not_authorized",
        "protocol_path": protocol_file.relative_to(root).as_posix(),
        "protocol_sha256": canonical_json_sha256(protocol),
        "cluster_count": 5,
        "cell_count": 15,
        "participant_physical_experiment_count": 180,
        "candidate_truth_execution_count": 40,
        "checkpoint_truth_execution_count": 80,
        "provider_free_truth_execution_count": 120,
        "provider_free_exact_replay_count": 120,
        "provider_execution_authorized": False,
        "candidate_selection_uses_hidden_truth": False,
        "candidate_selection_uses_hidden_rank": False,
        "clusters": clusters,
        "cells": cells,
    }
    design["design_sha256"] = canonical_json_sha256(design)
    return design


__all__ = [
    "DESIGN_VERSION",
    "PROTOCOL_VERSION",
    "build_candidate_pool",
    "build_decision_design",
    "candidate_packet_coverage",
    "load_decision_protocol",
    "select_outcome_blind_packet",
]
