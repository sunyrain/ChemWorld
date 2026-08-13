from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import pytest
import scripts.run_work_ii_constitutive_structural_qualification as runner
from scripts.run_work_ii_campaign_pilot import _campaign_card
from scripts.run_work_ii_constitutive_structural_qualification import (
    BASE_CONFIGS,
    DEFAULT_DEVELOPMENT_CRYSTALLIZATION_Q0,
    DEFAULT_DEVELOPMENT_PARTITION_Q0,
    _compile_actions,
    _d1_config,
    _load,
    _validate_q0_inputs,
)

from chemworld.eval.work_ii_c2_admission import C2_MATERIAL_SOURCE_EXCLUSIONS
from chemworld.eval.work_ii_constitutive_structural_qualification import (
    CANDIDATE_IDS,
    COORDINATES_PER_CANDIDATE_WORLD,
    CRYSTALLIZATION_CANDIDATE_ID,
    EXACT_REPLAYS_TOTAL,
    PARTITION_CANDIDATE_ID,
    PARTITION_NOMINAL_PAIR_STRATA,
    PRIMARY_EXECUTIONS_PER_CANDIDATE_WORLD,
    PRIMARY_EXECUTIONS_TOTAL,
    WORLD_SEEDS,
    analyze_candidate_world,
    build_prior_arms,
    build_qualification_plan,
    candidate_specs,
    package_sha256,
    plan_sha256,
    registered_coordinates,
    selected_q2_queries,
    validate_qualification_plan,
)
from chemworld.eval.work_ii_execution_mode import (
    build_execution_envelope,
    prepare_execution_context,
)
from chemworld.eval.work_ii_formal import build_checkpoint_contract


def _audit(candidate_id: str, world_seed: int) -> dict[str, Any]:
    spec = candidate_specs()[candidate_id]
    common: dict[str, Any] = {
        "candidate_id": candidate_id,
        "world_seed": world_seed,
        "registered_law_ids": list(spec["law_ids"]),
        "world_intervention": spec["world_intervention"],
        "baseline_mechanism_hash": "b" * 64,
        "altered_hash_deterministic": True,
        "altered_intervention_hash": "i" * 64,
    }
    if candidate_id == PARTITION_CANDIDATE_ID:
        common.update(
            {
                "altered_mechanism_hash": "b" * 64,
                "mechanism_hash_changed": False,
                "changed_domain_parameter_keys": ["partition_coefficient_exponent"],
                "only_registered_constitutive_parameter_changed": True,
            }
        )
    else:
        common.update(
            {
                "altered_mechanism_hash": "a" * 64,
                "mechanism_hash_changed": True,
                "added_reaction_count": 1,
                "transform_id": "reversible_target_pathway_stress_v1",
            }
        )
    return common


def _metrics(candidate_id: str, coordinate_index: int, altered: bool) -> dict[str, float]:
    spec = candidate_specs()[candidate_id]
    base = 0.40 + 0.0001 * coordinate_index
    return {
        metric: base + 0.20 * altered + 0.01 * metric_index
        for metric_index, metric in enumerate(spec["metric_ids"])
    }


def _rows(candidate_id: str, world_seed: int = 0) -> list[dict[str, Any]]:
    spec = candidate_specs()[candidate_id]
    rows: list[dict[str, Any]] = []
    for coordinate in registered_coordinates(candidate_id):
        for law_id in spec["law_ids"]:
            altered = law_id == spec["altered_law_id"]
            rows.append(
                {
                    **coordinate,
                    "candidate_id": candidate_id,
                    "task_id": spec["task_id"],
                    "world_seed": world_seed,
                    "law_id": law_id,
                    "status": "completed",
                    "safe": True,
                    "metrics": _metrics(candidate_id, int(coordinate["coordinate_index"]), altered),
                    "action_plan_sha256": coordinate["coordinate_sha256"],
                    "observation_coordinate_sha256": coordinate["coordinate_sha256"],
                    "mechanism_hash": (
                        "a" * 64
                        if altered and candidate_id == CRYSTALLIZATION_CANDIDATE_ID
                        else "b" * 64
                    ),
                    "intervention_hash": "i" * 64 if altered else None,
                    "exact_replay": True,
                    "participant_visible_leakage_matches": [],
                    "trajectory": {
                        "path": (
                            f"runs/{candidate_id}/{world_seed}/"
                            f"{coordinate['coordinate_id']}/{law_id}.jsonl"
                        ),
                        "sha256": "t" * 64,
                    },
                }
            )
    return rows


