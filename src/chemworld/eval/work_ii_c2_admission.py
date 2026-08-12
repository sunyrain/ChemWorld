"""Fail-closed admission contract for the complete Work II C2 programme."""

from __future__ import annotations

import json
import re
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    git_source_commit,
)
from chemworld.eval.work_ii_source_binding import work_ii_material_tree_sha256

C2_ADMISSION_PLAN_VERSION = "chemworld-work-ii-c2-admission-plan-0.1"
C2_ADMISSION_REPORT_VERSION = "chemworld-work-ii-c2-admission-report-0.1"
C2_TASK_ADMISSION_RECEIPT_VERSION = "chemworld-work-ii-c2-task-admission-receipt-0.1"
C2_LOCI = ("A_P", "A_S")
C2_REQUIRED_TASK_COUNTS = {"A_P": 2, "A_S": 2}
C2_REQUIRED_ROUNDS = {"A_P": 10, "A_S": 12}
C2_PUBLIC_AE_CELL_COUNT = 75
C2_MATERIAL_SOURCE_ROOTS = (
    "configs/benchmark",
    "configs/foundation",
    "configs/mechanisms",
    "configs/methods",
    "configs/scenarios",
    "pyproject.toml",
    "scripts/run_work_ii_ae_prior_qualification.py",
    "scripts/run_work_ii_resource_calibration.py",
    "src/chemworld",
    "uv.lock",
)
C2_MATERIAL_SOURCE_EXCLUSIONS = (
    "configs/benchmark/work_ii_c2_admission_manifest_v0.1.json",
)


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _self_hash(payload: Mapping[str, Any], field: str) -> str:
    return canonical_json_sha256(
        {key: value for key, value in payload.items() if key != field}
    )


def c2_admission_sha256(report: Mapping[str, Any]) -> str:
    return _self_hash(report, "admission_sha256")


def c2_task_admission_receipt_sha256(receipt: Mapping[str, Any]) -> str:
    return _self_hash(receipt, "receipt_sha256")


def _is_commit(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value) is not None


def build_c2_source_binding(root: Path) -> dict[str, Any]:
    return {
        "schema_version": "chemworld-work-ii-c2-source-binding-0.1",
        "tested_commit": git_source_commit(root),
        "material_tree": {
            "relative_roots": list(C2_MATERIAL_SOURCE_ROOTS),
            "excluded_relative_paths": list(C2_MATERIAL_SOURCE_EXCLUSIONS),
            "sha256": work_ii_material_tree_sha256(
                root,
                relative_roots=C2_MATERIAL_SOURCE_ROOTS,
                excluded_relative_paths=C2_MATERIAL_SOURCE_EXCLUSIONS,
            ),
        },
    }


