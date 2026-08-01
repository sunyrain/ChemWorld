"""Calibrate known/unknown/mismatched G2 campaign resource designs offline."""

# ruff: noqa: RUF001 -- Chinese report strings intentionally use Chinese punctuation.

from __future__ import annotations

import argparse
import json
import statistics
from collections.abc import Mapping, Sequence
from copy import deepcopy
from pathlib import Path
from typing import Any

import numpy as np

import chemworld  # noqa: F401
from chemworld.agents.g2_triarm_calibration import (
    G2CalibrationPolicy,
    G2TriarmCalibrationAgent,
)
from chemworld.campaign_resources import generous_electrochemical_max_envelope_card
from chemworld.data.logging import load_jsonl
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic
from chemworld.eval.runner import run_agent
from chemworld.eval.static_optimization_seeds import exploration_observation_seed
from chemworld.eval.verify import verify_records
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = (
    ROOT
    / "configs/benchmark/"
    "g2_autonomous_electrochemical_material_5x3_design_v0.1_dev.json"
)
DEFAULT_OUTPUT_ROOT = (
    ROOT / "runs/development/g2-triarm-resource-design-calibration-v1"
)
DEFAULT_REPORT = (
    ROOT / "workstreams/G2_TRIARM_RESOURCE_DESIGN_RESULTS_ZH.md"
)
ARMS = ("unknown", "known", "mismatched")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument(
        "--design",
        action="append",
        default=[],
        help="Run only the named resource design; repeat to select multiple.",
    )
    parser.add_argument(
        "--world-seeds",
        help="Comma-separated override for development screening seeds.",
    )
    return parser


