from __future__ import annotations

import json

import pytest

from chemworld.physchem.maturity import ModelAdapterManifest, validate_model_card
from chemworld.physchem.transfer_adapter_manifest import (
    OWNED_PATHS,
    TransferUnitProvider,
    transfer_adapter_manifest,
    transfer_provider_contract,
)
from chemworld.physchem.transfer_units import (
    IDAES_COMMIT,
    TRANSFER_MODEL_ID,
    TransferEquipmentSpec,
    TransferRequest,
    simulate_transfer,
    transfer_unit_model_card,
)


def _request(
    *,
    source_amounts: dict[str, float] | None = None,
    source_volume_L: float = 10.0,
    transfer_fraction: float = 0.8,
    heel_L: float = 0.0,
    hold_up_L: float = 0.0,
    max_transfer_L: float | None = None,
    initial_line_amounts: dict[str, float] | None = None,
    initial_line_volume_L: float = 0.0,
    flush_amounts: dict[str, float] | None = None,
    flush_volume_L: float = 0.0,
) -> TransferRequest:
    return TransferRequest(
        source_amounts_mol=source_amounts or {"product": 10.0, "solvent": 90.0},
        source_volume_L=source_volume_L,
        transfer_fraction=transfer_fraction,
        equipment=TransferEquipmentSpec(
            source_heel_L=heel_L,
            line_holdup_L=hold_up_L,
            max_transfer_volume_L=max_transfer_L,
            max_flush_volume_L=5.0,
        ),
        initial_line_amounts_mol=initial_line_amounts or {},
        initial_line_volume_L=initial_line_volume_L,
        flush_amounts_mol=flush_amounts or {},
        flush_volume_L=flush_volume_L,
    )


def _assert_closed(result) -> None:
    assert result.material_balance_error_mol <= 1.0e-10
    assert result.volume_balance_error_L <= 1.0e-10
    assert max(result.component_balance_error_mol.values(), default=0.0) <= 1.0e-10


def test_zero_holdup_delivers_every_withdrawn_component() -> None:
    result = simulate_transfer(_request())
    assert result.withdrawn_source_volume_L == pytest.approx(8.0)
    assert result.target_delivered_volume_L == pytest.approx(8.0)
    assert result.final_line_volume_L == pytest.approx(0.0)
    assert result.source_remaining_amounts_mol == pytest.approx(
        {"product": 2.0, "solvent": 18.0}
    )
    assert result.target_delivered_amounts_mol == pytest.approx(
        {"product": 8.0, "solvent": 72.0}
    )
    assert result.source_delivery_fraction_of_withdrawn == pytest.approx(1.0)
    _assert_closed(result)


def test_source_heel_and_equipment_capacity_clip_withdrawal_explicitly() -> None:
    heel = simulate_transfer(
        _request(transfer_fraction=1.0, heel_L=2.0, max_transfer_L=None)
    )
    assert heel.requested_transfer_volume_L == pytest.approx(10.0)
    assert heel.withdrawn_source_volume_L == pytest.approx(8.0)
    assert heel.source_remaining_volume_L == pytest.approx(2.0)
    assert "clipped" in heel.warnings[0]
    _assert_closed(heel)

    capacity = simulate_transfer(
        _request(transfer_fraction=1.0, heel_L=0.0, max_transfer_L=6.0)
    )
    assert capacity.withdrawn_source_volume_L == pytest.approx(6.0)
    assert capacity.source_remaining_volume_L == pytest.approx(4.0)
    _assert_closed(capacity)


def test_empty_line_holdup_retains_tail_of_source_slug() -> None:
    result = simulate_transfer(
        _request(source_volume_L=5.0, transfer_fraction=1.0, hold_up_L=2.0)
    )
    assert result.withdrawn_source_volume_L == pytest.approx(5.0)
    assert result.target_delivered_volume_L == pytest.approx(3.0)
    assert result.final_line_volume_L == pytest.approx(2.0)
    assert result.final_line_volume_by_origin_L["source"] == pytest.approx(2.0)
    assert result.source_delivery_fraction_of_withdrawn == pytest.approx(0.6)
    assert result.target_delivered_amounts_mol == pytest.approx(
        {"product": 6.0, "solvent": 54.0}
    )
    assert result.final_line_amounts_mol == pytest.approx(
        {"product": 4.0, "solvent": 36.0}
    )
    _assert_closed(result)


