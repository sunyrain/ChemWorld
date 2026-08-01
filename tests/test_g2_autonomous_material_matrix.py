from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from scripts import run_g2_autonomous_material_matrix as matrix

from chemworld.agents.base import HistoryRecord
from chemworld.eval.provenance import canonical_json_sha256, file_sha256


def _source() -> dict[str, Any]:
    return {
        "git_commit": "test-commit",
        "material_source_tree_sha256": "test-tree",
        "protocol_file_sha256": "test-protocol",
    }


def _environment_contract(seed: int) -> dict[str, Any]:
    return {
        "public_contract": {
            "task_contract_hash": "task-hash",
            "runtime_profile_hash": "runtime-hash",
            "scoring_contract_hash": "scoring-hash",
            "observation_contract_hash": "observation-hash",
            "workflow_mode": "autonomous_open_v1",
        },
        "evaluator_identity": {
            "world_id": f"world-{seed}",
            "mechanism_hash": f"mechanism-{seed}",
            "electrochemical_material_family_id": "family",
            "electrochemical_material_family_sha256": "family-sha",
            "electrochemical_material_instance_sha256": f"instance-{seed}",
            "observation_noise_mode": "keyed",
            "observation_noise_namespace": "paired-noise",
        },
        "initial_campaign_resources": {},
    }


def test_protocol_freezes_k6_budget_and_counterbalanced_pair_order() -> None:
    protocol = matrix._load_protocol(matrix.DEFAULT_CONFIG)
    cells = matrix._scheduled_cells(protocol)
    card = matrix._campaign_card(protocol, qualification=False)
    limits = matrix._method_limits(protocol, qualification=False)

    assert len(cells) == 10
    assert [cell["condition_id"] for cell in cells[:4]] == [
        "opaque_codes",
        "anonymous_nominal_properties",
        "anonymous_nominal_properties",
        "opaque_codes",
    ]
    assert [cell["world_seed"] for cell in cells] == [
        0,
        0,
        1,
        1,
        2,
        2,
        3,
        3,
        4,
        4,
    ]
    assert card.operation_attempt_limit == 144
    assert card.vessel_start_limit == 6
    assert card.final_assay_limit == 6
    assert card.nonfinal_instrument_use_limit == 18
    assert card.card_id == "electrochemical-k6-shared-two-charge-envelope-v3"
    assert card.stock_limits == {
        "reagent_mol": pytest.approx(0.48),
        "solvent_L": pytest.approx(0.96),
    }
    assert limits["operation_limit"] == 144
    assert limits["complete_experiment_limit"] == 6
    assert limits["model_call_limit"] == 6
    assert limits["checkpoint_complete_experiments"] == (1, 2, 3, 4, 5, 6)


@pytest.mark.parametrize("experiment_count", [1, 2, 6])
def test_qualification_budget_scales_per_experiment_in_one_cell(
    experiment_count: int,
) -> None:
    protocol = matrix._load_protocol(matrix.DEFAULT_CONFIG)
    card = matrix._campaign_card(
        protocol,
        qualification=True,
        qualification_experiments=experiment_count,
    )
    limits = matrix._method_limits(
        protocol,
        qualification=True,
        qualification_experiments=experiment_count,
    )

    assert card.card_id == (
        f"electrochemical-k{experiment_count}-"
        "shared-stock-envelope-qualification-v2"
    )
    assert card.stock_limits["reagent_mol"] == pytest.approx(
        0.080 * experiment_count
    )
    assert card.stock_limits["solvent_L"] == pytest.approx(
        0.160 * experiment_count
    )
    assert card.operation_attempt_limit == 24 * experiment_count
    assert card.vessel_start_limit == experiment_count
    assert card.final_assay_limit == experiment_count
    assert card.nonfinal_instrument_use_limit == 3 * experiment_count
    assert card.stock_limits == {
        "reagent_mol": pytest.approx(0.08 * experiment_count),
        "solvent_L": pytest.approx(0.16 * experiment_count),
    }
    assert limits == {
        "operation_limit": 24 * experiment_count,
        "complete_experiment_limit": experiment_count,
        "checkpoint_complete_experiments": tuple(
            range(1, experiment_count + 1)
        ),
        "wall_time_limit_s": 3_600.0 * experiment_count,
        "model_call_limit": experiment_count,
        "input_token_limit": (
            matrix.INPUT_TOKEN_LIMIT_PER_OPERATION
            * 24
            * experiment_count
        ),
        "output_token_limit": 200_000 * experiment_count,
        "training_environment_step_limit": 0,
    }


