"""W2-118: fixed task-specific qualification with a real public prior interface."""

# ruff: noqa: RUF001
from __future__ import annotations

import argparse
import json
import math
import threading
import time
from copy import deepcopy
from pathlib import Path

import gymnasium as gym
from scripts.run_work_ii_new_system_gates import action, measure, resource_checks, write

from chemworld.campaign_resources import CampaignResourceCard
from chemworld.data.logging import load_jsonl
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.research_brief import TASKS, VERSION
from chemworld.runtime.phase_ledger_services import ChemWorldPhaseLedgerServices
from chemworld.runtime.species import MechanismSpeciesView
from chemworld.tasks import get_task
from chemworld.world.instruments import chemworld_instruments
from chemworld.world.scoring import (
    PARTITION_S0_EXTRACTION_EFFICIENCY_V3,
    TASK_DERIVED_SCORING_CONTRACT,
)

ROOT = Path(__file__).resolve().parents[1]
NOTE = "workstreams/flagship_tasks/WORK_II_GATE_REPAIR_NOTE.md"
REPORT = ROOT / "workstreams/flagship_tasks/reports/work-ii-gate-repair-20260916.json"
BUDGETS = {"RX": 48, "EQ": 24, "BC": 18, "PA": 48, "FL": 72}
METRICS = {
    "RX": "yield",
    "EQ": "acid_dissociation_fraction",
    "BC": "yield",
    "PA": "product_in_organic",
    "FL": "flow_conversion",
}
PAIRS = {
    "RX": [(1, 3), (5, 7)],
    "EQ": [(0, 1), (2, 3)],
    "BC": [(0, 2)],
    "PA": [(0, 1), (2, 3)],
    "FL": [(3, 5), (6, 8)],
}
ANCHORS = {"RX": (3, 1), "EQ": (1, 0), "BC": (2, 0), "PA": (1, 0), "FL": (8, 0)}
SHIFTS = {
    "EQ": [{"axis_id": "equilibrium.acid-base-constants", "mode": "extrapolation", "severity": 1}],
    "PA": [{"kind": "mechanism_family", "mode": "constitutive_law_family", "severity": 1}],
    "FL": [{"axis_id": "flow.reaction-kinetics", "mode": "extrapolation", "severity": 1}],
}


def recipes(code):
    close = [action("terminate"), measure("final_assay")]
    if code in {"RX", "BC"}:
        points = (
            [(c, t) for c in (0.00002, 0.00025) for t in (1, 5, 30, 300)]
            if code == "RX"
            else [(0.00025, t) for t in (1, 30, 600)]
        )
        return [
            [
                action("add_solvent", volume_L=0.028, solvent=2),
                action("add_reagent", amount_mol=0.010),
                action("add_catalyst", catalyst_amount_mol=c, catalyst=1),
                action("heat", target_temperature_K=335, duration_s=t, stirring_speed_rpm=720),
                *close,
            ]
            for c, t in points
        ]
    if code == "EQ":
        return [
            [
                action("add_solvent", volume_L=v, solvent=0),
                action("add_reagent", amount_mol=a),
                measure("ph_meter"),
                *close,
            ]
            for v in (0.020, 0.060)
            for a in (0.00001, 0.010)
        ]
    if code == "PA":
        return [
            [
                action("add_solvent", volume_L=0.025, solvent=0),
                action("add_phase", phase="aqueous", volume_L=0.018),
                action("add_extractant", extractant=e, volume_L=v),
                action("mix", duration_s=240, stirring_speed_rpm=750),
                action("settle", duration_s=360),
                *close,
            ]
            for v in (0.006, 0.030)
            for e in (0, 3)
        ]
    if code == "FL":
        return [
            [
                action("add_solvent", volume_L=0.026, solvent=2),
                action("add_reagent", amount_mol=0.010),
                action("add_catalyst", catalyst_amount_mol=0.00022, catalyst=1),
                action("set_flow_rate", flow_rate_mL_min=1.2, residence_time_s=t),
                action("run_flow", target_temperature_K=temp, duration_s=2 * t),
                *close,
            ]
            for t in (900, 3600, 7200)
            for temp in (340, 390, 430)
        ]
    raise ValueError(code)


