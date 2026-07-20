"""Run the four exploratory DeepSeek flagship mechanism diagnostics."""

from __future__ import annotations

import argparse
import copy
import json
import os
import sys
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from chemworld.agents.diagnostic_live_llm import (  # noqa: E402
    MechanismDiagnosticLiveLLMAgent,
)
from chemworld.eval.flagship_diagnostics import (  # noqa: E402
    DEFAULT_PROTOCOL_PATH,
    ContinuingHistoryAgent,
    ContinuingPublicViewAgent,
    FeedbackCondition,
    build_flagship_diagnostic_report,
    load_flagship_diagnostic_protocol,
    render_flagship_diagnostic_markdown,
    run_two_phase_campaign,
)
from chemworld.eval.formal_operation import make_frozen_operation_agent  # noqa: E402
from chemworld.eval.runner import make_agent  # noqa: E402
from chemworld.providers.deepseek import DeepSeekClient  # noqa: E402


def _progress(payload: Mapping[str, Any]) -> None:
    print(json.dumps(dict(payload), sort_keys=True), flush=True)


def _deepseek_agent(task_card: Mapping[str, Any], model: Mapping[str, Any]) -> Any:
    client = DeepSeekClient(
        model=str(model["model_id"]),
        thinking=bool(model["thinking"]),
        max_attempts=2,
        timeout_s=120.0,
    )
    return MechanismDiagnosticLiveLLMAgent(
        client,
        role_id="deepseek_flagship_mechanism_diagnostic",
        spectrum_disclosure=str(model["spectrum_disclosure"]),
        response_max_tokens=int(model["response_max_tokens"]),
        fail_fast_on_unbillable_provider_failure=True,
        mechanism_candidates=tuple(str(item) for item in task_card["mechanism_candidates"]),
    )


def _method_adapter(
    method_id: str,
    *,
    task_id: str,
    task_card: Mapping[str, Any],
    model: Mapping[str, Any],
    feedback_condition: str = "true_feedback",
) -> Any:
    critical = str(task_card["critical_diagnostic_instrument"])
    if method_id == "deepseek_v4_flash":
        return ContinuingPublicViewAgent(
            _deepseek_agent(task_card, model),
            method_id=method_id,
            feedback_condition=cast(FeedbackCondition, feedback_condition),
            critical_instrument=critical,
        )
    if method_id == "rule_based":
        return ContinuingPublicViewAgent(
            make_frozen_operation_agent("rule_based"),
            method_id=method_id,
            feedback_condition="true_feedback",
            critical_instrument=critical,
        )
    return ContinuingHistoryAgent(make_agent(method_id), method_id=method_id)


def _run_or_load(
    *,
    summary_path: Path,
    factory: Callable[[], dict[str, Any]],
    resume: bool,
) -> dict[str, Any]:
    if resume and summary_path.is_file():
        payload = json.loads(summary_path.read_text(encoding="utf-8"))
        _progress({"status": "reused", "campaign_id": payload.get("campaign_id")})
        return payload
    payload = factory()
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _progress(
        {
            "status": "completed",
            "campaign_id": payload.get("campaign_id"),
            "iid_complete": payload.get("iid", {}).get("complete_experiment_count"),
            "shifted_complete": payload.get("shifted", {}).get("complete_experiment_count"),
        }
    )
    return payload