@pytest.mark.parametrize(
    ("condition", "condition_id", "mode"),
    [
        ("opaque", "opaque_codes", "opaque_codes"),
        (
            "nominal",
            "anonymous_nominal_properties",
            "anonymous_nominal_properties",
        ),
    ],
)
def test_qualification_cell_and_default_root_encode_condition_and_k(
    condition: str,
    condition_id: str,
    mode: str,
) -> None:
    protocol = matrix._load_protocol(matrix.DEFAULT_CONFIG)
    cell = matrix._qualification_cell(
        protocol,
        condition=condition,
        experiment_count=2,
        world_seed=3,
    )
    root = matrix._qualification_output_root(
        condition=condition,
        experiment_count=2,
        world_seed=3,
    )

    assert cell["cell_id"] == f"qualification-seed3-{condition}-k2"
    assert cell["world_seed"] == 3
    assert cell["condition_id"] == condition_id
    assert cell["material_information"] == {"mode": mode}
    assert cell["qualification_experiments"] == 2
    assert root.name == (
        "g2-autonomous-electrochemical-seed3-"
        f"{condition}-k2-qualification-mcp-medium-v2"
    )
    assert root != matrix.DEFAULT_QUALIFICATION_ROOT


def test_qualification_cli_selects_nominal_same_cell_k2_without_provider(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_root = tmp_path / "nominal-k2"
    captured: dict[str, Any] = {}

    def run_cell(**kwargs: Any) -> dict[str, Any]:
        captured.update(kwargs)
        return {"run_status": "completed"}

    monkeypatch.setattr(matrix, "_source_manifest", lambda path: _source())
    monkeypatch.setattr(
        matrix,
        "_codex_cli_manifest",
        lambda: {"version": "test-codex"},
    )
    monkeypatch.setattr(matrix, "_run_cell", run_cell)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_g2_autonomous_material_matrix.py",
            "--qualification",
            "--qualification-condition",
            "nominal",
            "--qualification-experiments",
            "2",
            "--qualification-world-seed",
            "3",
            "--output-root",
            str(output_root),
            "--allow-external-provider",
        ],
    )

    assert matrix.main() == 0
    assert captured["cell"]["condition_id"] == (
        "anonymous_nominal_properties"
    )
    assert captured["cell"]["qualification_experiments"] == 2
    assert captured["cell"]["world_seed"] == 3
    assert captured["cell_root"] == (
        output_root.resolve() / "qualification-seed3-nominal-k2"
    )
    assert captured["card"].vessel_start_limit == 2
    assert captured["method_limits"]["complete_experiment_limit"] == 2

    summary = json.loads(
        (output_root / "qualification_summary.json").read_text(
            encoding="utf-8"
        )
    )
    assert summary["qualification_condition"] == "nominal"
    assert summary["condition_id"] == "anonymous_nominal_properties"
    assert summary["qualification_experiments"] == 2
    assert summary["qualification_world_seed"] == 3
    assert summary["cell_run_dir"] == "qualification-seed3-nominal-k2"


def test_qualification_experiment_cli_rejects_values_outside_frozen_counts() -> None:
    with pytest.raises(SystemExit):
        matrix._parser().parse_args(
            ["--qualification", "--qualification-experiments", "3"]
        )


