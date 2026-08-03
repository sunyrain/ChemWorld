from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

from scripts.render_work_i_figure_1 import (
    GATE_ORDER,
    MANIFEST_PATH,
    OUTPUT_DIR,
    OUTPUT_STEM,
    load_figure_inputs,
    manifest_sha256,
)

ROOT = Path(__file__).resolve().parents[1]


def _manifest() -> dict[str, object]:
    payload = json.loads((ROOT / MANIFEST_PATH).read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_figure_inputs_are_exactly_the_frozen_f_census() -> None:
    inputs = load_figure_inputs(ROOT)
    certificate = inputs["certificate"]
    design = certificate["design"]
    assert design == {
        "executions_per_variant": 2,
        "intervention_class_count": 2,
        "parent_child_pair_count": 6,
        "provider_call_count": 0,
        "same_public_midpoint_action_sequence_within_pair": True,
        "seed_count_per_class": 3,
        "trace_count": 24,
        "world_variants_per_pair": 2,
    }
    assert [case["case_id"] for case in inputs["cases"]] == [
        "partition-constitutive-law-family",
        "electrochemical-material-law-counterfactual",
    ]
    assert all(case["pair_pass_count"] == 3 for case in inputs["cases"])
    assert inputs["gate_pass_counts"] == dict.fromkeys(GATE_ORDER, 6)
    assert inputs["public_component_count"] == 9


def test_manifest_is_self_hashed_and_binds_all_outputs() -> None:
    manifest = _manifest()
    assert manifest["manifest_sha256"] == manifest_sha256(manifest)
    assert manifest["figure_id"] == "F1"
    assert manifest["owner_task"] == "W1-P02"
    assert manifest["figure_system_sha256"] == (
        "c7abb490d247121e47fe20efca909df28527de64e7d1110699ccd104f6873643"
    )
    outputs = manifest["outputs"]
    assert [row["format"] for row in outputs] == ["svg", "pdf", "png"]
    for row in outputs:
        path = ROOT / row["path"]
        assert path.stat().st_size == row["bytes"]
        assert _sha256(path) == row["sha256"]
    source_bindings = manifest["source_bindings"]
    assert len(source_bindings) == 5
    for binding in source_bindings:
        assert _sha256(ROOT / binding["path"]) == binding["sha256"]


def test_outputs_meet_editability_embedding_and_final_size_rules() -> None:
    output_dir = ROOT / OUTPUT_DIR
    svg = (output_dir / f"{OUTPUT_STEM}.svg").read_text(encoding="utf-8")
    pdf = (output_dir / f"{OUTPUT_STEM}.pdf").read_bytes()
    png = (output_dir / f"{OUTPUT_STEM}.png").read_bytes()
    assert "<text" in svg
    assert "ChemWorld apparatus and controlled world forks" not in svg
    assert pdf.startswith(b"%PDF")
    assert b"/FontFile2" in pdf
    assert png[:8] == b"\x89PNG\r\n\x1a\n"
    assert int.from_bytes(png[16:20], "big") == 2124
    assert int.from_bytes(png[20:24], "big") == 1560


def test_manifest_preserves_panel_roles_counts_and_claim_boundary() -> None:
    manifest = _manifest()
    assert manifest["panel_roles"] == {
        "A": "agent_world_interaction_loop",
        "B": "identity_authority_evidence_resource_and_replay_controls",
        "C": "single_private_component_forks_with_public_invariance",
        "D": "six_pair_twenty_four_trace_qualification_gates",
    }
    assert manifest["evidence_census"] == {
        "intervention_classes": 2,
        "seeds_per_class": 3,
        "parent_child_pairs": 6,
        "traces": 24,
        "executions_per_variant": 2,
        "public_components_invariant_per_pair": 9,
        "provider_calls": 0,
        "all_six_pairs_pass_all_six_gates": True,
    }
    assert manifest["claim_boundary"] == {
        "programmable_world_apparatus": True,
        "agent_performance_claim": False,
        "rule_adaptation_claim": False,
        "arbitrary_world_dsl_claim": False,
        "physical_laboratory_transfer_claim": False,
    }

    tampered = deepcopy(manifest)
    tampered["evidence_census"]["traces"] = 25
    assert tampered["manifest_sha256"] != manifest_sha256(tampered)
