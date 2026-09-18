from __future__ import annotations

import json
from pathlib import Path

from chemworld.eval import experiment_1_challenge as challenge
from chemworld.eval.provenance import canonical_json_sha256, file_sha256


def test_pa_parametric_probe_fails_lower_budget_edge_when_default_is_robust() -> None:
    report = {
        "aligned_prior": {"k_star_band": [3.8, 4.6]},
        "misspecified_prior": {"k_star_band": [5.1, 6.3]},
        "aligned_contains_fit": True,
        "misspecified_contains_fit": False,
        "phase_point_reports": [
            {
                "point_id": "low_ratio",
                "prediction_gap": 0.08,
                "noise_robust_counterexample": True,
            },
            {
                "point_id": "reference",
                "prediction_gap": 0.06,
                "noise_robust_counterexample": True,
            },
        ],
    }
    probe = challenge._pa_parametric_probe(
        report,
        {
            "default_point_id": "reference",
            "minimum_active_prediction_gap": 0.05,
            "plausible_false_to_aligned_center_ratio": [0.5, 1.6],
        },
    )

    assert probe["plausibility_passed"] is True
    assert probe["default_one_shot_reliably_discriminates"] is True
    assert probe["active_information_passed"] is True
    assert probe["minimum_reliable_unique_condition_cost"] == 1


def test_entity_probe_requires_paired_conditions() -> None:
    report = {
        "descriptor_permutation": [3, 1, 2, 0],
        "prior_audit": {"passed": True, "checks": {}},
        "private_world_audit": {
            "mapping_rows": [
                {"own_mapping_closer": True},
                {"own_mapping_closer": True},
            ]
        },
        "anchor_results": [{"passed": True, "signal_to_noise_ratio": 4.2}],
    }
    probe = challenge._entity_probe(report, {"minimum_active_snr": 2.0})

    assert probe["plausibility_passed"] is True
    assert probe["default_one_shot_reliably_discriminates"] is False
    assert probe["active_information_passed"] is True
    assert probe["minimum_reliable_unique_condition_cost"] == 2


def test_build_probe_summary_preserves_full_denominator_and_fail_closed(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(challenge, "validate_contract", lambda contract, root: None)

    def synthetic_probe(report, rule):
        default_success = report["world_index"] < 5 or rule.get("all_default", False)
        return {
            "plausibility_passed": True,
            "plausibility_evidence": "synthetic",
            "default_one_shot_reliably_discriminates": default_success,
            "default_evidence": "synthetic",
            "active_information_score": 1.0,
            "active_information_passed": True,
            "active_evidence": "synthetic",
            "minimum_reliable_unique_condition_cost": 2,
        }

    monkeypatch.setitem(challenge.PROBE_FAMILIES, "synthetic", synthetic_probe)
    contract = {
        "source_registry": {"registry_sha256": "r" * 64},
        "denominator": {"trivial_lower_bound_unique_conditions": 1},
        "loci": {
            block: {
                "probe_family": "synthetic",
                "participant_budget": 4,
                "all_default": block == "PA-P",
            }
            for block in challenge.EXPECTED_BLOCKS
        },
    }
    evidence_root = tmp_path / "evidence"
    rows = []
    for block in challenge.EXPECTED_BLOCKS:
        system, short = block.split("-")
        locus = {"E": "entity", "P": "parametric", "S": "structural"}[short]
        for index in range(1, 6):
            relative = f"runs/{block}/W{index}.json"
            path = evidence_root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            report = {"world_index": index}
            report["report_sha256"] = canonical_json_sha256(report)
            path.write_text(json.dumps(report), encoding="utf-8")
            rows.append(
                {
                    "unit_id": f"{system}-W{index:02d}:{locus}",
                    "system_id": system,
                    "prior_locus": locus,
                    "world_id": f"{system}-W{index:02d}",
                    "current_status": "qualified-development",
                    "qualification_run": {
                        "evidence": {
                            "path": relative,
                            "sha256": file_sha256(path),
                            "report_sha256": report["report_sha256"],
                        }
                    },
                }
            )
    registry = {
        "registry_sha256": "r" * 64,
        "rows": rows
        + [
            {
                "unit_id": f"unused-{index}",
                "system_id": "D",
                "prior_locus": "entity",
            }
            for index in range(55)
        ],
    }

    summary = challenge.build_probe_summary(
        contract,
        registry,
        root=tmp_path,
        evidence_roots=[evidence_root],
    )

    assert summary["denominators"]["planned_world_probe_rows"] == 50
    assert summary["denominators"]["completed_world_probe_rows"] == 50
    assert len(summary["world_probe_rows"]) == 50
    assert summary["challenge_passed_loci"] == 9
    failed = next(row for row in summary["loci"] if row["block"] == "PA-P")
    assert failed["checks"]["non_triviality"] is False
    assert failed["challenge_probe_passed"] is False
