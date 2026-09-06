"""Describe all existing B3 public packets without fitting against private truth."""
# ruff: noqa: RUF001

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
METRICS = ("product_in_organic", "product_in_aqueous", "phase_ratio", "score")
NOTE = "workstreams/flagship_tasks/WORK_II_PUBLIC_INFORMATION_VISUALIZATION_NOTE.md"
REPORT = "workstreams/flagship_tasks/reports/work-ii-public-information-20260906.json"


def analyze(packets: list[dict]) -> dict:
    rows, failures, contracts = [], [], []
    for world, packet in enumerate(packets, 1):
        evidence = packet.get("evidence", [])
        contracts.append(
            {
                "world": world,
                "packet_fields": sorted(packet),
                "candidate_formulas": packet.get("candidate_mechanism_families", []),
                "evidence_rows": len(evidence),
                "reference_coefficients_present": all(
                    "reference_partition_coefficient" in row for row in evidence
                ),
                "explicit_process_factor_definition": "process_factor_definition" in packet,
                "explicit_observation_equations": "observation_equations" in packet,
                "explicit_noise_model": "noise_model" in packet,
            }
        )
        for index in range(8):
            for metric in METRICS:
                try:
                    item = evidence[index]
                    reference = item["reference_linear_observations"][metric]
                    target = item["target_observations"][metric]
                    rows.append(
                        {
                            "world": world,
                            "evidence_index": index + 1,
                            "metric": metric,
                            "reference": reference,
                            "target": target,
                            "difference": target - reference,
                        }
                    )
                except (KeyError, IndexError, TypeError) as exc:
                    failures.append(
                        {
                            "world": world,
                            "evidence_index": index + 1,
                            "metric": metric,
                            "error": type(exc).__name__,
                        }
                    )
    summaries = []
    for world in [None, *range(1, len(packets) + 1)]:
        for metric in METRICS:
            selected = [
                r for r in rows if r["metric"] == metric and (world is None or r["world"] == world)
            ]
            differences = [abs(r["difference"]) for r in selected]
            summaries.append(
                {
                    "world": world,
                    "metric": metric,
                    "scheduled": 8 * (len(packets) if world is None else 1),
                    "completed": len(selected),
                    "mean_absolute_difference": mean(differences) if differences else None,
                    "max_absolute_difference": max(differences) if differences else None,
                    "exact_equal_count": differences.count(0),
                }
            )
    return {
        "schema_version": "work-ii-public-information-1",
        "experiment_note": NOTE,
        "analysis_type": "posthoc_public_packet_description",
        "formal_qualification": False,
        "worlds": len(packets),
        "additional_independent_worlds": 0,
        "scheduled_pairs": len(packets) * 8,
        "scheduled_metric_pairs": len(packets) * 32,
        "completed_metric_pairs": len(rows),
        "failures": failures,
        "provider_calls": 0,
        "new_physical_executions": 0,
        "contract_inventory": contracts,
        "summaries": summaries,
        "rows": rows,
        "interpretation": (
            "The published candidate equations refer to an effective coefficient and a process "
            "factor, but the packet supplies no complete observation mapping or noise model. "
            "Public-only structural identifiability is not established. This inventory does not "
            "prove that the implemented simulator is unidentifiable, and paired differences are "
            "neither a signal-to-noise estimate nor a held-out predictive baseline."
        ),
    }


def main() -> None:
    current_path = ROOT / "configs/current.json"
    current = json.loads(current_path.read_text(encoding="utf-8"))
    binding = current["work_ii"]["w2_77_final_diagnostic"]
    protocol = json.loads((ROOT / binding["protocol"]).read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / protocol["source_root"] / "input_manifest.json").read_text())
    packets = {}
    for cell in manifest["cells"]:
        key, packet = cell["cluster_id"], cell["public_packet"]
        if key in packets and packets[key] != packet:
            raise ValueError("Public packet differs within an existing world")
        packets[key] = packet
    if len(packets) != 5:
        raise ValueError("Expected all five original worlds")
    report = analyze(list(packets.values()))
    target = ROOT / REPORT
    target.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    lines = [
        "# B3公开信息复核",
        "",
        "事后描述性再分析；5个既有世界、40对证据、160个metric对。",
        "不调用provider或私有模拟器，不增加独立样本。",
        "",
        "| 观测量 | 完成/计划 | 完全相同 | 平均绝对差 | 最大绝对差 |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for r in report["summaries"][:4]:
        lines.append(
            f"| {r['metric']} | {r['completed']}/{r['scheduled']} | "
            f"{r['exact_equal_count']} | {r['mean_absolute_difference']:.8f} | "
            f"{r['max_absolute_difference']:.8f} |"
        )
    lines += [
        "",
        "五份公开包给出候选系数公式和参考系数，但没有完整的过程因子定义、",
        "从有效系数到各观测量的方程或噪声模型。同信息参考恢复路径仍未建立。",
        "这不证明真实模拟器不可识别；配对差不是信噪比，也不是未见候选预测基线。",
        "保留F2数值/结构输出的条件性分离，不能升级为信息充分时的内部能力故障。",
        "",
        f"失败：{len(report['failures'])}；全部行与逐world摘要见同名JSON。",
    ]
    target.with_suffix(".md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    current["work_ii"]["w2_79_public_information"] = {
        "report": REPORT,
        "report_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "experiment_note": NOTE,
        "status": "posthoc_description_completed",
        "worlds": 5,
        "additional_independent_worlds": 0,
    }
    current_path.write_text(
        json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(
        f"Public packets 5/5; metric pairs {len(report['rows'])}/160; "
        f"failures {len(report['failures'])}; ETA 0s",
        flush=True,
    )
    print(target.with_suffix(".md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
