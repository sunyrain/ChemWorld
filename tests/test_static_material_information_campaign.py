from __future__ import annotations

import pytest

from chemworld.eval.static_material_information_campaign import (
    _bootstrap_interval,
    _interim_rule_preview,
    _summary,
)


def test_nominal_information_bootstrap_is_world_level_and_reproducible() -> None:
    values = [-0.02, 0.01, 0.08, 0.12, 0.15]

    interval = _bootstrap_interval(
        values,
        confidence=0.95,
        seed=17,
        draws=10_000,
        label="paired-world-test",
    )

    assert _summary(values)["mean"] == pytest.approx(0.068)
    assert interval[0] < 0.068 < interval[1]
    assert interval == _bootstrap_interval(
        values,
        confidence=0.95,
        seed=17,
        draws=10_000,
        label="paired-world-test",
    )


@pytest.mark.parametrize(
    ("interval", "classification"),
    [
        ((0.01, 0.20), "positive_information_value"),
        ((-0.20, -0.01), "harmful_information"),
        ((-0.01, 0.20), "inconclusive"),
    ],
)
def test_nominal_information_rule_preview(
    interval: tuple[float, float],
    classification: str,
) -> None:
    assert _interim_rule_preview(interval) == classification
