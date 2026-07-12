"""Fail closed when public documentation drifts from the published user contract."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_TOKENS = (
    "claims/active",
    "claims/completed",
    "codex_subagent",
    "todolist.md",
    "workstreams/",
    "python scripts/",
)
UNIMPLEMENTED_COMMANDS = ("chemworld score",)
RESULT_PAGES = (
    "README.md",
    "docs/benchmark_release.md",
    "docs/benchmark_protocol.md",
    "docs/baseline_reference.md",
    "docs/safety_cost.md",
    "docs/world_model_learning.md",
    "docs/en/research_findings.md",
    "docs/limitations.md",
    "docs/release_notes.md",
)
CURRENT_TRUTH_MARKERS = {
    "docs/tasks.md": ("reference_validated", "proxy_allowed=false"),
    "docs/task_cards.md": ("reference_validated", "proxy_allowed=false"),
    "docs/worlds.md": ("15", "reference_validated", "proxy_allowed=false"),
    "docs/backends.md": ("v0.5", "candidate"),
    "docs/world_law.md": ("v0.4", "v0.5"),
    "docs/model_maturity.md": ("reference_validated", "backend v0.5 candidate"),
    "docs/physchem_core_design.md": ("reference_validated", "proxy"),
}
REQUIRED_NARRATIVE_MARKERS = {
    "docs/index.md": ("让实验智能拥有自己的世界引擎", "同一个任务", "不直接迁移配方"),
    "docs/vision.md": ("实验交互的规模瓶颈", "Core、Bench 与 Bridge"),
    "docs/experimental_intelligence.md": ("测量本身也是行动", "失败恢复也是能力"),
    "docs/causal_worlds.md": ("World、Task 与 Scenario", "为什么只换 Seed 不够"),
    "docs/benchmark_overview.md": ("适应需要自己的指标", "不同 Agent Track 分开报告"),
    "docs/real_world_bridge.md": ("验证路线", "Transfer advantage", "Shadow Mode"),
    "docs/en/index.md": ("Give experimental intelligence its own world engine", "Causal Worlds"),
    "docs/en/research_findings.md": ("Finding 4", "benchmark candidate"),
}
NAV_GROUPS = (
    "开始使用",
    "选择任务",
    "开发 Agent",
    "运行与评测",
    "理解世界",
    "研究边界",
    "技术参考",
)


def audit_public_docs(root: Path = ROOT) -> dict[str, Any]:
    files = _public_files(root)
    forbidden_hits = _token_hits(files, root, FORBIDDEN_TOKENS)
    unimplemented_hits = _token_hits(files, root, UNIMPLEMENTED_COMMANDS)

    protocol = json.loads(
        (root / "configs/foundation/backend_v0.5.json").read_text(encoding="utf-8")
    )
    tasks_text = (root / "docs/tasks.md").read_text(encoding="utf-8")
    truth_markers = (
        protocol["backend_id"],
        protocol["world_law_id"],
        protocol["task_contract_version"],
        "reference_validated",
        "proxy_allowed=false",
    )
    missing_task_truth = [marker for marker in truth_markers if marker not in tasks_text]
    missing_task_hashes = {
        task_id: digest
        for task_id, digest in protocol["expected_task_contract_hashes"].items()
        if task_id not in tasks_text or digest not in tasks_text
    }
    missing_current_markers = _missing_markers(root, CURRENT_TRUTH_MARKERS)
    missing_narrative_markers = _missing_markers(root, REQUIRED_NARRATIVE_MARKERS)
    missing_history_boundaries = [
        relative
        for relative in RESULT_PAGES
        if "pre-v0.5" not in (root / relative).read_text(encoding="utf-8").lower()
    ]

    mkdocs = (root / "mkdocs.yml").read_text(encoding="utf-8")
    nav_targets = re.findall(
        r"^[ \t]*-[ \t]+[^:\n]+:[ \t]+([^#\n]+\.md)[ \t]*$", mkdocs, flags=re.MULTILINE
    )
    missing_nav_targets = [
        target for target in nav_targets if not (root / "docs" / target).is_file()
    ]
    duplicate_nav_targets = sorted(
        {target for target in nav_targets if nav_targets.count(target) > 1}
    )
    nav_checks = {
        "user_journey_groups": all(f"  - {group}:" in mkdocs for group in NAV_GROUPS),
        "language_switch_present": "name: English" in mkdocs and "/ChemWorld/en/" in mkdocs,
        "no_duplicate_english_group": "  - English:" not in mkdocs,
        "targets_unique": not duplicate_nav_targets,
        "targets_exist": bool(nav_targets) and not missing_nav_targets,
    }

    navigation_js = (root / "docs/assets/javascripts/navigation-v7.js").read_text(encoding="utf-8")
    site_css = (root / "docs/assets/stylesheets/site.css").read_text(encoding="utf-8")
    language_css = (root / "docs/assets/stylesheets/language-switch.css").read_text(
        encoding="utf-8"
    )
    folding_checks = {
        "left_navigation_control": "setupPrimaryNavigation" in navigation_js,
        "right_toc_control": "setupTocNavigation" in navigation_js,
        "content_folding_opt_in": "h2.cw-fold[id]" in navigation_js
        and "h2[data-cw-fold][id]" in navigation_js,
        "content_folding_not_global": 'querySelectorAll(":scope > h2[id]")' not in navigation_js,
        "collapse_css_single_owner": ".cw-outline-toggle" in site_css
        and ".cw-" not in language_css,
    }

    checks = {
        "utf8_files_readable": bool(files),
        "no_maintainer_paths_or_commands": not forbidden_hits,
        "no_unimplemented_cli": not unimplemented_hits,
        "task_truth_matches_v05_protocol": not missing_task_truth and not missing_task_hashes,
        "current_truth_markers_present": not missing_current_markers,
        "pre_v05_results_marked_diagnostic": not missing_history_boundaries,
        "research_narrative_present": not missing_narrative_markers,
        "user_journey_navigation": all(nav_checks.values()),
        "folding_contract": all(folding_checks.values()),
        "chemworld_is_primary_brand": "site_name: ChemWorld\n" in mkdocs,
        "readme_boundary_explicit": "complete benchmark is not yet validated"
        in (root / "README.md").read_text(encoding="utf-8").lower(),
    }
    return {
        "schema_version": "chemworld-public-docs-audit-0.2",
        "passed": all(checks.values()),
        "checks": checks,
        "file_count": len(files),
        "forbidden_hits": forbidden_hits,
        "unimplemented_command_hits": unimplemented_hits,
        "missing_task_truth": missing_task_truth,
        "missing_task_hashes": missing_task_hashes,
        "missing_current_markers": missing_current_markers,
        "missing_history_boundaries": missing_history_boundaries,
        "missing_narrative_markers": missing_narrative_markers,
        "navigation_checks": nav_checks,
        "missing_navigation_targets": missing_nav_targets,
        "duplicate_navigation_targets": duplicate_nav_targets,
        "folding_checks": folding_checks,
    }


def _public_files(root: Path) -> list[Path]:
    files = [root / "README.md", root / "mkdocs.yml"]
    files.extend(sorted((root / "docs").rglob("*.md")))
    for path in files:
        path.read_text(encoding="utf-8")
    return files


def _token_hits(files: list[Path], root: Path, tokens: tuple[str, ...]) -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    for path in files:
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            normalized = line.replace("\\", "/").lower()
            for token in tokens:
                if token.lower() in normalized:
                    hits.append(
                        {
                            "path": path.relative_to(root).as_posix(),
                            "line": line_number,
                            "token": token,
                        }
                    )
    return hits


def _missing_markers(root: Path, requirements: dict[str, tuple[str, ...]]) -> dict[str, list[str]]:
    missing: dict[str, list[str]] = {}
    for relative, markers in requirements.items():
        text = (root / relative).read_text(encoding="utf-8")
        absent = [marker for marker in markers if marker not in text]
        if absent:
            missing[relative] = absent
    return missing


def main() -> int:
    report = audit_public_docs()
    print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
