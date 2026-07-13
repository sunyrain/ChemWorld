from __future__ import annotations

import json
import sys
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest
from scripts.run_formal_cell import main as formal_cell_main

from chemworld.eval.formal_protocol_v0_4 import load_formal_protocol
from chemworld.eval.formal_runner import (
    CellBusyError,
    CellIdentityError,
    CellIntegrityError,
    FormalAdapterRegistry,
    FormalCellSpec,
    FormalMethodBinding,
    IssuedFormalCell,
    PrivateCellRuntime,
    canonical_sha256,
    discard_incomplete_staging,
    file_sha256,
    issue_run_manifest,
    load_issued_cell,
    private_seed_commitment,
    private_world_commitment,
    run_formal_cell,
    statistical_failure_class,
    validate_published_cell,
)
from chemworld.eval.method_protocol import (
    METHOD_RESOURCE_LEDGER_VERSION,
    METHOD_RESOURCE_USAGE_VERSION,
    MethodResourceLimitError,
)
from chemworld.eval.runner import make_agent, run_agent
from chemworld.tasks import get_task

SHA = "a" * 64
RUN_ID = "b" * 64
COMMIT = "c" * 40


def _runtime() -> PrivateCellRuntime:
    return PrivateCellRuntime(
        method_seed=1_234_567,
        world_seed=7_654_321,
        seed_nonce="private-seed-nonce-never-publish",
        world_nonce="private-world-nonce-never-publish",
        world_interventions=({"axis_id": "partition.distribution-coefficient", "severity": 0.81},),
    )


def _method(kind: str = "classic", method_id: str = "random") -> FormalMethodBinding:
    kwargs: dict[str, Any] = {}
    resource_profile = "classic_recipe"
    if kind == "rl":
        kwargs["checkpoint_sha256"] = "d" * 64
        resource_profile = "rl_evaluation"
    elif kind == "live_llm":
        kwargs["prompt_sha256"] = "e" * 64
        kwargs["model_config_sha256"] = "f" * 64
        resource_profile = "live_llm_evaluation"
    return FormalMethodBinding(
        method_id=method_id,
        kind=kind,  # type: ignore[arg-type]
        artifact_sha256=SHA,
        resource_profile=resource_profile,  # type: ignore[arg-type]
        **kwargs,
    )


def _spec(
    *,
    runtime: PrivateCellRuntime | None = None,
    kind: str = "classic",
    method_id: str = "random",
    operation_limit: int = 2,
    complete_experiments: int = 1,
    protocol_sha256: str = SHA,
) -> FormalCellSpec:
    private = _runtime() if runtime is None else runtime
    pair_id = "pair-opaque-000"
    task_id = "partition-discovery"
    return FormalCellSpec(
        run_id=RUN_ID,
        task_id=task_id,
        pair_id=pair_id,
        spectrum_condition="masked",
        private_seed_commitment=private_seed_commitment(
            run_id=RUN_ID,
            pair_id=pair_id,
            method_seed=private.method_seed,
            nonce=private.seed_nonce,
        ),
        world_commitment=private_world_commitment(
            run_id=RUN_ID,
            task_id=task_id,
            pair_id=pair_id,
            world_seed=private.world_seed,
            nonce=private.world_nonce,
            interventions=private.world_interventions,
        ),
        protocol_sha256=protocol_sha256,
        backend_semantic_sha256=SHA,
        evaluator_sha256=SHA,
        interaction_protocol_sha256=SHA,
        statistics_protocol_sha256=SHA,
        reference_manifest_sha256=SHA,
        source_commit=COMMIT,
        complete_experiments=complete_experiments,
        operation_limit=operation_limit,
        method=_method(kind, method_id),
    )


def _issued(spec: FormalCellSpec) -> IssuedFormalCell:
    manifest = issue_run_manifest([spec], metadata={"formal": False, "purpose": "test"})
    return load_issued_cell(manifest, cell_identity_sha256=spec.cell_identity_sha256)


def _staging_attempts(root: Path, spec: FormalCellSpec) -> list[Path]:
    return sorted((root / ".staging").glob(f"{spec.cell_identity_sha256[:16]}-*"))


