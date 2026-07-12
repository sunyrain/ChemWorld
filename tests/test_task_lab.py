from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

import pytest
from apps.task_lab.catalog import TASK_BACKGROUNDS, task_catalog
from apps.task_lab.classic_runner import run_classic_task
from apps.task_lab.deepseek_client import DeepSeekAPIError, DeepSeekClient, JsonCompletion
from apps.task_lab.experiment_audit import audit_experiment_design
from apps.task_lab.interaction_semantics import (
    aligned_affordance,
    operation_semantics,
    validate_interactive_action,
)
from apps.task_lab.runner import run_task
from apps.task_lab.server import RunJobManager, _read_api_key_file
from apps.task_lab.spectral_payload import spectral_payload
from apps.task_lab.student_session import StudentSessionManager

from chemworld.data.logging import load_jsonl
from chemworld.tasks import list_tasks
from chemworld.world.operations import OPERATION_TYPES


class FakePlannerClient:
    model = "fake-json-planner"

    def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
    ) -> JsonCompletion:
        del system_prompt, max_tokens
        request = json.loads(user_prompt)
        task_id = request.get("task_contract", {}).get("task_id")
        if task_id == "equilibrium-characterization":
            actions = [
                _decision({"operation": "add_solvent", "volume_L": 0.028, "solvent": 2}),
                _decision({"operation": "add_reagent", "amount_mol": 0.010}),
                _decision({"operation": "measure", "instrument": "ph_meter"}),
                _decision({"operation": "add_reagent", "amount_mol": 0.004}),
                _decision({"operation": "measure", "instrument": "ph_meter"}),
                _decision({"operation": "terminate"}),
                _decision({"operation": "measure", "instrument": "final_assay"}),
            ]
        else:
            actions = [
                _decision({"operation": "add_solvent", "volume_L": 0.028, "solvent": 2}),
                _decision({"operation": "add_reagent", "amount_mol": 0.010}),
                _decision(
                    {
                        "operation": "add_catalyst",
                        "catalyst_amount_mol": 0.00025,
                        "catalyst": 1,
                    }
                ),
                _decision(
                    {
                        "operation": "heat",
                        "target_temperature_K": 378.0,
                        "duration_s": 1350.0,
                        "stirring_speed_rpm": 720.0,
                    }
                ),
                _decision({"operation": "measure", "instrument": "hplc"}),
                _decision({"operation": "quench"}),
                _decision({"operation": "terminate"}),
                _decision({"operation": "measure", "instrument": "final_assay"}),
            ]
        return JsonCompletion(
            payload={"strategy_summary": "offline test plan", "actions": actions},
            model=self.model,
            usage={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        )


class IncompleteAssayPlannerClient:
    model = "fake-incomplete-planner"

    def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
    ) -> JsonCompletion:
        del system_prompt, user_prompt, max_tokens
        actions = [
            _decision({"operation": "add_solvent", "volume_L": 0.028, "solvent": 2}),
            _decision({"operation": "add_reagent", "amount_mol": 0.010}),
            _decision({"operation": "terminate"}),
        ]
        return JsonCompletion(
            payload={"strategy_summary": "plan omits final assay", "actions": actions},
            model=self.model,
            usage={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        )


class FlakyJsonClient(DeepSeekClient):
    def __init__(self) -> None:
        super().__init__(
            api_key="test-only-key",
            model="fake-json-model",
            thinking=True,
            reasoning_effort="max",
        )
        self.request_count = 0
        self.bodies: list[dict[str, Any]] = []

    def _send(self, body: dict[str, Any]) -> tuple[str, str | None]:
        self.bodies.append(body)
        self.request_count += 1
        content = "" if self.request_count == 1 else '{"action": {"operation": "terminate"}}'
        envelope = {
            "id": f"request-{self.request_count}",
            "model": self.model,
            "choices": [
                {
                    "message": {
                        "content": content,
                        "reasoning_content": "PRIVATE_REASONING_MUST_NOT_BE_RETAINED",
                    }
                }
            ],
            "usage": {"prompt_tokens": 3, "completion_tokens": 2, "total_tokens": 5},
        }
        return json.dumps(envelope), None


class AdaptiveAuditClient:
    model = "fake-adaptive-auditor"

    def __init__(self) -> None:
        self.prompts: list[dict[str, Any]] = []
        self.action_index = 0
        self.actions = [
            {"operation": "add_solvent", "volume_L": 0.028, "solvent": 2},
            {"operation": "add_reagent", "amount_mol": 0.010},
            {
                "operation": "add_catalyst",
                "catalyst_amount_mol": 0.00025,
                "catalyst": 1,
            },
            {
                "operation": "heat",
                "target_temperature_K": 378.0,
                "duration_s": 1350.0,
                "stirring_speed_rpm": 720.0,
            },
            {"operation": "measure", "instrument": "hplc"},
            {"operation": "quench"},
            {"operation": "terminate"},
            {"operation": "measure", "instrument": "final_assay"},
        ]

    def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
    ) -> JsonCompletion:
        del system_prompt, max_tokens
        prompt = json.loads(user_prompt)
        self.prompts.append(prompt)
        if (
            self.action_index == 5
            and prompt["available_spectra"]
            and not prompt["retrieved_spectra"]
        ):
            return JsonCompletion(
                payload={"spectrum_request_id": prompt["available_spectra"][-1]["spectrum_id"]},
                model=self.model,
                usage={"prompt_tokens": 4, "completion_tokens": 2, "total_tokens": 6},
            )
        action = self.actions[self.action_index]
        self.action_index += 1
        spectrum = next(
            (item for item in reversed(prompt["retrieved_spectra"]) if item.get("available")),
            None,
        )
        return JsonCompletion(
            payload={
                "action": action,
                "evidence": ["The latest public report was reviewed."],
                "spectrum_interpretation": (
                    "The HPLC trace contains a dominant reactant peak."
                    if spectrum
                    else "No spectrum was inspected for this decision."
                ),
                "rationale": "Choose the next valid operation from public evidence.",
                "hypothesis": "The next observation will reduce uncertainty.",
                "uncertainty": 0.35,
                "uncertainty_note": "Limited public measurements.",
            },
            model=self.model,
            usage={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        )


class LateFailureAdaptiveClient(AdaptiveAuditClient):
    def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
    ) -> JsonCompletion:
        if len(self.prompts) == 7:
            self.prompts.append(json.loads(user_prompt))
            raise DeepSeekAPIError(
                "late invalid JSON",
                attempts=3,
                usage={"prompt_tokens": 30, "completion_tokens": 6, "total_tokens": 36},
            )
        return super().complete_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=max_tokens,
        )