def card_for(code, batches):
    n = len(batches)
    return CampaignResourceCard(
        card_id=f"work-ii-research-{code}-{n}-batch",
        operation_attempt_limit=BUDGETS[code],
        vessel_start_limit=n,
        final_assay_limit=n,
        nonfinal_instrument_use_limit=n if code == "EQ" else 0,
        stock_limits={
            "reagent_mol": 0.04 * n,
            "solvent_L": 0.08 * n,
            "catalyst_mol": 0.005 * n,
            "phase_liquid_L": 0.06 * n,
            "extractant_L": 0.06 * n,
        },
        process_time_limit_s=14400 * n,
    )


def cutoff(metric):
    return max(
        0.01 if metric == "pH_normalized" else 0.02,
        3 * math.sqrt(2) * chemworld_instruments()["final_assay"].noise_std[metric],
    )


def brief_for(code, prior=None):
    return {"schema_version": VERSION, "card": code, "prior_record": deepcopy(prior)}


class ReceivedReference(_FrozenTruthReplayAgent):
    def __init__(self, actions, folder):
        super().__init__(actions)
        self.folder = folder
        self.public_packets_seen = 0
        self.public_packet = None

    def reset(self, task_info, seed):
        super().reset(task_info, seed)
        self.public_packet = deepcopy(task_info["research_brief"])
        write(self.folder / "received_task_info.json", task_info)

    def act_with_public_view(self, context, public_view):
        del context
        assert public_view["tool_json"]["research_brief"] == self.public_packet
        assert "operational_state" in public_view["tool_json"]
        self.public_packets_seen += 1
        return self.act([])


class EvaluatorCapture(gym.Wrapper):
    """Observe committed PA sample bookkeeping without returning it to the agent."""

    def __init__(self, env, records):
        super().__init__(env)
        self.evaluator_records = records

    def reset(self, **kwargs):
        result = self.env.reset(**kwargs)
        base = self.unwrapped
        original = base.runtime.apply_transaction
        phases = ChemWorldPhaseLedgerServices(
            MechanismSpeciesView(base.scenario_instance.compiled_mechanism)
        )
        species = phases.product_candidate_species()

        def target_total(state):
            if state.phases is not None:
                return sum(
                    p.species_amounts_mol.get(s, 0)
                    for p in state.phases.phases.values()
                    for s in species
                )
            return sum(state.species_amounts.get(s, 0) for s in species)

        def capture(state, payload):
            result = original(state, payload)
            if payload.get("instrument") == "final_assay":
                initial = sum(state.species.initial_amounts_mol.get(s, 0) for s in species)
                before, after = target_total(state), target_total(result.state)
                volume = chemworld_instruments()["final_assay"].sample_volume_L
                expected_loss = before * volume / state.volume_L
                self.evaluator_records.append(
                    {
                        "initial_target_mol": initial,
                        "before_assay_target_mol": before,
                        "after_assay_target_mol": after,
                        "expected_sample_target_mol": expected_loss,
                        "before_error_mol": abs(before - initial),
                        "after_plus_sample_error_mol": abs(after + expected_loss - initial),
                    }
                )
            return result

        base.runtime.apply_transaction = capture
        return result


