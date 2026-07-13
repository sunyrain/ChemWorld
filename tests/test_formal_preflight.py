from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest
import scripts.run_formal_preflight as preflight_script
from scripts.run_formal_preflight import main as preflight_main

from chemworld.eval.formal_matrix import (
    FormalMatrixJob,
    build_formal_matrix_plan,
    run_formal_matrix,
)
from chemworld.eval.formal_preflight import (
    PREFLIGHT_PRIVATE_ASSIGNMENT_VERSION,
    PREFLIGHT_REQUEST_VERSION,
    PreflightOutcome,
    run_formal_preflight,
)
from chemworld.eval.formal_runner import (
    FormalCellSpec,
    PrivateCellRuntime,
    file_sha256,
    load_issued_cell,
    run_formal_cell,
)
from chemworld.eval.method_protocol import (
    METHOD_RESOURCE_LEDGER_VERSION,
    METHOD_RESOURCE_USAGE_VERSION,
)
from chemworld.eval.resource_accounting_v0_4 import (
    CLASSIC_COMPUTE_EVENT_VERSION,
    PROVIDER_RECEIPT_VERSION,
    RL_TRAINING_RESOURCE_VERSION,
    bind_pricing_snapshot,
)

COMMIT = "a" * 40
SHA = "b" * 64
TASK = "partition-discovery"
PAIR = "pair-opaque-000"
RECIPE_METHODS = (
    "random",
    "lhs",
    "greedy_local",
    "structured_gp_ei",
    "structured_gp_pi",
    "structured_gp_ucb",
    "structured_rf_ei",
    "structured_safe_gp_ei",
)
OPERATION_METHODS = ("operation_random", "observation_blind", "rule_based")
RL_METHODS = ("ppo", "sac")
LLM_METHODS = ("live_llm_a", "live_llm_b")
ALL_METHODS = (*RECIPE_METHODS, *OPERATION_METHODS, *RL_METHODS, *LLM_METHODS)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_artifact(root: Path, relative: str, content: bytes) -> dict[str, str]:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return {"path": relative, "sha256": _sha(path)}


