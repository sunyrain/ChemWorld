from __future__ import annotations

import pytest

from chemworld.eval.static_optimization_campaign import (
    _algorithm_role,
    _bootstrap_interval,
    _summary,
)


def test_campaign_summary_treats_worlds_as_bootstrap_units() -> None:
    values = [0.1, 0.2, 0.3, 0.4]

    interval = _bootstrap_interval(
        values,
        seed=7,
        draws=10_000,
        label="test",
    )

    assert _summary(values)["mean"] == pytest.approx(0.25)
    assert interval[0] < 0.25 < interval[1]
    assert interval == _bootstrap_interval(
        values,
        seed=7,
        draws=10_000,
        label="test",
    )


@pytest.mark.parametrize(
    ("condition", "role"),
    [
        ("opaque_score_and_public_measurements", "information_matched"),
        (
            "privileged_nominal_material_descriptors_calibration",
            "privileged_calibration",
        ),
        (
            "negative_control_shuffled_material_descriptors",
            "negative_control",
        ),
    ],
)
def test_campaign_summary_classifies_baseline_information(
    condition: str,
    role: str,
) -> None:
    assert _algorithm_role(condition) == role
