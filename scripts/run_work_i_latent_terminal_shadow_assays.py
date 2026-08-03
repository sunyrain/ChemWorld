"""Freeze, execute, and validate the 36 registered latent-terminal assays."""

from __future__ import annotations

import argparse
import json
import math
import subprocess
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any, cast

from chemworld.envs.chemworld_env import ChemWorldEnv
from chemworld.eval.latent_terminal_contract import (
    FROZEN_MATRIX_MANIFEST_SHA256,
    TERMINAL_INDEX_PATH,
    latent_terminal_contract_sha256,
    validate_latent_terminal_contract,
)
from chemworld.eval.latent_terminal_reconstructability import (
    _historical_resource_prefixes,
    _make_replay_env,
    _read_jsonl,
    _validate_indexed_root,
    discover_run_root,
    reconstructability_report_sha256,
    validate_reconstructability_report,
)
from chemworld.eval.latent_terminal_replay import (
    capture_prefix_identity,
    evaluate_terminal_replacement,
    load_frozen_terminal_contract,
)
from chemworld.eval.provenance import canonical_json_sha256, file_sha256

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = Path("configs/benchmark/work_i_latent_terminal_shadow_assays_v0.1.json")
L02_PATH = Path("workstreams/arxiv_v1/reports/work-i-latent-terminal-reconstructability-v0.1.json")
L03_PATH = Path(
    "workstreams/arxiv_v1/reports/work-i-latent-terminal-replay-qualification-v0.1.json"
)
L04_PATH = Path(
    "workstreams/arxiv_v1/reports/work-i-latent-terminal-analysis-qualification-v0.1.json"
)
PREFLIGHT_PATH = Path(
    "workstreams/arxiv_v1/reports/work-i-latent-terminal-shadow-assay-preflight-v0.1.json"
)
RESULT_PATH = Path("workstreams/arxiv_v1/reports/work-i-latent-terminal-shadow-assays-v0.1.json")
MARKDOWN_PATH = Path("workstreams/arxiv_v1/reports/work-i-latent-terminal-shadow-assays-v0.1.md")
FREEZE_PATHS = (
    PROTOCOL_PATH,
    Path("scripts/run_work_i_latent_terminal_shadow_assays.py"),
    Path("tests/test_work_i_latent_terminal_shadow_assays.py"),
    PREFLIGHT_PATH,
)
EXPECTED_PROTOCOL_SHA256 = "bb033351a9605f9782081962f4ff548faab7e326c58761a661549af8a259f881"
EXPECTED_DISCARD_COUNT = 36
EXPECTED_CELL_COUNT = 10


class ShadowAssayError(RuntimeError):
    """Raised when the frozen shadow-assay boundary is violated."""


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ShadowAssayError(f"expected JSON object: {path}")
    return payload


