#!/usr/bin/env python3
"""Run the EQ-P five-world block with canonical K1/Q/K2 and sealed EQS."""
# ruff: noqa: E402, E501, RUF001

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
import threading
import time
from collections.abc import Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.run_work_ii_eq_bounded_equilibrium as v1

from chemworld.agents.diagnostic_numerics import FOLLOWUP_NUMERICS
from chemworld.data.logging import load_jsonl
from chemworld.eval.verify import verify_records

CONFIG = ROOT / "configs/benchmark/work_ii_eq_bounded_equilibrium_v2.0.json"
FREEZE = ROOT / "configs/benchmark/work_ii_eq_bounded_equilibrium_freeze_v2.0.json"
TASK = v1.TASK
ARMS = v1.ARMS
METRICS = v1.METRICS
PROVIDER = v1.PROVIDER
GOALS = v1.GOALS
SYSTEM = v1.SYSTEM.replace(
    "A separate same-thread sequence will request a full K1 report, fixed\nblind predictions, and K2 retrospective questions.",
    "A separate same-thread sequence will request a full K1 report, fixed\nblind predictions, K2 retrospective questions, and an EQ-specific structured supplement.",
)
POSTTEST_STAGES = ("K1", "Q", "K2", "EQS")

K1 = """实验阶段已结束，任务交付已经封存。现在请用英文提交完整、独立可读的机理报告。
请讲清你认为这个世界如何运行：关键变量、作用关系、耦合、可能的方程或过程；哪些实验使你形成或修改这个解释；说明解释适用范围、尚不能识别的因素和合理的竞争解释。
使用你认为最合适的自然语言、数学或伪代码，不要求任何预设模型形式，也不要求确定答案。
引用真实批次编号与数值，区分实际观测、外推和猜测；不补做实验，不编造未测信息。
请充分展开，不必压成短摘要。所有报告文本必须使用英文。返回JSON的report字段。此报告封存后才给预测题。"""

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

EQS = """K1, Q, and K2 are sealed, and no prediction truth, hidden parameter, arm label, or score has been shown. Complete the EQ-specific structured supplement in English using only evidence already acquired during the source campaign. Do not run an experiment and do not revise K1, Q, or K2.

1. Give one estimate and an 80% interval for the world's effective pKa if it is identifiable from your evidence. If it is not identifiable, abstain explicitly and explain the principal confounding factors.
2. Assess whether the final public responses are predominantly determined by the final amount/volume state or show reproducible dependence on staged-addition path. Cite actual batches and distinguish evidence from conjecture.
3. Assess whether the observed dissociation–precipitation relationship is continuous, threshold-like, mixed, or not identifiable within the studied range. State the supported range and the most important competing explanation.

Return the complete EQ supplement JSON. All rationale fields must be in English."""

read = v1.read
write = v1.write
digest = v1.digest
file_sha256 = v1.file_sha256
deterministic_seed = v1.deterministic_seed
resource_card = v1.resource_card
queries = v1.queries
world_by_id = v1.world_by_id
public_prior = v1.public_prior
research_brief = v1.research_brief
physics = v1.physics
reference_run = v1.reference_run
evaluate_predictions = v1.evaluate_predictions
EqFreeResearchAgent = v1.EqFreeResearchAgent
provider_shared = v1.provider_shared
shared = v1.shared


def load_config() -> dict[str, Any]:
    overlay = read(CONFIG)
    binding = overlay["base_config"]
    base_path = ROOT / binding["path"]
    if file_sha256(base_path) != binding["sha256"]:
        raise RuntimeError("EQ v2 overlay does not bind the current v1.1 base config")
    original = v1.CONFIG
    try:
        v1.CONFIG = base_path
        resolved = v1.load_config()
    finally:
        v1.CONFIG = original
    resolved.update(
        {
            "schema_version": overlay["schema_version"],
            "status": overlay["status"],
            "protocol": overlay["protocol"],
            "prior_locus": overlay["prior_locus"],
            "posttest_stages": copy.deepcopy(overlay["posttest_stages"]),
            "counts": copy.deepcopy(overlay["counts"]),
            "truth_embargo": overlay["truth_embargo"],
            "execution_order": copy.deepcopy(overlay["execution_order"]),
            "canary": copy.deepcopy(overlay["canary"]),
            "full_matrix": copy.deepcopy(overlay["full_matrix"]),
            "v2_overlay": copy.deepcopy(overlay),
        }
    )
    return resolved


