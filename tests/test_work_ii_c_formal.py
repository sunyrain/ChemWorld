from __future__ import annotations

import copy
import json

import pytest
from scripts import run_work_ii_c_formal as c


@pytest.mark.parametrize("budget", [12, 24])
@pytest.mark.parametrize("arm", c.pilot.ARMS)
def test_actual_public_tool_retains_anonymity_and_delivers_budget(arm, budget):
    result = c.check_public(arm, 2, budget)
    assert result["anonymous"] and result["particle_available"]
    assert result["contract"]["study_budget"] == {
        "complete_batches": budget,
        "extra_measurements": budget,
        "final_assays": budget,
        "operation_attempts": 60 * budget,
    }
    assert (result["payload"]["material_information"]["dossier"] is None) == (arm == "Opaque")
    system = c.source_system(budget)
    assert f"Complete {budget}" in system
    assert f"with {budget} extra" in system
    assert f"plus {budget} final assays and {60 * budget}" in system
    assert "128 public calculator attempts" in system
    assert "target product present before separation" in system
    definition = result["contract"]["prediction_metrics"]["crystal_yield"]
    assert "target product present before separation" in definition
    assert "target product present before separation" in c.pilot.prediction_question([])


def test_counterfactual_priors_are_only_a_dossier_permutation():
    aligned = c.check_public("Aligned", 0, 12)["payload"]["material_information"]["dossier"]
    mismatch = c.check_public("MisIndexed", 0, 12)["payload"]["material_information"]["dossier"]
    assert aligned["choices"]["catalyst"] == mismatch["choices"]["catalyst"]
    for i, j in enumerate([0, 3, 2, 1]):
        assert (
            mismatch["choices"]["solvent"][i]["nominal_properties"]
            == aligned["choices"]["solvent"][j]["nominal_properties"]
        )


def test_recommendation_retest_preserves_source_measurement_envelope(tmp_path):
    actions = c.process(path=[c.pilot.cool(278.15, 120)])
    actions.insert(-3, {"operation": "measure", "instrument": "particle_size"})
    actions.insert(-3, {"operation": "measure", "instrument": "hplc"})
    result = c.fixed(tmp_path / "retest", actions, world_seed=0, envelope=12)
    assert result["passed"]
    assert result["exact_replay"]["verified"]
    assert len(result["batches"]) == 1


def test_rejected_duplicate_seed_is_not_part_of_the_physical_retest(tmp_path):
    actions = c.process(path=[c.pilot.cool(278.15, 120)])
    seed_position = next(i for i, a in enumerate(actions) if a["operation"] == "seed_crystals")
    actions.insert(seed_position + 1, copy.deepcopy(actions[seed_position]))
    source_truth = []
    trajectory = tmp_path / "source.jsonl"
    c.physics(
        c._FrozenTruthReplayAgent(actions),
        trajectory,
        world_seed=0,
        batches=1,
        truths=source_truth,
        envelope=12,
        arm="Opaque",
        observation_seed=101,
        callback=None,
    )
    records = c.load_jsonl(trajectory)
    original_bytes = trajectory.read_bytes()
    recipe = c.pilot.committed_recipe(records, 1)
    assert len(recipe["excluded_rejected_attempts"]) == 1
    assert sum(a["operation"] == "seed_crystals" for a in recipe["actions"]) == 1
    result = c.fixed(tmp_path / "corrected", recipe["actions"], world_seed=0, envelope=12)
    assert result["passed"] and result["truth"] == source_truth
    assert trajectory.read_bytes() == original_bytes
    with pytest.raises(ValueError, match="final assay"):
        c.pilot.committed_recipe(records[:-1], 1)
    unknown = copy.deepcopy(records)
    unknown[0]["transaction_status"] = "unknown"
    with pytest.raises(ValueError, match="Unknown transaction"):
        c.pilot.committed_recipe(unknown, 1)


