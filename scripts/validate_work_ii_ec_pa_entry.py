"""Fixed, provider-free EC prediction and PA prior-entry checks (W2-131)."""
# ruff: noqa: RUF001

from __future__ import annotations

import argparse
import json
import math
import tempfile
import time
from pathlib import Path

from scripts import run_work_ii_ec_dual_goal_trial as ec
from scripts import run_work_ii_pa_single_trial as pa
from scripts.run_work_ii_astra_single_trial import write

from chemworld.agents.experiment_codex_mcp import ChemWorldMCPServer
from chemworld.data.logging import load_jsonl
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent


def material_reply(task_info, arm):
    """Use PAAgent's real reset/publication and MCP reader, without launching a provider."""
    with tempfile.TemporaryDirectory(prefix="chemworld-research-") as temporary:
        home = Path(temporary)
        agent = pa.PAAgent(
            arm=arm,
            batches=1,
            home_root=home,
            output=home,
            workspace=home / "laboratory",
            role_id="free_research",
        )
        try:
            agent.reset(task_info, 0)
            agent.workspace.start_session(
                session_id="reference-check", response_timeout_s=10, session_scope="campaign"
            )
            response = ChemWorldMCPServer(agent.workspace.root)._call_tool(
                "material_information", {}
            )
            if response.get("isError"):
                raise RuntimeError("material_information returned a tool error")
            return json.loads(response["content"][0]["text"])
        finally:
            agent.close()


def anonymous(payload):
    serialized = json.dumps(payload).lower()
    forbidden = (
        '"display_name": "water"',
        "ethanol",
        "acetonitrile",
        "toluene",
        "cas_number",
        '"formula"',
        '"arm"',
        "anonymous_misindexed_properties",
    )
    return not any(token in serialized for token in forbidden)


