"""Audit the preparatory VLM spectrum-observation contract without loading a model."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
import subprocess
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from chemworld.eval.vlm_observation import prepare_vlm_observation

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "configs" / "benchmark" / "vlm_observation_v0.1.json"
DEFAULT_OUTPUT = ROOT / "workstreams" / "benchmark_v1" / "reports" / "vlm-observation-v0.1.json"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _package_status(import_name: str, distribution_name: str) -> dict[str, Any]:
    installed = importlib.util.find_spec(import_name) is not None
    version = None
    if installed:
        try:
            version = importlib.metadata.version(distribution_name)
        except importlib.metadata.PackageNotFoundError:
            version = "present-version-unavailable"
    return {"declared": True, "installed": installed, "version": version}


def _packet(*, peak: float = 1.0, assignment: str = "public-target") -> dict[str, Any]:
    return {
        "kind": "hplc_chromatogram",
        "instrument_id": "hplc",
        "time_min": [0.0, 1.0, 2.0, 3.0],
        "intensity": [0.0, 0.2, peak, 0.1],
        "peaks": [
            {
                "retention_time_min": 2.0,
                "assignment": assignment,
                "analyte_id": assignment,
            }
        ],
        "assignments": [{"analyte_id": assignment}],
        "metadata": {"synthetic": True},
    }


def _context(*, historical: bool) -> dict[str, Any]:
    requested = (
        {
            "spectrum_id": "spectrum-history-requested",
            "status": "retrieved",
            "raw_signal": _packet(peak=0.7, assignment="historical-target"),
        }
        if historical
        else {}
    )
    return {
        "step": 3,
        "task_id": "yield_optimization_v0",
        "campaign_state": {"remaining_budget": 3},
        "latest_spectra": {
            "spectrum_id": "spectrum-current",
            "raw_signal": _packet(),
        },
        "historical_spectrum_catalog": [
            {
                "spectrum_id": "spectrum-catalog-only",
                "raw_signal": _packet(peak=0.5, assignment="must-not-render"),
            }
        ],
        "requested_historical_spectrum": requested,
    }


def _behavior_checks() -> dict[str, bool]:
    with tempfile.TemporaryDirectory(prefix="chemworld-vlm-audit-") as temp:
        root = Path(temp)
        first = prepare_vlm_observation(
            _context(historical=False),
            artifact_root=root,
            decision_id="audit-decision",
            modality="image_only",
            disclosure="unassigned",
        )
        repeated = prepare_vlm_observation(
            _context(historical=False),
            artifact_root=root,
            decision_id="audit-decision",
            modality="image_only",
            disclosure="unassigned",
        )
        assigned = prepare_vlm_observation(
            _context(historical=False),
            artifact_root=root,
            decision_id="audit-decision",
            modality="image_only",
            disclosure="assigned",
        )
        changed_context = _context(historical=False)
        changed_context["latest_spectra"]["raw_signal"] = _packet(peak=0.6)
        changed = prepare_vlm_observation(
            changed_context,
            artifact_root=root,
            decision_id="audit-decision",
            modality="image_only",
            disclosure="unassigned",
        )
        with_history = prepare_vlm_observation(
            _context(historical=True),
            artifact_root=root,
            decision_id="audit-history",
            modality="image_only",
            disclosure="unassigned",
        )
        masked = prepare_vlm_observation(
            _context(historical=True),
            artifact_root=root,
            decision_id="audit-masked",
            modality="image_plus_numeric",
            disclosure="masked",
        )
        first_image = first.images[0]
        first_manifest = json.dumps(first.to_manifest(), sort_keys=True)
        prompt_text = json.dumps(first.prompt_context, sort_keys=True)
        return {
            "deterministic_png_bytes": first_image.sha256 == repeated.images[0].sha256,
            "deterministic_manifest": first.manifest_hash == repeated.manifest_hash,
            "changed_signal_changes_digest": first_image.signal_sha256
            != changed.images[0].signal_sha256,
            "assigned_unassigned_share_curve": first_image.signal_sha256
            == assigned.images[0].signal_sha256,
            "unassigned_identity_removed": "public-target" not in prompt_text,
            "catalog_signal_not_rendered": len(first.images) == 1
            and "catalog-only" not in first_manifest,
            "requested_history_rendered_only_after_request": len(with_history.images) == 2
            and with_history.images[1].source == "historical",
            "masked_never_renders": not masked.images
            and "intensity" not in str(masked.prompt_context),
            "log_contains_no_embedded_image": "data:image" not in first_manifest
            and "base64" not in first_manifest.lower(),
            "log_contains_no_absolute_path": str(root).lower() not in first_manifest.lower(),
            "png_signature_valid": (root / first_image.relative_path)
            .read_bytes()
            .startswith(b"\x89PNG\r\n\x1a\n"),
        }


def audit(config_path: Path, output_path: Path) -> dict[str, Any]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    pyproject_text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    optional_dependencies = {
        "accelerate": _package_status("accelerate", "accelerate"),
        "pillow": _package_status("PIL", "pillow"),
        "safetensors": _package_status("safetensors", "safetensors"),
        "torch": _package_status("torch", "torch"),
        "transformers": _package_status("transformers", "transformers"),
    }
    declaration_checks = {
        name: f'"{name}' in pyproject_text or (name == "pillow" and '"pillow' in pyproject_text)
        for name in optional_dependencies
    }
    for name, declared in declaration_checks.items():
        optional_dependencies[name]["declared"] = declared

    behavior = _behavior_checks()
    weight_patterns = ("*.safetensors", "pytorch_model*.bin", "*.gguf")
    repository_weights = sorted(
        str(path.relative_to(ROOT)).replace("\\", "/")
        for pattern in weight_patterns
        for path in ROOT.rglob(pattern)
        if ".venv" not in path.parts and ".git" not in path.parts
    )
    output_relative = str(output_path.resolve().relative_to(ROOT)).replace("\\", "/")
    dirty_excluding_report = bool(
        _git("status", "--porcelain", "--", ".", f":(exclude){output_relative}")
    )
    config_safe = (
        config.get("status") == "preparatory_non_gating"
        and config.get("benchmark_claim_allowed") is False
        and config.get("included_in_base_matrix_v0.4") is False
        and config["candidate_runtime"].get("weights_downloaded_by_this_task") is False
        and config["candidate_runtime"].get("execution_authorized_by_this_task") is False
        and config["candidate_runtime"].get("model_revision_must_be_pinned_before_execution")
        is True
    )
    contract_ready = (
        all(behavior.values())
        and all(declaration_checks.values())
        and optional_dependencies["pillow"]["installed"]
        and not repository_weights
        and config_safe
        and not dirty_excluding_report
    )
    runtime_ready = all(item["installed"] for item in optional_dependencies.values())
    return {
        "schema_version": "chemworld-vlm-observation-audit-0.1",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "source_commit": _git("rev-parse", "HEAD"),
        "dirty_tree_excluding_report": dirty_excluding_report,
        "config": {
            "path": str(config_path.relative_to(ROOT)).replace("\\", "/"),
            "sha256": _digest(config_path),
            "preparatory_boundaries_valid": config_safe,
        },
        "dependency_lock": {
            "path": "uv.lock",
            "sha256": _digest(ROOT / "uv.lock"),
            "optional_packages": optional_dependencies,
        },
        "behavior_checks": behavior,
        "repository_model_weight_files": repository_weights,
        "model_download_attempted": False,
        "model_loaded_or_executed": False,
        "provider_network_call_attempted": False,
        "contract_ready": contract_ready,
        "runtime_ready_for_model_execution": runtime_ready,
        "benchmark_claim_allowed": False,
        "limitations": [
            "This audit validates observation delivery, not VLM quality or learning value.",
            "A model and processor revision must be pinned before a one-task Dev pilot.",
            "Optional inference packages may remain uninstalled until that pilot is authorized.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    report = audit(args.config.resolve(), args.output.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["contract_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