def _load_protocol(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != (
        "chemworld-g2-autonomous-material-triarm-design-0.1"
    ):
        raise ValueError("unsupported G2 tri-arm resource-design protocol")
    conditions = payload.get("conditions")
    if not isinstance(conditions, list):
        raise ValueError("tri-arm protocol conditions must be a list")
    arms = [str(item.get("arm_id")) for item in conditions if isinstance(item, Mapping)]
    if tuple(arms) != ARMS:
        raise ValueError(f"tri-arm protocol arms must be {list(ARMS)}")
    designs = payload.get("resource_designs")
    if not isinstance(designs, list) or not designs:
        raise ValueError("tri-arm protocol requires resource designs")
    return payload


def _condition_map(protocol: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(item["arm_id"]): deepcopy(dict(item))
        for item in protocol["conditions"]
    }


def _designs(
    protocol: Mapping[str, Any],
    selected: Sequence[str],
) -> list[dict[str, Any]]:
    rows = [deepcopy(dict(item)) for item in protocol["resource_designs"]]
    if not selected:
        return rows
    requested = set(selected)
    available = {str(item["design_id"]) for item in rows}
    unknown = sorted(requested - available)
    if unknown:
        raise ValueError(f"unknown resource designs: {unknown}")
    return [item for item in rows if str(item["design_id"]) in requested]


def _arm_order(protocol: Mapping[str, Any], seed: int) -> list[str]:
    schedule = protocol["execution_order"]["order_by_seed_mod_3"]
    order = schedule[str(seed % 3)]
    if sorted(order) != sorted(ARMS):
        raise ValueError("each tri-arm schedule row must contain all arms")
    return [str(item) for item in order]


def _policy(design: Mapping[str, Any]) -> G2CalibrationPolicy:
    policy = design["policy"]
    return G2CalibrationPolicy(
        policy_id=str(design["design_id"]),
        diagnostic_instrument=(
            None
            if policy.get("diagnostic_instrument") is None
            else str(policy["diagnostic_instrument"])
        ),
        adapted_second_stage=policy.get("adapted_second_stage") is True,
    )


def _run_cell(
    *,
    protocol: Mapping[str, Any],
    design: Mapping[str, Any],
    condition: Mapping[str, Any],
    world_seed: int,
    cell_root: Path,
) -> dict[str, Any]:
    if cell_root.exists():
        raise FileExistsError(f"refusing to overwrite calibration cell: {cell_root}")
    cell_root.mkdir(parents=True)
    task = protocol["task"]
    batch_count = int(design["batch_count"])
    operation_limit = int(design["operation_attempt_limit"])
    nonfinal_limit = int(design["nonfinal_instrument_use_limit"])
    policy = _policy(design)
    if operation_limit < batch_count * policy.operations_per_completed_batch:
        raise ValueError(
            f"{design['design_id']} cannot close all batches under its operation limit"
        )
    card = generous_electrochemical_max_envelope_card(
        experiment_count=batch_count,
        operation_attempt_limit=operation_limit,
        nonfinal_instrument_use_limit=nonfinal_limit,
        stock_action_envelopes_per_experiment=float(
            design["stock_action_envelopes_per_batch"]
        ),
        card_id=f"g2-triarm-{design['design_id']}",
    )
    agent = G2TriarmCalibrationAgent(policy)
    trajectory = cell_root / "trajectory.jsonl"
    history = run_agent(
        env_id=get_task(str(task["task_id"])).env_id,
        agent=agent,
        world_split=str(task["world_split"]),
        budget=operation_limit,
        objective=str(task["objective"]),
        seed=world_seed,
        agent_seed=world_seed,
        observation_seed=exploration_observation_seed(
            str(task["task_id"]),
            world_seed,
        ),
        task_id=str(task["task_id"]),
        output_path=trajectory,
        budget_override=operation_limit,
        episode_mode_override=str(task["episode_mode"]),
        method_resource_limits={
            "operation_limit": operation_limit,
            "complete_experiment_limit": batch_count,
            "checkpoint_complete_experiments": tuple(
                range(1, batch_count + 1)
            ),
            "training_environment_step_limit": 0,
        },
        evaluation_policy="task_contract",
        material_information=deepcopy(dict(condition["material_information"])),
        electrochemical_material_family_id=str(
            task["electrochemical_material_family_id"]
        ),
        electrochemical_workflow_mode=str(
            task["electrochemical_workflow_mode"]
        ),
        scoring_contract_id=str(task["scoring_contract_id"]),
        observation_noise_mode=str(task["observation_noise_mode"]),
        observation_noise_namespace=str(
            task["observation_noise_namespace"]
        ),
        campaign_resource_card=card.to_dict(),
    )
    records = load_jsonl(trajectory)
    verification = verify_records(records)
    terminal = [record for record in history if record.event_type == "experiment_end"]
    scores = [
        float(record.info["leaderboard_score"])
        for record in terminal
        if record.info.get("leaderboard_score") is not None
    ]
    incumbent = 0.0
    curve = []
    for record in history:
        score = record.info.get("leaderboard_score")
        if isinstance(score, int | float) and not isinstance(score, bool):
            incumbent = max(incumbent, float(score))
        curve.append(incumbent)
    last_resources = (
        history[-1].info.get("campaign_resources", {}) if history else {}
    )
    resource_state = (
        last_resources.get("state", {})
        if isinstance(last_resources, Mapping)
        else {}
    )
    selected_pairs = agent.manifest()["selected_pairs"]
    summary = {
        "schema_version": "chemworld-g2-triarm-calibration-cell-0.1",
        "design_id": design["design_id"],
        "arm_id": condition["arm_id"],
        "condition_id": condition["condition_id"],
        "world_seed": world_seed,
        "batch_target": batch_count,
        "closed_batch_count": len(terminal),
        "lifecycle_completed": len(terminal) == batch_count,
        "operation_count": len(history),
        "operation_attempt_limit": operation_limit,
        "operation_utilization": len(history) / operation_limit,
        "final_scores": scores,
        "best_final_score": max(scores) if scores else None,
        "mean_final_score": statistics.fmean(scores) if scores else None,
        "incumbent_auc_per_operation": (
            statistics.fmean(curve) if curve else None
        ),
        "selected_pairs": selected_pairs,
        "selected_solvents": [int(pair[1]) for pair in selected_pairs],
        "selected_electrolytes": [int(pair[0]) for pair in selected_pairs],
        "first_solvent": int(selected_pairs[0][1]),
        "last_solvent": int(selected_pairs[-1][1]),
        "late_minus_early_score": _late_minus_early(scores),
        "invalid_operation_count": sum(
            record.info.get("transaction_status") != "committed"
            for record in history
        ),
        "resource_state": resource_state,
        "campaign_resource_card": card.to_dict(),
        "exact_replay_verified": verification.verified,
        "exact_replay_mismatches": verification.mismatches,
        "trajectory_sha256": file_sha256(trajectory),
        "agent_manifest": agent.manifest(),
    }
    write_json_atomic(cell_root / "cell_summary.json", summary)
    return summary


def _late_minus_early(scores: Sequence[float]) -> float | None:
    if len(scores) < 2:
        return None
    split = max(len(scores) // 2, 1)
    return statistics.fmean(scores[split:]) - statistics.fmean(scores[:split])


def _mean(values: Sequence[float]) -> float:
    return statistics.fmean(values) if values else 0.0


def _summary(values: Sequence[float]) -> dict[str, Any]:
    numeric = [float(item) for item in values]
    return {
        "count": len(numeric),
        "mean": _mean(numeric),
        "minimum": min(numeric) if numeric else None,
        "maximum": max(numeric) if numeric else None,
        "values": numeric,
    }


def _contrast(
    left: Mapping[int, Mapping[str, Any]],
    right: Mapping[int, Mapping[str, Any]],
    key: str,
) -> dict[str, Any]:
    seeds = sorted(set(left) & set(right))
    values = [float(left[seed][key]) - float(right[seed][key]) for seed in seeds]
    return {
        **_summary(values),
        "paired_world_seeds": seeds,
        "bootstrap_95_interval": _bootstrap_interval(values),
        "win_tie_loss": {
            "wins": sum(value > 1.0e-12 for value in values),
            "ties": sum(abs(value) <= 1.0e-12 for value in values),
            "losses": sum(value < -1.0e-12 for value in values),
        },
    }


def _bootstrap_interval(values: Sequence[float]) -> list[float] | None:
    if not values:
        return None
    array = np.asarray(values, dtype=float)
    rng = np.random.default_rng(20260731)
    indices = rng.integers(0, len(array), size=(20_000, len(array)))
    means = array[indices].mean(axis=1)
    return [float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))]