def _write_json_artifact(
    root: Path, relative: str, payload: dict[str, Any]
) -> dict[str, str]:
    return _write_artifact(
        root,
        relative,
        (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )


def _pricing() -> dict[str, Any]:
    return bind_pricing_snapshot(
        {
            "provider": "SyntheticProvider",
            "model_id": "synthetic-model",
            "access_date": "2026-07-13",
            "currency": "USD",
            "input_cache_hit_per_million_usd": 0.0,
            "input_cache_miss_per_million_usd": 100.0,
            "output_per_million_usd": 0.0,
        }
    )


def _fixture(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    capability_matrix = {
        method_id: {
            "track": "recipe_level" if method_id in RECIPE_METHODS else "operation_level",
            "resource_profile": (
                "classic_recipe"
                if method_id in RECIPE_METHODS
                else "rl_evaluation"
                if method_id in RL_METHODS
                else "live_llm_evaluation"
                if method_id in LLM_METHODS
                else "operation_baseline"
            ),
            "spectrum_conditions": (
                ["assigned", "masked"] if method_id in LLM_METHODS else ["masked"]
            ),
        }
        for method_id in ALL_METHODS
    }
    controls_payload = {
        "backend_release": {
            "schema_version": "chemworld-backend-release-manifest-0.1",
            "portable_release_ready": True,
            "release_status": "formal_candidate",
            "backend_semantic_sha256": "1" * 64,
            "dependency_lock_sha256": "7" * 64,
        },
        "formal_protocol": {
            "controls_ready": True,
            "formal_results_present": False,
            "protocol_sha256": "2" * 64,
            "public_split_summary": {
                "train": {"minimum_seed": 10000, "maximum_seed": 10099},
                "dev": {"minimum_seed": 11000, "maximum_seed": 11019},
                "reference_search": {"minimum_seed": 12000, "maximum_seed": 12099},
            },
        },
        "interaction_strata": {
            "controls_ready": True,
            "formal_results_present": False,
            "protocol_sha256": "3" * 64,
            "capability_matrix": capability_matrix,
        },
        "statistical_plan": {
            "controls_ready": True,
            "formal_results_present": False,
            "analysis_plan_sha256": "4" * 64,
        },
        "reference_plan": {
            "controls_ready": True,
            "formal_results_present": False,
            "run_plan_sha256": "5" * 64,
            "status": "reference_plan_frozen_evidence_not_generated",
        },
        "method_protocol": {
            "controls_ready": True,
            "formal_results_present": False,
            "formal_method_matrix_ready": False,
        },
        "formal_runner": {"controls_ready": True, "formal_results_present": False},
        "formal_matrix": {"controls_ready": True, "formal_results_present": False},
        "resource_accounting": {
            "controls_ready": True,
            "formal_results_present": False,
        },
    }
    control_artifacts = {
        name: _write_json_artifact(root, f"controls/{name}.json", payload)
        for name, payload in controls_payload.items()
    }
    source_artifact = {
        **_write_artifact(root, "dist/chemworld-test.whl", b"frozen-wheel"),
        "source_commit": COMMIT,
    }
    source_artifact_manifest = _write_json_artifact(
        root,
        "dist/chemworld-test.manifest.json",
        {
            "schema_version": "chemworld-source-artifact-manifest-0.4",
            "source_commit": COMMIT,
            "artifact_sha256": source_artifact["sha256"],
            "clean_build": True,
            "dependency_lock_sha256": "7" * 64,
        },
    )
    evaluator = _write_artifact(root, "artifacts/evaluator.bin", b"frozen-evaluator")

    methods: list[dict[str, Any]] = []
    for method_id in ALL_METHODS:
        artifact = _write_artifact(
            root,
            f"methods/{method_id}.bin",
            f"formal-method:{method_id}".encode(),
        )
        if method_id in RECIPE_METHODS:
            methods.append(
                {
                    "method_id": method_id,
                    "kind": "classic",
                    "track": "recipe_level",
                    "resource_profile": "classic_recipe",
                    "spectrum_conditions": ["masked"],
                    "implementation_status": "formal_ready",
                    "artifact": artifact,
                }
            )
        elif method_id in OPERATION_METHODS:
            methods.append(
                {
                    "method_id": method_id,
                    "kind": "classic",
                    "track": "operation_level",
                    "resource_profile": "operation_baseline",
                    "spectrum_conditions": ["masked"],
                    "implementation_status": "formal_ready",
                    "artifact": artifact,
                }
            )
        elif method_id in RL_METHODS:
            checkpoint = _write_artifact(
                root,
                f"methods/{method_id}.checkpoint",
                f"checkpoint:{method_id}".encode(),
            )
            methods.append(
                {
                    "method_id": method_id,
                    "kind": "rl",
                    "track": "operation_level",
                    "resource_profile": "rl_evaluation",
                    "spectrum_conditions": ["masked"],
                    "implementation_status": "formal_ready",
                    "artifact": artifact,
                    "checkpoint": checkpoint,
                    "training_resources": {
                        "schema_version": RL_TRAINING_RESOURCE_VERSION,
                        "accounting_complete": True,
                        "training_run_id": f"training-{method_id}",
                        "checkpoint_sha256": checkpoint["sha256"],
                        "source_manifest_sha256": "6" * 64,
                        "requested_training_environment_step_count": 100,
                        "training_environment_step_count": 100,
                        "cpu_time_s": 2.0,
                        "gpu_time_s": 1.0,
                        "wall_time_s": 1.5,
                    },
                }
            )
        else:
            prompt = _write_artifact(root, f"methods/{method_id}.prompt", b"prompt")
            model_config = _write_artifact(
                root,
                f"methods/{method_id}.model.json",
                b'{"model":"synthetic-model"}',
            )
            methods.append(
                {
                    "method_id": method_id,
                    "kind": "live_llm",
                    "track": "operation_level",
                    "resource_profile": "live_llm_evaluation",
                    "spectrum_conditions": ["assigned", "masked"],
                    "implementation_status": "formal_ready",
                    "artifact": artifact,
                    "prompt": prompt,
                    "model_config": model_config,
                    "provider_model_id": "synthetic-model",
                    "pricing_snapshot": _pricing(),
                }
            )

    spectrum = {
        method_id: (["assigned", "masked"] if method_id in LLM_METHODS else ["masked"])
        for method_id in ALL_METHODS
    }
    request = {
        "schema_version": PREFLIGHT_REQUEST_VERSION,
        "purpose": "nonformal_smoke",
        "cohort_nonce": "preflight-smoke-cohort-0001",
        "source": {
            "expected_commit": COMMIT,
            "artifact_kind": "wheel",
            "artifact": source_artifact,
            "artifact_manifest": source_artifact_manifest,
        },
        "control_artifacts": control_artifacts,
        "cell_bindings": {
            "protocol_sha256": "2" * 64,
            "backend_semantic_sha256": "1" * 64,
            "evaluator_sha256": evaluator["sha256"],
            "evaluator_artifact": evaluator,
            "interaction_protocol_sha256": "3" * 64,
            "statistics_protocol_sha256": "4" * 64,
            "reference_manifest_sha256": "5" * 64,
        },
        "methods": methods,
        "matrix_contract": {
            "tasks": [TASK],
            "methods": list(ALL_METHODS),
            "pair_ids": [PAIR],
            "spectrum_conditions_by_method": spectrum,
            "checkpoints": [1],
            "complete_experiments_per_cell": 1,
            "operation_limits_by_task": {TASK: 1},
        },
        "orchestration": {
            "cpu_workers": 2,
            "gpu_devices": [
                {"device_id": "test-gpu-0", "max_concurrency": 1, "quota_fraction": 1.0}
            ],
            "api_max_concurrency": 2,
            "api_cell_starts_per_minute": 100,
            "api_provider_requests_per_minute_limit": 200,
            "api_cost_usd_per_cell_limit": 5.0,
            "matrix_monetary_cost_usd_limit": 20.0,
        },
        "infrastructure": {
            "required_free_disk_bytes": 1000,
            "estimated_bytes_per_cell": 50,
            "api_key_env": "TEST_API_KEY",
        },
    }
    private = {
        "schema_version": PREFLIGHT_PRIVATE_ASSIGNMENT_VERSION,
        "split": {
            "namespace_id": "chemworld-v0.5-bench-private-test",
            "bench_access_state": "sealed_unrun",
            "forbidden_public_seeds": [10000, 11000, 12000],
        },
        "pairs": {
            PAIR: {
                "method_seed": 70001,
                "seed_nonce": "private-method-nonce",
                "tasks": {
                    TASK: {
                        "world_seed": 80001,
                        "world_nonce": "private-world-nonce",
                        "world_interventions": [
                            {"axis_id": "partition.test", "severity": 0.5}
                        ],
                    }
                },
            }
        },
    }
    resources = {
        "cpu_count": 8,
        "free_disk_bytes": 1_000_000,
        "gpu_devices": ["test-gpu-0"],
        "api_credential_available": True,
        "api_max_concurrency": 4,
        "api_requests_per_minute": 200,
        "api_monetary_quota_usd": 25.0,
    }
    return request, private, resources


@dataclass
class _SmokeAdapter:
    method_id: str
    kind: str

    def execute(
        self,
        *,
        spec: FormalCellSpec,
        runtime: PrivateCellRuntime,
        trajectory_path: Path,
    ) -> None:
        pricing = _pricing()
        live = spec.method.kind == "live_llm"
        classic_events = []
        if spec.method.method_id.startswith("structured_"):
            classic_events = [
                {
                    "schema_version": CLASSIC_COMPUTE_EVENT_VERSION,
                    "event_id": f"fit-{spec.cell_identity_sha256[:8]}",
                    "cell_identity_sha256": spec.cell_identity_sha256,
                    "event_kind": "fit",
                    "cpu_time_s": 0.01,
                    "wall_time_s": 0.01,
                },
                {
                    "schema_version": CLASSIC_COMPUTE_EVENT_VERSION,
                    "event_id": f"acq-{spec.cell_identity_sha256[:8]}",
                    "cell_identity_sha256": spec.cell_identity_sha256,
                    "event_kind": "acquisition_optimization",
                    "cpu_time_s": 0.01,
                    "wall_time_s": 0.01,
                },
            ]
        receipt = {
            "schema_version": PROVIDER_RECEIPT_VERSION,
            "request_id": f"request-{spec.cell_identity_sha256[:16]}",
            "logical_decision_index": 1,
            "attempt_index": 1,
            "status": "succeeded",
            "provider": "SyntheticProvider",
            "model_id": "synthetic-model",
            "pricing_version_sha256": pricing["pricing_version_sha256"],
            "usage_source": "provider_response",
            "usage_complete": True,
            "billable": True,
            "input_token_count": 100,
            "output_token_count": 20,
            "input_cache_hit_token_count": 0,
            "input_cache_miss_token_count": 100,
            "billed_cost_usd": 0.01,
        }
        record = {
            "step": 1,
            "seed": runtime.world_seed,
            "benchmark_task_id": spec.task_id,
            "formal_cell_identity_sha256": spec.cell_identity_sha256,
            "formal_method_id": spec.method.method_id,
            "formal_pair_id": spec.pair_id,
            "formal_spectrum_condition": spec.spectrum_condition,
            "action": {"operation": "wait", "duration_s": 1.0},
            "observation": {"signal": 0.5},
            "reward": 0.1,
            "method_resources": {
                "schema_version": METHOD_RESOURCE_LEDGER_VERSION,
                "accounting_complete": True,
                "operation_count": 1,
                "complete_experiment_count": 1,
                "decision_wall_time_s": 0.02,
                "update_wall_time_s": 0.02,
                "run_wall_time_s": 0.1,
                "reached_checkpoints": [1],
                "limits": {
                    "operation_limit": 1,
                    "complete_experiment_limit": 1,
                    "checkpoint_complete_experiments": [1],
                },
                "agent_usage": {
                    "schema_version": METHOD_RESOURCE_USAGE_VERSION,
                    "accounting_complete": True,
                    "usage_source": "provider_response" if live else "synthetic-runtime",
                    "model_call_count": 1 if live else 0,
                    "input_token_count": 100 if live else 0,
                    "output_token_count": 20 if live else 0,
                    "training_environment_step_count": 0,
                    "monetary_cost_usd": 0.01 if live else 0.0,
                    "cpu_time_s": 0.05,
                    "gpu_time_s": 0.02 if spec.method.kind == "rl" else 0.0,
                    "model_provenance": (
                        {
                            "provider": "SyntheticProvider",
                            "model_id": "synthetic-model",
                            "model_snapshot_or_access_date": "2026-07-13",
                            "prompt_hash": "f" * 64,
                            "request_parameters": {"temperature": 0.0},
                            "tokenizer_or_provider_usage_source": "provider_response",
                        }
                        if live
                        else {}
                    ),
                },
            },
            "formal_resource_evidence": {
                "classic_compute_events": classic_events,
                "pricing_snapshot": pricing if live else None,
                "provider_receipts": [receipt] if live else [],
            },
        }
        trajectory_path.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")


def _replay(
    spec: FormalCellSpec,
    runtime: PrivateCellRuntime,
    records: list[dict[str, Any]],
    trajectory_path: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    del spec, runtime, records
    return (
        {
            "result_schema_version": "synthetic-preflight-smoke",
            "verified": True,
            "trajectory_sha256": file_sha256(trajectory_path),
            "verification": {"verified": True},
            "score": 0.5,
        },
        {"verified": True, "engine": "synthetic-preflight-replay"},
    )


@dataclass(frozen=True)
class _SmokeExecutor:
    manifest: dict[str, Any]
    runtimes: dict[str, dict[str, Any]]
    output_root: str

    def __call__(self, job: FormalMatrixJob) -> dict[str, Any]:
        issued = load_issued_cell(self.manifest, cell_identity_sha256=job.cell_identity_sha256)
        runtime = PrivateCellRuntime.from_payload(self.runtimes[job.cell_identity_sha256])
        run_formal_cell(
            issued_cell=issued,
            runtime=runtime,
            adapter=_SmokeAdapter(issued.spec.method.method_id, issued.spec.method.kind),
            output_root=self.output_root,
            replay_evaluator=_replay,
        )
        return {"worker_pid": 1}


def test_preflight_issues_full_method_two_track_smoke_and_all_cells_replay(tmp_path) -> None:
    request, private, resources = _fixture(tmp_path)
    outcome = run_formal_preflight(
        request,
        private,
        repository_root=tmp_path,
        source_probe={"commit": COMMIT, "clean": True},
        resource_probe=resources,
    )
    assert outcome.passed, outcome.report["blockers"]
    assert outcome.run_manifest is not None and outcome.private_runtimes is not None
    assert outcome.report["issued_cell_count"] == 17
    assert len(outcome.private_runtimes) == 17
    public = json.dumps({"report": outcome.report, "manifest": outcome.run_manifest})
    assert "70001" not in public and "80001" not in public
    assert "private-method-nonce" not in public and "private-world-nonce" not in public
    assert outcome.report["force_override_available"] is False
    second_issuance = run_formal_preflight(
        request,
        private,
        repository_root=tmp_path,
        source_probe={"commit": COMMIT, "clean": True},
        resource_probe=resources,
    )
    assert second_issuance.passed is True
    assert second_issuance.report["run_id"] != outcome.report["run_id"]

    plan = build_formal_matrix_plan(outcome.run_manifest)
    matrix_root = tmp_path / "matrix"
    matrix = run_formal_matrix(
        plan=plan,
        executor=_SmokeExecutor(
            outcome.run_manifest,
            outcome.private_runtimes,
            str(matrix_root),
        ),
        output_root=matrix_root,
        mode="diagnostic_serial",
    )
    assert matrix.report["status"] == "complete_aggregation_ready"
    assert matrix.report["audit"]["replay_verified_success_count"] == 17
    assert matrix.report["audit"]["resource_aggregation"]["accounting_complete"] is True


@pytest.mark.parametrize(
    ("mutation", "expected_blocker"),
    [
        ("dirty_source", "clean_source"),
        ("method_pending", "method:random:implementation_not_formal_ready"),
        ("seed_denylist", "private_assignment_invalid_or_not_disjoint"),
        ("api_missing", "infrastructure"),
        ("artifact_hash", "control_formal_protocol"),
        ("source_artifact_commit", "source_artifact_commit"),
        ("public_seed_range", "private_assignment_invalid_or_not_disjoint"),
        ("disk_estimate", "infrastructure"),
        ("provider_rate", "infrastructure"),
        ("registration", "method:random:interaction_registration_mismatch"),
    ],
)
def test_preflight_failures_are_specific_and_never_issue(
    tmp_path, mutation: str, expected_blocker: str
) -> None:
    request, private, resources = _fixture(tmp_path)
    source = {"commit": COMMIT, "clean": True}
    if mutation == "dirty_source":
        source["clean"] = False
    elif mutation == "method_pending":
        request["methods"][0]["implementation_status"] = "pending"
    elif mutation == "seed_denylist":
        private["split"]["forbidden_public_seeds"].append(70001)
    elif mutation == "api_missing":
        resources["api_credential_available"] = False
    elif mutation == "artifact_hash":
        request["control_artifacts"]["formal_protocol"]["sha256"] = SHA
    elif mutation == "source_artifact_commit":
        request["source"]["artifact"]["source_commit"] = "c" * 40
    elif mutation == "public_seed_range":
        private["pairs"][PAIR]["method_seed"] = 10050
    elif mutation == "disk_estimate":
        request["infrastructure"]["required_free_disk_bytes"] = 100
    elif mutation == "provider_rate":
        request["orchestration"]["api_provider_requests_per_minute_limit"] = 201
    elif mutation == "registration":
        registration_path = tmp_path / request["control_artifacts"]["interaction_strata"][
            "path"
        ]
        registration = json.loads(registration_path.read_text(encoding="utf-8"))
        registration["capability_matrix"]["random"]["track"] = "operation_level"
        registration_path.write_text(
            json.dumps(registration, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        request["control_artifacts"]["interaction_strata"]["sha256"] = _sha(
            registration_path
        )
    outcome = run_formal_preflight(
        request,
        private,
        repository_root=tmp_path,
        source_probe=source,
        resource_probe=resources,
    )
    assert outcome.passed is False
    assert outcome.run_manifest is None and outcome.private_runtimes is None
    assert expected_blocker in outcome.report["blockers"]
    encoded = json.dumps(outcome.report)
    assert "private-method-nonce" not in encoded and "private-world-nonce" not in encoded


def test_formal_bench_requires_release_method_freeze_and_reference_evidence(tmp_path) -> None:
    request, private, resources = _fixture(tmp_path)
    request["purpose"] = "formal_bench"
    outcome = run_formal_preflight(
        request,
        private,
        repository_root=tmp_path,
        source_probe={"commit": COMMIT, "clean": True},
        resource_probe=resources,
    )
    assert outcome.passed is False
    assert {
        "formal_release_artifact",
        "formal_method_matrix_ready",
        "reference_evidence_ready",
    }.issubset(outcome.report["blockers"])


def test_cli_exposes_no_force_override(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_formal_preflight.py",
            "--request",
            str(tmp_path / "request.json"),
            "--private-assignments",
            str(tmp_path / "private.json"),
            "--repo-root",
            str(tmp_path),
            "--manifest-output",
            str(tmp_path / "manifest.json"),
            "--private-runtime-output-dir",
            str(tmp_path / "runtimes"),
            "--report-output",
            str(tmp_path / "report.json"),
            "--force",
        ],
    )
    with pytest.raises(SystemExit) as exc:
        preflight_main()
    assert exc.value.code == 2
    assert "--force" in capsys.readouterr().err


def test_cli_publishes_private_runtimes_before_manifest_and_refuses_overwrite(
    tmp_path, monkeypatch, capsys
) -> None:
    request_path = tmp_path / "request.json"
    private_path = tmp_path / "private.json"
    request_path.write_text("{}\n", encoding="utf-8")
    private_path.write_text("{}\n", encoding="utf-8")
    manifest_path = tmp_path / "issued" / "manifest.json"
    report_path = tmp_path / "issued" / "report.json"
    runtime_root = tmp_path / "private-runtimes"
    safe_report = {
        "schema_version": "chemworld-formal-preflight-report-0.4",
        "passed": True,
        "status": "issued_nonformal_smoke",
        "raw_private_seeds_reported": False,
    }
    fake = PreflightOutcome(
        report=safe_report,
        run_manifest={"schema_version": "test-issued-manifest", "status": "issued"},
        private_runtimes={
            "f" * 64: {
                "method_seed": 70001,
                "world_seed": 80001,
                "seed_nonce": "private-method-nonce",
                "world_nonce": "private-world-nonce",
                "world_interventions": [],
            }
        },
    )
    monkeypatch.setattr(preflight_script, "run_formal_preflight", lambda *args, **kwargs: fake)
    argv = [
        "run_formal_preflight.py",
        "--request",
        str(request_path),
        "--private-assignments",
        str(private_path),
        "--repo-root",
        str(tmp_path),
        "--manifest-output",
        str(manifest_path),
        "--private-runtime-output-dir",
        str(runtime_root),
        "--report-output",
        str(report_path),
    ]
    monkeypatch.setattr(sys, "argv", argv)
    assert preflight_main() == 0
    assert manifest_path.is_file() and report_path.is_file()
    assert (runtime_root / f"{'f' * 64}.json").is_file()
    output = capsys.readouterr().out
    assert "70001" not in output and "private-method-nonce" not in output

    monkeypatch.setattr(sys, "argv", argv)
    with pytest.raises(SystemExit) as exc:
        preflight_main()
    assert exc.value.code == 2
