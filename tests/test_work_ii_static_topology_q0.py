from __future__ import annotations

from typing import Any

from chemworld.eval.work_ii_static_topology_q0 import (
    LAW_IDS,
    analyze_task,
    registered_cells,
    task_specs,
    topology_intervention,
)


def _rows(task_id: str) -> list[dict[str, Any]]:
    spec = task_specs()[task_id]
    rows = []
    for cell in registered_cells(task_id):
        for law_id in LAW_IDS:
            time_index = int(cell["time_index"])
            reverse_penalty = 0.0 if law_id == "baseline" else 0.08 + 0.07 * time_index
            metrics = dict.fromkeys(spec["direct_metrics"], 0.75 - reverse_penalty)
            rows.append(
                {
                    **cell,
                    "task_id": task_id,
                    "law_id": law_id,
                    "status": "completed",
                    "safe": True,
                    "exact_replay": True,
                    "action_plan_sha256": f"actions-{cell['cell_id']}",
                    "direct_noise_key_sha256": f"noise-{cell['cell_id']}",
                    "direct_metrics": metrics,
                    "direct_observed_mask": dict.fromkeys(spec["direct_metrics"], True),
                    "participant_visible_payload": {"observation": metrics},
                }
            )
    return rows


def _mechanism_audit() -> dict[str, Any]:
    return {
        "added_reaction_count": 1,
        "mechanism_hash_changed": True,
        "reversible_hash_deterministic": True,
        "execution_mechanism_binding_matches": True,
    }


def test_topology_intervention_is_explicit() -> None:
    payload = topology_intervention()
    assert payload["mode"] == "topology_family"
    assert payload["topology_change"]["transform_id"] == (
        "reversible_target_pathway_stress_v1"
    )


def test_static_topology_q0_accepts_separated_accumulating_signal() -> None:
    for task_id in task_specs():
        result = analyze_task(task_id, _rows(task_id), _mechanism_audit())
        assert result["passed"] is True
        assert result["denominators"] == {
            "attempted": 18,
            "completed": 18,
            "exact_replay": 18,
            "physical_failures": 0,
            "platform_failures": 0,
            "unsafe_completed": 0,
        }
        assert result["passing_metric_count"] >= 2
        assert result["separated_support"] is True


def test_static_topology_q0_rejects_unpaired_noise() -> None:
    rows = _rows("reaction-to-crystallization")
    rows[0]["direct_noise_key_sha256"] = "unpaired"

    result = analyze_task("reaction-to-crystallization", rows, _mechanism_audit())

    assert result["passed"] is False
    assert "paired_observation_noise" in result["failures"]


def test_static_topology_q0_rejects_weak_signal() -> None:
    rows = _rows("flow-reaction-optimization")
    for row in rows:
        row["direct_metrics"] = dict.fromkeys(row["direct_metrics"], 0.5)

    result = analyze_task("flow-reaction-optimization", rows, _mechanism_audit())

    assert result["passed"] is False
    assert "at_least_two_direct_metrics_resolve_topology" in result["failures"]
    assert "duration_accumulation_signature" in result["failures"]
