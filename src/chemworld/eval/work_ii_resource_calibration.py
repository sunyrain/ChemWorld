"""Outcome-blind W2-26 resource-calibration readiness and summary contracts."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    git_source_commit,
)

RESOURCE_CALIBRATION_MANIFEST_VERSION = (
    "chemworld-work-ii-resource-calibration-manifest-0.1"
)
RESOURCE_CALIBRATION_READINESS_VERSION = (
    "chemworld-work-ii-resource-calibration-readiness-0.1"
)
RESOURCE_CALIBRATION_SUMMARY_VERSION = (
    "chemworld-work-ii-resource-calibration-summary-0.1"
)
RESOURCE_CALIBRATION_Q2_GENERATION_VERSION = (
    "chemworld-work-ii-resource-calibration-q2-generation-0.1"
)
RESOURCE_CALIBRATION_ARMS = ("opaque", "aligned_nominal", "misindexed_nominal")
RESOURCE_CALIBRATION_ROUNDS = (8, 10, 12)
RESOURCE_CALIBRATION_LOCI = {8: "A_E", 10: "A_P", 12: "A_S"}
DEFAULT_RESOURCE_CALIBRATION_FORMAL_DESIGN = Path(
    "configs/benchmark/work_ii_formal_design_v0.2.json"
)
DEFAULT_RESOURCE_CALIBRATION_SELECTION_PROTOCOLS = {
    "A_P": Path("configs/benchmark/work_ii_c2_ap_selection_protocol_v0.1.json"),
    "A_S": Path("configs/benchmark/work_ii_c2_as_selection_protocol_v0.1.json"),
}
DEFAULT_RESOURCE_CALIBRATION_Q2_GENERATION_RECORDS = {
    "A_P": Path(
        "workstreams/flagship_tasks/reports/"
        "work-ii-reaction-safety-matched-prior-qualification-20260811.json"
    ),
    "A_S": Path(
        "workstreams/flagship_tasks/reports/"
        "work-ii-as-paired-law-q1-q2-five-world-20260812.json"
    ),
}
RESOURCE_CALIBRATION_CHECKPOINTS = {
    8: (0, 2, 4, 6, 8),
    10: (0, 2, 4, 7, 10),
    12: (0, 3, 6, 9, 12),
}
EXPECTED_RESOURCE_CALIBRATION_DENOMINATORS = {
    "pattern_triplets": 3,
    "cells": 9,
    "complete_experiments": 90,
    "belief_checkpoints": 45,
    "accepted_provider_sessions": 9,
    "accepted_participant_model_calls": 9,
}
EXPECTED_RESOURCE_CALIBRATION_OBSERVED_DENOMINATORS = {
    "pattern_triplets_started": 3,
    "pattern_triplets_terminal": 3,
    "cells_started": 9,
    "cells_terminal": 9,
    "complete_experiments": 90,
    "belief_checkpoints": 45,
    "provider_sessions": 9,
    "participant_model_calls": 9,
}
RESOURCE_CALIBRATION_CAP_FIELDS = (
    "operation_attempt_limit",
    "protected_closeout_operation_reserve",
    "maximum_exact_repeats",
    "process_time_limit_s",
    "protected_closeout_reserve_s",
    "input_token_limit",
    "uncached_input_token_limit",
    "output_token_limit",
    "provider_wall_time_limit_s",
    "currency_ceiling_usd",
)
RESOURCE_CALIBRATION_OBSERVED_FIELDS = {
    "operation_attempt_limit": "operation_attempts",
    "maximum_exact_repeats": "exact_repeat_count",
    "process_time_limit_s": "process_time_used_s",
    "input_token_limit": "input_tokens",
    "uncached_input_token_limit": "uncached_input_tokens",
    "output_token_limit": "output_tokens",
    "provider_wall_time_limit_s": "provider_elapsed_s",
    "currency_ceiling_usd": "observed_currency_usd",
}


def build_resource_calibration_execution_manifest(
    root: Path,
    protocol_manifest_path: Path,
    *,
    formal_design_path: Path | None = None,
    selection_protocol_paths: Mapping[str, Path] | None = None,
    q2_generation_record_paths: Mapping[str, Path] | None = None,
) -> dict[str, Any]:
    """Materialize 8/10/12 from final A-E/A-P/A-S selection evidence only."""

    root = root.resolve()
    protocol_manifest_path = protocol_manifest_path.resolve()
    formal_design_path = (
        root / DEFAULT_RESOURCE_CALIBRATION_FORMAL_DESIGN
        if formal_design_path is None
        else formal_design_path
    ).resolve()
    selection_protocol_paths = {
        locus: (root / path).resolve()
        for locus, path in (
            DEFAULT_RESOURCE_CALIBRATION_SELECTION_PROTOCOLS.items()
            if selection_protocol_paths is None
            else selection_protocol_paths.items()
        )
    }
    q2_generation_record_paths = {
        locus: (root / path).resolve()
        for locus, path in (
            DEFAULT_RESOURCE_CALIBRATION_Q2_GENERATION_RECORDS.items()
            if q2_generation_record_paths is None
            else q2_generation_record_paths.items()
        )
    }
    expected_design = (root / DEFAULT_RESOURCE_CALIBRATION_FORMAL_DESIGN).resolve()
    expected_protocols = {
        locus: (root / path).resolve()
        for locus, path in DEFAULT_RESOURCE_CALIBRATION_SELECTION_PROTOCOLS.items()
    }
    expected_q2 = {
        locus: (root / path).resolve()
        for locus, path in DEFAULT_RESOURCE_CALIBRATION_Q2_GENERATION_RECORDS.items()
    }
    if formal_design_path != expected_design:
        raise ValueError("resource calibration requires the canonical formal design v0.2 path")
    if selection_protocol_paths != expected_protocols:
        raise ValueError(
            "resource calibration requires the canonical protected selection protocols"
        )
    if q2_generation_record_paths != expected_q2:
        raise ValueError("resource calibration requires the canonical Q2 generation records")
    protocol = _load_object(protocol_manifest_path)
    if validate_resource_calibration_manifest(root, protocol):
        raise ValueError("resource calibration protocol manifest is invalid")
    patterns, resolution = resolve_resource_calibration_representatives(
        root,
        protocol,
        formal_design_path=formal_design_path,
        selection_protocol_paths=selection_protocol_paths,
        q2_generation_record_paths=q2_generation_record_paths,
    )
    if resolution["blocking_requirements"]:
        raise ValueError(
            "resource calibration representatives are not ready: "
            + "; ".join(resolution["blocking_requirements"])
        )
    manifest = json.loads(json.dumps(protocol))
    manifest["patterns"] = patterns
    manifest["status"] = "ready_authorization_blocked"
    manifest["representative_resolution"] = resolution
    manifest["protocol_manifest_binding"] = {
        "path": protocol_manifest_path.relative_to(root).as_posix(),
        "sha256": file_sha256(protocol_manifest_path),
        "hash_kind": "file_sha256",
    }
    manifest["development_binding_policy"] = {
        "exact_selected_campaign_configs_bound": True,
        "selection_and_q2_inputs_bound": True,
        "whole_tree_hash_required": False,
        "clean_worktree_required": False,
        "release_freeze_deferred": True,
    }
    errors = validate_resource_calibration_manifest(root, manifest)
    if errors:
        raise ValueError("execution manifest failed: " + "; ".join(errors))
    return manifest


def _repository_binding(root: Path, path: Path) -> dict[str, str]:
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(root.resolve()).as_posix()
    except ValueError as error:
        raise ValueError("resource calibration dependency escapes repository") from error
    if not resolved.is_file():
        raise ValueError(f"resource calibration dependency is missing: {relative}")
    return {
        "path": relative,
        "sha256": file_sha256(resolved),
        "hash_kind": "file_sha256",
    }


def _representative_config_errors(
    config: Mapping[str, Any],
    *,
    rounds: int,
    locus: str,
    task_id: str,
) -> list[str]:
    campaign = config.get("campaign")
    campaign = campaign if isinstance(campaign, Mapping) else {}
    resources = config.get("method_resources")
    resources = resources if isinstance(resources, Mapping) else {}
    errors: list[str] = []
    if config.get("task_id") != task_id:
        errors.append(f"{rounds}-round {locus} config task_id differs from selection")
    if isinstance(config.get("world_seed"), bool) or not isinstance(
        config.get("world_seed"), int
    ):
        errors.append(f"{rounds}-round {locus} config lacks an exact integer world_seed")
    prior_arms = config.get("prior_arms")
    if not isinstance(prior_arms, Mapping) or set(prior_arms) != set(
        RESOURCE_CALIBRATION_ARMS
    ):
        errors.append(f"{rounds}-round {locus} config lacks the exact arm triplet")
    if (
        campaign.get("complete_experiments") != rounds
        or tuple(campaign.get("checkpoint_complete_experiments", []))
        != RESOURCE_CALIBRATION_CHECKPOINTS[rounds]
        or resources.get("complete_experiment_limit") != rounds
    ):
        errors.append(f"{rounds}-round {locus} config differs from its frozen pattern")
    return errors


def _validate_ap_q2_record(
    root: Path, record: Mapping[str, Any], *, task_id: str
) -> tuple[list[str], object]:
    """Validate the complete frozen matched-prior Q2 summary contract for A-P."""

    errors: list[str] = []
    expected_coverage = {
        "world_count": 5,
        "surface_queries_per_world": 121,
        "planned_surface_query_count": 605,
        "held_out_queries_per_world": 16,
    }
    expected_denominators = {
        "world_count": 5,
        "passed_world_count": 5,
        "classified_surface_query_count": 605,
        "physical_failure_count": 64,
        "platform_failure_count": 0,
        "safe_fit_count": 150,
        "safe_held_out_count": 391,
    }
    digest = record.get("summary_sha256")
    if (
        record.get("schema_version")
        != "chemworld-work-ii-matched-prior-five-world-summary-0.3"
        or record.get("qualification_schema_version")
        != "chemworld-work-ii-matched-prior-qualification-0.3"
        or record.get("task_id") != task_id
        or record.get("qualification_passed") is not True
        or record.get("coverage") != expected_coverage
        or record.get("denominators") != expected_denominators
        or record.get("failure_count") != 0
        or record.get("failures") != []
        or record.get("d1_authorized") is not True
        or record.get("decision") != "proceed_to_reaction_safety_d1"
        or record.get("world_seeds") != [0, 1, 2, 3, 4]
        or not isinstance(digest, str)
        or digest != _self_hash(record, "summary_sha256")
    ):
        errors.append("10-round A_P rank-1 task lacks a valid frozen Q2 summary")
    worlds = record.get("worlds")
    worlds = worlds if isinstance(worlds, list) else []
    if len(worlds) != 5:
        errors.append("10-round A_P Q2 summary lacks all five world results")
    else:
        totals = {
            "passed_world_count": 0,
            "physical_failure_count": 0,
            "safe_fit_count": 0,
            "safe_held_out_count": 0,
        }
        for seed, world in enumerate(worlds):
            world = world if isinstance(world, Mapping) else {}
            leakage = world.get("leakage_audit")
            leakage = leakage if isinstance(leakage, Mapping) else {}
            matching = world.get("prior_matching")
            matching = matching if isinstance(matching, Mapping) else {}
            reflection = world.get("selected_reflection")
            reflection = reflection if isinstance(reflection, Mapping) else {}
            if (
                world.get("world_seed") != seed
                or world.get("passed") is not True
                or leakage.get("passed") is not True
                or leakage.get("failures") != []
                or leakage.get("forbidden_pattern_hits") != []
                or matching.get("passed") is not True
                or matching.get("failures") != []
                or reflection.get("passed") is not True
            ):
                errors.append(f"10-round A_P Q2 world {seed} is not fully passed")
            totals["passed_world_count"] += int(world.get("passed") is True)
            for field in (
                "physical_failure_count",
                "safe_fit_count",
                "safe_held_out_count",
            ):
                value = world.get(field)
                if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                    errors.append(f"10-round A_P Q2 world {seed} lacks valid {field}")
                else:
                    totals[field] += value
        denominators = record.get("denominators")
        denominators = denominators if isinstance(denominators, Mapping) else {}
        if any(denominators.get(field) != value for field, value in totals.items()):
            errors.append("10-round A_P Q2 world totals differ from denominators")
    raw_bindings = record.get("raw_bindings")
    raw_bindings = raw_bindings if isinstance(raw_bindings, list) else []
    if len(raw_bindings) != 5 or any(
        not isinstance(binding, Mapping)
        or binding.get("world_seed") != seed
        or binding.get("passed") is not True
        or not isinstance(binding.get("path"), str)
        or not isinstance(binding.get("sha256"), str)
        or len(str(binding.get("sha256"))) != 64
        for seed, binding in enumerate(raw_bindings)
    ):
        errors.append("10-round A_P Q2 raw world bindings are incomplete")
    generated_package = record.get("generated_package")
    package_errors = _validate_binding(
        root,
        {
            **(dict(generated_package) if isinstance(generated_package, Mapping) else {}),
            "hash_kind": "file_sha256",
        },
        "10-round A_P generated package",
    )
    errors.extend(package_errors)
    return errors, record.get("generated_d1_config")


def _validate_as_q2_record(
    root: Path, record: Mapping[str, Any], *, task_id: str
) -> tuple[list[str], object]:
    from chemworld.eval.work_ii_constitutive_structural_qualification import (
        CANDIDATE_IDS,
        candidate_specs,
        validate_summary,
    )

    errors = [f"12-round A_S Q2: {error}" for error in validate_summary(root, record)]
    candidates = record.get("candidates")
    candidates = candidates if isinstance(candidates, Mapping) else {}
    candidate_ids = [
        candidate_id
        for candidate_id in CANDIDATE_IDS
        if candidate_specs()[candidate_id].get("task_id") == task_id
    ]
    candidate_id = candidate_ids[0] if len(candidate_ids) == 1 else None
    candidate = candidates.get(candidate_id) if candidate_id is not None else None
    candidate = candidate if isinstance(candidate, Mapping) else {}
    if (
        candidate_id is None
        or candidate.get("qualification_passed") is not True
        or candidate.get("passed_world_count") != 5
    ):
        errors.append("12-round A_S rank-1 task lacks a passed Q2 record")
    generated_map = record.get("participant_d1_configs_generated")
    generated_map = generated_map if isinstance(generated_map, Mapping) else {}
    return errors, generated_map.get(candidate_id)


def _selection_protocol_rank_one(
    root: Path, path: Path, *, locus: str
) -> tuple[list[str], dict[str, str] | None, str | None]:
    from chemworld.eval.work_ii_c2_admission import (
        C2_SELECTION_PROTOCOL_VERSION,
        build_c2_selection_protocol,
    )

    errors: list[str] = []
    try:
        binding = _repository_binding(root, path)
        protocol = _load_object(path)
    except (OSError, ValueError) as error:
        return [f"{locus} selection protocol is unavailable: {error}"], None, None
    roster = protocol.get("candidate_roster")
    roster = roster if isinstance(roster, list) else []
    try:
        rebuilt = build_c2_selection_protocol(
            locus=locus,
            candidate_roster=[
                dict(row) if isinstance(row, Mapping) else {} for row in roster
            ],
        )
    except (TypeError, ValueError) as error:
        errors.append(f"{locus} selection protocol cannot be rebuilt: {error}")
    else:
        if (
            protocol.get("schema_version") != C2_SELECTION_PROTOCOL_VERSION
            or protocol != rebuilt
        ):
            errors.append(f"{locus} selection protocol is stale or not pre-evidence frozen")
    rank_one = [
        row
        for row in roster
        if isinstance(row, Mapping) and row.get("frozen_rank") == 1
    ]
    task_id = rank_one[0].get("task_id") if len(rank_one) == 1 else None
    if not isinstance(task_id, str) or not task_id:
        errors.append(f"{locus} selection protocol lacks one canonical rank-1 task")
        task_id = None
    return errors, binding, task_id


def _q2_generation_contract(
    root: Path,
    path: Path,
    *,
    locus: str,
    rounds: int,
    task_id: str,
) -> tuple[list[str], dict[str, str] | None, Path | None, dict[str, Any] | None]:
    errors: list[str] = []
    try:
        record_binding = _repository_binding(root, path)
        record = _load_object(path)
    except (OSError, ValueError) as error:
        return (
            [f"{rounds}-round {locus} Q2 generation record is unavailable: {error}"],
            None,
            None,
            None,
        )
    if (
        record.get("formal_result") is not False
        or record.get("provider_call_count") != 0
        or record.get("participant_session_count") not in {None, 0}
    ):
        errors.append(
            f"{rounds}-round {locus} Q2 generation record is not provider/participant-free"
        )

    generated: object = None
    try:
        if record.get("schema_version") == RESOURCE_CALIBRATION_Q2_GENERATION_VERSION:
            errors.append(
                f"{rounds}-round {locus} self-declared Q2 generation records "
                "cannot unlock execution"
            )
            generated = record.get("generated_d1_config")
        elif locus == "A_P":
            locus_errors, generated = _validate_ap_q2_record(
                root, record, task_id=task_id
            )
            errors.extend(locus_errors)
        else:
            locus_errors, generated = _validate_as_q2_record(
                root, record, task_id=task_id
            )
            errors.extend(locus_errors)
    except (OSError, TypeError, ValueError) as error:
        errors.append(f"{rounds}-round {locus} Q2 record cannot be validated: {error}")

    generated = generated if isinstance(generated, Mapping) else {}
    relative = generated.get("path")
    digest = generated.get("sha256")
    if not isinstance(relative, str) or not isinstance(digest, str):
        errors.append(f"{rounds}-round {locus} Q2 record lacks its generated static D1 config")
        return errors, record_binding, None, None
    config_path = (root / relative).resolve()
    try:
        config_path.relative_to(root)
    except ValueError:
        errors.append(f"{rounds}-round {locus} generated static D1 config escapes repository")
        return errors, record_binding, None, None
    if not config_path.is_file() or file_sha256(config_path) != digest:
        errors.append(f"{rounds}-round {locus} generated static D1 config binding is stale")
        return errors, record_binding, config_path, None
    config = _load_object(config_path)
    errors.extend(
        _representative_config_errors(
            config, rounds=rounds, locus=locus, task_id=task_id
        )
    )
    if config.get("formal_result") is not False:
        errors.append(f"{rounds}-round {locus} generated static D1 config is not non-formal")
    qualification = config.get("qualification")
    qualification = qualification if isinstance(qualification, Mapping) else {}
    if qualification.get("q2_passed") is not True:
        errors.append(f"{rounds}-round {locus} generated static D1 config is not Q2-bound")
    return errors, record_binding, config_path, config


def resolve_resource_calibration_representatives(
    root: Path,
    protocol: Mapping[str, Any],
    *,
    formal_design_path: Path,
    selection_protocol_paths: Mapping[str, Path],
    q2_generation_record_paths: Mapping[str, Path],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Resolve representatives from formal v0.2 and provider-free Q2 generation.

    For A-P/A-S, the protected pre-evidence protocol owns the rank-1 identity and
    the passed provider-free Q2 generation record owns the exact static D1 config.
    Terminal D1 receipts are deliberately downstream and are not accepted here.
    """

    root = root.resolve()
    formal_design_path = formal_design_path.resolve()
    selection_protocol_paths = {
        locus: path.resolve() for locus, path in selection_protocol_paths.items()
    }
    q2_generation_record_paths = {
        locus: path.resolve() for locus, path in q2_generation_record_paths.items()
    }
    blockers: list[str] = []
    resolved_patterns = json.loads(json.dumps(protocol.get("patterns", [])))
    selected: dict[str, Any] = {}

    try:
        design = _load_object(formal_design_path)
        design_binding = _repository_binding(root, formal_design_path)
    except (OSError, ValueError) as error:
        design = {}
        design_binding = None
        blockers.append(f"formal v0.2 design is unavailable: {error}")
    if design and design.get("schema_version") != "chemworld-work-ii-formal-design-0.2":
        blockers.append("resource calibration requires formal design schema v0.2")

    patterns_by_round = {
        int(row.get("rounds")): row
        for row in resolved_patterns
        if isinstance(row, dict) and isinstance(row.get("rounds"), int)
    }
    if set(patterns_by_round) != set(RESOURCE_CALIBRATION_ROUNDS):
        blockers.append("resource calibration protocol does not contain exact 8/10/12 patterns")
    else:
        ae_pattern = patterns_by_round[8]
        ae_task_id = ae_pattern.get("task_id")
        design_tasks = design.get("tasks")
        design_tasks = design_tasks if isinstance(design_tasks, list) else []
        matching_tasks = [
            row
            for row in design_tasks
            if isinstance(row, Mapping) and row.get("task_id") == ae_task_id
        ]
        if len(matching_tasks) != 1 or not isinstance(ae_task_id, str):
            blockers.append(
                "8-round A_E representative is not an exact formal v0.2 task selection"
            )
        else:
            relative = matching_tasks[0].get("campaign_config")
            try:
                config_path = (root / str(relative)).resolve()
                config_binding = _repository_binding(root, config_path)
                config = _load_object(config_path)
            except (OSError, ValueError) as error:
                blockers.append(f"8-round A_E representative config is unavailable: {error}")
            else:
                ae_errors = _representative_config_errors(
                    config, rounds=8, locus="A_E", task_id=ae_task_id
                )
                blockers.extend(ae_errors)
                if not ae_errors:
                    ae_pattern.update(
                        {
                            "representative_task_status": "frozen",
                            "world_seed": config.get("world_seed"),
                            "campaign_config_binding": config_binding,
                            "task_specific_resource_formula_frozen": True,
                            "representative_selection_source": "formal_design_v0.2_task",
                            "representative_selection_binding": design_binding,
                        }
                    )
                    selected["8"] = {
                        "locus": "A_E",
                        "task_id": ae_task_id,
                        "selection_rule": "protocol_frozen_task_id_in_formal_design_v0.2",
                    }

        for rounds in (10, 12):
            locus = RESOURCE_CALIBRATION_LOCI[rounds]
            if set(selection_protocol_paths) != {"A_P", "A_S"} or set(
                q2_generation_record_paths
            ) != {"A_P", "A_S"}:
                blockers.append("resource calibration requires exact A_P/A_S Q2 inputs")
                break
            protocol_errors, protocol_binding, task_id = _selection_protocol_rank_one(
                root, selection_protocol_paths[locus], locus=locus
            )
            blockers.extend(protocol_errors)
            if task_id is None:
                continue
            q2_errors, q2_binding, config_path, config = _q2_generation_contract(
                root,
                q2_generation_record_paths[locus],
                locus=locus,
                rounds=rounds,
                task_id=task_id,
            )
            blockers.extend(q2_errors)
            if protocol_errors or q2_errors or config_path is None or config is None:
                continue
            patterns_by_round[rounds].update(
                {
                    "representative_task_status": "q2_generated_static_config_frozen",
                    "task_id": task_id,
                    "world_seed": config["world_seed"],
                    "campaign_config_binding": _repository_binding(root, config_path),
                    "task_specific_resource_formula_frozen": True,
                    "representative_selection_source": (
                        "protected_selection_protocol_rank_1"
                    ),
                    "representative_selection_binding": protocol_binding,
                    "q2_generation_record_binding": q2_binding,
                }
            )
            selected[str(rounds)] = {
                "locus": locus,
                "task_id": task_id,
                "selection_rule": (
                    "rank_1_in_protected_pre_evidence_selection_protocol"
                ),
            }

    resolution: dict[str, Any] = {
        "status": "resolved" if not blockers else "not_ready_fail_closed",
        "formal_design_binding": design_binding,
        "selection_protocol_bindings": {
            locus: (
                _repository_binding(root, path) if path.is_file() else None
            )
            for locus, path in selection_protocol_paths.items()
        },
        "q2_generation_record_bindings": {
            locus: (
                _repository_binding(root, path) if path.is_file() else None
            )
            for locus, path in q2_generation_record_paths.items()
        },
        "arbitrary_config_override_allowed": False,
        "proxy_substitution_allowed": False,
        "selected_representatives": selected,
        "blocking_requirements": blockers,
    }
    return resolved_patterns, resolution


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _self_hash(payload: Mapping[str, Any], field: str) -> str:
    return canonical_json_sha256(
        {key: value for key, value in payload.items() if key != field}
    )


