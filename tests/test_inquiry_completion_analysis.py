from scripts.analyze_inquiry_completion import fit_references, path_record, preparation


def event(cursor, batch, action, observed=None, status="committed"):
    return {
        "cursor": cursor,
        "batch": batch,
        "action": action,
        "observations": observed or {},
        "transaction_status": status,
    }


def test_references_ignore_rejected_material_and_nonfinal_observation():
    events = [
        event(1, 1, {"operation": "add_solvent", "solvent": 2, "volume_L": 0.08}),
        event(2, 1, {"operation": "add_solvent", "solvent": 3}, status="rejected"),
        event(3, 1, {"operation": "measure", "instrument": "hplc"}, {"crystal_purity": 0.1}),
        event(
            4, 1, {"operation": "measure", "instrument": "final_assay"}, {"crystal_purity": 0.98}
        ),
        event(5, 2, {"operation": "add_solvent", "solvent": 1, "volume_L": 0.08}),
        event(
            6, 2, {"operation": "measure", "instrument": "final_assay"}, {"crystal_purity": 0.96}
        ),
    ]
    queries = [
        {"query_id": "a", "actions": [{"operation": "add_solvent", "solvent": 2}]},
        {"query_id": "b", "actions": [{"operation": "add_solvent", "solvent": 0}]},
    ]
    a, b = fit_references(events, queries)
    assert a["source_mean"]["crystal_purity"] == 0.97
    assert a["same_solvent_mean"]["crystal_purity"] == 0.98
    assert not a["fallback"] and a["same_solvent_batches"] == 1
    assert b["fallback"] and b["same_solvent_mean"]["crystal_purity"] == 0.97
    assert a["source_mean"]["crystal_size"] is None
    # Changing evaluator-only data cannot change reference fitting.
    for q in queries:
        q["truth"] = {"crystal_purity": -100}
    assert fit_references(events, queries) == [a, b]
    events.insert(3, event(7, 1, {"operation": "resuspend_crystals", "solvent": 0}))
    assert fit_references(events, queries)[0]["fallback"]


def test_no_final_assay_remains_missing():
    row = fit_references([], [{"query_id": "q", "actions": []}])[0]
    assert row["source_batches"] == 0
    assert all(v is None for v in row["source_mean"].values())


def test_preparation_preserves_topology_but_not_measurement_timing():
    a = [
        {"operation": "add_reagent", "container": 7, "amount_mol": 0.02},
        {"operation": "measure", "container": 7, "instrument": "hplc"},
        {"operation": "transfer", "source_container": 7, "target_container": 8},
    ]
    b = [
        {"operation": "add_reagent", "container": 1, "amount_mol": 0.02},
        {"operation": "transfer", "source_container": 1, "target_container": 2},
    ]
    assert preparation(a) == preparation(b)
    b[-1]["target_container"] = 1
    assert preparation(a) != preparation(b)


def test_path_committed_loading_and_missing_first_choice():
    events = [
        event(1, 1, {"operation": "add_solvent", "solvent": 3}, status="rejected"),
        event(2, 1, {"operation": "add_reagent", "amount_mol": 0.02}),
        event(3, 1, {"operation": "add_component", "component": 0, "amount_mol": 0.01}),
    ]
    row = path_record(events)
    assert row["first_solvent"] is None
    assert row["rejected_operations"] == 1
    assert row["nominal_reagent_mol_max"] == 0.03
    assert row["nominal_reagent_per_added_solvent_M_max"] is None


def test_public_input_comparison_excludes_only_random_campaign_label():
    from scripts.report_inquiry_completion import scientific_public_context

    a = {"initial_public_state": {"campaign_state": {"campaign_id": "a", "budget": 12}}}
    b = {"initial_public_state": {"campaign_state": {"campaign_id": "b", "budget": 12}}}
    assert scientific_public_context(a) == scientific_public_context(b)
    assert a["initial_public_state"]["campaign_state"]["campaign_id"] == "a"
    b["initial_public_state"]["campaign_state"]["budget"] = 11
    assert scientific_public_context(a) != scientific_public_context(b)


def test_opportunity_scores_preserve_five_observation_coverage_and_world_weight():
    from scripts.report_inquiry_completion import METRICS, aggregate, score_queries

    payload = {
        "predictions": [
            {
                "query_id": f"Q{i:02d}",
                "metrics": {m: {"estimate": 0.5, "lower80": 0.4, "upper80": 0.6} for m in METRICS},
            }
            for i in range(1, 13)
        ]
    }
    truth = {
        f"Q{i:02d}": [dict.fromkeys(METRICS, x) for x in (0.3, 0.4, 0.5, 0.6, 0.7)]
        for i in range(1, 13)
    }
    scores = score_queries(payload, truth)
    assert scores["groups"]["dilute"]["queries"] == 3
    assert scores["groups"]["other"]["queries"] == 9
    for m in METRICS:
        assert scores["groups"]["all"]["metrics"][m]["coverage80"] == 0.6
        assert abs(scores["groups"]["all"]["metrics"][m]["interval_score80"] - 0.6) < 1e-12
    import copy

    rows = []
    for world, n, value in (("W01", 3, 0.1), ("W02", 1, 0.5)):
        for repeat in range(n):
            s = copy.deepcopy(scores)
            s["groups"]["all"]["macro_mae"] = value
            rows.append(
                {
                    "world": world,
                    "opportunity": "Research",
                    "status": "completed",
                    "repeat": repeat,
                    "scores": s,
                }
            )
    a = aggregate(rows)
    assert a["equal_world_means"]["Research"]["all"]["macro_mae"] == 0.3
    assert a["equal_world_means"]["NoResearch"]["all"]["macro_mae"] is None
