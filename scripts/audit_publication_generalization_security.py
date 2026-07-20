"""Audit axis controls, invariance support, and executable exploit probes."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from chemworld.agents.task_recipes import task_recipe_event_count
from chemworld.data.submission import git_commit
from chemworld.eval.generalization import compare_publication_distribution_shift
from chemworld.eval.publication_evidence import payload_sha256
from chemworld.eval.publication_security import (
    DEFAULT_GENERALIZATION_SECURITY_PATH,
    audit_exploit_resistance,
    audit_generalization_controls,
    load_generalization_security_protocol,
)
from chemworld.eval.suite import run_suite
from chemworld.tasks import SERIOUS_TASK_IDS, get_task


def _tracked_tree_dirty() -> bool:
    completed = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        check=True,
        capture_output=True,
        text=True,
    )
    return bool(completed.stdout.strip())


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--protocol",
        type=Path,
        default=DEFAULT_GENERALIZATION_SECURITY_PATH,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "workstreams/benchmark_v1/reports/"
            "publication-generalization-security-summary.json"
        ),
    )
    parser.add_argument(
        "--run-evaluation-mode",
        choices=("public_seed_ood", "salted_private_eval"),
    )
    parser.add_argument(
        "--reference-results",
        type=Path,
        default=Path("runs/publication/protocol-v0.1/full/baseline_results.json"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("runs/publication/generalization-security-v0.1"),
    )
    parser.add_argument(
        "--combine-evidence",
        action="store_true",
        help="Combine existing public-OOD and salted-private formal runs.",
    )
    args = parser.parse_args()

    protocol = load_generalization_security_protocol(args.protocol)
    controls = audit_generalization_controls(protocol)
    if args.combine_evidence:
        return _combine_evidence(
            protocol=protocol,
            controls=controls,
            reference_results_path=args.reference_results,
            run_root=args.output_dir,
            output_path=args.output,
        )
    if args.run_evaluation_mode is not None:
        return _run_distribution_shift(
            mode_id=args.run_evaluation_mode,
            protocol=protocol,
            controls=controls,
            reference_results_path=args.reference_results,
            output_root=args.output_dir,
        )
    exploits = audit_exploit_resistance()
    publication_ready = controls["generalization_ready"] and exploits["passed"]
    report = {
        "schema_version": "chemworld-publication-generalization-security-audit-0.1",
        "status": "ready" if publication_ready else "blocked",
        "publication_ready": publication_ready,
        "controls": controls,
        "exploit_resistance": exploits,
    }
    _write_json(args.output, report)
    print(
        json.dumps(
            {
                "output": str(args.output),
                "status": report["status"],
                "axis_generalization_ready": controls["axis_generalization_ready"],
                "invariance_ready": controls["invariance_ready"],
                "exploit_resistance_passed": exploits["passed"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def _load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _combine_evidence(
    *,
    protocol: dict,
    controls: dict,
    reference_results_path: Path,
    run_root: Path,
    output_path: Path,
) -> int:
    reference = _load_json(reference_results_path)
    if not isinstance(reference, list):
        raise ValueError("reference results must be a JSON list")
    shifts: dict[str, dict] = {}
    manifests: dict[str, dict] = {}
    protocol_bindings: dict[str, bool] = {}
    active_protocol_sha256 = payload_sha256(protocol)
    for mode_id in ("public_seed_ood", "salted_private_eval"):
        root = run_root / mode_id
        manifest = _load_json(root / "manifest.json")
        shifted = _load_json(root / "baseline_results.json")
        if not isinstance(manifest, dict) or not isinstance(shifted, list):
            raise ValueError(f"{mode_id} formal artifacts have invalid JSON shapes")
        actual_digest = hashlib.sha256(
            (root / "baseline_results.json").read_bytes()
        ).hexdigest()
        if actual_digest != manifest.get("baseline_results_sha256"):
            raise ValueError(f"{mode_id} result digest does not match its manifest")
        protocol_bindings[mode_id] = (
            manifest.get("generalization_security_protocol_sha256")
            == active_protocol_sha256
        )
        if protocol_bindings[mode_id]:
            shifts[mode_id] = compare_publication_distribution_shift(
                reference,
                shifted,
                shift_id=mode_id,
            )
        else:
            shift_audit_path = root / "shift_audit.json"
            expected_audit_digest = manifest.get("shift_audit_sha256")
            if (
                isinstance(expected_audit_digest, str)
                and hashlib.sha256(shift_audit_path.read_bytes()).hexdigest()
                != expected_audit_digest
            ):
                raise ValueError(f"{mode_id} shift-audit digest does not match its manifest")
            historical_shift = _load_json(shift_audit_path)
            if not isinstance(historical_shift, dict):
                raise ValueError(f"{mode_id} shift audit has an invalid JSON shape")
            shifts[mode_id] = {
                **historical_shift,
                "active_protocol_binding_valid": False,
                "evidence_role": "historical_diagnostic_only",
            }
        manifests[mode_id] = {
            "evaluated_source_commit": manifest["evaluated_source_commit"],
            "evaluation_source_tree_dirty": manifest["evaluation_source_tree_dirty"],
            "baseline_results_sha256": manifest["baseline_results_sha256"],
            "result_count": manifest["result_count"],
            "private_salt_sha256": manifest.get("private_salt_sha256"),
            "raw_private_salt_published": manifest["raw_private_salt_published"],
            "active_protocol_binding_valid": protocol_bindings[mode_id],
        }
    exploits = audit_exploit_resistance()
    shift_ready = all(
        shift["passed"] and protocol_bindings[mode_id]
        for mode_id, shift in shifts.items()
    )
    publication_ready = (
        controls["generalization_ready"] and exploits["passed"] and shift_ready
    )
    report = {
        "schema_version": "chemworld-publication-generalization-security-audit-0.1",
        "status": "ready" if publication_ready else "blocked",
        "publication_ready": publication_ready,
        "controls": controls,
        "exploit_resistance": exploits,
        "distribution_shifts": shifts,
        "formal_run_manifests": manifests,
        "gates": {
            "axis_generalization_ready": controls["axis_generalization_ready"],
            "invariance_ready": controls["invariance_ready"],
            "exploit_resistance_passed": exploits["passed"],
            "distribution_shift_protocol_bindings_valid": all(
                protocol_bindings.values()
            ),
            "public_seed_ood_passed": (
                shifts["public_seed_ood"]["passed"]
                and protocol_bindings["public_seed_ood"]
            ),
            "salted_private_eval_passed": (
                shifts["salted_private_eval"]["passed"]
                and protocol_bindings["salted_private_eval"]
            ),
        },
    }
    _write_json(output_path, report)
    print(
        json.dumps(
            {
                "output": str(output_path),
                "status": report["status"],
                "publication_ready": publication_ready,
                "gates": report["gates"],
                "ready_task_counts": {
                    mode: shift["ready_task_count"] for mode, shift in shifts.items()
                },
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def _run_distribution_shift(
    *,
    mode_id: str,
    protocol: dict,
    controls: dict,
    reference_results_path: Path,
    output_root: Path,
) -> int:
    if not controls["protocol_valid"]:
        raise ValueError("generalization-security protocol is invalid")
    if _tracked_tree_dirty():
        raise RuntimeError("Formal distribution-shift runs require a clean tracked tree")
    commit = git_commit()
    if commit is None:
        raise RuntimeError("Formal distribution-shift runs require a Git commit")
    mode = protocol["evaluation_modes"][mode_id]
    salt_hash = None
    if mode_id == "salted_private_eval":
        environment_name = str(mode["salt_environment_variable"])
        salt = os.environ.get(environment_name)
        if not salt:
            raise ValueError(f"{environment_name} is required for salted private evaluation")
        salt_hash = hashlib.sha256(salt.encode("utf-8")).hexdigest()

    methods = [str(method) for method in protocol["methods"]]
    seeds = [int(seed) for seed in mode["seeds"]]
    complete_experiments = int(protocol["complete_experiments_per_task_seed"])
    root = output_root / mode_id
    results: list[dict] = []
    for task_id in SERIOUS_TASK_IDS:
        task = get_task(task_id)
        budget = task_recipe_event_count(task.to_dict()) * complete_experiments
        for method in methods:
            method_results = run_suite(
                agent_name=method,
                env_id=task.env_id,
                world_splits=[str(mode["world_split"])],
                seeds=seeds,
                budget=task.budget,
                budget_override=budget,
                objective=task.objective,
                output_dir=root / "runs" / task_id / method,
                threshold=task.threshold,
                task_id=task_id,
            )
            for result in method_results:
                result.update(
                    {
                        "task_id": task_id,
                        "baseline_agent": method,
                        "evaluation_budget_steps": budget,
                        "evaluated_complete_experiments": complete_experiments,
                        "generalization_security_protocol_id": protocol["protocol_id"],
                        "generalization_security_protocol_sha256": payload_sha256(protocol),
                        "evaluated_source_commit": commit,
                        "evaluation_source_tree_dirty": False,
                    }
                )
                if (
                    result["resource_usage"]["complete_experiment_count"]
                    != complete_experiments
                ):
                    raise RuntimeError("distribution-shift run has incomplete experiments")
            results.extend(method_results)

    reference_results = json.loads(reference_results_path.read_text(encoding="utf-8"))
    if not isinstance(reference_results, list):
        raise ValueError("reference results must be a JSON list")
    results_path = root / "baseline_results.json"
    _write_json(results_path, results)
    audit = compare_publication_distribution_shift(
        reference_results,
        results,
        shift_id=mode_id,
    )
    audit.update(
        {
            "evaluated_source_commit": commit,
            "evaluation_source_tree_dirty": False,
            "generalization_security_protocol_sha256": payload_sha256(protocol),
            "reference_results_sha256": hashlib.sha256(
                reference_results_path.read_bytes()
            ).hexdigest(),
            "shifted_results_sha256": hashlib.sha256(results_path.read_bytes()).hexdigest(),
            "private_salt_sha256": salt_hash,
            "raw_private_salt_published": False,
        }
    )
    audit_path = root / "shift_audit.json"
    _write_json(audit_path, audit)
    manifest = {
        "schema_version": "chemworld-publication-shift-run-0.1",
        "status": "completed",
        "generated_at": datetime.now(UTC).isoformat(),
        "mode_id": mode_id,
        "world_split": mode["world_split"],
        "methods": methods,
        "tasks": list(SERIOUS_TASK_IDS),
        "seeds": seeds,
        "complete_experiments_per_task_seed": complete_experiments,
        "result_count": len(results),
        "evaluated_source_commit": commit,
        "evaluation_source_tree_dirty": False,
        "generalization_security_protocol_sha256": payload_sha256(protocol),
        "baseline_results": str(results_path),
        "baseline_results_sha256": hashlib.sha256(results_path.read_bytes()).hexdigest(),
        "shift_audit": str(audit_path),
        "shift_audit_sha256": hashlib.sha256(audit_path.read_bytes()).hexdigest(),
        "private_salt_sha256": salt_hash,
        "raw_private_salt_published": False,
    }
    _write_json(root / "manifest.json", manifest)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