@pytest.mark.parametrize("candidate_id", CANDIDATE_IDS)
def test_frozen_roster_has_exact_paired_law_denominators(candidate_id: str) -> None:
    rows = registered_coordinates(candidate_id)
    assert len(rows) == COORDINATES_PER_CANDIDATE_WORLD == 512
    assert sum(row["phase"] == "q1_coverage" for row in rows) == 384
    assert sum(row["phase"] == "q2_heldout" for row in rows) == 128
    for family in candidate_specs()[candidate_id]["intervention_families"]:
        assert sum(row["intervention_family"] == family for row in rows) == 256
        assert (
            sum(
                row["phase"] == "q1_coverage" and row["intervention_family"] == family
                for row in rows
            )
            == 192
        )
        assert (
            sum(
                row["phase"] == "q2_heldout" and row["intervention_family"] == family
                for row in rows
            )
            == 64
        )
    assert PRIMARY_EXECUTIONS_PER_CANDIDATE_WORLD == 1024
    assert PRIMARY_EXECUTIONS_TOTAL == EXACT_REPLAYS_TOTAL == 10_240


def test_progress_eta_uses_current_candidate_rate(
    monkeypatch: Any, tmp_path: Path
) -> None:
    ticks = iter([100.0, 100.0, 160.0, 220.0, 220.0, 820.0])
    monkeypatch.setattr(runner, "perf_counter", lambda: next(ticks))
    progress_file = tmp_path / "progress.jsonl"
    status_file = tmp_path / "status.json"
    progress = runner.Progress(progress_file, status_file)

    progress.begin_candidate(PARTITION_CANDIDATE_ID)
    progress.update(
        {
            "candidate_id": PARTITION_CANDIDATE_ID,
            "world_seed": 0,
            "coordinate_id": "c000",
            "law_id": "linear_response",
            "status": "completed",
        }
    )
    progress.update(
        {
            "candidate_id": PARTITION_CANDIDATE_ID,
            "world_seed": 0,
            "coordinate_id": "c000",
            "law_id": "power_response",
            "status": "completed",
        }
    )
    progress.begin_candidate(CRYSTALLIZATION_CANDIDATE_ID)
    progress.update(
        {
            "candidate_id": CRYSTALLIZATION_CANDIDATE_ID,
            "world_seed": 0,
            "coordinate_id": "c000",
            "law_id": "baseline",
            "status": "completed",
        }
    )

    payload = json.loads(status_file.read_text(encoding="utf-8"))
    assert payload["stage"] == "provider_free_primary_and_exact_replay"
    assert payload["completed_primary_and_replay_pairs"] == 3
    assert payload["total_primary_and_replay_pairs"] == 10_240
    assert payload["candidate_completed_primary_and_replay_pairs"] == 1
    assert payload["candidate_total_primary_and_replay_pairs"] == 5_120
    assert payload["throughput_pairs_per_minute"] == 0.1
    assert payload["cumulative_throughput_pairs_per_minute"] == 0.25
    assert payload["throughput_scope"] == "current_candidate_and_stage"
    assert payload["eta_basis"] == "current_candidate_and_stage_throughput"
    assert payload["eta_s"] == 6_142_200.0
    assert payload["candidate_elapsed_s"] == 600.0


