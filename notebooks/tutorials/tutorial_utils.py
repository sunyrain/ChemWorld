# ruff: noqa: RUF001
"""Shared helpers for ChemWorld twelve-day tutorial notebooks."""

from __future__ import annotations

import html
import math
from pathlib import Path
from typing import Any

import gymnasium as gym
import numpy as np
import pandas as pd
from IPython.display import HTML, SVG, display

import chemworld  # noqa: F401
from chemworld.core.actions import CATALYSTS, SOLVENTS, sample_random_action
from chemworld.core.batch_reactor import recipe_to_event_sequence
from chemworld.data.logging import TrajectoryLogger, load_jsonl, observation_to_json


def project_root() -> Path:
    root = Path.cwd()
    while not (root / "pyproject.toml").exists() and root.parent != root:
        root = root.parent
    return root


OUTPUT_ROOT = project_root() / "runs" / "tutorials"


def ensure_output(day: int) -> Path:
    path = OUTPUT_ROOT / f"day{day:02d}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def scalar(observation: dict[str, Any], key: str) -> float:
    value = float(observation[key][0])
    return math.nan if not math.isfinite(value) else value


def format_recipe(recipe: dict[str, Any]) -> dict[str, Any]:
    return {
        "temperature_C": float(recipe["temperature"]),
        "time_h": float(recipe["time"]),
        "initial_concentration_M": float(recipe["initial_concentration"]),
        "stirring_rpm": float(recipe["stirring_speed"]),
        "catalyst": CATALYSTS[int(recipe["catalyst"])],
        "solvent": SOLVENTS[int(recipe["solvent"])],
    }


def run_events(
    events: list[dict[str, Any]],
    *,
    split: str = "public-dev",
    seed: int = 7,
    objective: str = "balanced",
    debug_truth: bool = False,
) -> pd.DataFrame:
    env = gym.make(
        "ChemWorld",
        world_split=split,
        budget=len(events),
        objective=objective,
        seed=seed,
        debug_truth=debug_truth,
    )
    env.reset(seed=seed)
    rows: list[dict[str, Any]] = []
    try:
        for action in events:
            observation, reward, terminated, truncated, info = env.step(action)
            rows.append(
                {
                    "step": info["step"],
                    "operation": info["operation_type"],
                    "instrument": info["instrument"],
                    "reward": float(reward),
                    "reward_source": info.get("reward_source"),
                    "leaderboard_score": info.get("leaderboard_score"),
                    "yield": scalar(observation, "yield"),
                    "selectivity": scalar(observation, "selectivity"),
                    "conversion": scalar(observation, "conversion"),
                    "byproduct": scalar(observation, "byproduct_signal"),
                    "degradation": scalar(observation, "degradation_warning"),
                    "cost": scalar(observation, "cost"),
                    "risk": scalar(observation, "safety_risk"),
                    "score": scalar(observation, "score"),
                    "measurement_cost": info.get("measurement_cost", 0.0),
                    "sample_consumed": info.get("sample_consumed", 0.0),
                    "observed_keys": ", ".join(info.get("observed_keys", [])),
                    "observed_mask": dict(info.get("observed_mask", {})),
                    "raw_signal": info.get("raw_signal", {}),
                    "processed_estimate": info.get("processed_estimate", {}),
                    "uncertainty": info.get("uncertainty", {}),
                    "error_message": info.get("error_message"),
                    "precondition_failed": info["constraint_flags"].get(
                        "precondition_failed",
                        False,
                    ),
                    "unsafe": info["constraint_flags"].get("unsafe", False),
                    "action": dict(action),
                    "truth": info.get("truth"),
                }
            )
            if terminated or truncated:
                break
    finally:
        env.close()
    return pd.DataFrame(rows)


def run_recipe(
    recipe: dict[str, Any],
    *,
    split: str = "public-dev",
    seed: int = 7,
    objective: str = "balanced",
) -> pd.Series:
    rows = run_events(
        recipe_to_event_sequence(recipe),
        split=split,
        seed=seed,
        objective=objective,
    )
    final = rows.iloc[-1].copy()
    for key, value in format_recipe(recipe).items():
        final[key] = value
    final.name = None
    return final