def test_initial_line_inventory_is_displaced_before_source_slug() -> None:
    result = simulate_transfer(
        _request(
            source_amounts={"product": 5.0},
            source_volume_L=5.0,
            transfer_fraction=0.2,
            hold_up_L=2.0,
            initial_line_amounts={"wash_solvent": 2.0},
            initial_line_volume_L=2.0,
        )
    )
    assert result.target_delivered_volume_L == pytest.approx(1.0)
    assert result.target_delivered_amounts_mol == pytest.approx({"wash_solvent": 1.0})
    assert result.source_amounts_delivered_mol == {}
    assert result.source_amounts_retained_in_line_mol == pytest.approx({"product": 1.0})
    assert result.final_line_amounts_mol == pytest.approx(
        {"wash_solvent": 1.0, "product": 1.0}
    )
    _assert_closed(result)


def test_flush_displaces_retained_source_without_destroying_inventory() -> None:
    result = simulate_transfer(
        _request(
            source_amounts={"product": 5.0},
            source_volume_L=5.0,
            transfer_fraction=1.0,
            hold_up_L=2.0,
            flush_amounts={"flush_solvent": 2.0},
            flush_volume_L=2.0,
        )
    )
    assert result.target_delivered_volume_L == pytest.approx(5.0)
    assert result.target_delivered_amounts_mol == pytest.approx({"product": 5.0})
    assert result.final_line_amounts_mol == pytest.approx({"flush_solvent": 2.0})
    assert result.final_line_volume_by_origin_L["flush"] == pytest.approx(2.0)
    assert result.source_delivery_fraction_of_withdrawn == pytest.approx(1.0)
    assert result.overall_source_delivery_fraction == pytest.approx(1.0)
    _assert_closed(result)


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"source_volume_L": 0.0}, "source_volume_L"),
        ({"transfer_fraction": 1.1}, "transfer_fraction"),
        ({"heel_L": 11.0}, "source_heel_L"),
        (
            {"hold_up_L": 1.0, "initial_line_volume_L": 2.0, "initial_line_amounts": {"x": 1.0}},
            "exceeds line_holdup",
        ),
        ({"flush_volume_L": 1.0}, "flush_amounts_mol"),
    ],
)
def test_invalid_transfer_domains_fail_explicitly(
    kwargs: dict[str, object],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        _request(**kwargs)  # type: ignore[arg-type]


def test_provider_uses_wf00_contract_for_success_and_failure() -> None:
    provider = TransferUnitProvider()
    success = provider.evaluate({"request": _request(hold_up_L=1.0)})
    assert success.success is True
    assert success.outputs["transfer_result"]["model_id"] == TRANSFER_MODEL_ID
    assert success.diagnostics["material_balance_error_mol"] <= 1.0e-10
    assert success.diagnostics["final_line_volume_L"] == pytest.approx(1.0)

    failure = provider.evaluate({"request": {}})
    assert failure.success is False
    assert failure.failure_reason == "request must be a TransferRequest"
    assert failure.outputs == {}


def test_model_card_and_adapter_are_bounded_hash_verified_evidence() -> None:
    card = transfer_unit_model_card()
    assert validate_model_card(card) == []
    assert card.model_id == TRANSFER_MODEL_ID
    assert any(IDAES_COMMIT in reference for reference in card.reference_reading)
    assert any("not plant piping design" in note for note in card.model_limit_notes)

    contract = transfer_provider_contract()
    manifest = transfer_adapter_manifest()
    assert manifest.provider_contract == contract
    assert manifest.owned_paths == OWNED_PATHS
    assert manifest.replaces_model_ids == ()
    payload = manifest.to_dict()
    assert ModelAdapterManifest.from_dict(payload).to_dict() == payload
    payload["adapter_version"] = "tampered"
    with pytest.raises(ValueError, match="hash mismatch"):
        ModelAdapterManifest.from_dict(payload)


def test_transfer_result_serialization_is_deterministic() -> None:
    request = _request(
        hold_up_L=1.0,
        flush_amounts={"flush_solvent": 0.5},
        flush_volume_L=0.5,
    )
    left = json.dumps(simulate_transfer(request).to_dict(), sort_keys=True)
    right = json.dumps(simulate_transfer(request).to_dict(), sort_keys=True)
    assert left == right