class RetrievedSpectrumRepairClient(AdaptiveAuditClient):
    """Request one spectrum, reject the associated action, then repair it."""

    def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
    ) -> JsonCompletion:
        prompt = json.loads(user_prompt)
        if str(prompt.get("instruction", "")).startswith("Repair the rejected action"):
            self.prompts.append(prompt)
            return JsonCompletion(
                payload={"action": {"operation": "quench"}},
                model=self.model,
                usage={"prompt_tokens": 3, "completion_tokens": 2, "total_tokens": 5},
            )
        if self.action_index == 5 and prompt.get("retrieved_spectra"):
            self.prompts.append(prompt)
            self.action_index += 1
            return JsonCompletion(
                payload={"action": {"operation": "measure", "instrument": "final_assay"}},
                model=self.model,
                usage={"prompt_tokens": 3, "completion_tokens": 2, "total_tokens": 5},
            )
        return super().complete_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=max_tokens,
        )


class RepeatedCampaignClient(AdaptiveAuditClient):
    def __init__(self) -> None:
        super().__init__()
        recipe = [
            {"operation": "add_solvent", "volume_L": 0.028, "solvent": 2},
            {"operation": "add_reagent", "amount_mol": 0.010},
            {
                "operation": "add_catalyst",
                "catalyst_amount_mol": 0.00025,
                "catalyst": 1,
            },
            {
                "operation": "heat",
                "target_temperature_K": 378.0,
                "duration_s": 1350.0,
                "stirring_speed_rpm": 720.0,
            },
            {"operation": "terminate"},
            {"operation": "measure", "instrument": "final_assay"},
        ]
        self.actions = [*recipe, *recipe]