def resource_calibration_readiness_sha256(report: Mapping[str, Any]) -> str:
    return _self_hash(report, "readiness_sha256")


def resource_calibration_summary_sha256(summary: Mapping[str, Any]) -> str:
    return _self_hash(summary, "summary_sha256")


def resource_calibration_authorization_sha256(
    authorization: Mapping[str, Any],
) -> str:
    return _self_hash(authorization, "authorization_sha256")


def build_resource_calibration_authorization(
    root: Path,
    manifest_path: Path,
    *,
    currency_ceiling_usd: float,
    approved_at: str,
    pricing_source: str,
    pricing_observed_at: str,
    cache_hit_input_usd_per_million: float,
    cache_miss_input_usd_per_million: float,
    output_usd_per_million: float,
) -> dict[str, Any]:
    """Build one credential-free, write-once W2-26 execution authorization."""

    root = root.resolve()
    manifest_path = manifest_path.resolve()
    manifest = _load_object(manifest_path)
    manifest_errors = validate_resource_calibration_manifest(root, manifest)
    if manifest_errors:
        raise ValueError("resource calibration manifest failed: " + "; ".join(manifest_errors))
    readiness = build_resource_calibration_readiness(root, manifest_path)
    if readiness.get("status") != "ready_authorization_blocked":
        raise ValueError("resource calibration manifest is not ready for authorization")
    rates = (
        cache_hit_input_usd_per_million,
        cache_miss_input_usd_per_million,
        output_usd_per_million,
    )
    if (
        not _is_nonnegative_number(currency_ceiling_usd)
        or currency_ceiling_usd <= 0
        or any(not _is_nonnegative_number(rate) for rate in rates)
        or not any(rate > 0 for rate in rates)
    ):
        raise ValueError("resource calibration pricing and ceiling must be finite and positive")
    if not approved_at.strip() or not pricing_source.strip() or not pricing_observed_at.strip():
        raise ValueError("resource calibration authorization metadata is incomplete")
    attempt_rows: list[dict[str, Any]] = []
    initial_cost = 0.0
    hard_cost = 0.0
    for pattern in manifest["patterns"]:
        binding = pattern["campaign_config_binding"]
        config = _load_object(root / binding["path"])
        resources = config["method_resources"]
        input_tokens = int(resources["input_token_limit"])
        uncached_tokens = int(resources["uncached_input_token_limit"])
        output_tokens = int(resources["output_token_limit"])
        cached_tokens = input_tokens - uncached_tokens
        per_attempt_cost = round(
            (
                cached_tokens * cache_hit_input_usd_per_million
                + uncached_tokens * cache_miss_input_usd_per_million
                + output_tokens * output_usd_per_million
            )
            / 1_000_000,
            12,
        )
        initial_cost += per_attempt_cost * 3
        hard_cost += per_attempt_cost * 6
        attempt_rows.append(
            {
                "rounds": pattern["rounds"],
                "locus": pattern["locus"],
                "task_id": pattern["task_id"],
                "world_seed": pattern["world_seed"],
                "campaign_config_binding": dict(binding),
                "per_cell_token_caps": {
                    "input_tokens": input_tokens,
                    "uncached_input_tokens": uncached_tokens,
                    "output_tokens": output_tokens,
                },
                "per_cell_attempt_cost_cap_usd": per_attempt_cost,
                "initial_triplet_cost_cap_usd": round(per_attempt_cost * 3, 12),
                "triplet_with_infrastructure_resume_cost_cap_usd": round(
                    per_attempt_cost * 6, 12
                ),
            }
        )
    initial_cost = round(initial_cost, 12)
    hard_cost = round(hard_cost, 12)
    if currency_ceiling_usd < hard_cost:
        raise ValueError(
            "resource calibration currency ceiling is below the all-attempt cap "
            f"({currency_ceiling_usd} < {hard_cost})"
        )
    authorization: dict[str, Any] = {
        "schema_version": "chemworld-work-ii-resource-calibration-authorization-0.1",
        "status": "authorized_calibration_only",
        "formal_result": False,
        "provider_execution_allowed": True,
        "formal_execution_authorized": False,
        "manifest_binding": {
            "path": manifest_path.relative_to(root).as_posix(),
            "file_sha256": file_sha256(manifest_path),
            "canonical_json_sha256": canonical_json_sha256(manifest),
        },
        "development_runtime_commit_observed": git_source_commit(root),
        "clean_worktree_required": False,
        "whole_tree_hash_required": False,
        "approved_at": approved_at,
        "provider_contract": manifest["provider_contract"],
        "provider_contract_confirmed_by_user": True,
        "credential_rotation_confirmed_by_user": True,
        "pricing": {
            "source": pricing_source,
            "observed_at": pricing_observed_at,
            "unit": "usd_per_million_tokens",
            "cache_hit_input": cache_hit_input_usd_per_million,
            "cache_miss_input": cache_miss_input_usd_per_million,
            "output": output_usd_per_million,
        },
        "pattern_attempt_contracts": attempt_rows,
        "initial_schedule": {
            "provider_process_attempts": 9,
            "cost_cap_usd": initial_cost,
        },
        "all_infrastructure_resumes": {
            "provider_process_attempts": 18,
            "cost_cap_usd": hard_cost,
        },
        "currency_ceiling_usd": currency_ceiling_usd,
        "runtime_enforcement": {
            "per_cell_provider_attempt_hard_cap": 2,
            "reserve_full_token_cost_before_launch": True,
            "missing_infrastructure_only_resume": True,
            "participant_scientific_or_method_failure_retained": True,
            "platform_defect_invalidates_affected_triplet": True,
            "affected_triplet_restarts_from_first_cell": True,
        },
    }
    authorization["authorization_sha256"] = (
        resource_calibration_authorization_sha256(authorization)
    )
    return authorization


