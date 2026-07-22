from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import gymnasium as gym
import pytest

import chemworld  # noqa: F401
from chemworld.tasks import get_task, list_tasks
from chemworld.world.parameters import WORLD_FAMILY_VERSION
from chemworld.wrappers import valid_operations


def _audit_module() -> ModuleType:
    path = Path("scripts/audit_environment_consistency.py")
    spec = importlib.util.spec_from_file_location("audit_environment_consistency", path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_task_info_exposes_consistency_contract_fields() -> None:
    required = {
        "world_law_id",
        "scenario_id",
        "initial_state_id",
        "runtime_profile_hash",
        "scoring_contract_hash",
        "observation_contract_hash",
        "kernel_maturity",
        "physics_maturity",
        "proxy_allowed",
    }
    world_law_ids: set[str] = set()
    for task in list_tasks():
        env = gym.make("ChemWorld", task_id=task.task_id, seed=task.seeds[0])
        try:
            _obs, info = env.reset(seed=task.seeds[0])
            assert required <= set(info), task.task_id
            provenance = env.unwrapped.evaluator_provenance()
            world_law_ids.add(str(info["world_law_id"]))
            assert info["scenario_id"] == task.scenario_id
            assert info["scoring_contract_hash"]
            assert info["runtime_profile_hash"]
            assert provenance["mechanism_hash"]
            assert info["physics_maturity"] == info["kernel_maturity"]["lowest_level"]
            assert set(valid_operations(env)).issubset(set(info["allowed_operations"]))
        finally:
            env.close()
    assert world_law_ids == {WORLD_FAMILY_VERSION}


def test_environment_audit_exit_policy_blocks_reported_failures() -> None:
    audit = _audit_module()
    aggregate = {
        "hash_coverage_complete": True,
        "verify_failures": 0,
        "spectra_failures": 0,
        "invalid_steps": 0,
        "constitution_failures": 0,
        "ledger_single_source_failures": 0,
        "public_leakage_failures": 0,
    }

    assert audit.audit_passed(aggregate)
    for key in audit.AUDIT_FAILURE_KEYS:
        failed = {**aggregate, key: 1}
        assert not audit.audit_passed(failed), key
    assert not audit.audit_passed({**aggregate, "hash_coverage_complete": False})


def test_audit_smoke_generates_replay_verified_trajectory(tmp_path: Path) -> None:
    audit = _audit_module()
    row = audit.run_smoke_audit(
        task_id="reaction-to-assay",
        seed=0,
        output_dir=tmp_path,
        max_steps=12,
    )
    assert row["verify_status"] == "pass"
    assert row["invalid_count"] == 0
    assert row["constitution_failure_count"] == 0
    assert row["state_check_failures"] == 0
    assert row["public_leakage_failures"] == 0
    assert row["score_recompute_max_error"] <= 1.0e-6
    assert Path(row["trajectory_path"]).exists()
    assert row["mechanism_hash"]
    assert row["task_contract_hash"]
    assert row["score_contract_hash"]
    assert row["profile_hash"]
    assert row["observation_contract_hash"]


def test_purification_slice_no_longer_allows_unrelated_process_ops(
    tmp_path: Path,
) -> None:
    audit = _audit_module()
    row = audit.run_smoke_audit(
        task_id="reaction-to-purification",
        seed=0,
        output_dir=tmp_path,
        max_steps=12,
    )
    assert row["verify_status"] == "pass"
    assert not any(
        warning.startswith("task_policy_warning:reaction_to_purification")
        for warning in row["warnings"]
    )
    allowed = set(get_task("reaction-to-purification").allowed_operations)
    assert not allowed.intersection(
        {
            "seed_crystals",
            "cool_crystallize",
            "filter_crystals",
            "evaporate",
            "distill",
            "collect_fraction",
            "set_flow_rate",
            "run_flow",
            "set_potential",
            "electrolyze",
        }
    )


def test_purification_final_assay_hplc_tracks_selected_product_phase(
    tmp_path: Path,
) -> None:
    audit = _audit_module()
    row = audit.run_smoke_audit(
        task_id="reaction-to-purification",
        seed=0,
        output_dir=tmp_path,
        max_steps=18,
    )
    assert row["verify_status"] == "pass"
    assert row["spectra_metric_consistency"] == "pass"
    assert not any(warning.startswith("semantic_alignment_warning:") for warning in row["warnings"])


def test_spectra_metric_warning_for_high_purity_with_reactant_dominant_hplc() -> None:
    audit = _audit_module()
    raw_signal = {
        "kind": "final_assay_packet",
        "spectra": {
            "hplc": {
                "kind": "hplc_chromatogram",
                "peaks": [
                    {
                        "species_id": "reactant_public",
                        "group": "reactant",
                        "estimated_concentration_mol_L": 0.8,
                    },
                    {
                        "species_id": "target_public",
                        "group": "target",
                        "estimated_concentration_mol_L": 0.1,
                    },
                    {
                        "species_id": "impurity_public",
                        "group": "byproduct",
                        "estimated_concentration_mol_L": 0.1,
                    },
                ],
            }
        },
    }
    status, warnings, details = audit.spectra_metric_consistency(
        task_id="reaction-to-purification",
        observation={"purity": 0.85, "score": 0.4},
        info={"raw_signal": raw_signal},
    )
    assert status == "warning"
    assert "semantic_alignment_warning:high_purity_with_dominant_reactant_peak" in warnings
    assert details["hplc"]["reactant_fraction"] == pytest.approx(0.8)


def test_spectra_metric_fails_on_hidden_species_label_leak() -> None:
    audit = _audit_module()
    status, warnings, details = audit.spectra_metric_consistency(
        task_id="reaction-to-purification",
        observation={"purity": 0.5, "score": 0.2},
        info={
            "raw_signal": {
                "kind": "hplc_chromatogram",
                "peaks": [
                    {
                        "species_id": "A_hidden",
                        "group": "reactant",
                        "estimated_concentration_mol_L": 0.1,
                    }
                ],
            }
        },
    )
    assert status == "fail"
    assert "hidden_species_label_leak" in warnings
    assert details["leaked_species_ids"] == ["A_hidden"]


def test_chinese_docs_and_notebooks_do_not_contain_obvious_mojibake() -> None:
    suspicious = (
        "\ufffd",
        "\u20ac?",
        "锛",
        "锟",
        "鍙",
        "銆",
        "鐨",
        "绋",
        "瀛",
        "褰",
        "鍓",
        "杩",
        "鈹",
        "乼",
        "乻",
    )
    paths = [
        *Path("docs").glob("*.md"),
        *Path("notebooks").glob("*.ipynb"),
        *Path("notebooks/tutorials").glob("*.ipynb"),
        Path("README.md"),
    ]
    offenders: list[str] = []
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if any(token in text for token in suspicious):
            offenders.append(str(path))
    assert offenders == []