class RepeatingInvalidClient:
    model = "fake-repeating-invalid"
    thinking = False

    def __init__(self) -> None:
        self.prompts: list[dict[str, Any]] = []

    def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
    ) -> JsonCompletion:
        del system_prompt, max_tokens
        self.prompts.append(json.loads(user_prompt))
        return JsonCompletion(
            payload={
                "action": {
                    "operation": "heat",
                    "temperature_K": 360.0,
                    "duration_s": 600.0,
                    "total_volume_L": 0.02,
                }
            },
            model=self.model,
            usage={"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
        )


def _decision(action: dict[str, Any]) -> dict[str, Any]:
    return {
        "action": action,
        "rationale": "exercise the public protocol",
        "hypothesis": "the operation will improve observable evidence",
    }


def test_task_catalog_covers_every_registered_task() -> None:
    task_ids = {task.task_id for task in list_tasks()}
    assert set(TASK_BACKGROUNDS) == task_ids
    assert {card["task_id"] for card in task_catalog()} == task_ids
    reaction_card = next(card for card in task_catalog() if card["task_id"] == "reaction-to-assay")
    assert reaction_card["classic_active_learning_compatible"] is True


def test_classic_active_learning_runs_repeated_extended_campaign(tmp_path: Path) -> None:
    events: list[dict[str, Any]] = []
    result = run_classic_task(
        agent_id="gp_bo",
        task_id="reaction-to-assay",
        output_dir=tmp_path,
        seed=0,
        max_steps=36,
        budget_multiplier=2.0,
        campaign_override=True,
        event_callback=events.append,
    )
    assert result.status == "scored_extended"
    assert result.contract_profile == "extended-research"
    assert result.official_score is None
    assert result.research_score is not None
    assert result.final_assay_count >= 3
    assert result.verified is True
    decisions = [event for event in events if event["type"] == "surrogate_decision"]
    assert decisions[0]["phase"] == "initial"
    assert any(event["phase"] == "acquisition" for event in decisions)
    records = [json.loads(line) for line in Path(result.trajectory_path).read_text().splitlines()]
    assert records[0]["contract_profile"] == "extended-research"
    assert records[0]["budget"] == 36
    assert records[0]["official_budget"] == 18


@pytest.mark.parametrize(
    "task_id",
    ["reaction-to-assay", "equilibrium-characterization"],
)
def test_offline_task_lab_pilots_write_verified_scores(tmp_path: Path, task_id: str) -> None:
    events: list[dict[str, Any]] = []
    result = run_task(
        client=FakePlannerClient(),
        task_id=task_id,
        output_dir=tmp_path,
        mode="plan",
        max_steps=12,
        event_callback=events.append,
    )
    assert result.status == "scored"
    assert result.official_score is not None
    assert result.final_assay_count == 1
    assert result.invalid_plan_actions == 0
    assert Path(result.trajectory_path).is_file()
    assert Path(result.result_path or "").is_file()
    verified = json.loads(Path(result.result_path or "").read_text(encoding="utf-8"))
    assert verified["verified"] is True
    assert events[0]["type"] == "task_started"
    assert any(event["type"] == "step_completed" for event in events)
    assert events[-1]["type"] == "task_completed"


def test_student_session_rejects_invalid_action_without_spending_budget() -> None:
    manager = StudentSessionManager()
    try:
        session = manager.create("reaction-to-assay", seed=0)
        before = session.state()["campaign_state"]
        rejected = session.step({"operation": "heat", "duration_s": 10.0})
        after = rejected["state"]["campaign_state"]
        assert rejected["accepted"] is False
        assert after["operation_count"] == before["operation_count"]
        accepted = session.step({"operation": "add_solvent", "volume_L": 0.028, "solvent": 2})
        assert accepted["accepted"] is True
        assert accepted["state"]["campaign_state"]["operation_count"] == 1
        assert accepted["state"]["history"][0]["action"]["operation"] == "add_solvent"
        assert accepted["state"]["history"][0]["state_effects"]["delta_volume_L"] == (
            pytest.approx(0.028)
        )
        assert accepted["state"]["public_vessel"]["vessel_relation"] == "cumulative"
        assert accepted["state"]["public_vessel"]["net_volume_delta_L"] == pytest.approx(0.028)
        solvent_affordance = next(
            item
            for item in accepted["state"]["available_actions"]
            if item["operation"] == "add_solvent"
        )
        assert solvent_affordance["recipe_lock"] == {"field": "solvent", "value": 2}
        solvent_field = next(
            field for field in solvent_affordance["fields"] if field["field"] == "solvent"
        )
        assert solvent_field["choices"] == [2]
        switched = session.step({"operation": "add_solvent", "volume_L": 0.005, "solvent": 1})
        assert switched["accepted"] is False
        assert "payload_locked:solvent" in switched["validation"]["invalid_reasons"]
        assert switched["state"]["campaign_state"]["operation_count"] == 1
    finally:
        manager.close_all()


def test_student_session_exposes_measurement_withdrawal_for_animation() -> None:
    manager = StudentSessionManager()
    try:
        session = manager.create("reaction-to-assay", seed=0)
        actions = [
            {"operation": "add_solvent", "volume_L": 0.028, "solvent": 2},
            {"operation": "add_reagent", "amount_mol": 0.010},
            {
                "operation": "add_catalyst",
                "catalyst_amount_mol": 0.00025,
                "catalyst": 1,
            },
            {
                "operation": "heat",
                "target_temperature_K": 360.0,
                "duration_s": 600.0,
                "stirring_speed_rpm": 720.0,
            },
            {"operation": "measure", "instrument": "hplc"},
        ]
        result: dict[str, Any] = {}
        for action in actions:
            result = session.step(action)
            assert result["accepted"] is True
        effects = result["record"]["state_effects"]
        assert effects["type"] == "destructive_measurement"
        assert effects["visual"] == "measure"
        assert effects["sample_delta_L"] == pytest.approx(0.0002)
        assert effects["delta_volume_L"] == pytest.approx(-0.0002)
        assert result["state"]["public_vessel"]["sampled_volume_L"] == pytest.approx(0.0002)
        assert result["state"]["lab_report"]["spectra_summary"]["channel_count"] == 1
        assert "1 displayed channel(s)" in result["state"]["lab_report"]["text"]
    finally:
        manager.close_all()


def test_plan_mode_closes_out_an_unfinished_model_plan(tmp_path: Path) -> None:
    events: list[dict[str, Any]] = []
    result = run_task(
        client=IncompleteAssayPlannerClient(),
        task_id="reaction-to-assay",
        output_dir=tmp_path,
        mode="plan",
        max_steps=10,
        event_callback=events.append,
    )
    assert result.status == "scored"
    assert result.official_score is not None
    assert result.final_assay_count == 1
    assert result.model_call_count == 1
    closeout_operations = [
        event["action"]["operation"] for event in events if event["type"] == "closeout_action"
    ]
    assert closeout_operations == ["measure"]


def test_deepseek_json_client_retries_empty_output_and_aggregates_usage() -> None:
    client = FlakyJsonClient()
    completion = client.complete_json(system_prompt="json", user_prompt="return json")
    assert completion.attempts == 2
    assert completion.payload["action"]["operation"] == "terminate"
    assert completion.usage == {
        "prompt_tokens": 6,
        "completion_tokens": 4,
        "total_tokens": 10,
        "prompt_cache_hit_tokens": 0,
        "prompt_cache_miss_tokens": 0,
    }
    assert client.bodies[0]["thinking"] == {"type": "enabled"}
    assert client.bodies[0]["reasoning_effort"] == "max"
    assert "PRIVATE_REASONING_MUST_NOT_BE_RETAINED" not in json.dumps(
        asdict(completion),
        sort_keys=True,
    )


def test_adaptive_runner_reads_public_spectrum_and_emits_audit_record(
    tmp_path: Path,
) -> None:
    client = AdaptiveAuditClient()
    events: list[dict[str, Any]] = []
    result = run_task(
        client=client,
        task_id="reaction-to-assay",
        output_dir=tmp_path,
        mode="adaptive",
        max_steps=10,
        event_callback=events.append,
    )
    assert result.status == "scored"
    assert result.model_call_count == 9
    assert client.prompts[0]["available_spectra"] == []
    assert client.prompts[0]["retrieved_spectra"] == []
    semantics = client.prompts[0]["state_semantics"]
    assert "current state" in semantics["current_vessel"]
    assert "spectrum_request_id" in client.prompts[0]["instruction"]
    assert client.prompts[0]["instruction"].startswith(
        "Return either one spectrum_request_id"
    )
    assert client.prompts[5]["available_spectra"]
    assert client.prompts[5]["retrieved_spectra"] == []
    assert client.prompts[5]["latest_lab_report"]["spectra_summary"] == {
        "has_spectral_packet": True,
        "instrument": "hplc",
        "retrieval_required": True,
    }
    assert client.prompts[6]["retrieved_spectra"][0]["available"] is True
    assert client.prompts[7]["available_spectra"]
    assert client.prompts[7]["retrieved_spectra"] == []
    decisions = [event for event in events if event["type"] == "decision_ready"]
    assert len(decisions) == 8
    assert decisions[0]["evidence"] == ["The latest public report was reviewed."]
    assert decisions[0]["uncertainty"] == pytest.approx(0.35)
    requested = [event for event in events if event["type"] == "spectrum_requested"]
    retrieved = [event for event in events if event["type"] == "spectrum_retrieved"]
    assert len(requested) == len(retrieved) == 1
    assert requested[0]["spectrum_id"] == retrieved[0]["spectrum_id"]
    assert decisions[5]["spectrum_input"]["available"] is True
    assert decisions[5]["spectrum_input"]["provenance"] == {
        "source": "measurement_output",
        "measurement_step": 5,
        "experiment_index": 0,
        "vessel_relation": "current_experiment",
    }
    assert decisions[5]["decision_origin"] == "online_model"
    assert decisions[5]["vessel_state"] == "cumulative_same_experiment"
    assert decisions[5]["experiment_index"] == 0
    assert decisions[5]["analysis"]["spectrum_interpretation"].startswith("The HPLC trace")
    assert decisions[6]["spectrum_input"]["available"] is False
    assert result.method_resources["accounting_complete"] is False
    assert result.method_resources["model_provenance"]["private_reasoning_retained"] is False
    records = load_jsonl(result.trajectory_path)
    assert records[-1]["method_resources"]["model_call_count"] == 9
    assert "PRIVATE_REASONING_MUST_NOT_BE_RETAINED" not in json.dumps(
        records,
        sort_keys=True,
    )
    spectral_steps = [
        event
        for event in events
        if event["type"] == "step_completed" and event["spectrum"]["available"]
    ]
    assert spectral_steps
    assert spectral_steps[0]["spectrum"]["series"][0]["kind"] == "hplc_chromatogram"
    assert spectral_steps[0]["decision_origin"] == "online_model"


def test_task_lab_static_ui_exposes_model_input_and_public_analysis() -> None:
    static_root = Path(__file__).resolve().parents[1] / "apps" / "task_lab" / "static"
    html = (static_root / "agent.html").read_text(encoding="utf-8")
    javascript = (static_root / "agent.js").read_text(encoding="utf-8")
    student_html = (static_root / "student.html").read_text(encoding="utf-8")
    student_javascript = (static_root / "student.js").read_text(encoding="utf-8")

    assert "MODEL INPUT / MEASUREMENT OUTPUT" in html
    assert 'id="agentSpectrumContext"' in html
    assert 'id="decisionIntent"' in html
    assert 'id="decisionComparison"' in html
    assert 'id="agentSpectrumHistory"' in html
    assert 'id="spectrumHistoryPrev"' in html
    assert 'id="spectrumHistoryNext"' in html
    assert 'id="liveVessel"' in html
    assert "PUBLIC MODEL ANALYSIS" in html
    assert "event.spectrum_input" in javascript
    assert "recordSpectrumSnapshot" in javascript
    assert "showSpectrumSnapshot" in javascript
    assert 'event.type === "spectrum_requested"' in javascript
    assert 'event.type === "spectrum_retrieved"' in javascript
    assert "spectrum_history" in javascript
    assert 'id="studentSpectrumHistory"' in student_html
    assert 'id="studentSpectrumHistoryPrev"' in student_html
    assert 'id="studentSpectrumHistoryNext"' in student_html
    assert "renderStudentSpectrumHistory" in student_javascript
    assert "showStudentSpectrumSnapshot" in student_javascript
    assert 'class="thermal-waves"' in student_html
    assert 'class="instrument-beam"' in student_html
    assert 'class="crystal-bed"' in student_html
    assert 'id="effectDeltas"' in student_html
    assert "state_effects" in student_javascript
    assert "public_vessel" in student_javascript
    assert "reasoning_content" not in javascript


def test_local_api_key_file_is_private_and_status_is_redacted(tmp_path: Path) -> None:
    key_path = tmp_path / "api.md"
    secret = "sk-private-test-value"
    key_path.write_text(secret + "\n", encoding="utf-8")

    api_key = _read_api_key_file(key_path)
    manager = RunJobManager(output_root=tmp_path / "runs", api_key=api_key)
    public_status = {
        "deepseek_configured": manager.deepseek_configured,
        "credential_source": manager.credential_source,
    }

    assert api_key == secret
    assert public_status == {
        "deepseek_configured": True,
        "credential_source": "api-key-file",
    }
    assert secret not in json.dumps(public_status)


def test_repository_ignores_local_api_key_file() -> None:
    gitignore = (Path(__file__).resolve().parents[1] / ".gitignore").read_text(encoding="utf-8")
    assert "/api.md" in gitignore.splitlines()


def test_task_lab_preserves_core_input_contract_and_adds_effect_semantics() -> None:
    assert all(
        operation_semantics(operation)["visual"] != "generic" for operation in OPERATION_TYPES
    )
    seed = aligned_affordance(
        {
            "operation": "seed_crystals",
            "schema": {
                "operation": "seed_crystals",
                "required_fields": ["seed_mass_g"],
                "fields": [
                    {
                        "field": "seed_mass_g",
                        "bounds": {"low": 0.0, "high": 0.05},
                        "recommended_range": {"low": 0.0, "high": 0.05},
                    }
                ],
            },
        },
        [],
    )
    assert seed["fields"][0]["bounds"] == {"low": 0.0, "high": 0.05}
    assert seed["effect"]["visual"] == "seed"

    phase = aligned_affordance(
        {
            "operation": "add_phase",
            "schema": {
                "operation": "add_phase",
                "fields": [
                    {"field": "phase", "choices": ["aqueous", "organic"]},
                    {"field": "volume_L", "bounds": {"low": 0.0, "high": 0.06}},
                ],
            },
        },
        [],
    )
    assert phase["fields"][0]["choices"] == ["aqueous", "organic"]
    assert phase["fields"][1]["bounds"] == {"low": 0.0, "high": 0.06}

    selection = aligned_affordance(
        {
            "operation": "separate_phase",
            "schema": {
                "operation": "separate_phase",
                "fields": [
                    {
                        "field": "target_phase",
                        "choices": ["aqueous", "organic"],
                    }
                ],
            },
        },
        [],
    )
    assert selection["fields"][0]["choices"] == ["aqueous", "organic"]


def test_task_lab_delegates_input_validation_to_core_contract() -> None:
    class Base:
        @staticmethod
        def validate_action(action: dict[str, Any]) -> dict[str, Any]:
            return {"valid": False, "canonical_action": action, "invalid_reasons": ["core"]}

    action = {"operation": "seed_crystals", "seed_mass_g": 0.01}
    assert validate_interactive_action(Base(), action, [{"ignored": True}]) == {
        "valid": False,
        "canonical_action": action,
        "invalid_reasons": ["core"],
    }


def test_adaptive_campaign_reuses_compact_completed_experiment_memory(
    tmp_path: Path,
) -> None:
    client = RepeatedCampaignClient()
    events: list[dict[str, Any]] = []
    result = run_task(
        client=client,
        task_id="reaction-to-assay",
        output_dir=tmp_path,
        mode="adaptive",
        max_steps=16,
        budget_multiplier=2.0,
        campaign_override=True,
        event_callback=events.append,
    )
    assert result.status == "scored_extended"
    assert result.final_assay_count == 2
    assert client.prompts[6]["completed_experiment_memory"][0]["conditions"]
    assert client.prompts[6]["state_semantics"]["current_experiment_index"] == 1
    assert (
        client.prompts[6]["available_spectra"][0]["provenance"]["vessel_relation"]
        == "completed_previous_experiment"
    )
    assert client.prompts[6]["available_spectra"][0]["provenance"]["experiment_index"] == 0
    assert client.prompts[6]["retrieved_spectra"] == []
    learned = [event for event in events if event["type"] == "experiment_learned"]
    assert len(learned) == 2
    assert learned[0]["final_score"] is not None
    assert learned[1]["design_audit"]["classification"] == "replication"
    assert result.experiment_design_audit["replication_count"] == 1
    verified = json.loads(Path(result.result_path or "").read_text(encoding="utf-8"))
    assert verified["experiment_design_audit"]["comparison_count"] == 1


def test_experiment_design_audit_detects_controls_replication_and_multi_factor() -> None:
    def experiment(
        index: int,
        score: float,
        *,
        catalyst: int,
        heat_program: list[tuple[float, float]],
    ) -> dict[str, Any]:
        conditions = [
            {"operation": "add_solvent", "solvent": 1, "volume_L": 0.04},
            {"operation": "add_reagent", "amount_mol": 0.01},
            {
                "operation": "add_catalyst",
                "catalyst": catalyst,
                "catalyst_amount_mol": 0.001,
            },
            *[
                {
                    "operation": "heat",
                    "target_temperature_K": temperature,
                    "duration_s": duration,
                    "stirring_speed_rpm": 600.0,
                }
                for temperature, duration in heat_program
            ],
        ]
        return {
            "experiment_index": index,
            "final_score": score,
            "conditions": conditions,
        }

    experiments = [
        experiment(0, 0.41, catalyst=0, heat_program=[(350.0, 1800.0), (370.0, 1800.0)]),
        experiment(1, 0.35, catalyst=1, heat_program=[(350.0, 1800.0)]),
        experiment(2, 0.49, catalyst=0, heat_program=[(360.0, 1800.0)]),
        experiment(3, 0.49, catalyst=0, heat_program=[(360.0, 1800.0)]),
    ]
    audit = audit_experiment_design(experiments)
    comparisons = audit["comparisons"]
    assert comparisons[1]["classification"] == "multi_factor_change"
    assert {item["factor"] for item in comparisons[1]["changed_factors"]} == {
        "catalyst_charge",
        "thermal_program",
    }
    assert comparisons[2]["classification"] == "controlled_single_factor"
    assert comparisons[2]["reference_experiment_index"] == 0
    assert comparisons[3]["classification"] == "replication"
    assert audit["controlled_single_factor_count"] == 1
    assert audit["multi_factor_change_count"] == 1
    assert audit["replication_count"] == 1


def test_spectrum_disclosure_levels_remove_assignments_and_peak_table() -> None:
    raw_signal = {
        "kind": "hplc_chromatogram",
        "time_min": [1.0, 1.5, 2.0],
        "intensity": [0.0, 10.0, 0.0],
        "peaks": [
            {
                "retention_time_min": 1.5,
                "assignment": "P",
                "group": "target",
                "area": 12.5,
            }
        ],
    }
    assigned = spectral_payload(raw_signal, disclosure="assigned")
    unassigned = spectral_payload(raw_signal, disclosure="unassigned")
    raw = spectral_payload(raw_signal, disclosure="raw")
    assert assigned["series"][0]["peaks"][0]["group"] == "target"
    assert unassigned["series"][0]["peaks"][0] == {
        "center": 1.5,
        "label": "unassigned",
        "group": "unknown",
        "area": 12.5,
        "detected": True,
    }
    assert raw["series"][0]["peaks"] == []
    assert raw["disclosure"] == "raw"


def test_raw_spectrum_mode_redacts_prompt_peak_assignments(tmp_path: Path) -> None:
    client = AdaptiveAuditClient()
    result = run_task(
        client=client,
        task_id="reaction-to-assay",
        output_dir=tmp_path,
        mode="adaptive",
        max_steps=10,
        spectrum_disclosure="raw",
    )
    assert result.spectrum_disclosure == "raw"
    assert client.prompts[5]["retrieved_spectra"] == []
    public_spectrum = client.prompts[6]["retrieved_spectra"][0]
    assert public_spectrum["disclosure"] == "raw"
    assert public_spectrum["series"][0]["peaks"] == []
    spectra_summary = client.prompts[5]["latest_lab_report"]["spectra_summary"]
    assert "peak_group_fractions" not in spectra_summary
    assert "dominant_peak" not in spectra_summary


def test_adaptive_runner_stops_a_repeating_unrepairable_decision_loop(
    tmp_path: Path,
) -> None:
    events: list[dict[str, Any]] = []
    client = RepeatingInvalidClient()
    result = run_task(
        client=client,
        task_id="reaction-to-assay",
        output_dir=tmp_path,
        mode="adaptive",
        max_steps=10,
        event_callback=events.append,
    )
    assert result.status == "no_final_assay"
    assert result.steps == 0
    assert result.invalid_plan_actions == 3
    assert result.model_call_count == 6
    assert any(event["type"] == "decision_loop_stopped" for event in events)
    repair_prompts = [
        prompt
        for prompt in client.prompts
        if str(prompt.get("instruction", "")).startswith("Repair the rejected action")
    ]
    assert repair_prompts
    assert all(prompt["available_spectra"] == [] for prompt in repair_prompts)
    assert all(prompt["retrieved_spectra"] == [] for prompt in repair_prompts)


def test_adaptive_runner_preserves_scoring_when_a_late_model_call_fails(
    tmp_path: Path,
) -> None:
    events: list[dict[str, Any]] = []
    client = LateFailureAdaptiveClient()
    result = run_task(
        client=client,
        task_id="reaction-to-assay",
        output_dir=tmp_path,
        mode="adaptive",
        max_steps=10,
        event_callback=events.append,
    )
    assert result.status == "scored"
    assert result.final_assay_count == 1
    assert result.model_call_count == 12
    assert result.usage == {
        "prompt_tokens": 114,
        "completion_tokens": 48,
        "total_tokens": 162,
        "prompt_cache_hit_tokens": 0,
        "prompt_cache_miss_tokens": 0,
    }
    assert any(event["type"] == "model_call_failed" for event in events)
    assert any(event["type"] == "closeout_action" for event in events)
    repair_prompt = next(
        prompt
        for prompt in client.prompts
        if str(prompt.get("instruction", "")).startswith("Repair the rejected action")
    )
    assert repair_prompt["available_spectra"]
    assert repair_prompt["retrieved_spectra"] == []
    assert all("series" not in item for item in repair_prompt["available_spectra"])


def test_adaptive_repair_receives_only_explicitly_retrieved_spectrum(
    tmp_path: Path,
) -> None:
    client = RetrievedSpectrumRepairClient()
    events: list[dict[str, Any]] = []
    result = run_task(
        client=client,
        task_id="reaction-to-assay",
        output_dir=tmp_path,
        mode="adaptive",
        max_steps=10,
        event_callback=events.append,
    )

    assert result.status == "scored"
    repair_prompt = next(
        prompt
        for prompt in client.prompts
        if str(prompt.get("instruction", "")).startswith("Repair the rejected action")
    )
    assert len(repair_prompt["retrieved_spectra"]) == 1
    retrieved = repair_prompt["retrieved_spectra"][0]
    assert retrieved["available"] is True
    assert retrieved["series"]
    catalog_ids = {item["spectrum_id"] for item in repair_prompt["available_spectra"]}
    assert retrieved["spectrum_id"] in catalog_ids
    assert all("series" not in item for item in repair_prompt["available_spectra"])
    assert len([event for event in events if event["type"] == "spectrum_retrieved"]) == 1


def test_adaptive_runner_reserves_two_steps_for_scoring_protocol(tmp_path: Path) -> None:
    events: list[dict[str, Any]] = []
    result = run_task(
        client=AdaptiveAuditClient(),
        task_id="reaction-to-assay",
        output_dir=tmp_path,
        mode="adaptive",
        max_steps=7,
        event_callback=events.append,
    )
    assert result.status == "scored"
    assert result.steps == 7
    assert result.model_call_count == 5
    closeout_actions = [
        event["action"]["operation"] for event in events if event["type"] == "closeout_action"
    ]
    assert closeout_actions == ["terminate", "measure"]
