#!/usr/bin/env python3
"""Build the sanitized anonymous supplement for the prior-discovery paper."""

from __future__ import annotations

import ast
import copy
import csv
import hashlib
import json
import re
import tempfile
import zipfile
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.agents.interactive_codex_experiment import _campaign_system_prompt
from chemworld.eval.work_ii_evidence_to_action_runtime import (
    RECIPIENT_SYSTEM_PROMPT,
    terminal_output_schema,
    yoked_snapshot_output_schema,
)
from chemworld.eval.work_ii_factorial import CONDITIONS, MODELS, TASKS
from chemworld.eval.work_ii_factorial_replication import CONTRASTS
from chemworld.eval.work_ii_reviewer_followup import (
    B3_METRIC_IDS,
    b3_output_schema,
)
from chemworld.eval.work_ii_study_b import prediction_output_schema

ROOT = Path(__file__).resolve().parents[2]
SUPPLEMENT_README = ROOT / "paper/iclr2027/supplement/README.md"
PUBLICATION_REPORT = (
    ROOT / "workstreams/flagship_tasks/reports/work-ii-w2-64-publication-reanalysis-v0.1.json"
)
ACTION_REPORT = (
    ROOT / "workstreams/flagship_tasks/reports/"
    "work-ii-w2-61-cross-model-action-aligned-causal-extension-v0.1.json"
)
DEEPSEEK_C2 = (
    ROOT / "workstreams/flagship_tasks/reports/"
    "work-ii-deepseek-c2-current-composite-evaluation-v0.2.json"
)
GPT_C2 = (
    ROOT / "workstreams/flagship_tasks/reports/"
    "work-ii-w2-62-codex-c2-current-composite-evaluation-v0.1.json"
)
B3_CROSS_MODEL = (
    ROOT / "workstreams/flagship_tasks/reports/work-ii-w2-63-b3-failure-aware-cross-model-v0.1.json"
)
DEEPSEEK_C2_PROTOCOL = ROOT / "configs/benchmark/work_ii_deepseek_c2_prospective_v0.2.json"
GPT_C2_PROTOCOL = ROOT / "configs/benchmark/work_ii_c2_gpt56_sol_medium_replication_v0.1.json"
B3_PROTOCOL = ROOT / "configs/benchmark/work_ii_as_study_b3_identifiable_law_action_v0.2.json"
B2_EXPRESSION_ANALYZER = ROOT / "scripts/analyze_work_ii_study_b2_results.py"
FIGURE_SOURCE_DIR = ROOT / "paper/figures/prior-discovery/source_data"
EXPORT_DIR = ROOT / "paper/exports/prior-discovery-iclr2027"
OUTPUT_ZIP = EXPORT_DIR / "prior-discovery-iclr2027-supplement.zip"

IDENTITY_STRINGS = (
    "Jiangjie Qiu",
    "Yijun Li",
    "Yaotian Yang",
    "Honghao Chen",
    "Wentao Li",
    "Xiaonan Wang",
    "wangxiaonan@tsinghua.edu.cn",
    "Tsinghua University",
    "Beijing Key Laboratory of Artificial Intelligence",
    "State Key Laboratory of Chemical Engineering",
)
INTERNAL_STAGE_NAMES = {
    "W2-50": "longitudinal-open-action",
    "W2-51": "96-query-oracle-qualification",
    "W2-52": "320-query-oracle-adaptation",
    "W2-53": "rank-action-gate-diagnostic",
    "W2-61": "four-condition-action-successor",
    "W2-62": "cross-model-C2-replication",
    "W2-63": "cross-model-B3-replication",
    "W2-64": "publication-reanalysis",
}
FORBIDDEN_TEXT_PATTERNS = {
    "absolute_windows_path": re.compile(r"(?i)(?:^|[\s\"'])(?:[A-Z]:[\\/])"),
    "absolute_unix_user_path": re.compile(r"(?i)(?:/home/|/Users/|/root/)[^\s\"']*"),
    "local_run_root": re.compile(r"(?i)(?:^|[\s\"'/])runs[\\/]"),
    "credential_file": re.compile(r"(?i)(?:api\.md|key2\.md|\.env(?:\W|$))"),
    "secret_field": re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|bearer[_-]?token)"),
    "provider_identity": re.compile(r"(?i)(?:thread[_-]?id|request[_-]?id|session[_-]?id)"),
    "email_address": re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def _jsonl_bytes(rows: Sequence[Mapping[str, Any]]) -> bytes:
    return (
        "".join(
            json.dumps(row, ensure_ascii=False, allow_nan=False, sort_keys=True) + "\n"
            for row in rows
        )
    ).encode("utf-8")


