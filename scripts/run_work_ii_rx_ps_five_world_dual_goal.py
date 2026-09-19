#!/usr/bin/env python3
"""Run the frozen RX P/S five-world, three-arm, dual-goal Work II block."""
# ruff: noqa: RUF001, E402, E501, C420

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import shutil
import sys
import tempfile
import threading
import time
from collections.abc import Mapping, Sequence
from dataclasses import replace
from pathlib import Path
from statistics import fmean
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.run_work_ii_ec_dual_goal_trial as shared
import scripts.run_work_ii_rx_p_opaque_dual_goal_canary as rx_canary
from scripts.author_experiment_1_rx_structural_redesign import reversible_intervention

from chemworld.campaign_resources import CampaignResourceCard
from chemworld.data.logging import load_jsonl
from chemworld.envs.observation_noise import ObservationNoiseCoordinate
from chemworld.eval.experiment_1_rx_qualification import (
    load_contract as load_rx_contract,
)
from chemworld.eval.experiment_1_rx_qualification import structural_prior_arms
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_catalyst_deactivation_q0 import (
    DIRECT_METRICS,
    registered_cells,
)
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.tasks import get_task

CONFIG = ROOT / "configs/benchmark/work_ii_rx_ps_five_world_dual_goal_v1.0.json"
CORRECTION = ROOT / "configs/benchmark/work_ii_rx_ps_five_world_dual_goal_v1.0.1.json"
P_PACKAGE = ROOT / "configs/benchmark/work_ii_reaction_safety_matched_prior_package.json"
S_CONTRACT = ROOT / "configs/benchmark/experiment_1_rx_structural_repair_v1.1.0.json"
TASK = "reaction-safety-constrained"
PROVIDER = {
    "id": "chemworld_openai_https",
    "name": "OpenAI",
    "model": "gpt-5.6-sol",
    "reasoning_effort": "medium",
    "auth_mode": "chatgpt_subscription_cached_login",
    "wire_api": "responses",
}
METRICS = (
    "yield",
    "conversion",
    "selectivity",
    "byproduct_signal",
    "safety_risk",
    "score",
)
ARMS = ("Opaque", "Aligned", "MisIndexed")
LOCI = ("P", "S")
WORLDS = tuple((f"RX-W{index + 1:02d}", index) for index in range(5))
GOALS = {
    "mechanism_discovery": (
        "Your primary goal is to discover and test an explanatory, predictive account of this "
        "reaction and thermal system. Choose all experiments autonomously. Investigate target "
        "formation, competing conversion, catalyst effects or deactivation, actual thermal/time "
        "history, and termination or quench timing. You may propose, revise, combine, or reject "
        "mechanisms and equations freely. The public safe score is a secondary observation, not "
        "the research objective."
    ),
    "safety_constrained_optimization": (
        "Your primary goal is to find an operating procedure with strong public safe-score "
        "performance in this reaction and thermal system while respecting the declared safety "
        "limit. Choose all experiments autonomously. Use measurements and mechanistic reasoning "
        "as you find helpful."
    ),
}
SYSTEM = """You are an autonomous scientist in a simulated reaction and thermal laboratory.
Use only the supplied chemworld_lab tools and public_numerics calculator. No filesystem,
network, repository inspection, external knowledge retrieval, or hidden simulator access.
Read material_information first. The task's research_goal is authoritative for this campaign.
Complete 12 independent batches; repetition is allowed. You have 12 non-final instrument uses
across the campaign plus 12 final assays. Measurements are optional up to their budget.
Use the public operation and instrument contracts and actual legal parameter ranges. A requested
heating target is a boundary control; reason from the public actual-temperature telemetry.
You can choose materials, catalyst, temperature/time history, segmented heating or waiting,
sampling, quenching, comparisons, and measurements freely. There are no mandatory belief
snapshots, expression templates, or decision-audit fields. For every batch explicitly terminate
then measure final_assay. A batch ending is not the campaign ending: continue with the returned
next_state until campaign_ended is true. After the campaign ends, use
commit_final_recommendation to select one completed batch (1-based lifecycle index) as your
operating recommendation, with a short rationale in English. For the discovery task this
recommendation is only a secondary readout. Then return the required status/summary JSON in
English. Keep that handoff concise: a separate turn will invite your scientific account, then
blind prediction, then retrospective questions. Do not answer those early. Public scores and
diagnostics are observations; supplied prior information may be incomplete or inaccurate, and
observations are authoritative. No particular scientific result is required.
"""
K1 = """实验阶段已结束，操作建议已经封存。现在请用英文提交完整、独立可读的机理报告。
请讲清你认为这个世界如何运行：关键变量、作用关系、耦合、可能的方程或过程；哪些实验使你形成或修改这个解释；说明解释适用范围、尚不能识别的因素和合理的竞争解释。
使用你认为最合适的自然语言、数学或伪代码，不要求任何预设模型形式，也不要求确定答案。
引用真实批次编号与数值，区分实际观测、外推和猜测；不补做实验，不编造未测信息。
**请充分展开，不必压成短摘要。所有报告文本必须使用英文。**返回JSON的report字段。此报告封存后才给预测题。"""
Q_PROMPT = """请基于你自己的研究，对以下12个独立新批次的最终结果逐一盲预测。每批从相同初始世界独立开始。对每个指标给出点估计及80%预测区间，考虑不确定性；不能补做实验。所有指标沿公共仪器及评分合同。题目并未限定你解释机理的形式。不要修改先前报告。返回完整predictions及rationale；所有rationale和其他自由文本字段必须使用英文。"""
K2 = """机理报告和盲预测已经封存，尚未向你反馈任何预测真值。请用英文按1—7逐项深入复盘。
引用真实批次和K1中的具体判断；不得补做实验，不得修改已经封存的K1或Q。
请引用前文，避免重复完整实验表和整篇机理报告。允许承认不足，不要把事后解释写成实验当时已经形成的判断。

1. 初始资料中的哪些重要主张得到支持、受到反驳或仍未检验？如果初始资料没有提供实质性主张，请明确说明。区分“没有发现反证”与“已经出现反证但当时没有修正”。
2. 哪些具体实验真正形成或改变了你的判断？哪些关键实验选择主要依赖初始资料、已有数据或未经验证的猜测？
3. 当前最重要的竞争机理或竞争解释是什么？现有实验能够区分哪些、不能区分哪些？
4. 如果只允许增加一次合法的完整实验，你会选择什么条件、测量什么？不同可能结果分别会怎样改变你的判断？不要实际执行。
5. 你的实验设计在机理可辨识性与提高操作得分之间做了什么取舍？研究目标怎样影响了你的实验选择？是否存在为了优化而牺牲辨识性，或为了辨识而牺牲得分的情况？
6. 哪些已经取得的证据没有被充分利用或难以利用？哪些盲预测最不可靠，哪些预测区间可能过窄？指出它们是否与K1声明的不确定性或适用范围不一致。
7. 封存推荐操作有什么局限？如何检验其重复性、局部稳健性、跨材料或跨世界推广范围？区分“样本内最高”与“已经证明最优”。

返回JSON的report字段；report内容必须使用英文。"""


