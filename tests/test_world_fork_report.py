from __future__ import annotations

import json
from pathlib import Path

from scripts.summarize_work_i_world_fork import (
    build_human_certificate,
    build_machine_certificate,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "workstreams/arxiv_v1/reports/work-i-world-fork-qualification-v0.1.json"
MACHINE = ROOT / "workstreams/arxiv_v1/reports/work-i-world-fork-certificate-v0.1.json"
HUMAN = ROOT / "workstreams/arxiv_v1/reports/work-i-world-fork-certificate-v0.1.md"


def test_world_fork_certificates_rebuild_from_frozen_formal_report() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    rebuilt = build_machine_certificate(source, source_path=SOURCE)
    committed = json.loads(MACHINE.read_text(encoding="utf-8"))
    assert committed == rebuilt
    assert HUMAN.read_text(encoding="utf-8") == build_human_certificate(rebuilt)


def test_world_fork_certificate_has_complete_success_counts_and_boundaries() -> None:
    certificate = json.loads(MACHINE.read_text(encoding="utf-8"))
    assert certificate["design"] == {
        "executions_per_variant": 2,
        "intervention_class_count": 2,
        "parent_child_pair_count": 6,
        "provider_call_count": 0,
        "same_public_midpoint_action_sequence_within_pair": True,
        "seed_count_per_class": 3,
        "trace_count": 24,
        "world_variants_per_pair": 2,
    }
    assert certificate["result"]["pair_pass_count"] == 6
    assert all(value == 6 for value in certificate["result"]["gate_pass_counts"].values())
    assert all(
        pair["public_component_count"] == 9
        and pair["public_invariant_component_count"] == 9
        and pair["identity_leakage_finding_count"] == 0
        for pair in certificate["result"]["pairs"]
    )
    assert certificate["claim_boundary"]["agent_performance_claim"] is False
    assert certificate["claim_boundary"]["arbitrary_world_dsl_claim"] is False
    assert certificate["claim_boundary"]["physical_laboratory_transfer_claim"] is False
