from __future__ import annotations

from chemworld.eval.flagship_reanalysis import (
    REANALYSIS_VERSION,
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