def test_progress_rejects_update_before_candidate_start(tmp_path: Path) -> None:
    progress = runner.Progress(tmp_path / "progress.jsonl", tmp_path / "status.json")
    with pytest.raises(RuntimeError, match="was not initialized"):
        progress.update(
            {
                "candidate_id": PARTITION_CANDIDATE_ID,
                "world_seed": 0,
                "coordinate_id": "c000",
                "law_id": "linear_response",
                "status": "completed",
            }
        )


def test_generated_a_s_evidence_is_outside_the_protected_source_tree() -> None:
    assert {
        "configs/benchmark/work_ii_as_paired_law_q2_package_v0.1.json",
        "configs/benchmark/work_ii_as_partition_d1_v0.1.json",
        "configs/benchmark/work_ii_as_crystallization_d1_v0.1.json",
    }.issubset(C2_MATERIAL_SOURCE_EXCLUSIONS)


@pytest.mark.parametrize("candidate_id", CANDIDATE_IDS)
def test_q2_selection_is_fixed_balanced_and_outcome_independent(candidate_id: str) -> None:
    first = selected_q2_queries(candidate_id)
    second = selected_q2_queries(candidate_id)
    assert first == second
    assert len(first) == 16
    assert all(row["phase"] == "q2_heldout" for row in first)
    assert {
        family: sum(row["intervention_family"] == family for row in first)
        for family in candidate_specs()[candidate_id]["intervention_families"]
    } == dict.fromkeys(candidate_specs()[candidate_id]["intervention_families"], 8)
    assert all("metrics" not in row and "outcome" not in row for row in first)


@pytest.mark.parametrize("candidate_id", CANDIDATE_IDS)
def test_analysis_accepts_only_complete_paired_actual_laws(candidate_id: str) -> None:
    result = analyze_candidate_world(candidate_id, 0, _rows(candidate_id), _audit(candidate_id, 0))
    assert result["passed"] is True
    assert result["denominators"] == {
        "planned_primary_executions": 1024,
        "attempted_primary_executions": 1024,
        "completed_primary_executions": 1024,
        "physical_failures": 0,
        "platform_failures": 0,
        "unsafe_completed": 0,
        "exact_replays": 1024,
    }
    assert result["q1"]["family_coordinate_counts"]
    assert result["q2"]["query_count"] == 16
    assert result["q2"]["selection_reads_outcomes"] is False
    assert {value["prediction_source"] for value in result["q2"]["candidate_laws"].values()} == {
        "direct_provider_free_execution"
    }
    assert result["q2"]["blind_identified_truth_law"] == "blind_law_b"


def test_partition_law_binding_requires_same_compiled_mechanism_and_exponent_only() -> None:
    rows = _rows(PARTITION_CANDIDATE_ID)
    audit = _audit(PARTITION_CANDIDATE_ID, 0)
    assert (
        analyze_candidate_world(PARTITION_CANDIDATE_ID, 0, rows, audit)["checks"][
            "executable_law_binding"
        ]
        is True
    )

    changed_hash_audit = dict(audit)
    changed_hash_audit.update({"mechanism_hash_changed": True, "altered_mechanism_hash": "a" * 64})
    assert (
        analyze_candidate_world(PARTITION_CANDIDATE_ID, 0, rows, changed_hash_audit)["checks"][
            "executable_law_binding"
        ]
        is False
    )

    changed_row = [dict(row) for row in rows]
    next(row for row in changed_row if row["law_id"] == "power_response")["mechanism_hash"] = (
        "a" * 64
    )
    assert (
        analyze_candidate_world(PARTITION_CANDIDATE_ID, 0, changed_row, audit)["checks"][
            "executable_law_binding"
        ]
        is False
    )

    extra_parameter_audit = dict(audit)
    extra_parameter_audit["changed_domain_parameter_keys"] = [
        "partition_coefficient_exponent",
        "partition_phase_volume_multiplier",
    ]
    assert (
        analyze_candidate_world(PARTITION_CANDIDATE_ID, 0, rows, extra_parameter_audit)["checks"][
            "executable_law_binding"
        ]
        is False
    )

    bad_intervention_rows = [dict(row) for row in rows]
    next(row for row in bad_intervention_rows if row["law_id"] == "power_response")[
        "intervention_hash"
    ] = "wrong"
    assert (
        analyze_candidate_world(PARTITION_CANDIDATE_ID, 0, bad_intervention_rows, audit)["checks"][
            "executable_law_binding"
        ]
        is False
    )

    missing_intervention_audit = dict(audit)
    missing_intervention_audit["altered_intervention_hash"] = None
    assert (
        analyze_candidate_world(PARTITION_CANDIDATE_ID, 0, rows, missing_intervention_audit)[
            "checks"
        ]["executable_law_binding"]
        is False
    )


