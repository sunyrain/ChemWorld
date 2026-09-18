"""Development EC: autonomous twelve-batch sources, then same-thread K1/Q/K2."""
# ruff: noqa: RUF001

from __future__ import annotations

import argparse
import json
import math
import shutil
import sys
import tempfile
import threading
import time
from dataclasses import replace
from pathlib import Path

from scripts.run_work_ii_astra_single_trial import read, write
from scripts.run_work_ii_final_diagnostic import build_command, launch
from scripts.run_work_ii_study_b import _prepare_codex_home

from chemworld.agents.interactive_codex_experiment import InteractiveCodexExperimentAgent
from chemworld.campaign_resources import CampaignResourceCard
from chemworld.data.logging import load_jsonl
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_electrochemical_matched_prior_qualification import build_public_priors
from chemworld.eval.work_ii_structural_candidate_qualification import build_prior_arms
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.tasks import get_task
from chemworld.world.instruments import instrument_contracts
from chemworld.world.operations import operation_contracts

ROOT = Path(__file__).resolve().parents[1]
TASK = "electrochemical-conversion"
PROTOCOL_VERSION = "ec-free-research-development-v3"
QUERY_VERSION = "ec-polarity-context-v2"
LEGACY_QUERY_VERSION = "ec-positive-short-v1"
PROVIDER = {
    "id": "chemworld_openai_https",
    "name": "OpenAI",
    "model": "gpt-5.6-sol",
    "reasoning_effort": "medium",
    "auth_mode": "chatgpt_subscription_cached_login",
    "wire_api": "responses",
}
METRICS = [
    "selective_product_yield",
    "electrochemical_selectivity",
    "faradaic_efficiency",
    "transport_efficiency",
    "energy_efficiency",
    "score",
]
GOALS = {
    "discovery": "Your primary goal is to discover and test an explanatory, predictive account "
    "of this electrochemical system. Choose all experiments autonomously. You may propose, "
    "revise, combine or reject mechanisms and equations freely. Seek informative observations. "
    "The public optimization score is a secondary observation, not the research objective.",
    "optimization": "Your primary goal is to find an operating procedure maximizing the public "
    "balanced-efficiency-v2 score in this electrochemical system. Choose all experiments "
    "autonomously. Use measurements and any mechanistic reasoning you find helpful.",
}
SYSTEM = """You are an autonomous scientist in a simulated electrochemical laboratory.
Use only the supplied chemworld_lab tools and public_numerics calculator. No filesystem,
network, repository inspection, external knowledge retrieval, or hidden simulator access.
Read material_information first. The task's research_goal is authoritative for this campaign.
Complete 12 independent batches; repetition is allowed. You have 12 intermediate instrument
uses across the campaign plus 12 final assays. Measurements are optional up to their budget.
Use the public operation and instrument contracts and actual current legal parameter ranges.
current_mA is a nonnegative magnitude cap, not a guaranteed delivered current.
You can choose materials, conditions, segmented operation, comparisons, and measurements freely.
Later prediction will cover both potential signs, short/long electrolysis, material changes,
and current caps, at a fixed stated loading; the actual conditions are withheld until reporting.
There are no mandatory belief snapshots, expression templates, or decision-audit fields.
For every batch explicitly terminate then measure final_assay. A batch ending is not the
campaign ending: continue with the returned next_state until campaign_ended is true.
After the campaign ends, use commit_final_recommendation to select one completed batch
(1-based lifecycle index) as your operating recommendation, with a short rationale. For the
discovery task this recommendation is only a secondary readout. Then return the required
status/summary JSON. Keep that handoff concise: a separate turn will invite your full scientific
account, then blind prediction, then a retrospective interview. Do not answer those early.
Public scores and diagnostics are observations; supplied prior information may be incomplete
or inaccurate, and observations are authoritative. No particular scientific result is required.
"""
K1 = """实验阶段已结束，操作建议已经封存。现在请用中文提交完整、独立可读的机理报告。
请讲清你认为这个世界如何运行：关键变量、作用关系、耦合、可能的方程或过程；哪些实验
使你形成或修改这个解释；说明解释适用范围、尚不能识别的因素和合理的竞争解释。
使用你认为最合适的自然语言、数学或伪代码，不要求任何预设模型形式，也不要求确定答案。
引用真实批次编号与数值，区分实际观测、外推和猜测；不补做实验，不编造未测信息。
请充分展开，不必压成短摘要。返回 JSON 的 report 字段。此报告封存后才给预测题。
"""
K2 = """机理报告和盲预测已经封存，尚未反馈预测真值。请用中文回答三点，引用批号，避免重复全文：
1. 哪条资料或自建规律被支持、反驳或仍未验证？哪些实际证据改变了判断？没有先验可明确说明。
2. 若再有一次实验，如何区分主要解释与竞争解释？预期不同结果会怎样改变判断？不执行。
3. 哪些证据未使用、哪些预测或操作建议最不可靠？本场目标是否影响取证选择？允许回答无明显冲突。
勿把事后解释写成当时已记录的想法。返回 JSON 的 report 字段。
"""


