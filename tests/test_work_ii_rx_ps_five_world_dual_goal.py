from __future__ import annotations

import copy

from scripts import run_work_ii_rx_ps_five_world_dual_goal as runner


def _design():
    config = runner.read(runner.CONFIG)
    return config, runner.validate_design(config)


def test_frozen_denominator_and_schedule_are_exact():
    config, validated = _design()
    assert config["counts"] == {
        "independent_source_sessions": 60,
        "model_stages_including_source": 240,
        "posttests": 180,
        "posttests_per_session": 3,
        "reference_executions": 600,
        "reference_repeats_per_query": 5,
        "source_batches": 720,
        "source_batches_per_session": 12,
    }
    assert len(validated["schedule"]) == 60
    assert len({row["cell_id"] for row in validated["schedule"]}) == 60
    assert {row["world_seed"] for row in validated["schedule"]} == set(range(5))
    assert {row["locus"] for row in validated["schedule"]} == {"P", "S"}
    assert {row["arm"] for row in validated["schedule"]} == set(runner.ARMS)
    assert {row["goal"] for row in validated["schedule"]} == set(runner.GOALS)


def test_strict_opaque_and_matched_prior_arms():
    _, validated = _design()
    for locus in runner.LOCI:
        for _, seed in runner.WORLDS:
            material, opaque = runner.priors(
                locus,
                "Opaque",
                seed,
                validated["p_package"],
                validated["s_contract"],
            )
            assert material == {"mode": "opaque_codes"}
            assert opaque is None
            _, aligned = runner.priors(
                locus,
                "Aligned",
                seed,
                validated["p_package"],
                validated["s_contract"],
            )
            _, wrong = runner.priors(
                locus,
                "MisIndexed",
                seed,
                validated["p_package"],
                validated["s_contract"],
            )
            if locus == "P":
                assert aligned["context_contract"] == wrong["context_contract"]
                a = copy.deepcopy(aligned)
                m = copy.deepcopy(wrong)
                assert (
                    a["model"]["claim"].pop("expected_relation")
                    != m["model"]["claim"].pop("expected_relation")
                )
                assert a == m
            else:
                assert aligned["claim"] != wrong["claim"]
                assert {k: v for k, v in aligned.items() if k != "claim"} == {
                    k: v for k, v in wrong.items() if k != "claim"
                }


def test_p_and_s_queries_are_twelve_legal_blind_batches():
    config, _ = _design()
    for locus in runner.LOCI:
        rows = runner.queries(config, locus)
        assert [row["query_id"] for row in rows] == [f"Q{i:02d}" for i in range(1, 13)]
        for row in rows:
            assert row["actions"][-2:] == [
                {"operation": "terminate"},
                {"operation": "measure", "instrument": "final_assay"},
            ]
            heat = [action for action in row["actions"] if action["operation"] == "heat"]
            assert 1 <= len(heat) <= 2
            assert all(350 <= action["target_temperature_K"] <= 465 for action in heat)
            assert all(0 < action["duration_s"] <= 14400 for action in heat)
    assert runner.queries(config, "P") != runner.queries(config, "S")


def test_s_gate_has_three_unique_paired_noise_coordinates_per_condition():
    config, _ = _design()
    gate = config["S_start_gate"]
    assert len(gate["ordered_action_ids"]) == 3
    assert gate["independent_noise_replicates_per_action_and_family"] == 3
    keys = set()
    for world_seed in range(5):
        for action_id in gate["ordered_action_ids"]:
            action_keys = set()
            for replicate in range(1, 4):
                seed = runner.deterministic_seed(
                    "rx-ps-s-start-gate-v1", world_seed, action_id, replicate
                )
                namespace = (
                    f"work-ii-rx-ps-s-gate-w{world_seed}-{action_id}-r{replicate:02d}"
                )
                key = runner.ObservationNoiseCoordinate(
                    namespace=namespace,
                    base_observation_seed=seed,
                    experiment_index=0,
                    operation_type="measure",
                    instrument="hplc",
                    replicate_index=0,
                ).key_sha256
                action_keys.add(key)
                keys.add(key)
            assert len(action_keys) == 3
    assert len(keys) == 45


def test_s_gate_accumulation_uses_parent_minus_reversible_child():
    config, _ = _design()
    rows = []
    action_ids = config["S_start_gate"]["ordered_action_ids"]
    parent_values = (0.20, 0.58, 0.83)
    child_values = (0.19, 0.51, 0.74)
    for action_id, parent, child in zip(action_ids, parent_values, child_values, strict=True):
        for replicate in range(3):
            noise_key = f"{action_id}-noise-{replicate}"
            for law_id, value in (
                ("deactivating_baseline", parent),
                ("reversible_target_pathway", child),
            ):
                rows.append(
                    {
                        "cell_id": action_id,
                        "law_id": law_id,
                        "status": "completed",
                        "direct_noise_key_sha256": noise_key,
                        "direct_metrics": {
                            "yield": value,
                            "conversion": value,
                            "selectivity": value,
                        },
                    }
                )
    policy = {
        "ordered_action_ids": action_ids,
        "minimum_noise_replicates": 3,
        "minimum_accumulation": 0.03,
        "minimum_information_gain": 0.03,
        "participant_budget": 4,
    }
    trace = runner._rx_structural_trace_direction_corrected(rows, policy)
    assert trace["estimand_version"] == "rx-s-parent-minus-child-accumulation-1.0.1"
    assert trace["minimum_reliable_unique_condition_cost"] == 2
    assert trace["active_information_passed"] is True
    assert trace["budget_window_passed"] is True


def test_posttest_contract_and_resource_envelope():
    config, _ = _design()
    assert "用英文提交" in runner.K1
    assert "按1—7逐项深入复盘" in runner.K2
    assert "80%预测区间" in runner.Q_PROMPT
    schema = runner.posttest_schema("Q")
    assert schema["properties"]["predictions"]["minItems"] == 12
    assert schema["properties"]["predictions"]["maxItems"] == 12
    assert set(
        schema["properties"]["predictions"]["items"]["properties"]["metrics"]["required"]
    ) == set(runner.METRICS)
    assert config["source_resource_card"]["process_time_limit_s"] == 216000
    assert runner.resource_card().process_time_limit_s == 216000