def test_crystallization_law_binding_requires_changed_topology_and_added_reaction() -> None:
    rows = _rows(CRYSTALLIZATION_CANDIDATE_ID)
    audit = _audit(CRYSTALLIZATION_CANDIDATE_ID, 0)
    assert (
        analyze_candidate_world(CRYSTALLIZATION_CANDIDATE_ID, 0, rows, audit)["checks"][
            "executable_law_binding"
        ]
        is True
    )

    unchanged_audit = dict(audit)
    unchanged_audit.update({"mechanism_hash_changed": False, "altered_mechanism_hash": "b" * 64})
    assert (
        analyze_candidate_world(CRYSTALLIZATION_CANDIDATE_ID, 0, rows, unchanged_audit)["checks"][
            "executable_law_binding"
        ]
        is False
    )

    no_added_reaction_audit = dict(audit)
    no_added_reaction_audit["added_reaction_count"] = 0
    assert (
        analyze_candidate_world(CRYSTALLIZATION_CANDIDATE_ID, 0, rows, no_added_reaction_audit)[
            "checks"
        ]["executable_law_binding"]
        is False
    )

    changed_baseline_rows = [dict(row) for row in rows]
    next(row for row in changed_baseline_rows if row["law_id"] == "baseline")["mechanism_hash"] = (
        "a" * 64
    )
    assert (
        analyze_candidate_world(CRYSTALLIZATION_CANDIDATE_ID, 0, changed_baseline_rows, audit)[
            "checks"
        ]["executable_law_binding"]
        is False
    )


def test_unpaired_or_leaking_result_is_rejected() -> None:
    rows = _rows(PARTITION_CANDIDATE_ID)
    rows.pop()
    result = analyze_candidate_world(
        PARTITION_CANDIDATE_ID, 0, rows, _audit(PARTITION_CANDIDATE_ID, 0)
    )
    assert result["passed"] is False
    assert "fixed_primary_denominator" in result["failures"]
    assert "complete_paired_law_roster" in result["failures"]

    rows = _rows(PARTITION_CANDIDATE_ID)
    rows[0]["participant_visible_leakage_matches"] = ["world_intervention"]
    result = analyze_candidate_world(
        PARTITION_CANDIDATE_ID, 0, rows, _audit(PARTITION_CANDIDATE_ID, 0)
    )
    assert "participant_visible_leakage_free" in result["failures"]


def test_prior_arms_bind_real_registered_laws_without_generic_surrogate() -> None:
    for candidate_id in CANDIDATE_IDS:
        priors = build_prior_arms(candidate_id)
        assert set(priors) == {"opaque", "aligned_nominal", "misindexed_nominal"}
        assert priors["aligned_nominal"]["confidence"] == 0.70
        assert priors["misindexed_nominal"]["confidence"] == 0.70
        assert (
            priors["aligned_nominal"]["executable_law"]["law_id"]
            == candidate_specs()[candidate_id]["altered_law_id"]
        )
        rendered = str(priors).lower()
        assert "quadratic" not in rendered
        assert "equilibrium" not in rendered


