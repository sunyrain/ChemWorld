from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
import scripts.build_work_ii_as_d1_production as cli

from chemworld.eval.work_ii_as_d1_production import (
    AS_D1_ARMS,
    AS_D1_CHECKPOINTS,
    AS_D1_EXPERIMENTS_PER_CELL,
    AS_D1_TASK_SPECS,
    AS_D1_WORLD_SEEDS,
    build_as_d1_production_materialization,
    validate_as_d1_child,
)

ROOT = Path(__file__).resolve().parents[1]


def test_real_w2_37_sources_build_exact_provider_blocked_five_seed_schedule(
    tmp_path: Path,
) -> None:
    output = ROOT / "configs/benchmark/test-work-ii-as-d1-production"
    parent, children = build_as_d1_production_materialization(
        ROOT,
        output_directory=output,
    )

    assert parent["status"] == "ready_static_materialization_provider_execution_blocked"
    assert parent["world_seeds"] == list(AS_D1_WORLD_SEEDS)
    assert parent["task_count"] == 2
    assert parent["campaign_child_count"] == 10
    assert parent["participant_cell_count"] == 30
    assert parent["complete_experiment_count"] == 360
    assert parent["provider_call_count"] == 0
    assert parent["provider_execution_authorized"] is False
    assert parent["formal_result"] is False
    assert parent["selection_reads_participant_outcomes"] is False
    assert len(children) == 10

    observed = {(row["task_id"], row["world_seed"]) for row in parent["schedule"]}
    assert observed == {
        (task_id, seed)
        for task_id in AS_D1_TASK_SPECS
        for seed in AS_D1_WORLD_SEEDS
    }
    for relative, child in children.items():
        task_id = child["task_id"]
        seed = child["world_seed"]
        source_path = str(AS_D1_TASK_SPECS[task_id]["source"])
        source = json.loads((ROOT / source_path).read_text(encoding="utf-8"))
        metadata = child["as_d1_production"]
        assert set(child["prior_arms"]) == AS_D1_ARMS
        assert child["campaign"]["complete_experiments"] == AS_D1_EXPERIMENTS_PER_CELL
        assert child["campaign"]["checkpoint_complete_experiments"] == AS_D1_CHECKPOINTS
        assert child["qualification"]["execution_authorized"] is False
        assert child["formal_result"] is False
        assert metadata["provider_call_count"] == 0
        assert metadata["provider_execution_authorized"] is False
        assert metadata["world_seed"] == seed
        assert child["pilot_id"].endswith(f"--seed{seed}")
        assert child["observation_noise_namespace"] == child["pilot_id"]
        assert validate_as_d1_child(
            child,
            source,
            task_id=task_id,
            candidate_id=str(AS_D1_TASK_SPECS[task_id]["candidate_id"]),
            source_path=source_path,
            child_path=relative,
            seed=seed,
        ) == []


@pytest.mark.parametrize(
    ("defect", "message"),
    [
        ("provider_calls", "provider-free five-world pass"),
        ("world_failed", "complete five-world pass"),
        ("candidate_task", "complete five-world pass"),
    ],
)
def test_materializer_fails_closed_on_w2_37_package_drift(
    tmp_path: Path,
    defect: str,
    message: str,
) -> None:
    package = json.loads(
        (ROOT / "configs/benchmark/work_ii_as_paired_law_q2_package_v0.1.json").read_text(
            encoding="utf-8"
        )
    )
    if defect == "provider_calls":
        package["provider_call_count"] = 1
    elif defect == "world_failed":
        package["candidate_laws"]["partition_power_response"]["world_evidence"][4][
            "passed"
        ] = False
    else:
        package["candidate_laws"]["partition_power_response"]["task_id"] = (
            "reaction-to-crystallization"
        )
    package_path = ROOT / f".pytest-{tmp_path.name}-as-d1-package.json"
    try:
        package_path.write_text(json.dumps(package), encoding="utf-8")
        with pytest.raises(ValueError, match=message):
            build_as_d1_production_materialization(
                ROOT,
                output_directory=ROOT / "configs/benchmark/test-work-ii-as-d1-production",
                package_path=package_path,
            )
    finally:
        package_path.unlink(missing_ok=True)


def test_child_validator_rejects_scientific_or_authorization_drift() -> None:
    parent, children = build_as_d1_production_materialization(
        ROOT,
        output_directory=ROOT / "configs/benchmark/test-work-ii-as-d1-production",
    )
    row = parent["schedule"][0]
    relative = row["campaign_child_config"]
    child = children[relative]
    task_id = child["task_id"]
    source_path = str(AS_D1_TASK_SPECS[task_id]["source"])
    source = json.loads((ROOT / source_path).read_text(encoding="utf-8"))

    drifts = []
    changed = deepcopy(child)
    changed["campaign"]["complete_experiments"] = 11
    drifts.append(changed)
    changed = deepcopy(child)
    changed["qualification"]["execution_authorized"] = True
    drifts.append(changed)
    changed = deepcopy(child)
    changed["belief_checkpoint"]["held_out_queries"] = []
    drifts.append(changed)
    for changed in drifts:
        assert validate_as_d1_child(
            changed,
            source,
            task_id=task_id,
            candidate_id=str(AS_D1_TASK_SPECS[task_id]["candidate_id"]),
            source_path=source_path,
            child_path=relative,
            seed=child["world_seed"],
        ) == ["A-S D1 child differs from its locked source"]


def test_materializer_rejects_stale_extra_child(tmp_path: Path) -> None:
    output = ROOT / "configs/benchmark/test-work-ii-as-d1-production-stale"
    try:
        cli.materialize(output, check=False)
        (output / "stale.json").write_text("{}", encoding="utf-8")
        with pytest.raises(RuntimeError, match="unexpected JSON files"):
            cli.materialize(output, check=True)
    finally:
        if output.exists():
            for path in output.iterdir():
                path.unlink()
            output.rmdir()


def test_cli_materializes_then_checks_without_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    output = ROOT / "configs/benchmark/test-work-ii-as-d1-production-cli"
    monkeypatch.setattr(cli, "ROOT", ROOT)
    try:
        result = cli.materialize(output, check=False)
        assert result["campaign_child_count"] == 10
        assert result["provider_call_count"] == 0
        assert result["provider_execution_authorized"] is False
        assert cli.materialize(output, check=True)["check"] is True
        assert len(list(output.glob("*.json"))) == 11
    finally:
        if output.exists():
            for path in output.iterdir():
                path.unlink()
            output.rmdir()
