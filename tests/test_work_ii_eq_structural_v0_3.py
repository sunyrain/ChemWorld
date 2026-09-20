from __future__ import annotations

import scripts.run_work_ii_eq_bounded_equilibrium_v2 as canonical
import scripts.run_work_ii_eq_structural_v0_3 as eq


def test_v03_uses_only_canonical_k1_q_k2() -> None:
    config = eq.load_config()
    validated = eq.validate_design(config)

    assert config["posttest_stages"] == ["K1", "Q", "K2"]
    assert config["counts"]["posttests"] == 45
    assert len(validated["schedule"]) == 15
    assert eq.K1 == canonical.K1
    assert eq.Q_PROMPT == canonical.Q_PROMPT
    assert eq.K2 == canonical.K2
    assert "EQS" not in eq.SYSTEM
    assert "network_family" not in eq.K1
    assert "aqueous_ion_pair_intermediate" not in eq.K1


def test_v03_keeps_frozen_s_queries_and_matched_priors() -> None:
    config = eq.load_config()
    rows = eq.queries(config)

    assert len(rows) == 12
    assert [row["query_id"] for row in rows] == [f"Q{index:02d}" for index in range(1, 13)]
    for world in config["worlds"]:
        world_id = world["world_id"]
        assert eq.public_prior(config, world_id, "Opaque") is None
        aligned = eq.public_prior(config, world_id, "Aligned")
        misindexed = eq.public_prior(config, world_id, "MisIndexed")
        assert aligned is not None and misindexed is not None
        assert aligned.keys() == misindexed.keys()
        assert aligned != misindexed


def test_v03_rejects_noncanonical_posttest() -> None:
    assert eq.validate_posttest("EQS", {}, [])["valid"] is False


def test_v03_external_audit_is_not_a_participant_question() -> None:
    config = eq.load_config()
    audit = config["canonical_relaunch"]["mechanism_evaluation"]

    assert audit["primary_participant_artifact"] == "sealed_K1_open_mechanistic_report"
    assert audit["participant_candidate_labels_exposed"] is False
    assert audit["primary_family_accuracy_authorized"] is False
    assert audit["single_composite_score_authorized"] is False
