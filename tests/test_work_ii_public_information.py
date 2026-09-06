"""Public-packet reanalysis must retain missing measurements and fixed denominators."""

from scripts.analyze_work_ii_public_information import METRICS, analyze


def test_missing_metric_stays_in_scheduled_denominator():
    evidence = [
        {
            "reference_linear_observations": dict.fromkeys(METRICS, 0.2),
            "target_observations": dict.fromkeys(METRICS, 0.3),
        }
        for _ in range(8)
    ]
    del evidence[0]["target_observations"]["score"]
    result = analyze([{"evidence": evidence}])
    assert result["scheduled_metric_pairs"] == 32
    assert result["completed_metric_pairs"] == 31
    assert len(result["failures"]) == 1
    score = next(r for r in result["summaries"] if r["world"] is None and r["metric"] == "score")
    assert (score["scheduled"], score["completed"]) == (8, 7)
    assert result["formal_qualification"] is False
    assert result["provider_calls"] == 0