def validate_resource_calibration_authorization(
    root: Path,
    authorization: Mapping[str, Any],
    manifest_path: Path,
) -> list[str]:
    errors: list[str] = []
    if authorization.get("schema_version") != (
        "chemworld-work-ii-resource-calibration-authorization-0.1"
    ):
        errors.append("unexpected resource calibration authorization schema")
    if authorization.get("authorization_sha256") != (
        resource_calibration_authorization_sha256(authorization)
    ):
        errors.append("resource calibration authorization self-hash mismatch")
    manifest_path = manifest_path.resolve()
    manifest = _load_object(manifest_path)
    binding = authorization.get("manifest_binding")
    binding = binding if isinstance(binding, Mapping) else {}
    if (
        binding.get("path") != manifest_path.relative_to(root.resolve()).as_posix()
        or binding.get("file_sha256") != file_sha256(manifest_path)
        or binding.get("canonical_json_sha256") != canonical_json_sha256(manifest)
    ):
        errors.append("resource calibration authorization manifest binding is stale")
    if (
        authorization.get("status") != "authorized_calibration_only"
        or authorization.get("formal_result") is not False
        or authorization.get("provider_execution_allowed") is not True
        or authorization.get("formal_execution_authorized") is not False
        or authorization.get("clean_worktree_required") is not False
        or authorization.get("whole_tree_hash_required") is not False
    ):
        errors.append("resource calibration authorization boundary is invalid")
    observed_commit = authorization.get("development_runtime_commit_observed")
    if not isinstance(observed_commit, str) or not observed_commit:
        errors.append("resource calibration lacks an observed development runtime commit")
    runtime = authorization.get("runtime_enforcement")
    runtime = runtime if isinstance(runtime, Mapping) else {}
    if any(
        runtime.get(field) is not True
        for field in (
            "reserve_full_token_cost_before_launch",
            "missing_infrastructure_only_resume",
            "participant_scientific_or_method_failure_retained",
            "platform_defect_invalidates_affected_triplet",
            "affected_triplet_restarts_from_first_cell",
        )
    ) or runtime.get("per_cell_provider_attempt_hard_cap") != 2:
        errors.append("resource calibration authorization runtime contract is incomplete")
    hard = authorization.get("all_infrastructure_resumes")
    hard = hard if isinstance(hard, Mapping) else {}
    ceiling = authorization.get("currency_ceiling_usd")
    if (
        not _is_nonnegative_number(ceiling)
        or not _is_nonnegative_number(hard.get("cost_cap_usd"))
        or ceiling < hard.get("cost_cap_usd", float("inf"))
        or len(authorization.get("pattern_attempt_contracts", [])) != 3
    ):
        errors.append("resource calibration authorization cost contract is invalid")
    return errors


