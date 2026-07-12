"""Fail closed when public documentation exposes maintainer-only paths or stale evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ROOTS = (ROOT / "README.md", ROOT / "mkdocs.yml", ROOT / "docs")
FORBIDDEN_TOKENS = (
    "claims/active",
    "claims/completed",
    "codex_subagent",
    "todolist.md",
    "workstreams/benchmark_v1",
)
REQUIRED_STATUS_MARKERS = {
    "docs/benchmark_release.md": (
        "0.018752",
        "100,000",
        "9/9",
        "没有真实 provider 轨迹",
        "不支持",
    ),
    "docs/limitations.md": (
        "80k checkpoint",
        "assigned/masked",
        "不能",
    ),
    "docs/mechanism_schema.md": (
        "六个研究任务",
        "9 个任务—模式组合",
        "精确干预上下文",
    ),
    "docs/llm_agent_harness.md": (
        "真实 provider 轨迹",
        "`masked`",
        "私有逐字思维链",
    ),
}
REQUIRED_NARRATIVE_MARKERS = {
    "docs/index.md": (
        "让实验智能拥有自己的世界引擎",
        "同一个任务",
        "不直接迁移配方",
    ),
    "docs/vision.md": (
        "实验交互的规模瓶颈",
        "Core、Bench 与 Bridge",
    ),
    "docs/experimental_intelligence.md": (
        "测量本身也是行动",
        "失败恢复也是能力",
    ),
    "docs/causal_worlds.md": (
        "World、Task 与 Scenario",
        "为什么只换 Seed 不够",
    ),
    "docs/benchmark_overview.md": (
        "适应需要自己的指标",
        "不同 Agent Track 分开报告",
    ),
    "docs/real_world_bridge.md": (
        "验证路线",
        "Transfer advantage",
        "Shadow Mode",
    ),
    "docs/en/index.md": (
        "Give experimental intelligence its own world engine",
        "Causal Worlds",
    ),
    "docs/en/vision.md": (
        "Why not one perfect digital twin",
        "Core, Bench, Lab, Bridge",
    ),
    "docs/en/experimental_intelligence.md": (
        "Measurement is an action",
        "Failure is part of the task",
    ),
    "docs/en/causal_worlds.md": (
        "Changing a seed",
        "The public contract stays stable",
    ),
    "docs/en/benchmark_overview.md": (
        "Generalization axes are distinct",
        "Adaptation metrics",
    ),
    "docs/en/research_findings.md": (
        "Finding 4",
        "benchmark candidate",
    ),
    "docs/en/real_world_bridge.md": (
        "Validity ladder",
        "validation roadmap",
    ),
}


def audit_public_docs(root: Path = ROOT) -> dict[str, Any]:
    files = _public_files(root)
    forbidden_hits: list[dict[str, Any]] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            normalized = line.replace("\\", "/").lower()
            for token in FORBIDDEN_TOKENS:
                if token.lower() in normalized:
                    forbidden_hits.append(
                        {
                            "path": path.relative_to(root).as_posix(),
                            "line": line_number,
                            "token": token,
                        }
                    )
    missing_markers: dict[str, list[str]] = {}
    for relative, markers in REQUIRED_STATUS_MARKERS.items():
        text = (root / relative).read_text(encoding="utf-8")
        missing = [marker for marker in markers if marker not in text]
        if missing:
            missing_markers[relative] = missing
    missing_narrative_markers: dict[str, list[str]] = {}
    for relative, markers in REQUIRED_NARRATIVE_MARKERS.items():
        text = (root / relative).read_text(encoding="utf-8")
        missing = [marker for marker in markers if marker not in text]
        if missing:
            missing_narrative_markers[relative] = missing
    mkdocs = (root / "mkdocs.yml").read_text(encoding="utf-8")
    nav_checks = {
        "research_story": "  - 研究主线:" in mkdocs,
        "worlds": "  - 探索世界:" in mkdocs,
        "build_agents": "  - 构建智能体:" in mkdocs,
        "benchmark": "  - 评测:" in mkdocs,
        "reference": "  - 技术参考:" in mkdocs,
        "english": "  - English:" in mkdocs,
    }
    checks = {
        "utf8_files_readable": bool(files),
        "no_maintainer_paths": not forbidden_hits,
        "current_evidence_markers_present": not missing_markers,
        "research_narrative_present": not missing_narrative_markers,
        "user_journey_navigation": all(nav_checks.values()),
        "chemworld_is_primary_brand": "site_name: ChemWorld\n" in mkdocs,
        "readme_boundary_explicit": "complete benchmark is not yet validated"
        in (root / "README.md").read_text(encoding="utf-8").lower(),
    }
    return {
        "schema_version": "chemworld-public-docs-audit-0.1",
        "passed": all(checks.values()),
        "checks": checks,
        "file_count": len(files),
        "forbidden_hits": forbidden_hits,
        "missing_status_markers": missing_markers,
        "missing_narrative_markers": missing_narrative_markers,
        "navigation_checks": nav_checks,
    }


def _public_files(root: Path) -> list[Path]:
    files = [root / "README.md", root / "mkdocs.yml"]
    files.extend(sorted((root / "docs").rglob("*.md")))
    return files


def main() -> int:
    report = audit_public_docs()
    print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
