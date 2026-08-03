from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from chemworld.agents.known_policy import (
    DEFAULT_CONTRACT_PATH,
    DEFAULT_QUALIFICATION_REPORT_PATH,
    DEFAULT_THRESHOLD_BINDING_PATH,
    KnownPolicyAgent,
    KnownPolicyContractError,
    KnownPolicyExecutionError,
    load_known_policy_artifacts,
)
from chemworld.campaign_resources import CampaignResourceCard
from chemworld.data.logging import load_jsonl
from chemworld.eval.known_policy_contract import PROBE_SCHEDULE
from chemworld.eval.known_policy_threshold import SOURCE_PATHS
from chemworld.eval.runner import run_agent

ROOT = Path(__file__).resolve().parents[1]


def _task_info(material_information: Any = None) -> dict[str, Any]:
    return {
        "task_id": "electrochemical-conversion",
        "episode_mode": "campaign",
        "electrochemical_workflow_mode": "autonomous_open_v1",
        "allowed_operations": [
            "add_reagent",
            "add_solvent",
            "discard_batch",
            "electrolyze",
            "measure",
            "set_potential",
            "terminate",
        ],
        "allowed_instruments": ["final_assay", "ph_meter", "uvvis"],
        "material_information": material_information,
    }


def _committed_info(action: dict[str, Any]) -> dict[str, Any]:
    discarded = action.get("operation") == "discard_batch"
    assayed = action == {"operation": "measure", "instrument": "final_assay"}
    return {
        "transaction_status": "committed",
        "experiment_ended": discarded or assayed,
        "batch_discarded": discarded,
    }


def _first_lifecycle(
    policy_id: str, diagnostic: float | None = None
) -> tuple[KnownPolicyAgent, list[dict[str, Any]]]:
    agent = KnownPolicyAgent(policy_id)
    agent.reset(_task_info({"mode": "must_not_be_read"}), seed=13)
    actions: list[dict[str, Any]] = []
    while True:
        action = agent.act([])
        actions.append(action)
        observation = (
            {"conversion": diagnostic}
            if action == {"operation": "measure", "instrument": "uvvis"}
            else {}
        )
        agent.update(action, observation, 0.0, _committed_info(action))
        if _committed_info(action)["experiment_ended"]:
            return agent, actions


def _prefix() -> list[dict[str, Any]]:
    probe = PROBE_SCHEDULE[0]
    return [
        {"operation": "add_solvent", "volume_L": 0.025, "solvent": probe.solvent},
        {"operation": "add_reagent", "amount_mol": probe.reagent_amount_mol},
        {
            "operation": "set_potential",
            "potential_V": probe.potential_V,
            "current_mA": probe.current_mA,
            "electrolyte_profile": probe.electrolyte_profile,
        },
        {"operation": "electrolyze", "duration_s": probe.probe_duration_s},
    ]


def _nonformal_smoke_resource_card() -> CampaignResourceCard:
    return CampaignResourceCard(
        card_id="work-i-v04-nonformal-smoke-v1",
        operation_attempt_limit=48,
        vessel_start_limit=6,
        final_assay_limit=6,
        nonfinal_instrument_use_limit=6,
        stock_limits={"reagent_mol": 0.10, "solvent_L": 0.16},
        per_instrument_limits={"uvvis": 6},
        metadata={"role": "V04_nonformal_integration_smoke"},
    )


def test_artifact_chain_is_frozen_and_tamper_evident(tmp_path: Path) -> None:
    artifacts = load_known_policy_artifacts(ROOT)
    assert artifacts.contract_sha256 == (
        "79681abfa92af758af8326db1727b865376ad0da192ea13552b68fd94a66dd45"
    )
    assert artifacts.threshold_binding_sha256 == (
        "8a55b713ca900a644a301ecd8e83a0a686f9a28b3f60a18a85a4e57b66288c6a"
    )
    assert artifacts.threshold == 0.007984561379998922

    copied_paths = {
        DEFAULT_CONTRACT_PATH,
        DEFAULT_THRESHOLD_BINDING_PATH,
        DEFAULT_QUALIFICATION_REPORT_PATH,
        *(Path(item) for item in SOURCE_PATHS),
    }
    for relative in copied_paths:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    binding_path = tmp_path / DEFAULT_THRESHOLD_BINDING_PATH
    binding = json.loads(binding_path.read_text(encoding="utf-8"))
    binding["threshold"] += 0.01
    binding_path.write_text(json.dumps(binding), encoding="utf-8")
    with pytest.raises(KnownPolicyContractError, match="threshold"):
        load_known_policy_artifacts(tmp_path)