def run(root, report):
    root.mkdir(parents=True, exist_ok=False)
    report.mkdir(parents=True, exist_ok=True)
    query_set = ec.queries()
    pa_actions = pa.queries()[4]["actions"]
    write(
        root / "design.json",
        {
            "note": "WORK_II_EC_PA_EXECUTION_UPDATE_NOTE.md",
            "ec_query_version": ec.QUERY_VERSION,
            "ec_queries": query_set,
            "pa_arms": list(pa.ARMS),
            "pa_actions": pa_actions,
            "planned_physical_batches": 15,
            "planned_operations": 99,
            "planned_replay_batches": 15,
            "planned_replay_operations": 99,
            "provider_calls": 0,
        },
    )
    started = time.monotonic()
    result = {
        "development_only": True,
        "formal_result": False,
        "provider_calls": 0,
        "retries": 0,
        "planned_physical_batches": 15,
        "planned_operations": 99,
        "planned_replay_batches": 15,
        "planned_replay_operations": 99,
        "ec_query_version": ec.QUERY_VERSION,
        "ec": [],
        "pa": [],
    }

    def save():
        rows = result["ec"] + result["pa"]
        result.update(
            attempted_units=len(rows),
            passed_units=sum(r["passed"] for r in rows),
            completed_batches=sum(r["completed_batches"] for r in rows),
            operations=sum(r["operations"] for r in rows),
            replay_verified_units=sum(
                r.get("exact_replay", {}).get("verified") is True for r in rows
            ),
            replay_checked_operations=sum(
                r.get("exact_replay", {}).get("checked_steps", 0) for r in rows
            ),
            elapsed_s=time.monotonic() - started,
        )
        write(root / "summary.json", result)
        write(report / "summary.json", result)
        lines = [
            "# EC预测题与PA先验入口验证",
            "",
            "development；固定参考，无模型来源。",
            "",
            f"完成{result['completed_batches']}/15批、{result['operations']}/99操作；"
            f"通过{result['passed_units']}/15单元，精确重放通过{result['replay_verified_units']}/15；"
            f"耗时{result['elapsed_s']:.2f}秒。",
            "",
            f"重放另计15计划批，已核对{result['replay_checked_operations']}/99操作；"
            "0 provider调用、0重试；失败和未执行保留分母。",
            "",
            "| EC题 | 条件组 | 电位域 | 产率 | 综合分 | 通过 |",
            "| --- | --- | --- | ---: | ---: | --- |",
        ]
        for r in result["ec"]:
            m = r.get("metrics", {})
            lines.append(
                f"| {r['query_id']} | {r['context']} | {r['potential_domain']} | "
                f"{m.get('selective_product_yield', '缺失')} | {m.get('score', '缺失')} | "
                f"{r['passed']} |"
            )
        if result.get("ec_domains"):
            lines += [
                "",
                "| 电位域 | 题数 | 产率范围 | 产率低于0.02 |",
                "| --- | ---: | --- | ---: |",
            ]
            for domain, values in result["ec_domains"].items():
                lines.append(
                    f"| {domain} | {values['n']} | "
                    f"{values['yield_min']:.5f}–{values['yield_max']:.5f} | "
                    f"{values['yield_below_0_02']} |"
                )
            lines += [
                "",
                "成对差为正电位减负电位，仅作描述；每种条件只有一次固定参考，"
                "不是显著性检验或完整机理辨识。",
                "",
                "| 条件组 | 产率差 | 综合分差 |",
                "| --- | ---: | ---: |",
            ]
            for context, values in result.get("ec_paired_differences", {}).items():
                lines.append(
                    f"| {context} | {values['selective_product_yield']:.5f} | "
                    f"{values['score']:.5f} |"
                )
        lines += [
            "",
            "| PA条件 | 完成批数 | 操作数 | 匿名工具回复 | 通过 |",
            "| --- | ---: | ---: | --- | --- |",
        ]
        for r in result["pa"]:
            lines.append(
                f"| {r['arm']} | {r['completed_batches']} | {r['operations']} | "
                f"{r.get('anonymous_reply')} | {r['passed']} |"
            )
        lines += [
            "",
            "```json",
            json.dumps(result.get("cross_checks", {}), ensure_ascii=False, indent=2),
            "```",
            "",
            "参考合法性、匿名送达与物理不变性不代表Agent学会规律，亦不代表正式三臂已执行。"
            "EC题目在本次执行前固定，低响应或零差异也保留；没有按输出重新选题。",
            "",
        ]
        (report / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")

    save()
    for query in query_set:
        print(f"EC {len(result['ec'])}/12; {query['query_id']}", flush=True)
        raw = ec.reference_run(root / query["query_id"], query["actions"])
        metrics = raw["batches"][0]["metrics"] if raw["batches"] else {}
        row = {
            **query,
            "completed_batches": len(raw["batches"]),
            "operations": raw["operation_attempts"],
            "metrics": metrics,
            "exact_replay": raw["exact_replay"],
            "failure": raw["failure"],
            "rollbacks": raw["rollbacks"],
        }
        row["passed"] = (
            len(raw["batches"]) == 1
            and row["operations"] == len(query["actions"])
            and not raw["failure"]
            and not raw["rollbacks"]
            and raw["exact_replay"].get("verified") is True
            and all(math.isfinite(metrics.get(k, float("nan"))) for k in ec.METRICS)
        )
        result["ec"].append(row)
        save()

    replies, physical_values = {}, []
    for arm in pa.ARMS:
        print(f"PA {len(result['pa'])}/3; {arm}", flush=True)
        folder = root / arm
        folder.mkdir()
        agent = _FrozenTruthReplayAgent(pa_actions)
        truths = []
        failure = None
        payload = None
        try:
            pa.physics(agent, folder / "trajectory.jsonl", arm=arm, batches=1, truth=truths)
            payload = material_reply(agent.task_info, arm)
            write(folder / "material-reply.json", payload)
        except Exception as exc:
            failure = {"type": type(exc).__name__, "message": str(exc)}
        path = folder / "trajectory.jsonl"
        records = load_jsonl(path) if path.exists() else []
        replay = ec.replay_with_progress(records, arm)
        measured = [r for r in pa.observations(records) if r["instrument"] == "hplc"]
        physical_values.append(
            [
                {
                    "action": r["action"],
                    "measurement": r.get("processed_estimate"),
                    "observed_mask": r.get("observed_mask"),
                }
                for r in records
            ]
        )
        if payload:
            replies[arm] = payload
        row = {
            "arm": arm,
            "completed_batches": len(ec.summaries(records)),
            "operations": len(records),
            "exact_replay": replay,
            "failure": failure,
            "material_reply": payload,
            "anonymous_reply": bool(payload and anonymous(payload)),
            "hplc": measured,
            "truth": truths,
        }
        row["passed"] = (
            not failure
            and row["completed_batches"] == 1
            and row["operations"] == len(pa_actions)
            and row["anonymous_reply"]
            and replay.get("verified") is True
            and all(r.get("transaction_status") == "committed" for r in records)
            and len(truths) == len(measured) == 1
            and abs(sum(truths[0][k] for k in pa.METRICS) - 1) <= 1e-8
            and all(
                math.isfinite(measured[0]["values"].get(k, float("nan")))
                and measured[0]["observed_mask"].get(k) is True
                for k in pa.METRICS
            )
        )
        result["pa"].append(row)
        save()

    check = {
        "pa_actions_and_observations_same_across_arms": all(
            v == physical_values[0] for v in physical_values
        ),
        "all_material_replies_delivered": len(replies) == 3,
    }
    if len(replies) == 3:
        dossier = {a: replies[a]["material_information"]["dossier"] for a in pa.ARMS}
        a, m = dossier["Aligned"]["choices"], dossier["MisIndexed"]["choices"]
        check.update(
            opaque_without_dossier=dossier["Opaque"] is None,
            solvent_dossier_unchanged=a["solvent"] == m["solvent"],
            extractant_properties_transposed=[r["nominal_properties"] for r in m["extractant"]]
            == [a["extractant"][i]["nominal_properties"] for i in (3, 1, 2, 0)],
            public_catalog_same=all(
                replies[arm]["material_catalog"] == replies["Opaque"]["material_catalog"]
                for arm in pa.ARMS
            ),
        )
    result["cross_checks"] = check
    result["ec_domains"] = {
        domain: {
            "n": len(rows),
            "yield_min": min(r["metrics"]["selective_product_yield"] for r in rows),
            "yield_max": max(r["metrics"]["selective_product_yield"] for r in rows),
            "yield_below_0_02": sum(r["metrics"]["selective_product_yield"] < 0.02 for r in rows),
        }
        for domain in ("negative", "positive")
        if (rows := [r for r in result["ec"] if r["potential_domain"] == domain and r["passed"]])
    }
    result["ec_paired_differences"] = {
        negative["context"]: {
            metric: positive["metrics"][metric] - negative["metrics"][metric]
            for metric in ec.METRICS
        }
        for negative, positive in zip(result["ec"][::2], result["ec"][1::2], strict=True)
        if negative["passed"] and positive["passed"]
    }
    result["passed"] = all(r["passed"] for r in result["ec"] + result["pa"]) and all(check.values())
    save()
    print(
        json.dumps(
            {
                k: result[k]
                for k in ("passed", "passed_units", "completed_batches", "operations", "elapsed_s")
            }
        ),
        flush=True,
    )
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.output.resolve(), args.report.resolve())
    raise SystemExit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