def run_protocol(
    protocol: Mapping[str, Any],
    *,
    resume: bool,
    sections: set[str],
) -> dict[str, Any]:
    runtime_root = ROOT / str(protocol["artifacts"]["runtime_root"])
    summary_root = runtime_root / "campaigns"
    trajectory_root = runtime_root / "trajectories"
    seed = int(protocol["seed"])
    pre = int(protocol["pre_change_experiments"])
    post = int(protocol["post_change_experiments"])
    model = protocol["deepseek"]
    campaigns: list[dict[str, Any]] = []
    ranking_deepseek: dict[str, dict[str, Any]] = {}

    if "ranking" in sections:
        for task_id, task_card in protocol["tasks"].items():
            shift = task_card["mechanism_shift"]
            for method_id in protocol["ranking_methods"]:
                campaign_id = f"ranking--{task_id}--{method_id}--seed{seed}"
                _progress(
                    {
                        "status": "starting",
                        "experiment": "ranking_shift",
                        "campaign_id": campaign_id,
                    }
                )

                def run(
                    task_id: str = task_id,
                    task_card: Mapping[str, Any] = task_card,
                    method_id: str = method_id,
                    campaign_id: str = campaign_id,
                    shift: Mapping[str, Any] = shift,
                ) -> dict[str, Any]:
                    result = run_two_phase_campaign(
                        task_id=task_id,
                        adapter=_method_adapter(
                            method_id,
                            task_id=task_id,
                            task_card=task_card,
                            model=model,
                        ),
                        seed=seed,
                        pre_change_experiments=pre,
                        post_change_experiments=post,
                        shifted_interventions=shift["interventions"],
                        output_root=trajectory_root,
                        campaign_id=campaign_id,
                        closeout_headroom_per_experiment=int(
                            protocol["closeout_headroom_per_experiment"]
                        ),
                    )
                    result.update(
                        {
                            "experiment_id": "ranking_shift",
                            "feedback_condition": "true_feedback",
                            "shifted_truth_id": shift["truth_id"],
                            "formal_result": False,
                        }
                    )
                    return result

                result = _run_or_load(
                    summary_path=summary_root / f"{campaign_id}.json",
                    factory=run,
                    resume=resume,
                )
                campaigns.append(result)
                if method_id == "deepseek_v4_flash":
                    ranking_deepseek[task_id] = result

    if "feedback" in sections:
        for task_id, task_card in protocol["tasks"].items():
            shift = task_card["mechanism_shift"]
            true_result = ranking_deepseek.get(task_id)
            if true_result is None:
                ranking_path = summary_root / (
                    f"ranking--{task_id}--deepseek_v4_flash--seed{seed}.json"
                )
                if ranking_path.is_file():
                    true_result = json.loads(ranking_path.read_text(encoding="utf-8"))
            if true_result is not None:
                alias = copy.deepcopy(true_result)
                alias.update(
                    {
                        "experiment_id": "feedback_ablation",
                        "feedback_condition": "true_feedback",
                        "resource_reused_from_campaign": true_result["campaign_id"],
                    }
                )
                campaigns.append(alias)
            for condition in protocol["feedback_conditions"]:
                if condition == "true_feedback":
                    continue
                campaign_id = f"feedback--{task_id}--{condition}--seed{seed}"
                _progress(
                    {
                        "status": "starting",
                        "experiment": "feedback_ablation",
                        "campaign_id": campaign_id,
                    }
                )

                def run_feedback(
                    task_id: str = task_id,
                    task_card: Mapping[str, Any] = task_card,
                    condition: str = condition,
                    campaign_id: str = campaign_id,
                    shift: Mapping[str, Any] = shift,
                ) -> dict[str, Any]:
                    result = run_two_phase_campaign(
                        task_id=task_id,
                        adapter=_method_adapter(
                            "deepseek_v4_flash",
                            task_id=task_id,
                            task_card=task_card,
                            model=model,
                            feedback_condition=condition,
                        ),
                        seed=seed,
                        pre_change_experiments=pre,
                        post_change_experiments=post,
                        shifted_interventions=shift["interventions"],
                        output_root=trajectory_root,
                        campaign_id=campaign_id,
                        closeout_headroom_per_experiment=int(
                            protocol["closeout_headroom_per_experiment"]
                        ),
                    )
                    result.update(
                        {
                            "experiment_id": "feedback_ablation",
                            "feedback_condition": condition,
                            "shifted_truth_id": shift["truth_id"],
                            "formal_result": False,
                        }
                    )
                    return result

                campaigns.append(
                    _run_or_load(
                        summary_path=summary_root / f"{campaign_id}.json",
                        factory=run_feedback,
                        resume=resume,
                    )
                )

    if "counterfactual" in sections:
        for task_id, task_card in protocol["tasks"].items():
            shift = task_card["material_law_swap"]
            campaign_id = f"material-law--{task_id}--deepseek--seed{seed}"
            _progress(
                {
                    "status": "starting",
                    "experiment": "material_law_swap",
                    "campaign_id": campaign_id,
                }
            )

            def run_counterfactual(
                task_id: str = task_id,
                task_card: Mapping[str, Any] = task_card,
                campaign_id: str = campaign_id,
                shift: Mapping[str, Any] = shift,
            ) -> dict[str, Any]:
                result = run_two_phase_campaign(
                    task_id=task_id,
                    adapter=_method_adapter(
                        "deepseek_v4_flash",
                        task_id=task_id,
                        task_card=task_card,
                        model=model,
                    ),
                    seed=seed,
                    pre_change_experiments=pre,
                    post_change_experiments=post,
                    shifted_interventions=shift["interventions"],
                    output_root=trajectory_root,
                    campaign_id=campaign_id,
                    closeout_headroom_per_experiment=int(
                        protocol["closeout_headroom_per_experiment"]
                    ),
                )
                result.update(
                    {
                        "experiment_id": "material_law_swap",
                        "feedback_condition": "true_feedback",
                        "shifted_truth_id": shift["truth_id"],
                        "formal_result": False,
                    }
                )
                return result

            campaigns.append(
                _run_or_load(
                    summary_path=summary_root / f"{campaign_id}.json",
                    factory=run_counterfactual,
                    resume=resume,
                )
            )

    index_path = ROOT / str(protocol["artifacts"]["campaign_index"])
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(
        json.dumps(campaigns, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    report = build_flagship_diagnostic_report(protocol, campaigns)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL_PATH)
    parser.add_argument("--api-key-file", type=Path)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument(
        "--section",
        action="append",
        choices=("ranking", "feedback", "counterfactual"),
        help="repeat to run selected sections; default runs all",
    )
    args = parser.parse_args()
    if args.api_key_file is not None and not os.environ.get("DEEPSEEK_API_KEY"):
        os.environ["DEEPSEEK_API_KEY"] = args.api_key_file.read_text(encoding="utf-8").strip()
    if not os.environ.get("DEEPSEEK_API_KEY"):
        parser.error("set DEEPSEEK_API_KEY or pass --api-key-file")
    protocol = load_flagship_diagnostic_protocol(args.protocol)
    sections = set(args.section or ("ranking", "feedback", "counterfactual"))
    report = run_protocol(protocol, resume=args.resume, sections=sections)
    report_path = ROOT / str(protocol["artifacts"]["json_report"])
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    markdown_path = ROOT / str(protocol["artifacts"]["markdown_report"])
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(
        render_flagship_diagnostic_markdown(report),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": report["status"],
                "report": str(report_path),
                "markdown_report": str(markdown_path),
                "benchmark_claim_allowed": False,
                "publication_ready": False,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["status"] == "exploratory_complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
