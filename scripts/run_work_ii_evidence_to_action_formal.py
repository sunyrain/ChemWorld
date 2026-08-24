#!/usr/bin/env python3
"""Prepare, execute, and analyze the frozen Work II W2-51 decomposition."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
import threading
import time
from collections.abc import Mapping, Sequence
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import gymnasium as gym
import numpy as np
import run_work_ii_multi_task_open_action_pilot as task_runner
import run_work_ii_study_b as codex_harness
from run_work_ii_campaign_pilot import (
    _arm_material_information,
    _campaign_card,
    _world_interventions,
)
from work_ii_longitudinal_runtime import Progress, _run_one_cell

import chemworld  # noqa: F401
from chemworld.agents.interactive_codex_experiment import _public_task_contract
from chemworld.data.logging import load_jsonl
from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_analysis import WorkIIAnalysisError, score_prediction_error
from chemworld.eval.work_ii_evidence_to_action import (
    CONDITIONS,
    DONOR_CONDITION,
    analyze_terminal_results,
    build_design_manifest,
    build_hybrid_disjoint_oracle_grid,
    evaluate_candidate_packet,
    evaluate_law_action_agreement,
    evaluate_oracle_law_candidate_order,
    fit_oracle_law_from_disjoint_grid,
    predict_candidate_ranking_from_law,
    split_registered_query_pool_maximin,
    validate_protocol,
)
from chemworld.eval.work_ii_evidence_to_action_runtime import (
    execute_stratum,
    yoked_snapshot_output_schema,
)
from chemworld.eval.work_ii_prior_discovery import parse_work_ii_law_summary
from chemworld.eval.work_ii_truth import (
    build_evaluator_truth_plan,
    compile_evaluator_truth_query,
    execute_evaluator_truth_plan,
    validate_evaluator_truth_plan,
    validate_evaluator_truth_report,
)
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = (
    ROOT / "configs/benchmark/work_ii_evidence_to_action_causal_decomposition_v0.1.json"
)
DEFAULT_OUTPUT = ROOT / "runs/formal/w2-51-e2a-20260824"
RESULT_SCHEMA = "chemworld-work-ii-evidence-to-action-formal-stratum-0.1"
MANIFEST_SCHEMA = "chemworld-work-ii-evidence-to-action-formal-manifest-0.1"
AUTHORIZATION_SCHEMA = "chemworld-work-ii-evidence-to-action-execution-authorization-0.1"
PREPARATION_SUMMARY_SCHEMA = "chemworld-work-ii-e2a-formal-preparation-summary-0.1"

EXECUTION_SURFACE = (
    "configs/benchmark/work_ii_evidence_to_action_causal_decomposition_v0.1.json",
    "scripts/run_work_ii_evidence_to_action_formal.py",
    "scripts/run_work_ii_multi_task_open_action_pilot.py",
    "scripts/run_work_ii_campaign_pilot.py",
    "scripts/work_ii_longitudinal_runtime.py",
    "src/chemworld/eval/work_ii_evidence_to_action.py",
    "src/chemworld/eval/work_ii_evidence_to_action_runtime.py",
    "src/chemworld/eval/work_ii_truth.py",
)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


@contextmanager
def _periodic_liveness(
    progress: Progress,
    payload: Mapping[str, Any],
    *,
    interval_s: float = 30.0,
):
    """Emit bounded liveness while a provider-free truth helper is inside one unit."""

    stopped = threading.Event()
    started = time.perf_counter()

    def emit() -> None:
        counter = 0
        while not stopped.wait(interval_s):
            counter += 1
            progress.emit(
                {
                    **dict(payload),
                    "liveness_counter": counter,
                    "elapsed_s": round(time.perf_counter() - started, 1),
                }
            )

    thread = threading.Thread(target=emit, daemon=True)
    thread.start()
    try:
        yield
    finally:
        stopped.set()
        thread.join(timeout=interval_s)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _git_output(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.stdout.strip()


def _source_binding() -> dict[str, Any]:
    status = _git_output("status", "--porcelain", "--untracked-files=all")
    if status:
        raise RuntimeError("formal preparation requires one clean source commit")
    commit = _git_output("rev-parse", "HEAD")
    files = []
    for relative in EXECUTION_SURFACE:
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(f"execution-surface file is missing: {relative}")
        files.append({"path": relative, "sha256": _sha256_file(path)})
    binding = {
        "schema_version": "chemworld-work-ii-e2a-source-binding-0.1",
        "tested_commit": commit,
        "worktree_clean": True,
        "execution_surface": files,
    }
    binding["binding_sha256"] = canonical_json_sha256(binding)
    return binding


def _validate_source_binding(binding: Mapping[str, Any]) -> None:
    expected = binding.get("binding_sha256")
    actual = canonical_json_sha256(
        {key: value for key, value in binding.items() if key != "binding_sha256"}
    )
    if expected != actual:
        raise RuntimeError("formal source binding self-hash differs")
    if _git_output("rev-parse", "HEAD") != binding.get("tested_commit"):
        raise RuntimeError("current commit differs from the prepared formal source")
    for row in binding.get("execution_surface", []):
        if not isinstance(row, Mapping):
            raise RuntimeError("formal execution surface is malformed")
        path = ROOT / str(row.get("path"))
        if not path.is_file() or _sha256_file(path) != row.get("sha256"):
            raise RuntimeError(f"formal execution surface drifted: {path}")


class RecipientTurnError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        classification: str,
        receipt: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.classification = classification
        self.receipt = dict(receipt or {})
        self.provider_call_count = 1


class CodexRecipientSessionClient:
    """Multiplex fresh condition sessions while preserving the six-turn yoked thread."""

    model = "deepseek-v4-flash"

    def __init__(
        self,
        *,
        provider: Mapping[str, Any],
        stratum_id: str,
        output_root: Path,
        progress: Progress,
        query_metric_contract: Mapping[str, Sequence[str]],
        allowed_feature_ids: Sequence[str],
        allowed_metric_ids: Sequence[str],
        allowed_prior_fields: Sequence[str],
        nominal_information_available: bool,
    ) -> None:
        self.provider = deepcopy(dict(provider))
        self.model = str(provider["model"])
        self.stratum_id = stratum_id
        self.output_root = output_root
        self.progress = progress
        self.query_metric_contract = {
            str(query_id): [str(metric_id) for metric_id in metric_ids]
            for query_id, metric_ids in query_metric_contract.items()
        }
        self.allowed_feature_ids = [str(item) for item in allowed_feature_ids]
        self.allowed_metric_ids = [str(item) for item in allowed_metric_ids]
        self.allowed_prior_fields = [str(item) for item in allowed_prior_fields]
        self.nominal_information_available = bool(nominal_information_available)
        self.total_provider_call_count = 0
        self.receipts: list[dict[str, Any]] = []
        self._condition_threads: dict[str, str] = {}
        self._condition_turn_counts: dict[str, int] = {}
        self._temporary = tempfile.TemporaryDirectory(prefix="chemworld-e2a-recipient-")
        self._temp_root = Path(self._temporary.name)
        self._workspace = self._temp_root / "workspace"
        self._workspace.mkdir()
        self._environment = codex_harness._prepare_codex_home(
            self._temp_root,
            self.provider,
        )

    def close(self) -> None:
        self._temporary.cleanup()

    def __enter__(self) -> CodexRecipientSessionClient:
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    def _schema_for_snapshot(self, context: Mapping[str, Any]) -> dict[str, Any]:
        evidence_ids = [
            str(event["evidence_id"])
            for round_row in context.get("visible_yoked_evidence_rounds", [])
            if isinstance(round_row, Mapping)
            for event in round_row.get("events", [])
            if isinstance(event, Mapping) and isinstance(event.get("evidence_id"), str)
        ]
        return yoked_snapshot_output_schema(
            stage=str(context["stage"]),
            query_metric_contract=self.query_metric_contract,
            allowed_feature_ids=self.allowed_feature_ids,
            allowed_metric_ids=self.allowed_metric_ids,
            allowed_prior_fields=self.allowed_prior_fields,
            evidence_catalog=evidence_ids,
            nominal_information_available=self.nominal_information_available,
        )

    def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
        output_schema: Mapping[str, Any] | None = None,
    ) -> Any:
        context = json.loads(user_prompt)
        if not isinstance(context, Mapping):
            raise ValueError("recipient prompt context must be an object")
        condition = str(context.get("condition"))
        stage = str(context.get("stage"))
        if condition not in CONDITIONS:
            raise ValueError("recipient prompt condition is outside the frozen design")
        turn_index = self._condition_turn_counts.get(condition, 0) + 1
        if condition != "yoked_evidence" and turn_index != 1:
            raise RuntimeError("one-turn recipient condition attempted to reuse a session")
        if condition == "yoked_evidence":
            expected_stages = (
                "pre_evidence",
                "after_experiment_3",
                "after_experiment_6",
                "after_experiment_9",
                "final",
                "terminal_ranking",
            )
            if turn_index > len(expected_stages) or stage != expected_stages[turn_index - 1]:
                raise RuntimeError("yoked recipient turn order differs from the frozen contract")
        schema = (
            deepcopy(dict(output_schema))
            if isinstance(output_schema, Mapping)
            else self._schema_for_snapshot(context)
        )
        schema_path = self._temp_root / f"schema-{condition}-{turn_index}.json"
        codex_harness._atomic_json(schema_path, schema)
        initial = codex_harness._initial_command(self.provider, schema_path, self._workspace)
        sandbox_index = initial.index("--sandbox")
        initial[sandbox_index:sandbox_index] = ["--disable", "shell_tool"]
        if turn_index == 1:
            command = initial
            prompt = (
                f"{system_prompt}\n\nExecution envelope:\n"
                "- Do not use tools, files, web, apps, plugins, MCP, or external context.\n"
                "- Return only the requested schema-conforming JSON object.\n"
                f"- Keep the response within {max_tokens} output tokens.\n\nINPUT:\n"
                f"{user_prompt}"
            )
        else:
            thread_id = self._condition_threads[condition]
            command = codex_harness._resume_command(
                initial,
                thread_id=thread_id,
                schema_path=schema_path,
            )
            prompt = (
                "Continue the same blinded yoked-evidence session. Use only the cumulative "
                "public context below and return only the requested JSON object.\n\nINPUT:\n"
                f"{user_prompt}"
            )
        self.total_provider_call_count += 1
        self.progress.emit(
            {
                "stage": "e2a_recipient_turn_started",
                "stratum_id": self.stratum_id,
                "condition": condition,
                "turn": turn_index,
                "condition_stage": stage,
            }
        )

        def liveness(payload: dict[str, Any]) -> None:
            self.progress.emit(
                {
                    "stage": "e2a_recipient_turn_liveness",
                    "stratum_id": self.stratum_id,
                    "condition": condition,
                    "turn": turn_index,
                    "condition_stage": stage,
                    **payload,
                }
            )

        raw = codex_harness._launch_turn(
            command,
            prompt,
            cwd=self._workspace,
            environment=self._environment,
            timeout_s=float(self.provider["request_timeout_s"]),
            liveness=liveness,
        )
        payload = raw.get("final_payload")
        receipt = {
            **{key: deepcopy(value) for key, value in raw.items() if key != "final_payload"},
            "condition": condition,
            "condition_stage": stage,
            "turn_index": turn_index,
        }
        self.receipts.append(receipt)
        record = {"receipt": receipt, "sanitized_public_payload": payload}
        write_json_atomic(
            self.output_root / condition / f"turn-{turn_index:02d}-{stage}.json",
            record,
        )
        observed_thread = raw.get("thread_id")
        if raw.get("status") != "completed" or not isinstance(observed_thread, str):
            raise RecipientTurnError(
                "recipient provider turn did not complete with a thread identity",
                classification="provider_infrastructure",
                receipt=receipt,
            )
        if int(raw.get("tool_event_count", 0)) != 0:
            raise RecipientTurnError(
                "recipient provider turn emitted a forbidden tool event",
                classification="contamination",
                receipt=receipt,
            )
        if turn_index == 1:
            if observed_thread in self._condition_threads.values():
                raise RecipientTurnError(
                    "fresh recipient conditions reused a provider thread",
                    classification="contamination",
                    receipt=receipt,
                )
            self._condition_threads[condition] = observed_thread
        elif observed_thread != self._condition_threads[condition]:
            raise RecipientTurnError(
                "yoked recipient did not preserve its original provider thread",
                classification="provider_infrastructure",
                receipt=receipt,
            )
        if not isinstance(payload, Mapping):
            raise RecipientTurnError(
                "recipient provider turn returned no JSON object",
                classification="participant_schema",
                receipt=receipt,
            )
        self._condition_turn_counts[condition] = turn_index
        self.progress.emit(
            {
                "stage": "e2a_recipient_turn_terminal",
                "stratum_id": self.stratum_id,
                "condition": condition,
                "turn": turn_index,
                "condition_stage": stage,
                "status": "completed",
                "elapsed_s": raw.get("elapsed_s"),
            }
        )
        return SimpleNamespace(
            payload=deepcopy(dict(payload)),
            model=self.model,
            request_id=observed_thread,
            attempts=1,
            usage=deepcopy(dict(raw.get("usage", {}))),
        )

    def session_audit(
        self,
        *,
        autonomous_thread_id: str | None,
        autonomous_provider_call_count: int,
    ) -> dict[str, Any]:
        thread_ids = list(self._condition_threads.values())
        recipient_fresh = len(thread_ids) == len(set(thread_ids))
        autonomous_observed = (
            autonomous_provider_call_count == 0 or autonomous_thread_id is not None
        )
        autonomous_fresh = autonomous_thread_id is None or autonomous_thread_id not in thread_ids
        yoked_turns = [
            receipt for receipt in self.receipts if receipt.get("condition") == "yoked_evidence"
        ]
        return {
            "schema_version": "chemworld-work-ii-e2a-fresh-session-audit-0.1",
            "recipient_condition_thread_count": len(thread_ids),
            "recipient_condition_threads_unique": recipient_fresh,
            "autonomous_thread_identity_observed": autonomous_observed,
            "autonomous_thread_distinct_from_recipients": autonomous_fresh,
            "yoked_turn_count": len(yoked_turns),
            "yoked_same_thread": len({row.get("thread_id") for row in yoked_turns}) <= 1,
            "forbidden_tool_event_count": sum(
                int(row.get("tool_event_count", 0)) for row in self.receipts
            ),
            "passed": recipient_fresh
            and autonomous_observed
            and autonomous_fresh
            and len({row.get("thread_id") for row in yoked_turns}) <= 1
            and all(int(row.get("tool_event_count", 0)) == 0 for row in self.receipts),
        }


def _configure_formal_task_runner(
    protocol: Mapping[str, Any],
    *,
    binding_sha256: str,
    tested_commit: str,
) -> None:
    task_runner.RESOURCE_PROFILE = "resource_recovery_v2"
    task_runner.STUDY_ID = str(protocol["study_id"])
    task_runner.FORMAL_RESULT = True
    task_runner.FORMAL_PREFLIGHT_SHA256 = binding_sha256
    task_runner.TESTED_COMMIT = tested_commit
    task_runner.QUERY_SPLIT_STRATEGY = "registered_public_feature_maximin"


def _compile_valid_oracle_grid(
    source: Mapping[str, Any],
    proposed: Sequence[Mapping[str, Any]],
    *,
    global_count: int,
    neighborhood_count: int,
) -> list[dict[str, Any]]:
    required = {"global": global_count, "candidate_neighborhood": neighborhood_count}
    counts = dict.fromkeys(required, 0)
    retained: list[dict[str, Any]] = []
    for raw in proposed:
        component = str(raw.get("grid_component"))
        if component not in counts or counts[component] >= required[component]:
            continue
        query = deepcopy(dict(raw))
        try:
            compile_evaluator_truth_query(source, query)
        except (TypeError, ValueError):
            continue
        retained.append(query)
        counts[component] += 1
        if counts == required:
            break
    if counts != required:
        raise ValueError("formal oracle grid did not reach its registered component counts")
    return retained


def _oracle_grid_for_task(
    task_id: str,
    source: Mapping[str, Any],
    protocol: Mapping[str, Any],
    *,
    task_index: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str], list[str]]:
    checkpoint = source.get("belief_checkpoint")
    checkpoint = checkpoint if isinstance(checkpoint, Mapping) else {}
    registered = checkpoint.get("held_out_queries")
    if not isinstance(registered, list):
        raise ValueError(f"{task_id}: registered query pool is missing")
    feature_ids = [str(item) for item in checkpoint.get("allowed_feature_ids", [])]
    metric_ids = task_runner._task_metrics(source)
    candidates, _ = split_registered_query_pool_maximin(
        registered,
        allowed_feature_ids=feature_ids,
    )
    candidate_ids = [str(row["query_id"]) for row in candidates]
    contract = protocol["oracle_grid_contract"]
    global_count = int(contract["global_query_count_per_task"])
    neighborhood_count = int(contract["candidate_neighborhood_query_count_per_task"])
    oversampling = int(contract["compile_valid_oversampling_factor"])
    proposed = build_hybrid_disjoint_oracle_grid(
        registered,
        allowed_feature_ids=feature_ids,
        allowed_metric_ids=metric_ids,
        candidate_query_ids=candidate_ids,
        global_query_count=global_count * oversampling,
        neighborhood_query_count=neighborhood_count * oversampling,
        neighborhood_span_fraction=float(contract["candidate_neighborhood_span_fraction"]),
        grid_id=f"e2a-f-t{task_index}",
    )
    grid = _compile_valid_oracle_grid(
        source,
        proposed,
        global_count=global_count,
        neighborhood_count=neighborhood_count,
    )
    if len(grid) != int(contract["query_count_per_task"]):
        raise ValueError(f"{task_id}: formal oracle-grid denominator differs")
    return grid, candidates, feature_ids, metric_ids


def _public_task_contract_for_config(
    config: Mapping[str, Any],
    *,
    world_seed: int,
) -> dict[str, Any]:
    task_id = str(config["task_id"])
    env_kwargs: dict[str, Any] = {
        "world_split": str(config["world_split"]),
        "budget": int(config["method_resources"]["operation_limit"]),
        "objective": str(config["objective"]),
        "seed": world_seed,
        "observation_seed_override": world_seed,
        "task_id": task_id,
        "budget_override": int(config["method_resources"]["operation_limit"]),
        "episode_mode_override": str(config["episode_mode"]),
        "material_information": _arm_material_information(config, "opaque"),
        "campaign_resource_card": _campaign_card(config),
        "observation_noise_mode": str(config["observation_noise_mode"]),
        "observation_noise_namespace": (
            f"{config['observation_noise_namespace']}--seed{world_seed}"
        ),
    }
    for source_key, target_key in (
        ("electrochemical_material_family_id", "electrochemical_material_family_id"),
        ("crystallization_material_family_id", "crystallization_material_family_id"),
        ("electrochemical_workflow_mode", "electrochemical_workflow_mode"),
        ("scoring_contract_id", "scoring_contract_id"),
    ):
        if config.get(source_key) is not None:
            env_kwargs[target_key] = config[source_key]
    interventions = _world_interventions(config)
    if interventions:
        env_kwargs["world_interventions"] = list(interventions)
    env = gym.make(get_task(task_id).env_id, **env_kwargs)
    try:
        env.reset(seed=world_seed)
        task_info = env.unwrapped.task_info()
        method = config["method_resources"]
        task_info["method_budget_contract"] = {
            key: (list(method[key]) if key == "checkpoint_complete_experiments" else method[key])
            for key in (
                "operation_limit",
                "complete_experiment_limit",
                "checkpoint_complete_experiments",
            )
            if key in method
        }
        contract = _public_task_contract(task_info)
    finally:
        env.close()
    contract["terminal_decision_contract"] = deepcopy(dict(config["terminal_action_readout"]))
    contract["physical_experiment_authority_is_condition_specific"] = True
    return contract


def _execute_formal_oracle_truth(
    *,
    cluster_id: str,
    task_id: str,
    world_seed: int,
    campaign_config: Mapping[str, Any],
    grid: Sequence[Mapping[str, Any]],
    output_root: Path,
    binding_sha256: str,
    progress: Progress,
) -> dict[str, Any]:
    oracle_runtime = deepcopy(dict(campaign_config))
    checkpoint = deepcopy(dict(oracle_runtime["belief_checkpoint"]))
    metric_ids = [str(item) for item in checkpoint["allowed_metric_ids"]]
    checkpoint["held_out_queries"] = [
        {**deepcopy(dict(query)), "metric_ids": list(metric_ids)} for query in grid
    ]
    oracle_runtime["belief_checkpoint"] = checkpoint
    oracle_cluster_id = f"{cluster_id}--oracle-grid"
    plan = build_evaluator_truth_plan(
        {
            "world_cluster_id": oracle_cluster_id,
            "task_id": task_id,
            "world_seed": world_seed,
        },
        oracle_runtime,
        formal_result=True,
        formal_preflight_sha256=binding_sha256,
    )
    errors = validate_evaluator_truth_plan(plan)
    if errors:
        raise ValueError(f"{cluster_id}: invalid formal oracle truth plan: {'; '.join(errors)}")
    progress.emit(
        {
            "stage": "e2a_formal_oracle_truth_started",
            "cluster_id": cluster_id,
            "completed_queries": 0,
            "total_queries": len(grid),
        }
    )
    with _periodic_liveness(
        progress,
        {
            "stage": "e2a_formal_oracle_truth_liveness",
            "cluster_id": cluster_id,
            "completed_queries": 0,
            "total_queries": len(grid),
        },
    ):
        report = execute_evaluator_truth_plan(plan, oracle_runtime, output_root)
    errors = validate_evaluator_truth_report(report, plan)
    if errors or report.get("status") != "completed":
        raise ValueError(
            f"{cluster_id}: formal oracle truth failed: {'; '.join(errors) or report.get('status')}"
        )
    progress.emit(
        {
            "stage": "e2a_formal_oracle_truth_terminal",
            "cluster_id": cluster_id,
            "completed_queries": int(report["completed_truth_query_count"]),
            "total_queries": len(grid),
        }
    )
    return report


def _write_json_once_or_match(path: Path, payload: Mapping[str, Any]) -> None:
    if path.is_file():
        if _load(path) != dict(payload):
            raise RuntimeError(f"retained derived evidence differs: {path}")
        return
    write_json_atomic(path, dict(payload))


def _verify_retained_truth_report(
    path: Path,
    *,
    expected_query_count: int,
) -> tuple[dict[str, Any], int, str | None, str | None]:
    report = _load(path)
    expected_hash = canonical_json_sha256(
        {key: value for key, value in report.items() if key != "report_sha256"}
    )
    if report.get("report_sha256") != expected_hash:
        raise RuntimeError(f"retained truth report self-hash differs: {path}")
    if (
        report.get("status") != "completed"
        or report.get("formal_result") is not True
        or report.get("truth_query_count") != expected_query_count
        or report.get("completed_truth_query_count") != expected_query_count
        or report.get("failed_truth_query_count") != 0
        or report.get("evaluator_provider_call_count") != 0
        or report.get("participant_operation_denominator_impact") != 0
        or report.get("participant_feedback_emitted") is not False
    ):
        raise RuntimeError(f"retained formal truth report is incomplete or contaminated: {path}")
    receipts = report.get("receipts")
    if not isinstance(receipts, list) or len(receipts) != expected_query_count:
        raise RuntimeError(f"retained formal truth receipt denominator differs: {path}")
    exact_replay_count = sum(
        isinstance(receipt, Mapping)
        and receipt.get("status") == "completed"
        and isinstance(receipt.get("exact_replay"), Mapping)
        and receipt["exact_replay"].get("verified") is True
        for receipt in receipts
    )
    if exact_replay_count != expected_query_count:
        raise RuntimeError(f"retained formal exact replay is incomplete: {path}")

    retained_commit: str | None = None
    first_receipt = dict(receipts[0])
    trajectory = first_receipt.get("trajectory")
    if isinstance(trajectory, Mapping) and trajectory.get("path"):
        trajectory_path = path.parent / str(trajectory["path"])
        with trajectory_path.open("r", encoding="utf-8") as handle:
            first_record = json.loads(handle.readline())
        metadata = first_record.get("agent_metadata")
        if isinstance(metadata, Mapping) and metadata.get("git_commit"):
            retained_commit = str(metadata["git_commit"])
    binding_sha256 = report.get("formal_preflight_sha256")
    return (
        report,
        exact_replay_count,
        str(binding_sha256) if binding_sha256 else None,
        retained_commit,
    )


def _retained_oracle_task_bundle(
    *,
    protocol: Mapping[str, Any],
    output_root: Path,
    task_id: str,
) -> dict[str, Any]:
    task_items = list(protocol["task_runtime_sources"].items())
    task_index = next(
        index
        for index, (candidate_task_id, _path) in enumerate(task_items, start=1)
        if str(candidate_task_id) == task_id
    )
    runtime_path = Path(str(protocol["task_runtime_sources"][task_id]))
    source = _load((ROOT / runtime_path).resolve())
    grid, candidates, feature_ids, metric_ids = _oracle_grid_for_task(
        task_id,
        source,
        protocol,
        task_index=task_index,
    )
    retained_grid = _load(
        output_root / "prepared" / "tasks" / task_id / "oracle-grid.json"
    )
    if (
        retained_grid.get("query_count") != len(grid)
        or retained_grid.get("queries") != grid
        or retained_grid.get("candidate_outcomes_used") is not False
        or retained_grid.get("candidate_query_ids_excluded") is not True
    ):
        raise RuntimeError(f"retained oracle grid differs from the frozen task grid: {task_id}")
    return {
        "grid": grid,
        "candidate_feature_queries": candidates,
        "feature_ids": feature_ids,
        "metric_ids": metric_ids,
    }


def _write_rejected_preparation_report_zh(
    path: Path,
    summary: Mapping[str, Any],
) -> None:
    failure = dict(summary["failure"])
    gate_display = (
        "candidate opportunity gate"
        if failure["gate"] == "frozen_formal_candidate_opportunity_gate"
        else "oracle rank gate"
    )
    qualified_phrase = (
        "前七个"
        if summary["qualified_cluster_count"] == 7
        else f"前 {summary['qualified_cluster_count']} 个"
    )
    oracle = failure.get("oracle_qualification")
    oracle_rho = oracle.get("spearman_rank_correlation") if isinstance(oracle, Mapping) else None
    oracle_rho_text = f"{oracle_rho:.6f}" if isinstance(oracle_rho, (int, float)) else "n/a"
    top1_text = (
        str(bool(oracle.get("top1_agreement"))).lower()
        if isinstance(oracle, Mapping)
        else "n/a"
    )
    overlap_text = (
        str(oracle.get("fit_candidate_overlap_count"))
        if isinstance(oracle, Mapping)
        else "n/a"
    )
    lines = [
        "# W2-51 evidence-to-action 正式 provider-free 收口",
        "",
        "## 结论",
        "",
        f"正式 provider-free preparation 在冻结的 {gate_display} 上科学拒绝。",
        "provider cohort、operational canary 和 participant experiments 均未启动; 不得替换 world、",
        "放宽阈值或补跑以获得更有利结果。",
        "",
        "## 精确分母",
        "",
        f"- 计划 cluster: {summary['planned_cluster_count']}",
        f"- 已完成 truth/replay 的 cluster: {summary['attempted_cluster_count']}",
        f"- 完整通过: {summary['qualified_cluster_count']}",
        f"- 科学拒绝: {summary['scientifically_rejected_cluster_count']}",
        f"- 因冻结门控未启动: {summary['not_started_cluster_count']}",
        (
            "- provider-free truth 与 exact replay: "
            f"{summary['provider_free_truth_query_count']}/"
            f"{summary['provider_free_truth_query_planned_count']}"
        ),
        f"- evaluator/provider calls: {summary['provider_free_evaluator_provider_call_count']}",
        f"- participant/provider calls: {summary['participant_provider_call_count']}",
        f"- participant physical experiments: {summary['participant_physical_experiment_count']}",
        "",
        "## 触发门控",
        "",
        f"- cluster: {failure['cluster_id']}",
        f"- task: {failure['task_id']}",
        f"- world seed: {failure['world_seed']}",
        f"- gate: {failure['gate']}",
        f"- 冻结阈值: rho >= {failure['minimum_rank_correlation']:.2f}",
        f"- 实测 Spearman rho: {oracle_rho_text}",
        f"- Top-1 agreement: {top1_text}",
        f"- fit/candidate overlap: {overlap_text}",
        "",
        "## 处置",
        "",
        (
            "W2-51 以 `scientifically_rejected_before_provider` 终止。"
            f"{qualified_phrase}通过结果、失败 cluster"
        ),
        "及其余未启动分母全部保留; 该块不产生五条件 participant 因果对比。",
    ]
    content = "\n".join(lines) + "\n"
    if path.is_file():
        if path.read_text(encoding="utf-8") != content:
            raise RuntimeError(f"retained readable preparation report differs: {path}")
        return
    path.write_text(content, encoding="utf-8")


def finalize_rejected_preparation(
    *,
    protocol: Mapping[str, Any],
    output_root: Path,
    progress: Progress | None = None,
) -> dict[str, Any]:
    """Materialize a frozen scientific-gate rejection without executing new truth."""

    if (output_root / "input_manifest.json").exists():
        raise RuntimeError("a passed formal preparation cannot be finalized as rejected")
    if (output_root / "execution-authorization.json").exists() or (
        output_root / "formal"
    ).exists():
        raise RuntimeError("provider execution exists; provider-free rejection is not applicable")

    errors = validate_protocol(protocol)
    if errors:
        raise ValueError("; ".join(errors))
    design = build_design_manifest(protocol)
    task_bundles: dict[str, dict[str, Any]] = {}
    qualification_rows: list[dict[str, Any]] = []
    unstarted_clusters: list[dict[str, Any]] = []
    failure: dict[str, Any] | None = None
    truth_count = 0
    exact_replay_count = 0
    evaluator_provider_calls = 0
    binding_sha256s: set[str] = set()
    retained_commits: set[str] = set()

    candidate_count = int(protocol["candidate_contract"]["candidate_count"])
    checkpoint_count = candidate_count
    oracle_count = int(protocol["oracle_grid_contract"]["query_count_per_task"])
    minimum_rho = float(
        protocol["artifact_contract"]["minimum_oracle_candidate_rank_correlation"]
    )

    for cluster in design["clusters"]:
        cluster_id = str(cluster["cluster_id"])
        task_id = str(cluster["task_id"])
        world_seed = int(cluster["world_seed"])
        cluster_root = (
            output_root
            / "prepared"
            / "clusters"
            / task_id
            / f"seed-{world_seed}"
            / task_id
        )
        candidate_report_path = cluster_root / "candidate-truth" / "report.json"
        checkpoint_report_path = cluster_root / "checkpoint-truth" / "report.json"
        oracle_report_path = cluster_root / "oracle-grid-truth" / "report.json"

        if not candidate_report_path.is_file() and not checkpoint_report_path.is_file():
            unstarted_clusters.append(
                {
                    "cluster_id": cluster_id,
                    "task_id": task_id,
                    "world_seed": world_seed,
                    "status": "not_started_due_to_provider_free_gate_failure",
                }
            )
            continue
        if failure is not None:
            raise RuntimeError("formal truth exists after the first frozen scientific gate failure")
        if not candidate_report_path.is_file() or not checkpoint_report_path.is_file():
            raise RuntimeError(f"{cluster_id}: retained candidate/checkpoint truth is incomplete")

        candidate_report, candidate_replay, binding, commit = _verify_retained_truth_report(
            candidate_report_path,
            expected_query_count=candidate_count,
        )
        checkpoint_report, checkpoint_replay, checkpoint_binding, checkpoint_commit = (
            _verify_retained_truth_report(
                checkpoint_report_path,
                expected_query_count=checkpoint_count,
            )
        )
        for value in (binding, checkpoint_binding):
            if value:
                binding_sha256s.add(value)
        for value in (commit, checkpoint_commit):
            if value:
                retained_commits.add(value)
        truth_count += candidate_count + checkpoint_count
        exact_replay_count += candidate_replay + checkpoint_replay
        evaluator_provider_calls += int(candidate_report["evaluator_provider_call_count"])
        evaluator_provider_calls += int(checkpoint_report["evaluator_provider_call_count"])

        candidate_qualification = evaluate_candidate_packet(
            candidate_report["truth"],
            protocol["candidate_contract"],
        )
        row: dict[str, Any] = {
            "cluster_id": cluster_id,
            "task_id": task_id,
            "world_seed": world_seed,
            "candidate_qualification": candidate_qualification,
            "oracle_qualification": None,
            "provider_free_truth_query_count": candidate_count + checkpoint_count,
            "exact_replay_query_count": candidate_replay + checkpoint_replay,
        }
        if candidate_qualification["status"] != "passed":
            if oracle_report_path.exists():
                raise RuntimeError(
                    f"{cluster_id}: oracle truth exists after candidate gate failure"
                )
            failure = {
                "cluster_id": cluster_id,
                "task_id": task_id,
                "world_seed": world_seed,
                "gate": "frozen_formal_candidate_opportunity_gate",
                "candidate_qualification": candidate_qualification,
                "oracle_qualification": None,
                "minimum_rank_correlation": minimum_rho,
            }
            qualification_rows.append(row)
            continue

        if not oracle_report_path.is_file():
            raise RuntimeError(f"{cluster_id}: retained oracle truth is incomplete")
        oracle_report, oracle_replay, oracle_binding, oracle_commit = (
            _verify_retained_truth_report(
                oracle_report_path,
                expected_query_count=oracle_count,
            )
        )
        if oracle_binding:
            binding_sha256s.add(oracle_binding)
        if oracle_commit:
            retained_commits.add(oracle_commit)
        truth_count += oracle_count
        exact_replay_count += oracle_replay
        evaluator_provider_calls += int(oracle_report["evaluator_provider_call_count"])

        if task_id not in task_bundles:
            task_bundles[task_id] = _retained_oracle_task_bundle(
                protocol=protocol,
                output_root=output_root,
                task_id=task_id,
            )
        bundle = task_bundles[task_id]
        candidate_packet = _load(cluster_root / "public_candidate_packet.json")
        packet_ids = [str(item["query_id"]) for item in candidate_packet["candidates"]]
        candidate_ids = [
            str(item["query_id"]) for item in bundle["candidate_feature_queries"]
        ]
        if (
            candidate_packet.get("candidate_outcomes_included") is not False
            or packet_ids != candidate_ids
        ):
            raise RuntimeError(f"{cluster_id}: retained public candidate packet differs")

        artifact = fit_oracle_law_from_disjoint_grid(
            bundle["grid"],
            oracle_report["truth"],
            candidate_query_ids=candidate_ids,
            allowed_feature_ids=bundle["feature_ids"],
            allowed_metric_ids=bundle["metric_ids"],
            summary_id=f"oracle--{task_id}--seed{world_seed}",
        )
        oracle_qualification = evaluate_oracle_law_candidate_order(
            artifact,
            candidate_queries=bundle["candidate_feature_queries"],
            candidate_truth=candidate_report["truth"],
            allowed_feature_ids=bundle["feature_ids"],
            allowed_metric_ids=bundle["metric_ids"],
            minimum_rank_correlation=minimum_rho,
        )
        row.update(
            {
                "oracle_qualification": oracle_qualification,
                "provider_free_truth_query_count": candidate_count
                + checkpoint_count
                + oracle_count,
                "exact_replay_query_count": candidate_replay
                + checkpoint_replay
                + oracle_replay,
            }
        )
        qualification_rows.append(row)
        if oracle_qualification["status"] != "passed":
            failure = {
                "cluster_id": cluster_id,
                "task_id": task_id,
                "world_seed": world_seed,
                "gate": "frozen_formal_oracle_rank_gate",
                "candidate_qualification": candidate_qualification,
                "oracle_qualification": oracle_qualification,
                "minimum_rank_correlation": minimum_rho,
            }
            _write_json_once_or_match(
                cluster_root / "rejected-oracle-artifact.json",
                artifact,
            )
            _write_json_once_or_match(
                cluster_root / "rejected-oracle-qualification.json",
                oracle_qualification,
            )
        else:
            retained_artifact_path = cluster_root / "oracle-artifact.json"
            if not retained_artifact_path.is_file() or _load(retained_artifact_path) != artifact:
                raise RuntimeError(f"{cluster_id}: retained passed oracle artifact differs")

    if failure is None:
        raise RuntimeError("no frozen scientific preparation gate failure was found")
    if len(binding_sha256s) != 1 or len(retained_commits) != 1:
        raise RuntimeError("retained formal source binding is incomplete or inconsistent")

    planned_cluster_count = len(design["clusters"])
    attempted_cluster_count = len(qualification_rows)
    qualified_cluster_count = sum(
        row["candidate_qualification"]["status"] == "passed"
        and isinstance(row["oracle_qualification"], Mapping)
        and row["oracle_qualification"]["status"] == "passed"
        for row in qualification_rows
    )
    planned_truth_count = planned_cluster_count * (
        candidate_count + checkpoint_count + oracle_count
    )
    summary: dict[str, Any] = {
        "schema_version": PREPARATION_SUMMARY_SCHEMA,
        "status": "scientifically_rejected_before_provider",
        "terminal_decision": "do_not_execute_provider_cohort",
        "study_id": protocol["study_id"],
        "planned_cluster_count": planned_cluster_count,
        "attempted_cluster_count": attempted_cluster_count,
        "qualified_cluster_count": qualified_cluster_count,
        "scientifically_rejected_cluster_count": 1,
        "not_started_cluster_count": len(unstarted_clusters),
        "candidate_gate_pass_count": sum(
            row["candidate_qualification"]["status"] == "passed"
            for row in qualification_rows
        ),
        "oracle_gate_pass_count": sum(
            isinstance(row["oracle_qualification"], Mapping)
            and row["oracle_qualification"]["status"] == "passed"
            for row in qualification_rows
        ),
        "provider_free_truth_query_planned_count": planned_truth_count,
        "provider_free_truth_query_count": truth_count,
        "provider_free_exact_replay_count": exact_replay_count,
        "provider_free_evaluator_provider_call_count": evaluator_provider_calls,
        "provider_execution_requested_by_user": True,
        "provider_execution_started": False,
        "operational_canary_started": False,
        "participant_provider_call_count": 0,
        "participant_session_count": 0,
        "participant_physical_experiment_count": 0,
        "outcome_based_replacement_count": 0,
        "formal_world_replacement_count": 0,
        "retained_source_binding": {
            "formal_preflight_sha256": next(iter(binding_sha256s)),
            "git_commit": next(iter(retained_commits)),
        },
        "failure": failure,
        "qualification_rows": qualification_rows,
        "unstarted_clusters": unstarted_clusters,
    }
    if (
        attempted_cluster_count + len(unstarted_clusters) != planned_cluster_count
        or truth_count != exact_replay_count
        or evaluator_provider_calls != 0
    ):
        raise RuntimeError("rejected preparation accounting differs")
    summary["summary_sha256"] = canonical_json_sha256(summary)
    summary_path = output_root / "provider-free-preparation-summary.json"
    summary_already_exists = summary_path.is_file()
    _write_json_once_or_match(summary_path, summary)
    _write_rejected_preparation_report_zh(output_root / "REPORT_ZH.md", summary)
    if progress is not None and not summary_already_exists:
        progress.emit(
            {
                "stage": "e2a_formal_provider_free_preparation_rejected",
                "status": summary["status"],
                "attempted_clusters": attempted_cluster_count,
                "planned_clusters": planned_cluster_count,
                "truth_queries": truth_count,
                "exact_replay_queries": exact_replay_count,
                "provider_calls": 0,
                "failure_cluster_id": failure["cluster_id"],
                "failure_gate": failure["gate"],
            }
        )
    return summary


def prepare_formal(
    *,
    protocol: Mapping[str, Any],
    output_root: Path,
    progress: Progress,
) -> dict[str, Any]:
    errors = validate_protocol(protocol)
    if errors:
        raise ValueError("; ".join(errors))
    if (output_root / "input_manifest.json").exists():
        raise RuntimeError("formal input manifest already exists")
    binding = _source_binding()
    _configure_formal_task_runner(
        protocol,
        binding_sha256=str(binding["binding_sha256"]),
        tested_commit=str(binding["tested_commit"]),
    )
    design = build_design_manifest(protocol)
    design_cells = {str(cell["cell_id"]): dict(cell) for cell in design["cells"]}
    task_grids: dict[str, dict[str, Any]] = {}
    task_items = list(protocol["task_runtime_sources"].items())
    for task_index, (task_id, runtime_path) in enumerate(task_items, start=1):
        source = _load((ROOT / str(runtime_path)).resolve())
        grid, candidates, feature_ids, metric_ids = _oracle_grid_for_task(
            str(task_id),
            source,
            protocol,
            task_index=task_index,
        )
        task_grids[str(task_id)] = {
            "source": source,
            "source_path": str(runtime_path),
            "grid": grid,
            "candidate_feature_queries": candidates,
            "feature_ids": feature_ids,
            "metric_ids": metric_ids,
        }
        write_json_atomic(
            output_root / "prepared" / "tasks" / str(task_id) / "oracle-grid.json",
            {
                "schema_version": "chemworld-work-ii-e2a-formal-oracle-grid-0.1",
                "task_id": task_id,
                "candidate_outcomes_used": False,
                "candidate_query_ids_excluded": True,
                "query_count": len(grid),
                "queries": grid,
            },
        )

    autonomous_cells: list[dict[str, Any]] = []
    prepared_clusters: list[dict[str, Any]] = []
    qualification_rows: list[dict[str, Any]] = []
    cluster_total = len(design["clusters"])
    for cluster_index, cluster in enumerate(design["clusters"], start=1):
        cluster_id = str(cluster["cluster_id"])
        task_id = str(cluster["task_id"])
        world_seed = int(cluster["world_seed"])
        task_bundle = task_grids[task_id]
        source_path = (ROOT / str(task_bundle["source_path"])).resolve()
        task_runner.WORLD_SEED = world_seed
        task_runner.PACKET_SEED = int(cluster["candidate_packet_seed"])
        cluster_root = output_root / "prepared" / "clusters" / task_id / f"seed-{world_seed}"
        progress.emit(
            {
                "stage": "e2a_formal_cluster_preparation_started",
                "cluster_id": cluster_id,
                "completed_clusters": cluster_index - 1,
                "total_clusters": cluster_total,
            }
        )
        with _periodic_liveness(
            progress,
            {
                "stage": "e2a_formal_candidate_checkpoint_truth_liveness",
                "cluster_id": cluster_id,
                "completed_clusters": cluster_index - 1,
                "total_clusters": cluster_total,
                "completed_queries": 0,
                "total_queries": 16,
            },
        ):
            task_manifest = task_runner._prepare_task(
                task_id,
                source_path,
                cluster_root,
                progress,
                cluster_id=cluster_id,
            )
        task_root = cluster_root / task_id
        campaign_config_path = task_root / "campaign-config.json"
        campaign_config = _load(campaign_config_path)
        candidate_packet_path = task_root / "public_candidate_packet.json"
        first_cell = dict(task_manifest["cells"][0])
        candidate_truth = deepcopy(dict(first_cell["candidate_truth"]))
        candidate_qualification = evaluate_candidate_packet(
            candidate_truth,
            protocol["candidate_contract"],
        )
        if candidate_qualification["status"] != "passed":
            finalize_rejected_preparation(
                protocol=protocol,
                output_root=output_root,
                progress=progress,
            )
            raise RuntimeError(f"{cluster_id}: frozen formal candidate opportunity gate failed")
        oracle_report = _execute_formal_oracle_truth(
            cluster_id=cluster_id,
            task_id=task_id,
            world_seed=world_seed,
            campaign_config=campaign_config,
            grid=task_bundle["grid"],
            output_root=task_root / "oracle-grid-truth",
            binding_sha256=str(binding["binding_sha256"]),
            progress=progress,
        )
        candidate_ids = [str(row["query_id"]) for row in task_bundle["candidate_feature_queries"]]
        artifact = fit_oracle_law_from_disjoint_grid(
            task_bundle["grid"],
            oracle_report["truth"],
            candidate_query_ids=candidate_ids,
            allowed_feature_ids=task_bundle["feature_ids"],
            allowed_metric_ids=task_bundle["metric_ids"],
            summary_id=f"oracle--{task_id}--seed{world_seed}",
        )
        oracle_qualification = evaluate_oracle_law_candidate_order(
            artifact,
            candidate_queries=task_bundle["candidate_feature_queries"],
            candidate_truth=candidate_truth,
            allowed_feature_ids=task_bundle["feature_ids"],
            allowed_metric_ids=task_bundle["metric_ids"],
            minimum_rank_correlation=float(
                protocol["artifact_contract"]["minimum_oracle_candidate_rank_correlation"]
            ),
        )
        if oracle_qualification["status"] != "passed":
            finalize_rejected_preparation(
                protocol=protocol,
                output_root=output_root,
                progress=progress,
            )
            raise RuntimeError(f"{cluster_id}: frozen formal oracle rank gate failed")
        oracle_artifact_path = task_root / "oracle-artifact.json"
        write_json_atomic(oracle_artifact_path, artifact)
        public_contract = _public_task_contract_for_config(
            campaign_config,
            world_seed=world_seed,
        )
        public_contract_path = task_root / "public-task-contract.json"
        write_json_atomic(public_contract_path, public_contract)
        candidate_feature_path = task_root / "candidate-feature-queries.json"
        write_json_atomic(
            candidate_feature_path,
            {
                "schema_version": "chemworld-work-ii-e2a-candidate-feature-queries-0.1",
                "task_id": task_id,
                "candidate_outcomes_included": False,
                "queries": task_bundle["candidate_feature_queries"],
            },
        )
        query_metric_contract = {
            str(query["query_id"]): [str(metric) for metric in query["metric_ids"]]
            for query in first_cell["checkpoint_truth_plan"]["queries"]
        }
        checkpoint = campaign_config["belief_checkpoint"]
        base_by_arm = {str(cell["arm"]): dict(cell) for cell in task_manifest["cells"]}
        cluster_autonomous_ids: list[str] = []
        for stratum_id in cluster["stratum_ids"]:
            stratum = next(row for row in design["strata"] if row["stratum_id"] == stratum_id)
            prior_arm = str(stratum["prior_arm"])
            donor_design = design_cells[str(stratum["donor_cell_id"])]
            donor = deepcopy(base_by_arm[prior_arm])
            donor.update(
                {
                    "cell_id": donor_design["cell_id"],
                    "cluster_id": cluster_id,
                    "stratum_id": stratum_id,
                    "prior_arm": prior_arm,
                    "condition": DONOR_CONDITION,
                    "campaign_config_path": campaign_config_path.relative_to(
                        output_root
                    ).as_posix(),
                }
            )
            autonomous_cells.append(donor)
            cluster_autonomous_ids.append(str(donor["cell_id"]))
        prepared_clusters.append(
            {
                "cluster_id": cluster_id,
                "task_id": task_id,
                "world_seed": world_seed,
                "candidate_packet_path": candidate_packet_path.relative_to(output_root).as_posix(),
                "candidate_feature_queries_path": candidate_feature_path.relative_to(
                    output_root
                ).as_posix(),
                "candidate_truth": candidate_truth,
                "oracle_artifact_path": oracle_artifact_path.relative_to(output_root).as_posix(),
                "public_task_contract_path": public_contract_path.relative_to(
                    output_root
                ).as_posix(),
                "campaign_config_path": campaign_config_path.relative_to(output_root).as_posix(),
                "query_metric_contract": query_metric_contract,
                "allowed_feature_ids": [str(item) for item in checkpoint["allowed_feature_ids"]],
                "allowed_metric_ids": [str(item) for item in checkpoint["allowed_metric_ids"]],
                "allowed_prior_fields": [str(item) for item in checkpoint["allowed_prior_fields"]],
                "autonomous_cell_ids": cluster_autonomous_ids,
                "provider_free_truth_query_count": int(task_manifest["checkpoint_query_count"])
                + int(task_manifest["candidate_count"])
                + int(oracle_report["truth_query_count"]),
            }
        )
        qualification_rows.append(
            {
                "cluster_id": cluster_id,
                "task_id": task_id,
                "world_seed": world_seed,
                "candidate_qualification": candidate_qualification,
                "oracle_qualification": oracle_qualification,
                "fit_candidate_overlap_count": oracle_qualification["fit_candidate_overlap_count"],
                "public_truth_executed_action_plan_identity": "passed",
                "exact_replay_query_count": int(task_manifest["checkpoint_query_count"])
                + int(task_manifest["candidate_count"])
                + int(oracle_report["truth_query_count"]),
            }
        )
        progress.emit(
            {
                "stage": "e2a_formal_cluster_preparation_terminal",
                "cluster_id": cluster_id,
                "completed_clusters": cluster_index,
                "total_clusters": cluster_total,
                "candidate_status": candidate_qualification["status"],
                "oracle_status": oracle_qualification["status"],
                "oracle_rho": oracle_qualification["spearman_rank_correlation"],
            }
        )

    manifest = {
        "schema_version": MANIFEST_SCHEMA,
        "study_id": protocol["study_id"],
        "formal_result": True,
        "formal_denominator": True,
        "provider_execution_authorized_by_manifest": True,
        "provider_execution_authorization_source": "direct_user_request_complete_W2-51",
        "provider_resource_limits": "report_only",
        "currency_ceiling_usd": None,
        "currency_accounting_semantics": "descriptive_unpriced_provider_accounting",
        "source_binding": binding,
        "design_manifest": design,
        "prepared_clusters": prepared_clusters,
        "autonomous_cells": autonomous_cells,
        "qualification_rows": qualification_rows,
        "operational_canary_cluster_id": prepared_clusters[0]["cluster_id"],
        "scheduled_session_count": design["scheduled_session_count"],
        "autonomous_session_count": design["autonomous_session_count"],
        "participant_physical_experiment_count": design["participant_physical_experiment_count"],
        "provider_free_truth_query_count": sum(
            int(row["provider_free_truth_query_count"]) for row in prepared_clusters
        ),
        "provider_free_exact_replay_count": sum(
            int(row["exact_replay_query_count"]) for row in qualification_rows
        ),
        "all_formal_candidate_gates_passed": all(
            row["candidate_qualification"]["status"] == "passed" for row in qualification_rows
        ),
        "all_formal_oracle_gates_passed": all(
            row["oracle_qualification"]["status"] == "passed" for row in qualification_rows
        ),
    }
    if (
        len(prepared_clusters) != 15
        or len(autonomous_cells) != 45
        or manifest["scheduled_session_count"] != 225
        or manifest["participant_physical_experiment_count"] != 540
    ):
        raise AssertionError("formal evidence-to-action denominator differs")
    manifest["manifest_sha256"] = canonical_json_sha256(manifest)
    write_json_atomic(output_root / "input_manifest.json", manifest)
    write_json_atomic(
        output_root / "provider-free-preparation-summary.json",
        {
            "schema_version": "chemworld-work-ii-e2a-formal-preparation-summary-0.1",
            "status": "passed",
            "cluster_count": len(prepared_clusters),
            "candidate_gate_pass_count": sum(
                row["candidate_qualification"]["status"] == "passed" for row in qualification_rows
            ),
            "oracle_gate_pass_count": sum(
                row["oracle_qualification"]["status"] == "passed" for row in qualification_rows
            ),
            "provider_free_truth_query_count": manifest["provider_free_truth_query_count"],
            "provider_free_exact_replay_count": manifest["provider_free_exact_replay_count"],
            "provider_call_count": 0,
            "manifest_sha256": manifest["manifest_sha256"],
        },
    )
    return manifest


def _validate_manifest(manifest: Mapping[str, Any]) -> None:
    expected = manifest.get("manifest_sha256")
    actual = canonical_json_sha256(
        {key: value for key, value in manifest.items() if key != "manifest_sha256"}
    )
    if manifest.get("schema_version") != MANIFEST_SCHEMA or expected != actual:
        raise RuntimeError("formal evidence-to-action manifest is invalid")
    if (
        manifest.get("scheduled_session_count") != 225
        or manifest.get("autonomous_session_count") != 45
        or manifest.get("participant_physical_experiment_count") != 540
        or manifest.get("all_formal_candidate_gates_passed") is not True
        or manifest.get("all_formal_oracle_gates_passed") is not True
    ):
        raise RuntimeError("formal evidence-to-action manifest denominator or gates differ")
    _validate_source_binding(manifest["source_binding"])


def _authorization_record(output_root: Path, manifest: Mapping[str, Any]) -> dict[str, Any]:
    path = output_root / "execution-authorization.json"
    if path.is_file():
        record = _load(path)
        if (
            record.get("schema_version") != AUTHORIZATION_SCHEMA
            or record.get("manifest_sha256") != manifest.get("manifest_sha256")
            or record.get("provider_execution_authorized") is not True
        ):
            raise RuntimeError("retained provider authorization record differs")
        return record
    record = {
        "schema_version": AUTHORIZATION_SCHEMA,
        "study_id": manifest["study_id"],
        "manifest_sha256": manifest["manifest_sha256"],
        "authorized_at_unix_s": time.time(),
        "authorized_by": "user",
        "authorization_source": "direct request: 完成W2-51",
        "provider_execution_authorized": True,
        "provider_profile": "deepseek-v4-flash-high-codex-harness",
        "provider_resource_limits": "report_only",
        "currency_ceiling_usd": None,
        "currency_semantics": (
            "No trustworthy per-run USD schedule is bound; calls and tokens are retained "
            "descriptively under the previously qualified report-only DeepSeek contract."
        ),
        "single_executor": True,
        "scientific_failures_retained": True,
        "outcome_based_replacement_forbidden": True,
        "donor_replacement_forbidden": True,
        "missing_donor_descendant_status": "not_started_due_to_missing_donor",
        "platform_defect_requires_affected_block_restart_from_first_unit": True,
    }
    write_json_atomic(path, record)
    return record


def _cluster_lookup(manifest: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(row["cluster_id"]): dict(row) for row in manifest["prepared_clusters"]}


def _autonomous_lookup(manifest: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(row["cell_id"]): dict(row) for row in manifest["autonomous_cells"]}


def _autonomous_thread_id(result: Mapping[str, Any]) -> str | None:
    campaign = result.get("campaign_summary")
    campaign = campaign if isinstance(campaign, Mapping) else {}
    receipts = campaign.get("provider_receipts")
    receipts = receipts if isinstance(receipts, list) else []
    ids = [
        str(receipt["thread_id"])
        for receipt in receipts
        if isinstance(receipt, Mapping) and isinstance(receipt.get("thread_id"), str)
    ]
    return ids[-1] if ids else None


def _autonomous_failure_classification(raw: Mapping[str, Any]) -> str | None:
    if raw.get("status") == "completed_uncontaminated":
        return None
    campaign = raw.get("campaign_summary")
    campaign = campaign if isinstance(campaign, Mapping) else {}
    failure = campaign.get("failure")
    if isinstance(failure, Mapping):
        rendered = f"{failure.get('type')} {failure.get('message')}".lower()
        if any(token in rendered for token in ("provider", "codex", "timeout", "process")):
            return "provider_infrastructure"
        return "runner_infrastructure"
    usage = campaign.get("method_resources")
    usage = usage if isinstance(usage, Mapping) else {}
    if int(usage.get("provider_error_event_count", 0) or 0) > 0:
        return "provider_infrastructure"
    return "scientific_process"


def _autonomous_executor(
    *,
    campaign_cell: Mapping[str, Any],
    output_root: Path,
    progress: Progress,
    cell_index: int,
    total_cells: int,
) -> dict[str, Any]:
    raw = _run_one_cell(
        campaign_cell,
        output_root=output_root,
        phase="formal/autonomous",
        progress=progress,
        cell_index=cell_index,
        total_cells=total_cells,
    )
    campaign = deepcopy(dict(raw["campaign_summary"]))
    analysis = campaign.get("analysis")
    analysis = analysis if isinstance(analysis, Mapping) else {}
    physical_count = int(analysis.get("complete_experiment_count", 0) or 0)
    ranking = raw.get("participant_ranking")
    eligible = (
        raw.get("status") == "completed_uncontaminated"
        and physical_count == 12
        and isinstance(ranking, list)
        and len(ranking) == 8
        and len(set(map(str, ranking))) == 8
    )
    campaign["physical_campaign_completed"] = campaign.get("completed") is True
    campaign["completed"] = eligible
    usage = campaign.get("method_resources")
    usage = usage if isinstance(usage, Mapping) else {}
    trajectory_path = (
        output_root
        / "formal"
        / "autonomous"
        / "campaigns"
        / str(campaign_cell["cell_id"])
        / "trajectory.jsonl"
    )
    trajectory = load_jsonl(trajectory_path) if trajectory_path.is_file() else []
    payload: dict[str, Any] = {
        "cell_id": str(campaign_cell["cell_id"]),
        "condition": DONOR_CONDITION,
        "status": "completed_uncontaminated" if eligible else "failed_retained",
        "physical_experiment_count": physical_count,
        "provider_call_count": int(usage.get("provider_session_count", 0) or 0),
        "provider_process_attempt_count": int(usage.get("provider_process_attempt_count", 0) or 0),
        "provider_usage": deepcopy(dict(usage)),
        "participant_ranking": deepcopy(ranking) if isinstance(ranking, list) else None,
        "trajectory_rows": trajectory,
        "trajectory_sha256": _sha256_file(trajectory_path) if trajectory_path.is_file() else None,
        "campaign_summary": campaign,
        "raw_autonomous_result_sha256": raw.get("result_sha256"),
        "autonomous_thread_id": _autonomous_thread_id(raw),
        "failure_classification": _autonomous_failure_classification(raw),
    }
    if isinstance(ranking, list):
        payload["submission"] = {"ranking": [str(item) for item in ranking]}
    return payload


def _stratum_paths(output_root: Path, stratum_id: str) -> tuple[Path, Path, Path]:
    result = output_root / "formal" / "strata" / f"{stratum_id}.json"
    recipients = output_root / "formal" / "recipient-turns" / stratum_id
    autonomous = (
        output_root / "formal" / "autonomous" / "campaigns" / (f"{stratum_id}--{DONOR_CONDITION}")
    )
    return result, recipients, autonomous


def _load_retained_stratum(path: Path, *, stratum_id: str) -> dict[str, Any]:
    result = _load(path)
    expected = result.get("result_sha256")
    actual = canonical_json_sha256(
        {key: value for key, value in result.items() if key != "result_sha256"}
    )
    if (
        result.get("schema_version") != RESULT_SCHEMA
        or result.get("stratum_id") != stratum_id
        or expected != actual
    ):
        raise RuntimeError(f"invalid retained formal stratum result: {path}")
    return result


def execute_one_stratum(
    *,
    stratum: Mapping[str, Any],
    manifest: Mapping[str, Any],
    output_root: Path,
    progress: Progress,
    autonomous_index: int,
) -> dict[str, Any]:
    stratum_id = str(stratum["stratum_id"])
    result_path, recipient_root, autonomous_root = _stratum_paths(output_root, stratum_id)
    if result_path.is_file():
        return _load_retained_stratum(result_path, stratum_id=stratum_id)
    if recipient_root.exists() or autonomous_root.exists():
        raise RuntimeError(
            f"partial formal stratum must be held for causal inspection: {stratum_id}"
        )
    clusters = _cluster_lookup(manifest)
    autonomous_cells = _autonomous_lookup(manifest)
    cluster = clusters[str(stratum["cluster_id"])]
    design_cells = {
        str(cell["cell_id"]): dict(cell) for cell in manifest["design_manifest"]["cells"]
    }
    cells = [design_cells[str(cell_id)] for cell_id in stratum["cell_ids"]]
    donor_cell_id = str(stratum["donor_cell_id"])
    campaign_cell = autonomous_cells[donor_cell_id]
    campaign_config = _load(output_root / str(cluster["campaign_config_path"]))
    provider = campaign_config["provider"]
    candidate_packet = _load(output_root / str(cluster["candidate_packet_path"]))
    task_contract = _load(output_root / str(cluster["public_task_contract_path"]))
    oracle_artifact = _load(output_root / str(cluster["oracle_artifact_path"]))
    prior_arm = str(stratum["prior_arm"])
    initial_model = deepcopy(dict(campaign_config["prior_arms"][prior_arm]["initial_world_model"]))
    nominal = initial_model.get("availability") != "opaque_for_target_locus"
    donor_holder: dict[str, Any] = {}

    def run_donor(_: Mapping[str, Any]) -> Mapping[str, Any]:
        donor = _autonomous_executor(
            campaign_cell=campaign_cell,
            output_root=output_root,
            progress=progress,
            cell_index=autonomous_index,
            total_cells=int(manifest["autonomous_session_count"]),
        )
        donor_holder.update(donor)
        return donor

    started = time.perf_counter()
    with CodexRecipientSessionClient(
        provider=provider,
        stratum_id=stratum_id,
        output_root=recipient_root,
        progress=progress,
        query_metric_contract=cluster["query_metric_contract"],
        allowed_feature_ids=cluster["allowed_feature_ids"],
        allowed_metric_ids=cluster["allowed_metric_ids"],
        allowed_prior_fields=cluster["allowed_prior_fields"],
        nominal_information_available=nominal,
    ) as client:
        result = execute_stratum(
            client,
            cells=cells,
            autonomous_executor=run_donor,
            task_contract=task_contract,
            initial_world_model=initial_model,
            candidate_packet=candidate_packet,
            oracle_law_artifact=oracle_artifact,
            query_metric_contract=cluster["query_metric_contract"],
            allowed_feature_ids=cluster["allowed_feature_ids"],
            allowed_metric_ids=cluster["allowed_metric_ids"],
            allowed_prior_fields=cluster["allowed_prior_fields"],
            nominal_information_available=nominal,
        )
        audit = client.session_audit(
            autonomous_thread_id=(
                str(donor_holder["autonomous_thread_id"])
                if isinstance(donor_holder.get("autonomous_thread_id"), str)
                else None
            ),
            autonomous_provider_call_count=int(donor_holder.get("provider_call_count", 0) or 0),
        )
        recipient_receipts = deepcopy(client.receipts)
    formal = {
        **deepcopy(dict(result)),
        "schema_version": RESULT_SCHEMA,
        "study_id": manifest["study_id"],
        "formal_result": True,
        "cluster_id": str(stratum["cluster_id"]),
        "task_id": str(cluster["task_id"]),
        "world_seed": int(cluster["world_seed"]),
        "prior_arm": prior_arm,
        "fresh_session_audit": audit,
        "recipient_provider_receipts": recipient_receipts,
        "elapsed_s": round(time.perf_counter() - started, 3),
    }
    formal["result_sha256"] = canonical_json_sha256(formal)
    write_json_atomic(result_path, formal)
    for cell_id, cell_result in formal["cell_results"].items():
        write_json_atomic(
            output_root / "formal" / "cells" / f"{cell_id}.json",
            {
                **deepcopy(dict(cell_result)),
                "stratum_id": stratum_id,
                "cluster_id": str(stratum["cluster_id"]),
                "task_id": str(cluster["task_id"]),
                "world_seed": int(cluster["world_seed"]),
                "prior_arm": prior_arm,
                "formal_result": True,
            },
        )
    return formal


def _recipient_accounting_defects(stratum_result: Mapping[str, Any]) -> list[str]:
    defects: list[str] = []
    for receipt in stratum_result.get("recipient_provider_receipts", []):
        if not isinstance(receipt, Mapping):
            defects.append("malformed recipient receipt")
            continue
        if receipt.get("status") != "completed":
            defects.append(
                f"{receipt.get('condition')}/{receipt.get('condition_stage')}: provider turn failed"
            )
        if not isinstance(receipt.get("thread_id"), str):
            defects.append(
                f"{receipt.get('condition')}/{receipt.get('condition_stage')}: thread ID missing"
            )
        if not isinstance(receipt.get("usage"), Mapping) or not receipt.get("usage"):
            defects.append(
                f"{receipt.get('condition')}/{receipt.get('condition_stage')}: usage missing"
            )
        if int(receipt.get("tool_event_count", 0) or 0) != 0:
            defects.append(
                f"{receipt.get('condition')}/{receipt.get('condition_stage')}: tool contamination"
            )
    donor = next(
        (
            row
            for row in stratum_result.get("cell_results", {}).values()
            if isinstance(row, Mapping) and row.get("condition") == DONOR_CONDITION
        ),
        None,
    )
    if isinstance(donor, Mapping):
        usage = donor.get("provider_usage")
        usage = usage if isinstance(usage, Mapping) else {}
        if donor.get("provider_call_count", 0) and (
            usage.get("provider_call_accounting_complete") is not True
            or usage.get("provider_token_accounting_complete") is not True
            or usage.get("provider_usage_accounting_complete") is not True
        ):
            defects.append("autonomous donor provider accounting is incomplete")
    return defects


def _canary_defects(results: Sequence[Mapping[str, Any]]) -> list[str]:
    defects: list[str] = []
    if len(results) != 3:
        defects.append("canary does not contain all three prior strata")
    for result in results:
        stratum_id = str(result.get("stratum_id"))
        audit = result.get("fresh_session_audit")
        if not isinstance(audit, Mapping) or audit.get("passed") is not True:
            defects.append(f"{stratum_id}: fresh-session audit failed")
        defects.extend(
            f"{stratum_id}: {message}" for message in _recipient_accounting_defects(result)
        )
        cell_results = result.get("cell_results")
        cell_results = cell_results if isinstance(cell_results, Mapping) else {}
        for cell_id, row in cell_results.items():
            if not isinstance(row, Mapping):
                defects.append(f"{stratum_id}/{cell_id}: malformed cell result")
                continue
            if row.get("status") != "failed_retained":
                continue
            if row.get("condition") == DONOR_CONDITION:
                classification = row.get("failure_classification")
            else:
                failure = row.get("failure")
                classification = (
                    failure.get("classification") if isinstance(failure, Mapping) else None
                )
            if classification != "scientific_process":
                defects.append(
                    f"{stratum_id}/{cell_id}: retained {classification or 'unclassified'} failure"
                )
    return defects


def _load_completed_strata(
    output_root: Path,
    strata: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for stratum in strata:
        stratum_id = str(stratum["stratum_id"])
        result_path, recipient_root, autonomous_root = _stratum_paths(output_root, stratum_id)
        if result_path.is_file():
            results.append(_load_retained_stratum(result_path, stratum_id=stratum_id))
        elif recipient_root.exists() or autonomous_root.exists():
            raise RuntimeError(
                f"partial formal stratum must be held for causal inspection: {stratum_id}"
            )
    return results


def _execution_summary(
    manifest: Mapping[str, Any],
    results: Sequence[Mapping[str, Any]],
    *,
    execution_status: str,
) -> dict[str, Any]:
    cell_rows = [
        row
        for result in results
        for row in result.get("cell_results", {}).values()
        if isinstance(row, Mapping)
    ]
    donor_rows = [row for row in cell_rows if row.get("condition") == DONOR_CONDITION]
    provider_calls = sum(int(row.get("provider_call_count", 0) or 0) for row in cell_rows)
    provider_process_attempts = sum(
        int(row.get("provider_process_attempt_count", 0) or 0) for row in donor_rows
    )
    physical = sum(int(row.get("physical_experiment_count", 0) or 0) for row in cell_rows)
    usage_rows = [
        receipt.get("usage")
        for result in results
        for receipt in result.get("recipient_provider_receipts", [])
        if isinstance(receipt, Mapping) and isinstance(receipt.get("usage"), Mapping)
    ] + [
        row.get("provider_usage")
        for row in donor_rows
        if isinstance(row.get("provider_usage"), Mapping)
    ]
    summary = {
        "schema_version": "chemworld-work-ii-e2a-formal-execution-summary-0.1",
        "study_id": manifest["study_id"],
        "execution_status": execution_status,
        "formal_result": True,
        "scheduled_stratum_count": 45,
        "retained_stratum_count": len(results),
        "scheduled_session_count": 225,
        "retained_cell_record_count": len(cell_rows),
        "completed_cell_count": sum(
            row.get("status") in {"completed", "completed_uncontaminated"} for row in cell_rows
        ),
        "failed_retained_cell_count": sum(
            row.get("status") == "failed_retained" for row in cell_rows
        ),
        "donor_blocked_descendant_count": sum(
            row.get("status") == "not_started_due_to_missing_donor" for row in cell_rows
        ),
        "autonomous_donor_count": len(donor_rows),
        "eligible_autonomous_donor_count": sum(
            row.get("status") == "completed_uncontaminated" for row in donor_rows
        ),
        "participant_physical_experiment_denominator": 540,
        "participant_physical_experiment_observed": physical,
        "provider_call_count": provider_calls,
        "provider_process_attempt_count": provider_process_attempts,
        "provider_resource_limits": "report_only",
        "monetary_accounting_complete": False,
        "currency_ceiling_usd": None,
        "input_token_count": sum(
            int(row.get("input_tokens", row.get("input_token_count", 0)) or 0) for row in usage_rows
        ),
        "cached_input_token_count": sum(
            int(row.get("cached_input_tokens", row.get("cached_input_token_count", 0)) or 0)
            for row in usage_rows
        ),
        "output_token_count": sum(
            int(row.get("output_tokens", row.get("output_token_count", 0)) or 0)
            for row in usage_rows
        ),
        "provider_free_truth_query_count": manifest["provider_free_truth_query_count"],
        "provider_free_exact_replay_count": manifest["provider_free_exact_replay_count"],
        "public_truth_executed_action_plan_identity": "passed",
        "all_scheduled_failures_retained": True,
        "outcome_based_replacement_count": 0,
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    return summary


def execute_phase(
    *,
    manifest: Mapping[str, Any],
    output_root: Path,
    progress: Progress,
    canary: bool,
) -> int:
    _authorization_record(output_root, manifest)
    strata = [dict(row) for row in manifest["design_manifest"]["strata"]]
    canary_cluster = str(manifest["operational_canary_cluster_id"])
    canary_strata = [row for row in strata if row["cluster_id"] == canary_cluster]
    completed = _load_completed_strata(output_root, strata)
    completed_ids = {str(row["stratum_id"]) for row in completed}
    if canary:
        selected = [row for row in canary_strata if row["stratum_id"] not in completed_ids]
        if len(selected) != 3 or any(row["stratum_id"] in completed_ids for row in canary_strata):
            raise RuntimeError("operational canary must start as one fresh complete cluster")
    else:
        canary_results = [row for row in completed if row["cluster_id"] == canary_cluster]
        canary_summary_path = output_root / "canary-summary.json"
        if (
            len(canary_results) != 3
            or not canary_summary_path.is_file()
            or _load(canary_summary_path).get("qualified") is not True
        ):
            raise RuntimeError("remaining cohort is held until the complete cluster canary passes")
        selected = [
            row
            for row in strata
            if row["cluster_id"] != canary_cluster and row["stratum_id"] not in completed_ids
        ]
    phase = "canary" if canary else "remaining"
    progress.emit(
        {
            "stage": f"e2a_{phase}_execution_started",
            "completed_strata": 0,
            "total_strata": len(selected),
            "single_executor": True,
        }
    )
    started = time.perf_counter()
    new_results: list[dict[str, Any]] = []
    autonomous_index_by_id = {
        str(cell["cell_id"]): index
        for index, cell in enumerate(manifest["autonomous_cells"], start=1)
    }
    for index, stratum in enumerate(selected, start=1):
        progress.emit(
            {
                "stage": f"e2a_{phase}_stratum_started",
                "stratum_id": stratum["stratum_id"],
                "completed_strata": index - 1,
                "total_strata": len(selected),
            }
        )
        result = execute_one_stratum(
            stratum=stratum,
            manifest=manifest,
            output_root=output_root,
            progress=progress,
            autonomous_index=autonomous_index_by_id[str(stratum["donor_cell_id"])],
        )
        new_results.append(result)
        elapsed = max(time.perf_counter() - started, 1.0e-9)
        throughput = index / elapsed
        progress.emit(
            {
                "stage": f"e2a_{phase}_progress",
                "stratum_id": stratum["stratum_id"],
                "completed_strata": index,
                "total_strata": len(selected),
                "completed_sessions": index * 5,
                "total_sessions": len(selected) * 5,
                "throughput_strata_per_hour": round(throughput * 3600.0, 3),
                "eta_seconds": round((len(selected) - index) / throughput, 1),
            }
        )
    all_results = completed + new_results
    if canary:
        defects = _canary_defects(new_results)
        summary = {
            "schema_version": "chemworld-work-ii-e2a-formal-canary-summary-0.1",
            "study_id": manifest["study_id"],
            "cluster_id": canary_cluster,
            "stratum_count": len(new_results),
            "session_count": sum(len(row["cell_results"]) for row in new_results),
            "qualified": not defects,
            "platform_schema_binding_accounting_defects": defects,
            "poor_scientific_performance_is_not_a_stop_rule": True,
            "scientific_failures_retained": True,
        }
        write_json_atomic(output_root / "canary-summary.json", summary)
        status = "canary_qualified_hold_for_remaining" if not defects else "canary_failed_hold"
        write_json_atomic(
            output_root / "execution-summary.json",
            _execution_summary(manifest, all_results, execution_status=status),
        )
        progress.emit(
            {
                "stage": status,
                "completed_strata": len(all_results),
                "total_strata": 45,
                "defect_count": len(defects),
            }
        )
        return 0 if not defects else 2
    status = "completed" if len(all_results) == 45 else "incomplete"
    write_json_atomic(
        output_root / "execution-summary.json",
        _execution_summary(manifest, all_results, execution_status=status),
    )
    progress.emit(
        {
            "stage": f"e2a_formal_cohort_{status}",
            "completed_strata": len(all_results),
            "total_strata": 45,
        }
    )
    return 0 if status == "completed" else 2


def _final_snapshot(snapshots: object) -> Mapping[str, Any] | None:
    if not isinstance(snapshots, list):
        return None
    rows = [row for row in snapshots if isinstance(row, Mapping) and row.get("stage") == "final"]
    return rows[0] if len(rows) == 1 else None


def _law_for_condition(
    condition: str,
    result: Mapping[str, Any],
    *,
    donor: Mapping[str, Any] | None,
    oracle_artifact: Mapping[str, Any],
) -> Mapping[str, Any] | None:
    if condition == "oracle_law":
        law = oracle_artifact.get("law_summary")
        return law if isinstance(law, Mapping) else None
    if condition in {"autonomous_exploration", "learned_law_only"}:
        source = result if condition == "autonomous_exploration" else donor
        campaign = source.get("campaign_summary") if isinstance(source, Mapping) else None
        campaign = campaign if isinstance(campaign, Mapping) else {}
        analysis = campaign.get("analysis")
        analysis = analysis if isinstance(analysis, Mapping) else {}
        final = _final_snapshot(analysis.get("belief_snapshots"))
        law = final.get("law_summary") if isinstance(final, Mapping) else None
        return law if isinstance(law, Mapping) else None
    if condition == "yoked_evidence":
        final = _final_snapshot(result.get("belief_snapshots"))
        law = final.get("law_summary") if isinstance(final, Mapping) else None
        return law if isinstance(law, Mapping) else None
    return None


def _law_error(
    law_payload: Mapping[str, Any] | None,
    *,
    truth_plan: Mapping[str, Any],
    truth: Mapping[str, Mapping[str, Any]],
    allowed_feature_ids: Sequence[str],
    allowed_metric_ids: Sequence[str],
) -> float | None:
    if law_payload is None:
        return None
    evidence = law_payload.get("evidence_ids")
    evidence_ids = [str(item) for item in evidence] if isinstance(evidence, list) else []
    try:
        law = parse_work_ii_law_summary(
            law_payload,
            allowed_feature_ids=allowed_feature_ids,
            allowed_metric_ids=allowed_metric_ids,
            evidence_catalog=evidence_ids,
            required_metric_ids=allowed_metric_ids,
        )
        predictions: list[dict[str, Any]] = []
        for query in truth_plan["queries"]:
            values = law.predict(query["feature_values"])
            predictions.append(
                {
                    "query_id": str(query["query_id"]),
                    "metrics": [
                        {"metric_id": str(metric_id), "mean": values[str(metric_id)]}
                        for metric_id in query["metric_ids"]
                    ],
                }
            )
        return score_prediction_error(predictions, truth).error
    except (KeyError, ValueError, WorkIIAnalysisError):
        return None


def _snapshot_error(
    snapshot: Mapping[str, Any] | None,
    truth: Mapping[str, Mapping[str, Any]],
) -> float | None:
    if not isinstance(snapshot, Mapping):
        return None
    predictions = snapshot.get("predictions")
    if not isinstance(predictions, list):
        return None
    try:
        return score_prediction_error(predictions, truth).error
    except WorkIIAnalysisError:
        return None


def _add_cluster_bootstrap(
    analysis: dict[str, Any],
    *,
    cluster_task: Mapping[str, str],
    resamples: int = 10_000,
) -> None:
    rng = np.random.default_rng(20260824)
    for summary in analysis["contrast_summaries"]:
        rows = [dict(row) for row in summary["cluster_rows"]]
        by_task = {
            task_id: [row for row in rows if cluster_task[str(row["cluster_id"])] == task_id]
            for task_id in sorted(set(cluster_task.values()))
        }
        draws = np.empty(resamples, dtype=float)
        for draw_index in range(resamples):
            sampled: list[float] = []
            for task_rows in by_task.values():
                indices = rng.integers(0, len(task_rows), size=len(task_rows))
                sampled.extend(
                    float(task_rows[int(index)]["mean_failure_aware_normalized_regret_difference"])
                    for index in indices
                )
            draws[draw_index] = float(np.mean(sampled))
        summary["cluster_bootstrap_resample_count"] = resamples
        summary["cluster_bootstrap_stratified_by_task"] = True
        summary["failure_aware_normalized_regret_difference_ci95"] = [
            float(np.quantile(draws, 0.025)),
            float(np.quantile(draws, 0.975)),
        ]


def _condition_summaries(cell_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for condition in CONDITIONS:
        rows = [row for row in cell_rows if row.get("condition") == condition]
        summaries.append(
            {
                "condition": condition,
                "scheduled_session_count": len(rows),
                "missing_or_unranked_session_count": sum(
                    row.get("status") == "failed_missing_terminal_ranking" for row in rows
                ),
                "mean_failure_aware_normalized_regret": float(
                    np.mean([float(row["failure_aware_normalized_regret"]) for row in rows])
                ),
                "top1_count": sum(int(row["top1"]) for row in rows),
                "within_0_01_count": sum(int(row["within_0_01_of_best"]) for row in rows),
                "mean_pairwise_ranking_agreement": (
                    float(
                        np.mean(
                            [
                                float(
                                    row[
                                        "pairwise_ranking_agreement_excluding_truth_gaps_below_0_01"
                                    ]
                                )
                                for row in rows
                                if row.get(
                                    "pairwise_ranking_agreement_excluding_truth_gaps_below_0_01"
                                )
                                is not None
                            ]
                        )
                    )
                    if any(
                        row.get("pairwise_ranking_agreement_excluding_truth_gaps_below_0_01")
                        is not None
                        for row in rows
                    )
                    else None
                ),
            }
        )
    return summaries


def analyze_formal(
    *,
    manifest: Mapping[str, Any],
    output_root: Path,
    progress: Progress,
) -> dict[str, Any]:
    strata = [dict(row) for row in manifest["design_manifest"]["strata"]]
    retained = _load_completed_strata(output_root, strata)
    if len(retained) != 45:
        raise RuntimeError("formal analysis requires all 45 retained strata")
    results: dict[str, dict[str, Any]] = {
        str(cell_id): deepcopy(dict(row))
        for stratum in retained
        for cell_id, row in stratum["cell_results"].items()
    }
    clusters = _cluster_lookup(manifest)
    truth = {
        cluster_id: deepcopy(dict(cluster["candidate_truth"]))
        for cluster_id, cluster in clusters.items()
    }
    progress.emit(
        {
            "stage": "e2a_formal_analysis_started",
            "completed_sessions": 0,
            "total_sessions": 225,
        }
    )
    terminal = analyze_terminal_results(
        manifest["design_manifest"],
        results,
        candidate_truth_by_cluster=truth,
    )
    cluster_task = {
        str(row["cluster_id"]): str(row["task_id"]) for row in manifest["prepared_clusters"]
    }
    _add_cluster_bootstrap(terminal, cluster_task=cluster_task)
    mechanism_rows: list[dict[str, Any]] = []
    autonomous_cells = _autonomous_lookup(manifest)
    stratum_by_id = {str(row["stratum_id"]): row for row in strata}
    for index, cell in enumerate(manifest["design_manifest"]["cells"], start=1):
        cell_id = str(cell["cell_id"])
        result = results[cell_id]
        stratum = stratum_by_id[str(cell["stratum_id"])]
        donor = results.get(str(stratum["donor_cell_id"]))
        cluster = clusters[str(cell["cluster_id"])]
        oracle_artifact = _load(output_root / str(cluster["oracle_artifact_path"]))
        law = _law_for_condition(
            str(cell["condition"]),
            result,
            donor=donor,
            oracle_artifact=oracle_artifact,
        )
        candidate_features = _load(output_root / str(cluster["candidate_feature_queries_path"]))[
            "queries"
        ]
        campaign_cell = autonomous_cells[str(stratum["donor_cell_id"])]
        checkpoint_truth = campaign_cell["checkpoint_truth"]
        law_error = _law_error(
            law,
            truth_plan=campaign_cell["checkpoint_truth_plan"],
            truth=checkpoint_truth,
            allowed_feature_ids=cluster["allowed_feature_ids"],
            allowed_metric_ids=cluster["allowed_metric_ids"],
        )
        submission = result.get("submission")
        submitted_ranking = submission.get("ranking") if isinstance(submission, Mapping) else None
        implied: list[str] | None = None
        if law is not None:
            try:
                predicted = predict_candidate_ranking_from_law(
                    law,
                    candidate_queries=candidate_features,
                    allowed_feature_ids=cluster["allowed_feature_ids"],
                    allowed_metric_ids=cluster["allowed_metric_ids"],
                    evidence_catalog=(
                        [str(item) for item in law.get("evidence_ids", [])]
                        if isinstance(law.get("evidence_ids"), list)
                        else []
                    ),
                )
                implied = list(predicted["law_implied_ranking"])
            except (KeyError, ValueError):
                implied = None
        snapshots: object = None
        condition = str(cell["condition"])
        if condition == "autonomous_exploration":
            campaign = result.get("campaign_summary")
            campaign = campaign if isinstance(campaign, Mapping) else {}
            campaign_analysis = campaign.get("analysis")
            campaign_analysis = campaign_analysis if isinstance(campaign_analysis, Mapping) else {}
            snapshots = campaign_analysis.get("belief_snapshots")
        elif condition == "yoked_evidence":
            snapshots = result.get("belief_snapshots")
        pre = (
            next(
                (
                    row
                    for row in snapshots
                    if isinstance(row, Mapping) and row.get("stage") == "pre_evidence"
                ),
                None,
            )
            if isinstance(snapshots, list)
            else None
        )
        final = _final_snapshot(snapshots)
        pre_error = _snapshot_error(pre, checkpoint_truth)
        final_error = _snapshot_error(final, checkpoint_truth)
        mechanism_rows.append(
            {
                "cell_id": cell_id,
                "cluster_id": str(cell["cluster_id"]),
                "stratum_id": str(cell["stratum_id"]),
                "task_id": str(cell["task_id"]),
                "world_seed": int(cell["world_seed"]),
                "prior_arm": str(cell["prior_arm"]),
                "condition": condition,
                "executable_law_present": law is not None,
                "final_executable_law_error": law_error,
                "pre_prediction_error": pre_error,
                "final_prediction_error": final_error,
                "pre_to_final_prediction_error_change": (
                    None if pre_error is None or final_error is None else pre_error - final_error
                ),
                **evaluate_law_action_agreement(submitted_ranking, implied),
            }
        )
        if index % 25 == 0 or index == 225:
            progress.emit(
                {
                    "stage": "e2a_formal_analysis_progress",
                    "completed_sessions": index,
                    "total_sessions": 225,
                }
            )
    analysis = {
        **terminal,
        "formal_result": True,
        "study_id": manifest["study_id"],
        "condition_summaries": _condition_summaries(terminal["cell_rows"]),
        "mechanism_rows": mechanism_rows,
        "resource_and_failure_summary": _load(output_root / "execution-summary.json"),
        "provider_free_truth_query_count": manifest["provider_free_truth_query_count"],
        "provider_free_exact_replay_count": manifest["provider_free_exact_replay_count"],
        "fit_candidate_overlap_count": sum(
            int(row["fit_candidate_overlap_count"]) for row in manifest["qualification_rows"]
        ),
    }
    analysis["analysis_sha256"] = canonical_json_sha256(analysis)
    write_json_atomic(output_root / "analysis.json", analysis)
    _write_report_zh(output_root / "REPORT_ZH.md", analysis)
    progress.emit(
        {
            "stage": "e2a_formal_analysis_terminal",
            "completed_sessions": 225,
            "total_sessions": 225,
        }
    )
    return analysis


def _write_report_zh(path: Path, analysis: Mapping[str, Any]) -> None:
    resource = analysis["resource_and_failure_summary"]
    lines = [
        "# W2-51 evidence-to-action 五条件因果分解",
        "",
        (
            f"正式分母为 {analysis['scheduled_session_count']} 个 fresh sessions、"
            f"{resource['autonomous_donor_count']} 个 autonomous donors 和 "
            f"{resource['participant_physical_experiment_denominator']} 次预定 "
            "participant experiments。"
        ),
        "",
        "## 条件结果",
        "",
        (
            "| condition | sessions | missing/unranked | mean normalized regret | "
            "Top-1 | within 0.01 |"
        ),
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in analysis["condition_summaries"]:
        lines.append(
            f"| {row['condition']} | {row['scheduled_session_count']} | "
            f"{row['missing_or_unranked_session_count']} | "
            f"{row['mean_failure_aware_normalized_regret']:.4f} | "
            f"{row['top1_count']} | {row['within_0_01_count']} |"
        )
    lines.extend(
        [
            "",
            "## 预注册对比",
            "",
            "负值表示前一个条件的 regret 更低。置信区间按 task 内 world cluster 重采样。",
            "",
            "| contrast | clusters | mean regret difference | cluster-bootstrap 95% CI |",
            "|---|---:|---:|---:|",
        ]
    )
    for row in analysis["contrast_summaries"]:
        ci = row["failure_aware_normalized_regret_difference_ci95"]
        lines.append(
            f"| {row['contrast']} | {row['independent_cluster_count']} | "
            f"{row['mean_failure_aware_normalized_regret_difference']:.4f} | "
            f"[{ci[0]:.4f}, {ci[1]:.4f}] |"
        )
    lines.extend(
        [
            "",
            "## 完整性",
            "",
            f"- retained cell records: {resource['retained_cell_record_count']}/225",
            f"- failed retained: {resource['failed_retained_cell_count']}",
            f"- donor-blocked descendants: {resource['donor_blocked_descendant_count']}",
            (
                "- participant experiments: "
                f"{resource['participant_physical_experiment_observed']}/"
                f"{resource['participant_physical_experiment_denominator']}"
            ),
            f"- provider calls: {resource['provider_call_count']} (report-only accounting)",
            f"- provider-free truth + exact replay: {analysis['provider_free_truth_query_count']}",
            f"- oracle fit/candidate overlap: {analysis['fit_candidate_overlap_count']}",
            "- outcome-based replacement: 0",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--execute-canary", action="store_true")
    parser.add_argument("--execute-remaining", action="store_true")
    parser.add_argument("--analyze", action="store_true")
    parser.add_argument("--finalize-rejected-preparation", action="store_true")
    parser.add_argument("--allow-provider-execution", action="store_true")
    args = parser.parse_args()
    if not any(
        (
            args.prepare,
            args.execute_canary,
            args.execute_remaining,
            args.analyze,
            args.finalize_rejected_preparation,
        )
    ):
        parser.error(
            "select --prepare, --execute-canary, --execute-remaining, --analyze, "
            "or --finalize-rejected-preparation"
        )
    if args.execute_canary and args.execute_remaining:
        parser.error("canary and remaining execution are separate operational gates")
    if args.finalize_rejected_preparation and any(
        (args.prepare, args.execute_canary, args.execute_remaining, args.analyze)
    ):
        parser.error("rejected preparation finalization must run by itself")
    output_root = (
        args.output_root if args.output_root.is_absolute() else ROOT / args.output_root
    ).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    protocol_path = (
        args.protocol if args.protocol.is_absolute() else ROOT / args.protocol
    ).resolve()
    protocol = _load(protocol_path)
    progress = Progress(output_root / "progress.jsonl")
    manifest_path = output_root / "input_manifest.json"
    if args.finalize_rejected_preparation:
        finalize_rejected_preparation(
            protocol=protocol,
            output_root=output_root,
            progress=progress,
        )
        return 0
    if args.prepare:
        manifest = prepare_formal(
            protocol=protocol,
            output_root=output_root,
            progress=progress,
        )
        progress.emit(
            {
                "stage": "e2a_formal_provider_free_preparation_complete",
                "clusters": len(manifest["prepared_clusters"]),
                "sessions": manifest["scheduled_session_count"],
                "truth_queries": manifest["provider_free_truth_query_count"],
                "exact_replay_queries": manifest["provider_free_exact_replay_count"],
                "provider_calls": 0,
            }
        )
        if not any((args.execute_canary, args.execute_remaining, args.analyze)):
            return 0
    else:
        if not manifest_path.is_file():
            raise RuntimeError("formal input manifest has not been prepared")
        manifest = _load(manifest_path)
    _validate_manifest(manifest)
    if args.execute_canary or args.execute_remaining:
        if not args.allow_provider_execution:
            raise RuntimeError("provider execution requires --allow-provider-execution")
        code = execute_phase(
            manifest=manifest,
            output_root=output_root,
            progress=progress,
            canary=bool(args.execute_canary),
        )
        if code:
            return code
    if args.analyze:
        analyze_formal(manifest=manifest, output_root=output_root, progress=progress)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
