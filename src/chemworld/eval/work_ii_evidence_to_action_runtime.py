"""Provider-independent recipient runtime for the five evidence-to-action conditions."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from copy import deepcopy
from typing import Any, Protocol

from chemworld.eval.provenance import canonical_json_sha256
from chemworld.eval.work_ii_evidence_to_action import (
    CONDITION_STAGES,
    CONDITIONS,
    build_learned_law_artifact,
    build_yoked_evidence_packet,
)
from chemworld.eval.work_ii_prior_discovery import parse_work_ii_belief_snapshot

RECIPIENT_CONTEXT_SCHEMA = "chemworld-work-ii-evidence-to-action-recipient-context-0.1"
TERMINAL_SUBMISSION_SCHEMA = "chemworld-work-ii-evidence-to-action-terminal-submission-0.1"
RECIPIENT_SYSTEM_PROMPT = """You are making a blinded scientific decision in ChemWorld.
Use only the public task contract, prior information, and evidence included in this turn. Candidate
outcomes and evaluator ranks are unavailable. Return exactly the requested JSON object. Rank all
candidate ActionPlans from best to worst and select the first-ranked candidate. Do not invent
experiments, observations, or hidden simulator state."""

_FORBIDDEN_PUBLIC_KEYS = frozenset(
    {
        "agent_trace",
        "candidate_pool_ranks",
        "candidate_truth",
        "donor_reasoning",
        "hidden_evaluator_fields",
        "presented_candidate_ranks",
    }
)


class JsonRecipientClient(Protocol):
    model: str

    def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
        output_schema: Mapping[str, Any] | None = None,
    ) -> Any: ...


def _assert_public(value: Any, *, path: str = "context") -> None:
    if isinstance(value, Mapping):
        forbidden = _FORBIDDEN_PUBLIC_KEYS & {str(key) for key in value}
        if forbidden:
            raise ValueError(f"{path} contains forbidden fields: {sorted(forbidden)}")
        for key, item in value.items():
            _assert_public(item, path=f"{path}.{key}")
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        for index, item in enumerate(value):
            _assert_public(item, path=f"{path}[{index}]")


def _public_candidates(candidate_packet: Mapping[str, Any] | Sequence[Any]) -> list[dict[str, Any]]:
    if isinstance(candidate_packet, Mapping):
        if candidate_packet.get("candidate_outcomes_included") is not False:
            raise ValueError("candidate packet does not prove outcome blindness")
        raw = candidate_packet.get("candidates")
    else:
        raw = candidate_packet
    if isinstance(raw, (str, bytes)) or not isinstance(raw, Sequence):
        raise ValueError("candidate packet must contain a candidate list")
    candidates = [deepcopy(dict(row)) for row in raw if isinstance(row, Mapping)]
    query_ids = [str(row.get("query_id")) for row in candidates]
    if len(candidates) != 8 or len(set(query_ids)) != 8 or any(
        query_id in {"", "None"} for query_id in query_ids
    ):
        raise ValueError("candidate packet must contain eight unique query IDs")
    _assert_public(candidates, path="candidate_packet")
    return candidates


def _yoked_evidence_at_stage(
    packet: Mapping[str, Any],
    stage: str,
) -> list[dict[str, Any]]:
    if packet.get("schema_version") != "chemworld-work-ii-yoked-evidence-packet-0.1":
        raise ValueError("yoked evidence packet schema is invalid")
    rounds = packet.get("checkpoint_rounds")
    if not isinstance(rounds, list) or len(rounds) != 12:
        raise ValueError("yoked evidence packet must contain 12 rounds")
    visible_count = {
        "pre_evidence": 0,
        "after_experiment_3": 3,
        "after_experiment_6": 6,
        "after_experiment_9": 9,
        "final": 12,
        "terminal_ranking": 12,
    }.get(stage)
    if visible_count is None:
        raise ValueError("stage is invalid for yoked evidence")
    visible = [deepcopy(dict(row)) for row in rounds[:visible_count]]
    _assert_public(visible, path="yoked_evidence")
    return visible


def build_recipient_context(
    *,
    condition: str,
    stage: str,
    task_contract: Mapping[str, Any],
    initial_world_model: Mapping[str, Any],
    candidate_packet: Mapping[str, Any] | Sequence[Any],
    yoked_evidence_packet: Mapping[str, Any] | None = None,
    law_artifact: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Compile one condition-specific public turn without crossing reveal gates."""

    if condition not in CONDITIONS:
        raise ValueError("unknown evidence-to-action condition")
    if stage not in CONDITION_STAGES[condition]:
        raise ValueError("recipient stage differs from its condition contract")
    if condition == "autonomous_exploration" and stage != "terminal_ranking":
        raise ValueError("autonomous evidence turns belong to the campaign runtime")
    candidates = _public_candidates(candidate_packet)
    candidate_visible = stage == "terminal_ranking"
    evidence: list[dict[str, Any]] = []
    artifact: dict[str, Any] | None = None

    if condition == "yoked_evidence":
        if not isinstance(yoked_evidence_packet, Mapping):
            raise ValueError("yoked condition requires its donor evidence packet")
        evidence = _yoked_evidence_at_stage(yoked_evidence_packet, stage)
    elif yoked_evidence_packet is not None:
        raise ValueError("non-yoked condition may not receive donor evidence")

    if condition in {"learned_law_only", "oracle_law"}:
        if not isinstance(law_artifact, Mapping):
            raise ValueError("artifact-only condition requires one law artifact")
        expected_type = (
            "participant_final_typed_law"
            if condition == "learned_law_only"
            else "provider_free_disjoint_grid_fitted_predictive_law"
        )
        if law_artifact.get("artifact_type") != expected_type:
            raise ValueError("law artifact type differs from the recipient condition")
        if law_artifact.get("candidate_information_included") is not False:
            raise ValueError("law artifact does not prove candidate blindness")
        artifact = deepcopy(dict(law_artifact))
        candidate_visible = True
    elif law_artifact is not None:
        raise ValueError("condition may not receive an external law artifact")

    context: dict[str, Any] = {
        "schema_version": RECIPIENT_CONTEXT_SCHEMA,
        "condition": condition,
        "stage": stage,
        "task_contract": deepcopy(dict(task_contract)),
        "initial_world_model": deepcopy(dict(initial_world_model)),
        "visible_yoked_evidence_rounds": evidence,
        "law_artifact": artifact,
        "candidate_packet": candidates if candidate_visible else None,
        "candidate_outcomes_included": False,
        "candidate_ranks_included": False,
        "physical_experiment_authority": condition == "autonomous_exploration",
    }
    _assert_public(context)
    context["context_sha256"] = canonical_json_sha256(context)
    return context