def execute(root, code, stage, prior, progress):
    folder = root / f"{code}-{stage}"
    folder.mkdir()
    all_batches = recipes(code)
    batches = [all_batches[i] for i in ANCHORS[code]] if stage in {"O", "A", "M"} else all_batches
    actions = [a for b in batches for a in b]
    resources_card = card_for(code, batches)
    research = brief_for(code, prior)
    interventions = SHIFTS[code] if stage == "shift" else []
    scoring = (
        PARTITION_S0_EXTRACTION_EFFICIENCY_V3 if code == "PA" else TASK_DERIVED_SCORING_CONTRACT
    )
    namespace = "w2-118-verification" if stage in {"O", "A", "M"} else "w2-118-calibration"
    write(
        folder / "plan.json",
        {
            "task": TASKS[code],
            "batches": batches,
            "research_brief": research,
            "scoring_contract_id": scoring,
            "world_interventions": interventions,
            "resource_card": resources_card.to_dict(),
            "seed": 0,
            "observation_seed": 1,
            "observation_noise_namespace": namespace,
        },
    )
    holder, snapshots, evaluator_records, telemetry = [], [], [], []
    progress.update(stage="physical", unit=folder.name, operations=0)
    started = time.monotonic()
    agent = ReceivedReference(actions, folder)

    def wrap(env):
        holder.append(env.unwrapped)
        return EvaluatorCapture(env, evaluator_records) if code == "PA" else env

    def on_step(record, trace):
        del trace
        progress["operations"] += 1
        snapshots.append(holder[0].public_campaign_resource_state())
        telemetry.append(
            {
                "step": record.step,
                "operation": record.action["operation"],
                **record.public_view["tool_json"]["operational_state"],
            }
        )
        if record.info.get("transaction_status") != "committed":
            raise RuntimeError(f"failed transaction at step {record.step}")

    failure = None
    try:
        run_agent(
            env_id=get_task(TASKS[code]).env_id,
            agent=agent,
            world_split="public-test",
            budget=BUDGETS[code],
            budget_override=BUDGETS[code],
            objective="balanced",
            seed=0,
            agent_seed=0,
            observation_seed=1,
            task_id=TASKS[code],
            output_path=folder / "trajectory.jsonl",
            episode_mode_override="campaign",
            research_brief=research,
            campaign_resource_card=resources_card,
            observation_noise_mode="keyed",
            observation_noise_namespace=namespace,
            world_interventions=interventions,
            scoring_contract_id=scoring,
            step_callback=on_step,
            env_wrapper=wrap,
        )
    except Exception as exc:
        failure = {"type": type(exc).__name__, "message": str(exc)}
    physical_seconds = time.monotonic() - started
    rows = load_jsonl(folder / "trajectory.jsonl") if (folder / "trajectory.jsonl").exists() else []
    progress["stage"] = "exact_replay"
    start_replay = time.monotonic()
    try:
        replay = verify_records(rows, tolerance=0, world_interventions=interventions).to_dict()
    except Exception as exc:
        replay = {"verified": False, "error": str(exc)}
    replay_seconds = time.monotonic() - start_replay
    finals = [
        r
        for r in rows
        if r.get("instrument") == "final_assay" and r.get("transaction_status") == "committed"
    ]
    values = [
        {k: v for k, v in r["observation"].items() if v is not None and not k.endswith("_mask")}
        for r in finals
    ]
    resource_result = resource_checks(rows, snapshots, resources_card)
    runtime = failure is None and len(rows) == len(actions) and len(finals) == len(batches)
    packet_ok = agent.public_packets_seen == len(actions) and agent.public_packet is not None
    result = {
        "card": code,
        "stage": stage,
        "failure": failure,
        "runtime_passed": runtime,
        "packet_delivered": packet_ok,
        "received_packet": agent.public_packet,
        "planned_batches": len(batches),
        "completed_batches": len(finals),
        "planned_operations": len(actions),
        "operations": len(rows),
        "metrics": values,
        "resources": resource_result,
        "replay": replay,
        "evaluator_records": evaluator_records,
        "physical_seconds": physical_seconds,
        "replay_seconds": replay_seconds,
        "directory": folder.relative_to(ROOT).as_posix(),
        "failures": [
            {
                "step": r["step"],
                "reason": r.get("rollback_reason"),
                "preconditions": r.get("preconditions"),
            }
            for r in rows
            if r.get("transaction_status") != "committed"
        ],
    }
    for filename, payload in (
        ("result.json", result),
        ("resource_events.json", snapshots),
        ("telemetry.json", telemetry),
        ("replay.json", replay),
    ):
        write(folder / filename, payload)
    return result


def ok(cell):
    return (
        cell["runtime_passed"]
        and cell["packet_delivered"]
        and cell["resources"]["passed"]
        and cell["replay"]["verified"]
    )


