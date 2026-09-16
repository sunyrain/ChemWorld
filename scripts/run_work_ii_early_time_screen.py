"""W2-101 development screen; fixed full factorial, no provider calls."""

# ruff: noqa: RUF001
from __future__ import annotations

import argparse
import itertools
import json
import threading
import time
from collections import Counter
from pathlib import Path

import numpy as np
from scripts import run_work_ii_astra_corrected_pilot as base

ROOT = base.ROOT
BOUNDS = {**base.BOUNDS, "reaction_duration_s": (30.0, 5400.0)}
LEVELS = ((350, 377.5, 405), (30, 120, 300, 600, 1200, 3600), (0, 1), (1200, 3600))
NOTE = "workstreams/flagship_tasks/WORK_II_EARLY_TIME_SCREEN_NOTE.md"
REPORT = ROOT / "workstreams/flagship_tasks/reports/work-ii-early-time-screen-20260914.json"
TOTAL = 288


def grid():
    return [base.plan(values) for values in itertools.product(*LEVELS)]


def action_value(utilities):
    """Regrets use world-normalized utilities; no hidden truth or fitting."""
    u = np.asarray(utilities, dtype=float)
    best = u.max(axis=1)
    normalized = u / np.maximum(best[:, None], 1e-12)
    axis_groups = {"R": ((0, 3), (2, 1)), "C": ((0, 2), (3, 1))}
    axis_loss = {
        axis: float(np.mean([1 - normalized[list(pair)].mean(axis=0).max() for pair in pairs]))
        for axis, pairs in axis_groups.items()
    }
    source_best = np.argmax(u[:2], axis=1)
    copied = normalized[2:, source_best].max(axis=1)
    return {
        "best_by_world": {
            w: {
                "grid_index": int(np.argmax(u[i])),
                "utility": float(best[i]),
                "plan": grid()[int(np.argmax(u[i]))],
            }
            for i, w in enumerate(base.WORLDS)
        },
        "best_common_recipe_mean_relative_loss": float(1 - normalized.mean(axis=0).max()),
        "axis_common_recipe_mean_relative_loss": axis_loss,
        "best_of_two_source_winners_heldout_mean_relative_loss": float(1 - copied.mean()),
        "source_winner_indices": source_best.tolist(),
        "source_reuse_relative_loss_by_heldout_world": dict(
            zip(base.WORLDS[2:], (1 - copied).tolist(), strict=True)
        ),
        "all_144_source_recipes_include_all_72_control_plans": True,
    }


