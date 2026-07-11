"""Audit whether ChemWorld serious v1 supports a defensible benchmark claim."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from chemworld.eval.baseline_report import SERIOUS_BASELINE_AGENTS  # type: ignore[import-untyped]
from chemworld.runtime.model_reachability import (  # type: ignore[import-untyped]
    audit_model_reachability,
    audit_shared_claim_ownership,
)
from chemworld.tasks import SERIOUS_TASK_IDS, get_task  # type: ignore[import-untyped]

SCHEMA_VERSION = "chemworld-benchmark-v1-gap-audit-0.1"
SEVERITY_WEIGHT = {"blocker": 5, "major": 3, "minor": 1}
ADAPTIVE_AGENTS = frozenset({"gp_bo", "safe_gp_bo"})
NONADAPTIVE_AGENTS = frozenset({"random", "lhs"})
RL_AGENT_MARKERS = ("ppo", "sac", "dqn", "a2c", "reinforce", "rl_")


@dataclass(frozen=True)
class AuditCheck:
    category: str
    check_id: str
    severity: str
    passed: bool
    observed: Any
    required: str
    remediation: str
    evidence: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["evidence"] = list(self.evidence)
        return payload


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _files(root: Path, pattern: str) -> list[str]:
    return sorted(path.relative_to(root).as_posix() for path in root.glob(pattern))


def _tag_names(root: Path) -> list[str]:
    try:
        completed = subprocess.run(
            ["git", "tag", "--list", "chemworld-serious-v1*"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return []
    return sorted(line.strip() for line in completed.stdout.splitlines() if line.strip())


def _check(
    checks: list[AuditCheck],
    category: str,
    check_id: str,
    severity: str,
    passed: bool,
    observed: Any,
    required: str,
    remediation: str,
    *evidence: str,
) -> None:
    checks.append(
        AuditCheck(
            category=category,
            check_id=check_id,
            severity=severity,
            passed=bool(passed),
            observed=observed,
            required=required,
            remediation=remediation,
            evidence=tuple(evidence),
        )
    )


def _baseline_index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    return {(str(row["task_id"]), str(row["agent_name"])): row for row in rows}


def _intervals_overlap(left: list[float], right: list[float]) -> bool:
    return max(float(left[0]), float(right[0])) <= min(float(left[1]), float(right[1]))


def build_audit(root: Path, *, generalization_report: Path | None = None) -> dict[str, Any]:
    release_dir = root / "benchmark" / "releases" / "chemworld-serious-v1"
    manifest_path = release_dir / "manifest.json"
    baseline_path = release_dir / "baseline_summary.json"
    validation_path = release_dir / "benchmark_validation.json"
    surface_path = release_dir / "response_surface_audit.json"
    manifest = _read_json(manifest_path)
    baseline = _read_json(baseline_path)
    validation = _read_json(validation_path)
    surfaces = _read_json(surface_path)
    rows = [row for row in baseline.get("rows", []) if isinstance(row, dict)]
    indexed = _baseline_index(rows)
    checks: list[AuditCheck] = []
    task_ids = tuple(SERIOUS_TASK_IDS)
    agent_names = tuple(SERIOUS_BASELINE_AGENTS)

    _check(
        checks,
        "claim_contract",
        "six_explicit_serious_tasks",
        "blocker",
        tuple(manifest.get("task_ids", ())) == task_ids,
        manifest.get("task_ids"),
        "The release and runtime must name the same explicit serious-task set.",
        "Rebuild the release after the accepted task set is frozen.",
        "benchmark/releases/chemworld-serious-v1/manifest.json",
    )
    _check(
        checks,
        "claim_contract",
        "per_task_reporting",
        "major",
        manifest.get("reporting_policy") == "per-task; no cross-task aggregate score",
        manifest.get("reporting_policy"),
        "Official results must be reported per task without an opaque aggregate.",
        "Keep per-task tables and define any future aggregate separately.",
        "benchmark/releases/chemworld-serious-v1/manifest.json",
    )
    limitations = (root / "docs" / "limitations.md").read_text(encoding="utf-8")
    _check(
        checks,
        "claim_contract",
        "bounded_non_real_world_claim",
        "blocker",
        "不是\n真实反应预测软件" in limitations and "不可声明" in limitations,
        "explicit non-prediction and non-industrial boundary",
        "The benchmark must not imply real-yield or industrial validity.",
        "Preserve the limitations page in every paper and release artifact.",
        "docs/limitations.md",
    )
    primary_fields = {
        task_id: str(validation["task_evidence"][task_id]["primary_metric_field"])
        for task_id in task_ids
    }
    _check(
        checks,
        "claim_contract",
        "task_specific_primary_metrics",
        "major",
        len(set(primary_fields.values())) == len(task_ids),
        primary_fields,
        "Every serious task must have one explicit, task-specific primary metric.",
        "Resolve any duplicate or ambiguous primary metric before freezing.",
        "benchmark/releases/chemworld-serious-v1/benchmark_validation.json",
    )

    expected_pairs = {(task_id, agent) for task_id in task_ids for agent in agent_names}
    seed_counts = sorted({int(row.get("runs", 0)) for row in rows})
    _check(
        checks,
        "empirical_validity",
        "official_baseline_matrix_complete",
        "blocker",
        set(indexed) == expected_pairs and seed_counts == [5],
        {"rows": len(rows), "run_counts": seed_counts},
        "All official methods must cover all tasks and the declared frozen seeds.",
        "Regenerate missing task-agent cells before comparison.",
        "benchmark/releases/chemworld-serious-v1/baseline_summary.json",
    )
    surface_tasks = surfaces.get("tasks", {})
    surface_counts = {
        task_id: int(surface_tasks[task_id].get("sample_count", 0)) for task_id in task_ids
    }
    _check(
        checks,
        "empirical_validity",
        "response_surface_coverage",
        "major",
        all(count >= 60 for count in surface_counts.values()),
        surface_counts,
        "Each task needs deterministic response-surface probes across all frozen seeds.",
        "Increase or repair task-level probes where coverage is incomplete.",
        "benchmark/releases/chemworld-serious-v1/response_surface_audit.json",
    )
    oracle_failures: dict[str, dict[str, float]] = {}
    for task_id in task_ids:
        oracle = float(surface_tasks[task_id]["approximate_oracle_score"])
        best_baseline = max(
            float(indexed[(task_id, agent)]["mean_total_score"]) for agent in agent_names
        )
        if oracle + 1.0e-12 < best_baseline:
            oracle_failures[task_id] = {"oracle": oracle, "best_baseline": best_baseline}
    _check(
        checks,
        "empirical_validity",
        "oracle_is_valid_upper_reference",
        "blocker",
        not oracle_failures,
        oracle_failures,
        "An oracle/regret reference must dominate every evaluated baseline on its own metric.",
        "Replace one-shot maxima with a campaign-aware oracle or stop calling it an oracle.",
        "benchmark/releases/chemworld-serious-v1/response_surface_audit.json",
        "benchmark/releases/chemworld-serious-v1/baseline_summary.json",
    )
    adaptive_advantages: dict[str, float] = {}
    for task_id in task_ids:
        adaptive = max(
            float(indexed[(task_id, agent)]["mean_total_score"]) for agent in ADAPTIVE_AGENTS
        )
        nonadaptive = max(
            float(indexed[(task_id, agent)]["mean_total_score"]) for agent in NONADAPTIVE_AGENTS
        )
        adaptive_advantages[task_id] = adaptive - nonadaptive
    adaptive_wins = sum(value > 0.01 for value in adaptive_advantages.values())
    _check(
        checks,
        "empirical_validity",
        "adaptive_methods_show_broad_value",
        "blocker",
        adaptive_wins >= 4,
        {"wins_over_0.01": adaptive_wins, "advantages": adaptive_advantages},
        (
            "Adaptive methods should beat task-aware non-adaptive search on most "
            "tasks by a material margin."
        ),
        "Fix task/action encoding and tune adaptive baselines before making an exploration claim.",
        "benchmark/releases/chemworld-serious-v1/baseline_summary.json",
    )
    resolved_tasks: list[str] = []
    for task_id in task_ids:
        ranked = sorted(
            (indexed[(task_id, agent)] for agent in agent_names),
            key=lambda row: float(row["mean_total_score"]),
            reverse=True,
        )
        if not _intervals_overlap(ranked[0]["ci95_total_score"], ranked[1]["ci95_total_score"]):
            resolved_tasks.append(task_id)
    _check(
        checks,
        "empirical_validity",
        "top_method_statistically_resolved",
        "blocker",
        len(resolved_tasks) >= 4,
        {"resolved_task_count": len(resolved_tasks), "resolved_tasks": resolved_tasks},
        (
            "The top two methods should be distinguishable on most tasks at the "
            "declared interval level."
        ),
        (
            "Run a power analysis, increase seeds, and use paired task-seed tests "
            "with multiplicity control."
        ),
        "benchmark/releases/chemworld-serious-v1/baseline_summary.json",
    )
    _check(
        checks,
        "empirical_validity",
        "paper_grade_seed_depth",
        "blocker",
        bool(seed_counts) and min(seed_counts) >= 20,
        seed_counts,
        (
            "Paper claims require a justified seed count, provisionally at least "
            "20 without a power analysis."
        ),
        "Estimate variance and freeze a powered paired-seed protocol.",
        "benchmark/releases/chemworld-serious-v1/baseline_summary.json",
    )

    official_agents = set(agent_names)
    _check(
        checks,
        "method_coverage",
        "traditional_search_baselines",
        "major",
        {"random", "lhs", "scripted_chemistry"}.issubset(official_agents),
        sorted(official_agents),
        "Official evidence must include uninformed, space-filling, and domain-informed baselines.",
        "Retain the three traditional controls in the final experiment matrix.",
        "src/chemworld/eval/baseline_report.py",
    )
    _check(
        checks,
        "method_coverage",
        "diverse_active_learning_family",
        "blocker",
        len({agent for agent in official_agents if "bo" in agent or "forest" in agent}) >= 4,
        sorted(agent for agent in official_agents if "bo" in agent or "forest" in agent),
        "Active-learning evidence should span acquisition functions and surrogate families.",
        "Promote PI/UCB/random-forest or equivalent implementations into the official matrix.",
        "src/chemworld/agents/bo.py",
        "src/chemworld/eval/baseline_report.py",
    )
    rl_agents = sorted(
        agent
        for agent in official_agents
        if any(marker in agent.lower() for marker in RL_AGENT_MARKERS)
    )
    _check(
        checks,
        "method_coverage",
        "reinforcement_learning_baseline",
        "blocker",
        bool(rl_agents),
        rl_agents,
        (
            "At least one trained RL policy with train/eval separation is required "
            "for an RL comparison."
        ),
        "Add PPO/SAC or a justified alternative with frozen checkpoints and held-out evaluation.",
        "src/chemworld/eval/baseline_report.py",
    )
    real_llm_agents = sorted(
        agent
        for agent in official_agents
        if "llm" in agent.lower() and "stub" not in agent.lower() and "replay" not in agent.lower()
    )
    _check(
        checks,
        "method_coverage",
        "real_llm_agent_baseline",
        "blocker",
        bool(real_llm_agents),
        real_llm_agents,
        (
            "LLM conclusions require real model calls, fixed prompts, model "
            "snapshots, budgets, and traces."
        ),
        "Run at least two real LLM families separately from the deterministic stub.",
        "src/chemworld/eval/baseline_report.py",
        "docs/limitations.md",
    )
    resource_fields = {
        key for row in rows for key in row if "token" in key or "wall" in key or "cost" in key
    }
    _check(
        checks,
        "method_coverage",
        "resource_matched_comparison",
        "major",
        {"wall_time_s", "agent_cost"}.issubset(resource_fields),
        sorted(resource_fields),
        (
            "Methods must report comparable environment calls, wall time, model "
            "tokens, and monetary cost."
        ),
        "Add a resource ledger and normalize comparisons by experiment and compute budget.",
        "benchmark/releases/chemworld-serious-v1/baseline_summary.json",
    )

    generalization_path = generalization_report
    generalization = (
        _read_json(generalization_path)
        if generalization_path is not None and generalization_path.exists()
        else None
    )
    rank_correlations: dict[str, float] = {}
    if generalization is not None:
        rank_correlations = {
            task_id: float(
                generalization["tasks"][task_id]["score_diagnostics"]["rank_correlation"]
            )
            for task_id in task_ids
        }
    _check(
        checks,
        "generalization_security",
        "heldout_rank_stability",
        "blocker",
        bool(rank_correlations)
        and min(rank_correlations.values()) >= 0.3
        and sum(value >= 0.5 for value in rank_correlations.values()) >= 4,
        rank_correlations or "not run",
        (
            "Public-to-held-out method rankings must be stable on most tasks and "
            "non-adversarial on all."
        ),
        "Increase OOD seeds and redesign unstable tasks before freezing rankings.",
        str(generalization_path.relative_to(root)) if generalization_path else "not available",
    )
    _check(
        checks,
        "generalization_security",
        "generalization_in_public_release",
        "blocker",
        (release_dir / "generalization_audit.json").exists(),
        (release_dir / "generalization_audit.json").exists(),
        "The public bundle must contain the exact generalization report used by the claim.",
        "Version and hash the accepted generalization matrix in the release manifest.",
        "benchmark/releases/chemworld-serious-v1",
    )
    _check(
        checks,
        "generalization_security",
        "axis_intervention_not_seed_only",
        "blocker",
        False,
        "current audit changes held-out seeds but does not execute named axis interventions",
        "Each declared axis needs explicit in-range, extrapolation, composition, and noise slices.",
        (
            "Implement parameterized world-family interventions rather than "
            "treating new seeds as full OOD."
        ),
        "scripts/audit_serious_generalization.py",
        "src/chemworld/task_design.py",
    )
    private_configs = _files(root, "configs/private_eval*.json")
    _check(
        checks,
        "generalization_security",
        "non_placeholder_private_eval",
        "blocker",
        any("placeholder" not in path for path in private_configs),
        private_configs,
        "A maintainer-side private evaluation must exist without publishing its secret parameters.",
        "Create a separately stored salted private configuration and signed aggregate artifact.",
        *private_configs,
    )
    invariance_files = _files(root, "tests/**/*invar*.py")
    _check(
        checks,
        "generalization_security",
        "policy_invariance_suite",
        "major",
        bool(invariance_files),
        invariance_files,
        (
            "Material remapping, field order, equivalent actions, and observation "
            "formatting need invariance tests."
        ),
        "Add paired metamorphic evaluations for every method family.",
        "tests",
    )
    _check(
        checks,
        "generalization_security",
        "public_observation_leakage_tests",
        "blocker",
        (root / "tests" / "test_public_observation_leakage.py").exists(),
        "dedicated leakage test exists",
        "Agents must not receive hidden scenario or state through public observations.",
        "Keep leakage tests in the release gate and add an out-of-process harness.",
        "tests/test_public_observation_leakage.py",
    )
    exploit_reports = _files(release_dir, "*exploit*") + _files(release_dir, "*anti_gaming*")
    _check(
        checks,
        "generalization_security",
        "published_exploit_audit",
        "blocker",
        bool(exploit_reports),
        exploit_reports,
        (
            "The release must publish replay, budget, invalid-action, termination, "
            "assay, and float exploit results."
        ),
        "Build an executable exploit matrix and bind its digest into the release.",
        "benchmark/releases/chemworld-serious-v1",
    )

    adapter_paths = _files(root, "workstreams/world_foundation/adapters/*.json")
    adapters = [_read_json(root / path) for path in adapter_paths]
    replacement_adapters = [
        str(adapter["adapter_id"]) for adapter in adapters if adapter.get("replaces_model_ids")
    ]
    reachability = audit_model_reachability()
    claim_ownership = audit_shared_claim_ownership(root)
    reachability_passed = bool(
        reachability["contract_integrity_passed"]
        and reachability["declaration_alignment_status"] == "aligned"
        and claim_ownership["passed"]
    )
    _check(
        checks,
        "backend_fidelity",
        "runtime_dependency_alignment",
        "blocker",
        reachability_passed,
        {
            "contract_integrity_passed": reachability["contract_integrity_passed"],
            "declaration_alignment_status": reachability["declaration_alignment_status"],
            "declaration_gap_count": reachability["declaration_gap_count"],
            "claim_ownership_passed": claim_ownership["passed"],
        },
        "Declared task maturity modules must equal actual reachable runtime dependencies.",
        "Keep --strict-alignment in the final release gate.",
        "scripts/audit_model_reachability.py",
        "workstreams/world_foundation/reports/wf-00-maturity-audit.json",
    )
    proxy_tasks = [
        task_id for task_id in task_ids if get_task(task_id).kernel_maturity.proxy_allowed
    ]
    _check(
        checks,
        "backend_fidelity",
        "serious_tasks_exclude_proxy",
        "blocker",
        not proxy_tasks,
        proxy_tasks,
        "No formal serious task may depend on a proxy-allowed runtime path.",
        "Demote or replace any proxy-dependent task before release.",
        "src/chemworld/tasks.py",
    )
    _check(
        checks,
        "backend_fidelity",
        "vnext_candidates_integrated",
        "blocker",
        not replacement_adapters,
        {
            "base_world_law": manifest.get("world_law_version"),
            "pending_replacement_adapters": replacement_adapters,
        },
        (
            "Accepted professional replacement proposals must be routed and "
            "re-frozen or explicitly excluded."
        ),
        "Run WF-110 integration, remove superseded runtime paths, and regenerate all evidence.",
        "workstreams/world_foundation/adapters",
        "workstreams/world_foundation/110_release_integration.md",
    )
    reference_evidence = _files(release_dir, "**/*reference*")
    _check(
        checks,
        "backend_fidelity",
        "optional_reference_backends_decided",
        "major",
        bool(reference_evidence),
        reference_evidence,
        (
            "Optional external comparisons must either run in a named validation "
            "profile or be excluded from claims."
        ),
        (
            "Publish a dependency-locked reference-validation report and stop "
            "presenting skips as evidence."
        ),
        "tests/reference/test_optional_reference_backends.py",
    )
    platform_evidence = _files(release_dir, "**/*platform*")
    _check(
        checks,
        "backend_fidelity",
        "cross_platform_replay",
        "major",
        bool(platform_evidence),
        platform_evidence,
        (
            "Frozen trajectories must replay within tolerance on at least two "
            "supported Python/platform profiles."
        ),
        "Run and publish Windows/Linux Python 3.11/3.12 replay comparisons.",
        "benchmark/releases/chemworld-serious-v1",
    )
    _check(
        checks,
        "backend_fidelity",
        "limitations_are_public",
        "blocker",
        "proxy/lite" in limitations and "spectroscopy/instruments" in limitations,
        "physics and instrument limitations are explicit",
        "All synthetic physics, instrument, safety, and cost limitations must be public.",
        "Carry these boundaries into release cards and the paper.",
        "docs/limitations.md",
    )

    current_hashes = {task_id: get_task(task_id).contract_hash for task_id in task_ids}
    release_hashes = {
        task_id: str(manifest["task_contract_hashes"][task_id]) for task_id in task_ids
    }
    drift = {
        task_id: {"release": release_hashes[task_id], "current": current_hashes[task_id]}
        for task_id in task_ids
        if release_hashes[task_id] != current_hashes[task_id]
    }
    _check(
        checks,
        "evidence_chain",
        "release_contract_hashes_current",
        "blocker",
        not drift,
        drift,
        "Every released task hash must match the source tree that claims to validate it.",
        "Invalidate the stale bundle and rebuild it after all runtime/task changes.",
        "benchmark/releases/chemworld-serious-v1/manifest.json",
        "src/chemworld/tasks.py",
    )
    embedded_digest_pairs = {
        "baseline_summary_sha256": baseline_path,
        "benchmark_validation_sha256": validation_path,
        "response_surface_audit_sha256": surface_path,
    }
    digest_matches = {
        key: manifest.get("evidence", {}).get(key) == _sha256(path)
        for key, path in embedded_digest_pairs.items()
    }
    _check(
        checks,
        "evidence_chain",
        "embedded_release_digests",
        "blocker",
        all(digest_matches.values()),
        digest_matches,
        "Every embedded public evidence file must match its manifest digest.",
        "Rebuild rather than hand-editing release evidence.",
        "benchmark/releases/chemworld-serious-v1/manifest.json",
    )
    _check(
        checks,
        "evidence_chain",
        "release_commit_binding",
        "blocker",
        bool(manifest.get("commit_hash")),
        manifest.get("commit_hash"),
        "The immutable release must bind the exact source commit.",
        "Add commit hash and dirty-worktree policy to the release manifest.",
        "benchmark/releases/chemworld-serious-v1/manifest.json",
    )
    release_trajectories = _files(release_dir, "**/*.jsonl")
    _check(
        checks,
        "evidence_chain",
        "complete_trajectory_evidence",
        "blocker",
        len(release_trajectories) >= len(rows) * 5,
        {"published": len(release_trajectories), "expected_minimum": len(rows) * 5},
        (
            "Every official task-agent-seed result needs a bound trajectory or "
            "content-addressed archive."
        ),
        "Publish all 180 verified trajectories or a signed, independently retrievable archive.",
        "benchmark/releases/chemworld-serious-v1",
    )
    checker_text = (root / "scripts" / "check_frozen_benchmark.py").read_text(encoding="utf-8")
    checker_verifies_manifest = "manifest.json" in checker_text and "sha256" in checker_text
    _check(
        checks,
        "evidence_chain",
        "frozen_checker_verifies_release_manifest",
        "blocker",
        checker_verifies_manifest,
        (
            "manifest and SHA-256 verification implemented"
            if checker_verifies_manifest
            else "checker only evaluates readiness metadata"
        ),
        "The frozen checker must validate current task hashes and every release digest.",
        "Make stale contracts or modified evidence fail check_frozen_benchmark.py.",
        "scripts/check_frozen_benchmark.py",
    )
    tags = _tag_names(root)
    _check(
        checks,
        "evidence_chain",
        "immutable_release_tag",
        "major",
        bool(tags),
        tags,
        "A named immutable git tag must identify the released commit.",
        "Create the tag only after the final bundle and paper evidence pass.",
        ".git/refs/tags",
    )
    wheels = _files(release_dir, "**/*.whl")
    _check(
        checks,
        "evidence_chain",
        "installable_artifact_in_release",
        "major",
        bool(wheels),
        wheels,
        "The public release must provide or bind an installable wheel.",
        "Publish a wheel digest and verify from an isolated installation.",
        "benchmark/releases/chemworld-serious-v1",
    )

    _check(
        checks,
        "training_readiness",
        "gymnasium_api",
        "major",
        (root / "src" / "chemworld" / "envs" / "chemworld_env.py").exists(),
        "Gymnasium-compatible environment exists",
        "A stable reset/step interface is required for optimizer and RL adapters.",
        "Freeze the interface separately from benchmark task semantics.",
        "src/chemworld/envs/chemworld_env.py",
    )
    vector_files = [
        path
        for path in _files(root, "src/**/*.py")
        if "vector" in (root / path).read_text(encoding="utf-8").lower() and "env" in path.lower()
    ]
    _check(
        checks,
        "training_readiness",
        "vectorized_training_environment",
        "major",
        bool(vector_files),
        vector_files,
        "RL training needs batched deterministic environments and throughput evidence.",
        "Add Sync/Async vector adapters with seed-isolation tests.",
        "src/chemworld/envs",
    )
    generator_files = _files(root, "src/**/*generator*.py")
    _check(
        checks,
        "training_readiness",
        "separate_train_world_generator",
        "blocker",
        bool(generator_files),
        generator_files,
        (
            "Training worlds must be generated outside frozen benchmark seeds "
            "with train/dev/OOD families."
        ),
        "Implement ChemWorld-Train generators before claiming cross-episode learning.",
        "src/chemworld",
    )
    dataset_files = _files(release_dir, "**/*.jsonl")
    _check(
        checks,
        "training_readiness",
        "offline_training_dataset",
        "major",
        len(dataset_files) >= len(task_ids),
        dataset_files,
        (
            "Offline learning requires multi-task trajectories with explicit split "
            "and license metadata."
        ),
        "Export verified trajectories without exposing private benchmark worlds.",
        "benchmark/releases/chemworld-serious-v1",
    )

    paper_files = _files(root, "paper/**/*.tex") + _files(root, "papers/**/*.tex")
    figure_files = _files(root, "paper/figures/*") + _files(root, "papers/figures/*")
    _check(
        checks,
        "paper_readiness",
        "aaai_latex_source",
        "major",
        bool(paper_files),
        paper_files,
        "The paper must be a reproducible LaTeX source tree using the selected AAAI template.",
        "Create the paper only after benchmark claims and experiment tables are frozen.",
        "paper",
        "papers",
    )
    _check(
        checks,
        "paper_readiness",
        "generated_figures",
        "major",
        bool(figure_files),
        figure_files,
        "Every result figure must be generated from a committed summary artifact.",
        "Add deterministic plotting scripts, data digests, and vector figures.",
        "paper/figures",
        "papers/figures",
    )

    category_names = sorted({check.category for check in checks})
    categories: dict[str, dict[str, Any]] = {}
    for category in category_names:
        members = [check for check in checks if check.category == category]
        total_weight = sum(SEVERITY_WEIGHT[check.severity] for check in members)
        passed_weight = sum(SEVERITY_WEIGHT[check.severity] for check in members if check.passed)
        categories[category] = {
            "passed": sum(check.passed for check in members),
            "total": len(members),
            "readiness_percent": round(100.0 * passed_weight / total_weight, 1),
            "blockers": [
                check.check_id
                for check in members
                if check.severity == "blocker" and not check.passed
            ],
        }
    total_weight = sum(SEVERITY_WEIGHT[check.severity] for check in checks)
    passed_weight = sum(SEVERITY_WEIGHT[check.severity] for check in checks if check.passed)
    blocker_ids = [
        check.check_id for check in checks if check.severity == "blocker" and not check.passed
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "suite_id": "chemworld-serious-v1",
        "audit_scope": ("scientific-claim readiness, not merely executable pipeline readiness"),
        "source_release_manifest_sha256": _sha256(manifest_path),
        "generalization_report_sha256": (
            _sha256(generalization_path)
            if generalization_path is not None and generalization_path.exists()
            else None
        ),
        "readiness_percent": round(100.0 * passed_weight / total_weight, 1),
        "release_recommendation": (
            "candidate_only_do_not_submit_final_claim" if blocker_ids else "release_candidate"
        ),
        "passed_check_count": sum(check.passed for check in checks),
        "check_count": len(checks),
        "blocker_count": len(blocker_ids),
        "blockers": blocker_ids,
        "categories": categories,
        "checks": [check.to_dict() for check in checks],
        "required_sequence": [
            "invalidate stale v1 evidence and make the frozen checker fail closed",
            "integrate accepted vNext runtime replacements and refreeze task contracts",
            "repair task validity and power the paired-seed statistical protocol",
            "add axis-level OOD, private evaluation, invariance, and exploit audits",
            "run traditional, active-learning, RL, and real-LLM methods under one resource ledger",
            "publish complete trajectories, figures, paper artifacts, wheel, and immutable tag",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--generalization-report",
        type=Path,
        default=Path("runs/benchmark_v1_gap_audit/generalization_audit.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workstreams/benchmark_v1/reports/benchmark_v1_gap_audit.json"),
    )
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    generalization = args.generalization_report
    if not generalization.is_absolute():
        generalization = root / generalization
    report = build_audit(root, generalization_report=generalization)
    output = args.output
    if not output.is_absolute():
        output = root / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if args.require_ready and report["blocker_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