def _record(
    step: int,
    *,
    operations: int,
    experiments: int,
    spec: FormalCellSpec | None = None,
) -> dict[str, Any]:
    bound = _spec() if spec is None else spec
    return {
        "step": step,
        "benchmark_task_id": bound.task_id,
        "formal_cell_identity_sha256": bound.cell_identity_sha256,
        "formal_method_id": bound.method.method_id,
        "formal_pair_id": bound.pair_id,
        "formal_spectrum_condition": bound.spectrum_condition,
        "seed": _runtime().world_seed,
        "action": {"operation": "wait"},
        "observation": {"signal": 0.5},
        "reward": 0.1,
        "method_resources": {
            "schema_version": METHOD_RESOURCE_LEDGER_VERSION,
            "accounting_complete": True,
            "operation_count": operations,
            "complete_experiment_count": experiments,
            "decision_wall_time_s": 0.01,
            "update_wall_time_s": 0.01,
            "run_wall_time_s": 0.02,
            "reached_checkpoints": [1] if experiments else [],
            "limits": {
                "operation_limit": bound.operation_limit,
                "complete_experiment_limit": bound.complete_experiments,
                "checkpoint_complete_experiments": [1],
            },
            "agent_usage": {
                "schema_version": METHOD_RESOURCE_USAGE_VERSION,
                "accounting_complete": True,
                "usage_source": "synthetic-runtime",
                "model_call_count": 0,
                "input_token_count": 0,
                "output_token_count": 0,
                "training_environment_step_count": 0,
                "monetary_cost_usd": 0.0,
                "cpu_time_s": 0.0,
                "gpu_time_s": 0.0,
                "model_provenance": {},
            },
        },
    }


@dataclass
class _Adapter:
    method_id: str = "random"
    kind: str = "classic"
    behavior: str = "success"
    calls: int = 0

    def execute(
        self,
        *,
        spec: FormalCellSpec,
        runtime: PrivateCellRuntime,
        trajectory_path: Path,
    ) -> None:
        del runtime
        self.calls += 1
        if self.behavior == "timeout":
            raise TimeoutError("provider timed out without secret values")
        if self.behavior == "interrupt":
            raise KeyboardInterrupt
        if self.behavior == "disk":
            raise OSError("simulated disk failure")
        if self.behavior == "resource_limit":
            record = _record(1, operations=1, experiments=0, spec=spec)
            trajectory_path.write_text(
                json.dumps(record, sort_keys=True) + "\n", encoding="utf-8"
            )
            raise MethodResourceLimitError(
                "method resource limit exceeded: wall_time_s"
            )
        if self.behavior == "bad_json":
            trajectory_path.write_text("{bad-json\n", encoding="utf-8")
            return
        if self.behavior == "extra_file":
            (trajectory_path.parent / "undeclared-secret.txt").write_text(
                "must never publish", encoding="utf-8"
            )
        if self.behavior == "manifest_tamper":
            (trajectory_path.parent / "manifest.json").write_text("{}\n", encoding="utf-8")
        if self.behavior == "overrun":
            records = [
                _record(1, operations=1, experiments=0, spec=spec),
                _record(2, operations=2, experiments=1, spec=spec),
                _record(3, operations=3, experiments=1, spec=spec),
            ]
        elif self.behavior == "incomplete_accounting":
            records = [_record(1, operations=1, experiments=1, spec=spec)]
            records[-1]["method_resources"]["accounting_complete"] = False
        elif self.behavior == "wrong_cell":
            records = [_record(1, operations=1, experiments=1, spec=spec)]
            records[-1]["formal_pair_id"] = "another-pair"
        elif self.behavior == "nonfinite":
            records = [_record(1, operations=1, experiments=1, spec=spec)]
            records[-1]["reward"] = float("nan")
        else:
            records = [_record(1, operations=1, experiments=1, spec=spec)]
        trajectory_path.write_text(
            "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
            encoding="utf-8",
        )


