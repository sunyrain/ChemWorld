"""One PA development source with a chosen batch budget and sealed K1/Q/K2."""
# ruff: noqa: RUF001

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import sys
import tempfile
import threading
import time
from pathlib import Path

import gymnasium as gym
from scripts.report_work_ii_ec_dual_goal_trial import model_tool_transcript
from scripts.run_work_ii_astra_single_trial import read, write
from scripts.run_work_ii_ec_dual_goal_trial import (
    PROVIDER,
    FreeResearchAgent,
    replay_with_progress,
    summaries,
)
from scripts.run_work_ii_final_diagnostic import build_command, launch

from chemworld.agents.interactive_codex_experiment import InteractiveCodexExperimentAgent
from chemworld.campaign_resources import CampaignResourceCard
from chemworld.data.logging import load_jsonl
from chemworld.eval.runner import run_agent
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.materials import public_material_catalog
from chemworld.runtime.phase_ledger_services import ChemWorldPhaseLedgerServices
from chemworld.runtime.species import MechanismSpeciesView
from chemworld.tasks import get_task
from chemworld.world.instruments import instrument_contracts
from chemworld.world.operations import operation_contracts
from chemworld.world.separation_kernel import downstream_truth_values
from chemworld.world.species_roles import PHASE_PRODUCT_AMOUNT_KEY

ROOT = Path(__file__).resolve().parents[1]
TASK = "partition-discovery"
METRICS = ("product_in_organic", "product_in_aqueous")
GOAL = (
    "Discover and test a predictive explanation of target partition between the two phases, "
    "including material pairing, phase amounts and mixing. Choose twelve experiments freely. "
    "Explain evidence, alternatives and limits. Predict new conditions and phase-retention "
    "decisions after the campaign. Native score is not this task's objective. "
    "No best recipe, prescribed law, or belief checkpoints are required."
)
SYSTEM = """You are an autonomous scientist studying two-phase partition in a simulated lab.
Use only chemworld_lab and public_numerics. No filesystem, network, repository, hidden physics,
or general code execution is available. First read material_information. Follow research_goal.
Conduct 12 independent batches from the same initial mixture; conditions and repetition are
your choice. You have 12 additional instrument uses shared across batches and 12 final assays.
Follow actual tool schemas, legal operation ranges, and operational_state. Read all purchased
measurement outputs; preserve their batch, timing, and whether a phase has already been removed.
HPLC before separate_phase provides the two-phase readings. product_in_organic and
product_in_aqueous are fractions of this batch's fixed initial target inventory, NOT concentrations.
phase_ratio means organic volume divided by total two-phase volume. Solvent addition and initial
liquid contribute to actual volumes; an aqueous addition is not the entire aqueous volume.
separate_phase retains the requested phase and removes the other; it is not a sampling switch.
Instrument noise and sampling affect observed closure. Do not infer missing measurements as zero.
Use the current lawful workflow; explicitly terminate and measure final_assay for each batch.
An ended batch is not an ended campaign: use next_state until campaign_ended=true, then stop step.
There are no mandatory belief snapshots or fixed mechanism templates. After campaign terminal
return only status/summary JSON with a brief completion handoff; no best-batch recommendation.
Later turns request your mechanism, blind predictions and reflection. Do not answer them early.
Anonymous IDs are independent categories, not ordered numbers or real chemical identities.
You may use the public calculator to fit your own relationships within its supported operations.
No particular discovery or high score is required; report uncertainty and unavailable evidence.
"""
K1 = """实验已结束。请用中文说明你认为本体系的分配规律是什么，哪些具体批次和测量支持它，
资料与实验各贡献了什么，以及还有哪些竞争解释或适用范围不能确定。表达形式自由，不要求预定
方程；不要重抄整张数据表。区分观察、推断与猜测。返回report字段。本报告先封存，再给预测题。"""
K2 = """机理报告和预测均已封存，尚未反馈真值。请用中文回答三点，引用批号并避免重复全文：
1. 最可能出错或尚未验证的一条初始资料/自建规律是什么？没有实例先验就说明没有。
2. 若再给一次实验，你会怎么做、测什么来区分主要解释与替代解释？不同结果怎样改变判断？不执行。
3. 哪些已有证据未被充分利用，哪些预测最不可靠，报告和预测有无不一致？
事后反思不冒充当时记录，不修改此前交付。返回report字段。"""


def study_goal(batches=12):
    return GOAL.replace("twelve", str(batches)) if batches != 12 else GOAL


def source_system(batches=12):
    return SYSTEM.replace("12", str(batches))


def resource_card(batches=12):
    operations = 30 * batches
    return CampaignResourceCard(
        card_id="pa-free-research-twelve-v1" if batches == 12 else f"pa-free-research-{batches}-v1",
        operation_attempt_limit=operations,
        vessel_start_limit=batches,
        final_assay_limit=batches,
        nonfinal_instrument_use_limit=batches,
        stock_limits={
            "reagent_mol": 0.04 * operations,
            "solvent_L": 0.08 * operations,
            "phase_liquid_L": 0.06 * operations,
            "extractant_L": 0.06 * operations,
        },
        process_time_limit_s=None,
    )


