"""Checks for observed cross-system execution failures on the P entry path."""

from scripts import run_work_ii_p_study as study

from chemworld.eval.resource_accounting import MethodResourceLedger, MethodResourceLimits


def test_resource_rejection_is_retained_but_not_retested():
    records = [
        {
            "experiment_index": 0,
            "step": 1,
            "transaction_status": "committed",
            "action": {"operation": "terminate"},
        },
        {
            "experiment_index": 0,
            "step": 2,
            "transaction_status": "campaign_resource_rejected",
            "action": {"operation": "measure", "instrument": "hplc"},
        },
        {
            "experiment_index": 0,
            "step": 3,
            "transaction_status": "committed",
            "action": {"operation": "measure", "instrument": "final_assay"},
            "instrument": "final_assay",
        },
    ]
    recipe = study.recipe_from_records(records, 1)
    assert len(recipe["actions"]) == 2
    assert recipe["rejected_attempts"][0]["transaction_status"] == "campaign_resource_rejected"


def test_foreign_query_schema_cannot_silently_score():
    queries = study.gate.queries("v3")
    observations = [{"purity": 0.7, "recovery": 0.2}] * 12
    foreign = {"predictions": [{"query_id": q["query_id"], "crystal_yield": 0.2} for q in queries]}
    assert not study.evaluate(foreign, observations, queries)["valid"]


def test_prediction_intervals_and_low_recovery_are_valid_outcomes():
    queries = study.gate.queries("v3")
    observations = [{"purity": 0.7, "recovery": 0.01}] * 12
    interval = {"estimate": 0.2, "lower80": 0.1, "upper80": 0.3}
    payload = {
        "predictions": [
            {"query_id": q["query_id"], "purity": interval, "recovery": interval} for q in queries
        ]
    }
    result = study.evaluate(payload, observations, queries)
    assert result["valid"]
    assert result["metrics"]["recovery"]["coverage80"] == 0
    assert result["metrics"]["purity"]["mae"] > 0.49


def test_two_percent_resolution_keeps_decimal_boundary_small():
    queries = study.gate.queries("v3")
    observations = [{"purity": 0.5, "recovery": 0.5}] * 12
    payload = {
        "predictions": [
            {
                "query_id": q["query_id"],
                **{
                    metric: {"estimate": 0.84 if i % 2 else 0.82, "lower80": 0, "upper80": 1}
                    for metric in study.METRICS
                },
            }
            for i, q in enumerate(queries)
        ]
    }
    result = study.evaluate(payload, observations, queries)
    assert result["valid"] and all(p["correct"] for p in result["pairs"])
    payload["predictions"][1]["purity"]["estimate"] = 0.840001
    assert not study.evaluate(payload, observations, queries)["pairs"][0]["correct"]


def test_actual_resource_ledger_accepts_one_bounded_pending_session():
    ledger = MethodResourceLedger(MethodResourceLimits(**study.SOURCE_LIMITS), True)
    usage = {
        "schema_version": "chemworld-method-resource-usage-0.1",
        "accounting_complete": False,
        "provider_usage_pending": True,
        "in_flight_model_call_count": 1,
        "provider_call_accounting_complete": True,
        "provider_token_accounting_complete": False,
        "monetary_accounting_complete": False,
        "model_call_count": 1,
        "model_provenance": dict.fromkeys(
            (
                "provider",
                "model_id",
                "model_snapshot_or_access_date",
                "prompt_hash",
                "request_parameters",
                "tokenizer_or_provider_usage_source",
            )
        ),
    }
    ledger.record_decision(elapsed_s=1, agent_usage=usage)
    assert ledger.snapshot()["development_deferred_provider_usage"]
    assert ledger.operation_count == 1


def test_startup_recovery_never_repeats_accepted_science_or_quota_failure(tmp_path):
    stdout = tmp_path / "source-stdout.jsonl"
    stderr = tmp_path / "source-stderr.txt"
    stdout.write_text("", encoding="utf-8")
    stderr.write_text("required MCP servers failed to initialize: chemworld_lab", encoding="utf-8")
    result = {"source": {"operations": 0}, "posttests": {}}
    assert study.startup_failure(tmp_path, result)
    result["source"]["operations"] = 1
    assert not study.startup_failure(tmp_path, result)
    result["source"]["operations"] = 0
    stdout.write_text('{"thread_id":"accepted"}', encoding="utf-8")
    assert not study.startup_failure(tmp_path, result)
    stdout.write_text("", encoding="utf-8")
    stderr.write_text("quota exceeded", encoding="utf-8")
    assert not study.startup_failure(tmp_path, result)


def test_service_unavailable_retries_only_provider_events_without_quota_or_auth(tmp_path):
    path = tmp_path / "stdout.jsonl"
    unavailable = "unexpected status 503 Service Unavailable"
    path.write_text('{"type":"error","message":"' + unavailable + '"}', encoding="utf-8")
    assert study.retryable_transport(path)
    path.write_text(
        '{"type":"error","message":"' + unavailable + '; quota exceeded"}', encoding="utf-8"
    )
    assert not study.retryable_transport(path)
    path.write_text(
        '{"type":"item.completed","message":"' + unavailable + '"}', encoding="utf-8"
    )
    assert not study.retryable_transport(path)