def write_events_trajectory(
    events: list[dict[str, Any]],
    output_path: Path,
    *,
    split: str = "public-test",
    seed: int = 7,
    objective: str = "balanced",
    agent_name: str = "tutorial_replay",
) -> list[dict[str, Any]]:
    """Run explicit events and write a standard benchmark JSONL trajectory."""

    env = gym.make(
        "ChemWorld",
        world_split=split,
        budget=len(events),
        objective=objective,
        seed=seed,
    )
    env.reset(seed=seed)
    task_info = env.unwrapped.task_info()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "agent_name": agent_name,
        "agent_family": "fixed_event_replay",
        "source": "seven_day_tutorial",
    }
    try:
        with TrajectoryLogger(output_path) as logger:
            for step, action in enumerate(events, start=1):
                observation, reward, terminated, truncated, info = env.step(action)
                obs_json = observation_to_json(observation)
                logger.log(
                    task_info=task_info,
                    step=step,
                    action=action,
                    observation=obs_json,
                    reward=float(reward),
                    terminated=terminated,
                    truncated=truncated,
                    info=info,
                    agent_metadata=metadata,
                )
                if terminated or truncated:
                    break
    finally:
        env.close()
    return load_jsonl(output_path)


def write_recipe_trajectory(
    recipe: dict[str, Any],
    output_path: Path,
    *,
    split: str = "public-test",
    seed: int = 7,
    objective: str = "balanced",
    agent_name: str = "tutorial_recipe_replay",
) -> list[dict[str, Any]]:
    return write_events_trajectory(
        recipe_to_event_sequence(recipe),
        output_path,
        split=split,
        seed=seed,
        objective=objective,
        agent_name=agent_name,
    )


def sample_recipes(seed: int, count: int) -> list[dict[str, Any]]:
    rng = np.random.default_rng(seed)
    return [sample_random_action(rng) for _ in range(count)]


def leaderboard_wide(leaderboard: pd.DataFrame) -> pd.DataFrame:
    """Make a one-row-per-agent leaderboard table for classroom reading."""

    rows = []
    for agent_name, group in leaderboard.groupby("agent_name", sort=False):
        public = group[group["world_split"] == "public-test"]
        private = group[group["world_split"] == "private-eval"]
        public_score = (
            float(public["mean_total_score"].iloc[0]) if not public.empty else math.nan
        )
        private_score = (
            float(private["mean_total_score"].iloc[0]) if not private.empty else math.nan
        )
        safety_values = pd.to_numeric(
            group["mean_safety_aware_score"],
            errors="coerce",
        )
        rows.append(
            {
                "agent": agent_name,
                "public_score": public_score,
                "private_score": private_score,
                "public_private_gap": public_score - private_score,
                "mean_safety_score": float(safety_values.mean()),
                "runs": int(pd.to_numeric(group["runs"], errors="coerce").sum()),
            }
        )
    return pd.DataFrame(rows).sort_values("private_score", ascending=False).reset_index(drop=True)


def raw_signal_payload(row: pd.Series) -> dict[str, Any]:
    """Create a teaching-level raw signal plus derived estimate payload."""

    instrument = row.get("instrument")
    if row.get("raw_signal"):
        return {
            "instrument": instrument,
            "raw_signal": row.get("raw_signal", {}),
            "processed_estimate": row.get("processed_estimate", {}),
            "uncertainty": row.get("uncertainty", {}),
        }

    def value(key: str) -> float | None:
        raw = row.get(key)
        if raw is None:
            return None
        try:
            numeric = float(raw)
        except (TypeError, ValueError):
            return None
        return numeric if math.isfinite(numeric) else None

    processed = {
        key: value(key)
        for key in ["yield", "selectivity", "conversion", "byproduct", "degradation"]
        if value(key) is not None
    }
    uncertainty = {
        f"{key}_std": 0.04 if instrument == "uvvis" else 0.02
        for key in processed
    }
    if instrument == "uvvis":
        yld = value("yield") or 0.0
        conv = value("conversion") or 0.0
        raw_signal: dict[str, Any] = {
            "wavelength_nm": [360, 420, 510, 620],
            "absorbance": [
                round(0.08 + 0.25 * conv, 4),
                round(0.05 + 0.35 * yld, 4),
                round(0.04 + 0.15 * max(conv - yld, 0.0), 4),
                round(0.03, 4),
            ],
        }
    elif instrument == "hplc":
        yld = value("yield") or 0.0
        byproduct = value("byproduct") or 0.0
        raw_signal = {
            "peaks": [
                {"retention_time_min": 1.18, "peak_area": round(900 * max(1 - yld, 0), 2)},
                {"retention_time_min": 2.74, "peak_area": round(1200 * yld, 2)},
                {"retention_time_min": 3.52, "peak_area": round(900 * byproduct, 2)},
            ]
        }
    elif instrument == "gc":
        byproduct = value("byproduct") or 0.0
        degradation = value("degradation") or 0.0
        raw_signal = {
            "peaks": [
                {"retention_time_min": 0.82, "peak_area": round(800 * byproduct, 2)},
                {"retention_time_min": 1.65, "peak_area": round(800 * degradation, 2)},
            ]
        }
    elif instrument == "final_assay":
        raw_signal = {
            "assay_packet": "integrated HPLC/GC/final calibration",
            "quality": "high",
        }
    else:
        raw_signal = {}
    return {
        "instrument": instrument,
        "raw_signal": raw_signal,
        "processed_estimate": processed,
        "uncertainty": uncertainty,
    }


