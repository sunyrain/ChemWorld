"""W2-117 fixed development gate screen; real campaigns, no provider calls."""

# ruff: noqa: RUF001
from __future__ import annotations

import argparse
import json
import math
import threading
import time
from collections import Counter
from pathlib import Path

import gymnasium as gym

import chemworld  # noqa: F401
from chemworld.campaign_resources import CampaignResourceCard
from chemworld.data.logging import load_jsonl
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.tasks import get_task
from chemworld.world.instruments import chemworld_instruments

ROOT = Path(__file__).resolve().parents[1]
NOTE = "workstreams/flagship_tasks/WORK_II_NEW_SYSTEM_GATE_NOTE.md"
REPORT = ROOT / "workstreams/flagship_tasks/reports/work-ii-new-system-gates-20260916.json"
TASKS = {
    "RX": "reaction-mechanism-explanation",
    "EQ": "equilibrium-characterization",
    "BC": "low-budget-characterization",
    "PA": "partition-discovery",
    "FL": "flow-reaction-optimization",
}
CHANNELS = {
    "RX": ["yield", "conversion", "byproduct_signal"],
    "BC": ["yield", "conversion", "byproduct_signal"],
    "EQ": ["pH_normalized", "acid_dissociation_fraction", "precipitation_signal"],
    "PA": ["product_in_organic", "product_in_aqueous"],
    "FL": ["flow_conversion", "yield"],
}
AXES = {
    "EQ": "equilibrium.acid-base-constants",
    "PA": "partition.distribution-coefficient",
    "FL": "flow.reaction-kinetics",
}
STOCK = {
    "add_solvent": ("solvent_L", "volume_L"),
    "add_reagent": ("reagent_mol", "amount_mol"),
    "add_catalyst": ("catalyst_mol", "catalyst_amount_mol"),
    "add_phase": ("phase_liquid_L", "volume_L"),
    "add_extractant": ("extractant_L", "volume_L"),
}


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def action(operation, **kwargs):
    return {"operation": operation, **kwargs}


def measure(instrument):
    return action("measure", instrument=instrument)


def recipes(code):
    close = [action("terminate"), measure("final_assay")]
    if code in {"RX", "BC"}:
        points = (
            [(335, 30), (385, 30), (335, 300), (385, 300)]
            if code == "RX"
            else [(345, 120), (385, 120)]
        )
        return [
            [
                action("add_solvent", volume_L=0.028, solvent=2),
                action("add_reagent", amount_mol=0.010),
                action("add_catalyst", catalyst_amount_mol=0.00025, catalyst=1),
                action(
                    "heat", target_temperature_K=temp, duration_s=duration, stirring_speed_rpm=720
                ),
                measure("hplc"),
                action("wait", duration_s=duration if code == "RX" else 60, stirring_speed_rpm=720),
                measure("uvvis"),
                *close,
            ]
            for temp, duration in points
        ]
    if code == "EQ":
        return [
            [
                action("add_solvent", volume_L=volume, solvent=0),
                action("add_reagent", amount_mol=amount),
                measure("ph_meter"),
                measure("uvvis"),
                *close,
            ]
            for volume, amount in [(0.020, 0.002), (0.060, 0.002), (0.020, 0.010), (0.060, 0.010)]
        ]
    if code == "PA":
        return [
            [
                action("add_solvent", volume_L=0.025, solvent=1),
                action("add_phase", phase="aqueous", volume_L=0.018),
                action("add_extractant", extractant=extractant, volume_L=volume),
                action("mix", duration_s=240, stirring_speed_rpm=750),
                action("settle", duration_s=360),
                measure("hplc"),
                action("separate_phase", target_phase="organic"),
                measure("hplc"),
                *close,
            ]
            for extractant, volume in [(1, 0.006), (3, 0.006), (1, 0.024), (3, 0.024)]
        ]
    if code == "FL":
        return [
            [
                action("add_solvent", volume_L=0.026, solvent=2),
                action("add_reagent", amount_mol=0.010),
                action("add_catalyst", catalyst_amount_mol=0.00022, catalyst=1),
                action("set_flow_rate", flow_rate_mL_min=flow, residence_time_s=residence),
                action("run_flow", target_temperature_K=temp, duration_s=2 * residence),
                measure("hplc"),
                *close,
            ]
            for flow, residence, temp in [
                (0.6, 300, 340),
                (0.6, 300, 390),
                (1.8, 1200, 340),
                (1.8, 1200, 390),
            ]
        ]
    raise ValueError(code)


