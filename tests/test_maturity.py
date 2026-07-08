from __future__ import annotations

import gymnasium as gym
import pytest

import chemworld  # noqa: F401
from chemworld.physchem import (
    MaturityLevel,
    ModelCard,
    ValidationEvidence,
    model_card_template_map,
    validate_model_card,
)
from chemworld.tasks import get_task, list_tasks


def test_maturity_levels_are_machine_readable() -> None:
    assert [level.value for level in MaturityLevel] == [
        "proxy",
        "lite",
        "reference_validated",
        "professional_candidate",
        "professional",
    ]
    assert MaturityLevel.normalize("lite") is MaturityLevel.LITE
    with pytest.raises(ValueError, match="unknown maturity level"):
        MaturityLevel.normalize("demo")


def test_model_card_templates_cover_professional_modules() -> None:
    templates = model_card_template_map()
    assert {
        "properties",
        "eos",
        "phase_equilibrium",
        "equilibrium_chemistry",
        "reaction_kinetics",
        "reactors",
        "separations",
        "transport",
        "spectroscopy_instruments",
    }.issubset(templates)
    for template in templates.values():
        payload = template.to_dict()
        assert "validation_evidence" in payload["required_sections"]
        assert payload["reference_targets"]


def test_model_card_validation_blocks_unsupported_professional_claims() -> None:
    with pytest.raises(ValueError, match="validation_evidence"):
        ModelCard(
            model_id="bad_professional_claim",
            module_id="eos",
            title="Bad claim",
            maturity=MaturityLevel.PROFESSIONAL,
            summary="Missing evidence.",
            validity_limits=("narrow",),
        )

    proxy_card = ModelCard(
        model_id="separation_proxy",
        module_id="separations",
        title="Separation proxy",
        maturity=MaturityLevel.PROXY,
        summary="Qualitative proxy.",
    )
    assert validate_model_card(proxy_card) == [
        "proxy model cards must include model_limit_notes"
    ]

    professional_card = ModelCard(
        model_id="validated_ideal_vle",
        module_id="phase_equilibrium",
        title="Validated ideal VLE",
        maturity=MaturityLevel.PROFESSIONAL_CANDIDATE,
        summary="Controlled ideal VLE case.",
        validity_limits=("ideal binary mixture only",),
        failure_modes=("nonideal mixtures",),
        reference_reading=("reference_repos/thermo/thermo/property_package.py",),
        validation_evidence=(
            ValidationEvidence(
                evidence_id="thermo-ideal-vle",
                evidence_type="optional_reference_test",
                description="Ideal VLE comparison against thermo.",
                status="passing",
                reference_backend="thermo",
                command_or_path="tests/reference/test_optional_reference_backends.py",
                tolerance="rtol=1e-11",
            ),
        ),
    )
    assert validate_model_card(professional_card) == []


def test_task_maturity_metadata_is_public_and_policy_checked() -> None:
    reaction = get_task("reaction-optimization-standard")
    reaction_payload = reaction.to_dict()
    assert reaction_payload["physics_maturity"] == "lite"
    assert reaction_payload["proxy_allowed"] is False
    assert all(
        module["level"] != "proxy"
        for module in reaction_payload["kernel_maturity"]["modules"]
    )

    distillation = get_task("reaction-to-distillation")
    distillation_payload = distillation.to_dict()
    assert distillation_payload["physics_maturity"] == "lite"
    assert distillation_payload["proxy_allowed"] is False
    assert any(
        module["module_id"] == "distillation"
        and module["level"] == "reference_validated"
        and "vle_shortcut_distillation" in module["model_ids"]
        for module in distillation_payload["kernel_maturity"]["modules"]
    )

    for task in list_tasks():
        payload = task.to_dict()
        if payload["proxy_allowed"]:
            assert set(payload["tags"]).intersection(
                {"teaching", "smoke", "exploratory", "education"}
            )


def test_env_task_info_exposes_maturity_metadata() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=0)
    try:
        _, info = env.reset(seed=0)
        assert info["physics_maturity"] == "proxy"
        assert info["proxy_allowed"] is True
        assert any(
            module["module_id"] == "separations" and module["level"] == "proxy"
            for module in info["kernel_maturity"]["modules"]
        )
    finally:
        env.close()