def resource_card(batches=12):
    operations = 30 * batches
    return CampaignResourceCard(
        card_id=f"ec-free-research-v2-{batches}",
        operation_attempt_limit=operations,
        vessel_start_limit=batches,
        final_assay_limit=batches,
        nonfinal_instrument_use_limit=batches,
        stock_limits={"reagent_mol": 0.04 * operations, "solvent_L": 0.08 * operations},
        process_time_limit_s=None,
    )


def planned_units(cell_ids):
    """Keep the explicitly selected scope; never expand it to a factorial queue."""
    allowed = {
        f"{goal}-{locus}-{arm}": (goal, locus, arm)
        for goal in GOALS
        for locus in "EPS"
        for arm in ("Opaque", "Aligned", "MisIndexed")
    }
    if not cell_ids or len(set(cell_ids)) != len(cell_ids):
        raise ValueError("select a nonempty list of unique goal-locus-arm units")
    if any(cell not in allowed for cell in cell_ids):
        raise ValueError("unknown goal-locus-arm unit")
    return [allowed[cell] for cell in cell_ids]


def posttest_context_available(receipt):
    """A valid terminal handoff, not scientific success, permits same-thread questions."""
    return bool(
        receipt.get("thread_id")
        and receipt.get("final_payload_valid") is True
        and not receipt.get("provider_error_event_count", 0)
    )


def priors(locus, arm):
    material = {"mode": "opaque_codes"}
    prior = None
    if locus == "E":
        if arm == "Aligned":
            material = {"mode": "anonymous_nominal_properties"}
        elif arm == "MisIndexed":
            contract = read(
                ROOT / "configs/benchmark/experiment_1_ec_qualification_repair_v1.0.2.json"
            )
            permutation = contract["loci"]["entity"]["descriptor_permutation_by_world"]["EC-W01"]
            material = {
                "mode": "anonymous_misindexed_properties",
                "target_field": "electrolyte_profile",
                "descriptor_permutation": permutation,
            }
    elif locus == "P":
        data = read(
            ROOT
            / "workstreams/flagship_tasks/reports"
            / "work-ii-electrochemical-matched-prior-qualification-20260811.json"
        )
        world = next(w for w in data["worlds"] if w["world_seed"] == 0)
        arms = build_public_priors(
            world["selected_reflection"], reference_context=world["reference_context"]
        )
        prior = arms[{"Opaque": "opaque", "Aligned": "supplied_a", "MisIndexed": "supplied_b"}[arm]]
    else:
        arms = build_prior_arms("electrochemical_transport")
        prior = arms[
            {"Opaque": "opaque", "Aligned": "aligned_nominal", "MisIndexed": "misindexed_nominal"}[
                arm
            ]
        ]
        prior["reference_context"] = {
            "electrolyte_profile": 0,
            "solvent": 0,
            "reagent_amount_mol": 0.012,
            "probe_potential_V": 0.8,
            "probe_current_mA": 90,
            "probe_duration_s": 300,
            "controlled_duration_s": 1800,
        }
    return material, prior