@pytest.mark.parametrize("candidate_id", CANDIDATE_IDS)
def test_actions_vary_the_registered_intervention_families(candidate_id: str) -> None:
    coordinates = registered_coordinates(candidate_id)
    first_family, second_family = candidate_specs()[candidate_id]["intervention_families"]
    first = [row for row in coordinates if row["intervention_family"] == first_family]
    second = [row for row in coordinates if row["intervention_family"] == second_family]
    first_actions = {
        _action_signature(_compile_actions(candidate_id, row["feature_values"])) for row in first
    }
    second_actions = {
        _action_signature(_compile_actions(candidate_id, row["feature_values"])) for row in second
    }
    assert len(first_actions) > 1
    assert len(second_actions) > 1


def _partition_pair_counts(rows: list[dict[str, Any]]) -> Counter[tuple[int, int]]:
    return Counter(
        (
            int(row["feature_values"]["solvent"]),
            int(row["feature_values"]["extractant"]),
        )
        for row in rows
    )


def test_partition_identity_roster_is_explicitly_stratified_over_all_pairs() -> None:
    identity = [
        row
        for row in registered_coordinates(PARTITION_CANDIDATE_ID)
        if row["intervention_family"] == "identity"
    ]
    q1 = [row for row in identity if row["phase"] == "q1_coverage"]
    heldout = [row for row in identity if row["phase"] == "q2_heldout"]
    assert _partition_pair_counts(q1) == Counter(dict.fromkeys(PARTITION_NOMINAL_PAIR_STRATA, 12))
    assert _partition_pair_counts(heldout) == Counter(
        dict.fromkeys(PARTITION_NOMINAL_PAIR_STRATA, 4)
    )
    assert all(
        row["feature_values"]["aqueous_phase_volume_L"] == 0.015
        and row["feature_values"]["extractant_volume_L"] == 0.019
        and row["feature_values"]["mix_duration_s"] == 420.0
        and row["feature_values"]["settle_duration_s"] == 900.0
        and row["feature_values"]["stirring_speed_rpm"] == 800.0
        for row in identity
    )


def test_partition_identity_q2_selection_is_balanced_not_single_extractant() -> None:
    selected = [
        row
        for row in selected_q2_queries(PARTITION_CANDIDATE_ID)
        if row["intervention_family"] == "identity"
    ]
    counts = _partition_pair_counts(selected)
    assert len(selected) == 8
    assert len(counts) == 8
    assert set(counts.values()) == {1}
    assert {pair[0] for pair in counts} == {0, 1, 2, 3}
    assert {pair[1] for pair in counts} == {0, 1, 2, 3}
    assert Counter(pair[0] for pair in counts) == Counter(dict.fromkeys(range(4), 2))
    assert Counter(pair[1] for pair in counts) == Counter(dict.fromkeys(range(4), 2))


def _action_signature(actions: list[dict[str, Any]]) -> str:
    return repr(actions)


@pytest.mark.parametrize("candidate_id", CANDIDATE_IDS)
def test_generated_d1_config_is_runnable_but_not_authorized(candidate_id: str) -> None:
    context = prepare_execution_context(Path.cwd(), mode="development")
    config = _d1_config(
        candidate_id,
        _load(BASE_CONFIGS[candidate_id]),
        package_sha256="p" * 64,
        execution_context=context,
    )
    assert config["world_seed"] == WORLD_SEEDS[0]
    assert config["campaign"]["complete_experiments"] == 12
    assert config["campaign"]["checkpoint_complete_experiments"] == [0, 3, 6, 9, 12]
    assert config["qualification"]["q2_passed"] is True
    assert config["qualification"]["execution_authorized"] is False
    assert config["qualification"]["formal_r5_authorized"] is False
    assert config["execution_context"]["evidence_status"] == "development_only"
    assert config["execution_context"]["c2_admission_authorized"] is False
    assert (
        config["intervention"]["registered_truth_law_id"]
        == candidate_specs()[candidate_id]["altered_law_id"]
    )
    for arm in config["prior_arms"]:
        contract = build_checkpoint_contract(config, arm)
        assert len(contract["held_out_queries"]) == 16
    card = _campaign_card(config)
    assert card.operation_attempt_limit == config["campaign"]["operation_attempt_limit"]