def _svg_text(text: str) -> str:
    return html.escape(str(text), quote=True)


def _scale(values: list[float], low_px: float, high_px: float) -> list[float]:
    finite = [value for value in values if math.isfinite(value)]
    if not finite:
        return [(low_px + high_px) / 2.0 for _ in values]
    low = min(finite)
    high = max(finite)
    if abs(high - low) < 1.0e-12:
        return [(low_px + high_px) / 2.0 for _ in values]
    return [low_px + (value - low) / (high - low) * (high_px - low_px) for value in values]


def workflow_svg() -> SVG:
    labels = ["提出假设", "设计动作", "执行实验", "读取观测", "建立模型", "下一轮决策"]
    width = 880
    height = 180
    gap = 16
    box_w = 126
    y = 58
    parts = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' "
        "viewBox='0 0 880 180'>",
        "<rect width='880' height='180' fill='#f8fafc'/>",
        "<text x='24' y='32' font-size='18' font-family='Arial' "
        "font-weight='700' fill='#0f172a'>闭环实验决策流程</text>",
    ]
    for index, label in enumerate(labels):
        x = 24 + index * (box_w + gap)
        parts.append(
            f"<rect x='{x}' y='{y}' width='{box_w}' height='54' rx='7' "
            "fill='#ffffff' stroke='#64748b'/>"
        )
        parts.append(
            f"<text x='{x + box_w / 2}' y='{y + 33}' text-anchor='middle' "
            "font-size='13' font-family='Arial' fill='#0f172a'>"
            f"{_svg_text(label)}</text>"
        )
        if index < len(labels) - 1:
            arrow_x = x + box_w
            parts.append(
                f"<path d='M {arrow_x + 4} {y + 27} L {arrow_x + gap - 8} {y + 27}' "
                "stroke='#2563eb' stroke-width='2'/>"
            )
            parts.append(
                f"<path d='M {arrow_x + gap - 8} {y + 27} l -7 -5 l 0 10 z' "
                "fill='#2563eb'/>"
            )
    parts.append("</svg>")
    return SVG("".join(parts))


def reaction_network_svg() -> SVG:
    width = 760
    height = 270
    nodes = {
        "A": (90, 126),
        "P": (285, 126),
        "B": (285, 52),
        "D": (480, 126),
        "E": (480, 52),
        "活性催化剂": (285, 206),
        "失活催化剂": (480, 206),
    }
    arrows = [
        ("A", "P", "目标反应", "#16a34a"),
        ("A", "B", "副产物", "#dc2626"),
        ("P", "D", "产物降解", "#f97316"),
        ("P", "E", "偶联杂质", "#9333ea"),
        ("活性催化剂", "失活催化剂", "催化剂失活", "#475569"),
    ]
    parts = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' "
        "viewBox='0 0 760 270'>",
        "<rect width='760' height='270' fill='#ffffff'/>",
        "<text x='24' y='32' font-size='18' font-family='Arial' "
        "font-weight='700' fill='#0f172a'>ChemWorld 反应网络</text>",
    ]
    for source, target, label, color in arrows:
        x1, y1 = nodes[source]
        x2, y2 = nodes[target]
        parts.append(
            f"<path d='M {x1 + 42} {y1} L {x2 - 44} {y2}' stroke='{color}' "
            "stroke-width='2.5' fill='none'/>"
        )
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2 - 8
        parts.append(
            f"<text x='{mid_x}' y='{mid_y}' font-size='11' font-family='Arial' "
            f"text-anchor='middle' fill='{color}'>{_svg_text(label)}</text>"
        )
    for label, (x, y) in nodes.items():
        parts.append(
            f"<circle cx='{x}' cy='{y}' r='36' fill='#f8fafc' stroke='#334155'/>"
        )
        parts.append(
            f"<text x='{x}' y='{y + 5}' font-size='13' font-family='Arial' "
            "text-anchor='middle' fill='#0f172a'>"
            f"{_svg_text(label)}</text>"
        )
    parts.append("</svg>")
    return SVG("".join(parts))