def test_cell_config_exposes_auditor_fields_and_pair_hash_excludes_arm() -> None:
    protocol = matrix._load_protocol(matrix.DEFAULT_CONFIG)
    cells = matrix._scheduled_cells(protocol)
    card = matrix._campaign_card(protocol, qualification=False)
    limits = matrix._method_limits(protocol, qualification=False)
    cli = {"version": "test-codex"}
    configs = [
        matrix._cell_config(
            protocol=protocol,
            source=_source(),
            cli=cli,
            cell=cell,
            card=card,
            method_limits=limits,
            qualification=False,
        )
        for cell in cells[:2]
    ]

    assert configs[0]["world_seed"] == configs[0]["seed"] == 0
    assert configs[0]["arm"] == "opaque_codes"
    assert configs[0]["material_information"] == {"mode": "opaque_codes"}
    assert configs[0]["campaign_resource_card_sha256"] == card.card_sha256
    assert configs[0]["pair_config_sha256"] == configs[1]["pair_config_sha256"]
    for config in configs:
        declared = config["config_sha256"]
        unhashed = dict(config)
        unhashed.pop("config_sha256")
        assert declared == canonical_json_sha256(unhashed)


def test_manifest_cells_are_flat_and_analyzer_addressable(
    tmp_path: Path,
) -> None:
    protocol = matrix._load_protocol(matrix.DEFAULT_CONFIG)
    card = matrix._campaign_card(protocol, qualification=False)
    cells = matrix._scheduled_cells(protocol)[:2]
    results = [
        {
            "run_status": "completed",
            "cell": cell,
            "config_sha256": f"config-{index}",
            "pair_config_sha256": "pair-0",
            "trajectory_sha256": f"trajectory-{index}",
            "campaign_resource_card_sha256": card.card_sha256,
            "campaign_resource_ledger_sha256": f"ledger-{index}",
            "environment_contract": _environment_contract(0),
            "behavior": {
                "complete_experiment_count": 6,
                "best_final_score": 0.5,
            },
            "provider_session_audit": {
                "passed": True,
                "receipt_count": 6,
            },
        }
        for index, cell in enumerate(cells)
    ]
    path = tmp_path / "matrix_manifest.json"

    manifest = matrix._write_matrix_manifest(
        path,
        protocol=protocol,
        source={**_source(), "protocol_file_sha256": "protocol"},
        cli={"version": "test-codex"},
        started_at="2026-01-01T00:00:00+00:00",
        cell_results=results,
        status="running",
    )

    first = manifest["cells"][0]
    assert "cell" not in first
    assert first["run_dir"] == "cell-01"
    assert first["world_seed"] == first["seed"] == 0
    assert first["arm"] == "opaque_codes"
    assert first["material_information"] == {"mode": "opaque_codes"}
    assert first["config_path"] == "run_config.json"
    assert first["summary_path"] == "run_summary.json"
    assert first["trajectory_path"] == "trajectory.jsonl"
    assert first["campaign_resource_ledger_path"] == (
        "campaign_resource_ledger.json"
    )
    assert first["exact_replay_path"] == "exact_replay.json"
    assert first["provider_session_audit_passed"] is True
    assert json.loads(path.read_text(encoding="utf-8")) == manifest


