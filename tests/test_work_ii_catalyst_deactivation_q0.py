from __future__ import annotations

from typing import Any

from chemworld.eval.work_ii_catalyst_deactivation_q0 import (
    DIRECT_METRICS,
    LAW_IDS,
    TASK_ID,
    analyze,
    registered_cells,
    stable_catalyst_intervention,
)


def _rows() -> list[dict[str, Any]]:
    rows = []
    for cell in registered_cells():
        duration_index = int(cell["duration_index"])
        dose_index = int(cell["dose_index"])
        advantage = 0.01 + 0.07 * duration_index + 0.02 * dose_index
        for law_id in LAW_IDS:
            value = 0.55 if law_id == "deactivating_baseline" else 0.55 + advantage
            metrics = dict.fromkeys(DIRECT_METRICS, value)
            rows.append(
                {
                    **cell,
                    "task_id": TASK_ID,
                    "law_id": law_id,
                    "status": "completed",
                    "safe": True,
                    "exact_replay": True,
                    "action_plan_sha256": f"actions-{cell['cell_id']}",
                    "direct_noise_key_sha256": f"noise-{cell['cell_id']}",
                    "direct_metrics": metrics,
                    "direct_observed_mask": dict.fromkeys(DIRECT_METRICS, True),
                    "participant_visible_payload": {"observation": metrics},
                }
            )
    return rows


def _mechanism_audit() -> dict[str, Any]:
    return {
        "removed_reaction_count": 1,
        "removed_reaction_id": "catalyst_deactivation",
        "mechanism_hash_changed": True,
        "stable_hash_deterministic": True,
        "execution_mechanism_binding_matches": True,
    }


def test_stable_catalyst_intervention_is_explicit_and_discrete() -> None:
    payload = stable_catalyst_intervention()
    assert payload["severity"] == 1.0
    assert payload["topology_change"] == {
        "reaction_role": "catalyst_deactivation_pathway",
        "transform_id": "stable_catalyst_topology_v1",
    }


def test_q0_accepts_separated_accumulating_signal() -> None:
    result = analyze(_rows(), _mechanism_audit())
    assert result["passed"] is True
    assert result["denominators"] == {
        "attempted": 54,
        "completed": 54,
        "exact_replay": 54,
        "physical_failures": 0,
        "platform_failures": 0,
        "unsafe_completed": 0,
    }
    assert result["passing_metric_count"] >= 2
    assert result["separated_support"] is True
    assert result["dose_coverage"] is True


def test_q0_rejects_unpaired_noise() -> None:
    rows = _rows()
    rows[0]["direct_noise_key_sha256"] = "unpaired"
    result = analyze(rows, _mechanism_audit())
    assert result["passed"] is False
    assert "paired_observation_noise" in result["failures"]


def test_q0_rejects_weak_signal() -> None:
    rows = _rows()
    for row in rows:
        row["direct_metrics"] = dict.fromkeys(DIRECT_METRICS, 0.5)
    result = analyze(rows, _mechanism_audit())
    assert result["passed"] is False
    assert "at_least_two_direct_metrics_resolve_topology" in result["failures"]
    assert "duration_accumulation_signature" in result["failures"]