def line_svg(
    frame: pd.DataFrame,
    *,
    x: str,
    ys: list[str],
    title: str,
    width: int = 780,
    height: int = 330,
) -> SVG:
    margin_left = 62
    margin_right = 24
    margin_top = 54
    margin_bottom = 48
    plot_w = width - margin_left - margin_right
    plot_h = height - margin_top - margin_bottom
    x_values = pd.to_numeric(frame[x], errors="coerce").fillna(0.0).astype(float).tolist()
    all_y = [
        float(value)
        for y_name in ys
        for value in pd.to_numeric(frame[y_name], errors="coerce").fillna(0.0).tolist()
        if math.isfinite(float(value))
    ]
    x_pos = _scale(x_values, margin_left, margin_left + plot_w)
    y_min = min(all_y or [0.0])
    y_max = max(all_y or [1.0])
    colors = ["#2563eb", "#16a34a", "#dc2626", "#9333ea", "#f97316"]
    parts = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' "
        f"viewBox='0 0 {width} {height}'>",
        "<rect width='100%' height='100%' fill='#ffffff'/>",
        f"<text x='22' y='28' font-size='17' font-family='Arial' "
        f"font-weight='700' fill='#0f172a'>{_svg_text(title)}</text>",
        f"<line x1='{margin_left}' y1='{margin_top + plot_h}' "
        f"x2='{margin_left + plot_w}' y2='{margin_top + plot_h}' stroke='#94a3b8'/>",
        f"<line x1='{margin_left}' y1='{margin_top}' "
        f"x2='{margin_left}' y2='{margin_top + plot_h}' stroke='#94a3b8'/>",
        f"<text x='{margin_left}' y='{height - 16}' font-size='11' "
        f"font-family='Arial' fill='#475569'>{_svg_text(x)}</text>",
        f"<text x='14' y='{margin_top - 8}' font-size='11' "
        f"font-family='Arial' fill='#475569'>{y_max:.2f}</text>",
        f"<text x='14' y='{margin_top + plot_h}' font-size='11' "
        f"font-family='Arial' fill='#475569'>{y_min:.2f}</text>",
    ]
    for index, y_name in enumerate(ys):
        values = (
            pd.to_numeric(frame[y_name], errors="coerce")
            .fillna(0.0)
            .astype(float)
            .tolist()
        )
        y_points = _scale(values, margin_top + plot_h, margin_top)
        points = " ".join(f"{px:.1f},{py:.1f}" for px, py in zip(x_pos, y_points, strict=False))
        color = colors[index % len(colors)]
        parts.append(
            f"<polyline points='{points}' fill='none' stroke='{color}' stroke-width='2.4'/>"
        )
        for px, py in zip(x_pos, y_points, strict=False):
            parts.append(f"<circle cx='{px:.1f}' cy='{py:.1f}' r='3.4' fill='{color}'/>")
        lx = margin_left + index * 138
        parts.append(f"<rect x='{lx}' y='{height - 34}' width='12' height='12' fill='{color}'/>")
        parts.append(
            f"<text x='{lx + 18}' y='{height - 24}' font-size='12' "
            f"font-family='Arial' fill='#0f172a'>{_svg_text(y_name)}</text>"
        )
    parts.append("</svg>")
    return SVG("".join(parts))


