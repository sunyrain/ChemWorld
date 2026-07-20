"""Live-LLM controller with explicit public mechanism-belief diagnostics."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from chemworld.agents.interaction import AgentDecisionContext
from chemworld.agents.live_llm import LiveLLMAgent

DIAGNOSTIC_PROMPT_VERSION = "chemworld-mechanism-diagnostic-prompt-0.2"


class MechanismDiagnosticLiveLLMAgent(LiveLLMAgent):
    """Require falsifiable mechanism beliefs in addition to the selected action."""

    name = "mechanism_diagnostic_live_llm"

    def __init__(
        self,
        *args: Any,
        mechanism_candidates: tuple[str, ...],
        **kwargs: Any,
    ) -> None:
        if len(mechanism_candidates) < 2 or len(set(mechanism_candidates)) != len(
            mechanism_candidates
        ):
            raise ValueError("mechanism_candidates must contain at least two unique IDs")
        if "no_change" not in mechanism_candidates:
            raise ValueError("mechanism_candidates must include no_change")
        self.mechanism_candidates = tuple(mechanism_candidates)
        super().__init__(*args, **kwargs)

    def act_with_public_view(
        self,
        context: AgentDecisionContext,
        public_view: dict[str, Any],
    ) -> dict[str, Any]:
        action = super().act_with_public_view(context, public_view)
        if self._last_decision is not None and self._recent_decisions:
            for key in (
                "mechanism_belief",
                "mechanism_prediction",
                "change_probability",
                "expected_information_gain",
                "diagnostic_measurement_rationale",
            ):
                if key in self._last_decision:
                    self._recent_decisions[-1][key] = self._last_decision[key]
        return action

    def manifest(self) -> dict[str, Any]:
        payload = super().manifest()
        diagnostic_contract = {
            "version": DIAGNOSTIC_PROMPT_VERSION,
            "mechanism_candidates": list(self.mechanism_candidates),
            "required_fields": [
                "mechanism_belief",
                "change_probability",
                "expected_information_gain",
                "diagnostic_measurement_rationale",
            ],
        }
        payload.update(
            {
                "diagnostic_prompt_version": DIAGNOSTIC_PROMPT_VERSION,
                "diagnostic_prompt_sha256": hashlib.sha256(
                    json.dumps(
                        diagnostic_contract,
                        sort_keys=True,
                        separators=(",", ":"),
                    ).encode("utf-8")
                ).hexdigest(),
                "mechanism_candidates": list(self.mechanism_candidates),
                "diagnostic_claim_boundary": (
                    "public candidate diagnostic; not a formal mechanism-adaptation result"
                ),
            }
        )
        return payload

    def _build_prompt(
        self,
        context: AgentDecisionContext,
        public_view: dict[str, Any],
    ) -> str:
        payload = json.loads(super()._build_prompt(context, public_view))
        payload["instruction"] += (
            " The hidden world law may remain stable or may change during the campaign. "
            "Do not infer a change from experiment count alone. Use only released evidence "
            "to maintain a normalized belief over the supplied candidate mechanism IDs. "
            "Report the expected information value of the selected next operation; this is "
            "a public forecast and will be scored against subsequent belief change. "
            "A completed experiment is mandatory. The campaign state exposes "
            "diagnostic_actions_used_current_experiment and "
            "diagnostic_per_experiment_action_limit. Reserve the final two action slots "
            "for terminate followed by measure with instrument=final_assay; once used "
            "actions reach limit minus two, stop optional diagnostics and begin closeout."
        )
        payload["mechanism_diagnostic_contract"] = {
            "version": DIAGNOSTIC_PROMPT_VERSION,
            "candidate_ids": list(self.mechanism_candidates),
            "belief_semantics": "probability distribution summing to one",
            "change_probability_semantics": (
                "probability that the current hidden law differs from the initial regime"
            ),
            "expected_information_gain_semantics": (
                "0 means no expected reduction in mechanism uncertainty; 1 means maximal"
            ),
            "ground_truth_withheld": True,
        }
        payload["required_json_shape"]["diagnostic_report"] = {
            "mechanism_belief": dict.fromkeys(self.mechanism_candidates, "probability from 0 to 1"),
            "change_probability": "number from 0 to 1",
            "expected_information_gain": "number from 0 to 1",
            "diagnostic_measurement_rationale": (
                "concise statement of which hypotheses the action distinguishes"
            ),
        }
        return json.dumps(payload, ensure_ascii=False, sort_keys=True)

    def _normalize_decision(
        self,
        payload: dict[str, Any],
        *,
        context: AgentDecisionContext,
    ) -> dict[str, Any]:
        decision = super()._normalize_decision(payload, context=context)
        diagnostic = payload.get("diagnostic_report")
        if not isinstance(diagnostic, dict):
            raise ValueError("model decision is missing diagnostic_report")
        raw_belief = diagnostic.get("mechanism_belief")
        if not isinstance(raw_belief, dict) or set(raw_belief) != set(self.mechanism_candidates):
            raise ValueError("mechanism_belief must contain exactly the candidate IDs")
        belief: dict[str, float] = {}
        for candidate in self.mechanism_candidates:
            value = raw_belief[candidate]
            if isinstance(value, bool) or not isinstance(value, int | float):
                raise ValueError("mechanism belief values must be numeric")
            probability = float(value)
            if not 0.0 <= probability <= 1.0:
                raise ValueError("mechanism belief values must be in [0, 1]")
            belief[candidate] = probability
        total = sum(belief.values())
        if not 0.98 <= total <= 1.02:
            raise ValueError("mechanism belief probabilities must sum to one")
        belief = {key: value / total for key, value in belief.items()}

        change_probability = _probability(
            diagnostic.get("change_probability"),
            "change_probability",
        )
        expected_information_gain = _probability(
            diagnostic.get("expected_information_gain"),
            "expected_information_gain",
        )
        rationale = str(diagnostic.get("diagnostic_measurement_rationale") or "").strip()
        if not rationale:
            raise ValueError("diagnostic_measurement_rationale must be non-empty")
        decision.update(
            {
                "mechanism_belief": belief,
                "mechanism_prediction": max(belief, key=belief.__getitem__),
                "change_probability": change_probability,
                "expected_information_gain": expected_information_gain,
                "diagnostic_measurement_rationale": rationale,
            }
        )
        return decision

    def _failure_decision(
        self,
        context: AgentDecisionContext,
        error: Exception,
    ) -> dict[str, Any]:
        decision = super()._failure_decision(context, error)
        uniform = 1.0 / len(self.mechanism_candidates)
        decision.update(
            {
                "mechanism_belief": dict.fromkeys(self.mechanism_candidates, uniform),
                "mechanism_prediction": "no_change",
                "change_probability": 0.5,
                "expected_information_gain": 0.0,
                "diagnostic_measurement_rationale": (
                    "No diagnostic forecast was available because the model decision failed."
                ),
            }
        )
        return decision


def _probability(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"{field} must be numeric")
    probability = float(value)
    if not 0.0 <= probability <= 1.0:
        raise ValueError(f"{field} must be in [0, 1]")
    return probability


__all__ = ["DIAGNOSTIC_PROMPT_VERSION", "MechanismDiagnosticLiveLLMAgent"]
