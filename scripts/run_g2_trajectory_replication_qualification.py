"""Qualify the fresh-trajectory replication runner with one K1 or K2 cell."""

from __future__ import annotations

import argparse
from collections.abc import Mapping, Sequence
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from scripts import run_g2_autonomous_material_matrix as base
from scripts import run_g2_trajectory_replication as replication

from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    git_source_commit,
    git_worktree_dirty,
    repository_tree_sha256,
    write_json_atomic,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = replication.DEFAULT_CONFIG
DEFAULT_OUTPUT_ROOT = (
    ROOT / "runs/development/g2-trajectory-replication-seed1-r01-nominal-k1-qualification-v1"
)
RUNNER_VERSION = "chemworld-g2-trajectory-replication-qualification-runner-0.1"
MANIFEST_SCHEMA_VERSION = "chemworld-g2-trajectory-replication-qualification-run-0.1"
CONDITION_LABELS = {
    "nominal": "anonymous_nominal_properties",
    "opaque": "opaque_codes",
}


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _source_manifest(config_path: Path) -> dict[str, Any]:
    source_roots = (
        "src/chemworld",
        "scripts/run_g2_autonomous_material_matrix.py",
        "scripts/run_g2_trajectory_replication.py",
        "scripts/run_g2_trajectory_replication_qualification.py",
        config_path.relative_to(ROOT).as_posix(),
    )
    return {
        "git_commit": git_source_commit(ROOT),
        "worktree_dirty": git_worktree_dirty(
            ROOT,
            excluded_prefixes=("runs/development/",),
        ),
        "material_source_roots": list(source_roots),
        "material_source_tree_sha256": repository_tree_sha256(
            ROOT,
            relative_roots=source_roots,
        ),
        "protocol_file": config_path.relative_to(ROOT).as_posix(),
        "protocol_file_sha256": file_sha256(config_path),
        "runner_version": RUNNER_VERSION,
    }


def _qualification_cell(
    protocol: Mapping[str, Any],
    *,
    pair_order: int,
    condition: str,
    world_seed: int | None = None,
) -> dict[str, Any]:
    condition_id = CONDITION_LABELS[condition]
    matches = [
        cell
        for cell in replication._scheduled_cells(protocol)
        if int(cell["pair_order"]) == pair_order and cell["condition_id"] == condition_id
    ]
    if len(matches) != 1:
        raise ValueError("qualification cell is not unique in the frozen schedule")
    cell = deepcopy(matches[0])
    if world_seed is not None:
        if world_seed in {int(seed) for seed in protocol["task"]["world_seeds"]}:
            raise ValueError("qualification world must be outside the formal confirmatory sample")
        cell["world_seed"] = int(world_seed)
        cell["agent_seed"] = 900_000 + int(world_seed)
    cell["cell_id"] = (
        f"qualification-seed{cell['world_seed']}-{cell['trajectory_replicate_id']}-{condition}"
    )
    cell["qualification_pair_order"] = pair_order
    cell["qualification_condition"] = condition
    return cell


def _default_output_root(
    *,
    cell: Mapping[str, Any],
    condition: str,
    experiments: int,
) -> Path:
    if (
        int(cell["world_seed"]) == 1
        and cell["trajectory_replicate_id"] == "r01"
        and condition == "nominal"
        and experiments == 1
    ):
        return DEFAULT_OUTPUT_ROOT
    return (
        ROOT
        / "runs/development"
        / (
            f"g2-trajectory-replication-seed{cell['world_seed']}-"
            f"{cell['trajectory_replicate_id']}-{condition}-k{experiments}-"
            "qualification-v1"
        )
    )


def _manifest_payload(
    *,
    protocol: Mapping[str, Any],
    source: Mapping[str, Any],
    cli: Mapping[str, Any],
    cell: Mapping[str, Any],
    state: Mapping[str, Any],
    started_at: str,
    experiments: int,
    card: Any,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "runner_version": RUNNER_VERSION,
        "protocol_id": protocol["protocol_id"],
        "run_status": state["state"],
        "formal_result": False,
        "confirmatory_claim_allowed": False,
        "started_at": started_at,
        "updated_at": _now(),
        "source": deepcopy(dict(source)),
        "codex_cli": deepcopy(dict(cli)),
        "qualification_experiments": experiments,
        "campaign_resource_card_sha256": card.card_sha256,
        "cell": deepcopy(dict(cell)),
        "cell_state": deepcopy(dict(state)),
    }
    payload["manifest_sha256"] = canonical_json_sha256(payload)
    return payload


