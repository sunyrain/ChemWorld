"""Opt-in P inventory correction; historical/default runtime remains replayable."""

from contextlib import contextmanager
from dataclasses import replace

from chemworld.foundation import upsert_equipment_record
from chemworld.foundation.state import PhaseLedger, selected_phase_id
from chemworld.runtime.phase_ledger_services import ChemWorldPhaseLedgerServices
from chemworld.runtime.phase_separation_services import ChemWorldPhaseSeparationServices
from chemworld.runtime.vnext_downstream import PhaseSlice, run_bounded_transfer
from chemworld.world.species_roles import PHASE_PRODUCT_AMOUNT_KEY


def is_p(state):
    return state.metadata.get("full_process_task_id") == "reaction-to-purification"


@contextmanager
def inventory_v2():
    """Transfer existing material only; never reconstruct reactor from vessel totals."""
    old_records = ChemWorldPhaseLedgerServices.phase_ledger_records
    old_transfer = ChemWorldPhaseSeparationServices.transfer_phase

    def records(self, state, ledger, **kwargs):
        if is_p(state) and state.phases and "reactor_liquid" in ledger:
            reactor = state.phases.phases.get("reactor_liquid")
            if reactor is not None:
                state = state.replace(species_amounts=dict(reactor.species_amounts_mol))
        return old_records(self, state, ledger, **kwargs)

    def transfer(self, state, action):
        if not is_p(state):
            return old_transfer(self, state, action)
        phases = {} if state.phases is None else state.phases.phases
        target = selected_phase_id(state.phases)
        if target is None:
            target = "organic" if "organic" in phases else "reactor_liquid"
        if target not in phases:
            raise ValueError("Transfer requires an existing liquid phase")
        if target != "reactor_liquid":
            return old_transfer(self, state, action)
        phase = phases[target]
        products = self.phase_ledgers.product_candidate_species()
        impurities = self.phase_ledgers.partition_impurity_candidate_species()
        material = PhaseSlice(
            product_mol=sum(phase.species_amounts_mol.get(k, 0) for k in products),
            impurity_mol=sum(phase.species_amounts_mol.get(k, 0) for k in impurities),
            volume_L=phase.volume_L,
            solvent_loss=0.0,
        )
        if not material.has_material:
            raise ValueError("Transfer requires nonempty source material")
        result = run_bounded_transfer(
            material, fraction=min(1.0, max(0.0, float(action.get("transfer_fraction", 0.98))))
        )
        fraction = result.target_delivered_volume_L / phase.volume_L
        kept = replace(
            phase,
            volume_L=result.target_delivered_volume_L,
            species_amounts_mol={k: v * fraction for k, v in phase.species_amounts_mol.items()},
            selected=True,
        )
        ledger = PhaseLedger(
            {
                key: kept if key == target else replace(value, selected=False)
                for key, value in phases.items()
            }
        )
        discarded = {}
        for name, volume in (
            ("transfer_source_heel", result.source_remaining_volume_L),
            ("transfer_line_holdup", result.final_line_volume_L),
        ):
            discarded[name] = {
                "volume_L": volume,
                "species_amounts_mol": {
                    k: v * volume / phase.volume_L for k, v in phase.species_amounts_mol.items()
                },
            }
        metadata, volume, product, impurity = self._removed_inventory_summary(
            state, operation="transfer", inventories=discarded
        )
        next_state = state.replace(
            phases=ledger,
            species_amounts=ledger.total_amounts_mol(),
            volume_L=sum(p.volume_L for p in ledger.phases.values()),
            metadata={**state.metadata, **metadata},
            ledger=state.ledger.with_updates(cost=state.ledger.cost + 0.01),
            equipment=upsert_equipment_record(
                state.equipment,
                equipment_id="transfer_line",
                equipment_type="finite_holdup_transfer_line",
                attached_vessel_id=state.vessel_id,
                status="transferred",
                settings=metadata,
            ),
        )
        return self._account_removed_inventory(
            next_state,
            removed_volume_L=volume,
            removed_product_mol=product,
            removed_impurity_mol=impurity,
        )

    ChemWorldPhaseLedgerServices.phase_ledger_records = records
    ChemWorldPhaseSeparationServices.transfer_phase = transfer
    try:
        yield
    finally:
        ChemWorldPhaseLedgerServices.phase_ledger_records = old_records
        ChemWorldPhaseSeparationServices.transfer_phase = old_transfer


