"""RX-W01/P/Opaque dual-goal development canary with same-thread K1/Q/K2."""
# ruff: noqa: RUF001

from __future__ import annotations

import argparse
import copy
import json
import shutil
import tempfile
import threading
import time
from dataclasses import replace
from pathlib import Path

import scripts.run_work_ii_ec_dual_goal_trial as shared

from chemworld.campaign_resources import CampaignResourceCard
from chemworld.data.logging import load_jsonl
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[1]
_SHARED_BUILD_COMMAND = shared.build_command
TASK = "reaction-safety-constrained"
WORLD = "RX-W01"
LOCUS = "P"
ARM = "Opaque"
PACKAGE = ROOT / "configs/benchmark/work_ii_reaction_safety_matched_prior_package.json"
PROVIDER = {
    "id": "chemworld_openai_https",
    "name": "OpenAI",
    "model": "gpt-5.6-sol",
    "reasoning_effort": "medium",
    "auth_mode": "chatgpt_subscription_cached_login",
    "wire_api": "responses",
}
METRICS = [
    "yield",
    "conversion",
    "selectivity",
    "byproduct_signal",
    "safety_risk",
    "score",
]
GOALS = {
    "discovery": (
        "Your primary goal is to discover and test an explanatory, predictive account of this "
        "reaction and thermal system. Choose all experiments autonomously. Investigate target "
        "formation, competing conversion, catalyst effects or deactivation, actual thermal/time "
        "history, and termination or quench timing. You may propose, revise, combine, or reject "
        "mechanisms and equations freely. The public safe score is a secondary observation, not "
        "the research objective."
    ),
    "optimization": (
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
operating recommendation, with a short rationale. For the discovery task this recommendation is
only a secondary readout. Then return the required status/summary JSON. Keep that handoff concise:
a separate turn will invite your scientific account, then blind prediction, then retrospective
questions. Do not answer those early. Public scores and diagnostics are observations; supplied
prior information may be incomplete or inaccurate, and observations are authoritative. No
particular scientific result is required.
"""
K1 = """实验阶段已结束，操作建议已经封存。请用中文提交一份独立可读的机理报告。
说明你认为目标生成、竞争转化、催化剂作用或失活、实际热历史、时间和终止/淬灭时机
如何共同决定结果；引用真实批次编号和数值，说明哪些实验形成或改变了判断。区分实际
观测、外推和猜测，并说明适用范围、尚不能识别的因素和合理竞争解释。可自由使用自然
语言、方程或伪代码，不要求预设模型形式或唯一答案；不补做实验，不编造未测信息，
也不必重复完整实验表。返回 JSON 的 report 字段。此报告封存后才展示预测题。
"""
K2 = """机理报告和盲预测已经封存，尚未向你反馈任何预测真值。请用中文集中回答三点：
1. 哪条最重要的初始资料主张或自建规律仍未直接验证、可能错误或仅在局部成立？引用证据。
2. 若只多给一次合法完整实验，你会怎样区分最关键的竞争解释？
说明测什么及不同结果如何改变判断；不执行。
3. 哪些已取得证据没有被利用，哪些预测最不可靠，或与K1中的不确定性/适用边界不一致？
引用K1和真实批号，避免重述全文；允许承认不足，勿把事后解释写成当时已有判断。
返回 JSON 的 report 字段。
"""


def resource_card(batches: int = 12) -> CampaignResourceCard:
    return CampaignResourceCard(
        card_id=f"rx-p-opaque-dual-goal-{batches}",
        operation_attempt_limit=30 * batches,
        vessel_start_limit=batches,
        final_assay_limit=batches,
        nonfinal_instrument_use_limit=batches,
        stock_limits={
            "reagent_mol": 0.04 * batches,
            "solvent_L": 0.08 * batches,
            "catalyst_mol": 0.005 * batches,
        },
        process_time_limit_s=12000 * batches,
        implicit_operation_time_s={"quench": 120.0},
    )


def package_world() -> dict:
    data = shared.read(PACKAGE)
    if data.get("task_id") != TASK or data.get("qualification_passed") is not True:
        raise RuntimeError("RX P prior package is not qualified for the selected physical task")
    world = next((row for row in data["worlds"] if row["world_seed"] == 0), None)
    if world is None or world.get("qualification_passed") is not True:
        raise RuntimeError("RX-W01 P prior is unavailable or unqualified")
    return world


def priors(locus: str, arm: str) -> tuple[dict, dict | None]:
    if locus != LOCUS or arm not in {"Opaque", "Aligned", "MisIndexed"}:
        raise ValueError(f"unsupported RX canary cell: {locus}/{arm}")
    key = {
        "Opaque": "opaque",
        "Aligned": "aligned_nominal",
        "MisIndexed": "misindexed_nominal",
    }[arm]
    record = copy.deepcopy(package_world()["prior_arms"][key])
    return record["material_information"], record["initial_world_model"]


def recipe(feature_values: dict) -> list[dict]:
    return [
        {
            "operation": "add_solvent",
            "solvent": int(feature_values["solvent"]),
            "volume_L": float(feature_values["solvent_volume_L"]),
        },
        {"operation": "add_reagent", "amount_mol": float(feature_values["reagent_amount_mol"])},
        {
            "operation": "add_catalyst",
            "catalyst": int(feature_values["catalyst"]),
            "catalyst_amount_mol": float(feature_values["catalyst_amount_mol"]),
        },
        {
            "operation": "heat",
            "target_temperature_K": float(feature_values["reaction_temperature_K"]),
            "duration_s": float(feature_values["reaction_duration_s"]),
            "stirring_speed_rpm": float(feature_values["stirring_speed_rpm"]),
        },
        {"operation": "quench"},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


def queries() -> list[dict]:
    frozen = package_world()["held_out_queries"][:12]
    rows = [
        {"query_id": str(row["query_id"]), "actions": recipe(row["feature_values"])}
        for row in frozen
    ]
    if len(rows) != 12 or len({row["query_id"] for row in rows}) != 12:
        raise RuntimeError("RX blind query selection must contain twelve unique conditions")
    return rows


def enable_code_mode_tool_router(command: list[str]) -> list[str]:
    """Adapt the frozen EC command to the current Codex MCP tool router."""

    enabled = {"code_mode", "code_mode_host"}
    adapted: list[str] = []
    index = 0
    while index < len(command):
        if (
            command[index] == "--disable"
            and index + 1 < len(command)
            and command[index + 1] in enabled
        ):
            index += 2
            continue
        adapted.append(command[index])
        index += 1
    for feature in sorted(enabled):
        if not any(
            adapted[position : position + 2] == ["--enable", feature]
            for position in range(len(adapted) - 1)
        ):
            adapted.extend(["--enable", feature])
    return adapted


def build_command(provider, schema_path, workspace, **kwargs) -> list[str]:
    command = enable_code_mode_tool_router(
        _SHARED_BUILD_COMMAND(provider, schema_path, workspace, **kwargs)
    )
    prefix = "mcp_servers.public_numerics.args="
    for index, argument in enumerate(command):
        if not argument.startswith(prefix):
            continue
        values = json.loads(argument.removeprefix(prefix))
        limit_index = values.index("--limit")
        values[limit_index + 1] = "128"
        command[index] = prefix + json.dumps(values)
    return command


class RxFreeResearchAgent(shared.FreeResearchAgent):
    def __init__(self, **kwargs):
        kwargs.pop("role_id", None)
        super().__init__(role_id="rx_free_research", **kwargs)

    def _command(self, *, instructions_path, schema_path):
        return enable_code_mode_tool_router(
            super()._command(
                instructions_path=instructions_path,
                schema_path=schema_path,
            )
        )


def physics(
    agent,
    output,
    *,
    batches: int = 12,
    material=None,
    observation_seed: int = 0,
    callback=None,
    source_envelope: bool = False,
):
    operation_budget = 360 if source_envelope else 30 * batches
    physical_card = (
        replace(
            resource_card(),
            card_id="rx-source-envelope-single-retest",
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
        seed=0,
        agent_seed=0,
        observation_seed=observation_seed,
        budget=operation_budget,
        budget_override=operation_budget,
        episode_mode_override="campaign" if batches > 1 else "single_experiment",
        campaign_resource_card=physical_card,
        material_information=material or {"mode": "opaque_codes"},
        observation_noise_mode="keyed",
        observation_noise_namespace="work-ii-rx-p-opaque-dual-goal-canary",
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
            if isinstance(agent, RxFreeResearchAgent)
            else None
        ),
    )


def configure_shared_helpers() -> None:
    shared.TASK = TASK
    shared.PROVIDER = PROVIDER
    shared.METRICS = METRICS
    shared.GOALS = GOALS
    shared.SYSTEM = SYSTEM
    shared.K1 = K1
    shared.K2 = K2
    shared.resource_card = resource_card
    shared.priors = priors
    shared.queries = queries
    shared.physics = physics
    shared.build_command = build_command


def run_cell(root: Path, goal: str, truth: dict, progress: dict) -> dict:
    cell_id = f"{goal}-{LOCUS}-{ARM}"
    folder = root / cell_id
    if (folder / "result.json").is_file():
        return shared.read(folder / "result.json")
    folder.mkdir(parents=True, exist_ok=False)
    shared.write(folder / "attempt.json", {"cell_id": cell_id, "started_epoch": time.time()})
    progress.update(stage=cell_id, phase="source", operations=0, batches=0)
    started = time.monotonic()
    material, prior = priors(LOCUS, ARM)
    result = {
        "cell_id": cell_id,
        "goal": goal,
        "locus": LOCUS,
        "arm": ARM,
        "status": "failed",
        "failure": None,
        "posttests": {},
    }
    with tempfile.TemporaryDirectory(prefix="chemworld-rx-sol-") as temporary:
        agent = RxFreeResearchAgent(
            goal=goal,
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
        except Exception as exc:  # retained as experiment evidence
            result["failure"] = {"type": type(exc).__name__, "message": str(exc)[:1600]}
        finally:
            agent.close()
        shutil.copytree(agent.workspace.root, folder / "workspace")
        records = (
            load_jsonl(folder / "trajectory.jsonl")
            if (folder / "trajectory.jsonl").exists()
            else []
        )
        result["batches"] = shared.summaries(records)
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
        shared.write(folder / "source-receipts.json", receipts)
        result["source_usage"] = agent.method_resource_usage()
        last = receipts[-1] if receipts else {}
        result["recommendation"] = last.get("final_recommendation")
        thread_id = last.get("thread_id")
        result["source_status"] = (
            "completed"
            if len(result["batches"]) == 12 and not result["failure"]
            else "partial"
            if result["batches"]
            else "failed"
        )
        # Predeclared behavior: a legally sealed partial source still receives identical posttests.
        if thread_id and result["batches"] and result.get("recommendation"):
            for stage in ("K1", "Q", "K2"):
                progress["phase"] = stage
                turn = shared.posttest(agent, folder, stage, thread_id, progress)
                result["posttests"][stage] = turn
                if turn.get("failure"):
                    result["failure"] = result["failure"] or {
                        "type": "posttest_failure",
                        "stage": stage,
                        "message": turn["failure"],
                    }
                    break
            result["prediction_evaluation"] = shared.evaluate_predictions(
                result["posttests"].get("Q", {}).get("payload"), truth
            )
        sessions = agent.home_root / "codex-home" / "sessions"
        if sessions.exists():
            shutil.copytree(sessions, folder / "provider-rollouts")
        recommendation = result.get("recommendation") or {}
        index = recommendation.get("selected_experiment_index")
        selected = next(
            (b for b in result["batches"] if b["lifecycle_index"] == index), None
        )
        if selected is not None:
            result["recommendation_retest"] = shared.reference_run(
                folder / "recommendation-retest",
                selected["actions"],
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
    shared.write(folder / "result.json", result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--engineering-only", action="store_true")
    args = parser.parse_args()
    configure_shared_helpers()
    root = args.output.resolve()
    root.mkdir(parents=True, exist_ok=True)
    frozen = {
        "schema_version": "work-ii-rx-p-opaque-dual-goal-canary-0.1",
        "development_only": True,
        "model": PROVIDER["model"],
        "reasoning_effort": PROVIDER["reasoning_effort"],
        "task": TASK,
        "world": WORLD,
        "locus": LOCUS,
        "arm": ARM,
        "source_sessions": 2,
        "source_batches": 24,
        "queries": queries(),
        "system": SYSTEM,
        "goals": GOALS,
        "K1": K1,
        "K2": K2,
        "measurement_budget": {"intermediate": 12, "final": 12},
        "experiment_note": (
            "workstreams/flagship_tasks/WORK_II_RX_P_OPAQUE_DUAL_GOAL_CANARY_NOTE.md"
        ),
    }
    design_path = root / "design.json"
    if design_path.exists() and shared.read(design_path) != frozen:
        raise RuntimeError("existing development block design differs")
    shared.write(design_path, frozen)
    priors(LOCUS, ARM)

    engineering = root / "engineering"
    if not (engineering / "result.json").exists():
        actions = []
        for query in queries():
            plan = copy.deepcopy(query["actions"])
            plan.insert(-2, {"operation": "measure", "instrument": "hplc"})
            actions.extend(plan)
        shared.reference_run(engineering, actions, batches=12, observation_seed=0)
    canary = shared.read(engineering / "result.json")
    if (
        canary["failure"]
        or len(canary["batches"]) != 12
        or canary["rollbacks"]
        or not canary["exact_replay"].get("verified")
    ):
        raise RuntimeError("engineering path failed; retain results and fix before provider")
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
            shared.read(directory / "result.json")
            if (directory / "result.json").exists()
            else shared.reference_run(directory, query["actions"])
        )
        if (
            record["failure"]
            or len(record["batches"]) != 1
            or record["rollbacks"]
            or not record["exact_replay"].get("verified")
        ):
            raise RuntimeError(f"blind truth failed: {query['query_id']}")
        truth[query["query_id"]] = record["batches"][0]["metrics"]
    shared.write(root / "truth.json", truth)

    progress = {"completed": 0, "total": 2, "stage": "starting", "phase": "setup"}
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
                        "eta_s": round(elapsed / done * (2 - done)) if done else None,
                    },
                    default=str,
                ),
                flush=True,
            )

    thread = threading.Thread(target=heartbeat, daemon=True)
    thread.start()
    results = []
    try:
        for goal in GOALS:
            result = run_cell(root, goal, truth, progress)
            results.append(result)
            progress["completed"] = len(results)
            summary = {
                "schema_version": "work-ii-rx-p-opaque-dual-goal-canary-summary-0.1",
                "development_only": True,
                "planned_sources": 2,
                "planned_batches": 24,
                "attempted_sources": len(results),
                "completed_sources": sum(r["status"] == "completed" for r in results),
                "results": results,
            }
            shared.write(root / "summary.json", summary)
            print(
                json.dumps(
                    {
                        "cell": result["cell_id"],
                        "status": result["status"],
                        "completed": len(results),
                        "total": 2,
                    }
                ),
                flush=True,
            )
            if result["failure"] and result["operations"] == 0:
                raise RuntimeError("shared pre-action startup failure; stop the block")
            if result["failure"] and result["failure"].get("type") == "posttest_failure":
                failed_turn = result["posttests"][result["failure"]["stage"]]
                if not failed_turn.get("thread_id"):
                    raise RuntimeError("posttest could not start a turn; stop the block")
    finally:
        stop.set()
        thread.join(timeout=2)


if __name__ == "__main__":
    main()
