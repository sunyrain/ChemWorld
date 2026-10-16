"""Scientific contracts for the matched-world experiment, not model success tests."""

from __future__ import annotations

from copy import deepcopy

import pytest

from chemworld.physchem.abductive_worlds import (
    ASSAY_STD,
    METRICS,
    build_config,
    build_queries,
    build_worlds,
    diagnostic_queries,
    initial_queries,
    solve_query,
)
from chemworld.world.world_family import AxisIntervention


def test_pairs_change_only_association_topology_and_legal_axes():
    worlds = build_worlds()
    assert len(worlds) == 10
    for a, b in zip(worlds[::2], worlds[1::2], strict=True):
        assert a["world_seed"] == b["world_seed"] == 0
        left = deepcopy(a["private_authoring"])
        right = deepcopy(b["private_authoring"])
        for key in ("mechanism_id", "mechanism_family", "association_beta_L_per_mol"):
            left.pop(key)
            right.pop(key)
        assert left == right
        assert b["world_interventions"][:-1] == a["world_interventions"]
        for world in (a, b):
            for row in world["world_interventions"]:
                AxisIntervention(**row)


def test_reference_doses_clear_material_rule_and_are_low_information():
    queries = initial_queries()
    assert sum(q["final_state"]["solvent_L"] for q in queries) <= 0.16
    for q in queries:
        assert q["final_state"]["reagent_mol"] > 5e-7
        assert q["final_state"]["solvent_L"] <= 0.08
    worlds = build_worlds()
    for a, b in zip(worlds[::2], worlds[1::2], strict=True):
        for query in queries:
            left, right = solve_query(a, query)["metrics"], solve_query(b, query)["metrics"]
            assert all(abs(left[m] - right[m]) <= ASSAY_STD[m] for m in METRICS)


def test_accessible_diagnostics_discriminate_each_pair():
    worlds = build_worlds()
    for a, b in zip(worlds[::2], worlds[1::2], strict=True):
        counts = []
        for query in diagnostic_queries():
            left, right = solve_query(a, query)["metrics"], solve_query(b, query)["metrics"]
            counts.append(sum(abs(left[m] - right[m]) >= 3 * ASSAY_STD[m] for m in METRICS))
        assert sum(c >= 1 for c in counts) >= 3
        assert sum(c >= 2 for c in counts) >= 2


def test_mass_charge_and_equilibrium_closure_on_every_planned_state():
    for world in build_worlds():
        for query in initial_queries() + diagnostic_queries() + build_queries():
            row = solve_query(world, query)
            state = row["physical_state"]
            total = query["final_state"]["concentration_mol_L"]
            volume = query["final_state"]["solvent_L"]
            solid = state["precipitated_mol"] / volume
            acid = state["undissociated_acid_mol_L"] + state["free_conjugate_base_mol_L"]
            acid += state["aqueous_pair_mol_L"] + solid
            cation = state["free_cation_mol_L"] + state["aqueous_pair_mol_L"] + solid
            assert acid == pytest.approx(total, rel=1e-7, abs=1e-14)
            assert cation == pytest.approx(0.15 * total, rel=1e-7, abs=1e-14)
            assert state["equilibrium_residual"] <= 1e-7
            assert all(0 <= value <= 1 for value in row["metrics"].values())


def test_heldout_controls_preserve_final_state_and_source_resource_limits():
    queries = build_queries()
    assert [q["query_id"] for q in queries] == [f"Q{i:02d}" for i in range(1, 13)]
    assert sum(len(q["actions"]) for q in queries) < 180
    assert sum(q["final_state"]["reagent_mol"] for q in queries) < 0.24
    assert sum(q["final_state"]["solvent_L"] for q in queries) < 0.72
    for world in build_worlds():
        predictions = {q["query_id"]: solve_query(world, q)["metrics"] for q in queries}
        for anchor, control in (
            ("Q04", "Q07"),
            ("Q04", "Q08"),
            ("Q05", "Q09"),
            ("Q05", "Q10"),
            ("Q06", "Q11"),
            ("Q06", "Q12"),
        ):
            assert predictions[anchor] == pytest.approx(predictions[control], abs=1e-9)


def test_config_keeps_base_untouched_and_separates_thirty_sessions_from_assays():
    base = {"unrelated": {"preserved": True}, "worlds": ["old"]}
    config = build_config(base)
    assert base["worlds"] == ["old"]
    config["unrelated"]["preserved"] = False
    assert base["unrelated"]["preserved"] is True
    assert config["counts"]["independent_source_sessions"] == 30
    assert config["counts"]["source_batches"] == 360
    assert config["counts"]["reference_assays"] == 20
    assert config["arms"] == ["Opaque"]