def legacy_queries():
    # Outcomes are never used to choose these conditions. Four matched comparisons plus diversity.
    rows = [
        (0, 0, 0.75, 20, 600),
        (0, 0, 0.75, 100, 600),
        (0, 0, 1.05, 20, 1800),
        (0, 0, 1.05, 100, 1800),
        (1, 0, 0.90, 60, 1200),
        (2, 0, 0.90, 60, 1200),
        (3, 0, 0.90, 60, 1200),
        (0, 0, 0.90, 60, 1200),
        (0, 1, 0.90, 60, 1200),
        (0, 2, 0.90, 60, 1200),
        (2, 2, 1.15, 90, 2400),
        (3, 1, 0.70, 35, 900),
    ]
    return [{"query_id": f"Q{i:02d}", "actions": recipe(*row)} for i, row in enumerate(rows, 1)]


def queries(version=QUERY_VERSION):
    if version == LEGACY_QUERY_VERSION:
        return legacy_queries()
    if version != QUERY_VERSION:
        raise ValueError(f"unknown EC prediction version: {version}")
    contexts = [
        ("short", 0, 0, 100, 600),
        ("long", 0, 0, 100, 7200),
        ("electrolyte_1", 1, 0, 100, 7200),
        ("electrolyte_3", 3, 0, 100, 7200),
        ("solvent_2", 0, 2, 100, 7200),
        ("current_cap", 0, 0, 500, 7200),
    ]
    result = []
    for context, electrolyte, solvent, current, duration in contexts:
        for potential in (-0.8, 0.8):
            result.append(
                {
                    "query_id": f"Q{len(result) + 1:02d}",
                    "context": context,
                    "potential_domain": "negative" if potential < 0 else "positive",
                    "actions": recipe(electrolyte, solvent, potential, current, duration),
                }
            )
    return result


def prediction_question(query_set):
    public_queries = [{"query_id": q["query_id"], "actions": q["actions"]} for q in query_set]
    return (
        f"请基于你自己的研究，对以下{len(query_set)}个独立新批次的最终结果逐一盲预测。"
        "每批从相同初始世界独立开始。对每个指标给出点估计及80%预测区间，"
        "考虑不确定性；不能补做实验。所有指标沿公共仪器及评分合同。"
        "题目并未限定你解释机理的形式。不要修改先前报告。"
        "返回完整predictions及一段共用的简要rationale，不逐题重复操作清单。\n"
        + json.dumps(public_queries)
    )


