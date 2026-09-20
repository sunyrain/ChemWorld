from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import gymnasium as gym
import numpy as np
import scripts.run_work_ii_eq_bounded_equilibrium_v2 as canonical
import scripts.run_work_ii_eq_entity_design_gate_v0_2 as eq_e
import scripts.run_work_ii_eq_entity_v0_2 as formal

import chemworld  # noqa: F401
from chemworld.tasks import get_task


def _entity_intervention(world: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": "equilibrium_entity_panel",
        "version": "eq-e-v0.2",
        "base_pka": world["base_pka_nuisance"],
        "profiles": world["profiles"],
    }


def _run_entity_query(world: dict[str, Any], selector: int) -> dict[str, float]:
    kwargs = get_task("equilibrium-characterization").env_kwargs(
        seed=int(world["world_seed"])
    )
    kwargs["world_interventions"] = [_entity_intervention(world)]
    env = gym.make("ChemWorld", **kwargs)
    try:
        env.reset(seed=int(world["world_seed"]))
        observation: dict[str, Any] = {}
        for action in (
            {"operation": "add_solvent", "solvent": selector, "volume_L": 0.024},
            {"operation": "add_reagent", "amount_mol": 0.00192},
            {"operation": "terminate"},
            {"operation": "measure", "instrument": "final_assay"},
        ):
            observation, _, _, _, info = env.step(action)
            assert info["transaction_status"] == "committed"
        return {
            metric: float(np.asarray(observation[metric]).reshape(-1)[0])
            for metric in eq_e.METRICS
        }
    finally:
        env.close()


def test_eq_e_v02_is_provider_sealed_characterization() -> None:
    config = eq_e.load_config()
    validated = eq_e.validate_design(config)

    assert config["prior_locus"] == "E"
    assert config["research_goal"] == "characterization"
    assert config["provider_execution_authorized"] is False
    assert config["provider_calls_authorized"] == 0
    assert config["participant_posttest_stages"] == ["K1", "Q", "K2"]
    assert config["objective"]["operation_recommendation_applicable"] is False
    assert len(validated["schedule"]) == 15
    assert {row["goal"] for row in validated["schedule"]} == {"characterization"}


def test_eq_e_v02_approved_runtime_preserves_the_frozen_design() -> None:
    config = formal.load_config()
    validated = formal.validate_design(config)

    assert config["execution_authorized"] is True
    assert config["provider_execution_authorized"] is True
    assert config["posttest_stages"] == ["K1", "Q", "K2"]
    runtime = config["execution_overlay"]["runtime"]
    assert runtime["source_pre_action_restart_limit"] == 2
    assert runtime["provider_request_retry_limit"] == 2
    assert runtime["posttest_auto_compact_token_limit"] == 120000
    assert runtime["posttest_auto_compact_token_limit_scope"] == "total"
    assert len(validated["schedule"]) == 15
    assert formal.K1 == canonical.K1
    assert formal.Q_PROMPT == canonical.Q_PROMPT
    assert formal.K2 == canonical.K2
    for world in config["worlds"]:
        intervention = world["world_interventions"]
        assert intervention == [
            {
                "kind": "equilibrium_entity_panel",
                "version": "eq-e-v0.2",
                "base_pka": world["base_pka_nuisance"],
                "profiles": world["profiles"],
            }
        ]


def test_eq_e_transport_recovery_is_bounded_and_posttest_only(tmp_path) -> None:
    config = formal.load_config()
    formal.configure_runtime(config)

    agent = object.__new__(formal.EqEntityResearchAgent)
    source_overrides = agent._model_provider_config_overrides()
    source_rendered = " ".join(source_overrides)
    assert "request_max_retries=2" in source_rendered
    assert "stream_max_retries=2" in source_rendered

    workspace = tmp_path / "followup"
    workspace.mkdir()
    schema = workspace / "schema.json"
    schema.write_text("{}", encoding="utf-8")
    command = formal.eq_runtime.shared.build_command(
        formal.PROVIDER,
        schema,
        workspace,
        audit=tmp_path / "numerics.jsonl",
        thread_id="thread-test",
        provider_retries=0,
    )
    rendered = " ".join(command)
    assert "model_auto_compact_token_limit=120000" in rendered
    assert 'model_auto_compact_token_limit_scope="total"' in rendered
    assert "request_max_retries=2" in rendered
    assert "stream_max_retries=2" in rendered


def test_eq_e_v02_uses_canonical_open_k1_q_k2_contract() -> None:
    config = eq_e.load_config()
    protocol = (
        eq_e.ROOT / config["canonical_posttest_protocol"]["path"]
    ).read_text(encoding="utf-8")

    assert "任务交付" in protocol
    assert "operation recommendation is not applicable" in protocol
    assert "以下12个独立新批次" in canonical.Q_PROMPT
    assert "候选机制" not in canonical.K1
    assert "candidate property-vector" not in canonical.K2
    assert config["participant_posttest_stages"] == ["K1", "Q", "K2"]
    assert all(
        supplement not in config["participant_posttest_stages"]
        for supplement in ("EQE", "EQS")
    )