def validate_design(config: Mapping[str, Any]) -> dict[str, Any]:
    expected = {
        "worlds": 5,
        "independent_source_sessions": 15,
        "source_batches_per_session": 12,
        "source_batches": 180,
        "posttests_per_session": 4,
        "posttests": 60,
        "reference_repeats_per_query": 5,
        "reference_executions": 300,
    }
    if config.get("counts") != expected:
        raise ValueError("EQ v2 frozen denominators changed")
    if tuple(config.get("posttest_stages", ())) != POSTTEST_STAGES:
        raise ValueError("EQ v2 posttest order changed")
    legacy_view = copy.deepcopy(dict(config))
    legacy_view["counts"] = {
        **expected,
        "posttests_per_session": 3,
        "posttests": 45,
    }
    return v1.validate_design(legacy_view)


def configure_provider_helpers(config: Mapping[str, Any]) -> None:
    v1.SYSTEM = SYSTEM
    v1.K1 = K1
    v1.Q_PROMPT = Q_PROMPT
    v1.K2 = K2
    v1.configure_provider_helpers(config)
    shared.SYSTEM = SYSTEM
    shared.K1 = K1
    shared.K2 = K2


def run_provider_free_gate(root: Path, config: Mapping[str, Any]) -> dict[str, Any]:
    original = v1.CONFIG
    try:
        v1.CONFIG = CONFIG
        return v1.run_provider_free_gate(root, config)
    finally:
        v1.CONFIG = original


def posttest_schema(stage: str) -> dict[str, Any]:
    if stage != "EQS":
        return v1.posttest_schema(stage)
    nullable_number = {"type": ["number", "null"]}
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "effective_pka": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "identifiable": {"type": "boolean"},
                    "estimate": nullable_number,
                    "lower80": nullable_number,
                    "upper80": nullable_number,
                    "rationale": {"type": "string"},
                },
                "required": ["identifiable", "estimate", "lower80", "upper80", "rationale"],
            },
            "path_dependence": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "assessment": {"enum": ["final_state_dominant", "path_dependent", "indeterminate"]},
                    "rationale": {"type": "string"},
                },
                "required": ["assessment", "rationale"],
            },
            "dissociation_precipitation": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "assessment": {"enum": ["continuous", "threshold_like", "mixed", "indeterminate"]},
                    "supported_range": {"type": "string"},
                    "competing_explanation": {"type": "string"},
                },
                "required": ["assessment", "supported_range", "competing_explanation"],
            },
        },
        "required": ["effective_pka", "path_dependence", "dissociation_precipitation"],
    }