def resource_card(code):
    batches = recipes(code)
    n = len(batches)
    instruments = sum(
        a["operation"] == "measure" and a["instrument"] != "final_assay"
        for batch in batches
        for a in batch
    )
    return CampaignResourceCard(
        card_id=f"work-ii-new-system-gates-{code}",
        operation_attempt_limit=get_task(TASKS[code]).budget,
        vessel_start_limit=n,
        final_assay_limit=n,
        nonfinal_instrument_use_limit=instruments,
        stock_limits={
            "reagent_mol": 0.04 * n,
            "solvent_L": 0.08 * n,
            "catalyst_mol": 0.005 * n,
            "phase_liquid_L": 0.06 * n,
            "extractant_L": 0.06 * n,
        },
        process_time_limit_s=7200 * n,
    )


def check_entries(root, progress):
    rows = []
    modes = {
        "O": "opaque_codes",
        "A": "anonymous_nominal_properties",
        "M": "anonymous_misindexed_properties",
    }
    for code, task in TASKS.items():
        for arm, mode in modes.items():
            progress.update(stage="materializer", unit=f"{code}-{arm}")
            config = {"mode": mode}
            if arm == "M":
                config.update(target_field="solvent", descriptor_permutation=[1, 0, 2, 3])
            row = {"card": code, "arm": arm, "passed": False}
            env = None
            try:
                env = gym.make(
                    get_task(task).env_id, task_id=task, seed=0, material_information=config
                )
                env.reset(seed=0)
                row.update(
                    passed=True,
                    permissions={
                        "operations": sorted(env.unwrapped.allowed_operations),
                        "instruments": sorted(env.unwrapped.allowed_instruments),
                        "budget": env.unwrapped.task_info()["budget"],
                    },
                    dossier=env.unwrapped.material_information_dossier(),
                )
            except Exception as exc:
                row["error"] = {"type": type(exc).__name__, "message": str(exc)}
            finally:
                if env is not None:
                    env.close()
            rows.append(row)
            write(root / "entry_checks.json", rows)
    return rows


def resource_checks(records, snapshots, card):
    errors = []
    stocks = Counter()
    finals = nonfinal = 0
    previous = {}
    for index, (row, snapshot) in enumerate(zip(records, snapshots, strict=True), 1):
        state = snapshot.get("state", {})
        if state.get("operation_attempts") != index:
            errors.append(f"step {index}: operation accounting")
        for key in (
            "operation_attempts",
            "vessel_starts",
            "final_assays",
            "nonfinal_instrument_uses",
        ):
            if state.get(key, -1) < previous.get(key, 0):
                errors.append(f"step {index}: {key} reset")
        if row.get("transaction_status") == "committed":
            a = row["action"]
            if a["operation"] in STOCK:
                key, field = STOCK[a["operation"]]
                stocks[key] += a[field]
            if a["operation"] == "measure":
                finals += a["instrument"] == "final_assay"
                nonfinal += a["instrument"] != "final_assay"
        if state.get("final_assays") != finals or state.get("nonfinal_instrument_uses") != nonfinal:
            errors.append(f"step {index}: instrument accounting")
        actual = state.get("stocks_used", {})
        for key in set(actual) | set(stocks):
            if not math.isclose(actual.get(key, 0), stocks[key], rel_tol=0, abs_tol=1e-10):
                errors.append(f"step {index}: {key} accounting")
            if actual.get(key, 0) > card.stock_limits.get(key, 0) + 1e-10:
                errors.append(f"step {index}: {key} over budget")
        previous = state
    if not records:
        errors.append("no physical trajectory")
    if previous.get("vessel_starts") != finals:
        errors.append("vessel/closed-batch mismatch")
    return {"passed": not errors, "errors": errors, "final_state": previous}