def test_assay_all_and_start_then_discard_match_frozen_plans() -> None:
    assay_agent, assay_actions = _first_lifecycle("assay_all")
    assert assay_actions == [
        *_prefix(),
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]
    assert assay_agent.manifest()["input_access_contract"][
        "observation_fields_read"
    ] == []

    discard_agent, discard_actions = _first_lifecycle("start_then_discard")
    assert discard_actions == [
        {"operation": "add_solvent", "volume_L": 0.025, "solvent": 0},
        {
            "operation": "discard_batch",
            "reason": "known_policy_immediate_discard",
        },
    ]
    assert discard_agent.agent_trace() == []


@pytest.mark.parametrize(
    ("diagnostic", "expected_tail", "expected_branch"),
    [
        (
            1.0,
            [
                {
                    "operation": "electrolyze",
                    "duration_s": PROBE_SCHEDULE[0].post_measure_duration_s,
                },
                {"operation": "terminate"},
                {"operation": "measure", "instrument": "final_assay"},
            ],
            "continue_and_assay",
        ),
        (
            0.0,
            [
                {
                    "operation": "discard_batch",
                    "reason": "known_policy_below_threshold",
                }
            ],
            "discard_below_threshold",
        ),
        (
            None,
            [
                {
                    "operation": "discard_batch",
                    "reason": "known_policy_diagnostic_unavailable",
                }
            ],
            "discard_diagnostic_unavailable",
        ),
    ],
)
def test_threshold_policy_implements_all_frozen_terminal_branches(
    diagnostic: float | None,
    expected_tail: list[dict[str, Any]],
    expected_branch: str,
) -> None:
    agent, actions = _first_lifecycle("measure_then_threshold", diagnostic)
    assert actions == [
        *_prefix(),
        {"operation": "measure", "instrument": "uvvis"},
        *expected_tail,
    ]
    trace = agent.agent_trace()
    assert len(trace) == 1
    assert trace[0]["diagnostic_value"] == diagnostic
    assert trace[0]["branch"] == expected_branch
    assert trace[0]["observation_fields_read"] == ["conversion"]
    assert trace[0]["material_information_read"] is False


def test_policy_ignores_material_dossier_and_fails_closed() -> None:
    left = KnownPolicyAgent("measure_then_threshold")
    right = KnownPolicyAgent("measure_then_threshold")
    left.reset(_task_info({"mode": "opaque_codes", "dossier": {"x": 1}}), seed=0)
    right.reset(
        _task_info({"mode": "anonymous_nominal_properties", "dossier": {"x": 999}}),
        seed=999,
    )
    assert left.act([]) == right.act([])
    with pytest.raises(KnownPolicyExecutionError, match="before the preceding"):
        left.act([])

    failed = KnownPolicyAgent("assay_all")
    failed.reset(_task_info(), seed=0)
    action = failed.act([])
    with pytest.raises(KnownPolicyExecutionError, match="non-committed"):
        failed.update(
            action,
            {},
            0.0,
            {"transaction_status": "validation_failed"},
        )
    with pytest.raises(KnownPolicyExecutionError, match="faulted"):
        failed.act([])


@pytest.mark.parametrize(
    ("policy_id", "budget"),
    [("assay_all", 36), ("start_then_discard", 12), ("measure_then_threshold", 48)],
)
def test_nonformal_environment_smoke_closes_six_lifecycles_with_audits(
    policy_id: str,
    budget: int,
    tmp_path: Path,
) -> None:
    output = tmp_path / f"{policy_id}.jsonl"
    records = run_agent(
        env_id="ChemWorld",
        agent=KnownPolicyAgent(policy_id),
        world_split="public-test",
        budget=budget,
        objective="balanced",
        seed=20_000,
        observation_seed=220_000,
        task_id="electrochemical-conversion",
        output_path=output,
        budget_override=budget,
        episode_mode_override="campaign",
        material_information={"mode": "opaque_codes"},
        campaign_resource_card=_nonformal_smoke_resource_card(),
        electrochemical_material_family_id="nominal-prior-latent-v2",
        electrochemical_workflow_mode="autonomous_open_v1",
        observation_noise_mode="keyed",
        observation_noise_namespace=f"work-i-v04-smoke-{policy_id}",
    )
    assert records
    assert all(item.info["transaction_status"] == "committed" for item in records)
    assert records[-1].info["campaign_resources"]["state"]["closed_batches"] == 6
    assert all(item.decision_audit["status"] == "provided" for item in records)

    rows = load_jsonl(output)
    manifest = rows[0]["agent_metadata"]
    assert manifest["provider_call_count"] == 0
    assert manifest["input_access_contract"]["reads_material_information"] is False
    assert manifest["artifact_bindings"]["threshold_binding_sha256"] == (
        "8a55b713ca900a644a301ecd8e83a0a686f9a28b3f60a18a85a4e57b66288c6a"
    )
    if policy_id == "measure_then_threshold":
        assert len(rows[-1]["agent_trace"]) == 6
