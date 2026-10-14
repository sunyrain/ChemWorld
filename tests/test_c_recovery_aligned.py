from collections import Counter

import gymnasium as gym
import pytest
from scripts import run_c_recovery_aligned as block
from scripts import run_work_ii_c_formal as c
from scripts.run_paper_case_notebooks import read, write

from chemworld.foundation import upsert_equipment_record
from chemworld.foundation.state import PhaseLedger, PhaseRecord, ProcessLedger, SpeciesLedger
from chemworld.runtime.full_process_contract import FULL_PROCESS_FREE_RESEARCH_CONTRACT
from chemworld.runtime.species import MechanismSpeciesView


def test_actual_assay_uses_initial_charge_not_internal_stage_recovery():
    env = gym.make(
        "ChemWorld",
        task_id=c.pilot.TASK,
        seed=0,
        full_process_contract_id=FULL_PROCESS_FREE_RESEARCH_CONTRACT,
    )
    try:
        env.reset(seed=0)
        base = env.unwrapped
        species = MechanismSpeciesView(base.scenario_instance.compiled_mechanism)
        target, feed = species.target_species[0], species.feed_species[0]
        state = base._state
        # Partial conversion: 0.01 mol available before separation from 0.02 mol feed.
        # Solid contains 0.006 mol, of which 0.001 mol is purchased seed.
        base._state = state.replace(
            species=SpeciesLedger(initial_amounts_mol={feed: 0.02}),
            process=ProcessLedger(
                metrics={
                    "crystal_yield": 0.5,
                    "pre_separation_product_mol": 0.01,
                }
            ),
            phases=PhaseLedger(
                {
                    "solid": PhaseRecord(
                        phase_id="solid",
                        vessel_id="test",
                        phase_type="solid",
                        volume_L=0.001,
                        species_amounts_mol={target: 0.006},
                    )
                }
            ),
            equipment=upsert_equipment_record(
                state.equipment,
                equipment_id="crystallizer",
                equipment_type="crystallizer",
                attached_vessel_id="batch_reactor",
                status="configured",
                settings={"seed_target_mol": 0.001},
            ),
        )
        truth = base.observation_kernel._truth_values(base._state)
        assert truth["crystal_yield"] == pytest.approx(0.25)
        assert base._state.process.metrics["crystal_yield"] == 0.5
        assert (
            "tracked initial reagent charge"
            in c.full_process_operational_state(base, {})["sampling_contract"]
        )
    finally:
        env.close()


def test_schedule_and_corrected_design_preserve_original_science(tmp_path):
    rows = block.schedule()
    assert len({(r["repeat"], r["id"]) for r in rows}) == 45
    assert Counter(r["arm"] for r in rows) == dict.fromkeys(c.pilot.ARMS, 15)
    assert set(Counter(r["id"] for r in rows).values()) == {3}
    assert sum(r["batches"] for r in rows) == 540
    old_bytes = block.DEFAULT_INPUT.read_bytes()
    old = read(block.DEFAULT_INPUT)
    refs = tmp_path / "retained"
    for world in range(1, 6):
        write(refs / f"C-W{world:02d}/result.json", {"truth": []})
    root = tmp_path / "new"
    block.prepare(root, references_root=refs)
    design = read(root / "repeat-01/C/design.json")
    for key in ("queries", "K1", "K2", "posttest_numerics", "model", "resolution"):
        assert design[key] == old[key]
    assert "tracked initial reagent charge" in design["systems"]["12"]
    assert "tracked initial reagent charge" in design["Q"]
    assert block.DEFAULT_INPUT.read_bytes() == old_bytes
    assert read(root / "design.json")["planned_sources"] == 45
    with pytest.raises(FileExistsError):
        block.prepare(root, references_root=refs)


def test_reference_numeric_drift_stops_before_participants(tmp_path, monkeypatch):
    refs = tmp_path / "retained"
    for world in range(1, 6):
        write(refs / f"C-W{world:02d}/result.json", {"truth": [{"crystal_yield": 0.25}]})
    root = tmp_path / "new"
    block.prepare(root, references_root=refs)
    monkeypatch.setattr(
        c,
        "fixed",
        lambda *a, **kw: {
            "passed": True,
            "batches": [{}] * 12,
            "truth": [{"crystal_yield": 0.5}],
        },
    )
    with pytest.raises(RuntimeError, match="Numerical semantics changed"):
        block.references(root, {})
    assert not (root / "references/complete.json").exists()