def test_eq_e_v02_fixes_topology_and_varies_entity_property_bundles() -> None:
    config = eq_e.load_config()

    assert config["common_private_topology"] == {
        "mechanism_family": "direct_free_ion_precipitation",
        "species_nodes": ["HA(aq)", "H+(aq)", "A-(aq)", "M+(aq)", "MA(s)"],
        "equation_ids": ["acid_dissociation", "free_ion_solid_equilibrium"],
        "aqueous_intermediate_present": False,
    }
    assert "identical in Opaque, Aligned, and MisIndexed" in config[
        "public_common_background"
    ]["delivery"]
    property_vectors = set()
    for world in config["worlds"]:
        assert set(eq_e.profiles(world)) == {0, 1, 2}
        for profile in world["profiles"]:
            property_vectors.add(
                (
                    profile["pka_shift"],
                    profile["log10_ksp"],
                    profile["cation_fraction"],
                    profile["activity_coefficient_ratio"],
                )
            )
    assert len(property_vectors) == 15


def test_eq_e_v02_priors_are_field_matched_and_only_e_mapping_changes() -> None:
    config = eq_e.load_config()
    permutation = config["prior_contract"]["misindex_permutation"]
    descriptor_levels = {"higher", "intermediate", "lower"}

    assert all(int(target) != int(source) for target, source in permutation.items())
    for descriptor in (
        "acid_ionization_tendency",
        "solid_formation_tendency",
    ):
        for selector in range(3):
            assert {
                next(
                    row[descriptor]
                    for row in world["aligned_descriptors"]
                    if row["selector"] == selector
                )
                for world in config["worlds"]
            } == descriptor_levels
    for world in config["worlds"]:
        assert eq_e.public_prior(config, world, "Opaque") is None
        aligned = eq_e.public_prior(config, world, "Aligned")
        wrong = eq_e.public_prior(config, world, "MisIndexed")
        assert aligned is not None and wrong is not None
        assert aligned.keys() == wrong.keys()
        assert aligned != wrong
        assert [set(row) for row in aligned["entities"]] == [
            set(row) for row in wrong["entities"]
        ]
        aligned_by_selector = {row["selector"]: row for row in aligned["entities"]}
        wrong_by_selector = {row["selector"]: row for row in wrong["entities"]}
        for selector in range(3):
            source = int(permutation[str(selector)])
            assert {
                key: value
                for key, value in wrong_by_selector[selector].items()
                if key != "selector"
            } == {
                key: value
                for key, value in aligned_by_selector[source].items()
                if key != "selector"
            }

        prior_text = json.dumps([aligned, wrong], sort_keys=True).lower()
        for field in config["prior_contract"]["forbidden_public_fields"]:
            assert field.lower() not in prior_text


def test_eq_e_v02_q_is_balanced_entity_concentration_and_scale_matrix() -> None:
    config = eq_e.load_config()
    rows = eq_e.queries(config)

    assert [row["query_id"] for row in rows] == [f"Q{index:02d}" for index in range(1, 13)]
    for concentration in (0.005, 0.08, 0.6):
        primary = [
            row
            for row in rows
            if row["concentration_M"] == concentration and row["volume_L"] == 0.024
        ]
        assert [row["selector"] for row in primary] == [0, 1, 2]
    scaled = [row for row in rows if row["volume_L"] == 0.048]
    assert [row["selector"] for row in scaled] == [0, 1, 2]
    assert {row["concentration_M"] for row in scaled} == {0.08}
    for row in rows:
        assert row["actions"][0]["operation"] == "add_solvent"
        assert row["actions"][0]["solvent"] == row["selector"]
        assert row["actions"][-1] == {
            "operation": "measure",
            "instrument": "final_assay",
        }


def test_eq_e_v02_full_provider_free_gate_passes(tmp_path: Path) -> None:
    report = eq_e.run_gate(tmp_path / "gate")

    assert report["passed"] is True
    assert report["provider_calls"] == 0
    assert report["completed_campaigns"] == 15
    assert report["completed_batches"] == 180
    assert report["exact_replay_batches"] == 180
    assert all(report["checks"].values())


def test_eq_e_v02_entity_panel_is_reachable_in_full_environment() -> None:
    world = eq_e.load_config()["worlds"][0]
    rows = [_run_entity_query(world, selector) for selector in range(3)]

    assert max(row["pH_normalized"] for row in rows) - min(
        row["pH_normalized"] for row in rows
    ) > 0.05
    assert max(row["precipitation_signal"] for row in rows) - min(
        row["precipitation_signal"] for row in rows
    ) > 0.04


def test_eq_e_v02_rejects_mixed_media_inside_one_batch() -> None:
    world = eq_e.load_config()["worlds"][0]
    kwargs = get_task("equilibrium-characterization").env_kwargs(
        seed=int(world["world_seed"])
    )
    kwargs["world_interventions"] = [_entity_intervention(world)]
    env = gym.make("ChemWorld", **kwargs)
    try:
        env.reset(seed=int(world["world_seed"]))
        env.step({"operation": "add_solvent", "solvent": 0, "volume_L": 0.012})
        _obs, _reward, _terminated, _truncated, info = env.step(
            {"operation": "add_solvent", "solvent": 1, "volume_L": 0.012}
        )
        assert info["transaction_status"] != "committed"
        assert info["preconditions"]["equilibrium_entity_single_medium_per_batch"] is False
    finally:
        env.close()