def _validate_binding(root: Path, binding: object, label: str) -> list[str]:
    if not isinstance(binding, Mapping):
        return [f"resource calibration {label} binding is missing"]
    relative = binding.get("path")
    digest = binding.get("sha256")
    hash_kind = binding.get("hash_kind")
    if (
        not isinstance(relative, str)
        or not isinstance(digest, str)
        or hash_kind not in {"file_sha256", "canonical_json_sha256"}
    ):
        return [f"resource calibration {label} binding is incomplete"]
    path = (root / relative).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        return [f"resource calibration {label} binding escapes the repository"]
    if not path.is_file():
        return [f"resource calibration {label} binding is missing"]
    actual = (
        file_sha256(path)
        if hash_kind == "file_sha256"
        else canonical_json_sha256(_load_object(path))
    )
    return [] if actual == digest else [f"resource calibration {label} binding is stale"]


def _validate_ready_representative_provenance(
    root: Path,
    manifest: Mapping[str, Any],
    patterns: list[object],
) -> list[str]:
    errors: list[str] = []
    resolution = manifest.get("representative_resolution")
    resolution = resolution if isinstance(resolution, Mapping) else {}
    if (
        resolution.get("status") != "resolved"
        or resolution.get("arbitrary_config_override_allowed") is not False
        or resolution.get("proxy_substitution_allowed") is not False
        or resolution.get("blocking_requirements") != []
    ):
        errors.append(
            "ready resource calibration lacks a fail-closed representative resolution"
        )
    design_binding = resolution.get("formal_design_binding")
    protocol_bindings = resolution.get("selection_protocol_bindings")
    protocol_bindings = protocol_bindings if isinstance(protocol_bindings, Mapping) else {}
    q2_bindings = resolution.get("q2_generation_record_bindings")
    q2_bindings = q2_bindings if isinstance(q2_bindings, Mapping) else {}
    errors.extend(_validate_binding(root, design_binding, "formal v0.2 design"))
    expected_design_path = DEFAULT_RESOURCE_CALIBRATION_FORMAL_DESIGN.as_posix()
    if (
        not isinstance(design_binding, Mapping)
        or design_binding.get("path") != expected_design_path
    ):
        errors.append("ready resource calibration does not bind the canonical formal design")
    design: dict[str, Any] = {}
    if isinstance(design_binding, Mapping) and isinstance(design_binding.get("path"), str):
        path = (root / str(design_binding["path"])).resolve()
        if path.is_file():
            design = _load_object(path)
    if design.get("schema_version") != "chemworld-work-ii-formal-design-0.2":
        errors.append("ready resource calibration is not bound to formal design v0.2")
    selected = resolution.get("selected_representatives")
    selected = selected if isinstance(selected, Mapping) else {}
    design_tasks = design.get("tasks")
    design_tasks = design_tasks if isinstance(design_tasks, list) else []

    for rounds, raw in zip(RESOURCE_CALIBRATION_ROUNDS, patterns, strict=True):
        if not isinstance(raw, Mapping):
            continue
        locus = RESOURCE_CALIBRATION_LOCI[rounds]
        task_id = raw.get("task_id")
        if raw.get("locus") != locus:
            errors.append(f"{rounds}-round calibration representative must be {locus} owned")
        selected_row = selected.get(str(rounds))
        selected_row = selected_row if isinstance(selected_row, Mapping) else {}
        if selected_row.get("locus") != locus or selected_row.get("task_id") != task_id:
            errors.append(f"{rounds}-round representative resolution differs from pattern")
        selection_binding = raw.get("representative_selection_binding")
        errors.extend(
            _validate_binding(
                root,
                selection_binding,
                f"{rounds}-round representative selection",
            )
        )
        campaign_binding = raw.get("campaign_config_binding")
        campaign_binding = (
            campaign_binding if isinstance(campaign_binding, Mapping) else {}
        )
        if rounds == 8:
            if (
                raw.get("representative_selection_source")
                != "formal_design_v0.2_task"
                or selection_binding != design_binding
                or selected_row.get("selection_rule")
                != "protocol_frozen_task_id_in_formal_design_v0.2"
            ):
                errors.append("8-round representative is not selected by formal design v0.2")
            task_rows = [
                row
                for row in design_tasks
                if isinstance(row, Mapping) and row.get("task_id") == task_id
            ]
            if (
                len(task_rows) != 1
                or task_rows[0].get("campaign_config") != campaign_binding.get("path")
            ):
                errors.append("8-round representative config differs from formal design v0.2")
            continue

        protocol_binding = protocol_bindings.get(locus)
        q2_binding = q2_bindings.get(locus)
        errors.extend(_validate_binding(root, protocol_binding, f"{locus} selection protocol"))
        errors.extend(_validate_binding(root, q2_binding, f"{locus} Q2 generation record"))
        expected_protocol_path = DEFAULT_RESOURCE_CALIBRATION_SELECTION_PROTOCOLS[
            locus
        ].as_posix()
        expected_q2_path = DEFAULT_RESOURCE_CALIBRATION_Q2_GENERATION_RECORDS[
            locus
        ].as_posix()
        if (
            not isinstance(protocol_binding, Mapping)
            or protocol_binding.get("path") != expected_protocol_path
            or not isinstance(q2_binding, Mapping)
            or q2_binding.get("path") != expected_q2_path
        ):
            errors.append(
                f"{rounds}-round {locus} representative uses noncanonical evidence paths"
            )
        if (
            raw.get("representative_selection_source")
            != "protected_selection_protocol_rank_1"
            or selected_row.get("selection_rule")
            != "rank_1_in_protected_pre_evidence_selection_protocol"
            or selection_binding != protocol_binding
            or raw.get("q2_generation_record_binding") != q2_binding
        ):
            errors.append(
                f"{rounds}-round {locus} representative is not bound to rank-1 "
                "protected selection and provider-free Q2 generation"
            )
            continue
        if not isinstance(protocol_binding, Mapping) or not isinstance(q2_binding, Mapping):
            continue
        protocol_path = (root / str(protocol_binding.get("path"))).resolve()
        q2_path = (root / str(q2_binding.get("path"))).resolve()
        protocol_errors, _, selected_task = _selection_protocol_rank_one(
            root, protocol_path, locus=locus
        )
        q2_errors, _, config_path, _ = _q2_generation_contract(
            root,
            q2_path,
            locus=locus,
            rounds=rounds,
            task_id=str(selected_task or ""),
        )
        errors.extend(protocol_errors)
        errors.extend(q2_errors)
        if (
            selected_task != task_id
            or config_path is None
            or campaign_binding.get("path")
            != config_path.relative_to(root).as_posix()
            or campaign_binding.get("sha256") != file_sha256(config_path)
        ):
            errors.append(
                f"{rounds}-round {locus} representative config differs from Q2 generation"
            )
    return errors