def terminal_output_schema(candidate_query_ids: Sequence[str]) -> dict[str, Any]:
    query_ids = [str(query_id) for query_id in candidate_query_ids]
    if len(query_ids) != 8 or len(set(query_ids)) != 8:
        raise ValueError("terminal schema requires eight unique candidate IDs")
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "schema_version",
            "ranking",
            "selected_query_id",
            "decision_rationale",
        ],
        "properties": {
            "schema_version": {"type": "string", "const": TERMINAL_SUBMISSION_SCHEMA},
            "ranking": {
                "type": "array",
                "minItems": 8,
                "maxItems": 8,
                "uniqueItems": True,
                "items": {"type": "string", "enum": query_ids},
            },
            "selected_query_id": {"type": "string", "enum": query_ids},
            "decision_rationale": {"type": "string", "minLength": 1, "maxLength": 2000},
        },
    }


def validate_terminal_submission(
    payload: Mapping[str, Any],
    *,
    candidate_query_ids: Sequence[str],
) -> dict[str, Any]:
    expected = {"schema_version", "ranking", "selected_query_id", "decision_rationale"}
    if set(payload) != expected:
        raise ValueError("terminal submission fields differ from the contract")
    if payload.get("schema_version") != TERMINAL_SUBMISSION_SCHEMA:
        raise ValueError("terminal submission schema is invalid")
    ranking = payload.get("ranking")
    if isinstance(ranking, (str, bytes)) or not isinstance(ranking, Sequence):
        raise ValueError("terminal ranking must be a list")
    normalized = [str(query_id) for query_id in ranking]
    expected_ids = [str(query_id) for query_id in candidate_query_ids]
    if len(normalized) != 8 or len(set(normalized)) != 8 or set(normalized) != set(
        expected_ids
    ):
        raise ValueError("terminal ranking must be a permutation of all candidates")
    if payload.get("selected_query_id") != normalized[0]:
        raise ValueError("selected query must equal the first-ranked candidate")
    rationale = payload.get("decision_rationale")
    if not isinstance(rationale, str) or not rationale.strip() or len(rationale) > 2000:
        raise ValueError("terminal decision rationale is invalid")
    return {
        "schema_version": TERMINAL_SUBMISSION_SCHEMA,
        "ranking": normalized,
        "selected_query_id": normalized[0],
        "decision_rationale": rationale.strip(),
    }


