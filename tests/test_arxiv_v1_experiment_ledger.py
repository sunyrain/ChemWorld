from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    ROOT
    / "workstreams/arxiv_v1/reports/"
    "experimental-intelligence-experiment-ledger-v0.1.json"
)


def _load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_arxiv_v1_experiment_accounting_has_no_g0_double_count() -> None:
    ledger = _load(LEDGER_PATH)
    g0 = ledger["experiment_layers"]["g0_compiled_recipe"]
    accounting = ledger["scientific_experiment_accounting"]

    assert g0["participant_three_arm"]["opaque_slice_reuses_v1_0_participant"]
    assert g0["nonduplicated_active_total"]["physical_experiments"] == (
        g0["classic_baselines"]["physical_experiments"]
        + g0["participant_three_arm"]["physical_experiments"]
    )
    assert g0["nonduplicated_active_total"]["physical_experiments"] == 29_580
    assert accounting["completed_or_audited_before_v0_5"]["total"] == (
        accounting["completed_or_audited_before_v0_5"][
            "g0_physical_experiments"
        ]
        + accounting["completed_or_audited_before_v0_5"][
            "g2_v0_4_completed_physical_experiments"
        ]
    )
    assert accounting["completed_or_audited_before_v0_5"]["total"] == 29_640


def test_arxiv_v1_required_remaining_experiments_match_frozen_g2_protocol() -> None:
    ledger = _load(LEDGER_PATH)
    protocol = _load(
        ROOT
        / "configs/benchmark/"
        "g2_autonomous_electrochemical_material_seed1_seed3_r5_v0.5_dev.json"
    )
    g2 = ledger["experiment_layers"][
        "g2_v0_5_fresh_trajectory_replication"
    ]
    remaining = ledger["scientific_experiment_accounting"][
        "required_remaining_for_arxiv_v1"
    ]

    assert g2["cells"]["planned"] == protocol["planned_resources"]["cells"]
    assert g2["physical_experiment_opportunities"]["planned"] == protocol[
        "planned_resources"
    ]["physical_vessels_and_final_assays"]
    assert g2["provider_sessions"]["planned"] == protocol[
        "planned_resources"
    ]["provider_sessions"]
    assert g2["primitive_operation_ceiling"] == protocol["planned_resources"][
        "primitive_operation_ceiling"
    ]
    assert g2["projected_primitive_operations"] == protocol["planned_resources"][
        "observed_v0.4_projection"
    ]["primitive_operations"]
    assert g2["cells"] == {
        "planned": 20,
        "completed": 0,
        "right_censored": 0,
        "remaining": 20,
    }
    assert remaining == {
        "g0_new_physical_experiments": 0,
        "g2_v0_5_physical_experiment_opportunities": 120,
        "total": 120,
    }


def test_projected_arxiv_total_and_optional_experiments_are_separated() -> None:
    ledger = _load(LEDGER_PATH)
    accounting = ledger["scientific_experiment_accounting"]
    g2_v0_4 = ledger["experiment_layers"]["g2_v0_4_autonomous_development"]
    optional = ledger["optional_post_arxiv_experiments"]

    assert accounting["projected_arxiv_v1_total_after_g2_v0_5"] == (
        accounting["completed_or_audited_before_v0_5"]["total"]
        + accounting["required_remaining_for_arxiv_v1"]["total"]
    )
    assert accounting["projected_arxiv_v1_total_after_g2_v0_5"] == 29_760
    assert accounting["qualification_attempts_excluded_from_scientific_total"] == 2
    assert g2_v0_4["nonfinal_instrument_measurements"] == 164
    assert g2_v0_4["final_assays"] == 60
    assert g2_v0_4["total_measure_operations_including_final_assay"] == 224
    assert g2_v0_4["total_measure_operations_including_final_assay"] == (
        g2_v0_4["nonfinal_instrument_measurements"] + g2_v0_4["final_assays"]
    )
    assert all(not item["required_for_v1"] for item in optional.values())


def test_tracked_g0_evidence_hashes_match_the_ledger() -> None:
    ledger = _load(LEDGER_PATH)
    g0 = ledger["experiment_layers"]["g0_compiled_recipe"]
    foundation = ledger["foundation_qualification"]

    assert g0["formal_summary_file_sha256"]["v1_0"] == _sha256(
        ROOT / g0["formal_summary_paths"][0]
    )
    assert g0["formal_summary_file_sha256"]["v1_2"] == _sha256(
        ROOT / g0["formal_summary_paths"][1]
    )
    assert foundation["evidence_file_sha256"] == _sha256(
        ROOT / foundation["evidence_path"]
    )


def test_paper_scope_keeps_g2_primary_and_claims_bounded() -> None:
    ledger = _load(LEDGER_PATH)
    scope = ledger["paper_scope"]
    g2 = ledger["experiment_layers"][
        "g2_v0_5_fresh_trajectory_replication"
    ]

    assert scope["working_title"] == (
        "Experimental Intelligence in Executable Chemical Worlds"
    )
    assert scope["primary_interface"] == (
        "agent-directed closed-loop primitive experimentation"
    )
    assert scope["direct_g0_vs_g2_superiority_claim"] is False
    assert scope["general_population_prior_effect_claim"] is False
    assert "no pooled general-world p-value" in g2["claim_boundary"]
    assert len(ledger["publication_blockers"]) == 7


def test_active_manuscript_and_master_plan_use_the_frozen_scope() -> None:
    manuscript = (
        ROOT / "paper/experimental_intelligence_v1_manuscript.md"
    ).read_text(encoding="utf-8")
    master_plan = (
        ROOT
        / "workstreams/arxiv_v1/"
        "EXPERIMENTAL_INTELLIGENCE_V1_MASTER_PLAN_ZH.md"
    ).read_text(encoding="utf-8")

    assert manuscript.startswith(
        "# Experimental Intelligence in Executable Chemical Worlds"
    )
    assert "[PENDING G2 v0.5" in manuscript
    assert "No new G0 scientific experiment is required" in manuscript
    assert "20 G2 v0.5 cells" in manuscript
    assert "120 G2 experiment opportunities" in manuscript
    assert "29,640 existing + 120 new = 29,760" in master_plan
    assert "From Recipe Optimization" not in manuscript
    assert "From Recipe Optimization" not in master_plan


def test_all_tracked_evidence_and_execution_entrypoints_exist() -> None:
    ledger = _load(LEDGER_PATH)
    g0 = ledger["experiment_layers"]["g0_compiled_recipe"]
    g2_v0_4 = ledger["experiment_layers"]["g2_v0_4_autonomous_development"]
    g2_v0_5 = ledger["experiment_layers"][
        "g2_v0_5_fresh_trajectory_replication"
    ]

    paths = [
        ledger["foundation_qualification"]["evidence_path"],
        *g0["formal_summary_paths"],
        g2_v0_4["tracked_compact_report"],
        g2_v0_5["protocol"],
        g2_v0_5["runner"],
        g2_v0_5["launcher"],
        g2_v0_5["audit"],
    ]
    assert all((ROOT / path).is_file() for path in paths)
    assert g2_v0_5["physical_experiment_opportunities"]["planned"] == (
        g2_v0_5["cells"]["planned"] * 6
    )
    blocker_ids = [item["id"] for item in ledger["publication_blockers"]]
    assert blocker_ids == ["B1", "B2", "B3", "B4", "B5", "B6", "B7"]