def read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def digest(payload: Any) -> str:
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def deterministic_seed(*parts: object) -> int:
    value = "|".join(str(part) for part in parts)
    return int.from_bytes(hashlib.sha256(value.encode("utf-8")).digest()[:8], "big") % 2_147_483_647


def resource_card(batches: int = 12) -> CampaignResourceCard:
    return CampaignResourceCard(
        card_id=f"rx-ps-five-world-dual-goal-{batches}",
        operation_attempt_limit=30 * batches,
        vessel_start_limit=batches,
        final_assay_limit=batches,
        nonfinal_instrument_use_limit=batches,
        stock_limits={
            "reagent_mol": 0.04 * batches,
            "solvent_L": 0.08 * batches,
            "catalyst_mol": 0.005 * batches,
        },
        process_time_limit_s=18000 * batches,
        implicit_operation_time_s={"quench": 120.0},
    )


def _base_recipe(catalyst_amount_mol: float) -> list[dict[str, Any]]:
    return [
        {"operation": "add_solvent", "solvent": 2, "volume_L": 0.005},
        {"operation": "add_reagent", "amount_mol": 0.003},
        {
            "operation": "add_catalyst",
            "catalyst": 1,
            "catalyst_amount_mol": catalyst_amount_mol,
        },
    ]


