from dataclasses import replace
from math import nan

import pytest

from chemworld.eval.work_ii_public_partition_reference import (
    PublicContact,
    forward,
    invert_power_exponent,
)


def contact() -> PublicContact:
    return PublicContact(2.0, 298.15, 0.0, 0.0, 0.02, 0.02)


def test_known_contact_and_continuous_phase_tie() -> None:
    # D=1.5, equilibrium fraction=0.6, efficiency=.75, entrainment=.01.
    result = forward(contact(), 1.0)
    assert result["coefficient"] == pytest.approx(1.5)
    assert result["organic_fraction"] == pytest.approx(0.4555)
    assert result["aqueous_fraction"] == pytest.approx(0.5445)
    assert invert_power_exponent(contact(), 0.4555) == pytest.approx(1.0)


def test_aqueous_continuous_phase_removes_entrained_organic_product() -> None:
    value = replace(contact(), aqueous_volume_L=0.03)
    # Equilibrium fraction=.5; organic carries .375 before its .01 loss.
    result = forward(value, 1.0)
    assert result["organic_fraction"] == pytest.approx(0.37125)
    assert sum(result[k] for k in ("organic_fraction", "aqueous_fraction")) == pytest.approx(1)
    assert invert_power_exponent(value, 0.37125) == pytest.approx(1)


def test_unit_reference_coefficient_has_no_exponent_information() -> None:
    value = replace(contact(), reference_coefficient=1)
    assert forward(value, 1) == forward(value, 2)
    with pytest.raises(ValueError, match="no exponent information"):
        invert_power_exponent(value, 0.4)


def test_clipped_coefficient_does_not_manufacture_unique_recovery() -> None:
    value = replace(contact(), reference_coefficient=0.01)
    fraction = forward(value, 2)["organic_fraction"]
    assert fraction == forward(value, 3)["organic_fraction"]
    with pytest.raises(ValueError, match="floor"):
        invert_power_exponent(value, fraction)


def test_invalid_observation_and_inputs_are_explicit_failures() -> None:
    with pytest.raises(ValueError, match="finite"):
        replace(contact(), reference_coefficient=nan)
    with pytest.raises(ValueError, match="positive"):
        replace(contact(), aqueous_volume_L=0)
    with pytest.raises(ValueError, match="invertible"):
        invert_power_exponent(contact(), 0.99)