def test_dry_run_never_probes_codex_cli(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def forbidden() -> dict[str, Any]:
        raise AssertionError("dry-run must not inspect or invoke Codex")

    def inspect(
        *,
        protocol: Any,
        cell: Any,
        card: Any,
        operation_limit: int,
    ) -> dict[str, Any]:
        del protocol, card, operation_limit
        return _environment_contract(int(cell["world_seed"]))

    monkeypatch.setattr(matrix, "_codex_cli_manifest", forbidden)
    monkeypatch.setattr(matrix, "_inspect_cell_environment", inspect)
    monkeypatch.setattr(matrix, "_source_manifest", lambda path: _source())
    monkeypatch.setattr(
        sys,
        "argv",
        ["run_g2_autonomous_material_matrix.py", "--dry-run"],
    )

    assert matrix.main() == 0
    output = json.loads(capsys.readouterr().out)
    assert output["planned_cells"] == 10
    assert output["passed"] is True


def test_exact_replay_receipt_binds_trajectory_and_resource_hash(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    trajectory = tmp_path / "trajectory.jsonl"
    trajectory.write_text('{"step": 1}\n', encoding="utf-8")
    receipt_path = tmp_path / "exact_replay.json"
    result = SimpleNamespace(
        verified=True,
        to_dict=lambda: {
            "verified": True,
            "checked_steps": 1,
            "max_abs_error": 0.0,
            "mismatches": [],
        },
    )
    monkeypatch.setattr(matrix, "load_jsonl", lambda path: [{"step": 1}])
    monkeypatch.setattr(matrix, "verify_records", lambda records: result)

    receipt = matrix._write_exact_replay_receipt(
        trajectory,
        receipt_path,
        campaign_resource_ledger_sha256="ledger-sha",
    )

    assert receipt["trajectory_sha256"] == file_sha256(trajectory)
    assert receipt["trajectory_record_count"] == 1
    assert receipt["campaign_resource_ledger_sha256"] == "ledger-sha"
    assert json.loads(receipt_path.read_text(encoding="utf-8")) == receipt


def test_experiment_summary_reads_electrolyte_from_set_potential() -> None:
    history = [
        HistoryRecord(
            step=1,
            action={
                "operation": "set_potential",
                "potential_V": 1.0,
                "electrolyte_profile": 2,
            },
            observation={},
            reward=0.0,
            info={"transaction_status": "committed"},
        ),
        HistoryRecord(
            step=2,
            action={"operation": "measure", "instrument": "final_assay"},
            observation={},
            reward=0.5,
            info={
                "transaction_status": "committed",
                "leaderboard_score": 0.5,
            },
            event_type="experiment_end",
        ),
    ]

    rows = matrix._experiment_rows(history)

    assert rows[0]["electrolyte_choices"] == [2]


def test_provider_session_audit_requires_six_fully_qualified_turns() -> None:
    receipts = [
        {
            "session_id": f"session-{index}",
            "status": "completed",
            "return_code": 0,
            "terminal_reason": "experiment_complete",
            "final_payload_valid": True,
            "final_payload_status": "experiment_complete",
            "usage_complete": True,
            "lab_tool_integrity_verified_after_session": True,
        }
        for index in range(6)
    ]
    resources = {
        "provider_usage_pending": False,
        "provider_usage_accounting_complete": True,
        "provider_token_accounting_complete": True,
        "provider_call_accounting_complete": True,
        "model_call_count": 6,
    }

    passed = matrix._provider_session_audit(
        receipts,
        resources,
        target_experiments=6,
    )
    receipts[2]["final_payload_valid"] = False
    failed = matrix._provider_session_audit(
        receipts,
        resources,
        target_experiments=6,
    )

    assert passed["passed"] is True
    assert passed["receipt_count"] == 6
    assert failed["passed"] is False
    assert failed["receipts"][2]["checks"]["final_payload_valid"] is False


def test_resume_rejects_sparse_cell_directories(
    tmp_path: Path,
) -> None:
    protocol = matrix._load_protocol(matrix.DEFAULT_CONFIG)
    source = _source()
    cli = {"version": "test-codex"}
    matrix_manifest = {
        "runner_version": matrix.RUNNER_VERSION,
        "protocol_id": protocol["protocol_id"],
        "world_seeds": list(protocol["task"]["world_seeds"]),
        "started_at": "2026-01-01T00:00:00+00:00",
        "source": source,
        "codex_cli": cli,
        "cells": [],
    }
    (tmp_path / "matrix_manifest.json").write_text(
        json.dumps(matrix_manifest),
        encoding="utf-8",
    )
    (tmp_path / "cell-02").mkdir()

    with pytest.raises(
        RuntimeError,
        match="not an exact frozen-schedule prefix",
    ):
        matrix._load_resume_results(
            tmp_path,
            protocol=protocol,
            source=source,
            cli=cli,
            card=matrix._campaign_card(protocol, qualification=False),
            method_limits=matrix._method_limits(
                protocol,
                qualification=False,
            ),
        )