def validate_c2_source_binding(root: Path, binding: object) -> list[str]:
    if not isinstance(binding, Mapping):
        return ["C2 source binding is missing"]
    errors: list[str] = []
    if binding.get("schema_version") != "chemworld-work-ii-c2-source-binding-0.1":
        errors.append("unexpected C2 source-binding schema")
    tested_commit = binding.get("tested_commit")
    if not _is_commit(tested_commit):
        errors.append("C2 source binding tested commit is invalid")
    else:
        completed = subprocess.run(
            ["git", "merge-base", "--is-ancestor", tested_commit, git_source_commit(root)],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            errors.append("C2 source binding tested commit is not an ancestor of HEAD")
    material = binding.get("material_tree")
    material = material if isinstance(material, Mapping) else {}
    if (
        material.get("relative_roots") != list(C2_MATERIAL_SOURCE_ROOTS)
        or material.get("excluded_relative_paths")
        != list(C2_MATERIAL_SOURCE_EXCLUSIONS)
    ):
        errors.append("C2 protected material-source roster mismatch")
    else:
        try:
            current = work_ii_material_tree_sha256(
                root,
                relative_roots=C2_MATERIAL_SOURCE_ROOTS,
                excluded_relative_paths=C2_MATERIAL_SOURCE_EXCLUSIONS,
            )
        except ValueError as error:
            errors.append(f"C2 protected material tree cannot be rebuilt: {error}")
        else:
            if material.get("sha256") != current:
                errors.append("C2 protected material tree changed after evidence execution")
    return errors


def _binding(root: Path, path: Path, *, embedded_hash: str | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {
        "path": path.resolve().relative_to(root.resolve()).as_posix(),
        "sha256": file_sha256(path),
    }
    if embedded_hash is not None:
        value["embedded_sha256"] = embedded_hash
    return value


def _schedule_binding(cells: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "block": "A_E",
        "public_schedule_cell_count": len(cells),
        "public_schedule_sha256": canonical_json_sha256(list(cells)),
        "schedule_owner": "formal_preflight.cells",
    }


def _plan_errors(plan: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if plan.get("schema_version") != C2_ADMISSION_PLAN_VERSION:
        errors.append("unexpected C2 admission plan schema")
    if (
        plan.get("program_scope") != "C2"
        or plan.get("status") not in {"not_ready_fail_closed", "candidate_evidence_frozen"}
        or plan.get("formal_execution_allowed") is not False
    ):
        errors.append("C2 admission plan does not preserve its non-execution boundary")
    required = plan.get("required_blocks")
    required = required if isinstance(required, Mapping) else {}
    if set(required) != {"A_E", "A_P", "A_S"}:
        errors.append("C2 admission plan does not contain exactly A_E, A_P and A_S")
    ae = required.get("A_E")
    ae = ae if isinstance(ae, Mapping) else {}
    if ae.get("public_schedule_cell_count") != C2_PUBLIC_AE_CELL_COUNT:
        errors.append("C2 admission plan changed the 75-cell A_E public subblock")
    for locus in C2_LOCI:
        block = required.get(locus)
        block = block if isinstance(block, Mapping) else {}
        if (
            block.get("required_terminal_task_count") != C2_REQUIRED_TASK_COUNTS[locus]
            or block.get("complete_experiments_per_cell") != C2_REQUIRED_ROUNDS[locus]
            or not isinstance(block.get("task_admission_receipt_paths"), list)
        ):
            errors.append(f"C2 admission plan changed the frozen {locus} contract")
    calibration = plan.get("resource_calibration")
    calibration = calibration if isinstance(calibration, Mapping) else {}
    if (
        calibration.get("work_item") != "W2-26"
        or calibration.get("manifest_path")
        != "configs/benchmark/work_ii_resource_calibration_manifest_v0.1.json"
    ):
        errors.append("C2 admission plan changed the W2-26 contract")
    freeze = plan.get("freeze_contract")
    freeze = freeze if isinstance(freeze, Mapping) else {}
    expected_freeze = {
        "all_blocks_share_one_runtime_commit": True,
        "clean_worktree_required_at_admission": True,
        "partial_A_E_launch_forbidden": True,
        "participant_outcomes_before_admission": 0,
        "outcome_based_task_selection_forbidden": True,
    }
    if dict(freeze) != expected_freeze:
        errors.append("C2 admission plan changed the shared-freeze contract")
    return errors


def _task_receipt_errors(
    root: Path,
    receipt: Mapping[str, Any],
    *,
    locus: str,
) -> list[str]:
    errors: list[str] = []
    task_id = receipt.get("task_id")
    if receipt.get("schema_version") != C2_TASK_ADMISSION_RECEIPT_VERSION:
        errors.append(f"{locus} task admission has an unexpected schema")
    if receipt.get("receipt_sha256") != c2_task_admission_receipt_sha256(receipt):
        errors.append(f"{locus} task admission receipt self-hash mismatch: {task_id}")
    if (
        receipt.get("status") != "passed_terminal_task_admission"
        or receipt.get("formal_result") is not False
        or receipt.get("terminal_qualification_passed") is not True
        or receipt.get("participant_outcomes_used_for_selection") is not False
        or receipt.get("formal_participant_outcomes_observed") != 0
        or receipt.get("locus") != locus
        or receipt.get("complete_experiments_per_cell") != C2_REQUIRED_ROUNDS[locus]
        or not isinstance(task_id, str)
        or not task_id
    ):
        errors.append(f"{locus} task admission is not a terminal outcome-blind pass: {task_id}")
    errors.extend(validate_c2_source_binding(root, receipt.get("source_binding")))
    for label in ("campaign_config_binding", "qualification_report_binding"):
        binding = receipt.get(label)
        binding = binding if isinstance(binding, Mapping) else {}
        relative = binding.get("path")
        digest = binding.get("sha256")
        if not isinstance(relative, str) or not isinstance(digest, str):
            errors.append(f"{locus} task admission lacks {label}: {task_id}")
            continue
        path = (root / relative).resolve()
        try:
            path.relative_to(root)
        except ValueError:
            errors.append(f"{locus} task admission binding escapes repository: {task_id}")
            continue
        if not path.is_file() or file_sha256(path) != digest:
            errors.append(f"{locus} task admission binding is stale: {task_id}.{label}")
    return errors


def _ae_qualification_errors(
    root: Path,
    report_path: Path,
    design: Mapping[str, Any],
) -> tuple[dict[str, Any] | None, list[str]]:
    if not report_path.is_file():
        return None, ["A_E prior qualification report is missing"]
    report = _load_object(report_path)
    # Local import avoids a module cycle: the qualification plan reuses the
    # frozen A-E checkpoint builder from work_ii_formal.
    from chemworld.eval.work_ii_ae_prior_qualification import (
        validate_qualification_report,
    )

    errors = validate_qualification_report(
        root,
        report,
        design,
        report_path=report_path,
    )
    if report.get("status") != "passed":
        errors.append("A_E prior qualification did not pass")
    errors.extend(validate_c2_source_binding(root, report.get("c2_source_binding")))
    return report, errors


def _resource_calibration_errors(
    root: Path,
    manifest_path: Path,
    summary_path: Path,
) -> tuple[dict[str, Any] | None, list[str]]:
    if not manifest_path.is_file():
        return None, ["W2-26 resource calibration manifest is missing"]
    if not summary_path.is_file():
        return None, ["W2-26 resource calibration summary is missing"]
    manifest = _load_object(manifest_path)
    summary = _load_object(summary_path)
    from chemworld.eval.work_ii_resource_calibration import (
        validate_resource_calibration_manifest,
        validate_resource_calibration_summary,
    )

    errors = validate_resource_calibration_manifest(root, manifest)
    errors.extend(
        validate_resource_calibration_summary(
            summary,
            manifest=manifest,
        )
    )
    if (
        summary.get("status") != "passed"
        or summary.get("calibration_passed") is not True
        or summary.get("method_qualification_may_be_authorized") is not True
    ):
        errors.append("W2-26 resource calibration did not pass")
    errors.extend(validate_c2_source_binding(root, summary.get("c2_source_binding")))
    return summary, errors


def build_c2_admission_report(
    root: Path,
    plan_path: Path,
    design_path: Path,
    ae_public_cells: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Build a truthful current C2 admission report without executing experiments."""

    root = root.resolve()
    plan_path = plan_path.resolve()
    design_path = design_path.resolve()
    plan = _load_object(plan_path)
    design = _load_object(design_path)
    blockers: list[str] = []
    evidence_errors: list[str] = _plan_errors(plan)
    evidence_commits: list[str] = []

    required = plan.get("required_blocks")
    required = required if isinstance(required, Mapping) else {}
    task_rows: dict[str, list[dict[str, Any]]] = {locus: [] for locus in C2_LOCI}
    for locus in C2_LOCI:
        block = required.get(locus)
        block = block if isinstance(block, Mapping) else {}
        paths = block.get("task_admission_receipt_paths")
        paths = paths if isinstance(paths, list) else []
        if len(paths) != C2_REQUIRED_TASK_COUNTS[locus]:
            blockers.append(
                f"{locus} requires exactly {C2_REQUIRED_TASK_COUNTS[locus]} "
                "terminal task admissions"
            )
        for relative in paths:
            if not isinstance(relative, str):
                evidence_errors.append(f"{locus} task admission path is invalid")
                continue
            path = (root / relative).resolve()
            try:
                path.relative_to(root)
            except ValueError:
                evidence_errors.append(f"{locus} task admission path escapes repository")
                continue
            if not path.is_file():
                evidence_errors.append(f"{locus} task admission receipt is missing: {relative}")
                continue
            receipt = _load_object(path)
            receipt_errors = _task_receipt_errors(
                root,
                receipt,
                locus=locus,
            )
            source = receipt.get("source_binding")
            source = source if isinstance(source, Mapping) else {}
            if _is_commit(source.get("tested_commit")):
                evidence_commits.append(str(source["tested_commit"]))
            evidence_errors.extend(receipt_errors)
            task_rows[locus].append(
                {
                    "task_id": receipt.get("task_id"),
                    "receipt_binding": _binding(
                        root,
                        path,
                        embedded_hash=str(receipt.get("receipt_sha256", "")),
                    ),
                    "passed": not receipt_errors,
                }
            )
        task_ids = [row.get("task_id") for row in task_rows[locus]]
        if len(task_ids) != len(set(task_ids)):
            evidence_errors.append(f"{locus} task admission roster contains duplicates")

    ae_block = required.get("A_E")
    ae_block = ae_block if isinstance(ae_block, Mapping) else {}
    ae_path_value = ae_block.get("prior_qualification_report_path")
    ae_report: dict[str, Any] | None = None
    ae_errors: list[str] = []
    if not isinstance(ae_path_value, str) or not ae_path_value:
        blockers.append("A_E prior distinguishability qualification is missing")
    else:
        ae_path = (root / ae_path_value).resolve()
        ae_report, ae_errors = _ae_qualification_errors(
            root,
            ae_path,
            design,
        )
        evidence_errors.extend(ae_errors)
        ae_source = ae_report.get("c2_source_binding") if ae_report else None
        ae_source = ae_source if isinstance(ae_source, Mapping) else {}
        if _is_commit(ae_source.get("tested_commit")):
            evidence_commits.append(str(ae_source["tested_commit"]))

    calibration = plan.get("resource_calibration")
    calibration = calibration if isinstance(calibration, Mapping) else {}
    manifest_value = calibration.get("manifest_path")
    summary_value = calibration.get("summary_path")
    calibration_summary: dict[str, Any] | None = None
    calibration_errors: list[str] = []
    if not isinstance(summary_value, str) or not summary_value:
        blockers.append("W2-26 resource calibration is missing")
    elif not isinstance(manifest_value, str) or not manifest_value:
        evidence_errors.append("W2-26 resource calibration manifest path is invalid")
    else:
        calibration_summary, calibration_errors = _resource_calibration_errors(
            root,
            (root / manifest_value).resolve(),
            (root / summary_value).resolve(),
        )
        evidence_errors.extend(calibration_errors)
        calibration_source = (
            calibration_summary.get("c2_source_binding")
            if calibration_summary
            else None
        )
        calibration_source = (
            calibration_source if isinstance(calibration_source, Mapping) else {}
        )
        if _is_commit(calibration_source.get("tested_commit")):
            evidence_commits.append(str(calibration_source["tested_commit"]))

    expected_evidence_commits = 6
    shared_commits = set(evidence_commits)
    if len(evidence_commits) != expected_evidence_commits or len(shared_commits) != 1:
        blockers.append(
            "A_E, two A_P, two A_S and W2-26 do not prove one shared runtime commit"
        )
    runtime_commit = next(iter(shared_commits)) if len(shared_commits) == 1 else None

    schedule = _schedule_binding(ae_public_cells)
    if (
        len(ae_public_cells) != C2_PUBLIC_AE_CELL_COUNT
        or ae_block.get("public_schedule_cell_count") != C2_PUBLIC_AE_CELL_COUNT
    ):
        evidence_errors.append("A_E public schedule is not the frozen 75-cell subblock")

    blockers.extend(f"invalid evidence: {error}" for error in evidence_errors)
    ready = not blockers
    report: dict[str, Any] = {
        "schema_version": C2_ADMISSION_REPORT_VERSION,
        "status": "ready_for_formal_authorization" if ready else "not_ready_fail_closed",
        "program_scope": "C2",
        "formal_result": False,
        "formal_execution_allowed": ready,
        "plan_binding": _binding(root, plan_path),
        "design_binding": {
            "path": design_path.relative_to(root).as_posix(),
            "sha256": canonical_json_sha256(design),
        },
        "shared_runtime_commit": runtime_commit,
        "blocks": {
            "A_E": {
                "public_schedule": schedule,
                "prior_qualification_binding": (
                    None
                    if ae_report is None or not isinstance(ae_path_value, str)
                    else _binding(
                        root,
                        (root / ae_path_value).resolve(),
                        embedded_hash=str(ae_report.get("report_sha256", "")),
                    )
                ),
                "passed": ae_report is not None and not ae_errors,
            },
            "A_P": {
                "required_terminal_task_count": 2,
                "task_admissions": task_rows["A_P"],
                "passed": len(task_rows["A_P"]) == 2
                and all(row["passed"] for row in task_rows["A_P"]),
            },
            "A_S": {
                "required_terminal_task_count": 2,
                "task_admissions": task_rows["A_S"],
                "passed": len(task_rows["A_S"]) == 2
                and all(row["passed"] for row in task_rows["A_S"]),
            },
        },
        "resource_calibration": {
            "work_item": "W2-26",
            "summary_binding": (
                None
                if calibration_summary is None or not isinstance(summary_value, str)
                else _binding(
                    root,
                    (root / summary_value).resolve(),
                    embedded_hash=str(calibration_summary.get("summary_sha256", "")),
                )
            ),
            "passed": calibration_summary is not None and not calibration_errors,
        },
        "blocking_requirements": blockers,
        "evidence_validation_errors": evidence_errors,
    }
    report["admission_sha256"] = c2_admission_sha256(report)
    return report


def validate_c2_admission_report(
    root: Path,
    report: Mapping[str, Any],
    plan_path: Path,
    design_path: Path,
    ae_public_cells: Sequence[Mapping[str, Any]],
) -> list[str]:
    """Rebuild every evidence binding and reject forged ready-state reports."""

    errors: list[str] = []
    if report.get("schema_version") != C2_ADMISSION_REPORT_VERSION:
        errors.append("unexpected C2 admission report schema")
    if report.get("admission_sha256") != c2_admission_sha256(report):
        errors.append("C2 admission report self-hash mismatch")
    expected = build_c2_admission_report(root, plan_path, design_path, ae_public_cells)
    if dict(report) != expected:
        errors.append("C2 admission report differs from deterministic evidence rebuild")
    ready = report.get("status") == "ready_for_formal_authorization"
    if ready != (report.get("formal_execution_allowed") is True):
        errors.append("C2 admission report has an inconsistent authorization state")
    if ready and (
        report.get("blocking_requirements") != []
        or report.get("evidence_validation_errors") != []
    ):
        errors.append("C2 admission report claims readiness without complete clean evidence")
    return errors


__all__ = [
    "C2_ADMISSION_PLAN_VERSION",
    "C2_ADMISSION_REPORT_VERSION",
    "C2_MATERIAL_SOURCE_EXCLUSIONS",
    "C2_MATERIAL_SOURCE_ROOTS",
    "C2_TASK_ADMISSION_RECEIPT_VERSION",
    "build_c2_admission_report",
    "build_c2_source_binding",
    "c2_admission_sha256",
    "c2_task_admission_receipt_sha256",
    "validate_c2_admission_report",
    "validate_c2_source_binding",
]