def test_no_equilibrium_candidate_and_all_five_worlds_are_frozen() -> None:
    assert set(CANDIDATE_IDS) == {
        PARTITION_CANDIDATE_ID,
        CRYSTALLIZATION_CANDIDATE_ID,
    }
    assert WORLD_SEEDS == (0, 1, 2, 3, 4)
    assert all("equilibrium" not in candidate for candidate in CANDIDATE_IDS)


def test_package_self_hash_excludes_its_own_field() -> None:
    package = {"schema_version": "test", "candidate_laws": {}}
    package["package_sha256"] = package_sha256(package)
    assert package["package_sha256"] == package_sha256(package)


def test_qualification_plan_survives_disk_roundtrip(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    context = prepare_execution_context(Path.cwd(), mode="development")
    monkeypatch.setattr(
        "chemworld.eval.work_ii_constitutive_structural_qualification._validated_q0_bindings",
        lambda *args, **kwargs: [],
    )
    plan = build_qualification_plan(
        Path.cwd(),
        q0_bindings={},
        execution_context=build_execution_envelope(context),
    )
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(json.dumps(plan), encoding="utf-8")
    reopened = json.loads(plan_path.read_text(encoding="utf-8"))

    assert reopened == plan
    assert (
        validate_qualification_plan(Path.cwd(), reopened, expected_execution_context=context) == []
    )


@pytest.mark.skipif(
    not (
        DEFAULT_DEVELOPMENT_PARTITION_Q0.is_file()
        and DEFAULT_DEVELOPMENT_CRYSTALLIZATION_Q0.is_file()
    ),
    reason="local ignored development Q0 summaries are unavailable",
)
def test_real_development_q0_bindings_build_a_valid_frozen_plan() -> None:
    context = prepare_execution_context(Path.cwd(), mode="development")
    args = type(
        "Args",
        (),
        {
            "partition_q0_summary": DEFAULT_DEVELOPMENT_PARTITION_Q0,
            "crystallization_q0_summary": DEFAULT_DEVELOPMENT_CRYSTALLIZATION_Q0,
        },
    )()
    q0_bindings = _validate_q0_inputs(args, context)
    plan = build_qualification_plan(
        Path.cwd(),
        q0_bindings=q0_bindings,
        execution_context=build_execution_envelope(context),
    )
    assert validate_qualification_plan(Path.cwd(), plan, expected_execution_context=context) == []

    changed = {**plan, "world_seeds": [0, 1, 2, 3]}
    changed["plan_sha256"] = plan_sha256(changed)
    assert "A-S qualification plan differs from the frozen spec or roster" in (
        validate_qualification_plan(Path.cwd(), changed, expected_execution_context=context)
    )


def test_rehashed_row_tamper_cannot_pass_without_bound_receipt(tmp_path: Path) -> None:
    from chemworld.eval.work_ii_constitutive_structural_qualification import (
        WORLD_REPORT_VERSION,
        report_sha256,
        validate_world_report,
    )

    context = prepare_execution_context(Path.cwd(), mode="development")
    report = {
        "schema_version": WORLD_REPORT_VERSION,
        "qualification_schema_version": ("chemworld-work-ii-constitutive-structural-q1-q2-0.1"),
        "formal_result": False,
        "provider_call_count": 0,
        "participant_session_count": 0,
        "execution_context": {
            "execution_mode": "development",
            "evidence_status": "development_only",
            "release_eligible": False,
            "c2_admission_authorized": False,
            "tested_commit": None,
            "freeze_id": None,
            "release_manifest_sha256": None,
            "execution_surface_sha256": None,
        },
        "plan_binding": {},
        "candidate_id": PARTITION_CANDIDATE_ID,
        "task_id": candidate_specs()[PARTITION_CANDIDATE_ID]["task_id"],
        "world_seed": 0,
        "law_audit": _audit(PARTITION_CANDIDATE_ID, 0),
        "rows": [{**_rows(PARTITION_CANDIDATE_ID)[0], "receipt": {}}],
        "analysis": {},
    }
    report["report_sha256"] = report_sha256(report)
    errors = validate_world_report(report, root=tmp_path, expected_execution_context=context)
    assert any("receipt" in error or "plan binding" in error for error in errors)


def test_cli_defaults_keep_all_development_artifacts_under_runs(
    monkeypatch: Any, tmp_path: Path
) -> None:
    output_root = tmp_path / "strict-as-dev"
    progress = tmp_path / "progress.jsonl"
    status = tmp_path / "status.json"
    captured: dict[str, Any] = {}

    def fake_run(args: Any) -> dict[str, Any]:
        captured["args"] = args
        return {
            "denominators": {
                "completed_primary_executions": PRIMARY_EXECUTIONS_TOTAL,
                "completed_exact_replays": EXACT_REPLAYS_TOTAL,
            },
            "decision": "development-test",
            "elapsed_s": 0.0,
            "all_candidates_passed": True,
        }

    monkeypatch.setattr(runner, "run", fake_run)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "strict-as",
            "--output-root",
            str(output_root),
            "--progress-file",
            str(progress),
            "--status-file",
            str(status),
        ],
    )
    assert runner.main() == 0
    args = captured["args"]
    assert args.execution_mode == "development"
    assert args.summary == output_root.resolve() / "summary.json"
    assert args.package == output_root.resolve() / "q2-package.json"
    assert args.partition_q0_summary == DEFAULT_DEVELOPMENT_PARTITION_Q0.resolve()
    assert args.crystallization_q0_summary == (DEFAULT_DEVELOPMENT_CRYSTALLIZATION_Q0.resolve())
    assert "partition-nominal-pair-q0" in args.partition_q0_summary.as_posix()