def bar_svg(
    labels: list[str],
    values: list[float],
    *,
    title: str,
    width: int = 780,
    height: int = 330,
    color: str = "#2563eb",
) -> SVG:
    margin_left = 60
    margin_right = 24
    margin_top = 54
    margin_bottom = 80
    plot_w = width - margin_left - margin_right
    plot_h = height - margin_top - margin_bottom
    max_value = max([float(value) for value in values] + [1.0e-9])
    bar_w = plot_w / max(len(values), 1) * 0.62
    parts = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' "
        f"viewBox='0 0 {width} {height}'>",
        "<rect width='100%' height='100%' fill='#ffffff'/>",
        f"<text x='22' y='28' font-size='17' font-family='Arial' "
        f"font-weight='700' fill='#0f172a'>{_svg_text(title)}</text>",
        f"<line x1='{margin_left}' y1='{margin_top + plot_h}' "
        f"x2='{margin_left + plot_w}' y2='{margin_top + plot_h}' stroke='#94a3b8'/>",
    ]
    for index, (label, value) in enumerate(zip(labels, values, strict=False)):
        value = float(value)
        center = margin_left + (index + 0.5) * plot_w / max(len(values), 1)
        bar_h = plot_h * value / max_value
        x = center - bar_w / 2
        y = margin_top + plot_h - bar_h
        parts.append(
            f"<rect x='{x:.1f}' y='{y:.1f}' width='{bar_w:.1f}' height='{bar_h:.1f}' "
            f"fill='{color}' opacity='0.86'/>"
        )
        parts.append(
            f"<text x='{center:.1f}' y='{y - 6:.1f}' font-size='11' font-family='Arial' "
            f"text-anchor='middle' fill='#0f172a'>{value:.3f}</text>"
        )
        parts.append(
            f"<text x='{center:.1f}' y='{height - 48}' font-size='11' font-family='Arial' "
            f"text-anchor='middle' fill='#334155'>{_svg_text(label)}</text>"
        )
    parts.append("</svg>")
    return SVG("".join(parts))


def heatmap_svg(
    matrix: pd.DataFrame,
    *,
    title: str,
    width: int = 660,
    height: int = 420,
) -> SVG:
    values = matrix.astype(float).to_numpy()
    finite = values[np.isfinite(values)]
    low = float(np.min(finite)) if finite.size else 0.0
    high = float(np.max(finite)) if finite.size else 1.0
    rows = list(matrix.index)
    cols = list(matrix.columns)
    cell_w = 86
    cell_h = 50
    start_x = 112
    start_y = 76
    parts = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' "
        f"viewBox='0 0 {width} {height}'>",
        "<rect width='100%' height='100%' fill='#ffffff'/>",
        f"<text x='22' y='30' font-size='17' font-family='Arial' "
        f"font-weight='700' fill='#0f172a'>{_svg_text(title)}</text>",
    ]
    for col_index, col in enumerate(cols):
        x = start_x + col_index * cell_w + cell_w / 2
        parts.append(
            f"<text x='{x}' y='{start_y - 16}' text-anchor='middle' font-size='12' "
            f"font-family='Arial' fill='#334155'>{_svg_text(col)}</text>"
        )
    for row_index, row in enumerate(rows):
        y = start_y + row_index * cell_h + cell_h / 2 + 4
        parts.append(
            f"<text x='{start_x - 16}' y='{y}' text-anchor='end' font-size='12' "
            f"font-family='Arial' fill='#334155'>{_svg_text(row)}</text>"
        )
        for col_index, col in enumerate(cols):
            value = float(matrix.loc[row, col])
            if not math.isfinite(value):
                value = low
            ratio = 0.0 if high == low else (value - low) / (high - low)
            red = int(240 - 130 * ratio)
            green = int(249 - 100 * ratio)
            blue = int(255 - 25 * ratio)
            x = start_x + col_index * cell_w
            y_cell = start_y + row_index * cell_h
            parts.append(
                f"<rect x='{x}' y='{y_cell}' width='{cell_w}' height='{cell_h}' "
                f"fill='rgb({red},{green},{blue})' stroke='#ffffff'/>"
            )
            parts.append(
                f"<text x='{x + cell_w / 2}' y='{y_cell + 31}' text-anchor='middle' "
                f"font-size='12' font-family='Arial' fill='#0f172a'>{value:.3f}</text>"
            )
    parts.append(
        f"<text x='{start_x}' y='{height - 28}' font-size='11' font-family='Arial' "
        f"fill='#475569'>low={low:.3f}, high={high:.3f}</text>"
    )
    parts.append("</svg>")
    return SVG("".join(parts))