@dataclass
class _BlockingAdapter(_Adapter):
    started: threading.Event | None = None
    release: threading.Event | None = None

    def execute(
        self,
        *,
        spec: FormalCellSpec,
        runtime: PrivateCellRuntime,
        trajectory_path: Path,
    ) -> None:
        assert self.started is not None and self.release is not None
        self.started.set()
        assert self.release.wait(timeout=5.0)
        super().execute(spec=spec, runtime=runtime, trajectory_path=trajectory_path)


@dataclass
class _RealReplayAdapter:
    method_id: str = "scripted_chemistry"
    kind: str = "classic"

    def execute(
        self,
        *,
        spec: FormalCellSpec,
        runtime: PrivateCellRuntime,
        trajectory_path: Path,
    ) -> None:
        task = get_task(spec.task_id)
        run_agent(
            env_id=task.env_id,
            agent=make_agent(self.method_id),
            world_split=task.world_split,
            budget=task.budget,
            objective=task.objective,
            seed=runtime.world_seed,
            task_id=task.task_id,
            output_path=trajectory_path,
            budget_override=spec.operation_limit,
            world_interventions=runtime.world_interventions,
        )
        records = [
            json.loads(line)
            for line in trajectory_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        for record in records:
            record.update(
                {
                    "formal_cell_identity_sha256": spec.cell_identity_sha256,
                    "formal_method_id": spec.method.method_id,
                    "formal_pair_id": spec.pair_id,
                    "formal_spectrum_condition": spec.spectrum_condition,
                }
            )
        trajectory_path.write_text(
            "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
            encoding="utf-8",
        )


def _replay(
    spec: FormalCellSpec,
    runtime: PrivateCellRuntime,
    records: list[dict[str, Any]],
    trajectory_path: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    del spec, runtime, records
    return (
        {
            "result_schema_version": "synthetic-test-result",
            "verified": True,
            "trajectory_sha256": file_sha256(trajectory_path),
            "verification": {"verified": True},
            "score": 0.5,
        },
        {"verified": True, "engine": "independent-test-replay"},
    )


def _failed_replay(
    spec: FormalCellSpec,
    runtime: PrivateCellRuntime,
    records: list[dict[str, Any]],
    trajectory_path: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    del spec, runtime, records, trajectory_path
    return {"verified": False}, {"verified": False}


def _leaking_replay(
    spec: FormalCellSpec,
    runtime: PrivateCellRuntime,
    records: list[dict[str, Any]],
    trajectory_path: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    result, replay = _replay(spec, runtime, records, trajectory_path)
    result["method_seed"] = runtime.method_seed
    return result, replay


def test_manifest_issues_exact_identity_and_rejects_tampering() -> None:
    spec = _spec()
    manifest = issue_run_manifest([spec])
    issued = load_issued_cell(manifest, cell_identity_sha256=spec.cell_identity_sha256)
    assert issued.spec == spec
    assert issued.run_manifest_sha256 == manifest["run_manifest_sha256"]
    assert (
        canonical_sha256(
            {key: value for key, value in manifest.items() if key != "run_manifest_sha256"}
        )
        == manifest["run_manifest_sha256"]
    )

    tampered = json.loads(json.dumps(manifest))
    tampered["cells"][0]["operation_limit"] += 1
    with pytest.raises(CellIdentityError, match="manifest digest mismatch"):
        load_issued_cell(tampered, cell_identity_sha256=spec.cell_identity_sha256)


def test_method_resource_profile_is_identity_bound_and_kind_checked() -> None:
    with pytest.raises(CellIdentityError, match="resource profile"):
        FormalMethodBinding(
            method_id="ppo",
            kind="rl",
            artifact_sha256=SHA,
            resource_profile="classic_recipe",
            checkpoint_sha256="d" * 64,
        )
    manifest = issue_run_manifest([_spec()])
    manifest["cells"][0]["method"]["resource_profile"] = "operation_baseline"
    with pytest.raises(CellIdentityError, match="manifest digest mismatch"):
        load_issued_cell(
            manifest,
            cell_identity_sha256=manifest["cells"][0]["cell_identity_sha256"],
        )


def test_cli_validate_only_resolves_issued_identity_without_private_runtime(
    tmp_path, monkeypatch, capsys
) -> None:
    spec = _spec()
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(issue_run_manifest([spec]), sort_keys=True), encoding="utf-8"
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_formal_cell.py",
            "--manifest",
            str(manifest_path),
            "--cell-id",
            spec.cell_identity_sha256,
            "--output-dir",
            str(tmp_path / "output"),
            "--validate-only",
        ],
    )
    assert formal_cell_main() == 0
    output = capsys.readouterr().out
    assert spec.cell_identity_sha256 in output
    assert _runtime().seed_nonce not in output


def test_private_runtime_values_must_match_public_commitments() -> None:
    spec = _spec()
    wrong_runtime = PrivateCellRuntime(
        method_seed=_runtime().method_seed + 1,
        world_seed=_runtime().world_seed,
        seed_nonce=_runtime().seed_nonce,
        world_nonce=_runtime().world_nonce,
        world_interventions=_runtime().world_interventions,
    )
    with pytest.raises(CellIdentityError, match="method seed"):
        run_formal_cell(
            issued_cell=_issued(spec),
            runtime=wrong_runtime,
            adapter=_Adapter(),
            output_root=Path.cwd(),
            replay_evaluator=_replay,
        )


@pytest.mark.parametrize(
    ("kind", "method_id"),
    [("classic", "random"), ("rl", "ppo"), ("live_llm", "live_llm_a")],
)
def test_adapter_registry_supports_all_three_formal_method_kinds(kind: str, method_id: str) -> None:
    spec = _spec(kind=kind, method_id=method_id)
    registry = FormalAdapterRegistry()
    registry.register(
        method_id,
        kind,  # type: ignore[arg-type]
        lambda _spec: _Adapter(method_id=method_id, kind=kind),
    )
    adapter = registry.create(spec)
    assert (adapter.method_id, adapter.kind) == (method_id, kind)


def test_success_is_published_atomically_and_repeat_is_idempotent(tmp_path) -> None:
    runtime = _runtime()
    spec = _spec(runtime=runtime)
    issued = _issued(spec)
    adapter = _Adapter()

    first = run_formal_cell(
        issued_cell=issued,
        runtime=runtime,
        adapter=adapter,
        output_root=tmp_path,
        replay_evaluator=_replay,
    )
    second = run_formal_cell(
        issued_cell=issued,
        runtime=runtime,
        adapter=adapter,
        output_root=tmp_path,
        replay_evaluator=_replay,
    )

    assert first.status == "succeeded" and not first.cached
    assert second.status == "succeeded" and second.cached
    assert first.cell_identity_sha256 == second.cell_identity_sha256
    assert adapter.calls == 1
    assert {item.name for item in first.cell_dir.iterdir()} == {
        "manifest.json",
        "trajectory.jsonl",
        "result.json",
        "failure.json",
        "replay.json",
        "resources.json",
        "artifact-index.json",
        "completion.json",
    }
    completion = json.loads((first.cell_dir / "completion.json").read_text(encoding="utf-8"))
    assert completion["completion_marker_written_last"] is True
    resources = json.loads((first.cell_dir / "resources.json").read_text(encoding="utf-8"))
    assert resources["accounting_complete"] is True
    assert resources["axes"]["operation_count"] == 1
    assert resources["resource_profile"] == "classic_recipe"
    validate_published_cell(first.cell_dir, expected_cell=issued)


def test_duplicate_concurrent_cell_is_rejected_by_os_lock(tmp_path) -> None:
    runtime = _runtime()
    spec = _spec(runtime=runtime)
    issued = _issued(spec)
    started = threading.Event()
    release = threading.Event()
    blocking = _BlockingAdapter(started=started, release=release)
    failures: list[BaseException] = []

    def execute_first() -> None:
        try:
            run_formal_cell(
                issued_cell=issued,
                runtime=runtime,
                adapter=blocking,
                output_root=tmp_path,
                replay_evaluator=_replay,
            )
        except BaseException as exc:  # pragma: no cover - diagnostic capture
            failures.append(exc)

    worker = threading.Thread(target=execute_first)
    worker.start()
    assert started.wait(timeout=5.0)
    try:
        with pytest.raises(CellBusyError, match="already running"):
            run_formal_cell(
                issued_cell=issued,
                runtime=runtime,
                adapter=_Adapter(),
                output_root=tmp_path,
                replay_evaluator=_replay,
            )
    finally:
        release.set()
        worker.join(timeout=10.0)
    assert not worker.is_alive()
    assert not failures


def test_public_control_artifacts_do_not_contain_private_runtime_values(tmp_path) -> None:
    runtime = _runtime()
    outcome = run_formal_cell(
        issued_cell=_issued(_spec(runtime=runtime)),
        runtime=runtime,
        adapter=_Adapter(),
        output_root=tmp_path,
        replay_evaluator=_replay,
    )
    public_controls = "\n".join(
        (outcome.cell_dir / name).read_text(encoding="utf-8")
        for name in (
            "manifest.json",
            "result.json",
            "failure.json",
            "replay.json",
            "resources.json",
            "artifact-index.json",
            "completion.json",
        )
    )
    assert str(runtime.method_seed) not in public_controls
    assert str(runtime.world_seed) not in public_controls
    assert runtime.seed_nonce not in public_controls
    assert runtime.world_nonce not in public_controls


@pytest.mark.parametrize(
    ("behavior", "failure_class"),
    [
        ("bad_json", "runtime_failure"),
        ("overrun", "budget_overrun"),
        ("incomplete_accounting", "incomplete_resource_accounting"),
        ("wrong_cell", "runtime_failure"),
        ("nonfinite", "missing_or_nonfinite_metric"),
    ],
)
def test_trajectory_faults_publish_classified_failures(
    tmp_path, behavior: str, failure_class: str
) -> None:
    runtime = _runtime()
    outcome = run_formal_cell(
        issued_cell=_issued(_spec(runtime=runtime)),
        runtime=runtime,
        adapter=_Adapter(behavior=behavior),
        output_root=tmp_path,
        replay_evaluator=_replay,
    )
    assert outcome.status == "failed"
    assert outcome.failure_class == failure_class
    failure = json.loads((outcome.cell_dir / "failure.json").read_text(encoding="utf-8"))
    assert failure["retained_in_denominator"] is True
    assert failure["automatic_retry"] is False


def test_live_llm_timeout_is_retained_as_provider_failure(tmp_path) -> None:
    runtime = _runtime()
    spec = _spec(runtime=runtime, kind="live_llm", method_id="live_llm_a")
    adapter = _Adapter(method_id="live_llm_a", kind="live_llm", behavior="timeout")
    outcome = run_formal_cell(
        issued_cell=_issued(spec),
        runtime=runtime,
        adapter=adapter,
        output_root=tmp_path,
        replay_evaluator=_replay,
    )
    assert outcome.status == "failed"
    assert outcome.failure_class == "provider_or_model_failure"


def test_method_resource_limit_is_budget_failure_with_partial_accounting(
    tmp_path,
) -> None:
    runtime = _runtime()
    spec = _spec(runtime=runtime)
    private_diagnostics = tmp_path / "private-diagnostics"
    public_output = tmp_path / "public-output"
    outcome = run_formal_cell(
        issued_cell=_issued(spec),
        runtime=runtime,
        adapter=_Adapter(behavior="resource_limit"),
        output_root=public_output,
        private_diagnostic_root=private_diagnostics,
        replay_evaluator=_replay,
    )

    failure = json.loads(
        (outcome.cell_dir / "failure.json").read_text(encoding="utf-8")
    )
    resources = json.loads(
        (outcome.cell_dir / "resources.json").read_text(encoding="utf-8")
    )
    diagnostics = list(private_diagnostics.rglob("*.json"))
    public_text = "\n".join(
        path.read_text(encoding="utf-8") for path in outcome.cell_dir.iterdir()
    )

    assert outcome.status == "failed"
    assert outcome.failure_class == "budget_overrun"
    assert failure["failure_code"] == "method_resource_limit_exceeded"
    assert resources["accounting_complete"] is True
    assert resources["axes"]["operation_count"] == 1
    assert resources["axes"]["complete_experiment_count"] == 0
    assert len(diagnostics) == 1
    raw_message = "method resource limit exceeded: wall_time_s"
    assert raw_message in diagnostics[0].read_text(encoding="utf-8")
    assert raw_message not in public_text


def test_private_diagnostics_cannot_be_written_under_public_output(tmp_path) -> None:
    runtime = _runtime()
    spec = _spec(runtime=runtime)
    with pytest.raises(CellIdentityError, match="outside the public"):
        run_formal_cell(
            issued_cell=_issued(spec),
            runtime=runtime,
            adapter=_Adapter(),
            output_root=tmp_path,
            private_diagnostic_root=tmp_path / "private-diagnostics",
            replay_evaluator=_replay,
        )


def test_live_llm_without_attempt_receipts_fails_resource_accounting(tmp_path) -> None:
    runtime = _runtime()
    spec = _spec(runtime=runtime, kind="live_llm", method_id="live_llm_a")
    outcome = run_formal_cell(
        issued_cell=_issued(spec),
        runtime=runtime,
        adapter=_Adapter(method_id="live_llm_a", kind="live_llm"),
        output_root=tmp_path,
        replay_evaluator=_replay,
    )
    assert outcome.status == "failed"
    assert outcome.failure_class == "incomplete_resource_accounting"
    resources = json.loads((outcome.cell_dir / "resources.json").read_text(encoding="utf-8"))
    assert resources["accounting_complete"] is False
    assert resources["axes"]["monetary_cost_usd"] is None
    assert "provider_receipts_missing" in resources["failure_reasons"]


def test_protocol_failures_map_exhaustively_to_statistical_denominator() -> None:
    expected = {
        "invalid_action": "invalid_action",
        "provider_or_model_failure": "provider_model_failure",
        "runtime_failure": "runtime_failure",
        "budget_overrun": "budget_overrun",
        "missing_or_nonfinite_metric": "runtime_failure",
        "incomplete_resource_accounting": "incomplete_accounting",
        "replay_mismatch": "runtime_failure",
    }
    assert {key: statistical_failure_class(key) for key in expected} == expected


def test_private_runtime_leak_in_result_is_rejected_without_republishing_value(tmp_path) -> None:
    runtime = _runtime()
    outcome = run_formal_cell(
        issued_cell=_issued(_spec(runtime=runtime)),
        runtime=runtime,
        adapter=_Adapter(),
        output_root=tmp_path,
        replay_evaluator=_leaking_replay,
    )
    assert outcome.status == "failed"
    artifacts = "\n".join(
        path.read_text(encoding="utf-8")
        for path in outcome.cell_dir.iterdir()
        if path.suffix == ".json"
    )
    assert str(runtime.method_seed) not in artifacts
    assert "private_runtime_value_in_public_control" in artifacts


def test_replay_mismatch_invalidates_cell_without_synthesizing_success(tmp_path) -> None:
    runtime = _runtime()
    outcome = run_formal_cell(
        issued_cell=_issued(_spec(runtime=runtime)),
        runtime=runtime,
        adapter=_Adapter(),
        output_root=tmp_path,
        replay_evaluator=_failed_replay,
    )
    assert outcome.status == "failed"
    assert outcome.failure_class == "replay_mismatch"
    result = json.loads((outcome.cell_dir / "result.json").read_text(encoding="utf-8"))
    assert result["status"] == "no_verified_result"


def test_default_replay_evaluator_verifies_a_real_environment_trajectory(tmp_path) -> None:
    runtime = PrivateCellRuntime(
        method_seed=13_001,
        world_seed=13_001,
        seed_nonce="real-test-method-seed",
        world_nonce="real-test-world-seed",
        world_interventions=(),
    )
    spec = _spec(
        runtime=runtime,
        method_id="scripted_chemistry",
        operation_limit=10,
        complete_experiments=1,
        protocol_sha256=canonical_sha256(load_formal_protocol()),
    )
    outcome = run_formal_cell(
        issued_cell=_issued(spec),
        runtime=runtime,
        adapter=_RealReplayAdapter(),
        output_root=tmp_path,
    )
    assert outcome.status == "succeeded"
    replay = json.loads((outcome.cell_dir / "replay.json").read_text(encoding="utf-8"))
    assert replay["verified"] is True
    assert replay["engine"] == "chemworld.eval.verify.verify_records"


@pytest.mark.parametrize("behavior", ["interrupt", "disk"])
def test_process_or_disk_interruption_never_publishes_half_a_cell(tmp_path, behavior: str) -> None:
    runtime = _runtime()
    spec = _spec(runtime=runtime)
    error = KeyboardInterrupt if behavior == "interrupt" else OSError
    with pytest.raises(error):
        run_formal_cell(
            issued_cell=_issued(spec),
            runtime=runtime,
            adapter=_Adapter(behavior=behavior),
            output_root=tmp_path,
            replay_evaluator=_replay,
        )
    assert not (tmp_path / "cells" / spec.cell_identity_sha256).exists()
    attempts = _staging_attempts(tmp_path, spec)
    assert len(attempts) == 1
    assert not (attempts[0] / "completion.json").exists()


def test_interrupted_cell_can_retry_same_identity_without_using_partial_output(tmp_path) -> None:
    runtime = _runtime()
    spec = _spec(runtime=runtime)
    issued = _issued(spec)
    with pytest.raises(KeyboardInterrupt):
        run_formal_cell(
            issued_cell=issued,
            runtime=runtime,
            adapter=_Adapter(behavior="interrupt"),
            output_root=tmp_path,
            replay_evaluator=_replay,
        )
    outcome = run_formal_cell(
        issued_cell=issued,
        runtime=runtime,
        adapter=_Adapter(),
        output_root=tmp_path,
        replay_evaluator=_replay,
    )
    assert outcome.status == "succeeded"
    attempts = _staging_attempts(tmp_path, spec)
    assert len(attempts) == 1


def test_digest_tampering_is_rejected_and_never_overwritten(tmp_path) -> None:
    runtime = _runtime()
    spec = _spec(runtime=runtime)
    issued = _issued(spec)
    adapter = _Adapter()
    outcome = run_formal_cell(
        issued_cell=issued,
        runtime=runtime,
        adapter=adapter,
        output_root=tmp_path,
        replay_evaluator=_replay,
    )
    with (outcome.cell_dir / "trajectory.jsonl").open("a", encoding="utf-8") as handle:
        handle.write("{}\n")
    with pytest.raises(CellIntegrityError, match="digest mismatch"):
        run_formal_cell(
            issued_cell=issued,
            runtime=runtime,
            adapter=adapter,
            output_root=tmp_path,
            replay_evaluator=_replay,
        )
    assert adapter.calls == 1


def test_undeclared_staging_file_prevents_publication(tmp_path) -> None:
    runtime = _runtime()
    spec = _spec(runtime=runtime)
    with pytest.raises(OSError, match="undeclared artifacts"):
        run_formal_cell(
            issued_cell=_issued(spec),
            runtime=runtime,
            adapter=_Adapter(behavior="extra_file"),
            output_root=tmp_path,
            replay_evaluator=_replay,
        )
    assert not (tmp_path / "cells" / spec.cell_identity_sha256).exists()


def test_adapter_cannot_modify_runner_owned_manifest(tmp_path) -> None:
    runtime = _runtime()
    spec = _spec(runtime=runtime)
    with pytest.raises(OSError, match="runner-owned"):
        run_formal_cell(
            issued_cell=_issued(spec),
            runtime=runtime,
            adapter=_Adapter(behavior="manifest_tamper"),
            output_root=tmp_path,
            replay_evaluator=_replay,
        )
    assert not (tmp_path / "cells" / spec.cell_identity_sha256).exists()


def test_explicit_staging_cleanup_never_deletes_a_published_cell(tmp_path) -> None:
    runtime = _runtime()
    spec = _spec(runtime=runtime)
    with pytest.raises(KeyboardInterrupt):
        run_formal_cell(
            issued_cell=_issued(spec),
            runtime=runtime,
            adapter=_Adapter(behavior="interrupt"),
            output_root=tmp_path,
            replay_evaluator=_replay,
        )
    assert discard_incomplete_staging(tmp_path, cell_identity_sha256=spec.cell_identity_sha256) == 1
    assert not _staging_attempts(tmp_path, spec)