def _aggregate_design(
    design: Mapping[str, Any],
    cells: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    by_arm = {
        arm: {
            int(cell["world_seed"]): cell
            for cell in cells
            if cell["arm_id"] == arm
        }
        for arm in ARMS
    }
    arm_summary = {}
    for arm in ARMS:
        rows = list(by_arm[arm].values())
        arm_summary[arm] = {
            "cell_count": len(rows),
            "lifecycle_completion_rate": _mean(
                [float(row["lifecycle_completed"]) for row in rows]
            ),
            "best_final_score": _summary(
                [float(row["best_final_score"]) for row in rows]
            ),
            "mean_final_score": _summary(
                [float(row["mean_final_score"]) for row in rows]
            ),
            "incumbent_auc_per_operation": _summary(
                [float(row["incumbent_auc_per_operation"]) for row in rows]
            ),
            "operation_utilization": _summary(
                [float(row["operation_utilization"]) for row in rows]
            ),
            "first_solvent_values": [int(row["first_solvent"]) for row in rows],
            "last_solvent_values": [int(row["last_solvent"]) for row in rows],
            "late_minus_early_score": _summary(
                [
                    float(row["late_minus_early_score"])
                    for row in rows
                    if row["late_minus_early_score"] is not None
                ]
            ),
        }
    contrasts = {
        "known_minus_unknown": _contrast(
            by_arm["known"], by_arm["unknown"], "best_final_score"
        ),
        "mismatched_minus_known": _contrast(
            by_arm["mismatched"], by_arm["known"], "best_final_score"
        ),
        "mismatched_minus_unknown": _contrast(
            by_arm["mismatched"], by_arm["unknown"], "best_final_score"
        ),
    }
    mismatch_rows = list(by_arm["mismatched"].values())
    known_rows = list(by_arm["known"].values())
    lifecycle_pass = all(cell["lifecycle_completed"] for cell in cells)
    replay_pass = all(cell["exact_replay_verified"] for cell in cells)
    manipulation_rate = _mean(
        [float(row["first_solvent"] == 3) for row in mismatch_rows]
    )
    known_adherence_rate = _mean(
        [float(row["first_solvent"] == 1) for row in known_rows]
    )
    recovery_rate = _mean(
        [float(row["last_solvent"] != 3) for row in mismatch_rows]
    )
    recovery_gain = arm_summary["mismatched"]["late_minus_early_score"]["mean"]
    manipulation_visible = manipulation_rate >= 0.8 and known_adherence_rate >= 0.8
    recovery_visible = recovery_rate >= 0.6 and recovery_gain > 0.0
    operation_limit = int(design["operation_attempt_limit"])
    mean_best = _mean(
        [float(cell["best_final_score"]) for cell in cells]
    )
    return {
        "design": deepcopy(dict(design)),
        "cell_count": len(cells),
        "all_lifecycles_completed": lifecycle_pass,
        "all_exact_replays_verified": replay_pass,
        "arm_summary": arm_summary,
        "paired_best_score_contrasts": contrasts,
        "wrong_prior": {
            "mismatched_first_transposed_solvent_rate": manipulation_rate,
            "known_first_nominal_solvent_rate": known_adherence_rate,
            "mismatched_late_leaves_transposed_solvent_rate": recovery_rate,
            "mismatched_late_minus_early_score_mean": recovery_gain,
            "manipulation_visible": manipulation_visible,
            "recovery_visible": recovery_visible,
        },
        "resource_efficiency": {
            "mean_best_score_all_arms": mean_best,
            "score_per_hard_operation_slot": mean_best / operation_limit,
            "mean_operation_utilization": _mean(
                [float(cell["operation_utilization"]) for cell in cells]
            ),
            "unused_operation_fraction": 1.0
            - _mean([float(cell["operation_utilization"]) for cell in cells]),
        },
        "selection_gates": {
            "lifecycle": lifecycle_pass,
            "exact_replay": replay_pass,
            "manipulation_visibility": manipulation_visible,
            "recovery_visibility": recovery_visible,
        },
    }


def _select_design(designs: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    passing = [
        item
        for item in designs
        if all(item["selection_gates"].values())
    ]
    candidates = passing or list(designs)
    selected = min(
        candidates,
        key=lambda item: (
            int(item["design"]["operation_attempt_limit"]),
            -float(item["resource_efficiency"]["score_per_hard_operation_slot"]),
            float(item["resource_efficiency"]["unused_operation_fraction"]),
        ),
    )
    return {
        "selected_design_id": selected["design"]["design_id"],
        "all_selection_gates_passed": all(
            selected["selection_gates"].values()
        ),
        "selection_rule": (
            "smallest hard operation envelope passing lifecycle, replay, "
            "wrong-prior manipulation, and recovery visibility"
        ),
        "selected_design": selected,
    }


def _render_report(summary: Mapping[str, Any]) -> str:
    lines = [
        "# G2 已知／未知／错配三臂资源设计实验",
        "",
        "状态：离线、逐操作、精确回放的设计标定；不使用外部模型调用。",
        "",
        "## 候选设计",
        "",
        "| 设计 | batch | hard operations | 诊断上限 | 两阶段 | 生命周期 | "
        "错配操纵 | 错配恢复 | 平均利用率 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for item in summary["design_results"]:
        design = item["design"]
        gates = item["selection_gates"]
        wrong = item["wrong_prior"]
        lines.append(
            f"| {design['design_id']} | {design['batch_count']} | "
            f"{design['operation_attempt_limit']} | "
            f"{design['nonfinal_instrument_use_limit']} | "
            f"{'是' if design['policy']['adapted_second_stage'] else '否'} | "
            f"{'通过' if gates['lifecycle'] else '失败'} | "
            f"{wrong['mismatched_first_transposed_solvent_rate']:.0%} | "
            f"{wrong['mismatched_late_leaves_transposed_solvent_rate']:.0%} | "
            f"{item['resource_efficiency']['mean_operation_utilization']:.0%} |"
        )
    selected = summary["selection"]
    lines.extend(
        [
            "",
            "## 推荐",
            "",
            f"推荐设计：`{selected['selected_design_id']}`。",
            "",
            "选择原则不是最高单次分数，而是用最小资源同时证明：完整生命周期、"
            "正确信息的行为影响、错配信息的初始操纵，以及后期基于实验结果的纠错。",
            "",
            "## 三臂定义",
            "",
            "- 未知：只有匿名 action codes。",
            "- 已知：正确匿名 nominal properties。",
            "- 错配：Agent 不知情地交换 solvent-S1 与 solvent-S3 的整行属性；物理世界不变。",
            "",
            "## 评价建议",
            "",
            "主评价使用 paired-world best final score 与 operation-normalized incumbent AUC；"
            "同时把 first material choice、late material choice、lifecycle completion、"
            "invalid/resource rejection 和账本利用率作为共同必要的行为证据。只看最终最高分"
            "会遗漏错配先验是否真正影响过 Agent，也无法区分恢复与偶然命中。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = _parser().parse_args()
    config_path = args.config.resolve()
    output_root = args.output_root.resolve()
    report_path = args.report.resolve()
    if output_root.exists():
        raise FileExistsError(f"refusing to overwrite output root: {output_root}")
    protocol = _load_protocol(config_path)
    seeds = (
        [int(item) for item in args.world_seeds.split(",")]
        if args.world_seeds
        else [int(item) for item in protocol["task"]["world_seeds"]]
    )
    designs = _designs(protocol, args.design)
    conditions = _condition_map(protocol)
    output_root.mkdir(parents=True)
    all_design_results = []
    for design in designs:
        design_id = str(design["design_id"])
        cells = []
        for seed in seeds:
            for arm in _arm_order(protocol, seed):
                print(
                    json.dumps(
                        {"design_id": design_id, "world_seed": seed, "arm": arm},
                        sort_keys=True,
                    ),
                    flush=True,
                )
                cell = _run_cell(
                    protocol=protocol,
                    design=design,
                    condition=conditions[arm],
                    world_seed=seed,
                    cell_root=(
                        output_root
                        / design_id
                        / f"world-{seed:02d}-{arm}"
                    ),
                )
                cells.append(cell)
        design_result = _aggregate_design(design, cells)
        write_json_atomic(
            output_root / design_id / "design_summary.json",
            design_result,
        )
        all_design_results.append(design_result)
    selection = _select_design(all_design_results)
    summary = {
        "schema_version": "chemworld-g2-triarm-resource-design-result-0.1",
        "status": "completed_offline_design_calibration",
        "formal_result": False,
        "external_model_calls": 0,
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": canonical_json_sha256(protocol),
        "config_path": str(config_path),
        "world_seeds": seeds,
        "arms": list(ARMS),
        "mismatch_freeze": protocol["mismatch_freeze"],
        "design_results": all_design_results,
        "selection": selection,
        "reporting_boundary": (
            "Calibration-agent results select a resource/evaluation protocol; "
            "they are not evidence of Codex scientific performance."
        ),
    }
    write_json_atomic(output_root / "resource_design_summary.json", summary)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(_render_report(summary), encoding="utf-8")
    print(
        json.dumps(
            {
                "summary": str(output_root / "resource_design_summary.json"),
                "report": str(report_path),
                "selected_design_id": selection["selected_design_id"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
