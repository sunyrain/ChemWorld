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