def validate_resource_calibration_manifest(
    root: Path,
    manifest: Mapping[str, Any],
) -> list[str]:
    """Validate the frozen 8/10/12 design without treating gaps as authorization."""

    root = root.resolve()
    errors: list[str] = []
    if manifest.get("schema_version") != RESOURCE_CALIBRATION_MANIFEST_VERSION:
        errors.append("unexpected resource calibration manifest schema")
    if (
        manifest.get("formal_result") is not False
        or manifest.get("provider_execution_allowed") is not False
        or manifest.get("provider_calls_executed") != 0
    ):
        errors.append("resource calibration manifest crossed the execution boundary")
    errors.extend(
        _validate_binding(root, manifest.get("experiment_note_binding"), "experiment note")
    )
    errors.extend(
        _validate_binding(
            root,
            manifest.get("participant_method_binding"),
            "participant method",
        )
    )
    if tuple(manifest.get("prior_arms", [])) != RESOURCE_CALIBRATION_ARMS:
        errors.append("resource calibration manifest lacks the exact arm triplet")
    patterns = manifest.get("patterns")
    if not isinstance(patterns, list) or len(patterns) != 3:
        errors.append("resource calibration manifest must contain three pattern triplets")
        return errors
    if tuple(row.get("rounds") for row in patterns if isinstance(row, Mapping)) != (
        RESOURCE_CALIBRATION_ROUNDS
    ):
        errors.append("resource calibration pattern order must equal 8/10/12")
    ready = True
    for expected_rounds, row in zip(RESOURCE_CALIBRATION_ROUNDS, patterns, strict=True):
        if not isinstance(row, Mapping):
            errors.append(f"resource calibration {expected_rounds}-round pattern is malformed")
            ready = False
            continue
        if tuple(row.get("checkpoint_complete_experiments", [])) != (
            RESOURCE_CALIBRATION_CHECKPOINTS[expected_rounds]
        ):
            errors.append(
                f"resource calibration {expected_rounds}-round checkpoints are not frozen"
            )
        selected = (
            isinstance(row.get("task_id"), str)
            and isinstance(row.get("world_seed"), int)
            and row.get("task_specific_resource_formula_frozen") is True
            and isinstance(row.get("campaign_config_binding"), Mapping)
        )
        if selected:
            errors.extend(
                _validate_binding(
                    root,
                    row.get("campaign_config_binding"),
                    f"{expected_rounds}-round campaign config",
                )
            )
            binding = row.get("campaign_config_binding")
            binding = binding if isinstance(binding, Mapping) else {}
            relative = binding.get("path")
            if isinstance(relative, str) and (root / relative).is_file():
                config = _load_object(root / relative)
                campaign = config.get("campaign")
                campaign = campaign if isinstance(campaign, Mapping) else {}
                resources = config.get("method_resources")
                resources = resources if isinstance(resources, Mapping) else {}
                if (
                    config.get("task_id") != row.get("task_id")
                    or config.get("world_seed") != row.get("world_seed")
                    or not isinstance(config.get("prior_arms"), Mapping)
                    or set(config.get("prior_arms", {})) != set(RESOURCE_CALIBRATION_ARMS)
                    or campaign.get("complete_experiments") != expected_rounds
                    or tuple(campaign.get("checkpoint_complete_experiments", []))
                    != RESOURCE_CALIBRATION_CHECKPOINTS[expected_rounds]
                    or resources.get("complete_experiment_limit") != expected_rounds
                ):
                    errors.append(
                        f"resource calibration {expected_rounds}-round campaign config "
                        "differs from its frozen pattern"
                    )
        else:
            ready = False
        if expected_rounds == 12 and row.get("locus") != "A_S":
            errors.append("12-round calibration representative must be A-S owned")
    expected_status = "ready_authorization_blocked" if ready else "not_ready_fail_closed"
    if manifest.get("status") != expected_status:
        errors.append("resource calibration manifest status differs from task selection state")
    if ready:
        errors.extend(
            _validate_ready_representative_provenance(root, manifest, patterns)
        )
        errors.extend(
            _validate_binding(
                root,
                manifest.get("protocol_manifest_binding"),
                "protocol manifest",
            )
        )
        policy = manifest.get("development_binding_policy")
        policy = policy if isinstance(policy, Mapping) else {}
        if any(
            policy.get(field) is not True
            for field in (
                "exact_selected_campaign_configs_bound",
                "selection_and_q2_inputs_bound",
                "release_freeze_deferred",
            )
        ) or any(
            policy.get(field) is not False
            for field in ("whole_tree_hash_required", "clean_worktree_required")
        ):
            errors.append("resource calibration development binding policy is invalid")
    denominators = manifest.get("expected_denominators")
    denominators = denominators if isinstance(denominators, Mapping) else {}
    if denominators != EXPECTED_RESOURCE_CALIBRATION_DENOMINATORS:
        errors.append("resource calibration expected denominators are invalid")
    gate = manifest.get("authorization_gate")
    gate = gate if isinstance(gate, Mapping) else {}
    if any(
        gate.get(field) is not True
        for field in (
            "all_three_representative_tasks_resolved_required",
            "exact_campaign_configs_bound_required",
            "provider_contract_user_confirmation_required",
            "credential_rotation_user_confirmation_required",
            "calibration_currency_ceiling_required",
            "twelve_round_proxy_substitution_forbidden",
        )
    ):
        errors.append("resource calibration authorization gate is incomplete")
    return errors


def build_resource_calibration_readiness(
    root: Path,
    manifest_path: Path,
    summary_path: Path | None = None,
) -> dict[str, Any]:
    """Build a deterministic readiness receipt; this function never authorizes calls."""

    root = root.resolve()
    manifest_path = manifest_path.resolve()
    manifest = _load_object(manifest_path)
    internal_errors = validate_resource_calibration_manifest(root, manifest)
    patterns = manifest.get("patterns")
    effective_patterns = patterns if isinstance(patterns, list) else []

    def project_pattern_readiness(
        rows: Sequence[Mapping[str, Any] | object],
    ) -> list[dict[str, Any]]:
        projected: list[dict[str, Any]] = []
        for row in rows:
            if not isinstance(row, Mapping):
                continue
            selected = (
                isinstance(row.get("task_id"), str)
                and isinstance(row.get("campaign_config_binding"), Mapping)
                and row.get("task_specific_resource_formula_frozen") is True
            )
            projected.append(
                {
                    "rounds": row.get("rounds"),
                    "locus": row.get("locus"),
                    "representative_task_status": row.get(
                        "representative_task_status"
                    ),
                    "representative_task_selected_and_frozen": selected,
                    "task_id": row.get("task_id"),
                    "world_seed": row.get("world_seed"),
                    "campaign_config_binding": row.get("campaign_config_binding"),
                    "ready": selected,
                }
            )
        return projected

    pattern_rows = project_pattern_readiness(effective_patterns)
    missing_rounds = [row["rounds"] for row in pattern_rows if not row["ready"]]
    representative_resolution: dict[str, Any] | None = None
    representative_blockers: list[str] = []
    if missing_rounds:
        try:
            effective_patterns, representative_resolution = (
                resolve_resource_calibration_representatives(
                    root,
                    manifest,
                    formal_design_path=(
                        root / DEFAULT_RESOURCE_CALIBRATION_FORMAL_DESIGN
                    ),
                    selection_protocol_paths={
                        locus: root / path
                        for locus, path in (
                            DEFAULT_RESOURCE_CALIBRATION_SELECTION_PROTOCOLS.items()
                        )
                    },
                    q2_generation_record_paths={
                        locus: root / path
                        for locus, path in (
                            DEFAULT_RESOURCE_CALIBRATION_Q2_GENERATION_RECORDS.items()
                        )
                    },
                )
            )
        except (OSError, TypeError, ValueError) as error:
            representative_blockers.append(
                f"final representative resolution failed closed: {error}"
            )
        else:
            representative_blockers.extend(
                str(item)
                for item in representative_resolution.get(
                    "blocking_requirements", []
                )
            )
            # The checked-in protocol is intentionally a pre-evidence template. Its
            # pending labels must not hide representatives that the protected,
            # outcome-blind selection and Q2 contracts already resolve. Readiness is
            # therefore projected from the deterministic resolution result.
            pattern_rows = project_pattern_readiness(effective_patterns)
            missing_rounds = [
                row["rounds"] for row in pattern_rows if not row["ready"]
            ]
    source_commit = git_source_commit(root)
    summary: dict[str, Any] | None = None
    summary_errors: list[str] = []
    summary_binding: dict[str, Any] | None = None
    summary_requested = summary_path is not None
    if summary_path is not None:
        summary_path = summary_path.resolve()
        try:
            summary_relative = summary_path.relative_to(root).as_posix()
        except ValueError:
            summary_errors.append("resource calibration summary escapes the repository")
        else:
            if not summary_path.is_file():
                summary_errors.append("resource calibration summary is missing")
            else:
                summary = _load_object(summary_path)
                summary_errors.extend(
                    validate_resource_calibration_summary(
                        summary,
                        manifest=manifest,
                        root=root,
                    )
                )
                summary_binding = {
                    "path": summary_relative,
                    "file_sha256": file_sha256(summary_path),
                    "summary_sha256": summary.get("summary_sha256"),
                }
    summary_present = summary is not None
    summary_passed = (
        summary is not None
        and not summary_errors
        and summary.get("status") == "passed"
        and summary.get("calibration_passed") is True
        and summary.get("method_qualification_may_be_authorized") is True
    )
    base_ready = not missing_rounds and not internal_errors
    method_qualification_may_be_authorized = base_ready and summary_passed
    if not base_ready:
        status = "not_ready_fail_closed"
    elif not summary_present and not summary_requested:
        status = "ready_authorization_blocked"
    elif method_qualification_may_be_authorized:
        status = "calibration_passed_method_qualification_eligible"
    else:
        status = "calibration_failed_fail_closed"
    blockers = [
        *internal_errors,
        *(
            representative_blockers
            or [
                f"{rounds}-round representative task/config is not "
                "terminal-selected and frozen"
                for rounds in missing_rounds
            ]
        ),
        *(
            ["user must confirm the provider contract and credential rotation"]
            if not summary_present
            else []
        ),
        *(
            ["user must approve a calibration-only currency ceiling"]
            if not summary_present
            else []
        ),
        *(["all three pattern triplets remain unexecuted"] if not summary_present else []),
        *(
            ["the bound calibration summary is absent, invalid, or did not pass"]
            if summary_present and not summary_passed
            else []
        ),
    ]
    report: dict[str, Any] = {
        "schema_version": RESOURCE_CALIBRATION_READINESS_VERSION,
        "status": status,
        "formal_result": False,
        "provider_execution_allowed": False,
        "provider_calls_executed": 0,
        "formal_participant_outcome_count": 0,
        "manifest_binding": {
            "path": manifest_path.relative_to(root).as_posix(),
            "file_sha256": file_sha256(manifest_path),
            "canonical_json_sha256": canonical_json_sha256(manifest),
        },
        "development_runtime_commit_observed": source_commit,
        "clean_worktree_required": False,
        "whole_tree_hash_required": False,
        "pattern_readiness": pattern_rows,
        "representative_resolution": representative_resolution,
        "expected_denominators": manifest.get("expected_denominators"),
        "missing_pattern_rounds": missing_rounds,
        "calibration_summary_present": summary_present,
        "calibration_summary_requested": summary_requested,
        "calibration_summary_binding": summary_binding,
        "calibration_summary_status": summary.get("status") if summary else None,
        "calibration_summary_source_commit": (
            summary.get("source_commit") if summary else None
        ),
        "calibration_summary_passed": summary_passed,
        "calibration_summary_errors": summary_errors,
        "method_qualification_may_be_authorized": (
            method_qualification_may_be_authorized
        ),
        "blocking_requirements": blockers,
        "internal_errors": internal_errors,
    }
    report["readiness_sha256"] = resource_calibration_readiness_sha256(report)
    return report