def execute(root, code, variant, progress):
    task = TASKS[code]
    batches = recipes(code)
    actions = [a for batch in batches for a in batch]
    intervention = (
        [{"axis_id": AXES[code], "mode": "extrapolation", "severity": 1.0}]
        if variant == "shift"
        else []
    )
    folder = root / f"{code}-{variant}"
    folder.mkdir()
    card = resource_card(code)
    progress.update(stage="campaign", unit=folder.name, operations=0)
    write(
        folder / "plan.json",
        {
            "task": task,
            "actions": actions,
            "world_interventions": intervention,
            "seed": 0,
            "observation_seed": 1,
            "resource_card": card.to_dict(),
        },
    )
    snapshots, holder = [], []
    started = time.monotonic()

    def wrap(env):
        holder.append(env.unwrapped)
        return env

    def on_step(record, trace):
        del trace
        snapshots.append(holder[0].public_campaign_resource_state())
        progress["operations"] += 1
        if record.info.get("transaction_status") != "committed":
            raise RuntimeError(f"failed transaction at operation {progress['operations']}")

    failure = None
    try:
        run_agent(
            env_id=get_task(task).env_id,
            agent=_FrozenTruthReplayAgent(actions),
            world_split="public-test",
            budget=get_task(task).budget,
            budget_override=get_task(task).budget,
            objective="balanced",
            seed=0,
            agent_seed=0,
            observation_seed=1,
            task_id=task,
            output_path=folder / "trajectory.jsonl",
            episode_mode_override="campaign",
            campaign_resource_card=card,
            observation_noise_mode="keyed",
            observation_noise_namespace="work-ii-new-system-gates-20260916",
            world_interventions=intervention,
            step_callback=on_step,
            env_wrapper=wrap,
        )
    except Exception as exc:
        failure = {"type": type(exc).__name__, "message": str(exc)}
    execution_seconds = time.monotonic() - started
    records = (
        load_jsonl(folder / "trajectory.jsonl") if (folder / "trajectory.jsonl").exists() else []
    )
    write(folder / "resource_events.json", snapshots)
    progress["stage"] = "exact-replay"
    replay_started = time.monotonic()
    try:
        replay = verify_records(records, tolerance=0, world_interventions=intervention).to_dict()
    except Exception as exc:
        replay = {"verified": False, "error": {"type": type(exc).__name__, "message": str(exc)}}
    replay_seconds = time.monotonic() - replay_started
    write(folder / "replay.json", replay)
    finals = [
        r
        for r in records
        if r.get("transaction_status") == "committed" and r.get("instrument") == "final_assay"
    ]
    metrics = [
        {k: v for k, v in r["observation"].items() if v is not None and not k.endswith("_mask")}
        for r in finals
    ]
    resources = resource_checks(records, snapshots, card)
    runtime = failure is None and len(records) == len(actions) and len(finals) == len(batches)
    errors = [
        {
            "step": r["step"],
            "action": r["action"],
            "status": r.get("transaction_status"),
            "reason": r.get("rollback_reason"),
            "preconditions": r.get("preconditions"),
        }
        for r in records
        if r.get("transaction_status") != "committed"
    ]
    result = {
        "card": code,
        "variant": variant,
        "task": task,
        "planned_batches": len(batches),
        "completed_batches": len(finals),
        "planned_operations": len(actions),
        "recorded_operations": len(records),
        "runtime_passed": runtime,
        "resources": resources,
        "replay": replay,
        "failure": failure,
        "failed_transactions": errors,
        "final_metrics": metrics,
        "execution_seconds": execution_seconds,
        "replay_seconds": replay_seconds,
        "artifact_directory": folder.relative_to(ROOT).as_posix(),
    }
    write(folder / "result.json", result)
    return result


def contrast(left, right, channels):
    noise = chemworld_instruments()["final_assay"].noise_std
    result = {}
    for key in channels:
        threshold = max(0.01 if key == "pH_normalized" else 0.02, 3 * math.sqrt(2) * noise[key])
        a, b = left.get(key), right.get(key)
        delta = None if a is None or b is None else float(b - a)
        result[key] = {
            "delta": delta,
            "threshold": threshold,
            "passed": delta is not None and abs(delta) >= threshold,
        }
    return result


