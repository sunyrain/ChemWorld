from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from scripts import run_g2_autonomous_material_matrix as base
from scripts import run_g2_trajectory_replication as replication
from scripts import run_g2_trajectory_replication_qualification as qualification


def _source() -> dict[str, Any]:
    return {
        "git_commit": "test-commit",
        "worktree_dirty": False,
        "material_source_tree_sha256": "test-tree",
        "protocol_file_sha256": "test-protocol",
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def test_qualification_cell_is_an_exact_frozen_schedule_selection() -> None:
    protocol = replication._load_protocol(replication.DEFAULT_CONFIG)
    cell = qualification._qualification_cell(
        protocol,
        pair_order=1,
        condition="nominal",
    )

    assert cell["world_seed"] == 1
    assert cell["trajectory_replicate_id"] == "r01"
    assert cell["agent_seed"] == 120101
    assert cell["condition_id"] == "anonymous_nominal_properties"
    assert cell["material_information"] == {"mode": "anonymous_nominal_properties"}
    assert cell["qualification_pair_order"] == 1
    assert cell["qualification_condition"] == "nominal"


def test_confirmatory_qualification_uses_a_world_outside_the_formal_sample() -> None:
    config = Path("configs/benchmark/g2_endpoint_lifecycle_confirmatory_v0.6.json")
    protocol = replication._load_protocol(config.resolve())
    cell = qualification._qualification_cell(
        protocol,
        pair_order=1,
        condition="nominal",
        world_seed=99,
    )

    assert cell["world_seed"] == 99
    assert cell["agent_seed"] == 900099
    assert 99 not in protocol["task"]["world_seeds"]
    with pytest.raises(ValueError, match="outside"):
        qualification._qualification_cell(
            protocol,
            pair_order=1,
            condition="nominal",
            world_seed=protocol["task"]["world_seeds"][0],
        )


@pytest.mark.parametrize(
    ("experiments", "operations", "nonfinal", "input_tokens"),
    [
        (1, 24, 3, 12_000_000),
        (2, 48, 6, 24_000_000),
    ],
)
def test_k1_k2_qualification_resources_scale_without_changing_semantics(
    experiments: int,
    operations: int,
    nonfinal: int,
    input_tokens: int,
) -> None:
    protocol = replication._load_protocol(replication.DEFAULT_CONFIG)
    card = base._campaign_card(
        protocol,
        qualification=True,
        qualification_experiments=experiments,
    ).to_dict()
    limits = base._method_limits(
        protocol,
        qualification=True,
        qualification_experiments=experiments,
    )

    assert card["hard_limits"] == {
        "operation_attempts": operations,
        "vessel_starts": experiments,
        "final_assays": experiments,
        "nonfinal_instrument_uses": nonfinal,
        "stocks": {
            "reagent_mol": pytest.approx(0.08 * experiments),
            "solvent_L": pytest.approx(0.16 * experiments),
        },
        "per_instrument": {},
    }
    assert limits == {
        "operation_limit": operations,
        "complete_experiment_limit": experiments,
        "checkpoint_complete_experiments": tuple(range(1, experiments + 1)),
        "wall_time_limit_s": 3_600.0 * experiments,
        "model_call_limit": experiments,
        "input_token_limit": input_tokens,
        "output_token_limit": 200_000 * experiments,
        "training_environment_step_limit": 0,
    }


def _patch_qualification_runtime(
    monkeypatch: pytest.MonkeyPatch,
    run_cell: Any,
) -> None:
    monkeypatch.setattr(qualification, "_source_manifest", lambda path: _source())
    monkeypatch.setattr(base, "_codex_cli_manifest", lambda: {"version": "test"})
    monkeypatch.setattr(base, "_run_cell", run_cell)
    monkeypatch.setattr(qualification, "_validate_final_state", lambda **_: None)


def test_qualification_retries_only_a_zero_action_provider_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []

    def run_cell(*, cell: dict[str, Any], cell_root: Path, **_: Any) -> None:
        calls.append(cell_root.name)
        _write_json(cell_root / "run_config.json", {})
        if len(calls) == 1:
            _write_json(
                cell_root / "run_summary.json",
                {
                    "run_status": "provider_infrastructure_failure",
                    "accepted_operation_count": 0,
                    "cell": cell,
                },
            )
            raise RuntimeError("synthetic pre-action provider failure")
        _write_json(
            cell_root / "run_summary.json",
            {
                "run_status": "completed",
                "behavior": {"operation_count": 11},
                "cell": cell,
            },
        )

    _patch_qualification_runtime(monkeypatch, run_cell)
    output_root = tmp_path / "qualification-retry"
    assert (
        qualification.main(
            [
                "--allow-external-provider",
                "--output-root",
                str(output_root),
            ]
        )
        == 0
    )

    assert calls == ["attempt-01", "attempt-02"]
    manifest = json.loads((output_root / "qualification_manifest.json").read_text(encoding="utf-8"))
    assert manifest["run_status"] == "completed"
    attempts = manifest["cell_state"]["attempts"]
    assert [item["accepted_operation_count"] for item in attempts] == [0, 11]
    assert attempts[0]["classification"] == ("retryable_pre_action_provider_failure")
    assert attempts[1]["classification"] == "completed"


def test_qualification_preserves_post_action_failure_as_right_censored(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []

    def run_cell(*, cell: dict[str, Any], cell_root: Path, **_: Any) -> None:
        calls.append(cell_root.name)
        _write_json(cell_root / "run_config.json", {})
        _write_json(
            cell_root / "run_summary.json",
            {
                "run_status": "provider_infrastructure_failure",
                "accepted_operation_count": 4,
                "cell": cell,
            },
        )
        raise RuntimeError("synthetic post-action provider failure")

    _patch_qualification_runtime(monkeypatch, run_cell)
    output_root = tmp_path / "qualification-censored"
    assert (
        qualification.main(
            [
                "--allow-external-provider",
                "--output-root",
                str(output_root),
            ]
        )
        == 2
    )

    assert calls == ["attempt-01"]
    manifest = json.loads((output_root / "qualification_manifest.json").read_text(encoding="utf-8"))
    assert manifest["run_status"] == "right_censored"
    assert manifest["cell_state"]["authoritative_attempt_dir"].endswith("attempt-01")


def test_resume_manifest_rejects_a_different_qualification_cell(
    tmp_path: Path,
) -> None:
    protocol = replication._load_protocol(replication.DEFAULT_CONFIG)
    nominal = qualification._qualification_cell(
        protocol,
        pair_order=1,
        condition="nominal",
    )
    opaque = qualification._qualification_cell(
        protocol,
        pair_order=1,
        condition="opaque",
    )
    card = base._campaign_card(
        protocol,
        qualification=True,
        qualification_experiments=1,
    )
    manifest = qualification._manifest_payload(
        protocol=protocol,
        source=_source(),
        cli={"version": "test"},
        cell=nominal,
        state={"state": "pending"},
        started_at="2026-08-01T00:00:00+00:00",
        experiments=1,
        card=card,
    )
    path = tmp_path / "qualification_manifest.json"
    _write_json(path, manifest)

    with pytest.raises(RuntimeError, match="cell"):
        qualification._validate_resume_manifest(
            path,
            protocol=protocol,
            source=_source(),
            cli={"version": "test"},
            cell=opaque,
            experiments=1,
        )
