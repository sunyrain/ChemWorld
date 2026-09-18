"""Chemical categories derived from recorded task identifiers, not archive versions."""

import re

CATEGORIES = [
    {"id": "electrochemistry", "label": "电化学", "tasks": ["electrochemical-conversion"]},
    {
        "id": "reaction",
        "label": "反应与热过程",
        "tasks": [
            "reaction-optimization-standard",
            "reaction-safety-constrained",
            "reaction-mechanism-explanation",
            "reaction-to-assay",
        ],
    },
    {
        "id": "purification",
        "label": "萃取与纯化",
        "tasks": [
            "reaction-to-purification",
            "purity-yield-tradeoff",
        ],
    },
    {"id": "crystallization", "label": "结晶", "tasks": ["reaction-to-crystallization"]},
    {"id": "distillation", "label": "蒸馏", "tasks": ["reaction-to-distillation"]},
    {
        "id": "phase",
        "label": "相、平衡与表征",
        "tasks": [
            "partition-discovery",
            "equilibrium-characterization",
            "low-budget-characterization",
        ],
    },
    {"id": "flow", "label": "连续流", "tasks": ["flow-reaction-optimization"]},
    {
        "id": "other",
        "label": "综合与未分类",
        "tasks": [
            "public-private-generalization",
            "tool-agent-planning",
        ],
    },
]
TASK_CATEGORY = {task: category["id"] for category in CATEGORIES for task in category["tasks"]}
TASK_PATTERN = re.compile(r"(?<![a-z])(" + "|".join(TASK_CATEGORY) + r")(?![a-z])")


def categories_in(value) -> set[str]:
    if isinstance(value, str):
        return {TASK_CATEGORY[m.group()] for m in TASK_PATTERN.finditer(value)}
    result = set()
    if isinstance(value, dict):
        for key, child in value.items():
            result.update(categories_in(key))
            result.update(categories_in(child))
    elif isinstance(value, list):
        for child in value:
            result.update(categories_in(child))
    return result


def ordered_categories(values) -> list[str]:
    return [c["id"] for c in CATEGORIES if c["id"] in values] or ["other"]


def recorded_categories(row) -> set[str]:
    if not isinstance(row, dict):
        return set()
    # Task identity belongs to the record, not to every task mentioned in a
    # model prompt or the full tool catalogue embedded in public observations.
    context = (row.get("explanation") or {}).get("decision_context") or {}
    return categories_in(
        [
            row.get("task_id"),
            row.get("benchmark_task_id"),
            context.get("task_id"),
        ]
    )