def fixture_prediction():
    queries = [{"query_id": f"Q{i:02d}", "pair": c.FACTORS[(i - 1) // 2]} for i in range(1, 13)]
    truth = {
        q["query_id"]: {
            "crystal_yield": 0.2,
            "crystal_purity": 0.95,
            "crystal_size": 0.1,
            "crystal_fines_fraction": 0.2 if i % 2 else 0.9,
            "particles_present": True,
        }
        for i, q in enumerate(queries)
    }
    payload = {
        "predictions": [
            {
                "query_id": key,
                "quality_feasible": c.pilot.quality(values),
                "particles_present": True,
                **{
                    m: {
                        "estimate": values[m],
                        "lower80": max(0, values[m] - 0.02),
                        "upper80": min(1, values[m] + 0.02),
                    }
                    for m in c.METRICS
                },
            }
            for key, values in truth.items()
        ]
    }
    return queries, truth, payload


def test_public_neighbor_baseline_does_not_count_rejected_seed_doses():
    records = []
    for batch, dose, value in ((0, 0.05, 0.2), (1, 0.15, 0.8)):
        base = {"experiment_index": batch, "transaction_status": "committed"}
        action = {"operation": "seed_crystals", "seed_mass_g": dose}
        records.append({**base, "action": action})
        if batch == 0:
            records.extend(
                {**base, "action": action, "transaction_status": "validation_failed"}
                for _ in range(40)
            )
        records.append(
            {
                **base,
                "action": {"operation": "measure", "instrument": "final_assay"},
                "instrument": "final_assay",
                "observation": dict.fromkeys(c.METRICS, value),
            }
        )
    queries = [
        {
            "query_id": "Q01",
            "actions": [
                {
                    "operation": "seed_crystals",
                    "seed_mass_g": 0.05,
                }
            ],
        }
    ]
    result = c.public_baselines(records, queries, {"Q01": dict.fromkeys(c.METRICS, 0.2)})
    assert result["training_batches"] == 2
    assert all(v == 0 for v in result["mae"]["public_nearest_neighbor"].values())


def test_scoring_separates_resolved_effects_ties_and_quality_classes():
    queries, truth, payload = fixture_prediction()
    result = c.evaluate(payload, truth, queries)
    assert result["valid"]
    assert result["resolved_direction_n"] == result["resolved_direction_correct"] == 6
    assert result["tie_n"] == result["tie_correct"] == 18
    assert result["quality"]["balanced_accuracy"] == 1
    assert result["metrics"]["crystal_yield"]["interval_score80"] == pytest.approx(0.04)
    wrong = copy.deepcopy(payload)
    for r in wrong["predictions"]:
        r["quality_feasible"] = False
    assert c.evaluate(wrong, truth, queries)["quality"]["balanced_accuracy"] == 0.5
    broken = copy.deepcopy(payload)
    broken["predictions"][0].pop("crystal_size")
    result = c.evaluate(broken, truth, queries)
    assert not result["valid"]
    assert result["metrics"]["crystal_size"]["n"] == 11
    assert result["metrics"]["crystal_size"]["planned"] == 12


def test_live_report_does_not_claim_zero_batches_or_erase_failures(tmp_path):
    root, report = tmp_path / "run", tmp_path / "report"
    cell = {"id": "C-W01-B12-E-Opaque", "arm": "Opaque", "batches": 12}
    c.write(
        root / "design.json",
        {"protocol": "test", "schedule": [cell], "planned_batches": 12, "planned_posttests": 3},
    )
    folder = root / "sources" / cell["id"]
    c.write(
        folder / "result.json",
        {
            "id": cell["id"],
            "arm": "Opaque",
            "batches_budget": 12,
            "status": "running",
            "posttests": {},
        },
    )
    record = {
        "experiment_index": 0,
        "transaction_status": "committed",
        "instrument": "final_assay",
        "action": {"operation": "measure", "instrument": "final_assay"},
        "observation": {},
    }
    (folder / "trajectory.jsonl").write_text(json.dumps(record) + '\n{"partial":', encoding="utf-8")
    result = c.export(root, report)
    assert result["completed_chains"] == 0
    assert result["sealed_batches"] == 0
    assert result["live_unsealed_batches"] == 1
    assert result["started_sources"] == 1
    c.write(root / "qualification/result.json", {"status": "running", "worlds": {}})
    c.write(
        root / "controller-status.json",
        {
            "stage": "qualification",
            "pid": c.os.getpid(),
            "process_created": c.psutil.Process().create_time() - 100,
        },
    )
    assert c.export(root, report)["phase"] == "interrupted"