def recipe(s, x, aq=0.015, org=0.019, duration=900, rpm=1200):
    return [
        {"operation": "add_solvent", "solvent": s, "volume_L": 0.020},
        {"operation": "add_phase", "phase": "aqueous", "volume_L": aq},
        {"operation": "add_extractant", "extractant": x, "volume_L": org},
        {"operation": "mix", "duration_s": duration, "stirring_speed_rpm": rpm},
        {"operation": "settle", "duration_s": 300},
        {"operation": "measure", "instrument": "hplc"},
        {"operation": "separate_phase", "target_phase": "organic"},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


def queries():
    recipes = [
        recipe(0, 0, 0.030, 0.008),
        recipe(0, 0, 0.030, 0.030),
        recipe(0, 3, 0.030, 0.008),
        recipe(0, 3, 0.030, 0.030),
        recipe(0, 0),
        recipe(0, 3),
        recipe(2, 0),
        recipe(2, 3),
        recipe(0, 0, duration=120, rpm=700),
        recipe(0, 0, duration=1200, rpm=700),
        recipe(2, 3, duration=600, rpm=200),
        recipe(2, 3, duration=600, rpm=1200),
    ]
    return [{"query_id": f"Q{i:02d}", "actions": r} for i, r in enumerate(recipes, 1)]


class PAAgent(FreeResearchAgent):
    def __init__(self, *, batches=12, **kwargs):
        self.batches = batches
        super().__init__(goal="discovery", **kwargs)
        self.belief_checkpoint_contract["final_recommendation_required"] = False

    def reset(self, task_info, seed):
        InteractiveCodexExperimentAgent.reset(self, task_info, seed)
        task = get_task(TASK)
        self._task_contract.update(
            free_research_campaign=True,
            final_recommendation_required=False,
            research_goal=study_goal(self.batches),
            description=study_goal(self.batches),
            instrument_contracts={
                k: instrument_contracts()[k].to_dict() for k in task.allowed_instruments
            },
            operation_contracts={
                k: operation_contracts()[k].to_dict() for k in task.allowed_operations
            },
            study_budget=dict.fromkeys(
                ("complete_batches", "extra_measurements", "final_assays"), self.batches
            ),
            assessment_scope=["material pairing", "phase volumes", "mixing", "phase retention"],
        )
        self._task_contract_manifest = self.workspace.publish_task_contract(self._task_contract)

    def _command(self, *, instructions_path, schema_path):
        command = super()._command(instructions_path=instructions_path, schema_path=schema_path)
        instructions = source_system(self.batches)
        instructions_path.write_text(instructions, encoding="utf-8")
        (self.output / "source-instructions.txt").write_text(instructions, encoding="utf-8")
        for i, argument in enumerate(command):
            if argument.startswith("mcp_servers.chemworld_lab.enabled_tools="):
                command[i] = "mcp_servers.chemworld_lab.enabled_tools=" + json.dumps(
                    ["material_information", "status", "history", "inspect_artifact", "step"]
                )
        return command


class ReferenceCapture(gym.Wrapper):
    """Capture pre-sample reference truth without changing the public transition."""

    def __init__(self, env, output):
        super().__init__(env)
        self.output = output

    def reset(self, **kwargs):
        result = self.env.reset(**kwargs)
        base = self.unwrapped
        original = base.runtime.apply_transaction
        phases = ChemWorldPhaseLedgerServices(
            MechanismSpeciesView(base.scenario_instance.compiled_mechanism)
        )

        def capture(state, action):
            truth = None
            if action.get("operation") == "measure" and action.get("instrument") == "hplc":
                ledger = phases.phase_ledger(state)
                initial = sum(
                    state.species.initial_amounts_mol.get(s, 0)
                    for s in phases.product_candidate_species()
                )
                truth = downstream_truth_values(
                    state,
                    ledger,
                    initial_product_mol=initial,
                    product_amount_mol=sum(p[PHASE_PRODUCT_AMOUNT_KEY] for p in ledger.values()),
                )
            outcome = original(state, action)
            if truth is not None:
                self.output.append({k: truth[k] for k in (*METRICS, "phase_ratio")})
            return outcome

        base.runtime.apply_transaction = capture
        return result


def physics(agent, output, *, callback=None, truth=None):
    batches = agent.batches if isinstance(agent, PAAgent) else 12
    operations = 30 * batches
    return run_agent(
        env_id=get_task(TASK).env_id,
        agent=agent,
        task_id=TASK,
        world_split="public-test",
        objective="balanced",
        seed=0,
        agent_seed=0,
        observation_seed=0 if isinstance(agent, PAAgent) else 101,
        budget=operations,
        budget_override=operations,
        episode_mode_override="campaign",
        campaign_resource_card=resource_card(batches),
        material_information={"mode": "opaque_codes"},
        scoring_contract_id="partition-s0-extraction-efficiency-v3",
        observation_noise_mode="keyed",
        observation_noise_namespace="pa-sol-opaque-20260918-v1",
        output_path=output,
        step_callback=callback,
        env_wrapper=(lambda env: ReferenceCapture(env, truth)) if truth is not None else None,
        method_resource_limits={
            "operation_limit": operations,
            "complete_experiment_limit": batches,
            "wall_time_limit_s": 150 * batches,
            "model_call_limit": 1,
            "input_token_limit": 8000000 * batches // 12,
            "uncached_input_token_limit": 2000000 * batches // 12,
            "output_token_limit": 128000 * batches // 12,
            "training_environment_step_limit": 0,
        }
        if isinstance(agent, PAAgent)
        else None,
    )


def schema(stage):
    if stage != "Q":
        properties = {"report": {"type": "string"}}
    else:
        interval = {
            "type": "object",
            "additionalProperties": False,
            "properties": {k: {"type": "number"} for k in ("estimate", "lower90", "upper90")},
            "required": ["estimate", "lower90", "upper90"],
        }
        row = {"query_id": {"type": "string"}, **dict.fromkeys(METRICS, interval)}
        properties = {
            "predictions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": row,
                    "required": list(row),
                },
            },
            "D1_phase": {"type": "string", "enum": ["organic", "aqueous", "uncertain"]},
            "D2_query": {"type": "string", "enum": ["Q05", "Q06", "uncertain"]},
            "rationale": {"type": "string"},
        }
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": properties,
        "required": list(properties),
    }