def recipe(electrolyte=0, solvent=0, potential=0.9, current=60, duration=1200):
    return [
        {"operation": "add_solvent", "solvent": solvent, "volume_L": 0.025},
        {"operation": "add_reagent", "amount_mol": 0.012},
        {
            "operation": "set_potential",
            "potential_V": potential,
            "current_mA": current,
            "electrolyte_profile": electrolyte,
        },
        {"operation": "electrolyze", "duration_s": duration},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


class FreeResearchAgent(InteractiveCodexExperimentAgent):
    def __init__(self, *, goal, home_root, output, **kwargs):
        self.goal = goal
        self.home_root = home_root
        self.output = output
        self.followup_environment = None
        super().__init__(
            model=PROVIDER["model"],
            reasoning_effort="medium",
            model_provider=PROVIDER["id"],
            model_provider_auth_mode="none",
            session_scope="campaign",
            belief_checkpoint_contract={
                "free_research": True,
                "snapshot_stages": [],
                "checkpoint_complete_experiments": [],
            },
            **kwargs,
        )
        factory = self._process_factory

        def capture(command, prompt, cwd):
            (self.output / "source-prompt.txt").write_text(prompt, encoding="utf-8")
            process = factory(command, prompt, cwd)
            process.stdout = TeeStream(process.stdout, self.output / "source-stdout.jsonl")
            process.stderr = TeeStream(process.stderr, self.output / "source-stderr.txt")
            return process

        self._process_factory = capture

    def _prepare_provider_launch(self, *, temp_root):
        del temp_root
        self.followup_environment = _prepare_codex_home(self.home_root, PROVIDER)
        self._session_process_environment = self.followup_environment
        self._use_isolated_codex_home = True

    def _model_provider_config_overrides(self):
        return [
            "-c",
            f'model_providers.{PROVIDER["id"]}={{name="OpenAI",wire_api="responses",'
            "requires_openai_auth=true,supports_websockets=false,request_max_retries=0,stream_max_retries=0}",
        ]

    def reset(self, task_info, seed):
        super().reset(task_info, seed)
        task = get_task(TASK)
        self._task_contract.update(
            free_research_campaign=True,
            research_goal=GOALS[self.goal],
            description=GOALS[self.goal],
            instrument_contracts={
                k: instrument_contracts()[k].to_dict() for k in task.allowed_instruments
            },
            operation_contracts={
                k: operation_contracts()[k].to_dict() for k in task.allowed_operations
            },
            study_budget={
                "complete_batches": 12,
                "intermediate_measurements": 12,
                "final_assays": 12,
            },
            posttests=[
                "free mechanism report",
                "blind quantitative prediction",
                "retrospective interview",
            ],
        )
        self._task_contract_manifest = self.workspace.publish_task_contract(self._task_contract)

    def _command(self, *, instructions_path, schema_path):
        instructions_path.write_text(SYSTEM, encoding="utf-8")
        (self.output / "source-instructions.txt").write_text(SYSTEM, encoding="utf-8")
        command = super()._command(instructions_path=instructions_path, schema_path=schema_path)
        command.insert(2, "--ignore-user-config")
        for feature in (
            "shell_tool",
            "browser_use",
            "computer_use",
            "in_app_browser",
            "goals",
            "image_generation",
            "skill_search",
            "hooks",
            "code_mode",
            "code_mode_host",
        ):
            command += ["--disable", feature]
        command += [
            "-c",
            "mcp_servers.chemworld_lab.enabled_tools="
            + json.dumps(
                [
                    "material_information",
                    "status",
                    "history",
                    "inspect_artifact",
                    "step",
                    "commit_final_recommendation",
                ]
            ),
        ]
        server = self.home_root / "public_numerics.py"
        shutil.copyfile(ROOT / "src/chemworld/agents/diagnostic_numerics.py", server)
        config = {
            "command": sys.executable,
            "args": [
                str(server),
                "--audit",
                str(self.output / "source-numerics.jsonl"),
                "--limit",
                "128",
            ],
            "required": True,
            "enabled": True,
            "enabled_tools": ["calculate"],
            "default_tools_approval_mode": "approve",
            "tool_timeout_sec": 15,
        }
        for key, value in config.items():
            command += ["-c", f"mcp_servers.public_numerics.{key}={json.dumps(value)}"]
        return command


class TeeStream:
    """Retain transport diagnostics in ignored runs, while the normal monitor drains them."""

    def __init__(self, stream, path):
        self.stream = stream
        self.path = path

    def __iter__(self):
        with self.path.open("w", encoding="utf-8") as output:
            for line in self.stream:
                output.write(line)
                output.flush()
                yield line

    def __getattr__(self, name):
        return getattr(self.stream, name)

    def read(self, size=-1):
        data = self.stream.read(size)
        with self.path.open("a", encoding="utf-8") as output:
            output.write(data)
        return data


def physics(
    agent,
    output,
    *,
    batches=12,
    material=None,
    observation_seed=0,
    callback=None,
    source_envelope=False,
):
    operation_budget = 360 if source_envelope else 30 * batches
    physical_card = (
        replace(
            resource_card(),
            card_id="ec-source-envelope-single-retest",
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
        objective="balanced",
        seed=0,
        agent_seed=0,
        observation_seed=observation_seed,
        budget=operation_budget,
        budget_override=operation_budget,
        episode_mode_override="campaign" if batches > 1 else "single_experiment",
        campaign_resource_card=physical_card,
        material_information=material or {"mode": "opaque_codes"},
        electrochemical_material_family_id="nominal-prior-latent-v2",
        electrochemical_workflow_mode="autonomous_open_v1",
        scoring_contract_id="electrochemical-s0-balanced-efficiency-v2",
        observation_noise_mode="keyed",
        observation_noise_namespace="work-ii-ec-sol-twelve-batch",
        output_path=output,
        step_callback=callback,
        method_resource_limits=(
            {
                "operation_limit": 30 * batches,
                "complete_experiment_limit": batches,
                "wall_time_limit_s": 5700,
                "model_call_limit": 1,
                "input_token_limit": 8000000,
                "uncached_input_token_limit": 2000000,
                "output_token_limit": 128000,
                "training_environment_step_limit": 0,
            }
            if isinstance(agent, FreeResearchAgent)
            else None
        ),
    )


def scalar(value):
    while isinstance(value, list) and value:
        value = value[0]
    return float(value) if type(value) in (int, float) else None


def summaries(records):
    batches, actions = [], []
    active_index = None
    for index, record in enumerate(records, 1):
        lifecycle_index = int(record.get("experiment_index", len(batches))) + 1
        if lifecycle_index != active_index:
            actions = []
            active_index = lifecycle_index
        actions.append(record.get("action"))
        if (
            record.get("transaction_status") == "committed"
            and record.get("instrument") == "final_assay"
        ):
            metrics = {
                k: scalar(v)
                for k, v in record.get("observation", {}).items()
                if not k.endswith("_mask") and scalar(v) is not None
            }
            batches.append(
                {
                    "ordinal": len(batches) + 1,
                    "lifecycle_index": lifecycle_index,
                    "end_step": index,
                    "actions": actions,
                    "metrics": metrics,
                }
            )
            actions = []
    return batches


def reference_run(folder, actions, *, batches=1, observation_seed=100, source_envelope=False):
    folder.mkdir(parents=True, exist_ok=False)
    failure = None

    def progress(record, trace):
        del trace
        print(
            json.dumps(
                {"stage": folder.name, "operation": record.step, "planned_operations": len(actions)}
            ),
            flush=True,
        )

    try:
        physics(
            _FrozenTruthReplayAgent(actions),
            folder / "trajectory.jsonl",
            batches=batches,
            observation_seed=observation_seed,
            callback=progress,
            source_envelope=source_envelope,
        )
    except Exception as exc:
        failure = {"type": type(exc).__name__, "message": str(exc)[:1200]}
    records = (
        load_jsonl(folder / "trajectory.jsonl") if (folder / "trajectory.jsonl").exists() else []
    )
    replay = replay_with_progress(records, folder.name)
    result = {
        "failure": failure,
        "batches": summaries(records),
        "exact_replay": replay,
        "operation_attempts": len(records),
        "rollbacks": [
            i + 1 for i, r in enumerate(records) if r.get("transaction_status") != "committed"
        ],
    }
    write(folder / "result.json", result)
    return result


def replay_with_progress(records, label):
    if not records:
        return {"verified": False}
    stop = threading.Event()
    started = time.monotonic()

    def heartbeat():
        while not stop.wait(30):
            print(
                json.dumps(
                    {
                        "stage": label,
                        "phase": "exact_replay",
                        "input_records": len(records),
                        "elapsed_s": round(time.monotonic() - started),
                    }
                ),
                flush=True,
            )

    thread = threading.Thread(target=heartbeat, daemon=True)
    thread.start()
    try:
        return verify_records(records, tolerance=0).to_dict()
    finally:
        stop.set()
        thread.join(timeout=2)


def schema(stage):
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
        "properties": {k: {"type": "number"} for k in ("estimate", "lower80", "upper80")},
        "required": ["estimate", "lower80", "upper80"],
    }
    row = {
        "type": "object",
        "additionalProperties": False,
        "properties": {"query_id": {"type": "string"}, **dict.fromkeys(METRICS, interval)},
        "required": ["query_id", *METRICS],
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "predictions": {"type": "array", "items": row},
            "rationale": {"type": "string"},
        },
        "required": ["predictions", "rationale"],
    }


