from __future__ import annotations

import json
from pathlib import Path

END_TO_END_DIR = Path("notebooks/end_to_end")
END_TO_END_NOTEBOOKS = {
    "reaction_to_assay_end_to_end.ipynb": "reaction-to-assay",
    "reaction_to_purification_end_to_end.ipynb": "reaction-to-purification",
    "partition_discovery_end_to_end.ipynb": "partition-discovery",
}

REQUIRED_PHRASES = (
    "任务规划",
    "validate_action",
    "执行",
    "谱图",
    "processed_estimate",
    "leaderboard_score",
    "反思记录",
)


def _notebook_text(path: Path) -> str:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    return "\n".join(
        "".join(cell.get("source", []))
        if isinstance(cell.get("source", []), list)
        else str(cell.get("source", ""))
        for cell in notebook["cells"]
    )


def test_end_to_end_notebooks_exist_and_have_required_sections() -> None:
    for notebook_name, task_id in END_TO_END_NOTEBOOKS.items():
        path = END_TO_END_DIR / notebook_name
        assert path.exists()
        text = _notebook_text(path)
        assert task_id in text
        for phrase in REQUIRED_PHRASES:
            assert phrase in text


def test_end_to_end_notebooks_are_valid_json_notebooks() -> None:
    for notebook_name in END_TO_END_NOTEBOOKS:
        notebook = json.loads((END_TO_END_DIR / notebook_name).read_text(encoding="utf-8"))
        assert notebook["nbformat"] == 4
        assert len(notebook["cells"]) >= 8
        assert sum(1 for cell in notebook["cells"] if cell["cell_type"] == "code") >= 5