def execute_terminal_recipient(
    client: JsonRecipientClient,
    context: Mapping[str, Any],
    *,
    max_tokens: int = 4096,
) -> dict[str, Any]:
    """Execute one nonphysical terminal recipient turn through an injected provider client."""

    if context.get("schema_version") != RECIPIENT_CONTEXT_SCHEMA:
        raise ValueError("recipient context schema is invalid")
    if context.get("stage") != "terminal_ranking":
        raise ValueError("terminal recipient requires the terminal-ranking stage")
    candidates = context.get("candidate_packet")
    if not isinstance(candidates, list):
        raise ValueError("terminal recipient lacks its candidate packet")
    query_ids = [str(row["query_id"]) for row in candidates]
    completion = client.complete_json(
        system_prompt=RECIPIENT_SYSTEM_PROMPT,
        user_prompt=json.dumps(context, ensure_ascii=False, sort_keys=True),
        max_tokens=max_tokens,
        output_schema=terminal_output_schema(query_ids),
    )
    submission = validate_terminal_submission(
        completion.payload,
        candidate_query_ids=query_ids,
    )
    return {
        "status": "completed",
        "condition": context["condition"],
        "stage": "terminal_ranking",
        "context_sha256": context["context_sha256"],
        "submission": submission,
        "provider_model": str(completion.model),
        "provider_request_id": getattr(completion, "request_id", None),
        "provider_attempts": int(completion.attempts),
        "provider_usage": deepcopy(dict(completion.usage)),
    }


def validate_yoked_snapshot_submission(
    payload: Mapping[str, Any],
    *,
    stage: str,
    query_metric_contract: Mapping[str, Sequence[str]],
    allowed_feature_ids: Sequence[str],
    allowed_metric_ids: Sequence[str],
    allowed_prior_fields: Sequence[str],
    evidence_catalog: Sequence[str],
    nominal_information_available: bool,
) -> dict[str, Any]:
    """Apply the existing typed belief schema to a yoked recipient checkpoint."""

    parsed = parse_work_ii_belief_snapshot(
        payload,
        expected_stage=stage,
        query_metric_contract=query_metric_contract,
        allowed_feature_ids=allowed_feature_ids,
        allowed_metric_ids=allowed_metric_ids,
        allowed_prior_fields=allowed_prior_fields,
        evidence_catalog=evidence_catalog,
        nominal_information_available=nominal_information_available,
    )
    return parsed.to_dict()


def resolve_dependency_status(
    cell: Mapping[str, Any],
    completed_results: Mapping[str, Mapping[str, Any]],
) -> str:
    """Resolve a scheduled cell without replacing a failed autonomous donor."""

    dependencies = cell.get("dependency_cell_ids")
    if not isinstance(dependencies, list):
        raise ValueError("cell dependency list is invalid")
    if not dependencies:
        return "ready"
    if len(dependencies) != 1:
        raise ValueError("recipient cell must have exactly one autonomous donor")
    donor_id = str(dependencies[0])
    donor = completed_results.get(donor_id)
    if donor is None:
        return "waiting_for_donor"
    campaign_summary = donor.get("campaign_summary")
    campaign_summary = campaign_summary if isinstance(campaign_summary, Mapping) else {}
    completed = donor.get("status") == "completed_uncontaminated" or (
        donor.get("completed") is True or campaign_summary.get("completed") is True
    )
    return "ready" if completed else "not_started_due_to_missing_donor"


def build_donor_derivatives(
    *,
    donor_cell_id: str,
    donor_result: Mapping[str, Any],
    trajectory_rows: Sequence[Mapping[str, Any]],
    candidate_query_ids: Sequence[str],
) -> dict[str, Any]:
    """Create the two allowed donor products after an eligible autonomous terminal."""

    dependency_status = resolve_dependency_status(
        {"dependency_cell_ids": [donor_cell_id]},
        {donor_cell_id: donor_result},
    )
    if dependency_status != "ready":
        raise ValueError("failed autonomous donor may not produce recipient artifacts")
    campaign_summary = donor_result.get("campaign_summary")
    campaign_summary = (
        campaign_summary if isinstance(campaign_summary, Mapping) else donor_result
    )
    yoked = build_yoked_evidence_packet(
        trajectory_rows,
        donor_cell_id=donor_cell_id,
    )
    learned = build_learned_law_artifact(
        campaign_summary,
        donor_cell_id=donor_cell_id,
        candidate_query_ids=candidate_query_ids,
    )
    return {
        "schema_version": "chemworld-work-ii-evidence-to-action-donor-derivatives-0.1",
        "donor_cell_id": donor_cell_id,
        "yoked_evidence_packet": yoked,
        "learned_law_artifact": learned,
        "donor_reasoning_transferred": False,
        "candidate_information_transferred": False,
    }


__all__ = [
    "RECIPIENT_CONTEXT_SCHEMA",
    "RECIPIENT_SYSTEM_PROMPT",
    "TERMINAL_SUBMISSION_SCHEMA",
    "JsonRecipientClient",
    "build_donor_derivatives",
    "build_recipient_context",
    "execute_terminal_recipient",
    "resolve_dependency_status",
    "terminal_output_schema",
    "validate_terminal_submission",
    "validate_yoked_snapshot_submission",
]
