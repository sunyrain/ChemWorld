"""Run a small development-only Scientific Adaptation shakedown."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, cast
from uuid import uuid4

from chemworld.agents.scientific_adaptation import (
    ScientificPlanValidationError,
    canonical_sha256,
)
from chemworld.eval.mechanism_adaptation_execution import (
    load_json_object,
    load_protocol_object,
    selected_campaign_rows,
)
from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.scientific_adaptation_execution import (
    ScientificAdaptationExperimentSession,
    build_scientific_adaptation_agent,
)
from chemworld.providers.deepseek import DeepSeekAPIError, JsonCompletion
from chemworld.providers.wellau import ReasoningEffort, WellAUClient

ROOT = Path(__file__).resolve().parents[1]
DEVELOPMENT_TEST_PROTOCOL = (
    ROOT / "configs/benchmark/mechanism_adaptation_v0.3.0_rc28.json"
)
DEVELOPMENT_TEST_METHODS = (
    ROOT / "configs/methods/llm_v0.4/participant_methods_development.json"
)
DEFAULT_METHOD_IDS = (
    "dev_pro_direct",
    "dev_pro_stateful",
    "dev_flash_direct",
    "dev_flash_stateful",
)
REPORT_SCHEMA_VERSION = "chemworld-scientific-adaptation-shakedown-0.2-dev"
DEFAULT_TASK = "reaction-to-crystallization"


class _DeterministicMockClient:
    """Exercise the provider boundary without making an external request."""

    def __init__(self, *, model: str) -> None:
        self.model = model
        self.thinking = False
        self.reasoning_effort = None

    def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
    ) -> JsonCompletion:
        del system_prompt, max_tokens
        prompt = json.loads(user_prompt)
        context = prompt["public_experiment_context"]
        scaffold = prompt["scaffold_context"]
        history = context["experiment_history"]
        candidates = tuple(context["mechanism_candidates"])
        distribution = _mock_distribution(candidates, history)
        vector = _mock_search_vector(
            int(context["experiment_interface"]["search_vector_dimension"]),
            len(history),
            history,
        )
        payload: dict[str, Any] = {
            "experiment_intent": _mock_intent(len(history)),
            "search_vector": vector,
            "requested_measurement_slots": [
                item["slot_id"]
                for item in context["experiment_interface"]["diagnostic_measurement_slots"]
            ],
            "diagnostic_target": "matched response contrast across the public history",
            "mechanism_distribution": distribution,
            "expected_effect": "the matched probe should reveal a reproducible score contrast",
            "belief_update_rule": (
                "increase change-family belief after a material drop from the public reference"
            ),
            "uncertainty": 0.65 if len(history) < 2 else 0.35,
        }
        if scaffold["scaffold_id"] == "stateful_scientific":
            payload["scientific_state"] = {
                "belief": distribution,
                "unresolved_question": "Is the latest response stable under a matched probe?",
                "next_experiment_plan": {
                    "intent": _mock_intent(len(history) + 1),
                    "controlled_variables": ["temperature", "solvent"],
                    "varied_variable": "catalyst dose",
                },
                "evidence_summary": _mock_evidence_summary(history),
            }
        prompt_tokens = max(len(user_prompt) // 4, 1)
        return JsonCompletion(
            payload=payload,
            model=self.model,
            usage={
                "prompt_tokens": prompt_tokens,
                "completion_tokens": 260,
                "total_tokens": prompt_tokens + 260,
                "prompt_cache_hit_tokens": 0,
                "prompt_cache_miss_tokens": prompt_tokens,
            },
            attempts=1,
        )

    def pricing_snapshot(self) -> dict[str, Any]:
        return {
            "schema_version": "chemworld-mock-pricing-0.1",
            "provider": "deterministic_mock",
            "model_id": self.model,
        }

    def estimate_cost_usd(self, usage: Mapping[str, Any]) -> float:
        del usage
        return 0.0


def _mock_intent(experiment_count: int) -> str:
    intents = (
        "establish a public reference experiment",
        "run a high-dose matched probe",
        "adapt with an opposing-dose confirmation",
    )
    return intents[min(experiment_count, len(intents) - 1)]


def _mock_search_vector(
    dimension: int,
    experiment_count: int,
    history: Sequence[Mapping[str, Any]],
) -> list[float]:
    vector = [0.5] * dimension
    if dimension == 10:
        dose_schedule = (0.36, 0.90, 0.05)
        vector[5] = dose_schedule[min(experiment_count, len(dose_schedule) - 1)]
        if experiment_count >= 2 and _latest_score(history) >= _first_score(history):
            vector[5] = 0.90
    return vector


def _mock_distribution(
    candidates: Sequence[str],
    history: Sequence[Mapping[str, Any]],
) -> dict[str, float]:
    if len(history) < 2:
        probability = 1.0 / len(candidates)
        return dict.fromkeys(candidates, probability)
    changed = abs(_latest_score(history) - _first_score(history)) >= 0.03
    selected = "rate_law_family" if changed and "rate_law_family" in candidates else "no_change"
    residual = 0.3 / (len(candidates) - 1)
    return {
        candidate_id: 0.7 if candidate_id == selected else residual for candidate_id in candidates
    }


def _first_score(history: Sequence[Mapping[str, Any]]) -> float:
    return float(history[0]["terminal_summary"]["leaderboard_score"])


def _latest_score(history: Sequence[Mapping[str, Any]]) -> float:
    return float(history[-1]["terminal_summary"]["leaderboard_score"])


def _mock_evidence_summary(
    history: Sequence[Mapping[str, Any]],
) -> list[dict[str, str]]:
    entries = [evidence for record in history for evidence in record["measurement_evidence"]][-2:]
    return [
        {
            "evidence_id": str(entry["evidence_id"]),
            "observation": f"Public evidence {entry['evidence_id']} was recorded.",
            "interpretation": "Retain this result for the next matched comparison.",
            "reliability": "high",
        }
        for entry in entries
    ]


def _stable_observation_seed(pair_id: str) -> int:
    digest = hashlib.sha256(f"scientific-adaptation|{pair_id}".encode()).digest()
    return int.from_bytes(digest[:4], "big")


def _run_cell(
    *,
    protocol: Mapping[str, Any],
    methods: Mapping[str, Any],
    method_id: str,
    row: Mapping[str, Any],
    provider: str,
    pre_experiments: int,
    post_experiments: int,
    resume_checkpoint: Mapping[str, Any] | None = None,
    client_override: Any | None = None,
) -> dict[str, Any]:
    method = methods["methods"][method_id]
    client = (
        client_override
        if client_override is not None
        else (
            _DeterministicMockClient(model=str(method["model_id"]))
            if provider == "mock"
            else (
                WellAUClient(
                    model=str(method["model_id"]),
                    reasoning_effort=cast(
                        ReasoningEffort,
                        str(method["request_configuration"]["reasoning_effort"]),
                    ),
                    timeout_s=float(method["request_configuration"]["timeout_s"]),
                    max_attempts=int(method["request_configuration"]["max_attempts"]),
                    retry_backoff_s=float(method["request_configuration"]["retry_backoff_s"]),
                )
                if provider == "wellau"
                else None
            )
        )
    )
    agent = build_scientific_adaptation_agent(
        protocol,
        row,
        llm_methods=methods,
        method_id=method_id,
        client=client,
    )
    history: list[dict[str, Any]] = copy.deepcopy(
        list(resume_checkpoint.get("public_history", [])) if resume_checkpoint is not None else []
    )
    experiments: list[dict[str, Any]] = copy.deepcopy(
        list(resume_checkpoint.get("experiments", [])) if resume_checkpoint is not None else []
    )
    if resume_checkpoint is not None:
        last_state = (
            experiments[-1]["result"]["plan"].get("scientific_state") if experiments else None
        )
        agent.restore_development_checkpoint(
            experiment_history=history,
            scientific_state=last_state,
            resources=resume_checkpoint["resources"],
        )
    failure: dict[str, Any] | None = None
    observation_seed = _stable_observation_seed(str(row["pair_id"]))
    planned_experiments = pre_experiments + post_experiments
    try:
        for experiment_index in range(len(experiments), planned_experiments):
            pre_change = experiment_index < pre_experiments
            phase = "pre_change" if pre_change else "post_change"
            interventions = () if pre_change else tuple(row["world_interventions"])
            with ScientificAdaptationExperimentSession(
                task_id=str(row["task_id"]),
                seed=int(row["world_seed"]),
                experiment_horizon=1,
                experiment_index_offset=experiment_index,
                interventions=interventions,
                observation_seed=observation_seed,
                observation_noise_namespace=(
                    f"scientific-adaptation-shakedown-{row['pair_id']}-"
                    f"experiment-{experiment_index:03d}"
                ),
            ) as session:
                plan = agent.plan_next(history)
                result = session.execute(plan)
                public_record = result.public_record()
                history.append(public_record)
                experiments.append(
                    {
                        "phase": phase,
                        "result": result.to_dict(),
                        "decision_audit": agent.decision_audit(),
                    }
                )
    except Exception as error:
        reason_code = _failure_reason_code(error)
        failure = {
            "reason_code": reason_code,
            "error_type": type(error).__name__,
            "message": " ".join(str(error).split())[:500],
            "scientific_retry_allowed": False,
            "infrastructure_resume_eligible": (reason_code == "provider_infrastructure_failure"),
            "runner_missing_only_resume_supported": False,
        }
        if isinstance(error, ScientificPlanValidationError):
            failure["validation_diagnostics"] = copy.deepcopy(
                error.validation_diagnostics
            )
    resources = agent.method_resource_usage()
    cell_status = "completed"
    if failure is not None:
        cell_status = (
            "infrastructure_failure"
            if failure["reason_code"] == "provider_infrastructure_failure"
            else "method_failure"
        )
        failure["runner_missing_only_resume_supported"] = cell_status == "infrastructure_failure"
    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "formal_result": False,
        "benchmark_claim_allowed": False,
        "provider_mode": provider,
        "mock_provider": provider == "mock",
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": canonical_sha256(protocol),
        "method_config_freeze_id": methods["freeze_id"],
        "method_config_sha256": canonical_sha256(methods),
        "method_id": method_id,
        "method_contract_sha256": canonical_sha256(method),
        "method": {
            "model_id": method["model_id"],
            "scaffold_id": method["scientific_adaptation_scaffold_id"],
        },
        "pair": {
            key: copy.deepcopy(row[key])
            for key in (
                "pair_id",
                "statistical_cluster_id",
                "task_id",
                "arm",
                "truth_id",
                "world_seed",
            )
        },
        "development_horizon": {
            "pre_change_experiments": pre_experiments,
            "post_change_experiments": post_experiments,
            "ordinary_change_detection_claim_allowed": False,
        },
        "cell_status": cell_status,
        "failure": failure,
        "agent_manifest": agent.manifest(),
        "resources": resources,
        "planned_experiment_count": planned_experiments,
        "experiment_count": len(experiments),
        "completed_experiment_count": sum(int(item["result"]["completed"]) for item in experiments),
        "scores": [item["result"]["terminal_summary"]["leaderboard_score"] for item in experiments],
        "experiments": experiments,
        "public_history": history,
    }


def _failure_reason_code(error: Exception) -> str:
    if isinstance(error, DeepSeekAPIError):
        return "provider_infrastructure_failure"
    if isinstance(error, ValueError):
        return "invalid_model_response"
    if isinstance(error, RuntimeError):
        return "experiment_execution_failure"
    if isinstance(error, OSError):
        return "provider_infrastructure_failure"
    return "unexpected_cell_failure"


def _infrastructure_attempt_paths(output: Path, cell_stem: str) -> list[Path]:
    return sorted((output / "infrastructure_attempts" / cell_stem).glob("*.json"))


def _write_infrastructure_attempt(
    output: Path,
    cell_stem: str,
    checkpoint: Mapping[str, Any],
) -> Path:
    path = output / "infrastructure_attempts" / cell_stem / f"{uuid4().hex}.json"
    write_json_atomic(
        path,
        {
            "schema_version": "chemworld-scientific-adaptation-infrastructure-attempt-0.1-dev",
            "status": "retryable_infrastructure_failure",
            "cell_stem": cell_stem,
            "checkpoint": copy.deepcopy(dict(checkpoint)),
            "checkpoint_sha256": canonical_sha256(checkpoint),
        },
    )
    return path


def run_shakedown(args: argparse.Namespace) -> dict[str, Any]:
    protocol = load_protocol_object(args.protocol)
    methods = load_json_object(args.llm_methods)
    method_ids = tuple(args.method_id or DEFAULT_METHOD_IDS)
    raw_tasks = getattr(args, "task", None)
    task_ids = [raw_tasks] if isinstance(raw_tasks, str) else list(raw_tasks or [DEFAULT_TASK])
    rows = [
        row
        for task_id in task_ids
        for row in selected_campaign_rows(
            protocol,
            tasks=[task_id],
            pair_ids=args.pair_id,
            limit=args.pair_limit,
        )
    ]
    if not rows:
        raise ValueError("development selection produced no campaign rows")
    arm_filter = getattr(args, "arm", None)
    if arm_filter:
        rows = [row for row in rows if row["arm"] == arm_filter]
    expected_calls = len(method_ids) * len(rows) * (args.pre_experiments + args.post_experiments)
    max_provider_total_tokens = int(getattr(args, "max_provider_total_tokens", 1_000_000))
    max_provider_output_tokens = int(getattr(args, "max_provider_output_tokens", 8_000))
    if expected_calls > args.max_provider_calls:
        raise ValueError(
            f"planned provider calls {expected_calls} exceed cap {args.max_provider_calls}"
        )
    if args.provider in {"deepseek", "wellau"} and not args.allow_external_provider:
        raise ValueError("--allow-external-provider is required for billable requests")
    max_method_output_tokens = max(
        int(methods["methods"][method_id]["request_configuration"]["max_tokens"])
        for method_id in method_ids
    )
    if max_method_output_tokens > max_provider_output_tokens:
        raise ValueError(
            f"method output cap {max_method_output_tokens} exceeds provider cap "
            f"{max_provider_output_tokens}"
        )

    cells: list[dict[str, Any]] = []
    terminal_receipts: list[dict[str, Any]] = []
    cumulative_cost = 0.0
    for method_id in method_ids:
        if method_id not in methods["methods"]:
            raise ValueError(f"unknown development method: {method_id}")
        for row in rows:
            filename = f"{method_id}--{row['pair_id']}--{row['arm']}.json"
            cell_stem = Path(filename).stem
            receipt_path = args.output / "receipts" / filename
            if receipt_path.exists():
                if not args.resume:
                    raise FileExistsError(f"receipt already exists: {receipt_path}")
                receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            else:
                attempt_paths = _infrastructure_attempt_paths(args.output, cell_stem)
                if attempt_paths and not args.resume:
                    raise FileExistsError(
                        f"infrastructure checkpoint exists without --resume: {cell_stem}"
                    )
                resume_checkpoint = None
                if attempt_paths:
                    attempt = json.loads(attempt_paths[-1].read_text(encoding="utf-8"))
                    resume_checkpoint = attempt["checkpoint"]
                receipt = _run_cell(
                    protocol=protocol,
                    methods=methods,
                    method_id=method_id,
                    row=row,
                    provider=args.provider,
                    pre_experiments=args.pre_experiments,
                    post_experiments=args.post_experiments,
                    resume_checkpoint=resume_checkpoint,
                )
                if receipt["cell_status"] == "infrastructure_failure":
                    _write_infrastructure_attempt(args.output, cell_stem, receipt)
                else:
                    write_json_atomic(receipt_path, receipt)
            cells.append(receipt)
            if receipt["cell_status"] != "infrastructure_failure":
                terminal_receipts.append(receipt)
            accounting_complete = bool(receipt["resources"]["accounting_complete"])
            if accounting_complete:
                cumulative_cost += float(receipt["resources"]["monetary_cost_usd"])
            cumulative_tokens = sum(
                int(item["resources"]["provider_usage"]["total_tokens"]) for item in cells
            )
            cost_text = (
                f"{receipt['resources']['monetary_cost_usd']:.6f}"
                if accounting_complete
                else "unknown"
            )
            print(
                f"{method_id} {row['arm']}: "
                f"{receipt['completed_experiment_count']}/"
                f"{receipt['planned_experiment_count']} "
                f"complete, status={receipt['cell_status']}, "
                f"cost_usd={cost_text}",
                flush=True,
            )
            if accounting_complete and cumulative_cost > args.max_provider_cost_usd:
                raise RuntimeError(
                    f"provider cost {cumulative_cost:.6f} exceeded cap "
                    f"{args.max_provider_cost_usd:.6f}"
                )
            if cumulative_tokens > max_provider_total_tokens:
                raise RuntimeError(
                    f"provider tokens {cumulative_tokens} exceeded cap {max_provider_total_tokens}"
                )

    prompt_token_estimate_cap = {
        method_id: int(
            methods["methods"][method_id]["scientific_adaptation_prompt_budget_contract"][
                "per_decision_max_estimated_tokens"
            ]
        )
        for method_id in method_ids
    }
    max_prompt_estimated_tokens = {
        method_id: max(
            (
                int(experiment["decision_audit"]["prompt_estimated_tokens"])
                for cell in cells
                if cell["method_id"] == method_id
                for experiment in cell["experiments"]
            ),
            default=0,
        )
        for method_id in method_ids
    }
    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "formal_result": False,
        "benchmark_claim_allowed": False,
        "provider_mode": args.provider,
        "mock_provider": args.provider == "mock",
        "task_ids": task_ids,
        "method_config_freeze_id": methods["freeze_id"],
        "method_config_sha256": canonical_sha256(methods),
        "method_contract_sha256": {
            method_id: canonical_sha256(methods["methods"][method_id]) for method_id in method_ids
        },
        "prompt_token_estimate_cap": prompt_token_estimate_cap,
        "max_prompt_estimated_tokens": max_prompt_estimated_tokens,
        "prompt_budget_within_contract": all(
            max_prompt_estimated_tokens[method_id] <= prompt_token_estimate_cap[method_id]
            for method_id in method_ids
        ),
        "runner_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "method_ids": list(method_ids),
        "pair_ids": list(dict.fromkeys(row["pair_id"] for row in rows)),
        "cell_count": len(cells),
        "terminal_receipt_count": len(terminal_receipts),
        "completed_cell_count": sum(int(item["cell_status"] == "completed") for item in cells),
        "failed_cell_count": sum(int(item["cell_status"] == "method_failure") for item in cells),
        "infrastructure_failure_cell_count": sum(
            int(item["cell_status"] == "infrastructure_failure") for item in cells
        ),
        "experiment_count": sum(int(item["experiment_count"]) for item in cells),
        "planned_experiment_count": sum(int(item["planned_experiment_count"]) for item in cells),
        "completed_experiment_count": sum(
            int(item["completed_experiment_count"]) for item in cells
        ),
        "provider_call_count": sum(int(item["resources"]["model_call_count"]) for item in cells),
        "provider_attempt_count": sum(
            int(item["resources"]["provider_attempt_count"]) for item in cells
        ),
        "accounting_complete": all(
            bool(item["resources"]["accounting_complete"]) for item in cells
        ),
        "provider_billed_cost_usd": (
            cumulative_cost
            if all(bool(item["resources"]["accounting_complete"]) for item in cells)
            else None
        ),
        "provider_reported_total_tokens": sum(
            int(item["resources"]["provider_usage"]["total_tokens"]) for item in cells
        ),
        "provider_reported_output_tokens": sum(
            int(item["resources"]["provider_usage"]["completion_tokens"]) for item in cells
        ),
        "provider_input_token_count": sum(
            int(item["resources"]["provider_usage"]["prompt_tokens"]) for item in cells
        ),
        "provider_output_token_count": sum(
            int(item["resources"]["provider_usage"]["completion_tokens"]) for item in cells
        ),
        "provider_total_token_count": sum(
            int(item["resources"]["provider_usage"]["total_tokens"]) for item in cells
        ),
        "max_provider_calls": args.max_provider_calls,
        "max_provider_cost_usd": args.max_provider_cost_usd,
        "max_provider_total_tokens": max_provider_total_tokens,
        "max_provider_output_tokens_per_call": max_provider_output_tokens,
        "cost_cap_enforceable": all(
            bool(item["resources"]["accounting_complete"]) for item in cells
        ),
        "receipt_sha256": {
            (
                f"{item['method_id']}:{item['pair']['pair_id']}:{item['pair']['arm']}"
            ): canonical_sha256(item)
            for item in terminal_receipts
        },
        "latest_infrastructure_checkpoint_sha256": {
            (
                f"{item['method_id']}:{item['pair']['pair_id']}:{item['pair']['arm']}"
            ): canonical_sha256(item)
            for item in cells
            if item["cell_status"] == "infrastructure_failure"
        },
        "execution_complete": not any(
            item["cell_status"] == "infrastructure_failure" for item in cells
        ),
        "interpretation": (
            "Development shakedown only. It validates execution and accounting; "
            "it does not estimate a Participant outcome or method effect."
        ),
    }
    write_json_atomic(args.output / "report.json", report)
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--llm-methods", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--provider", choices=("mock", "deepseek", "wellau"), default="mock")
    parser.add_argument("--allow-external-provider", action="store_true")
    parser.add_argument("--task", action="append")
    parser.add_argument("--pair-id", action="append")
    parser.add_argument("--pair-limit", type=int, default=1)
    parser.add_argument("--arm", choices=("changed", "no_change_twin"))
    parser.add_argument("--method-id", action="append")
    parser.add_argument("--pre-experiments", type=int, default=1)
    parser.add_argument("--post-experiments", type=int, default=2)
    parser.add_argument("--max-provider-calls", type=int, default=24)
    parser.add_argument("--max-provider-cost-usd", type=float, default=0.50)
    parser.add_argument("--max-provider-total-tokens", type=int, default=1_000_000)
    parser.add_argument("--max-provider-output-tokens", type=int, default=8_000)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if args.pre_experiments <= 0 or args.post_experiments <= 0:
        parser.error("development experiment counts must be positive")
    if (
        args.max_provider_calls <= 0
        or args.max_provider_cost_usd < 0.0
        or args.max_provider_total_tokens <= 0
        or args.max_provider_output_tokens <= 0
    ):
        parser.error("provider caps must be positive")
    return args


def main() -> None:
    report = run_shakedown(parse_args())
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    if not report["execution_complete"]:
        raise RuntimeError(
            "development execution has retryable infrastructure checkpoints; rerun with --resume"
        )


if __name__ == "__main__":
    main()
