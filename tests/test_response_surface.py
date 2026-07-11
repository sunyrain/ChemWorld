from __future__ import annotations

from chemworld.eval.response_surface import audit_serious_response_surfaces


def test_response_surface_probe_is_not_labeled_as_an_oracle() -> None:
    report = audit_serious_response_surfaces(
        samples_per_seed=2,
        task_ids=("partition-discovery",),
    )

    assert report["reference_semantics"]["is_oracle"] is False
    assert report["reference_semantics"]["regret_reference_allowed"] is False
    task = report["tasks"]["partition-discovery"]
    assert "approximate_oracle_score" not in task
    assert task["sampled_recipe_ceiling_score"] >= task["score"]["median"]
    assert set(task["seed_reports"]) == {"0", "1", "2", "3", "4"}