def p_queries(config: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for query in config["P_queries"]:
        actions = _base_recipe(0.000525)
        actions.extend(
            {
                "operation": "heat",
                "target_temperature_K": float(temperature),
                "duration_s": float(duration),
                "stirring_speed_rpm": 400.0,
            }
            for temperature, duration in query["thermal_history"]
        )
        if query["quench"]:
            actions.append({"operation": "quench"})
        actions.extend(
            [
                {"operation": "terminate"},
                {"operation": "measure", "instrument": "final_assay"},
            ]
        )
        rows.append({"query_id": query["query_id"], "actions": actions})
    return rows


def s_queries(config: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for query in config["S_queries"]:
        actions = _base_recipe(float(query["catalyst_amount_mol"]))
        actions.append(
            {
                "operation": "heat",
                "target_temperature_K": float(query["temperature_K"]),
                "duration_s": float(query["duration_s"]),
                "stirring_speed_rpm": 400.0,
            }
        )
        if query["quench"]:
            actions.append({"operation": "quench"})
        actions.extend(
            [
                {"operation": "terminate"},
                {"operation": "measure", "instrument": "final_assay"},
            ]
        )
        rows.append({"query_id": query["query_id"], "actions": actions})
    return rows


def queries(config: Mapping[str, Any], locus: str) -> list[dict[str, Any]]:
    rows = p_queries(config) if locus == "P" else s_queries(config)
    if len(rows) != 12 or [row["query_id"] for row in rows] != [f"Q{i:02d}" for i in range(1, 13)]:
        raise ValueError(f"{locus} query contract is not exactly Q01--Q12")
    return rows


def _p_world(package: Mapping[str, Any], world_seed: int) -> Mapping[str, Any]:
    world = next((row for row in package["worlds"] if int(row["world_seed"]) == world_seed), None)
    if world is None or world.get("qualification_passed") is not True:
        raise ValueError(f"qualified P package missing world seed {world_seed}")
    return world


def priors(
    locus: str,
    arm: str,
    world_seed: int,
    p_package: Mapping[str, Any],
    s_contract: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    material = {"mode": "opaque_codes"}
    if arm == "Opaque":
        return material, None
    if locus == "P":
        world = _p_world(p_package, world_seed)
        key = {"Aligned": "aligned_nominal", "MisIndexed": "misindexed_nominal"}[arm]
        return material, copy.deepcopy(world["prior_arms"][key]["initial_world_model"])
    arms = structural_prior_arms(s_contract)
    key = {"Aligned": "aligned", "MisIndexed": "misspecified"}[arm]
    return material, copy.deepcopy(arms[key])


def validate_design(config: Mapping[str, Any]) -> dict[str, Any]:
    if config["counts"]["independent_source_sessions"] != 60:
        raise ValueError("source session denominator changed")
    if config["counts"]["source_batches"] != 720 or config["counts"]["posttests"] != 180:
        raise ValueError("frozen denominator changed")
    p_package = read(P_PACKAGE)
    s_contract = load_rx_contract(ROOT, S_CONTRACT)
    if s_contract["task"]["truth_family"] != "deactivating_baseline":
        raise ValueError("S participant truth must remain the baseline parent")
    for locus in LOCI:
        queries(config, locus)
        for _, seed in WORLDS:
            opaque = priors(locus, "Opaque", seed, p_package, s_contract)
            aligned = priors(locus, "Aligned", seed, p_package, s_contract)
            wrong = priors(locus, "MisIndexed", seed, p_package, s_contract)
            if opaque != ({"mode": "opaque_codes"}, None):
                raise ValueError(f"{locus} opaque leaked target-locus prior")
            if locus == "P":
                if aligned[1]["context_contract"] != wrong[1]["context_contract"]:
                    raise ValueError(f"P A/M context mismatch in world seed {seed}")
                aligned_claim = aligned[1]["model"]["claim"]["expected_relation"]
                wrong_claim = wrong[1]["model"]["claim"]["expected_relation"]
                if aligned_claim == wrong_claim:
                    raise ValueError(f"P A/M target claims do not differ in world seed {seed}")
                matched_a = copy.deepcopy(aligned[1])
                matched_m = copy.deepcopy(wrong[1])
                matched_a["model"]["claim"].pop("expected_relation")
                matched_m["model"]["claim"].pop("expected_relation")
                if matched_a != matched_m:
                    raise ValueError(f"P A/M differ outside the target claim in world seed {seed}")
            else:
                comparable_a = {k: v for k, v in aligned[1].items() if k != "claim"}
                comparable_m = {k: v for k, v in wrong[1].items() if k != "claim"}
                if comparable_a != comparable_m or aligned[1]["claim"] == wrong[1]["claim"]:
                    raise ValueError("S A/M arms are not matched except for the claim")
    schedule = [
        {
            "cell_id": f"{world_id}--{locus}--{goal}--{arm}",
            "world_id": world_id,
            "world_seed": seed,
            "locus": locus,
            "goal": goal,
            "arm": arm,
        }
        for world_id, seed in WORLDS
        for locus in LOCI
        for goal in GOALS
        for arm in ARMS
    ]
    if len(schedule) != 60 or len({row["cell_id"] for row in schedule}) != 60:
        raise ValueError("schedule does not contain 60 unique cells")
    return {
        "schedule": schedule,
        "p_package": p_package,
        "s_contract": s_contract,
        "query_sha256": {locus: digest(queries(config, locus)) for locus in LOCI},
    }


def configure_shared_helpers() -> None:
    shared.TASK = TASK
    shared.PROVIDER = PROVIDER
    shared.METRICS = list(METRICS)
    shared.GOALS = GOALS
    shared.SYSTEM = SYSTEM
    shared.K1 = K1
    shared.K2 = K2
    shared.resource_card = resource_card
    shared.build_command = rx_canary.build_command


def physics(
    agent: Any,
    output: Path,
    *,
    world_seed: int,
    batches: int = 12,
    material: Mapping[str, Any] | None = None,
    observation_seed: int = 0,
    observation_namespace: str,
    callback: Any = None,
    source_envelope: bool = False,
) -> Any:
    operation_budget = 360 if source_envelope else 30 * batches
    card = (
        replace(
            resource_card(),
            card_id="rx-ps-source-envelope-single-retest",
            vessel_start_limit=1,
            final_assay_limit=1,
        )
        if source_envelope
        else resource_card(batches)
    )
    return run_agent(
        env_id=get_task(TASK).env_id,
        agent=agent,
        task_id=TASK,
        world_split="public-test",
        objective="safe",
        seed=world_seed,
        agent_seed=world_seed,
        observation_seed=observation_seed,
        budget=operation_budget,
        budget_override=operation_budget,
        episode_mode_override="campaign" if batches > 1 else "single_experiment",
        campaign_resource_card=card,
        material_information=dict(material or {"mode": "opaque_codes"}),
        observation_noise_mode="keyed",
        observation_noise_namespace=observation_namespace,
        output_path=output,
        step_callback=callback,
        method_resource_limits=(
            {
                "operation_limit": 30 * batches,
                "complete_experiment_limit": batches,
                "wall_time_limit_s": 5700,
                "model_call_limit": 1,
                "input_token_limit": 8_000_000,
                "uncached_input_token_limit": 2_000_000,
                "output_token_limit": 128_000,
                "training_environment_step_limit": 0,
            }
            if isinstance(agent, rx_canary.RxFreeResearchAgent)
            else None
        ),
    )


def _reference_run(
    folder: Path,
    actions: list[dict[str, Any]],
    *,
    world_seed: int,
    observation_seed: int,
    observation_namespace: str,
    batches: int = 1,
    source_envelope: bool = False,
) -> dict[str, Any]:
    result_path = folder / "result.json"
    if result_path.exists():
        return read(result_path)
    folder.mkdir(parents=True, exist_ok=False)
    failure = None
    try:
        physics(
            _FrozenTruthReplayAgent(actions),
            folder / "trajectory.jsonl",
            world_seed=world_seed,
            batches=batches,
            observation_seed=observation_seed,
            observation_namespace=observation_namespace,
            source_envelope=source_envelope,
            callback=lambda record, trace: print(
                json.dumps(
                    {
                        "stage": folder.name,
                        "operation": record.step,
                        "planned_operations": len(actions),
                    }
                ),
                flush=True,
            ),
        )
    except Exception as exc:  # retained as engineering evidence
        failure = {"type": type(exc).__name__, "message": str(exc)[:1600]}
    records = load_jsonl(folder / "trajectory.jsonl") if (folder / "trajectory.jsonl").exists() else []
    replay = shared.replay_with_progress(records, folder.name) if records else {"verified": False}
    result = {
        "failure": failure,
        "batches": shared.summaries(records),
        "exact_replay": replay,
        "operation_attempts": len(records),
        "rollbacks": [
            index + 1
            for index, row in enumerate(records)
            if row.get("transaction_status") != "committed"
        ],
    }
    write(result_path, result)
    return result


def _with_hplc(query_actions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    actions = copy.deepcopy(list(query_actions))
    terminate_index = next(index for index, row in enumerate(actions) if row["operation"] == "terminate")
    actions.insert(terminate_index, {"operation": "measure", "instrument": "hplc"})
    return actions


def engineering_gate(root: Path, config: Mapping[str, Any]) -> dict[str, Any]:
    reports = {}
    for locus in LOCI:
        actions = [action for query in queries(config, locus) for action in _with_hplc(query["actions"])]
        report = _reference_run(
            root / "engineering" / locus,
            actions,
            world_seed=0,
            observation_seed=deterministic_seed("rx-ps-engineering", locus),
            observation_namespace=f"work-ii-rx-ps-engineering-{locus.lower()}",
            batches=12,
        )
        if (
            report["failure"]
            or len(report["batches"]) != 12
            or report["rollbacks"]
            or report["exact_replay"].get("verified") is not True
        ):
            raise RuntimeError(f"{locus} engineering path failed; provider block remains sealed")
        reports[locus] = report
    return reports


def _s_gate_actions(cell: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"operation": "add_solvent", "volume_L": 0.025, "solvent": 0},
        {"operation": "add_reagent", "amount_mol": 0.015},
        {
            "operation": "add_catalyst",
            "catalyst_amount_mol": float(cell["catalyst_amount_mol"]),
            "catalyst": 1,
        },
        {
            "operation": "heat",
            "target_temperature_K": float(cell["temperature_K"]),
            "duration_s": float(cell["duration_s"]),
            "stirring_speed_rpm": 675.0,
        },
        {"operation": "quench"},
        {"operation": "measure", "instrument": "hplc"},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


def _direct_measurement(records: Sequence[Mapping[str, Any]]) -> tuple[dict[str, float], dict[str, bool]]:
    rows = [
        row
        for row in records
        if row.get("transaction_status") == "committed"
        and row.get("operation_type") == "measure"
        and row.get("instrument") == "hplc"
    ]
    if len(rows) != 1:
        raise ValueError("S start-gate execution lacks exactly one committed HPLC measurement")
    estimates = rows[0].get("processed_estimate")
    masks = rows[0].get("observed_mask")
    if not isinstance(estimates, Mapping) or not isinstance(masks, Mapping):
        raise ValueError("S start-gate HPLC payload is malformed")
    values = {metric: float(estimates[metric]) for metric in DIRECT_METRICS}
    observed = {metric: masks.get(metric) is True for metric in DIRECT_METRICS}
    if not all(math.isfinite(value) for value in values.values()) or not all(observed.values()):
        raise ValueError("S start-gate direct metrics are not finite and visible")
    return values, observed


def _s_gate_execution(
    folder: Path,
    *,
    world_seed: int,
    cell: Mapping[str, Any],
    law_id: str,
    replicate: int,
) -> dict[str, Any]:
    result_path = folder / "result.json"
    if result_path.exists():
        return read(result_path)
    folder.mkdir(parents=True, exist_ok=False)
    actions = _s_gate_actions(cell)
    observation_seed = deterministic_seed(
        "rx-ps-s-start-gate-v1", world_seed, cell["cell_id"], replicate
    )
    namespace = f"work-ii-rx-ps-s-gate-w{world_seed}-{cell['cell_id']}-r{replicate:02d}"
    interventions = [] if law_id == "deactivating_baseline" else [reversible_intervention()]
    failure = None
    records: list[dict[str, Any]] = []
    replay: dict[str, Any] = {"verified": False}
    direct_metrics = None
    direct_mask = None
    try:
        run_agent(
            env_id=get_task(TASK).env_id,
            agent=_FrozenTruthReplayAgent(actions),
            world_split="public-test",
            budget=len(actions),
            objective="safe",
            seed=world_seed,
            agent_seed=0,
            observation_seed=observation_seed,
            task_id=TASK,
            output_path=folder / "trajectory.jsonl",
            budget_override=len(actions),
            episode_mode_override="single_experiment",
            observation_noise_mode="keyed",
            observation_noise_namespace=namespace,
            world_interventions=interventions,
        )
        records = load_jsonl(folder / "trajectory.jsonl")
        rollbacks = [row for row in records if row.get("transaction_status") != "committed"]
        if rollbacks:
            raise ValueError(f"S start-gate rollback: {rollbacks[0].get('rollback_reason')}")
        replay = verify_records(records, tolerance=0.0, world_interventions=interventions).to_dict()
        if replay.get("verified") is not True:
            raise ValueError("S start-gate exact replay failed")
        direct_metrics, direct_mask = _direct_measurement(records)
    except Exception as exc:
        failure = {"type": type(exc).__name__, "message": str(exc)[:1600]}
        if (folder / "trajectory.jsonl").exists() and not records:
            records = load_jsonl(folder / "trajectory.jsonl")
    noise_key = ObservationNoiseCoordinate(
        namespace=namespace,
        base_observation_seed=observation_seed,
        experiment_index=0,
        operation_type="measure",
        instrument="hplc",
        replicate_index=0,
    ).key_sha256
    result = {
        "cell_id": cell["cell_id"],
        "world_seed": world_seed,
        "law_id": law_id,
        "replicate": replicate,
        "status": "completed" if failure is None else "platform_failure",
        "failure": failure,
        "direct_metrics": direct_metrics,
        "direct_observed_mask": direct_mask,
        "direct_noise_key_sha256": noise_key,
        "observation_namespace": namespace,
        "observation_seed_sha256": hashlib.sha256(str(observation_seed).encode()).hexdigest(),
        "action_plan_sha256": digest(actions),
        "exact_replay": replay.get("verified") is True,
        "operation_attempts": len(records),
    }
    write(result_path, result)
    print(
        json.dumps(
            {
                "stage": "S_start_gate",
                "world_seed": world_seed,
                "action": cell["cell_id"],
                "law": law_id,
                "replicate": replicate,
                "status": result["status"],
            }
        ),
        flush=True,
    )
    return result


def _rx_structural_trace_direction_corrected(
    rows: Sequence[Mapping[str, Any]], policy: Mapping[str, Any]
) -> dict[str, Any]:
    """Apply the v1.0.1 parent-minus-child accumulation estimand."""

    grouped: dict[tuple[str, str], list[Mapping[str, Any]]] = {}
    for row in rows:
        if row.get("status") == "completed":
            grouped.setdefault((str(row["cell_id"]), str(row["law_id"])), []).append(row)
    action_ids = [str(value) for value in policy["ordered_action_ids"]]
    metrics = ("yield", "conversion", "selectivity")
    gaps: list[dict[str, float]] = []
    steps = []
    default_information = 0.0
    repeated_noise_support = {}
    offline = []
    for index, action_id in enumerate(action_ids, 1):
        baseline_rows = grouped.get((action_id, "deactivating_baseline"), [])
        target_rows = grouped.get((action_id, "reversible_target_pathway"), [])
        if not baseline_rows or not target_rows:
            raise ValueError("RX-S action lacks one of the frozen candidate families")
        target_noise_keys = {str(row.get("direct_noise_key_sha256")) for row in target_rows}
        if "None" in target_noise_keys or len(target_noise_keys) != len(target_rows):
            raise ValueError("RX-S target observations lack unique raw noise identities")
        repeated_noise_support[action_id] = len(target_noise_keys)
        target_means = {
            metric: fmean(float(row["direct_metrics"][metric]) for row in target_rows)
            for metric in metrics
        }
        baseline_predictions = {
            metric: fmean(float(row["direct_metrics"][metric]) for row in baseline_rows)
            for metric in metrics
        }
        gap = {
            metric: baseline_predictions[metric] - target_means[metric]
            for metric in metrics
        }
        gaps.append(gap)
        information = sum(abs(value) for value in gap.values())
        accumulation = (
            min(gap[metric] - gaps[0][metric] for metric in ("yield", "conversion"))
            if index > 1
            else 0.0
        )
        information_gain = information - default_information if index > 1 else 0.0
        reliable = bool(
            index > 1
            and accumulation >= float(policy["minimum_accumulation"])
            and len(target_noise_keys) >= int(policy["minimum_noise_replicates"])
        )
        offline.append(
            {
                "action_id": action_id,
                "candidate_prediction_family": "deactivating_baseline",
                "hidden_observation_family": "reversible_target_pathway",
                "baseline_prediction": baseline_predictions,
                "target_mean": target_means,
                "paired_gap_parent_minus_child": gap,
            }
        )
        steps.append(
            {
                "step": index,
                "unique_condition_cost": index,
                "action_id": action_id,
                "observation_sha256": digest(
                    {
                        "hidden_world_law": "reversible_target_pathway",
                        "target_noise_keys": sorted(target_noise_keys),
                        "target_observed_metrics": target_means,
                    }
                ),
                "statistic_before": 0.0
                if index == 1
                else min(
                    gaps[-2][metric] - gaps[0][metric]
                    for metric in ("yield", "conversion")
                ),
                "statistic_after": accumulation,
                "reliable_falsification": reliable,
                "information_gain_over_default": information_gain,
                "stop_reason": (
                    "two-condition parent-minus-child accumulation signature crossed threshold"
                    if reliable
                    else "continue"
                ),
            }
        )
        if index == 1:
            default_information = information
    stopping_row = next((row for row in steps if row["reliable_falsification"]), None)
    stopping = int(stopping_row["unique_condition_cost"]) if stopping_row else None
    stopping_gain = float(stopping_row["information_gain_over_default"]) if stopping_row else 0.0
    return {
        "estimand_version": "rx-s-parent-minus-child-accumulation-1.0.1",
        "default_action_id": steps[0]["action_id"],
        "default_one_shot_reliably_discriminates": bool(
            steps[0]["reliable_falsification"]
        ),
        "ordered_policy_steps": steps,
        "minimum_reliable_unique_condition_cost": stopping,
        "information_choice_gain_over_default_at_stop": stopping_gain,
        "minimum_information_gain": float(policy["minimum_information_gain"]),
        "active_information_passed": bool(
            stopping is not None
            and stopping_gain >= float(policy["minimum_information_gain"])
        ),
        "budget_window_passed": bool(
            stopping is not None and 1 < stopping <= int(policy["participant_budget"])
        ),
        "repeated_noise_support": {
            "observed_replicates_by_condition": repeated_noise_support,
            "required": int(policy["minimum_noise_replicates"]),
            "derivation": "unique direct_noise_key_sha256 values in hidden-world receipts",
        },
        "offline_paired_family_separability": offline,
    }


def s_start_gate(root: Path, config: Mapping[str, Any]) -> dict[str, Any]:
    summary_path = root / "s-start-gate" / "summary.json"
    if summary_path.exists():
        summary = read(summary_path)
        if summary.get("passed") is not True:
            raise RuntimeError("existing S start gate did not pass")
        return summary
    by_id = {row["cell_id"]: row for row in registered_cells()}
    policy = dict(config["S_start_gate"])
    policies = {
        "ordered_action_ids": policy["ordered_action_ids"],
        "minimum_noise_replicates": policy["independent_noise_replicates_per_action_and_family"],
        "minimum_accumulation": policy["minimum_accumulation"],
        "minimum_information_gain": policy["minimum_information_gain"],
        "participant_budget": policy["participant_budget"],
    }
    world_reports = []
    for world_id, world_seed in WORLDS:
        rows = []
        for action_id in policy["ordered_action_ids"]:
            cell = by_id[action_id]
            for replicate in range(1, 4):
                for law_id in ("deactivating_baseline", "reversible_target_pathway"):
                    row = _s_gate_execution(
                        root
                        / "s-start-gate"
                        / world_id
                        / action_id
                        / f"replicate-{replicate:02d}"
                        / law_id,
                        world_seed=world_seed,
                        cell=cell,
                        law_id=law_id,
                        replicate=replicate,
                    )
                    rows.append(row)
                    if row["status"] != "completed":
                        raise RuntimeError(f"S start gate platform failure: {world_id}/{action_id}")
        for action_id in policy["ordered_action_ids"]:
            for replicate in range(1, 4):
                pair = [
                    row
                    for row in rows
                    if row["cell_id"] == action_id and row["replicate"] == replicate
                ]
                if len(pair) != 2 or len({row["action_plan_sha256"] for row in pair}) != 1:
                    raise ValueError("S start-gate paired actions diverged")
                if len({row["direct_noise_key_sha256"] for row in pair}) != 1:
                    raise ValueError("S start-gate paired observation noise diverged")
        trace = _rx_structural_trace_direction_corrected(rows, policies)
        passed = bool(trace["active_information_passed"] and trace["budget_window_passed"])
        world_report = {
            "world_id": world_id,
            "world_seed": world_seed,
            "passed": passed,
            "trace": trace,
            "execution_count": len(rows),
        }
        write(root / "s-start-gate" / world_id / "report.json", world_report)
        world_reports.append(world_report)
        if not passed:
            raise RuntimeError(f"S start gate scientific failure in {world_id}; provider block sealed")
    summary = {
        "schema_version": "work-ii-rx-ps-s-start-gate-1.0.1",
        "provider_calls": 0,
        "planned_executions": 90,
        "completed_executions": sum(row["execution_count"] for row in world_reports),
        "passed_worlds": sum(row["passed"] for row in world_reports),
        "passed": all(row["passed"] for row in world_reports),
        "worlds": world_reports,
    }
    write(summary_path, summary)
    return summary


def posttest_schema(stage: str) -> dict[str, Any]:
    if stage != "Q":
        return {
            "type": "object",
            "additionalProperties": False,
            "properties": {"report": {"type": "string"}},
            "required": ["report"],
        }
    interval = {
        "type": "object",
        "additionalProperties": False,
        "properties": {key: {"type": "number"} for key in ("estimate", "lower80", "upper80")},
        "required": ["estimate", "lower80", "upper80"],
    }
    metric_map = {
        "type": "object",
        "additionalProperties": False,
        "properties": {metric: interval for metric in METRICS},
        "required": list(METRICS),
    }
    row = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "query_id": {"type": "string"},
            "metrics": metric_map,
            "rationale": {"type": "string"},
        },
        "required": ["query_id", "metrics", "rationale"],
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "predictions": {"type": "array", "items": row, "minItems": 12, "maxItems": 12},
            "rationale": {"type": "string"},
        },
        "required": ["predictions", "rationale"],
    }


def run_posttest(
    agent: Any,
    folder: Path,
    stage: str,
    thread_id: str,
    progress: dict[str, Any],
    query_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    workspace = agent.home_root / "followup"
    workspace.mkdir(exist_ok=True)
    schema_path = workspace / f"{stage}-schema.json"
    write(schema_path, posttest_schema(stage))
    instructions = workspace / "instructions.md"
    instructions.write_text(
        "Continue your own completed research using your existing observations. "
        "No new laboratory experiments, network, filesystem, repository, or hidden-truth access. "
        "Only public_numerics.calculate is available. Answer the current question in full in "
        "English; do not rewrite earlier sealed outputs.",
        encoding="utf-8",
    )
    message = K1 if stage == "K1" else K2
    if stage == "Q":
        message = Q_PROMPT + "\n" + json.dumps(list(query_rows), ensure_ascii=False)
    audit = folder / f"{stage}-numerics.jsonl"
    command = rx_canary.build_command(
        PROVIDER,
        schema_path,
        workspace,
        audit=audit,
        thread_id=thread_id,
        provider_retries=0,
    )
    command += [
        "-c",
        "mcp_servers.chemworld_lab.enabled=false",
        "-c",
        f"mcp_servers.chemworld_lab.command={json.dumps(sys.executable)}",
        "-c",
        f"model_instructions_file={json.dumps(instructions.as_posix())}",
    ]
    result = shared.launch(
        command,
        message,
        workspace,
        agent.followup_environment,
        folder / stage,
        1200,
        True,
        audit,
        {**progress, "phase": stage},
    )
    if not result.get("payload"):
        result["failure"] = result.get("failure") or "missing_payload"
    write(folder / stage / "receipt.json", result)
    return result


def _contains_cjk(text: str) -> bool:
    return any("\u3400" <= char <= "\u9fff" for char in text)


def validate_posttest_payload(stage: str, payload: Any, query_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        return {"valid": False, "failure": "missing_payload"}
    if stage != "Q":
        report = payload.get("report")
        return {
            "valid": isinstance(report, str) and bool(report.strip()) and not _contains_cjk(report),
            "failure": None
            if isinstance(report, str) and bool(report.strip()) and not _contains_cjk(report)
            else "report_missing_or_not_English",
        }
    rows = payload.get("predictions")
    if not isinstance(rows, list):
        return {"valid": False, "failure": "predictions_missing"}
    expected = [row["query_id"] for row in query_rows]
    ids = [row.get("query_id") for row in rows if isinstance(row, Mapping)]
    if len(rows) != 12 or sorted(ids) != sorted(expected):
        return {"valid": False, "failure": "query_ids_missing_or_duplicated"}
    try:
        for row in rows:
            if not isinstance(row.get("rationale"), str) or _contains_cjk(row["rationale"]):
                raise ValueError("row_rationale_missing_or_not_English")
            metric_rows = row["metrics"]
            if set(metric_rows) != set(METRICS):
                raise ValueError("metric_set_mismatch")
            for metric in METRICS:
                estimate, lower, upper = (
                    float(metric_rows[metric][key]) for key in ("estimate", "lower80", "upper80")
                )
                if not all(math.isfinite(value) for value in (estimate, lower, upper)):
                    raise ValueError("non_finite_prediction")
                if not 0.0 <= lower <= estimate <= upper <= 1.0:
                    raise ValueError("invalid_prediction_interval")
        overall = payload.get("rationale")
        if not isinstance(overall, str) or _contains_cjk(overall):
            raise ValueError("overall_rationale_missing_or_not_English")
    except (KeyError, TypeError, ValueError) as exc:
        return {"valid": False, "failure": str(exc)}
    return {"valid": True, "failure": None}


def run_cell(
    root: Path,
    cell: Mapping[str, Any],
    *,
    p_package: Mapping[str, Any],
    s_contract: Mapping[str, Any],
    config: Mapping[str, Any],
    progress: dict[str, Any],
) -> dict[str, Any]:
    folder = root / "sources" / cell["cell_id"]
    result_path = folder / "result.json"
    if result_path.exists():
        return read(result_path)
    if folder.exists():
        raise RuntimeError(f"incomplete write-once cell requires explicit repair: {cell['cell_id']}")
    folder.mkdir(parents=True)
    write(folder / "attempt.json", {**dict(cell), "started_epoch": time.time()})
    material, prior = priors(
        cell["locus"], cell["arm"], int(cell["world_seed"]), p_package, s_contract
    )
    write(
        folder / "public-prior-binding.json",
        {"material_information": material, "initial_world_model": prior},
    )
    progress.update(stage=cell["cell_id"], phase="source", operations=0, batches=0)
    started = time.monotonic()
    result: dict[str, Any] = {
        **dict(cell),
        "status": "failed",
        "failure": None,
        "posttests": {},
        "posttest_validation": {},
    }
    with tempfile.TemporaryDirectory(prefix="chemworld-rx-ps-sol-") as temporary:
        agent = rx_canary.RxFreeResearchAgent(
            goal=cell["goal"],
            home_root=Path(temporary),
            output=folder,
            workspace=Path(temporary) / "laboratory",
            initial_world_model=prior,
            request_timeout_s=1200,
            finalization_timeout_s=300,
            session_wall_time_limit_s=5400,
            max_recovered_mcp_tool_failures=12,
            max_consecutive_mcp_tool_failures=6,
            max_provider_error_events=0,
            pre_action_restart_limit=0,
            accepted_turn_continuation_limit=0,
            provider_process_attempt_limit=1,
            max_initial_prompt_bytes=262144,
            max_tool_output_bytes=131072,
            history_event_limit=360,
            history_byte_limit=524288,
            session_progress_callback=lambda payload: progress.update(provider_liveness=payload),
        )

        def callback(record: Any, trace: Any) -> None:
            del trace
            progress["operations"] += 1
            if (
                record.info.get("instrument") == "final_assay"
                and record.info.get("transaction_status") == "committed"
            ):
                progress["batches"] += 1
            print(
                json.dumps(
                    {
                        "stage": cell["cell_id"],
                        "operations": progress["operations"],
                        "batches": progress["batches"],
                        "action": record.action,
                    }
                ),
                flush=True,
            )

        try:
            physics(
                agent,
                folder / "trajectory.jsonl",
                world_seed=int(cell["world_seed"]),
                material=material,
                observation_seed=deterministic_seed("rx-ps-source", cell["cell_id"]),
                observation_namespace=f"work-ii-rx-ps-source-{cell['cell_id'].lower()}",
                callback=callback,
            )
        except Exception as exc:  # retain source failure as evidence
            result["failure"] = {"type": type(exc).__name__, "message": str(exc)[:1600]}
        finally:
            agent.close()
        if agent.workspace.root.exists():
            shutil.copytree(agent.workspace.root, folder / "workspace")
        records = load_jsonl(folder / "trajectory.jsonl") if (folder / "trajectory.jsonl").exists() else []
        result["batches"] = shared.summaries(records)
        result["operations"] = len(records)
        result["rollbacks"] = [
            {
                "step": index + 1,
                "action": row.get("action"),
                "reason": row.get("rollback_reason"),
            }
            for index, row in enumerate(records)
            if row.get("transaction_status") != "committed"
        ]
        result["exact_replay"] = (
            shared.replay_with_progress(records, cell["cell_id"])
            if records
            else {"verified": False}
        )
        receipts = agent.provider_receipts()
        write(folder / "source-receipts.json", receipts)
        result["source_usage"] = agent.method_resource_usage()
        last = receipts[-1] if receipts else {}
        result["recommendation"] = last.get("final_recommendation")
        thread_id = last.get("thread_id")
        result["thread_id_sha256"] = (
            hashlib.sha256(str(thread_id).encode()).hexdigest() if thread_id else None
        )
        result["source_status"] = (
            "completed"
            if len(result["batches"]) == 12 and result["exact_replay"].get("verified") is True
            else "partial"
            if result["batches"]
            else "failed"
        )
        query_rows = queries(config, cell["locus"])
        if thread_id and result["batches"]:
            for stage in ("K1", "Q", "K2"):
                progress["phase"] = stage
                turn = run_posttest(agent, folder, stage, thread_id, progress, query_rows)
                result["posttests"][stage] = turn
                result["posttest_validation"][stage] = validate_posttest_payload(
                    stage, turn.get("payload"), query_rows
                )
        sessions = agent.home_root / "codex-home" / "sessions"
        if sessions.exists():
            shutil.copytree(sessions, folder / "provider-rollouts")
    result["posttest_chain_sealed"] = all(
        stage in result["posttests"] and result["posttests"][stage].get("payload")
        for stage in ("K1", "Q", "K2")
    )
    result["status"] = (
        "completed"
        if result["source_status"] == "completed"
        and result["posttest_chain_sealed"]
        and not result["failure"]
        and all(item["valid"] for item in result["posttest_validation"].values())
        else "retained_nonconforming"
    )
    result["elapsed_s"] = time.monotonic() - started
    write(result_path, result)
    return result


def generate_truth(
    root: Path,
    config: Mapping[str, Any],
) -> dict[str, dict[str, dict[str, list[dict[str, float]]]]]:
    truth: dict[str, dict[str, dict[str, list[dict[str, float]]]]] = {}
    for world_id, world_seed in WORLDS:
        truth[world_id] = {}
        for locus in LOCI:
            truth[world_id][locus] = {}
            for query in queries(config, locus):
                repeats = []
                for replicate in range(1, 6):
                    seed = deterministic_seed(
                        "rx-ps-q-v1", world_id, locus, query["query_id"], f"r{replicate:02d}"
                    )
                    report = _reference_run(
                        root
                        / "reference-truth"
                        / world_id
                        / locus
                        / query["query_id"]
                        / f"replicate-{replicate:02d}",
                        query["actions"],
                        world_seed=world_seed,
                        observation_seed=seed,
                        observation_namespace=(
                            f"work-ii-rx-ps-truth-{world_id.lower()}-{locus.lower()}-"
                            f"{query['query_id'].lower()}-r{replicate:02d}"
                        ),
                    )
                    if (
                        report["failure"]
                        or len(report["batches"]) != 1
                        or report["rollbacks"]
                        or report["exact_replay"].get("verified") is not True
                    ):
                        raise RuntimeError(
                            f"reference truth failed: {world_id}/{locus}/{query['query_id']}/r{replicate}"
                        )
                    repeats.append(
                        {metric: float(report["batches"][0]["metrics"][metric]) for metric in METRICS}
                    )
                truth[world_id][locus][query["query_id"]] = repeats
    write(root / "truth.json", truth)
    return truth


def evaluate_predictions(
    payload: Any,
    query_rows: Sequence[Mapping[str, Any]],
    truth: Mapping[str, Sequence[Mapping[str, float]]],
) -> dict[str, Any]:
    validation = validate_posttest_payload("Q", payload, query_rows)
    if not validation["valid"]:
        return validation
    predictions = {row["query_id"]: row for row in payload["predictions"]}
    output = {}
    for metric in METRICS:
        errors: list[float] = []
        coverage: list[bool] = []
        widths: list[float] = []
        interval_scores: list[float] = []
        for query in query_rows:
            query_id = query["query_id"]
            interval = predictions[query_id]["metrics"][metric]
            estimate = float(interval["estimate"])
            lower = float(interval["lower80"])
            upper = float(interval["upper80"])
            outcomes = [float(row[metric]) for row in truth[query_id]]
            errors.append(abs(estimate - fmean(outcomes)))
            for outcome in outcomes:
                coverage.append(lower <= outcome <= upper)
                widths.append(upper - lower)
                penalty = 0.0
                if outcome < lower:
                    penalty = 10.0 * (lower - outcome)
                elif outcome > upper:
                    penalty = 10.0 * (outcome - upper)
                interval_scores.append((upper - lower) + penalty)
        output[metric] = {
            "query_count": 12,
            "reference_observation_count": 60,
            "mae_to_five_repeat_mean": fmean(errors),
            "empirical_coverage80": fmean(coverage),
            "mean_width80": fmean(widths),
            "mean_interval_score_alpha_0_2": fmean(interval_scores),
        }
    return {"valid": True, "metrics": output}


def run_recommendation_retest(root: Path, result: Mapping[str, Any]) -> dict[str, Any] | None:
    recommendation = result.get("recommendation") or {}
    index = recommendation.get("selected_experiment_index")
    selected = next(
        (row for row in result.get("batches", []) if row["lifecycle_index"] == index),
        None,
    )
    if selected is None:
        return None
    return _reference_run(
        root / "recommendation-retests" / result["cell_id"],
        selected["actions"],
        world_seed=int(result["world_seed"]),
        observation_seed=deterministic_seed("rx-ps-recommendation-retest", result["cell_id"]),
        observation_namespace=f"work-ii-rx-ps-retest-{result['cell_id'].lower()}",
        source_envelope=True,
    )


def write_summary(root: Path, results: Sequence[Mapping[str, Any]], phase: str) -> None:
    write(
        root / "summary.json",
        {
            "schema_version": "work-ii-rx-ps-five-world-dual-goal-summary-1.0",
            "phase": phase,
            "planned_sources": 60,
            "planned_source_batches": 720,
            "planned_posttests": 180,
            "attempted_sources": len(results),
            "completed_sources": sum(row.get("status") == "completed" for row in results),
            "sealed_posttest_chains": sum(
                row.get("posttest_chain_sealed") is True for row in results
            ),
            "results": [
                {
                    "cell_id": row["cell_id"],
                    "status": row.get("status"),
                    "source_status": row.get("source_status"),
                    "operations": row.get("operations"),
                    "batches": len(row.get("batches", [])),
                    "posttest_chain_sealed": row.get("posttest_chain_sealed"),
                    "failure": row.get("failure"),
                }
                for row in results
            ],
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--engineering-only", action="store_true")
    args = parser.parse_args()
    configure_shared_helpers()
    config = read(CONFIG)
    correction = read(CORRECTION)
    if correction["base_config"]["sha256"] != hashlib.sha256(CONFIG.read_bytes()).hexdigest():
        raise RuntimeError("v1.0.1 correction is not bound to the current v1.0 base config")
    validated = validate_design(config)
    root = args.output.resolve()
    root.mkdir(parents=True, exist_ok=True)
    design = {
        "schema_version": "work-ii-rx-ps-five-world-dual-goal-run-design-1.0.1",
        "frozen_config": config,
        "frozen_config_sha256": digest(config),
        "frozen_correction": correction,
        "frozen_correction_sha256": digest(correction),
        "schedule": validated["schedule"],
        "queries": {locus: queries(config, locus) for locus in LOCI},
        "query_sha256": validated["query_sha256"],
        "provider": PROVIDER,
        "system_prompt": SYSTEM,
        "goals": GOALS,
        "K1": K1,
        "Q": Q_PROMPT,
        "K2": K2,
        "truth_embargo": "No reference truth generation until all 60 K2 responses are sealed.",
    }
    design_path = root / "design.json"
    if design_path.exists() and read(design_path) != design:
        raise RuntimeError("existing run design differs from frozen design")
    write(design_path, design)
    print(
        json.dumps(
            {
                "stage": "design",
                "source_sessions": 60,
                "source_batches": 720,
                "posttests": 180,
                "design_sha256": digest(design),
            }
        ),
        flush=True,
    )
    engineering_gate(root, config)
    gate = s_start_gate(root, config)
    print(
        json.dumps(
            {
                "stage": "preflight_complete",
                "engineering_loci": 2,
                "s_gate_executions": gate["completed_executions"],
                "s_gate_worlds_passed": gate["passed_worlds"],
            }
        ),
        flush=True,
    )
    if args.engineering_only:
        return

    progress: dict[str, Any] = {
        "completed": 0,
        "total": 60,
        "stage": "starting",
        "phase": "source",
    }
    stop = threading.Event()
    started = time.monotonic()

    def heartbeat() -> None:
        while not stop.wait(30):
            elapsed = time.monotonic() - started
            done = progress["completed"]
            print(
                json.dumps(
                    {
                        **progress,
                        "elapsed_s": round(elapsed),
                        "eta_s": round(elapsed / done * (60 - done)) if done else None,
                    },
                    default=str,
                ),
                flush=True,
            )

    heartbeat_thread = threading.Thread(target=heartbeat, daemon=True)
    heartbeat_thread.start()
    results = []
    try:
        for cell in validated["schedule"]:
            result = run_cell(
                root,
                cell,
                p_package=validated["p_package"],
                s_contract=validated["s_contract"],
                config=config,
                progress=progress,
            )
            results.append(result)
            progress["completed"] = len(results)
            write_summary(root, results, "provider_sources_and_posttests")
            print(
                json.dumps(
                    {
                        "cell": result["cell_id"],
                        "status": result["status"],
                        "completed": len(results),
                        "total": 60,
                    }
                ),
                flush=True,
            )
            if result.get("failure") and result.get("operations") == 0:
                raise RuntimeError("shared pre-action provider failure; remaining block stopped")
        if not all(row.get("posttest_chain_sealed") is True for row in results):
            write_summary(root, results, "truth_embargoed_incomplete_posttest_chain")
            raise RuntimeError("not all K2 responses sealed; reference truth remains embargoed")
        progress.update(stage="reference_truth", phase="provider_free")
        truth = generate_truth(root, config)
        for result in results:
            query_rows = queries(config, result["locus"])
            evaluation = evaluate_predictions(
                result["posttests"]["Q"].get("payload"),
                query_rows,
                truth[result["world_id"]][result["locus"]],
            )
            write(root / "evaluations" / f"{result['cell_id']}.json", evaluation)
            retest = run_recommendation_retest(root, result)
            if retest is not None and (
                retest["failure"]
                or len(retest["batches"]) != 1
                or retest["rollbacks"]
                or retest["exact_replay"].get("verified") is not True
            ):
                raise RuntimeError(f"recommendation retest failed: {result['cell_id']}")
        write_summary(root, results, "complete")
        write(
            root / "completion.json",
            {
                "completed_epoch": time.time(),
                "source_sessions": len(results),
                "source_batches": sum(len(row.get("batches", [])) for row in results),
                "posttests": sum(len(row.get("posttests", {})) for row in results),
                "reference_executions": 600,
                "recommendation_retests": sum(
                    (root / "recommendation-retests" / row["cell_id"] / "result.json").exists()
                    for row in results
                ),
            },
        )
    finally:
        stop.set()
        heartbeat_thread.join(timeout=2)


if __name__ == "__main__":
    main()
