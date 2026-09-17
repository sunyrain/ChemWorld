from __future__ import annotations

from scripts.author_experiment_1_rx_entity_repair import _pair_report


def test_pair_report_requires_both_anchors_and_behavioral_consequence() -> None:
    receipts = []
    for anchor in (0, 1):
        for category, base in ((0, 0.25), (1, 0.40)):
            for replicate, offset in enumerate((-0.005, 0.0, 0.005)):
                receipts.append(
                    {
                        "status": "completed",
                        "nuisance_anchor": anchor,
                        "target_category": category,
                        "replicate": replicate,
                        "allowed_metrics": {
                            "yield": base + offset,
                            "selectivity": base + 0.02 + offset,
                            "conversion": base + 0.04 + offset,
                            "byproduct_signal": base + 0.01 + offset,
                        },
                    }
                )

    report = _pair_report(
        receipts,
        (0, 1),
        minimum_mean=0.05,
        minimum_single=0.03,
        minimum_snr=2.0,
        minimum_consequence=0.05,
    )

    assert report["identifiable"] is True
    assert report["behaviorally_relevant"] is True
    assert len(report["anchors"]) == 2
