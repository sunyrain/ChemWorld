from __future__ import annotations

import json
from pathlib import Path

from scripts.run_static_optimization_s0 import _DeterministicStaticMockClient

from chemworld.eval.provenance import canonical_json_sha256
from chemworld.eval.static_optimization_execution import (
    build_static_optimization_agent,
)
from chemworld.eval.static_optimization_protocol import (
    validate_static_optimization_protocol,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = (
    ROOT
    / "configs"
    / "benchmark"
    / "scientific_optimization_s0_v1.1_nominal_information_freeze_manifest.json"
)
EXPECTED_FREEZE_SHA256 = (
    "17b569a7bfaeac1ea900dcfb434218e4d18524fba525ae300b120705565acc3e"
)
PREFLIGHT_PATH = (
    ROOT
    / "workstreams"
    / "flagship_tasks"
    / "reports"
    / "static-s0-v1.1-nominal-information-preflight.json"
)


def _load(path: str | Path) -> dict[str, object]:
    target = Path(path)
    if not target.is_absolute():
        target = ROOT / target
    return json.loads(target.read_text(encoding="utf-8"))


def _without_information_condition(
    payload: dict[str, object],
) -> dict[str, object]:
    comparable = dict(payload)
    for field in (
        "schema_version",
        "protocol_family_id",
        "protocol_id",
        "condition_id",
        "material_information",
        "method_config_path",
        "method_ids",
        "information_intervention",
        "objective",
    ):
        comparable.pop(field, None)
    return comparable


def test_nominal_information_manifest_is_exactly_frozen() -> None:
    manifest = _load(MANIFEST_PATH)

    assert canonical_json_sha256(manifest) == EXPECTED_FREEZE_SHA256
    assert manifest["world_seeds"] == list(range(10))
    assert len(manifest["participant_tracks"]) == 2
    assert all(
        track["reuse_only"] is True for track in manifest["baseline_tracks"]
    )
    assert (
        manifest["planned_accounting"]["new_participant_provider_calls"] == 420
    )
    assert (
        manifest["planned_accounting"][
            "new_participant_total_physical_experiments"
        ]
        == 760
    )
    assert {
        track["material_information_sha256"]
        for track in manifest["participant_tracks"]
    } == {
        "f3fd3ea3c98f68f97c591e2e23d2fc0c0d07112a5fdd4f3124879e00612bbc63",
        "4432e956ccc0923de2dd226503673e7fea3faa257208b45d226a6e701c1f92e7",
    }
    assert (
        manifest["confirmatory_analysis"]["familywise_interval"]
        == (
            "paired_world_bootstrap_97.5_percent_per_task_"
            "for_two_task_bonferroni_family"
        )
    )


def test_nominal_preflight_binds_frozen_protocol_method_and_dossier_hashes() -> None:
    manifest = _load(MANIFEST_PATH)
    preflight = _load(PREFLIGHT_PATH)

    assert preflight["freeze_sha256"] == EXPECTED_FREEZE_SHA256
    assert preflight["status"] == (
        "passed_ready_for_frozen_external_execution"
    )
    assert all(preflight["checks"].values())
    for track in manifest["participant_tracks"]:
        result = preflight["tracks"][track["track_id"]]
        assert result["protocol_sha256"] == track["protocol_sha256"]
        assert result["method_sha256"] == track["method_sha256"]
        assert result["material_information_sha256"] == (
            track["material_information_sha256"]
        )
        assert result["completed_exploration_experiments"] == 20
        assert result["completed_predictive_physical_experiments"] == 12
        assert result["completed_blind_validation_experiments"] == 6
        assert result["exact_replay_verified"] is True


def test_nominal_protocols_change_only_the_frozen_information_condition() -> None:
    manifest = _load(MANIFEST_PATH)

    for track in manifest["participant_tracks"]:
        nominal = _load(track["protocol_path"])
        opaque = _load(track["paired_opaque_protocol_path"])
        validate_static_optimization_protocol(nominal)
        assert canonical_json_sha256(nominal) == track["protocol_sha256"]
        assert nominal["material_information"] == {
            "mode": "anonymous_nominal_properties"
        }
        assert (
            nominal["observation_noise_namespace"]
            == opaque["observation_noise_namespace"]
        )
        assert _without_information_condition(nominal) == (
            _without_information_condition(opaque)
        )


def test_nominal_methods_retain_model_budget_and_change_scaffold_label_only() -> None:
    manifest = _load(MANIFEST_PATH)

    for track in manifest["participant_tracks"]:
        nominal = _load(track["method_path"])
        opaque = _load(track["paired_opaque_method_path"])
        nominal_method = nominal["methods"][track["method_id"]]
        opaque_method = next(iter(opaque["methods"].values()))
        assert canonical_json_sha256(nominal) == track["method_sha256"]
        assert nominal_method["model_id"] == opaque_method["model_id"]
        assert (
            nominal_method["request_configuration"]
            == opaque_method["request_configuration"]
        )
        nominal_budget = dict(
            nominal_method["static_optimization_prompt_budget_contract"]
        )
        opaque_budget = dict(
            opaque_method["static_optimization_prompt_budget_contract"]
        )
        assert nominal_budget.pop("preflight_status") == (
            "passed_nominal_full_20_round_mock_and_exact_replay_2026_07_29"
        )
        opaque_budget.pop("preflight_status")
        assert (
            nominal_budget
            == opaque_budget
        )
        assert (
            nominal["architecture_candidate"]["material_information"]
            == "anonymous_nominal_properties"
        )


def test_both_nominal_dossiers_reach_public_context_without_hidden_fields() -> None:
    manifest = _load(MANIFEST_PATH)

    for track in manifest["participant_tracks"]:
        protocol = _load(track["protocol_path"])
        methods = _load(track["method_path"])
        agent = build_static_optimization_agent(
            protocol,
            track["task_id"],
            llm_methods=methods,
            method_id=track["method_id"],
            client=_DeterministicStaticMockClient(),
        )
        context = agent.public_context([])
        dossier = context["experiment_interface"]["material_information"]
        serialized = json.dumps(dossier, sort_keys=True).lower()

        assert dossier["presentation"] == (
            "anonymous_material_ids_with_nominal_properties"
        )
        assert "world_id" not in serialized
        assert "residual_generator" not in serialized
        assert "leaderboard_score" not in serialized
        assert agent.manifest()["hidden_world_fields_supplied"] is False
        assert agent.manifest()["material_information_sha256"]