def scatter_svg(
    frame: pd.DataFrame,
    *,
    x: str,
    y: str,
    title: str,
    width: int = 520,
    height: int = 420,
) -> SVG:
    margin_left = 62
    margin_right = 28
    margin_top = 54
    margin_bottom = 54
    plot_w = width - margin_left - margin_right
    plot_h = height - margin_top - margin_bottom
    x_values = pd.to_numeric(frame[x], errors="coerce").fillna(0.0).astype(float).tolist()
    y_values = pd.to_numeric(frame[y], errors="coerce").fillna(0.0).astype(float).tolist()
    x_pos = _scale(x_values, margin_left, margin_left + plot_w)
    y_pos = _scale(y_values, margin_top + plot_h, margin_top)
    parts = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' "
        f"viewBox='0 0 {width} {height}'>",
        "<rect width='100%' height='100%' fill='#ffffff'/>",
        f"<text x='22' y='28' font-size='17' font-family='Arial' "
        f"font-weight='700' fill='#0f172a'>{_svg_text(title)}</text>",
        f"<line x1='{margin_left}' y1='{margin_top + plot_h}' "
        f"x2='{margin_left + plot_w}' y2='{margin_top + plot_h}' stroke='#94a3b8'/>",
        f"<line x1='{margin_left}' y1='{margin_top}' "
        f"x2='{margin_left}' y2='{margin_top + plot_h}' stroke='#94a3b8'/>",
        f"<text x='{margin_left + plot_w / 2}' y='{height - 14}' "
        f"font-size='12' font-family='Arial' text-anchor='middle' fill='#475569'>"
        f"{_svg_text(x)}</text>",
        f"<text x='16' y='{margin_top - 8}' font-size='12' "
        f"font-family='Arial' fill='#475569'>{_svg_text(y)}</text>",
    ]
    for px, py, x_value, y_value in zip(x_pos, y_pos, x_values, y_values, strict=False):
        parts.append(f"<circle cx='{px:.1f}' cy='{py:.1f}' r='5' fill='#2563eb'/>")
        parts.append(
            f"<title>{_svg_text(x)}={x_value:.3f}, {_svg_text(y)}={y_value:.3f}</title>"
        )
    parts.append("</svg>")
    return SVG("".join(parts))


def show_json_panel(title: str, payload: dict[str, Any]) -> None:
    escaped = html.escape(str(payload), quote=True)
    display(
        HTML(
            "<div style='border:1px solid #cbd5e1;border-radius:8px;padding:12px;"
            "font-family:Consolas,monospace;background:#f8fafc'>"
            f"<strong>{html.escape(title)}</strong><pre>{escaped}</pre></div>"
        )
    )


def display_api_card() -> None:
    display(
        HTML(
            "<div style='border:1px solid #cbd5e1;border-radius:8px;padding:12px;"
            "background:#f8fafc;margin:10px 0'>"
            "<strong>Notebook API 速查卡</strong>"
            "<ul>"
            "<li><code>tu.run_recipe(recipe, seed)</code>：执行一组 recipe，"
            "并返回最终检测行。</li>"
            "<li><code>tu.run_events(events, seed)</code>：执行显式事件动作，"
            "并返回公开轨迹表。</li>"
            "<li><code>tu.line_svg / bar_svg / heatmap_svg</code>：生成无需额外依赖的 "
            "notebook 图。</li>"
            "</ul>"
            "</div>"
        )
    )


def display_score_terms() -> None:
    display(
        HTML(
            "<div style='border:1px solid #cbd5e1;border-radius:8px;padding:12px;"
            "background:#fff7ed;margin:10px 0'>"
            "<strong>评分术语</strong>"
            "<ul>"
            "<li><code>observed_score</code>/<code>reward</code>：由当前可见观测或延续估计计算的在线反馈。</li>"
            "<li><code>leaderboard_score</code>：正式 benchmark 指标使用的 final assay 得分。</li>"
            "<li><code>hidden_true_score</code>：仅供开发者调试的隐藏真实分数，不出现在学生轨迹中。</li>"
            "</ul>"
            "</div>"
        )
    )


def display_learning_goal(day: int, title: str, goals: list[str]) -> None:
    items = "".join(f"<li>{html.escape(goal)}</li>" for goal in goals)
    display(
        HTML(
            "<div style='border-left:5px solid #2563eb;padding:12px 16px;"
            "background:#eff6ff;margin:10px 0'>"
            f"<div style='font-weight:700'>第 {day} 天：{html.escape(title)}</div>"
            f"<ul>{items}</ul></div>"
        )
    )