def checks_ok(cell):
    return cell["runtime_passed"] and cell["resources"]["passed"] and cell["replay"]["verified"]


def retained_diagnostics(root, cells):
    """Read paid measurements only; exploratory diagnostics do not revise gates."""
    measurements = []
    for cell in cells:
        path = root / f"{cell['card']}-{cell['variant']}" / "trajectory.jsonl"
        if not path.exists():
            continue
        batch = 1
        for row in load_jsonl(path):
            if row.get("transaction_status") != "committed":
                continue
            if row.get("operation_type") == "measure":
                keys = [*CHANNELS[cell["card"]], "phase_ratio", "safety_risk"]
                measurements.append(
                    {
                        "card": cell["card"],
                        "variant": cell["variant"],
                        "batch": batch,
                        "step": row["step"],
                        "instrument": row.get("instrument"),
                        "public_values": {
                            k: row["observation"][k]
                            for k in keys
                            if row["observation"].get(k) is not None
                        },
                    }
                )
            if row.get("instrument") == "final_assay":
                batch += 1
    return {"status": "posthoc_read_only_no_gate_revision", "measurements": measurements}


def build_report(root, entries, cells, elapsed):
    systems = []
    for code in TASKS:
        group = [r for r in entries if r["card"] == code]
        entry_ok = (
            all(r["passed"] for r in group)
            and group[0]["dossier"] is None
            and bool(group[1]["dossier"])
            and bool(group[2]["dossier"])
            and group[1]["dossier"] != group[2]["dossier"]
            and group[0]["permissions"] == group[1]["permissions"] == group[2]["permissions"]
        )
        base = next(c for c in cells if c["card"] == code and c["variant"] == "base")
        values = base["final_metrics"]
        pairs = [(0, 1)] if code == "BC" else [(0, 1), (2, 3)]
        contrasts = [
            contrast(
                values[a] if a < len(values) else {},
                values[b] if b < len(values) else {},
                CHANNELS[code],
            )
            for a, b in pairs
        ]
        s1 = any(all(pair[k]["passed"] for pair in contrasts) for k in CHANNELS[code])
        extra = (
            []
            if code == "BC"
            else [
                contrast(
                    values[a] if a < len(values) else {},
                    values[b] if b < len(values) else {},
                    CHANNELS[code],
                )
                for a, b in [(0, 2), (1, 3)]
            ]
        )
        row = {
            "card": code,
            "entry_passed": entry_ok,
            "runtime_passed": base["runtime_passed"],
            "resources_passed": base["resources"]["passed"],
            "replay_passed": base["replay"]["verified"],
            "response_passed": s1,
            "primary_contrasts": contrasts,
            "secondary_contrasts": extra,
            "base_screen_passed": checks_ok(base) and s1,
            "entry_and_base_passed": entry_ok and checks_ok(base) and s1,
        }
        if code in AXES:
            shift = next(c for c in cells if c["card"] == code and c["variant"] == "shift")
            shifted = shift["final_metrics"]
            world_pairs = [
                contrast(
                    values[i] if i < len(values) else {},
                    shifted[i] if i < len(shifted) else {},
                    CHANNELS[code],
                )
                for i in range(4)
            ]
            row["world_contrasts"] = world_pairs
            row["world_response_passed"] = (
                checks_ok(base)
                and checks_ok(shift)
                and any(sum(p[k]["passed"] for p in world_pairs) >= 2 for k in CHANNELS[code])
            )
        else:
            row["world_response_passed"] = None
            row["world_response_status"] = "mechanism_family_adapter_not_registered"
        if code == "FL":
            feasible = [
                m.get("flow_conversion", -1) >= 0.50
                and m.get("yield", -1) >= 0.10
                and m.get("safety_risk", 1) <= 0.35
                for m in values
            ]
            row["illustrative_feasible_points"] = feasible
            row["illustrative_boundary_covered"] = (
                len(feasible) == 4 and any(feasible) and not all(feasible)
            )
        systems.append(row)
    counts = {
        "entry_planned": 15,
        "entry_attempted": len(entries),
        "entry_constructed": sum(r["passed"] for r in entries),
        "campaigns_planned": 8,
        "campaigns_attempted": len(cells),
        "campaigns_complete": sum(c["runtime_passed"] for c in cells),
        "batches_planned": 30,
        "batches_complete": sum(c["completed_batches"] for c in cells),
        "resource_passes": sum(c["resources"]["passed"] for c in cells),
        "replay_passes": sum(c["replay"]["verified"] for c in cells),
        "recorded_operations": sum(c["recorded_operations"] for c in cells),
        "base_screen_passes": sum(r["base_screen_passed"] for r in systems),
        "entry_and_base_passes": sum(r["entry_and_base_passed"] for r in systems),
        "world_response_passes": sum(r["world_response_passed"] is True for r in systems),
        "world_response_tested": 3,
        "model_calls": 0,
        "retries": 0,
    }
    return {
        "schema_version": "work-ii-new-system-gates-0.1",
        "evidence_mode": "development",
        "experiment_note": NOTE,
        "run_root": root.relative_to(ROOT).as_posix(),
        "status": "fixed_block_closed",
        "elapsed_seconds": elapsed,
        "counts": counts,
        "systems": systems,
        "retained_measurement_diagnostics": retained_diagnostics(root, cells),
        "entry_checks": entries,
        "campaigns": cells,
        "full_science_gate_qualified": False,
        "full_agent_chain_tested": False,
        "judge_tested": False,
        "formal_result": False,
    }