def summarize(root, cells, elapsed, codes=TASKS, note=NOTE):
    systems = []
    for code in codes:
        base = next(c for c in cells if c["card"] == code and c["stage"] == "base")
        metric = METRICS[code]
        comparisons = []
        for a, b in PAIRS[code]:
            delta = (
                base["metrics"][b][metric] - base["metrics"][a][metric]
                if len(base["metrics"]) > max(a, b)
                else None
            )
            comparisons.append(
                {
                    "batches": [a + 1, b + 1],
                    "delta": delta,
                    "cutoff": cutoff(metric),
                    "passed": delta is not None and abs(delta) >= cutoff(metric),
                }
            )
        arms = [
            next(c for c in cells if c["card"] == code and c["stage"] == arm)
            for arm in ("O", "A", "M")
        ]
        invariant = all(ok(c) for c in arms) and all(
            c["metrics"] == arms[0]["metrics"]
            and c["resources"]["final_state"] == arms[0]["resources"]["final_state"]
            for c in arms[1:]
        )
        agreement, refuted = False, False
        if all(c["metrics"] and c["received_packet"] for c in arms):
            a = arms[1]["received_packet"]["prior_record"]
            m = arms[2]["received_packet"]["prior_record"]
            observed = arms[1]["metrics"][0][metric]
            agreement = abs(observed - a["estimate"]) <= a["half_width"]
            refuted = abs(observed - m["estimate"]) > m["half_width"]
        result = {
            "card": code,
            "reference_runtime_passed": ok(base),
            "response_comparisons": comparisons,
            "response_passed": ok(base) and all(p["passed"] for p in comparisons),
            "triarm_physics_invariant": invariant,
            "aligned_supported": agreement,
            "misindexed_refuted": refuted,
        }
        result["local_prior_qualification"] = invariant and agreement and refuted
        if code in SHIFTS:
            shifted = next(c for c in cells if c["card"] == code and c["stage"] == "shift")
            key = "pH_normalized" if code == "EQ" else metric
            deltas = [
                b[key] - a[key] for a, b in zip(base["metrics"], shifted["metrics"], strict=False)
            ]
            result["world_deltas"] = deltas
            result["world_response_passed"] = (
                ok(base) and ok(shifted) and sum(abs(d) >= cutoff(key) for d in deltas) >= 2
            )
        if code == "PA":
            sums = [m["product_in_organic"] + m["product_in_aqueous"] for m in base["metrics"]]
            errors = [
                max(x["before_error_mol"], x["after_plus_sample_error_mol"])
                for x in base["evaluator_records"]
            ]
            result.update(
                phase_fraction_sums=sums,
                mass_errors_mol=errors,
                phase_accounting_passed=(
                    len(sums) == 4
                    and len(errors) == 4
                    and all(0.90 <= s <= 1.05 for s in sums)
                    and all(e <= 1e-8 for e in errors)
                ),
            )
        if code == "FL":
            feasible = [
                m["flow_conversion"] >= 0.5 and m["yield"] >= 0.1 and m["safety_risk"] <= 0.35
                for m in base["metrics"]
            ]
            result.update(
                feasible_points=feasible,
                window_covered=len(feasible) == 9 and any(feasible) and not all(feasible),
            )
        result["screen_passed"] = (
            result["response_passed"]
            and result["local_prior_qualification"]
            and result.get("phase_accounting_passed", True)
            and result.get("window_covered", True)
        )
        systems.append(result)
    counts = {
        "campaigns_planned": len(cells),
        "campaigns_complete": sum(c["runtime_passed"] for c in cells),
        "batches_planned": sum(c["planned_batches"] for c in cells),
        "batches_complete": sum(c["completed_batches"] for c in cells),
        "operations": sum(c["operations"] for c in cells),
        "resources_passed": sum(c["resources"]["passed"] for c in cells),
        "replays_passed": sum(c["replay"]["verified"] for c in cells),
        "triarm_entry_passes": sum(ok(c) for c in cells if c["stage"] in {"O", "A", "M"}),
        "response_passes": sum(s["response_passed"] for s in systems),
        "local_prior_passes": sum(s["local_prior_qualification"] for s in systems),
        "system_screen_passes": sum(s["screen_passed"] for s in systems),
        "world_response_passes": sum(s.get("world_response_passed", False) for s in systems),
        "model_calls": 0,
        "retries": 0,
    }
    return {
        "evidence_mode": "development",
        "status": "closed",
        "experiment_note": note,
        "run_root": root.relative_to(ROOT).as_posix(),
        "elapsed_seconds": elapsed,
        "counts": counts,
        "systems": systems,
        "campaigns": cells,
        "full_science_gate_qualified": False,
        "full_agent_chain_tested": False,
    }


