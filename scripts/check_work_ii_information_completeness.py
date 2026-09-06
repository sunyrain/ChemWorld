"""Run the fixed W2-87 offline contact calibration and summarize conditional costs."""
# ruff: noqa: RUF001

from __future__ import annotations

import hashlib
import json
import time
from collections import Counter
from pathlib import Path

from chemworld.eval.work_ii_public_partition_reference import (
    PublicContact,
    forward,
    invert_power_exponent,
)
from chemworld.world.phase_kernel import (
    INDEPENDENT_NOMINAL_SOLVENT_EXTRACTANT_PAIR_V1,
    partition_split,
)

ROOT = Path(__file__).resolve().parents[1]
NOTE = "workstreams/flagship_tasks/WORK_II_INFORMATION_COMPLETENESS_EXPERIMENT_NOTE.md"
REPORT = "workstreams/flagship_tasks/reports/work-ii-information-completeness-20260906.json"


def main() -> None:
    target = ROOT / REPORT
    if target.exists() or target.with_suffix(".md").exists():
        raise FileExistsError("W2-87 calibration already exists; preserve its terminal result")
    current_path = ROOT / "configs/current.json"
    current = json.loads(current_path.read_text(encoding="utf-8"))
    source = current["work_ii"]["w2_77_final_diagnostic"]
    protocol = json.loads((ROOT / source["protocol"]).read_text(encoding="utf-8"))
    manifest = json.loads(
        (ROOT / protocol["source_root"] / "input_manifest.json").read_text(encoding="utf-8")
    )
    packets = {}
    for cell in manifest["cells"]:
        packet = cell["public_packet"]
        key = cell["cluster_id"]
        if key in packets and packets[key] != packet:
            raise ValueError("public evidence differs within a source world")
        packets[key] = packet
    if len(packets) != 5:
        raise ValueError("expected all five source public packets")

    def coordinates(packet: dict) -> list[dict]:
        return [
            {k: row[k] for k in ("query_id", "feature_values", "reference_partition_coefficient")}
            for row in packet["evidence"] + packet["scoring_action_queries"]
        ]

    queries = coordinates(next(iter(packets.values())))
    if len(queries) != 16 or len({q["query_id"] for q in queries}) != 16:
        raise ValueError("expected the disjoint 8+8 public coordinates")
    if any(coordinates(packet) != queries for packet in packets.values()):
        raise ValueError("source public coordinate contracts differ")
    rows = []
    kernel_calls = 0
    started = time.perf_counter()
    print("W2-87 kernel calibration: 0/96; no provider calls", flush=True)
    for temperature in (293.15, 303.15):
        for exponent in (1.0, 1.3, 1.75):
            for query in queries:
                controls = query["feature_values"]
                row = {"unit": len(rows) + 1, "temperature_K": temperature, "exponent": exponent}
                row["query_id"] = query["query_id"]
                try:
                    contact = PublicContact(
                        reference_coefficient=query["reference_partition_coefficient"],
                        temperature_K=temperature,
                        duration_s=controls["mix_duration_s"],
                        stirring_speed_rpm=controls["stirring_speed_rpm"],
                        organic_volume_L=controls["extractant_volume_L"],
                        aqueous_volume_L=0.020 + controls["aqueous_phase_volume_L"],
                    )
                    predicted = forward(contact, exponent)
                    kernel_calls += 1
                    actual = partition_split(
                        product_mol=0.02,
                        impurity_mol=0.003,
                        solvent=controls["solvent"],
                        extractant=controls["extractant"],
                        nominal_pair_contract=INDEPENDENT_NOMINAL_SOLVENT_EXTRACTANT_PAIR_V1,
                        temperature_K=temperature,
                        duration_s=contact.duration_s,
                        stirring_speed_rpm=contact.stirring_speed_rpm,
                        organic_volume_L=contact.organic_volume_L,
                        aqueous_volume_L=contact.aqueous_volume_L,
                        coefficient_exponent=exponent,
                    )
                    actual_values = {
                        "coefficient": actual["partition_coefficient"],
                        "organic_fraction": actual["organic_product_mol"] / 0.02,
                        "aqueous_fraction": actual["aqueous_product_mol"] / 0.02,
                    }
                    error = max(abs(predicted[k] - actual_values[k]) for k in predicted)
                    estimate = invert_power_exponent(contact, actual_values["organic_fraction"])
                    row.update(
                        actual=actual_values,
                        predicted=predicted,
                        max_absolute_error=error,
                        inferred_exponent=estimate,
                        exponent_error=abs(estimate - exponent),
                        status="passed"
                        if error <= 1e-10 and abs(estimate - exponent) <= 1e-8
                        else "failed",
                    )
                except Exception as exc:
                    row.update(status="failed", failure=f"{type(exc).__name__}: {exc}")
                rows.append(row)
            elapsed = time.perf_counter() - started
            rate = len(rows) / max(elapsed, 1e-9)
            print(
                f"W2-87 kernel {len(rows)}/96; {rate:.1f} units/s; "
                f"ETA {(96 - len(rows)) / rate:.1f}s; failures "
                f"{sum(r['status'] == 'failed' for r in rows)}",
                flush=True,
            )
    old = json.loads((ROOT / source["report"]).read_text(encoding="utf-8"))
    resources = [r for r in old["resources"] if r["tool"] == "on"]
    costs = []
    for resource in resources:
        seconds = resource["wall_seconds"] / resource["attempted_sessions"]
        costs.append(
            {
                "model": resource["model"],
                "source_sessions": resource["attempted_sessions"],
                "seconds_per_session": seconds,
                "proposed_development_sessions": 6,
                "proposed_formal_sessions": 60,
                "historical_rate_development_hours": 6 * seconds / 3600,
                "historical_rate_formal_hours": 60 * seconds / 3600,
            }
        )
    counts = dict(Counter(r["status"] for r in rows))
    report = {
        "schema_version": "work-ii-information-completeness-feasibility-1",
        "experiment_note": NOTE,
        "status": "development_kernel_calibration_completed",
        "formal_result": False,
        "source_binding": "work_ii.w2_77_final_diagnostic",
        "public_packets_checked": len(packets),
        "public_coordinates": len(queries),
        "coordinate_contracts": queries,
        "calibration_inputs": {
            "temperatures_K": [293.15, 303.15],
            "exponents": [1.0, 1.3, 1.75],
            "product_mol": 0.02,
            "impurity_mol": 0.003,
            "additional_aqueous_volume_L": 0.020,
            "coefficient_multiplier": 1.0,
            "phase_volume_multiplier": 1.0,
        },
        "artificial_calibration_contexts": 2,
        "scheduled": 96,
        "attempted": len(rows),
        "counts": counts,
        "failures": [r for r in rows if r["status"] == "failed"],
        "rows": rows,
        "kernel_calls": kernel_calls,
        "complete_physical_experiments": 0,
        "exact_replays": 0,
        "additional_independent_worlds": 0,
        "provider_calls": 0,
        "elapsed_seconds": time.perf_counter() - started,
        "participant_same_information_identifiability_established": False,
        "formal_agent_block_ready": False,
        "remaining_dependencies": [
            "Complete phase-removal, sampling, normalization, score and noise contract",
            "Public-only family/parameter fit and sealed held-out prediction calibration",
            "Ten new world coverage design and evidence/replay generation",
            "Twelve-session same-harness development and budget calibration",
        ],
        "proposed_matrix": {
            "formal_worlds": 10,
            "models": 2,
            "priors": 3,
            "information_conditions": 2,
            "repeats_per_cell": 1,
            "development_sessions": 12,
            "formal_sessions": 120,
            "formal_turns": 240,
            "recovery_primary_sessions": 80,
            "aligned_retention_sessions": 40,
            "status": "conditional_design_not_frozen",
        },
        "historical_rate_costs": costs,
        "interpretation": (
            "This is privileged implementation validation of explicit contact equations and "
            "noiseless, power-family-conditional inversion. It is neither historical B3 replay, "
            "full endpoint calibration, family identification nor new independent-world evidence. "
            "Cost extrapolations use existing tool-on sessions, not new measured throughput."
        ),
    }
    target.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    lines = [
        "# 公开信息补全：离线可行性与剩余矩阵",
        "",
        f"固定kernel校准：{len(rows)}/96尝试，{counts.get('passed', 0)}通过，"
        f"{counts.get('failed', 0)}失败；耗时{report['elapsed_seconds']:.2f}秒。",
        "5/5原公开包查询合同一致；16个输入坐标×2个人工上下文×3指数。",
        "新增独立world、完整物理实验、replay和provider调用均0。",
        "",
        "该结果只校验接触器公开方程及已知幂律族下的无噪声反解；最终观测映射、噪声、",
        "公开信息下的族选择与留出预测仍未资格，正式Agent块不可启动。旧B3不升级为可识别。",
        "",
        "| 模型 | 历史工具开放会话 | 秒/会话 | 新6开发会话折算小时 | 新60正式会话折算小时 |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for cost in costs:
        lines.append(
            f"| {cost['model']} | {cost['source_sessions']} | {cost['seconds_per_session']:.2f} | "
            f"{cost['historical_rate_development_hours']:.2f} | "
            f"{cost['historical_rate_formal_hours']:.2f} |"
        )
    lines += [
        "",
        "规模方案：10新world×3先验×2信息条件×2模型×1次＝120正式会话/240轮，开发另12。",
        "恢复主分析80会话，正确先验保持40；比5world×2次保留同样会话量并增加world覆盖。",
        "当前剩余：完整参考合同与留出校准→新world证据→12开发→120正式→图文整合。",
        "运行时长仅为历史工具开放组的外推；新披露长度、工具使用和服务状态可能改变吞吐。",
        "当前没有新Agent调用，不存在运行中倒计时；后续预算在开发完成后冻结。",
        "",
        "全部失败及96单位的读数、偏差见同名JSON；不以好结果替换。",
    ]
    target.with_suffix(".md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    current["work_ii"]["w2_87_information_completeness"] = {
        "report": REPORT,
        "report_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "experiment_note": NOTE,
        "status": report["status"],
        "formal_result": False,
        "formal_agent_block_ready": False,
        "kernel_scheduled": 96,
        "kernel_passed": counts.get("passed", 0),
        "provider_calls": 0,
    }
    current_path.write_text(
        json.dumps(current, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
    )
    print(target.with_suffix(".md").read_text(encoding="utf-8"), flush=True)


if __name__ == "__main__":
    main()