def test_q0_binding_accepts_new_nominal_pair_and_rejects_old_summary(
    monkeypatch: Any,
) -> None:
    context = prepare_execution_context(Path.cwd(), mode="development")
    args = type(
        "Args",
        (),
        {
            "partition_q0_summary": DEFAULT_DEVELOPMENT_PARTITION_Q0,
            "crystallization_q0_summary": DEFAULT_DEVELOPMENT_CRYSTALLIZATION_Q0,
        },
    )()
    new_partition = {
        "schema_version": "nominal-pair",
        "analysis": {"passed": True},
        "summary_sha256": "n" * 64,
    }
    crystallization = {
        "schema_version": "crystallization",
        "analysis": {"passed": True},
        "summary_sha256": "c" * 64,
    }
    payloads = {
        DEFAULT_DEVELOPMENT_PARTITION_Q0: new_partition,
        DEFAULT_DEVELOPMENT_CRYSTALLIZATION_Q0: crystallization,
    }
    monkeypatch.setattr(runner, "_load", lambda path: payloads[path])
    monkeypatch.setattr(
        runner,
        "validate_partition_q0",
        lambda payload, **kwargs: (
            []
            if payload.get("schema_version") == "nominal-pair"
            else ["unexpected partition nominal-pair Q0 summary schema"]
        ),
    )
    monkeypatch.setattr(
        runner,
        "validate_crystallization_q0",
        lambda root, payload, **kwargs: [],
    )
    monkeypatch.setattr(runner, "file_sha256", lambda path: "f" * 64)
    bindings = _validate_q0_inputs(args, context)
    assert bindings[PARTITION_CANDIDATE_ID]["path"] == (
        "runs/development/work-ii-partition-nominal-pair-q0-seed0-20260812/summary.json"
    )

    old_path = Path.cwd() / "old-nine-cell-summary.json"
    payloads[old_path] = {
        "schema_version": "old-nine-cell",
        "analysis": {"passed": True},
        "summary_sha256": "o" * 64,
    }
    args.partition_q0_summary = old_path
    with pytest.raises(RuntimeError, match="nominal-pair Q0"):
        _validate_q0_inputs(args, context)