def summarize(root, failure=None):
    rows = [base.read(p) for p in sorted((root / "physical").rglob("result.json"))]
    attempts = list((root / "physical").rglob("attempt.json"))
    counts = Counter(r["status"] for r in rows)
    resources = Counter()
    for row in rows:
        resources.update(row["resources"])
    report = {
        "status": "development_stopped" if failure else "development_completed",
        "formal_result": False,
        "note": NOTE,
        "run_root": root.relative_to(ROOT).as_posix(),
        "physical_runs": {
            "planned": TOTAL,
            "attempted": len(attempts),
            "completed": counts["completed"],
            "failed": counts["failed"],
            "interrupted": len(attempts) - len(rows),
            "not_started": TOTAL - len(attempts),
            "exact_replay_verified": sum(r["exact_replay"] for r in rows),
        },
        "model_sessions": 0,
        "retries": 0,
        "failure": failure,
        "bounds": BOUNDS,
        "levels": LEVELS,
        "resources": dict(resources),
        "rows": rows,
    }
    if counts["completed"] == TOTAL:
        lookup = {(r["world"], int(r["name"].rsplit("/", 1)[1])): r for r in rows}
        utility = [
            [lookup[w, i]["public"]["terminal"]["utility_per_hour"] for i in range(72)]
            for w in base.WORLDS
        ]
        value = action_value(utility)
        invariant = all(
            lookup[r + "C1", i]["public"]["upstream_hplc"]
            == lookup[r + "C2", i]["public"]["upstream_hplc"]
            for r in ("R1", "R2")
            for i in range(72)
        )
        support = base.support_report(
            {"full_diagonal_grid": [r for r in rows if r["world"] in base.TRAIN]},
            {r["name"]: r for r in rows if r["world"] not in base.TRAIN},
        )
        near = sum(r["near_support"] for r in support)
        criteria = {
            "runtime_and_replay": invariant
            and report["physical_runs"]["exact_replay_verified"] == TOTAL,
            "common_recipe_loss_at_least_10pct": value["best_common_recipe_mean_relative_loss"]
            >= 0.1,
            "R_axis_loss_at_least_5pct": value["axis_common_recipe_mean_relative_loss"]["R"]
            >= 0.05,
            "C_axis_loss_at_least_5pct": value["axis_common_recipe_mean_relative_loss"]["C"]
            >= 0.05,
            "source_winners_loss_at_least_10pct": value[
                "best_of_two_source_winners_heldout_mean_relative_loss"
            ]
            >= 0.1,
            "public_support_at_least_80pct": near / 144 >= 0.8,
        }
        report.update(
            action_value=value,
            support=support,
            near_support={"count": near, "denominator": 144},
            upstream_invariant_to_C=invariant,
            criteria=criteria,
            screen_passed=all(criteria.values()),
        )
    base.write(root / "summary.json", report)
    base.write(REPORT, report)
    lines = [
        "# 早期反应区间开发筛选",
        "",
        f"状态：{report['status']}。仅一个既有四格组；不属于正式证据。",
        "",
        f"原始轨迹：{counts['completed']}/{TOTAL}完成；失败{counts['failed']}；"
        f"重放{report['physical_runs']['exact_replay_verified']}；模型会话0。",
        "",
        "完整扫描3个反应温度、6个反应时间（30—3600秒）、2个冷却比例、2个冷却时长。",
        "时间及采样收费与上一块一致；效用仍是公开观测代理，并非精确隔离产物摩尔数。",
    ]
    if "action_value" in report:
        lines += [
            "",
            "| 世界 | 反应K/秒 | 冷却比例/秒 | 最佳网格效用/小时 |",
            "| --- | --- | --- | --- |",
        ]
        for w, best in value["best_by_world"].items():
            p = best["plan"]
            lines.append(
                f"| {w} | {p['reaction_temperature_K']}/{p['reaction_duration_s']} | "
                f"{p['cooling_fraction']}/{p['cooling_duration_s']} | {best['utility']:.6f} |"
            )
        lines += [
            "",
            f"最优共用配方平均相对损失：{value['best_common_recipe_mean_relative_loss']:.2%}。",
            f"R轴共用损失：{value['axis_common_recipe_mean_relative_loss']['R']:.2%}；"
            f"C轴共用损失：{value['axis_common_recipe_mean_relative_loss']['C']:.2%}。",
            f"两学习最佳配方在每个留出世界取较好者，平均损失："
            f"{value['best_of_two_source_winners_heldout_mean_relative_loss']:.2%}。",
            f"公开接口近支持：{near}/144。完整支持及行动资格通过：{report['screen_passed']}。",
            "",
            "逐格结果、阈值、失败、实际温度、资源及支持距离均见同名JSON。",
            "网格上界只针对预定离散动作；来源已覆盖全部72种控制，不能把全部历史配方集合称为缺少目标最优动作。",
            "最佳来源配方复用比较只回答是否需要重新选择配方，不证明组合推理不可替代。",
        ]
    if failure:
        lines += ["", f"停止原因：{failure}"]
    REPORT.with_suffix(".md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k not in ("rows", "support")}), flush=True)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--initialization-from", type=Path, required=True)
    args = parser.parse_args()
    root = args.output.resolve()
    root.mkdir(parents=True, exist_ok=False)
    seed = base.read(args.initialization_from / "private_inputs.json")["seed"]
    base.write(root / "private_inputs.json", {"seed": seed})
    base.write(root / "design.json", {"note": NOTE, "grid": grid(), "total": TOTAL})
    for source in (Path(__file__), Path(base.__file__)):
        (root / source.name).write_bytes(source.read_bytes())
    (root / "experiment_note.md").write_bytes((ROOT / NOTE).read_bytes())
    started = time.monotonic()
    stop = threading.Event()

    def heartbeat():
        while not stop.wait(30):
            n = len(list((root / "physical").rglob("result.json")))
            rate = n * 60 / (time.monotonic() - started)
            print(
                json.dumps(
                    {
                        "stage": "early_time_full_factorial",
                        "completed": n,
                        "total": TOTAL,
                        "batches_per_minute": round(rate, 2),
                        "eta_minutes": round((TOTAL - n) / rate, 1) if rate else None,
                    }
                ),
                flush=True,
            )

    worker = threading.Thread(target=heartbeat, daemon=True)
    worker.start()
    failure = None
    try:
        for w in base.WORLDS:
            for i, p in enumerate(grid()):
                if time.monotonic() - started > 7200:
                    raise TimeoutError("two-hour block limit")
                base.execute_batch(root, f"grid/{w}/{i:02d}", w, p, seed, bounds=BOUNDS)
    except (Exception, KeyboardInterrupt) as exc:
        failure = f"{type(exc).__name__}: {exc}"
    finally:
        stop.set()
        worker.join(timeout=2)
        base.write(root / "closed.json", {"failure": failure, "resume_planned": False})
        summarize(root, failure)
    if failure:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
