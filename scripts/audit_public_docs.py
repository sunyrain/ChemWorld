"""Fail closed when public documentation drifts from the published user contract."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_TOKENS = (
    "codex_subagent",
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
    "docs/research_findings.md",
    "docs/research_findings.en.md",
    "docs/limitations.md",
)
CURRENT_TRUTH_MARKERS = {
    "docs/tasks.md": ("reference_validated", "proxy_allowed=false"),
    "docs/task_cards.md": ("reference_validated", "proxy_allowed=false"),
    "docs/worlds.md": ("15", "reference_validated", "proxy_allowed=false"),
    "docs/backends.md": ("v0.5", "candidate"),
    "docs/world_law.md": ("v0.5",),
    "docs/model_maturity.md": ("reference_validated", "backend v0.5 candidate"),
    "docs/physchem_core_design.md": ("reference_validated", "proxy"),
}
REQUIRED_NARRATIVE_MARKERS = {
    "docs/index.md": ("让实验智能拥有自己的世界引擎", "同一个任务", "不直接迁移配方"),
    "docs/vision.md": (
        "实验交互的规模瓶颈",
        "ChemWorld Engine",
        "ChemWorld Bench",
        "ChemWorld Lab",
        "ChemWorld Bridge",
    ),
    "docs/experimental_intelligence.md": ("测量本身也是行动", "失败恢复也是能力"),
    "docs/causal_worlds.md": ("World、Task 与 Scenario", "为什么只换 Seed 不够"),
    "docs/benchmark_overview.md": ("适应需要自己的指标", "不同 Agent Track 分开报告"),
    "docs/real_world_bridge.md": ("验证路线", "Transfer advantage", "Shadow Mode"),
    "docs/index.en.md": ("Give experimental intelligence its own world engine", "Causal Worlds"),
    "docs/research_findings.md": ("发现五", "benchmark candidate"),
    "docs/research_findings.en.md": ("Finding 4", "benchmark candidate"),
}
NAV_GROUPS = (
    "研究主线",
    "探索世界",
    "构建智能体",
    "评测",
    "技术参考",
)
ENGLISH_NAV_TARGETS = (
    "index.md",
    "vision.md",
    "experimental_intelligence.md",
    "causal_worlds.md",
    "benchmark_overview.md",
    "research_findings.md",
    "real_world_bridge.md",
)
README_BOUNDARY_MARKERS = (
    "campaign",
    "no formal cross-method result",
    "gate a now establishes environment-level identifiability",
    "agent-level mechanism-discovery claims remain unsupported",
)
PASSED_GATE_A_STATUS_MARKERS = {
    "README.md": (
        "Gate A now establishes environment-level identifiability",
    ),
    "docs/benchmark_release.md": (
        "Gate A 整体因此通过",
        "237/240",
    ),
    "docs/research_findings.md": (
        "Gate A 总状态为 true",
        "237/240",
    ),
    "docs/research_findings.en.md": (
        "so Gate A is true",
        "237/240 (98.75%)",
    ),
}
STALE_GATE_A_STATUS_MARKERS = (
    "online-policy-feasible certificate remains pending",
    "Gate A as a whole remains false",
    "online-policy-feasible certificate 尚未执行",
    "Gate A 总状态仍为 false",
    "在线策略可行证书待完成",
    "Gate A 整体仍为 false",
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
    current = json.loads(
        (root / "configs/current.json").read_text(encoding="utf-8")
    )
    gate_a_pass = (
        current.get("mechanism_adaptation", {}).get("gate_a_pass") is True
    )
    status_surface_missing_markers = (
        _missing_markers(root, PASSED_GATE_A_STATUS_MARKERS)
        if gate_a_pass
        else {}
    )
    status_surface_stale_markers = (
        _token_hits(
            [root / relative for relative in PASSED_GATE_A_STATUS_MARKERS],
            root,
            STALE_GATE_A_STATUS_MARKERS,
        )
        if gate_a_pass
        else []
    )

    mkdocs = (root / "mkdocs.yml").read_text(encoding="utf-8")
    mkdocs_config = yaml.safe_load(mkdocs)
    chinese_nav = mkdocs_config["nav"]
    chinese_nav_targets = _nav_targets(chinese_nav)
    chinese_nav_labels = _nav_labels(chinese_nav)
    i18n_config = _plugin_config(mkdocs_config["plugins"], "i18n")
    language_configs = {
        language["locale"]: language for language in i18n_config.get("languages", [])
    }
    english_nav = language_configs.get("en", {}).get("nav", [])
    english_nav_targets = _nav_targets(english_nav)
    english_source_targets = [_localized_source(target, "en") for target in english_nav_targets]

    missing_chinese_nav_targets = [
        target for target in chinese_nav_targets if not (root / "docs" / target).is_file()
    ]
    missing_english_nav_targets = [
        target for target in english_source_targets if not (root / "docs" / target).is_file()
    ]
    missing_nav_targets = missing_chinese_nav_targets + [
        f"en:{target}" for target in missing_english_nav_targets
    ]
    public_markdown_targets = {
        path.relative_to(root / "docs").as_posix()
        for path in (root / "docs").rglob("*.md")
        if not path.name.endswith(".en.md")
    }
    public_english_targets = {
        path.relative_to(root / "docs").as_posix()
        for path in (root / "docs").rglob("*.en.md")
    }
    unlisted_public_pages = sorted(public_markdown_targets - set(chinese_nav_targets)) + [
        f"en:{target}"
        for target in sorted(public_english_targets - set(english_source_targets))
    ]
    duplicate_chinese_targets = {
        target for target in chinese_nav_targets if chinese_nav_targets.count(target) > 1
    }
    duplicate_english_targets = {
        target for target in english_nav_targets if english_nav_targets.count(target) > 1
    }
    duplicate_nav_targets = sorted(duplicate_chinese_targets) + [
        f"en:{target}" for target in sorted(duplicate_english_targets)
    ]
    nav_group_positions = [
        chinese_nav_labels.index(group) if group in chinese_nav_labels else -1
        for group in NAV_GROUPS
    ]
    theme_features = mkdocs_config.get("theme", {}).get("features", [])
    nav_checks = {
        "professional_narrative_groups": all(group in chinese_nav_labels for group in NAV_GROUPS),
        "professional_narrative_order": nav_group_positions == sorted(nav_group_positions),
        "language_switch_present": set(language_configs) == {"zh", "en"}
        and language_configs["zh"].get("default") is True
        and i18n_config.get("reconfigure_material") is True,
        "english_navigation_present": _is_ordered_subset(
            ENGLISH_NAV_TARGETS,
            tuple(english_nav_targets),
        ),
        "english_is_not_a_chinese_nav_section": "English" not in chinese_nav_labels,
        "locale_sources_are_isolated": i18n_config.get("docs_structure") == "suffix"
        and i18n_config.get("fallback_to_default") is False,
        "contextual_switch_compatible": "navigation.instant" not in theme_features
        and not mkdocs_config.get("extra", {}).get("alternate"),
        "all_public_pages_listed": not unlisted_public_pages,
        "targets_unique": not duplicate_nav_targets,
        "targets_exist": bool(chinese_nav_targets)
        and bool(english_nav_targets)
        and not missing_nav_targets,
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
        "navigation_controls_localized": "var isEnglish" in navigation_js
        and 'onThisPage: "On this page"' in navigation_js,
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
        "professional_information_architecture": all(nav_checks.values()),
        "folding_contract": all(folding_checks.values()),
        "chemworld_is_primary_brand": "site_name: ChemWorld\n" in mkdocs,
        "readme_boundary_explicit": all(
            marker.lower()
            in " ".join(
                (root / "README.md").read_text(encoding="utf-8").lower().split()
            )
            for marker in README_BOUNDARY_MARKERS
        ),
        "research_status_matches_current_registry": (
            not status_surface_missing_markers
            and not status_surface_stale_markers
        ),
    }
    return {
        "schema_version": "chemworld-public-docs-audit-0.4",
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
        "status_surface_missing_markers": status_surface_missing_markers,
        "status_surface_stale_markers": status_surface_stale_markers,
        "navigation_checks": nav_checks,
        "unlisted_public_pages": unlisted_public_pages,
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


def _plugin_config(plugins: list[Any], name: str) -> dict[str, Any]:
    for plugin in plugins:
        if isinstance(plugin, dict) and name in plugin:
            config = plugin[name]
            return config if isinstance(config, dict) else {}
    return {}


def _is_ordered_subset(required: tuple[str, ...], actual: tuple[str, ...]) -> bool:
    """Return whether all required navigation targets occur in their declared order."""

    cursor = iter(actual)
    return all(any(candidate == item for candidate in cursor) for item in required)


def _nav_labels(nav: list[Any]) -> list[str]:
    return [str(next(iter(item))) for item in nav if isinstance(item, dict) and item]


def _nav_targets(nav: list[Any]) -> list[str]:
    targets: list[str] = []
    for item in nav:
        if isinstance(item, str):
            targets.append(item)
            continue
        if not isinstance(item, dict):
            continue
        for value in item.values():
            if isinstance(value, str):
                targets.append(value)
            elif isinstance(value, list):
                targets.extend(_nav_targets(value))
    return targets


def _localized_source(target: str, locale: str) -> str:
    path = Path(target)
    return path.with_name(f"{path.stem}.{locale}{path.suffix}").as_posix()


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