def _english(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and not v1._contains_cjk(value)


def validate_posttest(
    stage: str, payload: Any, query_rows: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    if stage != "EQS":
        return v1.validate_posttest(stage, payload, query_rows)
    if not isinstance(payload, Mapping):
        return {"valid": False, "failure": "missing_payload"}
    try:
        pka = payload["effective_pka"]
        identifiable = pka["identifiable"]
        if not isinstance(identifiable, bool) or not _english(pka["rationale"]):
            raise ValueError("invalid_effective_pka_fields")
        values = [pka[key] for key in ("estimate", "lower80", "upper80")]
        if identifiable:
            numeric = [float(value) for value in values]
            if not all(math.isfinite(value) for value in numeric):
                raise ValueError("non_finite_effective_pka")
            if not numeric[1] <= numeric[0] <= numeric[2]:
                raise ValueError("invalid_effective_pka_interval")
        elif values != [None, None, None]:
            raise ValueError("abstention_requires_null_pka_values")
        path = payload["path_dependence"]
        if path["assessment"] not in {"final_state_dominant", "path_dependent", "indeterminate"}:
            raise ValueError("invalid_path_dependence_assessment")
        if not _english(path["rationale"]):
            raise ValueError("path_dependence_rationale_missing_or_not_English")
        coupling = payload["dissociation_precipitation"]
        if coupling["assessment"] not in {"continuous", "threshold_like", "mixed", "indeterminate"}:
            raise ValueError("invalid_dissociation_precipitation_assessment")
        if not _english(coupling["supported_range"]) or not _english(coupling["competing_explanation"]):
            raise ValueError("coupling_text_missing_or_not_English")
    except (KeyError, TypeError, ValueError) as exc:
        return {"valid": False, "failure": str(exc)}
    return {"valid": True, "failure": None}


def run_posttest(
    agent: Any,
    folder: Path,
    private_folder: Path,
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
        "Continue your own completed research using your existing public observations. "
        "No new laboratory experiments, network, filesystem, repository, or hidden-truth access. "
        "Only public_numerics.calculate is available. Answer the current question fully; all report, "
        "rationale, supported-range, and competing-explanation text must be in English. Do not rewrite "
        "earlier sealed outputs. equilibrium_confidence is an environment diagnostic, not your uncertainty "
        "and not a task score.",
        encoding="utf-8",
    )
    messages = {"K1": K1, "K2": K2, "EQS": EQS}
    message = messages.get(stage)
    if stage == "Q":
        message = Q_PROMPT + "\n" + json.dumps(list(query_rows), ensure_ascii=False)
    if message is None:
        raise ValueError(f"unknown EQ v2 posttest stage: {stage}")
    audit = private_folder / f"{stage}-numerics.jsonl"
    command = provider_shared.build_command(
        PROVIDER, schema_path, workspace, audit=audit, thread_id=thread_id, provider_retries=0
    )
    command += [
        "-c",
        "mcp_servers.chemworld_lab.enabled=false",
        "-c",
        f"mcp_servers.chemworld_lab.command={json.dumps(sys.executable)}",
        "-c",
        f"model_instructions_file={json.dumps(instructions.as_posix())}",
    ]
    raw = shared.launch(
        command,
        message,
        workspace,
        agent.followup_environment,
        private_folder / stage,
        1200,
        True,
        audit,
        {**progress, "phase": stage},
        numerics_budget=FOLLOWUP_NUMERICS,
    )
    write(private_folder / stage / "receipt.json", raw)
    public = {
        "payload": raw.get("payload"),
        "failure": raw.get("failure") or (None if raw.get("payload") else "missing_payload"),
        "elapsed_s": raw.get("elapsed_s"),
        "method_resources": raw.get("method_resources"),
    }
    write(folder / "sealed" / f"{stage}.json", public)
    return public


def run_cell(
    root: Path,
    config: Mapping[str, Any],
    cell: Mapping[str, Any],
    progress: dict[str, Any],
    progress_lock: threading.Lock,
) -> dict[str, Any]:
    folder = root / "sources" / cell["cell_id"]
    result_path = folder / "RESULT.json"
    if result_path.exists():
        return read(result_path)
    if folder.exists():
        raise RuntimeError(f"incomplete write-once cell requires recovery: {cell['cell_id']}")
    private_folder = v1.create_cell_folders(folder)
    prior = public_prior(config, cell["world_id"], cell["arm"])
    write(
        folder / "public-input-binding.json",
        {
            "cell_id": cell["cell_id"],
            "research_brief": research_brief(),
            "initial_world_model": prior,
            "world_public_id": cell["world_id"],
            "arm": cell["arm"],
            "source_batches": 12,
            "posttest_stages": list(POSTTEST_STAGES),
        },
    )
    write(private_folder / "attempt.json", {**dict(cell), "started_epoch": time.time()})
    world = world_by_id(config, cell["world_id"])
    started = time.monotonic()
    result: dict[str, Any] = {
        "schema_version": "work-ii-eq-cell-result-2.0",
        "cell_id": cell["cell_id"],
        "world_id": cell["world_id"],
        "arm": cell["arm"],
        "goal": cell["goal"],
        "status": "failed",
        "failure": None,
        "posttests": {},
        "posttest_validation": {},
    }
    agent = EqFreeResearchAgent(
        goal=cell["goal"],
        home_root=private_folder / "home",
        output=private_folder / "source",
        workspace=private_folder / "laboratory",
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
        session_progress_callback=lambda payload: progress.update(
            {cell["cell_id"]: {"phase": "source", "provider": payload}}
        ),
    )
    cell_progress = {"stage": cell["cell_id"], "phase": "source", "operations": 0, "batches": 0}

    def callback(record: Any, trace: Any) -> None:
        del trace
        cell_progress["operations"] += 1
        if record.info.get("instrument") == "final_assay" and record.info.get("transaction_status") == "committed":
            cell_progress["batches"] += 1
        with progress_lock:
            progress[cell["cell_id"]] = dict(cell_progress)

    try:
        physics(
            agent,
            folder / "trajectory.jsonl",
            config=config,
            world=world,
            observation_seed=deterministic_seed("eq-source-v2", cell["cell_id"]),
            observation_namespace=f"work-ii-eq-v2-source-{cell['cell_id'].lower()}",
            callback=callback,
        )
    except Exception as exc:
        result["failure"] = {"type": type(exc).__name__, "message": str(exc)[:1600]}
    finally:
        agent.close()
    records = load_jsonl(folder / "trajectory.jsonl") if (folder / "trajectory.jsonl").exists() else []
    result["batches"] = shared.summaries(records)
    result["operations"] = len(records)
    result["rollbacks"] = [
        {"step": index + 1, "action": row.get("action"), "reason": row.get("rollback_reason")}
        for index, row in enumerate(records)
        if row.get("transaction_status") != "committed"
    ]
    result["exact_replay"] = (
        verify_records(records, tolerance=0, world_interventions=copy.deepcopy(world["world_interventions"])).to_dict()
        if records
        else {"verified": False}
    )
    receipts = agent.provider_receipts()
    write(private_folder / "source-receipts.json", receipts)
    result["source_usage"] = agent.method_resource_usage()
    last = receipts[-1] if receipts else {}
    thread_id = last.get("thread_id")
    result["thread_id_sha256"] = hashlib.sha256(str(thread_id).encode()).hexdigest() if thread_id else None
    result["evidentiary_anchor"] = last.get("final_recommendation")
    result["source_status"] = (
        "completed"
        if len(result["batches"]) == 12 and result["exact_replay"].get("verified") is True
        else "partial"
        if result["batches"]
        else "failed"
    )
    query_rows = queries(config)
    if thread_id and result["source_status"] == "completed":
        for stage in POSTTEST_STAGES:
            cell_progress["phase"] = stage
            turn = run_posttest(agent, folder, private_folder, stage, str(thread_id), cell_progress, query_rows)
            result["posttests"][stage] = turn
            result["posttest_validation"][stage] = validate_posttest(stage, turn.get("payload"), query_rows)
            if not result["posttest_validation"][stage]["valid"]:
                break
    result["posttest_chain_sealed"] = all(
        result["posttest_validation"].get(stage, {}).get("valid") is True for stage in POSTTEST_STAGES
    )
    result["status"] = (
        "completed"
        if result["source_status"] == "completed" and result["posttest_chain_sealed"] and not result["failure"]
        else "retained_nonconforming"
    )
    result["elapsed_s"] = time.monotonic() - started
    write(result_path, result)
    return result


def write_summary(root: Path, schedule: Sequence[Mapping[str, Any]], phase: str) -> dict[str, Any]:
    results = []
    for cell in schedule:
        path = root / "sources" / cell["cell_id"] / "RESULT.json"
        if path.exists():
            results.append(read(path))
    payload = {
        "schema_version": "work-ii-eq-matrix-summary-2.0",
        "phase": phase,
        "planned_sources": 15,
        "planned_source_batches": 180,
        "planned_posttests": 60,
        "attempted_sources": len(results),
        "completed_sources": sum(row.get("status") == "completed" for row in results),
        "completed_source_batches": sum(len(row.get("batches", [])) for row in results),
        "sealed_posttests": sum(len(row.get("posttests", {})) for row in results),
        "sealed_posttest_chains": sum(row.get("posttest_chain_sealed") is True for row in results),
        "failures": [
            {"cell_id": row["cell_id"], "status": row.get("status"), "source_status": row.get("source_status"), "failure": row.get("failure")}
            for row in results
            if row.get("status") != "completed"
        ],
        "cells": [
            {
                "cell_id": row["cell_id"],
                "world_id": row["world_id"],
                "arm": row["arm"],
                "status": row.get("status"),
                "source_batches": len(row.get("batches", [])),
                "posttests": {stage: row.get("posttest_validation", {}).get(stage, {}).get("valid") for stage in POSTTEST_STAGES},
                "posttest_chain_sealed": row.get("posttest_chain_sealed"),
            }
            for row in results
        ],
    }
    write(root / "summary.json", payload)
    return payload


def validate_freeze(root: Path, config: Mapping[str, Any]) -> Mapping[str, Any]:
    if not FREEZE.exists():
        raise RuntimeError("provider remains sealed: EQ v2 freeze manifest is absent")
    freeze = read(FREEZE)
    gate_path = root / "provider-free-gate" / "gate.json"
    if not gate_path.exists() or read(gate_path).get("passed") is not True:
        raise RuntimeError("provider remains sealed: EQ v2 provider-free gate is absent or failed")
    if freeze.get("config_sha256") != file_sha256(CONFIG):
        raise RuntimeError("EQ v2 freeze does not bind the current config")
    if read(gate_path).get("config_sha256") != file_sha256(CONFIG):
        raise RuntimeError("EQ v2 gate does not bind the current config")
    if freeze.get("gate_sha256") != file_sha256(gate_path):
        raise RuntimeError("EQ v2 freeze does not bind this gate")
    if freeze.get("resolved_config_sha256") != digest(config):
        raise RuntimeError("EQ v2 freeze does not bind the resolved config")
    bindings = freeze.get("bindings")
    if not isinstance(bindings, Mapping) or not bindings:
        raise RuntimeError("EQ v2 freeze has no immutable bindings")
    repository = ROOT.resolve()
    for relative, expected in bindings.items():
        path = (ROOT / str(relative)).resolve()
        if repository not in path.parents or not path.is_file() or file_sha256(path) != expected:
            raise RuntimeError(f"EQ v2 freeze binding changed or is missing: {relative}")
    if freeze.get("provider_calls_before_freeze") != 0:
        raise RuntimeError("EQ v2 freeze must precede every provider call")
    if freeze.get("status") != "frozen_for_formal_development_execution":
        raise RuntimeError("EQ v2 freeze status is not executable")
    return freeze


def write_design(root: Path, config: Mapping[str, Any], validated: Mapping[str, Any], freeze: Mapping[str, Any]) -> None:
    design = {
        "schema_version": "work-ii-eq-run-design-2.0",
        "config": copy.deepcopy(config),
        "config_sha256": file_sha256(CONFIG),
        "freeze": copy.deepcopy(freeze),
        "schedule": copy.deepcopy(validated["schedule"]),
        "query_sha256": validated["query_sha256"],
        "prior_sha256": copy.deepcopy(validated["prior_sha256"]),
        "provider": copy.deepcopy(PROVIDER),
        "system_prompt": SYSTEM,
        "K1": K1,
        "Q": Q_PROMPT,
        "K2": K2,
        "EQS": EQS,
        "truth_embargo": config["truth_embargo"],
    }
    path = root / "design.json"
    if path.exists() and read(path) != design:
        raise RuntimeError("existing EQ v2 run design differs from the frozen design")
    write(path, design)


def execute_sources(
    root: Path, config: Mapping[str, Any], schedule: Sequence[Mapping[str, Any]], *, workers: int
) -> list[dict[str, Any]]:
    if not 1 <= workers <= 8:
        raise ValueError("workers must be in 1..8")
    progress: dict[str, Any] = {}
    progress_lock = threading.Lock()
    stop = threading.Event()
    started = time.monotonic()

    def heartbeat() -> None:
        while not stop.wait(30):
            with progress_lock:
                snapshot = copy.deepcopy(progress)
            completed = sum((root / "sources" / cell["cell_id"] / "RESULT.json").exists() for cell in schedule)
            elapsed = time.monotonic() - started
            print(json.dumps({"stage": "provider_sources", "completed": completed, "total": len(schedule), "workers": workers, "elapsed_s": round(elapsed), "eta_s": round(elapsed / completed * (len(schedule) - completed)) if completed else None, "active": snapshot}, default=str), flush=True)

    heartbeat_thread = threading.Thread(target=heartbeat, daemon=True)
    heartbeat_thread.start()
    results = []
    try:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(run_cell, root, config, cell, progress, progress_lock): cell for cell in schedule}
            for future in as_completed(futures):
                cell = futures[future]
                result = future.result()
                results.append(result)
                summary = write_summary(root, validate_design(config)["schedule"], "provider_sources")
                print(json.dumps({"stage": "cell_complete", "cell_id": cell["cell_id"], "status": result["status"], "completed_sources": summary["completed_sources"], "attempted_sources": summary["attempted_sources"]}), flush=True)
    finally:
        stop.set()
        heartbeat_thread.join(timeout=2)
    return results


def generate_truth(root: Path, config: Mapping[str, Any]) -> dict[str, Any]:
    return v1.generate_truth(root, config)


def evaluate_eqs(payload: Any, effective_pka: float) -> dict[str, Any]:
    validation = validate_posttest("EQS", payload, ())
    if not validation["valid"]:
        return validation
    pka = payload["effective_pka"]
    diagnostic = {
        "valid": True,
        "identifiable": pka["identifiable"],
        "absolute_error": None,
        "covered80": None,
        "width80": None,
        "aligned_prior_is_treatment_not_discovery_credit": True,
        "path_dependence": payload["path_dependence"]["assessment"],
        "dissociation_precipitation": payload["dissociation_precipitation"]["assessment"],
        "structural_labels_scored": False,
    }
    if pka["identifiable"]:
        diagnostic.update(
            {
                "absolute_error": abs(float(pka["estimate"]) - effective_pka),
                "covered80": float(pka["lower80"]) <= effective_pka <= float(pka["upper80"]),
                "width80": float(pka["upper80"]) - float(pka["lower80"]),
            }
        )
    return diagnostic


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--scope", choices=("gate", "canary", "remaining", "full"), required=True)
    parser.add_argument("--workers", type=int, default=1)
    args = parser.parse_args()
    config = load_config()
    validated = validate_design(config)
    configure_provider_helpers(config)
    root = args.output.resolve()
    root.mkdir(parents=True, exist_ok=True)
    if args.scope == "gate":
        report = run_provider_free_gate(root, config)
        print(json.dumps({"stage": "provider_free_gate_complete", "passed": report["passed"], "completed_batches": report["completed_batches"], "provider_calls": 0}), flush=True)
        if not report["passed"]:
            raise SystemExit(2)
        return
    freeze = validate_freeze(root, config)
    write_design(root, config, validated, freeze)
    schedule = validated["schedule"]
    canary = [cell for cell in schedule if cell["world_id"] == "EQ-W01"]
    if args.scope == "canary":
        if args.workers > 3:
            raise ValueError("EQ v2 canary has only three cells; workers must be <= 3")
        selected = canary
    elif args.scope == "remaining":
        canary_results = [root / "sources" / cell["cell_id"] / "RESULT.json" for cell in canary]
        if not all(path.is_file() and read(path).get("status") == "completed" for path in canary_results):
            raise RuntimeError("EQ v2 remaining matrix is sealed until all three W01 canary chains complete")
        selected = [cell for cell in schedule if cell["world_id"] != "EQ-W01"]
    else:
        if any((root / "sources" / cell["cell_id"]).exists() for cell in schedule):
            raise RuntimeError("use canary then remaining for a started EQ v2 namespace")
        raise RuntimeError("EQ v2 full launch is intentionally sealed; run canary before remaining")
    execute_sources(root, config, selected, workers=args.workers)
    summary = write_summary(root, schedule, "canary_complete" if args.scope == "canary" else "sources_complete")
    if args.scope == "canary":
        if summary["completed_sources"] < 3:
            raise RuntimeError("EQ v2 canary did not complete all three W01 K1/Q/K2/EQS chains")
        return
    results = [read(root / "sources" / cell["cell_id"] / "RESULT.json") for cell in schedule if (root / "sources" / cell["cell_id"] / "RESULT.json").exists()]
    if len(results) != 15 or not all(row.get("posttest_chain_sealed") is True for row in results):
        write_summary(root, schedule, "truth_embargoed_incomplete_EQS_chain")
        raise RuntimeError("not all 15 EQS responses are sealed; reference truth remains embargoed")
    truth = generate_truth(root, config)
    for result in results:
        evaluation = evaluate_predictions(
            result["posttests"]["Q"].get("payload"),
            queries(config),
            truth[result["world_id"]],
        )
        evaluation["eqs"] = evaluate_eqs(
            result["posttests"]["EQS"].get("payload"),
            float(world_by_id(config, result["world_id"])["private_authoring"]["effective_pka"]),
        )
        write(root / "evaluations" / f"{result['cell_id']}.json", evaluation)
    summary = write_summary(root, schedule, "complete")
    completion = {
        "schema_version": "work-ii-eq-completion-2.0",
        "completed_epoch": time.time(),
        "source_sessions": 15,
        "source_batches": sum(len(row.get("batches", [])) for row in results),
        "posttests": sum(len(row.get("posttests", {})) for row in results),
        "reference_executions": 300,
        "equilibrium_confidence_used_as_agent_uncertainty_or_score": False,
        "summary_sha256": digest(summary),
    }
    write(root / "completion.json", completion)


if __name__ == "__main__":
    main()
