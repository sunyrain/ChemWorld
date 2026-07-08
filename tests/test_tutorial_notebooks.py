from __future__ import annotations

# ruff: noqa: RUF001
import json
from pathlib import Path

TUTORIAL_DIR = Path("notebooks/tutorials")
TUTORIAL_NOTEBOOKS = (
    "day_01_enter_virtual_lab.ipynb",
    "day_02_ontology_and_constitution.ipynb",
    "day_03_observation_and_instruments.ipynb",
    "day_04_mechanism_scans.ipynb",
    "day_05_surrogate_modeling.ipynb",
    "day_06_baselines_and_leaderboard.ipynb",
    "day_07_capstone_artifact.ipynb",
    "day_08_gpt_planner_and_validation.ipynb",
    "day_09_bayesian_optimization.ipynb",
    "day_10_public_leaderboard_challenge.ipynb",
    "day_11_private_generalization.ipynb",
    "day_12_demo_day_artifact.ipynb",
    "day_13_year2_process_modules.ipynb",
    "project_leaderboard_blueprint.ipynb",
)


def _notebook_text(path: Path) -> str:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook["cells"]
        if cell.get("cell_type") == "markdown"
    )


def test_tutorial_notebooks_have_half_hour_timeboxes() -> None:
    expected_slots = (
        "0:00-0:30",
        "0:30-1:00",
        "1:00-1:30",
        "1:30-2:00",
        "2:00-2:30",
        "2:30-3:00",
    )
    for notebook_name in TUTORIAL_NOTEBOOKS:
        text = _notebook_text(TUTORIAL_DIR / notebook_name)
        assert "课堂时间盒：每 30 分钟都有产出" in text
        for slot in expected_slots:
            assert slot in text


def test_tutorial_notebooks_use_plain_markdown_checkpoints() -> None:
    for notebook_name in TUTORIAL_NOTEBOOKS:
        text = _notebook_text(TUTORIAL_DIR / notebook_name)
        assert "display_student_checkpoint" not in text
        assert "student-checkpoint" not in text