def _write_manifest(
    path: Path,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = _manifest_payload(**kwargs)
    write_json_atomic(path, payload)
    return payload


def _validate_resume_manifest(
    path: Path,
    *,
    protocol: Mapping[str, Any],
    source: Mapping[str, Any],
    cli: Mapping[str, Any],
    cell: Mapping[str, Any],
    experiments: int,
) -> str:
    manifest = replication._load_json_object(path, label="qualification manifest")
    unhashed = dict(manifest)
    declared_hash = unhashed.pop("manifest_sha256", None)
    manifest_source = manifest.get("source")
    checks = {
        "content_hash": declared_hash == canonical_json_sha256(unhashed),
        "schema": manifest.get("schema_version") == MANIFEST_SCHEMA_VERSION,
        "runner": manifest.get("runner_version") == RUNNER_VERSION,
        "protocol": manifest.get("protocol_id") == protocol["protocol_id"],
        "cell": manifest.get("cell") == dict(cell),
        "experiments": manifest.get("qualification_experiments") == experiments,
        "source": isinstance(manifest_source, Mapping)
        and manifest_source.get("material_source_tree_sha256")
        == source["material_source_tree_sha256"]
        and manifest_source.get("protocol_file_sha256") == source["protocol_file_sha256"],
        "cli": manifest.get("codex_cli") == dict(cli),
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise RuntimeError("qualification resume identity mismatch: " + ", ".join(failed))
    return str(manifest.get("started_at") or _now())


def _validate_final_state(
    *,
    output_root: Path,
    state: Mapping[str, Any],
    protocol: Mapping[str, Any],
    source: Mapping[str, Any],
    cli: Mapping[str, Any],
    card: Any,
    method_limits: Mapping[str, Any],
) -> None:
    authoritative = state.get("authoritative_attempt_dir")
    if authoritative is None:
        return
    cell = state["cell"]
    attempt_root = output_root / str(authoritative)
    if state["state"] == "completed":
        base._validated_resume_result(
            cell_root=attempt_root,
            cell=cell,
            protocol=protocol,
            source=source,
            cli=cli,
            card=card,
            method_limits=method_limits,
        )
    elif state["state"] == "right_censored":
        replication._validate_attempt_identity(
            attempt_root=attempt_root,
            cell=cell,
            protocol=protocol,
            source=source,
            cli=cli,
            card=card,
            method_limits=method_limits,
        )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument(
        "--pair-order",
        type=int,
        default=1,
    )
    parser.add_argument(
        "--qualification-world-seed",
        type=int,
        help="Use a dedicated world outside the formal protocol world sample.",
    )
    parser.add_argument(
        "--condition",
        choices=tuple(CONDITION_LABELS),
        default="nominal",
    )
    parser.add_argument(
        "--experiments",
        type=int,
        choices=(1, 2),
        default=1,
    )
    parser.add_argument("--resume", action="store_true")
    parser.add_argument(
        "--allow-external-provider",
        action="store_true",
        help="Required opt-in for native Codex execution.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if not args.allow_external_provider:
        raise RuntimeError("external execution requires --allow-external-provider")
    config_path = args.config.resolve()
    protocol = replication._load_protocol(config_path)
    source = _source_manifest(config_path)
    condition = str(args.condition)
    experiments = int(args.experiments)
    cell = _qualification_cell(
        protocol,
        pair_order=int(args.pair_order),
        condition=condition,
        world_seed=args.qualification_world_seed,
    )
    output_root = (
        args.output_root.resolve()
        if args.output_root is not None
        else _default_output_root(
            cell=cell,
            condition=condition,
            experiments=experiments,
        )
    )
    if output_root.exists() and not args.resume:
        raise FileExistsError(f"refusing to overwrite existing output root: {output_root}")
    output_root.mkdir(parents=True, exist_ok=True)
    manifest_path = output_root / "qualification_manifest.json"
    cli = base._codex_cli_manifest()
    card = base._campaign_card(
        protocol,
        qualification=True,
        qualification_experiments=experiments,
    )
    limits = base._method_limits(
        protocol,
        qualification=True,
        qualification_experiments=experiments,
    )
    maximum_attempts = int(
        protocol["attempt_policy"]["maximum_pre_action_provider_attempts_per_cell"]
    )
    started_at = _now()
    if args.resume:
        if not manifest_path.is_file():
            if any(output_root.iterdir()):
                raise RuntimeError(
                    "resume requires qualification_manifest.json in a non-empty root"
                )
        else:
            started_at = _validate_resume_manifest(
                manifest_path,
                protocol=protocol,
                source=source,
                cli=cli,
                cell=cell,
                experiments=experiments,
            )

    while True:
        state = replication._cell_state(
            output_root=output_root,
            cell=cell,
            maximum_pre_action_attempts=maximum_attempts,
        )
        _validate_final_state(
            output_root=output_root,
            state=state,
            protocol=protocol,
            source=source,
            cli=cli,
            card=card,
            method_limits=limits,
        )
        manifest = _write_manifest(
            manifest_path,
            protocol=protocol,
            source=source,
            cli=cli,
            cell=cell,
            state=state,
            started_at=started_at,
            experiments=experiments,
            card=card,
        )
        if state["state"] == "completed":
            return 0
        if state["state"] == "right_censored":
            return 2
        if state["state"] not in {"pending", "pending_provider_retry"}:
            raise RuntimeError(f"qualification cannot continue: {manifest['run_status']}")
        cell_root = output_root / str(cell["cell_id"])
        cell_root.mkdir(parents=True, exist_ok=True)
        attempt_number = len(state["attempts"]) + 1
        attempt_root = cell_root / f"attempt-{attempt_number:02d}"
        try:
            base._run_cell(
                protocol=protocol,
                source=source,
                cli=cli,
                cell=cell,
                cell_root=attempt_root,
                card=card,
                method_limits=limits,
                qualification=True,
            )
        except Exception as error:
            refreshed = replication._cell_state(
                output_root=output_root,
                cell=cell,
                maximum_pre_action_attempts=maximum_attempts,
            )
            _write_manifest(
                manifest_path,
                protocol=protocol,
                source=source,
                cli=cli,
                cell=cell,
                state=refreshed,
                started_at=started_at,
                experiments=experiments,
                card=card,
            )
            if refreshed["state"] in {
                "pending_provider_retry",
                "right_censored",
            }:
                continue
            raise RuntimeError(f"qualification stopped: {refreshed['state']}") from error


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "DEFAULT_CONFIG",
    "DEFAULT_OUTPUT_ROOT",
    "MANIFEST_SCHEMA_VERSION",
    "RUNNER_VERSION",
    "main",
]