def _replace_public_terms(value: str) -> str:
    result = value
    for internal, public in INTERNAL_STAGE_NAMES.items():
        stage_number = internal.removeprefix("W2-")
        result = re.sub(
            rf"(?i)\bW2[-_]{stage_number}\b",
            public,
            result,
        )
    result = re.sub(r"(?i)\bW2[-_]\d+\b", "internal-stage", result)
    result = re.sub(r"\bCodex\b", "GPT-5.6-sol", result)
    result = re.sub(r"\bcodex\b", "gpt_5_6_sol", result)
    return result


def _sanitize_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for raw_key, raw_value in value.items():
            key = str(raw_key)
            lowered = key.lower()
            if lowered in {
                "path",
                "root",
                "output_root",
                "source_root",
                "api_key_file",
                "thread_id",
                "request_id",
                "session_id",
                "donor_source",
                "original_summary",
                "recovery_summary",
            }:
                continue
            public_key = {
                "codex": "gpt_5_6_sol",
                "w2_50": "longitudinal_open_action",
            }.get(key, _replace_public_terms(key))
            result[public_key] = _sanitize_value(raw_value)
        return result
    if isinstance(value, list):
        return [_sanitize_value(item) for item in value]
    if isinstance(value, str):
        return _replace_public_terms(value)
    return value


def _public_source_hashes(source_bindings: Sequence[Mapping[str, Any]]) -> list[dict[str, str]]:
    roles = (
        "four_condition_action_report",
        "deepseek_c2_evaluation",
        "gpt_c2_evaluation",
        "cross_model_c2_summary",
        "cross_model_b3_summary",
        "b2_deepseek_high_summary",
        "b2_gpt_medium_summary",
        "b2_deepseek_low_summary",
        "b2_participant_visible_identifiability_audit",
        "b2_expression_coding_source",
        "longitudinal_open_action_summary",
        "longitudinal_open_action_manifest",
        "electrochemical_runtime_contract",
        "crystallization_runtime_contract",
        "safety_runtime_contract",
    )
    if len(source_bindings) != len(roles):
        raise ValueError("publication source-binding denominator changed")
    return [
        {"role": role, "sha256": str(binding["sha256"])}
        for role, binding in zip(roles, source_bindings, strict=True)
    ]