def markdown(report):
    c = report["counts"]
    lines = [
        "# W2-117：五体系首轮 gate 实测",
        "",
        "固定开发块；无模型调用、无重试。完整科学资格与 Agent 后测链尚未通过。",
        "",
        f"耗时 {report['elapsed_seconds'] / 60:.2f} 分钟；"
        f"真实多批campaign {c['campaigns_complete']}/8 完整，"
        f"终检 {c['batches_complete']}/30，记录动作 {c['recorded_operations']}。",
        f"共用账本 {c['resource_passes']}/8，精确重放 {c['replay_passes']}/8；重放不增加独立样本。",
        "",
        f"旧三臂资料入口可构造 {c['entry_constructed']}/15；基础筛查 {c['base_screen_passes']}/5；"
        f"入口与基础筛查合取 {c['entry_and_base_passes']}/5；"
        f"成对世界差异 {c['world_response_passes']}/3。",
        "",
        "这些比例是固定小覆盖的工程/科学必要条件通过率，不是 Agent 成功率或全矩阵资格率。",
        "",
        "| 体系 | 三臂入口 | 基础多批 | 账本 | 重放 | S1公开响应 | 基础合取 | S2世界差异 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    def label(value):
        return "未接入" if value is None else ("通过" if value else "未通过")

    for r in report["systems"]:
        keys = [
            "entry_passed",
            "runtime_passed",
            "resources_passed",
            "replay_passed",
            "response_passed",
            "base_screen_passed",
            "world_response_passed",
        ]
        lines.append(f"| {r['card']} | " + " | ".join(label(r[k]) for k in keys) + " |")
    lines += [
        "",
        "## 每个 campaign 的终态",
        "",
        "| 条件 | 完成批次 | 动作 | 运行秒 | 重放秒 | 失败 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for r in report["campaigns"]:
        lines.append(
            f"| {r['card']}-{r['variant']} | {r['completed_batches']}/{r['planned_batches']} | "
            f"{r['recorded_operations']}/{r['planned_operations']} | "
            f"{r['execution_seconds']:.2f} | "
            f"{r['replay_seconds']:.2f} | {r['failure'] or '无'} |"
        )
    lines += ["", "## 入口失败（全部保留）", ""]
    lines += [
        f"- {r['card']}/{r['arm']}：{r['error']['type']} — {r['error']['message']}"
        for r in report["entry_checks"]
        if not r["passed"]
    ]
    lines += ["", "## 公开终检（顺序对应实验说明中的固定批次）", ""]
    for r in report["campaigns"]:
        keys = CHANNELS[r["card"]]
        lines += [
            f"### {r['card']}-{r['variant']}",
            "",
            "| 批次 | " + " | ".join(keys) + " |",
            "| --- | " + " | ".join("---" for _ in keys) + " |",
        ]
        for i, m in enumerate(r["final_metrics"], 1):
            lines.append(
                f"| {i} | " + " | ".join(f"{m[k]:.6f}" if k in m else "缺失" for k in keys) + " |"
            )
        lines.append("")
    lines += [
        "## 解释边界",
        "",
        "S1要求预定的两对对比在同一主通道均超过3倍合并仪器噪声及最小效应；BC仅一对。S2要求同通道至少2/4条件越阈值。它们不是结构可辨识性证明或正式显著性检验。",
        "旧适配器构造失败说明当前调用路径未接入，不能推断模拟器不能支持该科学任务；"
        "旧nominal dossier可构造也不证明新卡的Aligned内容已科学验证。",
        "G-D仅本块明确；G-S仍缺留出预测/任务可达性与先验内容核验；G-R本轮覆盖真实多批、资源和重放，未覆盖provider→自由K1→Q→K2；G-J未测，G-F不适用，G-C保留全部终态。",
        "RX/BC未接入规律变化接口。PA本轮未独立核验两相质量守恒；FL的示例窗口阈值仅作开发诊断；EQ的confidence不作为Agent置信度。",
        "",
        "[固定说明](../WORK_II_NEW_SYSTEM_GATE_NOTE.md) · "
        "[机器结果](work-ii-new-system-gates-20260916.json)",
        "",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run-root", type=Path, default=ROOT / "runs/development/work-ii-new-system-gates-20260916"
    )
    parser.add_argument("--summarize-only", action="store_true")
    args = parser.parse_args()
    root = args.run_root.resolve()
    if args.summarize_only:
        entries = json.loads((root / "entry_checks.json").read_text(encoding="utf-8"))
        cells = json.loads((root / "cells.json").read_text(encoding="utf-8"))
        elapsed = json.loads((root / "timing.json").read_text(encoding="utf-8"))["elapsed_seconds"]
    else:
        root.mkdir(parents=True, exist_ok=False)
        (root / "experiment_note.md").write_bytes((ROOT / NOTE).read_bytes())
        plans = [
            (code, variant)
            for code in TASKS
            for variant in (["base", "shift"] if code in AXES else ["base"])
        ]
        write(
            root / "block_plan.json",
            {
                "campaigns": [
                    {
                        "card": code,
                        "variant": variant,
                        "batches": recipes(code),
                        "resource_card": resource_card(code).to_dict(),
                    }
                    for code, variant in plans
                ],
                "seed": 0,
                "observation_seed": 1,
            },
        )
        progress = {"stage": "start", "unit": "none", "completed": 0, "total": 8, "operations": 0}
        started = time.monotonic()
        stop = threading.Event()

        def heartbeat():
            while not stop.wait(20):
                seconds = time.monotonic() - started
                complete = progress["completed"]
                rate = complete / seconds
                print(
                    json.dumps(
                        {
                            **progress,
                            "elapsed_s": round(seconds, 1),
                            "campaigns_per_min": round(rate * 60, 3),
                            "eta_s": round((8 - complete) / rate, 1) if rate else None,
                        }
                    ),
                    flush=True,
                )

        thread = threading.Thread(target=heartbeat, daemon=True)
        thread.start()
        try:
            entries = check_entries(root, progress)
            cells = []
            for code, variant in plans:
                cell = execute(root, code, variant, progress)
                cells.append(cell)
                progress["completed"] += 1
                write(root / "cells.json", cells)
                print(
                    json.dumps(
                        {
                            **progress,
                            "completed_batches": cell["completed_batches"],
                            "runtime_passed": cell["runtime_passed"],
                            "failure": cell["failure"],
                        }
                    ),
                    flush=True,
                )
            elapsed = time.monotonic() - started
            write(root / "timing.json", {"elapsed_seconds": elapsed})
        finally:
            stop.set()
            thread.join(timeout=1)
    report = build_report(root, entries, cells, elapsed)
    write(REPORT, report)
    REPORT.with_suffix(".md").write_text(markdown(report), encoding="utf-8")
    print(json.dumps(report["counts"], ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
