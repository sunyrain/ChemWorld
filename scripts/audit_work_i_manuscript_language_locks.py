"""Audit Work I manuscript figure, counting, sensitivity, and language locks."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT_PATH = Path("paper/experimental_intelligence_v1_manuscript.md")
STORY_PATH = Path("workstreams/arxiv_v1/story/work-i-story-architecture-v0.1.md")
G2_COMPARISON_PATH = Path("workstreams/arxiv_v1/reports/g2-agent-system-comparison-v0.1.json")
FIGURE_SYSTEM_PATH = Path("paper/figures/experimental-intelligence-v1/figure-system-v0.1.json")
FIGURE_6_MANIFEST_PATH = Path(
    "paper/figures/experimental-intelligence-v1/publication/"
    "figure-6-fresh-trajectories.manifest.json"
)
REPORT_JSON_PATH = Path(
    "workstreams/arxiv_v1/story/work-i-manuscript-language-lock-audit-v0.1.json"
)
REPORT_MD_PATH = Path("workstreams/arxiv_v1/story/work-i-manuscript-language-lock-audit-v0.1.md")

FIGURE_REFERENCE_RE = re.compile(r"\b(?:Fig\.|Figure)\s+([1-6])\b", re.IGNORECASE)
EXPECTED_FIGURE_ORDER = [1, 2, 3, 4, 5, 6]


class ManuscriptLanguageLockError(RuntimeError):
    """Raised when a frozen evidence or narrative contract fails closed."""


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ManuscriptLanguageLockError(f"cannot read JSON object: {path}") from exc
    if not isinstance(payload, dict):
        raise ManuscriptLanguageLockError(f"JSON root must be an object: {path}")
    return payload


def _mapping(payload: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = payload.get(key)
    if not isinstance(value, Mapping):
        raise ManuscriptLanguageLockError(f"{key} must be an object")
    return value


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise ManuscriptLanguageLockError(f"cannot read bound file: {path}") from exc
    return digest.hexdigest()


def _canonical_sha256(payload: Any, hash_field: str | None = None) -> str:
    unhashed = deepcopy(payload)
    if hash_field is not None:
        if not isinstance(unhashed, dict):
            raise ManuscriptLanguageLockError("self-hashed payload must be an object")
        unhashed.pop(hash_field, None)
    return hashlib.sha256(
        json.dumps(
            unhashed,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def receipt_sha256(payload: Mapping[str, Any]) -> str:
    """Return the audit digest excluding its embedded self-hash."""

    return _canonical_sha256(payload, "receipt_sha256")


def _validate_self_hash(payload: Mapping[str, Any], field: str, label: str) -> None:
    if payload.get(field) != _canonical_sha256(payload, field):
        raise ManuscriptLanguageLockError(f"{label} self-hash mismatch")


def _line_hits(lines: list[str], pattern: re.Pattern[str]) -> list[dict[str, Any]]:
    return [
        {"line": number, "text": line.strip()}
        for number, line in enumerate(lines, start=1)
        if pattern.search(line)
    ]


def _first_figure_references(lines: list[str]) -> tuple[list[int], list[dict[str, Any]]]:
    first_by_figure: dict[int, dict[str, Any]] = {}
    for number, line in enumerate(lines, start=1):
        for match in FIGURE_REFERENCE_RE.finditer(line):
            figure = int(match.group(1))
            first_by_figure.setdefault(
                figure,
                {"figure": figure, "line": number, "text": line.strip()},
            )
    rows = [
        first_by_figure.get(figure, {"figure": figure, "line": None, "text": None})
        for figure in EXPECTED_FIGURE_ORDER
    ]
    observed = [
        int(row["figure"])
        for row in sorted(
            (row for row in rows if row["line"] is not None),
            key=lambda row: int(row["line"]),
        )
    ]
    return observed, rows


def _validate_story_contract(text: str) -> None:
    normalized = " ".join(text.split())
    required = (
        "Figures are first referenced in numeric order.",
        "120 closed lifecycles: 84 final assays and 36 explicit discards",
        "distinct complete agent systems",
        "2/8 best-versus-raw-terminal sign discordance",
        "6/8 mixed classification as threshold-sensitive supporting evidence",
        "two fresh-session worlds were deliberately selected",
        "not pooled into a population-level model comparison",
    )
    missing = [phrase for phrase in required if phrase not in normalized]
    if missing:
        raise ManuscriptLanguageLockError(f"story contract changed: {missing}")


def _validate_g2_evidence(payload: Mapping[str, Any]) -> dict[str, Any]:
    _validate_self_hash(payload, "comparison_sha256", "G2 comparison")
    systems = _mapping(payload, "systems")
    codex = _mapping(systems, "codex_sol_medium_mcp")
    deepseek = _mapping(systems, "deepseek_v4_flash_direct")
    expected = {
        "codex": {"closed": 60, "assays": 60, "discards": 0},
        "deepseek": {"closed": 60, "assays": 24, "discards": 36},
    }

    def count(row: Mapping[str, Any], key: str) -> int:
        value = row.get(key)
        if not isinstance(value, int) or isinstance(value, bool):
            raise ManuscriptLanguageLockError(f"G2 count is not an integer: {key}")
        return value

    observed: dict[str, dict[str, int]] = {
        "codex": {
            "closed": count(codex, "closed_batch_count"),
            "assays": count(codex, "final_assay_count"),
            "discards": count(codex, "discarded_batch_count"),
        },
        "deepseek": {
            "closed": count(deepseek, "closed_batch_count"),
            "assays": count(deepseek, "final_assay_count"),
            "discards": count(deepseek, "discarded_batch_count"),
        },
    }
    if (
        payload.get("schema_version") != "chemworld-g2-agent-system-comparison-0.1"
        or payload.get("status") != "completed_audited_two_agent-system_demonstration"
        or observed != expected
        or any(row["closed"] != row["assays"] + row["discards"] for row in observed.values())
    ):
        raise ManuscriptLanguageLockError("G2 120/84/36 evidence changed")
    return {
        "closed_lifecycles": 120,
        "distinct_complete_agent_systems": 2,
        "explicit_discards": 36,
        "final_assays": 84,
        "system_partition": expected,
    }


def _validate_figure_contracts(
    figure_system: Mapping[str, Any], figure_6_manifest: Mapping[str, Any]
) -> dict[str, Any]:
    _validate_self_hash(figure_system, "system_sha256", "figure system")
    _validate_self_hash(figure_6_manifest, "manifest_sha256", "Figure 6 manifest")
    figures = figure_system.get("figures")
    if not isinstance(figures, list) or len(figures) != 6:
        raise ManuscriptLanguageLockError("figure system no longer defines six figures")
    orders = [row.get("order") for row in figures if isinstance(row, Mapping)]
    ids = [row.get("figure_id") for row in figures if isinstance(row, Mapping)]
    acceptance = _mapping(figure_system, "acceptance_rules")
    census = _mapping(figure_6_manifest, "evidence_census")
    boundary = _mapping(figure_6_manifest, "claim_boundary")
    if (
        orders != EXPECTED_FIGURE_ORDER
        or ids != [f"F{number}" for number in EXPECTED_FIGURE_ORDER]
        or acceptance.get("first_references_follow_numeric_order") is not True
        or figure_6_manifest.get("figure_id") != "F6"
        or census.get("best_vs_raw_terminal_sign_discordant_pairs") != 2
        or census.get("complete_matched_pairs") != 8
        or census.get("mixed_world_by_core_metric_classifications") != 6
        or census.get("world_by_core_metric_classifications") != 8
        or boundary.get("two_of_eight_endpoint_result_is_diagnostic") is not True
        or boundary.get("six_of_eight_mixed_result_is_supporting_threshold_sensitive") is not True
        or boundary.get("selected_worlds_are_development_selected") is not True
        or boundary.get("population_level_material_information_claim") is not False
    ):
        raise ManuscriptLanguageLockError("figure or 2/8--6/8 contract changed")
    return {
        "expected_first_reference_order": EXPECTED_FIGURE_ORDER,
        "fresh_complete_pairs": 8,
        "selected_worlds": 2,
        "two_of_eight_role": "endpoint_diagnostic",
        "six_of_eight_role": "threshold_sensitive_supporting_evidence",
    }


def _finding(
    finding_id: str, lock: str, lines: list[int], current: str, required: str
) -> dict[str, Any]:
    return {
        "current": current,
        "finding_id": finding_id,
        "lines": lines,
        "lock": lock,
        "required": required,
        "severity": "blocking_for_final_manuscript_integration",
    }


def _audit_manuscript(lines: list[str]) -> dict[str, Any]:
    text = "\n".join(lines)
    observed_order, first_references = _first_figure_references(lines)
    first_120 = _line_hits(lines, re.compile(r"\b120\b"))
    explicit_84 = _line_hits(lines, re.compile(r"(?<!\d)84(?!\d)"))
    explicit_36 = _line_hits(lines, re.compile(r"(?<!\d)36(?!\d)"))
    prohibited_terms = {
        "independently_configured": re.compile(r"\bindependently configured\b", re.I),
        "closed_vessels": re.compile(r"\bclosed vessels\b", re.I),
        "arbitrary_recombination": re.compile(r"\bcan therefore be recombined\b", re.I),
    }
    term_hits = {name: _line_hits(lines, pattern) for name, pattern in prohibited_terms.items()}

    sensitivity_context = " ".join(text.split())
    sensitivity_passed = all(
        phrase in sensitivity_context
        for phrase in (
            "two of eight complete pairs are sign-discordant with best score",
            "analysis as a supporting sensitivity summary",
            "six of eight selected world-by-lifecycle cells as mixed",
            "That categorical count is supporting rather than the main result",
            "two deliberately selected worlds",
            "not a population estimate",
        )
    )

    findings: list[dict[str, Any]] = []
    if observed_order != EXPECTED_FIGURE_ORDER:
        present_lines = sorted(
            int(row["line"]) for row in first_references if row["line"] is not None
        )
        findings.append(
            _finding(
                "FIGURE_FIRST_REFERENCE_ORDER",
                "figures_1_through_6_first_referenced_in_numeric_order",
                present_lines,
                f"observed first-reference sequence {observed_order}; Figure 2 is absent",
                "integrate first textual references in the exact sequence [1, 2, 3, 4, 5, 6]",
            )
        )
    first_120_line = int(first_120[0]["line"]) if first_120 else 0
    if not first_120 or not explicit_84:
        findings.append(
            _finding(
                "FIRST_120_COUNT_LOCK",
                "first_120_mention_states_full_terminal_partition",
                [first_120_line] if first_120_line else [],
                (
                    "the first mention gives 120 plus system-specific counts but never "
                    "states 84 total final assays"
                ),
                "120 closed lifecycles: 84 final assays and 36 explicit discards",
            )
        )
    for name, hits in term_hits.items():
        if hits:
            required = {
                "independently_configured": "distinct complete agent systems",
                "closed_vessels": "closed lifecycles",
                "arbitrary_recombination": (
                    "preregistered, qualified interventions on named world components; "
                    "no arbitrary-recombination claim"
                ),
            }[name]
            findings.append(
                _finding(
                    f"TERMINOLOGY_{name.upper()}",
                    "frozen_story_terminology",
                    [int(hit["line"]) for hit in hits],
                    "; ".join(str(hit["text"]) for hit in hits),
                    required,
                )
            )
    if not sensitivity_passed:
        findings.append(
            _finding(
                "SENSITIVITY_2_OF_8_6_OF_8",
                "endpoint_diagnostic_and_threshold_sensitive_supporting_roles",
                [],
                "required semantic distinctions are incomplete",
                "2/8 is the endpoint diagnostic; 6/8 is threshold-sensitive supporting evidence",
            )
        )

    allowed_protocol_terms = {
        "g0": _line_hits(lines, re.compile(r"\bG0\b")),
        "g2": _line_hits(lines, re.compile(r"\bG2\b")),
        "negative_leaderboard_boundary": _line_hits(
            lines, re.compile(r"does not depend on .*leaderboard", re.I)
        ),
    }
    return {
        "current_manuscript_compliant": not findings,
        "finding_count": len(findings),
        "findings": findings,
        "figure_first_references": {
            "expected_sequence": EXPECTED_FIGURE_ORDER,
            "first_reference_by_figure": first_references,
            "observed_sequence": observed_order,
            "passed": observed_order == EXPECTED_FIGURE_ORDER,
        },
        "counting_lock": {
            "explicit_36_lines": [int(row["line"]) for row in explicit_36],
            "explicit_84_lines": [int(row["line"]) for row in explicit_84],
            "first_120_line": first_120_line or None,
            "passed": bool(first_120 and explicit_84),
            "required_first_mention": (
                "120 closed lifecycles: 84 final assays and 36 explicit discards"
            ),
        },
        "sensitivity_lock": {
            "passed": sensitivity_passed,
            "six_of_eight_role": "threshold_sensitive_supporting_evidence",
            "two_of_eight_role": "endpoint_diagnostic",
        },
        "terminology_lock": {
            "allowed_context_hits": allowed_protocol_terms,
            "passed": not any(term_hits.values()),
            "prohibited_hits": term_hits,
        },
    }


def _integration_actions(audit: Mapping[str, Any]) -> list[dict[str, Any]]:
    references = _mapping(audit, "figure_first_references")
    first_rows = references.get("first_reference_by_figure")
    if not isinstance(first_rows, list):
        raise ManuscriptLanguageLockError("first-reference rows are missing")
    lines = sorted(int(row["line"]) for row in first_rows if row.get("line") is not None)
    counting = _mapping(audit, "counting_lock")
    terminology = _mapping(audit, "terminology_lock")
    prohibited = _mapping(terminology, "prohibited_hits")

    def hit_lines(name: str) -> list[int]:
        hits = prohibited.get(name)
        if not isinstance(hits, list):
            return []
        return [int(hit["line"]) for hit in hits]

    return [
        {
            "action_id": "S07-A1",
            "lines": lines,
            "owner_handoff": "W1-S10 manuscript integrator",
            "replacement_or_rule": (
                "First-reference sequence must be F1 apparatus, F2 known-policy validity, "
                "F3 terminal policy, F4 compiled controls, F5 primitive lifecycle, "
                "F6 fresh process."
            ),
        },
        {
            "action_id": "S07-A2",
            "lines": [counting.get("first_120_line")],
            "owner_handoff": "W1-S03/W1-S10 abstract integration",
            "replacement_or_rule": (
                "Two distinct complete agent systems produced 120 closed lifecycles: "
                "84 final assays and 36 explicit discards across five matched worlds."
            ),
        },
        {
            "action_id": "S07-A3",
            "lines": hit_lines("closed_vessels"),
            "owner_handoff": "W1-S10 display-item integration",
            "replacement_or_rule": (
                "Replace '120 closed vessels' with the frozen lifecycle partition."
            ),
        },
        {
            "action_id": "S07-A4",
            "lines": hit_lines("arbitrary_recombination"),
            "owner_handoff": "W1-S09/W1-S10 limitations integration",
            "replacement_or_rule": (
                "Replace arbitrary recombination wording with preregistered, qualified "
                "interventions "
                "on named components while authority and audit semantics remain fixed."
            ),
        },
        {
            "action_id": "S07-A5",
            "lines": [],
            "owner_handoff": "W1-S10 final scan",
            "replacement_or_rule": (
                "Retain the current semantic hierarchy: 2/8 endpoint diagnostic; "
                "6/8 threshold-sensitive supporting evidence; selected worlds are descriptive."
            ),
        },
    ]


def build_language_lock_audit(root: Path = ROOT) -> dict[str, Any]:
    """Build the source-bound manuscript lock audit and integration handoff."""

    resolved = root.resolve()
    manuscript_text = (resolved / MANUSCRIPT_PATH).read_text(encoding="utf-8")
    story_text = (resolved / STORY_PATH).read_text(encoding="utf-8")
    _validate_story_contract(story_text)
    g2 = _read_json(resolved / G2_COMPARISON_PATH)
    figure_system = _read_json(resolved / FIGURE_SYSTEM_PATH)
    figure_6 = _read_json(resolved / FIGURE_6_MANIFEST_PATH)
    frozen_counts = _validate_g2_evidence(g2)
    sensitivity_contract = _validate_figure_contracts(figure_system, figure_6)
    manuscript_audit = _audit_manuscript(manuscript_text.splitlines())

    source_paths = (
        MANUSCRIPT_PATH,
        STORY_PATH,
        G2_COMPARISON_PATH,
        FIGURE_SYSTEM_PATH,
        FIGURE_6_MANIFEST_PATH,
    )
    receipt: dict[str, Any] = {
        "schema_id": "chemworld.work_i_manuscript_language_lock_audit",
        "schema_version": "0.1.0",
        "audit_id": "work-i-w1-s07-manuscript-language-lock-audit-v0.1",
        "owner_task": "W1-S07",
        "status": (
            "compliant"
            if manuscript_audit["current_manuscript_compliant"]
            else "integration_changes_required"
        ),
        "source_bindings": [
            {
                "bytes": (resolved / path).stat().st_size,
                "path": path.as_posix(),
                "sha256": _file_sha256(resolved / path),
            }
            for path in source_paths
        ],
        "frozen_counting_evidence": frozen_counts,
        "frozen_figure_and_sensitivity_contract": sensitivity_contract,
        "current_manuscript_audit": manuscript_audit,
        "integration_actions": _integration_actions(manuscript_audit),
        "write_boundary": {
            "display_items_edited": False,
            "figure_assets_edited": False,
            "manuscript_edited": False,
            "paper_arxiv_main_edited": False,
            "proposal_is_line_addressed_to_bound_manuscript_sha256": True,
        },
        "claim_boundary": {
            "six_of_eight_promoted_to_primary_result": False,
            "two_selected_worlds_generalized_to_population": False,
            "work_ii_rule_learning_claimed": False,
        },
    }
    receipt["receipt_sha256"] = receipt_sha256(receipt)
    return receipt


def build_markdown_report(receipt: Mapping[str, Any]) -> str:
    """Render a concise integration-facing manuscript audit."""

    audit = _mapping(receipt, "current_manuscript_audit")
    references = _mapping(audit, "figure_first_references")
    counting = _mapping(audit, "counting_lock")
    sensitivity = _mapping(audit, "sensitivity_lock")
    findings = audit.get("findings")
    actions = receipt.get("integration_actions")
    if not isinstance(findings, list) or not isinstance(actions, list):
        raise ManuscriptLanguageLockError("report findings or actions are invalid")
    rows = [
        "# Work I manuscript language-lock audit",
        "",
        f"Status: **{receipt['status']}**",
        f"Receipt SHA-256: `{receipt['receipt_sha256']}`",
        "",
        "| Lock | Current result | Required result |",
        "| --- | --- | --- |",
        (f"| Figure first references | {references['observed_sequence']} | [1, 2, 3, 4, 5, 6] |"),
        (
            f"| First 120 mention | line {counting['first_120_line']}; 84 absent | "
            "120 closed lifecycles: 84 final assays and 36 explicit discards |"
        ),
        (
            f"| 2/8 vs 6/8 | {'PASS' if sensitivity['passed'] else 'FAIL'} | "
            "2/8 diagnostic; 6/8 threshold-sensitive supporting evidence |"
        ),
        (
            f"| Terminology | {len(findings) - 2} residual findings plus figure/count locks | "
            "frozen S02 terms |"
        ),
        "",
        "## Blocking findings for final integration",
        "",
    ]
    for finding in findings:
        line_text = ", ".join(str(line) for line in finding["lines"]) or "n/a"
        rows.append(f"- `{finding['finding_id']}` (lines {line_text}): {finding['required']}.")
    rows.extend(["", "## Integration actions", ""])
    for action in actions:
        line_text = (
            ", ".join(str(line) for line in action["lines"] if line is not None) or "final scan"
        )
        rows.append(
            f"- `{action['action_id']}` ({action['owner_handoff']}; lines {line_text}): "
            f"{action['replacement_or_rule']}"
        )
    rows.extend(
        [
            "",
            "The current sensitivity language already preserves the registered hierarchy and needs",
            "no scientific reinterpretation. W1-S07 did not edit the manuscript or any shared "
            "hot file.",
            "",
        ]
    )
    return "\n".join(rows)


def _json_text(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    receipt = build_language_lock_audit(ROOT)
    if args.check:
        committed = _read_json(ROOT / REPORT_JSON_PATH)
        if committed.get("receipt_sha256") != receipt_sha256(committed):
            raise SystemExit("committed manuscript lock audit self-hash mismatch")
        if committed != receipt:
            raise SystemExit("committed manuscript lock audit differs from deterministic rebuild")
        if (ROOT / REPORT_MD_PATH).read_text(encoding="utf-8") != build_markdown_report(receipt):
            raise SystemExit("committed Markdown audit differs from deterministic rebuild")
    else:
        (ROOT / REPORT_JSON_PATH).write_text(_json_text(receipt), encoding="utf-8", newline="\n")
        (ROOT / REPORT_MD_PATH).write_text(
            build_markdown_report(receipt), encoding="utf-8", newline="\n"
        )
    print(
        json.dumps(
            {
                "check": bool(args.check),
                "finding_count": receipt["current_manuscript_audit"]["finding_count"],
                "receipt_sha256": receipt["receipt_sha256"],
                "status": receipt["status"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