def display_notebook_style() -> None:
    """Install lightweight visual polish for tutorial notebooks."""

    display(
        HTML(
            """
<style>
.cw-hero {
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 18px 20px;
  margin: 10px 0 16px 0;
  background: linear-gradient(135deg, #f8fafc 0%, #eef6ff 54%, #f0fdf4 100%);
  color: #0f172a;
}
.cw-hero h1 {
  font-size: 26px;
  margin: 0 0 6px 0;
  letter-spacing: 0;
}
.cw-hero .subtitle {
  font-size: 14px;
  color: #334155;
  margin-bottom: 12px;
}
.cw-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 10px;
}
.cw-card {
  background: rgba(255,255,255,0.88);
  border: 1px solid #dbe3ef;
  border-radius: 8px;
  padding: 10px 12px;
}
.cw-card strong {
  display: block;
  margin-bottom: 5px;
}
.cw-card ul {
  margin: 0;
  padding-left: 18px;
}
.cw-kicker {
  display: inline-block;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  color: #0369a1;
  margin-bottom: 6px;
}
.cw-note {
  border-left: 5px solid #7c3aed;
  background: #f5f3ff;
  padding: 12px 16px;
  margin: 12px 0;
}
.cw-reflect {
  border-left: 5px solid #ea580c;
  background: #fff7ed;
  padding: 12px 16px;
  margin: 12px 0;
}
.cw-timeline {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(82px, 1fr));
  gap: 6px;
  margin: 10px 0 14px 0;
}
.cw-day {
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 8px 6px;
  background: #ffffff;
  text-align: center;
  font-size: 12px;
}
.cw-day.active {
  background: #dbeafe;
  border-color: #2563eb;
  font-weight: 700;
}
</style>
            """
        )
    )


def display_tutorial_header(
    *,
    day: int,
    title: str,
    subtitle: str,
    focus: list[str],
    deliverables: list[str],
    project_link: str,
) -> None:
    """Render a consistent opening card for one tutorial notebook."""

    display_notebook_style()
    focus_items = "".join(f"<li>{html.escape(item)}</li>" for item in focus)
    deliverable_items = "".join(
        f"<li>{html.escape(item)}</li>" for item in deliverables
    )
    display(
        HTML(
            "<div class='cw-hero'>"
            f"<div class='cw-kicker'>ChemWorld 教程 - 第 {day} 天</div>"
            f"<h1>{html.escape(title)}</h1>"
            f"<div class='subtitle'>{html.escape(subtitle)}</div>"
            "<div class='cw-grid'>"
            "<div class='cw-card'><strong>今天你将学习</strong>"
            f"<ul>{focus_items}</ul></div>"
            "<div class='cw-card'><strong>需要产出的证据</strong>"
            f"<ul>{deliverable_items}</ul></div>"
            "<div class='cw-card'><strong>它如何连接到 benchmark</strong>"
            f"<p>{html.escape(project_link)}</p></div>"
            "</div></div>"
        )
    )


def display_course_map(active_day: int) -> None:
    """Show where the current notebook sits in the twelve-day sequence."""

    labels = [
        "实验室",
        "世界规则",
        "观测",
        "扫描",
        "建模",
        "评分",
        "成果包",
        "GPT",
        "BO",
        "公开榜",
        "私有泛化",
        "展示",
    ]
    cells = []
    for index, label in enumerate(labels, start=1):
        cls = "cw-day active" if index == active_day else "cw-day"
        cells.append(f"<div class='{cls}'>第{index}天<br>{html.escape(label)}</div>")
    display(HTML("<div class='cw-timeline'>" + "".join(cells) + "</div>"))


def display_reflection_box(questions: list[str]) -> None:
    items = "".join(f"<li>{html.escape(question)}</li>" for question in questions)
    display(
        HTML(
            "<div class='cw-reflect'><strong>课后反思</strong>"
            f"<ul>{items}</ul></div>"
        )
    )


def display_project_canvas(
    *,
    title: str,
    problem: str,
    strategy: str,
    artifact: str,
    risks: str,
) -> None:
    display_notebook_style()
    display(
        HTML(
            "<div class='cw-hero'>"
            f"<div class='cw-kicker'>项目画布</div><h1>{html.escape(title)}</h1>"
            "<div class='cw-grid'>"
            "<div class='cw-card'><strong>科学问题</strong>"
            f"<p>{html.escape(problem)}</p></div>"
            f"<div class='cw-card'><strong>策略</strong><p>{html.escape(strategy)}</p></div>"
            f"<div class='cw-card'><strong>成果物</strong><p>{html.escape(artifact)}</p></div>"
            f"<div class='cw-card'><strong>已知风险</strong><p>{html.escape(risks)}</p></div>"
            "</div></div>"
        )
    )