def _without(payload: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = deepcopy(dict(payload))
    result.pop(field, None)
    return result


def protocol_sha256(payload: Mapping[str, Any]) -> str:
    return canonical_json_sha256(_without(payload, "protocol_sha256"))


def report_sha256(payload: Mapping[str, Any]) -> str:
    return canonical_json_sha256(_without(payload, "report_sha256"))


def _json_text(payload: Mapping[str, Any]) -> str:
    return (
        json.dumps(
            payload,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def validate_protocol(protocol: Mapping[str, Any], *, root: Path) -> list[str]:
    errors: list[str] = []
    if protocol.get("protocol_sha256") != EXPECTED_PROTOCOL_SHA256:
        errors.append("protocol identity is not the executable's frozen identity")
    if protocol_sha256(protocol) != EXPECTED_PROTOCOL_SHA256:
        errors.append("protocol self-hash mismatch")
    if protocol.get("status") != "prospective-formal-frozen":
        errors.append("protocol is not prospectively frozen")
    if protocol.get("population") != {
        "campaign_cells": 10,
        "discarded_lifecycles": 36,
        "observed_assays": 24,
        "original_lifecycles": 60,
        "original_operation_attempts": 889,
    }:
        errors.append("registered population changed")
    if protocol.get("counting_rules") != {
        "agent_provider_calls": 0,
        "formal_population_units": 36,
        "original_agent_experiments_added": 0,
        "same_identity_verification_evaluations": 36,
        "shadow_terminal_assays": 36,
    }:
        errors.append("counting rules changed")
    bindings = protocol.get("dependency_bindings")
    if not isinstance(bindings, Mapping):
        return [*errors, "dependency bindings are missing"]
    for label in (
        "l01_contract",
        "l02_reconstructability",
        "l03_replay_qualification",
        "l04_analysis_qualification",
        "terminal_file_index",
    ):
        binding = bindings.get(label)
        if not isinstance(binding, Mapping):
            errors.append(f"missing dependency binding: {label}")
            continue
        path = root / str(binding.get("path", ""))
        if not path.is_file() or file_sha256(path) != binding.get("file_sha256"):
            errors.append(f"dependency file mismatch: {label}")
    return errors


def _dependency_content_errors(
    protocol: Mapping[str, Any],
    *,
    root: Path,
) -> tuple[list[str], dict[str, Any], dict[str, Any]]:
    errors: list[str] = []
    bindings = cast(Mapping[str, Any], protocol["dependency_bindings"])
    contract = load_frozen_terminal_contract(root)
    errors.extend(validate_latent_terminal_contract(contract, root=root))
    if (
        latent_terminal_contract_sha256(contract)
        != cast(Mapping[str, Any], bindings["l01_contract"])["content_sha256"]
    ):
        errors.append("L01 content identity mismatch")
    l02 = _read_json(root / L02_PATH)
    errors.extend(validate_reconstructability_report(l02, root=root))
    if (
        reconstructability_report_sha256(l02)
        != cast(Mapping[str, Any], bindings["l02_reconstructability"])["content_sha256"]
    ):
        errors.append("L02 content identity mismatch")
    for label, path, accepted_status in (
        ("l03_replay_qualification", L03_PATH, "PASS"),
        ("l04_analysis_qualification", L04_PATH, "qualified"),
    ):
        report = _read_json(root / path)
        binding = cast(Mapping[str, Any], bindings[label])
        if report_sha256(report) != binding["content_sha256"]:
            errors.append(f"{label} content identity mismatch")
        if report.get("status") != accepted_status:
            errors.append(f"{label} status is not qualified")
    return errors, contract, l02


def build_preflight(root: Path, run_root: Path) -> dict[str, Any]:
    """Verify the complete registered population without evaluating a score."""

    protocol = _read_json(root / PROTOCOL_PATH)
    errors = validate_protocol(protocol, root=root)
    dependency_errors, contract, l02 = _dependency_content_errors(
        protocol,
        root=root,
    )
    errors.extend(dependency_errors)
    index = _read_json(root / TERMINAL_INDEX_PATH)
    raw_root_audit = _validate_indexed_root(run_root, index)
    matrix = _read_json(run_root / "matrix_manifest.json")
    bindings = cast(Mapping[str, Any], protocol["dependency_bindings"])
    if matrix.get("manifest_sha256") != FROZEN_MATRIX_MANIFEST_SHA256:
        errors.append("raw matrix manifest identity mismatch")
    if matrix.get("manifest_sha256") != bindings["raw_matrix_manifest_sha256"]:
        errors.append("protocol/raw matrix manifest mismatch")

    contract_cells = contract.get("population", {}).get("cells", [])
    l02_cells = l02.get("cells", [])
    discard_ids = [
        str(unit.get("discard_id"))
        for cell in contract_cells
        if isinstance(cell, Mapping)
        for unit in cell.get("discard_units", [])
        if isinstance(unit, Mapping)
    ]
    l02_units = [
        unit
        for cell in l02_cells
        if isinstance(cell, Mapping)
        for unit in cell.get("discard_units", [])
        if isinstance(unit, Mapping)
    ]
    gates = {
        "protocol_valid": not validate_protocol(protocol, root=root),
        "dependencies_valid": not dependency_errors,
        "registered_10_cells": len(contract_cells) == EXPECTED_CELL_COUNT,
        "registered_36_unique_discards": (
            len(discard_ids) == len(set(discard_ids)) == EXPECTED_DISCARD_COUNT
        ),
        "l02_36_of_36_reconstructable": (
            len(l02_units) == EXPECTED_DISCARD_COUNT
            and all(unit.get("reconstructable") is True for unit in l02_units)
        ),
        "raw_root_exactly_matches_index": raw_root_audit["all_paths_sizes_and_hashes_match"],
        "formal_outcomes_not_accessed": True,
        "formal_shadow_evaluations_zero": True,
        "agent_provider_calls_zero": True,
    }
    errors.extend(name for name, passed in gates.items() if not passed)
    report: dict[str, Any] = {
        "schema_id": "chemworld.latent_terminal_shadow_assay_preflight",
        "schema_version": "0.1.0",
        "report_id": "work-i-latent-terminal-shadow-assay-preflight-v0.1",
        "status": "PASS" if not errors else "FAIL",
        "protocol_sha256": protocol["protocol_sha256"],
        "population_manifest_sha256": contract["population"]["population_manifest_sha256"],
        "raw_matrix_manifest_sha256": matrix["manifest_sha256"],
        "terminal_file_index_sha256": index["index_sha256"],
        "census": {
            "campaign_cells": len(contract_cells),
            "registered_discard_units": len(discard_ids),
            "unique_discard_identities": len(set(discard_ids)),
            "reconstructable_discard_units": sum(
                unit.get("reconstructable") is True for unit in l02_units
            ),
            "formal_shadow_evaluations_executed": 0,
            "formal_shadow_scores_accessed": 0,
            "agent_provider_calls": 0,
        },
        "raw_root_audit": raw_root_audit,
        "gates": gates,
        "errors": sorted(set(errors)),
    }
    report["report_sha256"] = report_sha256(report)
    return report


def validate_preflight(report: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if report.get("status") != "PASS":
        errors.append("preflight did not pass")
    if report.get("report_sha256") != report_sha256(report):
        errors.append("preflight self-hash mismatch")
    gates = report.get("gates")
    if not isinstance(gates, Mapping) or not gates or not all(gates.values()):
        errors.append("preflight gate failed")
    census = report.get("census")
    if (
        not isinstance(census, Mapping)
        or census.get("registered_discard_units") != EXPECTED_DISCARD_COUNT
    ):
        errors.append("preflight population is incomplete")
    if isinstance(census, Mapping) and (
        census.get("formal_shadow_evaluations_executed") != 0
        or census.get("formal_shadow_scores_accessed") != 0
        or census.get("agent_provider_calls") != 0
    ):
        errors.append("preflight crossed the outcome boundary")
    return errors


def _git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def validate_pushed_freeze(root: Path, freeze_commit: str) -> list[str]:
    errors: list[str] = []
    full_commit = _git(root, "rev-parse", f"{freeze_commit}^{{commit}}")
    branch = _git(root, "branch", "--show-current")
    remote_ref = f"origin/{branch}"
    try:
        _git(root, "rev-parse", f"{remote_ref}^{{commit}}")
        _git(root, "merge-base", "--is-ancestor", full_commit, remote_ref)
    except subprocess.CalledProcessError:
        errors.append("freeze commit is not present on the pushed branch")
    status = _git(root, "status", "--porcelain")
    if status:
        errors.append("worktree is not clean at formal start")
    for relative in FREEZE_PATHS:
        try:
            frozen = subprocess.run(
                ["git", "-C", str(root), "show", f"{full_commit}:{relative.as_posix()}"],
                check=True,
                capture_output=True,
            ).stdout
        except subprocess.CalledProcessError:
            errors.append(f"freeze commit lacks {relative.as_posix()}")
            continue
        if frozen != (root / relative).read_bytes():
            errors.append(f"working file differs from freeze: {relative.as_posix()}")
    return errors


def _l02_unit_map(l02: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {
        str(unit["discard_id"]): unit
        for cell in l02.get("cells", [])
        if isinstance(cell, Mapping)
        for unit in cell.get("discard_units", [])
        if isinstance(unit, Mapping)
    }


def _matrix_cell_map(matrix: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {
        str(cell["cell_id"]): cell for cell in matrix.get("cells", []) if isinstance(cell, Mapping)
    }


def _prefix_matches_l02(
    identity: Mapping[str, Any],
    l02_unit: Mapping[str, Any],
) -> bool:
    fields = (
        "discard_id",
        "cell_id",
        "lifecycle_index",
        "terminal_step",
        "terminal_action_sha256",
        "public_prefix_sha256",
        "hidden_state_sha256",
        "campaign_resource_snapshot_sha256",
        "campaign_resource_state_sha256",
    )
    return all(identity.get(field) == l02_unit.get(field) for field in fields)


def _execute_pass(
    *,
    root: Path,
    run_root: Path,
    contract: Mapping[str, Any],
    l02: Mapping[str, Any],
    matrix: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    l02_units = _l02_unit_map(l02)
    matrix_cells = _matrix_cell_map(matrix)
    outputs: dict[str, dict[str, Any]] = {}
    for contract_cell in contract["population"]["cells"]:
        cell_id = str(contract_cell["cell_id"])
        attempt = str(matrix_cells[cell_id]["authoritative_attempt_dir"])
        raw_path = (run_root / attempt / "trajectory.jsonl").resolve()
        records = _read_jsonl(raw_path)
        compact = _read_jsonl(root / str(contract_cell["compact_path"]))
        ledger = _read_json(raw_path.parent / "campaign_resource_ledger.json")
        units_by_step = {
            int(unit["terminal_step"]): unit for unit in contract_cell["discard_units"]
        }
        prefixes = _historical_resource_prefixes(ledger, set(units_by_step))
        env = _make_replay_env(records[0])
        try:
            env.reset(seed=int(records[0]["seed"]))
            base = cast(ChemWorldEnv, env.unwrapped)
            for record in records:
                step = int(record["step"])
                unit = units_by_step.get(step)
                if unit is not None:
                    discard_id = str(unit["discard_id"])
                    try:
                        identity = capture_prefix_identity(
                            base,
                            cell_id=cell_id,
                            lifecycle_index=int(unit["lifecycle_index"]),
                            terminal_step=step,
                            original_discard_action=record["action"],
                            public_prefix_records=compact[: step - 1],
                            authoritative_resource_snapshot=prefixes[step],
                        )
                        if not _prefix_matches_l02(identity, l02_units[discard_id]):
                            raise ShadowAssayError("captured prefix differs from L02")
                        evaluation = evaluate_terminal_replacement(
                            base,
                            expected_identity=identity,
                            original_discard_action=record["action"],
                            public_prefix_records=compact[: step - 1],
                            authoritative_resource_snapshot=prefixes[step],
                            frozen_contract=contract,
                        )
                        outputs[discard_id] = {
                            "status": "resolved",
                            "identity": identity,
                            "evaluation": evaluation,
                        }
                    except Exception as exc:  # full-population failure receipt
                        outputs[discard_id] = {
                            "status": "unresolved",
                            "failure_category": type(exc).__name__,
                            "failure_reason": str(exc),
                        }
                env.step(record["action"])
        except Exception as exc:
            for unit in contract_cell["discard_units"]:
                discard_id = str(unit["discard_id"])
                outputs.setdefault(
                    discard_id,
                    {
                        "status": "unresolved",
                        "failure_category": type(exc).__name__,
                        "failure_reason": str(exc),
                    },
                )
        finally:
            env.close()
    return outputs


def _formal_receipt(
    unit: Mapping[str, Any],
    cell: Mapping[str, Any],
    first: Mapping[str, Any],
    repeat: Mapping[str, Any],
    *,
    contract_sha256: str,
    population_manifest_sha256: str,
) -> dict[str, Any]:
    base: dict[str, Any] = {
        "fixture_kind": "formal_shadow_receipt",
        "contract_sha256": contract_sha256,
        "population_manifest_sha256": population_manifest_sha256,
        "discard_id": unit["discard_id"],
        "cell_id": cell["cell_id"],
        "world_seed": cell["world_seed"],
        "information_arm": cell["information_arm"],
        "lifecycle_index": unit["lifecycle_index"],
        "terminal_step": unit["terminal_step"],
        "public_prefix_sha256": unit["public_prefix_sha256"],
        "terminal_action_sha256": unit["terminal_action_sha256"],
    }
    if first.get("status") != "resolved" or repeat.get("status") != "resolved":
        failed = first if first.get("status") != "resolved" else repeat
        return {
            **base,
            "outcome_status": "unresolved",
            "failure_category": failed.get("failure_category", "replay_failure"),
            "failure_reason": failed.get("failure_reason", "formal replay failed"),
        }
    evaluation = cast(Mapping[str, Any], first["evaluation"])
    replay = cast(Mapping[str, Any], repeat["evaluation"])
    same_identity = all(
        evaluation.get(field) == replay.get(field)
        for field in (
            "leaderboard_score",
            "terminal_evaluation_identity_sha256",
            "shadow_observation_sha256",
            "noise_key_sha256",
        )
    )
    if not same_identity:
        return {
            **base,
            "outcome_status": "unresolved",
            "failure_category": "same_identity_replay_mismatch",
            "failure_reason": "independent formal evaluation identities differ",
        }
    return {
        **base,
        "outcome_status": "resolved",
        "score": evaluation["leaderboard_score"],
        "same_identity_replay": {
            "passed": True,
            "terminal_evaluation_identity_sha256": replay["terminal_evaluation_identity_sha256"],
            "shadow_observation_sha256": replay["shadow_observation_sha256"],
            "noise_key_sha256": replay["noise_key_sha256"],
        },
        "terminal_evaluation": dict(evaluation),
    }


def _raw_source_manifest(
    contract: Mapping[str, Any],
    matrix: Mapping[str, Any],
    run_root: Path,
) -> dict[str, str]:
    matrix_cells = _matrix_cell_map(matrix)
    result: dict[str, str] = {}
    for cell in contract["population"]["cells"]:
        cell_id = str(cell["cell_id"])
        attempt = str(matrix_cells[cell_id]["authoritative_attempt_dir"])
        for name in ("trajectory.jsonl", "campaign_resource_ledger.json"):
            logical = f"{cell_id}/{name}"
            result[logical] = file_sha256(run_root / attempt / name)
    return result


def build_formal_report(root: Path, run_root: Path, freeze_commit: str) -> dict[str, Any]:
    preflight = _read_json(root / PREFLIGHT_PATH)
    errors = validate_preflight(preflight)
    errors.extend(validate_pushed_freeze(root, freeze_commit))
    if errors:
        raise ShadowAssayError("formal freeze invalid: " + "; ".join(errors))
    protocol = _read_json(root / PROTOCOL_PATH)
    dependency_errors, contract, l02 = _dependency_content_errors(
        protocol,
        root=root,
    )
    if dependency_errors:
        raise ShadowAssayError("dependency invalid: " + "; ".join(dependency_errors))
    matrix = _read_json(run_root / "matrix_manifest.json")
    before = _raw_source_manifest(contract, matrix, run_root)
    first = _execute_pass(
        root=root,
        run_root=run_root,
        contract=contract,
        l02=l02,
        matrix=matrix,
    )
    repeat = _execute_pass(
        root=root,
        run_root=run_root,
        contract=contract,
        l02=l02,
        matrix=matrix,
    )
    receipts = [
        _formal_receipt(
            unit,
            cell,
            first[str(unit["discard_id"])],
            repeat[str(unit["discard_id"])],
            contract_sha256=str(contract["contract_sha256"]),
            population_manifest_sha256=str(contract["population"]["population_manifest_sha256"]),
        )
        for cell in contract["population"]["cells"]
        for unit in cell["discard_units"]
    ]
    after = _raw_source_manifest(contract, matrix, run_root)
    resolved = sum(row["outcome_status"] == "resolved" for row in receipts)
    gates = {
        "pushed_freeze_verified_before_first_score": True,
        "complete_registered_population_reported": len(receipts) == 36,
        "all_36_shadow_assays_resolved": resolved == 36,
        "all_36_same_identity_replays_passed": all(
            row.get("same_identity_replay", {}).get("passed") is True for row in receipts
        ),
        "agent_provider_calls_zero": all(
            row.get("terminal_evaluation", {}).get("agent_provider_calls") == 0 for row in receipts
        ),
        "original_environment_unmodified": all(
            row.get("terminal_evaluation", {}).get("original_environment_mutated") is False
            for row in receipts
        ),
        "original_resource_ledger_unmodified": all(
            row.get("terminal_evaluation", {}).get("original_resource_ledger_mutated") is False
            for row in receipts
        ),
        "raw_sources_unchanged": before == after,
        "no_outcome_selection_or_replacement": True,
    }
    report: dict[str, Any] = {
        "schema_id": "chemworld.latent_terminal_shadow_assay_results",
        "schema_version": "0.1.0",
        "report_id": "work-i-latent-terminal-shadow-assays-v0.1",
        "status": "PASS" if all(gates.values()) else "FAIL",
        "freeze_commit": _git(root, "rev-parse", f"{freeze_commit}^{{commit}}"),
        "protocol_sha256": protocol["protocol_sha256"],
        "preflight_report_sha256": preflight["report_sha256"],
        "contract_sha256": contract["contract_sha256"],
        "population_manifest_sha256": contract["population"]["population_manifest_sha256"],
        "counting_rule": {
            "registered_population_units": 36,
            "resolved_units": resolved,
            "unresolved_units": 36 - resolved,
            "formal_shadow_assays": 36,
            "same_identity_verification_evaluations": 36,
            "agent_provider_calls": 0,
            "original_agent_experiments_added": 0,
        },
        "receipts": receipts,
        "raw_source_manifest_before_sha256": canonical_json_sha256(before),
        "raw_source_manifest_after_sha256": canonical_json_sha256(after),
        "gates": gates,
        "analysis_owner": "W1-L06",
    }
    report["report_sha256"] = report_sha256(report)
    return report


def validate_formal_report(report: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if report.get("report_sha256") != report_sha256(report):
        errors.append("formal report self-hash mismatch")
    receipts = report.get("receipts")
    if not isinstance(receipts, list) or len(receipts) != 36:
        errors.append("formal report does not contain 36 receipts")
        receipts = []
    if len({row.get("discard_id") for row in receipts}) != len(receipts):
        errors.append("formal receipt identities are not unique")
    for row in receipts:
        status = row.get("outcome_status")
        score = row.get("score")
        if status == "resolved" and (
            isinstance(score, bool)
            or not isinstance(score, int | float)
            or not math.isfinite(float(score))
            or not 0.0 <= float(score) <= 1.0
        ):
            errors.append(f"invalid resolved score: {row.get('discard_id')}")
        if status not in {"resolved", "unresolved"}:
            errors.append(f"invalid outcome status: {row.get('discard_id')}")
    gates = report.get("gates")
    if report.get("status") == "PASS" and (
        not isinstance(gates, Mapping) or not all(gates.values())
    ):
        errors.append("PASS report has a failed gate")
    return errors


def build_markdown(report: Mapping[str, Any]) -> str:
    counts = cast(Mapping[str, Any], report["counting_rule"])
    return "\n".join(
        [
            "# Work I Latent-Terminal Shadow Assays",
            "",
            f"Status: **{report['status']}**",
            "",
            f"Report SHA-256: `{report['report_sha256']}`",
            f"Freeze commit: `{report['freeze_commit']}`",
            "",
            "## Execution handoff",
            "",
            f"All {counts['registered_population_units']} registered discarded "
            f"lifecycles were reported; {counts['resolved_units']} resolved and "
            f"{counts['unresolved_units']} remained unresolved.",
            "",
            "Each registered unit used one evaluator-only final assay and one "
            "independent same-identity verification. No agent/provider call was made, "
            "no original experiment was added, and source trajectories and resource "
            "ledgers remained unchanged.",
            "",
            "This artifact is an execution receipt, not an inferential analysis. "
            "W1-L06 owns the frozen finite-population analysis.",
            "",
        ]
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--preflight", action="store_true")
    mode.add_argument("--formal", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--freeze-commit")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.preflight:
        run_root = discover_run_root(ROOT)
        report = build_preflight(ROOT, run_root)
        errors = validate_preflight(report)
        if errors:
            raise SystemExit("preflight failed: " + "; ".join(errors))
        (ROOT / PREFLIGHT_PATH).write_text(_json_text(report), encoding="utf-8", newline="\n")
    elif args.formal:
        if not args.freeze_commit:
            raise SystemExit("--formal requires --freeze-commit")
        run_root = discover_run_root(ROOT)
        report = build_formal_report(ROOT, run_root, args.freeze_commit)
        errors = validate_formal_report(report)
        if errors:
            raise SystemExit("formal report invalid: " + "; ".join(errors))
        (ROOT / RESULT_PATH).write_text(_json_text(report), encoding="utf-8", newline="\n")
        (ROOT / MARKDOWN_PATH).write_text(build_markdown(report), encoding="utf-8", newline="\n")
    else:
        report = _read_json(ROOT / RESULT_PATH)
        errors = validate_formal_report(report)
        if errors:
            raise SystemExit("committed formal report invalid: " + "; ".join(errors))
        if (ROOT / MARKDOWN_PATH).read_text(encoding="utf-8") != build_markdown(report):
            raise SystemExit("committed markdown differs from the formal report")
    print(
        json.dumps(
            {
                "status": report["status"],
                "report_sha256": report["report_sha256"],
                "mode": "preflight" if args.preflight else "formal" if args.formal else "check",
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