def posttest(agent, folder, stage, thread_id, progress, *, design):
    workspace = agent.home_root / "followup"
    workspace.mkdir(exist_ok=True)
    schema_path = workspace / f"{stage}-schema.json"
    write(schema_path, schema(stage))
    instructions = workspace / "instructions.md"
    instructions.write_text(
        "Continue your own completed research using your existing observations. "
        "No new laboratory experiments or external access. "
        "Only public_numerics.calculate is available. "
        "Answer the current question in full; do not rewrite earlier sealed outputs.",
        encoding="utf-8",
    )
    message = design.get(stage)
    if stage == "Q":
        message = design.get("Q") or (
            "请基于你自己的研究，对以下12个独立新批次的最终结果逐一盲预测。每批从相同初始世界独立开始。"
            "对每个指标给出点估计及80%预测区间，考虑不确定性；不能补做实验。所有指标沿公共仪器及评分合同。"
            "题目并未限定你解释机理的形式。不要修改先前报告。返回完整predictions及rationale。\n"
            + json.dumps(design["queries"])
        )
    if not message:
        raise ValueError(f"missing saved {stage} prompt")
    audit = folder / f"{stage}-numerics.jsonl"
    command = build_command(
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
    result = launch(
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
    if result.get("thread_id") != thread_id:
        result["failure"] = result.get("failure") or "posttest_thread_changed"
    write(folder / stage / "receipt.json", result)
    return result


def evaluate_predictions(payload, truth, *, query_set=None):
    rows = payload.get("predictions", []) if isinstance(payload, dict) else []
    ids = [r.get("query_id") for r in rows if isinstance(r, dict)]
    expected = [q["query_id"] for q in query_set] if query_set is not None else list(truth)
    if not expected or len(set(expected)) != len(expected) or set(expected) != set(truth):
        return {"valid": False, "failure": "reference_query_ids_mismatch"}
    if len(ids) != len(rows) or any(not isinstance(q, str) for q in ids):
        return {"valid": False, "failure": "invalid_prediction_rows"}
    if sorted(ids) != sorted(expected):
        return {"valid": False, "failure": "query_ids_missing_or_duplicated"}
    by_id = {r["query_id"]: r for r in rows}
    output = {}
    try:
        for metric in METRICS:
            errors, coverage, widths = [], [], []
            for query in expected:
                item = by_id[query][metric]
                estimate, lower, upper = (
                    float(item[k]) for k in ("estimate", "lower80", "upper80")
                )
                if (
                    not all(math.isfinite(v) for v in (estimate, lower, upper))
                    or not lower <= estimate <= upper
                ):
                    raise ValueError("invalid prediction interval")
                target = truth[query][metric]
                errors.append(abs(estimate - target))
                coverage.append(lower <= target <= upper)
                widths.append(upper - lower)
            output[metric] = {
                "n": len(expected),
                "mae": sum(errors) / len(expected),
                "coverage80": sum(coverage) / len(expected),
                "mean_width80": sum(widths) / len(expected),
            }
    except (ValueError, KeyError, TypeError) as exc:
        return {"valid": False, "failure": str(exc)}
    result = {"valid": True, "metrics": output}
    if query_set is not None:
        groups = {}
        for field in ("potential_domain", "context"):
            for label in sorted({q[field] for q in query_set if field in q}):
                subset = [q["query_id"] for q in query_set if q.get(field) == label]
                groups[f"{field}:{label}"] = evaluate_predictions(
                    {"predictions": [by_id[q] for q in subset]},
                    {q: truth[q] for q in subset},
                )["metrics"]
        result["groups"] = groups
    return result


def run_cell(root, goal, locus, arm, truth, progress):
    design = read(root / "design.json")
    cell_id = f"{goal}-{locus}-{arm}"
    folder = root / cell_id
    if (folder / "result.json").is_file():
        return read(folder / "result.json")
    folder.mkdir(parents=True, exist_ok=False)
    write(folder / "attempt.json", {"cell_id": cell_id, "started_epoch": time.time()})
    progress.update(stage=cell_id, phase="source", operations=0, batches=0)
    started = time.monotonic()
    material, prior = priors(locus, arm)
    result = {
        "cell_id": cell_id,
        "goal": goal,
        "locus": locus,
        "arm": arm,
        "status": "failed",
        "failure": None,
        "posttests": {},
    }
    with tempfile.TemporaryDirectory(prefix="chemworld-ec-sol-") as temporary:
        agent = FreeResearchAgent(
            goal=goal,
            home_root=Path(temporary),
            output=folder,
            workspace=Path(temporary) / "laboratory",
            role_id="ec_free_research",
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

        def callback(record, trace):
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
                        "stage": cell_id,
                        "operations": progress["operations"],
                        "batches": progress["batches"],
                        "action": record.action,
                    }
                ),
                flush=True,
            )

        try:
            physics(agent, folder / "trajectory.jsonl", material=material, callback=callback)
        except Exception as exc:
            result["failure"] = {"type": type(exc).__name__, "message": str(exc)[:1600]}
        finally:
            agent.close()
        shutil.copytree(agent.workspace.root, folder / "workspace")
        records = (
            load_jsonl(folder / "trajectory.jsonl")
            if (folder / "trajectory.jsonl").exists()
            else []
        )
        result["batches"] = summaries(records)
        result["operations"] = len(records)
        result["rollbacks"] = [
            {"step": i + 1, "action": r.get("action"), "reason": r.get("rollback_reason")}
            for i, r in enumerate(records)
            if r.get("transaction_status") != "committed"
        ]
        result["exact_replay"] = (
            verify_records(records, tolerance=0).to_dict() if records else {"verified": False}
        )
        receipts = agent.provider_receipts()
        write(folder / "source-receipts.json", receipts)
        result["source_usage"] = agent.method_resource_usage()
        last = receipts[-1] if receipts else {}
        result["recommendation"] = last.get("final_recommendation")
        thread_id = last.get("thread_id")
        result["source_status"] = (
            "completed" if len(result["batches"]) == 12 and not result["failure"] else "failed"
        )
        result["source_failure"] = result["failure"]
        result["posttest_status"] = "unavailable"
        if posttest_context_available(last):
            for stage in ("K1", "Q", "K2"):
                progress["phase"] = stage
                turn = posttest(agent, folder, stage, thread_id, progress, design=design)
                result["posttests"][stage] = turn
                if turn.get("failure"):
                    result["posttest_failure"] = {
                        "type": "posttest_failure",
                        "stage": stage,
                        "message": turn["failure"],
                    }
                    result["failure"] = result["failure"] or result["posttest_failure"]
                    break
            result["posttest_status"] = (
                "completed"
                if len(result["posttests"]) == 3 and not result.get("posttest_failure")
                else "failed"
            )
            result["prediction_evaluation"] = evaluate_predictions(
                result["posttests"].get("Q", {}).get("payload"),
                truth,
                query_set=design["queries"],
            )
        sessions = agent.home_root / "codex-home" / "sessions"
        if sessions.exists():
            shutil.copytree(sessions, folder / "provider-rollouts")
        recommendation = result.get("recommendation") or {}
        index = recommendation.get("selected_experiment_index")
        selected = next((b for b in result["batches"] if b["lifecycle_index"] == index), None)
        if selected is not None:
            actions = selected["actions"]
            result["recommendation_retest"] = reference_run(
                folder / "recommendation-retest",
                actions,
                observation_seed=101,
                source_envelope=True,
            )
        result["status"] = (
            "completed"
            if (
                result["source_status"] == "completed"
                and len(result["posttests"]) == 3
                and not result["failure"]
                and result["exact_replay"].get("verified") is True
                and result.get("prediction_evaluation", {}).get("valid") is True
            )
            else "failed"
        )
    result["elapsed_s"] = time.monotonic() - started
    write(folder / "result.json", result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--engineering-only", action="store_true")
    parser.add_argument(
        "--units",
        nargs="+",
        required=True,
        help="Explicit ordered cells, e.g. discovery-E-Opaque optimization-E-Opaque",
    )
    args = parser.parse_args()
    units = planned_units(args.units)
    total = len(units)
    root = args.output.resolve()
    root.mkdir(parents=True, exist_ok=True)
    # Commit the actual questions and full recipe table before any physical/provider execution.
    frozen = {
        "protocol_version": PROTOCOL_VERSION,
        "units": args.units,
        "resource_card": resource_card().to_dict(),
        "model": PROVIDER["model"],
        "reasoning_effort": "medium",
        "world": "EC-W01",
        "source_sessions": total,
        "source_batches": 12 * total,
        "queries": queries(),
        "query_version": QUERY_VERSION,
        "Q": prediction_question(queries()),
        "system": SYSTEM,
        "goals": GOALS,
        "K1": K1,
        "K2": K2,
        "measurement_budget": {"intermediate": 12, "final": 12},
    }
    if (root / "design.json").exists() and read(root / "design.json") != frozen:
        raise RuntimeError("existing development block design differs")
    write(root / "design.json", frozen)
    for _, locus, arm in units:
        priors(locus, arm)
    engineering = root / "engineering"
    if not (engineering / "result.json").exists():
        actions = []
        for i in range(12):
            plan = recipe(i % 4, i % 3)
            plan.insert(-2, {"operation": "measure", "instrument": "uvvis"})
            actions.extend(plan)
        reference_run(engineering, actions, batches=12, observation_seed=0)
    canary = read(engineering / "result.json")
    if (
        canary["failure"]
        or len(canary["batches"]) != 12
        or canary["rollbacks"]
        or not canary["exact_replay"].get("verified")
    ):
        raise RuntimeError(
            "engineering path failed; retain results and fix platform before provider"
        )
    print(
        json.dumps({"stage": "engineering", "completed_batches": 12, "exact_replay": True}),
        flush=True,
    )
    if args.engineering_only:
        return
    truth = {}
    for query in queries():
        directory = root / "blind-truth" / query["query_id"]
        record = (
            read(directory / "result.json")
            if (directory / "result.json").exists()
            else reference_run(directory, query["actions"])
        )
        if (
            record["failure"]
            or len(record["batches"]) != 1
            or record["rollbacks"]
            or not record["exact_replay"].get("verified")
        ):
            raise RuntimeError(f"blind truth failed: {query['query_id']}")
        truth[query["query_id"]] = record["batches"][0]["metrics"]
    write(root / "truth.json", truth)
    progress = {"completed": 0, "total": total, "stage": "starting"}
    stop = threading.Event()
    started = time.monotonic()

    def heartbeat():
        while not stop.wait(30):
            elapsed = time.monotonic() - started
            done = progress["completed"]
            print(
                json.dumps(
                    {
                        **progress,
                        "elapsed_s": round(elapsed),
                        "eta_s": round(elapsed / done * (total - done)) if done else None,
                    },
                    default=str,
                ),
                flush=True,
            )

    thread = threading.Thread(target=heartbeat, daemon=True)
    thread.start()
    results = []
    try:
        for goal, locus, arm in units:
            result = run_cell(root, goal, locus, arm, truth, progress)
            results.append(result)
            progress["completed"] = len(results)
            write(
                root / "summary.json",
                {
                    "planned_sources": total,
                    "planned_batches": 12 * total,
                    "attempted_sources": len(results),
                    "completed_sources": sum(r["status"] == "completed" for r in results),
                    "results": results,
                },
            )
            print(
                json.dumps(
                    {
                        "cell": result["cell_id"],
                        "status": result["status"],
                        "completed": len(results),
                        "total": total,
                    }
                ),
                flush=True,
            )
            if result["source_failure"] and result["operations"] == 0:
                raise RuntimeError("shared pre-action startup failure; stop the block")
            if result.get("posttest_failure"):
                failed_turn = result["posttests"][result["posttest_failure"]["stage"]]
                if not failed_turn.get("thread_id"):
                    raise RuntimeError("posttest could not start a turn; stop the block")
    finally:
        stop.set()
        thread.join(timeout=2)


if __name__ == "__main__":
    main()
