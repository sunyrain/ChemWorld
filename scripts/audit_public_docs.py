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
        "deepseek-v4-pro",
        "masked 条件必须保留端点",
        "没有真实 provider 轨迹",
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
    mkdocs = (root / "mkdocs.yml").read_text(encoding="utf-8")
    nav_checks = {
        "quick_start": "  - 快速开始:" in mkdocs,
        "build_agents": "  - 构建智能体:" in mkdocs,
        "evaluation": "  - 评测与证据:" in mkdocs,
        "environment": "  - 环境与任务:" in mkdocs,
        "reference": "  - 数据与参考:" in mkdocs,
    }
    checks = {
        "utf8_files_readable": bool(files),
        "no_maintainer_paths": not forbidden_hits,
        "current_evidence_markers_present": not missing_markers,
        "user_journey_navigation": all(nav_checks.values()),
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
