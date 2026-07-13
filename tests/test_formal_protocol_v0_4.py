from __future__ import annotations

import copy
import json
import subprocess
from pathlib import Path

import pytest

from chemworld.eval.formal_protocol_v0_4 import (
    DEFAULT_PRIVATE_MANIFEST_PATH,
    FormalProtocolError,
    audit_formal_protocol,
    initialize_private_bench_manifest,
    load_formal_protocol,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "workstreams" / "benchmark_v1" / "reports" / "formal-protocol-v0.4.json"


def test_default_private_manifest_uses_git_common_directory() -> None:
    raw = subprocess.check_output(
        ["git", "rev-parse", "--git-common-dir"],
        cwd=ROOT,
        text=True,
    ).strip()
    common = Path(raw)
    if not common.is_absolute():
        common = (ROOT / common).resolve()
    expected = (
        common
        / "chemworld-private"
        / "formal-protocol-v0.4.2"
        / "bench-manifest.json"
    )
    assert expected == DEFAULT_PRIVATE_MANIFEST_PATH


@pytest.fixture()
def sealed_protocol(tmp_path: Path) -> tuple[dict[str, object], Path]:
    protocol = copy.deepcopy(load_formal_protocol())
    private_path = tmp_path / "private-bench.json"
    summary = initialize_private_bench_manifest(protocol, path=private_path)
    protocol["private_bench_manifest"]["commitment_sha256"] = summary[
        "commitment_sha256"
    ]
    return protocol, private_path


def test_formal_protocol_freezes_unseen_cohort_without_public_bench_values(
    sealed_protocol: tuple[dict[str, object], Path],
) -> None:
    protocol, private_path = sealed_protocol
    report = audit_formal_protocol(protocol, private_manifest_path=private_path)
    assert report["controls_ready"] is True
    assert report["formal_results_present"] is False
    assert report["benchmark_claim_allowed"] is False
    assert report["formal_core_tasks"] == [
        "partition-discovery",
        "reaction-to-crystallization",
        "reaction-to-distillation",
        "flow-reaction-optimization",
    ]
    assert report["exploratory_tasks"] == [
        "electrochemical-conversion",
        "equilibrium-characterization",
    ]
    assert report["experiment_budget"] == 40
    assert report["checkpoints"] == [4, 8, 12, 20, 40]
    assert report["private_bench"]["verified"] is True
    assert report["private_bench"]["disjoint_and_sealed"] is True
    assert report["private_bench"]["paired_seed_count"] == 100
    assert report["private_bench"]["raw_seed_values_reported"] is False
    assert report["private_bench"]["raw_world_parameters_reported"] is False


def test_public_seed_namespaces_are_new_and_disjoint(
    sealed_protocol: tuple[dict[str, object], Path],
) -> None:
    protocol, private_path = sealed_protocol
    report = audit_formal_protocol(protocol, private_manifest_path=private_path)
    summary = report["public_split_summary"]
    assert summary == {
        "train": {"seed_count": 100, "minimum_seed": 10000, "maximum_seed": 10099},
        "dev": {"seed_count": 20, "minimum_seed": 11000, "maximum_seed": 11019},
        "reference_search": {
            "seed_count": 100,
            "minimum_seed": 12000,
            "maximum_seed": 12099,
        },
    }
    assert report["controls"]["public_seed_splits_were_outside_quarantine_inventory"]


@pytest.mark.parametrize(
    ("path", "value", "control"),
    [
        (
            ("campaign_contract", "complete_experiments_per_cell"),
            39,
            "budget_checkpoints_and_stopping_are_frozen",
        ),
        (
            ("campaign_contract", "anytime_checkpoints"),
            [4, 8, 20, 40],
            "budget_checkpoints_and_stopping_are_frozen",
        ),
        (
            ("split_contract", "bench", "paired_seed_count"),
            20,
            "bench_public_contract_contains_no_raw_seed_or_world_values",
        ),
        (
            ("access_state", "bench_run_started"),
            True,
            "bench_access_state_is_unrun_and_untuned",
        ),
        (
            ("failure_policy", "silent_drop_or_imputation"),
            "allowed",
            "failure_policy_is_fail_closed",
        ),
    ],
)
def test_semantic_tampering_fails_closed(
    sealed_protocol: tuple[dict[str, object], Path],
    path: tuple[str, ...],
    value: object,
    control: str,
) -> None:
    protocol, private_path = sealed_protocol
    target: dict[str, object] = protocol
    for key in path[:-1]:
        target = target[key]  # type: ignore[assignment]
    target[path[-1]] = value
    report = audit_formal_protocol(protocol, private_manifest_path=private_path)
    assert report["controls_ready"] is False
    assert report["controls"][control] is False


def test_raw_public_bench_seed_is_rejected(
    sealed_protocol: tuple[dict[str, object], Path],
) -> None:
    protocol, private_path = sealed_protocol
    protocol["split_contract"]["bench"]["base_seeds"] = [987654321]
    report = audit_formal_protocol(protocol, private_manifest_path=private_path)
    assert report["controls_ready"] is False
    assert (
        report["controls"][
            "bench_public_contract_contains_no_raw_seed_or_world_values"
        ]
        is False
    )


def test_public_split_overlap_is_rejected(
    sealed_protocol: tuple[dict[str, object], Path],
) -> None:
    protocol, private_path = sealed_protocol
    protocol["split_contract"]["dev"]["base_seeds"] = {
        "start": 10090,
        "stop_inclusive": 10109,
    }
    report = audit_formal_protocol(protocol, private_manifest_path=private_path)
    assert report["controls_ready"] is False
    assert report["controls"]["public_seed_splits_are_well_formed_and_disjoint"] is False


def test_backend_and_p0_hash_tampering_is_rejected(
    sealed_protocol: tuple[dict[str, object], Path],
) -> None:
    protocol, private_path = sealed_protocol
    protocol["backend_binding"]["backend_semantic_sha256"] = "a" * 64
    protocol["p0_evidence_bindings"][0]["sha256"] = "b" * 64
    report = audit_formal_protocol(protocol, private_manifest_path=private_path)
    assert report["controls_ready"] is False
    assert report["controls"]["backend_release_is_exact_and_ready"] is False
    assert report["controls"]["all_p0_evidence_is_hash_bound_and_ready"] is False


def test_protocol_change_invalidates_existing_private_precommit(
    sealed_protocol: tuple[dict[str, object], Path],
) -> None:
    protocol, private_path = sealed_protocol
    protocol["research_question"] = "changed after sealing"
    report = audit_formal_protocol(protocol, private_manifest_path=private_path)
    assert report["controls_ready"] is False
    assert report["private_bench"]["verified"] is True
    assert report["private_bench"]["disjoint_and_sealed"] is False


def test_missing_private_manifest_fails_closed() -> None:
    protocol = load_formal_protocol()
    report = audit_formal_protocol(protocol, private_manifest_path=None)
    assert report["controls_ready"] is False
    assert report["controls"]["private_manifest_commitment_is_verified"] is False
    assert report["controls"]["private_bench_is_disjoint_and_sealed"] is False


def test_initializer_refuses_to_overwrite_private_cohort(tmp_path: Path) -> None:
    protocol = load_formal_protocol()
    private_path = tmp_path / "private-bench.json"
    initialize_private_bench_manifest(protocol, path=private_path)
    with pytest.raises(FormalProtocolError, match="refusing overwrite"):
        initialize_private_bench_manifest(protocol, path=private_path)


def test_checked_in_audit_report_is_nonclaiming_and_contains_no_private_values() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert report["controls_ready"] is True
    assert report["formal_results_present"] is False
    assert report["benchmark_claim_allowed"] is False
    assert report["private_bench"]["verified"] is True
    assert report["private_bench"]["disjoint_and_sealed"] is True
    assert report["private_bench"]["raw_seed_values_reported"] is False
    assert report["private_bench"]["raw_world_parameters_reported"] is False
    assert "base_seeds" not in report["private_bench"]
    assert "pairs" not in report["private_bench"]
