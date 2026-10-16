from scripts import summarize_abductive_resources as s


def receipt(n, *, thread="same-thread", failure=None):
    return {
        "thread_id": thread,
        "usage": {"input_tokens": n * 10, "cached_input_tokens": n * 4, "output_tokens": n},
        "failure": failure,
    }


def test_last_cumulative_receipt_is_total_not_sum_of_turns():
    source, followup = receipt(10), receipt(15)
    source["session_elapsed_s"], followup["elapsed_s"] = 10, 5
    result = s.chain_summary("unit", [("source", source), ("K1", followup)], terminal=True)
    assert result["total_tokens"]["output_tokens"] == 15
    assert result["stages"][1]["increment_since_previous_receipt"]["output_tokens"] == 5
    assert result["token_accounting_complete"] is True
    assert result["backend_api_requests"] is None
    assert result["monetary_cost_usd"] is None
    assert result["observed_receipt_elapsed_sum_s"] == 15


def test_missing_and_failed_usage_is_unknown_not_zero():
    unavailable = receipt(0)
    unavailable["usage_observed"] = False
    assert s.normalized_usage(unavailable) is None
    failed = s.chain_summary(
        "failure", [("source", {"failure": "startup"})], terminal=True, failure="startup"
    )
    assert failed["total_tokens"] is None
    assert failed["observed_cumulative_tokens"] is None
    partial = s.chain_summary("partial", [("source", receipt(10)), ("K1", {})], terminal=True)
    assert partial["total_tokens"] is None
    assert partial["latest_observed_cumulative_receipt"]["tokens"]["output_tokens"] == 10
    assert partial["stages"][1]["increment_since_previous_receipt"] is None


def test_nonmonotonic_or_changed_thread_is_not_a_valid_total():
    for second in (receipt(5), receipt(20, thread="another-thread")):
        result = s.chain_summary("unit", [("source", receipt(10)), ("K1", second)], terminal=True)
        assert result["total_tokens"] is None
        assert result["token_accounting_complete"] is False
        assert result["monotonicity_or_thread_issues"]


def test_group_keeps_failed_units_and_technical_blocks_separate():
    good = s.chain_summary("good", [("source", receipt(10))], terminal=True)
    failed = s.chain_summary("failed", [], terminal=True, failure="worker exit")
    group = s.aggregate("retained", "technical", 30, [good, failed], not_started=28)
    assert group["started_units"] == 2
    assert group["not_started_units"] == 28
    assert group["observed_tokens_from_latest_receipts"]["output_tokens"] == 10
    assert group["total_tokens_for_started_units"] is None
    assert group["units_with_incomplete_token_accounting"] == 1