def validate_resource_calibration_readiness(report: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if report.get("schema_version") != RESOURCE_CALIBRATION_READINESS_VERSION:
        errors.append("unexpected resource calibration readiness schema")
    if report.get("readiness_sha256") != resource_calibration_readiness_sha256(report):
        errors.append("resource calibration readiness self-hash mismatch")
    if report.get("status") not in {
        "not_ready_fail_closed",
        "ready_authorization_blocked",
        "calibration_passed_method_qualification_eligible",
        "calibration_failed_fail_closed",
    }:
        errors.append("resource calibration readiness has an invalid status")
    if report.get("internal_errors") != []:
        errors.append("resource calibration readiness has internal errors")
    if (
        report.get("formal_result") is not False
        or report.get("provider_execution_allowed") is not False
        or report.get("provider_calls_executed") != 0
        or report.get("formal_participant_outcome_count") != 0
    ):
        errors.append("resource calibration readiness crossed the execution boundary")
    patterns = report.get("pattern_readiness")
    patterns = patterns if isinstance(patterns, list) else []
    if tuple(row.get("rounds") for row in patterns if isinstance(row, Mapping)) != (
        RESOURCE_CALIBRATION_ROUNDS
    ):
        errors.append("resource calibration readiness lacks 8/10/12 pattern rows")
    missing = report.get("missing_pattern_rounds")
    if not isinstance(missing, list) or any(
        rounds not in RESOURCE_CALIBRATION_ROUNDS for rounds in missing
    ):
        errors.append("resource calibration readiness has invalid missing pattern rounds")
    else:
        projected_missing = [
            row.get("rounds")
            for row in patterns
            if isinstance(row, Mapping) and row.get("ready") is not True
        ]
        if missing != projected_missing:
            errors.append(
                "resource calibration missing rounds differ from pattern readiness"
            )
        summary_present = report.get("calibration_summary_present") is True
        summary_passed = report.get("calibration_summary_passed") is True
        summary_errors = report.get("calibration_summary_errors")
        if not isinstance(summary_errors, list):
            errors.append("resource calibration readiness lacks summary validation errors")
            summary_errors = ["malformed"]
        if (
            report.get("clean_worktree_required") is not False
            or report.get("whole_tree_hash_required") is not False
            or missing
        ):
            expected_status = "not_ready_fail_closed"
        elif not summary_present and report.get("calibration_summary_requested") is not True:
            expected_status = "ready_authorization_blocked"
        elif summary_passed and not summary_errors:
            expected_status = "calibration_passed_method_qualification_eligible"
        else:
            expected_status = "calibration_failed_fail_closed"
        if report.get("status") != expected_status:
            errors.append("resource calibration readiness status differs from missing patterns")
        may_authorize = report.get("method_qualification_may_be_authorized") is True
        if may_authorize != (
            expected_status == "calibration_passed_method_qualification_eligible"
        ):
            errors.append("resource calibration readiness has an invalid authorization decision")
        if summary_present != isinstance(
            report.get("calibration_summary_binding"), Mapping
        ):
            errors.append("resource calibration readiness summary binding is inconsistent")
    return errors


def empty_resource_calibration_summary(manifest: Mapping[str, Any]) -> dict[str, Any]:
    """Return the required machine-summary skeleton without claiming execution."""

    summary: dict[str, Any] = {
        "schema_version": RESOURCE_CALIBRATION_SUMMARY_VERSION,
        "status": "not_executed",
        "formal_result": False,
        "provider_calls_executed": 0,
        "manifest_sha256": canonical_json_sha256(manifest),
        "source_commit": None,
        "expected_denominators": manifest.get("expected_denominators"),
        "observed_denominators": {
            "pattern_triplets_started": 0,
            "pattern_triplets_terminal": 0,
            "cells_started": 0,
            "cells_terminal": 0,
            "complete_experiments": 0,
            "belief_checkpoints": 0,
            "provider_sessions": 0,
            "participant_model_calls": 0,
        },
        "pattern_summaries": [],
        "cell_summaries": [],
        "all_failures": [],
        "resource_card_proposals": [],
        "calibration_passed": False,
        "method_qualification_may_be_authorized": False,
    }
    summary["summary_sha256"] = resource_calibration_summary_sha256(summary)
    return summary


def _is_nonnegative_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0


def _validate_passed_cell_summary(
    cell: Mapping[str, Any],
    *,
    expected_rounds: int,
    expected_locus: str,
    expected_task_id: str,
    expected_world_seed: int,
    expected_arm: str,
) -> list[str]:
    errors: list[str] = []
    identity = (
        cell.get("rounds"),
        cell.get("locus"),
        cell.get("task_id"),
        cell.get("world_seed"),
        cell.get("arm"),
    )
    expected_identity = (
        expected_rounds,
        expected_locus,
        expected_task_id,
        expected_world_seed,
        expected_arm,
    )
    if identity != expected_identity:
        errors.append(f"resource calibration cell identity is invalid: {expected_identity}")
    required_true = (
        "terminal",
        "calibration_passed",
        "typed_checkpoints_valid",
        "final_recommendation_committed",
        "lifecycle_closed",
        "exact_replay_verified",
        "resource_ledgers_reconciled",
    )
    if cell.get("status") != "passed" or any(
        cell.get(field) is not True for field in required_true
    ):
        errors.append(f"resource calibration cell did not pass: {expected_identity}")
    if cell.get("complete_experiments") != expected_rounds:
        errors.append(f"resource calibration cell denominator is invalid: {expected_identity}")
    if tuple(cell.get("checkpoint_complete_experiments", [])) != (
        RESOURCE_CALIBRATION_CHECKPOINTS[expected_rounds]
    ):
        errors.append(f"resource calibration cell checkpoints are invalid: {expected_identity}")
    for field in (
        "unique_recipe_count",
        "exact_repeat_count",
        "operation_attempts",
        "committed_operations",
    ):
        if not _is_nonnegative_number(cell.get(field)):
            errors.append(f"resource calibration cell lacks {field}: {expected_identity}")
    process = cell.get("process_resources")
    process = process if isinstance(process, Mapping) else {}
    for field in (
        "process_time_used_s",
        "required_stage_max_s",
        "repeat_allowance_s",
        "protected_closeout_reserve_s",
        "protected_closeout_reserve_consumed_s",
    ):
        if not _is_nonnegative_number(process.get(field)):
            errors.append(
                f"resource calibration cell process resources lack {field}: "
                f"{expected_identity}"
            )
    if not isinstance(process.get("reserve_consumption_by_operation_class"), Mapping):
        errors.append(
            "resource calibration cell lacks reserve consumption classes: "
            f"{expected_identity}"
        )
    provider = cell.get("provider_resources")
    provider = provider if isinstance(provider, Mapping) else {}
    for field in (
        "input_tokens",
        "cache_hit_input_tokens",
        "uncached_input_tokens",
        "output_tokens",
        "provider_elapsed_s",
        "provider_attempts",
        "mcp_recovery_count",
        "mcp_error_count",
        "observed_currency_usd",
    ):
        if not _is_nonnegative_number(provider.get(field)):
            errors.append(
                f"resource calibration cell provider resources lack {field}: "
                f"{expected_identity}"
            )
    failures = cell.get("failure_counts")
    failures = failures if isinstance(failures, Mapping) else {}
    for field in (
        "resource_rejection",
        "unsafe_outcome",
        "dynamic_physical_failure",
        "provider_error",
        "platform_execution_failure",
    ):
        if not _is_nonnegative_number(failures.get(field)):
            errors.append(
                f"resource calibration cell failure accounting lacks {field}: "
                f"{expected_identity}"
            )
    if failures.get("provider_error") != 0 or failures.get(
        "platform_execution_failure"
    ) != 0:
        errors.append(
            f"passed resource calibration cell contains platform failures: {expected_identity}"
        )
    return errors


def validate_resource_calibration_summary(
    summary: Mapping[str, Any],
    *,
    manifest: Mapping[str, Any] | None = None,
    expected_source_commit: str | None = None,
    root: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    if summary.get("schema_version") != RESOURCE_CALIBRATION_SUMMARY_VERSION:
        errors.append("unexpected resource calibration summary schema")
    if summary.get("summary_sha256") != resource_calibration_summary_sha256(summary):
        errors.append("resource calibration summary self-hash mismatch")
    status = summary.get("status")
    if manifest is not None:
        if summary.get("manifest_sha256") != canonical_json_sha256(manifest):
            errors.append("resource calibration summary manifest binding is stale")
        if summary.get("expected_denominators") != manifest.get(
            "expected_denominators"
        ):
            errors.append("resource calibration summary manifest denominators differ")
    if expected_source_commit is not None and summary.get(
        "source_commit"
    ) != expected_source_commit:
        errors.append("resource calibration summary source commit is stale")
    if root is not None and isinstance(summary.get("c2_source_binding"), Mapping):
        from chemworld.eval.work_ii_c2_admission import validate_c2_source_binding

        c2_binding = summary.get("c2_source_binding")
        c2_binding = c2_binding if isinstance(c2_binding, Mapping) else {}
        if summary.get("source_commit") != c2_binding.get("tested_commit"):
            errors.append(
                "resource calibration summary source commit differs from its C2 binding"
            )
        errors.extend(validate_c2_source_binding(root.resolve(), c2_binding))
    if status == "not_executed":
        if (
            summary.get("provider_calls_executed") != 0
            or summary.get("pattern_summaries") != []
            or summary.get("cell_summaries") != []
            or summary.get("resource_card_proposals") != []
            or summary.get("calibration_passed") is not False
            or summary.get("method_qualification_may_be_authorized") is not False
        ):
            errors.append("unexecuted resource calibration summary claims results")
    elif status not in {"passed", "failed", "invalidated_platform_defect"}:
        errors.append("resource calibration summary has an invalid status")
    elif status != "passed":
        if (
            summary.get("calibration_passed") is not False
            or summary.get("method_qualification_may_be_authorized") is not False
            or not isinstance(summary.get("all_failures"), list)
            or not summary.get("all_failures")
        ):
            errors.append("failed resource calibration summary is not fail-closed")
    else:
        if manifest is None:
            errors.append("passed resource calibration summary requires its manifest")
            return errors
        if (
            summary.get("formal_result") is not False
            or summary.get("calibration_passed") is not True
            or summary.get("method_qualification_may_be_authorized") is not True
            or summary.get("provider_calls_executed") != 9
            or summary.get("expected_denominators")
            != EXPECTED_RESOURCE_CALIBRATION_DENOMINATORS
            or summary.get("observed_denominators")
            != EXPECTED_RESOURCE_CALIBRATION_OBSERVED_DENOMINATORS
        ):
            errors.append("passed resource calibration summary denominators are invalid")
        patterns = manifest.get("patterns")
        patterns = patterns if isinstance(patterns, list) else []
        pattern_summaries = summary.get("pattern_summaries")
        pattern_summaries = (
            pattern_summaries if isinstance(pattern_summaries, list) else []
        )
        cells = summary.get("cell_summaries")
        cells = cells if isinstance(cells, list) else []
        proposals = summary.get("resource_card_proposals")
        proposals = proposals if isinstance(proposals, list) else []
        if len(patterns) != 3 or len(pattern_summaries) != 3:
            errors.append("passed resource calibration summary lacks three pattern rows")
        if len(cells) != 9:
            errors.append("passed resource calibration summary lacks nine cell rows")
        if len(proposals) != 3:
            errors.append("passed resource calibration summary lacks three resource cards")
        seen_cells: set[tuple[object, ...]] = set()
        recalculated_complete = 0
        recalculated_checkpoints = 0
        recalculated_sessions = 0
        recalculated_calls = 0
        for manifest_row in patterns:
            if not isinstance(manifest_row, Mapping):
                continue
            rounds = manifest_row.get("rounds")
            locus = manifest_row.get("locus")
            task_id = manifest_row.get("task_id")
            world_seed = manifest_row.get("world_seed")
            if (
                rounds not in RESOURCE_CALIBRATION_ROUNDS
                or not isinstance(locus, str)
                or not isinstance(task_id, str)
                or not isinstance(world_seed, int)
            ):
                errors.append("passed summary is bound to an unselected pattern")
                continue
            pattern_matches = [
                row
                for row in pattern_summaries
                if isinstance(row, Mapping) and row.get("rounds") == rounds
            ]
            expected_complete = rounds * len(RESOURCE_CALIBRATION_ARMS)
            if len(pattern_matches) != 1 or any(
                pattern_matches[0].get(field) != value
                for field, value in (
                    ("locus", locus),
                    ("task_id", task_id),
                    ("world_seed", world_seed),
                    ("cell_count", 3),
                    ("cells_terminal", 3),
                    ("complete_experiments", expected_complete),
                    ("belief_checkpoints", 15),
                    ("triplet_passed", True),
                    ("platform_defect_detected", False),
                )
            ):
                errors.append(f"passed resource calibration pattern {rounds} is invalid")
            for arm in RESOURCE_CALIBRATION_ARMS:
                key = (rounds, locus, task_id, world_seed, arm)
                matches = [
                    cell
                    for cell in cells
                    if isinstance(cell, Mapping)
                    and (
                        cell.get("rounds"),
                        cell.get("locus"),
                        cell.get("task_id"),
                        cell.get("world_seed"),
                        cell.get("arm"),
                    )
                    == key
                ]
                if len(matches) != 1:
                    errors.append(f"passed resource calibration cell is missing: {key}")
                    continue
                seen_cells.add(key)
                recalculated_complete += int(matches[0].get("complete_experiments", 0))
                recalculated_checkpoints += len(
                    matches[0].get("checkpoint_complete_experiments", [])
                )
                provider_resources = matches[0].get("provider_resources")
                provider_resources = (
                    provider_resources
                    if isinstance(provider_resources, Mapping)
                    else {}
                )
                recalculated_sessions += int(
                    provider_resources.get("provider_attempts") == 1
                )
                recalculated_calls += int(
                    provider_resources.get("provider_attempts") == 1
                )
                errors.extend(
                    _validate_passed_cell_summary(
                        matches[0],
                        expected_rounds=rounds,
                        expected_locus=locus,
                        expected_task_id=task_id,
                        expected_world_seed=world_seed,
                        expected_arm=arm,
                    )
                )
            cards = [
                card
                for card in proposals
                if isinstance(card, Mapping) and card.get("rounds") == rounds
            ]
            if len(cards) != 1 or cards[0].get("locus") != locus:
                errors.append(f"passed resource calibration card {rounds} is missing")
                continue
            card = cards[0]
            observed = card.get("observed_maxima")
            observed = observed if isinstance(observed, Mapping) else {}
            caps = card.get("proposed_hard_caps")
            caps = caps if isinstance(caps, Mapping) else {}
            if card.get("protected_closeout_reserve_enforced") is not True:
                errors.append(f"resource calibration card {rounds} lacks closeout reserve")
            for cap_field in RESOURCE_CALIBRATION_CAP_FIELDS:
                if not _is_nonnegative_number(caps.get(cap_field)):
                    errors.append(
                        f"resource calibration card {rounds} lacks cap {cap_field}"
                    )
            for cap_field, observed_field in RESOURCE_CALIBRATION_OBSERVED_FIELDS.items():
                cap = caps.get(cap_field)
                maximum = observed.get(observed_field)
                if (
                    isinstance(maximum, bool)
                    or not isinstance(maximum, (int, float))
                    or maximum < 0
                    or isinstance(cap, bool)
                    or not isinstance(cap, (int, float))
                    or cap < 0
                    or cap < maximum
                ):
                    errors.append(
                        f"resource calibration card {rounds} cap is below "
                        f"{observed_field}"
                    )
        if len(seen_cells) != len(cells):
            errors.append("passed resource calibration summary has duplicate or extra cells")
        observed = summary.get("observed_denominators")
        observed = observed if isinstance(observed, Mapping) else {}
        recalculated = {
            "pattern_triplets_started": len(patterns),
            "pattern_triplets_terminal": sum(
                row.get("platform_defect_detected") is False
                for row in pattern_summaries
                if isinstance(row, Mapping)
            ),
            "cells_started": len(cells),
            "cells_terminal": sum(
                row.get("terminal") is True for row in cells if isinstance(row, Mapping)
            ),
            "complete_experiments": recalculated_complete,
            "belief_checkpoints": recalculated_checkpoints,
            "provider_sessions": recalculated_sessions,
            "participant_model_calls": recalculated_calls,
        }
        if dict(observed) != recalculated:
            errors.append("passed resource calibration denominators differ from cell rows")
        if summary.get("all_failures") != []:
            errors.append("passed resource calibration summary contains failures")
    return errors


def _mapping(value: object) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def build_resource_calibration_summary(
    manifest: Mapping[str, Any],
    reports: list[Mapping[str, Any]],
    *,
    source_commit: str,
    c2_source_binding: Mapping[str, Any] | None = None,
    observed_currency_usd_by_cell: Mapping[str, float] | None = None,
) -> dict[str, Any]:
    """Aggregate three completed triplet reports into the strict W2-26 contract."""

    currency = observed_currency_usd_by_cell or {}
    cells: list[dict[str, Any]] = []
    patterns: list[dict[str, Any]] = []
    proposals: list[dict[str, Any]] = []
    all_failures: list[dict[str, Any]] = []
    provider_attempts = 0
    accepted_provider_sessions = 0
    for pattern in manifest.get("patterns", []):
        if not isinstance(pattern, Mapping):
            continue
        rounds = int(pattern["rounds"])
        matches = [
            report
            for report in reports
            if report.get("world_seed") == pattern.get("world_seed")
            and report.get("config_file_sha256")
            == _mapping(pattern.get("campaign_config_binding")).get("sha256")
        ]
        report = matches[0] if len(matches) == 1 else {}
        campaign_contract = _mapping(report.get("calibration_campaign_contract"))
        campaign_policy = _mapping(campaign_contract.get("process_time_policy"))
        closeout_policy = _mapping(campaign_contract.get("closeout_policy"))
        report_rows = report.get("results")
        report_rows = report_rows if isinstance(report_rows, list) else []
        pattern_platform_defect = len(matches) != 1 or len(report_rows) != 3
        maxima: dict[str, float] = {
            "operation_attempts": 0,
            "exact_repeat_count": 0,
            "process_time_used_s": 0,
            "input_tokens": 0,
            "uncached_input_tokens": 0,
            "output_tokens": 0,
            "provider_elapsed_s": 0,
            "observed_currency_usd": 0,
        }
        pattern_complete = 0
        pattern_checkpoints = 0
        for arm in RESOURCE_CALIBRATION_ARMS:
            arm_rows = [
                row
                for row in report_rows
                if isinstance(row, Mapping) and row.get("arm") == arm
            ]
            if len(arm_rows) != 1:
                pattern_platform_defect = True
                all_failures.append(
                    {
                        "rounds": rounds,
                        "arm": arm,
                        "class": "platform_execution_failure",
                        "detail": "terminal cell report is missing or duplicated",
                    }
                )
                continue
            row = arm_rows[0]
            analysis = _mapping(row.get("analysis"))
            qualification = _mapping(row.get("qualification"))
            replay = _mapping(row.get("exact_replay"))
            resources = _mapping(analysis.get("final_campaign_resources"))
            state = _mapping(resources.get("state"))
            counts = _mapping(_mapping(analysis.get("process_profile")).get("counts"))
            method = _mapping(row.get("method_resources"))
            receipts = row.get("provider_receipts")
            receipts = receipts if isinstance(receipts, list) else []
            receipt = _mapping(receipts[0]) if len(receipts) == 1 else {}
            report_only = _mapping(state.get("report_only"))
            process_time = float(report_only.get("process_time_s", 0.0))
            operation_attempts = int(
                analysis.get(
                    "operation_attempt_count",
                    counts.get("participant_operation_attempt_count", 0),
                )
            )
            committed = int(counts.get("committed_operation_count", 0))
            provider_attempts += int(receipt.get("provider_attempt_count", 1))
            accepted_provider_sessions += int(
                len(receipts) == 1 and receipt.get("status") == "completed"
            )
            cell_id = f"{rounds}:{pattern['task_id']}:{pattern['world_seed']}:{arm}"
            checkpoint_stages = [
                snapshot.get("stage")
                for snapshot in analysis.get("belief_snapshots", [])
                if isinstance(snapshot, Mapping)
            ]
            failure = row.get("failure")
            checks = _mapping(qualification.get("checks"))
            platform_checks = (
                "tool_integrity",
                "exact_replay",
                "execution_audit",
            )
            platform_failure = (
                len(receipts) != 1
                or receipt.get("provider_error_event_count", 0) != 0
                or method.get("provider_usage_pending") is not False
                or method.get("provider_usage_accounting_complete") is not True
                or method.get("in_flight_model_call_count") != 0
                or any(checks.get(field) is not True for field in platform_checks)
            )
            if platform_failure:
                pattern_platform_defect = True
                all_failures.append(
                    {
                        "rounds": rounds,
                        "arm": arm,
                        "class": "platform_execution_failure",
                        "detail": failure
                        or "provider, replay, accounting, or harness check failed",
                    }
                )
            complete = int(analysis.get("complete_experiment_count", 0))
            pattern_complete += complete
            pattern_checkpoints += len(checkpoint_stages)
            cell_passed = (
                not platform_failure
                and row.get("completed") is True
                and qualification.get("passed") is True
                and replay.get("verified") is True
                and complete == rounds
            )
            if not cell_passed and not platform_failure:
                all_failures.append(
                    {
                        "rounds": rounds,
                        "arm": arm,
                        "class": "participant_scientific_or_method_failure",
                        "detail": qualification.get("failed_checks", []),
                        "retained": True,
                    }
                )
            provider_error_count = int(receipt.get("provider_error_event_count", 0))
            cell = {
                "rounds": rounds,
                "locus": pattern["locus"],
                "task_id": pattern["task_id"],
                "world_seed": pattern["world_seed"],
                "arm": arm,
                "status": "passed" if cell_passed else (
                    "platform_defect" if platform_failure else "method_failure_retained"
                ),
                "terminal": not platform_failure,
                "calibration_passed": cell_passed,
                "complete_experiments": complete,
                "unique_recipe_count": int(analysis.get("unique_recipe_count", 0)),
                "exact_repeat_count": int(analysis.get("exact_repeat_count", 0)),
                "operation_attempts": operation_attempts,
                "committed_operations": committed,
                "checkpoint_complete_experiments": list(
                    RESOURCE_CALIBRATION_CHECKPOINTS[rounds]
                ),
                "checkpoint_stages": checkpoint_stages,
                "typed_checkpoints_valid": qualification.get("checks", {}).get(
                    "typed_belief_checkpoints_complete"
                )
                is True,
                "final_recommendation_committed": qualification.get("checks", {}).get(
                    "final_recommendation_committed"
                )
                is True,
                "lifecycle_closed": qualification.get("checks", {}).get(
                    "campaign_terminal"
                )
                is True,
                "exact_replay_verified": replay.get("verified") is True,
                "resource_ledgers_reconciled": qualification.get("checks", {}).get(
                    "process_time_reconciled"
                )
                is True
                and qualification.get("checks", {}).get(
                    "provider_usage_reconciled"
                )
                is True,
                "process_resources": {
                    "process_time_used_s": process_time,
                    "required_stage_max_s": float(
                        campaign_policy.get("required_stage_max_s", 0.0)
                    ),
                    "repeat_allowance_s": float(
                        campaign_policy.get("repeat_allowance_s", 0.0)
                    ),
                    "protected_closeout_reserve_s": float(
                        campaign_policy.get("protected_reserve_s", 0.0)
                    ),
                    "protected_closeout_reserve_consumed_s": float(
                        report_only.get("protected_reserve_consumed_s", 0.0)
                    ),
                    "reserve_consumption_by_operation_class": dict(
                        _mapping(report_only.get("reserve_consumption_by_operation_class"))
                    ),
                },
                "provider_resources": {
                    "input_tokens": int(method.get("input_token_count", 0)),
                    "cache_hit_input_tokens": int(method.get("input_token_count", 0))
                    - int(method.get("uncached_input_token_count", 0)),
                    "uncached_input_tokens": int(
                        method.get("uncached_input_token_count", 0)
                    ),
                    "output_tokens": int(method.get("output_token_count", 0)),
                    "provider_elapsed_s": float(receipt.get("session_elapsed_s", 0.0)),
                    "provider_attempts": int(receipt.get("provider_attempt_count", 1)),
                    "mcp_recovery_count": int(
                        receipt.get("recovered_mcp_tool_failure_count", 0)
                    ),
                    "mcp_error_count": int(
                        receipt.get("maximum_consecutive_mcp_tool_failure_count", 0)
                    ),
                    "observed_currency_usd": float(currency.get(cell_id, 0.0)),
                },
                "failure_counts": {
                    "resource_rejection": int(
                        analysis.get("resource_rejection_count", 0)
                    ),
                    "unsafe_outcome": int(analysis.get("unsafe_outcome_count", 0)),
                    "dynamic_physical_failure": int(
                        analysis.get("dynamic_physical_failure_count", 0)
                    ),
                    "provider_error": provider_error_count,
                    "platform_execution_failure": int(platform_failure),
                },
            }
            cells.append(cell)
            for field in maxima:
                source = cell["process_resources"] if field == "process_time_used_s" else (
                    cell["provider_resources"]
                    if field
                    in {
                        "input_tokens",
                        "uncached_input_tokens",
                        "output_tokens",
                        "provider_elapsed_s",
                        "observed_currency_usd",
                    }
                    else cell
                )
                maxima[field] = max(maxima[field], float(source[field]))
        triplet_passed = (
            not pattern_platform_defect
            and len([cell for cell in cells if cell["rounds"] == rounds]) == 3
            and all(
                cell["calibration_passed"]
                for cell in cells
                if cell["rounds"] == rounds
            )
        )
        patterns.append(
            {
                "rounds": rounds,
                "locus": pattern["locus"],
                "task_id": pattern["task_id"],
                "world_seed": pattern["world_seed"],
                "cell_count": 3,
                "cells_terminal": sum(
                    cell["terminal"] for cell in cells if cell["rounds"] == rounds
                ),
                "complete_experiments": pattern_complete,
                "belief_checkpoints": pattern_checkpoints,
                "triplet_passed": triplet_passed,
                "platform_defect_detected": pattern_platform_defect,
            }
        )
        proposals.append(
            {
                "rounds": rounds,
                "locus": pattern["locus"],
                "observed_maxima": maxima,
                "protected_closeout_reserve_enforced": True,
                "proposed_hard_caps": {
                    "operation_attempt_limit": int(maxima["operation_attempts"]),
                    "protected_closeout_operation_reserve": int(
                        closeout_policy.get(
                            "final_assay_path_total_operation_reserve", 0
                        )
                    ),
                    "maximum_exact_repeats": int(maxima["exact_repeat_count"]),
                    "process_time_limit_s": maxima["process_time_used_s"]
                    + max(
                        (
                            cell["process_resources"][
                                "protected_closeout_reserve_s"
                            ]
                            for cell in cells
                            if cell["rounds"] == rounds
                        ),
                        default=0.0,
                    ),
                    "protected_closeout_reserve_s": max(
                        (
                            cell["process_resources"][
                                "protected_closeout_reserve_s"
                            ]
                            for cell in cells
                            if cell["rounds"] == rounds
                        ),
                        default=0.0,
                    ),
                    "input_token_limit": int(maxima["input_tokens"]),
                    "uncached_input_token_limit": int(
                        maxima["uncached_input_tokens"]
                    ),
                    "output_token_limit": int(maxima["output_tokens"]),
                    "provider_wall_time_limit_s": maxima["provider_elapsed_s"],
                    "currency_ceiling_usd": maxima["observed_currency_usd"],
                },
            }
        )
    platform_defect = any(row["platform_defect_detected"] for row in patterns)
    passed = (
        len(cells) == 9
        and len(patterns) == 3
        and not platform_defect
        and all(row["triplet_passed"] for row in patterns)
    )
    observed = {
        "pattern_triplets_started": len(patterns),
        "pattern_triplets_terminal": sum(
            not row["platform_defect_detected"] for row in patterns
        ),
        "cells_started": len(cells),
        "cells_terminal": sum(row["terminal"] for row in cells),
        "complete_experiments": sum(row["complete_experiments"] for row in cells),
        "belief_checkpoints": sum(len(row["checkpoint_stages"]) for row in cells),
        "provider_sessions": sum(
            row["provider_resources"]["provider_attempts"] > 0 for row in cells
        ),
        "participant_model_calls": sum(
            row["provider_resources"]["provider_attempts"] > 0 for row in cells
        ),
    }
    summary: dict[str, Any] = {
        "schema_version": RESOURCE_CALIBRATION_SUMMARY_VERSION,
        "status": "invalidated_platform_defect" if platform_defect else (
            "passed" if passed else "failed"
        ),
        "formal_result": False,
        "provider_calls_executed": accepted_provider_sessions,
        "provider_process_attempts_executed": provider_attempts,
        "manifest_sha256": canonical_json_sha256(manifest),
        "source_commit": source_commit,
        "c2_source_binding": None,
        "development_binding_policy": manifest.get("development_binding_policy"),
        "expected_denominators": manifest.get("expected_denominators"),
        "observed_denominators": observed,
        "pattern_summaries": patterns,
        "cell_summaries": cells,
        "all_failures": all_failures,
        "resource_card_proposals": proposals,
        "calibration_passed": passed,
        "method_qualification_may_be_authorized": passed,
    }
    summary["summary_sha256"] = resource_calibration_summary_sha256(summary)
    return summary


__all__ = [
    "RESOURCE_CALIBRATION_MANIFEST_VERSION",
    "RESOURCE_CALIBRATION_READINESS_VERSION",
    "RESOURCE_CALIBRATION_SUMMARY_VERSION",
    "build_resource_calibration_authorization",
    "build_resource_calibration_execution_manifest",
    "build_resource_calibration_readiness",
    "build_resource_calibration_summary",
    "empty_resource_calibration_summary",
    "resolve_resource_calibration_representatives",
    "resource_calibration_authorization_sha256",
    "resource_calibration_readiness_sha256",
    "resource_calibration_summary_sha256",
    "validate_resource_calibration_authorization",
    "validate_resource_calibration_manifest",
    "validate_resource_calibration_readiness",
    "validate_resource_calibration_summary",
]
