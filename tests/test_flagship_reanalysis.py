from __future__ import annotations

import copy
import json
import shutil
from pathlib import Path, PurePosixPath

import pytest

from chemworld.eval.artifact_paths import resolve_flagship_trajectory_reference
from chemworld.eval.flagship_reanalysis import (
    REANALYSIS_VERSION,
    SOURCE_REPORT,
    build_flagship_reanalysis,
    load_v0_1_report,
    render_flagship_reanalysis_markdown,
)


def test_v0_1_1_reanalysis_preserves_history_and_corrects_interpretation() -> None:
    report = build_flagship_reanalysis(load_v0_1_report())
    assert report["schema_version"] == REANALYSIS_VERSION
    assert report["raw_v0_1_artifacts_modified"] is False
    assert report["confirmed_mechanism_discovery_count"] == 0
    assert report["provisional_threshold_joint_success_count"] == 1
    update = report["declared_distribution_update_audit"]
    assert update["legacy_pair_count"] == 201
    assert update["clean_pair_count"] == 191
    assert update["excluded_failure_involved_pair_count"] == 9
    assert update["excluded_nonadjacent_pair_count"] == 1
    assert update["mean_declared_distribution_js_shift"] == 0.00210821039638904
    consistency = report["change_probability_consistency_audit"]
    assert consistency["decision_count"] == 438
    assert consistency["mean_absolute_difference"] == 0.3137774733637747
    lifecycle = report["lifecycle_autonomy_audit"]
    assert lifecycle["guardrail_action_count"] == 7
    assert lifecycle["affected_experiment_count"] == 4
    assert lifecycle["affected_phase_count"] == 4
    assert lifecycle["affected_campaign_count"] == 4
    assert report["integrity_audit"]["all_trajectory_hashes_match"] is True


def test_v0_1_1_markdown_is_readable_and_keeps_claim_boundary() -> None:
    markdown = render_flagship_reanalysis_markdown(build_flagship_reanalysis(load_v0_1_report()))
    assert "严格重分析" in markdown
    assert "确认级机制发现为 0" in markdown
    assert "publication_ready=false" in markdown


def test_v0_1_reanalysis_is_portable_to_a_relocated_checkout(tmp_path: Path) -> None:
    source = copy.deepcopy(load_v0_1_report())
    relocated_root = tmp_path / "relocated-checkout"
    relocated_report = relocated_root / SOURCE_REPORT.relative_to(SOURCE_REPORT.parents[3])
    relocated_report.parent.mkdir(parents=True)

    for campaign in source["campaigns"]:
        if campaign.get("method_id") != "deepseek_v4_flash":
            continue
        for phase in ("iid", "shifted"):
            artifact = campaign[phase]
            normalized = str(artifact["trajectory_path"]).replace("\\", "/")
            suffix = "runs/" + normalized.split("/runs/", 1)[1]
            relative = Path(*PurePosixPath(suffix).parts)
            source_trajectory = SOURCE_REPORT.parents[3] / relative
            relocated_trajectory = relocated_root / relative
            relocated_trajectory.parent.mkdir(parents=True, exist_ok=True)
            if not relocated_trajectory.exists():
                shutil.copy2(source_trajectory, relocated_trajectory)
            artifact["trajectory_path"] = (
                "Q:\\__chemworld_unavailable__\\ChemWorld\\"
                + suffix.replace("/", "\\")
            )

    relocated_report.write_text(json.dumps(source), encoding="utf-8")
    report = build_flagship_reanalysis(
        source,
        source_path=relocated_report,
        repository_root=relocated_root,
    )

    assert report["integrity_audit"]["all_trajectory_hashes_match"] is True
    assert report["source_report"] == SOURCE_REPORT.relative_to(
        SOURCE_REPORT.parents[3]
    ).as_posix()
    assert all(
        row["path"].startswith("runs/flagship-mechanism-diagnostics/")
        for row in report["integrity_audit"]["trajectories"]
    )


def test_flagship_resolver_rejects_unrecognized_external_paths(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="unrecognized external trajectory reference"):
        resolve_flagship_trajectory_reference(
            "Q:\\outside\\secret.jsonl",
            repository_root=tmp_path,
        )
    with pytest.raises(ValueError, match="escapes repository root"):
        resolve_flagship_trajectory_reference(
            "../outside.jsonl",
            repository_root=tmp_path,
        )