def question(stage):
    if stage != "Q":
        return {"K1": K1, "K2": K2}[stage]
    return (
        "基于原研究，预测下列12个独立新批次首次HPLC取样前的真实两相目标物比例，"
        "分母是各批固定初始目标量。每项给点估计及90%不确定区间，区间针对无噪声物料比例，"
        "不要求预测随机仪器噪声。不得补实验或修改K1。只预测分相前，不预测选相后终检。"
        "D1：Q01保留哪一相能留下更多目标物？D2：同用量Q05/Q06哪套有机相目标物更多？"
        "两题可声明uncertain。共用一段简要依据，不逐题写长文。返回指定JSON。\n"
        + json.dumps(queries(), ensure_ascii=False)
    )


def posttest(agent, folder, stage, thread_id, progress):
    workspace = agent.home_root / "followup"
    workspace.mkdir(exist_ok=True)
    schema_path = workspace / f"{stage}-schema.json"
    write(schema_path, schema(stage))
    instructions = workspace / "instructions.md"
    instructions.write_text(
        "Continue your own research from its actual recorded evidence. No laboratory access, "
        "filesystem, network or new experiments. Only public_numerics.calculate is available "
        "(8 calls per follow-up). Answer only this question; earlier outputs remain sealed.",
        encoding="utf-8",
    )
    audit = folder / f"{stage}-numerics.jsonl"
    command = build_command(
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
    result = launch(
        command,
        question(stage),
        workspace,
        agent.followup_environment,
        folder / stage,
        1200,
        True,
        audit,
        dict(progress),
    )
    if not result.get("payload"):
        result["failure"] = result.get("failure") or "missing_payload"
    write(folder / stage / "receipt.json", result)
    return result


def evaluate(payload, truth):
    try:
        rows = payload["predictions"]
        expected = [q["query_id"] for q in queries()]
        if sorted(r["query_id"] for r in rows) != expected:
            raise ValueError("missing or duplicated query IDs")
        by_id = {r["query_id"]: r for r in rows}
        scores = {}
        details = []
        for metric in METRICS:
            errors, coverage, widths, interval_scores = [], [], [], []
            for q in expected:
                item = by_id[q][metric]
                estimate, lo, hi = [float(item[k]) for k in ("estimate", "lower90", "upper90")]
                if not all(math.isfinite(v) for v in (estimate, lo, hi)) or not (
                    0 <= lo <= estimate <= hi <= 1
                ):
                    raise ValueError(f"invalid interval {q}/{metric}")
                target = truth[q][metric]
                error = abs(estimate - target)
                errors.append(error)
                coverage.append(lo <= target <= hi)
                widths.append(hi - lo)
                interval_scores.append(hi - lo + 20 * max(lo - target, target - hi, 0))
                details.append(
                    {
                        "query_id": q,
                        "metric": metric,
                        **item,
                        "truth": target,
                        "absolute_error": error,
                    }
                )
            scores[metric] = {
                "n": 12,
                "mae": sum(errors) / 12,
                "coverage90": sum(coverage) / 12,
                "mean_width90": sum(widths) / 12,
                "interval_score90": sum(interval_scores) / 12,
            }
        d1 = "organic" if truth["Q01"][METRICS[0]] > truth["Q01"][METRICS[1]] else "aqueous"
        d2 = max(("Q05", "Q06"), key=lambda q: truth[q][METRICS[0]])
        return {
            "valid": True,
            "metrics": scores,
            "details": details,
            "decisions": {
                "D1": {
                    "submitted": payload["D1_phase"],
                    "truth": d1,
                    "correct": payload["D1_phase"] == d1,
                },
                "D2": {
                    "submitted": payload["D2_query"],
                    "truth": d2,
                    "correct": payload["D2_query"] == d2,
                },
            },
        }
    except (TypeError, KeyError, ValueError) as exc:
        return {"valid": False, "failure": str(exc)}


def observations(records):
    result = []
    removed = set()
    for r in records:
        batch = int(r.get("experiment_index", 0)) + 1
        if r.get("transaction_status") != "committed":
            continue
        if r.get("action", {}).get("operation") == "separate_phase":
            removed.add(batch)
        if r.get("instrument"):
            result.append(
                {
                    "batch": batch,
                    "instrument": r["instrument"],
                    "before_phase_removal": batch not in removed,
                    "values": r.get("processed_estimate", {}),
                    "observed_mask": r.get("observed_mask", {}),
                }
            )
    return result


def source_execution_review(root, transcript):
    """Describe physical ordering separately from the model's script boundaries."""
    path = root / "source/source-stdout.jsonl"
    events = load_jsonl(path) if path.exists() else []
    active, completed = set(), set()
    maximum = 0
    identities = []
    for event in events:
        item = event.get("item", {})
        if item.get("type") != "mcp_tool_call":
            continue
        if item.get("tool") == "step":
            if event["type"] == "item.started":
                active.add(item["id"])
                maximum = max(maximum, len(active))
            elif event["type"] == "item.completed":
                completed.add(item["id"])
                active.discard(item["id"])
        if item.get("tool") == "material_information" and event["type"] == "item.completed":
            for block in (item.get("result") or {}).get("content", []):
                if block.get("type") != "text":
                    continue
                payload = json.loads(block["text"])
                for material in payload.get("material_catalog", {}).get("solvents", []):
                    if material.get("identity_kind", "").startswith("real_"):
                        identities.append(material["display_name"])
    scripts = []
    for entry in transcript:
        code = entry.get("input", "")
        if (
            entry.get("phase") == "source"
            and entry.get("type") == "custom_tool_call"
            and "mcp__chemworld_lab__step" in code
        ):
            scripts.append(
                {
                    "call_id": entry["call_id"],
                    "literal_action_count": len(re.findall(r"operation\s*:\s*[\"\']", code)),
                }
            )
    return {
        "completed_physical_step_calls": len(completed),
        "maximum_concurrent_physical_step_calls": maximum,
        "unfinished_step_calls": len(active),
        "model_authored_step_scripts": scripts,
        "script_counting_basis": "static action literals; inspect code for loops and branching",
        "physical_serialization_proves_model_redecision": False,
        "material_identity_exposure": identities,
        "strict_anonymous_opaque": False if identities else None,
        "identity_review_scope": "material_information response; absence is not certification",
    }


def legacy_twelve_report(result, records):
    source = result.get("source", {})
    reference = result.get("reference", {})
    review = result["execution_review"]
    turns = result.get("posttests", {})
    measured = observations(records)

    def count(instrument):
        return sum(r["instrument"] == instrument for r in measured)

    completed_posttests = sum(
        bool(t.get("payload")) and not t.get("failure") for t in turns.values()
    )
    lines = [
        "# PA单臂试跑：结果与实际决策方式",
        "",
        "2026-09-18；PA-W01；预定Opaque；GPT-5.6 Sol / medium；1来源，development。",
        "",
        "**运行链已完成，但不能作为严格匿名Opaque对照，也不能称为全程逐操作重新决策。** "
        "共享材料目录暴露真实名称；模型后续自主采用整批脚本，组批本身符合当时规则。"
        "保留原结果，不补跑其他臂。",
        "",
        "[完整提示、逐操作轨迹及K1/Q/K2原文](TRANSCRIPT.md) · "
        "[模型实际脚本与收到的输出](model-tools.json) · [机器汇总](summary.json)",
        "",
        "## 实际执行与计数",
        "",
        "| 项目 | 完成情况 |",
        "| --- | --- |",
        f"| Agent自主来源 | {source.get('completed_batches', 0)}/12批；"
        f"{source.get('operations', 0)}操作 |",
        f"| 来源测量 | {count('hplc')}/12分相前HPLC；{count('final_assay')}/12终检 |",
        f"| 固定参考 | {reference.get('completed_batches', 0)}/12批；"
        f"{reference.get('operations', 0)}操作；不送给Agent |",
        f"| 来源/参考精确重放 | {source.get('exact_replay', {})} / "
        f"{reference.get('exact_replay', {})} |",
        f"| 后测 | {completed_posttests}/3 （K1机理报告、Q预测、K2反思） |",
        f"| 来源事务回滚 | {len(source.get('rollbacks', []))} |",
        f"| 执行失败记录 | {result.get('failure')}；来源{source.get('failure')} |",
        "",
        "首次执行合计24物理批、228操作（来源12批/120操作，参考12批/108操作）。"
        "另有两条精确重放，共24批/228重放操作，不增加独立实验样本。无来源重启或provider重试。",
        "",
        "## 为什么输出是一组一组的",
        "",
        f"底层完成{review['completed_physical_step_calls']}次step，最大并发"
        f"{review['maximum_concurrent_physical_step_calls']}。但这只能证明物理操作串行。",
        "",
        "模型实际提交了10段单操作脚本（第1批），以及11段各含10操作的整批脚本（第2—12批）。"
        "后者先写好加料→加介质→加水相→加萃取剂→混合→静置→HPLC→保留有机相→终止→终检，"
        "脚本await每步后继续，末尾才text测量摘要；HPLC结果没有触发新的模型决策，"
        "脚本也没有按测量数值选择后续操作的分支。等待脚本的wait不等于新增科学决策。",
        "",
        "因此，本轮允许并实现了批间反馈：上一批结果返回后再提交下一批条件；"
        "不能宣称批内每个操作都由模型读取上一结果后重新选择，更不能由串行性证明反馈的因果利用。"
        "12批来源配方并非运行器预设，分组对照是Agent自己的策略。"
        "固定的12道Q题仅用于事后预测与后台参考。",
        "",
        "第2批脚本还误从顶层latest_measurement读取数据，打印的meas全部为null；"
        "随后Agent在第3批前调用history找回实际观测，第3批起改读processed_estimate。"
        "这是一次被自行纠正的证据摘要错误，不是模拟器没有产生测量。",
        "",
        "source model_call_count=1表示一个持久研究会话，不是仅一次底层推理；"
        "底层推理次数未完整计数。公开工具可以用JavaScript编排，"
        "不等于获得了文件、网络、仓库或任意外部程序访问。",
        "",
        "## 十二批自主选择与结果",
        "",
        "每批追加试剂0.02 mol，静置300 s，分相前HPLC，之后均保留有机相。"
        "下表为实际追加体积，不把水相追加量误当总水相量；读数含仪器噪声。",
        "",
        "| 批次 | S/X | 介质/水相/有机相追加mL | 混合s/rpm | HPLC有机/水相比例 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for batch in range(1, source.get("completed_batches", 0) + 1):
        batch_records = [r for r in records if int(r.get("experiment_index", 0)) + 1 == batch]
        actions = {r["action"]["operation"]: r["action"] for r in batch_records}
        solvent, extractant, mix = [actions[k] for k in ("add_solvent", "add_extractant", "mix")]
        hplc = next(
            r["values"] for r in measured if r["batch"] == batch and r["instrument"] == "hplc"
        )
        volumes = "/".join(
            f"{actions[k]['volume_L'] * 1000:g}"
            for k in ("add_solvent", "add_phase", "add_extractant")
        )
        lines.append(
            f"| {batch} | S{solvent['solvent']}/X{extractant['extractant']} | {volumes} | "
            f"{mix['duration_s']:g}/{mix['stirring_speed_rpm']:g} | "
            f"{hplc[METRICS[0]]:.4f}/{hplc[METRICS[1]]:.4f} |"
        )
    lines += [
        "",
        "1—4批固定S0筛X；5—7批固定X3换S；第8批补S1/X1交叉；9—10批变相量；"
        "11—12批变混合。各批条件没有重复，最后两批同时改变时长和转速，不能独立归因。",
        "",
        "## 后测与预测质量",
        "",
        "K1先封存自由机理报告，Q一次提交12条件×2互补指标及2个决策，最后K2三问。"
        "后测无新实验、无真值反馈；24个标量预测不是24个独立样本。",
        "",
        "| 指标 | 题数 | MAE | 90%区间覆盖 | 平均区间宽度 |",
        "| --- | --- | --- | --- | --- |",
    ]
    evaluation = result.get("prediction_evaluation", {})
    for metric, score in evaluation.get("metrics", {}).items():
        lines.append(
            f"| {metric} | {score['n']} | {score['mae']:.5f} | "
            f"{score['coverage90']:.1%} | {score['mean_width90']:.5f} |"
        )
    for name, decision in evaluation.get("decisions", {}).items():
        lines += [
            "",
            f"{name}：提交{decision['submitted']}，真值{decision['truth']}，"
            f"正确={decision['correct']}。",
        ]
    lines += [
        "",
        "最大误差Q07：未实测S2/X0组合，有机相预测0.497，真值0.678095，误差18.11个百分点。"
        "全部区间覆盖真值，但平均宽29.08个百分点，不能将高覆盖当成精确恢复机制。",
        "",
        "K1能区分材料、相量与混合效应，并承认交互、恒定分配系数和混合曲线未定。"
        "Q仍使用近似加性与对数混合插值；K2主动指出这些未经验证的假设和Q07风险。"
        "K2建议加做600 s/200 rpm以区分时长和转速，但本轮未执行。",
        "",
        "K1也有待纠正的表达：两相字段是以固定初始目标量为分母的比例，"
        "应区分该物理定义与带噪读数；部分批次水相多于有机相，"
        "不能笼统说所有条件下均偏向有机相。所有终点选择有机相只说明操作策略，"
        "本任务是机理探索，不能自动按产率优化失败评分。",
        "",
        "Q的低相量、未见材料组合、较长混合时长包含外推；"
        "参考配方未追加来源中的0.02 mol试剂、体积也不同。"
        "题目事前固定，不能把这12题称为12组严格配平的单因素因果比较。",
        "",
        "## 耗时与资源",
        "",
        f"来源{source.get('elapsed_s', 0) / 60:.2f}分钟；"
        + "；".join(
            f"{stage} {turns.get(stage, {}).get('elapsed_s', 0):.2f}秒"
            for stage in ("K1", "Q", "K2")
        )
        + f"。完整执行{result.get('elapsed_s', 0) / 60:.2f}分钟，"
        "包含参考、重放与调度，不含接入开发。",
        "",
        "来源累计输入1,215,393 token（缓存1,160,832），输出6,050。"
        "K2结束的同线程累计输入1,544,640（缓存1,369,728），输出15,829；"
        "各后测usage是累计值，不能相加。美元费用未能归属，不将账本占位0解释为免费。",
        "",
        *token_table(result["token_accounting"]),
        "",
        "## 保留的偏差与下一步",
        "",
        "1. 匿名性缺陷：material_information虽无实例dossier，却给出Water、Ethanol、"
        "Acetonitrile、Toluene，操作choice_labels也有真实名称；K1实际使用了这些名称。"
        "没有证据显示完整隐藏搭配表泄露，但严格匿名Opaque已不成立。后续须统一PA的S/X目录、"
        "初始提示和操作标签；本轮按有身份信息暴露的开发记录保留。",
        "2. 自主调度：保留单批或成组实验，不要求先交组计划，也不强制每次测量或批末"
        "触发模型反思。撤回此前必须逐测量/逐批交回模型的建议。三臂保持相同权限；"
        "组大小、脚本内条件分支、结果何时送达与何时重规划分别记录。"
        "串行操作、工具调用数和token不能当作思考次数。",
        "3. 证据交付：测量须稳定返回batch、instrument、时点、processed_estimate与observed_mask；"
        "保留模型实际看到的摘要，不能只凭底层轨迹断言观测已送达。",
        "",
        "本轮说明一臂12批加轻量后测能完成，也暴露接入问题；"
        "单来源尚不能建立三臂差异或系统性信息损失结论。",
        "",
    ]
    return "\n".join(lines)


def token_accounting(result):
    """Same-thread follow-up usage is cumulative, not additive across stages."""
    usage = result.get("source", {}).get("usage", {})
    snapshots = []
    if usage.get("provider_token_accounting_complete"):
        snapshots.append(
            (
                "source",
                {
                    "input": usage["input_token_count"],
                    "cached_input": usage["cached_input_token_count"],
                    "output": usage["output_token_count"],
                },
            )
        )
    for stage in ("K1", "Q", "K2"):
        usage = result.get("posttests", {}).get(stage, {}).get("usage") or {}
        if all(k in usage for k in ("input_tokens", "cached_input_tokens", "output_tokens")):
            snapshots.append(
                (
                    stage,
                    {
                        "input": usage["input_tokens"],
                        "cached_input": usage["cached_input_tokens"],
                        "output": usage["output_tokens"],
                    },
                )
            )
    rows, previous = [], dict.fromkeys(("input", "cached_input", "output"), 0)
    for stage, current in snapshots:
        delta = {k: current[k] - previous[k] for k in current}
        if any(v < 0 for v in delta.values()) or delta["cached_input"] > delta["input"]:
            return {"valid": False, "reason": "usage is not monotone cumulative", "stage": stage}
        rows.append(
            {"stage": stage, **delta, "uncached_input": delta["input"] - delta["cached_input"]}
        )
        previous = current
    return {
        "valid": bool(snapshots),
        "complete": [s for s, _ in snapshots] == ["source", "K1", "Q", "K2"],
        "basis": "cumulative thread snapshots differenced in source/K1/Q/K2 order",
        "stages": rows,
        "total": {
            **previous,
            "uncached_input": previous["input"] - previous["cached_input"],
            "input_plus_output": previous["input"] + previous["output"],
        },
        "monetary_cost_usd": None,
    }


def token_table(accounting):
    lines = [
        "| 阶段 | 输入 | 其中缓存输入 | 非缓存输入 | 输出 |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for row in accounting.get("stages", []) + (
        [{"stage": "合计", **accounting["total"]}] if accounting.get("valid") else []
    ):
        lines.append(
            f"| {row['stage']} | "
            + " | ".join(
                f"{row[k]:,}" for k in ("input", "cached_input", "uncached_input", "output")
            )
            + " |"
        )
    return lines


def concise_report(result, records):
    source = result.get("source", {})
    review = result["execution_review"]
    planned = result.get("planned_source_batches", 12)
    measured = observations(records)
    completed_posttests = sum(
        bool(t.get("payload")) and not t.get("failure")
        for t in result.get("posttests", {}).values()
    )
    lines = [
        f"# PA {planned}批单臂预算诊断",
        "",
        "PA-W01；GPT-5.6 Sol / medium；单来源开发诊断。",
        "本报告的身份暴露判定来自保留的实际输入；自主编排脚本本身不是协议缺陷。",
        "检测到真实名称：本轮不能作为严格匿名Opaque。"
        if review["material_identity_exposure"]
        else "未在已检查的材料回复中发现真实名称；这不替代完整实际输入核对。",
        "",
        "[完整提示和问答](TRANSCRIPT.md) · [实际模型工具输入输出](model-tools.json) · "
        "[机器汇总](summary.json)",
        "",
        f"执行状态：{result['status']}；来源{source.get('completed_batches', 0)}/{planned}批，"
        f"{source.get('operations', 0)}操作；后测"
        f"{completed_posttests}/3。",
        f"来源回滚{len(source.get('rollbacks', []))}；失败记录：{result.get('failure')}，"
        f"来源{source.get('failure')}。",
        f"HPLC {sum(r['instrument'] == 'hplc' for r in measured)}次；"
        f"终检{sum(r['instrument'] == 'final_assay' for r in measured)}次。",
        "",
        f"参考复用：{result.get('reference_reused_from')}；12题旧参考不计新增物理批。"
        f"本轮新增来源{source.get('completed_batches', 0)}批，来源精确重放另计："
        f"{source.get('exact_replay', {})}。",
        "",
        f"来源{source.get('elapsed_s', 0) / 60:.2f}分钟；"
        f"整链{result.get('elapsed_s', 0) / 60:.2f}分钟。后测："
        + "，".join(
            f"{s} {result.get('posttests', {}).get(s, {}).get('elapsed_s', 0):.2f}秒"
            for s in ("K1", "Q", "K2")
        ),
        "",
        "## 预测",
        "",
        "12条件、24个互补标量预测，不是24个独立样本。以下仅列有机相，水相另见完整记录。",
        "",
        "| 题目 | 预测 | 真值 | 绝对误差 | 90%区间 |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    evaluation = result.get("prediction_evaluation", {})
    for row in evaluation.get("details", []):
        if row["metric"] == METRICS[0]:
            lines.append(
                f"| {row['query_id']} | {row['estimate']:.4f} | {row['truth']:.4f} | "
                f"{row['absolute_error']:.4f} | {row['lower90']:.3f}—{row['upper90']:.3f} |"
            )
    lines += [
        "",
        "```json",
        json.dumps(
            {k: evaluation.get(k) for k in ("metrics", "decisions")}, ensure_ascii=False, indent=2
        ),
        "```",
        "",
        "## Token",
        "",
        *token_table(result["token_accounting"]),
        "",
        "输入含缓存命中；后测为累计值之差，推理token已在输出口径中，不另加。"
        "参考与重放不调用模型，美元费用不可归属。",
        "",
        "## 实际决策接口",
        "",
        f"已完成step {review['completed_physical_step_calls']}，最大物理并发"
        f"{review['maximum_concurrent_physical_step_calls']}；这不证明每步由模型重新决策。",
        f"模型step脚本的静态操作字面量数："
        f"{[s['literal_action_count'] for s in review['model_authored_step_scripts']]}。"
        "循环/分支须结合实际脚本复核，不能直接将静态计数当物理操作数。",
        "",
        f"实际公开材料身份：{review['material_identity_exposure']}。",
        "",
    ]
    return "\n".join(lines)


def export(root, out):
    result = read(root / "result.json")
    out.mkdir(parents=True, exist_ok=True)
    records = (
        load_jsonl(root / "source/trajectory.jsonl")
        if (root / "source/trajectory.jsonl").exists()
        else []
    )
    tools = model_tool_transcript(root / "source")
    result["execution_review"] = source_execution_review(root, tools)
    result["token_accounting"] = token_accounting(result)
    write(out / "summary.json", result)
    write(out / "model-tools.json", tools)
    lines = [
        "# PA Opaque单臂开发试跑",
        "",
        "开发结果，非正式三臂证据。匿名性检查与实际脚本决策粒度见[结果解释](REPORT.md)。",
        "",
        f"状态：{result['status']}；模型GPT-5.6 Sol / medium，PA-W01。",
        f"参考批次：{result['reference'].get('completed_batches', 0)}/12；"
        f"来源批次：{result.get('source', {}).get('completed_batches', 0)}/"
        f"{result.get('planned_source_batches', 12)}。",
        "",
        "## 逐批公开观测",
        "",
        "| 批次 | 仪器 | 分相前 | 有机相目标比例 | 水相目标比例 | 相体积分数 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in observations(records):
        vals = row["values"]
        numbers = [
            f"{vals[k]:.4f}" if isinstance(vals.get(k), int | float) else "—"
            for k in (*METRICS, "phase_ratio")
        ]
        lines.append(
            f"| {row['batch']} | {row['instrument']} | "
            f"{row['before_phase_removal']} | " + " | ".join(numbers) + " |"
        )
    saved_instructions = root / "source/source-instructions.txt"
    lines += [
        "",
        "## 完整源提示",
        "",
        "```text",
        saved_instructions.read_text(encoding="utf-8") if saved_instructions.exists() else SYSTEM,
        "```",
    ]
    prompt = root / "source/source-prompt.txt"
    if prompt.exists():
        lines += ["", "```json", prompt.read_text(encoding="utf-8"), "```"]
    lines += [
        "",
        "## 自主操作与实际工具输入输出",
        "",
        "[实际模型工具输入输出](model-tools.json)，包含工具调用脚本及其实际返回内容。",
        "",
        "```json",
        json.dumps(
            [
                {
                    "batch": int(r.get("experiment_index", 0)) + 1,
                    "action": r.get("action"),
                    "status": r.get("transaction_status"),
                    "observation": r.get("processed_estimate"),
                    "observed_mask": r.get("observed_mask"),
                }
                for r in records
            ],
            ensure_ascii=False,
            indent=2,
        ),
        "```",
    ]
    for stage in ("K1", "Q", "K2"):
        turn = result.get("posttests", {}).get(stage, {})
        lines += [
            "",
            f"## {stage} 输入",
            "",
            read(root / "design.json").get(stage, question(stage)),
            "",
            f"## {stage} 输出",
            "",
            "```json",
            json.dumps(turn.get("payload"), ensure_ascii=False, indent=2),
            "```",
        ]
    lines += [
        "",
        "## 预测评价及完整计数",
        "",
        "```json",
        json.dumps(
            {k: v for k, v in result.items() if k != "posttests"}, ensure_ascii=False, indent=2
        ),
        "```",
        "",
    ]
    (out / "TRANSCRIPT.md").write_text("\n".join(lines), encoding="utf-8")
    report = (
        legacy_twelve_report(result, records)
        if root.name == "pa-sol-opaque-20260918-v1"
        else concise_report(result, records)
    )
    if (out / "ANALYSIS.md").exists():
        report += "\n\n[轨迹、机理及比较边界的人工复核](ANALYSIS.md)\n"
    (out / "REPORT.md").write_text(report, encoding="utf-8")


def execute(root, progress, *, batches=12, reference_run=None):
    root.mkdir(parents=True, exist_ok=False)
    write(
        root / "design.json",
        {
            "model": PROVIDER,
            "world": "PA-W01",
            "arm": "Opaque",
            "public_catalog_version": public_material_catalog(task_id=TASK)["catalog_version"],
            "sources": 1,
            "source_batches": batches,
            "reference_reused_from": str(reference_run) if reference_run else None,
            "queries": queries(),
            "resources": resource_card(batches).to_dict(),
            "system": source_system(batches),
            "goal": study_goal(batches),
            "K1": K1,
            "Q": question("Q"),
            "K2": K2,
        },
    )
    result = {
        "status": "failed",
        "development_only": True,
        "formal_result": False,
        "planned_sources": 1,
        "planned_source_batches": batches,
        "planned_reference_batches": 12,
        "new_reference_batches": 0 if reference_run else 12,
        "reference_reused_from": str(reference_run) if reference_run else None,
        "posttests": {},
        "failure": None,
    }
    started = time.monotonic()
    progress.update(stage="reference", operations=0, batches=0, planned_batches=12)

    def callback(record, trace):
        del trace
        progress["operations"] += 1
        if record.info.get("instrument") == "final_assay" and (
            record.info.get("transaction_status") == "committed"
        ):
            progress["batches"] += 1
        print(
            json.dumps(
                {
                    "stage": progress["stage"],
                    "operations": progress["operations"],
                    "batches": progress["batches"],
                    "planned_batches": progress["planned_batches"],
                    "action": record.action,
                }
            ),
            flush=True,
        )

    reference_truth = []
    try:
        if reference_run:
            old_design = read(reference_run / "design.json")
            saved = read(reference_run / "reference-result.json")
            if old_design["queries"] != queries() or not saved.get("passed"):
                raise ValueError("reference mismatch or failed historical reference")
            shutil.copyfile(reference_run / "reference.jsonl", root / "reference.jsonl")
            reference_truth = [saved["truth"][q["query_id"]] for q in queries()]
            reference_replay = saved["exact_replay"]
            print(
                json.dumps({"stage": "reference_reused", "batches": 12, "new_physical_batches": 0}),
                flush=True,
            )
        else:
            physics(
                _FrozenTruthReplayAgent([a for q in queries() for a in q["actions"]]),
                root / "reference.jsonl",
                callback=callback,
                truth=reference_truth,
            )
            reference_replay = replay_with_progress(
                load_jsonl(root / "reference.jsonl"), "reference"
            )
        records = load_jsonl(root / "reference.jsonl")
        measured = [r for r in observations(records) if r["instrument"] == "hplc"]
        reference = {
            "completed_batches": len(summaries(records)),
            "operations": len(records),
            "exact_replay": reference_replay,
            "truth": dict(zip([q["query_id"] for q in queries()], reference_truth, strict=True)),
            "measurements": measured,
        }
        reference["passed"] = (
            reference["completed_batches"] == 12
            and len(measured) == 12
            and reference["exact_replay"].get("verified") is True
            and all(r.get("transaction_status") == "committed" for r in records)
            and all(abs(t[METRICS[0]] + t[METRICS[1]] - 1) <= 1e-8 for t in reference_truth)
            and all(
                m["before_phase_removal"]
                and all(
                    m["observed_mask"].get(k) is True and math.isfinite(m["values"][k])
                    for k in (*METRICS, "phase_ratio")
                )
                for m in measured
            )
        )
        result["reference"] = reference
        if not reference["passed"]:
            raise RuntimeError("reference functional checks failed; source not started")
        write(root / "reference-result.json", reference)
    except Exception as exc:
        result.setdefault("reference", {"completed_batches": progress["batches"]})
        result["failure"] = {"stage": "reference", "type": type(exc).__name__, "message": str(exc)}
        write(root / "result.json", result)
        return
    folder = root / "source"
    folder.mkdir()
    write(folder / "attempt.json", {"started_epoch": time.time(), "planned_attempts": 1})
    progress.update(
        stage="source",
        operations=0,
        batches=0,
        planned_batches=batches,
        stage_started=time.monotonic(),
    )
    source_started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="chemworld-research-") as temporary:
        agent = PAAgent(
            batches=batches,
            home_root=Path(temporary),
            output=folder,
            workspace=Path(temporary) / "laboratory",
            role_id="free_research",
            request_timeout_s=1200,
            finalization_timeout_s=300,
            session_wall_time_limit_s=150 * batches,
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
            session_progress_callback=lambda p: progress.update(provider_liveness=p),
        )
        source_failure = None
        try:
            physics(agent, folder / "trajectory.jsonl", callback=callback)
        except Exception as exc:
            source_failure = {"type": type(exc).__name__, "message": str(exc)}
        finally:
            agent.close()
        shutil.copytree(agent.workspace.root, folder / "workspace")
        records = (
            load_jsonl(folder / "trajectory.jsonl")
            if (folder / "trajectory.jsonl").exists()
            else []
        )
        receipts = agent.provider_receipts()
        write(folder / "source-receipts.json", receipts)
        last = receipts[-1] if receipts else {}
        source = {
            "status": "completed"
            if len(summaries(records)) == batches and not source_failure
            else "failed",
            "failure": source_failure,
            "completed_batches": len(summaries(records)),
            "operations": len(records),
            "observations": observations(records),
            "batches": summaries(records),
            "usage": agent.method_resource_usage(),
            "elapsed_s": time.monotonic() - source_started,
            "exact_replay": replay_with_progress(records, "source"),
            "rollbacks": [
                {"action": r.get("action"), "reason": r.get("rollback_reason")}
                for r in records
                if r.get("transaction_status") != "committed"
            ],
            "source_handoff": last.get("final_payload_summary"),
        }
        result["source"] = source
        write(root / "result.json", result)
        thread_id = last.get("thread_id")
        if (
            thread_id
            and last.get("final_payload_valid") is True
            and not last.get("provider_error_event_count", 0)
        ):
            for stage in ("K1", "Q", "K2"):
                progress.pop("provider_liveness", None)
                progress.update(stage=stage, stage_started=time.monotonic())
                turn = posttest(agent, folder, stage, thread_id, progress)
                result["posttests"][stage] = {
                    k: turn.get(k)
                    for k in (
                        "payload",
                        "failure",
                        "elapsed_s",
                        "usage",
                        "tool_events",
                        "exit_code",
                        "provider_errors",
                    )
                }
                write(root / "result.json", result)
                if turn.get("failure"):
                    result["failure"] = {"stage": stage, "message": turn["failure"]}
                    break
        else:
            result["failure"] = {
                "stage": "source",
                "message": "no intact terminal context",
                "details": source_failure,
            }
        sessions = agent.home_root / "codex-home/sessions"
        if sessions.exists():
            shutil.copytree(sessions, folder / "provider-rollouts")
        result["prediction_evaluation"] = evaluate(
            result["posttests"].get("Q", {}).get("payload"),
            reference["truth"],
        )
        result["status"] = (
            "completed"
            if (
                source["status"] == "completed"
                and source["exact_replay"].get("verified") is True
                and len(result["posttests"]) == 3
                and not result["failure"]
                and result["prediction_evaluation"].get("valid") is True
            )
            else "failed"
        )
    result["elapsed_s"] = time.monotonic() - started
    write(root / "result.json", result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--report-only", action="store_true")
    parser.add_argument("--batches", type=int, choices=(12, 24), default=12)
    parser.add_argument("--reference-run", type=Path)
    args = parser.parse_args()
    if args.report_only:
        export(args.output.resolve(), args.report.resolve())
        return
    progress = {"stage": "setup", "operations": 0, "batches": 0, "stage_started": time.monotonic()}
    stopped = threading.Event()

    def heartbeat():
        while not stopped.wait(30):
            elapsed = time.monotonic() - progress["stage_started"]
            n = progress["batches"]
            throughput = n / elapsed * 60 if elapsed > 0 and progress["stage"] == "source" else None
            print(
                json.dumps(
                    {
                        **progress,
                        "stage_elapsed_s": round(elapsed),
                        "batches_per_minute": throughput,
                        "source_eta_s": (progress.get("planned_batches", args.batches) - n)
                        / n
                        * elapsed
                        if n and throughput
                        else None,
                    }
                ),
                flush=True,
            )

    worker = threading.Thread(target=heartbeat, daemon=True)
    worker.start()
    try:
        execute(
            args.output.resolve(),
            progress,
            batches=args.batches,
            reference_run=args.reference_run.resolve() if args.reference_run else None,
        )
        export(args.output.resolve(), args.report.resolve())
    finally:
        stopped.set()
        worker.join(timeout=2)


if __name__ == "__main__":
    main()
