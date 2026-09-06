import json

from chemworld.eval.work_ii_information_intervention import cells_for_world, prompt, summarize
from chemworld.eval.work_ii_public_endpoint_reference import candidate_domains, public_contract


def world():
    query = {"query_id": "q", "reference_partition_coefficient": 2.0}
    return {
        "cluster_id": "test",
        "target_exponent": 2.05,
        "scoring_truth": {
            "q": {
                "product_in_organic": 0.8,
                "product_in_aqueous": 0,
                "phase_ratio": 1,
                "score": 0.58,
            }
        },
        "public_packet": {
            "task_id": "partition-discovery",
            "metric_range": [0, 1],
            "candidate_mechanism_families": [],
            "scoring_action_queries": [query],
            "candidate_parameter_domains": candidate_domains(),
            "complete_observation_contract": public_contract(298.15),
            "evidence": [],
        },
    }


def test_only_post_disclosure_differs_within_prior_pair():
    cells = cells_for_world(world(), "gpt", 0)
    assert len(cells) == len({c["cell_id"] for c in cells}) == 6
    for a, b in zip(cells[::2], cells[1::2], strict=True):
        assert prompt(a, "pre", "on") == prompt(b, "pre", "on")
        pa = json.loads(prompt(a, "post", "on").rsplit("\n", 1)[1])
        pb = json.loads(prompt(b, "post", "on").rsplit("\n", 1)[1])
        assert ("complete_observation_contract" in pa) != ("complete_observation_contract" in pb)
        pa.pop("complete_observation_contract", None)
        pb.pop("complete_observation_contract", None)
        assert pa == pb
        assert "scoring_truth" not in pa and "target_exponent" not in pa
        assert "initial_world_model" not in pa
    # Unknown-prior prompt contains no realized answer.
    assert "2.05" not in prompt(cells[0], "pre", "on")


def test_recovery_uses_each_world_answer_and_excludes_retention():
    cells = cells_for_world(world(), "gpt", 0)
    results = []
    for cell in cells:
        payload = {
            "family": "FAMILY_B_POWER",
            "exponent": 2.05,
            "predictions": world()["scoring_truth"],
            "selected_query_id": "q",
        }
        status = "completed" if cell["information"] == "complete" else "failed"
        results.append({"cell_id": cell["cell_id"], "status": status, "post": payload})
    report = summarize(results, cells, formal=False)
    assert report["primary"]["mean"] == 1
    assert report["counts"] == {"failed": 3, "completed": 3}
    complete_recovery = next(
        g for g in report["groups"] if (g["information"], g["analysis"]) == ("complete", "recovery")
    )
    assert complete_recovery["scheduled"] == complete_recovery["joint_recovery"] == 2
    assert report["primary"]["approximate_world_bootstrap_95"] is None