@contextmanager
def inventory_v3():
    """Also apply drying/concentration to a real receiver before extraction."""
    with inventory_v2():
        old_records = ChemWorldPhaseLedgerServices.phase_ledger_records
        old_dry = ChemWorldPhaseSeparationServices.dry_phase
        old_concentrate = ChemWorldPhaseSeparationServices.concentrate_phase
        old_wash = ChemWorldPhaseSeparationServices.wash_phase
        old_with_phases = ChemWorldPhaseLedgerServices.with_phase_ledger

        def with_phases(self, state, phases_payload, **kwargs):
            result = old_with_phases(self, state, phases_payload, **kwargs)
            return total_volume(result) if is_p(state) else result

        def receiver(state):
            phases = {} if state.phases is None else state.phases.phases
            if is_p(state) and selected_phase_id(state.phases) is None and "organic" not in phases:
                if "reactor_liquid" not in phases:
                    raise ValueError("Operation requires an existing selected liquid phase")
                return state.replace(
                    phases=PhaseLedger(
                        {k: replace(p, selected=k == "reactor_liquid") for k, p in phases.items()}
                    )
                )
            return state

        def records(self, state, ledger, **kwargs):
            output = old_records(self, state, ledger, **kwargs)
            if not is_p(state) or not state.phases or "reactor_liquid" not in ledger:
                return output
            before = state.phases.phases.get("reactor_liquid")
            if before is None:
                return output
            amounts = dict(before.species_amounts_mol)
            for species, key in (
                (self.product_candidate_species(), PHASE_PRODUCT_AMOUNT_KEY),
                (self.partition_impurity_candidate_species(), "impurity_mol"),
            ):
                total = sum(amounts.get(k, 0) for k in species)
                desired = ledger["reactor_liquid"].get(key, 0.0)
                if total == 0 and desired > 1e-12:
                    raise ValueError("Cannot create reactor solute without a source inventory")
                for k in species:
                    if k in amounts:
                        amounts[k] *= desired / total if total else 0.0
            phases = dict(output.phases)
            phases["reactor_liquid"] = replace(
                phases["reactor_liquid"], species_amounts_mol=amounts
            )
            return PhaseLedger(phases)

        def dry(self, state):
            result = old_dry(self, receiver(state))
            return total_volume(result) if is_p(state) else result

        def concentrate(self, state, action):
            result = old_concentrate(self, receiver(state), action)
            return total_volume(result) if is_p(state) else result

        def total_volume(state):
            return state.replace(volume_L=sum(p.volume_L for p in state.phases.phases.values()))

        def wash(self, state, action):
            if is_p(state) and (not state.phases or "organic" not in state.phases.phases):
                raise ValueError("Wash requires an existing organic phase")
            return old_wash(self, state, action)

        ChemWorldPhaseLedgerServices.phase_ledger_records = records
        ChemWorldPhaseLedgerServices.with_phase_ledger = with_phases
        ChemWorldPhaseSeparationServices.dry_phase = dry
        ChemWorldPhaseSeparationServices.concentrate_phase = concentrate
        ChemWorldPhaseSeparationServices.wash_phase = wash
        try:
            yield
        finally:
            ChemWorldPhaseLedgerServices.phase_ledger_records = old_records
            ChemWorldPhaseLedgerServices.with_phase_ledger = old_with_phases
            ChemWorldPhaseSeparationServices.dry_phase = old_dry
            ChemWorldPhaseSeparationServices.concentrate_phase = old_concentrate
            ChemWorldPhaseSeparationServices.wash_phase = old_wash