def world_law_svg() -> SVG:
    width = 860
    height = 300
    rows = [
        ("本体", "物质、相、容器、仪器"),
        ("世界宪法", "单位、守恒、安全、前置条件"),
        ("状态转移", "反应 ODE、分配、分离"),
        ("观测", "有噪声的仪器、mask、成本"),
        ("任务", "同一世界规律上的不同目标切片"),
    ]
    parts = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' "
        f"viewBox='0 0 {width} {height}'>",
        "<rect width='100%' height='100%' fill='#ffffff'/>",
        "<text x='24' y='32' font-size='18' font-family='Arial' "
        "font-weight='700' fill='#0f172a'>一个物理化学世界，多种任务切片</text>",
    ]
    x = 44
    box_w = 150
    y = 90
    for index, (title, desc) in enumerate(rows):
        bx = x + index * 158
        parts.append(
            f"<rect x='{bx}' y='{y}' width='{box_w}' height='96' rx='8' "
            "fill='#f8fafc' stroke='#64748b'/>"
        )
        parts.append(
            f"<text x='{bx + box_w / 2}' y='{y + 32}' text-anchor='middle' "
            "font-size='14' font-family='Arial' font-weight='700' fill='#0f172a'>"
            f"{_svg_text(title)}</text>"
        )
        parts.append(
            f"<foreignObject x='{bx + 12}' y='{y + 44}' width='{box_w - 24}' height='42'>"
            "<div xmlns='http://www.w3.org/1999/xhtml' "
            "style='font-family:Arial;font-size:11px;color:#475569;text-align:center'>"
            f"{_svg_text(desc)}</div></foreignObject>"
        )
        if index < len(rows) - 1:
            ax = bx + box_w + 6
            parts.append(
                f"<path d='M {ax} {y + 48} L {ax + 28} {y + 48}' "
                "stroke='#2563eb' stroke-width='2'/>"
            )
            parts.append(
                f"<path d='M {ax + 28} {y + 48} l -7 -5 l 0 10 z' "
                "fill='#2563eb'/>"
            )
    parts.append(
        "<text x='44' y='238' font-size='13' font-family='Arial' fill='#334155'>"
        "任务只改变预算、可用操作、仪器、指标和 split；不会创建一套新的物理小游戏。</text>"
    )
    parts.append("</svg>")
    return SVG("".join(parts))


def leaderboard_blueprint_svg() -> SVG:
    width = 860
    height = 360
    tracks = [
        ("性能", "最终检测得分", "#2563eb"),
        ("安全", "风险与违规次数", "#16a34a"),
        ("效率", "单位预算下的最优得分", "#f97316"),
        ("泛化", "public-private 差距", "#7c3aed"),
        ("理解", "机制解释质量", "#0f766e"),
    ]
    parts = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' "
        f"viewBox='0 0 {width} {height}'>",
        "<rect width='100%' height='100%' fill='#ffffff'/>",
        "<text x='24' y='34' font-size='18' font-family='Arial' "
        "font-weight='700' fill='#0f172a'>ChemWorld 共享世界挑战</text>",
        "<text x='24' y='58' font-size='12' font-family='Arial' fill='#475569'>"
        "Leaderboard 应奖励科学决策质量，而不只是一次高分。</text>",
    ]
    for index, (name, metric, color) in enumerate(tracks):
        y = 92 + index * 48
        parts.append(
            f"<rect x='52' y='{y}' width='190' height='34' rx='7' "
            f"fill='{color}' opacity='0.16' stroke='{color}'/>"
        )
        parts.append(
            f"<text x='66' y='{y + 22}' font-size='13' font-family='Arial' "
            f"font-weight='700' fill='#0f172a'>{_svg_text(name)}</text>"
        )
        parts.append(
            f"<text x='268' y='{y + 22}' font-size='12' font-family='Arial' "
            f"fill='#334155'>{_svg_text(metric)}</text>"
        )
        parts.append(
            f"<path d='M 470 {y + 17} L 590 {y + 17}' stroke='{color}' stroke-width='3'/>"
        )
    parts.append(
        "<rect x='620' y='100' width='190' height='146' rx='8' fill='#f8fafc' "
        "stroke='#64748b'/>"
    )
    parts.append(
        "<text x='715' y='130' text-anchor='middle' font-size='14' font-family='Arial' "
        "font-weight='700' fill='#0f172a'>综合报告</text>"
    )
    parts.append(
        "<foreignObject x='642' y='148' width='146' height='82'>"
        "<div xmlns='http://www.w3.org/1999/xhtml' "
        "style='font-family:Arial;font-size:12px;color:#334155;text-align:center'>"
        "排名表 + 轨迹回放 + 解释卡 + 失败分析"
        "</div></foreignObject>"
    )
    parts.append("</svg>")
    return SVG("".join(parts))

