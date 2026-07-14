"""Formal PPO/SAC contracts and execution adapters for benchmark v0.5.

This module deliberately separates three states that older RL development
artifacts conflated:

* a method contract can be audited without importing the optional ML stack;
* a checkpoint becomes eligible only after its own training-resource ledger is
  verified and bound to the exact task/action/reward/backend contracts;
* an evaluation cell reports inference resources only and references, but never
  copies, checkpoint training resources.

No function in this module selects a checkpoint from Bench or reference-search
evidence, and the contract audit never claims formal performance.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, Protocol, cast

import gymnasium as gym

import chemworld  # noqa: F401 - registers the environment
from chemworld.eval.formal_runner import (
    FormalAdapterRegistry,
    FormalCellSpec,
    MethodKind,
    PrivateCellRuntime,
)
from chemworld.eval.resource_accounting_v0_4 import audit_rl_training_resource
from chemworld.rl.hybrid_actions import (
    LATENT_ADAPTER_VERSION,
    conditional_hybrid_action_contract,
    policy_distribution_contract,
)
from chemworld.rl.rewards import reward_contract
from chemworld.tasks import get_task

FORMAL_RL_CONFIG_VERSION = "chemworld-formal-rl-methods-0.4"
FORMAL_RL_REPORT_VERSION = "chemworld-formal-rl-contract-controls-0.4"
FORMAL_RL_CHECKPOINT_INDEX_VERSION = "chemworld-formal-rl-checkpoint-index-0.4"
DEFAULT_CONFIG_PATH = Path("configs/methods/rl_v0.4/rl_methods.json")
DEFAULT_FORMAL_PROTOCOL_PATH = Path("configs/benchmark/formal_protocol_v0.4.json")
DEFAULT_INTERACTION_PATH = Path("configs/benchmark/interaction_strata_v0.4.json")
DEFAULT_PREFLIGHT_REPORT_PATH = Path("workstreams/benchmark_v1/reports/formal-preflight-v0.4.json")
DEFAULT_RESOURCE_REPORT_PATH = Path(
    "workstreams/benchmark_v1/reports/resource-accounting-v0.4.json"
)

RLMethodId = Literal["ppo", "sac"]


class FormalRLContractError(ValueError):
    """Raised when a formal RL artifact fails a frozen contract."""


class _AgentLike(Protocol):
    """Structural type used to inject a dependency-free test agent."""


AgentFactory = Callable[["RLCheckpointBinding", int], _AgentLike]
RunAgent = Callable[..., Any]


def canonical_sha256(payload: Any) -> str:
    """Return the canonical JSON digest used by formal RL controls."""

    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def file_sha256(path: str | Path) -> str:
    """Hash one on-disk artifact without following a directory contract."""

    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_formal_rl_config(path: str | Path = DEFAULT_CONFIG_PATH) -> dict[str, Any]:
    """Load the v0.4 formal RL method contract."""

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise FormalRLContractError("formal RL config must be a JSON object")
    return payload


def _load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FormalRLContractError(f"{label} cannot be loaded: {path}") from exc
    if not isinstance(payload, dict):
        raise FormalRLContractError(f"{label} must be a JSON object")
    return payload


def _resolve_inside(root: Path, value: str | Path, label: str) -> Path:
    path = (root / value).resolve() if not Path(value).is_absolute() else Path(value).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as exc:
        raise FormalRLContractError(f"{label} must stay inside the repository") from exc
    if path.is_symlink() or not path.is_file():
        raise FormalRLContractError(f"{label} is missing or not a regular file: {path}")
    return path


def _required_text(payload: Mapping[str, Any], field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise FormalRLContractError(f"{field} must be a non-empty string")
    return value


def _required_method_id(value: Any) -> RLMethodId:
    if value not in {"ppo", "sac"}:
        raise FormalRLContractError("formal RL method_id must be ppo or sac")
    return cast(RLMethodId, value)


def _parameter_keys(action_contract: Mapping[str, Any]) -> tuple[str, ...]:
    adapter = action_contract.get("training_adapter")
    if not isinstance(adapter, Mapping):
        raise FormalRLContractError("action contract is missing its training adapter")
    values = adapter.get("parameter_coordinate_keys")
    if (
        not isinstance(values, list)
        or not values
        or not all(isinstance(item, str) and item for item in values)
    ):
        raise FormalRLContractError("action contract parameter keys are invalid")
    return tuple(values)


def task_contract_bundle(task_id: str) -> dict[str, Any]:
    """Build dependency-free action/reward/policy contracts for one task."""

    task = get_task(task_id)
    env = gym.make("ChemWorld", task_id=task_id)
    try:
        if not isinstance(env.action_space, gym.spaces.Dict):
            raise FormalRLContractError("ChemWorld formal RL action space must be Dict")
        action = conditional_hybrid_action_contract(env.action_space)
    finally:
        env.close()
    policy = policy_distribution_contract(_parameter_keys(action))
    reward = reward_contract(task.allowed_operations)
    return {
        "task_id": task_id,
        "action_contract": action,
        "action_contract_sha256": action["contract_hash"],
        "training_reward_contract": reward,
        "training_reward_contract_sha256": reward["contract_hash"],
        "ppo_policy_distribution_contract": policy,
        "ppo_policy_distribution_contract_sha256": policy["contract_hash"],
    }


@dataclass(frozen=True)
class RLCheckpointBinding:
    """Verified checkpoint, training manifest, and separate resource ledger."""

    method_id: RLMethodId
    task_id: str
    checkpoint_path: Path
    checkpoint_manifest_path: Path
    training_resource_path: Path
    checkpoint_sha256: str
    checkpoint_manifest: dict[str, Any]
    training_resource: dict[str, Any]
    contract_bundle: dict[str, Any]

    @classmethod
    def from_payload(
        cls,
        payload: Mapping[str, Any],
        *,
        root: str | Path,
        formal_protocol: Mapping[str, Any] | None = None,
    ) -> RLCheckpointBinding:
        """Verify a task-specific checkpoint binding and its split resources."""

        repository = Path(root).resolve()
        method_id = _required_method_id(payload.get("method_id"))
        task_id = _required_text(payload, "task_id")
        checkpoint = _resolve_inside(
            repository, _required_text(payload, "checkpoint_path"), "RL checkpoint"
        )
        manifest_path = _resolve_inside(
            repository,
            _required_text(payload, "checkpoint_manifest_path"),
            "RL checkpoint manifest",
        )
        training_path = _resolve_inside(
            repository,
            _required_text(payload, "training_resource_path"),
            "RL training resource ledger",
        )
        manifest = _load_object(manifest_path, "RL checkpoint manifest")
        training = _load_object(training_path, "RL training resource ledger")
        digest = file_sha256(checkpoint)
        if payload.get("checkpoint_sha256") != digest:
            raise FormalRLContractError("checkpoint index digest does not match checkpoint")
        if manifest.get("schema_version") != "chemworld-rl-checkpoint-0.2":
            raise FormalRLContractError("checkpoint manifest schema is not formal-compatible")
        if manifest.get("algorithm") != method_id or manifest.get("task_id") != task_id:
            raise FormalRLContractError("checkpoint algorithm/task binding is invalid")
        if manifest.get("checkpoint_sha256") != digest:
            raise FormalRLContractError("checkpoint manifest digest does not match checkpoint")

        protocol = (
            dict(formal_protocol)
            if formal_protocol is not None
            else _load_object(repository / DEFAULT_FORMAL_PROTOCOL_PATH, "formal protocol")
        )
        formal_tasks = protocol.get("task_roles", {}).get("formal_core", {})
        if not isinstance(formal_tasks, Mapping) or task_id not in formal_tasks:
            raise FormalRLContractError("checkpoint task is not a formal-core task")
        train_split = protocol.get("split_contract", {}).get("train", {})
        allocation = manifest.get("allocation")
        if not isinstance(allocation, Mapping) or allocation.get("name") != "train":
            raise FormalRLContractError("checkpoint was not trained on the Train allocation")
        if allocation.get("namespace_id") != train_split.get("namespace_id"):
            raise FormalRLContractError("checkpoint Train namespace does not match protocol")
        if manifest.get("bench_finetuning_used") is not False:
            raise FormalRLContractError("checkpoint must explicitly deny Bench fine-tuning")

        contracts = task_contract_bundle(task_id)
        expected = {
            "action_contract_hash": contracts["action_contract_sha256"],
            "training_reward_contract_hash": contracts["training_reward_contract_sha256"],
        }
        if method_id == "ppo":
            expected["policy_distribution_contract_hash"] = contracts[
                "ppo_policy_distribution_contract_sha256"
            ]
        for contract_field, expected_value in expected.items():
            if manifest.get(contract_field) != expected_value:
                raise FormalRLContractError(f"checkpoint {contract_field} is incompatible")

        audited_training = audit_rl_training_resource(training)
        if audited_training.get("accounting_complete") is not True:
            reasons = audited_training.get("failure_reasons", [])
            raise FormalRLContractError(
                "checkpoint training-resource ledger is incomplete: "
                + ", ".join(str(item) for item in reasons)
            )
        if audited_training.get("checkpoint_sha256") != digest:
            raise FormalRLContractError("training resources reference a different checkpoint")
        if training.get("source_manifest_sha256") != file_sha256(manifest_path):
            raise FormalRLContractError("training resources do not bind the checkpoint manifest")
        return cls(
            method_id=method_id,
            task_id=task_id,
            checkpoint_path=checkpoint,
            checkpoint_manifest_path=manifest_path,
            training_resource_path=training_path,
            checkpoint_sha256=digest,
            checkpoint_manifest=manifest,
            training_resource=training,
            contract_bundle=contracts,
        )

    def public_summary(self) -> dict[str, Any]:
        """Return the non-secret identity needed by preflight and method freeze."""

        return {
            "method_id": self.method_id,
            "task_id": self.task_id,
            "checkpoint_sha256": self.checkpoint_sha256,
            "checkpoint_manifest_sha256": file_sha256(self.checkpoint_manifest_path),
            "training_resource_sha256": file_sha256(self.training_resource_path),
            "training_environment_step_count": self.training_resource.get(
                "training_environment_step_count"
            ),
            "training_resources_separate_from_evaluation": True,
            "action_contract_sha256": self.contract_bundle["action_contract_sha256"],
            "training_reward_contract_sha256": self.contract_bundle[
                "training_reward_contract_sha256"
            ],
            "ppo_policy_distribution_contract_sha256": (
                self.contract_bundle["ppo_policy_distribution_contract_sha256"]
                if self.method_id == "ppo"
                else None
            ),
        }


def load_checkpoint_index(
    path: str | Path,
    *,
    root: str | Path,
    formal_protocol: Mapping[str, Any] | None = None,
) -> tuple[RLCheckpointBinding, ...]:
    """Load an exact task-by-method checkpoint index after training completes."""

    index = _load_object(Path(path), "formal RL checkpoint index")
    if index.get("schema_version") != FORMAL_RL_CHECKPOINT_INDEX_VERSION:
        raise FormalRLContractError("formal RL checkpoint index schema is unsupported")
    entries = index.get("checkpoints")
    if not isinstance(entries, list) or not entries:
        raise FormalRLContractError("formal RL checkpoint index is empty")
    bindings = tuple(
        RLCheckpointBinding.from_payload(
            item,
            root=root,
            formal_protocol=formal_protocol,
        )
        for item in entries
    )
    keys = [(item.method_id, item.task_id) for item in bindings]
    if len(keys) != len(set(keys)):
        raise FormalRLContractError("formal RL checkpoint index has duplicate method/task")
    return bindings


def _default_agent_factory(binding: RLCheckpointBinding, method_seed: int) -> _AgentLike:
    from chemworld.agents.rl import FrozenSB3Agent

    return FrozenSB3Agent(
        algorithm=binding.method_id,
        checkpoint=binding.checkpoint_path,
        checkpoint_manifest=binding.checkpoint_manifest,
        task_id=binding.task_id,
        deterministic=True,
        policy_seed=method_seed,
        resource_reporting_scope="formal_evaluation_only",
    )


def _default_run_agent(**kwargs: Any) -> Any:
    from chemworld.eval.runner import run_agent

    return run_agent(**kwargs)


@dataclass
class FormalRLAdapter:
    """Task-specific frozen checkpoint exposed to the formal transaction runner."""

    binding: RLCheckpointBinding
    agent_factory: AgentFactory = _default_agent_factory
    run_agent_fn: RunAgent = _default_run_agent
    method_id: str = field(init=False)
    kind: MethodKind = field(default="rl", init=False)

    def __post_init__(self) -> None:
        self.method_id = self.binding.method_id

    def execute(
        self,
        *,
        spec: FormalCellSpec,
        runtime: PrivateCellRuntime,
        trajectory_path: Path,
    ) -> None:
        """Execute one issued cell without repair, closeout, or training leakage."""

        if spec.method.kind != "rl" or spec.method.method_id != self.binding.method_id:
            raise FormalRLContractError("issued method does not match RL adapter")
        if spec.task_id != self.binding.task_id:
            raise FormalRLContractError("issued task does not match RL checkpoint")
        if spec.method.checkpoint_sha256 != self.binding.checkpoint_sha256:
            raise FormalRLContractError("issued cell does not bind the RL checkpoint")
        if spec.spectrum_condition != "masked":
            raise FormalRLContractError("formal PPO/SAC adapters only accept masked spectra")
        agent = self.agent_factory(self.binding, runtime.method_seed)
        task = get_task(spec.task_id)
        self.run_agent_fn(
            env_id=task.env_id,
            agent=agent,
            world_split=task.world_split,
            budget=task.budget,
            objective=task.objective,
            seed=runtime.world_seed,
            task_id=task.task_id,
            output_path=trajectory_path,
            budget_override=spec.operation_limit,
            episode_mode_override="campaign",
            evaluation_policy="vnext_risk_cost",
            world_interventions=runtime.world_interventions,
        )
        records = [
            json.loads(line)
            for line in trajectory_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        if not records or not all(isinstance(record, dict) for record in records):
            raise FormalRLContractError("RL adapter produced no valid trajectory records")
        for record in records:
            record.update(
                {
                    "benchmark_task_id": spec.task_id,
                    "formal_cell_identity_sha256": spec.cell_identity_sha256,
                    "formal_method_id": spec.method.method_id,
                    "formal_pair_id": spec.pair_id,
                    "formal_spectrum_condition": spec.spectrum_condition,
                    "seed": runtime.world_seed,
                }
            )
        records[-1]["formal_resource_evidence"] = {
            "provider_receipts": [],
            "classic_compute_events": [],
            "rl_checkpoint_sha256": self.binding.checkpoint_sha256,
            "training_resource_policy": "referenced_by_preflight_not_copied_into_cell",
        }
        trajectory_path.write_text(
            "".join(
                json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"
                for record in records
            ),
            encoding="utf-8",
        )


class FormalRLAdapterFactory:
    """Select one frozen task checkpoint behind each formal method ID."""

    def __init__(
        self,
        bindings: Sequence[RLCheckpointBinding],
        *,
        agent_factory: AgentFactory = _default_agent_factory,
        run_agent_fn: RunAgent = _default_run_agent,
    ) -> None:
        self._bindings = {(item.method_id, item.task_id): item for item in bindings}
        if len(self._bindings) != len(bindings):
            raise FormalRLContractError("RL adapter bindings contain duplicate method/task")
        self._agent_factory = agent_factory
        self._run_agent_fn = run_agent_fn

    def create(self, spec: FormalCellSpec) -> FormalRLAdapter:
        try:
            binding = self._bindings[(cast(RLMethodId, spec.method.method_id), spec.task_id)]
        except KeyError as exc:
            raise FormalRLContractError(
                f"no frozen RL checkpoint for {spec.method.method_id}/{spec.task_id}"
            ) from exc
        return FormalRLAdapter(
            binding,
            agent_factory=self._agent_factory,
            run_agent_fn=self._run_agent_fn,
        )

    def register(self, registry: FormalAdapterRegistry) -> None:
        methods = sorted({method_id for method_id, _ in self._bindings})
        for method_id in methods:
            registry.register(method_id, "rl", self.create)


def _lock_version(lock_text: str, package: str) -> str | None:
    match = re.search(
        rf'^name = "{re.escape(package)}"\r?\nversion = "([^"]+)"$',
        lock_text,
        flags=re.MULTILINE,
    )
    return match.group(1) if match else None


def audit_formal_rl_contract(
    config: Mapping[str, Any],
    *,
    root: str | Path,
) -> dict[str, Any]:
    """Audit the pre-training formal RL contract without claiming checkpoints."""

    repository = Path(root).resolve()
    formal = _load_object(repository / DEFAULT_FORMAL_PROTOCOL_PATH, "formal protocol")
    interaction = _load_object(repository / DEFAULT_INTERACTION_PATH, "interaction strata")
    preflight = _load_object(repository / DEFAULT_PREFLIGHT_REPORT_PATH, "preflight report")
    resources = _load_object(repository / DEFAULT_RESOURCE_REPORT_PATH, "resource report")
    formal_tasks_raw = formal.get("task_roles", {}).get("formal_core", {})
    formal_tasks = list(formal_tasks_raw) if isinstance(formal_tasks_raw, Mapping) else []
    configured_tasks = config.get("formal_core_tasks")
    methods = config.get("methods")
    training = config.get("training")
    splits = config.get("split_bindings")
    resource_contract = config.get("resource_accounting")
    interaction_methods = interaction.get("methods", {})

    method_ids = list(methods) if isinstance(methods, Mapping) else []
    model_seeds = training.get("model_seeds") if isinstance(training, Mapping) else None
    checks: dict[str, bool] = {
        "schema_version": config.get("schema_version") == FORMAL_RL_CONFIG_VERSION,
        "contract_only_status": config.get("status") == "contract_ready_training_pending",
        "no_formal_results": config.get("formal_results_present") is False,
        "benchmark_claim_denied": config.get("benchmark_claim_allowed") is False,
        "parent_todo_not_completed_by_slice": config.get("parent_task_complete") is False,
        "exact_formal_core_tasks": configured_tasks == formal_tasks,
        "exact_method_ids": method_ids == ["ppo", "sac"],
        "five_unique_model_seeds": (
            isinstance(model_seeds, list)
            and len(model_seeds) == 5
            and len(set(model_seeds)) == 5
            and all(isinstance(seed, int) and not isinstance(seed, bool) for seed in model_seeds)
        ),
        "preflight_controls_ready": preflight.get("controls_ready") is True,
        "resource_controls_ready": resources.get("controls_ready") is True,
        "reference_repositories_unused": config.get("reference_repositories_used") == [],
    }
    formal_splits = formal.get("split_contract", {})
    checks["train_split_exact"] = isinstance(splits, Mapping) and splits.get(
        "train"
    ) == formal_splits.get("train")
    checks["dev_split_exact"] = isinstance(splits, Mapping) and splits.get(
        "dev"
    ) == formal_splits.get("dev")
    checks["bench_and_reference_feedback_forbidden"] = bool(
        isinstance(splits, Mapping)
        and splits.get("reference_search_access") == "forbidden"
        and splits.get("bench_access") == "forbidden_until_method_freeze"
    )
    checks["checkpoint_selection_dev_only"] = bool(
        isinstance(training, Mapping)
        and training.get("checkpoint_selection_allocation") == "dev"
        and training.get("bench_finetuning_allowed") is False
        and training.get("deterministic_dev_evaluation") is True
    )
    checks["training_resources_separate"] = bool(
        isinstance(resource_contract, Mapping)
        and resource_contract.get("checkpoint_training_ledger_required") is True
        and resource_contract.get("copy_training_resources_into_evaluation_cell") is False
        and resource_contract.get("evaluation_training_environment_step_count") == 0
    )

    task_contracts: dict[str, Any] = {}
    for task_id in formal_tasks:
        task_contracts[task_id] = task_contract_bundle(task_id)
    ppo = methods.get("ppo", {}) if isinstance(methods, Mapping) else {}
    sac = methods.get("sac", {}) if isinstance(methods, Mapping) else {}
    ppo_interaction = (
        interaction_methods.get("ppo", {}) if isinstance(interaction_methods, Mapping) else {}
    )
    sac_interaction = (
        interaction_methods.get("sac", {}) if isinstance(interaction_methods, Mapping) else {}
    )
    checks["ppo_native_masked_conditional_contract"] = bool(
        isinstance(ppo, Mapping)
        and ppo.get("operation_distribution") == "public-affordance-masked categorical"
        and ppo.get("parameter_distribution") == "operation-conditional diagonal Gaussian"
        and ppo.get("irrelevant_parameter_log_prob") is False
        and ppo_interaction.get("action_affordance")
        == "native_masked_categorical_with_conditional_parameters"
    )
    checks["sac_latent_comparability_disclosed"] = bool(
        isinstance(sac, Mapping)
        and sac.get("action_adapter_schema_version") == LATENT_ADAPTER_VERSION
        and sac.get("native_hybrid_distribution") is False
        and sac.get("same_public_affordance_decoder_as_ppo") is True
        and isinstance(sac.get("comparability_limitations"), list)
        and bool(sac.get("comparability_limitations"))
        and sac_interaction.get("action_affordance")
        == "continuous_latent_through_public_action_decoder"
    )
    checks["interaction_resource_profiles_match"] = bool(
        ppo_interaction.get("resource_profile") == "rl_evaluation"
        and sac_interaction.get("resource_profile") == "rl_evaluation"
        and ppo_interaction.get("spectrum_conditions") == ["masked"]
        and sac_interaction.get("spectrum_conditions") == ["masked"]
    )
    checkpoints = config.get("checkpoint_state")
    checks["checkpoint_evidence_explicitly_pending"] = bool(
        isinstance(checkpoints, Mapping)
        and checkpoints.get("status") == "pending_training_slice"
        and checkpoints.get("formal_ready_checkpoint_count") == 0
        and checkpoints.get("required_task_method_checkpoint_count") == len(formal_tasks) * 2
    )
    lock_text = (repository / "uv.lock").read_text(encoding="utf-8")
    locked_versions = {
        "stable_baselines3": _lock_version(lock_text, "stable-baselines3"),
        "torch": _lock_version(lock_text, "torch"),
    }
    expected_versions = config.get("runtime_dependencies", {})
    checks["runtime_dependencies_lock_bound"] = bool(
        isinstance(expected_versions, Mapping)
        and expected_versions.get("stable_baselines3", {}).get("version")
        == locked_versions["stable_baselines3"]
        and expected_versions.get("torch", {}).get("version") == locked_versions["torch"]
    )
    failed = sorted(name for name, passed in checks.items() if not passed)
    return {
        "schema_version": FORMAL_RL_REPORT_VERSION,
        "status": "contract_ready_training_pending" if not failed else "contract_failed",
        "controls_ready": not failed,
        "formal_results_present": False,
        "benchmark_claim_allowed": False,
        "parent_task_complete": False,
        "checks": checks,
        "failed_checks": failed,
        "config_sha256": canonical_sha256(config),
        "protocol_bindings": {
            str(DEFAULT_FORMAL_PROTOCOL_PATH).replace("\\", "/"): file_sha256(
                repository / DEFAULT_FORMAL_PROTOCOL_PATH
            ),
            str(DEFAULT_INTERACTION_PATH).replace("\\", "/"): file_sha256(
                repository / DEFAULT_INTERACTION_PATH
            ),
            str(DEFAULT_PREFLIGHT_REPORT_PATH).replace("\\", "/"): file_sha256(
                repository / DEFAULT_PREFLIGHT_REPORT_PATH
            ),
            str(DEFAULT_RESOURCE_REPORT_PATH).replace("\\", "/"): file_sha256(
                repository / DEFAULT_RESOURCE_REPORT_PATH
            ),
        },
        "runtime_dependencies": locked_versions,
        "task_contracts": task_contracts,
        "method_count": len(method_ids),
        "task_count": len(formal_tasks),
        "required_training_run_count": len(formal_tasks)
        * len(method_ids)
        * (len(model_seeds) if isinstance(model_seeds, list) else 0),
        "required_checkpoint_count": len(formal_tasks) * len(method_ids),
        "formal_ready_checkpoint_count": 0,
        "reference_evidence_used_for_method_development": False,
        "bench_evidence_used_for_method_development": False,
        "limitations": [
            (
                "This slice freezes the formal RL contract and executable adapter boundary; "
                "it does not train or select the required task-specific checkpoints."
            ),
            (
                "The prior five-seed PPO flow gate is diagnostic input only and is not "
                "substituted for four-task v0.4 Train/Dev evidence; its older backend-report "
                "binding now fails closed after later mainline evidence updates."
            ),
            (
                "SAC retains a bounded continuous latent carrier; its comparison to native "
                "masked-conditional PPO is system-level and discloses the decoder difference."
            ),
            (
                "No formal Bench run or performance claim is allowed until the later "
                "training/checkpoint slice and method freeze are complete."
            ),
        ],
        "next_gate": (
            "train and Dev-select all preregistered PPO/SAC task-seed runs, then bind eight "
            "frozen checkpoints and their separate training-resource ledgers"
        ),
    }


__all__ = [
    "DEFAULT_CONFIG_PATH",
    "FORMAL_RL_CHECKPOINT_INDEX_VERSION",
    "FORMAL_RL_CONFIG_VERSION",
    "FORMAL_RL_REPORT_VERSION",
    "FormalRLAdapter",
    "FormalRLAdapterFactory",
    "FormalRLContractError",
    "RLCheckpointBinding",
    "audit_formal_rl_contract",
    "canonical_sha256",
    "file_sha256",
    "load_checkpoint_index",
    "load_formal_rl_config",
    "task_contract_bundle",
]
