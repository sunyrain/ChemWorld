from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from chemworld.eval import work_ii_study_b2 as study_b2
from chemworld.eval.provenance import canonical_json_sha256
from chemworld.eval.work_ii_constitutive_structural_qualification import report_sha256

EVIDENCE_IDS = ["c385", "c401", "c417", "c433", "c449", "c465", "c481", "c497"]
SCORING_IDS = ["c393", "c409", "c425", "c441", "c457", "c473", "c489", "c505"]
METRIC_IDS = ["product_in_organic", "product_in_aqueous", "phase_ratio"]
INTERVENTION = {
    "kind": "mechanism_family",
    "mode": "constitutive_law_family",
    "severity": 1.0,
    "constitutive_law_change": {
        "transform_id": "partition_power_response_stress_v1",
        "partition_coefficient_exponent_at_full_severity": 1.75,
    },
}


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _qualification_report(world_index: int) -> dict:
    rows = []
    for coordinate_index in range(64):
        coordinate_id = f"c{385 + 2 * coordinate_index}"
        feature_values = {
            "partition_coefficient": 0.4 + coordinate_index / 100.0,
            "organic_to_aqueous_volume_ratio": 0.8 + coordinate_index / 200.0,
            "mixing_time_s": 60.0 + coordinate_index,
        }
        for law_id, offset in (("linear_response", 0.0), ("power_response", 0.2)):
            rows.append(
                {
                    "phase": "q2_heldout",
                    "intervention_family": "phase_process",
                    "status": "completed",
                    "exact_replay": True,
                    "safe": True,
                    "physical_failure": None,
                    "platform_failure": None,
                    "participant_visible_leakage_matches": [],
                    "coordinate_id": coordinate_id,
                    "coordinate_index": coordinate_index,
                    "coordinate_sha256": canonical_json_sha256(feature_values),
                    "law_id": law_id,
                    "feature_values": feature_values,
                    "metrics": dict.fromkeys(METRIC_IDS, 0.2 + offset),
                }
            )
    rows.extend({"phase": "unused"} for _ in range(1024 - len(rows)))
    report = {
        "candidate_id": "partition_power_response",
        "task_id": "partition-discovery",
        "world_seed": world_index,
        "provider_call_count": 0,
        "participant_session_count": 0,
        "rows": rows,
    }
    report["report_sha256"] = report_sha256(report)
    return report


def _build_fixture(tmp_path: Path) -> Path:
    for world_index in range(5):
        _write_json(
            tmp_path / "qualification" / f"world-{world_index}" / "world-report.json",
            _qualification_report(world_index),
        )
    runtime = {
        "task_id": "partition-discovery",
        "world_interventions": [deepcopy(INTERVENTION)],
        "belief_checkpoint": {"held_out_queries": []},
        "prior_arms": {
            arm: {"initial_world_model": {"arm": arm}}
            for arm in study_b2.ARMS
        },
    }
    _write_json(tmp_path / "runtime.json", runtime)
    protocol = {
        "schema_version": study_b2.STUDY_B2_PROTOCOL_VERSION,
        "study_id": "test-b2",
        "runtime_config": "runtime.json",
        "source_qualification_root": "qualification",
        "qualification_world_indices": [0, 1, 2, 3, 4],
        "public_world_seeds": [101, 102, 103, 104, 105],
        "arms": list(study_b2.ARMS),
        "query_selection": {
            "phase": "q2_heldout",
            "intervention_family": "phase_process",
            "candidate_laws": ["linear_response", "power_response"],
            "evidence_positions": [0, 8, 16, 24, 32, 40, 48, 56],
            "scoring_positions": [4, 12, 20, 28, 36, 44, 52, 60],
            "expected_evidence_query_ids": EVIDENCE_IDS,
            "expected_scoring_query_ids": SCORING_IDS,
            "metric_ids": METRIC_IDS,
            "paired_law_effect_gates": {
                "product_in_organic": 0.06,
                "product_in_aqueous": 0.06,
                "phase_ratio": 0.072,
            },
            "required_passing_metric_count_per_query": 2,
        },
        "provider": {"id": "test"},
        "execution": {"formal_sessions": 15},
    }
    protocol_path = tmp_path / "protocol.json"
    _write_json(protocol_path, protocol)
    return protocol_path


def test_b2_manifest_freezes_roster_denominators_and_power_truth(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    protocol_path = _build_fixture(tmp_path)
    seen_interventions = []

    def fake_plan(cluster: dict, config: dict, **_: object) -> dict:
        return {
            "world_seed": cluster["world_seed"],
            "truth_query_count": 16,
            "truth_query_metric_count": 48,
            "plan_sha256": f"plan-{cluster['world_seed']}",
        }

    def fake_execute(plan: dict, config: dict, output_root: Path) -> dict:
        seen_interventions.append(deepcopy(config["world_interventions"]))
        output_root.mkdir(parents=True)
        _write_json(output_root / "plan.json", plan)
        truth = {
            query_id: dict.fromkeys(METRIC_IDS, 0.5)
            for query_id in EVIDENCE_IDS + SCORING_IDS
        }
        report = {
            "status": "completed",
            "completed_truth_query_count": 16,
            "truth": truth,
            "report_sha256": f"report-{plan['world_seed']}",
        }
        _write_json(output_root / "report.json", report)
        return report

    monkeypatch.setattr(study_b2, "build_evaluator_truth_plan", fake_plan)
    monkeypatch.setattr(study_b2, "validate_evaluator_truth_plan", lambda _: [])
    monkeypatch.setattr(study_b2, "execute_evaluator_truth_plan", fake_execute)
    monkeypatch.setattr(study_b2, "validate_evaluator_truth_report", lambda *_: [])

    manifest = study_b2.build_study_b2_manifest(
        protocol_path,
        repository_root=tmp_path,
        output_root=tmp_path / "output",
    )

    assert manifest["cell_count"] == 15
    assert manifest["cluster_count"] == 5
    assert manifest["scoring_term_count"] == 24
    assert len(seen_interventions) == 5
    assert all(value == [INTERVENTION] for value in seen_interventions)
    for cluster_id in {cell["cluster_id"] for cell in manifest["cells"]}:
        members = [cell for cell in manifest["cells"] if cell["cluster_id"] == cluster_id]
        assert len(members) == 3
        assert {cell["arm"] for cell in members} == set(study_b2.ARMS)
        assert len({cell["public_packet_sha256"] for cell in members}) == 1
        packet = members[0]["public_packet"]
        assert [row["query_id"] for row in packet["evidence"]] == EVIDENCE_IDS
        assert [row["query_id"] for row in packet["scoring_queries"]] == SCORING_IDS
        assert set(EVIDENCE_IDS).isdisjoint(SCORING_IDS)


def test_b2_rejects_selected_query_below_diagnostic_gate(tmp_path: Path) -> None:
    protocol_path = _build_fixture(tmp_path)
    report_path = tmp_path / "qualification/world-3/world-report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    for row in report["rows"]:
        if row.get("coordinate_id") == EVIDENCE_IDS[0] and row.get("law_id") == "power_response":
            row["metrics"] = dict.fromkeys(METRIC_IDS, 0.21)
    report["report_sha256"] = report_sha256(report)
    _write_json(report_path, report)
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))

    with pytest.raises(ValueError, match="is not diagnostic in qualification world 3"):
        study_b2._source_bundle(protocol, tmp_path)