def render(report):
    c = report["counts"]
    n = c["campaigns_planned"]
    systems = len(report["systems"])
    shifts = sum("world_response_passed" in s for s in report["systems"])
    lines = [
        "# W2-118：五体系修复验证" if systems == 5 else "# W2-118：PA评估接口修复复测",
        "",
        "固定开发块；零provider、零重试。",
        "",
        f"耗时{report['elapsed_seconds'] / 60:.2f}分钟；"
        f"完整campaign {c['campaigns_complete']}/{n}，"
        f"终检{c['batches_complete']}/{c['batches_planned']}，动作{c['operations']}；"
        f"资源{c['resources_passed']}/{n}，精确重放{c['replays_passed']}/{n}。",
        "",
        f"真实三臂入口{c['triarm_entry_passes']}/{systems * 3}；"
        f"主响应{c['response_passes']}/{systems}；"
        f"局部资料反证资格{c['local_prior_passes']}/{systems}；"
        f"任务筛查合取{c['system_screen_passes']}/{systems}；"
        f"成对世界{c['world_response_passes']}/{shifts}。",
        "",
        "| 卡 | 基础运行 | 主响应 | 三臂物理一致 | A支持 | M反驳 | 任务筛查合取 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for s in report["systems"]:
        keys = [
            "reference_runtime_passed",
            "response_passed",
            "triarm_physics_invariant",
            "aligned_supported",
            "misindexed_refuted",
            "screen_passed",
        ]
        lines.append(
            f"| {s['card']} | " + " | ".join("通过" if s[k] else "未通过" for k in keys) + " |"
        )
    lines += [
        "",
        "## 全部执行终态",
        "",
        "| 条件 | 终检 | 动作 | 错误 |",
        "| --- | --- | --- | --- |",
    ]
    for cell in report["campaigns"]:
        lines.append(
            f"| {cell['card']}-{cell['stage']} | "
            f"{cell['completed_batches']}/{cell['planned_batches']} | "
            f"{cell['operations']}/{cell['planned_operations']} | {cell['failure'] or '无'} |"
        )
    lines += ["", "## 基础世界终检", ""]
    for cell in report["campaigns"]:
        if cell["stage"] != "base":
            continue
        code = cell["card"]
        keys = [METRICS[code]]
        if code == "PA":
            keys += ["product_in_aqueous"]
        if code == "FL":
            keys += ["yield", "safety_risk"]
        lines += [
            f"### {code}",
            "",
            "| 批次 | " + " | ".join(keys) + " |",
            "| --- | " + " | ".join("---" for _ in keys) + " |",
        ]
        for i, m in enumerate(cell["metrics"], 1):
            lines.append(f"| {i} | " + " | ".join(f"{m[k]:.6f}" for k in keys) + " |")
        lines.append("")
    lines += [
        "## 范围",
        "",
        "新research_brief实际进入Agent reset和每步工具视图；"
        "三臂相同操作不表示自主Agent会选择相同操作。"
        "这里检验资料接口不改变物理、A局部资料与复测相容、M可被预算内公开证据反驳，不是三臂能力结果。",
        "资料来自事前指定条件的付费标定读数，只给一条局部估计；模型仍可自由推断。"
        "已提示点不能作为后续盲测。完整机理可辨识性、新干预预测、K1/Q/K2及评审尚未完成。",
        "RX/BC可选结构世界分叉仍未接入；FL窗口标准只是公开示例，不能替代完整安全约束资格。"
        "历史W2-117结果和默认接口保留。",
        "",
        f"[固定说明](../{Path(report['experiment_note']).name})",
        "",
    ]
    return "\n".join(lines)


def closeout():
    """Read preserved blocks; never replace historical failures with the PA follow-up."""
    paths = [REPORT, REPORT.with_name("work-ii-pa-gate-repair-20260916.json")]
    blocks = [json.loads(p.read_text(encoding="utf-8")) for p in paths]
    all_cells = [c for b in blocks for c in b["campaigns"]]
    latest = {s["card"]: s for b in blocks for s in b["systems"]}
    effective_cells = [c for c in blocks[0]["campaigns"] if c["card"] != "PA"]
    effective_cells += blocks[1]["campaigns"]
    effective = summarize(ROOT, effective_cells, sum(b["elapsed_seconds"] for b in blocks))
    pa = blocks[1]["campaigns"]
    errors = [
        max(r["before_error_mol"], r["after_plus_sample_error_mol"])
        for c in pa
        for r in c["evaluator_records"]
    ]
    phase_sums = [
        m["product_in_organic"] + m["product_in_aqueous"] for c in pa for m in c["metrics"]
    ]
    failures = [
        {
            "block": p.relative_to(ROOT).as_posix(),
            "card": c["card"],
            "stage": c["stage"],
            "failure": c["failure"],
            "operations": c["operations"],
        }
        for p, b in zip(paths, blocks, strict=True)
        for c in b["campaigns"]
        if c["failure"]
    ]
    launcher = ROOT / blocks[0]["run_root"] / "launcher_error.json"
    payload = {
        "evidence_mode": "development",
        "status": "closed_partial_scientific_screen",
        "blocks": [
            {
                "report": p.relative_to(ROOT).as_posix(),
                "counts": b["counts"],
                "elapsed_seconds": b["elapsed_seconds"],
            }
            for p, b in zip(paths, blocks, strict=True)
        ],
        "total_counts": {
            "campaigns_planned": len(all_cells),
            "campaigns_attempted": sum(c["failure"] != "upstream_missing" for c in all_cells),
            "campaigns_complete": sum(c["runtime_passed"] for c in all_cells),
            "campaigns_setup_failed": sum(isinstance(c["failure"], dict) for c in all_cells),
            "campaigns_upstream_missing": sum(
                c["failure"] == "upstream_missing" for c in all_cells
            ),
            "batches_planned": sum(c["planned_batches"] for c in all_cells),
            "batches_complete": sum(c["completed_batches"] for c in all_cells),
            "operations_planned": sum(c["planned_operations"] for c in all_cells),
            "operations": sum(c["operations"] for c in all_cells),
            "resources_passed": sum(c["resources"]["passed"] for c in all_cells),
            "replays_passed": sum(c["replay"]["verified"] for c in all_cells),
            "model_calls": 0,
            "within_block_retries": 0,
            "explicit_repair_followup_campaigns": 5,
        },
        "current_source_rule": "Original block for RX/EQ/BC/FL; fixed PA follow-up for PA.",
        "current_counts": effective["counts"],
        "systems": list(latest.values()),
        "pa_all_batches": {
            "batches": len(errors),
            "max_mass_error_mol": max(errors),
            "phase_fraction_sum_range": [min(phase_sums), max(phase_sums)],
            "passed": len(errors) == len(phase_sums) == 14
            and all(e <= 1e-8 for e in errors)
            and all(0.90 <= s <= 1.05 for s in phase_sums),
        },
        "failures": failures,
        "launcher_failure": json.loads(launcher.read_text(encoding="utf-8")),
        "elapsed_seconds": effective["elapsed_seconds"],
        "full_science_gate_qualified": False,
        "full_agent_chain_tested": False,
        "formal_result": False,
    }
    path = REPORT.with_name("work-ii-gate-repair-summary-20260916.json")
    write(path, payload)
    c, t = payload["current_counts"], payload["total_counts"]
    lines = [
        "# W2-118：五体系修复结果与剩余缺口",
        "",
        "已修复任务/先验接入、测量口径和参考选点；当前局部任务筛查通过4/5。"
        "FL可行窗口仍未建立。全部为单实例开发证据，零模型调用，不能解释为Agent成功率。",
        "",
        "## 改了什么",
        "",
        "- 新增可选research_brief，将体系定制委托、测量定义和可修订实例资料送达"
        "Agent初始输入及每步工具视图。自由机理形式保留，未规定方程模板。",
        "- 提供理想温度/压力/体积/时间与流程配置读数，明确边界设定不等于流体状态，"
        "区分刚结束批次的化验与下一批初态；组分仍需付费测量。",
        "- RX/BC覆盖早期形成与后期损失；EQ扩大浓度范围；PA显式使用已有固定初始"
        "目标库存分母合同并在弃相前测量；FL覆盖更长停留时间与壁温。未修改化学定律或物理常数。",
        "- PA原评估器错误读取env.compiled_mechanism，在动作前失败。修复引用后，"
        "将受影响5个条件从头独立复测，原失败保留。默认历史接口不变。",
        "",
        "## 当前逐体系结果",
        "",
        "当前口径：RX/EQ/BC/FL取第一修复块，PA取接口修复后的独立复测块；不是整块一次全过。",
        "",
        "| 体系 | 公开主响应 | O/A/M物理一致 | A相容/M可反驳 | 额外任务检查 | 局部筛查 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for s in payload["systems"]:
        extra = (
            "两相核算通过"
            if s["card"] == "PA"
            else "可行点0/9"
            if s["card"] == "FL"
            else "不要求产率可行窗口"
        )
        flags = [
            s["response_passed"],
            s["triarm_physics_invariant"],
            s["local_prior_qualification"],
        ]
        lines.append(
            f"| {s['card']} | "
            + " | ".join("通过" if f else "未通过" for f in flags)
            + f" | {extra} | {'通过' if s['screen_passed'] else '未通过'} |"
        )
    lines += [
        "",
        f"三臂入口{c['triarm_entry_passes']}/15、主响应{c['response_passes']}/5、"
        f"局部资料反证资格{c['local_prior_passes']}/5；EQ/PA/FL世界分叉响应"
        f"{c['world_response_passes']}/3。RX/BC可选结构分叉未接入。",
        "RX两组时间主对比差约0.734/0.724，BC约0.636；EQ浓度对比绝对差0.091/0.176；"
        "PA介质对比差0.187/0.216，均超过预设噪声阈值。PA全部14批物料核算通过，"
        f"最大绝对误差{max(errors):.3g} mol，两相公开读数之和为"
        f"{min(phase_sums):.4f}—{max(phase_sums):.4f}。",
        "",
        "FL九点中最高转化约0.318，对应yield约0.193、risk约0.377；"
        "7200s/390K点约为conversion0.143、yield0.113、risk0.179。"
        "预定conversion≥0.50、yield≥0.10、risk≤0.35合取下仍为0/9。"
        "这说明本覆盖尚无可行见证，不证明整个动作空间无解，更不是Agent失效。"
        "已核查底层是几何/传热耦合PFR，继续加催化剂并非有依据的修复："
        "当前目标反应速率式没有催化剂浓度项。下一步需要独立标定安全约束下可达前沿，"
        "据此论证任务规格；不追溯降低本轮阈值。",
        "",
        "## 分母与失败保留",
        "",
        f"第一块18/23 campaign、61/75终检；PA独立修复复测5/5、14/14。"
        f"累计{t['campaigns_complete']}/{t['campaigns_planned']}个计划campaign完成，"
        f"{t['batches_complete']}/{t['batches_planned']}批终检，"
        f"{t['operations']}/{t['operations_planned']}个计划动作执行；"
        "2个动作前接入失败、3个上游缺失位仍在分母中。",
        "23条完整轨迹的资源核对与tolerance=0精确重放全部通过；另2个空轨迹重放未通过。"
        "当前有效版本覆盖23/23条件、75/75批；这是跨修复块汇总，不能替换累计尝试分母。",
        f"两块实验与重放墙钟共{payload['elapsed_seconds'] / 60:.2f}分钟，不含开发/测试耗时。"
        "零provider、块内零重试；PA另有5个明确的修复复测条件。"
        "首次直接脚本启动的导入错误另存launcher_error，发生在实验前，物理动作0。",
        "",
        "| 原块条件 | 保留终态 |",
        "| --- | --- |",
    ]
    for f in failures:
        lines.append(f"| {f['card']}-{f['stage']} | {f['failure']} |")
    lines += [
        "",
        "## 这些结果还不能说明什么",
        "",
        "当前O/A/M仅验证局部档案资料的传递、物理不变性和反证可达性。"
        "A来自指定条件的带噪付费标定，M把另一个指定条件的读数错配到相同条件；"
        "不是隐藏真值、完整机理先验，也不是已经冻结的正式三臂内容。"
        "已提示条件不能算后续盲测，全部标定与复测均为开发数据。",
        "当前固定脚本不会自主探索，因而无法回答Agent是否寻找反证、是否修正机制、"
        "是否丢失实验信息。完整机理可辨识性、自由K1交付、隔离Q盲测、K2访谈、"
        "LLM评审校准及真实provider全链仍待验证；新27来源主比较尚未就绪。",
        "",
        "## 可复查输出",
        "",
        "- [第一固定块](work-ii-gate-repair-20260916.md) · "
        "[机器数据](work-ii-gate-repair-20260916.json) · "
        "[事前说明](../WORK_II_GATE_REPAIR_NOTE.md)",
        "- [PA独立复测](work-ii-pa-gate-repair-20260916.md) · "
        "[机器数据](work-ii-pa-gate-repair-20260916.json) · "
        "[事前说明](../WORK_II_PA_GATE_REPAIR_NOTE.md)",
        "- [本汇总机器数据](work-ii-gate-repair-summary-20260916.json)",
        "",
    ]
    path.with_suffix(".md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"total": t, "current": c}), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--summarize-only", action="store_true")
    parser.add_argument("--pa-followup", action="store_true")
    parser.add_argument("--closeout-only", action="store_true")
    args = parser.parse_args()
    if args.closeout_only:
        closeout()
        return
    codes = ("PA",) if args.pa_followup else tuple(TASKS)
    note = "workstreams/flagship_tasks/WORK_II_PA_GATE_REPAIR_NOTE.md" if args.pa_followup else NOTE
    root = ROOT / (
        "runs/development/work-ii-pa-gate-repair-20260916"
        if args.pa_followup
        else "runs/development/work-ii-gate-repair-20260916"
    )
    report_path = (
        REPORT.with_name("work-ii-pa-gate-repair-20260916.json") if args.pa_followup else REPORT
    )
    total = sum(4 + int(c in SHIFTS) for c in codes)
    batch_count = sum(len(recipes(c)) * (1 + int(c in SHIFTS)) + 6 for c in codes)
    if args.summarize_only:
        cells = json.loads((root / "cells.json").read_text(encoding="utf-8"))
        elapsed = json.loads((root / "timing.json").read_text(encoding="utf-8"))["elapsed_seconds"]
    else:
        root.mkdir(parents=True, exist_ok=False)
        (root / "experiment_note.md").write_bytes((ROOT / note).read_bytes())
        write(
            root / "block_plan.json",
            {
                "recipes": {c: recipes(c) for c in codes},
                "budgets": BUDGETS,
                "anchors": ANCHORS,
                "shifts": SHIFTS,
                "pairs": PAIRS,
                "seed": 0,
                "observation_seed": 1,
                "planned_campaigns": total,
                "planned_batches": batch_count,
            },
        )
        progress = {
            "completed": 0,
            "total": total,
            "stage": "start",
            "unit": "none",
            "operations": 0,
        }
        start = time.monotonic()
        stop = threading.Event()

        def heartbeat():
            while not stop.wait(20):
                elapsed = time.monotonic() - start
                rate = progress["completed"] / elapsed
                print(
                    json.dumps(
                        {
                            **progress,
                            "elapsed_s": round(elapsed, 1),
                            "campaigns_per_min": round(rate * 60, 2),
                            "eta_s": round((total - progress["completed"]) / rate, 1)
                            if rate
                            else None,
                        }
                    ),
                    flush=True,
                )

        thread = threading.Thread(target=heartbeat, daemon=True)
        thread.start()
        cells = []
        try:
            for code in codes:
                base = execute(root, code, "base", None, progress)
                cells.append(base)
                progress["completed"] += 1
                write(root / "cells.json", cells)
                if code in SHIFTS:
                    cells.append(execute(root, code, "shift", None, progress))
                    progress["completed"] += 1
                    write(root / "cells.json", cells)
                target, counter = ANCHORS[code]
                available = len(base["metrics"]) > max(target, counter)
                for arm in ("O", "A", "M"):
                    if available:
                        prior = (
                            None
                            if arm == "O"
                            else {
                                "scope_actions": recipes(code)[target],
                                "metric": METRICS[code],
                                "estimate": round(
                                    base["metrics"][target if arm == "A" else counter][
                                        METRICS[code]
                                    ],
                                    6,
                                ),
                                "half_width": cutoff(METRICS[code]),
                            }
                        )
                        cell = execute(root, code, arm, prior, progress)
                    else:
                        cell = {
                            "card": code,
                            "stage": arm,
                            "failure": "upstream_missing",
                            "runtime_passed": False,
                            "packet_delivered": False,
                            "received_packet": None,
                            "planned_batches": 2,
                            "completed_batches": 0,
                            "planned_operations": sum(
                                len(recipes(code)[i]) for i in (target, counter)
                            ),
                            "operations": 0,
                            "metrics": [],
                            "resources": {"passed": False},
                            "replay": {"verified": False},
                        }
                    cells.append(cell)
                    progress["completed"] += 1
                    write(root / "cells.json", cells)
                    print(
                        json.dumps(
                            {
                                **progress,
                                "runtime_passed": cell["runtime_passed"],
                                "failure": cell["failure"],
                            }
                        ),
                        flush=True,
                    )
            elapsed = time.monotonic() - start
            write(root / "timing.json", {"elapsed_seconds": elapsed})
        finally:
            stop.set()
            thread.join(timeout=1)
    report = summarize(root, cells, elapsed, codes=codes, note=note)
    write(report_path, report)
    report_path.with_suffix(".md").write_text(render(report), encoding="utf-8")
    print(json.dumps(report["counts"]), flush=True)


if __name__ == "__main__":
    main()
