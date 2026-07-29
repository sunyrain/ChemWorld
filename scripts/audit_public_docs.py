"""Fail closed when public documentation drifts from the published user contract."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import unquote

import yaml

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_TOKENS = (
    "codex_subagent",
    "](workstreams/",
    "](../workstreams/",
    "python scripts/",
)
UNIMPLEMENTED_COMMANDS = ("chemworld score",)
RESULT_PAGES = (
    "README.md",
    "docs/benchmark_protocol.md",
    "docs/baseline_reference.md",
    "docs/safety_cost.md",
    "docs/world_model_learning.md",
)
CANONICAL_RESULT_TOKENS = (
    "0.7150",
    "0.5355",
    "0.7874",
    "0.5615",
    "0.6853",
    "0.5845",
)
CANONICAL_RESULT_PAGES = {
    "docs/benchmark_release.md",
    "docs/flagship_experiments.md",
    "docs/flagship_experiments.en.md",
}
HISTORICAL_CERTIFICATE_TOKENS = ("4,896", "2,016", "98.26%", "96.57%")
HISTORICAL_CERTIFICATE_PAGES = {"docs/benchmark_release.md"}
OBSOLETE_STATUS_PHRASES = (
    "替代固定世界 S0 的正式模型矩阵尚未执行",
    "当前正式方法矩阵仍缺少真实 provider 轨迹",
    "方法、资源和结果尚未冻结",
    "方法与结果尚未冻结",
)
CURRENT_TRUTH_MARKERS = {
    "docs/tasks.md": (
        "reference_validated",
        "proxy_allowed=false",
        "16 个独立控制",
        "415 个中点、坐标低/高与离散类别配方",
        "62 个声明成功指标全部有可执行端点",
    ),
    "docs/task_cards.md": ("reference_validated", "proxy_allowed=false"),
    "docs/worlds.md": ("15", "reference_validated", "proxy_allowed=false"),
    "docs/backends.md": ("v0.5", "candidate"),
    "docs/world_law.md": ("v0.5",),
    "docs/model_maturity.md": ("reference_validated", "backend v0.5 candidate"),
    "docs/physchem_core_design.md": ("reference_validated", "proxy"),
}
REQUIRED_NARRATIVE_MARKERS = {
    "docs/index.md": (
        "让实验智能拥有自己的世界引擎",
        "同一个任务",
        "不直接迁移配方",
        "15 个任务的完整实验合同",
        "查看精确结果与当前状态",
    ),
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
    "docs/index.en.md": (
        "Give experimental intelligence its own world engine",
        "Causal Worlds",
        "All 15 task contracts are executable",
    ),
    "docs/research_findings.md": (
        "主叙事",
        "信息改变行为，不等于模型理解信息",  # noqa: RUF001
        "下一条最有价值的证据",
    ),
    "docs/research_findings.en.md": (
        "Central narrative",
        "Behavioral influence is not evidence of understanding",
        "Highest-value next evidence",
    ),
}
NAV_GROUPS = (
    "研究与证据",
    "体验 ChemWorld",
    "构建与评测",
    "技术参考",
)
ENGLISH_NAV_TARGETS = (
    "index.md",
    "vision.md",
    "experimental_intelligence.md",
    "causal_worlds.md",
    "architecture.md",
    "benchmark_overview.md",
    "flagship_experiments.md",
    "research_findings.md",
    "real_world_bridge.md",
)
README_BOUNDARY_MARKERS = (
    "campaign",
    "participant gates b–e",  # noqa: RUF001
    "does not support broad sota",
    "real-world-transfer claims",
)
PASSED_GATE_A_STATUS_MARKERS = {
    "README.md": ("Historical RC28 Gate A passed",),
    "docs/benchmark_release.md": ("历史通过",),
}
FAILED_GATE_A_STATUS_MARKERS = {
    "README.md": ("benchmark_ready=false",),
    "docs/benchmark_release.md": ("benchmark_ready=false",),
}
BINDING_STALE_GATE_A_STATUS_MARKERS = {
    "README.md": (
        "binding is stale",
        "benchmark_ready=false",
    ),
    "docs/benchmark_release.md": (
        "当前源码指纹已经变化",
        "benchmark_ready=false",
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
    obsolete_status_hits = _token_hits(files, root, OBSOLETE_STATUS_PHRASES)
    result_number_hits = _disallowed_token_hits(
        files,
        root,
        CANONICAL_RESULT_TOKENS,
        CANONICAL_RESULT_PAGES,
    )
    historical_number_hits = _disallowed_token_hits(
        files,
        root,
        HISTORICAL_CERTIFICATE_TOKENS,
        HISTORICAL_CERTIFICATE_PAGES,
    )
    broken_local_links = _broken_local_links(root)
    unreferenced_images = _unreferenced_images(root)

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
    gate_a_binding_stale = (
        gate_a_pass
        and current.get("mechanism_adaptation", {}).get("gate_a_evidence_current")
        is not True
    )
    expected_status_markers = (
        BINDING_STALE_GATE_A_STATUS_MARKERS
        if gate_a_binding_stale
        else PASSED_GATE_A_STATUS_MARKERS
        if gate_a_pass
        else FAILED_GATE_A_STATUS_MARKERS
    )
    status_surface_missing_markers = _missing_markers(
        root,
        expected_status_markers,
    )
    status_surface_stale_markers = (
        _token_hits(
            [root / relative for relative in PASSED_GATE_A_STATUS_MARKERS],
            root,
            STALE_GATE_A_STATUS_MARKERS,
        )
        if gate_a_pass and not gate_a_binding_stale
        else []
        if gate_a_binding_stale
        else _token_hits(
            [root / relative for relative in FAILED_GATE_A_STATUS_MARKERS],
            root,
            tuple(
                marker
                for markers in PASSED_GATE_A_STATUS_MARKERS.values()
                for marker in markers
            ),
        )
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
    reference_catalog = (root / "docs/reference_index.md").read_text(encoding="utf-8")
    reference_catalog_targets = set(re.findall(r"\]\(([^)#?]+\.md)\)", reference_catalog))
    unlisted_public_pages = sorted(
        public_markdown_targets
        - set(chinese_nav_targets)
        - reference_catalog_targets
    ) + [
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
        "no_obsolete_status_phrases": not obsolete_status_hits,
        "canonical_result_numbers_are_not_duplicated": not result_number_hits,
        "historical_certificate_numbers_have_one_summary": not historical_number_hits,
        "local_links_resolve": not broken_local_links,
        "image_assets_are_referenced": not unreferenced_images,
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
        "schema_version": "chemworld-public-docs-audit-0.5",
        "passed": all(checks.values()),
        "checks": checks,
        "file_count": len(files),
        "forbidden_hits": forbidden_hits,
        "unimplemented_command_hits": unimplemented_hits,
        "obsolete_status_hits": obsolete_status_hits,
        "result_number_hits": result_number_hits,
        "historical_number_hits": historical_number_hits,
        "broken_local_links": broken_local_links,
        "unreferenced_images": unreferenced_images,
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


def _disallowed_token_hits(
    files: list[Path],
    root: Path,
    tokens: tuple[str, ...],
    allowed_paths: set[str],
) -> list[dict[str, Any]]:
    scoped_files = [
        path
        for path in files
        if path.relative_to(root).as_posix() not in allowed_paths
    ]
    return _token_hits(scoped_files, root, tokens)


def _broken_local_links(root: Path) -> list[dict[str, Any]]:
    broken: list[dict[str, Any]] = []
    docs_root = root / "docs"
    link_pattern = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")
    for path in sorted(docs_root.rglob("*.md")):
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(),
            start=1,
        ):
            for match in link_pattern.finditer(line):
                raw_target = match.group(1).strip()
                if raw_target.startswith("<") and ">" in raw_target:
                    target = raw_target[1 : raw_target.index(">")]
                else:
                    target = raw_target.split(maxsplit=1)[0]
                if (
                    not target
                    or target.startswith(("#", "/"))
                    or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE)
                ):
                    continue
                relative = unquote(target.split("#", 1)[0].split("?", 1)[0])
                resolved = (path.parent / relative).resolve()
                if not resolved.exists():
                    broken.append(
                        {
                            "path": path.relative_to(root).as_posix(),
                            "line": line_number,
                            "target": target,
                        }
                    )
    return broken


def _unreferenced_images(root: Path) -> list[str]:
    image_root = root / "docs/assets/images"
    if not image_root.is_dir():
        return []
    public_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((root / "docs").rglob("*.md"))
    )
    public_text += "\n" + (root / "mkdocs.yml").read_text(encoding="utf-8")
    return [
        path.relative_to(root).as_posix()
        for path in sorted(image_root.rglob("*"))
        if path.is_file()
        and path.relative_to(root / "docs").as_posix() not in public_text
        and path.name not in public_text
    ]


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