def _publication_projection(report: Mapping[str, Any]) -> dict[str, Any]:
    projected = _sanitize_value(copy.deepcopy(dict(report)))
    projected.pop("source_bindings", None)
    projected["source_hashes"] = _public_source_hashes(report["source_bindings"])
    projected["schema_version"] = "chemworld-anonymous-publication-data-0.1"
    projected.pop("summary_sha256", None)
    projected["projection_sha256"] = hashlib.sha256(
        json.dumps(
            projected,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    return projected


def _c2_rows(path: Path, *, model: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    report = _load(path)
    rows = []
    for raw in report["cell_rows"]:
        row = _sanitize_value(raw)
        row["model"] = model
        rows.append(row)
    failures = []
    for raw in report["all_retained_failures"]:
        row = _sanitize_value(raw)
        row["model"] = model
        failures.append(row)
    if len(rows) != 135:
        raise ValueError(f"{model} C2 row denominator differs from 135")
    return rows, failures


def _protocol_projection() -> dict[str, Any]:
    deepseek = _load(DEEPSEEK_C2_PROTOCOL)
    gpt = _load(GPT_C2_PROTOCOL)
    b3 = _load(B3_PROTOCOL)
    return {
        "schema_version": "chemworld-anonymous-protocol-projection-0.1",
        "models": {
            "deepseek_v4_flash": {"reasoning_effort": "high"},
            "gpt_5_6_sol": {"reasoning_effort": "medium"},
        },
        "c2": {
            "prior_arms": deepseek["prior_arms"],
            "deepseek_public_blocks": deepseek["public_blocks"],
            "gpt_public_blocks": gpt["public_blocks"],
            "scheduled_sessions_per_model": 135,
            "independent_task_world_clusters_per_model": 45,
            "failure_handling": deepseek["execution"],
            "private_confirmation_included": False,
        },
        "matched_evidence": {
            "conditions": ["pre_evidence", "matched_counterevidence"],
            "scoring_queries_are_disjoint_from_evidence": True,
            "participant_physical_experiments": 0,
            "two_turn_same_session": True,
        },
        "identifiable_law_action": {
            "arms": b3["arms"],
            "metric_ids": b3["metric_ids"],
            "candidate_grid": b3["candidate_grid"],
            "qualification": b3["qualification"],
            "execution": {
                key: value
                for key, value in b3["execution"].items()
                if key not in {"canary_sessions"}
            },
            "scheduled_sessions_per_model": 30,
            "participant_physical_experiments": 0,
        },
        "four_condition_action_successor": {
            "conditions": [
                "no_evidence",
                "yoked_evidence",
                "autonomous_exploration",
                "learned_law_only",
            ],
            "scheduled_strata_per_model": 45,
            "scheduled_condition_slots_per_model": 180,
            "independent_task_world_clusters_per_model": 15,
            "primary_estimand": "all-scheduled failure-aware strategy estimand",
            "missing_terminal_normalized_regret": 1.0,
            "donor_eligible_results": "availability-conditioned sensitivity only",
            "oracle_condition_included": False,
            "evidence_role": "development_strategy_comparison",
        },
    }


def _function_source(path: Path, names: set[str]) -> str:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    tree = ast.parse(text)
    selected: list[str] = []
    observed: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            if node.end_lineno is None:
                raise ValueError(f"cannot determine source extent for {node.name}")
            selected.extend(lines[node.lineno - 1 : node.end_lineno])
            selected.append("")
            observed.add(node.name)
    if observed != names:
        raise ValueError(
            f"prompt functions changed: expected {sorted(names)}, got {sorted(observed)}"
        )
    return "\n".join(selected).rstrip() + "\n"


def _prompt_templates() -> dict[str, Any]:
    return {
        "schema_version": "chemworld-anonymous-prompt-templates-0.1",
        "longitudinal_campaign_system_prompt": _campaign_system_prompt(
            terminal_action_readout=True,
            terminal_prediction_mode="ranking_only",
        ),
        "four_condition_recipient_system_prompt": RECIPIENT_SYSTEM_PROMPT,
        "dynamic_input_rule": (
            "The accompanying function-source file is verbatim. Dynamic JSON payloads contain "
            "only participant-visible task, prior, evidence, and candidate fields."
        ),
    }


def _schemas() -> dict[str, Any]:
    generic_scoring_queries = [
        {"query_id": f"query_{index:02d}", "metric_ids": ["metric_a", "metric_b"]}
        for index in range(1, 9)
    ]
    b3_queries = [
        {"query_id": f"query_{index:02d}", "metric_ids": list(B3_METRIC_IDS)}
        for index in range(1, 9)
    ]
    query_ids = [row["query_id"] for row in generic_scoring_queries]
    query_metric_contract = {row["query_id"]: row["metric_ids"] for row in generic_scoring_queries}
    return {
        "schema_version": "chemworld-anonymous-response-schemas-0.1",
        "matched_evidence_pre": prediction_output_schema(generic_scoring_queries, stage="pre"),
        "matched_evidence_post": prediction_output_schema(generic_scoring_queries, stage="post"),
        "identifiable_law_pre": b3_output_schema(b3_queries, stage="pre"),
        "identifiable_law_post": b3_output_schema(b3_queries, stage="post"),
        "four_condition_terminal": terminal_output_schema(query_ids),
        "four_condition_yoked_checkpoint": yoked_snapshot_output_schema(
            stage="final",
            query_metric_contract=query_metric_contract,
            allowed_feature_ids=["feature_a", "feature_b", "category"],
            allowed_metric_ids=["metric_a", "metric_b"],
            allowed_prior_fields=["prior_field"],
            evidence_catalog=[f"evidence_{index:02d}" for index in range(1, 13)],
            nominal_information_available=True,
        ),
        "executable_law_contract": {
            "schema_version": "chemworld-work-ii-law-summary-0.1",
            "basis": [
                "linear",
                "quadratic",
                "cubic",
                "interaction",
                "categorical_level",
                "conditional_linear",
                "conditional_quadratic",
                "conditional_cubic",
            ],
            "links": ["identity", "logistic"],
            "maximum_terms_per_metric_law": 64,
            "required_fields": [
                "schema_version",
                "summary_id",
                "feature_ids",
                "metric_laws",
                "evidence_ids",
                "applicability",
                "limitations",
                "confidence",
            ],
        },
    }


def _provenance_timeline() -> dict[str, Any]:
    return {
        "schema_version": "chemworld-anonymous-recovery-provenance-0.1",
        "rules": {
            "scientific_failures_retained": True,
            "affected_platform_block_restarted_from_first_unit": True,
            "outcome_based_replacement_forbidden": True,
            "superseded_records_not_in_current_estimate": True,
        },
        "current_surfaces": [
            {
                "surface": "DeepSeek C2",
                "incident": "one 15-cell shard was affected by runtime/evaluator defects",
                "recovery": "whole shard restarted; evaluator rerun over the full composite",
                "current_inclusion": "120 unaffected cells plus one 15-cell replacement shard",
            },
            {
                "surface": "GPT-5.6-sol C2",
                "incident": "no inherited stopped cell",
                "recovery": "new 135-cell block from cell one",
                "current_inclusion": "all 135 scheduled outcomes",
            },
            {
                "surface": "DeepSeek identifiable-law assay",
                "incident": "historical three-cell canary failed the participant schema",
                "recovery": "independent 30-cell successor from cell one",
                "current_inclusion": "17 complete cells plus 13 retained schema failures",
            },
            {
                "surface": "four-condition yoked evidence",
                "incident": "duplicate field deletion caused a recipient KeyError",
                "recovery": "entire yoked condition restarted from its first admitted unit",
                "current_inclusion": (
                    "recovered condition only; original failures retained in timeline"
                ),
            },
        ],
        "oracle_qualification": [
            {
                "version": "original_96_query",
                "role": "fresh formal qualification",
                "observed_units": 8,
                "pass_count": 7,
                "first_failure_spearman": 0.738095,
                "first_failure_top1": False,
                "provider_calls": 0,
                "stop_rule_applied": True,
            },
            {
                "version": "adaptive_v0_2",
                "role": "fresh development qualification",
                "first_failure_spearman": 0.785714,
                "provider_calls": 0,
                "stop_rule_applied": True,
            },
            {
                "version": "adaptive_v0_3",
                "role": "fresh development qualification",
                "first_failure_spearman": 0.595238,
                "provider_calls": 0,
                "stop_rule_applied": True,
            },
            {
                "version": "adaptive_v0_4",
                "role": "fresh development qualification after exposed construction checks",
                "first_failure_spearman": 0.785714,
                "provider_calls": 0,
                "stop_rule_applied": True,
            },
            {
                "version": "expanded_320_query",
                "role": "fresh qualification after seven exposed construction units",
                "observed_units": 1,
                "pass_count": 0,
                "first_failure_spearman": 0.714286,
                "first_failure_top1": True,
                "first_failure_normalized_regret": 0.0,
                "provider_calls": 0,
                "stop_rule_applied": True,
            },
        ],
        "interpretation": (
            "Version-specific attempts are not pooled into a success rate and do not revise "
            "the frozen rank threshold or any historical stop decision."
        ),
    }


VERIFY_SCRIPT = r"""#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
import hashlib
import importlib.util
import json
import math
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
for row in manifest["files"]:
    path = ROOT / row["path"]
    assert path.is_file(), row["path"]
    assert path.stat().st_size == row["bytes"], row["path"]
    assert sha256(path) == row["sha256"], row["path"]

report = json.loads((ROOT / "data/publication_report.json").read_text(encoding="utf-8"))
models = report["action_extension"]["models"]
deepseek = models["deepseek"]["primary_all_scheduled"]["contrasts"]
gpt = models["gpt_5_6_sol"]["primary_all_scheduled"]["contrasts"]


def jsonl(path):
    return [
        json.loads(line)
        for line in (ROOT / path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def close(left, right):
    assert math.isclose(float(left), float(right), rel_tol=0.0, abs_tol=1e-12), (
        left,
        right,
    )


def contrast(rows, name):
    return next(row for row in rows if row["contrast"] == name)


action_rows = jsonl("data/four_condition_scheduled_rows.jsonl")
assert len(action_rows) == 360
contrast_conditions = {
    "autonomous_exploration_minus_no_evidence": (
        "autonomous_exploration",
        "no_evidence",
    ),
    "yoked_evidence_minus_no_evidence": ("yoked_evidence", "no_evidence"),
    "learned_law_only_minus_no_evidence": ("learned_law_only", "no_evidence"),
    "autonomous_exploration_minus_yoked_evidence": (
        "autonomous_exploration",
        "yoked_evidence",
    ),
}
effect = "mean_failure_aware_normalized_regret_difference"
for model_name, published in (("deepseek", deepseek), ("gpt_5_6_sol", gpt)):
    model_rows = [row for row in action_rows if row["participant"] == model_name]
    assert len(model_rows) == 180
    by_condition = {}
    for row in model_rows:
        by_condition.setdefault(row["condition"], {})[row["stratum_id"]] = row
    assert set(by_condition) == {
        "autonomous_exploration",
        "no_evidence",
        "yoked_evidence",
        "learned_law_only",
    }
    assert all(len(rows) == 45 for rows in by_condition.values())
    for name, (left_name, right_name) in contrast_conditions.items():
        left = by_condition[left_name]
        right = by_condition[right_name]
        assert set(left) == set(right)
        replayed = mean(
            float(left[stratum]["failure_aware_normalized_regret"])
            - float(right[stratum]["failure_aware_normalized_regret"])
            for stratum in sorted(left)
        )
        close(replayed, contrast(published, name)[effect])

decision = report["longitudinal_open_action"]["decision_aligned_law_action"]["overall"]
assert decision["law_evaluated_count"] == 45
assert decision["law_implied_top1_count"] == 0
assert decision["participant_top1_count"] == 11
assert decision["law_implied_top1_followed_count"] == 12
assert decision["law_action_agreement_evaluable_count"] == 42

c2_rows = jsonl("data/c2_cell_records.jsonl")
assert len(c2_rows) == 270
c2 = report["c2_denominators"]["models"]
fields = (
    "completed_cell_count",
    "checkpoint_scored_count",
    "law_evaluated_count",
    "blind_gain_evaluable_count",
)
for model_name in ("deepseek", "gpt_5_6_sol"):
    rows = [row for row in c2_rows if row["model"] == model_name]
    assert len(rows) == 135
    replayed = {
        "completed_cell_count": sum(bool(row["qualification_passed"]) for row in rows),
        "checkpoint_scored_count": sum(
            int(row["checkpoint_error"]["scored_snapshot_count"]) for row in rows
        ),
        "law_evaluated_count": sum(
            row["law_summary"].get("status") == "evaluated" for row in rows
        ),
        "blind_gain_evaluable_count": sum(
            row["blind"].get("recommendation_gain_over_incumbent") is not None
            for row in rows
        ),
    }
    assert tuple(replayed[field] for field in fields) == tuple(
        c2[model_name][field] for field in fields
    )

b3_rows = jsonl("data/b3_cell_records.jsonl")
assert len(b3_rows) == 60
b3 = report["b3_denominators"]["models"]
eligibility_by_coordinate = {}
for row in b3_rows:
    coordinate = (row["cluster_id"], row["arm"], row["replicate_index"])
    eligibility = row["action_opportunity_eligible"]
    if eligibility is not None:
        prior = eligibility_by_coordinate.setdefault(coordinate, bool(eligibility))
        assert prior == bool(eligibility)
assert sum(eligibility_by_coordinate.values()) == 18
for model_name in ("deepseek", "gpt_5_6_sol"):
    rows = [row for row in b3_rows if row["participant"] == model_name]
    assert len(rows) == 30
    completed = [row for row in rows if row["completed"]]
    eligible = [row for row in completed if row["action_opportunity_eligible"]]
    published = b3[model_name]
    failures = Counter(
        str(row["failure_classification"])
        for row in rows
        if not row["completed"]
    )
    assert published["completed_cell_count"] == len(completed)
    assert published["failed_cell_count"] == len(rows) - len(completed)
    assert published["failure_classification_counts"] == dict(sorted(failures.items()))
    assert published["joint_law_recovery_count"] == sum(
        bool(row["joint_family_exponent_recovery"]) for row in rows
    )
    assert published["top1_count"] == sum(bool(row["top1_selected"]) for row in rows)
    close(
        published["mean_failure_aware_regret"],
        mean(float(row["normalized_regret"]) for row in rows),
    )
    close(
        published["completed_mean_post_mae"],
        mean(float(row["post_error"]) for row in completed),
    )
    assert published["useful_gain_completed_opportunity"] == {
        "count": sum(float(row["selected_action_gain"]) >= 0.02 for row in eligible),
        "denominator": len(eligible),
    }
    assert published["useful_gain_scheduled_opportunity"]["denominator"] == 18

assert b3["deepseek"]["useful_gain_completed_opportunity"] == {"count": 0, "denominator": 13}
assert b3["gpt_5_6_sol"]["useful_gain_completed_opportunity"] == {"count": 0, "denominator": 18}
assert b3["deepseek"]["useful_gain_scheduled_opportunity"]["denominator"] == 18
assert b3["gpt_5_6_sol"]["useful_gain_scheduled_opportunity"]["denominator"] == 18

b2 = report["b2_expression_and_identifiability"]
assert len(b2["public_summary_rows"]) == 45
identifiability = b2["participant_visible_identifiability"]
assert identifiability["decision"]["structural_family_identification_supported"] is False
assert identifiability["exact_alias"]["present"] is True
assert identifiability["positive_control"]["readout_positive_control_passed"] is False
assert round(identifiability["constant_endpoint_baseline"]["mean_scoring_error"], 5) == 0.00649
expected_exact = {
    "deepseek_v4_flash_high": (1, 0),
    "gpt_5_6_sol_medium": (0, 0),
    "deepseek_v4_flash_low": (2, 0),
}
for configuration, (aligned, misspecified) in expected_exact.items():
    audit = b2["configuration_summaries"][configuration]["public_expression_audit_by_arm"]
    assert audit["aligned_nominal"]["exact_1_75_power_law_recovery_count"] == aligned
    assert audit["misindexed_nominal"]["exact_1_75_power_law_recovery_count"] == misspecified

coding_path = ROOT / "methods/b2_expression_coding.py"
spec = importlib.util.spec_from_file_location("b2_expression_coding", coding_path)
assert spec is not None and spec.loader is not None
coding = importlib.util.module_from_spec(spec)
spec.loader.exec_module(coding)
rows = [
    json.loads(line)
    for line in (ROOT / "data/b2_public_summary_rows.jsonl")
    .read_text(encoding="utf-8")
    .splitlines()
    if line.strip()
]
assert len(rows) == 45
for configuration in expected_exact:
    observed = coding.audit_flat_public_rows(
        [row for row in rows if row["configuration"] == configuration]
    )
    expected = b2["configuration_summaries"][configuration][
        "public_expression_audit_by_arm"
    ]
    assert observed["by_arm"] == expected

boundaries = report["claim_boundaries"]
assert boundaries["matched_evidence_conditional_post_packet_response_supported"] is True
assert boundaries["matched_evidence_pure_packet_effect_supported"] is False
assert boundaries["b2_structural_family_identification_supported"] is False

if (ROOT / "verify_m1.py").exists():
    import runpy
    runpy.run_path(str(ROOT / "verify_m1.py"))
if (ROOT / "verify_m3.py").exists():
    import runpy
    runpy.run_path(str(ROOT / "verify_m3.py"))

print(f"verified {len(manifest['files'])} files and all publication invariants")
"""


def _sanitize_csv(content: str) -> str:
    return _replace_public_terms(content)


def _assert_anonymous(path: str, content: bytes) -> None:
    if b"\x00" in content:
        return
    text = content.decode("utf-8")
    lower = text.lower()
    identity_hits = [item for item in IDENTITY_STRINGS if item.lower() in lower]
    if identity_hits:
        raise ValueError(f"{path} contains identity strings: {identity_hits}")
    pattern_hits = [
        name for name, pattern in FORBIDDEN_TEXT_PATTERNS.items() if pattern.search(text)
    ]
    if pattern_hits:
        raise ValueError(f"{path} contains forbidden patterns: {pattern_hits}")
    internal_ids = sorted(set(re.findall(r"(?i)\bW2[-_]\d+\b", text)))
    if internal_ids:
        raise ValueError(f"{path} contains internal stage identifiers: {internal_ids}")


def _write_zip(files: Mapping[str, bytes]) -> None:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        prefix="prior-discovery-supplement-",
        suffix=".zip",
        dir=EXPORT_DIR,
        delete=False,
    ) as temporary:
        temporary_path = Path(temporary.name)
    try:
        with zipfile.ZipFile(
            temporary_path,
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        ) as archive:
            for path, content in sorted(files.items()):
                info = zipfile.ZipInfo(path, date_time=(2026, 8, 25, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, content)
        temporary_path.replace(OUTPUT_ZIP)
    finally:
        temporary_path.unlink(missing_ok=True)


def _m1_files() -> dict[str, bytes]:
    current = _load(ROOT / "configs/current.json")
    binding = current["work_ii"].get("w2_72_m1_replication")
    if not binding or not binding.get("formal_result"):
        return {}
    path = ROOT / binding["report"]
    if _sha256_bytes(path.read_bytes()) != binding["report_sha256"]:
        raise ValueError("M1 current report binding differs from the retained report")
    report = _load(path)
    protocol = _load(ROOT / report["protocol"])
    protocol["providers"] = {
        model: {key: provider[key] for key in ("model", "reasoning_effort")}
        for model, provider in protocol["providers"].items()
    }
    projected = {
        key: value
        for key, value in report.items()
        if key not in {"source_commit", "execution_surface", "experiment_note", "protocol"}
    }
    projected["source_hashes"] = [
        {"role": "independent_world_factorial_report", "sha256": binding["report_sha256"]}
    ]
    primitive_source = (
        "from __future__ import annotations\n"
        "import json\nimport math\nfrom copy import deepcopy\n"
        "from collections.abc import Mapping, Sequence\nfrom typing import Any\n"
        "import numpy as np\n\nBASIS = ['1', 'x', 'y', 'x*x', 'x*y', 'y*y']\n\n"
        + _function_source(
            ROOT / "src/chemworld/eval/work_ii_factorial.py",
            {
                "public_packet",
                "normalized_design",
                "design_matrix",
                "fit_public_law",
                "output_schema",
                "validate_payload",
                "maximize",
                "participant_prompt",
                "nearest_public_choice",
                "score_slots",
            },
        )
    )
    analysis_source = (
        "from __future__ import annotations\n"
        "from collections import defaultdict\nfrom typing import Any\nimport numpy as np\n\n"
        + f"TASKS = {TASKS!r}\nMODELS = {MODELS!r}\nCONDITIONS = {CONDITIONS!r}\n"
        + f"CONTRASTS = {CONTRASTS!r}\n\n"
        + _function_source(
            ROOT / "src/chemworld/eval/work_ii_factorial_replication.py",
            {"source_schedule", "bootstrap_interval", "summarize_factorial"},
        )
    )
    return {
        "data/m1_replication.json": _json_bytes(_sanitize_value(projected)),
        "protocols/m1_replication.json": _json_bytes(_sanitize_value(protocol)),
        "methods/m1_public_primitives.py": primitive_source.encode("utf-8"),
        "methods/m1_analysis.py": analysis_source.encode("utf-8"),
        "verify_m1.py": (ROOT / "paper/iclr2027/supplement/verify_m1.py").read_bytes(),
    }


def _m3_files() -> dict[str, bytes]:
    current = _load(ROOT / "configs/current.json")
    binding = current["work_ii"].get("w2_69_m3_portability")
    if not binding or not binding.get("formal_result"):
        return {}
    path = ROOT / binding["report"]
    if _sha256_bytes(path.read_bytes()) != binding["report_sha256"]:
        raise ValueError("M3 current binding differs from the retained report")
    report = _load(path)
    projected = {
        key: value
        for key, value in report.items()
        if key not in {"source_commit", "execution_surface", "source_binding", "experiment_note"}
    }
    projected["scientific_source_data"] = {
        key: value for key, value in report["scientific_source_data"].items() if key != "protocol"
    }
    projected["source_hashes"] = [
        {"role": "context_portability_report", "sha256": binding["report_sha256"]},
        {"role": "reused_m1_sources", "sha256": report["source_binding"]["report_sha256"]},
    ]
    protocol = {
        key: value
        for key, value in report["scientific_source_data"]["protocol"].items()
        if key != "source_binding"
    }
    concrete = _load(ROOT / binding["protocol"])
    protocol["providers"] = {
        model: {key: provider[key] for key in ("model", "reasoning_effort")}
        for model, provider in concrete["providers"].items()
    }
    information = (
        "from __future__ import annotations\nimport json\nimport math\nfrom copy import deepcopy\n"
        "from collections.abc import Sequence\nfrom typing import Any\n"
        "BASIS = ['1', 'x', 'y', 'x*x', 'x*y', 'y*y']\n"
        "CONDITIONS = ('none', 'raw', 'L', 'F')\n\n"
        + _function_source(ROOT / "src/chemworld/eval/work_ii_factorial.py", {"validate_payload"})
        + "\n"
        + _function_source(
            ROOT / "src/chemworld/eval/work_ii_m3_portability.py",
            {"recipient_input", "recipient_prompt"},
        )
    )
    return {
        "data/m3_portability.json": _json_bytes(_sanitize_value(projected)),
        "protocols/m3_portability.json": _json_bytes(_sanitize_value(protocol)),
        "methods/m3_information.py": information.encode("utf-8"),
        "verify_m3.py": (ROOT / "paper/iclr2027/supplement/verify_m3.py").read_bytes(),
    }


def build() -> dict[str, Any]:
    publication = _load(PUBLICATION_REPORT)
    action = _load(ACTION_REPORT)
    b3_cross_model = _load(B3_CROSS_MODEL)
    projected = _publication_projection(publication)
    b2 = projected["b2_expression_and_identifiability"]
    deepseek_rows, deepseek_failures = _c2_rows(DEEPSEEK_C2, model="deepseek")
    gpt_rows, gpt_failures = _c2_rows(GPT_C2, model="gpt_5_6_sol")

    files: dict[str, bytes] = {
        "README.md": SUPPLEMENT_README.read_bytes(),
        "data/publication_report.json": _json_bytes(projected),
        "data/four_condition_scheduled_rows.jsonl": _jsonl_bytes(
            _sanitize_value(action["condition_rows"])
        ),
        "data/four_condition_failure_records.jsonl": _jsonl_bytes(
            _sanitize_value(action["failure_records_primary_360_slots"])
        ),
        "data/c2_cell_records.jsonl": _jsonl_bytes([*deepseek_rows, *gpt_rows]),
        "data/c2_failure_records.jsonl": _jsonl_bytes([*deepseek_failures, *gpt_failures]),
        "data/b3_cell_records.jsonl": _jsonl_bytes(
            _sanitize_value(
                [
                    {**row, "participant": model}
                    for model, model_rows in b3_cross_model["cell_rows_by_model"].items()
                    for row in model_rows
                ]
            )
        ),
        "data/b2_public_summary_rows.jsonl": _jsonl_bytes(b2["public_summary_rows"]),
        "data/b2_identifiability_audit.json": _json_bytes(
            b2["participant_visible_identifiability"]
        ),
        "data/b2_configuration_summaries.json": _json_bytes(b2["configuration_summaries"]),
        "methods/b2_expression_coding.py": (
            "from collections.abc import Mapping, Sequence\n"
            "from typing import Any\n\n"
            'ARMS = ("opaque", "aligned_nominal", "misindexed_nominal")\n\n'
            + _function_source(
                B2_EXPRESSION_ANALYZER,
                {"_public_text", "_public_summary_audit"},
            )
            + "\n\ndef audit_flat_public_rows(\n"
            + "    rows: Sequence[Mapping[str, Any]],\n"
            + ") -> dict[str, Any]:\n"
            + "    normalized = [\n"
            + "        {\n"
            + '            "arm": row["arm"],\n'
            + '            "world_seed": row["world_index"],\n'
            + '            "post_prediction": {\n'
            + '                "model_summary": row["model_summary"],\n'
            + '                "evidence_assessment": row["evidence_assessment"],\n'
            + "            },\n"
            + "        }\n"
            + "        for row in rows\n"
            + "    ]\n"
            + "    audit = _public_summary_audit(normalized)\n"
            + '    audit["by_arm"] = {\n'
            + "        arm: {\n"
            + "            key: value\n"
            + "            for key, value in arm_audit.items()\n"
            + '            if key != "world_rows"\n'
            + "        }\n"
            + '        for arm, arm_audit in audit["by_arm"].items()\n'
            + "    }\n"
            + "    return audit\n"
        ).encode("utf-8"),
        "protocols/public_protocols.json": _json_bytes(_sanitize_value(_protocol_projection())),
        "prompts/prompt_templates.json": _json_bytes(_prompt_templates()),
        "prompts/prompt_function_sources.py": (
            _function_source(
                ROOT / "scripts/run_work_ii_study_b.py",
                {"_initial_prompt", "_evidence_prompt"},
            )
            + "\n"
            + _function_source(
                ROOT / "scripts/run_work_ii_reviewer_followups.py",
                {"_b3_initial_prompt", "_b3_evidence_prompt"},
            )
        ).encode("utf-8"),
        "schemas/response_schemas.json": _json_bytes(_schemas()),
        "provenance/recovery_and_oracle_timeline.json": _json_bytes(_provenance_timeline()),
        "verify_supplement.py": VERIFY_SCRIPT.encode("utf-8"),
    }
    files.update(_m1_files())
    files.update(_m3_files())
    for path in sorted(FIGURE_SOURCE_DIR.glob("*.csv")):
        content = _sanitize_csv(path.read_text(encoding="utf-8"))
        list(csv.reader(content.splitlines()))
        files[f"data/figure_source_data/{path.name}"] = content.encode("utf-8")

    for path, content in files.items():
        _assert_anonymous(path, content)
    manifest = {
        "schema_version": "chemworld-anonymous-supplement-manifest-0.1",
        "evidence_role": "anonymous_publication_projection",
        "provider_calls": 0,
        "physics_executions": 0,
        "files": [
            {"path": path, "bytes": len(content), "sha256": _sha256_bytes(content)}
            for path, content in sorted(files.items())
        ],
        "claim_boundaries": projected["claim_boundaries"],
    }
    files["manifest.json"] = _json_bytes(manifest)
    _assert_anonymous("manifest.json", files["manifest.json"])
    _write_zip(files)
    return {
        "status": "anonymous_supplement_built",
        "file_count": len(files),
        "output": OUTPUT_ZIP.relative_to(ROOT).as_posix(),
        "bytes": OUTPUT_ZIP.stat().st_size,
        "sha256": hashlib.sha256(OUTPUT_ZIP.read_bytes()).hexdigest(),
    }


def main() -> int:
    print(json.dumps(build(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
